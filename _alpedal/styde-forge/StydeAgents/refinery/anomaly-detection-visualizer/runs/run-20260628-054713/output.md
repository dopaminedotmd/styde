<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Visualizer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden;min-height:100vh}
.header{background:linear-gradient(135deg,#0f1a2e,#1a2a4a);padding:16px 24px;border-bottom:1px solid rgba(0,200,255,0.15);display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:18px;font-weight:600;color:#00d4ff;letter-spacing:1px}
.header .status{display:flex;align-items:center;gap:8px;font-size:13px}
.status-dot{width:8px;height:8px;border-radius:50%;background:#00ff88;animation:pulse-dot 1.5s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1;box-shadow:0 0 4px #00ff88}50%{opacity:0.4;box-shadow:0 0 12px #00ff88}}
.metrics-bar{display:flex;gap:24px;padding:12px 24px;background:#0d1525;border-bottom:1px solid rgba(255,255,255,0.04)}
.metric-card{display:flex;flex-direction:column;align-items:center;min-width:100px}
.metric-card .label{font-size:10px;text-transform:uppercase;color:#6b7b8d;letter-spacing:0.5px}
.metric-card .value{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums}
.metric-card .value.alert{color:#ff4757}
.metric-card .value.ok{color:#2ed573}
.metric-card .value.warn{color:#ffa502}
.metric-card .sub{font-size:11px;color:#4a5a6d;margin-top:2px}
.main-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px 24px}
@media(max-width:1024px){.main-grid{grid-template-columns:1fr}}
.panel{background:linear-gradient(180deg,#0f1a2e,#0a1220);border:1px solid rgba(0,200,255,0.1);border-radius:8px;overflow:hidden}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:8px 14px;background:rgba(0,200,255,0.04);border-bottom:1px solid rgba(0,200,255,0.06);font-size:12px;font-weight:600;color:#7f8fa6;text-transform:uppercase;letter-spacing:0.8px}
.panel-body{position:relative;width:100%;min-height:280px}
.panel-body canvas{display:block;width:100%;height:280px}
.controls{display:flex;gap:8px;align-items:center}
.controls button{background:rgba(0,200,255,0.08);border:1px solid rgba(0,200,255,0.15);color:#7f8fa6;padding:4px 12px;border-radius:4px;font-size:11px;cursor:pointer;transition:all 0.2s}
.controls button:hover{background:rgba(0,200,255,0.15);color:#00d4ff}
.controls button.active{background:rgba(0,200,255,0.2);color:#00d4ff;border-color:#00d4ff}
.heatmap-legend{display:flex;align-items:center;gap:4px;padding:4px 14px;font-size:10px;color:#4a5a6d;justify-content:flex-end}
.heatmap-legend .gradient{width:80px;height:8px;border-radius:2px;background:linear-gradient(90deg,#2ed573,#ffa502,#ff4757)}
.heatmap-legend span{margin:0 2px}
.root-cause-panel{grid-column:1/-1}
.root-cause-list{display:flex;gap:12px;padding:12px 14px;overflow-x:auto}
.root-cause-item{background:rgba(0,200,255,0.04);border:1px solid rgba(0,200,255,0.08);border-radius:6px;padding:8px 14px;min-width:180px;flex-shrink:0;display:flex;flex-direction:column;gap:2px}
.root-cause-item .rc-name{font-size:13px;font-weight:600}
.root-cause-item .rc-detail{font-size:11px;color:#6b7b8d;display:flex;justify-content:space-between}
.root-cause-item .rc-detail .rc-change{font-weight:600}
.root-cause-item .rc-detail .rc-change.pos{color:#ff4757}
.root-cause-item .rc-detail .rc-change.neg{color:#2ed573}
.root-cause-item .rc-bar{height:3px;border-radius:2px;margin-top:4px;background:linear-gradient(90deg,#2ed573,#ffa502,#ff4757);transition:width 0.3s}
.chain-link{color:#00d4ff;font-size:16px;margin:auto 0;opacity:0.5}
.tooltip{position:fixed;background:#1a2a4a;border:1px solid rgba(0,200,255,0.3);border-radius:6px;padding:8px 12px;font-size:12px;color:#c8d6e5;pointer-events:none;z-index:100;box-shadow:0 4px 20px rgba(0,0,0,0.5);opacity:0;transition:opacity 0.15s;max-width:220px}
.tooltip.visible{opacity:1}
.tooltip .tt-row{display:flex;justify-content:space-between;gap:12px;margin:2px 0}
.tooltip .tt-label{color:#6b7b8d}
.tooltip .tt-value{font-weight:600}
.tooltip .tt-value.alert{color:#ff4757}
.tooltip .tt-value.ok{color:#2ed573}
.tooltip .tt-value.warn{color:#ffa502}
.mode-selector{display:flex;gap:4px}
.mode-selector button{font-size:10px;padding:3px 8px}
</style>
</head>
<body>
<div class="header">
<h1>ANOMALY DETECTION VISUALIZER</h1>
<div class="status">
<span class="status-dot"></span>
<span id="streamStatus">Monitoring 6 metrics</span>
<span style="color:#4a5a6d;margin-left:12px">|</span>
<span id="anomalyCount" style="color:#ff4757;font-weight:600">0 anomalies</span>
<span style="color:#4a5a6d;margin-left:12px">|</span>
<span id="fpsDisplay" style="color:#6b7b8d;font-size:11px">60 fps</span>
</div>
</div>
<div class="metrics-bar" id="metricsBar"></div>
<div class="main-grid">
<div class="panel">
<div class="panel-header">
<span>Pulse Alerts</span>
<div class="mode-selector">
<button data-mode="zscore" class="active">Z-Score</button>
<button data-mode="iqr">Moving IQR</button>
<button data-mode="changepoint">Change-Point</button>
</div>
</div>
<div class="panel-body"><canvas id="pulseCanvas"></canvas></div>
</div>
<div class="panel">
<div class="panel-header">
<span>Deviation Heatmap</span>
<div class="controls">
<button id="heatmapZoomIn">+</button>
<button id="heatmapZoomOut">-</button>
</div>
</div>
<div class="panel-body"><canvas id="heatmapCanvas"></canvas></div>
<div class="heatmap-legend">
<span>-3&sigma;</span>
<div class="gradient"></div>
<span>+3&sigma;</span>
</div>
</div>
<div class="panel" style="grid-column:1/-1">
<div class="panel-header">
<span>Model Drift &amp; Threshold Bands</span>
<div class="controls">
<button id="driftMetricPrev">&larr;</button>
<span id="driftMetricLabel" style="font-size:11px;color:#00d4ff;font-weight:400;text-transform:none;letter-spacing:0">cpu_usage</span>
<button id="driftMetricNext">&rarr;</button>
</div>
</div>
<div class="panel-body" style="min-height:320px"><canvas id="driftCanvas"></canvas></div>
</div>
<div class="panel root-cause-panel">
<div class="panel-header">
<span>Root-Cause Analysis &mdash; Causal Chain</span>
<span style="font-size:10px;color:#4a5a6d;text-transform:none">correlated metrics that preceded anomaly</span>
</div>
<div class="root-cause-list" id="rootCauseList"></div>
</div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
const WINDOW = 120;
const METRICS_COUNT = 6;
const METRIC_NAMES = ['cpu_usage','memory_mb','request_latency_ms','error_rate_pct','throughput_rps','disk_iops'];
const METRIC_COLORS = ['#00d4ff','#7c5cfc','#ffa502','#ff4757','#2ed573','#e056fd'];
const BASELINES = [45, 3200, 120, 1.2, 850, 3400];
const NOISE = [8, 180, 30, 0.5, 120, 400];
let data = [];
for (let m = 0; m < METRICS_COUNT; m++) {
data[m] = {values:[], predictions:[], anomalies:[]};
for (let i = 0; i < WINDOW; i++) {
let v = BASELINES[m] + (Math.random() - 0.5) * NOISE[m] * 2;
data[m].values.push(v);
data[m].predictions.push(v + (Math.random() - 0.5) * NOISE[m] * 0.3);
}
}
let metricsMeta = METRIC_NAMES.map((name,i)=>({name,color:METRIC_COLORS[i],baseline:BASELINES[i],noise:NOISE[i]}));
let detectionMode = 'zscore';
let anomalyEvents = [];
let currentDriftMetric = 0;
let heatmapZoom = 1;
let animId = null;
let lastFrame = 0;
let fps = 60;
function zscoreDetect(vals, threshold) {
threshold = threshold || 2.5;
let n = vals.length;
if (n < 4) return [];
let mean = 0, std = 0;
for (let i = 0; i < n; i++) mean += vals[i];
mean /= n;
for (let i = 0; i < n; i++) std += (vals[i] - mean) ** 2;
std = Math.sqrt(std / n) || 1;
let results = [];
for (let i = 0; i < n; i++) {
let z = (vals[i] - mean) / std;
results.push({index:i, value:vals[i], z, anomaly:Math.abs(z) > threshold});
}
return results;
}
function movingIQR(vals, k) {
k = k || 20;
let n = vals.length;
let results = [];
for (let i = 0; i < n; i++) {
let start = Math.max(0, i - k);
let window = vals.slice(start, i);
let anomaly = false;
let score = 0;
if (window.length >= 4) {
let sorted = window.slice().sort((a,b)=>a-b);
let q1 = sorted[Math.floor(sorted.length * 0.25)];
let q3 = sorted[Math.floor(sorted.length * 0.75)];
let iqr = q3 - q1 || 1;
let lower = q1 - 1.5 * iqr;
let upper = q3 + 1.5 * iqr;
anomaly = vals[i] < lower || vals[i] > upper;
score = (vals[i] - (q1+q3)/2) / iqr;
}
results.push({index:i, value:vals[i], z:score, anomaly});
}
return results;
}
function changePoint(vals, windowSize) {
windowSize = windowSize || 30;
let n = vals.length;
let results = [];
for (let i = 0; i < n; i++) {
let left = vals.slice(Math.max(0,i-windowSize), i);
let right = vals.slice(i, Math.min(n,i+Math.floor(windowSize/2)));
let anomaly = false;
let score = 0;
if (left.length >= 5 && right.length >= 3) {
let lm = left.reduce((a,b)=>a+b,0)/left.length;
let rm = right.reduce((a,b)=>a+b,0)/right.length;
let lv = left.reduce((a,b)=>a+(b-lm)**2,0)/left.length || 1;
let rv = right.reduce((a,b)=>a+(b-rm)**2,0)/right.length || 1;
let pooledVar = ((left.length-1)*lv + (right.length-1)*rv) / (left.length+right.length-2) || 1;
score = (rm - lm) / Math.sqrt(pooledVar * (1/left.length + 1/right.length));
anomaly = Math.abs(score) > 2.0;
}
results.push({index:i, value:vals[i], z:score, anomaly});
}
return results;
}
function detectAnomalies(metricIdx) {
let vals = data[metricIdx].values;
switch(detectionMode) {
case 'zscore': return zscoreDetect(vals);
case 'iqr': return movingIQR(vals, 20);
case 'changepoint': return changePoint(vals, 30);
default: return zscoreDetect(vals);
}
}
function generateNewPoint() {
for (let m = 0; m < METRICS_COUNT; m++) {
let b = BASELINES[m], n = NOISE[m];
let v = b + (Math.random() - 0.5) * n * 2;
if (Math.random() < 0.04) {
v += (Math.random() < 0.5 ? 1 : -1) * n * (2 + Math.random() * 3);
let t = performance.now();
anomalyEvents.push({time:t, metric:m, value:v, x:0.5+Math.random()*0.4, y:0.1+Math.random()*0.7, id:t+'-'+m});
if (anomalyEvents.length > 80) anomalyEvents.splice(0, anomalyEvents.length-80);
}
data[m].values.push(v);
if (data[m].values.length > WINDOW * 2) data[m].values.splice(0, data[m].values.length - WINDOW * 2);
let pred = b + (Math.random() - 0.5) * n * 0.3;
let drift = (v - b) / n;
data[m].predictions.push(pred + drift * n * 0.2);
if (data[m].predictions.length > WINDOW * 2) data[m].predictions.splice(0, data[m].predictions.length - WINDOW * 2);
}
updateMetricsBar();
updateRootCause();
}
let metricsTimer = setInterval(generateNewPoint, 1200);
function getRecentAnomalyCount() {
let count = 0;
for (let m = 0; m < METRICS_COUNT; m++) {
let det = detectAnomalies(m);
let recent = det.slice(-10);
count += recent.filter(d=>d.anomaly).length;
}
return count;
}
function updateMetricsBar() {
let bar = document.getElementById('metricsBar');
let html = '';
let totalAnomalies = 0;
for (let m = 0; m < METRICS_COUNT; m++) {
let det = detectAnomalies(m);
let recent = det.slice(-1);
let val = data[m].values[data[m].values.length-1] || 0;
let isAnom = recent.length && recent[0].anomaly;
if (isAnom) totalAnomalies++;
let cls = isAnom ? 'alert' : (Math.abs(val - BASELINES[m]) > NOISE[m] * 1.2 ? 'warn' : 'ok');
html += '<div class="metric-card">';
html += '<div class="label">'+METRIC_NAMES[m]+'</div>';
html += '<div class="value '+cls+'">'+val.toFixed(1)+'</div>';
html += '<div class="sub">baseline: '+BASELINES[m]+'</div>';
html += '</div>';
}
bar.innerHTML = html;
document.getElementById('anomalyCount').textContent = totalAnomalies + ' anomalies';
}
function drawPulse(canvas) {
let ctx = canvas.getContext('2d');
let W = canvas.width, H = canvas.height;
ctx.clearRect(0, 0, W, H);
ctx.fillStyle = '#0a1220';
ctx.fillRect(0, 0, W, H);
let gridCols = METRICS_COUNT;
let cellW = W / gridCols;
let cellH = H;
let now = performance.now();
for (let m = 0; m < METRICS_COUNT; m++) {
let x = m * cellW;
let vals = data[m].values;
let det = detectAnomalies(m);
let recentDet = det.slice(-30);
ctx.strokeStyle = METRIC_COLORS[m];
ctx.lineWidth = 1.5;
ctx.beginPath();
let min = Math.min(...vals.slice(-60));
let max = Math.max(...vals.slice(-60));
let range = max - min || 1;
let segment = vals.slice(-60);
let stepX = cellW / 60;
for (let i = 0; i < segment.length; i++) {
let px = x + i * stepX;
let py = H - 10 - ((segment[i] - min) / range) * (H - 30);
if (i === 0) ctx.moveTo(px, py);
else ctx.lineTo(px, py);
}
ctx.stroke();
let threshLow = x + cellW * 0.05;
let threshHigh = x + cellW * 0.95;
let midY = H - 10 - ((BASELINES[m] - min) / range) * (H - 30);
ctx.fillStyle = 'rgba(255,255,255,0.03)';
let upperY = H - 10 - ((BASELINES[m] + NOISE[m]*2.5 - min) / range) * (H - 30);
let lowerY = H - 10 - ((BASELINES[m] - NOISE[m]*2.5 - min) / range) * (H - 30);
ctx.fillRect(threshLow, Math.min(upperY,lowerY), cellW*0.9, Math.abs(upperY-lowerY));
ctx.strokeStyle = 'rgba(255,255,255,0.08)';
ctx.setLineDash([2,3]);
ctx.beginPath();
ctx.moveTo(threshLow, upperY);
ctx.lineTo(threshHigh, upperY);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(threshLow, lowerY);
ctx.lineTo(threshHigh, lowerY);
ctx.stroke();
ctx.setLineDash([]);
for (let i = 0; i < recentDet.length; i++) {
if (recentDet[i].anomaly) {
let sIdx = segment.length - recentDet.length + i;
let px = x + Math.max(0, sIdx) * stepX;
let py = H - 10 - ((vals.slice(-60)[Math.max(0,sIdx)] - min) / range) * (H - 30);
let age = now / 1000;
let pulseRadius = 8 + (i / recentDet.length) * 12;
let alpha = 0.6 + 0.3 * Math.sin(age * 3 + i);
let grad = ctx.createRadialGradient(px, py, 0, px, py, pulseRadius);
grad.addColorStop(0, METRIC_COLORS[m].replace(')','').replace('rgb','rgba').replace('rgba','rgba').split('(')[0]+'rgba('+METRIC_COLORS[m].slice(1,7)+',0.6)');
let baseR = parseInt(METRIC_COLORS[m].slice(1,3),16);
let baseG = parseInt(METRIC_COLORS[m].slice(3,5),16);
let baseB = parseInt(METRIC_COLORS[m].slice(5,7),16);
grad.addColorStop(0.3, `rgba(${baseR},${baseG},${baseB},0.2)`);
grad.addColorStop(1, `rgba(${baseR},${baseG},${baseB},0)`);
ctx.fillStyle = grad;
ctx.beginPath();
ctx.arc(px, py, pulseRadius * 1.2, 0, Math.PI * 2);
ctx.fill();
ctx.strokeStyle = METRIC_COLORS[m];
ctx.globalAlpha = 0.5 + 0.3 * Math.sin(age * 4 + i * 0.7);
ctx.lineWidth = 2;
ctx.beginPath();
ctx.arc(px, py, pulseRadius * (0.6 + 0.4 * Math.sin(age * 2 + i)), 0, Math.PI * 2);
ctx.stroke();
ctx.globalAlpha = 1;
ctx.fillStyle = '#fff';
ctx.font = '9px monospace';
ctx.fillText('!'+m, px-4, py-8);
}
}
ctx.fillStyle = '#4a5a6d';
ctx.font = '10px sans-serif';
ctx.textAlign = 'center';
ctx.fillText(METRIC_NAMES[m], x + cellW/2, 14);
}
ctx.fillStyle = 'rgba(255,255,255,0.04)';
ctx.font = '11px sans-serif';
ctx.textAlign = 'center';
ctx.fillText('Threshold bands = +/- 2.5 sigma', W/2, H - 4);
}
function drawHeatmap(canvas) {
let ctx = canvas.getContext('2d');
let W = canvas.width, H = canvas.height;
ctx.clearRect(0, 0, W, H);
ctx.fillStyle = '#0a1220';
ctx.fillRect(0, 0, W, H);
let rows = METRICS_COUNT;
let cols = Math.min(30, data[0].values.length);
let cellW = (W - 40) / cols * heatmapZoom;
let cellH = (H - 30) / rows;
let offsetX = 40;
let offsetY = 15;
let now = performance.now();
let tooltips = [];
for (let r = 0; r < rows; r++) {
let vals = data[r].values;
let det = detectAnomalies(r);
let recentVals = vals.slice(-cols);
let recentDet = det.slice(-cols);
let mean = 0, std = 0;
let segment = recentVals;
for (let i = 0; i < segment.length; i++) mean += segment[i];
mean /= segment.length || 1;
for (let i = 0; i < segment.length; i++) std += (segment[i] - mean) ** 2;
std = Math.sqrt(std / (segment.length || 1)) || 1;
for (let c = 0; c < Math.min(cols, recentVals.length); c++) {
let z = (recentVals[c] - mean) / std;
let zNorm = Math.max(-3, Math.min(3, z)) / 3;
let rCol, gCol, bCol;
if (zNorm < 0) {
rCol = 46; gCol = Math.floor(213 + zNorm * 213); bCol = Math.floor(115 + zNorm * 115);
} else {
rCol = Math.floor(255 * zNorm); gCol = Math.floor(165 * (1 - zNorm)); bCol = Math.floor(87 * (1 - zNorm));
}
let x = offsetX + c * cellW;
let y = offsetY + r * cellH + r * 2;
ctx.fillStyle = `rgb(${Math.min(255,rCol)},${Math.min(255,gCol)},${Math.min(255,bCol)})`;
ctx.fillRect(x, y, cellW - 1, cellH - 2);
if (recentDet[c] && recentDet[c].anomaly) {
ctx.strokeStyle = '#fff';
ctx.lineWidth = 1.5;
ctx.strokeRect(x, y, cellW - 1, cellH - 2);
}
tooltips.push({x:c, y:r, px:x+cellW/2, py:y+cellH/2, metric:METRIC_NAMES[r], val:recentVals[c].toFixed(1), z:z.toFixed(2), anomaly:!!(recentDet[c]&&recentDet[c].anomaly)});
}
ctx.fillStyle = METRIC_COLORS[r];
ctx.font = '10px sans-serif';
ctx.textAlign = 'right';
ctx.fillText(METRIC_NAMES[r], offsetX - 4, offsetY + r * cellH + r * 2 + cellH/2 + 3);
}
canvas._tooltips = tooltips;
ctx.fillStyle = '#4a5a6d';
ctx.font = '9px sans-serif';
ctx.textAlign = 'left';
for (let i = 0; i < Math.min(30, cols); i += 5) {
ctx.fillText('t-'+(cols-i), offsetX + i * cellW, H - 4);
}
}
function drawDrift(canvas) {
let ctx = canvas.getContext('2d');
let W = canvas.width, H = canvas.height;
ctx.clearRect(0, 0, W, H);
ctx.fillStyle = '#0a1220';
ctx.fillRect(0, 0, W, H);
let m = currentDriftMetric;
let vals = data[m].values;
let preds = data[m].predictions;
let segment = vals.slice(-80);
let predSegment = preds.slice(-80);
let len = Math.min(segment.length, predSegment.length);
let min = Math.min(...segment, ...predSegment);
let max = Math.max(...segment, ...predSegment);
let range = max - min || 1;
let pad = 30;
let plotW = W - pad * 2;
let plotH = H - pad * 2;
let stepX = plotW / (len - 1 || 1);
let baseY = pad + plotH;
let now = performance.now();
let threshold = NOISE[m] * 2.5;
function yNorm(v) { return baseY - ((v - min) / range) * plotH; }
ctx.fillStyle = 'rgba(0,200,255,0.04)';
let upperBand = BASELINES[m] + threshold;
let lowerBand = BASELINES[m] - threshold;
ctx.fillRect(pad, yNorm(upperBand), plotW, yNorm(lowerBand) - yNorm(upperBand));
ctx.strokeStyle = 'rgba(255,255,255,0.06)';
ctx.setLineDash([3,4]);
ctx.lineWidth = 1;
ctx.beginPath();
ctx.moveTo(pad, yNorm(BASELINES[m] + threshold));
ctx.lineTo(pad + plotW, yNorm(BASELINES[m] + threshold));
ctx.stroke();
ctx.beginPath();
ctx.moveTo(pad, yNorm(BASELINES[m] - threshold));
ctx.lineTo(pad + plotW, yNorm(BASELINES[m] - threshold));
ctx.stroke();
ctx.setLineDash([]);
ctx.fillStyle = 'rgba(255,255,255,0.15)';
ctx.font = '9px sans-serif';
ctx.textAlign = 'left';
ctx.fillText('+'+threshold.toFixed(1), pad + 4, yNorm(BASELINES[m] + threshold) - 3);
ctx.fillText('-'+threshold.toFixed(1), pad + 4, yNorm(BASELINES[m] - threshold) + 11);
for (let i = 1; i < len; i++) {
let x1 = pad + (i-1) * stepX, y1a = yNorm(segment[i-1]);
let x2 = pad + i * stepX, y2a = yNorm(segment[i]);
let y1p = yNorm(predSegment[i-1]), y2p = yNorm(predSegment[i]);
let driftGap = (segment[i] - predSegment[i]) / range;
let isDiverging = Math.abs(driftGap) > 0.15;
ctx.fillStyle = isDiverging ? 'rgba(255,71,87,0.12)' : 'rgba(46,213,115,0.12)';
let fillTop = Math.min(y1a, y1p, y2a, y2p);
let fillBot = Math.max(y1a, y1p, y2a, y2p);
ctx.fillRect(x1, fillTop, x2 - x1, fillBot - fillTop);
ctx.strokeStyle = METRIC_COLORS[m];
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(x1, y1a);
ctx.lineTo(x2, y2a);
ctx.stroke();
ctx.strokeStyle = 'rgba(255,255,255,0.4)';
ctx.lineWidth = 1;
ctx.setLineDash([3,3]);
ctx.beginPath();
ctx.moveTo(x1, y1p);
ctx.lineTo(x2, y2p);
ctx.stroke();
ctx.setLineDash([]);
}
let lastVal = segment[len-1];
let lastPred = predSegment[len-1];
let lastDrift = lastVal - lastPred;
let driftPct = (lastDrift / BASELINES[m]) * 100;
ctx.fillStyle = Math.abs(driftPct) > 10 ? '#ff4757' : '#2ed573';
ctx.font = 'bold 13px monospace';
ctx.textAlign = 'right';
let driftSign = driftPct > 0 ? '+' : '';
ctx.fillText('Drift: '+driftSign+driftPct.toFixed(1)+'%', W - pad, pad + 16);
ctx.fillStyle = '#7f8fa6';
ctx.font = '10px sans-serif';
ctx.textAlign = 'center';
ctx.fillText('Prediction (dashed)  |  Actual (solid)  |  Green fill = on track  |  Red fill = diverging', W/2, H - 4);
}
function updateRootCause() {
let container = document.getElementById('rootCauseList');
let now = performance.now();
let recentAnomalies = anomalyEvents.filter(e => now - e.time < 15000);
let metricScores = {};
for (let m = 0; m < METRICS_COUNT; m++) {
metricScores[m] = {anomalies:0, totalDrift:0, count:0};
let det = detectAnomalies(m);
let recent = det.slice(-20);
for (let d of recent) {
if (d.anomaly) metricScores[m].anomalies++;
metricScores[m].totalDrift += Math.abs(d.z);
metricScores[m].count++;
}
}
let mcArray = Object.entries(metricScores).map(([idx,sc])=>({idx:parseInt(idx), name:METRIC_NAMES[idx], color:METRIC_COLORS[idx], score:sc.anomalies * 3 + (sc.totalDrift/(sc.count||1))*2 }));
mcArray.sort((a,b)=>b.score - a.score);
let causalChain = [];
let topScore = mcArray[0] ? mcArray[0].score : 0;
for (let i = 0; i < Math.min(4, mcArray.length) && mcArray[i].score > 0.5; i++) {
let m = mcArray[i];
let dt = detectAnomalies(m.idx);
let last = dt.length ? dt[dt.length-1] : null;
let zVal = last ? last.z : 0;
let direction = zVal > 0 ? 'pos' : 'neg';
let changePct = ((data[m.idx].values[data[m.idx].values.length-1] - BASELINES[m.idx]) / BASELINES[m.idx] * 100).toFixed(1);
let severity = Math.min(100, Math.round((m.score / (topScore||1)) * 100));
causalChain.push({name:m.name, color:m.color, changePct, direction, severity, z:zVal.toFixed(2)});
}
if (causalChain.length === 0) {
container.innerHTML = '<div class="root-cause-item"><div class="rc-name" style="color:#4a5a6d">No anomalies detected</div><div class="rc-detail">System operating within normal range</div></div>';
return;
}
let html = '';
for (let i = 0; i < causalChain.length; i++) {
let cc = causalChain[i];
html += '<div class="root-cause-item">';
html += '<div class="rc-name" style="color:'+cc.color+'">'+cc.name+'</div>';
html += '<div class="rc-detail"><span>z-score: '+cc.z+'</span><span class="rc-change '+cc.direction+'">'+cc.changePct+'%</span></div>';
html += '<div class="rc-bar" style="width:'+cc.severity+'%;background:linear-gradient(90deg,'+cc.color+',rgba(255,71,87,0.6))"></div>';
html += '<div class="rc-detail" style="font-size:10px;color:#4a5a6d">'+ (cc.direction === 'pos' ? 'spike above baseline' : 'drop below baseline') +'</div>';
html += '</div>';
if (i < causalChain.length - 1) {
html += '<div class="chain-link">&rarr;</div>';
}
}
container.innerHTML = html;
}
function resizeCanvas(canvas) {
let rect = canvas.parentElement.getBoundingClientRect();
let dpr = window.devicePixelRatio || 1;
let displayW = rect.width;
let displayH = canvas.parentElement.minHeight ? parseInt(canvas.parentElement.minHeight) : 280;
canvas.style.width = displayW + 'px';
canvas.style.height = displayH + 'px';
canvas.width = displayW * dpr;
canvas.height = displayH * dpr;
let ctx = canvas.getContext('2d');
ctx.scale(dpr, dpr);
canvas._displayW = displayW;
canvas._displayH = displayH;
}
function render() {
let pulseCanvas = document.getElementById('pulseCanvas');
let heatmapCanvas = document.getElementById('heatmapCanvas');
let driftCanvas = document.getElementById('driftCanvas');
resizeCanvas(pulseCanvas);
resizeCanvas(heatmapCanvas);
resizeCanvas(driftCanvas);
drawPulse(pulseCanvas);
drawHeatmap(heatmapCanvas);
drawDrift(driftCanvas);
}
function animationLoop(timestamp) {
if (!lastFrame) lastFrame = timestamp;
let delta = timestamp - lastFrame;
lastFrame = timestamp;
fps = Math.round(1000 / delta);
document.getElementById('fpsDisplay').textContent = fps + ' fps';
render();
animId = requestAnimationFrame(animationLoop);
}
animId = requestAnimationFrame(animationLoop);
document.querySelectorAll('.mode-selector button').forEach(btn => {
btn.addEventListener('click', function() {
document.querySelectorAll('.mode-selector button').forEach(b => b.classList.remove('active'));
this.classList.add('active');
detectionMode = this.dataset.mode;
});
});
document.getElementById('driftMetricPrev').addEventListener('click', function() {
currentDriftMetric = (currentDriftMetric - 1 + METRICS_COUNT) % METRICS_COUNT;
document.getElementById('driftMetricLabel').textContent = METRIC_NAMES[currentDriftMetric];
});
document.getElementById('driftMetricNext').addEventListener('click', function() {
currentDriftMetric = (currentDriftMetric + 1) % METRICS_COUNT;
document.getElementById('driftMetricLabel').textContent = METRIC_NAMES[currentDriftMetric];
});
document.getElementById('heatmapZoomIn').addEventListener('click', function() {
heatmapZoom = Math.min(3, heatmapZoom + 0.3);
});
document.getElementById('heatmapZoomOut').addEventListener('click', function() {
heatmapZoom = Math.max(0.5, heatmapZoom - 0.3);
});
let tooltipEl = document.getElementById('tooltip');
let heatmapCanvas = document.getElementById('heatmapCanvas');
heatmapCanvas.addEventListener('mousemove', function(e) {
let rect = this.getBoundingClientRect();
let mx = e.clientX - rect.left;
let my = e.clientY - rect.top;
let tips = this._tooltips || [];
let found = null;
for (let t of tips) {
let dist = Math.sqrt((mx - (t.px || 0))**2 + (my - (t.py || 0))**2);
if (dist < 14) { found = t; break; }
}
if (found) {
tooltipEl.innerHTML = '<div class="tt-row"><span class="tt-label">Metric:</span><span style="color:'+METRIC_COLORS[found.y]+';font-weight:600">'+found.metric+'</span></div>'
+'<div class="tt-row"><span class="tt-label">Value:</span><span class="tt-value">'+found.val+'</span></div>'
+'<div class="tt-row"><span class="tt-label">Z-Score:</span><span class="tt-value '+(found.anomaly?'alert':'ok')+'">'+found.z+'</span></div>'
+(found.anomaly?'<div class="tt-row"><span class="tt-label" style="color:#ff4757">ANOMALY DETECTED</span></div>':'');
let tx = e.clientX + 12;
let ty = e.clientY - 10;
if (tx + 200 > window.innerWidth) tx = e.clientX - 210;
if (ty < 10) ty = 10;
tooltipEl.style.left = tx + 'px';
tooltipEl.style.top = ty + 'px';
tooltipEl.classList.add('visible');
} else {
tooltipEl.classList.remove('visible');
}
});
heatmapCanvas.addEventListener('mouseleave', function() {
tooltipEl.classList.remove('visible');
});
window.addEventListener('resize', function() {
render();
});
updateMetricsBar();
updateRootCause();
document.getElementById('driftMetricLabel').textContent = METRIC_NAMES[currentDriftMetric];
console.log('Anomaly Detection Visualizer initialized');
console.log('Mode: '+detectionMode+' | Metrics: '+METRICS_COUNT+' | Window: '+WINDOW);
})();
</script>
</body>
</html>