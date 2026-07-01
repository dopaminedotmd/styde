```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#242836;--border:#2a2e3a;
  --text:#e1e4ed;--text2:#8b8fa3;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--radius:8px;--gap:10px;
  --transition:200ms ease;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px;overflow-x:hidden}
header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.2rem;font-weight:600;letter-spacing:-0.01em}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:6px 14px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);cursor:pointer;font-size:0.82rem;transition:background var(--transition);user-select:none;touch-action:manipulation}
.btn:hover{background:var(--surface2)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.badge{padding:2px 8px;border-radius:12px;font-size:0.72rem;background:var(--surface2);color:var(--text2)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);position:relative;min-height:200px}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;cursor:grab;transition:transform var(--transition),box-shadow var(--transition),opacity var(--transition);position:relative;overflow:hidden;touch-action:none;user-select:none}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.7;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,0.5);transform:scale(1.02)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent);transform:scale(1.01)}
.panel.locked{border-color:var(--warn);cursor:default}
.panel.locked:active{cursor:default}
.panel.compact{padding:8px 12px;font-size:0.78rem;grid-row:span 1!important;grid-column:span 1!important}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:block}
.panel.expanded .panel-preview{display:none}
.panel-header{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.panel-title{font-weight:600;font-size:0.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-score{font-size:0.7rem;color:var(--text2);white-space:nowrap}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions .btn{padding:2px 6px;font-size:0.7rem;border-radius:4px}
.panel-body{font-size:0.82rem;color:var(--text2);line-height:1.5}
.panel-value{font-size:1.6rem;font-weight:700;color:var(--text);margin:4px 0}
.panel-spark{height:40px;margin-top:6px;border-radius:4px;background:var(--surface2);overflow:hidden}
.panel-spark svg{width:100%;height:100%}
.panel-preview{display:none;font-size:0.72rem;color:var(--text2)}
.panel-rank{position:absolute;top:4px;right:8px;font-size:0.65rem;color:var(--border)}
.more-section{grid-column:1/-1;padding:8px;text-align:center}
.more-toggle{font-size:0.82rem;color:var(--accent);cursor:pointer;background:none;border:none}
.more-panels{display:none;margin-top:8px}
.more-panels.open{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:var(--gap)}
.toast{position:fixed;bottom:20px;right:20px;padding:10px 16px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius);font-size:0.82rem;z-index:200;opacity:0;transform:translateY(10px);transition:opacity 300ms,transform 300ms;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.stat-row{display:flex;gap:16px;margin-bottom:4px}
.stat-label{color:var(--text2);font-size:0.72rem}
.stat-val{font-weight:600;font-size:0.78rem}
@media(max-width:600px){.grid{grid-template-columns:1fr}.panel{padding:10px}}
</style>
</head>
<body>
<header>
  <div>
    <h1>Adaptive Dashboard</h1>
    <span class="badge" id="tracking-status">tracking active</span>
  </div>
  <div class="controls">
    <button class="btn" id="btn-reset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btn-lock-all" title="Lock all panels in place">Lock All</button>
    <button class="btn" id="btn-auto" title="Run auto-layout now">Auto-Layout</button>
    <button class="btn" id="btn-collapse-low" title="Compact low-rank panels">Compact Low</button>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const VIEWPORT_MARGIN = '0px 0px -40% 0px';
const COMPACT_THRESHOLD = 0.2;
const DECAY_HALF_LIFE_MS = 7 * 24 * 60 * 60 * 1000;
const MIN_SCORE = 0.001;
const SAVE_DEBOUNCE_MS = 500;
let panels = [];
let tracking = {};
let observer = null;
let timers = [];
let layoutScheduled = false;
let saveScheduled = false;
let dragState = null;
let intersectionLog = new Map();
let lastScoreSnapshot = null;
const grid = document.getElementById('grid');
const toast = document.getElementById('toast');
const statusEl = document.getElementById('tracking-status');
function now(){return Date.now()}
function el(tag,attrs={},...children){
  const e = document.createElement(tag);
  for(const[k,v]of Object.entries(attrs)){
    if(k==='className') e.className=v;
    else if(k.startsWith('on')) e.addEventListener(k.slice(2).toLowerCase(),v);
    else e.setAttribute(k,v);
  }
  for(const c of children){
    if(typeof c==='string') e.appendChild(document.createTextNode(c));
    else if(c) e.appendChild(c);
  }
  return e;
}
function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  const tid = setTimeout(()=>t.classList.remove('show'),2000);
  timers.push(tid);
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return null;
    return JSON.parse(raw);
  }catch(e){return null}
}
function saveState(){
  if(saveScheduled) return;
  saveScheduled = true;
  const tid = setTimeout(()=>{
    const state = {
      panels: panels.map(p=>({
        id:p.id, score:p.score, views:p.views, totalDuration:p.totalDuration,
        lastViewed:p.lastViewed, interactions:p.interactions, locked:p.locked,
        compact:p.compact, manualOrder:p.manualOrder
      })),
      order: panels.map(p=>p.id),
      savedAt: now()
    };
    try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}catch(e){}
    saveScheduled = false;
  },SAVE_DEBOUNCE_MS);
  timers.push(tid);
}
function computeScore(panel){
  const age = now() - (panel.lastViewed || now());
  const decay = Math.exp(-Math.log(2) * age / DECAY_HALF_LIFE_MS);
  const recency = Math.max(decay, 0.01);
  const views = Math.max(panel.views || 0, 1);
  const dur = Math.max(panel.totalDuration || 0, 1);
  const inter = Math.max(panel.interactions || 0, 1);
  return Math.max((views * dur * recency * (1 + Math.log1p(inter))) / 1000, MIN_SCORE);
}
function rankPanels(){
  let changed = false;
  for(const p of panels){
    const s = computeScore(p);
    if(Math.abs(p.score - s) > 0.001){changed = true}
    p.score = s;
  }
  if(changed){
    panels.sort((a,b)=>b.score - a.score);
    for(let i=0;i<panels.length;i++) panels[i].rank = i;
  }
  if(!lastScoreSnapshot || changed){
    lastScoreSnapshot = panels.map(p=>({id:p.id,score:p.score,rank:p.rank,compact:p.compact,locked:p.locked,manualOrder:p.manualOrder}));
  }
  return changed;
}
function diffLayout(prev, curr){
  const moves = [];
  const prevMap = new Map(prev.map((s,i)=>[s.id,{...s,index:i}]));
  for(let i=0;i<curr.length;i++){
    const c = curr[i];
    const p = prevMap.get(c.id);
    if(!p || p.rank !== c.rank || p.compact !== c.compact) moves.push({id:c.id,from:p?p.index:-1,to:i});
  }
  return moves;
}
function applyLayoutMutations(moves){
  if(moves.length===0) return;
  const domMap = new Map();
  for(const child of grid.children){
    const id = child.dataset.panelId;
    if(id) domMap.set(id,child);
  }
  for(const m of moves){
    const el = domMap.get(m.id);
    if(!el) continue;
    const panel = panels.find(p=>p.id===m.id);
    if(!panel) continue;
    if(panel.locked) continue;
    el.classList.toggle('compact', panel.compact);
    el.style.order = panel.rank;
    const ref = grid.children[panel.rank];
    if(ref && ref !== el){
      grid.insertBefore(el, ref);
    }else if(!ref && panel.rank >= grid.children.length){
      grid.appendChild(el);
    }
  }
}
function relayout(force=false){
  if(layoutScheduled && !force) return;
  layoutScheduled = true;
  requestAnimationFrame(()=>{
    const changed = rankPanels();
    if(!changed && !force){layoutScheduled=false;return}
    const curr = panels.map(p=>({id:p.id,rank:p.rank,compact:p.compact,locked:p.locked,manualOrder:p.manualOrder}));
    const moves = diffLayout(lastScoreSnapshot || [], curr);
    if(moves.length > 0) applyLayoutMutations(moves);
    else{
      for(const child of grid.children){
        const id = child.dataset.panelId;
        const panel = panels.find(p=>p.id===id);
        if(panel){
          child.style.order = panel.rank;
          child.classList.toggle('compact', panel.compact);
        }
      }
    }
    updatePanelDOM();
    lastScoreSnapshot = curr;
    layoutScheduled = false;
  });
}
function updatePanelDOM(){
  for(const child of grid.children){
    const id = child.dataset.panelId;
    const panel = panels.find(p=>p.id===id);
    if(!panel) continue;
    const scoreEl = child.querySelector('.panel-score');
    if(scoreEl) scoreEl.textContent = '#'+(panel.rank+1)+' · '+panel.score.toFixed(1);
    const rankEl = child.querySelector('.panel-rank');
    if(rankEl) rankEl.textContent = '#'+(panel.rank+1);
    const lockBtn = child.querySelector('[data-action="lock"]');
    if(lockBtn){
      lockBtn.textContent = panel.locked ? '🔒' : '🔓';
      lockBtn.classList.toggle('active', panel.locked);
    }
    const compactBtn = child.querySelector('[data-action="compact"]');
    if(compactBtn){
      compactBtn.textContent = panel.compact ? '⊞' : '⊟';
    }
  }
}
function recordInteraction(panelId, type){
  const panel = panels.find(p=>p.id===panelId);
  if(!panel) return;
  panel.interactions = (panel.interactions||0)+1;
  panel.lastViewed = now();
  relayout();
  saveState();
}
function createPanelElement(panel){
  const sparkData = Array.from({length:12},()=>Math.random()*40+30);
  const maxVal = Math.max(...sparkData);
  const points = sparkData.map((v,i)=>`${(i/(sparkData.length-1))*100},${100-(v/maxVal)*100}`).join(' ');
  const svg = `<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="${points}" fill="none" stroke="var(--accent2)" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>`;
  const e = el('div',{
    className:'panel expanded'+(panel.compact?' compact':''),
    'data-panel-id':panel.id,
    style:'order:'+panel.rank
  },
    el('span',{className:'panel-rank'},'#'+(panel.rank+1)),
    el('div',{className:'panel-header'},
      el('span',{className:'panel-title'},panel.title),
      el('span',{className:'panel-score'},'#'+(panel.rank+1)+' · '+panel.score.toFixed(1)),
      el('div',{className:'panel-actions'},
        el('button',{className:'btn','data-action':'lock',onClick(e){e.stopPropagation();toggleLock(panel.id)}},panel.locked?'🔒':'🔓'),
        el('button',{className:'btn','data-action':'compact',onClick(e){e.stopPropagation();toggleCompact(panel.id)}},panel.compact?'⊞':'⊟')
      )
    ),
    el('div',{className:'panel-body'},
      el('div',{className:'panel-value'},panel.value),
      el('div',{className:'stat-row'},
        el('span',{className:'stat-label'},'views:'),el('span',{className:'stat-val'},panel.views),
        el('span',{className:'stat-label'},'int:'),el('span',{className:'stat-val'},panel.interactions||0)
      ),
      el('div',{className:'panel-spark',innerHTML:svg})
    ),
    el('div',{className:'panel-preview'},panel.title+' · '+panel.value)
  );
  e.addEventListener('click',()=>recordInteraction(panel.id,'click'));
  e.addEventListener('pointerdown',onPointerDown);
  return e;
}
function toggleLock(panelId){
  const panel = panels.find(p=>p.id===panelId);
  if(!panel) return;
  panel.locked = !panel.locked;
  showToast(panel.locked ? panel.title+' locked' : panel.title+' unlocked');
  relayout(true);
  saveState();
}
function toggleCompact(panelId){
  const panel = panels.find(p=>p.id===panelId);
  if(!panel) return;
  panel.compact = !panel.compact;
  if(!panel.compact) panel.lastViewed = now();
  relayout(true);
  saveState();
}
function onPointerDown(e){
  const panelEl = e.currentTarget;
  const panelId = panelEl.dataset.panelId;
  const panel = panels.find(p=>p.id===panelId);
  if(!panel || panel.locked) return;
  if(e.target.closest('button')) return;
  e.preventDefault();
  panelEl.setPointerCapture(e.pointerId);
  dragState = {
    el: panelEl, panel, panelId,
    startX: e.clientX, startY: e.clientY,
    origRect: panelEl.getBoundingClientRect(),
    pointerId: e.pointerId,
    lastDropTarget: null,
    moved: false
  };
  panelEl.classList.add('dragging');
  const onMove = (ev)=>{
    if(!dragState || ev.pointerId !== dragState.pointerId) return;
    const dx = ev.clientX - dragState.startX;
    const dy = ev.clientY - dragState.startY;
    if(Math.abs(dx)>3 || Math.abs(dy)>3) dragState.moved = true;
    dragState.el.style.transform = `translate(${dx}px,${dy}px)`;
    dragState.el.style.zIndex = '100';
    const below = document.elementFromPoint(ev.clientX, ev.clientY);
    if(below){
      const targetPanel = below.closest('.panel');
      if(targetPanel && targetPanel !== dragState.el){
        if(dragState.lastDropTarget) dragState.lastDropTarget.classList.remove('drag-over');
        targetPanel.classList.add('drag-over');
        dragState.lastDropTarget = targetPanel;
      }else if(dragState.lastDropTarget && targetPanel !== dragState.lastDropTarget){
        dragState.lastDropTarget.classList.remove('drag-over');
        dragState.lastDropTarget = null;
      }
    }
  };
  const onUp = (ev)=>{
    if(!dragState) return;
    document.removeEventListener('pointermove',onMove);
    document.removeEventListener('pointerup',onUp);
    document.removeEventListener('pointercancel',onUp);
    dragState.el.classList.remove('dragging');
    dragState.el.style.transform = '';
    dragState.el.style.zIndex = '';
    if(dragState.lastDropTarget){
      dragState.lastDropTarget.classList.remove('drag-over');
      const targetId = dragState.lastDropTarget.dataset.panelId;
      const targetPanel = panels.find(p=>p.id===targetId);
      if(targetPanel && targetId !== dragState.panelId){
        const fromIdx = panels.indexOf(dragState.panel);
        const toIdx = panels.indexOf(targetPanel);
        if(fromIdx>=0 && toIdx>=0){
          panels.splice(fromIdx,1);
          panels.splice(toIdx,0,dragState.panel);
          dragState.panel.manualOrder = true;
          for(let i=0;i<panels.length;i++) panels[i].rank = i;
          lastScoreSnapshot = null;
          relayout(true);
          saveState();
          showToast(dragState.panel.title+' moved');
        }
      }
    }else if(!dragState.moved){
      recordInteraction(dragState.panelId,'click');
    }
    dragState = null;
  };
  document.addEventListener('pointermove',onMove);
  document.addEventListener('pointerup',onUp);
  document.addEventListener('pointercancel',onUp);
}
function initObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    const nowTs = now();
    for(const entry of entries){
      const panelId = entry.target.dataset.panelId;
      if(!panelId) continue;
      if(entry.isIntersecting){
        intersectionLog.set(panelId, nowTs);
      }else if(intersectionLog.has(panelId)){
        const start = intersectionLog.get(panelId);
        const duration = nowTs - start;
        intersectionLog.delete(panelId);
        const panel = panels.find(p=>p.id===panelId);
        if(panel && duration > 500){
          panel.views = (panel.views||0)+1;
          panel.totalDuration = (panel.totalDuration||0)+duration;
          panel.lastViewed = nowTs;
        }
      }
    }
    relayout();
  },{threshold:[0,0.1,0.5,1],rootMargin:VIEWPORT_MARGIN});
  for(const child of grid.children){
    observer.observe(child);
  }
}
function autoCompact(threshold){
  if(panels.length===0) return;
  const maxScore = Math.max(...panels.filter(p=>!p.locked).map(p=>p.score),1);
  let changed = false;
  for(const p of panels){
    if(p.locked) continue;
    const shouldCompact = (p.score / maxScore) < threshold;
    if(p.compact !== shouldCompact){
      p.compact = shouldCompact;
      changed = true;
    }
  }
  if(changed) relayout(true);
}
function buildAllDOM(){
  while(grid.firstChild) grid.removeChild(grid.firstChild);
  for(const panel of panels){
    grid.appendChild(createPanelElement(panel));
  }
  initObserver();
}
function initPanels(defaultPanels){
  const saved = loadState();
  if(saved && saved.panels && saved.panels.length === defaultPanels.length){
    panels = defaultPanels.map((dp,i)=>{
      const sp = saved.panels.find(p=>p.id===dp.id) || {};
      return {
        ...dp,
        views: sp.views || dp.views || 0,
        totalDuration: sp.totalDuration || dp.totalDuration || 0,
        lastViewed: sp.lastViewed || dp.lastViewed || now(),
        interactions: sp.interactions || dp.interactions || 0,
        locked: sp.locked || false,
        compact: sp.compact || false,
        manualOrder: sp.manualOrder || false,
        score: sp.score || 0
      };
    });
  }else{
    panels = defaultPanels.map(p=>({
      ...p,views:p.views||0,totalDuration:p.totalDuration||0,
      lastViewed:now(),interactions:0,locked:false,compact:false,
      manualOrder:false,score:0
    }));
  }
  rankPanels();
  buildAllDOM();
}
function resetAll(){
  panels.forEach(p=>{
    p.views=0;p.totalDuration=0;p.interactions=0;
    p.lastViewed=now();p.locked=false;p.compact=false;
    p.manualOrder=false;p.score=MIN_SCORE;
  });
  rankPanels();
  lastScoreSnapshot = null;
  buildAllDOM();
  saveState();
  showToast('Tracking data reset');
}
function lockAll(){
  const allLocked = panels.every(p=>p.locked);
  panels.forEach(p=>{p.locked=!allLocked});
  relayout(true);
  saveState();
  showToast(allLocked ? 'All unlocked' : 'All locked');
}
const defaultPanels = [
  {id:'cpu',title:'CPU Usage',value:'34%',type:'gauge',views:0,totalDuration:0},
  {id:'mem',title:'Memory',value:'8.2 GB',type:'gauge',views:0,totalDuration:0},
  {id:'req',title:'Requests/s',value:'1,247',type:'counter',views:0,totalDuration:0},
  {id:'err',title:'Error Rate',value:'0.12%',type:'counter',views:0,totalDuration:0},
  {id:'lat',title:'P99 Latency',value:'142ms',type:'timer',views:0,totalDuration:0},
  {id:'disk',title:'Disk I/O',value:'78 MB/s',type:'gauge',views:0,totalDuration:0},
  {id:'conn',title:'Connections',value:'3,842',type:'counter',views:0,totalDuration:0},
  {id:'cache',title:'Cache Hit Rate',value:'94.7%',type:'gauge',views:0,totalDuration:0},
  {id:'queue',title:'Queue Depth',value:'17',type:'counter',views:0,totalDuration:0},
  {id:'uptime',title:'Uptime',value:'47d 3h',type:'timer',views:0,totalDuration:0},
];
initPanels(defaultPanels);
document.getElementById('btn-reset').addEventListener('click',resetAll);
document.getElementById('btn-lock-all').addEventListener('click',lockAll);
document.getElementById('btn-auto').addEventListener('click',()=>{rankPanels();lastScoreSnapshot=null;relayout(true);showToast('Auto-layout applied')});
document.getElementById('btn-collapse-low').addEventListener('click',()=>{autoCompact(COMPACT_THRESHOLD);saveState();showToast('Low-rank panels compacted')});
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){
    const nowTs = now();
    for(const[id,start] of intersectionLog){
      const panel = panels.find(p=>p.id===id);
      if(panel){
        panel.totalDuration = (panel.totalDuration||0)+(nowTs-start);
        panel.lastViewed = nowTs;
      }
    }
    intersectionLog.clear();
  }
  statusEl.textContent = document.hidden ? 'tracking paused' : 'tracking active';
  if(!document.hidden) relayout();
});
window.addEventListener('beforeunload',()=>{
  if(observer) observer.disconnect();
  observer = null;
  for(const tid of timers) clearTimeout(tid);
  timers = [];
  saveState();
});
const periodicSave = setInterval(saveState,30000);
timers.push(periodicSave);
const periodicRelayout = setInterval(()=>relayout(),60000);
timers.push(periodicRelayout);
})();
</script>
</body>
</html>
```