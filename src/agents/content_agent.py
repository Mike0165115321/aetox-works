"""
Aetox Works — Content Agent ✍️
Pipeline step 3: เขียน copy, landing content, article

Tools:
  - content_store — save_draft, list_drafts
  - call_llm() — DeepSeek สำหรับสร้าง content
"""
import logging
import json as json_mod

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt
from src.llm.client import call_llm
from src.tools.content_store import init_db, save_draft, list_drafts
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.content")


def content_node(state: AgentState) -> dict:
    """
    Content Agent node สำหรับ LangGraph

    - รับข้อมูลจาก Research Agent
    - ใช้ LLM สร้าง content (landing, blog, social, email)
    - บันทึก draft ลง content_store
    - ส่ง structured content → Dev Agent
    """
    user_input = state.get("input", "")
    research_result = state.get("results", {}).get("research", "")
    prompt = get_system_prompt("content") or "คุณคือ Content Agent"

    try:
        reply = call_llm(
            f"ความต้องการลูกค้า: {user_input}\n\n"
            f"ข้อมูลจาก Research: {research_result}\n\n"
            f"สร้าง content ที่เหมาะสม พร้อมทั้ง:\n"
            f"- หัวข้อ (title)\n"
            f"- เนื้อหา (body)\n"
            f"- CTA\n"
            f"- กลุ่มเป้าหมาย\n\n"
            f"ตอบเป็นภาษาไทย พร้อม JSON output",
            system_prompt=prompt,
        )
    except Exception as e:
        log.warning("Content LLM error: %s", e)
        reply = f"[Content Agent] ร่าง content จาก: {user_input[:100]}..."

    # บันทึก draft
    draft_id = None
    try:
        init_db()
        draft_id = save_draft(
            title=f"Content จาก: {user_input[:50]}",
            body=reply[:2000],
        )
        log.info("Content saved draft #%d", draft_id)
    except Exception as e:
        log.warning("Content save error: %s", e)

    # Log metrics
    try:
        save_metric("content", "drafts_created", 1)
    except Exception:
        pass

    # Merge results
    merged = dict(state.get("results", {}))
    merged["content"] = json_mod.dumps({
        "agent": "content",
        "draft": reply[:500],
        "draft_id": draft_id,
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": merged,
        "messages": [("system", f"Content: created draft #{draft_id}")],
    }
