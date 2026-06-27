"""
Aetox Works — Data Agent 📊
Pipeline step 5: รวบรวมผลลัพธ์จากทุก agent → วิเคราะห์ → สรุปรายงาน → ส่งกลับ

Tools:
  - reporter — save_metric, aggregate_metrics, save_report, generate_summary
  - crm — list_leads
  - content_store — list_drafts
  - builder — list_projects
"""
import logging
import json as json_mod
import re

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm
from src.tools.reporter import (
    init_db as init_metrics_db,
    save_metric,
    aggregate_metrics,
    save_report,
    generate_summary,
)
from src.tools.crm import init_db as init_crm, list_leads
from src.tools.content_store import init_db as init_content, list_drafts
from src.tools.builder import list_projects

log = logging.getLogger("aetox.agents.data")

DATA_JSON_SCHEMA = {
    "overall_status": "success",
    "metrics": {},
    "insights": [],
    "recommendations": [],
    "summary_thai": "",
}


def _extract_data_json(text: str) -> dict:
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


def _collect_pipeline_stats(results: dict) -> dict:
    """รวบรวมสถิติจากทุก agent ใน pipeline"""
    stats = {
        "sales_done": "sales" in results,
        "research_done": "research" in results,
        "content_done": "content" in results,
        "dev_done": "dev" in results,
        "lead_id": None,
        "draft_id": None,
        "files_built": 0,
        "search_sources": 0,
    }

    for agent_name in ("sales", "research", "content", "dev"):
        raw = results.get(agent_name, "")
        if not raw:
            continue
        try:
            data = json_mod.loads(raw)
            if agent_name == "sales":
                stats["lead_id"] = data.get("lead_id")
            elif agent_name == "research":
                stats["search_sources"] = data.get("sources", 0)
            elif agent_name == "content":
                stats["draft_id"] = data.get("draft_id")
            elif agent_name == "dev":
                stats["files_built"] = len(data.get("files_built", []))
        except (json_mod.JSONDecodeError, AttributeError):
            pass

    return stats


def data_node(state: AgentState) -> dict:
    """
    Data Agent node สำหรับ LangGraph

    Pipeline step 5: รวบรวมทุกผลลัพธ์ → วิเคราะห์ → สรุป report → final output

    Flow:
      1. Collect stats from all DBs (leads, drafts, projects, metrics)
      2. Parse pipeline results from all agents
      3. LLM analyze + generate recommendations
      4. Save report
      5. Return final_output to user
    """
    user_input = state.get("input", "")
    results = state.get("results", {})
    system_prompt = get_system_prompt("data") or "คุณคือ Data Agent"
    output_format = get_output_format("data") or ""

    # ── Collect pipeline stats ──
    pipeline_stats = _collect_pipeline_stats(results)

    # ── Collect from databases ──
    db_stats = {"leads": 0, "drafts": 0, "projects": 0}
    try:
        init_crm(); init_content(); init_metrics_db()
        db_stats["leads"] = len(list_leads(limit=100))
        db_stats["drafts"] = len(list_drafts(limit=100))
        db_stats["projects"] = len(list_projects())
        log.info("Data: %d leads, %d drafts, %d projects",
                 db_stats["leads"], db_stats["drafts"], db_stats["projects"])
    except Exception as e:
        log.warning("Data collection error: %s", e)

    # ── Aggregate metrics ──
    aggregated_metrics = {}
    try:
        aggregated_metrics = aggregate_metrics()
    except Exception as e:
        log.warning("Data aggregate error: %s", e)

    # ── LLM Analyze ──
    report_context = {
        "input": user_input,
        "pipeline": pipeline_stats,
        "database": db_stats,
        "metrics": aggregated_metrics,
        "agents_completed": [k for k in results if k != "data"],
    }

    try:
        format_instruction = (
            f"\n\n⚠️ ตอบกลับเป็น JSON format นี้เท่านั้น:\n{output_format}"
            if output_format else ""
        )
        llm_summary = call_llm(
            f"## คำขอลูกค้า\n{user_input}\n\n"
            f"## สรุป Pipeline\n{json_mod.dumps(report_context, ensure_ascii=False, indent=2)}\n\n"
            f"วิเคราะห์ผลลัพธ์ทั้งหมด จุดเด่น จุดที่ควรปรับปรุง "
            f"และข้อเสนอแนะสำหรับขั้นตอนถัดไป (ภาษาไทย){format_instruction}",
            system_prompt=system_prompt,
        )
        log.info("Data LLM reply: %s", llm_summary[:120])
    except Exception as e:
        log.warning("Data LLM error: %s", e)
        llm_summary = f"[Data Agent] Pipeline complete: {len(results)} agents finished"

    # Parse structured JSON
    parsed = _extract_data_json(llm_summary)
    if parsed:
        analysis = parsed
    else:
        analysis = {**DATA_JSON_SCHEMA, "summary_thai": llm_summary[:500]}

    overall = analysis.get("overall_status", "success")
    insights = analysis.get("insights", [])
    recommendations = analysis.get("recommendations", [])
    summary_text = analysis.get("summary_thai", llm_summary[:500])

    # ── Save report ──
    report_id = None
    try:
        report_id = save_report(
            title=f"Report: {user_input[:60]}",
            summary=summary_text[:1000],
            data=report_context,
            report_type="pipeline",
        )
        save_metric("data", "reports_generated", 1)
    except Exception as e:
        log.warning("Data save report error: %s", e)

    # ── Build final output ──
    insights_md = "\n".join(f"- {i}" for i in insights[:5]) if insights else "- OK"
    recommendations_md = "\n".join(f"- {r}" for r in recommendations[:5]) if recommendations else "- พร้อมใช้งาน"

    final_output = (
        f"## 📊 Aetox Works — รายงานสรุป\n\n"
        f"### ผลลัพธ์\n"
        f"- สถานะ: **{overall}**\n"
        f"- Leads: {db_stats['leads']} | Drafts: {db_stats['drafts']} | Projects: {db_stats['projects']}\n"
        f"- Pipeline: {' → '.join(pipeline_stats.keys())}\n\n"
        f"### 🔍 Insights\n{insights_md}\n\n"
        f"### 💡 ข้อเสนอแนะ\n{recommendations_md}\n\n"
        f"### 📝 สรุป\n{summary_text}\n\n"
        f"---\n*Report ID: {report_id or 'N/A'}*"
    )

    merged = dict(results)
    merged["data"] = json_mod.dumps({
        "agent": "data",
        "report_id": report_id,
        "overall_status": overall,
        "summary": summary_text[:500],
        "insights": insights,
        "recommendations": recommendations,
        "metrics": aggregated_metrics,
        "status": "complete",
    }, ensure_ascii=False)

    return {
        "results": merged,
        "final_output": final_output,
        "messages": [("system", f"Data: report #{report_id} — {overall}")],
    }
