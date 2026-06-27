"""Tests for Aetox Works Supervisor"""

from unittest.mock import patch
from src.supervisor.workflow import build_supervisor_graph
from src.supervisor import AGENT_REGISTRY

# ---- Graph Structure ----


def test_supervisor_graph_compiles():
    graph = build_supervisor_graph()
    assert graph is not None


def test_supervisor_graph_has_all_agents():
    graph = build_supervisor_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent: {name}"


# ---- Router (mock LLM) ----


@patch("src.supervisor.workflow.call_llm", return_value="dev")
def test_router_returns_dev(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "create landing page", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[dev]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="sales")
def test_router_returns_sales(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "customer question", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[sales]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="data")
def test_router_returns_data(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "analyze this data", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[data]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="dev")
def test_router_invalid_fallback(mock_llm):
    """ถ้า LLM ตอบ nonsense → fallback เป็น dev"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "xyzzy", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert result["final_output"]  # ไม่ error
