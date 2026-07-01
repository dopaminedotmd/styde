<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh}
.dashboard{max-width:1400px;margin:0 auto;padding:16px}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #21262d;margin-bottom:16px}
.header h1{font-size:20px;font-weight:600;color:#f0f6fc}
.header-actions{display:flex;gap:8px}
.btn{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:12px;transition:background .15s}
.btn:hover{background:#30363d}
.btn.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;transition:all .3s ease}
.panel{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:14px;position:relative;transition:box-shadow .2s,transform .2s,border-color .2s;cursor:default;min-height:120px}
.panel:hover{border-color:#30363d}
.panel.high-rank{border-color:#1f6feb44;box-shadow:0 0 12px #1f6feb18}
.panel.locked{border-color:#d29922;box-shadow:0 0 8px #d2992218}
.panel.compact{min-height:64px;padding:8px 12px;font-size:11px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-sparkline{height:24px}
.panel.compact .panel-value{font-size:16px}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel-title{font-size:13px;font-weight:500;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.panel-value{font-size:28px;font-weight:600;color:#f0f6fc;line-height:1}
.panel-delta{font-size:11px;margin-left:6px}
.panel-delta.up{color:#3fb950}
.panel-delta.down{color:#f85149}
.panel-sparkline{width:100%;height:40px;margin-top:8px}
.panel-sparkline svg{width:100%;height:100%}
.panel-actions{display:flex;gap:4px;align-items:center}
.panel-btn{background:none;border:none;color:#484f58;cursor:pointer;font-size:14px;padding:2px 4px;border-radius:4px;line-height:1;transition:color .15s}
.panel-btn:hover{color:#c9d1d9}
.panel-btn.pinned{color:#d29922}
.panel-score{font-size:10px;color:#484f58;position:absolute;bottom:6px;right:10px}
.panel-rank-badge{position:absolute;top:-6px;left:-6px;background:#1f6feb;color:#fff;font-size:9px;font-weight:700;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;transition:background .3s}
.panel-rank-badge.low{background:#484f58}
.col-span-2{grid-column:span 2}
.col-span-1{grid-column:span 1}
.stats-bar{display:flex;gap:16px;padding:8px 0;font-size:11px;color:#484f58;margin-bottom:8px}
.stats-bar span{color:#8b949e}
@keyframes flash-rank{0%{box-shadow:0 0 0 #1f6feb44}50%{box-shadow:0 0 20px #1f6feb66}100%{box-shadow:0 0 0 #1f6feb44}}
.panel.rank-changed{animation:flash-rank .6s ease}
</style>
</head>
<body>
<div class="dashboard">
<div class="header">
<h1>Adaptive Dashboard</h1>
<div class="header-actions">
<button class="btn" id="resetBtn">Reset tracking</button>
<button class="btn" id="freezeBtn">Freeze layout</button>
<button class="btn" id="statsBtn">Show stats</button>
</div>
</div>
<div class="stats-bar" id="statsBar">
Sessions: <span id="statSessions">0</span>
Tracked interactions: <span id="statInteractions">0</span>
Layout updates: <span id="statLayouts">0</span>
</div>
<div class="grid" id="grid"></div>
</div>
<script>
(function(){
'use strict';
var PANEL_DEFS = [
{id:'cpu',title:'CPU Usage',unit:'%',range:[0,100],icon:'',color:'#58a6ff'},
{id:'memory',title:'Memory',unit:'GB',range:[0,64],icon:'',color:'#3fb950'},
{id:'network',title:'Network I/O',unit:'MB/s',range:[0,1000],icon:'',color:'#d29922'},
{id:'users',title:'Active Users',unit:'',range:[0,5000],icon:'',color:'#bc8cff'},
{id:'errors',title:'Error Rate',unit:'%',range:[0,5],icon:'',color:'#f85149'},
{id:'latency',title:'P95 Latency',unit:'ms',range:[0,500],icon:'',color:'#79c0ff'},
{id:'disk',title:'Disk Usage',unit:'%',range:[0,100],icon:'',color:'#56d364'},
{id:'throughput',title:'Throughput',unit:'rps',range:[0,10000],icon:'',color:'#f0883e'}
];
var DECAY_HALF = 300;
var SCORE_CYCLE_MS = 3000;
var DATA_TICK_MS = 1500;
var PERSIST_DEBOUNCE_MS = 400;
var COMPACT_THRESHOLD = 0.20;
var SPARKLINE_POINTS = 40;
var state = {
tracking:{},
overrides:{},
sparklines:{},
layoutVersion:0,
frozen:false,
sessions:0,
totalInteractions:0,
layoutUpdates:0
};
function now(){return Date.now()}
function debounce(fn,ms){var t;return function(){var a=arguments,c=this;clearTimeout(t);t=setTimeout(function(){fn.apply(c,a)},ms)}}
function loadState(){
try{
var raw=localStorage.getItem('adaptive_dashboard_v1');
if(raw){
var saved=JSON.parse(raw);
if(saved.tracking) state.tracking=saved.tracking;
if(saved.overrides) state.overrides=saved.overrides;
if(saved.sessions!=null) state.sessions=saved.sessions+1;
else state.sessions=1;
if(saved.totalInteractions) state.totalInteractions=saved.totalInteractions;
if(saved.layoutUpdates) state.layoutUpdates=saved.layoutUpdates;
}
}catch(e){state.sessions=1}
if(!state.sessions) state.sessions=1;
PANEL_DEFS.forEach(function(p){
if(!state.tracking[p.id]) state.tracking[p.id]={frequency:0,totalDuration:0,lastInteraction:0};
if(!state.overrides[p.id]) state.overrides[p.id]={locked:false};
if(!state.sparklines[p.id]) state.sparklines[p.id]=seedSparkline(p);
});
}
var persistState=debounce(function(){
try{
var save={tracking:state.tracking,overrides:state.overrides,sessions:state.sessions,totalInteractions:state.totalInteractions,layoutUpdates:state.layoutUpdates};
localStorage.setItem('adaptive_dashboard_v1',JSON.stringify(save));
}catch(e){}
},PERSIST_DEBOUNCE_MS);
function seedSparkline(panelDef){
var pts=[];
var base=panelDef.range[0]+(panelDef.range[1]-panelDef.range[0])*0.3;
for(var i=0;i<SPARKLINE_POINTS;i++){
pts.push(base+(Math.random()-0.5)*(panelDef.range[1]-panelDef.range[0])*0.15);
}
return pts;
}
function tickSparkline(panelDef){
var pts=state.sparklines[panelDef.id];
if(!pts||pts.length===0){state.sparklines[panelDef.id]=seedSparkline(panelDef);pts=state.sparklines[panelDef.id]}
var last=pts[pts.length-1];
var range=panelDef.range[1]-panelDef.range[0];
var delta=(Math.random()-0.5)*range*0.08;
var next=Math.max(panelDef.range[0],Math.min(panelDef.range[1],last+delta));
pts.push(next);
if(pts.length>SPARKLINE_POINTS) pts.shift();
}
function getScore(panelId){
var t=state.tracking[panelId];
if(!t) return 0;
var freq=t.frequency||0;
var dur=t.totalDuration||0;
var elapsed=(now()-(t.lastInteraction||0))/1000;
var recency=Math.exp(-elapsed*Math.LN2/DECAY_HALF);
return freq*Math.max(dur,0.01)*Math.max(recency,0.05);
}
function rankPanels(){
return PANEL_DEFS.map(function(p){
return{id:p.id,score:getScore(p.id),locked:state.overrides[p.id]&&state.overrides[p.id].locked};
}).sort(function(a,b){return b.score-a.score});
}
function computeLayout(ranked){
if(state.frozen) return ranked.map(function(r,i){return{id:r.id,span:2,row:Math.floor(i/3),col:i%3,compact:false}});
var layout=[];
var row=0,col=0;
ranked.forEach(function(r,i){
var span,compact;
if(i===0){span=2;compact=false}
else if(i<=2){span=1;compact=false}
else if(i<=5){span=1;compact=false}
else{span=1;compact=true}
if(col+span>4){row++;col=0}
layout.push({id:r.id,span:span,row:row,col:col,compact:compact,score:r.score,locked:r.locked});
col+=span;
if(col>=4){row++;col=0}
});
return layout;
}
var intersectionObserver=null;
var visibilityMap={};
function setupIntersectionObserver(){
if(intersectionObserver) intersectionObserver.disconnect();
intersectionObserver=new IntersectionObserver(function(entries){
var changed=false;
entries.forEach(function(e){
var id=e.target.dataset.panelId;
if(!id) return;
var wasVisible=visibilityMap[id]||false;
var isVisible=e.isIntersecting&&e.intersectionRatio>=0.5;
if(wasVisible&&!isVisible){
var elapsed=(now()-visibilityMap[id+'_start'])/1000;
state.tracking[id].totalDuration=(state.tracking[id].totalDuration||0)+elapsed;
state.tracking[id].lastInteraction=now();
visibilityMap[id]=false;
changed=true;
}else if(!wasVisible&&isVisible){
visibilityMap[id]=true;
visibilityMap[id+'_start']=now();
}
});
if(changed) persistState();
},{threshold:[0,0.25,0.5,0.75,1.0]});
}
function observePanels(){
intersectionObserver.disconnect();
document.querySelectorAll('.panel').forEach(function(el){
intersectionObserver.observe(el);
});
Object.keys(visibilityMap).forEach(function(k){
if(k.indexOf('_start')<0) visibilityMap[k]=false;
});
}
function trackInteraction(panelId){
var t=state.tracking[panelId];
t.frequency=(t.frequency||0)+1;
t.lastInteraction=now();
state.totalInteractions++;
persistState();
}
function toggleLock(panelId){
state.overrides[panelId].locked=!state.overrides[panelId].locked;
persistState();
render();
}
function resetTracking(){
if(!confirm('Reset all tracking data and layout?')) return;
state.tracking={};
state.overrides={};
state.sparklines={};
state.layoutVersion=0;
state.totalInteractions=0;
state.layoutUpdates=0;
PANEL_DEFS.forEach(function(p){
state.tracking[p.id]={frequency:0,totalDuration:0,lastInteraction:0};
state.overrides[p.id]={locked:false};
state.sparklines[p.id]=seedSparkline(p);
});
persistState();
render();
}
function renderSparklineSVG(panelId,panelDef){
var pts=state.sparklines[panelId]||[];
if(pts.length<2) return '';
var min=panelDef.range[0],max=panelDef.range[1];
var w=200,h=40,pad=2;
var getX=function(i){return pad+(i/(pts.length-1))*(w-2*pad)};
var getY=function(v){return h-pad-((v-min)/(max-min||1))*(h-2*pad)};
var d='M'+getX(0)+','+getY(pts[0]);
for(var i=1;i<pts.length;i++) d+=' L'+getX(i)+','+getY(pts[i]);
var lastVal=pts[pts.length-1];
var areaD=d+' L'+getX(pts.length-1)+','+(h-pad)+' L'+getX(0)+','+(h-pad)+' Z';
return '<svg viewBox="0 0 '+w+' '+h+'" preserveAspectRatio="none">'+
'<defs><linearGradient id="g'+panelId+'" x1="0" y1="0" x2="0" y2="1">'+
'<stop offset="0%" stop-color="'+panelDef.color+'44"/>'+
'<stop offset="100%" stop-color="'+panelDef.color+'04"/>'+
'</linearGradient></defs>'+
'<path d="'+areaD+'" fill="url(#g'+panelId+')"/>'+
'<path d="'+d+'" fill="none" stroke="'+panelDef.color+'" stroke-width="1.5" vector-effect="non-scaling-stroke"/>'+
'</svg>';
}
function renderPanel(layoutEntry,rank){
var p=PANEL_DEFS.find(function(d){return d.id===layoutEntry.id});
if(!p) return '';
var sparkData=state.sparklines[p.id]||[];
var lastVal=sparkData.length>0?sparkData[sparkData.length-1]:0;
var prevVal=sparkData.length>1?sparkData[sparkData.length-2]:lastVal;
var delta=lastVal-prevVal;
var deltaStr='';
if(sparkData.length>1){
var pct=prevVal!==0?Math.abs(delta/prevVal)*100:0;
deltaStr='<span class="panel-delta '+(delta>=0?'up':'down')+'">'+(delta>=0?'+':'')+pct.toFixed(1)+'%</span>';
}
var cls='panel';
if(layoutEntry.span===2) cls+=' col-span-2';
else cls+=' col-span-1';
if(layoutEntry.compact) cls+=' compact';
if(rank===0) cls+=' high-rank';
if(layoutEntry.locked) cls+=' locked';
var scoreDisplay=getScore(p.id).toFixed(0);
return '<div class="'+cls+'" data-panel-id="'+p.id+'" style="grid-row:'+(layoutEntry.row+1)+';grid-column:'+(layoutEntry.col+1)+'">'+
(rank<3?'<div class="panel-rank-badge'+(rank>1?' low':'')+'">'+(rank+1)+'</div>':'')+
'<div class="panel-header">'+
'<span class="panel-title">'+p.title+'</span>'+
'<div class="panel-actions">'+
'<button class="panel-btn'+(layoutEntry.locked?' pinned':'')+'" data-action="lock" data-panel="'+p.id+'" title="'+(layoutEntry.locked?'Unlock position':'Lock position')+'">'+(layoutEntry.locked?'':'')+'</button>'+
'</div>'+
'</div>'+
'<div class="panel-body">'+
'<div class="panel-value">'+formatValue(lastVal,p)+deltaStr+'</div>'+
'<div class="panel-sparkline">'+renderSparklineSVG(p.id,p)+'</div>'+
'</div>'+
'<div class="panel-score">score:'+scoreDisplay+'</div>'+
'</div>';
}
function formatValue(v,panelDef){
if(panelDef.id==='memory') return v.toFixed(1)+' '+panelDef.unit;
if(panelDef.id==='users') return Math.round(v).toLocaleString();
if(panelDef.id==='errors'||panelDef.id==='cpu'||panelDef.id==='disk') return v.toFixed(1)+panelDef.unit;
if(panelDef.id==='latency') return Math.round(v)+panelDef.unit;
if(panelDef.id==='throughput') return Math.round(v).toLocaleString()+' '+panelDef.unit;
return Math.round(v)+' '+panelDef.unit;
}
var rafId=null;
function render(){
var ranked=rankPanels();
var layout=computeLayout(ranked);
var html='';
layout.forEach(function(le,i){html+=renderPanel(le,i)});
document.getElementById('grid').innerHTML=html;
setupEventDelegation();
observePanels();
updateStats();
state.layoutUpdates++;
persistState();
}
function scheduleRender(){
if(rafId) cancelAnimationFrame(rafId);
rafId=requestAnimationFrame(render);
}
function updateStats(){
document.getElementById('statSessions').textContent=state.sessions;
document.getElementById('statInteractions').textContent=state.totalInteractions;
document.getElementById('statLayouts').textContent=state.layoutUpdates;
}
function setupEventDelegation(){
document.getElementById('grid').addEventListener('click',function(e){
var btn=e.target.closest('[data-action]');
if(!btn) return;
var action=btn.dataset.action;
var panelId=btn.dataset.panel;
if(action==='lock'){
e.stopPropagation();
toggleLock(panelId);
}
});
document.querySelectorAll('.panel').forEach(function(panel){
panel.addEventListener('click',function(){
var id=panel.dataset.panelId;
if(id) trackInteraction(id);
});
panel.addEventListener('dblclick',function(){
var id=panel.dataset.panelId;
if(id){trackInteraction(id);trackInteraction(id)}
});
});
}
function init(){
loadState();
setupIntersectionObserver();
scheduleRender();
setInterval(function(){
PANEL_DEFS.forEach(function(p){tickSparkline(p)});
var evicted=false;
Object.keys(visibilityMap).forEach(function(k){
if(k.indexOf('_start')<0&&visibilityMap[k]===true){
var elapsed=(now()-visibilityMap[k+'_start'])/1000;
state.tracking[k].totalDuration=(state.tracking[k].totalDuration||0)+elapsed;
visibilityMap[k+'_start']=now();
evicted=true;
}
});
if(evicted) persistState();
scheduleRender();
},DATA_TICK_MS);
setInterval(function(){
var ranked=rankPanels();
var layout=computeLayout(ranked);
var currentOrder=layout.map(function(l){return l.id}).join(',');
if(state._lastOrder!==currentOrder&&!state.frozen){
state._lastOrder=currentOrder;
scheduleRender();
}
},SCORE_CYCLE_MS);
document.getElementById('resetBtn').addEventListener('click',resetTracking);
document.getElementById('freezeBtn').addEventListener('click',function(){
state.frozen=!state.frozen;
this.classList.toggle('active',state.frozen);
this.textContent=state.frozen?'Unfreeze layout':'Freeze layout';
});
document.getElementById('statsBtn').addEventListener('click',function(){
var ranked=rankPanels();
var report='Panel Rankings\n'+Array(30).join('-')+'\n';
ranked.forEach(function(r,i){
report+=(i+1)+'. '+r.id+' score:'+r.score.toFixed(1)+' freq:'+(state.tracking[r.id].frequency||0)+' dur:'+(state.tracking[r.id].totalDuration||0).toFixed(0)+'s locked:'+r.locked+'\n';
});
alert(report);
});
}
if(document.readyState==='loading'){
document.addEventListener('DOMContentLoaded',init);
}else{
init();
}
console.assert(typeof IntersectionObserver!=='undefined','IntersectionObserver required');
})();
</script>
</body>
</html>