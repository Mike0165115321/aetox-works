"""Smoke tests for Tools — ตรวจสอบว่า import ได้และฟังก์ชันหลักทำงาน"""

# ── CRM ──────────────────────────────────────────────────

def test_crm_import():
    from src.tools.crm import init_db, save_lead, get_lead, list_leads
    assert callable(init_db)
    assert callable(save_lead)


def test_crm_save_and_get(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tools.crm._DB_PATH", tmp_path / "crm.db")
    from src.tools.crm import init_db, save_lead, get_lead
    init_db()
    lid = save_lead(name="ทดสอบ", company="TestCo", summary="ลูกค้าต้องการทำเว็บ")
    assert lid > 0
    lead = get_lead(lid)
    assert lead is not None
    assert lead["name"] == "ทดสอบ"
    assert lead["company"] == "TestCo"


# ── Content Store ────────────────────────────────────────

def test_content_store_import():
    from src.tools.content_store import init_db, save_draft, get_draft, list_drafts
    assert callable(init_db)
    assert callable(save_draft)


def test_content_store_save(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tools.content_store._DB_PATH", tmp_path / "content.db")
    from src.tools.content_store import init_db, save_draft, get_draft
    init_db()
    did = save_draft(title="หน้าแรก", body="เนื้อหาแซมเปิล", content_type="landing")
    assert did > 0
    draft = get_draft(did)
    assert draft is not None
    assert draft["title"] == "หน้าแรก"


# ── Builder ──────────────────────────────────────────────

def test_builder_import():
    from src.tools.builder import generate_landing, generate_html, write_file
    assert callable(generate_landing)
    assert callable(generate_html)


def test_builder_generate_landing(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tools.builder._OUTPUT_DIR", tmp_path / "websites")
    from src.tools.builder import generate_landing

    result = generate_landing(
        title="Test Page",
        headline="สวัสดี",
        subheadline="ยินดีต้อนรับ",
        features=[{"title": "ฟีเจอร์", "desc": "รายละเอียด"}],
    )
    assert result["path"].endswith(".html")
    html = result["html"]
    assert "สวัสดี" in html
    assert "ยินดีต้อนรับ" in html


# ── Reporter ─────────────────────────────────────────────

def test_reporter_import():
    from src.tools.reporter import init_db, save_metric, aggregate_metrics, save_report
    assert callable(init_db)
    assert callable(save_metric)
    assert callable(save_report)


# ── Searcher ─────────────────────────────────────────────

def test_searcher_import():
    """ตรวจสอบว่า import searcher ได้ (ไม่ต้องเรียก API จริง)"""
    from src.tools.searcher import web_search, semantic_search, scrape_url
    assert callable(web_search)
    assert callable(semantic_search)
    assert callable(scrape_url)


# ── Chat Server ──────────────────────────────────────────

def test_chat_server_import():
    from src.tools.chat_server import create_app
    app = create_app()
    assert app is not None
