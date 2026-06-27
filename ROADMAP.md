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
| 4 Agent templates (Sales, Dev, Video, Admin) | ✅ |
| Docs ภาษาไทยใน `docs/th/` | ✅ |
| GitHub: `Mike0165115321/aetox-works` | ✅ |

---

## Phase 1: Core — LLM Integration ✅ (เสร็จ)

| Task | Status |
|:-----|:------:|
| `.env` + `config.py` | ✅ |
| LLM client module (DeepSeek) | ✅ |
| LLM Router — classify intent เลือก agent | ✅ |
| Logging | ✅ |
| Tests (6 ผ่าน) | ✅ |

---

## Phase 2: Sales Agent (MVP) — Web Chat + Email

> **เป้าหมาย:** AI ตอบคำถามลูกค้าผ่านหน้าเว็บ สรุปความต้องการ ส่งอีเมล

- [ ] **2.1** Web chat UI (HTML/CSS/JS ติด直接在หน้าเว็บ)
- [ ] **2.2** Sales Agent prompt — personality + workflow
- [ ] **2.3** เชื่อมต่อ Gmail — ส่งอีเมลสรุปให้ลูกค้า (ใช้ Gmail MCP)
- [ ] **2.4** CRM พื้นฐาน — บันทึกประวัติลูกค้า (SQLite)
- [ ] **2.5** Tests

---

## Phase 3: Dev Agent (ทำเว็บ)

> **เป้าหมาย:** Agent ที่รับ requirement → สร้าง landing page → deploy

- [ ] **3.1** Dev Agent prompt
- [ ] **3.2** HTML/CSS/JS generator — สร้างหน้าเว็บจาก requirement
- [ ] **3.3** Local preview server
- [ ] **3.4** Deploy module — ขึ้น GitHub Pages หรือ server จริง
- [ ] **3.5** Human-in-the-loop — ให้คน approve ก่อน deploy
- [ ] **3.6** Tests

---

## Phase 4: Data Agent (วิเคราะห์ข้อมูล)

> **เป้าหมาย:** Agent ที่รับข้อมูล สร้างกราฟ รายงาน visuals

- [ ] **4.1** Data Agent prompt
- [ ] **4.2** รองรับ data formats (CSV, JSON, Excel)
- [ ] **4.3** สร้างกราฟ (matplotlib / plotly)
- [ ] **4.4** Report generator — สรุปเป็น HTML/Markdown
- [ ] **4.5** Dashboard พื้นฐาน
- [ ] **4.6** Tests

---

## Phase 6: Production — FastAPI Server & Deployment

> **เป้าหมาย:** ระบบพร้อมใช้งานจริง มี API, monitoring, auto-scaling

- [ ] **6.1** FastAPI server — endpoints สำหรับรับคำสั่ง
- [ ] **6.2** Authentication — ใครเรียกใช้ระบบได้บ้าง
- [ ] **6.3** LangSmith monitoring — ดู logs ทุก step
- [ ] **6.4** Human-in-the-loop approval system
- [ ] **6.5** Dockerize — Dockerfile + docker-compose
- [ ] **6.6** Deploy — ขึ้น server จริง (VPS / Cloud)

---

## Phase 7: ขยายระบบ

> **เป้าหมาย:** เพิ่มความสามารถใหม่ๆ ไม่จำกัด

- [ ] **7.1** Multi-language support (อังกฤษ, จีน)
- [ ] **7.2** เพิ่ม Agent ใหม่ — Finance, HR, Support ฯลฯ
- [ ] **7.3** File upload / management system
- [ ] **7.4** Knowledge base integration (RAG)
- [ ] **7.5** Performance optimization

---

## สถาปัตยกรรมปัจจุบัน

```
User Request
    │
    ▼
┌─────────────────────────────┐
│      SUPERVISOR AGENT       │
│  รับ → วิเคราะห์ → วางแผน   │
│  (LLM Router)               │
└──────┬──────┬──────┬───────┘
       │      │      │
       ▼      ▼      ▼
   Sales    Dev    Video   Admin
   Agent    Agent  Agent   Agent
       │      │      │       │
       └──────┴──────┴───────┘
               │
               ▼
        สรุปผล → ส่งกลับผู้ใช้
```

> **หมายเหตุ:** Phase 1-5 ทำพร้อมกันหรือสลับลำดับได้ตามความเหมาะสม
