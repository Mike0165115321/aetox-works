"""
Aetox Works — Sales Agent 🗣️ (v2 — Multi-turn Sales Conversation)

บทบาท: นักขาย / นักการตลาด
หน้าที่:
  1. คุยกับลูกค้า ถามทีละคำถาม เก็บข้อมูลให้ครบ
  2. เมื่อข้อมูลครบ → สรุปความเข้าใจ → ขอคำยืนยันจากลูกค้า
  3. ลูกค้ายืนยัน → บันทึก lead → ตั้ง sales_confirmed = True → ส่งต่อ Research

ห้าม: สร้าง content, เขียนเว็บ, วิเคราะห์ตลาด — นั่นไม่ใช่งาน Sales
"""
import logging
import json
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm
from src.tools.crm import init_db, save_lead

log = logging.getLogger("aetox.agents.sales")

# ข้อมูลที่ Sales ต้องเก็บให้ครบก่อนขอ confirmation
REQUIRED_FIELDS = ["customer_name", "company", "needs", "goals"]

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


def _parse_conversation(context: str) -> dict:
    """Parse conversation history → extract what's been collected so far"""
    data = dict(SALES_JSON_SCHEMA)

    if not context:
        return data

    # Try extracting from last summary JSON in context
    parsed = _extract_json(context)
    if parsed:
        # Map field names (รองรับทั้งไทย/อังกฤษ)
        field_map = {
            "customer_name": ["customer_name", "name", "ชื่อ", "ชื่อลูกค้า", "customer"],
            "company": ["company", "บริษัท", "company_name", "องค์กร"],
            "pain_points": ["pain_points", "pain point", "ปัญหา", "pain"],
            "needs": ["needs", "ความต้องการ", "need", "ต้องการ"],
            "goals": ["goals", "เป้าหมาย", "goal", "วัตถุประสงค์"],
            "timeline": ["timeline", "เวลา", "กำหนด", "deadline", "ภายใน"],
            "summary_thai": ["summary_thai", "summary", "สรุป"],
        }
        for target_key, aliases in field_map.items():
            for alias in aliases:
                if alias in parsed and parsed[alias]:
                    val = parsed[alias]
                    if isinstance(val, list):
                        data[target_key] = val
                    elif isinstance(val, str) and val.strip():
                        data[target_key] = val
                    break

    return data


def _is_info_complete(data: dict) -> bool:
    """ตรวจสอบว่าข้อมูลครบพอที่จะขอ confirmation หรือยัง"""
    # ต้องมีอย่างน้อย: ชื่อ/บริษัท (หรืออย่างใดอย่างหนึ่ง) + needs + goals
    has_identity = bool(data.get("customer_name") or data.get("company"))
    has_needs = bool(data.get("needs"))
    has_goals = bool(data.get("goals"))
    return has_identity and has_needs and has_goals


def sales_node(state: AgentState) -> dict:
    """
    Sales Agent — Multi-turn sales conversation

    1. ถ้ายังไม่มี conversation → ทักทาย ถามคำถามแรก
    2. มี conversation แล้ว → วิเคราะห์ว่าข้อมูลครบหรือยัง
       - ยังไม่ครบ → ถามคำถามต่อไป (ทีละข้อ)
       - ครบแล้ว → สรุป + ขอ confirmation
    3. ลูกค้าตอบ "yes/ตกลง/ยืนยัน/เริ่มเลย" → บันทึก lead → sales_confirmed = True
    """
    user_input = state.get("input", "").strip()
    conversation = state.get("conversation_context", "")
    system_prompt = get_system_prompt("sales") or _default_sales_prompt()
    output_format = get_output_format("sales") or ""

    # Append current message to conversation
    if conversation:
        full_context = f"{conversation}\nลูกค้า: {user_input}"
    else:
        full_context = f"ลูกค้า: {user_input}"

    # Parse what we've collected so far
    collected = _parse_conversation(full_context)

    # ── Detect confirmation ──
    confirm_keywords = ["ตกลง", "ยืนยัน", "yes", "ok", "เริ่มเลย", "ทำเลย", "ดำเนินการ",
                        "โอเค", "okay", "จัดเลย", "ลุย", "ได้เลย", "เห็นด้วย", "agree",
                        "confirm", "proceed", "go ahead", "เริ่มต้น", "พร้อม"]
    lower_input = user_input.lower()
    is_confirm = any(kw in lower_input for kw in confirm_keywords)

    info_complete = _is_info_complete(collected)

    # If customer confirms AND info is complete → handoff
    if is_confirm and info_complete:
        return _handle_confirmation(state, collected, full_context)

    # ── Call LLM for next response ──
    try:
        format_instruction = ""
        if info_complete and output_format:
            format_instruction = (
                f"\n\n⚠️ ข้อมูลครบแล้ว! สรุปสิ่งที่เข้าใจ และถามลูกค้าว่า "
                f"'ยืนยันให้ดำเนินการต่อหรือไม่?' "
                f"ถ้าลูกค้าตอบตกลง ให้ตอบกลับเป็น JSON:\n{output_format}"
            )

        reply = call_llm(
            f"## บทสนทนาจนถึงตอนนี้\n{full_context}\n\n"
            f"## ข้อมูลที่เก็บได้แล้ว\n{json.dumps(collected, ensure_ascii=False)}\n\n"
            f"## สิ่งที่ต้องถามต่อ (ข้อมูลที่ยังขาด)\n"
            f"{_missing_fields(collected)}\n\n"
            f"## คำสั่ง\n"
            f"คุณคือนักขายมืออาชีพของ Aetox Works คุยกับลูกค้าด้วยน้ำเสียงเป็นกันเอง อบอุ่น "
            f"ถามทีละคำถามเพื่อเก็บข้อมูล อย่ายัดทุกคำถามในรอบเดียว "
            f"ถ้าข้อมูลครบ → สรุปความเข้าใจทั้งหมด และถามลูกค้าว่าต้องการให้ดำเนินการต่อหรือไม่"
            f"{format_instruction}",
            system_prompt=system_prompt,
        )
        log.info("Sales reply: %s", reply[:100])
    except Exception as e:
        log.warning("Sales LLM error: %s", e)
        reply = "ขออภัยครับ ระบบมีปัญหาชั่วคราว กรุณาลองใหม่อีกครั้ง"

    return {
        "results": {},
        "conversation_context": f"{full_context}\nAetox: {reply}",
        "messages": [("system", f"Sales: {reply[:150]}")],
        "sales_confirmed": False,
    }


def _missing_fields(data: dict) -> str:
    """Return list of missing fields as Thai instructions"""
    missing = []
    if not data.get("customer_name") and not data.get("company"):
        missing.append("- ยังไม่รู้ชื่อลูกค้าหรือชื่อบริษัท → ถาม")
    if not data.get("pain_points"):
        missing.append("- ยังไม่รู้ปัญหาที่ลูกค้าเจอ → ถาม")
    if not data.get("needs"):
        missing.append("- ยังไม่รู้ว่าลูกค้าต้องการให้ช่วยอะไร → ถาม")
    if not data.get("goals"):
        missing.append("- ยังไม่รู้เป้าหมายที่ลูกค้าอยากได้ → ถาม")
    if not data.get("timeline"):
        missing.append("- ยังไม่รู้กรอบเวลา → ถาม (แต่ไม่ต้องบังคับ)")
    if not missing:
        return "✅ ข้อมูลครบแล้ว! สรุปและขอคำยืนยัน"
    return "\n".join(missing)


def _handle_confirmation(state: AgentState, collected: dict, context: str) -> dict:
    """Customer confirmed → save lead, set sales_confirmed = True"""
    lead_id = None
    try:
        init_db()
        lead_id = save_lead(
            name=collected.get("customer_name", ""),
            company=collected.get("company", ""),
            pain_points=collected.get("pain_points", []),
            needs=collected.get("needs", []),
            goals=collected.get("goals", []),
            timeline=collected.get("timeline", ""),
            summary=collected.get("summary_thai", ""),
            source="chat",
        )
        log.info("Sales CONFIRMED → lead #%d saved", lead_id)
    except Exception as e:
        log.warning("Sales CRM error on confirm: %s", e)

    output = json.dumps({
        "agent": "sales",
        "lead_id": lead_id,
        "lead_data": collected,
        "status": "confirmed",
    }, ensure_ascii=False)

    confirm_msg = (
        f"ขอบคุณที่ไว้วางใจครับ! 🎉\n"
        f"ผมได้บันทึกข้อมูลของคุณเรียบร้อยแล้ว (Lead #{lead_id})\n"
        f"กำลังส่งต่องานให้ทีม Research วิเคราะห์ตลาดให้คุณต่อครับ..."
    )

    return {
        "results": {"sales": output},
        "conversation_context": f"{context}\nAetox: {confirm_msg}",
        "messages": [("system", f"Sales CONFIRMED: lead #{lead_id}")],
        "sales_confirmed": True,
    }


def _default_sales_prompt() -> str:
    return (
        "คุณคือ Sales Agent มืออาชีพของ Aetox Works\n"
        "บุคลิก: เป็นกันเอง อบอุ่น ฟังเยอะ ถามทีละคำถาม ไม่ยัดเยียด\n"
        "หน้าที่: เก็บข้อมูลลูกค้าให้ครบ → สรุป → ขอคำยืนยัน → ส่งต่องาน\n"
        "ห้าม: สร้าง content, เขียนเว็บ, วิเคราะห์ตลาด — คุณเป็นแค่นักขาย"
    )
