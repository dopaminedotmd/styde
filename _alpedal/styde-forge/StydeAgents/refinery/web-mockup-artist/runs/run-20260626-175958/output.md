<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Agent Command Suite</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg-deep: #0b0d14;
  --bg-panel: #11131f;
  --bg-card: #161928;
  --bg-card-hover: #1c1f32;
  --border: #1e2238;
  --border-glow: #2a2f4f;
  --text-primary: #e8eaf0;
  --text-secondary: #8a8fb0;
  --text-muted: #55587a;
  --accent-1: #6c5ce7;
  --accent-2: #00cec9;
  --accent-3: #fd79a8;
  --accent-4: #fdcb6e;
  --status-ok: #00b894;
  --status-warn: #fdcb6e;
  --status-err: #e17055;
  --gpu-0: #6c5ce7;
  --gpu-1: #00cec9;
  --gpu-2: #fd79a8;
  --radius: 10px;
  --radius-sm: 6px;
  --shadow-card: 0 4px 24px rgba(0,0,0,0.4);
  --transition: 240ms cubic-bezier(0.25,0.46,0.45,0.94);
}
html { font-size: 15px; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg-deep);
  color: var(--text-primary);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
a { color: var(--accent-2); text-decoration: none; transition: color var(--transition); }
a:hover { color: #81ecec; }
::selection { background: var(--accent-1); color: #fff; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
/* HEADER */
.site-header {
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border);
  padding: 0 2rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-left { display: flex; align-items: center; gap: 1.5rem; }
.logo {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.logo span { font-weight: 300; color: var(--text-muted); -webkit-text-fill-color: var(--text-muted); }
.header-nav { display: flex; gap: 0.25rem; }
.header-nav a {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: var(--text-secondary);
  transition: all var(--transition);
}
.header-nav a:hover, .header-nav a.active {
  background: rgba(108,92,231,0.12);
  color: var(--accent-1);
}
.header-nav a.active { color: var(--text-primary); background: rgba(108,92,231,0.18); }
.header-right { display: flex; align-items: center; gap: 1rem; }
.status-pill {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}
.status-pill.online { background: rgba(0,184,148,0.12); color: var(--status-ok); border: 1px solid rgba(0,184,148,0.25); }
.status-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.hamburger {
  display: none; flex-direction: column; gap: 4px;
  background: none; border: none; cursor: pointer; padding: 6px;
}
.hamburger span { display: block; width: 22px; height: 2px; background: var(--text-secondary); border-radius: 2px; transition: var(--transition); }
/* BREADCRUMB */
.breadcrumb {
  padding: 0.75rem 2rem;
  background: rgba(17,19,31,0.6);
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
  color: var(--text-muted);
  display: flex; gap: 0.5rem; align-items: center;
}
.breadcrumb a { color: var(--text-secondary); }
.breadcrumb .sep { color: var(--border); }
/* LAYOUT */
.app-layout {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  gap: 0;
  flex: 1;
  min-height: 0;
}
/* SIDEBAR */
.sidebar {
  background: var(--bg-panel);
  border-right: 1px solid var(--border);
  padding: 1.25rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.sidebar-label {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  padding: 0.5rem 0.75rem;
  margin-top: 0.75rem;
}
.sidebar-label:first-child { margin-top: 0; }
.sidebar-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
}
.sidebar-item:hover { background: rgba(108,92,231,0.08); color: var(--text-primary); }
.sidebar-item.active { background: rgba(108,92,231,0.15); color: var(--accent-1); }
.sidebar-item .icon { width: 18px; text-align: center; font-size: 0.9rem; }
.sidebar-item .badge {
  margin-left: auto;
  font-size: 0.65rem;
  padding: 0.1rem 0.5rem;
  border-radius: 10px;
  background: var(--border);
  color: var(--text-muted);
}
.sidebar-item .badge.warn { background: rgba(253,203,110,0.15); color: var(--status-warn); }
.sidebar-item .badge.err { background: rgba(225,112,85,0.15); color: var(--status-err); }
/* MAIN CONTENT */
.main-content {
  padding: 1.5rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.page-title { font-size: 1.4rem; font-weight: 600; }
.page-subtitle { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; }
/* METRICS ROW */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
  transition: all var(--transition);
  cursor: default;
}
.metric-card:hover {
  border-color: var(--border-glow);
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}
.metric-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); }
.metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  margin-top: 0.4rem;
  line-height: 1.1;
}
.metric-value .unit { font-size: 0.9rem; font-weight: 400; color: var(--text-secondary); }
.metric-change {
  font-size: 0.75rem;
  margin-top: 0.3rem;
  display: inline-flex; align-items: center; gap: 0.25rem;
}
.metric-change.up { color: var(--status-ok); }
.metric-change.down { color: var(--status-err); }
/* AGENT CARDS GRID */
.section-header {
  display: flex; justify-content: space-between; align-items: center;
}
.section-header h2 { font-size: 1.05rem; font-weight: 600; }
.section-header .action-link { font-size: 0.8rem; color: var(--accent-2); cursor: pointer; }
.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.agent-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
  transition: all var(--transition);
}
.agent-card:hover {
  border-color: var(--border-glow);
  box-shadow: var(--shadow-card);
}
.agent-card-header {
  display: flex; justify-content: space-between; align-items: flex-start;
}
.agent-name { font-size: 0.95rem; font-weight: 600; }
.agent-type { font-size: 0.7rem; color: var(--text-muted); margin-top: 0.1rem; }
.agent-status {
  display: flex; align-items: center; gap: 0.35rem;
  font-size: 0.7rem; font-weight: 500; padding: 0.15rem 0.55rem;
  border-radius: 10px;
}
.agent-status.running { background: rgba(0,184,148,0.1); color: var(--status-ok); }
.agent-status.idle { background: rgba(253,203,110,0.1); color: var(--status-warn); }
.agent-status.paused { background: rgba(108,92,231,0.1); color: var(--accent-1); }
.agent-status .dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.agent-stats {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;
  margin-top: 0.75rem;
}
.agent-stat { }
.agent-stat-label { font-size: 0.6rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.04em; }
.agent-stat-value { font-size: 0.8rem; font-weight: 500; margin-top: 0.1rem; }
.agent-progress {
  margin-top: 0.75rem;
  height: 3px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}
.agent-progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.6s ease;
}
.agent-card-footer {
  display: flex; gap: 0.5rem; margin-top: 0.75rem; padding-top: 0.6rem;
  border-top: 1px solid var(--border);
}
.agent-action-btn {
  font-size: 0.7rem;
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
}
.agent-action-btn:hover { border-color: var(--accent-1); color: var(--accent-1); background: rgba(108,92,231,0.06); }
/* GPU MONITOR */
.gpu-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
}
.gpu-panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.gpu-panel-header h3 { font-size: 0.95rem; font-weight: 600; }
.gpu-list { display: flex; flex-direction: column; gap: 0.75rem; }
.gpu-item {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.65rem 0.9rem;
  background: var(--bg-panel);
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--border);
}
.gpu-item.gpu-0 { border-left-color: var(--gpu-0); }
.gpu-item.gpu-1 { border-left-color: var(--gpu-1); }
.gpu-item.gpu-2 { border-left-color: var(--gpu-2); }
.gpu-name { font-size: 0.8rem; font-weight: 500; width: 80px; flex-shrink: 0; }
.gpu-bar-wrap { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.gpu-bar-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.gpu-stats {
  display: flex; gap: 1rem; font-size: 0.7rem; color: var(--text-secondary);
  width: 130px; flex-shrink: 0; text-align: right;
}
/* RIGHT PANEL */
.right-panel {
  background: var(--bg-panel);
  border-left: 1px solid var(--border);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  overflow-y: auto;
}
.panel-section-title {
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-muted); margin-bottom: 0.5rem;
}
/* ACTIVITY FEED */
.activity-feed { display: flex; flex-direction: column; gap: 0.5rem; }
.activity-item {
  display: flex; gap: 0.75rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
}
.activity-item:last-child { border-bottom: none; }
.activity-time { font-size: 0.65rem; color: var(--text-muted); white-space: nowrap; width: 40px; flex-shrink: 0; }
.activity-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 0.25rem; flex-shrink: 0; }
.activity-dot.info { background: var(--accent-1); }
.activity-dot.success { background: var(--status-ok); }
.activity-dot.warn { background: var(--status-warn); }
.activity-dot.err { background: var(--status-err); }
.activity-text { flex: 1; color: var(--text-secondary); line-height: 1.4; }
.activity-text strong { color: var(--text-primary); font-weight: 500; }
/* COLLAPSIBLE PANELS */
.collapsible { border: 1px solid var(--border); border-radius: var(--radius-sm); overflow: hidden; }
.collapsible-trigger {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.65rem 0.9rem;
  background: var(--bg-card);
  cursor: pointer;
  font-size: 0.8rem;
  color: var(--text-secondary);
  transition: background var(--transition);
  user-select: none;
}
.collapsible-trigger:hover { background: var(--bg-card-hover); }
.collapsible-trigger .arrow { transition: transform var(--transition); font-size: 0.6rem; }
.collapsible.open .collapsible-trigger .arrow { transform: rotate(90deg); }
.collapsible-content {
  max-height: 0; overflow: hidden;
  transition: max-height 300ms ease, padding 300ms ease;
  padding: 0 0.9rem;
}
.collapsible.open .collapsible-content {
  max-height: 200px;
  padding: 0.6rem 0.9rem;
}
/* PERFORMANCE MINI CHART */
.mini-chart {
  display: flex; align-items: flex-end; gap: 3px; height: 40px; margin-top: 0.5rem;
}
.mini-bar {
  flex: 1;
  border-radius: 2px 2px 0 0;
  transition: height 0.3s ease;
  background: linear-gradient(to top, var(--accent-1), var(--accent-2));
  opacity: 0.7;
}
.mini-bar:hover { opacity: 1; }
/* FOOTER */
.site-footer {
  background: var(--bg-panel);
  border-top: 1px solid var(--border);
  padding: 1.25rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text-muted);
}
.footer-links { display: flex; gap: 1.5rem; }
.footer-links a { color: var(--text-secondary); font-size: 0.75rem; }
/* RESPONSIVE */
@media (max-width: 1100px) {
  .app-layout { grid-template-columns: 200px 1fr; }
  .right-panel { display: none; }
}
@media (max-width: 800px) {
  .app-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .site-header { padding: 0 1rem; }
  .main-content { padding: 1rem; }
  .breadcrumb { padding: 0.5rem 1rem; }
  .header-nav { display: none; }
  .hamburger { display: flex; }
  .metrics-row { grid-template-columns: repeat(2, 1fr); }
  .agent-grid { grid-template-columns: 1fr; }
  .site-footer { flex-direction: column; gap: 0.5rem; text-align: center; }
}
@media (max-width: 480px) {
  .metrics-row { grid-template-columns: 1fr; }
  .gpu-stats { width: 100px; }
  .gpu-name { width: 60px; }
  .header-right .status-pill { display: none; }
}
</style>
</head>
<body>
<header class="site-header">
  <div class="header-left">
    <div class="logo">styde<span>.se</span></div>
    <nav class="header-nav">
      <a href="#" class="active">Forge</a>
      <a href="#">Dashboard</a>
      <a href="#">Agents</a>
      <a href="#">Training</a>
      <a href="#">Docs</a>
    </nav>
  </div>
  <div class="header-right">
    <div class="status-pill online">
      <span class="dot"></span>
      All Systems
    </div>
    <button class="hamburger" onclick="toggleMobileNav()">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="breadcrumb">
  <a href="#">styde.se</a>
  <span class="sep">/</span>
  <a href="#">Forge</a>
  <span class="sep">/</span>
  <span>Command Suite</span>
</div>
<div class="app-layout">
  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-label">Navigate</div>
    <div class="sidebar-item active">
      <span class="icon">f</span>
      Overview
    </div>
    <div class="sidebar-item">
      <span class="icon">a</span>
      Agents
      <span class="badge">12</span>
    </div>
    <div class="sidebar-item">
      <span class="icon">g</span>
      GPU Pool
    </div>
    <div class="sidebar-item">
      <span class="icon">b</span>
      Blueprints
      <span class="badge warn">4</span>
    </div>
    <div class="sidebar-item">
      <span class="icon">h</span>
      History
    </div>
    <div class="sidebar-label">System</div>
    <div class="sidebar-item">
      <span class="icon">s</span>
      Settings
    </div>
    <div class="sidebar-item">
      <span class="icon">l</span>
      Logs
      <span class="badge err">3</span>
    </div>
    <div class="sidebar-item">
      <span class="icon">p</span>
      Performance
    </div>
  </aside>
  <!-- MAIN -->
  <main class="main-content">
    <div>
      <div class="page-title">Forge Command Suite</div>
      <div class="page-subtitle">Composite score: 89.6 / 100 — Production ready. 3 agents running, 2 idle.</div>
    </div>
    <!-- METRICS -->
    <div class="metrics-row">
      <div class="metric-card">
        <div class="metric-label">Active Agents</div>
        <div class="metric-value">12<span class="unit"> / 20</span></div>
        <div class="metric-change up">+2 this hour</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">GPU Utilization</div>
        <div class="metric-value">74<span class="unit">%</span></div>
        <div class="metric-change up">+12%</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Tasks Completed</div>
        <div class="metric-value">1,847</div>
        <div class="metric-change down">-3% today</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Avg Response</div>
        <div class="metric-value">340<span class="unit">ms</span></div>
        <div class="metric-change up">-22ms</div>
      </div>
    </div>
    <!-- AGENT GRID -->
    <div>
      <div class="section-header">
        <h2>Active Agents</h2>
        <span class="action-link">View all →</span>
      </div>
      <div style="height:0.75rem"></div>
      <div class="agent-grid">
        <div class="agent-card">
          <div class="agent-card-header">
            <div>
              <div class="agent-name">Hermes Orchestrator</div>
              <div class="agent-type">Primary Coordinator</div>
            </div>
            <div class="agent-status running"><span class="dot"></span> Running</div>
          </div>
          <div class="agent-stats">
            <div class="agent-stat">
              <div class="agent-stat-label">Tasks</div>
              <div class="agent-stat-value">142 queued</div>
            </div>
            <div class="agent-stat">
              <div class="agent-stat-label">Uptime</div>
              <div class="agent-stat-value">14h 23m</div>
            </div>
          </div>
          <div class="agent-progress">
            <div class="agent-progress-fill" style="width:68%;background:var(--accent-1);"></div>
          </div>
          <div class="agent-card-footer">
            <button class="agent-action-btn">Pause</button>
            <button class="agent-action-btn">Details</button>
            <button class="agent-action-btn">Logs</button>
          </div>
        </div>
        <div class="agent-card">
          <div class="agent-card-header">
            <div>
              <div class="agent-name">Precision Forge</div>
              <div class="agent-type">Blueprint Optimizer</div>
            </div>
            <div class="agent-status running"><span class="dot"></span> Running</div>
          </div>
          <div class="agent-stats">
            <div class="agent-stat">
              <div class="agent-stat-label">BP Processed</div>
              <div class="agent-stat-value">46/46</div>
            </div>
            <div class="agent-stat">
              <div class="agent-stat-label">Avg Score</div>
              <div class="agent-stat-value">88.4</div>
            </div>
          </div>
          <div class="agent-progress">
            <div class="agent-progress-fill" style="width:100%;background:var(--status-ok);"></div>
          </div>
          <div class="agent-card-footer">
            <button class="agent-action-btn">Review</button>
            <button class="agent-action-btn">Export</button>
          </div>
        </div>
        <div class="agent-card">
          <div class="agent-card-header">
            <div>
              <div class="agent-name">Web Mockup Artist</div>
              <div class="agent-type">Frontend Specialist</div>
            </div>
            <div class="agent-status idle"><span class="dot"></span> Idle</div>
          </div>
          <div class="agent-stats">
            <div class="agent-stat">
              <div class="agent-stat-label">Mockups</div>
              <div class="agent-stat-value">32 delivered</div>
            </div>
            <div class="agent-stat">
              <div class="agent-stat-label">Avg Score</div>
              <div class="agent-stat-value">91.4</div>
            </div>
          </div>
          <div class="agent-progress">
            <div class="agent-progress-fill" style="width:0%;background:var(--text-muted);"></div>
          </div>
          <div class="agent-card-footer">
            <button class="agent-action-btn">Wake</button>
            <button class="agent-action-btn">History</button>
          </div>
        </div>
        <div class="agent-card">
          <div class="agent-card-header">
            <div>
              <div class="agent-name">Delegate Runner</div>
              <div class="agent-type">Sub-agent Pool</div>
            </div>
            <div class="agent-status running"><span class="dot"></span> Running</div>
          </div>
          <div class="agent-stats">
            <div class="agent-stat">
              <div class="agent-stat-label">Active Subs</div>
              <div class="agent-stat-value">7 / 20</div>
            </div>
            <div class="agent-stat">
              <div class="agent-stat-label">Throughput</div>
              <div class="agent-stat-value">3.2/s</div>
            </div>
          </div>
          <div class="agent-progress">
            <div class="agent-progress-fill" style="width:45%;background:var(--accent-3);"></div>
          </div>
          <div class="agent-card-footer">
            <button class="agent-action-btn">Scale</button>
            <button class="agent-action-btn">Monitor</button>
          </div>
        </div>
      </div>
    </div>
    <!-- GPU MONITOR -->
    <div class="gpu-panel">
      <div class="gpu-panel-header">
        <h3>GPU Pool — 3 devices</h3>
        <span class="action-link" style="font-size:0.75rem;">Details →</span>
      </div>
      <div class="gpu-list">
        <div class="gpu-item gpu-0">
          <div class="gpu-name">RTX 4090</div>
          <div class="gpu-bar-wrap">
            <div class="gpu-bar-fill" style="width:82%;background:var(--gpu-0);"></div>
          </div>
          <div class="gpu-stats">
            <span>82% / 68°C</span>
            <span>21.3 GB</span>
          </div>
        </div>
        <div class="gpu-item gpu-1">
          <div class="gpu-name">RTX 4090</div>
          <div class="gpu-bar-wrap">
            <div class="gpu-bar-fill" style="width:47%;background:var(--gpu-1);"></div>
          </div>
          <div class="gpu-stats">
            <span>47% / 52°C</span>
            <span>8.1 GB</span>
          </div>
        </div>
        <div class="gpu-item gpu-2">
          <div class="gpu-name">RTX 3090</div>
          <div class="gpu-bar-wrap">
            <div class="gpu-bar-fill" style="width:93%;background:var(--gpu-2);"></div>
          </div>
          <div class="gpu-stats">
            <span>93% / 74°C</span>
            <span>22.6 GB</span>
          </div>
        </div>
      </div>
    </div>
  </main>
  <!-- RIGHT PANEL -->
  <aside class="right-panel">
    <div>
      <div class="panel-section-title">Activity Feed</div>
      <div class="activity-feed">
        <div class="activity-item">
          <span class="activity-time">14:23</span>
          <span class="activity-dot success"></span>
          <span class="activity-text"><strong>PrecisionForge</strong> completed batch #46 — score 89.6</span>
        </div>
        <div class="activity-item">
          <span class="activity-time">14:18</span>
          <span class="activity-dot info"></span>
          <span class="activity-text"><strong>Hermes</strong> spawned delegate_task for blueprint audit</span>
        </div>
        <div class="activity-item">
          <span class="activity-time">14:12</span>
          <span class="activity-dot warn"></span>
          <span class="activity-text"><strong>GPU 2</strong> crossed 90°C threshold — throttling engaged</span>
        </div>
        <div class="activity-item">
          <span class="activity-time">14:04</span>
          <span class="activity-dot success"></span>
          <span class="activity-text"><strong>WebMockup</strong> delivered mockup v32 — score 94.1</span>
        </div>
        <div class="activity-item">
          <span class="activity-time">13:55</span>
          <span class="activity-dot err"></span>
          <span class="activity-text"><strong>Blueprint 12</strong> eval failed — config truncation error</span>
        </div>
        <div class="activity-item">
          <span class="activity-time">13:41</span>
          <span class="activity-dot info"></span>
          <span class="activity-text"><strong>System</strong> maxtruncationchars raised to 50000</span>
        </div>
      </div>
    </div>
    <div>
      <div class="panel-section-title">BP Priority Tiers</div>
      <div class="collapsible open">
        <div class="collapsible-trigger" onclick="toggleCollapse(this)">
          Generation / 0.5
          <span class="arrow">▶</span>
        </div>
        <div class="collapsible-content">
          <div style="font-size:0.75rem;color:var(--text-secondary);">
            Score threshold: 95<br>
            12 blueprints in queue<br>
            Priority: highest
          </div>
        </div>
      </div>
      <div style="height:0.4rem"></div>
      <div class="collapsible">
        <div class="collapsible-trigger" onclick="toggleCollapse(this)">
          Remaining (85+)
          <span class="arrow">▶</span>
        </div>
        <div class="collapsible-content">
          <div style="font-size:0.75rem;color:var(--text-secondary);">
            Score threshold: 85<br>
            34 blueprints in queue<br>
            Priority: normal
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="panel-section-title">Performance (last 12h)</div>
      <div class="mini-chart">
        <div class="mini-bar" style="height:12px;"></div>
        <div class="mini-bar" style="height:24px;"></div>
        <div class="mini-bar" style="height:18px;"></div>
        <div class="mini-bar" style="height:32px;"></div>
        <div class="mini-bar" style="height:28px;"></div>
        <div class="mini-bar" style="height:36px;"></div>
        <div class="mini-bar" style="height:22px;"></div>
        <div class="mini-bar" style="height:40px;"></div>
        <div class="mini-bar" style="height:34px;"></div>
        <div class="mini-bar" style="height:28px;"></div>
        <div class="mini-bar" style="height:38px;"></div>
        <div class="mini-bar" style="height:30px;"></div>
      </div>
      <div style="font-size:0.65rem;color:var(--text-muted);margin-top:0.3rem;display:flex;justify-content:space-between;">
        <span>06:00</span>
        <span>12:00</span>
        <span>now</span>
      </div>
    </div>
    <div>
      <div class="panel-section-title">Quick Actions</div>
      <button class="agent-action-btn" style="width:100%;padding:0.5rem;margin-bottom:0.35rem;" onclick="alert('Spawning new agent blueprint...')">+ New Agent BP</button>
      <button class="agent-action-btn" style="width:100%;padding:0.5rem;margin-bottom:0.35rem;" onclick="alert('Running full batch evaluation...')">Run Batch Eval</button>
      <button class="agent-action-btn" style="width:100%;padding:0.5rem;" onclick="alert('Clearing cache and restarting dashboard...')">Restart Dashboard</button>
    </div>
  </aside>
</div>
<footer class="site-footer">
  <span>Styde Forge v2.4 — Composite Score: 89.6 / 100</span>
  <div class="footer-links">
    <a href="#">Documentation</a>
    <a href="#">API</a>
    <a href="#">Status</a>
    <a href="#">styde.se</a>
  </div>
</footer>
<script>
function toggleCollapse(el) {
  var parent = el.parentElement;
  parent.classList.toggle('open');
}
function toggleMobileNav() {
  var sidebar = document.querySelector('.sidebar');
  if (sidebar) {
    var display = sidebar.style.display;
    sidebar.style.display = (display === 'flex' || display === '') ? 'none' : 'flex';
    if (sidebar.style.display === 'flex') {
      sidebar.style.position = 'fixed';
      sidebar.style.top = '60px';
      sidebar.style.left = '0';
      sidebar.style.width = '240px';
      sidebar.style.height = 'calc(100vh - 60px)';
      sidebar.style.zIndex = '200';
    } else {
      sidebar.style.position = '';
      sidebar.style.width = '';
      sidebar.style.height = '';
      sidebar.style.zIndex = '';
    }
  }
}
</script>
</body>
</html>