<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --grid-cols: 4;
  --gap: 12px;
  --panel-min-w: 200px;
  --transition-speed: 0.35s;
  --color-bg: #0f1117;
  --color-surface: #1a1d27;
  --color-surface-hover: #22263a;
  --color-border: #2a2d3a;
  --color-accent: #6c8cff;
  --color-accent-dim: #3a4478;
  --color-text: #e0e2ec;
  --color-text-dim: #888a9a;
  --color-danger: #ff6b7a;
  --color-warn: #ffb347;
  --color-success: #4ecdc4;
  --drawer-width: 280px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
}
.app-shell {
  display: flex;
  height: 100vh;
}
.drawer {
  width: var(--drawer-width);
  min-width: var(--drawer-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-speed);
  z-index: 100;
}
.drawer-header {
  padding: 20px 16px 12px;
  border-bottom: 1px solid var(--color-border);
}
.drawer-header h2 {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--color-text);
}
.drawer-subtitle {
  font-size: 11px;
  color: var(--color-text-dim);
  margin-top: 4px;
}
.drawer-panels {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.drawer-panel-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: grab;
  user-select: none;
  margin-bottom: 4px;
  transition: background 0.15s;
  border: 1px solid transparent;
}
.drawer-panel-item:hover { background: var(--color-surface-hover); }
.drawer-panel-item:active { cursor: grabbing; }
.drawer-panel-item.dragging { opacity: 0.4; border: 1px dashed var(--color-accent-dim); }
.drawer-panel-icon {
  width: 32px; height: 32px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.drawer-panel-info { flex: 1; min-width: 0; }
.drawer-panel-name { font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.drawer-panel-score { font-size: 10px; color: var(--color-text-dim); margin-top: 2px; }
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
}
.toolbar-title {
  font-size: 14px;
  font-weight: 600;
  margin-right: auto;
}
.toolbar-btn {
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: transparent;
  color: var(--color-text);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.toolbar-btn:hover { background: var(--color-surface-hover); border-color: var(--color-accent-dim); }
.toolbar-btn.active { background: var(--color-accent); border-color: var(--color-accent); color: #fff; }
.toolbar-btn.danger { border-color: var(--color-danger); color: var(--color-danger); }
.toolbar-btn.danger:hover { background: var(--color-danger); color: #fff; }
.grid-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: var(--gap);
  transition: grid-template-columns 0.3s;
}
.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  overflow: hidden;
  transition: all var(--transition-speed);
  display: flex;
  flex-direction: column;
  position: relative;
  cursor: default;
}
.panel:hover { border-color: var(--color-accent-dim); }
.panel.locked { border-color: var(--color-warn); }
.panel.locked::after {
  content: 'locked';
  position: absolute;
  top: 6px; right: 8px;
  font-size: 9px;
  color: var(--color-warn);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  opacity: 0.7;
  pointer-events: none;
}
.panel.compact { grid-row: span 1 !important; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.compact .panel-header { padding: 8px 12px; }
.panel.drag-over { border: 2px dashed var(--color-accent); background: rgba(108,140,255,0.06); }
.panel-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}
.panel-header-icon {
  width: 28px; height: 28px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px;
  flex-shrink: 0;
}
.panel-header-title {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-header-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}
.panel:hover .panel-header-actions { opacity: 1; }
.panel-action-btn {
  width: 24px; height: 24px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--color-text-dim);
  cursor: pointer;
  font-size: 12px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.panel-action-btn:hover { background: var(--color-surface-hover); color: var(--color-text); }
.panel-action-btn.lock-toggle.locked { color: var(--color-warn); }
.panel-body {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80px;
}
.panel-metric {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1;
}
.panel-label {
  font-size: 11px;
  color: var(--color-text-dim);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.panel-sparkline {
  width: 100%;
  height: 40px;
  margin-top: 12px;
}
.panel-preview {
  display: none;
  padding: 8px 16px;
  font-size: 11px;
  color: var(--color-text-dim);
  align-items: center;
  gap: 8px;
}
.panel-rank-badge {
  position: absolute;
  top: 8px; left: 8px;
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--color-accent);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  z-index: 2;
}
.drag-ghost {
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.85;
  background: var(--color-surface);
  border: 2px solid var(--color-accent);
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  transform: translate(-50%, -50%);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s;
}
.modal {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  width: 480px;
  max-width: 90vw;
  box-shadow: 0 16px 48px rgba(0,0,0,0.5);
}
.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: 12px;
}
.modal-title { font-size: 15px; font-weight: 600; flex: 1; }
.modal-close {
  width: 28px; height: 28px;
  border: none; border-radius: 6px;
  background: transparent;
  color: var(--color-text-dim);
  cursor: pointer;
  font-size: 16px;
}
.modal-close:hover { background: var(--color-surface-hover); color: var(--color-text); }
.modal-body { padding: 20px; }
.picker-grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), 1fr);
  grid-auto-rows: 40px;
  gap: 4px;
  margin-bottom: 16px;
}
.picker-cell {
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-bg);
  cursor: pointer;
  transition: all 0.1s;
  position: relative;
}
.picker-cell:hover { background: var(--color-surface-hover); }
.picker-cell.selected { background: var(--color-accent); border-color: var(--color-accent); }
.picker-cell.occupied { background: rgba(255,107,122,0.15); border-color: var(--color-danger); cursor: not-allowed; }
.picker-cell.occupied::after {
  content: 'occupied';
  position: absolute;
  inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 8px;
  color: var(--color-danger);
  text-transform: uppercase;
}
.picker-info {
  font-size: 12px;
  color: var(--color-text-dim);
  margin-bottom: 12px;
}
.picker-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px 20px;
  font-size: 13px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  z-index: 300;
  animation: slideUp 0.25s;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 1400px) { :root { --grid-cols: 3; } }
@media (max-width: 1000px) { :root { --grid-cols: 2; } }
@media (max-width: 640px)  { :root { --grid-cols: 1; } .drawer { position: fixed; left: 0; top: 0; bottom: 0; transform: translateX(-100%); } .drawer.open { transform: translateX(0); } }
</style>
</head>
<body>
<div class="app-shell">
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <h2>Panel Library</h2>
      <div class="drawer-subtitle">Drag panels onto the grid to add them</div>
    </div>
    <div class="drawer-panels" id="drawerPanels"></div>
  </aside>
  <main class="main-area">
    <div class="toolbar">
      <span class="toolbar-title">Adaptive Dashboard</span>
      <button class="toolbar-btn" id="btnToggleDrawer" title="Toggle panel drawer">Drawer</button>
      <button class="toolbar-btn" id="btnRecalc" title="Recalculate layout">Recalc</button>
      <button class="toolbar-btn danger" id="btnReset" title="Reset all tracking data">Reset</button>
    </div>
    <div class="grid-container">
      <div class="grid" id="grid"></div>
    </div>
  </main>
</div>
<div class="drag-ghost" id="dragGhost" style="display:none"></div>
<div id="toastContainer"></div>
<div id="modalContainer"></div>
<script>
(function() {
'use strict';
// ========= CONFIGURATION =========
const STORAGE_KEY = 'adaptive_layout_v1';
const DECAY_HALF_LIFE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
const COMPACT_THRESHOLD = 0.2; // score ratio below max -> compact
const MIN_VIEW_DURATION_MS = 500; // minimum visible ms to count as a view
const INTERSECTION_THRESHOLD = 0.5; // 50% visible to count
// ========= DOM REFS =========
const gridEl = document.getElementById('grid');
const drawerPanelsEl = document.getElementById('drawerPanels');
const dragGhost = document.getElementById('dragGhost');
const toastContainer = document.getElementById('toastContainer');
const modalContainer = document.getElementById('modalContainer');
// ========= STATE =========
let panels = [];           // all panel definitions
let layout = [];           // [{panelId, col, row, colSpan, rowSpan, locked}]
let tracking = {};         // {panelId: {views, totalDuration, lastViewed, interactions}}
let gridCols = 4;
// Default panel definitions with IDs, names, icons, colors, and initial data
const DEFAULT_PANELS = [
  { id: 'revenue',    name: 'Revenue',        icon: '$',  color: '#4ecdc4', metric: '$128.4K', label: 'Monthly',  data: [30,45,38,52,48,60,55,72,65,80,75,92,88,95,90,85,98,95,100,105] },
  { id: 'users',      name: 'Active Users',   icon: 'U',  color: '#6c8cff', metric: '24,821',  label: 'Weekly',   data: [10,12,14,13,16,15,18,17,20,19,22,21,23,22,25,24,26,25,27,26] },
  { id: 'conversion', name: 'Conversion',     icon: '%',  color: '#ffb347', metric: '3.82%',   label: 'Rate',     data: [2.1,2.3,2.8,2.5,3.1,2.9,3.4,3.2,3.6,3.3,3.9,3.5,3.7,3.8,3.6,3.9,3.7,3.8,3.9,3.82] },
  { id: 'churn',      name: 'Churn Rate',     icon: 'C',  color: '#ff6b7a', metric: '1.24%',   label: 'Monthly',  data: [1.8,1.7,1.6,1.5,1.5,1.4,1.4,1.3,1.3,1.2,1.3,1.2,1.2,1.3,1.25,1.2,1.22,1.24,1.23,1.24] },
  { id: 'latency',    name: 'API Latency',    icon: 'ms', color: '#a855f7', metric: '42ms',    label: 'p95',      data: [55,52,48,50,45,47,43,44,40,42,38,41,40,39,42,41,43,42,41,42] },
  { id: 'errors',     name: 'Error Rate',     icon: '!',  color: '#f43f5e', metric: '0.12%',   label: '5min',     data: [0.3,0.25,0.2,0.18,0.15,0.13,0.1,0.12,0.09,0.11,0.08,0.1,0.09,0.11,0.1,0.12,0.11,0.13,0.12,0.12] },
  { id: 'storage',    name: 'Storage',        icon: 'GB', color: '#10b981', metric: '742 GB',  label: 'Used',     data: [600,610,620,630,640,650,660,670,680,690,700,705,710,715,720,725,730,735,740,742] },
  { id: 'bandwidth',  name: 'Bandwidth',      icon: 'M',  color: '#06b6d4', metric: '8.2 TB',  label: 'Daily',    data: [5,5.5,6,6.2,6.5,6.8,7,7.2,7.5,7.8,8,8.1,8.3,8.4,8.2,8.5,8.3,8.1,8.2,8.2] },
];
// ========= RESPONSIVE GRID =========
// Sync CSS custom property with JS-accessible value via matchMedia queries
function syncGridColumns() {
  const w = window.innerWidth;
  if (w <= 640)  gridCols = 1;
  else if (w <= 1000) gridCols = 2;
  else if (w <= 1400) gridCols = 3;
  else gridCols = 4;
  document.documentElement.style.setProperty('--grid-cols', gridCols);
}
// Listen to all breakpoints via matchMedia for reactive updates
const breakpoints = [
  { mq: window.matchMedia('(max-width: 640px)'),  cols: 1 },
  { mq: window.matchMedia('(max-width: 1000px)'), cols: 2 },
  { mq: window.matchMedia('(max-width: 1400px)'), cols: 3 },
  { mq: window.matchMedia('(min-width: 1401px)'), cols: 4 },
];
breakpoints.forEach(bp => {
  bp.mq.addEventListener('change', (e) => {
    if (e.matches) {
      gridCols = bp.cols;
      document.documentElement.style.setProperty('--grid-cols', gridCols);
      // Re-run layout on breakpoint change to fix overlaps
      if (layout.length > 0) {
        const scores = computeAllScores();
        const locked = layout.filter(l => l.locked);
        layout = computeLayout(scores, locked);
        renderGrid();
      }
    }
  });
});
syncGridColumns();
// ========= PERSISTENCE =========
function saveState() {
  const state = { layout, tracking, panels };
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) { /* quota exceeded */ }
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    const state = JSON.parse(raw);
    if (state.panels) panels = state.panels;
    if (state.layout) layout = state.layout;
    if (state.tracking) tracking = state.tracking;
    return true;
  } catch(e) { return false; }
}
function resetState() {
  panels = DEFAULT_PANELS.map(p => ({...p}));
  layout = [];
  tracking = {};
  try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
}
// ========= TRACKING ENGINE =========
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const panelId = entry.target.dataset.panelId;
    if (!panelId || !tracking[panelId]) return;
    if (entry.isIntersecting) {
      tracking[panelId]._visibleSince = Date.now();
    } else if (tracking[panelId]._visibleSince) {
      const duration = Date.now() - tracking[panelId]._visibleSince;
      if (duration >= MIN_VIEW_DURATION_MS) {
        tracking[panelId].views = (tracking[panelId].views || 0) + 1;
        tracking[panelId].totalDuration = (tracking[panelId].totalDuration || 0) + duration;
        tracking[panelId].lastViewed = Date.now();
      }
      tracking[panelId]._visibleSince = null;
    }
  });
}, { threshold: INTERSECTION_THRESHOLD });
function initTracking(panelId) {
  if (!tracking[panelId]) {
    tracking[panelId] = { views: 0, totalDuration: 0, lastViewed: Date.now(), interactions: 0, _visibleSince: null };
  }
}
function recordInteraction(panelId) {
  if (!tracking[panelId]) initTracking(panelId);
  tracking[panelId].interactions = (tracking[panelId].interactions || 0) + 1;
}
// ========= SCORING ENGINE =========
function computeScore(track, now) {
  if (!track) return 0;
  const views = track.views || 0;
  const interactions = track.interactions || 0;
  if (views === 0 && interactions === 0) return 0;
  const durationHours = (track.totalDuration || 0) / 3600000;
  const frequency = views + interactions * 1.5; // interactions weighted higher
  const recencyMs = now - (track.lastViewed || now);
  const recencyFactor = Math.pow(0.5, recencyMs / DECAY_HALF_LIFE_MS); // exponential decay
  return (frequency * 0.5 + durationHours * 1.0) * recencyFactor; // duration weighted 2x frequency
}
function computeAllScores() {
  const now = Date.now();
  const scores = {};
  panels.forEach(p => {
    scores[p.id] = computeScore(tracking[p.id], now);
  });
  return scores;
}
// ========= LAYOUT ENGINE =========
function computeLayout(scores, lockedItems) {
  const result = [];
  const occupancy = {}; // "col,row" -> true
  // Step 1: Register locked panels in occupancy grid BEFORE greedy placement
  (lockedItems || []).forEach(item => {
    const { col, row, colSpan = 1, rowSpan = 1 } = item;
    for (let c = col; c < col + colSpan; c++) {
      for (let r = row; r < row + rowSpan; r++) {
        occupancy[`${c},${r}`] = true;
      }
    }
    result.push({...item, locked: true});
  });
  // Step 2: Sort unlocked panels by score descending
  const sortedIds = Object.entries(scores)
    .filter(([id]) => !lockedItems || !lockedItems.some(l => l.panelId === id))
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id);
  // Step 3: Greedy placement — find first free span for each panel
  sortedIds.forEach((panelId, rank) => {
    const score = scores[panelId] || 0;
    const maxScore = Math.max(...Object.values(scores), 1);
    const scoreRatio = score / maxScore;
    // High-score panels get larger spans; low-score get compact
    let colSpan, rowSpan;
    if (scoreRatio >= 0.7)      { colSpan = 2; rowSpan = 2; }
    else if (scoreRatio >= 0.4) { colSpan = 1; rowSpan = 2; }
    else if (scoreRatio >= COMPACT_THRESHOLD) { colSpan = 1; rowSpan = 1; }
    else                         { colSpan = 1; rowSpan = 1; } // compact handled in render
    // Wrap colSpan to grid width
    colSpan = Math.min(colSpan, gridCols);
    // Find first available position
    let placed = false;
    const maxRow = 20; // safety cap
    for (let r = 0; r < maxRow && !placed; r++) {
      for (let c = 0; c <= gridCols - colSpan && !placed; c++) {
        let fits = true;
        for (let dc = 0; dc < colSpan && fits; dc++) {
          for (let dr = 0; dr < rowSpan && fits; dr++) {
            if (occupancy[`${c + dc},${r + dr}`]) fits = false;
          }
        }
        if (fits) {
          for (let dc = 0; dc < colSpan; dc++) {
            for (let dr = 0; dr < rowSpan; dr++) {
              occupancy[`${c + dc},${r + dr}`] = true;
            }
          }
          result.push({ panelId, col: c, row: r, colSpan, rowSpan, locked: false, scoreRatio });
          placed = true;
        }
      }
    }
    if (!placed) {
      // Force-place at end if grid is full
      let maxR = 0;
      Object.keys(occupancy).forEach(k => { const rr = parseInt(k.split(',')[1]); if (rr >= maxR) maxR = rr + 1; });
      result.push({ panelId, col: 0, row: maxR, colSpan: 1, rowSpan: 1, locked: false, scoreRatio });
    }
  });
  return result;
}
// ========= RENDER =========
function renderGrid() {
  gridEl.innerHTML = '';
  const scores = computeAllScores();
  const maxScore = Math.max(...Object.values(scores), 1);
  // Sort layout by row then col for display order (CSS Grid auto-flow would interfere)
  const sortedLayout = [...layout].sort((a, b) => a.row - b.row || a.col - b.col);
  sortedLayout.forEach((item, idx) => {
    const panel = panels.find(p => p.id === item.panelId);
    if (!panel) return;
    const score = scores[panel.id] || 0;
    const scoreRatio = score / maxScore;
    const isCompact = scoreRatio < COMPACT_THRESHOLD && !item.locked;
    const el = document.createElement('div');
    el.className = 'panel' + (item.locked ? ' locked' : '') + (isCompact ? ' compact' : '');
    el.dataset.panelId = panel.id;
    el.style.gridColumn = `${item.col + 1} / span ${item.colSpan}`;
    el.style.gridRow = `${item.row + 1} / span ${item.rowSpan}`;
    el.draggable = true;
    // Rank badge for top 3
    if (idx < 3 && !isCompact) {
      const badge = document.createElement('div');
      badge.className = 'panel-rank-badge';
      badge.textContent = idx + 1;
      el.appendChild(badge);
    }
    // Header
    const header = document.createElement('div');
    header.className = 'panel-header';
    header.innerHTML = `
      <div class="panel-header-icon" style="background:${panel.color}22;color:${panel.color}">${panel.icon}</div>
      <div class="panel-header-title">${panel.name}</div>
      <div class="panel-header-actions">
        <button class="panel-action-btn lock-toggle${item.locked ? ' locked' : ''}" data-action="lock" title="Lock position">L</button>
        <button class="panel-action-btn" data-action="move" title="Move panel">M</button>
        <button class="panel-action-btn" data-action="remove" title="Remove from grid">X</button>
      </div>`;
    el.appendChild(header);
    // Body (hidden in compact mode)
    if (!isCompact) {
      const body = document.createElement('div');
      body.className = 'panel-body';
      body.innerHTML = `
        <div class="panel-metric" style="color:${panel.color}">${panel.metric}</div>
        <div class="panel-label">${panel.label}</div>
        <svg class="panel-sparkline" viewBox="0 0 200 40" preserveAspectRatio="none">
          <polyline fill="none" stroke="${panel.color}" stroke-width="2"
            points="${sparklinePoints(panel.data, 200, 40)}"
            stroke-linecap="round" stroke-linejoin="round"/>
          <polygon fill="${panel.color}22"
            points="0,40 ${sparklineArea(panel.data, 200, 40)} 200,40"/>
        </svg>`;
      el.appendChild(body);
    }
    // Preview for compact
    const preview = document.createElement('div');
    preview.className = 'panel-preview';
    preview.innerHTML = `<span style="color:${panel.color};font-weight:600">${panel.metric}</span> ${panel.label} (score: ${score.toFixed(1)})`;
    el.appendChild(preview);
    // Click tracking
    el.addEventListener('click', (e) => {
      if (e.target.closest('[data-action]')) return; // don't count action button clicks
      recordInteraction(panel.id);
    });
    // Drag handlers
    el.addEventListener('dragstart', handleDragStart);
    el.addEventListener('dragend', handleDragEnd);
    el.addEventListener('dragover', handleDragOver);
    el.addEventListener('dragleave', handleDragLeave);
    el.addEventListener('drop', handleDrop);
    // Action buttons
    el.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const action = btn.dataset.action;
        if (action === 'lock') toggleLock(panel.id);
        else if (action === 'move') openPositionPicker(panel.id);
        else if (action === 'remove') removeFromGrid(panel.id);
      });
    });
    // Observe for view tracking
    observer.observe(el);
    gridEl.appendChild(el);
  });
  renderDrawer();
  saveState();
}
function sparklinePoints(data, width, height) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const stepX = width / (data.length - 1);
  return data.map((v, i) => `${(i * stepX).toFixed(1)},${(height - ((v - min) / range) * (height - 4) - 2).toFixed(1)}`).join(' ');
}
function sparklineArea(data, width, height) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const stepX = width / (data.length - 1);
  const pts = data.map((v, i) => `${(i * stepX).toFixed(1)},${(height - ((v - min) / range) * (height - 4) - 2).toFixed(1)}`).join(' ');
  return pts;
}
function renderDrawer() {
  const scores = computeAllScores();
  const maxScore = Math.max(...Object.values(scores), 1);
  const gridPanelIds = new Set(layout.map(l => l.panelId));
  const available = panels.filter(p => !gridPanelIds.has(p.id));
  drawerPanelsEl.innerHTML = '';
  // Sort drawer panels by score
  available.sort((a, b) => (scores[b.id] || 0) - (scores[a.id] || 0));
  available.forEach(panel => {
    const score = scores[panel.id] || 0;
    const scoreRatio = score / maxScore;
    const item = document.createElement('div');
    item.className = 'drawer-panel-item';
    item.draggable = true;
    item.dataset.panelId = panel.id;
    item.innerHTML = `
      <div class="drawer-panel-icon" style="background:${panel.color}22;color:${panel.color}">${panel.icon}</div>
      <div class="drawer-panel-info">
        <div class="drawer-panel-name">${panel.name}</div>
        <div class="drawer-panel-score">Score: ${score.toFixed(1)} | ${scoreRatio < COMPACT_THRESHOLD ? 'Low usage' : scoreRatio >= 0.7 ? 'High priority' : 'Normal'}</div>
      </div>`;
    item.addEventListener('dragstart', handleDrawerDragStart);
    item.addEventListener('dragend', handleDragEnd);
    drawerPanelsEl.appendChild(item);
  });
}
// ========= DRAG AND DROP =========
let dragSource = null; // {type: 'drawer'|'grid', panelId}
function handleDrawerDragStart(e) {
  dragSource = { type: 'drawer', panelId: e.currentTarget.dataset.panelId };
  e.currentTarget.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', e.currentTarget.dataset.panelId);
  showDragGhost(e, e.currentTarget.dataset.panelId);
}
function handleDragStart(e) {
  dragSource = { type: 'grid', panelId: e.currentTarget.dataset.panelId };
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', e.currentTarget.dataset.panelId);
  showDragGhost(e, e.currentTarget.dataset.panelId);
}
function showDragGhost(e, panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  dragGhost.textContent = panel.name;
  dragGhost.style.display = 'block';
  dragGhost.style.left = e.clientX + 'px';
  dragGhost.style.top = e.clientY + 'px';
}
function handleDragEnd(e) {
  dragGhost.style.display = 'none';
  document.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  dragSource = null;
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}
function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  const targetPanelId = e.currentTarget.dataset.panelId;
  const sourcePanelId = e.dataTransfer.getData('text/plain');
  if (!sourcePanelId || !targetPanelId || sourcePanelId === targetPanelId) return;
  if (dragSource && dragSource.type === 'drawer') {
    // Add from drawer at target position
    addToGrid(sourcePanelId, targetPanelId);
  } else if (dragSource && dragSource.type === 'grid') {
    // Swap grid positions
    swapGridPositions(sourcePanelId, targetPanelId);
  }
  dragSource = null;
}
// Handle drops on the grid itself (not on a panel)
gridEl.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});
gridEl.addEventListener('drop', (e) => {
  e.preventDefault();
  const sourcePanelId = e.dataTransfer.getData('text/plain');
  if (!sourcePanelId || !dragSource || dragSource.type !== 'drawer') return;
  // Add from drawer at end of grid
  const scores = computeAllScores();
  const locked = layout.filter(l => l.locked);
  layout = computeLayout(scores, locked);
  // Add the new panel
  const newItem = layout.find(l => l.panelId === sourcePanelId);
  if (!newItem) {
    // Force add
    const maxRow = layout.reduce((m, l) => Math.max(m, l.row + l.rowSpan), 0);
    layout.push({ panelId: sourcePanelId, col: 0, row: maxRow, colSpan: 1, rowSpan: 1, locked: false });
  }
  renderGrid();
  dragSource = null;
  showToast('Panel added to grid');
});
function addToGrid(panelId, targetPanelId) {
  const targetItem = layout.find(l => l.panelId === targetPanelId);
  if (!targetItem) return;
  const newItem = {
    panelId,
    col: targetItem.col,
    row: targetItem.row,
    colSpan: targetItem.colSpan,
    rowSpan: targetItem.rowSpan,
    locked: false
  };
  // Shift target and subsequent items down
  layout.push(newItem);
  recalculateLayout();
  showToast('Panel added from drawer');
}
function swapGridPositions(id1, id2) {
  const item1 = layout.find(l => l.panelId === id1);
  const item2 = layout.find(l => l.panelId === id2);
  if (!item1 || !item2) return;
  if (item1.locked || item2.locked) {
    showToast('Cannot swap locked panels', 'warn');
    return;
  }
  const tmp = { col: item1.col, row: item1.row, colSpan: item1.colSpan, rowSpan: item1.rowSpan };
  item1.col = item2.col; item1.row = item2.row; item1.colSpan = item2.colSpan; item1.rowSpan = item2.rowSpan;
  item2.col = tmp.col; item2.row = tmp.row; item2.colSpan = tmp.colSpan; item2.rowSpan = tmp.rowSpan;
  renderGrid();
  showToast('Panels swapped');
}
// ========= LOCK TOGGLE =========
function toggleLock(panelId) {
  const item = layout.find(l => l.panelId === panelId);
  if (!item) return;
  item.locked = !item.locked;
  renderGrid();
  showToast(item.locked ? 'Panel locked' : 'Panel unlocked');
}
// ========= REMOVE FROM GRID =========
function removeFromGrid(panelId) {
  layout = layout.filter(l => l.panelId !== panelId);
  renderGrid();
  showToast('Panel removed from grid');
}
// ========= POSITION PICKER (multi-cell region selection) =========
let pickerState = null; // {panelId, colSpan, rowSpan, startCol, startRow, mode: 'selecting'|'done'}
function openPositionPicker(panelId) {
  pickerState = {
    panelId,
    colSpan: 1,
    rowSpan: 1,
    startCol: -1,
    startRow: -1,
    selectedCells: new Set()
  };
  const currentItem = layout.find(l => l.panelId === panelId);
  if (currentItem) {
    pickerState.colSpan = currentItem.colSpan;
    pickerState.rowSpan = currentItem.rowSpan;
  }
  renderPickerModal();
}
function renderPickerModal() {
  const rows = 6;
  const cols = gridCols;
  // Build occupancy map (excluding the panel being moved)
  const occupancy = {};
  layout.forEach(item => {
    if (item.panelId === pickerState.panelId) return; // skip self
    if (!item.locked) return; // only locked items occupy in picker
    for (let c = item.col; c < item.col + (item.colSpan || 1); c++) {
      for (let r = item.row; r < item.row + (item.rowSpan || 1); r++) {
        occupancy[`${c},${r}`] = true;
      }
    }
  });
  let cellsHTML = '';
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const key = `${c},${r}`;
      const isOccupied = occupancy[key];
      const isSelected = pickerState.selectedCells.has(key);
      let cls = 'picker-cell';
      if (isOccupied) cls += ' occupied';
      if (isSelected) cls += ' selected';
      cellsHTML += `<div class="${cls}" data-col="${c}" data-row="${r}"></div>`;
    }
  }
  const panel = panels.find(p => p.id === pickerState.panelId);
  modalContainer.innerHTML = `
    <div class="modal-overlay" id="pickerOverlay">
      <div class="modal">
        <div class="modal-header">
          <span class="modal-title">Move: ${panel ? panel.name : pickerState.panelId}</span>
          <button class="modal-close" id="pickerClose">x</button>
        </div>
        <div class="modal-body">
          <div class="picker-info">
            Click a start cell, then click an end cell to select a ${pickerState.colSpan}x${pickerState.rowSpan} region.
            <br>Current span: <strong>${pickerState.colSpan} col x ${pickerState.rowSpan} row</strong>
            <br><small style="color:var(--color-danger)">Red cells are locked/occupied by other panels</small>
          </div>
          <div class="picker-grid" style="grid-template-columns:repeat(${cols},1fr)" id="pickerGrid">
            ${cellsHTML}
          </div>
          <div class="picker-actions">
            <button class="toolbar-btn" id="pickerSpan1">1x1</button>
            <button class="toolbar-btn" id="pickerSpan2">2x1</button>
            <button class="toolbar-btn" id="pickerSpan3">1x2</button>
            <button class="toolbar-btn" id="pickerSpan4">2x2</button>
            <button class="toolbar-btn" id="pickerClear">Clear</button>
            <button class="toolbar-btn active" id="pickerApply" disabled>Apply</button>
          </div>
        </div>
      </div>
    </div>`;
  // Event bindings
  document.getElementById('pickerClose').addEventListener('click', closePicker);
  document.getElementById('pickerOverlay').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closePicker();
  });
  document.getElementById('pickerClear').addEventListener('click', () => {
    pickerState.selectedCells.clear();
    pickerState.startCol = -1;
    pickerState.startRow = -1;
    renderPickerModal();
  });
  document.getElementById('pickerApply').addEventListener('click', applyPickerPosition);
  // Span presets
  document.getElementById('pickerSpan1').addEventListener('click', () => { pickerState.colSpan=1; pickerState.rowSpan=1; pickerState.selectedCells.clear(); pickerState.startCol=-1; pickerState.startRow=-1; renderPickerModal(); });
  document.getElementById('pickerSpan2').addEventListener('click', () => { pickerState.colSpan=2; pickerState.rowSpan=1; pickerState.selectedCells.clear(); pickerState.startCol=-1; pickerState.startRow=-1; renderPickerModal(); });
  document.getElementById('pickerSpan3').addEventListener('click', () => { pickerState.colSpan=1; pickerState.rowSpan=2; pickerState.selectedCells.clear(); pickerState.startCol=-1; pickerState.startRow=-1; renderPickerModal(); });
  document.getElementById('pickerSpan4').addEventListener('click', () => { pickerState.colSpan=2; pickerState.rowSpan=2; pickerState.selectedCells.clear(); pickerState.startCol=-1; pickerState.startRow=-1; renderPickerModal(); });
  // Cell click handling for multi-cell selection
  document.querySelectorAll('#pickerGrid .picker-cell:not(.occupied)').forEach(cell => {
    cell.addEventListener('click', () => {
      const c = parseInt(cell.dataset.col);
      const r = parseInt(cell.dataset.row);
      if (pickerState.startCol === -1) {
        // First click: set anchor
        pickerState.startCol = c;
        pickerState.startRow = r;
        selectCells(c, r, c, r);
      } else {
        // Second click: complete region
        selectCells(pickerState.startCol, pickerState.startRow, c, r);
      }
      renderPickerModal();
    });
  });
}
function selectCells(c1, r1, c2, r2) {
  pickerState.selectedCells.clear();
  const minC = Math.min(c1, c2);
  const maxC = Math.max(c1, c2);
  const minR = Math.min(r1, r2);
  const maxR = Math.max(r1, r2);
  pickerState.colSpan = maxC - minC + 1;
  pickerState.rowSpan = maxR - minR + 1;
  // Check if any cell in region is occupied
  const occupancy = {};
  layout.forEach(item => {
    if (item.panelId === pickerState.panelId) return;
    if (!item.locked) return;
    for (let c = item.col; c < item.col + (item.colSpan || 1); c++) {
      for (let r = item.row; r < item.row + (item.rowSpan || 1); r++) {
        occupancy[`${c},${r}`] = true;
      }
    }
  });
  let hasConflict = false;
  for (let c = minC; c <= maxC; c++) {
    for (let r = minR; r <= maxR; r++) {
      if (occupancy[`${c},${r}`]) { hasConflict = true; break; }
      pickerState.selectedCells.add(`${c},${r}`);
    }
    if (hasConflict) break;
  }
  if (hasConflict) {
    pickerState.selectedCells.clear();
    pickerState.startCol = -1;
    pickerState.startRow = -1;
    showToast('Selected region conflicts with locked panels', 'warn');
  }
  document.getElementById('pickerApply').disabled = pickerState.selectedCells.size === 0;
}
function applyPickerPosition() {
  if (pickerState.selectedCells.size === 0) return;
  const cells = Array.from(pickerState.selectedCells).map(k => k.split(',').map(Number));
  const minC = Math.min(...cells.map(c => c[0]));
  const minR = Math.min(...cells.map(c => c[1]));
  let item = layout.find(l => l.panelId === pickerState.panelId);
  if (item) {
    item.col = minC;
    item.row = minR;
    item.colSpan = pickerState.colSpan;
    item.rowSpan = pickerState.rowSpan;
  } else {
    layout.push({
      panelId: pickerState.panelId,
      col: minC,
      row: minR,
      colSpan: pickerState.colSpan,
      rowSpan: pickerState.rowSpan,
      locked: false
    });
  }
  closePicker();
  renderGrid();
  showToast('Panel repositioned');
}
function closePicker() {
  pickerState = null;
  modalContainer.innerHTML = '';
}
// ========= RECALCULATE LAYOUT =========
function recalculateLayout() {
  const scores = computeAllScores();
  const locked = layout.filter(l => l.locked);
  layout = computeLayout(scores, locked);
  renderGrid();
  showToast('Layout recalculated');
}
// ========= TOAST =========
function showToast(message, type) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  if (type === 'warn') toast.style.borderColor = 'var(--color-warn)';
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 2000);
}
// ========= INIT =========
function init() {
  if (!loadState()) {
    panels = DEFAULT_PANELS.map(p => ({...p}));
    // Initialize tracking for all panels
    panels.forEach(p => initTracking(p.id));
    // Initial layout computation
    const scores = computeAllScores();
    layout = computeLayout(scores, []);
  }
  // Ensure tracking exists for all panels
  panels.forEach(p => initTracking(p.id));
  renderGrid();
  // Toolbar buttons
  document.getElementById('btnToggleDrawer').addEventListener('click', () => {
    document.getElementById('drawer').classList.toggle('open');
  });
  document.getElementById('btnRecalc').addEventListener('click', recalculateLayout);
  document.getElementById('btnReset').addEventListener('click', () => {
    if (confirm('Reset all tracking data and layout?')) {
      resetState();
      panels.forEach(p => initTracking(p.id));
      const scores = computeAllScores();
      layout = computeLayout(scores, []);
      renderGrid();
      showToast('All data reset');
    }
  });
  // Periodic save (every 10s) and layout refresh (every 30s for score decay)
  setInterval(() => {
    saveState();
  }, 10000);
  // Auto-refresh layout periodically to reflect score changes
  setInterval(() => {
    const scores = computeAllScores();
    const locked = layout.filter(l => l.locked);
    const newLayout = computeLayout(scores, locked);
    // Only re-render if positions changed
    const changed = newLayout.length !== layout.length ||
      newLayout.some((nl, i) => {
        const ol = layout[i];
        return !ol || nl.panelId !== ol.panelId || nl.col !== ol.col || nl.row !== ol.row || nl.colSpan !== ol.colSpan || nl.rowSpan !== ol.rowSpan;
      });
    if (changed) {
      layout = newLayout;
      renderGrid();
    }
  }, 30000);
}
// ========= STARTUP =========
document.addEventListener('DOMContentLoaded', init);
// ========= PERFORMANCE: passive scroll listener for grid =========
document.querySelector('.grid-container')?.addEventListener('scroll', () => {
  // No-op; just ensure scroll performance by avoiding active listeners
}, { passive: true });
})();
</script>
</body>
</html>