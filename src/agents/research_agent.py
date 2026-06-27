"""
Aetox Works — Research Agent 🔍
Pipeline step 2: รับ leads จาก Sales → หาข้อมูลตลาด, คู่แข่ง, keyword, insight → ส่ง Content

Tools:
  - searcher.web_search() — Firecrawl
  - searcher.semantic_search() — Exa
  - searcher.scrape_url()
"""
import logging
import json as json_mod
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm, is_llm_failure
from src.tools.searcher import web_search, semantic_search, scrape_url
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.research")

# Default structure สำหรับ research output
RESEARCH_JSON_SCHEMA = {
    "market_overview": "",
    "competitors": [],
    "keywords": [],
    "insights": [],
    "references": [],
    "summary_thai": "",
}


def _result_source_mode(results: list[dict], demo_label: str) -> str:
    if not results:
        return "none"
    marker = f"[{demo_label.upper()} DEMO]"
    return "demo" if any(marker in str(item.get("title", "")) for item in results) else "real"


def _extract_research_json(text: str) -> dict:
    """Extract JSON จาก LLM response (รองรับ code block + inline)"""
    patterns = [
        r"```(?:json)?\s*(\{.*?\})\s*```",
        r"(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL)
        if m:
            try:
                return json_mod.loads(m.group(1))
            except json_mod.JSONDecodeError:
                continue
    return {}


def _build_search_query(sales_data: dict | None, user_input: str) -> str:
    """สร้าง search query จาก handoff_brief หรือ sales data"""
    if not sales_data:
        return user_input

    parts = []
    # handoff_brief uses project_name, raw sales uses company
    company = sales_data.get("project_name") or sales_data.get("company") or ""
    if company:
        parts.append(company)
    if sales_data.get("needs"):
        parts.extend(sales_data["needs"][:2])
    if sales_data.get("pain_points"):
        parts.extend(sales_data["pain_points"][:1])

    if parts:
        return " ".join(parts)
    return user_input


def research_node(state: AgentState) -> dict:
    """
    Research Agent node สำหรับ LangGraph

    Pipeline step 2: รับ leads/summary จาก Sales → ค้นหา → สรุป structured report → ส่ง Content

    Flow:
      1. Parse sales results → build search query
      2. Web search + Semantic search
      3. Scrape top URLs for detail (ถ้ามี)
      4. LLM synthesize → structured JSON
      5. Log metrics
    """
    user_input = state.get("input", "")
    system_prompt = get_system_prompt("research") or "คุณคือ Research Agent"
    output_format = get_output_format("research") or ""

    # Parse handoff_brief from Sales Agent (preferred)
    sales_data = state.get("handoff_brief") or {}
    if not sales_data:
        # Fallback: parse from raw sales results
        sales_raw = state.get("results", {}).get("sales", "")
        if sales_raw:
            try:
                sales_json = json_mod.loads(sales_raw)
                sales_data = sales_json.get("lead_data", {})
            except (json_mod.JSONDecodeError, AttributeError):
                sales_data = {}

    # Build optimized search query
    query = _build_search_query(sales_data, user_input)
    log.info("Research query: %s", query[:100])

    # ── Web Search ──
    web_results = []
    search_errors = []
    try:
        web_results = web_search(query, num_results=5)
        log.info("Research: web search → %d results", len(web_results))
    except Exception as e:
        log.warning("Research web_search error: %s", e)
        search_errors.append(f"web_search: {e}")

    # ── Semantic Search ──
    exa_results = []
    try:
        exa_results = semantic_search(query, num_results=3)
        log.info("Research: semantic search → %d results", len(exa_results))
    except Exception as e:
        log.warning("Research semantic_search error: %s", e)
        search_errors.append(f"semantic_search: {e}")

    web_source_mode = _result_source_mode(web_results, "firecrawl")
    semantic_source_mode = _result_source_mode(exa_results, "exa")
    source_modes = {web_source_mode, semantic_source_mode} - {"none"}
    if not source_modes:
        source_mode = "none"
    elif source_modes == {"real"}:
        source_mode = "real"
    elif source_modes == {"demo"}:
        source_mode = "demo"
    else:
        source_mode = "mixed"

    # ── Deep scrape top URLs (max 2) ──
    deep_content = ""
    top_urls = [r.get("url", "") for r in web_results[:2] if r.get("url")]
    for url in top_urls:
        try:
            content = scrape_url(url)
            if content and not content.startswith("["):
                deep_content += f"\n--- Content from {url} ---\n{content[:2000]}\n"
        except Exception as e:
            log.warning("Research scrape_url error %s: %s", url, e)

    # ── LLM Synthesize ──
    llm_error = ""
    try:
        search_text = ""
        for r in web_results:
            search_text += f"- [{r.get('title', '')}]({r.get('url', '')}): {r.get('description', '')}\n"
        for r in exa_results:
            search_text += f"- [Exa] {r.get('title', '')}: {r.get('text', '')[:300]}\n"

        if not search_text:
            search_text = "(ไม่พบผลการค้นหา — ใช้เฉพาะ LLM knowledge)"

        sales_context = json_mod.dumps(sales_data, ensure_ascii=False) if sales_data else user_input
        format_instruction = (
            f"\n\n⚠️ ตอบกลับเป็น JSON format นี้เท่านั้น:\n{output_format}"
            if output_format else ""
        )

        reply = call_llm(
            f"## ลูกค้าต้องการ\n{sales_context}\n\n"
            f"## ผลการค้นหา\n{search_text}\n"
            f"{deep_content}\n\n"
            f"## หน้าที่\nสรุปข้อมูลตลาด คู่แข่ง keywords และ insight "
            f"ที่เกี่ยวข้องกับการตัดสินใจของลูกค้าเป็นภาษาไทย{format_instruction}",
            system_prompt=system_prompt,
        )
        if is_llm_failure(reply):
            llm_error = reply
            log.warning("Research LLM failure response: %s", reply)
            reply = f"[Research Agent] วิเคราะห์ตลาดเบื้องต้นจากข้อมูลที่มีสำหรับ: {user_input[:100]}..."
        log.info("Research LLM reply: %s", reply[:120])
    except Exception as e:
        log.warning("Research LLM error: %s", e)
        llm_error = str(e)
        reply = f"[Research Agent] วิเคราะห์ตลาดสำหรับ: {user_input[:100]}..."

    # ── Parse structured JSON ──
    parsed = _extract_research_json(reply)
    if parsed:
        findings = parsed
    else:
        findings = {**RESEARCH_JSON_SCHEMA, "summary_thai": reply[:500]}

    # ── Log metrics ──
    total_sources = len(web_results) + len(exa_results)
    try:
        save_metric("research", "searches_done", total_sources)
        save_metric("research", "deep_scrapes", len(top_urls))
    except Exception as e:
        log.warning("Research metric save error: %s", e)

    status = "complete"
    if llm_error or search_errors or source_mode in {"demo", "none"}:
        status = "partial"

    output = json_mod.dumps({
        "agent": "research",
        "findings": findings,
        "raw_reply": reply[:300],
        "sources": total_sources,
        "source_mode": source_mode,
        "web_source_mode": web_source_mode,
        "semantic_source_mode": semantic_source_mode,
        "deep_scrapes": len(top_urls),
        "warnings": search_errors,
        "llm_error": llm_error,
        "status": status,
    }, ensure_ascii=False)

    merged = dict(state.get("results", {}))
    merged["research"] = output

    return {
        "results": merged,
        "messages": [("system", f"Research: {total_sources} sources → {findings.get('summary_thai', '')[:100]}")],
    }
