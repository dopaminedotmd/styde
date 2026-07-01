<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--text:#e2e8f0;--accent:#38bdf8;--low:#64748b;--border:#334155;--rank1:#38bdf8;--rank2:#a78bfa;--rank3:#fb923c;--rank4:#4ade80;--rank5:#f472b6}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;min-height:100vh;padding:12px}
h1{font-size:1.1rem;margin-bottom:8px;color:var(--accent)}
.toolbar{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.toolbar button{background:var(--panel);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem}
.toolbar button:hover{border-color:var(--accent)}
.toolbar button.active{background:var(--accent);color:var(--bg)}
#grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;transition:all .3s}
.panel{background:var(--panel);border:1px solid var(--border);border-radius:8px;overflow:hidden;transition:all .3s;position:relative}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important;max-height:120px;opacity:.7}
.panel.compact .body{display:none}
.panel.collapsed{max-height:44px}
.panel.collapsed .body,.panel.collapsed .stats{display:none}
.panel-header{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:rgba(0,0,0,.2);cursor:move;user-select:none;font-size:0.85rem;font-weight:600}
.panel-header .rank-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}
.panel-header .actions{display:flex;gap:4px}
.panel-header button{background:none;border:none;color:var(--text);cursor:pointer;font-size:0.8rem;padding:2px 6px;border-radius:4px;opacity:.6}
.panel-header button:hover{opacity:1;background:rgba(255,255,255,.1)}
.panel-header button.locked{opacity:1;color:#fbbf24}
.body{padding:10px;min-height:60px}
.metric{font-size:1.8rem;font-weight:700;margin-bottom:4px}
.metric-label{font-size:0.75rem;color:var(--low)}
.spark{height:30px;background:linear-gradient(90deg,var(--accent),transparent);border-radius:4px;margin-top:6px;opacity:.3}
.stats{display:flex;gap:12px;padding:6px 10px;font-size:0.65rem;color:var(--low);border-top:1px solid var(--border)}
.stats span{display:flex;align-items:center;gap:3px}
.drag-over{border-color:var(--accent)!important;box-shadow:0 0 12px rgba(56,189,248,.3)}
.pinned{border-left:3px solid #fbbf24}
.more-section{grid-column:1/-1;text-align:center;padding:8px;color:var(--low);font-size:0.75rem;cursor:pointer}
.more-section:hover{color:var(--text)}
.toast{position:fixed;bottom:20px;right:20px;background:var(--accent);color:var(--bg);padding:8px 16px;border-radius:6px;font-size:0.8rem;animation:fadeout 2s forwards;z-index:999}
@keyframes fadeout{0%,70%{opacity:1}100%{opacity:0}}
</style>
</head>
<body>
<h1>Adaptive Layout</h1>
<div class="toolbar">
  <button onclick="resetData()">Reset tracking</button>
  <button onclick="autoArrange()">Auto-arrange</button>
  <span style="font-size:0.7rem;color:var(--low);align-self:center">Drag to override | Lock to pin</span>
</div>
<div id="grid"></div>
<script>
const STORAGE_KEY='adaptive_layout_v1';
const DEBOUNCE_MS=150;
const METRICS=['Revenue','Users','Conversion','Latency','Errors','CPU Load','Memory','Throughput','Sessions','Bounce Rate'];
const RANK_COLORS=['var(--rank1)','var(--rank2)','var(--rank3)','var(--rank4)','var(--rank5)']
let state={panels:{},order:[],locked:{},positions:{}};
let observers=[],renderTimer=null,scrollTimer=null;
function loadState(){
  try{return JSON.parse(localStorage.getItem(STORAGE_KEY))||{}}catch(e){return{}}
}
function saveState(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}
function initPanels(){
  let saved=loadState();
  METRICS.forEach((name,i)=>{
    let id='p'+i;
    let savedP=saved.panels&&saved.panels[id]||{};
    state.panels[id]={
      id,name,
      views:savedP.views||0,
      totalDuration:savedP.totalDuration||0,
      lastViewed:savedP.lastViewed||0,
      interactions:savedP.interactions||0,
      collapsed:savedP.collapsed||false
    };
  });
  state.order=saved.order||METRICS.map((_,i)=>'p'+i);
  state.locked=saved.locked||{};
  state.positions=saved.positions||{};
}
function computeScore(p){
  let hoursSince=(Date.now()-p.lastViewed)/3600000;
  let recency=Math.max(0.1,1/(1+hoursSince));
  return (p.views*0.3+p.totalDuration*0.4+p.interactions*0.3)*recency;
}
function rankPanels(){
  let scored=state.order.map(id=>({id,score:computeScore(state.panels[id])}));
  scored.sort((a,b)=>b.score-a.score);
  return scored;
}
function trackView(id){
  let p=state.panels[id];p.views++;p.lastViewed=Date.now();
  let observer=new IntersectionObserver((entries)=>{
    let entry=entries[0];
    if(entry.isIntersecting){
      let start=Date.now();
      let intv=setInterval(()=>{
        if(!document.getElementById(id)||!document.getElementById(id).offsetParent){clearInterval(intv);return}
        p.totalDuration+=(Date.now()-start)/1000;start=Date.now();
      },1000);
      observer.disconnect();
    }
  },{threshold:0.5});
  let el=document.getElementById(id);if(el)observer.observe(el);
  observers.push(observer);
}
function handleInteraction(id){state.panels[id].interactions++;saveState();render()}
function toggleCollapse(id){
  let p=state.panels[id];p.collapsed=!p.collapsed;handleInteraction(id)
}
function toggleLock(id){
  state.locked[id]=!state.locked[id];saveState();render();
  toast(state.locked[id]?'Panel pinned':'Panel unlocked');
}
function toast(msg){
  let t=document.createElement('div');t.className='toast';t.textContent=msg;
  document.body.appendChild(t);setTimeout(()=>t.remove(),2100);
}
function resetData(){localStorage.removeItem(STORAGE_KEY);initPanels();saveState();render();toast('Data reset')}
function autoArrange(){
  let ranked=rankPanels();
  ranked.forEach((r,i)=>{
    if(!state.locked[r.id])state.positions[r.id]=i;
  });
  state.order=ranked.map(r=>r.id);saveState();render();toast('Layout optimized')
}
function getRankIndex(id){
  if(state.positions[id]!==undefined)return state.positions[id];
  let ranked=rankPanels();return ranked.findIndex(r=>r.id===id);
}
function render(){
  clearTimeout(renderTimer);
  renderTimer=setTimeout(_render,DEBOUNCE_MS);
}
function _render(){
  let grid=document.getElementById('grid');let frag=document.createDocumentFragment();
  let ranked=rankPanels();let maxScore=ranked[0]?ranked[0].score:1;
  let ordered=state.order.slice();
  // apply position overrides
  Object.entries(state.positions).forEach(([id,pos])=>{
    ordered=ordered.filter(x=>x!==id);
    ordered.splice(Math.min(pos,ordered.length),0,id);
  });
  let shown=[],hidden=[];
  ordered.forEach((id,i)=>{
    let p=state.panels[id];let score=computeScore(p);
    let isCompact=!state.locked[id]&&i>=Math.min(6,ordered.length-2)&&score<maxScore*0.3;
    if(isCompact&&ordered.length>6)hidden.push({id,p,score,i});else shown.push({id,p,score,i});
  });
  shown.forEach(({id,p,score,i})=>{
    let rankIdx=getRankIndex(id);let color=RANK_COLORS[Math.min(rankIdx,4)];
    let locked=state.locked[id];let isCompact=!locked&&score<maxScore*0.2&&i>=5;
    let existing=document.getElementById(id);
    let panel=existing||document.createElement('div');
    if(!existing)panel.id=id;
    panel.className='panel'+(state.panels[id].collapsed?' collapsed':'')+(isCompact?' compact':'')+(locked?' pinned':'');
    panel.draggable=!locked;
    panel.style.gridRow=rankIdx<3?'span 2':'span 1';
    panel.style.gridColumn=rankIdx<2?'span 2':'span 1';
    panel.style.borderTopColor=color;
    let relScore=Math.min(100,Math.round(score/maxScore*100));
    panel.innerHTML=`
      <div class="panel-header">
        <span><span class="rank-dot" style="background:${color}"></span>${p.name}</span>
        <span class="actions">
          <button class="${locked?'locked':''}" onclick="toggleLock('${id}')" title="Lock">${locked?'&#128274;':'&#128275;'}</button>
          <button onclick="toggleCollapse('${id}')">${p.collapsed?'+':'-'}</button>
        </span>
      </div>
      <div class="body">
        <div class="metric">${Math.floor(Math.random()*1000)}${p.name.includes('Rate')?'%':p.name.includes('Latency')?'ms':''}</div>
        <div class="metric-label">${p.name} • rel score ${relScore}</div>
        <div class="spark" style="width:${30+relScore}%"></div>
      </div>
      <div class="stats">
        <span>&#128065; ${p.views}</span><span>&#9201; ${p.totalDuration.toFixed(0)}s</span><span>&#128172; ${p.interactions}</span>
      </div>`;
    panel.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',id);e.target.classList.add('dragging')});
    panel.addEventListener('dragend',e=>{e.target.classList.remove('dragging')});
    panel.addEventListener('dragover',e=>{e.preventDefault();e.currentTarget.classList.add('drag-over')});
    panel.addEventListener('dragleave',e=>{e.currentTarget.classList.remove('drag-over')});
    panel.addEventListener('drop',e=>{
      e.preventDefault();e.currentTarget.classList.remove('drag-over');
      let from=e.dataTransfer.getData('text/plain');let to=id;
      let fromIdx=state.order.indexOf(from);let toIdx=state.order.indexOf(to);
      if(fromIdx>=0&&toIdx>=0){state.order.splice(fromIdx,1);state.order.splice(toIdx,0,from);saveState();render();toast('Reordered')}
    });
    panel.addEventListener('click',e=>{if(!e.target.closest('button'))handleInteraction(id)});
    if(!existing){frag.appendChild(panel);trackView(id)}
  });
  if(hidden.length){
    let more=document.createElement('div');more.className='more-section';
    more.textContent='+ '+hidden.length+' more';
    more.onclick=()=>{hidden.forEach(h=>{state.positions[h.id]=0;state.locked[h.id]=true});saveState();render()};
    frag.appendChild(more);
  }
  // virtual diff: only replace changed panels, keep rest
  let currentIds=new Set(ordered);
  Array.from(grid.children).forEach(child=>{
    if(!currentIds.has(child.id)&&!child.classList.contains('more-section'))child.remove();
  });
  if(frag.children.length)grid.appendChild(frag);
}
// scroll debounce with rAF
let rafId=null;
window.addEventListener('scroll',()=>{
  if(rafId)return;
  rafId=requestAnimationFrame(()=>{
    // no-op render on scroll; view tracking handles intersection
    rafId=null;
  });
},{passive:true});
// cleanup
window.addEventListener('beforeunload',()=>{
  observers.forEach(o=>o.disconnect());
  observers=[];
  clearTimeout(renderTimer);
});
// init
initPanels();render();
// periodic auto-arrange (every 30s if unlocked panels exist)
setInterval(()=>{if(!Object.keys(state.locked).length||Object.values(state.locked).some(v=>!v))autoArrange()},30000);
</script>
</body>
</html>