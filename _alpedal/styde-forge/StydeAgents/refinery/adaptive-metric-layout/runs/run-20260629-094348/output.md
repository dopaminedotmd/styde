<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh}
header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:#161b22;border-bottom:1px solid #30363d}
header h1{font-size:18px;font-weight:600}
.controls{display:flex;gap:8px}
.controls button{padding:6px 14px;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:6px;cursor:pointer;font-size:13px;transition:all .15s}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.dashboard{padding:16px;display:grid;gap:12px;grid-auto-rows:minmax(140px,auto);transition:all .4s ease}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;display:flex;flex-direction:column;transition:all .35s ease;cursor:grab;position:relative}
.panel:hover{border-color:#58a6ff}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important;max-height:140px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.locked{border-color:#d2991d;cursor:default}
.panel.locked::after{content:'\1F512';position:absolute;top:4px;right:40px;font-size:12px;opacity:.7}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#1c2128;border-bottom:1px solid #30363d;min-height:42px}
.panel-title{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px}
.panel-metric{font-size:11px;color:#8b949e;background:#21262d;padding:2px 8px;border-radius:10px}
.panel-actions{display:flex;gap:4px}
.panel-actions button{background:none;border:none;color:#8b949e;cursor:pointer;padding:2px 6px;font-size:14px;border-radius:4px;transition:all .1s}
.panel-actions button:hover{color:#c9d1d9;background:#30363d}
.panel-body{padding:14px;flex:1;display:flex;align-items:center;justify-content:center;min-height:80px}
.panel-preview{display:none;padding:10px 14px;align-items:center;gap:8px;font-size:12px;color:#8b949e}
.panel-preview .spark{height:24px;width:80px;background:linear-gradient(90deg,#1f6feb22,#1f6feb88);border-radius:3px;position:relative;overflow:hidden}
.panel-preview .spark::after{content:'';position:absolute;top:4px;left:4px;right:4px;bottom:4px;background:repeating-linear-gradient(90deg,#58a6ff 0px,#58a6ff 2px,transparent 2px,transparent 6px);opacity:.4}
.more-section{margin-top:8px;padding:8px}
.more-toggle{width:100%;padding:8px;background:#1c2128;border:1px dashed #30363d;color:#8b949e;border-radius:6px;cursor:pointer;font-size:13px;text-align:center}
.more-toggle:hover{border-color:#58a6ff;color:#c9d1d9}
.more-panels{display:grid;gap:12px;margin-top:8px}
.more-panels.collapsed{display:none}
.score-bar{position:absolute;bottom:0;left:0;height:3px;background:#1f6feb;transition:width .5s ease;border-radius:0 2px 0 0}
.chart{width:100%;height:100%;display:flex;align-items:flex-end;gap:4px;padding:0 10px}
.chart .bar{flex:1;background:linear-gradient(0deg,#1f6feb44,#58a6ff);border-radius:3px 3px 0 0;transition:height .4s ease;min-width:8px}
.kpi{font-size:36px;font-weight:700;color:#58a6ff}
.kpi-label{font-size:12px;color:#8b949e;margin-top:4px}
.gauge{width:80px;height:80px;border-radius:50%;background:conic-gradient(#1f6feb var(--pct),#21262d var(--pct));display:flex;align-items:center;justify-content:center}
.gauge-inner{width:60px;height:60px;border-radius:50%;background:#161b22;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700}
.stats{font-size:11px;color:#8b949e;padding:0 14px 8px;display:flex;gap:12px}
.drag-ghost{opacity:.5;border-style:dashed}
</style>
</head>
<body>
<header>
<h1>Adaptive Dashboard</h1>
<div class="controls">
<button onclick="resetAll()" title="Reset all tracking and layout">Reset</button>
<button onclick="toggleEditMode()" id="editBtn">Edit Mode</button>
</div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection"></div>
<script>
const PANEL_DEFS = [
  {id:'cpu',title:'CPU Usage',type:'chart',data:[35,52,28,60,42,38,55,48,32,45,58,40]},
  {id:'memory',title:'Memory',type:'gauge',value:67},
  {id:'requests',title:'Requests/min',type:'kpi',value:'1,247'},
  {id:'errors',title:'Error Rate',type:'kpi',value:'0.12%'},
  {id:'latency',title:'P95 Latency',type:'chart',data:[120,95,140,110,130,105,155,118,125,108,135,115]},
  {id:'users',title:'Active Users',type:'kpi',value:'843'},
  {id:'disk',title:'Disk IO',type:'gauge',value:42},
  {id:'network',title:'Network',type:'chart',data:[820,950,780,1100,890,760,1020,940,870,1050,910,980]},
  {id:'uptime',title:'Uptime',type:'kpi',value:'99.97%'},
  {id:'threads',title:'Thread Pool',type:'gauge',value:31},
  {id:'cache',title:'Cache Hit',type:'gauge',value:88},
  {id:'queue',title:'Queue Depth',type:'chart',data:[5,8,3,12,7,4,9,6,11,5,8,7]}
];
const STORAGE_KEY = 'adaptive_layout_v2';
const DECAY_DAYS = 7;
const MORE_THRESHOLD = 3;
let panels = [];
let editMode = false;
let dragSrc = null;
let locked = new Set();
let moreCollapsed = true;
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch(e) { return {}; }
}
function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}
function now() { return Date.now(); }
function initTracking() {
  let state = loadState();
  if (!state.tracking) state.tracking = {};
  if (!state.overrides) state.overrides = {};
  if (!state.locked) state.locked = [];
  PANEL_DEFS.forEach(p => {
    if (!state.tracking[p.id]) {
      state.tracking[p.id] = {views:0,totalDuration:0,lastView:0,interactions:0,expands:0,collapses:0};
    }
  });
  locked = new Set(state.locked || []);
  return state;
}
let state = initTracking();
let viewStartTimes = {};
function trackView(panelId) {
  if (viewStartTimes[panelId]) return;
  viewStartTimes[panelId] = now();
  state.tracking[panelId].views++;
  state.tracking[panelId].lastView = now();
  state.tracking[panelId].interactions++;
  saveState(state);
}
function trackHide(panelId) {
  if (!viewStartTimes[panelId]) return;
  const duration = now() - viewStartTimes[panelId];
  state.tracking[panelId].totalDuration += duration;
  delete viewStartTimes[panelId];
  saveState(state);
}
function trackExpand(panelId) {
  state.tracking[panelId].expands++;
  state.tracking[panelId].interactions++;
  trackView(panelId);
  saveState(state);
}
function trackCollapse(panelId) {
  state.tracking[panelId].collapses++;
  state.tracking[panelId].interactions++;
  trackHide(panelId);
  saveState(state);
}
function computeScore(track, panelId) {
  const age = (now() - track.lastView) / 1000 / 3600;
  const recency = Math.exp(-age / (DECAY_DAYS * 24));
  const freqPerDay = track.totalDuration > 0 ? track.views / Math.max(1, age / 24) : track.views;
  const durSec = track.totalDuration / 1000;
  const interactionBonus = 1 + Math.log(1 + track.interactions) * 0.2;
  return (freqPerDay * durSec * recency * interactionBonus) || 0;
}
function rankPanels() {
  const nowTs = now();
  return PANEL_DEFS.map(p => {
    const track = state.tracking[p.id] || {views:0,totalDuration:0,lastView:0,interactions:0,expands:0,collapses:0};
    return {
      ...p,
      score: computeScore(track, p.id),
      views: track.views,
      duration: track.totalDuration,
      interactions: track.interactions
    };
  }).sort((a,b) => b.score - a.score);
}
function getLayout() {
  const ranked = rankPanels();
  const overrides = state.overrides || {};
  const top = [];
  const compact = [];
  const more = [];
  ranked.forEach((p, i) => {
    if (locked.has(p.id)) {
      top.push({...p, position: overrides[p.id] || i, size: overrides[p.id + '_size'] || 'large'});
      return;
    }
    if (i < MORE_THRESHOLD && p.score > 0) {
      top.push({...p, position: i, size: i === 0 ? 'xlarge' : i <= 2 ? 'large' : 'medium'});
    } else if (p.score > 0 && p.score >= ranked[MORE_THRESHOLD]?.score * 0.3) {
      compact.push({...p, position: i, size: 'compact'});
    } else {
      more.push({...p, position: i, size: 'hidden'});
    }
  });
  top.sort((a,b) => (a.position || 99) - (b.position || 99));
  if (state.overrides) {
    top.forEach(p => {
      if (state.overrides[p.id] !== undefined) p.position = state.overrides[p.id];
    });
    top.sort((a,b) => (a.position || 99) - (b.position || 99));
  }
  return {top, compact, more};
}
function renderChart(data) {
  const max = Math.max(...data);
  return '<div class="chart">' + data.map(v => {
    const h = (v / max) * 100;
    return '<div class="bar" style="height:' + h + '%" title="' + v + '"></div>';
  }).join('') + '</div>';
}
function renderGauge(value) {
  return '<div style="display:flex;flex-direction:column;align-items:center;gap:8px">' +
    '<div class="gauge" style="--pct:' + value + '%">' +
    '<div class="gauge-inner">' + value + '%</div></div></div>';
}
function renderKPI(value) {
  return '<div style="text-align:center"><div class="kpi">' + value + '</div></div>';
}
function renderPanel(p, size) {
  const track = state.tracking[p.id] || {};
  const scoreDisplay = p.score > 0 ? (p.score / 1000).toFixed(1) + 'k' : '0';
  let body = '';
  if (p.type === 'chart') body = renderChart(p.data || []);
  else if (p.type === 'gauge') body = renderGauge(p.value || 0);
  else body = renderKPI(p.value || '-');
  const lockIcon = locked.has(p.id) ? ' \uD83D\uDD12' : '';
  const compactClass = size === 'compact' ? ' compact' : '';
  const lockedClass = locked.has(p.id) ? ' locked' : '';
  const rowSpan = size === 'xlarge' ? '3' : size === 'large' ? '2' : '1';
  const colSpan = size === 'xlarge' ? '2' : '1';
  return '<div class="panel' + compactClass + lockedClass + '" ' +
    'data-panel="' + p.id + '" ' +
    'style="grid-row:span ' + rowSpan + ';grid-column:span ' + colSpan + '" ' +
    'draggable="' + (!locked.has(p.id) && editMode) + '" ' +
    'ondragstart="handleDragStart(event)" ' +
    'ondragover="handleDragOver(event)" ' +
    'ondrop="handleDrop(event)" ' +
    'ondragend="handleDragEnd(event)" ' +
    'onmouseenter="trackView(\'' + p.id + '\')" ' +
    'onmouseleave="trackHide(\'' + p.id + '\')" ' +
    'onclick="trackView(\'' + p.id + '\')">' +
    '<div class="panel-header">' +
      '<span class="panel-title">' + p.title + lockIcon +
        '<span class="panel-metric">' + scoreDisplay + '</span>' +
      '</span>' +
      '<div class="panel-actions">' +
        (size !== 'compact' && !locked.has(p.id) ? '<button onclick="event.stopPropagation();compactPanel(\'' + p.id + '\')" title="Compact">\u25E2</button>' : '') +
        (size === 'compact' ? '<button onclick="event.stopPropagation();expandPanel(\'' + p.id + '\')" title="Expand">\u25E3</button>' : '') +
        '<button onclick="event.stopPropagation();toggleLock(\'' + p.id + '\')" title="' + (locked.has(p.id) ? 'Unlock' : 'Lock') + '">' + (locked.has(p.id) ? '\uD83D\uDD12' : '\uD83D\uDD13') + '</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' + body + '</div>' +
    '<div class="panel-preview"><span class="spark"></span><span>' + p.title + ' — ' + track.views + ' views</span></div>' +
    '<div class="stats"><span>Views: ' + track.views + '</span><span>Interactions: ' + track.interactions + '</span></div>' +
    '<div class="score-bar" style="width:' + Math.min(100, (p.score / (rankPanels()[0]?.score || 1)) * 100) + '%"></div>' +
  '</div>';
}
function render() {
  const {top, compact, more} = getLayout();
  const dash = document.getElementById('dashboard');
  const moreSec = document.getElementById('moreSection');
  const allTop = [...top, ...compact];
  dash.innerHTML = allTop.map(p => renderPanel(p, p.size)).join('');
  if (more.length > 0) {
    moreSec.innerHTML =
      '<button class="more-toggle" onclick="toggleMore()">' +
      (moreCollapsed ? '\u25B6' : '\u25BC') + ' More panels (' + more.length + ')</button>' +
      '<div class="more-panels' + (moreCollapsed ? ' collapsed' : '') + '" id="morePanels">' +
      more.map(p => renderPanel(p, 'compact')).join('') +
      '</div>';
  } else {
    moreSec.innerHTML = '';
  }
  const editBtn = document.getElementById('editBtn');
  editBtn.className = editMode ? 'active' : '';
  editBtn.textContent = editMode ? 'Done Editing' : 'Edit Mode';
}
function toggleMore() {
  moreCollapsed = !moreCollapsed;
  render();
}
function compactPanel(id) {
  trackCollapse(id);
  render();
}
function expandPanel(id) {
  trackExpand(id);
  render();
}
function toggleLock(id) {
  if (locked.has(id)) {
    locked.delete(id);
  } else {
    locked.add(id);
  }
  state.locked = Array.from(locked);
  saveState(state);
  render();
}
function toggleEditMode() {
  editMode = !editMode;
  render();
}
function handleDragStart(e) {
  if (!editMode || locked.has(e.target.dataset.panel)) {
    e.preventDefault();
    return;
  }
  dragSrc = e.target.closest('.panel');
  if (dragSrc) {
    e.dataTransfer.effectAllowed = 'move';
    dragSrc.classList.add('drag-ghost');
  }
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
}
function handleDrop(e) {
  e.preventDefault();
  const target = e.target.closest('.panel');
  if (!dragSrc || !target || dragSrc === target) return;
  const srcId = dragSrc.dataset.panel;
  const tgtId = target.dataset.panel;
  const ranked = rankPanels();
  const srcIdx = ranked.findIndex(p => p.id === srcId);
  const tgtIdx = ranked.findIndex(p => p.id === tgtId);
  if (!state.overrides) state.overrides = {};
  state.overrides[srcId] = tgtIdx;
  state.overrides[tgtId] = srcIdx;
  locked.add(srcId);
  locked.add(tgtId);
  state.locked = Array.from(locked);
  saveState(state);
  render();
}
function handleDragEnd(e) {
  if (dragSrc) dragSrc.classList.remove('drag-ghost');
  dragSrc = null;
}
function resetAll() {
  localStorage.removeItem(STORAGE_KEY);
  locked.clear();
  state = initTracking();
  moreCollapsed = true;
  render();
}
const visibilityObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const panelId = entry.target.dataset.panel;
    if (!panelId) return;
    if (entry.isIntersecting) trackView(panelId);
    else trackHide(panelId);
  });
}, {threshold: 0.5});
const mutationObserver = new MutationObserver(() => {
  document.querySelectorAll('.panel').forEach(el => {
    if (!el.dataset.observed) {
      visibilityObserver.observe(el);
      el.dataset.observed = '1';
    }
  });
});
mutationObserver.observe(document.getElementById('dashboard'), {childList:true,subtree:true});
setInterval(() => {
  const state = loadState();
  if (JSON.stringify(state) !== JSON.stringify(window.state)) {
    window.state = state;
    locked = new Set(state.locked || []);
  }
}, 5000);
render();
</script>
</body>
</html>