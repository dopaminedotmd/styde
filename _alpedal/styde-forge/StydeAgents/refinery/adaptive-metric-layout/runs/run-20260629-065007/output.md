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
  --surface-hover: #22263a;
  --border: #2a2e3d;
  --text: #e1e4ed;
  --text-dim: #8b90a5;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --heat-high: #ff4757;
  --heat-mid: #ffa502;
  --heat-low: #2ed573;
  --heat-cold: #3742fa;
  --compact-size: 120px;
  --radius: 10px;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  min-height: 100vh;
  padding: 16px;
  user-select: none;
}
.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 12px 18px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.toolbar h1 {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-right: auto;
  white-space: nowrap;
}
.toolbar .badge {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 12px;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  white-space: nowrap;
}
.btn {
  padding: 7px 14px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  border-radius: 7px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: var(--transition);
  white-space: nowrap;
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.dashboard {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(8, 1fr);
  grid-auto-rows: minmax(140px, auto);
  transition: grid-template-columns var(--transition), grid-template-rows var(--transition);
}
.panel {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  cursor: grab;
  transition: all var(--transition);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 140px;
}
.panel:hover { border-color: var(--accent); background: var(--surface-hover); }
.panel.locked { cursor: default; border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent-glow); }
.panel.compact { min-height: var(--compact-size); padding: 10px 14px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.dragging { opacity: 0.6; z-index: 10; }
.panel.drag-over { border-color: var(--accent); box-shadow: inset 0 0 0 2px var(--accent-glow); }
.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.panel.compact .panel-header { margin-bottom: 4px; }
.panel-icon { font-size: 18px; line-height: 1; }
.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-dim);
  letter-spacing: 0.2px;
  flex: 1;
}
.panel-rank {
  font-size: 10px;
  padding: 2px 7px;
  border-radius: 9px;
  background: var(--border);
  color: var(--text-dim);
  font-weight: 600;
}
.panel-score-bar {
  position: absolute;
  top: 0; left: 0;
  height: 3px;
  background: var(--accent);
  border-radius: var(--radius) var(--radius) 0 0;
  transition: width 0.6s ease;
}
.panel-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}
.panel-body .metric-unit { font-size: 13px; font-weight: 400; color: var(--text-dim); margin-left: 4px; }
.panel-body .sparkline {
  width: 100%;
  height: 48px;
  margin-top: 8px;
}
.panel-body .sparkline svg { width: 100%; height: 100%; }
.panel-preview {
  display: none;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-dim);
}
.panel-actions {
  display: flex;
  gap: 4px;
  position: absolute;
  top: 10px;
  right: 14px;
  opacity: 0;
  transition: opacity 0.2s;
}
.panel:hover .panel-actions, .panel.locked .panel-actions { opacity: 1; }
.panel-actions button {
  width: 26px; height: 26px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-dim);
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}
.panel-actions button:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
.panel-actions button.lock-btn.locked { background: var(--accent); color: #fff; }
.heatmap-overlay .panel::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius);
  pointer-events: none;
  transition: background 0.5s ease;
}
.heatmap-overlay .panel.heat-high::after { background: rgba(255,71,87,0.18); }
.heatmap-overlay .panel.heat-mid::after { background: rgba(255,165,2,0.14); }
.heatmap-overlay .panel.heat-low::after { background: rgba(46,213,115,0.10); }
.heatmap-overlay .panel.heat-cold::after { background: rgba(55,66,250,0.06); }
.heatmap-legend {
  display: none;
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  gap: 8px;
  font-size: 11px;
  z-index: 100;
}
.heatmap-overlay .heatmap-legend { display: flex; align-items: center; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.stats-bar {
  display: flex;
  gap: 16px;
  padding: 8px 18px;
  font-size: 11px;
  color: var(--text-dim);
}
@keyframes pulse {
  0%,100% { opacity:1; }
  50% { opacity:0.5; }
}
.recording-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #ff4757;
  animation: pulse 1.5s infinite;
  display: inline-block;
  margin-right: 4px;
}
@media (max-width: 900px) {
  .dashboard { grid-template-columns: repeat(4, 1fr) !important; }
}
@media (max-width: 500px) {
  .dashboard { grid-template-columns: repeat(2, 1fr) !important; }
  .panel { min-height: 110px; }
  .panel.compact { min-height: 90px; }
}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <span class="badge"><span class="recording-dot"></span>Tracking</span>
  <button class="btn" id="btnHeatmap" title="Toggle attention heatmap overlay">Heatmap</button>
  <button class="btn" id="btnReset" title="Reset all tracking data and layout">Reset</button>
  <span id="statusText" style="font-size:11px;color:var(--text-dim)"></span>
</div>
<div class="stats-bar" id="statsBar"></div>
<div class="dashboard" id="dashboard"></div>
<div class="heatmap-legend">
  <span><span class="legend-dot" style="background:var(--heat-high)"></span> High</span>
  <span><span class="legend-dot" style="background:var(--heat-mid)"></span> Medium</span>
  <span><span class="legend-dot" style="background:var(--heat-low)"></span> Low</span>
  <span><span class="legend-dot" style="background:var(--heat-cold)"></span> Cold</span>
</div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const IDLE_TIMEOUT = 5000;
const DECAY_HALF_LIFE = 7 * 24 * 3600 * 1000; // 7 days in ms
const COMPACT_THRESHOLD = 0.15; // bottom 15% of scores get compacted
const MIN_VISIBILITY_RATIO = 0.5;
const METRICS = [
  { id: 'cpu', icon: '⚙', title: 'CPU Usage', unit: '%', value: () => 20 + Math.random() * 60, color: '#6c8cff' },
  { id: 'memory', icon: '🧠', title: 'Memory', unit: 'GB', value: () => 4 + Math.random() * 12, color: '#ff6b81' },
  { id: 'network', icon: '🌐', title: 'Network I/O', unit: 'MB/s', value: () => Math.random() * 800, color: '#2ed573' },
  { id: 'errors', icon: '⚠', title: 'Error Rate', unit: '%', value: () => Math.random() * 5, color: '#ffa502' },
  { id: 'users', icon: '👥', title: 'Active Users', unit: '', value: () => Math.floor(Math.random() * 12000), color: '#a55eea' },
  { id: 'revenue', icon: '💰', title: 'Revenue', unit: 'kr/h', value: () => Math.floor(Math.random() * 50000), color: '#26de81' },
  { id: 'latency', icon: '⏱', title: 'P95 Latency', unit: 'ms', value: () => 40 + Math.random() * 200, color: '#fd9644' },
  { id: 'requests', icon: '📡', title: 'Requests/s', unit: '', value: () => Math.floor(Math.random() * 4500), color: '#45aaf2' },
  { id: 'disk', icon: '💾', title: 'Disk Usage', unit: '%', value: () => 30 + Math.random() * 50, color: '#fc5c65' },
  { id: 'cache', icon: '⚡', title: 'Cache Hit Rate', unit: '%', value: () => 70 + Math.random() * 28, color: '#f7b731' },
  { id: 'uptime', icon: '🟢', title: 'Uptime', unit: '%', value: () => 99.9 + Math.random() * 0.09, color: '#20bf6b' },
  { id: 'threads', icon: '🧵', title: 'Active Threads', unit: '', value: () => Math.floor(Math.random() * 200), color: '#8854d0' }
];
let panels = [];
let panelData = new Map(); // id -> { viewMs, interactions, lastSeen, locked, userPosition, compact, }
let idleTimer = null;
let isIdle = false;
let heatmapActive = false;
let visibilityObserver = null;
let resizeObserver = null;
let activeVisiblePanels = new Set();
let visibilityEntries = new Map(); // id -> { enterTime, ratio }
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      if (saved.panelData && typeof saved.panelData === 'object') {
        for (const [id, data] of Object.entries(saved.panelData)) {
          panelData.set(id, {
            viewMs: data.viewMs || 0,
            interactions: data.interactions || 0,
            lastSeen: data.lastSeen || 0,
            locked: !!data.locked,
            userPosition: data.userPosition ?? null,
            compact: !!data.compact
          });
        }
      }
      if (typeof saved.heatmapActive === 'boolean') heatmapActive = saved.heatmapActive;
    }
  } catch(e) { /* corrupted data, start fresh */ }
}
function saveState() {
  const obj = {};
  for (const [id, data] of panelData) {
    obj[id] = {
      viewMs: data.viewMs,
      interactions: data.interactions,
      lastSeen: data.lastSeen,
      locked: data.locked,
      userPosition: data.userPosition,
      compact: data.compact
    };
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    panelData: obj,
    heatmapActive
  }));
}
function ensurePanelData(id) {
  if (!panelData.has(id)) {
    panelData.set(id, {
      viewMs: 0,
      interactions: 0,
      lastSeen: 0,
      locked: false,
      userPosition: null,
      compact: false
    });
  }
}
function computeScore(data, now) {
  const recencyHours = Math.max(0, (now - data.lastSeen)) / 3600000;
  const recencyFactor = Math.exp(-recencyHours * Math.LN2 / (DECAY_HALF_LIFE / 3600000));
  const viewMinutes = data.viewMs / 60000;
  const interactionWeight = 1 + Math.log1p(data.interactions);
  return viewMinutes * interactionWeight * recencyFactor;
}
function rankPanels() {
  const now = Date.now();
  const scored = METRICS.map(m => {
    ensurePanelData(m.id);
    const data = panelData.get(m.id);
    return { id: m.id, score: computeScore(data, now), locked: data.locked, userPosition: data.userPosition, compact: data.compact };
  });
  scored.sort((a, b) => b.score - a.score);
  const scores = scored.map(s => s.score);
  const maxScore = Math.max(...scores, 0.001);
  const threshold = maxScore * COMPACT_THRESHOLD;
  const ranked = [];
  let lockCount = 0;
  const lockedItems = [];
  const unlockedItems = [];
  for (const s of scored) {
    if (s.locked) {
      lockedItems.push(s);
    } else {
      unlockedItems.push(s);
    }
  }
  unlockedItems.forEach((s, i) => {
    const autoRank = i + 1;
    const shouldCompact = s.score < threshold && autoRank > 3;
    ranked.push({ ...s, rank: autoRank, autoCompact: shouldCompact });
  });
  lockedItems.forEach((s, i) => {
    ranked.push({ ...s, rank: unlockedItems.length + i + 1, autoCompact: false });
  });
  return ranked;
}
function getGridPlacement(rank, total, locked, userPosition) {
  if (locked && userPosition !== null) {
    return userPosition;
  }
  if (rank === 1) return { colSpan: 3, rowSpan: 2 };
  if (rank === 2) return { colSpan: 3, rowSpan: 1 };
  if (rank <= 4) return { colSpan: 2, rowSpan: 1 };
  if (rank <= 7) return { colSpan: 2, rowSpan: 1 };
  return { colSpan: 2, rowSpan: 1 };
}
function getHeatClass(score, maxScore) {
  if (maxScore === 0) return 'heat-cold';
  const ratio = score / maxScore;
  if (ratio >= 0.7) return 'heat-high';
  if (ratio >= 0.4) return 'heat-mid';
  if (ratio >= 0.15) return 'heat-low';
  return 'heat-cold';
}
function buildPanelElement(metric, rank, score, maxScore, isCompact) {
  const el = document.createElement('div');
  el.className = 'panel' + (isCompact ? ' compact' : '');
  el.dataset.id = metric.id;
  el.draggable = !isCompact;
  const data = panelData.get(metric.id);
  if (data && data.locked) el.classList.add('locked');
  const placement = getGridPlacement(rank, METRICS.length, data ? data.locked : false, data ? data.userPosition : null);
  el.style.gridColumn = `span ${placement.colSpan}`;
  el.style.gridRow = `span ${placement.rowSpan}`;
  if (heatmapActive) {
    el.classList.add(getHeatClass(score, maxScore));
  }
  const scorePct = maxScore > 0 ? Math.min(100, (score / maxScore) * 100) : 0;
  el.innerHTML = `
    <div class="panel-score-bar" style="width:${scorePct}%"></div>
    <div class="panel-header">
      <span class="panel-icon">${metric.icon}</span>
      <span class="panel-title">${metric.title}</span>
      <span class="panel-rank">#${rank}</span>
    </div>
    <div class="panel-body">
      <span class="metric-value">${metric.value().toFixed(1)}</span><span class="metric-unit">${metric.unit}</span>
    </div>
    <div class="panel-preview">
      <span class="panel-icon">${metric.icon}</span> ${metric.title} — ${metric.value().toFixed(1)}${metric.unit}
    </div>
    <div class="panel-actions">
      <button class="lock-btn${data && data.locked ? ' locked' : ''}" data-action="lock" title="Lock position">🔒</button>
      <button data-action="compact" title="${isCompact ? 'Expand' : 'Compact'}">${isCompact ? '⤢' : '⤡'}</button>
    </div>`;
  return el;
}
function recomputeLayout() {
  const dashboard = document.getElementById('dashboard');
  const ranked = rankPanels();
  const scores = ranked.map(r => r.score);
  const maxScore = Math.max(...scores, 0.001);
  const existingEls = new Map();
  for (const child of dashboard.children) {
    if (child.dataset.id) existingEls.set(child.dataset.id, child);
  }
  dashboard.innerHTML = '';
  const fragment = document.createDocumentFragment();
  ranked.forEach(r => {
    const metric = METRICS.find(m => m.id === r.id);
    if (!metric) return;
    const isCompact = r.autoCompact || (panelData.get(r.id) && panelData.get(r.id).compact);
    const el = buildPanelElement(metric, r.rank, r.score, maxScore, isCompact);
    fragment.appendChild(el);
  });
  dashboard.appendChild(fragment);
  observePanels();
  updateStatsBar(ranked, maxScore);
  saveState();
}
function updateStatsBar(ranked, maxScore) {
  const bar = document.getElementById('statsBar');
  const totalViews = Array.from(panelData.values()).reduce((s, d) => s + d.viewMs, 0);
  const totalInteractions = Array.from(panelData.values()).reduce((s, d) => s + d.interactions, 0);
  bar.textContent = `Total view time: ${(totalViews/60000).toFixed(1)}min | Interactions: ${totalInteractions} | Panels: ${METRICS.length} | Compact: ${ranked.filter(r => r.autoCompact).length}`;
}
function observePanels() {
  if (visibilityObserver) visibilityObserver.disconnect();
  const panelEls = document.querySelectorAll('.panel');
  visibilityObserver = new IntersectionObserver((entries) => {
    const now = Date.now();
    for (const entry of entries) {
      const id = entry.target.dataset.id;
      if (!id) continue;
      ensurePanelData(id);
      const data = panelData.get(id);
      if (entry.isIntersecting && entry.intersectionRatio >= MIN_VISIBILITY_RATIO) {
        if (!visibilityEntries.has(id)) {
          visibilityEntries.set(id, { enterTime: now, ratio: entry.intersectionRatio });
        }
        activeVisiblePanels.add(id);
        data.lastSeen = now;
      } else {
        const visEntry = visibilityEntries.get(id);
        if (visEntry) {
          data.viewMs += (now - visEntry.enterTime);
          visibilityEntries.delete(id);
        }
        activeVisiblePanels.delete(id);
      }
    }
  }, { threshold: [0, 0.5, 1.0] });
  for (const el of panelEls) {
    visibilityObserver.observe(el);
  }
}
function setupResizeObserver() {
  if (resizeObserver) resizeObserver.disconnect();
  const dashboard = document.getElementById('dashboard');
  resizeObserver = new ResizeObserver(() => {
    queueMicrotask(() => {
      recomputeLayout();
    });
  });
  resizeObserver.observe(dashboard);
}
function resetIdleTimer() {
  isIdle = false;
  document.getElementById('statusText').textContent = 'active';
  if (idleTimer) clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    isIdle = true;
    document.getElementById('statusText').textContent = 'idle (tracking paused)';
    flushVisibilityTimers();
  }, IDLE_TIMEOUT);
}
function flushVisibilityTimers() {
  const now = Date.now();
  for (const [id, visEntry] of visibilityEntries) {
    ensurePanelData(id);
    panelData.get(id).viewMs += (now - visEntry.enterTime);
    visibilityEntries.set(id, { enterTime: now, ratio: visEntry.ratio });
  }
}
function setupActivityListeners() {
  const events = ['scroll', 'click', 'keydown', 'mousemove', 'touchstart'];
  for (const evt of events) {
    document.addEventListener(evt, resetIdleTimer, { passive: true });
  }
}
function setupDragAndDrop() {
  const dashboard = document.getElementById('dashboard');
  let dragSrc = null;
  dashboard.addEventListener('dragstart', (e) => {
    const panel = e.target.closest('.panel');
    if (!panel || panel.classList.contains('locked')) { e.preventDefault(); return; }
    dragSrc = panel;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.dataset.id);
  });
  dashboard.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    const panel = e.target.closest('.panel');
    if (panel && panel !== dragSrc) {
      panel.classList.add('drag-over');
    }
  });
  dashboard.addEventListener('dragleave', (e) => {
    const panel = e.target.closest('.panel');
    if (panel) panel.classList.remove('drag-over');
  });
  dashboard.addEventListener('drop', (e) => {
    e.preventDefault();
    const target = e.target.closest('.panel');
    if (!target || !dragSrc || target === dragSrc) return;
    target.classList.remove('drag-over');
    const srcId = dragSrc.dataset.id;
    const tgtId = target.dataset.id;
    ensurePanelData(srcId);
    ensurePanelData(tgtId);
    const srcData = panelData.get(srcId);
    const tgtData = panelData.get(tgtId);
    const ranked = rankPanels();
    const srcRank = ranked.find(r => r.id === srcId);
    const tgtRank = ranked.find(r => r.id === tgtId);
    if (srcRank && tgtRank) {
      srcData.userPosition = tgtRank.rank;
      srcData.locked = true;
      tgtData.userPosition = srcRank.rank;
      tgtData.locked = true;
    }
    dragSrc.classList.remove('dragging');
    dragSrc = null;
    recomputeLayout();
    saveState();
  });
  dashboard.addEventListener('dragend', (e) => {
    if (dragSrc) dragSrc.classList.remove('dragging');
    dragSrc = null;
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  });
}
function setupActionButtons() {
  const dashboard = document.getElementById('dashboard');
  dashboard.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const panel = btn.closest('.panel');
    if (!panel) return;
    const id = panel.dataset.id;
    ensurePanelData(id);
    const data = panelData.get(id);
    const action = btn.dataset.action;
    if (action === 'lock') {
      data.locked = !data.locked;
      data.userPosition = data.locked ? rankPanels().find(r => r.id === id)?.rank ?? null : null;
      data.interactions++;
      data.lastSeen = Date.now();
      recomputeLayout();
      saveState();
    } else if (action === 'compact') {
      data.compact = !data.compact;
      data.interactions++;
      data.lastSeen = Date.now();
      recomputeLayout();
      saveState();
    }
  });
  dashboard.addEventListener('click', (e) => {
    const panel = e.target.closest('.panel');
    if (panel && !e.target.closest('button')) {
      const id = panel.dataset.id;
      ensurePanelData(id);
      panelData.get(id).interactions++;
      panelData.get(id).lastSeen = Date.now();
    }
  });
}
function setupToolbar() {
  document.getElementById('btnHeatmap').addEventListener('click', () => {
    heatmapActive = !heatmapActive;
    document.getElementById('btnHeatmap').classList.toggle('active', heatmapActive);
    document.body.classList.toggle('heatmap-overlay', heatmapActive);
    if (heatmapActive) {
      const ranked = rankPanels();
      const maxScore = Math.max(...ranked.map(r => r.score), 0.001);
      document.querySelectorAll('.panel').forEach(el => {
        const id = el.dataset.id;
        const r = ranked.find(rr => rr.id === id);
        if (r) {
          el.classList.add(getHeatClass(r.score, maxScore));
        }
      });
    } else {
      document.querySelectorAll('.panel').forEach(el => {
        el.classList.remove('heat-high', 'heat-mid', 'heat-low', 'heat-cold');
      });
    }
    saveState();
  });
  document.getElementById('btnReset').addEventListener('click', () => {
    if (confirm('Reset all tracking data and layout preferences?')) {
      panelData.clear();
      localStorage.removeItem(STORAGE_KEY);
      visibilityEntries.clear();
      activeVisiblePanels.clear();
      heatmapActive = false;
      document.getElementById('btnHeatmap').classList.remove('active');
      document.body.classList.remove('heatmap-overlay');
      recomputeLayout();
    }
  });
}
function refreshMetricValues() {
  document.querySelectorAll('.panel').forEach(el => {
    const id = el.dataset.id;
    const metric = METRICS.find(m => m.id === id);
    if (!metric) return;
    const valEl = el.querySelector('.metric-value');
    if (valEl) valEl.textContent = metric.value().toFixed(1);
    const previewEl = el.querySelector('.panel-preview');
    if (previewEl) {
      previewEl.innerHTML = `<span class="panel-icon">${metric.icon}</span> ${metric.title} — ${metric.value().toFixed(1)}${metric.unit}`;
    }
  });
}
function init() {
  loadState();
  METRICS.forEach(m => ensurePanelData(m.id));
  recomputeLayout();
  setupResizeObserver();
  setupActivityListeners();
  setupDragAndDrop();
  setupActionButtons();
  setupToolbar();
  resetIdleTimer();
  document.getElementById('btnHeatmap').classList.toggle('active', heatmapActive);
  document.body.classList.toggle('heatmap-overlay', heatmapActive);
  setInterval(refreshMetricValues, 2000);
  window.addEventListener('beforeunload', () => {
    flushVisibilityTimers();
    saveState();
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