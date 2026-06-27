"""
Aetox Works — Dev Agent 💻
Pipeline step 4: รับ content → สร้างเว็บ, landing page, automation → ส่ง Data

Tools:
  - builder — generate_landing(), generate_html(), write_file(), serve_preview(), list_projects()
  - reporter — save_metric
"""
import logging
import json as json_mod
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm, is_llm_failure
from src.tools.builder import (
    generate_landing,
    generate_html,
    write_file,
    write_project_file,
    serve_preview,
    list_projects,
)
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.dev")

DEV_JSON_SCHEMA = {
    "project_type": "landing",
    "title": "",
    "headline": "",
    "subheadline": "",
    "features": [],
    "cta_text": "เริ่มต้นเลย",
    "files_created": [],
    "tech_stack": ["HTML", "CSS"],
    "summary_thai": "",
}


def _extract_dev_json(text: str) -> dict:
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


def dev_node(state: AgentState) -> dict:
    """
    Dev Agent node สำหรับ LangGraph

    Pipeline step 4: รับ content จาก Content Agent → สร้างหน้าเว็บ → preview

    Flow:
      1. Parse content from previous step
      2. LLM plans page structure + generates content
      3. Build HTML using builder tools
      4. Log metrics
    """
    user_input = state.get("input", "")
    system_prompt = get_system_prompt("dev") or "คุณคือ Dev Agent"
    output_format = get_output_format("dev") or ""

    # Parse content from Content Agent
    content_context = ""
    content_raw = state.get("results", {}).get("content", "")
    if content_raw:
        try:
            content_json = json_mod.loads(content_raw)
            content_context = json_mod.dumps(content_json, ensure_ascii=False)
        except (json_mod.JSONDecodeError, AttributeError):
            content_context = content_raw[:1000]

    # ── LLM Plan + Generate ──
    llm_error = ""
    try:
        format_instruction = (
            f"\n\n⚠️ ตอบกลับเป็น JSON format นี้เท่านั้น:\n{output_format}"
            if output_format else ""
        )
        llm_response = call_llm(
            f"## ความต้องการ\n{user_input}\n\n"
            f"## Content จาก Content Agent\n{content_context}\n\n"
            f"วางแผนและสร้าง: title, headline, subheadline, "
            f"features (list of {{title, desc}}), cta_text, project_type "
            f"{'landing' if 'landing' in user_input.lower() else 'website'}"
            f"{format_instruction}",
            system_prompt=system_prompt,
        )
        if is_llm_failure(llm_response):
            llm_error = llm_response
            log.warning("Dev LLM failure response: %s", llm_response)
            llm_response = json_mod.dumps({
                "project_type": "landing",
                "title": "Aetox Page",
                "headline": user_input[:80],
                "subheadline": "สร้างโดย Dev Agent",
                "features": [{"title": "อัตโนมัติ", "desc": "ระบบ AI"}],
            }, ensure_ascii=False)
        log.info("Dev LLM reply: %s", llm_response[:120])
    except Exception as e:
        log.warning("Dev LLM error: %s", e)
        llm_error = str(e)
        llm_response = json_mod.dumps({
            "project_type": "landing",
            "title": "Aetox Page",
            "headline": user_input[:80],
            "subheadline": "สร้างโดย Dev Agent",
            "features": [{"title": "อัตโนมัติ", "desc": "ระบบ AI"}],
        }, ensure_ascii=False)

    # Parse structured JSON
    parsed = _extract_dev_json(llm_response)
    if not parsed:
        parsed = {
            "project_type": "landing",
            "title": "Aetox Page",
            "headline": user_input[:80],
            "subheadline": "",
            "features": [],
            "cta_text": "เริ่มต้นเลย",
        }

    project_type = parsed.get("project_type", "landing") or "landing"
    title = parsed.get("title", user_input[:80])
    headline = parsed.get("headline", user_input[:80])
    subheadline = parsed.get("subheadline", "")
    features = parsed.get("features", [])
    cta_text = parsed.get("cta_text", "เริ่มต้นเลย")
    tech_stack = parsed.get("tech_stack", ["HTML", "CSS"])

    # ── Build ──
    files_built = []
    build_error = ""
    try:
        if project_type in ("landing", "website"):
            result = generate_landing(
                title=title,
                headline=headline,
                subheadline=subheadline,
                features=features,
                cta_text=cta_text,
                output_subdir="aetox-latest",
                template="modern",
            )
            files_built.append({"path": result["path"], "type": project_type})
            log.info("Dev built landing: %s", result["path"])

        elif project_type == "api":
            # Generate a simple FastAPI skeleton
            api_code = f'''"""API: {title}"""
from fastapi import FastAPI
app = FastAPI(title="{title}")

@app.get("/")
def root():
    return {{"message": "{headline}"}}
'''
            result = write_project_file(
                f"{title.lower().replace(' ', '_')}_api.py",
                api_code,
                output_subdir="aetox-latest",
            )
            files_built.append({"path": result["path"], "type": "api"})

        else:
            # generic: generate HTML
            result = generate_html(
                filename=f"{title.lower().replace(' ', '-')[:30]}.html",
                html_content=f"<h1>{headline}</h1><p>{subheadline}</p>",
                output_subdir="aetox-latest",
            )
            files_built.append({"path": result["path"], "type": project_type})
    except Exception as e:
        log.warning("Dev build error: %s", e)
        build_error = str(e)

    # ── Log metrics ──
    try:
        save_metric("dev", "pages_built", len(files_built))
        save_metric("dev", "project_type_requests", 1, metadata={"project_type": project_type})
    except Exception as e:
        log.warning("Dev metric save error: %s", e)

    status = "complete"
    if llm_error:
        status = "partial"
    if build_error or not files_built:
        status = "error"

    merged = dict(state.get("results", {}))
    merged["dev"] = json_mod.dumps({
        "agent": "dev",
        "project_type": project_type,
        "title": title,
        "files_built": files_built,
        "tech_stack": tech_stack,
        "llm_error": llm_error,
        "build_error": build_error,
        "status": status,
    }, ensure_ascii=False)

    return {
        "results": merged,
        "messages": [("system", f"Dev: built {project_type} '{title}' ({len(files_built)} files)")],
    }
