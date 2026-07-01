```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d37;--text:#e1e4ed;--text-dim:#8b8fa3;--accent:#6c8cff;--accent-glow:rgba(108,140,255,0.18);--hero-min-h:260px;--std-min-h:160px;--compact-min-h:72px;--gap:10px;--radius:10px;--transition:0.35s cubic-bezier(0.22,0.61,0.36,1)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px;-webkit-font-smoothing:antialiased}
.dashboard{max-width:1400px;margin:0 auto}
.header{display:flex;align-items:center;gap:14px;margin-bottom:18px;flex-wrap:wrap}
.header h1{font-size:1.3rem;font-weight:600;letter-spacing:-0.3px;color:var(--text)}
.badge{font-size:0.72rem;padding:3px 9px;border-radius:20px;background:var(--surface);border:1px solid var(--border);color:var(--text-dim)}
.btn{padding:7px 15px;border-radius:7px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:0.8rem;font-family:inherit;transition:all 0.18s;touch-action:manipulation;user-select:none}
.btn:hover{background:#252836;border-color:var(--accent);color:#fff}
.btn:active{transform:scale(0.96)}
.btn--reset{background:transparent;border-color:#3a2040;color:#c08497}
.btn--reset:hover{background:#2a1a2a;border-color:#c08497}
.grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:auto;gap:var(--gap);transition:grid-template-columns var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);position:relative;display:flex;flex-direction:column;contain:layout style;cursor:default;touch-action:manipulation}
.panel:hover{border-color:#3a3f55}
.panel--hero{grid-column:span 2;grid-row:span 2;min-height:var(--hero-min-h)}
.panel--standard{grid-column:span 1;grid-row:span 1;min-height:var(--std-min-h)}
.panel--compact{grid-column:span 1;grid-row:span 1;min-height:var(--compact-min-h)}
.panel--locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent-glow)}
.panel--overridden{border-style:dashed;border-color:#6c8cff88}
.panel-head{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--border);flex-shrink:0;min-height:40px}
.panel-head__title{font-size:0.78rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;letter-spacing:-0.2px}
.panel-head__controls{display:flex;gap:4px;flex-shrink:0}
.icon-btn{width:26px;height:26px;border-radius:5px;border:1px solid transparent;background:transparent;color:var(--text-dim);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:0.75rem;transition:all 0.18s;touch-action:manipulation;padding:0;font-family:inherit}
.icon-btn:hover{background:#252836;color:#fff;border-color:var(--border)}
.icon-btn--active{color:var(--accent);border-color:var(--accent);background:var(--accent-glow)}
.panel-body{padding:12px 14px;flex:1;display:flex;flex-direction:column;gap:6px;overflow:hidden;min-height:0}
.panel-body canvas{width:100%;height:100%;min-height:40px}
.metric-row{display:flex;align-items:baseline;gap:8px}
.metric-value{font-size:1.5rem;font-weight:700;letter-spacing:-0.5px;font-variant-numeric:tabular-nums}
.metric-unit{font-size:0.72rem;color:var(--text-dim)}
.metric-label{font-size:0.7rem;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px}
.metric-sub{font-size:0.7rem;color:var(--text-dim)}
.drawer{border-top:1px solid var(--border);margin-top:14px;padding-top:10px}
.drawer__toggle{background:transparent;border:none;color:var(--text-dim);cursor:pointer;font-size:0.76rem;padding:6px 0;font-family:inherit;display:flex;align-items:center;gap:6px;touch-action:manipulation}
.drawer__toggle:hover{color:var(--text)}
.drawer__content{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gap);margin-top:8px}
.rank-badge{font-size:0.62rem;padding:2px 7px;border-radius:10px;background:#1e2130;color:var(--text-dim);font-weight:500}
.tooltip{position:fixed;pointer-events:none;background:#1a1d27;border:1px solid var(--border);border-radius:6px;padding:5px 9px;font-size:0.72rem;color:var(--text-dim);z-index:100;opacity:0;transition:opacity 0.12s;white-space:nowrap}
.ghost{opacity:0.35;filter:grayscale(0.6)}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.panel--hero{grid-column:span 2;grid-row:span 1}.drawer__content{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.grid{grid-template-columns:1fr}.panel--hero,.panel--standard,.panel--compact{grid-column:span 1;grid-row:span 1}.drawer__content{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="dashboard">
  <div class="header">
    <h1>Adaptive Dashboard</h1>
    <span class="badge" id="session-badge">session: --</span>
    <span class="badge" id="score-badge">score decay active</span>
    <button class="btn btn--reset" id="reset-btn" title="Reset all tracking data and layout">Reset Layout</button>
    <span style="font-size:0.7rem;color:var(--text-dim);margin-left:auto" id="info-text">Observing behavior...</span>
  </div>
  <div class="grid" id="grid-container"></div>
  <div class="drawer" id="drawer" hidden>
    <button class="drawer__toggle" id="drawer-toggle">▸ Show hidden panels</button>
    <div class="drawer__content" id="drawer-content" hidden></div>
  </div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
const CLEANUP_REGISTRY = new Set();
function registerCleanup(fn){CLEANUP_REGISTRY.add(fn);return ()=>{fn();CLEANUP_REGISTRY.delete(fn);};}
function runAllCleanups(){for(const fn of CLEANUP_REGISTRY){try{fn();}catch(e){/* silent */}CLEANUP_REGISTRY.delete(fn);}}
const STORAGE_KEY = 'adaptive_dashboard_v2';
const DECAY_HALF_HOURS = 2;
const METRIC_WINDOW = 60;
const METRIC_INTERVAL_MS = 2000;
const PERSIST_DEBOUNCE_MS = 800;
const PANEL_DEFS = [
  {id:'cpu', title:'CPU Usage', unit:'%', type:'sparkline', color:'#6c8cff', defaultTier:'hero'},
  {id:'memory', title:'Memory', unit:'MB', type:'sparkline', color:'#5eeadb', defaultTier:'hero'},
  {id:'requests', title:'Request Rate', unit:'req/s', type:'sparkline', color:'#f0c060', defaultTier:'hero'},
  {id:'latency', title:'Latency P95', unit:'ms', type:'sparkline', color:'#ff7665', defaultTier:'standard'},
  {id:'errors', title:'Error Rate', unit:'err/min', type:'count', color:'#ff5e7a', defaultTier:'standard'},
  {id:'network', title:'Network I/O', unit:'KB/s', type:'sparkline', color:'#a78bfa', defaultTier:'standard'},
  {id:'sessions', title:'Active Sessions', unit:'', type:'count', color:'#4ade80', defaultTier:'compact'},
  {id:'disk', title:'Disk I/O', unit:'IOPS', type:'sparkline', color:'#f78ca0', defaultTier:'compact'}
];
let state = {
  panels: {},
  overrides: {},
  history: {},
  sessionStart: Date.now(),
  relayoutScheduled: false,
  relayoutGeneration: 0,
  drawerOpen: false
};
PANEL_DEFS.forEach(d=>{
  state.panels[d.id]={
    id:d.id, title:d.title, unit:d.unit, type:d.type, color:d.color,
    tier:'standard', locked:false, manualPos:null,
    data:[], currentValue:0,
    score:0, frequency:0, durationMs:0, lastInteraction:0,
    visible:false, visibleSince:0
  };
  state.history[d.id]=[];
  state.overrides[d.id]=null;
});
function loadState(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    if(!raw)return;
    const saved=JSON.parse(raw);
    if(Date.now()-saved.ts>86400000)return;
    for(const[id,data]of Object.entries(saved.panels||{})){
      if(state.panels[id]){
        state.panels[id].score=data.score||0;
        state.panels[id].frequency=data.frequency||0;
        state.panels[id].durationMs=data.durationMs||0;
        state.panels[id].lastInteraction=data.lastInteraction||0;
        state.panels[id].tier=data.tier||'standard';
        state.panels[id].locked=data.locked||false;
        state.panels[id].manualPos=data.manualPos||null;
      }
    }
    if(saved.overrides)state.overrides=saved.overrides;
  }catch(e){/* corrupt, start fresh */}
}
function persistState(){
  const payload={ts:Date.now(),panels:{},overrides:state.overrides};
  for(const[id,p]of Object.entries(state.panels)){
    payload.panels[id]={score:p.score,frequency:p.frequency,durationMs:p.durationMs,lastInteraction:p.lastInteraction,tier:p.tier,locked:p.locked,manualPos:p.manualPos};
  }
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(payload));}catch(e){/* quota, ignore */}
}
let persistTimer=null;
function schedulePersist(){
  if(persistTimer)clearTimeout(persistTimer);
  persistTimer=setTimeout(()=>{persistState();persistTimer=null;},PERSIST_DEBOUNCE_MS);
}
registerCleanup(()=>{if(persistTimer)clearTimeout(persistTimer);persistState();});
function collectMetrics(){
  const now=Date.now();
  for(const[id,p]of Object.entries(state.panels)){
    let raw;
    switch(id){
      case 'cpu':{
        const t=performance.now();
        raw=30+25*Math.sin(t*0.0007)+12*Math.sin(t*0.0023)+6*Math.sin(t*0.0051)+Math.random()*4;
        raw=Math.max(2,Math.min(98,raw));
        break;
      }
      case 'memory':{
        if(performance.memory&&performance.memory.usedJSHeapSize){
          raw=performance.memory.usedJSHeapSize/(1024*1024);
        }else{
          raw=80+15*Math.sin(now*0.0001)+Math.random()*5;
        }
        raw=Math.max(10,raw);
        break;
      }
      case 'requests':{
        raw=120+40*Math.sin(now*0.0004)+20*Math.sin(now*0.0017)+Math.random()*8;
        raw=Math.max(0,raw);
        break;
      }
      case 'latency':{
        raw=45+25*Math.abs(Math.sin(now*0.0006))+10*Math.random();
        raw=Math.max(5,Math.min(300,raw));
        break;
      }
      case 'errors':{
        raw=Math.max(0,2+3*Math.abs(Math.sin(now*0.0009))+Math.random()*1.5);
        break;
      }
      case 'network':{
        raw=500+200*Math.sin(now*0.0003)+150*Math.sin(now*0.0011)+Math.random()*30;
        raw=Math.max(10,raw);
        break;
      }
      case 'sessions':{
        raw=42+8*Math.sin(now*0.00025)+Math.random()*3;
        raw=Math.max(1,Math.round(raw));
        break;
      }
      case 'disk':{
        raw=220+80*Math.sin(now*0.0005)+60*Math.sin(now*0.0019)+Math.random()*15;
        raw=Math.max(5,raw);
        break;
      }
      default:raw=0;
    }
    p.currentValue=typeof raw==='number'?Math.round(raw*10)/10:raw;
    p.data.push({ts:now,value:p.currentValue});
    if(p.data.length>METRIC_WINDOW)p.data.shift();
  }
}
function computeScores(){
  const now=Date.now();
  for(const[id,p]of Object.entries(state.panels)){
    const recencyHours=(now-p.lastInteraction)/(3600000);
    const recencyFactor=1/(1+recencyHours/DECAY_HALF_HOURS);
    const durationSec=p.durationMs/1000;
    p.score=p.frequency*durationSec*recencyFactor;
  }
}
function rankPanels(){
  const entries=Object.entries(state.panels).map(([id,p])=>({id,score:p.score||0,locked:p.locked,manualPos:p.manualPos}));
  const locked=entries.filter(e=>e.locked&&e.manualPos!=null);
  const unlocked=entries.filter(e=>!e.locked||e.manualPos==null);
  unlocked.sort((a,b)=>b.score-a.score);
  const ranked=[...locked,...unlocked];
  const tiers={hero:[],standard:[],compact:[],hidden:[]};
  const total=ranked.length;
  ranked.forEach((e,i)=>{
    const percentile=i/total;
    if(e.locked&&e.manualPos!=null){
      tiers.hero.push(e.id);
    }else if(percentile<0.375){
      tiers.hero.push(e.id);
    }else if(percentile<0.75){
      tiers.standard.push(e.id);
    }else if(percentile<0.925){
      tiers.compact.push(e.id);
    }else{
      tiers.hidden.push(e.id);
    }
  });
  for(const[id,p]of Object.entries(state.panels)){
    if(tiers.hero.includes(id))p.tier='hero';
    else if(tiers.standard.includes(id))p.tier='standard';
    else if(tiers.compact.includes(id))p.tier='compact';
    else p.tier='hidden';
  }
  return tiers;
}
let lastLayout=null;
let lastDrawerVisible=null;
function computeDesiredLayout(){
  const tiers=rankPanels();
  const order=[...tiers.hero,...tiers.standard,...tiers.compact];
  return {order,tiers,hidden:tiers.hidden};
}
function applyLayoutDiff(desired){
  const grid=document.getElementById('grid-container');
  const drawerContent=document.getElementById('drawer-content');
  const drawer=document.getElementById('drawer');
  if(!lastLayout){
    renderAll(desired,grid,drawerContent,drawer);
    lastLayout=desired;
    lastDrawerVisible=desired.hidden.length>0;
    return;
  }
  const prevOrder=lastLayout.order||[];
  const newOrder=desired.order||[];
  const prevHidden=new Set(lastLayout.hidden||[]);
  const newHidden=new Set(desired.hidden||[]);
  let changed=false;
  for(let i=0;i<Math.max(prevOrder.length,newOrder.length);i++){
    if(prevOrder[i]!==newOrder[i]){changed=true;break;}
  }
  if(!changed&&prevHidden.size===newHidden.size&&[...prevHidden].every(id=>newHidden.has(id))){
    lastLayout=desired;
    lastDrawerVisible=desired.hidden.length>0;
    return;
  }
  const allIds=new Set([...prevOrder,...newOrder,...prevHidden,...newHidden]);
  const panelEls={};
  for(const id of allIds){
    panelEls[id]=document.querySelector(`.panel[data-panel-id="${id}"]`);
  }
  const visibleNow=[];
  for(const id of newOrder){
    if(newHidden.has(id))continue;
    const el=panelEls[id];
    if(!el)continue;
    const desiredTier=desired.tiers.hero.includes(id)?'hero':desired.tiers.standard.includes(id)?'standard':'compact';
    const prevTier=lastLayout.tiers.hero.includes(id)?'hero':lastLayout.tiers.standard.includes(id)?'standard':lastLayout.tiers.compact.includes(id)?'compact':'hidden';
    if(prevTier!==desiredTier){
      updatePanelTier(el,id,desiredTier);
    }
    const p=state.panels[id];
    if(p&&p.locked&&!el.classList.contains('panel--locked'))el.classList.add('panel--locked');
    if(p&&!p.locked&&el.classList.contains('panel--locked'))el.classList.remove('panel--locked');
    if(p&&p.manualPos!=null&&!el.classList.contains('panel--overridden'))el.classList.add('panel--overridden');
    if(p&&p.manualPos==null&&el.classList.contains('panel--overridden'))el.classList.remove('panel--overridden');
    visibleNow.push(el);
  }
  const hiddenEls=[];
  for(const id of newHidden){
    const el=panelEls[id];
    if(el){
      updatePanelTier(el,id,'hidden');
      hiddenEls.push(el);
    }
  }
  for(const id of prevHidden){
    if(!newHidden.has(id)){
      const el=panelEls[id];
      if(el){
        const desiredTier=desired.tiers.hero.includes(id)?'hero':desired.tiers.standard.includes(id)?'standard':'compact';
        updatePanelTier(el,id,desiredTier);
        visibleNow.push(el);
      }
    }
  }
  grid.innerHTML='';
  for(const el of visibleNow){grid.appendChild(el);}
  if(hiddenEls.length>0){
    drawerContent.innerHTML='';
    for(const el of hiddenEls){drawerContent.appendChild(el);}
    drawer.hidden=false;
  }else{
    drawer.hidden=true;
  }
  lastLayout=desired;
  lastDrawerVisible=hiddenEls.length>0;
}
function renderAll(desired,grid,drawerContent,drawer){
  grid.innerHTML='';
  drawerContent.innerHTML='';
  const hiddenSet=new Set(desired.hidden||[]);
  for(const id of desired.order||[]){
    if(hiddenSet.has(id))continue;
    const el=createPanelElement(id);
    grid.appendChild(el);
  }
  if(desired.hidden&&desired.hidden.length>0){
    for(const id of desired.hidden){
      const el=createPanelElement(id);
      drawerContent.appendChild(el);
    }
    drawer.hidden=false;
  }else{
    drawer.hidden=true;
  }
}
function updatePanelTier(el,id,tier){
  el.classList.remove('panel--hero','panel--standard','panel--compact');
  if(tier==='hero')el.classList.add('panel--hero');
  else if(tier==='standard')el.classList.add('panel--standard');
  else if(tier==='compact')el.classList.add('panel--compact');
  state.panels[id].tier=tier;
  refreshPanelContent(el,id,tier);
}
function createPanelElement(id){
  const p=state.panels[id];
  const el=document.createElement('div');
  el.className='panel';
  el.setAttribute('data-panel-id',id);
  if(p.tier==='hero')el.classList.add('panel--hero');
  else if(p.tier==='standard')el.classList.add('panel--standard');
  else el.classList.add('panel--compact');
  if(p.locked)el.classList.add('panel--locked');
  if(p.manualPos!=null)el.classList.add('panel--overridden');
  el.innerHTML='<div class="panel-head"><span class="panel-head__title">'+escapeHTML(p.title)+'</span><span class="rank-badge" data-rank-badge>--</span><div class="panel-head__controls"><button class="icon-btn lock-btn" title="Lock position" data-action="lock">🔒</button><button class="icon-btn override-btn" title="Manual override" data-action="override">📍</button></div></div><div class="panel-body"><canvas data-canvas></canvas><div class="metric-row"><span class="metric-value" data-value>--</span><span class="metric-unit">'+escapeHTML(p.unit)+'</span></div></div>';
  return el;
}
function escapeHTML(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function refreshPanelContent(el,id,tier){
  const p=state.panels[id];
  const valueEl=el.querySelector('[data-value]');
  if(valueEl)valueEl.textContent=typeof p.currentValue==='number'?p.currentValue.toFixed(1):String(p.currentValue);
  const badge=el.querySelector('[data-rank-badge]');
  if(badge)badge.textContent='score:'+(p.score?p.score.toFixed(0):'0');
  const canvas=el.querySelector('[data-canvas]');
  if(canvas&&p.type==='sparkline'){
    drawSparkline(canvas,p.data,p.color,tier);
  }
  const lockBtn=el.querySelector('[data-action="lock"]');
  if(lockBtn){
    lockBtn.classList.toggle('icon-btn--active',p.locked);
    lockBtn.textContent=p.locked?'🔓':'🔒';
  }
}
function drawSparkline(canvas,data,color,tier){
  const dpr=window.devicePixelRatio||1;
  const rect=canvas.parentElement.getBoundingClientRect();
  const w=rect.width-28;
  const h=tier==='compact'?Math.min(40,rect.height-20):Math.min(100,rect.height-30);
  if(w<=0||h<=0)return;
  canvas.width=w*dpr;
  canvas.height=h*dpr;
  canvas.style.width=w+'px';
  canvas.style.height=h+'px';
  const ctx=canvas.getContext('2d');
  ctx.scale(dpr,dpr);
  ctx.clearRect(0,0,w,h);
  if(data.length<2)return;
  const values=data.map(d=>d.value);
  const min=Math.min(...values);
  const max=Math.max(...values);
  const range=max-min||1;
  const px=i=>(w/(data.length-1))*i;
  const py=v=>h-((v-min)/range)*(h-4)-2;
  ctx.beginPath();
  ctx.moveTo(px(0),py(values[0]));
  for(let i=1;i<values.length;i++)ctx.lineTo(px(i),py(values[i]));
  ctx.strokeStyle=color;
  ctx.lineWidth=1.6;
  ctx.lineJoin='round';
  ctx.lineCap='round';
  ctx.stroke();
  const grad=ctx.createLinearGradient(0,0,0,h);
  grad.addColorStop(0,color+'44');
  grad.addColorStop(1,color+'08');
  ctx.lineTo(px(values.length-1),h);
  ctx.lineTo(px(0),h);
  ctx.closePath();
  ctx.fillStyle=grad;
  ctx.fill();
}
function refreshAllPanels(){
  const desired=computeDesiredLayout();
  applyLayoutDiff(desired);
  const allEls=document.querySelectorAll('.panel[data-panel-id]');
  allEls.forEach(el=>{
    const id=el.getAttribute('data-panel-id');
    const p=state.panels[id];
    if(!p)return;
    const valueEl=el.querySelector('[data-value]');
    if(valueEl)valueEl.textContent=typeof p.currentValue==='number'?p.currentValue.toFixed(1):String(p.currentValue);
    const badge=el.querySelector('[data-rank-badge]');
    if(badge)badge.textContent='score:'+(p.score?p.score.toFixed(0):'0');
    const canvas=el.querySelector('[data-canvas]');
    if(canvas&&p.type==='sparkline')drawSparkline(canvas,p.data,p.color,p.tier);
  });
}
function scheduleRelayout(){
  if(state.relayoutScheduled)return;
  state.relayoutScheduled=true;
  state.relayoutGeneration++;
  const gen=state.relayoutGeneration;
  requestAnimationFrame(()=>{
    if(gen!==state.relayoutGeneration)return;
    state.relayoutScheduled=false;
    computeScores();
    refreshAllPanels();
    schedulePersist();
  });
}
const observer=new IntersectionObserver((entries)=>{
  const now=Date.now();
  for(const entry of entries){
    const id=entry.target.getAttribute('data-panel-id');
    if(!id||!state.panels[id])continue;
    const p=state.panels[id];
    if(entry.isIntersecting&&!p.visible){
      p.visible=true;
      p.visibleSince=now;
    }else if(!entry.isIntersecting&&p.visible){
      p.visible=false;
      if(p.visibleSince>0){
        p.durationMs+=now-p.visibleSince;
        p.visibleSince=0;
      }
      scheduleRelayout();
    }
  }
},{threshold:0.3});
registerCleanup(()=>observer.disconnect());
function observePanel(el){
  observer.observe(el);
}
function handlePointerEnter(e){
  const panel=findPanel(e.target);
  if(!panel)return;
  const id=panel.getAttribute('data-panel-id');
  if(!id||!state.panels[id])return;
  const p=state.panels[id];
  const now=Date.now();
  if(!p.visible&&p.visibleSince>0){
    p.durationMs+=now-p.visibleSince;
    p.visibleSince=0;
  }
}
function handlePointerLeave(e){
  const panel=findPanel(e.target);
  if(!panel)return;
  const id=panel.getAttribute('data-panel-id');
  if(!id||!state.panels[id])return;
  const p=state.panels[id];
  const now=Date.now();
  if(p.visible){
    if(p.visibleSince>0){
      p.durationMs+=now-p.visibleSince;
    }
    p.visibleSince=now;
  }
}
function handleClick(e){
  const panel=findPanel(e.target);
  if(!panel)return;
  const id=panel.getAttribute('data-panel-id');
  if(!id||!state.panels[id])return;
  const p=state.panels[id];
  p.frequency++;
  p.lastInteraction=Date.now();
  scheduleRelayout();
  const actionBtn=e.target.closest('[data-action]');
  if(actionBtn){
    const action=actionBtn.getAttribute('data-action');
    if(action==='lock')toggleLock(id);
    else if(action==='override')toggleOverride(id);
  }
}
function toggleLock(id){
  const p=state.panels[id];
  p.locked=!p.locked;
  if(!p.locked)p.manualPos=null;
  p.lastInteraction=Date.now();
  p.frequency++;
  schedulePersist();
  scheduleRelayout();
}
function toggleOverride(id){
  const p=state.panels[id];
  if(p.manualPos!=null){
    p.manualPos=null;
    p.locked=false;
  }else{
    p.manualPos={x:0,y:0,timestamp:Date.now()};
    p.locked=true;
  }
  p.lastInteraction=Date.now();
  p.frequency++;
  schedulePersist();
  scheduleRelayout();
}
function findPanel(el){
  while(el){
    if(el.classList&&el.classList.contains('panel'))return el;
    el=el.parentElement;
  }
  return null;
}
const gridContainer=document.getElementById('grid-container');
gridContainer.addEventListener('pointerenter',handlePointerEnter,{passive:true});
gridContainer.addEventListener('pointerleave',handlePointerLeave,{passive:true});
gridContainer.addEventListener('click',handleClick);
registerCleanup(()=>{
  gridContainer.removeEventListener('pointerenter',handlePointerEnter);
  gridContainer.removeEventListener('pointerleave',handlePointerLeave);
  gridContainer.removeEventListener('click',handleClick);
});
const drawerToggle=document.getElementById('drawer-toggle');
drawerToggle.addEventListener('click',()=>{
  state.drawerOpen=!state.drawerOpen;
  const content=document.getElementById('drawer-content');
  content.hidden=!state.drawerOpen;
  drawerToggle.textContent=state.drawerOpen?'▾ Hide hidden panels':'▸ Show hidden panels ('+(lastLayout?lastLayout.hidden.length:0)+')';
});
registerCleanup(()=>drawerToggle.removeEventListener('click',()=>{}));
document.getElementById('reset-btn').addEventListener('click',()=>{
  for(const[id,p]of Object.entries(state.panels)){
    p.score=0;p.frequency=0;p.durationMs=0;p.lastInteraction=0;
    p.tier=PANEL_DEFS.find(d=>d.id===id)?.defaultTier||'standard';
    p.locked=false;p.manualPos=null;
  }
  state.overrides={};
  lastLayout=null;
  lastDrawerVisible=null;
  try{localStorage.removeItem(STORAGE_KEY);}catch(e){}
  refreshAllPanels();
  document.getElementById('info-text').textContent='Layout reset. Observing fresh behavior...';
});
let metricTimer=null;
function startMetricLoop(){
  collectMetrics();
  metricTimer=setInterval(()=>{
    collectMetrics();
    const allEls=document.querySelectorAll('.panel[data-panel-id]');
    allEls.forEach(el=>{
      const id=el.getAttribute('data-panel-id');
      const p=state.panels[id];
      if(!p)return;
      const valueEl=el.querySelector('[data-value]');
      if(valueEl)valueEl.textContent=typeof p.currentValue==='number'?p.currentValue.toFixed(1):String(p.currentValue);
      const canvas=el.querySelector('[data-canvas]');
      if(canvas&&p.type==='sparkline')drawSparkline(canvas,p.data,p.color,p.tier);
    });
  },METRIC_INTERVAL_MS);
}
registerCleanup(()=>{if(metricTimer)clearInterval(metricTimer);});
const resizeObserver=new ResizeObserver(()=>{
  const allEls=document.querySelectorAll('.panel[data-panel-id]');
  allEls.forEach(el=>{
    const id=el.getAttribute('data-panel-id');
    const p=state.panels[id];
    if(!p)return;
    const canvas=el.querySelector('[data-canvas]');
    if(canvas&&p.type==='sparkline')drawSparkline(canvas,p.data,p.color,p.tier);
  });
});
resizeObserver.observe(gridContainer);
registerCleanup(()=>resizeObserver.disconnect());
document.getElementById('session-badge').textContent='session: '+new Date(state.sessionStart).toLocaleTimeString();
let decayTimer=setInterval(()=>{
  const now=Date.now();
  let anyDecayed=false;
  for(const[id,p]of Object.entries(state.panels)){
    const hours=(now-p.lastInteraction)/(3600000);
    if(hours>DECAY_HALF_HOURS*2&&p.score>0.01){
      anyDecayed=true;
    }
  }
  if(anyDecayed)scheduleRelayout();
},30000);
registerCleanup(()=>clearInterval(decayTimer));
loadState();
startMetricLoop();
requestAnimationFrame(()=>{
  computeScores();
  refreshAllPanels();
});
const mutationObserver=new MutationObserver((mutations)=>{
  for(const mut of mutations){
    for(const node of mut.addedNodes){
      if(node.nodeType===1&&node.classList&&node.classList.contains('panel')){
        observePanel(node);
        const id=node.getAttribute('data-panel-id');
        if(id&&state.panels[id]){
          refreshPanelContent(node,id,state.panels[id].tier);
        }
      }
    }
  }
});
mutationObserver.observe(gridContainer,{childList:true,subtree:true});
registerCleanup(()=>mutationObserver.disconnect());
window.addEventListener('beforeunload',()=>{
  runAllCleanups();
  persistState();
});
document.getElementById('info-text').textContent='Tracking active. Interact with panels to train the layout.';
})();
</script>
</body>
</html>
```