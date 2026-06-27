"""
Aetox Works — Content Agent ✍️
Pipeline step 3: รับ research → เขียน copy, landing content, article, social → ส่ง Dev

Tools:
  - content_store — save_draft, list_drafts, update_draft
  - call_llm() — DeepSeek สำหรับสร้าง content
  - reporter — save_metric
"""
import logging
import json as json_mod
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm
from src.tools.content_store import init_db, save_draft, list_drafts, update_draft
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.content")

CONTENT_JSON_SCHEMA = {
    "content_type": "landing",
    "title": "",
    "body": "",
    "cta": "",
    "target_audience": "",
    "tone": "professional",
    "keywords": [],
    "summary_thai": "",
}


def _extract_content_json(text: str) -> dict:
    """Extract JSON จาก LLM response"""
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


def _infer_content_type(user_input: str) -> str:
    """เดา content type จาก input ของ user"""
    lower = user_input.lower()
    type_keywords = {
        "landing": ["landing", "หน้าเว็บ", "landing page", "hero", "homepage", "หน้าหลัก"],
        "blog": ["blog", "บทความ", "article", "เขียนบทความ", "โพสต์"],
        "social": ["social", "โซเชียล", "facebook", "line", "tiktok", "โพสต์โซเชียล", "caption"],
        "email": ["email", "อีเมล", "newsletter", "email marketing", "เมล"],
    }
    for ctype, keywords in type_keywords.items():
        if any(kw in lower for kw in keywords):
            return ctype
    return "landing"  # default


def content_node(state: AgentState) -> dict:
    """
    Content Agent node สำหรับ LangGraph

    Pipeline step 3: รับ research findings → สร้าง content → บันทึก draft → ส่ง Dev

    Flow:
      1. Parse research findings
      2. Infer content type
      3. LLM generate content with structured output
      4. Save to content_store
      5. Log metrics
    """
    user_input = state.get("input", "")
    system_prompt = get_system_prompt("content") or "คุณคือ Content Agent"
    output_format = get_output_format("content") or ""

    # Parse research results
    research_findings = ""
    research_raw = state.get("results", {}).get("research", "")
    if research_raw:
        try:
            research_json = json_mod.loads(research_raw)
            findings = research_json.get("findings", {})
            if isinstance(findings, dict):
                research_findings = json_mod.dumps(findings, ensure_ascii=False)
            else:
                research_findings = str(findings)
        except (json_mod.JSONDecodeError, AttributeError):
            research_findings = research_raw[:1000]

    # Infer content type
    content_type = _infer_content_type(user_input)

    # ── Generate Content via LLM ──
    try:
        format_instruction = (
            f"\n\n⚠️ ตอบกลับเป็น JSON format นี้เท่านั้น:\n{output_format}"
            if output_format else ""
        )
        reply = call_llm(
            f"## ความต้องการลูกค้า\n{user_input}\n\n"
            f"## ข้อมูลวิจัย\n{research_findings or '(ไม่มีข้อมูลวิจัย)'}\n\n"
            f"## ประเภท Content\n{content_type}\n\n"
            f"สร้าง content ภาษาไทยสำหรับประเภท '{content_type}' "
            f"โดยใช้ข้อมูลวิจัยประกอบ เขียนให้น่าสนใจและ actionable{format_instruction}",
            system_prompt=system_prompt,
        )
        log.info("Content LLM reply: %s", reply[:120])
    except Exception as e:
        log.warning("Content LLM error: %s", e)
        reply = f"[Content Agent] ร่าง content จาก: {user_input[:100]}..."

    # Parse structured JSON
    parsed = _extract_content_json(reply)
    if not parsed:
        parsed = {**CONTENT_JSON_SCHEMA, "body": reply[:2000], "title": user_input[:80]}

    title = parsed.get("title", user_input[:80])
    body = parsed.get("body", reply[:2000])
    cta = parsed.get("cta", "")
    tone = parsed.get("tone", "professional") or "professional"
    target = parsed.get("target_audience", "")
    actual_type = parsed.get("content_type", content_type) or content_type

    # ── Save to content_store ──
    draft_id = None
    try:
        init_db()
        draft_id = save_draft(
            title=title,
            content_type=actual_type,
            body=body,
            cta=cta,
            tone=tone,
            target=target,
            metadata={"keywords": parsed.get("keywords", []), "source": "pipeline"},
        )
        log.info("Content saved draft #%d: '%s' [%s]", draft_id, title, actual_type)
    except Exception as e:
        log.warning("Content save error: %s", e)

    # ── Log metrics ──
    try:
        save_metric("content", "drafts_created", 1)
    except Exception:
        pass

    merged = dict(state.get("results", {}))
    merged["content"] = json_mod.dumps({
        "agent": "content",
        "draft_id": draft_id,
        "content_type": actual_type,
        "title": title,
        "body_preview": body[:200],
        "cta": cta,
        "tone": tone,
        "target_audience": target,
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": merged,
        "messages": [("system", f"Content: draft #{draft_id} '{title}' [{actual_type}]")],
    }
