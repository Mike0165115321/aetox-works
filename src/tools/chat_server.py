"""
Aetox Works — Web Chat Server (Sales Agent 🗣️)

FastAPI server สำหรับ Web Chat
รับข้อความจากลูกค้า → ส่งเข้า LangGraph → ตอบกลับ
"""
import os
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from src.supervisor.workflow import build_supervisor_graph
from src.tools.crm import save_lead, init_db

log = logging.getLogger("aetox.chat")

# HTML Chat UI (inline เพื่อความสะดวก ไม่ต้องพึ่ง static files)
_CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox — Sales Chat</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, 'Noto Sans Thai', sans-serif;
         background: #f5f5f7; display: flex; justify-content: center;
         align-items: center; min-height: 100vh; }
  .chat-box { width: 420px; max-width: 96vw; height: 90vh;
              background: white; border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
              display: flex; flex-direction: column; overflow: hidden; }
  .header { padding: 20px 24px; background: #1a1a2e; color: white; }
  .header h1 { font-size: 18px; font-weight: 600; }
  .header p { font-size: 13px; opacity: 0.7; margin-top: 2px; }
  .messages { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex;
              flex-direction: column; gap: 10px; }
  .msg { max-width: 80%; padding: 10px 16px; border-radius: 16px;
         font-size: 14px; line-height: 1.5; white-space: pre-wrap; }
  .msg.user { align-self: flex-end; background: #1a1a2e; color: white;
              border-bottom-right-radius: 4px; }
  .msg.bot { align-self: flex-start; background: #f0f0f5; color: #1a1a2e;
             border-bottom-left-radius: 4px; }
  .input-area { display: flex; gap: 8px; padding: 12px 20px 20px;
                border-top: 1px solid #eee; }
  input { flex: 1; padding: 12px 16px; border: 1px solid #ddd; border-radius: 12px;
          font-size: 14px; outline: none; }
  input:focus { border-color: #1a1a2e; }
  button { padding: 12px 20px; background: #1a1a2e; color: white; border: none;
           border-radius: 12px; font-size: 14px; cursor: pointer; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .typing { align-self: flex-start; background: #f0f0f5; padding: 12px 20px;
            border-radius: 16px; border-bottom-left-radius: 4px; font-size: 14px; }
  .typing::after { content: '...'; animation: dots 1.5s steps(4) infinite; }
  @keyframes dots { 0% { content: ''; } 25% { content: '.'; } 50% { content: '..'; } 75% { content: '...'; } }
</style>
</head>
<body>
<div class="chat-box">
  <div class="header">
    <h1>🤖 Aetox Sales</h1>
    <p>บอกเราว่าคุณต้องการอะไร</p>
  </div>
  <div class="messages" id="messages">
    <div class="msg bot">สวัสดีครับ! 👋 ยินดีที่ได้รู้จัก\n\nผมคือ Sales Agent ของ Aetox\n\nคุณมีโปรเจกต์อะไร หรือต้องการให้ช่วยอะไรครับ?</div>
  </div>
  <div class="input-area">
    <input type="text" id="input" placeholder="พิมพ์ข้อความ..." autofocus>
    <button id="sendBtn" onclick="send()">ส่ง</button>
  </div>
</div>
<script>
const messages = document.getElementById('messages');
const input = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
let conversation = [];

function addMsg(text, role) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  conversation.push({ role, text });
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'typing';
  div.id = 'typing';
  div.textContent = 'กำลังพิมพ์';
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

async function send() {
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg(text, 'user');
  sendBtn.disabled = true;
  showTyping();
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: conversation.slice(0, -1)
      })
    });
    const data = await res.json();
    hideTyping();
    addMsg(data.reply, 'bot');
    if (data.lead_id) {
      addMsg('✅ บันทึก lead id: ' + data.lead_id, 'bot');
    }
  } catch(e) {
    hideTyping();
    addMsg('ขออภัย ระบบมีปัญหา กรุณาลองใหม่ครับ', 'bot');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
</script>
</body>
</html>"""


def create_app() -> FastAPI:
    """สร้าง FastAPI app สำหรับ Web Chat"""
    app = FastAPI(title="Aetox Sales Chat", version="1.0.0")

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return _CHAT_HTML

    @app.post("/chat")
    async def chat(req: Request):
        body = await req.json()
        message = body.get("message", "")
        history = body.get("history", [])

        # สร้าง context จากประวัติ
        context = "\n".join(
            f"{'ลูกค้า' if m['role'] == 'user' else 'Aetox'}: {m['text']}"
            for m in history[-6:]  # จำแค่ 6 ข้อความล่าสุด
        )

        # เรียก LangGraph — router mode (quick chat)
        graph = build_supervisor_graph(mode="router")
        result = graph.invoke({
            "input": f"{context}\nลูกค้า: {message}" if context else message,
            "plan": "",
            "current_agent": "",
            "messages": [],
            "results": {},
            "final_output": "",
            "error": None,
        })

        reply = result.get("final_output", "")
        # ตัด prefix "## Summary" ออกถ้ามี
        reply = reply.replace("## Summary\n\n", "").strip()

        # บันทึก lead ถ้าพบข้อมูล
        lead_id = None
        try:
            # ถ้า response มี keywords → บันทึก lead
            if any(kw in reply for kw in ["ต้องการ", "ปัญหา", "ช่วย", "โปรเจก", "ทำเว็บ"]):
                lead_id = save_lead(summary=reply[:500], name="(จากแชท)")
        except Exception:
            pass

        return JSONResponse({"reply": reply, "lead_id": lead_id})

    return app


def run_chat_server(host: str = "127.0.0.1", port: int = 8080):
    """รัน Web Chat Server"""
    log.info("Starting Sales Chat at http://%s:%d", host, port)
    init_db()
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")
