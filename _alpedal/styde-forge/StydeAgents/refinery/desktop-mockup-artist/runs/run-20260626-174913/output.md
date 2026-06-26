<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge Control Center</title>
<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
@font-face {
  font-family: 'Segoe UI Variable';
  src: local('Segoe UI Variable Display'), local('Segoe UI'), local('Segoe UI Variable');
}
@font-face {
  font-family: 'Segoe Fluent Icons';
  src: local('Segoe Fluent Icons'), local('Segoe MDL2 Assets');
}
:root {
  --bg-surface: #1f1f1f;
  --bg-surface-alt: #252525;
  --bg-surface-raised: #2d2d2d;
  --bg-surface-card: #262626;
  --bg-accent: #60cdff;
  --bg-accent-dim: #3a3d4a;
  --text-primary: #f0f0f0;
  --text-secondary: #a0a0a0;
  --text-tertiary: #727272;
  --border-subtle: #3a3a3a;
  --border-raised: #484848;
  --shadow-window: 0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04);
  --shadow-card: 0 2px 8px rgba(0,0,0,0.3);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --font-ui: 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
  --titlebar-h: 32px;
}
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: var(--font-ui);
  background: #111;
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}
/* --- DESKTOP BACKGROUND --- */
.desktop {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at 30% 20%, #1a1f2e 0%, #0c0d14 70%);
  position: relative;
}
/* --- WINDOW --- */
.window {
  width: 1200px;
  height: 780px;
  background: var(--bg-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-window);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}
/* --- TITLEBAR --- */
.titlebar {
  height: var(--titlebar-h);
  background: #1a1a1a;
  display: flex;
  align-items: center;
  padding: 0 8px;
  flex-shrink: 0;
  user-select: none;
  border-bottom: 1px solid var(--border-subtle);
}
.titlebar-icon {
  width: 16px;
  height: 16px;
  background: var(--bg-accent);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #111;
  font-weight: 700;
  margin-right: 8px;
}
.titlebar-title {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 400;
  letter-spacing: 0.02em;
}
.titlebar-drag {
  flex: 1;
  -webkit-app-region: drag;
}
.titlebar-actions {
  display: flex;
  gap: 4px;
}
.titlebar-btn {
  width: 46px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0;
  transition: background 0.08s, color 0.08s;
}
.titlebar-btn:hover { background: #333; color: var(--text-primary); }
.titlebar-btn.close:hover { background: #c42b1c; color: #fff; }
.titlebar-btn svg { width: 10px; height: 10px; fill: currentColor; }
/* --- MAIN LAYOUT --- */
.main {
  flex: 1;
  display: flex;
  overflow: hidden;
}
/* --- SIDEBAR --- */
.sidebar {
  width: 220px;
  background: var(--bg-surface-alt);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-nav {
  flex: 1;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-section-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-tertiary);
  padding: 12px 12px 4px;
  letter-spacing: 0.05em;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: background 0.1s, color 0.1s;
}
.nav-item:hover { background: rgba(255,255,255,0.04); color: var(--text-primary); }
.nav-item.active { background: rgba(96, 205, 255, 0.1); color: var(--bg-accent); }
.nav-item .icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  opacity: 0.7;
}
.nav-item.active .icon { opacity: 1; }
.sidebar-footer {
  padding: 8px;
  border-top: 1px solid var(--border-subtle);
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: var(--radius-sm);
  cursor: pointer;
}
.user-profile:hover { background: rgba(255,255,255,0.04); }
.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #60cdff, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}
.user-name { font-size: 12px; color: var(--text-primary); }
.user-role { font-size: 10px; color: var(--text-tertiary); }
/* --- CONTENT AREA --- */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}
/* Toolbar */
.toolbar {
  height: 44px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 12px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
  background: var(--bg-surface-alt);
}
.toolbar h1 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.01em;
}
.toolbar-badge {
  font-size: 10px;
  background: rgba(96, 205, 255, 0.15);
  color: var(--bg-accent);
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}
.toolbar-spacer { flex: 1; }
.toolbar-btn {
  padding: 6px 14px;
  background: var(--bg-surface-raised);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  font-family: var(--font-ui);
  transition: background 0.1s, border-color 0.1s;
}
.toolbar-btn:hover { background: #363636; border-color: var(--border-raised); color: var(--text-primary); }
.toolbar-btn.primary { background: var(--bg-accent); color: #111; border: none; font-weight: 600; }
.toolbar-btn.primary:hover { background: #7fd9ff; }
/* Scrollable body */
.scroll-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}
.scroll-body::-webkit-scrollbar { width: 6px; }
.scroll-body::-webkit-scrollbar-track { background: transparent; }
.scroll-body::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 3px; }
.scroll-body::-webkit-scrollbar-thumb:hover { background: #555; }
/* --- DASHBOARD GRID --- */
.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.grid-3 {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
/* --- CARDS --- */
.card {
  background: var(--bg-surface-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  overflow: hidden;
  transition: border-color 0.15s;
}
.card:hover { border-color: var(--border-raised); }
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px 8px;
  border-bottom: 1px solid transparent;
}
.card-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.card-action {
  font-size: 16px;
  color: var(--text-tertiary);
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.1s;
}
.card-action:hover { opacity: 1; color: var(--text-secondary); }
.card-body {
  padding: 10px 14px 14px;
}
/* Stat cards */
.stat-value {
  font-size: 28px;
  font-weight: 300;
  color: var(--text-primary);
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.stat-sub {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
}
.stat-change {
  font-size: 11px;
  font-weight: 500;
  margin-top: 6px;
}
.stat-change.up { color: #4caf88; }
.stat-change.down { color: #e5554a; }
/* GPU Monitor */
.gauge-container {
  position: relative;
  width: 100%;
  height: 80px;
}
.gauge-canvas {
  width: 100%;
  height: 100%;
}
.gauge-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
}
.gauge-label {
  text-align: center;
  font-size: 11px;
  color: var(--text-secondary);
}
.gauge-label strong {
  display: block;
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 400;
}
/* Activity Feed */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.activity-item {
  display: flex;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.activity-item:last-child { border-bottom: none; }
.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}
.activity-dot.info { background: var(--bg-accent); }
.activity-dot.success { background: #4caf88; }
.activity-dot.warn { background: #f5a623; }
.activity-dot.error { background: #e5554a; }
.activity-text {
  flex: 1;
  font-size: 12px;
  color: var(--text-primary);
  line-height: 1.4;
}
.activity-text .ts {
  font-size: 10px;
  color: var(--text-tertiary);
  display: block;
  margin-top: 2px;
}
/* Agent status */
.agent-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.agent-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.02);
}
.agent-status {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.agent-status.online { background: #4caf88; box-shadow: 0 0 6px rgba(76,175,136,0.4); }
.agent-status.busy { background: #f5a623; box-shadow: 0 0 6px rgba(245,166,35,0.3); }
.agent-status.idle { background: var(--text-tertiary); }
.agent-status.offline { background: #e5554a; }
.agent-name { font-size: 12px; color: var(--text-primary); flex: 1; }
.agent-metrics { font-size: 10px; color: var(--text-tertiary); font-family: var(--font-mono); }
/* Mini chart */
.chart-container {
  height: 60px;
  position: relative;
}
.chart-svg {
  width: 100%;
  height: 100%;
}
/* Resource bars */
.resource-bar {
  margin-bottom: 8px;
}
.resource-bar:last-child { margin-bottom: 0; }
.resource-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
.resource-track {
  height: 4px;
  background: #333;
  border-radius: 2px;
  overflow: hidden;
}
.resource-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}
.resource-fill.cpu { background: linear-gradient(90deg, #60cdff, #8b5cf6); }
.resource-fill.mem { background: linear-gradient(90deg, #4caf88, #60cdff); }
.resource-fill.disk { background: linear-gradient(90deg, #f5a623, #e5554a); }
/* Live indicator pulse */
.live-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  color: var(--text-tertiary);
}
.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4caf88;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
/* Separator */
.sep { border-top: 1px solid var(--border-subtle); margin: 16px 0; }
/* Section title */
.section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  letter-spacing: 0.02em;
}
/* Responsive tweaks */
@media (max-width: 1100px) {
  .window { width: 96vw; height: 90vh; }
}
@media (max-width: 800px) {
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .sidebar { width: 56px; }
  .sidebar .nav-item span,
  .sidebar .nav-section-label,
  .sidebar .user-profile .user-name,
  .sidebar .user-profile .user-role { display: none; }
  .sidebar .nav-item { justify-content: center; padding: 10px; }
  .sidebar .user-profile { justify-content: center; }
}
</style>
</head>
<body>
<div class="desktop">
<div class="window">
  <!-- TITLEBAR -->
  <div class="titlebar">
    <div class="titlebar-icon">SF</div>
    <span class="titlebar-title">Styde Forge &mdash; Control Center</span>
    <div class="titlebar-drag"></div>
    <div class="titlebar-actions">
      <button class="titlebar-btn" title="Minimize">
        <svg viewBox="0 0 10 10"><rect x="0" y="4.5" width="10" height="1" fill="currentColor"/></svg>
      </button>
      <button class="titlebar-btn" title="Maximize">
        <svg viewBox="0 0 10 10"><rect x="1.5" y="1.5" width="7" height="7" rx=".5" fill="none" stroke="currentColor" stroke-width="1"/></svg>
      </button>
      <button class="titlebar-btn close" title="Close">
        <svg viewBox="0 0 10 10"><path d="M1.5 1.5l7 7m-7 0l7-7" stroke="currentColor" stroke-width="1.2" fill="none"/></svg>
      </button>
    </div>
  </div>
  <!-- MAIN -->
  <div class="main">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <div class="sidebar-nav">
        <div class="nav-section-label">Manage</div>
        <div class="nav-item active">
          <span class="icon">&#9632;</span>
          <span>Dashboard</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9881;</span>
          <span>Agents</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9733;</span>
          <span>Blueprints</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9673;</span>
          <span>Pipeline</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9776;</span>
          <span>Logs</span>
        </div>
        <div class="nav-section-label">System</div>
        <div class="nav-item">
          <span class="icon">&#9889;</span>
          <span>Workers</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9874;</span>
          <span>Storage</span>
        </div>
        <div class="nav-item">
          <span class="icon">&#9993;</span>
          <span>Settings</span>
        </div>
      </div>
      <div class="sidebar-footer">
        <div class="user-profile">
          <div class="user-avatar">PA</div>
          <div>
            <div class="user-name">Pontus Alpedal</div>
            <div class="user-role">Orchestrator</div>
          </div>
        </div>
      </div>
    </div>
    <!-- CONTENT -->
    <div class="content">
      <!-- TOOLBAR -->
      <div class="toolbar">
        <h1>Dashboard</h1>
        <span class="toolbar-badge">v1.7.2</span>
        <div class="toolbar-spacer"></div>
        <span class="live-indicator"><span class="live-dot"></span> Live</span>
        <button class="toolbar-btn primary" id="deployBtn">Deploy All</button>
        <button class="toolbar-btn" id="refreshBtn">Refresh</button>
      </div>
      <!-- SCROLL BODY -->
      <div class="scroll-body">
        <!-- STAT ROW -->
        <div class="grid-4">
          <div class="card">
            <div class="card-header">
              <span class="card-title">Active Agents</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="stat-value" id="activeAgents">12</div>
              <div class="stat-sub">of 18 provisioned</div>
              <div class="stat-change up">+2 since last hour</div>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-title">Pipelines</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="stat-value" id="pipelineCount">7</div>
              <div class="stat-sub">running</div>
              <div class="stat-change up">3 completed, 0 failed</div>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-title">GPU Load</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="stat-value" id="gpuLoad">68%</div>
              <div class="stat-sub">RTX 4090 &bull; 24 GB</div>
              <div class="stat-change down">+12% from idle</div>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-title">Uptime</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="stat-value" id="uptime">14d 7h</div>
              <div class="stat-sub">last deploy: 2h ago</div>
              <div class="stat-change up">All systems nominal</div>
            </div>
          </div>
        </div>
        <!-- GPU + SYSTEM -->
        <div class="grid-3" style="grid-template-columns: 1.4fr 1fr;">
          <!-- GPU Monitor Card -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">GPU Monitor &mdash; NVIDIA RTX 4090</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="gauge-container">
                <canvas id="gaugeChart" class="gauge-canvas"></canvas>
              </div>
              <div class="gauge-labels" style="margin-top: 8px;">
                <div class="gauge-label"><strong id="gCore">1845</strong>MHz Core</div>
                <div class="gauge-label"><strong id="gMem">10201</strong>MHz Mem</div>
                <div class="gauge-label"><strong id="gTemp">71</strong>&deg;C Temp</div>
                <div class="gauge-label"><strong id="gPower">285</strong>W Power</div>
              </div>
            </div>
          </div>
          <!-- System Resources -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">System Resources</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="resource-bar">
                <div class="resource-label"><span>CPU &mdash; AMD Ryzen 9 7950X</span><span id="cpuPct">42%</span></div>
                <div class="resource-track"><div class="resource-fill cpu" id="cpuFill" style="width:42%"></div></div>
              </div>
              <div class="resource-bar">
                <div class="resource-label"><span>Memory &mdash; 64 GB DDR5</span><span id="memPct">37%</span></div>
                <div class="resource-track"><div class="resource-fill mem" id="memFill" style="width:37%"></div></div>
              </div>
              <div class="resource-bar">
                <div class="resource-label"><span>Disk &mdash; NVMe 2 TB</span><span id="diskPct">54%</span></div>
                <div class="resource-track"><div class="resource-fill disk" id="diskFill" style="width:54%"></div></div>
              </div>
              <div class="sep" style="margin: 12px 0;"></div>
              <div class="chart-container">
                <canvas id="miniChart" class="chart-svg"></canvas>
              </div>
            </div>
          </div>
        </div>
        <!-- AGENTS + ACTIVITY -->
        <div class="grid-2">
          <!-- Agent Status -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Agent Fleet</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="agent-list" id="agentList">
                <div class="agent-row">
                  <span class="agent-status online"></span>
                  <span class="agent-name">Hermes Core</span>
                  <span class="agent-metrics">142ms &bull; 0 err</span>
                </div>
                <div class="agent-row">
                  <span class="agent-status busy"></span>
                  <span class="agent-name">PrecisionForge</span>
                  <span class="agent-metrics">283ms &bull; 2 queued</span>
                </div>
                <div class="agent-row">
                  <span class="agent-status online"></span>
                  <span class="agent-name">Desktop Mockup Artist</span>
                  <span class="agent-metrics">97ms &bull; idle</span>
                </div>
                <div class="agent-row">
                  <span class="agent-status online"></span>
                  <span class="agent-name">Refinery Agent</span>
                  <span class="agent-metrics">211ms &bull; refining</span>
                </div>
                <div class="agent-row">
                  <span class="agent-status idle"></span>
                  <span class="agent-name">Production Agent</span>
                  <span class="agent-metrics">156ms &bull; idle</span>
                </div>
                <div class="agent-row">
                  <span class="agent-status offline"></span>
                  <span class="agent-name">Legacy Bridge</span>
                  <span class="agent-metrics">N/A &bull; offline</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Activity Feed -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Activity Feed</span>
              <span class="card-action">&hellip;</span>
            </div>
            <div class="card-body">
              <div class="activity-feed" id="activityFeed">
                <div class="activity-item">
                  <span class="activity-dot success"></span>
                  <div class="activity-text">Deployment complete: blueprint v1.7.2 promoted to production<span class="ts">2 min ago</span></div>
                </div>
                <div class="activity-item">
                  <span class="activity-dot info"></span>
                  <div class="activity-text">Hermes Core spawned new agent: Desktop Mockup Artist<span class="ts">8 min ago</span></div>
                </div>
                <div class="activity-item">
                  <span class="activity-dot warn"></span>
                  <div class="activity-text">Resource threshold warning: GPU memory approaching 22 GB<span class="ts">15 min ago</span></div>
                </div>
                <div class="activity-item">
                  <span class="activity-dot info"></span>
                  <div class="activity-text">PrecisionForge pipeline completed: 7 batches, 0 failures<span class="ts">32 min ago</span></div>
                </div>
                <div class="activity-item">
                  <span class="activity-dot success"></span>
                  <div class="activity-text">Agent auto-recovery: Legacy Bridge reconnected after timeout<span class="ts">47 min ago</span></div>
                </div>
                <div class="activity-item">
                  <span class="activity-dot error"></span>
                  <div class="activity-text">Error in eval pipeline: timeout on batch #412, retrying<span class="ts">1h ago</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div><!-- /scroll-body -->
    </div><!-- /content -->
  </div><!-- /main -->
</div><!-- /window -->
</div><!-- /desktop -->
<script>
(function() {
// --- GAUGE CHART (semi-circle radial gauge) ---
function drawGauge(canvas, pct) {
  if (!canvas) return;
  const rect = canvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || rect.width;
  const h = canvas.clientHeight || rect.height;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const cx = w / 2;
  const cy = h * 0.75;
  const r = Math.min(w * 0.38, h * 0.55);
  const startAngle = Math.PI * 0.75;
  const endAngle = Math.PI * 0.25;
  const sweep = endAngle - startAngle;
  const curAngle = startAngle + sweep * (Math.min(Math.max(pct, 0), 100) / 100);
  ctx.clearRect(0, 0, w, h);
  // BG arc
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, endAngle);
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 10;
  ctx.lineCap = 'round';
  ctx.stroke();
  // Fill arc
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, curAngle);
  ctx.strokeStyle = '#60cdff';
  ctx.lineWidth = 10;
  ctx.lineCap = 'round';
  ctx.stroke();
  // Glow
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, curAngle);
  ctx.strokeStyle = 'rgba(96, 205, 255, 0.15)';
  ctx.lineWidth = 18;
  ctx.lineCap = 'round';
  ctx.stroke();
  // Center value
  ctx.fillStyle = '#f0f0f0';
  ctx.font = '600 28px "Segoe UI Variable", "Segoe UI", system-ui, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(Math.round(pct) + '%', cx, cy - 6);
  ctx.fillStyle = '#727272';
  ctx.font = '11px "Segoe UI Variable", "Segoe UI", system-ui, sans-serif';
  ctx.fillText('GPU Util', cx, cy + 20);
}
// --- MINI SPARKLINE ---
function drawSparkline(canvas, data, color) {
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || canvas.parentElement.clientWidth;
  const h = canvas.clientHeight || 60;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const pad = 4;
  const dw = w - pad * 2;
  const dh = h - pad * 2;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  ctx.clearRect(0, 0, w, h);
  // Fill area
  ctx.beginPath();
  data.forEach((v, i) => {
    const x = pad + (i / (data.length - 1)) * dw;
    const y = pad + dh - ((v - min) / range) * dh;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.lineTo(pad + dw, pad + dh);
  ctx.lineTo(pad, pad + dh);
  ctx.closePath();
  ctx.fillStyle = 'rgba(96, 205, 255, 0.06)';
  ctx.fill();
  // Stroke line
  ctx.beginPath();
  data.forEach((v, i) => {
    const x = pad + (i / (data.length - 1)) * dw;
    const y = pad + dh - ((v - min) / range) * dh;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = color || '#60cdff';
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.stroke();
  // Glow
  ctx.beginPath();
  data.forEach((v, i) => {
    const x = pad + (i / (data.length - 1)) * dw;
    const y = pad + dh - ((v - min) / range) * dh;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = 'rgba(96, 205, 255, 0.2)';
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.stroke();
}
// --- SIMULATED LIVE DATA ---
function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function simulateLiveData() {
  const cpu = rand(20, 85);
  const mem = rand(25, 70);
  const disk = rand(30, 80);
  const gpu = rand(30, 95);
  document.getElementById('cpuPct').textContent = cpu + '%';
  document.getElementById('cpuFill').style.width = cpu + '%';
  document.getElementById('memPct').textContent = mem + '%';
  document.getElementById('memFill').style.width = mem + '%';
  document.getElementById('diskPct').textContent = disk + '%';
  document.getElementById('diskFill').style.width = disk + '%';
  document.getElementById('gpuLoad').textContent = gpu + '%';
  document.getElementById('gCore').textContent = rand(1500, 2760);
  document.getElementById('gMem').textContent = rand(8000, 11000);
  document.getElementById('gTemp').textContent = rand(55, 82);
  document.getElementById('gPower').textContent = rand(180, 350);
  const gaugeCanvas = document.getElementById('gaugeChart');
  drawGauge(gaugeCanvas, gpu);
  // Update activity feed periodically
  const feed = document.getElementById('activityFeed');
  const msgs = [
    { dot: 'info', text: 'GPU load spiked to ' + gpu + '% during batch inference' },
    { dot: 'success', text: 'Agent Hermes Core heartbeat: ' + rand(80, 200) + 'ms latency' },
    { dot: 'warn', text: 'Memory pressure: ' + mem + '% system RAM utilized' },
    { dot: 'info', text: 'Pipeline #' + rand(400, 499) + ' queued with ' + rand(1, 6) + ' tasks' },
    { dot: 'success', text: 'Agent self-heal: idle worker re-engaged' },
  ];
  const pick = msgs[rand(0, msgs.length - 1)];
  const item = document.createElement('div');
  item.className = 'activity-item';
  item.innerHTML = '<span class="activity-dot ' + pick.dot + '"></span><div class="activity-text">' + pick.text + '<span class="ts">just now</span></div>';
  feed.insertBefore(item, feed.firstChild);
  if (feed.children.length > 12) feed.removeChild(feed.lastChild);
}
// --- INIT ---
window.addEventListener('load', function() {
  // Gauge
  const gaugeCanvas = document.getElementById('gaugeChart');
  drawGauge(gaugeCanvas, 68);
  // Sparkline
  const sparkData = Array.from({ length: 30 }, () => rand(20, 95));
  const miniChart = document.getElementById('miniChart');
  drawSparkline(miniChart, sparkData, '#60cdff');
  // Live simulation every 3s
  setInterval(simulateLiveData, 3500);
  // Button events
  document.getElementById('deployBtn').addEventListener('click', function() {
    const orig = this.textContent;
    this.textContent = 'Deploying...';
    this.disabled = true;
    setTimeout(() => { this.textContent = 'Deployed!'; setTimeout(() => { this.textContent = orig; this.disabled = false; }, 1500); }, 800);
  });
  document.getElementById('refreshBtn').addEventListener('click', function() {
    simulateLiveData();
    this.textContent = 'Refreshed';
    setTimeout(() => { this.textContent = 'Refresh'; }, 1000);
  });
});
// Resize handler
window.addEventListener('resize', function() {
  const gaugeCanvas = document.getElementById('gaugeChart');
  const gpuText = document.getElementById('gpuLoad').textContent;
  drawGauge(gaugeCanvas, parseInt(gpuText) || 68);
  const sparkData = Array.from({ length: 30 }, () => rand(20, 95));
  drawSparkline(document.getElementById('miniChart'), sparkData, '#60cdff');
});
})();
</script>
</body>
</html>