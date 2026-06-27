"""
Aetox Works — Chat UI v5
Background: sky-ocean gradient scene
Bubbles: glass morphism (transparent + blur)
"""
CHAT_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Aetox</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Noto Sans Thai',system-ui,sans-serif;
  color:#1a1a2e;height:100dvh;display:flex;flex-direction:column;overflow:hidden;
  -webkit-font-smoothing:antialiased;
  background:url(/static/bg.jpg) center/cover no-repeat fixed;
}

/* Header */
.header{
  position:relative;z-index:2;
  background:rgba(255,255,255,0.55);backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  padding:0 16px;height:52px;display:flex;align-items:center;
  justify-content:space-between;flex-shrink:0;
}
.header-left{display:flex;align-items:center;gap:10px}
.avatar{width:34px;height:34px;border-radius:50%;
  background:linear-gradient(135deg,#f43f5e,#e94560);
  display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:0.85em;font-weight:700}
.header h1{font-size:0.95em;font-weight:700;color:#1a1a2e}
.header-sub{font-size:0.7em;color:#6b7280}
.header a{color:#6b7280;text-decoration:none;font-size:0.8em;padding:6px 12px;border-radius:8px;transition:all 0.2s}
.header a:hover{background:rgba(0,0,0,0.04);color:#1a1a2e}

/* Chat */
.chat-area{position:relative;z-index:1;flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.chat-area::-webkit-scrollbar{width:4px}
.chat-area::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.4);border-radius:2px}

/* Glass Messages */
.msg{max-width:74%;animation:msgIn 0.25s ease-out;display:flex;flex-direction:column}
.msg.self{align-self:flex-end;align-items:flex-end}
.msg.other{align-self:flex-start;align-items:flex-start}
.msg .bubble{padding:9px 14px;font-size:0.9em;line-height:1.5;word-break:break-word;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.msg.self .bubble{background:rgba(244,63,94,0.82);color:#fff;border-radius:18px 18px 4px 18px}
.msg.other .bubble{background:rgba(255,255,255,0.6);color:#1a1a2e;border-radius:18px 18px 18px 4px;border:1px solid rgba(255,255,255,0.5)}

/* Result Card */
.result-card{align-self:flex-start;width:100%;max-width:500px;
  background:rgba(255,255,255,0.65);backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid rgba(255,255,255,0.5);border-radius:14px;overflow:hidden;
  animation:msgIn 0.3s ease-out;margin:4px 0}
.rc-top{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(0,0,0,0.06)}
.rc-top h3{font-size:0.85em;font-weight:700}
.rc-time{font-size:0.72em;color:#6b7280}
.rc-steps{display:flex;gap:0;padding:8px 16px;border-bottom:1px solid rgba(0,0,0,0.06)}
.rc-step{flex:1;text-align:center;padding:4px 2px;font-size:0.6em;font-weight:700;color:#9ca3af}
.rc-step .si{font-size:1.2em;display:block}
.rc-step.done{color:#1a1a2e}
.rc-body{padding:12px 16px;font-size:0.82em;line-height:1.55;color:#4b5563}

/* Typing */
.typing{align-self:flex-start;display:flex;align-items:center;gap:3px;padding:10px 14px;
  background:rgba(255,255,255,0.5);backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  border-radius:18px;animation:msgIn 0.2s ease-out}
.typing span{width:6px;height:6px;border-radius:50%;background:#9ca3af;animation:typingBounce 1.3s ease-in-out infinite}
.typing span:nth-child(2){animation-delay:0.16s}
.typing span:nth-child(3){animation-delay:0.32s}

/* Input */
.input-area{position:relative;z-index:2;
  background:rgba(255,255,255,0.5);backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  padding:10px 14px;flex-shrink:0}
.input-row{max-width:680px;margin:0 auto;display:flex;gap:8px;align-items:flex-end}
.input-row textarea{flex:1;background:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.5);color:#1a1a2e;padding:10px 16px;border-radius:20px;font-size:0.88em;font-family:inherit;resize:none;outline:none;min-height:40px;max-height:100px;line-height:1.4;transition:all 0.2s}
.input-row textarea:focus{background:rgba(255,255,255,0.7);border-color:rgba(244,63,94,0.5)}
.input-row button{width:40px;height:40px;border-radius:50%;background:#f43f5e;color:#fff;border:none;font-size:1em;cursor:pointer;flex-shrink:0;transition:transform 0.15s,opacity 0.15s;display:flex;align-items:center;justify-content:center}
.input-row button:hover{transform:scale(1.08)}
.input-row button:disabled{opacity:0.4;cursor:not-allowed;transform:none}

/* Welcome */
.welcome{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.welcome-avatar{width:68px;height:68px;border-radius:50%;
  background:linear-gradient(135deg,#f43f5e,#e94560);
  display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:2em;margin-bottom:14px;
  box-shadow:0 8px 32px rgba(244,63,94,0.25)}
.welcome p{color:rgba(26,26,46,0.55);font-size:0.85em;max-width:260px;line-height:1.5}

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
    <div class="welcome-avatar">A</div>
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
    if(d.status!=='success'){addMsg('Sorry, system error','other');toggleSend(false);inp.focus();return}
    ctx=d.conversation_context||'';
    if(d.sales_confirmed){addResult(d)}else{const reply=ctx.replace(/\[NB:\w+\]\n?/g,'').split('\nAetox: ').pop()||'';if(reply)addMsg(reply,'other')}
  }catch(e){typingEl.remove();addMsg('Connection error','other')}
  toggleSend(false);inp.focus()
}

function addMsg(t,role){const d=document.createElement('div');d.className='msg '+role;d.innerHTML=`<div class="bubble">${esc(t)}</div>`;ca.appendChild(d);ca.scrollTop=ca.scrollHeight}
function addTyping(){const d=document.createElement('div');d.className='typing';d.innerHTML='<span></span><span></span><span></span>';ca.appendChild(d);ca.scrollTop=ca.scrollHeight;return d}

function addResult(d){
  const agents=d.agents_used||[],steps=A.map(a=>`<div class="rc-step${agents.includes(a)?' done':''}"><span class="si">${I[a]}</span>${N[a]}</div>`).join('');
  const summary=(d.results||{}).data?.summary||d.output?.slice(0,250)||'';
  const card=document.createElement('div');card.innerHTML=`
    <div class="result-card">
      <div class="rc-top"><h3>✓ Complete</h3><span class="rc-time">${d.elapsed_ms}ms</span></div>
      <div class="rc-steps">${steps}</div>
      <div class="rc-body">${esc(summary)}</div>
    </div>`;
  ca.appendChild(card.firstElementChild);ca.scrollTop=ca.scrollHeight
}

function toggleSend(v){btn.disabled=v;inp.disabled=v}
function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
inp.addEventListener('input',()=>{inp.style.height='40px';inp.style.height=Math.min(inp.scrollHeight,100)+'px'})
</script>
</body>
</html>"""
