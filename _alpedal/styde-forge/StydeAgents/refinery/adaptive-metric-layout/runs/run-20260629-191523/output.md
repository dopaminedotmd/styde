<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root{--bg:#0f1117;--panel-bg:#1a1d27;--panel-border:#2a2d3a;--text:#e0e0e0;--text-dim:#888;--accent:#6c8cff;--accent-glow:rgba(108,140,255,0.3);--rank-1:#6c8cff;--rank-2:#5a7ae0;--rank-3:#4868c0;--danger:#ff6b6b;--warn:#ffa94d;--compact-bg:#14161f;--compact-text:#777;font-family:'Segoe UI',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:12px;padding:10px 16px;background:#161820;border-bottom:1px solid var(--panel-border);position:sticky;top:0;z-index:100;flex-wrap:wrap}
.toolbar h1{font-size:1rem;font-weight:600;color:var(--accent);white-space:nowrap}
.toolbar .stat{font-size:0.75rem;color:var(--text-dim);padding:3px 8px;background:#1e2130;border-radius:4px;white-space:nowrap}
.toolbar button{font-size:0.75rem;padding:5px 12px;border:1px solid var(--panel-border);background:#1e2130;color:var(--text);border-radius:4px;cursor:pointer;transition:all .15s;white-space:nowrap}
.toolbar button:hover{background:#2a2d3a;border-color:var(--accent)}
.toolbar button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;gap:8px;padding:8px;min-height:calc(100vh - 50px);transition:grid-template-columns .35s ease,grid-template-rows .35s ease;grid-template-columns:repeat(6,1fr);grid-auto-rows:minmax(120px,auto)}
.panel{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:8px;position:relative;overflow:hidden;transition:all .35s ease,border-color .15s,box-shadow .15s;display:flex;flex-direction:column;cursor:grab;user-select:none}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:.7;z-index:50;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 16px var(--accent-glow)}
.panel.locked{border-color:var(--warn)}
.panel.high-rank{border-left:3px solid var(--rank-1)}
.panel.compact{background:var(--compact-bg)}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{font-size:0.7rem}
.panel.compact .metric-value{font-size:0.75rem}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:8px 10px;font-size:0.8rem;font-weight:600;color:var(--text);cursor:pointer;min-height:34px;flex-shrink:0}
.panel-header-badges{display:flex;gap:4px;align-items:center}
.badge{font-size:0.6rem;padding:1px 5px;border-radius:3px;background:#1e2130;color:var(--text-dim)}
.badge.rank{background:var(--accent);color:#fff;font-weight:700}
.badge.lock{background:var(--warn);color:#000}
.badge.compact-badge{background:#2a2a2a;color:var(--compact-text)}
.panel-controls{display:flex;gap:4px}
.panel-controls button{font-size:0.65rem;padding:2px 6px;border:1px solid var(--panel-border);background:transparent;color:var(--text-dim);border-radius:3px;cursor:pointer;transition:all .1s;line-height:1}
.panel-controls button:hover{background:#2a2d3a;color:var(--text)}
.panel-controls button.on{background:var(--warn);color:#000;border-color:var(--warn)}
.panel-body{flex:1;padding:8px 10px;overflow:hidden;display:flex;flex-direction:column;gap:6px}
.metric-row{display:flex;align-items:baseline;gap:6px}
.metric-value{font-size:1.4rem;font-weight:700;color:var(--text);line-height:1}
.metric-label{font-size:0.7rem;color:var(--text-dim)}
.metric-change{font-size:0.7rem;padding:1px 4px;border-radius:2px}
.metric-change.up{color:#4caf50}
.metric-change.down{color:var(--danger)}
.mini-chart{height:28px;display:flex;align-items:flex-end;gap:1px}
.mini-chart .bar{flex:1;background:var(--accent);opacity:.5;border-radius:1px 1px 0 0;min-width:2px;transition:height .3s}
.heatmap-dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin:0 1px}
.heatmap-dot.hot{background:var(--danger)}
.heatmap-dot.warm{background:var(--warn)}
.heatmap-dot.cold{background:var(--accent)}
.heatmap-dot.cool{background:var(--text-dim)}
.tooltip{position:fixed;pointer-events:none;background:#000;color:#fff;font-size:0.7rem;padding:4px 8px;border-radius:4px;z-index:999;opacity:0;transition:opacity .15s;white-space:nowrap}
.tooltip.show{opacity:1}
.grid.compact-mode .panel:not(.locked):not(.high-rank){grid-column:span 1!important;grid-row:span 1!important}
.resize-handle{position:absolute;bottom:0;right:0;width:14px;height:14px;cursor:nwse-resize;z-index:5;opacity:0;transition:opacity .15s}
.panel:hover .resize-handle{opacity:.6}
</style>
</head>
<body>
<div class="toolbar" id="toolbar">
  <h1>Adaptive Dashboard</h1>
  <span class="stat" id="stat-sessions">Sessions: 0</span>
  <span class="stat" id="stat-visible">Panels: 0</span>
  <span class="stat" id="stat-debounce">Idle</span>
  <button id="btn-reset" title="Reset all tracking data">Reset Data</button>
  <button id="btn-lock-all" title="Toggle lock all panels">Lock All</button>
  <button id="btn-compact-all" title="Toggle compact mode for low-rank panels">Compact Low</button>
  <button id="btn-export" title="Export tracking data as JSON">Export</button>
</div>
<div class="grid" id="grid"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const DEBOUNCE_MS = 4000;
const MAX_TRACKING_ENTRIES = 200;
const RECENCY_HALF_LIFE_MS = 7 * 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD = 0.15;
const DRAG_MIN_PX = 4;
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',metric:'$128,430',label:'MRR',change:'+12.4%',changeDir:'up',spark:[40,55,48,70,62,80,75,85,72,90,82,95]},
  {id:'users',title:'Active Users',metric:'8,942',label:'DAU',change:'+5.7%',changeDir:'up',spark:[30,35,38,42,40,48,45,52,50,58,55,60]},
  {id:'churn',title:'Churn Rate',metric:'2.1%',label:'Monthly',change:'-0.3%',changeDir:'down',spark:[90,85,82,78,75,72,70,68,65,63,62,60]},
  {id:'latency',title:'API Latency',metric:'142ms',label:'p95',change:'+8ms',changeDir:'down',spark:[20,22,25,23,28,26,30,28,32,30,35,33]},
  {id:'errors',title:'Error Rate',metric:'0.12%',label:'5xx',change:'-0.05%',changeDir:'down',spark:[80,75,78,72,70,65,62,60,58,55,52,50]},
  {id:'conversion',title:'Conversion',metric:'3.8%',label:'Signup',change:'+0.4%',changeDir:'up',spark:[10,15,12,18,20,22,25,28,30,32,35,38]},
  {id:'storage',title:'Storage',metric:'842 GB',label:'Used',change:'+18 GB',changeDir:'up',spark:[50,52,55,58,60,62,65,68,70,72,75,78]},
  {id:'queries',title:'Queries/s',metric:'4,210',label:'Avg',change:'+320',changeDir:'up',spark:[35,40,42,45,48,50,52,55,58,60,62,65]},
  {id:'cache',title:'Cache Hit',metric:'94.2%',label:'Ratio',change:'+1.2%',changeDir:'up',spark:[70,72,75,78,80,82,85,87,88,90,92,94]},
  {id:'cpu',title:'CPU Load',metric:'62%',label:'Avg',change:'-4%',changeDir:'down',spark:[85,82,80,78,75,73,70,68,65,63,62,60]},
  {id:'memory',title:'Memory',metric:'14.2 GB',label:'Used',change:'+0.8 GB',changeDir:'up',spark:[55,58,60,62,63,65,67,68,70,72,73,75]},
  {id:'network',title:'Network I/O',metric:'1.2 Gbps',label:'Peak',change:'+0.1 Gbps',changeDir:'up',spark:[30,35,38,40,42,45,48,50,52,54,56,58]}
];
let state = loadState();
let panels = [];
let visibleDurationTimers = {};
let debounceTimer = null;
let layoutDirty = false;
let dragState = null;
let resizeState = null;
let interactionObserver = null;
function defaultPanelState(id){
  return {id:id,viewDurationMs:0,interactions:0,collapses:0,expands:0,lastInteraction:0,locked:false,compact:false,manualRank:null,manualSize:null};
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return {panels:{},sessions:0,layoutVersion:1};
    const parsed = JSON.parse(raw);
    if(parsed.layoutVersion !== 1) return {panels:{},sessions:0,layoutVersion:1};
    parsed.sessions = (parsed.sessions||0) + 1;
    return parsed;
  }catch(e){ return {panels:{},sessions:0,layoutVersion:1}; }
}
function saveState(){
  try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }catch(e){}
}
function getPanelState(id){
  if(!state.panels[id]) state.panels[id] = defaultPanelState(id);
  return state.panels[id];
}
function computeAttentionScore(ps){
  const now = Date.now();
  const hoursSinceLast = ps.lastInteraction ? Math.max(0,(now - ps.lastInteraction)/3600000) : 168;
  const recencyFactor = Math.exp(-hoursSinceLast * Math.LN2 / (RECENCY_HALF_LIFE_MS/3600000));
  const interactions = Math.max(ps.interactions, 1);
  const durationMinutes = Math.max(ps.viewDurationMs / 60000, 0.1);
  return interactions * durationMinutes * (0.3 + 0.7 * recencyFactor);
}
function rankPanels(){
  const scored = panels.map(p => {
    const ps = getPanelState(p.id);
    return {panel:p, score:computeAttentionScore(ps), state:ps};
  });
  scored.sort((a,b) => b.score - a.score);
  return scored;
}
function assignLayout(ranked, forceCompactAll){
  const total = ranked.length;
  if(total === 0) return;
  const maxScore = ranked[0].score || 1;
  ranked.forEach((entry, index) => {
    const ps = entry.state;
    const normScore = maxScore > 0 ? entry.score / maxScore : 0;
    if(ps.locked){
      entry.rank = ps.manualRank !== null ? ps.manualRank : index + 1;
      entry.isCompact = ps.compact;
      entry.colSpan = ps.manualSize || 2;
      entry.rowSpan = 1;
      return;
    }
    entry.rank = index + 1;
    if(forceCompactAll && normScore < COMPACT_THRESHOLD && !ps.locked){
      entry.isCompact = true;
      entry.colSpan = 1;
      entry.rowSpan = 1;
    }else if(normScore < COMPACT_THRESHOLD){
      entry.isCompact = true;
      entry.colSpan = 1;
      entry.rowSpan = 1;
    }else{
      entry.isCompact = false;
      if(index === 0){ entry.colSpan = 2; entry.rowSpan = 2; }
      else if(index <= 2){ entry.colSpan = 2; entry.rowSpan = 1; }
      else if(index <= 5){ entry.colSpan = 1; entry.rowSpan = 2; }
      else { entry.colSpan = 1; entry.rowSpan = 1; }
    }
  });
}
let panelElements = new Map();
let gridEl, tooltipEl;
function createPanelElement(entry){
  const p = entry.panel;
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  if(entry.isCompact) el.classList.add('compact');
  if(entry.rank <= 2) el.classList.add('high-rank');
  if(entry.state.locked) el.classList.add('locked');
  el.style.gridColumn = 'span ' + entry.colSpan;
  el.style.gridRow = 'span ' + entry.rowSpan;
  el.draggable = true;
  const header = document.createElement('div');
  header.className = 'panel-header';
  const titleSpan = document.createElement('span');
  titleSpan.textContent = p.title;
  const badges = document.createElement('div');
  badges.className = 'panel-header-badges';
  const rankBadge = document.createElement('span');
  rankBadge.className = 'badge rank';
  rankBadge.textContent = '#' + entry.rank;
  badges.appendChild(rankBadge);
  if(entry.state.locked){
    const lockBadge = document.createElement('span');
    lockBadge.className = 'badge lock';
    lockBadge.textContent = 'LCK';
    badges.appendChild(lockBadge);
  }
  if(entry.isCompact){
    const compBadge = document.createElement('span');
    compBadge.className = 'badge compact-badge';
    compBadge.textContent = 'MINI';
    badges.appendChild(compBadge);
  }
  const controls = document.createElement('div');
  controls.className = 'panel-controls';
  const lockBtn = document.createElement('button');
  lockBtn.textContent = entry.state.locked ? '🔒' : '🔓';
  lockBtn.className = entry.state.locked ? 'on' : '';
  lockBtn.title = 'Toggle lock';
  lockBtn.addEventListener('click',(e)=>{ e.stopPropagation(); toggleLock(p.id); });
  const expandBtn = document.createElement('button');
  expandBtn.textContent = entry.isCompact ? '⊞' : '⊟';
  expandBtn.title = 'Toggle compact';
  expandBtn.addEventListener('click',(e)=>{ e.stopPropagation(); toggleCompact(p.id); });
  controls.appendChild(lockBtn);
  controls.appendChild(expandBtn);
  header.appendChild(titleSpan);
  header.appendChild(badges);
  header.appendChild(controls);
  const body = document.createElement('div');
  body.className = 'panel-body';
  body.innerHTML = buildPanelBody(p);
  const resizeHandle = document.createElement('div');
  resizeHandle.className = 'resize-handle';
  el.appendChild(header);
  el.appendChild(body);
  el.appendChild(resizeHandle);
  el.addEventListener('dragstart', onDragStart);
  el.addEventListener('dragend', onDragEnd);
  el.addEventListener('dragover', onDragOver);
  el.addEventListener('dragleave', onDragLeave);
  el.addEventListener('drop', onDrop);
  el.addEventListener('click', (e)=>{ if(e.target === el || e.target === header || e.target === titleSpan) recordInteraction(p.id,'click'); });
  header.addEventListener('click',(e)=>{ if(e.target === header || e.target === titleSpan) recordInteraction(p.id,'click'); });
  resizeHandle.addEventListener('mousedown',(e)=>{ e.preventDefault(); e.stopPropagation(); startResize(e,p.id,el); });
  return {el, entry};
}
function buildPanelBody(p){
  const sparkBars = p.spark.map((v,i)=>'<div class="bar" style="height:'+(v*0.3)+'px"></div>').join('');
  const heatHtml = p.spark.slice(-6).map((v,i)=>{
    let cls = 'cool';
    if(v>80) cls='hot';
    else if(v>60) cls='warm';
    else if(v>40) cls='cold';
    return '<span class="heatmap-dot '+cls+'"></span>';
  }).join('');
  return '<div class="metric-row"><span class="metric-value">'+p.metric+'</span><span class="metric-label">'+p.label+'</span><span class="metric-change '+p.changeDir+'">'+p.change+'</span></div><div class="mini-chart">'+sparkBars+'</div><div style="font-size:0.65rem;color:var(--text-dim);margin-top:2px">Activity: '+heatHtml+'</div>';
}
function renderLayout(forceCompactAll){
  const ranked = rankPanels();
  assignLayout(ranked, forceCompactAll);
  const newChildren = [];
  ranked.forEach(entry => {
    const existing = panelElements.get(entry.panel.id);
    let container;
    if(existing){
      container = {el: existing.el, entry: existing.entry};
      updatePanelElement(container, entry);
    }else{
      container = createPanelElement(entry);
      panelElements.set(entry.panel.id, container);
    }
    newChildren.push(container.el);
  });
  const grid = document.getElementById('grid');
  const currentChildren = Array.from(grid.children);
  const newSet = new Set(newChildren);
  currentChildren.forEach(child => {
    if(!newSet.has(child)){
      const pid = child.dataset.panelId;
      panelElements.delete(pid);
      grid.removeChild(child);
    }
  });
  newChildren.forEach((el, idx) => {
    const current = grid.children[idx];
    if(current !== el){
      if(current && newSet.has(current)){
        grid.insertBefore(el, current);
      }else{
        grid.appendChild(el);
      }
    }
  });
  updateToolbar(ranked);
}
function updatePanelElement(container, entry){
  const el = container.el;
  const prevCompact = container.entry.isCompact;
  const prevLocked = container.entry.state.locked;
  const prevRank = container.entry.rank;
  if(entry.colSpan !== container.entry.colSpan || entry.rowSpan !== container.entry.rowSpan){
    el.style.gridColumn = 'span ' + entry.colSpan;
    el.style.gridRow = 'span ' + entry.rowSpan;
  }
  if(entry.isCompact !== prevCompact){
    if(entry.isCompact) el.classList.add('compact'); else el.classList.remove('compact');
  }
  if(entry.rank <= 2) el.classList.add('high-rank'); else el.classList.remove('high-rank');
  if(entry.state.locked !== prevLocked){
    if(entry.state.locked) el.classList.add('locked'); else el.classList.remove('locked');
  }
  const rankBadge = el.querySelector('.badge.rank');
  if(rankBadge && entry.rank !== prevRank) rankBadge.textContent = '#' + entry.rank;
  const lockBadge = el.querySelector('.badge.lock');
  if(entry.state.locked && !lockBadge){
    const b = document.createElement('span'); b.className='badge lock'; b.textContent='LCK';
    el.querySelector('.panel-header-badges').appendChild(b);
  }else if(!entry.state.locked && lockBadge){
    lockBadge.remove();
  }
  const compactBadge = el.querySelector('.badge.compact-badge');
  if(entry.isCompact && !compactBadge){
    const b = document.createElement('span'); b.className='badge compact-badge'; b.textContent='MINI';
    el.querySelector('.panel-header-badges').appendChild(b);
  }else if(!entry.isCompact && compactBadge){
    compactBadge.remove();
  }
  el.querySelector('.panel-controls button:first-child').textContent = entry.state.locked ? '🔒' : '🔓';
  el.querySelector('.panel-controls button:first-child').className = entry.state.locked ? 'on' : '';
  el.querySelector('.panel-controls button:last-child').textContent = entry.isCompact ? '⊞' : '⊟';
  container.entry = entry;
}
function updateToolbar(ranked){
  document.getElementById('stat-sessions').textContent = 'Sessions: ' + state.sessions;
  document.getElementById('stat-visible').textContent = 'Panels: ' + ranked.filter(r=>!r.isCompact).length + '/' + ranked.length;
}
function scheduleLayout(forceCompactAll){
  layoutDirty = true;
  document.getElementById('stat-debounce').textContent = 'Pending...';
  if(debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(()=>{
    debounceTimer = null;
    document.getElementById('stat-debounce').textContent = 'Updating...';
    renderLayout(forceCompactAll);
    saveState();
    layoutDirty = false;
    document.getElementById('stat-debounce').textContent = 'Idle';
  }, DEBOUNCE_MS);
}
function recordInteraction(id, type){
  const ps = getPanelState(id);
  ps.interactions++;
  ps.lastInteraction = Date.now();
  if(type === 'collapse') ps.collapses++;
  if(type === 'expand') ps.expands++;
  scheduleLayout(false);
}
function beginViewTracking(id){
  if(visibleDurationTimers[id]) return;
  visibleDurationTimers[id] = Date.now();
}
function endViewTracking(id){
  if(!visibleDurationTimers[id]) return;
  const elapsed = Date.now() - visibleDurationTimers[id];
  const ps = getPanelState(id);
  ps.viewDurationMs += elapsed;
  delete visibleDurationTimers[id];
}
function toggleLock(id){
  const ps = getPanelState(id);
  ps.locked = !ps.locked;
  if(!ps.locked){ ps.manualRank = null; ps.manualSize = null; }
  recordInteraction(id, ps.locked ? 'lock' : 'unlock');
}
function toggleCompact(id){
  const ps = getPanelState(id);
  ps.compact = !ps.compact;
  recordInteraction(id, ps.compact ? 'collapse' : 'expand');
}
function onDragStart(e){
  const id = e.currentTarget.dataset.panelId;
  const ps = getPanelState(id);
  if(ps.locked){ e.preventDefault(); return; }
  if(e.clientX === 0 && e.clientY === 0) return;
  dragState = {sourceId:id, sourceEl:e.currentTarget,startX:e.clientX,startY:e.clientY};
  e.currentTarget.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', id);
  setTimeout(()=>{ if(dragState) dragState.sourceEl.style.opacity='0.4'; },0);
}
function onDragEnd(e){
  if(!dragState) return;
  dragState.sourceEl.classList.remove('dragging');
  dragState.sourceEl.style.opacity = '';
  document.querySelectorAll('.drag-over').forEach(el=>el.classList.remove('drag-over'));
  dragState = null;
}
function onDragOver(e){
  e.preventDefault();
  if(!dragState) return;
  const targetEl = e.currentTarget;
  if(targetEl === dragState.sourceEl) return;
  targetEl.classList.add('drag-over');
  e.dataTransfer.dropEffect = 'move';
}
function onDragLeave(e){
  e.currentTarget.classList.remove('drag-over');
}
function onDrop(e){
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  if(!dragState) return;
  const targetId = e.currentTarget.dataset.panelId;
  if(targetId === dragState.sourceId) return;
  const sourcePs = getPanelState(dragState.sourceId);
  const targetPs = getPanelState(targetId);
  if(targetPs.locked) return;
  sourcePs.locked = true;
  sourcePs.manualRank = null;
  sourcePs.manualSize = null;
  targetPs.locked = true;
  targetPs.manualRank = null;
  targetPs.manualSize = null;
  const sourceIdx = panels.findIndex(p=>p.id===dragState.sourceId);
  const targetIdx = panels.findIndex(p=>p.id===targetId);
  if(sourceIdx >= 0 && targetIdx >= 0){
    const tmp = panels[sourceIdx];
    panels[sourceIdx] = panels[targetIdx];
    panels[targetIdx] = tmp;
  }
  recordInteraction(dragState.sourceId, 'drop');
  scheduleLayout(false);
  dragState = null;
}
function startResize(e, id, el){
  const startX = e.clientX;
  const startY = e.clientY;
  const startW = el.offsetWidth;
  const startH = el.offsetHeight;
  resizeState = {id, el, startX, startY, startW, startH};
  function onMove(ev){
    if(!resizeState) return;
    const dx = ev.clientX - resizeState.startX;
    const dy = ev.clientY - resizeState.startY;
    const nw = Math.max(120, resizeState.startW + dx);
    const nh = Math.max(80, resizeState.startH + dy);
    resizeState.el.style.width = nw + 'px';
    resizeState.el.style.height = nh + 'px';
  }
  function onUp(ev){
    if(!resizeState) return;
    const ps = getPanelState(resizeState.id);
    ps.locked = true;
    ps.manualSize = Math.max(1, Math.round(resizeState.el.offsetWidth / 180));
    resizeState.el.style.width = '';
    resizeState.el.style.height = '';
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onUp);
    resizeState = null;
    scheduleLayout(false);
  }
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onUp);
}
function setupIntersectionObserver(){
  if(interactionObserver) interactionObserver.disconnect();
  interactionObserver = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      const id = entry.target.dataset.panelId;
      if(!id) return;
      if(entry.isIntersecting) beginViewTracking(id);
      else endViewTracking(id);
    });
  },{threshold:0.6});
}
function observePanel(el){
  if(interactionObserver) interactionObserver.observe(el);
}
function init(){
  gridEl = document.getElementById('grid');
  tooltipEl = document.getElementById('tooltip');
  panels = PANEL_DEFS.map(d=>({...d}));
  panels.forEach(p=>{ if(!state.panels[p.id]) state.panels[p.id]=defaultPanelState(p.id); });
  renderLayout(false);
  setupIntersectionObserver();
  document.querySelectorAll('.panel').forEach(el=>observePanel(el));
  const origAppend = gridEl.appendChild.bind(gridEl);
  gridEl.appendChild = function(child){
    origAppend(child);
    if(child.classList && child.classList.contains('panel')) observePanel(child);
    return child;
  };
  const origInsert = gridEl.insertBefore.bind(gridEl);
  gridEl.insertBefore = function(child, ref){
    origInsert(child, ref);
    if(child.classList && child.classList.contains('panel')) observePanel(child);
    return child;
  };
  document.getElementById('btn-reset').addEventListener('click',()=>{
    if(confirm('Clear all tracking data and reset layout?')){
      state = {panels:{},sessions:0,layoutVersion:1};
      panels = PANEL_DEFS.map(d=>({...d}));
      panels.forEach(p=>{ state.panels[p.id]=defaultPanelState(p.id); });
      panelElements.clear();
      saveState();
      renderLayout(false);
    }
  });
  document.getElementById('btn-lock-all').addEventListener('click',()=>{
    const allLocked = panels.every(p=>getPanelState(p.id).locked);
    panels.forEach(p=>{
      const ps = getPanelState(p.id);
      ps.locked = !allLocked;
      if(!ps.locked){ ps.manualRank=null; ps.manualSize=null; }
    });
    scheduleLayout(false);
  });
  let compactAllActive = false;
  document.getElementById('btn-compact-all').addEventListener('click',()=>{
    compactAllActive = !compactAllActive;
    document.getElementById('btn-compact-all').classList.toggle('active',compactAllActive);
    scheduleLayout(compactAllActive);
  });
  document.getElementById('btn-export').addEventListener('click',()=>{
    const data = JSON.stringify(state, null, 2);
    const blob = new Blob([data],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'dashboard-tracking-'+new Date().toISOString().slice(0,10)+'.json'; a.click();
    URL.revokeObjectURL(url);
  });
  window.addEventListener('beforeunload',()=>{
    Object.keys(visibleDurationTimers).forEach(endViewTracking);
    saveState();
  });
  setTimeout(()=>{
    if(interactionObserver){
      document.querySelectorAll('.panel').forEach(el=>interactionObserver.observe(el));
    }
  },100);
}
if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
})();
</script>
</body>
</html>