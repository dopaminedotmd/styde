<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent-dim: #1f6feb;
  --danger: #f85149;
  --success: #3fb950;
  --warn: #d2991d;
  --panel-large: 2;
  --panel-medium: 1;
  --panel-compact: 0.5;
  --gap: 12px;
  --radius: 8px;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--bg);
  color:var(--text);
  font-family:system-ui,-apple-system,sans-serif;
  min-height:100vh;
  padding:16px;
}
#toolbar{
  display:flex;
  gap:8px;
  margin-bottom:16px;
  flex-wrap:wrap;
  align-items:center;
}
#toolbar button{
  background:var(--surface);
  color:var(--text);
  border:1px solid var(--border);
  padding:6px 14px;
  border-radius:6px;
  cursor:pointer;
  font-size:13px;
  transition:background var(--transition);
}
#toolbar button:hover{background:var(--accent-dim);border-color:var(--accent)}
#toolbar button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
#summary-bar{
  display:flex;
  gap:16px;
  margin-bottom:12px;
  font-size:12px;
  color:var(--text-dim);
  flex-wrap:wrap;
}
#summary-bar span{background:var(--surface);padding:4px 10px;border-radius:4px;border:1px solid var(--border)}
#dashboard{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:var(--gap);
  transition:grid-template-columns var(--transition);
}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  overflow:hidden;
  transition:all var(--transition);
  display:flex;
  flex-direction:column;
  min-height:160px;
  position:relative;
}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 1;grid-row:span 1}
.panel.compact{grid-column:span 1;grid-row:span 1;opacity:0.7;min-height:80px}
.panel.compact .panel-body{font-size:11px;padding:8px}
.panel.compact .metric-value{font-size:18px}
.panel.collapsed{min-height:44px}
.panel.collapsed .panel-body{display:none}
.panel.collapsed .panel-footer{display:none}
.panel.locked{border-color:var(--warn);box-shadow:0 0 0 1px var(--warn)}
.panel.dragging{opacity:0.5;z-index:10}
.panel-header{
  display:flex;
  align-items:center;
  gap:6px;
  padding:8px 12px;
  border-bottom:1px solid var(--border);
  cursor:grab;
  font-size:13px;
  font-weight:600;
  user-select:none;
}
.panel-header:active{cursor:grabbing}
.panel-header .drag-handle{color:var(--text-dim);cursor:grab;font-size:14px}
.panel-header .panel-title{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header button{
  background:none;
  border:none;
  color:var(--text-dim);
  cursor:pointer;
  font-size:16px;
  padding:2px 6px;
  border-radius:4px;
  line-height:1;
  transition:color 0.15s;
}
.panel-header button:hover{color:var(--text)}
.panel-header button.lock-btn.locked{color:var(--warn)}
.panel-body{
  padding:12px;
  flex:1;
  display:flex;
  flex-direction:column;
  gap:8px;
  transition:all var(--transition);
}
.metric-value{font-size:28px;font-weight:700;color:var(--accent)}
.metric-label{font-size:12px;color:var(--text-dim)}
.metric-spark{height:40px;background:linear-gradient(90deg,var(--accent-dim),var(--accent));border-radius:4px;opacity:0.4}
.panel-footer{
  padding:4px 12px;
  font-size:10px;
  color:var(--text-dim);
  border-top:1px solid var(--border);
  display:flex;
  justify-content:space-between;
}
.score-indicator{
  display:inline-block;
  width:6px;
  height:6px;
  border-radius:50%;
  margin-right:4px;
}
.score-indicator.high{background:var(--success)}
.score-indicator.mid{background:var(--warn)}
.score-indicator.low{background:var(--danger)}
#drag-ghost{
  position:fixed;
  pointer-events:none;
  z-index:1000;
  opacity:0.85;
  transform:translate(-50%,-50%);
  display:none;
}
</style>
</head>
<body>
<div id="toolbar">
  <button id="btn-reset" title="Reset all tracking data">Reset</button>
  <button id="btn-export" title="Export layout to clipboard">Export</button>
  <button id="btn-import-file" title="Import layout from file">Import</button>
  <button id="btn-unlock-all" title="Unlock all panels">Unlock All</button>
  <span style="font-size:12px;color:var(--text-dim);margin-left:auto" id="last-ranked">Last rank: --</span>
</div>
<div id="summary-bar">
  <span id="sum-total">Panels: 0</span>
  <span id="sum-large">Large: 0</span>
  <span id="sum-compact">Compact: 0</span>
  <span id="sum-locked">Locked: 0</span>
  <span id="sum-high">Score >50: 0</span>
</div>
<div id="dashboard"></div>
<div id="drag-ghost"></div>
<script>
'use strict';
// ── State ────────────────────────────────────────────────────
const STORAGE_KEY = 'adaptive_dashboard_v1';
const RANK_INTERVAL = 30000;
const COMPACT_THRESHOLD = 0.25;  // bottom 25% => compact
const COLLAPSE_THRESHOLD = 0.10; // bottom 10% => collapsed
const LARGE_THRESHOLD = 0.60;    // top 40% => large
const RECENCY_HALFLIFE = 86400000; // 24h in ms
let state = {
  panels: [],
  layoutOrder: [],
  manualOverrides: {}, // panelId -> {locked:bool, position:num}
  lastRanked: 0
};
// ── Cached DOM refs (single querySelector, per feedback) ────
const dom = {};
function cacheDom() {
  dom.dashboard = document.getElementById('dashboard');
  dom.summaryBar = document.getElementById('summary-bar');
  dom.sumTotal = document.getElementById('sum-total');
  dom.sumLarge = document.getElementById('sum-large');
  dom.sumCompact = document.getElementById('sum-compact');
  dom.sumLocked = document.getElementById('sum-locked');
  dom.sumHigh = document.getElementById('sum-high');
  dom.lastRanked = document.getElementById('last-ranked');
  dom.dragGhost = document.getElementById('drag-ghost');
}
cacheDom();
// ── Default panels ───────────────────────────────────────────
function defaultPanels() {
  const names = [
    'CPU Usage', 'Memory', 'Disk I/O', 'Network',
    'Requests/s', 'Error Rate', 'Latency p95', 'Active Users',
    'Throughput', 'Queue Depth', 'Cache Hit %', 'Uptime'
  ];
  return names.map((n, i) => ({
    id: 'p' + i,
    title: n,
    value: (Math.random() * 100).toFixed(1) + (n.includes('%') || n.includes('Rate') ? '%' : n.includes('Users') ? '' : n.includes('Uptime') ? '%' : 'ms'),
    interactions: 0,
    viewDurationMs: 0,
    lastInteraction: 0,
    score: 0,
    size: 'medium',
    locked: false
  }));
}
// ── Persistence ──────────────────────────────────────────────
function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      panels: state.panels,
      manualOverrides: state.manualOverrides,
      layoutOrder: state.layoutOrder,
      lastRanked: state.lastRanked
    }));
  } catch(e) { /* quota exceeded, silent */ }
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    const data = JSON.parse(raw);
    state.panels = data.panels || defaultPanels();
    state.manualOverrides = data.manualOverrides || {};
    state.layoutOrder = data.layoutOrder || [];
    state.lastRanked = data.lastRanked || 0;
    return true;
  } catch(e) { return false; }
}
// ── Scoring (frequency × duration × recency) ─────────────────
function computeRecencyFactor(lastTs) {
  if (!lastTs) return 0.1;
  const age = Date.now() - lastTs;
  return Math.exp(-age / RECENCY_HALFLIFE);
}
function rankPanels() {
  const now = Date.now();
  state.panels.forEach(p => {
    const freq = Math.log2(p.interactions + 2);
    const dur = Math.log2((p.viewDurationMs / 1000) + 2);
    const recency = computeRecencyFactor(p.lastInteraction);
    p.score = +(freq * dur * recency * 10).toFixed(1);
  });
  // Sort by score descending
  const sorted = [...state.panels].sort((a, b) => b.score - a.score);
  const total = sorted.length;
  sorted.forEach((p, idx) => {
    if (state.manualOverrides[p.id]?.locked) return; // skip locked
    const percentile = idx / total;
    if (percentile < (1 - LARGE_THRESHOLD)) p.size = 'large';
    else if (percentile >= (1 - COLLAPSE_THRESHOLD)) p.size = 'collapsed';
    else if (percentile >= (1 - COMPACT_THRESHOLD)) p.size = 'compact';
    else p.size = 'medium';
  });
  state.layoutOrder = sorted.map(p => p.id);
  state.lastRanked = now;
}
// ── Targeted DOM updates (no full re-render) ─────────────────
function updatePanelDOM(panel, el) {
  // Patch only what changed — no innerHTML
  if (!el) return;
  el.className = 'panel ' + panel.size + (panel.locked ? ' locked' : '');
  const titleEl = el.querySelector('.panel-title');
  if (titleEl) titleEl.textContent = panel.title;
  const valueEl = el.querySelector('.metric-value');
  if (valueEl) valueEl.textContent = panel.value;
  const footEl = el.querySelector('.panel-footer');
  if (footEl) {
    const scoreClass = panel.score > 50 ? 'high' : panel.score > 20 ? 'mid' : 'low';
    footEl.innerHTML = '<span><span class="score-indicator '+scoreClass+'"></span>Score: '+panel.score.toFixed(1)+'</span><span>Views: '+panel.interactions+'</span>';
  }
  const lockBtn = el.querySelector('.lock-btn');
  if (lockBtn) {
    lockBtn.textContent = panel.locked ? '🔒' : '🔓';
    lockBtn.classList.toggle('locked', panel.locked);
  }
  const compactBtn = el.querySelector('.compact-btn');
  if (compactBtn) {
    compactBtn.textContent = panel.size === 'collapsed' ? '▶' : panel.size === 'compact' ? '⊞' : '⊟';
  }
}
function applyLayout() {
  const ids = state.layoutOrder;
  const fragment = document.createDocumentFragment();
  ids.forEach(id => {
    let el = dom.dashboard.querySelector('[data-panel-id="'+id+'"]');
    const panel = state.panels.find(p => p.id === id);
    if (!panel) return;
    if (!el) {
      // Create new panel element (only on first render)
      el = document.createElement('div');
      el.setAttribute('data-panel-id', id);
      el.className = 'panel ' + panel.size + (panel.locked ? ' locked' : '');
      el.draggable = true;
      el.innerHTML =
        '<div class="panel-header">' +
          '<span class="drag-handle">⠿</span>' +
          '<span class="panel-title"></span>' +
          '<button class="compact-btn" title="Toggle compact/collapse">⊟</button>' +
          '<button class="lock-btn" title="Lock position">🔓</button>' +
        '</div>' +
        '<div class="panel-body">' +
          '<div class="metric-value"></div>' +
          '<div class="metric-label"></div>' +
          '<div class="metric-spark"></div>' +
        '</div>' +
        '<div class="panel-footer"></div>';
      fragment.appendChild(el);
    }
    updatePanelDOM(panel, el);
  });
  if (fragment.children.length > 0) {
    dom.dashboard.appendChild(fragment);
  }
  // Reorder existing elements in DOM
  ids.forEach((id, idx) => {
    const el = dom.dashboard.querySelector('[data-panel-id="'+id+'"]');
    if (el && Array.from(dom.dashboard.children).indexOf(el) !== idx) {
      dom.dashboard.insertBefore(el, dom.dashboard.children[idx] || null);
    }
  });
  updateSummary();
}
function updateSummary() {
  const panels = state.panels;
  const total = panels.length;
  const large = panels.filter(p => p.size === 'large').length;
  const compact = panels.filter(p => p.size === 'compact').length;
  const locked = panels.filter(p => p.locked).length;
  const high = panels.filter(p => p.score > 50).length;
  dom.sumTotal.textContent = 'Panels: ' + total;
  dom.sumLarge.textContent = 'Large: ' + large;
  dom.sumCompact.textContent = 'Compact: ' + compact;
  dom.sumLocked.textContent = 'Locked: ' + locked;
  dom.sumHigh.textContent = 'Score >50: ' + high;
  dom.lastRanked.textContent = 'Last rank: ' + (state.lastRanked ? new Date(state.lastRanked).toLocaleTimeString() : '--');
}
// ── Tracking ─────────────────────────────────────────────────
let observer = null;
let visibilityMap = new Map(); // panelId -> {enterTime, accumulated}
function setupTracking() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    const now = Date.now();
    entries.forEach(entry => {
      const id = entry.target.getAttribute('data-panel-id');
      if (!id) return;
      let data = visibilityMap.get(id) || { enterTime: 0, accumulated: 0 };
      if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
        data.enterTime = now;
      } else if (data.enterTime > 0) {
        data.accumulated += now - data.enterTime;
        data.enterTime = 0;
        const panel = state.panels.find(p => p.id === id);
        if (panel) {
          panel.viewDurationMs = data.accumulated;
          saveState();
        }
      }
      visibilityMap.set(id, data);
    });
  }, { threshold: [0, 0.5] });
  // Observe all panels
  dom.dashboard.querySelectorAll('[data-panel-id]').forEach(el => observer.observe(el));
}
// Re-setup tracking after any DOM mutation
const trackingObserver = new MutationObserver(() => {
  setupTracking();
});
trackingObserver.observe(dom.dashboard, { childList: true });
// Click tracking via delegation (single listener)
dom.dashboard.addEventListener('click', (e) => {
  const panelEl = e.target.closest('[data-panel-id]');
  if (!panelEl) return;
  const id = panelEl.getAttribute('data-panel-id');
  const panel = state.panels.find(p => p.id === id);
  if (!panel) return;
  panel.interactions++;
  panel.lastInteraction = Date.now();
  // Handle button clicks
  if (e.target.classList.contains('lock-btn')) {
    panel.locked = !panel.locked;
    if (panel.locked) {
      state.manualOverrides[id] = { locked: true, position: state.layoutOrder.indexOf(id) };
    } else {
      delete state.manualOverrides[id];
    }
    updatePanelDOM(panel, panelEl);
    updateSummary();
    saveState();
    return;
  }
  if (e.target.classList.contains('compact-btn')) {
    const sizes = ['large', 'medium', 'compact', 'collapsed'];
    const cur = sizes.indexOf(panel.size);
    panel.size = sizes[(cur + 1) % sizes.length];
    if (panel.size !== 'large' && !state.manualOverrides[id]) {
      state.manualOverrides[id] = { locked: false, position: state.layoutOrder.indexOf(id) };
    }
    updatePanelDOM(panel, panelEl);
    updateSummary();
    saveState();
    return;
  }
  // General interaction
  saveState();
});
// ── Drag and Drop ────────────────────────────────────────────
let dragState = null;
dom.dashboard.addEventListener('dragstart', (e) => {
  const panelEl = e.target.closest('[data-panel-id]');
  if (!panelEl) { e.preventDefault(); return; }
  dragState = {
    id: panelEl.getAttribute('data-panel-id'),
    el: panelEl
  };
  panelEl.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragState.id);
  // Set ghost
  dom.dragGhost.style.display = 'block';
  dom.dragGhost.textContent = panelEl.querySelector('.panel-title')?.textContent || '';
  dom.dragGhost.style.width = panelEl.offsetWidth + 'px';
  dom.dragGhost.style.height = '40px';
  dom.dragGhost.style.background = 'var(--accent-dim)';
  dom.dragGhost.style.borderRadius = '6px';
  dom.dragGhost.style.color = '#fff';
  dom.dragGhost.style.display = 'flex';
  dom.dragGhost.style.alignItems = 'center';
  dom.dragGhost.style.justifyContent = 'center';
  dom.dragGhost.style.fontWeight = '600';
  dom.dragGhost.style.fontSize = '13px';
  e.dataTransfer.setDragImage(dom.dragGhost, 0, 0);
});
dom.dashboard.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});
dom.dashboard.addEventListener('drop', (e) => {
  e.preventDefault();
  if (!dragState) return;
  const targetEl = e.target.closest('[data-panel-id]');
  if (!targetEl || targetEl === dragState.el) { cleanupDrag(); return; }
  const targetId = targetEl.getAttribute('data-panel-id');
  const srcIdx = state.layoutOrder.indexOf(dragState.id);
  const tgtIdx = state.layoutOrder.indexOf(targetId);
  if (srcIdx >= 0 && tgtIdx >= 0) {
    state.layoutOrder.splice(srcIdx, 1);
    state.layoutOrder.splice(tgtIdx, 0, dragState.id);
    // Lock the dragged panel at new position
    const panel = state.panels.find(p => p.id === dragState.id);
    if (panel) {
      panel.locked = true;
      state.manualOverrides[dragState.id] = { locked: true, position: tgtIdx };
    }
    applyLayout();
    saveState();
  }
  cleanupDrag();
});
dom.dashboard.addEventListener('dragend', cleanupDrag);
function cleanupDrag() {
  if (dragState) {
    dragState.el.classList.remove('dragging');
    dom.dragGhost.style.display = 'none';
    dragState = null;
  }
}
// ── Toolbar actions ──────────────────────────────────────────
document.getElementById('btn-reset').addEventListener('click', () => {
  state.panels = defaultPanels();
  state.layoutOrder = [];
  state.manualOverrides = {};
  visibilityMap.clear();
  dom.dashboard.innerHTML = '';
  rankPanels();
  applyLayout();
  saveState();
});
document.getElementById('btn-export').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(state, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'dashboard-layout-' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
});
document.getElementById('btn-import-file').addEventListener('click', () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const data = JSON.parse(ev.target.result);
        state.panels = data.panels || state.panels;
        state.manualOverrides = data.manualOverrides || {};
        state.layoutOrder = data.layoutOrder || [];
        state.lastRanked = data.lastRanked || 0;
        visibilityMap.clear();
        dom.dashboard.innerHTML = '';
        applyLayout();
        saveState();
      } catch(ex) { console.warn('Import failed:', ex); }
    };
    reader.readAsText(file);
  };
  input.click();
});
document.getElementById('btn-unlock-all').addEventListener('click', () => {
  state.panels.forEach(p => { p.locked = false; });
  state.manualOverrides = {};
  rankPanels();
  applyLayout();
  saveState();
});
// ── Periodic ranking (rAF-coalesced) ─────────────────────────
let rankScheduled = false;
function scheduleRank() {
  if (rankScheduled) return;
  rankScheduled = true;
  requestAnimationFrame(() => {
    rankPanels();
    applyLayout();
    saveState();
    rankScheduled = false;
  });
}
setInterval(scheduleRank, RANK_INTERVAL);
// ── Bootstrap ────────────────────────────────────────────────
(function init() {
  const loaded = loadState();
  if (!loaded || state.panels.length === 0) {
    state.panels = defaultPanels();
  }
  rankPanels();
  applyLayout();
  setupTracking();
  saveState();
})();
// ── Periodic value simulation (demo only) ────────────────────
setInterval(() => {
  state.panels.forEach(p => {
    const base = parseFloat(p.value) || 0;
    const delta = (Math.random() - 0.5) * base * 0.1;
    const next = Math.max(0, +(base + delta).toFixed(1));
    p.value = next + (p.title.includes('%') || p.title.includes('Rate') ? '%' : p.title.includes('Users') ? '' : p.title.includes('Uptime') ? '%' : 'ms');
    const el = dom.dashboard.querySelector('[data-panel-id="'+p.id+'"] .metric-value');
    if (el) el.textContent = p.value;
  });
}, 3000);
// Visibility tracking: flush on page unload
window.addEventListener('beforeunload', () => {
  const now = Date.now();
  visibilityMap.forEach((data, id) => {
    if (data.enterTime > 0) {
      data.accumulated += now - data.enterTime;
      const panel = state.panels.find(p => p.id === id);
      if (panel) panel.viewDurationMs = data.accumulated;
    }
  });
  saveState();
});
</script>
</body>
</html>