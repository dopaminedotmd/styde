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
  --border: #2a2d3a;
  --text: #e1e4e8;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent-glow: rgba(88,166,255,0.15);
  --warn: #d29922;
  --good: #3fb950;
  --bad: #f85149;
  --compact-scale: 0.45;
  --transition: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing:border-box; margin:0; padding:0 }
body {
  background:var(--bg); color:var(--text);
  font-family:system-ui,-apple-system,sans-serif;
  overflow-x:hidden; min-height:100vh;
}
.toolbar {
  display:flex; gap:12px; padding:12px 16px;
  background:#16181d; border-bottom:1px solid var(--border);
  align-items:center; position:sticky; top:0; z-index:100;
}
.toolbar h1 { font-size:15px; font-weight:600; margin-right:auto }
.toolbar button {
  background:var(--panel-bg); border:1px solid var(--border);
  color:var(--text); padding:6px 14px; border-radius:6px;
  cursor:pointer; font-size:12px; transition:background 150ms;
}
.toolbar button:hover { background:#252830 }
.toolbar button.active { background:var(--accent); border-color:var(--accent); color:#000 }
.grid {
  display:grid; gap:10px; padding:12px;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  grid-auto-rows:minmax(180px,auto);
  transition:all var(--transition);
}
.grid.compact-view { grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); grid-auto-rows:minmax(100px,auto) }
.panel {
  background:var(--panel-bg); border:1px solid var(--border);
  border-radius:10px; padding:14px; position:relative;
  transition:all var(--transition); overflow:hidden;
  display:flex; flex-direction:column;
  will-change:transform,grid-column,grid-row,width,height,opacity;
}
.panel:hover { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent-glow) }
.panel.rank-high { border-left:3px solid var(--accent) }
.panel.rank-mid { border-left:3px solid var(--warn) }
.panel.rank-low { border-left:3px solid transparent }
.panel.compact {
  transform:scale(var(--compact-scale));
  transform-origin:top left;
  opacity:0.65; padding:8px;
}
.panel.compact:hover { opacity:0.9 }
.panel.compact .panel-body { font-size:10px }
.panel.compact .panel-value { font-size:18px }
.panel.compact .panel-chart { height:50px }
.panel.compact .panel-actions { display:none }
.panel.pinned { border-color:var(--accent); box-shadow:0 0 0 2px var(--accent-glow) }
.panel.pinned::after {
  content:'📌'; position:absolute; top:6px; right:8px; font-size:12px;
}
.panel-header {
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:8px; font-size:12px; font-weight:600;
  color:var(--text-dim); text-transform:uppercase; letter-spacing:0.5px;
}
.panel-body { flex:1; display:flex; flex-direction:column; justify-content:center }
.panel-value { font-size:32px; font-weight:700; color:var(--text); line-height:1.1 }
.panel-sub { font-size:12px; color:var(--text-dim); margin-top:4px }
.panel-chart {
  height:80px; margin-top:8px; border-radius:6px;
  background:linear-gradient(135deg,var(--panel-bg),#1f2330);
  display:flex; align-items:flex-end; gap:2px; padding:4px;
}
.panel-chart .bar {
  flex:1; border-radius:2px 2px 0 0;
  background:var(--accent); opacity:0.6;
  transition:height 300ms ease;
  min-height:2px;
}
.panel-chart .bar.high { opacity:1; background:var(--good) }
.panel-chart .bar.low { background:var(--bad); opacity:0.7 }
.panel-actions {
  display:flex; gap:6px; margin-top:8px; justify-content:flex-end;
}
.panel-actions button {
  background:transparent; border:1px solid var(--border);
  color:var(--text-dim); font-size:10px; padding:3px 8px;
  border-radius:4px; cursor:pointer; transition:all 150ms;
}
.panel-actions button:hover { border-color:var(--accent); color:var(--accent) }
.panel-actions button.locked { background:var(--accent); border-color:var(--accent); color:#000 }
.rank-badge {
  position:absolute; top:8px; right:8px; font-size:9px;
  padding:2px 6px; border-radius:8px; background:#252830;
  color:var(--text-dim);
}
.more-section {
  grid-column:1/-1; border-top:1px solid var(--border);
  padding:8px 0; margin-top:8px;
}
.more-section summary {
  color:var(--text-dim); font-size:12px; cursor:pointer;
  padding:8px 0; user-select:none;
}
.more-drawer {
  display:grid; gap:8px;
  grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
}
.usage-indicator {
  position:absolute; bottom:6px; left:8px; right:8px;
  height:3px; border-radius:2px; background:var(--border); overflow:hidden;
}
.usage-indicator .fill {
  height:100%; background:var(--accent); border-radius:2px;
  transition:width 600ms ease;
}
.drag-ghost { opacity:0.6; border:2px dashed var(--accent) }
[data-drag-over] { border-color:var(--accent); background:var(--accent-glow) }
.toast {
  position:fixed; bottom:20px; right:20px; z-index:999;
  background:var(--panel-bg); border:1px solid var(--border);
  padding:10px 16px; border-radius:8px; font-size:12px;
  animation:toastIn 300ms ease, toastOut 300ms ease 2s forwards;
  pointer-events:none;
}
@keyframes toastIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
@keyframes toastOut { from{opacity:1} to{opacity:0;transform:translateY(-10px)} }
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <button id="btnReset" title="Reset layout">Reset</button>
  <button id="btnCompact" title="Toggle compact mode">Compact</button>
  <button id="btnExport" title="Export layout">Export</button>
  <span style="font-size:11px;color:var(--text-dim);margin-left:8px" id="statusText"></span>
</div>
<div class="grid" id="grid"></div>
<script>
(function(){
'use strict';
const LS_KEY = 'adaptive_dashboard_v2';
const DEBOUNCE_MS = 300;
const ATTENTION_WINDOW_DAYS = 7;
const COMPACT_RANK_PERCENTILE = 0.3;
const MORE_RANK_PERCENTILE = 0.15;
let panels = [];
let panelMap = new Map();
let rankOrder = [];
let dirtyFlags = new Set();
let rafScheduled = false;
let dragState = null;
let viewTimers = new Map();
let observer = null;
let resizeObserver = null;
let toastTimer = null;
const defaultPanels = [
  { id:'cpu', title:'CPU Usage', value:'23%', sub:'+2% from avg', type:'gauge', data:[45,38,52,30,23,18,25,30,22,23] },
  { id:'mem', title:'Memory', value:'7.2 GB', sub:'62% of 11.6 GB', type:'gauge', data:[60,58,62,65,61,63,62,64,61,62] },
  { id:'disk', title:'Disk I/O', value:'142 MB/s', sub:'Read: 98 | Write: 44', type:'spark', data:[80,120,95,140,110,160,130,142,115,142] },
  { id:'net', title:'Network', value:'3.8 Gbps', sub:'↑ 2.1 ↓ 1.7', type:'spark', data:[2.1,3.2,2.8,3.5,4.0,3.6,3.9,4.1,3.7,3.8] },
  { id:'req', title:'Requests/s', value:'12.4k', sub:'p95: 42ms', type:'spark', data:[8,12,10,14,11,13,15,12,11,12.4] },
  { id:'err', title:'Error Rate', value:'0.12%', sub:'24 errors last hour', type:'spark', data:[0.3,0.1,0.05,0.2,0.08,0.15,0.1,0.12,0.09,0.12] },
  { id:'lat', title:'Latency', value:'18ms', sub:'p50: 12 | p99: 210', type:'spark', data:[22,18,15,20,16,19,17,21,18,18] },
  { id:'cache', title:'Cache Hit Rate', value:'94.2%', sub:'miss: 5.8%', type:'gauge', data:[92,94,93,95,96,94,93,95,94,94.2] },
  { id:'queue', title:'Queue Depth', value:'3', sub:'max: 15 | avg: 4.2', type:'gauge', data:[5,2,8,3,1,4,6,2,3,3] },
  { id:'conn', title:'Connections', value:'842', sub:'active: 612 idle: 230', type:'gauge', data:[700,780,800,820,850,830,860,840,845,842] },
  { id:'temp', title:'CPU Temp', value:'58°C', sub:'threshold: 85°C', type:'gauge', data:[55,60,57,59,56,58,61,57,59,58] },
  { id:'gc', title:'GC Pause', value:'4.2ms', sub:'p99: 18ms | freq: 12/min', type:'spark', data:[8,3,5,12,2,6,4,7,3,4.2] },
];
function loadState() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) {
      const s = JSON.parse(raw);
      if (s.panels && Array.isArray(s.panels)) return s;
    }
  } catch(e) {}
  return { panels: defaultPanels.map(p => ({
    ...p,
    rank: 0,
    pinned: false,
    compact: false,
    attentionScore: 0,
    viewCount: 0,
    totalViewMs: 0,
    lastViewed: null,
    interactions: 0,
    collapsed: false,
    order: null,
    locked: false
  })) };
}
function saveState() {
  const data = {
    panels: panels.map(p => ({
      id: p.id, title: p.title, value: p.value, sub: p.sub, type: p.type, data: p.data,
      rank: p.rank, pinned: p.pinned, compact: p.compact,
      attentionScore: p.attentionScore, viewCount: p.viewCount,
      totalViewMs: p.totalViewMs, lastViewed: p.lastViewed,
      interactions: p.interactions, collapsed: p.collapsed,
      order: p.order, locked: p.locked
    })),
    updated: Date.now()
  };
  localStorage.setItem(LS_KEY, JSON.stringify(data));
}
function computeAttentionScore(p) {
  const now = Date.now();
  const recencyDays = p.lastViewed ? Math.max(0, (now - p.lastViewed) / 86400000) : ATTENTION_WINDOW_DAYS;
  const recencyFactor = Math.exp(-recencyDays / ATTENTION_WINDOW_DAYS);
  const durationFactor = Math.log1p(p.totalViewMs / 1000);
  const freqFactor = Math.log1p(p.viewCount);
  const interactionBonus = Math.log1p(p.interactions);
  return (freqFactor * durationFactor * recencyFactor * (1 + interactionBonus * 0.3));
}
function recomputeRanks() {
  panels.forEach(p => { p.attentionScore = computeAttentionScore(p); });
  const sorted = [...panels].sort((a,b) => b.attentionScore - a.attentionScore);
  sorted.forEach((p,i) => { p.rank = i; });
  rankOrder = sorted.map(p => p.id);
  const threshold = Math.max(1, Math.floor(panels.length * COMPACT_RANK_PERCENTILE));
  const moreThreshold = Math.max(1, Math.floor(panels.length * MORE_RANK_PERCENTILE));
  panels.forEach(p => {
    if (p.locked || p.pinned) return;
    p.compact = p.rank >= threshold;
    p.collapsed = p.rank >= panels.length - moreThreshold;
  });
}
function getDropTargetIndex(x, y) {
  const els = document.elementsFromPoint(x, y);
  for (const el of els) {
    const pid = el.closest?.('.panel')?.dataset?.panelId;
    if (pid && panelMap.has(pid)) return pid;
  }
  return null;
}
function buildDropTargetMap() {
  const map = new Map();
  const grid = document.getElementById('grid');
  if (!grid) return map;
  const panels = grid.querySelectorAll('.panel');
  panels.forEach(el => {
    const rect = el.getBoundingClientRect();
    map.set(el.dataset.panelId, rect);
  });
  return map;
}
function findDropTarget(x, y, targetMap) {
  for (const [id, rect] of targetMap) {
    if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) return id;
  }
  return null;
}
function scheduleRender(panelId) {
  dirtyFlags.add(panelId || '__all__');
  if (!rafScheduled) {
    rafScheduled = true;
    requestAnimationFrame(doRender);
  }
}
function doRender() {
  rafScheduled = false;
  const allDirty = dirtyFlags.has('__all__');
  const grid = document.getElementById('grid');
  if (!grid) return;
  if (allDirty) {
    renderAllPanels(grid);
  } else {
    dirtyFlags.forEach(pid => {
      if (pid === '__all__') return;
      const el = grid.querySelector(`[data-panel-id="${pid}"]`);
      if (el) patchPanel(el, panelMap.get(pid));
    });
  }
  dirtyFlags.clear();
}
function patchPanel(el, p) {
  if (!p) return;
  el.querySelector('.panel-value').textContent = p.value;
  el.querySelector('.panel-sub').textContent = p.sub;
  el.className = buildPanelClass(p);
  const pinMark = el.querySelector('.pin-mark');
  if (p.pinned && !pinMark) {
    const mark = document.createElement('span');
    mark.className = 'pin-mark';
    mark.textContent = '📌';
    mark.style.cssText = 'position:absolute;top:6px;right:8px;font-size:12px;';
    el.appendChild(mark);
  } else if (!p.pinned && pinMark) {
    pinMark.remove();
  }
  const usageFill = el.querySelector('.usage-indicator .fill');
  if (usageFill) {
    const maxScore = panels.length > 0 ? Math.max(...panels.map(pp => pp.attentionScore)) : 1;
    usageFill.style.width = maxScore > 0 ? `${(p.attentionScore / maxScore) * 100}%` : '0%';
  }
  updateChart(el, p);
}
function renderAllPanels(grid) {
  const existingMap = new Map();
  grid.querySelectorAll('.panel').forEach(el => existingMap.set(el.dataset.panelId, el));
  const fragment = document.createDocumentFragment();
  const sortedPanels = [...panels].sort((a,b) => {
    if (a.pinned && !b.pinned) return -1;
    if (!a.pinned && b.pinned) return 1;
    if (a.locked && !b.locked) return -1;
    if (!a.locked && b.locked) return 1;
    return a.rank - b.rank;
  });
  const visiblePanels = sortedPanels.filter(p => !p.collapsed);
  const morePanels = sortedPanels.filter(p => p.collapsed);
  visiblePanels.forEach(p => {
    let el = existingMap.get(p.id);
    if (!el) {
      el = createPanelElement(p);
    } else {
      existingMap.delete(p.id);
      patchPanel(el, p);
    }
    el.style.order = p.rank;
    el.style.gridColumn = p.pinned ? 'span 2' : '';
    el.style.gridRow = p.pinned ? 'span 2' : '';
    fragment.appendChild(el);
  });
  if (morePanels.length > 0) {
    const moreSection = document.createElement('details');
    moreSection.className = 'more-section';
    moreSection.innerHTML = `<summary>More (${morePanels.length} panels)</summary><div class="more-drawer" id="moreDrawer"></div>`;
    const drawer = moreSection.querySelector('.more-drawer');
    morePanels.forEach(p => {
      let el = existingMap.get(p.id);
      if (!el) {
        el = createPanelElement(p);
      } else {
        existingMap.delete(p.id);
        patchPanel(el, p);
      }
      drawer.appendChild(el);
    });
    fragment.appendChild(moreSection);
    moreSection.addEventListener('toggle', () => {
      if (moreSection.open) {
        morePanels.forEach(p => { p.collapsed = false; p.compact = true; });
        scheduleRender('__all__');
      }
    });
  }
  existingMap.forEach(el => el.remove());
  grid.innerHTML = '';
  grid.appendChild(fragment);
  attachPanelEvents();
}
function createPanelElement(p) {
  const el = document.createElement('div');
  el.className = buildPanelClass(p);
  el.dataset.panelId = p.id;
  el.draggable = true;
  el.innerHTML = `
    <div class="panel-header">
      <span>${escapeHtml(p.title)}</span>
      <span class="rank-badge">#${p.rank + 1}</span>
    </div>
    <div class="panel-body">
      <div class="panel-value">${escapeHtml(String(p.value))}</div>
      <div class="panel-sub">${escapeHtml(p.sub)}</div>
      <div class="panel-chart">${buildChartBars(p)}</div>
    </div>
    <div class="usage-indicator"><div class="fill" style="width:${usagePercent(p)}%"></div></div>
    <div class="panel-actions">
      <button class="pin-btn ${p.pinned?'locked':''}" data-action="pin">${p.pinned?'📌':'📌'}</button>
      <button class="lock-btn ${p.locked?'locked':''}" data-action="lock">${p.locked?'🔒':'🔓'}</button>
    </div>
  `;
  return el;
}
function buildPanelClass(p) {
  const classes = ['panel'];
  if (p.rank < 3) classes.push('rank-high');
  else if (p.rank < 6) classes.push('rank-mid');
  else classes.push('rank-low');
  if (p.compact) classes.push('compact');
  if (p.pinned) classes.push('pinned');
  return classes.join(' ');
}
function buildChartBars(p) {
  if (!p.data || !Array.isArray(p.data)) return '';
  const max = Math.max(...p.data, 0.001);
  return p.data.map(v => {
    const h = (v / max) * 100;
    const cls = v > max * 0.8 ? 'bar high' : v < max * 0.2 ? 'bar low' : 'bar';
    return `<div class="${cls}" style="height:${h}%"></div>`;
  }).join('');
}
function updateChart(el, p) {
  const chart = el.querySelector('.panel-chart');
  if (!chart || !p.data) return;
  chart.innerHTML = buildChartBars(p);
}
function usagePercent(p) {
  const max = panels.reduce((m, pp) => Math.max(m, pp.attentionScore), 0.001);
  return (p.attentionScore / max) * 100;
}
function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
function attachPanelEvents() {
  const grid = document.getElementById('grid');
  if (!grid) return;
  grid.querySelectorAll('.panel').forEach(el => {
    const pid = el.dataset.panelId;
    el.addEventListener('dragstart', onDragStart);
    el.addEventListener('dragend', onDragEnd);
    el.addEventListener('mouseenter', () => startViewTimer(pid));
    el.addEventListener('mouseleave', () => stopViewTimer(pid));
    const pinBtn = el.querySelector('.pin-btn');
    const lockBtn = el.querySelector('.lock-btn');
    if (pinBtn) {
      pinBtn.addEventListener('click', throttleCb((e) => {
        e.stopPropagation();
        togglePin(pid);
      }, DEBOUNCE_MS));
    }
    if (lockBtn) {
      lockBtn.addEventListener('click', throttleCb((e) => {
        e.stopPropagation();
        toggleLock(pid);
      }, DEBOUNCE_MS));
    }
    el.addEventListener('click', throttleCb(() => {
      recordClick(pid);
    }, DEBOUNCE_MS));
  });
}
function throttleCb(fn, ms) {
  let last = 0;
  return function(...args) {
    const now = Date.now();
    if (now - last < ms) return;
    last = now;
    fn.apply(this, args);
  };
}
let dropTargetMap = null;
function onDragStart(e) {
  const pid = e.target.closest('.panel')?.dataset?.panelId;
  if (!pid) return;
  dropTargetMap = buildDropTargetMap();
  dragState = { id:pid, fromIdx:panels.findIndex(p=>p.id===pid) };
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', pid);
  setTimeout(() => e.target.classList.add('drag-ghost'), 0);
}
function onDragEnd(e) {
  e.target.classList.remove('drag-ghost');
  if (dragState && dragState.targetId) {
    reorderPanel(dragState.id, dragState.targetId);
  }
  dragState = null;
  dropTargetMap = null;
  document.querySelectorAll('[data-drag-over]').forEach(el => el.removeAttribute('data-drag-over'));
}
document.addEventListener('dragover', throttleCb((e) => {
  e.preventDefault();
  if (!dragState) return;
  const target = findDropTarget(e.clientX, e.clientY, dropTargetMap);
  document.querySelectorAll('[data-drag-over]').forEach(el => el.removeAttribute('data-drag-over'));
  if (target && target !== dragState.id) {
    const el = document.querySelector(`[data-panel-id="${target}"]`);
    if (el) el.setAttribute('data-drag-over', '');
    dragState.targetId = target;
  }
}, 50));
document.addEventListener('drop', (e) => {
  e.preventDefault();
  if (!dragState) return;
  const target = findDropTarget(e.clientX, e.clientY, dropTargetMap);
  if (target) dragState.targetId = target;
});
function reorderPanel(fromId, toId) {
  const fromIdx = panels.findIndex(p => p.id === fromId);
  const toIdx = panels.findIndex(p => p.id === toId);
  if (fromIdx < 0 || toIdx < 0 || fromIdx === toIdx) return;
  const [moved] = panels.splice(fromIdx, 1);
  panels.splice(toIdx, 0, moved);
  moved.locked = true;
  moved.pinned = false;
  moved.order = toIdx;
  recomputeRanks();
  saveState();
  scheduleRender('__all__');
  toast('Panel reordered');
}
function togglePin(pid) {
  const p = panelMap.get(pid);
  if (!p) return;
  p.pinned = !p.pinned;
  if (p.pinned) p.locked = false;
  recomputeRanks();
  saveState();
  scheduleRender(pid);
  toast(p.pinned ? 'Panel pinned' : 'Panel unpinned');
}
function toggleLock(pid) {
  const p = panelMap.get(pid);
  if (!p) return;
  p.locked = !p.locked;
  if (p.locked) p.pinned = false;
  saveState();
  scheduleRender(pid);
  toast(p.locked ? 'Panel locked' : 'Panel unlocked');
}
function recordClick(pid) {
  const p = panelMap.get(pid);
  if (!p) return;
  p.interactions = (p.interactions || 0) + 1;
  p.lastViewed = Date.now();
  recomputeRanks();
  saveState();
  scheduleRender('__all__');
}
function startViewTimer(pid) {
  if (viewTimers.has(pid)) return;
  viewTimers.set(pid, Date.now());
}
function stopViewTimer(pid) {
  const start = viewTimers.get(pid);
  if (!start) return;
  const elapsed = Date.now() - start;
  viewTimers.delete(pid);
  const p = panelMap.get(pid);
  if (!p) return;
  p.totalViewMs = (p.totalViewMs || 0) + elapsed;
  p.viewCount = (p.viewCount || 0) + 1;
  p.lastViewed = Date.now();
  recomputeRanks();
  saveState();
  scheduleRender('__all__');
}
function toast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.remove(), 2500);
}
let refreshInterval = null;
let refreshCount = 0;
const REFRESH_INTERVAL_MS = 30000;
const STALE_THRESHOLD_MS = 25000;
function startAutoRefresh() {
  if (refreshInterval) return;
  refreshInterval = setInterval(() => {
    const now = Date.now();
    panels.forEach(p => {
      if (now - (p.lastViewed || 0) < STALE_THRESHOLD_MS) return;
      if (p.pinned) return;
    });
    panels.forEach(p => {
      const jitter = (Math.random() - 0.5) * 0.1;
      if (p.type === 'gauge') {
        const v = parseFloat(p.value);
        if (!isNaN(v)) {
          const newV = Math.max(0, v * (1 + jitter));
          p.value = p.value.includes('%') ? `${newV.toFixed(1)}%` :
                    p.value.includes('GB') ? `${newV.toFixed(1)} GB` :
                    p.value.includes('°C') ? `${Math.round(newV)}°C` :
                    `${Math.round(newV)}`;
        }
      }
      if (p.data && Array.isArray(p.data)) {
        p.data.push(p.data.shift());
      }
    });
    recomputeRanks();
    saveState();
    scheduleRender('__all__');
    refreshCount++;
    const status = document.getElementById('statusText');
    if (status) status.textContent = `Auto-refresh #${refreshCount}`;
  }, REFRESH_INTERVAL_MS);
}
function init() {
  const state = loadState();
  panels = state.panels;
  panels.forEach(p => panelMap.set(p.id, p));
  recomputeRanks();
  scheduleRender('__all__');
  document.getElementById('btnReset').addEventListener('click', throttleCb(() => {
    localStorage.removeItem(LS_KEY);
    const fresh = loadState();
    panels.length = 0;
    panels.push(...fresh.panels);
    panelMap.clear();
    panels.forEach(p => panelMap.set(p.id, p));
    recomputeRanks();
    scheduleRender('__all__');
    toast('Layout reset');
  }, DEBOUNCE_MS));
  document.getElementById('btnCompact').addEventListener('click', throttleCb(() => {
    const grid = document.getElementById('grid');
    grid.classList.toggle('compact-view');
    toast(grid.classList.contains('compact-view') ? 'Compact mode on' : 'Compact mode off');
  }, DEBOUNCE_MS));
  document.getElementById('btnExport').addEventListener('click', throttleCb(() => {
    const data = JSON.stringify({
      panels: panels.map(p => ({
        id:p.id, rank:p.rank, pinned:p.pinned, locked:p.locked,
        attentionScore:p.attentionScore, viewCount:p.viewCount,
        totalViewMs:p.totalViewMs, compact:p.compact
      })),
      exported: Date.now()
    }, null, 2);
    const blob = new Blob([data], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `dashboard-layout-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast('Layout exported');
  }, DEBOUNCE_MS));
  startAutoRefresh();
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