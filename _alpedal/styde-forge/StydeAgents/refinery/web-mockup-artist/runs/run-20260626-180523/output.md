<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge · Control Center</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0b0d11;--surface:#13161c;--card:#191e27;--border:#252b38;--text:#cdd2de;--text-dim:#6d768a;--accent:#58b4ff;--accent2:#a78bfa;--accent3:#f97316;--green:#3ccf7a;--red:#ef4444;--yellow:#eab308;--radius:10px;--shadow:0 2px 12px rgba(0,0,0,0.4)}
html,body{height:100%;font-family:'Inter','Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:1.5}
body{overflow-x:hidden;display:flex;flex-direction:column}
/* === APP SHELL === */
.app-shell{display:flex;flex:1;min-height:100vh;position:relative}
.sidebar{width:250px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;transition:transform .3s ease,width .3s ease;z-index:100;overflow-y:auto}
.sidebar-brand{padding:18px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px}
.sidebar-brand .logo{width:32px;height:32px;background:linear-gradient(135deg,var(--accent),var(--accent2));border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#fff}
.sidebar-brand h1{font-size:16px;font-weight:700;color:#fff;letter-spacing:-0.3px}
.sidebar-brand h1 span{color:var(--accent)}
.sidebar-nav{flex:1;padding:12px 0}
.nav-section{margin-bottom:4px}
.nav-section-title{padding:8px 20px 4px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--text-dim)}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 20px;color:var(--text-dim);text-decoration:none;font-size:13px;cursor:pointer;transition:all .15s;border-left:3px solid transparent;position:relative}
.nav-item:hover,.nav-item.active{color:var(--text);background:rgba(88,180,255,0.06)}
.nav-item.active{border-left-color:var(--accent);color:var(--accent)}
.nav-item .icon{width:18px;text-align:center;font-size:15px;flex-shrink:0}
.nav-item .badge{margin-left:auto;background:var(--card);padding:1px 8px;border-radius:10px;font-size:11px;color:var(--text-dim)}
.nav-item .chevron{margin-left:auto;font-size:10px;transition:transform .2s;color:var(--text-dim)}
.nav-item .chevron.open{transform:rotate(90deg)}
.sub-nav{padding-left:48px;max-height:0;overflow:hidden;transition:max-height .25s ease}
.sub-nav.open{max-height:300px}
.sub-nav .nav-item{padding:6px 0;font-size:12px;border-left:none}
.sub-nav .nav-item.active{color:var(--accent2)}
.sidebar-footer{padding:12px 20px;border-top:1px solid var(--border);font-size:11px;color:var(--text-dim)}
/* === MAIN === */
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{display:flex;align-items:center;padding:12px 24px;background:var(--surface);border-bottom:1px solid var(--border);gap:16px;flex-wrap:wrap}
.hamburger{display:none;background:none;border:none;color:var(--text);font-size:22px;cursor:pointer;padding:4px;line-height:1}
.breadcrumbs{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-dim);flex:1}
.breadcrumbs a{color:var(--text-dim);text-decoration:none}
.breadcrumbs a:hover{color:var(--accent)}
.breadcrumbs span{color:var(--text)}
.topbar-actions{display:flex;align-items:center;gap:12px}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.status-dot.green{background:var(--green);box-shadow:0 0 6px var(--green)}
.status-dot.yellow{background:var(--yellow);box-shadow:0 0 6px var(--yellow)}
.status-dot.red{background:var(--red);box-shadow:0 0 6px var(--red)}
.topbar-status{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-dim)}
.avatar{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,var(--accent2),var(--accent3));display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;cursor:pointer}
/* === CONTENT === */
.content{padding:24px;flex:1;overflow-y:auto;max-width:1440px}
.page-title{font-size:22px;font-weight:700;color:#fff;margin-bottom:4px;letter-spacing:-0.4px}
.page-sub{font-size:13px;color:var(--text-dim);margin-bottom:24px}
/* Metrics Grid */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:24px}
.metric-card{background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:18px 20px;position:relative;overflow:hidden;transition:border-color .2s}
.metric-card:hover{border-color:var(--accent)}
.metric-card .label{font-size:12px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px}
.metric-card .value{font-size:28px;font-weight:700;color:#fff;letter-spacing:-0.5px}
.metric-card .change{font-size:12px;margin-top:4px;display:flex;align-items:center;gap:4px}
.metric-card .change.up{color:var(--green)}
.metric-card .change.down{color:var(--red)}
.metric-card .mini-chart{height:40px;margin-top:10px}
.metric-card .icon-bg{position:absolute;right:16px;top:16px;font-size:32px;opacity:0.06;color:#fff}
/* === GRID LAYOUT === */
.dashboard-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
@media(max-width:1100px){.dashboard-grid{grid-template-columns:1fr}}
.card{background:var(--card);border-radius:var(--radius);border:1px solid var(--border);overflow:hidden}
.card-header{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;border-bottom:1px solid var(--border);cursor:pointer;user-select:none}
.card-header:hover{background:rgba(88,180,255,0.03)}
.card-header h3{font-size:14px;font-weight:600;color:#fff}
.card-header .collapse-btn{background:none;border:none;color:var(--text-dim);cursor:pointer;font-size:12px;padding:2px 6px;border-radius:4px;transition:all .15s}
.card-header .collapse-btn:hover{background:var(--border);color:var(--text)}
.card-body{padding:16px 20px;transition:max-height .3s ease;overflow:hidden}
.card-body.collapsed{max-height:0;padding:0 20px}
/* Agent Table */
.agent-table{width:100%;border-collapse:collapse;font-size:13px}
.agent-table th{text-align:left;padding:8px 10px;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:var(--text-dim);border-bottom:1px solid var(--border)}
.agent-table td{padding:10px;border-bottom:1px solid rgba(37,43,56,0.5);vertical-align:middle}
.agent-table tr:last-child td{border-bottom:none}
.agent-table tr:hover td{background:rgba(88,180,255,0.03)}
.agent-name{display:flex;align-items:center;gap:8px}
.agent-name .agent-icon{width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff}
.status-badge{padding:2px 10px;border-radius:10px;font-size:11px;font-weight:500}
.status-badge.online{background:rgba(60,207,122,0.15);color:var(--green)}
.status-badge.busy{background:rgba(234,179,8,0.15);color:var(--yellow)}
.status-badge.offline{background:rgba(239,68,68,0.15);color:var(--red)}
.progress-bar{height:4px;background:var(--border);border-radius:4px;overflow:hidden;width:100px}
.progress-bar .fill{height:100%;background:var(--accent);border-radius:4px;transition:width .5s}
/* Activity Feed */
.activity-feed{display:flex;flex-direction:column;gap:10px}
.activity-item{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid rgba(37,43,56,0.4)}
.activity-item:last-child{border-bottom:none}
.activity-dot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0}
.activity-dot.info{background:var(--accent)}
.activity-dot.success{background:var(--green)}
.activity-dot.warn{background:var(--yellow)}
.activity-dot.error{background:var(--red)}
.activity-text{font-size:13px;color:var(--text);flex:1}
.activity-text strong{color:#fff}
.activity-time{font-size:11px;color:var(--text-dim);white-space:nowrap}
/* GPU Monitor */
.gpu-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:600px){.gpu-cards{grid-template-columns:1fr}}
.gpu-item{padding:12px;background:rgba(11,13,17,0.5);border-radius:8px;border:1px solid var(--border)}
.gpu-item .gpu-header{display:flex;justify-content:space-between;margin-bottom:6px}
.gpu-item .gpu-name{font-size:12px;font-weight:600;color:var(--text)}
.gpu-item .gpu-temp{font-size:12px;color:var(--text-dim)}
.gpu-bar{height:6px;background:var(--border);border-radius:4px;overflow:hidden;margin:4px 0}
.gpu-bar .fill{height:100%;border-radius:4px;transition:width .5s}
.gpu-bar .fill.warm{background:var(--yellow)}
.gpu-bar .fill.hot{background:var(--red)}
.gpu-bar .fill.cool{background:var(--green)}
.gpu-stats{display:flex;justify-content:space-between;font-size:11px;color:var(--text-dim)}
/* Chart Containers */
.chart-container{height:200px;position:relative}
/* Footer */
footer{padding:16px 24px;border-top:1px solid var(--border);background:var(--surface);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;font-size:12px;color:var(--text-dim)}
footer nav{display:flex;gap:16px}
footer nav a{color:var(--text-dim);text-decoration:none}
footer nav a:hover{color:var(--accent)}
/* === OVERLAY === */
.sidebar-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:99}
/* === RESPONSIVE === */
@media(max-width:768px){
  .sidebar{position:fixed;top:0;left:0;bottom:0;transform:translateX(-100%);width:280px}
  .sidebar.open{transform:translateX(0)}
  .sidebar-overlay.open{display:block}
  .hamburger{display:block}
  .topbar{padding:10px 16px}
  .content{padding:16px}
  .metrics{grid-template-columns:1fr 1fr}
  .dashboard-grid{grid-template-columns:1fr}
  footer{flex-direction:column;text-align:center}
}
@media(max-width:480px){
  .metrics{grid-template-columns:1fr}
  .topbar-actions .topbar-status span{display:none}
  .breadcrumbs{font-size:11px}
}
</style>
</head>
<body>
<div class="app-shell">
<!-- SIDEBAR -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-brand">
    <div class="logo">SF</div>
    <h1>Styde<span>Forge</span></h1>
  </div>
  <nav class="sidebar-nav">
    <div class="nav-section">
      <div class="nav-section-title">Overview</div>
      <a class="nav-item active" data-target="dashboard" href="#">
        <span class="icon">&#9632;</span> Dashboard
        <span class="badge">12</span>
      </a>
      <a class="nav-item" data-target="agents" href="#">
        <span class="icon">&#9679;</span> Agents
        <span class="badge">8</span>
      </a>
      <a class="nav-item" data-target="pipelines" href="#">
        <span class="icon">&#8644;</span> Pipelines
      </a>
    </div>
    <div class="nav-section">
      <div class="nav-section-title">Monitor</div>
      <a class="nav-item collapsible-trigger" data-target="gpu-sub" href="#">
        <span class="icon">&#9881;</span> GPU Cluster
        <span class="chevron" id="chev-gpu-sub">&#9654;</span>
      </a>
      <div class="sub-nav" id="gpu-sub">
        <a class="nav-item" href="#">A100 Nodes</a>
        <a class="nav-item active" href="#">H100 Pool</a>
        <a class="nav-item" href="#">RTX Pool</a>
      </div>
      <a class="nav-item collapsible-trigger" data-target="logs-sub" href="#">
        <span class="icon">&#9776;</span> Logs
        <span class="chevron" id="chev-logs-sub">&#9654;</span>
      </a>
      <div class="sub-nav" id="logs-sub">
        <a class="nav-item" href="#">Build Logs</a>
        <a class="nav-item" href="#">Agent Output</a>
        <a class="nav-item" href="#">System Events</a>
      </div>
    </div>
    <div class="nav-section">
      <div class="nav-section-title">Config</div>
      <a class="nav-item" href="#">
        <span class="icon">&#9878;</span> Blueprints
      </a>
      <a class="nav-item" href="#">
        <span class="icon">&#9881;</span> Settings
      </a>
    </div>
  </nav>
  <div class="sidebar-footer">
    Forge v3.2.1 &middot; Hermes runtime
  </div>
</aside>
<div class="sidebar-overlay" id="sidebar-overlay"></div>
<!-- MAIN -->
<div class="main">
  <header class="topbar">
    <button class="hamburger" id="hamburger-btn" aria-label="Toggle sidebar">&#9776;</button>
    <div class="breadcrumbs">
      <a href="#">Styde</a> <span>&rsaquo;</span>
      <a href="#">Forge</a> <span>&rsaquo;</span>
      <span>Control Center</span>
    </div>
    <div class="topbar-actions">
      <div class="topbar-status">
        <span class="status-dot green"></span>
        <span>All systems nominal</span>
      </div>
      <div class="avatar">PA</div>
    </div>
  </header>
  <div class="content">
    <h2 class="page-title">Control Center</h2>
    <p class="page-sub">Overview of forge operations, agent health, and cluster resources</p>
    <!-- METRICS -->
    <div class="metrics" id="metrics-grid">
      <div class="metric-card" data-metric="agents">
        <div class="icon-bg">&#9679;</div>
        <div class="label">Active Agents</div>
        <div class="value" id="metric-agents">18</div>
        <div class="change up">+2 this hour</div>
        <div class="mini-chart"><canvas id="spark-agents" height="40"></canvas></div>
      </div>
      <div class="metric-card" data-metric="pipelines">
        <div class="icon-bg">&#8644;</div>
        <div class="label">Pipeline Runs</div>
        <div class="value" id="metric-pipelines">247</div>
        <div class="change up">+12% vs yesterday</div>
        <div class="mini-chart"><canvas id="spark-pipelines" height="40"></canvas></div>
      </div>
      <div class="metric-card" data-metric="gpu">
        <div class="icon-bg">&#9881;</div>
        <div class="label">GPU Utilization</div>
        <div class="value" id="metric-gpu">73%</div>
        <div class="change up">+5% from baseline</div>
        <div class="mini-chart"><canvas id="spark-gpu" height="40"></canvas></div>
      </div>
      <div class="metric-card" data-metric="queue">
        <div class="icon-bg">&#9776;</div>
        <div class="label">Queue Depth</div>
        <div class="value" id="metric-queue">6</div>
        <div class="change down">-3 in last 5 min</div>
        <div class="mini-chart"><canvas id="spark-queue" height="40"></canvas></div>
      </div>
    </div>
    <!-- DASHBOARD GRID -->
    <div class="dashboard-grid">
      <!-- AGENT STATUS CARD -->
      <div class="card">
        <div class="card-header" data-collapse="agent-table-body">
          <h3>Agent Status</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="agent-table-body">
          <table class="agent-table">
            <thead><tr><th>Agent</th><th>Status</th><th>Task</th><th>Progress</th><th>Memory</th></tr></thead>
            <tbody id="agent-table-body-data"></tbody>
          </table>
        </div>
      </div>
      <!-- CHART CARD - PIPELINE THROUGHPUT -->
      <div class="card">
        <div class="card-header" data-collapse="chart-throughput-body">
          <h3>Pipeline Throughput (24h)</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="chart-throughput-body">
          <div class="chart-container">
            <canvas id="chart-throughput"></canvas>
          </div>
        </div>
      </div>
      <!-- ACTIVITY FEED CARD -->
      <div class="card">
        <div class="card-header" data-collapse="activity-body">
          <h3>Recent Activity</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="activity-body">
          <div class="activity-feed" id="activity-feed"></div>
        </div>
      </div>
      <!-- GPU MONITOR CARD -->
      <div class="card">
        <div class="card-header" data-collapse="gpu-body">
          <h3>GPU Cluster</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="gpu-body">
          <div class="gpu-cards" id="gpu-cards"></div>
        </div>
      </div>
      <!-- CHART CARD - AGENT LOAD DISTRIBUTION -->
      <div class="card">
        <div class="card-header" data-collapse="chart-dist-body">
          <h3>Agent Load Distribution</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="chart-dist-body">
          <div class="chart-container">
            <canvas id="chart-distribution"></canvas>
          </div>
        </div>
      </div>
      <!-- CHART CARD - GPU MEMORY -->
      <div class="card">
        <div class="card-header" data-collapse="chart-gpu-mem-body">
          <h3>GPU Memory Usage by Node</h3>
          <button class="collapse-btn" aria-label="Collapse">&#8722;</button>
        </div>
        <div class="card-body" id="chart-gpu-mem-body">
          <div class="chart-container">
            <canvas id="chart-gpu-mem"></canvas>
          </div>
        </div>
      </div>
    </div><!-- /dashboard-grid -->
  </div><!-- /content -->
  <footer>
    <span>&copy; 2026 Styde AB &middot; Forge Control Center</span>
    <nav>
      <a href="#">Documentation</a>
      <a href="#">API</a>
      <a href="#">Status</a>
      <a href="#">Support</a>
      <a href="#">Privacy</a>
    </nav>
  </footer>
</div><!-- /main -->
</div><!-- /app-shell -->
<script>
// ===== DATA STORE =====
const DB = {
  agents: [
    {name:'Hermes Prime',   icon:'HP', color:'#58b4ff', status:'online',  task:'Orchestrating batch #412',  progress:78, memory:'2.8GB'},
    {name:'Caveman',        icon:'CM', color:'#a78bfa', status:'busy',    task:'Code review pass 3',        progress:45, memory:'4.2GB'},
    {name:'Prompt Engineer',icon:'PE', color:'#f97316', status:'busy',    task:'Blueprint refinement',      progress:62, memory:'1.1GB'},
    {name:'Data Weaver',    icon:'DW', color:'#3ccf7a', status:'online',  task:'JSON pipeline hydration',   progress:91, memory:'6.4GB'},
    {name:'Vision Scout',   icon:'VS', color:'#ef4444', status:'offline', task:'---',                        progress:0,  memory:'0GB'},
    {name:'Forge Evaluator',icon:'FE', color:'#eab308', status:'online',  task:'Batch 47 validation',       progress:33, memory:'3.7GB'},
    {name:'Blueprint Forger',icon:'BF',color:'#06b6d4',status:'busy',     task:'Generation loop v3',         progress:55, memory:'5.0GB'},
    {name:'Log Weaver',     icon:'LW', color:'#ec4899', status:'online',  task:'Audit trail compaction',     progress:100,memory:'0.9GB'}
  ],
  activities: [
    {type:'info',    text:'<strong>Hermes Prime</strong> completed batch #412 in 47s',     time:'1m ago'},
    {type:'success', text:'<strong>Data Weaver</strong> hydrated 14 blueprints from JSON', time:'3m ago'},
    {type:'info',    text:'<strong>Prompt Engineer</strong> submitted PlanPrompt-v8.md',   time:'5m ago'},
    {type:'warn',    text:'<strong>Vision Scout</strong> offline — heartbeat missed x3',   time:'8m ago'},
    {type:'success', text:'<strong>Forge Evaluator</strong> passed 46/46 BPs in gate',     time:'12m ago'},
    {type:'info',    text:'<strong>Blueprint Forger</strong> locked v3 generation loop',   time:'18m ago'},
    {type:'error',   text:'<strong>Caveman</strong> flagged 12 lint violations in PR #89', time:'22m ago'},
    {type:'info',    text:'<strong>Log Weaver</strong> compacted 2.3GB of audit trails',   time:'28m ago'}
  ],
  gpus: [
    {name:'H100-01', temp:62, util:87, mem:71, barClass:'warm'},
    {name:'H100-02', temp:55, util:73, mem:64, barClass:'cool'},
    {name:'H100-03', temp:71, util:94, mem:88, barClass:'hot'},
    {name:'A100-01', temp:48, util:41, mem:53, barClass:'cool'},
    {name:'A100-02', temp:59, util:68, mem:72, barClass:'warm'},
    {name:'RTX-01',  temp:44, util:22, mem:31, barClass:'cool'}
  ],
  throughputData: [12,19,15,22,28,25,18,21,24,30,33,27,22,26,31,35,29,24,20,26,32,38,34,30],
  distributionData: [22,18,14,11,9,8,7,6,5],
  gpuMemData: [71,64,88,53,72,31],
  sparkAgents: [12,14,13,16,15,18,17,19,18,20,18,17],
  sparkPipelines: [180,195,210,205,220,235,240,230,247,240,238,245],
  sparkGpu: [62,65,68,64,70,73,71,68,72,75,73,70],
  sparkQueue: [12,11,10,9,8,7,9,8,7,6,7,6]
};
// ===== RENDER HELPERS =====
function renderAgents() {
  const tbody = document.getElementById('agent-table-body-data');
  tbody.innerHTML = DB.agents.map(a => `
    <tr>
      <td><div class="agent-name"><div class="agent-icon" style="background:${a.color}">${a.icon}</div>${a.name}</div></td>
      <td><span class="status-badge ${a.status}">${a.status}</span></td>
      <td style="font-size:12px;color:var(--text-dim)">${a.task}</td>
      <td><div class="progress-bar"><div class="fill" style="width:${a.progress}%"></div></div></td>
      <td style="font-size:12px;color:var(--text-dim)">${a.memory}</td>
    </tr>
  `).join('');
}
function renderActivities() {
  const feed = document.getElementById('activity-feed');
  feed.innerHTML = DB.activities.map(a => `
    <div class="activity-item">
      <div class="activity-dot ${a.type}"></div>
      <div class="activity-text">${a.text}</div>
      <div class="activity-time">${a.time}</div>
    </div>
  `).join('');
}
function renderGpus() {
  const container = document.getElementById('gpu-cards');
  container.innerHTML = DB.gpus.map(g => `
    <div class="gpu-item">
      <div class="gpu-header">
        <span class="gpu-name">${g.name}</span>
        <span class="gpu-temp">${g.temp}&deg;C</span>
      </div>
      <div style="font-size:11px;color:var(--text-dim);display:flex;justify-content:space-between;margin-bottom:2px">
        <span>Util</span><span>${g.util}%</span>
      </div>
      <div class="gpu-bar"><div class="fill ${g.barClass}" style="width:${g.util}%"></div></div>
      <div class="gpu-stats">
        <span>Mem: ${g.mem}%</span>
        <span>${g.util >= 85 ? 'Heavy load' : g.util >= 60 ? 'Moderate' : 'Idle'}</span>
      </div>
    </div>
  `).join('');
}
// ===== CHARTS =====
function initCharts() {
  // Pipeline throughput (line)
  new Chart(document.getElementById('chart-throughput'), {
    type:'line',
    data:{
      labels:Array.from({length:24},(_,i)=>String(i).padStart(2,'0')+':00'),
      datasets:[{
        label:'Pipeline Runs',
        data:DB.throughputData,
        borderColor:'#58b4ff',
        backgroundColor:'rgba(88,180,255,0.08)',
        fill:true,
        tension:0.35,
        pointRadius:3,
        pointBackgroundColor:'#58b4ff',
        pointBorderColor:'#0b0d11',
        pointBorderWidth:1.5
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:true,labels:{color:'#6d768a',boxWidth:12,font:{size:11}}}},
      scales:{
        x:{ticks:{color:'#6d768a',font:{size:10}},grid:{color:'rgba(37,43,56,0.3)'}},
        y:{ticks:{color:'#6d768a',font:{size:10}},grid:{color:'rgba(37,43,56,0.3)'},beginAtZero:true}
      }
    }
  });
  // Agent load distribution (doughnut)
  new Chart(document.getElementById('chart-distribution'), {
    type:'doughnut',
    data:{
      labels:['Hermes Prime','Caveman','Prompt Engineer','Data Weaver','Forge Evaluator','Blueprint Forger','Log Weaver','Idle','Offline'],
      datasets:[{
        data:DB.distributionData,
        backgroundColor:['#58b4ff','#a78bfa','#f97316','#3ccf7a','#eab308','#06b6d4','#ec4899','#252b38','#ef4444'],
        borderWidth:0
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{
        legend:{position:'bottom',labels:{color:'#6d768a',boxWidth:10,font:{size:10},padding:10}},
        tooltip:{callbacks:{label:ctx=>ctx.label+': '+ctx.parsed+'%'}}
      },
      cutout:'55%'
    }
  });
  // GPU Memory Usage (bar)
  new Chart(document.getElementById('chart-gpu-mem'), {
    type:'bar',
    data:{
      labels:['H100-01','H100-02','H100-03','A100-01','A100-02','RTX-01'],
      datasets:[{
        label:'Memory %',
        data:DB.gpuMemData,
        backgroundColor:['rgba(88,180,255,0.6)','rgba(60,207,122,0.6)','rgba(239,68,68,0.6)','rgba(60,207,122,0.6)','rgba(234,179,8,0.6)','rgba(88,180,255,0.6)'],
        borderColor:['#58b4ff','#3ccf7a','#ef4444','#3ccf7a','#eab308','#58b4ff'],
        borderWidth:1,
        borderRadius:4
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:true,labels:{color:'#6d768a',boxWidth:12,font:{size:11}}}},
      scales:{
        x:{ticks:{color:'#6d768a',font:{size:10}},grid:{display:false}},
        y:{ticks:{color:'#6d768a',font:{size:10}},grid:{color:'rgba(37,43,56,0.3)'},beginAtZero:true,max:100}
      }
    }
  });
  // Sparklines (mini line charts for metric cards)
  const sparkOpts = (color) => ({
    type:'line',
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{enabled:false}},
      scales:{x:{display:false},y:{display:false,beginAtZero:true}},
      elements:{point:{radius:0}},
      animation:false
    }
  });
  new Chart(document.getElementById('spark-agents'), {
    ...sparkOpts('#58b4ff'),
    data:{labels:Array(12).fill(''), datasets:[{data:DB.sparkAgents,borderColor:'#58b4ff',borderWidth:1.5,fill:false,tension:0.3}]}
  });
  new Chart(document.getElementById('spark-pipelines'), {
    ...sparkOpts('#3ccf7a'),
    data:{labels:Array(12).fill(''), datasets:[{data:DB.sparkPipelines,borderColor:'#3ccf7a',borderWidth:1.5,fill:false,tension:0.3}]}
  });
  new Chart(document.getElementById('spark-gpu'), {
    ...sparkOpts('#a78bfa'),
    data:{labels:Array(12).fill(''), datasets:[{data:DB.sparkGpu,borderColor:'#a78bfa',borderWidth:1.5,fill:false,tension:0.3}]}
  });
  new Chart(document.getElementById('spark-queue'), {
    ...sparkOpts('#f97316'),
    data:{labels:Array(12).fill(''), datasets:[{data:DB.sparkQueue,borderColor:'#f97316',borderWidth:1.5,fill:false,tension:0.3}]}
  });
}
// ===== INTERACTIVITY =====
// Sidebar toggle (hamburger)
document.getElementById('hamburger-btn').addEventListener('click',()=>{
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebar-overlay').classList.toggle('open');
});
document.getElementById('sidebar-overlay').addEventListener('click',()=>{
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebar-overlay').classList.remove('open');
});
// Collapsible sub-nav sections
document.querySelectorAll('.collapsible-trigger').forEach(trigger=>{
  trigger.addEventListener('click',function(e){
    e.preventDefault();
    const targetId = this.dataset.target;
    const sub = document.getElementById(targetId);
    const chev = document.getElementById('chev-'+targetId);
    if(sub){sub.classList.toggle('open')}
    if(chev){chev.classList.toggle('open')}
  });
});
// Card collapse/expand
document.querySelectorAll('.card-header').forEach(header=>{
  header.addEventListener('click',function(e){
    if(e.target.closest('.collapse-btn') || e.target.closest('button')){return}
    const bodyId = this.dataset.collapse;
    const body = document.getElementById(bodyId);
    const btn = this.querySelector('.collapse-btn');
    if(body && btn){
      body.classList.toggle('collapsed');
      btn.textContent = body.classList.contains('collapsed') ? '+' : '\u2212';
    }
  });
  const btn = header.querySelector('.collapse-btn');
  if(btn){
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      const bodyId = header.dataset.collapse;
      const body = document.getElementById(bodyId);
      if(body){
        body.classList.toggle('collapsed');
        this.textContent = body.classList.contains('collapsed') ? '+' : '\u2212';
      }
    });
  }
});
// Nav item active state
document.querySelectorAll('.nav-item').forEach(item=>{
  item.addEventListener('click',function(e){
    if(this.classList.contains('collapsible-trigger')){return}
    document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
    this.classList.add('active');
  });
});
// ===== RESIZE HANDLER (responsive validation test support) =====
window.addEventListener('resize',()=>{
  const sidebar = document.getElementById('sidebar');
  if(window.innerWidth > 768 && sidebar.classList.contains('open')){
    sidebar.classList.remove('open');
    document.getElementById('sidebar-overlay').classList.remove('open');
  }
});
// ===== INIT =====
document.addEventListener('DOMContentLoaded',()=>{
  renderAgents();
  renderActivities();
  renderGpus();
  initCharts();
});
</script>
</body>
</html>