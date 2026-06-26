glass-base.css
```css
:root {
  --glass-bg: rgba(255, 255, 255, 0.06);
  --glass-bg-strong: rgba(255, 255, 255, 0.12);
  --glass-bg-darker: rgba(0, 0, 0, 0.25);
  --glass-border: rgba(255, 255, 255, 0.10);
  --glass-border-strong: rgba(255, 255, 255, 0.18);
  --glass-blur: blur(24px);
  --glass-blur-light: blur(12px);
  --glass-radius: 16px;
  --glass-radius-sm: 10px;
  --glass-radius-lg: 24px;
  --edge-glow: 0 0 0 1px rgba(255,255,255,0.06) inset;
  --edge-glow-strong: 0 0 0 1px rgba(255,255,255,0.12) inset;
  --shadow-card: 0 8px 40px rgba(0,0,0,0.35), 0 2px 8px rgba(0,0,0,0.2);
  --shadow-elevated: 0 16px 64px rgba(0,0,0,0.45), 0 4px 16px rgba(0,0,0,0.25);
  --shadow-soft: 0 4px 20px rgba(0,0,0,0.2);
  --z-bg: 0;
  --z-mid: 10;
  --z-glass: 20;
  --z-ui: 30;
  --z-foreground: 40;
  --ambient-light-1: radial-gradient(ellipse 60% 50% at 20% 15%, rgba(120,140,255,0.12), transparent 70%);
  --ambient-light-2: radial-gradient(ellipse 50% 60% at 80% 85%, rgba(255,160,100,0.08), transparent 65%);
  --ambient-light-3: radial-gradient(circle 30% at 50% 0%, rgba(255,255,255,0.04), transparent);
  --noise-svg: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  --text-primary: rgba(255,255,255,0.92);
  --text-secondary: rgba(255,255,255,0.60);
  --text-tertiary: rgba(255,255,255,0.35);
  --accent-blue: #6b8aff;
  --accent-cyan: #4dd9f6;
  --accent-green: #4ade80;
  --accent-amber: #fbbf24;
  --accent-rose: #fb7185;
  --accent-purple: #a78bfa;
}
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  height: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: #0a0a0f;
  color: var(--text-primary);
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}
body {
  display: flex;
  align-items: center;
  justify-content: center;
}
.space {
  position: relative;
  width: 1280px;
  height: 800px;
  overflow: hidden;
  background: radial-gradient(ellipse 70% 50% at 30% 20%, #12122a, #080812 70%, #030308);
  border-radius: 20px;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 32px 120px rgba(0,0,0,0.7);
}
.ambient-layer {
  position: absolute;
  inset: 0;
  z-index: var(--z-bg);
  pointer-events: none;
}
.ambient-layer::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--ambient-light-1);
}
.ambient-layer::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--ambient-light-2);
}
.noise-layer {
  position: absolute;
  inset: 0;
  z-index: calc(var(--z-bg) + 1);
  pointer-events: none;
  background: var(--noise-svg);
  background-size: 200px 200px;
  mix-blend-mode: overlay;
  opacity: 0.5;
}
.depth-plane-1 { z-index: var(--z-mid); }
.depth-plane-2 { z-index: var(--z-glass); }
.depth-plane-3 { z-index: var(--z-ui); }
.depth-plane-4 { z-index: var(--z-foreground); }
.glass {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--shadow-card), var(--edge-glow);
}
.glass-sm {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur-light);
  -webkit-backdrop-filter: var(--glass-blur-light);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius-sm);
  box-shadow: var(--shadow-soft), var(--edge-glow);
}
.glass-strong {
  background: var(--glass-bg-strong);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border-strong);
  border-radius: var(--glass-radius);
  box-shadow: var(--shadow-elevated), var(--edge-glow-strong);
}
.glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 50%, rgba(255,255,255,0.02) 100%);
  pointer-events: none;
}
.glass-sm::before, .glass-strong::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, transparent 50%);
  pointer-events: none;
}
.spatial-glow {
  position: relative;
}
.spatial-glow::after {
  content: '';
  position: absolute;
  width: 120%;
  height: 120%;
  top: -10%;
  left: -10%;
  background: radial-gradient(circle at 50% 50%, var(--glow-color, rgba(107,138,255,0.10)), transparent 70%);
  z-index: -1;
  pointer-events: none;
}
.text-gradient {
  background: linear-gradient(135deg, var(--text-primary), rgba(255,255,255,0.5));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-tertiary);
}
.stat-value {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.02em;
}
.stat-delta {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 6px;
}
.delta-positive {
  background: rgba(74, 222, 128, 0.15);
  color: var(--accent-green);
}
.delta-negative {
  background: rgba(251, 113, 133, 0.15);
  color: var(--accent-rose);
}
.scrollable {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.10) transparent;
}
.scrollable::-webkit-scrollbar {
  width: 4px;
}
.scrollable::-webkit-scrollbar-track {
  background: transparent;
}
.scrollable::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.10);
  border-radius: 4px;
}
.spacer-h { height: 8px; }
.spacer-h2 { height: 16px; }
.spacer-h3 { height: 24px; }
```
dashboard-analytics.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Analytics — Glass Spatial Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="glass-base.css">
<style>
:root {
  --sidebar-w: 220px;
  --topbar-h: 56px;
  --content-p: 28px;
}
.space { background: radial-gradient(ellipse 65% 45% at 25% 10%, #14142e, #080812 60%, #030308); }
.analytics-layout {
  position: relative;
  display: flex;
  height: 100%;
}
/* SIDEBAR */
.sidebar {
  position: relative;
  width: var(--sidebar-w);
  height: 100%;
  background: rgba(255,255,255,0.03);
  border-right: 1px solid var(--glass-border);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  z-index: calc(var(--z-glass) + 1);
}
.sidebar::before {
  content: '';
  position: absolute;
  inset: 0;
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  mask: linear-gradient(to right, black 85%, transparent);
  -webkit-mask: linear-gradient(to right, black 85%, transparent);
  pointer-events: none;
}
.logo {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.03em;
  padding: 0 4px 20px 4px;
  border-bottom: 1px solid var(--glass-border);
  margin-bottom: 20px;
}
.logo span { color: var(--accent-blue); }
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: default;
  transition: background 0.2s, color 0.2s;
}
.nav-item:hover { background: var(--glass-bg); color: var(--text-primary); }
.nav-item.active {
  background: rgba(107, 138, 255, 0.12);
  color: var(--accent-blue);
  border: 1px solid rgba(107, 138, 255, 0.15);
}
.nav-icon { width: 18px; height: 18px; border-radius: 4px; opacity: 0.7; flex-shrink: 0; }
.nav-item.active .nav-icon { opacity: 1; }
.nav-divider {
  height: 1px;
  background: var(--glass-border);
  margin: 12px 0;
}
/* MAIN */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.topbar {
  height: var(--topbar-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--content-p);
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}
.breadcrumb {
  font-size: 13px;
  color: var(--text-tertiary);
}
.breadcrumb strong { color: var(--text-primary); font-weight: 500; }
.topbar-actions {
  display: flex;
  gap: 10px;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
  border: 1px solid var(--glass-border-strong);
}
.topbar-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  cursor: default;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 14px;
}
/* CONTENT */
.content {
  flex: 1;
  padding: var(--content-p);
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto auto 1fr;
  gap: 16px;
  overflow-y: auto;
}
/* KPI ROW — spans 3 cols */
.kpi-row {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.kpi-card {
  position: relative;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.kpi-card .stat-value {
  font-size: 24px;
}
.kpi-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 2px;
}
/* CHARTS */
.chart-card {
  position: relative;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
}
.chart-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.chart-card .card-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}
.chart-body {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 6px;
  padding-bottom: 4px;
}
.bar {
  flex: 1;
  border-radius: 3px 3px 0 0;
  background: linear-gradient(to top, var(--accent-blue), rgba(107,138,255,0.3));
  min-height: 8px;
  transition: height 0.4s ease;
  position: relative;
}
.bar:nth-child(2n) { background: linear-gradient(to top, var(--accent-cyan), rgba(77,217,246,0.3)); }
.bar:nth-child(3n) { background: linear-gradient(to top, var(--accent-purple), rgba(167,139,250,0.3)); }
/* TABLE CARD — spans full width */
.table-card {
  grid-column: 1 / -1;
  position: relative;
  padding: 18px 0;
  display: flex;
  flex-direction: column;
}
.table-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px 12px 20px;
}
.table-card .card-title { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.table-card table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.table-card th {
  text-align: left;
  padding: 8px 20px;
  color: var(--text-tertiary);
  font-weight: 500;
  font-size: 11px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-bottom: 1px solid var(--glass-border);
}
.table-card td {
  padding: 10px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  color: var(--text-secondary);
}
.table-card td:first-child { color: var(--text-primary); font-weight: 500; }
.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 6px;
}
.status-online { background: var(--accent-green); }
.status-away { background: var(--accent-amber); }
.status-offline { background: var(--accent-rose); }
/* full-width KPI card variant */
.chart-card.colspan-2 {
  grid-column: span 2;
}
/* mini legend */
.legend {
  display: flex;
  gap: 14px;
  font-size: 11px;
  color: var(--text-tertiary);
}
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 6px; height: 6px; border-radius: 2px; }
</style>
</head>
<body>
<div class="space">
  <div class="ambient-layer"></div>
  <div class="noise-layer"></div>
  <div class="analytics-layout">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <div class="logo">styde<span>forge</span></div>
      <div class="nav-item active"><span class="nav-icon" style="background:var(--accent-blue)"></span>Overview</div>
      <div class="nav-item"><span class="nav-icon" style="background:var(--accent-cyan)"></span>Analytics</div>
      <div class="nav-item"><span class="nav-icon" style="background:var(--accent-purple)"></span>Reports</div>
      <div class="nav-item"><span class="nav-icon" style="background:var(--accent-amber)"></span>Alerts</div>
      <div class="nav-divider"></div>
      <div class="nav-item"><span class="nav-icon" style="background:var(--text-tertiary)"></span>Settings</div>
      <div class="nav-item" style="margin-top:auto"><span class="nav-icon" style="background:var(--text-tertiary)"></span>Logout</div>
    </div>
    <!-- MAIN -->
    <div class="main">
      <div class="topbar">
        <div class="breadcrumb">Dashboard / <strong>Overview</strong></div>
        <div class="topbar-actions">
          <div class="topbar-btn">&#8981;</div>
          <div class="topbar-btn">&#9881;</div>
          <div class="avatar"></div>
        </div>
      </div>
      <div class="content scrollable">
        <!-- KPI ROW -->
        <div class="kpi-row">
          <div class="kpi-card glass">
            <span class="stat-label">Total Revenue</span>
            <span class="stat-value text-gradient">$48,290</span>
            <div class="kpi-footer">
              <span class="stat-delta delta-positive">+12.4%</span>
              <span style="font-size:11px;color:var(--text-tertiary)">vs last month</span>
            </div>
          </div>
          <div class="kpi-card glass">
            <span class="stat-label">Active Users</span>
            <span class="stat-value text-gradient">2,481</span>
            <div class="kpi-footer">
              <span class="stat-delta delta-positive">+8.1%</span>
              <span style="font-size:11px;color:var(--text-tertiary)">vs last month</span>
            </div>
          </div>
          <div class="kpi-card glass">
            <span class="stat-label">Conversion</span>
            <span class="stat-value text-gradient">3.42%</span>
            <div class="kpi-footer">
              <span class="stat-delta delta-negative">-0.8%</span>
              <span style="font-size:11px;color:var(--text-tertiary)">vs last month</span>
            </div>
          </div>
          <div class="kpi-card glass">
            <span class="stat-label">Avg. Session</span>
            <span class="stat-value text-gradient">4m 32s</span>
            <div class="kpi-footer">
              <span class="stat-delta delta-positive">+6.3%</span>
              <span style="font-size:11px;color:var(--text-tertiary)">vs last month</span>
            </div>
          </div>
        </div>
        <!-- CHART 1: Bar chart (spans 2 cols) -->
        <div class="chart-card glass colspan-2">
          <div class="card-header">
            <span class="card-title">Weekly Sessions</span>
            <div class="legend">
              <span class="legend-item"><span class="legend-dot" style="background:var(--accent-blue)"></span>This week</span>
              <span class="legend-item"><span class="legend-dot" style="background:var(--accent-cyan)"></span>Last week</span>
            </div>
          </div>
          <div class="chart-body" style="height:120px">
            <div class="bar" style="height:45%"></div>
            <div class="bar" style="height:65%"></div>
            <div class="bar" style="height:52%"></div>
            <div class="bar" style="height:78%"></div>
            <div class="bar" style="height:61%"></div>
            <div class="bar" style="height:88%"></div>
            <div class="bar" style="height:73%"></div>
          </div>
        </div>
        <!-- CHART 2: Donut-like ring -->
        <div class="chart-card glass">
          <div class="card-header">
            <span class="card-title">Traffic Source</span>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:10px;padding:4px 0">
            <div style="display:flex;align-items:center;gap:10px">
              <span style="width:8px;height:8px;border-radius:2px;background:var(--accent-blue);flex-shrink:0"></span>
              <span style="font-size:12px;flex:1;color:var(--text-secondary)">Organic</span>
              <span style="font-size:13px;font-weight:500">42%</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <span style="width:8px;height:8px;border-radius:2px;background:var(--accent-cyan);flex-shrink:0"></span>
              <span style="font-size:12px;flex:1;color:var(--text-secondary)">Direct</span>
              <span style="font-size:13px;font-weight:500">28%</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <span style="width:8px;height:8px;border-radius:2px;background:var(--accent-purple);flex-shrink:0"></span>
              <span style="font-size:12px;flex:1;color:var(--text-secondary)">Referral</span>
              <span style="font-size:13px;font-weight:500">18%</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <span style="width:8px;height:8px;border-radius:2px;background:var(--accent-amber);flex-shrink:0"></span>
              <span style="font-size:12px;flex:1;color:var(--text-secondary)">Social</span>
              <span style="font-size:13px;font-weight:500">12%</span>
            </div>
          </div>
        </div>
        <!-- TABLE -->
        <div class="table-card glass">
          <div class="card-header">
            <span class="card-title">Recent Activity</span>
            <span style="font-size:11px;color:var(--accent-blue);cursor:default">View all</span>
          </div>
          <table>
            <thead><tr><th>User</th><th>Action</th><th>Project</th><th>Status</th><th>Time</th></tr></thead>
            <tbody>
              <tr><td>alex.c</td><td>Deployed pipeline</td><td>styde-forge</td><td><span class="status-dot status-online"></span>Completed</td><td>2m ago</td></tr>
              <tr><td>jordan.m</td><td>Created blueprint</td><td>precision-app</td><td><span class="status-dot status-online"></span>Completed</td><td>8m ago</td></tr>
              <tr><td>taylor.r</td><td>Review pending</td><td>dashboard-v2</td><td><span class="status-dot status-away"></span>In review</td><td>15m ago</td></tr>
              <tr><td>morgan.p</td><td>Submitted batch</td><td>forge-training</td><td><span class="status-dot status-online"></span>Completed</td><td>28m ago</td></tr>
              <tr><td>riley.s</td><td>Build failed</td><td>agent-core</td><td><span class="status-dot status-offline"></span>Failed</td><td>42m ago</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```
dashboard-metrics.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Metrics — Glass Spatial Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="glass-base.css">
<style>
:root {
  --metric-accent: var(--accent-cyan);
  --timeline-track: rgba(77, 217, 246, 0.15);
}
.space {
  background: radial-gradient(ellipse 55% 50% at 70% 20%, #0e1822, #080812 55%, #030308);
}
.metrics-layout {
  position: relative;
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 320px;
  grid-template-rows: auto 1fr;
  gap: 0;
}
/* TOP BAR */
.metrics-topbar {
  grid-column: 1 / -1;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.02);
  position: relative;
  z-index: 5;
}
.metrics-topbar .logo {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.03em;
}
.metrics-topbar .logo span { color: var(--metric-accent); }
.metrics-topbar .time-display {
  font-size: 13px;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}
.metrics-topbar .top-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}
.filter-pill {
  padding: 6px 14px;
  border-radius: 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  font-size: 12px;
  color: var(--text-secondary);
  cursor: default;
}
.filter-pill.active {
  background: rgba(77, 217, 246, 0.12);
  border-color: rgba(77, 217, 246, 0.2);
  color: var(--metric-accent);
}
/* PRIMARY METRICS AREA */
.primary-metrics {
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow-y: auto;
}
.headline-metric {
  position: relative;
  padding: 28px 32px;
  display: flex;
  align-items: center;
  gap: 40px;
}
.headline-value {
  font-size: 56px;
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1;
}
.headline-value .unit {
  font-size: 20px;
  font-weight: 500;
  color: var(--text-tertiary);
  margin-left: 6px;
}
.headline-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.headline-label {
  font-size: 12px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.headline-delta {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-green);
}
/* GAUGE GRID */
.gauge-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.gauge-card {
  position: relative;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}
.gauge-ring {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  position: relative;
  background: conic-gradient(var(--gauge-fill, var(--accent-cyan)) 0% var(--gauge-pct, 0%), rgba(255,255,255,0.06) var(--gauge-pct, 0%) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.gauge-ring::before {
  content: '';
  position: absolute;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #0a0a0f;
  border: 1px solid var(--glass-border);
}
.gauge-ring::after {
  content: attr(data-pct);
  position: absolute;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}
.gauge-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.gauge-value {
  font-size: 14px;
  font-weight: 600;
}
/* MINI TREND */
.mini-trend {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 20px;
}
.mini-trend span {
  width: 3px;
  border-radius: 2px;
  background: var(--metric-accent);
  opacity: 0.4;
}
.mini-trend span:nth-child(2n) { opacity: 0.6; }
.mini-trend span:nth-child(3n) { opacity: 0.8; }
.mini-trend span.active { opacity: 1; }
/* RIGHT PANEL — Timeline */
.timeline-panel {
  position: relative;
  padding: 24px;
  border-left: 1px solid var(--glass-border);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.timeline-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  backdrop-filter: blur(32px);
  -webkit-backdrop-filter: blur(32px);
  mask: linear-gradient(to left, black 90%, transparent);
  -webkit-mask: linear-gradient(to left, black 90%, transparent);
  pointer-events: none;
}
.timeline-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  position: relative;
}
.timeline-item {
  position: relative;
  padding-left: 20px;
  padding-bottom: 18px;
  border-left: 1px solid var(--glass-border);
}
.timeline-item:last-child { border-left-color: transparent; padding-bottom: 0; }
.timeline-item::before {
  content: '';
  position: absolute;
  left: -4px;
  top: 4px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--metric-accent);
  border: 2px solid #0a0a0f;
}
.timeline-item .tl-time {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}
.timeline-item .tl-event {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}
.timeline-item .tl-event strong { color: var(--text-primary); font-weight: 500; }
.timeline-item .tl-tag {
  display: inline-block;
  font-size: 10px;
  padding: 1px 8px;
  border-radius: 4px;
  margin-top: 4px;
  background: rgba(77, 217, 246, 0.1);
  color: var(--metric-accent);
}
/* metric cards row under headline */
.metric-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.metric-mini {
  position: relative;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.metric-mini .stat-value { font-size: 20px; }
</style>
</head>
<body>
<div class="space">
  <div class="ambient-layer"></div>
  <div class="noise-layer"></div>
  <div class="metrics-layout">
    <!-- TOP BAR -->
    <div class="metrics-topbar">
      <div class="logo">styde<span>metrics</span></div>
      <div style="display:flex;gap:8px">
        <span class="filter-pill active">Real-time</span>
        <span class="filter-pill">1h</span>
        <span class="filter-pill">24h</span>
        <span class="filter-pill">7d</span>
      </div>
      <div class="top-actions">
        <span class="time-display">Fri, 26 Jun 2026 — 20:27 UTC</span>
        <div class="avatar" style="width:30px;height:30px"></div>
      </div>
    </div>
    <!-- PRIMARY METRICS -->
    <div class="primary-metrics scrollable">
      <!-- Headline -->
      <div class="headline-metric glass-strong">
        <div>
          <div class="headline-value">94.7<span class="unit">%</span></div>
          <div style="margin-top:4px;display:flex;gap:16px">
            <span class="headline-label">Uptime SLA</span>
            <span class="headline-delta">+2.1%</span>
          </div>
        </div>
        <div style="flex:1;display:flex;gap:40px;justify-content:center">
          <div><span class="headline-label">Target</span><div style="font-size:24px;font-weight:600;margin-top:2px">99.9%</div></div>
          <div><span class="headline-label">Status</span><div style="font-size:24px;font-weight:600;margin-top:2px;color:var(--accent-green)">Healthy</div></div>
          <div><span class="headline-label">Region</span><div style="font-size:24px;font-weight:600;margin-top:2px">EU-WEST</div></div>
        </div>
      </div>
      <!-- Gauge grid -->
      <div class="gauge-grid">
        <div class="gauge-card glass" style="--gauge-fill: var(--accent-cyan); --gauge-pct: 78%;">
          <div class="gauge-ring" data-pct="78%" style="--gauge-pct: 78%"></div>
          <span class="gauge-label">CPU Usage</span>
          <span class="gauge-value" style="color:var(--accent-cyan)">2.4 GHz</span>
        </div>
        <div class="gauge-card glass" style="--gauge-fill: var(--accent-green); --gauge-pct: 62%;">
          <div class="gauge-ring" data-pct="62%" style="--gauge-pct: 62%"></div>
          <span class="gauge-label">Memory</span>
          <span class="gauge-value" style="color:var(--accent-green)">12.8 GB</span>
        </div>
        <div class="gauge-card glass" style="--gauge-fill: var(--accent-amber); --gauge-pct: 45%;">
          <div class="gauge-ring" data-pct="45%" style="--gauge-pct: 45%"></div>
          <span class="gauge-label">Disk IO</span>
          <span class="gauge-value" style="color:var(--accent-amber)">342 MB/s</span>
        </div>
      </div>
      <!-- Metric row -->
      <div class="metric-row">
        <div class="metric-mini glass">
          <span class="stat-label">Requests/sec</span>
          <span class="stat-value text-gradient">2,481</span>
          <div class="mini-trend">
            <span style="height:4px"></span><span style="height:8px"></span><span style="height:6px"></span>
            <span style="height:12px" class="active"></span><span style="height:10px"></span><span style="height:14px"></span>
            <span style="height:8px"></span>
          </div>
        </div>
        <div class="metric-mini glass">
          <span class="stat-label">P50 Latency</span>
          <span class="stat-value text-gradient">42ms</span>
          <div class="mini-trend">
            <span style="height:8px"></span><span style="height:6px"></span><span style="height:10px"></span>
            <span style="height:7px" class="active"></span><span style="height:5px"></span><span style="height:9px"></span>
            <span style="height:6px"></span>
          </div>
        </div>
        <div class="metric-mini glass">
          <span class="stat-label">Error Rate</span>
          <span class="stat-value text-gradient" style="color:var(--accent-green)">0.02%</span>
          <div class="mini-trend">
            <span style="height:3px"></span><span style="height:4px"></span><span style="height:2px"></span>
            <span style="height:3px" class="active"></span><span style="height:5px"></span><span style="height:3px"></span>
            <span style="height:4px"></span>
          </div>
        </div>
      </div>
    </div>
    <!-- TIMELINE PANEL -->
    <div class="timeline-panel">
      <div class="timeline-title">Event Timeline</div>
      <div class="timeline-item">
        <div class="tl-time">20:27:12</div>
        <div class="tl-event"><strong>Auto-scaling</strong> triggered — +2 nodes</div>
        <span class="tl-tag">scaling</span>
      </div>
      <div class="timeline-item">
        <div class="tl-time">20:24:08</div>
        <div class="tl-event"><strong>Deploy</strong> v2.14.3 promoted to production</div>
        <span class="tl-tag">deploy</span>
      </div>
      <div class="timeline-item">
        <div class="tl-time">20:19:44</div>
        <div class="tl-event"><strong>Alert</strong> CPU threshold warning cleared</div>
        <span class="tl-tag">alert</span>
      </div>
      <div class="timeline-item">
        <div class="tl-time">20:12:30</div>
        <div class="tl-event"><strong>Pipeline</strong> forge-batch-461 completed (12/12)</div>
        <span class="tl-tag">ci/cd</span>
      </div>
      <div class="timeline-item">
        <div class="tl-time">20:04:15</div>
        <div class="tl-event"><strong>Blueprint</strong> dashboard-v3 approved</div>
        <span class="tl-tag">design</span>
      </div>
      <div class="timeline-item" style="border-left-color:transparent">
        <div class="tl-time">19:58:02</div>
        <div class="tl-event"><strong>Backup</strong> database snapshot completed</div>
        <span class="tl-tag">system</span>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```
dashboard-monitor.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Monitor — Glass Spatial Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="glass-base.css">
<style>
:root {
  --monitor-accent: var(--accent-green);
  --monitor-bg-pulse: rgba(74, 222, 128, 0.04);
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
}
.space {
  background: radial-gradient(ellipse 50% 60% at 50% 50%, #0a1412, #060a08 60%, #020404);
}
.monitor-layout {
  position: relative;
  height: 100%;
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-rows: auto 1fr;
  gap: 0;
}
/* STATUS BAR */
.status-bar {
  grid-column: 1 / -1;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.015);
  z-index: 5;
}
.status-bar .logo-mono {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.06em;
  color: var(--text-secondary);
}
.status-bar .logo-mono span { color: var(--monitor-accent); }
.status-indicators {
  display: flex;
  gap: 20px;
  font-size: 11px;
  font-family: var(--font-mono);
}
.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-tertiary);
}
.status-indicator .pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}
.pulse-green { background: var(--accent-green); animation-delay: 0s; }
.pulse-cyan { background: var(--accent-cyan); animation-delay: 0.5s; }
.pulse-amber { background: var(--accent-amber); animation-delay: 1s; }
@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(74,222,128,0.4); }
  50% { opacity: 0.5; box-shadow: 0 0 0 4px rgba(74,222,128,0); }
}
/* SERVICE LIST */
.service-list {
  position: relative;
  padding: 16px;
  border-right: 1px solid var(--glass-border);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.service-list::before {
  content: '';
  position: absolute;
  inset: 0;
  backdrop-filter: blur(36px);
  -webkit-backdrop-filter: blur(36px);
  mask: linear-gradient(to right, black 88%, transparent);
  -webkit-mask: linear-gradient(to right, black 88%, transparent);
  pointer-events: none;
}
.service-list-title {
  font-size: 10px;
  font-family: var(--font-mono);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 8px 8px 4px 8px;
}
.service-item {
  padding: 10px 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: default;
  transition: background 0.15s;
  font-size: 12px;
}
.service-item:hover { background: var(--glass-bg); }
.service-item.active {
  background: rgba(74, 222, 128, 0.08);
  border: 1px solid rgba(74, 222, 128, 0.12);
}
.service-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.service-dot.up { background: var(--accent-green); }
.service-dot.warn { background: var(--accent-amber); }
.service-dot.down { background: var(--accent-rose); }
.service-name {
  flex: 1;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
}
.service-status-text {
  font-size: 10px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}
/* MAIN PANEL — Monitor Grid */
.monitor-main {
  padding: 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr 1fr;
  gap: 16px;
  overflow-y: auto;
}
/* LOG HEADER */
.log-header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.log-header h2 {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  letter-spacing: 0.02em;
}
.log-header h2 span { color: var(--monitor-accent); }
.log-count {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 4px 10px;
  border-radius: 6px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
}
/* LOG STREAM */
.log-stream {
  grid-column: 1 / -1;
  position: relative;
  padding: 12px 16px;
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.7;
  max-height: 200px;
  overflow-y: auto;
}
.log-line {
  display: flex;
  gap: 12px;
  opacity: 0.85;
}
.log-line:hover { opacity: 1; }
.log-time {
  color: var(--text-tertiary);
  flex-shrink: 0;
  width: 60px;
}
.log-level {
  width: 36px;
  flex-shrink: 0;
  font-weight: 500;
}
.log-level.info { color: var(--accent-cyan); }
.log-level.warn { color: var(--accent-amber); }
.log-level.error { color: var(--accent-rose); }
.log-level.ok { color: var(--accent-green); }
.log-msg {
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
/* MONITOR CARDS */
.monitor-card {
  position: relative;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.monitor-card .card-label {
  font-size: 10px;
  font-family: var(--font-mono);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.monitor-card .card-value {
  font-size: 32px;
  font-weight: 600;
  font-family: var(--font-mono);
  letter-spacing: -0.02em;
}
.monitor-card .card-bar {
  height: 4px;
  border-radius: 4px;
  background: rgba(255,255,255,0.06);
  overflow: hidden;
  margin-top: 4px;
}
.monitor-card .card-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}
.monitor-card .card-sub {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-tertiary);
}
/* Sparkline style mini-graph */
.sparkline {
  display: flex;
  gap: 2px;
  align-items: flex-end;
  height: 28px;
  margin-top: 4px;
}
.sparkline span {
  width: 4px;
  border-radius: 2px;
  background: var(--monitor-accent);
  opacity: 0.3;
  transition: opacity 0.2s, height 0.4s;
}
.sparkline span:nth-child(3n) { opacity: 0.5; }
.sparkline span:nth-child(5n) { opacity: 0.7; }
.sparkline span:last-child { opacity: 1; }
</style>
</head>
<body>
<div class="space">
  <div class="ambient-layer"></div>
  <div class="noise-layer"></div>
  <div class="monitor-layout">
    <!-- STATUS BAR -->
    <div class="status-bar">
      <div class="logo-mono">styde<span>monitor</span> v2.1</div>
      <div style="display:flex;gap:16px;align-items:center">
        <span style="font-family:var(--font-mono);font-size:11px;color:var(--text-tertiary)">cluster: forge-prod</span>
        <div class="status-indicators">
          <span class="status-indicator"><span class="pulse pulse-green"></span>12 nodes</span>
          <span class="status-indicator"><span class="pulse pulse-cyan"></span>4 pipelines</span>
          <span class="status-indicator"><span class="pulse pulse-amber"></span>2 alerts</span>
        </div>
      </div>
    </div>
    <!-- SERVICE LIST -->
    <div class="service-list">
      <div class="service-list-title">Services</div>
      <div class="service-item active">
        <span class="service-dot up"></span>
        <span class="service-name">forge-api</span>
        <span class="service-status-text">98ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">eval-engine</span>
        <span class="service-status-text">142ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">blueprint-svc</span>
        <span class="service-status-text">67ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot warn"></span>
        <span class="service-name">gateway-proxy</span>
        <span class="service-status-text">420ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">cron-dispatcher</span>
        <span class="service-status-text">12ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot down"></span>
        <span class="service-name">log-aggregator</span>
        <span class="service-status-text">offline</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">cache-redis</span>
        <span class="service-status-text">3ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">auth-provider</span>
        <span class="service-status-text">34ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot warn"></span>
        <span class="service-name">db-writer</span>
        <span class="service-status-text">210ms</span>
      </div>
      <div class="service-item">
        <span class="service-dot up"></span>
        <span class="service-name">agent-queue</span>
        <span class="service-status-text">8ms</span>
      </div>
    </div>
    <!-- MAIN PANEL -->
    <div class="monitor-main scrollable">
      <!-- Log header -->
      <div class="log-header">
        <h2>&#62; <span>live</span> stream</h2>
        <span class="log-count">142 events / 5m</span>
      </div>
      <!-- Log stream -->
      <div class="log-stream glass-sm">
        <div class="log-line"><span class="log-time">20:27:12</span><span class="log-level ok">OK</span><span class="log-msg">forge-api health check passed (98ms)</span></div>
        <div class="log-line"><span class="log-time">20:27:08</span><span class="log-level info">INFO</span><span class="log-msg">eval-engine processed batch #4612 in 4.2s</span></div>
        <div class="log-line"><span class="log-time">20:26:55</span><span class="log-level warn">WARN</span><span class="log-msg">gateway-proxy latency spike detected (420ms)</span></div>
        <div class="log-line"><span class="log-time">20:26:42</span><span class="log-level info">INFO</span><span class="log-msg">blueprint-svc cached 8 new personas</span></div>
        <div class="log-line"><span class="log-time">20:26:30</span><span class="log-level error">ERR</span><span class="log-msg">log-aggregator connection refused, retry 3/5</span></div>
        <div class="log-line"><span class="log-time">20:26:18</span><span class="log-level ok">OK</span><span class="log-msg">cron-dispatcher tick 12 jobs completed</span></div>
        <div class="log-line"><span class="log-time">20:26:04</span><span class="log-level info">INFO</span><span class="log-msg">db-writer checkpoint flushed (2.1GB WAL)</span></div>
      </div>
      <!-- Monitor card: CPU -->
      <div class="monitor-card glass">
        <span class="card-label">CPU Load</span>
        <div class="card-value" style="color:var(--accent-cyan)">37.2%</div>
        <div class="card-bar"><div class="card-bar-fill" style="width:37%;background:var(--accent-cyan)"></div></div>
        <div class="card-sub">avg across 12 cores</div>
        <div class="sparkline">
          <span style="height:8px"></span><span style="height:12px"></span><span style="height:6px"></span>
          <span style="height:14px"></span><span style="height:10px"></span><span style="height:18px"></span>
          <span style="height:12px"></span><span style="height:8px"></span><span style="height:16px"></span>
          <span style="height:14px"></span><span style="height:12px"></span><span style="height:10px"></span>
        </div>
      </div>
      <!-- Monitor card: Memory -->
      <div class="monitor-card glass">
        <span class="card-label">Memory Usage</span>
        <div class="card-value" style="color:var(--accent-green)">18.4 GB</div>
        <div class="card-bar"><div class="card-bar-fill" style="width:58%;background:var(--accent-green)"></div></div>
        <div class="card-sub">of 32 GB total — 56%</div>
        <div class="sparkline">
          <span style="height:14px"></span><span style="height:16px"></span><span style="height:12px"></span>
          <span style="height:18px"></span><span style="height:14px"></span><span style="height:20px"></span>
          <span style="height:16px"></span><span style="height:14px"></span><span style="height:18px"></span>
          <span style="height:16px"></span><span style="height:14px"></span><span style="height:12px"></span>
        </div>
      </div>
      <!-- Monitor card: Disk -->
      <div class="monitor-card glass">
        <span class="card-label">Disk Throughput</span>
        <div class="card-value" style="color:var(--accent-amber)">284 MB/s</div>
        <div class="card-bar"><div class="card-bar-fill" style="width:45%;background:var(--accent-amber)"></div></div>
        <div class="card-sub">read: 198 / write: 86 MB/s</div>
        <div class="sparkline">
          <span style="height:10px"></span><span style="height:14px"></span><span style="height:8px"></span>
          <span style="height:16px"></span><span style="height:12px"></span><span style="height:10px"></span>
          <span style="height:18px"></span><span style="height:14px"></span><span style="height:12px"></span>
          <span style="height:8px"></span><span style="height:14px"></span><span style="height:10px"></span>
        </div>
      </div>
      <!-- Monitor card: Network -->
      <div class="monitor-card glass">
        <span class="card-label">Network IO</span>
        <div class="card-value" style="color:var(--accent-purple)">1.2 Gbps</div>
        <div class="card-bar"><div class="card-bar-fill" style="width:40%;background:var(--accent-purple)"></div></div>
        <div class="card-sub">in: 780 / out: 440 Mbps</div>
        <div class="sparkline">
          <span style="height:6px"></span><span style="height:10px"></span><span style="height:14px"></span>
          <span style="height:8px"></span><span style="height:12px"></span><span style="height:16px"></span>
          <span style="height:10px"></span><span style="height:14px"></span><span style="height:12px"></span>
          <span style="height:18px"></span><span style="height:14px"></span><span style="height:10px"></span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```
File summary:
glass-base.css — shared stylesheet containing:
  Custom properties for glass, blur, shadows, z-planes, ambient lights, noise texture, accent colors, typography
  Base reset and body scaffolding
  `.glass`, `.glass-sm`, `.glass-strong` utility classes with consistent texture overlay (::before gradient)
  `.spatial-glow` pseudo-element glow ring
  `.text-gradient` utility
  `.stat-label`, `.stat-value`, `.stat-delta` KPI micro-components
  `.scrollable` custom scrollbar
  Z-plane layer system: `.depth-plane-1` through `.depth-plane-4`
dashboard-analytics.html — Analytics Overview:
  Left sidebar with navigation, glass border + depth mask
  4 KPI cards row (revenue, users, conversion, session)
  2-column bar chart card with legend
  Traffic source breakdown card
  Full-width activity table with status dots
  Layout: sidebar / topbar / scrollable grid content
dashboard-metrics.html — Real-time Metrics:
  Top bar with time filter pills (real-time, 1h, 24h, 7d)
  Headline glass-strong card with uptime SLA (94.7%)
  3 gauge rings (CPU, memory, disk IO) using conic-gradient
  3 mini-metric cards with sparkline bars
  Right timeline panel with event log + depth fade
dashboard-monitor.html — System Monitor:
  Status bar with animated pulse indicators
  Left service list (10 services with latency, status dots, active highlight)
  Live log stream with timestamp, level, message
  4 monitor cards (CPU, memory, disk, network) with bar fill + sparkline
  Monospace typography throughout, dark terminal-green accent
All three variants use glass-base.css via custom properties -- no duplicated glass-surface or depth-layer code. Open the HTML files in a browser (they expect glass-base.css in the same directory) to see the spatial glass interface.