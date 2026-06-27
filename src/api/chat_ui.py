"""
Aetox Works — Chat UI (MVP Showcase) v2
Premium design: Multi-agent pipeline demo with glass morphism, staggered reveals, micro-interactions
"""
CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Works — AI Workforce</title>
<style>
:root {
  --bg: #06080f;
  --surface: #0c0f1a;
  --card: #111524;
  --border: #1e2438;
  --ink: #e2e6f2;
  --muted: #6e7594;
  --accent: #f43f5e;
  --accent-soft: rgba(244,63,94,0.12);
  --accent-glow: rgba(244,63,94,0.35);
  --green: #10b981;
  --green-soft: rgba(16,185,129,0.12);
  --amber: #f59e0b;
  --amber-soft: rgba(245,158,11,0.12);
  --blue: #6366f1;
  --blue-soft: rgba(99,102,241,0.12);
  --purple: #8b5cf6;
  --purple-soft: rgba(139,92,246,0.12);
  --radius-sm: 8px;
  --radius: 14px;
  --radius-lg: 20px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans Thai', 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--ink);
  height: 100vh; display: flex; flex-direction: column;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}

/* ── Header ── */
.header{
  background: rgba(12,15,26,0.85);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid var(--border);
  padding: 0 28px; height: 58px; display: flex; align-items: center;
  justify-content: space-between; flex-shrink: 0; z-index: 10;
}
.brand{display:flex;align-items:center;gap:10px}
.brand-dot{
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--accent); box-shadow: 0 0 14px var(--accent-glow);
  animation: brandPulse 3s ease-in-out infinite;
}
.brand h1{font-size:1em;font-weight:700;letter-spacing:-0.01em}
.nav{display:flex;gap:4px}
.nav a{
  color: var(--muted); text-decoration: none; font-size: 0.82em;
  font-weight: 500; padding: 7px 16px; border-radius: var(--radius-sm);
  transition: color 0.2s, background 0.2s;
}
.nav a:hover{color:var(--ink);background:rgba(255,255,255,0.04)}
.nav a.active{color:var(--accent);background:var(--accent-soft)}

/* ── Chat Area ── */
.chat-area{
  flex: 1; overflow-y: auto; padding: 24px 28px;
  display: flex; flex-direction: column; gap: 20px;
}
.chat-area::-webkit-scrollbar{width:5px}
.chat-area::-webkit-scrollbar-track{background:transparent}
.chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}

/* ── Welcome ── */
.welcome{
  flex:1; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding:40px 20px;
  animation: fadeInUp 0.6s ease-out;
}
.welcome-glow{
  width: 80px; height: 80px; border-radius: 50%;
  background: radial-gradient(circle, var(--accent-soft) 0%, transparent 70%);
  display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
  animation: welcomePulse 3s ease-in-out infinite;
}
.welcome-icon{font-size:2.4em;filter:drop-shadow(0 0 20px var(--accent-glow))}
.welcome h2{font-size:1.5em;font-weight:800;letter-spacing:-0.02em;margin-bottom:8px}
.welcome p{color:var(--muted);font-size:0.92em;max-width:460px;line-height:1.6;margin-bottom:28px}
.examples{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:520px}
.example-chip{
  background: var(--card); border: 1px solid var(--border);
  padding: 9px 18px; border-radius: 24px; font-size: 0.82em;
  color: var(--muted); cursor: pointer;
  transition: border-color 0.25s, color 0.25s, transform 0.2s, box-shadow 0.2s;
}
.example-chip:hover{
  border-color: var(--accent); color: var(--ink);
  transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

/* ── Messages ── */
.msg{max-width:78%;animation:msgIn 0.35s cubic-bezier(0.34,1.56,0.64,1)}
.msg.user{align-self:flex-end}
.msg.user .bubble{
  background: linear-gradient(135deg, var(--accent), #e11d48);
  color: #fff; border-radius: var(--radius-lg) var(--radius-lg) 6px var(--radius-lg);
  padding: 13px 20px; font-size: 0.93em; line-height: 1.55;
  box-shadow: 0 4px 20px var(--accent-glow);
}
.msg.bot{align-self:flex-start}
.msg.bot .bubble{
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 6px;
  padding: 13px 20px; font-size: 0.93em; line-height: 1.6;
}

/* ── Pipeline Loading ── */
.pl-loading{
  align-self:flex-start; width:100%; max-width:680px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 28px 24px 22px;
  animation: msgIn 0.4s ease-out;
}
.pl-title{text-align:center;color:var(--muted);font-size:0.88em;margin-bottom:20px}
.pl-title span{animation:pulse 1.5s ease-in-out infinite}
.pl-row{display:flex;align-items:center;justify-content:center;gap:6px}
.pl-step{
  width: 52px; height: 52px; border-radius: 50%;
  background: var(--border); display: flex; align-items: center;
  justify-content: center; font-size: 1.3em;
  transition: all 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
.pl-step.active{transform:scale(1.18)}
.pl-step.done{color:#fff}
.pl-step[data-a="sales"].active,.pl-step[data-a="sales"].done{background:var(--amber);box-shadow:0 0 20px rgba(245,158,11,0.45)}
.pl-step[data-a="research"].active,.pl-step[data-a="research"].done{background:var(--blue);box-shadow:0 0 20px rgba(99,102,241,0.45)}
.pl-step[data-a="content"].active,.pl-step[data-a="content"].done{background:var(--purple);box-shadow:0 0 20px rgba(139,92,246,0.45)}
.pl-step[data-a="dev"].active,.pl-step[data-a="dev"].done{background:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.pl-step[data-a="data"].active,.pl-step[data-a="data"].done{background:var(--green);box-shadow:0 0 20px rgba(16,185,129,0.45)}
.pl-arrow{color:var(--border);font-size:0.75em;margin:0 2px}
.pl-labels{display:flex;gap:6px;justify-content:center;margin-top:12px}
.pl-label{width:52px;text-align:center;font-size:0.68em;color:var(--muted);font-weight:600}

/* ── Result Card ── */
.result-card{
  align-self:flex-start; width:100%; max-width:680px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  animation: msgIn 0.5s ease-out;
}
.rc-header{
  padding: 18px 22px; background: linear-gradient(135deg, rgba(16,185,129,0.06), rgba(99,102,241,0.04));
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--border);
}
.rc-header h3{font-size:0.95em;font-weight:700;display:flex;align-items:center;gap:8px}
.rc-time{font-size:0.78em;color:var(--muted)}
.rc-steps{
  display: flex; gap: 2px; padding: 12px 22px;
  border-bottom: 1px solid var(--border);
}
.rc-step{
  flex:1; text-align:center; padding:8px 4px; border-radius:8px;
  font-size:0.66em; font-weight:700; color:var(--muted);
  transition: all 0.3s;
}
.rc-step .si{font-size:1.35em;display:block;margin-bottom:3px}
.rc-step.done{color:var(--ink)}
.rc-step.done[data-a="sales"]{background:var(--amber-soft)}
.rc-step.done[data-a="research"]{background:var(--blue-soft)}
.rc-step.done[data-a="content"]{background:var(--purple-soft)}
.rc-step.done[data-a="dev"]{background:var(--accent-soft)}
.rc-step.done[data-a="data"]{background:var(--green-soft)}
.rc-body{padding:0}
.rc-section{border-bottom:1px solid var(--border)}
.rc-section:last-child{border-bottom:none}
.rc-section summary{
  padding:13px 22px; cursor:pointer; font-size:0.84em; font-weight:600;
  display:flex;align-items:center;gap:8px; user-select:none;
  transition:background 0.15s;
}
.rc-section summary:hover{background:rgba(255,255,255,0.02)}
.rc-section summary::-webkit-details-marker{display:none}
.rc-section .content{
  padding:0 22px 16px; font-size:0.83em; color:var(--muted);
  line-height:1.65; white-space:pre-wrap;
}
.tag{
  display:inline-block;padding:3px 10px;border-radius:6px;
  font-size:0.78em;font-weight:700;letter-spacing:0.02em;
}
.tag-s{background:var(--amber-soft);color:var(--amber)}
.tag-r{background:var(--blue-soft);color:var(--blue)}
.tag-c{background:var(--purple-soft);color:var(--purple)}
.tag-d{background:var(--accent-soft);color:var(--accent)}
.tag-a{background:var(--green-soft);color:var(--green)}
.rc-actions{
  padding:14px 22px; display:flex; gap:10px;
  border-top:1px solid var(--border);
}
.btn{
  padding: 9px 20px; border-radius: var(--radius-sm); font-size: 0.83em;
  font-weight: 600; cursor: pointer; border: none; text-decoration: none;
  transition: transform 0.15s, box-shadow 0.15s; display: inline-flex;
  align-items: center; gap: 6px;
}
.btn:hover{transform:translateY(-1px)}
.btn-primary{background:var(--accent);color:#fff}
.btn-primary:hover{box-shadow:0 4px 18px var(--accent-glow)}
.btn-ghost{background:transparent;color:var(--muted);border:1px solid var(--border)}
.btn-ghost:hover{color:var(--ink);border-color:var(--muted)}

/* ── Input ── */
.input-area{
  background: var(--surface); border-top: 1px solid var(--border);
  padding: 16px 28px; flex-shrink: 0;
}
.input-row{max-width:780px;margin:0 auto;display:flex;gap:10px}
.input-row textarea{
  flex:1; background:var(--bg); border:1px solid var(--border);
  color:var(--ink); padding:13px 18px; border-radius:var(--radius);
  font-size:0.9em; font-family:inherit; resize:none; outline:none;
  min-height:52px; max-height:140px; line-height:1.5;
  transition:border-color 0.2s, box-shadow 0.2s;
}
.input-row textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.input-row button{
  padding: 0 28px; background: var(--accent); color: #fff;
  border: none; border-radius: var(--radius); font-weight: 700;
  font-size: 0.92em; cursor: pointer; flex-shrink: 0;
  transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s;
}
.input-row button:hover{transform:translateY(-1px);box-shadow:0 4px 20px var(--accent-glow)}
.input-row button:disabled{opacity:0.45;cursor:not-allowed;transform:none;box-shadow:none}
.hint{text-align:center;font-size:0.72em;color:var(--border);margin-top:8px}

/* ── Keyframes ── */
@keyframes msgIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
@keyframes brandPulse{0%,100%{box-shadow:0 0 14px var(--accent-glow)}50%{box-shadow:0 0 24px var(--accent-glow)}}
@keyframes welcomePulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:0.01ms!important;transition-duration:0.01ms!important}
}
@media (max-width:640px){
  .header{padding:0 16px}
  .chat-area{padding:16px}
  .input-area{padding:12px 16px}
  .msg{max-width:90%}
  .pl-step{width:42px;height:42px;font-size:1.1em}
  .pl-label{width:42px;font-size:0.6em}
}
</style>
</head>
<body>

<div class="header">
  <div class="brand">
    <span class="brand-dot"></span>
    <h1>Aetox Works</h1>
  </div>
  <nav>
    <a href="/" class="active">Chat</a>
    <a href="/admin">Admin</a>
    <a href="/docs">API</a>
  </nav>
</div>

<div class="chat-area" id="chatArea">
  <div class="welcome" id="welcome">
    <div class="welcome-glow"><span class="welcome-icon">⚡</span></div>
    <h2>AI Workforce ที่ทำงานแทนคุณได้</h2>
    <p>บอกสิ่งที่คุณต้องการ — Aetox จะจัดการทุกขั้นตอน ตั้งแต่คุยลูกค้า ค้นหาข้อมูล เขียนคอนเทนต์ สร้างเว็บ ไปจนถึงวัดผล</p>
    <div class="examples">
      <span class="example-chip" onclick="quickSend(this)">สร้าง landing page ขายคอร์ส AI</span>
      <span class="example-chip" onclick="quickSend(this)">วิเคราะห์ตลาด Automation</span>
      <span class="example-chip" onclick="quickSend(this)">เขียนบทความเรื่องอนาคตของงาน</span>
      <span class="example-chip" onclick="quickSend(this)">ทำเว็บให้ startup จัดการคลังสินค้า</span>
    </div>
  </div>
</div>

<div class="input-area">
  <div class="input-row">
    <textarea id="userInput" placeholder="บอกสิ่งที่คุณต้องการให้ Aetox ทำให้..." rows="1"
      onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
    <button id="sendBtn" onclick="send()">Send</button>
  </div>
  <div class="hint">Enter to send · Shift+Enter for new line</div>
</div>

<script>
const A = ['sales','research','content','dev','data'];
const N = {sales:'Sales',research:'Research',content:'Content',dev:'Dev',data:'Data'};
const I = {sales:'🗣️',research:'🔍',content:'✍️',dev:'💻',data:'📊'};
const T = {sales:'tag-s',research:'tag-r',content:'tag-c',dev:'tag-d',data:'tag-a'};
const ca = document.getElementById('chatArea');
const inp = document.getElementById('userInput');
const btn = document.getElementById('sendBtn');

// Multi-turn conversation state
let conversationCtx = '';
let isConversationMode = false;

function quickSend(el){inp.value=el.textContent;send()}

async function send(){
  const t = inp.value.trim(); if(!t) return;
  inp.value=''; inp.style.height='auto';
  document.getElementById('welcome')?.remove();
  addMsg(t,'user'); toggleSend(true);

  // If in conversation mode, show typing indicator
  if(isConversationMode){
    const typingCard = addTyping('Sales Agent is thinking...');
    await sleep(600);
    typingCard.remove();
  } else {
    // First message — show pipeline loading
    const card = addLoading();
    for(let i=0;i<A.length;i++){await sleep(400);stepLoading(card,i)}
    card.remove();
  }

  try{
    const r = await fetch('/pipeline/run',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({input:t,mode:'pipeline',conversation_context:conversationCtx})
    });
    const d = await r.json();

    if(d.status==='success'){
      // Update conversation context
      conversationCtx = d.conversation_context||'';

      if(d.sales_confirmed){
        // Sales confirmed → full pipeline result
        isConversationMode = false;
        addResult(d);
      } else if(!d.sales_confirmed && d.conversation_context){
        // Sales in conversation mode → show reply as chat message
        isConversationMode = true;
        const lastReply = d.conversation_context.split('\nAetox: ').pop() || d.output || 'สวัสดีครับ';
        addMsg(lastReply, 'bot');
      } else if(d.agents_used.length===1 && d.agents_used[0]==='sales'){
        // Fallback: only Sales ran
        isConversationMode = true;
        addMsg(d.output||'สวัสดีครับ','bot');
      } else {
        // Full pipeline without sales step
        addResult(d);
      }
    } else {
      addMsg('Error: '+(d.detail||'Unknown'),'bot');
    }
  }catch(e){
    isConversationMode = false;
    addMsg('Connection error: '+e.message,'bot');
  }
  toggleSend(false); inp.focus();
}

function addTyping(text){
  const d=document.createElement('div');d.innerHTML=`
    <div class="pl-loading" style="text-align:center;padding:16px">
      <div class="pl-title"><span>${esc(text)}</span></div>
    </div>`;
  ca.appendChild(d.firstElementChild);ca.scrollTop=ca.scrollHeight;
  return ca.lastElementChild;
}

function addMsg(text,role){
  const d=document.createElement('div');d.className='msg '+role;
  d.innerHTML=`<div class="bubble">${esc(text)}</div>`;
  ca.appendChild(d);ca.scrollTop=ca.scrollHeight;
}

function addLoading(){
  const s = A.map((a,i)=>`<div class="pl-step" data-a="${a}" id="ls${i}">${I[a]}</div>`+(i<A.length-1?'<span class="pl-arrow">▸</span>':'')).join('');
  const l = A.map(a=>`<div class="pl-label">${N[a]}</div>`).join('');
  const d=document.createElement('div');d.innerHTML=`
    <div class="pl-loading" id="loadCard">
      <div class="pl-title"><span>Pipeline running...</span></div>
      <div class="pl-row">${s}</div><div class="pl-labels">${l}</div>
    </div>`;
  ca.appendChild(d.firstElementChild);ca.scrollTop=ca.scrollHeight;
  return document.getElementById('loadCard');
}

function stepLoading(card,i){
  const s=card.querySelector('#ls'+i); if(s)s.classList.add('active');
  if(i>0){const p=card.querySelector('#ls'+(i-1));if(p){p.classList.remove('active');p.classList.add('done')}}
}

function addResult(d){
  const agents = d.agents_used||[];
  const steps = A.map(a=>{
    const ok=agents.includes(a);
    return `<div class="rc-step${ok?' done':''}" data-a="${a}"><span class="si">${I[a]}</span>${N[a]}</div>`;
  }).join('');

  // Simple summary for customer — no internal details
  const dataResult = (d.results||{}).data||{};
  const summary = dataResult.summary || d.output?.slice(0,300) || 'Pipeline completed successfully.';

  const card=document.createElement('div');card.innerHTML=`
    <div class="result-card">
      <div class="rc-header"><h3><span style="color:var(--green)">&#10003;</span> Pipeline Complete</h3><span class="rc-time">${d.elapsed_ms}ms</span></div>
      <div class="rc-steps">${steps}</div>
      <div style="padding:16px 22px;font-size:0.9em;line-height:1.6;color:var(--muted)">${esc(summary)}</div>
      <div class="rc-actions">
        <span style="font-size:0.78em;color:var(--muted)">ระบบกำลังดำเนินการต่อ — รอสักครู่</span>
      </div>
    </div>`;
  ca.appendChild(card.firstElementChild);ca.scrollTop=ca.scrollHeight;
}

function copyReport(btn){
  const el=document.getElementById('fullOutput');
  if(el){navigator.clipboard.writeText(el.textContent||'')}
  btn.textContent='Copied!';setTimeout(()=>btn.textContent='Copy Report',2000);
}

function toggleSend(v){btn.disabled=v;btn.textContent=v?'...':'Send';inp.disabled=v}
function sleep(ms){return new Promise(r=>setTimeout(r,ms))}
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
inp.addEventListener('input',()=>{inp.style.height='auto';inp.style.height=Math.min(inp.scrollHeight,140)+'px'});
</script>
</body>
</html>"""
