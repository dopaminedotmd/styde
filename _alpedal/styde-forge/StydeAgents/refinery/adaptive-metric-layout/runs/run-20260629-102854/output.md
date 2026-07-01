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
  --surface-hover: #22252f;
  --border: #2a2d37;
  --text: #e1e4eb;
  --text-muted: #888b98;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --success: #4ade80;
  --warning: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
*{margin:0;padding:0;box-sizing:border-box}
body{
  background:var(--bg);color:var(--text);
  font-family:system-ui,-apple-system,sans-serif;
  min-height:100vh;padding:16px;
}
.dashboard-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:20px;padding:0 4px;
}
.dashboard-header h1{font-size:1.3rem;font-weight:600;letter-spacing:-0.3px}
.header-meta{display:flex;gap:16px;align-items:center}
.header-meta .badge{
  font-size:0.72rem;padding:4px 10px;border-radius:20px;
  background:var(--surface);border:1px solid var(--border);color:var(--text-muted);
}
.header-meta .badge.active{color:var(--accent);border-color:var(--accent)}
#grid{
  display:grid;grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(140px,auto);gap:12px;
  transition:grid-template-columns var(--transition);
}
.panel{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:14px 16px;
  position:relative;cursor:grab;transition:all var(--transition);
  display:flex;flex-direction:column;overflow:hidden;
  min-height:140px;
}
.panel:hover{border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.panel.dragging{opacity:0.6;cursor:grabbing;z-index:10;transform:scale(0.95)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 30px var(--accent-glow)}
.panel.locked{cursor:default}
.panel.span-2{grid-column:span 2;grid-row:span 2}
.panel.span-2-col{grid-column:span 2}
.panel.span-2-row{grid-row:span 2}
.panel.compact{min-height:70px;padding:10px 14px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:10px;gap:8px;
}
.compact .panel-header{margin-bottom:0}
.panel-title{
  font-size:0.82rem;font-weight:600;color:var(--text);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{
  background:none;border:none;color:var(--text-muted);
  cursor:pointer;font-size:0.85rem;padding:2px 4px;border-radius:4px;
  transition:color 0.15s,background 0.15s;line-height:1;
}
.panel-actions button:hover{color:var(--text);background:rgba(255,255,255,0.05)}
.panel-actions button.locked{color:var(--accent)}
.panel-actions .drag-handle{cursor:grab;font-size:0.75rem;opacity:0.5}
.panel-actions .drag-handle:hover{opacity:1}
.panel.locked .drag-handle{display:none}
.panel-body{flex:1;display:flex;flex-direction:column;gap:8px}
.panel-preview{display:none;align-items:center;gap:8px;font-size:0.75rem;color:var(--text-muted)}
.panel-preview .preview-value{font-weight:700;color:var(--accent);font-size:1.1rem}
.metric-row{display:flex;align-items:center;justify-content:space-between;gap:12px}
.metric-value{font-size:1.6rem;font-weight:700;letter-spacing:-0.5px}
.metric-value.up{color:var(--success)}
.metric-value.down{color:var(--danger)}
.metric-label{font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px}
.metric-change{font-size:0.72rem;font-weight:600}
.metric-change.up{color:var(--success)}.metric-change.down{color:var(--danger)}
.mini-chart{flex:1;display:flex;align-items:flex-end;gap:2px;min-height:40px;margin-top:4px}
.mini-bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-width:3px;transition:height 0.5s}
.chart-svg{flex:1;min-height:50px;width:100%}
.chart-svg svg{width:100%;height:100%}
.activity-feed{flex:1;overflow-y:auto;font-size:0.72rem;display:flex;flex-direction:column;gap:6px}
.activity-item{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--border)}
.activity-item:last-child{border-bottom:none}
.activity-time{color:var(--text-muted);font-size:0.65rem;flex-shrink:0}
.rank-badge{
  position:absolute;top:-1px;right:-1px;
  font-size:0.6rem;padding:2px 7px;border-radius:0 var(--radius) 0 var(--radius);
  background:var(--surface);border:1px solid var(--border);color:var(--text-muted);
  border-top:none;border-right:none;
}
.panel.rank-top .rank-badge{color:var(--accent);border-color:var(--accent)}
.compact-indicator{
  font-size:0.6rem;color:var(--warning);text-transform:uppercase;letter-spacing:0.5px;
}
.reset-btn{
  background:var(--surface);border:1px solid var(--border);color:var(--text-muted);
  padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.72rem;
  transition:all 0.15s;
}
.reset-btn:hover{color:var(--text);border-color:var(--accent)}
.config-panel{
  margin-top:24px;padding:14px 16px;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:0.72rem;
}
.config-panel label{display:flex;align-items:center;gap:6px;color:var(--text-muted)}
.config-panel input{width:70px;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:4px 8px;border-radius:4px;font-size:0.72rem}
.config-panel input:focus{outline:none;border-color:var(--accent)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.sort-pending{animation:pulse 1.5s infinite;color:var(--warning)}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Adaptive Metric Layout</h1>
  <div class="header-meta">
    <span class="badge" id="changes-badge">Changes: 0</span>
    <span class="badge" id="sort-badge">Sorted: just now</span>
    <span class="badge" id="locked-badge">Locked: 0</span>
    <button class="reset-btn" onclick="resetAll()">Reset Layout</button>
  </div>
</div>
<div id="grid"></div>
<div class="config-panel">
  <label>Change threshold <input type="number" id="cfg-threshold" value="10" min="1" max="100" onchange="updateConfig()"></label>
  <label>Flush timeout (ms) <input type="number" id="cfg-flush" value="5000" min="1000" max="60000" step="1000" onchange="updateConfig()"></label>
  <label>Max force (ms) <input type="number" id="cfg-maxforce" value="30000" min="5000" max="300000" step="5000" onchange="updateConfig()"></label>
  <label>Compact threshold <input type="number" id="cfg-compact" value="0.15" min="0.05" max="0.5" step="0.05" onchange="updateConfig()"></label>
  <span id="flush-timer" style="color:var(--text-muted);margin-left:auto">Next sort: 5.0s</span>
</div>
<script>
const CONFIG = {
  batch: {
    changeThreshold: 10,
    flushTimeout: 5000,
    maxForceInterval: 30000
  },
  compactThreshold: 0.15,
  gridColumns: 4
};
const state = {
  panels: new Map(),
  manualOrder: new Map(),
  lockedPanels: new Set(),
  changesSinceSort: 0,
  lastSortTime: Date.now(),
  lastInteractionTime: new Map(),
  refMap: new Map(),
  attentionLog: [],
  flushTimerId: null,
  dragState: null
};
const DEFAULT_PANELS = [
  {id:'revenue',title:'Revenue',type:'metric',value:'$128.4K',change:'+12.3%',trend:'up',bars:[30,45,38,52,60,48,70,65,80,72,88,95]},
  {id:'users',title:'Active Users',type:'metric',value:'8,421',change:'+5.7%',trend:'up',bars:[60,65,58,72,70,75,80,78,85,82,90,88]},
  {id:'conversion',title:'Conversion Rate',type:'metric',value:'3.82%',change:'-0.4%',trend:'down',bars:[4.1,3.9,4.2,3.8,3.7,3.9,4.0,3.6,3.8,3.9,3.5,3.82]},
  {id:'churn',title:'Churn Rate',type:'metric',value:'1.24%',change:'-0.18%',trend:'up',bars:[1.8,1.6,1.7,1.5,1.6,1.4,1.5,1.3,1.4,1.3,1.2,1.24]},
  {id:'latency',title:'Avg Latency',type:'metric',value:'42ms',change:'-8ms',trend:'up',bars:[60,55,58,50,52,45,48,44,46,40,43,42]},
  {id:'errors',title:'Error Rate',type:'metric',value:'0.12%',change:'+0.03%',trend:'down',bars:[0.1,0.08,0.09,0.11,0.1,0.12,0.09,0.13,0.11,0.1,0.14,0.12]},
  {id:'cpu',title:'CPU Usage',type:'chart',value:'67%',data:[45,52,48,60,55,62,58,70,65,72,68,67]},
  {id:'memory',title:'Memory',type:'chart',value:'8.2GB',data:[6,6.5,7,7.2,7.5,7.8,8,8.1,8.3,8.1,8.4,8.2]},
  {id:'requests',title:'Requests/min',type:'chart',value:'1,240',data:[800,900,1100,950,1200,1050,1300,1150,1250,1180,1280,1240]},
  {id:'activity',title:'Activity Feed',type:'feed',items:[
    {time:'2m ago',text:'Deploy v2.4.1 completed'},
    {time:'15m ago',text:'New user signup spike detected'},
    {time:'32m ago',text:'SSL certificate renewed'},
    {time:'1h ago',text:'Database backup finished'},
    {time:'2h ago',text:'Alert: latency threshold breached'}
  ]},
  {id:'top_pages',title:'Top Pages',type:'list',items:[
    {label:'/dashboard',value:'3.2K'},
    {label:'/api/docs',value:'1.8K'},
    {label:'/pricing',value:'1.2K'},
    {label:'/blog',value:'890'},
    {label:'/login',value:'760'}
  ]},
  {id:'realtime',title:'Realtime Events',type:'feed',items:[
    {time:'now',text:'User jane@example.com signed up'},
    {time:'30s ago',text:'Payment $49.99 processed'},
    {time:'1m ago',text:'API key rotated for service-3'},
    {time:'2m ago',text:'Webhook delivery failed (retry 2/3)'},
    {time:'3m ago',text:'Cache invalidation completed'}
  ]}
];
function initScore(p) {
  p._score = 50;
  p._frequency = 0;
  p._duration = 0;
  p._lastViewed = 0;
  return p;
}
function initState() {
  state.panels.clear();
  state.manualOrder.clear();
  state.lockedPanels.clear();
  state.lastInteractionTime.clear();
  state.refMap.clear();
  state.changesSinceSort = 0;
  state.lastSortTime = Date.now();
  DEFAULT_PANELS.forEach((p,i) => {
    const panel = initScore({...p,_index:i});
    state.panels.set(p.id, panel);
  });
}
function persistToStorage() {
  const data = {
    panels: Array.from(state.panels.entries()),
    manualOrder: Array.from(state.manualOrder.entries()),
    lockedPanels: Array.from(state.lockedPanels),
    lastInteractionTime: Array.from(state.lastInteractionTime.entries()),
    lastSortTime: state.lastSortTime,
    config: CONFIG
  };
  try { localStorage.setItem('adaptive_layout_v2', JSON.stringify(data)); } catch(e) {}
}
function loadFromStorage() {
  try {
    const raw = localStorage.getItem('adaptive_layout_v2');
    if (!raw) return false;
    const data = JSON.parse(raw);
    state.panels = new Map(data.panels.map(([k,v]) => [k, initScore({...v})]));
    state.manualOrder = new Map(data.manualOrder);
    state.lockedPanels = new Set(data.lockedPanels);
    state.lastInteractionTime = new Map(data.lastInteractionTime);
    state.lastSortTime = data.lastSortTime || Date.now();
    if (data.config) Object.assign(CONFIG, data.config);
    return true;
  } catch(e) { return false; }
}
function scorePanel(panel, now) {
  const hoursSinceView = Math.max(0, (now - panel._lastViewed) / 3600000);
  const recencyFactor = Math.exp(-hoursSinceView * 0.5);
  const freqNorm = Math.min(panel._frequency / 50, 1);
  const durNorm = Math.min(panel._duration / 300000, 1);
  panel._score = Math.round((freqNorm * 0.4 + durNorm * 0.35 + recencyFactor * 0.25) * 100);
}
function rankPanels() {
  const now = Date.now();
  state.panels.forEach(p => scorePanel(p, now));
  state.lastSortTime = now;
}
function getSortedPanels() {
  const entries = Array.from(state.panels.entries());
  const locked = entries.filter(([id]) => state.lockedPanels.has(id));
  const unlocked = entries.filter(([id]) => !state.lockedPanels.has(id));
  const manualSorted = locked.filter(([id]) => state.manualOrder.has(id))
    .sort((a,b) => (state.manualOrder.get(a[0])||0) - (state.manualOrder.get(b[0])||0));
  const lockedUnsorted = locked.filter(([id]) => !state.manualOrder.has(id));
  unlocked.sort((a,b) => b[1]._score - a[1]._score);
  return [...manualSorted, ...lockedUnsorted, ...unlocked];
}
function getLayoutSlots(sorted) {
  const total = sorted.length;
  const compactCount = Math.max(0, Math.min(
    Math.floor(total * CONFIG.compactThreshold),
    total - 2
  ));
  const layouts = [];
  sorted.forEach(([id, panel], i) => {
    const rank = i;
    const isCompact = rank >= total - compactCount && !state.lockedPanels.has(id);
    let spanClass = '';
    if (!isCompact) {
      if (rank === 0 && total >= 4) spanClass = 'span-2';
      else if (rank === 1 && total >= 6) spanClass = 'span-2-col';
    }
    layouts.push({id, panel, rank, isCompact, spanClass});
  });
  return layouts;
}
function rebuildRefMap() {
  state.refMap.clear();
  document.querySelectorAll('.panel').forEach(el => {
    const id = el.dataset.panelId;
    if (id) state.refMap.set(id, el);
  });
}
function getPanelEl(panelId) {
  return state.refMap.get(panelId);
}
function buildPanelHTML(layout) {
  const {id, panel, rank, isCompact, spanClass} = layout;
  const locked = state.lockedPanels.has(id);
  let bodyHTML = '';
  if (panel.type === 'metric') {
    bodyHTML = `<div class="metric-row"><span class="metric-value ${panel.trend}">${panel.value}</span><span class="metric-change ${panel.trend}">${panel.change}</span></div>
      <div class="mini-chart">${(panel.bars||[]).map(h => `<div class="mini-bar" style="height:${h}%"></div>`).join('')}</div>`;
  } else if (panel.type === 'chart') {
    bodyHTML = `<div class="metric-row"><span class="metric-value">${panel.value}</span></div>
      <div class="mini-chart">${(panel.data||[]).map(h => `<div class="mini-bar" style="height:${Math.max(5,h/80*100)}%"></div>`).join('')}</div>`;
  } else if (panel.type === 'feed') {
    bodyHTML = `<div class="activity-feed">${(panel.items||[]).map(it => `<div class="activity-item"><span>${it.text}</span><span class="activity-time">${it.time}</span></div>`).join('')}</div>`;
  } else if (panel.type === 'list') {
    bodyHTML = `<div class="activity-feed">${(panel.items||[]).map(it => `<div class="activity-item"><span>${it.label}</span><span>${it.value}</span></div>`).join('')}</div>`;
  }
  const previewHTML = panel.type === 'metric'
    ? `<span class="preview-value">${panel.value}</span><span class="metric-change ${panel.trend}">${panel.change}</span>`
    : `<span class="preview-value">${panel.value}</span>`;
  return `<div class="panel ${spanClass}${isCompact?' compact':''}${locked?' locked':''}${rank===0?' rank-top':''}"
    data-panel-id="${id}" draggable="${locked?'false':'true'}">
    <span class="rank-badge">#${rank+1}</span>
    <div class="panel-header">
      <span class="panel-title">${panel.title}</span>
      <div class="panel-actions">
        ${isCompact ? '<span class="compact-indicator">compact</span>' : ''}
        <button class="drag-handle" ${locked?'style="display:none"':''}>⠿</button>
        <button class="lock-btn${locked?' locked':''}" data-action="lock" data-panel-id="${id}">${locked?'🔒':'🔓'}</button>
      </div>
    </div>
    <div class="panel-body">${bodyHTML}</div>
    <div class="panel-preview">${previewHTML}</div>
  </div>`;
}
function renderGrid() {
  rankPanels();
  const sorted = getSortedPanels();
  const layouts = getLayoutSlots(sorted);
  const grid = document.getElementById('grid');
  grid.innerHTML = layouts.map(l => buildPanelHTML(l)).join('');
  rebuildRefMap();
  attachPanelEvents();
  state.changesSinceSort = 0;
  updateBadges();
}
function attachPanelEvents() {
  document.querySelectorAll('.lock-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panelId = btn.dataset.panelId;
      toggleLock(panelId);
    });
  });
  document.querySelectorAll('.panel[draggable="true"]').forEach(el => {
    el.addEventListener('dragstart', handleDragStart);
    el.addEventListener('dragend', handleDragEnd);
  });
  document.querySelectorAll('.panel').forEach(el => {
    el.addEventListener('dragover', e => { e.preventDefault(); el.classList.add('drag-over'); });
    el.addEventListener('dragleave', () => el.classList.remove('drag-over'));
    el.addEventListener('drop', handleDrop);
  });
}
function toggleLock(panelId) {
  if (state.lockedPanels.has(panelId)) {
    state.lockedPanels.delete(panelId);
  } else {
    state.lockedPanels.add(panelId);
  }
  state.changesSinceSort++;
  const el = getPanelEl(panelId);
  if (el) {
    const locked = state.lockedPanels.has(panelId);
    el.classList.toggle('locked', locked);
    el.draggable = !locked;
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.textContent = locked ? '🔒' : '🔓';
      lockBtn.classList.toggle('locked', locked);
    }
    const dragHandle = el.querySelector('.drag-handle');
    if (dragHandle) dragHandle.style.display = locked ? 'none' : '';
  }
  updateBadges();
  persistToStorage();
}
function handleDragStart(e) {
  const panelId = e.target.closest('.panel')?.dataset.panelId;
  if (!panelId || state.lockedPanels.has(panelId)) { e.preventDefault(); return; }
  state.dragState = {id: panelId};
  e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panelId);
}
function handleDragEnd(e) {
  e.target.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  state.dragState = null;
}
function handleDrop(e) {
  e.preventDefault();
  const targetEl = e.target.closest('.panel');
  const dragId = state.dragState?.id;
  if (!dragId || !targetEl) return;
  const targetId = targetEl.dataset.panelId;
  if (dragId === targetId) return;
  const sorted = getSortedPanels();
  const targetIdx = sorted.findIndex(([id]) => id === targetId);
  if (targetIdx === -1) return;
  state.manualOrder.set(dragId, targetIdx);
  state.changesSinceSort++;
  applyLayout();
  persistToStorage();
}
function applyLayout() {
  const sorted = getSortedPanels();
  const layouts = getLayoutSlots(sorted);
  const grid = document.getElementById('grid');
  const existingEls = new Map();
  grid.querySelectorAll('.panel').forEach(el => existingEls.set(el.dataset.panelId, el));
  const fragment = document.createDocumentFragment();
  layouts.forEach((layout, idx) => {
    let el = existingEls.get(layout.id);
    if (!el) {
      const temp = document.createElement('div');
      temp.innerHTML = buildPanelHTML(layout);
      el = temp.firstElementChild;
    } else {
      existingEls.delete(layout.id);
      el.className = `panel ${layout.spanClass}${layout.isCompact?' compact':''}${state.lockedPanels.has(layout.id)?' locked':''}${layout.rank===0?' rank-top':''}`;
      el.draggable = !state.lockedPanels.has(layout.id);
      const rankBadge = el.querySelector('.rank-badge');
      if (rankBadge) rankBadge.textContent = `#${layout.rank+1}`;
      const lockBtn = el.querySelector('.lock-btn');
      if (lockBtn) {
        const locked = state.lockedPanels.has(layout.id);
        lockBtn.textContent = locked ? '🔒' : '🔓';
        lockBtn.classList.toggle('locked', locked);
      }
      const dragHandle = el.querySelector('.drag-handle');
      if (dragHandle) dragHandle.style.display = state.lockedPanels.has(layout.id) ? 'none' : '';
      const compactInd = el.querySelector('.compact-indicator');
      if (layout.isCompact && !compactInd) {
        const hdr = el.querySelector('.panel-header .panel-actions');
        if (hdr) hdr.insertAdjacentHTML('afterbegin', '<span class="compact-indicator">compact</span>');
      } else if (!layout.isCompact && compactInd) {
        compactInd.remove();
      }
    }
    fragment.appendChild(el);
  });
  grid.innerHTML = '';
  grid.appendChild(fragment);
  rebuildRefMap();
  attachPanelEvents();
  updateBadges();
}
function updateBadges() {
  document.getElementById('changes-badge').textContent = `Changes: ${state.changesSinceSort}`;
  const elapsed = Math.round((Date.now() - state.lastSortTime) / 1000);
  document.getElementById('sort-badge').textContent = `Sorted: ${elapsed}s ago`;
  document.getElementById('locked-badge').textContent = `Locked: ${state.lockedPanels.size}`;
}
function updateConfig() {
  CONFIG.batch.changeThreshold = parseInt(document.getElementById('cfg-threshold').value) || 10;
  CONFIG.batch.flushTimeout = parseInt(document.getElementById('cfg-flush').value) || 5000;
  CONFIG.batch.maxForceInterval = parseInt(document.getElementById('cfg-maxforce').value) || 30000;
  CONFIG.compactThreshold = parseFloat(document.getElementById('cfg-compact').value) || 0.15;
  restartFlushTimer();
  persistToStorage();
}
function maybeSort(force = false) {
  const elapsed = Date.now() - state.lastSortTime;
  if (force || state.changesSinceSort >= CONFIG.batch.changeThreshold || elapsed >= CONFIG.batch.maxForceInterval) {
    applyLayout();
    state.lastSortTime = Date.now();
    state.changesSinceSort = 0;
  }
  updateBadges();
}
let flushCountdown = 0;
function restartFlushTimer() {
  if (state.flushTimerId) clearInterval(state.flushTimerId);
  flushCountdown = CONFIG.batch.flushTimeout / 1000;
  state.flushTimerId = setInterval(() => {
    flushCountdown = Math.max(0, flushCountdown - 1);
    document.getElementById('flush-timer').textContent = `Next sort: ${flushCountdown.toFixed(1)}s`;
    if (flushCountdown <= 0) {
      flushCountdown = CONFIG.batch.flushTimeout / 1000;
      maybeSort();
    }
  }, 1000);
}
function resetAll() {
  localStorage.removeItem('adaptive_layout_v2');
  initState();
  renderGrid();
  restartFlushTimer();
}
let visibilityObserver = null;
let visibilityTimers = new Map();
function setupAttentionTracking() {
  if (visibilityObserver) visibilityObserver.disconnect();
  visibilityObserver = new IntersectionObserver((entries) => {
    const now = Date.now();
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      const panel = state.panels.get(panelId);
      if (!panel) return;
      if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
        if (!visibilityTimers.has(panelId)) {
          visibilityTimers.set(panelId, now);
        }
      } else {
        const startTime = visibilityTimers.get(panelId);
        if (startTime) {
          panel._duration += now - startTime;
          panel._lastViewed = now;
          visibilityTimers.delete(panelId);
          state.changesSinceSort++;
        }
      }
    });
  }, { threshold: [0, 0.5, 1.0] });
  state.refMap.forEach(el => visibilityObserver.observe(el));
}
function trackInteraction(panelId) {
  const panel = state.panels.get(panelId);
  if (!panel) return;
  panel._frequency++;
  panel._lastViewed = Date.now();
  state.lastInteractionTime.set(panelId, Date.now());
  state.changesSinceSort++;
  updateBadges();
}
document.addEventListener('click', e => {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  const panelId = panelEl.dataset.panelId;
  if (e.target.closest('.lock-btn')) return;
  trackInteraction(panelId);
});
function init() {
  document.getElementById('cfg-threshold').value = CONFIG.batch.changeThreshold;
  document.getElementById('cfg-flush').value = CONFIG.batch.flushTimeout;
  document.getElementById('cfg-maxforce').value = CONFIG.batch.maxForceInterval;
  document.getElementById('cfg-compact').value = CONFIG.compactThreshold;
  if (!loadFromStorage()) initState();
  renderGrid();
  setupAttentionTracking();
  restartFlushTimer();
}
init();
</script>
</body>
</html>