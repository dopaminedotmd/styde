<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22263a;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa8;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --rank-1: #6c8cff;
  --rank-2: #7caf7a;
  --rank-3: #d4a76a;
  --rank-4: #c47a9e;
  --rank-5: #6aafcf;
  --compact-scale: 0.45;
  --transition-speed: 380ms;
  --easing: cubic-bezier(0.22, 0.61, 0.36, 1);
  --radius: 10px;
  --gap: 12px;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text);
  background: var(--bg);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; }
body {
  min-height: 100vh;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
  flex-shrink: 0;
}
h1 {
  font-size: 1.35rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}
.controls {
  display: flex;
  gap: 10px;
  align-items: center;
}
.btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-dim);
  padding: 7px 14px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 0.8rem;
  font-family: inherit;
  transition: background 150ms, color 150ms, border-color 150ms;
}
.btn:hover { background: var(--surface-hover); color: var(--text); border-color: #4a4e66; }
.btn.active { background: var(--accent-glow); border-color: var(--accent); color: var(--accent); }
#stats-bar {
  display: flex;
  gap: 20px;
  font-size: 0.75rem;
  color: var(--text-dim);
  margin-bottom: 16px;
  flex-shrink: 0;
}
.stat { display: flex; gap: 5px; align-items: baseline; }
.stat-val { color: var(--accent); font-weight: 600; font-variant-numeric: tabular-nums; }
.grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-auto-rows: 140px;
  gap: var(--gap);
  flex: 1;
  align-content: start;
  position: relative;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  position: relative;
  overflow: hidden;
  will-change: transform, width, height;
  transition: border-color 200ms, box-shadow 200ms, background 200ms;
  display: flex;
  flex-direction: column;
  cursor: grab;
  user-select: none;
  min-width: 0;
}
.panel:hover {
  border-color: #4a4e66;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.panel.dragging {
  cursor: grabbing;
  z-index: 100;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
  opacity: 0.92;
}
.panel.locked { border-color: #6c8cff55; }
.panel.locked .lock-indicator { opacity: 1; }
.panel.compact {
  padding: 8px 10px;
  font-size: 0.65rem;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.compact .panel-header { font-size: 0.72rem; }
.panel.hidden-panel { display: none; }
.panel.animating { pointer-events: none; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin-bottom: 6px;
  flex-shrink: 0;
}
.panel-title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.panel-actions { display: flex; gap: 4px; flex-shrink: 0; }
.panel-action {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  width: 22px;
  height: 22px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  transition: color 120ms, background 120ms;
  padding: 0;
}
.panel-action:hover { color: var(--text); background: #ffffff0a; }
.lock-indicator {
  opacity: 0;
  transition: opacity 200ms;
  font-size: 0.6rem;
  color: var(--accent);
}
.panel-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  color: var(--text);
  min-height: 40px;
}
.panel-body .metric-label {
  font-size: 0.6rem;
  font-weight: 400;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 2px;
}
.panel-preview { display: none; font-size: 0.55rem; color: var(--text-dim); }
.panel-rank-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 0.5rem;
  color: var(--text-dim);
  opacity: 0.4;
}
.more-section {
  grid-column: 1 / -1;
  margin-top: 6px;
  border-top: 1px dashed var(--border);
  padding-top: 14px;
}
.more-toggle {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-dim);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.72rem;
  font-family: inherit;
  transition: all 150ms;
  display: flex;
  align-items: center;
  gap: 6px;
}
.more-toggle:hover { border-color: #4a4e66; color: var(--text); }
.more-toggle .count { color: var(--accent); }
.more-panels {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--gap);
  margin-top: 10px;
}
.more-panels .panel { grid-column: span 1; grid-row: span 1; }
#heatmap-toggle.active { background: #6c8cff18; border-color: #6c8cff44; color: #6c8cff; }
.heat-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: var(--radius);
  transition: opacity 300ms;
  opacity: 0;
}
.heat-overlay.visible { opacity: 1; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Layout</h1>
  <div class="controls">
    <button class="btn" id="reset-btn" title="Reset all tracking data">Reset</button>
    <button class="btn" id="heatmap-toggle" title="Show attention heatmap">Heatmap</button>
    <button class="btn" id="auto-layout-toggle" class="active" title="Toggle auto-layout">Auto: ON</button>
  </div>
</header>
<div id="stats-bar">
  <div class="stat">Sessions: <span class="stat-val" id="stat-sessions">1</span></div>
  <div class="stat">Total views: <span class="stat-val" id="stat-views">0</span></div>
  <div class="stat">Locked: <span class="stat-val" id="stat-locked">0</span></div>
  <div class="stat">Compact: <span class="stat-val" id="stat-compact">0</span></div>
  <div class="stat">Next recalc: <span class="stat-val" id="stat-next">--</span></div>
</div>
<div class="grid" id="grid"></div>
<div class="more-section" id="more-section" style="display:none;">
  <button class="more-toggle" id="more-toggle">
    More panels <span class="count" id="more-count">0</span>
  </button>
  <div class="more-panels" id="more-panels" style="display:none;"></div>
</div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive-dashboard-v2';
const TRACK_INTERVAL = 2000;
const RECALC_COOLDOWN = 8000;
const DECAY_HALF_LIFE = 86400000;
const COMPACT_THRESHOLD = 0.2;
const HIDE_THRESHOLD = 0.06;
const PANEL_COUNT = 18;
const COLS = 6;
const GRID_ROW_HEIGHT = 140;
const GAP = 12;
const metricNames = [
  'CPU Usage', 'Memory', 'Disk I/O', 'Network In', 'Network Out',
  'Requests/s', 'Error Rate', 'P99 Latency', 'P50 Latency', 'Active Users',
  'Sessions', 'Cache Hit %', 'DB Queries', 'Queue Depth', 'Uptime',
  'Throughput', 'Connections', 'Thread Pool'
];
let panels = [];
let attentionData = {};
let layoutVersion = 0;
let isAutoLayout = true;
let scheduleTimeout = null;
let observer = null;
let viewTimers = {};
let dragging = null;
let dragClone = null;
let dragOffset = { x: 0, y: 0 };
let dragStartPos = null;
let moreExpanded = false;
let showHeatmap = false;
function now() { return Date.now(); }
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const state = JSON.parse(raw);
      attentionData = state.attentionData || {};
      if (state.panels && Array.isArray(state.panels) && state.panels.length === PANEL_COUNT) {
        panels = state.panels;
      } else {
        initPanels();
      }
      isAutoLayout = state.isAutoLayout !== false;
      document.getElementById('auto-layout-toggle').textContent = 'Auto: ' + (isAutoLayout ? 'ON' : 'OFF');
      if (!isAutoLayout) document.getElementById('auto-layout-toggle').classList.add('active');
      return;
    }
  } catch(e) {}
  initPanels();
}
function initPanels() {
  panels = [];
  for (let i = 0; i < PANEL_COUNT; i++) {
    panels.push({
      id: 'panel-' + i,
      label: metricNames[i],
      value: Math.round(Math.random() * 100),
      unit: ['%', 'GB', 'MB/s', 'Mbps', 'Mbps', 'rps', '%', 'ms', 'ms', '', '', '%', 'qps', '', '%', 'rps', '', '%'][i],
      locked: false,
      hidden: false,
      compact: false,
      colSpan: 2,
      rowSpan: 2,
      colStart: 1,
      rowStart: 1,
      userPosition: null
    });
  }
}
function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      panels: panels,
      attentionData: attentionData,
      isAutoLayout: isAutoLayout
    }));
  } catch(e) {}
}
function getAttentionScore(panelId) {
  const d = attentionData[panelId];
  if (!d) return 0;
  const age = now() - (d.lastView || now());
  const recency = Math.exp(-age / DECAY_HALF_LIFE);
  const freq = Math.min(d.viewCount || 0, 50);
  const dur = Math.min(d.totalDuration || 0, 300000) / 1000;
  const interact = Math.min(d.interactions || 0, 20);
  return (freq * 1.2 + dur * 0.8 + interact * 1.5) * recency;
}
function computeRankings() {
  const unlocked = panels.filter(p => !p.locked);
  const scored = unlocked.map(p => ({ id: p.id, score: getAttentionScore(p.id) }));
  scored.sort((a, b) => b.score - a.score);
  return scored;
}
function computeLayoutAssignments(scoredUnlocked) {
  const locked = panels.filter(p => p.locked);
  const layout = new Array(panels.length).fill(null);
  const lockedPositions = new Map();
  const usedSlots = new Set();
  locked.forEach(p => {
    const idx = panels.indexOf(p);
    if (idx >= 0) {
      layout[idx] = p.id;
      usedSlots.add(idx);
    }
  });
  const freeSlots = [];
  for (let i = 0; i < panels.length; i++) {
    if (!usedSlots.has(i)) freeSlots.push(i);
  }
  const compactCutoff = Math.floor(scoredUnlocked.length * COMPACT_THRESHOLD);
  const hideCutoff = Math.floor(scoredUnlocked.length * HIDE_THRESHOLD);
  scoredUnlocked.forEach((item, rank) => {
    let panel = panels.find(p => p.id === item.id);
    if (!panel || panel.locked) return;
    panel._rank = rank;
    if (freeSlots.length === 0) {
      panel.hidden = true;
      return;
    }
    const slotIdx = freeSlots.shift();
    layout[slotIdx] = panel.id;
    panel.hidden = rank < hideCutoff ? true : false;
    panel.compact = rank >= compactCutoff;
  });
  return layout;
}
function getGridSlot(index) {
  const col = index % COLS;
  const row = Math.floor(index / COLS);
  return { col: col + 1, row: row + 1 };
}
function assignGridPositions() {
  const scored = computeRankings();
  const layout = computeLayoutAssignments(scored);
  layout.forEach((panelId, idx) => {
    if (panelId === null) return;
    const panel = panels.find(p => p.id === panelId);
    if (!panel) return;
    const slot = getGridSlot(idx);
    const span = panel.compact ? 1 : 2;
    panel.colStart = slot.col;
    panel.rowStart = slot.row;
    panel.colSpan = span;
    panel.rowSpan = span;
  });
}
function applyLayout(animate) {
  if (scheduleTimeout !== null) {
    clearTimeout(scheduleTimeout);
    scheduleTimeout = null;
  }
  if (!isAutoLayout) return;
  const prevRects = animate ? captureRects() : null;
  if (animate) {
    document.querySelectorAll('.panel.animating').forEach(el => el.classList.remove('animating'));
  }
  assignGridPositions();
  const visiblePanels = panels.filter(p => !p.hidden);
  const hiddenPanels = panels.filter(p => p.hidden);
  renderPanels(visiblePanels, hiddenPanels);
  if (animate && prevRects) {
    requestAnimationFrame(() => {
      const currRects = captureRects();
      flipAnimate(prevRects, currRects);
    });
  }
  saveState();
  updateStats();
  layoutVersion++;
}
function captureRects() {
  const rects = {};
  document.querySelectorAll('.panel:not(.hidden-panel)').forEach(el => {
    const id = el.dataset.panelId;
    if (id) rects[id] = el.getBoundingClientRect();
  });
  return rects;
}
function flipAnimate(prev, curr) {
  const els = document.querySelectorAll('.panel:not(.hidden-panel)');
  const animating = [];
  els.forEach(el => {
    const id = el.dataset.panelId;
    if (!id) return;
    const pr = prev[id];
    const cr = curr[id];
    if (!pr || !cr) return;
    const dx = pr.left - cr.left;
    const dy = pr.top - cr.top;
    const dw = pr.width > 0 ? cr.width / pr.width : 1;
    const dh = pr.height > 0 ? cr.height / pr.height : 1;
    if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5 && Math.abs(dw - 1) < 0.005 && Math.abs(dh - 1) < 0.005) return;
    el.style.transform = `translate(${dx}px, ${dy}px) scale(${dw}, ${dh})`;
    el.style.transition = 'none';
    el.classList.add('animating');
    animating.push(el);
  });
  if (animating.length === 0) return;
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      animating.forEach(el => {
        el.style.transition = `transform var(--transition-speed) var(--easing)`;
        el.style.transform = 'translate(0, 0) scale(1, 1)';
      });
      const cleanup = () => {
        animating.forEach(el => {
          el.classList.remove('animating');
          el.style.transform = '';
          el.style.transition = '';
        });
      };
      setTimeout(cleanup, 400);
    });
  });
}
function renderPanels(visible, hidden) {
  const grid = document.getElementById('grid');
  const existingMap = new Map();
  grid.querySelectorAll('.panel').forEach(el => {
    existingMap.set(el.dataset.panelId, el);
  });
  const fragment = document.createDocumentFragment();
  const observed = new Set();
  visible.forEach(panel => {
    let el = existingMap.get(panel.id);
    if (el) {
      existingMap.delete(panel.id);
      patchPanelElement(el, panel);
    } else {
      el = createPanelElement(panel);
    }
    if (el.parentNode !== grid) {
      fragment.appendChild(el);
    }
    observed.add(panel.id);
  });
  existingMap.forEach(el => {
    if (observer) observer.unobserve(el);
    el.remove();
  });
  grid.appendChild(fragment);
  grid.querySelectorAll('.panel').forEach(el => {
    if (observer) {
      if (!observed.has(el.dataset.panelId)) {
        observer.unobserve(el);
      } else if (!el.dataset.observed) {
        observer.observe(el);
        el.dataset.observed = '1';
      }
    }
  });
  const moreSection = document.getElementById('more-section');
  const morePanels = document.getElementById('more-panels');
  const moreCount = document.getElementById('more-count');
  if (hidden.length > 0) {
    moreSection.style.display = '';
    moreCount.textContent = hidden.length;
    if (moreExpanded) {
      morePanels.style.display = '';
      const moreMap = new Map();
      morePanels.querySelectorAll('.panel').forEach(el => moreMap.set(el.dataset.panelId, el));
      const mfrag = document.createDocumentFragment();
      hidden.forEach(panel => {
        let el = moreMap.get(panel.id);
        if (el) {
          moreMap.delete(panel.id);
          patchPanelElement(el, panel);
        } else {
          el = createPanelElement(panel);
        }
        if (el.parentNode !== morePanels) mfrag.appendChild(el);
      });
      moreMap.forEach(el => {
        if (observer) observer.unobserve(el);
        el.remove();
      });
      morePanels.appendChild(mfrag);
      if (observer) {
        morePanels.querySelectorAll('.panel').forEach(el => {
          if (!el.dataset.observed) { observer.observe(el); el.dataset.observed = '1'; }
        });
      }
    }
  } else {
    moreSection.style.display = 'none';
    morePanels.style.display = 'none';
  }
}
function createPanelElement(panel) {
  const el = document.createElement('div');
  el.className = 'panel';
  if (panel.compact) el.classList.add('compact');
  if (panel.locked) el.classList.add('locked');
  if (panel.hidden) el.classList.add('hidden-panel');
  el.dataset.panelId = panel.id;
  el.style.gridColumn = `${panel.colStart} / span ${panel.colSpan}`;
  el.style.gridRow = `${panel.rowStart} / span ${panel.rowSpan}`;
  el.innerHTML = buildPanelInner(panel);
  el.querySelector('.lock-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleLock(panel.id);
  });
  el.querySelector('.compact-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleCompact(panel.id);
  });
  el.addEventListener('mousedown', (e) => {
    if (e.target.closest('button')) return;
    startDrag(e, panel.id);
  });
  el.addEventListener('click', (e) => {
    if (e.target.closest('button')) return;
    recordInteraction(panel.id);
  });
  const heatOverlay = el.querySelector('.heat-overlay');
  if (heatOverlay && showHeatmap) heatOverlay.classList.add('visible');
  return el;
}
function patchPanelElement(el, panel) {
  const wasCompact = el.classList.contains('compact');
  const wasLocked = el.classList.contains('locked');
  const wasHidden = el.classList.contains('hidden-panel');
  if (panel.compact !== wasCompact) el.classList.toggle('compact', panel.compact);
  if (panel.locked !== wasLocked) el.classList.toggle('locked', panel.locked);
  if (panel.hidden !== wasHidden) el.classList.toggle('hidden-panel', panel.hidden);
  const newGridCol = `${panel.colStart} / span ${panel.colSpan}`;
  const newGridRow = `${panel.rowStart} / span ${panel.rowSpan}`;
  if (el.style.gridColumn !== newGridCol) el.style.gridColumn = newGridCol;
  if (el.style.gridRow !== newGridRow) el.style.gridRow = newGridRow;
  const titleEl = el.querySelector('.panel-title');
  if (titleEl && titleEl.textContent !== panel.label) titleEl.textContent = panel.label;
  const valueEl = el.querySelector('.metric-value');
  if (valueEl && valueEl.textContent !== String(panel.value)) valueEl.textContent = panel.value;
  const unitEl = el.querySelector('.metric-label');
  if (unitEl) {
    const txt = panel.unit || '';
    if (unitEl.textContent !== txt) unitEl.textContent = txt;
  }
  const rankBadge = el.querySelector('.panel-rank-badge');
  if (rankBadge) {
    const rk = panel._rank !== undefined ? '#' + (panel._rank + 1) : '';
    if (rankBadge.textContent !== rk) rankBadge.textContent = rk;
  }
  const heatOverlay = el.querySelector('.heat-overlay');
  if (heatOverlay) {
    heatOverlay.classList.toggle('visible', showHeatmap);
    if (showHeatmap) {
      const score = getAttentionScore(panel.id);
      const maxScore = Math.max(1, ...panels.map(p => getAttentionScore(p.id)));
      const intensity = score / maxScore;
      heatOverlay.style.background = `rgba(108,140,255,${(intensity * 0.4).toFixed(2)})`;
      heatOverlay.style.opacity = intensity > 0.01 ? '1' : '0';
    } else {
      heatOverlay.style.opacity = '0';
    }
  }
}
function buildPanelInner(panel) {
  const score = getAttentionScore(panel.id);
  const maxScore = Math.max(1, ...panels.map(p => getAttentionScore(p.id)));
  const intensity = score / maxScore;
  const rankStr = panel._rank !== undefined ? '#' + (panel._rank + 1) : '';
  return `
    <div class="heat-overlay${showHeatmap ? ' visible' : ''}" style="background:rgba(108,140,255,${(intensity*0.4).toFixed(2)});opacity:${intensity>0.01?1:0}"></div>
    <div class="panel-header">
      <span class="panel-title">${panel.label}</span>
      <div class="panel-actions">
        <span class="lock-indicator" title="Locked">&#128274;</span>
        <button class="panel-action lock-btn" title="Lock position">&#128275;</button>
        <button class="panel-action compact-btn" title="Toggle compact">&#9636;</button>
      </div>
    </div>
    <div class="panel-body">
      <div style="text-align:center;">
        <div class="metric-value" style="color:${panel._rank===0?'var(--rank-1)':panel._rank===1?'var(--rank-2)':panel._rank===2?'var(--rank-3)':'var(--text)'}">${panel.value}</div>
        <div class="metric-label">${panel.unit || ''}</div>
      </div>
    </div>
    <div class="panel-preview">${panel.label}: ${panel.value}${panel.unit||''}</div>
    <div class="panel-rank-badge">${rankStr}</div>`;
}
function scheduleRecalc() {
  if (scheduleTimeout !== null) {
    clearTimeout(scheduleTimeout);
  }
  scheduleTimeout = setTimeout(() => {
    scheduleTimeout = null;
    applyLayout(true);
  }, RECALC_COOLDOWN);
  updateStats();
}
function toggleLock(panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  panel.locked = !panel.locked;
  if (panel.locked) {
    panel.userPosition = {
      colStart: panel.colStart,
      rowStart: panel.rowStart,
      colSpan: panel.colSpan,
      rowSpan: panel.rowSpan
    };
  } else {
    panel.userPosition = null;
  }
  recordInteraction(panelId);
  applyLayout(true);
}
function toggleCompact(panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  panel.compact = !panel.compact;
  panel.locked = true;
  recordInteraction(panelId);
  applyLayout(true);
}
function recordInteraction(panelId) {
  if (!attentionData[panelId]) {
    attentionData[panelId] = { viewCount: 0, totalDuration: 0, lastView: 0, interactions: 0 };
  }
  attentionData[panelId].interactions = (attentionData[panelId].interactions || 0) + 1;
  attentionData[panelId].lastView = now();
  scheduleRecalc();
}
function startViewTimer(panelId) {
  if (viewTimers[panelId]) return;
  viewTimers[panelId] = now();
}
function stopViewTimer(panelId) {
  if (!viewTimers[panelId]) return;
  const duration = now() - viewTimers[panelId];
  delete viewTimers[panelId];
  if (!attentionData[panelId]) {
    attentionData[panelId] = { viewCount: 0, totalDuration: 0, lastView: 0, interactions: 0 };
  }
  attentionData[panelId].totalDuration = (attentionData[panelId].totalDuration || 0) + duration;
  attentionData[panelId].viewCount = (attentionData[panelId].viewCount || 0) + 1;
  attentionData[panelId].lastView = now();
}
function setupObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const id = entry.target.dataset.panelId;
      if (!id) return;
      if (entry.isIntersecting) {
        startViewTimer(id);
      } else {
        stopViewTimer(id);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.panel').forEach(el => {
    el.dataset.observed = '1';
    observer.observe(el);
  });
}
function startDrag(e, panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  e.preventDefault();
  const el = document.querySelector(`[data-panel-id="${panelId}"]`);
  if (!el) return;
  const rect = el.getBoundingClientRect();
  dragOffset = { x: e.clientX - rect.left, y: e.clientY - rect.top };
  dragStartPos = { colStart: panel.colStart, rowStart: panel.rowStart };
  dragging = { id: panelId, el: el };
  dragClone = el.cloneNode(true);
  dragClone.style.position = 'fixed';
  dragClone.style.zIndex = '999';
  dragClone.style.pointerEvents = 'none';
  dragClone.style.width = rect.width + 'px';
  dragClone.style.height = rect.height + 'px';
  dragClone.style.left = rect.left + 'px';
  dragClone.style.top = rect.top + 'px';
  dragClone.style.margin = '0';
  dragClone.style.opacity = '0.85';
  dragClone.style.boxShadow = '0 12px 40px rgba(0,0,0,0.6)';
  dragClone.style.transition = 'none';
  document.body.appendChild(dragClone);
  el.style.opacity = '0.3';
  el.classList.add('dragging');
  document.addEventListener('mousemove', onDragMove);
  document.addEventListener('mouseup', onDragEnd);
}
function onDragMove(e) {
  if (!dragging || !dragClone) return;
  dragClone.style.left = (e.clientX - dragOffset.x) + 'px';
  dragClone.style.top = (e.clientY - dragOffset.y) + 'px';
}
function onDragEnd(e) {
  document.removeEventListener('mousemove', onDragMove);
  document.removeEventListener('mouseup', onDragEnd);
  if (!dragging) return;
  const panel = panels.find(p => p.id === dragging.id);
  const el = dragging.el;
  if (el) {
    el.style.opacity = '';
    el.classList.remove('dragging');
  }
  if (dragClone && dragClone.parentNode) {
    dragClone.remove();
  }
  dragClone = null;
  const grid = document.getElementById('grid');
  const gridRect = grid.getBoundingClientRect();
  const cx = e.clientX;
  const cy = e.clientY;
  if (cx < gridRect.left || cx > gridRect.right || cy < gridRect.top || cy > gridRect.bottom) {
    dragging = null;
    return;
  }
  const relX = cx - gridRect.left;
  const relY = cy - gridRect.top;
  const cellW = (gridRect.width - GAP * (COLS - 1)) / COLS;
  const cellH = GRID_ROW_HEIGHT;
  const col = Math.min(COLS, Math.max(1, Math.floor(relX / (cellW + GAP)) + 1));
  const row = Math.max(1, Math.floor(relY / (cellH + GAP)) + 1);
  if (panel) {
    panel.colStart = Math.min(col, COLS - panel.colSpan + 1);
    panel.rowStart = row;
    panel.locked = true;
    panel.userPosition = {
      colStart: panel.colStart,
      rowStart: panel.rowStart,
      colSpan: panel.colSpan,
      rowSpan: panel.rowSpan
    };
    recordInteraction(panel.id);
  }
  dragging = null;
  applyLayout(true);
}
function updateStats() {
  const totalViews = Object.values(attentionData).reduce((s, d) => s + (d.viewCount || 0), 0);
  const lockedCount = panels.filter(p => p.locked).length;
  const compactCount = panels.filter(p => p.compact && !p.hidden).length;
  document.getElementById('stat-views').textContent = totalViews;
  document.getElementById('stat-locked').textContent = lockedCount;
  document.getElementById('stat-compact').textContent = compactCount;
  if (scheduleTimeout) {
    document.getElementById('stat-next').textContent = '~' + Math.ceil(RECALC_COOLDOWN / 1000) + 's';
  } else {
    document.getElementById('stat-next').textContent = 'idle';
  }
}
function updateHeatmap() {
  document.querySelectorAll('.panel .heat-overlay').forEach(overlay => {
    const el = overlay.closest('.panel');
    if (!el) return;
    const id = el.dataset.panelId;
    if (!id) return;
    if (showHeatmap) {
      overlay.classList.add('visible');
      const score = getAttentionScore(id);
      const maxScore = Math.max(1, ...panels.map(p => getAttentionScore(p.id)));
      const intensity = score / maxScore;
      overlay.style.background = `rgba(108,140,255,${(intensity * 0.4).toFixed(2)})`;
      overlay.style.opacity = intensity > 0.01 ? '1' : '0';
    } else {
      overlay.classList.remove('visible');
      overlay.style.opacity = '0';
    }
  });
}
function toggleAutoLayout() {
  isAutoLayout = !isAutoLayout;
  const btn = document.getElementById('auto-layout-toggle');
  btn.textContent = 'Auto: ' + (isAutoLayout ? 'ON' : 'OFF');
  if (isAutoLayout) {
    btn.classList.add('active');
    applyLayout(true);
  } else {
    btn.classList.remove('active');
  }
  saveState();
}
function resetAll() {
  attentionData = {};
  initPanels();
  document.getElementById('stat-sessions').textContent = '1';
  applyLayout(false);
}
document.getElementById('auto-layout-toggle').addEventListener('click', toggleAutoLayout);
document.getElementById('reset-btn').addEventListener('click', resetAll);
document.getElementById('heatmap-toggle').addEventListener('click', function() {
  showHeatmap = !showHeatmap;
  this.classList.toggle('active', showHeatmap);
  updateHeatmap();
});
document.getElementById('more-toggle').addEventListener('click', function() {
  moreExpanded = !moreExpanded;
  const morePanels = document.getElementById('more-panels');
  if (moreExpanded) {
    morePanels.style.display = '';
    const hidden = panels.filter(p => p.hidden);
    const frag = document.createDocumentFragment();
    hidden.forEach(panel => {
      const el = createPanelElement(panel);
      frag.appendChild(el);
    });
    morePanels.appendChild(frag);
    if (observer) {
      morePanels.querySelectorAll('.panel').forEach(el => {
        if (!el.dataset.observed) { observer.observe(el); el.dataset.observed = '1'; }
      });
    }
  } else {
    morePanels.querySelectorAll('.panel').forEach(el => {
      if (observer) observer.unobserve(el);
      el.remove();
    });
    morePanels.style.display = 'none';
  }
});
window.addEventListener('beforeunload', () => {
  Object.keys(viewTimers).forEach(id => stopViewTimer(id));
  saveState();
});
loadState();
if (!document.getElementById('auto-layout-toggle').classList.contains('active') && isAutoLayout) {
  document.getElementById('auto-layout-toggle').classList.add('active');
}
if (!isAutoLayout) {
  document.getElementById('auto-layout-toggle').classList.remove('active');
}
applyLayout(false);
setupObserver();
})();
</script>
</body>
</html>