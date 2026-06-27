"""
Aetox Works — Tool Registry

เครื่องมือพร้อมใช้งานสำหรับทุก agent
Agent สร้าง node function → import tool → เรียกใช้ได้ทันที
"""
from typing import Any

# ── Registry ──────────────────────────────────────────────

TOOL_REGISTRY = {
    # Sales 🗣️
    "crm.save_lead": "บันทึก lead ใหม่ ลง SQLite → return lead_id",
    "crm.get_lead": "ดึงข้อมูล lead ตาม id",
    "crm.list_leads": "แสดงรายการ leads (กรองตาม status ได้)",
    "chat.run_chat_server": "เปิด Web Chat Server (FastAPI + UI)",

    # Research 🔍
    "searcher.web_search": "ค้นหาเว็บด้วย Firecrawl → list[dict]",
    "searcher.scrape_url": "ดึงเนื้อหาจาก URL ด้วย Firecrawl → str",
    "searcher.semantic_search": "Semantic search ด้วย Exa → list[dict]",

    # Content ✍️
    "content_store.save_draft": "บันทึก draft ใหม่ ลง SQLite → return draft_id",
    "content_store.get_draft": "ดึง draft ตาม id",
    "content_store.list_drafts": "แสดงรายการ drafts (กรองตามประเภทได้)",

    # Dev 💻
    "builder.generate_landing": "สร้าง Landing Page HTML → {path, url}",
    "builder.generate_html": "เขียน HTML ตามกำหนด → {path, url}",
    "builder.write_file": "เขียนไฟล์ไปยัง path ใด ๆ → {path, size}",
    "builder.list_projects": "แสดงรายการโปรเจคที่สร้างไว้",
    "builder.serve_preview": "เปิด Preview Server → {url, port}",

    # Data 📊
    "reporter.save_metric": "บันทึก metric → return metric_id",
    "reporter.aggregate_metrics": "รวม metrics → {metric_name: sum}",
    "reporter.save_report": "บันทึกรายงาน → return report_id",
    "reporter.get_report": "ดึงรายงานตาม id",
    "reporter.generate_summary": "สรุปข้อมูลด้วย LLM → str",
}

# ── Agent-to-Tools Mapping ────────────────────────────────

AGENT_TOOLS = {
    "sales":    ["crm", "chat"],
    "research": ["searcher"],
    "content":  ["content_store"],
    "dev":      ["builder"],
    "data":     ["reporter", "crm", "content_store", "builder"],
}
