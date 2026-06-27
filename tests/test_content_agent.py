"""Tests for Content Agent — Phase 4"""
import json
from unittest.mock import patch

# ── Content Type Inference ───────────────────────────────


def test_infer_landing():
    from src.agents.content_agent import _infer_content_type
    assert _infer_content_type("ทำ landing page สวยๆ") == "landing"
    assert _infer_content_type("ต้องการหน้าเว็บ") == "landing"


def test_infer_blog():
    from src.agents.content_agent import _infer_content_type
    assert _infer_content_type("เขียน blog เกี่ยวกับ AI") == "blog"
    assert _infer_content_type("บทความเรื่องการตลาด") == "blog"


def test_infer_social():
    from src.agents.content_agent import _infer_content_type
    assert _infer_content_type("ทำ content facebook") == "social"
    assert _infer_content_type("caption TikTok") == "social"


def test_infer_email():
    from src.agents.content_agent import _infer_content_type
    assert _infer_content_type("เขียน email newsletter") == "email"


def test_infer_default():
    from src.agents.content_agent import _infer_content_type
    assert _infer_content_type("อะไรก็ได้") == "landing"


# ── JSON Extraction ──────────────────────────────────────


def test_extract_content_json():
    from src.agents.content_agent import _extract_content_json
    text = '''```json
{"content_type": "landing", "title": "Hero Section", "body": "Welcome", "cta": "Sign Up", "tone": "professional"}
```'''
    result = _extract_content_json(text)
    assert result["content_type"] == "landing"
    assert result["title"] == "Hero Section"
    assert result["cta"] == "Sign Up"


# ── Content Node ─────────────────────────────────────────


@patch("src.agents.content_agent.call_llm")
def test_content_node_landing(mock_llm, tmp_path, monkeypatch):
    """Generate landing page content → save draft"""
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_llm.return_value = json.dumps({
        "content_type": "landing",
        "title": "AI Solutions สำหรับธุรกิจคุณ",
        "body": "## ทำไมต้อง AI?\n\nAI ช่วยเพิ่มประสิทธิภาพ...",
        "cta": "เริ่มต้นวันนี้ ฟรี!",
        "target_audience": "เจ้าของธุรกิจ SME",
        "tone": "professional",
        "keywords": ["AI", "automation", "business"],
        "summary_thai": "landing page สำหรับ AI solution",
    }, ensure_ascii=False)

    from src.agents.content_agent import content_node

    state = {
        "input": "ทำ landing page สำหรับ AI solution",
        "plan": "", "current_agent": "",
        "messages": [], "results": {
            "research": json.dumps({
                "findings": {"market_overview": "ตลาด AI โต 25%"}
            }, ensure_ascii=False)
        }, "final_output": "", "error": None,
    }

    result = content_node(state)
    assert "content" in result["results"]
    parsed = json.loads(result["results"]["content"])
    assert parsed["content_type"] == "landing"
    assert parsed["draft_id"] > 0
    assert "AI Solutions" in parsed["title"]

    # verify draft saved
    from src.tools.content_store import get_draft
    draft = get_draft(parsed["draft_id"])
    assert draft is not None
    assert draft["content_type"] == "landing"
    assert draft["tone"] == "professional"


@patch("src.agents.content_agent.call_llm")
def test_content_node_blog(mock_llm, tmp_path, monkeypatch):
    """Generate blog article"""
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")

    mock_llm.return_value = json.dumps({
        "content_type": "blog",
        "title": "5 เทรนด์ AI ปี 2026",
        "body": "บทความนี้จะพาไปดู...",
        "cta": "อ่านต่อ",
        "tone": "casual",
    }, ensure_ascii=False)

    from src.agents.content_agent import content_node

    state = {
        "input": "เขียน blog เกี่ยวกับ AI trends",
        "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = content_node(state)
    parsed = json.loads(result["results"]["content"])
    assert parsed["content_type"] == "blog"

    from src.tools.content_store import get_draft
    draft = get_draft(parsed["draft_id"])
    assert draft["content_type"] == "blog"


@patch("src.agents.content_agent.call_llm")
def test_content_node_llm_error(mock_llm, tmp_path, monkeypatch):
    """LLM error → fallback"""
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")
    mock_llm.side_effect = Exception("Timeout")

    from src.agents.content_agent import content_node

    state = {
        "input": "ทำ content", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = content_node(state)
    assert "content" in result["results"]
    parsed = json.loads(result["results"]["content"])
    assert parsed["status"] == "partial"
    assert parsed["llm_error"] == "Timeout"


@patch("src.agents.content_agent.call_llm")
def test_content_node_no_json_fallback(mock_llm, tmp_path, monkeypatch):
    """LLM returns plain text (no JSON) → fallback"""
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")
    mock_llm.return_value = "นี่คือ content ธรรมดา ไม่มี JSON"

    from src.agents.content_agent import content_node

    state = {
        "input": "ทำ content", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = content_node(state)
    parsed = json.loads(result["results"]["content"])
    assert parsed["draft_id"] > 0  # still saved

    from src.tools.content_store import get_draft
    draft = get_draft(parsed["draft_id"])
    assert "content ธรรมดา" in draft["body"]
