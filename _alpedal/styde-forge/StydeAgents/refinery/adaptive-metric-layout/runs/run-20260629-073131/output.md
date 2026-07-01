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
  --border: #2a2d37;
  --text: #e1e4eb;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --rank-1: #ff6b6b;
  --rank-2: #ffa94d;
  --rank-3: #ffd43b;
  --compact-bg: #14161f;
}
* { box-sizing:border-box; margin:0; padding:0 }
body {
  font-family:system-ui,-apple-system,sans-serif;
  background:var(--bg); color:var(--text);
  min-height:100vh; padding:16px;
}
header {
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:16px; padding:0 4px;
}
h1 { font-size:1.25rem; font-weight:600; letter-spacing:-0.02em }
.controls { display:flex; gap:8px; align-items:center }
.btn {
  background:var(--surface); border:1px solid var(--border);
  color:var(--text); padding:6px 14px; border-radius:6px;
  cursor:pointer; font-size:0.8125rem; transition:all 0.15s;
}
.btn:hover { border-color:var(--accent); background:var(--accent-glow) }
.btn.active { background:var(--accent); border-color:var(--accent); color:#fff }
.grid {
  display:grid; gap:12px;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  grid-auto-rows:minmax(200px,auto);
  grid-auto-flow:dense;
}
.panel {
  background:var(--surface); border:1px solid var(--border);
  border-radius:10px; padding:16px; position:relative;
  transition: grid-column 0.35s ease, grid-row 0.35s ease, opacity 0.35s ease;
  display:flex; flex-direction:column; min-height:200px;
}
.panel.rank-1 { grid-column:span 2; grid-row:span 2; min-height:420px }
.panel.rank-2 { grid-column:span 2; grid-row:span 1; min-height:280px }
.panel.rank-3 { grid-column:span 1; grid-row:span 1 }
.panel.compact { grid-column:span 1; grid-row:span 1; min-height:120px; background:var(--compact-bg) }
.panel.compact .body { display:none }
.panel.compact .preview { display:flex }
.panel.locked { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent) }
.panel-header {
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:12px; gap:8px;
}
.panel-title { font-weight:600; font-size:0.875rem; text-transform:uppercase; letter-spacing:0.05em }
.rank-badge {
  font-size:0.6875rem; padding:2px 8px; border-radius:4px;
  font-weight:600; opacity:0.8;
}
.rank-1-badge { background:var(--rank-1); color:#000 }
.rank-2-badge { background:var(--rank-2); color:#000 }
.rank-3-badge { background:var(--rank-3); color:#000 }
.panel-actions { display:flex; gap:4px }
.icon-btn {
  background:none; border:none; color:var(--text-dim); cursor:pointer;
  padding:4px 6px; border-radius:4px; font-size:0.75rem; line-height:1;
}
.icon-btn:hover { color:var(--text); background:var(--border) }
.icon-btn.locked-icon { color:var(--accent) }
.body { flex:1; display:flex; flex-direction:column; gap:8px }
.metric { display:flex; justify-content:space-between; align-items:baseline }
.metric-label { font-size:0.75rem; color:var(--text-dim) }
.metric-value { font-size:1.5rem; font-weight:700; font-variant-numeric:tabular-nums }
.metric-value.up { color:#51cf66 }
.metric-value.down { color:var(--rank-1) }
.spark {
  height:40px; background:var(--bg); border-radius:6px;
  display:flex; align-items:flex-end; gap:2px; padding:4px 6px; margin-top:4px;
}
.spark-bar {
  flex:1; min-width:2px; border-radius:2px 2px 0 0;
  background:var(--accent); opacity:0.6; transition:height 0.3s ease;
}
.preview {
  display:none; align-items:center; justify-content:center; flex:1;
  font-size:0.75rem; color:var(--text-dim); gap:4px;
}
.score-info {
  font-size:0.6875rem; color:var(--text-dim); margin-top:auto;
  padding-top:8px; border-top:1px solid var(--border);
  display:flex; justify-content:space-between;
}
.tooltip {
  position:fixed; background:var(--surface); border:1px solid var(--accent);
  color:var(--text); padding:6px 10px; border-radius:6px; font-size:0.75rem;
  pointer-events:none; z-index:100; opacity:0; transition:opacity 0.15s;
  box-shadow:0 4px 12px rgba(0,0,0,0.4);
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btnLockAll" title="Lock current layout">Lock All</button>
    <span style="font-size:0.75rem;color:var(--text-dim)" id="statusText">idle</span>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
const STORE_KEY = 'adaptive_layout_v1';
const POLL_INTERVAL_IDLE = 8000;
const POLL_INTERVAL_ACTIVE = 1500;
const IDLE_TIMEOUT = 12000;
const RECENCY_HALFLIFE = 3600000;
const COMPACT_THRESHOLD = 0.15;
const VIEWPORT_VISIBILITY = 0.5;
const PANEL_DEFS = [
  { id:'revenue', title:'Revenue', metric:'$128.4K', change:'+12.3%', dir:'up', spark:[3,5,4,7,6,8,7,9,8,10,9,11,10,12,11,13,12,14,13,15] },
  { id:'users', title:'Active Users', metric:'8,421', change:'+5.7%', dir:'up', spark:[2,3,4,3,5,4,6,5,7,6,8,7,9,8,10,9,11,10,12,11] },
  { id:'latency', title:'API Latency', metric:'42ms', change:'-8.1%', dir:'down', spark:[8,7,6,5,4,5,4,3,4,3,2,3,2,1,2,1,2,1,1,1] },
  { id:'errors', title:'Error Rate', metric:'0.12%', change:'-0.03%', dir:'down', spark:[1,1,2,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1] },
  { id:'conversion', title:'Conversion', metric:'3.8%', change:'+0.4%', dir:'up', spark:[1,2,1,2,3,2,3,4,3,4,5,4,5,6,5,6,7,6,7,8] },
  { id:'sessions', title:'Sessions', metric:'2.1K', change:'+9.2%', dir:'up', spark:[4,5,6,5,7,6,8,7,9,8,10,9,11,10,12,11,13,12,14,13] },
  { id:'bounce', title:'Bounce Rate', metric:'24%', change:'+1.2%', dir:'up', spark:[6,5,6,5,4,5,4,3,4,3,2,3,2,2,3,2,2,3,2,2] },
  { id:'storage', title:'Storage', metric:'64.2GB', change:'+2.1%', dir:'up', spark:[3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,10,10,10,10] },
];
let state = loadState();
let panels = buildPanels(state);
let dirtyLayout = false;
let dirtyScores = false;
let lastInteraction = Date.now();
let pollTimer = null;
let observer = null;
let viewTimeAccum = new Map();
let visibilityMap = new Map();
let panelEls = new Map();
function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return { scores:{}, locks:{}, positions:{}, tracking:{ viewTime:{}, interactions:{}, lastSeen:{} } };
}
function saveState() {
  const scores = {};
  const locks = {};
  const positions = {};
  panels.forEach(p => {
    scores[p.id] = p.score;
    locks[p.id] = p.locked;
    positions[p.id] = p.manualPos;
  });
  state.scores = scores;
  state.locks = locks;
  state.positions = positions;
  state.tracking.viewTime = Object.fromEntries(viewTimeAccum);
  state.tracking.interactions = Object.fromEntries(state.tracking.interactions instanceof Map ? state.tracking.interactions : new Map());
  try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch(e) {}
}
function buildPanels(saved) {
  const now = Date.now();
  return PANEL_DEFS.map((def, i) => {
    const sid = saved.scores[def.id] || 0.5;
    const locked = !!saved.locks[def.id];
    const manualPos = saved.positions[def.id] || null;
    const viewTime = saved.tracking.viewTime[def.id] || 0;
    const interactions = saved.tracking.interactions[def.id] || 0;
    const lastSeen = saved.tracking.lastSeen[def.id] || now;
    viewTimeAccum.set(def.id, viewTime);
    return {
      ...def,
      score: sid,
      locked,
      manualPos,
      compact: false,
      rank: 3,
      viewTime,
      interactions,
      lastSeen,
      _prevRank: 0,
      _prevCompact: false,
      _el: null,
    };
  });
}
function rescore() {
  const now = Date.now();
  const maxTime = Math.max(1, ...Array.from(viewTimeAccum.values()));
  const maxInteract = Math.max(1, ...panels.map(p => p.interactions));
  panels.forEach(p => {
    const vt = viewTimeAccum.get(p.id) || 0;
    const freq = p.interactions || 0;
    const recency = Math.exp(-(now - (p.lastSeen || now)) / RECENCY_HALFLIFE);
    const normTime = vt / maxTime;
    const normFreq = freq / maxInteract;
    p.score = (normTime * 0.4 + normFreq * 0.4 + recency * 0.2);
  });
  const sorted = [...panels].sort((a,b) => b.score - a.score);
  const total = sorted.length;
  sorted.forEach((p, i) => {
    const percentile = i / total;
    const prevRank = p.rank;
    if (percentile < 0.25) p.rank = 1;
    else if (percentile < 0.55) p.rank = 2;
    else p.rank = 3;
    const prevCompact = p.compact;
    p.compact = p.score < COMPACT_THRESHOLD && !p.locked;
    if (p.rank !== prevRank || p.compact !== prevCompact) dirtyLayout = true;
    p._prevRank = prevRank;
    p._prevCompact = prevCompact;
  });
  dirtyScores = false;
}
function updatePanelDOM(p) {
  const el = p._el;
  if (!el) return;
  const changed = p.rank !== p._prevRank || p.compact !== p._prevCompact;
  if (!changed) {
    const scoreEl = el.querySelector('.score-val');
    if (scoreEl) scoreEl.textContent = (p.score * 100).toFixed(1);
    return;
  }
  el.classList.remove('rank-1','rank-2','rank-3');
  el.classList.add('rank-' + p.rank);
  el.classList.toggle('compact', p.compact);
  const badge = el.querySelector('.rank-badge');
  if (badge) {
    badge.textContent = 'R' + p.rank + (p.compact ? '·C' : '');
    badge.className = 'rank-badge rank-' + p.rank + '-badge';
  }
  const scoreEl = el.querySelector('.score-val');
  if (scoreEl) scoreEl.textContent = (p.score * 100).toFixed(1);
  p._prevRank = p.rank;
  p._prevCompact = p.compact;
}
function commitLayout() {
  if (!dirtyLayout) return;
  rescore();
  panels.forEach(p => updatePanelDOM(p));
  reorderGrid();
  dirtyLayout = false;
}
function reorderGrid() {
  const grid = document.getElementById('grid');
  const lockedFirst = [...panels].filter(p => p.locked);
  const unlocked = [...panels].filter(p => !p.locked);
  unlocked.sort((a,b) => b.score - a.score);
  const ordered = [...lockedFirst, ...unlocked];
  ordered.forEach((p, i) => {
    const el = p._el;
    if (!el) return;
    if (el.style.order !== String(i)) {
      el.style.order = i;
    }
  });
}
function createPanelEl(p) {
  const el = document.createElement('div');
  el.className = 'panel rank-' + p.rank + (p.compact ? ' compact' : '') + (p.locked ? ' locked' : '');
  el.style.order = 0;
  el.innerHTML = `
    <div class="panel-header">
      <span class="panel-title">${p.title}</span>
      <span class="rank-badge rank-${p.rank}-badge">R${p.rank}${p.compact?'·C':''}</span>
      <div class="panel-actions">
        <button class="icon-btn lock-btn${p.locked?' locked-icon':''}" data-action="lock" title="Lock position">&#128274;</button>
        <button class="icon-btn" data-action="expand" title="Toggle compact">&#8690;</button>
      </div>
    </div>
    <div class="body">
      <div class="metric">
        <span class="metric-label">${p.metric}</span>
        <span class="metric-value ${p.dir}">${p.change}</span>
      </div>
      <div class="spark">${p.spark.map(v => '<div class="spark-bar" style="height:'+(v/p.spark.reduce((a,b)=>Math.max(a,b),1)*100)+'%"></div>').join('')}</div>
    </div>
    <div class="preview">&#9632; ${p.metric} | ${p.change}</div>
    <div class="score-info">
      <span>Score: <span class="score-val">${(p.score*100).toFixed(1)}</span></span>
      <span>${formatViewTime(viewTimeAccum.get(p.id)||0)}</span>
    </div>`;
  el.dataset.panelId = p.id;
  el.addEventListener('click', e => {
    const btn = e.target.closest('[data-action]');
    if (!btn) { recordInteraction(p); return; }
    const action = btn.dataset.action;
    if (action === 'lock') toggleLock(p);
    if (action === 'expand') toggleCompact(p);
    recordInteraction(p);
  });
  el.addEventListener('mouseenter', () => {
    const tip = document.getElementById('tooltip');
    tip.textContent = `${p.title}: ${(p.score*100).toFixed(1)}pts | ${p.interactions} clicks | ${formatViewTime(viewTimeAccum.get(p.id)||0)}`;
    tip.style.opacity = '1';
  });
  el.addEventListener('mousemove', e => {
    const tip = document.getElementById('tooltip');
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top = (e.clientY - 40) + 'px';
  });
  el.addEventListener('mouseleave', () => {
    document.getElementById('tooltip').style.opacity = '0';
  });
  p._el = el;
  p._prevRank = p.rank;
  p._prevCompact = p.compact;
  panelEls.set(p.id, el);
  return el;
}
function formatViewTime(ms) {
  const s = Math.floor(ms / 1000);
  if (s < 60) return s + 's';
  return Math.floor(s/60) + 'm' + (s%60) + 's';
}
function toggleLock(p) {
  p.locked = !p.locked;
  const el = p._el;
  if (!el) return;
  el.classList.toggle('locked', p.locked);
  const btn = el.querySelector('.lock-btn');
  if (btn) btn.classList.toggle('locked-icon', p.locked);
  dirtyLayout = true;
  saveState();
}
function toggleCompact(p) {
  p.locked = true;
  p.compact = !p.compact;
  p.manualPos = p.compact ? 'compact' : 'expanded';
  const el = p._el;
  if (!el) return;
  el.classList.toggle('compact', p.compact);
  const badge = el.querySelector('.rank-badge');
  if (badge) badge.textContent = 'R' + p.rank + (p.compact ? '·C' : '');
  dirtyLayout = true;
  saveState();
}
function recordInteraction(p) {
  lastInteraction = Date.now();
  p.interactions = (p.interactions || 0) + 1;
  p.lastSeen = Date.now();
  const prev = state.tracking.interactions;
  if (typeof prev === 'object' && prev !== null && !(prev instanceof Map)) {
    state.tracking.interactions = new Map(Object.entries(prev));
  }
  if (state.tracking.interactions instanceof Map) {
    state.tracking.interactions.set(p.id, p.interactions);
  }
  dirtyScores = true;
  schedulePoll(true);
}
function setupVisibilityTracking() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver(entries => {
    const now = Date.now();
    let anyChange = false;
    entries.forEach(entry => {
      const id = entry.target.dataset.panelId;
      if (!id) return;
      const wasVisible = visibilityMap.get(id) || false;
      const isVisible = entry.intersectionRatio >= VIEWPORT_VISIBILITY;
      if (isVisible && !wasVisible) {
        visibilityMap.set(id, true);
        (state.tracking.lastSeen || (state.tracking.lastSeen = {}))[id] = now;
        anyChange = true;
      } else if (!isVisible && wasVisible) {
        visibilityMap.set(id, false);
        anyChange = true;
      }
    });
    if (anyChange) lastInteraction = now;
  }, { threshold: [0, VIEWPORT_VISIBILITY] });
  panels.forEach(p => {
    if (p._el) observer.observe(p._el);
  });
}
function accumulateViewTime() {
  const now = Date.now();
  let anyChange = false;
  visibilityMap.forEach((visible, id) => {
    if (visible) {
      const prev = viewTimeAccum.get(id) || 0;
      viewTimeAccum.set(id, prev + 1000);
      const panel = panels.find(p => p.id === id);
      if (panel) panel.lastSeen = now;
      anyChange = true;
    }
  });
  if (anyChange) dirtyScores = true;
}
function schedulePoll(immediate) {
  clearTimeout(pollTimer);
  const interval = immediate ? POLL_INTERVAL_ACTIVE :
    (Date.now() - lastInteraction > IDLE_TIMEOUT) ? POLL_INTERVAL_IDLE : POLL_INTERVAL_ACTIVE;
  pollTimer = setTimeout(pollCycle, interval);
}
function pollCycle() {
  accumulateViewTime();
  if (dirtyScores) rescore();
  if (dirtyLayout || dirtyScores) commitLayout();
  saveState();
  updateStatus();
  schedulePoll(false);
}
function updateStatus() {
  const mode = (Date.now() - lastInteraction > IDLE_TIMEOUT) ? 'idle' : 'active';
  document.getElementById('statusText').textContent = mode + ' · ' + POLL_INTERVAL_ACTIVE/1000 + 's';
}
function init() {
  const grid = document.getElementById('grid');
  const frag = document.createDocumentFragment();
  panels.forEach(p => frag.appendChild(createPanelEl(p)));
  grid.appendChild(frag);
  rescore();
  commitLayout();
  setupVisibilityTracking();
  schedulePoll(false);
  document.getElementById('btnReset').addEventListener('click', () => {
    viewTimeAccum.clear();
    panels.forEach(p => { p.interactions = 0; p.score = 0.5; p.rank = 3; p.compact = false; p.locked = false; p.lastSeen = Date.now(); });
    state = { scores:{}, locks:{}, positions:{}, tracking:{ viewTime:{}, interactions:{}, lastSeen:{} } };
    try { localStorage.removeItem(STORE_KEY); } catch(e) {}
    dirtyLayout = true; dirtyScores = true;
    commitLayout();
    updateStatus();
  });
  document.getElementById('btnLockAll').addEventListener('click', () => {
    const allLocked = panels.every(p => p.locked);
    panels.forEach(p => { p.locked = !allLocked; });
    dirtyLayout = true;
    commitLayout();
    saveState();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      accumulateViewTime();
      saveState();
    } else {
      lastInteraction = Date.now();
      schedulePoll(true);
    }
  });
}
init();
})();
</script>
</body>
</html>