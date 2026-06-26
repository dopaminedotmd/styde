<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Precision Command Center</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg-deep: #080a0f;
  --bg-surface: #0d0f17;
  --bg-card: #11131e;
  --bg-card-hover: #161827;
  --border-subtle: rgba(255,255,255,0.04);
  --border-accent: rgba(99,102,241,0.25);
  --border-accent-strong: rgba(99,102,241,0.5);
  --accent: #6366f1;
  --accent-glow: #818cf8;
  --accent-dim: rgba(99,102,241,0.12);
  --green: #22c55e;
  --green-dim: rgba(34,197,94,0.12);
  --amber: #f59e0b;
  --amber-dim: rgba(245,158,11,0.12);
  --red: #ef4444;
  --red-dim: rgba(239,68,68,0.12);
  --cyan: #06b6d4;
  --cyan-dim: rgba(6,182,212,0.1);
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-tertiary: #64748b;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', system-ui, -apple-system, sans-serif;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --shadow-card: 0 1px 3px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.02) inset;
  --shadow-float: 0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.03) inset;
  --anim-slow: 0.4s cubic-bezier(0.16,1,0.3,1);
  --anim-fast: 0.2s cubic-bezier(0.16,1,0.3,1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg-deep);
  color: var(--text-primary);
  font-family: var(--sans);
  min-height: 100vh;
  overflow: hidden;
  position: relative;
}
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 20% 0%, rgba(99,102,241,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 80% 100%, rgba(6,182,212,0.04) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}
.grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 70%);
}
.app {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 1440px;
  margin: 0 auto;
  padding: 12px;
}
/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  flex-shrink: 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: linear-gradient(135deg, var(--accent), var(--cyan));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  box-shadow: 0 0 20px rgba(99,102,241,0.3);
}
.logo-text {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}
.logo-badge {
  font-size: 10px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 100px;
  background: var(--accent-dim);
  color: var(--accent-glow);
  border: 1px solid var(--border-accent);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.header-status {
  display: flex;
  align-items: center;
  gap: 20px;
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}
.status-dot.online { background: var(--green); box-shadow: 0 0 8px rgba(34,197,94,0.5); }
.status-dot.warning { background: var(--amber); box-shadow: 0 0 8px rgba(245,158,11,0.4); }
.status-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}
.status-value {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 500;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-icon {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all var(--anim-fast);
}
.btn-icon:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
  border-color: var(--border-accent);
}
.btn-primary {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  background: linear-gradient(135deg, var(--accent), #4f46e5);
  color: white;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--anim-fast);
  font-family: var(--sans);
}
.btn-primary:hover {
  box-shadow: 0 0 20px rgba(99,102,241,0.4);
  transform: translateY(-1px);
}
/* Layout */
.main {
  display: flex;
  gap: 12px;
  flex: 1;
  min-height: 0;
}
.sidebar {
  width: 200px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}
.right-panel {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
/* Cards */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all var(--anim-slow);
}
.card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-float);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-subtle);
}
.card-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
}
.card-badge {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 8px;
  border-radius: 100px;
  font-family: var(--mono);
}
.card-badge.green { background: var(--green-dim); color: var(--green); }
.card-badge.amber { background: var(--amber-dim); color: var(--amber); }
.card-badge.cyan { background: var(--cyan-dim); color: var(--cyan); }
.card-body {
  padding: 14px;
}
/* Sidebar Nav */
.nav-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
  padding: 8px 12px 4px;
  font-weight: 600;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--anim-fast);
  text-decoration: none;
}
.nav-item:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
}
.nav-item.active {
  background: var(--accent-dim);
  color: var(--accent-glow);
  border: 1px solid var(--border-accent);
}
.nav-item .nav-icon {
  width: 18px;
  text-align: center;
  font-size: 14px;
  flex-shrink: 0;
}
.nav-count {
  margin-left: auto;
  font-size: 11px;
  font-family: var(--mono);
  color: var(--text-tertiary);
  background: rgba(255,255,255,0.04);
  padding: 1px 6px;
  border-radius: 4px;
}
/* Agent List (sidebar bottom) */
.agent-mini-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.agent-mini {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  transition: background var(--anim-fast);
  cursor: pointer;
}
.agent-mini:hover {
  background: var(--bg-card-hover);
}
.agent-avatar {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}
.agent-avatar.r { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.agent-avatar.b { background: linear-gradient(135deg, #06b6d4, #0891b2); }
.agent-avatar.g { background: linear-gradient(135deg, #22c55e, #16a34a); }
.agent-avatar.a { background: linear-gradient(135deg, #f59e0b, #d97706); }
.agent-mini-info {
  flex: 1;
  min-width: 0;
}
.agent-mini-name {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}
.agent-mini-status {
  font-size: 10px;
  color: var(--text-tertiary);
}
.agent-mini-score {
  font-size: 11px;
  font-family: var(--mono);
  font-weight: 600;
}
.score-high { color: var(--green); }
.score-mid { color: var(--amber); }
.score-low { color: var(--red); }
/* Metric Cards Row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px;
  transition: all var(--anim-slow);
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  border-radius: 2px 2px 0 0;
}
.metric-card.m1::before { background: linear-gradient(90deg, var(--accent), var(--accent-glow)); }
.metric-card.m2::before { background: linear-gradient(90deg, var(--cyan), #22d3ee); }
.metric-card.m3::before { background: linear-gradient(90deg, var(--green), #4ade80); }
.metric-card.m4::before { background: linear-gradient(90deg, var(--amber), #fbbf24); }
.metric-card:hover {
  border-color: var(--border-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-float);
}
.metric-label {
  font-size: 11px;
  color: var(--text-tertiary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 4px;
}
.metric-value {
  font-size: 28px;
  font-weight: 700;
  font-family: var(--mono);
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
}
.metric-change {
  font-size: 11px;
  font-family: var(--mono);
  font-weight: 500;
  margin-top: 4px;
}
.metric-change.up { color: var(--green); }
.metric-change.down { color: var(--red); }
.metric-change.neutral { color: var(--text-tertiary); }
.metric-sub {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
}
/* Content split */
.content-split {
  display: flex;
  gap: 12px;
  flex: 1;
  min-height: 0;
}
.content-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}
.content-right {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
/* Activity Feed */
.activity-feed {
  flex: 1;
  overflow-y: auto;
}
.activity-item {
  display: flex;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.activity-item:last-child { border-bottom: none; }
.activity-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  flex-shrink: 0;
}
.activity-icon.success { background: var(--green-dim); color: var(--green); }
.activity-icon.fail { background: var(--red-dim); color: var(--red); }
.activity-icon.running { background: var(--cyan-dim); color: var(--cyan); }
.activity-icon.info { background: var(--accent-dim); color: var(--accent-glow); }
.activity-content {
  flex: 1;
  min-width: 0;
}
.activity-text {
  font-size: 12px;
  color: var(--text-primary);
  line-height: 1.4;
}
.activity-text strong { font-weight: 600; }
.activity-time {
  font-size: 10px;
  color: var(--text-tertiary);
  font-family: var(--mono);
  margin-top: 2px;
}
.activity-actor {
  font-size: 10px;
  color: var(--text-tertiary);
}
/* Right panel widgets */
.system-bar {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sys-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sys-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-secondary);
}
.sys-label span:last-child {
  font-family: var(--mono);
  color: var(--text-primary);
  font-weight: 500;
}
.sys-track {
  height: 4px;
  background: rgba(255,255,255,0.06);
  border-radius: 100px;
  overflow: hidden;
}
.sys-fill {
  height: 100%;
  border-radius: 100px;
  transition: width 0.6s ease;
}
.sys-fill.cpu { background: linear-gradient(90deg, var(--accent), var(--accent-glow)); }
.sys-fill.ram { background: linear-gradient(90deg, var(--cyan), #22d3ee); }
.sys-fill.gpu { background: linear-gradient(90deg, var(--green), #4ade80); }
.sys-fill.disk { background: linear-gradient(90deg, var(--amber), #fbbf24); }
/* GPU Details */
.gpu-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.gpu-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.gpu-header {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
}
.gpu-name { color: var(--text-primary); font-weight: 500; }
.gpu-temp { color: var(--text-secondary); font-family: var(--mono); }
.gpu-bars {
  display: flex;
  gap: 6px;
}
.gpu-bar-wrap {
  flex: 1;
}
.gpu-bar-label {
  font-size: 9px;
  color: var(--text-tertiary);
  margin-bottom: 2px;
}
.gpu-bar-track {
  height: 3px;
  background: rgba(255,255,255,0.06);
  border-radius: 100px;
  overflow: hidden;
}
.gpu-bar-fill {
  height: 100%;
  border-radius: 100px;
  transition: width 0.8s ease;
}
.gpu-bar-fill.util { background: var(--accent); }
.gpu-bar-fill.mem { background: var(--cyan); }
/* Queue Items */
.queue-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.queue-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border-subtle);
}
.queue-priority {
  width: 3px;
  height: 24px;
  border-radius: 2px;
  flex-shrink: 0;
}
.queue-priority.high { background: var(--red); }
.queue-priority.medium { background: var(--amber); }
.queue-priority.low { background: var(--text-tertiary); }
.queue-info {
  flex: 1;
  min-width: 0;
}
.queue-name {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}
.queue-detail {
  font-size: 10px;
  color: var(--text-tertiary);
}
.queue-eta {
  font-size: 10px;
  font-family: var(--mono);
  color: var(--text-secondary);
}
/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
/* Mini Sparkline area */
.spark-area {
  height: 24px;
  margin-top: 4px;
  opacity: 0.5;
}
/* Animation */
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.online.pulsing { animation: pulse-dot 2s ease-in-out infinite; }
@keyframes slideIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.activity-item { animation: slideIn 0.3s ease both; }
.activity-item:nth-child(1) { animation-delay: 0s; }
.activity-item:nth-child(2) { animation-delay: 0.05s; }
.activity-item:nth-child(3) { animation-delay: 0.1s; }
.activity-item:nth-child(4) { animation-delay: 0.15s; }
.activity-item:nth-child(5) { animation-delay: 0.2s; }
.activity-item:nth-child(6) { animation-delay: 0.25s; }
</style>
</head>
<body>
<div class="grid-bg"></div>
<div class="app">
  <header class="header">
    <div class="header-left">
      <div class="logo">
        <div class="logo-icon">SF</div>
        <span class="logo-text">Styde Forge</span>
        <span class="logo-badge">v3.0</span>
      </div>
    </div>
    <div class="header-status">
      <div class="status-item">
        <span class="status-dot online pulsing"></span>
        Pipeline
        <span class="status-value">Active</span>
      </div>
      <div class="status-item">
        Uptime
        <span class="status-value">12h 34m</span>
      </div>
      <div class="status-item">
        Agents
        <span class="status-value">14/23</span>
      </div>
      <div class="status-item">
        Queue
        <span class="status-value">5</span>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn-icon">&#8981;</button>
      <button class="btn-icon">&#9881;</button>
      <button class="btn-primary">+ New Task</button>
    </div>
  </header>
  <div class="main">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="card">
        <div class="card-header">
          <span class="card-title">Navigation</span>
        </div>
        <div class="card-body" style="padding:8px">
          <div class="nav-section">
            <div class="nav-item active">
              <span class="nav-icon">&#9632;</span> Dashboard
              <span class="nav-count">6</span>
            </div>
            <div class="nav-item">
              <span class="nav-icon">&#9679;</span> Agents
              <span class="nav-count">23</span>
            </div>
            <div class="nav-item">
              <span class="nav-icon">&#9673;</span> Blueprints
              <span class="nav-count">51</span>
            </div>
            <div class="nav-item">
              <span class="nav-icon">&#9660;</span> Evaluations
              <span class="nav-count">142</span>
            </div>
            <div class="nav-item">
              <span class="nav-icon">&#9675;</span> Production
              <span class="nav-count">7</span>
            </div>
            <div class="nav-item">
              <span class="nav-icon">&#9881;</span> Settings
            </div>
          </div>
        </div>
      </div>
      <div class="card" style="flex:1;min-height:0;display:flex;flex-direction:column">
        <div class="card-header">
          <span class="card-title">Active Agents</span>
          <span class="card-badge green">14 online</span>
        </div>
        <div class="card-body agent-mini-list" style="overflow-y:auto;flex:1">
          <div class="agent-mini">
            <div class="agent-avatar r">R</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Refinery Runner</div>
              <div class="agent-mini-status">Iter 3/5 &middot; 34s</div>
            </div>
            <span class="agent-mini-score score-high">94.6</span>
          </div>
          <div class="agent-mini">
            <div class="agent-avatar b">B</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Bento Architect</div>
              <div class="agent-mini-status">Iter 2/5 &middot; 28s</div>
            </div>
            <span class="agent-mini-score score-high">89.2</span>
          </div>
          <div class="agent-mini">
            <div class="agent-avatar g">G</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Glass Spatial</div>
              <div class="agent-mini-status">Iter 3/5 &middot; 41s</div>
            </div>
            <span class="agent-mini-score score-high">88.0</span>
          </div>
          <div class="agent-mini">
            <div class="agent-avatar a">A</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Data Dense Ops</div>
              <div class="agent-mini-status">Iter 2/5 &middot; 19s</div>
            </div>
            <span class="agent-mini-score score-mid">85.0</span>
          </div>
          <div class="agent-mini">
            <div class="agent-avatar r">M</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Mockup Curator</div>
              <div class="agent-mini-status">Iter 1/5 &middot; 22s</div>
            </div>
            <span class="agent-mini-score score-mid">82.2</span>
          </div>
          <div class="agent-mini">
            <div class="agent-avatar b">H</div>
            <div class="agent-mini-info">
              <div class="agent-mini-name">Holo Futurist</div>
              <div class="agent-mini-status">Iter 6/5 &middot; 52s</div>
            </div>
            <span class="agent-mini-score score-mid">69.4</span>
          </div>
        </div>
      </div>
    </aside>
    <!-- Main Content -->
    <div class="content">
      <!-- Metrics Row -->
      <div class="metrics-row">
        <div class="metric-card m1">
          <div class="metric-label">Composite Score</div>
          <div class="metric-value">85.3</div>
          <div class="metric-change up">+2.4 &uarr;</div>
          <div class="metric-sub">Across 142 evals</div>
        </div>
        <div class="metric-card m2">
          <div class="metric-label">Agents Trained</div>
          <div class="metric-value">23</div>
          <div class="metric-change up">+4 this batch</div>
          <div class="metric-sub">7 in production</div>
        </div>
        <div class="metric-card m3">
          <div class="metric-label">Throughput</div>
          <div class="metric-value">12.4</div>
          <div class="metric-change up">+18%</div>
          <div class="metric-sub">Iterations / hour</div>
        </div>
        <div class="metric-card m4">
          <div class="metric-label">Avg Response</div>
          <div class="metric-value">2.3s</div>
          <div class="metric-change down">-0.4s</div>
          <div class="metric-sub">P95: 4.1s</div>
        </div>
      </div>
      <!-- Content Split -->
      <div class="content-split">
        <div class="content-left">
          <!-- Activity Feed -->
          <div class="card" style="flex:1;display:flex;flex-direction:column;min-height:0">
            <div class="card-header">
              <span class="card-title">Activity Feed</span>
              <span class="card-badge cyan">live</span>
            </div>
            <div class="card-body activity-feed" style="flex:1;padding:4px 14px">
              <div class="activity-item">
                <div class="activity-icon success">&#10003;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>desktop-mockup-artist</strong> archived at score 94.6</div>
                  <div class="activity-time">14:32:17 &middot; <span class="activity-actor">Teacher Review</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon running">&#9654;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>editorial-minimal-designer</strong> iter 3/10 — generating</div>
                  <div class="activity-time">14:31:58 &middot; <span class="activity-actor">Spawn Agent</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon info">&#9432;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>glass-spatial-designer</strong> S:85 J:90 C:88.0 — passing gate</div>
                  <div class="activity-time">14:31:42 &middot; <span class="activity-actor">Eval Complete</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon fail">&#10007;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>neo-brutalist-designer</strong> S:34 J:0 C:13.6 — retry</div>
                  <div class="activity-time">14:31:30 &middot; <span class="activity-actor">Eval Failed</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon success">&#10003;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>clay-soft-designer</strong> S:82 J:95 C:89.8 — promoted</div>
                  <div class="activity-time">14:31:12 &middot; <span class="activity-actor">Production Gate</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon running">&#9654;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>terminal-purist-designer</strong> S:85 J:91 C:88.6 — production ready</div>
                  <div class="activity-time">14:30:55 &middot; <span class="activity-actor">Teacher Review</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon info">&#9432;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>data-dense-ops</strong> iter 4/10 — eval pending</div>
                  <div class="activity-time">14:30:38 &middot; <span class="activity-actor">Spawn Agent</span></div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon success">&#10003;</div>
                <div class="activity-content">
                  <div class="activity-text"><strong>secrets-hardening-auditor</strong> S:86 J:91 C:89.0</div>
                  <div class="activity-time">14:30:20 &middot; <span class="activity-actor">Eval Complete</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="content-right">
          <!-- System Health -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">System Health</span>
              <span class="card-badge green">nominal</span>
            </div>
            <div class="card-body system-bar">
              <div class="sys-item">
                <div class="sys-label">
                  <span>CPU</span>
                  <span>62% &middot; 4.8 GHz / 8 cores</span>
                </div>
                <div class="sys-track">
                  <div class="sys-fill cpu" style="width:62%"></div>
                </div>
              </div>
              <div class="sys-item">
                <div class="sys-label">
                  <span>RAM</span>
                  <span>21.4 / 32.0 GB</span>
                </div>
                <div class="sys-track">
                  <div class="sys-fill ram" style="width:67%"></div>
                </div>
              </div>
              <div class="sys-item">
                <div class="sys-label">
                  <span>GPU</span>
                  <span>58% &middot; 12.2 GB VRAM</span>
                </div>
                <div class="sys-track">
                  <div class="sys-fill gpu" style="width:58%"></div>
                </div>
              </div>
              <div class="sys-item">
                <div class="sys-label">
                  <span>Disk</span>
                  <span>312 / 2.0 TB used</span>
                </div>
                <div class="sys-track">
                  <div class="sys-fill disk" style="width:17%"></div>
                </div>
              </div>
            </div>
          </div>
          <!-- GPU Details -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">GPU Details</span>
              <span class="card-badge cyan">NVIDIA RTX</span>
            </div>
            <div class="card-body gpu-list">
              <div class="gpu-item">
                <div class="gpu-header">
                  <span class="gpu-name">GPU 0 &mdash; RTX 4090</span>
                  <span class="gpu-temp">67&deg;C</span>
                </div>
                <div class="gpu-bars">
                  <div class="gpu-bar-wrap">
                    <div class="gpu-bar-label">Util</div>
                    <div class="gpu-bar-track"><div class="gpu-bar-fill util" style="width:58%"></div></div>
                  </div>
                  <div class="gpu-bar-wrap">
                    <div class="gpu-bar-label">Memory</div>
                    <div class="gpu-bar-track"><div class="gpu-bar-fill mem" style="width:73%"></div></div>
                  </div>
                </div>
              </div>
              <div class="gpu-item">
                <div class="gpu-header">
                  <span class="gpu-name">GPU 1 &mdash; RTX 4090</span>
                  <span class="gpu-temp">54&deg;C</span>
                </div>
                <div class="gpu-bars">
                  <div class="gpu-bar-wrap">
                    <div class="gpu-bar-label">Util</div>
                    <div class="gpu-bar-track"><div class="gpu-bar-fill util" style="width:23%"></div></div>
                  </div>
                  <div class="gpu-bar-wrap">
                    <div class="gpu-bar-label">Memory</div>
                    <div class="gpu-bar-track"><div class="gpu-bar-fill mem" style="width:34%"></div></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Queue -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Job Queue</span>
              <span class="card-badge amber">5 pending</span>
            </div>
            <div class="card-body queue-list">
              <div class="queue-item">
                <div class="queue-priority high"></div>
                <div class="queue-info">
                  <div class="queue-name">holographic-futurist</div>
                  <div class="queue-detail">Iter 7/5 &middot; Improve</div>
                </div>
                <span class="queue-eta">2:14</span>
              </div>
              <div class="queue-item">
                <div class="queue-priority medium"></div>
                <div class="queue-info">
                  <div class="queue-name">organic-fluid</div>
                  <div class="queue-detail">Iter 8/5 &middot; Eval</div>
                </div>
                <span class="queue-eta">4:32</span>
              </div>
              <div class="queue-item">
                <div class="queue-priority medium"></div>
                <div class="queue-info">
                  <div class="queue-name">mockup-diversity-enforcer</div>
                  <div class="queue-detail">Iter 1/5 &middot; Spawn</div>
                </div>
                <span class="queue-eta">6:10</span>
              </div>
              <div class="queue-item">
                <div class="queue-priority low"></div>
                <div class="queue-info">
                  <div class="queue-name">wcag-accessibility</div>
                  <div class="queue-detail">Iter 1/5 &middot; Spawn</div>
                </div>
                <span class="queue-eta">8:45</span>
              </div>
              <div class="queue-item">
                <div class="queue-priority low"></div>
                <div class="queue-info">
                  <div class="queue-name">color-palette-originator</div>
                  <div class="queue-detail">Iter 1/5 &middot; Spawn</div>
                </div>
                <span class="queue-eta">11:20</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', function() {
      navItems.forEach(i => i.classList.remove('active'));
      this.classList.add('active');
    });
  });
  const gpuFills = document.querySelectorAll('.gpu-bar-fill');
  const sysFills = document.querySelectorAll('.sys-fill');
  setInterval(() => {
    gpuFills.forEach(el => {
      const base = parseFloat(el.style.width);
      const drift = (Math.random() - 0.5) * 6;
      const next = Math.max(5, Math.min(95, base + drift));
      el.style.width = next.toFixed(1) + '%';
    });
    sysFills.forEach(el => {
      const base = parseFloat(el.style.width);
      const drift = (Math.random() - 0.5) * 3;
      const next = Math.max(10, Math.min(95, base + drift));
      el.style.width = next.toFixed(1) + '%';
    });
  }, 3000);
  const temps = document.querySelectorAll('.gpu-temp');
  setInterval(() => {
    temps.forEach(el => {
      const base = parseInt(el.textContent);
      const drift = Math.floor((Math.random() - 0.5) * 4);
      const next = Math.max(40, Math.min(85, base + drift));
      el.textContent = next + '\u00B0C';
    });
  }, 4000);
  const statusValues = document.querySelectorAll('.status-value');
  setInterval(() => {
    const uptimeEl = statusValues[0];
    if (uptimeEl && uptimeEl.textContent.includes('h')) {
      const parts = uptimeEl.textContent.match(/(\d+)h\s+(\d+)m/);
      if (parts) {
        let h = parseInt(parts[1]), m = parseInt(parts[2]) + 1;
        if (m >= 60) { h += 1; m = 0; }
        uptimeEl.textContent = h + 'h ' + m.toString().padStart(2, '0') + 'm';
      }
    }
  }, 60000);
  const queueEtas = document.querySelectorAll('.queue-eta');
  setInterval(() => {
    queueEtas.forEach(el => {
      const parts = el.textContent.match(/(\d+):(\d+)/);
      if (parts) {
        let m = parseInt(parts[1]), s = parseInt(parts[2]) - 1;
        if (s < 0) { m -= 1; s = 59; }
        if (m < 0) { m = 0; s = 0; }
        el.textContent = m + ':' + s.toString().padStart(2, '0');
      }
    });
  }, 1000);
  const now = new Date();
  const timeStr = now.getHours().toString().padStart(2, '0') + ':' +
                  now.getMinutes().toString().padStart(2, '0') + ':00';
  const firstActivityTime = document.querySelector('.activity-time');
  if (firstActivityTime) {
    const timeParts = firstActivityTime.textContent.match(/(\d+:\d+:\d+)/);
    if (timeParts) {
      const secs = parseInt(timeParts[1].split(':')[2]);
      let currentSec = secs;
      setInterval(() => {
        currentSec = (currentSec + 1) % 60;
        document.querySelectorAll('.activity-time').forEach((el, i) => {
          const match = el.textContent.match(/(\d+:\d+):\d+/);
          if (match) {
            const newTime = match[1] + ':' + (currentSec - i).toString().padStart(2, '0');
            el.innerHTML = el.innerHTML.replace(/(\d+:\d+:\d+)/, newTime);
          }
        });
      }, 1000);
    }
  }
});
</script>
</body>
</html>