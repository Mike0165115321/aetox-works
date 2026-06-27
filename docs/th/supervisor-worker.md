# Supervisor-Worker Pattern

รูปแบบการออกแบบที่ Supervisor Agent วางแผน → ส่งต่องานให้ Worker Agents

## Flow

```
User: "สร้าง landing page"
       │
       ▼
┌──────────────────┐
│   SUPERVISOR     │  วิเคราะห์ → วางแผน
│   (LLM)          │  "ต้องสร้างเว็บ 1 หน้า"
└────────┬─────────┘
         │ ส่งต่อ
         ▼
┌──────────────────┐
│   DEV AGENT      │  สร้าง HTML, CSS, JS
│                  │  ทดสอบ, deploy
└──────────────────┘
         │
         ▼
┌──────────────────┐
│   SUPERVISOR     │  ตรวจสอบ → สรุป
│                  │  "เสร็จแล้ว URL: ..."
└──────────────────┘
         │
         ▼
       User
```

## วิธีใช้ใน LangGraph

```python
from langgraph.graph import StateGraph

# 1. สร้าง State
class State(TypedDict):
    input: str
    result: str

# 2. สร้าง graph
graph = StateGraph(State)

# 3. เพิ่ม nodes
graph.add_node("supervisor", supervisor_fn)
graph.add_node("dev_agent", dev_fn)

# 4. Conditional edge — supervisor เลือก agent
graph.add_conditional_edges(
    "supervisor",
    router_fn,       # LLM ตัดสินใจ
    {"dev": "dev_agent", "sales": "sales_agent"}
)

# 5. compile
app = graph.compile()
```
