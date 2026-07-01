```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22263a;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-muted: #8b8fa8;
  --accent: #7c6ff7;
  --accent-glow: rgba(124,111,247,0.25);
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #f87171;
  --info: #60a5fa;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  padding:16px;
  line-height:1.5;
}
.header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:12px;
  margin-bottom:var(--gap);
  padding:0 4px;
}
.header h1{font-size:1.5rem;font-weight:600;letter-spacing:-0.02em;}
.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.btn{
  background:var(--surface);
  color:var(--text);
  border:1px solid var(--border);
  padding:8px 16px;
  border-radius:8px;
  cursor:pointer;
  font-size:0.875rem;
  transition:background var(--transition),border-color var(--transition);
  display:inline-flex;align-items:center;gap:6px;
  white-space:nowrap;
}
.btn:hover{background:var(--surface-hover);border-color:var(--accent)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn:active{transform:scale(0.97)}
.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.accent:hover{box-shadow:0 0 20px var(--accent-glow)}
.btn.danger{color:var(--danger);border-color:var(--danger)}
.btn-sm{padding:5px 10px;font-size:0.75rem}
.dashboard{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:var(--gap);
  align-items:start;
}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  overflow:hidden;
  transition:transform var(--transition),box-shadow var(--transition),grid-column var(--transition),grid-row var(--transition),border-color var(--transition);
  position:relative;
  will-change:transform,grid-column,grid-row;
  contain:layout style;
}
.panel:focus-within{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow)}
.panel:hover:not(.dragging){border-color:var(--info)}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 1;grid-row:span 1}
.panel.compact{grid-column:span 1;grid-row:span 1}
.panel.compact .panel-body{max-height:80px;overflow:hidden;opacity:0.7}
.panel.compact .panel-body>*:not(.compact-preview){display:none}
.panel.compact .compact-preview{display:flex!important}
.panel.compact:hover{opacity:1}
.panel.locked{border-left:3px solid var(--warning)}
.panel.dragging{z-index:100;box-shadow:0 20px 60px rgba(0,0,0,0.5);transform:scale(1.03);opacity:0.95}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow);background:var(--surface-hover)}
.panel-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:10px 14px;
  border-bottom:1px solid var(--border);
  cursor:grab;
  user-select:none;
  gap:8px;
  background:linear-gradient(180deg,rgba(255,255,255,0.02) 0%,transparent 100%);
}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:0.9rem;display:flex;align-items:center;gap:8px;flex:1;min-width:0}
.panel-header .title .icon{font-size:1.1rem;flex-shrink:0}
.panel-header .title .label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-header .actions{display:flex;gap:4px;flex-shrink:0}
.panel-header .pill{
  font-size:0.65rem;
  padding:2px 8px;
  border-radius:20px;
  font-weight:600;
  text-transform:uppercase;
  letter-spacing:0.05em;
  flex-shrink:0;
}
.pill.locked{background:rgba(251,191,36,0.15);color:var(--warning)}
.pill.auto{background:rgba(96,165,250,0.15);color:var(--info)}
.pill.compact-badge{background:rgba(139,143,168,0.15);color:var(--text-muted)}
.rank-badge{
  position:absolute;
  top:8px;right:8px;
  font-size:0.6rem;
  padding:1px 6px;
  border-radius:10px;
  background:var(--accent);
  color:#fff;
  font-weight:700;
  opacity:0.6;
  z-index:1;
}
.icon-btn{
  background:none;border:none;color:var(--text-muted);cursor:pointer;
  padding:4px 6px;border-radius:6px;font-size:0.85rem;
  transition:color var(--transition),background var(--transition);
  display:inline-flex;align-items:center;justify-content:center;
}
.icon-btn:hover{color:var(--text);background:rgba(255,255,255,0.05)}
.icon-btn:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.icon-btn[aria-pressed="true"]{color:var(--warning)}
.panel-body{padding:14px;transition:max-height var(--transition)}
.compact-preview{display:none;align-items:center;gap:8px;color:var(--text-muted);font-size:0.8rem}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:10px}
.metric-item{text-align:center}
.metric-value{font-size:1.6rem;font-weight:700;letter-spacing:-0.03em}
.metric-label{font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em}
.metric-trend{font-size:0.7rem;margin-top:2px}
.trend-up{color:var(--success)}.trend-down{color:var(--danger)}.trend-stable{color:var(--text-muted)}
.sparkline{width:100%;height:40px;margin-top:8px}
.sparkline svg{width:100%;height:100%}
.stat-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.03);font-size:0.82rem}
.stat-row:last-child{border-bottom:none}
.stat-key{color:var(--text-muted)}.stat-val{font-weight:500}
.usage-bar{height:4px;background:var(--border);border-radius:3px;margin-top:6px;overflow:hidden}
.usage-fill{height:100%;border-radius:3px;transition:width 0.6s ease}
.usage-fill.low{background:var(--success)}
.usage-fill.mid{background:var(--warning)}
.usage-fill.high{background:var(--danger)}
.empty-state{text-align:center;padding:40px 20px;color:var(--text-muted)}
.empty-state .empty-icon{font-size:2.5rem;margin-bottom:12px;opacity:0.4}
.error-boundary{background:rgba(248,113,113,0.08);border:1px solid var(--danger);border-radius:var(--radius);padding:20px;text-align:center;color:var(--danger)}
.error-boundary .retry-btn{margin-top:12px}
.loading-shimmer{background:linear-gradient(90deg,var(--surface) 25%,var(--surface-hover) 50%,var(--surface) 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:8px;height:60px}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.layout-warning{
  background:rgba(251,191,36,0.1);
  border:1px solid var(--warning);
  border-radius:var(--radius);
  padding:10px 16px;
  margin-bottom:var(--gap);
  font-size:0.82rem;
  display:flex;align-items:center;gap:8px;
  color:var(--warning);
}
.layout-warning[hidden]{display:none}
@media(max-width:1024px){.dashboard{grid-template-columns:repeat(2,1fr)}.panel.large{grid-column:span 2;grid-row:span 1}}
@media(max-width:600px){.dashboard{grid-template-columns:1fr}.panel.large,.panel.medium,.panel.compact{grid-column:span 1;grid-row:span 1}body{padding:8px}.header h1{font-size:1.2rem}}
:focus:not(:focus-visible){outline:none}
</style>
</head>
<body>
<header class="header" role="banner">
  <h1 id="dash-title">Adaptive Metric Dashboard</h1>
  <div class="controls">
    <button class="btn btn-sm" id="btn-reset" aria-label="Reset all tracking data and layout">
      <span aria-hidden="true">↺</span> Reset Data
    </button>
    <button class="btn btn-sm" id="btn-unlock-all" aria-label="Unlock all panels">
      <span aria-hidden="true">🔓</span> Unlock All
    </button>
    <button class="btn btn-sm" id="btn-compact-all" aria-label="Set all panels to compact mode">
      <span aria-hidden="true">⊟</span> Compact All
    </button>
    <button class="btn btn-sm accent" id="btn-expand-all" aria-label="Expand all panels">
      <span aria-hidden="true">⊞</span> Expand All
    </button>
    <span style="font-size:0.75rem;color:var(--text-muted);white-space:nowrap">
      Panels: <span id="panel-count">8</span> &middot; Auto: <span id="auto-count">8</span>
    </span>
  </div>
</header>
<div id="layout-warning" class="layout-warning" hidden role="alert">
  <span aria-hidden="true">⚠</span>
  <span id="layout-warning-text"></span>
</div>
<main class="dashboard" id="dashboard" role="main" aria-label="Adaptive metric dashboard grid" aria-describedby="dash-title">
</main>
<script>
'use strict';
const STORAGE_KEY = 'adaptive_dash_v1';
const MAX_PANELS = 12;
const DECAY_LAMBDA = 0.05;
const COMPACT_RANK_THRESHOLD = 6;
const LARGE_RANK_THRESHOLD = 3;
const VIEW_TRACK_INTERVAL = 2000;
const RESIZE_DEBOUNCE = 150;
const SAVE_DEBOUNCE = 300;
const PANEL_DEFS = [
  {id:'cpu',title:'CPU Usage',icon:'⚙',metrics:[
    {label:'Current',valueKey:'cpu'},{label:'Avg 1m',valueKey:'cpuAvg'},
    {label:'Peak',valueKey:'cpuPeak'},{label:'Cores',valueKey:'cpuCores'}
  ]},
  {id:'memory',title:'Memory',icon:'🧠',metrics:[
    {label:'Used',valueKey:'mem'},{label:'Total',valueKey:'memTotal'},
    {label:'Cache',valueKey:'memCache'},{label:'Swap',valueKey:'memSwap'}
  ]},
  {id:'disk',title:'Disk I/O',icon:'💾',metrics:[
    {label:'Read',valueKey:'diskRead'},{label:'Write',valueKey:'diskWrite'},
    {label:'IOPS',valueKey:'diskIops'},{label:'Queue',valueKey:'diskQueue'}
  ]},
  {id:'network',title:'Network',icon:'🌐',metrics:[
    {label:'In',valueKey:'netIn'},{label:'Out',valueKey:'netOut'},
    {label:'Pkts/s',valueKey:'netPps'},{label:'Err',valueKey:'netErr'}
  ]},
  {id:'users',title:'Active Users',icon:'👥',metrics:[
    {label:'Online',valueKey:'usersOnline'},{label:'7d Avg',valueKey:'usersAvg'},
    {label:'New',valueKey:'usersNew'},{label:'Bounce',valueKey:'usersBounce'}
  ]},
  {id:'errors',title:'Error Rate',icon:'🚨',metrics:[
    {label:'5xx',valueKey:'err5xx'},{label:'4xx',valueKey:'err4xx'},
    {label:'Timeout',valueKey:'errTimeout'},{label:'Total',valueKey:'errTotal'}
  ]},
  {id:'throughput',title:'Throughput',icon:'⚡',metrics:[
    {label:'RPS',valueKey:'tputRps'},{label:'Lat p50',valueKey:'tputP50'},
    {label:'Lat p99',valueKey:'tputP99'},{label:'BW',valueKey:'tputBw'}
  ]},
  {id:'latency',title:'Latency Heatmap',icon:'🔥',metrics:[
    {label:'p50',valueKey:'latP50'},{label:'p90',valueKey:'latP90'},
    {label:'p99',valueKey:'latP99'},{label:'Max',valueKey:'latMax'}
  ]}
];
function seedRandom(seed){let s=seed;return()=>{s=(s*1664525+1013904223)&0xffffffff;return(s>>>0)/0xffffffff}}
const rng=seedRandom(42);
function generateMetrics(base){
  const set={};
  for(const d of PANEL_DEFS){
    for(const m of d.metrics){
      let b=base[m.valueKey]||rng()*100;
      b=Math.max(0,Math.min(99.9,b+(rng()-0.5)*8));
      set[m.valueKey]=Math.round(b*10)/10;
    }
  }
  return set;
}
let simMetrics=generateMetrics({
  cpu:35,cpuAvg:28,cpuPeak:72,cpuCores:16,
  mem:62,memTotal:128,memCache:18,memSwap:4,
  diskRead:340,diskWrite:210,diskIops:1200,diskQueue:2.1,
  netIn:850,netOut:420,netPps:3400,netErr:3,
  usersOnline:1240,usersAvg:980,usersNew:47,usersBounce:22,
  err5xx:12,err4xx:89,errTimeout:5,errTotal:106,
  tputRps:2400,tputP50:12,tputP99:145,tputBw:960,
  latP50:8,latP90:34,latP99:145,latMax:890
});
setInterval(()=>{simMetrics=generateMetrics(simMetrics);updateAllMetrics()},3000);
function makeBehaviorStore(){
  let bh={};
  try{
    const raw=localStorage.getItem(STORAGE_KEY+'_bh');
    if(raw) bh=JSON.parse(raw);
  }catch(e){bh={}}
  return new Proxy(bh,{
    set(t,k,v){t[k]=v;debouncedSaveBehavior(t);return true},
    deleteProperty(t,k){delete t[k];debouncedSaveBehavior(t);return true}
  });
}
function makeLayoutStore(){
  let ls={order:[],locks:{},compactOverrides:{}};
  try{
    const raw=localStorage.getItem(STORAGE_KEY+'_layout');
    if(raw) ls=JSON.parse(raw);
  }catch(e){}
  return new Proxy(ls,{
    set(t,k,v){t[k]=v;debouncedSaveLayout(t);return true}
  });
}
let behaviorStore=makeBehaviorStore();
let layoutStore=makeLayoutStore();
function ensureBehavior(panelId){
  if(!behaviorStore[panelId]){
    behaviorStore[panelId]={
      viewCount:0,totalViewDuration:0,lastViewed:null,
      interactionCount:0,expandCount:0,collapseCount:0
    };
  }
  return behaviorStore[panelId];
}
function recordView(panelId,duration){
  const b=ensureBehavior(panelId);
  b.viewCount=(b.viewCount||0)+1;
  b.totalViewDuration=(b.totalViewDuration||0)+duration;
  b.lastViewed=Date.now();
  behaviorStore[panelId]=b;
}
function recordInteraction(panelId){
  const b=ensureBehavior(panelId);
  b.interactionCount=(b.interactionCount||0)+1;
  b.lastViewed=Date.now();
  behaviorStore[panelId]=b;
}
function recordToggle(panelId,expanded){
  const b=ensureBehavior(panelId);
  if(expanded){b.expandCount=(b.expandCount||0)+1}
  else{b.collapseCount=(b.collapseCount||0)+1}
  b.lastViewed=Date.now();
  behaviorStore[panelId]=b;
}
function calcCompositeScore(panelId){
  const b=behaviorStore[panelId];
  if(!b)return 0;
  const f=b.interactionCount||0;
  const v=b.viewCount||0;
  const d=Math.min((b.totalViewDuration||0)/1000,3600);
  const hoursSinceLast=b.lastViewed?(Date.now()-b.lastViewed)/(1000*60*60):72;
  const recency=Math.exp(-DECAY_LAMBDA*hoursSinceLast);
  return (f*4+v*2+d*0.5)*recency;
}
function rankPanels(panelIds){
  return panelIds.map(id=>({id,score:calcCompositeScore(id)}))
    .sort((a,b)=>b.score-a.score);
}
let saveTimeout=null;
function debouncedSaveBehavior(data){clearTimeout(saveTimeout);saveTimeout=setTimeout(()=>{try{localStorage.setItem(STORAGE_KEY+'_bh',JSON.stringify(data))}catch(e){showWarning('Failed to save tracking data: '+e.message)}},SAVE_DEBOUNCE)}
function debouncedSaveLayout(data){clearTimeout(saveTimeout);saveTimeout=setTimeout(()=>{try{localStorage.setItem(STORAGE_KEY+'_layout',JSON.stringify(data))}catch(e){showWarning('Failed to save layout: '+e.message)}},SAVE_DEBOUNCE)}
function showWarning(msg){const w=document.getElementById('layout-warning');const t=document.getElementById('layout-warning-text');t.textContent=msg;w.hidden=false;setTimeout(()=>{w.hidden=true},4000)}
let resizeTimer=null;
let rafPending=false;
const observers=new Map();
const visibilityTimers=new Map();
function applyLayout(){
  if(rafPending)return;
  rafPending=true;
  requestAnimationFrame(()=>{
    rafPending=false;
    _applyLayoutNow();
  });
}
function _applyLayoutNow(){
  const dashboard=document.getElementById('dashboard');
  const panels=[...dashboard.querySelectorAll('.panel')];
  const panelIds=panels.map(p=>p.dataset.panelId).filter(Boolean);
  const ranked=rankPanels(panelIds);
  const lockOrder=[];
  const autoOrder=[];
  for(const r of ranked){
    if(layoutStore.locks[r.id]){lockOrder.push(r.id)}
    else{autoOrder.push({id:r.id,score:r.score})}
  }
  lockOrder.sort((a,b)=>{
    const ia=layoutStore.order.indexOf(a);
    const ib=layoutStore.order.indexOf(b);
    return (ia>=0?ia:999)-(ib>=0?ib:999);
  });
  autoOrder.sort((a,b)=>b.score-a.score);
  const finalOrder=[...lockOrder,...autoOrder.map(a=>a.id)];
  layoutStore.order=finalOrder;
  const container=document.getElementById('dashboard');
  const existing={};
  for(const p of panels){existing[p.dataset.panelId]=p}
  for(let i=0;i<finalOrder.length;i++){
    const pid=finalOrder[i];
    const el=existing[pid];
    if(!el)continue;
    removePanelClasses(el);
    const locked=!!layoutStore.locks[pid];
    const overrideCompact=layoutStore.compactOverrides[pid];
    if(overrideCompact===false){addClass(el,'medium')}
    else if(overrideCompact===true||(!locked&&i>=COMPACT_RANK_THRESHOLD)){addClass(el,'compact')}
    else if(!locked&&i<LARGE_RANK_THRESHOLD){addClass(el,'large')}
    else{addClass(el,'medium')}
    if(locked)el.classList.add('locked');
    updatePanelBadges(el,pid,i,locked);
  }
  for(let i=0;i<finalOrder.length;i++){
    const pid=finalOrder[i];
    const el=existing[pid];
    if(!el)continue;
    if(el.parentNode===container){container.appendChild(el)}
    el.style.order=i;
  }
  document.getElementById('panel-count').textContent=finalOrder.length;
  document.getElementById('auto-count').textContent=finalOrder.filter(id=>!layoutStore.locks[id]).length;
}
function removePanelClasses(el){el.classList.remove('large','medium','compact','locked')}
function addClass(el,cls){el.classList.add(cls)}
function updatePanelBadges(el,pid,rank,locked){
  let badge=el.querySelector('.rank-badge');
  if(!badge){badge=document.createElement('span');badge.className='rank-badge';el.appendChild(badge)}
  badge.textContent='#'+(rank+1)+' · '+(calcCompositeScore(pid).toFixed(1));
  badge.title='Composite score: '+calcCompositeScore(pid).toFixed(2)+' | '+
    'Views: '+(behaviorStore[pid]?.viewCount||0)+
    ' | Interactions: '+(behaviorStore[pid]?.interactionCount||0)+
    ' | Duration: '+Math.round((behaviorStore[pid]?.totalViewDuration||0)/1000)+'s';
  const lockEl=el.querySelector('.lock-btn');
  if(lockEl)lockEl.setAttribute('aria-pressed',locked?'true':'false');
  const pill=el.querySelector('.panel-header .pill');
  if(pill){
    if(locked){pill.textContent='LOCKED';pill.className='pill locked'}
    else if(el.classList.contains('compact')){pill.textContent='COMPACT';pill.className='pill compact-badge'}
    else{pill.textContent='AUTO';pill.className='pill auto'}
  }
}
function buildPanel(def){
  const el=document.createElement('div');
  el.className='panel';
  el.dataset.panelId=def.id;
  el.setAttribute('role','region');
  el.setAttribute('aria-label',def.title+' panel');
  el.tabIndex=0;
  el.addEventListener('keydown',e=>{
    if(e.key==='Escape'&&el.classList.contains('compact')){
      e.preventDefault();
      toggleCompact(def.id);
    }
  });
  el.innerHTML='<div class="panel-header" draggable="true" aria-grabbed="false">'+
    '<span class="title"><span class="icon" aria-hidden="true">'+def.icon+'</span><span class="label">'+def.title+'</span></span>'+
    '<span class="pill auto">AUTO</span>'+
    '<div class="actions">'+
      '<button class="icon-btn compact-btn" aria-label="Toggle compact mode for '+def.title+'" title="Toggle compact (Esc)">⊟</button>'+
      '<button class="icon-btn lock-btn" aria-label="Lock '+def.title+' position" title="Lock position" aria-pressed="false">🔒</button>'+
    '</div>'+
  '</div>'+
  '<div class="panel-body">'+
    '<div class="compact-preview">'+
      '<span class="icon" aria-hidden="true">'+def.icon+'</span>'+
      '<span>'+def.title+' — click to expand</span>'+
    '</div>'+
    '<div class="metric-grid">'+def.metrics.map(m=>
      '<div class="metric-item">'+
        '<div class="metric-value" data-metric="'+m.valueKey+'">—</div>'+
        '<div class="metric-label">'+m.label+'</div>'+
        '<div class="metric-trend" data-trend="'+m.valueKey+'"></div>'+
      '</div>'
    ).join('')+'</div>'+
    '<div class="usage-bar"><div class="usage-fill low" data-usage="'+def.id+'" style="width:0%"></div></div>'+
  '</div>';
  const header=el.querySelector('.panel-header');
  const lockBtn=el.querySelector('.lock-btn');
  const compactBtn=el.querySelector('.compact-btn');
  const body=el.querySelector('.panel-body');
  header.addEventListener('dragstart',e=>handleDragStart(e,def.id));
  header.addEventListener('dragend',e=>handleDragEnd(e,def.id));
  header.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='move'});
  header.addEventListener('drop',e=>handleDrop(e,def.id));
  el.addEventListener('dragenter',e=>{e.preventDefault();el.classList.add('drag-over')});
  el.addEventListener('dragleave',()=>el.classList.remove('drag-over'));
  el.addEventListener('dragover',e=>e.preventDefault());
  el.addEventListener('drop',e=>{e.preventDefault();el.classList.remove('drag-over');handleDrop(e,def.id)});
  lockBtn.addEventListener('click',e=>{e.stopPropagation();toggleLock(def.id)});
  compactBtn.addEventListener('click',e=>{e.stopPropagation();toggleCompact(def.id)});
  el.addEventListener('click',()=>recordInteraction(def.id));
  body.addEventListener('click',()=>{
    if(el.classList.contains('compact')) toggleCompact(def.id);
    recordInteraction(def.id);
  });
  observePanel(def.id,el);
  return el;
}
function handleDragStart(e,panelId){
  const el=document.querySelector('[data-panel-id="'+panelId+'"]');
  if(!el)return;
  el.classList.add('dragging');
  e.dataTransfer.effectAllowed='move';
  e.dataTransfer.setData('text/plain',panelId);
  const header=el.querySelector('.panel-header');
  if(header)header.setAttribute('aria-grabbed','true');
}
function handleDragEnd(e,panelId){
  const el=document.querySelector('[data-panel-id="'+panelId+'"]');
  if(!el)return;
  el.classList.remove('dragging');
  const header=el.querySelector('.panel-header');
  if(header)header.setAttribute('aria-grabbed','false');
  document.querySelectorAll('.drag-over').forEach(p=>p.classList.remove('drag-over'));
}
function handleDrop(e,targetId){
  e.preventDefault();
  const draggedId=e.dataTransfer.getData('text/plain');
  if(!draggedId||draggedId===targetId)return;
  const order=[...layoutStore.order];
  const dragIdx=order.indexOf(draggedId);
  const targetIdx=order.indexOf(targetId);
  if(dragIdx<0||targetIdx<0)return;
  order.splice(dragIdx,1);
  order.splice(targetIdx,0,draggedId);
  layoutStore.order=order;
  rebuildGrid();
}
function observePanel(panelId,el){
  if(observers.has(panelId)) observers.get(panelId).disconnect();
  let visible=false;
  let visibleSince=null;
  const observer=new IntersectionObserver(entries=>{
    const entry=entries[0];
    const wasVisible=visible;
    visible=entry.isIntersecting;
    if(visible&&!wasVisible){
      visibleSince=Date.now();
      visibilityTimers.set(panelId,setInterval(()=>{
        if(visibleSince)recordView(panelId,VIEW_TRACK_INTERVAL);
      },VIEW_TRACK_INTERVAL));
    }else if(!visible&&wasVisible&&visibleSince){
      const duration=Date.now()-visibleSince;
      recordView(panelId,duration);
      visibleSince=null;
      const timer=visibilityTimers.get(panelId);
      if(timer){clearInterval(timer);visibilityTimers.delete(panelId)}
    }
  },{threshold:0.3});
  observer.observe(el);
  observers.set(panelId,observer);
}
function toggleLock(panelId){
  layoutStore.locks[panelId]=!layoutStore.locks[panelId];
  recordInteraction(panelId);
  applyLayout();
}
function toggleCompact(panelId){
  const current=layoutStore.compactOverrides[panelId];
  layoutStore.compactOverrides[panelId]=current===true?false:true;
  recordToggle(panelId,layoutStore.compactOverrides[panelId]!==true);
  applyLayout();
}
function updateAllMetrics(){
  const dashboard=document.getElementById('dashboard');
  for(const def of PANEL_DEFS){
    const panel=dashboard.querySelector('[data-panel-id="'+def.id+'"]');
    if(!panel)continue;
    for(const m of def.metrics){
      const el=panel.querySelector('[data-metric="'+m.valueKey+'"]');
      const trendEl=panel.querySelector('[data-trend="'+m.valueKey+'"]');
      if(el){
        const v=simMetrics[m.valueKey];
        el.textContent=v!=null?formatMetric(v):'—';
      }
      if(trendEl){
        const v=simMetrics[m.valueKey];
        if(v!=null)updateTrend(trendEl,v,m.valueKey);
      }
    }
    const bar=panel.querySelector('[data-usage="'+def.id+'"]');
    if(bar){
      const usage=calcPanelUsage(def.id);
      bar.style.width=usage+'%';
      bar.className='usage-fill '+(usage>70?'high':usage>40?'mid':'low');
    }
  }
}
let lastMetrics={};
function updateTrend(el,current,key){
  const prev=lastMetrics[key];
  lastMetrics[key]=current;
  if(prev==null){el.textContent='';el.className='metric-trend';return}
  const diff=current-prev;
  if(Math.abs(diff)<0.3){el.textContent='→ stable';el.className='metric-trend trend-stable'}
  else if(diff>0){el.textContent='↑ +'+diff.toFixed(1);el.className='metric-trend trend-up'}
  else{el.textContent='↓ '+diff.toFixed(1);el.className='metric-trend trend-down'}
}
function formatMetric(v){
  if(v>=1000)return (v/1000).toFixed(1)+'k';
  if(v>=100)return Math.round(v).toString();
  return v.toFixed(1);
}
function calcPanelUsage(panelId){
  const b=behaviorStore[panelId];
  if(!b||!b.totalViewDuration)return 5+Math.random()*15;
  const rank=rankPanels(PANEL_DEFS.map(d=>d.id));
  const idx=rank.findIndex(r=>r.id===panelId);
  if(idx<0)return 5;
  return Math.min(95,Math.max(10,90-idx*12+rng()*8));
}
function rebuildGrid(){
  const dashboard=document.getElementById('dashboard');
  const existingEls={};
  for(const child of [...dashboard.children]){
    const pid=child.dataset.panelId;
    if(pid)existingEls[pid]=child;
  }
  const ids=PANEL_DEFS.map(d=>d.id).filter(id=>existingEls[id]);
  const ranked=rankPanels(ids);
  const lockOrder=[];
  const autoOrder=[];
  for(const r of ranked){
    if(layoutStore.locks[r.id])lockOrder.push(r.id);
    else autoOrder.push({id:r.id,score:r.score});
  }
  lockOrder.sort((a,b)=>{
    const ia=layoutStore.order.indexOf(a);
    const ib=layoutStore.order.indexOf(b);
    return (ia>=0?ia:999)-(ib>=0?ib:999);
  });
  autoOrder.sort((a,b)=>b.score-a.score);
  const finalOrder=[...lockOrder,...autoOrder.map(a=>a.id)];
  layoutStore.order=finalOrder;
  const frag=document.createDocumentFragment();
  for(const id of finalOrder){
    if(existingEls[id])frag.appendChild(existingEls[id]);
  }
  dashboard.appendChild(frag);
  applyLayout();
}
function initDashboard(){
  const dashboard=document.getElementById('dashboard');
  dashboard.innerHTML='';
  const frag=document.createDocumentFragment();
  for(const def of PANEL_DEFS){
    frag.appendChild(buildPanel(def));
  }
  dashboard.appendChild(frag);
  ensureAllBehavior();
  rebuildGrid();
  updateAllMetrics();
}
function ensureAllBehavior(){
  for(const def of PANEL_DEFS){
    if(!behaviorStore[def.id]){
      behaviorStore[def.id]={
        viewCount:Math.floor(rng()*50),
        totalViewDuration:Math.floor(rng()*3600*1000),
        lastViewed:Date.now()-Math.floor(rng()*24*3600*1000),
        interactionCount:Math.floor(rng()*30),
        expandCount:Math.floor(rng()*10),
        collapseCount:Math.floor(rng()*5)
      };
    }
  }
}
function resetAll(){
  try{localStorage.removeItem(STORAGE_KEY+'_bh');localStorage.removeItem(STORAGE_KEY+'_layout')}catch(e){}
  behaviorStore=makeBehaviorStore();
  layoutStore=makeLayoutStore();
  for(const o of observers.values())o.disconnect();
  observers.clear();
  for(const t of visibilityTimers.values())clearInterval(t);
  visibilityTimers.clear();
  initDashboard();
  showWarning('All tracking data and layout preferences reset.');
}
function unlockAll(){
  for(const def of PANEL_DEFS){layoutStore.locks[def.id]=false}
  applyLayout();
}
function compactAll(){
  for(const def of PANEL_DEFS){layoutStore.compactOverrides[def.id]=true}
  applyLayout();
}
function expandAll(){
  for(const def of PANEL_DEFS){layoutStore.compactOverrides[def.id]=false}
  applyLayout();
}
function handleResize(){
  clearTimeout(resizeTimer);
  resizeTimer=setTimeout(()=>{applyLayout()},RESIZE_DEBOUNCE);
}
function teardown(){
  window.removeEventListener('resize',handleResize);
  for(const o of observers.values())o.disconnect();
  observers.clear();
  for(const t of visibilityTimers.values())clearInterval(t);
  visibilityTimers.clear();
  clearTimeout(saveTimeout);
  clearTimeout(resizeTimer);
  rafPending=false;
}
window.addEventListener('resize',handleResize,{passive:true});
window.addEventListener('beforeunload',teardown);
document.getElementById('btn-reset').addEventListener('click',resetAll);
document.getElementById('btn-unlock-all').addEventListener('click',unlockAll);
document.getElementById('btn-compact-all').addEventListener('click',compactAll);
document.getElementById('btn-expand-all').addEventListener('click',expandAll);
document.addEventListener('keydown',e=>{
  if(e.key==='l'&&e.ctrlKey&&!e.shiftKey&&!e.altKey){
    e.preventDefault();
    const focused=document.activeElement;
    if(focused&&focused.closest&&focused.closest('.panel')){
      const panel=focused.closest('.panel');
      const pid=panel.dataset.panelId;
      if(pid)toggleLock(pid);
    }
  }
});
try{initDashboard()}catch(e){
  const dashboard=document.getElementById('dashboard');
  dashboard.innerHTML='<div class="error-boundary" role="alert"><strong>Initialization Error</strong><br>'+e.message+'<br><button class="btn btn-sm retry-btn" onclick="location.reload()">Retry</button></div>';
}
</script>
</body>
</html>
```