```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Command Center</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg-deep: #0a0c0f;
    --bg-panel: #12161c;
    --bg-card: #181d26;
    --bg-hover: #1f2632;
    --border: #283040;
    --border-active: #3a4a66;
    --text: #cdd6e4;
    --text-dim: #7a889e;
    --text-bright: #ecf0f7;
    --accent: #64b5f6;
    --accent-dim: #3d7eb3;
    --green: #4caf7a;
    --orange: #e8a64c;
    --red: #e2574c;
    --purple: #9b7fd4;
    --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
    --radius: 10px;
    --shadow: 0 4px 24px rgba(0,0,0,.5);
  }
  html { font-size: 15px; }
  body {
    font-family: var(--font);
    background: var(--bg-deep);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.5;
  }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg-deep); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  .app-wrapper {
    max-width: 1440px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  /* ─── HEADER ─── */
  .site-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .header-left { display: flex; align-items: center; gap: 1rem; }
  .logo {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text-bright);
    letter-spacing: -0.02em;
  }
  .logo span { color: var(--accent); }
  .header-tag {
    font-size: 0.7rem;
    background: var(--accent-dim);
    color: #fff;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .header-center {
    display: flex;
    gap: 0.25rem;
    background: var(--bg-deep);
    border-radius: var(--radius);
    padding: 0.2rem;
  }
  .nav-btn {
    background: transparent;
    border: none;
    color: var(--text-dim);
    padding: 0.45rem 0.9rem;
    border-radius: 7px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all .2s;
    font-family: var(--font);
  }
  .nav-btn:hover { color: var(--text-bright); background: var(--bg-hover); }
  .nav-btn.active { color: var(--text-bright); background: var(--bg-card); box-shadow: inset 0 1px 0 var(--border-active); }
  .header-right { display: flex; align-items: center; gap: 1rem; }
  .status-badge {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    color: var(--text-dim);
  }
  .status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: pulse-dot 2s ease-in-out infinite;
  }
  @keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:.4} }
  .hamburger {
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
  }
  .hamburger span {
    display: block;
    width: 22px;
    height: 2px;
    background: var(--text);
    border-radius: 2px;
    transition: all .25s;
  }
  /* ─── BREADCRUMB ─── */
  .breadcrumb {
    padding: 0.6rem 1.5rem;
    font-size: 0.75rem;
    color: var(--text-dim);
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border);
  }
  .breadcrumb a { color: var(--accent-dim); text-decoration: none; }
  .breadcrumb a:hover { color: var(--accent); text-decoration: underline; }
  .breadcrumb .sep { margin: 0 0.4rem; color: var(--border); }
  /* ─── MAIN ─── */
  .main-grid {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
  }
  /* ─── CARDS ─── */
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: border-color .2s, box-shadow .2s;
  }
  .card:hover { border-color: var(--border-active); box-shadow: 0 2px 16px rgba(0,0,0,.35); }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    user-select: none;
  }
  .card-header h3 {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-bright);
    letter-spacing: 0.01em;
  }
  .card-body { padding: 1rem; }
  .card-footer {
    padding: 0.6rem 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.75rem;
    color: var(--text-dim);
  }
  /* collapsible */
  .collapsible .card-body { max-height: 600px; overflow: hidden; transition: max-height .35s ease, padding .35s ease; }
  .collapsible.collapsed .card-body { max-height: 0; padding: 0 1rem; }
  /* ─── METRICS STRIP ─── */
  .metrics-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  .metric-tile {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.85rem 1rem;
    transition: border-color .2s, transform .2s;
  }
  .metric-tile:hover { border-color: var(--border-active); transform: translateY(-1px); }
  .metric-tile .label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-dim);
    margin-bottom: 0.25rem;
  }
  .metric-tile .value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-bright);
    line-height: 1.1;
  }
  .metric-tile .sub {
    font-size: 0.7rem;
    color: var(--text-dim);
    margin-top: 0.15rem;
  }
  .quick-action-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--accent-dim);
    color: #fff;
    border: none;
    padding: 0.3rem 0.7rem;
    border-radius: 5px;
    font-size: 0.7rem;
    cursor: pointer;
    transition: background .2s, transform .15s;
    font-family: var(--font);
    font-weight: 500;
  }
  .quick-action-btn:hover { background: var(--accent); transform: scale(1.04); }
  .quick-action-btn.sm { padding: 0.2rem 0.5rem; font-size: 0.65rem; }
  /* ─── AGENT CARDS ─── */
  .agent-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.65rem;
  }
  .agent-card {
    background: var(--bg-deep);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem;
    transition: border-color .2s, box-shadow .2s;
    opacity: 0;
    animation: fade-in .4s ease forwards;
  }
  .agent-card:nth-child(1) { animation-delay: 40ms; }
  .agent-card:nth-child(2) { animation-delay: 120ms; }
  .agent-card:nth-child(3) { animation-delay: 200ms; }
  .agent-card:nth-child(4) { animation-delay: 280ms; }
  .agent-card:nth-child(5) { animation-delay: 360ms; }
  .agent-card:nth-child(6) { animation-delay: 440ms; }
  .agent-card:hover { border-color: var(--border-active); box-shadow: 0 0 0 1px var(--border-active); }
  @keyframes fade-in { to { opacity: 1; } }
  .agent-card .a-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
  }
  .agent-card .a-name { font-size: 0.78rem; font-weight: 600; color: var(--text-bright); }
  .agent-card .a-status {
    font-size: 0.6rem;
    padding: 0.1rem 0.45rem;
    border-radius: 3px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .a-status.ok { background: rgba(76,175,122,.18); color: var(--green); }
  .a-status.busy { background: rgba(232,166,76,.18); color: var(--orange); }
  .a-status.err { background: rgba(226,87,76,.18); color: var(--red); }
  .agent-card .a-task {
    font-size: 0.68rem;
    color: var(--text-dim);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .agent-card .a-gpu {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    margin-top: 0.35rem;
    font-size: 0.62rem;
    color: var(--text-dim);
  }
  .agent-card .a-gpu .bar-track {
    flex: 1;
    height: 3px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
  }
  .agent-card .a-gpu .bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width .6s ease;
  }
  /* ─── ACTIVITY FEED ─── */
  .feed-list { list-style: none; }
  .feed-item {
    display: flex;
    gap: 0.65rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.78rem;
  }
  .feed-item:last-child { border-bottom: none; }
  .feed-icon {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    flex-shrink: 0;
  }
  .feed-icon.blue { background: rgba(100,181,246,.15); color: var(--accent); }
  .feed-icon.green { background: rgba(76,175,122,.15); color: var(--green); }
  .feed-icon.purple { background: rgba(155,127,212,.15); color: var(--purple); }
  .feed-icon.orange { background: rgba(232,166,76,.15); color: var(--orange); }
  .feed-content { flex: 1; }
  .feed-content .f-text { color: var(--text); }
  .feed-content .f-text strong { color: var(--text-bright); font-weight: 600; }
  .feed-content .f-time { font-size: 0.65rem; color: var(--text-dim); margin-top: 0.15rem; }
  /* ─── SIDEBAR ─── */
  .sidebar { display: flex; flex-direction: column; gap: 0.75rem; }
  .gpu-panel { }
  .gpu-list { display: flex; flex-direction: column; gap: 0.5rem; }
  .gpu-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.45rem 0;
  }
  .gpu-row .gpu-label {
    width: 48px;
    font-size: 0.68rem;
    color: var(--text-dim);
    font-weight: 500;
    flex-shrink: 0;
  }
  .gpu-row .gpu-track {
    flex: 1;
    height: 6px;
    background: var(--bg-deep);
    border-radius: 3px;
    overflow: hidden;
  }
  .gpu-row .gpu-track .fill {
    height: 100%;
    border-radius: 3px;
    transition: width .8s ease;
  }
  .gpu-row .gpu-pct {
    width: 32px;
    text-align: right;
    font-size: 0.7rem;
    color: var(--text);
    font-weight: 500;
  }
  .gpu-row .gpu-temp {
    font-size: 0.62rem;
    color: var(--text-dim);
    width: 28px;
    text-align: right;
  }
  .summary-block {
    background: var(--bg-deep);
    border-radius: 6px;
    padding: 0.65rem 0.8rem;
  }
  .summary-block .s-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    padding: 0.2rem 0;
  }
  .summary-block .s-row .s-label { color: var(--text-dim); }
  .summary-block .s-row .s-val { color: var(--text-bright); font-weight: 600; }
  .summary-block .s-row .s-val.pass { color: var(--green); }
  .summary-block .s-row .s-val.warn { color: var(--orange); }
  .summary-block .s-row .s-val.fail { color: var(--red); }
  /* ─── FOOTER ─── */
  .site-footer {
    padding: 1rem 1.5rem;
    background: var(--bg-panel);
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 0.72rem;
    color: var(--text-dim);
  }
  .site-footer .links { display: flex; gap: 1rem; }
  .site-footer .links a { color: var(--text-dim); text-decoration: none; }
  .site-footer .links a:hover { color: var(--accent); }
  /* ─── RESPONSIVE ─── */
  @media (max-width: 960px) {
    .main-grid { grid-template-columns: 1fr; }
    .sidebar { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
    .metrics-strip { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 660px) {
    .site-header { padding: 0.5rem 0.75rem; }
    .header-center { display: none; }
    .header-center.mobile-open {
      display: flex;
      flex-direction: column;
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border);
      padding: 0.5rem;
      z-index: 99;
    }
    .hamburger { display: flex; }
    .main-grid { padding: 0.75rem; }
    .sidebar { grid-template-columns: 1fr; }
    .metrics-strip { grid-template-columns: 1fr 1fr; }
    .agent-grid { grid-template-columns: 1fr 1fr; }
    .breadcrumb { font-size: 0.68rem; padding: 0.4rem 0.75rem; }
    .site-footer { flex-direction: column; text-align: center; }
  }
  @media (max-width: 420px) {
    .metrics-strip { grid-template-columns: 1fr; }
    .agent-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
<div class="app-wrapper">
  <!-- HEADER -->
  <header class="site-header">
    <div class="header-left">
      <div class="logo">styde<span>forge</span></div>
      <span class="header-tag">pre-alpha</span>
    </div>
    <nav class="header-center" id="mainNav">
      <button class="nav-btn active">dashboard</button>
      <button class="nav-btn">agents</button>
      <button class="nav-btn">blueprints</button>
      <button class="nav-btn">batch</button>
      <button class="nav-btn">logs</button>
    </nav>
    <div class="header-right">
      <div class="status-badge">
        <span class="status-dot"></span>
        <span>all systems nominal</span>
      </div>
      <button class="hamburger" id="hamToggle" aria-label="menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
  <!-- BREADCRUMB -->
  <div class="breadcrumb">
    <a href="#">styde.se</a>
    <span class="sep">/</span>
    <a href="#">forge</a>
    <span class="sep">/</span>
    <span>command center</span>
  </div>
  <!-- MAIN -->
  <div class="main-grid">
    <!-- LEFT COLUMN -->
    <div class="left-col">
      <!-- METRICS STRIP -->
      <div class="metrics-strip">
        <div class="metric-tile">
          <div class="label">active agents</div>
          <div class="value">12</div>
          <div class="sub">of 18 deployed</div>
        </div>
        <div class="metric-tile">
          <div class="label">gpu utilization</div>
          <div class="value">73<small style="font-size:.7rem;font-weight:400;color:var(--text-dim)">%</small></div>
          <div class="sub">4.2 TFLOPS avg</div>
        </div>
        <div class="metric-tile">
          <div class="label">queue depth</div>
          <div class="value">8</div>
          <div class="sub">2.3 min avg wait</div>
        </div>
        <div class="metric-tile">
          <div class="label">eval score</div>
          <div class="value">89.2</div>
          <div class="sub">+1.7 vs last run</div>
        </div>
      </div>
      <!-- AGENT STATUS -->
      <div class="card collapsible" id="agentCard">
        <div class="card-header" onclick="toggleCollapse('agentCard')">
          <h3>&diams; agent status</h3>
          <div>
            <button class="quick-action-btn sm" onclick="event.stopPropagation();void 0">&circlearrowleft; refresh</button>
            <span style="font-size:.65rem;color:var(--text-dim);margin-left:.5rem">click to toggle</span>
          </div>
        </div>
        <div class="card-body">
          <div class="agent-grid">
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">caveman</span>
                <span class="a-status ok">idle</span>
              </div>
              <div class="a-task">awaiting directive</div>
              <div class="a-gpu">
                <span>GPU0</span>
                <div class="bar-track"><div class="bar-fill" style="width:12%;background:var(--green)"></div></div>
                <span>12%</span>
              </div>
            </div>
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">mockup</span>
                <span class="a-status busy">busy</span>
              </div>
              <div class="a-task">render dashboard v4</div>
              <div class="a-gpu">
                <span>GPU1</span>
                <div class="bar-track"><div class="bar-fill" style="width:68%;background:var(--orange)"></div></div>
                <span>68%</span>
              </div>
            </div>
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">forge</span>
                <span class="a-status ok">idle</span>
              </div>
              <div class="a-task">polling blueprint queue</div>
              <div class="a-gpu">
                <span>GPU0</span>
                <div class="bar-track"><div class="bar-fill" style="width:4%;background:var(--green)"></div></div>
                <span>4%</span>
              </div>
            </div>
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">prompt-eng</span>
                <span class="a-status ok">idle</span>
              </div>
              <div class="a-task">optimizing plan prompt</div>
              <div class="a-gpu">
                <span>GPU2</span>
                <div class="bar-track"><div class="bar-fill" style="width:23%;background:var(--green)"></div></div>
                <span>23%</span>
              </div>
            </div>
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">evaluator</span>
                <span class="a-status busy">busy</span>
              </div>
              <div class="a-task">batch #46 scoring</div>
              <div class="a-gpu">
                <span>GPU3</span>
                <div class="bar-track"><div class="bar-fill" style="width:91%;background:var(--orange)"></div></div>
                <span>91%</span>
              </div>
            </div>
            <div class="agent-card">
              <div class="a-top">
                <span class="a-name">web-mockup</span>
                <span class="a-status err">error</span>
              </div>
              <div class="a-task">artifact rejected (score 47)</div>
              <div class="a-gpu">
                <span>GPU1</span>
                <div class="bar-track"><div class="bar-fill" style="width:0%;background:var(--red)"></div></div>
                <span>0%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- EVALUATION SUMMARY -->
      <div class="card collapsible" id="evalCard" style="margin-top:0.75rem">
        <div class="card-header" onclick="toggleCollapse('evalCard')">
          <h3>&#9744; evaluation summary</h3>
          <span style="font-size:.65rem;color:var(--text-dim)">click to toggle</span>
        </div>
        <div class="card-body">
          <div class="summary-block">
            <div class="s-row"><span class="s-label">overall score</span><span class="s-val">89.2 / 100</span></div>
            <div class="s-row"><span class="s-label">clarity</span><span class="s-val" style="color:var(--orange)">72</span></div>
            <div class="s-row"><span class="s-label">efficiency</span><span class="s-val" style="color:var(--orange)">78</span></div>
            <div class="s-row"><span class="s-label">functionality</span><span class="s-val pass">94</span></div>
            <div class="s-row"><span class="s-label">aesthetics</span><span class="s-val pass">96</span></div>
            <div class="s-row" style="border-top:1px solid var(--border);padding-top:0.45rem;margin-top:0.35rem">
              <span class="s-label">pass / warn / fail</span>
              <span><span class="s-val pass">12</span> / <span class="s-val warn">2</span> / <span class="s-val fail">1</span></span>
            </div>
          </div>
          <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
            <button class="quick-action-btn sm">&#9654; re-evaluate</button>
            <button class="quick-action-btn sm" style="background:var(--bg-hover);color:var(--text)">&#128279; share report</button>
          </div>
        </div>
      </div>
    </div>
    <!-- SIDEBAR -->
    <div class="sidebar">
      <!-- GPU MONITOR -->
      <div class="card gpu-panel collapsible" id="gpuCard">
        <div class="card-header" onclick="toggleCollapse('gpuCard')">
          <h3>&#9881; gpu monitor</h3>
          <button class="quick-action-btn sm" onclick="event.stopPropagation();void 0">&#8635;</button>
        </div>
        <div class="card-body">
          <div class="gpu-list">
            <div class="gpu-row">
              <span class="gpu-label">GPU0</span>
              <div class="gpu-track"><div class="fill" style="width:24%;background:var(--green)"></div></div>
              <span class="gpu-pct">24%</span>
              <span class="gpu-temp">52&deg;</span>
            </div>
            <div class="gpu-row">
              <span class="gpu-label">GPU1</span>
              <div class="gpu-track"><div class="fill" style="width:78%;background:var(--orange)"></div></div>
              <span class="gpu-pct">78%</span>
              <span class="gpu-temp">71&deg;</span>
            </div>
            <div class="gpu-row">
              <span class="gpu-label">GPU2</span>
              <div class="gpu-track"><div class="fill" style="width:15%;background:var(--green)"></div></div>
              <span class="gpu-pct">15%</span>
              <span class="gpu-temp">44&deg;</span>
            </div>
            <div class="gpu-row">
              <span class="gpu-label">GPU3</span>
              <div class="gpu-track"><div class="fill" style="width:95%;background:var(--red)"></div></div>
              <span class="gpu-pct">95%</span>
              <span class="gpu-temp">83&deg;</span>
            </div>
          </div>
        </div>
      </div>
      <!-- ACTIVITY FEED -->
      <div class="card collapsible" id="activityCard">
        <div class="card-header" onclick="toggleCollapse('activityCard')">
          <h3>&#9776; activity feed</h3>
        </div>
        <div class="card-body" style="padding:.5rem .75rem">
          <ul class="feed-list">
            <li class="feed-item">
              <div class="feed-icon green">&#10003;</div>
              <div class="feed-content">
                <div class="f-text"><strong>caveman</strong> completed blueprint #47</div>
                <div class="f-time">just now</div>
              </div>
            </li>
            <li class="feed-item">
              <div class="feed-icon orange">&#9888;</div>
              <div class="feed-content">
                <div class="f-text"><strong>evaluator</strong> flagged clarity metric (score 72)</div>
                <div class="f-time">2 min ago</div>
              </div>
            </li>
            <li class="feed-item">
              <div class="feed-icon blue">&#8635;</div>
              <div class="feed-content">
                <div class="f-text"><strong>forge</strong> started batch training run 12</div>
                <div class="f-time">7 min ago</div>
              </div>
            </li>
            <li class="feed-item">
              <div class="feed-icon purple">&#9733;</div>
              <div class="feed-content">
                <div class="f-text"><strong>prompt-eng</strong> pushed PlanPrompt-v6.md</div>
                <div class="f-time">14 min ago</div>
              </div>
            </li>
            <li class="feed-item">
              <div class="feed-icon orange">&#9888;</div>
              <div class="feed-content">
                <div class="f-text"><strong>web-mockup</strong> artifact rejected — score 47</div>
                <div class="f-time">23 min ago</div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <!-- FOOTER -->
  <footer class="site-footer">
    <span>styde forge &mdash; command center &bull; build 20260626</span>
    <div class="links">
      <a href="#">docs</a>
      <a href="#">status</a>
      <a href="#">api</a>
      <a href="#">github</a>
      <a href="#">styde.se</a>
    </div>
  </footer>
</div>
<script>
function toggleCollapse(id) {
  var el = document.getElementById(id);
  if (el) el.classList.toggle('collapsed');
}
// hamburger toggle
document.getElementById('hamToggle').addEventListener('click', function(e) {
  e.stopPropagation();
  var nav = document.getElementById('mainNav');
  nav.classList.toggle('mobile-open');
});
// nav button interactivity
document.querySelectorAll('.nav-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.remove('active')});
    this.classList.add('active');
    // close mobile nav on selection
    var nav = document.getElementById('mainNav');
    if (nav.classList.contains('mobile-open')) nav.classList.remove('mobile-open');
  });
});
// staggered GPU bar animation on load
document.addEventListener('DOMContentLoaded', function() {
  var fills = document.querySelectorAll('.gpu-row .fill');
  fills.forEach(function(fill, i) {
    var target = fill.style.width;
    fill.style.width = '0%';
    setTimeout(function() {
      fill.style.width = target;
    }, 80 * i + 100);
  });
});
</script>
</body>
</html>
```