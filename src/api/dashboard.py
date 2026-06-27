"""
Aetox Works — Agent Workspace Dashboard v4
Product register: data-dense tool, dark theme
Brand: oklch(0.68 0.22 290) violet
"""
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aetox Workspace</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:oklch(0.97 0.008 285);--ink-muted:oklch(0.70 0.016 285);--ink-dim:oklch(0.55 0.020 285);--bg:oklch(0.14 0.022 270);--bg-raised:oklch(0.18 0.025 270);--bg-hover:oklch(0.22 0.030 270);--surface:oklch(0.20 0.028 270);--border:oklch(0.28 0.032 270);--border-light:oklch(0.24 0.030 270);--brand:oklch(0.68 0.22 290);--brand-dim:oklch(0.50 0.18 290);--brand-bg:oklch(0.30 0.12 290 / 0.20);--amber:oklch(0.72 0.18 85);--amber-dim:oklch(0.55 0.14 85);--amber-bg:oklch(0.72 0.18 85 / 0.12);--green:oklch(0.65 0.18 155);--green-dim:oklch(0.48 0.14 155);--green-bg:oklch(0.65 0.18 155 / 0.10);--red:oklch(0.62 0.20 25);--red-bg:oklch(0.62 0.20 25 / 0.12);--blue:oklch(0.62 0.18 250);--blue-bg:oklch(0.62 0.18 250 / 0.10);--font-sans:'Inter',system-ui,-apple-system,sans-serif;--font-mono:'JetBrains Mono','Fira Code',monospace;--radius-sm:6px;--radius-md:10px;--radius-lg:14px;--shadow-sm:0 1px 2px rgba(0,0,0,0.3);--shadow-md:0 4px 16px rgba(0,0,0,0.25);--shadow-lg:0 8px 32px rgba(0,0,0,0.35);--z-sidebar:30;--z-topbar:40;--z-dropdown:50;--z-tooltip:60;--z-modal:70}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font-sans);background:var(--bg);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased;overflow:hidden;height:100vh}
::selection{background:var(--brand);color:#fff}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:var(--ink-dim)}
.app{display:flex;height:100vh;overflow:hidden}
.sidebar{width:220px;background:var(--bg-raised);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;z-index:var(--z-sidebar)}
.sidebar-logo{padding:16px 18px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}
.sidebar-logo svg{flex-shrink:0}
.sidebar-logo h1{font-size:.95em;font-weight:800;letter-spacing:-0.02em;color:var(--ink)}
.sidebar-logo .version{font-size:.6em;color:var(--ink-dim);font-weight:500;margin-left:auto}
.sidebar-nav{flex:1;overflow-y:auto;padding:8px 8px 0}
.sidebar-nav-label{font-size:.6em;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-dim);padding:12px 10px 4px}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:var(--radius-sm);cursor:pointer;transition:all .15s ease;text-decoration:none;color:var(--ink-muted);font-size:.82em;font-weight:500;position:relative;user-select:none}
.nav-item:hover{background:var(--bg-hover);color:var(--ink)}
.nav-item.active{background:var(--brand-bg);color:var(--brand)}
.nav-item.active::before{content:'';position:absolute;left:-8px;top:50%;transform:translateY(-50%);width:3px;height:20px;background:var(--brand);border-radius:0 3px 3px 0}
.nav-item .nav-icon{width:18px;height:18px;display:flex;align-items:center;justify-content:center;flex-shrink:0;opacity:.7}
.nav-item.active .nav-icon{opacity:1}
.nav-item .nav-badge{margin-left:auto;font-size:.65em;font-weight:700;padding:1px 6px;border-radius:999px;background:var(--border);color:var(--ink-dim)}
.nav-item.active .nav-badge{background:var(--brand);color:#fff}
.nav-item .nav-dot{width:7px;height:7px;border-radius:50%;margin-left:auto;flex-shrink:0}
.nav-dot.active{background:var(--amber);box-shadow:0 0 8px var(--amber)}
.nav-dot.done{background:var(--green)}
.nav-dot.error{background:var(--red)}
.nav-dot.idle{background:var(--ink-dim)}
.nav-dot.waiting{background:var(--blue)}
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}
.topbar{height:48px;background:var(--bg-raised);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:16px;flex-shrink:0}
.topbar-pipeline{display:flex;align-items:center;gap:4px;flex:1;overflow-x:auto;padding:2px 0}
.pipeline-step{display:flex;align-items:center;gap:4px;font-size:.7em;font-weight:600;color:var(--ink-dim);white-space:nowrap;padding:3px 8px;border-radius:999px;background:var(--surface);border:1px solid var(--border-light);transition:all .2s}
.pipeline-step.done{color:var(--green);border-color:var(--green-dim);background:var(--green-bg)}
.pipeline-step.active{color:var(--amber);border-color:var(--amber-dim);background:var(--amber-bg)}
.pipeline-step.pending{color:var(--ink-dim)}
.pipeline-arrow{color:var(--border);font-size:.65em;flex-shrink:0}
.topbar-right{display:flex;align-items:center;gap:10px;flex-shrink:0}
.topbar-status{font-size:.7em;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--green-bg);color:var(--green);border:1px solid var(--green-dim)}
.topbar-time{font-size:.72em;color:var(--ink-dim);font-weight:500;font-family:var(--font-mono)}
.content{flex:1;overflow-y:auto;padding:20px 24px}
.agent-panel{display:none}
.agent-panel.active{display:block;animation:panelIn .25s ease}
@keyframes panelIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.section-title{font-size:.75em;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-dim);margin-bottom:10px}
.section-title .count{font-weight:500;color:var(--ink-muted);margin-left:4px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:16px 18px;transition:border-color .15s}
.card:hover{border-color:var(--brand-dim)}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.card-header h3{font-size:.84em;font-weight:700}
.card-meta{font-size:.7em;color:var(--ink-dim)}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.grid-sidebar{display:grid;grid-template-columns:1fr 280px;gap:16px}
.tag{display:inline-flex;align-items:center;gap:4px;font-size:.68em;font-weight:600;padding:2px 8px;border-radius:999px;background:var(--bg-hover);color:var(--ink-muted)}
.tag-green{background:var(--green-bg);color:var(--green)}
.tag-amber{background:var(--amber-bg);color:var(--amber)}
.tag-red{background:var(--red-bg);color:var(--red)}
.tag-blue{background:var(--blue-bg);color:var(--blue)}
.tag-brand{background:var(--brand-bg);color:var(--brand)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:var(--radius-sm);font-size:.78em;font-weight:600;font-family:inherit;border:1px solid var(--border);background:var(--surface);color:var(--ink-muted);cursor:pointer;transition:all .15s}
.btn:hover{background:var(--bg-hover);color:var(--ink);border-color:var(--ink-dim)}
.btn-primary{background:var(--brand);border-color:var(--brand);color:#fff}
.btn-primary:hover{background:var(--brand-dim);border-color:var(--brand-dim)}
.btn-danger{background:var(--red);border-color:var(--red);color:#fff}
.btn-danger:hover{background:var(--red);border-color:var(--red);color:#fff;filter:brightness(1.08)}
.btn-ghost{border-color:transparent;background:transparent}
.btn-ghost:hover{background:var(--bg-hover);border-color:transparent}
.btn-sm{padding:4px 10px;font-size:.72em}
.input{width:100%;padding:8px 12px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--ink);font-size:.82em;font-family:inherit;outline:none;transition:border-color .15s}
.input:focus{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-bg)}
.input::placeholder{color:var(--ink-dim)}
.textarea{width:100%;padding:10px 12px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--ink);font-size:.82em;font-family:inherit;outline:none;resize:vertical;min-height:80px;transition:border-color .15s}
.textarea:focus{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-bg)}
.code-block{font-family:var(--font-mono);font-size:.75em;line-height:1.65;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px;overflow-x:auto;white-space:pre-wrap;color:var(--ink-muted)}
.divider{border:0;border-top:1px solid var(--border);margin:14px 0}
.alert{padding:10px 14px;border-radius:var(--radius-sm);font-size:.78em;font-weight:500;display:flex;align-items:center;gap:8px}
.alert-info{background:var(--blue-bg);color:var(--blue);border:1px solid var(--blue)}
.alert-warn{background:var(--amber-bg);color:var(--amber);border:1px solid var(--amber-dim)}
.alert-error{background:var(--red-bg);color:var(--red);border:1px solid var(--red)}
.empty-state{text-align:center;padding:40px 20px;color:var(--ink-dim)}
.empty-state p{font-size:.82em}
.pa-pipeline-flow{display:flex;align-items:center;gap:0;margin-bottom:18px;padding:14px 18px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);overflow-x:auto}
.flow-node{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:70px;position:relative}
.flow-node-icon{width:36px;height:36px;border-radius:50%;background:var(--bg-hover);border:2px solid var(--border);display:flex;align-items:center;justify-content:center;transition:all .2s}
.flow-node.active .flow-node-icon{border-color:var(--amber);background:var(--amber-bg);box-shadow:0 0 12px var(--amber-bg)}
.flow-node.done .flow-node-icon{border-color:var(--green);background:var(--green-bg)}
.flow-node-label{font-size:.62em;font-weight:600;color:var(--ink-dim);text-align:center;white-space:nowrap}
.flow-node.active .flow-node-label{color:var(--amber)}
.flow-node.done .flow-node-label{color:var(--green)}
.flow-connector{flex-shrink:0;width:20px;height:2px;background:var(--border);margin:0 2px;margin-bottom:18px}
.flow-connector.done{background:var(--green)}
.flow-connector.active{background:var(--amber);height:2px;position:relative}
.flow-connector.active::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(90deg,var(--amber),var(--brand));animation:flowPulse 1.5s ease infinite}
@keyframes flowPulse{0%,100%{opacity:.3}50%{opacity:1}}
.router-table{width:100%;border-collapse:collapse;font-size:.8em}
.router-table th{text-align:left;padding:8px 12px;border-bottom:1px solid var(--border);color:var(--ink-dim);font-weight:600;font-size:.7em;text-transform:uppercase;letter-spacing:.04em}
.router-table td{padding:8px 12px;border-bottom:1px solid var(--border-light)}
.router-table tr:hover td{background:var(--bg-hover)}
.router-table .route-indicator{width:8px;height:8px;border-radius:50%;display:inline-block}
.route-indicator.routed{background:var(--green)}
.route-indicator.pending{background:var(--ink-dim)}
.handoff-brief{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px;margin-top:8px}
.handoff-brief-item{display:flex;align-items:flex-start;gap:8px;padding:6px 0;font-size:.78em;border-bottom:1px solid var(--border-light)}
.handoff-brief-item:last-child{border-bottom:0}
.handoff-key{font-weight:600;color:var(--ink-muted);min-width:80px;flex-shrink:0}
.sales-chat{border:1px solid var(--border);border-radius:var(--radius-md);background:var(--surface);overflow:hidden;display:flex;flex-direction:column;height:320px}
.sales-chat-header{padding:10px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;font-size:.75em;font-weight:600;color:var(--ink-muted)}
.sales-chat-messages{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.chat-msg{max-width:85%;padding:8px 12px;border-radius:12px;font-size:.78em;line-height:1.5;animation:msgIn .2s ease}
@keyframes msgIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.chat-msg.user{align-self:flex-end;background:var(--brand-bg);border:1px solid var(--brand-dim);border-bottom-right-radius:4px}
.chat-msg.agent{align-self:flex-start;background:var(--bg);border:1px solid var(--border);border-bottom-left-radius:4px}
.chat-msg .msg-time{font-size:.65em;color:var(--ink-dim);margin-top:3px;display:block}
.sales-chat-input{display:flex;gap:6px;padding:8px 10px;border-top:1px solid var(--border);background:var(--bg)}
.sales-chat-input input{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:7px 10px;font-size:.78em;font-family:inherit;color:var(--ink);outline:none}
.sales-chat-input input:focus{border-color:var(--brand)}
.sales-chat-footer{padding:9px 12px;border-top:1px solid var(--border);background:var(--bg);font-size:.72em;color:var(--ink-dim)}
.notebook-item{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-bottom:1px solid var(--border-light);transition:background .15s;cursor:pointer}
.notebook-item:last-child{border-bottom:0}
.notebook-item:hover{background:var(--bg-hover)}
.notebook-item .nb-title{font-size:.82em;font-weight:600}
.notebook-item .nb-meta{font-size:.68em;color:var(--ink-dim);margin-top:2px}
.notebook-actions{display:flex;align-items:center;gap:6px;flex-shrink:0}
.notebook-viewer{min-height:150px;max-height:340px;overflow:auto}
.notebook-render{display:flex;flex-direction:column;gap:12px;font-size:.78em;color:var(--ink-muted)}
.notebook-render-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding-bottom:10px;border-bottom:1px solid var(--border-light)}
.notebook-render-title{font-size:1.05em;font-weight:800;color:var(--ink);line-height:1.35}
.notebook-render-meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.notebook-field{background:var(--bg);border:1px solid var(--border-light);border-radius:var(--radius-sm);padding:8px 10px}
.notebook-field-label{font-size:.72em;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-dim);font-weight:700;margin-bottom:2px}
.notebook-field-value{color:var(--ink);font-weight:600;word-break:break-word}
.notebook-section{border:1px solid var(--border-light);border-radius:var(--radius-sm);padding:10px 12px;background:var(--bg)}
.notebook-section h4{font-size:.82em;color:var(--ink);margin-bottom:8px}
.notebook-list{display:flex;flex-direction:column;gap:6px}
.notebook-list-item{display:flex;gap:8px;line-height:1.55}
.notebook-list-item::before{content:'';width:5px;height:5px;border-radius:50%;background:var(--brand);margin-top:8px;flex-shrink:0}
.notebook-log{display:flex;flex-direction:column;gap:7px}
.notebook-log-line{padding:7px 9px;border-radius:var(--radius-sm);border:1px solid var(--border-light);background:var(--surface)}
.notebook-log-line.user{border-color:var(--brand-dim);background:var(--brand-bg);color:var(--ink)}
.notebook-log-line.agent{border-color:var(--green-dim);background:var(--green-bg);color:var(--ink)}
.notebook-confirm-btn{display:flex;align-items:center;gap:4px;padding:3px 8px;border-radius:999px;font-size:.65em;font-weight:700;border:1px solid var(--green-dim);color:var(--green);background:transparent;cursor:pointer;transition:all .15s}
.notebook-confirm-btn:hover{background:var(--green-bg)}
.notebook-confirm-btn.confirmed{background:var(--green-bg)}
.source-list{display:flex;flex-direction:column;gap:6px}
.source-item{display:flex;align-items:center;gap:8px;padding:8px 10px;background:var(--bg);border:1px solid var(--border-light);border-radius:var(--radius-sm);font-size:.78em;transition:border-color .15s}
.source-item:hover{border-color:var(--brand-dim)}
.source-icon{width:20px;height:20px;border-radius:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.source-icon.real{background:var(--green-bg);color:var(--green)}
.source-icon.demo{background:var(--amber-bg);color:var(--amber)}
.source-icon.mock{background:var(--red-bg);color:var(--red)}
.source-info{flex:1;min-width:0}
.source-name{font-weight:600}
.source-url{font-size:.7em;color:var(--ink-dim);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.source-tag{flex-shrink:0}
.draft-card{padding:14px 16px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);transition:border-color .15s;cursor:pointer}
.draft-card:hover{border-color:var(--brand-dim)}
.draft-card.active{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-bg)}
.draft-title{font-size:.85em;font-weight:700;margin-bottom:4px}
.draft-meta{display:flex;gap:8px;font-size:.68em;color:var(--ink-dim);flex-wrap:wrap}
.draft-preview{font-size:.75em;color:var(--ink-muted);margin-top:6px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.version-timeline{display:flex;flex-direction:column;gap:6px}
.version-item{display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--bg);border:1px solid var(--border-light);border-radius:var(--radius-sm);font-size:.76em}
.version-dot{width:8px;height:8px;border-radius:50%;background:var(--brand);flex-shrink:0}
.version-info{flex:1}
.version-num{font-weight:600}
.version-time{font-size:.7em;color:var(--ink-dim)}
.file-tree{border:1px solid var(--border);border-radius:var(--radius-sm);overflow:hidden}
.file-item{display:flex;align-items:center;gap:8px;padding:7px 12px;border-bottom:1px solid var(--border-light);font-size:.78em;cursor:pointer;transition:background .1s}
.file-item:last-child{border-bottom:0}
.file-item:hover{background:var(--bg-hover)}
.file-item.active{background:var(--brand-bg);color:var(--brand)}
.file-item .file-size{margin-left:auto;font-size:.7em;color:var(--ink-dim)}
.build-log{font-family:var(--font-mono);font-size:.72em;line-height:1.5;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px;max-height:200px;overflow-y:auto}
.build-log .log-info{color:var(--ink-muted)}
.build-log .log-success{color:var(--green)}
.build-log .log-error{color:var(--red)}
.build-log .log-warn{color:var(--amber)}
.dev-layout{display:flex;flex-direction:column;gap:16px}
.dev-side-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(280px,.8fr);gap:16px}
.dev-files-panel{display:flex;flex-direction:column;gap:10px}
.dev-preview-panel{display:flex;flex-direction:column;gap:10px}
.dev-preview-head{display:flex;align-items:center;justify-content:space-between;gap:12px}
.dev-preview-area{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);overflow:hidden;height:clamp(520px,68vh,820px);display:flex;align-items:center;justify-content:center;color:var(--ink-dim);font-size:.78em}
.dev-preview-shell{width:100%;height:100%;display:flex;flex-direction:column;background:#fff}
.dev-preview-bar{height:28px;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:0 10px;background:var(--surface);border-bottom:1px solid var(--border);font-size:.7em;color:var(--ink-muted);font-weight:600}
.dev-preview-frame{flex:1;width:100%;border:0;background:#fff}
.file-actions{display:flex;align-items:center;gap:8px;margin-left:auto;flex-shrink:0}
.file-delete-btn{padding:3px 8px;font-size:.68em}
.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.metric-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:14px 16px;text-align:center}
.metric-val{font-size:1.6em;font-weight:800;letter-spacing:-0.02em;line-height:1.2;color:var(--ink)}
.metric-label{font-size:.7em;color:var(--ink-dim);font-weight:500;margin-top:2px}
.metric-trend{font-size:.65em;font-weight:600;margin-top:4px}
.metric-trend.up{color:var(--green)}
.metric-trend.down{color:var(--red)}
.checklist-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border-light);font-size:.8em}
.checklist-item:last-child{border-bottom:0}
.checkbox-custom{width:16px;height:16px;border:2px solid var(--border);border-radius:4px;flex-shrink:0;cursor:pointer;transition:all .15s;display:flex;align-items:center;justify-content:center}
.checkbox-custom.done{border-color:var(--green);background:var(--green)}
.checkbox-custom.done::after{content:'\2713';color:#fff;font-size:10px;font-weight:800}
.deliverable-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:18px}
.deliverable-card .dl-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border-light);font-size:.82em}
.deliverable-card .dl-row:last-child{border-bottom:0}
.dl-label{color:var(--ink-dim);font-weight:500}
.dl-value{font-weight:600;font-family:var(--font-mono);font-size:.92em}
.dl-value.file{color:var(--brand);cursor:pointer}
.dl-value.file:hover{text-decoration:underline}
.status-banner{display:flex;align-items:center;gap:10px;padding:14px 18px;border-radius:var(--radius-md);font-weight:600;font-size:.85em}
.status-banner.ready{background:var(--green-bg);border:1px solid var(--green-dim);color:var(--green)}
.status-banner.incomplete{background:var(--amber-bg);border:1px solid var(--amber-dim);color:var(--amber)}
.graph-shell{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;min-height:calc(100vh - 108px)}
.graph-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.graph-toolbar h2{font-size:1.05em;font-weight:700;letter-spacing:-0.01em}
.graph-toolbar p{font-size:.78em;color:var(--ink-dim);margin-top:2px}
.graph-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.segmented{display:inline-flex;border:1px solid var(--border);border-radius:var(--radius-sm);overflow:hidden;background:var(--surface)}
.segmented button{border:0;background:transparent;color:var(--ink-dim);padding:6px 10px;font-size:.72em;font-weight:700;cursor:pointer}
.segmented button.active{background:var(--brand-bg);color:var(--brand)}
.agent-graph-stage{position:relative;min-height:560px;background:radial-gradient(circle at 50% 50%,oklch(0.24 0.04 285 / .45),transparent 42%),var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden}
.agent-graph-stage::before{content:'';position:absolute;inset:0;background-image:linear-gradient(var(--border-light) 1px,transparent 1px),linear-gradient(90deg,var(--border-light) 1px,transparent 1px);background-size:34px 34px;opacity:.22;pointer-events:none}
.agent-edge-layer{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}
.agent-edge{stroke:var(--border);stroke-width:2;fill:none;opacity:.76}
.agent-edge.active{stroke:var(--amber);stroke-width:3;filter:drop-shadow(0 0 6px var(--amber-bg));stroke-dasharray:8 7;animation:edgeFlow 1.2s linear infinite}
.agent-edge.done{stroke:var(--green);opacity:.9}
.agent-edge.waiting{stroke:var(--blue);stroke-dasharray:4 6}
.agent-edge.error{stroke:var(--red);stroke-width:3}
@keyframes edgeFlow{to{stroke-dashoffset:-15}}
.agent-graph-node{position:absolute;z-index:2;width:150px;min-height:88px;transform:translate(-50%,-50%);background:oklch(0.17 0.025 270 / .94);border:1px solid var(--border);border-radius:12px;padding:12px;box-shadow:var(--shadow-md);cursor:grab;user-select:none;transition:border-color .15s,box-shadow .15s,background .15s}
.agent-graph-node:hover{border-color:var(--brand-dim);box-shadow:0 10px 30px rgba(0,0,0,.32)}
.agent-graph-node.selected{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-bg),var(--shadow-md)}
.agent-graph-node.active{border-color:var(--amber);box-shadow:0 0 0 3px var(--amber-bg),0 0 22px var(--amber-bg)}
.agent-graph-node.done{border-color:var(--green-dim)}
.agent-graph-node.waiting{border-color:var(--blue)}
.agent-graph-node.error{border-color:var(--red)}
.agent-node-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.agent-node-name{font-size:.82em;font-weight:800;line-height:1.2}
.agent-node-state{font-size:.6em;font-weight:800;text-transform:uppercase;letter-spacing:.04em;padding:2px 6px;border-radius:999px;background:var(--bg-hover);color:var(--ink-dim)}
.agent-graph-node.active .agent-node-state{background:var(--amber-bg);color:var(--amber)}
.agent-graph-node.done .agent-node-state{background:var(--green-bg);color:var(--green)}
.agent-graph-node.waiting .agent-node-state{background:var(--blue-bg);color:var(--blue)}
.agent-graph-node.error .agent-node-state{background:var(--red-bg);color:var(--red)}
.agent-node-role{font-size:.66em;color:var(--ink-dim);line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.agent-loader{display:none;position:absolute;right:8px;bottom:8px;width:14px;height:14px;border:2px solid var(--amber-bg);border-top-color:var(--amber);border-radius:50%;animation:spin .8s linear infinite}
.agent-graph-node.active .agent-loader{display:block}
@keyframes spin{to{transform:rotate(360deg)}}
.agent-inspector-panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:16px;min-height:560px;overflow:auto}
.agent-inspector-panel h3{font-size:.95em;font-weight:800;margin-bottom:4px}
.inspector-muted{font-size:.72em;color:var(--ink-dim);line-height:1.5}
.inspector-row{display:grid;grid-template-columns:88px 1fr;gap:8px;padding:8px 0;border-bottom:1px solid var(--border-light);font-size:.76em}
.inspector-row:last-child{border-bottom:0}
.inspector-key{color:var(--ink-dim);font-weight:700}
.inspector-value{color:var(--ink-muted);word-break:break-word}
.graph-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--ink-dim);font-size:.8em;z-index:3;pointer-events:none}
@media(max-width:900px){.sidebar{width:56px}.sidebar-logo h1,.sidebar-logo .version,.sidebar-nav-label,.nav-item .nav-text,.nav-item .nav-badge{display:none}.nav-item{padding:9px;justify-content:center}.nav-item .nav-icon{margin:0}.nav-item.active::before{left:-4px}.grid-2,.grid-sidebar,.dev-side-grid{grid-template-columns:1fr}.grid-3{grid-template-columns:1fr 1fr}.metric-grid{grid-template-columns:repeat(2,1fr)}.content{padding:14px 16px}.dev-preview-area{height:clamp(420px,64vh,680px)}}
@media(max-width:900px){.graph-shell{grid-template-columns:1fr}.agent-inspector-panel{min-height:260px}.agent-graph-stage{min-height:520px}}
@media(max-width:600px){.sidebar{width:48px}.grid-3,.metric-grid{grid-template-columns:1fr}.content{padding:10px 12px}.agent-graph-node{width:128px;min-height:82px;padding:10px}.graph-actions{justify-content:flex-start}.graph-toolbar{align-items:flex-start;flex-direction:column}}
</style>
</head>
<body>

<div class="app">
  <aside class="sidebar">
    <div class="sidebar-logo">
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none"><rect x="2" y="2" width="18" height="18" rx="4" stroke="oklch(0.68 0.22 290)" stroke-width="2" fill="oklch(0.68 0.22 290 / 0.08)"/><path d="M7 11L10 14L15 8" stroke="oklch(0.68 0.22 290)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <h1>Aetox</h1><span class="version">v0.3</span>
    </div>
    <nav class="sidebar-nav">
      <div class="sidebar-nav-label">Agents</div>
      <div class="nav-item active" data-agent="graph" onclick="switchAgent('graph')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="2.2" stroke="currentColor" stroke-width="1.3"/><circle cx="3.5" cy="4" r="1.7" stroke="currentColor" stroke-width="1.3"/><circle cx="12.5" cy="4" r="1.7" stroke="currentColor" stroke-width="1.3"/><circle cx="4.5" cy="12.5" r="1.7" stroke="currentColor" stroke-width="1.3"/><circle cx="12" cy="12" r="1.7" stroke="currentColor" stroke-width="1.3"/><path d="M5 5.2l1.5 1.5M11 5.2L9.5 6.7M6.2 9.4l-1 1.6M9.6 9.5l1.2 1.2" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg></span><span class="nav-text">Agent Graph</span><span class="nav-dot active"></span></div>
      <div class="nav-item" data-agent="personal_assistant" onclick="switchAgent('personal_assistant')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="5" r="3" stroke="currentColor" stroke-width="1.3" fill="none"/><path d="M2 14c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="1.3"/></svg></span><span class="nav-text">Personal Assistant</span><span class="nav-dot active"></span></div>
      <div class="nav-item" data-agent="sales" onclick="switchAgent('sales')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 5l6 3 6-3M2 5v6l6 3 6-3V5" stroke="currentColor" stroke-width="1.3" fill="none"/></svg></span><span class="nav-text">Sales</span><span class="nav-badge" id="salesNavBadge">0</span></div>
      <div class="nav-item" data-agent="research" onclick="switchAgent('research')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.3" stroke="currentColor" stroke-width="1.3"/><path d="M10 10l3.5 3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></span><span class="nav-text">Research</span><span class="nav-dot idle"></span></div>
      <div class="nav-item" data-agent="content" onclick="switchAgent('content')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 2h10v12H3V2z" stroke="currentColor" stroke-width="1.3"/><path d="M5 5h6M5 8h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></span><span class="nav-text">Content</span><span class="nav-badge">3</span></div>
      <div class="nav-item" data-agent="dev" onclick="switchAgent('dev')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M5 4L2 8l3 4M11 4l3 4-3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 2.5L7 13.5" stroke="currentColor" stroke-width="1.3" opacity="0.5"/></svg></span><span class="nav-text">Dev</span><span class="nav-dot waiting"></span></div>
      <div class="nav-item" data-agent="data" onclick="switchAgent('data')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="12" height="5" rx="1.5" stroke="currentColor" stroke-width="1.3"/><rect x="2" y="9" width="12" height="5" rx="1.5" stroke="currentColor" stroke-width="1.3"/></svg></span><span class="nav-text">Data</span><span class="nav-dot done"></span></div>
      <div class="nav-item" data-agent="final" onclick="switchAgent('final')"><span class="nav-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 8l4 4 8-8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="nav-text">Final Output</span><span class="nav-dot idle"></span></div>
    </nav>
  </aside>

  <div class="main">
    <header class="topbar">
      <div class="topbar-pipeline" id="pipelineBar">
        <span class="pipeline-step pending" data-step="personal_assistant">PA</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="sales">Sales</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="research">Research</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="content">Content</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="dev">Dev</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="data">Data</span><span class="pipeline-arrow">→</span>
        <span class="pipeline-step pending" data-step="final">Final</span>
      </div>
      <div class="topbar-right">
        <span class="topbar-status" id="topbarStatus">Idle</span>
        <span class="topbar-time" id="clock">--:--</span>
      </div>
    </header>

    <main class="content" id="mainContent">

      <!-- AGENT GRAPH -->
      <section class="agent-panel active" id="panel-graph">
        <div class="graph-toolbar">
          <div><h2>Agent Graph</h2><p>Runtime graph จริงผ่าน Personal Assistant เป็น hub กลาง กด node เพื่อเปิด workspace หรือลากเพื่อจัด layout</p></div>
          <div class="graph-actions">
            <div class="segmented">
              <button class="active" id="graphModePipeline" onclick="setGraphViewMode('pipeline')">Pipeline</button>
              <button id="graphModeRouter" onclick="setGraphViewMode('router')">Router</button>
            </div>
            <button class="btn btn-ghost btn-sm" onclick="resetAgentLayout()">Reset Layout</button>
            <button class="btn btn-primary btn-sm" onclick="refreshAgentGraph()">Refresh</button>
          </div>
        </div>
        <div class="graph-shell">
          <div class="agent-graph-stage" id="agentGraphStage">
            <svg class="agent-edge-layer" id="agentEdgeLayer" aria-hidden="true"></svg>
            <div class="graph-empty" id="agentGraphEmpty">Loading agent graph...</div>
          </div>
          <aside class="agent-inspector-panel" id="agentInspector"></aside>
        </div>
      </section>

      <!-- PA -->
      <section class="agent-panel" id="panel-personal_assistant">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Personal Assistant</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">รับคำสั่ง วางแผน flow และจัดการ handoff ระหว่าง agents</p></div>
          <div style="display:flex;gap:6px"><span class="tag tag-green" id="paMode">Pipeline Mode</span><span class="tag tag-amber" id="paState">Routing...</span></div>
        </div>
        <div class="pa-pipeline-flow" id="paFlowGraph">
          <div class="flow-node done"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><circle cx="7" cy="7" r="3" fill="oklch(0.65 0.18 155)"/></svg></div><span class="flow-node-label">PA</span></div>
          <div class="flow-connector done"></div>
          <div class="flow-node active" id="flowNode-sales"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M2 4.5l5 2.5 5-2.5M2 4.5v5l5 2.5 5-2.5v-5" stroke="oklch(0.72 0.18 85)" stroke-width="1.5" fill="none"/></svg></div><span class="flow-node-label">Sales</span></div>
          <div class="flow-connector"></div>
          <div class="flow-node" id="flowNode-research"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><circle cx="6" cy="6" r="3.5" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M9 9l2.5 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><span class="flow-node-label">Research</span></div>
          <div class="flow-connector"></div>
          <div class="flow-node" id="flowNode-content"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M2.5 2h9v10h-9V2z" stroke="currentColor" stroke-width="1.5" fill="none"/></svg></div><span class="flow-node-label">Content</span></div>
          <div class="flow-connector"></div>
          <div class="flow-node" id="flowNode-dev"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M4 3.5L2 7l2 3.5M10 3.5L12 7l-2 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/></svg></div><span class="flow-node-label">Dev</span></div>
          <div class="flow-connector"></div>
          <div class="flow-node" id="flowNode-data"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><rect x="2" y="2" width="10" height="4" rx="1" stroke="currentColor" stroke-width="1.5" fill="none"/><rect x="2" y="8" width="10" height="4" rx="1" stroke="currentColor" stroke-width="1.5" fill="none"/></svg></div><span class="flow-node-label">Data</span></div>
          <div class="flow-connector"></div>
          <div class="flow-node" id="flowNode-final"><div class="flow-node-icon"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M3 7l3 3 5-6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></div><span class="flow-node-label">Final</span></div>
        </div>
        <div class="grid-2" style="gap:16px">
          <div class="card">
            <div class="card-header"><h3>Router / Supervisor</h3><span class="card-meta">LangGraph</span></div>
            <table class="router-table">
              <thead><tr><th>Agent</th><th>Status</th><th>Route</th><th>Handoff</th></tr></thead>
              <tbody>
                <tr><td style="font-weight:600">Sales</td><td><span class="tag tag-amber">Active</span></td><td><span class="route-indicator routed"></span> Routed</td><td><button class="btn btn-ghost btn-sm" onclick="showHandoffBrief('sales')">View Brief</button></td></tr>
                <tr><td style="font-weight:600">Research</td><td><span class="tag tag-blue">Queued</span></td><td><span class="route-indicator pending"></span> Pending</td><td><span style="font-size:.72em;color:var(--ink-dim)">-</span></td></tr>
                <tr><td style="font-weight:600">Content</td><td><span class="tag" style="color:var(--ink-dim);background:var(--bg-hover)">Waiting</span></td><td><span class="route-indicator pending"></span> Pending</td><td><span style="font-size:.72em;color:var(--ink-dim)">-</span></td></tr>
                <tr><td style="font-weight:600">Dev</td><td><span class="tag" style="color:var(--ink-dim);background:var(--bg-hover)">Waiting</span></td><td><span class="route-indicator pending"></span> Pending</td><td><span style="font-size:.72em;color:var(--ink-dim)">-</span></td></tr>
                <tr><td style="font-weight:600">Data</td><td><span class="tag" style="color:var(--ink-dim);background:var(--bg-hover)">Waiting</span></td><td><span class="route-indicator pending"></span> Pending</td><td><span style="font-size:.72em;color:var(--ink-dim)">-</span></td></tr>
              </tbody>
            </table>
            <div id="handoffBrief" style="display:none">
              <hr class="divider">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px"><span class="section-title" style="margin-bottom:0">Sales Handoff Brief</span><button class="btn btn-ghost btn-sm" onclick="document.getElementById('handoffBrief').style.display='none'">\2715</button></div>
              <div class="handoff-brief">
                <div class="handoff-brief-item"><span class="handoff-key">Task:</span><span>เก็บ requirement ลูกค้าใหม่</span></div>
                <div class="handoff-brief-item"><span class="handoff-key">Business:</span><span>ต้องการทำ landing page สำหรับโปรดักต์</span></div>
                <div class="handoff-brief-item"><span class="handoff-key">Scope:</span><span>ออกแบบ + เขียน copy + สร้างหน้า HTML</span></div>
                <div class="handoff-brief-item"><span class="handoff-key">Constraints:</span><span>ใช้ brand color, รองรับ mobile</span></div>
                <div class="handoff-brief-item" style="color:var(--ink-dim);font-style:italic"><span class="handoff-key">Note:</span><span>ไม่มีข้อมูลส่วนตัวลูกค้า</span></div>
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><h3>Shared State / Handoff</h3><span class="card-meta">Current session</span></div>
            <div style="margin-bottom:10px"><div style="font-size:.72em;color:var(--ink-dim);font-weight:600;margin-bottom:4px">INPUT</div><div style="font-size:.8em;background:var(--bg);padding:8px 10px;border-radius:var(--radius-sm);border:1px solid var(--border-light)">"ต้องการทำ landing page สำหรับโปรดักต์ AI agent ใหม่"</div></div>
            <div style="margin-bottom:10px"><div style="font-size:.72em;color:var(--ink-dim);font-weight:600;margin-bottom:4px">SHARED STATE</div>
              <div class="code-block" style="max-height:160px;overflow-y:auto">{<br>  "session_id": "ctx_8f3a2b",<br>  "user_id": "usr_017",<br>  "task_type": "landing_page",<br>  "current_agent": "sales",<br>  "pipeline": ["sales", "research", "content", "dev", "data"],<br>  "completed": ["sales"],<br>  "handoffs": {"sales": { "lead_id": "LD-042", "confirmed": true }},<br>  "errors": []<br>}</div></div>
            <div><div style="font-size:.72em;color:var(--ink-dim);font-weight:600;margin-bottom:4px">CURRENT AGENT</div><div style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:var(--amber-bg);border:1px solid var(--amber-dim);border-radius:var(--radius-sm);font-size:.82em;color:var(--amber)"><svg width="12" height="12" viewBox="0 0 12 12"><circle cx="6" cy="6" r="5" fill="currentColor"/></svg> Sales — กำลังเก็บ requirement</div></div>
          </div>
        </div>
      </section>

      <!-- SALES -->
      <section class="agent-panel" id="panel-sales">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Sales</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">เก็บโจทย์ลูกค้า จัดการ lead และ notebook</p></div>
          <span class="tag tag-amber">Active</span>
        </div>
        <div class="alert alert-info" id="salesNotice" style="margin-bottom:14px"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.3"/><path d="M7 4v4M7 10v-0.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg><span id="salesNoticeText">กำลังโหลดประวัติ Sales จริงจากระบบ</span><button class="btn btn-sm" style="margin-left:auto;white-space:nowrap" onclick="this.parentElement.style.display='none'">Dismiss</button></div>
        <div class="grid-2" style="gap:16px">
          <div><div class="section-title">Live Chat</div>
            <div class="sales-chat">
              <div class="sales-chat-header"><span id="salesChatTitle">Real customer conversation</span><span class="tag tag-blue" id="salesChatStatus">Last pipeline</span></div>
              <div class="sales-chat-messages" id="salesChatMessages">
                <div class="empty-state"><p>กำลังโหลดประวัติแชทจริง...</p></div>
              </div>
              <div class="sales-chat-footer">หน้านี้อ่านประวัติจริงเท่านั้น การคุยกับลูกค้าให้ใช้หน้าหลักเพื่อให้ Sales จด notebook ถูกชุด</div>
            </div>
          </div>
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px"><span class="section-title" style="margin-bottom:0">Sales Notebook</span><div style="display:flex;gap:6px"><button class="btn btn-ghost btn-sm" onclick="loadSalesWorkspace()">Refresh</button><button class="btn btn-danger btn-sm" onclick="deleteAllSalesNotebooks()">Delete all</button></div></div>
            <div class="card" style="padding:0" id="salesNotebookList">
              <div class="empty-state"><p>กำลังโหลด notebook จริง...</p></div>
            </div>
            <hr class="divider">
            <div class="section-title">Notebook Preview</div>
            <div class="card notebook-viewer" id="salesNotebookViewer"><div class="empty-state"><p>เลือก notebook เพื่อเปิดอ่านไฟล์จริง</p></div></div>
          </div>
        </div>
      </section>

      <!-- RESEARCH -->
      <section class="agent-panel" id="panel-research">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Research</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">ค้นหาข้อมูล ตลาด คู่แข่ง และ insight</p></div>
          <div style="display:flex;gap:6px"><span class="tag tag-blue" id="resStatus">Searching...</span><span class="tag" id="resSourceCount">4 sources</span></div>
        </div>
        <div class="alert alert-warn" style="margin-bottom:14px"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.3"/><path d="M7 4v4M7 10v-0.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg><span><strong>Demo fallback:</strong> 2 sources ใช้ mock data — Firecrawl API ไม่ตอบสนอง</span></div>
        <div class="grid-sidebar" style="gap:16px">
          <div>
            <div style="margin-bottom:14px"><div class="section-title">Search Query</div><div style="display:flex;gap:8px"><input class="input" value="AI agent landing page best practices 2026 SME" id="resSearchQuery" style="flex:1"><button class="btn btn-primary" onclick="alert('Searching...')">Search</button></div></div>
            <div class="section-title">Sources <span class="count">(4)</span></div>
            <div class="source-list">
              <div class="source-item"><span class="source-icon real">R</span><div class="source-info"><div class="source-name">Firecrawl.dev — Docs</div><div class="source-url">docs.firecrawl.dev/features/search</div></div><span class="tag tag-green source-tag">Real</span></div>
              <div class="source-item"><span class="source-icon real">R</span><div class="source-info"><div class="source-name">Exa AI — Semantic Search</div><div class="source-url">exa.ai/search?q=ai+landing+page</div></div><span class="tag tag-green source-tag">Real</span></div>
              <div class="source-item"><span class="source-icon demo">D</span><div class="source-info"><div class="source-name">G2 — Best AI Tools 2026</div><div class="source-url">g2.com/categories/ai-agents</div></div><span class="tag tag-amber source-tag">Demo</span></div>
              <div class="source-item"><span class="source-icon mock">M</span><div class="source-info"><div class="source-name">Competitor Analysis — Mock</div><div class="source-url">(fallback — cached data)</div></div><span class="tag tag-red source-tag">Mock</span></div>
            </div>
            <hr class="divider">
            <div class="section-title">References & Citations</div>
            <div class="code-block" style="max-height:120px;font-size:.72em">[1] Firecrawl Search API — "best practices for AI landing pages" (2026)\n[2] Exa Neural Search — "SME AI adoption trends 2026"\n[3] G2 Report — "Top AI Agent Platforms 2026" [DEMO]\n[4] Mock — "Competitor landing page analysis" [FALLBACK]</div>
          </div>
          <div>
            <div class="section-title">Search Status</div>
            <div class="card" style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span style="font-size:.78em;font-weight:600">Firecrawl</span><span class="tag tag-green">\2713 200</span></div><div style="font-size:.72em;color:var(--ink-dim)"><div>Results: 12</div><div>Tokens: 4,230</div><div>Speed: 1.2s</div></div></div>
            <div class="card" style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span style="font-size:.78em;font-weight:600">Exa</span><span class="tag tag-green">\2713 200</span></div><div style="font-size:.72em;color:var(--ink-dim)"><div>Results: 8</div><div>Tokens: 2,150</div><div>Speed: 0.8s</div></div></div>
            <div class="card" style="margin-bottom:10px;border-color:var(--amber-dim)"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span style="font-size:.78em;font-weight:600">Demo Fallback</span><span class="tag tag-amber">Warn</span></div><div style="font-size:.72em;color:var(--ink-dim)"><div>Sources: 2 (mock)</div><div style="color:var(--amber)">\26A0 Rate limited — ใช้ cached data</div></div></div>
          </div>
        </div>
      </section>

      <!-- CONTENT -->
      <section class="agent-panel" id="panel-content">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Content</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">เขียน copy, landing content และ draft</p></div>
          <button class="btn btn-primary btn-sm" onclick="alert('New draft created')">+ New Draft</button>
        </div>
        <div class="grid-sidebar" style="gap:16px">
          <div>
            <div class="section-title">Drafts <span class="count">(3)</span></div>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div class="draft-card active" onclick="document.querySelectorAll('.draft-card').forEach(c=>c.classList.remove('active'));this.classList.add('active')"><div class="draft-title">AI Agent Landing Page — Thai Innovation</div><div class="draft-meta"><span>Landing Page</span><span>\B7</span><span>Professional</span><span>\B7</span><span>v2</span></div><div class="draft-preview">ปลดล็อกศักยภาพองค์กรของคุณด้วย AI Agent อัจฉริยะ เพิ่มประสิทธิภาพการทำงาน ลดต้นทุน...</div></div>
              <div class="draft-card" onclick="document.querySelectorAll('.draft-card').forEach(c=>c.classList.remove('active'));this.classList.add('active')"><div class="draft-title">AI for SMEs — Blog Post</div><div class="draft-meta"><span>Blog</span><span>\B7</span><span>Educational</span><span>\B7</span><span>v1</span></div><div class="draft-preview">ทำไม SME ไทยต้องเริ่มใช้ AI Agent วันนี้? 5 เหตุผลที่คุณไม่ควรรอ...</div></div>
              <div class="draft-card" onclick="document.querySelectorAll('.draft-card').forEach(c=>c.classList.remove('active'));this.classList.add('active')"><div class="draft-title">Product Feature Email</div><div class="draft-meta"><span>Email</span><span>\B7</span><span>Persuasive</span><span>\B7</span><span>v3</span></div><div class="draft-preview">Subject: พบกับ AI Agent ตัวใหม่ที่จะเปลี่ยนวิธีทำงานของคุณ...</div></div>
            </div>
          </div>
          <div>
            <div class="section-title">Draft Detail</div>
            <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:14px">
              <div><div style="font-size:.7em;color:var(--ink-dim);font-weight:600;margin-bottom:3px">TITLE</div><input class="input" value="AI Agent Landing Page — Thai Innovation"></div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><div style="font-size:.7em;color:var(--ink-dim);font-weight:600;margin-bottom:3px">TONE</div><input class="input" value="Professional"></div><div><div style="font-size:.7em;color:var(--ink-dim);font-weight:600;margin-bottom:3px">CTA</div><input class="input" value="เริ่มต้นใช้งานฟรี"></div></div>
              <div><div style="font-size:.7em;color:var(--ink-dim);font-weight:600;margin-bottom:3px">KEYWORDS</div><div style="display:flex;gap:4px;flex-wrap:wrap"><span class="tag tag-brand">AI Agent</span><span class="tag tag-brand">SME</span><span class="tag tag-brand">automation</span><span class="tag tag-brand">landing page</span><span class="tag">efficiency</span><span class="tag">cost saving</span></div></div>
              <div><div style="font-size:.7em;color:var(--ink-dim);font-weight:600;margin-bottom:3px">BODY</div><textarea class="textarea" rows="4">ปลดล็อกศักยภาพองค์กรของคุณด้วย AI Agent อัจฉริยะ เพิ่มประสิทธิภาพการทำงาน ลดต้นทุน และยกระดับธุรกิจสู่ยุคดิจิทัลอย่างเต็มรูปแบบ เหมาะสำหรับ SME ที่ต้องการเปลี่ยนแปลง...</textarea></div>
            </div>
            <div class="section-title">Version History</div>
            <div class="version-timeline">
              <div class="version-item"><span class="version-dot"></span><div class="version-info"><div class="version-num">v2 — 10:42</div><div style="font-size:.7em;color:var(--ink-dim)">ปรับ CTA + เพิ่ม keywords</div></div><button class="btn btn-ghost btn-sm">Restore</button></div>
              <div class="version-item"><span class="version-dot" style="background:var(--ink-dim)"></span><div class="version-info"><div class="version-num">v1 — 09:15</div><div style="font-size:.7em;color:var(--ink-dim)">ร่างแรกจาก research insight</div></div><button class="btn btn-ghost btn-sm">Restore</button></div>
            </div>
            <hr class="divider">
            <div class="section-title">Research Insights Used</div>
            <div style="font-size:.76em;color:var(--ink-muted);line-height:1.65"><div>\2022 "84% ของ SME ไทยสนใจ AI แต่ไม่รู้จะเริ่มยังไง" — G2 Report</div><div>\2022 "Landing page ที่มี customer testimonial + demo เพิ่ม conversion 32%" — Firecrawl</div><div>\2022 "ราคาที่โปร่งใสเป็นปัจจัยอันดับ 1 สำหรับ SME" — Exa Search</div></div>
          </div>
        </div>
      </section>

      <!-- DEV -->
      <section class="agent-panel" id="panel-dev">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Dev</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">สร้างเว็บ, feature, automation</p></div>
          <div style="display:flex;gap:6px"><span class="tag tag-blue" id="devStatusTag">Loading</span><span class="tag" id="devProjectTag">Project: -</span></div>
        </div>
        <div class="alert alert-info" id="devNotice" style="margin-bottom:14px"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.3"/><path d="M7 4v4M7 10v-0.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg><span id="devNoticeText">กำลังโหลดงาน Dev จริงจาก output/websites</span></div>
        <div class="dev-layout">
          <div class="dev-files-panel">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0"><span class="section-title" style="margin-bottom:0">Generated Files</span><span class="card-meta" id="devFileMeta">0 files</span></div>
            <div class="file-tree" id="devFileTree">
              <div class="empty-state"><p>กำลังโหลดไฟล์ที่ Dev Agent สร้างจริง...</p></div>
            </div>
          </div>
          <div class="dev-preview-panel">
            <div class="dev-preview-head">
              <span class="section-title" style="margin-bottom:0">Preview</span>
              <span class="card-meta" id="devPreviewMeta">HTML preview</span>
            </div>
            <div id="devPreview" class="dev-preview-area">ยังไม่มี HTML preview</div>
          </div>
          <div class="dev-side-grid">
            <div>
            <div class="section-title">Project Path</div>
            <div class="code-block" style="font-size:.7em" id="devProjectPath">ยังไม่มีโปรเจกต์</div>
            </div>
            <div>
            <div class="section-title">Build Logs</div>
            <div class="build-log" style="margin-bottom:14px" id="devBuildLogs">
              <div class="log-line log-info">Waiting for real Dev output...</div>
            </div>
            </div>
          </div>
        </div>
      </section>

      <!-- DATA -->
      <section class="agent-panel" id="panel-data">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Data</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">วิเคราะห์ผลลัพธ์ lead, content, performance</p></div>
          <span class="tag tag-green">Ready</span>
        </div>
        <div style="margin-bottom:16px"><div class="section-title">Report Summary</div>
          <div class="card"><div style="font-size:.82em;font-weight:600;margin-bottom:6px">Sales Pipeline Report — Q2 2026</div><div style="font-size:.74em;color:var(--ink-muted);line-height:1.65">รอบนี้มีการทำงานทั้งหมด <strong>5 agents</strong> เริ่มจาก Sales เก็บ requirement จากลูกค้า 2 ราย Research ค้นข้อมูลแล้ว 12 แหล่ง Content สร้าง 3 drafts Dev กำลัง build อยู่ 1 โปรเจกต์ และ Data กำลังรวม metrics สำหรับรายงานสรุป</div></div></div>
        <div style="margin-bottom:16px"><div class="section-title">Metrics</div>
          <div class="metric-grid">
            <div class="metric-card"><div class="metric-val">14</div><div class="metric-label">Leads Generated</div><div class="metric-trend up">\2191 23%</div></div>
            <div class="metric-card"><div class="metric-val">7</div><div class="metric-label">Drafts Created</div><div class="metric-trend up">\2191 12%</div></div>
            <div class="metric-card"><div class="metric-val">3</div><div class="metric-label">Projects Built</div><div class="metric-trend up">\2191 50%</div></div>
            <div class="metric-card"><div class="metric-val">92%</div><div class="metric-label">Pipeline Success</div><div class="metric-trend up">\2191 5%</div></div>
            <div class="metric-card"><div class="metric-val">2.4s</div><div class="metric-label">Avg Response</div><div class="metric-trend down">\2193 0.3s</div></div>
            <div class="metric-card"><div class="metric-val">8</div><div class="metric-label">Active Sessions</div><div class="metric-trend">-</div></div>
          </div></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px">
          <div><div class="section-title">Deliverables Checklist</div>
            <div class="card" style="padding:10px 14px">
              <div class="checklist-item"><span class="checkbox-custom done"></span><span style="flex:1">Lead qualified & notebook confirmed</span><span class="tag tag-green">Done</span></div>
              <div class="checklist-item"><span class="checkbox-custom done"></span><span style="flex:1">Research completed \2265 5 sources</span><span class="tag tag-green">4/5</span></div>
              <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Content draft approved</span><span class="tag tag-amber">Review</span></div>
              <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Dev output available in workspace</span><span class="tag tag-amber">Check Dev</span></div>
              <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Final deliverable ready for customer</span><span class="tag" style="color:var(--ink-dim)">Pending</span></div>
            </div></div>
          <div><div class="section-title">Final Customer-ready Output</div>
            <div class="card" style="padding:12px 14px;border-color:var(--green-dim)">
              <div style="font-size:.82em;font-weight:600;margin-bottom:4px">\1F4E6 Delivery Package</div>
              <div style="font-size:.75em;color:var(--ink-muted);margin-bottom:10px;line-height:1.5">รวบรวม deliverables จากผลลัพธ์จริงของแต่ละ agent เมื่องาน pipeline เสร็จครบ</div>
              <div style="display:flex;gap:6px;flex-wrap:wrap"><span class="tag tag-green">sales notebook</span><span class="tag tag-green">research summary</span><span class="tag tag-green">content draft</span><span class="tag tag-amber">dev workspace</span></div>
            </div></div>
        </div>
      </section>

      <!-- FINAL OUTPUT -->
      <section class="agent-panel" id="panel-final">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <div><h2 style="font-size:1.05em;font-weight:700;letter-spacing:-0.01em">Final Output</h2><p style="font-size:.78em;color:var(--ink-dim);margin-top:2px">สิ่งที่ส่งให้ลูกค้าได้จริง</p></div>
          <span class="tag tag-amber">Incomplete</span>
        </div>
        <div class="status-banner incomplete" style="margin-bottom:16px"><svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M9 5v5M9 12.5V12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><div><strong>ยังไม่พร้อมส่ง</strong> — ขาด: Dev build ยังมี error, Content draft ยังไม่ approved</div></div>
        <div class="deliverable-card" style="margin-bottom:14px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px"><svg width="20" height="20" viewBox="0 0 20 20"><path d="M3 3h14v14H3V3z" stroke="var(--brand)" stroke-width="1.5" fill="none"/><path d="M7 7h6v1H7zM7 10h4v1H7z" fill="var(--brand)" opacity=".5"/></svg><span style="font-weight:700;font-size:.95em">Deliverables Summary</span></div>
          <div class="dl-row"><span class="dl-label">Lead ID</span><span class="dl-value">LD-042</span></div>
          <div class="dl-row"><span class="dl-label">Draft ID</span><span class="dl-value">CT-017</span></div>
          <div class="dl-row"><span class="dl-label">Dev Project</span><span class="dl-value file" onclick="switchAgent('dev')">Open Dev workspace \2192</span></div>
          <div class="dl-row"><span class="dl-label">Report ID</span><span class="dl-value">RP-008</span></div>
          <div class="dl-row"><span class="dl-label">Output Path</span><span class="dl-value file" style="font-size:.78em">E:\Aetox\output\deliverables\LD-042\</span></div>
          <div class="dl-row"><span class="dl-label">Date</span><span class="dl-value">28 Jun 2026 11:23</span></div>
        </div>
        <div class="section-title">Readiness Checklist</div>
        <div class="card" style="padding:10px 14px">
          <div class="checklist-item"><span class="checkbox-custom done"></span><span style="flex:1">Sales notebook confirmed</span><span class="tag tag-green">\2713</span></div>
          <div class="checklist-item"><span class="checkbox-custom done"></span><span style="flex:1">Research sources \2265 5 (real)</span><span class="tag tag-green">\2713</span></div>
          <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Content draft approved</span><span class="tag tag-amber">Pending</span></div>
          <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Dev build clean (no errors)</span><span class="tag tag-red">Error</span></div>
          <div class="checklist-item"><span class="checkbox-custom"></span><span style="flex:1">Data report generated</span><span class="tag tag-amber">Running</span></div>
        </div>
        <hr class="divider">
        <div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn btn-ghost" onclick="alert('Exported')">Export Summary</button><button class="btn btn-primary" onclick="alert('Preparing package...')">Prepare Delivery Package</button></div>
      </section>

    </main>
  </div>
</div>

<script>
var AGENT_GRAPH={
  nodes:[],
  edges:[],
  layout:{},
  selected:"personal_assistant",
  viewMode:"pipeline",
  drag:null
};
var SALES_STATE={
  notebooks:[],
  selectedNotebookId:"",
  selectedNotebookContent:"",
  lastPipeline:null,
  loading:false
};
var DEV_STATE={
  projects:[],
  selectedProject:"",
  detail:null,
  selectedFile:"",
  loading:false
};
var DEFAULT_NODE_LAYOUT={
  personal_assistant:{x:50,y:52},
  sales:{x:15,y:24},
  research:{x:38,y:16},
  content:{x:62,y:16},
  dev:{x:85,y:24},
  data:{x:78,y:80},
  final:{x:22,y:80}
};
var NODE_LABELS={
  personal_assistant:"Personal Assistant",
  sales:"Sales",
  research:"Research",
  content:"Content",
  dev:"Dev",
  data:"Data",
  final:"Final Output"
};

function esc(v){
  return String(v==null?"":v).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}

function setGraphViewMode(mode){
  AGENT_GRAPH.viewMode=mode==="router"?"router":"pipeline";
  document.getElementById("graphModePipeline").className=AGENT_GRAPH.viewMode==="pipeline"?"active":"";
  document.getElementById("graphModeRouter").className=AGENT_GRAPH.viewMode==="router"?"active":"";
  renderAgentEdges();
}

function refreshAgentGraph(){
  var statusReq=fetch("/api/agents/status").then(function(res){return res.json()});
  var layoutReq=fetch("/api/agents/layout").then(function(res){return res.json()});
  return Promise.all([statusReq,layoutReq]).then(function(all){
    var status=all[0]&&all[0].success?all[0].data:null;
    var layout=all[1]&&all[1].success&&all[1].data?all[1].data.nodes:{};
    AGENT_GRAPH.nodes=status&&status.nodes?status.nodes:[];
    AGENT_GRAPH.edges=status&&status.edges?status.edges:[];
    AGENT_GRAPH.layout=Object.assign({},DEFAULT_NODE_LAYOUT,layout||{});
    if(status&&status.mode){
      AGENT_GRAPH.viewMode=status.mode==="router"?"router":"pipeline";
      setGraphViewMode(AGENT_GRAPH.viewMode);
    }
    updateRuntimeChrome(status);
    buildAgentGraph();
  }).catch(function(err){
    var empty=document.getElementById("agentGraphEmpty");
    if(empty)empty.textContent="Cannot load agent graph: "+err;
  });
}

function updateRuntimeChrome(status){
  var nodeMap={};
  AGENT_GRAPH.nodes.forEach(function(node){nodeMap[node.id]=node});
  document.querySelectorAll(".pipeline-step[data-step]").forEach(function(step){
    var id=step.getAttribute("data-step");
    var node=nodeMap[id]||{};
    var state=node.state||"idle";
    var cls="pending";
    if(state==="active")cls="active";
    if(state==="done")cls="done";
    if(state==="waiting")cls="pending";
    if(state==="error")cls="active";
    step.className="pipeline-step "+cls;
  });
  var statusEl=document.getElementById("topbarStatus");
  if(statusEl){
    if(status&&status.running){
      var current=status.current_agent?": "+String(status.current_agent).replace("_"," "):"";
      statusEl.textContent="Running"+current;
      statusEl.style.background="var(--amber-bg)";
      statusEl.style.color="var(--amber)";
      statusEl.style.borderColor="var(--amber-dim)";
    }else{
      statusEl.textContent="Idle";
      statusEl.style.background="var(--green-bg)";
      statusEl.style.color="var(--green)";
      statusEl.style.borderColor="var(--green-dim)";
    }
  }
  ["personal_assistant","sales","research","content","dev","data","final"].forEach(function(id){
    var item=document.querySelector('.nav-item[data-agent="'+id+'"]');
    if(!item)return;
    var marker=item.querySelector(".nav-dot");
    if(!marker)return;
    var state=(nodeMap[id]&&nodeMap[id].state)||"idle";
    marker.className="nav-dot "+(state==="active"?"active":state==="done"?"done":state==="waiting"?"waiting":state==="error"?"error":"idle");
  });
  var graphMarker=document.querySelector('.nav-item[data-agent="graph"] .nav-dot');
  if(graphMarker)graphMarker.className="nav-dot "+(status&&status.running?"active":"idle");
}

function buildAgentGraph(){
  var stage=document.getElementById("agentGraphStage");
  if(!stage)return;
  stage.querySelectorAll(".agent-graph-node").forEach(function(el){el.remove()});
  var empty=document.getElementById("agentGraphEmpty");
  if(empty)empty.style.display=AGENT_GRAPH.nodes.length?"none":"flex";
  AGENT_GRAPH.nodes.forEach(function(node){
    var pos=AGENT_GRAPH.layout[node.id]||DEFAULT_NODE_LAYOUT[node.id]||{x:50,y:50};
    var div=document.createElement("div");
    div.className="agent-graph-node "+(node.state||"idle")+(node.id===AGENT_GRAPH.selected?" selected":"");
    div.id="agentNode-"+node.id;
    div.setAttribute("data-node-id",node.id);
    div.style.left=pos.x+"%";
    div.style.top=pos.y+"%";
    div.innerHTML='<div class="agent-node-head"><div class="agent-node-name">'+esc(node.name||NODE_LABELS[node.id]||node.id)+'</div><div class="agent-node-state">'+esc(node.label||node.state||"idle")+'</div></div><div class="agent-node-role">'+esc(node.role||node.note||"")+'</div><div class="agent-loader"></div>';
    div.addEventListener("click",function(e){selectGraphNode(node.id)});
    div.addEventListener("dblclick",function(e){openAgentWorkspace(node.id)});
    div.addEventListener("pointerdown",function(e){startDragAgent(e,node.id)});
    stage.appendChild(div);
  });
  renderAgentEdges();
  renderAgentInspector();
}

function renderAgentEdges(){
  var svg=document.getElementById("agentEdgeLayer");
  var stage=document.getElementById("agentGraphStage");
  if(!svg||!stage)return;
  svg.innerHTML="";
  var rect=stage.getBoundingClientRect();
  var edges=agentEdgesForView();
  edges.forEach(function(edge){
    var a=AGENT_GRAPH.layout[edge.from]||DEFAULT_NODE_LAYOUT[edge.from];
    var b=AGENT_GRAPH.layout[edge.to]||DEFAULT_NODE_LAYOUT[edge.to];
    if(!a||!b)return;
    var x1=rect.width*a.x/100;
    var y1=rect.height*a.y/100;
    var x2=rect.width*b.x/100;
    var y2=rect.height*b.y/100;
    var midX=(x1+x2)/2;
    var path=document.createElementNS("http://www.w3.org/2000/svg","path");
    path.setAttribute("d","M "+x1+" "+y1+" C "+midX+" "+y1+", "+midX+" "+y2+", "+x2+" "+y2);
    path.setAttribute("class","agent-edge "+(edge.state||"idle"));
    svg.appendChild(path);
  });
}

function agentEdgesForView(){
  if(AGENT_GRAPH.viewMode==="router"){
    var selected=AGENT_GRAPH.selected&&AGENT_GRAPH.selected!=="personal_assistant"&&AGENT_GRAPH.selected!=="final"?AGENT_GRAPH.selected:"sales";
    return [
      {from:"personal_assistant",to:selected,state:edgeState("personal_assistant",selected)},
      {from:selected,to:"personal_assistant",state:edgeState(selected,"personal_assistant")},
      {from:"personal_assistant",to:"final",state:edgeState("personal_assistant","final")}
    ];
  }
  return AGENT_GRAPH.edges.length?AGENT_GRAPH.edges:[
    {from:"personal_assistant",to:"sales",state:"idle"},
    {from:"sales",to:"personal_assistant",state:"idle"},
    {from:"personal_assistant",to:"research",state:"idle"},
    {from:"research",to:"personal_assistant",state:"idle"},
    {from:"personal_assistant",to:"content",state:"idle"},
    {from:"content",to:"personal_assistant",state:"idle"},
    {from:"personal_assistant",to:"dev",state:"idle"},
    {from:"dev",to:"personal_assistant",state:"idle"},
    {from:"personal_assistant",to:"data",state:"idle"},
    {from:"data",to:"personal_assistant",state:"idle"},
    {from:"personal_assistant",to:"final",state:"idle"}
  ];
}

function edgeState(from,to){
  for(var i=0;i<AGENT_GRAPH.edges.length;i++){
    var edge=AGENT_GRAPH.edges[i];
    if(edge.from===from&&edge.to===to)return edge.state||"idle";
  }
  return "idle";
}

function selectGraphNode(id){
  AGENT_GRAPH.selected=id;
  document.querySelectorAll(".agent-graph-node").forEach(function(el){el.classList.remove("selected")});
  var node=document.getElementById("agentNode-"+id);
  if(node)node.classList.add("selected");
  renderAgentEdges();
  renderAgentInspector();
}

function renderAgentInspector(){
  var panel=document.getElementById("agentInspector");
  if(!panel)return;
  var node=null;
  for(var i=0;i<AGENT_GRAPH.nodes.length;i++){if(AGENT_GRAPH.nodes[i].id===AGENT_GRAPH.selected)node=AGENT_GRAPH.nodes[i]}
  if(!node&&AGENT_GRAPH.nodes.length){node=AGENT_GRAPH.nodes[0];AGENT_GRAPH.selected=node.id}
  if(!node){
    panel.innerHTML="<h3>Agent Inspector</h3><p class='inspector-muted'>ยังไม่มี runtime status</p>";
    return;
  }
  panel.innerHTML=
    "<h3>"+esc(node.name||NODE_LABELS[node.id]||node.id)+"</h3>"+
    "<p class='inspector-muted'>"+esc(node.role||"")+"</p>"+
    inspectorRow("State",node.state||"idle")+
    inspectorRow("Note",node.note||"-")+
    inspectorRow("Started",node.started_at||"-")+
    inspectorRow("Finished",node.finished_at||"-")+
    inspectorRow("Error",node.error||"-")+
    inspectorRow("Output",node.output_summary||"-")+
    '<hr class="divider"><button class="btn btn-primary btn-sm" id="openWorkspaceBtn">Open Workspace</button>';
  var openBtn=document.getElementById("openWorkspaceBtn");
  if(openBtn)openBtn.onclick=function(){openAgentWorkspace(node.id)};
}

function inspectorRow(key,value){
  return '<div class="inspector-row"><div class="inspector-key">'+esc(key)+'</div><div class="inspector-value">'+esc(value)+'</div></div>';
}

function openAgentWorkspace(nodeId){
  if(nodeId==="final"){switchAgent("final");return}
  if(nodeId==="personal_assistant"){switchAgent("personal_assistant");return}
  switchAgent(nodeId);
}

function startDragAgent(e,nodeId){
  if(e.button!==0)return;
  var stage=document.getElementById("agentGraphStage");
  var node=document.getElementById("agentNode-"+nodeId);
  if(!stage||!node)return;
  selectGraphNode(nodeId);
  node.setPointerCapture(e.pointerId);
  AGENT_GRAPH.drag={nodeId:nodeId,pointerId:e.pointerId};
  node.style.cursor="grabbing";
  node.addEventListener("pointermove",dragAgentMove);
  node.addEventListener("pointerup",dragAgentEnd);
  node.addEventListener("pointercancel",dragAgentEnd);
}

function dragAgentMove(e){
  if(!AGENT_GRAPH.drag)return;
  var stage=document.getElementById("agentGraphStage");
  var rect=stage.getBoundingClientRect();
  var x=Math.max(5,Math.min(95,((e.clientX-rect.left)/rect.width)*100));
  var y=Math.max(5,Math.min(95,((e.clientY-rect.top)/rect.height)*100));
  AGENT_GRAPH.layout[AGENT_GRAPH.drag.nodeId]={x:x,y:y};
  var node=document.getElementById("agentNode-"+AGENT_GRAPH.drag.nodeId);
  if(node){node.style.left=x+"%";node.style.top=y+"%"}
  renderAgentEdges();
}

function dragAgentEnd(e){
  var drag=AGENT_GRAPH.drag;
  if(!drag)return;
  var node=document.getElementById("agentNode-"+drag.nodeId);
  if(node){
    node.style.cursor="grab";
    node.removeEventListener("pointermove",dragAgentMove);
    node.removeEventListener("pointerup",dragAgentEnd);
    node.removeEventListener("pointercancel",dragAgentEnd);
  }
  AGENT_GRAPH.drag=null;
  var payload={nodes:{}};
  payload.nodes[drag.nodeId]=AGENT_GRAPH.layout[drag.nodeId];
  fetch("/api/agents/layout",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)}).catch(function(){});
}

function resetAgentLayout(){
  fetch("/api/agents/layout",{method:"DELETE"}).then(function(){return refreshAgentGraph()});
}

function switchAgent(agentId){
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  const navItem=document.querySelector('.nav-item[data-agent="'+agentId+'"]');
  if(navItem)navItem.classList.add('active');
  document.querySelectorAll('.agent-panel').forEach(p=>p.classList.remove('active'));
  const panel=document.getElementById('panel-'+agentId);
  if(panel)panel.classList.add('active');
  if(agentId==="sales"){loadSalesWorkspace()}
  if(agentId==="dev"){loadDevWorkspace()}
}

function updateClock(){
  const now=new Date();
  document.getElementById('clock').textContent=now.toLocaleTimeString('th-TH',{hour:'2-digit',minute:'2-digit'});
}
updateClock();setInterval(updateClock,30000);

function escapeHtml(value){
  return String(value==null?"":value).replace(/[&<>"']/g,function(ch){
    return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch];
  });
}

function findSalesNotebook(id){
  for(var i=0;i<SALES_STATE.notebooks.length;i++){
    if(SALES_STATE.notebooks[i].id===id)return SALES_STATE.notebooks[i];
  }
  return null;
}

function loadSalesWorkspace(){
  if(SALES_STATE.loading)return;
  SALES_STATE.loading=true;
  var notice=document.getElementById("salesNotice");
  var noticeText=document.getElementById("salesNoticeText");
  if(notice&&noticeText){notice.style.display="flex";noticeText.textContent="กำลังโหลดประวัติ Sales จริงจากระบบ"}
  Promise.all([
    fetch("/api/notebooks").then(function(r){return r.json()}).catch(function(e){return {success:false,error:String(e),data:[]}}),
    fetch("/api/last-pipeline").then(function(r){return r.json()}).catch(function(e){return {success:false,error:String(e),data:null}})
  ]).then(function(results){
    var notebookResp=results[0]||{};
    var pipelineResp=results[1]||{};
    SALES_STATE.notebooks=notebookResp.success&&notebookResp.data?notebookResp.data:[];
    var salesBadge=document.getElementById("salesNavBadge");
    if(salesBadge)salesBadge.textContent=String(SALES_STATE.notebooks.length);
    SALES_STATE.lastPipeline=pipelineResp.success?pipelineResp.data:null;
    if(SALES_STATE.selectedNotebookId&&!findSalesNotebook(SALES_STATE.selectedNotebookId)){
      SALES_STATE.selectedNotebookId="";
      SALES_STATE.selectedNotebookContent="";
    }
    if(!SALES_STATE.selectedNotebookId&&SALES_STATE.notebooks.length){
      SALES_STATE.selectedNotebookId=SALES_STATE.notebooks[0].id;
      SALES_STATE.selectedNotebookContent="";
    }
    renderSalesNotebooks();
    updateSalesNotice();
    if(SALES_STATE.selectedNotebookId&&!SALES_STATE.selectedNotebookContent){
      viewSalesNotebook(SALES_STATE.selectedNotebookId);
    }else{
      renderSalesChat();
    }
  }).finally(function(){
    SALES_STATE.loading=false;
  });
}

function updateSalesNotice(){
  var notice=document.getElementById("salesNotice");
  var noticeText=document.getElementById("salesNoticeText");
  if(!notice||!noticeText)return;
  var count=SALES_STATE.notebooks.length;
  var hasPipeline=!!(SALES_STATE.lastPipeline&&SALES_STATE.lastPipeline.conversation_context);
  if(count===0&&!hasPipeline){
    notice.className="alert alert-warn";
    noticeText.textContent="ยังไม่มี Sales notebook หรือประวัติแชทจริงในระบบ";
    return;
  }
  notice.className="alert alert-info";
  noticeText.textContent="พบ notebook จริง "+count+" ไฟล์ และประวัติแชทล่าสุด"+(hasPipeline?"พร้อมแสดง":"ยังไม่มีในรอบล่าสุด");
}

function renderSalesNotebooks(){
  var list=document.getElementById("salesNotebookList");
  if(!list)return;
  list.innerHTML="";
  if(!SALES_STATE.notebooks.length){
    list.innerHTML='<div class="empty-state"><p>ยังไม่มี notebook จริงใน data/notebooks</p></div>';
    SALES_STATE.selectedNotebookId="";
    SALES_STATE.selectedNotebookContent="";
    var emptyViewer=document.getElementById("salesNotebookViewer");
    if(emptyViewer)emptyViewer.innerHTML='<div class="empty-state"><p>เลือก notebook เพื่อเปิดอ่านไฟล์จริง</p></div>';
    return;
  }
  for(var i=0;i<SALES_STATE.notebooks.length;i++){
    (function(nb){
      var item=document.createElement("div");
      item.className="notebook-item";
      if(nb.id===SALES_STATE.selectedNotebookId)item.style.background="var(--bg-hover)";
      item.addEventListener("click",function(){viewSalesNotebook(nb.id)});

      var body=document.createElement("div");
      body.style.minWidth="0";
      var title=document.createElement("div");
      title.className="nb-title";
      title.textContent=nb.title||("Sales Notebook — "+nb.id);
      var meta=document.createElement("div");
      meta.className="nb-meta";
      var parts=[];
      if(nb.company)parts.push(nb.company);
      if(nb.customer)parts.push(nb.customer);
      if(nb.updated)parts.push("updated "+nb.updated);
      parts.push(nb.id);
      meta.textContent=parts.join(" · ");
      body.appendChild(title);
      body.appendChild(meta);

      var actions=document.createElement("div");
      actions.className="notebook-actions";
      var status=document.createElement("span");
      status.className=nb.status==="confirmed"?"tag tag-green":"tag tag-amber";
      status.textContent=nb.status==="confirmed"?"confirmed":"in progress";
      var del=document.createElement("button");
      del.className="btn btn-danger btn-sm";
      del.textContent="Delete";
      del.addEventListener("click",function(e){e.stopPropagation();deleteSalesNotebook(nb.id)});
      actions.appendChild(status);
      actions.appendChild(del);

      item.appendChild(body);
      item.appendChild(actions);
      list.appendChild(item);
    })(SALES_STATE.notebooks[i]);
  }
}

function viewSalesNotebook(id){
  SALES_STATE.selectedNotebookId=id;
  renderSalesNotebooks();
  var viewer=document.getElementById("salesNotebookViewer");
  if(viewer)viewer.innerHTML='<div class="empty-state"><p>กำลังเปิดไฟล์ notebook จริง...</p></div>';
  fetch("/api/notebooks/"+encodeURIComponent(id)).then(function(r){return r.json()}).then(function(resp){
    if(!resp.success){
      if(viewer)viewer.innerHTML='<div class="empty-state"><p>เปิด notebook ไม่สำเร็จ</p></div>';
      return;
    }
    SALES_STATE.selectedNotebookContent=resp.data||"";
    renderSalesNotebookViewer();
    renderSalesChat();
  }).catch(function(){
    if(viewer)viewer.innerHTML='<div class="empty-state"><p>เปิด notebook ไม่สำเร็จ</p></div>';
  });
}

function renderSalesNotebookViewer(){
  var viewer=document.getElementById("salesNotebookViewer");
  if(!viewer)return;
  var text=SALES_STATE.selectedNotebookContent||"";
  if(!text){
    viewer.innerHTML='<div class="empty-state"><p>เลือก notebook เพื่อเปิดอ่านไฟล์จริง</p></div>';
    return;
  }
  var title=getNotebookTitle(text);
  var status=getNotebookMeta(text,"Status");
  var created=getNotebookMeta(text,"Created");
  var updated=getNotebookMeta(text,"Last Updated");
  var confirmed=status.indexOf("confirmed")>=0;
  var name=getNotebookTableValue(text,"Name")||"-";
  var company=getNotebookTableValue(text,"Company")||"-";
  var contact=getNotebookTableValue(text,"Contact")||"-";
  var logs=parseSalesChatMessages(text);
  var logHtml="";
  for(var i=0;i<logs.length&&i<12;i++){
    logHtml+='<div class="notebook-log-line '+(logs[i].role==="user"?"user":"agent")+'">'+escapeHtml((logs[i].role==="user"?"ลูกค้า: ":"Aetox: ")+logs[i].text)+'</div>';
  }
  if(!logHtml)logHtml='<div style="color:var(--ink-dim)">ยังไม่มี conversation log</div>';
  viewer.innerHTML=
    '<div class="notebook-render">'+
      '<div class="notebook-render-head">'+
        '<div><div class="notebook-render-title">'+escapeHtml(title)+'</div><div style="font-size:.72em;color:var(--ink-dim);margin-top:3px">'+escapeHtml(updated?("Updated "+updated):"")+'</div></div>'+
        '<span class="tag '+(confirmed?"tag-green":"tag-amber")+'">'+escapeHtml(confirmed?"confirmed":"in progress")+'</span>'+
      '</div>'+
      '<div class="notebook-render-meta">'+
        notebookField("Name",name)+notebookField("Company",company)+notebookField("Contact",contact)+notebookField("Created",created||"-")+
      '</div>'+
      '<div class="notebook-section"><h4>Business Requirements</h4>'+
        notebookRequirementBlock("Pain Points",getNotebookItems(text,"Pain Points"))+
        notebookRequirementBlock("Needs",getNotebookItems(text,"Needs"))+
        notebookRequirementBlock("Goals",getNotebookItems(text,"Goals"))+
        notebookRequirementBlock("Timeline",getNotebookItems(text,"Timeline"))+
      '</div>'+
      '<div class="notebook-section"><h4>Conversation Log</h4><div class="notebook-log">'+logHtml+'</div></div>'+
    '</div>';
}

function getNotebookTitle(text){
  var first=String(text||"").split(/\r?\n/)[0]||"Sales Notebook";
  return first.replace(/^#\s*/,"").replace(/^📓\s*/,"").trim()||"Sales Notebook";
}

function getNotebookMeta(text,key){
  var re=new RegExp("\\*\\*"+key+":\\*\\*\\s*([^\\n]+)");
  var m=String(text||"").match(re);
  return m?m[1].trim():"";
}

function getNotebookTableValue(text,field){
  var re=new RegExp("\\|\\s*"+field+"\\s*\\|\\s*(.*?)\\s*\\|");
  var m=String(text||"").match(re);
  var val=m?m[1].trim():"";
  return val==="|"?"":val;
}

function getNotebookSection(text,label){
  var re=new RegExp("### "+label+"\\s*\\n([\\s\\S]*?)(?=\\n###|\\n---|\\n## |$)");
  var m=String(text||"").match(re);
  return m?m[1].trim():"";
}

function getNotebookItems(text,label){
  var section=getNotebookSection(text,label);
  if(!section||section.indexOf("ยังไม่มีข้อมูล")>=0)return [];
  var lines=section.split(/\r?\n/);
  var items=[];
  for(var i=0;i<lines.length;i++){
    var line=lines[i].replace(/^-\s*/,"").trim();
    if(line&&line.indexOf("ยังไม่มีข้อมูล")<0)items.push(line);
  }
  return items;
}

function notebookField(label,value){
  return '<div class="notebook-field"><div class="notebook-field-label">'+escapeHtml(label)+'</div><div class="notebook-field-value">'+escapeHtml(value||"-")+'</div></div>';
}

function notebookRequirementBlock(label,items){
  var html='<div style="margin-bottom:10px"><div class="notebook-field-label">'+escapeHtml(label)+'</div>';
  if(!items.length){
    html+='<div style="color:var(--ink-dim)">ยังไม่มีข้อมูล</div></div>';
    return html;
  }
  html+='<div class="notebook-list">';
  for(var i=0;i<items.length;i++){
    html+='<div class="notebook-list-item"><span>'+escapeHtml(items[i])+'</span></div>';
  }
  html+='</div></div>';
  return html;
}

function parseSalesChatMessages(text){
  var messages=[];
  var lines=String(text||"").replace(/\[NB:[^\]\r\n]+\]\n?/g,"").split(/\r?\n/);
  for(var i=0;i<lines.length;i++){
    var line=lines[i].trim();
    if(!line)continue;
    line=line.replace(/^-\s*[^|]+\|\s*/,"").trim();
    var user=line.match(/^ลูกค้า:\s*(.+)$/);
    var agent=line.match(/^Aetox:\s*(.+)$/);
    if(user&&user[1])messages.push({role:"user",text:user[1]});
    if(agent&&agent[1])messages.push({role:"agent",text:agent[1]});
  }
  return messages;
}

function renderSalesChat(){
  var box=document.getElementById("salesChatMessages");
  if(!box)return;
  var title=document.getElementById("salesChatTitle");
  var status=document.getElementById("salesChatStatus");
  var source="Last pipeline";
  var context=SALES_STATE.lastPipeline&&SALES_STATE.lastPipeline.conversation_context?SALES_STATE.lastPipeline.conversation_context:"";
  var messages=parseSalesChatMessages(context);
  if(!messages.length&&SALES_STATE.selectedNotebookContent){
    source="Notebook log";
    messages=parseSalesChatMessages(SALES_STATE.selectedNotebookContent);
  }
  var selected=findSalesNotebook(SALES_STATE.selectedNotebookId);
  if(title){
    title.textContent=selected?(selected.title||selected.id):"Real customer conversation";
  }
  if(status){
    status.className=source==="Notebook log"?"tag tag-amber":"tag tag-blue";
    status.textContent=source;
  }
  box.innerHTML="";
  if(!messages.length){
    box.innerHTML='<div class="empty-state"><p>ยังไม่มีประวัติแชทจริงให้แสดง</p></div>';
    return;
  }
  for(var i=0;i<messages.length;i++){
    var msg=document.createElement("div");
    msg.className=messages[i].role==="user"?"chat-msg user":"chat-msg agent";
    msg.innerHTML=escapeHtml(messages[i].text)+'<span class="msg-time">'+escapeHtml(source)+'</span>';
    box.appendChild(msg);
  }
  box.scrollTop=box.scrollHeight;
}

function deleteSalesNotebook(id){
  if(!confirm("ลบ Sales Notebook นี้จริงไหม?\\n"+id))return;
  fetch("/api/notebooks/"+encodeURIComponent(id),{method:"DELETE"}).then(function(r){return r.json()}).then(function(resp){
    if(!resp.success){alert(resp.message||resp.error||"Delete failed");return}
    if(SALES_STATE.selectedNotebookId===id){
      SALES_STATE.selectedNotebookId="";
      SALES_STATE.selectedNotebookContent="";
      var viewer=document.getElementById("salesNotebookViewer");
      if(viewer)viewer.innerHTML='<div class="empty-state"><p>เลือก notebook เพื่อเปิดอ่านไฟล์จริง</p></div>';
    }
    loadSalesWorkspace();
  }).catch(function(){alert("Delete failed")});
}

function deleteAllSalesNotebooks(){
  if(!confirm("ลบ Sales Notebook ทั้งหมดจริงไหม?"))return;
  fetch("/api/notebooks",{method:"DELETE"}).then(function(r){return r.json()}).then(function(resp){
    if(!resp.success){alert(resp.error||"Delete all failed");return}
    SALES_STATE.selectedNotebookId="";
    SALES_STATE.selectedNotebookContent="";
    loadSalesWorkspace();
  }).catch(function(){alert("Delete all failed")});
}

function loadDevWorkspace(){
  if(DEV_STATE.loading)return;
  DEV_STATE.loading=true;
  setDevNotice("info","กำลังโหลดงาน Dev จริงจาก output/websites");
  Promise.all([
    fetch("/api/projects").then(function(r){return r.json()}).catch(function(e){return {success:false,error:String(e),data:[]}}),
    fetch("/api/last-pipeline").then(function(r){return r.json()}).catch(function(e){return {success:false,error:String(e),data:null}})
  ]).then(function(results){
    var projectsResp=results[0]||{};
    DEV_STATE.projects=projectsResp.success&&projectsResp.data?projectsResp.data:[];
    if(DEV_STATE.selectedProject&&!findDevProject(DEV_STATE.selectedProject)){
      DEV_STATE.selectedProject="";
      DEV_STATE.detail=null;
      DEV_STATE.selectedFile="";
    }
    if(!DEV_STATE.selectedProject&&DEV_STATE.projects.length){
      DEV_STATE.selectedProject=DEV_STATE.projects[0].name;
    }
    if(!DEV_STATE.selectedProject){
      renderDevEmpty(projectsResp.success?"ยังไม่มีโปรเจกต์ที่ Dev Agent สร้างจริง":"โหลดโปรเจกต์ไม่สำเร็จ");
      return;
    }
    return fetch("/api/projects/"+encodeURIComponent(DEV_STATE.selectedProject)).then(function(r){return r.json()}).then(function(detailResp){
      if(!detailResp.success){
        renderDevEmpty("เปิดโปรเจกต์ไม่สำเร็จ");
        return;
      }
      DEV_STATE.detail=detailResp.data;
      renderDevWorkspace();
    });
  }).catch(function(){
    renderDevEmpty("โหลดงาน Dev ไม่สำเร็จ");
  }).finally(function(){
    DEV_STATE.loading=false;
  });
}

function findDevProject(name){
  for(var i=0;i<DEV_STATE.projects.length;i++){
    if(DEV_STATE.projects[i].name===name)return DEV_STATE.projects[i];
  }
  return null;
}

function setDevNotice(kind,text){
  var notice=document.getElementById("devNotice");
  var noticeText=document.getElementById("devNoticeText");
  if(!notice||!noticeText)return;
  notice.className="alert "+(kind==="error"?"alert-error":kind==="warn"?"alert-warn":"alert-info");
  noticeText.textContent=text;
}

function renderDevEmpty(message){
  DEV_STATE.detail=null;
  DEV_STATE.selectedFile="";
  setDevNotice("warn",message);
  var status=document.getElementById("devStatusTag");
  var projectTag=document.getElementById("devProjectTag");
  var fileMeta=document.getElementById("devFileMeta");
  var fileTree=document.getElementById("devFileTree");
  var preview=document.getElementById("devPreview");
  var previewMeta=document.getElementById("devPreviewMeta");
  var logs=document.getElementById("devBuildLogs");
  var path=document.getElementById("devProjectPath");
  if(status){status.className="tag";status.textContent="Idle"}
  if(projectTag)projectTag.textContent="Project: -";
  if(fileMeta)fileMeta.textContent="0 files";
  if(fileTree)fileTree.innerHTML='<div class="empty-state"><p>'+escapeHtml(message)+'</p></div>';
  if(previewMeta)previewMeta.textContent="HTML preview";
  if(preview)preview.innerHTML='<div class="empty-state"><p>ยังไม่มี HTML preview</p></div>';
  if(logs)logs.innerHTML='<div class="log-line log-info">No real Dev project output yet.</div>';
  if(path)path.textContent="ยังไม่มีโปรเจกต์";
}

function renderDevWorkspace(){
  var detail=DEV_STATE.detail||{};
  var files=detail.files||[];
  var status=document.getElementById("devStatusTag");
  var projectTag=document.getElementById("devProjectTag");
  var fileMeta=document.getElementById("devFileMeta");
  var path=document.getElementById("devProjectPath");
  if(status){status.className="tag tag-green";status.textContent="Ready"}
  if(projectTag)projectTag.textContent="Project: "+(detail.name||DEV_STATE.selectedProject);
  if(fileMeta)fileMeta.textContent=files.length+" files · "+formatBytes(totalDevFileSize(files));
  if(path)path.textContent=detail.path||"";
  setDevNotice("info","แสดงงาน Dev จริงจาก output/websites: "+(detail.name||DEV_STATE.selectedProject));
  if(!DEV_STATE.selectedFile&&files.length){
    var htmlFile=null;
    for(var i=0;i<files.length;i++){if(files[i].is_html&&!htmlFile)htmlFile=files[i]}
    DEV_STATE.selectedFile=(htmlFile||files[0]).name;
  }
  renderDevFiles();
  renderDevSelectedFile();
  renderDevLogs();
}

function renderDevFiles(){
  var fileTree=document.getElementById("devFileTree");
  if(!fileTree)return;
  var detail=DEV_STATE.detail||{};
  var files=detail.files||[];
  fileTree.innerHTML="";
  if(!files.length){
    fileTree.innerHTML='<div class="empty-state"><p>โปรเจกต์นี้ยังไม่มีไฟล์</p></div>';
    return;
  }
  for(var i=0;i<files.length;i++){
    (function(file){
      var item=document.createElement("div");
      item.className="file-item"+(file.name===DEV_STATE.selectedFile?" active":"");
      item.addEventListener("click",function(){
        DEV_STATE.selectedFile=file.name;
        renderDevFiles();
        renderDevSelectedFile();
      });
      item.innerHTML='<svg width="13" height="13" viewBox="0 0 13 13"><path d="M2 2h9v9H2V2z" stroke="currentColor" stroke-width="1.2" fill="none"/><path d="M4 4h5v1H4zM4 6h5v1H4zM4 8h3v1H4z" fill="currentColor" opacity=".5"/></svg><span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+escapeHtml(file.name)+'</span><span class="file-size">'+escapeHtml(formatBytes(file.size||0))+'</span>';
      var actions=document.createElement("div");
      actions.className="file-actions";
      var del=document.createElement("button");
      del.className="btn btn-danger btn-sm file-delete-btn";
      del.textContent="Delete";
      del.addEventListener("click",function(e){
        e.stopPropagation();
        deleteDevFile(file.name);
      });
      actions.appendChild(del);
      item.appendChild(actions);
      fileTree.appendChild(item);
    })(files[i]);
  }
}

function deleteDevFile(fileName){
  if(!DEV_STATE.selectedProject||!fileName)return;
  if(!confirm("ลบไฟล์ Dev นี้จริงไหม?\\n"+fileName))return;
  fetch("/api/projects/"+encodeURIComponent(DEV_STATE.selectedProject)+"/files/"+encodeURIComponent(fileName),{method:"DELETE"}).then(function(r){return r.json()}).then(function(resp){
    if(!resp.success){alert(resp.message||resp.error||"Delete failed");return}
    if(DEV_STATE.selectedFile===fileName)DEV_STATE.selectedFile="";
    DEV_STATE.detail=null;
    loadDevWorkspace();
  }).catch(function(){alert("Delete failed")});
}

function renderDevSelectedFile(){
  var preview=document.getElementById("devPreview");
  if(!preview)return;
  var meta=document.getElementById("devPreviewMeta");
  var file=getSelectedDevFile();
  preview.innerHTML="";
  if(!file){
    if(meta)meta.textContent="No file selected";
    preview.innerHTML='<div class="empty-state"><p>เลือกไฟล์เพื่อดู preview</p></div>';
    return;
  }
  if(meta)meta.textContent=file.name+" · "+formatBytes(file.size||0);
  if(file.is_html&&file.content){
    var shell=document.createElement("div");
    shell.className="dev-preview-shell";
    var bar=document.createElement("div");
    bar.className="dev-preview-bar";
    bar.innerHTML='<span>Preview: '+escapeHtml(file.name)+'</span><span class="tag tag-green">HTML loaded</span>';
    var iframe=document.createElement("iframe");
    iframe.className="dev-preview-frame";
    iframe.setAttribute("sandbox","");
    iframe.setAttribute("srcdoc",file.content);
    shell.appendChild(bar);
    shell.appendChild(iframe);
    preview.appendChild(shell);
    return;
  }
  var pre=document.createElement("pre");
  pre.className="code-block";
  pre.style.margin="0";
  pre.style.width="100%";
  pre.style.height="100%";
  pre.style.border="0";
  pre.style.borderRadius="0";
  pre.textContent=file.content||("ไม่มี preview สำหรับ "+file.name);
  preview.appendChild(pre);
}

function renderDevLogs(){
  var logs=document.getElementById("devBuildLogs");
  if(!logs)return;
  var detail=DEV_STATE.detail||{};
  var files=detail.files||[];
  logs.innerHTML="";
  logs.innerHTML+='<div class="log-line log-success">✓ Loaded real project: '+escapeHtml(detail.name||DEV_STATE.selectedProject)+'</div>';
  logs.innerHTML+='<div class="log-line log-info">→ Files found: '+files.length+'</div>';
  var htmlCount=0;
  for(var i=0;i<files.length;i++){if(files[i].is_html)htmlCount++}
  logs.innerHTML+='<div class="log-line '+(htmlCount?"log-success":"log-warn")+'">'+(htmlCount?"✓":"⚠")+' HTML previews: '+htmlCount+'</div>';
  logs.innerHTML+='<div class="log-line log-info">Path: '+escapeHtml(detail.path||"")+'</div>';
}

function getSelectedDevFile(){
  var detail=DEV_STATE.detail||{};
  var files=detail.files||[];
  for(var i=0;i<files.length;i++){
    if(files[i].name===DEV_STATE.selectedFile)return files[i];
  }
  return files.length?files[0]:null;
}

function totalDevFileSize(files){
  var total=0;
  for(var i=0;i<files.length;i++){total+=Number(files[i].size||0)}
  return total;
}

function formatBytes(size){
  size=Number(size||0);
  if(size<1024)return size+" B";
  if(size<1024*1024)return Math.round(size/1024)+" KB";
  return (size/1024/1024).toFixed(1)+" MB";
}

function showHandoffBrief(agentId){
  var brief=document.getElementById('handoffBrief');
  brief.style.display=brief.style.display==='none'?'block':'none';
}

function simulatePipeline(){
  var steps=['sales','research','content','dev','data','final'];
  var stepEls=steps.map(function(id){return document.getElementById('flowNode-'+id)});
  var connectors=document.querySelectorAll('.flow-connector');
  var pipelineSteps=document.querySelectorAll('.pipeline-step');
  var currentStep=0;
  setInterval(function(){
    stepEls.forEach(function(el){if(el){el.classList.remove('active','done')}});
    connectors.forEach(function(el){el.classList.remove('active','done')});
    pipelineSteps.forEach(function(el,i){if(i===0)el.className='pipeline-step done';else el.className='pipeline-step pending'});
    for(var i=0;i<currentStep&&i<stepEls.length;i++){if(stepEls[i])stepEls[i].classList.add('done');if(connectors[i])connectors[i].classList.add('done');if(pipelineSteps[i+1])pipelineSteps[i+1].className='pipeline-step done'}
    if(stepEls[currentStep])stepEls[currentStep].classList.add('active');
    if(connectors[currentStep])connectors[currentStep].classList.add('active');
    if(pipelineSteps[currentStep+1])pipelineSteps[currentStep+1].className='pipeline-step active';
    currentStep=(currentStep+1)%(stepEls.length+1);
  },4000);
}
refreshAgentGraph();
loadSalesWorkspace();
loadDevWorkspace();
setInterval(refreshAgentGraph,3000);
setInterval(function(){
  var panel=document.getElementById("panel-sales");
  if(panel&&panel.classList.contains("active"))loadSalesWorkspace();
},7000);
setInterval(function(){
  var panel=document.getElementById("panel-dev");
  if(panel&&panel.classList.contains("active"))loadDevWorkspace();
},9000);
window.addEventListener("resize",renderAgentEdges);

document.querySelectorAll('.nav-item').forEach(function(item){
  item.addEventListener('click',function(){document.getElementById('mainContent').scrollTop=0});
});
</script>

</body>
</html>"""
