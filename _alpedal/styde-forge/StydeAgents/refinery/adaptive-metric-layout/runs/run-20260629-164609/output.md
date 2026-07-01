<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #222533;
  --border: #2a2d3a;
  --text: #e1e3eb;
  --text2: #8b8fa7;
  --accent: #6c8aff;
  --accent2: #4ef0b5;
  --warn: #f5a623;
  --danger: #f0506e;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2);
  --compact-height: 64px;
  --panel-min-w: 260px;
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
  -webkit-font-smoothing: antialiased;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}
header h1 { font-size: 1.25rem; font-weight: 600; letter-spacing: -0.3px; }
.controls { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  font-family: var(--font);
  transition: background 0.15s;
}
.btn:hover { background: var(--border); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.badge {
  font-size: 0.7rem;
  background: var(--surface2);
  padding: 3px 8px;
  border-radius: 10px;
  color: var(--text2);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--panel-min-w), 1fr));
  gap: var(--gap);
  grid-auto-flow: dense;
  transition: grid-template-columns 0.3s;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform var(--transition), opacity var(--transition), grid-column var(--transition), grid-row var(--transition), max-height var(--transition);
  cursor: grab;
  position: relative;
  contain: layout style;
}
.panel:active { cursor: grabbing; }
.panel.locked { cursor: default; border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.panel.compact { max-height: var(--compact-height); }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-compact-preview { display: flex; }
.panel.dragging { opacity: 0.6; transform: scale(0.97); z-index: 10; }
.panel.drag-over { border-color: var(--accent2); box-shadow: 0 0 12px rgba(78,240,181,0.25); }
.panel[data-rank="1"] { grid-column: span 2; grid-row: span 2; }
@media (max-width: 900px) {
  .panel[data-rank="1"] { grid-column: span 2; grid-row: span 1; }
}
@media (max-width: 600px) {
  .panel[data-rank="1"] { grid-column: span 1; }
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  user-select: none;
}
.panel-header h3 {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: -0.2px;
  display: flex;
  align-items: center;
  gap: 7px;
}
.panel-header h3 .dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}
.panel-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}
.panel-actions button {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 0.85rem;
  line-height: 1;
  transition: color 0.15s, background 0.15s;
}
.panel-actions button:hover { color: var(--text); background: var(--surface2); }
.panel-actions button.pinned { color: var(--accent); }
.panel-body { padding: 14px; position: relative; }
.panel-compact-preview {
  display: none;
  padding: 12px 14px;
  align-items: center;
  gap: 12px;
  font-size: 0.8rem;
  color: var(--text2);
}
.panel-compact-preview .mini-stat {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}
.panel-compact-preview .mini-spark {
  flex: 1;
  height: 28px;
}
.panel-compact-preview .mini-spark svg { width: 100%; height: 100%; }
.metric-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 10px;
}
.metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: -1px;
  font-variant-numeric: tabular-nums;
}
.metric-unit { color: var(--text2); font-size: 0.8rem; }
.metric-delta {
  font-size: 0.75rem;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}
.metric-delta.up { color: var(--accent2); background: rgba(78,240,181,0.1); }
.metric-delta.down { color: var(--danger); background: rgba(240,80,110,0.1); }
.bar-container { height: 6px; background: var(--surface2); border-radius: 3px; overflow: hidden; margin-bottom: 6px; }
.bar-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.bar-label { font-size: 0.7rem; color: var(--text2); display: flex; justify-content: space-between; }
.gauge-svg { display: block; margin: 0 auto; }
.sparkline-svg { width: 100%; height: 60px; display: block; }
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stat-item { text-align: center; }
.stat-item .stat-val { font-size: 1.3rem; font-weight: 700; }
.stat-item .stat-lbl { font-size: 0.7rem; color: var(--text2); }
.heat-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
.heat-cell {
  aspect-ratio: 1;
  border-radius: 3px;
  background: var(--surface2);
  transition: background 0.3s;
}
.usage-rank {
  font-size: 0.7rem;
  color: var(--text2);
  padding: 2px 5px;
  background: var(--surface2);
  border-radius: 4px;
}
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  z-index: 100;
}
.toast.show { opacity: 1; }
.drop-indicator {
  position: absolute;
  height: 3px;
  background: var(--accent2);
  border-radius: 2px;
  pointer-events: none;
  z-index: 20;
  opacity: 0;
  transition: opacity 0.15s;
  left: 0; right: 0;
}
.drop-indicator.show { opacity: 1; }
@keyframes rankBump {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}
.panel.rank-changed { animation: rankBump 0.4s ease; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <span class="badge" id="tracking-status">Tracking active</span>
    <button class="btn" id="btn-reset-layout" title="Reset all layout preferences">Reset Layout</button>
    <button class="btn" id="btn-export" title="Export tracking data">Export Data</button>
  </div>
</header>
<div class="grid" id="grid" role="list"></div>
<div class="toast" id="toast" aria-live="polite"></div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v2';
const RANK_INTERVAL = 30000;
const VIEW_DURATION_SAMPLE_INTERVAL = 2000;
const DECAY_HALF_LIFE = 7 * 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD_PERCENTILE = 0.35;
const MIN_RANK_SCORE = 0.01;
const PANEL_DEFS = [
  { id: 'cpu', title: 'CPU Usage', dotColor: '#6c8aff', type: 'gauge', metric: 'cpu_pct', unit: '%', target: 65 },
  { id: 'memory', title: 'Memory', dotColor: '#f5a623', type: 'bar', metric: 'mem_pct', unit: '%', target: 80 },
  { id: 'network', title: 'Network I/O', dotColor: '#4ef0b5', type: 'spark', metric: 'net_mbps', unit: 'Mbps', target: 500 },
  { id: 'users', title: 'Active Users', dotColor: '#c084fc', type: 'counter', metric: 'active_users', unit: '', target: 1000 },
  { id: 'errors', title: 'Error Rate', dotColor: '#f0506e', type: 'spark', metric: 'err_rate', unit: '%', target: 1 },
  { id: 'latency', title: 'Response Time', dotColor: '#f97316', type: 'histogram', metric: 'latency_ms', unit: 'ms', target: 200 },
  { id: 'requests', title: 'Requests/min', dotColor: '#22d3ee', type: 'counter', metric: 'rpm', unit: '/min', target: 5000 },
  { id: 'disk', title: 'Disk I/O', dotColor: '#a78bfa', type: 'bar', metric: 'disk_pct', unit: '%', target: 70 }
];
let panels = [];
let tracking = {};
let layoutOrder = [];
let lockedPanels = new Set();
let manualPositions = {};
let rankScores = {};
let lastRankTime = 0;
let rankEpoch = 0;
let intersectionObserver = null;
let resizeObserver = null;
let toastTimer = null;
let viewDurationTimer = null;
let dragState = null;
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    return JSON.parse(raw);
  } catch (e) { return {}; }
}
function saveState(state) {
  try {
    const existing = loadState();
    const merged = { ...existing, ...state };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
  } catch (e) {}
}
function now() { return Date.now(); }
function getMetricValue(panelId) {
  const def = PANEL_DEFS.find(p => p.id === panelId);
  if (!def) return 0;
  const t = now() / 1000;
  const seed = panelId.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  const base = {
    cpu: 35 + 25 * Math.sin(t * 0.3 + seed) + 10 * Math.sin(t * 0.7 + seed * 1.3),
    memory: 55 + 15 * Math.sin(t * 0.15 + seed * 0.7) + 5 * Math.sin(t * 0.4),
    net_mbps: 280 + 180 * Math.sin(t * 0.25 + seed) + 60 * Math.cos(t * 0.5 + seed * 2),
    active_users: 600 + 350 * Math.sin(t * 0.1 + seed * 0.3) + 100 * Math.sin(t * 0.02 + seed),
    err_rate: 0.4 + 0.3 * Math.abs(Math.sin(t * 0.4 + seed)) + 0.1 * Math.sin(t * 0.8),
    latency_ms: 120 + 60 * Math.sin(t * 0.2 + seed) + 30 * Math.abs(Math.cos(t * 0.55 + seed * 2)),
    rpm: 3000 + 1800 * Math.sin(t * 0.18 + seed) + 500 * Math.sin(t * 0.05 + seed * 1.5),
    disk_pct: 40 + 20 * Math.sin(t * 0.12 + seed) + 10 * Math.cos(t * 0.35)
  };
  const raw = base[def.metric] || 40;
  return Math.max(0, Math.round(raw * 10) / 10);
}
function getSparklineData(panelId, points) {
  const data = [];
  const seed = panelId.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  for (let i = 0; i < points; i++) {
    const t = (now() / 1000) - (points - i) * 2;
    const base = {
      cpu: 40 + 20 * Math.sin(t * 0.3 + seed) + 8 * Math.sin(t * 0.7 + seed * 1.3),
      memory: 55 + 12 * Math.sin(t * 0.15 + seed * 0.7),
      net_mbps: 300 + 150 * Math.sin(t * 0.25 + seed),
      active_users: 600 + 300 * Math.sin(t * 0.12 + seed),
      err_rate: 0.5 + 0.25 * Math.sin(t * 0.5 + seed),
      latency_ms: 130 + 50 * Math.sin(t * 0.22 + seed),
      rpm: 3200 + 1500 * Math.sin(t * 0.17 + seed),
      disk_pct: 45 + 18 * Math.sin(t * 0.14 + seed * 1.1)
    };
    const def = PANEL_DEFS.find(p => p.id === panelId);
    const val = def ? (base[def.metric] || 40) : 40;
    data.push(Math.max(0, Math.round(val * 10) / 10));
  }
  return data;
}
function computeAttentionScore(panelId) {
  const t = tracking[panelId];
  if (!t) return MIN_RANK_SCORE;
  const age = now() - Math.max(t.lastInteraction || t.lastViewed || 0);
  const recencyDecay = Math.pow(0.5, age / DECAY_HALF_LIFE);
  const frequency = t.interactionCount || 1;
  const duration = t.viewDurationMs || 0;
  const durationWeight = Math.log2((duration / 1000) + 1) + 1;
  return Math.max(MIN_RANK_SCORE, frequency * durationWeight * recencyDecay);
}
function rankPanels() {
  const scores = {};
  PANEL_DEFS.forEach(def => { scores[def.id] = computeAttentionScore(def.id); });
  rankScores = scores;
  const sorted = PANEL_DEFS.map(d => d.id).sort((a, b) => {
    if (lockedPanels.has(a) && lockedPanels.has(b)) return 0;
    if (lockedPanels.has(a)) return -1;
    if (lockedPanels.has(b)) return 1;
    return scores[b] - scores[a];
  });
  const oldOrder = [...layoutOrder];
  layoutOrder = sorted;
  rankEpoch++;
  lastRankTime = now();
  return !oldOrder.length || sorted.some((id, i) => oldOrder[i] !== id);
}
function shouldBeCompact(panelId) {
  if (lockedPanels.has(panelId)) return false;
  const scores = Object.values(rankScores).filter(s => s > MIN_RANK_SCORE).sort((a, b) => a - b);
  if (scores.length < 3) return false;
  const cutoffIndex = Math.floor(scores.length * COMPACT_THRESHOLD_PERCENTILE);
  const threshold = scores[cutoffIndex] || 0;
  return (rankScores[panelId] || 0) < threshold;
}
function getLayoutPosition(panelId) {
  if (lockedPanels.has(panelId) && manualPositions[panelId] !== undefined) {
    return manualPositions[panelId];
  }
  return layoutOrder.indexOf(panelId);
}
function renderSparkline(el, data, color, height, width) {
  if (!data.length) return;
  const h = height || 60;
  const w = width || el.clientWidth || 200;
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const pad = 2;
  const points = data.map((v, i) => {
    const x = pad + (i / (data.length - 1)) * (w - pad * 2);
    const y = pad + (1 - (v - min) / range) * (h - pad * 2);
    return `${x},${y}`;
  }).join(' ');
  const area = `${pad},${h - pad} ${points} ${w - pad},${h - pad}`;
  const frag = document.createDocumentFragment();
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('preserveAspectRatio', 'none');
  svg.style.display = 'block';
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const grad = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
  grad.setAttribute('id', `sg-${color.replace('#','')}`);
  grad.setAttribute('x1', '0'); grad.setAttribute('y1', '0');
  grad.setAttribute('x2', '0'); grad.setAttribute('y2', '1');
  const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
  stop1.setAttribute('offset', '0%'); stop1.setAttribute('stop-color', color); stop1.setAttribute('stop-opacity', '0.35');
  const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
  stop2.setAttribute('offset', '100%'); stop2.setAttribute('stop-color', color); stop2.setAttribute('stop-opacity', '0.02');
  grad.appendChild(stop1); grad.appendChild(stop2); defs.appendChild(grad); svg.appendChild(defs);
  const areaPath = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
  areaPath.setAttribute('points', area);
  areaPath.setAttribute('fill', `url(#sg-${color.replace('#','')})`);
  areaPath.setAttribute('stroke', 'none');
  svg.appendChild(areaPath);
  const linePath = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
  linePath.setAttribute('points', points);
  linePath.setAttribute('fill', 'none');
  linePath.setAttribute('stroke', color);
  linePath.setAttribute('stroke-width', '1.5');
  linePath.setAttribute('stroke-linejoin', 'round');
  linePath.setAttribute('stroke-linecap', 'round');
  svg.appendChild(linePath);
  frag.appendChild(svg);
  el.textContent = '';
  el.appendChild(frag);
}
function renderGauge(el, value, max, color) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const size = 100;
  const strokeW = 8;
  const r = (size - strokeW) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - pct / 100);
  const frag = document.createDocumentFragment();
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${size} ${size}`);
  svg.setAttribute('width', size);
  svg.setAttribute('height', size);
  svg.setAttribute('class', 'gauge-svg');
  const bg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  bg.setAttribute('cx', size/2); bg.setAttribute('cy', size/2); bg.setAttribute('r', r);
  bg.setAttribute('fill', 'none'); bg.setAttribute('stroke', 'var(--surface2)'); bg.setAttribute('stroke-width', strokeW);
  svg.appendChild(bg);
  const fg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  fg.setAttribute('cx', size/2); fg.setAttribute('cy', size/2); fg.setAttribute('r', r);
  fg.setAttribute('fill', 'none'); fg.setAttribute('stroke', color); fg.setAttribute('stroke-width', strokeW);
  fg.setAttribute('stroke-dasharray', circ); fg.setAttribute('stroke-dashoffset', offset);
  fg.setAttribute('stroke-linecap', 'round');
  fg.setAttribute('transform', `rotate(-90 ${size/2} ${size/2})`);
  fg.style.transition = 'stroke-dashoffset 0.6s ease';
  svg.appendChild(fg);
  const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  text.setAttribute('x', size/2); text.setAttribute('y', size/2 + 6);
  text.setAttribute('text-anchor', 'middle'); text.setAttribute('font-size', '22');
  text.setAttribute('font-weight', '700'); text.setAttribute('fill', 'var(--text)');
  text.setAttribute('font-family', 'var(--font)');
  text.textContent = Math.round(value);
  svg.appendChild(text);
  frag.appendChild(svg);
  el.textContent = '';
  el.appendChild(frag);
}
function renderHeatmap(el, data) {
  const frag = document.createDocumentFragment();
  const grid = document.createElement('div');
  grid.className = 'heat-grid';
  data.forEach(v => {
    const cell = document.createElement('div');
    cell.className = 'heat-cell';
    const intensity = Math.min(1, Math.max(0, v / 100));
    const r = Math.round(30 + intensity * 60);
    const g = Math.round(180 + intensity * 60);
    cell.style.background = `rgb(${r},${g},130)`;
    grid.appendChild(cell);
  });
  frag.appendChild(grid);
  el.textContent = '';
  el.appendChild(frag);
}
function renderBar(el, value, max, color) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const frag = document.createDocumentFragment();
  const container = document.createElement('div');
  container.className = 'bar-container';
  const fill = document.createElement('div');
  fill.className = 'bar-fill';
  fill.style.width = `${pct}%`;
  fill.style.background = color;
  container.appendChild(fill);
  frag.appendChild(container);
  const label = document.createElement('div');
  label.className = 'bar-label';
  const valSpan = document.createElement('span');
  valSpan.textContent = `${Math.round(value)}%`;
  const maxSpan = document.createElement('span');
  maxSpan.textContent = `${max}%`;
  label.appendChild(valSpan); label.appendChild(maxSpan);
  frag.appendChild(label);
  el.textContent = '';
  el.appendChild(frag);
}
function renderCompactPreview(panelId, el, def) {
  const val = getMetricValue(panelId);
  const sparkData = getSparklineData(panelId, 20);
  const frag = document.createDocumentFragment();
  const stat = document.createElement('span');
  stat.className = 'mini-stat';
  stat.textContent = def.unit ? `${Math.round(val)}${def.unit}` : `${Math.round(val)}`;
  frag.appendChild(stat);
  const spark = document.createElement('span');
  spark.className = 'mini-spark';
  frag.appendChild(spark);
  el.textContent = '';
  el.appendChild(frag);
  requestAnimationFrame(() => {
    renderSparkline(spark, sparkData, def.dotColor, 28, el.clientWidth - 100);
  });
}
function renderPanelBody(panelId, bodyEl, def) {
  const val = getMetricValue(panelId);
  const frag = document.createDocumentFragment();
  const row = document.createElement('div');
  row.className = 'metric-row';
  const vSpan = document.createElement('span');
  vSpan.className = 'metric-value';
  vSpan.textContent = def.unit ? `${Math.round(val)}` : `${Math.round(val)}`;
  row.appendChild(vSpan);
  if (def.unit) {
    const uSpan = document.createElement('span');
    uSpan.className = 'metric-unit';
    uSpan.textContent = def.unit;
    row.appendChild(uSpan);
  }
  const prevVal = getMetricValue(panelId + '_prev') || val;
  const delta = val - prevVal;
  if (Math.abs(delta) > 0.01) {
    const dSpan = document.createElement('span');
    dSpan.className = 'metric-delta';
    dSpan.classList.add(delta > 0 ? 'up' : 'down');
    dSpan.textContent = `${delta > 0 ? '+' : ''}${delta.toFixed(1)}${def.unit}`;
    row.appendChild(dSpan);
  }
  frag.appendChild(row);
  if (def.type === 'gauge') {
    const gaugeWrap = document.createElement('div');
    frag.appendChild(gaugeWrap);
    requestAnimationFrame(() => renderGauge(gaugeWrap, val, def.target, def.dotColor));
  } else if (def.type === 'bar') {
    const barWrap = document.createElement('div');
    frag.appendChild(barWrap);
    requestAnimationFrame(() => renderBar(barWrap, val, def.target, def.dotColor));
  } else if (def.type === 'spark') {
    const sparkWrap = document.createElement('div');
    sparkWrap.className = 'sparkline-svg';
    frag.appendChild(sparkWrap);
    const sparkData = getSparklineData(panelId, 24);
    requestAnimationFrame(() => renderSparkline(sparkWrap, sparkData, def.dotColor, 60, sparkWrap.clientWidth || 250));
  } else if (def.type === 'counter') {
    const statGrid = document.createElement('div');
    statGrid.className = 'stat-grid';
    ['Peak', 'Avg', 'Min', 'Now'].forEach(label => {
      const item = document.createElement('div');
      item.className = 'stat-item';
      const vEl = document.createElement('div');
      vEl.className = 'stat-val';
      const lEl = document.createElement('div');
      lEl.className = 'stat-lbl';
      lEl.textContent = label;
      const variation = label === 'Peak' ? val * 1.3 : label === 'Min' ? val * 0.6 : label === 'Avg' ? val * 0.95 : val;
      vEl.textContent = Math.round(variation);
      item.appendChild(vEl); item.appendChild(lEl);
      statGrid.appendChild(item);
    });
    frag.appendChild(statGrid);
  } else if (def.type === 'histogram') {
    const barWrap = document.createElement('div');
    frag.appendChild(barWrap);
    requestAnimationFrame(() => renderBar(barWrap, val, def.target, def.dotColor));
    const heatWrap = document.createElement('div');
    frag.appendChild(heatWrap);
    const heatData = Array.from({length: 28}, (_, i) => {
      const t = (now()/1000) - (28 - i) * 300;
      return 20 + 60 * Math.abs(Math.sin(t * 0.3 + panelId.charCodeAt(0)));
    });
    requestAnimationFrame(() => renderHeatmap(heatWrap, heatData));
  }
  bodyEl.textContent = '';
  bodyEl.appendChild(frag);
}
function createPanelElement(def, rank) {
  const panel = document.createElement('div');
  panel.className = 'panel';
  panel.setAttribute('data-panel-id', def.id);
  panel.setAttribute('data-rank', rank);
  panel.setAttribute('draggable', 'true');
  panel.setAttribute('role', 'listitem');
  panel.setAttribute('aria-label', def.title);
  if (lockedPanels.has(def.id)) {
    panel.classList.add('locked');
  }
  const header = document.createElement('div');
  header.className = 'panel-header';
  const title = document.createElement('h3');
  const dot = document.createElement('span');
  dot.className = 'dot';
  dot.style.background = def.dotColor;
  title.appendChild(dot);
  title.appendChild(document.createTextNode(def.title));
  header.appendChild(title);
  const rankBadge = document.createElement('span');
  rankBadge.className = 'usage-rank';
  const score = rankScores[def.id] || 0;
  rankBadge.textContent = `Rank ${rank + 1} · ${score.toFixed(1)}`;
  rankBadge.setAttribute('data-rank-badge', '');
  header.appendChild(rankBadge);
  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const lockBtn = document.createElement('button');
  lockBtn.setAttribute('data-action', 'lock');
  lockBtn.setAttribute('aria-label', lockedPanels.has(def.id) ? 'Unlock panel' : 'Lock panel position');
  lockBtn.textContent = lockedPanels.has(def.id) ? '📌' : '📍';
  if (lockedPanels.has(def.id)) lockBtn.classList.add('pinned');
  actions.appendChild(lockBtn);
  const compactBtn = document.createElement('button');
  compactBtn.setAttribute('data-action', 'toggle-compact');
  compactBtn.setAttribute('aria-label', 'Toggle compact mode');
  compactBtn.textContent = '⊟';
  actions.appendChild(compactBtn);
  header.appendChild(actions);
  panel.appendChild(header);
  const compactPreview = document.createElement('div');
  compactPreview.className = 'panel-compact-preview';
  compactPreview.setAttribute('data-compact-preview', '');
  panel.appendChild(compactPreview);
  if (shouldBeCompact(def.id)) {
    panel.classList.add('compact');
    renderCompactPreview(def.id, compactPreview, def);
  }
  const body = document.createElement('div');
  body.className = 'panel-body';
  body.setAttribute('data-panel-body', '');
  panel.appendChild(body);
  if (!shouldBeCompact(def.id)) {
    renderPanelBody(def.id, body, def);
  }
  return panel;
}
function updatePanelElement(panelEl, def, rank, orderChanged) {
  const panelId = def.id;
  const oldRank = parseInt(panelEl.getAttribute('data-rank'));
  panelEl.setAttribute('data-rank', rank);
  if (oldRank !== rank && orderChanged) {
    panelEl.classList.add('rank-changed');
    panelEl.addEventListener('animationend', () => panelEl.classList.remove('rank-changed'), { once: true });
  }
  if (lockedPanels.has(panelId)) {
    panelEl.classList.add('locked');
  } else {
    panelEl.classList.remove('locked');
  }
  const rankBadge = panelEl.querySelector('[data-rank-badge]');
  if (rankBadge) {
    rankBadge.textContent = `Rank ${rank + 1} · ${(rankScores[panelId] || 0).toFixed(1)}`;
  }
  const lockBtn = panelEl.querySelector('[data-action="lock"]');
  if (lockBtn) {
    lockBtn.textContent = lockedPanels.has(panelId) ? '📌' : '📍';
    lockBtn.setAttribute('aria-label', lockedPanels.has(panelId) ? 'Unlock panel' : 'Lock panel position');
    if (lockedPanels.has(panelId)) { lockBtn.classList.add('pinned'); }
    else { lockBtn.classList.remove('pinned'); }
  }
  const isCompact = shouldBeCompact(panelId);
  const wasCompact = panelEl.classList.contains('compact');
  if (isCompact !== wasCompact) {
    if (isCompact) {
      panelEl.classList.add('compact');
      const previewEl = panelEl.querySelector('[data-compact-preview]');
      if (previewEl) renderCompactPreview(panelId, previewEl, def);
    } else {
      panelEl.classList.remove('compact');
      const bodyEl = panelEl.querySelector('[data-panel-body]');
      if (bodyEl) renderPanelBody(panelId, bodyEl, def);
    }
  } else if (!isCompact) {
    const bodyEl = panelEl.querySelector('[data-panel-body]');
    if (bodyEl) {
      const metricEl = bodyEl.querySelector('.metric-value');
      const val = getMetricValue(panelId);
      if (metricEl) {
        const newText = def.unit ? `${Math.round(val)}` : `${Math.round(val)}`;
        if (metricEl.textContent !== newText) {
          metricEl.textContent = newText;
        }
      }
      const gaugeWrap = bodyEl.querySelector('.gauge-svg')?.parentElement;
      if (gaugeWrap && def.type === 'gauge') {
        const svg = gaugeWrap.querySelector('svg');
        if (svg) {
          const fg = svg.querySelector('circle[stroke-dasharray]');
          if (fg) {
            const pct = Math.min(100, Math.max(0, (val / def.target) * 100));
            const size = 100; const strokeW = 8;
            const r = (size - strokeW) / 2;
            const circ = 2 * Math.PI * r;
            const newOffset = circ * (1 - pct / 100);
            if (Math.abs(parseFloat(fg.getAttribute('stroke-dashoffset')) - newOffset) > 0.01) {
              fg.setAttribute('stroke-dashoffset', newOffset);
            }
          }
          const textEl = svg.querySelector('text');
          if (textEl) {
            const newVal = String(Math.round(val));
            if (textEl.textContent !== newVal) {
              textEl.textContent = newVal;
            }
          }
        }
      }
      const barFill = bodyEl.querySelector('.bar-fill');
      if (barFill && (def.type === 'bar' || def.type === 'histogram')) {
        const pct = Math.min(100, Math.max(0, (val / def.target) * 100));
        const newWidth = `${pct}%`;
        if (barFill.style.width !== newWidth) {
          barFill.style.width = newWidth;
        }
      }
    }
  } else if (isCompact) {
    const previewEl = panelEl.querySelector('[data-compact-preview]');
    if (previewEl) {
      const statEl = previewEl.querySelector('.mini-stat');
      const val = getMetricValue(panelId);
      const newText = def.unit ? `${Math.round(val)}${def.unit}` : `${Math.round(val)}`;
      if (statEl && statEl.textContent !== newText) {
        statEl.textContent = newText;
      }
    }
  }
}
function reconcileDOM(grid, changed) {
  const existingPanels = new Map();
  grid.querySelectorAll('.panel').forEach(el => {
    existingPanels.set(el.getAttribute('data-panel-id'), el);
  });
  const frag = document.createDocumentFragment();
  const orderedDefs = layoutOrder.map(id => PANEL_DEFS.find(d => d.id === id)).filter(Boolean);
  orderedDefs.forEach((def, rank) => {
    let panelEl = existingPanels.get(def.id);
    if (!panelEl) {
      panelEl = createPanelElement(def, rank);
      existingPanels.delete(def.id);
    }
    updatePanelElement(panelEl, def, rank, changed);
    frag.appendChild(panelEl);
  });
  existingPanels.forEach(el => el.remove());
  const currentOrder = Array.from(grid.children).map(el => el.getAttribute('data-panel-id'));
  const newOrder = orderedDefs.map(d => d.id);
  const needsReorder = currentOrder.join(',') !== newOrder.join(',');
  if (needsReorder) {
    grid.textContent = '';
    grid.appendChild(frag);
  } else {
    const targetRanks = new Map();
    orderedDefs.forEach((d, rank) => targetRanks.set(d.id, rank));
    grid.querySelectorAll('.panel').forEach(el => {
      const id = el.getAttribute('data-panel-id');
      const rank = targetRanks.get(id);
      if (rank !== undefined) {
        el.setAttribute('data-rank', rank);
      }
    });
  }
}
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}
function handleGridClick(e) {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const panelEl = btn.closest('.panel');
  if (!panelEl) return;
  const panelId = panelEl.getAttribute('data-panel-id');
  const action = btn.getAttribute('data-action');
  if (action === 'lock') {
    if (lockedPanels.has(panelId)) {
      lockedPanels.delete(panelId);
      showToast(`${PANEL_DEFS.find(d => d.id === panelId)?.title || panelId}: Auto-layout restored`);
    } else {
      lockedPanels.add(panelId);
      manualPositions[panelId] = layoutOrder.indexOf(panelId);
      showToast(`${PANEL_DEFS.find(d => d.id === panelId)?.title || panelId}: Position locked`);
    }
    saveState({ lockedPanels: [...lockedPanels], manualPositions });
    rankPanels();
    reconcileDOM(grid, true);
    return;
  }
  if (action === 'toggle-compact') {
    const isCompact = panelEl.classList.contains('compact');
    if (isCompact) {
      lockedPanels.add(panelId);
    } else {
      lockedPanels.delete(panelId);
    }
    saveState({ lockedPanels: [...lockedPanels] });
    rankPanels();
    reconcileDOM(grid, true);
    return;
  }
  if (!tracking[panelId]) {
    tracking[panelId] = { interactionCount: 0, viewDurationMs: 0, lastViewed: 0, lastInteraction: 0, expandCount: 0, collapseCount: 0 };
  }
  tracking[panelId].interactionCount = (tracking[panelId].interactionCount || 0) + 1;
  tracking[panelId].lastInteraction = now();
}
function handleGridDragStart(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl || lockedPanels.has(panelEl.getAttribute('data-panel-id'))) {
    if (lockedPanels.has(panelEl?.getAttribute('data-panel-id'))) {
      e.preventDefault();
    }
    return;
  }
  dragState = {
    el: panelEl,
    id: panelEl.getAttribute('data-panel-id'),
    startX: e.clientX,
    startY: e.clientY
  };
  panelEl.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragState.id);
}
function handleGridDragOver(e) {
  e.preventDefault();
  if (!dragState) return;
  const target = e.target.closest('.panel');
  if (!target || target === dragState.el) return;
  e.dataTransfer.dropEffect = 'move';
  document.querySelectorAll('.panel.drag-over').forEach(el => el.classList.remove('drag-over'));
  target.classList.add('drag-over');
}
function handleGridDrop(e) {
  e.preventDefault();
  document.querySelectorAll('.panel.drag-over').forEach(el => el.classList.remove('drag-over'));
  if (!dragState) return;
  const targetEl = e.target.closest('.panel');
  if (!targetEl || targetEl === dragState.el) {
    dragState.el.classList.remove('dragging');
    dragState = null;
    return;
  }
  const targetId = targetEl.getAttribute('data-panel-id');
  const sourceId = dragState.id;
  const sourceIdx = layoutOrder.indexOf(sourceId);
  const targetIdx = layoutOrder.indexOf(targetId);
  if (sourceIdx >= 0 && targetIdx >= 0) {
    layoutOrder.splice(sourceIdx, 1);
    layoutOrder.splice(targetIdx, 0, sourceId);
    lockedPanels.add(sourceId);
    lockedPanels.add(targetId);
    manualPositions[sourceId] = layoutOrder.indexOf(sourceId);
    manualPositions[targetId] = layoutOrder.indexOf(targetId);
    saveState({ lockedPanels: [...lockedPanels], manualPositions });
    showToast('Panels reordered & locked');
  }
  dragState.el.classList.remove('dragging');
  dragState = null;
  reconcileDOM(grid, true);
}
function handleGridDragEnd(e) {
  if (dragState) {
    dragState.el.classList.remove('dragging');
    dragState = null;
  }
  document.querySelectorAll('.panel.drag-over').forEach(el => el.classList.remove('drag-over'));
}
function setupIntersectionObserver() {
  if (intersectionObserver) intersectionObserver.disconnect();
  const viewStartTimes = new Map();
  intersectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panelId = entry.target.getAttribute('data-panel-id');
      if (!panelId) return;
      if (!tracking[panelId]) {
        tracking[panelId] = { interactionCount: 0, viewDurationMs: 0, lastViewed: 0, lastInteraction: 0, expandCount: 0, collapseCount: 0 };
      }
      if (entry.isIntersecting) {
        viewStartTimes.set(panelId, now());
        tracking[panelId].lastViewed = now();
      } else {
        const startTime = viewStartTimes.get(panelId);
        if (startTime) {
          tracking[panelId].viewDurationMs = (tracking[panelId].viewDurationMs || 0) + (now() - startTime);
          viewStartTimes.delete(panelId);
        }
      }
    });
    saveState({ tracking });
  }, { threshold: 0.1 });
  return viewStartTimes;
}
function setupResizeObserver(grid) {
  if (resizeObserver) resizeObserver.disconnect();
  resizeObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const panelEl = entry.target.closest('.panel');
      if (!panelEl) continue;
      const panelId = panelEl.getAttribute('data-panel-id');
      if (!panelId) continue;
      const def = PANEL_DEFS.find(d => d.id === panelId);
      if (!def) continue;
      if (panelEl.classList.contains('compact')) {
        const sparkWrap = panelEl.querySelector('.mini-spark');
        if (sparkWrap) {
          const sparkData = getSparklineData(panelId, 20);
          requestAnimationFrame(() => renderSparkline(sparkWrap, sparkData, def.dotColor, 28, sparkWrap.clientWidth));
        }
      } else if (def.type === 'spark') {
        const sparkWrap = panelEl.querySelector('.sparkline-svg');
        if (sparkWrap) {
          const sparkData = getSparklineData(panelId, 24);
          requestAnimationFrame(() => renderSparkline(sparkWrap, sparkData, def.dotColor, 60, sparkWrap.clientWidth || 250));
        }
      }
    }
  });
  return resizeObserver;
}
let viewStartTimes = null;
let scoreTickInterval = null;
let rankInterval = null;
function init() {
  const grid = document.getElementById('grid');
  const saved = loadState();
  tracking = saved.tracking || {};
  layoutOrder = saved.layoutOrder || PANEL_DEFS.map(d => d.id);
  lockedPanels = new Set(saved.lockedPanels || []);
  manualPositions = saved.manualPositions || {};
  rankScores = saved.rankScores || {};
  if (layoutOrder.length !== PANEL_DEFS.length || !PANEL_DEFS.every(d => layoutOrder.includes(d.id))) {
    layoutOrder = PANEL_DEFS.map(d => d.id);
  }
  viewStartTimes = setupIntersectionObserver();
  resizeObserver = setupResizeObserver(grid);
  grid.addEventListener('click', handleGridClick);
  grid.addEventListener('dragstart', handleGridDragStart);
  grid.addEventListener('dragover', handleGridDragOver);
  grid.addEventListener('drop', handleGridDrop);
  grid.addEventListener('dragend', handleGridDragEnd);
  PANEL_DEFS.forEach(def => {
    if (!tracking[def.id]) {
      tracking[def.id] = { interactionCount: 0, viewDurationMs: 0, lastViewed: 0, lastInteraction: 0, expandCount: 0, collapseCount: 0 };
    }
  });
  rankPanels();
  reconcileDOM(grid, true);
  grid.querySelectorAll('.panel').forEach(el => {
    intersectionObserver.observe(el);
    resizeObserver.observe(el);
  });
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      mutation.addedNodes.forEach(node => {
        if (node.nodeType === 1 && node.classList.contains('panel')) {
          intersectionObserver.observe(node);
          resizeObserver.observe(node);
        }
      });
    });
  });
  observer.observe(grid, { childList: true });
  scoreTickInterval = setInterval(() => {
    const gridEl = document.getElementById('grid');
    const allPanels = gridEl.querySelectorAll('.panel');
    allPanels.forEach(panelEl => {
      const panelId = panelEl.getAttribute('data-panel-id');
      const def = PANEL_DEFS.find(d => d.id === panelId);
      if (!def) return;
      if (panelEl.classList.contains('compact')) {
        const statEl = panelEl.querySelector('.mini-stat');
        if (statEl) {
          const val = getMetricValue(panelId);
          const newText = def.unit ? `${Math.round(val)}${def.unit}` : `${Math.round(val)}`;
          if (statEl.textContent !== newText) statEl.textContent = newText;
        }
      } else {
        const bodyEl = panelEl.querySelector('[data-panel-body]');
        if (!bodyEl) return;
        const metricEl = bodyEl.querySelector('.metric-value');
        const val = getMetricValue(panelId);
        if (metricEl) {
          const newText = def.unit ? `${Math.round(val)}` : `${Math.round(val)}`;
          if (metricEl.textContent !== newText) metricEl.textContent = newText;
        }
        const gaugeWrap = bodyEl.querySelector('.gauge-svg')?.parentElement;
        if (gaugeWrap && def.type === 'gauge') {
          const svg = gaugeWrap.querySelector('svg');
          if (svg) {
            const fg = svg.querySelector('circle[stroke-dasharray]');
            if (fg) {
              const pct = Math.min(100, Math.max(0, (val / def.target) * 100));
              const size = 100; const strokeW = 8;
              const r = (size - strokeW) / 2;
              const circ = 2 * Math.PI * r;
              fg.setAttribute('stroke-dashoffset', circ * (1 - pct / 100));
            }
            const textEl = svg.querySelector('text');
            if (textEl) textEl.textContent = Math.round(val);
          }
        }
        const barFill = bodyEl.querySelector('.bar-fill');
        if (barFill && (def.type === 'bar' || def.type === 'histogram')) {
          const pct = Math.min(100, Math.max(0, (val / def.target) * 100));
          barFill.style.width = `${pct}%`;
        }
        const sparkWrap = bodyEl.querySelector('.sparkline-svg');
        if (sparkWrap && def.type === 'spark') {
          const sparkData = getSparklineData(panelId, 24);
          renderSparkline(sparkWrap, sparkData, def.dotColor, 60, sparkWrap.clientWidth || 250);
        }
      }
    });
  }, 30000);
  rankInterval = setInterval(() => {
    const changed = rankPanels();
    if (changed) {
      reconcileDOM(document.getElementById('grid'), true);
    }
  }, RANK_INTERVAL);
  document.getElementById('btn-reset-layout').addEventListener('click', () => {
    lockedPanels.clear();
    manualPositions = {};
    layoutOrder = PANEL_DEFS.map(d => d.id);
    rankPanels();
    saveState({ lockedPanels: [], manualPositions: {}, tracking, layoutOrder });
    reconcileDOM(grid, true);
    showToast('Layout reset — all panels unlocked');
  });
  document.getElementById('btn-export').addEventListener('click', () => {
    const data = {
      tracking,
      rankScores,
      layoutOrder,
      lockedPanels: [...lockedPanels],
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dashboard-tracking-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Tracking data exported');
  });
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
})();
</script>
</body>
</html>