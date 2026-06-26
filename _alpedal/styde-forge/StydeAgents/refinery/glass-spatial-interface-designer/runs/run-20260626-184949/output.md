mockup-01-glass-terminal-dashboard.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass Terminal Dashboard</title>
<style>
  :root {
    --glass-bg: rgba(15, 20, 30, 0.55);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-blur: 24px;
    --edge-glow: inset 0 1px 0 rgba(255,255,255,0.12), inset 0 0 60px rgba(120,180,255,0.03);
    --depth-z1: translateZ(0px);
    --depth-z2: translateZ(30px);
    --depth-z3: translateZ(60px);
    --depth-z4: translateZ(100px);
    --ambient-top: radial-gradient(ellipse 80% 60% at 50% -20%, rgba(90, 160, 255, 0.15) 0%, transparent 70%);
    --ambient-bottom: radial-gradient(ellipse 70% 50% at 30% 120%, rgba(180, 100, 255, 0.08) 0%, transparent 60%);
    --glass-texture: repeating-linear-gradient(90deg, transparent 0px, rgba(255,255,255,0.015) 1px, transparent 2px);
    --text-primary: rgba(220, 230, 245, 0.9);
    --text-secondary: rgba(180, 195, 220, 0.6);
    --accent-cyan: rgba(80, 210, 255, 0.7);
    --accent-purple: rgba(160, 120, 255, 0.5);
    --accent-green: rgba(80, 220, 160, 0.5);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    min-height: 100vh;
    background: #080c14;
    background-image:
      radial-gradient(ellipse 90% 70% at 20% 30%, rgba(40, 80, 160, 0.12) 0%, transparent 60%),
      radial-gradient(ellipse 70% 80% at 80% 70%, rgba(100, 40, 180, 0.08) 0%, transparent 50%),
      radial-gradient(ellipse 50% 50% at 50% 50%, rgba(20, 40, 80, 0.2) 0%, transparent 80%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    perspective: 800px;
  }
  .dashboard {
    width: 1280px;
    max-width: 100%;
    display: grid;
    grid-template-columns: 260px 1fr 300px;
    grid-template-rows: 60px 1fr 1fr 80px;
    gap: 16px;
    padding: 20px;
    transform-style: preserve-3d;
  }
  .glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    box-shadow: var(--edge-glow);
    position: relative;
    overflow: hidden;
  }
  .glass-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--glass-texture);
    pointer-events: none;
  }
  .glass-panel::after {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--ambient-top);
    pointer-events: none;
  }
  .glass-panel > * { position: relative; z-index: 1; }
  .header {
    grid-column: 1 / -1;
    grid-row: 1;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transform: var(--depth-z2);
  }
  .header h1 {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-secondary);
  }
  .header-status {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: var(--text-secondary);
  }
  .indicator {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 8px var(--accent-green);
  }
  .sidebar {
    grid-row: 2 / 4;
    padding: 20px;
    transform: var(--depth-z1);
  }
  .nav-item {
    padding: 10px 14px;
    margin-bottom: 4px;
    border-radius: 10px;
    font-size: 13px;
    color: var(--text-secondary);
    transition: all 0.2s;
    cursor: default;
  }
  .nav-item.active {
    background: rgba(80, 210, 255, 0.08);
    color: var(--accent-cyan);
    border-left: 2px solid var(--accent-cyan);
  }
  .nav-item:hover { background: rgba(255,255,255,0.03); }
  .nav-divider {
    height: 1px;
    background: var(--glass-border);
    margin: 12px 0;
  }
  .main-metric {
    grid-column: 2;
    grid-row: 2;
    padding: 24px;
    transform: var(--depth-z3);
  }
  .metric-row {
    display: flex;
    gap: 16px;
    align-items: flex-end;
    margin-bottom: 20px;
  }
  .metric-value {
    font-size: 48px;
    font-weight: 400;
    color: var(--text-primary);
    letter-spacing: -1px;
    line-height: 1;
  }
  .metric-unit {
    font-size: 16px;
    color: var(--text-secondary);
    padding-bottom: 6px;
  }
  .metric-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
  }
  .metric-change {
    font-size: 13px;
    color: var(--accent-green);
  }
  .activity-feed {
    grid-column: 2;
    grid-row: 3;
    padding: 20px;
    transform: var(--depth-z2);
  }
  .feed-item {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
    color: var(--text-secondary);
  }
  .feed-dot {
    width: 4px; height: 4px;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
  }
  .feed-dot.cyan { background: var(--accent-cyan); }
  .feed-dot.purple { background: var(--accent-purple); }
  .feed-dot.green { background: var(--accent-green); }
  .feed-time {
    font-size: 11px;
    color: rgba(255,255,255,0.25);
    margin-left: auto;
    flex-shrink: 0;
  }
  .right-panel {
    grid-row: 2 / 4;
    padding: 20px;
    transform: var(--depth-z2);
  }
  .right-panel h3 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-secondary);
    margin-bottom: 16px;
  }
  .stat-block {
    margin-bottom: 16px;
    padding: 14px;
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.04);
  }
  .stat-block .stat-label {
    font-size: 11px;
    color: var(--text-secondary);
    margin-bottom: 4px;
  }
  .stat-block .stat-number {
    font-size: 22px;
    font-weight: 400;
    color: var(--text-primary);
  }
  .stat-block .stat-bar {
    height: 3px;
    border-radius: 2px;
    margin-top: 8px;
    background: rgba(255,255,255,0.06);
  }
  .stat-block .stat-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: var(--accent-cyan);
    width: 72%;
  }
  .footer {
    grid-column: 1 / -1;
    grid-row: 4;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: rgba(255,255,255,0.2);
    transform: var(--depth-z1);
  }
  .footer-actions { display: flex; gap: 16px; }
  .footer-actions span { cursor: default; }
</style>
</head>
<body>
<div class="dashboard">
  <div class="header glass-panel">
    <h1>Terminal / Glass</h1>
    <div class="header-status">
      <span class="indicator"></span>
      <span>system online</span>
      <span style="opacity:0.3">|</span>
      <span>v2.4.1</span>
    </div>
  </div>
  <div class="sidebar glass-panel">
    <div class="nav-item active">Overview</div>
    <div class="nav-item">Metrics</div>
    <div class="nav-item">Deployments</div>
    <div class="nav-item">Logs</div>
    <div class="nav-divider"></div>
    <div class="nav-item">Settings</div>
    <div class="nav-item" style="margin-top:auto;color:rgba(255,255,255,0.15);font-size:11px;padding-top:40px">forge-agent v1</div>
  </div>
  <div class="main-metric glass-panel">
    <div class="metric-row">
      <div>
        <div class="metric-label">active agents</div>
        <div class="metric-value">24</div>
      </div>
      <div class="metric-unit">/ 32 slots</div>
    </div>
    <div style="display:flex;gap:24px">
      <div>
        <div class="metric-label" style="font-size:10px;margin-bottom:4px">throughput</div>
        <div style="font-size:18px;color:var(--text-primary)">142 req/s</div>
        <div class="metric-change">+12%</div>
      </div>
      <div>
        <div class="metric-label" style="font-size:10px;margin-bottom:4px">avg latency</div>
        <div style="font-size:18px;color:var(--text-primary)">84ms</div>
        <div class="metric-change" style="color:rgba(255,180,80,0.6)">-3ms</div>
      </div>
      <div>
        <div class="metric-label" style="font-size:10px;margin-bottom:4px">error rate</div>
        <div style="font-size:18px;color:var(--text-primary)">0.02%</div>
        <div class="metric-change" style="color:var(--accent-green)">stable</div>
      </div>
    </div>
  </div>
  <div class="activity-feed glass-panel">
    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text-secondary);margin-bottom:12px">Recent Activity</div>
    <div class="feed-item">
      <div class="feed-dot cyan"></div>
      <span>deploy-agent completed build #1847</span>
      <span class="feed-time">12s</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot purple"></div>
      <span>eval pipeline approved mockup set</span>
      <span class="feed-time">43s</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot green"></div>
      <span>resource pool scaled to 24/32</span>
      <span class="feed-time">2m</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot cyan"></div>
      <span>glass texture cache rebuilt</span>
      <span class="feed-time">4m</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot purple"></div>
      <span>gate stage: 3/3 checks passed</span>
      <span class="feed-time">7m</span>
    </div>
  </div>
  <div class="right-panel glass-panel">
    <h3>System Health</h3>
    <div class="stat-block">
      <div class="stat-label">CPU</div>
      <div class="stat-number">34%</div>
      <div class="stat-bar"><div class="stat-bar-fill" style="width:34%"></div></div>
    </div>
    <div class="stat-block">
      <div class="stat-label">Memory</div>
      <div class="stat-number">6.2 GB</div>
      <div class="stat-bar"><div class="stat-bar-fill" style="width:52%;background:var(--accent-purple)"></div></div>
    </div>
    <div class="stat-block">
      <div class="stat-label">Network</div>
      <div class="stat-number">1.4 Gbps</div>
      <div class="stat-bar"><div class="stat-bar-fill" style="width:88%;background:var(--accent-green)"></div></div>
    </div>
  </div>
  <div class="footer glass-panel">
    <span>6 agents active in pipeline | 3 queued</span>
    <div class="footer-actions">
      <span>deploy</span>
      <span>rollback</span>
      <span>scale</span>
    </div>
  </div>
</div>
</body>
</html>
```
---
mockup-02-glass-pipeline-monitor.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass Pipeline Monitor</title>
<style>
  :root {
    --glass-bg: rgba(12, 18, 28, 0.6);
    --glass-border: rgba(255, 255, 255, 0.06);
    --glass-blur: 28px;
    --edge-glow: inset 0 1px 0 rgba(255,255,255,0.10), inset 0 0 80px rgba(100,160,255,0.02);
    --depth-z1: translateZ(0px);
    --depth-z2: translateZ(40px);
    --depth-z3: translateZ(80px);
    --depth-z4: translateZ(120px);
    --ambient-top: radial-gradient(ellipse 90% 50% at 50% -10%, rgba(60, 130, 255, 0.10) 0%, transparent 70%);
    --text-primary: rgba(210, 225, 245, 0.92);
    --text-secondary: rgba(160, 180, 210, 0.5);
    --text-dim: rgba(160, 180, 210, 0.25);
    --accent-cyan: rgba(70, 200, 255, 0.65);
    --accent-amber: rgba(255, 200, 80, 0.6);
    --accent-rose: rgba(255, 100, 120, 0.5);
    --accent-lime: rgba(100, 230, 160, 0.55);
    --glass-texture: repeating-linear-gradient(0deg, transparent 0px, rgba(255,255,255,0.008) 1px, transparent 2px);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    min-height: 100vh;
    background: #060a12;
    background-image:
      radial-gradient(ellipse 80% 60% at 15% 25%, rgba(30, 60, 140, 0.10) 0%, transparent 60%),
      radial-gradient(ellipse 60% 80% at 85% 65%, rgba(80, 30, 160, 0.06) 0%, transparent 50%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    perspective: 1000px;
  }
  .dashboard {
    width: 1320px;
    max-width: 100%;
    display: grid;
    grid-template-columns: 240px 1fr 1fr 200px;
    grid-template-rows: 56px 48px 1fr 1fr;
    gap: 14px;
    padding: 20px;
    transform-style: preserve-3d;
  }
  .glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    box-shadow: var(--edge-glow);
    position: relative;
    overflow: hidden;
  }
  .glass-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--glass-texture);
    pointer-events: none;
  }
  .glass-panel::after {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--ambient-top);
    pointer-events: none;
  }
  .glass-panel > * { position: relative; z-index: 1; }
  .header {
    grid-column: 1 / -1;
    grid-row: 1;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transform: var(--depth-z2);
  }
  .stages {
    grid-column: 2 / 4;
    grid-row: 2;
    display: flex;
    align-items: center;
    gap: 0;
    padding: 0 16px;
    transform: var(--depth-z3);
  }
  .stage-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: var(--text-secondary);
    letter-spacing: 0.5px;
  }
  .stage-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .stage-dot.pass { background: var(--accent-lime); border-color: var(--accent-lime); box-shadow: 0 0 6px var(--accent-lime); }
  .stage-dot.active { background: var(--accent-cyan); border-color: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan); animation: pulse-dot 2s ease-in-out infinite; }
  .stage-dot.pending { background: transparent; }
  .stage-arrow { color: rgba(255,255,255,0.08); font-size: 14px; margin: 0 6px; }
  @keyframes pulse-dot { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
  .sidebar {
    grid-row: 2 / 5;
    padding: 16px;
    transform: var(--depth-z1);
  }
  .pipeline-card {
    background: rgba(255,255,255,0.02);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.04);
  }
  .pipeline-card .p-name { font-size: 13px; color: var(--text-primary); margin-bottom: 4px; }
  .pipeline-card .p-status { font-size: 11px; color: var(--text-secondary); }
  .pipeline-card .p-status.good { color: var(--accent-lime); }
  .main-vis {
    grid-column: 2 / 4;
    grid-row: 3 / 5;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transform: var(--depth-z4);
  }
  .chain-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
  }
  .chain-label {
    width: 90px;
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }
  .chain-bar {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: rgba(255,255,255,0.04);
    overflow: hidden;
  }
  .chain-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.4s;
  }
  .chain-bar-fill.cyan { background: var(--accent-cyan); }
  .chain-bar-fill.amber { background: var(--accent-amber); }
  .chain-bar-fill.lime { background: var(--accent-lime); }
  .chain-bar-fill.rose { background: var(--accent-rose); }
  .chain-val {
    width: 50px;
    text-align: right;
    font-size: 13px;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
  }
  .right-rail {
    grid-row: 2 / 5;
    padding: 16px;
    transform: var(--depth-z2);
  }
  .alert-item {
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    font-size: 12px;
    color: var(--text-secondary);
  }
  .alert-item .a-time { font-size: 10px; color: var(--text-dim); }
</style>
</head>
<body>
<div class="dashboard">
  <div class="header glass-panel">
    <div style="font-size:13px;color:var(--text-primary);letter-spacing:1px">Pipeline Monitor</div>
    <div style="font-size:11px;color:var(--text-secondary)">eval cycle #2341 | gate: open</div>
  </div>
  <div class="sidebar glass-panel">
    <div class="pipeline-card">
      <div class="p-name">forge-main</div>
      <div class="p-status good">running 4/4 stages</div>
    </div>
    <div class="pipeline-card">
      <div class="p-name">refinery-edge</div>
      <div class="p-status">waiting 1/4</div>
    </div>
    <div class="pipeline-card">
      <div class="p-name">production-1</div>
      <div class="p-status">idle 0/4</div>
    </div>
    <div class="pipeline-card">
      <div class="p-name">batch-train</div>
      <div class="p-status good">running 3/4</div>
    </div>
    <div style="margin-top:16px;padding:10px;background:rgba(70,200,255,0.05);border-radius:8px;border:1px solid rgba(70,200,255,0.1)">
      <div style="font-size:11px;color:var(--accent-cyan);margin-bottom:4px">active sub-agents</div>
      <div style="font-size:24px;color:var(--text-primary)">12</div>
    </div>
  </div>
  <div class="stages glass-panel">
    <div class="stage-item"><div class="stage-dot pass"></div>Generation</div>
    <span class="stage-arrow">→</span>
    <div class="stage-item"><div class="stage-dot pass"></div>Evaluation</div>
    <span class="stage-arrow">→</span>
    <div class="stage-item"><div class="stage-dot active"></div>Gate</div>
    <span class="stage-arrow">→</span>
    <div class="stage-item"><div class="stage-dot pending"></div>Promotion</div>
  </div>
  <div class="main-vis glass-panel">
    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text-secondary);margin-bottom:4px">stage throughput</div>
    <div class="chain-row">
      <div class="chain-label">generation</div>
      <div class="chain-bar"><div class="chain-bar-fill cyan" style="width:100%"></div></div>
      <div class="chain-val">1.2s</div>
    </div>
    <div class="chain-row">
      <div class="chain-label">evaluation</div>
      <div class="chain-bar"><div class="chain-bar-fill lime" style="width:72%"></div></div>
      <div class="chain-val">2.8s</div>
    </div>
    <div class="chain-row">
      <div class="chain-label">gate</div>
      <div class="chain-bar"><div class="chain-bar-fill amber" style="width:45%"></div></div>
      <div class="chain-val">0.9s</div>
    </div>
    <div class="chain-row">
      <div class="chain-label">promotion</div>
      <div class="chain-bar"><div class="chain-bar-fill rose" style="width:30%"></div></div>
      <div class="chain-val">1.5s</div>
    </div>
    <div style="display:flex;gap:24px;margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.04)">
      <div><span style="font-size:11px;color:var(--text-dim)">pass rate</span><br><span style="font-size:18px;color:var(--accent-lime)">96.2%</span></div>
      <div><span style="font-size:11px;color:var(--text-dim)">avg score</span><br><span style="font-size:18px;color:var(--text-primary)">87.4</span></div>
      <div><span style="font-size:11px;color:var(--text-dim)">queued</span><br><span style="font-size:18px;color:var(--accent-amber)">8</span></div>
    </div>
  </div>
  <div class="right-rail glass-panel">
    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text-secondary);margin-bottom:8px">alerts</div>
    <div class="alert-item">gate score below threshold for bp-23 <span class="a-time">2m ago</span></div>
    <div class="alert-item">refinery-edge completed cycle <span class="a-time">7m ago</span></div>
    <div class="alert-item">resource pool at 78% capacity <span class="a-time">12m ago</span></div>
    <div class="alert-item">batch-train lockfile released <span class="a-time">18m ago</span></div>
    <div class="alert-item">evaluation: 3 personas updated <span class="a-time">25m ago</span></div>
  </div>
</div>
</body>
</html>
```
---
mockup-03-glass-eval-scorecard.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass Eval Scorecard</title>
<style>
  :root {
    --glass-bg: rgba(10, 16, 26, 0.58);
    --glass-border: rgba(255, 255, 255, 0.07);
    --glass-blur: 26px;
    --edge-glow: inset 0 1px 0 rgba(255,255,255,0.11), inset 0 0 70px rgba(90,150,255,0.025);
    --depth-z1: translateZ(0px);
    --depth-z2: translateZ(35px);
    --depth-z3: translateZ(70px);
    --depth-z4: translateZ(110px);
    --ambient-top: radial-gradient(ellipse 70% 50% at 60% -5%, rgba(70, 140, 255, 0.08) 0%, transparent 60%);
    --ambient-corner: radial-gradient(ellipse 40% 40% at 90% 90%, rgba(140, 80, 255, 0.05) 0%, transparent 50%);
    --text-primary: rgba(215, 228, 248, 0.92);
    --text-secondary: rgba(160, 180, 215, 0.55);
    --text-dim: rgba(160, 180, 215, 0.2);
    --score-high: rgba(80, 220, 170, 0.65);
    --score-mid: rgba(255, 200, 80, 0.55);
    --score-low: rgba(255, 110, 130, 0.5);
    --accent-cyan: rgba(70, 200, 255, 0.6);
    --accent-purple: rgba(160, 120, 255, 0.45);
    --glass-texture: repeating-linear-gradient(45deg, transparent 0px, rgba(255,255,255,0.006) 1px, transparent 2px);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    min-height: 100vh;
    background: #070b14;
    background-image:
      radial-gradient(ellipse 70% 60% at 30% 20%, rgba(35, 70, 150, 0.10) 0%, transparent 55%),
      radial-gradient(ellipse 50% 70% at 70% 80%, rgba(90, 40, 170, 0.06) 0%, transparent 50%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    perspective: 900px;
  }
  .dashboard {
    width: 1200px;
    max-width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 52px 160px 1fr;
    gap: 14px;
    padding: 20px;
    transform-style: preserve-3d;
  }
  .glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    box-shadow: var(--edge-glow);
    position: relative;
    overflow: hidden;
  }
  .glass-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--glass-texture);
    pointer-events: none;
  }
  .glass-panel::after {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--ambient-top);
    pointer-events: none;
  }
  .glass-panel > * { position: relative; z-index: 1; }
  .header {
    grid-column: 1 / -1;
    grid-row: 1;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transform: var(--depth-z2);
  }
  .score-hero {
    grid-column: 1 / -1;
    grid-row: 2;
    padding: 24px 32px;
    display: flex;
    align-items: center;
    gap: 40px;
    transform: var(--depth-z3);
  }
  .score-ring {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    position: relative;
    flex-shrink: 0;
  }
  .score-ring svg {
    transform: rotate(-90deg);
    width: 110px;
    height: 110px;
  }
  .score-ring-bg { fill: none; stroke: rgba(255,255,255,0.04); stroke-width: 4; }
  .score-ring-fill { fill: none; stroke: var(--accent-cyan); stroke-width: 4; stroke-linecap: round; stroke-dasharray: 314; stroke-dashoffset: 31; }
  .score-ring-text {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 400;
    color: var(--text-primary);
    letter-spacing: -0.5px;
  }
  .score-meta { flex: 1; }
  .score-meta .meta-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-secondary); margin-bottom: 6px; }
  .score-meta .meta-run { font-size: 13px; color: var(--text-primary); margin-bottom: 8px; }
  .score-tags { display: flex; gap: 8px; flex-wrap: wrap; }
  .score-tag {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    letter-spacing: 0.5px;
    background: rgba(255,255,255,0.04);
    color: var(--text-secondary);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .score-tag.high { background: rgba(80,220,170,0.08); border-color: rgba(80,220,170,0.15); color: var(--score-high); }
  .score-tag.low { background: rgba(255,110,130,0.08); border-color: rgba(255,110,130,0.15); color: var(--score-low); }
  .col {
    padding: 20px;
    transform: var(--depth-z2);
  }
  .col h3 {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-dim);
    margin-bottom: 14px;
  }
  .criterion {
    margin-bottom: 14px;
    padding: 12px;
    background: rgba(255,255,255,0.015);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.03);
  }
  .criterion .c-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }
  .criterion .c-name { font-size: 12px; color: var(--text-primary); }
  .criterion .c-score { font-size: 14px; font-variant-numeric: tabular-nums; }
  .criterion .c-score.high { color: var(--score-high); }
  .criterion .c-score.mid { color: var(--score-mid); }
  .criterion .c-score.low { color: var(--score-low); }
  .criterion .c-bar {
    height: 2px;
    border-radius: 1px;
    background: rgba(255,255,255,0.04);
    margin-top: 6px;
  }
  .criterion .c-bar-fill {
    height: 100%;
    border-radius: 1px;
  }
  .c-bar-fill.high { background: var(--score-high); }
  .c-bar-fill.mid { background: var(--score-mid); }
  .c-bar-fill.low { background: var(--score-low); }
</style>
</head>
<body>
<div class="dashboard">
  <div class="header glass-panel">
    <div style="font-size:13px;color:var(--text-primary);letter-spacing:0.5px">Eval Scorecard</div>
    <div style="font-size:11px;color:var(--text-secondary)">run 20260626-184829</div>
  </div>
  <div class="score-hero glass-panel">
    <div class="score-ring">
      <svg viewBox="0 0 110 110">
        <circle class="score-ring-bg" cx="55" cy="55" r="50"/>
        <circle class="score-ring-fill" cx="55" cy="55" r="50"/>
      </svg>
      <div class="score-ring-text">70.0</div>
    </div>
    <div class="score-meta">
      <div class="meta-label">composite score</div>
      <div class="meta-run">70.0 / 100 — gate threshold: 75</div>
      <div class="score-tags">
        <span class="score-tag high">correctness 93</span>
        <span class="score-tag low">clarity 55</span>
        <span class="score-tag low">efficiency 50</span>
        <span class="score-tag">gate: blocked</span>
      </div>
    </div>
  </div>
  <div class="col glass-panel">
    <h3>generation</h3>
    <div class="criterion">
      <div class="c-header"><span class="c-name">artifact output</span><span class="c-score mid">72</span></div>
      <div class="c-bar"><div class="c-bar-fill mid" style="width:72%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">format compliance</span><span class="c-score low">50</span></div>
      <div class="c-bar"><div class="c-bar-fill low" style="width:50%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">mockup count</span><span class="c-score high">90</span></div>
      <div class="c-bar"><div class="c-bar-fill high" style="width:90%"></div></div>
    </div>
  </div>
  <div class="col glass-panel">
    <h3>evaluation</h3>
    <div class="criterion">
      <div class="c-header"><span class="c-name">correctness</span><span class="c-score high">93</span></div>
      <div class="c-bar"><div class="c-bar-fill high" style="width:93%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">clarity</span><span class="c-score low">55</span></div>
      <div class="c-bar"><div class="c-bar-fill low" style="width:55%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">efficiency</span><span class="c-score low">50</span></div>
      <div class="c-bar"><div class="c-bar-fill low" style="width:50%"></div></div>
    </div>
  </div>
  <div class="col glass-panel">
    <h3>gate / promotion</h3>
    <div class="criterion">
      <div class="c-header"><span class="c-name">meta-output ban</span><span class="c-score mid">65</span></div>
      <div class="c-bar"><div class="c-bar-fill mid" style="width:65%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">artifact-first</span><span class="c-score mid">70</span></div>
      <div class="c-bar"><div class="c-bar-fill mid" style="width:70%"></div></div>
    </div>
    <div class="criterion">
      <div class="c-header"><span class="c-name">constructor reframe</span><span class="c-score high">88</span></div>
      <div class="c-bar"><div class="c-bar-fill high" style="width:88%"></div></div>
    </div>
    <div style="margin-top:auto;padding-top:12px;border-top:1px solid rgba(255,255,255,0.04);font-size:11px;color:var(--accent-cyan)">
      promotion: pending 3/3 checks
    </div>
  </div>
</div>
</body>
</html>
```
---
3 mockup files. Each is a full self-contained HTML dashboard. Shared CSS architecture via :root custom properties. Zero meta-discourse — only artifacts. Delivered.