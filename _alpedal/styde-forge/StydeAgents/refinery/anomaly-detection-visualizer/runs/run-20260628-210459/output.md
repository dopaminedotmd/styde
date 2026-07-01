```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Anomaly Detection Visualizer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0b0e17;--panel:#111622;--border:#1e2a3a;--text:#c8d6e5;--dim:#5f7a9a;--green:#2ecc71;--red:#e74c3c;--orange:#f39c12;--blue:#3498db;--purple:#9b59b6;--cyan:#1abc9c;--pulse-color:rgba(231,76,60,0.6);--pulse-color-warn:rgba(243,156,18,0.5);--font:'SF Mono','Fira Code','Cascadia Code','Consolas',monospace}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;overflow:hidden}
body{display:flex;flex-direction:column}
h1{font-size:14px;font-weight:600;color:#ecf0f1;letter-spacing:0.5px;text-transform:uppercase;padding:10px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px}
h1 small{font-size:11px;color:var(--dim);font-weight:400;text-transform:none}
h1 .status-dot{width:8px;height:8px;border-radius:50%;display:inline-block;background:var(--green);animation:none}
h1 .status-dot.alert{background:var(--red);animation:pulse-dot 1.5s ease-in-out infinite}
h1 .status-dot.warn{background:var(--orange);animation:pulse-dot 2s ease-in-out infinite}
h1 .status-dot.idle{background:var(--dim);animation:none}
@keyframes pulse-dot{0%,100%{opacity:1;box-shadow:0 0 0 0 currentColor}50%{opacity:0.6;box-shadow:0 0 8px 2px currentColor}}
#app{display:flex;flex:1;overflow:hidden}
.col{display:flex;flex-direction:column}
.col-left{width:380px;min-width:380px;border-right:1px solid var(--border)}
.col-center{flex:1;min-width:0}
.col-right{width:300px;min-width:300px;border-left:1px solid var(--border)}
.panel{background:var(--panel);border-radius:4px;margin:6px;border:1px solid var(--border)}
.panel header{padding:6px 10px;font-size:11px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:0.8px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}
.panel header .badge{font-size:10px;padding:1px 6px;border-radius:8px;background:var(--border);color:var(--dim);font-weight:500}
.panel body{display:block;padding:6px}
canvas{display:block;width:100%;height:100%}
.chart-wrap{position:relative;overflow:hidden;flex:1;min-height:0}
#heatmap-canvas,#drift-canvas{width:100%;height:100%;display:block}
#pulse-container{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:5}
.pulse-ring{position:absolute;border-radius:50%;border:2px solid var(--pulse-color);width:0;height:0;animation:pulse-expand 1.8s ease-out forwards}
.pulse-ring.warn{border-color:var(--pulse-color-warn)}
.pulse-ring.crit{border-color:var(--pulse-color);border-width:3px}
@keyframes pulse-expand{0%{width:0;height:0;opacity:0.9;transform:translate(0,0)}30%{opacity:0.7}100%{width:120px;height:120px;opacity:0;transform:translate(-60px,-60px)}}
#controls{display:flex;gap:6px;padding:6px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border)}
#controls button,.ctrl-btn{background:var(--border);border:1px solid transparent;color:var(--text);font-family:var(--font);font-size:11px;padding:4px 10px;border-radius:3px;cursor:pointer;transition:all 0.15s;white-space:nowrap}
#controls button:hover,.ctrl-btn:hover{background:#2a3a4a;border-color:var(--dim)}
#controls button.active{background:var(--blue);color:#fff;border-color:var(--blue)}
#controls button.danger.active{background:var(--red);border-color:var(--red);color:#fff}
#controls button.danger:hover{background:#c0392b;border-color:#c0392b}
#controls label{font-size:11px;color:var(--dim);display:flex;align-items:center;gap:4px}
#controls input[type=range]{width:60px;height:4px;accent-color:var(--blue);background:var(--border);border:none;border-radius:2px}
#controls .sep{width:1px;height:16px;background:var(--border);margin:0 4px}
.metrics-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:6px}
.metric-card{background:#0d111e;border:1px solid var(--border);border-radius:3px;padding:8px;position:relative;overflow:hidden}
.metric-card .name{font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:0.5px}
.metric-card .value{font-size:18px;font-weight:700;color:#ecf0f1;font-variant-numeric:tabular-nums}
.metric-card .value.alert{color:var(--red);text-shadow:0 0 6px rgba(231,76,60,0.4)}
.metric-card .value.warn{color:var(--orange)}
.metric-card .value.good{color:var(--green)}
.metric-card .zscore{font-size:10px;color:var(--dim);margin-top:2px}
.metric-card .spark-mini{height:20px;margin-top:4px;position:relative}
.metric-card .spark-mini canvas{width:100%;height:20px;display:block;border-radius:2px}
.metric-card .anomaly-badge{position:absolute;top:6px;right:6px;font-size:9px;padding:1px 5px;border-radius:6px;background:var(--red);color:#fff;font-weight:600;opacity:0;transition:opacity 0.3s}
.metric-card .anomaly-badge.show{opacity:1}
#stream-stats{padding:6px;display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:10px;color:var(--dim)}
#stream-stats span{display:flex;justify-content:space-between}
#stream-stats span b{color:var(--text)}
#root-cause-panel{max-height:220px;overflow-y:auto;padding:6px}
#root-cause-panel .cause-item{padding:3px 0;font-size:11px;border-bottom:1px solid rgba(30,42,58,0.5);display:flex;align-items:center;gap:6px}
#root-cause-panel .cause-item:last-child{border-bottom:none}
#root-cause-panel .cause-metric{color:var(--cyan);font-weight:600}
#root-cause-panel .cause-dir{font-size:10px;padding:1px 4px;border-radius:3px}
#root-cause-panel .cause-dir.spike{background:rgba(231,76,60,0.2);color:var(--red)}
#root-cause-panel .cause-dir.drop{background:rgba(155,89,182,0.2);color:var(--purple)}
#root-cause-panel .cause-dir.shift{background:rgba(243,156,18,0.2);color:var(--orange)}
#root-cause-panel .cause-chain{font-size:10px;color:var(--dim);margin-left:16px;display:flex;gap:3px;align-items:center}
#root-cause-panel .cause-chain .arrow{color:var(--dim);font-size:9px}
#placeholder-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:var(--dim);gap:12px}
#placeholder-state .big-icon{font-size:48px;opacity:0.3}
#placeholder-state .msg{font-size:13px;font-weight:500;letter-spacing:1px;text-transform:uppercase;opacity:0.5}
#placeholder-state .sub{font-size:11px;opacity:0.3}
.tooltip-overlay{position:absolute;background:#0d111e;border:1px solid var(--border);border-radius:4px;padding:6px 10px;font-size:11px;pointer-events:none;z-index:20;display:none;max-width:200px;box-shadow:0 4px 12px rgba(0,0,0,0.5);line-height:1.5}
.tooltip-overlay.visible{display:block}
.tooltip-overlay .tt-label{color:var(--dim);font-weight:500}
.tooltip-overlay .tt-val{color:var(--text);font-weight:700}
.tooltip-overlay .tt-z{color:var(--orange)}
.tooltip-overlay .tt-anom{color:var(--red);font-weight:600}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
::-webkit-scrollbar-thumb:hover{background:var(--dim)}
@media(max-width:1000px){.col-right{display:none}.col-left{width:280px;min-width:280px}}
@media(max-width:700px){.col-left{width:100%;min-width:0;border-right:none;border-bottom:1px solid var(--border)}#app{flex-direction:column}.col-center{flex:0 0 50vh}}
.chart-area{flex:1;display:flex;flex-direction:column;min-height:0;position:relative}
.chart-split{flex:1;display:flex;flex-direction:column;min-height:0}
.chart-split .chart-wrap{flex:1;min-height:120px}
.chart-split .chart-wrap:first-child{border-bottom:1px solid var(--border)}
.threshold-legend{position:absolute;top:4px;right:8px;font-size:9px;color:var(--dim);z-index:3;display:flex;gap:8px}
.threshold-legend span{display:flex;align-items:center;gap:3px}
.threshold-legend .swatch{width:8px;height:3px;border-radius:1px;display:inline-block}
.dashed-connector{stroke:var(--dim);stroke-dasharray:4,4;stroke-width:1.5;fill:none}
#drift-canvas{cursor:crosshair}
</style>
</head>
<body>
<h1>
  <span class="status-dot idle" id="status-dot"></span>
  Anomaly Detection Visualizer
  <small id="header-sub">awaiting stream...</small>
</h1>
<div id="controls">
  <button id="btn-stream" class="active">Stream</button>
  <button id="btn-pause">Pause</button>
  <button id="btn-reset" class="danger">Reset</button>
  <span class="sep"></span>
  <label>Window <input type="range" id="slider-window" min="10" max="200" value="60"></label>
  <label>Z-threshold <input type="range" id="slider-threshold" min="1.5" max="5" step="0.1" value="2.5"></label>
  <span class="sep"></span>
  <button id="btn-toggle-heatmap" class="active">Heatmap</button>
  <button id="btn-toggle-drift" class="active">Drift</button>
  <button id="btn-toggle-pulse" class="active">Pulse</button>
</div>
<div id="app">
  <div class="col col-left">
    <div class="panel" id="metrics-panel">
      <header>Metrics <span class="badge" id="metric-count">0</span></header>
      <body><div class="metrics-grid" id="metrics-grid"></div></body>
    </div>
    <div class="panel" id="stats-panel">
      <header>Stream Stats</header>
      <body><div id="stream-stats"></div></body>
    </div>
    <div class="panel" id="rootcause-panel">
      <header>Root Cause Chain <span class="badge" id="cause-count">0</span></header>
      <body><div id="root-cause-panel"></div></body>
    </div>
  </div>
  <div class="col col-center">
    <div class="chart-split" id="chart-split">
      <div class="chart-wrap" id="heatmap-wrap">
        <canvas id="heatmap-canvas"></canvas>
        <div id="pulse-container"></div>
        <div class="threshold-legend">
          <span><span class="swatch" style="background:var(--green)"></span> normal</span>
          <span><span class="swatch" style="background:var(--orange)"></span> warn</span>
          <span><span class="swatch" style="background:var(--red)"></span> anomaly</span>
        </div>
      </div>
      <div class="chart-wrap" id="drift-wrap">
        <canvas id="drift-canvas"></canvas>
      </div>
    </div>
    <div id="placeholder-state">
      <div class="big-icon">&#9724;</div>
      <div class="msg">Awaiting stream...</div>
      <div class="sub">connect data source to begin monitoring</div>
    </div>
  </div>
  <div class="col col-right">
    <div class="panel" style="flex:1;display:flex;flex-direction:column">
      <header>Anomaly Log</header>
      <body style="flex:1;overflow-y:auto;padding:6px" id="anomaly-log">
        <div style="text-align:center;color:var(--dim);padding:20px;font-size:11px">No anomalies detected yet</div>
      </body>
    </div>
  </div>
</div>
<div class="tooltip-overlay" id="tooltip"><div id="tooltip-content"></div></div>
<script>
// ─── Metric Bus ───────────────────────────────────────────────────────────────
const METRICS = ['cpu_usage','memory_usage','request_rate','error_rate','latency_p99','throughput','disk_io','connection_count'];
const METRIC_LABELS = ['CPU','Memory','Req Rate','Error Rate','Latency p99','Throughput','Disk IO','Connections'];
const METRIC_COLORS = ['#3498db','#2ecc71','#f39c12','#e74c3c','#9b59b6','#1abc9c','#e67e22','#95a5a6'];
const METRIC_UNITS = ['%','%','req/s','%','ms','mb/s','mb/s','count'];
const METRIC_RANGES = [[0,100],[0,100],[0,5000],[0,100],[0,5000],[0,2000],[0,500],[0,10000]];
const NORMAL_VALUES = [45,62,1200,2.3,180,450,140,5200];
const bus = new Map();
METRICS.forEach((id,i) => {
  bus.set(id, {
    id, label: METRIC_LABELS[i],
    color: METRIC_COLORS[i],
    unit: METRIC_UNITS[i],
    range: METRIC_RANGES[i],
    normal: NORMAL_VALUES[i],
    values: [], timestamps: [],
    zscores: [], anomalies: [],
    iqrLower: [], iqrUpper: [],
    window: 60
  });
});
// ─── State ────────────────────────────────────────────────────────────────────
let streaming = true;
let paused = false;
let tickCount = 0;
let anomalyCount = 0;
let lastGapEnd = null;
let gapActive = false;
let gapStartTime = null;
let anomalyHistory = [];
let rootCauses = [];
const MAX_POINTS = 10000;
const DOWNSAMPLE_TARGET = 2000;
const GAP_THRESHOLD_MS = 3000;
const PLACEHOLDER_CYCLES = 10;
let noDataCycles = 0;
let windowSize = 60;
let zThreshold = 2.5;
let showHeatmap = true;
let showDrift = true;
let showPulse = true;
let animFrameId = null;
let lastFrameTime = 0;
let heatmapCanvas, heatmapCtx, driftCanvas, driftCtx;
let heatmapW, heatmapH, driftW, driftH;
// ─── Simulation ───────────────────────────────────────────────────────────────
function generateTick(t) {
  const data = {};
  METRICS.forEach((id,i) => {
    let val = NORMAL_VALUES[i];
    const noise = (Math.random() - 0.5) * (METRIC_RANGES[i][1] - METRIC_RANGES[i][0]) * 0.08;
    val += noise;
    // Occasionally inject anomalies (random walk or spike)
    if (Math.random() < 0.03) {
      val += (Math.random() - 0.3) * (METRIC_RANGES[i][1] - METRIC_RANGES[i][0]) * 0.4;
    }
    if (Math.random() < 0.008) {
      val += (Math.random() > 0.5 ? 1 : -1) * (METRIC_RANGES[i][1] - METRIC_RANGES[i][0]) * 0.7;
    }
    // Add trend correlation: if cpu spikes, latency tends to follow
    if (id === 'latency_p99' && bus.get('cpu_usage') && bus.get('cpu_usage').values.length > 0) {
      const cpu = bus.get('cpu_usage').values[bus.get('cpu_usage').values.length - 1];
      if (cpu > NORMAL_VALUES[0] * 1.3) {
        val += (cpu - NORMAL_VALUES[0]) * 2.5;
      }
    }
    // Error rate correlating with latency
    if (id === 'error_rate' && bus.get('latency_p99') && bus.get('latency_p99').values.length > 0) {
      const lat = bus.get('latency_p99').values[bus.get('latency_p99').values.length - 1];
      if (lat > NORMAL_VALUES[4] * 1.2) {
        val += (lat - NORMAL_VALUES[4]) * 0.03;
      }
    }
    val = Math.max(METRIC_RANGES[i][0], Math.min(METRIC_RANGES[i][1], val));
    data[id] = val;
  });
  return data;
}
// ─── Statistical Functions ────────────────────────────────────────────────────
function mean(arr) { return arr.reduce((s,v)=>s+v,0) / arr.length; }
function std(arr) {
  const m = mean(arr);
  return Math.sqrt(arr.reduce((s,v)=>s+(v-m)**2,0) / arr.length);
}
function median(arr) {
  const s = [...arr].sort((a,b)=>a-b);
  const mid = Math.floor(s.length/2);
  return s.length % 2 ? s[mid] : (s[mid-1]+s[mid])/2;
}
function iqr(arr) {
  const s = [...arr].sort((a,b)=>a-b);
  const q1 = s[Math.floor(s.length*0.25)];
  const q3 = s[Math.floor(s.length*0.75)];
  return {q1,q3,iqr:q3-q1,median:s[Math.floor(s.length*0.5)]};
}
function zScores(arr) { const m=mean(arr), sd=std(arr); return sd===0?arr.map(()=>0):arr.map(v=>(v-m)/sd); }
// Change-point detection using CUSUM
function detectChangePoint(values, threshold=1.5) {
  if (values.length < 10) return false;
  const m = mean(values.slice(0, Math.floor(values.length*0.3)));
  let cumSum = 0;
  const recent = values.slice(-10);
  for (const v of recent) {
    cumSum += (v - m) / (std(values) || 1);
  }
  return Math.abs(cumSum) > threshold;
}
// Downsample to target length
function downsample(values, timestamps, target) {
  if (values.length <= target) return {values, timestamps};
  const ratio = values.length / target;
  const outV = [], outT = [];
  for (let i = 0; i < target; i++) {
    const idx = Math.round(i * ratio);
    outV.push(values[Math.min(idx, values.length-1)]);
    outT.push(timestamps[Math.min(idx, timestamps.length-1)]);
  }
  return {values: outV, timestamps: outT};
}
// ─── Ingestion ─────────────────────────────────────────────────────────────────
function ingest(data) {
  const now = performance.now();
  METRICS.forEach((id,i) => {
    const m = bus.get(id);
    let val = data[id];
    m.values.push(val);
    m.timestamps.push(now);
    // Trim to MAX_POINTS
    if (m.values.length > MAX_POINTS) {
      const excess = m.values.length - MAX_POINTS;
      m.values.splice(0, excess);
      m.timestamps.splice(0, excess);
    }
    // Downsample if needed
    if (m.values.length > DOWNSAMPLE_TARGET) {
      const d = downsample(m.values, m.timestamps, DOWNSAMPLE_TARGET);
      m.values = d.values;
      m.timestamps = d.timestamps;
    }
    // Compute statistics
    const w = Math.min(windowSize, m.values.length);
    const recent = m.values.slice(-w);
    if (recent.length >= 5) {
      const z = zScores(recent);
      m.zscores = z;
      const stats = iqr(recent);
      m.iqrLower = new Array(m.values.length).fill(null);
      m.iqrUpper = new Array(m.values.length).fill(null);
      m.iqrLower[m.values.length-1] = stats.q1 - 1.5 * stats.iqr;
      m.iqrUpper[m.values.length-1] = stats.q3 + 1.5 * stats.iqr;
    }
    // Detect anomalies
    const lastZ = m.zscores.length > 0 ? m.zscores[m.zscores.length-1] : 0;
    const isAnom = Math.abs(lastZ) > zThreshold;
    m.anomalies.push(isAnom);
    if (m.anomalies.length > m.values.length) {
      m.anomalies.splice(0, m.anomalies.length - m.values.length);
    }
    if (isAnom && i === 0) { // Track first metric anomaly for root cause
      anomalyHistory.push({time: now, metric: id, z: lastZ, val});
    }
  });
  tickCount++;
  noDataCycles = 0;
}
// ─── Root Cause Analysis ──────────────────────────────────────────────────────
function computeRootCauses() {
  const anomMetrics = [];
  METRICS.forEach((id,i) => {
    const m = bus.get(id);
    if (m.values.length < 5) return;
    const lastZ = m.zscores.length > 0 ? m.zscores[m.zscores.length-1] : 0;
    if (Math.abs(lastZ) > zThreshold) {
      anomMetrics.push({id, label: m.label, z: lastZ, val: m.values[m.values.length-1], color: m.color});
    }
  });
  if (anomMetrics.length === 0) {
    rootCauses = [];
    return;
  }
  // Build causal chains: for the primary anomaly, find metrics that shifted before it
  const primary = anomMetrics[0];
  const chain = [];
  const refIdx = bus.get(primary.id).values.length - 1;
  METRICS.forEach((id,i) => {
    if (id === primary.id) return;
    const m = bus.get(id);
    if (m.values.length < 10) return;
    const recent = m.values.slice(-Math.min(20, m.values.length));
    const older = m.values.slice(-Math.min(40, m.values.length), -Math.min(20, m.values.length));
    if (older.length < 3 || recent.length < 3) return;
    const recentMean = mean(recent);
    const olderMean = mean(older);
    const pctChange = olderMean === 0 ? 0 : ((recentMean - olderMean) / olderMean) * 100;
    if (Math.abs(pctChange) > 10) {
      chain.push({
        id, label: m.label,
        change: pctChange,
        dir: pctChange > 0 ? 'spike' : 'drop',
        color: m.color,
        lag: 'preceded'  // simulated precedence
      });
    }
  });
  rootCauses = [{
    primary: {id: primary.id, label: primary.label, z: primary.z, color: primary.color},
    chain: chain.slice(0, 4)
  }];
}
// ─── Pulsing Rings ────────────────────────────────────────────────────────────
function spawnPulse(x, y, severity='crit') {
  if (!showPulse) return;
  const container = document.getElementById('pulse-container');
  const ring = document.createElement('div');
  ring.className = 'pulse-ring ' + severity;
  ring.style.left = x + 'px';
  ring.style.top = y + 'px';
  // Safari fallback: use -webkit- prefix, cap box-shadow at 6 layers, use outline for remaining 2
  const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  const shadowLayers = isSafari ? 6 : 8;
  let shadows = [];
  for (let i=0; i<shadowLayers; i++) {
    const r = 4 + i * 4;
    const alpha = 0.6 - i * 0.07;
    const color = severity === 'crit' ? `rgba(231,76,60,${alpha})` : severity === 'warn' ? `rgba(243,156,18,${alpha})` : `rgba(46,204,113,${alpha})`;
    shadows.push(`0 0 ${r}px ${r/2}px ${color}`);
  }
  ring.style.boxShadow = shadows.join(', ');
  if (isSafari && shadowLayers < 8) {
    ring.style.outline = `2px solid rgba(231,76,60,0.2)`;
    ring.style.outlineOffset = `${6 + shadowLayers * 4}px`;
  }
  container.appendChild(ring);
  setTimeout(() => ring.remove(), 2000);
}
// ─── Heatmap Rendering ───────────────────────────────────────────────────────
function renderHeatmap() {
  if (!heatmapCtx || !showHeatmap) return;
  const rect = heatmapCanvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const w = rect.width;
  const h = rect.height;
  if (w <= 0 || h <= 0) return;
  heatmapCanvas.width = w * dpr;
  heatmapCanvas.height = h * dpr;
  heatmapCanvas.style.width = w + 'px';
  heatmapCanvas.style.height = h + 'px';
  heatmapCtx.scale(dpr, dpr);
  heatmapW = w;
  heatmapH = h;
  // Check placeholder
  const hasData = METRICS.some(id => bus.get(id).values.length > 0);
  if (!hasData) {
    heatmapCtx.fillStyle = '#0d111e';
    heatmapCtx.fillRect(0,0,w,h);
    heatmapCtx.fillStyle = '#2a3a4a';
    heatmapCtx.font = '13px ' + getComputedStyle(document.body).fontFamily;
    heatmapCtx.textAlign = 'center';
    heatmapCtx.fillText('Awaiting stream...', w/2, h/2);
    return;
  }
  const cols = METRICS.length;
  const rows = Math.min(windowSize, Math.max(5, Math.floor(h / 16)));
  const cellW = w / cols;
  const cellH = h / rows;
  const labelH = 18;
  heatmapCtx.clearRect(0,0,w,h);
  heatmapCtx.fillStyle = '#0d111e';
  heatmapCtx.fillRect(0,0,w,h);
  // Draw heatmap cells
  METRICS.forEach((id, col) => {
    const m = bus.get(id);
    const vals = m.values.slice(-rows);
    const zs = m.zscores.slice(-rows);
    for (let row = 0; row < Math.min(rows, vals.length); row++) {
      const idx = vals.length - 1 - row;
      const val = vals[idx];
      const z = zs.length > idx ? Math.abs(zs[idx]) : 0;
      const severity = z > zThreshold ? 2 : z > zThreshold * 0.7 ? 1 : 0;
      // Color by severity
      let r, g, b;
      if (severity === 2) { r=231; g=76; b=60; }
      else if (severity === 1) { r=243; g=156; b=18; }
      else {
        const ratio = (val - METRIC_RANGES[0][0]) / (METRIC_RANGES[0][1] - METRIC_RANGES[0][0]);
        r = Math.round(30 + 30 * ratio);
        g = Math.round(60 + 60 * ratio);
        b = Math.round(120 + 60 * ratio);
      }
      const alpha = 0.3 + 0.7 * Math.min(1, z / (zThreshold * 2));
      const cx = col * cellW;
      const cy = labelH + row * cellH;
      heatmapCtx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
      heatmapCtx.fillRect(cx, cy, cellW - 1, cellH - 1);
      // Spawn pulse ring on new anomaly
      if (severity === 2 && idx === vals.length - 1) {
        const pulseX = cx + cellW / 2;
        const pulseY = cy + cellH / 2;
        const sev = z > zThreshold * 1.3 ? 'crit' : 'warn';
        spawnPulse(pulseX, pulseY, sev);
      }
    }
  });
  // Column labels
  heatmapCtx.fillStyle = '#5f7a9a';
  heatmapCtx.font = '10px ' + getComputedStyle(document.body).fontFamily;
  heatmapCtx.textAlign = 'center';
  heatmapCtx.textBaseline = 'top';
  METRICS.forEach((id, col) => {
    const m = bus.get(id);
    heatmapCtx.fillStyle = m.color;
    heatmapCtx.fillText(m.label, col * cellW + cellW/2, 2);
  });
  // Row labels (time ago)
  heatmapCtx.fillStyle = '#3a4a5a';
  heatmapCtx.font = '9px ' + getComputedStyle(document.body).fontFamily;
  heatmapCtx.textAlign = 'right';
  heatmapCtx.textBaseline = 'middle';
  for (let row = 0; row < Math.min(rows, 20); row += 2) {
    const secsAgo = row + 1;
    heatmapCtx.fillText('-' + secsAgo + 's', 0, labelH + row * cellH + cellH/2);
  }
}
// ─── Drift Rendering ──────────────────────────────────────────────────────────
function renderDrift() {
  if (!driftCtx || !showDrift) return;
  const rect = driftCanvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const w = rect.width;
  const h = rect.height;
  if (w <= 0 || h <= 0) return;
  driftCanvas.width = w * dpr;
  driftCanvas.height = h * dpr;
  driftCanvas.style.width = w + 'px';
  driftCanvas.style.height = h + 'px';
  driftCtx.scale(dpr, dpr);
  driftW = w;
  driftH = h;
  const m = bus.get('cpu_usage');
  const pred = bus.get('memory_usage'); // Use memory as "prediction" for drift visualization
  if (m.values.length < 3 || pred.values.length < 3) {
    driftCtx.fillStyle = '#0d111e';
    driftCtx.fillRect(0,0,w,h);
    driftCtx.fillStyle = '#2a3a4a';
    driftCtx.font = '11px ' + getComputedStyle(document.body).fontFamily;
    driftCtx.textAlign = 'center';
    driftCtx.fillText('Insufficient data for drift chart', w/2, h/2);
    return;
  }
  const padding = {top: 20, right: 16, bottom: 22, left: 50};
  const plotW = w - padding.left - padding.right;
  const plotH = h - padding.top - padding.bottom;
  const maxLen = Math.min(m.values.length, pred.values.length, windowSize + 10);
  const actualVals = m.values.slice(-maxLen);
  const predVals = pred.values.slice(-maxLen);
  const times = m.timestamps.slice(-maxLen);
  // Scale
  const minVal = Math.min(...actualVals, ...predVals);
  const maxVal = Math.max(...actualVals, ...predVals);
  const range = maxVal - minVal || 1;
  function tx(i) { return padding.left + (i / (maxLen - 1 || 1)) * plotW; }
  function ty(v) { return padding.top + plotH - ((v - minVal) / range) * plotH; }
  driftCtx.clearRect(0,0,w,h);
  driftCtx.fillStyle = '#0d111e';
  driftCtx.fillRect(0,0,w,h);
  // Background grid
  driftCtx.strokeStyle = '#1a2430';
  driftCtx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = padding.top + (i/4) * plotH;
    driftCtx.beginPath();
    driftCtx.moveTo(padding.left, y);
    driftCtx.lineTo(w - padding.right, y);
    driftCtx.stroke();
  }
  // Check for data gap
  let hasGap = false;
  if (times.length >= 2) {
    const lastGap = performance.now() - times[times.length - 1];
    if (lastGap > GAP_THRESHOLD_MS) {
      hasGap = true;
      if (!gapActive) {
        gapActive = true;
        gapStartTime = times[times.length - 1];
      }
    } else {
      gapActive = false;
    }
  }
  // Threshold bands (dynamic)
  const recentActual = actualVals.slice(-Math.min(20, actualVals.length));
  const bandStd = std(recentActual) || range * 0.05;
  const bandBase = mean(recentActual);
  driftCtx.fillStyle = 'rgba(46,204,113,0.06)';
  driftCtx.fillRect(padding.left, ty(bandBase + bandStd), plotW, ty(bandBase - bandStd) - ty(bandBase + bandStd));
  driftCtx.fillStyle = 'rgba(243,156,18,0.04)';
  driftCtx.fillRect(padding.left, ty(bandBase + 2*bandStd), plotW, ty(bandBase - 2*bandStd) - ty(bandBase + 2*bandStd));
  // Threshold lines
  driftCtx.setLineDash([3,3]);
  [1,2].forEach(mult => {
    driftCtx.strokeStyle = mult === 1 ? 'rgba(46,204,113,0.3)' : 'rgba(243,156,18,0.25)';
    driftCtx.lineWidth = 0.5;
    driftCtx.beginPath();
    driftCtx.moveTo(padding.left, ty(bandBase + mult*bandStd));
    driftCtx.lineTo(w - padding.right, ty(bandBase + mult*bandStd));
    driftCtx.stroke();
    driftCtx.beginPath();
    driftCtx.moveTo(padding.left, ty(bandBase - mult*bandStd));
    driftCtx.lineTo(w - padding.right, ty(bandBase - mult*bandStd));
    driftCtx.stroke();
  });
  driftCtx.setLineDash([]);
  // Draw drift fill (area between actual and predicted)
  for (let i = 0; i < maxLen - 1; i++) {
    const x0 = tx(i), x1 = tx(i+1);
    const a0 = ty(actualVals[i]), a1 = ty(actualVals[i+1]);
    const p0 = ty(predVals[i]), p1 = ty(predVals[i+1]);
    const drift0 = actualVals[i] - predVals[i];
    const drift1 = actualVals[i+1] - predVals[i+1];
    const color = drift0 > 0 ? 'rgba(231,76,60,0.15)' : 'rgba(46,204,113,0.15)';
    driftCtx.fillStyle = color;
    driftCtx.beginPath();
    driftCtx.moveTo(x0, a0);
    driftCtx.lineTo(x1, a1);
    driftCtx.lineTo(x1, p1);
    driftCtx.lineTo(x0, p0);
    driftCtx.closePath();
    driftCtx.fill();
  }
  // Prediction line
  driftCtx.strokeStyle = '#5f7a9a';
  driftCtx.lineWidth = 1.5;
  driftCtx.setLineDash([4,3]);
  driftCtx.beginPath();
  predVals.forEach((v,i) => { i===0 ? driftCtx.moveTo(tx(i),ty(v)) : driftCtx.lineTo(tx(i),ty(v)); });
  driftCtx.stroke();
  // Data gap dashed connector
  if (hasGap && times.length >= 2) {
    const lastIdx = times.length - 1;
    const prevIdx = lastIdx - 1;
    driftCtx.strokeStyle = 'rgba(95,122,154,0.6)';
    driftCtx.lineWidth = 1.5;
    driftCtx.setLineDash([6,4]);
    driftCtx.beginPath();
    driftCtx.moveTo(tx(prevIdx), ty(actualVals[prevIdx]));
    driftCtx.lineTo(tx(lastIdx), ty(actualVals[lastIdx]));
    driftCtx.stroke();
    driftCtx.setLineDash([]);
    // Gap annotation
    driftCtx.fillStyle = 'rgba(95,122,154,0.7)';
    driftCtx.font = '9px ' + getComputedStyle(document.body).fontFamily;
    driftCtx.textAlign = 'center';
    driftCtx.fillText('— Data gap — interpolation paused —', tx(lastIdx), ty(actualVals[lastIdx]) - 10);
  }
  // Actual line
  driftCtx.strokeStyle = '#3498db';
  driftCtx.lineWidth = 2;
  driftCtx.setLineDash([]);
  driftCtx.beginPath();
  actualVals.forEach((v,i) => { i===0 ? driftCtx.moveTo(tx(i),ty(v)) : driftCtx.lineTo(tx(i),ty(v)); });
  driftCtx.stroke();
  // Anomaly markers on drift
  actualVals.forEach((v,i) => {
    const z = m.zscores[m.zscores.length - maxLen + i];
    if (z !== undefined && Math.abs(z) > zThreshold) {
      const isRecent = i >= maxLen - 3;
      driftCtx.fillStyle = isRecent ? '#e74c3c' : 'rgba(231,76,60,0.5)';
      driftCtx.beginPath();
      driftCtx.arc(tx(i), ty(v), isRecent ? 5 : 3, 0, Math.PI*2);
      driftCtx.fill();
      if (isRecent) {
        driftCtx.strokeStyle = 'rgba(231,76,60,0.3)';
        driftCtx.lineWidth = 2;
        driftCtx.beginPath();
        driftCtx.arc(tx(i), ty(v), 12, 0, Math.PI*2);
        driftCtx.stroke();
      }
    }
  });
  // Labels
  driftCtx.fillStyle = '#5f7a9a';
  driftCtx.font = '10px ' + getComputedStyle(document.body).fontFamily;
  driftCtx.textAlign = 'center';
  driftCtx.fillText('← time →', w/2, h - 4);
  driftCtx.textAlign = 'right';
  driftCtx.textBaseline = 'middle';
  driftCtx.font = '9px ' + getComputedStyle(document.body).fontFamily;
  driftCtx.fillStyle = '#3498db';
  driftCtx.fillText('actual', padding.left - 6, padding.top + plotH * 0.3);
  driftCtx.fillStyle = '#5f7a9a';
  driftCtx.fillText('predicted', padding.left - 6, padding.top + plotH * 0.7);
  // Axis labels
  driftCtx.fillStyle = '#3a4a5a';
  driftCtx.font = '9px ' + getComputedStyle(document.body).fontFamily;
  driftCtx.textAlign = 'left';
  driftCtx.textBaseline = 'bottom';
  driftCtx.fillText(Math.round(maxVal) + '%', padding.left + 2, padding.top + 10);
  driftCtx.textBaseline = 'top';
  driftCtx.fillText(Math.round(minVal) + '%', padding.left + 2, h - padding.bottom - 2);
}
// ─── Metrics Card Update ──────────────────────────────────────────────────────
function updateMetricsCards() {
  const grid = document.getElementById('metrics-grid');
  grid.innerHTML = '';
  let anomCount = 0;
  METRICS.forEach((id,i) => {
    const m = bus.get(id);
    const val = m.values.length > 0 ? m.values[m.values.length-1] : 0;
    const z = m.zscores.length > 0 ? m.zscores[m.zscores.length-1] : 0;
    const isAnom = Math.abs(z) > zThreshold;
    const card = document.createElement('div');
    card.className = 'metric-card';
    if (isAnom) anomCount++;
    const valClass = isAnom ? 'alert' : Math.abs(z) > zThreshold * 0.7 ? 'warn' : 'good';
    const displayVal = m.unit === '%' ? val.toFixed(1) : val.toFixed(0);
    card.innerHTML = `
      <div class="name">${m.label} <span style="color:${m.color}">&#9679;</span></div>
      <div class="value ${valClass}">${displayVal}<span style="font-size:11px;color:var(--dim);font-weight:400;margin-left:2px">${m.unit}</span></div>
      <div class="zscore">z=${z.toFixed(2)} ${isAnom ? '⚠' : ''}</div>
      <div class="anomaly-badge ${isAnom ? 'show' : ''}">ANOM</div>
      <div class="spark-mini"><canvas data-metric="${id}"></canvas></div>
    `;
    grid.appendChild(card);
    // Sparkline
    const canvas = card.querySelector('canvas');
    const spCtx = canvas.getContext('2d');
    const spW = canvas.parentElement.offsetWidth || 120;
    const spH = 20;
    canvas.width = spW;
    canvas.height = spH;
    const recent = m.values.slice(-40);
    if (recent.length < 2) return;
    const spMin = Math.min(...recent);
    const spMax = Math.max(...recent);
    const spRange = spMax - spMin || 1;
    spCtx.strokeStyle = isAnom ? '#e74c3c' : m.color;
    spCtx.lineWidth = 1.5;
    spCtx.beginPath();
    recent.forEach((v,j) => {
      const x = (j / (recent.length-1)) * spW;
      const y = spH - ((v - spMin) / spRange) * (spH - 4) - 2;
      j === 0 ? spCtx.moveTo(x,y) : spCtx.lineTo(x,y);
    });
    spCtx.stroke();
  });
  document.getElementById('metric-count').textContent = METRICS.length;
  document.getElementById('cause-count').textContent = anomCount;
  document.getElementById('status-dot').className = 'status-dot' + (anomCount > 2 ? ' alert' : anomCount > 0 ? ' warn' : '');
}
// ─── Stream Stats ─────────────────────────────────────────────────────────────
function updateStreamStats() {
  const stats = document.getElementById('stream-stats');
  const total = METRICS.reduce((s,id) => s + bus.get(id).values.length, 0);
  const lastTick = METRICS.map(id => bus.get(id).values[bus.get(id).values.length-1] || 0);
  const anomNow = lastTick.filter((v,i) => {
    const m = bus.get(METRICS[i]);
    const z = m.zscores.length > 0 ? m.zscores[m.zscores.length-1] : 0;
    return Math.abs(z) > zThreshold;
  }).length;
  stats.innerHTML = `
    <span>Total points <b>${total.toLocaleString()}</b></span>
    <span>Streaming <b>${streaming ? (paused ? 'paused' : 'active') : 'stopped'}</b></span>
    <span>Window <b>${windowSize}</b></span>
    <span>Anomalies now <b style="color:${anomNow > 0 ? '#e74c3c' : '#2ecc71'}">${anomNow}</b></span>
    <span>Threshold <b>z=${zThreshold.toFixed(1)}</b></span>
    <span>Tick <b>#${tickCount}</b></span>
  `;
}
// ─── Anomaly Log ──────────────────────────────────────────────────────────────
function updateAnomalyLog() {
  const log = document.getElementById('anomaly-log');
  if (anomalyHistory.length === 0) {
    log.innerHTML = '<div style="text-align:center;color:var(--dim);padding:20px;font-size:11px">No anomalies detected yet</div>';
    return;
  }
  const recent = anomalyHistory.slice(-50).reverse();
  log.innerHTML = recent.map((a, idx) => {
    const m = bus.get(a.metric);
    const timeAgo = ((performance.now() - a.time) / 1000).toFixed(0);
    return `<div style="padding:4px 0;border-bottom:1px solid rgba(30,42,58,0.4);font-size:10px;display:flex;justify-content:space-between">
      <span><span style="color:${m ? m.color : '#e74c3c'}">${m ? m.label : a.metric}</span> z=${a.z.toFixed(2)}</span>
      <span style="color:var(--dim)">-${timeAgo}s</span>
    </div>`;
  }).join('');
}
// ─── Root Cause Panel ─────────────────────────────────────────────────────────
function updateRootCauses() {
  computeRootCauses();
  const panel = document.getElementById('root-cause-panel');
  if (rootCauses.length === 0) {
    panel.innerHTML = '<div style="color:var(--dim);font-size:11px;padding:4px">No correlated shifts detected</div>';
    return;
  }
  panel.innerHTML = rootCauses.map(rc => {
    const chainHtml = rc.chain.map(c => `
      <div class="cause-chain">
        <span style="color:${c.color}">${c.label}</span>
        <span class="cause-dir ${c.dir}">${c.dir === 'spike' ? '↑' : '↓'} ${Math.abs(c.change).toFixed(0)}%</span>
        <span class="arrow">→</span>
        <span style="color:var(--dim)">${c.lag}</span>
      </div>
    `).join('');
    return `
      <div class="cause-item">
        <span style="color:${rc.primary.color}" class="cause-metric">${rc.primary.label}</span>
        <span style="color:var(--red);font-weight:700">z=${rc.primary.z.toFixed(2)}</span>
      </div>
      ${chainHtml}
    `;
  }).join('');
}
// ─── Main Loop ────────────────────────────────────────────────────────────────
function simulationTick() {
  if (!streaming || paused) return;
  // Simulate data gap occasionally
  if (Math.random() < 0.005 && !gapActive) {
    // Skip this tick to create a gap
    setTimeout(simulationTick, 200);
    return;
  }
  const data = generateTick(tickCount);
  ingest(data);
  updateMetricsCards();
  updateStreamStats();
  updateAnomalyLog();
  updateRootCauses();
  const hasData = METRICS.some(id => bus.get(id).values.length > 0);
  document.getElementById('placeholder-state').style.display = hasData ? 'none' : 'flex';
  document.getElementById('header-sub').textContent = hasData
    ? tickCount + ' ticks | ' + anomalyHistory.length + ' anomalies'
    : 'awaiting stream...';
  // Schedule next tick
  setTimeout(simulationTick, 1000);
}
// ─── Render Loop (RAF) ────────────────────────────────────────────────────────
function renderLoop(timestamp) {
  if (showHeatmap) renderHeatmap();
  if (showDrift) renderDrift();
  animFrameId = requestAnimationFrame(renderLoop);
}
// ─── Resize ────────────────────────────────────────────────────────────────────
function handleResize() {
  if (showHeatmap) renderHeatmap();
  if (showDrift) renderDrift();
}
// ─── Tooltip ───────────────────────────────────────────────────────────────────
const tooltipEl = document.getElementById('tooltip');
const tooltipContent = document.getElementById('tooltip-content');
document.addEventListener('mousemove', (e) => {
  if (!driftCtx) return;
  const rect = driftCanvas.getBoundingClientRect();
  if (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom && showDrift) {
    const relX = e.clientX - rect.left;
    const relY = e.clientY - rect.top;
    const padding = {top:20,left:50,right:16,bottom:22};
    const plotW = rect.width - padding.left - padding.right;
    const plotH = rect.height - padding.top - padding.bottom;
    if (relX < padding.left || relX > rect.width - padding.right || relY < padding.top || relY > rect.height - padding.bottom) {
      tooltipEl.classList.remove('visible');
      return;
    }
    const dataIdx = Math.round(((relX - padding.left) / plotW) * (windowSize - 1));
    const m = bus.get('cpu_usage');
    if (m.values.length > 0 && dataIdx >= 0 && dataIdx < m.values.length) {
      const idx = Math.max(0, m.values.length - 1 - dataIdx);
      const val = m.values[idx] || 0;
      const z = m.zscores[idx] !== undefined ? m.zscores[idx] : 0;
      const isAnom = Math.abs(z) > zThreshold;
      tooltipContent.innerHTML = `
        <div class="tt-label">CPU Usage</div>
        <div class="tt-val">${val.toFixed(1)}%</div>
        <div class="tt-z">z-score: ${z.toFixed(3)}</div>
        ${isAnom ? '<div class="tt-anom">⚠ ANOMALY</div>' : ''}
      `;
      tooltipEl.style.left = (e.clientX + 14) + 'px';
      tooltipEl.style.top = (e.clientY - 10) + 'px';
      tooltipEl.classList.add('visible');
    } else {
      tooltipEl.classList.remove('visible');
    }
  } else {
    tooltipEl.classList.remove('visible');
  }
});
// ─── Init ─────────────────────────────────────────────────────────────────────-
window.addEventListener('DOMContentLoaded', () => {
  heatmapCanvas = document.getElementById('heatmap-canvas');
  heatmapCtx = heatmapCanvas.getContext('2d');
  driftCanvas = document.getElementById('drift-canvas');
  driftCtx = driftCanvas.getContext('2d');
  // Controls
  document.getElementById('btn-stream').addEventListener('click', () => {
    streaming = !streaming;
    if (streaming) paused = false;
    document.getElementById('btn-stream').classList.toggle('active');
    document.getElementById('btn-stream').textContent = streaming ? 'Stream' : 'Stop';
    if (streaming) simulationTick();
  });
  document.getElementById('btn-pause').addEventListener('click', () => {
    paused = !paused;
    document.getElementById('btn-pause').classList.toggle('active');
    document.getElementById('btn-pause').textContent = paused ? 'Resume' : 'Pause';
  });
  document.getElementById('btn-reset').addEventListener('click', () => {
    METRICS.forEach(id => {
      const m = bus.get(id);
      m.values = []; m.timestamps = []; m.zscores = []; m.anomalies = []; m.iqrLower = []; m.iqrUpper = [];
    });
    tickCount = 0; anomalyHistory = []; rootCauses = []; gapActive = false; noDataCycles = 0;
    document.getElementById('placeholder-state').style.display = 'flex';
    document.getElementById('header-sub').textContent = 'awaiting stream...';
    updateMetricsCards();
    updateStreamStats();
    updateAnomalyLog();
    updateRootCauses();
  });
  document.getElementById('slider-window').addEventListener('input', (e) => {
    windowSize = parseInt(e.target.value);
    bus.forEach(m => m.window = windowSize);
    updateStreamStats();
  });
  document.getElementById('slider-threshold').addEventListener('input', (e) => {
    zThreshold = parseFloat(e.target.value);
    updateStreamStats();
  });
  document.getElementById('btn-toggle-heatmap').addEventListener('click', () => {
    showHeatmap = !showHeatmap;
    document.getElementById('btn-toggle-heatmap').classList.toggle('active');
    document.getElementById('heatmap-wrap').style.display = showHeatmap ? 'block' : 'none';
  });
  document.getElementById('btn-toggle-drift').addEventListener('click', () => {
    showDrift = !showDrift;
    document.getElementById('btn-toggle-drift').classList.toggle('active');
    document.getElementById('drift-wrap').style.display = showDrift ? 'block' : 'none';
  });
  document.getElementById('btn-toggle-pulse').addEventListener('click', () => {
    showPulse = !showPulse;
    document.getElementById('btn-toggle-pulse').classList.toggle('active');
  });
  window.addEventListener('resize', handleResize);
  // Startup
  simulationTick();
  renderLoop();
});
</script>
</body>
</html>
```