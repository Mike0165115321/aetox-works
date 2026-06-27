"""Tests for Aetox Works Supervisor Graph — Pipeline + Router modes"""

from unittest.mock import patch
from src.supervisor.workflow import (
    build_supervisor_graph,
    build_pipeline_graph,
    build_router_graph,
    router_llm,
    pipeline_next_agent,
)
from src.supervisor import AGENT_REGISTRY


# ── Pipeline Graph ────────────────────────────────────────

def test_pipeline_graph_compiles():
    """Pipeline graph compile ได้"""
    graph = build_pipeline_graph()
    assert graph is not None


def test_pipeline_graph_has_all_agents():
    """ทุก agent ใน REGISTRY มี node ใน pipeline graph"""
    graph = build_pipeline_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent: {name}"


def test_pipeline_graph_node_count():
    """Pipeline graph: __start__ + supervisor + final + 5 agents = 8 nodes"""
    graph = build_pipeline_graph()
    assert len(graph.nodes) == 8


# ── Router Graph ──────────────────────────────────────────

def test_router_graph_compiles():
    """Router graph compile ได้"""
    graph = build_router_graph()
    assert graph is not None


def test_router_graph_has_all_agents():
    """ทุก agent มี node ใน router graph"""
    graph = build_router_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent: {name}"


def test_router_graph_node_count():
    """Router graph: __start__ + supervisor + final + 5 agents = 8 nodes"""
    graph = build_router_graph()
    assert len(graph.nodes) == 8


# ── Build Supervisor (with mode) ──────────────────────────

def test_build_default_is_pipeline():
    """Default mode = pipeline"""
    graph = build_supervisor_graph()  # no mode arg
    assert graph is not None


def test_build_pipeline_explicit():
    """Explicit pipeline mode"""
    graph = build_supervisor_graph(mode="pipeline")
    assert graph is not None


def test_build_router_mode():
    """Router mode"""
    graph = build_supervisor_graph(mode="router")
    assert graph is not None


# ── Pipeline Router ───────────────────────────────────────

def test_pipeline_next_starts_at_sales():
    """No results → start at sales"""
    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }
    assert pipeline_next_agent(state) == "sales"


def test_pipeline_sales_to_research():
    """Sales done → next is research"""
    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {"sales": "done"},
        "final_output": "", "error": None,
    }
    assert pipeline_next_agent(state) == "research"


def test_pipeline_data_to_final():
    """Data done → final (complete)"""
    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {
            "sales": "done", "research": "done", "content": "done",
            "dev": "done", "data": "done",
        }, "final_output": "", "error": None,
    }
    assert pipeline_next_agent(state) == "final"


def test_pipeline_partial_next():
    """Research เสร็จแล้ว แต่ content ยัง → next = content"""
    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {"sales": "done", "research": "done"},
        "final_output": "", "error": None,
    }
    assert pipeline_next_agent(state) == "content"


# ── LLM Router (router mode) ──────────────────────────────

@patch("src.supervisor.workflow.call_llm", return_value="sales")
def test_router_returns_valid_agent(mock_llm):
    """router_llm ส่งคืนชื่อ agent ที่มีอยู่จริง"""
    state = {
        "input": "test query", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }
    result = router_llm(state)
    assert result == "sales", f"Router returned '{result}' instead of 'sales'"


@patch("src.supervisor.workflow.call_llm", side_effect=Exception("API error"))
def test_router_fallback_on_error(mock_llm):
    """router_llm fallback เป็น 'dev' เมื่อ LLM error"""
    state = {
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }
    result = router_llm(state)
    assert result == "dev", f"Expected fallback 'dev', got '{result}'"


# ── Integration: Pipeline mode invoke ────────────────────

@patch("src.agents.sales_agent.call_llm")
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
def test_pipeline_full_run(
    mock_agg, mock_proj, mock_drafts, mock_leads,
    mock_data_llm, mock_dev_llm, mock_content_llm,
    mock_research_llm, mock_exa, mock_firecrawl, mock_sales_llm,
    tmp_path, monkeypatch
):
    """Pipeline mode: รันทั้ง 5 agents ต่อกัน → ได้ final_output"""
    import json
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db")
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")

    # Mock all LLM calls
    mock_sales_llm.return_value = json.dumps({
        "customer_name": "ไมค์", "company": "Aetox",
        "summary_thai": "ต้องการ AI workforce",
    }, ensure_ascii=False)
    mock_firecrawl.return_value = []
    mock_exa.return_value = []
    mock_research_llm.return_value = json.dumps({
        "summary_thai": "ตลาด AI กำลังโต",
        "keywords": ["AI"],
    }, ensure_ascii=False)
    mock_content_llm.return_value = json.dumps({
        "title": "AI Solutions", "body": "เนื้อหา",
        "content_type": "landing",
    }, ensure_ascii=False)
    mock_dev_llm.return_value = json.dumps({
        "project_type": "landing", "title": "Aetox",
        "headline": "AI", "features": [],
    }, ensure_ascii=False)
    mock_leads.return_value = []
    mock_drafts.return_value = []
    mock_proj.return_value = []
    mock_agg.return_value = {}
    mock_data_llm.return_value = json.dumps({
        "overall_status": "success",
        "summary_thai": "Pipeline complete!",
    }, ensure_ascii=False)

    graph = build_pipeline_graph()

    result = graph.invoke({
        "input": "สร้าง AI solution สำหรับธุรกิจ",
        "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })

    assert result["final_output"] != ""
    assert "sales" in result["results"]
    assert "research" in result["results"]
    assert "content" in result["results"]
    assert "dev" in result["results"]
    assert "data" in result["results"]

