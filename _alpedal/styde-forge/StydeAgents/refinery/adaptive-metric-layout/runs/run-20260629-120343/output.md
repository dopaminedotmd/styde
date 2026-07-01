<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Layout Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222633;--border:#2a3040;
  --text:#e0e4f0;--text2:#8892a8;--accent:#6c8cff;--accent2:#40c9a2;
  --warn:#f0a040;--danger:#f06060;--compact-scale:0.6;
  --high-span:4;--mid-span:2;--low-span:1;--grid-cols:12;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;flex-wrap:wrap}
.toolbar .title{font-weight:700;font-size:16px;color:var(--accent);margin-right:auto}
.toolbar button{padding:6px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:12px;transition:all .15s}
.toolbar button:hover{background:var(--accent);border-color:var(--accent);color:#fff}
.toolbar button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.toolbar .score-display{font-size:11px;color:var(--text2);margin-left:8px}
.dashboard{display:grid;grid-template-columns:repeat(var(--grid-cols),1fr);gap:8px;padding:8px;min-height:calc(100vh - 100px);grid-auto-rows:140px;transition:all .4s ease}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:12px;position:relative;overflow:hidden;transition:all .4s ease;display:flex;flex-direction:column;cursor:grab;min-width:0}
.panel:active{cursor:grabbing}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.compact{padding:8px;transform:scale(var(--compact-scale));transform-origin:top left;margin-bottom:-30px;margin-right:-20px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-title{font-size:11px}
.panel.compact .panel-metric{font-size:16px}
.panel.compact .sparkline{height:20px}
.panel-title{font-size:13px;font-weight:600;color:var(--text2);margin-bottom:6px;display:flex;align-items:center;gap:6px}
.panel-title .rank-badge{font-size:10px;padding:1px 6px;border-radius:10px;background:var(--accent);color:#fff;opacity:0.8}
.panel-metric{font-size:28px;font-weight:700;margin-bottom:2px;line-height:1}
.panel-change{font-size:12px;margin-bottom:6px}
.panel-change.up{color:var(--accent2)}
.panel-change.down{color:var(--danger)}
.panel-body{flex:1;display:flex;flex-direction:column;gap:4px;min-height:0;overflow:hidden}
.sparkline{width:100%;height:36px;flex-shrink:0}
.panel-actions{position:absolute;top:6px;right:6px;display:flex;gap:4px;opacity:0;transition:opacity .15s}
.panel:hover .panel-actions{opacity:1}
.panel-actions button{width:22px;height:22px;border:1px solid var(--border);border-radius:4px;background:var(--surface2);color:var(--text2);cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;line-height:1}
.panel-actions button:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.panel-actions button.lock-btn.locked{background:var(--accent);color:#fff}
.panel-score{font-size:10px;color:var(--text2);position:absolute;bottom:4px;right:8px;opacity:0.5}
.compact-zone{border:2px dashed var(--border);border-radius:12px;padding:8px;min-height:100px;display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start;align-content:flex-start;grid-column:1/-1;background:var(--surface2);opacity:0.6}
.compact-zone::before{content:'More panels — drag to expand';display:block;width:100%;text-align:center;font-size:11px;color:var(--text2);padding:4px;margin-bottom:4px}
.compact-zone .panel{transform:none;margin-bottom:0;margin-right:0;display:inline-flex;width:180px;height:80px;flex-shrink:0}
.dragging{opacity:0.5;z-index:999}
.drag-over{border-color:var(--accent2);box-shadow:0 0 12px rgba(64,201,162,.3)}
.score-bar{height:3px;background:var(--border);border-radius:2px;margin-top:auto;overflow:hidden}
.score-bar-fill{height:100%;background:linear-gradient(90deg,var(--danger),var(--warn),var(--accent2));border-radius:2px;transition:width .6s}
</style>
</head>
<body>
<div class="toolbar">
  <span class="title">Adaptive Layout</span>
  <button id="btn-auto" class="active" title="Auto-arrange based on attention scores">Auto</button>
  <button id="btn-reset" title="Reset all tracking data">Reset</button>
  <button id="btn-export" title="Export layout">Export</button>
  <span class="score-display">Last rearrange: --</span>
</div>
<div class="dashboard" id="dashboard"></div>
<script>
(function(){
const STORAGE_KEY = 'adaptive_layout_v1';
const SCORE_THRESHOLD_RERANK = 0.05;
const THROTTLE_MS = 500;
const REEVAL_INTERVAL = 30000;
const DECAY_HALF_LIFE_H = 24;
const COMPACT_PERCENTILE = 0.25;
let panels = {};
let panelOrder = [];
let autoMode = true;
let lastRearrange = null;
function createPanels(){
  const defs = [
    {id:'revenue',title:'Revenue',metric:'$45,231',change:'+12.5%',dir:'up',data:[30,35,32,40,38,45,42,48,52,49,55,60,58,62,65,70,68,72,75,78,76,80,82,85]},
    {id:'users',title:'Active Users',metric:'8,492',change:'+5.2%',dir:'up',data:[120,125,130,128,135,140,138,145,150,148,155,160,158,162,165,170,168,172,175,178,180,182,185,188]},
    {id:'conversion',title:'Conversion',metric:'3.8%',change:'-0.3%',dir:'down',data:[42,41,43,40,38,39,37,38,36,37,35,36,34,35,33,34,32,33,31,32,30,31,29,30].map(v=>v/10)},
    {id:'cpu',title:'CPU Load',metric:'67%',change:'+8.1%',dir:'up',data:[45,48,52,50,55,58,60,62,59,65,68,70,67,72,69,71,74,73,76,75,78,77,80,82]},
    {id:'memory',title:'Memory',metric:'4.2GB',change:'+2.1%',dir:'up',data:[32,33,35,34,36,38,37,39,40,41,42,43,44,45,44,46,47,48,47,49,50,51,50,52].map(v=>v/10)},
    {id:'latency',title:'P95 Latency',metric:'142ms',change:'-12ms',dir:'up',data:[180,175,170,168,160,155,158,150,148,145,140,142,138,135,130,132,128,125,122,120,118,115,112,110]},
    {id:'errors',title:'Error Rate',metric:'0.12%',change:'+0.04%',dir:'down',data:[5,4,6,5,7,6,8,7,9,8,10,9,8,7,6,5,4,3,2,3,2,1,2,1].map(v=>v/100)},
    {id:'bandwidth',title:'Bandwidth',metric:'2.4Gbps',change:'+18%',dir:'up',data:[80,85,90,88,95,100,98,105,110,108,115,120,118,125,130,128,135,140,138,145,150,148,155,160]},
    {id:'alerts',title:'Active Alerts',metric:'3',change:'+1',dir:'down',data:[2,1,3,2,1,4,3,2,5,4,3,6,5,4,3,2,1,0,1,0,2,1,3,2]},
    {id:'disk',title:'Disk I/O',metric:'320MB/s',change:'-5%',dir:'up',data:[60,62,58,65,63,68,70,66,72,69,74,71,76,73,78,75,80,77,82,79,84,81,86,83]},
    {id:'cache',title:'Cache Hit',metric:'94.2%',change:'+1.1%',dir:'up',data:[90,91,89,92,90,93,91,94,92,95,93,96,94,95,93,96,94,97,95,96,94,97,95,96].map(v=>v-10)},
    {id:'queue',title:'Queue Depth',metric:'47',change:'-12',dir:'up',data:[80,75,70,68,65,60,58,55,50,52,48,45,42,40,38,35,32,30,28,25,22,20,18,15]},
  ];
  defs.forEach((d,i)=>{
    panels[d.id] = {
      id:d.id,title:d.title,metric:d.metric,change:d.change,dir:d.dir,
      data:d.data,viewDuration:0,interactionCount:0,lastInteraction:null,
      attentionScore:0,locked:false,compact:false,
      manualOrder:i,orderIndex:i,
      _lastScore:0,_throttleTs:0,_sparkCanvas:null
    };
    panelOrder.push(d.id);
  });
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return;
    const saved = JSON.parse(raw);
    if(saved.panels) Object.keys(saved.panels).forEach(id=>{
      if(panels[id]) Object.assign(panels[id], saved.panels[id]);
    });
    if(saved.panelOrder) panelOrder = saved.panelOrder.filter(id=>panels[id]);
    if(saved.autoMode!==undefined) autoMode = saved.autoMode;
  }catch(e){}
}
function saveState(){
  const out = {
    panels:{},panelOrder,autoMode,
    savedAt:Date.now()
  };
  Object.keys(panels).forEach(id=>{
    out.panels[id] = {
      viewDuration:panels[id].viewDuration,
      interactionCount:panels[id].interactionCount,
      lastInteraction:panels[id].lastInteraction,
      attentionScore:panels[id].attentionScore,
      locked:panels[id].locked,
      compact:panels[id].compact,
      manualOrder:panels[id].manualOrder,
    };
  });
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(out))}catch(e){}
}
function recencyFactor(ts){
  if(!ts) return 0.5;
  const hours = (Date.now() - ts) / 3600000;
  return 1 / (1 + hours / DECAY_HALF_LIFE_H);
}
function computeScore(id){
  const p = panels[id];
  const rec = recencyFactor(p.lastInteraction);
  const dur = Math.max(p.viewDuration, 0.1);
  const freq = p.interactionCount + 1;
  return freq * dur * rec;
}
function recomputeAllScores(){
  panelOrder.forEach(id=>{
    panels[id].attentionScore = computeScore(id);
  });
}
function rankPanels(){
  recomputeAllScores();
  const unlocked = panelOrder.filter(id=>!panels[id].locked);
  unlocked.sort((a,b)=>panels[b].attentionScore - panels[a].attentionScore);
  const locked = panelOrder.filter(id=>panels[id].locked);
  const newOrder = [];
  unlocked.forEach((id,i)=>{
    panels[id].orderIndex = i;
    newOrder.push(id);
  });
  locked.forEach(id=>newOrder.splice(panels[id].manualOrder,0,id));
  panelOrder = newOrder.filter((id,i)=>panelOrder.indexOf(id)===i||panelOrder.indexOf(id)<0?true:(panelOrder.splice(panelOrder.indexOf(id),1),false));
  const scores = panelOrder.map(id=>panels[id].attentionScore);
  const sorted = [...scores].sort((a,b)=>a-b);
  const threshold = sorted[Math.floor(COMPACT_PERCENTILE * sorted.length)] || 0;
  panelOrder.forEach(id=>{
    panels[id].compact = panels[id].attentionScore <= threshold && !panels[id].locked;
  });
  applyLayout();
  lastRearrange = new Date().toLocaleTimeString();
  document.querySelector('.score-display').textContent = 'Last rearrange: '+lastRearrange;
  saveState();
}
function applyLayout(){
  const compactIds = panelOrder.filter(id=>panels[id].compact && !panels[id].locked);
  const visibleIds = panelOrder.filter(id=>!panels[id].compact || panels[id].locked);
  const container = document.getElementById('dashboard');
  container.innerHTML = '';
  if(compactIds.length>0){
    const zone = document.createElement('div');
    zone.className = 'compact-zone';
    zone.setAttribute('data-zone','compact');
    compactIds.forEach(id=>renderPanel(id, zone));
    container.appendChild(zone);
  }
  visibleIds.forEach(id=>renderPanel(id, container));
  assignGridPositions(visibleIds, container);
}
function assignGridPositions(ids, container){
  const cols = 12;
  let row = 1, col = 1;
  const children = container.querySelectorAll(':scope > .panel:not(.compact-zone .panel)');
  ids.forEach((id,idx)=>{
    const el = container.querySelector('[data-panel-id="'+id+'"]:not(.compact-zone .panel)');
    if(!el) return;
    const isHigh = idx < Math.ceil(ids.length * 0.25);
    const isMid = idx < Math.ceil(ids.length * 0.7);
    let span, rowSpan;
    if(isHigh){span=4;rowSpan=2}
    else if(isMid){span=3;rowSpan=1}
    else{span=2;rowSpan=1}
    if(col + span > cols + 1){col=1;row+=rowSpan}
    el.style.gridColumn = col+' / span '+span;
    el.style.gridRow = row+' / span '+rowSpan;
    panels[id].gridArea = {col,row,span,rowSpan};
    col += span;
    if(col > cols){col=1;row+=rowSpan}
  });
}
function renderPanel(id, parent){
  const p = panels[id];
  const el = document.createElement('div');
  el.className = 'panel'+(p.locked?' locked':'')+(p.compact?' compact':'');
  el.setAttribute('data-panel-id',id);
  el.draggable = true;
  const scorePercent = panelOrder.length>0?Math.min(100,Math.round((p.attentionScore/(panelOrder.reduce((m,id2)=>Math.max(m,panels[id2].attentionScore),0.1)))*100)):0;
  el.innerHTML = 
    '<div class="panel-actions">'+
      '<button class="lock-btn'+(p.locked?' locked':'')+'" title="Lock position">&#x1F512;</button>'+
      '<button class="expand-btn" title="'+(p.compact?'Expand':'Compact')+'">'+(p.compact?'+':'\u2212')+'</button>'+
    '</div>'+
    '<div class="panel-title">'+p.title+' <span class="rank-badge">#'+(p.orderIndex+1)+'</span></div>'+
    '<div class="panel-metric">'+p.metric+'</div>'+
    '<div class="panel-change '+p.dir+'">'+p.change+'</div>'+
    '<div class="panel-body"><canvas class="sparkline"></canvas></div>'+
    '<div class="score-bar"><div class="score-bar-fill" style="width:'+scorePercent+'%"></div></div>'+
    '<div class="panel-score">'+Math.round(p.attentionScore)+'</div>';
  parent.appendChild(el);
  requestAnimationFrame(()=>drawSparkline(el.querySelector('.sparkline'), p.data, p.dir==='up'?1:-1));
  el.querySelector('.lock-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleLock(id)});
  el.querySelector('.expand-btn').addEventListener('click',(e)=>{e.stopPropagation();toggleCompact(id)});
  el.addEventListener('dragstart',handleDragStart);
  el.addEventListener('dragover',handleDragOver);
  el.addEventListener('drop',handleDrop);
  el.addEventListener('dragend',handleDragEnd);
  el.addEventListener('click',()=>recordInteraction(id,'click'));
  el.addEventListener('mouseenter',()=>recordInteraction(id,'hover'));
  return el;
}
function drawSparkline(canvas, data, direction){
  if(!canvas) return;
  const rect = canvas.parentElement.getBoundingClientRect();
  const w = rect.width - 8;
  const h = canvas.parentElement.clientHeight || 36;
  canvas.width = w * (window.devicePixelRatio||1);
  canvas.height = h * (window.devicePixelRatio||1);
  canvas.style.width = w+'px';
  canvas.style.height = h+'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(window.devicePixelRatio||1, window.devicePixelRatio||1);
  ctx.clearRect(0,0,w,h);
  const min = Math.min(...data), max = Math.max(...data);
  const range = max-min || 1;
  const xStep = w/(data.length-1);
  ctx.beginPath();
  ctx.strokeStyle = direction>=0?'#40c9a2':'#f06060';
  ctx.lineWidth = 1.5;
  ctx.lineJoin = 'round';
  data.forEach((v,i)=>{
    const x = i*xStep;
    const y = h - ((v-min)/range)*(h-4) - 2;
    if(i===0) ctx.moveTo(x,y);
    else ctx.lineTo(x,y);
  });
  ctx.stroke();
  const grad = ctx.createLinearGradient(0,0,0,h);
  grad.addColorStop(0, direction>=0?'rgba(64,201,162,0.15)':'rgba(240,96,96,0.15)');
  grad.addColorStop(1,'rgba(0,0,0,0)');
  ctx.lineTo(w,h);
  ctx.lineTo(0,h);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();
}
function recordInteraction(id, type){
  const p = panels[id];
  if(!p) return;
  const now = Date.now();
  if(type==='hover' && now - p._throttleTs < THROTTLE_MS) return;
  p._throttleTs = now;
  p.interactionCount++;
  p.lastInteraction = now;
}
function toggleLock(id){
  panels[id].locked = !panels[id].locked;
  if(panels[id].locked) panels[id].manualOrder = panelOrder.indexOf(id);
  saveState();
  refreshUI();
}
function toggleCompact(id){
  panels[id].compact = !panels[id].compact;
  if(panels[id].compact) panels[id].locked = false;
  saveState();
  refreshUI();
}
let dragSrcId = null;
function handleDragStart(e){
  dragSrcId = this.getAttribute('data-panel-id');
  this.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain',dragSrcId);
}
function handleDragOver(e){
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  this.classList.add('drag-over');
}
function handleDragLeave(){this.classList.remove('drag-over')}
function handleDrop(e){
  e.preventDefault();
  this.classList.remove('drag-over');
  const targetId = this.getAttribute('data-panel-id');
  if(!dragSrcId||dragSrcId===targetId) return;
  const srcIdx = panelOrder.indexOf(dragSrcId);
  const tgtIdx = panelOrder.indexOf(targetId);
  panelOrder.splice(srcIdx,1);
  panelOrder.splice(tgtIdx,0,dragSrcId);
  panelOrder.forEach((id,i)=>{panels[id].orderIndex=i});
  panels[dragSrcId].locked = true;
  panels[dragSrcId].manualOrder = tgtIdx;
  panels[targetId].locked = true;
  panels[targetId].manualOrder = panelOrder.indexOf(targetId);
  recomputeAllScores();
  saveState();
  refreshUI();
}
function handleDragEnd(e){
  this.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(el=>el.classList.remove('drag-over'));
  dragSrcId = null;
}
function refreshUI(){
  const container = document.getElementById('dashboard');
  const existingEls = {};
  container.querySelectorAll('[data-panel-id]').forEach(el=>{
    existingEls[el.getAttribute('data-panel-id')] = el;
  });
  const visibleIds = panelOrder.filter(id=>!panels[id].compact||panels[id].locked);
  const compactIds = panelOrder.filter(id=>panels[id].compact&&!panels[id].locked);
  container.innerHTML = '';
  if(compactIds.length>0){
    const zone = document.createElement('div');
    zone.className = 'compact-zone';
    zone.setAttribute('data-zone','compact');
    compactIds.forEach(id=>renderPanel(id, zone));
    container.appendChild(zone);
  }
  visibleIds.forEach(id=>renderPanel(id, container));
  assignGridPositions(visibleIds, container);
  document.getElementById('btn-auto').classList.toggle('active', autoMode);
}
function startTracking(){
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      const id = entry.target.getAttribute('data-panel-id');
      if(!id||!panels[id]) return;
      if(entry.isIntersecting){
        entry.target._visibleSince = Date.now();
      }else if(entry.target._visibleSince){
        panels[id].viewDuration += (Date.now() - entry.target._visibleSince)/1000;
        entry.target._visibleSince = null;
      }
    });
  },{threshold:0.3});
  const mo = new MutationObserver(()=>{
    document.querySelectorAll('[data-panel-id]').forEach(el=>{
      if(!el._observed){el._observed=true;observer.observe(el)}
    });
  });
  mo.observe(document.getElementById('dashboard'),{childList:true,subtree:true});
  document.querySelectorAll('[data-panel-id]').forEach(el=>{
    el._observed=true;observer.observe(el);
  });
  window.addEventListener('beforeunload',()=>{
    const now = Date.now();
    document.querySelectorAll('[data-panel-id]').forEach(el=>{
      if(el._visibleSince){
        const id = el.getAttribute('data-panel-id');
        if(panels[id]) panels[id].viewDuration += (now - el._visibleSince)/1000;
      }
    });
    saveState();
  });
  setInterval(()=>{
    if(!autoMode) return;
    recomputeAllScores();
    const needsRerank = panelOrder.some(id=>{
      const p = panels[id];
      const diff = Math.abs(p.attentionScore - p._lastScore);
      return p._lastScore>0 && diff/p._lastScore > SCORE_THRESHOLD_RERANK;
    });
    panelOrder.forEach(id=>{panels[id]._lastScore=panels[id].attentionScore});
    if(needsRerank) rankPanels();
    else applyLayout();
    saveState();
  },REEVAL_INTERVAL);
}
function init(){
  createPanels();
  loadState();
  recomputeAllScores();
  panelOrder.forEach(id=>{panels[id]._lastScore=panels[id].attentionScore});
  if(!autoMode){
    panelOrder.sort((a,b)=>panels[a].manualOrder-panels[b].manualOrder);
    panelOrder.forEach((id,i)=>{panels[id].orderIndex=i});
  }else{
    panelOrder.sort((a,b)=>panels[b].attentionScore-panels[a].attentionScore);
    panelOrder.forEach((id,i)=>{panels[id].orderIndex=i});
  }
  refreshUI();
  startTracking();
  document.getElementById('btn-auto').addEventListener('click',()=>{
    autoMode = !autoMode;
    document.getElementById('btn-auto').classList.toggle('active',autoMode);
    if(autoMode) rankPanels();
    saveState();
  });
  document.getElementById('btn-reset').addEventListener('click',()=>{
    if(!confirm('Reset all tracking data?')) return;
    panelOrder.forEach(id=>{
      panels[id].viewDuration=0;
      panels[id].interactionCount=0;
      panels[id].lastInteraction=null;
      panels[id].attentionScore=0;
      panels[id].locked=false;
      panels[id].compact=false;
    });
    localStorage.removeItem(STORAGE_KEY);
    rankPanels();
  });
  document.getElementById('btn-export').addEventListener('click',()=>{
    const exp = {panels:{},layout:panelOrder,autoMode,scores:{}};
    Object.keys(panels).forEach(id=>{
      exp.panels[id]={title:panels[id].title,locked:panels[id].locked,compact:panels[id].compact,gridArea:panels[id].gridArea};
      exp.scores[id]=Math.round(panels[id].attentionScore);
    });
    const blob = new Blob([JSON.stringify(exp,null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href=url;a.download='layout-export-'+Date.now()+'.json';
    a.click();
    URL.revokeObjectURL(url);
  });
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
else init();
})();
</script>
</body>
</html>