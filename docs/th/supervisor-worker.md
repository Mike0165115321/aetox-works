# Supervisor-Worker Pattern (Pipeline)

Aetox Works ใช้รูปแบบ **Pipeline Supervisor-Worker** — Supervisor รับคำสั่ง ส่งต่อ pipeline 5 ขั้นตอน

## Flow

```
User: "ช่วยทำ landing page สำหรับร้านกาแฟ"

       │
       ▼
┌──────────────────────┐
│   SUPERVISOR AGENT   │  วิเคราะห์ → วางแผน → ส่งเข้าสู่ pipeline
│   (LLM Router)       │  "เริ่มที่ Sales ก่อน"
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│                      PIPELINE                        │
│                                                      │
│  Step 1 ───►  Sales Agent                           │
│             เก็บโจทย์: "ร้านกาแฟ急需 offline →
│             online อยากได้ website"                  │
│                    │                                 │
│                    ▼                                 │
│  Step 2 ───►  Research Agent                        │
│             หาตลาด: แนวโน้มร้านกาแฟ, คู่แข่งในพื้นที่ │
│                    │                                 │
│                    ▼                                 │
│  Step 3 ───►  Content Agent                         │
│             เขียน copy: headline, menu, story        │
│                    │                                 │
│                    ▼                                 │
│  Step 4 ───►  Dev Agent                             │
│             สร้างหน้าเว็บ: HTML/CSS/JS → deploy      │
│                    │                                 │
│                    ▼                                 │
│  Step 5 ───►  Data Agent                            │
│             วัดผล: วิเคราะห์ content, performance     │
│                                                      │
└──────────────────────────────────────────────────────┘
           │
           ▼
   สรุปผล + URL: "เสร็จแล้วครับ ดูได้ที่..."
   ส่งกลับลูกค้า
```

## โค้ดตัวอย่าง

```python
from src.supervisor.workflow import build_supervisor_graph

graph = build_supervisor_graph()
result = graph.invoke({
    "input": "ช่วยทำ landing page ร้านกาแฟ",
    "plan": "",
    "current_agent": "",
    "messages": [],
    "results": {},
    "final_output": "",
    "error": None,
})
print(result["final_output"])
```

## การทำงานของ Supervisor

1. **Router** (`router_llm`) — ใช้ DeepSeek V4 Flash วิเคราะห์ intent
2. **Agent** ทำงานตาม pipeline — แต่ละตัวมี system prompt จาก `src/config/agent_configs/`
3. **Final Aggregator** — รวมผลลัพธ์ทั้งหมดส่งกลับ

## ข้อควรรู้

- Pipeline ต้องทำตามลำดับ (Sales → Research → Content → Dev → Data)
- แต่ละ agent รับ input จาก agent ก่อนหน้า
- Agent configs เก็บที่ `src/config/agent_configs/*.yaml`
