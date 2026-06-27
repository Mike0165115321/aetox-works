"""Tests for Sales Agent — Phase 2"""
import json
from unittest.mock import patch

# ── JSON Extraction ──────────────────────────────────────


def test_extract_json_from_code_block():
    """ดึง JSON จาก ```json ... ``` block"""
    from src.agents.sales_agent import _extract_json
    text = '''นี่คือบทวิเคราะห์
```json
{"customer_name": "สมชาย", "company": "ThaiTech"}
```
จบการสนทนา'''
    result = _extract_json(text)
    assert result["customer_name"] == "สมชาย"
    assert result["company"] == "ThaiTech"


def test_extract_json_inline():
    """ดึง JSON ที่ไม่มี code block"""
    from src.agents.sales_agent import _extract_json
    text = 'สรุป: {"needs": ["ทำเว็บ", "SEO"], "timeline": "2 เดือน"}'
    result = _extract_json(text)
    assert result["needs"] == ["ทำเว็บ", "SEO"]
    assert result["timeline"] == "2 เดือน"


def test_extract_json_no_json():
    """ถ้าไม่มี JSON → return empty dict"""
    from src.agents.sales_agent import _extract_json
    result = _extract_json("แค่ข้อความธรรมดา ไม่มี JSON")
    assert result == {}


def test_extract_json_invalid():
    """JSON พัง → return empty dict"""
    from src.agents.sales_agent import _extract_json
    result = _extract_json("{invalid json here}")
    assert result == {}


# ── Schema Merging ───────────────────────────────────────


def test_merge_with_schema_defaults():
    """merge ดาต้าที่ขาด field → เติม default"""
    from src.agents.sales_agent import _merge_with_schema
    raw = {"customer_name": "ไมค์"}
    result = _merge_with_schema(raw)
    assert result["customer_name"] == "ไมค์"
    assert result["company"] == ""
    assert result["pain_points"] == []
    assert result["needs"] == []


def test_merge_with_schema_all_fields():
    """merge ครบทุก field"""
    from src.agents.sales_agent import _merge_with_schema
    raw = {
        "customer_name": "สมศรี",
        "company": "GreenEnergy",
        "pain_points": ["ยอดขายตก", "ไม่มีเว็บ"],
        "needs": ["ทำเว็บขายของ", "SEO"],
        "goals": ["เพิ่มยอดขาย 50%"],
        "timeline": "ภายใน 3 เดือน",
        "summary_thai": "ต้องการทำเว็บ e-commerce",
    }
    result = _merge_with_schema(raw)
    assert result["customer_name"] == "สมศรี"
    assert result["pain_points"] == ["ยอดขายตก", "ไม่มีเว็บ"]
    assert result["timeline"] == "ภายใน 3 เดือน"


def test_merge_handles_non_list_fields():
    """ถ้า pain_points เป็น string → แปลงเป็น list"""
    from src.agents.sales_agent import _merge_with_schema
    raw = {"pain_points": "ยอดขายตก"}
    result = _merge_with_schema(raw)
    assert result["pain_points"] == ["ยอดขายตก"]


# ── Parse Lead from Reply ────────────────────────────────


def test_parse_lead_full_json():
    """parse reply ที่เป็น JSON สมบูรณ์"""
    from src.agents.sales_agent import _parse_lead_from_reply
    reply = json.dumps({
        "customer_name": "ชยพล",
        "company": "Aetox",
        "pain_points": ["ไม่มี automation"],
        "needs": ["ระบบ AI จัดการงาน"],
        "goals": ["ลดต้นทุน 30%"],
        "timeline": "6 เดือน",
        "summary_thai": "Aetox ต้องการ AI workforce",
    }, ensure_ascii=False)
    result = _parse_lead_from_reply(reply)
    assert result["customer_name"] == "ชยพล"
    assert result["company"] == "Aetox"
    assert result["pain_points"] == ["ไม่มี automation"]


def test_parse_lead_fallback():
    """reply ไม่มี JSON → ใช้ทั้งข้อความเป็น summary"""
    from src.agents.sales_agent import _parse_lead_from_reply
    reply = "ลูกค้าสนใจทำเว็บ แต่ยังไม่ให้ข้อมูลครบ"
    result = _parse_lead_from_reply(reply)
    assert result["customer_name"] == ""  # default
    assert result["summary_thai"] == reply  # ใช้ทั้ง reply เป็น summary


# ── Sales Node Integration ───────────────────────────────


@patch("src.agents.sales_agent.call_llm")
def test_sales_node_basic(mock_llm, tmp_path, monkeypatch):
    """sales_node เรียก LLM → parse JSON → save CRM"""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "test_crm.db")

    mock_llm.return_value = json.dumps({
        "customer_name": "ทดสอบ",
        "company": "TestCorp",
        "pain_points": ["เว็บเก่า", "SEO ไม่ดี"],
        "needs": ["ทำเว็บใหม่", "SEO"],
        "goals": ["เพิ่ม traffic 2x"],
        "timeline": "1 เดือน",
        "summary_thai": "ต้องการรีแบรนด์เว็บ",
    }, ensure_ascii=False)

    from src.agents.sales_agent import sales_node

    state = {
        "input": "ช่วยทำเว็บหน่อยครับ",
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
    }

    result = sales_node(state)
    assert "sales" in result["results"]
    parsed = json.loads(result["results"]["sales"])
    assert parsed["lead_id"] > 0
    assert parsed["lead_data"]["customer_name"] == "ทดสอบ"
    assert parsed["lead_data"]["company"] == "TestCorp"

    # verify CRM มีข้อมูล
    from src.tools.crm import get_lead
    lead = get_lead(parsed["lead_id"])
    assert lead is not None
    assert lead["name"] == "ทดสอบ"
    assert lead["company"] == "TestCorp"
    assert "เว็บเก่า" in lead["pain_points"]


@patch("src.agents.sales_agent.call_llm")
def test_sales_node_llm_error_graceful(mock_llm, tmp_path, monkeypatch):
    """LLM error → fallback โดยไม่ crash"""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "test_crm.db")
    mock_llm.side_effect = Exception("API Timeout")

    from src.agents.sales_agent import sales_node

    state = {
        "input": "ช่วยด้วย",
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
    }

    result = sales_node(state)
    assert "sales" in result["results"]
    parsed = json.loads(result["results"]["sales"])
    assert parsed["status"] == "complete"  # ไม่ crash


@patch("src.agents.sales_agent.call_llm")
def test_sales_node_multiple_leads(mock_llm, tmp_path, monkeypatch):
    """save หลาย lead → ทุก lead ได้รับการบันทึก"""
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "test_crm.db")

    from src.agents.sales_agent import sales_node
    from src.tools.crm import list_leads

    for i in range(3):
        mock_llm.return_value = json.dumps({
            "customer_name": f"ลูกค้า {i+1}",
            "company": f"Company{i+1}",
            "summary_thai": f"lead #{i+1}",
        }, ensure_ascii=False)

        state = {
            "input": f"ต้องการเว็บ #{i+1}",
            "plan": "", "current_agent": "",
            "messages": [], "results": {}, "final_output": "", "error": None,
        }
        sales_node(state)

    leads = list_leads()
    assert len(leads) >= 3
    names = [l["name"] for l in leads]
    assert "ลูกค้า 1" in names
    assert "ลูกค้า 3" in names
