"""
Aetox Works — Sales Agent 🗣️
Pipeline step 1: เก็บโจทย์ลูกค้า, pain point, สรุป需求 → ส่ง Research

Tools:
  - CRM (SQLite) — save_lead, list_leads, update_lead_status
  - LLM Summary Generator — extract structured data
  - Web Chat — run_chat_server()
"""
import logging
import json
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm
from src.tools.crm import init_db, save_lead, list_leads, update_lead_status

log = logging.getLogger("aetox.agents.sales")

# โครงสร้าง JSON ที่ Sales Agent ต้อง extract
SALES_JSON_SCHEMA = {
    "customer_name": "",
    "company": "",
    "pain_points": [],
    "needs": [],
    "goals": [],
    "timeline": "",
    "summary_thai": "",
}


def _extract_json(text: str) -> dict:
    """พยายาม extract JSON object จากข้อความ LLM response"""
    # ลองหาทั้ง block ที่อยู่ใน ```json ... ``` หรือ { ... } โดยตรง
    patterns = [
        r"```(?:json)?\s*(\{.*?\})\s*```",
        r"(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
    return {}


def _merge_with_schema(raw: dict) -> dict:
    """เติม default จาก schema และ map field names (รองรับทั้งไทย/อังกฤษ)"""
    result = dict(SALES_JSON_SCHEMA)

    # map field names (รองรับหลายรูปแบบ)
    field_map = {
        "customer_name": ["customer_name", "name", "ชื่อ", "ชื่อลูกค้า", "customer"],
        "company": ["company", "บริษัท", "company_name", "องค์กร", "business"],
        "pain_points": ["pain_points", "pain point", "ปัญหา", "pain", "painpoint"],
        "needs": ["needs", "ความต้องการ", "need", "ต้องการ", "requirements"],
        "goals": ["goals", "เป้าหมาย", "goal", "วัตถุประสงค์", "objective"],
        "timeline": ["timeline", "เวลา", "กำหนด", "deadline", "schedule", "ภายใน"],
        "summary_thai": ["summary_thai", "summary", "สรุป", "สรุปภาษาไทย", "brief"],
    }

    list_fields = {"pain_points", "needs", "goals"}

    for target_key, aliases in field_map.items():
        for alias in aliases:
            if alias in raw and raw[alias] is not None:
                val = raw[alias]
                if isinstance(val, list):
                    result[target_key] = [str(v) for v in val]
                elif target_key in list_fields:
                    # fields ที่ควรเป็น list → wrap string
                    result[target_key] = [str(val)]
                elif isinstance(val, str):
                    result[target_key] = val
                else:
                    result[target_key] = str(val)
                break

    return result


def _parse_lead_from_reply(reply: str) -> dict:
    """
    วิเคราะห์ LLM response → extract structured lead data

    Returns:
        dict with customer_name, company, pain_points, needs, goals, timeline, summary_thai
    """
    parsed = _extract_json(reply)
    if parsed:
        structured = _merge_with_schema(parsed)
        log.info("Sales extracted structured data: %s", list(structured.keys()))
        return structured

    # fallback: ไม่เจอ JSON → ใช้ทั้ง reply เป็น summary
    return {
        **SALES_JSON_SCHEMA,
        "summary_thai": reply[:500],
    }


def sales_node(state: AgentState) -> dict:
    """
    Sales Agent node สำหรับ LangGraph

    Pipeline step 1: รับ input จาก user/supervisor → วิเคราะห์ความต้องการ → extract structured data → บันทึก CRM → ส่งต่อ Research

    Flow:
      1. เรียก LLM ด้วย system prompt + output format
      2. Parse JSON จาก response (extract structured fields)
      3. บันทึก lead ลง CRM แบบมีโครงสร้าง
      4. ส่งคืน structured result ให้ pipeline
    """
    user_input = state.get("input", "")
    system_prompt = get_system_prompt("sales") or "คุณคือ Sales Agent"
    output_format = get_output_format("sales") or ""

    messages_history = state.get("messages", [])

    # เรียก LLM สำหรับวิเคราะห์
    try:
        format_instruction = (
            f"\n\n⚠️ เมื่อคุณมีข้อมูลครบแล้ว ให้ตอบกลับเป็น JSON format นี้เท่านั้น:\n{output_format}"
            if output_format else ""
        )
        reply = call_llm(
            f"ลูกค้าพูดว่า: {user_input}\n\n"
            f"บทสนทนาก่อนหน้า: {json.dumps(messages_history[-6:] if messages_history else [], ensure_ascii=False)}\n\n"
            f"ถามคำถามเพิ่มเติมถ้าข้อมูลยังไม่ครบ "
            f"ถ้าข้อมูลครบแล้วให้สรุปเป็น JSON{format_instruction}",
            system_prompt=system_prompt,
        )
        log.info("Sales LLM reply: %s", reply[:120])
    except Exception as e:
        log.warning("Sales LLM error: %s", e)
        reply = f"[Sales Agent] วิเคราะห์: {user_input[:100]}..."

    # Extract structured data
    lead_data = _parse_lead_from_reply(reply)

    # บันทึก lead ลง CRM
    lead_id = None
    try:
        init_db()
        lead_id = save_lead(
            name=lead_data.get("customer_name", ""),
            company=lead_data.get("company", ""),
            pain_points=lead_data.get("pain_points", []),
            needs=lead_data.get("needs", []),
            goals=lead_data.get("goals", []),
            timeline=lead_data.get("timeline", ""),
            summary=lead_data.get("summary_thai", reply[:500]),
            source="workflow",
        )
        log.info("Sales saved lead #%d: %s / %s", lead_id, lead_data.get("customer_name"), lead_data.get("company"))
    except Exception as e:
        log.warning("Sales CRM error: %s", e)

    # Output for pipeline
    output = json.dumps({
        "agent": "sales",
        "lead_id": lead_id,
        "lead_data": lead_data,
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": {"sales": output},
        "messages": [("system", f"Sales: saved lead #{lead_id} — {lead_data.get('summary_thai', '')[:150]}")],
    }
