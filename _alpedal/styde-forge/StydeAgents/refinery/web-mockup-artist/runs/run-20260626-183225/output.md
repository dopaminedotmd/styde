```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Control Panel</title>
<style>
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
:root {
  --bg: #f4f2ed;
  --surface: #ffffff;
  --sidebar: #1a1c1e;
  --sidebar-text: #b0b3b8;
  --sidebar-active: #e8d5b7;
  --accent: #c89b5e;
  --accent2: #7a9a6d;
  --accent3: #b06d6d;
  --text: #2c2a28;
  --text2: #6b6760;
  --border: #dedbd4;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 10px;
  --transition: 0.28s ease;
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
html {
  font-size: 15px;
}
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
}
a {
  color: var(--accent);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
/* sidebar */
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--sidebar);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: transform var(--transition);
}
.sidebar-brand {
  padding: 24px 20px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.sidebar-brand h1 {
  color: #e8d5b7;
  font-size: 1.3rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}
.sidebar-brand span {
  display: block;
  color: var(--sidebar-text);
  font-size: 0.72rem;
  margin-top: 2px;
  opacity: 0.6;
}
.sidebar-nav {
  padding: 12px 0;
  flex: 1;
}
.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  color: var(--sidebar-text);
  font-size: 0.85rem;
  transition: all var(--transition);
  border-left: 3px solid transparent;
}
.sidebar-nav a:hover {
  color: #ddd;
  background: rgba(255,255,255,0.04);
  text-decoration: none;
}
.sidebar-nav a.active {
  color: var(--sidebar-active);
  border-left-color: var(--accent);
  background: rgba(200,155,94,0.08);
}
.sidebar-nav .nav-icon {
  width: 18px;
  text-align: center;
  font-size: 0.9rem;
  opacity: 0.7;
}
.sidebar-footer {
  padding: 14px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 0.72rem;
  color: var(--sidebar-text);
  opacity: 0.5;
}
/* main */
.main {
  margin-left: 240px;
  flex: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
/* top bar */
.topbar {
  display: flex;
  align-items: center;
  padding: 14px 28px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  gap: 16px;
  position: sticky;
  top: 0;
  z-index: 50;
}
.hamburger {
  display: none;
  background: none;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  color: var(--text);
  padding: 4px;
}
.hamburger:hover {
  color: var(--accent);
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--text2);
}
.breadcrumb span {
  opacity: 0.5;
}
.breadcrumb a {
  color: var(--text2);
}
.breadcrumb a:hover {
  color: var(--accent);
}
.topbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 14px;
}
.topbar-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: var(--accent2);
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent2);
  display: inline-block;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.topbar-btn {
  background: none;
  border: 1px solid var(--border);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.78rem;
  cursor: pointer;
  color: var(--text2);
  transition: all var(--transition);
}
.topbar-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}
/* page content */
.page {
  padding: 28px;
  flex: 1;
}
.page-header {
  margin-bottom: 24px;
}
.page-header h2 {
  font-size: 1.4rem;
  font-weight: 500;
  color: var(--text);
}
.page-header p {
  color: var(--text2);
  font-size: 0.85rem;
  margin-top: 4px;
}
/* metric grid */
.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 28px;
}
.metric-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
}
.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0,0,0,0.08);
}
.metric-card .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--text2);
  margin-bottom: 6px;
}
.metric-card .value {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text);
}
.metric-card .sub {
  font-size: 0.78rem;
  color: var(--text2);
  margin-top: 2px;
}
.metric-card.trend-up .value {
  color: var(--accent2);
}
.metric-card.trend-down .value {
  color: var(--accent3);
}
.metric-card .quick-action-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--bg);
  border: none;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.7rem;
  opacity: 0;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text2);
}
.metric-card:hover .quick-action-btn {
  opacity: 1;
}
.quick-action-btn:hover {
  background: var(--accent);
  color: #fff;
}
/* two column */
.cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 28px;
}
@media (max-width: 820px) {
  .cols {
    grid-template-columns: 1fr;
  }
}
/* panel */
.panel {
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  overflow: hidden;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  cursor: pointer;
  user-select: none;
  transition: background var(--transition);
}
.panel-header:hover {
  background: #faf9f6;
}
.panel-header h3 {
  font-size: 0.9rem;
  font-weight: 500;
}
.panel-toggle {
  font-size: 0.7rem;
  transition: transform var(--transition);
  color: var(--text2);
}
.panel.collapsed .panel-toggle {
  transform: rotate(-90deg);
}
/* collapsible body */
.panel-body-wrap {
  max-height: 600px;
  overflow: hidden;
  transition: max-height 0.35s ease;
}
.panel.collapsed .panel-body-wrap {
  max-height: 0;
}
.panel-body {
  padding: 0 18px 16px;
}
/* agent list */
.agent-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.agent-item:last-child {
  border-bottom: none;
}
.agent-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
  color: #fff;
  flex-shrink: 0;
}
.agent-info {
  flex: 1;
  min-width: 0;
}
.agent-info .name {
  font-size: 0.82rem;
  font-weight: 500;
}
.agent-info .role {
  font-size: 0.72rem;
  color: var(--text2);
}
.agent-status {
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 20px;
  font-weight: 500;
  flex-shrink: 0;
}
.status-idle {
  background: #e8e4dc;
  color: #6b6760;
}
.status-active {
  background: #d8e6d2;
  color: #4a7a3f;
}
.status-busy {
  background: #e8d2d2;
  color: #8a4040;
}
/* activity feed */
.feed-item {
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.82rem;
  line-height: 1.4;
}
.feed-item:last-child {
  border-bottom: none;
}
.feed-item .time {
  font-size: 0.7rem;
  color: var(--text2);
  margin-top: 2px;
}
.feed-item .highlight {
  color: var(--accent);
}
/* GPU monitor */
.gpu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
}
.gpu-card {
  background: var(--bg);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  border: 1px solid var(--border);
  transition: all var(--transition);
  opacity: 0;
  animation: fadeUp 0.4s ease forwards;
}
.gpu-card:nth-child(1) { animation-delay: 0.02s; }
.gpu-card:nth-child(2) { animation-delay: 0.12s; }
.gpu-card:nth-child(3) { animation-delay: 0.22s; }
.gpu-card:nth-child(4) { animation-delay: 0.32s; }
.gpu-card:hover {
  border-color: var(--accent);
  transform: translateY(-1px);
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.gpu-card .gpu-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text2);
}
.gpu-card .gpu-temp {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 4px 0;
}
.gpu-card .gpu-load {
  font-size: 0.78rem;
}
.gpu-load-bar {
  height: 4px;
  background: #e0ddd6;
  border-radius: 4px;
  margin-top: 6px;
  overflow: hidden;
}
.gpu-load-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}
.gpu-card.loading .gpu-temp,
.gpu-card.loading .gpu-load {
  background: linear-gradient(90deg, #e0ddd6 25%, #f0ede8 50%, #e0ddd6 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  color: transparent;
  border-radius: 4px;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
/* footer */
.footer {
  border-top: 1px solid var(--border);
  padding: 16px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text2);
  background: var(--surface);
  flex-wrap: wrap;
  gap: 8px;
}
.footer-links {
  display: flex;
  gap: 16px;
}
.footer-links a {
  color: var(--text2);
}
.footer-links a:hover {
  color: var(--accent);
}
/* sidebar overlay on mobile */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 90;
}
/* empty state */
.empty-state {
  text-align: center;
  padding: 28px 12px;
  color: var(--text2);
}
.empty-state .icon {
  font-size: 2rem;
  margin-bottom: 8px;
  opacity: 0.3;
}
.empty-state p {
  font-size: 0.85rem;
}
/* error state */
.error-state {
  text-align: center;
  padding: 28px 12px;
  color: var(--accent3);
}
.error-state .icon {
  font-size: 2rem;
  margin-bottom: 8px;
}
.error-state p {
  font-size: 0.85rem;
}
/* loading state */
.loading-state {
  text-align: center;
  padding: 28px 12px;
  color: var(--text2);
}
.loading-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 10px;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
/* responsive */
@media (max-width: 720px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.open {
    transform: translateX(0);
  }
  .sidebar-overlay.active {
    display: block;
  }
  .main {
    margin-left: 0;
  }
  .hamburger {
    display: block;
  }
  .topbar {
    padding: 10px 16px;
  }
  .page {
    padding: 16px;
  }
  .metrics {
    grid-template-columns: 1fr 1fr;
  }
  .gpu-grid {
    grid-template-columns: 1fr 1fr;
  }
  .footer {
    flex-direction: column;
    text-align: center;
  }
}
@media (max-width: 440px) {
  .metrics {
    grid-template-columns: 1fr;
  }
  .topbar-right .topbar-btn span {
    display: none;
  }
}
</style>
</head>
<body>
<!-- sidebar -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-brand">
    <h1>styde forge</h1>
    <span>agent control panel</span>
  </div>
  <nav class="sidebar-nav">
    <a href="#" class="active"><span class="nav-icon">&#9707;</span> Overview</a>
    <a href="#"><span class="nav-icon">&#9679;</span> Agents</a>
    <a href="#"><span class="nav-icon">&#9650;</span> Batch Training</a>
    <a href="#"><span class="nav-icon">&#9724;</span> Blueprints</a>
    <a href="#"><span class="nav-icon">&#9673;</span> GPU Cluster</a>
    <a href="#"><span class="nav-icon">&#9881;</span> Settings</a>
  </nav>
  <div class="sidebar-footer">
    styde.se &middot; v2.6.1
  </div>
</aside>
<!-- overlay for mobile -->
<div class="sidebar-overlay" id="overlay"></div>
<!-- main -->
<div class="main">
  <!-- top bar -->
  <header class="topbar">
    <button class="hamburger" id="hamburger" aria-label="Toggle menu">&#9776;</button>
    <div class="breadcrumb">
      <a href="#">styde.se</a> <span>/</span>
      <a href="#">forge</a> <span>/</span>
      <span>overview</span>
    </div>
    <div class="topbar-right">
      <div class="topbar-status">
        <span class="status-dot"></span>
        <span>All systems nominal</span>
      </div>
      <button class="topbar-btn"><span>&#9654;</span> <span>New Batch</span></button>
      <button class="topbar-btn"><span>&#9998;</span> <span>Edit</span></button>
    </div>
  </header>
  <!-- page content -->
  <div class="page">
    <div class="page-header">
      <h2>Forge Overview</h2>
      <p>Real-time status of the agent training pipeline and cluster resources</p>
    </div>
    <!-- metrics -->
    <div class="metrics">
      <div class="metric-card trend-up">
        <button class="quick-action-btn" title="Refresh">&#8635;</button>
        <div class="label">Active Agents</div>
        <div class="value">12</div>
        <div class="sub">&#9650; +3 since yesterday</div>
      </div>
      <div class="metric-card trend-up">
        <button class="quick-action-btn" title="Refresh">&#8635;</button>
        <div class="label">Batch Throughput</div>
        <div class="value">94</div>
        <div class="sub">blueprints / hr &middot; &#9650; 8%</div>
      </div>
      <div class="metric-card trend-down">
        <button class="quick-action-btn" title="Refresh">&#8635;</button>
        <div class="label">Avg Latency</div>
        <div class="value">2.4s</div>
        <div class="sub">&#9660; 0.3s from peak</div>
      </div>
      <div class="metric-card">
        <button class="quick-action-btn" title="Refresh">&#8635;</button>
        <div class="label">Cluster Load</div>
        <div class="value">67%</div>
        <div class="sub">8 of 12 GPUs active</div>
      </div>
    </div>
    <!-- columns -->
    <div class="cols">
      <!-- left: agents -->
      <div class="panel" id="panel-agents">
        <div class="panel-header" data-toggle="panel-agents">
          <h3>&#9679; Agent Fleet</h3>
          <span class="panel-toggle">&#9660;</span>
        </div>
        <div class="panel-body-wrap">
          <div class="panel-body" id="agent-list">
            <div class="loading-state" id="agents-loading">
              <div class="loading-spinner"></div>
              <p>Loading agents...</p>
            </div>
            <div class="error-state" id="agents-error" style="display:none;">
              <div class="icon">&#9888;</div>
              <p>Failed to load agent data. <a href="#" id="retry-agents">Retry</a></p>
            </div>
            <div class="empty-state" id="agents-empty" style="display:none;">
              <div class="icon">&#9632;</div>
              <p>No agents deployed yet. Start a batch to create one.</p>
            </div>
            <div id="agents-content" style="display:none;"></div>
          </div>
        </div>
      </div>
      <!-- right: activity -->
      <div class="panel" id="panel-activity">
        <div class="panel-header" data-toggle="panel-activity">
          <h3>&#9776; Activity Feed</h3>
          <span class="panel-toggle">&#9660;</span>
        </div>
        <div class="panel-body-wrap">
          <div class="panel-body" id="activity-feed">
            <div class="loading-state" id="feed-loading">
              <div class="loading-spinner"></div>
              <p>Loading activity...</p>
            </div>
            <div class="error-state" id="feed-error" style="display:none;">
              <div class="icon">&#9888;</div>
              <p>Feed unavailable. <a href="#" id="retry-feed">Retry</a></p>
            </div>
            <div class="empty-state" id="feed-empty" style="display:none;">
              <div class="icon">&#9776;</div>
              <p>No recent activity to show.</p>
            </div>
            <div id="feed-content" style="display:none;"></div>
          </div>
        </div>
      </div>
    </div>
    <!-- GPU monitor -->
    <div class="panel" id="panel-gpu" style="margin-bottom:28px;">
      <div class="panel-header" data-toggle="panel-gpu">
        <h3>&#9673; GPU Cluster Monitor</h3>
        <span class="panel-toggle">&#9660;</span>
      </div>
      <div class="panel-body-wrap">
        <div class="panel-body">
          <div class="loading-state" id="gpu-loading">
            <div class="loading-spinner"></div>
            <p>Polling GPU metrics...</p>
          </div>
          <div class="error-state" id="gpu-error" style="display:none;">
            <div class="icon">&#9888;</div>
            <p>GPU cluster unreachable. <a href="#" id="retry-gpu">Retry</a></p>
          </div>
          <div class="empty-state" id="gpu-empty" style="display:none;">
            <div class="icon">&#9673;</div>
            <p>No GPUs registered in the cluster.</p>
          </div>
          <div class="gpu-grid" id="gpu-grid" style="display:none;"></div>
        </div>
      </div>
    </div>
  </div>
  <!-- footer -->
  <footer class="footer">
    <span>&copy; 2026 styde.se &mdash; Forge Control Panel</span>
    <div class="footer-links">
      <a href="#">Documentation</a>
      <a href="#">API</a>
      <a href="#">Status</a>
      <a href="#">Support</a>
    </div>
  </footer>
</div>
<script>
(function() {
  'use strict';
  document.addEventListener('DOMContentLoaded', function() {
    /* ---- hamburger ---- */
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');
    var hamburger = document.getElementById('hamburger');
    function toggleSidebar() {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('active');
    }
    hamburger.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
    /* ---- collapsible panels ---- */
    var toggles = document.querySelectorAll('[data-toggle]');
    toggles.forEach(function(el) {
      el.addEventListener('click', function() {
        var panel = el.closest('.panel');
        if (panel) {
          panel.classList.toggle('collapsed');
        }
      });
    });
    /* ---- staggered GPU updates ---- */
    var GPU_COLORS = ['var(--accent2)', 'var(--accent)', 'var(--accent3)', '#8a7ab0', '#b08a6d', '#6d8ab0'];
    function renderGPUs(container, gpus) {
      container.innerHTML = '';
      gpus.forEach(function(gpu, i) {
        var card = document.createElement('div');
        card.className = 'gpu-card';
        card.innerHTML =
          '<div class="gpu-label">' + gpu.name + '</div>' +
          '<div class="gpu-temp">' + gpu.temp + '&deg;C</div>' +
          '<div class="gpu-load">' + gpu.load + '% load</div>' +
          '<div class="gpu-load-bar"><div class="gpu-load-fill" style="width:' + gpu.load + '%;background:' + GPU_COLORS[i % GPU_COLORS.length] + '"></div></div>';
        container.appendChild(card);
        /* staggered timer per GPU */
        var interval = 3000 + (i * 400);
        setTimeout(function() {
          var timer = setInterval(function() {
            var newLoad = Math.floor(Math.random() * 40) + 20;
            var fill = card.querySelector('.gpu-load-fill');
            var loadEl = card.querySelector('.gpu-load');
            var tempEl = card.querySelector('.gpu-temp');
            if (fill && loadEl && tempEl) {
              fill.style.width = newLoad + '%';
              loadEl.textContent = newLoad + '% load';
              tempEl.textContent = (Math.floor(Math.random() * 20) + 55) + '\u00B0C';
            }
          }, 4000);
          /* store timer on card for cleanup */
          card._timer = timer;
        }, 200 + (i * 180));
      });
    }
    /* ---- agent data (mocked) ---- */
    var agentsData = [
      { name: 'Hermes', role: 'Orchestrator', status: 'active', color: '#c89b5e' },
      { name: 'PrecisionForge', role: 'Production pipeline', status: 'busy', color: '#b06d6d' },
      { name: 'PromptSmith', role: 'Prompt engineering', status: 'idle', color: '#7a9a6d' },
      { name: 'BatchMaster', role: 'Batch training', status: 'active', color: '#8a7ab0' },
      { name: 'Mockup Artist', role: 'Frontend prototype', status: 'idle', color: '#b08a6d' }
    ];
    var activityData = [
      { text: 'Batch <span class="highlight">#142</span> completed — 46 blueprints processed', time: '2 min ago' },
      { text: 'Agent <span class="highlight">PrecisionForge</span> started iteration loop v8.2', time: '7 min ago' },
      { text: 'GPU <span class="highlight">A100-03</span> temperature spike to 82\u00B0C — throttled', time: '14 min ago' },
      { text: 'Blueprint <span class="highlight">web-mockup-v12</span> promoted to production', time: '22 min ago' },
      { text: 'Memory pool expanded to <span class="highlight">1GB</span> per subagent', time: '36 min ago' }
    ];
    var gpuData = [
      { name: 'A100-01', temp: 68, load: 72 },
      { name: 'A100-02', temp: 71, load: 88 },
      { name: 'A100-03', temp: 79, load: 94 },
      { name: 'RTX6090', temp: 62, load: 45 }
    ];
    function showState(containerId, state) {
      ['loading','error','empty','content'].forEach(function(s) {
        var el = document.getElementById(containerId + '-' + s);
        if (el) el.style.display = (s === state) ? '' : 'none';
      });
    }
    function populateAgents() {
      showState('agents', 'loading');
      setTimeout(function() {
        var ok = true; /* simulate success */
        if (!ok) {
          showState('agents', 'error');
          return;
        }
        var cont = document.getElementById('agents-content');
        if (!cont) return;
        if (agentsData.length === 0) {
          showState('agents', 'empty');
          return;
        }
        cont.innerHTML = agentsData.map(function(a) {
          var cls = 'status-' + a.status;
          return '<div class="agent-item">' +
            '<div class="agent-avatar" style="background:' + a.color + '">' + a.name.charAt(0) + '</div>' +
            '<div class="agent-info"><div class="name">' + a.name + '</div><div class="role">' + a.role + '</div></div>' +
            '<div class="agent-status ' + cls + '">' + a.status + '</div>' +
            '</div>';
        }).join('');
        showState('agents', 'content');
      }, 300);
    }
    function populateFeed() {
      showState('feed', 'loading');
      setTimeout(function() {
        var ok = true;
        if (!ok) {
          showState('feed', 'error');
          return;
        }
        var cont = document.getElementById('feed-content');
        if (!cont) return;
        if (activityData.length === 0) {
          showState('feed', 'empty');
          return;
        }
        cont.innerHTML = activityData.map(function(a) {
          return '<div class="feed-item">' + a.text + '<div class="time">' + a.time + '</div></div>';
        }).join('');
        showState('feed', 'content');
      }, 400);
    }
    function populateGPUs() {
      showState('gpu', 'loading');
      setTimeout(function() {
        var ok = true;
        if (!ok) {
          showState('gpu', 'error');
          return;
        }
        var grid = document.getElementById('gpu-grid');
        if (!grid) return;
        if (gpuData.length === 0) {
          showState('gpu', 'empty');
          return;
        }
        renderGPUs(grid, gpuData);
        showState('gpu', 'content');
      }, 250);
    }
    populateAgents();
    populateFeed();
    populateGPUs();
    /* retry handlers */
    document.getElementById('retry-agents').addEventListener('click', function(e) {
      e.preventDefault();
      populateAgents();
    });
    document.getElementById('retry-feed').addEventListener('click', function(e) {
      e.preventDefault();
      populateFeed();
    });
    document.getElementById('retry-gpu').addEventListener('click', function(e) {
      e.preventDefault();
      populateGPUs();
    });
    /* quick action buttons */
    var quickBtns = document.querySelectorAll('.quick-action-btn');
    quickBtns.forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        var card = btn.closest('.metric-card');
        if (card) {
          card.style.opacity = '0.6';
          setTimeout(function() {
            card.style.opacity = '1';
          }, 350);
        }
      });
    });
  });
})();
</script>
</body>
</html>
```