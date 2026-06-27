# ตัวอย่างการใช้งาน Supervisor Graph

```python
# 1. เรียก supervisor
import asyncio
from src.supervisor.workflow import build_supervisor_graph

graph = build_supervisor_graph()

# 2. ส่งคำสั่ง
result = graph.invoke({
    "input": "สร้าง landing page สำหรับโปรโมทสินค้าใหม่",
    "plan": "",
    "current_agent": "",
    "messages": [],
    "results": {},
    "final_output": "",
    "error": None,
})

# 3. ดูผลลัพธ์
print(result["final_output"])
```

## ตัวอย่าง FastAPI Server

```python
from fastapi import FastAPI
from src.supervisor.workflow import build_supervisor_graph

app = FastAPI()
graph = build_supervisor_graph()

@app.post("/run")
async def run_task(input: str):
    result = graph.invoke({"input": input, ...})
    return {"output": result["final_output"]}
```
