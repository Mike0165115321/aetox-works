# 🗺️ Aetox Works — แผนพัฒนา (Roadmap)

> ระบบ AI Enterprise Workforce — LangGraph Supervisor-Worker

---

## Phase 0: Foundation ✅ (เสร็จแล้ว)

| Task | Status |
|:-----|:------:|
| สร้างโครงสร้างโปรเจค | ✅ |
| LangGraph v1.2.6 dependencies | ✅ |
| .venv (Python 3.13.3) | ✅ |
| Supervisor-Worker Graph scaffold | ✅ |
| 5 Agent templates (Sales, Research, Content, Dev, Data) | ✅ |
| Docs ภาษาไทยใน `docs/th/` | ✅ |
| GitHub: `Mike0165115321/aetox-works` | ✅ |

---

## Phase 1: Core — LLM Integration & Router จริง ✅

> **เป้าหมาย:** ทำให้ Supervisor ใช้ LLM วิเคราะห์คำสั่งและเลือก agent ได้จริง

- [x] **1.1** สร้าง `.env` + `config.py` — ใส่ API key (DeepSeek V4 Flash)
- [x] **1.2** สร้าง LLM client module — เรียก LLM ได้
- [x] **1.3** ทำให้ `router()` ใช้ LLM จริง — วิเคราะห์ intent แล้วเลือก agent
- [x] **1.4** เพิ่ม `src/config/agent_configs/` — เก็บ prompt แต่ละ agent (5 ตัว)
- [x] **1.5** เพิ่ม logging / tracing — รู้ว่า agent แต่ละตัวทำอะไร
- [x] **1.6** Tests — router, config, llm client (7 ผ่าน)

---

## Phase 2: Agent ที่ 1 — Sales Agent (คุยลูกค้า 🗣️) ✅

> **Pipeline step 1:** เก็บโจทย์ลูกค้า, pain point, สรุป需求 → ส่ง Research
> **เป้าหมาย:** Agent ที่คุยกับลูกค้าผ่าน Web Chat สรุปความต้องการ ส่งต่องาน

- [x] **2.1** Sales Agent prompt — personality + workflow
- [x] **2.2** Web Chat UI — ตอบลูกค้าผ่านเว็บ
- [x] ~~**2.3** เชื่อมต่อ Gmail (ผ่าน Gmail MCP)~~ — ตัดออกเพื่อลดความซับซ้อน
- [x] **2.4** CRM module — บันทึกประวัติลูกค้า (SQLite)
- [x] **2.5** Summary generator — สรุปบทสนทนาเป็น structured data → ส่ง Research
- [x] **2.6** Tests (12 tests)

---

## Phase 3: Agent ที่ 2 — Research Agent (ค้นหา 🔍) ✅

> **Pipeline step 2:** หาข้อมูลตลาด, คู่แข่ง, keyword, insight → ส่ง Content
> **เป้าหมาย:** Agent ที่รับ需求จาก Sales → ค้นหาข้อมูลตลาด คู่แข่ง และ insight

- [x] **3.1** Research Agent prompt
- [x] **3.2** Firecrawl integration (search + scrape)
- [x] **3.3** Exa integration (semantic search)
- [x] **3.4** รายงาน structured data — สรุป insights → ส่ง Content Agent
- [x] **3.5** Tests (9 tests)

---

## Phase 4: Agent ที่ 3 — Content Agent (เขียนคอนเทนต์ ✍️) ✅

> **Pipeline step 3:** เขียน copy, landing content, article → ส่ง Dev
> **เป้าหมาย:** Agent ที่รับข้อมูลจาก Research → เขียน content ทุกประเภท

- [x] **4.1** Content Agent prompt
- [x] **4.2** Landing page copy generator
- [x] **4.3** Blog/article generator
- [x] **4.4** Social media / Email copy generator
- [x] **4.5** ส่ง content → Dev Agent
- [x] Tests (10 tests)

---

## Phase 5: Agent ที่ 4 — Dev Agent (สร้างเว็บ 💻) ✅

> **Pipeline step 4:** สร้างเว็บ, feature, automation → ส่ง Data
> **เป้าหมาย:** Agent ที่รับ content → สร้างหน้าเว็บ / feature / automation

- [x] **5.1** Dev Agent prompt
- [x] **5.2** HTML/CSS/JS generator — สร้างหน้าเว็บจาก requirement
- [x] **5.3** Local preview server
- [x] ~~**5.4** Deploy module~~ — Phase 7
- [x] ~~**5.5** Human-in-the-loop~~ — Phase 7
- [x] **5.6** Tests (5 tests)

---

## Phase 6: Agent ที่ 5 — Data Agent (วัดผล 📊) ✅

> **Pipeline step 5:** วิเคราะห์ผลลัพธ์ lead/content/performance → สรุปส่งลูกค้า
> **เป้าหมาย:** Agent ที่รวบรวมผลลัพธ์จากทุก agent วิเคราะห์และสรุป

- [x] **6.1** Data Agent prompt
- [x] **6.2** รองรับ CSV / JSON / logs
- [x] ~~**6.3** สร้างกราฟ + report (matplotlib)~~ — ใช้ LLM summary แทน
- [x] ~~**6.4** Dashboard พื้นฐาน~~ — Phase 7
- [x] **6.5** สรุปผล → ส่งกลับลูกค้า
- [x] **6.6** Tests (6 tests)

---

## ⚡ Pipeline Mode — Sequential Execution ✅

- [x] `build_pipeline_graph()` — Sales → Research → Content → Dev → Data → Final
- [x] `build_router_graph()` — Single-agent routing (เดิม)
- [x] `build_supervisor_graph(mode="pipeline")` — default = pipeline
- [x] `pipeline_next_agent()` — auto-advance ตามลำดับ

---

## Phase 7: Production — FastAPI Server & Deployment

> **เป้าหมาย:** ระบบพร้อมใช้งานจริง มี API, monitoring, auto-scaling

- [ ] **6.1** FastAPI server — endpoints สำหรับรับคำสั่ง
- [ ] **6.2** Authentication — ใครเรียกใช้ระบบได้บ้าง
- [ ] **6.3** LangSmith monitoring — ดู logs ทุก step
- [ ] **6.4** Human-in-the-loop approval system
- [ ] **6.5** Dockerize — Dockerfile + docker-compose
- [ ] **6.6** Deploy — ขึ้น server จริง (VPS / Cloud)

---

## Phase 8: ขยายระบบ

> **เป้าหมาย:** เพิ่มความสามารถใหม่ๆ ไม่จำกัด

- [ ] **7.1** Multi-language support (อังกฤษ, จีน)
- [ ] **7.2** เพิ่ม Agent ใหม่ — Finance, HR, Support ฯลฯ
- [ ] **7.3** File upload / management system
- [ ] **7.4** Knowledge base integration (RAG)
- [ ] **7.5** Performance optimization

---

## สถาปัตยกรรมปัจจุบัน

```
ลูกค้า / User
    │
    ▼
┌─────────────────────────────┐
│      SUPERVISOR AGENT       │
│  รับ → วิเคราะห์ → วางแผน   │
│  (LLM Router → DeepSeek)    │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│              PIPELINE                    │
│                                         │
│  Sales  →  Research  →  Content  →  Dev  →  Data  │
│  เก็บโจทย์   หาตลาด      เขียน      สร้าง     วัดผล   │
│                                         │
└─────────────────────────────────────────┘
       │
       ▼
   สรุปผล + ส่งมอบ
```

> **หมายเหตุ:** Pipeline ต้องทำตามลำดับ (Sales → Research → Content → Dev → Data)
