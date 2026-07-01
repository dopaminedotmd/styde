<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-raised: #222639;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #888ca0;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --success: #4ade80;
  --warn: #fbbf24;
  --danger: #f87171;
  --gap: 12px;
  --radius: 12px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-wrap: wrap;
  min-height: 52px;
}
.toolbar-title {
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--text);
  white-space: nowrap;
}
.toolbar-spacer {flex:1}
.toolbar-btn {
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface-raised);
  color: var(--text-dim);
  font-size: 0.82rem;
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
  font-family: inherit;
}
.toolbar-btn:hover,.toolbar-btn:focus-visible {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 3px var(--accent-glow);
}
.toolbar-btn:active{transform:scale(0.97)}
.toolbar-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.toolbar-btn .indicator {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
}
.indicator-live{background:var(--success);animation:pulse 2s infinite}
.indicator-paused{background:var(--warn)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.dashboard {
  display: grid;
  gap: var(--gap);
  padding: 16px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-rows: minmax(180px, auto);
  grid-auto-flow: dense;
  max-width: 1600px;
  margin: 0 auto;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: all var(--transition);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  min-height: 160px;
  container-type: inline-size;
}
.panel:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-glow);
}
.panel.rank-high {
  grid-column: span 2;
  grid-row: span 2;
  min-height: 340px;
}
.panel.rank-medium {
  grid-column: span 1;
  grid-row: span 1;
}
.panel.rank-low {
  grid-column: span 1;
  grid-row: span 1;
}
.panel.rank-compact {
  grid-column: span 1;
  grid-row: span 1;
  min-height: 100px;
  max-height: 140px;
  opacity: 0.82;
}
.panel.rank-compact .panel-body {display:none}
.panel.rank-compact .panel-preview {display:flex}
.panel.locked {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent-glow);
}
.panel.dragging {
  opacity: 0.7;
  transform: scale(0.96);
  z-index: 50;
}
.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  cursor: grab;
  user-select: none;
  min-height: 44px;
  background: var(--surface);
}
.panel-header:active{cursor:grabbing}
.panel-icon{font-size:1.1rem;flex-shrink:0}
.panel-title{font-weight:600;font-size:0.88rem;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-score{font-size:0.7rem;color:var(--text-dim);flex-shrink:0;font-variant-numeric:tabular-nums}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-btn {
  width: 28px;
  height: 28px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  color: var(--text-dim);
  cursor: pointer;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}
.panel-btn:hover,.panel-btn:focus-visible {
  background: var(--surface-raised);
  color: var(--text);
  border-color: var(--border);
  outline: none;
}
.panel-btn.lock-btn.locked {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.panel-body {
  flex: 1;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: auto;
}
.panel-preview {
  display: none;
  flex: 1;
  padding: 12px 14px;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
  color: var(--text-dim);
}
.panel-preview-spark {
  flex: 1;
  height: 32px;
  background: linear-gradient(90deg, var(--surface-raised) 0%, var(--accent) 50%, var(--surface-raised) 100%);
  border-radius: 4px;
  opacity: 0.5;
}
.panel-preview-val {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text);
  flex-shrink: 0;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
}
.metric-label{color:var(--text-dim)}
.metric-value{font-weight:600;font-variant-numeric:tabular-nums}
.metric-bar {
  height: 6px;
  border-radius: 3px;
  background: var(--surface-raised);
  overflow: hidden;
  margin-top: 4px;
}
.metric-bar-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--accent);
  transition: width 0.6s ease;
}
.chart-mini {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 60px;
  padding: 4px 0;
}
.chart-bar {
  flex: 1;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
  opacity: 0.7;
  min-height: 4px;
  transition: height 0.5s ease;
}
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface-raised);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 0.82rem;
  color: var(--text);
  z-index: 200;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s ease;
  pointer-events: none;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.toast.show{opacity:1;transform:translateY(0)}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border: 0;
}
@media (max-width: 640px) {
  .dashboard {
    grid-template-columns: 1fr;
    padding: 8px;
    gap: 8px;
  }
  .panel.rank-high {
    grid-column: span 1;
    grid-row: span 2;
    min-height: 240px;
  }
  .toolbar {
    padding: 8px 12px;
    gap: 6px;
  }
  .toolbar-title{font-size:0.95rem}
  .toolbar-btn{padding:5px 10px;font-size:0.75rem}
}
@media (prefers-reduced-motion: reduce) {
  *,*::before,*::after{animation-duration:0.01ms!important;transition-duration:0.01ms!important}
}
</style>
</head>
<body>
<header class="toolbar" role="toolbar" aria-label="Dashboard controls">
  <span class="toolbar-title" aria-live="polite">Adaptive Dashboard</span>
  <div class="toolbar-spacer"></div>
  <button class="toolbar-btn" id="btn-reset" aria-label="Reset all layout preferences">
    <span aria-hidden="true">↺</span> Reset
  </button>
  <button class="toolbar-btn" id="btn-export" aria-label="Export layout configuration">
    <span aria-hidden="true">⇧</span> Export
  </button>
  <button class="toolbar-btn active" id="btn-live" aria-label="Toggle live tracking. Currently active" aria-pressed="true">
    <span class="indicator indicator-live" aria-hidden="true"></span> Live
  </button>
  <span class="visually-hidden" id="status-live" aria-live="polite">Live tracking is active</span>
</header>
<main class="dashboard" id="dashboard" role="region" aria-label="Adaptive metric panels grid">
</main>
<div class="toast" id="toast" role="status" aria-live="polite" aria-atomic="true"></div>
<script>
(function(){
'use strict';
const CACHE_KEY = 'adaptive_dashboard_v2';
const DEBOUNCE_MS = 100;
const THROTTLE_MS = 200;
const DECAY_RESET_WINDOW = 10 * 60 * 1000;
const DECAY_HALF_FACTOR = 0.5;
const COMPACT_THRESHOLD = 0.3;
const HIGH_THRESHOLD = 0.75;
const INTERVAL_MS = 2000;
const RANK_WEIGHTS = {frequency:0.4,duration:0.4,recency:0.2};
let state = {
  panels: [],
  live: true,
  cache: {},
  lastVisibilityChange: Date.now()
};
let intervalId = null;
let observer = null;
let resizeTimer = null;
const $dashboard = document.getElementById('dashboard');
const $toast = document.getElementById('toast');
const $btnLive = document.getElementById('btn-live');
const $btnReset = document.getElementById('btn-reset');
const $btnExport = document.getElementById('btn-export');
const $statusLive = document.getElementById('status-live');
const defaultPanels = [
  {id:'cpu',title:'CPU Usage',icon:'⚙',category:'system',metric:'cpu_pct',unit:'%',min:0,max:100,value:42,trend:[35,40,38,45,42,48,42,39]},
  {id:'mem',title:'Memory',icon:'🧠',category:'system',metric:'mem_pct',unit:'%',min:0,max:100,value:67,trend:[60,62,65,68,67,70,67,64]},
  {id:'disk',title:'Disk I/O',icon:'💾',category:'system',metric:'disk_mbps',unit:'MB/s',min:0,max:500,value:128,trend:[80,120,90,150,128,140,128,110]},
  {id:'net',title:'Network',icon:'🌐',category:'system',metric:'net_mbps',unit:'Mbps',min:0,max:1000,value:342,trend:[200,280,310,350,342,380,342,300]},
  {id:'req',title:'Requests/s',icon:'📨',category:'app',metric:'req_ps',unit:'rps',min:0,max:5000,value:1240,trend:[800,950,1100,1300,1240,1400,1240,1000]},
  {id:'err',title:'Error Rate',icon:'⚠',category:'app',metric:'err_pct',unit:'%',min:0,max:100,value:1.2,trend:[2.1,1.8,1.5,1.3,1.2,1.4,1.2,1.0]},
  {id:'lat',title:'Latency p95',icon:'⏱',category:'app',metric:'lat_ms',unit:'ms',min:0,max:1000,value:187,trend:[220,200,195,190,187,192,187,180]},
  {id:'cache',title:'Cache Hit Rate',icon:'🎯',category:'infra',metric:'cache_pct',unit:'%',min:0,max:100,value:94.3,trend:[90,91,92,93,94.3,95,94.3,92]},
  {id:'queue',title:'Queue Depth',icon:'📋',category:'infra',metric:'queue_n',unit:'items',min:0,max:200,value:34,trend:[50,45,40,38,34,36,34,30]},
  {id:'users',title:'Active Users',icon:'👥',category:'business',metric:'users_n',unit:'users',min:0,max:5000,value:892,trend:[700,750,820,880,892,910,892,850]},
  {id:'rev',title:'Revenue/min',icon:'💰',category:'business',metric:'rev_eur',unit:'EUR',min:0,max:1000,value:423,trend:[300,350,380,410,423,440,423,390]},
  {id:'conv',title:'Conversion',icon:'✨',category:'business',metric:'conv_pct',unit:'%',min:0,max:100,value:3.8,trend:[3.2,3.5,3.6,3.7,3.8,3.9,3.8,3.6]}
];
function loadState() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      if (saved && saved.panels && Array.isArray(saved.panels)) {
        state.panels = saved.panels;
        state.cache = saved.cache || {};
        const now = Date.now();
        const unseenCutoff = now - DECAY_RESET_WINDOW;
        for (const pid in state.cache) {
          if ((state.cache[pid].lastSeen || 0) < unseenCutoff) {
            state.cache[pid].decayRate = (state.cache[pid].decayRate || 1) * DECAY_HALF_FACTOR;
          }
        }
        const savedIds = new Set(state.panels.map(p=>p.id));
        for (const def of defaultPanels) {
          if (!savedIds.has(def.id)) {
            state.panels.push({...def, locked:false,rankOverride:null});
          }
        }
        return;
      }
    }
  } catch(e){}
  state.panels = defaultPanels.map(d=>({...d,locked:false,rankOverride:null}));
  state.cache = {};
}
function saveState() {
  try {
    const out = {panels:state.panels,cache:state.cache,ts:Date.now()};
    localStorage.setItem(CACHE_KEY, JSON.stringify(out));
  } catch(e){}
}
function computeScore(panel) {
  const c = state.cache[panel.id] || {frequency:0,duration:0,lastInteraction:0,decayRate:1};
  const now = Date.now();
  const age = Math.max(0, now - (c.lastInteraction || now));
  const ageHours = age / (1000*60*60);
  const decay = Math.exp(-0.05 * ageHours * (c.decayRate || 1));
  const freqScore = Math.min(1, (c.frequency||0) / 20);
  const durScore = Math.min(1, (c.duration||0) / 300000);
  const recencyScore = Math.max(0, decay);
  return (freqScore * RANK_WEIGHTS.frequency + durScore * RANK_WEIGHTS.duration + recencyScore * RANK_WEIGHTS.recency);
}
function computeRanks() {
  const scored = state.panels.map(p=>({...p,score:computeScore(p)}));
  scored.sort((a,b)=>b.score - a.score);
  const max = Math.max(...scored.map(s=>s.score), 0.001);
  scored.forEach((p,i)=>{
    const norm = p.score / max;
    if (p.locked || p.rankOverride !== null) {
      p.rank = p.rankOverride || (norm >= HIGH_THRESHOLD ? 'high' : norm >= COMPACT_THRESHOLD ? 'medium' : 'low');
    } else if (norm >= HIGH_THRESHOLD) {
      p.rank = 'high';
    } else if (norm >= COMPACT_THRESHOLD) {
      p.rank = 'medium';
    } else if (norm > 0.05) {
      p.rank = 'low';
    } else {
      p.rank = 'compact';
    }
    p.sortOrder = p.locked ? 0 : i;
  });
  scored.sort((a,b)=>a.sortOrder - b.sortOrder);
  return scored;
}
function trackEvent(panelId, type, duration) {
  if (!state.live) return;
  if (!state.cache[panelId]) {
    state.cache[panelId] = {frequency:0,duration:0,lastInteraction:0,decayRate:1};
  }
  const c = state.cache[panelId];
  const now = Date.now();
  if (now - (c.lastSeen || 0) > DECAY_RESET_WINDOW) {
    c.decayRate = Math.max(0.1, (c.decayRate || 1) * DECAY_HALF_FACTOR);
  }
  c.lastSeen = now;
  if (type === 'view') c.frequency = (c.frequency||0) + 1;
  if (type === 'interact') { c.frequency = (c.frequency||0) + 1; c.lastInteraction = now; }
  if (duration && type === 'view') c.duration = (c.duration||0) + duration;
}
let viewStart = {};
let interactTimers = {};
function setupIntersectionObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      const pid = e.target.dataset.panelId;
      if (!pid) return;
      if (e.isIntersecting) {
        viewStart[pid] = Date.now();
      } else {
        if (viewStart[pid]) {
          const dur = Date.now() - viewStart[pid];
          trackEvent(pid, 'view', dur);
          delete viewStart[pid];
        }
      }
    });
  },{threshold:0.3});
  document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
}
function debounce(fn, ms) {
  let t;
  return function(...args){clearTimeout(t);t=setTimeout(()=>fn.apply(this,args),ms)};
}
const debouncedRender = debounce(renderDashboard, DEBOUNCE_MS);
const debouncedResize = debounce(()=>{setupIntersectionObserver()}, DEBOUNCE_MS);
function patchPanelDOM(panelEl, panelData) {
  const titleEl = panelEl.querySelector('.panel-title');
  if (titleEl && titleEl.textContent !== panelData.title) titleEl.textContent = panelData.title;
  const scoreEl = panelEl.querySelector('.panel-score');
  const newScore = computeScore(panelData).toFixed(1);
  if (scoreEl && scoreEl.textContent !== newScore) scoreEl.textContent = newScore;
  const lockBtn = panelEl.querySelector('.lock-btn');
  if (lockBtn) {
    const isLocked = panelData.locked;
    if (lockBtn.classList.contains('locked') !== isLocked) {
      lockBtn.classList.toggle('locked', isLocked);
      lockBtn.setAttribute('aria-pressed', String(isLocked));
      lockBtn.setAttribute('aria-label', (isLocked?'Unlock':'Lock') + ' ' + panelData.title);
    }
  }
  const rankClasses = ['rank-high','rank-medium','rank-low','rank-compact'];
  rankClasses.forEach(cls=>{
    if (cls === 'rank-'+panelData.rank) {
      if (!panelEl.classList.contains(cls)) panelEl.classList.add(cls);
    } else {
      panelEl.classList.remove(cls);
    }
  });
  if (panelData.rank === 'compact') {
    const previewVal = panelEl.querySelector('.panel-preview-val');
    if (previewVal) previewVal.textContent = panelData.value + (panelData.unit||'');
  }
}
function renderDashboard() {
  const ranked = computeRanks();
  const existingEls = new Map();
  $dashboard.querySelectorAll('.panel').forEach(el=>{
    const pid = el.dataset.panelId;
    if (pid) existingEls.set(pid, el);
  });
  const usedIds = new Set();
  ranked.forEach(panel=>{
    usedIds.add(panel.id);
    let el = existingEls.get(panel.id);
    if (!el) {
      el = buildPanelElement(panel);
      $dashboard.appendChild(el);
    } else {
      patchPanelDOM(el, panel);
    }
    if (panel.rank === 'high') {
      el.style.gridColumn = 'span 2';
      el.style.gridRow = 'span 2';
    } else {
      el.style.gridColumn = '';
      el.style.gridRow = '';
    }
    el.style.order = panel.sortOrder;
  });
  existingEls.forEach((el,pid)=>{
    if (!usedIds.has(pid)) el.remove();
  });
  setupIntersectionObserver();
}
function buildPanelElement(panel) {
  const el = document.createElement('article');
  el.className = 'panel rank-' + (panel.rank||'medium');
  el.dataset.panelId = panel.id;
  el.setAttribute('role','region');
  el.setAttribute('aria-label', panel.title + ' panel. Score: ' + computeScore(panel).toFixed(1));
  el.setAttribute('tabindex','-1');
  el.innerHTML = buildPanelHTML(panel);
  el.querySelector('.lock-btn')?.addEventListener('click',(e)=>{
    e.stopPropagation();
    panel.locked = !panel.locked;
    el.classList.toggle('locked',panel.locked);
    trackEvent(panel.id,'interact');
    saveState();
    debouncedRender();
    showToast(panel.locked ? panel.title+' locked' : panel.title+' unlocked');
  });
  el.querySelector('.collapse-btn')?.addEventListener('click',(e)=>{
    e.stopPropagation();
    if (panel.rankOverride === 'compact') {
      panel.rankOverride = null;
    } else {
      panel.rankOverride = 'compact';
    }
    trackEvent(panel.id,'interact');
    saveState();
    debouncedRender();
    showToast(panel.title + (panel.rankOverride==='compact' ? ' collapsed' : ' expanded'));
  });
  el.addEventListener('click',()=>trackEvent(panel.id,'interact'));
  el.addEventListener('keydown',(e)=>{
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      trackEvent(panel.id,'interact');
      showToast(panel.title+' focused. Score: '+computeScore(panel).toFixed(1));
    }
  });
  return el;
}
function buildPanelHTML(panel) {
  const score = computeScore(panel).toFixed(1);
  const isCompact = panel.rank === 'compact' || panel.rankOverride === 'compact';
  let html = '<div class="panel-header" aria-grabbed="false">';
  html += '<span class="panel-icon" aria-hidden="true">'+escHtml(panel.icon||'')+'</span>';
  html += '<span class="panel-title">'+escHtml(panel.title)+'</span>';
  html += '<span class="panel-score" aria-label="Attention score">'+score+'</span>';
  html += '<div class="panel-actions">';
  html += '<button class="panel-btn collapse-btn" aria-label="'+(isCompact?'Expand':'Collapse')+' '+escHtml(panel.title)+'">'+(isCompact?'⊞':'⊟')+'</button>';
  html += '<button class="panel-btn lock-btn'+(panel.locked?' locked':'')+'" aria-pressed="'+panel.locked+'" aria-label="'+(panel.locked?'Unlock':'Lock')+' '+escHtml(panel.title)+'">'+(panel.locked?'🔒':'🔓')+'</button>';
  html += '</div></div>';
  if (!isCompact) {
    html += '<div class="panel-body">';
    html += '<div class="metric-row"><span class="metric-label">Current</span><span class="metric-value">'+panel.value+(panel.unit||'')+'</span></div>';
    html += '<div class="metric-bar"><div class="metric-bar-fill" style="width:'+Math.min(100,((panel.value-panel.min)/(panel.max-panel.min))*100)+'%" role="progressbar" aria-valuenow="'+panel.value+'" aria-valuemin="'+panel.min+'" aria-valuemax="'+panel.max+'" aria-label="'+panel.title+' gauge"></div></div>';
    if (panel.trend && panel.trend.length) {
      html += '<div class="chart-mini" aria-label="Trend chart for '+escHtml(panel.title)+'">';
      const tmax = Math.max(...panel.trend,0.001);
      panel.trend.forEach(v=>{
        const h = Math.max(4,(v/tmax)*100);
        html += '<div class="chart-bar" style="height:'+h+'%" aria-hidden="true"></div>';
      });
      html += '</div>';
    }
    html += '<div class="metric-row"><span class="metric-label">Category</span><span class="metric-value">'+escHtml(panel.category||'')+'</span></div>';
    html += '</div>';
  }
  html += '<div class="panel-preview">';
  html += '<div class="panel-preview-spark" aria-hidden="true"></div>';
  html += '<span class="panel-preview-val">'+panel.value+(panel.unit||'')+'</span>';
  html += '</div>';
  return html;
}
function escHtml(s) {
  const map = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'};
  return String(s).replace(/[&<>"']/g,c=>map[c]||c);
}
function showToast(msg, duration) {
  duration = duration || 1800;
  $toast.textContent = msg;
  $toast.classList.add('show');
  clearTimeout($toast._timeout);
  $toast._timeout = setTimeout(()=>$toast.classList.remove('show'),duration);
}
function simulationTick() {
  if (!state.live) return;
  state.panels.forEach(p=>{
    const delta = (Math.random()-0.5) * (p.max-p.min) * 0.08;
    p.value = Math.round(Math.max(p.min,Math.min(p.max,p.value+delta))*10)/10;
    if (p.trend) {
      p.trend.push(p.value);
      if (p.trend.length > 16) p.trend.shift();
    }
  });
  debouncedRender();
}
function startInterval() {
  stopInterval();
  intervalId = setInterval(simulationTick, INTERVAL_MS);
}
function stopInterval() {
  if (intervalId) {clearInterval(intervalId);intervalId=null;}
}
function handleVisibility() {
  state.lastVisibilityChange = Date.now();
  if (document.hidden) {
    stopInterval();
    $btnLive.querySelector('.indicator').classList.remove('indicator-live');
    $btnLive.querySelector('.indicator').classList.add('indicator-paused');
    $statusLive.textContent = 'Live tracking paused — tab hidden';
  } else if (state.live) {
    startInterval();
    $btnLive.querySelector('.indicator').classList.add('indicator-live');
    $btnLive.querySelector('.indicator').classList.remove('indicator-paused');
    $statusLive.textContent = 'Live tracking is active';
  }
}
function toggleLive() {
  state.live = !state.live;
  $btnLive.classList.toggle('active',state.live);
  $btnLive.setAttribute('aria-pressed',String(state.live));
  if (state.live && !document.hidden) {
    startInterval();
    $btnLive.querySelector('.indicator').classList.add('indicator-live');
    $btnLive.querySelector('.indicator').classList.remove('indicator-paused');
    $statusLive.textContent = 'Live tracking is active';
  } else {
    stopInterval();
    $btnLive.querySelector('.indicator').classList.remove('indicator-live');
    $btnLive.querySelector('.indicator').classList.add('indicator-paused');
    $statusLive.textContent = 'Live tracking is paused';
  }
  showToast(state.live ? 'Live tracking resumed' : 'Live tracking paused');
}
function resetLayout() {
  state.panels = defaultPanels.map(d=>({...d,locked:false,rankOverride:null}));
  state.cache = {};
  saveState();
  renderDashboard();
  showToast('Layout reset to defaults');
}
function exportLayout() {
  const ranked = computeRanks();
  const data = {panels:ranked.map(p=>({id:p.id,title:p.title,score:computeScore(p).toFixed(2),rank:p.rank,value:p.value,locked:p.locked})),cache:state.cache,exported:new Date().toISOString()};
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'adaptive-layout-export.json';
  a.click();
  URL.revokeObjectURL(url);
  showToast('Layout exported');
}
function init() {
  loadState();
  renderDashboard();
  startInterval();
  window.addEventListener('resize', debouncedResize, {passive:true});
  document.addEventListener('visibilitychange', handleVisibility);
  $btnLive.addEventListener('click', toggleLive);
  $btnReset.addEventListener('click', resetLayout);
  $btnExport.addEventListener('click', exportLayout);
  let dragEl = null;
  let dragStartX = 0, dragStartY = 0;
  $dashboard.addEventListener('dragstart',(e)=>{
    const panel = e.target.closest('.panel');
    if (!panel) return;
    dragEl = panel;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.dataset.panelId);
  });
  $dashboard.addEventListener('dragend',(e)=>{
    if (dragEl) dragEl.classList.remove('dragging');
    dragEl = null;
  });
  $dashboard.addEventListener('dragover',(e)=>{e.preventDefault();e.dataTransfer.dropEffect='move'});
  $dashboard.addEventListener('drop',(e)=>{
    e.preventDefault();
    if (!dragEl) return;
    const target = e.target.closest('.panel');
    if (!target || target === dragEl) return;
    const srcId = dragEl.dataset.panelId;
    const dstId = target.dataset.panelId;
    const srcIdx = state.panels.findIndex(p=>p.id===srcId);
    const dstIdx = state.panels.findIndex(p=>p.id===dstId);
    if (srcIdx>=0 && dstIdx>=0) {
      const src = state.panels[srcIdx];
      src.locked = true;
      src.rankOverride = 'high';
      state.panels.splice(srcIdx,1);
      state.panels.splice(dstIdx,0,src);
      saveState();
      renderDashboard();
      showToast('Panel reordered and locked');
    }
    dragEl = null;
  });
  document.addEventListener('keydown',(e)=>{
    if (e.key === 'Escape') {
      state.panels.forEach(p=>{p.locked=false;p.rankOverride=null});
      saveState();
      renderDashboard();
      showToast('All locks and overrides cleared');
    }
  });
}
init();
})();
</script>
</body>
</html>