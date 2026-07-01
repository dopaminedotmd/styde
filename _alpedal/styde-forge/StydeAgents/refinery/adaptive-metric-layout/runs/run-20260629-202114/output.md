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
  --surface2: #242836;
  --text: #e1e4ed;
  --text2: #8b90a0;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --border: #2a2e3a;
  --radius: 12px;
  --gap: 12px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
* { box-sizing:border-box; margin:0; padding:0 }
body {
  font-family:system-ui,-apple-system,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  padding:16px
}
header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:16px;
  flex-wrap:wrap;
  gap:8px
}
h1 { font-size:1.25rem; font-weight:600; letter-spacing:-0.02em }
.controls { display:flex; gap:8px; align-items:center; flex-wrap:wrap }
.btn {
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text);
  padding:6px 14px;
  border-radius:8px;
  cursor:pointer;
  font-size:0.8rem;
  transition:var(--transition)
}
.btn:hover { background:var(--border) }
.btn:focus-visible { outline:2px solid var(--accent); outline-offset:2px }
.btn.active { background:var(--accent); border-color:var(--accent); color:#fff }
.grid {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  gap:var(--gap);
  align-items:start
}
.panel {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  overflow:hidden;
  transition:all var(--transition);
  cursor:default;
  position:relative
}
.panel.rank-high { grid-column:span 2; grid-row:span 2; min-height:280px }
.panel.rank-medium { grid-column:span 1; min-height:200px }
.panel.rank-low { grid-column:span 1; min-height:80px }
.panel.compact { min-height:60px }
.panel.compact .panel-body { display:none }
.panel.locked { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent) }
.panel.dragging { opacity:0.6; transform:scale(0.96); z-index:10 }
.panel.drag-target { outline:2px dashed var(--accent); outline-offset:-2px }
.panel-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:10px 14px;
  background:var(--surface2);
  border-bottom:1px solid var(--border);
  gap:8px;
  user-select:none
}
.panel.compact .panel-header { border-bottom:none }
.panel-title { font-size:0.85rem; font-weight:600; letter-spacing:-0.01em; flex:1 }
.panel-rank-badge {
  font-size:0.65rem;
  padding:1px 6px;
  border-radius:4px;
  font-weight:600
}
.panel-rank-badge.high { background:var(--accent2); color:#000 }
.panel-rank-badge.medium { background:var(--warn); color:#000 }
.panel-rank-badge.low { background:var(--surface); color:var(--text2) }
.panel-actions { display:flex; gap:4px }
.icon-btn {
  background:none;
  border:none;
  color:var(--text2);
  cursor:pointer;
  padding:4px;
  border-radius:6px;
  font-size:0.85rem;
  line-height:1;
  transition:var(--transition)
}
.icon-btn:hover { color:var(--text); background:var(--surface) }
.icon-btn:focus-visible { outline:2px solid var(--accent); outline-offset:1px }
.icon-btn.active { color:var(--accent) }
.panel-body { padding:14px }
.metric-value { font-size:1.6rem; font-weight:700; letter-spacing:-0.03em; line-height:1.2 }
.metric-label { font-size:0.7rem; color:var(--text2); margin-top:4px; text-transform:uppercase; letter-spacing:0.05em }
.metric-spark {
  margin-top:10px;
  height:40px;
  background:var(--surface2);
  border-radius:6px;
  overflow:hidden
}
.metric-spark svg { width:100%; height:100% }
.usage-stats {
  display:flex;
  gap:12px;
  margin-top:10px;
  font-size:0.65rem;
  color:var(--text2)
}
.usage-stats span { display:flex; align-items:center; gap:4px }
.usage-dot {
  width:6px; height:6px;
  border-radius:50%;
  display:inline-block
}
.usage-dot.green { background:var(--accent2) }
.usage-dot.yellow { background:var(--warn) }
.usage-dot.gray { background:var(--text2) }
.rank-override-input {
  width:100%;
  margin-top:8px;
  padding:4px 8px;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:6px;
  color:var(--text);
  font-size:0.75rem
}
.rank-override-input:focus { outline:2px solid var(--accent); outline-offset:1px }
.rank-override-input::placeholder { color:var(--text2) }
.more-section {
  margin-top:16px;
  padding:12px;
  background:var(--surface);
  border:1px dashed var(--border);
  border-radius:var(--radius);
  text-align:center
}
.more-section summary {
  cursor:pointer;
  font-size:0.75rem;
  color:var(--text2);
  list-style:none
}
.more-section summary::-webkit-details-marker { display:none }
.more-section summary:focus-visible { outline:2px solid var(--accent); outline-offset:2px }
.more-grid {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  gap:8px;
  margin-top:8px
}
.mini-card {
  background:var(--surface2);
  border-radius:8px;
  padding:10px;
  text-align:left;
  cursor:pointer;
  transition:var(--transition)
}
.mini-card:hover { background:var(--border) }
.mini-card .mini-val { font-size:1rem; font-weight:700 }
.mini-card .mini-label { font-size:0.6rem; color:var(--text2); text-transform:uppercase }
.score-bar {
  height:3px;
  background:var(--surface);
  border-radius:2px;
  margin-top:8px;
  overflow:hidden
}
.score-bar-fill {
  height:100%;
  border-radius:2px;
  transition:width 0.5s var(--transition)
}
.score-bar-fill.high { background:var(--accent2) }
.score-bar-fill.medium { background:var(--warn) }
.score-bar-fill.low { background:var(--text2) }
.a11y-announce {
  position:absolute;
  width:1px;height:1px;
  overflow:hidden;
  clip:rect(0,0,0,0);
  white-space:nowrap
}
@media (max-width:640px) {
  .grid { grid-template-columns:1fr }
  .panel.rank-high { grid-column:span 1; grid-row:span 1 }
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnReset" aria-label="Reset layout to default">Reset</button>
    <button class="btn" id="btnAuto" aria-label="Toggle auto-layout">Auto: ON</button>
    <button class="btn" id="btnCompact" aria-label="Toggle compact all low-rank panels">Compact Low</button>
    <span style="font-size:0.7rem;color:var(--text2)">Session: <span id="sessionTimer">0s</span></span>
  </div>
</header>
<div class="grid" id="grid" role="list" aria-label="Dashboard panels"></div>
<details class="more-section" id="moreSection" style="display:none">
  <summary aria-label="Show hidden low-usage panels">More panels ▸</summary>
  <div class="more-grid" id="moreGrid"></div>
</details>
<div class="a11y-announce" id="a11y" aria-live="polite"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v2';
const TICK_MS = 5000;
const DECAY_HALF_LIFE = 300000;
const RANK_HIGH = 75;
const RANK_MEDIUM = 50;
const PANEL_DEFS = [
  { id:'cpu',      title:'CPU Usage',        icon:'⚙', val:42, unit:'%',   spark:[30,45,55,42,38,50,48,42] },
  { id:'memory',   title:'Memory',            icon:'🧠', val:68, unit:'%',   spark:[60,62,65,70,68,72,68] },
  { id:'requests', title:'Requests/s',        icon:'📡', val:1240,unit:'/s', spark:[800,950,1100,1300,1240,1180,1240] },
  { id:'errors',   title:'Error Rate',        icon:'❌', val:2.3, unit:'%',  spark:[1.5,2.1,1.8,2.5,2.3,2.0,2.3] },
  { id:'latency',  title:'P95 Latency',       icon:'⏱', val:142, unit:'ms', spark:[120,135,150,145,142,138,142] },
  { id:'storage',  title:'Disk I/O',          icon:'💾', val:78,  unit:'%',  spark:[60,65,70,75,78,76,78] },
  { id:'cache',    title:'Cache Hit Rate',    icon:'🎯', val:94,  unit:'%',  spark:[90,92,93,95,94,93,94] },
  { id:'users',    title:'Active Users',      icon:'👥', val:342, unit:'',   spark:[200,250,300,320,340,342,342] }
];
let panels = [];
let stateVersion = 0;
let autoLayout = true;
let dragState = null;
let sessionStart = Date.now();
let prevSnapshot = '';
const $ = (s,d) => (d||document).querySelector(s);
const $$ = (s,d) => (d||document).querySelectorAll(s);
const a11y = (msg) => { const e=$('#a11y'); e.textContent=''; e.textContent=msg; };
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return null;
}
function saveState() {
  const data = {
    panels: panels.map(p => ({
      id:p.id, locked:p.locked, rankOverride:p.rankOverride,
      compactForced:p.compactForced, order:p.order,
      score:p.score, viewMs:p.viewMs, interactions:p.interactions, lastInteraction:p.lastInteraction,
      collapsed:p.collapsed
    })),
    autoLayout
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
function computeScore(p) {
  const now = Date.now();
  const recencyMs = now - p.lastInteraction;
  const recencyWeight = Math.pow(0.5, recencyMs / DECAY_HALF_LIFE);
  const freqWeight = Math.log2(p.interactions + 2);
  const durWeight = Math.log2((p.viewMs / 1000) + 2);
  return Math.round(freqWeight * durWeight * recencyWeight * 10);
}
function getTier(score) {
  if (score >= RANK_HIGH) return 'high';
  if (score >= RANK_MEDIUM) return 'medium';
  return 'low';
}
function initPanels() {
  const saved = loadState();
  PANEL_DEFS.forEach((def,i) => {
    const savedP = saved?.panels?.find(sp => sp.id === def.id);
    panels.push({
      id:def.id, title:def.title, icon:def.icon,
      val:def.val, unit:def.unit, spark:def.spark.slice(),
      score:savedP?.score ?? (50 - i * 5),
      viewMs:savedP?.viewMs ?? 0,
      interactions:savedP?.interactions ?? 0,
      lastInteraction:savedP?.lastInteraction ?? (Date.now() - (PANEL_DEFS.length - i) * 60000),
      locked:savedP?.locked ?? false,
      rankOverride:savedP?.rankOverride ?? null,
      compactForced:savedP?.compactForced ?? false,
      collapsed:savedP?.collapsed ?? false,
      order:savedP?.order ?? i,
      visible:true
    });
  });
  if (saved?.autoLayout !== undefined) autoLayout = saved.autoLayout;
  sortPanels();
}
function sortPanels() {
  panels.sort((a,b) => {
    if (a.rankOverride !== null && b.rankOverride !== null) return a.rankOverride - b.rankOverride;
    if (a.rankOverride !== null) return -1;
    if (b.rankOverride !== null) return 1;
    return b.score - a.score;
  });
  panels.forEach((p,i) => { p.order = i; });
}
function rankClass(p) {
  if (p.rankOverride !== null) {
    if (p.rankOverride >= RANK_HIGH) return 'high';
    if (p.rankOverride >= RANK_MEDIUM) return 'medium';
    return 'low';
  }
  return getTier(p.score);
}
function isCompact(p) {
  if (p.compactForced) return true;
  if (p.locked) return false;
  if (p.rankOverride !== null) {
    return p.rankOverride < RANK_MEDIUM;
  }
  return getTier(p.score) === 'low';
}
function panelSnapshot() {
  return panels.map(p => `${p.id}|${p.order}|${rankClass(p)}|${isCompact(p)?1:0}|${p.locked?1:0}|${p.val}|${p.score}|${p.collapsed?1:0}`).join(',');
}
function patchDOM() {
  const snap = panelSnapshot();
  if (snap === prevSnapshot) return;
  const prevParts = prevSnapshot ? prevSnapshot.split(',') : [];
  const curParts = snap.split(',');
  prevSnapshot = snap;
  const grid = $('#grid');
  const moreGrid = $('#moreGrid');
  const moreSection = $('#moreSection');
  let hasHidden = false;
  const wantedIds = new Set();
  const currentEls = {};
  $$('.panel', grid).forEach(el => { currentEls[el.dataset.pid] = el; });
  $$('.mini-card', moreGrid).forEach(el => { currentEls[el.dataset.pid] = el; });
  panels.forEach((p,i) => {
    wantedIds.add(p.id);
    const tier = rankClass(p);
    const compact = isCompact(p);
    const hidden = p.collapsed && !p.locked;
    if (hidden) { hasHidden = true; }
    const key = `${p.id}|${p.order}|${tier}|${compact?1:0}|${p.locked?1:0}|${p.val}|${p.score}|${p.collapsed?1:0}`;
    const prevKey = prevParts[i] || '';
    if (!currentEls[p.id] || key !== prevKey) {
      if (currentEls[p.id]) currentEls[p.id].remove();
      const el = hidden ? buildMiniCard(p,tier) : buildPanel(p,tier,compact);
      if (hidden) {
        moreGrid.appendChild(el);
      } else {
        grid.appendChild(el);
      }
    } else {
      const el = currentEls[p.id];
      if (!hidden && el.parentElement === moreGrid) {
        grid.appendChild(el);
      } else if (hidden && el.parentElement === grid) {
        moreGrid.appendChild(el);
      }
      updatePanelData(el, p, tier, compact, hidden);
    }
  });
  Object.keys(currentEls).forEach(id => {
    if (!wantedIds.has(id)) currentEls[id].remove();
  });
  moreSection.style.display = hasHidden ? '' : 'none';
}
function updatePanelData(el, p, tier, compact, hidden) {
  if (hidden) {
    const mv = el.querySelector('.mini-val');
    if (mv && mv.textContent !== p.icon+' '+p.val+p.unit) mv.textContent = p.icon+' '+p.val+p.unit;
    const ml = el.querySelector('.mini-label');
    if (ml && ml.textContent !== p.title) ml.textContent = p.title;
    const sf = el.querySelector('.score-bar-fill');
    if (sf) { sf.style.width = Math.min(p.score,100)+'%'; sf.className = 'score-bar-fill '+tier; }
    return;
  }
  if (compact) {
    const mv = el.querySelector('.metric-value');
    if (mv && mv.textContent !== p.icon+' '+p.val+p.unit) mv.textContent = p.icon+' '+p.val+p.unit;
  } else {
    const mv = el.querySelector('.metric-value');
    if (mv && mv.textContent !== p.val+p.unit) mv.textContent = p.val+p.unit;
    const sparkEl = el.querySelector('.metric-spark');
    if (sparkEl) {
      const svg = sparkEl.querySelector('svg');
      if (svg) {
        const polyline = svg.querySelector('polyline');
        const maxV = Math.max(...p.spark, 1);
        const pts = p.spark.map((v,i) => `${(i/(p.spark.length-1))*100},${100-(v/maxV)*100}`).join(' ');
        if (polyline && polyline.getAttribute('points') !== pts) {
          polyline.setAttribute('points', pts);
        }
      }
    }
  }
  const badge = el.querySelector('.panel-rank-badge');
  if (badge) {
    const newText = tier.toUpperCase();
    const newClass = 'panel-rank-badge '+tier;
    if (badge.textContent !== newText || badge.className !== newClass) {
      badge.textContent = newText;
      badge.className = newClass;
    }
  }
  el.className = 'panel rank-'+tier + (compact?' compact':'') + (p.locked?' locked':'');
  el.style.order = p.order;
}
function buildPanel(p, tier, compact) {
  const el = document.createElement('div');
  el.className = 'panel rank-'+tier + (compact?' compact':'') + (p.locked?' locked':'');
  el.dataset.pid = p.id;
  el.setAttribute('role','listitem');
  el.setAttribute('aria-label',p.title+' - '+tier+' priority');
  el.setAttribute('tabindex','0');
  el.style.order = p.order;
  const sparkSvg = compact ? '' : buildSparkSVG(p.spark);
  el.innerHTML =
    '<div class="panel-header">'+
      '<span class="panel-title">'+esc(p.icon+' '+p.title)+'</span>'+
      '<span class="panel-rank-badge '+tier+'">'+tier.toUpperCase()+'</span>'+
      '<div class="panel-actions">'+
        '<button class="icon-btn btn-lock'+(p.locked?' active':'')+'" aria-label="'+(p.locked?'Unlock':'Lock')+' panel position" title="'+(p.locked?'Unlock':'Lock')+'">'+(p.locked?'🔒':'🔓')+'</button>'+
        '<button class="icon-btn btn-compact'+(p.compactForced?' active':'')+'" aria-label="Toggle compact mode" title="Compact">⊟</button>'+
        '<button class="icon-btn btn-collapse" aria-label="'+(p.collapsed?'Show':'Hide')+' panel" title="'+(p.collapsed?'Show':'Hide')+'">'+(p.collapsed?'👁':'⊖')+'</button>'+
        '<button class="icon-btn btn-drag" aria-label="Reorder panel (Space to grab, arrows to move)" title="Drag to reorder">⋮⋮</button>'+
      '</div>'+
    '</div>'+
    '<div class="panel-body">'+
      '<div class="metric-value">'+(compact?p.icon+' '+p.val+p.unit:p.val+p.unit)+'</div>'+
      '<div class="metric-label">'+esc(p.title)+'</div>'+
      sparkSvg+
      '<div class="usage-stats">'+
        '<span>👁 '+fmtDuration(p.viewMs)+'</span>'+
        '<span>🖱 '+p.interactions+'</span>'+
        '<span>📊 '+p.score+'pts</span>'+
      '</div>'+
      '<input type="number" class="rank-override-input" placeholder="Rank override (0-100)" value="'+(p.rankOverride!==null?p.rankOverride:'')+'" aria-label="Manual rank override">'+
    '</div>';
  el.addEventListener('click', () => recordInteraction(p));
  el.addEventListener('mouseenter', () => recordInteraction(p));
  el.querySelector('.btn-lock').addEventListener('click', e => { e.stopPropagation(); toggleLock(p); });
  el.querySelector('.btn-compact').addEventListener('click', e => { e.stopPropagation(); toggleCompact(p); });
  el.querySelector('.btn-collapse').addEventListener('click', e => { e.stopPropagation(); toggleCollapse(p); });
  el.querySelector('.btn-drag').addEventListener('click', e => { e.stopPropagation(); startDrag(p,el); });
  el.querySelector('.btn-drag').addEventListener('keydown', e => { if(e.key===' '||e.key==='Enter'){e.preventDefault();e.stopPropagation();startDrag(p,el);} });
  el.addEventListener('keydown', e => keyboardDrag(e,p,el));
  el.querySelector('.rank-override-input').addEventListener('input', e => {
    const v = parseInt(e.target.value,10);
    p.rankOverride = isNaN(v) ? null : Math.max(0,Math.min(100,v));
    if (!isNaN(v)) p.locked = true;
    sortPanels();
    requestRender();
  });
  el.querySelector('.rank-override-input').addEventListener('click', e => e.stopPropagation());
  el.querySelector('.rank-override-input').addEventListener('keydown', e => e.stopPropagation());
  return el;
}
function buildMiniCard(p, tier) {
  const el = document.createElement('div');
  el.className = 'mini-card';
  el.dataset.pid = p.id;
  el.setAttribute('tabindex','0');
  el.setAttribute('role','button');
  el.setAttribute('aria-label','Restore '+p.title+' panel');
  el.innerHTML =
    '<div class="mini-val">'+esc(p.icon+' '+p.val+p.unit)+'</div>'+
    '<div class="mini-label">'+esc(p.title)+'</div>'+
    '<div class="score-bar"><div class="score-bar-fill '+tier+'" style="width:'+Math.min(p.score,100)+'%"></div></div>';
  el.addEventListener('click', () => {
    p.collapsed = false;
    sortPanels();
    requestRender();
  });
  return el;
}
function buildSparkSVG(data) {
  const maxV = Math.max(...data,1);
  const pts = data.map((v,i) => `${(i/(data.length-1))*100},${100-(v/maxV)*100}`).join(' ');
  return '<div class="metric-spark"><svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="'+pts+'" fill="none" stroke="var(--accent)" stroke-width="2" vector-effect="non-scaling-stroke"/></svg></div>';
}
function recordInteraction(p) {
  p.interactions++;
  p.lastInteraction = Date.now();
  p.score = computeScore(p);
  sortPanels();
  requestRender();
}
function toggleLock(p) {
  p.locked = !p.locked;
  if (p.locked) p.rankOverride = p.rankOverride ?? p.score;
  else { p.rankOverride = null; }
  sortPanels();
  a11y(p.title + (p.locked ? ' locked' : ' unlocked'));
  requestRender();
}
function toggleCompact(p) {
  p.compactForced = !p.compactForced;
  a11y(p.title + (p.compactForced ? ' compacted' : ' expanded'));
  requestRender();
}
function toggleCollapse(p) {
  p.collapsed = !p.collapsed;
  a11y(p.title + (p.collapsed ? ' hidden' : ' shown'));
  requestRender();
}
function startDrag(p, el) {
  if (dragState) { endDrag(); return; }
  dragState = { panel:p, el:el, originalOrder:p.order };
  el.classList.add('dragging');
  a11y('Grabbed '+p.title+'. Use arrow keys to reposition, Space or Escape to drop.');
}
function endDrag() {
  if (!dragState) return;
  dragState.el.classList.remove('dragging');
  a11y(dragState.panel.title + ' placed at position ' + (dragState.panel.order+1));
  dragState = null;
  sortPanels();
  requestRender();
}
function moveDragged(dir) {
  if (!dragState) return;
  const idx = dragState.panel.order;
  const newIdx = Math.max(0, Math.min(panels.length-1, idx+dir));
  if (newIdx === idx) return;
  const other = panels.find(p => p.order === newIdx);
  if (other) other.order = idx;
  dragState.panel.order = newIdx;
  dragState.panel.locked = true;
  dragState.panel.rankOverride = dragState.panel.rankOverride ?? dragState.panel.score;
  sortPanels();
  requestRender();
}
function keyboardDrag(e, p, el) {
  if (!dragState || dragState.panel.id !== p.id) return;
  if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); moveDragged(-1); }
  else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); moveDragged(1); }
  else if (e.key === ' ' || e.key === 'Escape') { e.preventDefault(); endDrag(); }
}
let renderPending = false;
function requestRender() {
  if (renderPending) return;
  renderPending = true;
  requestAnimationFrame(() => {
    patchDOM();
    saveState();
    renderPending = false;
    stateVersion++;
  });
}
function fmtDuration(ms) {
  if (ms < 60000) return Math.round(ms/1000)+'s';
  if (ms < 3600000) return Math.round(ms/60000)+'m';
  return Math.round(ms/3600000)+'h';
}
function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
let viewObserver;
function setupViewTracking() {
  viewObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const pid = entry.target.dataset.pid;
      const p = panels.find(px => px.id === pid);
      if (!p) return;
      if (entry.isIntersecting) {
        entry.target._viewStart = Date.now();
      } else if (entry.target._viewStart) {
        p.viewMs += Date.now() - entry.target._viewStart;
        entry.target._viewStart = null;
        p.score = computeScore(p);
      }
    });
  }, { threshold: 0.5 });
  const attachObserver = () => {
    $$('.panel').forEach(el => viewObserver.observe(el));
  };
  const mo = new MutationObserver(attachObserver);
  mo.observe($('#grid'), { childList:true, subtree:true });
  attachObserver();
}
function tickSimulation() {
  panels.forEach(p => {
    const def = PANEL_DEFS.find(d => d.id === p.id);
    if (!def) return;
    const delta = (Math.random() - 0.5) * 0.1 * def.val;
    p.val = Math.round((p.val + delta) * 10) / 10;
    p.spark.push(p.val);
    if (p.spark.length > 20) p.spark.shift();
  });
  requestRender();
}
function refreshScores() {
  const now = Date.now();
  panels.forEach(p => {
    if (viewObserver) {
      const el = document.querySelector('[data-pid="'+p.id+'"]');
      if (el && el._viewStart) {
        p.viewMs += now - el._viewStart;
        el._viewStart = now;
      }
    }
    p.score = computeScore(p);
  });
  sortPanels();
  requestRender();
}
const periodicTasks = (function() {
  let tickId, scoreId, sessionId;
  return {
    start() {
      tickId = setInterval(tickSimulation, TICK_MS);
      scoreId = setInterval(refreshScores, 30000);
      sessionId = setInterval(() => {
        const elapsed = Math.round((Date.now()-sessionStart)/1000);
        const el = $('#sessionTimer');
        if (el) el.textContent = elapsed >= 3600 ? Math.round(elapsed/3600)+'h' : elapsed >= 60 ? Math.round(elapsed/60)+'m' : elapsed+'s';
      }, 10000);
    },
    stop() {
      clearInterval(tickId);
      clearInterval(scoreId);
      clearInterval(sessionId);
    }
  };
})();
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && dragState) { e.preventDefault(); endDrag(); }
});
document.addEventListener('click', e => {
  if (dragState && !e.target.closest('[data-pid="'+dragState.panel.id+'"]')) {
    endDrag();
  }
});
$('#btnReset').addEventListener('click', () => {
  localStorage.removeItem(STORAGE_KEY);
  panels = [];
  initPanels();
  prevSnapshot = '';
  a11y('Layout reset to defaults');
  requestRender();
});
$('#btnAuto').addEventListener('click', function() {
  autoLayout = !autoLayout;
  this.textContent = 'Auto: ' + (autoLayout ? 'ON' : 'OFF');
  this.classList.toggle('active', autoLayout);
  if (autoLayout) { panels.forEach(p => { if(!p.locked) p.rankOverride = null; }); sortPanels(); requestRender(); }
  a11y('Auto-layout ' + (autoLayout ? 'enabled' : 'disabled'));
});
$('#btnCompact').addEventListener('click', function() {
  const allLow = panels.every(p => isCompact(p) || p.collapsed || (getTier(p.score)!=='low'));
  panels.forEach(p => {
    if (getTier(p.score) === 'low' && !p.locked) p.compactForced = !allLow;
  });
  a11y(allLow ? 'Low-rank panels expanded' : 'Low-rank panels compacted');
  requestRender();
});
initPanels();
patchDOM();
prevSnapshot = panelSnapshot();
setupViewTracking();
periodicTasks.start();
})();
</script>
</body>
</html>