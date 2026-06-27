"""
Aetox Works — Unified Dashboard HTML
Single-page app with tabs: Overview | Chat | Leads | Content | Projects
Served at GET / by the API server
"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Works — Dashboard</title>
<style>
:root {
  --bg: #f8f9fb; --surface: #ffffff; --ink: #1a1a2e;
  --muted: #e8eaf0; --accent: #e94560; --accent2: #6366f1;
  --green: #10b981; --amber: #f59e0b; --red: #ef4444;
  --radius: 10px; --shadow: 0 1px 3px rgba(0,0,0,0.06);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Noto Sans Thai', 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--ink); line-height: 1.6; }

/* Layout */
.topbar { background: var(--surface); border-bottom: 1px solid var(--muted);
          padding: 0 24px; display: flex; align-items: center; justify-content: space-between;
          height: 56px; position: sticky; top: 0; z-index: 10; }
.topbar h1 { font-size: 1.1em; font-weight: 700; }
.topbar .health { display: flex; align-items: center; gap: 12px; font-size: 0.85em; color: #666; }
.health-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); }
.main { max-width: 1200px; margin: 0 auto; padding: 20px 24px; }

/* Stats Row */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
         gap: 14px; margin-bottom: 20px; }
.stat-card { background: var(--surface); border-radius: var(--radius);
             padding: 18px 20px; box-shadow: var(--shadow); }
.stat-label { font-size: 0.8em; color: #888; text-transform: uppercase;
              letter-spacing: 0.05em; margin-bottom: 4px; }
.stat-val { font-size: 2em; font-weight: 800; }
.stat-sub { font-size: 0.8em; color: #888; margin-top: 2px; }

/* Tabs */
.tabs { display: flex; gap: 2px; margin-bottom: 20px; border-bottom: 2px solid var(--muted); }
.tab { padding: 10px 20px; cursor: pointer; border: none; background: none;
       font-size: 0.9em; font-weight: 600; color: #888;
       border-bottom: 2px solid transparent; margin-bottom: -2px;
       transition: color 0.2s, border-color 0.2s; }
.tab:hover { color: var(--ink); }
.tab.active { color: var(--accent); border-bottom-color: var(--accent); }

/* Tab Content */
.tab-content { display: none; }
.tab-content.active { display: block; }

/* Cards / Panels */
.panel { background: var(--surface); border-radius: var(--radius);
         box-shadow: var(--shadow); padding: 24px; margin-bottom: 16px; }

/* Table */
table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
th { text-align: left; padding: 10px 12px; border-bottom: 2px solid var(--muted);
     color: #888; font-weight: 600; font-size: 0.8em; text-transform: uppercase; }
td { padding: 10px 12px; border-bottom: 1px solid var(--muted); }
tr:hover { background: #fafbfc; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px;
         font-size: 0.75em; font-weight: 700; }
.badge-new { background: #dbeafe; color: #2563eb; }
.badge-contacted { background: #fef3c7; color: #d97706; }
.badge-qualified { background: #d1fae5; color: #059669; }
.badge-closed { background: #e5e7eb; color: #6b7280; }

/* Chat */
.chat-panel { display: flex; flex-direction: column; height: 500px; }
.chat-msgs { flex: 1; overflow-y: auto; padding: 12px 0; display: flex;
             flex-direction: column; gap: 8px; }
.msg { max-width: 75%; padding: 10px 16px; border-radius: 16px;
       font-size: 0.9em; line-height: 1.5; white-space: pre-wrap; }
.msg.user { align-self: flex-end; background: var(--accent); color: #fff;
            border-bottom-right-radius: 4px; }
.msg.bot { align-self: flex-start; background: var(--muted); color: var(--ink);
           border-bottom-left-radius: 4px; }
.chat-input { display: flex; gap: 8px; padding-top: 12px; border-top: 1px solid var(--muted); }
.chat-input input { flex: 1; padding: 10px 14px; border: 1px solid var(--muted);
                    border-radius: 10px; font-size: 0.9em; outline: none; }
.chat-input input:focus { border-color: var(--accent); }
.chat-input button { padding: 10px 20px; background: var(--accent); color: #fff;
                     border: none; border-radius: 10px; font-weight: 600; cursor: pointer; }
.chat-input button:disabled { opacity: 0.6; cursor: not-allowed; }
.typing { align-self: flex-start; color: #888; font-size: 0.85em; padding: 6px 12px; }

/* Content Grid */
.content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 14px; }
.content-card { background: var(--surface); border-radius: var(--radius);
                padding: 20px; box-shadow: var(--shadow);
                border-left: 3px solid var(--accent2); }
.content-card.landing { border-left-color: var(--accent); }
.content-card.blog { border-left-color: var(--accent2); }
.content-card h4 { font-size: 1em; margin-bottom: 6px; }
.content-card .meta { font-size: 0.8em; color: #888; }
.content-card .body-preview { font-size: 0.85em; color: #555; margin-top: 8px;
                               max-height: 80px; overflow: hidden; }

/* Projects */
.project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 14px; }
.project-card { background: var(--surface); border-radius: var(--radius);
                padding: 20px; box-shadow: var(--shadow); text-align: center; }
.project-card .icon { font-size: 2em; margin-bottom: 8px; }
.project-card h4 { font-size: 0.9em; }
.project-card a { color: var(--accent2); font-size: 0.8em; text-decoration: none; }

/* Empty State */
.empty { text-align: center; padding: 40px; color: #aaa; }
.empty .icon { font-size: 2.5em; margin-bottom: 8px; }

/* Loading */
.loading { text-align: center; padding: 20px; color: #888; }

/* Search */
.search-bar { margin-bottom: 14px; }
.search-bar input { width: 100%; max-width: 360px; padding: 8px 14px;
                    border: 1px solid var(--muted); border-radius: 8px;
                    font-size: 0.9em; outline: none; }
.search-bar input:focus { border-color: var(--accent2); }

/* Quick actions */
.quick-actions { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.btn { padding: 8px 20px; border-radius: 8px; font-size: 0.85em; font-weight: 600;
       cursor: pointer; border: none; transition: transform 0.15s ease, box-shadow 0.15s ease; }
.btn:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.btn-accent { background: var(--accent); color: #fff; }
.btn-outline { background: var(--surface); color: var(--accent); border: 1.5px solid var(--accent); }

@media (max-width: 640px) {
  .topbar { padding: 0 14px; }
  .main { padding: 14px; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  .tabs { overflow-x: auto; }
}
</style>
</head>
<body>
<div class="topbar">
  <h1>🚀 Aetox Works</h1>
  <div class="health">
    <a href="/chat" style="color:var(--accent);text-decoration:none;font-weight:600;font-size:0.9em;margin-right:12px">💬 Chat</a>
    <span class="health-dot" id="healthDot"></span>
    <span id="uptime">--</span>
  </div>
</div>

<div class="main">

  <!-- Stats Row -->
  <div class="stats" id="statsRow"></div>

  <!-- Quick Actions -->
  <div class="quick-actions">
    <a href="/chat" class="btn btn-accent" style="text-decoration:none">💬 Open Chat</a>
    <button class="btn btn-outline" onclick="refreshAll()">🔄 Refresh</button>
  </div>

  <!-- Tab Nav -->
  <div class="tabs">
    <button class="tab active" data-tab="overview">📊 ภาพรวม</button>
    <button class="tab" data-tab="leads">👥 Leads</button>
    <button class="tab" data-tab="content">✍️ Content</button>
    <button class="tab" data-tab="projects">🌐 Projects</button>
  </div>

  <!-- Tab: Overview -->
  <div class="tab-content active" id="tab-overview">
    <div class="panel" id="overviewContent">กำลังโหลด...</div>
  </div>

  <!-- Tab: Leads -->
  <div class="tab-content" id="tab-leads">
    <div class="search-bar"><input id="leadSearch" placeholder="🔍 ค้นหาชื่อ/บริษัท..." oninput="renderLeads()"></div>
    <div class="panel" id="leadsTable">กำลังโหลด...</div>
  </div>

  <!-- Tab: Content -->
  <div class="tab-content" id="tab-content-tab">
    <div class="panel" id="contentGrid">กำลังโหลด...</div>
  </div>

  <!-- Tab: Projects -->
  <div class="tab-content" id="tab-projects">
    <div class="panel" id="projectsGrid">กำลังโหลด...</div>
  </div>

</div>

<script>
// ── State ──
let state = { leads: [], drafts: [], projects: [], reports: [], metrics: {}, uptime: 0 };

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  refreshAll();
  setInterval(refreshStats, 15000);
});

function setupTabs() {
  document.querySelectorAll('.tab').forEach(t => {
    t.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      document.getElementById('tab-' + t.dataset.tab).classList.add('active');
    });
  });
}

// ── Data Fetching ──
async function refreshAll() {
  await Promise.all([fetchLeads(), fetchDrafts(), fetchProjects(), fetchStatus()]);
  renderAll();
}

async function refreshStats() {
  await fetchStatus();
  renderStats();
}

async function fetchJSON(url) {
  try { const r = await fetch(url); return await r.json(); }
  catch(e) { return { success: false, error: e.message }; }
}

async function fetchLeads() {
  const r = await fetchJSON('/api/leads?limit=100');
  if (r.success) state.leads = r.data;
}
async function fetchDrafts() {
  const r = await fetchJSON('/api/drafts?limit=100');
  if (r.success) state.drafts = r.data;
}
async function fetchProjects() {
  const r = await fetchJSON('/api/projects');
  if (r.success) state.projects = r.data;
}
async function fetchStatus() {
  const r = await fetchJSON('/status');
  state.metrics = r.metrics || {};
  state.uptime = r.uptime_seconds || 0;
  document.getElementById('uptime').textContent = fmtUptime(state.uptime);
  document.getElementById('healthDot').style.background = 'var(--green)';
}

// ── Render All ──
function renderAll() {
  renderStats();
  renderOverview();
  renderLeads();
  renderContent();
  renderProjects();
}

function renderStats() {
  document.getElementById('statsRow').innerHTML = `
    <div class="stat-card"><div class="stat-label">👥 Leads</div><div class="stat-val">${state.leads.length}</div></div>
    <div class="stat-card"><div class="stat-label">✍️ Drafts</div><div class="stat-val">${state.drafts.length}</div></div>
    <div class="stat-card"><div class="stat-label">🌐 Projects</div><div class="stat-val">${state.projects.length}</div></div>
    <div class="stat-card"><div class="stat-label">⏱ Uptime</div><div class="stat-val" style="font-size:1.4em">${fmtUptime(state.uptime)}</div></div>
  `;
}

function renderOverview() {
  const m = state.metrics;
  const metricItems = Object.entries(m).length
    ? Object.entries(m).map(([k,v]) => `<tr><td>${k}</td><td style="font-weight:700">${v}</td></tr>`).join('')
    : '<tr><td colspan="2" class="empty">ยังไม่มี metrics</td></tr>';
  document.getElementById('overviewContent').innerHTML = `
    <h3 style="margin-bottom:12px">📊 System Metrics</h3>
    <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>${metricItems}</tbody></table>
    <p style="margin-top:12px;color:#888;font-size:0.85em">
      📦 Leads: ${state.leads.length} | ✍️ Drafts: ${state.drafts.length} | 🌐 Projects: ${state.projects.length}
    </p>
  `;
}

// ── Leads ──
function renderLeads() {
  const q = (document.getElementById('leadSearch')?.value || '').toLowerCase();
  const filtered = state.leads.filter(l =>
    !q || (l.name||'').toLowerCase().includes(q) || (l.company||'').toLowerCase().includes(q)
  );
  if (!filtered.length) {
    document.getElementById('leadsTable').innerHTML = '<div class="empty"><div class="icon">👥</div>ยังไม่มี leads</div>';
    return;
  }
  const rows = filtered.map(l => `
    <tr>
      <td><strong>#${l.id}</strong></td>
      <td>${esc(l.name) || '<em style="color:#aaa">ไม่มีชื่อ</em>'}</td>
      <td>${esc(l.company) || '-'}</td>
      <td><span class="badge badge-${l.status || 'new'}">${l.status || 'new'}</span></td>
      <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(l.summary || '')}</td>
      <td>${l.created_at?.slice(0,10) || '-'}</td>
    </tr>
  `).join('');
  document.getElementById('leadsTable').innerHTML = `
    <table><thead><tr><th>ID</th><th>ชื่อ</th><th>บริษัท</th><th>สถานะ</th><th>สรุป</th><th>วันที่</th></tr></thead>
    <tbody>${rows}</tbody></table>
  `;
}

// ── Content ──
function renderContent() {
  if (!state.drafts.length) {
    document.getElementById('contentGrid').innerHTML = '<div class="empty"><div class="icon">✍️</div>ยังไม่มี drafts</div>';
    return;
  }
  const cards = state.drafts.map(d => `
    <div class="content-card ${d.content_type || 'landing'}">
      <h4>${esc(d.title) || 'Untitled'}</h4>
      <div class="meta">${d.content_type || 'landing'} · ${d.tone || '-'} · ${d.created_at?.slice(0,10) || '-'}</div>
      <div class="body-preview">${esc((d.body || '').slice(0,150))}</div>
    </div>
  `).join('');
  document.getElementById('contentGrid').innerHTML = `<div class="content-grid">${cards}</div>`;
}

// ── Projects ──
function renderProjects() {
  if (!state.projects.length) {
    document.getElementById('projectsGrid').innerHTML = '<div class="empty"><div class="icon">🌐</div>ยังไม่มีโปรเจค</div>';
    return;
  }
  const cards = state.projects.map(p => `
    <div class="project-card">
      <div class="icon">🌐</div>
      <h4>${esc(p.name)}</h4>
      <p style="font-size:0.8em;color:#888">${p.files?.length || 0} files</p>
    </div>
  `).join('');
  document.getElementById('projectsGrid').innerHTML = `<div class="project-grid">${cards}</div>`;
}

// ── Helpers ──
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function fmtUptime(s) {
  const h = Math.floor(s/3600), m = Math.floor((s%3600)/60);
  return h > 0 ? `${h}h ${m}m` : `${m}m ${Math.floor(s%60)}s`;
}
</script>
</body>
</html>"""
