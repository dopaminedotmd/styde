<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117; --panel-bg: #1a1d2e; --text: #e0e0e0; --muted: #8888aa;
  --accent: #6c5ce7; --accent2: #00cec9; --warn: #fdcb6e; --danger: #ff7675;
  --border: #2a2d3e; --shadow: 0 4px 24px rgba(0,0,0,0.4);
  --radius: 10px; --gap: 12px; --compact-ratio: 0.35;
  --transition-speed: 0.4s;
}
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  overflow-x: hidden;
}
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 24px; background: #141725; border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100; backdrop-filter: blur(10px);
}
.header h1 { font-size: 1.3rem; font-weight: 600; letter-spacing: 0.02em; }
.header-actions { display: flex; gap: 10px; align-items: center; }
.btn {
  padding: 7px 16px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--panel-bg); color: var(--text); cursor: pointer;
  font-size: 0.82rem; transition: all 0.2s; white-space: nowrap;
}
.btn:hover { border-color: var(--accent); background: #252840; }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.btn.danger { border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: var(--danger); color: #fff; }
.dashboard {
  display: grid; gap: var(--gap); padding: 20px;
  transition: opacity var(--transition-speed);
  opacity: 1;
}
.dashboard.dirty { opacity: 0.85; }
.panel {
  background: var(--panel-bg); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow);
  overflow: hidden; position: relative; cursor: grab;
  transition: transform 0.25s, box-shadow 0.25s;
  min-height: 160px; display: flex; flex-direction: column;
}
.panel.dragging { cursor: grabbing; transform: scale(1.02); box-shadow: 0 8px 32px rgba(108,92,231,0.3); z-index: 50; }
.panel.compact { opacity: 0.7; }
.panel.compact .panel-body { display: none; }
.panel.compact .compact-preview { display: flex; }
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: '🔒'; position: absolute; top: 6px; right: 36px;
  font-size: 0.7rem; opacity: 0.8; z-index: 5;
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; font-size: 0.85rem; font-weight: 600;
  border-bottom: 1px solid var(--border); user-select: none;
  background: linear-gradient(135deg, rgba(108,92,231,0.08), transparent);
}
.panel-header .title { display: flex; align-items: center; gap: 8px; }
.panel-header .rank-badge {
  font-size: 0.65rem; padding: 2px 8px; border-radius: 10px;
  background: rgba(108,92,231,0.2); color: var(--accent2); font-weight: 700;
}
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none; border: none; color: var(--muted); cursor: pointer;
  font-size: 0.85rem; padding: 3px 6px; border-radius: 4px; line-height: 1;
}
.panel-actions button:hover { color: var(--text); background: rgba(255,255,255,0.06); }
.panel-body { padding: 14px; flex: 1; }
.compact-preview { display: none; padding: 14px; font-size: 0.78rem; color: var(--muted); align-items: center; gap: 8px; }
.compact-preview .spark { flex: 1; height: 28px; background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent)); opacity: 0.3; border-radius: 4px; }
.metric-value { font-size: 2rem; font-weight: 700; color: var(--accent2); line-height: 1.1; }
.metric-label { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.metric-change { font-size: 0.75rem; margin-top: 4px; }
.metric-change.up { color: #00b894; }
.metric-change.down { color: var(--danger); }
.chart-area {
  width: 100%; height: 60px; margin-top: 10px;
  display: flex; align-items: flex-end; gap: 3px;
}
.chart-area .bar {
  flex: 1; background: var(--accent); border-radius: 2px 2px 0 0;
  min-height: 4px; opacity: 0.6; transition: height 0.5s;
}
.stats-row { display: flex; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
.stat-pill {
  padding: 5px 10px; border-radius: 14px; font-size: 0.7rem;
  background: rgba(255,255,255,0.04); color: var(--muted);
}
.stat-pill strong { color: var(--text); }
.drag-hint {
  position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; background: rgba(15,17,23,0.85); opacity: 0;
  pointer-events: none; transition: opacity 0.3s; font-size: 0.8rem;
  color: var(--accent2); z-index: 10;
}
.panel:hover .drag-hint:not(.hidden) { opacity: 1; }
.more-section {
  margin-top: 8px; padding: 14px 20px 20px;
}
.more-toggle {
  background: var(--panel-bg); border: 1px dashed var(--border);
  border-radius: var(--radius); padding: 10px 18px; cursor: pointer;
  text-align: center; color: var(--muted); font-size: 0.82rem;
  transition: all 0.2s;
}
.more-toggle:hover { border-color: var(--accent); color: var(--text); }
.more-panels { display: none; margin-top: var(--gap); }
.more-panels.open { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: var(--gap); }
.more-panels .panel { transform: scale(0.95); }
.toast {
  position: fixed; bottom: 24px; right: 24px; z-index: 200;
  padding: 10px 20px; background: #252840; border: 1px solid var(--accent);
  border-radius: 8px; font-size: 0.8rem; opacity: 0; transform: translateY(10px);
  transition: all 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
@media (max-width: 600px) {
  .dashboard { grid-template-columns: 1fr !important; padding: 10px; }
  .header { flex-direction: column; gap: 8px; padding: 10px 14px; }
  .panel { min-height: 120px; }
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset Data</button>
    <button class="btn" id="btnAutoLayout" title="Force re-rank and re-layout">Auto-Layout</button>
    <button class="btn danger" id="btnClearStorage" title="Clear localStorage">Clear Storage</button>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection" style="display:none">
  <div class="more-toggle" id="moreToggle">+ More panels</div>
  <div class="more-panels" id="morePanels"></div>
</div>
<div class="toast" id="toast"></div>
<script>
(function() {
'use strict';
// ---- Seeded PRNG (mulberry32) ----
function mulberry32(a) {
  return function() { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
// ---- Constants ----
const STORAGE_KEY = 'adaptive_dashboard_v1';
const COMPACT_THRESHOLD = 0.25;
const MORE_THRESHOLD = 0.12;
const DECAY_HALF_LIFE_DAYS = 7;
const DECAY_LAMBDA = Math.log(2) / (DECAY_HALF_LIFE_DAYS * 86400000);
const PANEL_DEFAULTS = [
  { id: 'revenue', title: 'Revenue', icon: '💰', value: 0, unit: 'kr', color: '#00cec9' },
  { id: 'users', title: 'Active Users', icon: '👥', value: 0, unit: '', color: '#6c5ce7' },
  { id: 'conversion', title: 'Conversion', icon: '📈', value: 0, unit: '%', color: '#00b894' },
  { id: 'bounce', title: 'Bounce Rate', icon: '↩️', value: 0, unit: '%', color: '#ff7675' },
  { id: 'latency', title: 'API Latency', icon: '⚡', value: 0, unit: 'ms', color: '#fdcb6e' },
  { id: 'errors', title: 'Error Rate', icon: '🚨', value: 0, unit: '%', color: '#d63031' },
  { id: 'storage', title: 'Storage', icon: '💾', value: 0, unit: 'GB', color: '#a29bfe' },
  { id: 'bandwidth', title: 'Bandwidth', icon: '🌐', value: 0, unit: 'Mbps', color: '#55efc4' },
];
// ---- State ----
var state = {
  panels: {},
  order: [],
  overrides: {},
  lastLayout: '',
  dirty: false,
  changeFlags: {}
};
// ---- DOM Cache ----
var dom = {};
function cacheDom() {
  dom.dashboard = document.getElementById('dashboard');
  dom.moreSection = document.getElementById('moreSection');
  dom.moreToggle = document.getElementById('moreToggle');
  dom.morePanels = document.getElementById('morePanels');
  dom.toast = document.getElementById('toast');
  dom.panelEls = {};
}
// ---- Panel tracking ----
function now() { return Date.now(); }
function getPanelData(panelId) {
  return state.panels[panelId];
}
function initPanelData(panelId) {
  if (!state.panels[panelId]) {
    state.panels[panelId] = {
      views: 0,
      totalDuration: 0,
      lastViewed: 0,
      interactions: 0,
      expanded: true,
      locked: false,
      collapsedManually: false,
      viewStart: 0,
      score: 0,
      rank: 0
    };
  }
}
function startView(panelId) {
  initPanelData(panelId);
  var p = state.panels[panelId];
  if (!p.viewStart) p.viewStart = now();
}
function endView(panelId) {
  var p = getPanelData(panelId);
  if (!p) return;
  if (p.viewStart) {
    p.totalDuration += now() - p.viewStart;
    p.viewStart = 0;
  }
}
function recordInteraction(panelId) {
  initPanelData(panelId);
  state.panels[panelId].interactions++;
  state.panels[panelId].lastViewed = now();
  state.changeFlags[panelId] = true;
  markDirty();
}
// ---- Scoring ----
function computeScore(panelId) {
  var p = getPanelData(panelId);
  if (!p) return 0;
  var age = now() - p.lastViewed;
  if (age < 0) age = 0;
  var recencyWeight = Math.exp(-DECAY_LAMBDA * age);
  var durationMinutes = p.totalDuration / 60000;
  var freq = p.views + p.interactions;
  var score = (freq * 0.4 + durationMinutes * 0.4 + recencyWeight * 10 * 0.2);
  return score;
}
function recomputeAllScores() {
  var scores = [];
  for (var id in state.panels) {
    var s = computeScore(id);
    state.panels[id].score = s;
    scores.push({ id: id, score: s });
  }
  scores.sort(function(a, b) { return b.score - a.score; });
  var maxScore = scores.length > 0 ? scores[0].score : 1;
  for (var i = 0; i < scores.length; i++) {
    state.panels[scores[i].id].rank = i + 1;
    state.panels[scores[i].id].scoreNorm = maxScore > 0 ? scores[i].score / maxScore : 0;
  }
  state.order = scores.map(function(s) { return s.id; });
}
// ---- Layout engine ----
function computeLayout() {
  recomputeAllScores();
  var maxScore = 0;
  for (var id in state.panels) {
    if (state.panels[id].scoreNorm > maxScore) maxScore = state.panels[id].scoreNorm;
  }
  if (maxScore === 0) maxScore = 1;
  var visibleCount = 0;
  var moreIds = [];
  var panelInfos = [];
  for (var i = 0; i < state.order.length; i++) {
    var id = state.order[i];
    var p = state.panels[id];
    var scoreNorm = p.scoreNorm;
    var locked = state.overrides[id] ? state.overrides[id].locked : false;
    p.locked = locked || p.locked;
    if (scoreNorm < MORE_THRESHOLD && !locked) {
      moreIds.push(id);
    } else {
      panelInfos.push({ id: id, scoreNorm: scoreNorm, locked: locked, rank: i + 1 });
      visibleCount++;
    }
  }
  // Determine columns based on visible count
  var cols = visibleCount <= 2 ? visibleCount : visibleCount <= 4 ? 2 : visibleCount <= 6 ? 3 : 4;
  // Build grid-template string with weighted columns
  var totalWeight = 0;
  for (var j = 0; j < panelInfos.length; j++) {
    totalWeight += panelInfos[j].scoreNorm;
  }
  if (totalWeight === 0) totalWeight = panelInfos.length;
  var colFractions = [];
  for (var k = 0; k < panelInfos.length; k++) {
    var frac = Math.max(0.5, panelInfos[k].scoreNorm / totalWeight * panelInfos.length);
    colFractions.push(frac.toFixed(2) + 'fr');
  }
  var layoutKey = panelInfos.map(function(pi) { return pi.id; }).join(',') + '|cols=' + cols;
  return {
    panels: panelInfos,
    moreIds: moreIds,
    cols: cols,
    colFractions: colFractions,
    layoutKey: layoutKey
  };
}
// ---- Rendering ----
var layoutVersion = 0;
var renderScheduled = false;
var lastRenderedLayoutKey = '';
function markDirty() {
  state.dirty = true;
  scheduleRender();
}
function scheduleRender() {
  if (renderScheduled) return;
  renderScheduled = true;
  requestAnimationFrame(function() {
    renderScheduled = false;
    if (state.dirty || lastRenderedLayoutKey !== state.lastLayout) {
      renderDashboard();
    }
  });
}
function renderDashboard() {
  var layout = computeLayout();
  if (layout.layoutKey === lastRenderedLayoutKey && !state.dirty) return;
  lastRenderedLayoutKey = layout.layoutKey;
  state.lastLayout = layout.layoutKey;
  state.dirty = false;
  layoutVersion++;
  var dash = dom.dashboard;
  // Build grid
  var gridCols = 'repeat(' + layout.cols + ', 1fr)';
  dash.style.gridTemplateColumns = gridCols;
  // Track existing elements
  var existingEls = {};
  var children = dash.children;
  for (var i = 0; i < children.length; i++) {
    existingEls[children[i].dataset.panelId] = children[i];
  }
  var fragment = document.createDocumentFragment();
  var newDomMap = {};
  // Render visible panels in rank order
  for (var j = 0; j < layout.panels.length; j++) {
    var info = layout.panels[j];
    var id = info.id;
    var panelData = state.panels[id];
    var isCompact = info.scoreNorm < COMPACT_THRESHOLD && !info.locked;
    var el = existingEls[id];
    if (!el || el.dataset.layoutVersion !== String(layoutVersion)) {
      el = createPanelElement(id, panelData, info, isCompact);
    } else {
      updatePanelElement(el, id, panelData, info, isCompact);
    }
    el.dataset.layoutVersion = layoutVersion;
    el.dataset.rank = info.rank;
    newDomMap[id] = el;
    fragment.appendChild(el);
  }
  dash.innerHTML = '';
  dash.appendChild(fragment);
  dom.panelEls = newDomMap;
  // More section
  if (layout.moreIds.length > 0) {
    dom.moreSection.style.display = 'block';
    dom.moreToggle.textContent = '+ ' + layout.moreIds.length + ' more panel' + (layout.moreIds.length > 1 ? 's' : '');
    renderMorePanels(layout.moreIds);
  } else {
    dom.moreSection.style.display = 'none';
  }
  // Re-attach observers
  attachObservers();
  setupDragHandlers();
  // Persist
  saveState();
  // Log
  console.log('[Layout v' + layoutVersion + '] cols=' + layout.cols + ' visible=' + layout.panels.length + ' more=' + layout.moreIds.length);
}
function createPanelElement(id, panelData, info, isCompact) {
  var defaults = PANEL_DEFAULTS.find(function(d) { return d.id === id; }) || { title: id, icon: '📊', value: 0, unit: '', color: '#6c5ce7' };
  var value = generateValue(id, defaults);
  var change = generateTrend(id);
  var changeClass = change >= 0 ? 'up' : 'down';
  var changeSymbol = change >= 0 ? '▲' : '▼';
  var barsHtml = generateBars(id, 12);
  var el = document.createElement('div');
  el.className = 'panel' + (isCompact ? ' compact' : '') + (info.locked ? ' locked' : '');
  el.dataset.panelId = id;
  el.draggable = true;
  el.innerHTML =
    '<div class="panel-header">' +
      '<span class="title">' + defaults.icon + ' ' + defaults.title + ' <span class="rank-badge">#' + info.rank + '</span></span>' +
      '<div class="panel-actions">' +
        '<button class="btn-lock" title="' + (info.locked ? 'Unlock' : 'Lock') + ' position">' + (info.locked ? '🔓' : '🔒') + '</button>' +
        '<button class="btn-pin" title="Pin to top">📌</button>' +
      '</div>' +
    '</div>' +
    '<div class="compact-preview">' +
      '<span>' + defaults.icon + ' ' + defaults.title + '</span>' +
      '<span style="font-weight:600;color:' + defaults.color + '">' + formatValue(value, defaults.unit) + '</span>' +
      '<div class="spark" style="width:' + (info.scoreNorm * 100).toFixed(0) + '%"></div>' +
    '</div>' +
    '<div class="panel-body">' +
      '<div class="metric-label">' + defaults.title + '</div>' +
      '<div class="metric-value" style="color:' + defaults.color + '">' + formatValue(value, defaults.unit) + '</div>' +
      '<div class="metric-change ' + changeClass + '">' + changeSymbol + ' ' + Math.abs(change).toFixed(1) + '% vs last period</div>' +
      '<div class="chart-area">' + barsHtml + '</div>' +
      '<div class="stats-row">' +
        '<span class="stat-pill">Views: <strong>' + panelData.views + '</strong></span>' +
        '<span class="stat-pill">Time: <strong>' + formatDuration(panelData.totalDuration) + '</strong></span>' +
        '<span class="stat-pill">Score: <strong>' + panelData.scoreNorm.toFixed(2) + '</strong></span>' +
      '</div>' +
    '</div>' +
    '<div class="drag-hint">Drag to reorder · Double-click to lock</div>';
  return el;
}
function updatePanelElement(el, id, panelData, info, isCompact) {
  var defaults = PANEL_DEFAULTS.find(function(d) { return d.id === id; }) || { title: id, icon: '📊', value: 0, unit: '', color: '#6c5ce7' };
  var value = generateValue(id, defaults);
  var change = generateTrend(id);
  var changeClass = change >= 0 ? 'up' : 'down';
  var changeSymbol = change >= 0 ? '▲' : '▼';
  el.className = 'panel' + (isCompact ? ' compact' : '') + (info.locked ? ' locked' : '');
  var rankBadge = el.querySelector('.rank-badge');
  if (rankBadge) rankBadge.textContent = '#' + info.rank;
  var lockBtn = el.querySelector('.btn-lock');
  if (lockBtn) lockBtn.textContent = info.locked ? '🔓' : '🔒';
  var metricValue = el.querySelector('.metric-value');
  if (metricValue) {
    metricValue.textContent = formatValue(value, defaults.unit);
    metricValue.style.color = defaults.color;
  }
  var metricChange = el.querySelector('.metric-change');
  if (metricChange) {
    metricChange.className = 'metric-change ' + changeClass;
    metricChange.textContent = changeSymbol + ' ' + Math.abs(change).toFixed(1) + '% vs last period';
  }
  var statPills = el.querySelectorAll('.stat-pill strong');
  if (statPills.length >= 3) {
    statPills[0].textContent = panelData.views;
    statPills[1].textContent = formatDuration(panelData.totalDuration);
    statPills[2].textContent = panelData.scoreNorm.toFixed(2);
  }
  var sparkEl = el.querySelector('.spark');
  if (sparkEl) sparkEl.style.width = (info.scoreNorm * 100).toFixed(0) + '%';
}
function renderMorePanels(moreIds) {
  var container = dom.morePanels;
  container.innerHTML = '';
  for (var i = 0; i < moreIds.length; i++) {
    var id = moreIds[i];
    var panelData = state.panels[id];
    var defaults = PANEL_DEFAULTS.find(function(d) { return d.id === id; }) || { title: id, icon: '📊', value: 0, unit: '', color: '#6c5ce7' };
    var value = generateValue(id, defaults);
    var mini = document.createElement('div');
    mini.className = 'panel compact';
    mini.dataset.panelId = id;
    mini.innerHTML =
      '<div class="panel-header">' +
        '<span class="title">' + defaults.icon + ' ' + defaults.title + '</span>' +
        '<button class="btn-restore" style="background:none;border:none;color:var(--accent);cursor:pointer;font-size:0.75rem;">Restore</button>' +
      '</div>' +
      '<div class="compact-preview" style="display:flex">' +
        '<span style="font-weight:600;color:' + defaults.color + '">' + formatValue(value, defaults.unit) + '</span>' +
        '<div class="spark" style="width:40%"></div>' +
      '</div>';
    container.appendChild(mini);
  }
  attachMoreObservers();
}
// ---- Value generation (deterministic seeded) ----
var metricSeeds = {};
function getSeed(id) {
  if (!metricSeeds[id]) {
    var hash = 0;
    for (var i = 0; i < id.length; i++) { hash = ((hash << 5) - hash) + id.charCodeAt(i); hash |= 0; }
    metricSeeds[id] = Math.abs(hash) || 1;
  }
  return metricSeeds[id];
}
function generateValue(id, defaults) {
  var seed = getSeed(id);
  var rng = mulberry32(seed + Math.floor(now() / 300000));
  var base = defaults.value;
  if (base === 0) {
    if (defaults.unit === '%') base = 5 + rng() * 40;
    else if (defaults.unit === 'ms') base = 20 + rng() * 180;
    else if (defaults.unit === 'GB') base = 100 + rng() * 900;
    else if (defaults.unit === 'Mbps') base = 50 + rng() * 950;
    else base = 10000 + rng() * 90000;
  }
  return base;
}
function generateTrend(id) {
  var seed = getSeed(id) + 999;
  var rng = mulberry32(seed + Math.floor(now() / 600000));
  return (rng() - 0.5) * 20;
}
function generateBars(id, count) {
  var seed = getSeed(id) + 777;
  var rng = mulberry32(seed + Math.floor(now() / 300000));
  var html = '';
  for (var i = 0; i < count; i++) {
    var h = (15 + rng() * 85).toFixed(0);
    html += '<div class="bar" style="height:' + h + '%"></div>';
  }
  return html;
}
function formatValue(val, unit) {
  if (unit === '%') return val.toFixed(1) + unit;
  if (unit === 'ms') return Math.round(val) + unit;
  if (unit === 'GB') return val.toFixed(1) + ' ' + unit;
  if (unit === 'Mbps') return Math.round(val) + ' ' + unit;
  if (val >= 1000000) return (val / 1000000).toFixed(1) + 'M ' + unit;
  if (val >= 1000) return (val / 1000).toFixed(1) + 'k ' + unit;
  return Math.round(val) + ' ' + unit;
}
function formatDuration(ms) {
  if (ms < 1000) return '0s';
  var sec = Math.floor(ms / 1000);
  if (sec < 60) return sec + 's';
  var min = Math.floor(sec / 60);
  if (min < 60) return min + 'm';
  return (min / 60).toFixed(1) + 'h';
}
// ---- Observers ----
var observer;
function attachObservers() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver(function(entries) {
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var id = entry.target.dataset.panelId;
      if (!id) continue;
      if (entry.isIntersecting) {
        startView(id);
        state.panels[id].views++;
      } else {
        endView(id);
      }
    }
  }, { threshold: 0.5 });
  var panels = dom.dashboard.querySelectorAll('.panel');
  for (var j = 0; j < panels.length; j++) {
    observer.observe(panels[j]);
  }
}
function attachMoreObservers() {
  var panels = dom.morePanels.querySelectorAll('.panel');
  for (var i = 0; i < panels.length; i++) {
    if (observer) observer.observe(panels[i]);
  }
}
// ---- Drag handlers ----
function setupDragHandlers() {
  var panels = dom.dashboard.querySelectorAll('.panel');
  var dragData = { el: null, startX: 0, startY: 0 };
  function onDragStart(e) {
    var panel = e.target.closest('.panel');
    if (!panel) return;
    if (e.target.closest('button')) return;
    dragData.el = panel;
    dragData.startX = e.clientX;
    dragData.startY = e.clientY;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.dataset.panelId);
  }
  function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }
  function onDrop(e) {
    e.preventDefault();
    var target = e.target.closest('.panel');
    var draggedId = e.dataTransfer.getData('text/plain');
    if (!draggedId || !target) return;
    var targetId = target.dataset.panelId;
    if (draggedId === targetId) return;
    // Swap positions via overrides
    var draggedIdx = state.order.indexOf(draggedId);
    var targetIdx = state.order.indexOf(targetId);
    if (draggedIdx >= 0 && targetIdx >= 0) {
      state.order[draggedIdx] = targetId;
      state.order[targetIdx] = draggedId;
      if (!state.overrides[draggedId]) state.overrides[draggedId] = {};
      if (!state.overrides[targetId]) state.overrides[targetId] = {};
      state.overrides[draggedId].locked = true;
      state.overrides[targetId].locked = true;
      state.panels[draggedId].locked = true;
      state.panels[targetId].locked = true;
      showToast('Swapped ' + draggedId + ' ↔ ' + targetId);
      markDirty();
    }
    if (dragData.el) dragData.el.classList.remove('dragging');
  }
  function onDragEnd(e) {
    if (dragData.el) dragData.el.classList.remove('dragging');
    dragData.el = null;
  }
  for (var i = 0; i < panels.length; i++) {
    panels[i].addEventListener('dragstart', onDragStart);
    panels[i].addEventListener('dragover', onDragOver);
    panels[i].addEventListener('drop', onDrop);
    panels[i].addEventListener('dragend', onDragEnd);
  }
  // Click handlers for lock/pin
  dom.dashboard.addEventListener('click', function(e) {
    var btn = e.target.closest('button');
    if (!btn) return;
    var panel = e.target.closest('.panel');
    if (!panel) return;
    var id = panel.dataset.panelId;
    if (!id) return;
    if (btn.classList.contains('btn-lock')) {
      var locked = !state.panels[id].locked;
      state.panels[id].locked = locked;
      if (!state.overrides[id]) state.overrides[id] = {};
      state.overrides[id].locked = locked;
      showToast(id + (locked ? ' locked' : ' unlocked'));
      recordInteraction(id);
    }
    if (btn.classList.contains('btn-pin')) {
      if (!state.overrides[id]) state.overrides[id] = {};
      state.overrides[id].pinned = true;
      state.panels[id].scoreNorm = 1.0;
      state.panels[id].locked = true;
      state.overrides[id].locked = true;
      showToast(id + ' pinned to top');
      recordInteraction(id);
    }
    if (btn.classList.contains('btn-restore')) {
      state.panels[id].scoreNorm = 0.5;
      state.panels[id].locked = true;
      if (!state.overrides[id]) state.overrides[id] = {};
      state.overrides[id].locked = true;
      showToast(id + ' restored');
      recordInteraction(id);
    }
  });
  // Double-click to lock/unlock
  dom.dashboard.addEventListener('dblclick', function(e) {
    var panel = e.target.closest('.panel');
    if (!panel) return;
    var id = panel.dataset.panelId;
    if (!id) return;
    state.panels[id].locked = !state.panels[id].locked;
    if (!state.overrides[id]) state.overrides[id] = {};
    state.overrides[id].locked = state.panels[id].locked;
    showToast(id + (state.panels[id].locked ? ' locked' : ' unlocked (auto-layout enabled)'));
    markDirty();
  });
}
// ---- More section toggle ----
dom.moreToggle.addEventListener('click', function() {
  var more = dom.morePanels;
  var open = more.classList.toggle('open');
  dom.moreToggle.textContent = open ? '− Show less' : '+ ' + more.children.length + ' more panel' + (more.children.length > 1 ? 's' : '');
});
// ---- Toast ----
var toastTimer;
function showToast(msg) {
  var t = dom.toast;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function() { t.classList.remove('show'); }, 2000);
}
// ---- Persistence ----
function saveState() {
  try {
    var data = {
      panels: state.panels,
      order: state.order,
      overrides: state.overrides,
      savedAt: now()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch(e) { /* quota exceeded */ }
}
function loadState() {
  try {
    var raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    var data = JSON.parse(raw);
    state.panels = data.panels || {};
    state.order = data.order || [];
    state.overrides = data.overrides || {};
    // Restore locked state from overrides
    for (var id in state.overrides) {
      if (state.overrides[id].locked && state.panels[id]) {
        state.panels[id].locked = true;
      }
    }
    return true;
  } catch(e) { return false; }
}
function resetData() {
  state.panels = {};
  state.order = [];
  state.overrides = {};
  state.lastLayout = '';
  state.dirty = true;
  lastRenderedLayoutKey = '';
  PANEL_DEFAULTS.forEach(function(d) { initPanelData(d.id); });
  saveState();
  renderDashboard();
  showToast('Tracking data reset');
}
function clearStorage() {
  localStorage.removeItem(STORAGE_KEY);
  resetData();
  showToast('localStorage cleared');
}
// ---- Init ----
function init() {
  cacheDom();
  var loaded = loadState();
  PANEL_DEFAULTS.forEach(function(d) { initPanelData(d.id); });
  if (!loaded) {
    state.order = PANEL_DEFAULTS.map(function(d) { return d.id; });
  }
  recomputeAllScores();
  renderDashboard();
  // Periodic gentle refresh for time-based values
  setInterval(function() {
    var needsRefresh = false;
    for (var id in state.panels) {
      if (state.changeFlags[id]) { needsRefresh = true; break; }
    }
    if (needsRefresh || state.dirty) {
      renderDashboard();
    } else {
      // Light update: only refresh values in visible panels
      var elapsed = now();
      var panels = dom.dashboard.querySelectorAll('.panel');
      for (var i = 0; i < panels.length; i++) {
        var id = panels[i].dataset.panelId;
        if (!id) continue;
        var defaults = PANEL_DEFAULTS.find(function(d) { return d.id === id; });
        if (!defaults) continue;
        var val = generateValue(id, defaults);
        var mv = panels[i].querySelector('.metric-value');
        if (mv) mv.textContent = formatValue(val, defaults.unit);
        // Update spark
        var spark = panels[i].querySelector('.spark');
        if (spark && state.panels[id]) {
          spark.style.width = ((state.panels[id].scoreNorm || 0) * 100).toFixed(0) + '%';
        }
      }
    }
    state.changeFlags = {};
  }, 5000);
  // Button handlers
  document.getElementById('btnReset').addEventListener('click', resetData);
  document.getElementById('btnAutoLayout').addEventListener('click', function() {
    state.dirty = true;
    lastRenderedLayoutKey = '';
    renderDashboard();
    showToast('Layout recomputed');
  });
  document.getElementById('btnClearStorage').addEventListener('click', clearStorage);
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