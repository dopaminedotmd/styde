<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
--bg:#0f1117;--surface:#1a1d27;--surface2:#22262f;--border:#2a2e3a;
--text:#c8ccd4;--text2:#8b8fa8;--accent:#5b8def;--accent2:#7c5ce7;
--warn:#e8a840;--good:#40c9a2;--bad:#e85d5d;--lock:#ffd166;
--radius:12px;--gap:12px;--header-h:56px;--transition:0.35s cubic-bezier(0.22,0.61,0.36,1);
}
body{
font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--text);
min-height:100vh;overflow-x:hidden;
}
header{
height:var(--header-h);display:flex;align-items:center;justify-content:space-between;
padding:0 20px;background:var(--surface);border-bottom:1px solid var(--border);
position:sticky;top:0;z-index:100;
}
header h1{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em}
header .controls{display:flex;gap:8px;align-items:center}
.btn{
padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:var(--surface2);
color:var(--text);cursor:pointer;font-size:0.82rem;transition:all 0.2s;white-space:nowrap;
}
.btn:hover{background:var(--border);border-color:var(--text2)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn .kbd{font-size:0.65rem;opacity:0.6;margin-left:4px}
.dashboard{
display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
gap:var(--gap);padding:var(--gap);transition:all var(--transition);
max-width:1600px;margin:0 auto;
}
.dashboard.compact-mode{gap:6px}
.panel{
background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
overflow:hidden;display:flex;flex-direction:column;transition:all var(--transition);
position:relative;min-height:160px;
}
.panel.high-rank{border-color:color-mix(in srgb,var(--accent) 40%,transparent);box-shadow:0 0 20px rgba(91,141,239,0.08)}
.panel.compact{min-height:56px;height:56px}
.panel.dragging{opacity:0.7;z-index:50;box-shadow:0 8px 32px rgba(0,0,0,0.4);cursor:grabbing}
.panel.drag-over{border-color:var(--accent);border-style:dashed}
.panel-header{
display:flex;align-items:center;justify-content:space-between;padding:10px 14px;
background:var(--surface2);border-bottom:1px solid var(--border);cursor:grab;
user-select:none;gap:8px;min-height:44px;
}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:0.88rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .meta{display:flex;gap:4px;align-items:center;flex-shrink:0}
.rank-badge{
font-size:0.65rem;padding:2px 7px;border-radius:20px;font-weight:600;
background:var(--surface);color:var(--text2);
}
.panel.high-rank .rank-badge{background:color-mix(in srgb,var(--accent) 15%,transparent);color:var(--accent)}
.icon-btn{
width:28px;height:28px;border-radius:6px;border:none;background:transparent;
color:var(--text2);cursor:pointer;display:flex;align-items:center;justify-content:center;
font-size:0.85rem;transition:all 0.15s;
}
.icon-btn:hover{background:var(--border);color:var(--text)}
.icon-btn.locked{color:var(--lock);background:color-mix(in srgb,var(--lock) 15%,transparent)}
.panel-body{
flex:1;padding:14px;display:flex;flex-direction:column;gap:8px;overflow:hidden;
transition:all var(--transition);
}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{border-bottom:none}
.metric-value{font-size:2rem;font-weight:700;line-height:1;letter-spacing:-0.02em}
.metric-label{font-size:0.75rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.04em}
.metric-delta{font-size:0.8rem;font-weight:600}
.metric-delta.up{color:var(--good)}
.metric-delta.down{color:var(--bad)}
.sparkline{width:100%;height:40px;margin-top:4px}
.mini-chart{width:100%;height:32px}
.heat-bar{
height:3px;border-radius:3px;background:var(--border);overflow:hidden;margin-top:4px;
}
.heat-bar-fill{height:100%;border-radius:3px;background:var(--accent);transition:width 0.8s ease}
.usage-stats{font-size:0.68rem;color:var(--text2);display:flex;gap:12px;margin-top:auto;padding-top:4px}
.usage-stats span{white-space:nowrap}
.toast{
position:fixed;bottom:20px;right:20px;padding:10px 18px;border-radius:10px;
background:var(--surface2);border:1px solid var(--border);color:var(--text);
font-size:0.82rem;z-index:200;opacity:0;transform:translateY(10px);transition:all 0.3s;
pointer-events:none;
}
.toast.show{opacity:1;transform:translateY(0)}
.reset-section{
padding:var(--gap);max-width:1600px;margin:0 auto;display:flex;gap:8px;justify-content:flex-end;
}
@media(max-width:640px){
.dashboard{grid-template-columns:1fr;gap:8px;padding:8px}
.panel{min-height:120px}
.panel.compact{min-height:48px;height:48px}
.metric-value{font-size:1.6rem}
header{padding:0 12px}
header h1{font-size:0.95rem}
.icon-btn{width:36px;height:36px}
.panel-header{padding:8px 10px;min-height:44px}
}
</style>
</head>
<body>
<header>
<h1>Adaptive Dashboard</h1>
<div class="controls">
<button class="btn" id="btnCompact" title="Toggle compact mode for low-rank panels">Compact</button>
<button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
</div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="reset-section">
<button class="btn" id="btnResetLayout">Reset Layout</button>
<button class="btn" id="btnResetTracking">Reset Tracking</button>
</div>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY = 'adaptive_dashboard_v1';
const PANEL_DEFS = [
{id:'revenue',title:'Revenue',value:'$',rawVal:()=>Math.round(12000+Math.random()*8000),prefix:'$',fmt:'currency',delta:()=>(Math.random()-0.45)*12,color:'var(--good)'},
{id:'users',title:'Active Users',value:'',rawVal:()=>Math.round(2400+Math.random()*1600),prefix:'',fmt:'number',delta:()=>(Math.random()-0.4)*18,color:'var(--accent)'},
{id:'latency',title:'API Latency',value:'',rawVal:()=>Math.round(45+Math.random()*70),prefix:'',fmt:'ms',delta:()=>(Math.random()-0.55)*25,color:'var(--warn)'},
{id:'errors',title:'Error Rate',value:'',rawVal:()=>+(Math.random()*2.8).toFixed(2),prefix:'',fmt:'pct',delta:()=>(Math.random()-0.6)*1.2,color:'var(--bad)'},
{id:'bandwidth',title:'Bandwidth',value:'',rawVal:()=>Math.round(80+Math.random()*200),prefix:'',fmt:'mbps',delta:()=>(Math.random()-0.5)*35,color:'var(--accent2)'},
{id:'cpu',title:'CPU Usage',value:'',rawVal:()=>Math.round(20+Math.random()*55),prefix:'',fmt:'pct',delta:()=>(Math.random()-0.5)*20,color:'var(--warn)'},
{id:'memory',title:'Memory',value:'',rawVal:()=>Math.round(40+Math.random()*35),prefix:'',fmt:'pct',delta:()=>(Math.random()-0.45)*15,color:'var(--accent)'},
{id:'requests',title:'Requests/min',value:'',rawVal:()=>Math.round(500+Math.random()*3500),prefix:'',fmt:'number',delta:()=>(Math.random()-0.5)*450,color:'var(--good)'},
];
let state = loadState();
let observers = [];
let visibilityByPanel = {};
let interactionCounts = {};
let panelTimers = {};
let draggedEl = null;
let dragGhost = null;
function loadState(){
try{
const raw = localStorage.getItem(STORAGE_KEY);
if(raw){
const s = JSON.parse(raw);
if(s.panels&&Array.isArray(s.panels)&&s.panels.length===PANEL_DEFS.length)return s;
}
}catch(e){}
return defaultState();
}
function defaultState(){
const now = Date.now();
return{
panels:PANEL_DEFS.map((d,i)=>({
id:d.id,
locked:false,
order:i,
compactOverride:false,
tracking:{views:0,totalDuration:0,lastInteraction:now,collapses:0,expands:0,lastViewed:now},
sparkline:Array.from({length:20},()=>d.rawVal()),
})),
compactMode:false,
};
}
function saveState(){
try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}catch(e){}
}
function getPanelDef(id){return PANEL_DEFS.find(d=>d.id===id)}
function getPanelState(id){return state.panels.find(p=>p.id===id)}
function computeScore(ps){
const now = Date.now();
const recencyHours = Math.max(0.1,(now-ps.tracking.lastInteraction)/(1000*60*60));
const recency = 1/(1+recencyHours);
const durationMinutes = ps.tracking.totalDuration/60000;
const freqBonus = Math.log2(1+ps.tracking.views);
const interactionScore = Math.log2(1+ps.tracking.collapses+ps.tracking.expands);
return (freqBonus*0.4 + durationMinutes*0.35 + recency*0.15 + interactionScore*0.1);
}
function rankPanels(){
const scores = state.panels.map((ps,i)=>({idx:i,score:computeScore(ps)}));
scores.sort((a,b)=>b.score-a.score);
scores.forEach((s,rank)=>state.panels[s.idx].rank=rank);
scores.forEach((s,rank)=>state.panels[s.idx].order=rank);
}
function applyLocks(){
const locked = state.panels.filter(p=>p.locked).sort((a,b)=>a.order-b.order);
const unlocked = state.panels.filter(p=>!p.locked).sort((a,b)=>a.rank-b.rank);
let li=0,ui=0;
const result = [];
for(let i=0;i<state.panels.length;i++){
const lp=locked.find(p=>p.order===i);
if(lp){result[i]=lp;li++}
else{result[i]=unlocked[ui++]}
}
result.forEach((p,i)=>{if(!p.locked)p.order=i});
}
function layoutPanels(){
rankPanels();
applyLocks();
const container = document.getElementById('dashboard');
const sorted = [...state.panels].sort((a,b)=>a.order-b.order);
const fragment = document.createDocumentFragment();
sorted.forEach(ps=>{
const el = container.querySelector(`[data-panel-id="${ps.id}"]`);
if(el)fragment.appendChild(el);
});
container.appendChild(fragment);
sorted.forEach((ps,i)=>{
const el = container.querySelector(`[data-panel-id="${ps.id}"]`);
if(!el)return;
const rankClass = ps.rank<3?'high-rank':'';
const compactClass = (state.compactMode||ps.compactOverride)&&ps.rank>=5?'compact':'';
el.className = `panel ${rankClass} ${compactClass}`.trim();
el.style.order = i;
el.querySelector('.rank-badge').textContent = `#${ps.rank+1}`;
});
updateHeatBars();
saveState();
}
function updateHeatBars(){
const maxScore = Math.max(...state.panels.map(p=>computeScore(p)),0.01);
state.panels.forEach(ps=>{
const el = document.querySelector(`[data-panel-id="${ps.id}"]`);
if(!el)return;
const fill = el.querySelector('.heat-bar-fill');
if(fill)fill.style.width = `${(computeScore(ps)/maxScore*100).toFixed(0)}%`;
});
}
function createPanel(ps){
const def = getPanelDef(ps.id);
const el = document.createElement('div');
el.className = 'panel';
el.setAttribute('data-panel-id',ps.id);
el.draggable = false;
el.innerHTML = `
<div class="panel-header">
<span class="title">${def.title}</span>
<div class="meta">
<span class="rank-badge">#${ps.rank+1}</span>
<button class="icon-btn lock-btn${ps.locked?' locked':''}" data-action="lock" title="Lock position">&#128274;</button>
<button class="icon-btn compact-btn${ps.compactOverride?' active':''}" data-action="compact" title="Toggle compact">&#9776;</button>
</div>
</div>
<div class="panel-body">
<div class="metric-value" style="color:${def.color}">--</div>
<div class="metric-label">${def.fmt==='currency'?'USD':def.fmt==='pct'?'Percent':def.fmt==='ms'?'Milliseconds':def.fmt==='mbps'?'Megabits/s':def.fmt==='number'?'Count':''}</div>
<canvas class="sparkline" width="280" height="40"></canvas>
<div class="heat-bar"><div class="heat-bar-fill" style="width:0%"></div></div>
<div class="usage-stats">
<span class="views">Views: 0</span>
<span class="duration">Time: 0s</span>
</div>
</div>
`;
const header = el.querySelector('.panel-header');
header.addEventListener('mousedown',e=>onDragStart(e,ps.id));
header.addEventListener('touchstart',e=>onDragStart(e,ps.id),{passive:false});
el.querySelector('[data-action="lock"]').addEventListener('click',e=>{e.stopPropagation();toggleLock(ps.id)});
el.querySelector('[data-action="compact"]').addEventListener('click',e=>{e.stopPropagation();toggleCompact(ps.id)});
return el;
}
function renderAll(){
rankPanels();
applyLocks();
const container = document.getElementById('dashboard');
const existing = new Map();
container.querySelectorAll('.panel').forEach(el=>existing.set(el.getAttribute('data-panel-id'),el));
const sorted = [...state.panels].sort((a,b)=>a.order-b.order);
const fragment = document.createDocumentFragment();
sorted.forEach(ps=>{
let el = existing.get(ps.id);
if(!el)el = createPanel(ps);
else existing.delete(ps.id);
const rankClass = ps.rank<3?'high-rank':'';
const compactClass = (state.compactMode||ps.compactOverride)&&ps.rank>=5?'compact':'';
el.className = `panel ${rankClass} ${compactClass}`.trim();
el.style.order = ps.order;
el.querySelector('.rank-badge').textContent = `#${ps.rank+1}`;
const lockBtn = el.querySelector('.lock-btn');
lockBtn.className = `icon-btn lock-btn${ps.locked?' locked':''}`;
const compactBtn = el.querySelector('.compact-btn');
compactBtn.className = `icon-btn compact-btn${ps.compactOverride?' active':''}`;
fragment.appendChild(el);
});
existing.forEach(el=>el.remove());
container.appendChild(fragment);
setupObservers();
updateHeatBars();
saveState();
}
function setupObservers(){
observers.forEach(o=>o.disconnect());
observers=[];
document.querySelectorAll('.panel').forEach(el=>{
const psId = el.getAttribute('data-panel-id');
const observer = new IntersectionObserver(entries=>{
entries.forEach(entry=>{
const wasVisible = visibilityByPanel[psId]||false;
visibilityByPanel[psId] = entry.isIntersecting;
if(entry.isIntersecting&&!wasVisible){
panelTimers[psId] = Date.now();
getPanelState(psId).tracking.views++;
getPanelState(psId).tracking.lastViewed = Date.now();
getPanelState(psId).tracking.lastInteraction = Date.now();
}
if(!entry.isIntersecting&&wasVisible&&panelTimers[psId]){
const dur = Date.now()-panelTimers[psId];
getPanelState(psId).tracking.totalDuration += dur;
panelTimers[psId]=null;
}
});
},{threshold:0.3});
observer.observe(el);
observers.push(observer);
});
}
function toggleLock(id){
const ps = getPanelState(id);
ps.locked = !ps.locked;
showToast(ps.locked?`${getPanelDef(id).title} locked`:`${getPanelDef(id).title} unlocked`);
ps.tracking.lastInteraction = Date.now();
renderAll();
}
function toggleCompact(id){
const ps = getPanelState(id);
ps.compactOverride = !ps.compactOverride;
ps.tracking.lastInteraction = Date.now();
ps.tracking[ps.compactOverride?'collapses':'expands']++;
renderAll();
}
function onDragStart(e,id){
const ps = getPanelState(id);
const el = document.querySelector(`[data-panel-id="${id}"]`);
if(!el)return;
e.preventDefault();
draggedEl = el;
const rect = el.getBoundingClientRect();
dragGhost = el.cloneNode(true);
dragGhost.style.position='fixed';
dragGhost.style.left=rect.left+'px';
dragGhost.style.top=rect.top+'px';
dragGhost.style.width=rect.width+'px';
dragGhost.style.height=rect.height+'px';
dragGhost.style.zIndex='1000';
dragGhost.style.opacity='0.85';
dragGhost.style.pointerEvents='none';
dragGhost.style.transition='none';
document.body.appendChild(dragGhost);
el.classList.add('dragging');
const startX = (e.touches?e.touches[0].clientX:e.clientX)||rect.left;
const startY = (e.touches?e.touches[0].clientY:e.clientY)||rect.top;
const offsetX = startX-rect.left;
const offsetY = startY-rect.top;
const onMove = (ev)=>{
const cx = (ev.touches?ev.touches[0].clientX:ev.clientX);
const cy = (ev.touches?ev.touches[0].clientY:ev.clientY);
dragGhost.style.left=(cx-offsetX)+'px';
dragGhost.style.top=(cy-offsetY)+'px';
document.querySelectorAll('.panel').forEach(p=>p.classList.remove('drag-over'));
const over = document.elementFromPoint(cx,cy)?.closest('.panel');
if(over&&over!==el)over.classList.add('drag-over');
};
const onUp = (ev)=>{
document.removeEventListener('mousemove',onMove);
document.removeEventListener('mouseup',onUp);
document.removeEventListener('touchmove',onMove);
document.removeEventListener('touchend',onUp);
el.classList.remove('dragging');
document.querySelectorAll('.panel').forEach(p=>p.classList.remove('drag-over'));
if(dragGhost){dragGhost.remove();dragGhost=null;}
const cx = (ev.changedTouches?ev.changedTouches[0].clientX:ev.clientX);
const cy = (ev.changedTouches?ev.changedTouches[0].clientY:ev.clientY);
const target = document.elementFromPoint(cx,cy)?.closest('.panel');
if(target&&target!==el){
const targetId = target.getAttribute('data-panel-id');
const fromPs = getPanelState(id);
const toPs = getPanelState(targetId);
const fromOrder = fromPs.order;
fromPs.order = toPs.order;
toPs.order = fromOrder;
fromPs.locked = true;
toPs.locked = true;
fromPs.tracking.lastInteraction = Date.now();
toPs.tracking.lastInteraction = Date.now();
showToast(`${getPanelDef(id).title} swapped with ${getPanelDef(targetId).title} — both locked`);
renderAll();
}else{
ps.tracking.lastInteraction = Date.now();
}
draggedEl=null;
};
document.addEventListener('mousemove',onMove);
document.addEventListener('mouseup',onUp);
document.addEventListener('touchmove',onMove,{passive:false});
document.addEventListener('touchend',onUp);
}
function updateValues(){
const timestamp = Date.now();
state.panels.forEach(ps=>{
const def = getPanelDef(ps.id);
const val = def.rawVal();
const delta = def.delta();
ps.sparkline.push(val);
if(ps.sparkline.length>30)ps.sparkline.shift();
const el = document.querySelector(`[data-panel-id="${ps.id}"]`);
if(!el||el.classList.contains('compact'))return;
const valEl = el.querySelector('.metric-value');
if(!valEl)return;
let display;
if(def.fmt==='currency')display = def.prefix+val.toLocaleString();
else if(def.fmt==='pct')display = val.toFixed(1)+'%';
else if(def.fmt==='ms')display = val+def.fmt;
else if(def.fmt==='mbps')display = val+' '+def.fmt;
else display = val.toLocaleString();
if(valEl.textContent!==display)valEl.textContent=display;
const canvas = el.querySelector('.sparkline');
if(canvas)drawSparkline(canvas,ps.sparkline,def.color);
const viewsEl = el.querySelector('.views');
if(viewsEl)viewsEl.textContent = `Views: ${ps.tracking.views}`;
const durEl = el.querySelector('.duration');
if(durEl){
const sec = Math.round(ps.tracking.totalDuration/1000);
durEl.textContent = `Time: ${sec<60?sec+'s':sec<3600?Math.round(sec/60)+'m':Math.round(sec/3600)+'h'}`;
}
});
updateHeatBars();
const now = Date.now();
state.panels.forEach(ps=>{
if(visibilityByPanel[ps.id]&&panelTimers[ps.id]){
ps.tracking.totalDuration += now-panelTimers[ps.id];
panelTimers[ps.id]=now;
}
});
saveState();
}
function drawSparkline(canvas,data,color){
const dpr = window.devicePixelRatio||1;
const w = canvas.clientWidth;
const h = canvas.clientHeight;
if(canvas.width!==w*dpr||canvas.height!==h*dpr){
canvas.width = w*dpr;
canvas.height = h*dpr;
}
const ctx = canvas.getContext('2d');
ctx.clearRect(0,0,canvas.width,canvas.height);
if(data.length<2)return;
const min = Math.min(...data);
const max = Math.max(...data);
const range = max-min||1;
const stepX = w/(data.length-1);
ctx.beginPath();
ctx.strokeStyle = color;
ctx.lineWidth = 1.5*dpr;
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
data.forEach((v,i)=>{
const x = i*stepX*dpr;
const y = (h-(v-min)/range*h)*dpr;
if(i===0)ctx.moveTo(x,y);
else ctx.lineTo(x,y);
});
ctx.stroke();
const lastX = (data.length-1)*stepX*dpr;
const lastY = (h-(data[data.length-1]-min)/range*h)*dpr;
ctx.beginPath();
ctx.arc(lastX,lastY,2.5*dpr,0,Math.PI*2);
ctx.fillStyle = color;
ctx.fill();
}
function showToast(msg){
const toast = document.getElementById('toast');
toast.textContent = msg;
toast.classList.add('show');
clearTimeout(toast._timeout);
toast._timeout = setTimeout(()=>toast.classList.remove('show'),1800);
}
function resetLayout(){
state.panels.forEach(p=>{p.locked=false;p.compactOverride=false;});
state.compactMode = false;
document.getElementById('btnCompact').classList.remove('active');
renderAll();
showToast('Layout reset');
}
function resetTracking(){
const now = Date.now();
state.panels.forEach(p=>{
p.tracking = {views:0,totalDuration:0,lastInteraction:now,collapses:0,expands:0,lastViewed:now};
p.locked = false;
p.compactOverride = false;
p.order = PANEL_DEFS.findIndex(d=>d.id===p.id);
});
state.compactMode = false;
document.getElementById('btnCompact').classList.remove('active');
renderAll();
showToast('Tracking reset');
}
document.getElementById('btnCompact').addEventListener('click',()=>{
state.compactMode = !state.compactMode;
document.getElementById('btnCompact').classList.toggle('active',state.compactMode);
renderAll();
});
document.getElementById('btnReset').addEventListener('click',resetTracking);
document.getElementById('btnResetLayout').addEventListener('click',resetLayout);
document.getElementById('btnResetTracking').addEventListener('click',resetTracking);
document.addEventListener('keydown',e=>{
if(e.key==='c'&&e.ctrlKey){
e.preventDefault();
state.compactMode = !state.compactMode;
document.getElementById('btnCompact').classList.toggle('active',state.compactMode);
renderAll();
}
});
const observer = new ResizeObserver(()=>{
document.querySelectorAll('.sparkline').forEach(canvas=>{
const psId = canvas.closest('.panel')?.getAttribute('data-panel-id');
if(!psId)return;
const ps = getPanelState(psId);
const def = getPanelDef(psId);
if(ps&&def)drawSparkline(canvas,ps.sparkline,def.color);
});
});
observer.observe(document.getElementById('dashboard'));
renderAll();
updateValues();
setInterval(updateValues,3000);
</script>
</body>
</html>