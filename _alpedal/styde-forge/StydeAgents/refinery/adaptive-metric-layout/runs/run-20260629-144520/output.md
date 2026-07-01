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
  --surface2: #242836;
  --border: #2a3040;
  --text: #e0e4f0;
  --text2: #8b90a0;
  --accent: #6c8cff;
  --accent2: #4cc9f0;
  --warn: #f0a040;
  --red: #e0556a;
  --green: #44c9a0;
  --radius: 8px;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.toolbar {
  display: flex;
  gap: 8px;
  padding: 10px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  align-items: center;
  flex-wrap: wrap;
}
.toolbar button {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}
.toolbar button:hover { background: #2e3440; border-color: var(--accent); }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.toolbar .spacer { flex:1; }
.toolbar .badge {
  font-size: 11px;
  color: var(--text2);
  background: var(--bg);
  padding: 4px 10px;
  border-radius: 12px;
}
.grid {
  display: grid;
  gap: 10px;
  padding: 12px;
  transition: grid-template-columns 0.3s ease, grid-template-rows 0.3s ease;
  grid-auto-flow: dense;
  min-height: calc(100vh - 52px);
}
.grid.cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: 120px;
}
.panel:hover { border-color: #4a5568; }
.panel.dragging { opacity: 0.6; z-index: 10; }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }
.panel.locked .panel-header { border-left: 3px solid var(--warn); }
.panel.compact { min-height: 80px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel-header {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  cursor: grab;
  gap: 8px;
  user-select: none;
}
.panel-header:active { cursor: grabbing; }
.panel-header .title {
  font-weight: 600;
  font-size: 13px;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-header .rank-badge {
  font-size: 10px;
  background: var(--accent);
  color: #fff;
  padding: 2px 7px;
  border-radius: 10px;
  opacity: 0.85;
}
.panel-header .controls { display: flex; gap: 4px; }
.panel-header .controls button {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1;
  transition: all 0.15s;
}
.panel-header .controls button:hover { color: var(--text); background: rgba(255,255,255,0.06); }
.panel-header .controls button.locked-btn { color: var(--warn); }
.panel-body {
  padding: 12px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
}
.panel-preview {
  display: none;
  padding: 8px 12px;
  font-size: 11px;
  color: var(--text2);
  align-items: center;
  gap: 8px;
}
.panel-preview .spark {
  flex: 1;
  height: 24px;
  opacity: 0.4;
}
.metric-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--accent2);
}
.metric-label {
  font-size: 11px;
  color: var(--text2);
  margin-top: 4px;
}
.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text2);
  font-size: 12px;
  flex-direction: column;
  gap: 6px;
}
.more-drawer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--surface);
  border-top: 2px solid var(--border);
  padding: 8px 16px;
  display: flex;
  gap: 12px;
  overflow-x: auto;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  z-index: 100;
  max-height: 140px;
}
.more-drawer.open { transform: translateY(0); }
.more-drawer .mini-panel {
  flex-shrink: 0;
  background: var(--surface2);
  border-radius: var(--radius);
  padding: 8px 14px;
  cursor: pointer;
  font-size: 12px;
  border: 1px solid var(--border);
  transition: all 0.15s;
  white-space: nowrap;
}
.more-drawer .mini-panel:hover { border-color: var(--accent); }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 10px 20px;
  border-radius: var(--radius);
  font-size: 12px;
  z-index: 200;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s ease;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.heatmap-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: var(--radius);
  opacity: 0;
  transition: opacity 0.3s;
}
.heatmap-overlay.show { opacity: 1; }
.resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 16px;
  height: 16px;
  cursor: nwse-resize;
  background: linear-gradient(135deg, transparent 50%, var(--border) 50%);
  border-radius: 0 0 var(--radius) 0;
  opacity: 0;
  transition: opacity 0.15s;
}
.panel:hover .resize-handle { opacity: 1; }
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text2);
  font-size: 14px;
  flex-direction: column;
  gap: 8px;
}
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="toggleHeatmap()" id="btnHeatmap">Heatmap</button>
  <button onclick="resetLayout()">Reset</button>
  <button onclick="toggleMore()" id="btnMore">More (0)</button>
  <span class="spacer"></span>
  <span class="badge" id="badgeUpdates">0 updates</span>
</div>
<div class="grid cols-4" id="grid"></div>
<div class="more-drawer" id="moreDrawer"></div>
<div class="toast" id="toast"></div>
<script>
// ── State ──
const PANEL_DEFS = [
  { id: 'revenue',   title: 'Revenue',       value: '$48,294', change: '+12.3%', color: '#44c9a0' },
  { id: 'users',     title: 'Active Users',   value: '12,847',  change: '+5.7%',  color: '#6c8cff' },
  { id: 'churn',     title: 'Churn Rate',     value: '2.4%',    change: '-0.3%',  color: '#f0a040' },
  { id: 'cpu',       title: 'CPU Load',       value: '67%',     change: '+8%',    color: '#e0556a' },
  { id: 'latency',   title: 'P99 Latency',    value: '142ms',   change: '-18ms',  color: '#4cc9f0' },
  { id: 'errors',    title: 'Error Rate',     value: '0.12%',   change: '-0.04%', color: '#e0556a' },
  { id: 'storage',   title: 'Storage',        value: '2.1 TB',  change: '+140GB', color: '#6c8cff' },
  { id: 'requests',  title: 'Requests/min',   value: '4,821',   change: '+9.1%',  color: '#44c9a0' },
  { id: 'sessions',  title: 'Sessions',       value: '3,204',   change: '+2.3%',  color: '#4cc9f0' },
  { id: 'apdex',     title: 'Apdex Score',    value: '0.94',    change: '+0.02',  color: '#44c9a0' },
  { id: 'bandwidth', title: 'Bandwidth',      value: '840 Mbps',change: '+10%',   color: '#6c8cff' },
  { id: 'uptime',    title: 'Uptime',         value: '99.97%',  change: 'stable', color: '#44c9a0' },
];
// Metrics tracked per panel: { viewStart, totalDuration, interactions, collapses, lastInteraction }
let metrics = new Map();
let panelOrder = PANEL_DEFS.map(p => p.id);
let lockedPanels = new Set();
let compactPanels = new Set();
let showHeatmap = false;
let updateCounter = 0;
let dirty = false;
let debounceTimer = null;
let debounceMs = 2000;
let svgIdCounter = 0;
// ── Init ──
function init() {
  loadState();
  PANEL_DEFS.forEach(p => {
    if (!metrics.has(p.id)) {
      metrics.set(p.id, {
        viewStart: null,
        totalDuration: 0,
        interactions: 0,
        collapses: 0,
        lastInteraction: 0
      });
    }
  });
  recomputeLayout();
  setupIntersectionObserver();
  requestAnimationFrame(() => {
    requestAnimationFrame(recomputeLayout);
  });
}
// ── Ranking (Map-based O(1)) ──
function computeScore(panelId) {
  const m = metrics.get(panelId);
  if (!m) return 0;
  const now = Date.now();
  const recencyHours = (now - m.lastInteraction) / 3600000;
  const recencyFactor = m.lastInteraction ? Math.max(0.05, 1 / (1 + recencyHours)) : 0.1;
  const freqFactor = Math.log2(m.interactions + 1) + 1;
  const durFactor = Math.log2((m.totalDuration / 1000) + 1) + 1;
  return (freqFactor * durFactor * recencyFactor * 100) | 0;
}
function recomputeLayout() {
  const scores = new Map();
  PANEL_DEFS.forEach(p => scores.set(p.id, computeScore(p.id)));
  // Sort: locked first (preserve position), then by score desc
  const ordered = [...PANEL_DEFS].sort((a, b) => {
    const aLocked = lockedPanels.has(a.id);
    const bLocked = lockedPanels.has(b.id);
    if (aLocked && !bLocked) return -1;
    if (!aLocked && bLocked) return 1;
    if (aLocked && bLocked) {
      return panelOrder.indexOf(a.id) - panelOrder.indexOf(b.id);
    }
    return scores.get(b.id) - scores.get(a.id);
  });
  panelOrder = ordered.map(p => p.id);
  // Compact: bottom 30% by score (unless locked)
  const scoreThreshold = [...scores.entries()]
    .filter(([id]) => !lockedPanels.has(id))
    .sort((a, b) => a[1] - b[1]);
  const cutoffIdx = Math.floor(scoreThreshold.length * 0.3);
  const newCompact = new Set(scoreThreshold.slice(0, cutoffIdx).map(([id]) => id));
  // Only update DOM if changed
  if (!arraysEqual([...compactPanels].sort(), [...newCompact].sort()) ||
      !arraysEqual(panelOrder, currentDomOrder())) {
    compactPanels = newCompact;
    renderGrid(ordered, scores);
    dirty = true;
    schedulePersist();
  }
}
function currentDomOrder() {
  const els = document.querySelectorAll('.panel');
  return [...els].map(el => el.dataset.panelId);
}
function arraysEqual(a, b) {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}
// ── Render (incremental) ──
function renderGrid(ordered, scores) {
  const grid = document.getElementById('grid');
  const existing = new Map();
  grid.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.panelId, el));
  const fragment = document.createDocumentFragment();
  const currentIds = new Set();
  ordered.forEach((p, idx) => {
    currentIds.add(p.id);
    let el = existing.get(p.id);
    if (!el) {
      el = createPanelElement(p);
    }
    updatePanelElement(el, p, idx, scores.get(p.id));
    fragment.appendChild(el);
  });
  grid.innerHTML = '';
  grid.appendChild(fragment);
  updateMoreDrawer(ordered, scores);
  updateBadge();
}
function createPanelElement(p) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  el.draggable = true;
  el.innerHTML = `
    <div class="panel-header">
      <span class="title">${p.title}</span>
      <span class="rank-badge"></span>
      <span class="controls">
        <button class="compact-btn" title="Compact/Expand">⊟</button>
        <button class="locked-btn" title="Lock position">🔓</button>
      </span>
    </div>
    <div class="panel-body">
      <div class="metric-value">${p.value}</div>
      <div class="metric-label">${p.change}</div>
    </div>
    <div class="panel-preview">
      <span>${p.title}</span>
      <span style="font-weight:600">${p.value}</span>
      <svg class="spark" data-spark-id="${p.id}"></svg>
    </div>
    <div class="heatmap-overlay"></div>
    <div class="resize-handle"></div>
  `;
  bindPanelEvents(el, p);
  return el;
}
function updatePanelElement(el, p, idx, score) {
  const isCompact = compactPanels.has(p.id);
  const isLocked = lockedPanels.has(p.id);
  el.classList.toggle('compact', isCompact);
  el.classList.toggle('locked', isLocked);
  const rankBadge = el.querySelector('.rank-badge');
  rankBadge.textContent = `#${idx + 1}`;
  const lockBtn = el.querySelector('.locked-btn');
  lockBtn.textContent = isLocked ? '🔒' : '🔓';
  if (isLocked) lockBtn.classList.add('locked-btn');
  else lockBtn.classList.remove('locked-btn');
  // Update heatmap overlay
  const overlay = el.querySelector('.heatmap-overlay');
  overlay.classList.toggle('show', showHeatmap);
  if (showHeatmap) {
    const intensity = Math.min(1, score / 300);
    const r = Math.round(108 + (240 - 108) * intensity);
    const g = Math.round(140 - 100 * intensity);
    const b = Math.round(255 - 200 * intensity);
    overlay.style.background = `rgba(${r},${g},${b},${0.15 + intensity * 0.25})`;
  }
  // Update sparkline for compact panels
  if (isCompact) {
    const spark = el.querySelector('.spark');
    if (spark && !spark.hasAttribute('data-drawn')) {
      drawSparkline(spark, p.id);
      spark.setAttribute('data-drawn', '1');
    }
  }
  // Grid span: top 2 get 2 columns
  if (idx < 2 && !isCompact) {
    el.style.gridColumn = 'span 2';
  } else {
    el.style.gridColumn = '';
  }
}
function bindPanelEvents(el, p) {
  // Lock toggle
  el.querySelector('.locked-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    if (lockedPanels.has(p.id)) {
      lockedPanels.delete(p.id);
    } else {
      lockedPanels.add(p.id);
    }
    trackInteraction(p.id, 'lock');
    recomputeLayout();
  });
  // Compact toggle
  el.querySelector('.compact-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    if (compactPanels.has(p.id)) {
      compactPanels.delete(p.id);
    } else {
      compactPanels.add(p.id);
    }
    trackInteraction(p.id, 'collapse');
    recomputeLayout();
  });
  // Panel click = interaction
  el.addEventListener('click', () => {
    trackInteraction(p.id, 'click');
  });
  // Drag
  el.addEventListener('dragstart', (e) => {
    el.classList.add('dragging');
    e.dataTransfer.setData('text/plain', p.id);
    e.dataTransfer.effectAllowed = 'move';
  });
  el.addEventListener('dragend', () => {
    el.classList.remove('dragging');
    document.querySelectorAll('.panel').forEach(pe => pe.classList.remove('drag-over'));
  });
  el.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    el.classList.add('drag-over');
  });
  el.addEventListener('dragleave', () => el.classList.remove('drag-over'));
  el.addEventListener('drop', (e) => {
    e.preventDefault();
    el.classList.remove('drag-over');
    const srcId = e.dataTransfer.getData('text/plain');
    const dstId = p.id;
    if (srcId !== dstId) {
      const srcIdx = panelOrder.indexOf(srcId);
      const dstIdx = panelOrder.indexOf(dstId);
      if (srcIdx >= 0 && dstIdx >= 0) {
        panelOrder.splice(srcIdx, 1);
        panelOrder.splice(dstIdx, 0, srcId);
        lockedPanels.add(srcId);
        trackInteraction(srcId, 'drag');
        recomputeLayout();
      }
    }
  });
  // Resize (simple: double-click to toggle span)
  el.querySelector('.resize-handle').addEventListener('dblclick', (e) => {
    e.stopPropagation();
    if (el.style.gridColumn === 'span 2') {
      el.style.gridColumn = '';
    } else {
      el.style.gridColumn = 'span 2';
    }
    trackInteraction(p.id, 'resize');
  });
}
// ── Sparkline (unique SVG IDs) ──
function drawSparkline(svg, panelId) {
  svgIdCounter++;
  const w = 60, h = 24;
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.setAttribute('width', '60');
  svg.setAttribute('height', '24');
  const points = [];
  for (let i = 0; i < 10; i++) {
    points.push(Math.sin(i * 0.8 + panelId.charCodeAt(0) * 0.1) * 8 + 12);
  }
  const d = points.map((y, i) => `${i === 0 ? 'M' : 'L'}${(i / 9) * w},${y}`).join(' ');
  const gradId = `sg-${svgIdCounter}`;
  svg.innerHTML = `
    <defs><linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="var(--accent2,#4cc9f0)" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="var(--accent2,#4cc9f0)" stop-opacity="0"/>
    </linearGradient></defs>
    <path d="${d}" fill="none" stroke="var(--accent2,#4cc9f0)" stroke-width="1.2"/>
    <path d="${d} L${w},${h} L0,${h} Z" fill="url(#${gradId})"/>
  `;
}
// ── Tracking ──
function trackInteraction(panelId, type) {
  const m = metrics.get(panelId);
  if (!m) return;
  m.interactions++;
  m.lastInteraction = Date.now();
  if (type === 'collapse') m.collapses++;
  updateCounter++;
  updateBadge();
  dirty = true;
  schedulePersist();
}
function setupIntersectionObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      const m = metrics.get(panelId);
      if (!m) return;
      if (entry.isIntersecting) {
        m.viewStart = Date.now();
      } else if (m.viewStart) {
        m.totalDuration += Date.now() - m.viewStart;
        m.viewStart = null;
        dirty = true;
        schedulePersist();
      }
    });
  }, { threshold: 0.5 });
  // Observe after render
  const obsAll = () => {
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  };
  // Re-observe after each render via MutationObserver
  const mo = new MutationObserver(() => {
    document.querySelectorAll('.panel').forEach(el => {
      if (!el.dataset.observed) {
        observer.observe(el);
        el.dataset.observed = '1';
      }
    });
  });
  mo.observe(document.getElementById('grid'), { childList: true, subtree: false });
  obsAll();
}
// ── Persistence with debounce ──
function schedulePersist() {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(persistState, debounceMs);
}
function persistState() {
  const data = {
    metrics: Object.fromEntries(metrics),
    order: panelOrder,
    locked: [...lockedPanels],
    compact: [...compactPanels],
    timestamp: Date.now()
  };
  try {
    localStorage.setItem('adaptive-dashboard', JSON.stringify(data));
  } catch(e) { /* quota exceeded, silent */ }
  debounceTimer = null;
  dirty = false;
}
function loadState() {
  try {
    const raw = localStorage.getItem('adaptive-dashboard');
    if (!raw) return;
    const data = JSON.parse(raw);
    // Restore metrics Map with O(1) lookups
    if (data.metrics && typeof data.metrics === 'object') {
      metrics = new Map(Object.entries(data.metrics));
    }
    if (Array.isArray(data.order)) {
      // Validate IDs exist
      const validIds = new Set(PANEL_DEFS.map(p => p.id));
      panelOrder = data.order.filter(id => validIds.has(id));
      // Append any missing panels
      PANEL_DEFS.forEach(p => {
        if (!panelOrder.includes(p.id)) panelOrder.push(p.id);
      });
    }
    if (Array.isArray(data.locked)) lockedPanels = new Set(data.locked);
    if (Array.isArray(data.compact)) compactPanels = new Set(data.compact);
  } catch(e) {
    // Corrupt state, start fresh
    metrics = new Map();
    panelOrder = PANEL_DEFS.map(p => p.id);
    lockedPanels = new Set();
    compactPanels = new Set();
  }
}
// ── More drawer ──
function updateMoreDrawer(ordered, scores) {
  const compactIds = [...compactPanels];
  const drawer = document.getElementById('moreDrawer');
  const btnMore = document.getElementById('btnMore');
  btnMore.textContent = `More (${compactIds.length})`;
  drawer.innerHTML = '';
  compactIds.forEach(id => {
    const p = PANEL_DEFS.find(d => d.id === id);
    if (!p) return;
    const mini = document.createElement('div');
    mini.className = 'mini-panel';
    mini.textContent = `${p.title}: ${p.value}`;
    mini.addEventListener('click', () => {
      compactPanels.delete(id);
      lockedPanels.add(id);
      trackInteraction(id, 'expand-from-more');
      recomputeLayout();
    });
    drawer.appendChild(mini);
  });
}
function toggleMore() {
  document.getElementById('moreDrawer').classList.toggle('open');
}
// ── Heatmap toggle ──
function toggleHeatmap() {
  showHeatmap = !showHeatmap;
  document.getElementById('btnHeatmap').classList.toggle('active', showHeatmap);
  document.querySelectorAll('.heatmap-overlay').forEach(el => {
    el.classList.toggle('show', showHeatmap);
  });
}
// ── Reset ──
function resetLayout() {
  metrics = new Map();
  panelOrder = PANEL_DEFS.map(p => p.id);
  lockedPanels = new Set();
  compactPanels = new Set();
  PANEL_DEFS.forEach(p => {
    metrics.set(p.id, {
      viewStart: null, totalDuration: 0, interactions: 0, collapses: 0, lastInteraction: 0
    });
  });
  localStorage.removeItem('adaptive-dashboard');
  recomputeLayout();
  toast('Layout reset');
}
// ── Badge ──
function updateBadge() {
  document.getElementById('badgeUpdates').textContent = `${updateCounter} updates`;
}
// ── Toast ──
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2000);
}
// ── Periodic recompute (every 30s to decay recency) ──
setInterval(() => {
  recomputeLayout();
}, 30000);
// ── Flush on unload ──
window.addEventListener('beforeunload', () => {
  if (dirty) persistState();
});
// ── Boot ──
init();
</script>
</body>
</html>