<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Control Center</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg-deep: #0a0b0e;
    --bg-surface: #111316;
    --bg-card: #181b20;
    --bg-elevated: #1e2229;
    --border: #252a33;
    --border-glow: #c87a2c;
    --text-primary: #e8e6e3;
    --text-secondary: #8a8f99;
    --text-muted: #555a63;
    --accent-amber: #c87a2c;
    --accent-orange: #e8952e;
    --accent-glow: rgba(200,122,44,0.3);
    --accent-pulse: rgba(200,122,44,0.6);
    --success: #3bb873;
    --warning: #e8a82e;
    --danger: #d9534f;
    --info: #4a9eff;
    --glass: rgba(24,27,32,0.85);
    --radius: 12px;
    --radius-sm: 8px;
    --shadow: 0 4px 24px rgba(0,0,0,0.5);
    --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
  }
  html { font-size: 15px; }
  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg-deep);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
  }
  /* --- Animated Forge Background --- */
  .forge-bg {
    position: fixed; inset: 0; z-index: 0;
    background: radial-gradient(ellipse 80% 60% at 20% 90%, rgba(200,122,44,0.06) 0%, transparent 70%),
                radial-gradient(ellipse 60% 50% at 85% 20%, rgba(232,149,46,0.04) 0%, transparent 60%);
    pointer-events: none;
  }
  .forge-bg::after {
    content: ''; position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(200,122,44,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(200,122,44,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
  }
  /* --- Particles --- */
  .particles {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    overflow: hidden;
  }
  .particle {
    position: absolute; width: 3px; height: 3px; border-radius: 50%;
    background: var(--accent-amber); opacity: 0;
    animation: floatUp linear infinite;
  }
  @keyframes floatUp {
    0% { transform: translateY(100vh) scale(0); opacity: 0; }
    10% { opacity: 0.7; }
    90% { opacity: 0.4; }
    100% { transform: translateY(-10vh) scale(1); opacity: 0; }
  }
  /* --- Layout --- */
  .app { position: relative; z-index: 1; display: flex; flex-direction: column; min-height: 100vh; }
  /* --- Header --- */
  .header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; height: 60px;
    background: var(--glass); border-bottom: 1px solid var(--border);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    position: sticky; top: 0; z-index: 100;
  }
  .header-brand {
    display: flex; align-items: center; gap: 12px; text-decoration: none;
  }
  .header-logo {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, var(--accent-amber), var(--accent-orange));
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 18px; color: var(--bg-deep);
    box-shadow: 0 0 20px var(--accent-glow);
  }
  .header-title {
    font-size: 18px; font-weight: 600; color: var(--text-primary);
    letter-spacing: -0.3px;
  }
  .header-title span { color: var(--accent-amber); }
  .header-tag {
    font-size: 11px; color: var(--text-muted);
    background: var(--bg-elevated); padding: 2px 8px; border-radius: 4px;
    border: 1px solid var(--border); margin-left: 4px;
  }
  .header-actions { display: flex; align-items: center; gap: 16px; }
  .header-btn {
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--bg-elevated); border: 1px solid var(--border);
    color: var(--text-secondary); cursor: pointer; display: flex;
    align-items: center; justify-content: center; transition: var(--transition);
    position: relative;
  }
  .header-btn:hover { background: var(--bg-card); color: var(--text-primary); border-color: var(--accent-amber); }
  .notif-dot {
    position: absolute; top: 5px; right: 5px; width: 8px; height: 8px;
    background: var(--danger); border-radius: 50%;
    box-shadow: 0 0 8px rgba(217,83,79,0.6);
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
  .header-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #2a2f3a, var(--accent-amber));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; color: var(--text-primary);
    cursor: pointer; border: 2px solid transparent; transition: var(--transition);
  }
  .header-avatar:hover { border-color: var(--accent-amber); }
  /* --- Mobile hamburger --- */
  .hamburger { display: none; flex-direction: column; gap: 4px; cursor: pointer; padding: 8px; }
  .hamburger span {
    width: 22px; height: 2px; background: var(--text-secondary); border-radius: 2px;
    transition: var(--transition);
  }
  .hamburger.active span:nth-child(1) { transform: rotate(45deg) translate(4px,4px); }
  .hamburger.active span:nth-child(2) { opacity: 0; }
  .hamburger.active span:nth-child(3) { transform: rotate(-45deg) translate(4px,-4px); }
  /* --- Body wrapper --- */
  .body-wrap { display: flex; flex: 1; }
  /* --- Sidebar --- */
  .sidebar {
    width: 220px; min-width: 220px;
    background: var(--glass); border-right: 1px solid var(--border);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    padding: 16px 0; display: flex; flex-direction: column;
    transition: var(--transition);
  }
  .sidebar-nav { display: flex; flex-direction: column; gap: 2px; padding: 0 10px; }
  .nav-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 14px; border-radius: var(--radius-sm);
    color: var(--text-secondary); text-decoration: none;
    font-size: 14px; cursor: pointer; transition: var(--transition);
    position: relative;
  }
  .nav-item:hover { background: rgba(200,122,44,0.08); color: var(--text-primary); }
  .nav-item.active {
    background: rgba(200,122,44,0.14); color: var(--accent-amber);
    box-shadow: inset 3px 0 0 var(--accent-amber);
  }
  .nav-item svg { width: 18px; height: 18px; flex-shrink: 0; }
  .nav-item .badge {
    margin-left: auto; background: var(--accent-amber); color: var(--bg-deep);
    font-size: 11px; font-weight: 700; padding: 1px 7px; border-radius: 10px;
  }
  .sidebar-spacer { flex: 1; }
  .sidebar-footer {
    padding: 12px 16px; border-top: 1px solid var(--border);
    font-size: 12px; color: var(--text-muted);
  }
  .sidebar-footer .status-dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: var(--success); margin-right: 6px;
    box-shadow: 0 0 6px rgba(59,184,115,0.5);
  }
  /* --- Main content --- */
  .main {
    flex: 1; padding: 24px 28px; min-width: 0;
  }
  /* --- Breadcrumbs --- */
  .breadcrumbs {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: var(--text-muted); margin-bottom: 20px;
  }
  .breadcrumbs a { color: var(--text-muted); text-decoration: none; transition: var(--transition); }
  .breadcrumbs a:hover { color: var(--accent-amber); }
  .breadcrumbs .sep { color: var(--border); }
  .breadcrumbs .current { color: var(--text-secondary); }
  /* --- Page title --- */
  .page-title {
    font-size: 26px; font-weight: 700; margin-bottom: 6px;
    letter-spacing: -0.5px;
  }
  .page-subtitle { font-size: 14px; color: var(--text-secondary); margin-bottom: 28px; }
  /* --- Overview banner --- */
  .overview-banner {
    background: linear-gradient(135deg, rgba(200,122,44,0.12), rgba(232,149,46,0.06));
    border: 1px solid rgba(200,122,44,0.2); border-radius: var(--radius);
    padding: 20px 24px; margin-bottom: 28px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 12px;
  }
  .overview-banner h3 { font-size: 15px; font-weight: 600; color: var(--accent-amber); }
  .overview-banner p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
  .overview-banner .forge-btn {
    padding: 8px 20px; border-radius: var(--radius-sm);
    background: linear-gradient(135deg, var(--accent-amber), var(--accent-orange));
    border: none; color: var(--bg-deep); font-weight: 600; font-size: 13px;
    cursor: pointer; transition: var(--transition);
    box-shadow: 0 0 20px var(--accent-glow);
  }
  .overview-banner .forge-btn:hover {
    transform: translateY(-1px); box-shadow: 0 0 30px var(--accent-pulse);
  }
  /* --- Metrics grid --- */
  .metrics-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px;
  }
  .metric-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 18px 20px; transition: var(--transition); cursor: default;
    position: relative; overflow: hidden;
  }
  .metric-card:hover { border-color: rgba(200,122,44,0.3); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
  .metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-amber), transparent);
    opacity: 0; transition: var(--transition);
  }
  .metric-card:hover::before { opacity: 1; }
  .metric-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-value { font-size: 28px; font-weight: 700; margin: 6px 0 2px; letter-spacing: -0.5px; }
  .metric-change {
    font-size: 12px; display: flex; align-items: center; gap: 4px;
  }
  .metric-change.up { color: var(--success); }
  .metric-change.down { color: var(--danger); }
  .metric-icon {
    position: absolute; top: 14px; right: 14px; width: 36px; height: 36px;
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    background: rgba(200,122,44,0.1); color: var(--accent-amber);
  }
  /* --- Two-column section --- */
  .cols-2 {
    display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; margin-bottom: 28px;
  }
  /* --- Card generic --- */
  .card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
    overflow: hidden;
  }
  .card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px; border-bottom: 1px solid var(--border);
  }
  .card-header h3 { font-size: 14px; font-weight: 600; }
  .card-header .card-action {
    font-size: 12px; color: var(--accent-amber); cursor: pointer;
    background: none; border: none; padding: 4px 8px; border-radius: 4px;
    transition: var(--transition);
  }
  .card-header .card-action:hover { background: rgba(200,122,44,0.12); }
  .card-body { padding: 16px 20px; }
  /* --- Agent list --- */
  .agent-row {
    display: flex; align-items: center; gap: 12px; padding: 10px 0;
    border-bottom: 1px solid rgba(37,42,51,0.5); cursor: pointer; transition: var(--transition);
  }
  .agent-row:last-child { border-bottom: none; }
  .agent-row:hover { padding-left: 8px; }
  .agent-avatar {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px; flex-shrink: 0;
  }
  .agent-info { flex: 1; min-width: 0; }
  .agent-name { font-size: 13px; font-weight: 600; }
  .agent-desc { font-size: 11px; color: var(--text-muted); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .agent-status {
    font-size: 11px; display: flex; align-items: center; gap: 5px;
    white-space: nowrap;
  }
  .agent-status .dot {
    width: 7px; height: 7px; border-radius: 50%; display: inline-block;
  }
  .dot.green { background: var(--success); box-shadow: 0 0 6px rgba(59,184,115,0.5); }
  .dot.yellow { background: var(--warning); box-shadow: 0 0 6px rgba(232,168,46,0.5); }
  .dot.red { background: var(--danger); box-shadow: 0 0 6px rgba(217,83,79,0.5); }
  /* --- Activity feed --- */
  .activity-item {
    display: flex; gap: 12px; padding: 10px 0;
    border-bottom: 1px solid rgba(37,42,51,0.3);
  }
  .activity-item:last-child { border-bottom: none; }
  .activity-dot {
    width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0;
    background: var(--accent-amber); border: 2px solid var(--bg-deep);
    box-shadow: 0 0 0 1px var(--accent-amber);
  }
  .activity-dot.success { background: var(--success); box-shadow: 0 0 0 1px var(--success); }
  .activity-dot.warning { background: var(--warning); box-shadow: 0 0 0 1px var(--warning); }
  .activity-dot.info { background: var(--info); box-shadow: 0 0 0 1px var(--info); }
  .activity-text { flex: 1; font-size: 13px; }
  .activity-text strong { color: var(--text-primary); }
  .activity-time { font-size: 11px; color: var(--text-muted); white-space: nowrap; }
  /* --- GPU Monitor --- */
  .gpu-bar {
    display: flex; align-items: center; gap: 12px; margin-bottom: 12px;
  }
  .gpu-label { font-size: 12px; color: var(--text-secondary); width: 60px; flex-shrink: 0; }
  .gpu-track {
    flex: 1; height: 8px; background: var(--bg-elevated); border-radius: 4px;
    overflow: hidden; position: relative;
  }
  .gpu-fill {
    height: 100%; border-radius: 4px; transition: width 1.2s ease;
    background: linear-gradient(90deg, var(--accent-amber), var(--accent-orange));
    box-shadow: 0 0 8px var(--accent-glow);
  }
  .gpu-fill.mem { background: linear-gradient(90deg, #4a9eff, #6ab0ff); }
  .gpu-pct { font-size: 12px; font-weight: 600; width: 38px; text-align: right; }
  .gpu-temp {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 12px; color: var(--text-secondary); margin-top: 4px;
  }
  .gpu-temp .hot { color: var(--warning); }
  /* --- Collapsible panels --- */
  .collapsible { border-bottom: 1px solid var(--border); }
  .collapsible:last-child { border-bottom: none; }
  .collapsible-trigger {
    display: flex; align-items: center; gap: 8px;
    padding: 12px 20px; cursor: pointer; font-size: 13px; font-weight: 500;
    transition: var(--transition); background: none; border: none; width: 100%;
    text-align: left; color: var(--text-secondary);
  }
  .collapsible-trigger:hover { background: rgba(200,122,44,0.04); color: var(--text-primary); }
  .collapsible-trigger .arrow {
    margin-left: auto; transition: var(--transition); font-size: 10px;
  }
  .collapsible.open .collapsible-trigger .arrow { transform: rotate(180deg); }
  .collapsible-trigger .icon { width: 16px; height: 16px; flex-shrink: 0; }
  .collapsible-body {
    max-height: 0; overflow: hidden; transition: max-height 0.35s ease;
    padding: 0 20px;
  }
  .collapsible.open .collapsible-body {
    max-height: 200px; padding: 0 20px 14px;
  }
  .collapsible-body p { font-size: 13px; color: var(--text-muted); }
  /* --- Footer --- */
  .footer {
    border-top: 1px solid var(--border); padding: 16px 28px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 8px; font-size: 12px; color: var(--text-muted);
  }
  .footer-links { display: flex; gap: 20px; }
  .footer-links a { color: var(--text-muted); text-decoration: none; transition: var(--transition); }
  .footer-links a:hover { color: var(--accent-amber); }
  /* --- Responsive --- */
  @media (max-width: 1024px) {
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .cols-2 { grid-template-columns: 1fr; }
  }
  @media (max-width: 768px) {
    .header { padding: 0 16px; }
    .hamburger { display: flex; }
    .header-tag { display: none; }
    .sidebar {
      position: fixed; top: 60px; left: -260px; height: calc(100vh - 60px);
      z-index: 99; width: 240px;
      border-right: 1px solid var(--border);
      box-shadow: 4px 0 30px rgba(0,0,0,0.6);
    }
    .sidebar.open { left: 0; }
    .sidebar-overlay {
      position: fixed; inset: 0; top: 60px; background: rgba(0,0,0,0.5);
      z-index: 98; opacity: 0; pointer-events: none; transition: var(--transition);
    }
    .sidebar-overlay.open { opacity: 1; pointer-events: auto; }
    .main { padding: 16px; }
    .metrics-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
    .metric-value { font-size: 22px; }
    .overview-banner { flex-direction: column; align-items: flex-start; }
    .footer { flex-direction: column; align-items: center; text-align: center; }
  }
  @media (max-width: 480px) {
    .metrics-grid { grid-template-columns: 1fr; }
    .breadcrumbs { font-size: 12px; flex-wrap: wrap; }
    .page-title { font-size: 20px; }
  }
  /* --- Mini sparkline (CSS-only) --- */
  .sparkline {
    display: flex; align-items: flex-end; gap: 2px; height: 24px;
    margin-top: 8px;
  }
  .sparkline .bar {
    width: 5px; border-radius: 2px 2px 0 0;
    background: linear-gradient(to top, var(--accent-amber), var(--accent-orange));
    transition: height 0.5s ease;
  }
  .sparkline .bar:nth-child(1)  { height: 12px; }
  .sparkline .bar:nth-child(2)  { height: 18px; }
  .sparkline .bar:nth-child(3)  { height: 8px; }
  .sparkline .bar:nth-child(4)  { height: 22px; }
  .sparkline .bar:nth-child(5)  { height: 14px; }
  .sparkline .bar:nth-child(6)  { height: 26px; }
  .sparkline .bar:nth-child(7)  { height: 10px; }
  .sparkline .bar:nth-child(8)  { height: 20px; }
  .sparkline .bar:nth-child(9)  { height: 16px; }
  .sparkline .bar:nth-child(10) { height: 24px; }
  .sparkline .bar:nth-child(11) { height: 6px; }
  .sparkline .bar:nth-child(12) { height: 18px; }
  .sparkline .bar:nth-child(13) { height: 28px; }
  .sparkline .bar:nth-child(14) { height: 12px; }
  .sparkline .bar:nth-child(15) { height: 20px; }
  /* --- Utility --- */
  .mobile-only { display: none; }
  @media (max-width: 768px) { .mobile-only { display: block; } }
</style>
</head>
<body>
<div class="forge-bg"></div>
<div class="particles" id="particles"></div>
<div class="app">
  <header class="header">
    <div style="display:flex;align-items:center;gap:12px;">
      <div class="hamburger" id="hamburger" onclick="toggleSidebar()">
        <span></span><span></span><span></span>
      </div>
      <a class="header-brand" href="#">
        <div class="header-logo">F</div>
        <span class="header-title">styde<span>forge</span></span>
        <span class="header-tag">v2.4 · control</span>
      </a>
    </div>
    <div class="header-actions">
      <button class="header-btn" title="Notifications">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        <span class="notif-dot"></span>
      </button>
      <div class="header-avatar">PA</div>
    </div>
  </header>
  <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
  <div class="body-wrap">
    <aside class="sidebar" id="sidebar">
      <nav class="sidebar-nav">
        <a class="nav-item active" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          Dashboard
        </a>
        <a class="nav-item" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Agents
          <span class="badge">12</span>
        </a>
        <a class="nav-item" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          Pipelines
          <span class="badge">4</span>
        </a>
        <a class="nav-item" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><path d="M6 6h.01M6 18h.01"/></svg>
          GPU Farm
        </a>
        <a class="nav-item" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Blueprints
        </a>
        <a class="nav-item" href="#" onclick="return navClick(this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          Settings
        </a>
      </nav>
      <div class="sidebar-spacer"></div>
      <div class="sidebar-footer">
        <span class="status-dot"></span>
        All systems nominal · 6 nodes online
      </div>
    </aside>
    <main class="main">
      <div class="breadcrumbs">
        <a href="#">styde.se</a>
        <span class="sep">/</span>
        <a href="#">forge</a>
        <span class="sep">/</span>
        <span class="current">Control Center</span>
      </div>
      <h1 class="page-title">Forge Control Center</h1>
      <p class="page-subtitle">Monitor and orchestrate your agent swarm, pipelines, and GPU infrastructure from one place.</p>
      <div class="overview-banner">
        <div>
          <h3>Swarm forge is active</h3>
          <p>3 refinement pipelines running · 2 blueprints queued for batch training · 0 failures in last hour</p>
        </div>
        <button class="forge-btn" onclick="handleEvent('forge', this)">Open Forge Console</button>
      </div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div class="metric-label">Active Agents</div>
          <div class="metric-value">12</div>
          <div class="metric-change up">+3 from yesterday</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          </div>
          <div class="metric-label">Pipelines</div>
          <div class="metric-value">8</div>
          <div class="metric-change up">2 queued · 3 running</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><path d="M6 6h.01M6 18h.01"/></svg>
          </div>
          <div class="metric-label">GPU Utilization</div>
          <div class="metric-value">74%</div>
          <div class="metric-change up">3.2 TFLOPS avg</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="metric-label">Uptime</div>
          <div class="metric-value">94h 12m</div>
          <div class="metric-change up">99.97% reliability</div>
        </div>
      </div>
      <div class="cols-2">
        <div class="card">
          <div class="card-header">
            <h3>Agent Swarm</h3>
            <button class="card-action" onclick="handleEvent('view-all-agents', this)">View all</button>
          </div>
          <div class="card-body">
            <div class="agent-row" onclick="handleEvent('agent-detail', this)">
              <div class="agent-avatar" style="background:rgba(59,184,115,0.15);color:var(--success);">PE</div>
              <div class="agent-info">
                <div class="agent-name">Prompt Engineer</div>
                <div class="agent-desc">Refining plan prompts · batch 6/12</div>
              </div>
              <div class="agent-status"><span class="dot green"></span>online</div>
            </div>
            <div class="agent-row" onclick="handleEvent('agent-detail', this)">
              <div class="agent-avatar" style="background:rgba(74,158,255,0.15);color:var(--info);">SA</div>
              <div class="agent-info">
                <div class="agent-name">Styde Architect</div>
                <div class="agent-desc">Blueprint evaluation · tier 1 scoring</div>
              </div>
              <div class="agent-status"><span class="dot green"></span>online</div>
            </div>
            <div class="agent-row" onclick="handleEvent('agent-detail', this)">
              <div class="agent-avatar" style="background:rgba(232,168,46,0.15);color:var(--warning);">CV</div>
              <div class="agent-info">
                <div class="agent-name">Code Validator</div>
                <div class="agent-desc">Static analysis · 43 files pending</div>
              </div>
              <div class="agent-status"><span class="dot yellow"></span>busy</div>
            </div>
            <div class="agent-row" onclick="handleEvent('agent-detail', this)">
              <div class="agent-avatar" style="background:rgba(232,149,46,0.15);color:var(--accent-orange);">FM</div>
              <div class="agent-info">
                <div class="agent-name">Forge MCP</div>
                <div class="agent-desc">Tool bridge · orchestrator mode</div>
              </div>
              <div class="agent-status"><span class="dot green"></span>online</div>
            </div>
            <div class="agent-row" onclick="handleEvent('agent-detail', this)">
              <div class="agent-avatar" style="background:rgba(217,83,79,0.15);color:var(--danger);">MD</div>
              <div class="agent-info">
                <div class="agent-name">Model Deployer</div>
                <div class="agent-desc">Retrying deployment · attempt 3/5</div>
              </div>
              <div class="agent-status"><span class="dot red"></span>error</div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h3>Activity Feed</h3>
            <button class="card-action" onclick="handleEvent('clear-feed', this)">Clear</button>
          </div>
          <div class="card-body" style="max-height:300px;overflow-y:auto;">
            <div class="activity-item">
              <div class="activity-dot success"></div>
              <div class="activity-text"><strong>PE-v3</strong> completed prompt refinement cycle</div>
              <div class="activity-time">2m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot info"></div>
              <div class="activity-text"><strong>StydeArch</strong> submitted scores for 12 blueprints</div>
              <div class="activity-time">7m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot warning"></div>
              <div class="activity-text"><strong>CodeVal</strong> flagged 3 files with style violations</div>
              <div class="activity-time">11m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot success"></div>
              <div class="activity-text"><strong>MCP-Bridge</strong> connected to 4 remote workers</div>
              <div class="activity-time">18m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot" style="background:var(--accent-amber);box-shadow:0 0 0 1px var(--accent-amber);"></div>
              <div class="activity-text"><strong>ForgeCore</strong> spawned batch training job · 46 BPs</div>
              <div class="activity-time">25m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot info"></div>
              <div class="activity-text"><strong>GPU-02</strong> temperature normalized to 67C</div>
              <div class="activity-time">31m ago</div>
            </div>
            <div class="activity-item">
              <div class="activity-dot success"></div>
              <div class="activity-text"><strong>ModelDeploy</strong> published refined blueprint v2.4.1</div>
              <div class="activity-time">44m ago</div>
            </div>
          </div>
        </div>
      </div>
      <div class="card" style="margin-bottom:28px;">
        <div class="card-header">
          <h3>GPU Farm Monitor</h3>
          <button class="card-action" onclick="handleEvent('gpu-details', this)">Details</button>
        </div>
        <div class="card-body">
          <div class="gpu-bar">
            <span class="gpu-label">GPU-01</span>
            <div class="gpu-track"><div class="gpu-fill" style="width:82%;"></div></div>
            <span class="gpu-pct">82%</span>
          </div>
          <div style="display:flex;gap:20px;flex-wrap:wrap;">
            <span class="gpu-temp">Temp: <strong>71°C</strong></span>
            <span class="gpu-temp">Mem: 19.7 / 24 GB</span>
            <span class="gpu-temp">Power: <strong class="hot">285W</strong></span>
            <span class="gpu-temp">Util: 3.1 TFLOPS</span>
          </div>
          <div class="gpu-bar" style="margin-top:16px;">
            <span class="gpu-label">GPU-02</span>
            <div class="gpu-track"><div class="gpu-fill" style="width:56%;"></div></div>
            <span class="gpu-pct">56%</span>
          </div>
          <div style="display:flex;gap:20px;flex-wrap:wrap;">
            <span class="gpu-temp">Temp: <strong>67°C</strong></span>
            <span class="gpu-temp">Mem: 14.1 / 24 GB</span>
            <span class="gpu-temp">Power: 198W</span>
            <span class="gpu-temp">Util: 2.1 TFLOPS</span>
          </div>
          <div class="gpu-bar" style="margin-top:16px;">
            <span class="gpu-label">GPU-03</span>
            <div class="gpu-track"><div class="gpu-fill mem" style="width:91%;"></div></div>
            <span class="gpu-pct">91%</span>
          </div>
          <div style="display:flex;gap:20px;flex-wrap:wrap;">
            <span class="gpu-temp">Temp: <strong class="hot">79°C</strong></span>
            <span class="gpu-temp">Mem: 22.8 / 24 GB</span>
            <span class="gpu-temp">Power: <strong class="hot">312W</strong></span>
            <span class="gpu-temp">Util: 4.0 TFLOPS</span>
          </div>
          <div class="sparkline" style="margin-top:16px;">
            <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <span style="font-size:11px;color:var(--text-muted);margin-left:8px;">GPU util · last 15min</span>
          </div>
        </div>
      </div>
      <div class="card" style="margin-bottom:28px;">
        <div class="card-header">
          <h3>Quick Actions & Info</h3>
        </div>
        <div class="collapsible open" onclick="toggleCollapsible(this)">
          <button class="collapsible-trigger">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            Batch Training
            <span class="arrow">▲</span>
          </button>
          <div class="collapsible-body">
            <p>46 blueprints queued · 8 in priority tier 1 · estimated completion: 2h 14m</p>
          </div>
        </div>
        <div class="collapsible" onclick="toggleCollapsible(this)">
          <button class="collapsible-trigger">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
            Pipeline Orchestrator
            <span class="arrow">▲</span>
          </button>
          <div class="collapsible-body">
            <p>3 refinement pipelines active · agent delegation mode: round-robin · max 20 subs per batch</p>
          </div>
        </div>
        <div class="collapsible" onclick="toggleCollapsible(this)">
          <button class="collapsible-trigger">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Agent Factory
            <span class="arrow">▲</span>
          </button>
          <div class="collapsible-body">
            <p>Blueprint → spawn → eval → improve → production · 1.2s avg spawn time · 97% success rate</p>
          </div>
        </div>
      </div>
    </main>
  </div>
  <footer class="footer">
    <span>2026 styde.se · Forge v2.4.1 · Build 0x1A4F</span>
    <div class="footer-links">
      <a href="#" onclick="return navClick(this)">Documentation</a>
      <a href="#" onclick="return navClick(this)">API Status</a>
      <a href="#" onclick="return navClick(this)">System Logs</a>
      <a href="#" onclick="return navClick(this)">Privacy</a>
    </div>
  </footer>
</div>
<script>
  // Particle generator
  (function initParticles() {
    var container = document.getElementById('particles');
    for (var i = 0; i < 35; i++) {
      var p = document.createElement('div');
      p.className = 'particle';
      p.style.left = Math.random() * 100 + '%';
      p.style.width = (1 + Math.random() * 3) + 'px';
      p.style.height = p.style.width;
      p.style.animationDuration = (12 + Math.random() * 18) + 's';
      p.style.animationDelay = (Math.random() * 20) + 's';
      p.style.opacity = 0.3 + Math.random() * 0.5;
      container.appendChild(p);
    }
  })();
  // Sidebar toggle
  function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    var hamburger = document.getElementById('hamburger');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
    hamburger.classList.toggle('active');
  }
  // Nav click handler
  function navClick(el) {
    document.querySelectorAll('.nav-item').forEach(function(n) { n.classList.remove('active'); });
    el.classList.add('active');
    handleEvent('nav-' + (el.textContent || '').trim(), el);
    return false;
  }
  // Collapsible panels
  function toggleCollapsible(el) {
    el.classList.toggle('open');
    var arrow = el.querySelector('.arrow');
    if (arrow) arrow.textContent = el.classList.contains('open') ? '▲' : '▼';
  }
  // Generic event handler (prototype interactivity)
  function handleEvent(action, el) {
    var msg = 'Navigated to: ' + action;
    console.log(msg);
    el.style.outline = '2px solid var(--accent-amber)';
    el.style.outlineOffset = '2px';
    setTimeout(function() {
      el.style.outline = '';
      el.style.outlineOffset = '';
    }, 600);
  }
  // Auto-animate GPU bars on load (cosmetic)
  document.addEventListener('DOMContentLoaded', function() {
    var fills = document.querySelectorAll('.gpu-fill');
    fills.forEach(function(f) {
      var w = f.style.width;
      f.style.width = '0%';
      setTimeout(function() { f.style.width = w; }, 100);
    });
  });
  // Close sidebar on resize to desktop
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      var sidebar = document.getElementById('sidebar');
      var overlay = document.getElementById('sidebarOverlay');
      var hamburger = document.getElementById('hamburger');
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
      hamburger.classList.remove('active');
    }
  });
</script>
</body>
</html>