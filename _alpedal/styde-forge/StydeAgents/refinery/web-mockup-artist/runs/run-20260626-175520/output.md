```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Command Center</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d0d0d; --panel:#161616; --steel:#2a2a2a;
  --amber:#ff7b00; --copper:#b87333; --brass:#cfa144;
  --glow:#ff9500; --text:#d4c9a8; --dim:#6b5e4a;
  --border:#3a3024; --rivet:#4a3f2e; --danger:#cc3333;
  --safe:#44bb66; --font:'JetBrains Mono','Fira Code',monospace;
  --hex:#1a1a1a;
}
html{font-size:14px}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--font);
  min-height:100vh;
  background-image:
    repeating-linear-gradient(60deg,transparent,transparent 30px,var(--hex) 30px,var(--hex) 31px),
    repeating-linear-gradient(-60deg,transparent,transparent 30px,var(--hex) 30px,var(--hex) 31px);
  background-size:52px 90px;
}
.wrap{max-width:1400px;margin:0 auto;padding:0 20px}
/* HEADER */
header{
  background:linear-gradient(180deg,#1c180e 0%,var(--panel) 100%);
  border-bottom:2px solid var(--border);
  padding:12px 0;
  position:relative;
  box-shadow:0 0 30px rgba(255,123,0,0.05);
}
header::after{
  content:'';position:absolute;bottom:-2px;left:0;right:0;
  height:2px;
  background:linear-gradient(90deg,transparent 0%,var(--amber) 20%,var(--brass) 50%,var(--amber) 80%,transparent 100%);
  opacity:0.4;
}
.header-inner{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.logo{display:flex;align-items:center;gap:14px}
.logo-icon{
  width:44px;height:44px;
  background:linear-gradient(135deg,var(--amber),var(--copper));
  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
  display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:20px;color:#0d0d0d;text-shadow:0 1px 2px rgba(255,255,255,0.2);
}
.logo-text{font-size:20px;font-weight:700;color:var(--brass);letter-spacing:2px;text-transform:uppercase}
.logo-text span{color:var(--amber)}
.subtitle{font-size:10px;color:var(--dim);letter-spacing:3px;text-transform:uppercase;margin-top:2px}
.header-right{display:flex;align-items:center;gap:16px}
.status-badge{
  display:flex;align-items:center;gap:6px;
  padding:4px 12px;border:1px solid var(--border);
  background:rgba(255,123,0,0.06);border-radius:2px;
  font-size:10px;text-transform:uppercase;letter-spacing:1px;
}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--safe);box-shadow:0 0 8px rgba(68,187,102,0.5);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:0.4}}
/* NAV */
nav{
  background:var(--panel);border-bottom:1px solid var(--border);
  padding:0;position:sticky;top:0;z-index:100;
}
.nav-inner{display:flex;align-items:center;gap:0;position:relative}
.nav-item{
  padding:10px 20px;font-size:11px;text-transform:uppercase;letter-spacing:1.5px;
  color:var(--dim);cursor:pointer;border-right:1px solid var(--border);
  transition:color 0.2s,background 0.2s;position:relative;user-select:none;
}
.nav-item:hover{color:var(--amber);background:rgba(255,123,0,0.04)}
.nav-item.active{color:var(--brass);background:rgba(255,123,0,0.06)}
.nav-item.active::after{
  content:'';position:absolute;bottom:-1px;left:10%;right:10%;
  height:2px;background:var(--amber);border-radius:1px;
}
.nav-item.system{color:var(--amber);font-weight:500}
.hamburger{display:none;flex-direction:column;gap:4px;cursor:pointer;padding:12px 16px;margin-left:auto}
.hamburger span{width:22px;height:2px;background:var(--dim);border-radius:1px;transition:all 0.3s}
/* BREADCRUMB */
.breadcrumb{padding:8px 0;font-size:10px;color:var(--dim);letter-spacing:0.5px}
.breadcrumb a{color:var(--dim);text-decoration:none}
.breadcrumb a:hover{color:var(--amber)}
.breadcrumb .sep{margin:0 6px;color:var(--border)}
.breadcrumb .current{color:var(--brass)}
/* MAIN LAYOUT */
.main-grid{display:grid;grid-template-columns:300px 1fr 280px;gap:16px;padding:16px 0 40px}
@media(max-width:1100px){.main-grid{grid-template-columns:1fr;grid-template-rows:auto auto auto}}
/* PANEL BASE */
.panel{
  background:var(--panel);
  border:1px solid var(--border);
  position:relative;
  padding:16px;
}
.panel::before{
  content:'';position:absolute;top:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,transparent 20%,var(--brass) 50%,transparent 80%);
  opacity:0.3;
}
.panel-title{
  font-size:10px;text-transform:uppercase;letter-spacing:2px;
  color:var(--brass);margin-bottom:14px;padding-bottom:8px;
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
}
.panel-title .count{
  font-size:10px;background:rgba(255,123,0,0.1);
  padding:0 6px;border:1px solid var(--border);border-radius:2px;color:var(--dim);
}
/* LEFT SIDEBAR */
.sidebar .panel+.panel{margin-top:12px}
.agent-list{display:flex;flex-direction:column;gap:6px}
.agent-card{
  display:flex;align-items:center;gap:10px;
  padding:8px 10px;border:1px solid var(--border);
  cursor:pointer;transition:all 0.2s;position:relative;
}
.agent-card:hover{border-color:var(--amber);background:rgba(255,123,0,0.03)}
.agent-card.online{border-left:2px solid var(--safe)}
.agent-card.busy{border-left:2px solid var(--amber)}
.agent-card.error{border-left:2px solid var(--danger)}
.agent-indicator{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.agent-indicator.online{background:var(--safe);box-shadow:0 0 6px rgba(68,187,102,0.4)}
.agent-indicator.busy{background:var(--amber);animation:pulse-dot 1s ease-in-out infinite}
.agent-indicator.error{background:var(--danger);box-shadow:0 0 6px rgba(204,51,51,0.4)}
.agent-info{flex:1;min-width:0}
.agent-name{font-size:11px;font-weight:500;color:var(--text)}
.agent-status{font-size:9px;text-transform:uppercase;letter-spacing:1px}
.agent-status.online{color:var(--safe)}
.agent-status.busy{color:var(--amber)}
.agent-status.error{color:var(--danger)}
.agent-tasks{font-size:9px;color:var(--dim)}
/* CENTER - SYSTEM OVERVIEW */
.system-header{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px}
.metric-card{
  padding:12px;border:1px solid var(--border);text-align:center;
  background:linear-gradient(180deg,rgba(255,123,0,0.02) 0%,transparent 100%);
  position:relative;overflow:hidden;
}
.metric-card::after{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent 20%,var(--brass) 50%,transparent 80%);
  opacity:0.2;
}
.metric-value{font-size:28px;font-weight:700;color:var(--brass);line-height:1}
.metric-label{font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:var(--dim);margin-top:6px}
.metric-change{font-size:9px;margin-top:4px}
.metric-change.up{color:var(--safe)}
.metric-change.down{color:var(--danger)}
/* GAUGE */
.gauge-container{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.gauge{
  padding:12px;border:1px solid var(--border);text-align:center;
}
.gauge-visual{position:relative;width:100px;height:56px;margin:0 auto 8px;overflow:hidden}
.gauge-visual::before{
  content:'';position:absolute;top:0;left:0;right:0;height:100%;
  border-radius:100px 100px 0 0;border:3px solid var(--border);
  border-bottom:none;clip-path:inset(0 0 40% 0);
}
.gauge-fill{
  position:absolute;top:0;left:0;right:0;height:100%;
  border-radius:100px 100px 0 0;border:3px solid var(--amber);
  border-bottom:none;clip-path:inset(0 0 40% 0);
  transform-origin:bottom center;
  transform:rotate(var(--gauge-deg,0deg));
  transition:transform 1s ease;
}
.gauge-label{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:var(--dim)}
.gauge-value{font-size:18px;font-weight:700;color:var(--brass)}
/* ACTIVITY FEED */
.activity-feed{display:flex;flex-direction:column;gap:4px;max-height:260px;overflow-y:auto}
.activity-feed::-webkit-scrollbar{width:3px}
.activity-feed::-webkit-scrollbar-track{background:var(--bg)}
.activity-feed::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.activity-item{
  padding:8px;border-left:2px solid var(--border);
  font-size:10px;line-height:1.4;
}
.activity-item .time{color:var(--dim);font-size:9px}
.activity-item .msg{color:var(--text)}
.activity-item .hl{color:var(--amber)}
.activity-item.new{border-left-color:var(--amber);background:rgba(255,123,0,0.03)}
/* RIGHT SIDEBAR - GPU MONITOR */
.gpu-monitor{display:flex;flex-direction:column;gap:10px}
.gpu-card{padding:10px;border:1px solid var(--border)}
.gpu-header{display:flex;justify-content:space-between;font-size:10px;margin-bottom:6px}
.gpu-name{color:var(--brass);font-weight:500}
.gpu-temp{color:var(--dim)}
.bar-track{height:4px;background:var(--bg);border-radius:2px;overflow:hidden;margin:4px 0}
.bar-fill{height:100%;border-radius:2px;transition:width 0.5s}
.bar-fill.usage{background:linear-gradient(90deg,var(--amber),var(--brass))}
.bar-fill.mem{background:linear-gradient(90deg,var(--copper),var(--amber))}
.bar-fill.vram{background:var(--brass)}
.gpu-stats{display:flex;justify-content:space-between;font-size:9px;color:var(--dim)}
/* COLLAPSIBLE */
.collapse-trigger{cursor:pointer;user-select:none}
.collapse-trigger::before{content:'\25be ';color:var(--dim)}
.collapse-trigger.collapsed::before{content:'\25b8 '}
.collapse-target{overflow:hidden;transition:max-height 0.3s ease}
.collapse-target.hidden{max-height:0 !important;padding-top:0 !important;padding-bottom:0 !important;border:none}
/* FOOTER */
footer{
  border-top:1px solid var(--border);
  padding:24px 0;margin-top:16px;
}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px}
.footer-col h4{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:var(--brass);margin-bottom:10px}
.footer-col a{display:block;font-size:11px;color:var(--dim);text-decoration:none;padding:2px 0;transition:color 0.2s}
.footer-col a:hover{color:var(--amber)}
.footer-bottom{border-top:1px solid var(--border);margin-top:16px;padding-top:12px;font-size:9px;color:var(--dim);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
/* RESPONSIVE */
@media(max-width:768px){
  .header-inner{flex-direction:column;align-items:flex-start}
  .header-right{width:100%;justify-content:flex-start}
  .hamburger{display:flex}
  .nav-inner{flex-wrap:wrap}
  .nav-item{display:none;width:100%;border-right:none;border-bottom:1px solid var(--border)}
  .nav-item.show{display:block}
  .nav-item:last-child{border-bottom:none}
  .main-grid{padding:8px 0 24px}
  .gauge-container{grid-template-columns:1fr}
  .system-header{grid-template-columns:1fr 1fr}
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:480px){
  .system-header{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr}
  .logo-text{font-size:16px}
}
/* TOGGLE SWITCH */
.toggle-switch{
  width:32px;height:16px;border:1px solid var(--border);
  border-radius:8px;position:relative;cursor:pointer;display:inline-block;
  background:var(--bg);transition:all 0.3s;
}
.toggle-switch.on{background:rgba(255,123,0,0.2);border-color:var(--amber)}
.toggle-switch::after{
  content:'';position:absolute;top:1px;left:1px;
  width:12px;height:12px;border-radius:50%;
  background:var(--dim);transition:all 0.3s;
}
.toggle-switch.on::after{left:17px;background:var(--amber);box-shadow:0 0 6px rgba(255,123,0,0.3)}
</style>
</head>
<body>
<header>
<div class="wrap header-inner">
<div class="logo">
<div class="logo-icon">S</div>
<div>
<div class="logo-text">styde<span>_forge</span></div>
<div class="subtitle">Command Center &middot; v2.1.4</div>
</div>
</div>
<div class="header-right">
<div class="status-badge"><span class="status-dot"></span> SYSTEM ONLINE</div>
<div style="display:flex;align-items:center;gap:8px;font-size:10px;color:var(--dim)">
<span>Auto-pilot</span>
<span class="toggle-switch on" id="autopilot-toggle"></span>
</div>
</div>
</div>
</header>
<nav>
<div class="wrap nav-inner">
<div class="hamburger" id="hamburger"><span></span><span></span><span></span></div>
<div class="nav-item system active">Forge Overview</div>
<div class="nav-item">Blueprint Lab</div>
<div class="nav-item">Agent Roster</div>
<div class="nav-item">Pipeline Runs</div>
<div class="nav-item">Audit Log</div>
<div class="nav-item">System Config</div>
</div>
</nav>
<div class="wrap breadcrumb">
<a href="#">styde.se</a><span class="sep">/</span><a href="#">forge</a><span class="sep">/</span><span class="current">command-center</span>
</div>
<main class="wrap main-grid">
<!-- LEFT SIDEBAR -->
<div class="sidebar">
<div class="panel">
<div class="panel-title">Agent Fleet <span class="count">12</span></div>
<div class="agent-list">
<div class="agent-card online" onclick="this.querySelector('.collapse-target').classList.toggle('hidden')">
<div class="agent-indicator online"></div>
<div class="agent-info">
<div class="agent-name">web-mockup-artist</div>
<div class="agent-status online">Online</div>
<div class="agent-tasks">0 active tasks</div>
</div>
</div>
<div class="agent-card busy">
<div class="agent-indicator busy"></div>
<div class="agent-info">
<div class="agent-name">production-hardener</div>
<div class="agent-status busy">Running</div>
<div class="agent-tasks">2 active tasks</div>
</div>
</div>
<div class="agent-card busy">
<div class="agent-indicator busy"></div>
<div class="agent-info">
<div class="agent-name">orchestration-wf-builder</div>
<div class="agent-status busy">Running</div>
<div class="agent-tasks">1 active task</div>
</div>
</div>
<div class="agent-card online">
<div class="agent-indicator online"></div>
<div class="agent-info">
<div class="agent-name">caveman-mode-enforcer</div>
<div class="agent-status online">Idle</div>
<div class="agent-tasks">0 active tasks</div>
</div>
</div>
<div class="agent-card error">
<div class="agent-indicator error"></div>
<div class="agent-info">
<div class="agent-name">secrets-hardening-auditor</div>
<div class="agent-status error">Failed</div>
<div class="agent-tasks">Retry pending</div>
</div>
</div>
<div class="agent-card online">
<div class="agent-indicator online"></div>
<div class="agent-info">
<div class="agent-name">wcag-accessibility-eng</div>
<div class="agent-status online">Idle</div>
<div class="agent-tasks">0 active tasks</div>
</div>
</div>
</div>
</div>
<div class="panel">
<div class="panel-title collapse-trigger" onclick="this.classList.toggle('collapsed');document.getElementById('quick-actions').classList.toggle('hidden')">Quick Actions</div>
<div id="quick-actions">
<div style="display:flex;flex-direction:column;gap:6px">
<button style="background:rgba(255,123,0,0.1);border:1px solid var(--amber);color:var(--brass);padding:8px;font-family:var(--font);font-size:10px;text-transform:uppercase;letter-spacing:1px;cursor:pointer;transition:all 0.2s" onmouseover="this.style.background='rgba(255,123,0,0.2)'" onmouseout="this.style.background='rgba(255,123,0,0.1)'">Run All Pipelines</button>
<button style="background:transparent;border:1px solid var(--border);color:var(--dim);padding:8px;font-family:var(--font);font-size:10px;text-transform:uppercase;letter-spacing:1px;cursor:pointer;transition:all 0.2s" onmouseover="this.style.borderColor='var(--amber)';this.style.color='var(--brass)'" onmouseout="this.style.borderColor='var(--border)';this.style.color='var(--dim)'">Sync Blueprints</button>
<button style="background:transparent;border:1px solid var(--border);color:var(--dim);padding:8px;font-family:var(--font);font-size:10px;text-transform:uppercase;letter-spacing:1px;cursor:pointer;transition:all 0.2s" onmouseover="this.style.borderColor='var(--danger)';this.style.color='var(--danger)'" onmouseout="this.style.borderColor='var(--border)';this.style.color='var(--dim)'">Emergency Halt</button>
</div>
</div>
</div>
</div>
<!-- CENTER -->
<div>
<div class="panel" style="margin-bottom:16px">
<div class="panel-title">System Overview <span class="count">LIVE</span></div>
<div class="system-header">
<div class="metric-card">
<div class="metric-value">12</div>
<div class="metric-label">Active Agents</div>
<div class="metric-change up">+2 from last hour</div>
</div>
<div class="metric-card">
<div class="metric-value">47</div>
<div class="metric-label">Blueprints Loaded</div>
<div class="metric-change up">+3 today</div>
</div>
<div class="metric-card">
<div class="metric-value">1,842</div>
<div class="metric-label">Pipelines Executed</div>
<div class="metric-change up">+18 today</div>
</div>
<div class="metric-card">
<div class="metric-value">99.3%</div>
<div class="metric-label">Uptime (24h)</div>
<div class="metric-change down">-0.2%</div>
</div>
</div>
<div class="gauge-container">
<div class="gauge">
<div class="gauge-visual"><div class="gauge-fill" style="--gauge-deg:68deg"></div></div>
<div class="gauge-value" id="cpu-gauge">68%</div>
<div class="gauge-label">CPU Allocation</div>
</div>
<div class="gauge">
<div class="gauge-visual"><div class="gauge-fill" style="--gauge-deg:82deg"></div></div>
<div class="gauge-value" id="mem-gauge">82%</div>
<div class="gauge-label">Memory Load</div>
</div>
</div>
</div>
<div class="panel">
<div class="panel-title collapse-trigger" onclick="this.classList.toggle('collapsed');document.getElementById('activity-body').classList.toggle('hidden')">Activity Feed <span class="count">latest</span></div>
<div class="activity-feed" id="activity-body">
<div class="activity-item new">
<span class="time">14:23:17</span> <span class="msg"><span class="hl">production-hardener</span> completed pipeline #8471 in 3.2s</span>
</div>
<div class="activity-item new">
<span class="time">14:21:04</span> <span class="msg"><span class="hl">secrets-hardening-auditor</span> detected 2 exposed keys in blueprint config</span>
</div>
<div class="activity-item">
<span class="time">14:19:42</span> <span class="msg"><span class="hl">orchestration-wf-builder</span> deployed workflow 'nightly-patch-rollout'</span>
</div>
<div class="activity-item">
<span class="time">14:18:10</span> <span class="msg"><span class="hl">agent-scheduler</span> queued 4 batch jobs for priority tier 1</span>
</div>
<div class="activity-item">
<span class="time">14:15:55</span> <span class="msg"><span class="hl">web-mockup-artist</span> generated forge-command-center.html (this page)</span>
</div>
<div class="activity-item">
<span class="time">14:12:30</span> <span class="msg"><span class="hl">caveman-mode-enforcer</span> validated 112 files, 0 violations</span>
</div>
<div class="activity-item">
<span class="time">14:08:18</span> <span class="msg"><span class="hl">wcag-accessibility-eng</span> audited 7 pages, 3 issues flagged</span>
</div>
<div class="activity-item">
<span class="time">14:02:00</span> <span class="msg">System auto-scaled agent pool to <span class="hl">12</span> instances</span>
</div>
<div class="activity-item">
<span class="time">13:58:44</span> <span class="msg"><span class="hl">blueprint-syncer</span> pulled 2 updates from remote registry</span>
</div>
<div class="activity-item">
<span class="time">13:52:11</span> <span class="msg"><span class="hl">pipeline-automation-eng</span> triggered scheduled run 'daily-audit'</span>
</div>
</div>
</div>
</div>
<!-- RIGHT SIDEBAR -->
<div>
<div class="panel" style="margin-bottom:12px">
<div class="panel-title">GPU Monitor <span class="count">2x RTX 5090</span></div>
<div class="gpu-monitor">
<div class="gpu-card">
<div class="gpu-header"><span class="gpu-name">GPU 0 &mdash; RTX 5090</span><span class="gpu-temp">71&deg;C</span></div>
<div class="gpu-stats"><span>Utilization</span><span>64%</span></div>
<div class="bar-track"><div class="bar-fill usage" style="width:64%"></div></div>
<div class="gpu-stats"><span>Memory</span><span>18.2 / 32 GB</span></div>
<div class="bar-track"><div class="bar-fill mem" style="width:57%"></div></div>
<div class="gpu-stats"><span>VRAM</span><span>21.4 / 32 GB</span></div>
<div class="bar-track"><div class="bar-fill vram" style="width:67%"></div></div>
<div style="display:flex;justify-content:space-between;font-size:9px;color:var(--dim);margin-top:6px">
<span>PCIe 5.0 x16</span><span>Fan: 2400 RPM</span><span>Power: 325W</span>
</div>
</div>
<div class="gpu-card">
<div class="gpu-header"><span class="gpu-name">GPU 1 &mdash; RTX 5090</span><span class="gpu-temp">67&deg;C</span></div>
<div class="gpu-stats"><span>Utilization</span><span>42%</span></div>
<div class="bar-track"><div class="bar-fill usage" style="width:42%"></div></div>
<div class="gpu-stats"><span>Memory</span><span>12.7 / 32 GB</span></div>
<div class="bar-track"><div class="bar-fill mem" style="width:40%"></div></div>
<div class="gpu-stats"><span>VRAM</span><span>15.0 / 32 GB</span></div>
<div class="bar-track"><div class="bar-fill vram" style="width:47%"></div></div>
<div style="display:flex;justify-content:space-between;font-size:9px;color:var(--dim);margin-top:6px">
<span>PCIe 5.0 x16</span><span>Fan: 2100 RPM</span><span>Power: 289W</span>
</div>
</div>
</div>
</div>
<div class="panel">
<div class="panel-title">System Health</div>
<div style="display:flex;flex-direction:column;gap:8px">
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Agent Pool</span><span style="color:var(--safe)">12/12 Online</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Queue Depth</span><span style="color:var(--brass)">7 pending</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Avg Latency</span><span style="color:var(--safe)">124ms</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Error Rate (1h)</span><span style="color:var(--danger)">0.3%</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Disk I/O</span><span style="color:var(--brass)">342 MB/s</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:10px;align-items:center">
<span>Network</span><span style="color:var(--safe)">1.2 Gbps</span>
</div>
</div>
</div>
<div class="panel">
<div class="panel-title">Running Pipelines</div>
<div style="display:flex;flex-direction:column;gap:6px">
<div style="padding:6px 0;border-bottom:1px solid var(--border)">
<div style="font-size:10px;color:var(--brass)">nightly-audit</div>
<div style="font-size:9px;color:var(--dim)">Step 4/7 &middot; 43s elapsed</div>
<div class="bar-track" style="margin:4px 0"><div class="bar-fill usage" style="width:57%"></div></div>
</div>
<div style="padding:6px 0;border-bottom:1px solid var(--border)">
<div style="font-size:10px;color:var(--brass)">blueprint-sync</div>
<div style="font-size:9px;color:var(--dim)">Step 2/3 &middot; 12s elapsed</div>
<div class="bar-track" style="margin:4px 0"><div class="bar-fill usage" style="width:66%"></div></div>
</div>
<div style="padding:6px 0">
<div style="font-size:10px;color:var(--brass)">batch-eval-46</div>
<div style="font-size:9px;color:var(--dim)">Step 12/46 &middot; 2m18s elapsed</div>
<div class="bar-track" style="margin:4px 0"><div class="bar-fill usage" style="width:26%"></div></div>
</div>
</div>
</div>
</div>
</main>
<footer>
<div class="wrap">
<div class="footer-grid">
<div class="footer-col">
<h4>Styde Forge</h4>
<a href="#">Command Center</a>
<a href="#">Blueprint Registry</a>
<a href="#">Agent Roster</a>
<a href="#">Pipeline Manager</a>
<a href="#">Audit Trail</a>
</div>
<div class="footer-col">
<h4>Resources</h4>
<a href="#">Documentation</a>
<a href="#">API Reference</a>
<a href="#">Agent SDK</a>
<a href="#">CLI Tools</a>
<a href="#">Release Notes</a>
</div>
<div class="footer-col">
<h4>Monitoring</h4>
<a href="#">System Health</a>
<a href="#">GPU Dashboard</a>
<a href="#">Log Explorer</a>
<a href="#">Alert Configuration</a>
<a href="#">Performance Reports</a>
</div>
<div class="footer-col">
<h4>Connect</h4>
<a href="#">styde.se</a>
<a href="#">GitHub</a>
<a href="#">Discord</a>
<a href="#">Status Page</a>
<a href="#">Support</a>
</div>
</div>
<div class="footer-bottom">
<span>&copy; 2026 Styde Labs &mdash; Forge Command Center v2.1.4</span>
<span>Uptime: 14d 7h 23m &middot; Build 2026.06.26-1752</span>
</div>
</div>
</footer>
<script>
// hamburger toggle
document.getElementById('hamburger').addEventListener('click',function(){
  document.querySelectorAll('.nav-item').forEach(function(el){el.classList.toggle('show')});
});
// nav item active
document.querySelectorAll('.nav-item').forEach(function(el){
  el.addEventListener('click',function(){
    document.querySelectorAll('.nav-item').forEach(function(e){e.classList.remove('active')});
    this.classList.add('active');
  });
});
// auto-pilot toggle
document.getElementById('autopilot-toggle').addEventListener('click',function(){
  this.classList.toggle('on');
  var dot=document.querySelector('.status-dot');
  var badge=document.querySelector('.status-badge');
  if(this.classList.contains('on')){
    badge.innerHTML='<span class="status-dot"></span> SYSTEM ONLINE';
    dot.style.background='var(--safe)';
  }else{
    badge.innerHTML='<span class="status-dot"></span> MANUAL MODE';
    dot.style.background='var(--amber)';
  }
});
// gauge animation on load
window.addEventListener('load',function(){
  document.querySelectorAll('.gauge-fill').forEach(function(g,i){
    var deg=g.style.getPropertyValue('--gauge-deg');
    setTimeout(function(){g.style.setProperty('--gauge-deg',deg)},100+i*200);
  });
});
// simulate activity feed updates
(function(){
  var feed=document.querySelector('.activity-feed');
  var msgs=[
    'Pipeline <span class="hl">#8472</span> queued for execution',
    '<span class="hl">agent-scheduler</span> allocated 2 new workers',
    'Cache flush completed &mdash; 1.4 GB freed',
    '<span class="hl">secrets-hardening-auditor</span> retrying scan',
    'Heartbeat: all 12 agents responsive',
  ];
  var idx=0;
  setInterval(function(){
    var item=document.createElement('div');
    item.className='activity-item new';
    var d=new Date();
    var ts=d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0')+':'+d.getSeconds().toString().padStart(2,'0');
    item.innerHTML='<span class="time">'+ts+'</span> <span class="msg">'+msgs[idx%msgs.length]+'</span>';
    feed.insertBefore(item,feed.firstChild);
    idx++;
    if(feed.children.length>15){feed.removeChild(feed.lastChild)}
  },8000);
})();
</script>
</body>
</html>
```