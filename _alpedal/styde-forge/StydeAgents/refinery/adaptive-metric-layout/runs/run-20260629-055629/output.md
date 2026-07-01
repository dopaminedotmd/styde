<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#c9d1d9;
  --accent:#58a6ff;--accent-dim:#1f6feb33;--danger:#f85149;--success:#3fb950;
  --warn:#d2991d;--grid-gap:8px;--radius:8px;--transition:200ms ease;
  --col1:1fr;--col2:1fr;--col3:1fr;--col4:1fr;--row-def:auto;
}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;padding:16px}
.toolbar{display:flex;gap:12px;align-items:center;padding:8px 12px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:16px;flex-wrap:wrap}
.toolbar button,.toolbar select,.toolbar input{background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:4px;padding:6px 14px;cursor:pointer;font-size:13px;transition:var(--transition)}
.toolbar button:hover{background:var(--accent-dim);border-color:var(--accent)}
.toolbar button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.toolbar .spacer{flex:1}
.stat-chip{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--text);opacity:0.7}
.stat-chip .val{color:var(--accent);font-weight:600}
.grid-container{display:grid;gap:var(--grid-gap);grid-template-columns:var(--col1) var(--col2) var(--col3) var(--col4);grid-auto-rows:minmax(120px,auto);transition:grid-template-columns var(--transition)}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  position:relative;overflow:hidden;transition:all var(--transition);
  display:flex;flex-direction:column;cursor:grab;user-select:none;
}
.panel:active{cursor:grabbing}
.panel.compact{grid-row:span 1;grid-column:span 1;max-height:140px}
.panel.medium{grid-row:span 2;grid-column:span 2}
.panel.large{grid-row:span 2;grid-column:span 3}
.panel.xlarge{grid-row:span 3;grid-column:span 4}
.panel.pinned{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-dim)}
.panel.pinned .pin-indicator{display:block}
.panel.dragging{opacity:0.7;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,.5);transform:scale(1.02)}
.panel.drag-over{border-color:var(--accent);background:var(--accent-dim)}
.panel-header{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid var(--border);flex-shrink:0}
.panel-header .title{font-weight:600;font-size:14px;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .actions{display:flex;gap:4px}
.panel-header .actions button{background:none;border:none;color:var(--text);cursor:pointer;padding:2px 6px;border-radius:3px;font-size:14px;line-height:1;opacity:0.6;transition:var(--transition)}
.panel-header .actions button:hover{opacity:1;background:var(--accent-dim)}
.pin-indicator{display:none;color:var(--accent);font-size:10px;margin-right:4px}
.panel-body{flex:1;padding:12px;display:flex;align-items:center;justify-content:center;min-height:60px}
.panel-body.sparkline{flex-direction:column;align-items:stretch;justify-content:center;gap:8px}
.sparkline-chart{width:100%;height:40px;display:flex;align-items:flex-end;gap:2px}
.sparkline-chart .bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;transition:height 300ms ease;min-width:3px;opacity:0.7}
.sparkline-chart .bar.high{opacity:1}
.sparkline-label{font-size:11px;color:var(--text);opacity:0.6;text-align:center}
.stat-overlay{display:flex;gap:16px;align-items:center;justify-content:center}
.stat-overlay .stat{text-align:center}
.stat-overlay .stat .num{font-size:22px;font-weight:700;color:var(--accent);line-height:1}
.stat-overlay .stat .lbl{font-size:10px;opacity:0.6;text-transform:uppercase;letter-spacing:0.5px}
.chart-placeholder{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--text);opacity:0.3;font-size:13px}
.heatmap-indicator{position:absolute;top:4px;right:8px;font-size:10px;opacity:0.5;display:flex;gap:4px;align-items:center}
.heatmap-indicator .dot{width:8px;height:8px;border-radius:50%}
.heatmap-indicator .dot.cold{background:var(--border)}
.heatmap-indicator .dot.warm{background:var(--warn)}
.heatmap-indicator .dot.hot{background:var(--danger)}
.score-badge{font-size:10px;padding:2px 6px;border-radius:10px;background:var(--accent-dim);color:var(--accent);font-weight:600}
.toast{position:fixed;bottom:24px;right:24px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px 16px;font-size:13px;z-index:999;opacity:0;transform:translateY(12px);transition:all 300ms ease;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.reset-prompt{position:fixed;inset:0;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;z-index:1000}
.reset-prompt.hidden{display:none}
.reset-prompt .box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;max-width:360px;text-align:center}
.reset-prompt .box p{margin-bottom:16px;font-size:14px}
.reset-prompt .box button{margin:4px}
@media(max-width:900px){.grid-container{grid-template-columns:1fr 1fr}.panel.large,.panel.xlarge{grid-column:span 2}}
@media(max-width:500px){.grid-container{grid-template-columns:1fr}.panel.medium,.panel.large,.panel.xlarge{grid-column:span 1}}
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="toggleAutoLayout()" id="btn-auto" class="active">Auto-layout</button>
  <button onclick="resetAllData()">Reset Data</button>
  <span class="spacer"></span>
  <span class="stat-chip">Session: <span class="val" id="session-time">0s</span></span>
  <span class="stat-chip">Events: <span class="val" id="event-count">0</span></span>
  <span class="stat-chip">Layout version: <span class="val" id="layout-ver">1</span></span>
</div>
<div class="grid-container" id="grid"></div>
<div class="toast" id="toast"></div>
<div class="reset-prompt hidden" id="reset-prompt">
  <div class="box">
    <p>Reset all tracking data and layout preferences?</p>
    <button onclick="confirmReset()" style="background:var(--danger);color:#fff;border:none">Reset Everything</button>
    <button onclick="cancelReset()">Cancel</button>
  </div>
</div>
<script>
(function(){
'use strict';
var STORAGE_KEY = 'adaptive-dashboard-v2';
var DEBOUNCE_MS = 80;
var DRAG_COOLDOWN_MS = 300;
var REBALANCE_INTERVAL_MS = 5000;
var COMPACT_SCORE_THRESHOLD = 0.15;
var MAX_GRID_COLS = 4;
var state = loadState();
var trackingSessions = {};
var nextSessionId = 1;
var sessionStartTime = Date.now();
var totalEvents = 0;
var autoLayoutEnabled = true;
var layoutVersion = 1;
var dragState = null;
var dragCooldownUntil = 0;
var rebalanceTimer = null;
var toastTimer = null;
function defaultPanels(){
  return [
    {id:'revenue',title:'Revenue',type:'chart',data:{values:[45,52,38,65,42,58,71,49,63,55,68,72],current:68450,trend:'+12%'},span:'medium',order:0,pinned:false},
    {id:'users',title:'Active Users',type:'chart',data:{values:[120,145,132,168,155,190,178,210,195,225,240,218],current:2418,trend:'+8%'},span:'medium',order:1,pinned:false},
    {id:'cpu',title:'CPU Load',type:'sparkline',data:{values:[34,38,42,36,45,52,48,41,37,33,29,35],current:'35%',trend:'stable'},span:'compact',order:2,pinned:false},
    {id:'memory',title:'Memory',type:'sparkline',data:{values:[62,65,68,64,70,72,69,67,63,66,71,68],current:'6.8GB',trend:'+2%'},span:'compact',order:3,pinned:false},
    {id:'errors',title:'Error Rate',type:'stat',data:{current:'0.12%',trend:'-0.03%',sub:'24h'},span:'compact',order:4,pinned:false},
    {id:'latency',title:'P95 Latency',type:'sparkline',data:{values:[120,135,115,140,128,155,145,132,118,125,138,142],current:'142ms',trend:'+5ms'},span:'compact',order:5,pinned:false},
    {id:'throughput',title:'Throughput',type:'chart',data:{values:[850,920,890,1050,980,1120,1080,1150,1020,1180,1210,1250],current:'1,250rps',trend:'+18%'},span:'medium',order:6,pinned:false},
    {id:'storage',title:'Storage IO',type:'sparkline',data:{values:[200,210,195,225,240,250,235,220,215,230,245,260],current:'260MB/s',trend:'+8%'},span:'compact',order:7,pinned:false}
  ];
}
function loadState(){
  try{
    var raw = localStorage.getItem(STORAGE_KEY);
    if(raw){var d=JSON.parse(raw);if(d&&d.panels&&Array.isArray(d.panels))return d;}
  }catch(e){}
  var def = {panels:defaultPanels(),scores:{},totalViewMs:{},interactionCounts:{},lastInteraction:{}};
  saveState(def);
  return def;
}
function saveState(s){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(s||state));}catch(e){}}
function persistState(){saveState(state);}
function ensureScoreFields(id){
  state.scores[id]=state.scores[id]||0;
  state.totalViewMs[id]=state.totalViewMs[id]||0;
  state.interactionCounts[id]=state.interactionCounts[id]||0;
  state.lastInteraction[id]=state.lastInteraction[id]||0;
}
function calcScore(id){
  ensureScoreFields(id);
  var now=Date.now();
  var freq=state.interactionCounts[id]||0;
  var dur=state.totalViewMs[id]||0;
  var recency=now-(state.lastInteraction[id]||0);
  var recencyHours=Math.max(0.001,recency/3600000);
  var recencyDecay=1/(1+recencyHours);
  if(freq===0&&dur===0)return 0;
  return (Math.log1p(freq)*0.4 + Math.log1p(dur/1000)*0.35 + recencyDecay*0.25);
}
function recalcAllScores(){
  state.panels.forEach(function(p){
    state.scores[p.id]=calcScore(p.id);
  });
}
function getSortedByScore(){
  return state.panels.slice().sort(function(a,b){
    var sa=state.scores[a.id]||0;
    var sb=state.scores[b.id]||0;
    return sb-sa;
  });
}
function rankToSpan(rank,total){
  if(total<=4){
    if(rank===0)return 'xlarge';
    if(rank<=2)return 'medium';
    return 'compact';
  }
  if(rank===0)return 'large';
  if(rank<=2)return 'medium';
  if(rank<=Math.floor(total*0.5))return 'medium';
  return 'compact';
}
function applyAutoLayout(){
  if(!autoLayoutEnabled)return;
  recalcAllScores();
  var sorted=getSortedByScore();
  var maxScore=sorted.length>0?(state.scores[sorted[0].id]||0):1;
  sorted.forEach(function(p,i){
    if(p.pinned)return;
    p.span=rankToSpan(i,sorted.length);
    p.order=i;
  });
  layoutVersion++;
  persistState();
}
function clampToGrid(cellIndex,totalCells){
  return Math.max(0,Math.min(totalCells-1,cellIndex));
}
function renderPanel(p){
  var score=state.scores[p.id]||0;
  var hotness=score>0.7?'hot':score>0.3?'warm':'cold';
  var scoreDisplay=(score*100).toFixed(0);
  var isCompact=p.span==='compact';
  var header='<div class="panel-header">';
  if(p.pinned)header+='<span class="pin-indicator" title="Pinned">📌</span>';
  header+='<span class="title">'+esc(p.title)+'</span>';
  header+='<span class="score-badge" title="Attention score">'+scoreDisplay+'</span>';
  header+='<div class="actions">';
  header+='<button onclick="event.stopPropagation();togglePin(\''+p.id+'\')" title="'+(p.pinned?'Unpin':'Pin')+'">'+(p.pinned?'📌':'📍')+'</button>';
  header+='<button onclick="event.stopPropagation();cycleSpan(\''+p.id+'\')" title="Resize">⊞</button>';
  header+='</div>';
  header+='</div>';
  var body='<div class="panel-body'+(isCompact&&p.type==='sparkline'?' sparkline':'')+'">';
  if(isCompact&&p.type==='sparkline'&&p.data.values){
    var maxVal=Math.max.apply(null,p.data.values);
    body+='<div class="sparkline-chart">';
    p.data.values.forEach(function(v){
      var h=(v/maxVal*100).toFixed(0);
      var cls=h>80?'bar high':'bar';
      body+='<div class="'+cls+'" style="height:'+h+'%"></div>';
    });
    body+='</div>';
    body+='<div class="sparkline-label">'+esc(p.data.current||'')+' <span style="color:var('+(p.data.trend&&p.data.trend.startsWith('+')?'--success':'--warn')+')">'+esc(p.data.trend||'')+'</span></div>';
  }else if(isCompact&&p.type==='stat'){
    body+='<div class="stat-overlay"><div class="stat"><div class="num">'+esc(p.data.current)+'</div><div class="lbl">'+esc(p.data.trend||'')+'</div></div></div>';
  }else if(p.type==='chart'&&p.data.values){
    body+='<div class="chart-placeholder">📊 '+esc(p.data.current||'')+' '+esc(p.data.trend||'')+'</div>';
  }else{
    body+='<div class="chart-placeholder">'+esc(p.data.current||p.title)+'</div>';
  }
  body+='</div>';
  var hotnessHtml='<div class="heatmap-indicator"><span class="dot '+hotness+'"></span></div>';
  return '<div class="panel '+p.span+(p.pinned?' pinned':'')+'" data-id="'+esc(p.id)+'" draggable="true" id="panel-'+esc(p.id)+'">'+hotnessHtml+header+body+'</div>';
}
function renderAll(){
  var grid=document.getElementById('grid');
  var sorted=state.panels.slice().sort(function(a,b){return a.order-b.order;});
  grid.innerHTML=sorted.map(renderPanel).join('');
  bindPanelEvents();
  updateStats();
  document.getElementById('layout-ver').textContent=layoutVersion;
}
function bindPanelEvents(){
  var panels=document.querySelectorAll('.panel');
  panels.forEach(function(el){
    el.addEventListener('dragstart',onDragStart);
    el.addEventListener('dragend',onDragEnd);
    el.addEventListener('dragover',onDragOver);
    el.addEventListener('drop',onDrop);
    el.addEventListener('click',function(e){
      if(e.target.closest('button'))return;
      onPanelClick(el.dataset.id);
    });
  });
  var observer=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      var id=entry.target.dataset.id;
      if(!id)return;
      if(entry.isIntersecting){
        startTracking(id);
      }else{
        stopTracking(id);
      }
    });
  },{threshold:0.5});
  panels.forEach(function(el){observer.observe(el);});
}
function onDragStart(e){
  if(Date.now()<dragCooldownUntil){e.preventDefault();return;}
  var id=e.target.closest('.panel')?.dataset?.id;
  if(!id){e.preventDefault();return;}
  dragState={id:id,startX:e.clientX,startY:e.clientY};
  e.dataTransfer.effectAllowed='move';
  e.dataTransfer.setData('text/plain',id);
  setTimeout(function(){
    var el=document.getElementById('panel-'+id);
    if(el)el.classList.add('dragging');
  },0);
  dragCooldownUntil=Date.now()+DRAG_COOLDOWN_MS;
  trackInteraction(id,'drag-start');
}
function onDragEnd(e){
  var el=document.getElementById('panel-'+(dragState?.id||''));
  if(el)el.classList.remove('dragging');
  dragState=null;
  document.querySelectorAll('.panel.drag-over').forEach(function(el){el.classList.remove('drag-over');});
}
function onDragOver(e){
  e.preventDefault();
  e.dataTransfer.dropEffect='move';
  var target=e.target.closest('.panel');
  if(target&&dragState&&target.dataset.id!==dragState.id){
    target.classList.add('drag-over');
  }
}
function onDrop(e){
  e.preventDefault();
  document.querySelectorAll('.panel.drag-over').forEach(function(el){el.classList.remove('drag-over');});
  var srcId=e.dataTransfer.getData('text/plain');
  var targetEl=e.target.closest('.panel');
  if(!targetEl||!srcId||srcId===targetEl.dataset.id)return;
  var dstId=targetEl.dataset.id;
  var srcIdx=state.panels.findIndex(function(p){return p.id===srcId;});
  var dstIdx=state.panels.findIndex(function(p){return p.id===dstId;});
  if(srcIdx<0||dstIdx<0)return;
  var total=state.panels.length;
  srcIdx=clampToGrid(srcIdx,total);
  dstIdx=clampToGrid(dstIdx,total);
  var src=state.panels[srcIdx];
  state.panels.splice(srcIdx,1);
  state.panels.splice(dstIdx,0,src);
  state.panels.forEach(function(p,i){p.order=i;});
  if(!src.pinned){
    var sorted=getSortedByScore();
    var nearestRank=sorted.findIndex(function(sp){return sp.id===src.id;});
    if(nearestRank>=0){
      src.span=rankToSpan(nearestRank,total);
    }
  }
  persistState();
  renderAll();
  trackInteraction(srcId,'drop');
  trackInteraction(dstId,'drop-target');
}
function onPanelClick(id){
  trackInteraction(id,'click');
}
function togglePin(id){
  var p=state.panels.find(function(px){return px.id===id;});
  if(!p)return;
  p.pinned=!p.pinned;
  persistState();
  renderAll();
  toastMsg(p.pinned?'Pinned: '+p.title:'Unpinned: '+p.title);
  trackInteraction(id,p.pinned?'pin':'unpin');
}
function cycleSpan(id){
  var p=state.panels.find(function(px){return px.id===id;});
  if(!p)return;
  var spans=['compact','medium','large','xlarge'];
  var idx=spans.indexOf(p.span);
  p.span=spans[(idx+1)%spans.length];
  if(!p.pinned){p.pinned=true;}
  persistState();
  renderAll();
  toastMsg('Resized: '+p.title+' → '+p.span);
  trackInteraction(id,'resize');
}
function toggleAutoLayout(){
  autoLayoutEnabled=!autoLayoutEnabled;
  var btn=document.getElementById('btn-auto');
  if(autoLayoutEnabled){
    btn.classList.add('active');
    btn.textContent='Auto-layout';
    applyAutoLayout();
    renderAll();
    toastMsg('Auto-layout enabled');
  }else{
    btn.classList.remove('active');
    btn.textContent='Manual layout';
    toastMsg('Manual layout — drag to arrange');
  }
}
function startTracking(id){
  if(trackingSessions[id])return;
  var sid=nextSessionId++;
  trackingSessions[id]={sessionId:sid,startTime:Date.now()};
}
function stopTracking(id){
  var sess=trackingSessions[id];
  if(!sess)return;
  var elapsed=Date.now()-sess.startTime;
  ensureScoreFields(id);
  state.totalViewMs[id]=(state.totalViewMs[id]||0)+elapsed;
  state.lastInteraction[id]=Date.now();
  delete trackingSessions[id];
  calcScore(id);
}
function trackInteraction(id,type){
  ensureScoreFields(id);
  state.interactionCounts[id]=(state.interactionCounts[id]||0)+1;
  state.lastInteraction[id]=Date.now();
  totalEvents++;
  calcScore(id);
}
function rebalanceLoop(){
  if(!autoLayoutEnabled)return;
  applyAutoLayout();
  renderAll();
}
function updateStats(){
  var elapsed=Math.floor((Date.now()-sessionStartTime)/1000);
  var m=Math.floor(elapsed/60);
  var s=elapsed%60;
  document.getElementById('session-time').textContent=m+'m '+s+'s';
  document.getElementById('event-count').textContent=totalEvents;
}
function toastMsg(msg){
  var el=document.getElementById('toast');
  el.textContent=msg;
  el.classList.add('show');
  if(toastTimer)clearTimeout(toastTimer);
  toastTimer=setTimeout(function(){el.classList.remove('show');},2000);
}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function resetAllData(){
  document.getElementById('reset-prompt').classList.remove('hidden');
}
function confirmReset(){
  localStorage.removeItem(STORAGE_KEY);
  state=loadState();
  trackingSessions={};
  nextSessionId=1;
  totalEvents=0;
  layoutVersion=1;
  autoLayoutEnabled=true;
  document.getElementById('btn-auto').classList.add('active');
  document.getElementById('btn-auto').textContent='Auto-layout';
  document.getElementById('reset-prompt').classList.add('hidden');
  recalcAllScores();
  renderAll();
  toastMsg('All data reset');
}
function cancelReset(){
  document.getElementById('reset-prompt').classList.add('hidden');
}
function init(){
  recalcAllScores();
  renderAll();
  rebalanceTimer=setInterval(function(){
    rebalanceLoop();
    updateStats();
  },REBALANCE_INTERVAL_MS);
  setInterval(updateStats,1000);
  setInterval(persistState,10000);
}
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',init);
}else{
  init();
}
})();
</script>
</body>
</html>