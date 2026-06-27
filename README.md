# Aetox Works — AI Enterprise Workforce

> **ระบบ AI ที่ทำงานแทนคนทุกรูปแบบ** — ตั้งแต่คุยลูกค้า ตัดต่อวิดีโอ ทำเว็บ landing page ไปจนถึงสรุปงานและบริหารทีม

## 🏗️ สถาปัตยกรรม

```
                         ┌──────────────────────┐
                         │   SUPERVISOR AGENT   │
                         │  (รับคำสั่ง → วางแผน)  │
                         └──────────┬───────────┘
                    ┌───────────────┼────────────────┐
                    ▼               ▼                ▼
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │  Sales Agent │ │   Dev Agent  │ │  Video Agent │
          │ (คุยลูกค้า)   │ │  (ทำเว็บ)    │ │  (ตัดต่อ)     │
          ├──────────────┤ ├──────────────┤ ├──────────────┤
          │ • LINE/Email │ │ • Landing    │ │ • HyperFrames│
          │ • CRM update │ │ • API        │ │ • Captions   │
          │ • Summary    │ │ • Deploy     │ │ • TTS        │
          └──────────────┘ └──────────────┘ └──────────────┘

          ┌──────────────────────────────────────────┐
          │           Admin Agent                    │
          │ (สรุปงาน, report, ประสานงาน, schedule)     │
          └──────────────────────────────────────────┘
```

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Orchestration** | LangGraph (MIT © LangChain, Inc.) |
| **Backend** | Python FastAPI |
| **Container** | Docker |
| **Video** | HyperFrames |
| **Database** | PostgreSQL / SQLite |

## 📁 โครงสร้างโปรเจค

```
aetox-works/
├── src/
│   ├── supervisor/     ← Supervisor Agent (วางแผน + ส่งต่องาน)
│   ├── agents/         ← Worker Agents (Sales, Dev, Video, Admin)
│   └── tools/          ← เครื่องมือที่ agent ใช้
├── docs/th/            ← เอกสารภาษาไทย
├── examples/           ← ตัวอย่างการใช้งาน
├── tests/              ← tests
├── requirements.txt
└── README.md
```

## 📜 License

- **Original Code:** LangGraph (MIT © LangChain, Inc.)
- **Aetox Works Extensions:** © 2026 Chayapol Promsavana
