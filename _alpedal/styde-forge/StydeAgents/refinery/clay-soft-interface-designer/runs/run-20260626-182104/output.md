Clay Soft Dashboard — Fas 0.5 Mockup
A single-file HTML dashboard with claymorphism aesthetics. Pastel palette, extruded cards, jelly-like buttons, tactile depth layers.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clay Dashboard</title>
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  body {
    background: #f0ebe3;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .dashboard {
    max-width: 1200px;
    width: 100%;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 2rem;
    align-items: start;
  }
  /* ---- SIDEBAR ---- */
  .sidebar {
    background: #f5f0e9;
    border-radius: 32px;
    padding: 2rem 1.5rem;
    box-shadow:
      10px 10px 20px rgba(174, 162, 147, 0.25),
      -8px -8px 16px rgba(255, 255, 255, 0.7),
      inset 2px 2px 4px rgba(255, 255, 255, 0.6),
      inset -2px -2px 4px rgba(174, 162, 147, 0.1);
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  .logo {
    font-size: 1.6rem;
    font-weight: 700;
    color: #7a6b5d;
    letter-spacing: -0.5px;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e3d9ce;
  }
  .logo span {
    color: #b8a99a;
    font-weight: 300;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    border-radius: 20px;
    color: #7a6b5d;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow:
      5px 5px 10px rgba(174, 162, 147, 0.15),
      -4px -4px 8px rgba(255, 255, 255, 0.5);
  }
  .nav-item:hover {
    transform: translateY(-2px);
    box-shadow:
      8px 8px 16px rgba(174, 162, 147, 0.25),
      -4px -4px 8px rgba(255, 255, 255, 0.6);
  }
  .nav-item.active {
    background: #e8ddd1;
    box-shadow:
      inset 4px 4px 8px rgba(174, 162, 147, 0.2),
      inset -4px -4px 8px rgba(255, 255, 255, 0.6);
    color: #5d4f42;
  }
  .nav-icon {
    width: 28px;
    height: 28px;
    border-radius: 10px;
    background: #ddd3c7;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
  }
  /* ---- MAIN ---- */
  .main {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  /* ---- HEADER ROW ---- */
  .header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-row h1 {
    font-size: 1.8rem;
    font-weight: 600;
    color: #5d4f42;
    letter-spacing: -0.3px;
  }
  .header-row p {
    color: #a69585;
    font-size: 0.95rem;
    margin-top: 4px;
  }
  .profile-badge {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 16px 8px 8px;
    border-radius: 30px;
    background: #f5f0e9;
    box-shadow:
      6px 6px 12px rgba(174, 162, 147, 0.2),
      -4px -4px 8px rgba(255, 255, 255, 0.6);
  }
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #d4c9bc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: #7a6b5d;
    box-shadow:
      inset 2px 2px 4px rgba(255,255,255,0.5),
      inset -2px -2px 4px rgba(174,162,147,0.2);
  }
  /* ---- STAT CARDS ---- */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
  }
  .stat-card {
    background: #f5f0e9;
    border-radius: 28px;
    padding: 1.5rem;
    box-shadow:
      10px 10px 20px rgba(174, 162, 147, 0.2),
      -8px -8px 16px rgba(255, 255, 255, 0.6),
      inset 1px 1px 3px rgba(255, 255, 255, 0.5),
      inset -1px -1px 3px rgba(174, 162, 147, 0.05);
    transition: all 0.3s ease;
    cursor: default;
  }
  .stat-card:hover {
    transform: translateY(-4px);
    box-shadow:
      14px 14px 28px rgba(174, 162, 147, 0.3),
      -8px -8px 16px rgba(255, 255, 255, 0.7);
  }
  .stat-label {
    font-size: 0.85rem;
    color: #a69585;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .stat-value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #5d4f42;
    margin: 8px 0 4px;
  }
  .stat-change {
    font-size: 0.85rem;
    color: #9bb87f;
    font-weight: 600;
  }
  .stat-card.pink { background: #f5e6e8; }
  .stat-card.pink .stat-value { color: #9e6b7a; }
  .stat-card.peach { background: #f5ebe0; }
  .stat-card.peach .stat-value { color: #b8856a; }
  .stat-card.mint { background: #e6f0ea; }
  .stat-card.mint .stat-value { color: #6d9b7a; }
  /* ---- ACTIVITY SECTION ---- */
  .section-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
  }
  .section-label h2 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #5d4f42;
  }
  .section-label a {
    color: #b8a99a;
    font-size: 0.9rem;
    text-decoration: none;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 16px;
    background: #f5f0e9;
    box-shadow:
      4px 4px 8px rgba(174,162,147,0.15),
      -4px -4px 8px rgba(255,255,255,0.5);
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .section-label a:hover {
    transform: translateY(-1px);
    box-shadow:
      6px 6px 12px rgba(174,162,147,0.2),
      -4px -4px 8px rgba(255,255,255,0.6);
  }
  /* ---- ACTIVITY CARDS LAYERED ---- */
  .activity-stack {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
  }
  .activity-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 1rem 1.5rem;
    background: #f5f0e9;
    border-radius: 24px;
    box-shadow:
      6px 6px 12px rgba(174, 162, 147, 0.15),
      -4px -4px 8px rgba(255, 255, 255, 0.5);
    transition: all 0.2s ease;
  }
  .activity-card:hover {
    transform: translateX(4px);
    box-shadow:
      8px 8px 16px rgba(174, 162, 147, 0.2),
      -4px -4px 8px rgba(255, 255, 255, 0.6);
  }
  .activity-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow:
      inset 2px 2px 4px rgba(255,255,255,0.6),
      inset -1px -1px 2px rgba(0,0,0,0.05);
  }
  .activity-dot.pink { background: #e8b4c0; }
  .activity-dot.peach { background: #e8c9b4; }
  .activity-dot.mint { background: #b4d4c0; }
  .activity-dot.lavender { background: #c4bce0; }
  .activity-text {
    flex: 1;
    color: #5d4f42;
    font-size: 0.92rem;
  }
  .activity-text strong {
    font-weight: 600;
  }
  .activity-time {
    color: #b8a99a;
    font-size: 0.82rem;
    font-weight: 500;
  }
  /* ---- MOCK CHART / EXTRA CARD ---- */
  .chart-card {
    background: #f5f0e9;
    border-radius: 28px;
    padding: 1.5rem 2rem;
    box-shadow:
      10px 10px 20px rgba(174, 162, 147, 0.2),
      -8px -8px 16px rgba(255, 255, 255, 0.6);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .chart-bars {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    height: 100px;
    padding: 0.5rem 0;
  }
  .bar {
    flex: 1;
    border-radius: 12px 12px 6px 6px;
    background: #ddd3c7;
    box-shadow:
      inset 3px 0 6px rgba(255,255,255,0.4),
      inset -2px 0 4px rgba(174,162,147,0.15);
    min-height: 20px;
    transition: all 0.3s ease;
  }
  .bar:hover {
    transform: scaleY(1.05);
    transform-origin: bottom;
  }
  .bar.pink { background: #e8b4c0; }
  .bar.peach { background: #e8c9b4; }
  .bar.mint { background: #b4d4c0; }
  .bar.lavender { background: #c4bce0; }
  .bar.coral { background: #e8b4a8; }
  .bar-label {
    display: flex;
    justify-content: space-between;
    color: #a69585;
    font-size: 0.82rem;
    font-weight: 500;
  }
  /* ---- CTA BUTTON ---- */
  .btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 32px;
    border: none;
    border-radius: 24px;
    background: #ddd3c7;
    color: #5d4f42;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow:
      8px 8px 16px rgba(174, 162, 147, 0.25),
      -6px -6px 12px rgba(255, 255, 255, 0.6),
      inset 1px 1px 2px rgba(255,255,255,0.5),
      inset -1px -1px 2px rgba(174,162,147,0.05);
  }
  .btn-primary:hover {
    transform: translateY(-3px);
    box-shadow:
      12px 12px 24px rgba(174, 162, 147, 0.3),
      -6px -6px 12px rgba(255, 255, 255, 0.7);
  }
  .btn-primary:active {
    transform: translateY(1px);
    box-shadow:
      inset 4px 4px 8px rgba(174, 162, 147, 0.2),
      inset -4px -4px 8px rgba(255, 255, 255, 0.5);
  }
  /* ---- RESPONSIVE ---- */
  @media (max-width: 800px) {
    .dashboard {
      grid-template-columns: 1fr;
    }
    .sidebar {
      flex-direction: row;
      flex-wrap: wrap;
      gap: 0.8rem;
      padding: 1rem;
    }
    .stat-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>
</head>
<body>
<div class="dashboard">
  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="logo">styde<span>forge</span></div>
    <div class="nav-item active">
      <div class="nav-icon">&#9679;</div>
      Overview
    </div>
    <div class="nav-item">
      <div class="nav-icon">&#9632;</div>
      Projects
    </div>
    <div class="nav-item">
      <div class="nav-icon">&#9673;</div>
      Agents
    </div>
    <div class="nav-item">
      <div class="nav-icon">&#9641;</div>
      Blueprints
    </div>
    <div class="nav-item">
      <div class="nav-icon">&#9675;</div>
      Settings
    </div>
    <div style="margin-top: auto; padding-top: 1rem;">
      <div class="btn-primary" style="width:100%; padding:12px 0; font-size:0.9rem;">
        + New Blueprint
      </div>
    </div>
  </aside>
  <!-- MAIN -->
  <main class="main">
    <!-- Header -->
    <div class="header-row">
      <div>
        <h1>Dashboard</h1>
        <p>Clay soft. Tactile. Yours.</p>
      </div>
      <div class="profile-badge">
        <div class="avatar">&#9786;</div>
        <span style="font-weight:500; color:#5d4f42; font-size:0.9rem;">Pontus</span>
      </div>
    </div>
    <!-- Stats -->
    <div class="stat-grid">
      <div class="stat-card pink">
        <div class="stat-label">Active Agents</div>
        <div class="stat-value">24</div>
        <div class="stat-change">+3 today</div>
      </div>
      <div class="stat-card peach">
        <div class="stat-label">Blueprints</div>
        <div class="stat-value">46</div>
        <div class="stat-change">+2 in draft</div>
      </div>
      <div class="stat-card mint">
        <div class="stat-label">Success Rate</div>
        <div class="stat-value">94%</div>
        <div class="stat-change">+1.2% this week</div>
      </div>
    </div>
    <!-- Activity -->
    <div class="section-label">
      <h2>Recent Activity</h2>
      <a href="#">View all</a>
    </div>
    <div class="activity-stack">
      <div class="activity-card">
        <div class="activity-dot mint"></div>
        <div class="activity-text"><strong>Blueprint v12</strong> generated — Clay Dashboard variant</div>
        <div class="activity-time">2 min ago</div>
      </div>
      <div class="activity-card">
        <div class="activity-dot pink"></div>
        <div class="activity-text"><strong>Agent Cascade</strong> completed evaluation batch</div>
        <div class="activity-time">14 min ago</div>
      </div>
      <div class="activity-card">
        <div class="activity-dot peach"></div>
        <div class="activity-text"><strong>PrecisionForge</strong> improved PlanPrompt to v8</div>
        <div class="activity-time">1 hr ago</div>
      </div>
      <div class="activity-card">
        <div class="activity-dot lavender"></div>
        <div class="activity-text"><strong>Forge</strong> deployed 3 new production agents</div>
        <div class="activity-time">3 hr ago</div>
      </div>
    </div>
    <!-- Chart -->
    <div class="chart-card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-weight:600; color:#5d4f42; font-size:1rem;">Weekly Output</span>
        <span style="color:#a69585; font-size:0.85rem;">last 7 days</span>
      </div>
      <div class="chart-bars">
        <div class="bar pink" style="height:48px;"></div>
        <div class="bar peach" style="height:72px;"></div>
        <div class="bar mint" style="height:55px;"></div>
        <div class="bar lavender" style="height:90px;"></div>
        <div class="bar coral" style="height:65px;"></div>
        <div class="bar pink" style="height:80px;"></div>
        <div class="bar peach" style="height:45px;"></div>
      </div>
      <div class="bar-label">
        <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span>
        <span>Fri</span><span>Sat</span><span>Sun</span>
      </div>
    </div>
  </main>
</div>
</body>
</html>
```
Tactile design decisions:
- Double-shadow extrusion on every card. Light source top-left (white shadows), bottom-right (warm brown shadows). Creates clay puffiness.
- inset shadows on avatars, dots, and bars for internal depth — the squeezed-in look.
- Pastel palette: warm beige base (#f5f0e9), pink/mint/peach/lavender accent variants. No pure greys, no stark whites.
- 24px-32px border radius range. Even small elements (nav items, dots) get radius. Nothing has sharp edges.
- Hover lift: cards rise 4px, shadows widen 40%. Feels responsive to touch.
- Active nav state uses inset shadows — pushed-in clay look.
- Button active state mirrors pressed clay — inset shadows replace extruded ones.
- Chart bars have inset highlights mimicking rounded clay columns.
- Layout: sidebar + main grid, but at desktop scale the sidebar itself feels like a stacked clay panel.
- Profile badge is a pill-shaped extruded chip.
Open the file in browser to see the clay interface. Adjust pastel hex values to match brand palette.