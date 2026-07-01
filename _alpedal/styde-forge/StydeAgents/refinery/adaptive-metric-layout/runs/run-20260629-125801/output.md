<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh}
header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:#161b22;border-bottom:1px solid #30363d}
h1{font-size:16px;font-weight:600;color:#f0f6fc}
.controls{display:flex;gap:8px}
.btn{background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:background .15s}
.btn:hover{background:#30363d}
.btn.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.dashboard{display:grid;gap:12px;padding:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));transition:grid-template-columns .4s ease,grid-template-rows .4s ease}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;transition:all .35s ease;position:relative;contain:layout style paint}
.panel.dominant{grid-column:span 2;grid-row:span 2}
.panel.compact{max-height:140px;opacity:.75}
.panel.compact .panel-body{display:none}
.panel.collapsed{max-height:52px;opacity:.5}
.panel.collapsed .panel-body{display:none}
.panel.collapsed .panel-meta{display:none}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#1c2128;border-bottom:1px solid #30363d;cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:13px;font-weight:600;color:#f0f6fc;display:flex;align-items:center;gap:6px}
.panel-score{font-size:10px;color:#8b949e;background:#21262d;padding:2px 8px;border-radius:10px}
.panel-rank{font-size:10px;color:#58a6ff;background:rgba(88,166,255,.12);padding:2px 8px;border-radius:10px}
.panel-actions{display:flex;gap:4px;align-items:center}
.icon-btn{background:none;border:none;color:#8b949e;cursor:pointer;padding:4px 6px;border-radius:4px;font-size:14px;line-height:1;transition:all .15s}
.icon-btn:hover{color:#f0f6fc;background:#30363d}
.icon-btn.locked{color:#d29922}
.icon-btn.collapsed-icon{transform:rotate(180deg)}
.panel-body{padding:14px;font-size:12px;color:#8b949e;min-height:60px;overflow:hidden}
.metric{display:flex;align-items:flex-end;gap:4px;margin-bottom:8px}
.metric-value{font-size:28px;font-weight:700;color:#f0f6fc;line-height:1}
.metric-unit{font-size:12px;color:#8b949e;padding-bottom:4px}
.metric-label{font-size:11px;color:#8b949e}
.sparkline{width:100%;height:40px;margin-top:8px}
.sparkline svg{width:100%;height:100%}
.panel-meta{display:flex;gap:12px;padding:0 14px 10px;font-size:10px;color:#484f58}
.panel-meta span{display:flex;align-items:center;gap:3px}
.compact-preview{display:none;padding:10px 14px;font-size:11px;color:#8b949e}
.panel.compact .compact-preview{display:flex;align-items:center;gap:8px}
.compact-spark{height:24px;width:80px}
.compact-val{font-weight:600;color:#f0f6fc}
.toast{position:fixed;bottom:20px;right:20px;background:#238636;color:#fff;padding:10px 18px;border-radius:8px;font-size:12px;z-index:1000;opacity:0;transform:translateY(10px);transition:all .3s ease;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
@media(max-width:600px){.dashboard{grid-template-columns:1fr!important}.panel.dominant{grid-column:span 1;grid-row:span 1}}
</style>
</head>
<body>
<header>
<h1>Adaptive Metrics</h1>
<div class="controls">
<button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
<button class="btn active" id="btnAuto" title="Auto-layout enabled">Auto</button>
</div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
const STORAGE_KEY='adaptive_metrics_layout';
const DEBOUNCE_MS=300;
const COMPACT_THRESHOLD=0.15;
const COLLAPSE_THRESHOLD=0.05;
const DOMINANT_CUTOFF=3;
const DECAY_HALF_LIFE=86400000;
let panels=[];
let tracking={};
let observer=null;
let autoLayout=true;
const defaultPanels=[
{id:'cpu',title:'CPU Usage',unit:'%',color:'#58a6ff',range:[0,100]},
{id:'memory',title:'Memory',unit:'GB',color:'#3fb950',range:[0,32]},
{id:'requests',title:'Requests/s',unit:'rps',color:'#d29922',range:[0,5000]},
{id:'latency',title:'P95 Latency',unit:'ms',color:'#f78166',range:[0,200]},
{id:'errors',title:'Error Rate',unit:'%',color:'#f85149',range:[0,10]},
{id:'throughput',title:'Throughput',unit:'MB/s',color:'#a371f7',range:[0,1000]},
{id:'connections',title:'Connections',unit:'',color:'#79c0ff',range:[0,500]},
{id:'disk',title:'Disk I/O',unit:'MB/s',color:'#7ee787',range:[0,500]},
];
function loadState(){
try{
const raw=localStorage.getItem(STORAGE_KEY);
if(raw){
const state=JSON.parse(raw);
if(state.tracking)tracking=state.tracking;
if(state.autoLayout!==undefined)autoLayout=state.autoLayout;
const btnAuto=document.getElementById('btnAuto');
btnAuto.textContent=autoLayout?'Auto':'Manual';
btnAuto.className='btn'+(autoLayout?' active':'');
}
}catch(e){}
}
let saveTimer=null;
function persistState(){
if(saveTimer)clearTimeout(saveTimer);
saveTimer=setTimeout(()=>{
const state={
tracking:tracking,
autoLayout:autoLayout,
panels:panels.map(p=>({id:p.id,locked:p.locked,order:p.order}))
};
try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}catch(e){}
},DEBOUNCE_MS);
}
function showToast(msg){
const t=document.getElementById('toast');
t.textContent=msg;
t.classList.add('show');
setTimeout(()=>t.classList.remove('show'),1800);
}
function generateValue(panel,timestamp){
const seed=hashCode(panel.id+Math.floor(timestamp/5000));
const range=panel.range||[0,100];
const base=range[0]+(range[1]-range[0])*0.4;
const amplitude=(range[1]-range[0])*0.3;
const noise=Math.sin(seed*0.1+timestamp*0.001)*amplitude;
const jitter=(Math.random()-0.5)*amplitude*0.3;
return Math.round(Math.max(range[0],Math.min(range[1],base+noise+jitter))*10)/10;
}
function hashCode(s){
let h=0;
for(let i=0;i<s.length;i++){h=((h<<5)-h)+s.charCodeAt(i);h|=0;}
return Math.abs(h);
}
function computeAttentionScore(panelId,now){
const t=tracking[panelId]||{views:0,totalDuration:0,lastViewed:0,frequency:0};
if(t.views===0)return 0;
const recency=Math.exp(-(now-t.lastViewed)/DECAY_HALF_LIFE);
const freqNorm=Math.log(1+t.views);
const durNorm=Math.log(1+t.totalDuration/1000);
return freqNorm*durNorm*recency;
}
function rankPanels(now){
const scored=defaultPanels.map(p=>({
...p,
score:computeAttentionScore(p.id,now),
locked:false,
order:Infinity
}));
const saved=panels;
saved.forEach(sp=>{
const idx=scored.findIndex(p=>p.id===sp.id);
if(idx>=0){
scored[idx].locked=sp.locked||false;
scored[idx].order=sp.order;
}
});
scored.sort((a,b)=>{
if(a.locked&&b.locked)return (a.order||0)-(b.order||0);
if(a.locked)return -1;
if(b.locked)return 1;
return b.score-a.score;
});
const maxScore=scored.length>0?Math.max(...scored.map(p=>p.score),0.001):0.001;
scored.forEach((p,i)=>{
p.rank=i+1;
p.normScore=maxScore>0?p.score/maxScore:0;
p.compact=p.normScore<COMPACT_THRESHOLD&&!p.locked;
p.collapsed=p.normScore<COLLAPSE_THRESHOLD&&!p.locked;
p.dominant=p.rank<=DOMINANT_CUTOFF&&!p.compact&&!p.collapsed;
});
return scored;
}
function generateSparklinePath(panel){
const now=Date.now();
const points=[];
const count=20;
for(let i=count-1;i>=0;i--){
const t=now-(i*2000);
points.push(generateValue(panel,t));
}
const min=Math.min(...points);
const max=Math.max(...points);
const range=max-min||1;
const w=200,h=40;
const px=1;
return points.map((v,i)=>{
const x=(i/(count-1))*(w-2)+1;
const y=h-1-((v-min)/range)*(h-2);
return(i===0?'M':'L')+x.toFixed(1)+' '+y.toFixed(1);
}).join(' ');
}
function buildPanelHTML(panel){
const val=generateValue(panel,Date.now());
const sparkPath=generateSparklinePath(panel);
const cls=['panel'];
if(panel.dominant)cls.push('dominant');
if(panel.compact)cls.push('compact');
if(panel.collapsed)cls.push('collapsed');
const lockIcon=panel.locked?'🔒':'🔓';
const collapseIcon=panel.collapsed?'▸':'▾';
const rankBadge=panel.rank<=DOMINANT_CUTOFF?`<span class="panel-rank">#${panel.rank}</span>`:'';
return'<div class="'+cls.join(' ')+'" data-panel-id="'+panel.id+'">'+
'<div class="panel-header">'+
'<div class="panel-title">'+panel.title+rankBadge+
'<span class="panel-score">'+(panel.score>0?panel.score.toFixed(1):'new')+'</span></div>'+
'<div class="panel-actions">'+
'<button class="icon-btn toggle-btn" data-action="toggle" title="Expand/Collapse">'+collapseIcon+'</button>'+
'<button class="icon-btn lock-btn'+(panel.locked?' locked':'')+'" data-action="lock" title="'+(panel.locked?'Unlock':'Lock')+' position">'+lockIcon+'</button>'+
'</div></div>'+
'<div class="compact-preview"><svg class="compact-spark" viewBox="0 0 200 40"><path d="'+sparkPath+'" fill="none" stroke="'+panel.color+'" stroke-width="1.5"/></svg><span class="compact-val">'+val+panel.unit+'</span></div>'+
'<div class="panel-body">'+
'<div class="metric"><span class="metric-value">'+val+'</span><span class="metric-unit">'+panel.unit+'</span></div>'+
'<div class="metric-label">Current</div>'+
'<div class="sparkline"><svg viewBox="0 0 200 40" preserveAspectRatio="none"><path d="'+sparkPath+'" fill="none" stroke="'+panel.color+'" stroke-width="2" vector-effect="non-scaling-stroke"/></svg></div>'+
'</div>'+
'<div class="panel-meta"><span>👁 '+(tracking[panel.id]?tracking[panel.id].views:0)+' views</span><span>⏱ '+(tracking[panel.id]?Math.round(tracking[panel.id].totalDuration/1000):0)+'s</span></div>'+
'</div>';
}
function renderDashboard(panelsToRender){
requestAnimationFrame(()=>{
const container=document.getElementById('dashboard');
container.innerHTML=panelsToRender.map(buildPanelHTML).join('');
bindPanelEvents(container);
observePanels();
});
}
function bindPanelEvents(container){
container.querySelectorAll('.panel').forEach(el=>{
const id=el.dataset.panelId;
el.querySelector('[data-action="toggle"]').addEventListener('click',(e)=>{
e.stopPropagation();
const panel=panels.find(p=>p.id===id);
if(!panel)return;
if(panel.collapsed){
panel.collapsed=false;
panel.compact=panel.normScore<COMPACT_THRESHOLD&&!panel.locked&&panel.rank>DOMINANT_CUTOFF;
}else if(panel.compact){
panel.collapsed=true;
panel.compact=false;
}else{
panel.compact=true;
}
showToast(panel.collapsed?id+' collapsed':panel.compact?id+' compacted':id+' expanded');
requestAnimationFrame(()=>updatePanelDOM(el,panel));
persistState();
});
el.querySelector('[data-action="lock"]').addEventListener('click',(e)=>{
e.stopPropagation();
const panel=panels.find(p=>p.id===id);
if(!panel)return;
panel.locked=!panel.locked;
if(panel.locked)panel.order=panels.indexOf(panel);
panel.compact=false;
panel.collapsed=false;
showToast(panel.locked?id+' locked':id+' unlocked');
refreshAll();
});
});
}
function updatePanelDOM(el,panel){
el.className='panel'+(panel.dominant?' dominant':'')+(panel.compact?' compact':'')+(panel.collapsed?' collapsed':'');
const lockBtn=el.querySelector('.lock-btn');
if(lockBtn){
lockBtn.className='icon-btn lock-btn'+(panel.locked?' locked':'');
lockBtn.textContent=panel.locked?'🔒':'🔓';
lockBtn.title=(panel.locked?'Unlock':'Lock')+' position';
}
const toggleBtn=el.querySelector('.toggle-btn');
if(toggleBtn){
toggleBtn.textContent=panel.collapsed?'▸':'▾';
}
}
function observePanels(){
if(observer)observer.disconnect();
const visiblePanels=new Set();
observer=new IntersectionObserver((entries)=>{
entries.forEach(entry=>{
const id=entry.target.dataset.panelId;
if(entry.isIntersecting){
if(!visiblePanels.has(id)){
visiblePanels.add(id);
startTrackingView(id);
}
}else{
if(visiblePanels.has(id)){
visiblePanels.delete(id);
stopTrackingView(id);
}
}
});
},{threshold:0.3});
document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
}
const activeViews={};
function startTrackingView(id){
if(!tracking[id])tracking[id]={views:0,totalDuration:0,lastViewed:0,frequency:0};
tracking[id].views++;
tracking[id].frequency=tracking[id].views;
tracking[id].lastViewed=Date.now();
activeViews[id]=Date.now();
}
function stopTrackingView(id){
if(activeViews[id]){
const dur=Date.now()-activeViews[id];
if(!tracking[id])tracking[id]={views:0,totalDuration:0,lastViewed:0,frequency:0};
tracking[id].totalDuration+=dur;
tracking[id].lastViewed=Date.now();
delete activeViews[id];
persistState();
}
}
let refreshInterval=null;
function refreshAll(){
const now=Date.now();
panels=rankPanels(now);
renderDashboard(panels);
persistState();
}
function startAutoRefresh(){
if(refreshInterval)clearInterval(refreshInterval);
refreshInterval=setInterval(()=>{
const now=Date.now();
panels.forEach(p=>{
if(activeViews[p.id]){
if(!tracking[p.id])tracking[p.id]={views:0,totalDuration:0,lastViewed:0,frequency:0};
tracking[p.id].totalDuration+=2000;
tracking[p.id].lastViewed=now;
}
});
panels=rankPanels(now);
requestAnimationFrame(()=>{
const container=document.getElementById('dashboard');
panels.forEach(p=>{
const el=container.querySelector('[data-panel-id="'+p.id+'"]');
if(el)updatePanelDOM(el,p);
});
const sparkEls=container.querySelectorAll('.sparkline svg path,.compact-spark path');
sparkEls.forEach(el=>{
const panelEl=el.closest('.panel');
if(panelEl){
const id=panelEl.dataset.panelId;
const panel=panels.find(p=>p.id===id);
if(panel)el.setAttribute('d',generateSparklinePath(panel));
}
});
persistState();
});
},2000);
}
document.getElementById('btnReset').addEventListener('click',()=>{
tracking={};
panels=[];
Object.keys(activeViews).forEach(k=>delete activeViews[k]);
localStorage.removeItem(STORAGE_KEY);
autoLayout=true;
document.getElementById('btnAuto').textContent='Auto';
document.getElementById('btnAuto').className='btn active';
refreshAll();
showToast('Tracking reset');
});
document.getElementById('btnAuto').addEventListener('click',function(){
autoLayout=!autoLayout;
this.textContent=autoLayout?'Auto':'Manual';
this.className='btn'+(autoLayout?' active':'');
showToast(autoLayout?'Auto-layout enabled':'Manual mode - locks preserved');
persistState();
});
let resizeTimer=null;
window.addEventListener('resize',()=>{
if(resizeTimer)clearTimeout(resizeTimer);
resizeTimer=setTimeout(refreshAll,150);
});
window.addEventListener('beforeunload',()=>{
Object.keys(activeViews).forEach(id=>stopTrackingView(id));
persistState();
});
loadState();
const now=Date.now();
panels=rankPanels(now);
document.getElementById('btnAuto').textContent=autoLayout?'Auto':'Manual';
document.getElementById('btnAuto').className='btn'+(autoLayout?' active':'');
renderDashboard(panels);
startAutoRefresh();
})();
</script>
</body>
</html>