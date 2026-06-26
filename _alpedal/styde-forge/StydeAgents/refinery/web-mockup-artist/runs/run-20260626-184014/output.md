```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Control Surface</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg-deep: #0a0c10;
    --bg-panel: #111318;
    --bg-card: #161a22;
    --bg-glass: rgba(22,26,34,0.72);
    --border-subtle: #1e2430;
    --border-active: #3b82f6;
    --text-primary: #e8edf5;
    --text-secondary: #8a93a8;
    --text-muted: #525b6e;
    --accent-1: #3b82f6;
    --accent-2: #8b5cf6;
    --accent-3: #06b6d4;
    --accent-4: #f59e0b;
    --green: #22c55e;
    --red: #ef4444;
    --amber: #f59e0b;
    --radius: 10px;
    --radius-lg: 16px;
    --radius-sm: 6px;
    --shadow-card: 0 4px 24px rgba(0,0,0,0.4);
    --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
    --sidebar-w: 240px;
  }
  html { font-size: 15px; }
  body {
    font-family: var(--font);
    background: var(--bg-deep);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-image:
      radial-gradient(ellipse at 20% 50%, rgba(59,130,246,0.04) 0%, transparent 60%),
      radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.03) 0%, transparent 50%),
      radial-gradient(ellipse at 50% 80%, rgba(6,182,212,0.02) 0%, transparent 50%);
  }
  a { color: var(--accent-1); text-decoration: none; }
  a:hover { text-decoration: underline; }
  /* ---- scrollbar ---- */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #2a3142; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #3a4560; }
  /* ---- layout ---- */
  .app-shell {
    display: flex;
    min-height: 100vh;
  }
  .sidebar {
    width: var(--sidebar-w);
    background: var(--bg-panel);
    border-right: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 100;
    transition: transform 0.3s ease;
  }
  .sidebar-brand {
    padding: 20px 18px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid var(--border-subtle);
  }
  .sidebar-brand .logo {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    color: #fff;
    flex-shrink: 0;
  }
  .sidebar-brand span {
    font-weight: 600;
    font-size: 16px;
    letter-spacing: -0.3px;
  }
  .sidebar-brand small {
    color: var(--text-muted);
    font-size: 11px;
    display: block;
    margin-top: -2px;
  }
  .sidebar-nav {
    flex: 1;
    padding: 12px 10px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.15s ease;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    font-family: var(--font);
  }
  .nav-item:hover {
    background: rgba(255,255,255,0.04);
    color: var(--text-primary);
  }
  .nav-item.active {
    background: rgba(59,130,246,0.12);
    color: var(--accent-1);
    font-weight: 500;
  }
  .nav-item .icon {
    width: 20px;
    text-align: center;
    font-size: 15px;
    flex-shrink: 0;
  }
  .nav-item .badge {
    margin-left: auto;
    background: var(--red);
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    padding: 1px 7px;
    border-radius: 10px;
    line-height: 16px;
  }
  .nav-section-label {
    padding: 16px 14px 6px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
  }
  .sidebar-footer {
    padding: 14px 16px;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .sidebar-footer .avatar {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-2), var(--accent-3));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    color: #fff;
    flex-shrink: 0;
  }
  .sidebar-footer .user-info {
    font-size: 13px;
    line-height: 1.3;
  }
  .sidebar-footer .user-info small {
    color: var(--text-muted);
    font-size: 11px;
    display: block;
  }
  /* ---- main area ---- */
  .main-area {
    margin-left: var(--sidebar-w);
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .topbar {
    display: flex;
    align-items: center;
    padding: 14px 28px;
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-subtle);
    position: sticky;
    top: 0;
    z-index: 50;
    gap: 14px;
  }
  .topbar .breadcrumb {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--text-muted);
  }
  .topbar .breadcrumb a { color: var(--text-secondary); }
  .topbar .breadcrumb a:hover { color: var(--accent-1); }
  .topbar .breadcrumb .sep { color: var(--text-muted); font-size: 10px; }
  .topbar .breadcrumb .current { color: var(--text-primary); font-weight: 500; }
  .topbar-actions {
    margin-left: auto;
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .hamburger {
    display: none;
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 22px;
    cursor: pointer;
    padding: 4px;
  }
  /* ---- content ---- */
  .content {
    flex: 1;
    padding: 24px 28px 40px;
    max-width: 1400px;
  }
  .page-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .page-title .glow {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: pulse-dot 2s infinite;
  }
  @keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }
  .page-subtitle {
    color: var(--text-secondary);
    font-size: 14px;
    margin-bottom: 28px;
  }
  /* ---- metric cards row ---- */
  .metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
  }
  .metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius);
    padding: 18px 20px;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: var(--radius) var(--radius) 0 0;
  }
  .metric-card:nth-child(1)::before { background: var(--accent-1); }
  .metric-card:nth-child(2)::before { background: var(--accent-2); }
  .metric-card:nth-child(3)::before { background: var(--accent-3); }
  .metric-card:nth-child(4)::before { background: var(--accent-4); }
  .metric-card:hover {
    border-color: rgba(255,255,255,0.1);
    transform: translateY(-1px);
  }
  .metric-card .label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 6px;
  }
  .metric-card .value {
    font-size: 28px;
    font-weight: 700;
    line-height: 1.2;
  }
  .metric-card .change {
    font-size: 12px;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .metric-card .change.up { color: var(--green); }
  .metric-card .change.down { color: var(--red); }
  /* ---- panels grid ---- */
  .panels-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 24px;
  }
  .panel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    overflow: hidden;
  }
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-subtle);
    cursor: pointer;
    user-select: none;
  }
  .panel-header h3 {
    font-size: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .panel-header .toggle-icon {
    color: var(--text-muted);
    transition: transform 0.25s ease;
    font-size: 14px;
  }
  .panel.collapsed .toggle-icon {
    transform: rotate(-90deg);
  }
  .panel-body {
    max-height: 600px;
    overflow: hidden;
    transition: max-height 0.35s ease, padding 0.25s ease;
    padding: 16px 20px;
  }
  .panel.collapsed .panel-body {
    max-height: 0;
    padding: 0 20px;
  }
  /* ---- agent status ---- */
  .agent-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .agent-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: rgba(255,255,255,0.02);
    border-radius: var(--radius-sm);
    transition: background 0.15s;
  }
  .agent-row:hover { background: rgba(255,255,255,0.04); }
  .agent-row .status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .status-dot.online { background: var(--green); box-shadow: 0 0 6px var(--green); }
  .status-dot.busy { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
  .status-dot.offline { background: var(--text-muted); }
  .status-dot.error { background: var(--red); box-shadow: 0 0 6px var(--red); }
  .agent-row .name {
    font-size: 14px;
    font-weight: 500;
    flex: 1;
  }
  .agent-row .status-text {
    font-size: 12px;
    color: var(--text-secondary);
  }
  .agent-row .task-count {
    font-size: 11px;
    background: rgba(255,255,255,0.06);
    padding: 2px 10px;
    border-radius: 12px;
    color: var(--text-muted);
  }
  .agent-row .quick-action-btn {
    padding: 4px 12px;
    font-size: 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-subtle);
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    font-family: var(--font);
    transition: all 0.15s;
  }
  .agent-row .quick-action-btn:hover {
    border-color: var(--accent-1);
    color: var(--accent-1);
    background: rgba(59,130,246,0.06);
  }
  /* ---- GPU monitor ---- */
  .gpu-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .gpu-card {
    background: rgba(255,255,255,0.02);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
  }
  .gpu-card .gpu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .gpu-card .gpu-name {
    font-size: 13px;
    font-weight: 600;
  }
  .gpu-card .gpu-temp {
    font-size: 12px;
    color: var(--text-secondary);
  }
  .gpu-bar-track {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 4px;
  }
  .gpu-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease, background 0.5s ease;
    background: var(--accent-1);
  }
  .gpu-bar-fill.high { background: var(--accent-4); }
  .gpu-bar-fill.full { background: var(--red); }
  .gpu-card .gpu-stats {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
  }
  /* ---- activity feed ---- */
  .activity-feed {
    grid-column: 1 / -1;
  }
  .feed-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .feed-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
  }
  .feed-item:last-child { border-bottom: none; }
  .feed-icon {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .feed-content {
    flex: 1;
    font-size: 13px;
    line-height: 1.4;
  }
  .feed-content .feed-highlight {
    font-weight: 500;
    color: var(--text-primary);
  }
  .feed-time {
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
  }
  .feed-empty, .feed-loading, .feed-error {
    text-align: center;
    padding: 24px;
    color: var(--text-muted);
    font-size: 14px;
  }
  /* ---- loading / empty / error states ---- */
  .state-box {
    text-align: center;
    padding: 32px 20px;
    color: var(--text-muted);
  }
  .state-box .state-icon { font-size: 32px; margin-bottom: 10px; }
  .state-box .state-title { font-size: 15px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
  .state-box .state-desc { font-size: 13px; }
  .spinner {
    display: inline-block;
    width: 18px; height: 18px;
    border: 2px solid var(--border-subtle);
    border-top-color: var(--accent-1);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  /* ---- footer ---- */
  .footer {
    border-top: 1px solid var(--border-subtle);
    padding: 18px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--text-muted);
  }
  .footer-links { display: flex; gap: 18px; }
  .footer-links a { color: var(--text-muted); }
  .footer-links a:hover { color: var(--text-secondary); }
  /* ---- sidebar overlay on mobile ---- */
  .sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 90;
  }
  .sidebar-overlay.open { display: block; }
  /* ---- responsive ---- */
  @media (max-width: 1024px) {
    .metrics-row { grid-template-columns: repeat(2, 1fr); }
    .panels-grid { grid-template-columns: 1fr; }
    .gpu-grid { grid-template-columns: 1fr; }
  }
  @media (max-width: 768px) {
    .sidebar {
      transform: translateX(-100%);
    }
    .sidebar.open {
      transform: translateX(0);
    }
    .hamburger { display: block; }
    .main-area { margin-left: 0; }
    .topbar { padding: 12px 16px; }
    .content { padding: 16px; }
    .metrics-row { grid-template-columns: 1fr 1fr; gap: 10px; }
    .metric-card .value { font-size: 22px; }
    .footer { flex-direction: column; gap: 10px; text-align: center; }
  }
  @media (max-width: 480px) {
    .metrics-row { grid-template-columns: 1fr; }
    .topbar .breadcrumb { display: none; }
  }
</style>
</head>
<body>
<div class="app-shell">
  <aside class="sidebar" id="sidebar" role="navigation" aria-label="Main navigation">
    <div class="sidebar-brand">
      <div class="logo">SF</div>
      <div>
        <span>styde forge</span>
        <small>control surface</small>
      </div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section-label">primary</div>
      <button class="nav-item active" data-nav="dashboard">
        <span class="icon">~</span> Dashboard
      </button>
      <button class="nav-item" data-nav="agents">
        <span class="icon">@</span> Agents
        <span class="badge">3</span>
      </button>
      <button class="nav-item" data-nav="pipelines">
        <span class="icon">#</span> Pipelines
      </button>
      <button class="nav-item" data-nav="models">
        <span class="icon">*</span> Models
      </button>
      <div class="nav-section-label">monitoring</div>
      <button class="nav-item" data-nav="gpu">
        <span class="icon">+</span> GPU Cluster
      </button>
      <button class="nav-item" data-nav="logs">
        <span class="icon">!</span> Logs
      </button>
      <button class="nav-item" data-nav="alerts">
        <span class="icon">?</span> Alerts
      </button>
      <div class="nav-section-label">system</div>
      <button class="nav-item" data-nav="settings">
        <span class="icon">=</span> Settings
      </button>
      <button class="nav-item" data-nav="docs">
        <span class="icon">?</span> Docs
      </button>
    </nav>
    <div class="sidebar-footer">
      <div class="avatar">AP</div>
      <div class="user-info">
        alpedal <small>operator · online</small>
      </div>
    </div>
  </aside>
  <div class="sidebar-overlay" id="sidebarOverlay"></div>
  <div class="main-area">
    <header class="topbar">
      <button class="hamburger" id="hamburgerBtn" aria-label="Toggle menu">=</button>
      <div class="breadcrumb">
        <a href="#">styde</a>
        <span class="sep">/</span>
        <a href="#">forge</a>
        <span class="sep">/</span>
        <span class="current">dashboard</span>
      </div>
      <div class="topbar-actions">
        <button class="quick-action-btn" style="font-size:13px;padding:6px 14px;">+ new run</button>
        <button class="quick-action-btn" style="font-size:13px;padding:6px 14px;">refresh</button>
      </div>
    </header>
    <main class="content">
      <div class="page-title">
        <span>Dashboard</span>
        <span class="glow"></span>
      </div>
      <div class="page-subtitle">Forge control surface — agent status, GPU load, and recent activity at a glance.</div>
      <!-- metrics -->
      <div class="metrics-row" id="metricsRow">
        <div class="metric-card" data-metric="agents">
          <div class="label">active agents</div>
          <div class="value" id="metricAgents">--</div>
          <div class="change up" id="metricAgentsChange">+2 today</div>
        </div>
        <div class="metric-card" data-metric="gpu">
          <div class="label">gpu utilization</div>
          <div class="value" id="metricGpu">--%</div>
          <div class="change" id="metricGpuChange">averaged across cluster</div>
        </div>
        <div class="metric-card" data-metric="tasks">
          <div class="label">tasks completed</div>
          <div class="value" id="metricTasks">--</div>
          <div class="change up" id="metricTasksChange">+47 this hour</div>
        </div>
        <div class="metric-card" data-metric="queue">
          <div class="label">queue depth</div>
          <div class="value" id="metricQueue">--</div>
          <div class="change" id="metricQueueChange">0 stalled</div>
        </div>
      </div>
      <!-- panels -->
      <div class="panels-grid" id="panelsGrid">
        <!-- agent status panel -->
        <div class="panel" id="agentPanel">
          <div class="panel-header" data-toggle="agentPanel">
            <h3>@ agent status</h3>
            <span class="toggle-icon">v</span>
          </div>
          <div class="panel-body">
            <div id="agentListContainer">
              <div class="state-box" id="agentLoading">
                <div class="spinner" style="margin:0 auto 10px;"></div>
                <div class="state-title">loading agents...</div>
              </div>
              <div class="state-box" id="agentEmpty" style="display:none;">
                <div class="state-icon">-</div>
                <div class="state-title">no agents deployed</div>
                <div class="state-desc">spawn an agent from the pipeline view to get started.</div>
              </div>
              <div class="state-box" id="agentError" style="display:none;">
                <div class="state-icon">x</div>
                <div class="state-title">connection failed</div>
                <div class="state-desc">could not reach the agent orchestrator.</div>
              </div>
              <div class="agent-list" id="agentList" style="display:none;"></div>
            </div>
          </div>
        </div>
        <!-- gpu monitor panel -->
        <div class="panel" id="gpuPanel">
          <div class="panel-header" data-toggle="gpuPanel">
            <h3>+ gpu cluster</h3>
            <span class="toggle-icon">v</span>
          </div>
          <div class="panel-body">
            <div id="gpuContainer">
              <div class="state-box" id="gpuLoading" style="display:none;">
                <div class="spinner" style="margin:0 auto 10px;"></div>
                <div class="state-title">polling GPU metrics...</div>
              </div>
              <div class="state-box" id="gpuEmpty" style="display:none;">
                <div class="state-icon">-</div>
                <div class="state-title">no GPUs detected</div>
                <div class="state-desc">the cluster appears to be offline.</div>
              </div>
              <div class="state-box" id="gpuError" style="display:none;">
                <div class="state-icon">x</div>
                <div class="state-title">metrics unavailable</div>
                <div class="state-desc">nvidia-smi returned an error.</div>
              </div>
              <div class="gpu-grid" id="gpuGrid" style="display:none;"></div>
            </div>
          </div>
        </div>
        <!-- activity feed full-width -->
        <div class="panel activity-feed" id="feedPanel">
          <div class="panel-header" data-toggle="feedPanel">
            <h3>! activity feed</h3>
            <span class="toggle-icon">v</span>
          </div>
          <div class="panel-body">
            <div id="feedContainer">
              <div class="state-box" id="feedLoading">
                <div class="spinner" style="margin:0 auto 10px;"></div>
                <div class="state-title">loading activity...</div>
              </div>
              <div class="state-box" id="feedEmpty" style="display:none;">
                <div class="state-icon">-</div>
                <div class="state-title">no recent activity</div>
                <div class="state-desc">events will appear here as agents execute tasks.</div>
              </div>
              <div class="state-box" id="feedError" style="display:none;">
                <div class="state-icon">x</div>
                <div class="state-title">feed unavailable</div>
                <div class="state-desc">could not stream the event log.</div>
              </div>
              <div class="feed-list" id="feedList" style="display:none;"></div>
            </div>
          </div>
        </div>
      </div><!-- panels-grid -->
    </main>
    <footer class="footer">
      <span>styde forge v1.0 · control surface</span>
      <div class="footer-links">
        <a href="#">docs</a>
        <a href="#">status</a>
        <a href="#">api</a>
        <a href="#">github</a>
      </div>
    </footer>
  </div>
</div>
<script>
(function() {
  'use strict';
  // ---- centralized interval manager ----
  const IntervalManager = {
    _registry: new Map(),
    _visible: true,
    init: function() {
      const self = this;
      document.addEventListener('visibilitychange', function() {
        self._visible = !document.hidden;
        self._sync();
      });
      if (window.IntersectionObserver) {
        self._observer = new IntersectionObserver(function(entries) {
          entries.forEach(function(e) {
            if (e.target.dataset.intervalKey) {
              const entry = self._registry.get(e.target.dataset.intervalKey);
              if (entry) {
                entry._visible = e.isIntersecting;
                self._syncOne(entry);
              }
            }
          });
        }, { threshold: 0.1 });
      }
    },
    register: function(key, fn, ms, el) {
      if (this._registry.has(key)) this.unregister(key);
      const entry = {
        key: key,
        fn: fn,
        ms: ms,
        el: el,
        _id: null,
        _visible: true
      };
      this._registry.set(key, entry);
      if (el && this._observer) {
        el.dataset.intervalKey = key;
        this._observer.observe(el);
      }
      this._syncOne(entry);
      return entry;
    },
    unregister: function(key) {
      const entry = this._registry.get(key);
      if (!entry) return;
      if (entry._id) { clearInterval(entry._id); entry._id = null; }
      if (entry.el && this._observer && entry.el.dataset.intervalKey) {
        this._observer.unobserve(entry.el);
        delete entry.el.dataset.intervalKey;
      }
      this._registry.delete(key);
    },
    unregisterAll: function() {
      const self = this;
      this._registry.forEach(function(entry) {
        if (entry._id) { clearInterval(entry._id); entry._id = null; }
        if (entry.el && self._observer) {
          self._observer.unobserve(entry.el);
          delete entry.el.dataset.intervalKey;
        }
      });
      this._registry.clear();
    },
    _sync: function() {
      const self = this;
      this._registry.forEach(function(entry) { self._syncOne(entry); });
    },
    _syncOne: function(entry) {
      const shouldRun = this._visible && entry._visible;
      if (shouldRun && !entry._id) {
        entry.fn();
        entry._id = setInterval(entry.fn, entry.ms);
      } else if (!shouldRun && entry._id) {
        clearInterval(entry._id);
        entry._id = null;
      }
    }
  };
  IntervalManager.init();
  // ---- helpers ----
  function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  // ---- simulated data ----
  const AGENTS = [
    { name: 'orchestrator-alpha', status: 'online', tasks: 4 },
    { name: 'refinery-beta', status: 'busy', tasks: 12 },
    { name: 'production-gamma', status: 'online', tasks: 0 },
    { name: 'evaluator-delta', status: 'error', tasks: 1 },
    { name: 'codex-epsilon', status: 'offline', tasks: 0 }
  ];
  const GPU_NAMES = ['A100-01', 'A100-02', 'A100-03', 'A100-04', 'H100-01', 'H100-02'];
  var feedIdx = 0;
  function makeFeedItem() {
    feedIdx++;
    const actions = [
      'completed blueprint evaluation for batch #' + feedIdx,
      'pushed model weights to production registry',
      'agent orchestrator-alpha spawned delegate sub-task',
      'GPU A100-03 temp exceeded 82C threshold',
      'pipeline forge-verify passed all 47 checks',
      'agent codex-epsilon went offline unexpectedly',
      'refinery-beta consolidated 6 planning iterations',
      'new BLUEPRINT.md registered from webhook',
      'cache flush completed for workspace forge-prime',
      'model validation produced 0.3% regression alert'
    ];
    var icons = ['~', '@', '#', '+', '!', '?', '*', '=', '~', '@'];
    return {
      icon: icons[feedIdx % icons.length],
      text: actions[feedIdx % actions.length],
      time: feedIdx + 'm ago'
    };
  }
  // ---- init mock data and start intervals ----
  function initAgentList() {
    var container = document.getElementById('agentList');
    var loading = document.getElementById('agentLoading');
    var empty = document.getElementById('agentEmpty');
    var error = document.getElementById('agentError');
    loading.style.display = 'block';
    container.style.display = 'none';
    empty.style.display = 'none';
    error.style.display = 'none';
    setTimeout(function() {
      loading.style.display = 'none';
      container.style.display = '';
      container.innerHTML = '';
      AGENTS.forEach(function(a) {
        var row = document.createElement('div');
        row.className = 'agent-row';
        var statusMap = { online: 'online', busy: 'busy', offline: 'offline', error: 'error' };
        row.innerHTML =
          '<span class="status-dot ' + statusMap[a.status] + '"></span>' +
          '<span class="name">' + a.name + '</span>' +
          '<span class="status-text">' + a.status + '</span>' +
          '<span class="task-count">' + a.tasks + ' tasks</span>' +
          '<button class="quick-action-btn">dispatch</button>';
        container.appendChild(row);
      });
      updateMetricAgents();
    }, 600);
  }
  function updateMetricAgents() {
    var active = AGENTS.filter(function(a) { return a.status === 'online' || a.status === 'busy'; }).length;
    document.getElementById('metricAgents').textContent = active + '/' + AGENTS.length;
  }
  function initGpuGrid() {
    var grid = document.getElementById('gpuGrid');
    var loading = document.getElementById('gpuLoading');
    var empty = document.getElementById('gpuEmpty');
    var error = document.getElementById('gpuError');
    loading.style.display = 'block';
    grid.style.display = 'none';
    empty.style.display = 'none';
    error.style.display = 'none';
    setTimeout(function() {
      loading.style.display = 'none';
      grid.style.display = '';
      grid.innerHTML = '';
      GPU_NAMES.forEach(function(name, i) {
        var card = document.createElement('div');
        card.className = 'gpu-card';
        card.id = 'gpuCard-' + i;
        var pct = rand(20, 95);
        var temp = rand(42, 84);
        var mem = rand(30, 90);
        var barClass = pct > 85 ? 'full' : (pct > 65 ? 'high' : '');
        card.innerHTML =
          '<div class="gpu-header">' +
            '<span class="gpu-name">' + name + '</span>' +
            '<span class="gpu-temp">' + temp + 'C</span>' +
          '</div>' +
          '<div class="gpu-bar-track"><div class="gpu-bar-fill ' + barClass + '" style="width:' + pct + '%;"></div></div>' +
          '<div class="gpu-stats"><span>' + pct + '% util</span><span>' + mem + '% mem</span></div>';
        grid.appendChild(card);
      });
      updateMetricGpu();
    }, 800);
  }
  // staggered GPU updates — each GPU has its own timer
  function startGpuTimers() {
    GPU_NAMES.forEach(function(name, i) {
      var card = document.getElementById('gpuCard-' + i);
      if (!card) return;
      // stagger: each GPU gets a random interval between 1800-3500ms
      var intervalMs = rand(1800, 3500);
      IntervalManager.register('gpu-' + i, function() {
        var cardEl = document.getElementById('gpuCard-' + i);
        if (!cardEl) return;
        var newPct = rand(15, 98);
        var newTemp = rand(40, 86);
        var newMem = rand(20, 95);
        var barClass = newPct > 85 ? 'full' : (newPct > 65 ? 'high' : '');
        var bar = cardEl.querySelector('.gpu-bar-fill');
        if (bar) {
          bar.style.width = newPct + '%';
          bar.className = 'gpu-bar-fill ' + barClass;
        }
        var stats = cardEl.querySelectorAll('.gpu-stats span');
        if (stats.length >= 2) {
          stats[0].textContent = newPct + '% util';
          stats[1].textContent = newMem + '% mem';
        }
        var tempEl = cardEl.querySelector('.gpu-temp');
        if (tempEl) tempEl.textContent = newTemp + 'C';
        updateMetricGpu();
      }, intervalMs, card);
    });
  }
  function updateMetricGpu() {
    var bars = document.querySelectorAll('#gpuGrid .gpu-bar-fill');
    var total = 0, count = 0;
    bars.forEach(function(b) {
      var w = parseFloat(b.style.width);
      if (!isNaN(w)) { total += w; count++; }
    });
    var avg = count > 0 ? Math.round(total / count) : 0;
    document.getElementById('metricGpu').textContent = avg + '%';
    document.getElementById('metricGpuChange').textContent = count + ' GPUs reporting';
  }
  // ---- activity feed ----
  function initFeed() {
    var list = document.getElementById('feedList');
    var loading = document.getElementById('feedLoading');
    var empty = document.getElementById('feedEmpty');
    var error = document.getElementById('feedError');
    loading.style.display = 'block';
    list.style.display = 'none';
    empty.style.display = 'none';
    error.style.display = 'none';
    setTimeout(function() {
      loading.style.display = 'none';
      list.style.display = '';
      list.innerHTML = '';
      // seed 8 items
      for (var i = 0; i < 8; i++) {
        var item = makeFeedItem();
        var div = document.createElement('div');
        div.className = 'feed-item';
        div.innerHTML =
          '<div class="feed-icon">' + item.icon + '</div>' +
          '<div class="feed-content"><span class="feed-highlight">' + item.text + '</span></div>' +
          '<div class="feed-time">' + item.time + '</div>';
        list.appendChild(div);
      }
      startFeedTimer();
    }, 500);
  }
  function startFeedTimer() {
    IntervalManager.register('feed-timer', function() {
      var list = document.getElementById('feedList');
      if (!list) return;
      var item = makeFeedItem();
      var div = document.createElement('div');
      div.className = 'feed-item';
      div.innerHTML =
        '<div class="feed-icon">' + item.icon + '</div>' +
        '<div class="feed-content"><span class="feed-highlight">' + item.text + '</span></div>' +
        '<div class="feed-time">' + item.time + '</div>';
      list.insertBefore(div, list.firstChild);
      // keep 30 max
      while (list.children.length > 30) {
        list.removeChild(list.lastChild);
      }
      // update task metric
      var cur = parseInt(document.getElementById('metricTasks').textContent, 10) || 142;
      document.getElementById('metricTasks').textContent = cur + 1;
    }, 6000, document.getElementById('feedPanel'));
  }
  // ---- queue metric ----
  function initQueueMetric() {
    document.getElementById('metricQueue').textContent = '12';
    IntervalManager.register('queue-metric', function() {
      var q = rand(3, 28);
      document.getElementById('metricQueue').textContent = q;
      var stalled = q > 20 ? 2 : 0;
      document.getElementById('metricQueueChange').textContent = stalled + ' stalled';
    }, 4500, document.getElementById('metricsRow'));
  }
  // ---- collapsible panels ----
  function initCollapsible() {
    document.querySelectorAll('[data-toggle]').forEach(function(header) {
      header.addEventListener('click', function() {
        var panelId = header.dataset.toggle;
        var panel = document.getElementById(panelId);
        if (!panel) return;
        var isCollapsed = panel.classList.toggle('collapsed');
        // pause/resume GPU timers in GPU panel
        if (panelId === 'gpuPanel') {
          GPU_NAMES.forEach(function(name, i) {
            var entry = IntervalManager._registry.get('gpu-' + i);
            if (entry) {
              entry._visible = !isCollapsed;
              IntervalManager._syncOne(entry);
            }
          });
        }
        // pause/resume feed timer
        if (panelId === 'feedPanel') {
          var feedEntry = IntervalManager._registry.get('feed-timer');
          if (feedEntry) {
            feedEntry._visible = !isCollapsed;
            IntervalManager._syncOne(feedEntry);
          }
        }
      });
    });
  }
  // ---- sidebar toggle ----
  function initSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    var btn = document.getElementById('hamburgerBtn');
    function openSidebar() { sidebar.classList.add('open'); overlay.classList.add('open'); }
    function closeSidebar() { sidebar.classList.remove('open'); overlay.classList.remove('open'); }
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      if (sidebar.classList.contains('open')) { closeSidebar(); }
      else { openSidebar(); }
    });
    overlay.addEventListener('click', closeSidebar);
    // close on nav click (mobile)
    sidebar.querySelectorAll('.nav-item').forEach(function(item) {
      item.addEventListener('click', function() {
        sidebar.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
        item.classList.add('active');
        if (window.innerWidth <= 768) closeSidebar();
      });
    });
    // handle resize
    window.addEventListener('resize', function() {
      if (window.innerWidth > 768) closeSidebar();
    });
  }
  // ---- bootstrap ----
  document.addEventListener('DOMContentLoaded', function() {
    initCollapsible();
    initSidebar();
    initAgentList();
    initGpuGrid();
    startGpuTimers();
    initFeed();
    initQueueMetric();
  });
  // ---- cleanup on page unload ----
  window.addEventListener('beforeunload', function() {
    IntervalManager.unregisterAll();
  });
})();
</script>
</body>
</html>
```