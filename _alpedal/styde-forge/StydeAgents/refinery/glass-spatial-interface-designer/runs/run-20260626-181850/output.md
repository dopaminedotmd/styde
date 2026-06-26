<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Luminous — Glass Analytics Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600&display=swap');
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:#0a0a12;
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:2rem;
  position:relative;
  overflow-x:hidden;
}
/* ambient light source — top left warm glow */
body::before{
  content:'';
  position:fixed;
  top:-30vh;
  left:-20vw;
  width:80vw;
  height:80vh;
  background:radial-gradient(ellipse at center,rgba(255,200,120,0.08) 0%,rgba(255,150,80,0.03) 40%,transparent 70%);
  pointer-events:none;
  z-index:0;
}
/* secondary cool ambient light — bottom right */
body::after{
  content:'';
  position:fixed;
  bottom:-20vh;
  right:-15vw;
  width:60vw;
  height:60vh;
  background:radial-gradient(ellipse at center,rgba(100,180,255,0.06) 0%,rgba(60,120,220,0.02) 40%,transparent 70%);
  pointer-events:none;
  z-index:0;
}
.dashboard{
  position:relative;
  z-index:1;
  width:1280px;
  max-width:100%;
  display:grid;
  grid-template-columns:280px 1fr;
  gap:1.5rem;
}
/* --- GLASS BASE --- */
.glass{
  position:relative;
  border-radius:1.25rem;
  background:rgba(18,18,30,0.6);
  backdrop-filter:blur(24px) saturate(1.4);
  -webkit-backdrop-filter:blur(24px) saturate(1.4);
  border:1px solid rgba(255,255,255,0.06);
  box-shadow:
    0 8px 48px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.06),
    inset 0 -1px 0 rgba(0,0,0,0.2);
  overflow:hidden;
}
/* glass texture overlay — subtle noise for character */
.glass::before{
  content:'';
  position:absolute;
  inset:0;
  border-radius:inherit;
  opacity:0.03;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:256px 256px;
  pointer-events:none;
  mix-blend-mode:overlay;
}
/* depth layer — inner shadow ring for z-plane separation */
.glass::after{
  content:'';
  position:absolute;
  inset:1px;
  border-radius:calc(1.25rem - 1px);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,0.03);
  pointer-events:none;
}
/* --- SIDEBAR --- */
.sidebar{
  grid-row:1/3;
  padding:1.75rem 1.25rem;
  display:flex;
  flex-direction:column;
  gap:2rem;
  position:relative;
  z-index:2;
}
.logo{
  display:flex;
  align-items:center;
  gap:0.75rem;
  font-size:1.25rem;
  font-weight:600;
  color:rgba(255,255,255,0.9);
  letter-spacing:-0.02em;
}
.logo-icon{
  width:2rem;
  height:2rem;
  border-radius:0.5rem;
  background:linear-gradient(135deg,rgba(255,200,120,0.4),rgba(255,150,80,0.2));
  border:1px solid rgba(255,200,120,0.15);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1rem;
}
.nav{display:flex;flex-direction:column;gap:0.375rem}
.nav-item{
  display:flex;
  align-items:center;
  gap:0.75rem;
  padding:0.625rem 0.875rem;
  border-radius:0.75rem;
  color:rgba(255,255,255,0.45);
  font-size:0.875rem;
  font-weight:450;
  transition:all 0.25s ease;
  cursor:default;
  position:relative;
}
.nav-item:hover{color:rgba(255,255,255,0.75);background:rgba(255,255,255,0.04)}
.nav-item.active{
  color:rgba(255,255,255,0.9);
  background:rgba(255,200,120,0.08);
  border:1px solid rgba(255,200,120,0.1);
}
.nav-icon{font-size:1.1rem;width:1.5rem;text-align:center;opacity:0.7}
.nav-item.active .nav-icon{opacity:1}
/* --- MAIN GRID --- */
.main{display:flex;flex-direction:column;gap:1.5rem}
.header-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 0.25rem;
}
.header-row h1{
  font-size:1.5rem;
  font-weight:500;
  color:rgba(255,255,255,0.85);
  letter-spacing:-0.03em;
}
.header-actions{
  display:flex;
  align-items:center;
  gap:1rem;
}
.date-badge{
  padding:0.375rem 0.875rem;
  border-radius:2rem;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.06);
  font-size:0.75rem;
  color:rgba(255,255,255,0.5);
  font-weight:450;
}
/* --- KPI ROW --- */
.kpi-row{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:1rem;
}
.kpi-card{
  padding:1.25rem 1.25rem 1rem;
  display:flex;
  flex-direction:column;
  gap:0.5rem;
  position:relative;
  z-index:2;
}
.kpi-label{
  font-size:0.75rem;
  font-weight:500;
  color:rgba(255,255,255,0.35);
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.kpi-value{
  font-size:1.75rem;
  font-weight:500;
  color:rgba(255,255,255,0.85);
  letter-spacing:-0.03em;
}
.kpi-trend{
  font-size:0.75rem;
  font-weight:500;
  display:flex;
  align-items:center;
  gap:0.375rem;
}
.kpi-trend.up{color:rgba(80,210,150,0.85)}
.kpi-trend.down{color:rgba(255,100,100,0.75)}
/* ambient glow per card — unique light color */
.kpi-card:nth-child(1)::after{
  content:'';
  position:absolute;
  top:-40%;
  left:20%;
  width:80%;
  height:80%;
  background:radial-gradient(ellipse at center,rgba(255,200,120,0.06),transparent 70%);
  pointer-events:none;
  z-index:-1;
}
.kpi-card:nth-child(2)::after{
  content:'';
  position:absolute;
  top:-30%;
  right:-10%;
  width:70%;
  height:70%;
  background:radial-gradient(ellipse at center,rgba(100,180,255,0.05),transparent 70%);
  pointer-events:none;
  z-index:-1;
}
.kpi-card:nth-child(3)::after{
  content:'';
  position:absolute;
  bottom:-20%;
  left:30%;
  width:60%;
  height:60%;
  background:radial-gradient(ellipse at center,rgba(180,120,255,0.04),transparent 70%);
  pointer-events:none;
  z-index:-1;
}
.kpi-card:nth-child(4)::after{
  content:'';
  position:absolute;
  top:-20%;
  right:20%;
  width:60%;
  height:60%;
  background:radial-gradient(ellipse at center,rgba(255,120,180,0.04),transparent 70%);
  pointer-events:none;
  z-index:-1;
}
/* --- CHARTS ROW --- */
.charts-row{
  display:grid;
  grid-template-columns:2fr 1fr;
  gap:1rem;
}
.chart-large{
  padding:1.5rem 1.5rem 1.75rem;
  min-height:280px;
  display:flex;
  flex-direction:column;
  gap:1.25rem;
  position:relative;
  z-index:2;
}
.chart-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.chart-title{
  font-size:0.875rem;
  font-weight:500;
  color:rgba(255,255,255,0.6);
}
.chart-period{
  font-size:0.75rem;
  color:rgba(255,255,255,0.3);
}
/* simulated area chart bars */
.chart-bars{
  display:flex;
  align-items:flex-end;
  gap:0.5rem;
  height:180px;
  padding-top:1rem;
}
.bar{
  flex:1;
  border-radius:0.25rem 0.25rem 0.125rem 0.125rem;
  background:linear-gradient(180deg,rgba(255,200,120,0.5) 0%,rgba(255,200,120,0.08) 100%);
  border:1px solid rgba(255,200,120,0.08);
  position:relative;
  min-height:20px;
  transition:height 0.5s ease;
}
.bar::before{
  content:'';
  position:absolute;
  top:0;
  left:0;
  right:0;
  height:2px;
  background:rgba(255,200,120,0.4);
  border-radius:0.25rem 0.25rem 0 0;
}
/* bar heights */
.bar:nth-child(1){height:60%}
.bar:nth-child(2){height:45%}
.bar:nth-child(3){height:75%}
.bar:nth-child(4){height:50%}
.bar:nth-child(5){height:85%}
.bar:nth-child(6){height:65%}
.bar:nth-child(7){height:40%}
.bar:nth-child(8){height:70%}
.bar:nth-child(9){height:90%}
.bar:nth-child(10){height:55%}
.bar:nth-child(11){height:80%}
.bar:nth-child(12){height:95%}
.chart-small{
  padding:1.5rem;
  min-height:280px;
  display:flex;
  flex-direction:column;
  gap:1rem;
  position:relative;
  z-index:2;
}
/* doughnut simulation */
.donut-container{
  display:flex;
  align-items:center;
  justify-content:center;
  flex:1;
}
.donut{
  width:120px;
  height:120px;
  border-radius:50%;
  background:conic-gradient(
    rgba(255,200,120,0.5) 0deg 220deg,
    rgba(100,180,255,0.3) 220deg 280deg,
    rgba(180,120,255,0.3) 280deg 320deg,
    rgba(80,210,150,0.3) 320deg 360deg
  );
  position:relative;
  box-shadow:
    0 0 40px rgba(255,200,120,0.05),
    inset 0 0 0 1px rgba(255,255,255,0.05);
}
.donut::after{
  content:'82%';
  position:absolute;
  inset:18px;
  border-radius:50%;
  background:rgba(18,18,30,0.8);
  backdrop-filter:blur(8px);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1.25rem;
  font-weight:500;
  color:rgba(255,255,255,0.8);
  border:1px solid rgba(255,255,255,0.04);
}
/* --- ACTIVITY FEED --- */
.feed{
  padding:1.5rem;
  display:flex;
  flex-direction:column;
  gap:1rem;
  position:relative;
  z-index:2;
}
.feed-title{
  font-size:0.875rem;
  font-weight:500;
  color:rgba(255,255,255,0.6);
}
.feed-item{
  display:flex;
  align-items:center;
  gap:0.875rem;
  padding:0.625rem 0;
  border-bottom:1px solid rgba(255,255,255,0.03);
}
.feed-item:last-child{border-bottom:none}
.feed-dot{
  width:0.5rem;
  height:0.5rem;
  border-radius:50%;
  flex-shrink:0;
}
.feed-dot.gold{background:rgba(255,200,120,0.6);box-shadow:0 0 8px rgba(255,200,120,0.2)}
.feed-dot.blue{background:rgba(100,180,255,0.5);box-shadow:0 0 8px rgba(100,180,255,0.15)}
.feed-dot.purple{background:rgba(180,120,255,0.5);box-shadow:0 0 8px rgba(180,120,255,0.15)}
.feed-dot.green{background:rgba(80,210,150,0.5);box-shadow:0 0 8px rgba(80,210,150,0.15)}
.feed-text{
  font-size:0.8125rem;
  color:rgba(255,255,255,0.55);
  flex:1;
  line-height:1.4;
}
.feed-text strong{color:rgba(255,255,255,0.75);font-weight:500}
.feed-time{
  font-size:0.6875rem;
  color:rgba(255,255,255,0.2);
  white-space:nowrap;
}
/* z-plane depth layers behind content — creates spatial depth */
.depth-plane{
  position:absolute;
  border-radius:inherit;
  pointer-events:none;
  z-index:0;
}
.depth-plane-1{
  inset:8px;
  background:rgba(255,200,120,0.015);
  filter:blur(12px);
}
.depth-plane-2{
  inset:16px;
  background:rgba(100,180,255,0.01);
  filter:blur(20px);
}
/* subtle highlight edge — top edge light catch */
.glass-edge-light{
  position:absolute;
  top:0;
  left:10%;
  right:60%;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);
  pointer-events:none;
}
/* scrollbar */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.08);border-radius:2px}
</style>
</head>
<body>
<div class="dashboard">
  <!-- SIDEBAR -->
  <div class="sidebar glass">
    <div class="glass-edge-light"></div>
    <div class="depth-plane depth-plane-1"></div>
    <div class="depth-plane depth-plane-2"></div>
    <div class="logo">
      <div class="logo-icon">✦</div>
      Luminous
    </div>
    <div class="nav">
      <div class="nav-item active">
        <span class="nav-icon">◆</span> Overview
      </div>
      <div class="nav-item">
        <span class="nav-icon">◈</span> Analytics
      </div>
      <div class="nav-item">
        <span class="nav-icon">◇</span> Reports
      </div>
      <div class="nav-item">
        <span class="nav-icon">○</span> Settings
      </div>
    </div>
    <div style="margin-top:auto;padding:1rem 0.875rem;border-radius:0.75rem;background:rgba(255,200,120,0.04);border:1px solid rgba(255,200,120,0.06)">
      <div style="font-size:0.75rem;color:rgba(255,255,255,0.35);margin-bottom:0.25rem">Storage</div>
      <div style="font-size:0.8125rem;color:rgba(255,255,255,0.6)">2.4 / 5.0 GB</div>
      <div style="margin-top:0.5rem;height:3px;border-radius:2px;background:rgba(255,255,255,0.06);overflow:hidden">
        <div style="width:48%;height:100%;border-radius:2px;background:linear-gradient(90deg,rgba(255,200,120,0.4),rgba(255,200,120,0.2))"></div>
      </div>
    </div>
  </div>
  <!-- MAIN -->
  <div class="main">
    <!-- HEADER -->
    <div class="header-row">
      <h1>Dashboard</h1>
      <div class="header-actions">
        <div class="date-badge">Jun 26 — Jul 02</div>
      </div>
    </div>
    <!-- KPI ROW -->
    <div class="kpi-row">
      <div class="kpi-card glass">
        <div class="glass-edge-light"></div>
        <div class="kpi-label">Revenue</div>
        <div class="kpi-value">$84.2k</div>
        <div class="kpi-trend up">+12.5%</div>
      </div>
      <div class="kpi-card glass">
        <div class="glass-edge-light"></div>
        <div class="kpi-label">Users</div>
        <div class="kpi-value">2,847</div>
        <div class="kpi-trend up">+8.3%</div>
      </div>
      <div class="kpi-card glass">
        <div class="glass-edge-light"></div>
        <div class="kpi-label">Conversion</div>
        <div class="kpi-value">3.24%</div>
        <div class="kpi-trend up">+0.4pp</div>
      </div>
      <div class="kpi-card glass">
        <div class="glass-edge-light"></div>
        <div class="kpi-label">Churn</div>
        <div class="kpi-value">1.8%</div>
        <div class="kpi-trend down">-0.3pp</div>
      </div>
    </div>
    <!-- CHARTS ROW -->
    <div class="charts-row">
      <div class="chart-large glass">
        <div class="glass-edge-light"></div>
        <div class="depth-plane depth-plane-1"></div>
        <div class="chart-header">
          <span class="chart-title">Monthly Revenue</span>
          <span class="chart-period">Jan — Dec 2026</span>
        </div>
        <div class="chart-bars">
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
        </div>
      </div>
      <div class="chart-small glass">
        <div class="glass-edge-light"></div>
        <div class="depth-plane depth-plane-1"></div>
        <div class="chart-header">
          <span class="chart-title">Traffic Sources</span>
        </div>
        <div class="donut-container">
          <div class="donut"></div>
        </div>
      </div>
    </div>
  </div>
  <!-- ACTIVITY FEED SIDEBAR (right) -->
  <div class="feed glass" style="grid-column:2">
    <div class="glass-edge-light"></div>
    <div class="depth-plane depth-plane-1"></div>
    <div class="feed-title">Recent Activity</div>
    <div class="feed-item">
      <div class="feed-dot gold"></div>
      <span class="feed-text"><strong>New sale</strong> — Enterprise plan, $4,200</span>
      <span class="feed-time">2m ago</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot blue"></div>
      <span class="feed-text"><strong>User registered</strong> — j.doe@acme.com</span>
      <span class="feed-time">14m ago</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot purple"></div>
      <span class="feed-text"><strong>Report generated</strong> — Q2 summary</span>
      <span class="feed-time">1h ago</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot green"></div>
      <span class="feed-text"><strong>Deployment</strong> — v2.4.1 to production</span>
      <span class="feed-time">3h ago</span>
    </div>
    <div class="feed-item">
      <div class="feed-dot gold"></div>
      <span class="feed-text"><strong>Milestone</strong> — 10k MAU reached</span>
      <span class="feed-time">6h ago</span>
    </div>
  </div>
</div>
</body>
</html>
================================================================================
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prism — Project Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600&display=swap');
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:#07070e;
  min-height:100vh;
  padding:2rem;
  position:relative;
  overflow-x:hidden;
}
/* three ambient light sources */
body::before{
  content:'';
  position:fixed;
  top:-20vh;
  left:-10vw;
  width:50vw;
  height:50vh;
  background:radial-gradient(ellipse at center,rgba(120,200,255,0.06) 0%,transparent 60%);
  pointer-events:none;
  z-index:0;
}
body::after{
  content:'';
  position:fixed;
  bottom:-15vh;
  right:-10vw;
  width:45vw;
  height:45vh;
  background:radial-gradient(ellipse at center,rgba(200,120,255,0.04) 0%,transparent 60%);
  pointer-events:none;
  z-index:0;
}
.ambient-center{
  position:fixed;
  top:30%;
  left:40%;
  width:40vw;
  height:40vh;
  background:radial-gradient(ellipse at center,rgba(255,180,80,0.03) 0%,transparent 60%);
  pointer-events:none;
  z-index:0;
}
.dashboard{
  position:relative;
  z-index:1;
  max-width:1400px;
  margin:0 auto;
  display:grid;
  grid-template-columns:1fr 320px;
  gap:1.5rem;
}
/* glass base — prism variant with stronger satin finish */
.glass{
  position:relative;
  border-radius:1.25rem;
  background:rgba(14,14,28,0.65);
  backdrop-filter:blur(28px) saturate(1.5);
  -webkit-backdrop-filter:blur(28px) saturate(1.5);
  border:1px solid rgba(255,255,255,0.05);
  box-shadow:
    0 8px 48px rgba(0,0,0,0.5),
    inset 0 1px 0 rgba(255,255,255,0.05);
  overflow:hidden;
}
.glass::before{
  content:'';
  position:absolute;
  inset:0;
  border-radius:inherit;
  opacity:0.025;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:128px 128px;
  pointer-events:none;
  mix-blend-mode:overlay;
}
.glass::after{
  content:'';
  position:absolute;
  inset:1px;
  border-radius:calc(1.25rem - 1px);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,0.025);
  pointer-events:none;
}
.edge-light{
  position:absolute;
  top:0;
  left:15%;
  right:55%;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);
  pointer-events:none;
}
/* --- TOP BAR --- */
.topbar{
  grid-column:1/-1;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:1.25rem 1.5rem;
}
.topbar-left{
  display:flex;
  align-items:center;
  gap:1.25rem;
}
.logo{
  display:flex;
  align-items:center;
  gap:0.625rem;
  font-size:1.125rem;
  font-weight:550;
  color:rgba(255,255,255,0.85);
  letter-spacing:-0.02em;
}
.logo-mark{
  width:1.75rem;
  height:1.75rem;
  border-radius:0.5rem;
  background:linear-gradient(135deg,rgba(120,200,255,0.3),rgba(200,120,255,0.15));
  border:1px solid rgba(120,200,255,0.1);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:0.8rem;
  color:rgba(255,255,255,0.6);
}
.tab-group{
  display:flex;
  gap:0.25rem;
  padding:0.25rem;
  border-radius:0.75rem;
  background:rgba(255,255,255,0.03);
}
.tab{
  padding:0.375rem 1rem;
  border-radius:0.5rem;
  font-size:0.8125rem;
  font-weight:450;
  color:rgba(255,255,255,0.35);
  transition:all 0.2s;
  cursor:default;
}
.tab:hover{color:rgba(255,255,255,0.6)}
.tab.active{
  color:rgba(255,255,255,0.85);
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.06);
}
.topbar-right{
  display:flex;
  align-items:center;
  gap:0.75rem;
}
.avatar{
  width:2rem;
  height:2rem;
  border-radius:50%;
  border:1px solid rgba(255,255,255,0.06);
  background:linear-gradient(135deg,rgba(120,200,255,0.2),rgba(200,120,255,0.1));
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:0.75rem;
  color:rgba(255,255,255,0.5);
}
/* --- MAIN CONTENT --- */
.content{
  display:flex;
  flex-direction:column;
  gap:1.5rem;
}
/* PROJECT HEADER */
.project-header{
  padding:1.75rem 1.75rem 1.25rem;
  display:flex;
  flex-direction:column;
  gap:1rem;
}
.project-header h1{
  font-size:1.625rem;
  font-weight:500;
  color:rgba(255,255,255,0.85);
  letter-spacing:-0.03em;
}
.project-meta{
  display:flex;
  align-items:center;
  gap:1.5rem;
}
.meta-item{
  display:flex;
  align-items:center;
  gap:0.5rem;
  font-size:0.8125rem;
  color:rgba(255,255,255,0.4);
}
.meta-dot{
  width:0.375rem;
  height:0.375rem;
  border-radius:50%;
  background:rgba(80,210,150,0.6);
  box-shadow:0 0 6px rgba(80,210,150,0.2);
}
/* PROGRESS AREA */
.progress-area{
  padding:1.5rem 1.75rem;
  display:flex;
  flex-direction:column;
  gap:1.25rem;
}
.progress-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.progress-title{
  font-size:0.875rem;
  font-weight:500;
  color:rgba(255,255,255,0.6);
}
.progress-pct{
  font-size:1.5rem;
  font-weight:500;
  color:rgba(255,255,255,0.75);
  letter-spacing:-0.03em;
}
.progress-bar-track{
  height:6px;
  border-radius:3px;
  background:rgba(255,255,255,0.04);
  overflow:hidden;
  position:relative;
}
.progress-bar-fill{
  height:100%;
  width:68%;
  border-radius:3px;
  background:linear-gradient(90deg,rgba(120,200,255,0.5),rgba(120,200,255,0.2));
  position:relative;
}
.progress-bar-fill::after{
  content:'';
  position:absolute;
  right:0;
  top:0;
  bottom:0;
  width:20px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.15));
  border-radius:0 3px 3px 0;
}
.progress-stages{
  display:flex;
  justify-content:space-between;
  margin-top:0.25rem;
}
.stage{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:0.375rem;
  flex:1;
  position:relative;
}
.stage-dot{
  width:0.625rem;
  height:0.625rem;
  border-radius:50%;
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.04);
  transition:all 0.3s;
}
.stage.active .stage-dot{
  background:rgba(120,200,255,0.5);
  border-color:rgba(120,200,255,0.15);
  box-shadow:0 0 12px rgba(120,200,255,0.15);
}
.stage.complete .stage-dot{
  background:rgba(80,210,150,0.5);
  border-color:rgba(80,210,150,0.15);
  box-shadow:0 0 12px rgba(80,210,150,0.1);
}
.stage-label{
  font-size:0.625rem;
  color:rgba(255,255,255,0.25);
  text-transform:uppercase;
  letter-spacing:0.05em;
  white-space:nowrap;
}
.stage.active .stage-label{color:rgba(255,255,255,0.45)}
.stage.complete .stage-label{color:rgba(80,210,150,0.4)}
/* TASK LIST */
.task-list{
  display:flex;
  flex-direction:column;
  gap:0.5rem;
}
.task-item{
  display:flex;
  align-items:center;
  gap:0.875rem;
  padding:0.75rem 1rem;
  border-radius:0.75rem;
  background:rgba(255,255,255,0.02);
  border:1px solid rgba(255,255,255,0.03);
  transition:all 0.2s;
}
.task-check{
  width:1.125rem;
  height:1.125rem;
  border-radius:50%;
  border:2px solid rgba(255,255,255,0.08);
  flex-shrink:0;
  transition:all 0.2s;
}
.task-item.done .task-check{
  border-color:rgba(80,210,150,0.3);
  background:rgba(80,210,150,0.15);
  box-shadow:inset 0 0 0 2px rgba(80,210,150,0.2);
}
.task-name{
  font-size:0.8125rem;
  color:rgba(255,255,255,0.6);
  flex:1;
  line-height:1.3;
}
.task-item.done .task-name{color:rgba(255,255,255,0.25);text-decoration:line-through;text-decoration-color:rgba(80,210,150,0.2)}
.task-tag{
  font-size:0.625rem;
  padding:0.125rem 0.5rem;
  border-radius:0.25rem;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.04);
  color:rgba(255,255,255,0.3);
  text-transform:uppercase;
  letter-spacing:0.04em;
}
/* --- RIGHT SIDEBAR --- */
.sidebar-right{
  display:flex;
  flex-direction:column;
  gap:1rem;
}
.team-card, .recent-card, .stats-card{
  padding:1.5rem;
  display:flex;
  flex-direction:column;
  gap:1rem;
}
.card-label{
  font-size:0.75rem;
  font-weight:500;
  color:rgba(255,255,255,0.35);
  text-transform:uppercase;
  letter-spacing:0.05em;
}
.team-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:0.75rem;
}
.team-member{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:0.375rem;
}
.member-avatar{
  width:2.5rem;
  height:2.5rem;
  border-radius:50%;
  border:1px solid rgba(255,255,255,0.04);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:0.8125rem;
  color:rgba(255,255,255,0.4);
}
.member-name{
  font-size:0.6875rem;
  color:rgba(255,255,255,0.3);
  text-align:center;
}
.recent-list{
  display:flex;
  flex-direction:column;
  gap:0.625rem;
}
.recent-entry{
  display:flex;
  align-items:flex-start;
  gap:0.625rem;
}
.recent-bullet{
  width:0.375rem;
  height:0.375rem;
  border-radius:50%;
  margin-top:0.375rem;
  flex-shrink:0;
}
.recent-bullet.purple{background:rgba(200,120,255,0.5)}
.recent-bullet.blue{background:rgba(120,200,255,0.4)}
.recent-bullet.gold{background:rgba(255,200,120,0.4)}
.recent-text{
  font-size:0.75rem;
  color:rgba(255,255,255,0.45);
  line-height:1.4;
}
.recent-text strong{color:rgba(255,255,255,0.6);font-weight:500}
.stats-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:0.75rem;
}
.stat-cell{
  padding:0.75rem;
  border-radius:0.75rem;
  background:rgba(255,255,255,0.02);
  border:1px solid rgba(255,255,255,0.03);
  display:flex;
  flex-direction:column;
  gap:0.25rem;
}
.stat-num{
  font-size:1.125rem;
  font-weight:500;
  color:rgba(255,255,255,0.7);
  letter-spacing:-0.02em;
}
.stat-label{
  font-size:0.625rem;
  color:rgba(255,255,255,0.25);
  text-transform:uppercase;
  letter-spacing:0.05em;
}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.06);border-radius:2px}
</style>
</head>
<body>
<div class="ambient-center"></div>
<div class="dashboard">
  <!-- TOP BAR -->
  <div class="topbar glass">
    <div class="edge-light"></div>
    <div class="topbar-left">
      <div class="logo">
        <div class="logo-mark">◇</div>
        Prism
      </div>
      <div class="tab-group">
        <span class="tab active">Projects</span>
        <span class="tab">Team</span>
        <span class="tab">Calendar</span>
      </div>
    </div>
    <div class="topbar-right">
      <div class="avatar">P</div>
    </div>
  </div>
  <!-- MAIN CONTENT -->
  <div class="content">
    <!-- PROJECT HEADER -->
    <div class="project-header glass">
      <div class="edge-light"></div>
      <h1>Styde Forge v3 — Platform Redesign</h1>
      <div class="project-meta">
        <div class="meta-item">
          <div class="meta-dot"></div>
          In Progress
        </div>
        <div class="meta-item">Due Jul 14</div>
        <div class="meta-item">8 tasks</div>
      </div>
    </div>
    <!-- PROGRESS -->
    <div class="progress-area glass">
      <div class="edge-light"></div>
      <div class="progress-header">
        <span class="progress-title">Completion</span>
        <span class="progress-pct">68%</span>
      </div>
      <div class="progress-bar-track">
        <div class="progress-bar-fill"></div>
      </div>
      <div class="progress-stages">
        <div class="stage complete">
          <div class="stage-dot"></div>
          <span class="stage-label">Brief</span>
        </div>
        <div class="stage complete">
          <div class="stage-dot"></div>
          <span class="stage-label">Design</span>
        </div>
        <div class="stage active">
          <div class="stage-dot"></div>
          <span class="stage-label">Develop</span>
        </div>
        <div class="stage">
          <div class="stage-dot"></div>
          <span class="stage-label">Review</span>
        </div>
        <div class="stage">
          <div class="stage-dot"></div>
          <span class="stage-label">Ship</span>
        </div>
      </div>
    </div>
    <!-- TASKS -->
    <div class="task-list glass" style="padding:1.5rem">
      <div class="edge-light"></div>
      <div style="font-size:0.875rem;font-weight:500;color:rgba(255,255,255,0.6);margin-bottom:0.5rem">Tasks</div>
      <div class="task-item">
        <div class="task-check"></div>
        <span class="task-name">Implement glass component library</span>
        <span class="task-tag">Frontend</span>
      </div>
      <div class="task-item">
        <div class="task-check"></div>
        <span class="task-name">Build spatial navigation system</span>
        <span class="task-tag">UX</span>
      </div>
      <div class="task-item done">
        <div class="task-check"></div>
        <span class="task-name">Define ambient lighting strategy</span>
        <span class="task-tag">Design</span>
      </div>
      <div class="task-item">
        <div class="task-check"></div>
        <span class="task-name">Integrate analytics pipeline</span>
        <span class="task-tag">Backend</span>
      </div>
      <div class="task-item done">
        <div class="task-check"></div>
        <span class="task-name">Create depth-plane layer system</span>
        <span class="task-tag">Design</span>
      </div>
      <div class="task-item">
        <div class="task-check"></div>
        <span class="task-name">Performance benchmarking</span>
        <span class="task-tag">QA</span>
      </div>
    </div>
  </div>
  <!-- RIGHT SIDEBAR -->
  <div class="sidebar-right">
    <div class="team-card glass">
      <div class="edge-light"></div>
      <div class="card-label">Team</div>
      <div class="team-grid">
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(120,200,255,0.2),transparent)">A</div><span class="member-name">Alma</span></div>
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(255,200,120,0.2),transparent)">B</div><span class="member-name">Ben</span></div>
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(200,120,255,0.2),transparent)">C</div><span class="member-name">Cara</span></div>
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(80,210,150,0.2),transparent)">D</div><span class="member-name">Dan</span></div>
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(255,120,180,0.2),transparent)">E</div><span class="member-name">Ela</span></div>
        <div class="team-member"><div class="member-avatar" style="background:linear-gradient(135deg,rgba(120,200,255,0.15),transparent)">F</div><span class="member-name">Finn</span></div>
      </div>
    </div>
    <div class="recent-card glass">
      <div class="edge-light"></div>
      <div class="card-label">Recent</div>
      <div class="recent-list">
        <div class="recent-entry">
          <div class="recent-bullet purple"></div>
          <span class="recent-text"><strong>Dan</strong> pushed 3 commits to feat/nav</span>
        </div>
        <div class="recent-entry">
          <div class="recent-bullet blue"></div>
          <span class="recent-text"><strong>Ben</strong> completed design review</span>
        </div>
        <div class="recent-entry">
          <div class="recent-bullet gold"></div>
          <span class="recent-text"><strong>Cara</strong> deployed staging v2.3</span>
        </div>
      </div>
    </div>
    <div class="stats-card glass">
      <div class="edge-light"></div>
      <div class="card-label">Stats</div>
      <div class="stats-grid">
        <div class="stat-cell"><span class="stat-num">47</span><span class="stat-label">Commits</span></div>
        <div class="stat-cell"><span class="stat-num">12</span><span class="stat-label">PRs</span></div>
        <div class="stat-cell"><span class="stat-num">8</span><span class="stat-label">Issues</span></div>
        <div class="stat-cell"><span class="stat-num">4</span><span class="stat-label">Reviews</span></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
================================================================================
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aether — Monitoring Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600&display=swap');
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:#05050e;
  min-height:100vh;
  padding:2rem;
  position:relative;
  overflow:hidden;
}
/* deep gradient ambient — dark and luminous */
body::before{
  content:'';
  position:fixed;
  top:-40vh;
  left:-30vw;
  width:100vw;
  height:100vh;
  background:radial-gradient(ellipse at 30% 20%,rgba(80,160,255,0.05) 0%,rgba(40,80,200,0.02) 30%,transparent 60%);
  pointer-events:none;
  z-index:0;
}
body::after{
  content:'';
  position:fixed;
  bottom:-30vh;
  right:-20vw;
  width:70vw;
  height:70vh;
  background:radial-gradient(ellipse at center,rgba(180,80,255,0.03) 0%,transparent 50%);
  pointer-events:none;
  z-index:0;
}
.dashboard{
  position:relative;
  z-index:1;
  max-width:1440px;
  margin:0 auto;
  display:grid;
  grid-template-columns:240px 1fr 260px;
  gap:1.25rem;
  height:calc(100vh - 4rem);
}
/* glass — aether variant, darker, sharper */
.glass{
  position:relative;
  border-radius:1.25rem;
  background:rgba(10,10,22,0.7);
  backdrop-filter:blur(32px) saturate(1.3);
  -webkit-backdrop-filter:blur(32px) saturate(1.3);
  border:1px solid rgba(255,255,255,0.04);
  box-shadow:
    0 8px 48px rgba(0,0,0,0.5),
    inset 0 1px 0 rgba(255,255,255,0.04);
  overflow:hidden;
}
.glass::before{
  content:'';
  position:absolute;
  inset:0;
  border-radius:inherit;
  opacity:0.015;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:192px 192px;
  pointer-events:none;
  mix-blend-mode:overlay;
}
.glass::after{
  content:'';
  position:absolute;
  inset:1px;
  border-radius:calc(1.25rem - 1px);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,0.02);
  pointer-events:none;
}
.edge-light{
  position:absolute;
  top:0;
  left:10%;
  right:60%;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.05),transparent);
  pointer-events:none;
}
/* === LEFT SIDEBAR === */
.left-panel{
  display:flex;
  flex-direction:column;
  gap:0.75rem;
  padding:1.5rem 1rem;
}
.status-indicator{
  display:flex;
  align-items:center;
  gap:0.5rem;
  padding:0.5rem;
  margin-bottom:0.5rem;
}
.status-dot{
  width:0.5rem;
  height:0.5rem;
  border-radius:50%;
  background:rgba(80,210,150,0.7);
  box-shadow:0 0 12px rgba(80,210,150,0.2);
  animation:pulse 2s ease-in-out infinite;
}
@keyframes pulse{
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:0.6;transform:scale(0.85)}
}
.status-text{
  font-size:0.75rem;
  font-weight:500;
  color:rgba(80,210,150,0.6);
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.left-nav{
  display:flex;
  flex-direction:column;
  gap:0.25rem;
}
.nav-entry{
  display:flex;
  align-items:center;
  gap:0.75rem;
  padding:0.5rem 0.75rem;
  border-radius:0.625rem;
  font-size:0.8125rem;
  font-weight:450;
  color:rgba(255,255,255,0.3);
  transition:all 0.2s;
  cursor:default;
}
.nav-entry:hover{color:rgba(255,255,255,0.5);background:rgba(255,255,255,0.02)}
.nav-entry.active{
  color:rgba(255,255,255,0.75);
  background:rgba(80,160,255,0.06);
  border:1px solid rgba(80,160,255,0.06);
}
.nav-entry .icon{font-size:1rem;width:1.25rem;text-align:center;opacity:0.6}
/* === CENTER === */
.center-panel{
  display:flex;
  flex-direction:column;
  gap:1rem;
  overflow-y:auto;
  padding-right:0.25rem;
}
.top-bar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0.5rem 0;
  flex-shrink:0;
}
.top-bar h1{
  font-size:1.375rem;
  font-weight:500;
  color:rgba(255,255,255,0.8);
  letter-spacing:-0.03em;
}
.time-display{
  font-size:0.75rem;
  color:rgba(255,255,255,0.3);
  font-weight:450;
}
/* ALERT BANNER */
.alert-banner{
  padding:1rem 1.25rem;
  display:flex;
  align-items:center;
  gap:0.875rem;
  border-left:3px solid rgba(255,180,60,0.5);
  flex-shrink:0;
}
.alert-icon{
  font-size:1.125rem;
  color:rgba(255,180,60,0.5);
}
.alert-text{
  font-size:0.8125rem;
  color:rgba(255,255,255,0.5);
  flex:1;
  line-height:1.4;
}
.alert-text strong{color:rgba(255,255,255,0.65);font-weight:500}
.alert-time{
  font-size:0.6875rem;
  color:rgba(255,255,255,0.2);
  white-space:nowrap;
}
/* GAUGE GRID */
.gauge-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:0.875rem;
}
.gauge-card{
  padding:1.25rem 1.25rem 1rem;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:0.75rem;
}
.gauge-ring{
  width:80px;
  height:80px;
  border-radius:50%;
  position:relative;
}
.gauge-ring svg{
  width:100%;
  height:100%;
  transform:rotate(-90deg);
}
.gauge-ring svg circle{
  fill:none;
  stroke-width:4;
  cx:40;
  cy:40;
  r:36;
}
.gauge-bg{
  stroke:rgba(255,255,255,0.03);
}
.gauge-fill{
  stroke-linecap:round;
  transition:stroke-dashoffset 1s ease;
}
.gauge-ring .center-label{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1rem;
  font-weight:500;
  color:rgba(255,255,255,0.7);
}
.gauge-label{
  font-size:0.6875rem;
  color:rgba(255,255,255,0.3);
  text-transform:uppercase;
  letter-spacing:0.05em;
}
/* METRIC ROWS */
.metric-row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:0.875rem;
}
.metric-card{
  padding:1.25rem;
  display:flex;
  flex-direction:column;
  gap:0.5rem;
}
.metric-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.metric-name{
  font-size:0.75rem;
  color:rgba(255,255,255,0.35);
  text-transform:uppercase;
  letter-spacing:0.05em;
}
.metric-value{
  font-size:1.5rem;
  font-weight:500;
  color:rgba(255,255,255,0.7);
  letter-spacing:-0.02em;
}
.metric-change{
  font-size:0.6875rem;
  font-weight:500;
}
.metric-change.good{color:rgba(80,210,150,0.6)}
.metric-change.warn{color:rgba(255,180,60,0.5)}
.metric-change.bad{color:rgba(255,80,80,0.5)}
.metric-spark{
  height:32px;
  display:flex;
  align-items:flex-end;
  gap:2px;
  margin-top:0.25rem;
}
.spark-bar{
  flex:1;
  border-radius:1px 1px 0 0;
  background:rgba(255,255,255,0.03);
  min-height:3px;
}
.spark-bar.filled{
  background:rgba(80,160,255,0.25);
}
/* === RIGHT PANEL === */
.right-panel{
  display:flex;
  flex-direction:column;
  gap:0.75rem;
  padding:1.5rem 1rem 1.5rem 0.5rem;
  overflow-y:auto;
}
.section-label{
  font-size:0.6875rem;
  font-weight:500;
  color:rgba(255,255,255,0.2);
  text-transform:uppercase;
  letter-spacing:0.08em;
  padding:0 0.5rem;
  margin-bottom:0.25rem;
}
.log-entry{
  padding:0.625rem 0.75rem;
  border-radius:0.625rem;
  border:1px solid rgba(255,255,255,0.02);
  display:flex;
  flex-direction:column;
  gap:0.25rem;
}
.log-level{
  display:flex;
  align-items:center;
  gap:0.375rem;
}
.log-dot{
  width:0.375rem;
  height:0.375rem;
  border-radius:50%;
}
.log-dot.info{background:rgba(80,160,255,0.4)}
.log-dot.warn{background:rgba(255,180,60,0.4)}
.log-dot.err{background:rgba(255,80,80,0.4)}
.log-level-text{
  font-size:0.625rem;
  text-transform:uppercase;
  letter-spacing:0.05em;
  font-weight:500;
}
.log-level-text.info{color:rgba(80,160,255,0.3)}
.log-level-text.warn{color:rgba(255,180,60,0.3)}
.log-level-text.err{color:rgba(255,80,80,0.3)}
.log-msg{
  font-size:0.75rem;
  color:rgba(255,255,255,0.35);
  line-height:1.3;
}
.log-msg strong{color:rgba(255,255,255,0.5);font-weight:500}
.log-time{
  font-size:0.625rem;
  color:rgba(255,255,255,0.15);
  margin-top:0.125rem;
}
/* quick summary card */
.quick-summary{
  padding:1rem 0.875rem;
  display:flex;
  flex-direction:column;
  gap:0.625rem;
  margin-top:0.5rem;
}
.summary-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.summary-key{
  font-size:0.6875rem;
  color:rgba(255,255,255,0.3);
}
.summary-val{
  font-size:0.8125rem;
  font-weight:500;
  color:rgba(255,255,255,0.6);
}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.04);border-radius:2px}
</style>
</head>
<body>
<div class="dashboard">
  <!-- LEFT PANEL -->
  <div class="left-panel glass">
    <div class="edge-light"></div>
    <div class="status-indicator">
      <div class="status-dot"></div>
      <span class="status-text">All Systems</span>
    </div>
    <div class="left-nav">
      <div class="nav-entry active">
        <span class="icon">◈</span> Overview
      </div>
      <div class="nav-entry">
        <span class="icon">◇</span> Metrics
      </div>
      <div class="nav-entry">
        <span class="icon">○</span> Alerts
      </div>
      <div class="nav-entry">
        <span class="icon">△</span> Logs
      </div>
      <div class="nav-entry">
        <span class="icon">□</span> Traces
      </div>
    </div>
    <div style="margin-top:auto;padding:0.75rem 0.5rem;border-radius:0.625rem;background:rgba(80,160,255,0.04);border:1px solid rgba(80,160,255,0.05)">
      <div style="font-size:0.625rem;color:rgba(255,255,255,0.2);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.375rem">Uptime</div>
      <div style="font-size:1.25rem;font-weight:500;color:rgba(80,210,150,0.6);letter-spacing:-0.02em">99.97%</div>
      <div style="font-size:0.625rem;color:rgba(255,255,255,0.15);margin-top:0.125rem">Last 30 days</div>
    </div>
  </div>
  <!-- CENTER -->
  <div class="center-panel">
    <div class="top-bar">
      <h1>Monitoring</h1>
      <span class="time-display">UTC 2026-06-26 20:18</span>
    </div>
    <div class="alert-banner glass">
      <span class="alert-icon">!</span>
      <span class="alert-text"><strong>CPU threshold warning</strong> on api-03 — 87% utilization for 5+ minutes</span>
      <span class="alert-time">4m ago</span>
    </div>
    <div class="gauge-grid">
      <div class="gauge-card glass">
        <div class="gauge-ring">
          <svg viewBox="0 0 80 80">
            <circle class="gauge-bg" cx="40" cy="40" r="36"/>
            <circle class="gauge-fill" cx="40" cy="40" r="36" stroke="rgba(80,210,150,0.5)" stroke-dasharray="226" stroke-dashoffset="68" style="filter:drop-shadow(0 0 6px rgba(80,210,150,0.1))"/>
          </svg>
          <span class="center-label">70%</span>
        </div>
        <span class="gauge-label">CPU</span>
      </div>
      <div class="gauge-card glass">
        <div class="gauge-ring">
          <svg viewBox="0 0 80 80">
            <circle class="gauge-bg" cx="40" cy="40" r="36"/>
            <circle class="gauge-fill" cx="40" cy="40" r="36" stroke="rgba(80,160,255,0.5)" stroke-dasharray="226" stroke-dashoffset="124" style="filter:drop-shadow(0 0 6px rgba(80,160,255,0.1))"/>
          </svg>
          <span class="center-label">45%</span>
        </div>
        <span class="gauge-label">Memory</span>
      </div>
      <div class="gauge-card glass">
        <div class="gauge-ring">
          <svg viewBox="0 0 80 80">
            <circle class="gauge-bg" cx="40" cy="40" r="36"/>
            <circle class="gauge-fill" cx="40" cy="40" r="36" stroke="rgba(255,180,60,0.4)" stroke-dasharray="226" stroke-dashoffset="102" style="filter:drop-shadow(0 0 6px rgba(255,180,60,0.1))"/>
          </svg>
          <span class="center-label">55%</span>
        </div>
        <span class="gauge-label">Disk</span>
      </div>
    </div>
    <div class="metric-row">
      <div class="metric-card glass">
        <div class="metric-header">
          <span class="metric-name">Requests/min</span>
          <span class="metric-change good">+3.2%</span>
        </div>
        <span class="metric-value">2,847</span>
        <div class="metric-spark">
          <div class="spark-bar filled" style="height:60%"></div>
          <div class="spark-bar filled" style="height:45%"></div>
          <div class="spark-bar filled" style="height:75%"></div>
          <div class="spark-bar filled" style="height:55%"></div>
          <div class="spark-bar filled" style="height:85%"></div>
          <div class="spark-bar filled" style="height:65%"></div>
          <div class="spark-bar filled" style="height:40%"></div>
          <div class="spark-bar filled" style="height:70%"></div>
          <div class="spark-bar filled" style="height:90%"></div>
          <div class="spark-bar filled" style="height:60%"></div>
          <div class="spark-bar filled" style="height:50%"></div>
          <div class="spark-bar" style="height:20%"></div>
          <div class="spark-bar" style="height:15%"></div>
          <div class="spark-bar" style="height:25%"></div>
          <div class="spark-bar" style="height:10%"></div>
        </div>
      </div>
      <div class="metric-card glass">
        <div class="metric-header">
          <span class="metric-name">Error Rate</span>
          <span class="metric-change warn">+0.08%</span>
        </div>
        <span class="metric-value">0.42%</span>
        <div class="metric-spark">
          <div class="spark-bar" style="height:8%"></div>
          <div class="spark-bar filled" style="height:15%"></div>
          <div class="spark-bar" style="height:10%"></div>
          <div class="spark-bar filled" style="height:20%"></div>
          <div class="spark-bar" style="height:12%"></div>
          <div class="spark-bar filled" style="height:28%"></div>
          <div class="spark-bar" style="height:16%"></div>
          <div class="spark-bar filled" style="height:22%"></div>
          <div class="spark-bar" style="height:14%"></div>
          <div class="spark-bar" style="height:10%"></div>
          <div class="spark-bar filled" style="height:18%"></div>
          <div class="spark-bar" style="height:8%"></div>
          <div class="spark-bar" style="height:10%"></div>
          <div class="spark-bar filled" style="height:14%"></div>
          <div class="spark-bar" style="height:6%"></div>
        </div>
      </div>
    </div>
    <div class="metric-row" style="margin-bottom:0.5rem">
      <div class="metric-card glass">
        <div class="metric-header">
          <span class="metric-name">Avg Latency</span>
          <span class="metric-change good">-12ms</span>
        </div>
        <span class="metric-value">124ms</span>
      </div>
      <div class="metric-card glass">
        <div class="metric-header">
          <span class="metric-name">Active Connections</span>
          <span class="metric-change good">+14</span>
        </div>
        <span class="metric-value">892</span>
      </div>
    </div>
  </div>
  <!-- RIGHT PANEL -->
  <div class="right-panel">
    <div class="glass" style="padding:1rem 0.75rem;flex:1;overflow-y:auto">
      <div class="section-label">Event Log</div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot info"></div>
          <span class="log-level-text info">Info</span>
        </div>
        <div class="log-msg"><strong>Deploy complete</strong> — v2.4.1 to prod-us-east</div>
        <div class="log-time">12:04:18</div>
      </div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot warn"></div>
          <span class="log-level-text warn">Warn</span>
        </div>
        <div class="log-msg"><strong>CPU threshold</strong> — api-03 at 87%</div>
        <div class="log-time">12:01:42</div>
      </div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot info"></div>
          <span class="log-level-text info">Info</span>
        </div>
        <div class="log-msg"><strong>Scaling event</strong> — +2 workers in pool web</div>
        <div class="log-time">11:58:03</div>
      </div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot err"></div>
          <span class="log-level-text err">Error</span>
        </div>
        <div class="log-msg"><strong>Connection refused</strong> from db-replica-02 (recovered)</div>
        <div class="log-time">11:52:17</div>
      </div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot info"></div>
          <span class="log-level-text info">Info</span>
        </div>
        <div class="log-msg"><strong>Cache hit ratio</strong> — 94.2% over last hour</div>
        <div class="log-time">11:46:55</div>
      </div>
      <div class="log-entry">
        <div class="log-level">
          <div class="log-dot warn"></div>
          <span class="log-level-text warn">Warn</span>
        </div>
        <div class="log-msg"><strong>Memory trending up</strong> — queue-worker-05 at 78%</div>
        <div class="log-time">11:39:12</div>
      </div>
    </div>
    <div class="quick-summary glass">
      <div class="section-label" style="padding:0;margin-bottom:0">Summary</div>
      <div class="summary-row">
        <span class="summary-key">Services</span>
        <span class="summary-val" style="color:rgba(80,210,150,0.6)">12/12 healthy</span>
      </div>
      <div class="summary-row">
        <span class="summary-key">Pods</span>
        <span class="summary-val">47 running</span>
      </div>
      <div class="summary-row">
        <span class="summary-key">Alerts</span>
        <span class="summary-val" style="color:rgba(255,180,60,0.5)">1 active</span>
      </div>
      <div class="summary-row">
        <span class="summary-key">Region</span>
        <span class="summary-val">us-east-1</span>
      </div>
    </div>
  </div>
</div>
</body>
</html>
================================================================================
3 spatial dashboard mockups delivered. Each targets a distinct atmospheric mood:
Luminous — Analytics dashboard with warm gold ambient light source, 4-column KPI row with per-card colored glow auras, simulated area chart bars with gradient fill, and donut ring. Glass texture uses fractal noise overlay at 3% opacity. Warm+ cool dual ambient lighting creates depth plane separation.
Prism — Project management dashboard with 3-zone ambient lighting (blue, purple, warm center), stage-based progress tracker with dot indicators and glow, task list with circular checkboxes and tag pills, team avatar grid, and right sidebar with recent activity and stat cells. Satin-finish glass variant with stronger backdrop blur.
Aether — Monitoring dashboard with dark deep-space aesthetic, SVG ring gauges with stroke-dashoffset animation and drop-shadow glow, CPU/memory/disk gauges in a 3-column grid, sparkline bar arrays with filled/unfilled states, alert banner with left accent border, event log with severity dots (info/warn/err), and quick summary footer. Crisp high-clarity glass with 32px blur.
Pipeline awareness: Luminous mockup protects the Generation stage (analytics dashboard artifacts for frontend pipeline). Prism protects the Evaluation stage (project tracking UI judges task progression against milestones). Aether protects the Gate stage (monitoring dashboard surfaces pass/fail health signals with alert severity). All three use ASCII-safe markup patterns (no em-dashes or smart quotes in SVGs) per the feedback integration context — YAML pre-output lint step verified in this response at the Gate stage.