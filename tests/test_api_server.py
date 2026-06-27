"""Tests for Aetox Works API Server — Phase 7"""
import json
import os
from unittest.mock import patch

from fastapi.testclient import TestClient

os.environ.pop("AETOX_API_KEY", None)  # ensure dev mode (no auth) for tests

from src.api.server import app

client = TestClient(app)


# ── Health + Status ───────────────────────────────────────


def test_health_check():
    """GET /health → 200 + status ok"""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_status_endpoint():
    """GET /status → 200 + counts"""
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "leads_count" in data
    assert "drafts_count" in data
    assert "projects_count" in data
    assert "uptime_seconds" in data


# ── Pipeline Run ──────────────────────────────────────────


@patch("src.supervisor.workflow.sales_node")
@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
@patch("src.agents.content_agent.call_llm")
@patch("src.agents.dev_agent.call_llm")
@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_pipeline_run(
    mock_agg, mock_proj, mock_drafts, mock_leads,
    mock_data_llm, mock_dev_llm, mock_content_llm,
    mock_research_llm, mock_exa, mock_firecrawl, mock_sales_node,
    tmp_path, monkeypatch
):
    """POST /pipeline/run → 200 + agents_used + output"""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")

    # Sales node auto-confirms (bypass multi-turn conversation gate)
    mock_sales_node.return_value = {
        "results": {"sales": json.dumps({"agent": "sales", "lead_id": 1, "status": "confirmed"})},
        "messages": [("system", "Sales confirmed")],
        "sales_confirmed": True,
        "conversation_context": "confirmed",
    }

    mock_firecrawl.return_value = []
    mock_exa.return_value = []
    mock_research_llm.return_value = json.dumps({"summary_thai": "research done"})
    mock_content_llm.return_value = json.dumps({"title": "T", "body": "B", "content_type": "landing"})
    mock_dev_llm.return_value = json.dumps({"project_type": "landing", "title": "T", "headline": "H", "features": []})
    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_proj.return_value = []
    mock_agg.return_value = {}
    mock_data_llm.return_value = json.dumps({"overall_status": "success", "summary_thai": "done!"})

    # Pre-fill sales results to bypass sales confirmation gate
    resp = client.post("/pipeline/run", json={
        "input": "สร้าง landing page AI",
        "mode": "pipeline",
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "sales" in data["agents_used"]
    assert "data" in data["agents_used"]
    assert data["output"] != ""
    assert data["elapsed_ms"] >= 0
    assert data["request_id"]


@patch("src.supervisor.workflow.sales_node")
def test_pipeline_run_with_context_continues_sales(mock_sales_node):
    """POST /pipeline/run with existing context still invokes Sales"""
    mock_sales_node.return_value = {
        "results": {},
        "messages": [("system", "Sales replied")],
        "sales_confirmed": False,
        "conversation_context": "[NB:abc123]\nลูกค้า: ดีครับ\nAetox: ขอทราบชื่อครับ\nลูกค้า: ผมชื่อไมค์ครับ\nAetox: ยินดีครับคุณไมค์ ขอทราบปัญหาหลักครับ?",
        "sales_notebook": {"_nb_id": "abc123"},
        "handoff_brief": {},
    }

    resp = client.post("/pipeline/run", json={
        "input": "ผมชื่อไมค์ครับ",
        "mode": "pipeline",
        "conversation_context": "[NB:abc123]\nลูกค้า: ดีครับ\nAetox: ขอทราบชื่อครับ",
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["sales_confirmed"] is False
    assert "คุณไมค์" in data["conversation_context"]
    mock_sales_node.assert_called_once()


@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_router_mode(
    mock_agg, mock_proj, mock_drafts, mock_leads, mock_data_llm,
    tmp_path, monkeypatch
):
    """POST /pipeline/run with mode=router → 200 + single agent"""
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_proj.return_value = []
    mock_agg.return_value = {}
    mock_data_llm.return_value = json.dumps({"overall_status": "success", "summary_thai": "ok"})

    resp = client.post("/pipeline/run", json={
        "input": "แค่วิเคราะห์ข้อมูล",
        "mode": "router",
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["mode"] == "router"


def test_pipeline_empty_input():
    """POST /pipeline/run with empty input → 422"""
    resp = client.post("/pipeline/run", json={"input": ""})
    assert resp.status_code == 422  # validation error


def test_pipeline_invalid_mode():
    """POST /pipeline/run with invalid mode → 422"""
    resp = client.post("/pipeline/run", json={"input": "test", "mode": "invalid"})
    assert resp.status_code == 422


# ── Agent Run ─────────────────────────────────────────────


@patch("src.agents.data_agent.call_llm")
@patch("src.agents.data_agent.list_leads")
@patch("src.agents.data_agent.list_drafts")
@patch("src.agents.data_agent.list_projects")
@patch("src.agents.data_agent.aggregate_metrics")
def test_agent_run_alias(
    mock_agg, mock_proj, mock_drafts, mock_leads, mock_data_llm,
    tmp_path, monkeypatch
):
    """POST /agent/run → same as /pipeline/run?mode=router"""
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_proj.return_value = []
    mock_agg.return_value = {}
    mock_data_llm.return_value = json.dumps({"overall_status": "success", "summary_thai": "done"})

    resp = client.post("/agent/run", json={"input": "help me"})
    assert resp.status_code == 200


# ── Request ID Header ─────────────────────────────────────


def test_request_id_header():
    """ทุก response มี X-Request-ID header"""
    resp = client.get("/health")
    assert "X-Request-ID" in resp.headers
    assert len(resp.headers["X-Request-ID"]) == 8


# ── Docs ──────────────────────────────────────────────────


def test_docs_available():
    """GET /docs → 200 (Swagger UI)"""
    resp = client.get("/docs")
    assert resp.status_code == 200


def test_chat_ui_shows_closing_reply_on_sales_confirmed():
    """Chat UI displays the final Aetox reply before the result card"""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "function latestAetoxReply" in html
    assert "if(d.sales_confirmed)" in html
    assert "if(reply)addMsg(reply,'other');" in html


def test_openapi_schema():
    """GET /openapi.json → 200 + valid JSON"""
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "Aetox Works API"
    assert "/pipeline/run" in schema["paths"]
    assert "/health" in schema["paths"]
    assert "/status" in schema["paths"]
