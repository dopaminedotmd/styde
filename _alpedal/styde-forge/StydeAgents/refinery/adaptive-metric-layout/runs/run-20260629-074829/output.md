<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222632;--border:#2a2e3a;
  --text:#d4d6dd;--text2:#8b8f9e;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--compact-ratio:0.4;
  --gap:12px;--radius:8px;--header-h:44px;--transition:200ms ease;
}
body{background:var(--bg);color:var(--text);font-family:'Inter',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}
.dashboard{max-width:1600px;margin:0 auto;padding:16px}
.dash-header{display:flex;align-items:center;justify-content:space-between;height:var(--header-h);margin-bottom:16px}
.dash-header h1{font-size:18px;font-weight:600;color:var(--text)}
.dash-controls{display:flex;gap:8px;align-items:center}
.dash-btn{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:background var(--transition)}
.dash-btn:hover{background:var(--border)}
.dash-btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.dash-btn.danger{color:var(--danger)}
.layout-badge{font-size:11px;padding:3px 8px;border-radius:10px;background:var(--surface2);color:var(--text2)}
.layout-badge.auto{color:var(--accent2)}
.layout-badge.manual{color:var(--warn)}
.grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(160px,auto);gap:var(--gap);transition:grid-template-columns var(--transition)}
.grid.cols-3{grid-template-columns:repeat(3,1fr)}
.grid.cols-2{grid-template-columns:repeat(2,1fr)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);display:flex;flex-direction:column;overflow:hidden;transition:all var(--transition);position:relative;min-height:120px}
.panel:hover{border-color:#3a3f50}
.panel.compact{min-height:80px}
.panel.compact .panel-body{max-height:60px;overflow:hidden;opacity:0.7}
.panel.compact .panel-chart{height:40px}
.panel.collapsed{min-height:44px}
.panel.collapsed .panel-body{display:none}
.panel.collapsed .panel-chart{display:none}
.panel.locked{border-left:3px solid var(--warn)}
.panel.dragging{opacity:0.5;z-index:100;border-color:var(--accent);box-shadow:0 8px 32px rgba(0,0,0,0.5)}
.panel.drag-over{border-color:var(--accent);border-style:dashed}
.panel.high-rank{border-color:var(--accent2);border-width:1.5px}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--surface2);border-bottom:1px solid var(--border);cursor:grab;user-select:none;min-height:36px}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:13px;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-title .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.panel-actions{display:flex;gap:2px;flex-shrink:0}
.panel-actions button{background:none;border:none;color:var(--text2);cursor:pointer;padding:4px;border-radius:4px;font-size:12px;line-height:1;width:26px;height:26px;display:flex;align-items:center;justify-content:center;transition:all var(--transition)}
.panel-actions button:hover{background:var(--border);color:var(--text)}
.panel-actions button.lock-btn.locked{color:var(--warn)}
.panel-actions button.compact-btn.compact-active{color:var(--accent2)}
.panel-body{padding:10px 12px;flex:1;display:flex;flex-direction:column;gap:8px;overflow:hidden}
.panel-value{font-size:28px;font-weight:700;line-height:1.1}
.panel-label{font-size:11px;color:var(--text2)}
.panel-chart{flex:1;min-height:50px;position:relative}
.panel-chart canvas{width:100%;height:100%}
.panel-stats{display:flex;gap:12px;font-size:11px;color:var(--text2)}
.panel-stats span{display:flex;align-items:center;gap:4px}
.rank-indicator{position:absolute;top:4px;right:8px;font-size:9px;color:var(--text2);opacity:0.5}
.resize-handle{position:absolute;right:0;bottom:0;width:14px;height:14px;cursor:nwse-resize;background:linear-gradient(135deg,transparent 50%,var(--border) 50%);border-radius:0 0 var(--radius) 0;opacity:0;transition:opacity var(--transition)}
.panel:hover .resize-handle{opacity:1}
.collapsed-section{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;padding:8px 12px;background:var(--surface);border:1px dashed var(--border);border-radius:var(--radius);align-items:center}
.collapsed-section .section-label{font-size:11px;color:var(--text2);margin-right:8px}
.collapsed-chip{background:var(--surface2);border:1px solid var(--border);padding:4px 10px;border-radius:12px;font-size:11px;cursor:pointer;transition:all var(--transition);display:flex;align-items:center;gap:4px}
.collapsed-chip:hover{background:var(--border)}
.collapsed-chip.expand-btn{color:var(--accent)}
.heatmap-overlay{position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:999;opacity:0.15;transition:opacity 500ms}
.heatmap-overlay.active{opacity:0.25}
.toast{position:fixed;bottom:20px;right:20px;background:var(--surface2);border:1px solid var(--border);padding:8px 16px;border-radius:var(--radius);font-size:12px;z-index:1000;animation:toast-in 200ms ease}
@keyframes toast-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:1200px){.grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:768px){.grid{grid-template-columns:repeat(2,1fr)}.dashboard{padding:8px}}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="dashboard" id="dashboard">
  <div class="dash-header">
    <h1>Adaptive Layout Dashboard</h1>
    <div class="dash-controls">
      <span class="layout-badge auto" id="layoutModeBadge">auto</span>
      <button class="dash-btn" id="btnHeatmap" aria-label="Toggle heatmap overlay">Heatmap</button>
      <button class="dash-btn" id="btnAutoLayout" aria-label="Toggle auto layout">Auto-Layout: On</button>
      <button class="dash-btn" id="btnReset" aria-label="Reset layout">Reset</button>
      <button class="dash-btn" id="btnCols3" aria-label="3 columns">3col</button>
      <button class="dash-btn" id="btnCols4" aria-label="4 columns">4col</button>
    </div>
  </div>
  <div class="grid cols-4" id="grid" role="region" aria-label="Dashboard panels"></div>
  <div id="collapsedSection" style="display:none"></div>
</div>
<canvas class="heatmap-overlay" id="heatmapCanvas" style="display:none"></canvas>
<script>
(function(){
'use strict';
const LS_KEY = 'adaptive_dashboard_v1';
const SAVE_DEBOUNCE = 2000;
const TRACK_INTERVAL = 1000;
const RANK_INTERVAL = 15000;
const DATA_TICK = 3000;
const RECENCY_HALFLIFE_HOURS = 4;
const COMPACT_THRESHOLD = 0.15;
const COLLAPSE_THRESHOLD = 0.05;
const EXPAND_THRESHOLD = 0.25;
const COLOR_PALETTE = ['#6c8cff','#4ade80','#f59e0b','#ef4444','#a78bfa','#f472b6','#2dd4bf','#fb923c'];
const DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',unit:'%',color:0,maxVal:100,noise:0.3,trend:0},
  {id:'memory',title:'Memory',unit:'%',color:1,maxVal:100,noise:0.2,trend:0.05},
  {id:'network',title:'Network I/O',unit:'MB/s',color:2,maxVal:500,noise:0.4,trend:0},
  {id:'disk',title:'Disk IOPS',unit:'iops',color:3,maxVal:2000,noise:0.35,trend:0},
  {id:'users',title:'Active Users',unit:'',color:4,maxVal:5000,noise:0.15,trend:0.02},
  {id:'requests',title:'Request Rate',unit:'req/s',color:5,maxVal:200,noise:0.25,trend:0},
  {id:'errors',title:'Error Rate',unit:'%',color:6,maxVal:10,noise:0.5,trend:-0.01},
  {id:'latency',title:'P99 Latency',unit:'ms',color:7,maxVal:500,noise:0.2,trend:0.01}
];
let state = {
  panels: {},
  panelOrder: [],
  collapsedIds: [],
  columns: 4,
  autoLayout: true,
  gridVersion: 0
};
let trackingTimers = {};
let saveTimer = null;
let rankTimer = null;
let dataTimer = null;
let intersectionObserver = null;
let heatmapActive = false;
let heatmapCanvas = null;
let heatmapCtx = null;
let heatmapPoints = [];
function $(sel,ctx){return(ctx||document).querySelector(sel)}
function $$(sel,ctx){return Array.from((ctx||document).querySelectorAll(sel))}
function now(){return Date.now()}
function clamp(v,min,max){return Math.max(min,Math.min(max,v))}
function debounce(fn,ms){
  let t;
  return function(...args){
    clearTimeout(t);
    t=setTimeout(()=>fn.apply(this,args),ms);
  };
}
function sparkData(panelDef){
  let vals=[];
  let v=panelDef.maxVal*(0.3+Math.random()*0.4);
  for(let i=0;i<60;i++){
    v+=panelDef.noise*(Math.random()-0.5)*panelDef.maxVal;
    v+=panelDef.trend*panelDef.maxVal/60;
    v=clamp(v,0,panelDef.maxVal);
    vals.push(v);
  }
  return vals;
}
function currentValue(panelDef){
  let p=state.panels[panelDef.id];
  if(!p._sparkData) p._sparkData=sparkData(panelDef);
  let v=p._sparkData[p._sparkData.length-1];
  v+=panelDef.noise*(Math.random()-0.5)*panelDef.maxVal*0.1;
  v+=panelDef.trend*panelDef.maxVal/60;
  v=clamp(v,0,panelDef.maxVal);
  p._sparkData.push(v);
  if(p._sparkData.length>120) p._sparkData.shift();
  return v;
}
function initPanelState(def){
  return {
    id:def.id,
    title:def.title,
    unit:def.unit,
    maxVal:def.maxVal,
    color:def.color,
    value:0,
    _sparkData:sparkData(def),
    compact:false,
    collapsed:false,
    locked:false,
    manualPos:-1,
    spanCol:1,
    spanRow:1,
    viewCount:0,
    viewDuration:0,
    viewStart:null,
    interactionCount:0,
    lastViewed:0,
    lastInteraction:0,
    rank:0,
    rankScore:0
  };
}
function loadState(){
  try{
    let raw=localStorage.getItem(LS_KEY);
    if(raw){
      let saved=JSON.parse(raw);
      let merged={};
      DEFAULT_PANELS.forEach(def=>{
        let sp=initPanelState(def);
        if(saved.panels && saved.panels[def.id]){
          let sv=saved.panels[def.id];
          sp.compact=!!sv.compact;
          sp.collapsed=!!sv.collapsed;
          sp.locked=!!sv.locked;
          sp.manualPos=sv.manualPos!=null?sv.manualPos:-1;
          sp.spanCol=sv.spanCol||1;
          sp.spanRow=sv.spanRow||1;
          sp.viewCount=sv.viewCount||0;
          sp.viewDuration=sv.viewDuration||0;
          sp.interactionCount=sv.interactionCount||0;
          sp.lastViewed=sv.lastViewed||0;
          sp.lastInteraction=sv.lastInteraction||0;
          sp.rank=sv.rank||0;
          sp.rankScore=sv.rankScore||0;
        }
        merged[def.id]=sp;
      });
      state.panels=merged;
      state.panelOrder=saved.panelOrder||DEFAULT_PANELS.map(d=>d.id);
      state.collapsedIds=saved.collapsedIds||[];
      state.columns=saved.columns||4;
      state.autoLayout=saved.autoLayout!==false;
    }else{
      state.panels={};
      state.panelOrder=DEFAULT_PANELS.map(d=>d.id);
      DEFAULT_PANELS.forEach(def=>{state.panels[def.id]=initPanelState(def)});
    }
  }catch(e){
    state.panels={};
    state.panelOrder=DEFAULT_PANELS.map(d=>d.id);
    DEFAULT_PANELS.forEach(def=>{state.panels[def.id]=initPanelState(def)});
  }
}
function persistState(){
  let toSave={
    panels:{},
    panelOrder:state.panelOrder,
    collapsedIds:state.collapsedIds,
    columns:state.columns,
    autoLayout:state.autoLayout
  };
  Object.values(state.panels).forEach(p=>{
    toSave.panels[p.id]={
      compact:p.compact,
      collapsed:p.collapsed,
      locked:p.locked,
      manualPos:p.manualPos,
      spanCol:p.spanCol,
      spanRow:p.spanRow,
      viewCount:p.viewCount,
      viewDuration:p.viewDuration,
      interactionCount:p.interactionCount,
      lastViewed:p.lastViewed,
      lastInteraction:p.lastInteraction,
      rank:p.rank,
      rankScore:p.rankScore
    };
  });
  try{localStorage.setItem(LS_KEY,JSON.stringify(toSave))}catch(e){}
}
const schedulePersist = debounce(persistState,SAVE_DEBOUNCE);
function computeRanks(){
  let nowMs=now();
  let panels=Object.values(state.panels);
  panels.forEach(p=>{
    if(p.viewCount===0){p.rankScore=0;return}
    let hoursSinceView=p.lastViewed?(nowMs-p.lastViewed)/(3600000):RECENCY_HALFLIFE_HOURS*2;
    let recency=1/(1+hoursSinceView/RECENCY_HALFLIFE_HOURS);
    p.rankScore=p.viewCount*p.viewDuration*recency+p.interactionCount*0.5;
  });
  panels.sort((a,b)=>b.rankScore-a.rankScore);
  panels.forEach((p,i)=>{p.rank=i+1});
}
function computeLayout(){
  if(!state.autoLayout) return;
  let locked=[];
  let unlocked=[];
  state.panelOrder.forEach(id=>{
    let p=state.panels[id];
    if(!p) return;
    if(p.collapsed){
    }else if(p.locked){
      locked.push(p);
    }else{
      unlocked.push(p);
    }
  });
  unlocked.sort((a,b)=>b.rankScore-a.rankScore);
  let highCutoff=Math.max(1,Math.floor(unlocked.length*0.3));
  let compactCutoff=Math.max(highCutoff,Math.floor(unlocked.length*0.7));
  unlocked.forEach((p,i)=>{
    if(i<highCutoff){
      p.compact=false;
      p.spanCol=2;
      p.spanRow=2;
    }else if(i<compactCutoff){
      p.compact=false;
      p.spanCol=1;
      p.spanRow=1;
    }else{
      p.compact=true;
      p.spanCol=1;
      p.spanRow=1;
    }
  });
  let ordered=[];
  unlocked.forEach(p=>ordered.push(p.id));
  locked.forEach(p=>{
    if(p.manualPos>=0&&p.manualPos<ordered.length){
      ordered.splice(p.manualPos,0,p.id);
    }else{
      ordered.push(p.id);
    }
  });
  let collapsedSet=new Set(state.collapsedIds);
  let oldOrder=state.panelOrder.slice();
  state.panelOrder=ordered;
  state.collapsedIds=[];
  Object.values(state.panels).forEach(p=>{
    if(p.collapsed) state.collapsedIds.push(p.id);
  });
  state.gridVersion++;
  let changed=oldOrder.length!==ordered.length||oldOrder.some((id,i)=>id!==ordered[i]);
  return changed;
}
function renderPanel(p,container){
  let el=document.getElementById('panel-'+p.id);
  let isNew=!el;
  if(isNew){
    el=document.createElement('div');
    el.id='panel-'+p.id;
    el.className='panel';
    el.setAttribute('role','region');
    el.setAttribute('aria-label',p.title+' panel');
    el.setAttribute('draggable','true');
    el.dataset.panelId=p.id;
    el.innerHTML=
      '<div class="panel-header">'+
        '<div class="panel-title"><span class="dot"></span><span class="title-text"></span></div>'+
        '<div class="panel-actions">'+
          '<button class="compact-btn" aria-label="Toggle compact" title="Compact">⊟</button>'+
          '<button class="collapse-btn" aria-label="Collapse" title="Collapse">−</button>'+
          '<button class="lock-btn" aria-label="Lock position" title="Lock">🔓</button>'+
        '</div>'+
      '</div>'+
      '<div class="panel-body">'+
        '<div class="panel-value"></div>'+
        '<div class="panel-label"></div>'+
        '<div class="panel-stats"></div>'+
        '<div class="panel-chart"><canvas></canvas></div>'+
      '</div>'+
      '<div class="resize-handle" aria-label="Resize panel"></div>'+
      '<div class="rank-indicator"></div>';
    container.appendChild(el);
    bindPanelEvents(el,p);
  }
  updatePanelDOM(el,p);
  return el;
}
function updatePanelDOM(el,p){
  let titleText=el.querySelector('.title-text');
  if(titleText&&titleText.textContent!==p.title) titleText.textContent=p.title;
  let dot=el.querySelector('.dot');
  if(dot) dot.style.background=COLOR_PALETTE[p.color]||'#888';
  let valueEl=el.querySelector('.panel-value');
  let valStr=p.unit?p.value.toFixed(1)+' '+p.unit:String(Math.round(p.value));
  if(valueEl&&valueEl.textContent!==valStr) valueEl.textContent=valStr;
  let labelEl=el.querySelector('.panel-label');
  let labelStr='Rank #'+p.rank+' · Score '+p.rankScore.toFixed(1);
  if(labelEl&&labelEl.textContent!==labelStr) labelEl.textContent=labelStr;
  let statsEl=el.querySelector('.panel-stats');
  let statsStr='<span>👁 '+p.viewCount+'</span><span>⏱ '+(p.viewDuration/1000).toFixed(0)+'s</span><span>🖱 '+p.interactionCount+'</span>';
  if(statsEl&&statsEl.innerHTML!==statsStr) statsEl.innerHTML=statsStr;
  el.classList.toggle('compact',p.compact&&!p.collapsed);
  el.classList.toggle('collapsed',p.collapsed);
  el.classList.toggle('locked',p.locked);
  el.classList.toggle('high-rank',p.rank<=3&&!p.collapsed);
  let lockBtn=el.querySelector('.lock-btn');
  if(lockBtn){
    let lockHTML=p.locked?'🔒':'🔓';
    if(lockBtn.innerHTML!==lockHTML) lockBtn.innerHTML=lockHTML;
    lockBtn.classList.toggle('locked',p.locked);
    lockBtn.setAttribute('aria-label',p.locked?'Unlock position':'Lock position');
  }
  let compactBtn=el.querySelector('.compact-btn');
  if(compactBtn){
    compactBtn.classList.toggle('compact-active',p.compact);
    compactBtn.setAttribute('aria-label',p.compact?'Expand panel':'Compact panel');
  }
  let collapseBtn=el.querySelector('.collapse-btn');
  if(collapseBtn){
    collapseBtn.innerHTML=p.collapsed?'+':'−';
    collapseBtn.setAttribute('aria-label',p.collapsed?'Expand panel':'Collapse panel');
  }
  el.style.gridColumn='span '+p.spanCol;
  el.style.gridRow='span '+p.spanRow;
  if(p.manualPos>=0&&p.locked){
    el.style.order=p.manualPos;
  }else{
    el.style.order='';
  }
  let rankInd=el.querySelector('.rank-indicator');
  if(rankInd){
    let rkStr='#'+p.rank;
    if(rankInd.textContent!==rkStr) rankInd.textContent=rkStr;
  }
  if(!p.collapsed){
    let canvas=el.querySelector('canvas');
    if(canvas){
      let rect=canvas.parentElement.getBoundingClientRect();
      let w=Math.floor(rect.width);
      let h=Math.floor(rect.height);
      if(w>0&&h>0&&(canvas.width!==w||canvas.height!==h)){
        canvas.width=w;
        canvas.height=h;
        drawSparkline(canvas,p);
      }else if(w>0&&h>0){
        drawSparkline(canvas,p);
      }
    }
  }
}
function drawSparkline(canvas,p){
  let ctx=canvas.getContext('2d');
  let w=canvas.width,h=canvas.height;
  ctx.clearRect(0,0,w,h);
  if(!p._sparkData||p._sparkData.length<2) return;
  let data=p._sparkData;
  let max=p.maxVal;
  let color=COLOR_PALETTE[p.color]||'#888';
  let pad=4;
  let px=x=>pad+(x/(data.length-1))*(w-2*pad);
  let py=v=>h-pad-(v/max)*(h-2*pad);
  ctx.beginPath();
  ctx.moveTo(px(0),py(data[0]));
  for(let i=1;i<data.length;i++){
    ctx.lineTo(px(i),py(data[i]));
  }
  ctx.strokeStyle=color;
  ctx.lineWidth=1.5;
  ctx.lineJoin='round';
  ctx.stroke();
  let lastX=px(data.length-1);
  let lastY=py(data[data.length-1]);
  ctx.beginPath();
  ctx.arc(lastX,lastY,3,0,Math.PI*2);
  ctx.fillStyle=color;
  ctx.fill();
  let grad=ctx.createLinearGradient(0,pad,0,h-pad);
  grad.addColorStop(0,color+'40');
  grad.addColorStop(1,color+'05');
  ctx.beginPath();
  ctx.moveTo(px(0),h-pad);
  for(let i=0;i<data.length;i++) ctx.lineTo(px(i),py(data[i]));
  ctx.lineTo(px(data.length-1),h-pad);
  ctx.closePath();
  ctx.fillStyle=grad;
  ctx.fill();
}
function bindPanelEvents(el,p){
  let header=el.querySelector('.panel-header');
  let lockBtn=el.querySelector('.lock-btn');
  let compactBtn=el.querySelector('.compact-btn');
  let collapseBtn=el.querySelector('.collapse-btn');
  let resizeHandle=el.querySelector('.resize-handle');
  el.addEventListener('dragstart',e=>{
    if(!state.autoLayout) return;
    el.classList.add('dragging');
    e.dataTransfer.effectAllowed='move';
    e.dataTransfer.setData('text/plain',p.id);
  });
  el.addEventListener('dragend',()=>{el.classList.remove('dragging');$$('.drag-over').forEach(d=>d.classList.remove('drag-over'))});
  el.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='move';el.classList.add('drag-over')});
  el.addEventListener('dragleave',()=>{el.classList.remove('drag-over')});
  el.addEventListener('drop',e=>{
    e.preventDefault();
    el.classList.remove('drag-over');
    let fromId=e.dataTransfer.getData('text/plain');
    if(fromId===p.id) return;
    let fromIdx=state.panelOrder.indexOf(fromId);
    let toIdx=state.panelOrder.indexOf(p.id);
    if(fromIdx<0||toIdx<0) return;
    state.panelOrder.splice(fromIdx,1);
    state.panelOrder.splice(toIdx,0,fromId);
    let fromPanel=state.panels[fromId];
    if(fromPanel){
      fromPanel.locked=true;
      fromPanel.manualPos=toIdx;
    }
    state.autoLayout=false;
    updateLayoutModeUI();
    schedulePersist();
    rebuildGrid();
  });
  el.addEventListener('click',e=>{
    let pid=el.dataset.panelId;
    if(!pid) return;
    let panel=state.panels[pid];
    if(!panel) return;
    panel.interactionCount++;
    panel.lastInteraction=now();
    schedulePersist();
  });
  if(lockBtn){
    lockBtn.addEventListener('click',e=>{
      e.stopPropagation();
      p.locked=!p.locked;
      if(p.locked){
        p.manualPos=state.panelOrder.indexOf(p.id);
        state.autoLayout=false;
        updateLayoutModeUI();
      }else{
        p.manualPos=-1;
      }
      updatePanelDOM(el,p);
      schedulePersist();
      showToast(p.locked?'Locked: '+p.title:'Unlocked: '+p.title);
    });
  }
  if(compactBtn){
    compactBtn.addEventListener('click',e=>{
      e.stopPropagation();
      if(p.collapsed) return;
      p.compact=!p.compact;
      updatePanelDOM(el,p);
      schedulePersist();
    });
  }
  if(collapseBtn){
    collapseBtn.addEventListener('click',e=>{
      e.stopPropagation();
      p.collapsed=!p.collapsed;
      if(p.collapsed){
        p.compact=false;
        state.collapsedIds.push(p.id);
      }else{
        state.collapsedIds=state.collapsedIds.filter(id=>id!==p.id);
      }
      updatePanelDOM(el,p);
      schedulePersist();
      rebuildCollapsedSection();
      showToast(p.collapsed?'Collapsed: '+p.title:'Expanded: '+p.title);
    });
  }
  if(resizeHandle){
    let startX,startY,startW,startH,resizing=false;
    resizeHandle.addEventListener('mousedown',e=>{
      e.preventDefault();
      e.stopPropagation();
      resizing=true;
      startX=e.clientX;
      startY=e.clientY;
      startW=el.offsetWidth;
      startH=el.offsetHeight;
      document.addEventListener('mousemove',onResize);
      document.addEventListener('mouseup',onResizeEnd);
    });
    function onResize(e){
      if(!resizing) return;
      let dw=e.clientX-startX;
      let dh=e.clientY-startY;
      let newW=Math.max(120,startW+dw);
      let newH=Math.max(80,startH+dh);
      let colW=el.parentElement?el.parentElement.offsetWidth/Math.max(1,state.columns):200;
      p.spanCol=Math.max(1,Math.round(newW/colW));
      p.spanRow=Math.max(1,Math.round(newH/140));
      updatePanelDOM(el,p);
    }
    function onResizeEnd(){
      resizing=false;
      document.removeEventListener('mousemove',onResize);
      document.removeEventListener('mouseup',onResizeEnd);
      if(p.spanCol>=2&&p.spanRow>=2) p.compact=false;
      schedulePersist();
    }
  }
}
function rebuildGrid(){
  let grid=$('#grid');
  if(!grid) return;
  let existingEls={};
  $$('.panel',grid).forEach(el=>{
    let pid=el.dataset.panelId;
    if(pid) existingEls[pid]=el;
  });
  let frag=document.createDocumentFragment();
  state.panelOrder.forEach(id=>{
    let p=state.panels[id];
    if(!p) return;
    if(p.collapsed) return;
    let el=existingEls[id];
    if(el){
      if(el.parentElement) el.parentElement.removeChild(el);
      frag.appendChild(el);
      updatePanelDOM(el,p);
    }else{
      el=renderPanel(p,frag);
    }
    delete existingEls[id];
  });
  Object.values(existingEls).forEach(el=>{
    if(el.parentElement) el.parentElement.removeChild(el);
    if(el.dataset.panelId){
      let pid=el.dataset.panelId;
      if(trackingTimers[pid]){
        clearInterval(trackingTimers[pid]);
        delete trackingTimers[pid];
      }
    }
  });
  grid.innerHTML='';
  grid.appendChild(frag);
  rebuildCollapsedSection();
  setupIntersectionObserver();
}
function rebuildCollapsedSection(){
  let section=$('#collapsedSection');
  if(!section) return;
  let collapsedPanels=state.collapsedIds.map(id=>state.panels[id]).filter(Boolean);
  if(collapsedPanels.length===0){
    section.style.display='none';
    section.innerHTML='';
    return;
  }
  section.style.display='flex';
  section.innerHTML='<span class="section-label">Collapsed ('+collapsedPanels.length+')</span>';
  collapsedPanels.forEach(p=>{
    let chip=document.createElement('span');
    chip.className='collapsed-chip expand-btn';
    chip.textContent=p.title;
    chip.setAttribute('role','button');
    chip.setAttribute('tabindex','0');
    chip.addEventListener('click',()=>{
      p.collapsed=false;
      state.collapsedIds=state.collapsedIds.filter(id=>id!==p.id);
      schedulePersist();
      rebuildGrid();
    });
    chip.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ') chip.click()});
    section.appendChild(chip);
  });
}
function setupIntersectionObserver(){
  if(intersectionObserver) intersectionObserver.disconnect();
  intersectionObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      let pid=entry.target.dataset.panelId;
      if(!pid) return;
      let p=state.panels[pid];
      if(!p) return;
      if(entry.isIntersecting&&entry.intersectionRatio>0.5){
        if(!p.viewStart){
          p.viewStart=now();
          startTrackingTimer(pid);
        }
      }else{
        if(p.viewStart){
          p.viewDuration+=now()-p.viewStart;
          p.viewStart=null;
          p.lastViewed=now();
          stopTrackingTimer(pid);
          schedulePersist();
        }
      }
    });
  },{threshold:[0,0.5,1.0]});
  $$('.panel',$('#grid')).forEach(el=>intersectionObserver.observe(el));
}
function startTrackingTimer(pid){
  stopTrackingTimer(pid);
  trackingTimers[pid]=setInterval(()=>{
    let p=state.panels[pid];
    if(!p||!p.viewStart) return;
    let elapsed=now()-p.viewStart;
    p.viewDuration+=elapsed;
    p.viewStart=now();
    p.viewCount++;
  },TRACK_INTERVAL);
}
function stopTrackingTimer(pid){
  if(trackingTimers[pid]){
    clearInterval(trackingTimers[pid]);
    delete trackingTimers[pid];
  }
}
function updateDataValues(){
  DEFAULT_PANELS.forEach(def=>{
    let p=state.panels[def.id];
    if(!p) return;
    p.value=currentValue(def);
    p._sparkData=state.panels[def.id]._sparkData;
  });
  $$('.panel',$('#grid')).forEach(el=>{
    let pid=el.dataset.panelId;
    let p=state.panels[pid];
    if(p&&!p.collapsed) updatePanelDOM(el,p);
  });
}
function updateLayoutModeUI(){
  let btn=$('#btnAutoLayout');
  let badge=$('#layoutModeBadge');
  if(btn){
    btn.textContent='Auto-Layout: '+(state.autoLayout?'On':'Off');
    btn.classList.toggle('active',state.autoLayout);
  }
  if(badge){
    badge.textContent=state.autoLayout?'auto':'manual';
    badge.className='layout-badge '+(state.autoLayout?'auto':'manual');
  }
}
function showToast(msg){
  let existing=$('.toast');
  if(existing) existing.remove();
  let toast=document.createElement('div');
  toast.className='toast';
  toast.textContent=msg;
  document.body.appendChild(toast);
  setTimeout(()=>toast.remove(),2500);
}
function initHeatmap(){
  heatmapCanvas=$('#heatmapCanvas');
  if(!heatmapCanvas) return;
  heatmapCanvas.width=window.innerWidth;
  heatmapCanvas.height=window.innerHeight;
  heatmapCtx=heatmapCanvas.getContext('2d');
  window.addEventListener('resize',()=>{
    heatmapCanvas.width=window.innerWidth;
    heatmapCanvas.height=window.innerHeight;
    if(heatmapActive) renderHeatmap();
  });
  document.addEventListener('mousemove',debounce(e=>{
    if(!heatmapActive) return;
    heatmapPoints.push({x:e.clientX,y:e.clientY,t:now(),w:1});
    if(heatmapPoints.length>500) heatmapPoints.shift();
    renderHeatmap();
  },50));
}
function renderHeatmap(){
  if(!heatmapCtx||!heatmapCanvas) return;
  let ctx=heatmapCtx;
  let w=heatmapCanvas.width,h=heatmapCanvas.height;
  ctx.clearRect(0,0,w,h);
  let nowMs=now();
  heatmapPoints=heatmapPoints.filter(pt=>nowMs-pt.t<30000);
  heatmapPoints.forEach(pt=>{
    let age=(nowMs-pt.t)/30000;
    let alpha=(1-age)*0.6;
    let radius=30*(1-age*0.5)+10;
    let grad=ctx.createRadialGradient(pt.x,pt.y,0,pt.x,pt.y,radius);
    grad.addColorStop(0,'rgba(255,140,60,'+alpha+')');
    grad.addColorStop(0.5,'rgba(255,100,30,'+alpha*0.5+')');
    grad.addColorStop(1,'rgba(255,60,0,0)');
    ctx.beginPath();
    ctx.arc(pt.x,pt.y,radius,0,Math.PI*2);
    ctx.fillStyle=grad;
    ctx.fill();
  });
  if(heatmapActive) requestAnimationFrame(()=>{if(heatmapActive) renderHeatmap()});
}
function toggleHeatmap(){
  heatmapActive=!heatmapActive;
  heatmapCanvas.style.display=heatmapActive?'block':'none';
  heatmapCanvas.classList.toggle('active',heatmapActive);
  $('#btnHeatmap').classList.toggle('active',heatmapActive);
  if(heatmapActive){
    heatmapPoints=[];
    renderHeatmap();
  }else{
    if(heatmapCtx) heatmapCtx.clearRect(0,0,heatmapCanvas.width,heatmapCanvas.height);
  }
}
function resetAll(){
  state.panels={};
  state.panelOrder=DEFAULT_PANELS.map(d=>d.id);
  state.collapsedIds=[];
  state.columns=4;
  state.autoLayout=true;
  DEFAULT_PANELS.forEach(def=>{state.panels[def.id]=initPanelState(def)});
  Object.values(trackingTimers).forEach(clearInterval);
  trackingTimers={};
  updateLayoutModeUI();
  $('#grid').className='grid cols-4';
  computeRanks();
  computeLayout();
  rebuildGrid();
  persistState();
  showToast('Layout reset');
}
function init(){
  loadState();
  computeRanks();
  computeLayout();
  rebuildGrid();
  updateLayoutModeUI();
  setupIntersectionObserver();
  initHeatmap();
  $('#btnAutoLayout').addEventListener('click',()=>{
    state.autoLayout=!state.autoLayout;
    if(state.autoLayout){
      Object.values(state.panels).forEach(p=>{if(!p.collapsed){p.locked=false;p.manualPos=-1}});
      computeLayout();
      rebuildGrid();
    }
    updateLayoutModeUI();
    persistState();
    showToast(state.autoLayout?'Auto-layout enabled':'Manual mode');
  });
  $('#btnReset').addEventListener('click',resetAll);
  $('#btnHeatmap').addEventListener('click',toggleHeatmap);
  $('#btnCols3').addEventListener('click',()=>{
    state.columns=3;
    $('#grid').className='grid cols-3';
    persistState();
  });
  $('#btnCols4').addEventListener('click',()=>{
    state.columns=4;
    $('#grid').className='grid cols-4';
    persistState();
  });
  $('#grid').addEventListener('dragover',e=>e.preventDefault());
  dataTimer=setInterval(updateDataValues,DATA_TICK);
  updateDataValues();
  rankTimer=setInterval(()=>{
    computeRanks();
    if(state.autoLayout){
      let changed=computeLayout();
      if(changed) rebuildGrid();
      else{
        $$('.panel',$('#grid')).forEach(el=>{
          let pid=el.dataset.panelId;
          let p=state.panels[pid];
          if(p) updatePanelDOM(el,p);
        });
      }
    }
    schedulePersist();
  },RANK_INTERVAL);
  window.addEventListener('beforeunload',()=>{
    Object.values(state.panels).forEach(p=>{
      if(p.viewStart){
        p.viewDuration+=now()-p.viewStart;
        p.viewStart=null;
        p.lastViewed=now();
      }
    });
    persistState();
    if(intersectionObserver) intersectionObserver.disconnect();
    Object.values(trackingTimers).forEach(clearInterval);
    clearInterval(dataTimer);
    clearInterval(rankTimer);
  });
}
document.addEventListener('DOMContentLoaded',init);
})();
</script>
</body>
</html>