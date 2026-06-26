```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Holographic Lens Interface v1</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root {
  --depth-bg: 0.6;
  --depth-mid: 0.3;
  --depth-fg: 0.0;
  --blur-bg: 2px;
  --blur-mid: 6px;
  --blur-fg: 10px;
  --glass-bg: rgba(8,12,28,0.55);
  --glass-mid: rgba(12,18,42,0.45);
  --glass-fg: rgba(16,24,56,0.35);
  --border-glass: rgba(120,160,255,0.12);
  --accent: #6c8cff;
  --accent2: #ff6cb8;
  --accent3: #6cffd8;
  --glow-1: #4a6cf7;
  --glow-2: #b84aff;
  --glow-3: #00d4ff;
}
html,body{height:100%;overflow:hidden;font-family:'Segoe UI',system-ui,-apple-system,sans-serif}
body{background:#040812;display:flex;align-items:center;justify-content:center;perspective:1200px}
/* ---- SVG FILTERS (refraction/lens) ---- */
.lens-defs{position:absolute;width:0;height:0;overflow:hidden}
/* ---- SCENE ---- */
.scene{width:100vw;height:100vh;position:relative;transform-style:preserve-3d;overflow:hidden}
.layer{position:absolute;inset:0;transform-style:preserve-3d;will-change:transform;pointer-events:none}
.layer-bg{z-index:1}
.layer-mid{z-index:2}
.layer-fg{z-index:3;pointer-events:auto}
/* ---- BACKGROUND LAYER ---- */
.bg-grid{position:absolute;inset:0;background-image:
  linear-gradient(rgba(74,108,247,0.03) 1px,transparent 1px),
  linear-gradient(90deg,rgba(74,108,247,0.03) 1px,transparent 1px);
  background-size:60px 60px}
.ambient-glow{position:absolute;inset:0;overflow:hidden}
.ambient-glow::before,.ambient-glow::after{content:'';position:absolute;border-radius:50%;filter:blur(80px);animation:glowPulse 8s ease-in-out infinite alternate}
.ambient-glow::before{width:600px;height:600px;top:10%;left:15%;background:radial-gradient(circle,rgba(74,108,247,0.25),transparent 70%);animation-delay:0s}
.ambient-glow::after{width:500px;height:500px;bottom:5%;right:10%;background:radial-gradient(circle,rgba(184,74,255,0.2),transparent 70%);animation-delay:-3s}
.glow-orb-3{position:absolute;width:400px;height:400px;top:40%;left:55%;background:radial-gradient(circle,rgba(0,212,255,0.15),transparent 70%);border-radius:50%;filter:blur(60px);animation:glowPulse 6s ease-in-out infinite alternate;animation-delay:-1.5s}
@keyframes glowPulse{0%{opacity:0.4;transform:scale(0.95) translate(0,0)}100%{opacity:0.9;transform:scale(1.15) translate(20px,-20px)}}
/* ---- MIDGROUND LAYER ---- */
.dashboard{position:absolute;inset:6%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr 1fr;gap:16px;padding:0}
.dboard-header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:8px 4px 4px 4px}
.dboard-header h1{font-size:18px;font-weight:500;color:rgba(255,255,255,0.7);letter-spacing:3px;text-transform:uppercase;text-shadow:0 0 20px rgba(74,108,247,0.3)}
.dboard-header .status{display:flex;gap:16px;align-items:center}
.dboard-header .status span{font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:1px}
.dboard-header .dot{width:6px;height:6px;border-radius:50%;background:var(--accent3);box-shadow:0 0 8px var(--accent3);animation:dotPulse 2s ease-in-out infinite}
@keyframes dotPulse{0%,100%{opacity:0.4}50%{opacity:1}}
.panel{position:relative;backdrop-filter:blur(var(--blur-mid));-webkit-backdrop-filter:blur(var(--blur-mid));background:var(--glass-mid);border:1px solid var(--border-glass);border-radius:12px;padding:16px;overflow:hidden;transition:all 0.4s cubic-bezier(0.2,0.9,0.3,1.1)}
.panel::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.03) 0%,transparent 50%,rgba(74,108,247,0.03) 100%);pointer-events:none;border-radius:12px}
.panel:hover{border-color:rgba(120,160,255,0.3);box-shadow:0 0 30px rgba(74,108,247,0.08),inset 0 0 30px rgba(74,108,247,0.03)}
.panel-title{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.25);margin-bottom:12px}
/* ---- CHART / VISUALS ---- */
.chart-area{display:flex;align-items:flex-end;gap:6px;height:100px;padding:0 4px}
.chart-bar{flex:1;border-radius:3px 3px 0 0;background:linear-gradient(180deg,rgba(74,108,247,0.6),rgba(74,108,247,0.2));min-height:12px;transition:all 0.6s cubic-bezier(0.2,0.9,0.4,1);position:relative;overflow:hidden}
.chart-bar::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,0.15),transparent);opacity:0;transition:opacity 0.3s}
.chart-bar:hover::after{opacity:1}
.chart-bar:nth-child(3n+1){background:linear-gradient(180deg,rgba(74,108,247,0.7),rgba(74,108,247,0.25))}
.chart-bar:nth-child(3n+2){background:linear-gradient(180deg,rgba(184,74,255,0.6),rgba(184,74,255,0.2))}
.chart-bar:nth-child(3n+3){background:linear-gradient(180deg,rgba(0,212,255,0.6),rgba(0,212,255,0.2))}
.metric-row{display:flex;justify-content:space-between;margin-bottom:6px}
.metric-label{font-size:11px;color:rgba(255,255,255,0.3)}
.metric-value{font-size:14px;font-weight:600;color:rgba(255,255,255,0.7);font-variant-numeric:tabular-nums}
.metric-value.accent{color:var(--accent)}
.metric-value.accent2{color:var(--accent2)}
.metric-value.accent3{color:var(--accent3)}
.metric-delta{font-size:10px;margin-left:4px}
.metric-delta.pos{color:#6cff88}
.metric-delta.neg{color:#ff6c6c}
/* ---- FOREGROUND LAYER ---- */
.fg-content{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center}
.fg-content .ctrl{padding:10px 20px;border-radius:8px;backdrop-filter:blur(var(--blur-fg));-webkit-backdrop-filter:blur(var(--blur-fg));background:var(--glass-fg);border:1px solid var(--border-glass);color:rgba(255,255,255,0.6);font-size:12px;letter-spacing:1px;cursor:pointer;transition:all 0.3s cubic-bezier(0.2,0.9,0.4,1);position:relative;overflow:hidden}
.fg-content .ctrl::before{content:'';position:absolute;inset:0;border-radius:8px;opacity:0;transition:opacity 0.3s;background:linear-gradient(135deg,rgba(255,255,255,0.05),transparent)}
.fg-content .ctrl:hover{color:rgba(255,255,255,0.9);border-color:rgba(120,160,255,0.4);transform:translateY(-1px);box-shadow:0 4px 20px rgba(74,108,247,0.15)}
.fg-content .ctrl:hover::before{opacity:1}
/* CHROMATIC ABERRATION on hover */
.panel:hover .panel-title,
.fg-content .ctrl:hover,
.metric-value.accent:hover{animation:chromaticShift 0.6s ease-out}
@keyframes chromaticShift{
  0%{text-shadow:-1px 0 rgba(255,0,80,0.5),1px 0 rgba(0,200,255,0.5)}
  30%{text-shadow:-2px 0 rgba(255,0,80,0.4),2px 0 rgba(0,200,255,0.4)}
  60%{text-shadow:-0.5px 0 rgba(255,0,80,0.3),0.5px 0 rgba(0,200,255,0.3)}
  100%{text-shadow:0 0 transparent}
}
/* REFRACTION: overlapping panels get lens distortion */
.panel + .panel{margin-top:0}
.panel:nth-child(2){filter:url(#lens-distort)}
.dboard-header + .panel{filter:url(#lens-distort)}
.panel:nth-child(3){filter:url(#lens-distort)}
/* ---- RESPONSIVE ---- */
@media(max-width:768px){
  .dashboard{inset:3%;grid-template-columns:1fr;gap:10px}
  .panel{padding:12px}
  .fg-content{bottom:16px;flex-wrap:wrap;justify-content:center}
}
/* DATA RING */
.data-ring{display:flex;align-items:center;justify-content:center;gap:24px;height:100%}
.ring-svg{width:80px;height:80px;transform:rotate(-90deg)}
.ring-bg{fill:none;stroke:rgba(255,255,255,0.04);stroke-width:4}
.ring-fg{fill:none;stroke-width:4;stroke-linecap:round;transition:stroke-dashoffset 1s ease}
.ring-label{font-size:10px;color:rgba(255,255,255,0.25);text-align:center;margin-top:4px}
.ring-value{font-size:18px;font-weight:600;color:rgba(255,255,255,0.7);text-align:center}
/* NOISE TEXTURE */
.scene::after{content:'';position:absolute;inset:0;z-index:10;pointer-events:none;opacity:0.015;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");background-size:200px 200px;mix-blend-mode:overlay}
</style>
</head>
<body>
<!-- SVG filters for refraction -->
<svg class=lens-defs aria-hidden=true>
  <filter id=lens-distort>
    <feTurbulence type=fractalNoise baseFrequency=0.01 numOctaves=2 result=noise seed=3/>
    <feDisplacementMap in=SourceGraphic in2=noise scale=3 xChannelSelector=R yChannelSelector=B/>
  </filter>
  <filter id=glow-filter>
    <feGaussianBlur stdDeviation=6 result=blur/>
    <feComposite in=SourceGraphic in2=blur operator=over/>
  </filter>
</svg>
<div class=scene id=scene>
  <!-- BACKGROUND LAYER -->
  <div class=layer layer-bg id=layerBg>
    <div class=bg-grid></div>
    <div class=ambient-glow>
      <div class=glow-orb-3></div>
    </div>
  </div>
  <!-- MIDGROUND LAYER -->
  <div class=layer layer-mid id=layerMid>
    <div class=dashboard id=dashboard>
      <!-- HEADER -->
      <div class="panel dboard-header" style="backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);background:rgba(8,12,28,0.3);border:none;padding:4px 8px">
        <h1>Holographic Lens</h1>
        <div class=status>
          <span>SYSTEM NOMINAL</span>
          <div class=dot></div>
          <span>v1.0</span>
        </div>
      </div>
      <!-- CHART PANEL -->
      <div class=panel>
        <div class=panel-title>Throughput / ops</div>
        <div class=chart-area id=chartArea></div>
      </div>
      <!-- METRICS PANEL -->
      <div class=panel>
        <div class=panel-title>System Metrics</div>
        <div class=metric-row>
          <span class=metric-label>Latency</span>
          <span><span class=metric-value accent2>12.4</span><span class=metric-delta pos>+2.1%</span></span>
        </div>
        <div class=metric-row>
          <span class=metric-label>Memory</span>
          <span><span class=metric-value accent>7.8</span><span class=metric-delta neg>-0.3%</span></span>
        </div>
        <div class=metric-row>
          <span class=metric-label>Cache Hit</span>
          <span><span class=metric-value accent3>94.2</span><span class=metric-delta pos>+0.7%</span></span>
        </div>
        <div class=metric-row>
          <span class=metric-label>Error Rate</span>
          <span><span class=metric-value style=color:#ff6c6c>0.03</span><span class=metric-delta neg>-0.01%</span></span>
        </div>
      </div>
      <!-- DATA RING PANEL -->
      <div class=panel>
        <div class=panel-title>Load Distribution</div>
        <div class=data-ring id=dataRing></div>
      </div>
      <!-- LOG PANEL -->
      <div class=panel style=grid-column:1/-1>
        <div class=panel-title>Event Log / Recent</div>
        <div style=font-size:11px;color:rgba(255,255,255,0.25);font-family:monospace;line-height:1.8>
          <div style=color:rgba(74,108,247,0.5)>[06:11:42]  lens.render  layer depth calibrated</div>
          <div style=color:rgba(0,212,255,0.4)>[06:11:43]  parallax.track  sensitivity set 0.4/0.2/0.1</div>
          <div style=color:rgba(184,74,255,0.4)>[06:11:44]  glass.blur  bg:2px mid:6px fg:10px</div>
          <div style=color:rgba(74,108,247,0.35)>[06:11:45]  chromatic.ready  rgb-split enabled</div>
          <div style=color:rgba(0,212,255,0.3)>[06:11:46]  glow.inject  ambient orbs active</div>
        </div>
      </div>
    </div>
  </div>
  <!-- FOREGROUND LAYER -->
  <div class=layer layer-fg id=layerFg>
    <div class=fg-content>
      <div class=ctrl>DEPTH</div>
      <div class=ctrl>LENS</div>
      <div class=ctrl>REFRACT</div>
      <div class=ctrl>GLASS</div>
      <div class=ctrl>CHROMA</div>
    </div>
  </div>
</div>
<script>
(function(){
  'use strict';
  // ---- BUILD CHART BARS ----
  const chart = document.getElementById('chartArea');
  const barCount = 24;
  for(let i=0;i<barCount;i++){
    const bar = document.createElement('div');
    bar.className = 'chart-bar';
    bar.style.height = (12 + Math.random() * 80) + 'px';
    chart.appendChild(bar);
  }
  // ---- BUILD DATA RINGS ----
  const ringContainer = document.getElementById('dataRing');
  const ringData = [
    { label: 'CPU', value: 0.42, color: '#6c8cff' },
    { label: 'GPU', value: 0.73, color: '#b84aff' },
    { label: 'IO',  value: 0.21, color: '#00d4ff' }
  ];
  const circumference = 2 * Math.PI * 32;
  ringData.forEach(d => {
    const wrapper = document.createElement('div');
    wrapper.style.textAlign = 'center';
    const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
    svg.setAttribute('viewBox','0 0 80 80');
    svg.setAttribute('class','ring-svg');
    const bg = document.createElementNS('http://www.w3.org/2000/svg','circle');
    bg.setAttribute('cx','40');bg.setAttribute('cy','40');bg.setAttribute('r','32');
    bg.setAttribute('class','ring-bg');
    const fg = document.createElementNS('http://www.w3.org/2000/svg','circle');
    fg.setAttribute('cx','40');fg.setAttribute('cy','40');fg.setAttribute('r','32');
    fg.setAttribute('class','ring-fg');
    fg.setAttribute('stroke',d.color);
    fg.setAttribute('stroke-dasharray',circumference);
    fg.setAttribute('stroke-dashoffset',circumference * (1 - d.value));
    svg.appendChild(bg);svg.appendChild(fg);
    wrapper.appendChild(svg);
    const val = document.createElement('div');
    val.className = 'ring-value';
    val.textContent = Math.round(d.value * 100) + '%';
    wrapper.appendChild(val);
    const lbl = document.createElement('div');
    lbl.className = 'ring-label';
    lbl.textContent = d.label;
    wrapper.appendChild(lbl);
    ringContainer.appendChild(wrapper);
  });
  // animate bars staggered
  const bars = chart.querySelectorAll('.chart-bar');
  bars.forEach((b,i) => {
    const h = b.style.height;
    b.style.height = '0px';
    b.style.transition = 'height 0.8s cubic-bezier(0.2,0.9,0.4,1)';
    setTimeout(() => { b.style.height = h; }, 80 + i * 30);
  });
  // ---- PARALLAX ----
  const scene = document.getElementById('scene');
  const layerBg = document.getElementById('layerBg');
  const layerMid = document.getElementById('layerMid');
  const layerFg = document.getElementById('layerFg');
  const SENSITIVITY = { bg: 0.4, mid: 0.2, fg: 0.1 };
  const ROTATE_RANGE = 6; // degrees
  const TRANS_RANGE = 30; // pixels
  function handleParallax(e){
    let cx, cy, w, h;
    if(e.touches && e.touches.length > 0){
      cx = e.touches[0].clientX;
      cy = e.touches[0].clientY;
    } else if(e.clientX !== undefined){
      cx = e.clientX;
      cy = e.clientY;
    } else { return; }
    w = window.innerWidth;
    h = window.innerHeight;
    const nx = (cx / w) * 2 - 1; // -1..1
    const ny = (cy / h) * 2 - 1;
    const rotX = -ny * ROTATE_RANGE;
    const rotY = nx * ROTATE_RANGE;
    const transX = nx * TRANS_RANGE;
    const transY = ny * TRANS_RANGE;
    layerBg.style.transform =
      `translateX(${transX * SENSITIVITY.bg}px) translateY(${transY * SENSITIVITY.bg}px) rotateX(${rotX * SENSITIVITY.bg}deg) rotateY(${rotY * SENSITIVITY.bg}deg) translateZ(-60px)`;
    layerMid.style.transform =
      `translateX(${transX * SENSITIVITY.mid}px) translateY(${transY * SENSITIVITY.mid}px) rotateX(${rotX * SENSITIVITY.mid}deg) rotateY(${rotY * SENSITIVITY.mid}deg) translateZ(0px)`;
    layerFg.style.transform =
      `translateX(${transX * SENSITIVITY.fg}px) translateY(${transY * SENSITIVITY.fg}px) rotateX(${rotX * SENSITIVITY.fg}deg) rotateY(${rotY * SENSITIVITY.fg}deg) translateZ(40px)`;
  }
  function handleLeave(){
    layerBg.style.transform = 'translateZ(-60px)';
    layerMid.style.transform = 'translateZ(0px)';
    layerFg.style.transform = 'translateZ(40px)';
  }
  document.addEventListener('mousemove',handleParallax);
  document.addEventListener('touchmove',handleParallax,{passive:true});
  if ('ontouchstart' in window === false){
    document.addEventListener('mouseleave',handleLeave);
  }
  // ---- DEVICE ORIENTATION (mobile tilt) ----
  if (window.DeviceOrientationEvent){
    window.addEventListener('deviceorientation', function(e){
      if (e.beta === null || e.gamma === null) return;
      if (typeof handleParallax._lastOrientation === 'undefined') handleParallax._lastOrientation = 0;
      const now = Date.now();
      if (now - handleParallax._lastOrientation < 50) return;
      handleParallax._lastOrientation = now;
      const beta = (e.beta || 0) / 45;      // front-to-back, normalize
      const gamma = (e.gamma || 0) / 45;    // left-to-right
      const w = window.innerWidth;
      const h = window.innerHeight;
      const cx = (gamma * 0.5 + 0.5) * w;
      const cy = (beta * 0.5 + 0.5) * h;
      const nx = (cx / w) * 2 - 1;
      const ny = (cy / h) * 2 - 1;
      const rotX = -ny * ROTATE_RANGE;
      const rotY = nx * ROTATE_RANGE;
      const transX = nx * TRANS_RANGE;
      const transY = ny * TRANS_RANGE;
      layerBg.style.transform =
        `translateX(${transX * SENSITIVITY.bg}px) translateY(${transY * SENSITIVITY.bg}px) rotateX(${rotX * SENSITIVITY.bg}deg) rotateY(${rotY * SENSITIVITY.bg}deg) translateZ(-60px)`;
      layerMid.style.transform =
        `translateX(${transX * SENSITIVITY.mid}px) translateY(${transY * SENSITIVITY.mid}px) rotateX(${rotX * SENSITIVITY.mid}deg) rotateY(${rotY * SENSITIVITY.mid}deg) translateZ(0px)`;
      layerFg.style.transform =
        `translateX(${transX * SENSITIVITY.fg}px) translateY(${transY * SENSITIVITY.fg}px) rotateX(${rotX * SENSITIVITY.fg}deg) rotateY(${rotY * SENSITIVITY.fg}deg) translateZ(40px)`;
    }, true);
  }
  // ---- LIVE METRICS UPDATES (simulated) ----
  setInterval(function(){
    const vals = document.querySelectorAll('.metric-value');
    vals.forEach(v => {
      const current = parseFloat(v.textContent);
      if (isNaN(current)) return;
      const delta = (Math.random() - 0.5) * 0.8;
      const newVal = Math.max(0, current + delta);
      v.textContent = newVal.toFixed(1);
    });
    // update ring values
    const ringVals = document.querySelectorAll('.ring-value');
    ringVals.forEach((rv,i) => {
      const base = [0.42, 0.73, 0.21][i];
      const drift = base + (Math.random() - 0.5) * 0.06;
      const clamped = Math.min(1, Math.max(0.05, drift));
      rv.textContent = Math.round(clamped * 100) + '%';
      // update ring stroke
      const svg = rv.parentElement.querySelector('svg');
      if(svg){
        const fg = svg.querySelector('.ring-fg');
        if(fg){
          fg.setAttribute('stroke-dashoffset', circumference * (1 - clamped));
        }
      }
    });
    // animate chart bars
    bars.forEach(b => {
      const cur = parseFloat(b.style.height);
      if (isNaN(cur)) return;
      const drift = cur + (Math.random() - 0.5) * 12;
      const clamped = Math.max(12, Math.min(92, drift));
      b.style.height = clamped + 'px';
    });
  }, 2000);
  // ---- CHROMATIC CLICK FEEDBACK ----
  document.querySelectorAll('.ctrl').forEach(btn => {
    btn.addEventListener('click', function(){
      this.style.animation = 'none';
      void this.offsetHeight;
      this.style.animation = 'chromaticShift 0.4s ease-out';
      // ripple
      const ripple = document.createElement('span');
      ripple.style.cssText = 'position:absolute;border-radius:50%;background:rgba(74,108,247,0.2);width:20px;height:20px;transform:scale(0);animation:rippleAnim 0.6s ease-out;pointer-events:none';
      ripple.style.left = '50%';
      ripple.style.top = '50%';
      ripple.style.marginLeft = '-10px';
      ripple.style.marginTop = '-10px';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });
  // inject ripple keyframe
  const styleSheet = document.createElement('style');
  styleSheet.textContent = '@keyframes rippleAnim{0%{transform:scale(0);opacity:1}100%{transform:scale(8);opacity:0}}';
  document.head.appendChild(styleSheet);
})();
</script>
</body>
</html>
```