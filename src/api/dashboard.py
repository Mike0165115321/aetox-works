"""
Aetox Works — Admin Dashboard v2
System management: leads, content, projects, metrics
"""
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Admin</title>
<style>
:root{
  --bg:#f7f8fc;--surface:#fff;--card:#fff;--border:#e4e7f0;
  --ink:#1a1a2e;--muted:#7c80a0;--accent:#f43f5e;
  --green:#10b981;--amber:#f59e0b;--blue:#6366f1;--purple:#8b5cf6;
  --radius:12px;--shadow:0 1px 3px rgba(0,0,0,0.04),0 1px 2px rgba(0,0,0,0.03);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Noto Sans Thai','Segoe UI',system-ui,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.6;
  -webkit-font-smoothing:antialiased;
}

/* Header */
.header{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:0 28px;height:58px;display:flex;align-items:center;
  justify-content:space-between;position:sticky;top:0;z-index:10;
}
.header h1{font-size:1.05em;font-weight:700;display:flex;align-items:center;gap:8px}
.header h1 span{color:var(--accent)}
.nav{display:flex;align-items:center;gap:8px;font-size:0.85em}
.nav a{color:var(--muted);text-decoration:none;font-weight:500;transition:color 0.15s}
.nav a:hover{color:var(--ink)}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:4px}
.uptime{color:var(--muted);font-size:0.8em}

.main{max-width:1160px;margin:0 auto;padding:24px 28px}

/* Stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}
.stat{
  background:var(--card);border-radius:var(--radius);padding:20px 22px;
  box-shadow:var(--shadow);border:1px solid var(--border);
  transition:transform 0.2s,box-shadow 0.2s;
}
.stat:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.06)}
.stat-label{font-size:0.75em;color:var(--muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:6px}
.stat-val{font-size:2em;font-weight:800;letter-spacing:-0.02em}
.stat-sub{font-size:0.78em;color:var(--muted);margin-top:2px}

/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:20px;border-bottom:2px solid var(--border)}
.tab{
  padding:10px 22px;cursor:pointer;border:none;background:none;
  font-size:0.85em;font-weight:600;color:var(--muted);
  border-bottom:2px solid transparent;margin-bottom:-2px;
  transition:color 0.2s,border-color 0.2s;
}
.tab:hover{color:var(--ink)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-content{display:none}
.tab-content.active{display:block}

/* Panel */
.panel{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);border:1px solid var(--border);padding:24px}

/* Table */
table{width:100%;border-collapse:collapse;font-size:0.88em}
th{text-align:left;padding:10px 14px;border-bottom:2px solid var(--border);color:var(--muted);font-weight:600;font-size:0.75em;text-transform:uppercase;letter-spacing:0.04em}
td{padding:11px 14px;border-bottom:1px solid var(--border)}
tr:hover td{background:#fafbfd}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.72em;font-weight:700}
.badge-new{background:#eef2ff;color:var(--blue)}
.badge-contacted{background:#fef9e7;color:var(--amber)}
.badge-qualified{background:#ecfdf5;color:var(--green)}
.badge-closed{background:#f3f4f6;color:var(--muted)}

/* Content Grid */
.content-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.content-card{
  background:var(--card);border-radius:var(--radius);padding:20px;
  box-shadow:var(--shadow);border:1px solid var(--border);
  border-left:3px solid var(--blue);transition:transform 0.2s,box-shadow 0.2s;
}
.content-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.06)}
.content-card.landing{border-left-color:var(--accent)}
.content-card.blog{border-left-color:var(--blue)}
.content-card.social{border-left-color:var(--purple)}
.content-card h4{font-size:0.95em;margin-bottom:4px}
.content-card .meta{font-size:0.78em;color:var(--muted);margin-bottom:8px}
.content-card .preview{font-size:0.83em;color:var(--muted);line-height:1.55;max-height:70px;overflow:hidden}

/* Projects */
.project-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
.project-card{
  background:var(--card);border-radius:var(--radius);padding:22px 18px;
  box-shadow:var(--shadow);border:1px solid var(--border);text-align:center;
  transition:transform 0.2s,box-shadow 0.2s;
}
.project-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.06)}
.project-card .icon{font-size:2em;margin-bottom:8px}
.project-card h4{font-size:0.85em;margin-bottom:4px}
.project-card .count{font-size:0.75em;color:var(--muted)}

/* Notebooks */
.nb-list{display:flex;flex-direction:column;gap:8px}
.nb-item{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;background:var(--card);border-radius:8px;border:1px solid var(--border);cursor:pointer;transition:border-color 0.2s,box-shadow 0.2s}
.nb-item:hover{border-color:var(--accent);box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.nb-item .nb-title{font-weight:600;font-size:0.9em}
.nb-item .nb-meta{font-size:0.78em;color:var(--muted)}
.nb-status{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.72em;font-weight:700}
.nb-status.in_progress{background:#fef9e7;color:var(--amber)}
.nb-status.confirmed{background:#ecfdf5;color:var(--green)}
.nb-viewer{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;font-family:monospace;font-size:0.84em;line-height:1.7;white-space:pre-wrap;max-height:600px;overflow-y:auto;margin-top:12px}
.nb-back{cursor:pointer;color:var(--accent);font-weight:600;font-size:0.85em;margin-bottom:12px;display:inline-block}

/* Search */
.search{width:100%;max-width:320px;padding:9px 14px;border:1px solid var(--border);border-radius:8px;font-size:0.85em;outline:none;margin-bottom:14px;font-family:inherit;transition:border-color 0.2s}
.search:focus{border-color:var(--accent)}

/* Empty */
.empty{text-align:center;padding:48px 20px;color:var(--muted)}
.empty .icon{font-size:2.5em;margin-bottom:8px}
.empty p{font-size:0.9em}

/* Quick bar */
.qbar{display:flex;gap:10px;margin-bottom:20px;align-items:center}
.qbar .btn{
  padding:8px 20px;border-radius:8px;font-size:0.83em;font-weight:600;
  cursor:pointer;border:none;text-decoration:none;
  transition:transform 0.15s,box-shadow 0.15s;
  display:inline-flex;align-items:center;gap:6px;
}
.qbar .btn:hover{transform:translateY(-1px)}
.btn-accent{background:var(--accent);color:#fff}
.btn-accent:hover{box-shadow:0 4px 14px rgba(244,63,94,0.3)}
.btn-ghost{background:var(--surface);color:var(--ink);border:1px solid var(--border)}

@media(max-width:768px){
  .header{padding:0 16px}
  .main{padding:16px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .content-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div class="header">
  <h1><span>⚡</span> Aetox Admin</h1>
  <div class="nav">
    <span class="status-dot"></span><span class="uptime" id="uptime">--</span>
    <span style="margin:0 8px;color:var(--border)">|</span>
    <a href="/">Chat</a>
  </div>
</div>

<div class="main">

  <div class="stats">
    <div class="stat"><div class="stat-label">Leads</div><div class="stat-val" id="statLeads">-</div><div class="stat-sub">CRM records</div></div>
    <div class="stat"><div class="stat-label">Drafts</div><div class="stat-val" id="statDrafts">-</div><div class="stat-sub">Content pieces</div></div>
    <div class="stat"><div class="stat-label">Projects</div><div class="stat-val" id="statProjects">-</div><div class="stat-sub">Built pages</div></div>
    <div class="stat"><div class="stat-label">Uptime</div><div class="stat-val" id="statUptime" style="font-size:1.5em">-</div><div class="stat-sub">Server running</div></div>
  </div>

  <div class="qbar">
    <a href="/" class="btn btn-accent">Back to Chat</a>
    <button class="btn btn-ghost" onclick="refresh()">Refresh</button>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="overview">Overview</button>
    <button class="tab" data-tab="leads">Leads</button>
    <button class="tab" data-tab="content">Content</button>
    <button class="tab" data-tab="projects">Projects</button>
    <button class="tab" data-tab="notebooks">📓 Notebooks</button>
  </div>

  <div class="tab-content active" id="t-overview"><div class="panel" id="overviewPanel">Loading...</div></div>
  <div class="tab-content" id="t-leads"><input class="search" id="leadSearch" placeholder="Search leads..." oninput="renderLeads()"><div class="panel" id="leadsPanel">Loading...</div></div>
  <div class="tab-content" id="t-content"><div class="panel" id="contentPanel">Loading...</div></div>
  <div class="tab-content" id="t-projects"><div class="panel" id="projectsPanel">Loading...</div></div>
  <div class="tab-content" id="t-notebooks"><div class="panel" id="notebooksPanel">Loading...</div></div>

</div>

<script>
let S={leads:[],drafts:[],projects:[],uptime:0,metrics:{}};

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');document.getElementById('t-'+t.dataset.tab).classList.add('active');
  }));
  refresh();setInterval(refreshStats,20000);
});

async function refresh(){await Promise.all([fLeads(),fDrafts(),fProjects(),fNotebooks(),fStatus()]);renderAll()}
async function refreshStats(){await fStatus();renderStats()}
async function fJSON(u){try{const r=await fetch(u);return await r.json()}catch(e){return{success:false}}}
async function fLeads(){const r=await fJSON('/api/leads?limit=200');if(r.success)S.leads=r.data}
async function fDrafts(){const r=await fJSON('/api/drafts?limit=200');if(r.success)S.drafts=r.data}
async function fProjects(){const r=await fJSON('/api/projects');if(r.success)S.projects=r.data}
async function fStatus(){const r=await fJSON('/status');S.metrics=r.metrics||{};S.uptime=r.uptime_seconds||0;
  document.getElementById('uptime').textContent=fmtTime(S.uptime)}
let notebooksData=[];
async function fNotebooks(){const r=await fJSON('/api/notebooks');if(r.success)notebooksData=r.data}

function renderAll(){renderStats();renderOverview();renderLeads();renderContent();renderProjects();renderNotebooks()}

function renderStats(){
  document.getElementById('statLeads').textContent=S.leads.length;
  document.getElementById('statDrafts').textContent=S.drafts.length;
  document.getElementById('statProjects').textContent=S.projects.length;
  document.getElementById('statUptime').textContent=fmtTime(S.uptime);
}

function renderOverview(){
  const m=S.metrics;const items=Object.entries(m).length
    ?Object.entries(m).map(([k,v])=>`<tr><td style="font-weight:600">${esc(k)}</td><td>${v}</td></tr>`).join('')
    :'<tr><td colspan="2" style="color:var(--muted);text-align:center;padding:20px">No metrics yet. Run the pipeline to generate data.</td></tr>';
  document.getElementById('overviewPanel').innerHTML=`
    <h3 style="font-size:0.95em;margin-bottom:14px">System Metrics</h3>
    <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>${items}</tbody></table>
    <p style="margin-top:14px;color:var(--muted);font-size:0.82em">Leads: ${S.leads.length} &middot; Drafts: ${S.drafts.length} &middot; Projects: ${S.projects.length}</p>`;
}

function renderLeads(){
  const q=(document.getElementById('leadSearch')?.value||'').toLowerCase();
  const list=S.leads.filter(l=>!q||(l.name||'').toLowerCase().includes(q)||(l.company||'').toLowerCase().includes(q));
  if(!list.length){document.getElementById('leadsPanel').innerHTML='<div class="empty"><div class="icon">👥</div><p>No leads yet</p></div>';return}
  document.getElementById('leadsPanel').innerHTML=`<table><thead><tr><th>ID</th><th>Name</th><th>Company</th><th>Status</th><th>Summary</th><th>Date</th></tr></thead><tbody>${
    list.map(l=>`<tr><td><strong>#${l.id}</strong></td><td>${esc(l.name)||'<span style="color:var(--muted)">-</span>'}</td><td>${esc(l.company)||'-'}</td><td><span class="badge badge-${l.status||'new'}">${l.status||'new'}</span></td><td style="max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(l.summary||'')}</td><td>${(l.created_at||'').slice(0,10)}</td></tr>`).join('')
  }</tbody></table>`;
}

function renderContent(){
  if(!S.drafts.length){document.getElementById('contentPanel').innerHTML='<div class="empty"><div class="icon">✍️</div><p>No drafts yet</p></div>';return}
  document.getElementById('contentPanel').innerHTML=`<div class="content-grid">${
    S.drafts.map(d=>`<div class="content-card ${d.content_type||'landing'}"><h4>${esc(d.title)||'Untitled'}</h4><div class="meta">${d.content_type||'landing'} · ${d.tone||'-'} · ${(d.created_at||'').slice(0,10)}</div><div class="preview">${esc((d.body||'').slice(0,160))}</div></div>`).join('')
  }</div>`;
}

function renderProjects(){
  if(!S.projects.length){document.getElementById('projectsPanel').innerHTML='<div class="empty"><div class="icon">🌐</div><p>No projects built yet</p></div>';return}
  document.getElementById('projectsPanel').innerHTML=`<div class="project-grid">${
    S.projects.map(p=>`<div class="project-card"><div class="icon">🌐</div><h4>${esc(p.name)}</h4><div class="count">${p.files?.length||0} files</div></div>`).join('')
  }</div>`;
}

function renderNotebooks(){
  if(!notebooksData.length){document.getElementById('notebooksPanel').innerHTML='<div class="empty"><div class="icon">📓</div><p>No notebooks yet. Start a chat conversation first.</p></div>';return}
  document.getElementById('notebooksPanel').innerHTML=`
    <div class="nb-list">${
      notebooksData.map(n=>`
        <div class="nb-item" onclick="viewNotebook('${n.id}')">
          <div>
            <div class="nb-title">📓 ${esc(n.title)}</div>
            <div class="nb-meta">ID: ${n.id} · ${(n.size||0)} bytes</div>
          </div>
          <span class="nb-status ${n.status}">${n.status==='confirmed'?'✅ Confirmed':'🟡 Active'}</span>
        </div>
      `).join('')
    }</div>`;
}

async function viewNotebook(id){
  document.getElementById('notebooksPanel').innerHTML='<div class="loading">Loading...</div>';
  const r=await fJSON('/api/notebooks/'+id);
  if(!r.success){document.getElementById('notebooksPanel').innerHTML='<div class="empty">Notebook not found</div>';return}
  document.getElementById('notebooksPanel').innerHTML=`
    <div class="nb-back" onclick="renderNotebooks()">← Back to list</div>
    <div class="nb-viewer">${esc(r.data)}</div>`;
}

function esc(s){return(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function fmtTime(s){const h=Math.floor(s/3600),m=Math.floor((s%3600)/60);return h>0?`${h}h ${m}m`:`${m}m`}
</script>
</body>
</html>"""
