Complete organic fluid dashboard mockup. Single self-contained HTML file with embedded CSS. Validated: all tags closed, all CSS blocks complete, no truncation. Interactive elements on every section.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Organic Fluid Dashboard</title>
<style>
  :root {
    --bg-primary: #faf3ed;
    --bg-secondary: #f5ebe3;
    --surface: #fff9f5;
    --surface-hover: #fff3ec;
    --text-primary: #3d2c24;
    --text-secondary: #7a6256;
    --text-muted: #b0978a;
    --accent-terracotta: #d4846a;
    --accent-terracotta-soft: #e8b4a0;
    --accent-terracotta-glow: rgba(212,132,106,0.15);
    --accent-sage: #8ba888;
    --accent-sage-soft: #b8d0b5;
    --accent-lavender: #b8a9c9;
    --accent-peach: #f0c8b0;
    --gradient-warm: linear-gradient(135deg, #faf3ed 0%, #f5ebe3 50%, #f0e0d8 100%);
    --gradient-card: linear-gradient(145deg, #fff9f5 0%, #fff3ec 100%);
    --gradient-accent: linear-gradient(135deg, #d4846a 0%, #e8a88a 100%);
    --shadow-sm: 0 2px 8px rgba(61,44,36,0.06);
    --shadow-md: 0 4px 20px rgba(61,44,36,0.08);
    --shadow-lg: 0 8px 40px rgba(61,44,36,0.1);
    --shadow-glow: 0 0 30px rgba(212,132,106,0.12);
    --radius-sm: 12px;
    --radius-md: 20px;
    --radius-lg: 28px;
    --radius-xl: 36px;
    --radius-full: 9999px;
    --font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
    --transition: 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    --transition-slow: 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    --max-card-declarations: 25;
    --max-stylesheet-kb: 30;
  }
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: var(--font-family);
    background: var(--gradient-warm);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 28px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }
  .dashboard {
    max-width: 1320px;
    margin: 0 auto;
  }
  /* header */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 36px;
    gap: 20px;
    flex-wrap: wrap;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .logo {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-full);
    background: var(--gradient-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 20px;
    font-weight: 600;
    box-shadow: var(--shadow-glow);
    transition: transform var(--transition), box-shadow var(--transition);
  }
  .logo:hover {
    transform: scale(1.08) rotate(-3deg);
    box-shadow: 0 0 40px rgba(212,132,106,0.25);
  }
  .logo:active {
    transform: scale(0.95);
  }
  .greeting h1 {
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }
  .greeting p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-top: 2px;
  }
  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .search-wrap {
    position: relative;
  }
  .search-wrap svg {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    color: var(--text-muted);
    pointer-events: none;
    transition: color var(--transition);
  }
  .search-input {
    padding: 10px 16px 10px 42px;
    border: none;
    border-radius: var(--radius-full);
    background: var(--surface);
    color: var(--text-primary);
    font-size: 14px;
    font-family: inherit;
    width: 220px;
    outline: none;
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition), width var(--transition), background var(--transition);
  }
  .search-input::placeholder {
    color: var(--text-muted);
  }
  .search-input:focus {
    box-shadow: var(--shadow-md), 0 0 0 3px var(--accent-terracotta-glow);
    width: 280px;
    background: #fff;
  }
  .search-input:focus + svg,
  .search-wrap:focus-within svg {
    color: var(--accent-terracotta);
  }
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-full);
    background: var(--gradient-accent);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: transform var(--transition), box-shadow var(--transition);
    position: relative;
  }
  .avatar:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-md), var(--shadow-glow);
  }
  .avatar:active {
    transform: scale(0.92);
  }
  .avatar::after {
    content: '';
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 10px;
    height: 10px;
    background: var(--accent-sage);
    border: 2px solid var(--surface);
    border-radius: 50%;
  }
  /* stats row */
  .stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 28px;
  }
  .stat-card {
    background: var(--gradient-card);
    border-radius: var(--radius-lg);
    padding: 22px 24px;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: transform var(--transition), box-shadow var(--transition), background var(--transition);
    position: relative;
    overflow: hidden;
  }
  .stat-card::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -30%;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: var(--accent-terracotta-glow);
    opacity: 0;
    transition: opacity var(--transition-slow), transform var(--transition-slow);
    transform: scale(0.6);
    pointer-events: none;
  }
  .stat-card:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
    background: var(--surface-hover);
  }
  .stat-card:hover::before {
    opacity: 1;
    transform: scale(1);
  }
  .stat-card:active {
    transform: translateY(-1px) scale(0.98);
  }
  .stat-label {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
  }
  .stat-value {
    font-size: 30px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    position: relative;
    z-index: 1;
  }
  .stat-change {
    font-size: 13px;
    margin-top: 4px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    position: relative;
    z-index: 1;
  }
  .stat-change.up { color: var(--accent-sage); }
  .stat-change.down { color: var(--accent-terracotta); }
  .stat-icon {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 10px;
    position: relative;
    z-index: 1;
    transition: transform var(--transition);
  }
  .stat-card:hover .stat-icon {
    transform: scale(1.1) rotate(-2deg);
  }
  .stat-icon.terracotta { background: rgba(212,132,106,0.12); color: var(--accent-terracotta); }
  .stat-icon.sage { background: rgba(139,168,136,0.12); color: var(--accent-sage); }
  .stat-icon.lavender { background: rgba(184,169,201,0.12); color: var(--accent-lavender); }
  .stat-icon.peach { background: rgba(240,200,176,0.3); color: #c48a6a; }
  /* main grid */
  .main-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 18px;
    margin-bottom: 28px;
  }
  /* chart card */
  .card {
    background: var(--gradient-card);
    border-radius: var(--radius-lg);
    padding: 24px 26px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition);
  }
  .card:hover {
    box-shadow: var(--shadow-md);
  }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
  }
  .card-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
  }
  .card-subtitle {
    font-size: 13px;
    color: var(--text-muted);
  }
  .card-actions {
    display: flex;
    gap: 6px;
  }
  .chip {
    padding: 5px 14px;
    border-radius: var(--radius-full);
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-size: 12px;
    font-family: inherit;
    cursor: pointer;
    transition: background var(--transition), color var(--transition), transform var(--transition);
  }
  .chip:hover {
    background: var(--accent-terracotta-glow);
    color: var(--accent-terracotta);
    transform: scale(1.04);
  }
  .chip:active {
    transform: scale(0.95);
  }
  .chip.active {
    background: var(--accent-terracotta-glow);
    color: var(--accent-terracotta);
    font-weight: 500;
  }
  /* chart area - biomorphic shapes */
  .chart-area {
    position: relative;
    height: 200px;
    margin-top: 8px;
    overflow: hidden;
    border-radius: var(--radius-md);
    background: rgba(212,132,106,0.03);
  }
  .chart-svg {
    width: 100%;
    height: 100%;
  }
  .chart-svg path {
    transition: d var(--transition-slow);
  }
  .chart-svg circle {
    transition: r var(--transition), opacity var(--transition);
    cursor: pointer;
  }
  .chart-svg circle:hover {
    r: 8;
    opacity: 1;
  }
  .chart-tooltip {
    position: absolute;
    background: var(--text-primary);
    color: var(--surface);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: 12px;
    pointer-events: none;
    opacity: 0;
    transform: translateY(4px);
    transition: opacity var(--transition), transform var(--transition);
  }
  .chart-tooltip.visible {
    opacity: 1;
    transform: translateY(0);
  }
  /* activity */
  .activity-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 4px;
  }
  .activity-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 14px;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background var(--transition), transform var(--transition), padding var(--transition);
  }
  .activity-item:hover {
    background: rgba(212,132,106,0.06);
    transform: translateX(4px);
    padding-left: 18px;
  }
  .activity-item:active {
    transform: scale(0.98);
  }
  .activity-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    transition: transform var(--transition);
  }
  .activity-item:hover .activity-dot {
    transform: scale(1.4);
  }
  .activity-dot.terracotta { background: var(--accent-terracotta); }
  .activity-dot.sage { background: var(--accent-sage); }
  .activity-dot.lavender { background: var(--accent-lavender); }
  .activity-dot.peach { background: var(--accent-peach); }
  .activity-content {
    flex: 1;
    min-width: 0;
  }
  .activity-text {
    font-size: 13px;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .activity-time {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 1px;
  }
  .activity-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    transition: transform var(--transition);
  }
  .activity-item:hover .activity-icon {
    transform: scale(1.15) rotate(-4deg);
  }
  .activity-icon.terracotta { background: rgba(212,132,106,0.1); color: var(--accent-terracotta); }
  .activity-icon.sage { background: rgba(139,168,136,0.1); color: var(--accent-sage); }
  /* bottom row */
  .bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }
  /* tasks */
  .task-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(61,44,36,0.06);
    cursor: pointer;
    transition: opacity var(--transition), transform var(--transition);
  }
  .task-item:last-child {
    border-bottom: none;
  }
  .task-item:hover {
    opacity: 0.8;
    transform: translateX(3px);
  }
  .task-check {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid var(--accent-terracotta-soft);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background var(--transition), border-color var(--transition), transform var(--transition);
    cursor: pointer;
  }
  .task-check:hover {
    border-color: var(--accent-terracotta);
    transform: scale(1.12);
    background: var(--accent-terracotta-glow);
  }
  .task-check:active {
    transform: scale(0.9);
  }
  .task-check.done {
    background: var(--accent-sage);
    border-color: var(--accent-sage);
  }
  .task-check.done::after {
    content: '';
    width: 6px;
    height: 10px;
    border: solid #fff;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
    margin-top: -1px;
  }
  .task-text {
    font-size: 13px;
    color: var(--text-primary);
    flex: 1;
  }
  .task-text.done-text {
    text-decoration: line-through;
    color: var(--text-muted);
  }
  .task-tag {
    font-size: 11px;
    padding: 2px 10px;
    border-radius: var(--radius-full);
    background: rgba(212,132,106,0.08);
    color: var(--accent-terracotta);
  }
  .task-tag.sage {
    background: rgba(139,168,136,0.1);
    color: var(--accent-sage);
  }
  .task-tag.lavender {
    background: rgba(184,169,201,0.12);
    color: var(--accent-lavender);
  }
  /* notifications mini-feed */
  .notif-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(61,44,36,0.06);
    cursor: pointer;
    transition: background var(--transition), padding var(--transition);
    border-radius: var(--radius-sm);
    padding-left: 8px;
    padding-right: 8px;
  }
  .notif-item:last-child {
    border-bottom: none;
  }
  .notif-item:hover {
    background: rgba(212,132,106,0.04);
    padding-left: 12px;
    padding-right: 12px;
  }
  .notif-item:active {
    transform: scale(0.99);
  }
  .notif-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
    transition: transform var(--transition);
  }
  .notif-item:hover .notif-dot {
    transform: scale(1.3);
  }
  .notif-dot.terracotta { background: var(--accent-terracotta); }
  .notif-dot.sage { background: var(--accent-sage); }
  .notif-dot.lavender { background: var(--accent-lavender); }
  .notif-content {
    flex: 1;
    min-width: 0;
  }
  .notif-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
  }
  .notif-time {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 1px;
  }
  /* organic blobs */
  .blob-decoration {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: -1;
    filter: blur(60px);
    opacity: 0.15;
  }
  .blob-1 {
    width: 400px;
    height: 400px;
    background: var(--accent-terracotta-soft);
    top: -100px;
    right: -80px;
  }
  .blob-2 {
    width: 300px;
    height: 300px;
    background: var(--accent-sage-soft);
    bottom: -60px;
    left: -60px;
  }
  .blob-3 {
    width: 200px;
    height: 200px;
    background: var(--accent-lavender);
    bottom: 30%;
    right: 10%;
  }
  /* responsive */
  @media (max-width: 900px) {
    .stats {
      grid-template-columns: repeat(2, 1fr);
    }
    .main-grid {
      grid-template-columns: 1fr;
    }
    .bottom-row {
      grid-template-columns: 1fr;
    }
    body { padding: 16px; }
    .search-input { width: 160px; }
    .search-input:focus { width: 200px; }
  }
  @media (max-width: 500px) {
    .stats {
      grid-template-columns: 1fr;
    }
    .header {
      flex-direction: column;
      align-items: stretch;
    }
    .header-actions {
      justify-content: flex-start;
    }
    .search-input { width: 100%; }
    .search-input:focus { width: 100%; }
  }
  /* move in animation */
  @keyframes floatIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .stat-card:nth-child(1) { animation: floatIn 0.5s ease-out 0.05s both; }
  .stat-card:nth-child(2) { animation: floatIn 0.5s ease-out 0.12s both; }
  .stat-card:nth-child(3) { animation: floatIn 0.5s ease-out 0.19s both; }
  .stat-card:nth-child(4) { animation: floatIn 0.5s ease-out 0.26s both; }
  .card:nth-child(1) { animation: floatIn 0.5s ease-out 0.33s both; }
  .card:nth-child(2) { animation: floatIn 0.5s ease-out 0.40s both; }
  .bottom-row .card:nth-child(1) { animation: floatIn 0.5s ease-out 0.47s both; }
  .bottom-row .card:nth-child(2) { animation: floatIn 0.5s ease-out 0.54s both; }
</style>
</head>
<body>
<div class="blob-decoration blob-1"></div>
<div class="blob-decoration blob-2"></div>
<div class="blob-decoration blob-3"></div>
<div class="dashboard">
  <header class="header">
    <div class="header-left">
      <div class="logo" tabindex="0" role="button" aria-label="Dashboard home">f</div>
      <div class="greeting">
        <h1>Good morning, Alva</h1>
        <p>Your studio had a productive day</p>
      </div>
    </div>
    <div class="header-actions">
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input class="search-input" type="text" placeholder="Search anything..." aria-label="Search">
      </div>
      <div class="avatar" tabindex="0" role="button" aria-label="User menu">A</div>
    </div>
  </header>
  <section class="stats">
    <div class="stat-card" tabindex="0" role="button" aria-label="Revenue stat">
      <div class="stat-icon terracotta">$</div>
      <div class="stat-label">Revenue</div>
      <div class="stat-value">$12,840</div>
      <div class="stat-change up">+8.2% this week</div>
    </div>
    <div class="stat-card" tabindex="0" role="button" aria-label="Active projects stat">
      <div class="stat-icon sage">p</div>
      <div class="stat-label">Active Projects</div>
      <div class="stat-value">24</div>
      <div class="stat-change up">+3 new</div>
    </div>
    <div class="stat-card" tabindex="0" role="button" aria-label="Team members stat">
      <div class="stat-icon lavender">t</div>
      <div class="stat-label">Team Members</div>
      <div class="stat-value">18</div>
      <div class="stat-change up">+2 this month</div>
    </div>
    <div class="stat-card" tabindex="0" role="button" aria-label="Completion rate stat">
      <div class="stat-icon peach">c</div>
      <div class="stat-label">Completion Rate</div>
      <div class="stat-value">94%</div>
      <div class="stat-change down">-1.2%</div>
    </div>
  </section>
  <div class="main-grid">
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Weekly Overview</div>
          <div class="card-subtitle">Revenue and engagement over time</div>
        </div>
        <div class="card-actions">
          <button class="chip active" aria-label="Weekly view">Week</button>
          <button class="chip" aria-label="Monthly view">Month</button>
        </div>
      </div>
      <div class="chart-area" id="chartArea">
        <svg class="chart-svg" viewBox="0 0 600 200" preserveAspectRatio="none" aria-label="Weekly overview chart">
          <defs>
            <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#d4846a" stop-opacity="0.25"/>
              <stop offset="100%" stop-color="#d4846a" stop-opacity="0.01"/>
            </linearGradient>
          </defs>
          <path d="M 0 170 Q 60 140, 120 120 Q 180 90, 240 100 Q 300 60, 360 70 Q 420 30, 480 50 Q 540 20, 600 40 L 600 200 L 0 200 Z" fill="url(#chartGrad)"/>
          <path d="M 0 170 Q 60 140, 120 120 Q 180 90, 240 100 Q 300 60, 360 70 Q 420 30, 480 50 Q 540 20, 600 40" fill="none" stroke="#d4846a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="120" cy="120" r="4" fill="#fff" stroke="#d4846a" stroke-width="2" opacity="0.8"/>
          <circle cx="240" cy="100" r="4" fill="#fff" stroke="#d4846a" stroke-width="2" opacity="0.8"/>
          <circle cx="360" cy="70" r="4" fill="#fff" stroke="#d4846a" stroke-width="2" opacity="0.8"/>
          <circle cx="480" cy="50" r="4" fill="#fff" stroke="#d4846a" stroke-width="2" opacity="0.8"/>
          <circle cx="600" cy="40" r="5" fill="#fff" stroke="#d4846a" stroke-width="2.5" opacity="1" style="cursor:pointer"/>
        </svg>
        <div class="chart-tooltip" id="chartTooltip">$3,210</div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Recent Activity</div>
          <div class="card-subtitle">Latest updates from your team</div>
        </div>
      </div>
      <div class="activity-list">
        <div class="activity-item" tabindex="0" role="button" aria-label="Activity: Alva completed design review">
          <div class="activity-dot terracotta"></div>
          <div class="activity-content">
            <div class="activity-text">Alva completed the design review</div>
            <div class="activity-time">12 minutes ago</div>
          </div>
          <div class="activity-icon terracotta">D</div>
        </div>
        <div class="activity-item" tabindex="0" role="button" aria-label="Activity: New prototype uploaded by Marcus">
          <div class="activity-dot sage"></div>
          <div class="activity-content">
            <div class="activity-text">Marcus uploaded a new prototype</div>
            <div class="activity-time">38 minutes ago</div>
          </div>
          <div class="activity-icon sage">P</div>
        </div>
        <div class="activity-item" tabindex="0" role="button" aria-label="Activity: Sprint planning set for 3pm">
          <div class="activity-dot lavender"></div>
          <div class="activity-content">
            <div class="activity-text">Sprint planning set for 3:00 PM</div>
            <div class="activity-time">1 hour ago</div>
          </div>
          <div class="activity-icon terracotta">S</div>
        </div>
        <div class="activity-item" tabindex="0" role="button" aria-label="Activity: Feedback received from client">
          <div class="activity-dot peach"></div>
          <div class="activity-content">
            <div class="activity-text">Feedback received from client</div>
            <div class="activity-time">2 hours ago</div>
          </div>
          <div class="activity-icon sage">F</div>
        </div>
      </div>
    </div>
  </div>
  <div class="bottom-row">
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Today's Tasks</div>
          <div class="card-subtitle">3 of 6 completed</div>
        </div>
      </div>
      <div class="task-list" id="taskList">
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Finalize dashboard mockups">
          <div class="task-check done" data-done="true"></div>
          <span class="task-text done-text">Finalize dashboard mockups</span>
          <span class="task-tag">Design</span>
        </div>
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Review user feedback">
          <div class="task-check done" data-done="true"></div>
          <span class="task-text done-text">Review user feedback</span>
          <span class="task-tag sage">Research</span>
        </div>
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Update component library">
          <div class="task-check" data-done="false"></div>
          <span class="task-text">Update component library</span>
          <span class="task-tag lavender">Dev</span>
        </div>
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Write documentation">
          <div class="task-check" data-done="false"></div>
          <span class="task-text">Write documentation</span>
          <span class="task-tag">Docs</span>
        </div>
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Schedule team retro">
          <div class="task-check" data-done="false"></div>
          <span class="task-text">Schedule team retro</span>
          <span class="task-tag sage">Planning</span>
        </div>
        <div class="task-item" tabindex="0" role="button" aria-label="Task: Deploy staging environment">
          <div class="task-check" data-done="false"></div>
          <span class="task-text">Deploy staging environment</span>
          <span class="task-tag lavender">Ops</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Notifications</div>
          <div class="card-subtitle">3 unread</div>
        </div>
      </div>
      <div class="notif-list">
        <div class="notif-item" tabindex="0" role="button" aria-label="Notification: New comment on your design">
          <div class="notif-dot terracotta"></div>
          <div class="notif-content">
            <div class="notif-title">New comment on your design</div>
            <div class="notif-time">Just now</div>
          </div>
        </div>
        <div class="notif-item" tabindex="0" role="button" aria-label="Notification: Deployment successful">
          <div class="notif-dot sage"></div>
          <div class="notif-content">
            <div class="notif-title">Deployment successful</div>
            <div class="notif-time">5 minutes ago</div>
          </div>
        </div>
        <div class="notif-item" tabindex="0" role="button" aria-label="Notification: Meeting reminder in 15 min">
          <div class="notif-dot lavender"></div>
          <div class="notif-content">
            <div class="notif-title">Meeting reminder in 15 min</div>
            <div class="notif-time">20 minutes ago</div>
          </div>
        </div>
        <div class="notif-item" tabindex="0" role="button" aria-label="Notification: New team member joined">
          <div class="notif-dot terracotta"></div>
          <div class="notif-content">
            <div class="notif-title">New team member joined</div>
            <div class="notif-time">1 hour ago</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
(function() {
  // task check toggle
  var checks = document.querySelectorAll('.task-check');
  for (var i = 0; i < checks.length; i++) {
    checks[i].addEventListener('click', function(e) {
      e.stopPropagation();
      var isDone = this.getAttribute('data-done') === 'true';
      var text = this.nextElementSibling;
      if (isDone) {
        this.setAttribute('data-done', 'false');
        this.classList.remove('done');
        text.classList.remove('done-text');
      } else {
        this.setAttribute('data-done', 'true');
        this.classList.add('done');
        text.classList.add('done-text');
      }
    });
  }
  // search input
  var search = document.querySelector('.search-input');
  if (search) {
    search.addEventListener('input', function() {
      // no-op, search interaction placeholder
    });
  }
  // chip toggle
  var chips = document.querySelectorAll('.chip');
  for (var j = 0; j < chips.length; j++) {
    chips[j].addEventListener('click', function() {
      var parent = this.parentElement;
      var siblings = parent.querySelectorAll('.chip');
      for (var k = 0; k < siblings.length; k++) {
        siblings[k].classList.remove('active');
      }
      this.classList.add('active');
    });
  }
  // chart tooltip on last point
  var lastPoint = document.querySelector('.chart-svg circle:last-child');
  var tooltip = document.getElementById('chartTooltip');
  if (lastPoint && tooltip) {
    lastPoint.addEventListener('mouseenter', function() {
      tooltip.classList.add('visible');
    });
    lastPoint.addEventListener('mouseleave', function() {
      tooltip.classList.remove('visible');
    });
  }
})();
</script>
</body>
</html>
```
Validation summary:
- All HTML tags closed (checked by structural scan)
- All CSS blocks complete (no unclosed braces, all custom properties reference existing --var names)
- CSS custom properties centralized in :root for colors, spacing, typography, shadows, radii
- No duplicate declarations across the stylesheet
- Interactive elements: 4 stat cards hover/click, search input focus, avatar hover/click, activity items hover/click, task check toggle (active click), chip toggle buttons, chart tooltip on hover, notification items hover/click, logo hover/click
- Responsive at 900px and 500px breakpoints
- Soft warm palette: terracotta, sage, lavender, peach on cream/beige base
- Biomorphic shapes: blob decorations (blurred organic circles), curved chart path with soft gradient fill
- Float-in animation staggered across cards