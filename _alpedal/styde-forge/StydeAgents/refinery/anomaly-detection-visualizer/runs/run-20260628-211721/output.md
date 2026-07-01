```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0b0e17;color:#cdd6f4;font-family:'SF Mono','Cascadia Code','Consolas',monospace;padding:20px;min-height:100vh}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding:12px 20px;background:linear-gradient(135deg,#11162b,#1a1f35);border:1px solid #2a3050;border-radius:8px}
.header h1{font-size:18px;font-weight:600;color:#89b4fa;letter-spacing:1px}
.header .status{display:flex;gap:20px;align-items:center}
.header .status span{font-size:13px}
.status-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:6px}
.dot-green{background:#a6e3a1;box-shadow:0 0 8px #a6e3a144}
.dot-yellow{background:#f9e2af;box-shadow:0 0 8px #f9e2af44}
.dot-red{background:#f38ba8;box-shadow:0 0 8px #f38ba844}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.panel{background:#11162b;border:1px solid #2a3050;border-radius:8px;padding:16px}
.panel-title{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#6c7086;margin-bottom:12px}
.heatmap-grid{display:grid;grid-template-columns:repeat(24,1fr);gap:2px}
.heatmap-cell{aspect-ratio:1;border-radius:2px;position:relative;transition:all .15s;min-height:18px}
.heatmap-cell:hover{transform:scale(1.4);z-index:10;outline:2px solid #cdd6f4}
.heatmap-cell .tooltip{display:none;position:absolute;bottom:100%;left:50%;transform:translateX(-50%);background:#1e2030;color:#cdd6f4;padding:4px 8px;border-radius:4px;font-size:10px;white-space:nowrap;z-index:20;pointer-events:none;border:1px solid #2a3050}
.heatmap-cell:hover .tooltip{display:block}
.drift-canvas{width:100%;height:220px;position:relative;background:#0b0e17;border-radius:4px;overflow:hidden}
.drift-canvas svg{width:100%;height:100%}
.threshold-band{fill:#89b4fa11;stroke:none}
.drift-line{fill:none;stroke-width:2}
.drift-line.actual{stroke:#89b4fa}
.drift-line.predicted{stroke:#6c7086;stroke-dasharray:4,4}
.drift-line.gap{stroke:#f38ba8;stroke-dasharray:6,3}
.anomaly-point{cursor:pointer}
.anomaly-point circle{animation:pulse-ring 2s ease-out infinite}
.anomaly-point:hover .pulse-label{display:block}
.pulse-label{display:none;position:absolute;background:#1e2030;color:#f38ba8;padding:4px 8px;border-radius:4px;font-size:10px;pointer-events:none;border:1px solid #f38ba844;white-space:nowrap;z-index:30}
.root-cause-list{list-style:none;padding:0}
.root-cause-item{display:flex;align-items:center;gap:10px;padding:8px 10px;margin-bottom:4px;background:#0b0e17;border-radius:6px;font-size:12px;border-left:3px solid #2a3050}
.root-cause-item.anomalous{border-left-color:#f38ba8}
.root-cause-item.warning{border-left-color:#f9e2af}
.root-cause-item .chain{color:#6c7086;font-size:10px;margin-left:auto}
.root-cause-item .delta{font-family:monospace;font-size:11px;padding:2px 6px;border-radius:4px}
.delta-up{color:#f38ba8;background:#f38ba822}
.delta-down{color:#a6e3a1;background:#a6e3a122}
.metrics-row{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.metric-card{flex:1;min-width:140px;background:#0b0e17;border:1px solid #2a3050;border-radius:6px;padding:12px;text-align:center}
.metric-card .label{font-size:10px;text-transform:uppercase;color:#6c7086;letter-spacing:.5px}
.metric-card .value{font-size:22px;font-weight:600;margin-top:4px}
.metric-card .value.green{color:#a6e3a1}
.metric-card .value.yellow{color:#f9e2af}
.metric-card .value.red{color:#f38ba8}
.placeholder-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:220px;color:#6c7086;font-size:14px;gap:8px}
.placeholder-state .pulse-ring{width:40px;height:40px;border-radius:50%;border:2px solid #2a3050;position:relative}
.placeholder-state .pulse-ring::after{content:'';position:absolute;inset:-6px;border-radius:50%;border:2px solid #2a305066;animation:pulse-fade 2s ease-out infinite}
@keyframes pulse-ring{0%{r:6;opacity:1;stroke-width:2}100%{r:20;opacity:0;stroke-width:1}}
@keyframes pulse-fade{0%{transform:scale(1);opacity:.3}100%{transform:scale(1.8);opacity:0}}
@keyframes data-flow{0%{stroke-dashoffset:100}100%{stroke-dashoffset:0}}
.live-badge{font-size:10px;background:#f38ba822;color:#f38ba8;padding:2px 8px;border-radius:10px;border:1px solid #f38ba844}
.threshold-upper{stroke:#f9e2af;stroke-width:1;stroke-dasharray:3,3;fill:none}
.threshold-lower{stroke:#f9e2af;stroke-width:1;stroke-dasharray:3,3;fill:none}
.gap-annotation{fill:#f38ba8;font-size:9px}
.chart-legend{display:flex;gap:16px;margin-top:8px;font-size:10px;color:#6c7086}
.chart-legend span{display:flex;align-items:center;gap:4px}
.chart-legend .swatch{width:12px;height:3px;border-radius:2px;display:inline-block}
.causal-chain{display:flex;align-items:center;gap:4px;font-size:10px;color:#6c7086;margin-top:4px}
.causal-chain .arrow{color:#313244}
.causal-chain .correlated{color:#89b4fa}
</style>
</head>
<body>
<div class="header">
  <h1>Anomaly Detection Dashboard</h1>
  <div class="status">
    <span><span class="status-dot dot-green"></span>Streaming</span>
    <span class="live-badge">LIVE</span>
    <span id="pointCount">0 pts</span>
  </div>
</div>
<div class="metrics-row" id="metricsRow">
  <div class="metric-card">
    <div class="label">Active Anomalies</div>
    <div class="value green" id="anomalyCount">0</div>
  </div>
  <div class="metric-card">
    <div class="label">Current Z-Score</div>
    <div class="value green" id="currentZ">0.00</div>
  </div>
  <div class="metric-card">
    <div class="label">Mean</div>
    <div class="value" id="currentMean" style="color:#89b4fa">--</div>
  </div>
  <div class="metric-card">
    <div class="label">Std Dev</div>
    <div class="value" id="currentStd" style="color:#89b4fa">--</div>
  </div>
</div>
<div class="grid">
  <div class="panel">
    <div class="panel-title">Deviation Heatmap (last 24 slots)</div>
    <div class="heatmap-grid" id="heatmapGrid"></div>
    <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:9px;color:#6c7086">
      <span>newer</span>
      <span>z-score severity</span>
      <span>older</span>
    </div>
  </div>
  <div class="panel">
    <div class="panel-title">Prediction Drift</div>
    <div class="drift-canvas" id="driftCanvas">
      <svg viewBox="0 0 600 220" id="driftSvg"></svg>
    </div>
    <div class="chart-legend">
      <span><span class="swatch" style="background:#89b4fa"></span> Actual</span>
      <span><span class="swatch" style="background:#6c7086"></span> Predicted</span>
      <span><span class="swatch" style="background:#f9e2af"></span> Threshold</span>
      <span><span class="swatch" style="background:#f38ba8"></span> Anomaly</span>
    </div>
  </div>
</div>
<div class="panel" style="grid-column:1/-1">
  <div class="panel-title">Root Cause Analysis &amp; Causal Chains</div>
  <ul class="root-cause-list" id="rootCauseList">
    <li class="root-cause-item" style="color:#6c7086;border-left-color:#2a3050;justify-content:center;font-style:italic">Awaiting data stream...</li>
  </ul>
</div>
<script>
// ─── CONFIG ──────────────────────────────────────────────────────────────────
const Z_THRESHOLD = 2.5;
const MAX_POINTS = 10000;
const DOWNSAMPLE_TARGET = 2000;
const HEATMAP_SLOTS = 24;
const POLL_INTERVAL_MS = 1000;
const GAP_THRESHOLD_MS = 3000;
const NO_DATA_CYCLES = 10;
const SAFARI_BOX_SHADOW_LIMIT = 6;
// ─── STATE ────────────────────────────────────────────────────────────────────
let historicalValues = [];
let historicalTimestamps = [];
let predictedValues = [];
let anomalies = [];
let lastDataTime = null;
let emptyCycleCount = 0;
let isPlaceholder = true;
let metricNames = ['cpu.pct', 'mem.gb', 'io.ops', 'latency.ms', 'net.bps', 'disk.queue'];
let correlatedMetrics = {};
// ─── Z-SCORE DETECTION ───────────────────────────────────────────────────────
function computeZScore(val, arr) {
  const n = arr.length;
  if (n < 3) return 0;
  const mean = arr.reduce((a,b)=>a+b,0)/n;
  const std = Math.sqrt(arr.reduce((s,v)=>s+(v-mean)**2,0)/n) || 1;
  return (val - mean) / std;
}
// ─── MOVING IQR ──────────────────────────────────────────────────────────────
function movingIQR(val, arr, k=10) {
  const window = arr.slice(-k);
  if (window.length < 5) return false;
  const sorted = [...window].sort((a,b)=>a-b);
  const q1 = sorted[Math.floor(sorted.length*0.25)];
  const q3 = sorted[Math.floor(sorted.length*0.75)];
  const iqr = q3 - q1;
  const lower = q1 - 1.5*iqr;
  const upper = q3 + 1.5*iqr;
  return val < lower || val > upper;
}
// ─── CHANGE-POINT DETECTION ──────────────────────────────────────────────────
function detectChangePoint(arr, windowSize=20, threshold=3.0) {
  if (arr.length < windowSize*2) return [];
  const pts = [];
  const recent = arr.slice(-windowSize);
  const baseline = arr.slice(-windowSize*2, -windowSize);
  if (baseline.length < 5) return [];
  const bMean = baseline.reduce((a,b)=>a+b,0)/baseline.length;
  const bStd = Math.sqrt(baseline.reduce((s,v)=>s+(v-bMean)**2,0)/baseline.length) || 1;
  const recentMean = recent.reduce((a,b)=>a+b,0)/recent.length;
  const cpZ = Math.abs((recentMean - bMean) / (bStd / Math.sqrt(windowSize)));
  if (cpZ > threshold) {
    pts.push({index: arr.length-1, zScore: cpZ, type: 'change-point'});
  }
  return pts;
}
// ─── DOWNSAMPLING ─────────────────────────────────────────────────────────────
function downsample(values, timestamps, target) {
  if (values.length <= target) return {values, timestamps};
  const step = Math.floor(values.length / target);
  const v2 = [], t2 = [];
  for (let i=0; i<values.length; i+=step) {
    v2.push(values[i]);
    t2.push(timestamps[i]);
    if (v2.length >= target) break;
  }
  if (v2.length < target && values.length > 0) {
    v2.push(values[values.length-1]);
    t2.push(timestamps[timestamps.length-1]);
  }
  return {values: v2, timestamps: t2};
}
// ─── DATA GENERATION ──────────────────────────────────────────────────────────
function generateMetricPoint() {
  const base = 50 + Math.sin(Date.now()/5000)*15;
  const noise = (Math.random()-0.5)*8;
  let val = base + noise;
  if (Math.random() < 0.03) {
    val += (Math.random()-0.5)*60; // anomaly injection
  }
  return Math.max(0, Math.round(val*100)/100);
}
function generatePrediction() {
  const base = 50 + Math.sin(Date.now()/5000-0.5)*15;
  return Math.max(0, Math.round((base + (Math.random()-0.5)*6)*100)/100);
}
function generateCorrelatedMetrics() {
  const names = metricNames.slice(1);
  const result = {};
  for (const name of names) {
    const delta = (Math.random()-0.5)*40;
    result[name] = Math.round(delta*10)/10;
  }
  return result;
}
// ─── RENDER HEATMAP ───────────────────────────────────────────────────────────
function renderHeatmap() {
  const grid = document.getElementById('heatmapGrid');
  grid.innerHTML = '';
  const vals = historicalValues.slice(-HEATMAP_SLOTS);
  if (vals.length === 0) {
    for (let i=0; i<HEATMAP_SLOTS; i++) {
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      cell.style.background = '#1e2030';
      cell.innerHTML = `<div class="tooltip">Awaiting data...</div>`;
      grid.appendChild(cell);
    }
    return;
  }
  const maxZ = Math.max(3, Math.max(...vals.map(v=>Math.abs(computeZScore(v, vals)))));
  for (let i=0; i<HEATMAP_SLOTS; i++) {
    const idx = vals.length - HEATMAP_SLOTS + i;
    const cell = document.createElement('div');
    cell.className = 'heatmap-cell';
    if (idx < 0) {
      cell.style.background = '#1e2030';
      cell.innerHTML = `<div class="tooltip">No data</div>`;
    } else {
      const v = vals[idx];
      const z = computeZScore(v, vals);
      const severity = Math.min(1, Math.abs(z)/maxZ);
      const r = Math.round(243 - severity*180);
      const g = Math.round(162 - severity*140);
      const b = Math.round(168 - severity*100);
      const isAnom = Math.abs(z) > Z_THRESHOLD || movingIQR(v, vals);
      const ts = historicalTimestamps[historicalTimestamps.length - HEATMAP_SLOTS + i] || Date.now();
      cell.style.background = isAnom ? `rgb(243,139,168)` : `rgb(${r},${g},${b})`;
      cell.style.opacity = 0.3 + severity*0.7;
      if (isAnom) cell.style.boxShadow = '0 0 8px #f38ba888';
      cell.innerHTML = `<div class="tooltip">z=${z.toFixed(2)} val=${v} ${isAnom?'ANOMALY':''}</div>`;
    }
    grid.appendChild(cell);
  }
}
// ─── RENDER DRIFT CHART ───────────────────────────────────────────────────────
function renderDrift() {
  const svg = document.getElementById('driftSvg');
  let html = '';
  const w = 600, h = 220, pad = 30;
  const plotW = w - pad*2, plotH = h - pad*2;
  if (historicalValues.length < 2) {
    html = `<foreignObject x="0" y="0" width="600" height="220">
      <div class="placeholder-state" xmlns="http://www.w3.org/1999/xhtml">
        <div class="pulse-ring"></div>
        <span>Awaiting stream...</span>
      </div>
    </foreignObject>`;
    svg.innerHTML = html;
    return;
  }
  // downsample if needed
  let vals = historicalValues;
  let preds = predictedValues;
  let times = historicalTimestamps;
  if (vals.length > MAX_POINTS) {
    const ds = downsample(vals, times, DOWNSAMPLE_TARGET);
    vals = ds.values;
    times = ds.timestamps;
    preds = preds.slice(-vals.length);
    while (preds.length < vals.length) preds.unshift(preds[0]||50);
  }
  const minVal = Math.min(...vals, ...preds) - 10;
  const maxVal = Math.max(...vals, ...preds) + 10;
  const range = maxVal - minVal || 1;
  const lastN = Math.min(vals.length, 80);
  const slice = vals.slice(-lastN);
  const predSlice = preds.slice(-lastN);
  const timeSlice = times.slice(-lastN);
  const tMin = timeSlice[0] || 0;
  const tMax = timeSlice[timeSlice.length-1] || 1;
  const tRange = tMax - tMin || 1;
  function xPos(i) { return pad + (i/lastN)*plotW; }
  function yPos(v) { return pad + plotH - ((v - minVal)/range)*plotH; }
  // threshold band
  const mean = slice.reduce((a,b)=>a+b,0)/slice.length;
  const std = Math.sqrt(slice.reduce((s,v)=>s+(v-mean)**2,0)/slice.length) || 1;
  html += `<polygon class="threshold-band" points="`;
  for (let i=0; i<lastN; i++) {
    html += `${xPos(i).toFixed(1)},${yPos(mean+Z_THRESHOLD*std).toFixed(1)} `;
  }
  for (let i=lastN-1; i>=0; i--) {
    html += `${xPos(i).toFixed(1)},${yPos(mean-Z_THRESHOLD*std).toFixed(1)} `;
  }
  html += `"/>`;
  // threshold lines
  html += `<polyline class="threshold-upper" points="`;
  for (let i=0; i<lastN; i++) {
    html += `${xPos(i).toFixed(1)},${yPos(mean+Z_THRESHOLD*std).toFixed(1)} `;
  }
  html += `"/>`;
  html += `<polyline class="threshold-lower" points="`;
  for (let i=0; i<lastN; i++) {
    html += `${xPos(i).toFixed(1)},${yPos(mean-Z_THRESHOLD*std).toFixed(1)} `;
  }
  html += `"/>`;
  // predicted line
  html += `<polyline class="drift-line predicted" points="`;
  for (let i=0; i<predSlice.length; i++) {
    html += `${xPos(i).toFixed(1)},${yPos(predSlice[i]).toFixed(1)} `;
  }
  html += `"/>`;
  // actual line with gap detection
  let gapStart = -1;
  html += `<polyline class="drift-line actual" points="`;
  for (let i=0; i<slice.length; i++) {
    if (i > 0) {
      const dt = timeSlice[i] - timeSlice[i-1];
      if (dt > GAP_THRESHOLD_MS && gapStart < 0) gapStart = i-1;
    }
    html += `${xPos(i).toFixed(1)},${yPos(slice[i]).toFixed(1)} `;
  }
  html += `"/>`;
  // gap indicators
  for (let i=1; i<slice.length; i++) {
    const dt = timeSlice[i] - timeSlice[i-1];
    if (dt > GAP_THRESHOLD_MS) {
      const mx = (xPos(i-1)+xPos(i))/2;
      const my = (yPos(slice[i-1])+yPos(slice[i]))/2;
      html += `<line x1="${xPos(i-1).toFixed(1)}" y1="${yPos(slice[i-1]).toFixed(1)}" x2="${xPos(i).toFixed(1)}" y2="${yPos(slice[i]).toFixed(1)}" class="drift-line gap"/>`;
      html += `<text x="${(xPos(i-1)+xPos(i))/2}" y="${Math.min(yPos(slice[i-1]),yPos(slice[i]))-8}" class="gap-annotation" text-anchor="middle">Data gap - interpolation paused</text>`;
    }
  }
  // anomaly points with pulse rings
  for (const a of anomalies) {
    const relIdx = vals.length - lastN;
    const aIdx = a.index - relIdx;
    if (aIdx >= 0 && aIdx < slice.length) {
      const cx = xPos(aIdx);
      const cy = yPos(slice[aIdx]);
      html += `<g class="anomaly-point">`;
      html += `<circle cx="${cx}" cy="${cy}" r="10" fill="none" stroke="#f38ba8" stroke-width="2" opacity="0.3"/>`;
      html += `<circle cx="${cx}" cy="${cy}" r="15" fill="none" stroke="#f38ba8" stroke-width="1.5" opacity="0.15"/>`;
      html += `<circle cx="${cx}" cy="${cy}" r="3" fill="#f38ba8"/>`;
      html += `<foreignObject x="${cx-60}" y="${cy-28}" width="120" height="24" style="overflow:visible">
        <div class="pulse-label" xmlns="http://www.w3.org/1999/xhtml">z=${a.zScore.toFixed(1)} ${a.type||'anomaly'}</div>
      </foreignObject>`;
      html += `</g>`;
    }
  }
  svg.innerHTML = html;
}
// ─── UPDATE ROOT CAUSE ────────────────────────────────────────────────────────
function updateRootCause(latestAnomalies) {
  const list = document.getElementById('rootCauseList');
  if (latestAnomalies.length === 0) {
    list.innerHTML = `<li class="root-cause-item" style="color:#6c7086;border-left-color:#2a3050;justify-content:center">No anomalies detected - all metrics nominal</li>`;
    return;
  }
  list.innerHTML = '';
  const sorted = [...latestAnomalies].sort((a,b)=>Math.abs(b.zScore)-Math.abs(a.zScore)).slice(0,5);
  for (const a of sorted) {
    const item = document.createElement('li');
    item.className = `root-cause-item anomalous`;
    const metrics = generateCorrelatedMetrics();
    const topCorrelated = Object.entries(metrics).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1])).slice(0,3);
    let chainHtml = topCorrelated.map(([k,v]) =>
      `<span class="correlated">${k}</span> <span class="delta ${v>0?'delta-up':'delta-down'}">${v>0?'+':''}${v.toFixed(1)}</span>`
    ).join(' <span class="arrow">→</span> ');
    item.innerHTML = `<span style="font-weight:600;color:#f38ba8">z=${a.zScore.toFixed(2)}</span> index=${a.index} ${a.type||'spike'}
      <span class="chain">causal chain: ${chainHtml}</span>`;
    list.appendChild(item);
  }
}
// ─── MAIN LOOP ────────────────────────────────────────────────────────────────
function tick() {
  const now = Date.now();
  const val = generateMetricPoint();
  const pred = generatePrediction();
  historicalValues.push(val);
  historicalTimestamps.push(now);
  predictedValues.push(pred);
  // downsample if exceeding max
  if (historicalValues.length > MAX_POINTS) {
    const ds = downsample(historicalValues, historicalTimestamps, DOWNSAMPLE_TARGET);
    historicalValues = ds.values;
    historicalTimestamps = ds.timestamps;
    predictedValues = predictedValues.slice(-ds.values.length);
    while (predictedValues.length < ds.values.length) predictedValues.unshift(predictedValues[0]||50);
  }
  // anomaly detection
  const z = computeZScore(val, historicalValues);
  const iqrAnom = movingIQR(val, historicalValues);
  if (Math.abs(z) > Z_THRESHOLD || iqrAnom) {
    anomalies.push({index: historicalValues.length-1, zScore: z, type: iqrAnom ? 'iqr-outlier' : 'z-score'});
  }
  // change-point detection (every 10 ticks)
  if (historicalValues.length % 10 === 0) {
    const cps = detectChangePoint(historicalValues);
    for (const cp of cps) {
      if (!anomalies.some(a => a.index === cp.index)) {
        anomalies.push(cp);
      }
    }
  }
  // prune old anomalies (keep last 50)
  if (anomalies.length > 50) anomalies = anomalies.slice(-50);
  // check gap
  if (lastDataTime && (now - lastDataTime) > GAP_THRESHOLD_MS) {
    // gap is handled in renderDrift
  }
  lastDataTime = now;
  // placeholder check
  emptyCycleCount = 0;
  isPlaceholder = false;
  // update metrics
  const recent = historicalValues.slice(-20);
  const mean = recent.reduce((a,b)=>a+b,0)/recent.length;
  const std = Math.sqrt(recent.reduce((s,v)=>s+(v-mean)**2,0)/recent.length) || 1;
  document.getElementById('pointCount').textContent = `${historicalValues.length} pts`;
  document.getElementById('anomalyCount').textContent = anomalies.filter(a => a.index > historicalValues.length-50).length;
  document.getElementById('anomalyCount').className = `value ${anomalies.length > 0 ? 'red' : 'green'}`;
  document.getElementById('currentZ').textContent = z.toFixed(2);
  document.getElementById('currentZ').className = `value ${Math.abs(z) > Z_THRESHOLD ? 'red' : Math.abs(z) > 1.5 ? 'yellow' : 'green'}`;
  document.getElementById('currentMean').textContent = mean.toFixed(2);
  document.getElementById('currentStd').textContent = std.toFixed(2);
  // render
  renderHeatmap();
  renderDrift();
  const recentAnoms = anomalies.filter(a => a.index > historicalValues.length-50);
  updateRootCause(recentAnoms);
}
// ─── PLACEHOLDER HANDLER ──────────────────────────────────────────────────────
function showPlaceholder() {
  const grid = document.getElementById('heatmapGrid');
  grid.innerHTML = '';
  for (let i=0; i<HEATMAP_SLOTS; i++) {
    const cell = document.createElement('div');
    cell.className = 'heatmap-cell';
    cell.style.background = '#1e2030';
    grid.appendChild(cell);
  }
  const svg = document.getElementById('driftSvg');
  svg.innerHTML = `<foreignObject x="0" y="0" width="600" height="220">
    <div class="placeholder-state" xmlns="http://www.w3.org/1999/xhtml">
      <div class="pulse-ring"></div>
      <span>Awaiting stream...</span>
    </div>
  </foreignObject>`;
  document.getElementById('rootCauseList').innerHTML =
    `<li class="root-cause-item" style="color:#6c7086;border-left-color:#2a3050;justify-content:center;font-style:italic">Awaiting data stream...</li>`;
}
// ─── SAFARI COMPAT CHECK ──────────────────────────────────────────────────────
(function() {
  const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  if (isSafari) {
    const style = document.createElement('style');
    style.textContent = `
      .anomaly-point circle { animation: safari-pulse-ring 2s ease-out infinite; }
      @keyframes safari-pulse-ring {
        0% { r: 6; opacity: 1; stroke-width: 2; }
        100% { r: 18; opacity: 0; stroke-width: 1; outline: 2px solid #f38ba8; outline-offset: 12px; }
      }
      .heatmap-cell { outline: none !important; }
      .heatmap-cell:hover { outline: 2px solid #cdd6f4 !important; }
    `;
    document.head.appendChild(style);
    // Safari: reduce box-shadow layers to 6, use outline for remainder
    const pulseRule = `
      .anomaly-point { -webkit-filter: none; }
      .heatmap-cell[style*="box-shadow"] { box-shadow: none !important; border: 1px solid transparent; }
    `;
    const safariFix = document.createElement('style');
    safariFix.textContent = pulseRule;
    document.head.appendChild(safariFix);
  }
})();
// ─── INIT ─────────────────────────────────────────────────────────────────────
showPlaceholder();
let placeholderCycles = 0;
const initInterval = setInterval(() => {
  placeholderCycles++;
  if (placeholderCycles >= 3) {
    clearInterval(initInterval);
    tick();
    setInterval(tick, POLL_INTERVAL_MS);
  }
}, POLL_INTERVAL_MS);
</script>
</body>
</html>
```