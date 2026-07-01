```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Visualizer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;padding:20px;overflow-x:hidden}
h2{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#48dbfb;margin-bottom:12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:1400px;margin:0 auto}
.card{background:#111827;border:1px solid #1e293b;border-radius:12px;padding:16px;position:relative}
.card-full{grid-column:1/-1}
canvas{display:block;width:100%;height:240px;border-radius:6px;background:#0d1117}
.controls{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.controls button{background:#1e293b;border:1px solid #334155;color:#c8d6e5;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .2s}
.controls button.active{background:#48dbfb;color:#0a0e17;border-color:#48dbfb;font-weight:600}
.controls button:hover{background:#334155}
.controls button.danger{background:#ef444422;border-color:#ef444444;color:#ef4444}
.controls button.danger:hover{background:#ef444444}
#heatmapCanvas{height:200px}
#pulseCanvas{height:260px}
#driftCanvas{height:200px}
#rootCause{font-size:13px;line-height:1.6;max-height:260px;overflow-y:auto}
#rootCause::-webkit-scrollbar{width:4px}
#rootCause::-webkit-scrollbar-track{background:#0d1117}
#rootCause::-webkit-scrollbar-thumb{background:#334155;border-radius:2px}
.cause-item{padding:8px 10px;margin-bottom:6px;border-radius:6px;border-left:3px solid;transition:all .3s}
.cause-item.critical{border-color:#ef4444;background:#ef444408}
.cause-item.warning{border-color:#f59e0b;background:#f59e0b08}
.cause-item.info{border-color:#48dbfb;background:#48dbfb08}
.cause-item .metric{font-weight:600;color:#e2e8f0}
.cause-item .arrow{color:#475569;margin:0 6px}
.cause-item .score{font-size:11px;opacity:.7;margin-left:8px}
.cause-item .desc{font-size:12px;color:#94a3b8;margin-top:2px}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600}
.badge.alert{background:#ef444422;color:#ef4444}
.badge.ok{background:#10b98122;color:#10b981}
.badge.warn{background:#f59e0b22;color:#f59e0b}
.stat-row{display:flex;gap:24px;margin-bottom:8px;flex-wrap:wrap}
.stat{font-size:12px}
.stat .label{color:#64748b}
.stat .value{color:#e2e8f0;font-weight:600;font-size:14px}
.stat .value.alert{color:#ef4444}
.stat .value.ok{color:#10b981}
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;animation:pulse-dot 2s infinite}
.status-dot.critical{background:#ef4444}
.status-dot.warning{background:#f59e0b}
.status-dot.ok{background:#10b981}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.4}}
.tooltip{position:absolute;display:none;background:#1e293b;border:1px solid #334155;border-radius:8px;padding:10px 14px;font-size:12px;z-index:100;pointer-events:none;max-width:260px;box-shadow:0 8px 24px rgba(0,0,0,.4)}
.tooltip.show{display:block}
.tooltip .tt-title{font-weight:600;color:#e2e8f0;margin-bottom:4px}
.tooltip .tt-row{color:#94a3b8;margin:2px 0}
.tooltip .tt-row .tt-val{color:#e2e8f0;font-weight:500}
#threshLegend{display:flex;gap:16px;font-size:11px;color:#94a3b8;margin-top:6px}
#threshLegend span{display:flex;align-items:center;gap:4px}
#threshLegend .swatch{width:20px;height:4px;border-radius:2px}
#threshLegend .swatch.band{background:rgba(72,219,251,.25)}
#threshLegend .swatch.outer{background:rgba(239,68,68,.3)}
#threshLegend .swatch.inner{background:rgba(16,185,129,.3)}
</style>
</head>
<body>
<div class="grid">
<div class="card card-full">
  <div class="controls">
    <button class="active" data-mode="stream">Live Stream</button>
    <button data-mode="batch">Batch Replay</button>
    <button class="danger" id="injectBtn">Inject Anomaly</button>
    <span style="flex:1"></span>
    <span style="font-size:12px;color:#64748b;display:flex;align-items:center;gap:6px">
      <span class="status-dot ok" id="statusDot"></span>
      <span id="statusText">Streaming</span>
      <span style="margin-left:12px;opacity:.7" id="fpsDisplay">30 fps</span>
    </span>
  </div>
  <div class="stat-row">
    <div class="stat"><span class="label">Anomalies </span><span class="value" id="anomalyCount">0</span></div>
    <div class="stat"><span class="label">Z-Score Threshold </span><span class="value" id="zThreshDisplay">2.5</span></div>
    <div class="stat"><span class="label">Window </span><span class="value" id="windowDisplay">60</span></div>
    <div class="stat"><span class="label">Series </span><span class="value" id="seriesCount">4</span></div>
  </div>
</div>
<div class="card card-full">
  <h2>Pulse — Anomaly Alert Rings <span class="badge alert">LIVE</span></h2>
  <canvas id="pulseCanvas"></canvas>
  <div id="threshLegend">
    <span><span class="swatch band"></span> Threshold Band (±z&sigma;)</span>
    <span><span class="swatch outer"></span> Outer Warning</span>
    <span><span class="swatch inner"></span> Inner Bound</span>
  </div>
</div>
<div class="card">
  <h2>Deviation Heatmap</h2>
  <canvas id="heatmapCanvas"></canvas>
  <div style="display:flex;justify-content:space-between;font-size:10px;color:#64748b;margin-top:4px">
    <span>← 5 min ago</span>
    <span>z-score</span>
    <span>now →</span>
  </div>
</div>
<div class="card">
  <h2>Drift — Prediction vs Actual</h2>
  <canvas id="driftCanvas"></canvas>
</div>
<div class="card card-full">
  <h2>Root-Cause Suggestions</h2>
  <div id="rootCause"></div>
</div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
// ── Configuration ──────────────────────────────────────────────
const CONFIG = {
  series: [
    {name:'CPU', base:55, amp:18, noise:4, color:'#48dbfb', zThreshold:2.5},
    {name:'Memory', base:68, amp:12, noise:3, color:'#f59e0b', zThreshold:2.5},
    {name:'Latency', base:120, amp:40, noise:15, color:'#ef4444', zThreshold:3.0},
    {name:'Throughput', base:850, amp:200, noise:60, color:'#10b981', zThreshold:2.5}
  ],
  windowSize: 60,
  lags: 5,
  updateIntervalMs: 80,
  changePointSensitivity: 0.65
};
// ── State ──────────────────────────────────────────────────────
const history = CONFIG.series.map(() => []);
const timestamps = [];
const anomalyLog = [];
let frame = 0;
let mode = 'stream';
let paused = false;
let rafId = null;
let lastTime = performance.now();
let fps = 30;
// ── Canvas Setup ──────────────────────────────────────────────
const pulseCanvas = document.getElementById('pulseCanvas');
const heatmapCanvas = document.getElementById('heatmapCanvas');
const driftCanvas = document.getElementById('driftCanvas');
const ctxPulse = pulseCanvas.getContext('2d');
const ctxHeat = heatmapCanvas.getContext('2d');
const ctxDrift = driftCanvas.getContext('2d');
const tooltip = document.getElementById('tooltip');
function resizeCanvases() {
  const rect = document.querySelector('.grid').getBoundingClientRect();
  const w = Math.min(rect.width - 40, 1360);
  [pulseCanvas, heatmapCanvas, driftCanvas].forEach(c => {
    c.width = (c.clientWidth || 800) * (window.devicePixelRatio||1);
    c.height = (c.clientHeight || 240) * (window.devicePixelRatio||1);
    c.style.width = (c.clientWidth || 800) + 'px';
    c.style.height = (c.clientHeight || 240) + 'px';
  });
}
resizeCanvases();
window.addEventListener('resize', resizeCanvases);
// ── Signal Generation ─────────────────────────────────────────
function generateSignal(seriesIdx, frame) {
  const s = CONFIG.series[seriesIdx];
  const t = frame * 0.05;
  let val = s.base
    + s.amp * Math.sin(t + seriesIdx)
    + s.amp * 0.3 * Math.sin(t * 3 + seriesIdx * 1.7)
    + (Math.random() - 0.5) * s.noise * 2;
  // Drift: slowly shift mean after frame 300
  if (frame > 300) val += (frame - 300) * 0.02 * (seriesIdx + 1);
  // Change-point: abrupt shift at frame 500
  if (frame >= 500 && frame < 530) val += 25 * (seriesIdx === 2 ? 2 : 1);
  return val;
}
// ── Z-Score Detection ─────────────────────────────────────────
function zScoreDetect(values, threshold) {
  if (values.length < 4) return {isAnomaly:false, z:0, mean:0, std:0};
  const n = values.length;
  const mean = values.reduce((a,b)=>a+b,0)/n;
  const variance = values.reduce((a,b)=>a+(b-mean)**2,0)/n;
  const std = Math.sqrt(variance) || 1;
  const last = values[n-1];
  const z = Math.abs(last - mean) / std;
  return {isAnomaly:z > threshold, z, mean, std, last};
}
// ── Moving IQR Detection ──────────────────────────────────────
function movingIQRScores(values, k=1.5) {
  if (values.length < 10) return [];
  const sorted = [...values].sort((a,b)=>a-b);
  const q1 = sorted[Math.floor(sorted.length*0.25)];
  const q3 = sorted[Math.floor(sorted.length*0.75)];
  const iqr = q3 - q1;
  const last = values[values.length-1];
  const score = (last - q3) / (iqr||1);
  const isOutlier = last < q1 - k*iqr || last > q3 + k*iqr;
  return {isOutlier, score, q1, q3, iqr, last};
}
// ── Change-Point Detection (CUSUM-style) ───────────────────────
function changePointDetect(values, sensitivity=0.65) {
  if (values.length < 15) return {isChange:false, score:0};
  const window = 10;
  const recent = values.slice(-window);
  const prior = values.slice(-window*2, -window);
  if (prior.length < window) return {isChange:false, score:0};
  const meanRecent = recent.reduce((a,b)=>a+b,0)/window;
  const meanPrior = prior.reduce((a,b)=>a+b,0)/window;
  const diff = Math.abs(meanRecent - meanPrior);
  const pooledStd = Math.sqrt(
    (recent.reduce((a,b)=>a+(b-meanRecent)**2,0) + prior.reduce((a,b)=>a+(b-meanPrior)**2,0)) / (window*2-2)
  ) || 1;
  const score = diff / pooledStd;
  return {isChange:score > sensitivity * 3, score, meanRecent, meanPrior};
}
// ── Pulse Animation ───────────────────────────────────────────
let pulses = [];
function spawnPulse(x, y, severity, color, metricName) {
  pulses.push({
    x, y, radius: 0, maxRadius: 40 + severity * 20,
    opacity: 1, severity, color, metricName,
    birth: performance.now(),
    lifetime: 2000 + severity * 500
  });
}
function updatePulses(now) {
  pulses = pulses.filter(p => {
    const age = now - p.birth;
    const progress = age / p.lifetime;
    if (progress >= 1) return false;
    p.radius = p.maxRadius * Math.pow(progress, 0.6);
    p.opacity = 1 - progress;
    return true;
  });
}
// ── Heatmap ────────────────────────────────────────────────────
function buildHeatmapData() {
  const nSeries = CONFIG.series.length;
  const nTime = Math.min(timestamps.length, CONFIG.windowSize);
  if (nTime < 2) return null;
  const data = [];
  for (let s = 0; s < nSeries; s++) {
    const row = [];
    const vals = history[s].slice(-nTime);
    const mean = vals.reduce((a,b)=>a+b,0)/vals.length;
    const std = Math.sqrt(vals.reduce((a,b)=>a+(b-mean)**2,0)/vals.length) || 1;
    for (let t = 0; t < vals.length; t++) {
      const z = (vals[t] - mean) / std;
      row.push(z);
    }
    data.push({series: CONFIG.series[s].name, color: CONFIG.series[s].color, values: row});
  }
  return data;
}
// ── Root-Cause Correlation ─────────────────────────────────────
function computeRootCause(anomalousSeriesIdx, timestamp) {
  const results = [];
  const window = 10;
  for (let s = 0; s < CONFIG.series.length; s++) {
    if (s === anomalousSeriesIdx) continue;
    const vals = history[s];
    const anomVals = history[anomalousSeriesIdx];
    if (vals.length < window + CONFIG.lags || anomVals.length < window + CONFIG.lags) continue;
    const recent = vals.slice(-window);
    const recentAnom = anomVals.slice(-window);
    const meanR = recent.reduce((a,b)=>a+b,0)/window;
    const meanA = recentAnom.reduce((a,b)=>a+b,0)/window;
    let crossCorr = 0;
    for (let lag = 1; lag <= CONFIG.lags; lag++) {
      const lagged = vals.slice(-window-lag, -lag);
      if (lagged.length < window-1) continue;
      const meanL = lagged.reduce((a,b)=>a+b,0)/lagged.length;
      let num = 0, denR = 0, denL = 0;
      for (let i = 0; i < window-1 && i < lagged.length; i++) {
        num += (recentAnom[i] - meanA) * (lagged[i] - meanL);
        denR += (recentAnom[i] - meanA)**2;
        denL += (lagged[i] - meanL)**2;
      }
      const c = denR && denL ? num / Math.sqrt(denR*denL) : 0;
      if (Math.abs(c) > Math.abs(crossCorr)) crossCorr = c;
    }
    // Check if this metric spiked before the anomaly
    const preAnom = vals.slice(-window-CONFIG.lags, -CONFIG.lags);
    const preMean = preAnom.reduce((a,b)=>a+b,0)/preAnom.length;
    const preStd = Math.sqrt(preAnom.reduce((a,b)=>a+(b-preMean)**2,0)/preAnom.length)||1;
    const lastVal = vals[vals.length-1];
    const zScore = Math.abs(lastVal - preMean) / preStd;
    const direction = lastVal > preMean ? 'increase' : 'decrease';
    const severity = zScore > 3 ? 'critical' : zScore > 2 ? 'warning' : 'info';
    let score = (Math.abs(crossCorr) * 0.6 + (zScore / 5) * 0.4) * 100;
    score = Math.min(100, Math.round(score));
    if (zScore > 1.8) {
      results.push({
        metric: CONFIG.series[s].name,
        score,
        correlation: crossCorr.toFixed(2),
        zScore: zScore.toFixed(1),
        direction,
        severity,
        lag: '1-5 steps',
        desc: `${direction} by ${Math.abs(lastVal - preMean).toFixed(0)} units (z=${zScore.toFixed(1)})`
      });
    }
  }
  return results.sort((a,b)=>b.score-a.score);
}
// ── Drawing ────────────────────────────────────────────────────
let tooltipTarget = null;
let mouseX = 0, mouseY = 0;
function drawPulse(now) {
  const c = ctxPulse;
  const W = pulseCanvas.width, H = pulseCanvas.height;
  const dpr = window.devicePixelRatio || 1;
  c.clearRect(0, 0, W, H);
  const n = CONFIG.series.length;
  const padTop = 30 * dpr;
  const padBot = 30 * dpr;
  const plotH = H - padTop - padBot;
  const visible = Math.min(CONFIG.windowSize, timestamps.length);
  if (visible < 2) { c.fillStyle='#475569'; c.font=`${14*dpr}px sans-serif`; c.textAlign='center'; c.fillText('Waiting for data...', W/2, H/2); return; }
  const leftPad = 60 * dpr;
  const rightPad = 20 * dpr;
  const plotW = W - leftPad - rightPad;
  const stepX = plotW / (visible - 1);
  // Y ranges per series
  const yRanges = CONFIG.series.map((s, idx) => {
    const vals = history[idx].slice(-visible);
    if (vals.length < 2) return {min:s.base - s.amp*2, max:s.base + s.amp*2};
    const mean = vals.reduce((a,b)=>a+b,0)/vals.length;
    const std = Math.sqrt(vals.reduce((a,b)=>a+(b-mean)**2,0)/vals.length)||1;
    const margin = Math.max(std * 3.5, s.amp * 1.2);
    return {min: mean - margin, max: mean + margin};
  });
  // Draw grid
  c.strokeStyle = '#1e293b';
  c.lineWidth = 1 * dpr;
  for (let g = 0; g <= 4; g++) {
    const y = padTop + plotH * g / 4;
    c.beginPath(); c.moveTo(leftPad, y); c.lineTo(W-rightPad, y); c.stroke();
  }
  // Draw each series
  for (let s = 0; s < n; s++) {
    const vals = history[s].slice(-visible);
    const {min:yMin, max:yMax} = yRanges[s];
    const yScale = plotH / (yMax - yMin);
    const seriesColor = CONFIG.series[s].color;
    // Threshold band
    const thresh = CONFIG.series[s].zThreshold;
    const yMid = (yMin + yMax) / 2;
    const yBand = thresh * (yMax - yMin) / 2 / 3.5;
    c.fillStyle = 'rgba(72,219,251,0.06)';
    c.fillRect(leftPad, padTop + plotH/2 - yBand * yScale, plotW, yBand * 2 * yScale);
    // Outer warning band
    c.fillStyle = 'rgba(239,68,68,0.04)';
    c.fillRect(leftPad, padTop, plotW, padTop + plotH/2 - yBand * yScale);
    c.fillRect(leftPad, padTop + plotH/2 + yBand * yScale, plotW, padTop + plotH - (padTop + plotH/2 + yBand * yScale));
    // Line
    c.beginPath();
    c.strokeStyle = seriesColor;
    c.lineWidth = 1.5 * dpr;
    c.globalAlpha = 0.6;
    for (let i = 0; i < vals.length; i++) {
      const x = leftPad + i * stepX;
      const yVal = padTop + plotH - (vals[i] - yMin) * yScale;
      i === 0 ? c.moveTo(x, yVal) : c.lineTo(x, yVal);
    }
    c.stroke();
    c.globalAlpha = 1;
    // Points + anomalies
    const lastIdx = vals.length - 1;
    const zResult = zScoreDetect(vals, CONFIG.series[s].zThreshold);
    const iqrResult = movingIQRScores(vals);
    const cpResult = changePointDetect(vals, CONFIG.changePointSensitivity);
    for (let i = 0; i < vals.length; i++) {
      const x = leftPad + i * stepX;
      const yVal = padTop + plotH - (vals[i] - yMin) * yScale;
      const subVals = vals.slice(0, i+1);
      const subZ = zScoreDetect(subVals, CONFIG.series[s].zThreshold);
      const subIqr = movingIQRScores(subVals);
      const isAnom = subZ.isAnomaly || (subIqr && subIqr.isOutlier);
      if (isAnom) {
        const severity = Math.min(subZ.z / CONFIG.series[s].zThreshold, 3);
        const r = (4 + severity * 3) * dpr;
        c.beginPath();
        c.arc(x, yVal, r, 0, Math.PI*2);
        c.fillStyle = seriesColor;
        c.globalAlpha = 0.3 + severity * 0.2;
        c.fill();
        c.globalAlpha = 1;
        c.strokeStyle = '#ef4444';
        c.lineWidth = 2 * dpr;
        c.stroke();
        // Spawn pulse ring
        if (i === lastIdx && Math.random() < 0.1) {
          spawnPulse(x, yVal, severity, seriesColor, CONFIG.series[s].name);
        }
      }
    }
    // Draw change-point marker
    if (cpResult.isChange) {
      const x = leftPad + (vals.length-1) * stepX;
      const yVal = padTop + plotH - (vals[vals.length-1] - yMin) * yScale;
      c.strokeStyle = '#f59e0b';
      c.lineWidth = 2 * dpr;
      c.setLineDash([4*dpr, 4*dpr]);
      c.beginPath(); c.moveTo(x, padTop); c.lineTo(x, padTop+plotH); c.stroke();
      c.setLineDash([]);
    }
    // Label
    c.fillStyle = seriesColor;
    c.font = `bold ${11*dpr}px sans-serif`;
    c.textAlign = 'left';
    c.textBaseline = 'top';
    const labelX = leftPad + 8*dpr;
    const labelY = padTop + s * 16 * dpr;
    c.fillText(CONFIG.series[s].name, labelX, labelY);
    c.fillStyle = '#475569';
    c.font = `${9*dpr}px sans-serif`;
    c.fillText(`z=${zResult.z.toFixed(1)}`, labelX + c.measureText(CONFIG.series[s].name).width + 8*dpr, labelY);
    // Last value
    c.fillStyle = seriesColor;
    c.font = `bold ${12*dpr}px sans-serif`;
    c.textAlign = 'right';
    c.textBaseline = 'bottom';
    const lastY = padTop + plotH - (vals[vals.length-1] - yMin) * yScale;
    c.fillText(vals[vals.length-1].toFixed(1), leftPad - 4*dpr, lastY);
  }
  // Draw pulse rings
  for (const p of pulses) {
    const r = p.radius * dpr;
    c.beginPath();
    c.arc(p.x, p.y, r, 0, Math.PI*2);
    c.strokeStyle = p.color;
    c.globalAlpha = p.opacity * 0.6;
    c.lineWidth = (2 + p.severity * 1.5) * dpr;
    c.stroke();
    c.globalAlpha = p.opacity * 0.15;
    c.fillStyle = p.color;
    c.fill();
    c.globalAlpha = 1;
  }
  // X axis labels
  c.fillStyle = '#475569';
  c.font = `${9*dpr}px sans-serif`;
  c.textAlign = 'center';
  c.textBaseline = 'top';
  const firstTs = timestamps[Math.max(0, timestamps.length-visible)];
  c.fillText(new Date(firstTs).toLocaleTimeString(), leftPad, padTop+plotH+4*dpr);
  c.fillText(new Date(timestamps[timestamps.length-1]).toLocaleTimeString(), W-rightPad, padTop+plotH+4*dpr);
  c.fillText(`-${visible} points`, leftPad + plotW/2, padTop+plotH+4*dpr);
}
function drawHeatmap() {
  const c = ctxHeat;
  const W = heatmapCanvas.width, H = heatmapCanvas.height;
  const dpr = window.devicePixelRatio || 1;
  c.clearRect(0, 0, W, H);
  const data = buildHeatmapData();
  if (!data) {
    c.fillStyle='#475569'; c.font=`${14*dpr}px sans-serif`; c.textAlign='center'; c.fillText('Waiting for data...', W/2, H/2);
    return;
  }
  const nSeries = data.length;
  const nTimes = data[0].values.length;
  const cellH = (H - 40*dpr) / nSeries;
  const cellW = (W - 60*dpr) / nTimes;
  const leftPad = 60*dpr;
  const topPad = 8*dpr;
  for (let s = 0; s < nSeries; s++) {
    for (let t = 0; t < nTimes; t++) {
      const z = data[s].values[t];
      const clamped = Math.max(-3.5, Math.min(3.5, z));
      const norm = (clamped + 3.5) / 7; // 0..1
      const r = Math.round(255 * Math.max(0, (norm-0.5)*2));
      const g = Math.round(255 * (1 - Math.abs(norm-0.5)*2));
      const b = Math.round(255 * Math.max(0, (0.5-norm)*2));
      c.fillStyle = `rgb(${r},${g},${b})`;
      const x = leftPad + t * cellW;
      const y = topPad + s * cellH;
      c.fillRect(Math.round(x), Math.round(y), Math.ceil(cellW-0.5), Math.ceil(cellH-2));
      // Border
      c.strokeStyle = '#0a0e17';
      c.lineWidth = 0.5 * dpr;
      c.strokeRect(Math.round(x), Math.round(y), Math.ceil(cellW-0.5), Math.ceil(cellH-2));
    }
  }
  // Labels
  c.font = `bold ${10*dpr}px sans-serif`;
  c.textAlign = 'right';
  c.textBaseline = 'middle';
  for (let s = 0; s < nSeries; s++) {
    c.fillStyle = data[s].color || '#c8d6e5';
    c.fillText(data[s].series, leftPad - 6*dpr, topPad + s*cellH + cellH/2);
  }
  // Color bar
  const barX = W - 16*dpr;
  const barY = topPad;
  const barH = H - 40*dpr;
  for (let i = 0; i < barH; i++) {
    const norm = i / barH;
    const clamped = norm * 7 - 3.5;
    const n = (clamped + 3.5) / 7;
    const r = Math.round(255 * Math.max(0, (n-0.5)*2));
    const g = Math.round(255 * (1 - Math.abs(n-0.5)*2));
    const b = Math.round(255 * Math.max(0, (0.5-n)*2));
    c.fillStyle = `rgb(${r},${g},${b})`;
    c.fillRect(barX, barY + i, 8*dpr, 1);
  }
  c.fillStyle = '#64748b';
  c.font = `${8*dpr}px sans-serif`;
  c.textAlign = 'left';
  c.fillText('+3.5σ', barX+10*dpr, barY+8*dpr);
  c.fillText('0', barX+10*dpr, barY+barH/2+3*dpr);
  c.fillText('-3.5σ', barX+10*dpr, barY+barH);
}
function drawDrift() {
  const c = ctxDrift;
  const W = driftCanvas.width, H = driftCanvas.height;
  const dpr = window.devicePixelRatio || 1;
  c.clearRect(0, 0, W, H);
  const visible = Math.min(CONFIG.windowSize, timestamps.length);
  if (visible < 2) {
    c.fillStyle='#475569'; c.font=`${14*dpr}px sans-serif`; c.textAlign='center'; c.fillText('Waiting for data...', W/2, H/2);
    return;
  }
  // Use latency (idx 2) as "prediction vs actual" demo
  // Simulate: prediction = smoothed version of actual
  const rawVals = history[2].slice(-visible);
  const predVals = rawVals.map((v,i) => {
    if (i < 3) return v;
    return (rawVals[i-1]*0.3 + rawVals[i-2]*0.2 + rawVals[i-3]*0.1 + rawVals[i]*0.4);
  });
  const yMin = Math.min(...rawVals, ...predVals);
  const yMax = Math.max(...rawVals, ...predVals);
  const pad = 20*dpr;
  const plotH = H - pad*2;
  const plotW = W - pad*2;
  const stepX = plotW / (visible-1);
  const yScale = plotH / (yMax - yMin || 1);
  // Fill drift gap
  for (let i = 0; i < rawVals.length-1; i++) {
    const x1 = pad + i * stepX;
    const x2 = pad + (i+1) * stepX;
    const yRaw1 = pad + plotH - (rawVals[i] - yMin) * yScale;
    const yRaw2 = pad + plotH - (rawVals[i+1] - yMin) * yScale;
    const yPred1 = pad + plotH - (predVals[i] - yMin) * yScale;
    const yPred2 = pad + plotH - (predVals[i+1] - yMin) * yScale;
    const drift1 = rawVals[i] - predVals[i];
    const drift2 = rawVals[i+1] - predVals[i+1];
    const isDiverging = Math.abs(drift1) > 5 || Math.abs(drift2) > 5;
    c.beginPath();
    c.moveTo(x1, yRaw1);
    c.lineTo(x1, yPred1);
    c.lineTo(x2, yPred2);
    c.lineTo(x2, yRaw2);
    c.closePath();
    c.fillStyle = isDiverging ? 'rgba(239,68,68,0.15)' : 'rgba(16,185,129,0.12)';
    c.fill();
  }
  // Prediction line
  c.beginPath();
  c.strokeStyle = '#f59e0b';
  c.lineWidth = 2*dpr;
  c.setLineDash([4*dpr, 4*dpr]);
  for (let i = 0; i < predVals.length; i++) {
    const x = pad + i * stepX;
    const y = pad + plotH - (predVals[i] - yMin) * yScale;
    i === 0 ? c.moveTo(x, y) : c.lineTo(x, y);
  }
  c.stroke();
  c.setLineDash([]);
  // Actual line
  c.beginPath();
  c.strokeStyle = '#48dbfb';
  c.lineWidth = 1.5*dpr;
  for (let i = 0; i < rawVals.length; i++) {
    const x = pad + i * stepX;
    const y = pad + plotH - (rawVals[i] - yMin) * yScale;
    i === 0 ? c.moveTo(x, y) : c.lineTo(x, y);
  }
  c.stroke();
  // Legend
  c.font = `${10*dpr}px sans-serif`;
  c.textAlign = 'left';
  c.textBaseline = 'top';
  c.fillStyle = '#48dbfb';
  c.fillRect(8*dpr, 4*dpr, 12*dpr, 3*dpr);
  c.fillText('Actual (Latency)', 24*dpr, 2*dpr);
  c.fillStyle = '#f59e0b';
  c.fillRect(8*dpr, 18*dpr, 12*dpr, 3*dpr);
  c.fillText('Prediction', 24*dpr, 16*dpr);
  c.fillStyle = 'rgba(16,185,129,0.3)';
  c.fillRect(8*dpr, 32*dpr, 12*dpr, 6*dpr);
  c.fillText('On Track', 24*dpr, 30*dpr);
  c.fillStyle = 'rgba(239,68,68,0.15)';
  c.fillRect(80*dpr, 32*dpr, 12*dpr, 6*dpr);
  c.fillText('Diverging', 96*dpr, 30*dpr);
  // Labels
  c.fillStyle = '#475569';
  c.font = `${9*dpr}px sans-serif`;
  c.textAlign = 'center';
  c.fillText(new Date(timestamps[Math.max(0,timestamps.length-visible)]).toLocaleTimeString(), pad, H-4*dpr);
  c.fillText(new Date(timestamps[timestamps.length-1]).toLocaleTimeString(), W-pad, H-4*dpr);
}
function updateStats() {
  let totalAnomalies = 0;
  for (let s = 0; s < CONFIG.series.length; s++) {
    const vals = history[s];
    const zr = zScoreDetect(vals, CONFIG.series[s].zThreshold);
    if (zr.isAnomaly) totalAnomalies++;
    const iqr = movingIQRScores(vals);
    if (iqr && iqr.isOutlier) totalAnomalies++;
  }
  document.getElementById('anomalyCount').textContent = totalAnomalies;
  document.getElementById('anomalyCount').className = 'value' + (totalAnomalies > 0 ? ' alert' : ' ok');
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('statusText');
  if (totalAnomalies > 2) {
    statusDot.className = 'status-dot critical';
    statusText.textContent = 'Critical';
  } else if (totalAnomalies > 0) {
    statusDot.className = 'status-dot warning';
    statusText.textContent = 'Warning';
  } else {
    statusDot.className = 'status-dot ok';
    statusText.textContent = 'Streaming';
  }
}
function updateRootCause() {
  const container = document.getElementById('rootCause');
  const now = Date.now();
  // Find most recent anomaly
  let latestAnomSeries = -1;
  let latestZ = 0;
  for (let s = 0; s < CONFIG.series.length; s++) {
    const vals = history[s];
    const zr = zScoreDetect(vals, CONFIG.series[s].zThreshold);
    if (zr.isAnomaly && zr.z > latestZ) {
      latestZ = zr.z;
      latestAnomSeries = s;
    }
  }
  if (latestAnomSeries < 0) {
    container.innerHTML = '<div style="text-align:center;padding:30px;color:#475569"><span style="font-size:28px">✓</span><br>No anomalies detected. System nominal.</div>';
    return;
  }
  const causes = computeRootCause(latestAnomSeries, now);
  if (causes.length === 0) {
    container.innerHTML = `<div style="padding:12px;border-left:3px solid #f59e0b;background:#f59e0b08">
      <span class="metric">${CONFIG.series[latestAnomSeries].name}</span> anomaly detected.
      <span class="desc">No correlated metrics found. Consider adding more metric sources.</span>
    </div>`;
    return;
  }
  let html = `<div style="margin-bottom:8px;font-size:12px;color:#64748b">
    Anomaly in <span style="color:${CONFIG.series[latestAnomSeries].color};font-weight:600">${CONFIG.series[latestAnomSeries].name}</span>
    — likely root causes:
  </div>`;
  for (const c of causes) {
    html += `<div class="cause-item ${c.severity}">
      <span class="metric">${c.metric}</span>
      <span class="arrow">→</span>
      <span style="color:#94a3b8">${c.direction}</span>
      <span class="score">${c.score}% match</span>
      <div class="desc">
        ${c.desc} &middot; corr=${c.correlation} &middot; lag=${c.lag}
      </div>
    </div>`;
  }
  container.innerHTML = html;
}
// ── Main Loop ──────────────────────────────────────────────────
function step(timestamp) {
  if (paused) return;
  const now = performance.now();
  const dt = now - lastTime;
  fps = 0.9 * fps + 0.1 * (1000 / dt);
  lastTime = now;
  document.getElementById('fpsDisplay').textContent = Math.round(fps) + ' fps';
  // Tick
  frame++;
  // Generate data
  for (let s = 0; s < CONFIG.series.length; s++) {
    const val = generateSignal(s, frame);
    history[s].push(val);
    if (history[s].length > CONFIG.windowSize * 3) {
      history[s].splice(0, history[s].length - CONFIG.windowSize * 2);
    }
  }
  timestamps.push(Date.now());
  if (timestamps.length > CONFIG.windowSize * 3) {
    timestamps.splice(0, timestamps.length - CONFIG.windowSize * 2);
  }
  updatePulses(now);
  // Draw
  drawPulse(now);
  drawHeatmap();
  drawDrift();
  updateStats();
  // Root cause every 10 frames
  if (frame % 10 === 0) updateRootCause();
  rafId = requestAnimationFrame(step);
}
// ── Inject Anomaly ─────────────────────────────────────────────
document.getElementById('injectBtn').addEventListener('click', () => {
  const s = Math.floor(Math.random() * CONFIG.series.length);
  const spike = 40 + Math.random() * 60;
  const idx = history[s].length - 1;
  if (idx >= 0) history[s][idx] += spike;
  // Add a few more spikes
  for (let i = 0; i < 3; i++) {
    history[s].push(generateSignal(s, frame + i) + spike * (0.5 + Math.random()));
    timestamps.push(Date.now());
    frame++;
  }
  // Spawn visual pulse on the anomaly
  const val = history[s][history[s].length-1];
  // Find x,y on canvas
  const visible = Math.min(CONFIG.windowSize, timestamps.length);
  const leftPad = 60 * (window.devicePixelRatio||1);
  const stepX = (pulseCanvas.width - leftPad - 20*(window.devicePixelRatio||1)) / (visible-1);
  const x = leftPad + (visible-1) * stepX;
  spawnPulse(x, pulseCanvas.height/2, 3, CONFIG.series[s].color, CONFIG.series[s].name);
  spawnPulse(x - stepX * 2, pulseCanvas.height/2 - 20*(window.devicePixelRatio||1), 2, CONFIG.series[s].color, CONFIG.series[s].name);
  spawnPulse(x - stepX * 4, pulseCanvas.height/2 + 30*(window.devicePixelRatio||1), 2.5, CONFIG.series[s].color, CONFIG.series[s].name);
});
// ── Mode Toggle ────────────────────────────────────────────────
document.querySelectorAll('[data-mode]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-mode]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    mode = btn.dataset.mode;
    document.getElementById('statusText').textContent = mode === 'stream' ? 'Streaming' : 'Batch Replay';
  });
});
// ── Mouse tracking for tooltip (placeholder—extend to real hit-test) ──
document.querySelector('.grid').addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});
// ── Start ──────────────────────────────────────────────────────
rafId = requestAnimationFrame(step);
// Cleanup on page unload (for memory)
window.addEventListener('beforeunload', () => {
  if (rafId) cancelAnimationFrame(rafId);
});
</script>
</body>
</html>
```