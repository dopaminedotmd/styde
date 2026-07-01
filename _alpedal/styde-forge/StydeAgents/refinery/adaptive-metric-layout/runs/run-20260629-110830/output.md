<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22253a;
  --border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #8890a8;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --danger: #ff6b7a;
  --success: #4ade80;
  --warning: #fbbf24;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--bg);
  color:var(--text);
  font-family:system-ui,-apple-system,sans-serif;
  min-height:100vh;
  padding:16px;
  -webkit-font-smoothing:antialiased;
}
.header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:16px;
  flex-wrap:wrap;
  gap:12px;
}
.header h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.01em}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.btn{
  background:var(--surface);
  color:var(--text);
  border:1px solid var(--border);
  padding:7px 14px;
  border-radius:7px;
  cursor:pointer;
  font-size:0.82rem;
  transition:var(--transition);
  white-space:nowrap;
}
.btn:hover{background:var(--surface-hover);border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.small{padding:4px 10px;font-size:0.75rem}
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  gap:var(--gap);
  transition:var(--transition);
}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:16px;
  cursor:grab;
  transition:var(--transition), grid-column 0.35s ease, grid-row 0.35s ease;
  position:relative;
  display:flex;
  flex-direction:column;
  gap:10px;
  will-change:transform;
  contain:layout style;
}
.panel:hover{border-color:var(--accent);box-shadow:0 0 16px var(--accent-glow)}
.panel.dragging{opacity:0.5;cursor:grabbing;transform:scale(0.98);z-index:10}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 24px var(--accent-glow);transform:scale(1.01)}
.panel.compact{
  grid-column:span 1;
  padding:10px 14px;
  gap:4px;
}
.panel.compact .metric-value{font-size:1.1rem}
.panel.compact .chart-area,.panel.compact .detail-row{display:none}
.panel.large{grid-column:span 2}
.panel.manual-lock{border-color:var(--warning);box-shadow:0 0 8px rgba(251,191,36,0.2)}
.panel.manual-lock::after{
  content:'locked';
  position:absolute;
  top:8px;right:10px;
  font-size:0.65rem;
  color:var(--warning);
  text-transform:uppercase;
  letter-spacing:0.05em;
  pointer-events:none;
}
.panel-handle{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
}
.panel-title{
  font-size:0.8rem;
  color:var(--text-dim);
  text-transform:uppercase;
  letter-spacing:0.04em;
  font-weight:500;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.icon-btn{
  background:none;
  border:none;
  color:var(--text-dim);
  cursor:pointer;
  padding:4px 6px;
  border-radius:5px;
  font-size:0.85rem;
  line-height:1;
  transition:var(--transition);
}
.icon-btn:hover{color:var(--text);background:var(--surface-hover)}
.metric-value{
  font-size:1.6rem;
  font-weight:700;
  letter-spacing:-0.02em;
  line-height:1.1;
}
.metric-sub{font-size:0.75rem;color:var(--text-dim)}
.chart-area{
  background:var(--bg);
  border-radius:6px;
  height:80px;
  position:relative;
  overflow:hidden;
}
.chart-area canvas{width:100%;height:100%}
.detail-row{
  display:flex;
  justify-content:space-between;
  font-size:0.73rem;
  color:var(--text-dim);
  gap:12px;
}
.detail-row span:last-child{color:var(--text);font-weight:500}
.rank-badge{
  position:absolute;
  top:8px;left:10px;
  font-size:0.6rem;
  color:var(--accent);
  opacity:0.7;
  font-weight:600;
}
.compact .rank-badge{top:4px;left:8px}
.toast{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%);
  background:var(--surface);
  border:1px solid var(--accent);
  color:var(--text);
  padding:10px 22px;
  border-radius:20px;
  font-size:0.82rem;
  z-index:100;
  animation:toastIn 0.3s ease, toastOut 0.3s ease 2.2s forwards;
  pointer-events:none;
}
@keyframes toastIn{from{opacity:0;transform:translateX(-50%) translateY(12px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
@keyframes toastOut{from{opacity:1}to{opacity:0}}
@media(max-width:640px){
  body{padding:8px}
  .grid{grid-template-columns:1fr;gap:8px}
  .panel{padding:12px}
  .panel.large{grid-column:span 1}
  .metric-value{font-size:1.3rem}
  .header h1{font-size:1.05rem}
  .btn{padding:6px 10px;font-size:0.75rem}
  .chart-area{height:60px}
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metrics</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset Data</button>
    <button class="btn" id="btnExport" title="Export layout">Export</button>
    <button class="btn" id="btnAuto" title="Force auto-arrange">Auto-Arrange</button>
  </div>
</div>
<div class="grid" id="grid"></div>
<script>
(function(){
'use strict';
const LS_KEY = 'adaptive_metrics_v1';
const COMPACT_THRESHOLD = 0.15;
const LARGE_THRESHOLD = 0.7;
const DECAY_DAYS = 7;
const MS_PER_DAY = 86400000;
const VIEW_DELAY = 800;
const SAVE_DEBOUNCE = 500;
let panels = [];
let attention = {};
let manualLocks = {};
let compactOverrides = {};
let dragState = null;
let viewTimers = {};
let saveTimer = null;
let lastArrangeHash = '';
const METRICS = [
  {id:'revenue',title:'Revenue',value:'$128,430',sub:'+12.3% vs last month',color:'#6c8cff'},
  {id:'users',title:'Active Users',value:'24,891',sub:'+8.1% this week',color:'#4ade80'},
  {id:'churn',title:'Churn Rate',value:'2.4%',sub:'-0.3% improvement',color:'#ff6b7a'},
  {id:'latency',title:'P95 Latency',value:'187ms',sub:'-14ms from baseline',color:'#fbbf24'},
  {id:'errors',title:'Error Rate',value:'0.12%',sub:'Below 0.5% threshold',color:'#ff6b7a'},
  {id:'conversion',title:'Conversion',value:'3.8%',sub:'+0.5% this quarter',color:'#4ade80'},
  {id:'sessions',title:'Sessions',value:'142K',sub:'+18% YoY',color:'#6c8cff'},
  {id:'nps',title:'NPS Score',value:'72',sub:'+5 points',color:'#fbbf24'},
  {id:'cpu',title:'CPU Usage',value:'64%',sub:'4 nodes active',color:'#8890a8'},
  {id:'storage',title:'Storage',value:'2.1TB',sub:'42% utilized',color:'#8890a8'},
];
function loadState(){
  try{
    const raw = localStorage.getItem(LS_KEY);
    if(raw){
      const d = JSON.parse(raw);
      attention = d.attention || {};
      manualLocks = d.manualLocks || {};
      compactOverrides = d.compactOverrides || {};
    }
  }catch(e){/* corrupt data, reset */}
}
function saveState(){
  clearTimeout(saveTimer);
  saveTimer = setTimeout(()=>{
    try{
      localStorage.setItem(LS_KEY, JSON.stringify({
        attention,
        manualLocks,
        compactOverrides,
        savedAt: Date.now()
      }));
    }catch(e){/* quota exceeded, silent */}
  }, SAVE_DEBOUNCE);
}
function computeScore(id){
  const a = attention[id];
  if(!a) return 0;
  const now = Date.now();
  const days = Math.max(0, (now - (a.lastSeen || now)) / MS_PER_DAY);
  const recency = Math.exp(-days / DECAY_DAYS);
  const freq = Math.log2((a.views || 0) + 1);
  const dur = Math.log2(((a.totalDuration || 0) / 1000) + 1);
  return freq * dur * recency;
}
function getRanked(){
  const scored = METRICS.map(m=>({...m, score:computeScore(m.id)}));
  scored.sort((a,b)=>b.score - a.score);
  return scored;
}
function panelClass(rank, total){
  const ratio = 1 - (rank / Math.max(total-1,1));
  if(compactOverrides[panels[rank]?.id]) return 'compact';
  if(ratio < COMPACT_THRESHOLD) return 'compact';
  if(ratio > LARGE_THRESHOLD && total > 3) return 'large';
  return '';
}
function arrangeHash(ranked){
  return ranked.map((p,i)=>`${p.id}:${i}:${panelClass(i,ranked.length)}`).join('|');
}
function renderPanel(p, rank, total){
  const cls = panelClass(rank, total);
  const locked = !!manualLocks[p.id];
  const score = computeScore(p.id);
  return (
    '<div class="panel'+(cls?' '+cls:'')+(locked?' manual-lock':'')+
    '" data-id="'+p.id+'" draggable="true">'+
    '<div class="rank-badge">#'+(rank+1)+' '+score.toFixed(1)+'</div>'+
    '<div class="panel-handle">'+
    '<span class="panel-title">'+p.title+'</span>'+
    '<div class="panel-actions">'+
    '<button class="icon-btn btn-toggle-compact" data-id="'+p.id+
    '" title="Toggle compact">'+(cls==='compact'?'expand':'compress')+'</button>'+
    '<button class="icon-btn btn-lock" data-id="'+p.id+
    '" title="'+(locked?'Unlock':'Lock')+' position">'+(locked?'lock_open':'lock')+'</button>'+
    '</div></div>'+
    '<div class="metric-value">'+p.value+'</div>'+
    '<div class="metric-sub">'+p.sub+'</div>'+
    '<div class="chart-area"><canvas data-id="'+p.id+'"></canvas></div>'+
    '<div class="detail-row"><span>Score</span><span>'+score.toFixed(2)+'</span></div>'+
    '<div class="detail-row"><span>Views</span><span>'+
    ((attention[p.id]?.views)||0)+'</span></div>'+
    '<div class="detail-row"><span>Duration</span><span>'+
    (attention[p.id]?Math.round((attention[p.id].totalDuration||0)/1000)+'s':'0s')+'</span></div>'+
    '</div>'
  );
}
function diffRender(ranked){
  const grid = document.getElementById('grid');
  const hash = arrangeHash(ranked);
  if(hash === lastArrangeHash) return;
  lastArrangeHash = hash;
  const existing = new Map();
  grid.querySelectorAll('.panel').forEach(el=>existing.set(el.dataset.id, el));
  const frag = document.createDocumentFragment();
  ranked.forEach((p, i)=>{
    const total = ranked.length;
    const cls = panelClass(i, total);
    const locked = !!manualLocks[p.id];
    const ex = existing.get(p.id);
    if(ex){
      ex.className = 'panel'+(cls?' '+cls:'')+(locked?' manual-lock':'');
      const badge = ex.querySelector('.rank-badge');
      if(badge) badge.textContent = '#'+(i+1)+' '+computeScore(p.id).toFixed(1);
      const scoreSpan = ex.querySelector('.detail-row:first-of-type span:last-child');
      if(scoreSpan) scoreSpan.textContent = computeScore(p.id).toFixed(2);
      const viewsSpan = ex.querySelectorAll('.detail-row')[1]?.querySelector('span:last-child');
      if(viewsSpan) viewsSpan.textContent = (attention[p.id]?.views)||0;
      const durSpan = ex.querySelectorAll('.detail-row')[2]?.querySelector('span:last-child');
      if(durSpan) durSpan.textContent = attention[p.id]?Math.round((attention[p.id].totalDuration||0)/1000)+'s':'0s';
      existing.delete(p.id);
      frag.appendChild(ex);
    }else{
      const tpl = document.createElement('template');
      tpl.innerHTML = renderPanel(p, i, total).trim();
      frag.appendChild(tpl.content.firstChild);
    }
  });
  existing.forEach(el=>el.remove());
  grid.appendChild(frag);
  drawCharts();
}
function drawCharts(){
  const ranked = getRanked();
  document.querySelectorAll('.chart-area canvas').forEach(canvas=>{
    const id = canvas.dataset.id;
    const ctx = canvas.getContext('2d');
    const w = canvas.parentElement.clientWidth;
    const h = canvas.parentElement.clientHeight;
    canvas.width = w * (devicePixelRatio||1);
    canvas.height = h * (devicePixelRatio||1);
    canvas.style.width = w+'px';
    canvas.style.height = h+'px';
    ctx.scale(devicePixelRatio||1, devicePixelRatio||1);
    const vals = [];
    for(let i=0;i<20;i++) vals.push(20+Math.random()*60+(id.charCodeAt(0)%20));
    const max = Math.max(...vals);
    const r = ranked.findIndex(p=>p.id===id);
    const colors = ['#6c8cff','#4ade80','#fbbf24','#ff6b7a','#8890a8','#6c8cff','#4ade80','#fbbf24','#ff6b7a','#8890a8'];
    const color = colors[r]||'#6c8cff';
    ctx.clearRect(0,0,w,h);
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.lineJoin = 'round';
    vals.forEach((v,i)=>{
      const x = (i/(vals.length-1))*w;
      const y = h - (v/max)*h;
      if(i===0) ctx.moveTo(x,y);
      else ctx.lineTo(x,y);
    });
    ctx.stroke();
    const grad = ctx.createLinearGradient(0,0,0,h);
    grad.addColorStop(0,color+'40');
    grad.addColorStop(1,color+'05');
    ctx.lineTo(w,h);
    ctx.lineTo(0,h);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();
  });
}
function trackView(id, start){
  if(!attention[id]) attention[id] = {views:0, totalDuration:0, lastSeen:0};
  attention[id].views++;
  attention[id].lastSeen = Date.now();
  attention[id].totalDuration = (attention[id].totalDuration||0) + (Date.now()-start);
  saveState();
  scheduleArrange();
}
let arrangePending = false;
function scheduleArrange(){
  if(arrangePending) return;
  arrangePending = true;
  requestAnimationFrame(()=>{
    arrangePending = false;
    const ranked = getRanked();
    const locked = ranked.filter(p=>manualLocks[p.id]);
    const unlocked = ranked.filter(p=>!manualLocks[p.id]);
    const reordered = [...locked, ...unlocked];
    diffRender(reordered);
  });
}
function initObserver(){
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      const id = e.target.dataset.id;
      if(!id) return;
      if(e.isIntersecting){
        viewTimers[id] = Date.now();
      }else if(viewTimers[id]){
        const elapsed = Date.now() - viewTimers[id];
        if(elapsed > VIEW_DELAY){
          if(!attention[id]) attention[id]={views:0,totalDuration:0,lastSeen:0};
          attention[id].totalDuration = (attention[id].totalDuration||0) + elapsed;
          attention[id].lastSeen = Date.now();
          saveState();
        }
        delete viewTimers[id];
      }
    });
  },{threshold:0.3});
  return observer;
}
let panelObserver = initObserver();
function observePanels(){
  panelObserver.disconnect();
  document.querySelectorAll('.panel').forEach(p=>panelObserver.observe(p));
}
function handleClick(e){
  const panel = e.target.closest('.panel');
  if(!panel) return;
  const id = panel.dataset.id;
  if(viewTimers[id]){
    const elapsed = Date.now() - viewTimers[id];
    if(elapsed > VIEW_DELAY){
      if(!attention[id]) attention[id]={views:0,totalDuration:0,lastSeen:0};
      attention[id].views++;
      attention[id].lastSeen = Date.now();
      attention[id].totalDuration = (attention[id].totalDuration||0)+elapsed;
      saveState();
      scheduleArrange();
    }
  }
  const btnToggle = e.target.closest('.btn-toggle-compact');
  if(btnToggle){
    e.preventDefault();
    const pid = btnToggle.dataset.id;
    compactOverrides[pid] = !compactOverrides[pid];
    saveState();
    scheduleArrange();
    observePanels();
    return;
  }
  const btnLock = e.target.closest('.btn-lock');
  if(btnLock){
    e.preventDefault();
    const pid = btnLock.dataset.id;
    manualLocks[pid] = !manualLocks[pid];
    saveState();
    scheduleArrange();
    observePanels();
    return;
  }
}
function handleDragStart(e){
  const panel = e.target.closest('.panel');
  if(!panel) return;
  if(e.target.closest('button')){e.preventDefault();return;}
  dragState = {el:panel, id:panel.dataset.id};
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panel.dataset.id);
}
function handleDragOver(e){
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const panel = e.target.closest('.panel');
  if(panel && panel !== dragState?.el){
    document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));
    panel.classList.add('drag-over');
  }
}
function handleDrop(e){
  e.preventDefault();
  document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));
  if(!dragState) return;
  const target = e.target.closest('.panel');
  if(!target || target === dragState.el){
    dragState.el.classList.remove('dragging');
    dragState = null;
    return;
  }
  manualLocks[dragState.id] = true;
  manualLocks[target.dataset.id] = true;
  const ranked = getRanked();
  const aIdx = ranked.findIndex(p=>p.id===dragState.id);
  const bIdx = ranked.findIndex(p=>p.id===target.dataset.id);
  if(aIdx>=0&&bIdx>=0){
    [ranked[aIdx], ranked[bIdx]] = [ranked[bIdx], ranked[aIdx]];
  }
  dragState.el.classList.remove('dragging');
  dragState = null;
  saveState();
  diffRender(ranked);
  observePanels();
  showToast('Layout updated · both panels locked');
}
function handleDragEnd(e){
  if(dragState){
    dragState.el.classList.remove('dragging');
    dragState = null;
  }
  document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));
}
function showToast(msg){
  const existing = document.querySelector('.toast');
  if(existing) existing.remove();
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(()=>t.remove(), 2600);
}
function resetData(){
  attention = {};
  manualLocks = {};
  compactOverrides = {};
  localStorage.removeItem(LS_KEY);
  lastArrangeHash = '';
  scheduleArrange();
  observePanels();
  showToast('All tracking data reset');
}
function exportLayout(){
  const data = {attention, manualLocks, compactOverrides, panels:getRanked().map((p,i)=>({id:p.id,rank:i+1,score:p.score}))};
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'adaptive-layout-'+new Date().toISOString().slice(0,10)+'.json';
  a.click();
  showToast('Layout exported');
}
function init(){
  loadState();
  scheduleArrange();
  observePanels();
  document.addEventListener('click', handleClick);
  document.addEventListener('dragstart', handleDragStart);
  document.addEventListener('dragover', handleDragOver);
  document.addEventListener('drop', handleDrop);
  document.addEventListener('dragend', handleDragEnd);
  document.getElementById('btnReset').addEventListener('click', resetData);
  document.getElementById('btnExport').addEventListener('click', exportLayout);
  document.getElementById('btnAuto').addEventListener('click', ()=>{
    manualLocks = {};
    compactOverrides = {};
    lastArrangeHash = '';
    saveState();
    scheduleArrange();
    observePanels();
    showToast('Auto-arrange enabled · all locks cleared');
  });
  window.addEventListener('resize', ()=>{
    clearTimeout(window._resizeTimer);
    window._resizeTimer = setTimeout(()=>{
      drawCharts();
    }, 200);
  });
  window.addEventListener('beforeunload', ()=>{
    Object.entries(viewTimers).forEach(([id,start])=>{
      const elapsed = Date.now() - start;
      if(elapsed > VIEW_DELAY){
        if(!attention[id]) attention[id]={views:0,totalDuration:0,lastSeen:0};
        attention[id].totalDuration = (attention[id].totalDuration||0) + elapsed;
      }
    });
    saveState();
  });
  const mq = window.matchMedia('(max-width:640px)');
  mq.addEventListener('change', ()=>{drawCharts();});
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
else init();
})();
</script>
</body>
</html>