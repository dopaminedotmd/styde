```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Command Center</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0c0e14;
  --bg2:#12161e;
  --bg3:#181e2a;
  --surface:#1f2636;
  --surface2:#29334a;
  --border:#2e3a54;
  --text:#d6e0f0;
  --text2:#8899bb;
  --text3:#5a6f91;
  --accent:#6fc3df;
  --accent2:#4fa8c9;
  --green:#4cd9a8;
  --orange:#f0b34b;
  --red:#f0636b;
  --purple:#b47dff;
  --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --radius:10px;
  --shadow:0 8px 32px rgba(0,0,0,.45);
}
html{font-size:15px}
body{
  font-family:var(--font);
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  display:flex;
  flex-direction:column;
  line-height:1.5;
}
a{color:var(--accent);text-decoration:none}
a:hover{color:#fff}
/* HEADER */
.header{
  background:var(--bg2);
  border-bottom:1px solid var(--border);
  padding:0 24px;
  display:flex;
  align-items:center;
  height:56px;
  position:sticky;
  top:0;
  z-index:100;
}
.header-left{
  display:flex;
  align-items:center;
  gap:14px;
}
.logo{
  font-weight:700;
  font-size:1.15rem;
  letter-spacing:-.02em;
  background:linear-gradient(135deg,var(--accent),var(--purple));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  white-space:nowrap;
}
.logo span{-webkit-text-fill-color:var(--text2);font-weight:400}
.header-center{flex:1;display:flex;justify-content:center;gap:6px}
.badge{
  font-size:.68rem;
  padding:3px 10px;
  border-radius:20px;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--text2);
  white-space:nowrap;
}
.badge.active{background:rgba(79,168,201,.12);border-color:var(--accent2);color:var(--accent)}
.header-right{display:flex;align-items:center;gap:14px}
.avatar{
  width:30px;height:30px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent),var(--purple));
  display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:600;color:#fff;cursor:pointer;
}
.hamburger{display:none;flex-direction:column;gap:4px;cursor:pointer;padding:4px}
.hamburger span{display:block;width:20px;height:2px;background:var(--text2);border-radius:2px}
/* NAV */
.nav{
  background:var(--bg2);
  border-bottom:1px solid var(--border);
  padding:0 24px;
  display:flex;
  align-items:center;
  gap:2px;
  height:42px;
  overflow-x:auto;
}
.nav a{
  padding:0 16px;
  height:42px;
  display:flex;
  align-items:center;
  font-size:.82rem;
  color:var(--text3);
  border-bottom:2px solid transparent;
  transition:.15s;
  white-space:nowrap;
}
.nav a:hover,.nav a.active{color:var(--text);border-bottom-color:var(--accent)}
.nav a.active{color:var(--accent)}
/* BREADCRUMB */
.breadcrumb{
  padding:12px 24px;
  font-size:.78rem;
  color:var(--text3);
  background:var(--bg);
  border-bottom:1px solid var(--border);
  display:flex;
  align-items:center;
  gap:6px;
}
.breadcrumb a{color:var(--text3)}
.breadcrumb a:hover{color:var(--accent)}
.breadcrumb .sep{color:var(--border);font-size:.7rem}
/* LAYOUT */
.layout{
  display:flex;
  flex:1;
  padding:20px 24px 24px;
  gap:20px;
}
.main{flex:1;min-width:0}
.sidebar{width:340px;flex-shrink:0;display:flex;flex-direction:column;gap:16px}
/* CARDS */
.card{
  background:var(--bg2);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:18px 20px;
}
.card-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:14px;
}
.card-title{
  font-size:.82rem;
  font-weight:600;
  color:var(--text2);
  text-transform:uppercase;
  letter-spacing:.04em;
}
.card-action{
  font-size:.72rem;
  color:var(--accent);
  cursor:pointer;
  padding:3px 8px;
  border-radius:4px;
  transition:.15s;
}
.card-action:hover{background:var(--surface);color:#fff}
/* METRICS GRID */
.metrics{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px;
  margin-bottom:20px;
}
.metric{
  background:var(--bg2);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:16px 18px;
  transition:.2s;
  cursor:default;
}
.metric:hover{border-color:var(--accent2);transform:translateY(-2px);box-shadow:0 4px 20px rgba(79,168,201,.08)}
.metric .label{font-size:.72rem;color:var(--text3);text-transform:uppercase;letter-spacing:.03em}
.metric .value{font-size:1.7rem;font-weight:700;margin-top:2px;letter-spacing:-.03em}
.metric .sub{font-size:.72rem;color:var(--text3);margin-top:2px}
.metric .value.green{color:var(--green)}
.metric .value.orange{color:var(--orange)}
.metric .value.red{color:var(--red)}
.metric .value.purple{color:var(--purple)}
.metric .value.accent{color:var(--accent)}
/* AGENT TABLE */
.agent-table{width:100%;border-collapse:collapse;font-size:.82rem}
.agent-table th{
  text-align:left;
  padding:8px 10px;
  color:var(--text3);
  font-weight:500;
  font-size:.7rem;
  text-transform:uppercase;
  letter-spacing:.05em;
  border-bottom:1px solid var(--border);
}
.agent-table td{padding:10px;border-bottom:1px solid rgba(46,58,84,.4)}
.agent-table tr:last-child td{border:none}
.agent-table tr:hover td{background:var(--surface)}
.status-dot{
  display:inline-block;
  width:8px;height:8px;border-radius:50%;
  margin-right:6px;
}
.status-dot.green{background:var(--green);box-shadow:0 0 8px rgba(76,217,168,.35)}
.status-dot.orange{background:var(--orange);box-shadow:0 0 8px rgba(240,179,75,.25)}
.status-dot.red{background:var(--red);box-shadow:0 0 8px rgba(240,99,107,.25)}
.status-dot.purple{background:var(--purple);box-shadow:0 0 8px rgba(180,125,255,.25)}
.agent-name{font-weight:500}
.agent-role{font-size:.72rem;color:var(--text3);margin-top:1px}
/* ACTIVITY FEED */
.activity-list{display:flex;flex-direction:column;gap:10px}
.activity-item{
  display:flex;
  gap:12px;
  padding:8px 0;
  border-bottom:1px solid rgba(46,58,84,.2);
  transition:.15s;
  cursor:default;
}
.activity-item:last-child{border:none}
.activity-item:hover{background:var(--surface);margin:0 -12px;padding:8px 12px;border-radius:6px}
.activity-icon{
  width:32px;height:32px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:.75rem;flex-shrink:0;
}
.activity-icon.build{background:rgba(79,168,201,.15);color:var(--accent)}
.activity-icon.deploy{background:rgba(76,217,168,.12);color:var(--green)}
.activity-icon.error{background:rgba(240,99,107,.12);color:var(--red)}
.activity-icon.train{background:rgba(180,125,255,.12);color:var(--purple)}
.activity-content{flex:1;min-width:0}
.activity-text{font-size:.82rem}
.activity-time{font-size:.7rem;color:var(--text3);margin-top:1px}
/* GPU MONITOR */
.gpu-bar{display:flex;flex-direction:column;gap:10px;margin-top:4px}
.gpu-item{display:flex;align-items:center;gap:10px}
.gpu-label{width:36px;font-size:.75rem;color:var(--text3);font-weight:500}
.gpu-track{flex:1;height:22px;background:var(--surface);border-radius:4px;overflow:hidden;position:relative}
.gpu-fill{height:100%;border-radius:4px;transition:width 1s ease;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:.62rem;font-weight:600;color:#fff}
.gpu-fill.a{background:linear-gradient(90deg,#4fa8c9,#6fc3df);width:72%}
.gpu-fill.b{background:linear-gradient(90deg,#b47dff,#c99fff);width:88%}
.gpu-fill.c{background:linear-gradient(90deg,#f0b34b,#f5c46e);width:34%}
.gpu-fill.d{background:linear-gradient(90deg,#4cd9a8,#6ee8c0);width:56%}
.gpu-pct{width:30px;text-align:right;font-size:.72rem;color:var(--text2);font-weight:600}
/* COLLAPSIBLE */
.collapsible{cursor:pointer;user-select:none}
.collapsible .arrow{display:inline-block;margin-right:6px;transition:transform .2s;font-size:.65rem}
.collapsible.open .arrow{transform:rotate(90deg)}
.collapsible-body{overflow:hidden;max-height:0;transition:max-height .35s ease}
.collapsible.open .collapsible-body{max-height:600px}
/* SIDEBAR WIDGETS */
.sidebar .card+.card{margin-top:0}
.status-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px}
.status-item{
  background:var(--surface);
  border-radius:6px;
  padding:10px;
  text-align:center;
  transition:.15s;
}
.status-item:hover{background:var(--surface2);transform:scale(1.03)}
.status-item .num{font-size:1.1rem;font-weight:700}
.status-item .lbl{font-size:.65rem;color:var(--text3);margin-top:1px;text-transform:uppercase;letter-spacing:.02em}
/* FOOTER */
.footer{
  background:var(--bg2);
  border-top:1px solid var(--border);
  padding:16px 24px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  font-size:.72rem;
  color:var(--text3);
  margin-top:auto;
}
.footer-links{display:flex;gap:18px}
.footer-links a{color:var(--text3);font-size:.7rem}
.footer-links a:hover{color:var(--accent)}
/* RESPONSIVE */
@media(max-width:1100px){
  .metrics{grid-template-columns:repeat(2,1fr)}
  .sidebar{width:280px}
}
@media(max-width:820px){
  .layout{flex-direction:column;padding:14px}
  .sidebar{width:100%}
  .hamburger{display:flex}
  .nav{display:none}
  .nav.mobile-open{display:flex;flex-wrap:wrap;height:auto;padding:8px 14px}
  .nav.mobile-open a{height:36px}
  .header-center{display:none}
  .breadcrumb{padding:10px 14px}
}
@media(max-width:520px){
  .metrics{grid-template-columns:1fr}
  .footer{flex-direction:column;gap:8px;text-align:center}
  .header{padding:0 14px}
}
/* ANIMATIONS */
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.metric,.card,.activity-item{animation:fadeIn .4s ease both}
.metric:nth-child(2){animation-delay:.06s}
.metric:nth-child(3){animation-delay:.12s}
.metric:nth-child(4){animation-delay:.18s}
</style>
</head>
<body>
<header class="header" role="banner">
  <div class="header-left">
    <div class="logo">styde<span>.se</span></div>
    <div class="hamburger" onclick="document.querySelector('.nav').classList.toggle('mobile-open')" aria-label="Toggle navigation" role="button" tabindex="0">
      <span></span><span></span><span></span>
    </div>
  </div>
  <div class="header-center">
    <span class="badge active">forge active</span>
    <span class="badge">3 agents online</span>
    <span class="badge">v2.1.4</span>
  </div>
  <div class="header-right">
    <span style="font-size:.78rem;color:var(--text3)">Pontus</span>
    <div class="avatar" aria-label="User avatar">P</div>
  </div>
</header>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <a href="#" class="active">Command Center</a>
  <a href="#">Agents</a>
  <a href="#">Blueprints</a>
  <a href="#">Training</a>
  <a href="#">Deployments</a>
  <a href="#">Monitoring</a>
  <a href="#">Settings</a>
</nav>
<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">
  <a href="#">styde.se</a>
  <span class="sep">/</span>
  <a href="#">Forge</a>
  <span class="sep">/</span>
  <span style="color:var(--text2)">Command Center</span>
</div>
<div class="layout">
  <div class="main">
    <div class="metrics" role="region" aria-label="System metrics">
      <div class="metric" tabindex="0">
        <div class="label">Active Agents</div>
        <div class="value accent">14</div>
        <div class="sub">+2 since last hour</div>
      </div>
      <div class="metric" tabindex="0">
        <div class="label">Blueprints</div>
        <div class="value purple">46</div>
        <div class="sub">12 in staging</div>
      </div>
      <div class="metric" tabindex="0">
        <div class="label">Avg Score</div>
        <div class="value green">90.4</div>
        <div class="sub">+2.1% this week</div>
      </div>
      <div class="metric" tabindex="0">
        <div class="label">GPU Load</div>
        <div class="value orange">62%</div>
        <div class="sub">4/4 online</div>
      </div>
    </div>
    <div class="card" style="margin-bottom:16px">
      <div class="card-header">
        <span class="card-title">Agent Fleet — Status</span>
        <span class="card-action" onclick="alert('Opening agent detail view')">View All →</span>
      </div>
      <table class="agent-table" role="grid" aria-label="Agent status table">
        <thead>
          <tr>
            <th>Agent</th>
            <th>Role</th>
            <th>Status</th>
            <th>Uptime</th>
            <th>Tasks</th>
          </tr>
        </thead>
        <tbody>
          <tr onclick="alert('Navigating to agent: Hermes Orchestrator')" style="cursor:pointer">
            <td><span class="status-dot green"></span><span class="agent-name">Hermes</span></td>
            <td><span class="agent-role">Orchestrator</span></td>
            <td style="color:var(--green)">Online</td>
            <td>4h 12m</td>
            <td>47</td>
          </tr>
          <tr onclick="alert('Navigating to agent: Caveman')" style="cursor:pointer">
            <td><span class="status-dot green"></span><span class="agent-name">Caveman</span></td>
            <td><span class="agent-role">Coder (ultra)</span></td>
            <td style="color:var(--green)">Online</td>
            <td>3h 48m</td>
            <td>31</td>
          </tr>
          <tr onclick="alert('Navigating to agent: PrecisionForge')" style="cursor:pointer">
            <td><span class="status-dot orange"></span><span class="agent-name">Precision</span></td>
            <td><span class="agent-role">Batch Trainer</span></td>
            <td style="color:var(--orange)">Training</td>
            <td>1h 03m</td>
            <td>12</td>
          </tr>
          <tr onclick="alert('Navigating to agent: WebMockup')" style="cursor:pointer">
            <td><span class="status-dot green"></span><span class="agent-name">Mockup</span></td>
            <td><span class="agent-role">Prototyper</span></td>
            <td style="color:var(--green)">Online</td>
            <td>2h 31m</td>
            <td>8</td>
          </tr>
          <tr onclick="alert('Navigating to agent: DelegateTask Worker Pool')" style="cursor:pointer">
            <td><span class="status-dot purple"></span><span class="agent-name">Workers</span></td>
            <td><span class="agent-role">Sub-agent pool</span></td>
            <td style="color:var(--purple)">10 active</td>
            <td>6h 00m</td>
            <td>142</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">GPU Monitor</span>
        <span class="card-action" onclick="document.querySelector('.gpu-details').classList.toggle('open');this.textContent=this.textContent==='Details ▸'?'Details ▾':'Details ▸'">Details ▸</span>
      </div>
      <div class="gpu-bar" role="region" aria-label="GPU utilization">
        <div class="gpu-item">
          <span class="gpu-label">GPU 0</span>
          <div class="gpu-track" role="progressbar" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100">
            <div class="gpu-fill a">72%</div>
          </div>
          <span class="gpu-pct">72%</span>
        </div>
        <div class="gpu-item">
          <span class="gpu-label">GPU 1</span>
          <div class="gpu-track" role="progressbar" aria-valuenow="88" aria-valuemin="0" aria-valuemax="100">
            <div class="gpu-fill b">88%</div>
          </div>
          <span class="gpu-pct">88%</span>
        </div>
        <div class="gpu-item">
          <span class="gpu-label">GPU 2</span>
          <div class="gpu-track" role="progressbar" aria-valuenow="34" aria-valuemin="0" aria-valuemax="100">
            <div class="gpu-fill c">34%</div>
          </div>
          <span class="gpu-pct">34%</span>
        </div>
        <div class="gpu-item">
          <span class="gpu-label">GPU 3</span>
          <div class="gpu-track" role="progressbar" aria-valuenow="56" aria-valuemin="0" aria-valuemax="100">
            <div class="gpu-fill d">56%</div>
          </div>
          <span class="gpu-pct">56%</span>
        </div>
      </div>
      <div class="collapsible gpu-details">
        <div class="collapsible-body">
          <div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:.78rem">
            <div><span style="color:var(--text3)">Memory:</span> 11.2 / 24 GB</div>
            <div><span style="color:var(--text3)">Temp:</span> 68°C avg</div>
            <div><span style="color:var(--text3)">Power:</span> 142W</div>
            <div><span style="color:var(--text3)">PCIe:</span> Gen4 x16</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="sidebar">
    <div class="card">
      <div class="card-header">
        <span class="card-title">Activity Feed</span>
        <span class="card-action" onclick="alert('View full activity log')">All →</span>
      </div>
      <div class="activity-list" role="log" aria-label="Recent activity">
        <div class="activity-item" tabindex="0">
          <div class="activity-icon deploy">D</div>
          <div class="activity-content">
            <div class="activity-text"><strong>Caveman</strong> completed blueprint <em>#BP-042</em></div>
            <div class="activity-time">2 min ago</div>
          </div>
        </div>
        <div class="activity-item" tabindex="0">
          <div class="activity-icon train">T</div>
          <div class="activity-content">
            <div class="activity-text"><strong>PrecisionForge</strong> batch #12 finished — avg score 91.2</div>
            <div class="activity-time">7 min ago</div>
          </div>
        </div>
        <div class="activity-item" tabindex="0">
          <div class="activity-icon build">B</div>
          <div class="activity-content">
            <div class="activity-text"><strong>Hermes</strong> spawned 3 sub-agents for dashboard task</div>
            <div class="activity-time">13 min ago</div>
          </div>
        </div>
        <div class="activity-item" tabindex="0">
          <div class="activity-icon error">E</div>
          <div class="activity-content">
            <div class="activity-text"><strong>Worker #7</strong> hit rate limit — retrying in 30s</div>
            <div class="activity-time">19 min ago</div>
          </div>
        </div>
        <div class="activity-item" tabindex="0">
          <div class="activity-icon deploy">D</div>
          <div class="activity-content">
            <div class="activity-text"><strong>WebMockup</strong> published new dashboard prototype</div>
            <div class="activity-time">24 min ago</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">System Health</span>
        <span class="card-action" onclick="alert('Refreshing health data')">Refresh</span>
      </div>
      <div class="status-grid">
        <div class="status-item">
          <div class="num" style="color:var(--green)">98.7%</div>
          <div class="lbl">Uptime</div>
        </div>
        <div class="status-item">
          <div class="num" style="color:var(--accent)">847ms</div>
          <div class="lbl">Avg Latency</div>
        </div>
        <div class="status-item">
          <div class="num" style="color:var(--orange)">2</div>
          <div class="lbl">Warnings</div>
        </div>
        <div class="status-item">
          <div class="num" style="color:var(--green)">16</div>
          <div class="lbl">Queued Tasks</div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">Quick Actions</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <button onclick="alert('Spawning new evaluation agent')" style="background:var(--surface);border:1px solid var(--border);color:var(--text);padding:8px 14px;border-radius:6px;font-size:.78rem;cursor:pointer;text-align:left;transition:.15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='var(--surface)'">+ New Agent</button>
        <button onclick="alert('Starting blueprint evaluation batch')" style="background:var(--surface);border:1px solid var(--border);color:var(--text);padding:8px 14px;border-radius:6px;font-size:.78rem;cursor:pointer;text-align:left;transition:.15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='var(--surface)'">Run Evaluation</button>
        <button onclick="alert('Opening monitoring dashboard')" style="background:var(--surface);border:1px solid var(--border);color:var(--text);padding:8px 14px;border-radius:6px;font-size:.78rem;cursor:pointer;text-align:left;transition:.15s" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='var(--surface)'">Open Monitoring</button>
        <button onclick="alert('Generating system report')" style="background:var(--surface);border:1px solid var(--border);color:var(--text);padding:8px 14px;border-radius:6px;font-size:.78rem;cursor:pointer;text-align:left;transition:.15s" onmouseover="this.style.background='var(--surface2')" onmouseout="this.style.background='var(--surface)'">Generate Report</button>
      </div>
    </div>
  </div>
</div>
<footer class="footer" role="contentinfo">
  <span>Styde Forge v2.1.4 — Command Center</span>
  <div class="footer-links">
    <a href="#" onclick="alert('Documentation')">Docs</a>
    <a href="#" onclick="alert('API Reference')">API</a>
    <a href="#" onclick="alert('Status Page')">Status</a>
    <a href="#" onclick="alert('Contact Support')">Support</a>
    <a href="#" onclick="alert('styde.se')">styde.se</a>
  </div>
</footer>
<script>
document.querySelectorAll('.collapsible').forEach(function(el){
  var header = el.previousElementSibling;
  if(header && header.classList.contains('card-action')) return;
});
document.querySelectorAll('.gpu-details .collapsible-body').forEach(function(body){
  body.style.maxHeight = '300px';
});
console.log('Styde Forge Command Center loaded');
</script>
</body>
</html>
```