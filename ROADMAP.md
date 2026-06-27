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

## Phase 1: Core — LLM Integration & Router จริง

> **เป้าหมาย:** ทำให้ Supervisor ใช้ LLM วิเคราะห์คำสั่งและเลือก agent ได้จริง

- [ ] **1.1** สร้าง `.env` + `config.py` — ใส่ API key (OpenAI / อื่นๆ)
- [ ] **1.2** สร้าง LLM client module — เรียก LLM ได้
- [ ] **1.3** ทำให้ `router()` ใช้ LLM จริง — วิเคราะห์ intent แล้วเลือก agent
- [ ] **1.4** เพิ่ม `src/config/agent_configs/` — เก็บ prompt แต่ละ agent
- [ ] **1.5** เพิ่ม logging / tracing — รู้ว่า agent แต่ละตัวทำอะไร
- [ ] **1.6** Tests — router, config, llm client

---

## Phase 2: Agent ที่ 1 — Sales Agent (คุยลูกค้า)

> **เป้าหมาย:** Agent ที่คุยกับลูกค้าผ่าน LINE/Email สรุปความต้องการ ส่งต่องาน

- [ ] **2.1** Sales Agent prompt — personality + workflow
- [ ] **2.2** เชื่อมต่อ LINE Messaging API
- [ ] **2.3** เชื่อมต่อ Gmail (ผ่าน Gmail MCP)
- [ ] **2.4** CRM module — บันทึกประวัติลูกค้า (SQLite → PostgreSQL)
- [ ] **2.5** Summary generator — สรุปบทสนทนาเป็น structured data
- [ ] **2.6** Tests

---

## Phase 3: Agent ที่ 2 — Dev Agent (ทำเว็บ)

> **เป้าหมาย:** Agent ที่รับ requirement → สร้าง landing page → deploy

- [ ] **3.1** Dev Agent prompt
- [ ] **3.2** HTML/CSS/JS generator — สร้างหน้าเว็บจาก requirement
- [ ] **3.3** Local preview server
- [ ] **3.4** Deploy module — ขึ้น GitHub Pages หรือ server จริง
- [ ] **3.5** Human-in-the-loop — ให้คน approve ก่อน deploy
- [ ] **3.6** Tests

---

## Phase 4: Agent ที่ 3 — Video Agent (ตัดต่อวิดีโอ)

> **เป้าหมาย:** Agent ที่รับสคริปต์ → สร้างวิดีโอด้วย HyperFrames → TTS → Captions

- [ ] **4.1** Video Agent prompt
- [ ] **4.2** Integrate HyperFrames — สร้าง composition จาก prompt
- [ ] **4.3** TTS integration (Kokoro / ElevenLabs)
- [ ] **4.4** Caption/subtitle generator
- [ ] **4.5** Render pipeline — วิดีโอสำเร็จรูป
- [ ] **4.6** Tests

---

## Phase 5: Agent ที่ 4 — Admin Agent (สรุปงาน)

> **เป้าหมาย:** Agent ที่สรุปงาน ทำรายงาน จัดการ schedule

- [ ] **5.1** Admin Agent prompt
- [ ] **5.2** Report generator — สรุปงานประจำวัน/สัปดาห์
- [ ] **5.3** Schedule manager — จัดลำดับความสำคัญ
- [ ] **5.4** Dashboard API — ดูสถานะงานทั้งหมด
- [ ] **5.5** Tests

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
