<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface-2: #22262f;
  --border: #2e3340; --text: #e1e4ea; --text-2: #8b909e;
  --accent: #6c8cff; --accent-2: #4a6cf7; --warn: #f59e0b;
  --danger: #ef4444; --success: #22c55e;
  --radius: 8px; --radius-sm: 4px;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
  --transition: 200ms ease;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100vh; line-height: 1.5;
}
body.keyboard-nav :focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px;
}
.header {
  background: var(--surface); border-bottom: 1px solid var(--border);
  padding: 12px 20px; display: flex; align-items: center;
  justify-content: space-between; gap: 16px; flex-wrap: wrap;
}
.header h1 { font-size: 1.1rem; font-weight: 600; color: var(--text); }
.header-actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.btn {
  background: var(--surface-2); color: var(--text);
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  padding: 6px 14px; font-size: 0.8rem; cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
  font-family: inherit; white-space: nowrap;
}
.btn:hover { background: var(--border); border-color: var(--text-2); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.btn.active { background: var(--accent-2); border-color: var(--accent); color: #fff; }
.btn.danger { border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: var(--danger); color: #fff; }
.toolbar {
  padding: 8px 20px; display: flex; gap: 6px; flex-wrap: wrap;
  border-bottom: 1px solid var(--border); font-size: 0.75rem;
  color: var(--text-2);
}
.toolbar span { display: flex; align-items: center; gap: 4px; }
.badge {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 10px; padding: 2px 8px; font-size: 0.7rem;
}
.dashboard {
  display: grid; gap: 12px; padding: 16px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  transition: all 300ms ease;
}
.dashboard.locked .panel-handle { display: none; }
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  display: flex; flex-direction: column;
  transition: box-shadow var(--transition), transform var(--transition),
    grid-column var(--transition), grid-row var(--transition),
    opacity 200ms ease;
  position: relative; min-height: 120px;
  will-change: transform;
}
.panel:hover { box-shadow: var(--shadow); }
.panel.compact { min-height: 60px; opacity: 0.85; }
.panel.compact .panel-body { max-height: 0; overflow: hidden; padding-top: 0; padding-bottom: 0; }
.panel.pinned { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.panel.rank-low { grid-column: span 1; }
.panel.rank-med { grid-column: span 1; }
.panel.rank-high { grid-column: span 2; }
.panel.rank-top { grid-column: span 3; }
@media (max-width: 768px) {
  .panel.rank-high, .panel.rank-top { grid-column: span 1; }
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: var(--surface-2);
  border-bottom: 1px solid var(--border); gap: 8px;
  cursor: grab; user-select: none;
}
.panel-header:active { cursor: grabbing; }
.panel-title {
  font-size: 0.85rem; font-weight: 600; color: var(--text);
  display: flex; align-items: center; gap: 6px; min-width: 0;
  flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.panel-rank-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.panel-rank-dot.hot { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
.panel-rank-dot.warm { background: var(--warn); }
.panel-rank-dot.cool { background: var(--text-2); }
.panel-score {
  font-size: 0.65rem; color: var(--text-2); flex-shrink: 0;
}
.panel-actions { display: flex; gap: 2px; flex-shrink: 0; }
.panel-btn {
  background: none; border: none; color: var(--text-2); cursor: pointer;
  padding: 4px; border-radius: var(--radius-sm); font-size: 0.9rem;
  line-height: 1; transition: color var(--transition), background var(--transition);
}
.panel-btn:hover { color: var(--text); background: var(--border); }
.panel-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
.panel-body { padding: 14px; flex: 1; overflow: hidden; transition: max-height 300ms ease; }
.panel-body canvas, .panel-body svg { max-width: 100%; height: auto; }
.metric-value { font-size: 1.8rem; font-weight: 700; color: var(--text); }
.metric-label { font-size: 0.7rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.5px; }
.metric-change { font-size: 0.75rem; }
.metric-change.up { color: var(--success); }
.metric-change.down { color: var(--danger); }
.sparkline { width: 100%; height: 48px; margin-top: 8px; }
.sparkline svg { display: block; width: 100%; }
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 40px 20px; text-align: center; color: var(--text-2);
  min-height: 200px;
}
.empty-state p { margin: 4px 0; font-size: 0.85rem; }
.loading-shimmer {
  background: linear-gradient(90deg, var(--surface-2) 25%, var(--border) 50%, var(--surface-2) 75%);
  background-size: 200% 100%; animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
.toast {
  position: fixed; bottom: 20px; right: 20px; z-index: 1000;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 10px 18px; box-shadow: var(--shadow);
  font-size: 0.8rem; opacity: 0; transform: translateY(10px);
  transition: opacity 200ms, transform 200ms; pointer-events: none;
  max-width: 320px;
}
.toast.show { opacity: 1; transform: translateY(0); }
.toast.error { border-color: var(--danger); }
.drag-ghost {
  position: fixed; z-index: 999; pointer-events: none;
  opacity: 0.9; background: var(--surface);
  border: 2px dashed var(--accent); border-radius: var(--radius);
  padding: 8px 14px; font-size: 0.8rem; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
  transform: translate(-50%, -50%);
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
</head>
<body class="keyboard-nav">
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <span style="font-size:0.7rem;color:var(--text-2)" id="status-text">Ready</span>
    <button class="btn" id="btn-lock" aria-label="Toggle layout lock" title="Lock/unlock auto-layout">Unlocked</button>
    <button class="btn" id="btn-reset" aria-label="Reset layout data">Reset Layout</button>
    <button class="btn" id="btn-add" aria-label="Add panel">+ Add Panel</button>
  </div>
</div>
<div class="toolbar">
  <span>Panels: <strong id="panel-count">0</strong></span>
  <span>|</span>
  <span>Sessions tracked: <strong id="session-count">0</strong></span>
  <span>|</span>
  <span class="badge" id="auto-status">auto-layout: active</span>
</div>
<div class="dashboard" id="dashboard" role="region" aria-label="Adaptive dashboard grid" aria-live="polite">
  <div class="empty-state" id="empty-state">
    <p>No panels yet</p>
    <p>Click "Add Panel" to create your first metric panel</p>
  </div>
</div>
<div class="toast" id="toast" aria-live="assertive"></div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const DECAY_HALF_DAYS = 7;
const TRACK_INTERVAL_MS = 2000;
const VIEWPORT_PADDING = 100;
const RANK_THRESHOLDS = { top: 0.8, high: 0.5, med: 0.2 };
const DEFAULT_PANELS = [
  { id: 'cpu', title: 'CPU Usage', type: 'gauge', value: 42, unit: '%', history: [] },
  { id: 'memory', title: 'Memory', type: 'gauge', value: 67, unit: '%', history: [] },
  { id: 'requests', title: 'Requests/s', type: 'counter', value: 1247, unit: '', history: [] },
  { id: 'latency', title: 'P95 Latency', type: 'counter', value: 32, unit: 'ms', history: [] },
  { id: 'errors', title: 'Error Rate', type: 'counter', value: 0.12, unit: '%', history: [] },
  { id: 'users', title: 'Active Users', type: 'counter', value: 892, unit: '', history: [] }
];
let state = {
  panels: [],
  tracking: {},
  sessions: 0,
  locked: false,
  lastTick: Date.now()
};
function safeGet(obj, path, fallback) {
  try {
    var parts = path.split('.');
    var current = obj;
    for (var i = 0; i < parts.length; i++) {
      if (current == null) return fallback;
      current = current[parts[i]];
    }
    return current != null ? current : fallback;
  } catch(e) { return fallback; }
}
function clamp(val, min, max) {
  if (val == null || isNaN(val)) return min;
  return Math.max(min, Math.min(max, Number(val) || min));
}
function now() { return Date.now(); }
function saveState() {
  try {
    var payload = JSON.parse(JSON.stringify({
      panels: state.panels, tracking: state.tracking,
      sessions: state.sessions, locked: state.locked
    }));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch(e) {
    showToast('Failed to save layout data', true);
  }
}
function loadState() {
  try {
    var raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    var data = JSON.parse(raw);
    if (!data || typeof data !== 'object') return false;
    state.panels = Array.isArray(data.panels) ? data.panels : [];
    state.tracking = (data.tracking && typeof data.tracking === 'object') ? data.tracking : {};
    state.sessions = typeof data.sessions === 'number' ? data.sessions : 0;
    state.locked = typeof data.locked === 'boolean' ? data.locked : false;
    state.sessions++;
    for (var i = 0; i < state.panels.length; i++) {
      var p = state.panels[i];
      if (!p.history) p.history = [];
      if (!p.id) p.id = 'panel_' + i;
    }
    return true;
  } catch(e) {
    showToast('Corrupted layout data, starting fresh', true);
    return false;
  }
}
function initDefaultPanels() {
  state.panels = JSON.parse(JSON.stringify(DEFAULT_PANELS));
  for (var i = 0; i < state.panels.length; i++) {
    state.panels[i].history = [];
    if (!state.tracking[state.panels[i].id]) {
      state.tracking[state.panels[i].id] = {
        viewCount: 0, totalDuration: 0, interactionCount: 0,
        lastInteraction: 0, pinned: false, positionOverride: null
      };
    }
  }
  state.sessions = 1;
  state.locked = false;
  saveState();
}
function computeScore(panelId) {
  var t = state.tracking[panelId];
  if (!t) return 0;
  var hoursSinceInteraction = (now() - (t.lastInteraction || 0)) / 3600000;
  var decay = Math.pow(0.5, hoursSinceInteraction / (DECAY_HALF_DAYS * 24));
  var freq = clamp(t.viewCount || 0, 0, Infinity);
  var dur = clamp(t.totalDuration || 0, 0, Infinity);
  return (freq * dur * decay);
}
function getRankTier(score, maxScore) {
  if (maxScore <= 0) return 'low';
  var ratio = score / maxScore;
  if (ratio >= RANK_THRESHOLDS.top) return 'top';
  if (ratio >= RANK_THRESHOLDS.high) return 'high';
  if (ratio >= RANK_THRESHOLDS.med) return 'med';
  return 'low';
}
function getRankClass(score, maxScore) {
  var tier = getRankTier(score, maxScore);
  if (tier === 'top') return 'rank-top';
  if (tier === 'high') return 'rank-high';
  if (tier === 'med') return 'rank-med';
  return 'rank-low';
}
function getHeatDot(score, maxScore) {
  if (maxScore <= 0) return 'cool';
  var ratio = score / maxScore;
  if (ratio >= 0.8) return 'hot';
  if (ratio >= 0.4) return 'warm';
  return 'cool';
}
function sortedPanels() {
  var scored = state.panels.map(function(p) {
    return { panel: p, score: computeScore(p.id) };
  });
  scored.sort(function(a, b) { return b.score - a.score; });
  return scored;
}
function getOrderedPanels() {
  var pinned = [];
  var unpinned = [];
  var scored = sortedPanels();
  for (var i = 0; i < scored.length; i++) {
    var entry = scored[i];
    var t = state.tracking[entry.panel.id];
    if ((t && t.pinned) || (entry.panel.pinned)) {
      pinned.push(entry);
    } else {
      unpinned.push(entry);
    }
  }
  return pinned.concat(unpinned);
}
var visiblePanels = {};
var visibilityObserver = null;
function setupVisibilityTracking() {
  if (visibilityObserver) visibilityObserver.disconnect();
  if (!window.IntersectionObserver) return;
  visibilityObserver = new IntersectionObserver(function(entries) {
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var panelId = entry.target.getAttribute('data-panel-id');
      if (!panelId) continue;
      if (entry.isIntersecting && entry.intersectionRatio > 0.3) {
        if (!visiblePanels[panelId]) {
          visiblePanels[panelId] = { start: now(), lastTick: now() };
          trackView(panelId);
        } else {
          visiblePanels[panelId].lastTick = now();
        }
      } else {
        if (visiblePanels[panelId]) {
          var elapsed = now() - visiblePanels[panelId].start;
          trackDuration(panelId, elapsed);
          delete visiblePanels[panelId];
        }
      }
    }
  }, { threshold: [0, 0.3, 0.6] });
  var panels = document.querySelectorAll('.panel');
  for (var j = 0; j < panels.length; j++) {
    visibilityObserver.observe(panels[j]);
  }
}
function trackView(panelId) {
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = { viewCount: 0, totalDuration: 0, interactionCount: 0, lastInteraction: 0, pinned: false, positionOverride: null };
  }
  state.tracking[panelId].viewCount = (state.tracking[panelId].viewCount || 0) + 1;
  state.tracking[panelId].lastInteraction = now();
}
function trackDuration(panelId, ms) {
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = { viewCount: 0, totalDuration: 0, interactionCount: 0, lastInteraction: 0, pinned: false, positionOverride: null };
  }
  state.tracking[panelId].totalDuration = (state.tracking[panelId].totalDuration || 0) + ms;
}
function trackInteraction(panelId) {
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = { viewCount: 0, totalDuration: 0, interactionCount: 0, lastInteraction: 0, pinned: false, positionOverride: null };
  }
  state.tracking[panelId].interactionCount = (state.tracking[panelId].interactionCount || 0) + 1;
  state.tracking[panelId].lastInteraction = now();
}
function flushVisibleDurations() {
  var ids = Object.keys(visiblePanels);
  for (var i = 0; i < ids.length; i++) {
    var id = ids[i];
    var elapsed = now() - visiblePanels[id].start;
    trackDuration(id, elapsed);
    visiblePanels[id].start = now();
  }
}
function tick() {
  flushVisibleDurations();
  state.lastTick = now();
  saveState();
}
setInterval(tick, TRACK_INTERVAL_MS);
var panelIdCounter = 0;
function generatePanelId() {
  panelIdCounter++;
  return 'panel_' + now() + '_' + panelIdCounter;
}
function renderDashboard() {
  var dash = document.getElementById('dashboard');
  if (!dash) return;
  var emptyState = document.getElementById('empty-state');
  var ordered = getOrderedPanels();
  var panelCount = ordered.length;
  if (emptyState) {
    emptyState.style.display = panelCount === 0 ? 'flex' : 'none';
  }
  document.getElementById('panel-count').textContent = panelCount;
  document.getElementById('session-count').textContent = state.sessions || 0;
  document.getElementById('auto-status').textContent = state.locked ? 'auto-layout: locked' : 'auto-layout: active';
  document.getElementById('btn-lock').textContent = state.locked ? 'Locked' : 'Unlocked';
  if (state.locked) {
    document.getElementById('btn-lock').classList.add('active');
    dash.classList.add('locked');
  } else {
    document.getElementById('btn-lock').classList.remove('active');
    dash.classList.remove('locked');
  }
  var maxScore = 0;
  for (var i = 0; i < ordered.length; i++) {
    var s = ordered[i].score;
    if (s > maxScore) maxScore = s;
  }
  var existingPanels = dash.querySelectorAll('.panel');
  var existingMap = {};
  for (var j = 0; j < existingPanels.length; j++) {
    var ep = existingPanels[j];
    existingMap[ep.getAttribute('data-panel-id')] = ep;
  }
  var fragment = document.createDocumentFragment();
  if (panelCount === 0) {
    dash.innerHTML = '';
    if (emptyState) {
      emptyState.style.display = 'flex';
      dash.appendChild(emptyState);
    }
    return;
  }
  if (emptyState) emptyState.style.display = 'none';
  for (var k = 0; k < ordered.length; k++) {
    var entry = ordered[k];
    var panel = entry.panel;
    var score = entry.score;
    var rankClass = getRankClass(score, maxScore);
    var heatDot = getHeatDot(score, maxScore);
    var t = state.tracking[panel.id] || {};
    var isPinned = !!(t.pinned || panel.pinned);
    var existing = existingMap[panel.id];
    if (existing) {
      existing.className = 'panel ' + rankClass + (isPinned ? ' pinned' : '') + (rankClass === 'rank-low' && score < maxScore * 0.1 ? ' compact' : '');
      existing.setAttribute('data-rank', rankClass);
      existing.setAttribute('data-score', Math.round(score));
      var dotEl = existing.querySelector('.panel-rank-dot');
      if (dotEl) { dotEl.className = 'panel-rank-dot ' + heatDot; }
      var scoreEl = existing.querySelector('.panel-score-val');
      if (scoreEl) scoreEl.textContent = Math.round(score / 100) / 10 + 'k';
      fragment.appendChild(existing);
      delete existingMap[panel.id];
      continue;
    }
    var el = document.createElement('div');
    el.className = 'panel ' + rankClass + (isPinned ? ' pinned' : '') + (rankClass === 'rank-low' && score < maxScore * 0.1 ? ' compact' : '');
    el.setAttribute('data-panel-id', panel.id);
    el.setAttribute('data-rank', rankClass);
    el.setAttribute('data-score', Math.round(score));
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', panel.title + ' panel, score ' + Math.round(score));
    el.setAttribute('tabindex', '0');
    var bodyHTML = renderPanelBody(panel);
    el.innerHTML =
      '<div class="panel-header" data-action="drag">' +
        '<span class="panel-title">' +
          '<span class="panel-rank-dot ' + heatDot + '" aria-hidden="true"></span>' +
          escapeHTML(panel.title) +
        '</span>' +
        '<span class="panel-score">' +
          '<span class="panel-score-val">' + (Math.round(score / 100) / 10) + 'k</span>' +
        '</span>' +
        '<div class="panel-actions">' +
          (isPinned
            ? '<button class="panel-btn" data-action="unpin" aria-label="Unpin ' + escapeHTML(panel.title) + '" title="Unpin">📌</button>'
            : '<button class="panel-btn" data-action="pin" aria-label="Pin ' + escapeHTML(panel.title) + '" title="Pin">📍</button>') +
          '<button class="panel-btn" data-action="toggle-compact" aria-label="Toggle compact mode for ' + escapeHTML(panel.title) + '" title="Toggle compact">⊟</button>' +
          '<button class="panel-btn" data-action="delete-panel" aria-label="Delete ' + escapeHTML(panel.title) + '" title="Delete panel" style="color:var(--danger)">✕</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body">' + bodyHTML + '</div>';
    bindPanelEvents(el);
    fragment.appendChild(el);
  }
  var removedIds = Object.keys(existingMap);
  for (var r = 0; r < removedIds.length; r++) {
    var rem = existingMap[removedIds[r]];
    if (rem && rem.parentNode) rem.parentNode.removeChild(rem);
  }
  dash.innerHTML = '';
  dash.appendChild(fragment);
  if (panelCount === 0 && emptyState) {
    dash.appendChild(emptyState);
  }
  setupVisibilityTracking();
  document.getElementById('status-text').textContent = 'Updated ' + new Date().toLocaleTimeString();
}
function escapeHTML(str) {
  if (str == null) return '';
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(String(str)));
  return div.innerHTML;
}
function renderPanelBody(panel) {
  var type = panel.type || 'counter';
  var value = panel.value != null ? panel.value : 0;
  var unit = panel.unit || '';
  var history = Array.isArray(panel.history) ? panel.history : [];
  var html = '';
  if (type === 'gauge') {
    var pct = clamp(value, 0, 100);
    var color = pct > 80 ? 'var(--danger)' : pct > 60 ? 'var(--warn)' : 'var(--success)';
    html += '<div class="metric-value" style="color:' + color + '">' + value + '<span style="font-size:0.5em;margin-left:2px;">' + escapeHTML(unit) + '</span></div>';
    html += '<div class="metric-label">Current</div>';
    html += '<div style="margin-top:6px;height:6px;background:var(--surface-2);border-radius:3px;overflow:hidden;">';
    html += '<div style="width:' + pct + '%;height:100%;background:' + color + ';border-radius:3px;transition:width 300ms;"></div>';
    html += '</div>';
  } else {
    html += '<div class="metric-value">' + value.toLocaleString() + '<span style="font-size:0.5em;margin-left:2px;">' + escapeHTML(unit) + '</span></div>';
    html += '<div class="metric-label">Current</div>';
  }
  if (history.length > 1) {
    var change = history[history.length - 1] - history[0];
    var changePct = history[0] !== 0 ? ((change / Math.abs(history[0])) * 100) : 0;
    var changeClass = change >= 0 ? 'up' : 'down';
    var arrow = change >= 0 ? '↑' : '↓';
    html += '<div class="metric-change ' + changeClass + '" style="margin-top:2px;">' + arrow + ' ' + Math.abs(changePct).toFixed(1) + '% from baseline</div>';
  }
  html += renderSparkline(history);
  return html;
}
function renderSparkline(history) {
  if (!history || history.length < 2) return '<div class="sparkline"></div>';
  var min = Infinity, max = -Infinity;
  for (var i = 0; i < history.length; i++) {
    var v = history[i];
    if (v < min) min = v;
    if (v > max) max = v;
  }
  if (min === max) { min = min - 1; max = max + 1; }
  var range = max - min || 1;
  var w = 200, h = 48, pad = 2;
  var points = [];
  for (var j = 0; j < history.length; j++) {
    var x = pad + (j / Math.max(history.length - 1, 1)) * (w - 2 * pad);
    var y = h - pad - ((history[j] - min) / range) * (h - 2 * pad);
    if (isNaN(x) || isNaN(y) || !isFinite(x) || !isFinite(y)) continue;
    points.push(x.toFixed(2) + ',' + y.toFixed(2));
  }
  if (points.length < 2) return '<div class="sparkline"></div>';
  var pathD = 'M' + points.join(' L');
  var svg = '<svg viewBox="0 0 ' + w + ' ' + h + '" class="sparkline" aria-label="Sparkline chart" role="img">';
  svg += '<path d="' + pathD + '" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
  svg += '<path d="' + pathD + ' L' + (pad + (history.length - 1) / Math.max(history.length - 1, 1) * (w - 2 * pad)).toFixed(2) + ',' + (h - pad) + ' L' + pad.toFixed(2) + ',' + (h - pad) + ' Z" fill="url(#sparkGrad)" opacity="0.15"/>';
  svg += '<defs><linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--accent)"/><stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/></linearGradient></defs>';
  svg += '</svg>';
  return svg;
}
function bindPanelEvents(el) {
  var panelId = el.getAttribute('data-panel-id');
  if (!panelId) return;
  el.addEventListener('click', function(e) {
    trackInteraction(panelId);
  });
  el.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      trackInteraction(panelId);
    }
  });
  el.addEventListener('mouseenter', function() {
    if (!visiblePanels[panelId]) {
      visiblePanels[panelId] = { start: now(), lastTick: now() };
      trackView(panelId);
    }
  });
  el.addEventListener('mouseleave', function() {
    if (visiblePanels[panelId]) {
      var elapsed = now() - visiblePanels[panelId].start;
      trackDuration(panelId, elapsed);
      delete visiblePanels[panelId];
    }
  });
  var buttons = el.querySelectorAll('.panel-btn');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      var action = this.getAttribute('data-action');
      trackInteraction(panelId);
      if (action === 'pin' || action === 'unpin') togglePin(panelId);
      else if (action === 'toggle-compact') toggleCompact(panelId);
      else if (action === 'delete-panel') deletePanel(panelId);
    });
  }
  var header = el.querySelector('.panel-header');
  if (header) {
    header.addEventListener('mousedown', function(e) {
      if (e.target.closest('.panel-btn')) return;
      startDrag(panelId, el, e);
    });
    header.addEventListener('touchstart', function(e) {
      if (e.target.closest('.panel-btn')) return;
      startDrag(panelId, el, e);
    }, { passive: false });
  }
}
var dragState = null;
var ghostEl = null;
function startDrag(panelId, el, e) {
  if (state.locked) {
    showToast('Layout is locked. Unlock to rearrange panels.');
    return;
  }
  e.preventDefault();
  var clientX = e.touches ? e.touches[0].clientX : e.clientX;
  var clientY = e.touches ? e.touches[0].clientY : e.clientY;
  dragState = { panelId: panelId, el: el, startX: clientX, startY: clientY, moved: false };
  ghostEl = document.createElement('div');
  ghostEl.className = 'drag-ghost';
  ghostEl.textContent = 'Moving: ' + (el.querySelector('.panel-title') ? el.querySelector('.panel-title').textContent.trim() : 'Panel');
  ghostEl.style.left = clientX + 'px';
  ghostEl.style.top = clientY + 'px';
  document.body.appendChild(ghostEl);
  document.addEventListener('mousemove', onDragMove);
  document.addEventListener('mouseup', onDragEnd);
  document.addEventListener('touchmove', onDragMove, { passive: false });
  document.addEventListener('touchend', onDragEnd);
  document.addEventListener('touchcancel', onDragEnd);
}
function onDragMove(e) {
  if (!dragState) return;
  e.preventDefault();
  var clientX = e.touches ? e.touches[0].clientX : e.clientX;
  var clientY = e.touches ? e.touches[0].clientY : e.clientY;
  dragState.moved = true;
  if (ghostEl) {
    ghostEl.style.left = clientX + 'px';
    ghostEl.style.top = clientY + 'px';
  }
}
function onDragEnd(e) {
  document.removeEventListener('mousemove', onDragMove);
  document.removeEventListener('mouseup', onDragEnd);
  document.removeEventListener('touchmove', onDragMove);
  document.removeEventListener('touchend', onDragEnd);
  document.removeEventListener('touchcancel', onDragEnd);
  if (dragState && dragState.moved) {
    var clientX = (e.changedTouches ? e.changedTouches[0].clientX : e.clientX) || 0;
    var clientY = (e.changedTouches ? e.changedTouches[0].clientY : e.clientY) || 0;
    movePanelToPosition(dragState.panelId, clientX, clientY);
  }
  if (ghostEl && ghostEl.parentNode) {
    ghostEl.parentNode.removeChild(ghostEl);
  }
  ghostEl = null;
  dragState = null;
}
function movePanelToPosition(panelId, clientX, clientY) {
  var targetEl = document.elementFromPoint(clientX, clientY);
  if (!targetEl) return;
  var targetPanel = targetEl.closest('.panel');
  if (!targetPanel) return;
  var targetId = targetPanel.getAttribute('data-panel-id');
  if (!targetId || targetId === panelId) return;
  var idxA = -1, idxB = -1;
  for (var i = 0; i < state.panels.length; i++) {
    if (state.panels[i].id === panelId) idxA = i;
    if (state.panels[i].id === targetId) idxB = i;
  }
  if (idxA < 0 || idxB < 0) return;
  var panel = state.panels.splice(idxA, 1)[0];
  state.panels.splice(idxB, 0, panel);
  if (!state.tracking[panelId]) state.tracking[panelId] = { viewCount: 0, totalDuration: 0, interactionCount: 0, lastInteraction: 0, pinned: false, positionOverride: null };
  state.tracking[panelId].positionOverride = idxB;
  state.tracking[panelId].lastInteraction = now();
  saveState();
  renderDashboard();
  showToast('Panel moved');
}
function togglePin(panelId) {
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = { viewCount: 0, totalDuration: 0, interactionCount: 0, lastInteraction: 0, pinned: false, positionOverride: null };
  }
  state.tracking[panelId].pinned = !state.tracking[panelId].pinned;
  state.tracking[panelId].lastInteraction = now();
  var panel = state.panels.find(function(p) { return p.id === panelId; });
  if (panel) panel.pinned = state.tracking[panelId].pinned;
  saveState();
  renderDashboard();
  showToast(state.tracking[panelId].pinned ? 'Panel pinned' : 'Panel unpinned');
}
function toggleCompact(panelId) {
  var el = document.querySelector('[data-panel-id="' + panelId + '"]');
  if (!el) return;
  el.classList.toggle('compact');
  trackInteraction(panelId);
  showToast(el.classList.contains('compact') ? 'Panel compacted' : 'Panel expanded');
}
function deletePanel(panelId) {
  state.panels = state.panels.filter(function(p) { return p.id !== panelId; });
  delete state.tracking[panelId];
  saveState();
  renderDashboard();
  showToast('Panel deleted');
}
function addPanel() {
  var panelTypes = ['counter', 'gauge'];
  var titles = ['New Metric', 'Response Time', 'Throughput', 'CPU Load', 'Disk IO', 'Cache Hits', 'Queue Depth'];
  var newPanel = {
    id: generatePanelId(),
    title: titles[Math.floor(Math.random() * titles.length)],
    type: panelTypes[Math.floor(Math.random() * panelTypes.length)],
    value: Math.round(Math.random() * 100),
    unit: Math.random() > 0.5 ? '%' : 'ms',
    history: Array.from({ length: 20 }, function() { return Math.round(Math.random() * 100); })
  };
  state.panels.push(newPanel);
  state.tracking[newPanel.id] = {
    viewCount: 0, totalDuration: 0, interactionCount: 0,
    lastInteraction: now(), pinned: false, positionOverride: null
  };
  saveState();
  renderDashboard();
  showToast('Panel added: ' + newPanel.title);
}
function resetLayout() {
  if (!confirm('Reset all layout data? This clears tracking history and restores defaults.')) return;
  localStorage.removeItem(STORAGE_KEY);
  state.panels = [];
  state.tracking = {};
  state.sessions = 0;
  state.locked = false;
  visiblePanels = {};
  initDefaultPanels();
  renderDashboard();
  showToast('Layout reset to defaults');
}
function updateMetricValues() {
  var now2 = Date.now();
  for (var i = 0; i < state.panels.length; i++) {
    var p = state.panels[i];
    var change = (Math.random() - 0.5) * 10;
    p.value = clamp((p.value || 0) + change, 0, p.type === 'gauge' ? 100 : 999999);
    if (!p.history) p.history = [];
    p.history.push(Number(p.value.toFixed(1)));
    if (p.history.length > 30) p.history.shift();
  }
  renderDashboard();
}
var toastTimer = null;
function showToast(msg, isError) {
  var el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg || '';
  el.className = 'toast show' + (isError ? ' error' : '');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(function() {
    el.classList.remove('show');
    toastTimer = null;
  }, 2500);
}
function init() {
  var loaded = loadState();
  if (!loaded || state.panels.length === 0) {
    initDefaultPanels();
  }
  document.getElementById('btn-lock').addEventListener('click', function() {
    state.locked = !state.locked;
    saveState();
    renderDashboard();
    showToast(state.locked ? 'Layout locked' : 'Layout unlocked');
  });
  document.getElementById('btn-reset').addEventListener('click', resetLayout);
  document.getElementById('btn-add').addEventListener('click', function() {
    addPanel();
  });
  document.addEventListener('keydown', function(e) {
    document.body.classList.add('keyboard-nav');
    if (e.key === 'Escape' && dragState) {
      onDragEnd({});
    }
  });
  document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-nav');
  });
  window.addEventListener('beforeunload', function() {
    flushVisibleDurations();
    saveState();
  });
  window.addEventListener('error', function(e) {
    showToast('Dashboard error: ' + (e.message || 'Unknown error'), true);
  });
  renderDashboard();
  showToast('Dashboard ready. ' + state.sessions + ' sessions tracked.');
  setInterval(updateMetricValues, 5000);
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