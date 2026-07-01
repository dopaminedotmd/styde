<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --grid-min: 300px;
  --gap: 12px;
  --compact-scale: 0.45;
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --rank-1-scale: 1.0;
  --rank-2-scale: 0.85;
  --rank-3-scale: 0.7;
  --warn: #ff9e64;
  --transition: 0.35s cubic-bezier(0.4,0,0.2,1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.01em}
.stats{font-size:0.8rem;color:var(--text-dim);display:flex;gap:16px}
.btn{background:var(--panel-bg);border:1px solid var(--panel-border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:var(--transition)}
.btn:hover{background:var(--panel-border)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.dashboard{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(var(--grid-min),1fr));
  gap:var(--gap);
  transition:grid-template-columns 0.3s ease;
}
@media(max-width:768px){
  .dashboard{grid-template-columns:1fr}
}
.panel{
  background:var(--panel-bg);
  border:1px solid var(--panel-border);
  border-radius:10px;
  padding:14px;
  transition:all var(--transition);
  position:relative;
  min-height:120px;
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.panel:hover{border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.panel.compact{transform:scale(var(--compact-scale));opacity:0.75;order:100}
.panel.compact:hover{opacity:1;transform:scale(calc(var(--compact-scale) + 0.03))}
.panel.compact .panel-body{overflow:hidden;max-height:60px}
.panel.compact .panel-chart{display:none}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel-title{font-weight:600;font-size:0.9rem}
.panel-controls{display:flex;gap:4px}
.panel-ctrl{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:2px 4px;border-radius:4px;font-size:0.7rem;transition:all 0.15s}
.panel-ctrl:hover{color:var(--text);background:var(--panel-border)}
.panel-ctrl.pinned{color:var(--accent)}
.panel-body{font-size:0.82rem;color:var(--text-dim);flex:1}
.panel-value{font-size:1.6rem;font-weight:700;color:var(--text);line-height:1.1}
.panel-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-dim)}
.panel-score{position:absolute;top:6px;right:6px;font-size:0.6rem;color:var(--text-dim);opacity:0.5}
.panel-chart{height:40px;margin-top:8px;display:flex;align-items:flex-end;gap:2px}
.chart-bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-height:2px;opacity:0.6;transition:height 0.3s}
.panel.locked{border-color:var(--warn);box-shadow:0 0 12px rgba(255,158,100,0.1)}
.panel.locked::after{content:'LOCKED';position:absolute;top:6px;left:6px;font-size:0.55rem;color:var(--warn);opacity:0.7;letter-spacing:0.08em}
.drag-handle{cursor:grab;color:var(--text-dim);font-size:0.7rem;user-select:none}
.drag-handle:active{cursor:grabbing}
.toast{position:fixed;bottom:20px;right:20px;background:var(--accent);color:#fff;padding:8px 16px;border-radius:8px;font-size:0.8rem;z-index:100;opacity:0;transform:translateY(10px);transition:all 0.3s;pointer-events:none}
.toast.visible{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Layout</h1>
  <div class="stats">
    <span id="stat-sessions">sessions: 0</span>
    <span id="stat-tracked">tracked: 0s</span>
    <span id="stat-active">active: 0</span>
    <span id="stat-hidden">hidden: --</span>
  </div>
  <div>
    <button class="btn" id="btn-reset" title="Reset all tracking data">reset tracking</button>
    <button class="btn" id="btn-export" title="Export layout state">export</button>
    <button class="btn" id="btn-auto" title="Toggle auto-arrange">auto: on</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
'use strict';
const CFG = {
  debounceMs: 100,
  throttleMs: 200,
  pauseOnHidden: true,
  renderMode: 'diff',
  compactThreshold: 0.15,
  decayHalveUnseenMs: 600000,
  scoreWeights: { frequency: 0.4, duration: 0.35, recency: 0.25 },
  maxPanels: 12,
  gridBreakpoint: 768,
  sessionKey: 'aml_layout_v1',
  scoreKey: 'aml_scores_v1',
  overrideKey: 'aml_overrides_v1'
};
const META = {
  sessions: 0,
  totalTrackedMs: 0,
  hidden: false,
  autoArrange: true,
  debounceTimers: {},
  throttleTimers: {},
  observer: null,
  panels: [],
  panelMap: {},
  scores: null,
  overrides: null,
  domCache: {}
};
function debounce(key, fn, ms){
  if(META.debounceTimers[key]) clearTimeout(META.debounceTimers[key]);
  META.debounceTimers[key] = setTimeout(fn, ms || CFG.debounceMs);
}
function throttle(key, fn, ms){
  if(META.throttleTimers[key]) return;
  META.throttleTimers[key] = setTimeout(()=>{ META.throttleTimers[key]=null; }, ms || CFG.throttleMs);
  fn();
}
function safeLoad(key, fallback){
  try{
    const raw = localStorage.getItem(key);
    if(raw===null) return fallback;
    const parsed = JSON.parse(raw);
    if(parsed===null || typeof parsed!=='object') throw new Error('corrupt');
    return parsed;
  }catch(e){
    localStorage.removeItem(key);
    return fallback;
  }
}
function safeStore(key, val){
  try{ localStorage.setItem(key, JSON.stringify(val)); }catch(e){}
}
function now(){ return Date.now(); }
function computeScore(entry, t){
  const ageMs = t - entry.lastSeen;
  const ageMin = ageMs / 60000;
  let decay;
  if(ageMin > 10){
    decay = Math.exp(-ageMin / (20 * 2));
  }else{
    decay = Math.exp(-ageMin / 20);
  }
  const recencyComponent = decay;
  const durationComponent = Math.min(entry.totalDurationMs / 300000, 1);
  const frequencyComponent = Math.min(entry.viewCount / 50, 1);
  return (
    CFG.scoreWeights.frequency * frequencyComponent +
    CFG.scoreWeights.duration * durationComponent +
    CFG.scoreWeights.recency * recencyComponent
  );
}
function loadScores(){
  const raw = safeLoad(CFG.scoreKey, {});
  const t = now();
  const cleaned = {};
  for(const[id,entry] of Object.entries(raw)){
    try{
      if(typeof entry.viewCount!=='number') throw new Error('bad');
      if(typeof entry.totalDurationMs!=='number') throw new Error('bad');
      if(typeof entry.lastSeen!=='number') throw new Error('bad');
      cleaned[id] = entry;
    }catch(e){}
  }
  return cleaned;
}
function saveScores(){ safeStore(CFG.scoreKey, META.scores); }
function ensureScore(id){
  if(!META.scores[id]){
    META.scores[id] = { viewCount:0, totalDurationMs:0, lastSeen:now(), firstSeen:now() };
  }
  return META.scores[id];
}
function loadOverrides(){ return safeLoad(CFG.overrideKey, {}); }
function saveOverrides(){ safeStore(CFG.overrideKey, META.overrides); }
function computeRanks(){
  const t = now();
  const scored = [];
  for(const[id,entry] of Object.entries(META.scores)){
    const score = computeScore(entry, t);
    scored.push({ id, score, entry });
  }
  scored.sort((a,b)=>b.score - a.score);
  const rankMap = {};
  scored.forEach((s,i)=>{ rankMap[s.id] = i; });
  return { ranked: scored, rankMap, maxScore: scored.length>0 ? scored[0].score : 0 };
}
function panelTemplate(id, title, value, label, color, index){
  const override = META.overrides[id] || {};
  const locked = !!override.locked;
  const compact = false;
  return {
    id, title, value, label, color, index,
    locked, compact, pinnedPos: override.position || null
  };
}
const PANEL_DEFS = [
  { id:'cpu', title:'CPU Usage', value:'23%', label:'avg load', color:'#6c8cff' },
  { id:'mem', title:'Memory', value:'7.2 GB', label:'of 16 GB', color:'#ff9e64' },
  { id:'disk', title:'Disk I/O', value:'142 MB/s', label:'read / write', color:'#9d7cd8' },
  { id:'net', title:'Network', value:'3.8 Gbps', label:'total throughput', color:'#7dcfff' },
  { id:'req', title:'Requests', value:'2.4k/s', label:'avg rate', color:'#73daca' },
  { id:'err', title:'Errors', value:'0.12%', label:'error rate', color:'#f7768e' },
  { id:'lat', title:'Latency', value:'42ms', label:'p95', color:'#e0af68' },
  { id:'q', title:'Queue Depth', value:'18', label:'pending', color:'#bb9af7' },
  { id:'cache', title:'Cache Hit', value:'94.3%', label:'hit ratio', color:'#9ece6a' },
  { id:'conn', title:'Connections', value:'1.2k', label:'active', color:'#3d59a1' },
  { id:'uptime', title:'Uptime', value:'47d 3h', label:'since last restart', color:'#2ac3de' },
  { id:'cost', title:'Cost/hr', value:'$4.82', label:'estimated', color:'#ff007c' }
];
function buildPanels(){
  META.panels = PANEL_DEFS.map((d,i)=>panelTemplate(d.id,d.title,d.value,d.label,d.color,i));
  META.panelMap = {};
  META.panels.forEach(p=>{ META.panelMap[p.id]=p; });
}
function applyLayout(){
  if(!META.autoArrange) return;
  const { ranked, rankMap, maxScore } = computeRanks();
  const lockedPanels = META.panels.filter(p=>p.locked);
  const unlockedPanels = META.panels.filter(p=>!p.locked);
  unlockedPanels.sort((a,b)=>{
    const ra = rankMap[a.id]!==undefined ? rankMap[a.id] : 999;
    const rb = rankMap[b.id]!==undefined ? rankMap[b.id] : 999;
    return ra - rb;
  });
  const threshold = maxScore * CFG.compactThreshold;
  unlockedPanels.forEach(p=>{
    const score = META.scores[p.id] ? computeScore(META.scores[p.id], now()) : 0;
    p.compact = score < threshold && score > 0 && rankMap[p.id] > 3;
  });
  const ordered = [];
  lockedPanels.forEach(p=>{
    const pos = p.pinnedPos!==null ? p.pinnedPos : 0;
    ordered.push({ panel:p, pos });
  });
  ordered.sort((a,b)=>a.pos-b.pos);
  const lockedIds = new Set(lockedPanels.map(p=>p.id));
  const finalOrder = [];
  let li=0, ui=0;
  while(li<ordered.length || ui<unlockedPanels.length){
    if(li<ordered.length && ordered[li].pos<=finalOrder.length){
      finalOrder.push(ordered[li].panel); li++;
    }else if(ui<unlockedPanels.length){
      finalOrder.push(unlockedPanels[ui]); ui++;
    }else{
      finalOrder.push(ordered[li].panel); li++;
    }
  }
  META.panels = finalOrder;
  META.panelMap = {};
  META.panels.forEach(p=>{ META.panelMap[p.id]=p; });
}
function renderPanelDom(panel, el){
  if(!el){
    el = document.createElement('div');
    el.className = 'panel';
    el.setAttribute('data-panel-id', panel.id);
    el.innerHTML =
      '<div class="panel-score"></div>'+
      '<div class="panel-header">'+
        '<span class="panel-title"></span>'+
        '<div class="panel-controls">'+
          '<button class="panel-ctrl pin-ctrl" title="Lock position">📌</button>'+
          '<button class="panel-ctrl compact-ctrl" title="Toggle compact">⊟</button>'+
        '</div>'+
      '</div>'+
      '<div class="panel-body">'+
        '<div class="panel-value"></div>'+
        '<div class="panel-label"></div>'+
        '<div class="panel-chart"></div>'+
      '</div>';
    el.querySelector('.pin-ctrl').addEventListener('click',(e)=>{
      e.stopPropagation();
      toggleLock(panel.id);
    });
    el.querySelector('.compact-ctrl').addEventListener('click',(e)=>{
      e.stopPropagation();
      toggleCompactManual(panel.id);
    });
    el.addEventListener('click',()=>{ recordInteraction(panel.id); });
    META.domCache[panel.id] = el;
  }
  el.querySelector('.panel-title').textContent = panel.title;
  el.querySelector('.panel-value').textContent = panel.value;
  el.querySelector('.panel-label').textContent = panel.label;
  el.querySelector('.panel-score').textContent =
    META.scores[panel.id] ? (computeScore(META.scores[panel.id],now())*100).toFixed(0) : '0';
  el.classList.toggle('compact', panel.compact);
  el.classList.toggle('locked', panel.locked);
  el.querySelector('.pin-ctrl').classList.toggle('pinned', panel.locked);
  el.style.order = panel.compact ? '100' : '';
  el.style.borderLeftColor = panel.color || 'var(--panel-border)';
  el.style.borderLeftWidth = '3px';
  el.style.borderLeftStyle = 'solid';
  const chartEl = el.querySelector('.panel-chart');
  if(chartEl && !panel.compact){
    const bars = 8;
    let currentBars = chartEl.children.length;
    while(currentBars < bars){
      const bar = document.createElement('div');
      bar.className = 'chart-bar';
      chartEl.appendChild(bar);
      currentBars++;
    }
    while(currentBars > bars){
      chartEl.lastChild.remove();
      currentBars--;
    }
    for(let i=0;i<bars;i++){
      const h = 15 + Math.sin((now()/3000)+(i*0.7)+(panel.index||0))*15 + Math.random()*10;
      chartEl.children[i].style.height = Math.max(2,h)+'px';
    }
  }
  return el;
}
function renderDashboard(full){
  const container = document.getElementById('dashboard');
  if(full || CFG.renderMode==='full'){
    container.innerHTML = '';
    META.domCache = {};
    META.panels.forEach(p=>{
      const el = renderPanelDom(p, null);
      container.appendChild(el);
    });
  }else{
    const currentIds = new Set(META.panels.map(p=>p.id));
    for(const id of Object.keys(META.domCache)){
      if(!currentIds.has(id)){
        const el = META.domCache[id];
        if(el.parentNode) el.parentNode.removeChild(el);
        delete META.domCache[id];
      }
    }
    META.panels.forEach((p,i)=>{
      let el = META.domCache[p.id];
      if(!el){
        el = renderPanelDom(p, null);
        container.appendChild(el);
      }else{
        renderPanelDom(p, el);
      }
      if(el.parentNode !== container) container.appendChild(el);
    });
  }
  document.getElementById('stat-active').textContent = 'active: '+META.panels.filter(p=>!p.compact).length;
}
let compactManual = {};
function toggleLock(id){
  META.overrides[id] = META.overrides[id] || {};
  META.overrides[id].locked = !META.overrides[id].locked;
  META.panelMap[id].locked = META.overrides[id].locked;
  if(META.overrides[id].locked){
    const idx = META.panels.indexOf(META.panelMap[id]);
    META.overrides[id].position = idx;
    META.panelMap[id].pinnedPos = idx;
  }else{
    META.panelMap[id].pinnedPos = null;
  }
  saveOverrides();
  applyLayout();
  renderDashboard(false);
  toast(META.overrides[id].locked ? id+' locked' : id+' unlocked');
}
function toggleCompactManual(id){
  compactManual[id] = !compactManual[id];
  META.panelMap[id].compact = compactManual[id];
  renderDashboard(false);
}
function recordInteraction(id){ ensureScore(id).viewCount++; saveScores(); }
let visibilityTimers = {};
function startVisibilityTimer(id){
  if(visibilityTimers[id]) return;
  const entry = ensureScore(id);
  visibilityTimers[id] = { start: now(), entry };
}
function stopVisibilityTimer(id){
  const vt = visibilityTimers[id];
  if(!vt) return;
  const elapsed = now() - vt.start;
  vt.entry.totalDurationMs += elapsed;
  vt.entry.lastSeen = now();
  delete visibilityTimers[id];
  saveScores();
}
function setupObserver(){
  if(META.observer) META.observer.disconnect();
  META.observer = new IntersectionObserver((entries)=>{
    debounce('io',()=>{
      if(META.hidden && CFG.pauseOnHidden) return;
      entries.forEach(entry=>{
        const id = entry.target.getAttribute('data-panel-id');
        if(!id) return;
        if(entry.isIntersecting && entry.intersectionRatio > 0.3){
          startVisibilityTimer(id);
        }else{
          stopVisibilityTimer(id);
        }
      });
    });
  },{ threshold:[0,0.3,0.6,0.9] });
  document.querySelectorAll('.panel').forEach(el=>META.observer.observe(el));
}
function refreshObserver(){
  if(META.observer) META.observer.disconnect();
  META.observer = new IntersectionObserver((entries)=>{
    debounce('io',()=>{
      if(META.hidden && CFG.pauseOnHidden) return;
      entries.forEach(entry=>{
        const id = entry.target.getAttribute('data-panel-id');
        if(!id) return;
        if(entry.isIntersecting && entry.intersectionRatio > 0.3){
          startVisibilityTimer(id);
        }else{
          stopVisibilityTimer(id);
        }
      });
    });
  },{ threshold:[0,0.3,0.6,0.9] });
  document.querySelectorAll('.panel').forEach(el=>META.observer.observe(el));
}
function onVisibilityChange(){
  META.hidden = document.hidden;
  document.getElementById('stat-hidden').textContent = 'hidden: '+(META.hidden?'yes':'no');
  if(META.hidden && CFG.pauseOnHidden){
    for(const id of Object.keys(visibilityTimers)){ stopVisibilityTimer(id); }
  }
}
function onResize(){
  debounce('resize',()=>{
    const w = window.innerWidth;
    const gridMin = w <= CFG.gridBreakpoint ? '1fr' : 'var(--grid-min)';
    document.querySelector('.dashboard').style.gridTemplateColumns =
      w <= CFG.gridBreakpoint ? '1fr' : 'repeat(auto-fill,minmax(var(--grid-min),1fr))';
  });
}
function toast(msg){
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('visible');
  setTimeout(()=>el.classList.remove('visible'), 2000);
}
function init(){
  META.scores = loadScores();
  META.overrides = loadOverrides();
  META.sessions = safeLoad(CFG.sessionKey+'_sessions', 0) + 1;
  safeStore(CFG.sessionKey+'_sessions', META.sessions);
  document.getElementById('stat-sessions').textContent = 'sessions: '+META.sessions;
  buildPanels();
  for(const[id,ov] of Object.entries(META.overrides)){
    if(META.panelMap[id]){
      META.panelMap[id].locked = !!ov.locked;
      META.panelMap[id].pinnedPos = ov.position!==undefined ? ov.position : null;
    }
  }
  applyLayout();
  renderDashboard(true);
  setupObserver();
  document.addEventListener('visibilitychange', onVisibilityChange);
  window.addEventListener('resize', ()=>debounce('resize', onResize));
  document.getElementById('btn-reset').addEventListener('click',()=>{
    META.scores = {};
    saveScores();
    META.overrides = {};
    saveOverrides();
    compactManual = {};
    META.panels.forEach(p=>{ p.locked=false; p.compact=false; p.pinnedPos=null; });
    applyLayout();
    renderDashboard(true);
    refreshObserver();
    toast('tracking reset');
  });
  document.getElementById('btn-export').addEventListener('click',()=>{
    const state = { scores:META.scores, overrides:META.overrides, sessions:META.sessions, exportedAt:now() };
    const blob = new Blob([JSON.stringify(state,null,2)],{type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'aml-layout-'+new Date().toISOString().slice(0,10)+'.json';
    a.click();
    toast('exported');
  });
  const btnAuto = document.getElementById('btn-auto');
  btnAuto.addEventListener('click',()=>{
    META.autoArrange = !META.autoArrange;
    btnAuto.textContent = 'auto: '+(META.autoArrange?'on':'off');
    btnAuto.classList.toggle('active', META.autoArrange);
    if(META.autoArrange){ applyLayout(); renderDashboard(true); refreshObserver(); }
    toast('auto-arrange '+(META.autoArrange?'on':'off'));
  });
  btnAuto.classList.add('active');
  setInterval(()=>{
    if(!META.hidden || !CFG.pauseOnHidden){
      throttle('recalc',()=>{
        if(META.autoArrange) applyLayout();
        renderDashboard(false);
      });
    }
    const trackedSec = Math.round(Object.values(META.scores).reduce((s,e)=>s+e.totalDurationMs,0)/1000);
    document.getElementById('stat-tracked').textContent = 'tracked: '+trackedSec+'s';
  }, 5000);
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
else init();
})();
</script>
</body>
</html>