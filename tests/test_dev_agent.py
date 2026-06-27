"""Tests for Dev Agent — Phase 5"""
import json
from unittest.mock import patch


# ── JSON Extraction ──────────────────────────────────────


def test_extract_dev_json():
    from src.agents.dev_agent import _extract_dev_json
    text = '''```json
{"project_type": "landing", "title": "My Page", "headline": "Hello", "features": [{"title": "F1", "desc": "D1"}]}
```'''
    result = _extract_dev_json(text)
    assert result["project_type"] == "landing"
    assert len(result["features"]) == 1


# ── Dev Node ─────────────────────────────────────────────


@patch("src.agents.dev_agent.call_llm")
def test_dev_node_landing(mock_llm, tmp_path, monkeypatch):
    """Dev agent builds a landing page from content"""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")

    mock_llm.return_value = json.dumps({
        "project_type": "landing",
        "title": "Aetox AI Solutions",
        "headline": "ปลดล็อกศักยภาพด้วย AI",
        "subheadline": "โซลูชันครบวงจรสำหรับธุรกิจไทย",
        "features": [
            {"title": "Automation", "desc": "ลดงาน repetitive 90%"},
            {"title": "Analytics", "desc": "เข้าใจลูกค้าเชิงลึก"},
        ],
        "cta_text": "ทดลองฟรี",
        "tech_stack": ["HTML", "CSS", "JS"],
    }, ensure_ascii=False)

    from src.agents.dev_agent import dev_node

    state = {
        "input": "สร้าง landing page สำหรับ AI startup",
        "plan": "", "current_agent": "",
        "messages": [], "results": {
            "content": json.dumps({
                "title": "AI Solutions", "body": "เนื้อหา..."
            }, ensure_ascii=False)
        }, "final_output": "", "error": None,
    }

    result = dev_node(state)
    assert "dev" in result["results"]
    parsed = json.loads(result["results"]["dev"])
    assert parsed["project_type"] == "landing"
    assert len(parsed["files_built"]) >= 1
    assert parsed["files_built"][0]["path"].endswith(".html")

    # verify file exists
    import os
    assert os.path.exists(parsed["files_built"][0]["path"])


@patch("src.agents.dev_agent.call_llm")
def test_dev_node_llm_error(mock_llm, tmp_path, monkeypatch):
    """LLM error → fallback landing page"""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")
    mock_llm.side_effect = Exception("LLM down")

    from src.agents.dev_agent import dev_node

    state = {
        "input": "สร้างเว็บ", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = dev_node(state)
    parsed = json.loads(result["results"]["dev"])
    assert parsed["status"] == "complete"
    assert len(parsed["files_built"]) >= 1


@patch("src.agents.dev_agent.call_llm")
def test_dev_node_no_json(mock_llm, tmp_path, monkeypatch):
    """LLM returns plain text → still builds"""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")
    mock_llm.return_value = "สร้าง landing page ธรรมดาๆ"

    from src.agents.dev_agent import dev_node

    state = {
        "input": "ทำเว็บ", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = dev_node(state)
    parsed = json.loads(result["results"]["dev"])
    assert parsed["project_type"] == "landing"  # default


@patch("src.agents.dev_agent.call_llm")
def test_dev_node_api_type(mock_llm, tmp_path, monkeypatch):
    """project_type=api → generates Python file"""
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")

    mock_llm.return_value = json.dumps({
        "project_type": "api",
        "title": "User API",
        "headline": "REST API for users",
        "features": [],
    }, ensure_ascii=False)

    from src.agents.dev_agent import dev_node

    state = {
        "input": "สร้าง API", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = dev_node(state)
    parsed = json.loads(result["results"]["dev"])
    assert parsed["project_type"] == "api"
    assert any("api" in f["path"] for f in parsed["files_built"])
