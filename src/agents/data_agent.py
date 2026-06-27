"""
Aetox Works — Data Agent 📊
Pipeline step 5: วิเคราะห์ผลลัพธ์ lead/content/performance

Tools:
  - reporter — save_metric, aggregate_metrics, save_report, generate_summary
  - crm — list_leads
  - content_store — list_drafts
  - builder — list_projects
"""
import logging
import json as json_mod

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt
from src.llm.client import call_llm
from src.tools.reporter import (
    init_db as init_metrics_db,
    aggregate_metrics,
    save_report,
    generate_summary,
)
from src.tools.crm import init_db as init_crm, list_leads
from src.tools.content_store import init_db as init_content, list_drafts
from src.tools.builder import list_projects

log = logging.getLogger("aetox.agents.data")


def data_node(state: AgentState) -> dict:
    """
    Data Agent node สำหรับ LangGraph

    - รวบรวมผลลัพธ์จากทุก agent
    - วิเคราะห์ metrics
    - สรุปเป็น report
    - ส่งกลับลูกค้า
    """
    user_input = state.get("input", "")
    results = state.get("results", {})
    prompt = get_system_prompt("data") or "คุณคือ Data Agent"

    # รวบรวมข้อมูลจากทุกแหล่ง
    report_data = {
        "input": user_input,
        "results": results,
    }

    try:
        init_crm()
        init_content()
        init_metrics_db()

        leads = list_leads(limit=5)
        drafts = list_drafts(limit=5)
        projects = list_projects()
        metrics = aggregate_metrics()

        report_data["leads"] = len(leads)
        report_data["drafts"] = len(drafts)
        report_data["projects"] = len(projects)
        report_data["metrics"] = metrics

        log.info(
            "Data collected: %d leads, %d drafts, %d projects",
            len(leads), len(drafts), len(projects),
        )
    except Exception as e:
        log.warning("Data collection error: %s", e)

    # LLM สรุป
    try:
        summary = call_llm(
            f"คำขอลูกค้า: {user_input}\n\n"
            f"ข้อมูลที่รวบรวมได้:\n"
            f"{json_mod.dumps(report_data, ensure_ascii=False, indent=2)[:2000]}\n\n"
            f"สรุปผลการดำเนินงาน จุดที่ทำได้ดี จุดที่ควรปรับปรุง "
            f"และข้อเสนอแนะ (ภาษาไทย)",
            system_prompt=prompt,
        )
    except Exception as e:
        log.warning("Data LLM error: %s", e)
        summary = f"[Data Agent] วิเคราะห์จาก {len(results)} ผลลัพธ์"

    # บันทึก report
    report_id = None
    try:
        report_id = save_report(
            title=f"Report: {user_input[:50]}",
            summary=summary[:1000],
            data=report_data,
        )
    except Exception as e:
        log.warning("Data save report error: %s", e)

    # Merge results
    merged = dict(results)
    merged["data"] = json_mod.dumps({
        "agent": "data",
        "report_id": report_id,
        "summary": summary[:500],
        "metrics": report_data.get("metrics", {}),
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": merged,
        "final_output": (
            "## 📊 รายงานสรุป\n\n"
            f"{summary}\n\n"
            f"---\n"
            f"*Lead: {report_data.get('leads', 0)} ราย | "
            f"Draft: {report_data.get('drafts', 0)} รายการ | "
            f"โปรเจค: {report_data.get('projects', 0)} โปรเจค*"
        ),
        "messages": [("system", f"Data: report #{report_id} created")],
    }
