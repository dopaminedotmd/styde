<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0b0f19;--surface:#131a2b;--surface2:#1a2338;--border:#25304a;
  --text:#e2e8f0;--text2:#94a3b8;--text3:#64748b;
  --accent:#38bdf8;--green:#34d399;--yellow:#fbbf24;--red:#f87171;
  --purple:#a78bfa;--orange:#fb923c;--pink:#f472b6;
  --radius:10px;--radius-sm:6px;--gap:12px;
  --transition:0.35s cubic-bezier(0.4,0,0.2,1);
  --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
  --header-h:52px;--drawer-h:44px;
}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
header{
  position:sticky;top:0;z-index:100;height:var(--header-h);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;background:var(--surface);border-bottom:1px solid var(--border);
  backdrop-filter:blur(12px);
}
header h1{font-size:15px;font-weight:600;letter-spacing:-0.01em;color:var(--text)}
.header-actions{display:flex;gap:8px;align-items:center}
.btn{
  padding:6px 14px;border-radius:var(--radius-sm);border:1px solid var(--border);
  background:var(--surface2);color:var(--text2);cursor:pointer;
  font-size:12px;font-weight:500;transition:all var(--transition);
  white-space:nowrap;font-family:var(--font);
}
.btn:hover{background:var(--border);color:var(--text)}
.btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
.score-badge{
  font-size:11px;padding:4px 10px;border-radius:20px;border:1px solid var(--border);
  background:var(--surface2);color:var(--text3);font-variant-numeric:tabular-nums;
}
.score-badge.heat-0{border-color:#1e3a5f;color:#60a5fa}
.score-badge.heat-1{border-color:#1e4a2f;color:#4ade80}
.score-badge.heat-2{border-color:#4a3a1e;color:#facc15}
.score-badge.heat-3{border-color:#3a1e1e;color:#f87171}
main{padding:16px 20px 80px;max-width:1600px;margin:0 auto}
.dashboard-grid{
  display:grid;grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(140px,auto);gap:var(--gap);
}
@media(max-width:1200px){.dashboard-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:768px){.dashboard-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.dashboard-grid{grid-template-columns:1fr}}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:16px;position:relative;overflow:hidden;
  transition:all var(--transition);cursor:default;
  display:flex;flex-direction:column;min-height:140px;
}
.panel:hover{border-color:#33415c}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.compact{min-height:90px;padding:10px 14px;flex-direction:row;align-items:center;gap:12px}
.panel.compact .panel-body{flex-direction:row;align-items:center;gap:12px;flex:1}
.panel.compact .panel-value{font-size:22px}
.panel.compact .panel-chart{display:none}
.panel.compact .panel-label{font-size:11px}
.panel.locked{border-color:var(--yellow);box-shadow:0 0 0 1px var(--yellow)}
.panel.locked::after{
  content:'LOCKED';position:absolute;top:6px;right:36px;
  font-size:9px;font-weight:700;color:var(--yellow);letter-spacing:0.08em;
  opacity:0.7;
}
.panel.moved{animation:flash-move 0.6s ease}
@keyframes flash-move{0%{box-shadow:0 0 0 2px var(--accent)}100%{box-shadow:0 0 0 0 transparent}}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;min-height:20px}
.panel-title{font-size:13px;font-weight:600;color:var(--text2);letter-spacing:-0.01em;text-transform:uppercase}
.panel-actions{display:flex;gap:2px;align-items:center;opacity:0;transition:opacity 0.2s}
.panel:hover .panel-actions{opacity:1}
.panel-actions button{
  background:none;border:none;color:var(--text3);cursor:pointer;
  padding:2px 4px;border-radius:4px;font-size:13px;line-height:1;
  transition:all 0.15s;
}
.panel-actions button:hover{color:var(--text);background:var(--surface2)}
.panel-actions button.locked-btn{color:var(--yellow)}
.panel-body{display:flex;flex-direction:column;flex:1;justify-content:center}
.panel-value{font-size:36px;font-weight:700;line-height:1.1;letter-spacing:-0.02em;font-variant-numeric:tabular-nums}
.panel-unit{font-size:13px;font-weight:400;color:var(--text3);margin-left:4px}
.panel-label{font-size:12px;color:var(--text3);margin-top:4px}
.panel-chart{margin-top:auto;height:40px;display:flex;align-items:flex-end;gap:2px;padding-top:8px}
.panel-chart .bar{flex:1;border-radius:2px 2px 0 0;min-width:3px;transition:height 0.4s ease;opacity:0.7}
.panel-trend{font-size:12px;font-weight:500;display:flex;align-items:center;gap:3px}
.panel-trend.up{color:var(--green)}.panel-trend.down{color:var(--red)}.panel-trend.neutral{color:var(--text3)}
.panel-footer{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:6px}
.rank-indicator{
  position:absolute;top:10px;right:10px;font-size:9px;font-weight:700;
  color:var(--text3);opacity:0.6;letter-spacing:0.04em;
}
.heat-border{position:absolute;top:0;left:0;right:0;height:3px;border-radius:var(--radius) var(--radius) 0 0;transition:all var(--transition)}
.drawer-section{margin-top:20px}
.drawer-toggle{
  width:100%;padding:10px;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);color:var(--text2);cursor:pointer;
  font-size:12px;font-weight:500;text-align:center;transition:all 0.2s;
  font-family:var(--font);display:flex;align-items:center;justify-content:center;gap:6px;
}
.drawer-toggle:hover{background:var(--surface2)}
.drawer-count{font-size:10px;padding:2px 8px;border-radius:10px;background:var(--surface2);color:var(--text3)}
.drawer-panels{
  display:none;grid-template-columns:repeat(6,1fr);gap:var(--gap);
  margin-top:var(--gap);padding:12px;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);
}
.drawer-panels.open{display:grid}
.drawer-panels .panel.compact{grid-column:span 1}
@media(max-width:1200px){.drawer-panels{grid-template-columns:repeat(3,1fr)}}
@media(max-width:768px){.drawer-panels{grid-template-columns:repeat(2,1fr)}}
.override-modal{
  display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);
  z-index:200;align-items:center;justify-content:center;
}
.override-modal.open{display:flex}
.override-content{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:24px;min-width:320px;max-width:400px;
}
.override-content h3{font-size:16px;font-weight:600;margin-bottom:16px;color:var(--text)}
.override-content label{display:block;font-size:12px;color:var(--text2);margin-bottom:6px}
.override-content input[type=number]{
  width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:var(--radius-sm);
  background:var(--surface2);color:var(--text);font-size:14px;margin-bottom:12px;
  font-family:var(--font);
}
.override-content .btn-row{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}
.tracking-debug{
  position:fixed;bottom:10px;right:10px;padding:8px 12px;background:rgba(0,0,0,0.8);
  border:1px solid var(--border);border-radius:var(--radius-sm);font-size:10px;
  color:var(--text3);z-index:150;display:none;max-width:300px;font-family:monospace;
}
.tracking-debug.visible{display:block}
.toast{
  position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
  padding:10px 20px;background:var(--accent);color:#000;border-radius:var(--radius);
  font-size:13px;font-weight:600;z-index:300;opacity:0;transition:all 0.3s;
  pointer-events:none;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(-6px)}
.skeleton{background:linear-gradient(90deg,var(--surface2) 25%,var(--border) 50%,var(--surface2) 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:var(--radius-sm)}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
.empty-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:var(--text3);font-size:12px;gap:8px}
</style>
</head>
<body>
<header>
<h1>Adaptive Layout</h1>
<div class="header-actions">
<span class="score-badge" id="global-score" title="Average panel engagement score">-- pts</span>
<button class="btn" id="btn-recalc" title="Force layout recalculation">Recalc</button>
<button class="btn" id="btn-reset" title="Reset all tracking data">Reset</button>
<button class="btn" id="btn-debug" title="Toggle tracking debug overlay">Debug</button>
</div>
</header>
<main>
<div class="dashboard-grid" id="grid"></div>
<div class="drawer-section" id="drawer-section" style="display:none">
<button class="drawer-toggle" id="drawer-toggle">
<span>More panels</span><span class="drawer-count" id="drawer-count">0</span>
</button>
<div class="drawer-panels" id="drawer-panels"></div>
</div>
</main>
<div class="override-modal" id="override-modal">
<div class="override-content">
<h3>Panel Override</h3>
<label>Locked position slot (0 = auto)</label>
<input type="number" id="override-slot" min="0" max="20" value="0">
<label>Size mode</label>
<select id="override-size" style="width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--surface2);color:var(--text);font-size:14px;margin-bottom:12px;font-family:var(--font)">
<option value="auto">Auto (by rank)</option>
<option value="large">Large (2x2)</option>
<option value="normal">Normal (1x1)</option>
<option value="compact">Compact</option>
</select>
<div class="btn-row">
<button class="btn" id="btn-override-cancel">Cancel</button>
<button class="btn active" id="btn-override-save">Apply</button>
</div>
</div>
</div>
<div class="tracking-debug" id="tracking-debug"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
const PANEL_DEFS=[
  {id:'cpu',title:'CPU Usage',unit:'%',icon:'',color:'#38bdf8',initial:42,spark:0.6},
  {id:'memory',title:'Memory',unit:'GB',icon:'',color:'#a78bfa',initial:13.2,spark:0.5},
  {id:'disk',title:'Disk I/O',unit:'MB/s',icon:'',color:'#34d399',initial:87,spark:0.7},
  {id:'network',title:'Network',unit:'Mbps',icon:'',color:'#fb923c',initial:342,spark:0.55},
  {id:'users',title:'Active Users',unit:'',icon:'',color:'#f472b6',initial:2847,spark:0.45},
  {id:'errors',title:'Error Rate',unit:'%',icon:'',color:'#f87171',initial:0.12,spark:0.3},
  {id:'latency',title:'API Latency',unit:'ms',icon:'',color:'#fbbf24',initial:47,spark:0.65},
  {id:'revenue',title:'Revenue',unit:'USD',icon:'',color:'#34d399',initial:12850,spark:0.5},
  {id:'sessions',title:'Sessions',unit:'',icon:'',color:'#38bdf8',initial:942,spark:0.4},
  {id:'queries',title:'DB Queries',unit:'/s',icon:'',color:'#a78bfa',initial:2.3,spark:0.75},
  {id:'cache',title:'Cache Hit',unit:'%',icon:'',color:'#34d399',initial:94.7,spark:0.35},
  {id:'queue',title:'Queue Depth',unit:'',icon:'',color:'#fb923c',initial:17,spark:0.55},
];
const STORAGE_KEY='adaptive_layout_v2';
const RECALC_INTERVAL=30000;
const HALF_LIFE_MIN=30;
const COMPACT_THRESHOLD=20;
const DRAWER_THRESHOLD=8;
let panels=[];
let tracking={};
let observers=[];
let visibilityTimers={};
let overrideModalTarget=null;
let drawerOpen=false;
let moveFlashTimers={};
function loadState(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    if(raw){
      const saved=JSON.parse(raw);
      tracking=saved.tracking||{};
      PANEL_DEFS.forEach(p=>{
        if(saved.overrides&&saved.overrides[p.id]){
          p._override=saved.overrides[p.id];
        }
      });
      return true;
    }
  }catch(e){console.warn('Failed to load state:',e)}
  PANEL_DEFS.forEach(p=>{
    tracking[p.id]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now(),locked:false,overrideSlot:0,overrideSize:'auto'};
  });
  return false;
}
function saveState(){
  const overrides={};
  PANEL_DEFS.forEach(p=>{if(p._override)overrides[p.id]=p._override;});
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify({tracking,overrides}));}catch(e){}
}
function computeScore(panelId){
  const t=tracking[panelId]||{clicks:0,expands:0,viewSeconds:0,lastInteraction:Date.now()};
  const freq=Math.min(t.clicks+t.expands,50)/50;
  const dur=Math.min((t.viewSeconds||0)/300,1);
  const minsSince=(Date.now()-t.lastInteraction)/60000;
  const recency=Math.exp(-minsSince/HALF_LIFE_MIN);
  return ((freq*0.4)+(dur*0.4)+(recency*0.2))*100;
}
function computeAllScores(){
  return PANEL_DEFS.map(p=>({id:p.id,score:computeScore(p.id)}));
}
function getPanelDef(id){return PANEL_DEFS.find(p=>p.id===id)}
function getEffectiveLayout(){
  const scored=computeAllScores();
  scored.sort((a,b)=>b.score-a.score);
  const layout=[];
  const overrides=[];
  scored.forEach((s,idx)=>{
    const def=getPanelDef(s.id);
    if(def._override&&def._override.slot>0){
      overrides.push({id:s.id,score:s.score,slot:def._override.slot,size:def._override.size||'auto'});
    }else{
      layout.push({id:s.id,score:s.score,rank:idx+1});
    }
  });
  overrides.sort((a,b)=>a.slot-b.slot);
  return{auto:layout,overrides};
}
function assignGridPositions(){
  const {auto,overrides}=getEffectiveLayout();
  const positions={};
  const gridLayout=[];
  const sizeClass=(score,overrideSize)=>{
    if(overrideSize==='large')return'large';
    if(overrideSize==='compact')return'compact';
    if(overrideSize==='normal')return'normal';
    if(score>=60)return'large';
    if(score>=COMPACT_THRESHOLD)return'normal';
    return'compact';
  };
  const drawerIds=[];
  const activeAuto=auto.filter(a=>a.score>=DRAWER_THRESHOLD);
  const drawerAuto=auto.filter(a=>a.score<DRAWER_THRESHOLD);
  let slot=1;
  const assigned={};
  overrides.forEach(o=>{
    const cls=sizeClass(o.score,o.size);
    positions[o.id]={size:cls,slot:o.slot,score:o.score,locked:true};
    assigned[o.id]=true;
  });
  activeAuto.forEach(a=>{
    if(assigned[a.id])return;
    const cls=sizeClass(a.score,null);
    positions[a.id]={size:cls,slot:slot++,score:a.score,locked:false};
    assigned[a.id]=true;
  });
  drawerAuto.forEach(a=>{
    positions[a.id]={size:'compact',slot:-1,score:a.score,locked:false};
    drawerIds.push(a.id);
  });
  const allIds=[...overrides.map(o=>o.id),...activeAuto.map(a=>a.id)];
  const orderedIds=[];
  const entryMap={};
  allIds.forEach(id=>{entryMap[id]=positions[id]});
  const sorted=Object.entries(entryMap).sort((a,b)=>{
    if(a[1].slot!==b[1].slot)return a[1].slot-b[1].slot;
    return b[1].score-a[1].score;
  });
  sorted.forEach(([id])=>{orderedIds.push(id)});
  return{positions,orderedIds,drawerIds};
}
function buildGridHTML(positions,orderedIds,drawerIds){
  const gridEl=document.getElementById('grid');
  const drawerSection=document.getElementById('drawer-section');
  const drawerPanels=document.getElementById('drawer-panels');
  const drawerCount=document.getElementById('drawer-count');
  let html='';
  orderedIds.forEach(id=>{
    const def=getPanelDef(id);
    const pos=positions[id];
    const sizeClass=pos.size==='large'?'large':pos.size==='compact'?'compact':'';
    const lockedClass=pos.locked?'locked':'';
    const score=pos.score.toFixed(1);
    const heatPct=Math.min(score/100,1);
    const heatColor=heatPct>0.7?`hsl(${Math.round(heatPct*120)},70%,50%)`:heatPct>0.4?`hsl(${Math.round(heatPct*90+30)},65%,55%)`:`hsl(${Math.round(heatPct*60+200)},40%,45%)`;
    html+=`<div class="panel ${sizeClass} ${lockedClass}" data-panel="${id}" id="panel-${id}">
      <div class="heat-border" style="background:${heatColor};width:${Math.round(heatPct*100)}%"></div>
      <div class="panel-header">
        <span class="panel-title">${def.title}</span>
        <div class="panel-actions">
          <button class="locked-btn" data-action="lock" data-panel="${id}" title="${pos.locked?'Unlock':'Lock'} position">${pos.locked?'':'}'}</button>
          <button data-action="override" data-panel="${id}" title="Manual override">&#9881;</button>
          <button data-action="compact" data-panel="${id}" title="Toggle compact">&#8690;</button>
        </div>
      </div>
      <div class="panel-body">
        <div><span class="panel-value" id="val-${id}">${def.initial}</span><span class="panel-unit">${def.unit}</span></div>
        <div class="panel-label">${score} pts &#183; rank ${pos.slot>0?pos.slot:'drawer'}</div>
        <div class="panel-chart" id="chart-${id}"></div>
      </div>
      <div class="panel-footer">
        <span class="panel-trend neutral" id="trend-${id}">&#8212; 0%</span>
      </div>
    </div>`;
  });
  gridEl.innerHTML=html;
  if(drawerIds.length>0){
    drawerSection.style.display='block';
    drawerCount.textContent=drawerIds.length;
    let drawerHTML='';
    drawerIds.forEach(id=>{
      const def=getPanelDef(id);
      const score=computeScore(id).toFixed(1);
      drawerHTML+=`<div class="panel compact" data-panel="${id}" id="panel-${id}">
        <div class="heat-border" style="background:var(--text3);width:30%"></div>
        <div class="panel-header">
          <span class="panel-title">${def.title}</span>
          <div class="panel-actions">
            <button data-action="promote" data-panel="${id}" title="Promote to main grid">&#8593;</button>
          </div>
        </div>
        <div class="panel-body">
          <span class="panel-value" id="val-${id}">${def.initial}</span>
          <span class="panel-unit">${def.unit}</span>
          <span class="panel-label">${score} pts</span>
        </div>
      </div>`;
    });
    drawerPanels.innerHTML=drawerHTML;
    if(drawerOpen)drawerPanels.classList.add('open');
  }else{
    drawerSection.style.display='none';
    drawerPanels.innerHTML='';
  }
}
function updateSparklines(){
  PANEL_DEFS.forEach(def=>{
    const chartEl=document.getElementById('chart-'+def.id);
    if(!chartEl)return;
    const bars=[];
    const baseVal=def.initial;
    const variance=baseVal*(def.spark||0.5);
    for(let i=0;i<24;i++){
      const val=baseVal+variance*(Math.sin(i*0.7+def.id.charCodeAt(0)*0.1)*0.6+Math.random()*0.4-0.2);
      const pct=Math.max(5,Math.min(100,(val/(baseVal*2))*100));
      bars.push(`<div class="bar" style="height:${pct}%;background:${def.color}"></div>`);
    }
    chartEl.innerHTML=bars.join('');
  });
}
function updateValues(){
  PANEL_DEFS.forEach(def=>{
    const valEl=document.getElementById('val-'+def.id);
    if(!valEl)return;
    const variance=def.initial*(def.spark||0.5)*0.3;
    const newVal=def.initial+variance*(Math.sin(Date.now()*0.001+def.id.charCodeAt(0))*0.8+Math.random()*0.4-0.2);
    const trendEl=document.getElementById('trend-'+def.id);
    const prevVal=parseFloat(valEl.textContent)||def.initial;
    const change=newVal-prevVal;
    const changePct=prevVal!==0?(change/Math.abs(prevVal))*100:0;
    valEl.textContent=def.unit==='%'||def.unit==='ms'?Math.round(newVal*100)/100:def.unit==='USD'?Math.round(newVal):newVal>=100?Math.round(newVal):Math.round(newVal*10)/10;
    if(trendEl){
      const arrow=changePct>0.5?'&#8593;':changePct<-0.5?'&#8595;':'&#8212;';
      const cls=changePct>0.5?'up':changePct<-0.5?'down':'neutral';
      trendEl.className='panel-trend '+cls;
      trendEl.innerHTML=arrow+' '+Math.abs(changePct).toFixed(1)+'%';
    }
  });
}
function renderAll(){
  const {positions,orderedIds,drawerIds}=assignGridPositions();
  buildGridHTML(positions,orderedIds,drawerIds);
  setupObservers();
  setupEventDelegation();
  updateSparklines();
  updateValues();
  updateGlobalScore();
}
function updateGlobalScore(){
  const scores=computeAllScores();
  const avg=scores.reduce((a,b)=>a+b.score,0)/Math.max(scores.length,1);
  const badge=document.getElementById('global-score');
  badge.textContent=Math.round(avg)+' pts';
  badge.className='score-badge';
  if(avg>=60)badge.classList.add('heat-1');
  else if(avg>=30)badge.classList.add('heat-2');
  else badge.classList.add('heat-3');
}
function setupObservers(){
  observers.forEach(o=>o.disconnect());
  observers=[];
  visibilityTimers={};
  const visiblePanels=new Map();
  const observer=new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      const id=entry.target.dataset.panel;
      if(!id)return;
      if(entry.isIntersecting&&entry.intersectionRatio>=0.5){
        if(!visiblePanels.has(id)){
          visiblePanels.set(id,Date.now());
        }
      }else{
        if(visiblePanels.has(id)){
          const startTime=visiblePanels.get(id);
          const duration=(Date.now()-startTime)/1000;
          if(!tracking[id])tracking[id]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now()};
          tracking[id].viewSeconds=(tracking[id].viewSeconds||0)+duration;
          visiblePanels.delete(id);
          saveState();
        }
      }
    });
  },{threshold:[0.5]});
  document.querySelectorAll('.panel[data-panel]').forEach(el=>{
    observer.observe(el);
    observers.push(observer);
  });
  const flushRemaining=()=>{
    visiblePanels.forEach((startTime,id)=>{
      const duration=(Date.now()-startTime)/1000;
      if(!tracking[id])tracking[id]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now()};
      tracking[id].viewSeconds=(tracking[id].viewSeconds||0)+duration;
    });
    visiblePanels.clear();
    saveState();
  };
  window.addEventListener('beforeunload',flushRemaining);
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden)flushRemaining();
  });
}
function flashPanel(id){
  const el=document.getElementById('panel-'+id);
  if(!el)return;
  if(moveFlashTimers[id])clearTimeout(moveFlashTimers[id]);
  el.classList.add('moved');
  moveFlashTimers[id]=setTimeout(()=>el.classList.remove('moved'),600);
}
function setupEventDelegation(){
  const handler=(e)=>{
    const btn=e.target.closest('button[data-action]');
    if(!btn)return;
    const action=btn.dataset.action;
    const panelId=btn.dataset.panel;
    if(!panelId)return;
    if(action==='lock'){
      e.stopPropagation();
      const def=getPanelDef(panelId);
      if(!def._override)def._override={slot:0,size:'auto'};
      const currentlyLocked=def._override.slot>0;
      if(currentlyLocked){
        def._override.slot=0;
      }else{
        const {positions}=assignGridPositions();
        const pos=positions[panelId];
        def._override.slot=pos?pos.slot:0;
        if(def._override.slot===0||def._override.slot===-1)def._override.slot=1;
      }
      trackInteraction(panelId,'expand');
      renderAll();
      saveState();
      flashPanel(panelId);
    }
    if(action==='override'){
      e.stopPropagation();
      overrideModalTarget=panelId;
      const def=getPanelDef(panelId);
      document.getElementById('override-slot').value=def._override?def._override.slot||0:0;
      document.getElementById('override-size').value=def._override?def._override.size||'auto':'auto';
      document.getElementById('override-modal').classList.add('open');
    }
    if(action==='compact'){
      e.stopPropagation();
      const def=getPanelDef(panelId);
      if(!def._override)def._override={slot:0,size:'auto'};
      def._override.size=def._override.size==='compact'?'auto':'compact';
      trackInteraction(panelId,def._override.size==='compact'?'collapse':'expand');
      renderAll();
      saveState();
      flashPanel(panelId);
    }
    if(action==='promote'){
      e.stopPropagation();
      if(!tracking[panelId])tracking[panelId]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now()};
      tracking[panelId].clicks=(tracking[panelId].clicks||0)+5;
      tracking[panelId].lastInteraction=Date.now();
      renderAll();
      saveState();
      showToast('Panel promoted to main grid');
    }
  };
  document.getElementById('grid').addEventListener('click',handler);
  document.getElementById('drawer-panels').addEventListener('click',handler);
  document.querySelectorAll('.panel[data-panel]').forEach(el=>{
    el.addEventListener('click',function(e){
      if(e.target.closest('button'))return;
      const id=this.dataset.panel;
      trackInteraction(id,'click');
    });
  });
}
function trackInteraction(panelId,type){
  if(!tracking[panelId]){
    tracking[panelId]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now()};
  }
  if(type==='click')tracking[panelId].clicks=(tracking[panelId].clicks||0)+1;
  if(type==='expand')tracking[panelId].expands=(tracking[panelId].expands||0)+1;
  if(type==='collapse')tracking[panelId].collapses=(tracking[panelId].collapses||0)+1;
  tracking[panelId].lastInteraction=Date.now();
  saveState();
}
function showToast(msg){
  const toast=document.getElementById('toast');
  toast.textContent=msg;
  toast.classList.add('show');
  setTimeout(()=>toast.classList.remove('show'),2000);
}
function init(){
  loadState();
  renderAll();
  document.getElementById('btn-recalc').addEventListener('click',()=>{
    renderAll();
    showToast('Layout recalculated');
  });
  document.getElementById('btn-reset').addEventListener('click',()=>{
    if(confirm('Reset all tracking data and layout overrides?')){
      PANEL_DEFS.forEach(p=>{delete p._override;});
      tracking={};
      PANEL_DEFS.forEach(p=>{
        tracking[p.id]={clicks:0,expands:0,collapses:0,viewSeconds:0,lastInteraction:Date.now(),locked:false,overrideSlot:0,overrideSize:'auto'};
      });
      localStorage.removeItem(STORAGE_KEY);
      renderAll();
      showToast('All tracking data reset');
    }
  });
  document.getElementById('btn-debug').addEventListener('click',()=>{
    const debug=document.getElementById('tracking-debug');
    debug.classList.toggle('visible');
    if(debug.classList.contains('visible')){
      updateDebugDisplay();
    }
  });
  document.getElementById('btn-override-cancel').addEventListener('click',()=>{
    document.getElementById('override-modal').classList.remove('open');
    overrideModalTarget=null;
  });
  document.getElementById('btn-override-save').addEventListener('click',()=>{
    if(!overrideModalTarget)return;
    const def=getPanelDef(overrideModalTarget);
    const slot=parseInt(document.getElementById('override-slot').value)||0;
    const size=document.getElementById('override-size').value;
    if(!def._override)def._override={slot:0,size:'auto'};
    def._override.slot=slot;
    def._override.size=size;
    document.getElementById('override-modal').classList.remove('open');
    renderAll();
    saveState();
    flashPanel(overrideModalTarget);
    showToast('Override applied');
    overrideModalTarget=null;
  });
  document.getElementById('override-modal').addEventListener('click',function(e){
    if(e.target===this){
      this.classList.remove('open');
      overrideModalTarget=null;
    }
  });
  document.getElementById('drawer-toggle').addEventListener('click',()=>{
    drawerOpen=!drawerOpen;
    const dp=document.getElementById('drawer-panels');
    if(drawerOpen)dp.classList.add('open');
    else dp.classList.remove('open');
  });
  setInterval(()=>{
    updateValues();
    updateSparklines();
    updateGlobalScore();
  },5000);
  setInterval(()=>{
    const prevLayout=assignGridPositions();
    renderAll();
    const newLayout=assignGridPositions();
    const changed=[];
    newLayout.orderedIds.forEach(id=>{
      const prev=prevLayout.positions[id];
      const next=newLayout.positions[id];
      if(prev&&next&&prev.slot!==next.slot)changed.push(id);
    });
    changed.forEach(id=>flashPanel(id));
    if(changed.length>0)showToast('Layout adapted ('+changed.length+' panels moved)');
    updateDebugDisplay();
  },RECALC_INTERVAL);
}
function updateDebugDisplay(){
  const debug=document.getElementById('tracking-debug');
  if(!debug.classList.contains('visible'))return;
  const scores=computeAllScores().sort((a,b)=>b.score-a.score);
  let html='TRACKING DEBUG\n';
  scores.forEach((s,idx)=>{
    const def=getPanelDef(s.id);
    const t=tracking[s.id]||{};
    html+=`${idx+1}. ${def.title}: ${s.score.toFixed(1)}pts (clicks:${t.clicks||0} views:${((t.viewSeconds||0)/60).toFixed(1)}m rec:${((Date.now()-t.lastInteraction)/60000).toFixed(0)}m)\n`;
  });
  debug.textContent=html;
}
document.addEventListener('DOMContentLoaded',init);
})();
</script>
</body>
</html>