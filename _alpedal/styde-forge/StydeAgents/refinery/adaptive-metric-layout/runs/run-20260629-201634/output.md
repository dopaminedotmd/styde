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
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --danger: #ff5c7a;
  --success: #3dd68c;
  --warning: #ffb224;
  --radius: 12px;
  --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
.app { padding: 16px; max-width: 1400px; margin: 0 auto; }
.header {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; margin-bottom: 20px;
  background: var(--surface); border-radius: var(--radius);
  border: 1px solid var(--border);
}
.header h1 { font-size: 1.1rem; font-weight: 600; letter-spacing: -0.01em; flex:1; }
.stats { display:flex; gap:16px; font-size:0.8rem; color:var(--text-dim); }
.stat { display:flex; align-items:center; gap:6px; }
.stat-val { color:var(--accent); font-weight:600; font-variant-numeric:tabular-nums; }
.btn {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  padding: 6px 14px; border-radius: 8px;
  cursor: pointer; font-size: 0.8rem;
  transition: all var(--transition);
  font-family: inherit;
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.btn-accent { background: var(--accent); color:#fff; border-color:var(--accent); }
.btn-accent:hover { filter: brightness(1.1); }
.btn-sm { padding: 4px 10px; font-size:0.72rem; }
.btn-xs { padding: 2px 8px; font-size:0.68rem; border-radius:6px; }
.dashboard {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  transition: all var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: all var(--transition);
  position: relative;
  display: flex; flex-direction: column;
  min-height: 0;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 16px var(--accent-glow); }
.panel:focus-within { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.high { grid-column: span 2; grid-row: span 2; order: -100; }
.panel.medium { grid-column: span 1; grid-row: span 1; order: 0; }
.panel.compact { grid-column: span 1; grid-row: span 1; order: 100; }
.panel.compact .panel-body { max-height: 80px; overflow: hidden; }
.panel.compact .panel-body > * { opacity: 0.6; transform:scale(0.95); }
.panel.locked { border-color: var(--warning); box-shadow: 0 0 8px rgba(255,178,36,0.3); }
.panel-header {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  cursor: grab;
  user-select: none;
}
.panel-header:active { cursor: grabbing; }
.panel-header:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.panel-icon { font-size:1rem; width:24px; text-align:center; flex-shrink:0; }
.panel-title { font-size:0.85rem; font-weight:600; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.panel-rank {
  font-size:0.65rem; color:var(--text-dim);
  background:rgba(255,255,255,0.04); padding:2px 6px; border-radius:4px;
}
.panel-actions { display:flex; gap:4px; }
.panel-lock, .panel-collapse { background:none; border:none; color:var(--text-dim); cursor:pointer; padding:2px 4px; border-radius:4px; font-size:0.75rem; transition: color var(--transition); }
.panel-lock:hover, .panel-collapse:hover { color:var(--text); }
.panel-lock.locked { color:var(--warning); }
.panel-body { padding: 12px; flex:1; overflow:hidden; transition: all var(--transition); }
.panel-body canvas { width:100%; height:100%; min-height:120px; }
.metric-row { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px; }
.metric-label { font-size:0.72rem; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.04em; }
.metric-value { font-size:1.6rem; font-weight:700; font-variant-numeric:tabular-nums; }
.metric-sub { font-size:0.7rem; color:var(--text-dim); }
.metric-up { color:var(--success); }
.metric-down { color:var(--danger); }
.spark {
  display:flex; align-items:flex-end; gap:2px; height:40px; margin-top:8px;
}
.spark-bar {
  flex:1; background:var(--accent); border-radius:2px 2px 0 0;
  min-width:2px; transition: height 0.3s ease;
  opacity:0.6;
}
.spark-bar:last-child { opacity:1; }
.compact-preview { font-size:0.7rem; color:var(--text-dim); text-align:center; padding:4px; }
.compact-preview .mini-val { font-size:1rem; font-weight:600; color:var(--text); }
.drag-ghost { opacity:0.4; background:var(--accent); border:2px dashed var(--accent); border-radius:var(--radius); }
.drag-over { border-color:var(--accent); box-shadow: 0 0 24px var(--accent-glow); }
.toast {
  position:fixed; bottom:20px; right:20px;
  background:var(--surface); border:1px solid var(--border);
  padding:10px 16px; border-radius:8px; font-size:0.8rem;
  box-shadow:var(--shadow); z-index:1000;
  transform:translateY(100px); opacity:0;
  transition:all 0.3s ease;
}
.toast.show { transform:translateY(0); opacity:1; }
.sr-only {
  position:absolute; width:1px; height:1px; padding:0; margin:-1px;
  overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0;
}
</style>
</head>
<body>
<div class="app">
  <header class="header" role="banner" aria-label="Dashboard controls">
    <h1 id="dash-title">Adaptive Metrics</h1>
    <div class="stats" aria-live="polite" aria-atomic="true">
      <div class="stat"><span>Session</span><span class="stat-val" id="session-time">00:00</span></div>
      <div class="stat"><span>Interactions</span><span class="stat-val" id="interaction-count">0</span></div>
      <div class="stat"><span>Adaptations</span><span class="stat-val" id="adaptation-count">0</span></div>
    </div>
    <button class="btn btn-accent" id="btn-reset" aria-label="Reset layout to default">Reset Layout</button>
    <button class="btn" id="btn-export" aria-label="Export layout configuration">Export</button>
  </header>
  <div class="dashboard" id="dashboard" role="list" aria-label="Metric panels">
  </div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive-layout-v2';
const DEBOUNCE_MS = 100;
const THROTTLE_MS = 200;
const RANK_HIGH = 75;
const RANK_MEDIUM = 50;
const ADAPT_INTERVAL = 30000;
const RECENCY_DECAY = 0.95;
const VIEW_THRESHOLD_MS = 2000;
let panels = [];
let layoutOrder = [];
let lockedPanels = new Set();
let interactionLog = [];
let sessionStart = Date.now();
let adaptationCount = 0;
let totalInteractions = 0;
let pageHidden = false;
let pendingAdapt = false;
const defaultPanels = [
  { id:'revenue', icon:'chart-line', title:'Revenue', type:'metric', data:{ value:'$48,293', change:'+12.3%', up:true, spark:[30,45,38,52,48,60,55,70,65,80,75,90] } },
  { id:'users', icon:'users', title:'Active Users', type:'metric', data:{ value:'2,847', change:'+5.7%', up:true, spark:[800,900,1100,1050,1200,1400,1600,1800,2000,2200,2400,2847] } },
  { id:'latency', icon:'clock', title:'Avg Latency', type:'metric', data:{ value:'42ms', change:'-8.1%', up:false, spark:[55,50,48,52,45,42,44,40,38,42,40,42] } },
  { id:'errors', icon:'warning-triangle', title:'Error Rate', type:'metric', data:{ value:'0.12%', change:'-0.04%', up:false, spark:[0.2,0.18,0.15,0.19,0.14,0.16,0.13,0.11,0.12,0.10,0.13,0.12] } },
  { id:'cpu', icon:'cpu', title:'CPU Usage', type:'gauge', data:{ value:62, max:100, unit:'%' } },
  { id:'memory', icon:'memory', title:'Memory', type:'gauge', data:{ value:78, max:100, unit:'%' } },
  { id:'requests', icon:'activity', title:'Requests/min', type:'metric', data:{ value:'12.4k', change:'+18.2%', up:true, spark:[4,5,6,8,7,9,10,11,9,12,11,12.4] } },
  { id:'uptime', icon:'check-circle', title:'Uptime', type:'metric', data:{ value:'99.97%', change:'+0.02%', up:true, spark:[99.9,99.91,99.92,99.93,99.94,99.93,99.95,99.96,99.95,99.97,99.96,99.97] } },
  { id:'bandwidth', icon:'network', title:'Bandwidth', type:'gauge', data:{ value:45, max:100, unit:'Mbps' } },
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const state = JSON.parse(raw);
      layoutOrder = state.layoutOrder || defaultPanels.map(p => p.id);
      lockedPanels = new Set(state.lockedPanels || []);
      interactionLog = state.interactionLog || [];
      adaptationCount = state.adaptationCount || 0;
      totalInteractions = state.totalInteractions || 0;
      return;
    }
  } catch(e) {}
  layoutOrder = defaultPanels.map(p => p.id);
}
function saveState() {
  const state = {
    layoutOrder,
    lockedPanels: [...lockedPanels],
    interactionLog: interactionLog.slice(-200),
    adaptationCount,
    totalInteractions,
    savedAt: Date.now()
  };
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
function getPanelById(id) { return panels.find(p => p.id === id) || defaultPanels.find(p => p.id === id); }
function scorePanels() {
  const now = Date.now();
  const scores = {};
  const ids = panels.map(p => p.id);
  ids.forEach(id => { scores[id] = 0; });
  interactionLog.forEach(entry => {
    const { panelId, type, ts } = entry;
    const age = (now - ts) / 1000;
    const recency = Math.exp(-age / 3600);
    let weight = 1;
    if (type === 'view') weight = entry.duration ? Math.min(entry.duration / 1000, 30) : 1;
    else if (type === 'expand') weight = 5;
    else if (type === 'interact') weight = 3;
    scores[panelId] = (scores[panelId] || 0) + weight * recency;
  });
  return scores;
}
function rankPanels(scores) {
  const entries = Object.entries(scores).sort((a,b) => b[1] - a[1]);
  const ranked = {};
  entries.forEach(([id, score], i) => {
    if (score >= RANK_HIGH) ranked[id] = 'high';
    else if (score >= RANK_MEDIUM) ranked[id] = 'medium';
    else ranked[id] = 'compact';
  });
  return ranked;
}
function debounce(fn, ms) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), ms);
  };
}
function throttle(fn, ms) {
  let last = 0;
  return function(...args) {
    const now = Date.now();
    if (now - last >= ms) { last = now; fn.apply(this, args); }
  };
}
function logInteraction(panelId, type, extra) {
  if (pageHidden) return;
  const entry = { panelId, type, ts: Date.now(), ...extra };
  interactionLog.push(entry);
  totalInteractions++;
  if (interactionLog.length > 500) interactionLog.shift();
}
const debouncedLog = debounce((panelId, type, extra) => {
  logInteraction(panelId, type, extra);
}, DEBOUNCE_MS);
const throttledAdapt = throttle(() => {
  adaptLayout();
}, THROTTLE_MS);
function adaptLayout() {
  if (pageHidden) { pendingAdapt = true; return; }
  const scores = scorePanels();
  const ranks = rankPanels(scores);
  applyRanks(ranks);
  adaptationCount++;
  updateStats();
  saveState();
}
function applyRanks(ranks) {
  const container = document.getElementById('dashboard');
  const children = container.children;
  for (let i = 0; i < children.length; i++) {
    const el = children[i];
    const id = el.dataset.panelId;
    if (!id || lockedPanels.has(id)) continue;
    const rank = ranks[id] || 'medium';
    el.classList.remove('high', 'medium', 'compact');
    el.classList.add(rank);
    const rankEl = el.querySelector('.panel-rank');
    if (rankEl) rankEl.textContent = rank === 'high' ? '★ High' : rank === 'medium' ? '◆ Med' : '● Compact';
  }
}
function renderPanel(panel, rank) {
  const el = document.createElement('div');
  el.className = 'panel ' + (rank || 'medium');
  if (lockedPanels.has(panel.id)) el.classList.add('locked');
  el.dataset.panelId = panel.id;
  el.setAttribute('role', 'listitem');
  el.setAttribute('aria-label', panel.title + ' panel, rank ' + (rank || 'medium'));
  el.setAttribute('tabindex', '0');
  el.setAttribute('draggable', 'true');
  const header = document.createElement('div');
  header.className = 'panel-header';
  header.setAttribute('aria-grabbed', 'false');
  const icon = document.createElement('span');
  icon.className = 'panel-icon';
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = getIcon(panel.icon);
  const title = document.createElement('span');
  title.className = 'panel-title';
  title.textContent = panel.title;
  const rankBadge = document.createElement('span');
  rankBadge.className = 'panel-rank';
  rankBadge.textContent = rank === 'high' ? '★ High' : rank === 'medium' ? '◆ Med' : '● Compact';
  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const lockBtn = document.createElement('button');
  lockBtn.className = 'panel-lock' + (lockedPanels.has(panel.id) ? ' locked' : '');
  lockBtn.setAttribute('aria-label', lockedPanels.has(panel.id) ? 'Unlock ' + panel.title + ' position' : 'Lock ' + panel.title + ' position');
  lockBtn.setAttribute('aria-pressed', lockedPanels.has(panel.id) ? 'true' : 'false');
  lockBtn.textContent = lockedPanels.has(panel.id) ? '🔒' : '🔓';
  lockBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleLock(panel.id);
  });
  const collapseBtn = document.createElement('button');
  collapseBtn.className = 'panel-collapse';
  collapseBtn.setAttribute('aria-label', 'Toggle ' + panel.title + ' compact mode');
  collapseBtn.textContent = '⊟';
  collapseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleCompact(panel.id);
  });
  actions.appendChild(lockBtn);
  actions.appendChild(collapseBtn);
  header.appendChild(icon);
  header.appendChild(title);
  header.appendChild(rankBadge);
  header.appendChild(actions);
  const body = document.createElement('div');
  body.className = 'panel-body';
  body.setAttribute('aria-label', panel.title + ' content');
  body.innerHTML = renderPanelContent(panel);
  el.appendChild(header);
  el.appendChild(body);
  el.addEventListener('click', () => logInteraction(panel.id, 'interact'));
  el.addEventListener('focus', () => logInteraction(panel.id, 'interact'));
  el.addEventListener('dragstart', handleDragStart);
  el.addEventListener('dragend', handleDragEnd);
  el.addEventListener('dragover', handleDragOver);
  el.addEventListener('drop', handleDrop);
  el.addEventListener('keydown', (e) => handleKeyboardReorder(e, panel.id));
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        el.dataset.visibleSince = el.dataset.visibleSince || Date.now().toString();
      } else if (el.dataset.visibleSince) {
        const duration = Date.now() - parseInt(el.dataset.visibleSince);
        if (duration >= VIEW_THRESHOLD_MS) {
          logInteraction(panel.id, 'view', { duration });
        }
        delete el.dataset.visibleSince;
      }
    });
  }, { threshold: 0.6 });
  observer.observe(el);
  return { el, observer };
}
function getIcon(name) {
  const map = {
    'chart-line':'📈','users':'👥','clock':'⏱','warning-triangle':'⚠',
    'cpu':'💻','memory':'🧠','activity':'📊','check-circle':'✅','network':'🌐',
    'dollar':'💰','bar-chart':'📊','server':'🖥','database':'🗄','globe':'🌍'
  };
  return map[name] || '📌';
}
function renderPanelContent(panel) {
  if (panel.type === 'metric') {
    const d = panel.data;
    const bars = d.spark.map((v,i,a) => {
      const max = Math.max(...a);
      const h = max > 0 ? (v/max*100) : 0;
      return '<div class="spark-bar" style="height:'+h+'%" aria-hidden="true"></div>';
    }).join('');
    return '<div class="metric-row"><span class="metric-label">'+panel.title+'</span></div>' +
      '<div class="metric-row"><span class="metric-value">'+d.value+'</span>' +
      '<span class="metric-sub '+(d.up?'metric-up':'metric-down')+'" aria-label="Change: '+d.change+'">'+d.change+'</span></div>' +
      '<div class="spark" aria-label="Sparkline chart showing trend">'+bars+'</div>';
  }
  if (panel.type === 'gauge') {
    const d = panel.data;
    const pct = (d.value/d.max*100).toFixed(0);
    const color = d.value > 80 ? 'var(--danger)' : d.value > 60 ? 'var(--warning)' : 'var(--success)';
    return '<div class="metric-row"><span class="metric-label">'+panel.title+'</span></div>' +
      '<div class="metric-row"><span class="metric-value">'+d.value+d.unit+'</span></div>' +
      '<div style="background:rgba(255,255,255,0.06);border-radius:8px;height:8px;margin-top:12px;overflow:hidden;" role="progressbar" aria-valuenow="'+d.value+'" aria-valuemin="0" aria-valuemax="'+d.max+'" aria-label="'+panel.title+' '+d.value+d.unit+'">' +
      '<div style="width:'+pct+'%;height:100%;background:'+color+';border-radius:8px;transition:width 0.5s ease;"></div></div>';
  }
  return '<div class="compact-preview"><span class="mini-val">'+panel.title+'</span></div>';
}
let draggedEl = null;
let draggedId = null;
function handleDragStart(e) {
  draggedEl = this;
  draggedId = this.dataset.panelId;
  this.classList.add('drag-ghost');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', draggedId);
  this.setAttribute('aria-grabbed', 'true');
  logInteraction(draggedId, 'drag-start');
}
function handleDragEnd(e) {
  this.classList.remove('drag-ghost');
  this.setAttribute('aria-grabbed', 'false');
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  draggedEl = null;
  draggedId = null;
  logInteraction(this.dataset.panelId, 'drag-end');
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  if (this !== draggedEl) this.classList.add('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  this.classList.remove('drag-over');
  const targetId = this.dataset.panelId;
  if (!draggedId || draggedId === targetId) return;
  reorderPanels(draggedId, targetId);
  logInteraction(draggedId, 'drop', { target: targetId });
  toast('Panel moved');
}
function handleKeyboardReorder(e, panelId) {
  if (e.ctrlKey && e.key === 'ArrowUp') { e.preventDefault(); movePanel(panelId, -1); }
  if (e.ctrlKey && e.key === 'ArrowDown') { e.preventDefault(); movePanel(panelId, 1); }
  if (e.key === 'l' && e.ctrlKey) { e.preventDefault(); toggleLock(panelId); }
  if (e.key === 'c' && e.ctrlKey) { e.preventDefault(); toggleCompact(panelId); }
}
function reorderPanels(fromId, toId) {
  const fromIdx = layoutOrder.indexOf(fromId);
  const toIdx = layoutOrder.indexOf(toId);
  if (fromIdx === -1 || toIdx === -1) return;
  layoutOrder.splice(fromIdx, 1);
  layoutOrder.splice(toIdx, 0, fromId);
  rebuildDashboard();
  saveState();
  throttledAdapt();
}
function movePanel(id, dir) {
  const idx = layoutOrder.indexOf(id);
  if (idx === -1) return;
  const newIdx = idx + dir;
  if (newIdx < 0 || newIdx >= layoutOrder.length) return;
  [layoutOrder[idx], layoutOrder[newIdx]] = [layoutOrder[newIdx], layoutOrder[idx]];
  rebuildDashboard();
  saveState();
  throttledAdapt();
  toast('Panel moved ' + (dir < 0 ? 'up' : 'down'));
}
function toggleLock(id) {
  if (lockedPanels.has(id)) {
    lockedPanels.delete(id);
    logInteraction(id, 'unlock');
    toast('Panel unlocked');
  } else {
    lockedPanels.add(id);
    logInteraction(id, 'lock');
    toast('Panel locked');
  }
  patchPanelState(id);
  saveState();
}
function toggleCompact(id) {
  const el = document.querySelector('[data-panel-id="'+id+'"]');
  if (!el) return;
  if (el.classList.contains('compact')) {
    el.classList.remove('compact');
    el.classList.add('medium');
    logInteraction(id, 'expand');
  } else {
    el.classList.add('compact');
    el.classList.remove('high', 'medium');
    logInteraction(id, 'collapse');
  }
  saveState();
}
function patchPanelState(id) {
  const el = document.querySelector('[data-panel-id="'+id+'"]');
  if (!el) return;
  const lockBtn = el.querySelector('.panel-lock');
  if (lockBtn) {
    const locked = lockedPanels.has(id);
    lockBtn.classList.toggle('locked', locked);
    lockBtn.textContent = locked ? '🔒' : '🔓';
    lockBtn.setAttribute('aria-pressed', locked ? 'true' : 'false');
    lockBtn.setAttribute('aria-label', locked ? 'Unlock position' : 'Lock position');
    el.classList.toggle('locked', locked);
  }
}
function rebuildDashboard() {
  const container = document.getElementById('dashboard');
  const existing = {};
  container.querySelectorAll('.panel').forEach(el => {
    existing[el.dataset.panelId] = { el, observer: el._observer };
  });
  container.innerHTML = '';
  const orderedIds = layoutOrder.length ? layoutOrder : panels.map(p => p.id);
  orderedIds.forEach(id => {
    const panel = getPanelById(id);
    if (!panel) return;
    const oldRank = existing[id] ? (existing[id].el.classList.contains('high') ? 'high' : existing[id].el.classList.contains('compact') ? 'compact' : 'medium') : 'medium';
    const { el, observer } = renderPanel(panel, oldRank);
    el._observer = observer;
    container.appendChild(el);
  });
  updateStats();
}
function liveSimulation() {
  const updates = [
    { id:'revenue', data:{ value:'$48,'+(2900+Math.floor(Math.random()*500)), change:'+'+(10+Math.random()*5).toFixed(1)+'%', up:true, spark:Array.from({length:12},()=>30+Math.random()*60) } },
    { id:'latency', data:{ value:(38+Math.floor(Math.random()*10))+'ms', change:'-'+(5+Math.random()*10).toFixed(1)+'%', up:false, spark:Array.from({length:12},()=>35+Math.random()*25) } },
    { id:'cpu', data:{ value:40+Math.floor(Math.random()*40), max:100, unit:'%' } },
    { id:'memory', data:{ value:60+Math.floor(Math.random()*30), max:100, unit:'%' } },
    { id:'requests', data:{ value:(10+Math.random()*5).toFixed(1)+'k', change:'+'+(10+Math.random()*20).toFixed(1)+'%', up:true, spark:Array.from({length:12},()=>4+Math.random()*12) } },
  ];
  const container = document.getElementById('dashboard');
  updates.forEach(update => {
    const el = container.querySelector('[data-panel-id="'+update.id+'"]');
    if (!el || pageHidden) return;
    const body = el.querySelector('.panel-body');
    if (!body) return;
    const panel = getPanelById(update.id);
    if (!panel) return;
    panel.data = update.data;
    body.innerHTML = renderPanelContent(panel);
  });
}
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
}
function updateStats() {
  const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
  const mins = Math.floor(elapsed/60).toString().padStart(2,'0');
  const secs = (elapsed%60).toString().padStart(2,'0');
  document.getElementById('session-time').textContent = mins+':'+secs;
  document.getElementById('interaction-count').textContent = totalInteractions;
  document.getElementById('adaptation-count').textContent = adaptationCount;
}
function exportConfig() {
  const state = {
    layoutOrder,
    lockedPanels: [...lockedPanels],
    interactionLog: interactionLog.slice(-50),
    adaptationCount,
    totalInteractions,
    scores: scorePanels(),
    ranks: rankPanels(scorePanels()),
    exportedAt: new Date().toISOString()
  };
  const blob = new Blob([JSON.stringify(state, null, 2)], { type:'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'adaptive-layout-export.json';
  a.click();
  URL.revokeObjectURL(url);
  toast('Layout exported');
}
function init() {
  panels = defaultPanels.map(p => ({...p, data: p.data ? {...p.data} : {...p.data}}));
  loadState();
  rebuildDashboard();
  setTimeout(() => adaptLayout(), 2000);
  setInterval(() => adaptLayout(), ADAPT_INTERVAL);
  setInterval(updateStats, 1000);
  document.addEventListener('visibilitychange', () => {
    pageHidden = document.hidden;
    if (!pageHidden && pendingAdapt) {
      pendingAdapt = false;
      adaptLayout();
    }
  });
  document.getElementById('btn-reset').addEventListener('click', () => {
    layoutOrder = defaultPanels.map(p => p.id);
    lockedPanels.clear();
    interactionLog = [];
    adaptationCount = 0;
    totalInteractions = 0;
    panels = defaultPanels.map(p => ({...p, data: p.data ? {...p.data} : {...p.data}}));
    localStorage.removeItem(STORAGE_KEY);
    rebuildDashboard();
    toast('Layout reset to default');
  });
  document.getElementById('btn-export').addEventListener('click', exportConfig);
  setInterval(liveSimulation, 3000);
}
init();
})();
</script>
</body>
</html>