<html>
<head>
<meta charset="UTF-8">
<title>Anomaly Detection Pulse Panel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
#app{display:grid;grid-template-columns:1fr 340px;grid-template-rows:auto 1fr auto;height:100vh;gap:0}
#header{grid-column:1/-1;padding:10px 20px;background:#111827;border-bottom:1px solid #1e293b;display:flex;align-items:center;justify-content:space-between}
#header h1{font-size:16px;font-weight:600;color:#f1f5f9;letter-spacing:.5px}
#header .stats{display:flex;gap:20px;font-size:12px}
#header .stats span{opacity:.7}
#header .stats strong{color:#e2e8f0;opacity:1}
#main{position:relative;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
#heatmap-section,#drift-section{flex-shrink:0}
#heatmap-section label,#drift-section label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:3px;display:block}
.section-label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:3px}
#pulse-canvas{flex:1;width:100%;border-radius:8px;border:1px solid #1e293b;background:#0f172a;cursor:crosshair}
#heatmap-canvas{width:100%;height:52px;border-radius:6px;border:1px solid #1e293b}
#drift-canvas{width:100%;height:48px;border-radius:6px;border:1px solid #1e293b}
#sidebar{background:#0f172a;border-left:1px solid #1e293b;padding:12px;display:flex;flex-direction:column;gap:10px;overflow-y:auto}
#sidebar h2{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;border-bottom:1px solid #1e293b;padding-bottom:6px}
#root-cause-list{list-style:none;display:flex;flex-direction:column;gap:4px}
#root-cause-list li{font-size:11px;padding:6px 8px;background:#1e293b;border-radius:4px;border-left:3px solid #f59e0b;display:flex;justify-content:space-between;align-items:center}
#root-cause-list li .metric{color:#e2e8f0}
#root-cause-list li .corr{color:#94a3b8;font-size:10px}
#alert-log{flex:1;overflow-y:auto;font-size:11px;display:flex;flex-direction:column;gap:3px}
.alert-entry{padding:5px 6px;background:#1e293b;border-radius:3px;border-left:3px solid #ef4444;animation:flashIn .3s ease}
.alert-entry .time{color:#64748b;font-size:10px}
.alert-entry .msg{color:#f1f5f9}
.alert-entry.sev-high{border-left-color:#ef4444}
.alert-entry.sev-med{border-left-color:#f59e0b}
.alert-entry.sev-low{border-left-color:#3b82f6}
@keyframes flashIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}
#status-bar{grid-column:1/-1;background:#111827;border-top:1px solid #1e293b;padding:6px 20px;display:flex;justify-content:space-between;font-size:10px;color:#64748b}
.badge{display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px;font-weight:600}
.badge-ok{background:#065f46;color:#6ee7b7}
.badge-warn{background:#78350f;color:#fbbf24}
.badge-crit{background:#7f1d1d;color:#fca5a5}
</style>
</head>
<body>
<div id="app">
  <div id="header">
    <h1>ANOMALY PULSE — Real-Time Detection</h1>
    <div class="stats">
      <span>alerts: <strong id="alert-count">0</strong></span>
      <span>fps: <strong id="fps-display">60</strong></span>
      <span>latency: <strong id="latency-display">0ms</strong></span>
      <span>status: <span id="status-badge" class="badge badge-ok">nominal</span></span>
    </div>
  </div>
  <div id="main">
    <canvas id="pulse-canvas"></canvas>
    <div id="heatmap-section">
      <label>DEVIATION HEATMAP — last 60s</label>
      <canvas id="heatmap-canvas"></canvas>
    </div>
    <div id="drift-section">
      <label>MODEL DRIFT — prediction vs actual</label>
      <canvas id="drift-canvas"></canvas>
    </div>
  </div>
  <div id="sidebar">
    <h2>ROOT CAUSE CHAIN</h2>
    <ul id="root-cause-list"></ul>
    <h2>ALERT LOG</h2>
    <div id="alert-log"></div>
  </div>
  <div id="status-bar">
    <span>sliding window: 120pts | detect throttle: 4 frames | incr. delta: enabled</span>
    <span>stats: z-score + IQR + CUSUM</span>
  </div>
</div>
<script>
(function(){
'use strict';
// ───── CONFIGURATION ─────
const WINDOW_SIZE = 120;
const THROTTLE_DETECT = 4;
const Z_THRESHOLD = 2.5;
const IQR_MULTIPLIER = 1.5;
const MAX_HISTORY = 600;
const PULSE_LIFETIME = 2000;
const PULSE_MAX_RADIUS = 80;
const HEATMAP_BUCKETS = 60;
const ROOT_CAUSE_WINDOW = 30;
// ───── CACHED GRADIENTS ─────
let gradCache = {
  driftFill: null,
  heatmap: null,
  pulse: null,
  thresholdBand: null
};
function ensureGradients(ctx, w, h) {
  if (!gradCache.driftFill || gradCache.driftFill_w !== w) {
    const g = ctx.createLinearGradient(0,0,0,h);
    g.addColorStop(0,'rgba(34,197,94,0.25)');
    g.addColorStop(0.5,'rgba(234,179,8,0.15)');
    g.addColorStop(1,'rgba(239,68,68,0.25)');
    gradCache.driftFill = g;
    gradCache.driftFill_w = w;
  }
  if (!gradCache.heatmap || gradCache.heatmap_w !== w) {
    const g = ctx.createLinearGradient(0,0,w,0);
    g.addColorStop(0,'#22c55e');
    g.addColorStop(0.25,'#eab308');
    g.addColorStop(0.5,'#f97316');
    g.addColorStop(0.75,'#ef4444');
    g.addColorStop(1,'#7c3aed');
    gradCache.heatmap = g;
    gradCache.heatmap_w = w;
  }
  if (!gradCache.pulse) {
    const g = ctx.createRadialGradient(0,0,0,0,0,PULSE_MAX_RADIUS);
    g.addColorStop(0,'rgba(239,68,68,0)');
    g.addColorStop(0.4,'rgba(239,68,68,0.35)');
    g.addColorStop(0.7,'rgba(239,68,68,0.15)');
    g.addColorStop(1,'rgba(239,68,68,0)');
    gradCache.pulse = g;
  }
  if (!gradCache.thresholdBand || gradCache.thresholdBand_w !== w) {
    const g = ctx.createLinearGradient(0,0,0,h);
    g.addColorStop(0,'rgba(59,130,246,0.08)');
    g.addColorStop(0.5,'rgba(59,130,246,0.02)');
    g.addColorStop(1,'rgba(59,130,246,0.08)');
    gradCache.thresholdBand = g;
    gradCache.thresholdBand_w = w;
  }
}
// ───── STATE ─────
const data = {
  timestamps: [],
  values: [],
  predictions: [],
  mean: null,
  std: null,
  q1: null,
  q3: null,
  anomalies: [],  // {idx, severity, method, timestamp}
  windowValues: function() { return this.values.slice(-WINDOW_SIZE); }
};
const pulses = []; // {x, y, startTime, severity, color}
const heatmapBuffer = new Float32Array(HEATMAP_BUCKETS);
const alertLog = [];
const rootCauses = [];
let frameCount = 0;
let lastDetectFrame = 0;
let lastTime = performance.now();
let currentFps = 60;
// ───── STREAM SIMULATION ─────
const METRICS = ['cpu_pct','mem_gb','req_latency','disk_iops','net_throughput'];
const metricHistory = {};
METRICS.forEach(m => { metricHistory[m] = []; });
// Generate one tick of correlated metrics
function generateMetricsTick(t) {
  const base = 50 + 15 * Math.sin(t * 0.02) + 5 * Math.sin(t * 0.07);
  const cpu = base + (Math.random() - 0.5) * 8;
  const mem = 60 + 10 * Math.sin(t * 0.015) + (Math.random() - 0.5) * 4;
  const lat = 120 + 30 * Math.sin(t * 0.025) + (Math.random() - 0.5) * 20;
  const disk = 200 + 60 * Math.sin(t * 0.01) + (Math.random() - 0.5) * 30;
  const net = 800 + 200 * Math.sin(t * 0.018) + (Math.random() - 0.5) * 100;
  return {cpu_pct:cpu, mem_gb:mem, req_latency:lat, disk_iops:disk, net_throughput:net};
}
function maybeInjectAnomaly(t, metrics) {
  // Inject anomalies with ~3% probability, clustered
  if (Math.random() > 0.03) return null;
  const severity = Math.random() < 0.2 ? 'high' : Math.random() < 0.5 ? 'med' : 'low';
  const shift = severity === 'high' ? 40 + Math.random() * 25 :
                severity === 'med' ? 20 + Math.random() * 15 :
                8 + Math.random() * 8;
  const direction = Math.random() < 0.5 ? 1 : -1;
  const affected = Math.floor(Math.random() * 3) + 1;
  const keys = Object.keys(metrics);
  const result = {};
  for (let i = 0; i < affected; i++) {
    const k = keys[Math.floor(Math.random() * keys.length)];
    result[k] = metrics[k] + direction * shift * (1 + Math.random() * 0.3);
  }
  return {severity, shift, affected: Object.keys(result), values: result};
}
// ───── DETECTION ENGINE (incremental-aware) ─────
function computeStats(values) {
  if (!values || values.length < 4) return null;
  const n = values.length;
  const sorted = values.slice().sort((a,b)=>a-b);
  const mean = values.reduce((s,v)=>s+v,0) / n;
  const variance = values.reduce((s,v)=>s+(v-mean)**2,0) / (n-1);
  const std = Math.sqrt(variance);
  const q1 = sorted[Math.floor(n*0.25)];
  const q3 = sorted[Math.floor(n*0.75)];
  const iqr = q3 - q1;
  return {mean, std, q1, q3, iqr};
}
function detectAnomalies(values, timestamps) {
  // Only run on new data since last detection (incremental)
  if (values.length < 10) return [];
  const stats = computeStats(values);
  if (!stats) return [];
  const newAnomalies = [];
  const startIdx = Math.max(0, values.length - WINDOW_SIZE);
  // Z-score detection on trailing window
  const windowVals = values.slice(-WINDOW_SIZE);
  const windowTimestamps = timestamps.slice(-WINDOW_SIZE);
  const wStats = computeStats(windowVals);
  if (wStats && wStats.std > 0.001) {
    for (let i = 0; i < windowVals.length; i++) {
      const z = Math.abs((windowVals[i] - wStats.mean) / wStats.std);
      if (z > Z_THRESHOLD) {
        newAnomalies.push({
          idx: startIdx + i,
          value: windowVals[i],
          zScore: z,
          severity: z > 4 ? 'high' : z > 3 ? 'med' : 'low',
          method: 'z-score',
          timestamp: windowTimestamps[i]
        });
      }
    }
  }
  // IQR detection
  if (wStats && wStats.iqr > 0.001) {
    const lower = wStats.q1 - IQR_MULTIPLIER * wStats.iqr;
    const upper = wStats.q3 + IQR_MULTIPLIER * wStats.iqr;
    for (let i = 0; i < windowVals.length; i++) {
      if (windowVals[i] < lower || windowVals[i] > upper) {
        const dist = Math.min(
          Math.abs(windowVals[i] - lower),
          Math.abs(windowVals[i] - upper)
        ) / wStats.iqr;
        if (dist > 0.5 && !newAnomalies.some(a => a.idx === startIdx + i)) {
          const z = Math.abs((windowVals[i] - wStats.mean) / wStats.std);
          newAnomalies.push({
            idx: startIdx + i,
            value: windowVals[i],
            zScore: z,
            severity: dist > 2 ? 'high' : dist > 1 ? 'med' : 'low',
            method: 'IQR',
            timestamp: windowTimestamps[i]
          });
        }
      }
    }
  }
  // CUSUM change-point detection (simplified CUSUM)
  if (windowVals.length > 20) {
    const targetMean = wStats.mean;
    let cumSum = 0;
    const cusumThreshold = 3 * wStats.std;
    for (let i = 5; i < windowVals.length; i++) {
      cumSum += (windowVals[i] - targetMean);
      if (Math.abs(cumSum) > cusumThreshold) {
        const dist = Math.abs(cumSum) / cusumThreshold;
        if (!newAnomalies.some(a => Math.abs(a.idx - (startIdx + i)) < 3)) {
          newAnomalies.push({
            idx: startIdx + i,
            value: windowVals[i],
            zScore: dist * 2.5,
            severity: dist > 2.5 ? 'high' : dist > 1.5 ? 'med' : 'low',
            method: 'CUSUM',
            timestamp: windowTimestamps[i]
          });
        }
        cumSum = 0;
      }
    }
  }
  // Deduplicate by index
  const seen = new Set();
  return newAnomalies.filter(a => {
    if (seen.has(a.idx)) return false;
    seen.add(a.idx);
    return true;
  });
}
// ───── ROOT CAUSE SUGGESTION ─────
function computeRootCauses(currentMetrics, anomalyIdx) {
  const results = [];
  const anomalyTime = data.timestamps[anomalyIdx] || 0;
  for (const [name, hist] of Object.entries(metricHistory)) {
    if (hist.length < ROOT_CAUSE_WINDOW * 2) continue;
    const recent = hist.slice(-ROOT_CAUSE_WINDOW);
    const prior = hist.slice(-ROOT_CAUSE_WINDOW * 2, -ROOT_CAUSE_WINDOW);
    if (prior.length < 5 || recent.length < 5) continue;
    const priorMean = prior.reduce((s,v)=>s+v,0)/prior.length;
    const recentMean = recent.reduce((s,v)=>s+v,0)/recent.length;
    const shift = (recentMean - priorMean) / (priorMean || 1);
    if (Math.abs(shift) > 0.08) {
      results.push({
        metric: name,
        shift: shift,
        absShift: Math.abs(shift),
        leadTime: ROOT_CAUSE_WINDOW,
        direction: shift > 0 ? 'up' : 'down'
      });
    }
  }
  // Cross-correlation with primary metric
  const primaryHist = metricHistory['cpu_pct'] || [];
  for (const [name, hist] of Object.entries(metricHistory)) {
    if (name === 'cpu_pct' || hist.length < 20 || primaryHist.length < 20) continue;
    const n = Math.min(hist.length, primaryHist.length);
    const pMean = primaryHist.slice(-n).reduce((s,v)=>s+v,0)/n;
    const hMean = hist.slice(-n).reduce((s,v)=>s+v,0)/n;
    let num = 0, denP = 0, denH = 0;
    for (let i = 0; i < n; i++) {
      const dp = primaryHist[primaryHist.length - n + i] - pMean;
      const dh = hist[hist.length - n + i] - hMean;
      num += dp * dh;
      denP += dp * dp;
      denH += dh * dh;
    }
    const corr = denP && denH ? num / Math.sqrt(denP * denH) : 0;
    if (Math.abs(corr) > 0.4 && !results.some(r => r.metric === name && Math.abs(r.corr||0) > Math.abs(corr))) {
      results.push({
        metric: name,
        corr: corr,
        leadTime: 0,
        direction: corr > 0 ? 'up' : 'down'
      });
    }
  }
  results.sort((a,b) => Math.abs(b.absShift || b.corr||0) - Math.abs(a.absShift || a.corr||0));
  return results.slice(0, 5);
}
// ───── PULSE ANIMATION ─────
function spawnPulse(canvasX, canvasY, severity) {
  const colors = {
    high: '#ef4444',
    med: '#f59e0b',
    low: '#3b82f6'
  };
  pulses.push({
    x: canvasX, y: canvasY,
    startTime: performance.now(),
    severity: severity,
    color: colors[severity] || '#ef4444'
  });
}
function updatePulses(now) {
  for (let i = pulses.length - 1; i >= 0; i--) {
    if (now - pulses[i].startTime > PULSE_LIFETIME) {
      pulses.splice(i, 1);
    }
  }
}
// ───── RENDERING ─────
function renderPulseCanvas(ctx, w, h) {
  const dpr = window.devicePixelRatio || 1;
  ctx.clearRect(0,0,w*dpr,h*dpr);
  ctx.scale(1,1); // already scaled via CSS
  const pad = {top:20, bottom:25, left:55, right:20};
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  if (plotW <= 0 || plotH <= 0) return;
  const vals = data.values;
  const n = vals.length;
  if (n < 2) return;
  // Scale
  let min = Infinity, max = -Infinity;
  const windowVals = vals.slice(-WINDOW_SIZE);
  for (const v of windowVals) {
    if (v < min) min = v;
    if (v > max) max = v;
  }
  const range = max - min || 1;
  const padRange = range * 0.12;
  min -= padRange;
  max += padRange;
  function xPos(i) {
    return pad.left + (i / (WINDOW_SIZE - 1 || 1)) * plotW;
  }
  function yPos(v) {
    return pad.top + plotH - ((v - min) / (max - min)) * plotH;
  }
  const ctx2 = ctx;
  const dpr2 = dpr;
  // Draw grid
  ctx2.strokeStyle = 'rgba(51,65,85,0.3)';
  ctx2.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + (i / 4) * plotH;
    ctx2.beginPath();
    ctx2.moveTo(pad.left, y);
    ctx2.lineTo(w - pad.right, y);
    ctx2.stroke();
    ctx2.fillStyle = '#475569';
    ctx2.font = '9px sans-serif';
    ctx2.textAlign = 'right';
    const label = (max - (i/4)*range).toFixed(1);
    ctx2.fillText(label, pad.left - 5, y + 3);
  }
  // Threshold bands (dynamic)
  if (data.mean !== null && data.std !== null) {
    const upper2 = yPos(data.mean + 2 * data.std);
    const lower2 = yPos(data.mean - 2 * data.std);
    const upper3 = yPos(data.mean + 3 * data.std);
    const lower3 = yPos(data.mean - 3 * data.std);
    ctx2.fillStyle = gradCache.thresholdBand || 'rgba(59,130,246,0.05)';
    ctx2.fillRect(pad.left, upper3, plotW, lower3 - upper3);
    ctx2.setLineDash([4,4]);
    ctx2.strokeStyle = 'rgba(59,130,246,0.3)';
    ctx2.lineWidth = 1;
    ctx2.beginPath(); ctx2.moveTo(pad.left, upper2); ctx2.lineTo(w-pad.right, upper2); ctx2.stroke();
    ctx2.beginPath(); ctx2.moveTo(pad.left, lower2); ctx2.lineTo(w-pad.right, lower2); ctx2.stroke();
    ctx2.setLineDash([]);
    ctx2.strokeStyle = 'rgba(239,68,68,0.2)';
    ctx2.beginPath(); ctx2.moveTo(pad.left, upper3); ctx2.lineTo(w-pad.right, upper3); ctx2.stroke();
    ctx2.beginPath(); ctx2.moveTo(pad.left, lower3); ctx2.lineTo(w-pad.right, lower3); ctx2.stroke();
  }
  // Main line
  const startIdx = Math.max(0, n - WINDOW_SIZE);
  ctx2.beginPath();
  ctx2.strokeStyle = '#38bdf8';
  ctx2.lineWidth = 1.5;
  for (let i = 0; i < windowVals.length; i++) {
    const x = xPos(i);
    const y = yPos(vals[startIdx + i]);
    if (i === 0) ctx2.moveTo(x,y);
    else ctx2.lineTo(x,y);
  }
  ctx2.stroke();
  // Drift fill (prediction vs actual gap)
  if (data.predictions.length >= 2) {
    const predStart = Math.max(0, data.predictions.length - WINDOW_SIZE);
    const predWindow = data.predictions.slice(-WINDOW_SIZE);
    ctx2.beginPath();
    for (let i = 0; i < predWindow.length; i++) {
      const x = xPos(i);
      const y = yPos(predWindow[i]);
      if (i === 0) ctx2.moveTo(x,y);
      else ctx2.lineTo(x,y);
    }
    ctx2.strokeStyle = 'rgba(168,85,247,0.5)';
    ctx2.lineWidth = 1;
    ctx2.setLineDash([3,3]);
    ctx2.stroke();
    ctx2.setLineDash([]);
    // Fill gap between prediction and actual
    ctx2.beginPath();
    for (let i = 0; i < predWindow.length; i++) {
      const x = xPos(i);
      const y = yPos(predWindow[i]);
      if (i === 0) ctx2.moveTo(x,y);
      else ctx2.lineTo(x,y);
    }
    // Back along actual
    for (let i = predWindow.length - 1; i >= 0; i--) {
      const x = xPos(i);
      const y = yPos(vals[Math.max(0, n - predWindow.length + i)]);
      ctx2.lineTo(x,y);
    }
    ctx2.closePath();
    ctx2.fillStyle = gradCache.driftFill || 'rgba(34,197,94,0.1)';
    ctx2.fill();
  }
  // Anomaly markers + pulse origins
  for (const a of data.anomalies) {
    const relIdx = a.idx - startIdx;
    if (relIdx < 0 || relIdx >= windowVals.length) continue;
    const x = xPos(relIdx);
    const y = yPos(a.value);
    const color = a.severity === 'high' ? '#ef4444' :
                  a.severity === 'med' ? '#f59e0b' : '#3b82f6';
    ctx2.beginPath();
    ctx2.arc(x, y, a.severity === 'high' ? 5 : a.severity === 'med' ? 4 : 3, 0, Math.PI*2);
    ctx2.fillStyle = color;
    ctx2.fill();
    ctx2.strokeStyle = 'rgba(255,255,255,0.3)';
    ctx2.lineWidth = 1;
    ctx2.stroke();
  }
  // Pulse rings
  const now = performance.now();
  for (const p of pulses) {
    const age = (now - p.startTime) / PULSE_LIFETIME;
    if (age > 1) continue;
    const radius = age * PULSE_MAX_RADIUS;
    const alpha = 1 - age;
    // Outer ring
    ctx2.beginPath();
    ctx2.arc(p.x, p.y, radius, 0, Math.PI*2);
    ctx2.strokeStyle = p.color.replace(')', `,${alpha*0.6})`).replace('rgb', 'rgba');
    if (!p.color.includes('rgba')) {
      ctx2.strokeStyle = `rgba(${parseInt(p.color.slice(1,3),16)},${parseInt(p.color.slice(3,5),16)},${parseInt(p.color.slice(5,7),16)},${alpha*0.5})`;
    }
    ctx2.lineWidth = 2 * (1 - age) + 1;
    ctx2.stroke();
    // Inner glow
    const fillColor = p.color.startsWith('#')
      ? `rgba(${parseInt(p.color.slice(1,3),16)},${parseInt(p.color.slice(3,5),16)},${parseInt(p.color.slice(5,7),16)},${alpha*0.12})`
      : `rgba(239,68,68,${alpha*0.12})`;
    ctx2.beginPath();
    ctx2.arc(p.x, p.y, radius * 0.5, 0, Math.PI*2);
    ctx2.fillStyle = fillColor;
    ctx2.fill();
  }
  // Labels
  ctx2.fillStyle = '#64748b';
  ctx2.font = '9px sans-serif';
  ctx2.textAlign = 'center';
  for (let i = 0; i <= 4; i++) {
    const x = pad.left + (i/4)*plotW;
    const label = -(WINDOW_SIZE - 1) + Math.floor(i/4*(WINDOW_SIZE-1));
    ctx2.fillText(`${label}s`, x, h - 5);
  }
  ctx2.fillStyle = '#475569';
  ctx2.font = '9px sans-serif';
  ctx2.textAlign = 'left';
  ctx2.fillText('prediction (dashed)', w - pad.right - 130, pad.top + 10);
}
function renderHeatmap(ctx, w, h) {
  const dpr = window.devicePixelRatio || 1;
  ctx.clearRect(0,0,w*dpr,h*dpr);
  if (heatmapBuffer.length < 2) return;
  const maxAbs = Math.max(0.5, ...heatmapBuffer.map(Math.abs));
  const cellW = w / HEATMAP_BUCKETS;
  const cellH = h;
  for (let i = 0; i < HEATMAP_BUCKETS; i++) {
    const z = heatmapBuffer[i] || 0;
    const intensity = Math.min(1, Math.abs(z) / maxAbs);
    let r,g,b;
    if (z > 0) {
      r = 239; g = Math.round(68 + (187-68)*(1-intensity)); b = Math.round(68 + (68-68)*(1-intensity));
    } else {
      r = Math.round(34 + (205-34)*(1-intensity)); g = 197; b = 94;
    }
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    ctx.fillRect(i*cellW, 0, cellW + 0.5, cellH);
  }
  // Severity markers
  const markerY = h * 0.05;
  ctx.fillStyle = '#ef4444';
  ctx.font = '7px sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText('+3σ', w - 2, markerY + 6);
}
function renderDrift(ctx, w, h) {
  const dpr = window.devicePixelRatio || 1;
  ctx.clearRect(0,0,w*dpr,h*dpr);
  const pad = {left:40, right:15, top:8, bottom:10};
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  if (plotW <= 0 || plotH <= 0) return;
  const n = Math.min(data.values.length, data.predictions.length, WINDOW_SIZE);
  if (n < 2) return;
  const startIdx = data.values.length - n;
  const vals = data.values.slice(startIdx);
  const preds = data.predictions.slice(startIdx);
  let minV = Infinity, maxV = -Infinity;
  for (let i = 0; i < n; i++) {
    minV = Math.min(minV, vals[i], preds[i]);
    maxV = Math.max(maxV, vals[i], preds[i]);
  }
  const range2 = maxV - minV || 1;
  const padR = range2 * 0.15;
  minV -= padR;
  maxV += padR;
  function xP(i) { return pad.left + (i / (n-1)) * plotW; }
  function yP(v) { return pad.top + plotH - ((v - minV) / (maxV - minV)) * plotH; }
  // Fill gap colored by divergence direction
  for (let i = 0; i < n - 1; i++) {
    const x1 = xP(i), x2 = xP(i+1);
    const y1a = yP(vals[i]), y2a = yP(vals[i+1]);
    const y1p = yP(preds[i]), y2p = yP(preds[i+1]);
    const divergence = (vals[i] - preds[i]) / (maxV - minV);
    const color = divergence > 0.02 ? '#ef4444' : divergence < -0.02 ? '#22c55e' : '#eab308';
    ctx.fillStyle = color + '30';
    ctx.beginPath();
    ctx.moveTo(x1, y1a);
    ctx.lineTo(x2, y2a);
    ctx.lineTo(x2, y2p);
    ctx.lineTo(x1, y1p);
    ctx.closePath();
    ctx.fill();
    // Dots on prediction
    ctx.fillStyle = 'rgba(168,85,247,0.3)';
    ctx.beginPath();
    ctx.arc(x1, y1p, 1.5, 0, Math.PI*2);
    ctx.fill();
  }
  // Actual line
  ctx.beginPath();
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 1.5;
  for (let i = 0; i < n; i++) {
    const x = xP(i), y = yP(vals[i]);
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.stroke();
  // Prediction line
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(168,85,247,0.6)';
  ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  for (let i = 0; i < n; i++) {
    const x = xP(i), y = yP(preds[i]);
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.stroke();
  ctx.setLineDash([]);
}
// ───── MAIN LOOP ─────
function tick() {
  const now = performance.now();
  const dt = now - lastTime;
  lastTime = now;
  currentFps = dt > 0 ? Math.round(1000 / dt) : 60;
  frameCount++;
  // ── Generate new data point ──
  const t = data.timestamps.length;
  const metrics = generateMetricsTick(t);
  const anomaly = maybeInjectAnomaly(t, metrics);
  let value = metrics.cpu_pct;
  let prediction = value + (Math.random() - 0.5) * 3;
  if (anomaly && anomaly.values.cpu_pct !== undefined) {
    value = anomaly.values.cpu_pct;
    prediction = metrics.cpu_pct; // prediction lags
  }
  // Record all metrics for root-cause analysis
  for (const [k,v] of Object.entries(metrics)) {
    metricHistory[k].push(v);
    if (metricHistory[k].length > MAX_HISTORY) metricHistory[k].shift();
  }
  data.timestamps.push(t);
  data.values.push(value);
  data.predictions.push(prediction);
  // Trim
  if (data.values.length > MAX_HISTORY) {
    data.values.shift();
    data.timestamps.shift();
    data.predictions.shift();
  }
  // ── Throttled detection (every THROTTLE_DETECT frames) ──
  if (frameCount - lastDetectFrame >= THROTTLE_DETECT) {
    lastDetectFrame = frameCount;
    // Incremental: compute delta if we have old anomalies
    const newAnomalies = detectAnomalies(data.values, data.timestamps);
    const existingIdxs = new Set(data.anomalies.map(a => a.idx));
    const freshAnomalies = newAnomalies.filter(a => !existingIdxs.has(a.idx));
    if (freshAnomalies.length > 0) {
      data.anomalies = data.anomalies.concat(freshAnomalies);
      // Keep last 50
      if (data.anomalies.length > 50) data.anomalies.splice(0, data.anomalies.length - 50);
      // Spawn pulses for canvas
      const pulseCanvas = document.getElementById('pulse-canvas');
      const rect = pulseCanvas.getBoundingClientRect();
      const pad = {left:55, right:20, top:20, bottom:25};
      const plotW = rect.width - pad.left - pad.right;
      const plotH = rect.height - pad.top - pad.bottom;
      if (plotW > 0 && plotH > 0) {
        const wVals = data.values.slice(-WINDOW_SIZE);
        let mn = Infinity, mx = -Infinity;
        for (const v of wVals) { if (v<mn) mn=v; if (v>mx) mx=v; }
        const rg = mx-mn || 1;
        const pr = rg * 0.12;
        for (const a of freshAnomalies) {
          const relIdx = a.idx - Math.max(0, data.values.length - WINDOW_SIZE);
          if (relIdx < 0 || relIdx >= WINDOW_SIZE) continue;
          const cx = pad.left + (relIdx / (WINDOW_SIZE-1||1)) * plotW;
          const cy = pad.top + plotH - ((a.value - (mn-pr)) / ((mx+pr)-(mn-pr))) * plotH;
          spawnPulse(cx, cy, a.severity);
        }
      }
      // Update heatmap buffer
      const zScore = freshAnomalies.length > 0 ? freshAnomalies[0].zScore : 0;
      heatmapBuffer.copyWithin(0, 1);
      heatmapBuffer[HEATMAP_BUCKETS-1] = zScore;
      // Root cause
      const rc = computeRootCauses(metrics, freshAnomalies.length > 0 ? freshAnomalies[0].idx : -1);
      if (rc.length > 0) {
        rootCauses.unshift({time: t, causes: rc});
        if (rootCauses.length > 10) rootCauses.pop();
      }
      // Alert log
      for (const a of freshAnomalies) {
        alertLog.unshift({
          time: t,
          severity: a.severity,
          method: a.method,
          value: a.value.toFixed(1),
          score: a.zScore.toFixed(1)
        });
        if (alertLog.length > 50) alertLog.pop();
      }
    } else {
      // Still shift heatmap buffer for empty cells
      heatmapBuffer.copyWithin(0, 1);
      heatmapBuffer[HEATMAP_BUCKETS-1] = 0;
    }
  }
  // Update stats
  const wVals = data.windowValues();
  const stats = computeStats(wVals);
  if (stats) {
    data.mean = stats.mean;
    data.std = stats.std;
    data.q1 = stats.q1;
    data.q3 = stats.q3;
  }
  // ── Render ──
  const pulseCanvas = document.getElementById('pulse-canvas');
  const heatmapCanvas = document.getElementById('heatmap-canvas');
  const driftCanvas = document.getElementById('drift-canvas');
  const dpr = window.devicePixelRatio || 1;
  for (const [canvas, renderFn] of [
    [pulseCanvas, renderPulseCanvas],
    [heatmapCanvas, renderHeatmap],
    [driftCanvas, renderDrift]
  ]) {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ensureGradients(ctx, rect.width, rect.height);
    renderFn(ctx, rect.width, rect.height);
  }
  // Update pulses
  updatePulses(now);
  // ── Update DOM ──
  document.getElementById('alert-count').textContent = alertLog.length;
  document.getElementById('fps-display').textContent = currentFps;
  document.getElementById('latency-display').textContent = dt < 100 ? `${Math.round(dt)}ms` : `${(dt/1000).toFixed(1)}s`;
  const activeAnomalies = data.anomalies.filter(a => a.idx > data.values.length - 20).length;
  const badge = document.getElementById('status-badge');
  if (activeAnomalies > 3) { badge.textContent = 'critical'; badge.className = 'badge badge-crit'; }
  else if (activeAnomalies > 0) { badge.textContent = 'warning'; badge.className = 'badge badge-warn'; }
  else { badge.textContent = 'nominal'; badge.className = 'badge badge-ok'; }
  // Root cause list
  const rcEl = document.getElementById('root-cause-list');
  rcEl.innerHTML = '';
  if (rootCauses.length > 0) {
    for (const cause of rootCauses[0].causes.slice(0, 5)) {
      const li = document.createElement('li');
      const dir = cause.direction === 'up' ? '↑' : '↓';
      const val = cause.corr !== undefined ? cause.corr.toFixed(2) : (cause.shift*100).toFixed(1)+'%';
      li.innerHTML = `<span class="metric">${dir} ${cause.metric}</span><span class="corr">${val}</span>`;
      rcEl.appendChild(li);
    }
  } else {
    rcEl.innerHTML = '<li style="color:#64748b;font-style:italic;border-left-color:transparent">waiting for anomaly data...</li>';
    rcEl.querySelector('li').style.borderLeftColor = 'transparent';
  }
  // Alert log (show newest 8)
  const logEl = document.getElementById('alert-log');
  logEl.innerHTML = '';
  for (const a of alertLog.slice(0, 8)) {
    const div = document.createElement('div');
    div.className = `alert-entry sev-${a.severity}`;
    div.innerHTML = `<span class="time">t-${(t - a.time)}s</span> <span class="msg">${a.method} | value=${a.value} z=${a.score}</span>`;
    logEl.appendChild(div);
  }
  requestAnimationFrame(tick);
}
// ───── BOOT ─────
function boot() {
  // Set canvas sizes on resize
  function sizeCanvas(id) {
    const el = document.getElementById(id);
    el.style.width = '100%';
  }
  window.addEventListener('resize', () => {
    // Canvases auto-size via CSS + tick
  });
  requestAnimationFrame(tick);
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
})();
</script>
</body>
</html>