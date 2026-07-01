<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:#1e293b;border-bottom:1px solid #334155}
header h1{font-size:1.25rem;font-weight:600}
.toolbar{display:flex;gap:8px}
.toolbar button{padding:6px 14px;border:1px solid #475569;border-radius:6px;background:#1e293b;color:#e2e8f0;cursor:pointer;font-size:0.8rem;transition:background .15s}
.toolbar button:hover{background:#334155}
.toolbar button.on{background:#3b82f6;border-color:#3b82f6;color:#fff}
.dashboard{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;padding:16px;max-width:1600px;margin:0 auto;grid-auto-rows:160px}
.panel{border-radius:10px;background:#1e293b;border:1px solid #334155;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,border-color .2s,transform .15s;cursor:grab}
.panel:hover{box-shadow:0 4px 20px rgba(0,0,0,.3);border-color:#475569}
.panel.dragging{opacity:.7;cursor:grabbing;box-shadow:0 8px 30px rgba(0,0,0,.5);z-index:10;transform:scale(1.02)}
.panel.pinned{border-color:#3b82f6}
.panel.compact{grid-column:span 1;grid-row:span 1}
.panel.expanded{grid-column:span 2;grid-row:span 2}
.panel-head{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid #334155;background:#1e293b;flex-shrink:0;user-select:none}
.panel-head .title{font-weight:600;font-size:0.8rem;color:#94a3b8;display:flex;align-items:center;gap:6px}
.panel-head .title .dot{width:8px;height:8px;border-radius:50%}
.panel-actions{display:flex;gap:4px}
.panel-actions button{width:26px;height:26px;border:none;border-radius:4px;background:transparent;color:#64748b;cursor:pointer;font-size:0.7rem;display:flex;align-items:center;justify-content:center;transition:color .15s,background .15s}
.panel-actions button:hover{color:#e2e8f0;background:#334155}
.panel-actions .lock-btn.locked{color:#3b82f6}
.panel-body{flex:1;padding:10px 12px;overflow:hidden;display:flex;align-items:center;justify-content:center;min-height:0}
.panel-body .big-num{font-size:2.2rem;font-weight:700;line-height:1}
.panel-body .metric-label{font-size:0.72rem;color:#64748b;margin-top:4px}
.panel-body canvas{max-width:100%;max-height:100%}
.panel.compact .panel-body .big-num{font-size:1.2rem}
.panel.compact .panel-body{flex-direction:row;gap:12px;align-items:center}
.panel-body .spark-row{display:flex;align-items:flex-end;gap:2px;height:40px}
.panel-body .spark-row .bar{width:6px;border-radius:2px 2px 0 0;background:#3b82f6;transition:height .3s}
.panel.compact .panel-body .spark-row .bar{width:4px}
.drop-target{border:2px dashed #3b82f6!important;border-radius:10px!important;background:rgba(59,130,246,.1)!important}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="toolbar">
    <button id="btn-reset" title="Reset all tracking data">Reset</button>
    <button id="btn-auto" class="on" title="Auto-layout enabled">Auto</button>
    <button id="btn-compact-all" title="Compact unused panels">Compact</button>
  </div>
</header>
<div class="dashboard" id="grid"></div>
<script>
(function(){
const PANELS=[
  {id:'cpu',title:'CPU',color:'#3b82f6',unit:'%',v:42,history:[38,45,42,39,43,41,44,40,42,38]},
  {id:'mem',title:'Memory',color:'#22c55e',unit:'GB',v:12.4,history:[10,11,12,13,12,11,10,12,13,12]},
  {id:'disk',title:'Disk IO',color:'#f59e0b',unit:'MB/s',v:87,history:[80,90,85,88,92,86,84,82,91,87]},
  {id:'net',title:'Network',color:'#ec4899',unit:'Mbps',v:340,history:[300,320,310,330,350,340,360,335,345,340]},
  {id:'req',title:'Requests',color:'#8b5cf6',unit:'/s',v:1250,history:[1100,1200,1150,1300,1250,1280,1220,1180,1240,1250]},
  {id:'err',title:'Errors',color:'#ef4444',unit:'count',v:3,history:[5,2,1,4,3,2,0,1,3,3]},
  {id:'lat',title:'Latency',color:'#06b6d4',unit:'ms',v:24,history:[30,28,25,22,26,24,20,23,27,24]},
  {id:'cache',title:'Cache Hit',color:'#84cc16',unit:'%',v:94,history:[90,92,93,91,95,94,96,92,93,94]}
];
const STORAGE_KEY='ad_dash_v1';
const DECAY_HALF_HOURS=4;
const COMPACT_SCORE_PCT=25;
const MAX_COMPACT=3;
function loadState(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    return raw?JSON.parse(raw):{};
  }catch(e){return{};}
}
function saveState(s){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(s));}catch(e){}}
let state=loadState();
let now=()=>Date.now();
let autoLayout=true;
let gridEl=document.getElementById('grid');
let panelOrder=PANELS.map(p=>p.id);
let dragElId=null;
let panelEls={};
let viewTimers={};
function ensurePanelState(id){
  if(!state[id])state[id]={dur:0,clicks:0,last:0,locked:false,pos:null,compact:false};
}
PANELS.forEach(p=>ensurePanelState(p.id));
function score(id){
  let s=state[id]||{};
  let hours=(now()-s.last)/3600000;
  let recency=1/(1+hours/DECAY_HALF_HOURS);
  let freq=s.clicks||1;
  let dur=(s.dur||1000)/1000;
  return freq*dur*recency;
}
function rankPanels(){
  let scored=PANELS.map(p=>({id:p.id,s:score(p.id)}));
  scored.sort((a,b)=>b.s-a.s);
  return scored;
}
function compactThreshold(ranked){
  let max=ranked[0]?.s||1;
  return max*(COMPACT_SCORE_PCT/100);
}
function arrangeLayout(){
  if(!autoLayout)return;
  let ranked=rankPanels();
  let thresh=compactThreshold(ranked);
  let compactCount=0;
  ranked.forEach((r,i)=>{
    let st=state[r.id]||{};
    if(st.locked)return;
    st.compact=(i>=PANELS.length-MAX_COMPACT)&&(r.s<thresh||compactCount<MAX_COMPACT);
    if(st.compact)compactCount++;
    st.pos=st.compact?null:null;
  });
  renderAll();
}
function renderAll(){
  let ranked=rankPanels();
  let order=ranked.map(r=>r.id);
  panelOrder=order;
  let lockedPositions={};
  PANELS.forEach(p=>{
    let st=state[p.id]||{};
    if(st.locked&&st.pos!=null)lockedPositions[p.id]=st.pos;
  });
  let html='';
  order.forEach(id=>{
    let p=PANELS.find(px=>px.id===id);
    let st=state[id]||{};
    let cls=['panel'];
    cls.push(st.compact?'compact':'expanded');
    if(st.locked)cls.push('pinned');
    html+=panelHTML(p,st,cls.join(' '));
  });
  gridEl.innerHTML=html;
  // Symmetric lock button state
  order.forEach(id=>{
    let st=state[id]||{};
    let btn=document.getElementById('lock-'+id);
    if(btn){
      btn.textContent=st.locked?'🔒':'🔓';
      btn.className='lock-btn'+(st.locked?' locked':'');
      btn.title=st.locked?'Unlock panel':'Lock panel position';
    }
    let compactBtn=document.getElementById('compact-'+id);
    if(compactBtn){
      compactBtn.textContent=st.compact?'⤢':'⊟';
      compactBtn.title=st.compact?'Expand panel':'Compact panel';
    }
  });
  // Store refs for drag
  order.forEach(id=>{
    panelEls[id]=document.getElementById('panel-'+id);
  });
  attachDragEvents();
  startViewTracking();
}
function panelHTML(p,st,cls){
  let histBars='';
  let h=p.history||[];
  let mx=Math.max(...h,1);
  for(let i=0;i<h.length;i++){
    let hh=Math.max(4,Math.round((h[i]/mx)*32));
    histBars+='<div class="bar" style="height:'+hh+'px"></div>';
  }
  let colorDot='<span class="dot" style="background:'+p.color+'"></span>';
  let titleRow='<div class="title">'+colorDot+p.title+'</div>';
  let actions='<div class="panel-actions">'+
    '<button id="compact-'+p.id+'" class="compact-btn" onclick="window._dash.toggleCompact(\''+p.id+'\')">'+(st.compact?'⤢':'⊟')+'</button>'+
    '<button id="lock-'+p.id+'" class="lock-btn'+(st.locked?' locked':'')+'" onclick="window._dash.toggleLock(\''+p.id+'\')">'+(st.locked?'🔒':'🔓')+'</button>'+
    '</div>';
  let head='<div class="panel-head">'+titleRow+actions+'</div>';
  let body='<div class="panel-body">'+
    '<div style="text-align:center">'+
    '<div class="big-num" style="color:'+p.color+'">'+p.v+'</div>'+
    '<div class="metric-label">'+p.unit+'</div>'+
    '<div class="spark-row" style="margin-top:6px;justify-content:center">'+histBars+'</div>'+
    '</div>'+
    '</div>';
  return '<div class="'+cls+'" id="panel-'+p.id+'" data-id="'+p.id+'" draggable="true">'+head+body+'</div>';
}
function attachDragEvents(){
  Object.values(panelEls).forEach(el=>{
    if(!el)return;
    el.ondragstart=function(e){
      dragElId=e.target.closest('.panel')?.dataset.id;
      if(dragElId && state[dragElId]?.locked)return e.preventDefault();
      e.target.closest('.panel')?.classList.add('dragging');
      e.dataTransfer.effectAllowed='move';
      e.dataTransfer.setData('text/plain',dragElId);
    };
    el.ondragend=function(e){
      e.target.closest('.panel')?.classList.remove('dragging');
      dragElId=null;
    };
    el.ondragover=function(e){
      e.preventDefault();
      e.dataTransfer.dropEffect='move';
    };
    el.ondrop=function(e){
      e.preventDefault();
      let targetEl=e.target.closest('.panel');
      let targetId=targetEl?.dataset.id;
      let srcId=e.dataTransfer.getData('text/plain');
      if(!srcId||!targetId||srcId===targetId)return;
      if(state[srcId]?.locked||state[targetId]?.locked)return;
      let srcIdx=panelOrder.indexOf(srcId);
      let tgtIdx=panelOrder.indexOf(targetId);
      if(srcIdx<0||tgtIdx<0)return;
      panelOrder.splice(srcIdx,1);
      panelOrder.splice(tgtIdx,0,srcId);
      renderAll();
    };
  });
}
function startViewTracking(){
  // Stop old timers
  Object.keys(viewTimers).forEach(id=>{
    clearInterval(viewTimers[id]);
    delete viewTimers[id];
  });
  // Track visible panels
  let observer=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      let id=e.target.dataset.id;
      if(!id)return;
      if(e.isIntersecting){
        viewTimers[id]=setInterval(()=>{
          state[id].dur=(state[id].dur||0)+500;
          saveState(state);
        },500);
      }else{
        clearInterval(viewTimers[id]);
        delete viewTimers[id];
      }
    });
  },{threshold:0.3});
  Object.values(panelEls).forEach(el=>{if(el)observer.observe(el);});
}
// Public API bound to window for onclick handlers
let api={
  toggleLock(id){
    ensurePanelState(id);
    state[id].locked=!state[id].locked;
    if(state[id].locked){
      autoLayout=false;
      document.getElementById('btn-auto').className='';
    }
    saveState(state);
    renderAll();
  },
  toggleCompact(id){
    ensurePanelState(id);
    state[id].compact=!state[id].compact;
    state[id].clicks=(state[id].clicks||0)+1;
    state[id].last=now();
    saveState(state);
    renderAll();
  },
  reset(){
    localStorage.removeItem(STORAGE_KEY);
    state={};
    PANELS.forEach(p=>ensurePanelState(p.id));
    autoLayout=true;
    document.getElementById('btn-auto').className='on';
    renderAll();
  },
  toggleAuto(){
    autoLayout=!autoLayout;
    document.getElementById('btn-auto').className=autoLayout?'on':'';
    if(autoLayout)arrangeLayout();
  },
  compactAll(){
    let ranked=rankPanels();
    let thresh=compactThreshold(ranked);
    let cc=0;
    ranked.forEach((r,i)=>{
      let st=state[r.id]||{};
      if(st.locked)return;
      st.compact=(i>=PANELS.length-MAX_COMPACT)&&(r.s<thresh||cc<MAX_COMPACT);
      if(st.compact)cc++;
    });
    saveState(state);
    renderAll();
  }
};
window._dash=api;
// Button bindings
document.getElementById('btn-reset').onclick=api.reset;
document.getElementById('btn-auto').onclick=api.toggleAuto;
document.getElementById('btn-compact-all').onclick=api.compactAll;
// Click tracking on panels
gridEl.addEventListener('click',function(e){
  let panelEl=e.target.closest('.panel');
  if(!panelEl)return;
  let id=panelEl.dataset.id;
  if(!id)return;
  // Ignore clicks on action buttons
  if(e.target.closest('button'))return;
  ensurePanelState(id);
  state[id].clicks=(state[id].clicks||0)+1;
  state[id].last=now();
  saveState(state);
});
// Initial render with stored state
renderAll();
if(autoLayout)arrangeLayout();
// Periodic live data refresh (stretch goal)
setInterval(()=>{
  PANELS.forEach(p=>{
    let delta=(Math.random()-0.5)*p.v*0.1;
    p.v=Math.round((p.v+delta)*10)/10;
    p.history.push(p.v);
    if(p.history.length>15)p.history.shift();
  });
  renderAll();
},5000);
})();
</script>
</body>
</html>