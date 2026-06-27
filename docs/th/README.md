# Aetox Works — เอกสารภาษาไทย

> ระบบ AI Enterprise Workforce Pipeline ด้วย LangGraph

## สารบัญ

1. [ภาพรวม LangGraph](langgraph-overview.md) — สถาปัตยกรรม Three-Layer Design
2. [Supervisor-Worker Pattern](supervisor-worker.md) — แนวคิด Pipeline ส่งต่องาน

## Pipeline

```
Sales  →  Research  →  Content  →  Dev  →  Data
```

| Agent | ไฟล์ |
|-------|------|
| Sales | `src/agents/sales_agent.py` |
| Research | `src/agents/research_agent.py` |
| Content | `src/agents/content_agent.py` |
| Dev | `src/agents/dev_agent.py` |
| Data | `src/agents/data_agent.py` |

## เริ่มต้นพัฒนา

```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน tests
pytest tests/ -v
```
