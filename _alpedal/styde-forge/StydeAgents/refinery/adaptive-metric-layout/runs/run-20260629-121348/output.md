<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #c9d1d9; --text-dim: #8b949e; --accent: #58a6ff;
  --accent-glow: rgba(88,166,255,0.15); --danger: #f85149;
  --success: #3fb950; --warn: #d2991d; --radius: 8px;
  --gap: 12px; --header-h: 48px; --compact-scale: 0.45;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  overflow-x: hidden;
}
header {
  height: var(--header-h); background: var(--surface); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; padding: 0 20px; gap: 16px; position: sticky; top:0; z-index:100;
}
header .logo { font-weight: 700; font-size: 15px; letter-spacing: -0.3px; color: var(--accent); }
header .stats { display: flex; gap: 20px; font-size: 12px; color: var(--text-dim); margin-left: auto; }
header .stats span { color: var(--text); font-weight: 600; white-space: nowrap; }
.btn {
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px;
  font-weight: 500; transition: background 0.15s, border-color 0.15s;
}
.btn:hover { background: #1c2333; border-color: #484f58; }
.btn.accent { border-color: var(--accent); color: var(--accent); }
.btn.accent:hover { background: rgba(88,166,255,0.1); }
.btn.danger { border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: rgba(248,81,73,0.1); }
.grid {
  display: grid; gap: var(--gap); padding: var(--gap);
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  grid-auto-flow: dense;
  transition: grid-template-columns var(--transition);
}
@media (max-width: 1400px) { .grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 1000px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px)  { .grid { grid-template-columns: 1fr; } }
.panel {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  display: flex; flex-direction: column; overflow: hidden;
  transition: transform var(--transition), opacity var(--transition), box-shadow var(--transition);
  position: relative; min-height: 180px;
}
.panel:hover { border-color: #484f58; }
.panel.dominant {
  grid-column: span 2; grid-row: span 2;
  box-shadow: 0 0 20px var(--accent-glow);
}
.panel.compact {
  transform: scale(var(--compact-scale));
  transform-origin: top left;
  opacity: 0.72;
  min-height: 0;
}
.panel.compact:hover {
  opacity: 1; transform: scale(0.48);
  z-index: 10; box-shadow: 0 4px 24px rgba(0,0,0,0.5);
}
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: '🔒'; position: absolute; top: 6px; right: 34px;
  font-size: 11px; z-index: 5; pointer-events: none;
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; font-size: 13px; font-weight: 600;
  border-bottom: 1px solid var(--border); flex-shrink: 0;
  cursor: grab; user-select: none;
}
.panel-header:active { cursor: grabbing; }
.panel-header .title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.panel-header .actions { display: flex; gap: 4px; flex-shrink: 0; margin-left: 8px; }
.panel-header .actions button {
  background: none; border: none; color: var(--text-dim); cursor: pointer;
  padding: 2px 5px; border-radius: 4px; font-size: 13px; line-height: 1;
  transition: color 0.15s, background 0.15s;
}
.panel-header .actions button:hover { color: var(--text); background: #1c2333; }
.panel-header .actions .lock-btn.locked { color: var(--warn); }
.panel-body {
  flex: 1; padding: 12px; overflow: auto; display: flex; flex-direction: column; gap: 8px;
  font-size: 12px;
}
.panel.compact .panel-body { font-size: 9px; padding: 6px; gap: 3px; }
.compact-zone {
  grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: var(--gap);
  align-items: flex-start; padding: 8px; border: 1px dashed var(--border);
  border-radius: var(--radius); min-height: 120px;
  position: relative;
}
.compact-zone::before {
  content: 'Compact Zone — low-usage panels'; position: absolute;
  top: -10px; left: 16px; background: var(--bg); padding: 0 8px;
  font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px;
}
.compact-zone .panel {
  width: calc(25% - var(--gap)); min-width: 140px; flex-shrink: 0;
}
.compact-zone .panel.compact { transform: none; opacity: 0.72; }
.compact-zone .panel.compact:hover { transform: scale(1.03); opacity: 1; }
.metric-value { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }
.metric-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.3px; }
.metric-change { font-size: 12px; font-weight: 600; }
.metric-change.up { color: var(--success); }
.metric-change.down { color: var(--danger); }
.sparkline { display: flex; align-items: flex-end; gap: 2px; height: 48px; margin-top: 4px; }
.sparkline .bar {
  flex: 1; background: var(--accent); border-radius: 2px 2px 0 0;
  min-width: 3px; opacity: 0.7; transition: height 0.5s ease;
}
.activity-heat { display: flex; gap: 3px; margin-top: 4px; flex-wrap: wrap; }
.activity-heat .cell {
  width: 10px; height: 10px; border-radius: 2px; background: #1c2333;
  transition: background 0.3s;
}
.activity-heat .cell.hot { background: var(--accent); }
.activity-heat .cell.warm { background: #1f6feb; }
.activity-heat .cell.cool { background: #1c3b5c; }
.usage-bar { height: 3px; background: #1c2333; border-radius: 2px; margin-top: 4px; overflow:hidden; }
.usage-bar .fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.5s ease; }
.rank-badge {
  position: absolute; top: 6px; right: 6px; font-size: 10px; font-weight: 700;
  color: var(--accent); background: rgba(88,166,255,0.12); padding: 1px 6px;
  border-radius: 10px; z-index: 2; pointer-events: none;
}
.drag-ghost { opacity: 0.4; border-style: dashed; }
.drag-over { border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
.toast {
  position: fixed; bottom: 20px; right: 20px; background: var(--surface);
  border: 1px solid var(--accent); border-radius: var(--radius); padding: 10px 18px;
  font-size: 12px; z-index: 1000; opacity: 0; transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.handle { cursor: grab; display: flex; align-items: center; gap: 4px; }
.empty-state { text-align: center; padding: 40px; color: var(--text-dim); font-size: 13px; }
</style>
</head>
<body>
<header>
  <div class="logo">Adaptive Metrics</div>
  <div class="stats">
    <span>Panels: <span id="stat-count">0</span></span>
    <span>Tracked: <span id="stat-tracked">0s</span></span>
    <span>Session: <span id="stat-session">0m</span></span>
  </div>
  <button class="btn accent" id="btn-reset" title="Reset layout to automatic">Reset Layout</button>
  <button class="btn danger" id="btn-clear" title="Clear all tracking data">Clear Data</button>
</header>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v2';
const TRACK_KEY = 'adaptive_tracking_v2';
const DEBOUNCE_MS = 250;
const RECENCY_HALF_LIFE = 7 * 24 * 3600 * 1000;
const COMPACT_RANK_RATIO = 0.35;
const DOMINANT_RANK_RATIO = 0.75;
const MAX_CACHE_ENTRIES = 100;
const CACHE_TTL = 30 * 60 * 1000;
const PANEL_TEMPLATES = [
  { id: 'revenue', title: 'Revenue', type: 'metric', data: { value: '$128.4K', change: '+12.3%', dir:'up', label:'Monthly Recurring' }},
  { id: 'users', title: 'Active Users', type: 'metric', data: { value: '8,421', change: '+5.7%', dir:'up', label:'Daily Active' }},
  { id: 'churn', title: 'Churn Rate', type: 'metric', data: { value: '1.8%', change: '-0.3%', dir:'down', label:'Monthly Churn' }},
  { id: 'latency', title: 'API Latency', type: 'metric', data: { value: '43ms', change: '-8ms', dir:'down', label:'P95 Response' }},
  { id: 'errors', title: 'Error Rate', type: 'metric', data: { value: '0.12%', change: '+0.02%', dir:'up', label:'5xx Errors' }},
  { id: 'cpu', title: 'CPU Usage', type: 'chart', data: { value: '67%', label:'Cluster Avg' }},
  { id: 'memory', title: 'Memory', type: 'chart', data: { value: '54%', label:'Heap Used' }},
  { id: 'requests', title: 'Requests/s', type: 'chart', data: { value: '3,210', label:'Current Load' }},
  { id: 'bandwidth', title: 'Bandwidth', type: 'chart', data: { value: '2.8 Gbps', label:'Egress' }},
  { id: 'sessions', title: 'Sessions', type: 'metric', data: { value: '1,847', change: '-2.1%', dir:'down', label:'Concurrent' }},
  { id: 'conversion', title: 'Conversion', type: 'metric', data: { value: '3.4%', change: '+0.5%', dir:'up', label:'Free→Paid' }},
  { id: 'storage', title: 'Storage', type: 'chart', data: { value: '78%', label:'Disk Usage' }},
];
let panels = [];
let tracking = {};
let layoutCache = new Map();
let sessionStart = Date.now();
let resizeTimer = null;
let toastTimer = null;
let renderedPanels = new Set();
let pendingRender = null;
function cacheGet(key) {
  const entry = layoutCache.get(key);
  if (!entry) return undefined;
  if (Date.now() - entry.ts > CACHE_TTL) { layoutCache.delete(key); return undefined; }
  entry.ts = Date.now();
  return entry.val;
}
function cacheSet(key, val) {
  if (layoutCache.size >= MAX_CACHE_ENTRIES) {
    let oldest = null, oldestTs = Infinity;
    for (const [k, v] of layoutCache) { if (v.ts < oldestTs) { oldestTs = v.ts; oldest = k; } }
    if (oldest) layoutCache.delete(oldest);
  }
  layoutCache.set(key, { val, ts: Date.now() });
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) panels = JSON.parse(raw);
  } catch(e) { panels = []; }
  try {
    const raw = localStorage.getItem(TRACK_KEY);
    if (raw) tracking = JSON.parse(raw);
  } catch(e) { tracking = {}; }
}
function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(panels)); } catch(e) {}
  try { localStorage.setItem(TRACK_KEY, JSON.stringify(tracking)); } catch(e) {}
}
function initDefaultPanels() {
  if (panels.length === 0) {
    panels = PANEL_TEMPLATES.map((t, i) => ({
      ...t,
      locked: false,
      order: i,
      dominant: false,
      compact: false
    }));
  }
  PANEL_TEMPLATES.forEach(t => {
    if (!panels.find(p => p.id === t.id)) {
      panels.push({ ...t, locked: false, order: panels.length, dominant: false, compact: false });
    }
  });
}
function ensureTracking(panelId) {
  if (!tracking[panelId]) {
    tracking[panelId] = {
      views: 0, totalDuration: 0, lastViewed: 0,
      interactions: 0, collapses: 0, expands: 0,
      viewHistory: []
    };
  }
}
function getAttentionScore(panelId) {
  const t = tracking[panelId];
  if (!t) return 0;
  const now = Date.now();
  const recencyDays = (now - t.lastViewed) / 86400000;
  const recencyWeight = Math.exp(-recencyDays * Math.LN2 / (RECENCY_HALF_LIFE / 86400000));
  const freqScore = Math.log1p(t.views) * 10;
  const durScore = Math.log1p(t.totalDuration / 1000) * 5;
  const intScore = Math.log1p(t.interactions) * 3;
  const expandBonus = Math.log1p(t.expands) * 2;
  return (freqScore + durScore + intScore + expandBonus) * recencyWeight;
}
function rankPanels() {
  return panels
    .filter(p => !p.locked)
    .map(p => ({ id: p.id, score: Math.round(getAttentionScore(p.id) * 100) / 100 }))
    .sort((a, b) => b.score - a.score);
}
function assignLayout() {
  const rankings = rankPanels();
  const total = rankings.length || 1;
  rankings.forEach((r, i) => {
    const panel = panels.find(p => p.id === r.id);
    if (!panel || panel.locked) return;
    const ratio = i / total;
    panel.dominant = ratio < DOMINANT_RANK_RATIO * 0.3 && r.score > 0;
    panel.compact = ratio >= COMPACT_RANK_RATIO || r.score <= 0;
    panel.order = i;
  });
}
function buildSparkline(panelId) {
  const t = tracking[panelId];
  if (!t || !t.viewHistory || t.viewHistory.length < 2) {
    const bars = Array.from({length: 12}, () => Math.random() * 0.6 + 0.2);
    return bars.map(h => `<div class="bar" style="height:${(h*100).toFixed(0)}%"></div>`).join('');
  }
  const recent = t.viewHistory.slice(-12);
  const max = Math.max(...recent.map(r=>r.duration||0), 1);
  return recent.map(r => {
    const h = ((r.duration || 0) / max) * 100;
    return `<div class="bar" style="height:${Math.max(3,h).toFixed(0)}%"></div>`;
  }).join('');
}
function buildHeatCells(panelId) {
  const t = tracking[panelId];
  const cells = [];
  for (let i = 0; i < 28; i++) {
    const count = t ? (t.viewHistory || []).filter(v => {
      const day = Math.floor((Date.now() - i*86400000) / 86400000);
      return Math.floor(v.ts / 86400000) === day;
    }).length : 0;
    let cls = '';
    if (count > 5) cls = 'hot';
    else if (count > 2) cls = 'warm';
    else if (count > 0) cls = 'cool';
    cells.push(`<div class="cell ${cls}"></div>`);
  }
  return cells.join('');
}
function buildPanelBody(panel) {
  const track = tracking[panel.id];
  const usagePercent = track ? Math.min(100, Math.round((track.totalDuration / 3600000) * 100)) : 0;
  switch (panel.type) {
    case 'metric':
      return `
        <div class="metric-value">${panel.data.value}</div>
        <div class="metric-label">${panel.data.label}</div>
        <div class="metric-change ${panel.data.dir}">${panel.data.change}</div>
        <div class="usage-bar"><div class="fill" style="width:${usagePercent}%"></div></div>
        <div class="activity-heat">${buildHeatCells(panel.id)}</div>`;
    case 'chart':
      return `
        <div class="metric-value">${panel.data.value}</div>
        <div class="metric-label">${panel.data.label}</div>
        <div class="sparkline">${buildSparkline(panel.id)}</div>
        <div class="usage-bar"><div class="fill" style="width:${usagePercent}%"></div></div>
        <div class="activity-heat">${buildHeatCells(panel.id)}</div>`;
    default:
      return `<div class="metric-value">${panel.data.value||'—'}</div>`;
  }
}
function buildPanelDOM(panel) {
  const rankInfo = rankPanels().find(r => r.id === panel.id);
  const rank = rankInfo ? rankInfo.score.toFixed(1) : '0';
  return `
    <div class="rank-badge">${rank}</div>
    <div class="panel-header" draggable="true" data-panel="${panel.id}">
      <span class="handle">⋮⋮ <span class="title">${panel.title}</span></span>
      <span class="actions">
        <button class="lock-btn${panel.locked?' locked':''}" data-action="lock" data-panel="${panel.id}">${panel.locked?'🔒':'🔓'}</button>
        <button data-action="compact" data-panel="${panel.id}">${panel.compact?'⛶':'⊟'}</button>
      </span>
    </div>
    <div class="panel-body">${buildPanelBody(panel)}</div>`;
}
function getPanelEl(id) {
  return document.querySelector(`.panel[data-id="${id}"]`);
}
function updatePanelDOM(panel) {
  const el = getPanelEl(panel.id);
  if (!el) return;
  const rankInfo = rankPanels().find(r => r.id === panel.id);
  const rankBadge = el.querySelector('.rank-badge');
  if (rankBadge && rankInfo) rankBadge.textContent = rankInfo.score.toFixed(1);
  const lockBtn = el.querySelector('.lock-btn');
  if (lockBtn) {
    lockBtn.className = 'lock-btn' + (panel.locked ? ' locked' : '');
    lockBtn.textContent = panel.locked ? '🔒' : '🔓';
  }
  const compactBtn = el.querySelector('[data-action="compact"]');
  if (compactBtn) compactBtn.textContent = panel.compact ? '⛶' : '⊟';
  const body = el.querySelector('.panel-body');
  if (body) {
    const track = tracking[panel.id];
    const usagePercent = track ? Math.min(100, Math.round((track.totalDuration / 3600000) * 100)) : 0;
    const valueEl = body.querySelector('.metric-value');
    if (valueEl && panel.data.value) valueEl.textContent = panel.data.value;
    const changeEl = body.querySelector('.metric-change');
    if (changeEl && panel.data.change) {
      changeEl.textContent = panel.data.change;
      changeEl.className = 'metric-change ' + (panel.data.dir || '');
    }
    const fillEl = body.querySelector('.usage-bar .fill');
    if (fillEl) fillEl.style.width = usagePercent + '%';
    const heatEl = body.querySelector('.activity-heat');
    if (heatEl) heatEl.innerHTML = buildHeatCells(panel.id);
    const sparkEl = body.querySelector('.sparkline');
    if (sparkEl && panel.type === 'chart') sparkEl.innerHTML = buildSparkline(panel.id);
  }
}
function updatePanelClasses(panel) {
  const el = getPanelEl(panel.id);
  if (!el) return;
  if (panel.dominant) el.classList.add('dominant');
  else el.classList.remove('dominant');
  if (panel.compact) el.classList.add('compact');
  else el.classList.remove('compact');
  if (panel.locked) el.classList.add('locked');
  else el.classList.remove('locked');
}
function renderPanel(panel) {
  const existing = getPanelEl(panel.id);
  if (existing) {
    updatePanelDOM(panel);
    updatePanelClasses(panel);
    return;
  }
  const div = document.createElement('div');
  div.className = 'panel';
  div.dataset.id = panel.id;
  div.innerHTML = buildPanelDOM(panel);
  updatePanelClasses(panel);
  insertPanelIntoGrid(div, panel);
  renderedPanels.add(panel.id);
}
function insertPanelIntoGrid(el, panel) {
  const grid = document.getElementById('grid');
  if (!grid) return;
  if (panel.compact && !panel.dominant) {
    let cz = grid.querySelector('.compact-zone');
    if (!cz) {
      cz = document.createElement('div');
      cz.className = 'compact-zone';
      grid.appendChild(cz);
    }
    cz.appendChild(el);
  } else {
    const compactZone = grid.querySelector('.compact-zone');
    if (compactZone) {
      grid.insertBefore(el, compactZone);
    } else {
      grid.appendChild(el);
    }
  }
}
function renderAllPanels() {
  const sorted = [...panels].sort((a, b) => {
    if (a.locked && !b.locked) return -1;
    if (!a.locked && b.locked) return 1;
    return (a.order || 0) - (b.order || 0);
  });
  const grid = document.getElementById('grid');
  if (!grid) return;
  const existingIds = new Set();
  grid.querySelectorAll('.panel').forEach(el => existingIds.add(el.dataset.id));
  const panelIds = new Set(sorted.map(p => p.id));
  grid.querySelectorAll('.panel').forEach(el => {
    if (!panelIds.has(el.dataset.id)) el.remove();
  });
  const cz = grid.querySelector('.compact-zone');
  sorted.forEach(panel => {
    const el = getPanelEl(panel.id);
    if (!el) {
      renderPanel(panel);
      return;
    }
    updatePanelDOM(panel);
    updatePanelClasses(panel);
    if (panel.compact && !panel.dominant) {
      if (!cz) {
        const newCz = document.createElement('div');
        newCz.className = 'compact-zone';
        grid.appendChild(newCz);
        if (el.parentNode !== newCz) newCz.appendChild(el);
      } else if (el.parentNode !== cz) {
        cz.appendChild(el);
      }
    } else {
      if (el.parentNode && el.parentNode.classList.contains('compact-zone')) {
        if (cz && cz.children.length === 0) cz.remove();
        grid.insertBefore(el, grid.querySelector('.compact-zone') || null);
      }
    }
  });
  if (cz && cz.children.length === 0) cz.remove();
}
function scheduleRender() {
  if (pendingRender) return;
  pendingRender = requestAnimationFrame(() => {
    pendingRender = null;
    assignLayout();
    renderAllPanels();
    updateStats();
    saveState();
  });
}
function debouncedResize() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    scheduleRender();
  }, DEBOUNCE_MS);
}
function trackEvent(panelId, type, duration) {
  ensureTracking(panelId);
  const t = tracking[panelId];
  t.lastViewed = Date.now();
  switch (type) {
    case 'view': t.views++; t.totalDuration += duration || 0; break;
    case 'interact': t.interactions++; break;
    case 'collapse': t.collapses++; break;
    case 'expand': t.expands++; break;
  }
  const now = Date.now();
  t.viewHistory = (t.viewHistory || []).filter(v => now - v.ts < 30*86400000);
  t.viewHistory.push({ ts: now, type, duration: duration || 0 });
  if (t.viewHistory.length > 200) t.viewHistory = t.viewHistory.slice(-200);
  layoutCache.delete('rankings');
  scheduleRender();
}
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2000);
}
function updateStats() {
  const elCount = document.getElementById('stat-count');
  const elTracked = document.getElementById('stat-tracked');
  const elSession = document.getElementById('stat-session');
  if (elCount) elCount.textContent = panels.length;
  let totalSec = 0;
  Object.values(tracking).forEach(t => totalSec += (t.totalDuration || 0) / 1000);
  if (elTracked) elTracked.textContent = Math.round(totalSec) + 's';
  if (elSession) elSession.textContent = Math.round((Date.now() - sessionStart) / 60000) + 'm';
}
function handleLock(panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  panel.locked = !panel.locked;
  if (!panel.locked) { panel.dominant = false; panel.compact = false; }
  trackEvent(panelId, panel.locked ? 'collapse' : 'expand');
  showToast(panel.locked ? panel.title + ' locked' : panel.title + ' unlocked');
  layoutCache.clear();
  scheduleRender();
}
function handleCompact(panelId) {
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  if (panel.locked) { showToast('Unlock panel first'); return; }
  panel.compact = !panel.compact;
  if (panel.compact) panel.dominant = false;
  trackEvent(panelId, panel.compact ? 'collapse' : 'expand');
  showToast(panel.compact ? panel.title + ' → compact' : panel.title + ' → expanded');
  scheduleRender();
}
function handleDragStart(e) {
  const panelId = e.target.closest('.panel-header')?.dataset?.panel;
  if (!panelId) return;
  e.dataTransfer.setData('text/plain', panelId);
  e.dataTransfer.effectAllowed = 'move';
  const el = getPanelEl(panelId);
  if (el) {
    requestAnimationFrame(() => el.classList.add('drag-ghost'));
  }
}
function handleDragEnd(e) {
  const panelId = e.dataTransfer.getData('text/plain');
  if (!panelId) return;
  const el = getPanelEl(panelId);
  if (el) el.classList.remove('drag-ghost');
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const target = e.target.closest('.panel');
  if (target) target.classList.add('drag-over');
}
function handleDragLeave(e) {
  const target = e.target.closest('.panel');
  if (target) target.classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  const draggedId = e.dataTransfer.getData('text/plain');
  const targetEl = e.target.closest('.panel');
  if (!draggedId || !targetEl) return;
  const targetId = targetEl.dataset.id;
  if (draggedId === targetId) return;
  const dragged = panels.find(p => p.id === draggedId);
  const target = panels.find(p => p.id === targetId);
  if (!dragged || !target) return;
  if (dragged.locked && target.locked) {
    [dragged.order, target.order] = [target.order, dragged.order];
  } else if (!dragged.locked) {
    dragged.order = target.order;
  } else {
    showToast('Cannot reorder locked panel over unlocked');
    return;
  }
  dragged.locked = true;
  trackEvent(draggedId, 'interact');
  trackEvent(targetId, 'interact');
  layoutCache.clear();
  showToast(dragged.title + ' moved near ' + target.title);
  scheduleRender();
}
function setupPanelObservers() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.id;
      if (!panelId) return;
      if (entry.isIntersecting) {
        entry.target._visibleSince = Date.now();
        trackEvent(panelId, 'view', 0);
      } else if (entry.target._visibleSince) {
        const duration = Date.now() - entry.target._visibleSince;
        trackEvent(panelId, 'view', duration);
        delete entry.target._visibleSince;
      }
    });
  }, { threshold: 0.3 });
  return observer;
}
let panelObserver = null;
function observePanels() {
  if (panelObserver) panelObserver.disconnect();
  panelObserver = setupPanelObservers();
  document.querySelectorAll('.panel').forEach(el => panelObserver.observe(el));
}
function handleClick(e) {
  const btn = e.target.closest('button[data-action]');
  if (!btn) {
    const panelEl = e.target.closest('.panel');
    if (panelEl && !e.target.closest('button')) {
      trackEvent(panelEl.dataset.id, 'interact');
    }
    return;
  }
  e.preventDefault();
  e.stopPropagation();
  const panelId = btn.dataset.panel;
  if (!panelId) return;
  const action = btn.dataset.action;
  if (action === 'lock') handleLock(panelId);
  else if (action === 'compact') handleCompact(panelId);
}
function handleReset() {
  panels = PANEL_TEMPLATES.map((t, i) => ({
    ...t, locked: false, order: i, dominant: false, compact: false
  }));
  tracking = {};
  layoutCache.clear();
  renderedPanels.clear();
  const grid = document.getElementById('grid');
  if (grid) grid.innerHTML = '';
  scheduleRender();
  showToast('Layout reset');
}
function handleClear() {
  tracking = {};
  panels.forEach(p => { if (!p.locked) { p.dominant = false; p.compact = false; } });
  layoutCache.clear();
  scheduleRender();
  showToast('Tracking data cleared');
}
function init() {
  loadState();
  initDefaultPanels();
  assignLayout();
  renderAllPanels();
  updateStats();
  observePanels();
  document.getElementById('grid').addEventListener('click', handleClick);
  document.getElementById('grid').addEventListener('dragstart', handleDragStart);
  document.getElementById('grid').addEventListener('dragend', handleDragEnd);
  document.getElementById('grid').addEventListener('dragover', handleDragOver);
  document.getElementById('grid').addEventListener('dragleave', handleDragLeave);
  document.getElementById('grid').addEventListener('drop', handleDrop);
  const btnReset = document.getElementById('btn-reset');
  const btnClear = document.getElementById('btn-clear');
  if (btnReset) btnReset.addEventListener('click', handleReset);
  if (btnClear) btnClear.addEventListener('click', handleClear);
  window.addEventListener('resize', debouncedResize);
  window.addEventListener('beforeunload', () => {
    document.querySelectorAll('.panel').forEach(el => {
      if (el._visibleSince) {
        trackEvent(el.dataset.id, 'view', Date.now() - el._visibleSince);
      }
    });
    saveState();
  });
  setInterval(updateStats, 5000);
  setInterval(() => {
    layoutCache.clear();
    scheduleRender();
  }, 60000);
  layoutCache.set('rankings', rankPanels());
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