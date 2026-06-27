"""
Aetox Works — Sales Agent 🗣️ (v3 — Notebook + Handoff)

บทบาท: นักขาย / นักการตลาด
หน้าที่:
  1. คุยกับลูกค้า ถามทีละคำถาม จดลงสมุดโน๊ต (sales_notebook) อย่างต่อเนื่อง
  2. แยกข้อมูลส่วนตัวลูกค้า กับข้อมูลธุรกิจออกจากกัน
  3. เมื่อข้อมูลธุรกิจครบ → สรุป → ขอคำยืนยัน
  4. ลูกค้ายืนยัน → สร้าง handoff_brief (เฉพาะข้อมูลธุรกิจ) → sales_confirmed = True
  5. handoff_brief คือสิ่งที่ agent อื่นเอาไปใช้ต่อ

ห้าม: สร้าง content, เขียนเว็บ, วิเคราะห์ตลาด — ไม่ใช่งาน Sales
ห้าม: เอาข้อมูลส่วนตัวลูกค้าใส่ใน handoff_brief
"""
import logging
import json
import re
from copy import deepcopy

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm, is_llm_failure
from src.tools.crm import init_db, save_lead, update_lead_status
from src.tools.notebook import (
    build_notebook_id,
    build_notebook_title,
    create_notebook,
    lock_notebook,
    rename_notebook,
    update_notebook,
)

log = logging.getLogger("aetox.agents.sales")
NB_MARKER_RE = r"\[NB:([^\]\r\n]+)\]"
NB_MARKER_FULL_RE = r"\[NB:[^\]\r\n]+\]\n?"

# ข้อมูลที่ Sales ต้องเก็บให้ครบก่อนขอ confirmation
REQUIRED_FIELDS = ["customer_name", "company", "needs", "goals"]

SALES_JSON_SCHEMA = {
    "customer_name": "",
    "company": "",
    "pain_points": [],
    "needs": [],
    "goals": [],
    "timeline": "",
    "summary_thai": "",
}


def _extract_json(text: str) -> dict:
    patterns = [
        r"```(?:json)?\s*(\{.*?\})\s*```",
        r"(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
    return {}


def _parse_conversation(context: str) -> dict:
    """Parse conversation history → extract what's been collected so far"""
    data = deepcopy(SALES_JSON_SCHEMA)

    if not context:
        return data

    # Try extracting from last summary JSON in context
    parsed = _extract_json(context)
    if parsed:
        # Map field names (รองรับทั้งไทย/อังกฤษ)
        field_map = {
            "customer_name": ["customer_name", "name", "ชื่อ", "ชื่อลูกค้า", "customer"],
            "company": ["company", "บริษัท", "company_name", "องค์กร"],
            "pain_points": ["pain_points", "pain point", "ปัญหา", "pain"],
            "needs": ["needs", "ความต้องการ", "need", "ต้องการ"],
            "goals": ["goals", "เป้าหมาย", "goal", "วัตถุประสงค์"],
            "timeline": ["timeline", "เวลา", "กำหนด", "deadline", "ภายใน"],
            "summary_thai": ["summary_thai", "summary", "สรุป"],
        }
        for target_key, aliases in field_map.items():
            for alias in aliases:
                if alias in parsed and parsed[alias]:
                    val = parsed[alias]
                    if isinstance(val, list):
                        data[target_key] = val
                    elif isinstance(val, str) and val.strip():
                        data[target_key] = val
                    break

    natural = _parse_natural_conversation(context)
    for key, val in natural.items():
        if isinstance(val, list):
            existing = data.setdefault(key, [])
            for item in val:
                if item and not _has_similar_item(existing, item):
                    existing.append(item)
        elif val and not data.get(key):
            data[key] = val

    return data


def _parse_natural_conversation(context: str) -> dict:
    """Best-effort extraction from Thai customer messages without relying on JSON."""
    data = deepcopy(SALES_JSON_SCHEMA)
    user_lines = [
        line.strip()
        for line in re.findall(r"ลูกค้า:\s*(.+)", context)
        if line.strip()
    ]

    for line in user_lines:
        clean = _clean_customer_line(line)
        if not clean or _is_confirmation_only(clean):
            continue

        name_m = re.search(r"(?:ผม|ฉัน|ดิฉัน|เรา)?\s*ชื่อ\s*([^\s,，]+)", clean)
        if name_m and not data["customer_name"]:
            data["customer_name"] = _strip_thai_polite(name_m.group(1))

        company_m = re.search(r"(?:บริษัท(?:ชื่อ)?|จากบริษัท)\s*([^\s,，]+)", clean)
        if company_m and not data["company"]:
            data["company"] = _strip_thai_polite(company_m.group(1))

        if _has_any(clean, ["ปัญหา", "ติด", "เจอ", "ช้า", "ไม่พอ", "ไม่ค่อย", "ยอดขายน้อย"]):
            _append_unique(data["pain_points"], clean)

        if _has_any(clean, ["ช่วย", "ต้องการ", "อยากให้", "ทำเว็บ", "ทำ landing", "landing page", "ระบบ", "automation"]):
            _append_unique(data["needs"], clean)

        if _has_any(clean, ["เป้าหมาย", "เพิ่ม", "ยอดขาย", "ลูกค้าใหม่", "ลูกค้า", "ต่อเดือน", "รายได้", "จากปัจจุบัน"]):
            _append_unique(data["goals"], clean)
            if "อยากได้" in clean and not data["needs"]:
                _append_unique(data["needs"], f"ต้องการให้ช่วยบรรลุเป้าหมาย: {clean}")

        timeline = _extract_timeline(clean)
        if timeline and not data["timeline"]:
            data["timeline"] = timeline

    summary_parts = []
    if data["needs"]:
        summary_parts.append("ต้องการ: " + "; ".join(data["needs"]))
    if data["goals"]:
        summary_parts.append("เป้าหมาย: " + "; ".join(data["goals"]))
    if data["timeline"]:
        summary_parts.append("กรอบเวลา: " + data["timeline"])
    data["summary_thai"] = " | ".join(summary_parts)
    return data


def _clean_customer_line(line: str) -> str:
    clean = re.sub(NB_MARKER_FULL_RE, "", line).strip()
    clean = re.sub(r"\s+", " ", clean)
    return clean


def _strip_thai_polite(text: str) -> str:
    return re.sub(r"(ครับ|ค่ะ|คะ|นะครับ|นะคะ)$", "", text.strip())


def _has_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _append_unique(items: list, item: str) -> None:
    item = item.strip()
    if item and not _has_similar_item(items, item):
        items.append(item)


def _has_similar_item(items: list, item: str) -> bool:
    normalized = item.strip()
    return any(normalized == existing or normalized in existing or existing in normalized for existing in items)


def _is_confirmation_only(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {
        "ตกลง", "ยืนยัน", "yes", "ok", "โอเค", "okay", "ใช่", "ใช่แล้ว",
        "ถูกต้อง", "ได้เลย", "เริ่มเลย", "ทำเลย", "จัดเลย", "ลุย"
    }


def _extract_timeline(text: str) -> str:
    m = re.search(r"(?:ภายใน|ใน|กรอบเวลา|ใช้เวลา|อยากได้ภายใน)?\s*([0-9๐-๙]+\s*(?:วัน|อาทิตย์|สัปดาห์|เดือน|ปี))", text)
    return m.group(1).strip() if m else ""


def _is_info_complete(data: dict) -> bool:
    """ตรวจสอบว่าข้อมูลครบพอที่จะขอ confirmation หรือยัง"""
    # ต้องมีอย่างน้อย: ชื่อ/บริษัท (หรืออย่างใดอย่างหนึ่ง) + needs + goals
    has_identity = bool(data.get("customer_name") or data.get("company"))
    has_needs = bool(data.get("needs"))
    has_goals = bool(data.get("goals"))
    return has_identity and has_needs and has_goals


def _extract_nb_id(context: str) -> str:
    """Extract notebook ID from conversation_context marker"""
    import re
    m = re.search(NB_MARKER_RE, context)
    return m.group(1) if m else ""


def _embed_nb_id(context: str, nb_id: str) -> str:
    """Embed notebook ID into conversation_context so it persists across requests"""
    # Remove old marker if exists, then prepend new one
    import re
    clean = re.sub(NB_MARKER_FULL_RE, "", context)
    return f"[NB:{nb_id}]\n{clean}" if nb_id else clean


def _maybe_rename_notebook(nb_id: str, notebook: dict) -> str:
    """Give temporary Sales notebooks a meaningful file name once identity is known."""
    if not nb_id or not str(nb_id).isdigit():
        return nb_id

    customer = notebook.get("customer", {}) if notebook else {}
    name = customer.get("name", "")
    company = customer.get("company", "")
    if not name and not company:
        return nb_id

    title = build_notebook_title(name=name, company=company, fallback_id=nb_id)
    desired_id = build_notebook_id(name=name, company=company, fallback_id=nb_id)
    if not desired_id or desired_id == nb_id:
        return nb_id

    try:
        final_id = rename_notebook(nb_id, desired_id, title=title)
        if final_id != nb_id:
            log.info("Sales notebook renamed: %s → %s", nb_id, final_id)
        return final_id
    except Exception as e:
        log.warning("Sales notebook rename error: %s", e)
        return nb_id


def _load_notebook_from_disk(nb_id: str) -> dict | None:
    """Try to reconstruct notebook from .md file on disk"""
    try:
        from src.tools.notebook import read_notebook
        content = read_notebook(nb_id)
        if not content:
            return None
        # Parse markdown back to notebook dict (basic extraction)
        nb = _new_notebook()
        nb["_nb_id"] = nb_id

        # Extract customer info
        import re
        name_m = re.search(r"\|\s*Name\s*\|\s*(.+?)\s*\|", content)
        if name_m and name_m.group(1).strip(): nb["customer"]["name"] = name_m.group(1).strip()
        comp_m = re.search(r"\|\s*Company\s*\|\s*(.+?)\s*\|", content)
        if comp_m and comp_m.group(1).strip(): nb["customer"]["company"] = comp_m.group(1).strip()

        # Extract business info
        for field in ("pain_points", "needs", "goals"):
            section = re.search(rf"### {field.replace('_',' ').title()}\n(.*?)(?=\n###|\n---|\Z)", content, re.DOTALL)
            if section:
                items = re.findall(r"- (.+)", section.group(1))
                nb["business"][field] = [i.strip() for i in items if i.strip()]

        timeline_m = re.search(r"### Timeline\n- (.+)", content)
        if timeline_m: nb["business"]["timeline"] = timeline_m.group(1).strip()
        summary_m = re.search(r"### Notes Summary\n(.*?)(?=\n###|\n---|\Z)", content, re.DOTALL)
        if summary_m:
            nb["conversation_summary"] = re.sub(r"\s+", " ", summary_m.group(1)).strip()

        return nb
    except Exception:
        return None
EMPTY_NOTEBOOK = {
    "customer": {"name": "", "company": "", "contact": ""},
    "business": {"pain_points": [], "needs": [], "goals": [], "timeline": "", "budget_hint": ""},
    "conversation_summary": "",
    "confidence": "low",
}


def _new_notebook() -> dict:
    """Return a fresh notebook without sharing nested lists/dicts."""
    return deepcopy(EMPTY_NOTEBOOK)


def _update_notebook(notebook: dict, collected: dict) -> dict:
    """Merge new collected data into notebook (ไม่ overwrite ของเดิม)"""
    nb = deepcopy(notebook) if notebook else _new_notebook()

    # Customer info
    cust = nb.setdefault("customer", {})
    if collected.get("customer_name") and not cust.get("name"):
        cust["name"] = collected["customer_name"]
    if collected.get("company") and not cust.get("company"):
        cust["company"] = collected["company"]

    # Business info — merge lists
    biz = nb.setdefault("business", {})
    for field in ("pain_points", "needs", "goals"):
        existing = biz.get(field, [])
        new_items = collected.get(field, [])
        if isinstance(new_items, list):
            for item in new_items:
                if item and not _has_similar_item(existing, item):
                    existing.append(item)
            biz[field] = existing
    if collected.get("timeline") and not biz.get("timeline"):
        biz["timeline"] = collected["timeline"]
    if collected.get("summary_thai"):
        nb["conversation_summary"] = collected["summary_thai"]

    return nb


def _is_notebook_ready(notebook: dict) -> bool:
    """Check if notebook has enough business info to confirm"""
    biz = notebook.get("business", {}) if notebook else {}
    cust = notebook.get("customer", {}) if notebook else {}
    has_identity = bool(cust.get("name") or cust.get("company"))
    has_needs = bool(biz.get("needs"))
    has_goals = bool(biz.get("goals"))
    return has_identity and has_needs and has_goals


def _create_handoff_brief(notebook: dict) -> dict:
    """Create clean business handoff — NO personal customer data"""
    cust = notebook.get("customer", {}) if notebook else {}
    biz = notebook.get("business", {}) if notebook else {}

    return {
        "project_name": f"{cust.get('company', cust.get('name', 'New Project'))}",
        "industry": "",
        "pain_points": biz.get("pain_points", []),
        "needs": biz.get("needs", []),
        "goals": biz.get("goals", []),
        "timeline": biz.get("timeline", ""),
        "budget_hint": biz.get("budget_hint", ""),
        "context": notebook.get("conversation_summary", ""),
        "handoff_note": "ข้อมูลนี้ถูกส่งต่อจาก Sales Agent — ใช้สำหรับเริ่มงาน business analysis เท่านั้น",
    }


def sales_node(state: AgentState) -> dict:
    """
    Sales Agent v3 — Notebook + Handoff (file-based)

    1. หยิบสมุดโน๊ตจาก state (หรือเริ่มใหม่)
    2. คุยกับลูกค้า → จดลง notebook → เขียนไฟล์ .md
    3. แยกข้อมูลส่วนตัว กับข้อมูลธุรกิจ
    4. เมื่อข้อมูลธุรกิจครบ → ขอ confirmation
    5. Confirmed → lock notebook → สร้าง handoff_brief (ธุรกิจล้วน)
    """
    user_input = state.get("input", "").strip()
    conversation = state.get("conversation_context", "")
    notebook = deepcopy(state.get("sales_notebook") or {})
    system_prompt = get_system_prompt("sales") or _default_sales_prompt()

    # Get or create notebook ID (persisted via conversation_context)
    nb_id = _extract_nb_id(state.get("conversation_context", ""))
    if not nb_id:
        import time
        nb_id = str(int(time.time() * 1000))[-8:]
        log.info("Sales notebook created: %s", nb_id)
        try:
            create_notebook(nb_id)
        except Exception as e:
            log.warning("Sales notebook create error: %s", e)
    elif not notebook:
        loaded = _load_notebook_from_disk(nb_id)
        if loaded:
            notebook = loaded

    if not notebook:
        notebook = _new_notebook()
    notebook["_nb_id"] = nb_id

    # Build full conversation
    if conversation:
        full_context = f"{conversation}\nลูกค้า: {user_input}"
    else:
        full_context = f"ลูกค้า: {user_input}"

    # Update notebook with new info
    collected = _parse_conversation(full_context)
    notebook = _update_notebook(notebook, collected)
    nb_id = _maybe_rename_notebook(nb_id, notebook)
    notebook["_nb_id"] = nb_id

    # Write to notebook file on disk
    _sync_notebook_to_disk(nb_id, notebook)
    update_notebook(nb_id, "log", f"ลูกค้า: {user_input}")

    # ── Detect confirmation ──
    confirm_keywords = ["ตกลง", "ยืนยัน", "yes", "ok", "เริ่มเลย", "ทำเลย", "ดำเนินการ",
                        "โอเค", "okay", "จัดเลย", "ลุย", "ได้เลย", "เห็นด้วย", "agree",
                        "confirm", "proceed", "go ahead", "เริ่มต้น", "พร้อม",
                        "ใช่", "ถูกต้อง", "แน่นอน", "correct", "sure", "จัดไป"]
    is_confirm = any(kw in user_input.lower() for kw in confirm_keywords)
    notebook_ready = _is_notebook_ready(notebook)

    # ═══ Confirmation → Lock notebook + Save lead + Handoff ═══
    if is_confirm and notebook_ready:
        return _handle_confirmation_v3(state, notebook, full_context, nb_id)

    # ═══ Continue conversation ═══
    try:
        nb_summary = json.dumps({
            "customer": f"{notebook['customer'].get('name','')} / {notebook['customer'].get('company','')}",
            "business": notebook["business"],
        }, ensure_ascii=False)

        # Clean context for LLM (remove internal markers)
        clean_context = re.sub(NB_MARKER_FULL_RE, "", full_context)

        reply = call_llm(
            f"## บทสนทนาที่ผ่านมา\n{clean_context}\n\n"
            f"## ข้อมูลที่เก็บได้แล้ว\n{nb_summary}\n\n"
            f"## สิ่งที่ต้องถามต่อ\n{_missing_notebook_fields(notebook)}\n\n"
            f"## คำสั่งสำคัญ\n"
            f"1. อ่านบทสนทนาข้างบนให้เข้าใจ — ลูกค้าพูดอะไรมาบ้าง?\n"
            f"2. ถ้าลูกค้าให้ข้อมูลใหม่ → รับทราบสั้นๆ (1 ประโยค) → ถามคำถามต่อไปทันที\n"
            f"3. ห้ามทักทายซ้ำ ห้ามแนะนำตัวซ้ำ — บทสนทนาดำเนินมาหลายเทิร์นแล้ว\n"
            f"4. ถามทีละ 1 คำถามเท่านั้น\n"
            f"5. ถ้าข้อมูลครบ → สรุปสิ่งที่เข้าใจ + ขอคำยืนยัน",
            system_prompt=system_prompt,
        )
        if is_llm_failure(reply):
            log.warning("Sales LLM failure response: %s", reply)
            reply = "ขออภัยครับ ระบบตอบกลับมีปัญหาชั่วคราว กรุณาลองใหม่อีกครั้งครับ"
        log.info("Sales reply: %s", reply[:100])
    except Exception as e:
        log.warning("Sales LLM error: %s", e)
        reply = "ขออภัยครับ ระบบมีปัญหาชั่วคราว กรุณาลองใหม่อีกครั้ง"

    # Log Sales reply to notebook
    update_notebook(nb_id, "log", f"Aetox: {reply[:200]}")

    ctx_with_id = _embed_nb_id(f"{full_context}\nAetox: {reply}", nb_id)
    return {
        "results": {},
        "conversation_context": ctx_with_id,
        "sales_notebook": notebook,
        "handoff_brief": {},
        "messages": [("system", f"Sales: {reply[:150]}")],
        "sales_confirmed": False,
    }


def _sync_notebook_to_disk(nb_id: str, notebook: dict):
    """Write notebook state to .md file"""
    if not nb_id:
        return
    try:
        cust = notebook.get("customer", {})
        biz = notebook.get("business", {})
        update_notebook(nb_id, "customer", {
            "name": cust.get("name", ""),
            "company": cust.get("company", ""),
            "contact": cust.get("contact", ""),
        })
        biz_with_summary = dict(biz)
        biz_with_summary["summary"] = notebook.get("conversation_summary", "")
        update_notebook(nb_id, "business", biz_with_summary)
    except Exception as e:
        log.warning("Notebook sync error: %s", e)


def _missing_notebook_fields(notebook: dict) -> str:
    """Check what's still missing in the notebook"""
    cust = notebook.get("customer", {})
    biz = notebook.get("business", {})
    missing = []
    if not cust.get("name") and not cust.get("company"):
        missing.append("- ชื่อ/บริษัท → ถาม")
    if not biz.get("pain_points"):
        missing.append("- ปัญหาที่เจอ → ถาม")
    if not biz.get("needs"):
        missing.append("- ต้องการให้ช่วยอะไร → ถาม")
    if not biz.get("goals"):
        missing.append("- เป้าหมาย → ถาม")
    if not biz.get("timeline"):
        missing.append("- กรอบเวลา → ถาม (ไม่บังคับ)")
    return "\n".join(missing) if missing else "✅ ข้อมูลธุรกิจครบ — ขอคำยืนยัน!"


def _handle_confirmation_v3(state: AgentState, notebook: dict, context: str, nb_id: str = "") -> dict:
    """Customer confirmed → lock notebook → save lead → create handoff"""
    cust = notebook.get("customer", {})
    biz = notebook.get("business", {})

    # Save lead to CRM with full data
    lead_id = None
    try:
        init_db()
        lead_id = save_lead(
            name=cust.get("name", ""),
            company=cust.get("company", ""),
            pain_points=biz.get("pain_points", []),
            needs=biz.get("needs", []),
            goals=biz.get("goals", []),
            timeline=biz.get("timeline", ""),
            summary=notebook.get("conversation_summary", ""),
            source="chat",
        )
        log.info("Sales CONFIRMED: lead #%d saved", lead_id)
    except Exception as e:
        log.warning("Sales CRM save error: %s", e)

    # Lock notebook file + add confirmation
    lock_notebook(nb_id)
    update_notebook(nb_id, "log", f"✅ ลูกค้ายืนยัน — Lead #{lead_id} — ส่งต่องาน")
    log.info("Notebook locked: %s → Lead #%s", nb_id, lead_id)

    # Create handoff brief (business only — NO personal data)
    handoff = _create_handoff_brief(notebook)

    sales_output = json.dumps({
        "agent": "sales",
        "lead_id": lead_id,
        "status": "confirmed",
        "notebook_id": nb_id,
        "notebook": f"data/notebooks/lead_{nb_id}.md",
    }, ensure_ascii=False)

    confirm_msg = (
        f"ขอบคุณที่ไว้วางใจครับ!\n"
        f"ผมได้บันทึกข้อมูลลงสมุดเรียบร้อย (Lead #{lead_id})\n"
        f"และส่งต่องานให้ทีมแล้วครับ\n"
        f"ขอบคุณที่คุยกับ Aetox ครับ หากมีรายละเอียดเพิ่มเติม แจ้งผมได้เสมอครับ"
    )

    return {
        "results": {"sales": sales_output},
        "conversation_context": _embed_nb_id(f"{context}\nAetox: {confirm_msg}", nb_id),
        "sales_notebook": notebook,
        "handoff_brief": handoff,
        "messages": [("system", f"Sales CONFIRMED: lead #{lead_id}, notebook locked, handoff ready")],
        "sales_confirmed": True,
    }


def _default_sales_prompt() -> str:
    return (
        "คุณคือ Sales Agent มืออาชีพของ Aetox Works\n"
        "บุคลิก: เป็นกันเอง อบอุ่น ฟังเยอะ ถามทีละคำถาม ไม่ยัดเยียด\n"
        "หน้าที่: เก็บข้อมูลลูกค้าให้ครบ → สรุป → ขอคำยืนยัน → ส่งต่องาน\n"
        "ห้าม: สร้าง content, เขียนเว็บ, วิเคราะห์ตลาด — คุณเป็นแค่นักขาย"
    )
