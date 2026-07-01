<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #1a1d23;
  --panel-bg: #242830;
  --panel-bg-locked: #252a33;
  --text: #e1e4e8;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent-glow: rgba(88,166,255,0.15);
  --success: #3fb950;
  --warning: #d29922;
  --danger: #f85149;
  --border: #30363d;
  --border-hover: #58a6ff;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.3);
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
  --grid-gap: 12px;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  --focus-ring: 0 0 0 3px rgba(88,166,255,0.5);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--font);
  padding:16px;
  min-height:100vh;
  -webkit-font-smoothing:antialiased;
}
body.keyboard-user *:focus{
  outline:none;
  box-shadow:var(--focus-ring);
}
body.keyboard-user *:focus:not(:focus-visible){
  box-shadow:none;
}
.header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:16px;
  flex-wrap:wrap;
  gap:8px;
}
.header h1{
  font-size:1.25rem;
  font-weight:600;
  letter-spacing:-0.01em;
}
.header-actions{
  display:flex;
  gap:8px;
  align-items:center;
}
.btn{
  background:var(--panel-bg);
  border:1px solid var(--border);
  color:var(--text);
  padding:6px 14px;
  border-radius:6px;
  cursor:pointer;
  font-size:0.8125rem;
  font-family:var(--font);
  transition:border-color var(--transition),background var(--transition);
}
.btn:hover{border-color:var(--border-hover);background:#2a2e38}
.btn:focus-visible{box-shadow:var(--focus-ring);outline:none}
.btn-icon{
  padding:6px 8px;
  display:flex;
  align-items:center;
  gap:4px;
}
.score-badge{
  background:var(--panel-bg);
  border:1px solid var(--border);
  border-radius:6px;
  padding:4px 10px;
  font-size:0.75rem;
  font-family:var(--font-mono);
  color:var(--text-dim);
  display:flex;
  align-items:center;
  gap:6px;
}
.score-badge .val{color:var(--accent);font-weight:600}
.grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  grid-auto-rows:160px;
  gap:var(--grid-gap);
}
.panel{
  background:var(--panel-bg);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:14px 16px;
  position:relative;
  transition:grid-column var(--transition),grid-row var(--transition),border-color var(--transition),box-shadow var(--transition);
  display:flex;
  flex-direction:column;
  cursor:grab;
  min-width:0;
}
.panel:focus-visible{
  border-color:var(--accent);
  box-shadow:var(--focus-ring);
  outline:none;
}
.panel.dragging{
  opacity:0.7;
  cursor:grabbing;
  box-shadow:0 8px 24px rgba(0,0,0,0.4);
  z-index:10;
  border-color:var(--accent);
}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow)}
.panel.locked{
  cursor:default;
  background:var(--panel-bg-locked);
  border-left:3px solid var(--accent);
}
.panel.locked .lock-indicator{display:flex}
.panel.compact{grid-row:span 1}
.panel.compact .panel-body{flex-direction:row;align-items:center;gap:10px}
.panel.compact .panel-metric{font-size:1rem}
.panel.compact .panel-chart{width:80px;height:32px}
.panel.compact .panel-detail{display:none}
.panel.compact .panel-preview{display:block}
.panel-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:6px;
  gap:6px;
}
.panel-title{
  font-size:0.75rem;
  font-weight:500;
  color:var(--text-dim);
  text-transform:uppercase;
  letter-spacing:0.05em;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.panel-controls{
  display:flex;
  gap:2px;
  flex-shrink:0;
}
.panel-ctrl{
  background:none;
  border:none;
  color:var(--text-dim);
  cursor:pointer;
  padding:2px 4px;
  border-radius:4px;
  font-size:0.75rem;
  line-height:1;
  transition:color 0.15s,background 0.15s;
}
.panel-ctrl:hover{color:var(--text);background:rgba(255,255,255,0.06)}
.panel-ctrl:focus-visible{box-shadow:var(--focus-ring);outline:none}
.lock-indicator{
  display:none;
  align-items:center;
  color:var(--accent);
  font-size:0.625rem;
}
.panel-body{
  display:flex;
  flex-direction:column;
  gap:4px;
  flex:1;
  min-height:0;
}
.panel-metric{
  font-size:1.5rem;
  font-weight:600;
  font-family:var(--font-mono);
  letter-spacing:-0.02em;
  line-height:1.2;
}
.panel-metric.down{color:var(--danger)}
.panel-metric.up{color:var(--success)}
.panel-metric.warn{color:var(--warning)}
.panel-delta{
  font-size:0.75rem;
  font-family:var(--font-mono);
  display:flex;
  align-items:center;
  gap:4px;
}
.panel-chart{
  flex:1;
  min-height:36px;
  width:100%;
}
.panel-chart svg{width:100%;height:100%}
.panel-preview{
  display:none;
  font-size:0.6875rem;
  color:var(--text-dim);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  max-width:160px;
}
.panel-rank{
  position:absolute;
  top:4px;
  right:8px;
  font-size:0.5625rem;
  color:var(--text-dim);
  font-family:var(--font-mono);
  opacity:0.5;
}
.panel.high-rank{border-color:rgba(88,166,255,0.3);box-shadow:0 0 12px var(--accent-glow)}
.more-section{
  grid-column:1/-1;
  border-top:1px dashed var(--border);
  padding:8px 0;
  display:flex;
  align-items:center;
  gap:8px;
  cursor:pointer;
  color:var(--text-dim);
  font-size:0.75rem;
  transition:color 0.15s;
}
.more-section:hover{color:var(--text)}
.more-section:focus-visible{box-shadow:var(--focus-ring);outline:none;border-radius:4px}
.more-count{
  background:var(--panel-bg);
  border:1px solid var(--border);
  border-radius:10px;
  padding:1px 6px;
  font-size:0.625rem;
  font-family:var(--font-mono);
}
.data-source{
  font-size:0.625rem;
  color:var(--text-dim);
  display:flex;
  align-items:center;
  gap:4px;
}
.data-source .dot{
  width:6px;height:6px;
  border-radius:50%;
  background:var(--success);
}
.data-source .dot.mock{background:var(--warning)}
.tooltip{
  position:fixed;
  background:#30363d;
  color:var(--text);
  padding:6px 10px;
  border-radius:4px;
  font-size:0.6875rem;
  pointer-events:none;
  z-index:100;
  opacity:0;
  transition:opacity 0.1s;
  max-width:200px;
}
.tooltip.visible{opacity:1}
@media(max-width:900px){
  .grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:500px){
  .grid{grid-template-columns:1fr}
  .header h1{font-size:1rem}
}
.sr-only{
  position:absolute;
  width:1px;height:1px;
  padding:0;margin:-1px;
  overflow:hidden;
  clip:rect(0,0,0,0);
  white-space:nowrap;
  border:0;
}
</style>
</head>
<body>
<div class="header">
  <h1 id="dashboard-title">Adaptive Metrics</h1>
  <div class="header-actions">
    <span class="data-source" aria-live="polite"><span class="dot mock" aria-hidden="true"></span><span id="source-label">mock data</span></span>
    <span class="score-badge" aria-label="Session attention score">attn <span class="val" id="session-score">0</span></span>
    <button class="btn btn-icon" id="btn-reset" aria-label="Reset all tracking data and layout">Reset</button>
    <button class="btn btn-icon" id="btn-auto" aria-label="Run auto-layout now">Auto-layout</button>
  </div>
</div>
<div class="grid" id="grid" role="list" aria-label="Metric panels">
</div>
<div class="tooltip" id="tooltip" aria-hidden="true"></div>
<script>
(function(){
'use strict';
const METRICS = [
  {id:'cpu',title:'CPU Usage',unit:'%',range:[5,95],trend:'up'},
  {id:'mem',title:'Memory',unit:'GB',range:[2,30],trend:'warn'},
  {id:'rps',title:'Requests/s',unit:'',range:[50,500],trend:'up'},
  {id:'p95',title:'P95 Latency',unit:'ms',range:[20,300],trend:'down'},
  {id:'err',title:'Error Rate',unit:'%',range:[0.01,5],trend:'down'},
  {id:'disk',title:'Disk IO',unit:'MB/s',range:[1,200],trend:'warn'},
  {id:'conn',title:'Connections',unit:'',range:[10,500],trend:'up'},
  {id:'cache',title:'Cache Hit',unit:'%',range:[60,99],trend:'up'},
  {id:'queue',title:'Queue Depth',unit:'',range:[0,200],trend:'down'},
  {id:'cost',title:'Cost/hr',unit:'$',range:[0.5,15],trend:'warn'}
];
const STORAGE_KEY = 'adaptive_dashboard_v1';
const SCORE_INTERVAL = 15000;
const DECAY_HALF = 3600000;
let panels = [];
let tracking = {};
let orderedIds = [];
let sessionScore = 0;
let scoreTimer = null;
let observer = null;
let visibilityMap = {};
let viewStartMap = {};
let dragState = null;
let useLiveData = false;
let dataInterval = null;
function el(id){return document.getElementById(id)}
function createEl(tag,attrs={},children=[]){
  const e = document.createElement(tag);
  for(const[k,v] of Object.entries(attrs)){
    if(k==='className') e.className=v;
    else if(k==='dataset') Object.assign(e.dataset,v);
    else if(k==='aria') {for(const[ak,av] of Object.entries(v)) e.setAttribute('aria-'+ak,av);}
    else if(k.startsWith('on')&&typeof v==='function') e.addEventListener(k.slice(2),v);
    else e.setAttribute(k,v);
  }
  for(const c of children){
    if(typeof c==='string') e.appendChild(document.createTextNode(c));
    else if(c) e.appendChild(c);
  }
  return e;
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return null;
    return JSON.parse(raw);
  }catch(e){return null}
}
function saveState(){
  const data = {
    panels: panels.map(p=>({id:p.id,locked:p.locked,overridePos:p.overridePos,compactMode:p.compactMode})),
    tracking,
    orderedIds,
    ts: Date.now()
  };
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(data))}catch(e){}
}
function initPanels(){
  const saved = loadState();
  const savedPanels = saved&&saved.panels?new Map(saved.panels.map(p=>[p.id,p])):new Map();
  panels = METRICS.map((m,i)=>{
    const sp = savedPanels.get(m.id)||{};
    return {
      id:m.id,
      title:m.title,
      unit:m.unit,
      range:m.range,
      trend:m.trend,
      value:0,
      history:[],
      locked:!!sp.locked,
      overridePos:sp.overridePos||null,
      compactMode:!!sp.compactMode,
      rank: i,
      el: null
    };
  });
  if(saved&&saved.orderedIds) orderedIds = saved.orderedIds.filter(id=>panels.some(p=>p.id===id));
  if(!orderedIds.length) orderedIds = panels.map(p=>p.id);
  if(saved&&saved.tracking) tracking = saved.tracking;
  for(const p of panels){
    if(!tracking[p.id]){
      tracking[p.id]={viewTime:0,interactions:0,lastInteraction:0,collapses:0,expands:0};
    }
  }
}
function generateValue(metric){
  const[lo,hi]=metric.range;
  const base = lo+(hi-lo)*(0.3+0.4*Math.sin(Date.now()/30000+panels.indexOf(metric)*1.7));
  const noise = (Math.random()-0.5)*(hi-lo)*0.1;
  return Math.max(lo,Math.min(hi,base+noise));
}
function updateValues(){
  for(const p of panels){
    const v = generateValue(p);
    p.value = v;
    p.history.push({t:Date.now(),v});
    if(p.history.length>60) p.history.shift();
  }
}
function formatValue(p){
  const v = p.value;
  if(v>=100) return Math.round(v).toLocaleString();
  if(v>=10) return v.toFixed(1);
  if(v>=1) return v.toFixed(2);
  return v.toFixed(3);
}
function getDelta(p){
  if(p.history.length<2) return {val:0,dir:'neutral'};
  const recent = p.history.slice(-10);
  const avg = recent.reduce((s,h)=>s+h.v,0)/recent.length;
  const prev = p.history[p.history.length-10]||p.history[0];
  const pct = prev.v?((avg-prev.v)/prev.v)*100:0;
  return {val:Math.abs(pct).toFixed(1),dir:pct>0?'up':pct<0?'down':'neutral'};
}
function computeScores(){
  const now = Date.now();
  let total=0;
  const scores = {};
  for(const p of panels){
    const t = tracking[p.id];
    const hoursSinceLast = Math.max(0,(now-t.lastInteraction)/3600000);
    const recency = Math.exp(-hoursSinceLast*Math.log(2)/(DECAY_HALF/3600000));
    const freq = Math.log2(t.interactions+2);
    const dur = Math.log2(t.viewTime/1000+2);
    const score = freq*dur*recency;
    scores[p.id]=score;
    total+=score;
  }
  const entry = Object.entries(scores).sort((a,b)=>b[1]-a[1]);
  const ranked = entry.map(([id])=>id);
  const unlocked = panels.filter(p=>!p.locked);
  const locked = panels.filter(p=>p.locked);
  const unlockedSorted = ranked.filter(id=>unlocked.some(p=>p.id===id));
  const newOrder = [...locked.map(p=>p.id),...unlockedSorted];
  orderedIds = newOrder;
  sessionScore = total>0?Math.round((total/entry.length)*100)/100:0;
}
function renderSparkline(panel){
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('viewBox','0 0 100 30');
  svg.setAttribute('preserveAspectRatio','none');
  svg.setAttribute('aria-hidden','true');
  svg.style.width='100%';
  svg.style.height='100%';
  const hist = panel.history;
  if(hist.length<2){
    const line = document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('x1','0');line.setAttribute('y1','15');
    line.setAttribute('x2','100');line.setAttribute('y2','15');
    line.setAttribute('stroke','#30363d');line.setAttribute('stroke-width','1');
    svg.appendChild(line);
    return svg;
  }
  const vals = hist.map(h=>h.v);
  const min=Math.min(...vals),max=Math.max(...vals);
  const range = max-min||1;
  const points = vals.map((v,i)=>{
    const x=(i/(vals.length-1))*100;
    const y=30-((v-min)/range)*28-1;
    return `${x},${y}`;
  });
  const polyline = document.createElementNS('http://www.w3.org/2000/svg','polyline');
  polyline.setAttribute('points',points.join(' '));
  polyline.setAttribute('fill','none');
  const dir = getDelta(panel).dir;
  const color = dir==='up'?'#3fb950':dir==='down'?'#f85149':'#8b949e';
  polyline.setAttribute('stroke',color);
  polyline.setAttribute('stroke-width','1.5');
  polyline.setAttribute('stroke-linecap','round');
  polyline.setAttribute('stroke-linejoin','round');
  svg.appendChild(polyline);
  const area = document.createElementNS('http://www.w3.org/2000/svg','polygon');
  const areaPoints = points.join(' ')+` 100,30 0,30`;
  area.setAttribute('points',areaPoints);
  area.setAttribute('fill',color);
  area.setAttribute('opacity','0.08');
  svg.appendChild(area);
  return svg;
}
function getPreviewText(panel){
  const delta = getDelta(panel);
  const dir = delta.dir==='up'?'&#x25B2;':delta.dir==='down'?'&#x25BC;':'';
  return `${dir}${delta.val}% ${formatValue(panel)}${panel.unit}`;
}
function createPanelEl(panel,rank){
  const p = panel;
  const delta = getDelta(p);
  const dirClass = delta.dir==='up'?'up':delta.dir==='down'?'down':'';
  const compact = p.compactMode;
  const locked = p.locked;
  const isHighRank = rank<3;
  const el = createEl('div',{
    className:'panel'+(compact?' compact':'')+(locked?' locked':'')+(isHighRank?' high-rank':''),
    role:'listitem',
    tabindex:'0',
    dataset:{panelId:p.id},
    aria:{label:`${p.title}: ${formatValue(p)}${p.unit}, rank ${rank+1}${locked?' locked':''}`},
    onkeydown(e){
      if(e.key==='l'&&e.ctrlKey){e.preventDefault();toggleLock(p.id)}
      if(e.key==='c'&&e.ctrlKey){e.preventDefault();toggleCompact(p.id)}
      if(e.key==='ArrowUp'&&e.ctrlKey){e.preventDefault();movePanel(p.id,-1)}
      if(e.key==='ArrowDown'&&e.ctrlKey){e.preventDefault();movePanel(p.id,1)}
    },
    onmousedown(e){if(!locked&&e.target===el||e.target.classList.contains('panel-header')||e.target.classList.contains('panel-title')) startDrag(e,p.id)},
    ontouchstart(e){if(!locked) startDrag(e,p.id)},
    onclick(e){if(!e.target.closest('.panel-ctrl')) recordInteraction(p.id)}
  });
  const header = createEl('div',{className:'panel-header'},[
    createEl('span',{className:'panel-title'},[p.title]),
    createEl('div',{className:'panel-controls'},[
      createEl('button',{
        className:'panel-ctrl',
        aria:{label:locked?'Unlock panel':'Lock panel position'},
        title:locked?'Unlock':'Lock',
        onclick(e){e.stopPropagation();toggleLock(p.id)}
      },[locked?'\u{1F512}':'\u{1F513}']),
      createEl('button',{
        className:'panel-ctrl',
        aria:{label:compact?'Expand panel':'Compact panel'},
        title:compact?'Expand':'Compact',
        onclick(e){e.stopPropagation();toggleCompact(p.id)}
      },[compact?'\u{26F6}':'\u{25AD}']),
      createEl('span',{className:'lock-indicator',aria:{hidden:'true'}},['\u{1F512}'])
    ])
  ]);
  const metricEl = createEl('span',{className:'panel-metric'+(dirClass?' '+dirClass:'')},[formatValue(p)+p.unit]);
  const deltaEl = createEl('span',{className:'panel-delta'},[
    delta.dir==='up'?'\u25B2':delta.dir==='down'?'\u25BC':'',
    delta.val+'%'
  ]);
  const chartWrap = createEl('div',{className:'panel-chart'});
  chartWrap.appendChild(renderSparkline(p));
  const previewEl = createEl('span',{className:'panel-preview'},[getPreviewText(p)]);
  const rankEl = createEl('span',{className:'panel-rank',aria:{hidden:'true'}},['#'+(rank+1)]);
  const body = createEl('div',{className:'panel-body'},[metricEl,deltaEl,chartWrap,previewEl]);
  el.appendChild(header);
  el.appendChild(body);
  el.appendChild(rankEl);
  p.el = el;
  return el;
}
function updatePanelEl(panel,rank){
  const p = panel;
  if(!p.el) return;
  const el = p.el;
  const delta = getDelta(p);
  const dirClass = delta.dir==='up'?'up':delta.dir==='down'?'down':'';
  const compact = p.compactMode;
  const locked = p.locked;
  const isHighRank = rank<3;
  el.className = 'panel'+(compact?' compact':'')+(locked?' locked':'')+(isHighRank?' high-rank':'');
  el.setAttribute('aria-label',`${p.title}: ${formatValue(p)}${p.unit}, rank ${rank+1}${locked?' locked':''}`);
  el.querySelector('.panel-title').textContent = p.title;
  const metricEl = el.querySelector('.panel-metric');
  metricEl.textContent = formatValue(p)+p.unit;
  metricEl.className = 'panel-metric'+(dirClass?' '+dirClass:'');
  const deltaEl = el.querySelector('.panel-delta');
  deltaEl.innerHTML = (delta.dir==='up'?'\u25B2':delta.dir==='down'?'\u25BC':'')+delta.val+'%';
  const chartWrap = el.querySelector('.panel-chart');
  chartWrap.innerHTML = '';
  chartWrap.appendChild(renderSparkline(p));
  const previewEl = el.querySelector('.panel-preview');
  previewEl.textContent = getPreviewText(p);
  el.querySelector('.panel-rank').textContent = '#'+(rank+1);
  const lockBtn = el.querySelector('.panel-ctrl');
  if(lockBtn) lockBtn.innerHTML = locked?'\u{1F512}':'\u{1F513}';
}
function renderGrid(){
  const grid = el('grid');
  const existing = new Map();
  for(const child of grid.children){
    if(child.classList.contains('panel')) existing.set(child.dataset.panelId,child);
  }
  grid.innerHTML = '';
  const rankedIds = orderedIds.slice();
  const compactThreshold = Math.max(3,Math.floor(rankedIds.length*0.65));
  for(const p of panels){
    p.compactMode = rankedIds.indexOf(p.id)>=compactThreshold && !p.locked;
  }
  for(let i=0;i<rankedIds.length;i++){
    const pid = rankedIds[i];
    const panel = panels.find(p=>p.id===pid);
    if(!panel) continue;
    const rank = i;
    const existingEl = existing.get(pid);
    if(existingEl){
      updatePanelEl(panel,rank);
      panel.el = existingEl;
      positionPanel(existingEl,rank,rankedIds.length);
      grid.appendChild(existingEl);
    }else{
      const el = createPanelEl(panel,rank);
      positionPanel(el,rank,rankedIds.length);
      grid.appendChild(el);
    }
  }
  updateMoreIndicator();
  el('session-score').textContent = sessionScore;
}
function positionPanel(el,rank,total){
  const row = Math.floor(rank/4)*2;
  const col = rank%4;
  const isTop = rank<4;
  const isHigh = rank<3;
  if(isHigh){
    el.style.gridColumn = (col+1)+' / span 2';
    el.style.gridRow = (row+1)+' / span 2';
  }else if(isTop){
    el.style.gridColumn = (col+1)+' / span 1';
    el.style.gridRow = (row+1)+' / span 2';
  }else{
    el.style.gridColumn = (col+1)+' / span 1';
    el.style.gridRow = (row+1)+' / span 1';
  }
}
function updateMoreIndicator(){
  const grid = el('grid');
  let more = grid.querySelector('.more-section');
  const compactCount = panels.filter(p=>p.compactMode&&!p.locked).length;
  if(compactCount>2 && panels.length>6){
    if(!more){
      more = createEl('div',{
        className:'more-section',
        role:'button',
        tabindex:'0',
        aria:{label:`Show ${compactCount} compacted panels`},
        onclick(){expandAllCompact()},
        onkeydown(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();expandAllCompact()}}
      });
      grid.appendChild(more);
    }
    more.innerHTML = '';
    more.appendChild(createEl('span',{},[`+${compactCount} more panels`]));
    more.appendChild(createEl('span',{className:'more-count'},[String(compactCount)]));
  }else if(more){
    more.remove();
  }
}
function expandAllCompact(){
  for(const p of panels){
    if(p.compactMode && !p.locked){
      p.compactMode = false;
      recordInteraction(p.id);
    }
  }
  computeScores();
  renderGrid();
  saveState();
}
function toggleLock(id){
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  p.locked = !p.locked;
  if(p.locked) p.compactMode = false;
  computeScores();
  renderGrid();
  saveState();
  announce(`${p.title} ${p.locked?'locked':'unlocked'}`);
}
function toggleCompact(id){
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  if(p.locked) return;
  p.compactMode = !p.compactMode;
  tracking[id].interactions++;
  tracking[id].lastInteraction = Date.now();
  if(p.compactMode) tracking[id].collapses++;
  else tracking[id].expands++;
  computeScores();
  renderGrid();
  saveState();
  announce(`${p.title} ${p.compactMode?'compacted':'expanded'}`);
}
function movePanel(id,dir){
  const idx = orderedIds.indexOf(id);
  if(idx===-1) return;
  const newIdx = Math.max(0,Math.min(orderedIds.length-1,idx+dir));
  if(newIdx===idx) return;
  orderedIds.splice(idx,1);
  orderedIds.splice(newIdx,0,id);
  const p = panels.find(x=>x.id===id);
  if(p) p.locked = true;
  renderGrid();
  saveState();
}
function recordInteraction(id){
  if(!tracking[id]) return;
  tracking[id].interactions++;
  tracking[id].lastInteraction = Date.now();
}
function announce(msg){
  let ann = document.getElementById('sr-announce');
  if(!ann){
    ann = document.createElement('div');
    ann.id = 'sr-announce';
    ann.className = 'sr-only';
    ann.setAttribute('aria-live','assertive');
    ann.setAttribute('aria-atomic','true');
    document.body.appendChild(ann);
  }
  ann.textContent = msg;
}
function startDrag(e,panelId){
  if(panels.find(p=>p.id===panelId)?.locked) return;
  e.preventDefault();
  const clientX = e.touches?e.touches[0].clientX:e.clientX;
  const clientY = e.touches?e.touches[0].clientY:e.clientY;
  const sourceEl = panels.find(p=>p.id===panelId)?.el;
  if(!sourceEl) return;
  dragState = {panelId,sourceEl,startX:clientX,startY:clientY,offsetX:0,offsetY:0};
  sourceEl.classList.add('dragging');
  document.addEventListener('mousemove',onDragMove);
  document.addEventListener('mouseup',onDragEnd);
  document.addEventListener('touchmove',onDragMove,{passive:false});
  document.addEventListener('touchend',onDragEnd);
}
function onDragMove(e){
  if(!dragState) return;
  e.preventDefault();
  const clientX = e.touches?e.touches[0].clientX:e.clientX;
  const clientY = e.touches?e.touches[0].clientY:e.clientY;
  dragState.offsetX = clientX-dragState.startX;
  dragState.offsetY = clientY-dragState.startY;
  dragState.sourceEl.style.transform = `translate(${dragState.offsetX}px,${dragState.offsetY}px)`;
  const target = document.elementFromPoint(clientX,clientY);
  const panelEl = target?.closest('.panel');
  document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  if(panelEl && panelEl!==dragState.sourceEl){
    panelEl.classList.add('drag-over');
  }
}
function onDragEnd(e){
  if(!dragState) return;
  const clientX = e.changedTouches?e.changedTouches[0].clientX:e.clientX;
  const clientY = e.changedTouches?e.changedTouches[0].clientY:e.clientY;
  const target = document.elementFromPoint(clientX,clientY);
  const targetPanel = target?.closest('.panel');
  dragState.sourceEl.classList.remove('dragging');
  dragState.sourceEl.style.transform = '';
  document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  if(targetPanel && targetPanel!==dragState.sourceEl){
    const targetId = targetPanel.dataset.panelId;
    const srcIdx = orderedIds.indexOf(dragState.panelId);
    const tgtIdx = orderedIds.indexOf(targetId);
    if(srcIdx!==-1 && tgtIdx!==-1){
      orderedIds.splice(srcIdx,1);
      orderedIds.splice(tgtIdx,0,dragState.panelId);
      const p = panels.find(x=>x.id===dragState.panelId);
      if(p) p.locked = true;
    }
  }
  document.removeEventListener('mousemove',onDragMove);
  document.removeEventListener('mouseup',onDragEnd);
  document.removeEventListener('touchmove',onDragMove);
  document.removeEventListener('touchend',onDragEnd);
  dragState = null;
  computeScores();
  renderGrid();
  saveState();
}
function setupTracking(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    const now = Date.now();
    for(const entry of entries){
      const pid = entry.target.dataset.panelId;
      if(!pid) continue;
      if(entry.isIntersecting){
        if(!viewStartMap[pid]) viewStartMap[pid]=now;
        visibilityMap[pid]=true;
      }else{
        if(viewStartMap[pid]){
          const elapsed = now-viewStartMap[pid];
          if(tracking[pid]) tracking[pid].viewTime += elapsed;
          delete viewStartMap[pid];
        }
        visibilityMap[pid]=false;
      }
    }
    flushViewTimes();
  },{threshold:0.3});
  for(const p of panels){
    if(p.el) observer.observe(p.el);
  }
}
function flushViewTimes(){
  const now = Date.now();
  for(const pid of Object.keys(viewStartMap)){
    const elapsed = now-viewStartMap[pid];
    if(tracking[pid] && elapsed>0){
      tracking[pid].viewTime += elapsed;
      viewStartMap[pid]=now;
    }
  }
}
function rescoreLoop(){
  if(scoreTimer) clearTimeout(scoreTimer);
  scoreTimer = setTimeout(()=>{
    flushViewTimes();
    computeScores();
    renderGrid();
    saveState();
    rescoreLoop();
  },SCORE_INTERVAL);
}
function fetchLiveData(){
  return fetch('/api/metrics',{signal:AbortSignal.timeout(3000)})
    .then(r=>r.json())
    .then(data=>{
      for(const p of panels){
        if(data[p.id]!==undefined) p.value = data[p.id];
        else p.value = generateValue(p);
        p.history.push({t:Date.now(),v:p.value});
        if(p.history.length>60) p.history.shift();
      }
      useLiveData = true;
      updateSourceIndicator();
    })
    .catch(()=>{
      updateValues();
      useLiveData = false;
      updateSourceIndicator();
    });
}
function updateSourceIndicator(){
  const dot = document.querySelector('.data-source .dot');
  const label = el('source-label');
  if(useLiveData){
    dot.classList.remove('mock');
    label.textContent = 'live API';
  }else{
    dot.classList.add('mock');
    label.textContent = 'mock data';
  }
}
function tick(){
  if(useLiveData){
    fetchLiveData();
  }else{
    updateValues();
  }
  for(const p of panels){
    if(p.el){
      const chartWrap = p.el.querySelector('.panel-chart');
      if(chartWrap){
        chartWrap.innerHTML = '';
        chartWrap.appendChild(renderSparkline(p));
      }
      const metricEl = p.el.querySelector('.panel-metric');
      const delta = getDelta(p);
      const dirClass = delta.dir==='up'?'up':delta.dir==='down'?'down':'';
      if(metricEl){
        metricEl.textContent = formatValue(p)+p.unit;
        metricEl.className = 'panel-metric'+(dirClass?' '+dirClass:'');
      }
      const deltaEl = p.el.querySelector('.panel-delta');
      if(deltaEl){
        deltaEl.innerHTML = (delta.dir==='up'?'\u25B2':delta.dir==='down'?'\u25BC':'')+delta.val+'%';
      }
      const previewEl = p.el.querySelector('.panel-preview');
      if(previewEl) previewEl.textContent = getPreviewText(p);
    }
  }
}
function init(){
  initPanels();
  updateValues();
  computeScores();
  renderGrid();
  setupTracking();
  rescoreLoop();
  dataInterval = setInterval(tick,5000);
  el('btn-reset').addEventListener('click',()=>{
    localStorage.removeItem(STORAGE_KEY);
    tracking = {};
    for(const p of panels){
      tracking[p.id] = {viewTime:0,interactions:0,lastInteraction:0,collapses:0,expands:0};
    }
    orderedIds = panels.map(p=>p.id);
    for(const p of panels){p.locked=false;p.compactMode=false}
    sessionScore = 0;
    renderGrid();
    setupTracking();
    saveState();
    announce('All tracking data and layout reset');
  });
  el('btn-auto').addEventListener('click',()=>{
    flushViewTimes();
    computeScores();
    for(const p of panels) p.locked = false;
    renderGrid();
    saveState();
    announce('Auto-layout applied based on attention scores');
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Tab') document.body.classList.add('keyboard-user');
  });
  document.addEventListener('mousedown',()=>{
    document.body.classList.remove('keyboard-user');
  });
  fetchLiveData();
  announce('Dashboard ready. '+panels.length+' panels tracking user attention. Use Ctrl+L to lock, Ctrl+C to compact, Ctrl+arrows to move panels.');
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
else init();
})();
</script>
</body>
</html>