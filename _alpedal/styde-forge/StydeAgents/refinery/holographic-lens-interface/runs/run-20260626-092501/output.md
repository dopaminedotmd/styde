```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Holographic Lens Interface</title>
<style>
*,*::before,*::after{margin:0;padding:0;border:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#0a0a12;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;color:#e0e0f0}
/* ===== DEPTH CONTAINER ===== */
.depth-stage{width:100%;height:100vh;perspective:1200px;overflow:hidden;position:relative}
.depth-scene{width:100%;height:100%;transform-style:preserve-3d;position:relative}
/* ===== LAYER BASE ===== */
.layer{position:absolute;top:0;left:0;width:100%;height:100%;transform-style:preserve-3d;will-change:transform;pointer-events:none;backface-visibility:hidden}
.layer-foreground{transform:translateZ(80px);z-index:30;pointer-events:auto}
.layer-midground{transform:translateZ(20px);z-index:20}
.layer-background{transform:translateZ(-60px);z-index:10}
/* ===== GLASS PANELS ===== */
.glass-panel{background:rgba(20,22,40,0.35);border:1px solid rgba(120,140,255,0.15);border-radius:16px;padding:24px;position:absolute}
.glass-panel-1{top:6%;left:5%;width:28%;height:28%;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.glass-panel-2{top:8%;right:5%;width:22%;height:18%;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.glass-panel-3{bottom:8%;left:5%;width:20%;height:22%;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.glass-panel-4{bottom:10%;right:5%;width:30%;height:20%;backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px)}
.glass-panel-5{top:38%;left:32%;width:36%;height:24%;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
/* ===== CHROMATIC ABERRATION ===== */
.chromatic{position:relative;overflow:hidden;transition:transform 0.3s cubic-bezier(0.23,1,0.32,1)}
.chromatic::before,.chromatic::after{content:'';position:absolute;top:0;left:0;width:100%;height:100%;border-radius:inherit;pointer-events:none;opacity:0;transition:opacity 0.3s ease;mix-blend-mode:screen}
.chromatic::before{background:rgba(255,50,50,0.08);transform:translate(2px,0)}
.chromatic::after{background:rgba(50,100,255,0.08);transform:translate(-2px,0)}
.chromatic:hover::before,.chromatic:focus-within::before{opacity:1}
.chromatic:hover::after,.chromatic:focus-within::after{opacity:1}
.chromatic:hover{transform:scale(1.02)}
/* ===== PANEL INNER CONTENT ===== */
.panel-title{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:rgba(140,180,255,0.6);margin-bottom:12px;font-weight:500}
.panel-value{font-size:32px;font-weight:300;color:#fff;letter-spacing:-0.5px;margin-bottom:4px}
.panel-label{font-size:13px;color:rgba(200,210,255,0.5)}
.stat-row{display:flex;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid rgba(120,140,255,0.08)}
.stat-item{text-align:center}
.stat-num{font-size:18px;color:#fff;font-weight:400}
.stat-desc{font-size:10px;color:rgba(200,210,255,0.4);text-transform:uppercase;letter-spacing:1px;margin-top:2px}
/* small data bar */
.data-bar-wrap{height:4px;background:rgba(120,140,255,0.1);border-radius:2px;margin-top:8px;overflow:hidden}
.data-bar-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#6c7cff,#a78bfa);width:0%;transition:width 1.2s cubic-bezier(0.23,1,0.32,1)}
/* ===== MIDGROUND CHART AREA ===== */
.chart-container{position:absolute;top:28%;left:36%;width:50%;height:38%;pointer-events:none}
.chart-grid{position:absolute;bottom:0;left:0;width:100%;height:100%;display:flex;align-items:flex-end;gap:6px;padding:20px 12px 12px}
.chart-bar{flex:1;border-radius:3px 3px 0 0;min-height:4px;background:linear-gradient(180deg,rgba(120,140,255,0.5),rgba(167,139,250,0.2));transition:height 1.5s cubic-bezier(0.23,1,0.32,1);position:relative}
.chart-bar:nth-child(odd){background:linear-gradient(180deg,rgba(100,200,255,0.4),rgba(100,200,255,0.1))}
.chart-bar-label{position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);font-size:8px;color:rgba(200,210,255,0.3);white-space:nowrap}
/* ===== FOREGROUND CONTROLS ===== */
.control-bar{position:absolute;bottom:36px;left:50%;transform:translateX(-50%);display:flex;gap:12px;z-index:40;pointer-events:auto;padding:12px 20px;background:rgba(20,22,40,0.5);border:1px solid rgba(120,140,255,0.12);border-radius:40px;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px)}
.control-btn{background:rgba(120,140,255,0.1);border:1px solid rgba(120,140,255,0.15);color:rgba(200,210,255,0.8);padding:8px 20px;border-radius:24px;font-size:13px;cursor:pointer;transition:all 0.25s ease;font-family:inherit;letter-spacing:0.3px}
.control-btn:hover{background:rgba(120,140,255,0.2);border-color:rgba(120,140,255,0.3);color:#fff;box-shadow:0 0 20px rgba(120,140,255,0.1)}
/* ===== AMBIENT GLOW BACKGROUND ===== */
.ambient-glow{position:absolute;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none;overflow:hidden}
.glow-orb{position:absolute;border-radius:50%;opacity:0;animation:glowPulse 6s ease-in-out infinite}
.glow-orb:nth-child(1){width:50vw;height:50vw;top:-10%;left:-10%;background:radial-gradient(circle,rgba(80,100,255,0.12),transparent 70%);animation-delay:0s}
.glow-orb:nth-child(2){width:40vw;height:40vw;bottom:-5%;right:-5%;background:radial-gradient(circle,rgba(167,139,250,0.1),transparent 70%);animation-delay:2s}
.glow-orb:nth-child(3){width:30vw;height:30vw;top:40%;left:45%;background:radial-gradient(circle,rgba(100,200,255,0.08),transparent 70%);animation-delay:4s}
.glow-orb:nth-child(4){width:60vw;height:60vw;top:20%;left:20%;background:radial-gradient(circle,rgba(60,40,120,0.06),transparent 70%);animation-delay:1s}
@keyframes glowPulse{
  0%,100%{opacity:0;transform:scale(0.8)}
  50%{opacity:1;transform:scale(1.2)}
}
/* ===== SVG REFRACTION OVERLAY ===== */
.refraction-overlay{position:fixed;top:0;left:0;width:100%;height:100%;z-index:50;pointer-events:none;filter:url(#lens-distortion);opacity:0.3;mix-blend-mode:overlay}
/* ===== STATUS INDICATOR ===== */
.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:6px;background:#4ade80;box-shadow:0 0 8px rgba(74,222,128,0.4);animation:statusBlink 2s ease-in-out infinite}
@keyframes statusBlink{0%,100%{opacity:1}50%{opacity:0.4}}
/* ===== SCROLLBAR HIDE ===== */
body::-webkit-scrollbar{display:none}
</style>
</head>
<body>
<svg width=0 height=0 style=position:absolute>
  <defs>
    <filter id=lens-distortion>
      <feTurbulence type=fractalNoise baseFrequency=0.008 numOctaves=2 seed=3 result=noise/>
      <feDisplacementMap in=SourceGraphic in2=noise scale=6 xChannelSelector=R yChannelSelector=G/>
    </filter>
    <filter id=glass-blur>
      <feGaussianBlur stdDeviation=4/>
    </filter>
  </defs>
</svg>
<div class=depth-stage id=depthStage>
  <div class=depth-scene id=depthScene>
    <!-- BACKGROUND LAYER -->
    <div class=layer layer-background id=layerBg>
      <div class=ambient-glow>
        <div class=glow-orb></div>
        <div class=glow-orb></div>
        <div class=glow-orb></div>
        <div class=glow-orb></div>
      </div>
    </div>
    <!-- MIDGROUND LAYER -->
    <div class=layer layer-midground id=layerMid>
      <div class="glass-panel glass-panel-5 chromatic" style="top:34%;left:28%;width:44%;height:32%">
        <div class=panel-title>Network Throughput</div>
        <div style=display:flex;gap:24px;margin-top:4px>
          <div><div class=panel-value id=throughputVal>2.4</div><div class=panel-label>Gbps avg</div></div>
          <div><div class=panel-value id=latencyVal>12</div><div class=panel-label>ms latency</div></div>
          <div><div class=panel-value id=packetVal>99.8</div><div class=panel-label>% deliver</div></div>
        </div>
        <div class=stat-row>
          <div class=stat-item><div class=stat-num>847</div><div class=stat-desc>Act Conns</div></div>
          <div class=stat-item><div class=stat-num>1.2k</div><div class=stat-desc>Req/s</div></div>
          <div class=stat-item><div class=stat-num>0.3</div><div class=stat-desc>Err%</div></div>
        </div>
      </div>
      <div class=chart-container>
        <div class=panel-title style="position:absolute;top:4px;left:12px;z-index:2">Bandwidth Usage</div>
        <div class=chart-grid id=chartGrid></div>
      </div>
    </div>
    <!-- FOREGROUND LAYER -->
    <div class=layer layer-foreground id=layerFg>
      <div class="glass-panel glass-panel-1 chromatic">
        <div class=panel-title><span class=status-dot></span>System Status</div>
        <div class=panel-value id=statusCpu>47</div>
        <div class=panel-label>% CPU utilization</div>
        <div class=data-bar-wrap><div class=data-bar-fill id=cpuBar style=width:47%></div></div>
        <div style=margin-top:16px>
          <div style=display:flex;justify-content:space-between>
            <span class=panel-label>Memory</span>
            <span class=panel-value style=font-size:16px id=memVal>12.4 GB</span>
          </div>
          <div class=data-bar-wrap><div class=data-bar-fill id=memBar style=width:62%></div></div>
        </div>
      </div>
      <div class="glass-panel glass-panel-2 chromatic">
        <div class=panel-title>Active Alerts</div>
        <div class=panel-value style=font-size:28px>3</div>
        <div class=panel-label>2 warnings · 1 info</div>
        <div style=margin-top:12px;font-size:12px;color:rgba(200,210,255,0.5)>
          <div style=display:flex;gap:8px;align-items:center;margin-bottom:4px>
            <span style=color:#fbbf24>●</span> Latency spike (152ms)
          </div>
          <div style=display:flex;gap:8px;align-items:center;margin-bottom:4px>
            <span style=color:#fbbf24>●</span> Packet loss &gt;1%
          </div>
          <div style=display:flex;gap:8px;align-items:center>
            <span style=color:#60a5fa>●</span> Config drift detected
          </div>
        </div>
      </div>
      <div class="glass-panel glass-panel-3 chromatic">
        <div class=panel-title>Quick Actions</div>
        <div style=display:flex;flex-direction:column;gap:8px;margin-top:8px>
          <button class=control-btn onclick=\"handleAction('restart')\" style=width:100%>Restart Service</button>
          <button class=control-btn onclick=\"handleAction('flush')\" style=width:100%>Flush Cache</button>
          <button class=control-btn onclick=\"handleAction('diag')\" style=width:100%>Run Diagnostics</button>
        </div>
      </div>
      <div class="glass-panel glass-panel-4 chromatic">
        <div class=panel-title>Session Timeline</div>
        <div style=display:flex;flex-direction:column;gap:6px;margin-top:8px>
          <div style=display:flex;justify-content:space-between;font-size:12px>
            <span style=color:rgba(200,210,255,0.5)>14:23:12</span>
            <span style=color:rgba(200,210,255,0.7)>Auth success</span>
          </div>
          <div style=display:flex;justify-content:space-between;font-size:12px>
            <span style=color:rgba(200,210,255,0.5)>14:23:45</span>
            <span style=color:rgba(200,210,255,0.7)>API key rotated</span>
          </div>
          <div style=display:flex;justify-content:space-between;font-size:12px>
            <span style=color:rgba(200,210,255,0.5)>14:24:01</span>
            <span style=color:rgba(200,210,255,0.7)>Config sync OK</span>
          </div>
        </div>
      </div>
      <div class=control-bar>
        <button class=control-btn data-action=refresh>Refresh</button>
        <button class=control-btn data-action=reset>Reset View</button>
        <button class=control-btn data-action=theme>Toggle Theme</button>
      </div>
    </div>
  </div>
</div>
<div class=refraction-overlay></div>
<script>
// ===== ANIMATION TIMING UTILITY =====
const AnimTiming = (() => {
  const queue = { read: [], write: [] };
  let scheduled = false;
  const frame = () => {
    scheduled = false;
    const reads = queue.read.splice(0);
    const writes = queue.write.splice(0);
    const readResults = reads.map(fn => fn());
    writes.forEach(fn => fn(readResults));
  };
  const schedule = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(frame); } };
  return {
    read(fn) { queue.read.push(fn); schedule(); },
    write(fn) { queue.write.push(fn); schedule(); },
    throttle(fn, minInterval) {
      let lastCall = 0, pending = false, lastArgs;
      const invoke = () => { lastCall = performance.now(); pending = false; fn(...lastArgs); };
      return (...args) => {
        lastArgs = args;
        const now = performance.now();
        if (now - lastCall >= minInterval) { invoke(); }
        else if (!pending) { pending = true; requestAnimationFrame(() => invoke()); }
      };
    },
    debounce(fn, delay) {
      let timer;
      return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
    }
  };
})();
// ===== PARALLAX CONTROLLER =====
const ParallaxCtrl = (() => {
  const layers = {};
  let isEnabled = true;
  const onPointer = AnimTiming.throttle((x, y) => {
    if (!isEnabled) return;
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    const dx = (x - cx) / cx;
    const dy = (y - cy) / cy;
    AnimTiming.read(() => {
      const entries = Object.entries(layers);
      const transforms = entries.map(([id, sens]) => {
        const rotX = dy * sens * 6;
        const rotY = dx * sens * 8;
        const transZ = sens * 20;
        return { id, transform: `rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) translateZ(${transZ.toFixed(1)}px)` };
      });
      return transforms;
    });
    AnimTiming.write((transforms) => {
      if (!transforms) return;
      transforms.forEach(({ id, transform }) => {
        const el = document.getElementById(id);
        if (el) el.style.transform = transform;
      });
    });
  }, 16);
  return {
    register(id, sensitivity) { layers[id] = sensitivity; },
    unregister(id) { delete layers[id]; },
    handlePointer(x, y) { onPointer(x, y); },
    setEnabled(v) { isEnabled = v; },
    reset() {
      isEnabled = true;
      Object.keys(layers).forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.transform = '';
      });
    }
  };
})();
// ===== CHART INIT =====
const ChartCtrl = (() => {
  const LABELS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const data = [34,52,41,63,58,72,68];
  const render = () => {
    const grid = document.getElementById('chartGrid');
    if (!grid) return;
    grid.innerHTML = '';
    const max = Math.max(...data);
    data.forEach((v, i) => {
      const bar = document.createElement('div');
      bar.className = 'chart-bar';
      bar.style.height = '0%';
      bar.dataset.val = v;
      const label = document.createElement('div');
      label.className = 'chart-bar-label';
      label.textContent = LABELS[i];
      bar.appendChild(label);
      grid.appendChild(bar);
    });
    AnimTiming.read(() => {
      const bars = grid.querySelectorAll('.chart-bar');
      return Array.from(bars).map(b => { return { el: b, pct: (parseInt(b.dataset.val) / max * 100).toFixed(1) }; });
    });
    AnimTiming.write((barData) => {
      if (!barData) return;
      barData.forEach(({ el, pct }) => { el.style.height = pct + '%'; });
    });
  };
  return { render, data };
})();
// ===== ACTIONS =====
window.handleAction = (action) => {
  const msgs = {
    restart: 'Service restart initiated...',
    flush: 'Cache flushed successfully',
    diag: 'Diagnostics running...'
  };
  const msg = msgs[action] || 'Action executed';
  console.log('[ACTION]', msg);
  const btn = document.querySelector(`button[onclick*="${action}"]`);
  if (btn) { btn.style.background = 'rgba(74,222,128,0.15)'; setTimeout(() => { btn.style.background = ''; }, 600); }
};
// ===== CONTROL BAR HANDLERS =====
const handleControlAction = (action) => {
  switch(action) {
    case 'refresh':
      ChartCtrl.render();
      break;
    case 'reset':
      ParallaxCtrl.reset();
      break;
    case 'theme':
      document.body.style.filter = document.body.style.filter === 'invert(0.85) hue-rotate(180deg)' ? '' : 'invert(0.85) hue-rotate(180deg)';
      break;
  }
};
// ===== SINGLE MOUSEMOVE / POINTER LISTENER =====
const onPointerMove = (e) => {
  const x = e.clientX ?? e.touches?.[0]?.clientX ?? 0;
  const y = e.clientY ?? e.touches?.[0]?.clientY ?? 0;
  ParallaxCtrl.handlePointer(x, y);
};
// ===== REGISTER EVERYTHING =====
(() => {
  ParallaxCtrl.register('layerBg', 0.3);
  ParallaxCtrl.register('layerMid', 0.55);
  ParallaxCtrl.register('layerFg', 0.9);
  document.addEventListener('mousemove', onPointerMove, { passive: true });
  // control bar delegation
  document.querySelector('.control-bar')?.addEventListener('click', (e) => {
    const btn = e.target.closest('.control-btn');
    if (!btn) return;
    const action = btn.dataset.action;
    if (action) handleControlAction(action);
  });
  ChartCtrl.render();
  // animate data bars after paint
  AnimTiming.read(() => null);
  AnimTiming.write(() => {
    document.querySelectorAll('.data-bar-fill').forEach(el => {
      const w = el.style.width;
      el.style.width = '0%';
      requestAnimationFrame(() => { el.style.width = w; });
    });
  });
})();
</script>
</body>
</html>
```