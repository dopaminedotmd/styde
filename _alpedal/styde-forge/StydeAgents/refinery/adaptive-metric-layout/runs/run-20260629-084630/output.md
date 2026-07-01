fileschanged:
  - dashboard.html (new): single-file adaptive dashboard
fixes:
  - Built complete adaptive layout engine from scratch
  - Implemented attention scoring: frequency × duration × recency
  - Added IntersectionObserver-based view tracking
  - Added click and collapse/expand event tracking
  - CSS Grid auto-arrange by attention rank
  - Compact/miniature mode for low-score panels
  - Manual lock toggle with localStorage override priority
  - localStorage persistence across sessions
  - 6 sample metric panels with sparklines
  - Rescore timer every 30s plus on-interaction recalc
categories: feature, new-file
DIFF:
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117; --panel-bg: #1a1d27; --border: #2a2d3a;
  --text: #e1e4ed; --text-dim: #8b8fa3; --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15); --danger: #ff5c5c;
  --success: #34d399; --warning: #fbbf24; --radius: 10px;
}
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100vh; padding: 16px;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; flex-wrap: wrap; gap: 8px;
}
h1 { font-size: 1.3rem; font-weight: 600; letter-spacing: -0.01em; }
.controls { display: flex; gap: 8px; flex-wrap: wrap; }
.controls button, .controls select {
  background: var(--panel-bg); border: 1px solid var(--border);
  color: var(--text); padding: 6px 14px; border-radius: 6px;
  cursor: pointer; font-size: 0.82rem; transition: all 0.15s;
}
.controls button:hover { border-color: var(--accent); background: var(--accent-glow); }
.controls button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.grid {
  display: grid; gap: 12px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-rows: minmax(160px, auto);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.grid.arrange-by-rank {
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
}
.panel {
  background: var(--panel-bg); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 14px 16px;
  position: relative; transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default; display: flex; flex-direction: column;
  min-height: 140px; overflow: hidden;
}
.panel:hover { border-color: #3a3e50; }
.panel.dominant { grid-column: span 2; grid-row: span 2; min-height: 300px; }
.panel.normal { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; min-height: 80px; padding: 8px 12px; }
.panel.compact .panel-body { display: none; }
.panel.compact .sparkline-wrap { display: none; }
.panel.compact .panel-score { font-size: 0.7rem; }
.panel.collapsed { min-height: 44px; padding: 6px 12px; }
.panel.collapsed .panel-body, .panel.collapsed .sparkline-wrap,
.panel.collapsed .panel-actions, .panel.collapsed .panel-score { display: none; }
.panel.locked { border-color: var(--warning); box-shadow: 0 0 0 1px var(--warning); }
.panel.locked::after {
  content: 'LOCKED'; position: absolute; top: 6px; right: 40px;
  font-size: 0.6rem; color: var(--warning); font-weight: 700;
  letter-spacing: 0.08em; opacity: 0.8;
}
.panel-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 6px; gap: 8px;
}
.panel-title { font-size: 0.88rem; font-weight: 600; color: var(--text); }
.panel-value { font-size: 1.4rem; font-weight: 700; margin: 4px 0; }
.panel-subtitle { font-size: 0.72rem; color: var(--text-dim); }
.panel-body { flex: 1; }
.panel-actions {
  display: flex; gap: 4px; position: absolute; top: 8px; right: 8px;
  opacity: 0; transition: opacity 0.15s;
}
.panel:hover .panel-actions { opacity: 1; }
.panel-actions button {
  background: transparent; border: 1px solid transparent;
  color: var(--text-dim); cursor: pointer; padding: 3px 6px;
  border-radius: 4px; font-size: 0.7rem; transition: all 0.12s;
}
.panel-actions button:hover { border-color: var(--border); color: var(--text); }
.panel-actions button.lock-btn.locked { color: var(--warning); }
.sparkline-wrap { height: 36px; margin-top: 6px; }
.sparkline-wrap svg { width: 100%; height: 100%; }
.panel-score {
  font-size: 0.68rem; color: var(--text-dim); margin-top: auto;
  padding-top: 6px; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between;
}
.more-section {
  margin-top: 12px; padding: 10px 16px;
  background: var(--panel-bg); border: 1px dashed var(--border);
  border-radius: var(--radius); text-align: center;
  color: var(--text-dim); font-size: 0.82rem; cursor: pointer;
  transition: all 0.15s;
}
.more-section:hover { border-color: var(--accent); color: var(--text); }
.more-panels { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.more-panels .mini { 
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 6px 10px; font-size: 0.72rem;
  cursor: pointer; transition: all 0.15s;
}
.more-panels .mini:hover { border-color: var(--accent); }
.drag-handle {
  cursor: grab; color: var(--text-dim); font-size: 0.8rem;
  padding: 2px 4px; user-select: none;
}
.drag-handle:active { cursor: grabbing; }
.toast {
  position: fixed; bottom: 20px; right: 20px;
  background: var(--accent); color: #fff; padding: 10px 18px;
  border-radius: 8px; font-size: 0.82rem; z-index: 999;
  opacity: 0; transform: translateY(10px); pointer-events: none;
  transition: all 0.25s;
}
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<header>
  <div>
    <h1>Adaptive Metric Dashboard</h1>
    <span style="font-size:0.72rem;color:var(--text-dim)">Layout auto-adapts to your behavior</span>
  </div>
  <div class="controls">
    <button id="btn-reset" title="Reset all tracking data">Reset Data</button>
    <button id="btn-force-reflow" title="Force immediate re-arrange">Reflow Now</button>
    <select id="sel-mode">
      <option value="auto">Auto Arrange</option>
      <option value="manual">Manual (drag)</option>
      <option value="score-sort">Sort by Score</option>
    </select>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="more-section" id="more-section" style="display:none">
  Collapsed panels
  <div class="more-panels" id="more-panels"></div>
</div>
<div class="toast" id="toast"></div>
<script>
(function(){
const STORAGE_KEY = 'adaptive_dashboard_v1';
const RESCORE_INTERVAL = 30000;
const DECAY_HALF_LIFE = 3600000;
const DOMINANCE_THRESHOLD = 0.65;
const COMPACT_THRESHOLD = 0.20;
const COLLAPSE_THRESHOLD = 0.08;
function generateSparklinePath(n, min, max) {
  const pts = Array.from({length: n}, () => Math.random() * (max-min) + min);
  const w = 100, h = 36, pad = 2;
  const xs = pts.map((_,i) => pad + (i/(n-1))*(w-2*pad));
  const ys = pts.map(v => h - pad - ((v-min)/(max-min))*(h-2*pad));
  let d = `M${xs[0]},${ys[0]}`;
  for(let i=1;i<xs.length;i++) d += ` L${xs[i]},${ys[i]}`;
  return d;
}
const PANEL_DEFS = [
  {id:'revenue', title:'Revenue', value:'$48.2K', sub:'+12.3% vs last month', trend:'up', color:'var(--success)',
   min:10000,max:60000},
  {id:'users', title:'Active Users', value:'3,847', sub:'+8.1% this week', trend:'up', color:'var(--accent)',
   min:2000,max:5000},
  {id:'latency', title:'API Latency', value:'142ms', sub:'-5% improvement', trend:'down', color:'var(--warning)',
   min:80,max:250},
  {id:'errors', title:'Error Rate', value:'0.34%', sub:'+0.02% since deploy', trend:'up', color:'var(--danger)',
   min:0.1,max:2.0},
  {id:'throughput', title:'Throughput', value:'12.8K/s', sub:'Steady under load', trend:'flat', color:'var(--accent)',
   min:5000,max:20000},
  {id:'sessions', title:'Sessions', value:'21.4K', sub:'Weekend peak incoming', trend:'up', color:'var(--success)',
   min:10000,max:30000},
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw) return JSON.parse(raw);
  } catch(e) {}
  return { panels: {}, order: PANEL_DEFS.map(p=>p.id), overrides: {} };
}
function saveState(state) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
function now() { return Date.now(); }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function decayWeight(ts, refTime) {
  const age = refTime - ts;
  if(age <= 0) return 1.0;
  return Math.pow(0.5, age / DECAY_HALF_LIFE);
}
function computeScore(panelData, refTime) {
  const views = panelData.views || [];
  const clicks = panelData.clicks || 0;
  const expands = panelData.expands || 0;
  const viewDurations = panelData.viewDurations || [];
  const totalDuration = viewDurations.reduce((a,b)=>a+b, 0);
  const avgDuration = viewDurations.length ? totalDuration / viewDurations.length : 0;
  let recencyScore = 0;
  for(const v of views) recencyScore += decayWeight(v, refTime);
  const freqScore = views.length + clicks * 2 + expands * 1.5;
  const durationScore = Math.log1p(totalDuration / 1000);
  const composite = freqScore * durationScore * (1 + recencyScore);
  return { composite, freqScore, durationScore, recencyScore, totalDuration, clicks, expands, viewCount: views.length };
}
function getPanelData(state, id) {
  if(!state.panels[id]) {
    state.panels[id] = { views: [], viewDurations: [], clicks: 0, expands: 0, lastViewStart: null };
  }
  return state.panels[id];
}
let state = loadState();
state.order = state.order || PANEL_DEFS.map(p=>p.id);
state.overrides = state.overrides || {};
for(const def of PANEL_DEFS) {
  if(!state.panels[def.id]) state.panels[def.id] = { views: [], viewDurations: [], clicks: 0, expands: 0, lastViewStart: null };
}
saveState(state);
const grid = document.getElementById('grid');
const moreSection = document.getElementById('more-section');
const morePanels = document.getElementById('more-panels');
const toastEl = document.getElementById('toast');
let toastTimer = null;
function toast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2000);
}
function recordView(id, start, end) {
  const pd = getPanelData(state, id);
  pd.views = pd.views || [];
  pd.viewDurations = pd.viewDurations || [];
  pd.views.push(now());
  if(end > start) pd.viewDurations.push(end - start);
  if(pd.views.length > 200) pd.views = pd.views.slice(-200);
  if(pd.viewDurations.length > 200) pd.viewDurations = pd.viewDurations.slice(-200);
}
function recordClick(id) {
  const pd = getPanelData(state, id);
  pd.clicks = (pd.clicks || 0) + 1;
}
function recordExpand(id) {
  const pd = getPanelData(state, id);
  pd.expands = (pd.expands || 0) + 1;
}
function getScores() {
  const refTime = now();
  const scores = {};
  for(const def of PANEL_DEFS) {
    scores[def.id] = computeScore(getPanelData(state, def.id), refTime);
  }
  return scores;
}
const panelElements = new Map();
const panelViewTimers = new Map();
let observer = null;
function setupObserver() {
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    for(const entry of entries) {
      const id = entry.target.dataset.panelId;
      if(!id) continue;
      if(entry.isIntersecting) {
        panelViewTimers.set(id, now());
      } else {
        const start = panelViewTimers.get(id);
        if(start) {
          recordView(id, start, now());
          panelViewTimers.delete(id);
        }
      }
    }
  }, { threshold: 0.3 });
}
function observePanels() {
  panelElements.forEach(el => {
    if(el.isConnected) observer.observe(el);
  });
}
function buildSparkline(id, color) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 100 36');
  svg.setAttribute('preserveAspectRatio', 'none');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  const def = PANEL_DEFS.find(p=>p.id===id);
  const d = generateSparklinePath(16, def?def.min:0, def?def.max:100);
  path.setAttribute('d', d);
  path.setAttribute('fill', 'none');
  path.setAttribute('stroke', color || 'var(--accent)');
  path.setAttribute('stroke-width', '2');
  path.setAttribute('stroke-linecap', 'round');
  svg.appendChild(path);
  const wrapper = document.createElement('div');
  wrapper.className = 'sparkline-wrap';
  wrapper.appendChild(svg);
  return wrapper;
}
function createPanelElement(def, scoreData, rank) {
  const existing = panelElements.get(def.id);
  if(existing && existing.isConnected) {
    updatePanelElement(existing, def, scoreData, rank);
    return existing;
  }
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = def.id;
  el.dataset.rank = rank;
  el.innerHTML = `
    <div class="panel-actions">
      <button class="lock-btn" data-action="lock" data-id="${def.id}" title="Lock position">L</button>
      <button data-action="collapse" data-id="${def.id}" title="Collapse">_</button>
    </div>
    <div class="panel-header">
      <span class="panel-title">${def.title}</span>
    </div>
    <div class="panel-body">
      <div class="panel-value" style="color:${def.color}">${def.value}</div>
      <div class="panel-subtitle">${def.sub}</div>
    </div>
    <div class="panel-score">
      <span>Score: ${scoreData.composite.toFixed(1)}</span>
      <span>Rank #${rank}</span>
    </div>
  `;
  const sparkline = buildSparkline(def.id, def.color);
  el.querySelector('.panel-body').appendChild(sparkline);
  const lockBtn = el.querySelector('.lock-btn');
  if(state.overrides[def.id] && state.overrides[def.id].locked) {
    el.classList.add('locked');
    lockBtn.classList.add('locked');
  }
  el.addEventListener('click', (e) => {
    if(e.target.closest('button')) return;
    recordClick(def.id);
    saveState(state);
  });
  el.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const action = btn.dataset.action;
      const id = btn.dataset.id;
      if(action === 'lock') toggleLock(id, el, btn);
      if(action === 'collapse') toggleCollapse(id, el);
    });
  });
  panelElements.set(def.id, el);
  observer.observe(el);
  return el;
}
function updatePanelElement(el, def, scoreData, rank) {
  el.dataset.rank = rank;
  const scoreEl = el.querySelector('.panel-score');
  if(scoreEl) scoreEl.innerHTML = `<span>Score: ${scoreData.composite.toFixed(1)}</span><span>Rank #${rank}</span>`;
}
function toggleLock(id, el, btn) {
  if(!state.overrides[id]) state.overrides[id] = {};
  state.overrides[id].locked = !state.overrides[id].locked;
  if(state.overrides[id].locked) {
    el.classList.add('locked');
    btn.classList.add('locked');
    toast('Panel locked: ' + PANEL_DEFS.find(p=>p.id===id).title);
  } else {
    el.classList.remove('locked');
    btn.classList.remove('locked');
    toast('Panel unlocked: ' + PANEL_DEFS.find(p=>p.id===id).title);
  }
  saveState(state);
  renderGrid();
}
function toggleCollapse(id, el) {
  recordExpand(id);
  const wasCollapsed = el.classList.contains('collapsed');
  if(wasCollapsed) {
    el.classList.remove('collapsed');
    el.classList.add('normal');
    toast('Expanded: ' + PANEL_DEFS.find(p=>p.id===id).title);
  } else {
    el.classList.add('collapsed');
    el.classList.remove('dominant','normal','compact');
    toast('Collapsed: ' + PANEL_DEFS.find(p=>p.id===id).title);
  }
  saveState(state);
  renderGrid();
}
function classifyPanels(scores) {
  const arr = Object.entries(scores).map(([id,s]) => ({id, ...s}));
  arr.sort((a,b) => b.composite - a.composite);
  const maxScore = arr.length ? arr[0].composite : 1;
  const result = [];
  for(let i=0;i<arr.length;i++) {
    const item = arr[i];
    const ratio = maxScore > 0 ? item.composite / maxScore : 0;
    let tier;
    if(ratio >= DOMINANCE_THRESHOLD) tier = 'dominant';
    else if(ratio >= COMPACT_THRESHOLD) tier = 'normal';
    else if(ratio >= COLLAPSE_THRESHOLD) tier = 'compact';
    else tier = 'collapsed';
    result.push({...item, rank: i+1, ratio, tier});
  }
  result.sort((a,b) => {
    const aLocked = state.overrides[a.id]?.locked;
    const bLocked = state.overrides[b.id]?.locked;
    if(aLocked && !bLocked) return -1;
    if(!aLocked && bLocked) return 1;
    return a.rank - b.rank;
  });
  return result;
}
function renderGrid() {
  const scores = getScores();
  const classified = classifyPanels(scores);
  const fragment = document.createDocumentFragment();
  const collapsedItems = [];
  for(const item of classified) {
    const def = PANEL_DEFS.find(p=>p.id===item.id);
    if(!def) continue;
    if(item.tier === 'collapsed') {
      collapsedItems.push({def, item});
      const existing = panelElements.get(item.id);
      if(existing) existing.remove();
      continue;
    }
    const el = createPanelElement(def, item, item.rank);
    el.classList.remove('dominant','normal','compact','collapsed');
    if(item.tier === 'dominant') el.classList.add('dominant');
    else if(item.tier === 'normal') el.classList.add('normal');
    else if(item.tier === 'compact') el.classList.add('compact');
    if(state.overrides[item.id]?.locked) el.classList.add('locked');
    fragment.appendChild(el);
  }
  grid.innerHTML = '';
  grid.appendChild(fragment);
  const mode = document.getElementById('sel-mode').value;
  if(mode === 'score-sort') grid.classList.add('arrange-by-rank');
  else grid.classList.remove('arrange-by-rank');
  morePanels.innerHTML = '';
  if(collapsedItems.length) {
    moreSection.style.display = 'block';
    for(const {def, item} of collapsedItems) {
      const mini = document.createElement('span');
      mini.className = 'mini';
      mini.textContent = def.title + ' (' + item.composite.toFixed(1) + ')';
      mini.title = 'Click to restore';
      mini.addEventListener('click', () => {
        const pd = getPanelData(state, def.id);
        pd.clicks = (pd.clicks||0) + 5;
        pd.views.push(now());
        saveState(state);
        renderGrid();
        toast('Restored: ' + def.title);
      });
      morePanels.appendChild(mini);
    }
  } else {
    moreSection.style.display = 'none';
  }
  observePanels();
  saveState(state);
}
let rescoreTimer = null;
function scheduleRescore() {
  clearTimeout(rescoreTimer);
  rescoreTimer = setTimeout(() => {
    saveState(state);
    renderGrid();
    scheduleRescore();
  }, RESCORE_INTERVAL);
}
function stopViewTracking() {
  panelViewTimers.forEach((start, id) => {
    recordView(id, start, now());
  });
  panelViewTimers.clear();
}
window.addEventListener('beforeunload', () => {
  stopViewTracking();
  saveState(state);
});
document.getElementById('btn-reset').addEventListener('click', () => {
  state = { panels: {}, order: PANEL_DEFS.map(p=>p.id), overrides: {} };
  for(const def of PANEL_DEFS) {
    state.panels[def.id] = { views:[], viewDurations:[], clicks:0, expands:0, lastViewStart:null };
  }
  saveState(state);
  renderGrid();
  toast('All tracking data reset');
});
document.getElementById('btn-force-reflow').addEventListener('click', () => {
  stopViewTracking();
  renderGrid();
  toast('Layout reflowed');
});
document.getElementById('sel-mode').addEventListener('change', () => {
  renderGrid();
  const mode = document.getElementById('sel-mode').value;
  if(mode==='manual') toast('Manual mode: drag panels to reorder (simulated)');
  else if(mode==='score-sort') toast('Sorted by attention score');
  else toast('Auto-arrange active');
});
window.addEventListener('visibilitychange', () => {
  if(document.hidden) stopViewTracking();
});
window.addEventListener('pagehide', () => {
  stopViewTracking();
  saveState(state);
});
setupObserver();
renderGrid();
scheduleRescore();
})();
</script>
</body>
</html>