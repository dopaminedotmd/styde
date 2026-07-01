<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --grid-cols:6;--gap:8px;--header-h:48px;--compact-scale:0.35;
  --bg:#0f1117;--panel-bg:#191c24;--panel-border:#2a2e3a;
  --text:#d0d4e0;--text-dim:#7a7f90;--accent:#5b8def;--accent-glow:#5b8def40;
  --rank-1-bg:#1a1f2e;--rank-2-bg:#191e2b;--rank-3-bg:#181c28;--rank-4-bg:#171b26;
  --transition-speed:0.25s;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh}
.header{height:var(--header-h);display:flex;align-items:center;padding:0 16px;border-bottom:1px solid var(--panel-border);gap:12px;position:sticky;top:0;z-index:100;background:var(--bg)}
.header-title{font-weight:700;font-size:15px;letter-spacing:0.3px}
.header-sub{font-size:11px;color:var(--text-dim)}
.header-spacer{flex:1}
.btn{background:var(--panel-bg);border:1px solid var(--panel-border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:background var(--transition-speed),border-color var(--transition-speed)}
.btn:hover{background:#232738;border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.dashboard{position:relative;padding:16px;min-height:calc(100vh - var(--header-h))}
.grid-stage{display:grid;grid-template-columns:repeat(var(--grid-cols),1fr);grid-auto-rows:140px;gap:var(--gap);position:relative}
.panel{
  background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:10px;
  padding:12px;cursor:grab;position:relative;overflow:hidden;
  transition:grid-column var(--transition-speed) ease,grid-row var(--transition-speed) ease,
             width var(--transition-speed) ease,height var(--transition-speed) ease,
             opacity 0.2s ease,transform 0.2s ease,border-color 0.3s ease;
  display:flex;flex-direction:column;min-height:0;
}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.6;z-index:50;transform:scale(0.98);border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 16px var(--accent-glow)}
.panel.drop-target{border:2px dashed var(--accent);background:var(--accent-glow)}
.panel.locked{border-left:3px solid #e8b44b}
.panel.locked .lock-indicator{display:block}
.panel.compact{transform:scale(var(--compact-scale));transform-origin:top left;opacity:0.7;overflow:hidden}
.panel.compact:hover{opacity:1;transform:scale(0.4);z-index:30}
.panel.compact .panel-body{display:none}
.panel.compact .panel-title{font-size:10px}
.panel-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-shrink:0}
.panel-title{font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-btn{width:22px;height:22px;border:none;background:transparent;color:var(--text-dim);cursor:pointer;border-radius:4px;font-size:12px;display:flex;align-items:center;justify-content:center;transition:color 0.15s,background 0.15s}
.panel-btn:hover{color:var(--text);background:#2a2e3a}
.lock-indicator{display:none;color:#e8b44b;font-size:10px}
.panel-body{flex:1;overflow:hidden;min-height:0}
.chart-placeholder{width:100%;height:100%;border-radius:6px;display:flex;align-items:center;justify-content:center;color:var(--text-dim);font-size:11px;position:relative;overflow:hidden}
.bar-chart{display:flex;align-items:flex-end;gap:3px;height:80%;padding:0 8px}
.bar{flex:1;border-radius:3px 3px 0 0;min-width:6px;transition:height 0.5s ease}
.metric-value{font-size:28px;font-weight:800;letter-spacing:-1px}
.metric-label{font-size:11px;color:var(--text-dim)}
.sparkline{width:100%;height:40px;position:relative}
.sparkline svg{width:100%;height:100%}
.rank-badge{position:absolute;top:4px;right:4px;font-size:9px;background:#00000040;padding:2px 6px;border-radius:8px;color:var(--text-dim)}
.drop-zone{
  border:2px dashed var(--panel-border);border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  color:var(--text-dim);font-size:12px;transition:border-color 0.2s,background 0.2s;
  min-height:140px;
}
.drop-zone.active{border-color:var(--accent);background:var(--accent-glow)}
.panel-insert-indicator{position:absolute;background:var(--accent);z-index:60;border-radius:3px;pointer-events:none;opacity:0;transition:opacity 0.15s}
.panel-insert-indicator.visible{opacity:1}
@keyframes panel-flash{0%,100%{border-color:var(--panel-border)}50%{border-color:var(--accent)}}
.panel.flash{animation:panel-flash 0.6s ease}
.compact-section{border:1px dashed var(--panel-border);border-radius:10px;padding:8px;margin-top:8px}
.compact-section-title{font-size:10px;color:var(--text-dim);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.compact-row{display:flex;flex-wrap:wrap;gap:4px}
.compact-pill{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:6px;padding:3px 8px;font-size:10px;cursor:pointer;transition:border-color 0.15s;white-space:nowrap}
.compact-pill:hover{border-color:var(--accent)}
.toast{position:fixed;bottom:20px;right:20px;background:#232738;border:1px solid var(--accent);color:var(--text);padding:10px 16px;border-radius:8px;font-size:12px;z-index:200;animation:toast-in 0.3s ease,toast-out 0.3s ease 1.7s forwards}
@keyframes toast-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes toast-out{from{opacity:1}to{opacity:0}}
</style>
</head>
<body>
<header class="header">
  <span class="header-title">Adaptive Metric Dashboard</span>
  <span class="header-sub" id="rankInfo"></span>
  <span class="header-spacer"></span>
  <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
  <button class="btn" id="btnExport" title="Copy layout JSON">Export</button>
  <button class="btn" id="btnAutoArrange" title="Force re-rank and arrange">Auto-Arrange</button>
</header>
<div class="dashboard" id="dashboard">
  <div class="grid-stage" id="gridStage"></div>
  <div class="compact-section" id="compactSection" style="display:none">
    <div class="compact-section-title">Low Activity</div>
    <div class="compact-row" id="compactRow"></div>
  </div>
</div>
<script>
(function(){
'use strict';
const COLS = 6;
const GAP = 8;
const MIN_SPAN = 1;
const MAX_SPAN = 3;
const ROW_H = 148;
const TRACK_INTERVAL = 2000;
const DECAY_HALF = 3600000;
const COMPACT_THRESHOLD = 0.15;
const MAX_COMPACT = 3;
const LS_KEY = 'adaptive_dashboard_v2';
let panels = [];
let rankCache = null;
let rankCacheKey = '';
let layoutCache = new Map();
let observer = null;
let observerTargets = new WeakMap();
let dirty = true;
let dragState = null;
let trackTimers = new Map();
let trackEntries = new Map();
const defaultPanels = [
  {id:'cpu',title:'CPU Usage',type:'bar',color:'#5b8def',data:[42,55,38,62,48,71,33,58,44,67]},
  {id:'memory',title:'Memory',type:'bar',color:'#e85d75',data:[72,68,74,70,76,71,69,73,75,70]},
  {id:'requests',title:'Requests/sec',type:'metric',color:'#4caf93',value:2847,label:'req/s',trend:[120,190,160,240,210,280,250,310,290,330]},
  {id:'latency',title:'P95 Latency',type:'metric',color:'#e8b44b',value:142,label:'ms',trend:[180,165,155,148,140,138,145,142,140,142]},
  {id:'errors',title:'Error Rate',type:'metric',color:'#e85d75',value:0.12,label:'%',trend:[0.5,0.3,0.4,0.2,0.15,0.18,0.13,0.11,0.14,0.12]},
  {id:'throughput',title:'Throughput',type:'bar',color:'#8b5cf6',data:[120,140,135,155,148,162,158,170,165,180]},
  {id:'sessions',title:'Active Sessions',type:'metric',color:'#38bdf8',value:1248,label:'active',trend:[900,950,1020,1080,1120,1150,1180,1210,1230,1248]},
  {id:'disk',title:'Disk I/O',type:'bar',color:'#fb923c',data:[30,45,28,52,38,44,55,40,48,42]},
  {id:'cache',title:'Cache Hit Ratio',type:'metric',color:'#34d399',value:94.7,label:'%',trend:[91,92,93,93.5,94,94.2,94.5,94.6,94.7,94.7]},
  {id:'queue',title:'Queue Depth',type:'metric',color:'#f472b6',value:23,label:'items',trend:[45,38,32,28,25,24,22,23,22,23]},
  {id:'bandwidth',title:'Bandwidth',type:'bar',color:'#a78bfa',data:[80,85,90,88,95,92,98,96,100,94]},
  {id:'uptime',title:'Uptime',type:'metric',color:'#22d3ee',value:99.98,label:'%',trend:[99.9,99.92,99.95,99.96,99.97,99.98,99.98,99.98,99.98,99.98]},
];
function loadState(){
  try{
    const raw = localStorage.getItem(LS_KEY);
    if(raw){
      const s = JSON.parse(raw);
      panels = s.panels || [];
      trackEntries = new Map(s.trackEntries || []);
      if(panels.length === 0) panels = defaultPanels.map(clonePanel);
    } else {
      panels = defaultPanels.map(clonePanel);
    }
  }catch(e){
    panels = defaultPanels.map(clonePanel);
  }
}
function clonePanel(p){
  return {
    id:p.id,title:p.title,type:p.type,color:p.color,data:p.data?[...p.data]:undefined,
    value:p.value,label:p.label,trend:p.trend?[...p.trend]:undefined,
    locked:false,manualCol:null,manualRow:null,manualSpan:1,
    compact:false,span:MIN_SPAN
  };
}
function saveState(){
  const s = {panels,trackEntries:Array.from(trackEntries.entries())};
  localStorage.setItem(LS_KEY,JSON.stringify(s));
}
function getTrackEntry(panelId){
  if(!trackEntries.has(panelId)){
    trackEntries.set(panelId,{frequency:0,totalDuration:0,lastAccess:Date.now(),collapses:0,expands:0});
  }
  return trackEntries.get(panelId);
}
function computeScore(entry, now){
  const recency = Math.exp(-(now - entry.lastAccess) / DECAY_HALF);
  const freqScore = Math.log(1 + entry.frequency) * 0.4;
  const durScore = Math.log(1 + entry.totalDuration / 1000) * 0.4;
  const recScore = recency * 0.2;
  return freqScore + durScore + recScore;
}
function rankPanels(now){
  const key = panels.map(p=>{
    const e = getTrackEntry(p.id);
    return `${p.id}:${e.frequency}:${e.totalDuration}:${e.lastAccess}`;
  }).join('|');
  if(key === rankCacheKey && rankCache) return rankCache;
  const scored = panels.map(p=>({
    panel:p,
    score:computeScore(getTrackEntry(p.id),now || Date.now())
  }));
  scored.sort((a,b)=>b.score - a.score);
  rankCache = scored;
  rankCacheKey = key;
  return scored;
}
function findFirstSlot(grid, spanW, spanH){
  const rows = grid.length;
  const cols = COLS;
  for(let r = 0; r < rows; r++){
    for(let c = 0; c <= cols - spanW; c++){
      let fits = true;
      for(let dr = 0; dr < spanH && fits; dr++){
        const rr = r + dr;
        if(rr >= rows){fits=false;break;}
        for(let dc = 0; dc < spanW; dc++){
          if(grid[rr][c+dc]){fits=false;break;}
        }
      }
      if(fits) return {col:c,row:r};
    }
  }
  return {col:0,row:rows};
}
function computeLayout(ordered){
  const newKey = ordered.map(o=>`${o.panel.id}:${o.panel.locked}:${o.panel.manualCol}:${o.panel.manualRow}:${o.panel.span}`).join('|');
  if(layoutCache.has(newKey)) return layoutCache.get(newKey);
  const grid = [];
  const layout = new Map();
  const total = ordered.length;
  ordered.forEach((item,idx)=>{
    const p = item.panel;
    let span,row,col;
    if(p.locked && p.manualCol !== null && p.manualRow !== null){
      col = p.manualCol;
      row = p.manualRow;
      span = p.manualSpan || MIN_SPAN;
    } else if(idx < 3){
      span = MAX_SPAN;
    } else if(idx < 6){
      span = 2;
    } else {
      span = MIN_SPAN;
    }
    const spanH = span === MAX_SPAN ? 2 : 1;
    while(grid.length <= row || (row === undefined)){
      grid.push(new Array(COLS).fill(false));
    }
    let slot;
    if(col !== undefined && row !== undefined){
      slot = {col,row};
    } else {
      slot = findFirstSlot(grid, span, spanH);
    }
    while(grid.length <= slot.row + spanH - 1){
      grid.push(new Array(COLS).fill(false));
    }
    for(let dr = 0; dr < spanH; dr++){
      for(let dc = 0; dc < span; dc++){
        grid[slot.row+dr][slot.col+dc] = p.id;
      }
    }
    layout.set(p.id,{col:slot.col,row:slot.row,span,spanH,score:item.score,rank:idx+1});
  });
  layoutCache.set(newKey, layout);
  if(layoutCache.size > 30) layoutCache.clear();
  return layout;
}
function getLayout(){
  const now = Date.now();
  const ranked = rankPanels(now);
  return {layout:computeLayout(ranked),ranked};
}
function buildPanelHTML(p, layoutInfo, rank){
  const locked = p.locked ? ' locked' : '';
  const compact = p.compact ? ' compact' : '';
  const escId = p.id.replace(/[^a-z0-9-]/g,'');
  let bodyHTML = '';
  if(p.type === 'metric'){
    bodyHTML = `<div class="metric-value">${p.value}${p.label ? `<span style="font-size:14px;color:var(--text-dim);margin-left:4px">${p.label}</span>`:''}</div>`;
    if(p.trend){
      const pts = p.trend.map((v,i)=>`${(i/(p.trend.length-1))*100},${100-(v/Math.max(...p.trend))*35}`).join(' ');
      bodyHTML += `<div class="sparkline"><svg viewBox="0 0 100 35"><polyline points="${pts}" fill="none" stroke="${p.color}" stroke-width="2"/></svg></div>`;
    }
  } else if(p.type === 'bar'){
    const max = Math.max(...(p.data||[1]));
    bodyHTML = '<div class="chart-placeholder"><div class="bar-chart">';
    p.data.forEach(v=>{
      const h = (v/max)*100;
      bodyHTML += `<div class="bar" style="height:${h}%;background:${p.color}"></div>`;
    });
    bodyHTML += '</div></div>';
  }
  let rankBadge = '';
  if(!p.compact) rankBadge = `<span class="rank-badge">#${rank}</span>`;
  return `
    <div class="panel${locked}${compact}" data-panel-id="${escId}" id="panel-${escId}"
         style="grid-column:${layoutInfo.col+1}/span ${layoutInfo.span};grid-row:${layoutInfo.row+1}/span ${layoutInfo.spanH};background:var(--rank-${Math.min(rank,4)}-bg)">
      ${rankBadge}
      <div class="panel-header">
        <span class="panel-title">${p.title}</span>
        <div class="panel-actions">
          <button class="panel-btn lock-indicator" data-action="lock" data-pid="${escId}" title="Locked">🔒</button>
          <button class="panel-btn" data-action="lock" data-pid="${escId}" title="${p.locked?'Unlock':'Lock'} position">${p.locked?'🔓':'🔒'}</button>
          <button class="panel-btn" data-action="compact" data-pid="${escId}" title="${p.compact?'Expand':'Compact'}">${p.compact?'📌':'📎'}</button>
        </div>
      </div>
      <div class="panel-body">${bodyHTML}</div>
    </div>`;
}
function buildCompactPill(p){
  const escId = p.id.replace(/[^a-z0-9-]/g,'');
  return `<span class="compact-pill" data-pid="${escId}" data-action="expand">${p.title}</span>`;
}
let renderRAF = null;
let lastRenderHash = '';
function renderHash(){
  const {layout,ranked} = getLayout();
  let h = '';
  ranked.forEach(r=>{
    const li = layout.get(r.panel.id);
    h += `${r.panel.id}:${li.col}:${li.row}:${li.span}:${r.panel.locked}:${r.panel.compact}:${r.score.toFixed(4)};`;
  });
  return h;
}
function render(){
  const currentHash = renderHash();
  if(currentHash === lastRenderHash && !dirty) return;
  lastRenderHash = currentHash;
  dirty = false;
  const {layout,ranked} = getLayout();
  const stage = document.getElementById('gridStage');
  const compactRow = document.getElementById('compactRow');
  const compactSection = document.getElementById('compactSection');
  const activePanels = ranked.filter(r=>!r.panel.compact);
  const compactPanels = ranked.filter(r=>r.panel.compact);
  const frag = document.createDocumentFragment();
  const tempDiv = document.createElement('div');
  activePanels.forEach(item=>{
    const li = layout.get(item.panel.id);
    if(!li) return;
    tempDiv.innerHTML = buildPanelHTML(item.panel,li,li.rank);
    while(tempDiv.firstChild) frag.appendChild(tempDiv.firstChild);
  });
  if(compactPanels.length > 0){
    compactRow.innerHTML = compactPanels.map(p=>buildCompactPill(p.panel)).join('');
    compactSection.style.display = 'block';
  } else {
    compactSection.style.display = 'none';
  }
  const existingPanels = new Map();
  stage.querySelectorAll('.panel').forEach(el=>{
    existingPanels.set(el.dataset.panelId,el);
  });
  const newPanelIds = new Set();
  const toRemove = [];
  existingPanels.forEach((el,id)=>{
    if(!layout.has(id)) toRemove.push(el);
  });
  const newFrag = document.createDocumentFragment();
  const children = frag.children;
  while(children.length){
    const child = children[0];
    const pid = child.dataset.panelId;
    newPanelIds.add(pid);
    const existing = existingPanels.get(pid);
    if(existing){
      existing.style.gridColumn = child.style.gridColumn;
      existing.style.gridRow = child.style.gridRow;
      existing.className = child.className;
      const existingRank = existing.querySelector('.rank-badge');
      const newRank = child.querySelector('.rank-badge');
      if(existingRank && newRank) existingRank.textContent = newRank.textContent;
      else if(!existingRank && newRank) existing.appendChild(newRank.cloneNode(true));
      else if(existingRank && !newRank) existingRank.remove();
    } else {
      newFrag.appendChild(child);
    }
  }
  toRemove.forEach(el=>el.remove());
  if(newFrag.children.length) stage.appendChild(newFrag);
  rebindObservers(stage);
  updateRankInfo(ranked);
}
function rebindObservers(stage){
  if(observer) observer.disconnect();
  const targets = stage.querySelectorAll('.panel:not(.compact)');
  observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      const pid = entry.target.dataset.panelId;
      if(!pid) return;
      const track = getTrackEntry(pid);
      if(entry.isIntersecting){
        if(!trackTimers.has(pid)){
          track.lastAccess = Date.now();
          track.frequency++;
          trackTimers.set(pid,setInterval(()=>{
            track.totalDuration += TRACK_INTERVAL;
            track.lastAccess = Date.now();
          },TRACK_INTERVAL));
        }
      } else {
        if(trackTimers.has(pid)){
          clearInterval(trackTimers.get(pid));
          trackTimers.delete(pid);
        }
      }
    });
  },{threshold:0.5});
  targets.forEach(t=>observer.observe(t));
}
function updateRankInfo(ranked){
  const el = document.getElementById('rankInfo');
  const top3 = ranked.slice(0,3).map((r,i)=>`#${i+1} ${r.panel.title} (${r.score.toFixed(2)})`).join('  ');
  el.textContent = top3 || 'No panels';
}
function invalidateLayout(reason){
  rankCache = null;
  rankCacheKey = '';
  layoutCache.clear();
  dirty = true;
  scheduleRender();
}
function scheduleRender(){
  if(renderRAF) return;
  renderRAF = requestAnimationFrame(()=>{
    renderRAF = null;
    render();
    saveState();
  });
}
function toggleLock(panelId){
  const p = panels.find(x=>x.id===panelId);
  if(!p) return;
  p.locked = !p.locked;
  if(p.locked){
    const {layout} = getLayout();
    const li = layout.get(p.id);
    if(li){
      p.manualCol = li.col;
      p.manualRow = li.row;
      p.manualSpan = li.span;
    }
  } else {
    p.manualCol = null;
    p.manualRow = null;
    p.manualSpan = MIN_SPAN;
  }
  invalidateLayout('lock');
}
function toggleCompact(panelId){
  const p = panels.find(x=>x.id===panelId);
  if(!p) return;
  p.compact = !p.compact;
  if(!p.compact){
    const entry = getTrackEntry(p.id);
    entry.expands++;
  } else {
    const entry = getTrackEntry(p.id);
    entry.collapses++;
  }
  invalidateLayout('compact');
}
function expandFromPill(panelId){
  const p = panels.find(x=>x.id===panelId);
  if(!p) return;
  p.compact = false;
  const entry = getTrackEntry(p.id);
  entry.expands++;
  entry.lastAccess = Date.now();
  invalidateLayout('expand');
}
let dragPanelId = null;
let dragClone = null;
let dragStartCol = null;
let dragStartRow = null;
let dragListenersActive = false;
function onDragStart(e){
  const panel = e.target.closest('.panel');
  if(!panel || panel.classList.contains('compact')) return;
  const pid = panel.dataset.panelId;
  const p = panels.find(x=>x.id===pid);
  if(!p) return;
  dragPanelId = pid;
  dragStartCol = null;
  dragStartRow = null;
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain',pid);
}
function onDragOver(e){
  e.preventDefault();
  if(!dragPanelId) return;
  const panel = e.target.closest('.panel');
  const stage = document.getElementById('gridStage');
  stage.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  if(panel && panel.dataset.panelId !== dragPanelId){
    panel.classList.add('drag-over');
  }
  e.dataTransfer.dropEffect = 'move';
}
function onDragEnd(e){
  const stage = document.getElementById('gridStage');
  stage.querySelectorAll('.panel.dragging,.panel.drag-over').forEach(el=>{
    el.classList.remove('dragging','drag-over');
  });
  dragPanelId = null;
}
function onDrop(e){
  e.preventDefault();
  const stage = document.getElementById('gridStage');
  stage.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  if(!dragPanelId) return;
  const targetPanel = e.target.closest('.panel');
  if(!targetPanel || targetPanel.dataset.panelId === dragPanelId){
    const p = panels.find(x=>x.id===dragPanelId);
    if(p){
      p.locked = false;
      p.manualCol = null;
      p.manualRow = null;
      invalidateLayout('drop-self');
    }
    return;
  }
  const dragP = panels.find(x=>x.id===dragPanelId);
  const targetP = panels.find(x=>x.id===targetPanel.dataset.panelId);
  if(!dragP || !targetP) return;
  const {layout} = getLayout();
  const dragLi = layout.get(dragPanelId);
  const targetLi = layout.get(targetP.id);
  if(!dragLi || !targetLi) return;
  dragP.locked = true;
  dragP.manualCol = targetLi.col;
  dragP.manualRow = targetLi.row;
  dragP.manualSpan = targetLi.span;
  targetP.locked = true;
  targetP.manualCol = dragLi.col;
  targetP.manualRow = dragLi.row;
  targetP.manualSpan = dragLi.span;
  targetPanel.classList.add('flash');
  setTimeout(()=>targetPanel.classList.remove('flash'),600);
  const dragEl = document.getElementById('panel-'+dragPanelId.replace(/[^a-z0-9-]/g,''));
  if(dragEl) dragEl.classList.add('flash');
  dragPanelId = null;
  invalidateLayout('drop-swap');
}
function setupDragListeners(){
  if(dragListenersActive) return;
  const stage = document.getElementById('gridStage');
  stage.addEventListener('dragstart',onDragStart);
  stage.addEventListener('dragover',onDragOver);
  stage.addEventListener('dragend',onDragEnd);
  stage.addEventListener('drop',onDrop);
  dragListenersActive = true;
}
function handleAction(e){
  const btn = e.target.closest('[data-action]');
  if(!btn) return;
  const action = btn.dataset.action;
  const pid = btn.dataset.pid;
  if(action==='lock') toggleLock(pid);
  if(action==='compact') toggleCompact(pid);
  if(action==='expand') expandFromPill(pid);
}
function resetAll(){
  panels = defaultPanels.map(clonePanel);
  trackEntries.clear();
  rankCache = null;
  rankCacheKey = '';
  layoutCache.clear();
  trackTimers.forEach((t,k)=>clearInterval(t));
  trackTimers.clear();
  invalidateLayout('reset');
  showToast('Dashboard reset');
}
function exportState(){
  const s = {panels,trackEntries:Array.from(trackEntries.entries())};
  navigator.clipboard.writeText(JSON.stringify(s,null,2)).then(()=>showToast('Layout JSON copied'));
}
function showToast(msg){
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(()=>t.remove(),2000);
}
function autoCompactCheck(){
  const now = Date.now();
  const ranked = rankPanels(now);
  const total = ranked.reduce((s,r)=>s+r.score,0) || 1;
  let compactCount = panels.filter(p=>p.compact).length;
  ranked.forEach((item,idx)=>{
    const p = item.panel;
    const share = item.score/total;
    if(!p.compact && share < COMPACT_THRESHOLD && idx > 5 && compactCount < MAX_COMPACT){
      p.compact = true;
      compactCount++;
    }
  });
  if(compactCount !== panels.filter(p=>p.compact).length){
    invalidateLayout('auto-compact');
  }
}
function init(){
  loadState();
  setupDragListeners();
  invalidateLayout('init');
  const gridStage = document.getElementById('gridStage');
  gridStage.addEventListener('click',handleAction);
  document.getElementById('compactRow').addEventListener('click',handleAction);
  document.getElementById('btnReset').addEventListener('click',resetAll);
  document.getElementById('btnExport').addEventListener('click',exportState);
  document.getElementById('btnAutoArrange').addEventListener('click',()=>{
    panels.forEach(p=>{p.compact=false;p.locked=false;p.manualCol=null;p.manualRow=null;});
    invalidateLayout('force');
  });
  setInterval(autoCompactCheck,30000);
  render();
}
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',init);
} else {
  init();
}
})();
</script>
</body>
</html>