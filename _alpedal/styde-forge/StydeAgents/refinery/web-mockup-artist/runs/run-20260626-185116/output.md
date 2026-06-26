```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Command Center</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#080d1a;--surface:rgba(14,22,48,0.88);--surface2:rgba(20,32,64,0.75);--border:rgba(0,212,170,0.18);--accent:#00d4aa;--accent2:#f0a030;--warn:#f06430;--err:#e03550;--text:#d4e0f0;--muted:#5a6a8a;--font:system-ui,-apple-system,'Segoe UI',sans-serif;--mono:'Cascadia Code','Fira Code','JetBrains Mono',monospace;--radius:10px;--shadow:0 4px 24px rgba(0,0,0,0.5)}
html{font-size:15px}
body{background:var(--bg);color:var(--text);font-family:var(--font);min-height:100vh;overflow-x:hidden;background-image:radial-gradient(ellipse at 20% 10%,rgba(0,212,170,0.04) 0%,transparent 60%),radial-gradient(ellipse at 80% 90%,rgba(240,160,48,0.03) 0%,transparent 60%)}
a{color:var(--accent);text-decoration:none}
a:hover{color:#fff}
/* HEADER */
.header{position:sticky;top:0;z-index:100;background:rgba(8,13,26,0.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between}
.header-left{display:flex;align-items:center;gap:16px}
.header-logo{font-weight:700;font-size:1.15rem;letter-spacing:0.5px;color:#fff;display:flex;align-items:center;gap:8px}
.header-logo .pulse{width:8px;height:8px;border-radius:50%;background:var(--accent);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,212,170,0.6)}50%{opacity:0.6;box-shadow:0 0 0 6px rgba(0,212,170,0)}}
.header-right{display:flex;align-items:center;gap:16px}
.header-status{font-size:0.75rem;color:var(--muted);display:flex;align-items:center;gap:6px}
.header-status .dot{width:6px;height:6px;border-radius:50%;background:var(--accent)}
.hamburger{display:none;background:none;border:1px solid var(--border);color:var(--text);font-size:1.3rem;padding:4px 10px;border-radius:6px;cursor:pointer}
/* BREADCRUMB */
.breadcrumb{display:flex;align-items:center;gap:6px;padding:10px 24px;font-size:0.8rem;color:var(--muted);border-bottom:1px solid rgba(255,255,255,0.04)}
.breadcrumb a{color:var(--muted)}
.breadcrumb a:hover{color:var(--accent)}
.breadcrumb span{color:var(--text)}
/* NAV SIDEBAR */
.nav-overlay{display:none}
.app-layout{display:flex;min-height:calc(100vh - 56px - 34px - 48px)}
.sidebar{width:200px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:12px 0}
.sidebar-item{display:flex;align-items:center;gap:10px;padding:10px 20px;color:var(--muted);cursor:pointer;transition:all 0.15s;border-left:3px solid transparent;font-size:0.88rem}
.sidebar-item:hover{color:var(--text);background:rgba(0,212,170,0.06)}
.sidebar-item.active{color:var(--accent);border-left-color:var(--accent);background:rgba(0,212,170,0.08)}
.sidebar-item .ico{font-size:1.05rem;width:20px;text-align:center}
/* MAIN */
.main{flex:1;padding:20px 24px 24px;max-width:100%;overflow:hidden}
/* DASHBOARD GRID */
.dash-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-bottom:20px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:border-color 0.2s}
.card:hover{border-color:rgba(0,212,170,0.35)}
.card-title{font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:8px}
.card-value{font-size:1.8rem;font-weight:700;color:#fff;font-family:var(--mono)}
.card-sub{font-size:0.78rem;color:var(--muted);margin-top:2px}
/* METRICS GRID */
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:24px}
.metric-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.metric-card .label{font-size:0.72rem;text-transform:uppercase;letter-spacing:0.8px;color:var(--muted)}
.metric-card .val{font-size:1.3rem;font-weight:600;color:#fff;font-family:var(--mono)}
.metric-card .change{font-size:0.7rem;padding:2px 6px;border-radius:4px}
.metric-card .change.up{color:var(--accent);background:rgba(0,212,170,0.1)}
.metric-card .change.down{color:var(--err);background:rgba(224,53,80,0.1)}
/* AGENT LIST */
.agent-list{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.agent-row{display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--surface2);border-radius:6px;font-size:0.85rem}
.agent-row .status-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.agent-row .status-dot.on{background:var(--accent);box-shadow:0 0 6px rgba(0,212,170,0.4)}
.agent-row .status-dot.idle{background:var(--accent2)}
.agent-row .status-dot.off{background:var(--err)}
.agent-row .name{flex:1;color:#fff}
.agent-row .task{color:var(--muted);font-size:0.78rem;max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.agent-row .gpu-bar{width:60px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;flex-shrink:0}
.agent-row .gpu-bar .fill{height:100%;border-radius:2px;transition:width 0.4s ease}
/* ACTIVITY FEED */
.activity-feed{display:flex;flex-direction:column;gap:6px;margin-top:8px;max-height:300px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--border) transparent}
.activity-feed::-webkit-scrollbar{width:4px}
.activity-feed::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.activity-item{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.03);font-size:0.82rem}
.activity-item .time{color:var(--muted);font-family:var(--mono);font-size:0.72rem;white-space:nowrap;width:50px;flex-shrink:0}
.activity-item .msg{color:var(--text)}
.activity-item .msg .hl{color:var(--accent)}
/* GPU MONITOR */
.gpu-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:8px}
.gpu-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px;text-align:center}
.gpu-card .gpu-label{font-size:0.72rem;color:var(--muted);margin-bottom:4px}
.gpu-card .gpu-percent{font-size:1.6rem;font-weight:700;color:#fff;font-family:var(--mono)}
.gpu-card .gpu-bar-lg{width:100%;height:6px;background:rgba(255,255,255,0.05);border-radius:3px;margin-top:6px;overflow:hidden}
.gpu-card .gpu-bar-lg .fill{height:100%;border-radius:3px;transition:width 0.5s ease}
/* COLLAPSIBLE */
.collapsible-header{display:flex;justify-content:space-between;align-items:center;cursor:pointer;padding:8px 0;user-select:none}
.collapsible-header .toggle{font-size:0.8rem;color:var(--muted);transition:transform 0.2s}
.collapsible-header.collapsed .toggle{transform:rotate(-90deg)}
.collapsible-body{max-height:800px;overflow:hidden;transition:max-height 0.35s ease}
.collapsible-body.collapsed{max-height:0;overflow:hidden}
/* STATE INDICATORS */
.state-loading,.state-empty,.state-error{padding:20px;text-align:center;color:var(--muted);font-size:0.85rem;display:none}
.state-loading .spinner{display:inline-block;width:20px;height:20px;border:2px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin 0.7s linear infinite;margin-bottom:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.state-error{color:var(--err)}
/* FOOTER */
.footer{border-top:1px solid var(--border);padding:12px 24px;display:flex;justify-content:space-between;align-items:center;font-size:0.75rem;color:var(--muted)}
.footer-links{display:flex;gap:16px}
.footer-links a{color:var(--muted)}
.footer-links a:hover{color:var(--accent)}
/* RESPONSIVE */
@media(max-width:820px){
  .sidebar{position:fixed;top:56px;left:-220px;width:220px;height:calc(100vh - 56px);z-index:200;transition:left 0.25s;border-right:1px solid var(--border)}
  .sidebar.open{left:0}
  .nav-overlay{display:none;position:fixed;top:56px;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:199}
  .nav-overlay.show{display:block}
  .hamburger{display:block}
  .dash-grid{grid-template-columns:1fr}
  .metrics-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:480px){
  .header{padding:0 12px}
  .breadcrumb{padding:8px 12px;font-size:0.72rem}
  .main{padding:12px}
  .metrics-grid{grid-template-columns:1fr}
  .gpu-grid{grid-template-columns:1fr 1fr}
  .header-status .label{display:none}
}
</style>
</head>
<body>
<header class="header">
  <div class="header-left">
    <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation">☰</button>
    <div class="header-logo">
      <span class="pulse"></span>
      styde/forge
    </div>
  </div>
  <div class="header-right">
    <span class="header-status"><span class="dot"></span><span class="label">All Systems Nominal</span></span>
    <span style="color:var(--muted);font-size:0.82rem;font-family:var(--mono)">v2.4.1</span>
  </div>
</header>
<div class="breadcrumb">
  <a href="#">styde.se</a> <span>›</span>
  <a href="#">forge</a> <span>›</span>
  <span>command-center</span>
</div>
<div class="app-layout">
  <div class="nav-overlay" id="navOverlay"></div>
  <nav class="sidebar" id="sidebar">
    <div class="sidebar-item active" data-section="dashboard"><span class="ico">◉</span> Dashboard</div>
    <div class="sidebar-item" data-section="agents"><span class="ico">◆</span> Agents</div>
    <div class="sidebar-item" data-section="pipelines"><span class="ico">▷</span> Pipelines</div>
    <div class="sidebar-item" data-section="models"><span class="ico">⊞</span> Models</div>
    <div class="sidebar-item" data-section="gpu"><span class="ico">▓</span> GPU Pool</div>
    <div class="sidebar-item" data-section="logs"><span class="ico">☰</span> Logs</div>
    <div class="sidebar-item" data-section="settings"><span class="ico">⚙</span> Settings</div>
  </nav>
  <main class="main">
    <!-- Metrics cards row (loading/empty/error states for the whole dashboard) -->
    <div class="state-loading" id="dashLoading"><div class="spinner"></div><br>Loading dashboard data...</div>
    <div class="state-empty" id="dashEmpty">No dashboard data available. Configure a data source to begin.</div>
    <div class="state-error" id="dashError">Failed to load dashboard. Check backend connectivity and retry.</div>
    <div id="dashContent">
    <div class="metrics-grid" id="metricsGrid">
      <div class="metric-card">
        <div><div class="label">Active Agents</div><div class="val" id="metricActive">12</div></div>
        <span class="change up">+3</span>
      </div>
      <div class="metric-card">
        <div><div class="label">Pipeline Runs</div><div class="val" id="metricRuns">247</div></div>
        <span class="change up">+18</span>
      </div>
      <div class="metric-card">
        <div><div class="label">GPU Util</div><div class="val" id="metricGpu">67%</div></div>
        <span class="change down">-4%</span>
      </div>
      <div class="metric-card">
        <div><div class="label">Queue Depth</div><div class="val" id="metricQueue">8</div></div>
        <span class="change up">−2</span>
      </div>
    </div>
    <div class="dash-grid">
      <!-- System Overview card (collapsible) -->
      <div class="card">
        <div class="collapsible-header" data-target="sysBody">
          <span class="card-title">System Overview</span>
          <span class="toggle">▼</span>
        </div>
        <div class="collapsible-body" id="sysBody">
          <div class="card-value" style="font-size:1.2rem">uptime 14d 6h 32m</div>
          <div class="card-sub">Cluster: forge-prod-01 · 8 nodes · 32 vCPUs · 128 GB RAM</div>
          <div style="margin-top:10px;display:flex;gap:20px;flex-wrap:wrap">
            <div><span style="color:var(--muted);font-size:0.72rem">MEM</span><br><span style="font-family:var(--mono);color:#fff">71.4 / 128 GB</span></div>
            <div><span style="color:var(--muted);font-size:0.72rem">CPU</span><br><span style="font-family:var(--mono);color:#fff">43% avg</span></div>
            <div><span style="color:var(--muted);font-size:0.72rem">DISK</span><br><span style="font-family:var(--mono);color:#fff">2.1 / 4 TB</span></div>
          </div>
        </div>
      </div>
      <!-- Agent Status -->
      <div class="card">
        <div class="collapsible-header" data-target="agentBody">
          <span class="card-title">Agent Status</span>
          <span class="toggle">▼</span>
        </div>
        <div class="collapsible-body" id="agentBody">
          <div class="state-loading" id="agentLoading"><div class="spinner"></div></div>
          <div class="state-empty" id="agentEmpty">No agents deployed to this environment.</div>
          <div class="state-error" id="agentError">Agent telemetry unreachable. Verify agent daemon status.</div>
          <div class="agent-list" id="agentList">
            <div class="agent-row"><span class="status-dot on"></span><span class="name">blueprint-engine</span><span class="task">generating · bp-104</span><div class="gpu-bar"><div class="fill" style="width:72%;background:var(--accent)"></div></div></div>
            <div class="agent-row"><span class="status-dot on"></span><span class="name">codex-agent</span><span class="task">reviewing · pr-39</span><div class="gpu-bar"><div class="fill" style="width:45%;background:var(--accent2)"></div></div></div>
            <div class="agent-row"><span class="status-dot idle"></span><span class="name">evaluator</span><span class="task">idle · awaiting batch</span><div class="gpu-bar"><div class="fill" style="width:8%;background:var(--accent2)"></div></div></div>
            <div class="agent-row"><span class="status-dot on"></span><span class="name">deploy-agent</span><span class="task">pushing · v2.4.1</span><div class="gpu-bar"><div class="fill" style="width:91%;background:var(--accent)"></div></div></div>
            <div class="agent-row"><span class="status-dot off"></span><span class="name">monitor-daemon</span><span class="task">offline</span><div class="gpu-bar"><div class="fill" style="width:0%;background:var(--err)"></div></div></div>
          </div>
        </div>
      </div>
    </div>
    <div class="dash-grid" style="margin-top:0">
      <!-- Activity Feed (collapsible) -->
      <div class="card">
        <div class="collapsible-header" data-target="feedBody">
          <span class="card-title">Activity Feed</span>
          <span class="toggle">▼</span>
        </div>
        <div class="collapsible-body" id="feedBody">
          <div class="state-loading" id="feedLoading"><div class="spinner"></div></div>
          <div class="state-empty" id="feedEmpty">No recent activity recorded for this session.</div>
          <div class="state-error" id="feedError">Activity stream disconnected. Check event bus health.</div>
          <div class="activity-feed" id="activityFeed">
            <div class="activity-item"><span class="time">14:32</span><span class="msg"><span class="hl">bp-104</span> generated — ready for review</span></div>
            <div class="activity-item"><span class="time">14:28</span><span class="msg"><span class="hl">codex-agent</span> completed review on pr-39</span></div>
            <div class="activity-item"><span class="time">14:22</span><span class="msg"><span class="hl">deploy-agent</span> staged v2.4.1 to staging</span></div>
            <div class="activity-item"><span class="time">14:15</span><span class="msg"><span class="hl">evaluator</span> batch #112 passed (28/28)</span></div>
            <div class="activity-item"><span class="time">14:08</span><span class="msg"><span class="hl">monitor-daemon</span> heartbeat timeout · auto-restart queued</span></div>
            <div class="activity-item"><span class="time">13:55</span><span class="msg"><span class="hl">blueprint-engine</span> queued bp-105, bp-106</span></div>
          </div>
        </div>
      </div>
      <!-- GPU Monitor (collapsible) -->
      <div class="card">
        <div class="collapsible-header" data-target="gpuBody">
          <span class="card-title">GPU Monitor</span>
          <span class="toggle">▼</span>
        </div>
        <div class="collapsible-body" id="gpuBody">
          <div class="state-loading" id="gpuLoading"><div class="spinner"></div></div>
          <div class="state-empty" id="gpuEmpty">No GPU devices detected on this cluster.</div>
          <div class="state-error" id="gpuError">GPU metrics endpoint unreachable. Verify nvidia-smi or AMDCard health.</div>
          <div class="gpu-grid" id="gpuGrid">
            <div class="gpu-card" data-gpu="0"><div class="gpu-label">A100-0</div><div class="gpu-percent">82%</div><div class="gpu-bar-lg"><div class="fill" style="width:82%;background:var(--accent)"></div></div></div>
            <div class="gpu-card" data-gpu="1"><div class="gpu-label">A100-1</div><div class="gpu-percent">47%</div><div class="gpu-bar-lg"><div class="fill" style="width:47%;background:var(--accent2)"></div></div></div>
            <div class="gpu-card" data-gpu="2"><div class="gpu-label">A100-2</div><div class="gpu-percent">96%</div><div class="gpu-bar-lg"><div class="fill" style="width:96%;background:var(--accent)"></div></div></div>
            <div class="gpu-card" data-gpu="3"><div class="gpu-label">A100-3</div><div class="gpu-percent">23%</div><div class="gpu-bar-lg"><div class="fill" style="width:23%;background:var(--accent2)"></div></div></div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </main>
</div>
<footer class="footer">
  <span>© 2026 styde.se / Forge v2.4.1</span>
  <div class="footer-links">
    <a href="#">Documentation</a>
    <a href="#">Status</a>
    <a href="#">API</a>
    <a href="#">GitHub</a>
  </div>
</footer>
<script>
(function(){
'use strict';
const doc=document;
// ---------- CENTRALIZED INTERVAL MANAGER ----------
const intervalManager={
  _registry:{},
  _active:{},
  register(id,fn,ms){
    this._registry[id]={fn,ms};
  },
  start(id){
    if(this._active[id])return;
    const e=this._registry[id];
    if(!e)return;
    this._active[id]=setInterval(e.fn,e.ms);
  },
  stop(id){
    if(!this._active[id])return;
    clearInterval(this._active[id]);
    delete this._active[id];
  },
  startAll(){Object.keys(this._registry).forEach(k=>this.start(k));},
  stopAll(){Object.keys(this._active).forEach(k=>this.stop(k));},
  restart(id){this.stop(id);this.start(id);}
};
// ---------- GPU STAGGERED UPDATER ----------
function gpuUpdate(){
  const cards=doc.querySelectorAll('.gpu-card');
  cards.forEach(c=>{
    const pctEl=c.querySelector('.gpu-percent');
    const fillEl=c.querySelector('.gpu-bar-lg .fill');
    if(!pctEl||!fillEl)return;
    const cur=parseFloat(pctEl.textContent);
    const delta=(Math.random()-0.45)*12;
    const nxt=Math.max(2,Math.min(99,Math.round(cur+delta)));
    pctEl.textContent=nxt+'%';
    const hue=nxt>80?170:nxt>50?36:0;
    fillEl.style.width=nxt+'%';
    fillEl.style.background=nxt>80?'var(--accent)':nxt>50?'var(--accent2)':'var(--err)';
  });
}
intervalManager.register('gpu',gpuUpdate,2200);
// ---------- AGENT GPU BARS STAGGER ----------
function agentGpuUpdate(){
  doc.querySelectorAll('.agent-row .gpu-bar .fill').forEach(el=>{
    const cur=parseFloat(el.style.width)||0;
    const delta=(Math.random()-0.5)*18;
    const nxt=Math.max(0,Math.min(100,Math.round(cur+delta)));
    el.style.width=nxt+'%';
  });
}
intervalManager.register('agentGpu',agentGpuUpdate,3000);
// ---------- COLLAPSIBLE TOGGLE ----------
function setupCollapsible(){
  doc.querySelectorAll('.collapsible-header').forEach(hdr=>{
    const targetId=hdr.getAttribute('data-target');
    const body=doc.getElementById(targetId);
    if(!body)return;
    hdr.addEventListener('click',function(e){
      const isCollapsed=body.classList.contains('collapsed');
      body.classList.toggle('collapsed');
      hdr.classList.toggle('collapsed');
      // pause/resume GPU timers when panel collapsed
      const gpuGrid=doc.getElementById('gpuGrid');
      const agentList=doc.getElementById('agentList');
      if(body.id==='gpuBody'||body.id==='agentBody'){
        if(isCollapsed){
          intervalManager.start('gpu');
          intervalManager.start('agentGpu');
        }else{
          // check if any parent is still visible before stopping
          const gpuBody=doc.getElementById('gpuBody');
          const agentBody=doc.getElementById('agentBody');
          if(gpuBody&&gpuBody.classList.contains('collapsed'))intervalManager.stop('gpu');
          if(agentBody&&agentBody.classList.contains('collapsed'))intervalManager.stop('agentGpu');
        }
      }
    });
  });
}
// ---------- SIDEBAR NAV ----------
function setupSidebar(){
  doc.querySelectorAll('.sidebar-item').forEach(item=>{
    item.addEventListener('click',function(){
      doc.querySelectorAll('.sidebar-item').forEach(i=>i.classList.remove('active'));
      this.classList.add('active');
      if(window.innerWidth<=820){
        doc.getElementById('sidebar').classList.remove('open');
        doc.getElementById('navOverlay').classList.remove('show');
      }
    });
  });
}
// ---------- HAMBURGER ----------
function setupHamburger(){
  const btn=doc.getElementById('hamburgerBtn');
  const nav=doc.getElementById('sidebar');
  const ov=doc.getElementById('navOverlay');
  if(!btn||!nav||!ov)return;
  btn.addEventListener('click',function(){
    nav.classList.toggle('open');
    ov.classList.toggle('show');
  });
  ov.addEventListener('click',function(){
    nav.classList.remove('open');
    ov.classList.remove('show');
  });
}
// ---------- VISIBILITY / INTERSECTION HANDLING ----------
function setupVisibility(){
  const gpuBody=doc.getElementById('gpuBody');
  const agentBody=doc.getElementById('agentBody');
  const feedBody=doc.getElementById('feedBody');
  function handleVis(){
    if(doc.hidden){
      intervalManager.stop('gpu');
      intervalManager.stop('agentGpu');
    }else{
      const gpuC=gpuBody&&!gpuBody.classList.contains('collapsed');
      const agC=agentBody&&!agentBody.classList.contains('collapsed');
      if(gpuC)intervalManager.start('gpu');
      if(agC)intervalManager.start('agentGpu');
    }
  }
  doc.addEventListener('visibilitychange',handleVis);
  // IntersectionObserver for offscreen panels
  const panels=[gpuBody,agentBody,feedBody].filter(Boolean);
  if('IntersectionObserver' in window){
    const obs=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        const id=entry.target.id;
        if(!entry.isIntersecting){
          if(id==='gpuBody')intervalManager.stop('gpu');
          if(id==='agentBody')intervalManager.stop('agentGpu');
        }else{
          const collapsed=entry.target.classList.contains('collapsed');
          if(id==='gpuBody'&&!collapsed)intervalManager.start('gpu');
          if(id==='agentBody'&&!collapsed)intervalManager.start('agentGpu');
        }
      });
    },{threshold:0});
    panels.forEach(p=>obs.observe(p));
  }
}
// ---------- CLEANUP ----------
function cleanup(){
  intervalManager.stopAll();
}
// ---------- INIT ----------
function init(){
  setupCollapsible();
  setupSidebar();
  setupHamburger();
  setupVisibility();
  // start GPU timers (panels start expanded)
  intervalManager.start('gpu');
  intervalManager.start('agentGpu');
  // attach cleanup on page unload
  window.addEventListener('beforeunload',cleanup);
  // register cleanup on collapsible remove via mutation observer
  const targetNodes=[doc.getElementById('gpuBody'),doc.getElementById('agentBody')].filter(Boolean);
  targetNodes.forEach(n=>{
    const mo=new MutationObserver(()=>{
      if(!doc.contains(n)){
        if(n.id==='gpuBody')intervalManager.stop('gpu');
        if(n.id==='agentBody')intervalManager.stop('agentGpu');
        mo.disconnect();
      }
    });
    mo.observe(doc.body,{childList:true,subtree:true});
  });
  // show dash content, hide loading state
  const ld=doc.getElementById('dashLoading');
  if(ld)ld.style.display='none';
}
if(doc.readyState==='loading'){
  doc.addEventListener('DOMContentLoaded',init);
}else{
  init();
}
})();
</script>
</body>
</html>
```