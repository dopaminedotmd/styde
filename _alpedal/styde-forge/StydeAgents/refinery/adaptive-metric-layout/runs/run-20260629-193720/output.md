<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22263a;
  --border: #2a2e3f;
  --text: #e1e4ed;
  --text-secondary: #8b90a5;
  --accent: #6c8cff;
  --accent-dim: #4a5fb0;
  --danger: #ff6b6b;
  --success: #4ade80;
  --warning: #fbbf24;
  --compact-scale: 0.55;
  --transition-speed: 0.4s;
}
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 16px;
  line-height: 1.4;
}
.dashboard {
  max-width: 1440px;
  margin: 0 auto;
}
.controls {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.controls button {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}
.controls button:hover, .controls button:focus-visible {
  background: var(--surface-hover);
  color: var(--text);
  border-color: var(--accent);
  outline: none;
}
.controls button:active { transform: scale(0.97); }
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
  gap: 10px;
  transition: grid-template-columns var(--transition-speed) ease, gap var(--transition-speed) ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  cursor: default;
  transition: all var(--transition-speed) cubic-bezier(0.25, 0.1, 0.25, 1);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.panel:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.panel.locked {
  border-color: var(--warning);
}
.panel.locked::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 18px 18px 0;
  border-color: transparent var(--warning) transparent transparent;
}
.panel-large {
  grid-row: span 2;
  grid-column: span 2;
}
.panel-normal {
  grid-row: span 1;
  grid-column: span 1;
}
.panel-compact {
  grid-row: span 1;
  grid-column: span 1;
  transform: scale(var(--compact-scale));
  transform-origin: top left;
  margin-bottom: calc(-1 * (1 - var(--compact-scale)) * 100%);
  margin-right: calc(-1 * (1 - var(--compact-scale)) * 100%);
  opacity: 0.7;
  padding: 8px;
}
.panel-compact:hover, .panel-compact:focus-within {
  transform: scale(1);
  margin-bottom: 0;
  margin-right: 0;
  opacity: 1;
  z-index: 10;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-controls {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.panel-controls button {
  background: none;
  border: 1px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1;
  transition: all 0.15s;
}
.panel-controls button:hover, .panel-controls button:focus-visible {
  background: var(--surface-hover);
  border-color: var(--border);
  color: var(--text);
  outline: none;
}
.lock-btn.locked { color: var(--warning); }
.panel-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 0;
}
.metric-value {
  font-size: 28px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: -1px;
  margin-bottom: 6px;
}
.metric-label {
  font-size: 12px;
  color: var(--text-secondary);
}
.metric-trend {
  font-size: 12px;
  font-weight: 600;
}
.metric-trend.up { color: var(--success); }
.metric-trend.down { color: var(--danger); }
.sparkline-container {
  flex: 1;
  min-height: 0;
  width: 100%;
  margin-top: 6px;
}
.sparkline-container svg {
  display: block;
  width: 100%;
  height: 100%;
}
.rank-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 10px;
  font-weight: 700;
  color: var(--accent-dim);
  opacity: 0.5;
}
.overflow-section {
  margin-top: 12px;
}
.overflow-section summary {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 16px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 13px;
  transition: all 0.15s;
}
.overflow-section summary:hover { background: var(--surface-hover); color: var(--text); }
.overflow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin-top: 10px;
}
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
  font-size: 15px;
}
.skeleton {
  background: linear-gradient(90deg, var(--surface) 25%, var(--surface-hover) 50%, var(--surface) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@media (max-width: 768px) {
  .grid-container { grid-template-columns: repeat(2, 1fr); }
  .panel-large { grid-column: span 2; grid-row: span 1; }
}
</style>
</head>
<body>
<div id="dashboard" class="dashboard" role="region" aria-label="Adaptive Metric Dashboard">
  <div class="controls" role="toolbar" aria-label="Dashboard controls">
    <button id="reset-btn" type="button">Reset all tracking data</button>
    <button id="freeze-btn" type="button">Freeze layout (lock all)</button>
    <span id="last-update" style="font-size:12px;color:var(--text-secondary);align-self:center;margin-left:auto;"></span>
  </div>
  <div id="grid" class="grid-container" role="list" aria-label="Metric panels"></div>
  <details id="overflow-section" class="overflow-section" style="display:none;">
    <summary>More panels (<span id="overflow-count">0</span>)</summary>
    <div id="overflow-grid" class="overflow-grid"></div>
  </details>
</div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const RANK_RECALC_MS = 30000;
const METRIC_UPDATE_MS = 5000;
const VIEW_TRACK_MS = 2000;
const DECAY_HALF_LIFE_HOURS = 48;
const MAX_PANELS_VISIBLE = 8;
const LARGE_SLOTS = 2;
const OVERFLOW_THRESHOLD = 8;
const PANEL_DEFS = [
  { id: 'revenue', title: 'Revenue', unit: '$', fmt: v => '$' + v.toLocaleString(), trend: 1 },
  { id: 'users', title: 'Active Users', unit: '', fmt: v => v.toLocaleString(), trend: 1 },
  { id: 'conversion', title: 'Conversion', unit: '%', fmt: v => v.toFixed(2) + '%', trend: -1 },
  { id: 'latency', title: 'P95 Latency', unit: 'ms', fmt: v => v.toFixed(0) + 'ms', trend: 1 },
  { id: 'errors', title: 'Error Rate', unit: '%', fmt: v => v.toFixed(3) + '%', trend: 1 },
  { id: 'cpu', title: 'CPU Usage', unit: '%', fmt: v => v.toFixed(1) + '%', trend: 1 },
  { id: 'memory', title: 'Memory', unit: 'GB', fmt: v => v.toFixed(1) + 'GB', trend: 1 },
  { id: 'throughput', title: 'Throughput', unit: '/s', fmt: v => v.toFixed(0) + '/s', trend: -1 },
  { id: 'disk', title: 'Disk IO', unit: 'MB/s', fmt: v => v.toFixed(1) + 'MB/s', trend: -1 },
  { id: 'cache', title: 'Cache Hit Rate', unit: '%', fmt: v => v.toFixed(1) + '%', trend: -1 },
  { id: 'queue', title: 'Queue Depth', unit: '', fmt: v => v.toFixed(0), trend: 1 },
  { id: 'sessions', title: 'Sessions', unit: '', fmt: v => v.toLocaleString(), trend: -1 },
];
function createInitialMetrics() {
  const m = {};
  const now = Date.now();
  PANEL_DEFS.forEach(def => {
    const base = def.id === 'revenue' ? 50000 : def.id === 'users' ? 12000 : def.id === 'conversion' ? 3.5 : def.id === 'latency' ? 120 : def.id === 'errors' ? 0.05 : def.id === 'cpu' ? 45 : def.id === 'memory' ? 7.2 : def.id === 'throughput' ? 850 : def.id === 'disk' ? 120 : def.id === 'cache' ? 94 : def.id === 'queue' ? 23 : 4200;
    const history = [];
    for (let i = 29; i >= 0; i--) {
      const noise = (Math.random() - 0.5) * base * 0.15;
      history.push({ ts: now - i * 5000, val: Math.max(0, base + noise) });
    }
    m[def.id] = { current: history[history.length - 1].val, history };
  });
  return m;
}
function createInitialTracking() {
  const t = {};
  PANEL_DEFS.forEach(def => {
    t[def.id] = { frequency: 0, totalDurationMs: 0, lastInteraction: null, lastViewStart: null };
  });
  return t;
}
const state = {
  metrics: createInitialMetrics(),
  tracking: createInitialTracking(),
  lockedPanels: {},
  manualOrder: [],
  lastWrittenTracking: '',
  lastRankCalc: 0,
  frozen: false,
};
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const saved = JSON.parse(raw);
    if (saved.tracking) {
      for (const [id, t] of Object.entries(saved.tracking)) {
        if (state.tracking[id]) Object.assign(state.tracking[id], t);
      }
    }
    if (saved.lockedPanels) state.lockedPanels = saved.lockedPanels;
    if (saved.manualOrder) state.manualOrder = saved.manualOrder;
    if (saved.metrics) {
      for (const [id, m] of Object.entries(saved.metrics)) {
        if (state.metrics[id]) state.metrics[id] = m;
      }
    }
    state.lastWrittenTracking = JSON.stringify(state.tracking);
  } catch (e) { /* ignore corrupt storage */ }
}
function persistIfChanged() {
  const trackingJson = JSON.stringify(state.tracking);
  if (trackingJson === state.lastWrittenTracking) return;
  state.lastWrittenTracking = trackingJson;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      tracking: state.tracking,
      lockedPanels: state.lockedPanels,
      manualOrder: state.manualOrder,
      metrics: state.metrics,
    }));
  } catch (e) { /* quota exceeded - silently skip */ }
}
function computeScore(panelId) {
  const t = state.tracking[panelId];
  if (!t) return 0;
  const freq = t.frequency;
  const durSec = t.totalDurationMs / 1000;
  const baseScore = (freq * 10) + durSec;
  if (baseScore === 0) return 0;
  const hoursSince = t.lastInteraction ? (Date.now() - t.lastInteraction) / 3600000 : 999;
  const recency = Math.max(0.05, Math.pow(2, -hoursSince / DECAY_HALF_LIFE_HOURS));
  return baseScore * recency;
}
function rankPanels() {
  const now = Date.now();
  if (now - state.lastRankCalc < RANK_RECALC_MS) return;
  state.lastRankCalc = now;
  const scored = PANEL_DEFS.map(def => ({
    id: def.id,
    score: computeScore(def.id),
  }));
  scored.sort((a, b) => b.score - a.score);
  const lockedOrder = Object.entries(state.lockedPanels)
    .filter(([, locked]) => locked)
    .map(([id]) => id);
  const unlocked = scored
    .map(s => s.id)
    .filter(id => !lockedOrder.includes(id));
  const manualUnlocked = state.manualOrder.filter(id => !lockedOrder.includes(id) && unlocked.includes(id));
  const remainingUnlocked = unlocked.filter(id => !manualUnlocked.includes(id));
  const newOrder = [
    ...lockedOrder,
    ...manualUnlocked,
    ...remainingUnlocked,
  ];
  const prevOrderKey = (state._lastOrder || []).join(',');
  const newOrderKey = newOrder.join(',');
  if (prevOrderKey === newOrderKey) return;
  state._lastOrder = newOrder;
  applyLayout(newOrder, scored);
}
function applyLayout(order, scored) {
  const grid = document.getElementById('grid');
  const overflowSection = document.getElementById('overflow-section');
  const overflowGrid = document.getElementById('overflow-grid');
  const overflowCountEl = document.getElementById('overflow-count');
  const existingPanels = {};
  grid.querySelectorAll('.panel').forEach(p => { existingPanels[p.dataset.panelId] = p; });
  overflowGrid.querySelectorAll('.panel').forEach(p => { existingPanels[p.dataset.panelId] = p; });
  const visibleIds = order.slice(0, MAX_PANELS_VISIBLE);
  const overflowIds = order.slice(MAX_PANELS_VISIBLE);
  const scoreMap = {};
  scored.forEach(s => { scoreMap[s.id] = s.score; });
  function getSizeClass(idxInVisible) {
    if (idxInVisible < LARGE_SLOTS) return 'panel-large';
    if (idxInVisible < MAX_PANELS_VISIBLE - 2) return 'panel-normal';
    return 'panel-compact';
  }
  let domChanged = false;
  visibleIds.forEach((id, idx) => {
    let panel = existingPanels[id];
    if (!panel) {
      panel = createPanelElement(id, scoreMap[id] || 0);
      domChanged = true;
    }
    const sizeClass = getSizeClass(idx);
    const currentClasses = panel.className;
    const expectedBase = 'panel' + (state.lockedPanels[id] ? ' locked' : '') + (state.frozen ? ' locked' : '');
    const expectedClasses = expectedBase + ' ' + sizeClass;
    if (currentClasses !== expectedClasses) {
      panel.className = expectedClasses;
      domChanged = true;
    }
    if (panel.parentElement !== grid) {
      grid.appendChild(panel);
      domChanged = true;
    }
    const badge = panel.querySelector('.rank-badge');
    if (badge) badge.textContent = '#' + (idx + 1);
    updatePanelContent(panel, id);
  });
  overflowIds.forEach(id => {
    let panel = existingPanels[id];
    if (!panel) {
      panel = createPanelElement(id, scoreMap[id] || 0);
      domChanged = true;
    }
    panel.className = 'panel panel-compact' + (state.lockedPanels[id] ? ' locked' : '');
    if (panel.parentElement !== overflowGrid) {
      overflowGrid.appendChild(panel);
      domChanged = true;
    }
    const badge = panel.querySelector('.rank-badge');
    if (badge) badge.textContent = '';
    updatePanelContent(panel, id);
  });
  order.forEach(id => {
    if (!visibleIds.includes(id) && !overflowIds.includes(id)) {
      const panel = existingPanels[id];
      if (panel) { panel.remove(); domChanged = true; }
    }
  });
  if (overflowIds.length > 0) {
    if (overflowSection.style.display === 'none') domChanged = true;
    overflowSection.style.display = '';
    overflowCountEl.textContent = overflowIds.length;
  } else {
    if (overflowSection.style.display !== 'none') domChanged = true;
    overflowSection.style.display = 'none';
  }
  if (visibleIds.length === 0 && overflowIds.length === 0) {
    grid.innerHTML = '<div class="empty-state">No panels to display. Add metric panels to get started.</div>';
    domChanged = true;
  }
  if (domChanged) persistIfChanged();
}
function createPanelElement(id, score) {
  const def = PANEL_DEFS.find(d => d.id === id);
  if (!def) return document.createElement('div');
  const panel = document.createElement('div');
  panel.className = 'panel';
  panel.dataset.panelId = id;
  panel.setAttribute('role', 'region');
  panel.setAttribute('aria-label', def.title + ' panel');
  panel.setAttribute('tabindex', '0');
  panel.dataset.lastHash = '';
  panel.innerHTML =
    '<div class="panel-header">' +
      '<h3 class="panel-title">' + escapeHtml(def.title) + '</h3>' +
      '<div class="panel-controls">' +
        '<button class="lock-btn" type="button" aria-label="Lock ' + escapeHtml(def.title) + ' position">&#128274;</button>' +
        '<button class="expand-btn" type="button" aria-label="Move ' + escapeHtml(def.title) + ' to top">&#11014;</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' +
      '<div class="metric-value skeleton" style="height:32px;width:60%;"></div>' +
      '<div class="metric-label"></div>' +
      '<div class="metric-trend"></div>' +
      '<div class="sparkline-container"></div>' +
    '</div>' +
    '<span class="rank-badge"></span>';
  const lockBtn = panel.querySelector('.lock-btn');
  if (state.lockedPanels[id]) {
    lockBtn.classList.add('locked');
    lockBtn.innerHTML = '&#128274;';
  }
  if (state.frozen) {
    lockBtn.classList.add('locked');
    lockBtn.innerHTML = '&#128274;';
    panel.classList.add('locked');
  }
  return panel;
}
function updatePanelContent(panel, id) {
  const metric = state.metrics[id];
  if (!metric) return;
  const def = PANEL_DEFS.find(d => d.id === id);
  if (!def) return;
  const valEl = panel.querySelector('.metric-value');
  const labelEl = panel.querySelector('.metric-label');
  const trendEl = panel.querySelector('.metric-trend');
  const sparklineContainer = panel.querySelector('.sparkline-container');
  if (valEl) {
    valEl.classList.remove('skeleton');
    valEl.textContent = def.fmt(metric.current);
  }
  if (labelEl) {
    labelEl.textContent = def.unit ? 'in ' + def.unit : '';
  }
  if (trendEl && metric.history.length >= 2) {
    const prev = metric.history[metric.history.length - 2].val;
    const curr = metric.current;
    const pct = prev > 0 ? ((curr - prev) / prev) * 100 : 0;
    trendEl.textContent = (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%';
    trendEl.className = 'metric-trend ' + (pct >= 0 ? 'up' : 'down');
  }
  if (sparklineContainer) {
    const hash = computeHistoryHash(metric.history);
    if (panel.dataset.lastHash !== hash) {
      panel.dataset.lastHash = hash;
      sparklineContainer.innerHTML = '';
      sparklineContainer.appendChild(buildSparkline(metric.history));
    }
  }
}
function computeHistoryHash(history) {
  if (!history || history.length === 0) return 'empty';
  let h = history.length.toString(36);
  for (let i = history.length - 1; i >= Math.max(0, history.length - 10); i--) {
    h += ':' + Math.round(history[i].val * 100).toString(36);
  }
  return h;
}
function buildSparkline(history) {
  if (!history || history.length < 2) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 200 40');
    return svg;
  }
  const vals = history.map(h => h.val);
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const range = max - min || 1;
  const w = 200, h = 40, pad = 2;
  const points = vals.map((v, i) => {
    const x = pad + (i / (vals.length - 1)) * (w - 2 * pad);
    const y = h - pad - ((v - min) / range) * (h - 2 * pad);
    return x.toFixed(1) + ',' + y.toFixed(1);
  });
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', 'Sparkline chart');
  const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
  polyline.setAttribute('points', points.join(' '));
  polyline.setAttribute('fill', 'none');
  polyline.setAttribute('stroke', '#6c8cff');
  polyline.setAttribute('stroke-width', '1.5');
  polyline.setAttribute('stroke-linecap', 'round');
  polyline.setAttribute('stroke-linejoin', 'round');
  svg.appendChild(polyline);
  if (vals.length > 4) {
    const lastX = pad + (vals.length - 1) / (vals.length - 1) * (w - 2 * pad);
    const lastY = h - pad - ((vals[vals.length - 1] - min) / range) * (h - 2 * pad);
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', lastX.toFixed(1));
    circle.setAttribute('cy', lastY.toFixed(1));
    circle.setAttribute('r', '2');
    circle.setAttribute('fill', '#6c8cff');
    svg.appendChild(circle);
  }
  return svg;
}
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
function updateMetrics() {
  const now = Date.now();
  let changed = false;
  PANEL_DEFS.forEach(def => {
    const m = state.metrics[def.id];
    if (!m) return;
    const noise = (Math.random() - 0.5) * m.current * 0.05;
    m.current = Math.max(0, m.current + noise);
    m.history.push({ ts: now, val: m.current });
    if (m.history.length > 60) m.history.shift();
    changed = true;
  });
  if (!changed) return;
  const grid = document.getElementById('grid');
  const overflowGrid = document.getElementById('overflow-grid');
  const panels = [
    ...grid.querySelectorAll('.panel'),
    ...overflowGrid.querySelectorAll('.panel'),
  ];
  panels.forEach(panel => {
    updatePanelContent(panel, panel.dataset.panelId);
  });
  const lastUpdateEl = document.getElementById('last-update');
  if (lastUpdateEl) {
    lastUpdateEl.textContent = 'Updated ' + new Date().toLocaleTimeString();
  }
}
function recordEvent(panelId, type) {
  if (!state.tracking[panelId]) return;
  const t = state.tracking[panelId];
  const now = Date.now();
  switch (type) {
    case 'click':
    case 'expand':
    case 'collapse':
      t.frequency++;
      t.lastInteraction = now;
      break;
    case 'view_start':
      t.lastViewStart = now;
      break;
    case 'view_end':
      if (t.lastViewStart) {
        t.totalDurationMs += now - t.lastViewStart;
        t.lastViewStart = null;
      }
      break;
  }
  state.lastRankCalc = 0;
}
function setupDelegatedEvents() {
  const dashboard = document.getElementById('dashboard');
  dashboard.addEventListener('click', function(e) {
    const btn = e.target.closest('button');
    if (!btn) return;
    const panel = btn.closest('.panel');
    const panelId = panel ? panel.dataset.panelId : null;
    if (btn.classList.contains('lock-btn') && panelId) {
      e.stopPropagation();
      if (state.frozen) return;
      state.lockedPanels[panelId] = !state.lockedPanels[panelId];
      btn.classList.toggle('locked', state.lockedPanels[panelId]);
      if (state.lockedPanels[panelId]) {
        btn.innerHTML = '&#128274;';
        panel.classList.add('locked');
        recordEvent(panelId, 'expand');
      } else {
        btn.innerHTML = '&#128275;';
        panel.classList.remove('locked');
        recordEvent(panelId, 'collapse');
      }
      state.lastRankCalc = 0;
      rankPanels();
      persistIfChanged();
      return;
    }
    if (btn.classList.contains('expand-btn') && panelId) {
      e.stopPropagation();
      if (state.frozen) return;
      state.manualOrder = [panelId, ...state.manualOrder.filter(id => id !== panelId && !state.lockedPanels[id])];
      state.lastRankCalc = 0;
      recordEvent(panelId, 'expand');
      rankPanels();
      persistIfChanged();
      return;
    }
    if (btn.id === 'reset-btn') {
      state.tracking = createInitialTracking();
      state.lastRankCalc = 0;
      state.lastWrittenTracking = '';
      state.manualOrder = [];
      rankPanels();
      persistIfChanged();
      return;
    }
    if (btn.id === 'freeze-btn') {
      state.frozen = !state.frozen;
      if (state.frozen) {
        btn.textContent = 'Unfreeze layout';
        PANEL_DEFS.forEach(def => { state.lockedPanels[def.id] = true; });
      } else {
        btn.textContent = 'Freeze layout (lock all)';
        PANEL_DEFS.forEach(def => { delete state.lockedPanels[def.id]; });
      }
      state.lastRankCalc = 0;
      rankPanels();
      persistIfChanged();
      return;
    }
  });
  dashboard.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      const panel = e.target.closest('.panel');
      if (panel && !e.target.closest('button')) {
        e.preventDefault();
        recordEvent(panel.dataset.panelId, 'click');
      }
    }
  });
}
function setupViewTracking() {
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      if (entry.isIntersecting) {
        recordEvent(panelId, 'view_start');
      } else {
        recordEvent(panelId, 'view_end');
      }
    });
  }, { threshold: 0.3 });
  function observePanels() {
    const grid = document.getElementById('grid');
    const overflowGrid = document.getElementById('overflow-grid');
    const panels = [
      ...grid.querySelectorAll('.panel'),
      ...overflowGrid.querySelectorAll('.panel'),
    ];
    panels.forEach(panel => {
      if (!panel.dataset.observed) {
        observer.observe(panel);
        panel.dataset.observed = '1';
      }
    });
  }
  const mutationObserver = new MutationObserver(function() {
    observePanels();
    persistIfChanged();
  });
  mutationObserver.observe(document.getElementById('grid'), { childList: true, subtree: true });
  mutationObserver.observe(document.getElementById('overflow-grid'), { childList: true, subtree: true });
  observePanels();
}
function init() {
  loadState();
  setupDelegatedEvents();
  rankPanels();
  setupViewTracking();
  if (Object.keys(state.tracking).every(k => state.tracking[k].frequency === 0 && state.tracking[k].totalDurationMs === 0)) {
    PANEL_DEFS.slice(0, 3).forEach(def => {
      state.tracking[def.id].frequency = Math.floor(Math.random() * 5) + 1;
      state.tracking[def.id].totalDurationMs = Math.floor(Math.random() * 60000) + 10000;
      state.tracking[def.id].lastInteraction = Date.now() - Math.floor(Math.random() * 3600000);
    });
  }
  setTimeout(() => {
    state.lastRankCalc = 0;
    rankPanels();
  }, 500);
  setInterval(function() {
    updateMetrics();
  }, METRIC_UPDATE_MS);
  setInterval(function() {
    state.lastRankCalc = 0;
    rankPanels();
    persistIfChanged();
  }, RANK_RECALC_MS);
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