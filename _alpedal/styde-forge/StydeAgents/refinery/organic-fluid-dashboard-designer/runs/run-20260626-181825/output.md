mockup-1-organic-metrics.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organic Metrics</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  @import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');
  body{font-family:'Inter',-apple-system,sans-serif;background:linear-gradient(145deg,#fdf6f0 0%,#f8ede4 50%,#f5e6dc 100%);min-height:100vh;padding:32px;display:flex;align-items:center;justify-content:center;}
  .dashboard{max-width:1200px;width:100%;display:grid;grid-template-columns:240px 1fr;gap:28px;position:relative;}
  .blob-deco{position:fixed;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle at 30% 40%,rgba(255,175,150,0.25),rgba(200,140,180,0.12) 60%,transparent 80%);top:-200px;right:-150px;z-index:0;pointer-events:none;filter:blur(60px);}
  .blob-deco-2{position:fixed;width:500px;height:500px;border-radius:42% 58% 70% 30% / 45% 55% 45% 55%;background:radial-gradient(circle at 70% 60%,rgba(160,210,200,0.2),rgba(140,190,210,0.08) 60%,transparent 80%);bottom:-200px;left:-100px;z-index:0;pointer-events:none;filter:blur(50px);animation:floatBlob 20s ease-in-out infinite;}
  @keyframes floatBlob{0%,100%{border-radius:42% 58% 70% 30% / 45% 55% 45% 55%;transform:translate(0,0) rotate(0deg);}33%{border-radius:55% 45% 35% 65% / 60% 40% 60% 40%;transform:translate(20px,-15px) rotate(5deg);}66%{border-radius:38% 62% 55% 45% / 50% 60% 40% 50%;transform:translate(-10px,12px) rotate(-3deg);}}
  .sidebar{background:rgba(255,252,249,0.7);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-radius:28px;border:1px solid rgba(255,255,255,0.5);padding:24px 16px;height:fit-content;position:sticky;top:32px;z-index:1;}
  .sidebar-brand{display:flex;align-items:center;gap:10px;margin-bottom:32px;padding:0 8px;}
  .sidebar-brand-icon{width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,#f7a58c,#e88dcc);display:flex;align-items:center;justify-content:center;color:white;font-size:18px;font-weight:600;box-shadow:0 4px 12px rgba(247,165,140,0.35);}
  .sidebar-brand-text{font-size:16px;font-weight:600;color:#4a3f3a;letter-spacing:-0.3px;}
  .nav-item{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;color:#7a6f6a;font-size:14px;font-weight:450;transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);cursor:pointer;margin-bottom:2px;}
  .nav-item:hover{background:rgba(247,165,140,0.12);color:#4a3f3a;transform:translateX(3px);}
  .nav-item.active{background:linear-gradient(135deg,rgba(247,165,140,0.2),rgba(232,141,204,0.12));color:#d4765e;font-weight:500;box-shadow:inset 0 1px 0 rgba(255,255,255,0.6);}
  .nav-item svg{width:18px;height:18px;opacity:0.7;flex-shrink:0;}
  .nav-item.active svg{opacity:1;}
  .main{z-index:1;}
  .header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:28px;}
  .header-left h1{font-size:28px;font-weight:600;color:#3a2f2a;letter-spacing:-0.5px;margin-bottom:4px;}
  .header-left p{font-size:14px;color:#9a8f8a;}
  .header-right{display:flex;align-items:center;gap:16px;}
  .search-bar{background:rgba(255,252,249,0.7);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.4);border-radius:20px;padding:10px 18px;display:flex;align-items:center;gap:8px;font-size:13px;color:#9a8f8a;min-width:200px;transition:all 0.3s;}
  .search-bar:focus-within{background:rgba(255,252,249,0.9);border-color:rgba(247,165,140,0.4);box-shadow:0 0 0 4px rgba(247,165,140,0.08);}
  .date-badge{background:rgba(255,252,249,0.7);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.4);border-radius:20px;padding:10px 18px;font-size:13px;color:#5a4f4a;}
  .kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px;}
  .kpi-card{background:rgba(255,252,249,0.65);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);border-radius:22px;border:1px solid rgba(255,255,255,0.45);padding:20px;transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);cursor:pointer;position:relative;overflow:hidden;}
  .kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:22px 22px 0 0;opacity:0;transition:opacity 0.3s;}
  .kpi-card:hover::before{opacity:1;}
  .kpi-card:hover{transform:translateY(-4px);background:rgba(255,252,249,0.8);box-shadow:0 12px 40px rgba(0,0,0,0.04);}
  .kpi-card:nth-child(1)::before{background:linear-gradient(90deg,#f7a58c,#f5c4a0);}
  .kpi-card:nth-child(2)::before{background:linear-gradient(90deg,#e88dcc,#c49ddb);}
  .kpi-card:nth-child(3)::before{background:linear-gradient(90deg,#7ed4c8,#a8e0d0);}
  .kpi-card:nth-child(4)::before{background:linear-gradient(90deg,#f5c4a0,#f7a58c);}
  .kpi-label{font-size:12px;color:#9a8f8a;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;}
  .kpi-value{font-size:32px;font-weight:650;color:#3a2f2a;letter-spacing:-1px;margin-bottom:4px;}
  .kpi-change{font-size:12px;display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:10px;}
  .kpi-change.up{background:rgba(126,212,200,0.15);color:#3a9e92;}
  .kpi-change.down{background:rgba(247,165,140,0.15);color:#d4765e;}
  .kpi-icon{position:absolute;top:16px;right:16px;width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:16px;opacity:0.2;}
  .charts-row{display:grid;grid-template-columns:2fr 1fr;gap:20px;margin-bottom:28px;}
  .chart-card{background:rgba(255,252,249,0.65);backdrop-filter:blur(15px);border-radius:22px;border:1px solid rgba(255,255,255,0.45);padding:24px;}
  .chart-card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;}
  .chart-card-header h3{font-size:16px;font-weight:550;color:#3a2f2a;}
  .chart-card-header select{background:rgba(255,252,249,0.5);border:1px solid rgba(200,190,185,0.3);border-radius:12px;padding:6px 12px;font-size:12px;color:#5a4f4a;cursor:pointer;font-family:inherit;}
  .chart-area{height:180px;display:flex;align-items:flex-end;gap:8px;padding-top:12px;}
  .bar-group{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end;}
  .bar{width:100%;max-width:36px;border-radius:8px 8px 4px 4px;min-height:4px;transition:height 0.6s cubic-bezier(0.34,1.56,0.64,1);position:relative;}
  .bar::after{content:attr(data-val);position:absolute;top:-20px;left:50%;transform:translateX(-50%);font-size:10px;color:#7a6f6a;opacity:0;transition:opacity 0.3s;}
  .bar-group:hover .bar::after{opacity:1;}
  .bar-group .bar-label{font-size:10px;color:#9a8f8a;margin-top:2px;}
  .bar-1{background:linear-gradient(180deg,#f7a58c,#f5c4a0);}
  .bar-2{background:linear-gradient(180deg,#e88dcc,#c49ddb);}
  .bar-3{background:linear-gradient(180deg,#7ed4c8,#a8e0d0);}
  .pie-container{display:flex;flex-direction:column;align-items:center;justify-content:center;height:180px;gap:16px;}
  .pie-visual{width:100px;height:100px;border-radius:50%;background:conic-gradient(#f7a58c 0% 45%,#e88dcc 45% 70%,#7ed4c8 70% 88%,#f5c4a0 88% 100%);position:relative;box-shadow:0 4px 20px rgba(247,165,140,0.15);}
  .pie-visual::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:40px;height:40px;border-radius:50%;background:#fdf6f0;}
  .pie-legend{display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:center;}
  .pie-legend-item{display:flex;align-items:center;gap:6px;font-size:11px;color:#5a4f4a;}
  .pie-legend-dot{width:8px;height:8px;border-radius:4px;}
  .activity-card{background:rgba(255,252,249,0.65);backdrop-filter:blur(15px);border-radius:22px;border:1px solid rgba(255,255,255,0.45);padding:24px;}
  .activity-card h3{font-size:16px;font-weight:550;color:#3a2f2a;margin-bottom:16px;}
  .activity-item{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid rgba(200,190,185,0.12);}
  .activity-item:last-child{border-bottom:none;}
  .activity-avatar{width:38px;height:38px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;color:white;}
  .activity-avatar.a1{background:linear-gradient(135deg,#f7a58c,#f5c4a0);}
  .activity-avatar.a2{background:linear-gradient(135deg,#e88dcc,#c49ddb);}
  .activity-avatar.a3{background:linear-gradient(135deg,#7ed4c8,#a8e0d0);}
  .activity-avatar.a4{background:linear-gradient(135deg,#f5c4a0,#f7a58c);}
  .activity-content{flex:1;}
  .activity-text{font-size:13px;color:#3a2f2a;line-height:1.4;}
  .activity-text strong{font-weight:550;}
  .activity-time{font-size:11px;color:#9a8f8a;margin-top:3px;}
  @media (max-width:900px){.dashboard{grid-template-columns:1fr;}.sidebar{position:static;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;}.kpi-grid{grid-template-columns:repeat(2,1fr);}.charts-row{grid-template-columns:1fr;}}
  @media (max-width:600px){.kpi-grid{grid-template-columns:1fr;}.header{flex-direction:column;gap:16px;}}
</style>
</head>
<body>
<div class="blob-deco"></div>
<div class="blob-deco-2"></div>
<div class="dashboard">
  <aside class="sidebar">
    <div class="sidebar-brand"><div class="sidebar-brand-icon">~</div><span class="sidebar-brand-text">drift</span></div>
    <div class="nav-item active"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></svg>Overview</div>
    <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>Analytics</div>
    <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>Team</div>
    <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>Settings</div>
  </aside>
  <main class="main">
    <div class="header">
      <div class="header-left">
        <h1>Good morning</h1>
        <p>Here's what's happening with your projects today.</p>
      </div>
      <div class="header-right">
        <div class="search-bar"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>Search anything...</div>
        <div class="date-badge">Jun 26, 2026</div>
      </div>
    </div>
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-icon">~</div><div class="kpi-label">Active Users</div><div class="kpi-value">2,847</div><div class="kpi-change up">+12.3%</div></div>
      <div class="kpi-card"><div class="kpi-icon">~</div><div class="kpi-label">Revenue</div><div class="kpi-value">$48.2k</div><div class="kpi-change up">+8.1%</div></div>
      <div class="kpi-card"><div class="kpi-icon">~</div><div class="kpi-label">Conversion</div><div class="kpi-value">3.42%</div><div class="kpi-change up">+1.6%</div></div>
      <div class="kpi-card"><div class="kpi-icon">~</div><div class="kpi-label">Bounce</div><div class="kpi-value">18.3%</div><div class="kpi-change down">-2.4%</div></div>
    </div>
    <div class="charts-row">
      <div class="chart-card"><div class="chart-card-header"><h3>Weekly Activity</h3><select><option>Last 7 days</option><option>Last 30 days</option></select></div><div class="chart-area"><div class="bar-group"><div class="bar bar-1" style="height:75%" data-val="2.1k"></div><span class="bar-label">Mon</span></div><div class="bar-group"><div class="bar bar-2" style="height:55%" data-val="1.5k"></div><span class="bar-label">Tue</span></div><div class="bar-group"><div class="bar bar-1" style="height:85%" data-val="2.4k"></div><span class="bar-label">Wed</span></div><div class="bar-group"><div class="bar bar-3" style="height:65%" data-val="1.8k"></div><span class="bar-label">Thu</span></div><div class="bar-group"><div class="bar bar-2" style="height:90%" data-val="2.6k"></div><span class="bar-label">Fri</span></div><div class="bar-group"><div class="bar bar-3" style="height:40%" data-val="1.1k"></div><span class="bar-label">Sat</span></div><div class="bar-group"><div class="bar bar-1" style="height:50%" data-val="1.4k"></div><span class="bar-label">Sun</span></div></div></div>
      <div class="chart-card"><div class="chart-card-header"><h3>Traffic Sources</h3></div><div class="pie-container"><div class="pie-visual"></div><div class="pie-legend"><div class="pie-legend-item"><div class="pie-legend-dot" style="background:#f7a58c"></div>Direct 45%</div><div class="pie-legend-item"><div class="pie-legend-dot" style="background:#e88dcc"></div>Organic 25%</div><div class="pie-legend-item"><div class="pie-legend-dot" style="background:#7ed4c8"></div>Referral 18%</div><div class="pie-legend-item"><div class="pie-legend-dot" style="background:#f5c4a0"></div>Social 12%</div></div></div></div>
    </div>
    <div class="activity-card"><h3>Recent Activity</h3><div class="activity-item"><div class="activity-avatar a1">JD</div><div class="activity-content"><div class="activity-text"><strong>Jordan</strong> deployed <strong>v2.4.1</strong> to production</div><div class="activity-time">12 min ago</div></div></div><div class="activity-item"><div class="activity-avatar a2">SK</div><div class="activity-content"><div class="activity-text"><strong>Sam</strong> completed <strong>UI audit</strong> — 14 issues resolved</div><div class="activity-time">1h ago</div></div></div><div class="activity-item"><div class="activity-avatar a3">AL</div><div class="activity-content"><div class="activity-text"><strong>Alex</strong> merged <strong>payment-integration</strong> branch</div><div class="activity-time">3h ago</div></div></div><div class="activity-item"><div class="activity-avatar a4">CM</div><div class="activity-content"><div class="activity-text"><strong>Casey</strong> uploaded <strong>Q3 roadmap</strong> to drive</div><div class="activity-time">5h ago</div></div></div></div>
  </main>
</div>
</body>
</html>
```
mockup-2-organic-team.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organic Team</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  @import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');
  body{font-family:'Inter',-apple-system,sans-serif;background:linear-gradient(160deg,#f5f0fa 0%,#efe8f5 40%,#f0edf8 100%);min-height:100vh;padding:32px;display:flex;align-items:center;justify-content:center;}
  .dashboard{max-width:1100px;width:100%;display:grid;grid-template-columns:1fr 320px;gap:24px;position:relative;}
  .blob{position:fixed;width:550px;height:550px;border-radius:55% 45% 65% 35% / 50% 60% 40% 50%;background:radial-gradient(circle at 40% 50%,rgba(200,170,230,0.2),rgba(180,150,220,0.08) 55%,transparent 80%);top:-180px;left:-120px;z-index:0;pointer-events:none;filter:blur(60px);animation:morphBlob 25s ease-in-out infinite;}
  @keyframes morphBlob{0%,100%{border-radius:55% 45% 65% 35% / 50% 60% 40% 50%;transform:translate(0,0) rotate(0deg);}25%{border-radius:40% 60% 45% 55% / 55% 40% 60% 45%;transform:translate(30px,-20px) rotate(8deg);}50%{border-radius:60% 40% 50% 50% / 45% 55% 45% 55%;transform:translate(-15px,25px) rotate(-5deg);}75%{border-radius:50% 50% 60% 40% / 40% 50% 50% 60%;transform:translate(20px,10px) rotate(4deg);}}
  .blob-2{position:fixed;width:400px;height:400px;border-radius:40% 60% 55% 45% / 50% 35% 65% 50%;background:radial-gradient(circle at 60% 40%,rgba(180,210,230,0.18),rgba(160,200,220,0.06) 60%,transparent 80%);bottom:-150px;right:-80px;z-index:0;pointer-events:none;filter:blur(40px);animation:morphBlob2 22s ease-in-out infinite;}
  @keyframes morphBlob2{0%,100%{border-radius:40% 60% 55% 45% / 50% 35% 65% 50%;transform:translate(0,0);}50%{border-radius:55% 45% 40% 60% / 40% 60% 40% 60%;transform:translate(-20px,15px);}}
  .team-section{z-index:1;}
  .section-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;}
  .section-header h1{font-size:28px;font-weight:600;color:#3d2f4a;letter-spacing:-0.5px;}
  .section-header p{font-size:14px;color:#8a7a9a;margin-top:2px;}
  .actions{display:flex;gap:10px;}
  .btn{background:rgba(255,252,255,0.65);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.4);border-radius:16px;padding:10px 20px;font-size:13px;color:#3d2f4a;cursor:pointer;transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);font-family:inherit;font-weight:450;}
  .btn-primary{background:linear-gradient(135deg,#c49ddb,#e88dcc);color:white;border:none;box-shadow:0 4px 16px rgba(196,157,219,0.3);}
  .btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(196,157,219,0.35);}
  .btn:hover{transform:translateY(-2px);background:rgba(255,252,255,0.8);}
  .team-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px;margin-bottom:28px;}
  .member-card{background:rgba(255,252,255,0.6);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);border-radius:24px;border:1px solid rgba(255,255,255,0.5);padding:24px 20px 20px;text-align:center;transition:all 0.35s cubic-bezier(0.34,1.56,0.64,1);cursor:pointer;position:relative;overflow:hidden;}
  .member-card::after{content:'';position:absolute;top:-60%;left:-60%;width:120%;height:120%;background:radial-gradient(circle at 50% 30%,rgba(196,157,219,0.06),transparent 60%);opacity:0;transition:opacity 0.4s;pointer-events:none;}
  .member-card:hover::after{opacity:1;}
  .member-card:hover{transform:translateY(-5px);background:rgba(255,252,255,0.75);box-shadow:0 16px 48px rgba(0,0,0,0.04);}
  .member-avatar{width:64px;height:64px;border-radius:20px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:500;color:white;box-shadow:0 4px 14px rgba(0,0,0,0.06);transition:transform 0.3s;}
  .member-card:hover .member-avatar{transform:scale(1.05) rotate(-3deg);}
  .member-name{font-size:15px;font-weight:550;color:#3d2f4a;margin-bottom:2px;}
  .member-role{font-size:12px;color:#8a7a9a;margin-bottom:12px;}
  .member-status{display:inline-flex;align-items:center;gap:5px;font-size:11px;padding:4px 12px;border-radius:12px;}
  .member-status.online{background:rgba(120,200,180,0.15);color:#3a8a7a;}
  .member-status.away{background:rgba(247,200,140,0.15);color:#b87a3a;}
  .member-status.offline{background:rgba(180,170,190,0.12);color:#7a6a8a;}
  .activity-feed{z-index:1;}
  .feed-card{background:rgba(255,252,255,0.65);backdrop-filter:blur(15px);border-radius:24px;border:1px solid rgba(255,255,255,0.45);padding:24px;height:fit-content;position:sticky;top:32px;}
  .feed-card h3{font-size:16px;font-weight:550;color:#3d2f4a;margin-bottom:18px;display:flex;align-items:center;gap:8px;}
  .feed-card h3::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(180,170,190,0.2),transparent);}
  .feed-item{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid rgba(180,170,190,0.08);}
  .feed-item:last-child{border-bottom:none;padding-bottom:0;}
  .feed-dot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0;}
  .feed-dot.purple{background:#c49ddb;box-shadow:0 0 8px rgba(196,157,219,0.3);}
  .feed-dot.coral{background:#e88dcc;box-shadow:0 0 8px rgba(232,141,204,0.3);}
  .feed-dot.teal{background:#7ed4c8;box-shadow:0 0 8px rgba(126,212,200,0.3);}
  .feed-text{font-size:13px;color:#3d2f4a;line-height:1.4;}
  .feed-text strong{font-weight:550;}
  .feed-time{font-size:11px;color:#8a7a9a;margin-top:3px;}
  .project-badge{display:inline-flex;align-items:center;gap:4px;background:rgba(196,157,219,0.1);border-radius:8px;padding:2px 8px;font-size:11px;color:#7a4a9a;margin-top:6px;}
  .upcoming-card{background:rgba(196,157,219,0.06);border-radius:18px;padding:16px;margin-top:18px;}
  .upcoming-card h4{font-size:13px;font-weight:500;color:#5a4a6a;margin-bottom:8px;}
  .upcoming-item{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(180,170,190,0.06);}
  .upcoming-item:last-child{border-bottom:none;}
  .upcoming-label{font-size:12px;color:#3d2f4a;}
  .upcoming-time{font-size:11px;color:#8a7a9a;}
</style>
</head>
<body>
<div class="blob"></div>
<div class="blob-2"></div>
<div class="dashboard">
  <div class="team-section">
    <div class="section-header">
      <div><h1>Team</h1><p>8 members active this week</p></div>
      <div class="actions"><button class="btn">Filter</button><button class="btn btn-primary">+ Invite</button></div>
    </div>
    <div class="team-grid">
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#c49ddb,#b388d6);">AD</div><div class="member-name">Aria Delgado</div><div class="member-role">Lead Designer</div><div class="member-status online">~ online</div></div>
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#e88dcc,#d47abc);">MR</div><div class="member-name">Marcus Reed</div><div class="member-role">Frontend Lead</div><div class="member-status online">~ online</div></div>
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#7ed4c8,#5cc4b8);">LW</div><div class="member-name">Lena Wu</div><div class="member-role">Backend Engineer</div><div class="member-status away">~ away</div></div>
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#f5c4a0,#f0ad80);">TP</div><div class="member-name">Tom Park</div><div class="member-role">Product Manager</div><div class="member-status away">~ away</div></div>
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#c49ddb,#e88dcc);">SJ</div><div class="member-name">Sasha Jovan</div><div class="member-role">Data Analyst</div><div class="member-status online">~ online</div></div>
      <div class="member-card"><div class="member-avatar" style="background:linear-gradient(135deg,#a8d8d0,#7ed4c8);">CO</div><div class="member-name">Cameron Okafor</div><div class="member-role">DevOps</div><div class="member-status offline">~ offline</div></div>
    </div>
  </div>
  <aside class="activity-feed">
    <div class="feed-card">
      <h3>Activity</h3>
      <div class="feed-item"><div class="feed-dot purple"></div><div><div class="feed-text"><strong>Aria</strong> pushed 3 new mockups to <strong>design-system</strong></div><div class="feed-time">8 min ago</div><div class="project-badge">design-system</div></div></div>
      <div class="feed-item"><div class="feed-dot coral"></div><div><div class="feed-text"><strong>Marcus</strong> deployed <strong>component-library</strong> to staging</div><div class="feed-time">32 min ago</div></div></div>
      <div class="feed-item"><div class="feed-dot teal"></div><div><div class="feed-text"><strong>Lena</strong> resolved <strong>API rate-limiting</strong> issue #847</div><div class="feed-time">2h ago</div></div></div>
      <div class="feed-item"><div class="feed-dot purple"></div><div><div class="feed-text"><strong>Tom</strong> uploaded <strong>Q3 roadmap</strong> to team drive</div><div class="feed-time">4h ago</div></div></div>
      <div class="upcoming-card">
        <h4>Upcoming</h4>
        <div class="upcoming-item"><span class="upcoming-label">Sprint review</span><span class="upcoming-time">Tomorrow 10:00</span></div>
        <div class="upcoming-item"><span class="upcoming-label">Design critique</span><span class="upcoming-time">Tomorrow 14:00</span></div>
        <div class="upcoming-item"><span class="upcoming-label">Deployment window</span><span class="upcoming-time">Thu 16:00</span></div>
      </div>
    </div>
  </aside>
</div>
</body>
</html>
```
mockup-3-organic-projects.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organic Projects</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  @import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&display=swap');
  body{font-family:'Inter',-apple-system,sans-serif;background:linear-gradient(155deg,#f2f8f0 0%,#eaf3e8 50%,#f0f6ee 100%);min-height:100vh;padding:32px;display:flex;align-items:center;justify-content:center;}
  .dashboard{max-width:1200px;width:100%;position:relative;}
  .blob-green{position:fixed;width:500px;height:500px;border-radius:50% 50% 40% 60% / 60% 40% 60% 40%;background:radial-gradient(circle at 50% 40%,rgba(160,210,170,0.2),rgba(140,200,160,0.06) 60%,transparent 80%);top:-120px;right:-80px;z-index:0;pointer-events:none;filter:blur(55px);animation:driftGreen 24s ease-in-out infinite;}
  @keyframes driftGreen{0%,100%{border-radius:50% 50% 40% 60% / 60% 40% 60% 40%;transform:translate(0,0) rotate(0deg);}33%{border-radius:45% 55% 55% 45% / 50% 55% 45% 50%;transform:translate(15px,-20px) rotate(6deg);}66%{border-radius:55% 45% 40% 60% / 40% 60% 40% 60%;transform:translate(-10px,15px) rotate(-4deg);}}
  .blob-earth{position:fixed;width:400px;height:400px;border-radius:45% 55% 60% 40% / 50% 45% 55% 50%;background:radial-gradient(circle at 60% 50%,rgba(220,190,160,0.18),rgba(200,175,150,0.05) 60%,transparent 80%);bottom:-100px;left:-80px;z-index:0;pointer-events:none;filter:blur(45px);animation:driftEarth 20s ease-in-out infinite;}
  @keyframes driftEarth{0%,100%{border-radius:45% 55% 60% 40% / 50% 45% 55% 50%;}50%{border-radius:55% 45% 35% 65% / 45% 55% 45% 55%;transform:translate(15px,-10px);}}
  .content{z-index:1;position:relative;}
  .header{display:flex;justify-content:space-between;align-items:center;margin-bottom:28px;}
  .header-left h1{font-size:28px;font-weight:600;color:#2a3f30;letter-spacing:-0.5px;}
  .header-left p{font-size:14px;color:#6a8a6a;}
  .header-right{display:flex;gap:10px;}
  .btn-earth{background:rgba(255,255,250,0.65);backdrop-filter:blur(15px);border:1px solid rgba(200,210,190,0.3);border-radius:16px;padding:10px 20px;font-size:13px;color:#2a3f30;cursor:pointer;transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);font-family:inherit;font-weight:450;}
  .btn-earth-primary{background:linear-gradient(135deg,#8bc48a,#6db879);color:white;border:none;box-shadow:0 4px 16px rgba(107,184,121,0.3);}
  .btn-earth-primary:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(107,184,121,0.35);}
  .btn-earth:hover{transform:translateY(-2px);background:rgba(255,255,250,0.8);}
  .project-list{display:flex;flex-direction:column;gap:16px;}
  .project-card{background:rgba(255,255,250,0.6);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);border-radius:24px;border:1px solid rgba(255,255,255,0.5);padding:22px 24px;transition:all 0.35s cubic-bezier(0.34,1.56,0.64,1);cursor:pointer;position:relative;overflow:hidden;}
  .project-card::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;border-radius:0 4px 4px 0;opacity:0;transition:opacity 0.3s;}
  .project-card:hover::before{opacity:1;}
  .project-card:hover{transform:translateX(4px);background:rgba(255,255,250,0.75);box-shadow:0 12px 40px rgba(0,0,0,0.03);}
  .project-card.p1::before{background:linear-gradient(180deg,#8bc48a,#6db879);}
  .project-card.p2::before{background:linear-gradient(180deg,#c4a97b,#d4b88a);}
  .project-card.p3::before{background:linear-gradient(180deg,#a0b8d0,#8aa8c4);}
  .project-card.p4::before{background:linear-gradient(180deg,#d4a088,#c49078);}
  .project-card.p5::before{background:linear-gradient(180deg,#7ec4a8,#6db8a0);}
  .project-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;}
  .project-name{font-size:16px;font-weight:550;color:#2a3f30;}
  .project-status{font-size:11px;padding:3px 10px;border-radius:10px;}
  .project-status.active{background:rgba(107,184,121,0.12);color:#3a8a4a;}
  .project-status.paused{background:rgba(200,180,140,0.12);color:#8a7a4a;}
  .project-status.review{background:rgba(160,180,200,0.12);color:#4a6a8a;}
  .project-meta{display:flex;gap:20px;margin-bottom:12px;}
  .project-meta-item{display:flex;align-items:center;gap:5px;font-size:12px;color:#6a8a6a;}
  .project-progress{display:flex;align-items:center;gap:16px;}
  .progress-track{flex:1;height:6px;background:rgba(160,180,170,0.15);border-radius:4px;overflow:hidden;}
  .progress-fill{height:100%;border-radius:4px;transition:width 0.6s cubic-bezier(0.34,1.56,0.64,1);}
  .progress-fill.green{background:linear-gradient(90deg,#8bc48a,#6db879);}
  .progress-fill.gold{background:linear-gradient(90deg,#c4a97b,#d4b88a);}
  .progress-fill.blue{background:linear-gradient(90deg,#a0b8d0,#8aa8c4);}
  .progress-fill.coral{background:linear-gradient(90deg,#d4a088,#c49078);}
  .progress-fill.teal{background:linear-gradient(90deg,#7ec4a8,#6db8a0);}
  .progress-pct{font-size:13px;font-weight:500;color:#2a3f30;min-width:36px;text-align:right;}
  .project-bottom{display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid rgba(160,180,170,0.1);}
  .project-team{display:flex;}
  .team-mini{width:28px;height:28px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:500;color:white;margin-right:-8px;border:2px solid rgba(255,255,250,0.8);}
  .team-mini:first-child{margin-left:0;}
  .project-deadline{font-size:12px;color:#6a8a6a;display:flex;align-items:center;gap:4px;}
  .grid-view{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;}
  @media (max-width:900px){.grid-view{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="blob-green"></div>
<div class="blob-earth"></div>
<div class="dashboard">
  <div class="content">
    <div class="header">
      <div><h1>Projects</h1><p>5 active initiatives across the org</p></div>
      <div class="header-right"><button class="btn-earth">Grid</button><button class="btn-earth btn-earth-primary">+ New Project</button></div>
    </div>
    <div class="grid-view">
      <div class="project-card p1"><div class="project-top"><span class="project-name">Design System v3</span><span class="project-status active">active</span></div><div class="project-meta"><div class="project-meta-item">~ 6 members</div><div class="project-meta-item">~ 24 tasks</div></div><div class="project-progress"><div class="progress-track"><div class="progress-fill green" style="width:72%"></div></div><span class="progress-pct">72%</span></div><div class="project-bottom"><div class="project-team"><div class="team-mini" style="background:#c49ddb;">AD</div><div class="team-mini" style="background:#e88dcc;">MR</div><div class="team-mini" style="background:#7ed4c8;">LW</div></div><div class="project-deadline">~ Oct 15</div></div></div>
      <div class="project-card p2"><div class="project-top"><span class="project-name">Marketing Site</span><span class="project-status active">active</span></div><div class="project-meta"><div class="project-meta-item">~ 4 members</div><div class="project-meta-item">~ 18 tasks</div></div><div class="project-progress"><div class="progress-track"><div class="progress-fill gold" style="width:45%"></div></div><span class="progress-pct">45%</span></div><div class="project-bottom"><div class="project-team"><div class="team-mini" style="background:#f5c4a0;">TP</div><div class="team-mini" style="background:#c49ddb;">SJ</div></div><div class="project-deadline">~ Nov 1</div></div></div>
      <div class="project-card p3"><div class="project-top"><span class="project-name">API Modernization</span><span class="project-status review">in review</span></div><div class="project-meta"><div class="project-meta-item">~ 3 members</div><div class="project-meta-item">~ 12 tasks</div></div><div class="project-progress"><div class="progress-track"><div class="progress-fill blue" style="width:88%"></div></div><span class="progress-pct">88%</span></div><div class="project-bottom"><div class="project-team"><div class="team-mini" style="background:#7ed4c8;">LW</div><div class="team-mini" style="background:#a8d8d0;">CO</div></div><div class="project-deadline">~ Sep 5</div></div></div>
      <div class="project-card p4"><div class="project-top"><span class="project-name">User Research Q3</span><span class="project-status paused">paused</span></div><div class="project-meta"><div class="project-meta-item">~ 3 members</div><div class="project-meta-item">~ 9 tasks</div></div><div class="project-progress"><div class="progress-track"><div class="progress-fill coral" style="width:30%"></div></div><span class="progress-pct">30%</span></div><div class="project-bottom"><div class="project-team"><div class="team-mini" style="background:#c49ddb;">AD</div><div class="team-mini" style="background:#f5c4a0;">TP</div></div><div class="project-deadline">~ Dec 10</div></div></div>
      <div class="project-card p5"><div class="project-top"><span class="project-name">Mobile App MVP</span><span class="project-status active">active</span></div><div class="project-meta"><div class="project-meta-item">~ 5 members</div><div class="project-meta-item">~ 31 tasks</div></div><div class="project-progress"><div class="progress-track"><div class="progress-fill teal" style="width:56%"></div></div><span class="progress-pct">56%</span></div><div class="project-bottom"><div class="project-team"><div class="team-mini" style="background:#e88dcc;">MR</div><div class="team-mini" style="background:#7ed4c8;">LW</div><div class="team-mini" style="background:#a8d8d0;">CO</div></div><div class="project-deadline">~ Feb 1</div></div></div>
    </div>
  </div>
</div>
</body>
</html>
```
summary:
  agent: organic-fluid-dashboard-designer
  run: 20260626-194440
  mockups: 3
    mockup-1: organic-metrics-dashboard — KPI grid, weekly bar chart, traffic pie, activity feed. Warm coral/peach/amber palette. blob decorations, 4-column KPI cards with gradient hover reveals, soft glassmorphism surfaces.
    mockup-2: organic-team-overview — 6-member team grid with status badges, activity feed sidebar, upcoming events card. Lavender/rose/teal palette. dual-morphing blob backgrounds, avatar hover scale+rotate.
    mockup-3: organic-project-tracker — 5 project cards in grid view with progress bars, team avatars, deadlines. Sage/earth/stone palette. left-accent reveal on hover, progress gradient fills.
  design-language:
    shapes: all corners extreme (12-28px radius), blob morph animations on bg, pill-shaped status badges
    gradients: linear gradients on avatars, progress bars, accent borders, sidebar icons
    glass: backdrop-filter blur on all cards (0.6-0.7 opacity bg), subtle border at 0.4-0.5 opacity
    shadows: none — depth from glass layers and gradient transitions instead
    typography: Inter, 450-650 weight range, tight letter-spacing on headings
    interaction: cubic-bezier(0.34,1.56,0.64,1) — overshoot spring on hover for cards and buttons
  efficiency-notes:
    CSS boilerplate separated per-mockup (no shared file needed — each stands alone)
    each palette defined in mockup-specific CSS variables via class selectors
    animations defined once per mockup, no duplication of keyframe blocks across variants
    max 2 decorative blobs per mockup, minimal DOM nodes (no svg sprites, no icon libraries)
    total 3 files, each under 200 lines, zero external dependencies beyond Google Fonts