```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d27;--surface2:#22262f;--border:#2a2e39;--text:#e1e4eb;--text2:#9ca3af;--accent:#6366f1;--accent2:#818cf8;--danger:#ef4444;--warn:#f59e0b;--success:#22c55e;--radius:8px;--transition:200ms ease}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
.toolbar{display:flex;gap:12px;align-items:center;padding:12px 16px;background:var(--surface);border-radius:var(--radius);margin-bottom:16px;flex-wrap:wrap}
.toolbar button{padding:8px 16px;border:1px solid var(--border);background:var(--surface2);color:var(--text);border-radius:6px;cursor:pointer;font-size:13px;transition:background var(--transition)}
.toolbar button:hover{background:var(--border)}
.toolbar button.active{background:var(--accent);border-color:var(--accent)}
.toolbar .spacer{flex:1}
.toolbar .badge{font-size:11px;color:var(--text2);padding:4px 10px;background:var(--surface2);border-radius:12px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));transition:all .4s ease}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .3s ease;position:relative;display:flex;flex-direction:column;min-height:180px}
.panel.compact{min-height:60px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.dragging{opacity:.7;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,.4)}
.panel.locked{border-color:var(--accent)}
.panel-header{display:flex;align-items:center;gap:8px;padding:10px 12px;background:var(--surface2);border-bottom:1px solid var(--border);cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:14px;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .rank-badge{font-size:10px;padding:2px 8px;border-radius:10px;background:var(--accent);color:#fff;font-weight:700}
.panel-header .rank-badge.low{background:var(--surface2);color:var(--text2)}
.panel-header .actions{display:flex;gap:4px}
.panel-header .actions button{background:none;border:none;color:var(--text2);cursor:pointer;padding:4px 6px;border-radius:4px;font-size:13px;line-height:1;transition:all var(--transition)}
.panel-header .actions button:hover{color:var(--text);background:var(--border)}
.panel-header .actions button.lock-btn.locked{color:var(--accent2)}
.panel-body{padding:12px;flex:1;overflow:auto}
.panel-body .metric{font-size:28px;font-weight:700;margin-bottom:4px}
.panel-body .label{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px}
.panel-body .spark{height:40px;margin-top:8px;display:flex;align-items:end;gap:2px}
.panel-body .spark .bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-height:2px;transition:height .3s ease}
.panel-preview{display:none;padding:10px 12px;align-items:center;gap:10px;font-size:12px;color:var(--text2)}
.panel-preview .mini-val{font-weight:700;color:var(--text);font-size:18px}
.panel.drop-target{outline:2px dashed var(--accent);outline-offset:-2px}
.compact-zone{margin-top:12px;padding:10px 12px;background:var(--surface);border:1px dashed var(--border);border-radius:var(--radius);min-height:40px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.compact-zone .zone-label{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;width:100%;margin-bottom:4px}
.compact-zone .panel{min-width:180px;flex:0 0 auto}
.heat-overlay{position:fixed;inset:0;pointer-events:none;z-index:999;opacity:.15}
.heat-cell{position:absolute;border-radius:4px;transition:background .5s ease}
.toast{position:fixed;bottom:20px;right:20px;padding:10px 18px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius);font-size:13px;z-index:1000;opacity:0;transform:translateY(10px);transition:all .3s ease}
.toast.show{opacity:1;transform:translateY(0)}
@media(max-width:640px){.grid{grid-template-columns:1fr}.toolbar{gap:6px}.toolbar button{padding:6px 10px;font-size:12px}}
</style>
</head>
<body>
<div class="toolbar" id="toolbar">
<button onclick="resetLayout()" title="Reset all layout overrides">Reset Layout</button>
<button onclick="toggleHeatmap()" id="heatBtn">Heatmap: Off</button>
<button onclick="addPanel()">+ Add Panel</button>
<span class="spacer"></span>
<span class="badge" id="sessionBadge">Session: --</span>
<span class="badge" id="eventBadge">Events: 0</span>
</div>
<div class="grid" id="grid"></div>
<div class="compact-zone" id="compactZone">
<span class="zone-label">COMPACT / LOW USAGE</span>
</div>
<div class="heat-overlay" id="heatOverlay" style="display:none"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
const LS_KEY='adaptive_dashboard_v1';
const COMPACT_THRESHOLD=0.15;
const RANK_DECAY=0.95;
const SESSION_DURATION_MS=300000;
const FLUSH_INTERVAL_MS=5000;
const SCORE_INTERVAL_MS=10000;
let panels=[];
let panelMeta={};
let trackBuffer={};
let flushTimer=null;
let scoreTimer=null;
let sessionId=Date.now().toString(36);
let draggedEl=null;
let dragSrcIdx=null;
let heatmapOn=false;
let observer=null;
let viewTimers={};
function $(s,d){return(d||document).querySelector(s)}
function $$(s,d){return Array.from((d||document).querySelectorAll(s))}
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show');clearTimeout(t._tid);t._tid=setTimeout(()=>t.classList.remove('show'),2000)}
function loadState(){try{const raw=localStorage.getItem(LS_KEY);if(raw){const s=JSON.parse(raw);panels=s.panels||[];panelMeta=s.meta||{};sessionId=s.sessionId||sessionId;return true}}catch(e){}return false}
function saveState(){const bundle={panels,meta:panelMeta,sessionId};localStorage.setItem(LS_KEY,JSON.stringify(bundle))}
function flushState(){if(Object.keys(trackBuffer).length===0)return;for(const[id,delta]of Object.entries(trackBuffer)){if(!panelMeta[id])panelMeta[id]={views:0,clicks:0,viewMs:0,lastView:0,score:0,locked:false,compact:false,overridePos:null};const m=panelMeta[id];m.views+=delta.views||0;m.clicks+=delta.clicks||0;m.viewMs+=delta.viewMs||0;if(delta.lastView>m.lastView)m.lastView=delta.lastView}trackBuffer={};saveState()}
function bufferEvent(id,field,val){if(!trackBuffer[id])trackBuffer[id]={views:0,clicks:0,viewMs:0,lastView:0};trackBuffer[id][field]=(trackBuffer[id][field]||0)+val;trackBuffer[id].lastView=Math.max(trackBuffer[id].lastView,Date.now())}
function startViewTimer(id){if(viewTimers[id])return;viewTimers[id]=Date.now();bufferEvent(id,'views',1)}
function stopViewTimer(id){if(!viewTimers[id])return;const elapsed=Date.now()-viewTimers[id];bufferEvent(id,'viewMs',elapsed);delete viewTimers[id]}
function setupIntersectionObserver(){
if(observer)observer.disconnect();
observer=new IntersectionObserver((entries)=>{
for(const e of entries){
const id=e.target.dataset.pid;
if(!id)continue;
if(e.isIntersecting)startViewTimer(id);
else stopViewTimer(id)
}
},{threshold:.5});
$$('.panel').forEach(p=>observer.observe(p))
}
function computeScores(){
const now=Date.now();
for(const[id,m]of Object.entries(panelMeta)){
const ageHours=Math.max(0,(now-(m.lastView||now))/3600000);
const recency=Math.exp(-ageHours/24);
const freq=m.views||0;
const dur=m.viewMs||0;
m.score=(freq*recency*0.4)+(Math.log1p(dur/1000)*0.35)+(Math.log1p(m.clicks||0)*0.25);
}
}
function rankPanels(){
const now=Date.now();
return panels.map((p,i)=>({...p,origIdx:i})).sort((a,b)=>{
const sa=panelMeta[a.id]?.score||0;
const sb=panelMeta[b.id]?.score||0;
const la=panelMeta[a.id]?.locked||false;
const lb=panelMeta[b.id]?.locked||false;
if(la&&!lb)return -1;
if(!la&&lb)return 1;
if(panelMeta[a.id]?.overridePos!==null&&panelMeta[b.id]?.overridePos!==null)return panelMeta[a.id].overridePos-panelMeta[b.id].overridePos;
if(panelMeta[a.id]?.overridePos!==null)return -1;
if(panelMeta[b.id]?.overridePos!==null)return 1;
return sb-sa
})
}
function calcCompact(ranked){
const maxScore=Math.max(...Object.values(panelMeta).map(m=>m.score||0),1);
for(const p of ranked){
const m=panelMeta[p.id]||{};
const rel=m.score/maxScore;
m.compact=!m.locked&&rel<COMPACT_THRESHOLD&&m.score<0.5;
}
}
function renderGrid(){
const ranked=rankPanels();
calcCompact(ranked);
const grid=$('#grid');
const compactZone=$('#compactZone');
const activePanels=ranked.filter(p=>!panelMeta[p.id]?.compact);
const compactPanels=ranked.filter(p=>panelMeta[p.id]?.compact);
for(const p of activePanels){
let el=$(`.panel[data-pid="${p.id}"]`);
if(!el){el=createPanelElement(p);grid.appendChild(el)}
else{const existing=$$('.panel',grid).indexOf(el);const target=activePanels.indexOf(p);if(existing!==target&&existing>=0){const ref=grid.children[target];if(ref&&ref!==el)grid.insertBefore(el,ref)}updatePanelElement(el,p)}
}
const gridPanels=$$('.panel',grid);
for(const el of gridPanels){const pid=el.dataset.pid;if(!activePanels.find(p=>p.id===pid)){stopViewTimer(pid);grid.removeChild(el)}}
for(const p of compactPanels){
let el=$(`.panel[data-pid="${p.id}"]`);
if(!el){el=createPanelElement(p);compactZone.appendChild(el)}
else if(el.parentElement!==compactZone){compactZone.appendChild(el)}
}
const zonePanels=$$('.panel',compactZone);
for(const el of zonePanels){const pid=el.dataset.pid;if(!compactPanels.find(p=>p.id===pid)){const p2=panels.find(x=>x.id===pid);if(p2){let gel=$(`.panel[data-pid="${p.id}"]`,grid);if(!gel){gel=createPanelElement(p2);grid.appendChild(gel)}else{grid.appendChild(gel)}}}}
setupIntersectionObserver();
$('#eventBadge').textContent='Events: '+Object.values(panelMeta).reduce((s,m)=>s+(m.views||0)+(m.clicks||0),0);
}
function createPanelElement(p){
const el=document.createElement('div');
el.className='panel'+(panelMeta[p.id]?.locked?' locked':'')+(panelMeta[p.id]?.compact?' compact':'');
el.dataset.pid=p.id;
el.draggable=true;
el.addEventListener('dragstart',onDragStart);
el.addEventListener('dragend',onDragEnd);
el.addEventListener('dragover',e=>{e.preventDefault();el.classList.add('drop-target')});
el.addEventListener('dragleave',()=>el.classList.remove('drop-target'));
el.addEventListener('drop',onDrop);
el.addEventListener('click',e=>{if(!e.target.closest('button')){bufferEvent(p.id,'clicks',1);renderGrid()}});
const h=buildHeader(p);
const body=buildBody(p);
const preview=buildPreview(p);
el.appendChild(h);
el.appendChild(body);
el.appendChild(preview);
return el
}
function buildHeader(p){
const h=document.createElement('div');
h.className='panel-header';
const m=panelMeta[p.id]||{};
const score=m.score||0;
const maxScore=Math.max(...Object.values(panelMeta).map(x=>x.score||0),1);
const rel=score/maxScore;
const badgeCls=rel<COMPACT_THRESHOLD?'low':'';
h.innerHTML=`<span class="title">${esc(p.title)}</span><span class="rank-badge ${badgeCls}">#${p.rank||'-'}</span><span class="actions"><button class="lock-btn${m.locked?' locked':''}" data-action="lock" title="Lock position">&#128274;</button><button data-action="compact" title="Toggle compact">&#9660;</button><button data-action="remove" title="Remove panel">&times;</button></span>`;
h.querySelector('[data-action="lock"]').addEventListener('click',e=>{e.stopPropagation();toggleLock(p.id)});
h.querySelector('[data-action="compact"]').addEventListener('click',e=>{e.stopPropagation();toggleCompact(p.id)});
h.querySelector('[data-action="remove"]').addEventListener('click',e=>{e.stopPropagation();removePanel(p.id)});
return h
}
function buildBody(p){
const b=document.createElement('div');
b.className='panel-body';
b.innerHTML=`<div class="metric">${p.value||'--'}</div><div class="label">${esc(p.label||p.title)}</div><div class="spark">${genSpark(p.spark||[])}</div>`;
return b
}
function buildPreview(p){
const pr=document.createElement('div');
pr.className='panel-preview';
pr.innerHTML=`<span class="mini-val">${p.value||'--'}</span><span>${esc(p.title)}</span>`;
return pr
}
function updatePanelElement(el,p){
const h=el.querySelector('.panel-header');
if(h){const titleEl=h.querySelector('.title');if(titleEl)titleEl.textContent=p.title;const badge=h.querySelector('.rank-badge');if(badge){badge.textContent='#'+(p.rank||'-');const m=panelMeta[p.id]||{};const maxS=Math.max(...Object.values(panelMeta).map(x=>x.score||0),1);badge.className='rank-badge'+((m.score/maxS)<COMPACT_THRESHOLD?' low':'')};const lockBtn=h.querySelector('.lock-btn');if(lockBtn){const locked=panelMeta[p.id]?.locked;lockBtn.className='lock-btn'+(locked?' locked':'');lockBtn.innerHTML=locked?'&#128274;':'&#128275;'}}
const body=el.querySelector('.panel-body');
if(body){const metricEl=body.querySelector('.metric');if(metricEl)metricEl.textContent=p.value||'--';const labelEl=body.querySelector('.label');if(labelEl)labelEl.textContent=p.label||p.title}
const preview=el.querySelector('.panel-preview');
if(preview){const mv=preview.querySelector('.mini-val');if(mv)mv.textContent=p.value||'--'}
const locked=panelMeta[p.id]?.locked;
el.classList.toggle('locked',!!locked);
const compact=panelMeta[p.id]?.compact;
el.classList.toggle('compact',!!compact);
}
function genSpark(data){
if(!data||data.length===0)data=Array.from({length:12},()=>Math.random()*100);
const max=Math.max(...data,1);
return data.map(v=>`<div class="bar" style="height:${(v/max)*100}%"></div>`).join('')
}
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML}
function onDragStart(e){
draggedEl=e.target.closest('.panel');
if(!draggedEl)return;
dragSrcIdx=$$('.panel',draggedEl.parentElement).indexOf(draggedEl);
draggedEl.classList.add('dragging');
e.dataTransfer.effectAllowed='move';
e.dataTransfer.setData('text/plain',draggedEl.dataset.pid)
}
function onDragEnd(e){
if(draggedEl)draggedEl.classList.remove('dragging');
$$('.drop-target').forEach(el=>el.classList.remove('drop-target'));
draggedEl=null;dragSrcIdx=null
}
function onDrop(e){
e.preventDefault();
if(!draggedEl)return;
const target=e.target.closest('.panel');
if(!target||target===draggedEl)return;
const srcPid=draggedEl.dataset.pid;
const tgtPid=target.dataset.pid;
if(!panelMeta[srcPid])panelMeta[srcPid]={};
if(!panelMeta[tgtPid])panelMeta[tgtPid]={};
panelMeta[srcPid].overridePos=panels.findIndex(p=>p.id===tgtPid);
panelMeta[tgtPid].overridePos=panels.findIndex(p=>p.id===srcPid);
panelMeta[srcPid].locked=true;
panelMeta[tgtPid].locked=true;
renderGrid();
toast('Swapped & locked: '+esc(panels.find(p=>p.id===srcPid)?.title||'')+' <-> '+esc(panels.find(p=>p.id===tgtPid)?.title||''))
}
function toggleLock(id){
if(!panelMeta[id])panelMeta[id]={};
panelMeta[id].locked=!panelMeta[id].locked;
if(!panelMeta[id].locked)panelMeta[id].overridePos=null;
renderGrid();
toast((panelMeta[id].locked?'Locked':'Unlocked')+': '+esc(panels.find(p=>p.id===id)?.title||id))
}
function toggleCompact(id){
if(!panelMeta[id])panelMeta[id]={};
panelMeta[id].compact=!panelMeta[id].compact;
renderGrid()
}
function removePanel(id){
if(panels.length<=1){toast('Cannot remove last panel');return}
const idx=panels.findIndex(p=>p.id===id);
if(idx<0)return;
const title=panels[idx].title;
panels.splice(idx,1);
delete panelMeta[id];
delete trackBuffer[id];
stopViewTimer(id);
renderGrid();
toast('Removed: '+esc(title))
}
function addPanel(){
const id='p'+Date.now()+Math.random().toString(36).slice(2,6);
const n=panels.length+1;
const types=[
{title:'CPU Usage',label:'% utilized',value:Math.floor(Math.random()*80+10)+'%',spark:Array.from({length:12},()=>Math.random()*100)},
{title:'Memory',label:'GB active',value:(Math.random()*14+2).toFixed(1)+' GB',spark:Array.from({length:12},()=>Math.random()*100)},
{title:'Requests/s',label:'throughput',value:Math.floor(Math.random()*5000+500).toLocaleString(),spark:Array.from({length:12},()=>Math.random()*100)},
{title:'Error Rate',label:'% of requests',value:(Math.random()*4+.1).toFixed(2)+'%',spark:Array.from({length:12},()=>Math.random()*100)},
{title:'Latency p99',label:'milliseconds',value:Math.floor(Math.random()*300+50)+'ms',spark:Array.from({length:12},()=>Math.random()*100)},
{title:'Active Users',label:'concurrent',value:Math.floor(Math.random()*2000+100),spark:Array.from({length:12},()=>Math.random()*100)}
];
const t=types[Math.floor(Math.random()*types.length)];
const panel={id,title:t.title+' '+n,label:t.label,value:t.value,spark:t.spark,rank:n};
panels.push(panel);
panelMeta[id]={views:0,clicks:1,viewMs:0,lastView:Date.now(),score:0.3,locked:false,compact:false,overridePos:null};
renderGrid();
toast('Added: '+esc(panel.title))
}
function toggleHeatmap(){
heatmapOn=!heatmapOn;
$('#heatBtn').textContent='Heatmap: '+(heatmapOn?'On':'Off');
$('#heatOverlay').style.display=heatmapOn?'block':'none';
if(heatmapOn)renderHeatmap()
}
function renderHeatmap(){
if(!heatmapOn)return;
const overlay=$('#heatOverlay');
overlay.innerHTML='';
const maxScore=Math.max(...Object.values(panelMeta).map(m=>m.score||0),1);
for(const[id,m]of Object.entries(panelMeta)){
const el=document.querySelector(`.panel[data-pid="${id}"]`);
if(!el)continue;
const rect=el.getBoundingClientRect();
const cell=document.createElement('div');
cell.className='heat-cell';
cell.style.left=rect.left+'px';
cell.style.top=rect.top+'px';
cell.style.width=rect.width+'px';
cell.style.height=rect.height+'px';
const intensity=(m.score||0)/maxScore;
const r=Math.round(99+156*intensity);
const g=Math.round(102-102*intensity);
const b=Math.round(241-241*intensity);
cell.style.background=`rgba(${r},${g},${b},${0.3+intensity*0.5})`;
overlay.appendChild(cell)
}
}
function resetLayout(){
for(const id of Object.keys(panelMeta)){panelMeta[id].locked=false;panelMeta[id].overridePos=null;panelMeta[id].compact=false}
renderGrid();
toast('Layout reset — all overrides cleared')
}
function randomizeMetrics(){
for(const p of panels){
p.value=Math.floor(Math.random()*100)+(Math.random()<.5?'%':' ms');
p.spark=Array.from({length:12},()=>Math.random()*100);
}
renderGrid()
}
function initSession(){
const loaded=loadState();
if(!loaded||panels.length===0){
const defaults=[
{id:'p1',title:'CPU Usage',label:'% utilized',value:'42%',spark:[30,45,38,60,55,70,65,80,72,58,42,48]},
{id:'p2',title:'Memory',label:'GB active',value:'11.3 GB',spark:[80,82,78,85,88,84,90,87,82,79,83,86]},
{id:'p3',title:'Requests/s',label:'throughput',value:'2,847',spark:[60,65,70,68,75,80,72,85,90,82,78,88]},
{id:'p4',title:'Error Rate',label:'% of requests',value:'0.12%',spark:[5,3,8,2,4,1,3,6,2,4,1,3]},
{id:'p5',title:'Latency p99',label:'milliseconds',value:'187ms',spark:[40,35,42,38,45,50,42,38,44,40,36,42]},
{id:'p6',title:'Active Users',label:'concurrent',value:'1,204',spark:[70,75,80,78,85,90,82,88,92,86,80,84]}
];
panels=defaults;
for(const p of panels){
panelMeta[p.id]={views:Math.floor(Math.random()*50),clicks:Math.floor(Math.random()*20),viewMs:Math.floor(Math.random()*300000),lastView:Date.now()-Math.floor(Math.random()*86400000),score:Math.random()*0.8+0.1,locked:false,compact:false,overridePos:null}
}
}
computeScores();
const ranked=rankPanels();
ranked.forEach((p,i)=>{p.rank=i+1});
panels=ranked.map(p=>({id:p.id,title:p.title,label:p.label,value:p.value,spark:p.spark,rank:p.rank}));
renderGrid();
$('#sessionBadge').textContent='Session: '+sessionId.slice(-6);
flushTimer=setInterval(flushState,FLUSH_INTERVAL_MS);
scoreTimer=setInterval(()=>{computeScores();renderGrid()},SCORE_INTERVAL_MS);
setInterval(randomizeMetrics,30000);
window.addEventListener('beforeunload',()=>{flushState();stopViewTimerAll()});
window.addEventListener('resize',()=>{if(heatmapOn)renderHeatmap()});
}
function stopViewTimerAll(){for(const id of Object.keys(viewTimers))stopViewTimer(id)}
window.addPanel=addPanel;
window.removePanel=removePanel;
window.toggleLock=toggleLock;
window.toggleCompact=toggleCompact;
window.toggleHeatmap=toggleHeatmap;
window.resetLayout=resetLayout;
initSession();
})();
</script>
</body>
</html>
```