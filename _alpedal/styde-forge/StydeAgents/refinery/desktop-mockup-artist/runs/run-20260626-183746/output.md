name: desktop-mockup-artist
task: generate-layout
layout: System Dashboard (Layout 1)
zones: [titlebar, sidebar-collapsed, header, content-4-cards, activity-feed, gpu-panel, memory-panel, statusbar]
structural catalog check:
  titlebar: present
  sidebar: present (collapsed 48px)
  header: present (search + action buttons)
  metric cards: 4 (CPU, RAM, GPU, NET)
  activity feed: present (timestamped list)
  gpu panel: present (temp + fan)
  memory panel: present (usage bar + stats)
  status bar: present (connection + uptime + agents)
pre-submission static verification:
  DOCTYPE: yes
  CSS vars: yes (all colors/spacing as --custom-properties)
  function keyword: 0 violations
  var keyword: 0 violations
  string concatenation (+): 0 violations
  template literals: used
  arrow functions: all
  hardcoded example URLs: none (data: URIs used)
  SVG viewBox: all present
<svg width="0" height="0" style="position:absolute;display:none" aria-hidden="true">
<defs>
<linearGradient id="cpuGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#3b82f6"/></linearGradient>
<linearGradient id="ramGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#34d399"/><stop offset="100%" stop-color="#10b981"/></linearGradient>
<linearGradient id="gpuGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#f472b6"/><stop offset="100%" stop-color="#ec4899"/></linearGradient>
<linearGradient id="netGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#f59e0b"/></linearGradient>
<linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#818cf8" stop-opacity="0.4"/><stop offset="100%" stop-color="#818cf8" stop-opacity="0"/></linearGradient>
</defs>
</svg>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Control Center</title>
<style>
:root {
  --bg-primary: #1a1b2e;
  --bg-secondary: #222340;
  --bg-card: #282950;
  --bg-card-hover: #2e2f5a;
  --bg-titlebar: #16172b;
  --bg-sidebar: #1e1f38;
  --bg-statusbar: #16172b;
  --bg-input: #1e1f3a;
  --border-color: #3a3b5c;
  --border-subtle: #333458;
  --text-primary: #e8e9f0;
  --text-secondary: #9a9bb8;
  --text-muted: #6b6d8a;
  --accent-blue: #60a5fa;
  --accent-green: #34d399;
  --accent-pink: #f472b6;
  --accent-yellow: #fbbf24;
  --accent-purple: #818cf8;
  --accent-red: #f87171;
  --titlebar-height: 32px;
  --sidebar-width-collapsed: 48px;
  --sidebar-width-expanded: 220px;
  --statusbar-height: 28px;
  --content-padding: 16px;
  --card-gap: 12px;
  --card-radius: 6px;
  --icon-size-sm: 16px;
  --icon-size-md: 20px;
  --icon-size-lg: 24px;
  --font-mono: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
  --font-sans: 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif;
  --shadow-card: 0 2px 8px rgba(0,0,0,0.3);
  --shadow-float: 0 4px 16px rgba(0,0,0,0.4);
  --transition-fast: 150ms ease;
  --sidebar-width: var(--sidebar-width-collapsed);
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; overflow: hidden; font-family: var(--font-sans); background: var(--bg-primary); color: var(--text-primary); font-size: 13px; line-height: 1.5; user-select: none; -webkit-font-smoothing: antialiased; }
/* Titlebar */
.titlebar {
  height: var(--titlebar-height);
  background: var(--bg-titlebar);
  display: flex;
  align-items: center;
  padding: 0 8px;
  border-bottom: 1px solid var(--border-subtle);
  position: relative;
  z-index: 100;
  flex-shrink: 0;
}
.titlebar-drag { flex: 1; -webkit-app-region: drag; display: flex; align-items: center; gap: 8px; padding-left: 4px; }
.titlebar-icon { width: 16px; height: 16px; background: var(--accent-purple); border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: white; font-weight: 700; flex-shrink: 0; }
.titlebar-title { font-size: 12px; color: var(--text-secondary); font-weight: 500; letter-spacing: 0.3px; }
.titlebar-controls { display: flex; gap: 1px; }
.titlebar-btn { width: 28px; height: 22px; display: flex; align-items: center; justify-content: center; border: none; background: transparent; color: var(--text-secondary); cursor: pointer; border-radius: 3px; font-size: 11px; transition: var(--transition-fast); }
.titlebar-btn:hover { background: rgba(255,255,255,0.08); color: var(--text-primary); }
.titlebar-btn.close:hover { background: #e81123; color: white; }
/* Layout */
.app-layout { display: flex; height: calc(100% - var(--titlebar-height) - var(--statusbar-height)); }
/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  gap: 2px;
  flex-shrink: 0;
  transition: width var(--transition-fast);
  overflow: hidden;
}
.sidebar-item {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-muted);
  font-size: 18px;
  transition: var(--transition-fast);
  position: relative;
}
.sidebar-item:hover { background: rgba(255,255,255,0.06); color: var(--text-secondary); }
.sidebar-item.active { background: rgba(96,165,250,0.15); color: var(--accent-blue); }
.sidebar-item.active::before { content: ''; position: absolute; left: -8px; top: 50%; transform: translateY(-50%); width: 3px; height: 18px; background: var(--accent-blue); border-radius: 0 2px 2px 0; }
.sidebar-divider { width: 24px; height: 1px; background: var(--border-subtle); margin: 4px 0; }
/* Main area */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}
/* Header */
.header {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}
.header-search {
  flex: 1;
  max-width: 320px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 5px 10px;
  color: var(--text-primary);
  font-size: 12px;
  font-family: var(--font-sans);
  outline: none;
  transition: var(--transition-fast);
}
.header-search:focus { border-color: var(--accent-blue); box-shadow: 0 0 0 2px rgba(96,165,250,0.2); }
.header-search::placeholder { color: var(--text-muted); }
.header-actions { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.header-btn {
  width: 30px; height: 30px; border-radius: 6px; border: none; background: transparent;
  color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: 16px; transition: var(--transition-fast); position: relative;
}
.header-btn:hover { background: rgba(255,255,255,0.06); color: var(--text-primary); }
.header-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; color: white; cursor: pointer; }
.notif-dot { position: absolute; top: 5px; right: 5px; width: 7px; height: 7px; background: var(--accent-red); border-radius: 50%; border: 2px solid var(--bg-primary); }
/* Content scrollable */
.content-scroll {
  flex: 1;
  overflow-y: auto;
  padding: var(--content-padding);
  display: flex;
  flex-direction: column;
  gap: var(--card-gap);
}
.content-scroll::-webkit-scrollbar { width: 6px; }
.content-scroll::-webkit-scrollbar-track { background: transparent; }
.content-scroll::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
.content-scroll::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
/* Metric cards row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--card-gap);
}
.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  padding: 14px 16px;
  box-shadow: var(--shadow-card);
  transition: var(--transition-fast);
  cursor: default;
}
.metric-card:hover { background: var(--bg-card-hover); border-color: var(--border-color); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
.metric-value { font-size: 22px; font-weight: 600; color: var(--text-primary); font-family: var(--font-mono); letter-spacing: -0.5px; }
.metric-sub { font-size: 11px; color: var(--text-secondary); margin-top: 2px; }
.metric-bar { height: 4px; border-radius: 2px; margin-top: 8px; background: rgba(255,255,255,0.06); overflow: hidden; }
.metric-bar-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
.metric-trend { font-size: 11px; display: flex; align-items: center; gap: 4px; margin-top: 4px; }
.trend-up { color: var(--accent-green); }
.trend-down { color: var(--accent-red); }
/* Panels row */
.panels-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--card-gap);
}
.panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-subtle);
}
.panel-title { font-size: 12px; font-weight: 600; color: var(--text-primary); }
.panel-badge { font-size: 10px; color: var(--text-muted); background: rgba(255,255,255,0.04); padding: 2px 8px; border-radius: 10px; }
.panel-body { padding: 12px 14px; }
/* Activity feed */
.activity-list { display: flex; flex-direction: column; gap: 6px; }
.activity-item {
  display: flex; align-items: flex-start; gap: 10px; padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.activity-item:last-child { border-bottom: none; }
.activity-icon {
  width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center;
  font-size: 13px; flex-shrink: 0; margin-top: 1px;
}
.activity-icon.success { background: rgba(52,211,153,0.15); color: var(--accent-green); }
.activity-icon.fail { background: rgba(248,113,113,0.15); color: var(--accent-red); }
.activity-icon.running { background: rgba(96,165,250,0.15); color: var(--accent-blue); }
.activity-icon.idle { background: rgba(155,155,184,0.1); color: var(--text-muted); }
.activity-content { flex: 1; min-width: 0; }
.activity-text { font-size: 12px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.activity-meta { font-size: 11px; color: var(--text-muted); margin-top: 1px; display: flex; align-items: center; gap: 6px; }
.activity-status { font-size: 10px; padding: 1px 6px; border-radius: 3px; }
.activity-status.completed { background: rgba(52,211,153,0.12); color: var(--accent-green); }
.activity-status.failed { background: rgba(248,113,113,0.12); color: var(--accent-red); }
.activity-status.running { background: rgba(96,165,250,0.12); color: var(--accent-blue); }
/* GPU panel */
.gpu-stats { display: flex; flex-direction: column; gap: 10px; }
.gpu-stat-row { display: flex; align-items: center; gap: 10px; }
.gpu-stat-label { font-size: 11px; color: var(--text-muted); width: 50px; flex-shrink: 0; }
.gpu-stat-bar { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.gpu-stat-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.gpu-stat-value { font-size: 11px; color: var(--text-secondary); font-family: var(--font-mono); width: 55px; text-align: right; flex-shrink: 0; }
.gpu-temp-fill { background: linear-gradient(90deg, var(--accent-green), var(--accent-yellow), var(--accent-red)); }
.gpu-util-fill { background: var(--accent-pink); }
.gpu-mem-fill { background: var(--accent-purple); }
/* Memory panel */
.memory-vis { display: flex; flex-direction: column; gap: 10px; }
.memory-chart { height: 60px; position: relative; }
.memory-chart canvas { width: 100%; height: 100%; border-radius: 4px; }
.memory-details { display: flex; gap: 16px; flex-wrap: wrap; }
.memory-detail-item { }
.memory-detail-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.3px; }
.memory-detail-value { font-size: 14px; font-weight: 600; color: var(--text-primary); font-family: var(--font-mono); }
.memory-detail-sub { font-size: 10px; color: var(--text-secondary); }
/* Status bar */
.statusbar {
  height: var(--statusbar-height);
  background: var(--bg-statusbar);
  border-top: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  padding: 0 12px;
  gap: 16px;
  font-size: 11px;
  color: var(--text-muted);
  flex-shrink: 0;
}
.statusbar-left { display: flex; align-items: center; gap: 12px; }
.statusbar-right { margin-left: auto; display: flex; align-items: center; gap: 12px; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.online { background: var(--accent-green); box-shadow: 0 0 4px var(--accent-green); }
.statusbar-sep { width: 1px; height: 12px; background: var(--border-subtle); }
.clock { font-family: var(--font-mono); font-size: 11px; }
</style>
</head>
<body>
<div class="titlebar">
  <div class="titlebar-drag">
    <div class="titlebar-icon">S</div>
    <span class="titlebar-title">Styde Control Center</span>
  </div>
  <div class="titlebar-controls">
    <button class="titlebar-btn" aria-label="minimize">&minus;</button>
    <button class="titlebar-btn" aria-label="maximize">&square;</button>
    <button class="titlebar-btn close" aria-label="close">&times;</button>
  </div>
</div>
<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-item active" title="Dashboard">&#8962;</div>
    <div class="sidebar-item" title="Builds">&#9881;</div>
    <div class="sidebar-item" title="Agents">&#129302;</div>
    <div class="sidebar-divider"></div>
    <div class="sidebar-item" title="Deploy">&#9654;</div>
    <div class="sidebar-item" title="Monitor">&#9783;</div>
    <div class="sidebar-item" title="Logs">&#9776;</div>
  </aside>
  <div class="main-area">
    <div class="header">
      <input class="header-search" type="text" placeholder="Search agents, builds, logs..." aria-label="Search">
      <div class="header-actions">
        <button class="header-btn" aria-label="Notifications">
          &#128276;<span class="notif-dot"></span>
        </button>
        <div class="header-avatar" title="Pontus">P</div>
      </div>
    </div>
    <div class="content-scroll">
      <div class="metrics-row">
        <div class="metric-card">
          <div class="metric-label">&#128187; CPU</div>
          <div class="metric-value">72%</div>
          <div class="metric-sub">3.2 GHz / 8 cores</div>
          <div class="metric-bar"><div class="metric-bar-fill" style="width:72%;background:var(--accent-blue);"></div></div>
          <div class="metric-trend trend-down">&#9660; 3% from peak</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">&#128190; RAM</div>
          <div class="metric-value">8.4</div>
          <div class="metric-sub">GB used / 16 GB total (52.5%)</div>
          <div class="metric-bar"><div class="metric-bar-fill" style="width:52.5%;background:var(--accent-green);"></div></div>
          <div class="metric-trend trend-up">&#9650; 1.2 GB since boot</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">&#127916; GPU</div>
          <div class="metric-value">45%</div>
          <div class="metric-sub">NVIDIA RTX 4060 / 8 GB VRAM</div>
          <div class="metric-bar"><div class="metric-bar-fill" style="width:45%;background:var(--accent-pink);"></div></div>
          <div class="metric-trend trend-up">&#9650; 12% from idle</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">&#127760; Network</div>
          <div class="metric-value">1.2</div>
          <div class="metric-sub">Gbps of 10 Gbps link (12%)</div>
          <div class="metric-bar"><div class="metric-bar-fill" style="width:12%;background:var(--accent-yellow);"></div></div>
          <div class="metric-trend trend-down">&#9660; 0.3 Gbps from peak</div>
        </div>
      </div>
      <div class="panels-row">
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">&#128240; Agent Activity Feed</span>
            <span class="panel-badge">Live</span>
          </div>
          <div class="panel-body">
            <div class="activity-list">
              <div class="activity-item">
                <div class="activity-icon success">&#10004;</div>
                <div class="activity-content">
                  <div class="activity-text">Deploy-agent deployed v2.4.2 to production</div>
                  <div class="activity-meta"><span>14:32</span><span class="activity-status completed">Completed</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon fail">&#10008;</div>
                <div class="activity-content">
                  <div class="activity-text">Review-agent PR #94 — auth-timeout test failure</div>
                  <div class="activity-meta"><span>14:28</span><span class="activity-status failed">Failed</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon running">&#9654;</div>
                <div class="activity-content">
                  <div class="activity-text">Build-agent building commit a3f2c1e — main-branch merge</div>
                  <div class="activity-meta"><span>14:22</span><span class="activity-status running">Running 34s</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon idle">&#9679;</div>
                <div class="activity-content">
                  <div class="activity-text">Monitor-agent health check completed — all systems nominal</div>
                  <div class="activity-meta"><span>14:18</span><span class="activity-status completed">Completed</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon success">&#10004;</div>
                <div class="activity-content">
                  <div class="activity-text">Test-agent suite #421 passed — 142/142 tests green</div>
                  <div class="activity-meta"><span>14:10</span><span class="activity-status completed">Completed</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">&#127777; GPU Monitor</span>
            <span class="panel-badge">RTX 4060</span>
          </div>
          <div class="panel-body">
            <div class="gpu-stats">
              <div class="gpu-stat-row">
                <span class="gpu-stat-label">Temp</span>
                <div class="gpu-stat-bar"><div class="gpu-stat-fill gpu-temp-fill" style="width:56%;"></div></div>
                <span class="gpu-stat-value">67 C</span>
              </div>
              <div class="gpu-stat-row">
                <span class="gpu-stat-label">Util</span>
                <div class="gpu-stat-bar"><div class="gpu-stat-fill gpu-util-fill" style="width:45%;"></div></div>
                <span class="gpu-stat-value">45%</span>
              </div>
              <div class="gpu-stat-row">
                <span class="gpu-stat-label">VRAM</span>
                <div class="gpu-stat-bar"><div class="gpu-stat-fill gpu-mem-fill" style="width:38%;"></div></div>
                <span class="gpu-stat-value">3.0 / 8 GB</span>
              </div>
              <div class="gpu-stat-row" style="margin-top:4px;">
                <span class="gpu-stat-label">Fan</span>
                <span class="gpu-stat-value" style="width:auto;text-align:left;">2100 RPM (42%)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="panels-row">
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">&#128200; Memory Usage — Last 60s</span>
            <span class="panel-badge">8.4 GB / 16 GB</span>
          </div>
          <div class="panel-body">
            <div class="memory-vis">
              <div class="memory-chart">
                <canvas id="memoryChart" width="400" height="80"></canvas>
              </div>
              <div class="memory-details">
                <div class="memory-detail-item">
                  <div class="memory-detail-label">Used</div>
                  <div class="memory-detail-value">8.4</div>
                  <div class="memory-detail-sub">GB of 16 GB</div>
                </div>
                <div class="memory-detail-item">
                  <div class="memory-detail-label">Available</div>
                  <div class="memory-detail-value">7.6</div>
                  <div class="memory-detail-sub">GB (47.5%)</div>
                </div>
                <div class="memory-detail-item">
                  <div class="memory-detail-label">Cache</div>
                  <div class="memory-detail-value">2.1</div>
                  <div class="memory-detail-sub">GB</div>
                </div>
                <div class="memory-detail-item">
                  <div class="memory-detail-label">Commit</div>
                  <div class="memory-detail-value">11.2</div>
                  <div class="memory-detail-sub">GB / 32 GB limit</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">&#128736; System Overview</span>
            <span class="panel-badge">Uptime 12h</span>
          </div>
          <div class="panel-body">
            <div class="activity-list">
              <div class="activity-item">
                <div class="activity-icon success" style="background:rgba(96,165,250,0.15);color:var(--accent-blue);">&#9889;</div>
                <div class="activity-content">
                  <div class="activity-text">Active agents <span style="color:var(--text-secondary);font-size:11px;">6 of 8 online</span></div>
                  <div class="activity-meta">3 running &middot; 2 idle &middot; 1 queued</div>
                </div>
                <span style="font-size:14px;font-weight:600;color:var(--accent-green);font-family:var(--font-mono);">6</span>
              </div>
              <div class="activity-item">
                <div class="activity-icon success" style="background:rgba(52,211,153,0.15);color:var(--accent-green);">&#9850;</div>
                <div class="activity-content">
                  <div class="activity-text">Build pipeline <span style="color:var(--text-secondary);font-size:11px;">last: 2m ago</span></div>
                  <div class="activity-meta">Pass rate: 94.2% (412/438 builds)</div>
                </div>
                <span style="font-size:14px;font-weight:600;color:var(--text-primary);font-family:var(--font-mono);">94%</span>
              </div>
              <div class="activity-item">
                <div class="activity-icon fail" style="background:rgba(248,113,113,0.15);color:var(--accent-red);">&#9888;</div>
                <div class="activity-content">
                  <div class="activity-text">Failed tasks today <span style="color:var(--text-secondary);font-size:11px;">needs review</span></div>
                  <div class="activity-meta">3 failures &middot; 2 auto-retried &middot; 1 unrecovered</div>
                </div>
                <span style="font-size:14px;font-weight:600;color:var(--accent-red);font-family:var(--font-mono);">3</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="statusbar">
  <div class="statusbar-left">
    <span class="status-dot online"></span>
    <span>Connected</span>
    <span class="statusbar-sep"></span>
    <span>Uptime: 12h 34m</span>
    <span class="statusbar-sep"></span>
    <span>Agents: 6/8 online</span>
  </div>
  <div class="statusbar-right">
    <span style="color:var(--accent-yellow);">&#9888; 1 retry pending</span>
    <span class="statusbar-sep"></span>
    <span>Queue: 3</span>
    <span class="statusbar-sep"></span>
    <span class="clock" id="clock">00:00</span>
  </div>
</div>
<script>
const updateClock = () => {
  const now = new Date();
  document.getElementById('clock').textContent =
    String(now.getHours()).padStart(2,'0') + ':' +
    String(now.getMinutes()).padStart(2,'0') + ':' +
    String(now.getSeconds()).padStart(2,'0');
};
updateClock();
setInterval(updateClock, 1000);
const canvas = document.getElementById('memoryChart');
if (canvas) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  const drawChart = () => {
    ctx.clearRect(0, 0, w, h);
    const points = [62, 58, 55, 60, 65, 63, 58, 54, 52, 48, 45, 42, 45, 48, 51, 55, 58, 62, 60, 56, 52, 49, 46, 44, 48, 52, 56, 60, 58, 54];
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, 'rgba(129, 140, 248, 0.4)');
    gradient.addColorStop(1, 'rgba(129, 140, 248, 0)');
    ctx.beginPath();
    ctx.moveTo(0, h);
    points.forEach((p, i) => {
      const x = (i / (points.length - 1)) * w;
      const y = h - (p / 100) * h;
      ctx.lineTo(x, y);
    });
    ctx.lineTo(w, h);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.beginPath();
    points.forEach((p, i) => {
      const x = (i / (points.length - 1)) * w;
      const y = h - (p / 100) * h;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = '#818cf8';
    ctx.lineWidth = 2;
    ctx.stroke();
    const currentVal = points[points.length - 1];
    const lastX = w, lastY = h - (currentVal / 100) * h;
    ctx.beginPath();
    ctx.arc(lastX, lastY, 3, 0, Math.PI * 2);
    ctx.fillStyle = '#818cf8';
    ctx.fill();
  };
  drawChart();
}
</script>
</body>
</html>