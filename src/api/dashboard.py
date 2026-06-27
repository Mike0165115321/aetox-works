"""
Aetox Works — Admin Dashboard v3
Product register: data-dense, clean, professional
Seed: oklch(0.700 0.130 60.0) orange/honey
"""
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Admin</title>
<style>
:root{
  --bg:#f5f6fa;--surface:#fff;--ink:#1a1a2e;--muted:#6b7280;
  --border:#e5e7ec;--accent:#f43f5e;--accent2:#6366f1;
  --green:#10b981;--amber:#f59e0b;--radius:10px;
  --shadow:0 1px 3px rgba(0,0,0,0.04);
  --shadow-hover:0 4px 16px rgba(0,0,0,0.06);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Noto Sans Thai',system-ui,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.6;
  -webkit-font-smoothing:antialiased;
}

/* Top Bar */
.topbar{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:0 24px;height:54px;display:flex;align-items:center;
  justify-content:space-between;position:sticky;top:0;z-index:10;
}
.topbar-left{display:flex;align-items:center;gap:12px}
.topbar h1{font-size:1em;font-weight:700}
.topbar .dot{width:8px;height:8px;border-radius:50%;background:var(--green)}
.topbar nav{display:flex;gap:4px;font-size:0.84em}
.topbar nav a{color:var(--muted);text-decoration:none;padding:6px 14px;border-radius:6px;font-weight:500;transition:all 0.2s}
.topbar nav a:hover{color:var(--ink);background:rgba(0,0,0,0.03)}
.topbar nav a.active{color:var(--accent);background:rgba(244,63,94,0.06)}

/* Main */
.main{max-width:1120px;margin:0 auto;padding:20px 24px}

/* Stats Grid */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.stat{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:16px 20px;transition:transform 0.2s,box-shadow 0.2s;
}
.stat:hover{transform:translateY(-1px);box-shadow:var(--shadow-hover)}
.stat-label{font-size:0.7em;color:var(--muted);text-transform:uppercase;letter-spacing:0.05em;font-weight:600;margin-bottom:4px}
.stat-val{font-size:2em;font-weight:800;letter-spacing:-0.02em;line-height:1.1}
.stat-sub{font-size:0.72em;color:var(--muted);margin-top:2px}

/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:16px;border-bottom:2px solid var(--border)}
.tab{
  padding:9px 20px;cursor:pointer;border:none;background:none;
  font-size:0.83em;font-weight:600;color:var(--muted);
  border-bottom:2px solid transparent;margin-bottom:-2px;
  transition:color 0.2s,border-color 0.2s;
}
.tab:hover{color:var(--ink)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-content{display:none;animation:fadeIn 0.3s ease}
.tab-content.active{display:block}

/* Panel */
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}
.panel-header{padding:14px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.panel-header h3{font-size:0.9em;font-weight:700}
.panel-body{padding:20px}

/* Table */
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:0.84em}
th{text-align:left;padding:10px 14px;border-bottom:2px solid var(--border);color:var(--muted);font-weight:600;font-size:0.7em;text-transform:uppercase;letter-spacing:0.04em;white-space:nowrap}
td{padding:10px 14px;border-bottom:1px solid var(--border)}
tr:hover td{background:#fafbfd}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.7em;font-weight:700}
.badge-new{background:#eef2ff;color:var(--accent2)}
.badge-contacted{background:#fef9e7;color:var(--amber)}
.badge-qualified{background:#ecfdf5;color:var(--green)}
.badge-closed{background:#f3f4f6;color:var(--muted)}

/* Search */
.search{width:220px;padding:7px 12px;border:1px solid var(--border);border-radius:6px;font-size:0.82em;outline:none;font-family:inherit;transition:border-color 0.2s}
.search:focus{border-color:var(--accent2)}

/* Cards Grid */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:18px;transition:transform 0.2s,box-shadow 0.2s;
}
.card:hover{transform:translateY(-1px);box-shadow:var(--shadow-hover)}
.card.landing{border-left:3px solid var(--accent)}
.card.blog{border-left:3px solid var(--accent2)}
.card.social{border-left:3px solid #8b5cf6}
.card h4{font-size:0.9em;margin-bottom:4px}
.card .meta{font-size:0.72em;color:var(--muted);margin-bottom:8px}
.card .preview{font-size:0.8em;color:var(--muted);line-height:1.5;max-height:60px;overflow:hidden}

/* Projects */
.project-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.project-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:20px 14px;text-align:center;transition:transform 0.2s;
}
.project-card:hover{transform:translateY(-2px)}
.project-card .icon{font-size:1.8em;margin-bottom:6px}
.project-card h4{font-size:0.8em;margin-bottom:2px}
.project-card .count{font-size:0.7em;color:var(--muted)}

/* Notebooks */
.nb-list{display:flex;flex-direction:column;gap:6px}
.nb-item{
  display:flex;align-items:center;justify-content:space-between;padding:12px 16px;
  background:var(--surface);border:1px solid var(--border);border-radius:8px;
  cursor:pointer;transition:border-color 0.2s;
}
.nb-item:hover{border-color:var(--accent2)}
.nb-title{font-weight:600;font-size:0.85em}
.nb-meta{font-size:0.72em;color:var(--muted)}
.nb-status{font-size:0.68em;font-weight:700;padding:2px 8px;border-radius:10px}
.nb-status.active{background:#fef9e7;color:var(--amber)}
.nb-status.confirmed{background:#ecfdf5;color:var(--green)}
.nb-viewer{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;font-family:monospace;font-size:0.8em;line-height:1.7;white-space:pre-wrap;max-height:500px;overflow-y:auto;margin-top:12px}
.nb-back{cursor:pointer;color:var(--accent2);font-weight:600;font-size:0.8em;margin-bottom:10px;display:inline-block}

/* Pipeline Section */
.pl-section{margin-top:20px}
.pl-steps-row{display:flex;gap:4px;margin:8px 0}
.pl-step-badge{padding:3px 10px;border-radius:6px;font-size:0.7em;font-weight:700}
.pl-step-badge.done{background:#ecfdf5;color:var(--green)}
.pl-step-badge.pending{background:#f3f4f6;color:var(--muted)}
.pl-details details{margin-top:4px}
.pl-details summary{font-size:0.78em;font-weight:600;cursor:pointer;padding:2px 0}
.pl-details .content{padding:2px 0 2px 12px;font-size:0.75em;color:var(--muted)}

/* Empty */
.empty{text-align:center;padding:40px 20px;color:var(--muted)}
.empty .icon{font-size:2.2em;margin-bottom:6px}
.empty p{font-size:0.85em}

/* Skeleton loading */
.skeleton{background:linear-gradient(90deg,var(--border) 25%,#eef0f5 50%,var(--border) 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:4px}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

@media(max-width:768px){
  .topbar{padding:0 14px}
  .main{padding:14px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .cards{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-left">
    <span class="dot"></span><h1>Aetox Admin</h1>
  </div>
  <nav>
    <a href="/">Chat</a>
    <a href="/admin" class="active">Admin</a>
    <a href="/docs">API</a>
  </nav>
</div>

<div class="main">

  <div class="stats">
    <div class="stat"><div class="stat-label">Leads</div><div class="stat-val" id="s-leads">-</div></div>
    <div class="stat"><div class="stat-label">Drafts</div><div class="stat-val" id="s-drafts">-</div></div>
    <div class="stat"><div class="stat-label">Projects</div><div class="stat-val" id="s-projects">-</div></div>
    <div class="stat"><div class="stat-label">Uptime</div><div class="stat-val" id="s-uptime" style="font-size:1.4em">-</div></div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="overview">Overview</button>
    <button class="tab" data-tab="leads">Leads</button>
    <button class="tab" data-tab="content">Content</button>
    <button class="tab" data-tab="projects">Projects</button>
    <button class="tab" data-tab="notebooks">Notebooks</button>
  </div>

  <div class="tab-content active" id="t-overview">
    <div class="panel"><div class="panel-body" id="overviewBody">Loading...</div></div>
  </div>
  <div class="tab-content" id="t-leads">
    <div class="panel">
      <div class="panel-header"><h3>All Leads</h3><input class="search" id="leadSearch" placeholder="Search..." oninput="renderLeads()"></div>
      <div class="table-wrap"><table id="leadsTable"><tbody><tr><td colspan="6" style="text-align:center;padding:40px">Loading...</td></tr></tbody></table></div>
    </div>
  </div>
  <div class="tab-content" id="t-content">
    <div class="panel"><div class="panel-body" id="contentBody">Loading...</div></div>
  </div>
  <div class="tab-content" id="t-projects">
    <div class="panel"><div class="panel-body" id="projectsBody">Loading...</div></div>
  </div>
  <div class="tab-content" id="t-notebooks">
    <div class="panel"><div class="panel-body" id="notebooksBody">Loading...</div></div>
  </div>

</div>

<script>
const A=['sales','research','content','dev','data'];
const N={sales:'Sales',research:'Research',content:'Content',dev:'Dev',data:'Data'};
let S={leads:[],drafts:[],projects:[],notebooks:[],uptime:0,metrics:{}};

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');document.getElementById('t-'+t.dataset.tab).classList.add('active');
  }));
  refresh();setInterval(refresh,20000);
});

async function refresh(){
  await Promise.all([f('/api/leads?limit=200',d=>S.leads=d.data||[]),
    f('/api/drafts?limit=200',d=>S.drafts=d.data||[]),
    f('/api/projects',d=>S.projects=d.data||[]),
    f('/api/notebooks',d=>S.notebooks=d.data||[]),
    f('/status',d=>{S.metrics=d.metrics||{};S.uptime=d.uptime_seconds||0})]);
  renderAll()
}
async function f(url,cb){try{const r=await fetch(url);const d=await r.json();cb(d)}catch(e){}}

function renderAll(){
  document.getElementById('s-leads').textContent=S.leads.length;
  document.getElementById('s-drafts').textContent=S.drafts.length;
  document.getElementById('s-projects').textContent=S.projects.length;
  document.getElementById('s-uptime').textContent=fmt(S.uptime);
  renderOverview();renderLeads();renderContent();renderProjects();renderNotebooks();
}

function renderOverview(){
  const m=S.metrics,items=Object.entries(m).map(([k,v])=>`<tr><td style="font-weight:600">${esc(k)}</td><td>${v}</td></tr>`).join('')||'<tr><td colspan="2" style="color:var(--muted);text-align:center;padding:20px">No metrics yet</td></tr>';
  document.getElementById('overviewBody').innerHTML=`
    <h3 style="font-size:0.9em;margin-bottom:12px">System Metrics</h3>
    <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>${items}</tbody></table>
    <div id="lastPipeline"></div>`;
  f('/api/last-pipeline',d=>{
    if(!d.data)return;
    const p=d.data,steps=A.map(a=>`<span class="pl-step-badge ${(p.agents_used||[]).includes(a)?'done':'pending'}">${N[a]}</span>`).join('');
    const details=A.filter(a=>(p.agents_used||[]).includes(a)).map(a=>{
      const r=(p.results||{})[a]||{};let t='';
      if(a==='sales')t=`Lead #${r.lead_id||'?'}`;
      else if(a==='research')t=`Sources: ${r.sources||0}`;
      else if(a==='content')t=`Draft #${r.draft_id||'?'} — ${r.title||''}`;
      else if(a==='dev')t=`${(r.files||[]).length||0} files`;
      else if(a==='data')t=r.summary||'';
      return `<details><summary>${N[a]}</summary><div class="content">${esc(t)}</div></details>`;
    }).join('');
    document.getElementById('lastPipeline').innerHTML=`
      <h3 style="font-size:0.85em;margin-top:18px;margin-bottom:8px">Last Pipeline</h3>
      <div style="font-size:0.75em;color:var(--muted);margin-bottom:6px">${esc(p.input||'')} · ${p.elapsed_ms}ms</div>
      <div class="pl-steps-row">${steps}</div>
      <div class="pl-details">${details}</div>`;
  });
}

function renderLeads(){
  const q=(document.getElementById('leadSearch')?.value||'').toLowerCase();
  const list=S.leads.filter(l=>!q||(l.name||'').toLowerCase().includes(q)||(l.company||'').toLowerCase().includes(q));
  if(!list.length){
    document.getElementById('leadsTable').innerHTML='<tbody><tr><td colspan="6"><div class="empty"><div class="icon">👥</div><p>No leads yet</p></div></td></tr></tbody>';return
  }
  document.getElementById('leadsTable').innerHTML=`<thead><tr><th>ID</th><th>Name</th><th>Company</th><th>Status</th><th>Summary</th><th>Date</th></tr></thead><tbody>${
    list.map(l=>`<tr><td><strong>#${l.id}</strong></td><td>${esc(l.name)||'<span style="color:var(--muted)">-</span>'}</td><td>${esc(l.company)||'-'}</td><td><span class="badge badge-${l.status||'new'}">${l.status||'new'}</span></td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(l.summary||'')}</td><td>${(l.created_at||'').slice(0,10)}</td></tr>`).join('')
  }</tbody>`;
}

function renderContent(){
  if(!S.drafts.length){document.getElementById('contentBody').innerHTML='<div class="empty"><div class="icon">✍️</div><p>No drafts yet</p></div>';return}
  document.getElementById('contentBody').innerHTML=`<div class="cards">${
    S.drafts.map(d=>`<div class="card ${d.content_type||'landing'}"><h4>${esc(d.title)||'Untitled'}</h4><div class="meta">${d.content_type||'landing'} · ${d.tone||'-'} · ${(d.created_at||'').slice(0,10)}</div><div class="preview">${esc((d.body||'').slice(0,140))}</div></div>`).join('')
  }</div>`;
}

function renderProjects(){
  if(!S.projects.length){document.getElementById('projectsBody').innerHTML='<div class="empty"><div class="icon">🌐</div><p>No projects yet</p></div>';return}
  document.getElementById('projectsBody').innerHTML=`<div class="project-grid">${
    S.projects.map(p=>`<div class="project-card"><div class="icon">🌐</div><h4>${esc(p.name)}</h4><div class="count">${p.files?.length||0} files</div></div>`).join('')
  }</div>`;
}

function renderNotebooks(){
  if(!S.notebooks.length){document.getElementById('notebooksBody').innerHTML='<div class="empty"><div class="icon">📓</div><p>No notebooks yet</p></div>';return}
  document.getElementById('notebooksBody').innerHTML=`<div class="nb-list">${
    S.notebooks.map(n=>`<div class="nb-item" onclick="viewNotebook('${n.id}')"><div><div class="nb-title">📓 ${esc(n.title)}</div><div class="nb-meta">ID: ${n.id}</div></div><span class="nb-status ${n.status==='confirmed'?'confirmed':'active'}">${n.status==='confirmed'?'Confirmed':'Active'}</span></div>`).join('')
  }</div>`;
}

async function viewNotebook(id){
  document.getElementById('notebooksBody').innerHTML='<div style="text-align:center;padding:20px;color:var(--muted)">Loading...</div>';
  const r=await (await fetch('/api/notebooks/'+id)).json();
  if(!r.success){renderNotebooks();return}
  document.getElementById('notebooksBody').innerHTML=`<div class="nb-back" onclick="renderNotebooks()">← Back</div><div class="nb-viewer">${esc(r.data)}</div>`;
}

function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function fmt(s){const h=Math.floor(s/3600),m=Math.floor((s%3600)/60);return h>0?`${h}h ${m}m`:`${m}m`}
</script>
</body>
</html>"""
