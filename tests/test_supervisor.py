"""Tests for Aetox Works Supervisor"""

from unittest.mock import patch
from src.supervisor.workflow import build_supervisor_graph
from src.supervisor import AGENT_REGISTRY


def test_graph_compiles():
    graph = build_supervisor_graph()
    assert graph is not None


def test_graph_has_all_agents():
    graph = build_supervisor_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent: {name}"


@patch("src.supervisor.workflow.call_llm", return_value="sales")
def test_router_sales(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[sales]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="research")
def test_router_research(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[research]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="content")
def test_router_content(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[content]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="dev")
def test_router_dev(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[dev]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="data")
def test_router_data(mock_llm):
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    })
    assert "[data]" in result["final_output"]
