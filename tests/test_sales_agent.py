"""Tests for Sales Agent v2 — Multi-turn Conversation"""
import json
from unittest.mock import patch


# ── Conversation Parsing ─────────────────────────────────


def test_parse_empty_conversation():
    from src.agents.sales_agent import _parse_conversation
    result = _parse_conversation("")
    assert result["customer_name"] == ""
    assert result["needs"] == []


def test_parse_conversation_with_json():
    from src.agents.sales_agent import _parse_conversation
    ctx = 'ลูกค้า: ช่วยทำเว็บ\nAetox: {"customer_name":"ไมค์","needs":["ทำเว็บ"]}'
    result = _parse_conversation(ctx)
    assert result["customer_name"] == "ไมค์"
    assert result["needs"] == ["ทำเว็บ"]


def test_parse_conversation_thai_fields():
    from src.agents.sales_agent import _parse_conversation
    ctx = '{"ชื่อ": "สมชาย", "บริษัท": "ThaiTech", "ต้องการ": ["SEO"]}'
    result = _parse_conversation(ctx)
    assert result["customer_name"] == "สมชาย"
    assert result["company"] == "ThaiTech"
    assert result["needs"] == ["SEO"]


# ── Info Complete Check ──────────────────────────────────


def test_info_incomplete():
    from src.agents.sales_agent import _is_info_complete
    assert not _is_info_complete({"customer_name": "", "needs": [], "goals": []})


def test_info_missing_goals():
    from src.agents.sales_agent import _is_info_complete
    assert not _is_info_complete({"customer_name": "A", "needs": ["web"], "goals": []})


def test_info_complete():
    from src.agents.sales_agent import _is_info_complete
    assert _is_info_complete({
        "customer_name": "ไมค์", "company": "Aetox",
        "needs": ["ทำเว็บ"], "goals": ["เพิ่มยอดขาย"]
    })


def test_info_complete_company_only():
    from src.agents.sales_agent import _is_info_complete
    assert _is_info_complete({
        "customer_name": "", "company": "Aetox",
        "needs": ["AI"], "goals": ["growth"]
    })


# ── Sales Node: First Message ────────────────────────────


@patch("src.agents.sales_agent.call_llm")
def test_sales_first_message(mock_llm):
    """First message → Sales greets and asks first question"""
    mock_llm.return_value = "สวัสดีครับ! ยินดีที่ได้รู้จัก คุณมีปัญหาอะไรที่อยากให้ช่วยครับ?"

    from src.agents.sales_agent import sales_node

    state = new_state("ช่วยทำเว็บหน่อยครับ")

    result = sales_node(state)
    assert result["sales_confirmed"] is False
    assert "สวัสดี" in result.get("conversation_context", "")


# ── Sales Node: Conversation Continues ───────────────────


@patch("src.agents.sales_agent.call_llm")
def test_sales_continues_conversation(mock_llm):
    """Second message → Sales asks next question, stays in conversation"""
    mock_llm.return_value = "เข้าใจแล้วครับ แล้วเป้าหมายที่คุณอยากได้คืออะไรครับ?"

    from src.agents.sales_agent import sales_node

    state = new_state("อยากเพิ่มยอดขาย", ctx="ลูกค้า: ช่วยทำเว็บ\nAetox: สวัสดีครับ คุณมีปัญหาอะไรครับ?\nลูกค้า: เว็บเก่าช้ามาก")

    result = sales_node(state)
    assert result["sales_confirmed"] is False
    assert "conversation_context" in result


# ── Sales Node: Confirmation ─────────────────────────────


@patch("src.agents.sales_agent.call_llm")
def test_sales_confirmation(mock_llm, tmp_path, monkeypatch):
    """Customer confirms → sales_confirmed = True, lead saved"""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    mock_llm.return_value = "ขอบคุณที่ยืนยันครับ!"

    from src.agents.sales_agent import sales_node

    # Include [NB:xxx] marker in context so notebook persists
    ctx = (
        '[NB:test123]\n'
        'ลูกค้า: ช่วยทำเว็บ\n'
        'Aetox: บริษัทชื่ออะไรครับ?\n'
        'ลูกค้า: Aetox\n'
        'Aetox: ต้องการให้ช่วยอะไรครับ?\n'
        'ลูกค้า: ทำ landing page\n'
        'Aetox: เป้าหมายคืออะไรครับ?\n'
        'ลูกค้า: เพิ่มยอดขาย\n'
        'Aetox: {"customer_name":"ไมค์","company":"Aetox","needs":["landing page"],"goals":["เพิ่มยอดขาย"]}\n'
    )

    state = new_state("ตกลง เริ่มเลย", ctx=ctx)

    result = sales_node(state)
    assert result["sales_confirmed"] is True
    assert "sales" in result["results"]

    # Verify lead in CRM
    from src.tools.crm import get_lead
    parsed = json.loads(result["results"]["sales"])
    lead = get_lead(parsed["lead_id"])
    assert lead is not None
    assert lead["company"] == "Aetox"


# ── Sales Node: Info Complete But Not Confirmed ──────────


@patch("src.agents.sales_agent.call_llm")
def test_sales_asks_confirmation_when_complete(mock_llm):
    """Info complete but customer hasn't confirmed → ask for confirmation"""
    mock_llm.return_value = "ข้อมูลครบแล้วนะครับ คุณ Aetox ต้องการ landing page เพื่อเพิ่มยอดขาย ถูกต้องไหมครับ?"

    from src.agents.sales_agent import sales_node

    ctx = (
        'ลูกค้า: บริษัท Aetox ต้องการทำ landing page\n'
        'Aetox: เป้าหมายคืออะไรครับ?\n'
    )

    state = new_state("เพิ่มยอดขาย 50% ภายใน 3 เดือน", ctx=ctx)

    result = sales_node(state)
    # Should NOT auto-confirm even though info is complete
    assert "conversation_context" in result


# ── Helpers ──────────────────────────────────────────────


def new_state(input_text: str, ctx: str = ""):
    return {
        "input": input_text,
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
        "sales_confirmed": False,
        "conversation_context": ctx,
    }
