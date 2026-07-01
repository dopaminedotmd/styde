<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0b0e14;
  --surface:#131820;
  --surface2:#1a2332;
  --border:#2a3650;
  --text:#d0d8e8;
  --text-dim:#6a7a90;
  --green:#22c55e;
  --red:#ef4444;
  --amber:#f59e0b;
  --blue:#3b82f6;
  --purple:#8b5cf6;
  --pulse-color:#ef444488;
  --font:'Inter','SF Pro','Segoe UI',system-ui,sans-serif;
}
body{background:var(--bg);color:var(--text);font-family:var(--font);padding:20px;min-height:100vh}
.dashboard{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:20px}
header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:var(--surface);border:1px solid var(--border);border-radius:12px}
header h1{font-size:18px;font-weight:600;letter-spacing:-0.3px}
header .status-bar{display:flex;gap:16px;font-size:13px;color:var(--text-dim)}
header .status-bar .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.dot.green{background:var(--green);box-shadow:0 0 8px var(--green)}
.dot.red{background:var(--red);box-shadow:0 0 8px var(--red)}
.dot.amber{background:var(--amber);box-shadow:0 0 8px var(--amber)}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;position:relative}
.card h2{font-size:14px;font-weight:500;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:12px}
.card-full{grid-column:1/-1}
/* Pulse container */
.pulse-container{position:relative;height:120px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.pulse-ring{position:absolute;width:60px;height:60px;border-radius:50%;border:2px solid var(--pulse-color);animation:pulse 2s ease-out infinite;pointer-events:none}
.pulse-ring:nth-child(2){animation-delay:0.6s}
.pulse-ring:nth-child(3){animation-delay:1.2s}
@keyframes pulse{0%{transform:scale(0.3);opacity:1}100%{transform:scale(3);opacity:0}}
.pulse-center{width:14px;height:14px;border-radius:50%;background:var(--red);box-shadow:0 0 20px var(--red),0 0 40px var(--red);z-index:2}
.pulse-label{position:absolute;bottom:8px;font-size:12px;color:var(--red);font-weight:500}
/* Safari fallback: max 6 box-shadow layers, outline for rest */
@supports (-webkit-touch-callout: none) {
  .pulse-center{box-shadow:0 0 20px var(--red),0 0 40px var(--red),0 0 60px var(--red),0 0 80px var(--red),0 0 100px var(--red),0 0 120px var(--red);outline:6px solid rgba(239,68,68,0.2);outline-offset:20px}
}
/* Heatmap */
.heatmap-grid{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-bottom:12px}
.heatmap-cell{aspect-ratio:1;border-radius:3px;position:relative;cursor:pointer;transition:opacity 0.15s}
.heatmap-cell:hover{opacity:0.7}
.heatmap-cell .tooltip{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:6px 10px;font-size:11px;white-space:nowrap;z-index:10;pointer-events:none}
.heatmap-cell:hover .tooltip{display:block}
.heatmap-legend{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--text-dim);margin-top:8px}
.heatmap-legend .bar{display:flex;height:10px;border-radius:3px;overflow:hidden;flex:1;max-width:200px}
.heatmap-legend .bar span{flex:1}
.heatmap-placeholder{height:180px;display:flex;align-items:center;justify-content:center;background:var(--surface2);border-radius:8px;color:var(--text-dim);font-size:14px;letter-spacing:1px}
/* Drift chart */
.drift-chart{position:relative;height:200px;margin-top:8px}
.drift-chart svg{width:100%;height:100%}
.drift-legend{display:flex;gap:16px;font-size:12px;margin-top:8px;flex-wrap:wrap}
.drift-legend span{display:flex;align-items:center;gap:6px}
.drift-legend .swatch{width:12px;height:3px;border-radius:2px}
/* Threshold bands */
.threshold-band{fill-opacity:0.08}
.threshold-line{stroke-dasharray:4 3;stroke-width:1}
/* Root cause chains */
.cause-chain{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:12px;padding:12px;background:var(--surface2);border-radius:8px;font-size:13px}
.cause-chain .node{padding:4px 10px;background:var(--surface);border:1px solid var(--border);border-radius:20px;font-size:12px}
.cause-chain .node.primary{border-color:var(--red);color:var(--red)}
.cause-chain .node.secondary{border-color:var(--amber);color:var(--amber)}
.cause-chain .arrow{color:var(--text-dim);font-size:14px}
/* Metrics row */
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.metric-card{background:var(--surface2);border-radius:8px;padding:12px;text-align:center}
.metric-card .value{font-size:28px;font-weight:700;letter-spacing:-0.5px;margin-bottom:2px}
.metric-card .label{font-size:11px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px}
.metric-card .change{font-size:12px;margin-top:4px}
.change.up{color:var(--red)}
.change.down{color:var(--green)}
.change.flat{color:var(--text-dim)}
/* Data gap message */
.drift-gap{fill:none;stroke:var(--text-dim);stroke-width:1.5;stroke-dasharray:6 4;animation:dash-flow 1s linear infinite}
@keyframes dash-flow{to{stroke-dashoffset:-10}}
/* Loading state */
.awaiting-state{height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:var(--surface2);border-radius:8px}
.awaiting-state .icon{font-size:40px;opacity:0.3}
.awaiting-state .text{font-size:16px;color:var(--text-dim);letter-spacing:2px}
.awaiting-state .spinner{width:24px;height:24px;border:2px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:900px){.dashboard{grid-template-columns:1fr}.metrics-row{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<div class="dashboard" id="dashboard">
<header>
  <h1>Anomaly Detection Dashboard</h1>
  <div class="status-bar">
    <span><span class="dot green"></span>Streaming</span>
    <span>Points: <strong id="pointCount">847</strong></span>
    <span>Anomalies: <strong id="anomalyCount">3</strong></span>
    <span id="recencyBadge" style="color:var(--green)">Now</span>
  </div>
</header>
<div class="card">
  <h2>Pulse Alerts — Active Anomalies</h2>
  <div class="pulse-container" id="pulseContainer">
    <div class="pulse-ring"></div>
    <div class="pulse-ring"></div>
    <div class="pulse-ring"></div>
    <div class="pulse-center"></div>
    <div class="pulse-label">+3.2 sigma at t-12s</div>
  </div>
</div>
<div class="card">
  <h2>Key Metrics</h2>
  <div class="metrics-row">
    <div class="metric-card">
      <div class="value" style="color:var(--red)">1,284</div>
      <div class="label">Latency (ms)</div>
      <div class="change up">+22.4%</div>
    </div>
    <div class="metric-card">
      <div class="value" style="color:var(--green)">99.2</div>
      <div class="label">Success Rate %</div>
      <div class="change down">-0.4%</div>
    </div>
    <div class="metric-card">
      <div class="value" style="color:var(--text)">342</div>
      <div class="label">Throughput req/s</div>
      <div class="change flat">+1.1%</div>
    </div>
    <div class="metric-card">
      <div class="value" style="color:var(--amber)">0.12</div>
      <div class="label">Error Rate %</div>
      <div class="change up">+0.09</div>
    </div>
  </div>
</div>
<div class="card card-full">
  <h2>Deviation Heatmap — Last 24 Slots (z-score severity)</h2>
  <div class="heatmap-grid" id="heatmapGrid"></div>
  <div class="heatmap-legend">
    <span>-3</span>
    <div class="bar">
      <span style="background:#3b82f6"></span>
      <span style="background:#22c55e"></span>
      <span style="background:#f59e0b"></span>
      <span style="background:#ef4444"></span>
      <span style="background:#7c2d12"></span>
    </div>
    <span>+3</span>
  </div>
</div>
<div class="card card-full">
  <h2>Drift Chart — Prediction vs Actual</h2>
  <div class="drift-chart" id="driftChart"></div>
  <div class="drift-legend">
    <span><span class="swatch" style="background:var(--blue)"></span>Predicted</span>
    <span><span class="swatch" style="background:var(--green)"></span>Actual</span>
    <span><span class="swatch" style="background:var(--text-dim);stroke-dasharray:4 3"></span>Dynamic Threshold</span>
    <span><span class="swatch" style="background:var(--red)"></span>Anomaly</span>
  </div>
</div>
<div class="card card-full">
  <h2>Root-Cause Suggestion — Causal Chain</h2>
  <div class="cause-chain" id="causeChain">
    <span class="node primary">CPU 98%</span>
    <span class="arrow">→</span>
    <span class="node secondary">GC Pause 640ms</span>
    <span class="arrow">→</span>
    <span class="node secondary">Queue Depth 2,300</span>
    <span class="arrow">→</span>
    <span class="node primary">Latency +22%</span>
    <span style="margin-left:auto;font-size:11px;color:var(--text-dim)">Confidence: 87%</span>
  </div>
</div>
<div class="card card-full" style="display:none" id="awaitingCard">
  <h2>Heatmap — Deviation View</h2>
  <div class="awaiting-state">
    <div class="spinner"></div>
    <div class="icon">◉</div>
    <div class="text">Awaiting stream...</div>
  </div>
</div>
</div>
<script>
// ─── Configuration ───
const MAX_POINTS = 10000;
const DOWNSAMPLE_TARGET = 2000;
const LINE_CUTOFF = 796;
const GAP_THRESHOLD_MS = 3000;
// ─── State ───
let metricHistory = [];
let anomalyTimes = [];
// ─── Generate sample data ───
function generateSampleData(count) {
  const data = [];
  let t = Date.now() - count * 1000;
  let trend = 50;
  for (let i = 0; i < count; i++) {
    t += 1000;
    trend += (Math.random() - 0.48) * 2;
    const noise = (Math.random() - 0.5) * 12;
    const spike = (i === count - 15 || i === count - 8 || i === count - 3) ? 28 : 0;
    const val = Math.max(0, trend + noise + spike);
    const pred = trend + (Math.random() - 0.5) * 4;
    data.push({ t, val, pred, anomaly: spike > 0 });
    if (spike > 0) anomalyTimes.push({ t, val, severity: 3.2 });
  }
  return data;
}
function downsample(data, target) {
  if (data.length <= target) return data;
  const step = Math.ceil(data.length / target);
  return data.filter((_, i) => i % step === 0).slice(0, target);
}
// ─── Z-score detection ───
function computeZScores(data, windowSize) {
  const scores = [];
  for (let i = 0; i < data.length; i++) {
    if (i < windowSize) { scores.push(0); continue; }
    const window = data.slice(i - windowSize, i).map(d => d.val);
    const mean = window.reduce((a, b) => a + b, 0) / window.length;
    const std = Math.sqrt(window.reduce((s, v) => s + (v - mean) ** 2, 0) / window.length) || 1;
    scores.push((data[i].val - mean) / std);
  }
  return scores;
}
// ─── Moving IQR ───
function computeIQR(data, windowSize) {
  const iqrs = [];
  for (let i = 0; i < data.length; i++) {
    if (i < windowSize) { iqrs.push(0); continue; }
    const window = data.slice(i - windowSize, i).map(d => d.val).sort((a, b) => a - b);
    const q1 = window[Math.floor(window.length * 0.25)];
    const q3 = window[Math.floor(window.length * 0.75)];
    const med = window[Math.floor(window.length * 0.5)];
    const iqr = q3 - q1 || 1;
    iqrs.push((data[i].val - med) / (1.5 * iqr));
  }
  return iqrs;
}
// ─── Render heatmap ───
function renderHeatmap(data) {
  const grid = document.getElementById('heatmapGrid');
  grid.innerHTML = '';
  const recent = data.slice(-24);
  if (recent.length === 0) {
    grid.innerHTML = '<div class="heatmap-placeholder">Awaiting stream...</div>';
    return;
  }
  const zScores = computeZScores(data, 20).slice(-24);
  const colors = ['#3b82f6','#22c55e','#f59e0b','#ef4444','#7c2d12'];
  zScores.forEach((z, i) => {
    const cell = document.createElement('div');
    cell.className = 'heatmap-cell';
    let colorIdx = 0;
    if (z > 3) colorIdx = 4; else if (z > 2) colorIdx = 3;
    else if (z > 1) colorIdx = 2; else if (z < -2) colorIdx = 0;
    cell.style.background = colors[colorIdx];
    const d = recent[i] || { val: 0, t: Date.now() };
    const t = new Date(d.t);
    cell.innerHTML = `<div class="tooltip">${t.getHours()}:${String(t.getMinutes()).padStart(2,'0')} — ${d.val.toFixed(1)} (z=${z.toFixed(2)})</div>`;
    grid.appendChild(cell);
  });
}
// ─── Render drift chart ───
function renderDriftChart(data) {
  const svg = document.querySelector('#driftChart svg') || document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('viewBox','0 0 800 200');
  const W = 800, H = 200;
  const pad = { top: 10, bottom: 30, left: 50, right: 20 };
  const iw = W - pad.left - pad.right;
  const ih = H - pad.top - pad.bottom;
  const visible = data.slice(-60);
  if (visible.length < 2) {
    svg.innerHTML = `<text x="${W/2}" y="${H/2}" fill="#6a7a90" font-size="14" text-anchor="middle">Awaiting stream...</text>`;
    document.querySelector('#driftChart').appendChild(svg);
    return;
  }
  const allVals = visible.flatMap(d => [d.val, d.pred]);
  const minV = Math.min(...allVals) - 10;
  const maxV = Math.max(...allVals) + 10;
  const scaleX = (i) => (i / (visible.length - 1)) * iw + pad.left;
  const scaleY = (v) => pad.top + ih - ((v - minV) / (maxV - minV)) * ih;
  // Compute dynamic threshold bands
  const vals = visible.map(d => d.val);
  const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
  const std = Math.sqrt(vals.reduce((s, v) => s + (v - mean) ** 2, 0) / vals.length) || 1;
  const band = std * 2.5;
  let html = '';
  // Threshold band
  html += `<polygon class="threshold-band" fill="var(--amber)" points="`;
  visible.forEach((d, i) => { html += `${scaleX(i)},${scaleY(d.pred + band)} `; });
  visible.slice().reverse().forEach((d, i) => { html += `${scaleX(visible.length-1-i)},${scaleY(d.pred - band)} `; });
  html += `" />`;
  // Threshold lines
  html += `<polyline class="threshold-line" stroke="var(--amber)" fill="none" stroke-dasharray="4 3" points="`;
  visible.forEach((d, i) => { html += `${scaleX(i)},${scaleY(d.pred + band)} `; });
  html += `" />`;
  html += `<polyline class="threshold-line" stroke="var(--amber)" fill="none" stroke-dasharray="4 3" points="`;
  visible.forEach((d, i) => { html += `${scaleX(i)},${scaleY(d.pred - band)} `; });
  html += `" />`;
  // Check for data gaps
  let gapRendered = false;
  for (let i = 1; i < visible.length; i++) {
    if (visible[i].t - visible[i-1].t > GAP_THRESHOLD_MS) {
      const gx1 = scaleX(i-1), gx2 = scaleX(i);
      const gy = (scaleY(visible[i-1].val) + scaleY(visible[i].val)) / 2;
      html += `<line class="drift-gap" x1="${gx1}" y1="${scaleY(visible[i-1].val)}" x2="${gx2}" y2="${scaleY(visible[i].val)}" />`;
      html += `<rect x="${gx2-30}" y="${gy-18}" width="80" height="20" rx="4" fill="var(--surface2)" stroke="var(--border)" opacity="0.9" />`;
      html += `<text x="${gx2+10}" y="${gy-4}" fill="var(--text-dim)" font-size="9" text-anchor="middle">Data gap</text>`;
      gapRendered = true;
    }
  }
  // Predicted line
  html += `<polyline fill="none" stroke="var(--blue)" stroke-width="2" points="`;
  visible.forEach((d, i) => { html += `${scaleX(i)},${scaleY(d.pred)} `; });
  html += `" />`;
  // Actual line
  html += `<polyline fill="none" stroke="var(--green)" stroke-width="2" opacity="0.9" points="`;
  visible.forEach((d, i) => { html += `${scaleX(i)},${scaleY(d.val)} `; });
  html += `" />`;
  // Anomaly markers
  visible.forEach((d, i) => {
    if (d.anomaly) {
      html += `<circle cx="${scaleX(i)}" cy="${scaleY(d.val)}" r="6" fill="none" stroke="var(--red)" stroke-width="2" opacity="0.8">`;
      html += `<animate attributeName="r" values="4;8;4" dur="1.5s" repeatCount="indefinite" />`;
      html += `</circle>`;
      html += `<circle cx="${scaleX(i)}" cy="${scaleY(d.val)}" r="3" fill="var(--red)" />`;
    }
  });
  // Axis labels
  html += `<text x="${pad.left}" y="${scaleY(mean)}" fill="var(--text-dim)" font-size="10" text-anchor="end" dy="-4">${mean.toFixed(0)}</text>`;
  html += `<text x="${pad.left}" y="${scaleY(mean + band)}" fill="var(--amber)" font-size="9" text-anchor="end" dy="-3">+thr</text>`;
  html += `<text x="${pad.left}" y="${scaleY(mean - band)}" fill="var(--amber)" font-size="9" text-anchor="end" dy="12">-thr</text>`;
  // X-axis time labels
  const labelCount = Math.min(visible.length, 6);
  const step = Math.floor(visible.length / labelCount);
  for (let i = 0; i < labelCount; i++) {
    const idx = Math.min(i * step, visible.length - 1);
    const t = new Date(visible[idx].t);
    html += `<text x="${scaleX(idx)}" y="${H - 4}" fill="var(--text-dim)" font-size="9" text-anchor="middle">${t.getHours()}:${String(t.getMinutes()).padStart(2,'0')}:${String(t.getSeconds()).padStart(2,'0')}</text>`;
  }
  svg.innerHTML = html;
  document.querySelector('#driftChart').appendChild(svg);
}
// ─── Update dashboard ───
function updateDashboard() {
  const data = generateSampleData(200);
  metricHistory = downsample(data, DOWNSAMPLE_TARGET);
  document.getElementById('pointCount').textContent = metricHistory.length;
  document.getElementById('anomalyCount').textContent = anomalyTimes.length;
  renderHeatmap(metricHistory);
  renderDriftChart(metricHistory);
}
// ─── Simulate live streaming ───
let streamCount = 0;
let streamActive = false;
function streamTick() {
  streamCount++;
  if (streamCount < 3) {
    // Show awaiting state for first 3 ticks
    document.getElementById('awaitingCard').style.display = 'block';
    document.querySelector('.card-full:first-of-type').style.display = 'none';
    setTimeout(streamTick, 2000);
    return;
  }
  document.getElementById('awaitingCard').style.display = 'none';
  document.querySelector('.card-full:first-of-type').style.display = 'block';
  if (!streamActive) {
    streamActive = true;
    updateDashboard();
  }
  // Append new point
  const last = metricHistory[metricHistory.length - 1];
  if (last) {
    const t = Date.now();
    const trend = last.val + (Math.random() - 0.48) * 2;
    const spike = Math.random() < 0.03 ? 30 : 0;
    const val = Math.max(0, trend + (Math.random() - 0.5) * 8 + spike);
    metricHistory.push({ t, val, pred: trend + (Math.random() - 0.5) * 4, anomaly: spike > 0 });
    if (spike > 0) anomalyTimes.push({ t, val, severity: 3.0 + Math.random() });
    if (metricHistory.length > MAX_POINTS) {
      metricHistory = downsample(metricHistory, DOWNSAMPLE_TARGET);
    }
    document.getElementById('pointCount').textContent = metricHistory.length;
    document.getElementById('anomalyCount').textContent = anomalyTimes.length;
    renderHeatmap(metricHistory);
    renderDriftChart(metricHistory);
  }
  // Dynamic pulse rate based on anomaly recency
  const recentAnomaly = anomalyTimes.filter(a => Date.now() - a.t < 30000);
  const pulseSpeed = recentAnomaly.length > 0 ? 500 : 2000;
  setTimeout(streamTick, pulseSpeed);
}
// ─── Root cause chain updater ───
function updateCauseChain() {
  const chain = document.getElementById('causeChain');
  const causes = [
    { name: 'CPU 98%', cls: 'primary' },
    { name: 'GC Pause 640ms', cls: 'secondary' },
    { name: 'Queue Depth 2,300', cls: 'secondary' },
    { name: 'Connection Pool Exhausted', cls: 'secondary' },
    { name: 'Latency +22%', cls: 'primary' },
  ];
  const recentAnomalies = anomalyTimes.filter(a => Date.now() - a.t < 60000);
  if (recentAnomalies.length === 0) {
    chain.innerHTML = '<span style="color:var(--text-dim);font-size:12px">No active anomalies — causal chain idle</span>';
    return;
  }
  const conf = Math.min(95, 70 + recentAnomalies.length * 8);
  chain.innerHTML = causes.map((c, i) => {
    if (i > 0 && c.cls === 'primary') return `<span class="arrow">→</span><span class="node ${c.cls}">${c.name}</span>`;
    return `<span class="node ${c.cls}">${c.name}</span>`;
  }).join('') + `<span style="margin-left:auto;font-size:11px;color:var(--text-dim)">Confidence: ${conf}%</span>`;
}
// ─── Init ───
// Seed with gap example: inject a gap 3 data points back so the dash-line renders
const seed = generateSampleData(62);
seed[30].t += 4000; // Force a gap >3s
metricHistory = downsample(seed, DOWNSAMPLE_TARGET);
updateDashboard();
streamTick();
// Periodic cause chain refresh
setInterval(updateCauseChain, 5000);
updateCauseChain();
// Check line count for split warning
const docLen = document.documentElement.outerHTML.split('\n').length;
if (docLen > LINE_CUTOFF) {
  console.warn(`[Anomaly Dashboard] Main panel exceeds ${LINE_CUTOFF} lines (${docLen}). Consider moving detail overlays to a separate file.`);
}
</script>
</body>
</html>