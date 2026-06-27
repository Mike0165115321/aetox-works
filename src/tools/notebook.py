"""
Aetox Works — Notebook Tool (Sales Agent 📓)

ไฟล์ Notebook จริงบนดิสก์ — เปิดอ่าน/ตรวจสอบได้ตลอด
Format: Markdown — เขียนโดย Sales Agent, อ่านโดยคนและ AI
Location: data/notebooks/lead_{id}.md
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Any

_NOTEBOOK_DIR = Path(__file__).parent.parent.parent / "data" / "notebooks"


def _ensure_dir():
    _NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)


def _notebook_path(lead_id: int | str) -> Path:
    return _NOTEBOOK_DIR / f"lead_{lead_id}.md"


def create_notebook(lead_id: int | str) -> str:
    """
    สร้างไฟล์ notebook ใหม่สำหรับ lead

    Returns:
        path ของไฟล์ที่สร้าง
    """
    _ensure_dir()
    path = _notebook_path(lead_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# 📓 Sales Notebook — Lead #{lead_id}

**Status:** 🟡 in_progress
**Created:** {now}
**Last Updated:** {now}

---

## 👤 Customer Info

| Field | Value |
|-------|-------|
| Name | |
| Company | |
| Contact | |

## 💼 Business Requirements

### Pain Points
*(ยังไม่มีข้อมูล)*

### Needs
*(ยังไม่มีข้อมูล)*

### Goals
*(ยังไม่มีข้อมูล)*

### Timeline
*(ยังไม่มีข้อมูล)*

---

## 📝 Conversation Log

"""
    path.write_text(content, encoding="utf-8")
    return str(path)


def read_notebook(lead_id: int | str) -> str | None:
    """อ่านเนื้อหา notebook"""
    path = _notebook_path(lead_id)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def update_notebook(lead_id: int | str, section: str, content: str) -> str:
    """
    อัปเดต section ใน notebook

    Args:
        lead_id: เลข lead
        section: "customer" | "business" | "log"
        content: เนื้อหาที่จะเพิ่ม
    """
    _ensure_dir()
    path = _notebook_path(lead_id)

    if not path.exists():
        create_notebook(lead_id)

    text = path.read_text(encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if section == "customer":
        text = _replace_section(text, "## 👤 Customer Info", _format_customer_section(content))
    elif section == "business":
        text = _replace_section(text, "## 💼 Business Requirements", _format_business_section(content))
    elif section == "log":
        # Append to conversation log
        text += f"- {now} | {content}\n"
    elif section == "confirm":
        text = text.replace("🟡 in_progress", "🟢 confirmed")

    # Update timestamp
    text = _update_timestamp(text, now)

    path.write_text(text, encoding="utf-8")
    return str(path)


def lock_notebook(lead_id: int | str) -> str:
    """Lock notebook — mark as confirmed"""
    _ensure_dir()
    path = _notebook_path(lead_id)
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = text.replace("🟡 in_progress", "🟢 confirmed")
    text = _update_timestamp(text, now)
    path.write_text(text, encoding="utf-8")
    return str(path)


def list_notebooks() -> list[dict[str, Any]]:
    """List all notebooks"""
    _ensure_dir()
    notebooks = []
    for f in sorted(_NOTEBOOK_DIR.glob("lead_*.md"), reverse=True):
        text = f.read_text(encoding="utf-8")
        status = "confirmed" if "🟢 confirmed" in text else "in_progress"
        first_line = text.split("\n")[0] if text else f.stem
        notebooks.append({
            "id": f.stem.replace("lead_", ""),
            "path": str(f),
            "status": status,
            "title": first_line.replace("# 📓 ", ""),
            "size": f.stat().st_size,
        })
    return notebooks


# ── Internal helpers ──────────────────────────────────────

def _update_timestamp(text: str, now: str) -> str:
    """Update 'Last Updated' line"""
    import re
    return re.sub(r"\*\*Last Updated:\*\* .*", f"**Last Updated:** {now}", text)


def _replace_section(text: str, section_header: str, new_content: str) -> str:
    """Replace a section between header and next '---' or '## '"""
    import re
    # Find the section and replace everything until next section or end
    pattern = re.escape(section_header) + r".*?(?=\n---\n|\n## |\Z)"
    replacement = section_header + "\n\n" + new_content.strip()
    return re.sub(pattern, replacement, text, flags=re.DOTALL)


def _format_customer_section(data: dict | str) -> str:
    """Format customer data as markdown table"""
    if isinstance(data, str):
        try:
            import json
            data = json.loads(data)
        except Exception:
            return data
    name = data.get("name", "") if isinstance(data, dict) else ""
    company = data.get("company", "") if isinstance(data, dict) else ""
    contact = data.get("contact", "") if isinstance(data, dict) else ""
    return f"""| Field | Value |
|-------|-------|
| Name | {name} |
| Company | {company} |
| Contact | {contact} |"""


def _format_business_section(data: dict | str) -> str:
    """Format business data as markdown lists"""
    if isinstance(data, str):
        try:
            import json
            data = json.loads(data)
        except Exception:
            return data
    if not isinstance(data, dict):
        return str(data)

    parts = []
    for field, label in [("pain_points", "Pain Points"), ("needs", "Needs"),
                          ("goals", "Goals")]:
        items = data.get(field, [])
        if items:
            parts.append(f"### {label}")
            parts.extend(f"- {item}" for item in items)
        else:
            parts.append(f"### {label}\n*(ยังไม่มีข้อมูล)*")

    timeline = data.get("timeline", "")
    if timeline:
        parts.append(f"### Timeline\n- {timeline}")

    return "\n\n".join(parts)
