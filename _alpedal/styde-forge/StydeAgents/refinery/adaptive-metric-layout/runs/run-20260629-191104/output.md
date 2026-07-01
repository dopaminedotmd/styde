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
  --surface-hover: #22263a;
  --border: #2a2e3f;
  --text: #e1e4ed;
  --text-dim: #8b8fa8;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff5c6c;
  --success: #3ecf8e;
  --warning: #f0b048;
  --radius: 12px;
  --gap: 12px;
  --transition: 200ms ease;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
#dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  padding: var(--gap);
  min-height: 100vh;
  align-items: start;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition), grid-column var(--transition), grid-row var(--transition);
  cursor: grab;
  position: relative;
  min-height: 120px;
}
.panel:active { cursor: grabbing; }
.panel.dragging {
  opacity: 0.7;
  transform: scale(0.97);
  z-index: 1000;
  box-shadow: 0 0 0 2px var(--accent), 0 16px 48px rgba(0,0,0,0.5);
}
.panel.drag-target {
  box-shadow: 0 0 0 2px var(--accent), 0 0 24px var(--accent-glow);
}
.panel.compact { grid-column: span 1; grid-row: span 1; }
.panel.normal { grid-column: span 2; grid-row: span 1; }
.panel.expanded { grid-column: span 3; grid-row: span 2; }
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.02);
}
.panel-title {
  font-weight: 600;
  font-size: 13px;
  color: var(--text);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-controls {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.panel-btn {
  background: none;
  border: 1px solid transparent;
  color: var(--text-dim);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1;
  transition: color var(--transition), background var(--transition), border-color var(--transition);
}
.panel-btn:hover { color: var(--text); background: var(--surface-hover); border-color: var(--border); }
.panel-btn.locked { color: var(--accent); border-color: var(--accent); }
.panel-body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.panel-body.compact-mode { display: none; }
.panel.compact .panel-body.full-mode { display: none; }
.panel.compact .panel-body.compact-mode { display: flex; }
.metric-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}
.metric-label {
  font-size: 11px;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.metric-change { font-size: 12px; font-weight: 600; }
.metric-change.up { color: var(--success); }
.metric-change.down { color: var(--danger); }
.sparkline-container {
  width: 100%;
  height: 48px;
  margin-top: 4px;
}
.sparkline-container svg { width: 100%; height: 100%; }
.rank-badge {
  position: absolute;
  top: 8px;
  right: 38px;
  font-size: 10px;
  color: var(--text-dim);
  background: rgba(255,255,255,0.04);
  padding: 2px 6px;
  border-radius: 4px;
  pointer-events: none;
}
.drag-handle {
  color: var(--text-dim);
  cursor: grab;
  font-size: 12px;
  padding: 2px 6px;
  user-select: none;
}
.drag-handle:active { cursor: grabbing; }
#toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px var(--gap);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
#toolbar button {
  background: var(--surface-hover);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all var(--transition);
}
#toolbar button:hover { background: var(--accent); border-color: var(--accent); }
#toolbar button.reset-btn { margin-left: auto; }
#debug-log {
  position: fixed;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.85);
  color: var(--success);
  font: 10px monospace;
  padding: 6px 10px;
  border-radius: 6px;
  max-width: 320px;
  max-height: 80px;
  overflow-y: auto;
  pointer-events: none;
  opacity: 0;
  transition: opacity 300ms;
}
#debug-log.visible { opacity: 1; }
</style>
</head>
<body>
<div id="toolbar">
  <button id="btn-reset-auto" title="Remove all locks, let auto-layout take over">Reset Auto</button>
  <button id="btn-save" title="Save current layout manually">Save Layout</button>
  <button id="btn-log" title="Show usage stats in console">Dump Stats</button>
  <button id="btn-reset-data" class="reset-btn" title="Wipe all tracking data and reload">Reset All Data</button>
</div>
<div id="dashboard"></div>
<div id="debug-log"></div>
<script>
(function() {
'use strict';
var now = Date.now;
var perfNow = (typeof performance !== 'undefined' && performance.now) ? function(){return performance.now();} : function(){return Date.now();};
var $els = {
  dashboard: null,
  debugLog: null
};
var rafId = null;
var pendingMutations = [];
function enqueueMutation(fn) {
  pendingMutations.push(fn);
  if (rafId === null) {
    rafId = requestAnimationFrame(flushMutations);
  }
}
function flushMutations() {
  var batch = pendingMutations;
  pendingMutations = [];
  rafId = null;
  for (var i = 0; i < batch.length; i++) {
    try { batch[i](); } catch(e) { log('Mutation error: ' + e.message); }
  }
}
function log(msg) {
  var el = $els.debugLog;
  if (!el) return;
  el.textContent = msg;
  el.classList.add('visible');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(function(){ el.classList.remove('visible'); }, 2500);
}
function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
function isValidNum(v) { return typeof v === 'number' && isFinite(v) && !isNaN(v); }
var DataStore = (function() {
  var STORAGE_KEY = 'adaptive_dashboard_data';
  var data = {
    panels: [
      { id: 'cpu',      title: 'CPU Usage',        value: 42, change: 3.2,  unit: '%',    history: [], color: '#6c8cff' },
      { id: 'memory',   title: 'Memory',            value: 67, change: -1.5, unit: '%',    history: [], color: '#3ecf8e' },
      { id: 'requests', title: 'Requests/sec',      value: 1243, change: 8.7, unit: '/s',   history: [], color: '#f0b048' },
      { id: 'latency',  title: 'P95 Latency',       value: 142, change: -12,  unit: 'ms',   history: [], color: '#ff5c6c' },
      { id: 'errors',   title: 'Error Rate',        value: 0.4, change: -0.2, unit: '%',    history: [], color: '#d46cff' },
      { id: 'disk',     title: 'Disk I/O',          value: 85, change: 5.1,  unit: 'MB/s', history: [], color: '#4dc9f6' },
      { id: 'users',    title: 'Active Users',      value: 892, change: 15,   unit: '',     history: [], color: '#ff8c6c' },
      { id: 'uptime',   title: 'Uptime',            value: 99.97, change: 0.02, unit: '%',  history: [], color: '#6cffb8' }
    ],
    tracking: {}
  };
  function initHistory() {
    for (var i = 0; i < data.panels.length; i++) {
      var p = data.panels[i];
      if (p.history.length === 0) {
        var base = p.value;
        for (var j = 0; j < 30; j++) {
          p.history.push(base + (Math.random() - 0.5) * base * 0.2);
        }
      }
    }
  }
  function load() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var saved = JSON.parse(raw);
        if (saved.panels) { data.panels = saved.panels; }
        if (saved.tracking) { data.tracking = saved.tracking; }
      }
    } catch(e) {}
    initHistory();
    ensureTracking();
  }
  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ panels: data.panels, tracking: data.tracking }));
    } catch(e) {}
  }
  function ensureTracking() {
    for (var i = 0; i < data.panels.length; i++) {
      var id = data.panels[i].id;
      if (!data.tracking[id]) {
        data.tracking[id] = { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0, locked: false };
      }
    }
  }
  function getPanels() { return data.panels; }
  function getPanel(id) {
    for (var i = 0; i < data.panels.length; i++) {
      if (data.panels[i].id === id) return data.panels[i];
    }
    return null;
  }
  function getTracking() { return data.tracking; }
  function getTrackingFor(id) { return data.tracking[id] || null; }
  function recordView(id, durationMs) {
    var t = data.tracking[id];
    if (!t) return;
    t.viewCount += 1;
    t.totalDuration += durationMs;
    t.lastViewed = Date.now();
  }
  function recordInteraction(id) {
    var t = data.tracking[id];
    if (t) { t.interactions += 1; t.lastViewed = Date.now(); }
  }
  function setLocked(id, locked) {
    var t = data.tracking[id];
    if (t) { t.locked = locked; }
  }
  function isLocked(id) {
    var t = data.tracking[id];
    return t ? t.locked : false;
  }
  load();
  function simulateUpdate() {
    for (var i = 0; i < data.panels.length; i++) {
      var p = data.panels[i];
      var delta = (Math.random() - 0.5) * p.value * 0.08;
      p.value = Math.max(0, Math.round((p.value + delta) * 100) / 100);
      p.change = Math.round((Math.random() - 0.4) * 15 * 10) / 10;
      p.history.push(p.value);
      if (p.history.length > 40) { p.history.shift(); }
    }
    save();
  }
  setInterval(simulateUpdate, 4000);
  return {
    getPanels: getPanels,
    getPanel: getPanel,
    getTracking: getTracking,
    getTrackingFor: getTrackingFor,
    recordView: recordView,
    recordInteraction: recordInteraction,
    setLocked: setLocked,
    isLocked: isLocked,
    save: save,
    load: load
  };
})();
var Ranker = (function() {
  var RECENCY_DECAY = 1 / (1000 * 60 * 60);
  function computeScore(id, tracking) {
    var t = tracking;
    var freq = t.viewCount;
    var dur = t.totalDuration / 1000;
    var recency = Math.exp(-RECENCY_DECAY * Math.max(0, Date.now() - t.lastViewed));
    var interactionBonus = 1 + Math.log(1 + t.interactions) * 0.5;
    var score = (freq * 1.5 + dur * 0.8 + recency * 50) * interactionBonus;
    return Math.round(score * 100) / 100;
  }
  function getRanked() {
    var panels = DataStore.getPanels();
    var tracking = DataStore.getTracking();
    var ranked = [];
    for (var i = 0; i < panels.length; i++) {
      var p = panels[i];
      var t = tracking[p.id] || { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0, locked: false };
      ranked.push({
        panel: p,
        score: computeScore(p.id, t),
        locked: t.locked
      });
    }
    ranked.sort(function(a, b) { return b.score - a.score; });
    return ranked;
  }
  return { getRanked: getRanked, computeScore: computeScore };
})();
var Drawer = (function() {
  function sparkline(history, color, width, height, baseline, range) {
    if (!history || history.length === 0) {
      return '<svg viewBox="0 0 ' + width + ' ' + height + '"><text x="' + (width/2) + '" y="' + (height/2) + '" text-anchor="middle" fill="#555" font-size="10">no data</text></svg>';
    }
    if (history.length === 1) {
      var y = height / 2;
      return '<svg viewBox="0 0 ' + width + ' ' + height + '"><line x1="0" y1="' + y + '" x2="' + width + '" y2="' + y + '" stroke="' + color + '" stroke-width="1.5" stroke-dasharray="3,3"/><circle cx="' + (width/2) + '" cy="' + y + '" r="3" fill="' + color + '"/></svg>';
    }
    var bl = (baseline !== undefined && isValidNum(baseline)) ? baseline : null;
    var rng = (range !== undefined && isValidNum(range)) ? range : null;
    var min = Infinity, max = -Infinity;
    for (var i = 0; i < history.length; i++) {
      var v = history[i];
      if (!isValidNum(v)) continue;
      if (v < min) min = v;
      if (v > max) max = v;
    }
    if (!isFinite(min) || !isFinite(max)) {
      return '<svg viewBox="0 0 ' + width + ' ' + height + '"><text x="' + (width/2) + '" y="' + (height/2) + '" text-anchor="middle" fill="#555" font-size="10">invalid data</text></svg>';
    }
    if (max - min < 1e-10) {
      max = min + 1;
    }
    if (rng !== null && rng > 0) {
      var center = bl !== null ? bl : (min + max) / 2;
      min = center - rng / 2;
      max = center + rng / 2;
    }
    var margin = 2;
    var plotH = height - margin * 2;
    var step = (history.length > 1) ? (width - 2) / (history.length - 1) : 0;
    var points = [];
    for (var i2 = 0; i2 < history.length; i2++) {
      var v2 = history[i2];
      if (!isValidNum(v2)) v2 = (points.length > 0) ? points[points.length - 1].y : height / 2;
      var x = 1 + i2 * step;
      var y2 = margin + plotH - ((v2 - min) / (max - min)) * plotH;
      if (!isFinite(y2)) y2 = margin + plotH / 2;
      y2 = clamp(y2, margin, margin + plotH);
      points.push({ x: x, y: y2 });
    }
    var d = '';
    for (var i3 = 0; i3 < points.length; i3++) {
      d += (i3 === 0 ? 'M' : 'L') + points[i3].x.toFixed(1) + ' ' + points[i3].y.toFixed(1) + ' ';
    }
    var fillPath = d + 'L' + points[points.length - 1].x.toFixed(1) + ' ' + (margin + plotH) + ' L1 ' + (margin + plotH) + ' Z';
    return '<svg viewBox="0 0 ' + width + ' ' + height + '">'
      + '<defs><linearGradient id="sg-' + color.replace('#','') + '" x1="0" y1="0" x2="0" y2="1">'
      + '<stop offset="0%" stop-color="' + color + '" stop-opacity="0.25"/>'
      + '<stop offset="100%" stop-color="' + color + '" stop-opacity="0.02"/>'
      + '</linearGradient></defs>'
      + '<path d="' + fillPath + '" fill="url(#sg-' + color.replace('#','') + ')" stroke="none"/>'
      + '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<circle cx="' + points[points.length - 1].x.toFixed(1) + '" cy="' + points[points.length - 1].y.toFixed(1) + '" r="3" fill="' + color + '"/>'
      + '</svg>';
  }
  return { sparkline: sparkline };
})();
var Renderer = (function() {
  var VIEW_TIMERS = {};
  var INTERSECTION_OBSERVER = null;
  var panelElMap = {};
  function init(elMap) {
    panelElMap = elMap || {};
    if (typeof IntersectionObserver !== 'undefined') {
      INTERSECTION_OBSERVER = new IntersectionObserver(function(entries) {
        for (var i = 0; i < entries.length; i++) {
          var entry = entries[i];
          var panelId = entry.target.dataset.panelId;
          if (entry.isIntersecting) {
            VIEW_TIMERS[panelId] = Date.now();
          } else if (VIEW_TIMERS[panelId]) {
            var duration = Date.now() - VIEW_TIMERS[panelId];
            DataStore.recordView(panelId, duration);
            delete VIEW_TIMERS[panelId];
          }
        }
      }, { threshold: 0.3 });
    }
  }
  function observePanel(el, panelId) {
    if (INTERSECTION_OBSERVER && el) {
      INTERSECTION_OBSERVER.observe(el);
    }
    VIEW_TIMERS[panelId] = Date.now();
  }
  function unobservePanel(el) {
    if (INTERSECTION_OBSERVER && el) {
      INTERSECTION_OBSERVER.unobserve(el);
    }
  }
  function flushViewTimers() {
    var keys = Object.keys(VIEW_TIMERS);
    for (var i = 0; i < keys.length; i++) {
      var duration = Date.now() - VIEW_TIMERS[keys[i]];
      DataStore.recordView(keys[i], duration);
    }
    VIEW_TIMERS = {};
  }
  function renderPanel(panel, rank, totalPanels, el) {
    if (!el) return;
    var tracking = DataStore.getTrackingFor(panel.id) || { locked: false };
    var compact = rank > Math.floor(totalPanels * 0.6);
    var isLocked = tracking.locked;
    el.dataset.rank = rank;
    el.dataset.panelId = panel.id;
    if (el.classList.contains('compact') !== compact) {
      el.classList.toggle('compact', compact);
    }
    if (el.classList.contains('normal') !== !compact) {
      el.classList.toggle('normal', !compact);
    }
    var headerEl = el.querySelector('.panel-header');
    if (!headerEl) return;
    var lockBtn = headerEl.querySelector('.panel-btn.lock-btn');
    if (lockBtn) {
      if (lockBtn.classList.contains('locked') !== isLocked) {
        lockBtn.classList.toggle('locked', isLocked);
      }
      lockBtn.textContent = isLocked ? '\u{1F512}' : '\u{1F513}';
    }
    var badge = headerEl.querySelector('.rank-badge');
    if (badge) {
      badge.textContent = '#' + (rank + 1) + ' score:' + Math.round(Ranker.computeScore(panel.id, tracking));
    }
    var bodyFull = el.querySelector('.panel-body.full-mode');
    if (bodyFull) {
      var valEl = bodyFull.querySelector('.metric-value');
      if (valEl && valEl.textContent !== String(panel.value) + panel.unit) {
        valEl.textContent = panel.value + panel.unit;
      }
      var changeEl = bodyFull.querySelector('.metric-change');
      if (changeEl) {
        var sign = panel.change >= 0 ? '+' : '';
        var cls = panel.change >= 0 ? 'up' : 'down';
        var newText = sign + panel.change + panel.unit;
        if (changeEl.textContent !== newText) {
          changeEl.textContent = newText;
          changeEl.className = 'metric-change ' + cls;
        }
      }
      var svgContainer = bodyFull.querySelector('.sparkline-container');
      if (svgContainer && panel.history) {
        var svg = Drawer.sparkline(panel.history, panel.color, 200, 48, null, null);
        if (svgContainer.innerHTML !== svg) {
          svgContainer.innerHTML = svg;
        }
      }
    }
    var bodyCompact = el.querySelector('.panel-body.compact-mode');
    if (bodyCompact) {
      var cVal = bodyCompact.querySelector('.metric-value');
      if (cVal && cVal.textContent !== String(Math.round(panel.value)) + panel.unit) {
        cVal.textContent = Math.round(panel.value) + panel.unit;
      }
    }
  }
  function rebuildDashboard(container) {
    var panels = DataStore.getPanels();
    var ranked = Ranker.getRanked();
    var existingEls = {};
    var children = container.children;
    for (var i = children.length - 1; i >= 0; i--) {
      var c = children[i];
      var pid = c.dataset.panelId;
      if (pid) { existingEls[pid] = c; }
      else { container.removeChild(c); }
    }
    var lockedPanels = [];
    var unlockedPanels = [];
    for (var r = 0; r < ranked.length; r++) {
      var item = ranked[r];
      var el = existingEls[item.panel.id];
      if (!el) {
        el = createPanelElement(item.panel);
        container.appendChild(el);
        observePanel(el, item.panel.id);
      }
      panelElMap[item.panel.id] = el;
      if (item.locked) {
        lockedPanels.push({ panel: item.panel, rank: r, el: el, score: item.score });
      } else {
        unlockedPanels.push({ panel: item.panel, rank: r, el: el, score: item.score });
      }
    }
    var combined = lockedPanels.concat(unlockedPanels);
    for (var i2 = 0; i2 < combined.length; i2++) {
      var it = combined[i2];
      el = it.el;
      var effectiveRank = it.rank;
      if (combined[i2] === lockedPanels[0] && lockedPanels.length > 0) {
        effectiveRank = 0;
      }
      renderPanel(it.panel, effectiveRank, ranked.length, el);
      container.appendChild(el);
    }
  }
  function updateValues(container) {
    var panels = DataStore.getPanels();
    var ranked = Ranker.getRanked();
    for (var i = 0; i < panels.length; i++) {
      var p = panels[i];
      var el = container.querySelector('[data-panel-id="' + p.id + '"]');
      if (!el) continue;
      var rank = 0;
      for (var j = 0; j < ranked.length; j++) {
        if (ranked[j].panel.id === p.id) { rank = j; break; }
      }
      renderPanel(p, rank, ranked.length, el);
    }
  }
  function createPanelElement(panel) {
    var el = document.createElement('div');
    el.className = 'panel compact';
    el.dataset.panelId = panel.id;
    el.draggable = true;
    el.innerHTML =
      '<div class="panel-header">'
      + '<span class="drag-handle">\u2630</span>'
      + '<span class="panel-title">' + panel.title + '</span>'
      + '<span class="rank-badge">#--</span>'
      + '<div class="panel-controls">'
      + '<button class="panel-btn lock-btn" title="Lock/unlock position">\u{1F513}</button>'
      + '</div>'
      + '</div>'
      + '<div class="panel-body full-mode">'
      + '<div class="metric-label">' + panel.title + '</div>'
      + '<div class="metric-value">' + panel.value + panel.unit + '</div>'
      + '<div class="metric-change up">' + (panel.change >= 0 ? '+' : '') + panel.change + panel.unit + '</div>'
      + '<div class="sparkline-container"></div>'
      + '</div>'
      + '<div class="panel-body compact-mode">'
      + '<div class="metric-label">' + panel.title + '</div>'
      + '<div class="metric-value">' + Math.round(panel.value) + panel.unit + '</div>'
      + '</div>';
    el.querySelector('.lock-btn').addEventListener('click', function(e) {
      e.stopPropagation();
      var id = el.dataset.panelId;
      var currentlyLocked = DataStore.isLocked(id);
      DataStore.setLocked(id, !currentlyLocked);
      DataStore.recordInteraction(id);
      DataStore.save();
      enqueueMutation(function() { updateValues($els.dashboard); });
    });
    return el;
  }
  return {
    init: init,
    observePanel: observePanel,
    unobservePanel: unobservePanel,
    flushViewTimers: flushViewTimers,
    renderPanel: renderPanel,
    rebuildDashboard: rebuildDashboard,
    updateValues: updateValues,
    createPanelElement: createPanelElement
  };
})();
var Controller = (function() {
  var dragState = null;
  var rebuildTimeout = null;
  function init() {
    $els.dashboard = document.getElementById('dashboard');
    $els.debugLog = document.getElementById('debug-log');
    if (!$els.dashboard) return;
    Renderer.init({});
    Renderer.rebuildDashboard($els.dashboard);
    setupDragAndDrop($els.dashboard);
    setupToolbar();
    setupPeriodicRebuild();
    window.addEventListener('beforeunload', function() {
      Renderer.flushViewTimers();
      DataStore.save();
    });
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        Renderer.flushViewTimers();
      }
    });
  }
  function setupDragAndDrop(container) {
    container.addEventListener('dragstart', function(e) {
      var panel = e.target.closest('.panel');
      if (!panel) return;
      var id = panel.dataset.panelId;
      if (DataStore.isLocked(id)) {
        e.preventDefault();
        log('Panel locked - unlock to drag');
        return;
      }
      dragState = { source: panel, sourceId: id };
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', id);
      DataStore.recordInteraction(id);
      setTimeout(function() { panel.classList.add('dragging'); }, 0);
    });
    container.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      var target = e.target.closest('.panel');
      var prevTarget = container.querySelector('.panel.drag-target');
      if (prevTarget && prevTarget !== target) { prevTarget.classList.remove('drag-target'); }
      if (target && target !== dragState && dragState && target !== dragState.source) {
        target.classList.add('drag-target');
      }
    });
    container.addEventListener('drop', function(e) {
      e.preventDefault();
      var target = e.target.closest('.panel');
      var prevTarget = container.querySelector('.panel.drag-target');
      if (prevTarget) { prevTarget.classList.remove('drag-target'); }
      if (dragState && dragState.source) {
        dragState.source.classList.remove('dragging');
      }
      if (!dragState || !target || target === dragState.source) {
        dragState = null;
        return;
      }
      var sourceId = dragState.sourceId;
      var targetId = target.dataset.panelId;
      var panels = DataStore.getPanels();
      var srcIdx = -1, tgtIdx = -1;
      for (var i = 0; i < panels.length; i++) {
        if (panels[i].id === sourceId) srcIdx = i;
        if (panels[i].id === targetId) tgtIdx = i;
      }
      if (srcIdx >= 0 && tgtIdx >= 0) {
        var moved = panels.splice(srcIdx, 1)[0];
        panels.splice(tgtIdx, 0, moved);
        DataStore.recordInteraction(sourceId);
        DataStore.recordInteraction(targetId);
        DataStore.save();
        enqueueMutation(function() {
          Renderer.rebuildDashboard(container);
        });
        log('Moved ' + sourceId + ' after ' + targetId);
      }
      dragState = null;
    });
    container.addEventListener('dragend', function(e) {
      var panel = e.target.closest('.panel');
      if (panel) { panel.classList.remove('dragging'); }
      var dt = container.querySelector('.panel.drag-target');
      if (dt) { dt.classList.remove('drag-target'); }
      dragState = null;
    });
  }
  function setupToolbar() {
    var btnReset = document.getElementById('btn-reset-auto');
    var btnSave = document.getElementById('btn-save');
    var btnLog = document.getElementById('btn-log');
    var btnResetData = document.getElementById('btn-reset-data');
    if (btnReset) {
      btnReset.addEventListener('click', function() {
        var tracking = DataStore.getTracking();
        var keys = Object.keys(tracking);
        for (var i = 0; i < keys.length; i++) { tracking[keys[i]].locked = false; }
        DataStore.save();
        enqueueMutation(function() { Renderer.rebuildDashboard($els.dashboard); });
        log('All locks removed');
      });
    }
    if (btnSave) {
      btnSave.addEventListener('click', function() {
        DataStore.save();
        log('Layout saved');
      });
    }
    if (btnLog) {
      btnLog.addEventListener('click', function() {
        var ranked = Ranker.getRanked();
        var lines = [];
        for (var i = 0; i < ranked.length; i++) {
          var r = ranked[i];
          lines.push(r.panel.id + ': score=' + r.score + ' locked=' + r.locked);
        }
        log(lines.join(' | '));
        console.table(ranked.map(function(r){ return { id: r.panel.id, score: r.score, locked: r.locked }; }));
      });
    }
    if (btnResetData) {
      btnResetData.addEventListener('click', function() {
        if (confirm('Wipe all tracking data and reset layout?')) {
          localStorage.removeItem('adaptive_dashboard_data');
          location.reload();
        }
      });
    }
  }
  function setupPeriodicRebuild() {
    setInterval(function() {
      enqueueMutation(function() { Renderer.rebuildDashboard($els.dashboard); });
    }, 15000);
  }
  return { init: init };
})();
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', Controller.init);
} else {
  Controller.init();
}
})();
</script>
</body>
</html>