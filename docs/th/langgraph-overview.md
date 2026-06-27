# ภาพรวม LangGraph

LangGraph คือ **Graph-Based Agent Orchestration Framework** พัฒนาโดย LangChain Inc.

## Three-Layer Design

```
┌──────────────────────────────────┐
│  Layer 1: Graph Module           │
│  StateGraph, MessageGraph        │
│  → สร้าง graph workflow           │
├──────────────────────────────────┤
│  Layer 2: Pregel Runtime         │
│  execute nodes, ส่ง messages      │
│  → รัน graph                      │
├──────────────────────────────────┤
│  Layer 3: Channels               │
│  การสื่อสารระหว่าง nodes           │
│  → shared state                  │
└──────────────────────────────────┘
```

## Key Concepts

| Concept | คำอธิบาย |
|---------|----------|
| **StateGraph** | Graph ที่มี shared state — node อ่าน/เขียน state ได้ |
| **Node** | ตัว agent หรือ function ที่ทำงาน |
| **Edge** | เส้นเชื่อม — กำหนด flow การทำงาน |
| **Conditional Edge** | ถ้า condition X → ไป node Y, ถ้า Z → ไป node W |
| **Checkpoint** | บันทึก state เพื่อ resume ได้ถ้า crash |
| **Streaming** | ดูผลลัพธ์แบบ real-time ขณะ graph ทำงาน |

## แหล่งอ้างอิง

- Official Docs: https://docs.langchain.com/oss/python/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- ต้นฉบับ LangGraph (MIT © LangChain, Inc.)
