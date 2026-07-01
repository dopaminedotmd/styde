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
  --border: #2a2e3f;
  --text: #e4e6f0;
  --text-muted: #8b8fa8;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.25);
  --danger: #ff5e7a;
  --success: #3dd6c8;
  --warning: #f5a623;
  --radius: 12px;
  --radius-sm: 8px;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
  --gap: 12px;
  --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
}
* { box-sizing:border-box; margin:0; padding:0 }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.header {
  display:flex; align-items:center; justify-content:space-between;
  padding:16px 24px; border-bottom:1px solid var(--border);
  background: var(--surface); position:sticky; top:0; z-index:100;
}
.header h1 { font-size:1.25rem; font-weight:700; letter-spacing:-0.02em }
.header-actions { display:flex; gap:8px }
.btn {
  padding:8px 14px; border:1px solid var(--border); border-radius:var(--radius-sm);
  background:var(--surface); color:var(--text); cursor:pointer;
  font-size:0.8125rem; font-weight:500; transition:var(--transition);
  white-space:nowrap;
}
.btn:hover { background:var(--surface-hover); border-color:var(--accent) }
.btn.active { background:var(--accent); border-color:var(--accent); color:#fff }
.btn.danger { border-color:var(--danger); color:var(--danger) }
.btn.danger:hover { background:var(--danger); color:#fff }
.btn.success { border-color:var(--success); color:var(--success) }
.grid {
  display:grid; gap:var(--gap); padding:var(--gap);
  grid-auto-flow:dense;
}
.panel {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius); box-shadow:var(--shadow);
  transition: all var(--transition); position:relative;
  display:flex; flex-direction:column; overflow:hidden;
  min-height:140px; cursor:grab;
}
.panel:hover { border-color:var(--accent); box-shadow:0 4px 24px var(--accent-glow) }
.panel.dragging { opacity:0.75; transform:scale(0.98); z-index:10; cursor:grabbing }
.panel.locked { border-color:var(--warning); cursor:default }
.panel.locked:hover { border-color:var(--warning); box-shadow:0 0 0 1px var(--warning) }
.panel.compact .panel-body { display:none }
.panel.compact { min-height:52px }
.panel-header {
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 14px; border-bottom:1px solid var(--border);
  user-select:none;
}
.panel-header h3 { font-size:0.875rem; font-weight:600; letter-spacing:-0.01em }
.panel-meta { display:flex; align-items:center; gap:6px }
.panel-rank {
  font-size:0.6875rem; font-weight:700; color:var(--accent);
  background:var(--accent-glow); padding:2px 7px; border-radius:10px;
}
.panel-score { font-size:0.6875rem; color:var(--text-muted) }
.panel-body { padding:12px 14px; flex:1; display:flex; flex-direction:column }
.metric { font-size:1.5rem; font-weight:700; letter-spacing:-0.02em }
.metric-label { font-size:0.75rem; color:var(--text-muted); margin-top:2px }
.trend-up { color:var(--success) }
.trend-down { color:var(--danger) }
.chart-placeholder {
  flex:1; background:var(--bg); border-radius:var(--radius-sm);
  display:flex; align-items:center; justify-content:center;
  color:var(--text-muted); font-size:0.8125rem; min-height:80px;
}
.controls {
  display:flex; gap:6px; flex-wrap:wrap; padding:4px 0;
}
.controls .btn { font-size:0.75rem; padding:4px 10px }
.empty-state {
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:32px; color:var(--text-muted); gap:8px;
}
.empty-state-icon { font-size:2rem; opacity:0.4 }
.skeleton {
  background:linear-gradient(90deg, var(--surface) 25%, var(--surface-hover) 50%, var(--surface) 75%);
  background-size:200% 100%; animation:shimmer 1.5s infinite; border-radius:var(--radius-sm);
}
@keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }
.skeleton-line { height:14px; margin-bottom:8px; width:100% }
.skeleton-line.short { width:60% }
.toast {
  position:fixed; bottom:20px; left:50%; transform:translateX(-50%); z-index:1000;
  background:var(--surface); border:1px solid var(--accent); border-radius:var(--radius-sm);
  padding:10px 20px; font-size:0.8125rem; box-shadow:0 8px 32px rgba(0,0,0,0.4);
  animation:slideUp 0.3s ease; display:flex; align-items:center; gap:8px;
}
.toast.undo { cursor:pointer }
@keyframes slideUp { from{opacity:0;transform:translateX(-50%) translateY(12px)} to{opacity:1;transform:translateX(-50%) translateY(0)} }
.drag-ghost { opacity:0.5; background:var(--accent-glow); border:2px dashed var(--accent); border-radius:var(--radius) }
@media (max-width: 768px) {
  .panel.size-3 { grid-column:span 4 }
  .panel.size-2 { grid-column:span 4 }
  .panel.size-1 { grid-column:span 2 }
  .grid { grid-template-columns:repeat(4,1fr) }
  .header { padding:12px 16px }
  .header h1 { font-size:1rem }
}
@media (min-width: 769px) and (max-width: 1200px) {
  .panel.size-3 { grid-column:span 6 }
  .panel.size-2 { grid-column:span 3 }
  .panel.size-1 { grid-column:span 2 }
  .grid { grid-template-columns:repeat(6,1fr) }
}
@media (min-width: 1201px) {
  .panel.size-3 { grid-column:span 4 }
  .panel.size-2 { grid-column:span 2 }
  .panel.size-1 { grid-column:span 1 }
  .grid { grid-template-columns:repeat(8,1fr) }
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <button class="btn" onclick="resetLayout()" title="Reset all tracking data and layout">Reset</button>
    <button class="btn" id="autoBtn" onclick="toggleAuto()">Auto: ON</button>
    <span style="font-size:0.75rem;color:var(--text-muted);align-self:center" id="saveIndicator"></span>
  </div>
</div>
<div class="grid" id="grid"></div>
<div id="toastContainer"></div>
<script>
const PANELS = [
  {id:'revenue',label:'Revenue',type:'metric',value:'$48,291',trend:'+12.4%',dir:'up'},
  {id:'users',label:'Active Users',type:'metric',value:'2,847',trend:'+8.1%',dir:'up'},
  {id:'latency',label:'P99 Latency',type:'metric',value:'142ms',trend:'-3.2%',dir:'down'},
  {id:'errors',label:'Error Rate',type:'metric',value:'0.12%',trend:'+0.03%',dir:'up'},
  {id:'throughput',label:'Throughput',type:'metric',value:'8.2k/s',trend:'+5.7%',dir:'up'},
  {id:'cpu',label:'CPU Usage',type:'chart',value:'',trend:'',dir:''},
  {id:'memory',label:'Memory',type:'chart',value:'',trend:'',dir:''},
  {id:'requests',label:'Requests/min',type:'chart',value:'',trend:'',dir:''},
  {id:'sessions',label:'Sessions',type:'metric',value:'1,203',trend:'-2.1%',dir:'down'},
  {id:'conversion',label:'Conversion',type:'metric',value:'3.8%',trend:'+0.4%',dir:'up'},
  {id:'disk',label:'Disk I/O',type:'chart',value:'',trend:'',dir:''},
  {id:'cache',label:'Cache Hit Rate',type:'metric',value:'94.2%',trend:'+1.1%',dir:'up'}
];
const STATE_KEY = 'adaptive_dashboard_state';
const DEBOUNCE_MS = 250;
let state = {
  panels: [],
  tracking: {},
  locked: {},
  overrides: {},
  autoLayout: true,
  undoStack: [],
  lastPersist: 0
};
function loadState() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      state.tracking = saved.tracking || {};
      state.locked = saved.locked || {};
      state.overrides = saved.overrides || {};
      state.autoLayout = saved.autoLayout !== false;
    }
  } catch(e) {}
}
function persistState() {
  const now = Date.now();
  if (now - state.lastPersist < 1000) {
    if (!state._pendingPersist) {
      state._pendingPersist = true;
      setTimeout(() => { state._pendingPersist = false; persistState(); }, 1000);
    }
    return;
  }
  state.lastPersist = now;
  const toSave = {
    tracking: state.tracking,
    locked: state.locked,
    overrides: state.overrides,
    autoLayout: state.autoLayout
  };
  localStorage.setItem(STATE_KEY, JSON.stringify(toSave));
  const el = document.getElementById('saveIndicator');
  el.textContent = 'Saved';
  setTimeout(() => { el.textContent = ''; }, 1200);
}
function pushUndo(snapshot) {
  state.undoStack.push(snapshot);
  if (state.undoStack.length > 20) state.undoStack.shift();
}
function popUndo() {
  return state.undoStack.pop();
}
function computeScore(panelId) {
  const t = state.tracking[panelId] || {};
  const now = Date.now();
  const frequency = (t.interactions || 0) + 1;
  const duration = (t.viewDuration || 0) + 1;
  const lastSeen = t.lastInteraction || now;
  const hoursSince = Math.max(1, (now - lastSeen) / 3600000);
  const recency = 1 / Math.log(hoursSince + 1);
  return frequency * Math.log(duration + 1) * (0.3 + 0.7 * recency);
}
function rankPanels() {
  const scores = PANELS.map(p => ({ id: p.id, score: computeScore(p.id) }));
  scores.sort((a, b) => b.score - a.score);
  const ranked = [];
  for (let i = 0; i < scores.length; i++) {
    const panel = PANELS.find(p => p.id === scores[i].id);
    let size;
    if (i < 3) size = 3;
    else if (i < 7) size = 2;
    else size = 1;
    ranked.push({ ...panel, score: scores[i].score, rank: i + 1, size });
  }
  for (const r of ranked) {
    if (state.overrides[r.id] && state.overrides[r.id].size) {
      r.size = state.overrides[r.id].size;
    }
    if (state.overrides[r.id] && state.overrides[r.id].position != null) {
      r.overridePos = state.overrides[r.id].position;
    }
  }
  const lockedItems = ranked.filter(r => state.locked[r.id]);
  const unlockedItems = ranked.filter(r => !state.locked[r.id]);
  unlockedItems.sort((a, b) => {
    if (a.overridePos != null && b.overridePos != null) return a.overridePos - b.overridePos;
    if (a.overridePos != null) return -1;
    if (b.overridePos != null) return 1;
    return a.rank - b.rank;
  });
  const result = [...lockedItems, ...unlockedItems];
  for (let i = 0; i < result.length; i++) {
    if (result[i].overridePos == null && !state.locked[result[i].id]) {
      result[i]._gridOrder = i;
    } else if (result[i].overridePos != null) {
      result[i]._gridOrder = result[i].overridePos;
    } else {
      result[i]._gridOrder = i;
    }
  }
  return result;
}
function shouldCompact(panelId) {
  const score = computeScore(panelId);
  const maxScore = Math.max(...PANELS.map(p => computeScore(p.id)), 1);
  return (score / maxScore) < 0.15;
}
let viewTimers = {};
let observer = null;
function setupViewTracking() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const id = entry.target.dataset.panelId;
      if (!id) continue;
      if (entry.isIntersecting) {
        viewTimers[id] = Date.now();
      } else if (viewTimers[id]) {
        const duration = Date.now() - viewTimers[id];
        if (!state.tracking[id]) state.tracking[id] = { interactions: 0, viewDuration: 0, lastInteraction: 0 };
        state.tracking[id].viewDuration = (state.tracking[id].viewDuration || 0) + duration;
        delete viewTimers[id];
        persistState();
      }
    }
  }, { threshold: 0.3 });
}
function trackInteraction(panelId) {
  if (!state.tracking[panelId]) state.tracking[panelId] = { interactions: 0, viewDuration: 0, lastInteraction: 0 };
  state.tracking[panelId].interactions++;
  state.tracking[panelId].lastInteraction = Date.now();
}
let scheduleId = null;
function scheduleRerank() {
  if (scheduleId) cancelAnimationFrame(scheduleId);
  scheduleId = requestAnimationFrame(() => {
    scheduleId = null;
    if (state.autoLayout) renderGrid();
  });
}
function scheduleRerankDebounced() {
  if (scheduleId) cancelAnimationFrame(scheduleId);
  scheduleId = requestAnimationFrame(() => {
    scheduleId = null;
    if (state.autoLayout) renderGrid();
  });
}
function renderPanel(panel) {
  const compact = shouldCompact(panel.id);
  const locked = !!state.locked[panel.id];
  const score = panel.score || computeScore(panel.id);
  const cls = [
    'panel',
    `size-${panel.size}`,
    compact ? 'compact' : '',
    locked ? 'locked' : ''
  ].filter(Boolean).join(' ');
  let body = '';
  if (panel.type === 'metric') {
    body = `<div class="metric">${panel.value}</div>
      <div class="metric-label">
        <span class="${panel.dir === 'up' ? 'trend-up' : 'trend-down'}">${panel.trend}</span>
        vs last period
      </div>`;
  } else {
    body = `<div class="chart-placeholder">${panel.label} chart — live data stream</div>`;
  }
  return `<div class="${cls}" data-panel-id="${panel.id}" draggable="${!locked}"
    ondragstart="onDragStart(event)" ondragend="onDragEnd(event)"
    ondragover="onDragOver(event)" ondrop="onDrop(event)"
    onclick="trackInteraction('${panel.id}'); scheduleRerankDebounced();">
    <div class="panel-header">
      <h3>${panel.label}</h3>
      <div class="panel-meta">
        <span class="panel-rank">#${panel.rank}</span>
        <span class="panel-score">${score.toFixed(1)}</span>
      </div>
    </div>
    <div class="panel-body">${body}</div>
    <div class="controls" style="padding:6px 14px">
      <button class="btn" onclick="event.stopPropagation(); toggleLock('${panel.id}')">${locked ? 'Unlock' : 'Lock'}</button>
      <button class="btn" onclick="event.stopPropagation(); setSize('${panel.id}',1)">S</button>
      <button class="btn" onclick="event.stopPropagation(); setSize('${panel.id}',2)">M</button>
      <button class="btn" onclick="event.stopPropagation(); setSize('${panel.id}',3)">L</button>
    </div>
  </div>`;
}
function renderSkeleton() {
  let html = '';
  for (let i = 0; i < 8; i++) {
    html += `<div class="panel size-2">
      <div class="panel-header"><div class="skeleton skeleton-line short" style="height:16px"></div></div>
      <div class="panel-body">
        <div class="skeleton skeleton-line" style="height:28px;width:50%"></div>
        <div class="skeleton skeleton-line short"></div>
      </div>
    </div>`;
  }
  return html;
}
function renderEmptyState() {
  return `<div class="empty-state" style="grid-column:1/-1">
    <div class="empty-state-icon">No panels loaded</div>
    <div>Dashboard data will appear here once tracking begins.</div>
  </div>`;
}
function renderGrid() {
  const grid = document.getElementById('grid');
  if (!state.panels || state.panels.length === 0) {
    grid.innerHTML = renderEmptyState();
    return;
  }
  const ranked = rankPanels();
  state.panels = ranked;
  const fragment = document.createDocumentFragment();
  const temp = document.createElement('div');
  temp.innerHTML = ranked.map(p => renderPanel(p)).join('');
  while (temp.firstChild) fragment.appendChild(temp.firstChild);
  grid.innerHTML = '';
  grid.appendChild(fragment);
  setupViewTracking();
  for (const el of grid.querySelectorAll('.panel')) {
    observer.observe(el);
  }
  persistState();
}
function toggleLock(panelId) {
  const snapshot = {
    locked: { ...state.locked },
    overrides: { ...state.overrides }
  };
  if (state.locked[panelId]) {
    delete state.locked[panelId];
  } else {
    state.locked[panelId] = true;
  }
  pushUndo(snapshot);
  trackInteraction(panelId);
  renderGrid();
  persistState();
}
function setSize(panelId, size) {
  const snapshot = {
    overrides: JSON.parse(JSON.stringify(state.overrides))
  };
  if (!state.overrides[panelId]) state.overrides[panelId] = {};
  state.overrides[panelId].size = size;
  pushUndo(snapshot);
  trackInteraction(panelId);
  renderGrid();
  persistState();
}
function toggleAuto() {
  state.autoLayout = !state.autoLayout;
  const btn = document.getElementById('autoBtn');
  btn.textContent = 'Auto: ' + (state.autoLayout ? 'ON' : 'OFF');
  btn.className = 'btn' + (state.autoLayout ? ' active' : '');
  if (state.autoLayout) renderGrid();
  persistState();
}
function resetLayout() {
  localStorage.removeItem(STATE_KEY);
  state.tracking = {};
  state.locked = {};
  state.overrides = {};
  state.autoLayout = true;
  state.undoStack = [];
  document.getElementById('autoBtn').textContent = 'Auto: ON';
  document.getElementById('autoBtn').className = 'btn active';
  const initial = PANELS.map((p, i) => ({
    ...p, score: 1, rank: i + 1, size: i < 3 ? 3 : i < 7 ? 2 : 1
  }));
  state.panels = initial;
  renderGrid();
}
function showToast(msg, actionLabel, actionFn) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast' + (actionFn ? ' undo' : '');
  toast.textContent = msg;
  if (actionFn) {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = actionLabel;
    btn.onclick = () => { actionFn(); toast.remove(); };
    toast.appendChild(btn);
  }
  container.appendChild(toast);
  setTimeout(() => { if (toast.parentNode) toast.remove(); }, 4000);
}
let dragSource = null;
function onDragStart(e) {
  const panel = e.target.closest('.panel');
  if (!panel || panel.classList.contains('locked')) { e.preventDefault(); return; }
  dragSource = panel.dataset.panelId;
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragSource);
}
function onDragEnd(e) {
  const panel = e.target.closest('.panel');
  if (panel) panel.classList.remove('dragging');
  dragSource = null;
}
function onDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
}
function onDrop(e) {
  e.preventDefault();
  const target = e.target.closest('.panel');
  if (!target || !dragSource || dragSource === target.dataset.panelId) return;
  const snapshot = {
    overrides: JSON.parse(JSON.stringify(state.overrides))
  };
  const sourcePanel = state.panels.find(p => p.id === dragSource);
  const targetPanel = state.panels.find(p => p.id === target.dataset.panelId);
  if (!sourcePanel || !targetPanel) return;
  const srcPos = sourcePanel._gridOrder;
  const tgtPos = targetPanel._gridOrder;
  if (!state.overrides[dragSource]) state.overrides[dragSource] = {};
  if (!state.overrides[target.dataset.panelId]) state.overrides[target.dataset.panelId] = {};
  state.overrides[dragSource].position = tgtPos;
  state.overrides[target.dataset.panelId].position = srcPos;
  pushUndo(snapshot);
  trackInteraction(dragSource);
  trackInteraction(target.dataset.panelId);
  renderGrid();
  persistState();
  showToast('Panel swapped', 'Undo', () => {
    const prev = popUndo();
    if (prev) {
      state.overrides = prev.overrides;
      renderGrid();
      persistState();
    }
  });
}
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
    e.preventDefault();
    const prev = popUndo();
    if (prev) {
      if (prev.locked) state.locked = prev.locked;
      if (prev.overrides) state.overrides = prev.overrides;
      renderGrid();
      persistState();
      showToast('Undo applied');
    }
  }
});
const initial = PANELS.map((p, i) => ({
  ...p, score: 1, rank: i + 1, size: i < 3 ? 3 : i < 7 ? 2 : 1
}));
state.panels = initial;
loadState();
document.getElementById('autoBtn').className = 'btn' + (state.autoLayout ? ' active' : '');
document.getElementById('autoBtn').textContent = 'Auto: ' + (state.autoLayout ? 'ON' : 'OFF');
renderGrid();
setInterval(() => {
  if (state.autoLayout) {
    const ranked = rankPanels();
    const changed = ranked.some((p, i) => {
      const old = state.panels[i];
      return !old || p.id !== old.id || p.size !== old.size;
    });
    if (changed) renderGrid();
  }
}, 60000);
</script>
</body>
</html>