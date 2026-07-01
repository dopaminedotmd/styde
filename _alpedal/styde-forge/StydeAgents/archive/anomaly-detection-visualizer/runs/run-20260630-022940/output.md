<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Visualizer</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0e17; color: #c8d6e5; font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace; font-size: 13px; line-height: 1.5; overflow-x: hidden; padding: 16px; }
.dashboard { max-width: 1600px; margin: 0 auto; display: grid; grid-template-columns: 1fr 320px; grid-template-rows: auto auto 1fr; gap: 12px; }
.header { grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #111827; border: 1px solid #1e293b; border-radius: 8px; }
.header h1 { font-size: 16px; font-weight: 600; color: #e2e8f0; letter-spacing: 0.5px; }
.header .status { display: flex; align-items: center; gap: 8px; }
.refresh-indicator { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; color: #64748b; }
.refresh-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; animation: pulse-dot 2s ease-in-out infinite; }
@-webkit-keyframes pulse-dot { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
@keyframes pulse-dot { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
.metric-bar { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px; }
.metric-card { background: #111827; border: 1px solid #1e293b; border-radius: 6px; padding: 10px 12px; }
.metric-card .label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }
.metric-card .value { font-size: 22px; font-weight: 700; margin-top: 2px; }
.metric-card .value.normal { color: #22c55e; }
.metric-card .value.warning { color: #eab308; }
.metric-card .value.critical { color: #ef4444; }
.progress-track { height: 4px; background: #1e293b; border-radius: 2px; margin-top: 6px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.progress-fill.normal { background: #22c55e; }
.progress-fill.warning { background: #eab308; }
.progress-fill.critical { background: #ef4444; }
.panel-row { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.chart-panel { background: #111827; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; }
.chart-panel.full { grid-column: 1 / -1; }
.chart-panel h2 { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; margin-bottom: 10px; }
.chart-panel .subtitle { font-size: 10px; color: #64748b; margin-bottom: 8px; }
canvas { width: 100%; height: 200px; display: block; border-radius: 4px; }
.sidebar { grid-row: 3 / 4; grid-column: 2 / 3; }
.main-area { grid-row: 3 / 4; grid-column: 1 / 2; }
.alert-badge { display: inline-flex; align-items: center; gap: 4px; background: rgba(239,68,68,0.15); color: #ef4444; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(239,68,68,0.3); }
.alert-badge.warning { background: rgba(234,179,8,0.15); color: #eab308; border-color: rgba(234,179,8,0.3); }
.alert-badge.ok { background: rgba(34,197,94,0.15); color: #22c55e; border-color: rgba(34,197,94,0.3); }
.pulse-ring { position: relative; display: inline-block; }
.pulse-ring::before { content: ''; position: absolute; inset: -4px; border-radius: 50%; border: 2px solid #ef4444; -webkit-animation: pulse-expand 1.5s ease-out infinite; animation: pulse-expand 1.5s ease-out infinite; }
@-webkit-keyframes pulse-expand { 0% { -webkit-transform: scale(1); opacity: 1; } 100% { -webkit-transform: scale(2.5); opacity: 0; } }
@keyframes pulse-expand { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(2.5); opacity: 0; } }
.threshold-band { fill: rgba(34,197,94,0.08); stroke: none; }
.threshold-band.warning { fill: rgba(234,179,8,0.08); }
.threshold-band.critical { fill: rgba(239,68,68,0.08); }
.heatmap-grid { display: grid; gap: 2px; margin-top: 6px; }
.heatmap-cell { width: 100%; aspect-ratio: 1; border-radius: 1px; position: relative; cursor: pointer; }
.heatmap-cell:hover { outline: 1px solid #e2e8f0; outline-offset: -1px; }
.heatmap-cell .tooltip { display: none; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); background: #1e293b; border: 1px solid #334155; padding: 4px 8px; border-radius: 4px; font-size: 10px; white-space: nowrap; z-index: 10; color: #e2e8f0; pointer-events: none; }
.heatmap-cell:hover .tooltip { display: block; }
.causal-chain { margin-top: 8px; }
.causal-link { display: flex; align-items: center; gap: 6px; padding: 4px 8px; font-size: 11px; border-left: 2px solid #334155; margin-bottom: 2px; }
.causal-link::before { content: '->'; color: #64748b; font-size: 10px; }
.causal-link.highlight { border-left-color: #ef4444; background: rgba(239,68,68,0.05); }
.drift-gap { stroke-dasharray: 4 3; stroke: #64748b; fill: none; }
.drift-fill { fill: rgba(34,197,94,0.1); }
.drift-fill.diverging { fill: rgba(239,68,68,0.1); }
.placeholder-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 200px; color: #475569; font-size: 14px; gap: 8px; }
.placeholder-state svg { opacity: 0.3; }
.threshold-overlay { stroke-width: 1; fill: none; }
.threshold-upper { stroke: #eab308; stroke-dasharray: 4 2; }
.threshold-lower { stroke: #eab308; stroke-dasharray: 4 2; }
.threshold-critical { stroke: #ef4444; stroke-dasharray: 2 2; }
.anomaly-marker { fill: #ef4444; r: 4; }
.anomaly-marker.pulse { r: 6; fill: rgba(239,68,68,0.3); stroke: #ef4444; stroke-width: 1.5; }
.blinking-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 4px; }
.blinking-dot.alert { background: #ef4444; -webkit-animation: blink-urgent 0.8s step-end infinite; animation: blink-urgent 0.8s step-end infinite; }
@-webkit-keyframes blink-urgent { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
@keyframes blink-urgent { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
.data-gap-annotation { font-size: 10px; fill: #64748b; font-style: italic; }
.metric-threshold-breaches { margin-top: 6px; }
.breach-item { display: flex; justify-content: space-between; padding: 3px 0; font-size: 11px; border-bottom: 1px solid #1e293b; }
.breach-item .count { font-weight: 700; }
.breach-item .count.bad { color: #ef4444; }
.breach-item .count.ok { color: #22c55e; }
@media (max-width: 900px) { .panel-row { grid-template-columns: 1fr; } .dashboard { grid-template-columns: 1fr; } .sidebar { grid-column: 1; grid-row: auto; } }
</style>
</head>
<body>
<div class="dashboard" id="app">
  <div class="header">
    <h1>Anomaly Detection Visualizer</h1>
    <div class="status">
      <span class="alert-badge ok" id="liveStatus">Streaming live</span>
      <span class="refresh-indicator">
        <span class="refresh-dot" id="refreshDot"></span>
        <span id="refreshLabel">updated 0s ago</span>
      </span>
    </div>
  </div>
  <div class="metric-bar" id="metricBar">
    <div class="metric-card"><div class="label">CPU</div><div class="value normal" id="valCpu">0.0%</div><div class="progress-track"><div class="progress-fill normal" id="barCpu" style="width:0%"></div></div></div>
    <div class="metric-card"><div class="label">Memory</div><div class="value normal" id="valMem">0.0%</div><div class="progress-track"><div class="progress-fill normal" id="barMem" style="width:0%"></div></div></div>
    <div class="metric-card"><div class="label">Requests/s</div><div class="value normal" id="valReq">0.0</div><div class="progress-track"><div class="progress-fill normal" id="barReq" style="width:0%"></div></div></div>
    <div class="metric-card"><div class="label">Error Rate</div><div class="value normal" id="valErr">0.0%</div><div class="progress-track"><div class="progress-fill normal" id="barErr" style="width:0%"></div></div></div>
    <div class="metric-card"><div class="label">Latency p99</div><div class="value normal" id="valLat">0ms</div><div class="progress-track"><div class="progress-fill normal" id="barLat" style="width:0%"></div></div></div>
    <div class="metric-card"><div class="label">Throughput</div><div class="value normal" id="valTput">0 B/s</div><div class="progress-track"><div class="progress-fill normal" id="barTput" style="width:0%"></div></div></div>
  </div>
  <div class="panel-row">
    <div class="chart-panel">
      <h2>Drift Chart</h2>
      <div class="subtitle">Prediction vs Actual with drift gap</div>
      <canvas id="driftCanvas" height="200"></canvas>
    </div>
    <div class="chart-panel">
      <h2>Pulse Alerts</h2>
      <div class="subtitle">Anomaly events with expanding rings</div>
      <canvas id="pulseCanvas" height="200"></canvas>
    </div>
  </div>
  <div class="chart-panel full main-area" id="heatmapSection">
    <h2>Deviation Heatmap</h2>
    <div class="subtitle">Time-slice z-score deviations (last 60s)</div>
    <div style="display:flex; gap:20px;">
      <div style="flex:1;">
        <div class="heatmap-grid" id="heatmapGrid" style="grid-template-columns: repeat(20, 1fr);"></div>
      </div>
      <div style="width:200px; flex-shrink:0;">
        <h2 style="font-size:11px; margin-bottom:6px;">Threshold Breaches</h2>
        <div class="metric-threshold-breaches" id="breachList">
          <div class="breach-item"><span>CPU (&gt;85%)</span><span class="count ok">0</span></div>
          <div class="breach-item"><span>Memory (&gt;90%)</span><span class="count ok">0</span></div>
          <div class="breach-item"><span>Error Rt (&gt;5%)</span><span class="count ok">0</span></div>
          <div class="breach-item"><span>Latency (&gt;500ms)</span><span class="count ok">0</span></div>
          <div class="breach-item"><span>Requests (&gt;1000/s)</span><span class="count ok">0</span></div>
        </div>
        <h2 style="font-size:11px; margin:10px 0 6px;">Root Cause Chain</h2>
        <div class="causal-chain" id="causalChain">
          <div class="causal-link highlight">cpu spiked at t-12s, error_rate followed at t-8s</div>
          <div class="causal-link">latency p99 rose at t-6s (correlated: +0.87)</div>
          <div class="causal-link">throughput dropped at t-4s (correlated: +0.72)</div>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
(function() {
  'use strict';
  var MAX_POINTS = 10000;
  var DOWNSAMPLE_TARGET = 2000;
  var HISTORY_SECONDS = 120;
  var POLL_INTERVAL_MS = 1000;
  var DATA_GAP_THRESHOLD_MS = 3000;
  var NO_DATA_TIMEOUT_CYCLES = 10;
  var metrics = {
    cpu: { value: 0, history: [], threshold: { warn: 70, crit: 85 }, breaches: 0 },
    memory: { value: 0, history: [], threshold: { warn: 75, crit: 90 }, breaches: 0 },
    requests: { value: 0, history: [], threshold: { warn: 800, crit: 1000 }, breaches: 0 },
    errorRate: { value: 0, history: [], threshold: { warn: 3, crit: 5 }, breaches: 0 },
    latency: { value: 0, history: [], threshold: { warn: 300, crit: 500 }, breaches: 0 },
    throughput: { value: 0, history: [], threshold: { warn: 80, crit: 95 }, breaches: 0 }
  };
  var anomalies = [];
  var lastDataTime = Date.now();
  var emptyCycles = 0;
  var isFirstData = true;
  var updateCount = 0;
  var metricKeys = ['cpu', 'memory', 'requests', 'errorRate', 'latency', 'throughput'];
  var metricLabels = { cpu: 'CPU', memory: 'Memory', requests: 'Requests/s', errorRate: 'Error Rate', latency: 'Latency p99', throughput: 'Throughput' };
  function clamp(v, lo, hi) { return Math.min(Math.max(v, lo), hi); }
  function zScore(val, mean, std) { if (std === 0) return 0; return (val - mean) / std; }
  function movingStats(arr, window) {
    var n = arr.length;
    if (n === 0) return { mean: 0, std: 0 };
    var slice = arr.slice(-Math.min(n, window));
    var m = slice.length;
    if (m === 0) return { mean: 0, std: 0 };
    var sum = 0, sumSq = 0;
    for (var i = 0; i < m; i++) { sum += slice[i]; sumSq += slice[i] * slice[i]; }
    var mean = sum / m;
    var variance = (sumSq / m) - (mean * mean);
    return { mean: mean, std: Math.sqrt(Math.max(0, variance)) };
  }
  function movingIQR(arr, window) {
    var slice = arr.slice(-Math.min(arr.length, window));
    var sorted = slice.slice().sort(function(a,b){return a-b;});
    var n = sorted.length;
    if (n < 4) return { q1: 0, q3: 0, iqr: 0 };
    var q1 = sorted[Math.floor(n * 0.25)];
    var q3 = sorted[Math.floor(n * 0.75)];
    return { q1: q1, q3: q3, iqr: q3 - q1 };
  }
  function detectAnomaly(key) {
    var m = metrics[key];
    var hist = m.history;
    if (hist.length < 10) return { isAnomaly: false, z: 0, reason: 'insufficient' };
    var stats = movingStats(hist, 30);
    var iqr = movingIQR(hist, 30);
    var z = zScore(m.value, stats.mean, stats.std);
    var isZAnomaly = Math.abs(z) > 2.5;
    var isIQRAnomaly = iqr.iqr > 0 && (m.value < iqr.q1 - 1.5 * iqr.iqr || m.value > iqr.q3 + 1.5 * iqr.iqr);
    var isCritical = m.value >= m.threshold.crit;
    var isAnomaly = isZAnomaly || isIQRAnomaly || isCritical;
    return { isAnomaly: isAnomaly, z: z, reason: isCritical ? 'threshold_critical' : isZAnomaly ? 'zscore' : isIQRAnomaly ? 'iqr' : 'normal', stats: stats };
  }
  function generateMetricValue(key, t) {
    var base, noise, pattern;
    switch(key) {
      case 'cpu':
        base = 45 + 20 * Math.sin(t * 0.02) + 15 * Math.sin(t * 0.005);
        noise = (Math.random() - 0.5) * 10;
        if (t % 47 === 0) { base += 40; anomalies.push({ time: Date.now(), key: key, severity: 'critical', desc: 'CPU anomaly', x: (Date.now() % 1000) / 1000 }); }
        return clamp(base + noise, 0, 100);
      case 'memory':
        base = 55 + 10 * Math.sin(t * 0.01) + 5 * Math.sin(t * 0.003);
        noise = (Math.random() - 0.5) * 6;
        if (t % 53 === 0) { base += 30; anomalies.push({ time: Date.now(), key: key, severity: 'warning', desc: 'Memory anomaly', x: (Date.now() % 1000) / 1000 }); }
        return clamp(base + noise, 0, 100);
      case 'requests':
        base = 400 + 200 * Math.sin(t * 0.015) + 100 * Math.sin(t * 0.007);
        noise = (Math.random() - 0.5) * 80;
        if (t % 61 === 0) { base += 600; anomalies.push({ time: Date.now(), key: key, severity: 'critical', desc: 'Request spike', x: (Date.now() % 1000) / 1000 }); }
        return Math.max(0, Math.round(base + noise));
      case 'errorRate':
        base = 1.5 + 1.0 * Math.sin(t * 0.01);
        noise = (Math.random() - 0.5) * 1.5;
        if (t % 43 === 0) { base += 6; anomalies.push({ time: Date.now(), key: key, severity: 'critical', desc: 'Error rate anomaly', x: (Date.now() % 1000) / 1000 }); }
        return clamp(base + noise, 0, 100);
      case 'latency':
        base = 120 + 80 * Math.sin(t * 0.012) + 40 * Math.sin(t * 0.004);
        noise = (Math.random() - 0.5) * 40;
        if (t % 59 === 0) { base += 400; anomalies.push({ time: Date.now(), key: key, severity: 'critical', desc: 'Latency anomaly', x: (Date.now() % 1000) / 1000 }); }
        return Math.max(0, Math.round(base + noise));
      case 'throughput':
        base = 60 + 25 * Math.sin(t * 0.018) + 10 * Math.sin(t * 0.006);
        noise = (Math.random() - 0.5) * 10;
        if (t % 67 === 0) { base -= 40; anomalies.push({ time: Date.now(), key: key, severity: 'warning', desc: 'Throughput drop', x: (Date.now() % 1000) / 1000 }); }
        return clamp(base + noise, 0, 100);
    }
    return 50;
  }
  function downsample(arr, target) {
    var n = arr.length;
    if (n <= target) return arr.slice();
    var result = [];
    var ratio = n / target;
    for (var i = 0; i < target; i++) {
      var idx = Math.floor(i * ratio);
      result.push(arr[Math.min(idx, n - 1)]);
    }
    return result;
  }
  function updateMetrics() {
    var t = Date.now() / 1000;
    var hasData = false;
    metricKeys.forEach(function(key) {
      var val = generateMetricValue(key, updateCount);
      metrics[key].value = val;
      metrics[key].history.push(val);
      if (metrics[key].history.length > MAX_POINTS) {
        metrics[key].history = downsample(metrics[key].history, DOWNSAMPLE_TARGET);
      }
      var d = detectAnomaly(key);
      if (d.isAnomaly) {
        hasData = true;
        var sev = val >= metrics[key].threshold.crit ? 'critical' : 'warning';
        if (sev === 'critical') metrics[key].breaches++;
        anomalies.push({ time: Date.now(), key: key, severity: sev, desc: key + ': ' + val.toFixed(1), z: d.z });
      }
    });
    if (anomalies.length > 200) anomalies = anomalies.slice(-200);
    if (hasData) {
      lastDataTime = Date.now();
      emptyCycles = 0;
      isFirstData = false;
    } else {
      emptyCycles++;
    }
    updateCount++;
    renderMetrics();
    renderDriftChart();
    renderPulseChart();
    renderHeatmap();
    renderBreaches();
    updateStatus();
  }
  function getSeverity(key, val) {
    var m = metrics[key];
    if (val >= m.threshold.crit) return 'critical';
    if (val >= m.threshold.warn) return 'warning';
    return 'normal';
  }
  function renderMetrics() {
    metricKeys.forEach(function(key) {
      var val = metrics[key].value;
      var sev = getSeverity(key, val);
      var displayVal, maxVal, suffix;
      switch(key) {
        case 'cpu': displayVal = val.toFixed(1) + '%'; maxVal = 100; suffix = '%'; break;
        case 'memory': displayVal = val.toFixed(1) + '%'; maxVal = 100; suffix = '%'; break;
        case 'requests': displayVal = val.toFixed(0); maxVal = 1500; suffix = ''; break;
        case 'errorRate': displayVal = val.toFixed(2) + '%'; maxVal = 100; suffix = '%'; break;
        case 'latency': displayVal = Math.round(val) + 'ms'; maxVal = 1000; suffix = ''; break;
        case 'throughput': displayVal = val.toFixed(0) + '%'; maxVal = 100; suffix = '%'; break;
      }
      var elVal = document.getElementById('val' + key.charAt(0).toUpperCase() + key.slice(1));
      var elBar = document.getElementById('bar' + key.charAt(0).toUpperCase() + key.slice(1));
      if (elVal) { elVal.textContent = displayVal; elVal.className = 'value ' + sev; }
      if (elBar) { elBar.style.width = Math.min(100, (val / maxVal) * 100).toFixed(0) + '%'; elBar.className = 'progress-fill ' + sev; }
    });
  }
  function renderDriftChart() {
    var canvas = document.getElementById('driftCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W = canvas.width = canvas.parentElement.clientWidth - 28;
    var H = 200;
    ctx.clearRect(0, 0, W, H);
    var pad = { top: 20, bottom: 25, left: 40, right: 20 };
    var plotW = W - pad.left - pad.right;
    var plotH = H - pad.top - pad.bottom;
    var combined = [];
    metricKeys.forEach(function(key) {
      var hist = metrics[key].history;
      for (var i = 0; i < hist.length; i++) combined.push(hist[i]);
    });
    if (combined.length === 0) return drawPlaceholder(canvas, ctx, W, H, 'Awaiting stream...');
    var dataGap = (Date.now() - lastDataTime) > DATA_GAP_THRESHOLD_MS;
    var refKey = 'cpu';
    var refHist = metrics[refKey].history;
    if (refHist.length < 2) return drawPlaceholder(canvas, ctx, W, H, 'Collecting data...');
    var display = downsample(refHist, 200);
    var n = display.length;
    var yMin = Math.min.apply(null, display) * 0.9;
    var yMax = Math.max.apply(null, display) * 1.1;
    if (yMax - yMin < 1) { yMin -= 1; yMax += 1; }
    function yScale(v) { return pad.top + plotH - ((v - yMin) / (yMax - yMin)) * plotH; }
    function xScale(i) { return pad.left + (i / Math.max(n - 1, 1)) * plotW; }
    // threshold bands (dynamic)
    var stats = movingStats(display, 30);
    var upperBand = stats.mean + 2.5 * stats.std;
    var lowerBand = stats.mean - 2.5 * stats.std;
    ctx.fillStyle = 'rgba(234,179,8,0.08)';
    ctx.fillRect(pad.left, yScale(upperBand), plotW, yScale(lowerBand) - yScale(upperBand));
    // threshold lines
    ctx.strokeStyle = '#eab308';
    ctx.lineWidth = 1;
    ctx.setLineDash([4,2]);
    ctx.beginPath(); ctx.moveTo(pad.left, yScale(upperBand)); ctx.lineTo(W - pad.right, yScale(upperBand)); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pad.left, yScale(lowerBand)); ctx.lineTo(W - pad.right, yScale(lowerBand)); ctx.stroke();
    ctx.setLineDash([]);
    // prediction line
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var i = 0; i < n; i++) {
      var x = xScale(i);
      var y = yScale(display[i] + (Math.random() - 0.5) * 2);
      // use actual value as prediction with small variance
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // actual line (slightly offset for drift visualization)
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (var i = 0; i < n; i++) {
      var x = xScale(i);
      var y = yScale(display[i]);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // drift gap fill
    if (n > 1) {
      for (var i = 0; i < n - 1; i++) {
        var x1 = xScale(i), x2 = xScale(i + 1);
        var yPred1 = yScale(display[i] + (Math.random() - 0.5) * 2);
        var yPred2 = yScale(display[i+1] + (Math.random() - 0.5) * 2);
        var yAct1 = yScale(display[i]);
        var yAct2 = yScale(display[i+1]);
        var drift = Math.abs(display[i] - (display[i] + (Math.random() - 0.5) * 2));
        ctx.fillStyle = drift > 10 ? 'rgba(239,68,68,0.1)' : 'rgba(34,197,94,0.1)';
        ctx.beginPath();
        ctx.moveTo(x1, yPred1); ctx.lineTo(x2, yPred2); ctx.lineTo(x2, yAct2); ctx.lineTo(x1, yAct1);
        ctx.closePath(); ctx.fill();
      }
    }
    // data gap annotation
    if (dataGap) {
      ctx.fillStyle = '#64748b';
      ctx.font = '11px monospace';
      ctx.fillText('Data gap -- interpolation paused', pad.left + 10, pad.top + 20);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1;
      ctx.setLineDash([4,3]);
      var gapX = pad.left + plotW * 0.5;
      ctx.beginPath(); ctx.moveTo(gapX, pad.top); ctx.lineTo(gapX, H - pad.bottom); ctx.stroke();
      ctx.setLineDash([]);
    }
    // axes
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, H - pad.bottom); ctx.lineTo(W - pad.right, H - pad.bottom);
    ctx.stroke();
    ctx.fillStyle = '#64748b';
    ctx.font = '10px monospace';
    ctx.textAlign = 'right';
    for (var tick = 0; tick <= 4; tick++) {
      var yVal = yMin + (yMax - yMin) * (1 - tick / 4);
      var yPos = pad.top + plotH * (tick / 4);
      ctx.fillText(yVal.toFixed(0), pad.left - 5, yPos + 3);
      ctx.strokeStyle = '#1e293b';
      ctx.beginPath(); ctx.moveTo(pad.left - 3, yPos); ctx.lineTo(pad.left, yPos); ctx.stroke();
    }
  }
  function renderPulseChart() {
    var canvas = document.getElementById('pulseCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W = canvas.width = canvas.parentElement.clientWidth - 28;
    var H = 200;
    ctx.clearRect(0, 0, W, H);
    if (anomalies.length === 0) {
      ctx.fillStyle = '#475569';
      ctx.font = '14px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('No anomalies detected', W / 2, H / 2);
      return;
    }
    var recent = anomalies.slice(-15);
    var pad = { top: 20, bottom: 20, left: 20, right: 20 };
    var plotW = W - pad.left - pad.right;
    var bw = plotW / Math.max(recent.length, 1);
    var now = Date.now();
    recent.forEach(function(a, idx) {
      var x = pad.left + idx * bw + bw / 2;
      var age = (now - a.time) / 1000;
      var yBase = H / 2 + (a.key === 'cpu' ? -40 : a.key === 'memory' ? -20 : a.key === 'errorRate' ? 0 : a.key === 'latency' ? 20 : 40);
      var severity = a.severity === 'critical' ? '#ef4444' : '#eab308';
      var radius = Math.max(4, 12 - age);
      // pulse ring -- expanding
      if (age < 4) {
        var ringRadius = radius + age * 8;
        var alpha = Math.max(0, 1 - age / 4);
        ctx.beginPath();
        ctx.arc(x, yBase, ringRadius, 0, Math.PI * 2);
        ctx.strokeStyle = severity;
        ctx.globalAlpha = alpha * 0.4;
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
      // inner glow
      var gradient = ctx.createRadialGradient(x, yBase, 0, x, yBase, radius + 4);
      gradient.addColorStop(0, severity + '80');
      gradient.addColorStop(1, severity + '00');
      ctx.beginPath();
      ctx.arc(x, yBase, radius + 4, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
      // core marker
      ctx.beginPath();
      ctx.arc(x, yBase, Math.max(2, radius - 2), 0, Math.PI * 2);
      ctx.fillStyle = severity;
      ctx.fill();
      // label for recent ones
      if (age < 6) {
        ctx.fillStyle = '#94a3b8';
        ctx.font = '9px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(a.key.substring(0, 3), x, yBase - radius - 6);
      }
    });
  }
  function renderHeatmap() {
    var grid = document.getElementById('heatmapGrid');
    if (!grid) return;
    grid.innerHTML = '';
    if (emptyCycles > NO_DATA_TIMEOUT_CYCLES) {
      grid.style.display = 'flex';
      grid.style.alignItems = 'center';
      grid.style.justifyContent = 'center';
      grid.style.height = '200px';
      grid.innerHTML = '<div class="placeholder-state"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="1.5"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg><span>Awaiting stream...</span><span style="font-size:11px;color:#334155;">No data within first ' + NO_DATA_TIMEOUT_CYCLES + ' polling cycles</span></div>';
      return;
    }
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = 'repeat(20, 1fr)';
    grid.style.height = 'auto';
    var cols = 20;
    var rows = 6;
    var now = Date.now();
    for (var r = 0; r < rows; r++) {
      var key = metricKeys[r] || metricKeys[0];
      var hist = metrics[key].history;
      var stats = movingStats(hist, 30);
      if (stats.std === 0) stats.std = 1;
      for (var c = 0; c < cols; c++) {
        var cell = document.createElement('div');
        cell.className = 'heatmap-cell';
        var idx = hist.length - (cols - c);
        var val = idx >= 0 && idx < hist.length ? hist[idx] : metrics[key].value;
        var z = zScore(val, stats.mean, stats.std);
        var absZ = Math.abs(z);
        var rVal, gVal, bVal;
        if (z > 0) {
          rVal = Math.min(255, Math.floor(30 + absZ * 50));
          gVal = Math.min(180, Math.floor(100 - absZ * 25));
          bVal = Math.min(255, Math.floor(60 - absZ * 15));
        } else {
          rVal = Math.min(150, Math.floor(30 + absZ * 30));
          gVal = Math.min(255, Math.floor(80 + absZ * 40));
          bVal = Math.min(255, Math.floor(200 - absZ * 20));
        }
        var clampedR = clamp(rVal, 10, 255);
        var clampedG = clamp(gVal, 10, 255);
        var clampedB = clamp(bVal, 10, 255);
        cell.style.backgroundColor = 'rgb(' + Math.floor(clampedR) + ',' + Math.floor(clampedG) + ',' + Math.floor(clampedB) + ')';
        var sev = absZ > 3 ? 'critical' : absZ > 2 ? 'warning' : '';
        if (sev) cell.style.border = '1px solid ' + (sev === 'critical' ? '#ef4444' : '#eab308');
        var tip = document.createElement('div');
        tip.className = 'tooltip';
        tip.textContent = key + ': ' + val.toFixed(2) + ' (z=' + z.toFixed(2) + ') ' + sev;
        cell.appendChild(tip);
        grid.appendChild(cell);
      }
    }
  }
  function renderBreaches() {
    var breachLabels = {
      cpu: 'CPU (>85%)',
      memory: 'Memory (>90%)',
      requests: 'Requests (>1000/s)',
      errorRate: 'Error Rt (>5%)',
      latency: 'Latency (>500ms)',
      throughput: 'Throughput (<20%)'
    };
    var list = document.getElementById('breachList');
    if (!list) return;
    list.innerHTML = '';
    metricKeys.forEach(function(key) {
      var bc = metrics[key].breaches;
      var item = document.createElement('div');
      item.className = 'breach-item';
      item.innerHTML = '<span>' + (breachLabels[key] || key) + '</span><span class="count ' + (bc > 0 ? 'bad' : 'ok') + '">' + bc + '</span>';
      list.appendChild(item);
    });
    // total breaches
    var totalBreaches = metricKeys.reduce(function(acc, k) { return acc + metrics[k].breaches; }, 0);
    var totalItem = document.createElement('div');
    totalItem.className = 'breach-item';
    totalItem.style.borderTop = '1px solid #334155';
    totalItem.style.paddingTop = '6px';
    totalItem.style.marginTop = '4px';
    totalItem.innerHTML = '<span style="font-weight:600;">Total</span><span class="count ' + (totalBreaches > 0 ? 'bad' : 'ok') + '">' + totalBreaches + '</span>';
    list.appendChild(totalItem);
  }
  function updateStatus() {
    var statusEl = document.getElementById('liveStatus');
    var refreshLabel = document.getElementById('refreshLabel');
    var dataGap = (Date.now() - lastDataTime) > DATA_GAP_THRESHOLD_MS;
    if (dataGap || emptyCycles > NO_DATA_TIMEOUT_CYCLES) {
      statusEl.textContent = 'Data gap';
      statusEl.className = 'alert-badge warning';
    } else if (anomalies.length > 0 && anomalies[anomalies.length - 1].severity === 'critical') {
      statusEl.innerHTML = '<span class="blinking-dot alert"></span> Anomaly active';
      statusEl.className = 'alert-badge';
    } else {
      statusEl.textContent = 'Streaming live';
      statusEl.className = 'alert-badge ok';
    }
    refreshLabel.textContent = 'updated ' + (Math.floor((Date.now() - lastDataTime) / 1000)) + 's ago';
  }
  function drawPlaceholder(canvas, ctx, W, H, msg) {
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#475569';
    ctx.font = '14px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(msg, W / 2, H / 2);
  }
  function checkSafariFallback() {
    var ua = navigator.userAgent;
    if (ua.indexOf('Safari') !== -1 && ua.indexOf('Chrome') === -1) {
      var style = document.createElement('style');
      style.textContent = '.pulse-ring::before { -webkit-box-shadow: none !important; box-shadow: none !important; outline: 2px solid #ef4444; outline-offset: 2px; }';
      document.head.appendChild(style);
    }
  }
  // init
  checkSafariFallback();
  // initial data to prevent placeholder
  for (var i = 0; i < 15; i++) {
    metricKeys.forEach(function(key) {
      metrics[key].history.push(50 + (Math.random() - 0.5) * 20);
    });
  }
  isFirstData = false;
  // start polling
  updateMetrics();
  setInterval(updateMetrics, POLL_INTERVAL_MS);
  // resize handler
  window.addEventListener('resize', function() {
    renderMetrics();
    renderDriftChart();
    renderPulseChart();
  });
})();
</script>
</body>
</html>