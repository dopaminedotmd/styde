<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
--bg:#0f1117;--surface:#1a1d27;--surface2:#222634;--border:#2a2e3d;
--text:#e1e4ed;--text2:#8b90a0;--accent:#6c8cff;--accent2:#4ade80;
--warn:#f59e0b;--danger:#ef4444;--compact-scale:0.55;
--grid-gap:10px;--radius:10px;--transition:0.35s cubic-bezier(0.25,0.8,0.25,1.2);
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;gap:8px;padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--border);align-items:center;position:sticky;top:0;z-index:100}
.toolbar h1{font-size:16px;font-weight:600;margin-right:auto}
.toolbar .badge{font-size:11px;padding:3px 8px;border-radius:12px;background:var(--surface2);color:var(--text2)}
.btn{padding:6px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:12px;transition:all 0.15s}
.btn:hover{background:var(--border);border-color:var(--accent)}
.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.warn{background:var(--warn);border-color:var(--warn);color:#000}
.dashboard{display:grid;gap:var(--grid-gap);padding:12px;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(140px,auto);max-width:1400px;margin:0 auto}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);position:relative;display:flex;flex-direction:column;contain:layout style}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 2;grid-row:span 1}
.panel.normal{grid-column:span 1;grid-row:span 1}
.panel.compact{transform:scale(var(--compact-scale));transform-origin:top left;opacity:0.7;margin-bottom:-45px}
.panel.compact:hover{transform:scale(1);opacity:1;z-index:10;margin-bottom:0;box-shadow:0 8px 30px rgba(0,0,0,0.5)}
.panel.mini{grid-column:span 1;grid-row:span 1;max-height:50px;overflow:hidden;opacity:0.5}
.panel.mini:hover{max-height:none;opacity:1;z-index:10}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.locked::after{content:'🔒';position:absolute;top:6px;right:36px;font-size:11px;opacity:0.8;pointer-events:none}
.panel-header{display:flex;align-items:center;padding:8px 10px;gap:6px;border-bottom:1px solid var(--border);background:var(--surface2);cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:12px;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-rank{font-size:10px;color:var(--text2);background:var(--surface);padding:1px 6px;border-radius:8px;min-width:20px;text-align:center}
.panel-body{flex:1;padding:10px;display:flex;align-items:center;justify-content:center;min-height:60px;position:relative}
.panel-body canvas{max-width:100%;max-height:100%}
.panel-actions{display:flex;gap:2px}
.panel-actions button{width:24px;height:24px;border:none;background:none;color:var(--text2);cursor:pointer;border-radius:4px;font-size:13px;display:flex;align-items:center;justify-content:center;transition:all 0.12s}
.panel-actions button:hover{background:var(--border);color:var(--text)}
.panel-actions button.active{color:var(--accent);background:rgba(108,140,255,0.12)}
.metric-value{font-size:38px;font-weight:700;line-height:1}
.metric-label{font-size:11px;color:var(--text2);margin-top:4px}
.metric-unit{font-size:14px;font-weight:400;color:var(--text2);margin-left:2px}
.metric-trend{font-size:12px;margin-top:4px}
.metric-trend.up{color:var(--accent2)}
.metric-trend.down{color:var(--danger)}
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
.status-dot.ok{background:var(--accent2)}
.status-dot.warn{background:var(--warn)}
.status-dot.crit{background:var(--danger)}
.sparkline{width:100%;height:40px}
.compact-preview{font-size:10px;color:var(--text2);text-align:center;overflow:hidden;max-height:30px}
.more-section{grid-column:1/-1;padding:8px;text-align:center}
.more-section summary{font-size:12px;color:var(--text2);cursor:pointer;padding:4px 12px;display:inline-block;border-radius:6px;background:var(--surface2)}
.more-section summary:hover{color:var(--text)}
.tooltip{position:fixed;background:var(--surface2);border:1px solid var(--border);padding:6px 10px;border-radius:6px;font-size:11px;pointer-events:none;z-index:1000;display:none;white-space:nowrap}
@keyframes rankPulse{0%{box-shadow:0 0 0 0 rgba(108,140,255,0.4)}70%{box-shadow:0 0 0 8px rgba(108,140,255,0)}100%{box-shadow:0 0 0 0 rgba(108,140,255,0)}}
.panel.rank-changed{animation:rankPulse 0.6s ease}
.drop-zone{position:absolute;inset:0;border:2px dashed var(--accent);border-radius:var(--radius);background:rgba(108,140,255,0.06);display:none;pointer-events:none;z-index:5}
.panel.drag-over .drop-zone{display:block}
.panel.dragging{opacity:0.5;z-index:1}
@media(max-width:900px){.dashboard{grid-template-columns:repeat(2,1fr)}.panel.large{grid-column:span 2}.panel.medium{grid-column:span 2}}
@media(max-width:500px){.dashboard{grid-template-columns:1fr}.panel.large,.panel.medium,.panel.normal{grid-column:span 1}}
</style>
</head>
<body>
<div class="toolbar">
<h1>Adaptive Dashboard</h1>
<span class="badge" id="tracking-badge">tracking active</span>
<span class="badge" id="event-count">0 events</span>
<span class="badge" id="sort-count">0 resorts</span>
<button class="btn" id="btn-reset-layout" title="Reset learned layout">Reset Layout</button>
<button class="btn" id="btn-force-sort" title="Force immediate re-rank">Re-rank Now</button>
<button class="btn" id="btn-export" title="Export tracking data">Export Data</button>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
const CONF={sortThreshold:10,maxSortInterval:30000,debounceMs:300,throttleMs:100,decayHalfLife:86400000,compactThreshold:0.15,miniThreshold:0.05,viewDurationInterval:1000};
const LS_KEY='adaptive_dashboard_v2';
function now(){return Date.now()}
function debounce(fn,ms){let t;return function(...a){clearTimeout(t);t=setTimeout(()=>fn.apply(this,a),ms)}}
function throttle(fn,ms){let last=0;return function(...a){const n=now();if(n-last>=ms){last=n;fn.apply(this,a)}}}
const panels=[
{id:'cpu',title:'CPU Usage',type:'gauge',icon:'',color:'#6c8cff'},
{id:'memory',title:'Memory',type:'bar',icon:'',color:'#4ade80'},
{id:'network',title:'Network Throughput',type:'line',icon:'',color:'#f59e0b'},
{id:'users',title:'Active Users',type:'counter',icon:'',color:'#a78bfa'},
{id:'errors',title:'Error Rate',type:'sparkline',icon:'',color:'#ef4444'},
{id:'latency',title:'P95 Latency',type:'number',icon:'',color:'#fb923c'},
{id:'diskio',title:'Disk I/O',type:'dualbar',icon:'',color:'#38bdf8'},
{id:'queue',title:'Queue Depth',type:'number',icon:'',color:'#f472b6'},
{id:'throughput',title:'Throughput',type:'area',icon:'',color:'#34d399'},
{id:'uptime',title:'Uptime',type:'timer',icon:'',color:'#818cf8'},
{id:'alerts',title:'Alert Status',type:'status',icon:'',color:'#f87171'},
{id:'responsetime',title:'Response Time',type:'histogram',icon:'',color:'#2dd4bf'},
];
const state={
panels:new Map(),
tracking:new Map(),
layout:{},
overrides:{},
changeCount:0,
lastSort:0,
viewObservers:new Map(),
dragging:null,
dragOver:null,
};
function initTracking(pid){
if(!state.tracking.has(pid)){
state.tracking.set(pid,{viewDuration:0,interactions:0,collapseCount:0,expandCount:0,lastInteraction:now(),firstSeen:now(),locked:false,score:0});
}
}
function computeScore(t,pid){
const d=t.get(pid);if(!d)return 0;
const age=now()-d.lastInteraction;
const recency=Math.exp(-age/CONF.decayHalfLife);
const durationNorm=Math.log1p(d.viewDuration/1000);
const score=(d.interactions+1)*durationNorm*recency;
d.score=score;
return score;
}
function rankAll(){
const t=state.tracking;
const scores=[];
for(const[pid,d]of t){
const s=computeScore(t,pid);
scores.push({pid,score:s,interactions:d.interactions,duration:d.viewDuration});
}
scores.sort((a,b)=>b.score-a.score);
return scores;
}
function getTier(rank,total){
if(rank===0)return'large';
if(rank<=Math.floor(total*0.25))return'medium';
if(rank<=Math.floor(total*0.6))return'normal';
const topScore=state.tracking.get([...state.tracking.keys()][0])?.score||1;
const pScore=state.tracking.get([...state.tracking.keys()][rank])?.score||0;
if(topScore>0&&pScore/topScore<CONF.compactThreshold)return'compact';
return'normal';
}
function applyLayout(ranked){
const total=ranked.length;
const overrides=state.overrides;
const layout={};
const assigned=new Set();
for(const[pid,pos]of Object.entries(overrides)){
layout[pid]={tier:pos.tier||'normal',locked:true,rank:pos.rank||0};
assigned.add(pid);
}
let gridIdx=0;
const gridSlots=[];
for(let row=0;row<Math.ceil(total/2);row++){
for(let col=0;col<4;col++){
gridSlots.push({row,col});
}
}
for(const{pid} of ranked){
if(assigned.has(pid))continue;
const rank=gridIdx;
const tier=getTier(rank,total);
layout[pid]={tier,locked:false,rank};
gridIdx++;
if(tier==='large')gridIdx++;
}
state.layout=layout;
state.lastSort=now();
state.changeCount=0;
}
function maybeResort(force){
state.changeCount++;
if(state.changeCount>=CONF.sortThreshold||force||(now()-state.lastSort>CONF.maxSortInterval)){
const ranked=rankAll();
applyLayout(ranked);
renderLayout();
updateBadges();
}
}
const debouncedResort=debounce(()=>maybeResort(true),500);
const throttledResort=throttle(()=>maybeResort(false),CONF.throttleMs);
function recordInteraction(pid,type){
initTracking(pid);
const t=state.tracking.get(pid);
t.interactions++;
t.lastInteraction=now();
if(type==='collapse')t.collapseCount++;
if(type==='expand')t.expandCount++;
throttledResort();
}
function createPanelElement(pid){
const p=state.panels.get(pid);
const lo=state.layout[pid]||{tier:'normal',locked:false,rank:0};
const el=document.createElement('div');
el.className=`panel ${lo.tier}`+(lo.locked?' locked':'');
el.dataset.pid=pid;
el.draggable=true;
el.innerHTML=`
<div class="drop-zone"></div>
<div class="panel-header">
<span class="panel-rank">#${lo.rank+1}</span>
<span class="panel-title">${p.title}</span>
<div class="panel-actions">
<button class="btn-lock${lo.locked?' active':''}" data-action="lock" title="Lock position">L</button>
<button class="btn-collapse" data-action="toggle" title="Collapse/Expand">_</button>
</div>
</div>
<div class="panel-body" data-panel-body="${pid}"></div>
`;
return el;
}
function renderPanelBody(pid){
const body=document.querySelector(`[data-panel-body="${pid}"]`);
if(!body)return;
const p=state.panels.get(pid);
const lo=state.layout[pid]||{tier:'normal'};
const isCompact=lo.tier==='compact'||lo.tier==='mini';
body.innerHTML='';
if(isCompact&&lo.tier==='mini'){
body.innerHTML=`<div class="compact-preview">${p.title} — collapsed</div>`;
return;
}
if(isCompact){
body.innerHTML=`<div class="compact-preview">${p.title} — hover to expand</div>`;
return;
}
switch(p.type){
case'gauge':
body.innerHTML=`<div style="text-align:center"><div class="metric-value" style="color:${p.color}">${42+Math.floor(Math.random()*35)}<span class="metric-unit">%</span></div><div class="metric-label">CPU Utilization</div><div class="metric-trend up">+3.2%</div></div>`;
break;
case'bar':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="bar"></canvas><div class="metric-label">${(2+Math.random()*6).toFixed(1)} GB / 16 GB</div>`;
break;
case'line':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="line"></canvas><div class="metric-label">${(80+Math.random()*200).toFixed(0)} Mbps</div>`;
break;
case'counter':
body.innerHTML=`<div style="text-align:center"><div class="metric-value" style="color:${p.color}">${1200+Math.floor(Math.random()*500)}</div><div class="metric-label">Concurrent Users</div><div class="metric-trend up">+42</div></div>`;
break;
case'sparkline':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="spark"></canvas><div class="metric-trend down">0.12% error rate</div>`;
break;
case'number':
body.innerHTML=`<div style="text-align:center"><div class="metric-value" style="color:${p.color}">${(45+Math.random()*80).toFixed(0)}<span class="metric-unit">ms</span></div><div class="metric-label">P95 Latency</div></div>`;
break;
case'dualbar':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="dual"></canvas><div class="metric-label">R: ${(10+Math.random()*50).toFixed(0)} MB/s | W: ${(5+Math.random()*30).toFixed(0)} MB/s</div>`;
break;
case'area':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="area"></canvas><div class="metric-label">${(500+Math.random()*1500).toFixed(0)} req/s</div>`;
break;
case'timer':
const d=Math.floor((now()/1000)%86400);const h=Math.floor(d/3600);const m=Math.floor((d%3600)/60);const s=d%60;
body.innerHTML=`<div style="text-align:center"><div class="metric-value" style="color:${p.color}">${h}h ${m}m ${s}s</div><div class="metric-label">Since Last Restart</div><span class="status-dot ok"></span> Healthy</div>`;
break;
case'status':
body.innerHTML=`<div style="display:flex;flex-wrap:wrap;gap:4px;font-size:11px"><span><span class="status-dot ok"></span>API: OK</span><span><span class="status-dot ok"></span>DB: OK</span><span><span class="status-dot warn"></span>Cache: 78%</span><span><span class="status-dot ok"></span>MQ: OK</span></div>`;
break;
case'histogram':
body.innerHTML=`<canvas class="sparkline" data-chart="${pid}" data-type="hist"></canvas><div class="metric-label">Avg: ${(20+Math.random()*60).toFixed(0)}ms | Max: ${(100+Math.random()*200).toFixed(0)}ms</div>`;
break;
}
}
function drawCharts(){
document.querySelectorAll('canvas[data-chart]').forEach(canvas=>{
const ctx=canvas.getContext('2d');
const w=canvas.parentElement.clientWidth-20;
const h=canvas.parentElement.clientHeight-20||40;
canvas.width=w;canvas.height=h;
const type=canvas.dataset.type;
const color=state.panels.get(canvas.dataset.chart)?.color||'#6c8cff';
const points=Array.from({length:20},()=>Math.random());
ctx.clearRect(0,0,w,h);
ctx.strokeStyle=color;
ctx.lineWidth=1.5;
ctx.fillStyle=color+'20';
if(type==='bar'){
const bw=w/points.length-2;
points.forEach((v,i)=>{
ctx.fillStyle=color+'99';
ctx.fillRect(i*(bw+2),h-v*h,bw,v*h);
});
}else if(type==='line'||type==='spark'){
ctx.beginPath();
points.forEach((v,i)=>{const x=(i/(points.length-1))*w;const y=h-v*h;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});
ctx.stroke();
}else if(type==='area'){
ctx.beginPath();
points.forEach((v,i)=>{const x=(i/(points.length-1))*w;const y=h-v*h;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});
ctx.lineTo(w,h);ctx.lineTo(0,h);ctx.closePath();ctx.fill();ctx.stroke();
}else if(type==='dual'){
ctx.strokeStyle='#38bdf8';
ctx.beginPath();points.forEach((v,i)=>{const x=(i/(points.length-1))*w;const y=h-v*h*0.7;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});ctx.stroke();
ctx.strokeStyle='#f472b6';
ctx.beginPath();points.reverse().forEach((v,i)=>{const x=(i/(points.length-1))*w;const y=h-v*h*0.5;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y)});ctx.stroke();
}else if(type==='hist'){
const bw2=w/points.length-1;
points.forEach((v,i)=>{ctx.fillStyle=color+'80';ctx.fillRect(i*(bw2+1),h-v*h*0.8,bw2,v*h*0.8)});
}
});
}
function renderLayout(){
const dashboard=document.getElementById('dashboard');
const existing=new Map();
dashboard.querySelectorAll('.panel').forEach(el=>existing.set(el.dataset.pid,el));
const moreSection=document.createElement('details');
moreSection.className='more-section';
moreSection.innerHTML='<summary>More panels</summary><div class="more-panels"></div>';
let hasCompact=false;
const fragment=document.createDocumentFragment();
const ranked=Object.entries(state.layout).sort((a,b)=>a[1].rank-b[1].rank);
const toRemove=new Set();
document.querySelectorAll('.panel .panel-body canvas').forEach(c=>{const ctx=c.getContext('2d');ctx&&ctx.clearRect(0,0,c.width,c.height)});
for(const[pid,lo] of ranked){
if(lo.tier==='compact'||lo.tier==='mini'){
hasCompact=true;
continue;
}
let el=existing.get(pid);
if(!el){
el=createPanelElement(pid);
}else{
existing.delete(pid);
el.className=`panel ${lo.tier}`+(lo.locked?' locked':'');
const rk=el.querySelector('.panel-rank');if(rk)rk.textContent='#'+(lo.rank+1);
const lb=el.querySelector('.btn-lock');if(lb){lb.className='btn-lock'+(lo.locked?' active':'');lb.textContent=lo.locked?'L':'L';}
}
fragment.appendChild(el);
}
existing.forEach(el=>el.remove());
if(hasCompact){
const moreDiv=moreSection.querySelector('.more-panels');
moreDiv.innerHTML='';
for(const[pid,lo]of ranked){
if(lo.tier!=='compact'&&lo.tier!=='mini')continue;
let el=existing.get(pid);
if(!el){
el=createPanelElement(pid);
}
el.className=`panel ${lo.tier}`+(lo.locked?' locked':'');
moreDiv.appendChild(el);
}
dashboard.appendChild(moreSection);
}
dashboard.innerHTML='';
dashboard.appendChild(fragment);
if(hasCompact)dashboard.appendChild(moreSection);
document.querySelectorAll('.panel-body').forEach(b=>{
const pid=b.dataset.panelBody;
if(pid)renderPanelBody(pid);
});
drawCharts();
}
function updateBadges(){
let totalEvents=0;
for(const d of state.tracking.values())totalEvents+=d.interactions;
document.getElementById('event-count').textContent=totalEvents+' events';
document.getElementById('sort-count').textContent=state.changeCount+'Δ';
}
function persistState(){
const data={tracking:Array.from(state.tracking.entries()),overrides:state.overrides,layout:state.layout,lastSort:state.lastSort,changeCount:state.changeCount};
try{localStorage.setItem(LS_KEY,JSON.stringify(data))}catch(e){}
}
const persistDebounced=debounce(persistState,CONF.debounceMs);
function loadState(){
try{
const raw=localStorage.getItem(LS_KEY);
if(!raw)return false;
const data=JSON.parse(raw);
if(data.tracking)state.tracking=new Map(data.tracking);
if(data.overrides)state.overrides=data.overrides;
if(data.layout)state.layout=data.layout;
if(data.lastSort)state.lastSort=data.lastSort;
if(data.changeCount!=null)state.changeCount=data.changeCount;
return true;
}catch(e){return false}
}
function setupViewTracking(){
if(state.viewObservers.size>0){
state.viewObservers.forEach(o=>o.disconnect());
state.viewObservers.clear();
}
const observer=new IntersectionObserver((entries)=>{
entries.forEach(entry=>{
const pid=entry.target.dataset.pid;
if(!pid)return;
initTracking(pid);
if(entry.isIntersecting){
const interval=setInterval(()=>{
const t=state.tracking.get(pid);
if(t)t.viewDuration+=CONF.viewDurationInterval;
},CONF.viewDurationInterval);
state.viewObservers.set(pid+'_interval',interval);
entry.target.dataset.viewStart=now();
}else{
const iv=state.viewObservers.get(pid+'_interval');
if(iv){clearInterval(iv);state.viewObservers.delete(pid+'_interval')}
const start=parseInt(entry.target.dataset.viewStart);
if(start)state.tracking.get(pid).viewDuration+=now()-start;
}
persistDebounced();
});
},{threshold:0.3});
state.viewObservers.set('observer',observer);
return observer;
}
function observePanels(observer){
document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
}
function handleDashboardClick(e){
const btn=e.target.closest('button[data-action]');
if(!btn)return;
const panel=btn.closest('.panel');
if(!panel)return;
const pid=panel.dataset.pid;
switch(btn.dataset.action){
case'lock':
state.overrides[pid]=state.overrides[pid]?null:Object.assign({},state.layout[pid]);
if(!state.overrides[pid])delete state.overrides[pid];
recordInteraction(pid,'lock');
debouncedResort();
persistDebounced();
break;
case'toggle':
const lo=state.layout[pid];
if(!lo)return;
if(lo.tier==='mini'){lo.tier='normal';recordInteraction(pid,'expand')}
else if(lo.tier==='compact'){lo.tier='normal';recordInteraction(pid,'expand')}
else{lo.tier='mini';recordInteraction(pid,'collapse')}
renderLayout();
persistDebounced();
break;
}
}
const handleScrollThrottled=throttle(()=>{},CONF.throttleMs);
const handleResizeDebounced=debounce(()=>{drawCharts()},CONF.debounceMs);
function setupGlobalListeners(){
const oldClick=state._clickHandler;
if(oldClick)document.getElementById('dashboard').removeEventListener('click',oldClick);
state._clickHandler=handleDashboardClick;
document.getElementById('dashboard').addEventListener('click',handleDashboardClick);
window.addEventListener('resize',handleResizeDebounced,{passive:true});
document.addEventListener('scroll',handleScrollThrottled,{passive:true});
}
function handleDragStart(e){
const panel=e.target.closest('.panel');
if(!panel)return;
state.dragging=panel.dataset.pid;
panel.classList.add('dragging');
e.dataTransfer.effectAllowed='move';
e.dataTransfer.setData('text/plain',panel.dataset.pid);
}
function handleDragOver(e){
e.preventDefault();
const panel=e.target.closest('.panel');
if(!panel||panel.dataset.pid===state.dragging)return;
e.dataTransfer.dropEffect='move';
if(state.dragOver)state.dragOver.classList.remove('drag-over');
panel.classList.add('drag-over');
state.dragOver=panel;
}
function handleDragLeave(e){
if(state.dragOver&&!state.dragOver.contains(e.relatedTarget)){
state.dragOver.classList.remove('drag-over');
state.dragOver=null;
}
}
function handleDrop(e){
e.preventDefault();
if(state.dragOver)state.dragOver.classList.remove('drag-over');
const targetPid=state.dragOver?.dataset.pid;
const sourcePid=state.dragging;
if(!targetPid||!sourcePid||targetPid===sourcePid){state.dragging=null;state.dragOver=null;return}
const srcLo=state.layout[sourcePid];
const tgtLo=state.layout[targetPid];
if(srcLo&&tgtLo){
const tmpRank=srcLo.rank;
srcLo.rank=tgtLo.rank;
tgtLo.rank=tmpRank;
state.overrides[sourcePid]={tier:srcLo.tier,rank:srcLo.rank};
state.overrides[targetPid]={tier:tgtLo.tier,rank:tgtLo.rank};
recordInteraction(sourcePid,'drag');
recordInteraction(targetPid,'drag');
}
state.dragging=null;state.dragOver=null;
maybeResort(true);
persistDebounced();
}
function handleDragEnd(e){
if(state.dragOver)state.dragOver.classList.remove('drag-over');
document.querySelectorAll('.panel.dragging').forEach(el=>el.classList.remove('dragging'));
state.dragging=null;state.dragOver=null;
}
function setupDragListeners(){
const db=document.getElementById('dashboard');
db.addEventListener('dragstart',handleDragStart);
db.addEventListener('dragover',handleDragOver);
db.addEventListener('dragleave',handleDragLeave);
db.addEventListener('drop',handleDrop);
db.addEventListener('dragend',handleDragEnd);
}
function initialize(){
panels.forEach(p=>{
state.panels.set(p.id,{id:p.id,title:p.title,type:p.type,icon:p.icon,color:p.color});
initTracking(p.id);
});
const loaded=loadState();
if(!loaded){
const ranked=rankAll();
applyLayout(ranked);
persistState();
}
state.changeCount=CONF.sortThreshold;
renderLayout();
setupGlobalListeners();
const observer=setupViewTracking();
observePanels(observer);
setupDragListeners();
updateBadges();
document.getElementById('btn-reset-layout').addEventListener('click',()=>{
state.tracking.clear();
state.overrides={};
state.layout={};
state.changeCount=CONF.sortThreshold;
panels.forEach(p=>{state.panels.set(p.id,{id:p.id,title:p.title,type:p.type,icon:p.icon,color:p.color});initTracking(p.id)});
const ranked=rankAll();
applyLayout(ranked);
renderLayout();
updateBadges();
localStorage.removeItem(LS_KEY);
});
document.getElementById('btn-force-sort').addEventListener('click',()=>{
maybeResort(true);
renderLayout();
updateBadges();
persistDebounced();
});
document.getElementById('btn-export').addEventListener('click',()=>{
const exp={tracking:Object.fromEntries(state.tracking),overrides:state.overrides,layout:state.layout,timestamp:now()};
const blob=new Blob([JSON.stringify(exp,null,2)],{type:'application/json'});
const url=URL.createObjectURL(blob);
const a=document.createElement('a');a.href=url;a.download='dashboard-tracking.json';a.click();URL.revokeObjectURL(url);
});
const refreshInterval=setInterval(()=>{
renderPanelBodies();
drawCharts();
},5000);
const observer2=new MutationObserver(()=>{
const observer=state.viewObservers.get('observer');
if(observer)observePanels(observer);
});
observer2.observe(document.getElementById('dashboard'),{childList:true,subtree:true});
}
function renderPanelBodies(){
document.querySelectorAll('[data-panel-body]').forEach(b=>renderPanelBody(b.dataset.panelBody));
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);
else initialize();
})();
</script>
</body>
</html>