"""
Aetox Works — Sales Agent 🗣️
Pipeline step 1: เก็บโจทย์ลูกค้า, pain point, สรุป需求

Tools:
  - CRM (SQLite) — save_lead, list_leads
  - Web Chat — run_chat_server()
"""
import logging
import json

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt
from src.llm.client import call_llm
from src.tools.crm import init_db, save_lead, list_leads

log = logging.getLogger("aetox.agents.sales")


def sales_node(state: AgentState) -> dict:
    """
    Sales Agent node สำหรับ LangGraph

    - รับ input จาก supervisor
    - ใช้ LLM + system prompt เพื่อวิเคราะห์ความต้องการ
    - บันทึก lead ลง CRM
    - สรุป structured data ส่ง Research Agent
    """
    user_input = state.get("input", "")
    prompt = get_system_prompt("sales") or "คุณคือ Sales Agent"

    # ตรวจสอบว่ามีข้อมูลจากแชท history หรือไม่
    results = state.get("results", {})

    # เรียก LLM
    try:
        reply = call_llm(
            f"ลูกค้าพูดว่า: {user_input}\n\n"
            f"ประวัติผลลัพธ์ก่อนหน้า: {json.dumps(results, ensure_ascii=False)}\n\n"
            f"ตอบกลับเป็นสรุปความต้องการของลูกค้า "
            f"และถ้าข้อมูลครบให้ JSON output",
            system_prompt=prompt,
        )
    except Exception as e:
        log.warning("Sales LLM error: %s", e)
        reply = f"[Sales Agent] วิเคราะห์: {user_input[:100]}..."

    # บันทึก lead
    lead_id = None
    try:
        init_db()
        lead_id = save_lead(
            summary=reply[:500],
            source="workflow",
        )
        log.info("Sales saved lead #%d", lead_id)
    except Exception as e:
        log.warning("Sales CRM error: %s", e)

    output = json.dumps({
        "agent": "sales",
        "summary": reply,
        "lead_id": lead_id,
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": {"sales": output},
        "messages": [("system", f"Sales: {reply[:200]}...")],
    }
