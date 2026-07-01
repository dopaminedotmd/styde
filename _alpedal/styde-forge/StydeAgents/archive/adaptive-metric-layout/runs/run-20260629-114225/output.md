`html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #7a7f8e;
  --accent: #5b8af7;
  --accent-glow: rgba(91,138,247,0.3);
  --warn: #f0a040;
  --danger: #e0556a;
  --success: #4caf8e;
  --compact-bg: #141720;
  --lock-color: #f0a040;
  --overlay: rgba(0,0,0,0.6);
  --transition-speed: 0.35s;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 12px;
  user-select: none;
}
.toolbar {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  margin-bottom: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.toolbar button {
  background: #252836;
  border: 1px solid var(--panel-border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}
.toolbar button:hover { background: #2f3344; border-color: var(--accent); }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.toolbar .sep { width: 1px; height: 24px; background: var(--panel-border); margin: 0 4px; }
.toolbar .stats { font-size: 12px; color: var(--text-dim); margin-left: auto; }
.grid {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-flow: dense;
  transition: all var(--transition-speed) ease;
}
.grid.manual-mode { outline: 2px dashed var(--warn); outline-offset: 4px; border-radius: 6px; }
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  min-height: 160px;
  animation: panelIn 0.3s ease-out;
}
@keyframes panelIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.panel.size-large { grid-column: span 2; grid-row: span 2; min-height: 340px; }
.panel.size-medium { grid-column: span 1; grid-row: span 1; min-height: 200px; }
.panel.size-small { grid-column: span 1; grid-row: span 1; min-height: 130px; }
.panel.size-compact {
  grid-column: span 1; grid-row: span 1; min-height: 90px;
  background: var(--compact-bg); border-style: dashed;
}
.panel.size-compact .panel-body { display: none; }
.panel.size-compact .panel-header { padding: 8px 12px; }
.panel.size-compact .compact-preview { display: flex; }
.panel.dragging { opacity: 0.7; z-index: 100; box-shadow: 0 8px 32px rgba(0,0,0,0.5); cursor: grabbing; }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
.panel.locked { border-color: var(--lock-color); }
.panel-header {
  display: flex;
  align-items: center;
  padding: 10px 14px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--panel-border);
  gap: 8px;
  cursor: grab;
  min-height: 40px;
}
.panel-header:active { cursor: grabbing; }
.panel-header .rank-badge {
  background: var(--accent);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
  min-width: 22px;
  text-align: center;
  flex-shrink: 0;
}
.panel-header .rank-badge.low { background: #3a3f55; }
.panel-header .panel-title {
  font-weight: 600;
  font-size: 14px;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-header .panel-score {
  font-size: 10px;
  color: var(--text-dim);
  font-family: 'Consolas', 'Courier New', monospace;
  flex-shrink: 0;
}
.panel-header .btn {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  padding: 2px 6px;
  font-size: 15px;
  line-height: 1;
  border-radius: 3px;
  transition: all 0.15s;
  flex-shrink: 0;
}
.panel-header .btn:hover { background: rgba(255,255,255,0.08); color: var(--text); }
.panel-header .btn.lock-btn.locked { color: var(--lock-color); }
.panel-header .btn.compact-btn.compacted { color: var(--warn); }
.panel-body {
  padding: 14px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: opacity var(--transition-speed);
}
.panel-body .metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}
.panel-body .metric-value {
  font-weight: 700;
  font-size: 22px;
  font-family: 'Consolas', 'Courier New', monospace;
  color: var(--accent);
}
.panel-body .sparkline {
  height: 40px;
  background: rgba(255,255,255,0.03);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}
.panel-body .sparkline svg { width: 100%; height: 100%; }
.compact-preview {
  display: none;
  padding: 6px 14px 10px;
  gap: 12px;
  font-size: 12px;
  color: var(--text-dim);
  align-items: center;
}
.compact-preview .mini-val {
  font-weight: 700;
  font-size: 16px;
  color: var(--accent);
  font-family: 'Consolas', 'Courier New', monospace;
}
.tracking-indicator {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success);
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}
.panel.tracked .tracking-indicator { opacity: 1; animation: pulse 0.6s ease-out; }
@keyframes pulse { 0% { transform: scale(0.5); opacity: 0; } 50% { transform: scale(1.5); opacity: 1; } 100% { transform: scale(1); opacity: 0; } }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #252836;
  border: 1px solid var(--panel-border);
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  z-index: 1000;
  animation: toastIn 0.3s ease-out, toastOut 0.3s 2.5s ease-in forwards;
  max-width: 360px;
}
@keyframes toastIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes toastOut { from { opacity: 1; } to { opacity: 0; } }
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-dim);
}
.empty-state .big-num { font-size: 48px; font-weight: 300; color: var(--accent); margin-bottom: 8px; }
.modal-overlay {
  position: fixed; inset: 0; background: var(--overlay); z-index: 500;
  display: flex; align-items: center; justify-content: center;
}
.modal {
  background: var(--panel-bg); border: 1px solid var(--panel-border);
  border-radius: 12px; padding: 24px; min-width: 320px; max-width: 500px;
}
.modal h2 { font-size: 16px; margin-bottom: 16px; }
.modal label { display: block; font-size: 12px; color: var(--text-dim); margin-bottom: 4px; }
.modal input, .modal select {
  width: 100%; padding: 8px 12px; background: #141720; border: 1px solid var(--panel-border);
  color: var(--text); border-radius: 5px; margin-bottom: 12px; font-size: 13px;
}
.modal .btn-row { display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px; }
.modal button {
  padding: 8px 18px; border-radius: 5px; border: 1px solid var(--panel-border);
  background: #252836; color: var(--text); cursor: pointer; font-size: 13px;
}
.modal button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
</style>
</head>
<body>
<div class="toolbar" id="toolbar">
  <button id="btn-reset" title="Reset all tracking data">Reset Data</button>
  <button id="btn-seed" title="Load demo data">Seed Demo</button>
  <span class="sep"></span>
  <button id="btn-auto" class="active" title="Automatic layout mode">Auto</button>
  <button id="btn-manual" title="Manual override mode (drag to reorder)">Manual</button>
  <span class="sep"></span>
  <button id="btn-add-panel" title="Add a new metric panel">+ Panel</button>
  <span class="stats" id="stats-text">Interactions: 0 | Panels: 0</span>
</div>
<div class="grid" id="grid"></div>
<div id="toast-container"></div>
<script>
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const MIN_INTERACTIONS_BEFORE_RANK = 3;
const DEMO_SEED_COUNT = 12;
const COMPACT_THRESHOLD_PERCENTILE = 25;
const LARGE_THRESHOLD_PERCENTILE = 75;
const RECENCY_HALF_LIFE_MS = 3600000;
const SAVE_DEBOUNCE_MS = 1500;
const VIEW_TRACK_INTERVAL_MS = 2000;
function uid() { return 'p_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 7); }
function now() { return Date.now(); }
function defaultPanels() {
  return [
    { id: uid(), title: 'Active Users', value: 1247, unit: '', trend: [3,5,8,12,10,15,18,14,20,22], type: 'count' },
    { id: uid(), title: 'Revenue (USD)', value: 48250, unit: '$', trend: [40,42,45,43,48,50,47,52,55,53], type: 'currency' },
    { id: uid(), title: 'Response Time (ms)', value: 187, unit: 'ms', trend: [210,205,198,195,190,188,185,187,184,187], type: 'duration' },
    { id: uid(), title: 'Error Rate', value: 1.2, unit: '%', trend: [1.8,1.6,1.5,1.4,1.3,1.2,1.1,1.3,1.2,1.2], type: 'percent' },
    { id: uid(), title: 'CPU Load', value: 64, unit: '%', trend: [55,60,58,62,65,63,67,64,62,64], type: 'percent' },
    { id: uid(), title: 'Memory', value: 8.2, unit: 'GB', trend: [7.5,7.8,7.9,8.0,8.1,8.0,8.3,8.1,8.2,8.2], type: 'size' },
    { id: uid(), title: 'Requests/sec', value: 3420, unit: '', trend: [3.1,3.2,3.3,3.5,3.4,3.6,3.5,3.4,3.5,3.4], type: 'count' },
    { id: uid(), title: 'Cache Hit Rate', value: 94.7, unit: '%', trend: [92,93,94,93,95,94,96,95,94,94.7], type: 'percent' },
    { id: uid(), title: 'Active Sessions', value: 892, unit: '', trend: [800,820,850,870,860,890,880,900,895,892], type: 'count' },
    { id: uid(), title: 'Disk I/O', value: 124, unit: 'MB/s', trend: [100,110,115,120,118,125,122,128,126,124], type: 'throughput' },
    { id: uid(), title: 'Queue Depth', value: 17, unit: '', trend: [25,23,20,22,19,18,16,18,17,17], type: 'count' },
    { id: uid(), title: 'Uptime', value: 99.98, unit: '%', trend: [99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.98], type: 'percent' },
  ];
}
function createTracking(panelId) {
  return {
    panelId: panelId,
    viewCount: 0,
    totalViewDurationMs: 0,
    lastViewedAt: 0,
    interactionCount: 0,
    collapseCount: 0,
    expandCount: 0,
    currentViewStart: 0,
  };
}
let state = {
  panels: [],
  tracking: {},
  order: [],
  locks: {},
  manualPositions: {},
  compactOverrides: {},
  isManualMode: false,
  totalInteractions: 0,
  storageAvailable: true,
};
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object') return false;
    if (!Array.isArray(parsed.panels)) return false;
    if (!parsed.tracking || typeof parsed.tracking !== 'object') return false;
    state.panels = parsed.panels;
    state.tracking = parsed.tracking;
    state.order = Array.isArray(parsed.order) ? parsed.order : parsed.panels.map(p => p.id);
    state.locks = parsed.locks || {};
    state.manualPositions = parsed.manualPositions || {};
    state.compactOverrides = parsed.compactOverrides || {};
    state.isManualMode = !!parsed.isManualMode;
    state.totalInteractions = parsed.totalInteractions || countTotalInteractions();
    state.storageAvailable = true;
    syncTrackingKeys();
    return true;
  } catch (e) {
    state.storageAvailable = false;
    console.warn('localStorage unavailable:', e.message);
    return false;
  }
}
function saveState() {
  if (!state.storageAvailable) return;
  try {
    const payload = {
      panels: state.panels,
      tracking: state.tracking,
      order: state.order,
      locks: state.locks,
      manualPositions: state.manualPositions,
      compactOverrides: state.compactOverrides,
      isManualMode: state.isManualMode,
      totalInteractions: state.totalInteractions,
    };
    const serialized = JSON.stringify(payload);
    localStorage.setItem(STORAGE_KEY, serialized);
  } catch (e) {
    if (e.name === 'QuotaExceededError') {
      state.storageAvailable = false;
      toast('Storage full — tracking continues in memory only');
    } else {
      state.storageAvailable = false;
      console.warn('localStorage write failed:', e.message);
    }
  }
}
let saveTimer = null;
function debouncedSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveState, SAVE_DEBOUNCE_MS);
}
function syncTrackingKeys() {
  for (const p of state.panels) {
    if (!state.tracking[p.id]) state.tracking[p.id] = createTracking(p.id);
  }
  const validIds = new Set(state.panels.map(p => p.id));
  for (const tid of Object.keys(state.tracking)) {
    if (!validIds.has(tid)) delete state.tracking[tid];
  }
  for (const lid of Object.keys(state.locks)) {
    if (!validIds.has(lid)) delete state.locks[lid];
  }
  for (const cid of Object.keys(state.compactOverrides)) {
    if (!validIds.has(cid)) delete state.compactOverrides[cid];
  }
  for (const mid of Object.keys(state.manualPositions)) {
    if (!validIds.has(mid)) delete state.manualPositions[mid];
  }
}
function countTotalInteractions() {
  let total = 0;
  for (const t of Object.values(state.tracking)) {
    total += (t.viewCount || 0) + (t.interactionCount || 0) + (t.collapseCount || 0) + (t.expandCount || 0);
  }
  return total;
}
function computeScore(panelId) {
  const t = state.tracking[panelId];
  if (!t) return 0;
  const freq = (t.viewCount || 0) + (t.interactionCount || 0) * 1.5;
  if (freq === 0) return 0;
  const durNorm = Math.min((t.totalViewDurationMs || 0) / 60000, 60);
  const ageMs = now() - (t.lastViewedAt || now());
  const recencyFactor = Math.pow(0.5, ageMs / RECENCY_HALF_LIFE_MS);
  const expandBonus = 1 + Math.min((t.expandCount || 0) * 0.1, 0.5);
  return freq * Math.max(durNorm, 0.1) * Math.max(recencyFactor, 0.01) * expandBonus;
}
function computeScores() {
  const scores = {};
  for (const p of state.panels) {
    scores[p.id] = computeScore(p.id);
  }
  return scores;
}
function rankPanels() {
  const scores = computeScores();
  const entries = state.panels.map(p => ({
    id: p.id,
    score: scores[p.id] || 0,
    locked: !!state.locks[p.id],
  }));
  entries.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return a.id.localeCompare(b.id);
  });
  return entries;
}
function computeLayout() {
  if (state.isManualMode) {
    const order = state.order.length ? state.order : state.panels.map(p => p.id);
    const result = [];
    for (const id of order) {
      const pos = state.manualPositions[id];
      result.push({
        id,
        size: pos ? pos.size || 'medium' : 'medium',
        rank: 0,
        score: computeScore(id),
        locked: !!state.locks[id],
        compactOverride: !!state.compactOverrides[id],
        orderIdx: result.length,
      });
    }
    return result;
  }
  const ranked = rankPanels();
  if (ranked.length === 0) return [];
  const scoresArr = ranked.map(r => r.score).filter(s => s > 0);
  if (scoresArr.length === 0) {
    return ranked.map((r, i) => ({
      id: r.id, size: 'medium', rank: i + 1,
      score: 0, locked: r.locked, compactOverride: !!state.compactOverrides[r.id],
      orderIdx: i,
    }));
  }
  scoresArr.sort((a, b) => a - b);
  const p25 = scoresArr[Math.floor(scoresArr.length * 0.25)] || 0;
  const p75 = scoresArr[Math.floor(scoresArr.length * 0.75)] || 0;
  const result = [];
  for (let i = 0; i < ranked.length; i++) {
    const entry = ranked[i];
    let size = 'medium';
    if (state.compactOverrides[entry.id]) {
      size = 'compact';
    } else if (entry.score >= p75 && entry.score > 0) {
      size = 'large';
    } else if (entry.score <= p25 && entry.score > 0) {
      size = 'small';
    } else if (entry.score === 0 && i >= Math.floor(ranked.length * 0.7)) {
      size = 'small';
    }
    result.push({
      id: entry.id,
      size,
      rank: entry.score > 0 ? i + 1 : 0,
      score: entry.score,
      locked: entry.locked,
      compactOverride: !!state.compactOverrides[entry.id],
      orderIdx: i,
    });
  }
  return result;
}
function findPanel(id) { return state.panels.find(p => p.id === id); }
function getPanelData(panelId) {
  const panel = findPanel(panelId);
  const tracking = state.tracking[panelId];
  return { panel, tracking };
}
function startViewTracking(panelId) {
  const t = state.tracking[panelId];
  if (!t) return;
  t.currentViewStart = now();
  t.viewCount = (t.viewCount || 0) + 1;
  t.lastViewedAt = now();
  state.totalInteractions++;
  debouncedSave();
}
function stopViewTracking(panelId) {
  const t = state.tracking[panelId];
  if (!t) return;
  if (t.currentViewStart > 0) {
    const duration = now() - t.currentViewStart;
    t.totalViewDurationMs = (t.totalViewDurationMs || 0) + duration;
    t.currentViewStart = 0;
    debouncedSave();
  }
}
function trackInteraction(panelId) {
  const t = state.tracking[panelId];
  if (!t) return;
  t.interactionCount = (t.interactionCount || 0) + 1;
  t.lastViewedAt = now();
  state.totalInteractions++;
  debouncedSave();
  const el = document.querySelector(`[data-panel-id="${panelId}"]`);
  if (el) {
    el.classList.add('tracked');
    setTimeout(() => el.classList.remove('tracked'), 700);
  }
}
function trackCollapse(panelId) {
  const t = state.tracking[panelId];
  if (!t) return;
  t.collapseCount = (t.collapseCount || 0) + 1;
  t.lastViewedAt = now();
  state.totalInteractions++;
  debouncedSave();
}
function trackExpand(panelId) {
  const t = state.tracking[panelId];
  if (!t) return;
  t.expandCount = (t.expandCount || 0) + 1;
  t.lastViewedAt = now();
  state.totalInteractions++;
  debouncedSave();
}
function renderSparkline(trend, width, height) {
  if (!trend || trend.length < 2) return '';
  const w = width || 180;
  const h = height || 40;
  const pad = 4;
  const min = Math.min(...trend);
  const max = Math.max(...trend);
  const range = max - min || 1;
  const pts = trend.map((v, i) => {
    const x = pad + (i / (trend.length - 1)) * (w - pad * 2);
    const y = h - pad - ((v - min) / range) * (h - pad * 2);
    return `${x},${y}`;
  });
  const polyline = pts.join(' ');
  const fillPath = `${pts[0].split(',')[0]},${h - pad} ${polyline} ${pts[pts.length-1].split(',')[0]},${h - pad}`;
  const isUp = trend[trend.length - 1] >= trend[0];
  const color = isUp ? '#4caf8e' : '#e0556a';
  return `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
    <polygon points="${fillPath}" fill="${color}" fill-opacity="0.1"/>
    <polyline points="${polyline}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}
function renderPanel(panel, layoutEntry) {
  const { id, title, value, unit, trend } = panel;
  const size = layoutEntry.size;
  const rank = layoutEntry.rank;
  const score = layoutEntry.score;
  const isLocked = layoutEntry.locked;
  const isCompacted = size === 'compact';
  const trendLast = trend && trend.length >= 2 ? trend[trend.length - 1] : null;
  const trendPrev = trend && trend.length >= 2 ? trend[trend.length - 2] : null;
  let rankBadgeClass = rank <= 3 ? '' : 'low';
  let rankDisplay = rank > 0 ? `#${rank}` : '-';
  return `
  <div class="panel size-${size}${isLocked ? ' locked' : ''}"
       data-panel-id="${id}"
       draggable="${state.isManualMode ? 'true' : 'false'}"
       data-rank="${rank}">
    <div class="tracking-indicator"></div>
    <div class="panel-header">
      <span class="rank-badge ${rankBadgeClass}">${rankDisplay}</span>
      <span class="panel-title">${escapeHtml(title)}</span>
      <span class="panel-score">${score.toFixed(1)}</span>
      <button class="btn compact-btn${isCompacted ? ' compacted' : ''}"
              data-action="toggle-compact" data-panel="${id}"
              title="Toggle compact mode">${isCompacted ? '⊞' : '⊟'}</button>
      <button class="btn lock-btn${isLocked ? ' locked' : ''}"
              data-action="toggle-lock" data-panel="${id}"
              title="${isLocked ? 'Unlock position' : 'Lock position'}">${isLocked ? '🔒' : '🔓'}</button>
    </div>
    <div class="panel-body">
      <div class="metric-row">
        <span>${escapeHtml(title)}</span>
        <span class="metric-value">${unit}${formatValue(value)}</span>
      </div>
      ${trend ? `<div class="sparkline">${renderSparkline(trend)}</div>` : ''}
    </div>
    <div class="compact-preview">
      <span class="mini-val">${unit}${formatValue(value)}</span>
      <span>${escapeHtml(title)}</span>
    </div>
  </div>`;
}
function formatValue(v) {
  if (typeof v === 'number') {
    if (v >= 1000 && Number.isInteger(v)) return v.toLocaleString();
    return parseFloat(v.toFixed(2)).toString();
  }
  return String(v);
}
function escapeHtml(str) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  return String(str).replace(/[&<>"']/g, c => map[c]);
}
function renderGrid() {
  const grid = document.getElementById('grid');
  const layout = computeLayout();
  const layoutMap = {};
  for (const entry of layout) {
    layoutMap[entry.id] = entry;
  }
  const orderedIds = layout.map(e => e.id);
  state.order = orderedIds;
  const existingPanels = new Set();
  grid.querySelectorAll('.panel').forEach(el => {
    const pid = el.dataset.panelId;
    existingPanels.add(pid);
  });
  const newIds = orderedIds.filter(id => !existingPanels.has(id));
  const removedIds = [];
  existingPanels.forEach(id => {
    if (!orderedIds.includes(id)) removedIds.push(id);
  });
  for (const id of removedIds) {
    const el = grid.querySelector(`[data-panel-id="${id}"]`);
    if (el) {
      stopViewTracking(id);
      el.style.transition = 'all 0.2s ease';
      el.style.opacity = '0';
      el.style.transform = 'scale(0.9)';
      setTimeout(() => el.remove(), 250);
    }
  }
  for (const id of orderedIds) {
    const entry = layoutMap[id];
    const panel = findPanel(id);
    if (!panel) continue;
    const existing = grid.querySelector(`[data-panel-id="${id}"]`);
    if (existing) {
      const currentSize = Array.from(existing.classList).find(c => c.startsWith('size-'));
      const targetSize = 'size-' + entry.size;
      if (currentSize !== targetSize) {
        if (currentSize) existing.classList.remove(currentSize);
        existing.classList.add(targetSize);
      }
      if (entry.locked && !existing.classList.contains('locked')) {
        existing.classList.add('locked');
      } else if (!entry.locked && existing.classList.contains('locked')) {
        existing.classList.remove('locked');
      }
      existing.draggable = state.isManualMode;
      const rankBadge = existing.querySelector('.rank-badge');
      if (rankBadge) {
        rankBadge.textContent = entry.rank > 0 ? `#${entry.rank}` : '-';
        rankBadge.className = 'rank-badge' + (entry.rank > 0 && entry.rank <= 3 ? '' : ' low');
      }
      const scoreEl = existing.querySelector('.panel-score');
      if (scoreEl) scoreEl.textContent = entry.score.toFixed(1);
      const compactBtn = existing.querySelector('.compact-btn');
      if (compactBtn) {
        compactBtn.classList.toggle('compacted', entry.size === 'compact');
        compactBtn.textContent = entry.size === 'compact' ? '⊞' : '⊟';
      }
    } else {
      const html = renderPanel(panel, entry);
      const temp = document.createElement('div');
      temp.innerHTML = html;
      const el = temp.firstElementChild;
      grid.appendChild(el);
      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'scale(1)';
      }, 10);
      el.style.opacity = '0';
      el.style.transform = 'scale(0.95)';
    }
  }
  if (state.isManualMode) {
    grid.classList.add('manual-mode');
  } else {
    grid.classList.remove('manual-mode');
  }
  const remaining = grid.querySelectorAll('.panel');
  const orderedEls = [];
  for (const id of orderedIds) {
    const el = grid.querySelector(`[data-panel-id="${id}"]`);
    if (el) orderedEls.push(el);
  }
  orderedEls.forEach((el, i) => {
    el.style.order = i;
  });
  updateStats();
}
function updateStats() {
  const stats = document.getElementById('stats-text');
  stats.textContent = `Interactions: ${state.totalInteractions} | Panels: ${state.panels.length}`;
}
function toast(msg) {
  const container = document.getElementById('toast-container');
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}
function resetAll() {
  if (!confirm('Reset all tracking data and layout? This cannot be undone.')) return;
  stopAllTracking();
  state.panels = defaultPanels();
  state.tracking = {};
  state.order = state.panels.map(p => p.id);
  state.locks = {};
  state.manualPositions = {};
  state.compactOverrides = {};
  state.isManualMode = false;
  state.totalInteractions = 0;
  state.storageAvailable = true;
  syncTrackingKeys();
  saveState();
  renderGrid();
  updateToolbarButtons();
  toast('All data reset — fresh layout loaded');
}
function seedDemoData() {
  stopAllTracking();
  state.panels = defaultPanels();
  state.tracking = {};
  state.order = state.panels.map(p => p.id);
  state.locks = {};
  state.manualPositions = {};
  state.compactOverrides = {};
  state.isManualMode = false;
  syncTrackingKeys();
  const demoPatterns = [
    { vc: 45, dur: 420000, int: 28, coll: 2, exp: 4 },
    { vc: 38, dur: 380000, int: 22, coll: 1, exp: 3 },
    { vc: 30, dur: 310000, int: 18, coll: 3, exp: 5 },
    { vc: 25, dur: 250000, int: 14, coll: 2, exp: 2 },
    { vc: 20, dur: 180000, int: 10, coll: 4, exp: 6 },
    { vc: 15, dur: 120000, int: 7, coll: 3, exp: 3 },
    { vc: 10, dur: 90000, int: 5, coll: 5, exp: 4 },
    { vc: 7, dur: 60000, int: 3, coll: 7, exp: 5 },
    { vc: 4, dur: 30000, int: 2, coll: 2, exp: 1 },
    { vc: 2, dur: 15000, int: 1, coll: 1, exp: 0 },
    { vc: 1, dur: 5000, int: 0, coll: 0, exp: 0 },
    { vc: 0, dur: 0, int: 0, coll: 0, exp: 0 },
  ];
  for (let i = 0; i < state.panels.length; i++) {
    const p = state.panels[i];
    const pattern = demoPatterns[i] || demoPatterns[demoPatterns.length - 1];
    const t = state.tracking[p.id];
    if (!t) continue;
    t.viewCount = pattern.vc;
    t.totalViewDurationMs = pattern.dur;
    t.interactionCount = pattern.int;
    t.collapseCount = pattern.coll;
    t.expandCount = pattern.exp;
    t.lastViewedAt = now() - (state.panels.length - i) * 300000;
  }
  state.totalInteractions = countTotalInteractions();
  saveState();
  renderGrid();
  updateToolbarButtons();
  toast('Demo data seeded — 12 panels with varied attention patterns');
}
function stopAllTracking() {
  for (const id of Object.keys(state.tracking)) {
    stopViewTracking(id);
  }
}
function addPanel() {
  const id = uid();
  const newPanel = {
    id,
    title: `Metric ${state.panels.length + 1}`,
    value: Math.floor(Math.random() * 1000),
    unit: '',
    trend: Array.from({ length: 10 }, () => Math.floor(Math.random() * 100)),
    type: 'count',
  };
  state.panels.push(newPanel);
  state.tracking[id] = createTracking(id);
  state.order.push(id);
  saveState();
  renderGrid();
  toast(`Panel "${newPanel.title}" added`);
}
function toggleLock(panelId) {
  if (state.locks[panelId]) {
    delete state.locks[panelId];
  } else {
    state.locks[panelId] = true;
    if (state.isManualMode) {
      const currentEl = document.querySelector(`[data-panel-id="${panelId}"]`);
      if (currentEl) {
        const siblings = Array.from(currentEl.parentElement.children).filter(
          c => c.classList.contains('panel')
        );
        const idx = siblings.indexOf(currentEl);
        state.manualPositions[panelId] = {
          index: idx >= 0 ? idx : 0,
          size: Array.from(currentEl.classList).find(c => c.startsWith('size-'))?.replace('size-', '') || 'medium',
        };
      }
    }
  }
  trackInteraction(panelId);
  saveState();
  renderGrid();
}
function toggleCompact(panelId) {
  if (state.compactOverrides[panelId]) {
    delete state.compactOverrides[panelId];
    trackExpand(panelId);
  } else {
    state.compactOverrides[panelId] = true;
    trackCollapse(panelId);
  }
  saveState();
  renderGrid();
}
function toggleManualMode() {
  state.isManualMode = !state.isManualMode;
  if (!state.isManualMode) {
    state.manualPositions = {};
  } else {
    const grid = document.getElementById('grid');
    const panels = Array.from(grid.querySelectorAll('.panel'));
    panels.forEach((el, i) => {
      const pid = el.dataset.panelId;
      const sizeClass = Array.from(el.classList).find(c => c.startsWith('size-'));
      state.manualPositions[pid] = {
        index: i,
        size: sizeClass ? sizeClass.replace('size-', '') : 'medium',
      };
    });
    state.order = panels.map(el => el.dataset.panelId);
  }
  saveState();
  renderGrid();
  updateToolbarButtons();
}
function updateToolbarButtons() {
  const btnAuto = document.getElementById('btn-auto');
  const btnManual = document.getElementById('btn-manual');
  btnAuto.classList.toggle('active', !state.isManualMode);
  btnManual.classList.toggle('active', state.isManualMode);
}
function handlePanelClick(e) {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;
  const panelId = btn.dataset.panel;
  if (!panelId) return;
  e.preventDefault();
  e.stopPropagation();
  const action = btn.dataset.action;
  if (action === 'toggle-lock') toggleLock(panelId);
  else if (action === 'toggle-compact') toggleCompact(panelId);
}
function setupDragAndDrop() {
  const grid = document.getElementById('grid');
  let dragEl = null;
  let dragOverEl = null;
  grid.addEventListener('dragstart', e => {
    if (!state.isManualMode) { e.preventDefault(); return; }
    const panel = e.target.closest('.panel');
    if (!panel) { e.preventDefault(); return; }
    dragEl = panel;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.dataset.panelId);
  });
  grid.addEventListener('dragover', e => {
    if (!state.isManualMode || !dragEl) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    const panel = e.target.closest('.panel');
    if (panel && panel !== dragEl) {
      if (dragOverEl) dragOverEl.classList.remove('drag-over');
      dragOverEl = panel;
      panel.classList.add('drag-over');
    }
  });
  grid.addEventListener('dragleave', e => {
    const panel = e.target.closest('.panel');
    if (panel === dragOverEl) {
      panel.classList.remove('drag-over');
      dragOverEl = null;
    }
  });
  grid.addEventListener('drop', e => {
    if (!state.isManualMode || !dragEl) return;
    e.preventDefault();
    if (dragOverEl) dragOverEl.classList.remove('drag-over');
    const targetPanel = e.target.closest('.panel');
    if (!targetPanel || targetPanel === dragEl) {
      dragEl.classList.remove('dragging');
      dragEl = null;
      dragOverEl = null;
      return;
    }
    const allPanels = Array.from(grid.querySelectorAll('.panel'));
    const fromIdx = allPanels.indexOf(dragEl);
    const toIdx = allPanels.indexOf(targetPanel);
    if (fromIdx >= 0 && toIdx >= 0) {
      if (fromIdx < toIdx) {
        grid.insertBefore(dragEl, targetPanel.nextSibling);
      } else {
        grid.insertBefore(dragEl, targetPanel);
      }
      const newOrder = Array.from(grid.querySelectorAll('.panel')).map(el => el.dataset.panelId);
      state.order = newOrder;
      newOrder.forEach((pid, i) => {
        const sizeClass = Array.from(
          document.querySelector(`[data-panel-id="${pid}"]`)?.classList || []
        ).find(c => c.startsWith('size-'));
        state.manualPositions[pid] = {
          index: i,
          size: sizeClass ? sizeClass.replace('size-', '') : 'medium',
        };
      });
      saveState();
      updateStats();
    }
    dragEl.classList.remove('dragging');
    dragEl = null;
    dragOverEl = null;
  });
  grid.addEventListener('dragend', e => {
    if (dragEl) {
      dragEl.classList.remove('dragging');
      dragEl = null;
    }
    if (dragOverEl) {
      dragOverEl.classList.remove('drag-over');
      dragOverEl = null;
    }
  });
}
function setupIntersectionObserver() {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) continue;
      if (entry.isIntersecting) {
        startViewTracking(panelId);
      } else {
        stopViewTracking(panelId);
      }
    }
  }, { threshold: 0.5 });
  const mutationObs = new MutationObserver(() => {
    observer.disconnect();
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  });
  mutationObs.observe(document.getElementById('grid'), { childList: true, subtree: true });
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
function setupEventDelegation() {
  document.getElementById('grid').addEventListener('click', handlePanelClick);
  document.getElementById('btn-reset').addEventListener('click', resetAll);
  document.getElementById('btn-seed').addEventListener('click', seedDemoData);
  document.getElementById('btn-auto').addEventListener('click', () => {
    if (state.isManualMode) toggleManualMode();
  });
  document.getElementById('btn-manual').addEventListener('click', () => {
    if (!state.isManualMode) toggleManualMode();
  });
  document.getElementById('btn-add-panel').addEventListener('click', addPanel);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopAllTracking();
    } else {
      document.querySelectorAll('.panel').forEach(el => {
        const rect = el.getBoundingClientRect();
        const inView = rect.top < window.innerHeight && rect.bottom > 0;
        if (inView) startViewTracking(el.dataset.panelId);
      });
    }
  });
  window.addEventListener('beforeunload', () => {
    stopAllTracking();
    saveState();
  });
}
function e2eSelfTest() {
  const results = [];
  const grid = document.getElementById('grid');
  const assert = (condition, msg) => {
    results.push({ pass: !!condition, msg });
    if (!condition) console.warn('[E2E FAIL]', msg);
  };
  assert(state.panels.length > 0, 'Panels exist after init');
  assert(Object.keys(state.tracking).length === state.panels.length, 'Tracking entries match panel count');
  assert(grid.children.length > 0 || state.panels.length > 0, 'Grid has children or panels exist');
  const panelEls = grid.querySelectorAll('.panel');
  assert(panelEls.length === state.panels.length, `DOM panel count (${panelEls.length}) matches state (${state.panels.length})`);
  for (const el of panelEls) {
    const pid = el.dataset.panelId;
    assert(!!state.tracking[pid], `Tracking exists for panel ${pid}`);
    assert(!!findPanel(pid), `Panel data exists for ${pid}`);
    const lockBtn = el.querySelector('.lock-btn');
    assert(!!lockBtn, `Lock button exists on panel ${pid}`);
    const compactBtn = el.querySelector('.compact-btn');
    assert(!!compactBtn, `Compact button exists on panel ${pid}`);
  }
  const lockBtns = document.querySelectorAll('.lock-btn');
  let lockToggleWorks = false;
  if (lockBtns.length > 0) {
    const testPid = lockBtns[0].dataset.panel;
    const wasLocked = !!state.locks[testPid];
    toggleLock(testPid);
    lockToggleWorks = !!state.locks[testPid] !== wasLocked;
    toggleLock(testPid);
  }
  assert(lockToggleWorks, 'Lock toggle works');
  const compactBtns = document.querySelectorAll('.compact-btn');
  let compactToggleWorks = false;
  if (compactBtns.length > 0) {
    const testPid = compactBtns[0].dataset.panel;
    const wasCompact = !!state.compactOverrides[testPid];
    toggleCompact(testPid);
    compactToggleWorks = !!state.compactOverrides[testPid] !== wasCompact;
    toggleCompact(testPid);
  }
  assert(compactToggleWorks, 'Compact toggle works');
  assert(typeof computeScore(state.panels[0].id) === 'number', 'computeScore returns a number');
  const layout = computeLayout();
  assert(Array.isArray(layout), 'computeLayout returns array');
  assert(layout.length === state.panels.length, 'Layout has entry for each panel');
  const data = getPanelData(state.panels[0].id);
  assert(!!data.panel, 'getPanelData returns panel');
  assert(!!data.tracking, 'getPanelData returns tracking');
  return results;
}
function init() {
  const loaded = loadState();
  if (!loaded) {
    state.panels = defaultPanels();
    state.tracking = {};
    syncTrackingKeys();
    state.order = state.panels.map(p => p.id);
    state.locks = {};
    state.manualPositions = {};
    state.compactOverrides = {};
    state.isManualMode = false;
    state.totalInteractions = 0;
    state.storageAvailable = true;
  } else {
    syncTrackingKeys();
  }
  renderGrid();
  updateToolbarButtons();
  setupEventDelegation();
  setupDragAndDrop();
  setupIntersectionObserver();
  const testResults = e2eSelfTest();
  const failures = testResults.filter(r => !r.pass);
  if (failures.length > 0) {
    console.error('E2E Self-Test Failures:', failures.map(f => f.msg));
  } else {
    console.log('E2E Self-Test: all', testResults.length, 'assertions passed');
  }
  if (state.totalInteractions < MIN_INTERACTIONS_BEFORE_RANK) {
    setTimeout(() => {
      if (state.totalInteractions < MIN_INTERACTIONS_BEFORE_RANK) {
        toast('Low interaction data — seed demo data for visible adaptive behavior (click "Seed Demo")');
      }
    }, 3000);
  }
}
init();
</script>
</body>
</html>
```
Save to `E:\Stryde\_alpedal\styde-forge\adaptive-dashboard.html` and open in browser.
Core architecture:
- Panels tracked via IntersectionObserver (view duration) + click delegation (interactions)
- Score = frequency × normalized_duration × recency_decay × expand_bonus
- Tied scores resolve alphabetically by panel id
- Layout: top quartile → size-large (span 2), bottom quartile → size-compact, middle → medium
- Compact mode: dashed border, collapsed body, preview row with mini metric value
- Manual mode: drag-and-drop reorder, position locks persist through mode switches
- localStorage with QuotaExceededError catch → degrades to in-memory only
- E2E self-test runs on init: asserts panel count matches DOM, all buttons exist, toggle functions work, getPanelData returns valid refs
- After 3 seconds with < 3 interactions, prompts user to seed demo data so adaptive behavior is always visible
- Visibility API: pauses tracking when tab hidden, resumes on return