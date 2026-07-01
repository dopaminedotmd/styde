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
  --surface2: #222636;
  --border: #2a2e3a;
  --text: #d1d5db;
  --text2: #9ca3af;
  --accent: #6366f1;
  --accent2: #818cf8;
  --danger: #ef4444;
  --success: #22c55e;
  --warn: #f59e0b;
  --radius: 10px;
  --gap: 12px;
  --transition: 350ms cubic-bezier(0.4, 0, 0.2, 1);
  --panel-min: 180px;
  --panel-compact: 120px;
  --panel-large: 400px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.app{max-width:1440px;margin:0 auto;padding:16px}
.toolbar{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--surface);border-radius:var(--radius);margin-bottom:16px;flex-wrap:wrap}
.toolbar h1{font-size:1.1rem;font-weight:600;color:var(--accent2);white-space:nowrap}
.toolbar .spacer{flex:1}
.btn{padding:7px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:0.82rem;transition:all 150ms;white-space:nowrap}
.btn:hover{background:var(--border);color:#fff}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.small{padding:4px 8px;font-size:0.72rem}
.badge{font-size:0.7rem;padding:2px 8px;border-radius:12px;background:var(--surface2);color:var(--text2)}
.badge.hot{background:#7c3aed20;color:#a78bfa;border:1px solid #7c3aed40}
.badge.cold{background:#374151;color:#6b7280}
.badge.locked{background:#f59e0b20;color:#fbbf24;border:1px solid #f59e0b40}
.grid{display:grid;gap:var(--gap);transition:all var(--transition)}
.grid.mode-large{grid-template-columns:repeat(auto-fill,minmax(var(--panel-large),1fr));grid-auto-rows:minmax(280px,auto)}
.grid.mode-compact{grid-template-columns:repeat(auto-fill,minmax(var(--panel-compact),1fr));grid-auto-rows:minmax(100px,auto)}
.grid.mode-adaptive{grid-template-columns:repeat(auto-fill,minmax(var(--panel-min),1fr));grid-auto-rows:minmax(180px,auto)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);display:flex;flex-direction:column;position:relative;cursor:grab}
.panel:active{cursor:grabbing}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 1;grid-row:span 1}
.panel.compact{grid-column:span 1;grid-row:span 1;max-height:140px}
.panel.compact .panel-body{overflow:hidden;display:flex;align-items:center;justify-content:center;gap:8px;flex-direction:row}
.panel.compact .panel-body>*{transform:scale(0.7);transform-origin:center}
.panel.compact .panel-stats{display:none}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--surface2);border-bottom:1px solid var(--border);gap:8px;min-height:44px}
.panel-header .title{font-weight:600;font-size:0.88rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-header .actions{display:flex;gap:4px;flex-shrink:0}
.panel-body{flex:1;padding:14px;display:flex;flex-direction:column;gap:10px;overflow-y:auto;position:relative}
.panel-stats{font-size:0.72rem;color:var(--text2);display:flex;gap:12px;padding:4px 14px 10px;flex-wrap:wrap}
.panel-stats span{white-space:nowrap}
.chart-bar{display:flex;align-items:flex-end;gap:6px;height:100px;padding:4px 0}
.chart-bar .bar{flex:1;background:var(--accent);border-radius:3px 3px 0 0;min-width:12px;transition:height 300ms}
.chart-bar .bar.low{background:var(--warn)}
.chart-bar .bar.high{background:var(--success)}
.metric-big{font-size:2.4rem;font-weight:700;color:var(--accent2);line-height:1}
.metric-label{font-size:0.78rem;color:var(--text2)}
.gauge{position:relative;width:80px;height:80px;flex-shrink:0}
.gauge svg{transform:rotate(-90deg)}
.gauge .value{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:1.2rem;font-weight:700}
.table-mini{font-size:0.75rem;width:100%;border-collapse:collapse}
.table-mini td,.table-mini th{padding:4px 8px;border-bottom:1px solid var(--border);text-align:left}
.table-mini th{color:var(--text2);font-weight:500}
.heat-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
.heat-dot.hot{background:var(--danger)}
.heat-dot.warm{background:var(--warn)}
.heat-dot.cool{background:var(--accent)}
.lock-indicator{position:absolute;top:6px;right:6px;font-size:0.7rem;color:#fbbf24;pointer-events:none;opacity:0.8}
.panel.locked{border-color:#f59e0b60;box-shadow:0 0 0 1px #f59e0b20}
.panel.dragging{opacity:0.7;z-index:100}
.drag-ghost{opacity:0.3;border:2px dashed var(--accent);border-radius:var(--radius)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.panel.just-interacted{animation:pulse 600ms ease-out}
.hidden-panel{display:none}
</style>
</head>
<body>
<div class="app">
  <div class="toolbar">
    <h1>Adaptive Layout</h1>
    <button class="btn active" data-mode="adaptive" onclick="Layout.setMode('adaptive')">Adaptive</button>
    <button class="btn" data-mode="large" onclick="Layout.setMode('large')">All Large</button>
    <button class="btn" data-mode="compact" onclick="Layout.setMode('compact')">All Compact</button>
    <span class="spacer"></span>
    <span class="badge" id="stats-overview">0 panels tracked</span>
    <button class="btn small" onclick="Layout.reset()">Reset Tracking</button>
    <button class="btn small" onclick="Layout.exportData()">Export</button>
  </div>
  <div class="grid mode-adaptive" id="dashboard-grid"></div>
</div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_layout_v1';
const DECAY_HALF_LIFE = 7 * 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD = 0.15;
const LARGE_THRESHOLD = 0.65;
const REBALANCE_INTERVAL = 5000;
const VIEW_DURATION_MIN = 500;
const OBSERVER_THRESHOLD = 0.5;
let rafId = null;
let rebalanceTimer = null;
let pendingUpdate = false;
let layoutDirty = false;
let animatingCount = 0;
function now(){return Date.now()}
function decay(t){return Math.pow(0.5,(now()-t)/DECAY_HALF_LIFE)}
function memoize(fn){
  let lastArgs=null,lastResult=null;
  return function(...args){
    if(lastArgs && lastArgs.length===args.length && lastArgs.every((a,i)=>a===args[i])){
      return lastResult;
    }
    lastArgs=args;
    lastResult=fn.apply(this,args);
    return lastResult;
  };
}
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',type:'big-number',value:84720,fmt:'$',icon:'',trend:'+12.4%'},
  {id:'users',title:'Active Users',type:'big-number',value:12453,fmt:'',icon:'',trend:'+5.7%'},
  {id:'conversion',title:'Conversion Rate',type:'gauge',value:3.8,max:10,unit:'%',trend:'-0.2%'},
  {id:'churn',title:'Churn Rate',type:'gauge',value:2.1,max:10,unit:'%',trend:'+0.1%'},
  {id:'traffic',title:'Traffic Sources',type:'bars',bars:[{label:'Organic',v:4200},{label:'Paid',v:2800},{label:'Social',v:1900},{label:'Email',v:1500},{label:'Direct',v:1100}]},
  {id:'errors',title:'Error Rate',type:'gauge',value:0.4,max:5,unit:'%',trend:'stable'},
  {id:'latency',title:'P95 Latency',type:'big-number',value:187,fmt:'',unit:'ms',trend:'-8ms'},
  {id:'endpoints',title:'Top Endpoints',type:'table',rows:[{name:'/api/search',calls:8921},{name:'/api/auth',calls:7432},{name:'/api/orders',calls:5120},{name:'/api/users',calls:3890}]},
  {id:'cpu',title:'CPU Usage',type:'gauge',value:62,max:100,unit:'%',trend:'+3%'},
  {id:'memory',title:'Memory',type:'gauge',value:78,max:100,unit:'%',trend:'+1%'},
  {id:'disk',title:'Disk IOPS',type:'big-number',value:3200,fmt:'',unit:'/s',trend:'stable'},
  {id:'cache',title:'Cache Hit Ratio',type:'gauge',value:94.2,max:100,unit:'%',trend:'+0.5%'},
];
let state = {
  panels: {},
  order: [],
  mode: 'adaptive',
  rebalanceCount: 0
};
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw){
      const saved = JSON.parse(raw);
      if(saved.panels) state.panels = saved.panels;
      if(saved.order) state.order = saved.order;
      if(saved.mode) state.mode = saved.mode;
      if(saved.rebalanceCount!=null) state.rebalanceCount = saved.rebalanceCount;
    }
  }catch(e){}
  PANEL_DEFS.forEach(def=>{
    if(!state.panels[def.id]){
      state.panels[def.id]={
        viewCount:0,
        totalDuration:0,
        interactions:0,
        lastViewed:0,
        expandCount:0,
        collapseCount:0,
        locked:false,
        manualSize:null,
        manualPosition:null,
        firstSeen:now()
      };
    }
    const p=state.panels[def.id];
    p.viewCount=p.viewCount||0;
    p.totalDuration=p.totalDuration||0;
    p.interactions=p.interactions||0;
    p.lastViewed=p.lastViewed||0;
    p.expandCount=p.expandCount||0;
    p.collapseCount=p.collapseCount||0;
    p.locked=!!p.locked;
    p.manualSize=p.manualSize||null;
    p.manualPosition=p.manualPosition||null;
    p.firstSeen=p.firstSeen||now();
  });
  if(!state.order.length || state.order.length!==PANEL_DEFS.length){
    state.order = PANEL_DEFS.map(d=>d.id);
  }
}
function saveState(){
  try{
    localStorage.setItem(STORAGE_KEY,JSON.stringify({
      panels:state.panels,
      order:state.order,
      mode:state.mode,
      rebalanceCount:state.rebalanceCount
    }));
  }catch(e){}
}
const computeScore = memoize(function(panelId){
  const p = state.panels[panelId];
  if(!p) return 0;
  const recency = decay(p.lastViewed || p.firstSeen);
  const frequency = p.viewCount + p.interactions * 0.8 + p.expandCount * 0.5;
  const avgDuration = p.viewCount > 0 ? p.totalDuration / p.viewCount : 0;
  const durationNorm = Math.min(avgDuration / 30000, 1);
  const engagement = frequency * 0.4 + durationNorm * 0.35 + recency * 0.25;
  return engagement;
});
function batchDOMReads(ids){
  const results = {};
  ids.forEach(id=>{
    const el = document.getElementById('panel-'+id);
    if(el){
      results[id] = {
        rect: el.getBoundingClientRect(),
        visible: el.offsetParent !== null,
        sizeClass: el.classList.contains('large')?'large':(el.classList.contains('compact')?'compact':'medium')
      };
    }
  });
  return results;
}
function batchDOMWrites(updates){
  const frag = document.createDocumentFragment();
  updates.forEach(u=>{
    const el = document.getElementById('panel-'+u.id);
    if(!el) return;
    if(u.sizeClass) el.className = el.className.replace(/panel (large|medium|compact)/,'panel '+u.sizeClass);
    if(u.order!==undefined) el.style.order = u.order;
    if(u.classList){
      u.classList.add.forEach(c=>el.classList.add(c));
      u.classList.remove.forEach(c=>el.classList.remove(c));
    }
  });
}
function cancelStaleFrame(){
  if(rafId!==null){
    cancelAnimationFrame(rafId);
    rafId=null;
  }
}
function scheduleRebalance(){
  cancelStaleFrame();
  rafId = requestAnimationFrame(()=>{
    rafId=null;
    rebalance();
  });
}
function rebalance(){
  layoutDirty=false;
  const scores = state.order.map(id=>({id,score:computeScore(id)}));
  const maxScore = Math.max(...scores.map(s=>s.score),0.001);
  scores.sort((a,b)=>b.score-a.score);
  const updates = scores.map((s,i)=>{
    let sizeClass;
    const norm = s.score/maxScore;
    const p = state.panels[s.id];
    if(p.manualSize){sizeClass=p.manualSize}
    else if(p.locked && state.order.indexOf(s.id)<4){sizeClass='large'}
    else if(norm>=LARGE_THRESHOLD)sizeClass='large';
    else if(norm<=COMPACT_THRESHOLD)sizeClass='compact';
    else sizeClass='medium';
    return {id:s.id,sizeClass,order:i};
  });
  if(animatingCount===0){
    batchDOMWrites(updates);
  }else{
    updates.forEach(u=>{
      const el=document.getElementById('panel-'+u.id);
      if(el){
        el.className=el.className.replace(/panel (large|medium|compact)/,'panel '+u.sizeClass);
        el.style.order=u.order;
      }
    });
  }
  updateStats();
  state.rebalanceCount++;
  saveState();
}
function updateStats(){
  const el=document.getElementById('stats-overview');
  if(!el)return;
  el.textContent=state.rebalanceCount+' rebalances';
}
let observer=null;
let viewEntries={};
function setupObserver(){
  if(observer)observer.disconnect();
  observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      const id=entry.target.dataset.panelId;
      if(!id)return;
      if(entry.isIntersecting && entry.intersectionRatio>=OBSERVER_THRESHOLD){
        viewEntries[id]=now();
      }else if(viewEntries[id]){
        const duration=now()-viewEntries[id];
        if(duration>=VIEW_DURATION_MIN){
          state.panels[id].totalDuration+=duration;
          state.panels[id].viewCount++;
          state.panels[id].lastViewed=now();
          layoutDirty=true;
        }
        delete viewEntries[id];
      }
    });
    if(layoutDirty)scheduleRebalance();
  },{threshold:[0,0.25,0.5,0.75,1.0]});
}
function observePanel(el){
  if(observer)observer.observe(el);
}
function unobservePanel(el){
  if(observer)observer.unobserve(el);
}
function render(){
  const grid=document.getElementById('dashboard-grid');
  if(!grid)return;
  grid.innerHTML='';
  state.order.forEach((id,i)=>{
    const def=PANEL_DEFS.find(d=>d.id===id);
    if(!def)return;
    const p=state.panels[id];
    const score=computeScore(id);
    const norm=Math.max(...state.order.map(i=>computeScore(i)),0.001);
    const sizeClass=p.manualSize||(p.locked&&i<4?'large':(score/norm>=LARGE_THRESHOLD?'large':(score/norm<=COMPACT_THRESHOLD?'compact':'medium')));
    const el=document.createElement('div');
    el.className='panel '+sizeClass+(p.locked?' locked':'');
    el.id='panel-'+id;
    el.dataset.panelId=id;
    el.draggable=true;
    el.style.order=i;
    el.innerHTML=buildPanelHTML(def,p,score);
    el.addEventListener('click',e=>{
      if(e.target.closest('.btn'))return;
      state.panels[id].interactions++;
      state.panels[id].lastViewed=now();
      el.classList.add('just-interacted');
      setTimeout(()=>el.classList.remove('just-interacted'),600);
      layoutDirty=true;
      scheduleRebalance();
      saveState();
    });
    el.addEventListener('dragstart',e=>{
      e.dataTransfer.setData('text/plain',id);
      el.classList.add('dragging');
      animatingCount++;
    });
    el.addEventListener('dragend',e=>{
      el.classList.remove('dragging');
      animatingCount=Math.max(0,animatingCount-1);
      if(animatingCount===0 && layoutDirty)scheduleRebalance();
    });
    el.addEventListener('dragover',e=>{e.preventDefault();el.classList.add('drag-ghost')});
    el.addEventListener('dragleave',e=>{el.classList.remove('drag-ghost')});
    el.addEventListener('drop',e=>{
      e.preventDefault();
      el.classList.remove('drag-ghost');
      const fromId=e.dataTransfer.getData('text/plain');
      const toId=id;
      const fromIdx=state.order.indexOf(fromId);
      const toIdx=state.order.indexOf(toId);
      if(fromIdx>=0&&toIdx>=0&&fromIdx!==toIdx){
        state.order.splice(fromIdx,1);
        state.order.splice(toIdx,0,fromId);
        state.panels[fromId].manualPosition=toIdx;
        state.panels[fromId].lastViewed=now();
        layoutDirty=true;
        scheduleRebalance();
        saveState();
        render();
      }
    });
    grid.appendChild(el);
    observePanel(el);
  });
  if(observer)setupObserver();
}
function buildPanelHTML(def,p,score){
  let body='';
  switch(def.type){
    case 'big-number':
      body='<div class="metric-big">'+(def.fmt||'')+(def.value||0).toLocaleString()+(def.unit||'')+'</div>';
      body+='<div class="metric-label">'+(def.trend||'')+'</div>';
      break;
    case 'gauge':
      const pct=def.max?Math.min((def.value/def.max)*100,100):0;
      const r=30;const circ=2*Math.PI*r;const offset=circ-(pct/100)*circ;
      body='<div class="gauge"><svg width="80" height="80" viewBox="0 0 80 80"><circle cx="40" cy="40" r="'+r+'" fill="none" stroke="var(--border)" stroke-width="6"/><circle cx="40" cy="40" r="'+r+'" fill="none" stroke="var(--accent)" stroke-width="6" stroke-dasharray="'+circ+'" stroke-dashoffset="'+offset+'" stroke-linecap="round"/></svg><div class="value">'+(def.value||0)+'</div></div>';
      body+='<div class="metric-label">'+(def.trend||'')+' / '+(def.max||0)+(def.unit||'')+' max</div>';
      break;
    case 'bars':
      const maxV=Math.max(...(def.bars||[]).map(b=>b.v),1);
      body='<div class="chart-bar">'+(def.bars||[]).map(b=>{
        const h=(b.v/maxV)*100;
        const cls=h>70?'high':(h<25?'low':'');
        return '<div class="bar '+cls+'" style="height:'+h+'%" title="'+b.label+': '+b.v+'"></div>';
      }).join('')+'</div>';
      body+='<div style="display:flex;gap:6px;font-size:0.68rem;color:var(--text2)">'+(def.bars||[]).map(b=>'<span>'+b.label+'</span>').join('')+'</div>';
      break;
    case 'table':
      body='<table class="table-mini"><thead><tr><th>Endpoint</th><th>Calls</th></tr></thead><tbody>'+(def.rows||[]).map(r=>'<tr><td>'+r.name+'</td><td>'+r.calls.toLocaleString()+'</td></tr>').join('')+'</tbody></table>';
      break;
    default:body='<div class="metric-label">No data</div>';
  }
  const heat=score>0.5?'hot':(score>0.2?'warm':'cool');
  return '<div class="panel-header"><span class="title"><span class="heat-dot '+heat+'"></span>'+def.title+'</span><div class="actions">'+
    (p.locked?'<button class="btn small active" onclick="Layout.unlock(\''+def.id+'\')" title="Unlock">L</button>':'<button class="btn small" onclick="Layout.lock(\''+def.id+'\')" title="Lock">L</button>')+
    '<button class="btn small" onclick="Layout.setSize(\''+def.id+'\',\'large\')" title="Large">+</button>'+
    '<button class="btn small" onclick="Layout.setSize(\''+def.id+'\',\'compact\')" title="Compact">-</button>'+
    '<button class="btn small" onclick="Layout.setSize(\''+def.id+'\',\'medium\')" title="Reset">R</button>'+
    '</div></div>'+
    '<div class="panel-body">'+body+'</div>'+
    '<div class="panel-stats">'+
    '<span>Views:'+p.viewCount+'</span>'+
    '<span>Interact:'+p.interactions+'</span>'+
    '<span>Score:'+score.toFixed(3)+'</span>'+
    '</div>'+
    (p.locked?'<div class="lock-indicator">LOCKED</div>':'');
}
window.Layout = {
  setMode: function(mode){
    state.mode = mode;
    const grid = document.getElementById('dashboard-grid');
    if(grid){
      grid.className = 'grid mode-'+mode;
    }
    document.querySelectorAll('.toolbar .btn[data-mode]').forEach(b=>b.classList.remove('active'));
    const btn=document.querySelector('.toolbar .btn[data-mode="'+mode+'"]');
    if(btn)btn.classList.add('active');
    if(mode==='adaptive'){
      scheduleRebalance();
    }
    saveState();
  },
  lock: function(id){
    state.panels[id].locked=true;
    state.panels[id].lastViewed=now();
    layoutDirty=true;
    scheduleRebalance();
    saveState();
    render();
  },
  unlock: function(id){
    state.panels[id].locked=false;
    state.panels[id].lastViewed=now();
    layoutDirty=true;
    scheduleRebalance();
    saveState();
    render();
  },
  setSize: function(id,size){
    if(state.panels[id].locked){
      state.panels[id].manualSize=size;
    }else{
      state.panels[id].locked=true;
      state.panels[id].manualSize=size;
    }
    state.panels[id].lastViewed=now();
    layoutDirty=true;
    scheduleRebalance();
    saveState();
    render();
  },
  reset: function(){
    if(observer)observer.disconnect();
    PANEL_DEFS.forEach(def=>{
      state.panels[def.id]={
        viewCount:0,totalDuration:0,interactions:0,lastViewed:0,
        expandCount:0,collapseCount:0,locked:false,
        manualSize:null,manualPosition:null,firstSeen:now()
      };
    });
    state.order=PANEL_DEFS.map(d=>d.id);
    state.rebalanceCount=0;
    layoutDirty=true;
    saveState();
    render();
    setupObserver();
  },
  exportData: function(){
    const data={panels:state.panels,order:state.order,mode:state.mode,rebalanceCount:state.rebalanceCount};
    console.log(JSON.stringify(data,null,2));
    alert('Exported to console');
  }
};
rebalanceTimer = setInterval(()=>{
  if(layoutDirty && animatingCount===0){
    scheduleRebalance();
  }
}, REBALANCE_INTERVAL);
loadState();
document.querySelectorAll('.toolbar .btn[data-mode]').forEach(b=>{
  if(b.dataset.mode===state.mode)b.classList.add('active');
  else b.classList.remove('active');
});
const grid=document.getElementById('dashboard-grid');
if(grid)grid.className='grid mode-'+state.mode;
render();
setupObserver();
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){
    Object.keys(viewEntries).forEach(id=>{
      if(viewEntries[id]){
        const duration=now()-viewEntries[id];
        if(duration>=VIEW_DURATION_MIN){
          state.panels[id].totalDuration+=duration;
          state.panels[id].viewCount++;
          state.panels[id].lastViewed=now();
          layoutDirty=true;
        }
        delete viewEntries[id];
      }
    });
    if(layoutDirty)scheduleRebalance();
    saveState();
  }
});
})();
</script>
</body>
</html>