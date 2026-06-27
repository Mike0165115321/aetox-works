"""Tests for Research Agent — Phase 3"""
import json
from unittest.mock import patch

# ── Search Query Builder ──────────────────────────────────


def test_build_query_with_full_sales_data():
    """มี sales data ครบ → สร้าง query จาก company + needs + pain_points"""
    from src.agents.research_agent import _build_search_query
    sales_data = {
        "company": "ThaiTech",
        "needs": ["ทำเว็บ e-commerce", "SEO"],
        "pain_points": ["ยอดขายตก"],
    }
    query = _build_search_query(sales_data, "default fallback")
    assert "ThaiTech" in query
    assert "e-commerce" in query
    assert "ยอดขายตก" in query


def test_build_query_no_sales_data():
    """ไม่มี sales data → fallback ไป user_input"""
    from src.agents.research_agent import _build_search_query
    query = _build_search_query(None, "ตลาด AI ประเทศไทย")
    assert query == "ตลาด AI ประเทศไทย"


def test_build_query_minimal_sales_data():
    """มีแค่ company"""
    from src.agents.research_agent import _build_search_query
    query = _build_search_query({"company": "GreenCo"}, "fallback")
    assert "GreenCo" in query


# ── JSON Extraction ──────────────────────────────────────


def test_extract_research_json_code_block():
    """Extract JSON จาก code block"""
    from src.agents.research_agent import _extract_research_json
    text = '''วิเคราะห์แล้ว
```json
{"market_overview": "ตลาดโต 15%", "keywords": ["AI", "automation"]}
```'''
    result = _extract_research_json(text)
    assert result["market_overview"] == "ตลาดโต 15%"
    assert "AI" in result["keywords"]


def test_extract_research_json_inline():
    """Extract JSON แบบ inline"""
    from src.agents.research_agent import _extract_research_json
    text = '{"insights": ["ตลาดกำลังโต", "คู่แข่งน้อย"], "summary_thai": "โอกาสดี"}'
    result = _extract_research_json(text)
    assert len(result["insights"]) == 2
    assert result["summary_thai"] == "โอกาสดี"


# ── Research Node ────────────────────────────────────────


@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
def test_research_node_basic(mock_llm, mock_exa, mock_firecrawl):
    """research_node: search → synthesize → structured output"""
    mock_firecrawl.return_value = [
        {"title": "Market Report 2025", "url": "https://example.com/1",
         "description": "AI market growing", "content": "The market is huge..."},
    ]
    mock_exa.return_value = [
        {"title": "Competitor Analysis", "url": "https://ex.com/2",
         "text": "Top competitors in the space..."},
    ]
    mock_llm.return_value = json.dumps({
        "market_overview": "ตลาด AI กำลังโต 25% ต่อปี",
        "competitors": [{"name": "คู่แข่ง A", "strengths": ["price"], "weaknesses": ["support"]}],
        "keywords": ["AI", "automation", "enterprise"],
        "insights": ["ตลาดยังมีช่องว่าง"],
        "references": [{"title": "Market Report", "url": "https://example.com/1"}],
        "summary_thai": "ตลาด AI มีโอกาสสูง แนะนำเจาะกลุ่ม enterprise",
    }, ensure_ascii=False)

    from src.agents.research_agent import research_node

    state = {
        "input": "ตลาด AI ประเทศไทย",
        "plan": "", "current_agent": "",
        "messages": [], "results": {
            "sales": json.dumps({
                "lead_data": {"company": "ThaiTech", "needs": ["AI solution"]}
            }, ensure_ascii=False)
        }, "final_output": "", "error": None,
    }

    result = research_node(state)
    assert "research" in result["results"]
    parsed = json.loads(result["results"]["research"])
    findings = parsed["findings"]
    assert findings["market_overview"] != ""
    assert len(findings["keywords"]) >= 1
    assert findings["summary_thai"] != ""
    assert parsed["sources"] == 2
    assert parsed["source_mode"] == "real"
    assert parsed["status"] == "complete"


@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
def test_research_node_search_errors_graceful(mock_llm, mock_exa, mock_firecrawl):
    """search error → ไม่ crash, LLM ยังทำงาน"""
    mock_firecrawl.side_effect = Exception("API down")
    mock_exa.side_effect = Exception("API down")
    mock_llm.return_value = json.dumps({
        "summary_thai": "ใช้ LLM knowledge",
        "keywords": ["general"],
    }, ensure_ascii=False)

    from src.agents.research_agent import research_node

    state = {
        "input": "test query", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = research_node(state)
    assert "research" in result["results"]
    parsed = json.loads(result["results"]["research"])
    assert parsed["sources"] == 0  # searches failed
    assert parsed["source_mode"] == "none"
    assert parsed["warnings"]
    assert parsed["status"] == "partial"  # ไม่ crash แต่ไม่หลอกว่า complete เต็ม


@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
def test_research_node_marks_demo_sources_as_partial(mock_llm, mock_exa, mock_firecrawl):
    """DEMO fallback from missing search keys is visible in structured output."""
    mock_firecrawl.return_value = [
        {"title": "[FIRECRAWL DEMO] Result", "url": "https://example.com", "description": "demo"},
    ]
    mock_exa.return_value = [
        {"title": "[EXA DEMO] Result", "url": "https://example.com", "text": "demo"},
    ]
    mock_llm.return_value = json.dumps({"summary_thai": "demo research"}, ensure_ascii=False)

    from src.agents.research_agent import research_node

    state = {
        "input": "ตลาด AI", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = research_node(state)
    parsed = json.loads(result["results"]["research"])
    assert parsed["source_mode"] == "demo"
    assert parsed["status"] == "partial"


@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
@patch("src.agents.research_agent.scrape_url")
def test_research_node_deep_scrape(mock_scrape, mock_llm, mock_exa, mock_firecrawl):
    """มี URLs → scrape deep content"""
    mock_firecrawl.return_value = [
        {"title": "Page 1", "url": "https://example.com/1", "description": "desc1"},
        {"title": "Page 2", "url": "https://example.com/2", "description": "desc2"},
    ]
    mock_exa.return_value = []
    mock_scrape.return_value = "Deep content from page"
    mock_llm.return_value = json.dumps({"summary_thai": "deep research done"}, ensure_ascii=False)

    from src.agents.research_agent import research_node

    state = {
        "input": "deep research", "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = research_node(state)
    parsed = json.loads(result["results"]["research"])
    assert parsed["deep_scrapes"] == 2


@patch("src.agents.research_agent.web_search")
@patch("src.agents.research_agent.semantic_search")
@patch("src.agents.research_agent.call_llm")
def test_research_node_no_json_fallback(mock_llm, mock_exa, mock_firecrawl):
    """LLM ไม่คืน JSON → fallback summary"""
    mock_firecrawl.return_value = []
    mock_exa.return_value = []
    mock_llm.return_value = "ไม่มีข้อมูลในระบบตอนนี้"

    from src.agents.research_agent import research_node

    state = {
        "input": "query",
        "plan": "", "current_agent": "",
        "messages": [], "results": {}, "final_output": "", "error": None,
    }

    result = research_node(state)
    parsed = json.loads(result["results"]["research"])
    assert parsed["findings"]["summary_thai"] == "ไม่มีข้อมูลในระบบตอนนี้"
    assert parsed["status"] == "partial"
