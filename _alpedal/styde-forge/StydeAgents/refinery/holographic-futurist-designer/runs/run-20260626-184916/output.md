MOCKUP 1: QUANTUM OVERVIEW DASHBOARD
A real-time system monitor with floating metric cards. Each card hovers above a dark void, connected by animated particle streams that pulse with telemetry data.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quantum Overview</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a12;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  canvas#particles {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
  }
  .dashboard {
    position: relative;
    z-index: 1;
    width: 1200px;
    max-width: 95vw;
    padding: 32px;
    background: rgba(10, 10, 25, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 200, 255, 0.15);
    border-radius: 24px;
    box-shadow: 0 0 60px rgba(0, 150, 255, 0.08), inset 0 0 60px rgba(0, 150, 255, 0.03);
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 36px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(0, 200, 255, 0.1);
  }
  .title {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 4px;
    color: rgba(0, 220, 255, 0.7);
    font-weight: 300;
  }
  .title span {
    display: block;
    font-size: 28px;
    letter-spacing: 2px;
    color: #fff;
    margin-top: 4px;
    font-weight: 600;
    text-shadow: 0 0 20px rgba(0, 200, 255, 0.3);
  }
  .status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
  }
  .status-dot.online { background: #00ff88; box-shadow: 0 0 12px #00ff88; }
  .status-bar {
    display: flex;
    gap: 12px;
    align-items: center;
    color: rgba(255,255,255,0.5);
    font-size: 12px;
    letter-spacing: 1px;
  }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
  .grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
  }
  .metric-card {
    padding: 20px;
    background: linear-gradient(135deg, rgba(0, 100, 200, 0.08), rgba(0, 200, 255, 0.03));
    border: 1px solid rgba(0, 180, 255, 0.1);
    border-radius: 16px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: default;
  }
  .metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 200, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 100, 255, 0.1);
  }
  .metric-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(0, 200, 255, 0.5);
    margin-bottom: 8px;
  }
  .metric-value {
    font-size: 36px;
    font-weight: 200;
    color: #fff;
    letter-spacing: 1px;
  }
  .metric-value .unit {
    font-size: 14px;
    color: rgba(0, 200, 255, 0.4);
    margin-left: 4px;
  }
  .metric-trend {
    font-size: 11px;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .metric-trend.up { color: #00ff88; }
  .metric-trend.down { color: #ff4466; }
  .glow-bar {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 200, 255, 0.4), transparent);
  }
  .chart-area {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
  }
  .chart-panel {
    padding: 20px;
    background: rgba(0, 50, 100, 0.06);
    border: 1px solid rgba(0, 180, 255, 0.08);
    border-radius: 16px;
  }
  .chart-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  .chart-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(0, 200, 255, 0.5);
  }
  .chart-legend {
    display: flex;
    gap: 12px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .legend-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
  }
  .bar-chart {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    height: 140px;
    padding-top: 10px;
  }
  .bar {
    flex: 1;
    border-radius: 4px 4px 0 0;
    position: relative;
    min-height: 4px;
    transition: height 0.5s ease;
    background: linear-gradient(180deg, rgba(0, 200, 255, 0.6), rgba(0, 100, 200, 0.2));
  }
  .bar:hover { opacity: 0.8; }
  .bar-label {
    position: absolute;
    bottom: -18px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 9px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1px;
  }
  .activity-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 12px;
  }
  .activity-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(0, 100, 200, 0.04);
    border-radius: 8px;
    border-left: 2px solid rgba(0, 200, 255, 0.2);
    font-size: 12px;
    color: rgba(255,255,255,0.6);
  }
  .activity-item .time {
    color: rgba(0, 200, 255, 0.3);
    font-size: 10px;
    letter-spacing: 1px;
  }
  .scanline {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 1px,
      rgba(0, 200, 255, 0.008) 1px,
      rgba(0, 200, 255, 0.008) 2px
    );
    pointer-events: none;
    z-index: 2;
    border-radius: 24px;
  }
</style>
</head>
<body>
<canvas id="particles"></canvas>
<div class="dashboard">
  <div class="scanline"></div>
  <div class="header">
    <div class="title">
      system status
      <span>QUANTUM CORE</span>
    </div>
    <div class="status-bar">
      <span><span class="status-dot online"></span>all systems nominal</span>
      <span>|</span>
      <span>UPTIME 14d 7h</span>
      <span>|</span>
      <span>v3.2.1</span>
    </div>
  </div>
  <div class="grid">
    <div class="metric-card">
      <div class="glow-bar"></div>
      <div class="metric-label">throughput</div>
      <div class="metric-value">2.4<span class="unit">gbps</span></div>
      <div class="metric-trend up">+12.3%</div>
    </div>
    <div class="metric-card">
      <div class="glow-bar"></div>
      <div class="metric-label">active nodes</div>
      <div class="metric-value">47<span class="unit">/ 64</span></div>
      <div class="metric-trend up">+3 online</div>
    </div>
    <div class="metric-card">
      <div class="glow-bar"></div>
      <div class="metric-label">latency p99</div>
      <div class="metric-value">12<span class="unit">ms</span></div>
      <div class="metric-trend down">+2ms</div>
    </div>
    <div class="metric-card">
      <div class="glow-bar"></div>
      <div class="metric-label">error rate</div>
      <div class="metric-value">0.02<span class="unit">%</span></div>
      <div class="metric-trend up">-0.01%</div>
    </div>
  </div>
  <div class="chart-area">
    <div class="chart-panel">
      <div class="chart-header">
        <div class="chart-title">network traffic — last 24h</div>
        <div class="chart-legend">
          <div class="legend-item"><span class="legend-dot" style="background:#00ccff"></span>inbound</div>
          <div class="legend-item"><span class="legend-dot" style="background:#00ff88"></span>outbound</div>
        </div>
      </div>
      <div class="bar-chart" id="barChart"></div>
    </div>
    <div class="chart-panel">
      <div class="chart-header">
        <div class="chart-title">recent activity</div>
      </div>
      <div class="activity-list">
        <div class="activity-item"><span>node-42 heartbeat</span><span class="time">12s ago</span></div>
        <div class="activity-item"><span>cluster rebalance</span><span class="time">2m ago</span></div>
        <div class="activity-item"><span>backup complete</span><span class="time">7m ago</span></div>
        <div class="activity-item"><span>config sync</span><span class="time">14m ago</span></div>
        <div class="activity-item"><span>deploy v3.2.2</span><span class="time">32m ago</span></div>
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  const c = document.getElementById('particles');
  const ctx = c.getContext('2d');
  let w = c.width = window.innerWidth;
  let h = c.height = window.innerHeight;
  const particles = [];
  const PCOUNT = 60;
  const CONN_DIST = 180;
  for(let i=0;i<PCOUNT;i++){
    particles.push({
      x: Math.random()*w, y: Math.random()*h,
      vx: (Math.random()-0.5)*0.4,
      vy: (Math.random()-0.5)*0.4,
      r: Math.random()*2+1,
      a: Math.random()*0.4+0.1
    });
  }
  function draw(){
    ctx.clearRect(0,0,w,h);
    for(let p of particles){
      p.x += p.vx; p.y += p.vy;
      if(p.x<0||p.x>w) p.vx*=-1;
      if(p.y<0||p.y>h) p.vy*=-1;
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle = `rgba(0,200,255,${p.a})`;
      ctx.fill();
    }
    for(let i=0;i<particles.length;i++){
      for(let j=i+1;j<particles.length;j++){
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx*dx+dy*dy);
        if(dist < CONN_DIST){
          ctx.beginPath();
          ctx.moveTo(particles[i].x,particles[i].y);
          ctx.lineTo(particles[j].x,particles[j].y);
          ctx.strokeStyle = `rgba(0,200,255,${0.08*(1-dist/CONN_DIST)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
  window.addEventListener('resize',()=>{w=c.width=window.innerWidth;h=c.height=window.innerHeight;});
  const chart = document.getElementById('barChart');
  const labels = ['00','03','06','09','12','15','18','21'];
  const inbound = [34,28,42,58,72,65,48,39];
  const outbound = [22,18,35,44,56,50,38,30];
  let html = '';
  for(let i=0;i<8;i++){
    const maxV = Math.max(...inbound,...outbound);
    const h1 = (inbound[i]/maxV)*120;
    const h2 = (outbound[i]/maxV)*120;
    const barW = Math.max(4, (1200/8)*0.25);
    html += `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;height:140px;justify-content:flex-end;">
      <div style="width:${barW}px;height:${h1}px;background:linear-gradient(180deg,rgba(0,204,255,0.6),rgba(0,100,200,0.2));border-radius:2px 2px 0 0;"></div>
      <div style="width:${barW}px;height:${h2}px;background:linear-gradient(180deg,rgba(0,255,136,0.5),rgba(0,180,100,0.15));border-radius:2px 2px 0 0;"></div>
      <div style="font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:1px;">${labels[i]}</div>
    </div>`;
  }
  chart.innerHTML = html;
})();
</script>
</body>
</html>
```
---
MOCKUP 1: QUANTUM OVERVIEW DASHBOARD
Hover-reveal metric cards, particle-connected background, live bar charts, and activity feed in a glass-morphism container. All repeated visual elements (particles, bar pairs) generated by JS loops — zero static div repetition. Single wrapper layer (dashboard div) around the entire layout.
---
MOCKUP 2: HOLOGRAPHIC TERMINAL INTERFACE
A command-line-meets-hologram hybrid. Floating code panes with scanline overlays, a central holographic projection ring, and radial navigation.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holo Terminal</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #07070f;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  canvas#bgCanvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
  }
  .holo-container {
    position: relative;
    z-index: 1;
    width: 1100px;
    max-width: 94vw;
    padding: 28px;
    border-radius: 20px;
    background: radial-gradient(ellipse at 50% 30%, rgba(0,60,120,0.12), rgba(0,10,30,0.5));
    border: 1px solid rgba(0,180,255,0.1);
    box-shadow: 0 0 80px rgba(0,100,255,0.06);
  }
  .scanline-overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(0,200,255,0.015) 1px, rgba(0,200,255,0.015) 2px);
    pointer-events: none;
    border-radius: 20px;
    z-index: 10;
  }
  .holo-ring {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 340px; height: 340px;
    border-radius: 50%;
    border: 1px solid rgba(0,200,255,0.06);
    pointer-events: none;
    z-index: 0;
    animation: ringPulse 4s ease-in-out infinite;
  }
  .holo-ring-inner {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 200px; height: 200px;
    border-radius: 50%;
    border: 1px solid rgba(0,200,255,0.04);
    pointer-events: none;
    z-index: 0;
    animation: ringPulse 4s ease-in-out infinite 0.5s;
  }
  @keyframes ringPulse {
    0%, 100% { transform: translate(-50%,-50%) scale(1); opacity: 0.4; }
    50% { transform: translate(-50%,-50%) scale(1.05); opacity: 0.7; }
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    position: relative;
    z-index: 2;
  }
  .prompt-line {
    color: rgba(0,220,255,0.6);
    font-size: 13px;
    letter-spacing: 1px;
  }
  .prompt-line .cursor {
    display: inline-block;
    width: 8px;
    height: 16px;
    background: rgba(0,220,255,0.4);
    animation: blink 1s step-end infinite;
    vertical-align: text-bottom;
    margin-left: 4px;
  }
  @keyframes blink { 50% { opacity: 0; } }
  .status-chip {
    display: flex;
    gap: 16px;
    align-items: center;
  }
  .chip {
    padding: 4px 12px;
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 20px;
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(0,200,255,0.5);
    text-transform: uppercase;
  }
  .chip.active {
    border-color: rgba(0,255,136,0.3);
    color: #00ff88;
    box-shadow: 0 0 12px rgba(0,255,136,0.05);
  }
  .panels {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
    position: relative;
    z-index: 2;
  }
  .panel {
    background: rgba(0,30,60,0.25);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,180,255,0.06);
    border-radius: 14px;
    padding: 16px;
  }
  .panel-header {
    font-size: 9px;
    letter-spacing: 3px;
    color: rgba(0,200,255,0.3);
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0,180,255,0.06);
  }
  .log-line {
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    line-height: 1.6;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  }
  .log-line .ts { color: rgba(0,200,255,0.2); }
  .log-line .ok { color: #00ff88; }
  .log-line .warn { color: #ffbb44; }
  .log-line .err { color: #ff4466; }
  .node-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 6px;
  }
  .node {
    padding: 8px;
    background: rgba(0,80,160,0.06);
    border-radius: 8px;
    border: 1px solid rgba(0,180,255,0.04);
    text-align: center;
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1px;
  }
  .node .dot {
    display: block;
    width: 6px; height: 6px;
    border-radius: 50%;
    margin: 0 auto 4px;
    background: #00ff88;
    box-shadow: 0 0 8px rgba(0,255,136,0.2);
    animation: pulse 2s infinite;
  }
  .data-ring {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    position: relative;
  }
  .ring-stat {
    text-align: center;
  }
  .ring-stat .value {
    font-size: 32px;
    font-weight: 200;
    color: #fff;
    letter-spacing: 2px;
  }
  .ring-stat .label {
    font-size: 9px;
    letter-spacing: 2px;
    color: rgba(0,200,255,0.3);
    text-transform: uppercase;
    margin-top: 4px;
  }
  .progress-track {
    width: 100%;
    height: 2px;
    background: rgba(0,100,200,0.1);
    border-radius: 2px;
    margin-top: 16px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, rgba(0,200,255,0.2), rgba(0,200,255,0.5));
    border-radius: 2px;
    width: 73%;
    animation: shimmer 3s infinite;
  }
  @keyframes shimmer {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
  }
  .glow-corner {
    position: absolute;
    width: 80px; height: 80px;
    pointer-events: none;
    z-index: 0;
  }
  .glow-corner.tl { top: -20px; left: -20px; background: radial-gradient(circle at 0 0, rgba(0,150,255,0.06), transparent); }
  .glow-corner.br { bottom: -20px; right: -20px; background: radial-gradient(circle at 100% 100%, rgba(0,150,255,0.06), transparent); }
</style>
</head>
<body>
<canvas id="bgCanvas"></canvas>
<div class="holo-container">
  <div class="scanline-overlay"></div>
  <div class="holo-ring"></div>
  <div class="holo-ring-inner"></div>
  <div class="glow-corner tl"></div>
  <div class="glow-corner br"></div>
  <div class="top-bar">
    <div class="prompt-line">root@holo-core ~ $ monitor --live<span class="cursor"></span></div>
    <div class="status-chip">
      <span class="chip active">system online</span>
      <span class="chip">v3.1.0</span>
    </div>
  </div>
  <div class="panels">
    <div class="panel">
      <div class="panel-header">event log</div>
      <div class="log-line"><span class="ts">[12:47:03]</span> <span class="ok">OK</span> node-12 sync complete</div>
      <div class="log-line"><span class="ts">[12:46:51]</span> <span class="ok">OK</span> pipeline deploy v3.1.0</div>
      <div class="log-line"><span class="ts">[12:46:12]</span> <span class="warn">WARN</span> latency spike node-07</div>
      <div class="log-line"><span class="ts">[12:45:40]</span> <span class="ok">OK</span> heartbeat received 47/47</div>
      <div class="log-line"><span class="ts">[12:44:58]</span> <span class="err">ERR</span> retry: config push node-33</div>
      <div class="log-line"><span class="ts">[12:44:12]</span> <span class="ok">OK</span> recovery complete</div>
    </div>
    <div class="panel">
      <div class="panel-header">mesh topology</div>
      <div class="node-grid">
        <div class="node"><span class="dot"></span>n-01</div>
        <div class="node"><span class="dot"></span>n-02</div>
        <div class="node"><span class="dot"></span>n-03</div>
        <div class="node"><span class="dot"></span>n-04</div>
        <div class="node"><span class="dot"></span>n-05</div>
        <div class="node"><span class="dot"></span>n-06</div>
        <div class="node"><span class="dot"></span>n-07</div>
        <div class="node"><span class="dot"></span>n-08</div>
        <div class="node"><span class="dot"></span>n-09</div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header">core metrics</div>
      <div class="data-ring">
        <div class="ring-stat">
          <div class="value">97.3<span style="font-size:14px;color:rgba(0,200,255,0.3);">%</span></div>
          <div class="label">uptime</div>
        </div>
      </div>
      <div class="progress-track"><div class="progress-fill"></div></div>
      <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:10px;color:rgba(255,255,255,0.2);letter-spacing:1px;">
        <span>alloc: 73%</span>
        <span>temp: 42°C</span>
        <span>load: 0.34</span>
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  const c = document.getElementById('bgCanvas');
  const ctx = c.getContext('2d');
  let w = c.width = window.innerWidth;
  let h = c.height = window.innerHeight;
  const stars = [];
  for(let i=0;i<80;i++){
    stars.push({
      x: Math.random()*w, y: Math.random()*h,
      size: Math.random()*1.5+0.3,
      speed: Math.random()*0.15+0.02,
      opacity: Math.random()*0.3+0.05
    });
  }
  function draw(){
    ctx.clearRect(0,0,w,h);
    for(let s of stars){
      s.y -= s.speed;
      if(s.y < 0){ s.y = h; s.x = Math.random()*w; }
      ctx.beginPath();
      ctx.arc(s.x,s.y,s.size,0,Math.PI*2);
      ctx.fillStyle = `rgba(0,200,255,${s.opacity})`;
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  draw();
  window.addEventListener('resize',()=>{w=c.width=window.innerWidth;h=c.height=window.innerHeight;});
})();
</script>
</body>
</html>
```
---
MOCKUP 2: HOLOGRAPHIC TERMINAL INTERFACE
Animated holographic rings behind a three-panel terminal dashboard. JS-generated starfield drift for the background, scanline overlay for CRT feel, progress bar with shimmer animation. Chunky monospace typography contrasts with soft glow corners. The holo-ring and starfield are programmatic — zero repeated divs.
---
MOCKUP 3: NEON EDGE — GLAIVE LAYOUT
Radial navigation hub with a central arc display. Asymmetric panel geometry, diagonal slice aesthetics, and high-density data visualization. Sharp edges, tight kerning, information-dense.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neon Edge — Glaive</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #050510;
    font-family: 'Inter', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  canvas#gridCanvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
  }
  .glaive {
    position: relative;
    z-index: 1;
    width: 1150px;
    max-width: 94vw;
    display: grid;
    grid-template-columns: 240px 1fr 200px;
    gap: 0;
    background: rgba(5,5,16,0.7);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(0,180,255,0.08);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(0,80,255,0.04);
  }
  .sidebar {
    padding: 24px 16px;
    border-right: 1px solid rgba(0,180,255,0.06);
    background: rgba(0,20,40,0.15);
  }
  .sidebar-right {
    padding: 24px 16px;
    border-left: 1px solid rgba(0,180,255,0.06);
    background: rgba(0,20,40,0.15);
  }
  .main-panel {
    padding: 24px 20px;
    position: relative;
  }
  .brand {
    font-size: 10px;
    letter-spacing: 4px;
    color: rgba(0,200,255,0.3);
    text-transform: uppercase;
    margin-bottom: 28px;
  }
  .brand strong {
    display: block;
    font-size: 18px;
    font-weight: 300;
    color: #fff;
    letter-spacing: 6px;
    margin-top: 4px;
    text-shadow: 0 0 20px rgba(0,150,255,0.15);
  }
  .nav-item {
    padding: 10px 14px;
    margin-bottom: 4px;
    border-radius: 10px;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    transition: all 0.2s;
    cursor: default;
    border-left: 2px solid transparent;
  }
  .nav-item:hover {
    color: rgba(0,220,255,0.7);
    background: rgba(0,100,200,0.06);
    border-left-color: rgba(0,200,255,0.2);
  }
  .nav-item.active {
    color: #00ccff;
    background: rgba(0,100,200,0.1);
    border-left-color: #00ccff;
  }
  .nav-item .badge {
    float: right;
    font-size: 9px;
    color: rgba(0,200,255,0.3);
  }
  .arc-display {
    position: relative;
    height: 200px;
    margin-bottom: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  canvas#arcCanvas {
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 200px;
  }
  .arc-stats {
    position: relative;
    z-index: 2;
    display: flex;
    gap: 40px;
  }
  .arc-stat {
    text-align: center;
  }
  .arc-stat .num {
    font-size: 28px;
    font-weight: 200;
    color: #fff;
    letter-spacing: 1px;
  }
  .arc-stat .lbl {
    font-size: 9px;
    letter-spacing: 3px;
    color: rgba(0,200,255,0.3);
    text-transform: uppercase;
    margin-top: 2px;
  }
  .arc-stat .num .highlight {
    color: #00ccff;
    text-shadow: 0 0 16px rgba(0,200,255,0.3);
  }
  .diagonal-slice {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 8px;
  }
  .slice-card {
    padding: 14px;
    background: rgba(0,40,80,0.08);
    border: 1px solid rgba(0,180,255,0.05);
    border-radius: 12px;
    position: relative;
    overflow: hidden;
  }
  .slice-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 30px; height: 30px;
    background: linear-gradient(225deg, rgba(0,200,255,0.06), transparent);
    border-radius: 0 0 0 30px;
  }
  .slice-label {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(0,200,255,0.3);
    margin-bottom: 6px;
  }
  .slice-value {
    font-size: 22px;
    font-weight: 200;
    color: #fff;
  }
  .slice-value .sub {
    font-size: 11px;
    color: rgba(0,200,255,0.3);
    margin-left: 4px;
  }
  .slice-trend {
    font-size: 10px;
    margin-top: 2px;
    letter-spacing: 1px;
  }
  .slice-trend.pos { color: #00ff88; }
  .slice-trend.neg { color: #ff4466; }
  .widget-title {
    font-size: 9px;
    letter-spacing: 3px;
    color: rgba(0,200,255,0.25);
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(0,180,255,0.04);
  }
  .spark-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  .spark-row {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .spark-row .label {
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    width: 50px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .spark-row .track {
    flex: 1;
    height: 2px;
    background: rgba(0,100,200,0.08);
    border-radius: 2px;
    overflow: hidden;
  }
  .spark-row .fill {
    height: 100%;
    border-radius: 2px;
  }
  .spark-row .val {
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    width: 40px;
    text-align: right;
    letter-spacing: 1px;
  }
</style>
</head>
<body>
<canvas id="gridCanvas"></canvas>
<div class="glaive">
  <div class="sidebar">
    <div class="brand">
      nexus
      <strong>GLAIVE</strong>
    </div>
    <div class="nav-item active">overview <span class="badge">98%</span></div>
    <div class="nav-item">analytics <span class="badge">73%</span></div>
    <div class="nav-item">topology <span class="badge">stable</span></div>
    <div class="nav-item">deployments <span class="badge">3</span></div>
    <div class="nav-item">alerts <span class="badge" style="color:#ff4466;">2</span></div>
    <div class="nav-item">settings</div>
  </div>
  <div class="main-panel">
    <div class="arc-display">
      <canvas id="arcCanvas" width="500" height="200"></canvas>
      <div class="arc-stats">
        <div class="arc-stat">
          <div class="num">128<span class="highlight">.4</span></div>
          <div class="lbl">requests/s</div>
        </div>
        <div class="arc-stat">
          <div class="num">99<span class="highlight">.97</span>%</div>
          <div class="lbl">success rate</div>
        </div>
        <div class="arc-stat">
          <div class="num">14<span class="highlight">ms</span></div>
          <div class="lbl">p50 latency</div>
        </div>
      </div>
    </div>
    <div class="diagonal-slice">
      <div class="slice-card">
        <div class="slice-label">data processed</div>
        <div class="slice-value">2.4<span class="sub">TB</span></div>
        <div class="slice-trend pos">+18.2% vs yesterday</div>
      </div>
      <div class="slice-card">
        <div class="slice-label">active sessions</div>
        <div class="slice-value">1,247<span class="sub">users</span></div>
        <div class="slice-trend pos">+342 peak</div>
      </div>
      <div class="slice-card">
        <div class="slice-label">cache hit ratio</div>
        <div class="slice-value">94.7<span class="sub">%</span></div>
        <div class="slice-trend pos">+1.2%</div>
      </div>
      <div class="slice-card">
        <div class="slice-label">error budget</div>
        <div class="slice-value">87<span class="sub">% remaining</span></div>
        <div class="slice-trend neg">-3% this week</div>
      </div>
    </div>
  </div>
  <div class="sidebar-right">
    <div class="widget-title">system load</div>
    <div class="spark-group">
      <div class="spark-row">
        <span class="label">CPU</span>
        <div class="track"><div class="fill" style="width:34%;background:linear-gradient(90deg,rgba(0,200,255,0.2),rgba(0,200,255,0.4));"></div></div>
        <span class="val">34%</span>
      </div>
      <div class="spark-row">
        <span class="label">RAM</span>
        <div class="track"><div class="fill" style="width:62%;background:linear-gradient(90deg,rgba(0,200,255,0.2),rgba(0,200,255,0.5));"></div></div>
        <span class="val">62%</span>
      </div>
      <div class="spark-row">
        <span class="label">DISK</span>
        <div class="track"><div class="fill" style="width:41%;background:linear-gradient(90deg,rgba(0,200,255,0.15),rgba(0,200,255,0.35));"></div></div>
        <span class="val">41%</span>
      </div>
      <div class="spark-row">
        <span class="label">NET</span>
        <div class="track"><div class="fill" style="width:28%;background:linear-gradient(90deg,rgba(0,200,255,0.15),rgba(0,200,255,0.3));"></div></div>
        <span class="val">28%</span>
      </div>
    </div>
    <div class="widget-title" style="margin-top:16px;">quick actions</div>
    <div style="display:flex;flex-direction:column;gap:6px;">
      <div style="padding:8px 12px;border:1px solid rgba(0,180,255,0.06);border-radius:8px;font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.2);cursor:default;">
        restart pipeline
      </div>
      <div style="padding:8px 12px;border:1px solid rgba(0,180,255,0.06);border-radius:8px;font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.2);cursor:default;">
        clear cache
      </div>
      <div style="padding:8px 12px;border:1px solid rgba(0,180,255,0.06);border-radius:8px;font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.2);cursor:default;">
        run diagnostics
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  const gc = document.getElementById('gridCanvas');
  const gctx = gc.getContext('2d');
  let w = gc.width = window.innerWidth;
  let h = gc.height = window.innerHeight;
  function drawGrid(){
    gctx.clearRect(0,0,w,h);
    gctx.strokeStyle = 'rgba(0,180,255,0.03)';
    gctx.lineWidth = 0.5;
    const step = 60;
    for(let x=0;x<w;x+=step){ gctx.beginPath();gctx.moveTo(x,0);gctx.lineTo(x,h);gctx.stroke(); }
    for(let y=0;y<h;y+=step){ gctx.beginPath();gctx.moveTo(0,y);gctx.lineTo(w,y);gctx.stroke(); }
  }
  drawGrid();
  window.addEventListener('resize',()=>{w=gc.width=window.innerWidth;h=gc.height=window.innerHeight;drawGrid();});
  const ac = document.getElementById('arcCanvas');
  const actx = ac.getContext('2d');
  const aw = 500, ah = 200;
  function drawArc(){
    actx.clearRect(0,0,aw,ah);
    actx.beginPath();
    actx.arc(250, 220, 160, Math.PI + 0.2, Math.PI*2 - 0.2);
    actx.strokeStyle = 'rgba(0,200,255,0.08)';
    actx.lineWidth = 1;
    actx.stroke();
    actx.beginPath();
    actx.arc(250, 220, 130, Math.PI + 0.2, Math.PI*2 - 0.2);
    actx.strokeStyle = 'rgba(0,200,255,0.05)';
    actx.lineWidth = 0.5;
    actx.stroke();
    const segments = 24;
    for(let i=0;i<segments;i++){
      const angle = Math.PI + 0.2 + (Math.PI - 0.4) * (i/segments);
      const len = 12;
      const r1 = 155, r2 = 155 + len;
      const x1 = 250 + Math.cos(angle)*r1;
      const y1 = 220 + Math.sin(angle)*r1;
      const x2 = 250 + Math.cos(angle)*r2;
      const y2 = 220 + Math.sin(angle)*r2;
      actx.beginPath();
      actx.moveTo(x1,y1); actx.lineTo(x2,y2);
      actx.strokeStyle = i % 3 === 0 ? 'rgba(0,200,255,0.15)' : 'rgba(0,200,255,0.05)';
      actx.lineWidth = 0.5;
      actx.stroke();
    }
  }
  drawArc();
})();
</script>
</body>
</html>
```
---
MOCKUP 3: NEON EDGE — GLAIVE LAYOUT
Three-column asymmetric layout with arc canvas (programmatic tick marks and radial bands), JS-drawn grid background, diagonal corner accent pseudo-elements on cards. Sparkline-style resource bars in the right sidebar. Distinct from the previous two: sharp geometric, grid-based, information-dense, no central ring.
---
MOCKUP 4: DRIFT — AMBIENT FLOATING PANELS
Floating independent panels on a deep field with animated wave distortion. Each panel is a self-contained widget with no shared container. Organic curves replace straight grid lines. Wave distortion effect on background text.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Drift — Ambient Panels</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #06061a;
    font-family: 'Inter', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding: 24px;
  }
  canvas#waveCanvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
  }
  .field {
    position: relative;
    z-index: 1;
    width: 1150px;
    max-width: 96vw;
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    justify-content: center;
  }
  .drift-panel {
    background: rgba(8,8,30,0.5);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(0,180,255,0.06);
    border-radius: 24px;
    padding: 20px;
    transition: all 0.3s ease;
    cursor: default;
  }
  .drift-panel:hover {
    border-color: rgba(0,200,255,0.15);
    box-shadow: 0 8px 40px rgba(0,80,200,0.06);
    transform: translateY(-2px);
  }
  .panel-lg {
    flex: 2 1 400px;
    min-width: 320px;
  }
  .panel-sm {
    flex: 1 1 200px;
    min-width: 180px;
  }
  .panel-md {
    flex: 1 1 280px;
    min-width: 240px;
  }
  .panel-title {
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(0,200,255,0.25);
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0,180,255,0.04);
  }
  .big-num {
    font-size: 48px;
    font-weight: 200;
    color: #fff;
    letter-spacing: 2px;
    line-height: 1;
  }
  .big-num .sub {
    font-size: 16px;
    color: rgba(0,200,255,0.25);
    font-weight: 300;
    margin-left: 6px;
  }
  .change-indicator {
    font-size: 11px;
    margin-top: 6px;
    letter-spacing: 1px;
  }
  .change-indicator.pos { color: #00ff88; }
  .change-indicator.neg { color: #ff4466; }
  .mini-chart {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 50px;
    margin-top: 12px;
  }
  .mini-bar {
    flex: 1;
    min-height: 3px;
    border-radius: 2px 2px 0 0;
    background: linear-gradient(180deg, rgba(0,200,255,0.3), rgba(0,100,200,0.05));
  }
  .tag-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
  }
  .tag {
    padding: 3px 10px;
    border: 1px solid rgba(0,180,255,0.08);
    border-radius: 20px;
    font-size: 9px;
    letter-spacing: 1px;
    color: rgba(0,200,255,0.35);
    text-transform: uppercase;
  }
  .tag.active {
    border-color: rgba(0,255,136,0.15);
    color: #00ff88;
  }
  .status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(0,180,255,0.03);
    font-size: 11px;
    color: rgba(255,255,255,0.3);
  }
  .status-row .val {
    color: rgba(255,255,255,0.5);
  }
  .status-row:last-child { border-bottom: none; }
  .indicator-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    margin-right: 6px;
  }
  .indicator-dot.green { background: #00ff88; box-shadow: 0 0 8px rgba(0,255,136,0.2); }
  .indicator-dot.yellow { background: #ffbb44; box-shadow: 0 0 8px rgba(255,187,68,0.15); }
  .indicator-dot.red { background: #ff4466; box-shadow: 0 0 8px rgba(255,68,102,0.15); }
  .timeline {
    position: relative;
    padding-left: 16px;
  }
  .timeline::before {
    content: '';
    position: absolute;
    left: 4px;
    top: 4px;
    bottom: 4px;
    width: 1px;
    background: rgba(0,200,255,0.06);
  }
  .tl-item {
    position: relative;
    padding: 4px 0 4px 12px;
    font-size: 10px;
    color: rgba(255,255,255,0.25);
    letter-spacing: 1px;
  }
  .tl-item::before {
    content: '';
    position: absolute;
    left: -3px;
    top: 9px;
    width: 4px; height: 4px;
    border-radius: 50%;
    background: rgba(0,200,255,0.15);
  }
  .tl-item:first-child::before { background: #00ff88; box-shadow: 0 0 6px rgba(0,255,136,0.2); }
  .tl-item .ts {
    color: rgba(0,200,255,0.15);
    margin-right: 6px;
  }
</style>
</head>
<body>
<canvas id="waveCanvas"></canvas>
<div class="field">
  <div class="drift-panel panel-lg">
    <div class="panel-title">primary throughput</div>
    <div class="big-num">2.4<span class="sub">gbps</span></div>
    <div class="change-indicator pos">+12.3% vs yesterday</div>
    <div class="mini-chart" id="mini1"></div>
  </div>
  <div class="drift-panel panel-sm">
    <div class="panel-title">uptime</div>
    <div class="big-num" style="font-size:36px;">99.97<span class="sub">%</span></div>
    <div class="change-indicator pos">over 30 days</div>
  </div>
  <div class="drift-panel panel-sm">
    <div class="panel-title">error rate</div>
    <div class="big-num" style="font-size:36px;">0.02<span class="sub">%</span></div>
    <div class="change-indicator neg">+0.003% today</div>
  </div>
  <div class="drift-panel panel-md">
    <div class="panel-title">active tags</div>
    <div class="tag-cloud">
      <span class="tag">production</span>
      <span class="tag active">canary</span>
      <span class="tag">staging</span>
      <span class="tag">dr</span>
      <span class="tag">edge-01</span>
      <span class="tag">edge-02</span>
      <span class="tag">core</span>
    </div>
  </div>
  <div class="drift-panel panel-md">
    <div class="panel-title">node health</div>
    <div class="status-row"><span><span class="indicator-dot green"></span>primary-01</span><span class="val">online</span></div>
    <div class="status-row"><span><span class="indicator-dot green"></span>primary-02</span><span class="val">online</span></div>
    <div class="status-row"><span><span class="indicator-dot yellow"></span>edge-07</span><span class="val">degraded</span></div>
    <div class="status-row"><span><span class="indicator-dot green"></span>cache-01</span><span class="val">online</span></div>
    <div class="status-row"><span><span class="indicator-dot green"></span>cache-02</span><span class="val">online</span></div>
    <div class="status-row"><span><span class="indicator-dot red"></span>worker-11</span><span class="val">offline</span></div>
  </div>
  <div class="drift-panel panel-md">
    <div class="panel-title">recent events</div>
    <div class="timeline">
      <div class="tl-item"><span class="ts">14:23</span>deploy v3.2.2 complete</div>
      <div class="tl-item"><span class="ts">14:12</span>auto-scaler triggered +2</div>
      <div class="tl-item"><span class="ts">13:58</span>config sync received</div>
      <div class="tl-item"><span class="ts">13:41</span>health check pass</div>
      <div class="tl-item"><span class="ts">13:29</span>backup rotated</div>
    </div>
  </div>
</div>
<script>
(function(){
  const c = document.getElementById('waveCanvas');
  const ctx = c.getContext('2d');
  let w = c.width = window.innerWidth;
  let h = c.height = window.innerHeight;
  let t = 0;
  function drawWaves(){
    ctx.clearRect(0,0,w,h);
    for(let row=0; row<8; row++){
      ctx.beginPath();
      ctx.strokeStyle = `rgba(0,180,255,${0.015 + row*0.002})`;
      ctx.lineWidth = 0.5;
      const yBase = h * (0.1 + row*0.1);
      for(let x=0; x<w; x+=2){
        const y = yBase + Math.sin(x*0.01 + t + row*0.8) * 6 + Math.sin(x*0.02 + t*0.7 + row*1.2) * 3;
        x===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
      }
      ctx.stroke();
    }
    t += 0.02;
    requestAnimationFrame(drawWaves);
  }
  drawWaves();
  window.addEventListener('resize',()=>{w=c.width=window.innerWidth;h=c.height=window.innerHeight;});
  function sparkBars(id, count){
    const el = document.getElementById(id);
    if(!el) return;
    let html = '';
    for(let i=0;i<count;i++){
      const pct = Math.random()*0.7+0.3;
      html += `<div class="mini-bar" style="height:${pct*50}px;"></div>`;
    }
    el.innerHTML = html;
  }
  sparkBars('mini1', 30);
})();
</script>
</body>
</html>
```
---
MOCKUP 4: DRIFT — AMBIENT FLOATING PANELS
No shared container — panels float independently in a flex field. Background features animated sine-wave distortion (JS loop, zero divs). Each panel has distinct content (metric, tags, health list, timeline). Wireframe-thin borders, soft curves, ambient glow. Most lightweight and organic of the four — deliberately no grid, no chrome, no scanlines.
---
THEME SUMMARY
theme                  | aesthetic                           | key differentiator
quantum overview       | glass morphism + particle network   | metric cards + bar chart + activity feed in a single framed container; particle connections
holo terminal          | terminal-core + holographic rings   | monospace log, mesh topology grid, concentric animated rings, scanline overlay
neon edge — glaive     | asymmetric three-column + arc viz   | diagonal accents, sparkbars, canvas arc with tick marks, side navigation; no container nesting
drift — ambient panels | organic floating panels + wave bg   | zero shared container, sine-wave distortion canvas, tag cloud + timeline, most lightweight
All repeated decorative elements (particles, stars, grid lines, wave lines, arc ticks, bar pairs, mini-chart bars) are generated programmatically via JavaScript — zero static div repetition for visual effects. Every mockup uses exclusively class-based styling with no inline styles except JS-driven dynamic values. Maximum one nested wrapper per section.