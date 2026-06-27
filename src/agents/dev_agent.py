"""
Aetox Works — Dev Agent 💻
Pipeline step 4: สร้างเว็บ, feature, automation

Tools:
  - builder — generate_landing(), generate_html(), write_file(), serve_preview()
"""
import logging
import json as json_mod

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt
from src.llm.client import call_llm
from src.tools.builder import generate_landing, write_file, list_projects
from src.tools.reporter import save_metric

log = logging.getLogger("aetox.agents.dev")


def dev_node(state: AgentState) -> dict:
    """
    Dev Agent node สำหรับ LangGraph

    - รับ content จาก Content Agent
    - วิเคราะห์ว่าต้องทำอะไร (landing, script, API)
    - สร้างไฟล์ด้วย builder tools
    - สรุปผลส่ง Data Agent
    """
    user_input = state.get("input", "")
    content_result = state.get("results", {}).get("content", "")
    prompt = get_system_prompt("dev") or "คุณคือ Dev Agent"

    # ใช้ LLM วางแผน + สร้างเนื้อหา
    try:
        plan = call_llm(
            f"ความต้องการ: {user_input}\n\n"
            f"Content ที่มี: {content_result}\n\n"
            f"วางแผนว่าต้องสร้างอะไร (landing page, script, API) "
            f"และให้เนื้อหาที่จะใส่ในหน้าเว็บ\n"
            f"ตอบเป็นภาษาไทย พร้อม JSON: {{\"type\": \"...\", "
            f"\"title\": \"...\", \"headline\": \"...\", "
            f"\"subheadline\": \"...\", \"features\": [...]}}",
            system_prompt=prompt,
        )
    except Exception as e:
        log.warning("Dev LLM error: %s", e)
        plan = '{"type":"landing","title":"Aetox Page","headline":' + \
               f'"{user_input[:50]}","subheadline":"...","features":[]}}'

    # ลอง parse JSON จาก LLM response
    page_info = {"title": "Aetox Page", "headline": user_input[:80]}
    try:
        # หา JSON block
        text = plan
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        parsed = json_mod.loads(text)
        page_info.update(parsed)
    except (json_mod.JSONDecodeError, IndexError):
        pass

    # สร้างหน้าเว็บ
    build_result = {}
    try:
        build_result = generate_landing(
            title=page_info.get("title", "Aetox Page"),
            headline=page_info.get("headline", user_input[:80]),
            subheadline=page_info.get("subheadline", ""),
            features=page_info.get("features", []),
            output_subdir="aetox-latest",
        )
        log.info("Dev built: %s", build_result.get("path", ""))
    except Exception as e:
        log.warning("Dev build error: %s", e)
        build_result = {"path": "(error)", "url": ""}

    # Log metrics
    try:
        save_metric("dev", "pages_built", 1)
    except Exception:
        pass

    # Merge results
    merged = dict(state.get("results", {}))
    merged["dev"] = json_mod.dumps({
        "agent": "dev",
        "type": page_info.get("type", "landing"),
        "file_path": build_result.get("path", ""),
        "url": build_result.get("url", ""),
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": merged,
        "messages": [("system", f"Dev: built {build_result.get('path', 'N/A')}")],
    }
