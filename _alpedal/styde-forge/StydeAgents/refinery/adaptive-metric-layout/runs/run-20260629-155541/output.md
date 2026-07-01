<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d37;--text:#e1e4eb;--muted:#8b90a0;--accent:#6c8cff;--accent-glow:rgba(108,140,255,0.15);--warn:#f0a040;--danger:#e0556a;--success:#4caf88;--radius:10px;--gap:12px;--transition:0.35s cubic-bezier(0.4,0,0.2,1)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.dashboard{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(140px,auto);gap:var(--gap);padding:var(--gap);max-width:1400px;margin:0 auto;transition:var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);position:relative;overflow:hidden;display:flex;flex-direction:column;transition:all var(--transition);cursor:grab;min-height:140px}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.6;z-index:999;transform:scale(0.97)}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important;min-height:80px;max-height:100px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-chart{display:none}
.panel.compact .panel-value{font-size:1rem!important}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent),0 0 20px var(--accent-glow)}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--border);flex-shrink:0}
.panel-title{font-size:0.8rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:0.05em}
.panel-controls{display:flex;gap:4px}
.panel-ctrl{background:none;border:none;color:var(--muted);cursor:pointer;padding:4px 6px;border-radius:4px;font-size:0.75rem;transition:all 0.15s;line-height:1}
.panel-ctrl:hover{color:var(--text);background:var(--border)}
.panel-ctrl.locked-ctrl{color:var(--accent)}
.panel-body{padding:14px;flex:1;display:flex;flex-direction:column;justify-content:center}
.panel-value{font-size:2rem;font-weight:700;line-height:1.1}
.panel-sub{font-size:0.75rem;color:var(--muted);margin-top:4px}
.panel-chart{height:60px;margin:0 14px 14px;position:relative}
.panel-trend{display:inline-flex;align-items:center;gap:4px;font-size:0.75rem;font-weight:600;margin-top:6px}
.panel-trend.up{color:var(--success)}
.panel-trend.down{color:var(--danger)}
.panel-rank-badge{position:absolute;top:8px;right:40px;font-size:0.6rem;color:var(--muted);opacity:0.6;letter-spacing:0.1em}
.panel-drag-handle{cursor:grab;color:var(--muted);font-size:0.7rem;padding:2px}
.panel-compact-toggle{font-size:0.7rem}
.toolbar{display:flex;gap:8px;padding:12px var(--gap);align-items:center;flex-wrap:wrap}
.toolbar-btn{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:all 0.15s}
.toolbar-btn:hover{background:var(--border)}
.toolbar-btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.toolbar-divider{width:1px;height:24px;background:var(--border);margin:0 4px}
.rank-1{grid-column:span 2;grid-row:span 2;min-height:300px}
.rank-2{grid-column:span 2;grid-row:span 1;min-height:180px}
.rank-3{grid-column:span 1;grid-row:span 1}
.rank-4{grid-column:span 1;grid-row:span 1}
.rank-5{grid-column:span 1;grid-row:span 1}
.panel.compact .panel-rank-badge{display:none}
.drop-zone{border:2px dashed var(--accent);background:var(--accent-glow);border-radius:var(--radius)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.score-decay{animation:pulse 2s ease-in-out infinite}
@media(max-width:900px){.dashboard{grid-template-columns:repeat(2,1fr)}.rank-1,.rank-2{grid-column:span 2}}
@media(max-width:500px){.dashboard{grid-template-columns:1fr}.rank-1,.rank-2,.rank-3,.rank-4,.rank-5{grid-column:span 1}}
</style>
</head>
<body>
<div class="toolbar">
<button class="toolbar-btn active" onclick="toggleAutoLayout(this)" title="Auto-arrange panels by attention score">Auto Layout</button>
<button class="toolbar-btn" onclick="resetAllScores()">Reset Scores</button>
<button class="toolbar-btn" onclick="compactAll()">Compact All</button>
<button class="toolbar-btn" onclick="expandAll()">Expand All</button>
<span class="toolbar-divider"></span>
<span style="font-size:0.75rem;color:var(--muted)">Hover panels to boost rank. Lock to pin position. Drag to reorder.</span>
</div>
<div class="dashboard" id="dashboard"></div>
<script>
const STORAGE_KEY='adaptive_dashboard_v2';
const DECAY_RATE=0.998;
const DECAY_INTERVAL=30000;
let panels=[
  {id:'revenue',title:'Revenue',value:'$48,294',sub:'+12.3% vs last month',trend:'up',trendVal:'+12.3%',data:[30,35,32,40,45,42,48,52,50,55,58,62,60,65,70,68,72,75,78,80,82],color:'#4caf88'},
  {id:'users',title:'Active Users',value:'2,847',sub:'Online now: 342',trend:'up',trendVal:'+5.7%',data:[200,220,210,240,250,245,260,270,265,280,290,285,300,310,305,320,315,330,325,340,342],color:'#6c8cff'},
  {id:'conversion',title:'Conversion Rate',value:'3.82%',sub:'Target: 4.0%',trend:'down',trendVal:'-0.15%',data:[4.2,4.1,4.0,3.9,3.95,4.0,3.85,3.9,3.88,3.82,3.8,3.78,3.82,3.85,3.8,3.82],color:'#f0a040'},
  {id:'cpu',title:'Server CPU',value:'67%',sub:'4 cores / 8 threads',trend:'up',trendVal:'+3%',data:[45,50,48,55,52,58,60,62,58,65,63,67,70,68,65,67],color:'#e0556a'},
  {id:'latency',title:'API Latency',value:'142ms',sub:'p99: 380ms',trend:'down',trendVal:'-8ms',data:[180,175,170,165,160,155,150,148,145,142,140,138,142],color:'#6c8cff'},
  {id:'errors',title:'Error Rate',value:'0.12%',sub:'24 errors / 20k req',trend:'down',trendVal:'-0.03%',data:[0.25,0.22,0.20,0.18,0.19,0.17,0.15,0.14,0.13,0.12],color:'#e0556a'},
  {id:'storage',title:'Storage',value:'2.1 TB',sub:'32% used of 6.4 TB',trend:'up',trendVal:'+0.3 TB',data:[1.2,1.3,1.4,1.5,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2.0,2.05,2.1],color:'#4caf88'},
  {id:'bandwidth',title:'Bandwidth',value:'840 Mbps',sub:'Peak: 1.2 Gbps',trend:'up',trendVal:'+45 Mbps',data:[600,620,640,660,680,700,720,740,760,780,800,820,840],color:'#f0a040'}
];
let state={
  scores:{},
  locks:{},
  manualOrder:null,
  compact:new Set(),
  autoLayout:true
};
function loadState(){
  try{
    let raw=localStorage.getItem(STORAGE_KEY);
    if(raw){
      let s=JSON.parse(raw);
      if(s.scores)state.scores=s.scores;
      if(s.locks)state.locks=s.locks;
      if(s.compact)state.compact=new Set(s.compact);
      if(s.manualOrder!==undefined)state.manualOrder=s.manualOrder;
      if(s.autoLayout!==undefined)state.autoLayout=s.autoLayout;
    }
  }catch(e){}
  panels.forEach(p=>{
    if(!(p.id in state.scores))state.scores[p.id]=100;
    if(!(p.id in state.locks))state.locks[p.id]=false;
  });
}
function saveState(){
  let raw={
    scores:state.scores,
    locks:state.locks,
    compact:[...state.compact],
    manualOrder:state.manualOrder,
    autoLayout:state.autoLayout
  };
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(raw));}catch(e){}
}
function rankPanels(){
  return [...panels].sort((a,b)=>(state.scores[b.id]||0)-(state.scores[a.id]||0));
}
function getRankClass(idx){
  if(idx===0)return'rank-1';
  if(idx===1)return'rank-2';
  if(idx<4)return'rank-3';
  return'rank-4';
}
function renderSparkline(data,color,w,h){
  if(!data||data.length<2)return'';
  let min=Math.min(...data),max=Math.max(...data);
  let range=max-min||1;
  let points=data.map((v,i)=>{
    let x=(i/(data.length-1))*w;
    let y=h-((v-min)/range)*h;
    return`${x},${y}`;
  });
  let areaPoints=points[0]+' '+points.map(p=>p.replace(',',' ')).join(' ')+` ${w},${h} 0,${h}`;
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="display:block">
    <defs><linearGradient id="grad-${color}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${color}" stop-opacity="0.25"/><stop offset="100%" stop-color="${color}" stop-opacity="0.02"/></linearGradient></defs>
    <polygon points="${areaPoints}" fill="url(#grad-${color})"/>
    <polyline points="${points.join(' ')}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}
function buildPanel(panel,rank){
  let isCompact=state.compact.has(panel.id);
  let isLocked=state.locks[panel.id];
  let score=state.scores[panel.id]||0;
  let rankLabel=rank+1;
  let rankClass=isCompact?'compact':getRankClass(rank);
  let lockClass=isLocked?'locked':'';
  let showChart=!isCompact&&panel.data&&panel.data.length>1;
  return `<div class="panel ${rankClass} ${lockClass}" data-id="${panel.id}" draggable="true"
    onmouseenter="trackHover('${panel.id}')"
    onclick="trackClick('${panel.id}')"
    ondragstart="handleDragStart(event,'${panel.id}')"
    ondragover="handleDragOver(event)"
    ondragleave="handleDragLeave(event)"
    ondrop="handleDrop(event,'${panel.id}')"
    ondragend="handleDragEnd(event)">
    <div class="panel-rank-badge">${'#'+rankLabel} | ${Math.round(score)}</div>
    <div class="panel-header">
      <span class="panel-title">${panel.title}</span>
      <div class="panel-controls">
        <button class="panel-ctrl panel-compact-toggle" onclick="event.stopPropagation();toggleCompact('${panel.id}')" title="Toggle compact">${isCompact?'&boxbox;':'&minus;'}</button>
        <button class="panel-ctrl locked-ctrl" onclick="event.stopPropagation();toggleLock('${panel.id}')" title="${isLocked?'Unlock':'Lock'} position">${isLocked?'&#x1f512;':'&#x1f513;'}</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">${panel.value}</div>
      <div class="panel-sub">${panel.sub}</div>
      ${panel.trend?`<div class="panel-trend ${panel.trend}">${panel.trend==='up'?'&#x25B2;':'&#x25BC;'} ${panel.trendVal}</div>`:''}
    </div>
    ${showChart?`<div class="panel-chart">${renderSparkline(panel.data,panel.color,parseInt(panel.style?.width||'280'),60)}</div>`:''}
  </div>`;
}
function buildDashboard(){
  let container=document.getElementById('dashboard');
  let ordered;
  if(state.autoLayout){
    ordered=rankPanels();
    state.manualOrder=null;
  }else if(state.manualOrder){
    ordered=state.manualOrder.map(id=>panels.find(p=>p.id===id)).filter(Boolean);
    let remaining=panels.filter(p=>!state.manualOrder.includes(p.id));
    ordered=[...ordered,...remaining];
  }else{
    ordered=[...panels];
  }
  container.innerHTML=ordered.map((p,i)=>buildPanel(p,i)).join('');
}
let hoverTimers={};
function trackHover(panelId){
  if(hoverTimers[panelId])return;
  hoverTimers[panelId]=Date.now();
}
function trackClick(panelId){
  state.scores[panelId]=(state.scores[panelId]||0)+15;
  saveState();
  maybeRerender();
}
document.addEventListener('mouseleave',function(e){
  for(let id in hoverTimers){
    let duration=(Date.now()-hoverTimers[id])/1000;
    let boost=Math.min(duration*5,50);
    state.scores[id]=(state.scores[id]||0)+boost;
    delete hoverTimers[id];
  }
  saveState();
  maybeRerender();
},true);
function toggleCompact(id){
  if(state.compact.has(id))state.compact.delete(id);
  else state.compact.add(id);
  state.scores[id]=(state.scores[id]||0)+5;
  saveState();
  buildDashboard();
}
function toggleLock(id){
  state.locks[id]=!state.locks[id];
  state.scores[id]=(state.scores[id]||0)+10;
  if(state.locks[id]&&state.autoLayout){
    state.manualOrder=rankPanels().map(p=>p.id);
    state.autoLayout=false;
    document.querySelector('.toolbar-btn.active')?.classList.remove('active');
  }
  saveState();
  buildDashboard();
}
let dragSrcId=null;
function handleDragStart(e,panelId){
  dragSrcId=panelId;
  e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed='move';
}
function handleDragOver(e){
  e.preventDefault();
  e.dataTransfer.dropEffect='move';
  let panel=e.target.closest('.panel');
  if(panel)panel.classList.add('drop-zone');
}
function handleDragLeave(e){
  let panel=e.target.closest('.panel');
  if(panel)panel.classList.remove('drop-zone');
}
function handleDrop(e, targetId){
  e.preventDefault();
  document.querySelectorAll('.drop-zone').forEach(el=>el.classList.remove('drop-zone'));
  if(!dragSrcId||dragSrcId===targetId)return;
  let ordered=rankPanels().map(p=>p.id);
  let srcIdx=ordered.indexOf(dragSrcId);
  let tgtIdx=ordered.indexOf(targetId);
  if(srcIdx>=0&&tgtIdx>=0){
    ordered.splice(srcIdx,1);
    ordered.splice(tgtIdx,0,dragSrcId);
  }
  state.manualOrder=ordered;
  state.autoLayout=false;
  state.scores[dragSrcId]=(state.scores[dragSrcId]||0)+20;
  state.scores[targetId]=(state.scores[targetId]||0)+20;
  document.querySelector('.toolbar-btn.active')?.classList.remove('active');
  saveState();
  buildDashboard();
  dragSrcId=null;
}
function handleDragEnd(e){
  e.target.classList.remove('dragging');
  document.querySelectorAll('.drop-zone').forEach(el=>el.classList.remove('drop-zone'));
  dragSrcId=null;
}
function toggleAutoLayout(btn){
  state.autoLayout=!state.autoLayout;
  if(state.autoLayout){
    state.manualOrder=null;
    btn.classList.add('active');
  }else{
    state.manualOrder=rankPanels().map(p=>p.id);
    btn.classList.remove('active');
  }
  saveState();
  buildDashboard();
}
function resetAllScores(){
  panels.forEach(p=>state.scores[p.id]=100);
  state.locks={};
  state.compact.clear();
  state.manualOrder=null;
  state.autoLayout=true;
  let btn=document.querySelector('.toolbar-btn');
  if(btn)btn.classList.add('active');
  saveState();
  buildDashboard();
}
function compactAll(){
  panels.forEach(p=>state.compact.add(p.id));
  state.autoLayout=false;
  state.manualOrder=panels.map(p=>p.id);
  let btn=document.querySelector('.toolbar-btn.active');
  if(btn)btn.classList.remove('active');
  saveState();
  buildDashboard();
}
function expandAll(){
  state.compact.clear();
  saveState();
  buildDashboard();
}
setInterval(()=>{
  let changed=false;
  for(let id in state.scores){
    if(state.locks[id])continue;
    let old=state.scores[id];
    state.scores[id]=Math.max(10,state.scores[id]*DECAY_RATE);
    if(Math.abs(state.scores[id]-old)>0.5)changed=true;
  }
  if(changed){
    saveState();
    maybeRerender();
  }
},DECAY_INTERVAL);
let rerenderPending=false;
function maybeRerender(){
  if(rerenderPending)return;
  rerenderPending=true;
  requestAnimationFrame(()=>{
    if(state.autoLayout)buildDashboard();
    rerenderPending=false;
  });
}
loadState();
buildDashboard();
</script>
</body>
</html>