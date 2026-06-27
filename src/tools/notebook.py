"""
Aetox Works — Notebook Tool (Sales Agent 📓)

ไฟล์ Notebook จริงบนดิสก์ — เปิดอ่าน/ตรวจสอบได้ตลอด
Format: Markdown — เขียนโดย Sales Agent, อ่านโดยคนและ AI
Location: data/notebooks/lead_{id}.md
"""
import os
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import Any

_NOTEBOOK_DIR = Path(__file__).parent.parent.parent / "data" / "notebooks"


def _ensure_dir():
    _NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)


def _notebook_path(lead_id: int | str) -> Path:
    return _NOTEBOOK_DIR / f"lead_{lead_id}.md"


def _safe_notebook_id(value: int | str) -> str:
    raw = unicodedata.normalize("NFKC", str(value).strip().lower())
    chars: list[str] = []
    for ch in raw:
        if ch.isspace() or ch in "_-":
            if chars and chars[-1] != "-":
                chars.append("-")
            continue
        if ch in '\\/:*?"<>|' or ord(ch) < 32:
            continue
        if ch.isalnum() or unicodedata.category(ch).startswith("M"):
            chars.append(ch)
    safe = "".join(chars).strip("-")
    safe = re.sub(r"-{2,}", "-", safe)
    return safe[:56].strip("-")


def build_notebook_title(name: str = "", company: str = "", fallback_id: str = "") -> str:
    """Build a human-readable notebook title from customer identity."""
    name = str(name or "").strip()
    company = str(company or "").strip()
    if company and name:
        return f"{company} — {name}"
    if company:
        return company
    if name:
        return name
    return f"Lead #{fallback_id}" if fallback_id else "New Lead"


def build_notebook_id(name: str = "", company: str = "", fallback_id: str = "") -> str:
    """Build a stable, filesystem-safe notebook id from customer identity."""
    title = build_notebook_title(name=name, company=company, fallback_id=fallback_id)
    base = _safe_notebook_id(title) or _safe_notebook_id(fallback_id) or datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = _safe_notebook_id(fallback_id)[-6:]
    if suffix and suffix not in base:
        base = f"{base}-{suffix}"
    return base[:64].strip("-")


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


def rename_notebook(old_id: int | str, new_id: int | str, title: str = "") -> str:
    """Rename a notebook file and return the final notebook id."""
    _ensure_dir()
    old_id = str(old_id)
    safe_new_id = _safe_notebook_id(new_id)
    if not old_id or not safe_new_id:
        return old_id

    old_path = _notebook_path(old_id)
    if not old_path.exists():
        return old_id

    final_id = safe_new_id
    final_path = _notebook_path(final_id)
    if final_path.resolve() != old_path.resolve():
        counter = 2
        while final_path.exists():
            final_id = f"{safe_new_id}-{counter}"
            final_path = _notebook_path(final_id)
            counter += 1
        old_path.rename(final_path)

    if title:
        _retitle_notebook(final_path, title)
    return final_id


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
        customer = _extract_table_value(text, "Name")
        company = _extract_table_value(text, "Company")
        created = _extract_meta_value(text, "Created")
        updated = _extract_meta_value(text, "Last Updated")
        notebooks.append({
            "id": f.stem.replace("lead_", ""),
            "path": str(f),
            "status": status,
            "title": first_line.replace("# 📓 ", ""),
            "customer": customer,
            "company": company,
            "created": created,
            "updated": updated,
            "size": f.stat().st_size,
        })
    return notebooks


def delete_notebook(nb_id: str) -> bool:
    """Delete a notebook file"""
    path = _notebook_path(nb_id)
    if path.exists():
        path.unlink()
        return True
    return False


def delete_all_notebooks() -> int:
    """Delete all notebook files and return the number removed."""
    _ensure_dir()
    count = 0
    for path in _NOTEBOOK_DIR.glob("lead_*.md"):
        if path.is_file():
            path.unlink()
            count += 1
    return count


# ── Internal helpers ──────────────────────────────────────

def _update_timestamp(text: str, now: str) -> str:
    """Update 'Last Updated' line"""
    import re
    return re.sub(r"\*\*Last Updated:\*\* .*", f"**Last Updated:** {now}", text)


def _retitle_notebook(path: Path, title: str) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return
    lines[0] = f"# 📓 Sales Notebook — {title}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = "\n".join(lines)
    text = _update_timestamp(text, now)
    path.write_text(text + ("\n" if text and not text.endswith("\n") else ""), encoding="utf-8")


def _extract_meta_value(text: str, key: str) -> str:
    m = re.search(rf"\*\*{re.escape(key)}:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else ""


def _extract_table_value(text: str, field: str) -> str:
    m = re.search(rf"\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|", text)
    return m.group(1).strip() if m else ""


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
    summary = data.get("summary", "")
    if summary:
        parts.append(f"### Notes Summary\n{summary}")

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
