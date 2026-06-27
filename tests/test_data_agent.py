"""Tests for Data Agent — Phase 6"""
import json
from unittest.mock import patch

# ── Pipeline Stats ────────────────────────────────────────


def test_collect_pipeline_stats_full():
    """ทุก agent มีผลลัพธ์ → stats ครบ"""
    from src.agents.data_agent import _collect_pipeline_stats
    results = {
        "sales": json.dumps({"lead_id": 42}),
        "research": json.dumps({"sources": 5}),
        "content": json.dumps({"draft_id": 7}),
        "dev": json.dumps({"files_built": [{"path": "x.html"}]}),
    }
    stats = _collect_pipeline_stats(results)
    assert stats["sales_done"]
    assert stats["research_done"]
    assert stats["content_done"]
    assert stats["dev_done"]
    assert stats["lead_id"] == 42
    assert stats["search_sources"] == 5
    assert stats["draft_id"] == 7
    assert stats["files_built"] == 1


def test_collect_pipeline_stats_empty():
    """ไม่มีผลลัพธ์ → stats เป็น default"""
    from src.agents.data_agent import _collect_pipeline_stats
    stats = _collect_pipeline_stats({})
    assert not stats["sales_done"]
    assert stats["files_built"] == 0


# ── JSON Extraction ──────────────────────────────────────


def test_extract_data_json():
    from src.agents.data_agent import _extract_data_json
    text = '''```json
{"overall_status": "success", "insights": ["ดี"], "summary_thai": "สรุป"}
```'''
    result = _extract_data_json(text)
    assert result["overall_status"] == "success"
    assert len(result["insights"]) == 1


# ── Data Node ────────────────────────────────────────────


@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_data_node_full_pipeline(
    mock_metrics, mock_projects, mock_drafts, mock_leads, mock_llm,
    tmp_path, monkeypatch
):
    """Data agent รวบรวมทุกผลลัพธ์จาก pipeline → สรุป"""
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_leads.return_value = [{"id": 1}, {"id": 2}]
    mock_drafts.return_value = [{"id": 1}]
    mock_projects.return_value = [{"name": "test"}]
    mock_metrics.return_value = {"pages_built": 3, "leads_collected": 2}
    mock_llm.return_value = json.dumps({
        "overall_status": "success",
        "metrics": {"leads": 2},
        "insights": ["Pipeline ทำงานสมบูรณ์", "ทุกขั้นตอนผ่าน"],
        "recommendations": ["เพิ่ม automation", "ติดตามผลทุกสัปดาห์"],
        "summary_thai": "ระบบทำงานได้ดี พร้อมส่งมอบ",
    }, ensure_ascii=False)

    from src.agents.data_agent import data_node

    state = {
        "input": "สร้าง landing page AI",
        "plan": "", "current_agent": "",
        "messages": [], "results": {
            "sales": json.dumps({"lead_id": 1, "status": "complete"}),
            "research": json.dumps({"sources": 3, "status": "complete"}),
            "content": json.dumps({"draft_id": 1, "status": "complete"}),
            "dev": json.dumps({"files_built": [{"path": "x.html"}], "status": "complete"}),
        }, "final_output": "", "error": None,
    }

    result = data_node(state)
    assert result["final_output"] != ""
    assert "รายงานสรุป" in result["final_output"]
    assert "success" in result["final_output"]

    parsed = json.loads(result["results"]["data"])
    assert parsed["report_id"] is not None
    assert len(parsed["insights"]) >= 1
    assert len(parsed["recommendations"]) >= 1


@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_data_node_empty_pipeline(
    mock_metrics, mock_projects, mock_drafts, mock_leads, mock_llm,
    tmp_path, monkeypatch
):
    """ไม่มีผลลัพธ์จาก agent ก่อนหน้า → ยังทำงานได้"""
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_projects.return_value = []
    mock_metrics.return_value = {}
    mock_llm.return_value = json.dumps({
        "overall_status": "partial",
        "insights": ["ยังไม่มีข้อมูล"],
        "summary_thai": "รอข้อมูลเพิ่ม",
    }, ensure_ascii=False)

    from src.agents.data_agent import data_node

    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = data_node(state)
    assert result["final_output"] != ""
    parsed = json.loads(result["results"]["data"])
    assert parsed["overall_status"] == "partial"


@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_data_node_llm_error(
    mock_metrics, mock_projects, mock_drafts, mock_leads, mock_llm,
    tmp_path, monkeypatch
):
    """LLM error → fallback"""
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_projects.return_value = []
    mock_metrics.return_value = {}
    mock_llm.side_effect = Exception("LLM down")

    from src.agents.data_agent import data_node

    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = data_node(state)
    assert "รายงานสรุป" in result["final_output"]
    parsed = json.loads(result["results"]["data"])
    assert parsed["status"] == "complete"
