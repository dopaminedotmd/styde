```yaml
task: anomaly-detection-visualizer
status: building
features:
  - z-score moving IQR change-point detection
  - glowing pulse ring animation on anomaly points
  - time-slice deviation heatmap with severity coloring
  - model drift visualization with gap filling
  - dynamic threshold bands
  - root-cause correlated metric chains
  - live-updating interactive HTML panel
```
I notice the CAVEMAN format conflicts with the requirement to deliver a working HTML file. The HTML itself requires `<html><style><script>` tags. I will output the raw HTML code directly as the result content — that is the deliverable, not markdown.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Anomaly Detection Visualizer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;padding:20px}
h1{font-size:18px;font-weight:300;letter-spacing:2px;text-transform:uppercase;color:#48dbfb;margin-bottom:16px}
h1 span{color:#ff6b6b;font-weight:600}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:16px}
.panel{background:rgba(255,255,255,0.03);border:1px solid rgba(72,219,251,0.12);border-radius:12px;padding:16px;position:relative}
.panel-title{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#48dbfb;opacity:.6;margin-bottom:12px}
canvas{display:block;width:100%;height:auto;border-radius:6px}
#mainChart{max-height:280px;width:100%}
#heatmapCanvas{max-height:180px;width:100%}
.metrics-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.metric-card{background:rgba(255,255,255,0.04);border-radius:8px;padding:12px 16px;min-width:120px;flex:1}
.metric-card .label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:rgba(200,214,229,.5)}
.metric-card .value{font-size:22px;font-weight:300;margin-top:4px}
.metric-card .value.alert{color:#ff6b6b}
.metric-card .value.ok{color:#1dd1a1}
.metric-card .value.warn{color:#feca57}
.root-cause-list{list-style:none;margin-top:8px}
.root-cause-list li{padding:6px 10px;margin-bottom:4px;background:rgba(255,255,255,0.04);border-radius:6px;font-size:12px;border-left:3px solid transparent;display:flex;align-items:center;gap:8px}
.root-cause-list li.critical{border-left-color:#ff6b6b}
.root-cause-list li.warning{border-left-color:#feca57}
.root-cause-list li .arrow{color:#48dbfb;font-size:14px}
.root-cause-list li .metric-name{font-weight:600;color:#dfe6e9}
.root-cause-list li .metric-desc{color:rgba(200,214,229,.6);font-size:11px}
.root-cause-list li .z-badge{background:#ff6b6b20;color:#ff6b6b;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600}
.status-bar{display:flex;gap:20px;align-items:center;padding:10px 0 4px;font-size:11px;color:rgba(200,214,229,.5)}
.status-bar .dot{width:6px;height:6px;border-radius:50%;display:inline-block;margin-right:6px}
.status-bar .dot.green{background:#1dd1a1;box-shadow:0 0 6px #1dd1a1}
.status-bar .dot.red{background:#ff6b6b;box-shadow:0 0 6px #ff6b6b}
.threshold-legend{display:flex;gap:16px;font-size:10px;margin-top:6px}
.threshold-legend span{display:flex;align-items:center;gap:4px}
.threshold-legend .swatch{width:12px;height:3px;border-radius:2px}
.threshold-legend .swatch.upper{background:#ff6b6b}
.threshold-legend .swatch.lower{background:#48dbfb}
.threshold-legend .swatch.mean{background:#feca57}
</style>
</head>
<body>
<h1>Anomaly <span>Pulse</span> Monitor</h1>
<div class="metrics-row" id="metricCards">
  <div class="metric-card"><div class="label">Active Metrics</div><div class="value ok" id="metricCount">0</div></div>
  <div class="metric-card"><div class="label">Anomalies (30s)</div><div class="value" id="anomalyCount">0</div></div>
  <div class="metric-card"><div class="label">Current Z-Score</div><div class="value" id="currentZ">0.00</div></div>
  <div class="metric-card"><div class="label">Drift Gap</div><div class="value ok" id="driftGap">0.0%</div></div>
  <div class="metric-card"><div class="label">Alert Level</div><div class="value ok" id="alertLevel">STABLE</div></div>
</div>
<div class="grid">
  <div class="panel">
    <div class="panel-title">Metric Stream &bull; Drift &bull; Pulse Zones</div>
    <canvas id="mainChart"></canvas>
    <div class="threshold-legend">
      <span><div class="swatch upper"></div> Upper Threshold (dynamic)</span>
      <span><div class="swatch lower"></div> Lower Threshold (dynamic)</span>
      <span><div class="swatch mean"></div> Rolling Mean</span>
    </div>
  </div>
  <div class="panel">
    <div class="panel-title">Deviation Heatmap (last 60s)</div>
    <canvas id="heatmapCanvas"></canvas>
  </div>
</div>
<div class="grid" style="grid-template-columns:1fr 1fr">
  <div class="panel">
    <div class="panel-title">Root-Cause Chain &bull; Correlated Predecessors</div>
    <ul class="root-cause-list" id="rootCauseList">
      <li style="color:rgba(200,214,229,.4);font-style:italic">Awaiting anomaly events...</li>
    </ul>
  </div>
  <div class="panel">
    <div class="panel-title">Change-Point Detection &bull; CUSUM</div>
    <canvas id="cusumCanvas"></canvas>
    <div class="status-bar" id="statusBar">
      <span><span class="dot green"></span>Monitoring</span>
      <span id="lastUpdateTime">--</span>
    </div>
  </div>
</div>
<script>
// ============================================================
// Anomaly Detection Engine
// ============================================================
const WINDOW = 60;
const MAX_HISTORY = 120;
const METRICS = 4;
const METRIC_NAMES = ['latency_ms', 'error_rate', 'throughput', 'cpu_pct'];
const METRIC_BASELINES = [42, 2.3, 850, 55];
const METRIC_VARIANCES = [8, 0.8, 120, 10];
class AnomalyDetector {
  constructor() {
    this.history = {};
    this.predictions = {};
    this.anomalies = [];
    this.anomalyTimestamps = [];
    this.time = 0;
    METRIC_NAMES.forEach(m => {
      this.history[m] = [];
      this.predictions[m] = [];
    });
    this._initMetrics();
  }
  _initMetrics() {
    for (let t = 0; t < WINDOW; t++) {
      METRIC_NAMES.forEach((m, i) => {
        const val = METRIC_BASELINES[i] + (Math.random() - 0.5) * METRIC_VARIANCES[i] * 2;
        this.history[m].push(val);
        this.predictions[m].push(METRIC_BASELINES[i] + Math.sin(t * 0.1) * 3);
      });
    }
  }
  step() {
    this.time++;
    const results = {};
    const isAnomalyStep = Math.random() < 0.04;
    METRIC_NAMES.forEach((m, i) => {
      let val = METRIC_BASELINES[i] + (Math.random() - 0.5) * METRIC_VARIANCES[i] * 2;
      if (isAnomalyStep && i === 0) {
        val += (Math.random() * 40 + 20);
      }
      if (isAnomalyStep && i === 1 && Math.random() < 0.5) {
        val += (Math.random() * 3 + 1.5);
      }
      if (this.time % 30 === 0 && i === 2 && Math.random() < 0.3) {
        val -= Math.random() * 200 + 100;
      }
      if (this.time % 45 === 0 && i === 3) {
        val += (Math.random() - 0.5) * 30;
      }
      this.history[m].push(val);
      if (this.history[m].length > MAX_HISTORY) this.history[m].shift();
      this.predictions[m].push(METRIC_BASELINES[i] + Math.sin(this.time * 0.08) * 4 + (Math.random() - 0.5) * 5);
      if (this.predictions[m].length > MAX_HISTORY) this.predictions[m].shift();
      results[m] = val;
    });
    const detections = this.detectAll(results);
    if (detections.length > 0) {
      this.anomalies.push({ time: this.time, detections });
      this.anomalyTimestamps.push(this.time);
      if (this.anomalies.length > 20) this.anomalies.shift();
      if (this.anomalyTimestamps.length > 30) this.anomalyTimestamps.shift();
    }
    return { results, detections };
  }
  detectAll(currentVals) {
    const detections = [];
    METRIC_NAMES.forEach((m, i) => {
      const vals = this.history[m];
      if (vals.length < 10) return;
      const v = currentVals[m];
      // Z-score
      const mean = vals.reduce((a,b) => a+b, 0) / vals.length;
      const std = Math.sqrt(vals.reduce((a,b) => a + (b-mean)**2, 0) / vals.length);
      const z = std > 0.001 ? (v - mean) / std : 0;
      const zAnomaly = Math.abs(z) > 2.5;
      // Moving IQR
      const sorted = [...vals].sort((a,b)=>a-b);
      const q1 = sorted[Math.floor(sorted.length * 0.25)];
      const q3 = sorted[Math.floor(sorted.length * 0.75)];
      const iqr = q3 - q1;
      const iqrLower = q1 - 1.5 * iqr;
      const iqrUpper = q3 + 1.5 * iqr;
      const iqrAnomaly = v < iqrLower || v > iqrUpper;
      // Change point via CUSUM-like
      const cusum = Math.abs(v - mean) > 2.5 * (std || 1);
      if (zAnomaly || iqrAnomaly || cusum) {
        detections.push({
          metric: m,
          value: v,
          baseline: mean,
          zScore: z,
          iqrRange: [iqrLower, iqrUpper],
          isIQR: iqrAnomaly,
          isZ: zAnomaly,
          isCP: cusum,
          severity: Math.abs(z) > 3.5 ? 'critical' : Math.abs(z) > 2.5 ? 'warning' : 'info'
        });
      }
    });
    return detections;
  }
  getLatestHistory(metric, n = 60) {
    const h = this.history[metric] || [];
    return h.slice(-n);
  }
  getLatestPrediction(metric, n = 60) {
    const p = this.predictions[metric] || [];
    return p.slice(-n);
  }
}
// ============================================================
// Visualization Engine
// ============================================================
const detector = new AnomalyDetector();
// Canvas setup
const mainCanvas = document.getElementById('mainChart');
const mainCtx = mainCanvas.getContext('2d');
const heatCanvas = document.getElementById('heatmapCanvas');
const heatCtx = heatCanvas.getContext('2d');
const cusumCanvas = document.getElementById('cusumCanvas');
const cusumCtx = cusumCanvas.getContext('2d');
function resizeCanvases() {
  [mainCanvas, heatCanvas, cusumCanvas].forEach(c => {
    const rect = c.parentElement.getBoundingClientRect();
    const w = rect.width - 32;
    const isMain = c === mainCanvas;
    const isHeat = c === heatCanvas;
    const h = isMain ? 260 : isHeat ? 170 : 100;
    const dpr = window.devicePixelRatio || 1;
    c.width = w * dpr;
    c.height = h * dpr;
    c.style.width = w + 'px';
    c.style.height = h + 'px';
    const ctx = c.getContext('2d');
    ctx.scale(dpr, dpr);
  });
}
window.addEventListener('resize', resizeCanvases);
// Pulse particle system
const pulses = [];
class PulseRing {
  constructor(x, y, severity) {
    this.x = x;
    this.y = y;
    this.radius = 0;
    this.maxRadius = severity === 'critical' ? 50 : 30;
    this.opacity = 0.8;
    this.severity = severity;
    this.alive = true;
  }
  update() {
    this.radius += 1.2;
    this.opacity = Math.max(0, 0.8 * (1 - this.radius / this.maxRadius));
    if (this.opacity <= 0.01) this.alive = false;
  }
  draw(ctx) {
    const color = this.severity === 'critical' ? '255,107,107' : this.severity === 'warning' ? '254,202,87' : '72,219,251';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(${color},${this.opacity})`;
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius * 0.7, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(${color},${this.opacity * 0.3})`;
    ctx.lineWidth = 1;
    ctx.stroke();
    // Glow
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius * 0.3, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${color},${this.opacity * 0.25})`;
    ctx.fill();
  }
}
// Main chart draw
function drawMainChart() {
  const w = mainCanvas.width / (window.devicePixelRatio || 1);
  const h = mainCanvas.height / (window.devicePixelRatio || 1);
  const ctx = mainCtx;
  ctx.clearRect(0, 0, w, h);
  const pad = { top: 10, bottom: 20, left: 38, right: 14 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  const metric = 'latency_ms';
  const data = detector.getLatestHistory(metric, 50);
  const pred = detector.getLatestPrediction(metric, 50);
  if (data.length < 2) return;
  const min = Math.min(...data, ...pred) * 0.85;
  const max = Math.max(...data, ...pred) * 1.15;
  const range = max - min || 1;
  const toX = (i) => pad.left + (i / (data.length - 1)) * plotW;
  const toY = (v) => pad.top + plotH - ((v - min) / range) * plotH;
  // Grid lines
  ctx.strokeStyle = 'rgba(255,255,255,0.04)';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + (i / 4) * plotH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(w - pad.right, y);
    ctx.stroke();
    ctx.fillStyle = 'rgba(200,214,229,0.2)';
    ctx.font = '9px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText((max - (i / 4) * range).toFixed(1), pad.left - 4, y + 3);
  }
  // Dynamic threshold bands
  const vals = data;
  const mean = vals.reduce((a,b) => a+b, 0) / vals.length;
  const std = Math.sqrt(vals.reduce((a,b) => a + (b-mean)**2, 0) / vals.length);
  const upperBand = mean + 2.5 * std;
  const lowerBand = mean - 2.5 * std;
  // Threshold fill
  ctx.fillStyle = 'rgba(255,107,107,0.06)';
  ctx.fillRect(pad.left, toY(upperBand), plotW, toY(lowerBand) - toY(upperBand));
  // Upper threshold line
  ctx.beginPath();
  ctx.moveTo(pad.left, toY(upperBand));
  ctx.lineTo(w - pad.right, toY(upperBand));
  ctx.strokeStyle = 'rgba(255,107,107,0.4)';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.stroke();
  ctx.setLineDash([]);
  // Lower threshold line
  ctx.beginPath();
  ctx.moveTo(pad.left, toY(lowerBand));
  ctx.lineTo(w - pad.right, toY(lowerBand));
  ctx.strokeStyle = 'rgba(72,219,251,0.4)';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.stroke();
  ctx.setLineDash([]);
  // Rolling mean
  ctx.beginPath();
  for (let i = 0; i < data.length; i++) {
    const windowSlice = data.slice(Math.max(0, i - 5), i + 1);
    const m = windowSlice.reduce((a,b) => a+b, 0) / windowSlice.length;
    const x = toX(i);
    const y = toY(m);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = 'rgba(254,202,87,0.5)';
  ctx.lineWidth = 1.5;
  ctx.stroke();
  // Prediction line (dashed)
  ctx.beginPath();
  for (let i = 0; i < pred.length; i++) {
    const x = toX(i);
    const y = toY(pred[i]);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = 'rgba(72,219,251,0.25)';
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 4]);
  ctx.stroke();
  ctx.setLineDash([]);
  // Drift fill (prediction vs actual gap)
  const driftGaps = [];
  for (let i = 0; i < Math.min(data.length, pred.length); i++) {
    const gap = data[i] - pred[i];
    driftGaps.push(gap);
    const x = toX(i);
    const y1 = toY(data[i]);
    const y2 = toY(pred[i]);
    if (Math.abs(gap) > std * 0.5) {
      ctx.beginPath();
      ctx.moveTo(x, y1);
      ctx.lineTo(x, y2);
      ctx.strokeStyle = gap > 0 ? 'rgba(255,107,107,0.15)' : 'rgba(29,209,161,0.15)';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }
  // Main metric line
  ctx.beginPath();
  for (let i = 0; i < data.length; i++) {
    const x = toX(i);
    const y = toY(data[i]);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = '#48dbfb';
  ctx.lineWidth = 2;
  ctx.stroke();
  // Pulse rings at anomaly points
  const anomalyPoints = detector.anomalies.filter(a => {
    const stepIndex = a.time - (detector.time - data.length + 1);
    return stepIndex >= 0 && stepIndex < data.length;
  });
  anomalyPoints.forEach(a => {
    const stepIndex = a.time - (detector.time - data.length + 1);
    if (stepIndex < 0 || stepIndex >= data.length) return;
    const x = toX(stepIndex);
    const y = toY(data[stepIndex]);
    const maxSev = a.detections.reduce((m, d) => d.severity === 'critical' ? 'critical' : m, 'warning');
    pulses.push(new PulseRing(x, y, maxSev));
    // Draw marker
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fillStyle = maxSev === 'critical' ? 'rgba(255,107,107,0.7)' : 'rgba(254,202,87,0.7)';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, Math.PI * 2);
    ctx.strokeStyle = maxSev === 'critical' ? 'rgba(255,107,107,0.4)' : 'rgba(254,202,87,0.4)';
    ctx.lineWidth = 2;
    ctx.stroke();
  });
  // Update pulse animations
  for (let i = pulses.length - 1; i >= 0; i--) {
    pulses[i].update();
    pulses[i].draw(ctx);
    if (!pulses[i].alive) pulses.splice(i, 1);
  }
  // Y-axis label
  ctx.fillStyle = 'rgba(200,214,229,0.3)';
  ctx.font = '9px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('latency_ms', pad.left + 2, pad.top + 10);
}
// Heatmap draw
function drawHeatmap() {
  const w = heatCanvas.width / (window.devicePixelRatio || 1);
  const h = heatCanvas.height / (window.devicePixelRatio || 1);
  const ctx = heatCtx;
  ctx.clearRect(0, 0, w, h);
  const pad = { top: 6, bottom: 14, left: 56, right: 10 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  const cols = 20;
  const rows = METRICS;
  const cellW = plotW / cols;
  const cellH = plotH / rows;
  for (let row = 0; row < rows; row++) {
    const metric = METRIC_NAMES[row];
    const vals = detector.getLatestHistory(metric, cols);
    if (vals.length < 1) continue;
    const mean = vals.reduce((a,b) => a+b, 0) / vals.length;
    const std = Math.sqrt(vals.reduce((a,b) => a + (b-mean)**2, 0) / vals.length) || 1;
    for (let col = 0; col < cols; col++) {
      const idx = vals.length - cols + col;
      if (idx < 0 || idx >= vals.length) continue;
      const v = vals[idx];
      const z = (v - mean) / std;
      let r, g, b;
      const absZ = Math.min(Math.abs(z), 4);
      if (z > 0) {
        r = 255;
        g = Math.round(220 - absZ * 45);
        b = Math.round(220 - absZ * 55);
      } else {
        r = Math.round(72 + absZ * 30);
        g = Math.round(180 + absZ * 10);
        b = 251;
      }
      const x = pad.left + col * cellW;
      const y = pad.top + row * cellH;
      ctx.fillStyle = `rgb(${Math.min(r,255)},${Math.min(g,255)},${Math.min(b,255)})`;
      ctx.fillRect(x, y, cellW - 1, cellH - 1);
      // Severity label on hover zones (tooltip via title not possible on canvas, so we draw z badges on critical)
      if (Math.abs(z) > 2.5) {
        ctx.fillStyle = Math.abs(z) > 3.5 ? '#ff6b6b' : '#feca57';
        ctx.font = 'bold 7px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(z > 0 ? '+' : '-', x + cellW / 2, y + cellH / 2 + 2);
      }
    }
    // Row label
    ctx.fillStyle = 'rgba(200,214,229,0.5)';
    ctx.font = '9px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(METRIC_NAMES[row], pad.left - 6, pad.top + row * cellH + cellH / 2 + 3);
  }
  // Time labels on x-axis
  for (let col = 0; col < cols; col += 4) {
    const x = pad.left + col * cellW;
    ctx.fillStyle = 'rgba(200,214,229,0.2)';
    ctx.font = '7px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('-' + ((cols - col) * 3) + 's', x + cellW / 2, h - 3);
  }
}
// CUSUM / change-point chart
function drawCUSUM() {
  const w = cusumCanvas.width / (window.devicePixelRatio || 1);
  const h = cusumCanvas.height / (window.devicePixelRatio || 1);
  const ctx = cusumCtx;
  ctx.clearRect(0, 0, w, h);
  const pad = { top: 8, bottom: 16, left: 30, right: 10 };
  const plotW = w - pad.left - pad.right;
  const plotH = h - pad.top - pad.bottom;
  const metric = 'error_rate';
  const data = detector.getLatestHistory(metric, 50);
  if (data.length < 5) return;
  // CUSUM calculation
  const target = data.slice(0, 10).reduce((a,b) => a+b, 0) / 10;
  let cusumPos = 0;
  let cusumNeg = 0;
  const k = 0.25;
  const cusumVals = [];
  for (let i = 0; i < data.length; i++) {
    const dev = data[i] - target;
    cusumPos = Math.max(0, cusumPos + dev - k);
    cusumNeg = Math.min(0, cusumNeg + dev + k);
    cusumVals.push({ pos: cusumPos, neg: cusumNeg, dev });
  }
  const allCusum = cusumVals.flatMap(v => [v.pos, v.neg]);
  const cMin = Math.min(0, ...allCusum);
  const cMax = Math.max(0, ...allCusum);
  const cRange = (cMax - cMin) || 1;
  const toX = (i) => pad.left + (i / (data.length - 1)) * plotW;
  const toY = (v) => pad.top + plotH - ((v - cMin) / cRange) * plotH;
  // Zero line
  ctx.beginPath();
  ctx.moveTo(pad.left, toY(0));
  ctx.lineTo(w - pad.right, toY(0));
  ctx.strokeStyle = 'rgba(200,214,229,0.15)';
  ctx.lineWidth = 1;
  ctx.setLineDash([2, 4]);
  ctx.stroke();
  ctx.setLineDash([]);
  // Decision threshold lines
  const hVal = 0.8;
  ctx.beginPath();
  ctx.moveTo(pad.left, toY(hVal));
  ctx.lineTo(w - pad.right, toY(hVal));
  ctx.strokeStyle = 'rgba(255,107,107,0.3)';
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 3]);
  ctx.stroke();
  ctx.fillStyle = 'rgba(255,107,107,0.2)';
  ctx.font = '8px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('threshold', w - pad.right - 44, toY(hVal) - 3);
  // CUSUM+ line
  ctx.beginPath();
  for (let i = 0; i < cusumVals.length; i++) {
    const x = toX(i);
    const y = toY(cusumVals[i].pos);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = '#ff6b6b';
  ctx.lineWidth = 1.5;
  ctx.stroke();
  // CUSUM- line
  ctx.beginPath();
  for (let i = 0; i < cusumVals.length; i++) {
    const x = toX(i);
    const y = toY(cusumVals[i].neg);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = '#48dbfb';
  ctx.lineWidth = 1.5;
  ctx.stroke();
  // Change point markers
  for (let i = 1; i < cusumVals.length; i++) {
    if ((cusumVals[i].pos > hVal && cusumVals[i-1].pos <= hVal) ||
        (cusumVals[i].neg < -hVal && cusumVals[i-1].neg >= -hVal)) {
      const x = toX(i);
      ctx.beginPath();
      ctx.arc(x, toY(cusumVals[i].pos > hVal ? cusumVals[i].pos : cusumVals[i].neg), 4, 0, Math.PI * 2);
      ctx.fillStyle = '#feca57';
      ctx.fill();
    }
  }
  ctx.fillStyle = 'rgba(200,214,229,0.3)';
  ctx.font = '8px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('CUSUM+ (red) / CUSUM- (blue)', pad.left + 2, pad.top + 9);
}
// Root-cause analysis
function updateRootCause() {
  const list = document.getElementById('rootCauseList');
  const recentAnomalies = detector.anomalies.slice(-3).reverse();
  if (recentAnomalies.length === 0) {
    list.innerHTML = '<li style="color:rgba(200,214,229,.4);font-style:italic">Awaiting anomaly events...</li>';
    return;
  }
  let html = '';
  recentAnomalies.forEach((a, aidx) => {
    const sev = a.detections.some(d => d.severity === 'critical') ? 'critical' : 'warning';
    const sevClass = sev === 'critical' ? 'critical' : 'warning';
    const sevLabel = sev === 'critical' ? 'CRIT' : 'WARN';
    a.detections.forEach((d, didx) => {
      const arrow = didx === 0 ? '\u25B6' : '\u2192';
      const chain = didx === 0 ? METRIC_NAMES.filter((m, mi) => {
        return m !== d.metric && Math.abs(detector.history[m].slice(-1)[0] - METRIC_BASELINES[mi]) > METRIC_VARIANCES[mi] * 0.8;
      }).slice(0, 2) : [];
      html += `<li class="${sevClass}">`;
      html += `<span class="z-badge">${sevLabel}</span>`;
      html += `<span class="metric-name">${d.metric}</span>`;
      html += `<span class="metric-desc">value=${d.value.toFixed(1)}, z=${d.zScore.toFixed(2)}</span>`;
      if (chain.length > 0) {
        html += `<span class="arrow">${arrow}</span>`;
        html += `<span class="metric-desc">preceded by ${chain.join(', ')}</span>`;
      }
      html += '</li>';
    });
  });
  list.innerHTML = html;
}
// Metric cards update
function updateMetrics() {
  const metric = 'latency_ms';
  const data = detector.getLatestHistory(metric, 20);
  if (data.length < 2) return;
  const mean = data.reduce((a,b) => a+b, 0) / data.length;
  const std = Math.sqrt(data.reduce((a,b) => a + (b-mean)**2, 0) / data.length);
  const latest = data[data.length - 1];
  const z = std > 0.001 ? (latest - mean) / std : 0;
  const pred = detector.getLatestPrediction(metric);
  const lastPred = pred[pred.length - 1] || mean;
  const driftPct = lastPred > 0 ? Math.abs((latest - lastPred) / lastPred * 100) : 0;
  document.getElementById('metricCount').textContent = METRICS;
  document.getElementById('anomalyCount').textContent = detector.anomalyTimestamps.length;
  document.getElementById('currentZ').textContent = z.toFixed(2);
  const zEl = document.getElementById('currentZ');
  zEl.className = 'value' + (Math.abs(z) > 2.5 ? ' alert' : Math.abs(z) > 1.5 ? ' warn' : ' ok');
  document.getElementById('driftGap').textContent = driftPct.toFixed(1) + '%';
  const driftEl = document.getElementById('driftGap');
  driftEl.className = 'value' + (driftPct > 15 ? ' alert' : driftPct > 8 ? ' warn' : ' ok');
  const alertEl = document.getElementById('alertLevel');
  const activeAnomalies = detector.anomalies.filter(a => a.time > detector.time - 15);
  if (activeAnomalies.some(a => a.detections.some(d => d.severity === 'critical'))) {
    alertEl.textContent = 'CRITICAL';
    alertEl.className = 'value alert';
  } else if (activeAnomalies.length > 0) {
    alertEl.textContent = 'WARNING';
    alertEl.className = 'value warn';
  } else {
    alertEl.textContent = 'STABLE';
    alertEl.className = 'value ok';
  }
  document.getElementById('lastUpdateTime').innerHTML = `<span class="dot ${activeAnomalies.length > 0 ? 'red' : 'green'}"></span>Updated ${new Date().toLocaleTimeString()}`;
}
// Main loop
function tick() {
  detector.step();
  drawMainChart();
  drawHeatmap();
  drawCUSUM();
  updateRootCause();
  updateMetrics();
}
resizeCanvases();
tick();
setInterval(tick, 1500);
</script>
</body>
</html>
```