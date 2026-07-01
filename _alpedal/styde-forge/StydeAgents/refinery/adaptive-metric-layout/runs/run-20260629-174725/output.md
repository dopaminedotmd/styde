<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Adaptive Metric Layout</title><style>
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4ed;--muted:#8b8fa3;--accent:#6366f1;--accent2:#22d3ee;--warn:#f59e0b;--danger:#ef4444;--success:#10b981;--rank1:#6366f1;--rank2:#8b5cf6;--rank3:#3b82f6;--rank4:#06b6d4;--compact:#1f2233;--pin:#f59e0b}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.btn{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:all 0.15s}
.btn:hover{background:var(--border)}
.btn.active{background:var(--accent);border-color:var(--accent)}
.badge{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:3px 10px;font-size:0.7rem;color:var(--muted)}
.grid{display:grid;gap:12px;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(120px,auto);transition:all 0.4s cubic-bezier(0.4,0,0.2,1)}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:500px){.grid{grid-template-columns:1fr}}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;position:relative;overflow:hidden;transition:grid-column 0.4s cubic-bezier(0.4,0,0.2,1),grid-row 0.4s cubic-bezier(0.4,0,0.2,1)}
.panel.rank-1{border-color:var(--rank1);box-shadow:0 0 20px rgba(99,102,241,0.12)}
.panel.rank-2{border-color:var(--rank2)}
.panel.rank-3{border-color:var(--rank3)}
.panel.compact{background:var(--compact);padding:8px 14px;min-height:48px;display:flex;align-items:center;gap:10px}
.panel.compact .body,.panel.compact .chart{display:none}
.panel.compact .expand-btn{display:inline-flex}
.panel .expand-btn{display:none}
.panel.pinned::after{content:'📌';position:absolute;top:6px;right:36px;font-size:0.7rem;opacity:0.7}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;gap:8px}
.panel.compact .panel-header{margin-bottom:0;flex:1}
.panel-title{font-weight:600;font-size:0.85rem;display:flex;align-items:center;gap:6px}
.panel-title .icon{font-size:1.1rem}
.panel-actions{display:flex;gap:4px;align-items:center}
.panel-actions button{background:none;border:none;color:var(--muted);cursor:pointer;padding:2px 4px;border-radius:4px;font-size:0.75rem;transition:all 0.15s}
.panel-actions button:hover{color:var(--text);background:var(--border)}
.panel-actions button.pinned-btn{color:var(--pin)}
.metric-value{font-size:2rem;font-weight:700;line-height:1;letter-spacing:-0.03em}
.metric-label{font-size:0.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.05em}
.spark{display:flex;align-items:flex-end;gap:2px;height:40px;margin-top:8px}
.spark-bar{flex:1;min-width:3px;border-radius:2px 2px 0 0;background:var(--accent);transition:height 0.3s}
.panel.rank-1 .spark-bar{background:var(--rank1)}
.panel.rank-2 .spark-bar{background:var(--rank2)}
.panel.rank-3 .spark-bar{background:var(--rank3)}
.compact-metric{font-size:0.8rem;font-weight:600;white-space:nowrap}
.compact-spark{display:flex;align-items:flex-end;gap:1px;height:16px;flex:1;max-width:100px}
.compact-spark .spark-bar{min-width:2px}
.score-badge{font-size:0.65rem;color:var(--muted);background:var(--bg);padding:1px 6px;border-radius:8px;margin-left:auto}
.rank-dot{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0}
.rank-dot.r1{background:var(--rank1)}
.rank-dot.r2{background:var(--rank2)}
.rank-dot.r3{background:var(--rank3)}
.rank-dot.r4{background:var(--rank4)}
.rank-dot.rl{background:var(--muted)}
.pos-arrows{display:flex;gap:1px;flex-direction:column}
.pos-arrows button{font-size:0.55rem;padding:0 3px;line-height:1.2}
.toolbar{display:flex;gap:6px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
.fade-out{opacity:0.4}
.stats-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.stat-pill{font-size:0.7rem;color:var(--muted)}
.stat-pill span{color:var(--text);font-weight:600}
</style></head><body>
<header><h1>⚡ Adaptive Metric Layout</h1><div class=controls><button class="btn" id=btnReset title="Reset all tracking data">Reset</button><button class="btn" id=btnLockAll title="Lock all panels in place">Lock All</button><button class="btn" id=btnUnlockAll title="Unlock all panels">Unlock All</button><span class=badge id=updateBadge>Idle</span></div></header>
<div class=toolbar><span class=badge>Auto-layout: active</span><span class=badge id=trackBadge>Tracking: 0 panels</span></div>
<div class=grid id=grid></div>
<script>
(function(){
const LS_KEY='adaptive_layout_v1';
const DECAY_HALF=300000;
const RANK_TICK=5000;
const COMPACT_THRESHOLD=0.30;
const MAX_PANELS=8;
let panels=[],ranks=[],layout={},pinned=new Set(),manualPos={},compactState={};
let viewTimers={},interactions={};
function loadState(){
 try{
  const raw=localStorage.getItem(LS_KEY);
  if(!raw)return;
  const s=JSON.parse(raw);
  if(s.p)panels=s.p;
  if(s.i)interactions=s.i;
  if(s.pn)Array.isArray(s.pn)&&s.pn.forEach(k=>pinned.add(k));
  if(s.mp)manualPos=s.mp;
  if(s.cs)compactState=s.cs;
 }catch(e){}
}
function saveState(){
 try{
  const s={p:panels,i:interactions,pn:[...pinned],mp:manualPos,cs:compactState,ts:Date.now()};
  localStorage.setItem(LS_KEY,JSON.stringify(s));
 }catch(e){}
}
function initPanels(){
 if(panels.length===0){
  panels=[
   {id:'cpu',icon:'🖥',title:'CPU Usage',unit:'%',val:23,history:genHistory(42,18)},
   {id:'mem',icon:'🧠',title:'Memory',unit:'GB',val:7.2,history:genHistory(8.5,6)},
   {id:'net',icon:'🌐',title:'Network I/O',unit:'Mbps',val:342,history:genHistory(400,200)},
   {id:'req',icon:'📡',title:'Request Rate',unit:'rps',val:1250,history:genHistory(1400,800)},
   {id:'err',icon:'🚨',title:'Error Rate',unit:'%',val:0.3,history:genHistory(1.5,0.1)},
   {id:'lat',icon:'⏱',title:'Latency p95',unit:'ms',val:45,history:genHistory(80,30)},
   {id:'disk',icon:'💾',title:'Disk Usage',unit:'%',val:68,history:genHistory(75,55)},
   {id:'usr',icon:'👥',title:'Active Users',unit:'',val:3842,history:genHistory(4200,2500)}
  ];
  panels.forEach(p=>{
   if(!interactions[p.id])interactions[p.id]={count:0,totalDur:0,lastTs:0,viewStart:null};
  });
 }
}
function genHistory(max,min){const a=[];for(let i=0;i<14;i++)a.push(Math.round(min+Math.random()*(max-min)));return a}
function computeScore(panelId){
 const i=interactions[panelId]||{count:0,totalDur:0,lastTs:0};
 const now=Date.now();
 const recencyFactor=Math.exp(-Math.max(0,now-i.lastTs)/DECAY_HALF);
 const freqScore=Math.log1p(i.count);
 const durScore=Math.log1p(i.totalDur/1000);
 return parseFloat((freqScore*durScore*recencyFactor).toFixed(4));
}
function computeRanks(){
 const now=Date.now();
 const scored=panels.map(p=>({id:p.id,score:computeScore(p.id)}));
 scored.sort((a,b)=>b.score-a.score);
 const maxScore=scored[0]?.score||0;
 const rankMap=new Map();
 scored.forEach((s,i)=>{
  const tier=i===0?'rank-1':i<=2?'rank-2':i<=4?'rank-3':i<=5?'rank-4':'compact';
  const shouldCompact=!pinned.has(s.id)&&!manualPos[s.id]
   &&(s.score<maxScore*COMPACT_THRESHOLD||i>=Math.ceil(panels.length*0.65));
  rankMap.set(s.id,{score:s.score,rank:i+1,tier,compact:shouldCompact});
 });
 return rankMap;
}
function gridAreaForRank(rank,total){
 const pos=rank-1;
 if(total<=4){
  if(pos===0)return'1/1/3/3';
  if(pos===1)return'1/3/2/5';
  if(pos===2)return'2/3/3/5';
  return'3/3/4/5';
 }
 if(pos===0)return'1/1/3/3';
 if(pos===1)return'1/3/2/5';
 if(pos<=3)return pos===2?'2/3/3/4':pos===3?'2/4/3/5';
 if(pos<=5)return pos===4?'3/3/4/4':'3/4/4/5';
 return `${4+Math.floor((pos-6)/4)}/${((pos-6)%4)+1}/span 1`;
}
function findDiff(oldRanks,newRanks){
 const changes=[];
 newRanks.forEach((nr,id)=>{
  const or=oldRanks.get(id);
  if(!or||or.tier!==nr.tier||or.compact!==nr.compact||or.rank!==nr.rank)
   changes.push({id,old:or,new:nr});
 });
 oldRanks.forEach((_,id)=>{
  if(!newRanks.has(id))changes.push({id,old:oldRanks.get(id),new:null});
 });
 return changes;
}
function applyDiff(changes,rankMap){
 const grid=document.getElementById('grid');
 changes.forEach(({id,new:nr})=>{
  const el=document.getElementById('panel-'+id);
  if(!el)return;
  if(!nr)return;
  const rank=nr.rank;
  const total=panels.length;
  let gridCol,gridRow;
  if(manualPos[id]){
   gridCol=manualPos[id].col;
   gridRow=manualPos[id].row;
  }else if(pinned.has(id)){
   const cur=el.style.gridColumn||el.style.gridRow;
   gridCol=el.style.gridColumn||'auto';
   gridRow=el.style.gridRow||'auto';
  }else{
   if(rank===1){gridCol='span 2';gridRow='span 2'}
   else if(rank<=3){gridCol='span 1';gridRow='span 1'}
   else if(rank<=5){gridCol='span 1';gridRow='span 1'}
   else{gridCol='span 1';gridRow='span 1'}
  }
  el.style.gridColumn=gridCol;
  el.style.gridRow=gridRow;
  el.className=el.className.replace(/rank-\d|compact/g,'').replace(/\s+/g,' ').trim();
  el.classList.add(nr.tier);
  if(nr.compact)el.classList.add('compact');else el.classList.remove('compact');
  const rankDot=el.querySelector('.rank-dot');
  if(rankDot){
   rankDot.className='rank-dot '+(rank===1?'r1':rank<=3?'r2':rank<=4?'r3':rank<=5?'r4':'rl');
  }
  const badge=el.querySelector('.score-badge');
  if(badge){badge.textContent='s:'+nr.score.toFixed(1);badge.title='rank #'+rank}
  updateSpark(el,id);
 });
 const order=[...rankMap.entries()].sort((a,b)=>a[1].rank-b[1].rank).map(([id])=>id);
 order.forEach((id,idx)=>{
  const el=document.getElementById('panel-'+id);
  if(el&&!pinned.has(id)&&!manualPos[id])el.style.order=idx;
 });
}
function updateSpark(el,panelId){
 const p=panels.find(x=>x.id===panelId);
 if(!p)return;
 const bars=el.querySelectorAll('.spark-bar');
 if(!bars.length)return;
 const hist=p.history;
 const max=Math.max(...hist,1);
 bars.forEach((bar,i)=>{
  const h=Math.max(3,(hist[i]||0)/max*38);
  if(bar.style.height!==h+'px')bar.style.height=h+'px';
 });
}
function applyLayout(){
 const newRanks=computeRanks();
 const oldRanks=ranks.length?ranks:new Map();
 const changes=findDiff(oldRanks,newRanks);
 if(changes.length>0)applyDiff(changes,newRanks);
 ranks=newRanks;
 document.getElementById('trackBadge').textContent='Tracking: '+panels.length+' panels';
 document.getElementById('updateBadge').textContent=new Date().toLocaleTimeString();
 saveState();
}
function buildPanel(p){
 const intr=interactions[p.id];
 const score=computeScore(p.id);
 const rankInfo=ranks.get(p.id)||{score,tier:'',rank:999,compact:false};
 const compact=rankInfo.compact;
 const isPinned=pinned.has(p.id);
 const hist=p.history;
 const maxH=Math.max(...hist,1);
 return`<div class="panel${compact?' compact':''} ${rankInfo.tier}${isPinned?' pinned':''}" id="panel-${p.id}" data-id="${p.id}">
  <div class=panel-header>
   <div class=panel-title><span class=icon>${p.icon}</span>${p.title}<span class="rank-dot ${rankInfo.rank===1?'r1':rankInfo.rank<=3?'r2':rankInfo.rank<=4?'r3':rankInfo.rank<=5?'r4':'rl'}"></span></div>
   <div class=panel-actions>
    <span class=score-badge title="rank #${rankInfo.rank}">s:${score.toFixed(1)}</span>
    ${compact?`<button class=expand-btn onclick="expandPanel('${p.id}')" title=Expand>↕</button>`:''}
    <button class="${isPinned?'pinned-btn':''}" onclick="togglePin('${p.id}')" title="${isPinned?'Unpin':'Pin'}">${isPinned?'📌':'📍'}</button>
    <button onclick="movePanel('${p.id}','up')" title="Move up">▲</button>
    <button onclick="movePanel('${p.id}','down')" title="Move down">▼</button>
    <button onclick="movePanel('${p.id}','left')" title="Move left">◀</button>
    <button onclick="movePanel('${p.id}','right')" title="Move right">▶</button>
   </div>
  </div>
  <div class=body>
   <div class=metric-value>${p.val}${p.unit?'<small style=font-size:0.5em>'+p.unit+'</small>':''}</div>
   <div class=metric-label>current</div>
   <div class=spark>${hist.map(v=>`<div class=spark-bar style=height:${Math.max(3,v/maxH*38)}px></div>`).join('')}</div>
  </div>
  ${compact?`<span class=compact-metric>${p.val}${p.unit}</span><div class=compact-spark>${hist.slice(-6).map(v=>`<div class=spark-bar style=height:${Math.max(2,v/maxH*14)}px></div>`).join('')}</div>`:''}
 </div>`;
}
function renderAll(){
 document.getElementById('grid').innerHTML=panels.map(p=>buildPanel(p)).join('');
 initObservers();
}
function initObservers(){
 const obs=new IntersectionObserver((entries)=>{
  const now=Date.now();
  entries.forEach(e=>{
   const id=e.target.dataset.id;
   if(!id)return;
   if(e.isIntersecting){
    if(!viewTimers[id])viewTimers[id]=now;
   }else{
    if(viewTimers[id]){
     const dur=now-viewTimers[id];
     interactions[id].totalDur=(interactions[id].totalDur||0)+dur;
     interactions[id].lastTs=now;
     viewTimers[id]=null;
    }
   }
  });
 },{threshold:0.3});
 document.querySelectorAll('.panel').forEach(el=>{
  obs.observe(el);
  el.addEventListener('click',()=>{
   const id=el.dataset.id;
   if(!id)return;
   interactions[id].count=(interactions[id].count||0)+1;
   interactions[id].lastTs=Date.now();
  });
 });
}
window.expandPanel=function(id){
 compactState[id]=false;
 pinned.add(id);
 applyLayout();
};
window.togglePin=function(id){
 if(pinned.has(id))pinned.delete(id);else pinned.add(id);
 applyLayout();
};
window.movePanel=function(id,dir){
 if(!manualPos[id])manualPos[id]={col:1,row:1};
 if(dir==='up')manualPos[id].row=Math.max(1,manualPos[id].row-1);
 if(dir==='down')manualPos[id].row=manualPos[id].row+1;
 if(dir==='left')manualPos[id].col=Math.max(1,manualPos[id].col-1);
 if(dir==='right')manualPos[id].col=manualPos[id].col+1;
 pinned.add(id);
 applyLayout();
};
document.getElementById('btnReset').addEventListener('click',()=>{
 interactions={};pinned.clear();manualPos={};compactState={};
 panels.forEach(p=>{interactions[p.id]={count:0,totalDur:0,lastTs:0,viewStart:null}});
 localStorage.removeItem(LS_KEY);
 ranks=new Map();
 renderAll();
 applyLayout();
});
document.getElementById('btnLockAll').addEventListener('click',()=>{
 panels.forEach(p=>pinned.add(p.id));
 applyLayout();
});
document.getElementById('btnUnlockAll').addEventListener('click',()=>{
 pinned.clear();
 applyLayout();
});
let rankInterval;
function start(){
 loadState();
 initPanels();
 renderAll();
 applyLayout();
 rankInterval=setInterval(()=>{
  panels.forEach(p=>{
   p.val=Math.round((p.val+(Math.random()-0.5)*p.val*0.1)*10)/10;
   p.history.push(Math.round(p.val));
   if(p.history.length>14)p.history.shift();
  });
  applyLayout();
 },RANK_TICK);
}
start();
})();
</script></body></html>