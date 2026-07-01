<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222636;--border:#2d3142;
  --text:#e1e4ed;--text2:#9196a8;--accent:#6c8cff;--accent2:#4a6cf7;
  --compact-bg:#141720;--drag-bg:#283050;--shadow:0 4px 24px rgba(0,0,0,.4);
  --radius:10px;--gap:12px;--header-h:48px;--toolbar-h:40px;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
header{display:flex;align-items:center;justify-content:space-between;height:var(--header-h);padding:0 20px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
header h1{font-size:16px;font-weight:600;letter-spacing:.3px}
.toolbar{display:flex;align-items:center;gap:16px}
.toolbar label{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text2);cursor:pointer}
.toolbar input[type=range]{width:80px;accent-color:var(--accent)}
.toolbar button{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:all .15s}
.toolbar button:hover{background:var(--border);border-color:var(--accent)}
.toolbar button.active{background:var(--accent);border-color:var(--accent);color:#fff}
#grid{display:grid;gap:var(--gap);padding:20px;transition:grid-template-columns .35s ease,grid-template-rows .35s ease;min-height:calc(100vh - var(--header-h))}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column;transition:all .35s ease,box-shadow .2s;position:relative}
.panel:hover{box-shadow:var(--shadow)}
.panel.top-left{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.compact{background:var(--compact-bg);border-style:dashed;opacity:.85}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--surface2);border-bottom:1px solid var(--border);cursor:grab;user-select:none;min-height:42px}
.panel-header:active{cursor:grabbing}
.panel-header .panel-title{font-size:13px;font-weight:600;letter-spacing:.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .panel-actions{display:flex;align-items:center;gap:6px;flex-shrink:0}
.panel-header .panel-actions button{background:0;border:0;color:var(--text2);cursor:pointer;padding:4px;border-radius:4px;font-size:14px;line-height:1;transition:all .12s}
.panel-header .panel-actions button:hover{color:var(--text);background:var(--border)}
.panel-header .panel-actions button.locked{color:var(--accent)}
.panel-header .panel-score{font-size:10px;color:var(--text2);margin-left:4px;flex-shrink:0}
.panel-body{padding:14px;flex:1;display:flex;flex-direction:column;gap:10px;min-height:60px;overflow:auto}
.panel-body .metric{display:flex;align-items:baseline;gap:6px}
.panel-body .metric-value{font-size:28px;font-weight:700;letter-spacing:-.5px}
.panel-body .metric-label{font-size:12px;color:var(--text2)}
.panel-body .metric-trend{font-size:12px;padding:1px 6px;border-radius:3px}
.panel-body .metric-trend.up{color:#4ade80;background:rgba(74,222,128,.1)}
.panel-body .metric-trend.down{color:#f87171;background:rgba(248,113,113,.1)}
.panel-body .sparkline{display:flex;align-items:flex-end;gap:2px;height:40px}
.panel-body .sparkline span{flex:1;background:var(--accent);border-radius:1px 1px 0 0;min-height:2px;transition:height .3s}
.panel-preview{display:none;align-items:center;justify-content:center;padding:8px 14px;gap:8px;font-size:11px;color:var(--text2)}
.panel-preview .preview-metric{font-weight:600;color:var(--text)}
.panel-preview .preview-label{font-size:10px}
.panel-drag-ghost{position:fixed;pointer-events:none;z-index:9999;opacity:.8;transform:scale(1.02);background:var(--drag-bg);border:2px solid var(--accent);border-radius:var(--radius);padding:8px 16px;font-size:13px;font-weight:600;color:var(--text);box-shadow:0 8px 32px rgba(0,0,0,.5);display:none}
.btn-icon{width:28px;height:28px;display:flex;align-items:center;justify-content:center}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="toolbar">
    <label>Adaptivity<input type="range" id="adaptivitySlider" min="0" max="100" value="80" title="0=manual only, 100=full auto"></label>
    <button id="btnReset" title="Reset all tracking data">Reset</button>
    <button id="btnExport" title="Export layout config">Export</button>
  </div>
</header>
<div id="grid"></div>
<div class="panel-drag-ghost" id="dragGhost"></div>
<script>
(function(){
const LS_KEY='adaptive_dashboard_v1';
const DEFAULT_PANELS=[
  {id:'revenue',title:'Revenue',metric:'$48.2K',label:'This month',trend:'up',trendVal:'+12.4%',sparkline:[40,55,48,62,70,58,72,65,80,75,88,82]},
  {id:'users',title:'Active Users',metric:'2,847',label:'Online now',trend:'up',trendVal:'+5.8%',sparkline:[60,58,65,70,68,75,72,80,78,85,82,90]},
  {id:'conversion',title:'Conversion Rate',metric:'3.24%',label:'Avg 30d',trend:'down',trendVal:'-0.3%',sparkline:[70,68,65,62,60,58,55,52,50,48,45,42]},
  {id:'latency',title:'API Latency',metric:'142ms',label:'P95',trend:'up',trendVal:'+8ms',sparkline:[30,28,35,32,38,40,42,45,48,50,52,55]},
  {id:'errors',title:'Error Rate',metric:'0.12%',label:'Last 24h',trend:'down',trendVal:'-0.05%',sparkline:[20,22,18,15,12,10,8,9,7,6,5,4]},
  {id:'storage',title:'Storage',metric:'76.4GB',label:'Used of 100GB',trend:'down',trendVal:'-2.1GB',sparkline:[90,88,85,82,80,78,76,74,72,70,68,65]},
  {id:'sessions',title:'Sessions',metric:'12.4K',label:'Today',trend:'up',trendVal:'+18%',sparkline:[45,48,52,55,60,65,70,75,80,85,88,92]},
  {id:'uptime',title:'Uptime',metric:'99.97%',label:'30-day avg',trend:'up',trendVal:'+0.02%',sparkline:[95,96,95,97,96,98,97,98,99,98,99,99]},
  {id:'bandwidth',title:'Bandwidth',metric:'842Mbps',label:'Peak',trend:'up',trendVal:'+42Mbps',sparkline:[50,55,60,58,65,70,68,75,72,80,78,85]}
];
let panels=[];
let tracking={};
let layoutOrder=[];
let lockedPanels=new Set();
let recomputeCount=0;
let adaptivity=80;
let panelEls=new Map();
let dragState=null;
function loadState(){
  try{
    const raw=localStorage.getItem(LS_KEY);
    if(raw){
      const saved=JSON.parse(raw);
      panels=saved.panels||[...DEFAULT_PANELS];
      tracking=saved.tracking||{};
      layoutOrder=saved.layoutOrder||panels.map(p=>p.id);
      lockedPanels=new Set(saved.lockedPanels||[]);
      adaptivity=saved.adaptivity??80;
    }else{
      panels=[...DEFAULT_PANELS];
      panels.forEach(p=>{tracking[p.id]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true}});
      layoutOrder=panels.map(p=>p.id);
    }
  }catch(e){resetState()}
  document.getElementById('adaptivitySlider').value=adaptivity;
}
function saveState(){
  const data={panels,tracking,layoutOrder,lockedPanels:[...lockedPanels],adaptivity};
  localStorage.setItem(LS_KEY,JSON.stringify(data));
}
function resetState(){
  panels=[...DEFAULT_PANELS];
  tracking={};
  panels.forEach(p=>{tracking[p.id]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true}});
  layoutOrder=panels.map(p=>p.id);
  lockedPanels.clear();
  adaptivity=80;
  document.getElementById('adaptivitySlider').value=adaptivity;
  saveState();
  recomputeLayout();
}
function computeAttentionScore(panelId){
  const t=tracking[panelId];
  if(!t||t.views===0)return 0;
  const now=Date.now();
  const hoursSinceLastView=Math.max(1,(now-t.lastViewed)/(1000*60*60));
  const recency=1/Math.log(1+hoursSinceLastView);
  const avgDuration=t.views>0?t.totalDuration/t.views:0;
  return (t.interactions+1)*(avgDuration/1000+1)*recency;
}
function rankPanels(){
  const scores=layoutOrder.map(id=>{
    const panel=panels.find(p=>p.id===id);
    if(!panel)return{id,score:0};
    return{id,score:computeAttentionScore(id)};
  });
  scores.sort((a,b)=>b.score-a.score);
  return scores;
}
function isCompact(panelId){
  if(lockedPanels.has(panelId))return false;
  const t=tracking[panelId];
  if(!t||t.views<3)return false;
  const score=computeAttentionScore(panelId);
  const allScores=layoutOrder.map(id=>computeAttentionScore(id)).filter(s=>s>0);
  if(allScores.length<3)return false;
  const maxScore=Math.max(...allScores);
  return maxScore>0&&score/maxScore<0.15;
}
function recomputeLayout(){
  recomputeCount+=1;
  const ranked=rankPanels();
  const grid=document.getElementById('grid');
  if(!grid)return;
  const compactCount=ranked.filter(r=>isCompact(r.id)).length;
  const visibleCount=ranked.length-compactCount;
  const cols=Math.min(visibleCount>4?4:visibleCount>1?3:2,4);
  grid.style.gridTemplateColumns=`repeat(${cols},1fr)`;
  const newOrder=[];
  const compactIds=[];
  ranked.forEach((r,i)=>{
    const c=isCompact(r.id);
    if(c)compactIds.push(r.id);
    else newOrder.push(r.id);
  });
  newOrder.push(...compactIds);
  layoutOrder=newOrder;
  const fragment=document.createDocumentFragment();
  layoutOrder.forEach((id,i)=>{
    let el=panelEls.get(id);
    if(!el){
      el=createPanelElement(panels.find(p=>p.id===id));
      panelEls.set(id,el);
    }
    updatePanelDOM(el,id,i,ranked);
    if(el.parentNode!==fragment)fragment.appendChild(el);
  });
  const existing=Array.from(grid.children);
  existing.forEach(child=>{
    const pid=child.dataset.panelId;
    if(!layoutOrder.includes(pid))child.remove();
  });
  grid.appendChild(fragment);
  saveState();
}
function createPanelElement(panel){
  const el=document.createElement('div');
  el.className='panel';
  el.dataset.panelId=panel.id;
  el.draggable=true;
  el.innerHTML='<div class="panel-header"><span class="panel-title"></span><div class="panel-actions"><span class="panel-score"></span><button class="btn-icon lock-btn" title="Lock position">&#128274;</button><button class="btn-icon collapse-btn" title="Collapse">&#8722;</button></div></div><div class="panel-body"></div><div class="panel-preview"></div>';
  el.querySelector('.lock-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleLock(panel.id)});
  el.querySelector('.collapse-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleCollapse(panel.id)});
  el.addEventListener('dragstart',onDragStart);
  el.addEventListener('dragend',onDragEnd);
  el.addEventListener('mouseenter',()=>startViewTimer(panel.id));
  el.addEventListener('mouseleave',()=>stopViewTimer(panel.id));
  el.addEventListener('click',()=>recordInteraction(panel.id));
  return el;
}
function updatePanelDOM(el,id,position,ranked){
  const panel=panels.find(p=>p.id===id);
  if(!panel)return;
  const compact=isCompact(id);
  const rank=ranked.find(r=>r.id===id);
  const score=rank?rank.score:0;
  el.className='panel'+(position===0&&!compact?' top-left':'')+(compact?' compact':'');
  el.style.gridRow=compact?'auto':`span ${position===0?2:1}`;
  el.style.gridColumn=position===0&&!compact?'span 2':'span 1';
  el.dataset.position=position;
  const titleEl=el.querySelector('.panel-title');
  if(titleEl.textContent!==panel.title)titleEl.textContent=panel.title;
  const scoreEl=el.querySelector('.panel-score');
  const scoreText=score>0?score.toFixed(1):'0.0';
  if(scoreEl.textContent!==scoreText)scoreEl.textContent=scoreText;
  const lockBtn=el.querySelector('.lock-btn');
  lockBtn.className='btn-icon lock-btn'+(lockedPanels.has(id)?' locked':'');
  lockBtn.innerHTML=lockedPanels.has(id)?'&#128274;':'&#128275;';
  const collapseBtn=el.querySelector('.collapse-btn');
  const expanded=tracking[id]?.expanded!==false;
  collapseBtn.innerHTML=expanded?'&#8722;':'&#43;';
  if(compact){
    el.querySelector('.panel-body').style.display='none';
    const preview=el.querySelector('.panel-preview');
    preview.style.display='flex';
    preview.innerHTML=`<span class="preview-metric">${panel.metric}</span><span class="preview-label">${panel.label}</span>`;
  }else{
    el.querySelector('.panel-body').style.display='flex';
    el.querySelector('.panel-preview').style.display='none';
    const body=el.querySelector('.panel-body');
    const existingMetric=body.querySelector('.metric');
    if(!existingMetric||existingMetric.dataset.panelId!==id){
      body.innerHTML='';
      body.dataset.panelId=id;
      const metricDiv=document.createElement('div');
      metricDiv.className='metric';
      metricDiv.dataset.panelId=id;
      metricDiv.innerHTML=`<span class="metric-value">${panel.metric}</span><span class="metric-trend ${panel.trend}">${panel.trendVal}</span>`;
      const labelDiv=document.createElement('div');
      labelDiv.className='metric-label';
      labelDiv.textContent=panel.label;
      const sparkDiv=document.createElement('div');
      sparkDiv.className='sparkline';
      panel.sparkline.forEach(v=>{const s=document.createElement('span');s.style.height=v+'%';sparkDiv.appendChild(s)});
      body.appendChild(metricDiv);
      body.appendChild(labelDiv);
      body.appendChild(sparkDiv);
    }
  }
}
let viewTimer=null;
let viewPanelId=null;
function startViewTimer(id){
  if(viewPanelId===id)return;
  stopViewTimer();
  viewPanelId=id;
  viewTimer=setInterval(()=>{
    if(!tracking[id])tracking[id]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true};
    tracking[id].totalDuration+=500;
    tracking[id].lastViewed=Date.now();
  },500);
}
function stopViewTimer(id){
  if(viewTimer){clearInterval(viewTimer);viewTimer=null}
  if(viewPanelId){
    if(!tracking[viewPanelId])tracking[viewPanelId]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true};
    tracking[viewPanelId].views+=1;
    tracking[viewPanelId].lastViewed=Date.now();
    viewPanelId=null;
  }
}
function recordInteraction(id){
  if(!tracking[id])tracking[id]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true};
  tracking[id].interactions+=1;
  tracking[id].lastViewed=Date.now();
}
function toggleLock(id){
  if(lockedPanels.has(id))lockedPanels.delete(id);
  else lockedPanels.add(id);
  recomputeLayout();
}
function toggleCollapse(id){
  if(!tracking[id])tracking[id]={views:0,totalDuration:0,lastViewed:0,interactions:0,expanded:true};
  tracking[id].expanded=!tracking[id].expanded;
  recordInteraction(id);
  recomputeLayout();
}
function onDragStart(e){
  const el=e.target.closest('.panel');
  if(!el)return;
  const id=el.dataset.panelId;
  const panel=panels.find(p=>p.id===id);
  const ghost=document.getElementById('dragGhost');
  ghost.textContent=panel?panel.title:id;
  ghost.style.display='block';
  const clone=el.cloneNode(true);
  clone.style.position='absolute';
  clone.style.top='-9999px';
  clone.style.left='-9999px';
  clone.style.width=el.offsetWidth+'px';
  document.body.appendChild(clone);
  requestAnimationFrame(()=>{
    ghost.style.display='block';
    clone.remove();
  });
  e.dataTransfer.effectAllowed='move';
  e.dataTransfer.setData('text/plain',id);
  dragState={panelId:id,startX:e.clientX,startY:e.clientY};
  el.style.opacity='0.4';
}
function onDragEnd(e){
  const el=e.target.closest('.panel');
  if(el)el.style.opacity='1';
  const ghost=document.getElementById('dragGhost');
  ghost.style.display='none';
  if(dragState){
    recordInteraction(dragState.panelId);
    dragState=null;
  }
}
document.addEventListener('dragover',(e)=>{
  if(!dragState)return;
  e.preventDefault();
  const ghost=document.getElementById('dragGhost');
  ghost.style.left=(e.clientX-50)+'px';
  ghost.style.top=(e.clientY-15)+'px';
});
document.addEventListener('drop',(e)=>{
  e.preventDefault();
  if(!dragState)return;
  const target=e.target.closest('.panel');
  if(target&&target.dataset.panelId!==dragState.panelId){
    const targetId=target.dataset.panelId;
    const srcIdx=layoutOrder.indexOf(dragState.panelId);
    const tgtIdx=layoutOrder.indexOf(targetId);
    if(srcIdx>=0&&tgtIdx>=0){
      layoutOrder.splice(srcIdx,1);
      const newTgt=layoutOrder.indexOf(targetId);
      layoutOrder.splice(newTgt,0,dragState.panelId);
      recomputeLayout();
    }
  }
  dragState=null;
});
document.getElementById('adaptivitySlider').addEventListener('input',(e)=>{
  adaptivity=parseInt(e.target.value);
  saveState();
  if(adaptivity>50)recomputeLayout();
});
document.getElementById('btnReset').addEventListener('click',resetState);
document.getElementById('btnExport').addEventListener('click',()=>{
  const data={panels,tracking,layoutOrder,lockedPanels:[...lockedPanels],adaptivity,recomputeCount};
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='dashboard-layout-'+new Date().toISOString().slice(0,10)+'.json';
  a.click();
});
loadState();
recomputeLayout();
setInterval(()=>{
  const active=document.getElementById('grid').querySelectorAll('.panel:hover');
  if(active.length===0)recomputeLayout();
},30000);
})();
</script>
</body>
</html>