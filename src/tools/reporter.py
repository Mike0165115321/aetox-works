"""
Aetox Works — Reporter Tool (Data Agent 📊)

เก็บ metrics, สร้าง report, ทำ charts
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.llm.client import call_llm

_DB_PATH = Path(__file__).parent.parent.parent / "data" / "metrics.db"


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """สร้างตาราง metrics + reports ถ้ายังไม่มี"""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name  TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL DEFAULT 0,
                unit        TEXT NOT NULL DEFAULT '',
                metadata    TEXT NOT NULL DEFAULT '{}',
                recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL DEFAULT '',
                summary     TEXT NOT NULL DEFAULT '',
                data        TEXT NOT NULL DEFAULT '{}',
                report_type TEXT NOT NULL DEFAULT 'weekly',
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


# ── Metrics ───────────────────────────────────────────────

def save_metric(
    agent_name: str,
    metric_name: str,
    metric_value: float,
    unit: str = "",
    metadata: dict | None = None,
) -> int:
    """
    บันทึก metric

    Args:
        agent_name: ชื่อ agent (sales, research, content, dev, data)
        metric_name: ชื่อ metric (leads_collected, pages_built, etc.)
        metric_value: ค่าตัวเลข
        unit: หน่วย
        metadata: ข้อมูลเพิ่มเติม

    Returns:
        metric_id (int)
    """
    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO metrics
               (agent_name, metric_name, metric_value, unit, metadata)
               VALUES (?, ?, ?, ?, ?)""",
            (agent_name, metric_name, metric_value, unit,
             json.dumps(metadata or {}, ensure_ascii=False)),
        )
        return cur.lastrowid


def get_metrics(
    agent_name: str | None = None,
    metric_name: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """
    ดึง metrics พร้อมกรอง

    Args:
        agent_name: กรองตาม agent (None = ทั้งหมด)
        metric_name: กรองตามชื่อ metric (None = ทั้งหมด)
        limit: จำนวนสูงสุด
    """
    init_db()
    with _get_conn() as conn:
        conditions = []
        params = []
        if agent_name:
            conditions.append("agent_name = ?")
            params.append(agent_name)
        if metric_name:
            conditions.append("metric_name = ?")
            params.append(metric_name)

        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        rows = conn.execute(
            f"SELECT * FROM metrics {where} ORDER BY recorded_at DESC LIMIT ?",
            (*params, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]


def aggregate_metrics(agent_name: str | None = None) -> dict[str, float]:
    """
    รวม metrics: SUM ของแต่ละ metric_name

    Args:
        agent_name: กรองตาม agent (None = ทั้งหมด)

    Returns:
        { "leads_collected": 5, "pages_built": 2, ... }
    """
    init_db()
    with _get_conn() as conn:
        if agent_name:
            rows = conn.execute(
                "SELECT metric_name, SUM(metric_value) as total FROM metrics "
                "WHERE agent_name = ? GROUP BY metric_name",
                (agent_name,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT metric_name, SUM(metric_value) as total FROM metrics "
                "GROUP BY metric_name"
            ).fetchall()
        return {r["metric_name"]: r["total"] for r in rows}


# ── Reports ───────────────────────────────────────────────

def save_report(
    title: str,
    summary: str,
    data: dict | None = None,
    report_type: str = "summary",
) -> int:
    """
    บันทึกรายงาน

    Args:
        title: หัวข้อรายงาน
        summary: สรุป
        data: ข้อมูล structured
        report_type: ประเภท (summary, weekly, monthly, performance)

    Returns:
        report_id (int)
    """
    init_db()
    with _get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO reports (title, summary, data, report_type) VALUES (?, ?, ?, ?)",
            (title, summary, json.dumps(data or {}, ensure_ascii=False), report_type),
        )
        return cur.lastrowid


def get_report(report_id: int) -> dict | None:
    """ดึงรายงานตาม id"""
    init_db()
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
        if row is None:
            return None
        return _row_to_dict(row)


def list_reports(report_type: str | None = None, limit: int = 10) -> list[dict]:
    """ดึงรายการรายงาน"""
    init_db()
    with _get_conn() as conn:
        if report_type:
            rows = conn.execute(
                "SELECT * FROM reports WHERE report_type = ? ORDER BY created_at DESC LIMIT ?",
                (report_type, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reports ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [_row_to_dict(r) for r in rows]


# ── LLM Summary ───────────────────────────────────────────

def generate_summary(data: dict[str, Any], prompt: str = "") -> str:
    """
    สร้างสรุปด้วย LLM จากข้อมูล

    Args:
        data: ข้อมูลที่ต้องการสรุป
        prompt: คำแนะนำเพิ่มเติม

    Returns:
        สรุปภาษาไทย
    """
    system = "คุณคือ Data Analyst สรุปข้อมูลให้เข้าใจง่าย ใช้ภาษาไทย"
    user = f"ข้อมูล:\n{json.dumps(data, ensure_ascii=False, indent=2)}\n\n{prompt}" if prompt else \
           f"ข้อมูล:\n{json.dumps(data, ensure_ascii=False, indent=2)}\n\nกรุณาสรุปข้อมูลนี้"
    try:
        return call_llm(user, system_prompt=system)
    except Exception as e:
        log.warning("Summary LLM error: %s", e)
        return f"[สรุปข้อมูล] พบ {len(data)} รายการ"


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    for field in ("metadata", "data"):
        if isinstance(d.get(field), str):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                d[field] = {}
    return d


# Need logging
import logging
log = logging.getLogger("aetox.reporter")
