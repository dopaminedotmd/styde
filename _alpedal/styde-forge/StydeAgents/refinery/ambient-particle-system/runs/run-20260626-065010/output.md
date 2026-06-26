┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -306,7 +306,12 @@[0m
[38;2;184;134;11m [data-theme="oled"] { --bg: #000; --card: #0a0a10; --border: #1a1a28; --text: #c0c0d0; --dim: #484878; --accent: #6070ff; --green: #20d060; --blue: #5090ff; --xp-bg: #0a0a16; }[0m
[38;2;184;134;11m [data-theme="forest"] { --bg: #0f1410; --card: #182018; --border: #283428; --text: #b8c8b8; --dim: #588058; --accent: #40b860; --green: #40d060; --yellow: #c0b030; --red: #e05040; --blue: #4088e0; --xp-bg: #142018; }[0m
[38;2;184;134;11m *{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;119;20;20m-body{background:var(--bg);color:var(--text);padding:16px;transition:background var(--transition-slow),color var(--transition-slow);min-height:100vh}[0m
[38;2;255;255;255;48;2;19;87;20m+body{background:var(--bg);color:var(--text);padding:16px;transition:background var(--transition-slow),color var(--transition-slow);min-height:100vh;position:relative;z-index:1}[0m
[38;2;255;255;255;48;2;19;87;20m+#particle-canvas{position:fixed;inset:0;z-index:0;pointer-events:none;width:100vw;height:100vh;display:block;opacity:0;transition:opacity 1s ease}[0m
[38;2;255;255;255;48;2;19;87;20m+#particle-canvas.active{opacity:1}[0m
[38;2;255;255;255;48;2;19;87;20m+.particle-toggle{cursor:pointer;display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;border:1px solid var(--border);background:var(--card);color:var(--dim);font-size:9px;text-transform:uppercase;letter-spacing:1px;transition:all var(--transition-fast)}[0m
[38;2;255;255;255;48;2;19;87;20m+.particle-toggle:hover{border-color:var(--accent);color:var(--accent)}[0m
[38;2;255;255;255;48;2;19;87;20m+.particle-toggle.active{background:rgba(80,96,224,.15);border-color:var(--accent);color:var(--accent)}[0m
[38;2;184;134;11m h1{font-size:22px;font-weight:700;color:#d0d0f0;letter-spacing:-.5px}h1 span{color:var(--accent)}[0m
[38;2;184;134;11m .sub{color:var(--dim);font-size:11px;margin-bottom:14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -467,6 +467,7 @@[0m
[38;2;184;134;11m </style>[0m
[38;2;184;134;11m </head>[0m
[38;2;184;134;11m <body>[0m
[38;2;255;255;255;48;2;19;87;20m+<canvas id="particle-canvas"></canvas>[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m <h1>Styde <span>Forge</span> — Command Center v5</h1>[0m
[38;2;184;134;11m <div class="sub">[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -554,6 +554,7 @@[0m
[38;2;184;134;11m         <hr style="border-color:var(--border);margin:4px 0">[0m
[38;2;184;134;11m         <button class="ctrl-btn" style="background:var(--accent);color:#fff" onclick="window.open('/stream')">&#8635; Raw SSE Stream</button>[0m
[38;2;184;134;11m         <button class="ctrl-btn" style="background:var(--dim);color:#fff" onclick="document.querySelector('.btn-dark').click()">Dark Theme</button>[0m
[38;2;255;255;255;48;2;19;87;20m+        <button class="particle-toggle" id="particle-toggle" onclick="toggleParticles()">&#10023; Particles</button>[0m
[38;2;184;134;11m       </div>[0m
[38;2;184;134;11m     </div>[0m
[38;2;184;134;11m   </div>[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -758,6 +758,191 @@[0m
[38;2;184;134;11m   ).join('');[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+/* ═══════════ AMBIENT PARTICLE SYSTEM ═══════════ */[0m
[38;2;255;255;255;48;2;19;87;20m+const PC = document.getElementById('particle-canvas');[0m
[38;2;255;255;255;48;2;19;87;20m+let PCX, PCT;[0m
[38;2;255;255;255;48;2;19;87;20m+let particles = [];[0m
[38;2;255;255;255;48;2;19;87;20m+let prevSpawned = 0;[0m
[38;2;255;255;255;48;2;19;87;20m+let particleEnabled = false;[0m
[38;2;255;255;255;48;2;19;87;20m+const MAX_PARTICLES = 180;[0m
[38;2;255;255;255;48;2;19;87;20m+const PARTICLE_TTL = { ember: 4000, spark: 800, haze: 1200 };[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function initParticleCanvas() {[0m
[38;2;255;255;255;48;2;19;87;20m+  PCX = PC;[0m
[38;2;255;255;255;48;2;19;87;20m+  PCT = PCX.getContext('2d');[0m
[38;2;255;255;255;48;2;19;87;20m+  resizeParticles();[0m
[38;2;255;255;255;48;2;19;87;20m+  window.addEventListener('resize', resizeParticles);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function resizeParticles() {[0m
[38;2;255;255;255;48;2;19;87;20m+  const dpr = window.devicePixelRatio || 1;[0m
[38;2;255;255;255;48;2;19;87;20m+  PCX.width = window.innerWidth * dpr;[0m
[38;2;255;255;255;48;2;19;87;20m+  PCX.height = window.innerHeight * dpr;[0m
[38;2;255;255;255;48;2;19;87;20m+  PCX.style.width = window.innerWidth + 'px';[0m
[38;2;255;255;255;48;2;19;87;20m+  PCX.style.height = window.innerHeight + 'px';[0m
[38;2;255;255;255;48;2;19;87;20m+  PCT.scale(dpr, dpr);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function mkParticle(type, x, y) {[0m
[38;2;255;255;255;48;2;19;87;20m+  const gpuTemp = window._lastGpuTemp || 50;[0m
[38;2;255;255;255;48;2;19;87;20m+  const t = Math.min(Math.max((gpuTemp - 30) / 55, 0), 1);[0m
[38;2;255;255;255;48;2;19;87;20m+  const r = Math.round(40 + t * 200);[0m
[38;2;255;255;255;48;2;19;87;20m+  const g = Math.round(140 - t * 120);[0m
[38;2;255;255;255;48;2;19;87;20m+  const b = Math.round(200 - t * 180);[0m
[38;2;255;255;255;48;2;19;87;20m+  return {[0m
[38;2;255;255;255;48;2;19;87;20m+    type: type || 'ember',[0m
[38;2;255;255;255;48;2;19;87;20m+    x: x || Math.random() * window.innerWidth,[0m
[38;2;255;255;255;48;2;19;87;20m+    y: y || window.innerHeight + 10,[0m
[38;2;255;255;255;48;2;19;87;20m+    vx: (Math.random() - 0.5) * (type === 'spark' ? 3 : 0.5),[0m
[38;2;255;255;255;48;2;19;87;20m+    vy: -(0.3 + Math.random() * (type === 'ember' ? 0.6 : type === 'haze' ? 0.15 : 1.5)),[0m
[38;2;255;255;255;48;2;19;87;20m+    life: (type === 'spark' ? PARTICLE_TTL.spark : type === 'haze' ? PARTICLE_TTL.haze : PARTICLE_TTL.ember) + Math.random() * 500,[0m
[38;2;255;255;255;48;2;19;87;20m+    maxLife: type === 'spark' ? PARTICLE_TTL.spark + 500 : type === 'haze' ? PARTICLE_TTL.haze + 500 : PARTICLE_TTL.ember + 500,[0m
[38;2;255;255;255;48;2;19;87;20m+    r: r, g: g, b: b,[0m
[38;2;255;255;255;48;2;19;87;20m+    size: type === 'ember' ? 1.5 + Math.random() * 2 : type === 'spark' ? 2 + Math.random() * 3 : 4 + Math.random() * 6,[0m
[38;2;255;255;255;48;2;19;87;20m+    alpha: type === 'haze' ? 0.08 + Math.random() * 0.08 : 0.5 + Math.random() * 0.5,[0m
[38;2;255;255;255;48;2;19;87;20m+    drift: Math.random() * 0.3,[0m
[38;2;255;255;255;48;2;19;87;20m+    wobble: Math.random() * Math.PI * 2,[0m
[38;2;255;255;255;48;2;19;87;20m+    wobbleSpeed: 0.02 + Math.random() * 0.03,[0m
[38;2;255;255;255;48;2;19;87;20m+  };[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function emitSparks(count, x, y) {[0m
[38;2;255;255;255;48;2;19;87;20m+  for (let i = 0; i < count && particles.length < MAX_PARTICLES; i++) {[0m
[38;2;255;255;255;48;2;19;87;20m+    const sp = mkParticle('spark', x, y);[0m
[38;2;255;255;255;48;2;19;87;20m+    sp.vx = (Math.random() - 0.5) * 6;[0m
[38;2;255;255;255;48;2;19;87;20m+    sp.vy = -(1 + Math.random() * 3);[0m
[38;2;255;255;255;48;2;19;87;20m+    particles.push(sp);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function burstPromote() {[0m
[38;2;255;255;255;48;2;19;87;20m+  const cx = window.innerWidth * 0.5;[0m
[38;2;255;255;255;48;2;19;87;20m+  const cy = window.innerHeight * 0.4;[0m
[38;2;255;255;255;48;2;19;87;20m+  emitSparks(30, cx, cy);[0m
[38;2;255;255;255;48;2;19;87;20m+  for (let i = 0; i < 12; i++) {[0m
[38;2;255;255;255;48;2;19;87;20m+    const h = mkParticle('haze', cx, cy);[0m
[38;2;255;255;255;48;2;19;87;20m+    h.vx = Math.cos(i * Math.PI / 6) * 0.8;[0m
[38;2;255;255;255;48;2;19;87;20m+    h.vy = -0.3 - Math.random() * 0.3;[0m
[38;2;255;255;255;48;2;19;87;20m+    h.r = 200; h.g = 200; h.b = 255;[0m
[38;2;255;255;255;48;2;19;87;20m+    particles.push(h);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  // also spawn ember ring[0m
[38;2;255;255;255;48;2;19;87;20m+  for (let i = 0; i < 8; i++) {[0m
[38;2;255;255;255;48;2;19;87;20m+    const e = mkParticle('ember', cx + Math.cos(i * Math.PI / 4) * 40, cy + Math.sin(i * Math.PI / 4) * 40);[0m
[38;2;255;255;255;48;2;19;87;20m+    e.vy = -(0.8 + Math.random() * 0.6);[0m
[38;2;255;255;255;48;2;19;87;20m+    e.vx = Math.cos(i * Math.PI / 4) * 0.3;[0m
[38;2;255;255;255;48;2;19;87;20m+    particles.push(e);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;139;134;130m… omitted 113 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -666,6 +666,8 @@[0m
[38;2;184;134;11m evtSource.onmessage=function(event){[0m
[38;2;184;134;11m   const d=JSON.parse(event.data);[0m
[38;2;184;134;11m   agentData=d.agents||[];[0m
[38;2;255;255;255;48;2;19;87;20m+  window._lastSpawned = d.spawned;[0m
[38;2;255;255;255;48;2;19;87;20m+  window._lastGpuTemp = (d.gpus && d.gpus.length) ? d.gpus[0].temp : 50;[0m
[38;2;184;134;11m   document.getElementById('clock').textContent=d.ts;[0m
[38;2;184;134;11m   document.getElementById('hw').textContent=d.hardware;[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Core\dashboard.py → b/D:\styde\_alpedal\styde-forge\Core\dashboard.py[0m
[38;2;139;134;130m@@ -687,7 +687,7 @@[0m
[38;2;184;134;11m   renderEngineList(eng.processes||[]);[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m   // Toasts[0m
[38;2;255;255;255;48;2;119;20;20m-  if(d.production>prevProduction&&prevProduction>0)addToast('AGENT PROMOTED TO PRODUCTION');[0m
[38;2;255;255;255;48;2;19;87;20m+  if(d.production>prevProduction&&prevProduction>0){addToast('AGENT PROMOTED TO PRODUCTION');if(typeof burstPromote==='function')burstPromote();}[0m
[38;2;184;134;11m   if(fs.status==='crashed')addToast('FORGE CRASHED','toast-err');[0m
[38;2;184;134;11m   prevProduction=d.production;[0m
[38;2;184;134;11m [0m
All 18 particle-related references found. Implementation complete. Here is the summary of what was added:
AMBIENT PARTICLE SYSTEM — Styde Forge Dashboard v5
Patches applied to Core/dashboard.py:
CSS (2 additions):
  - `#particle-canvas`: fixed full-viewport canvas behind all panels, z-index 0, pointer-events none, opacity transition
  - `.particle-toggle`: toggle button style matching Control panel theme
HTML (2 additions):
  - `<canvas id="particle-canvas">` right after `<body>`
  - Particles toggle button in Control tab > Quick Actions section
JavaScript (~230 lines):
  - Three particle types:
    ember — small glowing dots that rise slowly from bottom, radial gradient glow
    spark — fast bright streaks emitted in bursts, leave short trails
    haze — large soft translucent blobs with slow horizontal drift, mimics heat distortion
  - Data reactivity:
    GPU temp (from nvidia-smi via SSE) drives particle color ramp: cool blue (30 C) -> amber (65 C) -> hot red (85 C+)
    total_agents_spawned drives ambient ember spawn rate — more spawns = more particles
    production promotion triggers burstPromote(): 30 sparks + 12 haze ring + 8 ember ring at screen center
  - Performance: max 180 particles, requestAnimationFrame with frame delta throttling, HiDPI canvas with `devicePixelRatio`
  - Toggle via localStorage (forge-particles), off by default on mobile (userAgent) and unplugged battery (getBattery API)
SSE wiring (3 edits):
  - `window._lastSpawned` updated each SSE tick
  - `window._lastGpuTemp` extracted from first GPU's temp sensor
  - `burstPromote()` called on production promotion alongside existing toast
Restart the dashboard to see it: particles start in the background, toggleable from Control > Quick Actions > Particles.