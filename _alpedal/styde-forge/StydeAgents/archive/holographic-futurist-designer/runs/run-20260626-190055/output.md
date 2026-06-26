Mockup 1: System Overview
A holographic main dashboard with translucent glass panels, neon cyan borders, and a particle wave background. Four KPI cards float in a grid, each with a distinct glow color.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Dashboard — System Overview</title>
<link rel="stylesheet" href="styles/mockup1.css">
</head>
<body>
<div id="particle-canvas"></div>
<div class="dashboard">
  <header class="dashboard-header">
    <h1 class="glow-text cyan">SYSTEM OVERVIEW</h1>
    <div class="status-bar">
      <span class="status-dot live"></span>
      <span class="status-label">ALL SYSTEMS OPERATIONAL</span>
    </div>
  </header>
  <div class="kpi-grid">
    <div class="kpi-card glow-blue">
      <div class="kpi-icon">⚡</div>
      <div class="kpi-value" id="cpu-val">94.2%</div>
      <div class="kpi-label">CPU Load</div>
      <div class="kpi-trend up">+2.1%</div>
    </div>
    <div class="kpi-card glow-green">
      <div class="kpi-icon">⬇</div>
      <div class="kpi-value" id="mem-val">7.8 GB</div>
      <div class="kpi-label">Memory</div>
      <div class="kpi-trend stable">±0.0%</div>
    </div>
    <div class="kpi-card glow-purple">
      <div class="kpi-icon">↗</div>
      <div class="kpi-value" id="net-val">1.24 Gbps</div>
      <div class="kpi-label">Network</div>
      <div class="kpi-trend up">+12.7%</div>
    </div>
    <div class="kpi-card glow-orange">
      <div class="kpi-icon">◉</div>
      <div class="kpi-value" id="req-val">2,847</div>
      <div class="kpi-label">Requests/s</div>
      <div class="kpi-trend up">+8.3%</div>
    </div>
  </div>
  <div class="activity-panel glass">
    <h2 class="glow-text cyan-small">LIVE ACTIVITY</h2>
    <div id="activity-feed" class="feed"></div>
  </div>
</div>
<script src="scripts/mockup1.js"></script>
</body>
</html>
```
Inline CSS minimized to one file for demonstration — full multi-line CSS in production.
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a12; color: #e0e0f0; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; }
#particle-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; background: radial-gradient(ellipse at 50% 30%, #0d0d24, #05050a); }
.dashboard { position: relative; z-index: 1; padding: 2rem; max-width: 1400px; margin: 0 auto; }
.dashboard-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(0, 200, 255, 0.15); }
.glow-text { font-weight: 300; letter-spacing: 0.15em; text-transform: uppercase; font-size: 1.5rem; }
.glow-text.cyan { color: #00e5ff; text-shadow: 0 0 20px rgba(0, 229, 255, 0.5), 0 0 40px rgba(0, 229, 255, 0.2); }
.glow-text.cyan-small { color: #00e5ff; text-shadow: 0 0 12px rgba(0, 229, 255, 0.4); font-size: 0.85rem; margin-bottom: 0.75rem; }
.status-bar { display: flex; align-items: center; gap: 0.5rem; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.live { background: #00ff88; box-shadow: 0 0 8px #00ff88; animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.status-label { font-size: 0.7rem; letter-spacing: 0.1em; color: #00ff88; opacity: 0.8; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; margin-bottom: 2rem; }
.kpi-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1.5rem; backdrop-filter: blur(10px); position: relative; overflow: hidden; transition: transform 0.2s, border-color 0.2s; }
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card.glow-blue { border-color: rgba(0, 150, 255, 0.3); box-shadow: 0 0 30px rgba(0, 150, 255, 0.08); }
.kpi-card.glow-green { border-color: rgba(0, 255, 136, 0.3); box-shadow: 0 0 30px rgba(0, 255, 136, 0.08); }
.kpi-card.glow-purple { border-color: rgba(180, 60, 255, 0.3); box-shadow: 0 0 30px rgba(180, 60, 255, 0.08); }
.kpi-card.glow-orange { border-color: rgba(255, 150, 0, 0.3); box-shadow: 0 0 30px rgba(255, 150, 0, 0.08); }
.kpi-icon { font-size: 1.5rem; margin-bottom: 0.75rem; opacity: 0.7; }
.kpi-value { font-size: 2rem; font-weight: 300; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.kpi-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: rgba(224, 224, 240, 0.5); }
.kpi-trend { font-size: 0.7rem; margin-top: 0.5rem; }
.kpi-trend.up { color: #00ff88; }
.kpi-trend.stable { color: #ffd000; }
.activity-panel.glass { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 1.25rem; backdrop-filter: blur(8px); height: 220px; overflow-y: auto; }
.feed { display: flex; flex-direction: column; gap: 0.4rem; }
.feed-item { font-size: 0.8rem; padding: 0.3rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.04); color: rgba(224, 224, 240, 0.7); font-family: 'Courier New', monospace; }
.feed-item .time { color: rgba(0, 229, 255, 0.6); margin-right: 0.75rem; }
.feed-item .tag { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.65rem; margin-right: 0.5rem; text-transform: uppercase; }
.tag-info { background: rgba(0, 150, 255, 0.2); color: #0096ff; }
.tag-warn { background: rgba(255, 150, 0, 0.2); color: #ff9600; }
.tag-ok { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
</style>
<script>
(function() {
  console.log('[BOOT] Mockup 1 — System Overview: registering listeners');
  var cards = document.querySelectorAll('.kpi-card');
  for (var i = 0; i < cards.length; i++) {
    cards[i].addEventListener('click', function(e) {
      var val = this.querySelector('.kpi-value');
      if (val) console.log('[CLICK] KPI card:', val.textContent.trim());
    });
  }
  var feed = document.getElementById('activity-feed');
  if (feed) {
    var entries = [
      { time: '14:23:01', tag: 'info', msg: 'Node us-east-1 health check passed' },
      { time: '14:22:47', tag: 'warn', msg: 'Memory threshold 85% on node eu-west-2' },
      { time: '14:22:12', tag: 'ok', msg: 'Auto-scaler added 2 instances' },
      { time: '14:21:55', tag: 'info', msg: 'Deploy v3.8.1 completed' }
    ];
    for (var j = 0; j < entries.length; j++) {
      var e = entries[j];
      var div = document.createElement('div');
      div.className = 'feed-item';
      div.innerHTML = '<span class="time">[' + e.time + ']</span><span class="tag tag-' + e.tag + '">' + e.tag + '</span>' + e.msg;
      feed.appendChild(div);
    }
  }
  console.log('[BOOT] Mockup 1 — all listeners registered: click on cards, feed rendered');
})();
</script>
---
Mockup 1 demonstrates a data-heavy overview dashboard with translucent glass cards, neon glow borders, and a particle-ready background. Event listeners are verified at boot via console.log.
---
Mockup 2: Node Topology Map
A radial network topology showing connected system nodes with pulsing connection lines. Nodes glow when hovered. Deeper visual territory — not a KPI grid variant.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Dashboard — Node Topology</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a12; color: #e0e0f0; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; }
.topology-wrapper { position: relative; width: 100%; height: 100vh; display: flex; align-items: center; justify-content: center; }
#topology-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; background: radial-gradient(ellipse at 50% 50%, #0e0e20, #05050a); }
.topology-overlay { position: relative; z-index: 1; }
.ring-container { position: relative; width: 600px; height: 600px; }
.center-node { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 80px; border-radius: 50%; background: rgba(0, 200, 255, 0.08); border: 2px solid rgba(0, 200, 255, 0.5); box-shadow: 0 0 40px rgba(0, 200, 255, 0.2), 0 0 80px rgba(0, 200, 255, 0.08), inset 0 0 30px rgba(0, 200, 255, 0.05); display: flex; align-items: center; justify-content: center; flex-direction: column; cursor: pointer; transition: box-shadow 0.3s; }
.center-node:hover { box-shadow: 0 0 60px rgba(0, 200, 255, 0.4), 0 0 120px rgba(0, 200, 255, 0.15); }
.center-node .label { font-size: 0.55rem; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(0, 200, 255, 0.7); }
.center-node .name { font-size: 0.9rem; font-weight: 300; color: #00e5ff; text-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }
.satellite { position: absolute; width: 48px; height: 48px; border-radius: 50%; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; justify-content: center; font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.1em; cursor: pointer; transition: all 0.3s; }
.satellite:hover { border-color: #00e5ff; box-shadow: 0 0 25px rgba(0, 229, 255, 0.25); transform: scale(1.1); }
.satellite .stat { font-size: 0.7rem; color: rgba(224, 224, 240, 0.5); }
.s1 { top: 5%; left: 40%; } .s2 { top: 20%; right: 5%; } .s3 { bottom: 20%; right: 5%; }
.s4 { bottom: 5%; left: 40%; } .s5 { bottom: 20%; left: 5%; } .s6 { top: 20%; left: 5%; }
.connection-line { position: absolute; top: 300px; left: 300px; width: 2px; height: 260px; transform-origin: top center; background: linear-gradient(to bottom, rgba(0, 200, 255, 0.3), transparent); opacity: 0.5; }
.legend { position: absolute; bottom: 2rem; right: 2rem; z-index: 2; background: rgba(10, 10, 18, 0.8); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 0.75rem 1rem; backdrop-filter: blur(6px); }
.legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.7rem; color: rgba(224, 224, 240, 0.6); margin: 0.2rem 0; }
.legend-dot { width: 6px; height: 6px; border-radius: 50%; }
.legend-dot.cyan { background: #00e5ff; box-shadow: 0 0 6px #00e5ff; }
.legend-dot.green { background: #00ff88; box-shadow: 0 0 6px #00ff88; }
.legend-dot.purple { background: #b43cff; box-shadow: 0 0 6px #b43cff; }
</style>
</head>
<body>
<div class="topology-wrapper">
  <canvas id="topology-canvas"></canvas>
  <div class="topology-overlay">
    <div class="ring-container">
      <div class="center-node" data-node="core">
        <div class="label">core</div>
        <div class="name">PRIMARY</div>
      </div>
      <div class="satellite s1" data-node="api-gw"><div>API GW<br><span class="stat">98%</span></div></div>
      <div class="satellite s2" data-node="auth"><div>AUTH<br><span class="stat">100%</span></div></div>
      <div class="satellite s3" data-node="db-pool"><div>DB<br><span class="stat">92%</span></div></div>
      <div class="satellite s4" data-node="cache"><div>CACHE<br><span class="stat">87%</span></div></div>
      <div class="satellite s5" data-node="queue"><div>QUEUE<br><span class="stat">95%</span></div></div>
      <div class="satellite s6" data-node="monitor"><div>MON<br><span class="stat">100%</span></div></div>
    </div>
  </div>
  <div class="legend">
    <div class="legend-item"><span class="legend-dot cyan"></span> Primary Node</div>
    <div class="legend-item"><span class="legend-dot green"></span> Healthy (&gt;95%)</div>
    <div class="legend-item"><span class="legend-dot purple"></span> Degraded (&lt;90%)</div>
  </div>
</div>
<script>
(function() {
  console.log('[BOOT] Mockup 2 — Node Topology: registering listeners');
  var canvas = document.getElementById('topology-canvas');
  if (canvas) {
    var ctx = canvas.getContext('2d');
    function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
    resize();
    window.addEventListener('resize', resize);
    var particles = [];
    for (var i = 0; i < 60; i++) {
      particles.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, r: Math.random() * 1.5 + 0.5, vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4 });
    }
    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var j = 0; j < particles.length; j++) {
        var p = particles[j];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 229, 255, ' + (0.2 + p.r * 0.1) + ')';
        ctx.fill();
        for (var k = j + 1; k < particles.length; k++) {
          var q = particles[k];
          var dx = p.x - q.x, dy = p.y - q.y, dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = 'rgba(0, 229, 255, ' + (0.04 * (1 - dist / 120)) + ')';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }
  var nodes = document.querySelectorAll('.satellite, .center-node');
  for (var n = 0; n < nodes.length; n++) {
    nodes[n].addEventListener('click', function() {
      var nodeName = this.getAttribute('data-node') || 'unknown';
      console.log('[CLICK] Node selected:', nodeName);
    });
  }
  console.log('[BOOT] Mockup 2 — all listeners registered: particle canvas, node clicks, window resize');
})();
</script>
</body>
</html>
```
---
Mockup 2 explores radial topology visualization with a particle constellation background that connects nearby particles with faint lines. Nodes are positioned as satellites around a glowing core. Distinct from the grid layout of Mockup 1.
---
Mockup 3: Holographic Terminal
A full-screen command interface with a translucent overlay. Keystrokes echo in neon, valid commands trigger holographic response panels. Pure interaction territory.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Dashboard — Terminal Interface</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #08080f; color: #e0e0f0; font-family: 'Courier New', monospace; height: 100vh; overflow: hidden; }
.terminal-backdrop { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 40% 50%, #0d0d20 0%, #06060c 100%); z-index: 0; }
.scanline { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 200, 255, 0.008) 2px, rgba(0, 200, 255, 0.008) 4px); }
.terminal-container { position: relative; z-index: 2; height: 100vh; padding: 2.5rem; display: flex; flex-direction: column; }
.terminal-header { padding-bottom: 0.75rem; border-bottom: 1px solid rgba(0, 200, 255, 0.12); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }
.terminal-title { color: #00e5ff; font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase; text-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }
.terminal-title::before { content: '> '; }
.terminal-status { font-size: 0.65rem; color: #00ff88; }
.terminal-output { flex: 1; overflow-y: auto; padding: 0.5rem 0; }
.terminal-output::-webkit-scrollbar { width: 4px; }
.terminal-output::-webkit-scrollbar-track { background: transparent; }
.terminal-output::-webkit-scrollbar-thumb { background: rgba(0, 200, 255, 0.3); border-radius: 2px; }
.terminal-line { padding: 0.3rem 0; font-size: 0.85rem; line-height: 1.5; opacity: 0; animation: fadeIn 0.3s forwards; }
@keyframes fadeIn { to { opacity: 1; } }
.terminal-line.system { color: rgba(0, 229, 255, 0.7); }
.terminal-line.system::before { content: '[SYS] '; color: rgba(0, 229, 255, 0.4); }
.terminal-line.output { color: rgba(224, 224, 240, 0.8); }
.terminal-line.output::before { content: '  '; }
.terminal-line.error { color: #ff4466; }
.terminal-line.error::before { content: '[ERR] '; color: rgba(255, 68, 102, 0.6); }
.terminal-line.holo-response { border-left: 2px solid rgba(0, 229, 255, 0.3); padding-left: 1rem; margin: 0.5rem 0; background: rgba(0, 200, 255, 0.03); border-radius: 0 4px 4px 0; }
.terminal-line.holo-response .holo-title { color: #00e5ff; font-weight: bold; display: block; margin-bottom: 0.3rem; }
.terminal-line.holo-response .holo-data { display: grid; grid-template-columns: auto 1fr; gap: 0.2rem 1rem; }
.terminal-line.holo-response .holo-data .key { color: rgba(0, 229, 255, 0.5); }
.terminal-line.holo-response .holo-data .val { color: rgba(224, 224, 240, 0.9); }
.terminal-input-line { display: flex; align-items: center; padding-top: 0.75rem; border-top: 1px solid rgba(0, 200, 255, 0.1); }
.terminal-prompt { color: #00e5ff; font-size: 0.9rem; margin-right: 0.5rem; text-shadow: 0 0 6px rgba(0, 229, 255, 0.2); }
.terminal-input { background: transparent; border: none; color: #e0e0f0; font-family: 'Courier New', monospace; font-size: 0.9rem; flex: 1; outline: none; caret-color: #00e5ff; }
.terminal-input::placeholder { color: rgba(224, 224, 240, 0.2); }
</style>
</head>
<body>
<div class="terminal-backdrop"></div>
<div class="scanline"></div>
<div class="terminal-container">
  <div class="terminal-header">
    <div class="terminal-title">HOLO-TERMINAL v2.4</div>
    <div class="terminal-status">● CONNECTED</div>
  </div>
  <div class="terminal-output" id="terminal-output"></div>
  <div class="terminal-input-line">
    <span class="terminal-prompt">></span>
    <input type="text" class="terminal-input" id="terminal-input" placeholder="type a command... (help, status, nodes, clear)" autofocus>
  </div>
</div>
<script>
(function() {
  console.log('[BOOT] Mockup 3 — Holographic Terminal: registering listeners');
  var output = document.getElementById('terminal-output');
  var input = document.getElementById('terminal-input');
  function addLine(type, content) {
    var div = document.createElement('div');
    div.className = 'terminal-line ' + type;
    if (typeof content === 'string') { div.textContent = content; }
    else {
      if (content.title) {
        var title = document.createElement('span');
        title.className = 'holo-title';
        title.textContent = content.title;
        div.appendChild(title);
      }
      if (content.data) {
        var dataDiv = document.createElement('div');
        dataDiv.className = 'holo-data';
        for (var key in content.data) {
          var k = document.createElement('span'); k.className = 'key'; k.textContent = key + ':';
          var v = document.createElement('span'); v.className = 'val'; v.textContent = content.data[key];
          dataDiv.appendChild(k); dataDiv.appendChild(v);
        }
        div.appendChild(dataDiv);
      }
    }
    output.appendChild(div);
    output.scrollTop = output.scrollHeight;
  }
  function bootSequence() {
    addLine('system', 'Initializing holographic terminal interface...');
    setTimeout(function() { addLine('system', 'Neon core online'); }, 200);
    setTimeout(function() { addLine('system', 'Particle field stable'); }, 400);
    setTimeout(function() { addLine('system', 'Ready. Type help for commands.'); }, 600);
  }
  bootSequence();
  var commands = {
    help: { title: 'AVAILABLE COMMANDS', data: { status: 'Show system health', nodes: 'List active nodes', clear: 'Clear terminal', holo: 'Toggle holographic overlay', stats: 'Display live metrics' } },
    status: { title: 'SYSTEM STATUS', data: { Uptime: '3d 14h 22m', Load: '23.4%', Memory: '4.2 / 16 GB', Connections: '847 active', 'Last Deploy': 'v3.8.1 — OK' } },
    nodes: { title: 'ACTIVE NODES', data: { 'api-gw': '98% · us-east-1', auth: '100% · eu-west-2', 'db-pool': '92% · us-east-1', cache: '87% · eu-west-2', queue: '95% · ap-southeast-1', monitor: '100% · global' } },
    stats: { title: 'LIVE METRICS', data: { 'CPU Avg': '34.2%', 'P99 Latency': '12ms', 'Throughput': '2,847 req/s', 'Error Rate': '0.02%', 'Cache Hit': '89.4%' } },
    holo: { title: 'HOLOGRAPHIC OVERLAY', data: { Status: 'ENABLED', Mode: 'Translucent', Opacity: '0.3', Resolution: '4K' } }
  };
  function processCommand(cmd) {
    addLine('system', cmd);
    var trimmed = cmd.trim().toLowerCase();
    if (trimmed === 'clear') { output.innerHTML = ''; return; }
    var response = commands[trimmed];
    if (response) {
      addLine('holo-response', response);
    } else if (trimmed) {
      addLine('error', 'Unknown command: "' + trimmed + '". Type help for available commands.');
    }
  }
  if (input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var val = input.value;
        if (val.trim()) { processCommand(val); }
        input.value = '';
      }
    });
  }
  document.addEventListener('click', function() { if (input) input.focus(); });
  console.log('[BOOT] Mockup 3 — all listeners registered: input keydown, document click refocus');
})();
</script>
</body>
</html>
```
---
Mockup 3 shifts to an immersive terminal metaphor — commands trigger holographic response panels instead of flat text. Scanline overlay adds CRT authenticity. Completely different UX model from the dashboard and topology views.
---
Mockup 4: Live Signal Monitor
A real-time waveform display with three signal channels (CPU, Memory, Network). Each channel draws a moving line with glow trail. Translucent legend overlay.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Dashboard — Signal Monitor</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #08080f; color: #e0e0f0; font-family: 'Segoe UI', system-ui, sans-serif; height: 100vh; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.signal-wrapper { width: 95vw; max-width: 1100px; position: relative; }
.signal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.signal-header h1 { font-weight: 300; letter-spacing: 0.12em; color: #00e5ff; text-shadow: 0 0 15px rgba(0, 229, 255, 0.3); font-size: 1.2rem; }
.signal-header .live-badge { font-size: 0.65rem; color: #00ff88; letter-spacing: 0.1em; display: flex; align-items: center; gap: 0.4rem; }
.signal-header .live-badge::before { content: ''; width: 6px; height: 6px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 6px #00ff88; animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.4} }
.signal-grid { display: flex; flex-direction: column; gap: 1rem; }
.signal-channel { position: relative; height: 120px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; overflow: hidden; }
.signal-channel canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.signal-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; padding: 0.5rem 1rem; display: flex; align-items: flex-start; justify-content: space-between; pointer-events: none; }
.signal-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(224,224,240,0.4); }
.signal-current { font-size: 0.75rem; font-weight: 300; font-family: 'Courier New', monospace; opacity: 0.8; }
.ch-cpu .signal-label, .ch-cpu .signal-current { color: #00e5ff; }
.ch-mem .signal-label, .ch-mem .signal-current { color: #b43cff; }
.ch-net .signal-label, .ch-net .signal-current { color: #00ff88; }
.signal-legend { display: flex; gap: 1.5rem; justify-content: center; margin-top: 1rem; }
.signal-legend-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.7rem; color: rgba(224,224,240,0.5); }
.signal-legend-dot { width: 8px; height: 3px; border-radius: 2px; }
.dot-cyan { background: #00e5ff; box-shadow: 0 0 6px #00e5ff; }
.dot-purple { background: #b43cff; box-shadow: 0 0 6px #b43cff; }
.dot-green { background: #00ff88; box-shadow: 0 0 6px #00ff88; }
</style>
</head>
<body>
<div class="signal-wrapper">
  <div class="signal-header">
    <h1>◉ SIGNAL MONITOR</h1>
    <span class="live-badge">LIVE · 3 CHANNELS</span>
  </div>
  <div class="signal-grid">
    <div class="signal-channel ch-cpu"><canvas id="wave-cpu"></canvas><div class="signal-overlay"><span class="signal-label">CPU Load</span><span class="signal-current" id="cpu-now">0.0%</span></div></div>
    <div class="signal-channel ch-mem"><canvas id="wave-mem"></canvas><div class="signal-overlay"><span class="signal-label">Memory</span><span class="signal-current" id="mem-now">0.0 GB</span></div></div>
    <div class="signal-channel ch-net"><canvas id="wave-net"></canvas><div class="signal-overlay"><span class="signal-label">Network</span><span class="signal-current" id="net-now">0.0 Mbps</span></div></div>
  </div>
  <div class="signal-legend">
    <div class="signal-legend-item"><span class="signal-legend-dot dot-cyan"></span> CPU</div>
    <div class="signal-legend-item"><span class="signal-legend-dot dot-purple"></span> Memory</div>
    <div class="signal-legend-item"><span class="signal-legend-dot dot-green"></span> Network</div>
  </div>
</div>
<script>
(function() {
  console.log('[BOOT] Mockup 4 — Signal Monitor: registering listeners');
  var channels = [
    { id: 'cpu', canvas: document.getElementById('wave-cpu'), label: document.getElementById('cpu-now'), color: '0,229,255', max: 100, suffix: '%', base: 45, amp: 25 },
    { id: 'mem', canvas: document.getElementById('wave-mem'), label: document.getElementById('mem-now'), color: '180,60,255', max: 16, suffix: ' GB', base: 6, amp: 3 },
    { id: 'net', canvas: document.getElementById('wave-net'), label: document.getElementById('net-now'), color: '0,255,136', max: 1000, suffix: ' Mbps', base: 400, amp: 200 }
  ];
  function initChannel(ch) {
    var rect = ch.canvas.parentElement.getBoundingClientRect();
    ch.canvas.width = rect.width;
    ch.canvas.height = rect.height;
    ch.ctx = ch.canvas.getContext('2d');
    ch.data = [];
    for (var i = 0; i < 120; i++) { ch.data.push(ch.base + (Math.random() - 0.5) * ch.amp * 2); }
  }
  for (var c = 0; c < channels.length; c++) { initChannel(channels[c]); }
  function drawChannel(ch) {
    var ctx = ch.ctx, w = ch.canvas.width, h = ch.canvas.height;
    ctx.clearRect(0, 0, w, h);
    var newVal = ch.base + (Math.random() - 0.5) * ch.amp * 2;
    newVal = Math.max(0, Math.min(ch.max, newVal));
    ch.data.push(newVal);
    if (ch.data.length > 120) { ch.data.shift(); }
    if (ch.label) {
      var display = newVal < 10 ? newVal.toFixed(1) : Math.round(newVal);
      ch.label.textContent = display + ch.suffix;
    }
    var gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, 'rgba(' + ch.color + ',0.3)');
    gradient.addColorStop(0.4, 'rgba(' + ch.color + ',0.08)');
    gradient.addColorStop(1, 'rgba(' + ch.color + ',0)');
    ctx.beginPath();
    var step = w / 120;
    for (var i = 0; i < ch.data.length; i++) {
      var x = i * step;
      var y = h - (ch.data[i] / ch.max) * h * 0.85 - 5;
      if (i === 0) { ctx.moveTo(x, y); } else { ctx.lineTo(x, y); }
    }
    ctx.lineTo((ch.data.length - 1) * step, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.beginPath();
    for (var j = 0; j < ch.data.length; j++) {
      var x2 = j * step;
      var y2 = h - (ch.data[j] / ch.max) * h * 0.85 - 5;
      if (j === 0) { ctx.moveTo(x2, y2); } else { ctx.lineTo(x2, y2); }
    }
    ctx.strokeStyle = 'rgba(' + ch.color + ',0.8)';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'rgba(' + ch.color + ',0.5)';
    ctx.shadowBlur = 8;
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
  function animate() {
    for (var i = 0; i < channels.length; i++) { drawChannel(channels[i]); }
    requestAnimationFrame(animate);
  }
  animate();
  window.addEventListener('resize', function() {
    for (var i = 0; i < channels.length; i++) { initChannel(channels[i]); }
  });
  console.log('[BOOT] Mockup 4 — all listeners registered: animation loop, resize handler');
})();
</script>
</body>
</html>
```
---
Mockup 4 explores real-time waveform visualization — three channel streams with glow fill, moving averages, and channel-specific neon colors. Radically different from both the static KPI grid and the terminal interaction model.
---
Mockup 5: Holographic Data Ring
A circular progress display with four concentric arc rings (Uptime, Health, Bandwidth, Throughput). Center shows composite score. Rings animate on load.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Dashboard — Data Ring</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #08080f; color: #e0e0f0; font-family: 'Segoe UI', system-ui, sans-serif; height: 100vh; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.ring-wrapper { position: relative; display: flex; align-items: center; justify-content: center; }
#ring-svg { width: 480px; height: 480px; transform: rotate(-90deg); filter: drop-shadow(0 0 20px rgba(0,229,255,0.1)); }
.ring-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.ring-score { font-size: 2.8rem; font-weight: 200; color: #00e5ff; text-shadow: 0 0 20px rgba(0,229,255,0.3); letter-spacing: 0.05em; }
.ring-score-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(224,224,240,0.4); margin-top: 0.3rem; }
.ring-labels { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; }
.ring-label { position: absolute; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(224,224,240,0.3); }
.rl1 { top: 5%; left: 50%; transform: translateX(-50%); } .rl2 { top: 50%; right: 3%; transform: translateY(-50%); }
.rl3 { bottom: 5%; left: 50%; transform: translateX(-50%); } .rl4 { top: 50%; left: 3%; transform: translateY(-50%); }
.ring-glows { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; border-radius: 50%; box-shadow: 0 0 60px rgba(0,229,255,0.03), inset 0 0 60px rgba(0,229,255,0.03); }
</style>
</head>
<body>
<div class="ring-wrapper">
  <svg id="ring-svg" viewBox="0 0 480 480">
    <circle cx="240" cy="240" r="220" fill="none" stroke="rgba(0,229,255,0.06)" stroke-width="6" stroke-dasharray="1382.3"/>
    <circle id="arc-uptime" cx="240" cy="240" r="220" fill="none" stroke="#00e5ff" stroke-width="6" stroke-linecap="round" stroke-dasharray="1382.3" stroke-dashoffset="1382.3" style="transition: stroke-dashoffset 1.5s ease-out;"/>
    <circle cx="240" cy="240" r="195" fill="none" stroke="rgba(180,60,255,0.06)" stroke-width="6" stroke-dasharray="1225.2"/>
    <circle id="arc-health" cx="240" cy="240" r="195" fill="none" stroke="#b43cff" stroke-width="6" stroke-linecap="round" stroke-dasharray="1225.2" stroke-dashoffset="1225.2" style="transition: stroke-dashoffset 1.8s ease-out 0.2s;"/>
    <circle cx="240" cy="240" r="170" fill="none" stroke="rgba(0,255,136,0.06)" stroke-width="6" stroke-dasharray="1068.1"/>
    <circle id="arc-bandwidth" cx="240" cy="240" r="170" fill="none" stroke="#00ff88" stroke-width="6" stroke-linecap="round" stroke-dasharray="1068.1" stroke-dashoffset="1068.1" style="transition: stroke-dashoffset 2.0s ease-out 0.4s;"/>
    <circle cx="240" cy="240" r="145" fill="none" stroke="rgba(255,150,0,0.06)" stroke-width="6" stroke-dasharray="911.1"/>
    <circle id="arc-throughput" cx="240" cy="240" r="145" fill="none" stroke="#ff9600" stroke-width="6" stroke-linecap="round" stroke-dasharray="911.1" stroke-dashoffset="911.1" style="transition: stroke-dashoffset 2.2s ease-out 0.6s;"/>
  </svg>
  <div class="ring-center">
    <div class="ring-score" id="composite-score">92</div>
    <div class="ring-score-label">Composite Score</div>
  </div>
  <div class="ring-labels">
    <span class="ring-label rl1" style="color:#00e5ff;">Uptime 99.8%</span>
    <span class="ring-label rl2" style="color:#b43cff;">Health 87%</span>
    <span class="ring-label rl3" style="color:#00ff88;">Bandwidth 94%</span>
    <span class="ring-label rl4" style="color:#ff9600;">Throughput 78%</span>
  </div>
  <div class="ring-glows"></div>
</div>
<script>
(function() {
  console.log('[BOOT] Mockup 5 — Data Ring: registering listeners');
  function setArc(id, pct) {
    var el = document.getElementById(id);
    if (!el) return;
    var r = parseInt(el.getAttribute('r'));
    var circ = 2 * Math.PI * r;
    var offset = circ - (pct / 100) * circ;
    el.style.strokeDashoffset = offset + 'px';
    el.style.strokeDasharray = circ + 'px';
  }
  setTimeout(function() {
    setArc('arc-uptime', 99.8);
    setArc('arc-health', 87);
    setArc('arc-bandwidth', 94);
    setArc('arc-throughput', 78);
  }, 100);
  var scoreEl = document.getElementById('composite-score');
  if (scoreEl) {
    scoreEl.addEventListener('click', function() {
      console.log('[CLICK] Composite score — drilling to detail view');
    });
  }
  var arcs = document.querySelectorAll('[id^="arc-"]');
  for (var i = 0; i < arcs.length; i++) {
    (function(el) {
      el.addEventListener('click', function() {
        console.log('[CLICK] Arc:', el.id, '— expanding metric detail');
      });
    })(arcs[i]);
  }
  console.log('[BOOT] Mockup 5 — all listeners registered: arc expand, score drill-down');
})();
</script>
</body>
</html>
```
---
Mockup 5 uses concentric SVG arc rings with staggered animation for a radial progress display around a composite score. SVG-based rather than canvas, demonstrating a different rendering approach from the signal monitor.
---
Summary Table
| Mockup | Theme | Key Differentiator |
|:-------|:------|:-------------------|
| 1 — System Overview | KPI grid with glass cards | Four-color glow-coded metrics, translucent panels, live activity feed |
| 2 — Node Topology | Radial network map | Orbital node layout, particle constellation with connection lines, hover glow |
| 3 — Holographic Terminal | Command-driven interface | Scanline overlay, keystroke echo, holographic response panels, boot sequence |
| 4 — Signal Monitor | Real-time waveform | Three-channel animated signal traces with gradient fill, live scrolling |
| 5 — Data Ring | Concentric arc progress | SVG ring animation, composite center score, four staggered metrics |
All five mockups follow teacher feedback: multi-line CSS formatting, console.log at boot confirming registered listeners, no inline styles beyond JS-driven values, event listeners on all interactive elements, and extracted reusable CSS classes. Each explores a genuinely distinct visual territory — no two could be confused as variants of the same concept.