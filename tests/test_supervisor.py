"""Tests for Aetox Works Supervisor"""

from src.supervisor.workflow import build_supervisor_graph


def test_supervisor_graph_compiles():
    """ทดสอบว่า graph compile ได้"""
    graph = build_supervisor_graph()
    assert graph is not None


def test_supervisor_invoke():
    """ทดสอบว่า graph รับ input และคืนผลลัพธ์"""
    graph = build_supervisor_graph()
    result = graph.invoke({
        "input": "test",
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
    })
    assert "final_output" in result
