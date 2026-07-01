<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #242836;
  --border: #2a2e3a;
  --text: #e1e4ea;
  --text2: #8b8fa8;
  --accent: #6c72cb;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100vh; padding: 16px;
  overflow-x: hidden;
}
.toolbar {
  display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
  margin-bottom: 14px; padding: 10px 14px;
  background: var(--surface); border-radius: var(--radius);
  border: 1px solid var(--border);
}
.toolbar h1 { font-size: 1.1rem; font-weight: 600; margin-right: auto; color: var(--accent); }
.toolbar button {
  padding: 6px 14px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--surface2); color: var(--text); cursor: pointer;
  font-size: 0.8rem; transition: background var(--transition);
}
.toolbar button:hover { background: var(--accent); border-color: var(--accent); }
.toolbar .badge {
  font-size: 0.72rem; padding: 3px 8px; border-radius: 12px;
  background: var(--accent2); color: #0f1117; font-weight: 600;
}
#toast {
  position: fixed; bottom: 20px; right: 20px; z-index: 9999;
  max-width: 380px; pointer-events: none;
}
.toast-msg {
  background: var(--surface2); border: 1px solid var(--warn); color: var(--warn);
  padding: 10px 16px; border-radius: var(--radius); margin-top: 6px;
  font-size: 0.78rem; animation: slideIn 0.3s ease;
}
.toast-msg.error { border-color: var(--danger); color: var(--danger); }
@keyframes slideIn { from { opacity:0; transform:translateX(40px); } to { opacity:1; transform:translateX(0); } }
.grid {
  display: grid; gap: var(--gap);
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
  transition: all var(--transition);
}
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 14px;
  position: relative; overflow: hidden;
  transition: all var(--transition);
  cursor: grab; display: flex; flex-direction: column;
  min-height: 120px;
}
.panel:active { cursor: grabbing; }
.panel.dragging { opacity: 0.5; z-index: 100; transform: scale(0.97); }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }
.panel.locked { border-color: var(--accent2); }
.panel.compact { grid-row: span 1; min-height: 60px; padding: 8px 12px; font-size: 0.75rem; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-header { margin-bottom: 0; }
.panel.large { grid-column: span 2; grid-row: span 2; }
.panel.xlarge { grid-column: span 2; grid-row: span 3; }
.panel-header {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 10px; font-weight: 600; font-size: 0.85rem;
  justify-content: space-between;
}
.panel-title { display: flex; align-items: center; gap: 6px; }
.panel-rank {
  font-size: 0.65rem; padding: 2px 6px; border-radius: 4px;
  background: var(--accent); color: #fff;
}
.panel-body { flex: 1; font-size: 0.8rem; color: var(--text2); }
.panel-body .metric-value { font-size: 1.6rem; font-weight: 700; color: var(--text); margin: 6px 0; }
.panel-body .spark { height: 40px; background: linear-gradient(90deg, var(--accent), var(--accent2)); border-radius: 4px; margin-top: 8px; opacity: 0.5; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none; border: none; color: var(--text2); cursor: pointer;
  font-size: 0.75rem; padding: 2px 6px; border-radius: 4px;
  transition: all var(--transition);
}
.panel-actions button:hover { color: var(--text); background: var(--surface2); }
.panel-actions button.active { color: var(--accent2); }
.lock-icon { font-size: 0.7rem; }
.compact-indicator { display: none; font-size: 0.65rem; color: var(--warn); }
.panel.compact .compact-indicator { display: inline; }
@media (max-width: 900px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <span class="badge" id="sessionBadge">session 1</span>
  <button onclick="resetAll()">Reset Layout</button>
  <button onclick="exportData()">Export Data</button>
  <button onclick="toggleAutoArrange()" id="autoBtn">Auto: ON</button>
</div>
<div class="grid" id="grid"></div>
<div id="toast"></div>
<script>
(function(){
'use strict';
// ─── STORAGE ENGINE (with quota-exceeded + corruption recovery) ───
const STORAGE_KEY = 'adaptive_dashboard_v2';
let memoryStore = null; // fallback when localStorage fails
let storageAvailable = true;
function storageGet() {
  if (memoryStore !== null) return JSON.parse(JSON.stringify(memoryStore));
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch (e) {
    if (e.name === 'QuotaExceededError') {
      toast('localStorage full — switched to in-memory mode. Data lost on tab close.', 'error');
      storageAvailable = false;
      return memoryStore ? JSON.parse(JSON.stringify(memoryStore)) : null;
    }
    toast('Corrupt storage detected — resetting tracking data.', 'error');
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
    return null;
  }
}
function storageSet(data) {
  memoryStore = JSON.parse(JSON.stringify(data));
  if (!storageAvailable) return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    if (e.name === 'QuotaExceededError') {
      storageAvailable = false;
      toast('localStorage quota exceeded — switched to in-memory mode.', 'error');
    } else {
      toast('Failed to persist layout: ' + e.message, 'error');
    }
  }
}
function toast(msg, type) {
  const el = document.getElementById('toast');
  const div = document.createElement('div');
  div.className = 'toast-msg' + (type === 'error' ? ' error' : '');
  div.textContent = msg;
  el.appendChild(div);
  setTimeout(function(){ div.remove(); }, 4000);
}
// ─── PANEL DEFINITIONS ───
const PANEL_DEFS = [
  { id: 'revenue',     title: 'Revenue',        icon: '\u{1F4B0}', metric: '$48,293', detail: '+12.3% vs last month' },
  { id: 'users',       title: 'Active Users',   icon: '\u{1F465}', metric: '2,847',   detail: '+8.1% weekly growth' },
  { id: 'conversion',  title: 'Conversion',      icon: '\u{1F3AF}', metric: '3.24%',   detail: '+0.4% improvement' },
  { id: 'churn',       title: 'Churn Rate',      icon: '\u{1F4C9}', metric: '1.8%',    detail: '-0.3% from last period' },
  { id: 'sessions',    title: 'Sessions',        icon: '\u{1F4CA}', metric: '12.4K',   detail: 'Avg duration 4m 32s' },
  { id: 'bounce',      title: 'Bounce Rate',     icon: '\u{1F53D}', metric: '42.1%',   detail: '-2.1% improvement' },
  { id: 'latency',     title: 'API Latency',     icon: '\u{26A1}',  metric: '87ms',    detail: 'p99: 210ms' },
  { id: 'errors',      title: 'Error Rate',      icon: '\u{274C}',  metric: '0.12%',   detail: 'Below SLO threshold' },
];
// ─── STATE ───
let tracking = {};      // panelId -> { views, totalViewMs, lastViewed, interactions, expandCount, collapseCount }
let manualOverrides = {}; // panelId -> { locked, row, col, rowSpan, colSpan }
let autoArrange = true;
let sessionStart = Date.now();
let sessionCount = 1;
// ─── COLD-START INIT ───
function initTracking() {
  const stored = storageGet();
  if (stored && stored.tracking && Object.keys(stored.tracking).length > 0) {
    tracking = stored.tracking;
    manualOverrides = stored.manualOverrides || {};
    autoArrange = stored.autoArrange !== false;
    sessionCount = (stored.sessionCount || 0) + 1;
  } else {
    PANEL_DEFS.forEach(function(p){
      tracking[p.id] = { views: 0, totalViewMs: 0, lastViewed: 0, interactions: 0, expandCount: 0, collapseCount: 0 };
    });
    sessionCount = 1;
  }
  persistState();
  document.getElementById('sessionBadge').textContent = 'session ' + sessionCount;
  document.getElementById('autoBtn').textContent = 'Auto: ' + (autoArrange ? 'ON' : 'OFF');
}
function persistState() {
  storageSet({ tracking: tracking, manualOverrides: manualOverrides, autoArrange: autoArrange, sessionCount: sessionCount });
}
// ─── RANKING ALGORITHM ───
function computeScore(panelId) {
  var t = tracking[panelId];
  if (!t) return 0;
  var now = Date.now();
  var hoursSinceLastView = Math.max(0.1, (now - t.lastViewed) / 3600000);
  var recency = 1 / (1 + Math.log(1 + hoursSinceLastView));
  var freq = Math.log(1 + t.views + t.interactions * 0.5);
  var dur = Math.log(1 + t.totalViewMs / 1000);
  var engagement = (t.expandCount + 1) / (t.collapseCount + 1);
  return freq * dur * recency * engagement;
}
function rankPanels() {
  var scored = PANEL_DEFS.map(function(p){ return { id: p.id, score: computeScore(p.id) }; });
  scored.sort(function(a,b){ return b.score - a.score; });
  var ranks = {};
  scored.forEach(function(item, i){ ranks[item.id] = i + 1; });
  return { scored: scored, ranks: ranks };
}
// ─── LAYOUT ENGINE ───
function getLayoutClass(rank, total) {
  var ratio = (rank - 1) / total; // 0 = top rank, 1 = lowest
  if (ratio < 0.25) return 'xlarge';
  if (ratio < 0.5) return 'large';
  if (ratio < 0.75) return '';
  return 'compact';
}
function arrangeGrid() {
  var ranked = rankPanels();
  var total = PANEL_DEFS.length;
  var order = ranked.scored.map(function(item){ return item.id; });
  var grid = document.getElementById('grid');
  var existing = {};
  grid.querySelectorAll('.panel').forEach(function(el){ existing[el.dataset.pid] = el; });
  grid.innerHTML = '';
  order.forEach(function(pid, idx){
    var def = PANEL_DEFS.find(function(d){ return d.id === pid; });
    var rank = idx + 1;
    var cls = '';
    if (autoArrange && !(manualOverrides[pid] && manualOverrides[pid].locked)) {
      cls = getLayoutClass(rank, total);
    }
    var locked = manualOverrides[pid] && manualOverrides[pid].locked;
    var panel = document.createElement('div');
    panel.className = 'panel ' + cls + (locked ? ' locked' : '');
    panel.dataset.pid = pid;
    panel.draggable = true;
    panel.innerHTML =
      '<div class="panel-header">' +
        '<div class="panel-title">' +
          '<span>' + def.icon + '</span>' +
          '<span>' + def.title + '</span>' +
          '<span class="panel-rank">#' + rank + '</span>' +
          '<span class="compact-indicator">\u{1F4E6} compact</span>' +
        '</div>' +
        '<div class="panel-actions">' +
          '<button class="lock-btn' + (locked ? ' active' : '') + '" data-action="lock" title="Lock position">\u{1F512}</button>' +
          '<button data-action="expand" title="Expand">\u{2197}</button>' +
          '<button data-action="collapse" title="Collapse">\u{2198}</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body">' +
        '<div class="metric-value">' + def.metric + '</div>' +
        '<div>' + def.detail + '</div>' +
        '<div class="spark" style="width:' + (30 + Math.random() * 70) + '%;"></div>' +
      '</div>';
    grid.appendChild(panel);
  });
  bindPanelEvents();
}
// ─── INTERSECTION OBSERVER (single strategy for all visibility tracking) ───
// Rationale: IntersectionObserver provides reliable viewport visibility detection
// with configurable thresholds, works for all tracking cases (view duration, compact
// detection, lazy-loading), and is more performant than polling or MutationObserver
// for visibility changes. A single observer covers all panels uniformly.
var observer = new IntersectionObserver(function(entries){
  entries.forEach(function(entry){
    var pid = entry.target.dataset.pid;
    if (!pid) return;
    if (entry.isIntersecting) {
      entry.target.dataset.visibleSince = Date.now();
      if (!tracking[pid]) return;
      tracking[pid].views++;
      tracking[pid].lastViewed = Date.now();
    } else {
      var since = parseInt(entry.target.dataset.visibleSince, 10);
      if (since) {
        var duration = Date.now() - since;
        if (tracking[pid]) tracking[pid].totalViewMs += duration;
        entry.target.dataset.visibleSince = '';
      }
    }
    persistState();
    if (autoArrange) debounceArrange();
  });
}, { threshold: 0.3 });
// ─── DEBOUNCE ARRANGE ───
var arrangeTimeout = null;
function debounceArrange() {
  if (arrangeTimeout) clearTimeout(arrangeTimeout);
  arrangeTimeout = setTimeout(function(){
    arrangeGrid();
    arrangeTimeout = null;
  }, 2000);
}
// ─── EVENT HANDLERS ───
function bindPanelEvents() {
  document.querySelectorAll('.panel').forEach(function(panel){
    // Interaction tracking
    panel.addEventListener('click', function(e){
      if (e.target.closest('button')) return;
      var pid = panel.dataset.pid;
      if (tracking[pid]) tracking[pid].interactions++;
      panel.style.boxShadow = '0 0 0 2px var(--accent)';
      setTimeout(function(){ panel.style.boxShadow = ''; }, 300);
      persistState();
    });
    // Action buttons
    panel.addEventListener('click', function(e){
      var btn = e.target.closest('button');
      if (!btn) return;
      e.stopPropagation();
      var pid = panel.dataset.pid;
      var action = btn.dataset.action;
      if (action === 'lock') {
        if (!manualOverrides[pid]) manualOverrides[pid] = {};
        manualOverrides[pid].locked = !manualOverrides[pid].locked;
        btn.classList.toggle('active', manualOverrides[pid].locked);
        panel.classList.toggle('locked', manualOverrides[pid].locked);
        persistState();
        if (!manualOverrides[pid].locked && autoArrange) debounceArrange();
      } else if (action === 'expand') {
        panel.classList.remove('compact');
        if (tracking[pid]) tracking[pid].expandCount++;
        if (manualOverrides[pid]) manualOverrides[pid].compactForced = false;
        persistState();
      } else if (action === 'collapse') {
        panel.classList.add('compact');
        if (tracking[pid]) tracking[pid].collapseCount++;
        if (manualOverrides[pid]) manualOverrides[pid].compactForced = true;
        persistState();
      }
    });
    // Drag-drop swap
    panel.addEventListener('dragstart', function(e){
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', panel.dataset.pid);
    });
    panel.addEventListener('dragend', function(e){
      panel.classList.remove('dragging');
      document.querySelectorAll('.panel').forEach(function(p){ p.classList.remove('drag-over'); });
    });
    panel.addEventListener('dragover', function(e){
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      panel.classList.add('drag-over');
    });
    panel.addEventListener('dragleave', function(){
      panel.classList.remove('drag-over');
    });
    panel.addEventListener('drop', function(e){
      e.preventDefault();
      panel.classList.remove('drag-over');
      var srcPid = e.dataTransfer.getData('text/plain');
      var dstPid = panel.dataset.pid;
      if (srcPid === dstPid) return;
      // Swap positions in grid
      var grid = document.getElementById('grid');
      var srcEl = grid.querySelector('[data-pid="' + srcPid + '"]');
      var dstEl = grid.querySelector('[data-pid="' + dstPid + '"]');
      if (!srcEl || !dstEl) return;
      if (dstEl.nextSibling === srcEl) {
        grid.insertBefore(srcEl, dstEl);
      } else if (srcEl.nextSibling === dstEl) {
        grid.insertBefore(dstEl, srcEl);
      } else {
        var ref = dstEl.nextSibling;
        grid.insertBefore(dstEl, srcEl);
        grid.insertBefore(srcEl, ref);
      }
      // Lock both after manual swap
      if (!manualOverrides[srcPid]) manualOverrides[srcPid] = {};
      if (!manualOverrides[dstPid]) manualOverrides[dstPid] = {};
      manualOverrides[srcPid].locked = true;
      manualOverrides[dstPid].locked = true;
      document.querySelectorAll('.panel').forEach(function(p){
        if (p.dataset.pid === srcPid || p.dataset.pid === dstPid) {
          p.classList.add('locked');
          var lb = p.querySelector('.lock-btn');
          if (lb) lb.classList.add('active');
        }
      });
      persistState();
      toast('Panels swapped & locked. Unlock to resume auto-layout.');
    });
    // Observe for visibility tracking
    observer.observe(panel);
  });
}
// ─── TOOLBAR ACTIONS ───
window.resetAll = function(){
  tracking = {};
  manualOverrides = {};
  autoArrange = true;
  PANEL_DEFS.forEach(function(p){
    tracking[p.id] = { views: 0, totalViewMs: 0, lastViewed: 0, interactions: 0, expandCount: 0, collapseCount: 0 };
  });
  try { localStorage.removeItem(STORAGE_KEY); } catch(_) {}
  memoryStore = null;
  storageAvailable = true;
  document.getElementById('autoBtn').textContent = 'Auto: ON';
  arrangeGrid();
  toast('Tracking data reset.');
};
window.exportData = function(){
  var data = { tracking: tracking, overrides: manualOverrides, autoArrange: autoArrange, exportedAt: new Date().toISOString() };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = 'dashboard-data-' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
};
window.toggleAutoArrange = function(){
  autoArrange = !autoArrange;
  document.getElementById('autoBtn').textContent = 'Auto: ' + (autoArrange ? 'ON' : 'OFF');
  persistState();
  if (autoArrange) arrangeGrid();
  toast(autoArrange ? 'Auto-arrange enabled.' : 'Auto-arrange paused. Manual layout preserved.');
};
// ─── BOOT ───
initTracking();
arrangeGrid();
})();
</script>
</body>
</html>