<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --card-bg: #1a1d27;
  --card-bg-compact: #14161e;
  --border: #2a2d3a;
  --text: #e1e4ea;
  --text-dim: #8b8fa3;
  --accent: #6366f1;
  --accent-glow: rgba(99,102,241,0.15);
  --up: #22c55e;
  --down: #ef4444;
  --radius: 12px;
  --gap: 12px;
  --transition: 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
  padding: 20px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}
h1 {
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
.controls button {
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text-dim);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
  font-family: inherit;
}
.controls button:hover {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.controls button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(200px, auto);
  gap: var(--gap);
  transition: all var(--transition);
}
.panel {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
  cursor: default;
}
.panel::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  z-index: 0;
}
.panel.high-rank::before {
  background: linear-gradient(135deg, var(--accent-glow), transparent 60%);
  opacity: 1;
}
.panel.compact {
  grid-row: span 1 !important;
  grid-column: span 1 !important;
  padding: 14px 16px;
  gap: 6px;
  background: var(--card-bg-compact);
  font-size: 0.8rem;
}
.panel.compact .panel-body,
.panel.compact .panel-chart,
.panel.compact .rank-badge { display: none; }
.panel.compact .panel-header { margin-bottom: 0; }
.panel.compact .panel-value { font-size: 1.1rem; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1;
}
.panel-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-dim);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.rank-badge {
  background: var(--accent);
  color: #fff;
  font-size: 0.6rem;
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: 700;
}
.panel-actions {
  display: flex;
  gap: 4px;
  z-index: 1;
}
.panel-actions button {
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-dim);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.panel-actions button:hover { background: rgba(255,255,255,0.05); color: var(--text); }
.panel-actions button.locked { color: #f59e0b; border-color: #f59e0b40; background: #f59e0b10; }
.panel-body { z-index: 1; }
.panel-value {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
}
.panel-delta {
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.panel-delta.up { color: var(--up); }
.panel-delta.down { color: var(--down); }
.score-details {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 0.65rem;
  color: var(--text-dim);
  z-index: 1;
  opacity: 0.5;
}
.panel-chart {
  flex: 1;
  min-height: 40px;
  z-index: 1;
}
.sparkline {
  width: 100%;
  height: 100%;
  min-height: 40px;
}
.sparkline path { fill: none; stroke-width: 2; stroke-linecap: round; }
.sparkline path.line { stroke: var(--accent); opacity: 0.6; }
.sparkline path.area { fill: url(#grad); opacity: 0.08; }
.panel.dragging {
  opacity: 0.6;
  transform: scale(0.95);
  z-index: 10;
}
.drag-handle {
  cursor: grab;
  opacity: 0;
  transition: opacity 0.2s;
  font-size: 1rem;
}
.panel:hover .drag-handle { opacity: 0.5; }
.panel:hover .drag-handle:hover { opacity: 1; }
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--card-bg);
  border: 1px solid var(--accent);
  color: var(--text);
  padding: 12px 20px;
  border-radius: var(--radius);
  font-size: 0.8rem;
  z-index: 100;
  transform: translateX(120%);
  transition: transform 0.3s;
  pointer-events: none;
}
.notification.show { transform: translateX(0); }
@media (max-width: 900px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) {
  .grid { grid-template-columns: 1fr; }
  .panel.compact { grid-column: span 1 !important; }
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button id="btnAuto" class="active" title="Auto-layout enabled">Auto</button>
    <button id="btnReset" title="Reset all tracking data">Reset</button>
    <button id="btnExport" title="Export layout">Export</button>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="notification" id="notification"></div>
<svg style="position:absolute;width:0;height:0" aria-hidden="true">
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
    </linearGradient>
  </defs>
</svg>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const DECAY_HALF = 3600000; // 1 hour in ms
const RESCORE_INTERVAL = 10000; // rescore every 10s
const VIEW_SAMPLE_RATE = 2000; // sample view time every 2s
let panels = [];
let viewIntervals = {};
let autoLayout = true;
let rescoreTimer = null;
// --- DATA ---
const DEFAULT_PANELS = [
  { id: 'revenue',        title: 'Revenue',       value: '$24,780', delta: '+12.5%', sparkline: genData(14, 20, 5) },
  { id: 'users',          title: 'Active Users',  value: '8,492',   delta: '+8.3%',  sparkline: genData(14, 5, 2) },
  { id: 'conversion',     title: 'Conversion',    value: '3.24%',   delta: '-0.8%',  sparkline: genData(14, 3, 1) },
  { id: 'bounce',         title: 'Bounce Rate',   value: '42.1%',   delta: '+2.1%',  sparkline: genData(14, 40, 5) },
  { id: 'session',        title: 'Session Time',  value: '4m 32s',  delta: '+15s',    sparkline: genData(14, 200, 30) },
  { id: 'retention',      title: 'Retention',     value: '68.5%',   delta: '+1.2%',  sparkline: genData(14, 60, 8) },
  { id: 'latency',        title: 'API Latency',   value: '142ms',   delta: '-18ms',   sparkline: genData(14, 140, 25) },
  { id: 'errors',         title: 'Error Rate',    value: '0.12%',   delta: '-0.03%', sparkline: genData(14, 0.1, 0.05) },
];
function genData(n, base, variance) {
  const d = [];
  for (let i = 0; i < n; i++) d.push(base + (Math.random() - 0.5) * variance * 2);
  return d;
}
// --- STORAGE ---
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch (e) { return null; }
}
function saveState() {
  const state = {
    panels: panels.map(p => ({
      id: p.id,
      freq: p.freq,
      duration: p.duration,
      lastInteraction: p.lastInteraction,
      locked: p.locked,
      compact: p.compact,
      manualPos: p.manualPos
    })),
    autoLayout,
    version: 1
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}
// --- SCORING ---
function computeScore(p) {
  const now = Date.now();
  const recency = Math.exp(-(now - p.lastInteraction) / DECAY_HALF);
  return p.freq * Math.max(p.duration / 1000, 1) * recency;
}
function rescore() {
  const now = Date.now();
  panels.forEach(p => {
    p.score = computeScore(p);
    p.age = now - p.lastInteraction;
  });
  const sorted = [...panels].sort((a, b) => b.score - a.score);
  sorted.forEach((p, i) => { p.rank = i + 1; });
}
// --- NUMERIC DELTA PARSING ---
function parseDeltaNumeric(deltaStr) {
  const num = parseFloat(deltaStr.replace(/[^0-9.\-]/g, ''));
  return isNaN(num) ? 0 : num;
}
function getDeltaClass(deltaStr) {
  const n = parseDeltaNumeric(deltaStr);
  if (n > 0) return 'up';
  if (n < 0) return 'down';
  return '';
}
// --- DOM ---
const grid = document.getElementById('grid');
const notification = document.getElementById('notification');
function notify(msg) {
  notification.textContent = msg;
  notification.classList.add('show');
  clearTimeout(notification._t);
  notification._t = setTimeout(() => notification.classList.remove('show'), 2500);
}
function createPanel(p) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.id = p.id;
  const deltaNum = parseDeltaNumeric(p.delta);
  const deltaClass = deltaNum > 0 ? 'up' : deltaNum < 0 ? 'down' : '';
  el.innerHTML =
    '<div class="panel-header">' +
      '<span class="panel-title">' +
        '<span class="drag-handle" title="Drag to reposition">⠿</span>' +
        p.title +
        '<span class="rank-badge" data-rank="rank">#' + (p.rank || '?') + '</span>' +
      '</span>' +
      '<div class="panel-actions">' +
        '<button class="btn-lock' + (p.locked ? ' locked' : '') + '" title="Lock position">🔒</button>' +
        '<button class="btn-compact' + (p.compact ? ' active' : '') + '" title="Toggle compact">⊟</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' +
      '<div class="panel-value" data-value="value">' + p.value + '</div>' +
      '<div class="panel-delta ' + deltaClass + '" data-delta="delta">' +
        (deltaNum >= 0 ? '▲' : '▼') + ' ' + p.delta +
      '</div>' +
    '</div>' +
    '<div class="score-details" data-score="score">' +
      '<span>Freq: ' + p.freq + '</span>' +
      '<span>Dur: ' + formatDuration(p.duration) + '</span>' +
      '<span>Score: ' + (p.score || 0).toFixed(1) + '</span>' +
    '</div>' +
    '<div class="panel-chart"><svg class="sparkline" viewBox="0 0 200 40" preserveAspectRatio="none"></svg></div>';
  // Sparkline
  requestAnimationFrame(() => {
    const svg = el.querySelector('.sparkline');
    if (!svg || !p.sparkline || !p.sparkline.length) return;
    const w = 200, h = 40, pad = 2;
    const data = p.sparkline;
    const min = Math.min(...data), max = Math.max(...data), range = max - min || 1;
    const points = data.map((v, i) => {
      const x = pad + (i / (data.length - 1)) * (w - pad * 2);
      const y = h - pad - ((v - min) / range) * (h - pad * 2);
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    const areaD = 'M' + points.split(' ')[0] + ' L' + points + ' L' +
      (w - pad).toFixed(1) + ',' + (h - pad).toFixed(1) + ' L' + pad.toFixed(1) + ',' + (h - pad).toFixed(1) + 'Z';
    svg.innerHTML =
      '<path class="area" d="' + areaD + '"/>' +
      '<path class="line" d="M' + points + '"/>';
  });
  // Event handlers
  el.addEventListener('mouseenter', () => recordInteraction(p.id, 'hover'));
  el.addEventListener('click', (e) => {
    if (e.target.closest('button')) return;
    recordInteraction(p.id, 'click');
  });
  // Lock button
  const btnLock = el.querySelector('.btn-lock');
  btnLock.addEventListener('click', (e) => {
    e.stopPropagation();
    p.locked = !p.locked;
    if (p.locked) {
      p.manualPos = panels.indexOf(p);
    } else {
      p.manualPos = null;
    }
    updatePanelDOM(p, el);
    if (autoLayout) applyLayout();
    saveState();
    notify(p.locked ? p.title + ' locked' : p.title + ' unlocked');
  });
  // Compact button
  const btnCompact = el.querySelector('.btn-compact');
  btnCompact.addEventListener('click', (e) => {
    e.stopPropagation();
    p.compact = !p.compact;
    updatePanelDOM(p, el);
    if (autoLayout) applyLayout();
    saveState();
  });
  // Drag
  const handle = el.querySelector('.drag-handle');
  handle.addEventListener('mousedown', (e) => {
    e.preventDefault();
    startDrag(p, el, e);
  });
  p._el = el;
  return el;
}
function updatePanelDOM(p, el) {
  if (!el) el = p._el;
  if (!el) return;
  // Targeted updates - never replace innerHTML
  const rankBadge = el.querySelector('[data-rank]');
  if (rankBadge && p.rank) rankBadge.textContent = '#' + p.rank;
  const scoreEl = el.querySelector('[data-score]');
  if (scoreEl) {
    scoreEl.innerHTML =
      '<span>Freq: ' + p.freq + '</span>' +
      '<span>Dur: ' + formatDuration(p.duration) + '</span>' +
      '<span>Score: ' + (p.score || 0).toFixed(1) + '</span>';
  }
  const btnLock = el.querySelector('.btn-lock');
  if (btnLock) {
    btnLock.classList.toggle('locked', p.locked);
    btnLock.title = p.locked ? 'Unlock position' : 'Lock position';
  }
  const btnCompact = el.querySelector('.btn-compact');
  if (btnCompact) {
    btnCompact.classList.toggle('active', p.compact);
    btnCompact.title = p.compact ? 'Expand' : 'Compact';
  }
  el.classList.toggle('compact', p.compact);
  el.classList.toggle('high-rank', p.rank <= 3 && !p.compact);
}
function formatDuration(ms) {
  if (ms < 1000) return '0s';
  if (ms < 60000) return Math.round(ms / 1000) + 's';
  return Math.round(ms / 60000) + 'm';
}
// --- LAYOUT ---
function applyLayout() {
  if (!autoLayout) return;
  rescore();
  const unlocked = panels.filter(p => !p.locked);
  const locked = panels.filter(p => p.locked);
  const sorted = [...unlocked].sort((a, b) => b.score - a.score);
  // Assign grid positions to unlocked panels
  sorted.forEach((p, i) => {
    if (i === 0) { p._span = 'span 2 / span 2'; p._row = 'span 2'; }
    else if (i === 1) { p._span = 'span 2 / span 2'; p._row = 'span 2'; }
    else if (i <= 3) { p._span = 'span 1 / span 1'; p._row = 'span 1'; }
    else { p._span = 'span 1 / span 1'; p._row = 'span 1'; }
  });
  // Apply compact mode based on rank
  panels.forEach(p => {
    if (!p.locked && p.rank > 6) p.compact = true;
    else if (!p.locked && p.rank <= 2) p.compact = false;
  });
  // Build final order: locked first (at manual positions), then sorted unlocked
  const ordered = [];
  const usedSlots = new Set();
  locked.forEach(p => {
    const pos = p.manualPos || 0;
    ordered[pos] = p;
    usedSlots.add(pos);
  });
  let ui = 0;
  sorted.forEach(p => {
    while (ordered[ui] !== undefined) ui++;
    ordered[ui] = p;
    ui++;
  });
  // Re-render grid children in order
  const fragment = document.createDocumentFragment();
  const existing = new Map();
  grid.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.id, el));
  ordered.forEach((p, i) => {
    let el = p._el || existing.get(p.id);
    if (!el) {
      el = createPanel(p);
      p._el = el;
    }
    updatePanelDOM(p, el);
    // Targeted style updates (not full re-render)
    if (!p.compact) {
      el.style.gridColumn = (i === 0 || i === 1) ? 'span 2' : 'span 1';
      el.style.gridRow = (i === 0 || i === 1) ? 'span 2' : 'span 1';
    } else {
      el.style.gridColumn = 'span 1';
      el.style.gridRow = 'span 1';
    }
    fragment.appendChild(el);
  });
  grid.innerHTML = '';
  grid.appendChild(fragment);
  saveState();
}
// --- TRACKING ---
function recordInteraction(id, type) {
  const p = panels.find(p => p.id === id);
  if (!p) return;
  p.freq = (p.freq || 0) + 1;
  p.lastInteraction = Date.now();
  // Targeted score update for the single panel
  p.score = computeScore(p);
  rescore();
  updatePanelDOM(p);
}
function startViewTracking(p) {
  if (viewIntervals[p.id]) return;
  viewIntervals[p.id] = setInterval(() => {
    p.duration = (p.duration || 0) + VIEW_SAMPLE_RATE;
    // Targeted update - just the score details node
    updatePanelDOM(p);
  }, VIEW_SAMPLE_RATE);
}
function stopViewTracking(p) {
  if (viewIntervals[p.id]) {
    clearInterval(viewIntervals[p.id]);
    delete viewIntervals[p.id];
  }
}
// Intersection Observer for view tracking
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const id = entry.target.dataset.id;
    const p = panels.find(p => p.id === id);
    if (!p) return;
    if (entry.isIntersecting) {
      startViewTracking(p);
    } else {
      stopViewTracking(p);
    }
  });
}, { threshold: 0.5 });
// --- DRAG ---
let dragState = null;
function startDrag(p, el, e) {
  if (p.locked) return;
  dragState = { p, el, startX: e.clientX, startY: e.clientY, originalIdx: panels.indexOf(p) };
  el.classList.add('dragging');
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
}
function onDrag(e) {
  if (!dragState) return;
  // Lightweight visual feedback only
  const dx = e.clientX - dragState.startX;
  const dy = e.clientY - dragState.startY;
  dragState.el.style.transform = 'translate(' + dx + 'px, ' + dy + 'px) scale(1.02)';
}
function stopDrag(e) {
  if (!dragState) return;
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
  dragState.el.classList.remove('dragging');
  dragState.el.style.transform = '';
  const dx = e.clientX - dragState.startX;
  const dy = e.clientY - dragState.startY;
  const dist = Math.sqrt(dx * dx + dy * dy);
  if (dist > 30) {
    // Determine drop target by elementFromPoint
    dragState.el.style.display = 'none';
    const target = document.elementFromPoint(e.clientX, e.clientY);
    dragState.el.style.display = '';
    const targetPanel = target ? target.closest('.panel') : null;
    if (targetPanel && targetPanel !== dragState.el) {
      const targetId = targetPanel.dataset.id;
      const targetP = panels.find(p => p.id === targetId);
      const fromIdx = panels.indexOf(dragState.p);
      const toIdx = panels.indexOf(targetP);
      if (fromIdx !== -1 && toIdx !== -1) {
        panels.splice(fromIdx, 1);
        panels.splice(toIdx, 0, dragState.p);
        dragState.p.locked = true;
        dragState.p.manualPos = toIdx;
        updatePanelDOM(dragState.p);
        applyLayout();
        saveState();
        notify(dragState.p.title + ' moved, position locked');
      }
    }
  }
  dragState = null;
}
// --- BUTTONS ---
document.getElementById('btnAuto').addEventListener('click', function() {
  autoLayout = !autoLayout;
  this.classList.toggle('active', autoLayout);
  this.textContent = autoLayout ? 'Auto' : 'Manual';
  if (autoLayout) {
    panels.forEach(p => { p.locked = false; p.manualPos = null; });
    applyLayout();
  }
  saveState();
  notify(autoLayout ? 'Auto-layout enabled' : 'Manual mode — drag to arrange');
});
document.getElementById('btnReset').addEventListener('click', () => {
  panels.forEach(p => {
    p.freq = 0;
    p.duration = 0;
    p.lastInteraction = Date.now() - DECAY_HALF * 2;
    p.locked = false;
    p.manualPos = null;
    p.compact = false;
  });
  rescore();
  applyLayout();
  saveState();
  notify('Tracking data reset');
});
document.getElementById('btnExport').addEventListener('click', () => {
  const data = JSON.stringify({
    panels: panels.map(p => ({
      id: p.id, title: p.title, freq: p.freq, duration: p.duration,
      score: p.score, rank: p.rank, locked: p.locked, compact: p.compact
    })),
    autoLayout
  }, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'dashboard-layout-' + new Date().toISOString().slice(0, 10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
  notify('Layout exported');
});
// --- INIT ---
function init() {
  const saved = loadState();
  panels = DEFAULT_PANELS.map((d, i) => {
    const savedPanel = saved ? saved.panels.find(sp => sp.id === d.id) : null;
    return {
      ...d,
      freq: (savedPanel && savedPanel.freq) || 0,
      duration: (savedPanel && savedPanel.duration) || 0,
      lastInteraction: (savedPanel && savedPanel.lastInteraction) || Date.now() - DECAY_HALF * 2,
      locked: (savedPanel && savedPanel.locked) || false,
      compact: (savedPanel && savedPanel.compact) || false,
      manualPos: (savedPanel && savedPanel.manualPos) || null,
      score: 0,
      rank: i + 1
    };
  });
  if (saved && saved.autoLayout !== undefined) autoLayout = saved.autoLayout;
  document.getElementById('btnAuto').classList.toggle('active', autoLayout);
  document.getElementById('btnAuto').textContent = autoLayout ? 'Auto' : 'Manual';
  rescore();
  renderAll();
  startRescoreTimer();
  notify('Dashboard ready — ' + panels.length + ' panels tracking');
}
function renderAll() {
  grid.innerHTML = '';
  panels.forEach(p => {
    const el = createPanel(p);
    p._el = el;
    grid.appendChild(el);
    updatePanelDOM(p, el);
    observer.observe(el);
  });
  applyLayout();
}
function startRescoreTimer() {
  if (rescoreTimer) clearInterval(rescoreTimer);
  rescoreTimer = setInterval(() => {
    if (!autoLayout) return;
    rescore();
    // Targeted rank badge updates only
    panels.forEach(p => {
      const el = p._el;
      if (!el) return;
      const badge = el.querySelector('.rank-badge');
      if (badge && badge.textContent !== '#' + p.rank) {
        badge.textContent = '#' + p.rank;
      }
      // Update high-rank class (targeted)
      const wasHigh = el.classList.contains('high-rank');
      const shouldBeHigh = p.rank <= 3 && !p.compact;
      if (wasHigh !== shouldBeHigh) el.classList.toggle('high-rank', shouldBeHigh);
    });
    // Re-apply layout if scores shifted significantly
    applyLayout();
  }, RESCORE_INTERVAL);
}
init();
})();
</script>
</body>
</html>