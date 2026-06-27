"""Shared test isolation for file-backed tools."""

import pytest


@pytest.fixture(autouse=True)
def isolate_persistent_tool_storage(tmp_path, monkeypatch):
    """Keep tests from writing CRM/notebook/report/project data into local app state."""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db", raising=False)
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db", raising=False)
    monkeypatch.setattr("src.tools.reporter._DB_PATH", tmp_path / "metrics.db", raising=False)
    monkeypatch.setattr("src.tools.notebook._NOTEBOOK_DIR", tmp_path / "notebooks", raising=False)
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites", raising=False)
    monkeypatch.setattr("src.tools.agent_graph_layout._LAYOUT_PATH", tmp_path / "agent_graph_layout.json", raising=False)
