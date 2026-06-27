# Aetox Works — AI Enterprise Workforce

> **ระบบ AI Workforce แบบ Pipeline** — ตั้งแต่เก็บโจทย์ลูกค้า → วิจัยตลาด → เขียนคอนเทนต์ → สร้างเว็บ → วัดผล

## 🏗️ Pipeline

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
┌───────────────────────────────────────────────────┐
│                   PIPELINE                        │
│                                                   │
│  Sales  →  Research  →  Content  →  Dev  →  Data  │
│  เก็บโจทย์   หาตลาด      เขียน      สร้าง     วัดผล   │
│                                                   │
└───────────────────────────────────────────────────┘
       │
       ▼
   สรุปผล + ส่งมอบ
```

| Agent | ภารกิจ | Tools |
|-------|--------|-------|
| **Sales** 🗣️ | เก็บโจทย์ลูกค้า, pain point, สรุป需求 | Web Chat, Gmail, CRM (SQLite) |
| **Research** 🔍 | หาข้อมูลตลาด, คู่แข่ง, keyword, insight | Firecrawl, Exa |
| **Content** ✍️ | เขียน copy, landing content, article | DeepSeek V4 Flash |
| **Dev** 💻 | สร้างเว็บ, feature, automation | HTML/CSS/JS, FastAPI |
| **Data** 📊 | วิเคราะห์ผลลัพธ์ lead/content/performance | SQLite, matplotlib |

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Orchestration** | LangGraph (MIT © LangChain, Inc.) |
| **LLM** | DeepSeek V4 Flash (OpenAI-compatible API) |
| **Backend** | Python FastAPI |
| **Database** | SQLite → PostgreSQL |
| **Search** | Firecrawl + Exa |
| **Container** | Docker |

## 📁 โครงสร้างโปรเจค

```
aetox-works/
├── src/
│   ├── supervisor/         ← LangGraph graph + router
│   │   └── workflow.py     ← StateGraph, nodes, conditional edges
│   ├── agents/             ← Worker Agents (implementations)
│   │   ├── sales_agent.py
│   │   ├── research_agent.py
│   │   ├── content_agent.py
│   │   ├── dev_agent.py
│   │   └── data_agent.py
│   ├── config/
│   │   ├── __init__.py     ← .env loader + env vars
│   │   └── agent_configs/  ← YAML prompts per agent
│   │       ├── sales.yaml
│   │       ├── research.yaml
│   │       ├── content.yaml
│   │       ├── dev.yaml
│   │       └── data.yaml
│   ├── llm/
│   │   └── client.py       ← call_llm() → DeepSeek API
│   └── tools/              ← Shared tools (TBD)
├── docs/th/                ← เอกสารภาษาไทย
├── tests/
│   ├── test_supervisor.py  ← Graph, router (7 tests)
│   └── test_agent_configs.py ← Prompts loader (8 tests)
├── ROADMAP.md              ← แผนพัฒนา 8 phases
├── requirements.txt
└── README.md
```

## 📜 License

- **LangGraph:** MIT © LangChain, Inc.
- **Aetox Works Extensions:** © 2026 Chayapol Promsavana
