<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4eb;--muted:#8b8fa8;
  --accent:#6c8cff;--accent2:#4ecdc4;--warn:#f7c948;--danger:#ff6b6b;
  --radius:8px;--radius-sm:4px;--shadow:0 2px 8px rgba(0,0,0,.3);--transition:200ms ease;
  --gap:12px;--header-h:48px;--compact-min-h:120px
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
#app{display:flex;flex-direction:column;height:100vh}
#header{height:var(--header-h);display:flex;align-items:center;padding:0 16px;background:var(--surface);border-bottom:1px solid var(--border);gap:16px;flex-shrink:0}
#header h1{font-size:16px;font-weight:600;color:var(--accent);white-space:nowrap}
#header .badge{font-size:11px;background:var(--accent);color:#fff;padding:2px 8px;border-radius:10px}
#header .controls{margin-left:auto;display:flex;gap:8px;align-items:center}
#header button{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:var(--radius-sm);cursor:pointer;font-size:12px;transition:background var(--transition)}
#header button:hover{background:var(--border)}
#header button.active{background:var(--accent);border-color:var(--accent);color:#fff}
#grid-container{flex:1;overflow-y:auto;padding:var(--gap);position:relative}
#grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);padding-bottom:60px}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);position:relative;display:flex;flex-direction:column;min-height:200px}
.panel.compact{min-height:var(--compact-min-h);grid-row:span 1}
.panel.expanded{grid-column:span 2;grid-row:span 2;min-height:400px}
.panel.locked{border-color:var(--warn)}
.panel-header{display:flex;align-items:center;padding:8px 12px;background:rgba(255,255,255,.03);border-bottom:1px solid var(--border);gap:8px;cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-size:13px;font-weight:500;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-header .rank-badge{font-size:10px;background:var(--accent);color:#fff;padding:1px 6px;border-radius:8px;white-space:nowrap}
.panel-header .actions{display:flex;gap:4px}
.panel-header .actions button{background:none;border:none;color:var(--muted);cursor:pointer;padding:2px 6px;font-size:14px;line-height:1;border-radius:var(--radius-sm);transition:all var(--transition)}
.panel-header .actions button:hover{color:var(--text);background:rgba(255,255,255,.05)}
.panel-header .actions button.lock-btn.locked{color:var(--warn)}
.panel-body{padding:12px;flex:1;display:flex;flex-direction:column;gap:8px;overflow:hidden;position:relative}
.metric-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.03)}
.metric-label{font-size:11px;color:var(--muted)}
.metric-value{font-size:18px;font-weight:600}
.metric-value.up{color:var(--accent2)}
.metric-value.down{color:var(--danger)}
.mini-chart{width:100%;height:40px;margin-top:4px}
.compact .mini-chart{height:24px}
.panel.ghost{opacity:.4;pointer-events:none}
.drag-placeholder{border:2px dashed var(--accent);border-radius:var(--radius);background:rgba(108,140,255,.05);min-height:200px;grid-column:span 2}
#stats-bar{position:fixed;bottom:0;left:0;right:0;height:32px;background:var(--surface);border-top:1px solid var(--border);display:flex;align-items:center;padding:0 12px;font-size:11px;color:var(--muted);gap:16px;z-index:100}
#stats-bar span{white-space:nowrap}
#reset-btn{margin-left:auto;background:none;border:none;color:var(--danger);cursor:pointer;font-size:11px;padding:2px 8px;border-radius:var(--radius-sm)}
#reset-btn:hover{background:rgba(255,107,107,.1)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.pulse{animation:pulse 1.5s infinite}
</style>
</head>
<body>
<div id="app">
  <div id="header">
    <h1>Adaptive Layout</h1>
    <span class="badge" id="score-badge">--</span>
    <div class="controls">
      <button id="btn-auto" class="active" onclick="AdaptiveLayout.setMode('auto')">Auto</button>
      <button id="btn-manual" onclick="AdaptiveLayout.setMode('manual')">Manual</button>
      <button id="btn-reset-scores" onclick="AdaptiveLayout.resetScores()">Reset Scores</button>
    </div>
  </div>
  <div id="grid-container"><div id="grid"></div></div>
  <div id="stats-bar">
    <span id="stat-mode">Mode: Auto</span>
    <span id="stat-updates">Updates: 0</span>
    <span id="stat-visible">Visible: true</span>
    <button id="reset-btn" onclick="AdaptiveLayout.resetAll()">Reset All</button>
  </div>
</div>
<script>
(function(){
'use strict';
const CONF = {
  IDLE_THRESHOLD_MS: 5000,
  IDLE_POLL_HZ: 1,
  ACTIVE_POLL_HZ: 4,
  RANK_DECAY_DAYS: 7,
  COMPACT_SCORE_MAX: 30,
  EXPAND_SCORE_MIN: 70,
  REBALANCE_DEBOUNCE_MS: 2000,
  STORAGE_KEY: 'adaptive_layout_v1',
  GRADIENT_ID_PREFIX: 'grad-'
};
let gradientCounter = 0;
function uniqueGradientId(base){ return CONF.GRADIENT_ID_PREFIX + (gradientCounter++) + '-' + base; }
function safeParse(v, fallback){
  if(v===null||v===undefined)return fallback;
  let n=Number(v);
  if(!isNaN(n))return n;
  n=parseFloat(v);
  if(!isNaN(n))return n;
  let m=String(v).match(/[\d.-]+/);
  if(m){let p=parseFloat(m[0]);if(!isNaN(p))return p;}
  return fallback;
}
const metricsDef = [
  {id:'cpu',label:'CPU Usage',unit:'%',min:5,max:95,color:'#6c8cff'},
  {id:'memory',label:'Memory',unit:'GB',min:2,max:32,color:'#4ecdc4'},
  {id:'requests',label:'Requests/s',unit:'',min:100,max:5000,color:'#f7c948'},
  {id:'errors',label:'Error Rate',unit:'%',min:0,max:15,color:'#ff6b6b'},
  {id:'latency',label:'P95 Latency',unit:'ms',min:10,max:500,color:'#a78bfa'},
  {id:'users',label:'Active Users',unit:'',min:0,max:2000,color:'#34d399'}
];
const panelDefs = metricsDef.map((m,i)=>({
  id:'panel-'+m.id,metric:m,title:m.label,
  initialRank:100-(i*8),locked:false,manualPos:-1
}));
let state={
  panels:[],
  mode:'auto',
  updates:0,
  lastInteraction:Date.now(),
  visible:true,
  observerActive:false,
  renderScheduled:false,
  lastRenderedDataHash:'',
  renderRAF:null
};
function now(){ return Date.now(); }
function loadState(){
  try{
    let raw=localStorage.getItem(CONF.STORAGE_KEY);
    if(raw){
      let saved=JSON.parse(raw);
      if(saved.panels&&Array.isArray(saved.panels)){
        let map=new Map(saved.panels.map(p=>[p.id,p]));
        state.panels=panelDefs.map(def=>{
          let s=map.get(def.id);
          if(s)return{...def,score:s.score||def.initialRank,views:s.views||0,lastViewed:s.lastViewed||0,interactions:s.interactions||0,totalDuration:s.totalDuration||0,locked:s.locked||false,manualPos:s.manualPos||-1};
          return{...def,score:def.initialRank,views:0,lastViewed:0,interactions:0,totalDuration:0,locked:false,manualPos:-1};
        });
      }else{resetPanels();}
      if(saved.mode)state.mode=saved.mode;
    }else{resetPanels();}
  }catch(e){resetPanels();}
}
function resetPanels(){
  state.panels=panelDefs.map(d=>({...d,score:d.initialRank,views:0,lastViewed:0,interactions:0,totalDuration:0,locked:false,manualPos:-1}));
}
function saveState(){
  try{
    let data={mode:state.mode,panels:state.panels.map(p=>({id:p.id,score:p.score,views:p.views,lastViewed:p.lastViewed,interactions:p.interactions,totalDuration:p.totalDuration,locked:p.locked,manualPos:p.manualPos})),savedAt:now()};
    localStorage.setItem(CONF.STORAGE_KEY,JSON.stringify(data));
  }catch(e){/* quota exceeded — silently fail */}
}
function trackView(panelId,duration){
  if(duration<100)return;
  let p=state.panels.find(x=>x.id===panelId);
  if(!p)return;
  p.views=(p.views||0)+1;
  p.totalDuration=(p.totalDuration||0)+duration;
  p.lastViewed=now();
  recalcScore(p);
}
function trackInteraction(panelId){
  let p=state.panels.find(x=>x.id===panelId);
  if(!p)return;
  p.interactions=(p.interactions||0)+1;
  p.lastViewed=now();
  recalcScore(p);
}
function recalcScore(p){
  let daysSinceLastView=(now()-p.lastViewed)/(86400000);
  let recencyFactor=Math.exp(-daysSinceLastView/CONF.RANK_DECAY_DAYS);
  let viewScore=Math.min((p.views||0)*10,50);
  let durationScore=Math.min((p.totalDuration||0)/60000*10,30);
  let interactionScore=Math.min((p.interactions||0)*5,20);
  p.score=Math.round((viewScore+durationScore+interactionScore)*recencyFactor);
  if(p.score<0)p.score=0;
  if(p.score>100)p.score=100;
}
function computeLayout(){
  if(state.mode==='manual')return state.panels.map((p,i)=>({...p,position:i,compact:p.score<CONF.COMPACT_SCORE_MAX,expanded:p.score>CONF.EXPAND_SCORE_MIN}));
  let ranked=[...state.panels].sort((a,b)=>b.score-a.score);
  let locked=ranked.filter(p=>p.locked);
  let unlocked=ranked.filter(p=>!p.locked);
  let result=[];
  locked.forEach(p=>{result.push({...p,position:p.manualPos>=0?p.manualPos:result.length,compact:p.score<CONF.COMPACT_SCORE_MAX,expanded:p.score>CONF.EXPAND_SCORE_MIN});});
  unlocked.forEach((p,i)=>{result.push({...p,position:result.length,compact:p.score<CONF.COMPACT_SCORE_MAX,expanded:p.score>CONF.EXPAND_SCORE_MIN});});
  result.sort((a,b)=>a.position-b.position);
  return result;
}
let observer=null;
function setupObserver(){
  if(observer)observer.disconnect();
  observer=new IntersectionObserver((entries)=>{
    state.visible=entries[0].isIntersecting;
    document.getElementById('stat-visible').textContent='Visible: '+state.visible;
    if(state.visible){resumeTracking();}else{pauseTracking();}
  },{threshold:0});
  observer.observe(document.getElementById('grid-container'));
}
let trackInterval=null;
let idleTimeout=null;
function pauseTracking(){
  if(trackInterval){clearInterval(trackInterval);trackInterval=null;}
  if(state.renderRAF){cancelAnimationFrame(state.renderRAF);state.renderRAF=null;state.renderScheduled=false;}
}
function resumeTracking(){startTracking();scheduleRender();}
function startTracking(){
  if(trackInterval)clearInterval(trackInterval);
  let hz=CONF.ACTIVE_POLL_HZ;
  if(now()-state.lastInteraction>CONF.IDLE_THRESHOLD_MS)hz=CONF.IDLE_POLL_HZ;
  trackInterval=setInterval(()=>{
    let idle=now()-state.lastInteraction>CONF.IDLE_THRESHOLD_MS;
    if(idle&&hz!==CONF.IDLE_POLL_HZ){hz=CONF.IDLE_POLL_HZ;clearInterval(trackInterval);trackInterval=setInterval(()=>trackCycle(),1000/CONF.IDLE_POLL_HZ);}
    if(!idle&&hz!==CONF.ACTIVE_POLL_HZ){hz=CONF.ACTIVE_POLL_HZ;clearInterval(trackInterval);trackInterval=setInterval(()=>trackCycle(),1000/CONF.ACTIVE_POLL_HZ);}
    trackCycle();
  },1000/hz);
}
function trackCycle(){
  if(!state.visible)return;
  state.panels.forEach(p=>{
    let el=document.getElementById(p.id);
    if(!el)return;
    let rect=el.getBoundingClientRect();
    let vh=window.innerHeight;
    if(rect.top<vh&&rect.bottom>0){let visiblePortion=Math.min(rect.bottom,vh)-Math.max(rect.top,0);if(visiblePortion>50){trackView(p.id,200);}}
  });
}
function scheduleRender(){
  if(state.renderScheduled||!state.visible)return;
  state.renderScheduled=true;
  state.renderRAF=requestAnimationFrame(()=>{
    state.renderRAF=null;state.renderScheduled=false;
    if(!state.visible)return;
    render();
  });
}
let lastLayout=null;
let lastMetrics=null;
function dataChanged(layout){
  let layoutKey=layout.map(p=>p.id+':'+p.score+':'+(p.compact?1:0)+':'+(p.expanded?1:0)+':'+p.position).join('|');
  return layoutKey!==lastLayout;
}
function metricsChanged(){
  let key=metricsDef.map(m=>m.id+':'+Math.round((m.min+Math.random()*(m.max-m.min)))).join('|');
  let changed=key!==lastMetrics;
  lastMetrics=key;
  return changed;
}
function render(){
  let layout=computeLayout();
  if(!dataChanged(layout)&&!metricsChanged())return;
  lastLayout=layout.map(p=>p.id+':'+p.score+':'+(p.compact?1:0)+':'+(p.expanded?1:0)+':'+p.position).join('|');
  let grid=document.getElementById('grid');
  let existing=new Map();
  grid.querySelectorAll('.panel').forEach(el=>existing.set(el.id,el));
  let frag=document.createDocumentFragment();
  let seen=new Set();
  layout.forEach((lp,i)=>{
    seen.add(lp.id);
    let el=existing.get(lp.id);
    if(!el){
      el=document.createElement('div');el.className='panel';el.id=lp.id;
      el.innerHTML=buildPanelHTML(lp);
      el.querySelector('.lock-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleLock(lp.id);});
      el.querySelector('.collapse-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleCollapse(lp.id);});
      el.addEventListener('click',()=>{state.lastInteraction=now();trackInteraction(lp.id);});
      el.addEventListener('mouseenter',()=>{state.lastInteraction=now();});
    }
    el.className='panel'+(lp.compact?' compact':'')+(lp.expanded?' expanded':'')+(lp.locked?' locked':'');
    el.style.order=lp.position;
    if(lp.locked){el.style.gridColumn=lp.expanded?'span 2':'';el.style.gridRow=lp.expanded?'span 2':'';}
    let rankBadge=el.querySelector('.rank-badge');
    if(rankBadge)rankBadge.textContent='#'+(i+1)+' '+lp.score;
    updatePanelMetrics(el,lp);
    frag.appendChild(el);
  });
  existing.forEach((el,id)=>{if(!seen.has(id))el.remove();});
  grid.innerHTML='';
  grid.appendChild(frag);
  state.updates++;
  document.getElementById('stat-updates').textContent='Updates: '+state.updates;
  let avgScore=Math.round(layout.reduce((s,p)=>s+p.score,0)/layout.length);
  document.getElementById('score-badge').textContent=avgScore;
}
function buildPanelHTML(lp){
  let m=lp.metric;
  let gid=uniqueGradientId(m.id);
  return '<div class="panel-header"><span class="title">'+esc(m.label)+'</span><span class="rank-badge">#'+lp.position+' '+lp.score+'</span><div class="actions"><button class="collapse-btn" title="Collapse">−</button><button class="lock-btn'+(lp.locked?' locked':'')+'" title="Lock">'+'🔒'+'</button></div></div><div class="panel-body"><div class="metric-row"><span class="metric-label">Current</span><span class="metric-value" id="val-'+lp.id+'">--</span></div><div class="metric-row"><span class="metric-label">Views</span><span>'+lp.views+'</span></div><div class="metric-row"><span class="metric-label">Score</span><span>'+lp.score+'</span></div><svg class="mini-chart" id="chart-'+lp.id+'"><defs><linearGradient id="'+gid+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="'+m.color+'" stop-opacity="0.4"/><stop offset="100%" stop-color="'+m.color+'" stop-opacity="0.05"/></linearGradient></defs></svg></div>';
}
function esc(s){let d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function updatePanelMetrics(el,lp){
  let m=lp.metric;
  let val=Math.round(m.min+Math.random()*(m.max-m.min));
  let prevVal=safeParse(el.dataset&&el.dataset.prevVal,val);
  let valEl=el.querySelector('#val-'+lp.id);
  if(valEl){
    valEl.textContent=val+m.unit;
    valEl.className='metric-value'+(val>prevVal?' up':val<prevVal?' down':'');
    if(el.dataset)el.dataset.prevVal=val;
    else el.setAttribute('data-prev-val',val);
  }
  let svg=el.querySelector('#chart-'+lp.id);
  if(svg){
    let w=svg.clientWidth||280,h=svg.clientHeight||40;
    let pts=Array.from({length:12},()=>Math.round(m.min+Math.random()*(m.max-m.min)));
    let maxV=Math.max(...pts,1);
    let gid=svg.querySelector('linearGradient').id;
    let pathD='M0,'+h+' '+'L'+pts.map((v,i)=>(i*w/(pts.length-1))+','+(h-(v/maxV)*(h-4))).join(' ')+' L'+w+','+h+' Z';
    let existing=svg.querySelector('path');
    if(!existing){let p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('fill','url(#'+gid+')');svg.appendChild(p);existing=p;}
    existing.setAttribute('d',pathD);
  }
}
function toggleLock(panelId){
  let p=state.panels.find(x=>x.id===panelId);if(!p)return;
  p.locked=!p.locked;state.lastInteraction=now();
  saveState();scheduleRender();
}
function toggleCollapse(panelId){
  let p=state.panels.find(x=>x.id===panelId);if(!p)return;
  p.score=Math.max(0,p.score-20);state.lastInteraction=now();
  saveState();scheduleRender();
}
window.AdaptiveLayout={
  setMode:function(m){
    state.mode=m;state.lastInteraction=now();
    document.getElementById('btn-auto').classList.toggle('active',m==='auto');
    document.getElementById('btn-manual').classList.toggle('active',m==='manual');
    document.getElementById('stat-mode').textContent='Mode: '+(m==='auto'?'Auto':'Manual');
    saveState();scheduleRender();
  },
  resetScores:function(){state.panels.forEach(p=>{p.score=p.initialRank;p.views=0;p.interactions=0;p.totalDuration=0;p.lastViewed=0;p.locked=false;p.manualPos=-1;});state.lastInteraction=now();saveState();scheduleRender();},
  resetAll:function(){localStorage.removeItem(CONF.STORAGE_KEY);resetPanels();state.mode='auto';state.lastInteraction=now();document.getElementById('btn-auto').classList.add('active');document.getElementById('btn-manual').classList.remove('active');document.getElementById('stat-mode').textContent='Mode: Auto';saveState();scheduleRender();},
  getState:function(){return state;}
};
document.addEventListener('click',()=>{state.lastInteraction=now();});
document.addEventListener('keydown',()=>{state.lastInteraction=now();});
document.addEventListener('mousemove',()=>{state.lastInteraction=now();});
window.addEventListener('resize',()=>{state.lastInteraction=now();scheduleRender();});
loadState();
setupObserver();
startTracking();
scheduleRender();
})();
</script>
</body>
</html>