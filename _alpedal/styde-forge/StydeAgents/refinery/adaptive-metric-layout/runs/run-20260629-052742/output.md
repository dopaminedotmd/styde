<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e3e8;--muted:#6b7080;
  --accent:#7c8aff;--accent2:#50e3c2;--accent3:#ff6b8a;--compact-scale:0.45;
  --rank-0-w:3fr;--rank-1-w:2fr;--rank-2-w:1fr;--rank-3-w:1fr;--rank-4-w:1fr;
  --rank-0-h:280px;--rank-1-h:220px;--rank-2-h:160px;--rank-3-h:120px;--rank-4-h:100px;
}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;padding:16px;min-height:100vh}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:8px}
header h1{font-size:1.3rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.controls button{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.82rem;transition:all .15s}
.controls button:hover{background:var(--border)}
.controls button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.stats-bar{display:flex;gap:16px;margin-bottom:16px;font-size:0.78rem;color:var(--muted);flex-wrap:wrap}
.stats-bar span{background:var(--surface);padding:4px 10px;border-radius:4px}
.stat-val{color:var(--accent2);font-weight:600}
#grid{display:grid;gap:12px;grid-template-columns:repeat(6,1fr);grid-auto-rows:minmax(100px,auto);transition:all .35s ease}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;position:relative;overflow:hidden;transition:all .35s ease;cursor:grab;display:flex;flex-direction:column;min-height:100px}
.panel:hover{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.dragging{opacity:0.7;cursor:grabbing;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,0.5);transform:scale(1.02)}
.panel.locked{border-color:var(--accent3);cursor:default}
.panel.locked:hover{box-shadow:0 0 0 1px var(--accent3)}
.panel.compact{padding:8px;min-height:60px;font-size:0.72rem}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header h3{font-size:0.78rem}
.panel.compact .panel-meta{font-size:0.65rem}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px}
.panel-header h3{font-size:0.88rem;font-weight:600;margin:0;line-height:1.2}
.panel-actions{display:flex;gap:4px}
.panel-actions button{background:none;border:1px solid transparent;color:var(--muted);cursor:pointer;padding:2px 6px;border-radius:4px;font-size:0.7rem;transition:all .15s}
.panel-actions button:hover{color:var(--text);border-color:var(--border);background:rgba(255,255,255,0.04)}
.panel-actions button.locked-btn{color:var(--accent3)}
.panel-actions button.locked-btn:hover{border-color:var(--accent3)}
.panel-body{flex:1;display:flex;align-items:center;justify-content:center;min-height:40px;font-size:0.82rem;color:var(--muted)}
.panel-rank-badge{position:absolute;top:6px;right:6px;font-size:0.6rem;background:var(--accent);color:#fff;padding:1px 6px;border-radius:10px;opacity:0.85}
.panel-meta{display:flex;justify-content:space-between;font-size:0.68rem;color:var(--muted);margin-top:4px;border-top:1px solid var(--border);padding-top:4px}
.score-indicator{display:flex;gap:6px;align-items:center}
.score-dot{width:8px;height:8px;border-radius:50%;background:var(--muted)}
.score-dot.high{background:var(--accent2)}
.score-dot.mid{background:var(--accent)}
.score-dot.low{background:var(--accent3)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.score-dot.active{animation:pulse 2s infinite}
.drop-zone-indicator{position:fixed;pointer-events:none;z-index:200;border:2px dashed var(--accent);border-radius:10px;background:rgba(124,138,255,0.08);display:none}
.compact-bin{padding:12px;margin-top:8px;border:1px dashed var(--border);border-radius:10px;display:flex;flex-wrap:wrap;gap:8px;min-height:80px;align-items:flex-start;align-content:flex-start}
.compact-bin h4{width:100%;font-size:0.75rem;color:var(--muted);margin:0;font-weight:500}
.compact-bin .panel{flex:0 1 180px;min-height:60px;font-size:0.72rem;padding:8px}
.compact-bin .panel .panel-body{display:none}
</style>
</head>
<body>
<header>
<h1>Adaptive Metric Dashboard</h1>
<div class="controls">
<button id="btn-auto" class="active" title="Auto-arrange panels by score">Auto Layout</button>
<button id="btn-reset" title="Reset all tracking data">Reset Stats</button>
<button id="btn-snapshot" title="Copy layout JSON to clipboard">Copy Layout</button>
</div>
</header>
<div class="stats-bar">
<span>Sessions: <b class="stat-val" id="stat-sessions">1</b></span>
<span>Total views: <b class="stat-val" id="stat-views">0</b></span>
<span>Active panels: <b class="stat-val" id="stat-active">6</b></span>
<span>Compact panels: <b class="stat-val" id="stat-compact">0</b></span>
</div>
<div id="grid"></div>
<div class="compact-bin" id="compact-bin">
<h4>COMPACT / LOW USAGE</h4>
</div>
<script>
(function(){
const LS_KEY='adaptive_dashboard_v1';
const DECAY_FLOOR=0.01;
const DECAY_HALF_LIFE_MS=7*24*60*60*1000;
const COMPACT_THRESHOLD=0.08;
const COMPACT_LIMIT=3;
const VIEW_INTERVAL_MS=2000;
const MIN_VIEW_MS=500;
const RECENCY_WEIGHT=0.3;
const FREQUENCY_WEIGHT=0.4;
const DURATION_WEIGHT=0.3;
let panels=[];
let scoreCache=new Map();
let scoreCacheVersion=0;
let observers=new Map();
let observerRefs=null;
let dragState=null;
let manualOverrides=new Map();
let isAutoLayout=true;
let sessions=1;
let viewTimers=new Map();
const defaultPanelDefs=[
  {id:'cpu',title:'CPU Usage',metric:'cpu',content:'<svg width="100%" height="60"><rect x="0" y="40" width="8" height="10" fill="var(--accent2)" rx="1"/><rect x="12" y="30" width="8" height="20" fill="var(--accent2)" rx="1"/><rect x="24" y="15" width="8" height="35" fill="var(--accent2)" rx="1"/><rect x="36" y="8" width="8" height="42" fill="var(--accent2)" rx="1"/><rect x="48" y="20" width="8" height="30" fill="var(--accent2)" rx="1"/><rect x="60" y="5" width="8" height="45" fill="var(--accent2)" rx="1"/><rect x="72" y="12" width="8" height="38" fill="var(--accent2)" rx="1"/><text x="0" y="58" fill="var(--muted)" font-size="8">1m 5m 15m load: 0.8 / 0.6 / 0.4</text></svg>'},
  {id:'mem',title:'Memory',metric:'memory','content':'<div style="text-align:center"><div style="font-size:2rem;font-weight:700;color:var(--accent)">68%</div><div style="font-size:0.7rem;color:var(--muted)">11.2 GB / 16 GB</div><div style="width:80%;height:6px;background:var(--border);border-radius:3px;margin:8px auto"><div style="width:68%;height:100%;background:var(--accent);border-radius:3px"></div></div></div>'},
  {id:'disk',title:'Disk I/O',metric:'disk','content':'<div style="display:flex;gap:16px;justify-content:center;align-items:center;height:100%"><div style="text-align:center"><div style="font-size:1.4rem;font-weight:700;color:var(--accent2)">320</div><div style="font-size:0.7rem;color:var(--muted)">MB/s read</div></div><div style="text-align:center"><div style="font-size:1.4rem;font-weight:700;color:var(--accent3)">180</div><div style="font-size:0.7rem;color:var(--muted)">MB/s write</div></div></div>'},
  {id:'net',title:'Network',metric:'network','content':'<div style="display:flex;gap:16px;justify-content:center;align-items:center;height:100%"><div style="text-align:center"><div style="font-size:1.4rem;font-weight:700;color:var(--accent)">2.4</div><div style="font-size:0.7rem;color:var(--muted)">Gbps ↓</div></div><div style="text-align:center"><div style="font-size:1.4rem;font-weight:700;color:var(--accent2)">0.8</div><div style="font-size:0.7rem;color:var(--muted)">Gbps ↑</div></div></div>'},
  {id:'errors',title:'Error Rate',metric:'errors','content':'<div style="text-align:center"><div style="font-size:2rem;font-weight:700;color:var(--accent3)">0.02%</div><div style="font-size:0.7rem;color:var(--muted)">Last 24h: 12 errors</div><div style="width:80%;height:6px;background:var(--border);border-radius:3px;margin:8px auto"><div style="width:2%;height:100%;background:var(--accent3);border-radius:3px"></div></div></div>'},
  {id:'requests',title:'Requests/min',metric:'requests','content':'<div style="text-align:center"><div style="font-size:2rem;font-weight:700;color:var(--accent2)">14.2k</div><div style="font-size:0.7rem;color:var(--muted)">Avg response: 42ms</div><div style="width:80%;height:6px;background:var(--border);border-radius:3px;margin:8px auto;overflow:hidden"><div style="width:71%;height:100%;background:linear-gradient(90deg,var(--accent2),var(--accent));border-radius:3px"></div></div></div>'}
];
function loadState(){
  try{
    const raw=localStorage.getItem(LS_KEY);
    if(!raw) return {panels:defaultPanelDefs.map(cloneDef),overrides:{},sessions:1};
    const data=JSON.parse(raw);
    const savedPanels=data.panels||[];
    const merged=defaultPanelDefs.map(def=>{
      const saved=savedPanels.find(p=>p.id===def.id);
      if(!saved) return cloneDef(def);
      return {
        ...cloneDef(def),
        views:saved.views||0,
        totalDuration:saved.totalDuration||0,
        lastViewed:saved.lastViewed||0,
        score:saved.score||0,
        compact:saved.compact||false,
        locked:saved.locked||false
      };
    });
    return {
      panels:merged,
      overrides:data.overrides||{},
      sessions:(data.sessions||0)+1
    };
  }catch(e){return {panels:defaultPanelDefs.map(cloneDef),overrides:{},sessions:1};}
}
function cloneDef(d){return{...d,views:0,totalDuration:0,lastViewed:0,score:0,compact:false,locked:false};}
function saveState(){
  const data={panels,sessions,overrides:Object.fromEntries(manualOverrides)};
  try{localStorage.setItem(LS_KEY,JSON.stringify(data));}catch(e){}
}
function computeScore(p){
  const now=Date.now();
  const recency=p.lastViewed?(now-p.lastViewed)/DECAY_HALF_LIFE_MS:999;
  const recencyFactor=Math.max(DECAY_FLOOR,Math.exp(-recency*Math.LN2));
  const freqNorm=Math.min(p.views/100,1);
  const durNorm=Math.min(p.totalDuration/(60*60*1000),1);
  let score=(freqNorm*FREQUENCY_WEIGHT)+(durNorm*DURATION_WEIGHT)+(recencyFactor*RECENCY_WEIGHT);
  score=Math.max(DECAY_FLOOR,Math.min(score,1));
  return score;
}
function getScore(p){
  const cacheKey=p.id+'|'+p.views+'|'+p.totalDuration+'|'+p.lastViewed+'|'+scoreCacheVersion;
  if(scoreCache.has(cacheKey)) return scoreCache.get(cacheKey);
  const s=computeScore(p);
  scoreCache.set(cacheKey,s);
  return s;
}
function rankPanels(){
  return panels.map(p=>({...p,score:getScore(p),locked:p.locked||manualOverrides.has(p.id)})).sort((a,b)=>b.score-a.score);
}
function assignLayout(ranked){
  const result=[];
  const compactBin=[];
  const overrides=[];
  ranked.forEach((p,i)=>{
    if(p.locked||manualOverrides.has(p.id)){
      overrides.push(p);
      return;
    }
    if(!p.compact&&i>=panels.length-COMPACT_LIMIT&&p.score<COMPACT_THRESHOLD){
      p.compact=true;
    }
    if(p.compact||p.score<COMPACT_THRESHOLD){
      compactBin.push(p);
    }else{
      result.push(p);
    }
  });
  result.sort((a,b)=>b.score-a.score);
  overrides.forEach(p=>result.push(p));
  return {main:result,compact:compactBin};
}
function getGridStyle(p,rank){
  if(p.compact) return 'grid-column:span 1;grid-row:span 1;';
  if(rank===0) return 'grid-column:span 3;grid-row:span 2;';
  if(rank===1) return 'grid-column:span 3;grid-row:span 2;';
  if(rank===2) return 'grid-column:span 2;grid-row:span 1;';
  if(rank===3) return 'grid-column:span 2;grid-row:span 1;';
  if(rank===4) return 'grid-column:span 2;grid-row:span 1;';
  return 'grid-column:span 1;grid-row:span 1;';
}
function scoreClass(score){
  if(score>=0.6) return 'high';
  if(score>=0.3) return 'mid';
  return 'low';
}
function render(){
  const ranked=rankPanels();
  const layout=assignLayout(ranked);
  const grid=document.getElementById('grid');
  const compactBin=document.getElementById('compact-bin');
  grid.innerHTML='';
  layout.main.forEach((p,rank)=>{
    const el=createPanelElement(p,rank);
    grid.appendChild(el);
  });
  const h4=compactBin.querySelector('h4');
  compactBin.innerHTML='';
  compactBin.appendChild(h4||document.createElement('h4'));
  if(!compactBin.querySelector('h4')){
    const nh4=document.createElement('h4');
    nh4.textContent='COMPACT / LOW USAGE';
    compactBin.appendChild(nh4);
  }
  layout.compact.forEach((p,rank)=>{
    const el=createPanelElement(p,rank);
    el.classList.add('compact');
    compactBin.appendChild(el);
  });
  updateStats();
  panels.forEach(p=>{p.score=getScore(p);});
}
function createPanelElement(p,rank){
  const el=document.createElement('div');
  el.className='panel';
  el.dataset.panelId=p.id;
  el.setAttribute('style',getGridStyle(p,rank));
  if(p.locked||manualOverrides.has(p.id)) el.classList.add('locked');
  if(p.compact) el.classList.add('compact');
  el.draggable=true;
  el.innerHTML=`
    <div class="panel-header">
      <h3>${p.title}</h3>
      <div class="panel-actions">
        <button class="expand-btn" title="${p.compact?'Expand':'Compact'}">${p.compact?'↔':'⊟'}</button>
        <button class="locked-btn${p.locked||manualOverrides.has(p.id)?' locked-btn':''}" title="Lock position">${p.locked||manualOverrides.has(p.id)?'🔒':'🔓'}</button>
      </div>
    </div>
    <div class="panel-body">${p.content}</div>
    <div class="panel-meta">
      <span>Views: ${p.views} | Time: ${fmtDuration(p.totalDuration)}</span>
      <span class="score-indicator">Score: ${(p.score||getScore(p)).toFixed(3)} <span class="score-dot ${scoreClass(p.score||getScore(p))}${p.views>0&&p.lastViewed&&(Date.now()-p.lastViewed)<30000?' active':''}"></span></span>
    </div>
  `;
  if(!p.compact&&!p.locked&&!manualOverrides.has(p.id)){
    el.addEventListener('dragstart',handleDragStart);
    el.addEventListener('dragend',handleDragEnd);
  }
  el.addEventListener('dragover',e=>e.preventDefault());
  el.addEventListener('drop',handleDrop);
  el.querySelector('.expand-btn').addEventListener('click',e=>{
    e.stopPropagation();
    toggleCompact(p.id);
  });
  el.querySelector('.locked-btn').addEventListener('click',e=>{
    e.stopPropagation();
    toggleLock(p.id);
  });
  el.addEventListener('click',()=>recordInteraction(p.id,'click'));
  setupObserver(el,p.id);
  return el;
}
function setupObserver(el,pid){
  if(observers.has(pid)){
    const old=observers.get(pid);
    if(old.target===el) return;
    old.unobserve(old.target);
    old.disconnect();
  }
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      const p=panels.find(x=>x.id===pid);
      if(!p) return;
      if(entry.isIntersecting){
        const start=Date.now();
        viewTimers.set(pid,start);
      }else{
        const start=viewTimers.get(pid);
        if(start){
          const dur=Date.now()-start;
          if(dur>=MIN_VIEW_MS){
            p.views++;
            p.totalDuration+=dur;
            p.lastViewed=Date.now();
            scoreCacheVersion++;
          }
          viewTimers.delete(pid);
        }
      }
    });
  },{threshold:0.5});
  obs.observe(el);
  observers.set(pid,obs);
}
function recordInteraction(pid,type){
  const p=panels.find(x=>x.id===pid);
  if(!p) return;
  if(type==='click'){p.views++;p.lastViewed=Date.now();scoreCacheVersion++;}
}
function toggleCompact(pid){
  const p=panels.find(x=>x.id===pid);
  if(!p) return;
  p.compact=!p.compact;
  saveState();
  render();
}
function toggleLock(pid){
  const p=panels.find(x=>x.id===pid);
  if(!p) return;
  if(manualOverrides.has(pid)){
    manualOverrides.delete(pid);
    p.locked=false;
  }else{
    manualOverrides.set(pid,{locked:true,position:null});
    p.locked=true;
  }
  saveState();
  render();
}
function handleDragStart(e){
  const pid=e.target.closest('.panel')?.dataset.panelId;
  if(!pid) return;
  const p=panels.find(x=>x.id===pid);
  if(!p||p.locked||manualOverrides.has(pid)){e.preventDefault();return;}
  dragState={pid,startX:e.clientX,startY:e.clientY};
  e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed='move';
  e.dataTransfer.setData('text/plain',pid);
}
function handleDragEnd(e){
  e.target.classList.remove('dragging');
  if(!dragState) return;
  const dx=e.clientX-dragState.startX;
  const dy=e.clientY-dragState.startY;
  if(Math.abs(dx)<10&&Math.abs(dy)<10){dragState=null;return;}
  const gridEl=document.getElementById('grid');
  const gridRect=gridEl.getBoundingClientRect();
  const cols=getComputedStyle(gridEl).gridTemplateColumns.split(' ').length;
  const cellW=gridRect.width/cols;
  const cellH=120;
  const relX=(e.clientX-gridRect.left)/cellW;
  const relY=(e.clientY-gridRect.top)/cellH;
  const targetCol=Math.max(0,Math.min(cols-1,Math.floor(relX)));
  const targetRow=Math.max(0,Math.floor(relY));
  manualOverrides.set(dragState.pid,{locked:true,position:{col:targetCol,row:targetRow}});
  const p=panels.find(x=>x.id===dragState.pid);
  if(p) p.locked=true;
  saveState();
  render();
  dragState=null;
}
function handleDrop(e){
  e.preventDefault();
  const pid=e.dataTransfer.getData('text/plain');
  if(!pid) return;
}
function fmtDuration(ms){
  if(ms<1000) return '0s';
  if(ms<60000) return Math.round(ms/1000)+'s';
  if(ms<3600000) return Math.round(ms/60000)+'m';
  return Math.round(ms/3600000)+'h';
}
function updateStats(){
  document.getElementById('stat-sessions').textContent=sessions;
  document.getElementById('stat-views').textContent=panels.reduce((s,p)=>s+p.views,0);
  document.getElementById('stat-active').textContent=panels.filter(p=>!p.compact).length;
  document.getElementById('stat-compact').textContent=panels.filter(p=>p.compact).length;
}
function resetStats(){
  panels.forEach(p=>{p.views=0;p.totalDuration=0;p.lastViewed=0;p.score=0;p.compact=false;p.locked=false;});
  manualOverrides.clear();
  scoreCache.clear();
  scoreCacheVersion++;
  observers.forEach(o=>{try{o.disconnect();}catch(e){}});
  observers.clear();
  viewTimers.clear();
  saveState();
  render();
}
function init(){
  const state=loadState();
  panels=state.panels;
  sessions=state.sessions;
  if(state.overrides){
    Object.entries(state.overrides).forEach(([k,v])=>manualOverrides.set(k,v));
  }
  render();
  setInterval(()=>{
    viewTimers.forEach((start,pid)=>{
      if(Date.now()-start>=VIEW_INTERVAL_MS){
        const p=panels.find(x=>x.id===pid);
        if(p){
          p.totalDuration+=VIEW_INTERVAL_MS;
          p.lastViewed=Date.now();
          scoreCacheVersion++;
        }
        viewTimers.set(pid,Date.now());
      }
    });
    saveState();
  },VIEW_INTERVAL_MS);
  document.getElementById('btn-auto').addEventListener('click',()=>{
    isAutoLayout=true;
    document.getElementById('btn-auto').classList.add('active');
    render();
  });
  document.getElementById('btn-reset').addEventListener('click',resetStats);
  document.getElementById('btn-snapshot').addEventListener('click',()=>{
    const snap={panels,sessions,layout:rankPanels().map(p=>({id:p.id,score:p.score,compact:p.compact,locked:p.locked}))};
    navigator.clipboard.writeText(JSON.stringify(snap,null,2)).then(()=>{
      const btn=document.getElementById('btn-snapshot');
      btn.textContent='Copied!';
      setTimeout(()=>btn.textContent='Copy Layout',1500);
    });
  });
}
document.addEventListener('DOMContentLoaded',init);
})();
</script>
</body>
</html>