```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Anomaly Detection Dashboard</title>
<style>
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Segoe UI',system-ui,-apple-system,sans-serif; background:#0b0e14; color:#e0e4ec; padding:20px; min-height:100vh; }
.header { display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; padding-bottom:16px; border-bottom:1px solid #2a3040; }
.header h1 { font-size:22px; font-weight:600; letter-spacing:0.5px; }
.header h1 span { color:#5af; }
.header-right { display:flex; gap:20px; align-items:center; font-size:13px; color:#8a9ab0; }
.status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; }
.status-dot.online { background:#4ade80; box-shadow:0 0 6px #4ade8066; }
.status-dot.gap { background:#facc15; box-shadow:0 0 6px #facc1566; }
.status-dot.offline { background:#f87171; box-shadow:0 0 6px #f8717166; }
.dashboard-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }
.card { background:#131a24; border-radius:10px; border:1px solid #29313d; padding:16px; position:relative; }
.card h2 { font-size:13px; font-weight:500; color:#8a9ab0; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; }
.card-full { grid-column:1/-1; }
.chart-container { position:relative; width:100%; height:240px; }
.chart-container canvas { width:100%; height:100%; display:block; }
.metrics-bar { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:16px; }
.metric-tile { flex:1; min-width:140px; background:#0e141f; border-radius:8px; border:1px solid #29313d; padding:12px; }
.metric-tile .label { font-size:11px; color:#6a7a90; text-transform:uppercase; letter-spacing:0.5px; }
.metric-tile .value { font-size:24px; font-weight:700; margin-top:4px; }
.metric-tile .value.ok { color:#4ade80; }
.metric-tile .value.warn { color:#facc15; }
.metric-tile .value.critical { color:#f87171; animation:blinkCritical 1s step-end infinite; }
@keyframes blinkCritical { 0%,100% { opacity:1; } 50% { opacity:0.3; } }
.pulse-ring { position:absolute; width:16px; height:16px; border-radius:50%; pointer-events:none; }
.pulse-ring::before, .pulse-ring::after { content:''; position:absolute; inset:-4px; border-radius:50%; border:2px solid currentColor; animation:pulseExpand 1.5s ease-out infinite; opacity:0; }
.pulse-ring::after { animation-delay:0.75s; }
@keyframes pulseExpand { 0% { transform:scale(0.5); opacity:0.8; } 100% { transform:scale(3); opacity:0; } }
.heatmap-grid { display:grid; gap:2px; }
.heatmap-cell { position:relative; border-radius:2px; cursor:pointer; transition:transform 0.1s; }
.heatmap-cell:hover { transform:scale(1.3); z-index:10; }
.heatmap-tooltip { display:none; position:absolute; bottom:100%; left:50%; transform:translateX(-50%); background:#1e2735; border:1px solid #3a4560; border-radius:6px; padding:6px 10px; font-size:11px; white-space:nowrap; z-index:20; pointer-events:none; }
.heatmap-cell:hover .heatmap-tooltip { display:block; }
.drift-gap { stroke:#facc15; stroke-dasharray:4,4; stroke-width:1.5; fill:none; }
.threshold-band { fill:rgba(74,222,128,0.08); }
.threshold-band.warn { fill:rgba(250,204,21,0.06); }
.threshold-band.critical { fill:rgba(248,113,113,0.06); }
.root-cause-list { list-style:none; }
.root-cause-list li { padding:6px 0; border-bottom:1px solid #1e2735; font-size:13px; display:flex; justify-content:space-between; }
.root-cause-list li:last-child { border-bottom:none; }
.root-cause-list .metric-name { color:#8a9ab0; }
.root-cause-list .corr-val { color:#5af; font-weight:600; }
.root-cause-list .arrow { color:#4ade80; margin:0 4px; }
.refresh-indicator { font-size:11px; color:#5a6a80; text-align:right; margin-top:8px; }
.refresh-indicator .ts { font-variant-numeric:tabular-nums; }
.alert-banner { display:none; background:linear-gradient(90deg, #f8717120,#f8711208); border:1px solid #f8717140; border-radius:8px; padding:10px 16px; margin-bottom:16px; font-size:13px; }
.alert-banner.active { display:flex; align-items:center; gap:12px; }
.alert-banner .alert-dot { width:10px; height:10px; border-radius:50%; background:#f87171; animation:blinkCritical 1s step-end infinite; flex-shrink:0; }
.alert-banner .alert-text { flex:1; }
.alert-banner .alert-count { background:#f8717130; border-radius:12px; padding:2px 10px; font-size:12px; font-weight:600; color:#f87171; }
.fullscreen-btn { background:none; border:1px solid #29313d; color:#6a7a90; border-radius:6px; padding:4px 10px; font-size:11px; cursor:pointer; }
.fullscreen-btn:hover { background:#1e2735; color:#e0e4ec; }
.awaiting-stream { display:flex; align-items:center; justify-content:center; height:200px; color:#4a5a70; font-size:16px; letter-spacing:1px; }
.awaiting-stream .pulse-dot { width:12px; height:12px; border-radius:50%; background:#5af; margin-right:12px; animation:pulseDot 1.5s ease-in-out infinite; }
@keyframes pulseDot { 0%,100% { opacity:0.3; transform:scale(0.8); } 50% { opacity:1; transform:scale(1.2); } }
@media(max-width:900px){ .dashboard-grid { grid-template-columns:1fr; } .metrics-bar { flex-direction:column; } }
</style>
</head>
<body>
<div class=header>
  <h1>Anomaly Detection <span>Visualizer</span></h1>
  <div class=header-right>
    <span><span class=status-dot online id=statusDot></span><span id=statusLabel>Streaming</span></span>
    <span>Points: <span id=pointCount>0</span></span>
    <span>Refresh: <span id=refreshCount>0</span></span>
    <button class=fullscreen-btn onclick="document.documentElement.requestFullscreen?.()">Fullscreen</button>
  </div>
</div>
<div class=alert-banner id=alertBanner>
  <span class=alert-dot></span>
  <span class=alert-text id=alertText>Anomaly detected in one or more metrics</span>
  <span class=alert-count id=alertCount>0</span>
</div>
<div class=metrics-bar id=metricsBar>
  <div class=metric-tile>
    <div class=label>CPU Usage</div>
    <div class="value ok" id=metricCPU>--</div>
  </div>
  <div class=metric-tile>
    <div class=label>Memory</div>
    <div class="value ok" id=metricMem>--</div>
  </div>
  <div class=metric-tile>
    <div class=label>Latency (ms)</div>
    <div class="value ok" id=metricLat>--</div>
  </div>
  <div class=metric-tile>
    <div class=label>Error Rate</div>
    <div class="value ok" id=metricErr>--</div>
  </div>
  <div class=metric-tile>
    <div class=label>Throughput</div>
    <div class="value ok" id=metricThr>--</div>
  </div>
</div>
<div class=dashboard-grid>
  <div class=card>
    <h2>Deviation Heatmap</h2>
    <div style=position:relative;>
      <div id=heatmapContainer class=chart-container style=height:200px;></div>
      <div id=heatmapPlaceholder class=awaiting-stream style=display:none;>
        <span class=pulse-dot></span> Awaiting stream...
      </div>
    </div>
    <div class=refresh-indicator>Last: <span class=ts id=heatmapTs>--</span></div>
  </div>
  <div class=card>
    <h2>Drift: Prediction vs Actual</h2>
    <div class=chart-container><canvas id=driftChart></canvas></div>
    <div class=refresh-indicator>Gaps: <span id=driftGapCount>0</span> | Last: <span class=ts id=driftTs>--</span></div>
  </div>
  <div class=card>
    <h2>Anomaly Timeline &amp; Pulse</h2>
    <div class=chart-container><canvas id=pulseChart></canvas></div>
    <div class=refresh-indicator>Active anomalies: <span id=pulseCount>0</span></div>
  </div>
  <div class=card>
    <h2>Root-Cause Correlations</h2>
    <ul class=root-cause-list id=rootCauseList>
      <li style=color:#4a5a70;font-size:12px;>Collecting data...</li>
    </ul>
    <div class=refresh-indicator>Min |r| &gt; 0.3 for report</div>
  </div>
  <div class="card card-full" style=grid-column:1/-1;>
    <h2>Metric Stream &amp; Thresholds</h2>
    <div class=chart-container><canvas id=streamChart></canvas></div>
  </div>
</div>
<script>
(function() {
'use strict';
const METRICS = ['cpu','memory','latency','error_rate','throughput'];
const METRIC_LABELS = { cpu:'CPU %', memory:'Mem %', latency:'Latency ms', error_rate:'Err/s', throughput:'TPS' };
const MAX_POINTS = 2000;
const WINDOW = 30;
const POLL_INTERVAL = 1000;
const ANOMALY_THRESHOLD = 2.5;
const GAP_THRESHOLD_MS = 3000;
const SAFARI_BOX_SHADOW_LIMIT = 6;
let isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
let streamData = {};
METRICS.forEach(m => { streamData[m] = []; });
let anomalies = [];
let timestamps = [];
let predictionData = [];
let gapIntervals = [];
let lastTimestamp = null;
let currentGap = false;
let gapStart = null;
let refreshCount = 0;
let anomalyCount = 0;
let awaitingStream = true;
let pollingCycles = 0;
let streamActive = true;
function genMetric(base, noise) {
  return base + (Math.random() - 0.5) * noise * 2;
}
function injectAnomaly(value, base, strength) {
  if (Math.random() < 0.04) {
    return value + (Math.random() > 0.5 ? 1 : -1) * base * strength;
  }
  return value;
}
function generateDataPoint() {
  let now = Date.now();
  let gap = false;
  if (pollingCycles < 10 && Math.random() < 0.15) {
    pollingCycles++;
    return null;
  }
  if (currentGap) {
    if (Math.random() < 0.3) {
      currentGap = false;
      gapStart = null;
    } else {
      return null;
    }
  }
  if (Math.random() < 0.06 && gapStart === null) {
    currentGap = true;
    gapStart = now;
    return null;
  }
  let pt = {
    cpu: injectAnomaly(genMetric(45, 20), 20, 2.0),
    memory: injectAnomaly(genMetric(62, 15), 15, 1.8),
    latency: injectAnomaly(genMetric(120, 60), 60, 2.5),
    error_rate: injectAnomaly(genMetric(3, 4), 4, 3.0),
    throughput: injectAnomaly(genMetric(850, 200), 200, 1.6),
    t: now
  };
  if (gapStart !== null) {
    let gapDur = now - gapStart;
    if (gapDur > 0) {
      gapIntervals.push({ start: gapStart, end: now });
    }
    gapStart = null;
    currentGap = false;
  }
  timestamps.push(now);
  METRICS.forEach(m => streamData[m].push(pt[m]));
  let pred = {
    cpu: pt.cpu + genMetric(0, 3),
    memory: pt.memory + genMetric(0, 2),
    latency: pt.latency + genMetric(0, 8),
    error_rate: Math.max(0, pt.error_rate + genMetric(0, 0.5)),
    throughput: pt.throughput + genMetric(0, 30)
  };
  predictionData.push(pred);
  if (streamData.cpu.length > MAX_POINTS) {
    let excess = streamData.cpu.length - MAX_POINTS;
    METRICS.forEach(m => streamData[m].splice(0, excess));
    timestamps.splice(0, excess);
    predictionData.splice(0, excess);
  }
  pollingCycles++;
  awaitingStream = false;
  return pt;
}
function zScore(arr, val) {
  if (arr.length < 4) return 0;
  let n = arr.length;
  let mean = arr.reduce((a,b) => a+b, 0) / n;
  let sqDiffs = arr.map(v => (v - mean) ** 2);
  let std = Math.sqrt(sqDiffs.reduce((a,b) => a+b, 0) / n);
  if (std === 0) return 0;
  return (val - mean) / std;
}
function movingIQR(arr, val) {
  if (arr.length < 4) return 0;
  let sorted = [...arr].sort((a,b) => a-b);
  let q1 = sorted[Math.floor(sorted.length * 0.25)];
  let q3 = sorted[Math.floor(sorted.length * 0.75)];
  let iqr = q3 - q1;
  if (iqr === 0) return 0;
  let median = sorted[Math.floor(sorted.length * 0.5)];
  return (val - median) / (iqr * 1.5);
}
function detectAnomalies() {
  anomalies = [];
  let now = Date.now();
  METRICS.forEach(metric => {
    let data = streamData[metric];
    if (data.length < 10) return;
    let windowEnd = data.length;
    let windowStart = Math.max(0, windowEnd - WINDOW);
    let recent = data.slice(windowStart, windowEnd - 1);
    let latest = data[data.length - 1];
    if (recent.length < 4) return;
    let z = zScore(recent, latest);
    let iqr = movingIQR(recent, latest);
    let isAnomaly = Math.abs(z) > ANOMALY_THRESHOLD || Math.abs(iqr) > 1.0;
    if (isAnomaly) {
      let severity = Math.abs(z) > 3.5 || Math.abs(iqr) > 2.0 ? 'critical' : 'warning';
      anomalies.push({
        metric,
        value: latest,
        zScore: z,
        iqrScore: iqr,
        severity,
        timestamp: now,
        index: data.length - 1
      });
    }
  });
  anomalyCount = anomalies.length;
  let banner = document.getElementById('alertBanner');
  let alertText = document.getElementById('alertText');
  let alertCount = document.getElementById('alertCount');
  if (anomalyCount > 0) {
    banner.classList.add('active');
    let metrics = [...new Set(anomalies.map(a => a.metric))];
    alertText.textContent = 'Anomaly detected: ' + metrics.join(', ');
    alertCount.textContent = anomalyCount;
  } else {
    banner.classList.remove('active');
  }
  renderPulseChart();
  updateHeatmap(); 
  updateMetrics();
  updateRootCauses();
}
function updateMetrics() {
  if (streamData.cpu.length === 0) return;
  let last = {
    cpu: streamData.cpu[streamData.cpu.length - 1],
    memory: streamData.memory[streamData.memory.length - 1],
    latency: streamData.latency[streamData.latency.length - 1],
    error_rate: streamData.error_rate[streamData.error_rate.length - 1],
    throughput: streamData.throughput[streamData.throughput.length - 1]
  };
  function setMetric(id, val, unit, warn, crit) {
    let el = document.getElementById(id);
    if (!el) return;
    let display = typeof val === 'number' ? val.toFixed(1) + (unit||'') : '--';
    el.textContent = display;
    el.className = 'value';
    if (val > crit) el.classList.add('critical');
    else if (val > warn) el.classList.add('warn');
    else el.classList.add('ok');
  }
  setMetric('metricCPU', last.cpu, '%', 70, 90);
  setMetric('metricMem', last.memory, '%', 80, 95);
  setMetric('metricLat', last.latency, '', 200, 500);
  setMetric('metricErr', last.error_rate, '', 8, 20);
  setMetric('metricThr', last.throughput, '', 600, 400);
}
function renderPulseChart() {
  let canvas = document.getElementById('pulseChart');
  if (!canvas) return;
  let rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  let ctx = canvas.getContext('2d');
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  let w = rect.width, h = rect.height;
  ctx.clearRect(0,0,w,h);
  let data = streamData.cpu;
  if (data.length < 2) {
    ctx.fillStyle = '#4a5a70';
    ctx.font = '14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Awaiting data...', w/2, h/2);
    return;
  }
  let pad = 10;
  let chartW = w - pad*2;
  let chartH = h - pad*2;
  let allVals = [];
  METRICS.forEach(m => { allVals = allVals.concat(streamData[m]); });
  let min = Math.min(...allVals);
  let max = Math.max(...allVals);
  let range = max - min || 1;
  let colors = { cpu:'#5af', memory:'#4ade80', latency:'#facc15', error_rate:'#f87171', throughput:'#a78bfa' };
  let xStep = chartW / (data.length - 1 || 1);
  anomalies.forEach(a => {
    let x = pad + a.index * xStep;
    let y = pad + chartH - ((a.value - min) / range * chartH);
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI*2);
    ctx.fillStyle = a.severity === 'critical' ? '#f8717130' : '#facc1530';
    ctx.fill();
    ctx.strokeStyle = a.severity === 'critical' ? '#f87171' : '#facc15';
    ctx.lineWidth = 2;
    ctx.stroke();
    if (isSafari) {
      let g = ctx.createRadialGradient(x,y,4,x,y,20);
      g.addColorStop(0, (a.severity==='critical'?'#f87171':'#facc15')+'80');
      g.addColorStop(1, (a.severity==='critical'?'#f87171':'#facc15')+'00');
      ctx.beginPath();
      ctx.arc(x, y, 20, 0, Math.PI*2);
      ctx.fillStyle = g;
      ctx.fill();
    } else {
      for (let ri = 0; ri < 3; ri++) {
        ctx.beginPath();
        ctx.arc(x, y, 8 + ri*6, 0, Math.PI*2);
        ctx.strokeStyle = (a.severity==='critical'?'#f87171':'#facc15') + (30 - ri*8).toString(16).padStart(2,'0');
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    }
    ctx.fillStyle = '#fff';
    ctx.font = '10px system-ui';
    ctx.textAlign = 'center';
    let label = a.metric.substring(0,3);
    ctx.fillText(label, x, y - 16);
  });
  METRICS.forEach(metric => {
    let d = streamData[metric];
    if (d.length < 2) return;
    ctx.beginPath();
    ctx.strokeStyle = colors[metric] + '60';
    ctx.lineWidth = 1;
    for (let i = 0; i < d.length; i++) {
      let x = pad + i * xStep;
      let y = pad + chartH - ((d[i] - min) / range * chartH);
      i === 0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
    }
    ctx.stroke();
  });
  document.getElementById('pulseCount').textContent = anomalies.length;
}
function updateHeatmap() {
  let container = document.getElementById('heatmapContainer');
  let placeholder = document.getElementById('heatmapPlaceholder');
  if (!container) return;
  if (streamData.cpu.length < 5) {
    placeholder.style.display = 'flex';
    container.innerHTML = '';
    return;
  }
  placeholder.style.display = 'none';
  let rect = container.getBoundingClientRect();
  let w = rect.width, h = rect.height;
  let cols = 24;
  let rows = 5;
  let cellW = Math.floor(w / cols);
  let cellH = Math.floor(h / rows);
  let gridW = cellW * cols;
  let gridH = cellH * rows;
  let html = '<div class=heatmap-grid style="grid-template-columns:repeat('+cols+','+cellW+'px);grid-template-rows:repeat('+rows+','+cellH+'px);width:'+gridW+'px;height:'+gridH+'px;margin:0 auto;">';
  let metrics = METRICS.slice(0, rows);
  for (let r = 0; r < rows; r++) {
    let metric = metrics[r];
    let data = streamData[metric];
    if (data.length < cols) continue;
    let slice = data.slice(-cols);
    let mean = slice.reduce((a,b) => a+b, 0) / slice.length;
    let sqDiffs = slice.map(v => (v - mean) ** 2);
    let std = Math.sqrt(sqDiffs.reduce((a,b) => a+b, 0) / slice.length) || 1;
    for (let c = 0; c < cols; c++) {
      let val = slice[c];
      let z = (val - mean) / std;
      let clampedZ = Math.max(-3, Math.min(3, z));
      let normalized = (clampedZ + 3) / 6;
      let r2, g2, b2;
      if (normalized < 0.5) {
        let t = normalized * 2;
        r2 = Math.floor(30 + t * 40);
        g2 = Math.floor(60 + t * 120);
        b2 = Math.floor(130 + t * 30);
      } else {
        let t = (normalized - 0.5) * 2;
        r2 = Math.floor(70 + t * 140);
        g2 = Math.floor(180 - t * 120);
        b2 = Math.floor(160 - t * 80);
      }
      let severity = '';
      if (Math.abs(z) > 2.5) severity = 'border:1px solid #f8717180;';
      else if (Math.abs(z) > 1.5) severity = 'border:1px solid #facc1540;';
      let valStr = val.toFixed(1);
      html += '<div class=heatmap-cell style="background:rgb('+r2+','+g2+','+b2+');width:'+cellW+'px;height:'+cellH+'px;'+severity+'"><span class=heatmap-tooltip>'+metric+': '+valStr+' (z='+z.toFixed(2)+')</span></div>';
    }
  }
  html += '</div>';
  container.innerHTML = html;
  document.getElementById('heatmapTs').textContent = new Date().toLocaleTimeString();
}
function renderDriftChart() {
  let canvas = document.getElementById('driftChart');
  if (!canvas) return;
  let rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  let ctx = canvas.getContext('2d');
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  let w = rect.width, h = rect.height;
  ctx.clearRect(0,0,w,h);
  let data = streamData.cpu;
  if (data.length < 2) {
    ctx.fillStyle = '#4a5a70';
    ctx.font = '14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Awaiting data...', w/2, h/2);
    return;
  }
  let pad = { t:15, r:15, b:25, l:40 };
  let chartW = w - pad.l - pad.r;
  let chartH = h - pad.t - pad.b;
  let allVals = data.concat(predictionData.map(p=>p.cpu).filter(v=>v!=null));
  let min = Math.min(...allVals);
  let max = Math.max(...allVals);
  let range = max - min || 1;
  let xStep = chartW / (data.length - 1 || 1);
  let gapCount = 0;
  ctx.beginPath();
  ctx.strokeStyle = '#4ade80';
  ctx.lineWidth = 2;
  for (let i = 0; i < data.length; i++) {
    let x = pad.l + i * xStep;
    let y = pad.t + chartH - ((predictionData[i].cpu - min) / range * chartH);
    i === 0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
  }
  ctx.stroke();
  ctx.beginPath();
  ctx.strokeStyle = '#5af';
  ctx.lineWidth = 2;
  for (let i = 0; i < data.length; i++) {
    let x = pad.l + i * xStep;
    let y = pad.t + chartH - ((data[i] - min) / range * chartH);
    i === 0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
  }
  ctx.stroke();
  let driftTotal = 0;
  for (let i = 0; i < data.length; i++) {
    driftTotal += Math.abs(data[i] - predictionData[i].cpu);
    let x = pad.l + i * xStep;
    let aY = pad.t + chartH - ((data[i] - min) / range * chartH);
    let pY = pad.t + chartH - ((predictionData[i].cpu - min) / range * chartH);
    let diff = Math.abs(data[i] - predictionData[i].cpu);
    let normDiff = diff / range;
    if (normDiff > 0.05) {
      ctx.beginPath();
      ctx.moveTo(x, aY);
      ctx.lineTo(x, pY);
      ctx.strokeStyle = normDiff > 0.15 ? '#f8717140' : '#facc1540';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }
  let driftUpper = pad.t + chartH - ((min + range*0.95) - min) / range * chartH;
  let driftLower = pad.t + chartH - ((min + range*0.7) - min) / range * chartH;
  ctx.fillStyle = 'rgba(74,222,128,0.08)';
  ctx.fillRect(pad.l, driftUpper, chartW, driftLower - driftUpper);
  ctx.fillStyle = '#4a5a70';
  ctx.font = '10px system-ui';
  ctx.fillText('Prediction', pad.l + 4, pad.t + 12);
  ctx.fillStyle = '#4a5a70';
  ctx.fillText('Actual', pad.l + 4, pad.t + 24);
  ctx.fillStyle = '#4ade80';
  ctx.fillRect(pad.l + 70, pad.t + 6, 12, 2);
  ctx.fillStyle = '#5af';
  ctx.fillRect(pad.l + 70, pad.t + 18, 12, 2);
  for (let g = 0; g < gapIntervals.length; g++) {
    let gap = gapIntervals[g];
    let stIdx = timestamps.findIndex(t => t >= gap.start);
    let enIdx = timestamps.findIndex(t => t >= gap.end);
    if (stIdx === -1 || enIdx === -1) continue;
    let x1 = pad.l + stIdx * xStep;
    let x2 = pad.l + enIdx * xStep;
    ctx.beginPath();
    ctx.setLineDash([4,4]);
    ctx.strokeStyle = '#facc15';
    ctx.lineWidth = 1.5;
    ctx.moveTo(x1, pad.t);
    ctx.lineTo(x2, pad.t + chartH);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#facc15';
    ctx.font = '9px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Data gap \u2014 interpolation paused', (x1+x2)/2, pad.t + chartH/2 - 4);
    gapCount++;
  }
  document.getElementById('driftGapCount').textContent = gapCount;
  document.getElementById('driftTs').textContent = new Date().toLocaleTimeString();
}
function renderStreamChart() {
  let canvas = document.getElementById('streamChart');
  if (!canvas) return;
  let rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  let ctx = canvas.getContext('2d');
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  let w = rect.width, h = rect.height;
  ctx.clearRect(0,0,w,h);
  let data = streamData.cpu;
  if (data.length < 2) {
    ctx.fillStyle = '#4a5a70';
    ctx.font = '14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('Awaiting stream...', w/2, h/2);
    return;
  }
  let pad = { t:8, r:8, b:20, l:40 };
  let chartW = w - pad.l - pad.r;
  let chartH = h - pad.t - pad.b;
  let colors = { cpu:'#5af', memory:'#4ade80', latency:'#facc15', error_rate:'#f87171', throughput:'#a78bfa' };
  METRICS.forEach(metric => {
    let d = streamData[metric];
    let allForAxis = [];
    METRICS.forEach(m => allForAxis = allForAxis.concat(streamData[m]));
    let min = Math.min(...allForAxis);
    let max = Math.max(...allForAxis);
    let range = max - min || 1;
    let xStep = chartW / (d.length - 1 || 1);
    ctx.beginPath();
    ctx.strokeStyle = colors[metric] + 'cc';
    ctx.lineWidth = metric === 'cpu' ? 2 : 1;
    for (let i = 0; i < d.length; i++) {
      let x = pad.l + i * xStep;
      let y = pad.t + chartH - ((d[i] - min) / range * chartH);
      i === 0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
    }
    ctx.stroke();
    ctx.fillStyle = colors[metric] + '80';
    ctx.font = '9px system-ui';
    ctx.fillText(metric, pad.l + 4, pad.t + (METRICS.indexOf(metric) * 11) + 10);
  });
  let dataLen = streamData.cpu.length;
  let recentSlice = streamData.cpu.slice(-20);
  let recentMean = recentSlice.reduce((a,b)=>a+b,0)/recentSlice.length;
  let recentStd = Math.sqrt(recentSlice.map(v=>(v-recentMean)**2).reduce((a,b)=>a+b,0)/recentSlice.length)||1;
  let allForAxis = [];
  METRICS.forEach(m => allForAxis = allForAxis.concat(streamData[m]));
  let minA = Math.min(...allForAxis);
  let maxA = Math.max(...allForAxis);
  let rangeA = maxA - minA || 1;
  let recentMid = pad.t + chartH - ((recentMean - minA) / rangeA * chartH);
  ctx.fillStyle = 'rgba(74,222,128,0.08)';
  let bandH = (recentStd * 1.5 / rangeA) * chartH;
  ctx.fillRect(pad.l, recentMid - bandH, chartW, bandH*2);
  ctx.fillStyle = 'rgba(250,204,21,0.04)';
  ctx.fillRect(pad.l, recentMid - bandH*2, chartW, bandH*4);
  ctx.strokeStyle = '#4ade8040';
  ctx.setLineDash([3,3]);
  ctx.beginPath();
  ctx.moveTo(pad.l, recentMid);
  ctx.lineTo(pad.l+chartW, recentMid);
  ctx.stroke();
  ctx.setLineDash([]);
}
function updateRootCauses() {
  let list = document.getElementById('rootCauseList');
  if (!list) return;
  if (streamData.cpu.length < 15) {
    list.innerHTML = '<li style=color:#4a5a70;font-size:12px;>Collecting data (need 15+ points)...</li>';
    return;
  }
  let pairs = [];
  let metrics = METRICS;
  for (let i = 0; i < metrics.length; i++) {
    for (let j = i+1; j < metrics.length; j++) {
      let a = streamData[metrics[i]];
      let b = streamData[metrics[j]];
      let n = Math.min(a.length, b.length);
      let sliceA = a.slice(-n);
      let sliceB = b.slice(-n);
      let meanA = sliceA.reduce((x,y)=>x+y,0)/n;
      let meanB = sliceB.reduce((x,y)=>x+y,0)/n;
      let varA = sliceA.reduce((x,y)=>x+(y-meanA)**2,0);
      let varB = sliceB.reduce((x,y)=>x+(y-meanB)**2,0);
      let cov = sliceA.reduce((x,y,i)=>x+(y-meanA)*(sliceB[i]-meanB),0);
      let denom = Math.sqrt(varA*varB) || 1;
      let r = cov/denom;
      if (Math.abs(r) > 0.3) {
        pairs.push({ a: metrics[i], b: metrics[j], r });
      }
    }
  }
  if (pairs.length === 0) {
    list.innerHTML = '<li style=color:#4a5a70;font-size:12px;>No correlations with |r| > 0.3 found</li>';
    return;
  }
  pairs.sort((x,y) => Math.abs(y.r) - Math.abs(x.r));
  list.innerHTML = pairs.slice(0, 6).map(p => {
    let dir = p.r > 0 ? '\u2191' : '\u2193';
    return '<li><span class=metric-name>'+p.a+' <span class=arrow>'+dir+'</span> '+p.b+'</span> <span class=corr-val>r='+p.r.toFixed(3)+'</span></li>';
  }).join('');
}
function checkStatus() {
  let dot = document.getElementById('statusDot');
  let label = document.getElementById('statusLabel');
  let now = Date.now();
  if (streamData.cpu.length === 0) {
    dot.className = 'status-dot offline';
    label.textContent = 'Awaiting stream...';
    return;
  }
  let lastT = timestamps[timestamps.length - 1];
  let elapsed = now - lastT;
  if (elapsed > GAP_THRESHOLD_MS && elapsed < 10000) {
    dot.className = 'status-dot gap';
    label.textContent = 'Data gap (' + Math.round(elapsed/1000) + 's)';
  } else if (elapsed >= 10000) {
    dot.className = 'status-dot offline';
    label.textContent = 'Offline (' + Math.round(elapsed/1000) + 's)';
  } else {
    dot.className = 'status-dot online';
    label.textContent = 'Streaming';
  }
}
function tick() {
  refreshCount++;
  let pt = generateDataPoint();
  if (pt) {
    streamActive = true;
  }
  document.getElementById('pointCount').textContent = streamData.cpu.length;
  document.getElementById('refreshCount').textContent = refreshCount;
  if (streamData.cpu.length >= 2) {
    detectAnomalies();
    renderDriftChart();
    renderStreamChart();
  }
  checkStatus();
  if (pollingCycles <= 10 && streamData.cpu.length < 5) {
    let placeholder = document.getElementById('heatmapPlaceholder');
    if (placeholder) placeholder.style.display = 'flex';
  }
}
let interval = setInterval(tick, POLL_INTERVAL);
tick();
window.addEventListener('resize', () => {
  renderPulseChart();
  renderDriftChart();
  renderStreamChart();
  updateHeatmap();
});
console.log('Anomaly Detection Dashboard initialized');
console.log('Safari detected:', isSafari);
console.log('Max points:', MAX_POINTS, '| Window:', WINDOW, '| Threshold z:', ANOMALY_THRESHOLD);
})();
</script>
</body>
</html>
```