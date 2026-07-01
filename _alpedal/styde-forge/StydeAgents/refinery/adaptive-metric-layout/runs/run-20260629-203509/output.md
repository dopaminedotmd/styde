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
  --text: #e1e4ed;
  --text2: #9498a5;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --compact-bg: #141720;
  --drag-ghost: rgba(108,140,255,0.15);
  --shadow: 0 2px 12px rgba(0,0,0,0.4);
  --radius: 8px;
  --radius-sm: 5px;
  --transition: 0.25s cubic-bezier(0.4,0,0.2,1);
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  font-family:system-ui,-apple-system,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
}
header {
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 20px; background:var(--surface);
  border-bottom:1px solid var(--border);
  position:sticky; top:0; z-index:100;
  backdrop-filter:blur(8px);
}
header h1 { font-size:1.1rem; font-weight:600; letter-spacing:-0.01em; }
.header-actions { display:flex; gap:8px; align-items:center; }
.btn {
  background:var(--surface2); border:1px solid var(--border);
  color:var(--text); padding:6px 14px; border-radius:var(--radius-sm);
  cursor:pointer; font-size:0.82rem; transition:var(--transition);
  display:flex; align-items:center; gap:5px;
}
.btn:hover { background:var(--border); }
.btn.active { background:var(--accent); border-color:var(--accent); color:#fff; }
.btn-sm { padding:3px 8px; font-size:0.7rem; }
.dashboard {
  display:grid; gap:10px; padding:14px;
  grid-template-columns:repeat(auto-fill, minmax(260px, 1fr));
  grid-auto-rows: minmax(120px, auto);
  grid-auto-flow: dense;
  transition:var(--transition);
  max-width:1600px; margin:0 auto;
}
.panel {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius); padding:14px;
  transition:var(--transition); position:relative;
  cursor:grab; user-select:none;
  display:flex; flex-direction:column;
  min-height:120px;
  overflow:hidden;
  box-shadow:var(--shadow);
}
.panel:hover { border-color:var(--accent); }
.panel.dragging {
  opacity:0.7; cursor:grabbing; z-index:10;
  box-shadow:0 8px 32px rgba(0,0,0,0.5);
}
.panel.drag-over { border-color:var(--accent); background:var(--drag-ghost); }
.panel.locked { cursor:default; }
.panel.locked:hover { border-color:var(--border); }
.panel.locked .lock-icon { color:var(--accent2); }
.panel.rank-high { grid-column:span 2; grid-row:span 2; min-height:260px; }
.panel.rank-mid { grid-column:span 1; grid-row:span 1; }
.panel.rank-low.compact {
  grid-column:span 1; grid-row:span 1;
  min-height:60px; padding:8px 12px;
  background:var(--compact-bg);
}
.panel.rank-low.compact .panel-body { display:none; }
.panel.rank-low.compact .panel-preview { display:flex; }
.panel-preview { display:none; align-items:center; gap:8px; font-size:0.78rem; color:var(--text2); }
.panel-preview .preview-value { color:var(--accent); font-weight:600; }
.panel-header {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:10px; gap:6px;
}
.panel-title { font-size:0.88rem; font-weight:600; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.panel-actions { display:flex; gap:4px; align-items:center; }
.icon-btn {
  background:none; border:none; color:var(--text2); cursor:pointer;
  padding:2px 4px; border-radius:3px; font-size:0.75rem;
  transition:var(--transition); line-height:1;
}
.icon-btn:hover { color:var(--text); background:var(--surface2); }
.icon-btn.locked-btn { font-size:0.85rem; }
.panel-body { flex:1; display:flex; flex-direction:column; gap:6px; }
.metric-row { display:flex; justify-content:space-between; align-items:center; font-size:0.82rem; }
.metric-label { color:var(--text2); }
.metric-value { font-weight:600; font-variant-numeric:tabular-nums; }
.metric-value.up { color:var(--accent2); }
.metric-value.down { color:#f87171; }
.metric-bar {
  height:4px; border-radius:2px; background:var(--surface2);
  margin-top:4px; overflow:hidden;
}
.metric-bar-fill {
  height:100%; border-radius:2px; transition:width 0.6s ease;
  background:linear-gradient(90deg, var(--accent), var(--accent2));
}
.rank-badge {
  font-size:0.65rem; padding:1px 6px; border-radius:10px;
  background:var(--surface2); color:var(--text2);
}
.rank-badge.hot { background:var(--accent); color:#fff; }
.rank-badge.warm { background:var(--warn); color:#000; }
.stats-bar {
  display:flex; gap:16px; padding:8px 20px; font-size:0.72rem;
  color:var(--text2); background:var(--surface); border-bottom:1px solid var(--border);
  justify-content:center;
}
.stats-bar span { display:flex; align-items:center; gap:4px; }
.stats-bar .stat-val { color:var(--accent); font-weight:600; }
@keyframes fadeIn {
  from { opacity:0; transform:translateY(8px); }
  to { opacity:1; transform:translateY(0); }
}
.panel { animation:fadeIn 0.3s ease both; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Dashboard</h1>
  <div class="header-actions">
    <span style="font-size:0.72rem;color:var(--text2)" id="layout-status">auto</span>
    <button class="btn btn-sm" id="btn-reset" title="Reset all tracking data">Reset</button>
    <button class="btn btn-sm" id="btn-auto-layout" title="Force auto-layout recalculation">Recalc</button>
  </div>
</header>
<div class="stats-bar">
  <span>Sessions: <span class="stat-val" id="stat-sessions">1</span></span>
  <span>Total views: <span class="stat-val" id="stat-views">0</span></span>
  <span>Interactions: <span class="stat-val" id="stat-interactions">0</span></span>
  <span>Locked panels: <span class="stat-val" id="stat-locked">0</span></span>
  <span>Last adapted: <span class="stat-val" id="stat-last">-</span></span>
</div>
<div class="dashboard" id="dashboard"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_metric_layout_v2';
const DECAY_HALF_LIFE = 7 * 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD = 0.25;
const TRACK_INTERVAL = 2000;
let mutationObserver = null;
let intersectionObserver = null;
let layoutCounter = 0;
let trackIntervalId = null;
let panels = [];
let panelMap = new Map();
let draggedEl = null;
let dragGhost = null;
let dragStartX = 0, dragStartY = 0;
function defaultPanels() {
  return [
    { id:'revenue',    title:'Revenue',        metric:'$45.2k', change:'+12.3%', trend:'up',   bar:78 },
    { id:'users',      title:'Active Users',   metric:'8,421',  change:'+5.1%',  trend:'up',   bar:65 },
    { id:'conversion', title:'Conversion Rate', metric:'3.2%',  change:'-0.4%',  trend:'down', bar:42 },
    { id:'latency',    title:'API Latency',     metric:'142ms',  change:'-8.2%',  trend:'up',   bar:55 },
    { id:'errors',     title:'Error Rate',      metric:'0.12%',  change:'+0.03%', trend:'down', bar:18 },
    { id:'storage',    title:'Storage Used',    metric:'67.8GB', change:'+2.1%',  trend:'up',   bar:72 },
    { id:'bandwidth',  title:'Bandwidth',       metric:'1.2Gbps',change:'-1.3%',  trend:'down', bar:38 },
    { id:'cpu',        title:'CPU Load',        metric:'34%',    change:'+2.8%',  trend:'down', bar:50 },
    { id:'memory',     title:'Memory',          metric:'58.3%',  change:'-0.9%',  trend:'up',   bar:60 },
    { id:'requests',   title:'Requests/min',    metric:'3.2k',   change:'+15.1%', trend:'up',   bar:88 },
  ];
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return null;
}
function saveState(state) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch(e) {}
}
function initState() {
  let saved = loadState();
  if (!saved || !saved.panels || saved.panels.length === 0) {
    const defaults = defaultPanels();
    saved = {
      panels: defaults.map((p,i) => ({
        ...p,
        rank: 0,
        viewDuration: 0,
        interactions: 0,
        lastInteraction: 0,
        locked: false,
        position: i,
        compact: false
      })),
      layoutCounter: 0,
      sessions: 1,
      lastAdapted: null
    };
    saveState(saved);
    layoutCounter = 0;
  } else {
    layoutCounter = saved.layoutCounter || 0;
    saved.sessions = (saved.sessions || 0) + 1;
    saveState(saved);
  }
  panels = saved.panels;
  updateStats();
}
function updateStats() {
  document.getElementById('stat-sessions').textContent = loadState()?.sessions || 1;
  document.getElementById('stat-views').textContent = panels.reduce((s,p)=>s+(p.viewDuration>0?1:0), 0);
  document.getElementById('stat-interactions').textContent = panels.reduce((s,p)=>s+p.interactions, 0);
  document.getElementById('stat-locked').textContent = panels.filter(p=>p.locked).length;
  document.getElementById('stat-last').textContent = (loadState()?.lastAdapted) || '-';
}
function computeRank(panel) {
  const now = Date.now();
  const recency = panel.lastInteraction ? Math.exp(-(now - panel.lastInteraction) / DECAY_HALF_LIFE) : 0.1;
  const frequency = Math.log1p(panel.interactions);
  const duration = Math.log1p(panel.viewDuration / 1000);
  return frequency * duration * (0.3 + 0.7 * recency);
}
function rankAll() {
  panels.forEach(p => { p.rank = computeRank(p); });
  const maxRank = Math.max(...panels.map(p=>p.rank), 0.001);
  panels.forEach(p => {
    const normalized = p.rank / maxRank;
    p.compact = !p.locked && normalized < COMPACT_THRESHOLD;
  });
  const sorted = [...panels].sort((a,b) => b.rank - a.rank);
  sorted.forEach((p,i) => {
    if (!p.locked) p.position = i;
  });
}
function getRankClass(panel) {
  const maxRank = Math.max(...panels.map(p=>p.rank), 0.001);
  const norm = panel.rank / maxRank;
  if (norm >= 0.7) return 'rank-high';
  if (norm >= COMPACT_THRESHOLD) return 'rank-mid';
  return 'rank-low';
}
function render() {
  const dashboard = document.getElementById('dashboard');
  const existing = new Map();
  dashboard.querySelectorAll('.panel').forEach(el => {
    existing.set(el.dataset.panelId, el);
  });
  const fragment = document.createDocumentFragment();
  panels.forEach((panel, index) => {
    let el = existing.get(panel.id);
    if (!el) {
      el = createPanelElement(panel);
    }
    updatePanelElement(el, panel, index);
    el.dataset.panelId = panel.id;
    if (panel.locked) {
      el.classList.add('locked');
    } else {
      el.classList.remove('locked');
    }
    const rankClass = getRankClass(panel);
    el.classList.remove('rank-high','rank-mid','rank-low','compact');
    el.classList.add(rankClass);
    if (panel.compact) el.classList.add('compact');
    const sortOrder = panel.locked ? panel.position : index;
    el.style.order = sortOrder;
    fragment.appendChild(el);
  });
  dashboard.innerHTML = '';
  dashboard.appendChild(fragment);
  existing.forEach((el, id) => {
    if (!panels.find(p => p.id === id)) el.remove();
  });
  document.getElementById('layout-status').textContent =
    panels.some(p=>p.locked) ? 'semi-auto' : 'auto';
  layoutCounter++;
}
function createPanelElement(panel) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.draggable = true;
  el.dataset.panelId = panel.id;
  el.innerHTML = `
    <div class="panel-header">
      <span class="panel-title">${escapeHtml(panel.title)}</span>
      <span class="rank-badge" data-rank-badge>--</span>
      <div class="panel-actions">
        <button class="icon-btn locked-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button class="icon-btn" data-action="expand" title="Toggle compact">&#8690;</button>
      </div>
    </div>
    <div class="panel-preview">
      <span>${escapeHtml(panel.title)}</span>
      <span class="preview-value">${escapeHtml(panel.metric)}</span>
    </div>
    <div class="panel-body">
      <div class="metric-row">
        <span class="metric-label">Value</span>
        <span class="metric-value">${escapeHtml(panel.metric)}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Change</span>
        <span class="metric-value ${panel.trend}">${escapeHtml(panel.change)}</span>
      </div>
      <div class="metric-bar"><div class="metric-bar-fill" style="width:${panel.bar}%"></div></div>
      <div style="font-size:0.68rem;color:var(--text2);margin-top:4px">
        Score: <span data-score>${panel.rank.toFixed(2)}</span>
      </div>
    </div>`;
  return el;
}
function updatePanelElement(el, panel, index) {
  const title = el.querySelector('.panel-title');
  if (title) title.textContent = panel.title;
  const metricVal = el.querySelector('.metric-value');
  if (metricVal) {
    metricVal.textContent = panel.metric;
    metricVal.className = 'metric-value ' + (panel.trend || '');
  }
  const changeEl = el.querySelectorAll('.metric-value')[1];
  if (changeEl) {
    changeEl.textContent = panel.change;
    changeEl.className = 'metric-value ' + (panel.trend || '');
  }
  const barFill = el.querySelector('.metric-bar-fill');
  if (barFill) barFill.style.width = panel.bar + '%';
  const scoreEl = el.querySelector('[data-score]');
  if (scoreEl) scoreEl.textContent = panel.rank.toFixed(2);
  const badge = el.querySelector('[data-rank-badge]');
  if (badge) {
    const maxRank = Math.max(...panels.map(p=>p.rank), 0.001);
    const norm = panel.rank / maxRank;
    badge.textContent = norm >= 0.7 ? 'HOT' : norm >= COMPACT_THRESHOLD ? 'WARM' : 'COLD';
    badge.className = 'rank-badge ' + (norm >= 0.7 ? 'hot' : norm >= COMPACT_THRESHOLD ? 'warm' : '');
  }
  const lockBtn = el.querySelector('[data-action="lock"]');
  if (lockBtn) lockBtn.innerHTML = panel.locked ? '&#128274;' : '&#128275;';
  el.dataset.panelId = panel.id;
}
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
function persist() {
  const state = loadState() || {};
  state.panels = panels.map(p => ({
    id:p.id, title:p.title, metric:p.metric, change:p.change,
    trend:p.trend, bar:p.bar, rank:p.rank,
    viewDuration:p.viewDuration, interactions:p.interactions,
    lastInteraction:p.lastInteraction, locked:p.locked,
    position:p.position, compact:p.compact
  }));
  state.layoutCounter = layoutCounter;
  state.lastAdapted = new Date().toISOString();
  saveState(state);
}
function initMutationObserver() {
  if (mutationObserver) return;
  mutationObserver = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.type === 'childList') {
        m.addedNodes.forEach(node => {
          if (node.nodeType === 1 && node.classList.contains('panel')) {
            intersectionObserver.observe(node);
          }
        });
        m.removedNodes.forEach(node => {
          if (node.nodeType === 1 && node.classList.contains('panel')) {
            intersectionObserver.unobserve(node);
          }
        });
      }
    }
  });
}
function initIntersectionObserver() {
  intersectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      const panel = panelMap.get(panelId);
      if (!panel) return;
      if (entry.isIntersecting) {
        entry.target.dataset.visibleStart = Date.now();
      } else if (entry.target.dataset.visibleStart) {
        const visibleDuration = Date.now() - parseInt(entry.target.dataset.visibleStart);
        panel.viewDuration += visibleDuration;
        delete entry.target.dataset.visibleStart;
        persist();
      }
    });
  }, { threshold: 0.3 });
}
function postMountInit() {
  const dashboard = document.getElementById('dashboard');
  if (mutationObserver) {
    mutationObserver.observe(dashboard, { childList: true, subtree: false });
  }
  document.querySelectorAll('.panel').forEach(el => {
    intersectionObserver.observe(el);
    el.dataset.visibleStart = Date.now();
  });
  const evt = new CustomEvent('virtualscroll', { detail: { type: 'post-mount' } });
  window.dispatchEvent(evt);
}
function trackViewDurations() {
  document.querySelectorAll('.panel').forEach(el => {
    const panelId = el.dataset.panelId;
    const panel = panelMap.get(panelId);
    if (!panel) return;
    const rect = el.getBoundingClientRect();
    const viewHeight = window.innerHeight;
    const visibleTop = Math.max(0, rect.top);
    const visibleBottom = Math.min(viewHeight, rect.bottom);
    const visibleHeight = Math.max(0, visibleBottom - visibleTop);
    if (visibleHeight > rect.height * 0.3) {
      panel.viewDuration += TRACK_INTERVAL;
    }
  });
  persist();
}
function setupTracking() {
  if (trackIntervalId) clearInterval(trackIntervalId);
  trackIntervalId = setInterval(trackViewDurations, TRACK_INTERVAL);
}
function setupEventDelegation() {
  const dashboard = document.getElementById('dashboard');
  dashboard.addEventListener('click', (e) => {
    const panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    const panelId = panelEl.dataset.panelId;
    const panel = panelMap.get(panelId);
    if (!panel) return;
    panel.interactions++;
    panel.lastInteraction = Date.now();
    const action = e.target.closest('[data-action]');
    if (action) {
      const act = action.dataset.action;
      if (act === 'lock') {
        panel.locked = !panel.locked;
        if (panel.locked) panel.position = panels.indexOf(panel);
      } else if (act === 'expand') {
        panel.compact = !panel.compact;
      }
      rankAll();
      render();
      persist();
      updateStats();
    } else {
      panel.interactions++;
      persist();
    }
  });
  dashboard.addEventListener('dragstart', (e) => {
    const panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    const panelId = panelEl.dataset.panelId;
    const panel = panelMap.get(panelId);
    if (!panel || !panel.locked) {
      e.preventDefault();
      return;
    }
    draggedEl = panelEl;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    panelEl.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panelId);
  });
  dashboard.addEventListener('dragover', (e) => {
    e.preventDefault();
    if (!draggedEl) return;
    const target = e.target.closest('.panel');
    if (target && target !== draggedEl) {
      target.classList.add('drag-over');
    }
  });
  dashboard.addEventListener('dragleave', (e) => {
    const target = e.target.closest('.panel');
    if (target) target.classList.remove('drag-over');
  });
  dashboard.addEventListener('drop', (e) => {
    e.preventDefault();
    if (!draggedEl) return;
    const target = e.target.closest('.panel');
    dashboard.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    if (target && target !== draggedEl) {
      const sourceId = draggedEl.dataset.panelId;
      const targetId = target.dataset.panelId;
      const sourcePanel = panelMap.get(sourceId);
      const targetPanel = panelMap.get(targetId);
      if (sourcePanel && targetPanel && sourcePanel.locked && targetPanel.locked) {
        const srcPos = sourcePanel.position;
        sourcePanel.position = targetPanel.position;
        targetPanel.position = srcPos;
        panels.sort((a,b) => a.position - b.position);
        rankAll();
        render();
        persist();
        updateStats();
      }
    }
    if (draggedEl) draggedEl.classList.remove('dragging');
    draggedEl = null;
  });
  dashboard.addEventListener('dragend', (e) => {
    if (draggedEl) draggedEl.classList.remove('dragging');
    dashboard.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    draggedEl = null;
  });
  window.addEventListener('virtualscroll', () => {
    document.querySelectorAll('.panel').forEach(el => {
      if (!el.dataset.visibleStart) {
        el.dataset.visibleStart = Date.now();
      }
    });
    rankAll();
    render();
    persist();
    updateStats();
  });
}
function bindButtons() {
  document.getElementById('btn-reset').addEventListener('click', () => {
    localStorage.removeItem(STORAGE_KEY);
    initState();
    panelMap.clear();
    panels.forEach(p => panelMap.set(p.id, p));
    rankAll();
    render();
    persist();
    updateStats();
    document.querySelectorAll('.panel').forEach(el => {
      intersectionObserver.observe(el);
      el.dataset.visibleStart = Date.now();
    });
  });
  document.getElementById('btn-auto-layout').addEventListener('click', () => {
    rankAll();
    render();
    layoutCounter++;
    persist();
    updateStats();
    document.getElementById('layout-status').textContent = 'recalc';
    setTimeout(() => {
      document.getElementById('layout-status').textContent =
        panels.some(p=>p.locked) ? 'semi-auto' : 'auto';
    }, 1500);
  });
}
function init() {
  initState();
  panels.forEach(p => panelMap.set(p.id, p));
  initMutationObserver();
  initIntersectionObserver();
  rankAll();
  render();
  setupEventDelegation();
  setupTracking();
  bindButtons();
  postMountInit();
  persist();
  updateStats();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
})();
</script>
</body>
</html>