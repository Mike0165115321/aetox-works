"""
Aetox Works — Chat UI (MVP Showcase)
Full multi-agent pipeline demo: Sales → Research → Content → Dev → Data
"""
CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Works — AI Chat</title>
<style>
:root {
  --bg: #0b0f1a; --surface: #131827; --card: #1a1f33;
  --ink: #e8ecf4; --muted: #6b7394; --border: #252b42;
  --accent: #e94560; --accent2: #6366f1; --green: #10b981;
  --sales: #f59e0b; --research: #6366f1; --content: #8b5cf6;
  --dev: #e94560; --data: #10b981;
  --radius: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Noto Sans Thai', 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--ink); height: 100vh;
       display: flex; flex-direction: column; overflow: hidden; }

/* Header */
.header { background: var(--surface); border-bottom: 1px solid var(--border);
          padding: 0 24px; height: 56px; display: flex; align-items: center;
          justify-content: space-between; flex-shrink: 0; }
.header h1 { font-size: 1em; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.header .logo-dot { width: 10px; height: 10px; border-radius: 50%;
                    background: var(--accent); box-shadow: 0 0 12px var(--accent); }
.header nav { display: flex; gap: 6px; }
.header nav a { color: var(--muted); text-decoration: none; font-size: 0.85em;
                padding: 6px 14px; border-radius: 6px; transition: all 0.2s; }
.header nav a:hover { color: var(--ink); background: var(--card); }
.header nav a.active { color: var(--accent); background: rgba(233,69,96,0.1); }

/* Chat Area */
.chat-area { flex: 1; overflow-y: auto; padding: 20px 24px;
             display: flex; flex-direction: column; gap: 16px; }

/* Messages */
.msg { max-width: 80%; animation: msgIn 0.3s ease-out; }
.msg.user { align-self: flex-end; }
.msg.user .bubble { background: var(--accent); color: #fff; border-radius: 18px 18px 4px 18px;
                    padding: 12px 18px; font-size: 0.95em; line-height: 1.5; }
.msg.bot { align-self: flex-start; }
.msg.bot .bubble { background: var(--card); border: 1px solid var(--border);
                   border-radius: 18px 18px 18px 4px;
                   padding: 12px 18px; font-size: 0.95em; line-height: 1.6; }

/* Pipeline Result Card */
.pipeline-result { align-self: flex-start; width: 100%; max-width: 700px;
                   background: var(--card); border: 1px solid var(--border);
                   border-radius: var(--radius); overflow: hidden;
                   animation: msgIn 0.4s ease-out; }
.pipeline-header { padding: 16px 20px; background: rgba(99,102,241,0.08);
                   display: flex; align-items: center; justify-content: space-between; }
.pipeline-header h3 { font-size: 0.95em; }
.pipeline-time { font-size: 0.8em; color: var(--muted); }

/* Agent Steps */
.agent-steps { display: flex; gap: 4px; padding: 14px 20px;
               border-bottom: 1px solid var(--border); }
.agent-step { flex: 1; text-align: center; padding: 8px 4px; border-radius: 8px;
              font-size: 0.7em; font-weight: 600; color: var(--muted);
              transition: all 0.3s ease; }
.agent-step .icon { font-size: 1.4em; display: block; margin-bottom: 4px; }
.agent-step.done { color: var(--ink); }
.agent-step.done[data-agent="sales"] { background: rgba(245,158,11,0.1); }
.agent-step.done[data-agent="research"] { background: rgba(99,102,241,0.1); }
.agent-step.done[data-agent="content"] { background: rgba(139,92,246,0.1); }
.agent-step.done[data-agent="dev"] { background: rgba(233,69,96,0.1); }
.agent-step.done[data-agent="data"] { background: rgba(16,185,129,0.1); }

/* Result Sections */
.result-sections { padding: 0; }
.result-section { border-bottom: 1px solid var(--border); }
.result-section:last-child { border-bottom: none; }
.result-section summary { padding: 12px 20px; cursor: pointer; font-size: 0.85em;
                          font-weight: 600; display: flex; align-items: center; gap: 8px;
                          user-select: none; }
.result-section summary::-webkit-details-marker { display: none; }
.result-section .content { padding: 0 20px 16px; font-size: 0.85em;
                           color: var(--muted); line-height: 1.6; white-space: pre-wrap; }
.result-section .tag { display: inline-block; padding: 2px 8px; border-radius: 4px;
                       font-size: 0.75em; font-weight: 700; }
.tag-sales { background: rgba(245,158,11,0.2); color: var(--sales); }
.tag-research { background: rgba(99,102,241,0.2); color: var(--research); }
.tag-content { background: rgba(139,92,246,0.2); color: var(--content); }
.tag-dev { background: rgba(233,69,96,0.2); color: var(--dev); }
.tag-data { background: rgba(16,185,129,0.2); color: var(--data); }

/* Actions */
.result-actions { padding: 12px 20px; display: flex; gap: 10px;
                  border-top: 1px solid var(--border); }
.btn { padding: 8px 18px; border-radius: 8px; font-size: 0.85em; font-weight: 600;
       cursor: pointer; border: none; text-decoration: none;
       transition: transform 0.15s, box-shadow 0.15s; display: inline-block; }
.btn:hover { transform: translateY(-1px); }
.btn-accent { background: var(--accent); color: #fff; }
.btn-accent:hover { box-shadow: 0 4px 16px rgba(233,69,96,0.4); }
.btn-outline { background: transparent; color: var(--ink); border: 1px solid var(--border); }

/* Pipeline Loading Animation */
.pipeline-loading { align-self: flex-start; width: 100%; max-width: 700px;
                    background: var(--card); border: 1px solid var(--border);
                    border-radius: var(--radius); padding: 24px; animation: msgIn 0.3s ease-out; }
.pl-title { font-size: 0.9em; color: var(--muted); margin-bottom: 16px; text-align: center; }
.pl-steps { display: flex; gap: 8px; align-items: center; justify-content: center; }
.pl-step { width: 48px; height: 48px; border-radius: 50%; background: var(--border);
           display: flex; align-items: center; justify-content: center;
           font-size: 1.2em; transition: all 0.5s ease; }
.pl-step.active { transform: scale(1.2); }
.pl-step.done { background: var(--green); color: #fff; }
.pl-step[data-agent="sales"].active { background: var(--sales); color: #fff; box-shadow: 0 0 20px rgba(245,158,11,0.4); }
.pl-step[data-agent="research"].active { background: var(--research); color: #fff; box-shadow: 0 0 20px rgba(99,102,241,0.4); }
.pl-step[data-agent="content"].active { background: var(--content); color: #fff; box-shadow: 0 0 20px rgba(139,92,246,0.4); }
.pl-step[data-agent="dev"].active { background: var(--dev); color: #fff; box-shadow: 0 0 20px rgba(233,69,96,0.4); }
.pl-step[data-agent="data"].active { background: var(--data); color: #fff; box-shadow: 0 0 20px rgba(16,185,129,0.4); }
.pl-arrow { color: var(--muted); font-size: 0.8em; }
.pl-labels { display: flex; gap: 8px; justify-content: center; margin-top: 10px; }
.pl-label { width: 48px; text-align: center; font-size: 0.65em; color: var(--muted);
            font-weight: 600; }

/* Input Area */
.input-area { background: var(--surface); border-top: 1px solid var(--border);
              padding: 14px 24px; flex-shrink: 0; }
.input-row { max-width: 800px; margin: 0 auto; display: flex; gap: 10px; }
.input-row textarea { flex: 1; background: var(--bg); border: 1px solid var(--border);
                      color: var(--ink); padding: 12px 16px; border-radius: 12px;
                      font-size: 0.9em; font-family: inherit; resize: none;
                      outline: none; min-height: 48px; max-height: 120px; }
.input-row textarea:focus { border-color: var(--accent); }
.input-row button { padding: 12px 24px; background: var(--accent); color: #fff;
                    border: none; border-radius: 12px; font-weight: 700; font-size: 0.9em;
                    cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
                    flex-shrink: 0; }
.input-row button:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(233,69,96,0.4); }
.input-row button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
.hint { text-align: center; font-size: 0.75em; color: var(--muted); margin-top: 8px; }

/* Welcome */
.welcome { text-align: center; padding: 60px 20px; }
.welcome .icon { font-size: 3em; margin-bottom: 16px; }
.welcome h2 { font-size: 1.4em; margin-bottom: 8px; }
.welcome p { color: var(--muted); font-size: 0.9em; max-width: 500px; margin: 0 auto 20px; }
.welcome .examples { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.example-chip { background: var(--card); border: 1px solid var(--border);
                padding: 8px 16px; border-radius: 20px; font-size: 0.8em;
                color: var(--muted); cursor: pointer; transition: all 0.2s; }
.example-chip:hover { border-color: var(--accent); color: var(--ink); }

@keyframes msgIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.pulse { animation: pulse 1.5s ease-in-out infinite; }

/* Scrollbar */
.chat-area::-webkit-scrollbar { width: 6px; }
.chat-area::-webkit-scrollbar-track { background: transparent; }
.chat-area::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
</head>
<body>

<div class="header">
  <h1><span class="logo-dot"></span> Aetox Works</h1>
  <nav>
    <a href="/chat" class="active">💬 Chat</a>
    <a href="/">📊 Dashboard</a>
    <a href="/docs">📖 API Docs</a>
  </nav>
</div>

<div class="chat-area" id="chatArea">
  <div class="welcome" id="welcome">
    <div class="icon">🤖</div>
    <h2>Aetox AI Workforce</h2>
    <p>ระบบ Multi-Agent อัจฉริยะ — บอกสิ่งที่คุณต้องการ แล้ว AI จะจัดการทุกขั้นตอนให้</p>
    <div class="examples">
      <span class="example-chip" onclick="sendExample(this.textContent)">ทำ landing page สำหรับ startup</span>
      <span class="example-chip" onclick="sendExample(this.textContent)">วิเคราะห์ตลาด AI ประเทศไทย</span>
      <span class="example-chip" onclick="sendExample(this.textContent)">เขียนบทความเกี่ยวกับ automation</span>
      <span class="example-chip" onclick="sendExample(this.textContent)">สร้างเว็บขายคอร์สออนไลน์</span>
    </div>
  </div>
</div>

<div class="input-area">
  <div class="input-row">
    <textarea id="userInput" placeholder="บอกสิ่งที่คุณต้องการให้ Aetox ทำให้..." rows="1"
              onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendMessage()}"></textarea>
    <button id="sendBtn" onclick="sendMessage()">▶ ส่ง</button>
  </div>
  <div class="hint">Enter ส่ง · Shift+Enter ขึ้นบรรทัดใหม่</div>
</div>

<script>
const AGENTS = ['sales','research','content','dev','data'];
const AGENT_NAMES = { sales:'Sales', research:'Research', content:'Content', dev:'Dev', data:'Data' };
const AGENT_ICONS = { sales:'🗣️', research:'🔍', content:'✍️', dev:'💻', data:'📊' };
const AGENT_TAGS = { sales:'tag-sales', research:'tag-research', content:'tag-content', dev:'tag-dev', data:'tag-data' };

const chatArea = document.getElementById('chatArea');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

function sendExample(text) { userInput.value = text; sendMessage(); }

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = '';
  userInput.style.height = 'auto';
  document.getElementById('welcome')?.remove();
  addUserMsg(text);
  setSending(true);

  const loadCard = addLoadingCard();

  // Animate pipeline steps
  for (let i = 0; i < AGENTS.length; i++) {
    await sleep(400);
    updateLoadingStep(loadCard, i);
  }

  try {
    const resp = await fetch('/pipeline/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: text, mode: 'pipeline' })
    });
    const data = await resp.json();
    loadCard.remove();
    if (data.status === 'success') {
      addResultCard(data);
    } else {
      addBotMsg('❌ Pipeline error: ' + (data.detail || 'Unknown error'));
    }
  } catch(e) {
    loadCard.remove();
    addBotMsg('❌ Connection error: ' + e.message);
  }
  setSending(false);
  userInput.focus();
}

function addUserMsg(text) {
  const div = document.createElement('div'); div.className = 'msg user';
  div.innerHTML = `<div class="bubble">${esc(text)}</div>`;
  chatArea.appendChild(div);
  scrollBottom();
}

function addBotMsg(text) {
  const div = document.createElement('div'); div.className = 'msg bot';
  div.innerHTML = `<div class="bubble">${esc(text)}</div>`;
  chatArea.appendChild(div);
  scrollBottom();
}

function addLoadingCard() {
  const steps = AGENTS.map((a,i) =>
    `<div class="pl-step" data-agent="${a}" id="ls-${i}">${AGENT_ICONS[a]}</div>` +
    (i < AGENTS.length-1 ? '<span class="pl-arrow">→</span>' : '')
  ).join('');
  const labels = AGENTS.map(a => `<div class="pl-label">${AGENT_NAMES[a]}</div>`).join('');

  const div = document.createElement('div');
  div.innerHTML = `
    <div class="pipeline-loading" id="loadingCard">
      <div class="pl-title pulse">⚡ Aetox Pipeline กำลังทำงาน...</div>
      <div class="pl-steps">${steps}</div>
      <div class="pl-labels">${labels}</div>
    </div>
  `;
  chatArea.appendChild(div.firstElementChild);
  scrollBottom();
  return document.getElementById('loadingCard');
}

function updateLoadingStep(card, idx) {
  const step = card.querySelector(`#ls-${idx}`);
  if (step) { step.classList.add('active'); }
  if (idx > 0) {
    const prev = card.querySelector(`#ls-${idx-1}`);
    if (prev) { prev.classList.remove('active'); prev.classList.add('done'); }
  }
}

function addResultCard(data) {
  const agents = data.agents_used || [];
  const stepsHtml = AGENTS.map(a => {
    const done = agents.includes(a);
    return `<div class="agent-step ${done?'done':''}" data-agent="${a}">
      <span class="icon">${AGENT_ICONS[a]}</span>${AGENT_NAMES[a]}
    </div>`;
  }).join('');

  const sectionsHtml = AGENTS.filter(a => agents.includes(a)).map(a => {
    return `<details class="result-section" ${a==='sales'?'open':''}>
      <summary><span class="tag ${AGENT_TAGS[a]}">${AGENT_ICONS[a]} ${AGENT_NAMES[a]}</span> Complete</summary>
      <div class="content" id="section-${a}">Loading...</div>
    </details>`;
  }).join('');

  const card = document.createElement('div');
  card.innerHTML = `
    <div class="pipeline-result">
      <div class="pipeline-header">
        <h3>✅ Pipeline Complete</h3>
        <span class="pipeline-time">${data.elapsed_ms}ms</span>
      </div>
      <div class="agent-steps">${stepsHtml}</div>
      <div class="result-sections">${sectionsHtml}</div>
      <div class="result-actions">
        <a href="/" class="btn btn-outline">📊 View Dashboard</a>
        <button class="btn btn-accent" onclick="this.textContent='Copied!';navigator.clipboard.writeText(document.getElementById('fullOutput')?.textContent||'')">📋 Copy Report</button>
      </div>
      <div style="display:none" id="fullOutput">${esc(data.output||'')}</div>
    </div>
  `;
  chatArea.appendChild(card.firstElementChild);
  scrollBottom();

  // Populate sections from output
  populateSections(data);
}

function populateSections(data) {
  // Parse the final output for per-agent data
  const output = data.output || '';
  const sections = {
    sales: output.match(/Sales[:\s]+([^\n]+)/)?.[1] || 'Lead captured successfully',
    research: output.match(/Research[:\s]+([^\n]+)/)?.[1] || 'Market research completed',
    content: output.match(/Content[:\s]+([^\n]+)/)?.[1] || 'Content draft created',
    dev: output.match(/Dev[:\s]+([^\n]+)/)?.[1] || 'Landing page built',
    data: output.match(/Data[:\s]+([^\n]+)/)?.[1] || 'Report generated',
  };
  for (const [agent, text] of Object.entries(sections)) {
    const el = document.getElementById('section-' + agent);
    if (el) el.textContent = text;
  }

  // Show full output in last section
  const dataSection = document.getElementById('section-data');
  if (dataSection && output) {
    dataSection.textContent = output;
  }
}

function setSending(disabled) {
  sendBtn.disabled = disabled;
  sendBtn.textContent = disabled ? '...' : '▶ ส่ง';
  userInput.disabled = disabled;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function scrollBottom() { chatArea.scrollTop = chatArea.scrollHeight; }

// Auto-resize textarea
userInput.addEventListener('input', () => {
  userInput.style.height = 'auto';
  userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
});
</script>
</body>
</html>"""
