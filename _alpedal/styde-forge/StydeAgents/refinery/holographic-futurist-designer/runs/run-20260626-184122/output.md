MOCKUP 2: GLASS ORBITAL
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ORBIT — Glass Interface</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#0b0b1a,#1a0b2e,#0b0b1a);min-height:100vh;display:flex;justify-content:center;align-items:center;font-family:'Segoe UI',system-ui,sans-serif}
.particles{position:fixed;inset:0;z-index:0;overflow:hidden}
.particle{position:absolute;width:3px;height:3px;background:rgba(200,150,255,.6);border-radius:50%;box-shadow:0 0 8px rgba(200,150,255,.4)}
.p1{top:15%;left:20%;animation:drift1 8s infinite}
.p2{top:45%;left:75%;animation:drift2 11s infinite;width:2px;height:2px}
.p3{top:70%;left:30%;animation:drift1 13s infinite;width:4px;height:4px;background:rgba(255,100,200,.5)}
.p4{top:25%;left:85%;animation:drift2 9s infinite}
.p5{top:60%;left:10%;animation:drift1 10s infinite}
.p6{top:80%;left:55%;animation:drift2 12s infinite;width:2px;height:2px;background:rgba(100,200,255,.5)}
.p7{top:10%;left:60%;animation:drift1 7s infinite}
.p8{top:50%;left:45%;animation:drift2 15s infinite;width:5px;height:5px;background:rgba(255,200,100,.3)}
@keyframes drift1{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-20px)}}
@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-40px,25px)}}
.dashboard{position:relative;z-index:1;width:1100px;max-width:94vw;padding:30px;display:grid;grid-template-columns:1fr 1fr;gap:24px}
.card{backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);background:linear-gradient(135deg,rgba(200,150,255,.06),rgba(100,50,180,.03));border:1px solid rgba(200,150,255,.15);border-radius:20px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.05),0 0 60px rgba(200,150,255,.03);transition:all .4s}
.card:hover{border-color:rgba(200,150,255,.3);box-shadow:0 8px 40px rgba(200,150,255,.08),inset 0 1px 0 rgba(255,255,255,.08)}
.card-full{grid-column:1/-1}
.orbital-center{position:relative;width:180px;height:180px;margin:0 auto 16px}
.core{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:50px;height:50px;border-radius:50%;background:radial-gradient(circle,rgba(200,150,255,.8),rgba(100,50,180,.3));box-shadow:0 0 40px rgba(200,150,255,.3),0 0 80px rgba(200,150,255,.1)}
.orbit-ring{position:absolute;top:50%;left:50%;border-radius:50%;border:1px solid rgba(200,150,255,.1);transform:translate(-50%,-50%)}
.orbit-ring.r1{width:120px;height:120px}
.orbit-ring.r2{width:180px;height:180px;border-color:rgba(200,150,255,.06)}
.orbit-dot{position:absolute;top:50%;left:50%;width:8px;height:8px;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 12px currentColor}
.orbit-dot.d1{background:#c96fff;color:#c96fff;animation:orbit1 6s linear infinite;margin-left:60px}
.orbit-dot.d2{background:#ff6fc8;color:#ff6fc8;animation:orbit2 8s linear infinite;margin-left:-90px}
.orbit-dot.d3{background:#6fc8ff;color:#6fc8ff;animation:orbit3 10s linear infinite;margin-top:-60px}
@keyframes orbit1{0%{transform:translate(-50%,-50%)rotate(0deg)translateX(60px)}100%{transform:translate(-50%,-50%)rotate(360deg)translateX(60px)}}
@keyframes orbit2{0%{transform:translate(-50%,-50%)rotate(0deg)translateX(90px)}100%{transform:translate(-50%,-50%)rotate(360deg)translateX(90px)}}
@keyframes orbit3{0%{transform:translate(-50%,-50%)rotate(0deg)translateY(-60px)}100%{transform:translate(-50%,-50%)rotate(360deg)translateY(-60px)}}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.stat-card{text-align:center;padding:16px;background:rgba(200,150,255,.04);border-radius:14px;border:1px solid rgba(200,150,255,.08)}
.stat-value{color:#c96fff;font-size:24px;font-weight:200;text-shadow:0 0 20px rgba(200,150,255,.2)}
.stat-label{color:rgba(255,255,255,.3);font-size:11px;margin-top:6px;letter-spacing:1px}
.stat-glow{color:#6fc8ff;text-shadow:0 0 20px rgba(111,200,255,.3)}
.title-area{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.title-text{color:rgba(255,255,255,.6);font-weight:300;font-size:18px;letter-spacing:3px}
.title-sub{color:rgba(255,255,255,.25);font-size:11px;letter-spacing:2px}
.activity-list{display:flex;flex-direction:column;gap:8px}
.activity-item{display:flex;align-items:center;gap:12px;padding:10px 14px;background:rgba(200,150,255,.03);border-radius:10px;border:1px solid rgba(200,150,255,.06)}
.activity-icon{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px}
.activity-icon.purple{background:rgba(200,150,255,.15);color:#c96fff}
.activity-icon.blue{background:rgba(111,200,255,.15);color:#6fc8ff}
.activity-icon.pink{background:rgba(255,111,200,.15);color:#ff6fc8}
.activity-text{flex:1;color:rgba(255,255,255,.5);font-size:13px}
.activity-meta{color:rgba(255,255,255,.2);font-size:10px}
.glow-top{position:fixed;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(200,150,255,.4),transparent);z-index:3}
</style>
</head>
<body>
<div class="glow-top"></div>
<div class="particles">
  <div class="particle p1"></div><div class="particle p2"></div><div class="particle p3"></div>
  <div class="particle p4"></div><div class="particle p5"></div><div class="particle p6"></div>
  <div class="particle p7"></div><div class="particle p8"></div>
</div>
<div class="dashboard">
  <div class="card card-full">
    <div class="title-area">
      <div>
        <div class="title-text">ORBITAL MONITOR</div>
        <div class="title-sub">HOLOGRAPHIC INTERFACE v2.4</div>
      </div>
      <div style="display:flex;gap:12px">
        <span style="color:rgba(200,150,255,.6);font-size:12px;letter-spacing:1px">ALL SYSTEMS</span>
        <span style="color:#6fc8ff;font-size:12px">◉ ONLINE</span>
      </div>
    </div>
  </div>
  <div class="card" style="display:flex;flex-direction:column;align-items:center">
    <div style="color:rgba(255,255,255,.3);font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;align-self:flex-start">NETWORK TOPOLOGY</div>
    <div class="orbital-center">
      <div class="core"></div>
      <div class="orbit-ring r1"></div>
      <div class="orbit-ring r2"></div>
      <div class="orbit-dot d1"></div>
      <div class="orbit-dot d2"></div>
      <div class="orbit-dot d3"></div>
    </div>
    <div style="display:flex;gap:20px;margin-top:8px">
      <div style="display:flex;align-items:center;gap:6px"><div style="width:8px;height:8px;border-radius:50%;background:#c96fff"></div><span style="color:rgba(255,255,255,.3);font-size:10px">Primary</span></div>
      <div style="display:flex;align-items:center;gap:6px"><div style="width:8px;height:8px;border-radius:50%;background:#6fc8ff"></div><span style="color:rgba(255,255,255,.3);font-size:10px">Secondary</span></div>
      <div style="display:flex;align-items:center;gap:6px"><div style="width:8px;height:8px;border-radius:50%;background:#ff6fc8"></div><span style="color:rgba(255,255,255,.3);font-size:10px">Relay</span></div>
    </div>
  </div>
  <div class="card">
    <div style="color:rgba(255,255,255,.3);font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">KEY METRICS</div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-value">98.7%</div><div class="stat-label">Uptime</div></div>
      <div class="stat-card"><div class="stat-value stat-glow">24ms</div><div class="stat-label">Avg Latency</div></div>
      <div class="stat-card"><div class="stat-value">1.4M</div><div class="stat-label">Requests</div></div>
      <div class="stat-card"><div class="stat-value">847</div><div class="stat-label">Active Nodes</div></div>
      <div class="stat-card"><div class="stat-value stat-glow">3.2s</div><div class="stat-label">Response</div></div>
      <div class="stat-card"><div class="stat-value">12</div><div class="stat-label">Alerts</div></div>
    </div>
  </div>
  <div class="card card-full">
    <div style="color:rgba(255,255,255,.3);font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px">RECENT ACTIVITY</div>
    <div class="activity-list">
      <div class="activity-item">
        <div class="activity-icon purple">⇡</div>
        <span class="activity-text">Node cluster 4 scaled up — 12 new instances deployed</span>
        <span class="activity-meta">2m ago</span>
      </div>
      <div class="activity-item">
        <div class="activity-icon blue">◉</div>
        <span class="activity-text">Singapore region health check passed — 0ms packet loss</span>
        <span class="activity-meta">7m ago</span>
      </div>
      <div class="activity-item">
        <div class="activity-icon pink">⚡</div>
        <span class="activity-text">Traffic spike absorbed — auto-scaled to 24 workers</span>
        <span class="activity-meta">14m ago</span>
      </div>
      <div class="activity-item">
        <div class="activity-icon purple">⇣</div>
        <span class="activity-text">Deployment v3.8.2 rolled back — audit triggered</span>
        <span class="activity-meta">23m ago</span>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```
DESIGN TERRITORY: Glass orbital interface — frosted glass cards with blur backdrop, circular orbital topology visualization with animated orbiting dots, drifting particle field. Purple/magenta/cyan palette. Card-based layout with rounded corners. Entirely different feel from NEON GRID — organic, floating, celestial. Uses backdrop-filter for glassmorphism. No grid lines, no sharp angles, no bar charts.
MOCKUP 3: CHROMA WAVE
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>CHROMA — Wave Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050510;min-height:100vh;display:flex;justify-content:center;align-items:center;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
.wave-bg{position:fixed;inset:0;z-index:0;overflow:hidden}
.wave{position:absolute;bottom:0;width:200%;height:180px;background:repeating-linear-gradient(90deg,transparent,transparent 40px,rgba(255,60,120,.03)40px,rgba(255,60,120,.03)41px);transform-origin:bottom center}
.wave::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 100%,rgba(255,60,120,.08),transparent 60%)}
.wave-1{animation:wave1 8s ease-in-out infinite alternate;height:200px}
.wave-2{animation:wave2 11s ease-in-out infinite alternate;height:140px;opacity:.5}
.wave-3{animation:wave3 14s ease-in-out infinite alternate;height:100px;opacity:.3}
@keyframes wave1{0%{transform:translateX(0)scaleY(1)}100%{transform:translateX(-30%)scaleY(1.4)}}
@keyframes wave2{0%{transform:translateX(-20%)scaleY(1)}100%{transform:translateX(0)scaleY(1.6)}}
@keyframes wave3{0%{transform:translateX(-10%)scaleY(1.1)}100%{transform:translateX(-40%)scaleY(1.8)}}
.dashboard{position:relative;z-index:1;width:1100px;max-width:94vw;padding:30px;display:grid;grid-template-columns:1fr 1fr 1fr;grid-template-rows:auto auto;gap:16px}
.badge{position:fixed;top:16px;right:24px;z-index:10;display:flex;align-items:center;gap:8px;padding:6px 14px;background:rgba(255,60,120,.1);border:1px solid rgba(255,60,120,.2);border-radius:20px;color:rgba(255,60,120,.7);font-size:11px;letter-spacing:1px}
.badge-dot{width:5px;height:5px;border-radius:50%;background:#ff3c78;animation:pulse2 1.5s infinite}
@keyframes pulse2{0%,100%{opacity:1;box-shadow:0 0 6px #ff3c78}50%{opacity:.3;box-shadow:0 0 2px #ff3c78}}
.panel{border-radius:16px;padding:20px;position:relative;overflow:hidden}
.panel::before{content:'';position:absolute;inset:0;border-radius:16px;padding:1px;background:linear-gradient(135deg,rgba(255,60,120,.15),rgba(255,200,60,.05));-webkit-mask:linear-gradient(#fff 0 0)content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.panel-content{position:relative;z-index:1}
.panel-dark{background:rgba(10,10,20,.7)}
.hero{grid-column:1/-1;padding:28px;display:flex;justify-content:space-between;align-items:flex-end}
.hero-left{display:flex;flex-direction:column;gap:4px}
.hero-title{color:#fff;font-size:28px;font-weight:200;letter-spacing:6px}
.hero-title span{color:#ff3c78;text-shadow:0 0 30px rgba(255,60,120,.3)}
.hero-sub{color:rgba(255,255,255,.3);font-size:12px;letter-spacing:3px}
.hero-right{text-align:right}
.hero-big{color:#ff3c78;font-size:36px;font-weight:100;text-shadow:0 0 40px rgba(255,60,120,.2)}
.hero-label{color:rgba(255,255,255,.25);font-size:11px;letter-spacing:2px}
.panel-label{color:rgba(255,255,255,.25);font-size:9px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px}
.gauge{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
.gauge-track{height:4px;background:rgba(255,255,255,.06);border-radius:2px;overflow:hidden}
.gauge-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#ff3c78,#ffc83c);transition:width 1s}
.gauge-row{display:flex;justify-content:space-between}
.gauge-label{color:rgba(255,255,255,.4);font-size:11px}
.gauge-value{color:rgba(255,255,255,.6);font-size:11px}
.metric-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.04)}
.metric-row:last-child{border-bottom:none}
.metric-row .label{color:rgba(255,255,255,.3);font-size:12px}
.metric-row .value{color:#ff3c78;font-size:14px;font-weight:300}
.metric-row .value.amber{color:#ffc83c}
.donut-wrap{display:flex;justify-content:center;align-items:center;padding:10px 0}
.donut{width:100px;height:100px;border-radius:50%;background:conic-gradient(#ff3c78 0% 72%,#ffc83c 72% 89%,rgba(255,255,255,.05)89% 100%);position:relative;display:flex;align-items:center;justify-content:center}
.donut-hole{width:60px;height:60px;border-radius:50%;background:#050510;display:flex;flex-direction:column;align-items:center;justify-content:center}
.donut-number{color:#fff;font-size:18px;font-weight:200}
.donut-sub{color:rgba(255,255,255,.3);font-size:8px}
.status-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.status-item{display:flex;align-items:center;gap:8px;padding:8px;background:rgba(255,255,255,.02);border-radius:8px}
.status-dot2{width:6px;height:6px;border-radius:50%}
.status-dot2.green{background:#0f6;box-shadow:0 0 8px #0f6}
.status-dot2.red{background:#f34;box-shadow:0 0 8px #f34}
.status-dot2.amber{background:#fc3;box-shadow:0 0 8px #fc3}
.status-name{color:rgba(255,255,255,.4);font-size:11px;flex:1}
.status-val{color:rgba(255,255,255,.3);font-size:10px}
</style>
</head>
<body>
<div class="badge">
  <div class="badge-dot"></div>
  <span>CHROMA · LIVE</span>
</div>
<div class="wave-bg">
  <div class="wave wave-1"></div>
  <div class="wave wave-2"></div>
  <div class="wave wave-3"></div>
</div>
<div class="dashboard">
  <div class="panel panel-dark hero">
    <div class="panel-content" style="display:flex;justify-content:space-between;width:100%;align-items:flex-end">
      <div class="hero-left">
        <div class="hero-title"><span>⋎</span> CHROMA</div>
        <div class="hero-sub">PERFORMANCE DASHBOARD</div>
      </div>
      <div class="hero-right">
        <div class="hero-big">94.2%</div>
        <div class="hero-label">OVERALL HEALTH</div>
      </div>
    </div>
  </div>
  <div class="panel panel-dark">
    <div class="panel-content">
      <div class="panel-label">SYSTEM LOAD</div>
      <div class="gauge">
        <div class="gauge-row"><span class="gauge-label">CPU</span><span class="gauge-value">47%</span></div>
        <div class="gauge-track"><div class="gauge-fill" style="width:47%"></div></div>
      </div>
      <div class="gauge">
        <div class="gauge-row"><span class="gauge-label">Memory</span><span class="gauge-value">62%</span></div>
        <div class="gauge-track"><div class="gauge-fill" style="width:62%"></div></div>
      </div>
      <div class="gauge">
        <div class="gauge-row"><span class="gauge-label">Disk</span><span class="gauge-value">38%</span></div>
        <div class="gauge-track"><div class="gauge-fill" style="width:38%"></div></div>
      </div>
      <div class="gauge">
        <div class="gauge-row"><span class="gauge-label">Network</span><span class="gauge-value">71%</span></div>
        <div class="gauge-track"><div class="gauge-fill" style="width:71%"></div></div>
      </div>
    </div>
  </div>
  <div class="panel panel-dark">
    <div class="panel-content">
      <div class="panel-label">DISTRIBUTION</div>
      <div class="donut-wrap">
        <div class="donut">
          <div class="donut-hole">
            <div class="donut-number">72%</div>
            <div class="donut-sub">active</div>
          </div>
        </div>
      </div>
      <div style="display:flex;justify-content:center;gap:16px;margin-top:4px">
        <div style="display:flex;align-items:center;gap:4px"><div style="width:8px;height:8px;border-radius:50%;background:#ff3c78"></div><span style="color:rgba(255,255,255,.3);font-size:10px">Web (72%)</span></div>
        <div style="display:flex;align-items:center;gap:4px"><div style="width:8px;height:8px;border-radius:50%;background:#ffc83c"></div><span style="color:rgba(255,255,255,.3);font-size:10px">API (17%)</span></div>
        <div style="display:flex;align-items:center;gap:4px"><div style="width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.1)"></div><span style="color:rgba(255,255,255,.3);font-size:10px">Other (11%)</span></div>
      </div>
    </div>
  </div>
  <div class="panel panel-dark">
    <div class="panel-content">
      <div class="panel-label">KEY METRICS</div>
      <div class="metric-row"><span class="label">Requests/min</span><span class="value">12,847</span></div>
      <div class="metric-row"><span class="label">Avg Response</span><span class="value amber">43ms</span></div>
      <div class="metric-row"><span class="label">Error Rate</span><span class="value" style="color:#0f6">0.12%</span></div>
      <div class="metric-row"><span class="label">Active Sessions</span><span class="value">3,204</span></div>
      <div class="metric-row"><span class="label">Queue Depth</span><span class="value amber">142</span></div>
    </div>
  </div>
  <div class="panel panel-dark">
    <div class="panel-content">
      <div class="panel-label">SERVICE STATUS</div>
      <div class="status-grid">
        <div class="status-item"><div class="status-dot2 green"></div><span class="status-name">Web Server</span><span class="status-val">100%</span></div>
        <div class="status-item"><div class="status-dot2 green"></div><span class="status-name">Database</span><span class="status-val">98%</span></div>
        <div class="status-item"><div class="status-dot2 amber"></div><span class="status-name">Cache Layer</span><span class="status-val">87%</span></div>
        <div class="status-item"><div class="status-dot2 green"></div><span class="status-name">Queue</span><span class="status-val">100%</span></div>
        <div class="status-item"><div class="status-dot2 red"></div><span class="status-name">CDN Edge</span><span class="status-val">62%</span></div>
        <div class="status-item"><div class="status-dot2 green"></div><span class="status-name">Auth</span><span class="status-val">100%</span></div>
      </div>
    </div>
  </div>
  <div class="panel panel-dark">
    <div class="panel-content">
      <div class="panel-label">RECENT DEPLOYS</div>
      <div class="metric-row"><span class="label">v3.9.1</span><span class="value" style="color:#0f6;font-size:11px">passed</span></div>
      <div class="metric-row"><span class="label">v3.9.0</span><span class="value" style="color:#0f6;font-size:11px">passed</span></div>
      <div class="metric-row"><span class="label">v3.8.4</span><span class="value" style="color:#fc3;font-size:11px">rolled back</span></div>
      <div class="metric-row"><span class="label">v3.8.3</span><span class="value" style="color:#0f6;font-size:11px">passed</span></div>
      <div class="metric-row"><span class="label">v3.8.2</span><span class="value" style="color:#f34;font-size:11px">failed</span></div>
    </div>
  </div>
</div>
</body>
</html>
```
DESIGN TERRITORY: Audio-visual wave dashboard — animated undulating wave backgrounds at bottom, conic donut chart, horizontal gauges, gradient from hot pink to amber. Dark minimal foreground over animated waveform background. Completely different from both NEON GRID (structured grid) and GLASS ORBITAL (frosted glass). Pink/amber/red color story. Warm vs the cool cyan and purple of the other two. Feels like a music production or audio monitoring interface.
SUMMARY TABLE
theme | layout | visual technique | color story | primary data viz | feeling
NEON GRID | 3-column grid sidebar+chart+panels | cyan neon scanlines + glow borders | cyan / black | bar chart | network ops center — precise, cold
GLASS ORBITAL | 2-column card grid | glassmorphism blur + particles + orbit animation | purple / magenta / cyan | orbital topology diagram | celestial control room — floating, organic
CHROMA WAVE | 3-column panel grid | animated fluid waveforms + gradient borders | hot pink / amber / black | conic donut + gauges | audio monitoring station — warm, energetic
SELF-CHECK:
html tags opened — html(1), head(1), meta(3), title(1), style(1), body(1), div(30+), span(15+)
html tags closed — every tag above verified closed
no mid-tag truncation — all style blocks end with </style>, all HTML closes with </html>
no unclosed open-tag angle brackets found
3 mockups, 3 distinct territories, no variants of same concept
each mockup separated by labeled divider with commentary
summary table present