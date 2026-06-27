"""
Aetox Works — Content Store Tool (Content Agent ✍️)

ระบบเก็บ Draft คอนเทนต์แบบ SQLite
ใช้เก็บ content ที่ Content Agent สร้างไว้
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

_DB_PATH = Path(__file__).parent.parent.parent / "data" / "content.db"


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """สร้างตาราง drafts ถ้ายังไม่มี"""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL DEFAULT '',
                content_type TEXT NOT NULL DEFAULT 'landing',
                body        TEXT NOT NULL DEFAULT '',
                cta         TEXT NOT NULL DEFAULT '',
                tone        TEXT NOT NULL DEFAULT 'professional',
                target      TEXT NOT NULL DEFAULT '',
                metadata    TEXT NOT NULL DEFAULT '{}',
                status      TEXT NOT NULL DEFAULT 'draft',
                lead_id     INTEGER DEFAULT NULL,
                created_at  TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


def save_draft(
    title: str = "",
    content_type: str = "landing",
    body: str = "",
    cta: str = "",
    tone: str = "professional",
    target: str = "",
    metadata: dict | None = None,
    lead_id: int | None = None,
) -> int:
    """
    บันทึก draft ใหม่

    Args:
        title: หัวข้อ
        content_type: ประเภท (landing, blog, social, email)
        body: เนื้อหา
        cta: Call-to-action
        tone: น้ำเสียง (professional, casual, friendly)
        target: กลุ่มเป้าหมาย
        metadata: ข้อมูลเพิ่มเติม (dict)
        lead_id: เชื่อมโยงกับ lead (ไม่บังคับ)

    Returns:
        draft_id (int)
    """
    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO drafts
               (title, content_type, body, cta, tone, target, metadata, lead_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                title,
                content_type,
                body,
                cta,
                tone,
                target,
                json.dumps(metadata or {}, ensure_ascii=False),
                lead_id,
            ),
        )
        return cur.lastrowid


def get_draft(draft_id: int) -> dict | None:
    """ดึง draft ตาม id"""
    init_db()
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
        if row is None:
            return None
        return _row_to_dict(row)


def list_drafts(content_type: str | None = None, limit: int = 20) -> list[dict]:
    """
    ดึงรายการ drafts

    Args:
        content_type: กรองตามประเภท (None = ทั้งหมด)
        limit: จำนวนสูงสุด
    """
    init_db()
    with _get_conn() as conn:
        if content_type:
            rows = conn.execute(
                "SELECT * FROM drafts WHERE content_type = ? ORDER BY updated_at DESC LIMIT ?",
                (content_type, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM drafts ORDER BY updated_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [_row_to_dict(r) for r in rows]


def update_draft(draft_id: int, **fields) -> bool:
    """
    อัปเดต draft (เฉพาะฟิลด์ที่ส่ง)
    เช่น update_draft(1, body="new content", status="published")
    """
    allowed = {"title", "body", "cta", "tone", "target", "content_type", "status"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [datetime.now().isoformat()]

    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            f"UPDATE drafts SET {set_clause}, updated_at = ? WHERE id = ?",
            (*values, draft_id),
        )
        return cur.rowcount > 0


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    if isinstance(d.get("metadata"), str):
        try:
            d["metadata"] = json.loads(d["metadata"])
        except (json.JSONDecodeError, TypeError):
            d["metadata"] = {}
    return d
