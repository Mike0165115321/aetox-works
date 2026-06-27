"""
Aetox Works — Research Agent 🔍
Pipeline step 2: หาข้อมูลตลาด, คู่แข่ง, keyword, insight

Tools:
  - searcher.web_search() — Firecrawl
  - searcher.semantic_search() — Exa
  - searcher.scrape_url()
"""
import logging
import json as json_mod

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt
from src.llm.client import call_llm
from src.tools.searcher import web_search, semantic_search
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.research")


def research_node(state: AgentState) -> dict:
    """
    Research Agent node สำหรับ LangGraph

    - รับสรุปจาก Sales Agent
    - ค้นหาข้อมูลตลาด, คู่แข่ง, keyword
    - เรียก LLM สรุป findings
    - ส่ง structured report → Content Agent
    """
    user_input = state.get("input", "")
    sales_result = state.get("results", {}).get("sales", "")
    prompt = get_system_prompt("research") or "คุณคือ Research Agent"

    # ค้นหาข้อมูล
    search_results = []
    try:
        results = web_search(user_input, num_results=5)
        search_results.extend(results)
        log.info("Research: web search → %d results", len(results))
    except Exception as e:
        log.warning("Research web_search error: %s", e)

    # Semantic search เพิ่ม
    semantic_results = []
    try:
        results = semantic_search(user_input, num_results=3)
        semantic_results.extend(results)
        log.info("Research: semantic search → %d results", len(results))
    except Exception as e:
        log.warning("Research semantic_search error: %s", e)

    # LLM สรุป findings
    try:
        search_text = ""
        for r in search_results:
            search_text += f"- {r.get('title', '')}: {r.get('description', '')}\n"
        for r in semantic_results:
            search_text += f"- [Exa] {r.get('title', '')}: {r.get('text', '')[:300]}\n"

        if not search_text:
            search_text = "(ไม่พบผลการค้นหา — ใช้เฉพาะ LLM)"

        reply = call_llm(
            f"ความต้องการลูกค้า: {user_input}\n\n"
            f"ผลลัพธ์จาก Sales: {sales_result}\n\n"
            f"ข้อมูลที่ค้นหาได้:\n{search_text}\n\n"
            f"สรุปข้อมูลตลาด คู่แข่ง และ insight ที่เกี่ยวข้อง "
            f"(ภาษาไทย) พร้อม JSON output",
            system_prompt=prompt,
        )
    except Exception as e:
        log.warning("Research LLM error: %s", e)
        reply = f"[Research Agent] วิเคราะห์ตลาดจาก: {user_input[:100]}..."

    # Log metrics
    try:
        save_metric("research", "searches_done", len(search_results) + len(semantic_results))
    except Exception:
        pass

    output = json_mod.dumps({
        "agent": "research",
        "findings": reply,
        "sources": len(search_results) + len(semantic_results),
        "status": "complete",
    }, ensure_ascii=False)

    # Merge results เพื่อไม่ให้ทับของ agent ก่อนหน้า
    merged = dict(state.get("results", {}))
    merged["research"] = output

    return {
        "results": merged,
        "messages": [("system", f"Research: found {len(search_results)+len(semantic_results)} sources")],
    }
