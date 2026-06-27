"""Tests for Aetox Works Supervisor"""

from unittest.mock import patch
from src.supervisor.workflow import build_supervisor_graph
from src.supervisor import AGENT_REGISTRY

# ---- Graph Structure ----


def test_supervisor_graph_compiles():
    """ทดสอบว่า graph compile ได้"""
    graph = build_supervisor_graph()
    assert graph is not None


def test_supervisor_graph_has_all_agents():
    """ทดสอบว่า graph มี node ครบทุก agent"""
    graph = build_supervisor_graph()
    for name in AGENT_REGISTRY:
        assert name in graph.nodes, f"Missing agent node: {name}"


# ---- Router (mock LLM) ----


@patch("src.supervisor.workflow.call_llm", return_value="dev")
def test_router_returns_dev(mock_llm):
    """ทดสอบ router ส่งงาน dev agent"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "สร้าง landing page",
        "plan": "", "current_agent": "", "messages": [],
        "results": {}, "final_output": "", "error": None,
    })
    assert "[dev]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="sales")
def test_router_returns_sales(mock_llm):
    """ทดสอบ router ส่งงาน sales agent"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "ติดต่อลูกค้า",
        "plan": "", "current_agent": "", "messages": [],
        "results": {}, "final_output": "", "error": None,
    })
    assert "[sales]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="video")
def test_router_returns_video(mock_llm):
    """ทดสอบ router ส่งงาน video agent"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "ตัดต่อวิดีโอ",
        "plan": "", "current_agent": "", "messages": [],
        "results": {}, "final_output": "", "error": None,
    })
    assert "[video]" in result["final_output"]


@patch("src.supervisor.workflow.call_llm", return_value="admin")
def test_router_returns_admin(mock_llm):
    """ทดสอบ router ส่งงาน admin agent"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "สรุปงาน",
        "plan": "", "current_agent": "", "messages": [],
        "results": {}, "final_output": "", "error": None,
    })
    assert "[admin]" in result["final_output"]
