<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --border: #2a2d3a;
  --text: #c8ccd4;
  --text-dim: #7a7f8a;
  --accent: #5b8def;
  --accent-glow: rgba(91,141,239,0.25);
  --warn: #f0a040;
  --danger: #e0556a;
  --success: #4caf88;
  --radius: 8px;
  --transition: 200ms ease;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 16px;
  user-select: none;
}
.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.header h1 {
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.badge {
  font-size: 0.7rem;
  background: var(--accent);
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
}
.btn {
  font-size: 0.75rem;
  background: var(--panel-bg);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 5px 12px;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}
.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.btn:hover { background: #252836; border-color: var(--accent); }
.btn:active { background: #2e3142; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  align-items: start;
}
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: grid-column var(--transition), grid-row var(--transition), opacity var(--transition), border-color var(--transition);
  cursor: grab;
  position: relative;
}
.panel:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.panel.dragging {
  opacity: 0.5;
  cursor: grabbing;
  border-color: var(--accent);
}
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: '🔒';
  position: absolute;
  top: 6px;
  right: 36px;
  font-size: 0.65rem;
  opacity: 0.7;
}
.panel.compact { grid-column: span 1; }
.panel.expanded { grid-column: span 2; }
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.02);
}
.panel-title {
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  display: flex;
  align-items: center;
  gap: 6px;
}
.panel-rank {
  font-size: 0.6rem;
  color: var(--text-dim);
  background: rgba(255,255,255,0.05);
  padding: 1px 6px;
  border-radius: 8px;
}
.panel-actions {
  display: flex;
  gap: 4px;
}
.icon-btn {
  width: 24px;
  height: 24px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-dim);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition), color var(--transition), border-color var(--transition);
}
.icon-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 1px;
}
.icon-btn:hover { background: rgba(255,255,255,0.06); color: var(--text); }
.icon-btn.active { color: var(--warn); border-color: var(--warn); }
.panel-body {
  padding: 10px;
  min-height: 80px;
  transition: max-height var(--transition), padding var(--transition), min-height var(--transition);
}
.panel-body.compact-body {
  max-height: 40px;
  min-height: 40px;
  padding: 4px 10px;
  overflow: hidden;
  opacity: 0.5;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 0;
  font-size: 0.75rem;
}
.metric-label { color: var(--text-dim); }
.metric-value { font-variant-numeric: tabular-nums; font-weight: 500; }
.metric-bar {
  height: 4px;
  background: rgba(255,255,255,0.06);
  border-radius: 2px;
  margin-top: 4px;
  overflow: hidden;
}
.metric-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 600ms ease;
}
.metric-bar-fill.ok { background: var(--success); }
.metric-bar-fill.warn { background: var(--warn); }
.metric-bar-fill.danger { background: var(--danger); }
.stats-footer {
  font-size: 0.6rem;
  color: var(--text-dim);
  margin-top: 6px;
  display: flex;
  gap: 10px;
}
[role="toolbar"] { display: flex; gap: 8px; align-items: center; }
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout</h1>
  <span class="badge">LIVE</span>
  <div role="toolbar" aria-label="Dashboard actions">
    <button class="btn" id="btnReset" aria-label="Reset all tracking data">Reset</button>
    <button class="btn" id="btnExport" aria-label="Export layout to clipboard">Export</button>
  </div>
</div>
<div class="grid" id="grid" role="list" aria-label="Metric panels"></div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_layout_v1';
const TICK_MS = 2000;
const DECAY_HALF_HOURS = 12;
const COMPACT_THRESHOLD = 0.15;
const PANEL_DEFS = [
  { id: 'cpu', title: 'CPU Usage', icon: '⚙', metric: 'cpu', unit: '%', warn: 70, danger: 90 },
  { id: 'memory', title: 'Memory', icon: '🧠', metric: 'memory', unit: '%', warn: 75, danger: 90 },
  { id: 'network', title: 'Network I/O', icon: '🌐', metric: 'network', unit: 'MB/s', warn: 800, danger: 950 },
  { id: 'disk', title: 'Disk IOPS', icon: '💾', metric: 'disk', unit: 'iops', warn: 5000, danger: 8000 },
  { id: 'errors', title: 'Error Rate', icon: '⚠', metric: 'errors', unit: '/min', warn: 5, danger: 20 },
  { id: 'latency', title: 'P99 Latency', icon: '⏱', metric: 'latency', unit: 'ms', warn: 200, danger: 500 },
  { id: 'requests', title: 'Req/sec', icon: '📊', metric: 'requests', unit: 'rps', warn: 5000, danger: 8000 },
  { id: 'cache', title: 'Cache Hit Rate', icon: '🗂', metric: 'cache', unit: '%', warn: 70, danger: 50 },
];
function rand(min, max) { return Math.random() * (max - min) + min; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function freshMetrics() {
  return {
    cpu: rand(15, 95),
    memory: rand(40, 88),
    network: rand(100, 950),
    disk: rand(200, 8000),
    errors: rand(0, 25),
    latency: rand(10, 500),
    requests: rand(1000, 8000),
    cache: rand(45, 98),
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === 'object' && parsed.panels) return parsed;
  } catch(e) { /* corrupt */ }
  return null;
}
function saveState(state) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
let state = loadState();
if (!state) {
  const now = Date.now();
  state = {
    panels: PANEL_DEFS.map((def, i) => ({
      id: def.id,
      lock: false,
      overrideRank: null,
      collapsed: false,
      views: 0,
      totalDuration: 0,
      lastView: now,
      interactions: 0,
      lastInteraction: now,
      initOrder: i,
    })),
  };
}
let panelStateMap = new Map(state.panels.map(p => [p.id, p]));
let metrics = freshMetrics();
let tickHandle = null;
let visibleStart = Date.now();
let visibleSet = new Set();
function getPanelState(id) {
  let ps = panelStateMap.get(id);
  if (!ps) {
    ps = {
      id, lock: false, overrideRank: null, collapsed: false,
      views: 0, totalDuration: 0, lastView: Date.now(),
      interactions: 0, lastInteraction: Date.now(), initOrder: PANEL_DEFS.length,
    };
    panelStateMap.set(id, ps);
  }
  return ps;
}
function persist() {
  state.panels = Array.from(panelStateMap.values());
  saveState(state);
}
/* ---------- attention scoring ---------- */
function attentionScore(ps, now) {
  const hoursSinceView = Math.max(0, (now - ps.lastView) / 3600000);
  const recency = Math.exp(-hoursSinceView / DECAY_HALF_HOURS);
  const freq = clamp(ps.interactions + 1, 1, 100);
  const dur = clamp(ps.totalDuration / 1000, 0.1, 3600);
  return freq * Math.log1p(dur) * recency;
}
function computeRanks(now) {
  const entries = [];
  for (const def of PANEL_DEFS) {
    const ps = getPanelState(def.id);
    const rawScore = attentionScore(ps, now);
    entries.push({ id: def.id, rawScore, locked: ps.lock, overrideRank: ps.overrideRank });
  }
  const locked = entries.filter(e => e.locked && e.overrideRank !== null)
    .sort((a, b) => a.overrideRank - b.overrideRank);
  const unlocked = entries.filter(e => !e.locked || e.overrideRank === null)
    .sort((a, b) => b.rawScore - a.rawScore);
  const assigned = new Set(locked.map(e => e.id));
  const ranked = [];
  let nextRank = 0;
  for (const e of locked) {
    ranked.push({ id: e.id, rank: nextRank++, score: e.rawScore, locked: true });
  }
  for (const e of unlocked) {
    ranked.push({ id: e.id, rank: nextRank++, score: e.rawScore, locked: false });
  }
  return ranked;
}
/* ---------- DOM reconciliation (no full rebuild) ---------- */
const grid = document.getElementById('grid');
let panelEls = new Map();
function classForValue(def, val) {
  if (val >= def.danger) return 'danger';
  if (val >= def.warn) return 'warn';
  return 'ok';
}
function createPanelEl(def, ps, rank, score, isCompact) {
  const el = document.createElement('div');
  el.className = 'panel' + (ps.lock ? ' locked' : '') + (isCompact ? ' compact' : ' expanded');
  el.draggable = true;
  el.setAttribute('role', 'listitem');
  el.setAttribute('aria-label', def.title + (ps.lock ? ' (locked)' : ''));
  el.setAttribute('tabindex', '0');
  el.dataset.id = def.id;
  const header = document.createElement('div');
  header.className = 'panel-header';
  const titleWrap = document.createElement('div');
  titleWrap.className = 'panel-title';
  titleWrap.textContent = def.icon + ' ' + def.title;
  const rankSpan = document.createElement('span');
  rankSpan.className = 'panel-rank';
  rankSpan.textContent = '#' + (rank + 1);
  titleWrap.appendChild(rankSpan);
  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const lockBtn = document.createElement('button');
  lockBtn.className = 'icon-btn' + (ps.lock ? ' active' : '');
  lockBtn.setAttribute('aria-label', ps.lock ? 'Unlock panel' : 'Lock panel position');
  lockBtn.setAttribute('aria-pressed', String(ps.lock));
  lockBtn.innerHTML = '🔒';
  lockBtn.dataset.action = 'lock';
  const collapseBtn = document.createElement('button');
  collapseBtn.className = 'icon-btn';
  collapseBtn.setAttribute('aria-label', ps.collapsed ? 'Expand panel' : 'Collapse panel');
  collapseBtn.setAttribute('aria-pressed', String(ps.collapsed));
  collapseBtn.innerHTML = ps.collapsed ? '▶' : '▼';
  collapseBtn.dataset.action = 'collapse';
  actions.appendChild(lockBtn);
  actions.appendChild(collapseBtn);
  header.appendChild(titleWrap);
  header.appendChild(actions);
  const body = document.createElement('div');
  body.className = 'panel-body' + (ps.collapsed ? ' compact-body' : '');
  body.dataset.role = 'body';
  el.appendChild(header);
  el.appendChild(body);
  return el;
}
function updateBodyContent(el, def, ps, metrics) {
  const body = el.querySelector('[data-role="body"]');
  if (!body) return;
  const isCollapsed = ps.collapsed;
  body.className = 'panel-body' + (isCollapsed ? ' compact-body' : '');
  if (isCollapsed) {
    body.innerHTML = '<span style="font-size:0.7rem;color:var(--text-dim)">Collapsed — click ▼ to expand</span>';
    return;
  }
  const val = metrics[def.metric] ?? 0;
  const cls = classForValue(def, val);
  body.innerHTML =
    '<div class="metric-row"><span class="metric-label">Current</span><span class="metric-value">' +
    val.toFixed(1) + ' ' + def.unit + '</span></div>' +
    '<div class="metric-bar"><div class="metric-bar-fill ' + cls + '" style="width:' +
    clamp(val / (def.danger || 100) * 100, 0, 100) + '%"></div></div>' +
    '<div class="stats-footer"><span>Views: ' + ps.views + '</span><span>Int: ' +
    ps.interactions + '</span></div>';
}
function updatePanelEl(el, def, ps, rank, score, now) {
  const isCompact = score < COMPACT_THRESHOLD * (computeMaxScore(now) || 1);
  el.className = 'panel' + (ps.lock ? ' locked' : '') + (isCompact ? ' compact' : ' expanded');
  el.setAttribute('aria-label', def.title + (ps.lock ? ' (locked)' : ''));
  const rankSpan = el.querySelector('.panel-rank');
  if (rankSpan) rankSpan.textContent = '#' + (rank + 1);
  const lockBtn = el.querySelector('[data-action="lock"]');
  if (lockBtn) {
    lockBtn.className = 'icon-btn' + (ps.lock ? ' active' : '');
    lockBtn.setAttribute('aria-pressed', String(ps.lock));
    lockBtn.setAttribute('aria-label', ps.lock ? 'Unlock panel' : 'Lock panel position');
  }
  const collapseBtn = el.querySelector('[data-action="collapse"]');
  if (collapseBtn) {
    collapseBtn.setAttribute('aria-pressed', String(ps.collapsed));
    collapseBtn.setAttribute('aria-label', ps.collapsed ? 'Expand panel' : 'Collapse panel');
    collapseBtn.innerHTML = ps.collapsed ? '▶' : '▼';
  }
  updateBodyContent(el, def, ps, metrics);
}
function computeMaxScore(now) {
  let max = 0;
  for (const def of PANEL_DEFS) {
    const s = attentionScore(getPanelState(def.id), now);
    if (s > max) max = s;
  }
  return max || 1;
}
/* targeted reorder: move DOM nodes instead of full rebuild */
function reconcileDOM(now) {
  const ranked = computeRanks(now);
  const idOrder = ranked.map(r => r.id);
  const existingIds = new Set();
  for (const el of grid.children) {
    if (el.dataset.id) existingIds.add(el.dataset.id);
  }
  for (const id of idOrder) {
    if (!existingIds.has(id)) {
      const def = PANEL_DEFS.find(d => d.id === id);
      const ps = getPanelState(id);
      const entry = ranked.find(r => r.id === id);
      const el = createPanelEl(def, ps, entry.rank, entry.score, false);
      panelEls.set(id, el);
      grid.appendChild(el);
    }
  }
  for (const el of grid.children) {
    const id = el.dataset.id;
    if (!id || !idOrder.includes(id)) {
      el.remove();
      panelEls.delete(id);
    }
  }
  const children = Array.from(grid.children);
  const currentOrder = children.map(c => c.dataset.id);
  if (currentOrder.join(',') !== idOrder.join(',')) {
    const frag = document.createDocumentFragment();
    for (const id of idOrder) {
      const el = children.find(c => c.dataset.id === id);
      if (el) frag.appendChild(el);
    }
    grid.appendChild(frag);
  }
  for (const id of idOrder) {
    const el = panelEls.get(id);
    const def = PANEL_DEFS.find(d => d.id === id);
    const ps = getPanelState(id);
    const entry = ranked.find(r => r.id === id);
    if (el && def && ps && entry) {
      updatePanelEl(el, def, ps, entry.rank, entry.score, now);
    }
  }
}
/* ---------- tick ---------- */
function tick() {
  const now = Date.now();
  metrics = freshMetrics();
  const elapsed = TICK_MS;
  for (const id of visibleSet) {
    const ps = getPanelState(id);
    ps.totalDuration += elapsed;
    ps.lastView = now;
  }
  reconcileDOM(now);
  persist();
}
function startTick() {
  if (tickHandle !== null) return;
  tickHandle = setInterval(tick, TICK_MS);
}
/* ---------- visibility tracking ---------- */
function updateVisibleSet() {
  visibleSet.clear();
  for (const el of grid.children) {
    if (!el.dataset.id) continue;
    const rect = el.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    if (rect.bottom > 0 && rect.top < vh && rect.right > 0 && rect.left < vw) {
      visibleSet.add(el.dataset.id);
    }
  }
}
/* ---------- interactions ---------- */
function handleInteraction(id, type) {
  const ps = getPanelState(id);
  const now = Date.now();
  ps.interactions++;
  ps.lastInteraction = now;
  if (!ps.views || ps.lastView < now - 5000) {
    ps.views++;
    ps.lastView = now;
  }
  persist();
}
function toggleLock(id) {
  const ps = getPanelState(id);
  const now = Date.now();
  if (ps.lock) {
    ps.lock = false;
    ps.overrideRank = null;
  } else {
    ps.lock = true;
    const ranked = computeRanks(now);
    const entry = ranked.find(r => r.id === id);
    ps.overrideRank = entry ? entry.rank : 0;
  }
  handleInteraction(id, 'lock');
  reconcileDOM(now);
}
function toggleCollapse(id) {
  const ps = getPanelState(id);
  ps.collapsed = !ps.collapsed;
  handleInteraction(id, 'collapse');
  const el = panelEls.get(id);
  const def = PANEL_DEFS.find(d => d.id === id);
  if (el && def) {
    const now = Date.now();
    const ranked = computeRanks(now);
    const entry = ranked.find(r => r.id === id);
    updatePanelEl(el, def, ps, entry ? entry.rank : 0, entry ? entry.score : 0, now);
  }
  persist();
}
/* ---------- event delegation ---------- */
grid.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const panel = btn.closest('.panel');
  if (!panel || !panel.dataset.id) return;
  e.stopPropagation();
  const action = btn.dataset.action;
  if (action === 'lock') toggleLock(panel.dataset.id);
  else if (action === 'collapse') toggleCollapse(panel.dataset.id);
});
grid.addEventListener('keydown', function(e) {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const panel = e.target.closest('.panel');
  if (!panel || !panel.dataset.id) return;
  const focused = document.activeElement;
  const lockBtn = panel.querySelector('[data-action="lock"]');
  const collapseBtn = panel.querySelector('[data-action="collapse"]');
  if (focused === lockBtn) {
    e.preventDefault();
    toggleLock(panel.dataset.id);
  } else if (focused === collapseBtn) {
    e.preventDefault();
    toggleCollapse(panel.dataset.id);
  }
});
/* ---------- drag and drop ---------- */
let dragSrc = null;
let dragGhost = null;
grid.addEventListener('dragstart', function(e) {
  const panel = e.target.closest('.panel');
  if (!panel || !panel.dataset.id) return;
  dragSrc = panel;
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panel.dataset.id);
  setTimeout(() => { if (dragSrc) dragSrc.style.opacity = '0.4'; }, 0);
});
grid.addEventListener('dragend', function(e) {
  if (dragSrc) {
    dragSrc.classList.remove('dragging');
    dragSrc.style.opacity = '';
    dragSrc = null;
  }
});
grid.addEventListener('dragover', function(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});
grid.addEventListener('drop', function(e) {
  e.preventDefault();
  if (!dragSrc) return;
  const target = e.target.closest('.panel');
  if (!target || target === dragSrc || !target.dataset.id) return;
  const srcId = dragSrc.dataset.id;
  const tgtId = target.dataset.id;
  const now = Date.now();
  const ranked = computeRanks(now);
  const srcEntry = ranked.find(r => r.id === srcId);
  const tgtEntry = ranked.find(r => r.id === tgtId);
  if (!srcEntry || !tgtEntry) return;
  const srcPs = getPanelState(srcId);
  const tgtPs = getPanelState(tgtId);
  srcPs.lock = true;
  srcPs.overrideRank = tgtEntry.rank;
  srcPs.interactions++;
  srcPs.lastInteraction = now;
  tgtPs.lock = true;
  tgtPs.overrideRank = srcEntry.rank;
  tgtPs.interactions++;
  tgtPs.lastInteraction = now;
  reconcileDOM(now);
});
/* ---------- scroll visibility ---------- */
let scrollTicking = false;
window.addEventListener('scroll', function() {
  if (!scrollTicking) {
    requestAnimationFrame(function() {
      updateVisibleSet();
      scrollTicking = false;
    });
    scrollTicking = true;
  }
}, { passive: true });
/* ---------- buttons ---------- */
document.getElementById('btnReset').addEventListener('click', function() {
  const now = Date.now();
  for (const def of PANEL_DEFS) {
    const ps = getPanelState(def.id);
    ps.lock = false;
    ps.overrideRank = null;
    ps.collapsed = false;
    ps.views = 0;
    ps.totalDuration = 0;
    ps.lastView = now;
    ps.interactions = 0;
    ps.lastInteraction = now;
  }
  panelStateMap.clear();
  for (const def of PANEL_DEFS) {
    panelStateMap.set(def.id, getPanelState(def.id));
  }
  grid.innerHTML = '';
  panelEls.clear();
  reconcileDOM(now);
  persist();
});
document.getElementById('btnExport').addEventListener('click', function() {
  const data = JSON.stringify({ panels: Array.from(panelStateMap.values()), exportedAt: Date.now() }, null, 2);
  navigator.clipboard.writeText(data).then(function() {
    const btn = document.getElementById('btnExport');
    const orig = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(function() { btn.textContent = orig; }, 1500);
  });
});
/* ---------- init ---------- */
const now = Date.now();
reconcileDOM(now);
updateVisibleSet();
startTick();
})();
</script>
</body>
</html>