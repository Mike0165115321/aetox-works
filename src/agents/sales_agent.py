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

from src.supervisor import AgentState
from src.config.agent_configs import get_system_prompt, get_output_format
from src.llm.client import call_llm
from src.tools.crm import init_db, save_lead, update_lead_status
from src.tools.notebook import create_notebook, update_notebook, lock_notebook

log = logging.getLogger("aetox.agents.sales")

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
    data = dict(SALES_JSON_SCHEMA)

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

    return data


def _is_info_complete(data: dict) -> bool:
    """ตรวจสอบว่าข้อมูลครบพอที่จะขอ confirmation หรือยัง"""
    # ต้องมีอย่างน้อย: ชื่อ/บริษัท (หรืออย่างใดอย่างหนึ่ง) + needs + goals
    has_identity = bool(data.get("customer_name") or data.get("company"))
    has_needs = bool(data.get("needs"))
    has_goals = bool(data.get("goals"))
    return has_identity and has_needs and has_goals


# Notebook template
EMPTY_NOTEBOOK = {
    "customer": {"name": "", "company": "", "contact": ""},
    "business": {"pain_points": [], "needs": [], "goals": [], "timeline": "", "budget_hint": ""},
    "conversation_summary": "",
    "confidence": "low",
}


def _update_notebook(notebook: dict, collected: dict) -> dict:
    """Merge new collected data into notebook (ไม่ overwrite ของเดิม)"""
    nb = dict(notebook) if notebook else dict(EMPTY_NOTEBOOK)

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
                if item not in existing and item:
                    existing.append(item)
            biz[field] = existing
    if collected.get("timeline") and not biz.get("timeline"):
        biz["timeline"] = collected["timeline"]

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
    notebook = state.get("sales_notebook") or dict(EMPTY_NOTEBOOK)
    system_prompt = get_system_prompt("sales") or _default_sales_prompt()

    # Get or create notebook ID (temp until confirmed)
    nb_id = notebook.get("_nb_id")
    if not nb_id:
        import time
        nb_id = str(int(time.time() * 1000))[-8:]  # short timestamp-based ID
        notebook["_nb_id"] = nb_id
        try:
            create_notebook(nb_id)
            log.info("Sales notebook created: %s", nb_id)
        except Exception as e:
            log.warning("Sales notebook create error: %s", e)

    # Build full conversation
    if conversation:
        full_context = f"{conversation}\nลูกค้า: {user_input}"
    else:
        full_context = f"ลูกค้า: {user_input}"

    # Update notebook with new info
    collected = _parse_conversation(full_context)
    notebook = _update_notebook(notebook, collected)

    # Write to notebook file on disk
    _sync_notebook_to_disk(nb_id, notebook)
    update_notebook(nb_id, "log", f"ลูกค้า: {user_input}")

    # ── Detect confirmation ──
    confirm_keywords = ["ตกลง", "ยืนยัน", "yes", "ok", "เริ่มเลย", "ทำเลย", "ดำเนินการ",
                        "โอเค", "okay", "จัดเลย", "ลุย", "ได้เลย", "เห็นด้วย", "agree",
                        "confirm", "proceed", "go ahead", "เริ่มต้น", "พร้อม"]
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

        reply = call_llm(
            f"## บทสนทนา\n{full_context}\n\n"
            f"## สมุดโน๊ต (ข้อมูลที่เก็บได้แล้ว)\n{nb_summary}\n\n"
            f"## ข้อมูลที่ยังขาด\n{_missing_notebook_fields(notebook)}\n\n"
            f"## คำสั่ง\n"
            f"คุณคือนักขายมืออาชีพของ Aetox Works คุยกับลูกค้าด้วยน้ำเสียงเป็นกันเอง "
            f"ถามทีละคำถาม อย่ายัดทุกคำถามในรอบเดียว "
            f"ถ้าข้อมูลธุรกิจครบ → สรุปทั้งหมด ถามลูกค้าว่ายืนยันดำเนินการต่อไหม",
            system_prompt=system_prompt,
        )
        log.info("Sales reply: %s", reply[:100])
    except Exception as e:
        log.warning("Sales LLM error: %s", e)
        reply = "ขออภัยครับ ระบบมีปัญหาชั่วคราว กรุณาลองใหม่อีกครั้ง"

    # Log Sales reply to notebook
    update_notebook(nb_id, "log", f"Aetox: {reply[:200]}")

    return {
        "results": {},
        "conversation_context": f"{full_context}\nAetox: {reply}",
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
        update_notebook(nb_id, "business", biz)
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
    log.info("Notebook locked: %s → Lead #%d", nb_id, lead_id)

    # Create handoff brief (business only — NO personal data)
    handoff = _create_handoff_brief(notebook)

    sales_output = json.dumps({
        "agent": "sales",
        "lead_id": lead_id,
        "status": "confirmed",
        "notebook": f"data/notebooks/lead_{lead_id}.md",
    }, ensure_ascii=False)

    confirm_msg = (
        f"ขอบคุณที่ไว้วางใจครับ!\n"
        f"ผมได้บันทึกข้อมูลลงสมุดเรียบร้อย (Lead #{lead_id})\n"
        f"และส่งต่องานให้ทีมแล้วครับ..."
    )

    return {
        "results": {"sales": sales_output},
        "conversation_context": f"{context}\nAetox: {confirm_msg}",
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
