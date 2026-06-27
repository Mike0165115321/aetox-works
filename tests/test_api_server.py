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


def test_agent_status_endpoint():
    """GET /api/agents/status → runtime graph nodes and edges"""
    resp = client.get("/api/agents/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    graph = data["data"]
    assert len(graph["nodes"]) == 7
    assert len(graph["edges"]) == 11
    assert [n["id"] for n in graph["nodes"]] == [
        "personal_assistant", "sales", "research", "content", "dev", "data", "final"
    ]
    assert any(e["from"] == "personal_assistant" and e["to"] == "sales" for e in graph["edges"])
    assert any(e["from"] == "sales" and e["to"] == "personal_assistant" for e in graph["edges"])


def test_api_logger_config_is_idempotent():
    """Repeated logger setup does not duplicate api.log handlers."""
    import logging
    from pathlib import Path
    from src.api import server

    server._configure_api_logger()
    server._configure_api_logger()

    api_log_handlers = [
        handler for handler in server.log.handlers
        if isinstance(handler, logging.FileHandler)
        and Path(getattr(handler, "baseFilename", "")).name == "api.log"
    ]
    assert len(api_log_handlers) == 1


def test_agent_layout_api_persists_and_sanitizes(tmp_path, monkeypatch):
    """Agent graph layout is saved server-side and sanitizes unknown/out-of-range nodes"""
    layout_path = tmp_path / "agent_graph_layout.json"
    monkeypatch.setattr("src.tools.agent_graph_layout._LAYOUT_PATH", layout_path)

    get_resp = client.get("/api/agents/layout")
    assert get_resp.status_code == 200
    defaults = get_resp.json()["data"]["nodes"]
    assert "personal_assistant" in defaults

    put_resp = client.put("/api/agents/layout", json={
        "nodes": {
            "sales": {"x": 120, "y": -10},
            "personal_assistant": {"x": 44.5, "y": 55.5},
            "ghost": {"x": 10, "y": 10},
        }
    })

    assert put_resp.status_code == 200
    nodes = put_resp.json()["data"]["nodes"]
    assert nodes["sales"] == {"x": 95.0, "y": 5.0}
    assert nodes["personal_assistant"] == {"x": 44.5, "y": 55.5}
    assert "ghost" not in nodes
    assert layout_path.exists()

    reset_resp = client.delete("/api/agents/layout")
    assert reset_resp.status_code == 200
    reset_nodes = reset_resp.json()["data"]["nodes"]
    assert reset_nodes["sales"] == defaults["sales"]
    assert not layout_path.exists()


def test_runtime_tracks_hub_edges_for_real_agent_status():
    """Runtime marks active/done on the assistant-mediated graph"""
    from src.supervisor import runtime

    runtime.reset_run("test-run", "pipeline", "สร้างเว็บ")
    runtime.mark_agent_running("sales")
    active = runtime.snapshot()
    assert active["current_agent"] == "sales"
    sales = next(n for n in active["nodes"] if n["id"] == "sales")
    assistant = next(n for n in active["nodes"] if n["id"] == "personal_assistant")
    assert sales["state"] == "active"
    assert assistant["state"] == "done"
    assert any(
        e["from"] == "personal_assistant" and e["to"] == "sales" and e["state"] == "active"
        for e in active["edges"]
    )

    runtime.mark_agent_done("sales", {
        "sales_confirmed": True,
        "results": {"sales": json.dumps({"lead_id": 10, "status": "confirmed"})},
    })
    done = runtime.snapshot()
    sales_done = next(n for n in done["nodes"] if n["id"] == "sales")
    research = next(n for n in done["nodes"] if n["id"] == "research")
    assert sales_done["state"] == "done"
    assert "Lead #10 confirmed" in sales_done["output_summary"]
    assert research["state"] == "waiting"
    assert any(
        e["from"] == "sales" and e["to"] == "personal_assistant" and e["state"] == "done"
        for e in done["edges"]
    )


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
    last = client.get("/api/last-pipeline").json()["data"]
    assert last["sales_confirmed"] is False
    assert last["conversation_context"] == data["conversation_context"]
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


def test_favicon_does_not_pollute_browser_console():
    """GET /favicon.ico avoids a browser 404 console error"""
    resp = client.get("/favicon.ico")
    assert resp.status_code == 204


def test_chat_ui_shows_closing_reply_on_sales_confirmed():
    """Chat UI displays the final Aetox reply before the result card"""
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "function latestAetoxReply" in html
    assert "if(d.sales_confirmed)" in html
    assert "if(reply)addMsg(reply,'other');" in html
    assert "?." not in html


def test_admin_dashboard_script_is_compatible_with_webview():
    """Admin dashboard JS avoids syntax that breaks the embedded WebView"""
    resp = client.get("/admin")
    assert resp.status_code == 200
    html = resp.text
    assert "Agent Graph" in html
    assert '<section class="agent-panel active" id="panel-graph">' in html
    assert "Personal Assistant" in html
    assert "function buildAgentGraph()" in html
    assert "/api/agents/status" in html
    assert "/api/agents/layout" in html
    assert "agent-graph-node" in html
    assert "renderAgentEdges" in html
    assert "agent-loader" in html
    assert "agentInspector" in html
    assert "startDragAgent" in html
    assert "Reset Layout" in html
    assert "Pipeline</button>" in html
    assert "Router</button>" in html
    assert "Open Workspace" in html
    assert "loadSalesWorkspace" in html
    assert "/api/last-pipeline" in html
    assert "/api/notebooks" in html
    assert "salesNotebookList" in html
    assert "salesNotebookViewer" in html
    assert "salesNavBadge" in html
    assert "notebook-render" in html
    assert "renderSalesNotebookViewer" in html
    assert "deleteSalesNotebook" in html
    assert "deleteAllSalesNotebooks" in html
    assert "loadDevWorkspace" in html
    assert "/api/projects" in html
    assert "/files/" in html
    assert "deleteDevFile" in html
    assert "devPreview" in html
    assert "dev-preview-area" in html
    assert "devPreviewMeta" in html
    assert "dev-preview-shell" in html
    assert "devBuildLogs" in html
    assert "Real customer conversation" in html
    assert "บริษัท ไทยนวัตกรรม" not in html
    assert "New notebook created" not in html
    assert "sendSalesMsg" not in html
    assert "Math.random" not in html
    assert "Build Failed" not in html
    assert "CSS bundle error" not in html
    assert "--brand-secondary" not in html
    assert "Undefined variable" not in html
    assert "thai-innovation-lp" not in html
    assert "setTimeout(simulatePipeline" not in html
    assert "?." not in html


def test_project_detail_endpoint_returns_preview_files(tmp_path, monkeypatch):
    """GET /api/projects/{name} returns generated project files for admin preview"""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path)
    project_dir = tmp_path / "demo"
    project_dir.mkdir()
    (project_dir / "index.html").write_text("<h1>Demo</h1>", encoding="utf-8")
    (project_dir / "style.css").write_text("body{color:#111}", encoding="utf-8")

    resp = client.get("/api/projects/demo")

    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["name"] == "demo"
    assert {f["name"] for f in data["data"]["files"]} == {"index.html", "style.css"}
    html_file = next(f for f in data["data"]["files"] if f["name"] == "index.html")
    assert html_file["is_html"] is True
    assert "<h1>Demo</h1>" in html_file["content"]


def test_project_file_delete_endpoint_removes_generated_file(tmp_path, monkeypatch):
    """DELETE /api/projects/{name}/files/{file} removes one generated file safely."""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path)
    project_dir = tmp_path / "demo"
    project_dir.mkdir()
    html_path = project_dir / "index.html"
    css_path = project_dir / "style.css"
    html_path.write_text("<h1>Demo</h1>", encoding="utf-8")
    css_path.write_text("body{color:#111}", encoding="utf-8")

    resp = client.delete("/api/projects/demo/files/style.css")

    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert not css_path.exists()
    assert html_path.exists()

    traversal = client.delete("/api/projects/demo/files/..%5Cindex.html")
    assert traversal.status_code == 200
    assert traversal.json()["success"] is False
    assert html_path.exists()


def test_delete_all_notebooks_endpoint(tmp_path, monkeypatch):
    """DELETE /api/notebooks removes every notebook file"""
    monkeypatch.setattr("src.tools.notebook._NOTEBOOK_DIR", tmp_path)
    from src.tools.notebook import create_notebook, list_notebooks

    create_notebook("bulk1")
    create_notebook("bulk2")
    assert len(list_notebooks()) == 2

    resp = client.delete("/api/notebooks")

    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["deleted"] == 2
    assert list_notebooks() == []


def test_openapi_schema():
    """GET /openapi.json → 200 + valid JSON"""
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "Aetox Works API"
    assert "/pipeline/run" in schema["paths"]
    assert "/health" in schema["paths"]
    assert "/status" in schema["paths"]
