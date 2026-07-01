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
  --border: #2a2e3d;
  --text: #e1e4ed;
  --text-muted: #8b90a0;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.25);
  --danger: #ff5c6e;
  --warning: #ffb84d;
  --success: #4ade80;
  --rank-1: #6c8cff;
  --rank-2: #5da0f0;
  --rank-3: #4db8d8;
  --rank-4: #8b90a0;
  --compact-scale: 0.45;
  --transition-speed: 0.35s;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:14px 24px;
  border-bottom:1px solid var(--border);
  background:var(--surface);
  position:sticky;
  top:0;
  z-index:100;
  backdrop-filter:blur(12px);
}
header h1{font-size:1.2rem;font-weight:600;letter-spacing:-0.01em}
.header-actions{display:flex;gap:10px;align-items:center}
.btn{
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--text);
  padding:7px 16px;
  border-radius:7px;
  cursor:pointer;
  font-size:0.8rem;
  font-weight:500;
  transition:all 0.2s;
  white-space:nowrap;
}
.btn:hover{background:var(--surface-hover);border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn-sm{padding:4px 10px;font-size:0.72rem}
.btn-icon{padding:5px 8px;font-size:0.85rem;line-height:1}
.usage-badge{
  font-size:0.7rem;
  color:var(--text-muted);
  background:var(--bg);
  padding:4px 10px;
  border-radius:20px;
  border:1px solid var(--border);
}
.dashboard{
  display:grid;
  gap:12px;
  padding:16px;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  transition:all var(--transition-speed) ease;
}
.dashboard.compact-layout{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:11px;
  overflow:hidden;
  transition:all var(--transition-speed) ease;
  position:relative;
  display:flex;
  flex-direction:column;
  min-height:140px;
  cursor:grab;
  user-select:none;
}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.6;z-index:50;box-shadow:0 8px 32px rgba(0,0,0,0.5)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow)}
.panel.pinned{border-left:3px solid var(--accent)}
.panel.compact{
  grid-row:span 1;
  min-height:80px;
  transform:scale(var(--compact-scale));
  transform-origin:top left;
  opacity:0.7;
  margin-bottom:-30px;
}
.panel.compact:hover{opacity:1;transform:scale(1);z-index:10;margin-bottom:0}
.panel.collapsed{display:none}
.panel-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:10px 14px;
  border-bottom:1px solid var(--border);
  background:rgba(255,255,255,0.015);
}
.panel-title{
  font-size:0.82rem;
  font-weight:600;
  display:flex;
  align-items:center;
  gap:8px;
}
.panel-title .dot{
  width:8px;
  height:8px;
  border-radius:50%;
  display:inline-block;
}
.panel-actions{display:flex;gap:4px}
.panel-body{
  padding:14px;
  flex:1;
  display:flex;
  flex-direction:column;
  gap:8px;
  transition:all 0.3s;
}
.panel.compact .panel-body{padding:8px;gap:4px}
.metric-value{
  font-size:2rem;
  font-weight:700;
  letter-spacing:-0.02em;
  line-height:1;
}
.metric-label{font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em}
.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.mini-metric{text-align:center}
.mini-metric .val{font-size:1.1rem;font-weight:600}
.mini-metric .lbl{font-size:0.62rem;color:var(--text-muted)}
.sparkline{
  height:36px;
  width:100%;
  margin-top:4px;
}
.sparkline svg{width:100%;height:100%}
.rank-badge{
  position:absolute;
  top:8px;
  right:8px;
  font-size:0.6rem;
  background:var(--bg);
  padding:2px 7px;
  border-radius:10px;
  color:var(--text-muted);
  z-index:2;
}
.tooltip{
  position:fixed;
  background:var(--surface);
  border:1px solid var(--border);
  padding:8px 12px;
  border-radius:7px;
  font-size:0.72rem;
  z-index:999;
  pointer-events:none;
  box-shadow:0 4px 16px rgba(0,0,0,0.4);
  opacity:0;
  transition:opacity 0.15s;
}
.tooltip.show{opacity:1}
.more-section{
  margin:0 16px 16px;
  padding:12px 16px;
  border:1px dashed var(--border);
  border-radius:11px;
  background:rgba(255,255,255,0.01);
}
.more-section summary{
  cursor:pointer;
  font-size:0.78rem;
  font-weight:500;
  color:var(--text-muted);
  user-select:none;
}
.more-section summary:hover{color:var(--text)}
.more-panels{
  display:grid;
  gap:8px;
  grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  margin-top:10px;
}
.toast{
  position:fixed;
  bottom:24px;
  right:24px;
  background:var(--surface);
  border:1px solid var(--border);
  padding:10px 18px;
  border-radius:9px;
  font-size:0.75rem;
  z-index:200;
  opacity:0;
  transform:translateY(10px);
  transition:all 0.3s;
  pointer-events:none;
}
.toast.show{opacity:1;transform:translateY(0)}
@media(max-width:768px){
  .dashboard{
    grid-template-columns:1fr;
    gap:8px;
    padding:10px;
  }
  .panel.compact{
    transform:scale(0.8);
    margin-bottom:-10px;
  }
  .metric-value{font-size:1.5rem}
  header{padding:10px 14px}
  header h1{font-size:1rem}
  .header-actions{gap:6px}
  .btn{padding:5px 10px;font-size:0.7rem}
}
@media(prefers-reduced-motion:reduce){
  .panel,.dashboard,.tooltip,.toast{transition:none}
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Layout</h1>
  <div class="header-actions">
    <span class="usage-badge" id="session-time">00:00</span>
    <button class="btn btn-sm" id="btn-reset" title="Reset layout learning">Reset</button>
    <button class="btn btn-sm active" id="btn-auto" title="Auto-layout enabled">Auto</button>
    <button class="btn btn-sm" id="btn-export" title="Export preferences">Export</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<details class="more-section" id="more-section" open>
  <summary>More panels <span id="more-count"></span></summary>
  <div class="more-panels" id="more-panels"></div>
</details>
<div class="tooltip" id="tooltip"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_layout_v1';
const IDLE_DEBOUNCE = 4000;
const POLL_INTERVAL = 3500;
const VIEW_INTERVAL = 2000;
const DECAY_HALF = 7200000;
const HISTORY_MAX = 200;
let panels = [
  {id:'cpu',title:'CPU Usage',icon:'🖥',unit:'%',min:0,max:100,color:'var(--rank-1)',mockBase:35,mockAmp:20},
  {id:'memory',title:'Memory',icon:'🧠',unit:'GB',min:0,max:64,color:'var(--rank-2)',mockBase:28,mockAmp:12,valFmt:v=>v.toFixed(1)},
  {id:'disk',title:'Disk I/O',icon:'💾',unit:'MB/s',min:0,max:500,color:'var(--rank-3)',mockBase:120,mockAmp:80},
  {id:'network',title:'Network',icon:'🌐',unit:'Mbps',min:0,max:1000,color:'var(--rank-1)',mockBase:320,mockAmp:200},
  {id:'api_latency',title:'API Latency',icon:'⏱',unit:'ms',min:0,max:500,color:'var(--warning)',mockBase:85,mockAmp:60,alertAbove:200},
  {id:'error_rate',title:'Error Rate',icon:'⚠',unit:'%',min:0,max:100,color:'var(--danger)',mockBase:1.2,mockAmp:2.5,valFmt:v=>v.toFixed(2),alertAbove:5},
  {id:'throughput',title:'Throughput',icon:'📊',unit:'rps',min:0,max:5000,color:'var(--success)',mockBase:1800,mockAmp:800},
  {id:'active_users',title:'Active Users',icon:'👥',unit:'',min:0,max:2000,color:'var(--rank-2)',mockBase:420,mockAmp:180},
  {id:'db_conn',title:'DB Connections',icon:'🗄',unit:'',min:0,max:100,color:'var(--rank-3)',mockBase:24,mockAmp:12},
  {id:'cache_hit',title:'Cache Hit Rate',icon:'💨',unit:'%',min:0,max:100,color:'var(--success)',mockBase:87,mockAmp:8,valFmt:v=>v.toFixed(1)},
  {id:'queue_depth',title:'Queue Depth',icon:'📥',unit:'',min:0,max:500,color:'var(--warning)',mockBase:45,mockAmp:35},
  {id:'response_time',title:'P99 Response',icon:'📈',unit:'ms',min:0,max:1000,color:'var(--danger)',mockBase:210,mockAmp:120,alertAbove:500}
];
let state = loadState();
let viewTimers = {};
let interactionCounts = {};
let panelOrder = state.order || panels.map(p=>p.id);
let pinnedPanels = state.pinned || {};
let collapsedPanels = state.collapsed || {};
let autoLayout = state.autoLayout !== false;
let rankings = state.rankings || {};
let historyLog = state.historyLog || [];
let sessionStart = Date.now();
let layoutDebounce = null;
let observer = null;
let dragState = null;
function defaultRankings(){
  let r = {};
  panels.forEach(p=>{r[p.id]={score:50,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:Date.now()}});
  return r;
}
if(Object.keys(rankings).length===0) rankings = defaultRankings();
function loadState(){
  try{
    let raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  }catch(e){return{}}
}
function saveState(){
  let data = {order:panelOrder,pinned:pinnedPanels,collapsed:collapsedPanels,autoLayout,rankings,historyLog};
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(data))}catch(e){}
}
function mockValue(panel){
  let base = panel.mockBase, amp = panel.mockAmp;
  let noise = (Math.random()-0.5)*amp*0.3;
  let wave = Math.sin(Date.now()/12000 + panels.indexOf(panel)*1.7)*amp*0.4;
  let val = base + noise + wave;
  return Math.max(panel.min,Math.min(panel.max,val));
}
function formatValue(panel,v){
  if(panel.valFmt) return panel.valFmt(v);
  return Math.round(v).toString();
}
function alertLevel(panel,v){
  if(panel.alertAbove && v>panel.alertAbove) return 'var(--danger)';
  return panel.color;
}
function historyPoints(panelId,n){
  let pts = historyLog.filter(h=>h.panel===panelId).slice(-n);
  return pts.map(p=>p.value);
}
function sparklineSvg(panelId,color,width,height){
  let pts = historyPoints(panelId,30);
  if(pts.length<2) return '';
  let panel = panels.find(p=>p.id===panelId);
  let min=Infinity,max=-Infinity;
  pts.forEach(v=>{if(v<min)min=v;if(v>max)max=v});
  let range = max-min || 1;
  let padX=2,padY=2;
  let w=width-padX*2,h=height-padY*2;
  let points = pts.map((v,i)=>{
    let x = padX + (i/(pts.length-1))*w;
    let y = padY + h - ((v-min)/range)*h;
    return x.toFixed(1)+','+y.toFixed(1);
  }).join(' ');
  return '<svg viewBox="0 0 '+width+' '+height+'"><polyline points="'+points+'" fill="none" stroke="'+color+'" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}
function computeScore(panelId){
  let r = rankings[panelId] || {score:50,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:0};
  let now = Date.now();
  let ageHours = Math.max(0,(now - r.lastAccess))/3600000;
  let recency = Math.exp(-ageHours * Math.log(2)/(DECAY_HALF/3600000));
  let freqScore = Math.log2(r.totalViews+1)*10;
  let durScore = Math.log2(r.totalDuration/1000+1)*8;
  let intScore = Math.log2(r.totalInteractions+1)*6;
  return (freqScore + durScore + intScore)*recency;
}
function rankAll(){
  let scores = panels.map(p=>({id:p.id,score:computeScore(p.id)}));
  scores.sort((a,b)=>b.score-a.score);
  return scores;
}
function rearrangeLayout(){
  if(!autoLayout) return;
  let ranked = rankAll();
  let ordered = [];
  let pinnedIds = Object.keys(pinnedPanels).filter(id=>pinnedPanels[id]);
  let collapsedIds = Object.keys(collapsedPanels).filter(id=>collapsedPanels[id]);
  pinnedIds.forEach(id=>{if(!ordered.includes(id))ordered.push(id)});
  ranked.forEach(r=>{if(!ordered.includes(r.id) && !collapsedIds.includes(r.id))ordered.push(r.id)});
  let prev = panelOrder.join(',');
  panelOrder = ordered;
  if(prev !== panelOrder.join(',')){
    rankings = ranked.reduce((acc,r)=>{acc[r.id]=rankings[r.id]||{score:r.score,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:Date.now()};acc[r.id].score=r.score;return acc},{});
    renderPanels(true);
    saveState();
  }
}
function scheduleRearrange(){
  clearTimeout(layoutDebounce);
  layoutDebounce = setTimeout(rearrangeLayout,IDLE_DEBOUNCE);
}
function recordView(panelId){
  if(!rankings[panelId]) rankings[panelId]={score:50,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:Date.now()};
  rankings[panelId].totalViews++;
  rankings[panelId].lastAccess = Date.now();
  scheduleRearrange();
}
function recordInteraction(panelId){
  if(!rankings[panelId]) rankings[panelId]={score:50,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:Date.now()};
  rankings[panelId].totalInteractions++;
  rankings[panelId].lastAccess = Date.now();
  scheduleRearrange();
}
function recordDuration(panelId,ms){
  if(!rankings[panelId]) rankings[panelId]={score:50,totalViews:0,totalDuration:0,totalInteractions:0,lastAccess:Date.now()};
  rankings[panelId].totalDuration += ms;
  rankings[panelId].lastAccess = Date.now();
}
function startViewTimer(panelId){
  if(viewTimers[panelId]) return;
  viewTimers[panelId] = Date.now();
}
function stopViewTimer(panelId){
  if(!viewTimers[panelId]) return 0;
  let elapsed = Date.now() - viewTimers[panelId];
  delete viewTimers[panelId];
  if(elapsed>500) recordDuration(panelId,elapsed);
  return elapsed;
}
function setupObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      let panelId = e.target.dataset.panelId;
      if(!panelId) return;
      if(e.isIntersecting){
        startViewTimer(panelId);
        recordView(panelId);
      }else{
        stopViewTimer(panelId);
      }
    });
  },{threshold:0.3});
}
function observePanel(el){
  if(observer) observer.observe(el);
}
function unobservePanel(el){
  if(observer) observer.unobserve(el);
}
function buildPanelElement(panel,rank){
  let el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = panel.id;
  el.draggable = true;
  if(pinnedPanels[panel.id]) el.classList.add('pinned');
  let isCompact = rank>=8 && !pinnedPanels[panel.id];
  if(isCompact) el.classList.add('compact');
  if(collapsedPanels[panel.id]) el.classList.add('collapsed');
  let val = mockValue(panel);
  let color = alertLevel(panel,val);
  let sparkW=280,sparkH=36;
  let spark = isCompact?'':sparklineSvg(panel.id,color,sparkW,sparkH);
  el.innerHTML =
    '<div class="rank-badge">#'+(rank+1)+' · '+Math.round(rankings[panel.id]?.score||50)+'</div>'+
    '<div class="panel-header">'+
      '<span class="panel-title"><span class="dot" style="background:'+color+'"></span>'+panel.icon+' '+panel.title+'</span>'+
      '<div class="panel-actions">'+
        '<button class="btn btn-icon btn-sm pin-btn" data-action="pin" title="'+(pinnedPanels[panel.id]?'Unpin':'Pin')+'">'+(pinnedPanels[panel.id]?'📌':'📍')+'</button>'+
        '<button class="btn btn-icon btn-sm collapse-btn" data-action="collapse" title="Collapse">−</button>'+
      '</div>'+
    '</div>'+
    '<div class="panel-body">'+
      '<div class="metric-value" style="color:'+color+'">'+formatValue(panel,val)+'<span style="font-size:0.7rem;margin-left:4px">'+panel.unit+'</span></div>'+
      '<div class="metric-label">Current</div>'+
      (isCompact?'':'<div class="sparkline">'+spark+'</div>')+
      (isCompact?'':'<div class="metric-grid">'+
        '<div class="mini-metric"><div class="val">'+rankings[panel.id]?.totalViews||0+'</div><div class="lbl">Views</div></div>'+
        '<div class="mini-metric"><div class="val">'+Math.round((rankings[panel.id]?.totalDuration||0)/1000)+'s</div><div class="lbl">Duration</div></div>'+
        '<div class="mini-metric"><div class="val">'+rankings[panel.id]?.totalInteractions||0+'</div><div class="lbl">Clicks</div></div>'+
        '<div class="mini-metric"><div class="val">'+Math.round(computeScore(panel.id))+'</div><div class="lbl">Score</div></div>'+
      '</div>')+
    '</div>';
  el.addEventListener('click',function(e){
    if(e.target.closest('button')) return;
    recordInteraction(panel.id);
    if(el.classList.contains('compact')){
      el.classList.remove('compact');
      scheduleRearrange();
    }
  });
  el.addEventListener('dragstart',function(e){
    dragState = {panelId:panel.id,el:el};
    el.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain',panel.id);
  });
  el.addEventListener('dragend',function(e){
    el.classList.remove('dragging');
    dragState = null;
    document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));
    rebuildOrderFromDOM();
    scheduleRearrange();
    saveState();
  });
  el.addEventListener('dragover',function(e){
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if(dragState && dragState.el !== el) el.classList.add('drag-over');
  });
  el.addEventListener('dragleave',function(e){el.classList.remove('drag-over')});
  el.addEventListener('drop',function(e){
    e.preventDefault();
    el.classList.remove('drag-over');
    if(!dragState) return;
    let src = dragState.el;
    let dst = el;
    if(src===dst) return;
    let parent = dst.parentNode;
    let allPanels = [...parent.querySelectorAll('.panel:not(.collapsed)')];
    let srcIdx = allPanels.indexOf(src);
    let dstIdx = allPanels.indexOf(dst);
    if(srcIdx<0||dstIdx<0) return;
    if(srcIdx<dstIdx){
      parent.insertBefore(src,dst.nextSibling);
    }else{
      parent.insertBefore(src,dst);
    }
    rebuildOrderFromDOM();
    pinnedPanels[src.dataset.panelId] = true;
    pinnedPanels[dst.dataset.panelId] = true;
    scheduleRearrange();
    saveState();
  });
  el.querySelector('.pin-btn').addEventListener('click',function(e){
    e.stopPropagation();
    let id = panel.id;
    pinnedPanels[id] = !pinnedPanels[id];
    if(pinnedPanels[id]){
      el.classList.add('pinned');
      el.classList.remove('compact');
      el.querySelector('.pin-btn').textContent = '📌';
      el.querySelector('.pin-btn').title = 'Unpin';
    }else{
      el.classList.remove('pinned');
      el.querySelector('.pin-btn').textContent = '📍';
      el.querySelector('.pin-btn').title = 'Pin';
    }
    recordInteraction(id);
    scheduleRearrange();
    saveState();
    toast(pinnedPanels[id]?panel.title+' pinned':panel.title+' unpinned');
  });
  el.querySelector('.collapse-btn').addEventListener('click',function(e){
    e.stopPropagation();
    let id = panel.id;
    collapsedPanels[id] = !collapsedPanels[id];
    el.classList.toggle('collapsed',collapsedPanels[id]);
    recordInteraction(id);
    scheduleRearrange();
    saveState();
    toast(collapsedPanels[id]?panel.title+' collapsed':panel.title+' expanded');
  });
  return el;
}
function rebuildOrderFromDOM(){
  let container = document.getElementById('dashboard');
  let more = document.getElementById('more-panels');
  let allEls = [...container.querySelectorAll('.panel'),...more.querySelectorAll('.panel')];
  panelOrder = allEls.map(el=>el.dataset.panelId).filter(Boolean);
}
function renderPanels(incremental){
  let ranked = rankAll();
  let rankMap = {};
  ranked.forEach((r,i)=>rankMap[r.id]=i);
  let container = document.getElementById('dashboard');
  let moreContainer = document.getElementById('more-panels');
  let moreSection = document.getElementById('more-section');
  let orderedPanels = panelOrder.map(id=>panels.find(p=>p.id===id)).filter(Boolean);
  let remaining = panels.filter(p=>!orderedPanels.some(op=>op.id===p.id));
  orderedPanels.push(...remaining);
  let currentEls = {};
  container.querySelectorAll('.panel').forEach(el=>currentEls[el.dataset.panelId]=el);
  moreContainer.querySelectorAll('.panel').forEach(el=>currentEls[el.dataset.panelId]=el);
  let visiblePanels = orderedPanels.filter(p=>!collapsedPanels[p.id]);
  let mainPanels = visiblePanels.slice(0,8);
  let morePanels = visiblePanels.slice(8);
  if(incremental && Object.keys(currentEls).length>0){
    let mainSet = new Set(mainPanels.map(p=>p.id));
    let moreSet = new Set(morePanels.map(p=>p.id));
    Object.entries(currentEls).forEach(([id,el])=>{
      if(!mainSet.has(id) && !moreSet.has(id)){
        el.remove();
      }
    });
    mainPanels.forEach((p,i)=>{
      let existing = currentEls[p.id];
      if(existing){
        if(existing.parentNode !== container) container.appendChild(existing);
        let rank = rankMap[p.id]||i;
        let shouldCompact = rank>=8 && !pinnedPanels[p.id];
        if(shouldCompact && !existing.classList.contains('compact')) existing.classList.add('compact');
        if(!shouldCompact && existing.classList.contains('compact')) existing.classList.remove('compact');
        if(!existing.classList.contains('pinned') && pinnedPanels[p.id]) existing.classList.add('pinned');
        if(existing.classList.contains('pinned') && !pinnedPanels[p.id]) existing.classList.remove('pinned');
        if(collapsedPanels[p.id] && !existing.classList.contains('collapsed')) existing.classList.add('collapsed');
        if(!collapsedPanels[p.id] && existing.classList.contains('collapsed')) existing.classList.remove('collapsed');
        let badge = existing.querySelector('.rank-badge');
        if(badge) badge.textContent = '#'+(rank+1)+' · '+Math.round(rankings[p.id]?.score||50);
        let valEl = existing.querySelector('.metric-value');
        if(valEl){
          let v = mockValue(p);
          let c = alertLevel(p,v);
          valEl.style.color = c;
          valEl.innerHTML = formatValue(p,v)+'<span style="font-size:0.7rem;margin-left:4px">'+p.unit+'</span>';
        }
      }else{
        let el = buildPanelElement(p,rankMap[p.id]||i);
        container.appendChild(el);
        observePanel(el);
      }
    });
    moreContainer.innerHTML = '';
    morePanels.forEach((p,i)=>{
      let el = buildPanelElement(p,(rankMap[p.id]||8+i));
      moreContainer.appendChild(el);
      observePanel(el);
    });
  }else{
    container.innerHTML = '';
    moreContainer.innerHTML = '';
    mainPanels.forEach((p,i)=>{
      let el = buildPanelElement(p,rankMap[p.id]||i);
      container.appendChild(el);
      observePanel(el);
    });
    morePanels.forEach((p,i)=>{
      let el = buildPanelElement(p,(rankMap[p.id]||8+i));
      moreContainer.appendChild(el);
      observePanel(el);
    });
  }
  document.getElementById('more-count').textContent = morePanels.length>0?' ('+morePanels.length+')':'';
  moreSection.style.display = morePanels.length>0?'block':'none';
}
function toast(msg){
  let el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(()=>el.classList.remove('show'),2000);
}
function pollData(){
  panels.forEach(p=>{
    let v = mockValue(p);
    historyLog.push({panel:p.id,value:v,ts:Date.now()});
  });
  if(historyLog.length>HISTORY_MAX) historyLog = historyLog.slice(-HISTORY_MAX);
  renderPanels(true);
  if(autoLayout) scheduleRearrange();
}
function updateSessionTime(){
  let elapsed = Math.floor((Date.now()-sessionStart)/1000);
  let m = Math.floor(elapsed/60).toString().padStart(2,'0');
  let s = (elapsed%60).toString().padStart(2,'0');
  document.getElementById('session-time').textContent = m+':'+s;
}
document.getElementById('btn-auto').addEventListener('click',function(){
  autoLayout = !autoLayout;
  this.classList.toggle('active',autoLayout);
  this.textContent = autoLayout?'Auto':'Manual';
  if(autoLayout) rearrangeLayout();
  saveState();
  toast(autoLayout?'Auto-layout enabled':'Manual layout active');
});
document.getElementById('btn-reset').addEventListener('click',function(){
  if(!confirm('Reset all layout learning data?')) return;
  rankings = defaultRankings();
  panelOrder = panels.map(p=>p.id);
  pinnedPanels = {};
  collapsedPanels = {};
  historyLog = [];
  viewTimers = {};
  interactionCounts = {};
  localStorage.removeItem(STORAGE_KEY);
  renderPanels(false);
  setupObserver();
  document.querySelectorAll('.panel').forEach(el=>observePanel(el));
  toast('Layout learning reset');
});
document.getElementById('btn-export').addEventListener('click',function(){
  saveState();
  let data = loadState();
  let blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  let url = URL.createObjectURL(blob);
  let a = document.createElement('a');
  a.href = url;
  a.download = 'adaptive-layout-prefs.json';
  a.click();
  URL.revokeObjectURL(url);
  toast('Preferences exported');
});
document.getElementById('btn-auto').classList.toggle('active',autoLayout);
document.getElementById('btn-auto').textContent = autoLayout?'Auto':'Manual';
setupObserver();
renderPanels(false);
document.querySelectorAll('.panel').forEach(el=>observePanel(el));
setInterval(pollData,POLL_INTERVAL);
setInterval(updateSessionTime,1000);
setInterval(saveState,15000);
if(autoLayout) rearrangeLayout();
updateSessionTime();
})();
</script>
</body>
</html>