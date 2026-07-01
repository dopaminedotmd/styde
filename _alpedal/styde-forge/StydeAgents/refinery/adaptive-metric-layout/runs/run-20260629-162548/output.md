<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d28;
  --surface2: #222636;
  --border: #2a2e3d;
  --text: #e1e4ed;
  --text2: #9196a8;
  --accent: #6c8cff;
  --accent2: #4ae0a0;
  --warn: #ffa94d;
  --danger: #ff6b6b;
  --radius: 10px;
  --gap: 10px;
  --compact-scale: 0.55;
  --transition: 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2);
  font-family: -apple-system, 'Segoe UI', system-ui, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
header h1 { font-size: 1.1rem; font-weight: 600; letter-spacing: -0.01em; }
.toolbar { display: flex; gap: 8px; align-items: center; }
.toolbar button {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text2);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: 0.15s;
}
.toolbar button:hover { background: var(--border); color: var(--text); }
.toolbar button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.grid {
  display: grid;
  gap: var(--gap);
  padding: var(--gap);
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  grid-auto-rows: 280px;
  grid-auto-flow: dense;
  transition: var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  position: relative;
  overflow: hidden;
  transition: grid-column var(--transition), grid-row var(--transition), transform var(--transition), opacity var(--transition);
  display: flex;
  flex-direction: column;
}
.panel.compact {
  transform: scale(var(--compact-scale));
  opacity: 0.65;
  filter: grayscale(0.15);
  z-index: 1;
}
.panel.compact:hover {
  transform: scale(0.7);
  opacity: 0.95;
  filter: grayscale(0);
  z-index: 2;
}
.panel.large { grid-column: span 2; grid-row: span 2; }
.panel.medium { grid-column: span 1; grid-row: span 1; }
.panel.small { grid-column: span 1; grid-row: span 1; transform: scale(0.8); }
.panel.locked { box-shadow: 0 0 0 2px var(--accent); }
.panel.locked::after {
  content: 'locked';
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 0.6rem;
  background: var(--accent);
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  opacity: 0.7;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-shrink: 0;
}
.panel-header h3 { font-size: 0.9rem; font-weight: 600; }
.panel-controls { display: flex; gap: 4px; }
.panel-controls button {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  font-size: 1rem;
  width: 26px;
  height: 26px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.15s;
}
.panel-controls button:hover { background: var(--surface2); color: var(--text); }
.panel-body {
  flex: 1;
  overflow: hidden;
  position: relative;
}
.metric-value { font-size: 2rem; font-weight: 700; color: var(--accent2); }
.metric-label { font-size: 0.78rem; color: var(--text2); margin-top: 4px; }
.metric-delta { font-size: 0.82rem; margin-top: 4px; }
.metric-delta.up { color: var(--accent2); }
.metric-delta.down { color: var(--danger); }
.chart-area {
  flex: 1;
  position: relative;
  min-height: 0;
}
.chart-area canvas {
  width: 100%;
  height: 100%;
}
.score-trace {
  position: absolute;
  bottom: 4px;
  left: 8px;
  right: 8px;
  font-size: 0.65rem;
  color: var(--text2);
  background: rgba(0,0,0,0.6);
  padding: 4px 8px;
  border-radius: 4px;
  display: none;
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.debug .score-trace { display: block; }
.compact-stub {
  text-align: center;
  padding-top: 12px;
  color: var(--text2);
  font-size: 0.75rem;
}
.rank-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: var(--surface2);
  color: var(--text2);
  font-size: 0.6rem;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 600;
}
.rank-badge.top { background: var(--accent); color: #fff; }
</style>
</head>
<body>
<header>
  <h1>adaptive dashboard</h1>
  <div class="toolbar">
    <button id="btnDebug" title="Toggle score traces">debug</button>
    <button id="btnReset" title="Reset all tracking data">reset</button>
    <button id="btnLayout" title="Force recompute layout">reflow</button>
  </div>
</header>
<div class="grid" id="grid"></div>
<script>
(function() {
'use strict';
/* ── STORAGE ───────────────────────────────── */
const STORE_KEY = 'adaptive_dash_v1';
function safeStore(fn) {
  try { return fn(); }
  catch(e) { return null; }
}
function loadState() {
  return safeStore(function() {
    var raw = localStorage.getItem(STORE_KEY);
    return raw ? JSON.parse(raw) : null;
  }) || { scores: {}, locks: {}, overrides: {}, events: [] };
}
function saveState(state) {
  safeStore(function() {
    localStorage.setItem(STORE_KEY, JSON.stringify(state));
  });
}
/* ── TRACKING ENGINE ───────────────────────── */
var state = loadState();
var visibilityObserver = null;
var interactionHandlers = new WeakMap();
var panelVisibility = {};
var viewStartTimes = {};
var now = Date.now;
var DECAY_HALF_LIFE = 7 * 24 * 3600 * 1000;
function decayFactor(ts) {
  var age = now() - ts;
  return Math.pow(0.5, age / DECAY_HALF_LIFE);
}
function computeScore(panelId) {
  var s = state.scores[panelId] || { frequency: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
  var freq = (s.frequency || 0) + (s.interactions || 0) * 0.3;
  var dur = (s.totalDuration || 0) / 1000;
  var recency = decayFactor(s.lastInteraction || state.events.length ? (state.events[state.events.length-1] || {}).ts || now() : now());
  var raw = (freq * 0.35 + Math.log2(dur + 1) * 0.40) * (0.5 + recency * 0.5);
  var score = Math.round(raw * 100) / 100;
  return { score: score, freq: freq, dur: dur, recency: recency, raw: raw };
}
function recordEvent(panelId, type) {
  var ts = now();
  state.events.push({ panel: panelId, type: type, ts: ts });
  if (state.events.length > 2000) state.events = state.events.slice(-1000);
  var s = state.scores[panelId] || { frequency: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
  s.frequency = (s.frequency || 0) + 1;
  s.lastInteraction = ts;
  if (type === 'interact') s.interactions = (s.interactions || 0) + 1;
  state.scores[panelId] = s;
  schedulePersist();
}
function flushViewDurations() {
  var ts = now();
  for (var pid in viewStartTimes) {
    if (!viewStartTimes[pid]) continue;
    var dur = ts - viewStartTimes[pid];
    if (dur < 200) continue;
    var s = state.scores[pid] || { frequency: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
    s.totalDuration = (s.totalDuration || 0) + dur;
    state.scores[pid] = s;
  }
  viewStartTimes = {};
  schedulePersist();
}
var persistTimer = null;
function schedulePersist() {
  if (persistTimer) return;
  persistTimer = setTimeout(function() {
    persistTimer = null;
    flushViewDurations();
    saveState(state);
  }, 2000);
}
/* ── VISIBILITY OBSERVER ───────────────────── */
function setupVisibilityObserver() {
  if (visibilityObserver) visibilityObserver.disconnect();
  visibilityObserver = new IntersectionObserver(function(entries) {
    var ts = now();
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var pid = entry.target.dataset.panelId;
      if (!pid) continue;
      var wasVisible = panelVisibility[pid] || false;
      var isVisible = entry.isIntersecting && entry.intersectionRatio > 0.25;
      if (wasVisible && !isVisible) {
        if (viewStartTimes[pid]) {
          var dur = ts - viewStartTimes[pid];
          if (dur > 200) {
            var s = state.scores[pid] || { frequency: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
            s.totalDuration = (s.totalDuration || 0) + dur;
            state.scores[pid] = s;
          }
          delete viewStartTimes[pid];
        }
      } else if (!wasVisible && isVisible) {
        viewStartTimes[pid] = ts;
        recordEvent(pid, 'view');
      }
      panelVisibility[pid] = isVisible;
    }
    schedulePersist();
  }, { threshold: [0, 0.25, 0.5, 0.75, 1] });
}
function observePanel(el) {
  if (!visibilityObserver) setupVisibilityObserver();
  if (el.dataset.observed === '1') return;
  el.dataset.observed = '1';
  visibilityObserver.observe(el);
}
function unobservePanel(el) {
  if (!visibilityObserver) return;
  if (el.dataset.observed !== '1') return;
  el.dataset.observed = '0';
  visibilityObserver.unobserve(el);
}
/* ── CHART RENDERER ────────────────────────── */
function renderChart(ctx, data, targetRes) {
  targetRes = targetRes || 48;
  var normalized = normalizeData(data, targetRes);
  var w = ctx.canvas.width || ctx.canvas.clientWidth * (window.devicePixelRatio || 1);
  var h = ctx.canvas.height || ctx.canvas.clientHeight * (window.devicePixelRatio || 1);
  if (!w || !h) return;
  ctx.clearRect(0, 0, w, h);
  var len = normalized.length;
  if (len < 2) return;
  var padX = w * 0.04;
  var padY = h * 0.1;
  var plotW = w - padX * 2;
  var plotH = h - padY * 2;
  var max = Math.max.apply(null, normalized) || 1;
  var min = Math.min.apply(null, normalized);
  var range = max - min || 1;
  var stepX = plotW / (len - 1);
  var grad = ctx.createLinearGradient(0, padY, 0, h - padY);
  grad.addColorStop(0, 'rgba(108,140,255,0.45)');
  grad.addColorStop(1, 'rgba(108,140,255,0.02)');
  ctx.beginPath();
  ctx.moveTo(padX, h - padY - ((normalized[0] - min) / range) * plotH);
  for (var i = 1; i < len; i++) {
    ctx.lineTo(padX + i * stepX, h - padY - ((normalized[i] - min) / range) * plotH);
  }
  ctx.strokeStyle = '#6c8cff';
  ctx.lineWidth = 1.6;
  ctx.stroke();
  ctx.lineTo(padX + (len - 1) * stepX, h - padY);
  ctx.lineTo(padX, h - padY);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();
  var dotI = len - 1;
  ctx.beginPath();
  ctx.arc(padX + dotI * stepX, h - padY - ((normalized[dotI] - min) / range) * plotH, 3.5, 0, Math.PI * 2);
  ctx.fillStyle = '#4ae0a0';
  ctx.fill();
}
function normalizeData(data, targetRes) {
  if (!data || !data.length) return [0];
  if (data.length <= targetRes) return data.slice();
  var result = new Array(targetRes);
  var ratio = data.length / targetRes;
  for (var i = 0; i < targetRes; i++) {
    var start = Math.floor(i * ratio);
    var end = Math.floor((i + 1) * ratio);
    if (end <= start) end = start + 1;
    var sum = 0;
    for (var j = start; j < end && j < data.length; j++) sum += data[j];
    result[i] = sum / (end - start);
  }
  return result;
}
/* ── VIRTUAL DOM DIFFING ──────────────────── */
function diffAndPatch(container, buildFn) {
  var existing = container.querySelectorAll('[data-panel-id]');
  var existingMap = {};
  for (var i = 0; i < existing.length; i++) {
    var el = existing[i];
    existingMap[el.dataset.panelId] = el;
  }
  var newDefs = buildFn();
  var newMap = {};
  for (var j = 0; j < newDefs.length; j++) {
    newMap[newDefs[j].id] = newDefs[j];
  }
  var frag = document.createDocumentFragment();
  var orderedIds = [];
  for (var k = 0; k < newDefs.length; k++) {
    var def = newDefs[k];
    orderedIds.push(def.id);
    var existingEl = existingMap[def.id];
    if (existingEl) {
      patchPanelElement(existingEl, def);
      if (existingEl.parentNode !== container || container.children[k] !== existingEl) {
        container.insertBefore(existingEl, container.children[k] || null);
      }
      frag.appendChild(existingEl);
    } else {
      var newEl = createPanelElement(def);
      frag.appendChild(newEl);
    }
  }
  for (var pid in existingMap) {
    if (!newMap[pid]) {
      unobservePanel(existingMap[pid]);
      if (existingMap[pid].parentNode) existingMap[pid].parentNode.removeChild(existingMap[pid]);
    }
  }
  container.innerHTML = '';
  container.appendChild(frag);
  for (var m = 0; m < orderedIds.length; m++) {
    var pel = container.querySelector('[data-panel-id="' + orderedIds[m] + '"]');
    if (pel) observePanel(pel);
  }
}
function createPanelElement(def) {
  var div = document.createElement('div');
  div.className = 'panel ' + (def.sizeClass || 'medium') + (def.locked ? ' locked' : '') + (def.compact ? ' compact' : '');
  div.dataset.panelId = def.id;
  div.dataset.observed = '0';
  div.innerHTML =
    '<span class="rank-badge' + (def.rank <= 2 ? ' top' : '') + '">#' + def.rank + ' | ' + def.score.toFixed(1) + '</span>' +
    '<div class="panel-header">' +
      '<h3>' + esc(def.title) + '</h3>' +
      '<div class="panel-controls">' +
        '<button data-action="lock" title="' + (def.locked ? 'unlock' : 'lock') + '">' + (def.locked ? '&#x1f512;' : '&#x1f513;') + '</button>' +
        '<button data-action="compact" title="toggle compact">&#x25f0;</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' +
      (def.compact
        ? '<div class="compact-stub">' + esc(def.title) + ' &middot; score ' + def.score.toFixed(1) + '<br><small>click to expand</small></div>'
        : def.bodyHTML) +
      '<div class="score-trace">f=' + def.trace.freq.toFixed(2) + ' d=' + def.trace.dur.toFixed(1) + 's r=' + def.trace.recency.toFixed(3) + ' raw=' + def.trace.raw.toFixed(4) + ' &rarr; ' + def.score.toFixed(2) + '</div>' +
    '</div>';
  setupPanelInteractions(div);
  return div;
}
function patchPanelElement(el, def) {
  var currentClass = 'panel ' + (def.sizeClass || 'medium') + (def.locked ? ' locked' : '') + (def.compact ? ' compact' : '');
  if (el.className !== currentClass) el.className = currentClass;
  var rankBadge = el.querySelector('.rank-badge');
  if (rankBadge) {
    var newBadgeHTML = '#' + def.rank + ' | ' + def.score.toFixed(1);
    var newBadgeClass = 'rank-badge' + (def.rank <= 2 ? ' top' : '');
    if (rankBadge.textContent !== newBadgeHTML) rankBadge.textContent = newBadgeHTML;
    if (rankBadge.className !== newBadgeClass) rankBadge.className = newBadgeClass;
  }
  var headerTitle = el.querySelector('.panel-header h3');
  if (headerTitle && headerTitle.textContent !== def.title) headerTitle.textContent = def.title;
  var lockBtn = el.querySelector('[data-action="lock"]');
  if (lockBtn) {
    var newLabel = def.locked ? '\u{1f512}' : '\u{1f513}';
    if (lockBtn.innerHTML !== newLabel) lockBtn.innerHTML = newLabel;
    lockBtn.title = def.locked ? 'unlock' : 'lock';
  }
  var body = el.querySelector('.panel-body');
  if (body) {
    if (def.compact) {
      var stubHTML = '<div class="compact-stub">' + esc(def.title) + ' &middot; score ' + def.score.toFixed(1) + '<br><small>click to expand</small></div>';
      if (!body.querySelector('.compact-stub')) {
        var canvases = body.querySelectorAll('canvas');
        for (var c = 0; c < canvases.length; c++) canvases[c].remove();
        body.innerHTML = stubHTML;
      } else if (body.querySelector('.compact-stub').innerHTML !== stubHTML) {
        body.querySelector('.compact-stub').innerHTML = stubHTML;
      }
    } else {
      body.querySelectorAll('.compact-stub').forEach(function(s) { s.remove(); });
    }
    var traceEl = body.querySelector('.score-trace');
    if (traceEl) {
      var newTrace = 'f=' + def.trace.freq.toFixed(2) + ' d=' + def.trace.dur.toFixed(1) + 's r=' + def.trace.recency.toFixed(3) + ' raw=' + def.trace.raw.toFixed(4) + ' \u2192 ' + def.score.toFixed(2);
      if (traceEl.textContent !== newTrace) traceEl.textContent = newTrace;
    }
  }
  if (!el._interactionsSetup) setupPanelInteractions(el);
}
function setupPanelInteractions(el) {
  if (el._interactionsSetup) return;
  el._interactionsSetup = true;
  el.addEventListener('click', function(e) {
    var target = e.target;
    var pid = el.dataset.panelId;
    if (target.dataset.action === 'lock') {
      e.stopPropagation();
      state.locks[pid] = !state.locks[pid];
      if (!state.locks[pid]) delete state.locks[pid];
      recordEvent(pid, 'lock');
      saveState(state);
      renderGrid();
      return;
    }
    if (target.dataset.action === 'compact') {
      e.stopPropagation();
      state.overrides[pid] = state.overrides[pid] || {};
      state.overrides[pid].compactOverride = !state.overrides[pid].compactOverride;
      recordEvent(pid, 'compact');
      saveState(state);
      renderGrid();
      return;
    }
    recordEvent(pid, 'interact');
  });
  el.addEventListener('mouseenter', function() {
    var pid = el.dataset.panelId;
    recordEvent(pid, 'hover');
  });
}
function esc(str) {
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}
/* ── PANEL DATA ───────────────────────────── */
var panelDefs = [
  { id: 'cpu', title: 'CPU Usage', type: 'chart', data: genData(120, 35, 15) },
  { id: 'memory', title: 'Memory', type: 'metric', value: '62.4%', delta: '+3.2', deltaDir: 'up' },
  { id: 'requests', title: 'Requests/min', type: 'chart', data: genData(200, 850, 200) },
  { id: 'latency', title: 'p95 Latency', type: 'metric', value: '142ms', delta: '-18', deltaDir: 'down' },
  { id: 'errors', title: 'Error Rate', type: 'metric', value: '0.12%', delta: '+0.02', deltaDir: 'up' },
  { id: 'throughput', title: 'Throughput', type: 'chart', data: genData(160, 420, 80) },
  { id: 'active_users', title: 'Active Users', type: 'metric', value: '3,842', delta: '+156', deltaDir: 'up' },
  { id: 'disk_io', title: 'Disk I/O', type: 'chart', data: genData(90, 280, 50) },
  { id: 'cache_hit', title: 'Cache Hit Rate', type: 'metric', value: '94.7%', delta: '+0.8', deltaDir: 'up' },
  { id: 'queue_depth', title: 'Queue Depth', type: 'metric', value: '7', delta: '-2', deltaDir: 'down' },
  { id: 'bandwidth', title: 'Bandwidth', type: 'chart', data: genData(150, 620, 110) },
  { id: 'connections', title: 'Connections', type: 'metric', value: '452', delta: '+23', deltaDir: 'up' }
];
function genData(len, base, amp) {
  var arr = new Array(len);
  for (var i = 0; i < len; i++) arr[i] = base + Math.sin(i * 0.12) * amp + Math.sin(i * 0.37) * amp * 0.55 + (Math.random() - 0.5) * amp * 0.25;
  return arr;
}
/* ── LAYOUT ENGINE ────────────────────────── */
function computeLayout() {
  var panels = [];
  for (var i = 0; i < panelDefs.length; i++) {
    var pd = panelDefs[i];
    var meta = computeScore(pd.id);
    var locked = !!state.locks[pd.id];
    var overrides = state.overrides[pd.id] || {};
    var compact = overrides.compactOverride !== undefined ? overrides.compactOverride : false;
    panels.push({
      id: pd.id,
      title: pd.title,
      type: pd.type,
      data: pd.data,
      value: pd.value,
      delta: pd.delta,
      deltaDir: pd.deltaDir,
      score: meta.score,
      trace: { freq: meta.freq, dur: meta.dur, recency: meta.recency, raw: meta.raw },
      locked: locked,
      compact: compact,
      rank: 0,
      sizeClass: 'medium'
    });
  }
  panels.sort(function(a, b) {
    if (a.locked && !b.locked) return -1;
    if (!a.locked && b.locked) return 1;
    return b.score - a.score;
  });
  var total = panels.length;
  for (var j = 0; j < panels.length; j++) {
    panels[j].rank = j + 1;
    var pct = j / total;
    if (pct < 0.18) panels[j].sizeClass = 'large';
    else if (pct < 0.55) panels[j].sizeClass = 'medium';
    else {
      panels[j].sizeClass = 'small';
      panels[j].compact = true;
    }
    if (panels[j].locked && panels[j].compact) panels[j].compact = false;
    if (state.overrides[panels[j].id] && state.overrides[panels[j].id].compactOverride !== undefined) {
      panels[j].compact = state.overrides[panels[j].id].compactOverride;
    }
  }
  lockedPanelsFirst(panels);
  return panels;
}
function lockedPanelsFirst(panels) {
  var locked = [];
  var unlocked = [];
  for (var i = 0; i < panels.length; i++) {
    if (panels[i].locked) locked.push(panels[i]);
    else unlocked.push(panels[i]);
  }
  panels.length = 0;
  for (var j = 0; j < locked.length; j++) panels.push(locked[j]);
  for (var k = 0; k < unlocked.length; k++) panels.push(unlocked[k]);
  for (var m = 0; m < panels.length; m++) panels[m].rank = m + 1;
}
function buildPanelHTML(def) {
  if (def.type === 'chart') {
    return '<div class="chart-area"><canvas id="chart-' + def.id + '" style="width:100%;height:100%"></canvas></div>';
  }
  if (def.type === 'metric') {
    var deltaHTML = def.delta ? ' <span class="metric-delta ' + def.deltaDir + '">' + def.delta + '</span>' : '';
    return '<div class="metric-value">' + esc(def.value) + deltaHTML + '</div><div class="metric-label">' + esc(def.title) + '</div>';
  }
  return '';
}
function buildDefsFromLayout(layout) {
  var defs = [];
  for (var i = 0; i < layout.length; i++) {
    var p = layout[i];
    defs.push({
      id: p.id,
      title: p.title,
      sizeClass: p.sizeClass,
      locked: p.locked,
      compact: p.compact,
      rank: p.rank,
      score: p.score,
      trace: p.trace,
      bodyHTML: buildPanelHTML(p),
      type: p.type,
      data: p.data,
      value: p.value,
      delta: p.delta,
      deltaDir: p.deltaDir
    });
  }
  return defs;
}
/* ── RENDER ──────────────────────────────── */
var currentLayoutMeta = null;
function renderGrid() {
  var layout = computeLayout();
  var defs = buildDefsFromLayout(layout);
  var grid = document.getElementById('grid');
  diffAndPatch(grid, function() { return defs; });
  currentLayoutMeta = layout;
  requestAnimationFrame(function() {
    for (var i = 0; i < layout.length; i++) {
      if (layout[i].type === 'chart' && !layout[i].compact) {
        var canvas = document.getElementById('chart-' + layout[i].id);
        if (canvas) {
          var dpr = window.devicePixelRatio || 1;
          var rect = canvas.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            var ctx = canvas.getContext('2d');
            renderChart(ctx, layout[i].data);
          }
        }
      }
    }
  });
}
/* ── DEBOUNCE ────────────────────────────── */
var renderTimer = null;
function debouncedRender() {
  if (renderTimer) return;
  renderTimer = requestAnimationFrame(function() {
    renderTimer = null;
    renderGrid();
  });
}
/* ── INIT ────────────────────────────────── */
function init() {
  setupVisibilityObserver();
  renderGrid();
  window.addEventListener('resize', debouncedRender);
  window.addEventListener('beforeunload', function() {
    flushViewDurations();
    saveState(state);
  });
  document.getElementById('btnDebug').addEventListener('click', function() {
    document.body.classList.toggle('debug');
    this.classList.toggle('active');
  });
  document.getElementById('btnReset').addEventListener('click', function() {
    state = { scores: {}, locks: {}, overrides: {}, events: [] };
    saveState(state);
    renderGrid();
  });
  document.getElementById('btnLayout').addEventListener('click', function() {
    renderGrid();
  });
  setInterval(function() {
    if (document.hidden) return;
    debouncedRender();
  }, 15000);
}
init();
})();
</script>
</body>
</html>