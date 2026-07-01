<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Sonification Console</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0f;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;padding:20px}
h1{font-weight:300;font-size:20px;letter-spacing:2px;text-transform:uppercase;color:#48dbfb;margin-bottom:4px}
.subtitle{font-size:11px;color:#576574;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-bottom:20px}
.card{background:#111118;border:1px solid #1e1e2a;border-radius:8px;padding:14px 16px}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#576574}
.metric-name{font-weight:600;color:#c8d6e5;font-size:13px}
.metric-value{font-size:22px;font-weight:300;font-family:'Courier New',monospace;color:#48dbfb;margin:4px 0 10px}
.controls{display:flex;gap:6px;flex-wrap:wrap}
.controls button{background:#1e1e2a;border:1px solid #2d2d3a;color:#8395a7;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:10px;transition:all 0.15s}
.controls button:hover{background:#2d2d3a;color:#c8d6e5}
.controls button.active{background:#48dbfb;color:#0a0a0f;border-color:#48dbfb}
.controls button.solo{background:#ff6348;color:#fff;border-color:#ff6348}
.volume-slider{-webkit-appearance:none;appearance:none;width:100%;height:3px;background:#1e1e2a;border-radius:2px;outline:none;margin-top:8px}
.volume-slider::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:12px;height:12px;border-radius:50%;background:#48dbfb;cursor:pointer}
.volume-slider::-moz-range-thumb{width:12px;height:12px;border-radius:50%;background:#48dbfb;cursor:pointer;border:none}
.status-bar{display:flex;gap:20px;flex-wrap:wrap;font-size:11px;color:#576574;margin-bottom:12px;padding:10px 14px;background:#111118;border:1px solid #1e1e2a;border-radius:8px}
.status-bar span{display:flex;align-items:center;gap:6px}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}
.dot.green{background:#2ecc71}
.dot.orange{background:#f39c12}
.dot.red{background:#e74c3c}
.dot.cyan{background:#48dbfb}
.event-log{background:#0d0d15;border:1px solid #1e1e2a;border-radius:8px;padding:10px 14px;max-height:120px;overflow-y:auto;font-family:'Courier New',monospace;font-size:11px;color:#576574;margin-bottom:20px}
.event-log .event{display:flex;gap:10px;padding:2px 0}
.event-log .event-pos{color:#2ecc71}
.event-log .event-neg{color:#e74c3c}
.event-log .event-info{color:#48dbfb}
.event-time{color:#2d2d3a;width:60px;flex-shrink:0}
.status-indicator{display:flex;align-items:center;gap:8px;font-size:13px}
.health-bar{flex:1;height:4px;background:#1e1e2a;border-radius:2px;overflow:hidden;max-width:200px}
.health-bar-fill{height:100%;border-radius:2px;transition:width 0.5s ease,background 0.5s ease}
.slider-label{display:flex;justify-content:space-between;font-size:9px;color:#576574;margin-top:2px}
.ambient-controls{display:flex;gap:12px;align-items:center;margin-top:8px}
.ambient-controls label{font-size:10px;color:#576574}
.presets{display:flex;gap:6px;margin-bottom:12px}
.presets button{background:#1e1e2a;border:1px solid #2d2d3a;color:#8395a7;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:10px;transition:all 0.15s}
.presets button:hover{background:#2d2d3a;color:#c8d6e5}
</style>
</head>
<body>
<h1>Data Sonification Console</h1>
<div class="subtitle">Web Audio API  |  Real-time sonification of streaming metrics</div>
<div class="presets">
<button data-preset="normal">Normal operation</button>
<button data-preset="highrev">High revenue spike</button>
<button data-preset="errors">Error storm</button>
<button data-preset="grow">Growth phase</button>
</div>
<div class="status-bar">
<span><span class="dot cyan"></span>System health: <span id="healthLabel">72%</span></span>
<div class="health-bar"><div class="health-bar-fill" id="healthFill" style="width:72%;background:#48dbfb"></div></div>
<span>Revenue stream <span id="revStatus">normal</span></span>
<span>Error rate <span id="errStatus">low</span></span>
<span>Active users <span id="userStatus">steady</span></span>
<span>Audio context: <span id="audioStatus"><span class="dot orange"></span> suspended</span></span>
</div>
<div class="grid" id="metricGrid"></div>
<div class="card">
<div class="card-header"><span>Ambient drone</span></div>
<div class="ambient-controls">
<label>On</label>
<input type="checkbox" id="ambientToggle" checked>
<label style="margin-left:12px">Tonality</label>
<select id="tonalitySelect" style="background:#1e1e2a;border:1px solid #2d2d3a;color:#c8d6e5;padding:2px 6px;border-radius:3px;font-size:10px">
<option value="major">Major (healthy)</option>
<option value="minor">Minor (stressed)</option>
<option value="dim">Diminished (critical)</option>
</select>
<label style="margin-left:12px">Volume</label>
<input type="range" id="ambientVolume" min="0" max="1" step="0.01" value="0.2" style="width:80px">
</div>
</div>
<div class="event-log" id="eventLog">
<div class="event"><span class="event-time">--:--:--</span><span class="event-info">System initialized. Awaiting data stream.</span></div>
</div>
<div style="font-size:10px;color:#2d2d3a;text-align:center;margin-top:8px">
Audio engine v1 — Web Audio API  |  Metrics via simulated stream  |  Headphones recommended
</div>
<script>
(function(){
// ---- Audio context ----
let ctx = null;
let masterGain = null;
let analyser = null;
// ---- Metrics config ----
const METRICS = [
  { id:'revenue',      label:'Revenue stream',   unit:'kr/s',  min:0,    max:5000, val:2350,     baseFreq:110, pan:0   },
  { id:'errorRate',    label:'Error rate',        unit:'err/s', min:0,    max:50,   val:2,        baseFreq:400, pan:0.3 },
  { id:'activeUsers',  label:'Active users',       unit:'users', min:0,    max:10000,val:3400,     baseFreq:220, pan:-0.3},
  { id:'latency',      label:'Latency p99',        unit:'ms',    min:0,    max:500,  val:45,       baseFreq:180, pan:0.5 },
  { id:'throughput',   label:'Throughput',        unit:'req/s',  min:0,    max:2000, val:890,      baseFreq:260, pan:-0.5},
  { id:'cpuLoad',      label:'CPU load',           unit:'%',     min:0,    max:100,  val:34,       baseFreq:300, pan:0.7 },
  { id:'memoryUse',    label:'Memory usage',       unit:'%',     min:0,    max:100,  val:62,       baseFreq:150, pan:-0.7},
  { id:'bounceRate',   label:'Bounce rate',        unit:'%',     min:0,    max:100,  val:18,       baseFreq:350, pan:0   },
];
// ---- Channel state ----
const CHANNELS = {};
METRICS.forEach(m => {
  CHANNELS[m.id] = {
    muted: false,
    solo: false,
    volume: 0.7,
    nodes: null,        // {src, gain, panner, filter?}
    lastValue: m.val,
    targetValue: m.val,
    smoothedValue: m.val,
  };
});
// ---- Audio node creation per metric ----
function createMetricNodes(metric) {
  const osc = ctx.createOscillator();
  osc.type = 'sine';
  osc.frequency.value = mapToFreq(metric.val, metric);
  osc.start();
  const gain = ctx.createGain();
  gain.gain.value = 0;
  const panner = ctx.createStereoPanner();
  panner.pan.value = metric.pan;
  // Filter for error rate (noise-ish)
  let filter = null;
  if (metric.id === 'errorRate') {
    osc.type = 'sawtooth';
    filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = mapToFreq(metric.val, metric);
    filter.Q.value = 2;
  }
  if (metric.id === 'cpuLoad') {
    osc.type = 'triangle';
  }
  if (metric.id === 'bounceRate') {
    osc.type = 'square';
  }
  osc.connect(filter || gain);
  if (filter) filter.connect(gain);
  gain.connect(panner);
  panner.connect(analyser || masterGain);
  return { osc, gain, panner, filter };
}
function rebuildMetricNodes(metric) {
  const ch = CHANNELS[metric.id];
  if (ch.nodes) {
    try { ch.nodes.osc.stop(); } catch(e) {}
    try { ch.nodes.osc.disconnect(); } catch(e) {}
    try { ch.nodes.gain.disconnect(); } catch(e) {}
    try { ch.nodes.panner.disconnect(); } catch(e) {}
    if (ch.nodes.filter) try { ch.nodes.filter.disconnect(); } catch(e) {}
  }
  ch.nodes = createMetricNodes(metric);
  updateChannelGain(metric.id);
}
function mapToFreq(val, metric) {
  const ratio = (val - metric.min) / (metric.max - metric.min);
  return metric.baseFreq + Math.max(0, Math.min(1, ratio)) * 600;
}
function mapNoiseFreq(val, metric) {
  const ratio = (val - metric.min) / (metric.max - metric.min);
  return 200 + Math.max(0, Math.min(1, ratio)) * 3000;
}
// ---- Rhythm (active users -> tempo) ----
let rhythmInterval = null;
function updateRhythm() {
  const u = CHANNELS['activeUsers'];
  const val = u.smoothedValue;
  const ratio = (val - 0) / (10000 - 0);
  const bpm = 40 + Math.max(0, Math.min(1, ratio)) * 160;
  const intervalMs = 60000 / bpm;
  if (rhythmInterval) { clearInterval(rhythmInterval); rhythmInterval = null; }
  rhythmInterval = setInterval(() => {
    if (!ctx || ctx.state === 'suspended' || CHANNELS['activeUsers'].muted) return;
    if (isSoloActive() && !CHANNELS['activeUsers'].solo) return;
    const v = CHANNELS['activeUsers'].volume * masterGain.gain.value;
    if (v < 0.01) return;
    // Short pulse
    try {
      const p = ctx.createOscillator();
      p.type = 'sine';
      p.frequency.value = 660;
      const pg = ctx.createGain();
      pg.gain.value = 0;
      p.connect(pg);
      pg.connect(ctx.destination);
      p.start();
      pg.gain.setValueAtTime(0.06 * v, ctx.currentTime);
      pg.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
      p.stop(ctx.currentTime + 0.08);
    } catch(e) {}
  }, intervalMs);
  document.getElementById('userStatus').textContent = Math.round(bpm) + ' bpm';
}
// ---- Ambient drone ----
let ambientNodes = null;
function buildAmbient() {
  if (ambientNodes) {
    try { ambientNodes.osc1.stop(); } catch(e) {}
    try { ambientNodes.osc2.stop(); } catch(e) {}
    try { ambientNodes.osc3.stop(); } catch(e) {}
    try { ambientNodes.lfo.stop(); } catch(e) {}
  }
  const tonality = document.getElementById('tonalitySelect').value;
  const baseAmt = 0.15;
  let freqs;
  if (tonality === 'major')    freqs = [110, 138.59, 164.81, 220];
  if (tonality === 'minor')    freqs = [110, 130.81, 155.56, 220];
  if (tonality === 'dim')      freqs = [110, 130.81, 155.56, 174.61];
  const o1 = ctx.createOscillator(); o1.type='sine'; o1.frequency.value=freqs[0];
  const o2 = ctx.createOscillator(); o2.type='sine'; o2.frequency.value=freqs[1]; o2.detune.value=5;
  const o3 = ctx.createOscillator(); o3.type='sine'; o3.frequency.value=freqs[2]; o3.detune.value=-3;
  const lfo = ctx.createOscillator(); lfo.type='sine'; lfo.frequency.value=0.15;
  const g1 = ctx.createGain(); g1.gain.value=baseAmt;
  const g2 = ctx.createGain(); g2.gain.value=baseAmt*0.6;
  const g3 = ctx.createGain(); g3.gain.value=baseAmt*0.4;
  const lfoGain = ctx.createGain(); lfoGain.gain.value=0.03;
  o1.connect(g1); g1.connect(masterGain);
  o2.connect(g2); g2.connect(masterGain);
  o3.connect(g3); g3.connect(masterGain);
  lfo.connect(lfoGain); lfoGain.connect(g1.gain);
  o1.start(); o2.start(); o3.start(); lfo.start();
  const volEl = document.getElementById('ambientVolume');
  g1.gain.value = baseAmt * parseFloat(volEl.value);
  g2.gain.value = baseAmt * 0.6 * parseFloat(volEl.value);
  g3.gain.value = baseAmt * 0.4 * parseFloat(volEl.value);
  const toggle = document.getElementById('ambientToggle');
  if (!toggle.checked) { g1.gain.value=0; g2.gain.value=0; g3.gain.value=0; }
  ambientNodes = { osc1:o1, osc2:o2, osc3:o3, lfo, g1, g2, g3, lfoGain, baseAmt };
}
function updateAmbientVolume() {
  if (!ambientNodes) return;
  const vol = document.getElementById('ambientToggle').checked ? parseFloat(document.getElementById('ambientVolume').value) : 0;
  ambientNodes.g1.gain.value = ambientNodes.baseAmt * vol;
  ambientNodes.g2.gain.value = ambientNodes.baseAmt * 0.6 * vol;
  ambientNodes.g3.gain.value = ambientNodes.baseAmt * 0.4 * vol;
}
// ---- Status events (chimes) ----
function playChime(positive) {
  if (!ctx || ctx.state === 'suspended') return;
  try {
    const o = ctx.createOscillator();
    o.type = 'sine';
    const g = ctx.createGain();
    g.gain.value = 0;
    o.connect(g);
    g.connect(ctx.destination);
    const t = ctx.currentTime;
    if (positive) {
      o.frequency.setValueAtTime(523.25, t);
      o.frequency.setValueAtTime(659.25, t+0.1);
      o.frequency.setValueAtTime(783.99, t+0.2);
    } else {
      o.frequency.setValueAtTime(440, t);
      o.frequency.setValueAtTime(349.23, t+0.12);
      o.frequency.setValueAtTime(293.66, t+0.25);
    }
    g.gain.setValueAtTime(0.08, t);
    g.gain.exponentialRampToValueAtTime(0.001, t+0.45);
    o.start(t);
    o.stop(t+0.5);
  } catch(e) {}
}
let eventCounter = 0;
function addEvent(text, type='info') {
  eventCounter++;
  const log = document.getElementById('eventLog');
  const d = new Date();
  const ts = d.toTimeString().slice(0,8);
  const cls = type==='pos' ? 'event-pos' : type==='neg' ? 'event-neg' : 'event-info';
  const el = document.createElement('div');
  el.className = 'event';
  el.innerHTML = `<span class="event-time">${ts}</span><span class="${cls}">${text}</span>`;
  log.appendChild(el);
  if (log.children.length > 50) log.removeChild(log.firstChild);
  log.scrollTop = log.scrollHeight;
  if (type !== 'info') playChime(type === 'pos');
}
// ---- Solo logic ----
function isSoloActive() {
  return Object.values(CHANNELS).some(ch => ch.solo);
}
function updateChannelGain(id) {
  const ch = CHANNELS[id];
  if (!ch.nodes) return;
  const soloActive = isSoloActive();
  let targetGain = 0;
  if (!ch.muted) {
    if (!soloActive || ch.solo) {
      targetGain = ch.volume * 0.12;
    }
  }
  try {
    ch.nodes.gain.gain.setTargetAtTime(targetGain, ctx.currentTime, 0.05);
  } catch(e) {}
}
// ---- UI rendering ----
function renderMetrics() {
  const grid = document.getElementById('metricGrid');
  grid.innerHTML = '';
  METRICS.forEach(m => {
    const ch = CHANNELS[m.id];
    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'card-' + m.id;
    const valDisplay = ((m.val) < 10 ? m.val.toFixed(1) : Math.round(m.val));
    card.innerHTML = `
      <div class="card-header">
        <span class="metric-name">${m.label}</span>
        <span style="font-size:10px;color:#576574">${m.unit}</span>
      </div>
      <div class="metric-value" id="val-${m.id}">${valDisplay}</div>
      <div class="controls">
        <button class="mute-btn ${ch.muted?'active':''}" data-id="${m.id}" data-action="mute">Mute</button>
        <button class="solo-btn ${ch.solo?'solo':''}" data-id="${m.id}" data-action="solo">Solo</button>
        <button class="reset-btn" data-id="${m.id}" data-action="reset">Reset</button>
      </div>
      <input type="range" class="volume-slider" data-id="${m.id}" min="0" max="1" step="0.01" value="${ch.volume}">
      <div class="slider-label"><span>Vol</span><span>${Math.round(ch.volume*100)}%</span></div>
      <div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap">
        <span style="font-size:9px;color:#576574">osc:</span>
        <span style="font-size:9px;color:#48dbfb" id="freq-${m.id}">${Math.round(ch.nodes?.osc?.frequency?.value || mapToFreq(m.val,m))} Hz</span>
      </div>
    `;
    grid.appendChild(card);
  });
  // Attach events
  document.querySelectorAll('.mute-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const id = this.dataset.id;
      const ch = CHANNELS[id];
      ch.muted = !ch.muted;
      this.classList.toggle('active');
      updateChannelGain(id);
      addEvent(`${METRICS.find(m=>m.id===id).label} ${ch.muted?'muted':'unmuted'}`, 'info');
    });
  });
  document.querySelectorAll('.solo-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const id = this.dataset.id;
      const ch = CHANNELS[id];
      ch.solo = !ch.solo;
      this.classList.toggle('solo');
      // Update all channels
      METRICS.forEach(m => updateChannelGain(m.id));
      const soloActive = isSoloActive();
      addEvent(soloActive ? `Solo mode: ${METRICS.find(m=>m.id===id).label}` : 'Solo mode off', 'info');
    });
  });
  document.querySelectorAll('.reset-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const id = this.dataset.id;
      const m = METRICS.find(mt => mt.id === id);
      const mid = Math.round((m.min + m.max) / 2);
      m.val = mid;
      CHANNELS[id].targetValue = mid;
      document.getElementById('val-'+id).textContent = mid < 10 ? mid.toFixed(1) : Math.round(mid);
      updateMetricAudio(id);
      addEvent(`${m.label} reset to baseline (${mid})`, 'info');
    });
  });
  document.querySelectorAll('.volume-slider').forEach(sl => {
    sl.addEventListener('input', function(e) {
      const id = this.dataset.id;
      const ch = CHANNELS[id];
      ch.volume = parseFloat(this.value);
      updateChannelGain(id);
      const label = this.parentElement.querySelector('.slider-label span:last-child');
      if (label) label.textContent = Math.round(ch.volume*100) + '%';
    });
  });
}
// ---- Audio update per metric ----
function updateMetricAudio(id) {
  const m = METRICS.find(mt => mt.id === id);
  if (!m) return;
  const ch = CHANNELS[id];
  if (!ch.nodes) return;
  const freq = mapToFreq(m.val, m);
  try {
    ch.nodes.osc.frequency.setTargetAtTime(freq, ctx.currentTime, 0.08);
    if (ch.nodes.filter) {
      ch.nodes.filter.frequency.setTargetAtTime(mapNoiseFreq(m.val, m), ctx.currentTime, 0.08);
    }
  } catch(e) {}
  const freqEl = document.getElementById('freq-'+id);
  if (freqEl) freqEl.textContent = Math.round(freq) + ' Hz';
}
// ---- System health & ambient ----
function updateSystemHealth() {
  const currentVals = METRICS.map(m => {
    const ratio = (m.val - m.min) / (m.max - m.min);
    return Math.max(0, Math.min(1, ratio));
  });
  // Revenue good when high, error good when low, latency good when low, etc
  const goodMetrics = [
    currentVals[0],                      // revenue: high=good
    1 - currentVals[1],                  // error: low=good
    currentVals[2] > 0.15 ? Math.min(1, currentVals[2]*1.5) : 0, // users: above 15% = good
    1 - currentVals[3],                  // latency: low=good
    currentVals[4],                      // throughput: high=good
    1 - currentVals[5],                  // cpu: low=good
    1 - currentVals[6],                  // memory: low=good
    1 - currentVals[7],                  // bounce: low=good
  ];
  const health = goodMetrics.reduce((a,b)=>a+b,0) / goodMetrics.length * 100;
  const healthClamped = Math.max(5, Math.min(100, Math.round(health)));
  document.getElementById('healthLabel').textContent = healthClamped + '%';
  const fill = document.getElementById('healthFill');
  fill.style.width = healthClamped + '%';
  if (healthClamped >= 70) fill.style.background = '#2ecc71';
  else if (healthClamped >= 40) fill.style.background = '#f39c12';
  else fill.style.background = '#e74c3c';
  // Update ambient tonality
  const tonality = document.getElementById('tonalitySelect');
  if (healthClamped >= 70 && tonality.value !== 'major') {
    tonality.value = 'major';
    buildAmbient();
    addEvent('Ambient shifted to major (healthy)', 'pos');
  } else if (healthClamped >= 40 && healthClamped < 70 && tonality.value !== 'minor') {
    tonality.value = 'minor';
    buildAmbient();
    addEvent('Ambient shifted to minor (stressed)', 'neg');
  } else if (healthClamped < 40 && tonality.value !== 'dim') {
    tonality.value = 'dim';
    buildAmbient();
    addEvent('Ambient shifted to diminished (critical)', 'neg');
  }
  return healthClamped;
}
// ---- Metric value frame update (simulated stream) ----
function updateMetrics() {
  const solo = isSoloActive();
  METRICS.forEach(m => {
    const ch = CHANNELS[m.id];
    // Random walk toward target
    let walk = (Math.random() - 0.48) * m.max * 0.03;
    m.val += walk;
    m.val = Math.max(m.min, Math.min(m.max, m.val));
    ch.smoothedValue += (m.val - ch.smoothedValue) * 0.2;
    // Update displayed value
    const el = document.getElementById('val-'+m.id);
    if (el) el.textContent = (m.val < 10 ? m.val.toFixed(1) : Math.round(m.val));
    // Update audio
    updateMetricAudio(m.id);
  });
  // System health
  const health = updateSystemHealth();
  // Revenue status
  const rev = METRICS[0].val;
  const revRatio = rev / METRICS[0].max;
  document.getElementById('revStatus').textContent = revRatio > 0.7 ? 'high' : revRatio > 0.3 ? 'normal' : 'low';
  // Error status
  const err = METRICS[1].val;
  document.getElementById('errStatus').textContent = err > 20 ? 'elevated' : err > 5 ? 'moderate' : 'low';
  // Check for threshold events
  if (revRatio > 0.85 && !chRevSpike) {
    chRevSpike = true;
    addEvent(`Revenue spike: ${Math.round(rev)} kr/s`, 'pos');
  }
  if (revRatio <= 0.8) chRevSpike = false;
  if (err > 25 && !chErrSpike) {
    chErrSpike = true;
    addEvent(`Error rate critical: ${err.toFixed(1)} err/s`, 'neg');
  }
  if (err <= 20) chErrSpike = false;
  const u = METRICS[2].val;
  if (u > 8000 && !chUserHigh) {
    chUserHigh = true;
    addEvent(`User milestone: ${Math.round(u)} active users`, 'pos');
  }
  if (u <= 7500) chUserHigh = false;
}
let chRevSpike = false, chErrSpike = false, chUserHigh = false;
let updateInterval = null;
// ---- Init audio ----
function initAudio() {
  if (ctx && ctx.state !== 'closed') return;
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  masterGain = ctx.createGain();
  masterGain.gain.value = 0.6;
  masterGain.connect(ctx.destination);
  analyser = ctx.createAnalyser();
  analyser.fftSize = 256;
  masterGain.connect(analyser);
  // Build metric nodes
  METRICS.forEach(m => {
    CHANNELS[m.id].nodes = createMetricNodes(m);
    updateChannelGain(m.id);
  });
  // Build ambient
  buildAmbient();
  updateRhythm();
  document.getElementById('audioStatus').innerHTML = '<span class="dot green"></span> running';
  addEvent('Audio context initialized. Sonification engine online.', 'pos');
}
function startStream() {
  if (updateInterval) clearInterval(updateInterval);
  updateInterval = setInterval(updateMetrics, 600);
  addEvent('Data stream started (600ms interval)', 'info');
}
function stopStream() {
  if (updateInterval) { clearInterval(updateInterval); updateInterval = null; }
  if (rhythmInterval) { clearInterval(rhythmInterval); rhythmInterval = null; }
  addEvent('Data stream stopped', 'info');
}
// ---- Presets ----
function applyPreset(name) {
  if (!ctx || ctx.state === 'suspended') {
    initAudio();
    if (ctx.state === 'suspended') ctx.resume();
  }
  const resetToMedian = (id, val) => {
    const m = METRICS.find(mt => mt.id === id);
    if (m) { m.val = val; CHANNELS[id].targetValue = val; updateMetricAudio(id); }
  };
  if (name === 'normal') {
    resetToMedian('revenue', 2350);
    resetToMedian('errorRate', 2);
    resetToMedian('activeUsers', 3400);
    resetToMedian('latency', 45);
    resetToMedian('throughput', 890);
    resetToMedian('cpuLoad', 34);
    resetToMedian('memoryUse', 62);
    resetToMedian('bounceRate', 18);
    addEvent('Preset: Normal operation', 'info');
  } else if (name === 'highrev') {
    resetToMedian('revenue', 4700);
    resetToMedian('errorRate', 1);
    resetToMedian('activeUsers', 7200);
    resetToMedian('latency', 30);
    resetToMedian('throughput', 1850);
    resetToMedian('cpuLoad', 55);
    resetToMedian('memoryUse', 78);
    resetToMedian('bounceRate', 8);
    addEvent('Preset: High revenue spike', 'pos');
  } else if (name === 'errors') {
    resetToMedian('revenue', 800);
    resetToMedian('errorRate', 38);
    resetToMedian('activeUsers', 1200);
    resetToMedian('latency', 320);
    resetToMedian('throughput', 210);
    resetToMedian('cpuLoad', 88);
    resetToMedian('memoryUse', 95);
    resetToMedian('bounceRate', 62);
    addEvent('Preset: Error storm — system under duress', 'neg');
  } else if (name === 'grow') {
    resetToMedian('revenue', 3800);
    resetToMedian('errorRate', 0.5);
    resetToMedian('activeUsers', 8800);
    resetToMedian('latency', 22);
    resetToMedian('throughput', 1650);
    resetToMedian('cpuLoad', 45);
    resetToMedian('memoryUse', 55);
    resetToMedian('bounceRate', 12);
    addEvent('Preset: Growth phase — healthy scaling', 'pos');
  }
}
// ---- Init UI & event listeners ----
document.addEventListener('DOMContentLoaded', function() {
  renderMetrics();
  // Click-to-init audio (user gesture requirement)
  document.addEventListener('click', function initOnce() {
    if (!ctx) {
      initAudio();
    } else if (ctx.state === 'suspended') {
      ctx.resume().then(() => {
        document.getElementById('audioStatus').innerHTML = '<span class="dot green"></span> running';
        addEvent('Audio context resumed', 'info');
      });
    }
    if (!updateInterval) startStream();
  }, { once: false });
  // Ambient controls
  document.getElementById('ambientToggle').addEventListener('change', updateAmbientVolume);
  document.getElementById('ambientVolume').addEventListener('input', updateAmbientVolume);
  document.getElementById('tonalitySelect').addEventListener('change', () => { if (ctx) buildAmbient(); });
  // Presets
  document.querySelectorAll('[data-preset]').forEach(btn => {
    btn.addEventListener('click', function() {
      applyPreset(this.dataset.preset);
    });
  });
});
// Expose for dev console
window.__sonification = { ctx, METRICS, CHANNELS, initAudio, startStream, stopStream, applyPreset };
})();
</script>
</body>
</html>