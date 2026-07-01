<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; background: #0f1117; color: #e1e4e8; min-height: 100vh; }
.header { padding: 16px 24px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 18px; font-weight: 600; }
.controls { display: flex; gap: 8px; }
.controls button { padding: 6px 14px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; color: #c9d1d9; cursor: pointer; font-size: 13px; }
.controls button:hover { background: #30363d; }
.grid { display: grid; gap: 12px; padding: 16px; transition: all 0.3s ease; }
/* All panel CSS classes use size- prefix convention */
.panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; transition: all 0.3s ease; }
.panel-header { padding: 10px 14px; background: #1c2128; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; cursor: move; user-select: none; }
.panel-title { font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 8px; }
.panel-rank { font-size: 11px; color: #8b949e; background: #21262d; padding: 2px 8px; border-radius: 10px; }
.panel-body { padding: 14px; flex: 1; overflow: auto; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button { padding: 4px 8px; border: 1px solid #30363d; border-radius: 4px; background: transparent; color: #8b949e; cursor: pointer; font-size: 12px; }
.panel-actions button:hover { color: #c9d1d9; background: #30363d; }
.panel-actions button.locked { color: #f0883e; border-color: #f0883e; }
.metric-value { font-size: 28px; font-weight: 700; color: #58a6ff; }
.metric-label { font-size: 12px; color: #8b949e; margin-top: 4px; }
.metric-bar { height: 6px; background: #21262d; border-radius: 3px; margin-top: 10px; overflow: hidden; }
.metric-bar-fill { height: 100%; background: linear-gradient(90deg, #238636, #58a6ff); border-radius: 3px; transition: width 0.5s ease; }
.chart-area { min-height: 120px; display: flex; align-items: flex-end; gap: 4px; padding: 8px 0; }
.chart-bar { flex: 1; background: #238636; border-radius: 3px 3px 0 0; min-height: 4px; transition: height 0.3s ease; }
/* size- prefixed panel size classes */
.size-full { grid-column: span 3; grid-row: span 2; }
.size-wide { grid-column: span 2; grid-row: span 2; }
.size-large { grid-column: span 2; grid-row: span 1; }
.size-medium { grid-column: span 1; grid-row: span 1; }
.size-small { grid-column: span 1; grid-row: span 1; }
.size-compact { grid-column: span 1; grid-row: span 1; }
.size-miniature { grid-column: span 1; grid-row: auto; }
.size-collapsed .panel-body { display: none; }
.size-collapsed .panel-header { border-bottom: none; }
/* locked panels get subtle top-border accent */
.panel-locked { border-top: 2px solid #f0883e; }
.more-section { padding: 8px 16px 16px; }
.more-toggle { width: 100%; padding: 10px; background: #21262d; border: 1px dashed #30363d; border-radius: 8px; color: #8b949e; cursor: pointer; font-size: 13px; text-align: center; }
.more-toggle:hover { border-color: #58a6ff; color: #c9d1d9; }
.size-s hrink-indicator { font-size: 11px; color: #f0883e; margin-left: 8px; }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button onclick="resetLayout()">Reset Layout</button>
    <button onclick="resetTracking()">Reset Tracking</button>
    <span style="font-size:12px;color:#8b949e;display:flex;align-items:center;margin-left:8px;">Last adapted: <span id="last-adapted">--</span></span>
  </div>
</div>
<div class="grid" id="grid"></div>
<div class="more-section" id="more-section" style="display:none;">
  <button class="more-toggle" onclick="toggleMore()">Show collapsed panels</button>
  <div class="grid" id="collapsed-grid" style="margin-top:8px;"></div>
</div>
<script>
(function() {
'use strict';
// ── Constants ────────────────────────────────────────────────────
var STORAGE_KEY_TRACKING = 'adaptive_dashboard_tracking';
var STORAGE_KEY_LAYOUT   = 'adaptive_dashboard_layout';
var STORAGE_KEY_MORE     = 'adaptive_dashboard_more_visible';
var VIEW_TIMER_INTERVAL  = 2000; // ms between view duration ticks
var RECENCY_HALF_LIFE    = 7 * 24 * 60 * 60 * 1000; // 7 days in ms
var COMPACT_THRESHOLD    = 0.2; // bottom 20% get compacted
var MINIATURE_THRESHOLD  = 0.1; // bottom 10% get miniature
var COLLAPSE_THRESHOLD   = 0.05; // bottom 5% get collapsed
// ── Panel definitions ────────────────────────────────────────────
var PANEL_DEFS = [
  { id: 'revenue',     title: 'Revenue',         type: 'metric', value: 84720, unit: 'USD', trend: 12 },
  { id: 'users',       title: 'Active Users',    type: 'metric', value: 18432, unit: '',    trend: 8  },
  { id: 'conversion',  title: 'Conversion Rate', type: 'metric', value: 3.24,  unit: '%',   trend: -2 },
  { id: 'churn',       title: 'Churn Rate',      type: 'metric', value: 1.82,  unit: '%',   trend: -5 },
  { id: 'loadtime',    title: 'Page Load Time',  type: 'metric', value: 1.24,  unit: 's',   trend: -15},
  { id: 'errors',      title: 'Error Rate',      type: 'metric', value: 0.42,  unit: '%',   trend: -3 },
  { id: 'latency',     title: 'API Latency',     type: 'chart',  values: [45,52,38,61,44,39,50] },
  { id: 'traffic',     title: 'Traffic Sources', type: 'chart',  values: [65,22,18,8,4,3] },
  { id: 'sessions',    title: 'Sessions',        type: 'chart',  values: [120,145,132,168,155,178,190] },
  { id: 'bandwidth',   title: 'Bandwidth',       type: 'chart',  values: [34,28,45,39,52,41,38] },
  { id: 'uptime',      title: 'Uptime',          type: 'metric', value: 99.97, unit: '%',   trend: 0  },
  { id: 'cpu',         title: 'CPU Usage',       type: 'chart',  values: [32,28,45,38,52,41,48] }
];
// ── Pure: load/save with localStorage edge-case handling ─────────
// Returns parsed data or null on any failure (private browsing, quota, corrupt data)
function safeLoadJSON(key) {
  try {
    var raw = localStorage.getItem(key);
    if (raw === null || raw === undefined) { return null; }
    var parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== 'object') { return null; }
    return parsed;
  } catch (e) {
    // localStorage unavailable (private browsing) or corrupt data
    return null;
  }
}
function safeSaveJSON(key, data) {
  try {
    localStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (e) {
    // quota exceeded or storage unavailable
    return false;
  }
}
// ── Pure: compute attention score for a panel ─────────────────────
// Score = frequency × duration × recency_decay
// frequency: total interactions (clicks, expands, collapses)
// duration: total visible milliseconds
// recency: exponential decay since last interaction
function computeAttentionScore(tracking, panelId, now) {
  var t = tracking[panelId];
  if (!t) { return 0; }
  var freq     = (t.interactions || 0) + 1; // +1 prevents zeroing out
  var duration = (t.totalViewMs || 0) + 1;
  var lastSeen = t.lastInteraction || now;
  var ageMs    = Math.max(0, now - lastSeen);
  var recency  = Math.exp(-ageMs / RECENCY_HALF_LIFE);
  return freq * Math.log(duration + 1) * recency;
}
// ── Pure: reconcile layout → returns diff object (no side effects) ──
// Compares desired state against current state, returns only changes needed
function reconcileLayout(currentSizes, desiredSizes, lockedPanels, collapsedIds) {
  var changes = [];
  var panelIds = Object.keys(desiredSizes);
  for (var i = 0; i < panelIds.length; i++) {
    var pid = panelIds[i];
    var cur = currentSizes[pid] || '';
    var des = desiredSizes[pid];
    var isLocked = lockedPanels.indexOf(pid) !== -1;
    var isCollapsed = collapsedIds.indexOf(pid) !== -1;
    // Collapsed state overrides size class
    if (isCollapsed && cur !== 'size-collapsed') {
      changes.push({ id: pid, action: 'setSize', value: 'size-collapsed', locked: isLocked });
    } else if (!isCollapsed && cur !== des) {
      changes.push({ id: pid, action: 'setSize', value: des, locked: isLocked });
    }
  }
  // Detect panels that disappeared entirely
  for (i = 0; i < panelIds.length; i++) {
    if (desiredSizes[panelIds[i]] === undefined && currentSizes[panelIds[i]]) {
      changes.push({ id: panelIds[i], action: 'remove' });
    }
  }
  return changes;
}
// ── Pure: compute desired size class from score percentile ────────
// All return values use 'size-' prefix convention
function scoreToSizeClass(percentile) {
  if (percentile >= 0.85) { return 'size-full'; }
  if (percentile >= 0.70) { return 'size-wide'; }
  if (percentile >= 0.50) { return 'size-large'; }
  if (percentile >= 0.30) { return 'size-medium'; }
  if (percentile >= COMPACT_THRESHOLD) { return 'size-small'; }
  if (percentile >= MINIATURE_THRESHOLD) { return 'size-compact'; }
  if (percentile >= COLLAPSE_THRESHOLD) { return 'size-miniature'; }
  return 'size-collapsed';
}
// ── State containers ──────────────────────────────────────────────
var tracking    = {};  // { panelId: { interactions, totalViewMs, lastInteraction, expandCount, collapseCount } }
var lockedPanels = []; // panel IDs that user manually locked
var viewTimers   = {}; // active interval IDs for visible panels
var currentSizes = {}; // panelId → current size class (for diffing)
var collapsedIds = []; // panels in collapsed state
var moreVisible  = false;
// ── Init tracking from storage with guard against empty/undefined ─
function initTracking() {
  var saved = safeLoadJSON(STORAGE_KEY_TRACKING);
  if (saved && typeof saved === 'object') {
    tracking = saved;
  } else {
    tracking = {};
  }
  // Ensure all panel IDs have tracking entries
  for (var i = 0; i < PANEL_DEFS.length; i++) {
    var pid = PANEL_DEFS[i].id;
    if (!tracking[pid]) {
      tracking[pid] = { interactions: 0, totalViewMs: 0, lastInteraction: Date.now(), expandCount: 0, collapseCount: 0 };
    }
  }
}
function initLayout() {
  var saved = safeLoadJSON(STORAGE_KEY_LAYOUT);
  if (saved && typeof saved === 'object') {
    lockedPanels = Array.isArray(saved.lockedPanels) ? saved.lockedPanels : [];
    currentSizes = saved.currentSizes && typeof saved.currentSizes === 'object' ? saved.currentSizes : {};
    collapsedIds = Array.isArray(saved.collapsedIds) ? saved.collapsedIds : [];
  } else {
    lockedPanels = [];
    currentSizes = {};
    collapsedIds = [];
  }
  moreVisible = safeLoadJSON(STORAGE_KEY_MORE) === true;
}
// ── Persist helpers (side-effect wrappers around pure save) ──────
function persistTracking() { safeSaveJSON(STORAGE_KEY_TRACKING, tracking); }
function persistLayout() {
  safeSaveJSON(STORAGE_KEY_LAYOUT, {
    lockedPanels: lockedPanels,
    currentSizes: currentSizes,
    collapsedIds: collapsedIds
  });
}
function persistMoreVisible() { safeSaveJSON(STORAGE_KEY_MORE, moreVisible); }
// ── Tracking: start view timer for visible panels ─────────────────
function startViewTimer(panelId) {
  if (viewTimers[panelId]) { return; } // already tracking
  viewTimers[panelId] = setInterval(function() {
    if (!tracking[panelId]) { return; }
    tracking[panelId].totalViewMs = (tracking[panelId].totalViewMs || 0) + VIEW_TIMER_INTERVAL;
    persistTracking();
  }, VIEW_TIMER_INTERVAL);
}
function stopViewTimer(panelId) {
  if (viewTimers[panelId]) {
    clearInterval(viewTimers[panelId]);
    delete viewTimers[panelId];
  }
}
// ── Tracking: record interaction ──────────────────────────────────
function recordInteraction(panelId) {
  if (!tracking[panelId]) { return; }
  tracking[panelId].interactions = (tracking[panelId].interactions || 0) + 1;
  tracking[panelId].lastInteraction = Date.now();
  persistTracking();
}
// ── Tracking: record expand/collapse ──────────────────────────────
function recordExpand(panelId) {
  if (!tracking[panelId]) { return; }
  tracking[panelId].expandCount = (tracking[panelId].expandCount || 0) + 1;
  tracking[panelId].interactions = (tracking[panelId].interactions || 0) + 1;
  tracking[panelId].lastInteraction = Date.now();
  persistTracking();
}
function recordCollapse(panelId) {
  if (!tracking[panelId]) { return; }
  tracking[panelId].collapseCount = (tracking[panelId].collapseCount || 0) + 1;
  tracking[panelId].interactions = (tracking[panelId].interactions || 0) + 1;
  tracking[panelId].lastInteraction = Date.now();
  persistTracking();
}
// ── Layout: compute ranked order with locked-panels-to-top ────────
// Locked panels always sort to the top of the grid; never to the bottom.
function computeRankedOrder() {
  var now = Date.now();
  var scored = [];
  for (var i = 0; i < PANEL_DEFS.length; i++) {
    var pid = PANEL_DEFS[i].id;
    var score = computeAttentionScore(tracking, pid, now);
    scored.push({ id: pid, score: score });
  }
  // Sort by locked-first, then by score descending
  scored.sort(function(a, b) {
    var aLocked = lockedPanels.indexOf(a.id) !== -1 ? 1 : 0;
    var bLocked = lockedPanels.indexOf(b.id) !== -1 ? 1 : 0;
    if (aLocked !== bLocked) { return bLocked - aLocked; } // locked first
    return b.score - a.score; // then by score descending
  });
  return scored;
}
// ── Layout: compute desired sizes from ranked order ───────────────
function computeDesiredSizes(rankedOrder) {
  var n = rankedOrder.length;
  var desiredSizes = {};
  for (var i = 0; i < n; i++) {
    var percentile = 1 - (i / Math.max(n - 1, 1)); // first = 1.0, last ≈ 0
    var pid = rankedOrder[i].id;
    desiredSizes[pid] = scoreToSizeClass(percentile);
  }
  return desiredSizes;
}
// ── DOM: apply diff changes via modular patching (not full rebuild) ──
function applyDiffChanges(changes) {
  var grid = document.getElementById('grid');
  var collapsedGrid = document.getElementById('collapsed-grid');
  var moreSection = document.getElementById('more-section');
  for (var i = 0; i < changes.length; i++) {
    var ch = changes[i];
    if (ch.action === 'remove') {
      var el = document.getElementById('panel-' + ch.id);
      if (el) { el.remove(); }
      continue;
    }
    if (ch.action === 'setSize') {
      var panel = document.getElementById('panel-' + ch.id);
      if (!panel) { continue; }
      // Remove all size- prefixed classes, then add the new one
      var classes = panel.className.split(' ');
      var kept = [];
      for (var j = 0; j < classes.length; j++) {
        if (classes[j].indexOf('size-') !== 0) { kept.push(classes[j]); }
      }
      kept.push(ch.value);
      // Toggle locked class
      if (ch.locked && kept.indexOf('panel-locked') === -1) { kept.push('panel-locked'); }
      else if (!ch.locked) {
        var lockIdx = kept.indexOf('panel-locked');
        if (lockIdx !== -1) { kept.splice(lockIdx, 1); }
      }
      panel.className = kept.join(' ');
      // Move panel to correct parent container
      if (ch.value === 'size-collapsed') {
        if (panel.parentNode !== collapsedGrid) {
          // Save current size before collapsing for restore
          currentSizes[ch.id] = currentSizes[ch.id] || 'size-medium';
          collapsedGrid.appendChild(panel);
        }
      } else {
        if (panel.parentNode !== grid && panel.parentNode === collapsedGrid) {
          grid.appendChild(panel);
        }
      }
    }
  }
  // Show/hide more section
  moreSection.style.display = collapsedGrid.children.length > 0 ? 'block' : 'none';
}
// ── Layout: full adaptation cycle ─────────────────────────────────
function adaptLayout() {
  var ranked = computeRankedOrder();
  var desiredSizes = computeDesiredSizes(ranked);
  // Build list of currently collapsed panels
  var collGrid = document.getElementById('collapsed-grid');
  collapsedIds = [];
  for (var c = 0; c < collGrid.children.length; c++) {
    var cid = collGrid.children[c].id.replace('panel-', '');
    collapsedIds.push(cid);
  }
  // Pure reconciliation: compute diff
  var changes = reconcileLayout(currentSizes, desiredSizes, lockedPanels, collapsedIds);
  // Apply side effects: update currentSizes and DOM
  for (var i = 0; i < changes.length; i++) {
    if (changes[i].action === 'setSize') {
      currentSizes[changes[i].id] = changes[i].value;
    } else if (changes[i].action === 'remove') {
      delete currentSizes[changes[i].id];
    }
  }
  // Apply DOM patches
  applyDiffChanges(changes);
  // Reorder DOM children in grid to match ranked order (locked-first, then score)
  reorderGridChildren(ranked);
  persistLayout();
  updateAdaptedTimestamp();
  // Restart view timers for visible panels
  restartViewTimers();
}
// ── DOM: reorder grid children to match ranked order ──────────────
// Locked panels sort to top first, then by score within each group
function reorderGridChildren(rankedOrder) {
  var grid = document.getElementById('grid');
  var orderMap = {};
  for (var i = 0; i < rankedOrder.length; i++) {
    orderMap[rankedOrder[i].id] = i;
  }
  var children = Array.prototype.slice.call(grid.children);
  children.sort(function(a, b) {
    var aId = a.id.replace('panel-', '');
    var bId = b.id.replace('panel-', '');
    var aIdx = orderMap[aId] !== undefined ? orderMap[aId] : 999;
    var bIdx = orderMap[bId] !== undefined ? orderMap[bId] : 999;
    return aIdx - bIdx;
  });
  for (var j = 0; j < children.length; j++) {
    grid.appendChild(children[j]);
  }
}
// ── View timer management ─────────────────────────────────────────
function restartViewTimers() {
  // Stop all existing timers
  var keys = Object.keys(viewTimers);
  for (var i = 0; i < keys.length; i++) { stopViewTimer(keys[i]); }
  // Start timers for panels visible in main grid (not collapsed)
  var grid = document.getElementById('grid');
  for (var j = 0; j < grid.children.length; j++) {
    var pid = grid.children[j].id.replace('panel-', '');
    startViewTimer(pid);
  }
}
// ── DOM: build initial panel elements (one-time full build) ───────
function buildInitialPanels() {
  var grid = document.getElementById('grid');
  var fragment = document.createDocumentFragment();
  for (var i = 0; i < PANEL_DEFS.length; i++) {
    var def = PANEL_DEFS[i];
    var panel = document.createElement('div');
    panel.className = 'panel ' + (currentSizes[def.id] || 'size-medium');
    if (lockedPanels.indexOf(def.id) !== -1) {
      panel.className += ' panel-locked';
    }
    panel.id = 'panel-' + def.id;
    panel.setAttribute('draggable', 'true');
    // Header
    var header = document.createElement('div');
    header.className = 'panel-header';
    header.innerHTML = '<span class="panel-title">' + escapeHtml(def.title) + '</span>' +
      '<div class="panel-actions">' +
        '<button class="' + (lockedPanels.indexOf(def.id) !== -1 ? 'locked' : '') + '" data-action="lock" data-panel="' + def.id + '" title="Lock position">&#128274;</button>' +
        '<button data-action="collapse" data-panel="' + def.id + '" title="Collapse/Expand">&#9660;</button>' +
      '</div>';
    // Body
    var body = document.createElement('div');
    body.className = 'panel-body';
    body.innerHTML = renderPanelContent(def);
    panel.appendChild(header);
    panel.appendChild(body);
    // Event delegation on the panel element
    panel.addEventListener('click', function(e) {
      var btn = e.target.closest('button');
      if (!btn) { return; }
      var action = btn.getAttribute('data-action');
      var pid = btn.getAttribute('data-panel');
      if (!action || !pid) { return; }
      e.stopPropagation();
      if (action === 'lock') { toggleLock(pid, btn); }
      else if (action === 'collapse') { toggleCollapse(pid); }
    });
    // Drag events
    panel.addEventListener('dragstart', function(e) {
      e.dataTransfer.setData('text/plain', this.id.replace('panel-', ''));
      this.style.opacity = '0.5';
    });
    panel.addEventListener('dragend', function(e) {
      this.style.opacity = '1';
    });
    // Hover tracking
    panel.addEventListener('mouseenter', function() {
      var pid = this.id.replace('panel-', '');
      startViewTimer(pid);
    });
    panel.addEventListener('mouseleave', function() {
      var pid = this.id.replace('panel-', '');
      stopViewTimer(pid);
    });
    fragment.appendChild(panel);
  }
  grid.appendChild(fragment);
  // Setup grid drop zones
  grid.addEventListener('dragover', function(e) { e.preventDefault(); });
  grid.addEventListener('drop', function(e) {
    e.preventDefault();
    var pid = e.dataTransfer.getData('text/plain');
    if (!pid) { return; }
    recordInteraction(pid);
    // Manual reorder: lock the dragged panel
    if (lockedPanels.indexOf(pid) === -1) {
      lockedPanels.push(pid);
      // Update lock button visual
      var lockBtn = document.querySelector('#panel-' + pid + ' [data-action="lock"]');
      if (lockBtn) { lockBtn.className = 'locked'; }
      var panelEl = document.getElementById('panel-' + pid);
      if (panelEl && panelEl.className.indexOf('panel-locked') === -1) {
        panelEl.className += ' panel-locked';
      }
    }
    adaptLayout();
  });
}
// ── Render panel content based on type ────────────────────────────
function renderPanelContent(def) {
  if (def.type === 'metric') {
    var trendClass = def.trend > 0 ? 'color:#3fb950' : (def.trend < 0 ? 'color:#f85149' : 'color:#8b949e');
    var trendArrow = def.trend > 0 ? '&#9650;' : (def.trend < 0 ? '&#9660;' : '&#9644;');
    var trendPct = Math.abs(def.trend);
    return '<div class="metric-value">' + def.value.toLocaleString() + (def.unit ? '<span style="font-size:16px;color:#8b949e;"> ' + escapeHtml(def.unit) + '</span>' : '') + '</div>' +
      '<div class="metric-label">' + escapeHtml(def.title) + ' <span style="' + trendClass + '">' + trendArrow + ' ' + trendPct + '%</span></div>' +
      '<div class="metric-bar"><div class="metric-bar-fill" style="width:' + Math.min(100, Math.max(0, 50 + def.trend * 3)) + '%"></div></div>';
  }
  if (def.type === 'chart') {
    var max = Math.max.apply(null, def.values);
    var bars = '';
    for (var i = 0; i < def.values.length; i++) {
      var h = max > 0 ? (def.values[i] / max) * 100 : 0;
      bars += '<div class="chart-bar" style="height:' + Math.max(4, h) + '%;" title="' + def.values[i] + '"></div>';
    }
    return '<div class="chart-area">' + bars + '</div>' +
      '<div class="metric-label">' + def.values.join(' | ') + '</div>';
  }
  return '<div style="color:#8b949e;">Unknown panel type</div>';
}
// ── Escape HTML ───────────────────────────────────────────────────
function escapeHtml(str) {
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}
// ── Actions ───────────────────────────────────────────────────────
function toggleLock(panelId, btn) {
  recordInteraction(panelId);
  var idx = lockedPanels.indexOf(panelId);
  if (idx === -1) {
    lockedPanels.push(panelId);
    btn.className = 'locked';
    var panelEl = document.getElementById('panel-' + panelId);
    if (panelEl && panelEl.className.indexOf('panel-locked') === -1) {
      panelEl.className += ' panel-locked';
    }
  } else {
    lockedPanels.splice(idx, 1);
    btn.className = '';
    var pel = document.getElementById('panel-' + panelId);
    if (pel) {
      pel.className = pel.className.replace(/\s*panel-locked/g, '');
    }
  }
  adaptLayout();
}
function toggleCollapse(panelId) {
  var panel = document.getElementById('panel-' + panelId);
  if (!panel) { return; }
  var isCollapsed = panel.className.indexOf('size-collapsed') !== -1;
  if (isCollapsed) {
    recordExpand(panelId);
    panel.className = panel.className.replace(/\s*size-collapsed/g, '');
    if (!panel.className.match(/size-/)) { panel.className += ' size-medium'; }
    currentSizes[panelId] = panel.className.match(/size-\w+/)[0];
    document.getElementById('grid').appendChild(panel);
  } else {
    recordCollapse(panelId);
    currentSizes[panelId] = panel.className.match(/size-\w+/)[0];
    panel.className = panel.className.replace(/\s*size-\w+/g, '');
    panel.className += ' size-collapsed';
    document.getElementById('collapsed-grid').appendChild(panel);
  }
  // Update more section visibility
  var moreSection = document.getElementById('more-section');
  var collGrid = document.getElementById('collapsed-grid');
  moreSection.style.display = collGrid.children.length > 0 ? 'block' : 'none';
  restartViewTimers();
  persistLayout();
}
function toggleMore() {
  moreVisible = !moreVisible;
  var collGrid = document.getElementById('collapsed-grid');
  collGrid.style.display = moreVisible ? '' : 'none';
  var toggle = document.querySelector('.more-toggle');
  if (toggle) {
    toggle.textContent = moreVisible ? 'Hide collapsed panels' : 'Show collapsed panels (' + collGrid.children.length + ')';
  }
  persistMoreVisible();
}
function resetLayout() {
  lockedPanels = [];
  currentSizes = {};
  collapsedIds = [];
  var collGrid = document.getElementById('collapsed-grid');
  var grid = document.getElementById('grid');
  // Move all collapsed panels back to main grid
  while (collGrid.firstChild) {
    var child = collGrid.firstChild;
    child.className = child.className.replace(/\s*size-collapsed/g, ' size-medium');
    grid.appendChild(child);
  }
  persistLayout();
  adaptLayout();
}
function resetTracking() {
  tracking = {};
  for (var i = 0; i < PANEL_DEFS.length; i++) {
    var pid = PANEL_DEFS[i].id;
    tracking[pid] = { interactions: 0, totalViewMs: 0, lastInteraction: Date.now(), expandCount: 0, collapseCount: 0 };
  }
  persistTracking();
  adaptLayout();
}
function updateAdaptedTimestamp() {
  var el = document.getElementById('last-adapted');
  if (el) {
    el.textContent = new Date().toLocaleTimeString();
  }
}
// ── Periodic adaptation ───────────────────────────────────────────
// Runs every 30 seconds to let tracking data accumulate
var adaptationInterval = setInterval(adaptLayout, 30000);
// ── Bootstrap ─────────────────────────────────────────────────────
initTracking();
initLayout();
buildInitialPanels();
// Apply more section visibility
var moreSection = document.getElementById('more-section');
var collGrid = document.getElementById('collapsed-grid');
if (collGrid.children.length > 0) {
  moreSection.style.display = 'block';
  collGrid.style.display = moreVisible ? '' : 'none';
  var toggle = document.querySelector('.more-toggle');
  if (toggle) {
    toggle.textContent = moreVisible ? 'Hide collapsed panels' : 'Show collapsed panels (' + collGrid.children.length + ')';
  }
}
// Run initial adaptation to set sizes based on stored tracking
adaptLayout();
updateAdaptedTimestamp();
})();
</script>
</body>
</html>