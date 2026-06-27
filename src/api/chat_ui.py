"""
Aetox Works — Chat UI v3
Bright minimal design, real chat feel, typing indicator, CSS background art
"""
CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox — AI Workforce</title>
<style>
:root{
  --bg:#f0f4ff;--surface:#fff;--ink:#1e1e3a;--muted:#8b8faa;
  --accent:#ff5e7a;--accent2:#7c5cfc;--green:#10b981;
  --bubble-user:linear-gradient(135deg,#ff5e7a,#ff3d6a);
  --bubble-bot:#fff;--border:#e8ecf4;
  --radius:18px;--shadow:0 2px 12px rgba(0,0,0,0.04);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Noto Sans Thai','Segoe UI',system-ui,sans-serif;
  background:var(--bg);color:var(--ink);height:100vh;display:flex;flex-direction:column;
  overflow:hidden;-webkit-font-smoothing:antialiased;
  background-image:
    radial-gradient(circle at 10% 20%,rgba(124,92,252,0.06) 0%,transparent 50%),
    radial-gradient(circle at 90% 80%,rgba(255,94,122,0.05) 0%,transparent 50%),
    radial-gradient(circle at 50% 50%,rgba(124,92,252,0.03) 0%,transparent 70%);
  background-attachment:fixed;
}

/* Header */
.header{
  background:rgba(255,255,255,0.8);backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);padding:0 24px;height:56px;
  display:flex;align-items:center;justify-content:space-between;flex-shrink:0;z-index:10;
}
.brand{display:flex;align-items:center;gap:10px}
.brand-dot{width:9px;height:9px;border-radius:50%;background:var(--accent);box-shadow:0 0 10px rgba(255,94,122,0.5)}
.brand h1{font-size:1em;font-weight:700;letter-spacing:-0.01em}
.nav{display:flex;gap:2px}
.nav a{color:var(--muted);text-decoration:none;font-size:0.82em;font-weight:500;padding:6px 14px;border-radius:8px;transition:all 0.2s}
.nav a:hover{color:var(--ink);background:rgba(0,0,0,0.03)}
.nav a.active{color:var(--accent);background:rgba(255,94,122,0.08)}

/* Chat */
.chat-area{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:14px}
.chat-area::-webkit-scrollbar{width:5px}
.chat-area::-webkit-scrollbar-track{background:transparent}
.chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}

/* Welcome */
.welcome{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.welcome-icon{font-size:3em;margin-bottom:12px;animation:welcomeFloat 3s ease-in-out infinite}
.welcome h2{font-size:1.5em;font-weight:800;margin-bottom:6px;letter-spacing:-0.02em}
.welcome p{color:var(--muted);font-size:0.9em;max-width:400px;line-height:1.6;margin-bottom:24px}
.examples{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:500px}
.example-chip{
  background:var(--surface);border:1.5px solid var(--border);
  padding:9px 18px;border-radius:24px;font-size:0.82em;color:var(--muted);
  cursor:pointer;transition:all 0.25s;
}
.example-chip:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px);box-shadow:0 4px 14px rgba(255,94,122,0.1)}

/* Messages */
.msg{max-width:76%;animation:msgIn 0.3s cubic-bezier(0.34,1.56,0.64,1)}
.msg.user{align-self:flex-end}
.msg.user .bubble{background:var(--bubble-user);color:#fff;border-radius:var(--radius) var(--radius) 6px var(--radius);padding:11px 18px;font-size:0.92em;line-height:1.55}
.msg.bot{align-self:flex-start}
.msg.bot .bubble{background:var(--bubble-bot);border:1px solid var(--border);border-radius:var(--radius) var(--radius) var(--radius) 6px;padding:11px 18px;font-size:0.92em;line-height:1.6;box-shadow:var(--shadow)}

/* Typing Indicator */
.typing{display:flex;align-items:center;gap:4px;padding:14px 20px;align-self:flex-start;animation:msgIn 0.3s ease-out}
.typing span{width:7px;height:7px;border-radius:50%;background:var(--muted);animation:typingBounce 1.4s ease-in-out infinite}
.typing span:nth-child(2){animation-delay:0.2s}
.typing span:nth-child(3){animation-delay:0.4s}
@keyframes typingBounce{0%,60%,100%{transform:translateY(0);opacity:0.4}30%{transform:translateY(-6px);opacity:1}}

/* Pipeline Loading (compact) */
.pl-compact{align-self:flex-start;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 20px;box-shadow:var(--shadow);animation:msgIn 0.3s ease-out;display:flex;align-items:center;gap:12px}
.pl-compact .pl-text{font-size:0.85em;color:var(--muted)}
.pl-compact .pl-dots{display:flex;gap:3px}
.pl-compact .pl-dots span{width:5px;height:5px;border-radius:50%;background:var(--accent);animation:typingBounce 1.2s ease-in-out infinite}
.pl-compact .pl-dots span:nth-child(2){animation-delay:0.15s}
.pl-compact .pl-dots span:nth-child(3){animation-delay:0.3s}

/* Result Card */
.result-card{align-self:flex-start;width:100%;max-width:600px;background:var(--surface);border:1px solid var(--border);border-radius:16px;overflow:hidden;box-shadow:var(--shadow);animation:msgIn 0.4s ease-out}
.rc-header{padding:16px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border)}
.rc-header h3{font-size:0.92em;font-weight:700}
.rc-time{font-size:0.78em;color:var(--muted)}
.rc-steps{display:flex;gap:2px;padding:10px 20px;border-bottom:1px solid var(--border)}
.rc-step{flex:1;text-align:center;padding:6px 4px;border-radius:8px;font-size:0.65em;font-weight:700;color:var(--muted);transition:all 0.3s}
.rc-step .si{font-size:1.3em;display:block;margin-bottom:2px}
.rc-step.done{color:var(--ink)}
.rc-step.done[data-a="sales"]{background:rgba(245,158,11,0.1)}
.rc-step.done[data-a="research"]{background:rgba(99,102,241,0.1)}
.rc-step.done[data-a="content"]{background:rgba(139,92,246,0.1)}
.rc-step.done[data-a="dev"]{background:rgba(255,94,122,0.08)}
.rc-step.done[data-a="data"]{background:rgba(16,185,129,0.1)}
.rc-body{padding:14px 20px;font-size:0.88em;line-height:1.6;color:var(--muted)}

/* Input */
.input-area{background:rgba(255,255,255,0.8);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-top:1px solid var(--border);padding:14px 24px;flex-shrink:0}
.input-row{max-width:700px;margin:0 auto;display:flex;gap:10px}
.input-row textarea{flex:1;background:var(--bg);border:1.5px solid var(--border);color:var(--ink);padding:12px 18px;border-radius:14px;font-size:0.9em;font-family:inherit;resize:none;outline:none;min-height:48px;max-height:120px;line-height:1.5;transition:border-color 0.2s,box-shadow 0.2s}
.input-row textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,94,122,0.1)}
.input-row button{padding:0 24px;background:var(--accent);color:#fff;border:none;border-radius:14px;font-weight:700;font-size:0.9em;cursor:pointer;flex-shrink:0;transition:transform 0.15s,box-shadow 0.15s,opacity 0.15s}
.input-row button:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(255,94,122,0.35)}
.input-row button:disabled{opacity:0.45;cursor:not-allowed;transform:none;box-shadow:none}

@keyframes msgIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes welcomeFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:0.01ms!important;transition-duration:0.01ms!important}}
@media(max-width:640px){.header{padding:0 16px}.chat-area{padding:14px 16px}.input-area{padding:10px 16px}.msg{max-width:88%}}
</style>
</head>
<body>

<div class="header">
  <div class="brand"><span class="brand-dot"></span><h1>Aetox Works</h1></div>
  <nav>
    <a href="/" class="active">Chat</a>
    <a href="/admin">Admin</a>
    <a href="/docs">API</a>
  </nav>
</div>

<div class="chat-area" id="chatArea">
  <div class="welcome" id="welcome">
    <div class="welcome-icon">✨</div>
    <h2>AI ที่ทำงานแทนคุณได้</h2>
    <p>บอกสิ่งที่คุณต้องการ แล้วระบบ Multi-Agent จะจัดการทุกขั้นตอนให้</p>
    <div class="examples">
      <span class="example-chip" onclick="quickSend(this)">สร้าง landing page</span>
      <span class="example-chip" onclick="quickSend(this)">วิเคราะห์ตลาด</span>
      <span class="example-chip" onclick="quickSend(this)">เขียนบทความ</span>
      <span class="example-chip" onclick="quickSend(this)">ทำเว็บให้ startup</span>
    </div>
  </div>
</div>

<div class="input-area">
  <div class="input-row">
    <textarea id="userInput" placeholder="บอกสิ่งที่คุณต้องการ..." rows="1"
      onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
    <button id="sendBtn" onclick="send()">Send</button>
  </div>
</div>

<script>
const A=['sales','research','content','dev','data'];
const N={sales:'Sales',research:'Research',content:'Content',dev:'Dev',data:'Data'};
const I={sales:'🗣️',research:'🔍',content:'✍️',dev:'💻',data:'📊'};
const ca=document.getElementById('chatArea'),inp=document.getElementById('userInput'),btn=document.getElementById('sendBtn');
let ctx='';

function quickSend(el){inp.value=el.textContent;send()}

async function send(){
  const t=inp.value.trim();if(!t)return;inp.value='';inp.style.height='auto';
  document.getElementById('welcome')?.remove();
  addMsg(t,'user');toggleSend(true);
  const typingEl=addTyping();
  try{
    const r=await fetch('/pipeline/run',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({input:t,mode:'pipeline',conversation_context:ctx})});
    const d=await r.json();typingEl.remove();
    if(d.status!=='success'){addMsg('ขออภัย ระบบขัดข้อง','bot');toggleSend(false);inp.focus();return}
    ctx=d.conversation_context||'';
    if(d.sales_confirmed){addResult(d)}
    else{const reply=ctx.split('\nAetox: ').pop()||'';if(reply)addMsg(reply,'bot')}
  }catch(e){typingEl.remove();addMsg('Connection error','bot')}
  toggleSend(false);inp.focus()
}

function addMsg(t,role){const d=document.createElement('div');d.className='msg '+role;d.innerHTML=`<div class="bubble">${esc(t)}</div>`;ca.appendChild(d);ca.scrollTop=ca.scrollHeight}
function addTyping(){const d=document.createElement('div');d.className='typing';d.innerHTML='<span></span><span></span><span></span>';ca.appendChild(d);ca.scrollTop=ca.scrollHeight;return d}

function addResult(d){
  const agents=d.agents_used||[];
  const steps=A.map(a=>`<div class="rc-step${agents.includes(a)?' done':''}" data-a="${a}"><span class="si">${I[a]}</span>${N[a]}</div>`).join('');
  const summary=(d.results||{}).data?.summary||d.output?.slice(0,300)||'Pipeline completed.';
  const card=document.createElement('div');card.innerHTML=`
    <div class="result-card">
      <div class="rc-header"><h3>✓ Pipeline Complete</h3><span class="rc-time">${d.elapsed_ms}ms</span></div>
      <div class="rc-steps">${steps}</div>
      <div class="rc-body">${esc(summary)}</div>
    </div>`;
  ca.appendChild(card.firstElementChild);ca.scrollTop=ca.scrollHeight
}

function toggleSend(v){btn.disabled=v;btn.textContent=v?'...':'Send';inp.disabled=v}
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
inp.addEventListener('input',()=>{inp.style.height='auto';inp.style.height=Math.min(inp.scrollHeight,120)+'px'})
</script>
</body>
</html>"""
