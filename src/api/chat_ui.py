"""
Aetox Works — Chat UI v4 (LINE-style)
Seed: oklch(0.700 0.130 60.0) orange/honey
Product register: restrained, familiar, task-focused
Scene: "Morning coffee shop — warm sunlight, casual conversations"
"""
CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Aetox</title>
<style>
:root{
  --bg:oklch(0.965 0.004 85);
  --surface:oklch(1 0 0);
  --ink:oklch(0.22 0.006 75);
  --muted:oklch(0.62 0.012 80);
  --primary:oklch(0.66 0.145 55);
  --primary-text:oklch(1 0 0);
  --accent:oklch(0.52 0.16 250);
  --bubble-self:oklch(0.72 0.12 150);
  --bubble-self-text:oklch(1 0 0);
  --bubble-other:var(--surface);
  --border:oklch(0.88 0.008 85);
  --shadow:0 1px 2px oklch(0 0 0 / 0.04);
  --radius:16px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Noto Sans Thai',system-ui,sans-serif;
  background:var(--bg);color:var(--ink);height:100dvh;display:flex;flex-direction:column;
  overflow:hidden;-webkit-font-smoothing:antialiased;
  background-image:url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5 Q35 0 40 5 Q45 10 40 15 Q35 20 30 15 Q25 10 30 5Z' fill='%23e8e4dd' opacity='0.5'/%3E%3Cpath d='M50 30 Q55 25 60 30 L55 38 Q50 43 45 38 L50 30Z' fill='%23e8e4dd' opacity='0.3'/%3E%3Cpath d='M10 45 Q15 40 20 45 Q25 50 20 55 Q15 60 10 55 Q5 50 10 45Z' fill='%23e8e4dd' opacity='0.4'/%3E%3C/svg%3E");
  background-size:120px 120px;
}

/* Header */
.header{
  background:oklch(0.98 0.003 85 / 0.92);backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--border);padding:0 16px;height:52px;
  display:flex;align-items:center;justify-content:space-between;flex-shrink:0;
}
.header-left{display:flex;align-items:center;gap:10px}
.avatar{width:34px;height:34px;border-radius:50%;background:var(--primary);display:flex;align-items:center;justify-content:center;color:var(--primary-text);font-size:0.85em;font-weight:700}
.header h1{font-size:0.95em;font-weight:700}
.header-sub{font-size:0.72em;color:var(--muted)}
.header a{color:var(--muted);text-decoration:none;font-size:0.8em;padding:6px 12px;border-radius:8px;transition:all 0.2s}
.header a:hover{background:oklch(0 0 0 / 0.04);color:var(--ink)}

/* Chat */
.chat-area{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.chat-area::-webkit-scrollbar{width:4px}
.chat-area::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

/* Messages */
.msg{max-width:72%;animation:msgIn 0.25s ease-out;display:flex;flex-direction:column}
.msg.self{align-self:flex-end;align-items:flex-end}
.msg.other{align-self:flex-start;align-items:flex-start}
.msg .bubble{padding:9px 14px;font-size:0.9em;line-height:1.5;word-break:break-word}
.msg.self .bubble{background:var(--bubble-self);color:var(--bubble-self-text);border-radius:var(--radius) var(--radius) 4px var(--radius)}
.msg.other .bubble{background:var(--bubble-other);color:var(--ink);border-radius:var(--radius) var(--radius) var(--radius) 4px;border:1px solid var(--border);box-shadow:var(--shadow)}
.msg .time{font-size:0.65em;color:var(--muted);margin-top:3px;padding:0 4px}

/* Date divider */
.date-divider{text-align:center;padding:8px 0}
.date-divider span{background:oklch(0 0 0 / 0.06);color:var(--muted);font-size:0.7em;padding:4px 12px;border-radius:10px}

/* Result card */
.result-card{align-self:flex-start;width:100%;max-width:520px;background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;box-shadow:var(--shadow);animation:msgIn 0.3s ease-out;margin:4px 0}
.rc-top{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border)}
.rc-top h3{font-size:0.85em;font-weight:700}
.rc-top .time{font-size:0.72em;color:var(--muted)}
.rc-steps{display:flex;gap:0;padding:8px 16px;border-bottom:1px solid var(--border)}
.rc-step{flex:1;text-align:center;padding:4px 2px;font-size:0.6em;font-weight:700;color:var(--muted)}
.rc-step .si{font-size:1.2em;display:block}
.rc-step.done{color:var(--ink)}
.rc-summary{padding:12px 16px;font-size:0.82em;line-height:1.55;color:var(--muted)}

/* Typing */
.typing{align-self:flex-start;display:flex;align-items:center;gap:3px;padding:8px 14px;animation:msgIn 0.2s ease-out}
.typing span{width:6px;height:6px;border-radius:50%;background:var(--muted);animation:typingBounce 1.3s ease-in-out infinite}
.typing span:nth-child(2){animation-delay:0.16s}
.typing span:nth-child(3){animation-delay:0.32s}

/* Input */
.input-area{background:var(--surface);border-top:1px solid var(--border);padding:10px 14px;flex-shrink:0}
.input-row{max-width:680px;margin:0 auto;display:flex;gap:8px;align-items:flex-end}
.input-row textarea{flex:1;background:var(--bg);border:1px solid var(--border);color:var(--ink);padding:10px 16px;border-radius:20px;font-size:0.88em;font-family:inherit;resize:none;outline:none;min-height:40px;max-height:100px;line-height:1.4;transition:border-color 0.2s}
.input-row textarea:focus{border-color:var(--primary)}
.input-row button{width:40px;height:40px;border-radius:50%;background:var(--primary);color:var(--primary-text);border:none;font-size:1.1em;cursor:pointer;flex-shrink:0;transition:transform 0.15s,opacity 0.15s;display:flex;align-items:center;justify-content:center}
.input-row button:hover{transform:scale(1.05)}
.input-row button:disabled{opacity:0.4;cursor:not-allowed;transform:none}

/* Welcome */
.welcome{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.welcome .avatar-lg{width:64px;height:64px;border-radius:50%;background:var(--primary);display:flex;align-items:center;justify-content:center;color:var(--primary-text);font-size:1.8em;margin-bottom:12px}
.welcome p{color:var(--muted);font-size:0.85em;max-width:280px;line-height:1.5}

@keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes typingBounce{0%,60%,100%{transform:translateY(0);opacity:0.3}30%{transform:translateY(-5px);opacity:1}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:0.01ms!important;transition-duration:0.01ms!important}}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="avatar">A</div>
    <div><h1>Aetox Works</h1><div class="header-sub">online</div></div>
  </div>
  <a href="/admin">Admin</a>
</div>

<div class="chat-area" id="chatArea">
  <div class="welcome" id="welcome">
    <div class="avatar-lg">A</div>
    <p>สวัสดีครับ!<br>ผมคือ Sales Agent ของ Aetox<br>มีอะไรให้ช่วยไหมครับ?</p>
  </div>
</div>

<div class="input-area">
  <div class="input-row">
    <textarea id="userInput" placeholder="Message..." rows="1"
      onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
    <button id="sendBtn" onclick="send()">▶</button>
  </div>
</div>

<script>
const A=['sales','research','content','dev','data'];
const N={sales:'Sales',research:'Research',content:'Content',dev:'Dev',data:'Data'};
const I={sales:'🗣️',research:'🔍',content:'✍️',dev:'💻',data:'📊'};
const ca=document.getElementById('chatArea'),inp=document.getElementById('userInput'),btn=document.getElementById('sendBtn');
let ctx='';

async function send(){
  const t=inp.value.trim();if(!t)return;inp.value='';inp.style.height='40px';
  document.getElementById('welcome')?.remove();
  addMsg(t,'self');toggleSend(true);
  const typingEl=addTyping();
  try{
    const r=await fetch('/pipeline/run',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({input:t,mode:'pipeline',conversation_context:ctx})});
    const d=await r.json();typingEl.remove();
    if(d.status!=='success'){addMsg('ขออภัย ระบบขัดข้อง','other');toggleSend(false);inp.focus();return}
    ctx=d.conversation_context||'';
    if(d.sales_confirmed){addResult(d)}else{const reply=ctx.split('\nAetox: ').pop()||'';if(reply)addMsg(reply,'other')}
  }catch(e){typingEl.remove();addMsg('Connection error','other')}
  toggleSend(false);inp.focus()
}

function addMsg(t,role){const d=document.createElement('div');d.className='msg '+role;d.innerHTML=`<div class="bubble">${esc(t)}</div>`;ca.appendChild(d);ca.scrollTop=ca.scrollHeight}
function addTyping(){const d=document.createElement('div');d.className='typing';d.innerHTML='<span></span><span></span><span></span>';ca.appendChild(d);ca.scrollTop=ca.scrollHeight;return d}

function addResult(d){
  const agents=d.agents_used||[],steps=A.map(a=>`<div class="rc-step${agents.includes(a)?' done':''}"><span class="si">${I[a]}</span>${N[a]}</div>`).join('');
  const summary=(d.results||{}).data?.summary||d.output?.slice(0,250)||'Pipeline completed';
  const card=document.createElement('div');card.innerHTML=`
    <div class="result-card">
      <div class="rc-top"><h3>✓ Complete</h3><span class="time">${d.elapsed_ms}ms</span></div>
      <div class="rc-steps">${steps}</div>
      <div class="rc-summary">${esc(summary)}</div>
    </div>`;
  ca.appendChild(card.firstElementChild);ca.scrollTop=ca.scrollHeight
}

function toggleSend(v){btn.disabled=v;inp.disabled=v}
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
inp.addEventListener('input',()=>{inp.style.height='40px';inp.style.height=Math.min(inp.scrollHeight,100)+'px'})
</script>
</body>
</html>"""
