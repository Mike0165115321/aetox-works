"""Tests for Aetox Works Supervisor Graph"""

from unittest.mock import patch
from src.supervisor.workflow import build_supervisor_graph, router_llm
from src.supervisor import AGENT_REGISTRY


def test_graph_compiles():
    """Graph compile ได้"""
    graph = build_supervisor_graph()
    assert graph is not None


def test_graph_has_all_agents():
    """ทุก agent ใน REGISTRY มี node ใน graph"""
    graph = build_supervisor_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent: {name}"


def test_graph_has_correct_node_count():
    """Graph มี node ถูกต้อง: __start__ + supervisor + final + 5 agents"""
    graph = build_supervisor_graph()
    # __start__ + supervisor + final + 5 agents = 8 nodes
    assert len(graph.nodes) == 8


def test_graph_has_supervisor_and_final():
    """Graph มี supervisor + final node"""
    graph = build_supervisor_graph()
    assert "supervisor" in graph.nodes
    assert "final" in graph.nodes


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
