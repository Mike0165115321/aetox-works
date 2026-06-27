"""
Aetox Works — CRM Tool (Sales Agent 🗣️)

ระบบจัดการ Lead / ลูกค้า พร้อม SQLite
สำหรับเก็บข้อมูลที่ Sales Agent สอบถามจากลูกค้า
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

_DB_PATH = Path(__file__).parent.parent.parent / "data" / "crm.db"


def _get_conn() -> sqlite3.Connection:
    """เปิด connection ไปยัง SQLite (สร้าง db file ถ้ายังไม่มี)"""
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """สร้างตาราง leads ถ้ายังไม่มี"""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL DEFAULT '',
                company     TEXT NOT NULL DEFAULT '',
                pain_points TEXT NOT NULL DEFAULT '[]',
                needs       TEXT NOT NULL DEFAULT '[]',
                goals       TEXT NOT NULL DEFAULT '[]',
                timeline    TEXT NOT NULL DEFAULT '',
                summary     TEXT NOT NULL DEFAULT '',
                status      TEXT NOT NULL DEFAULT 'new',
                created_at  TEXT NOT NULL DEFAULT (datetime('now')),

                -- extra metadata
                source      TEXT NOT NULL DEFAULT 'web_chat',
                email       TEXT NOT NULL DEFAULT '',
                phone       TEXT NOT NULL DEFAULT ''
            )
        """)


def save_lead(
    name: str = "",
    company: str = "",
    pain_points: list[str] | None = None,
    needs: list[str] | None = None,
    goals: list[str] | None = None,
    timeline: str = "",
    summary: str = "",
    source: str = "web_chat",
    email: str = "",
    phone: str = "",
) -> int:
    """
    บันทึก lead ใหม่ ลง SQLite

    Args:
        name: ชื่อลูกค้า
        company: ชื่อบริษัท
        pain_points: รายการปัญหาที่เจอ
        needs: รายการความต้องการ
        goals: เป้าหมายที่อยากได้
        timeline: กรอบเวลา / ความเร่งด่วน
        summary: สรุปภาษาไทยสั้น ๆ
        source: แหล่งที่มา (web_chat, email, ฯลฯ)
        email: อีเมลลูกค้า
        phone: เบอร์โทรศัพท์

    Returns:
        lead_id (int): ไอดีของ lead ที่สร้าง
    """
    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO leads
               (name, company, pain_points, needs, goals, timeline, summary, source, email, phone)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name,
                company,
                json.dumps(pain_points or [], ensure_ascii=False),
                json.dumps(needs or [], ensure_ascii=False),
                json.dumps(goals or [], ensure_ascii=False),
                timeline,
                summary,
                source,
                email,
                phone,
            ),
        )
        return cur.lastrowid


def get_lead(lead_id: int) -> dict | None:
    """ดึงข้อมูล lead ตาม id"""
    init_db()
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if row is None:
            return None
        return _row_to_dict(row)


def list_leads(status: str | None = None, limit: int = 50) -> list[dict]:
    """
    ดึงรายการ leads

    Args:
        status: กรองตามสถานะ (None = ทั้งหมด)
        limit: จำนวนสูงสุด

    Returns:
        list ของ dict lead
    """
    init_db()
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM leads WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM leads ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [_row_to_dict(r) for r in rows]


def update_lead_status(lead_id: int, status: str) -> bool:
    """อัปเดตสถานะ lead (new → contacted → qualified → closed)"""
    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            "UPDATE leads SET status = ? WHERE id = ?", (status, lead_id)
        )
        return cur.rowcount > 0


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    # แปลง JSON string → list
    for field in ("pain_points", "needs", "goals"):
        if isinstance(d.get(field), str):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                d[field] = []
    return d
