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
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-muted: #8b90a0;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --green: #4ade80;
  --red: #f87171;
  --yellow: #fbbf24;
  --compact-factor: 1;
  --grid-gap: 12px;
  --transition-speed: 0.35s;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px; border-bottom: 1px solid var(--border);
  background: var(--surface); position: sticky; top: 0; z-index: 100;
}
header h1 { font-size: 18px; font-weight: 600; letter-spacing: -0.3px; }
.header-actions { display: flex; gap: 10px; align-items: center; }
.btn {
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 7px 14px; border-radius: 7px; cursor: pointer; font-size: 13px;
  transition: all var(--transition-speed); display: flex; align-items: center; gap: 6px;
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.status-dot.tracking { background: var(--green); box-shadow: 0 0 6px var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.dashboard {
  display: grid; gap: var(--grid-gap); padding: 16px;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  transition: all var(--transition-speed);
}
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px; position: relative;
  transition: all var(--transition-speed); cursor: grab;
  display: flex; flex-direction: column; overflow: hidden;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel:active { cursor: grabbing; }
.panel.dragging { opacity: 0.6; z-index: 50; transform: scale(0.98); }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 30px var(--accent-glow); background: var(--surface-hover); }
.panel.rank-high { grid-column: span 2; grid-row: span 2; }
.panel.rank-medium { grid-column: span 1; grid-row: span 1; }
.panel.rank-low { grid-column: span 1; grid-row: span 1; }
.panel.compact {
  grid-column: span 1; grid-row: span 1; padding: 10px 12px;
  max-height: 120px; font-size: 12px;
}
.panel.compact .panel-content { transform: scale(var(--compact-factor)); transform-origin: top left; opacity: 0.7; }
.panel.compact .panel-controls { top: 4px; right: 6px; }
.panel.collapsed { grid-column: span 1; grid-row: span 1; max-height: 44px; padding: 8px 12px; font-size: 12px; }
.panel.collapsed .panel-content { display: none; }
.panel.locked { border-left: 3px solid var(--yellow); }
.panel.locked::after {
  content: 'locked'; position: absolute; top: 6px; left: 8px;
  font-size: 10px; color: var(--yellow); text-transform: uppercase; letter-spacing: 1px;
}
.panel-controls {
  position: absolute; top: 8px; right: 10px; display: flex; gap: 4px;
  opacity: 0; transition: opacity var(--transition-speed); z-index: 5;
}
.panel:hover .panel-controls { opacity: 1; }
.panel-btn {
  width: 24px; height: 24px; border-radius: 5px; border: 1px solid var(--border);
  background: var(--surface); color: var(--text-muted); cursor: pointer;
  display: flex; align-items: center; justify-content: center; font-size: 12px;
  transition: all 0.2s;
}
.panel-btn:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
.panel-btn.lock-btn.locked { background: var(--yellow); color: #000; border-color: var(--yellow); }
.panel-header { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 500; }
.panel-value { font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 1; }
.panel-sub { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.panel-sub.up { color: var(--green); }
.panel-sub.down { color: var(--red); }
.sparkline { margin-top: auto; height: 50px; }
.sparkline svg { width: 100%; height: 100%; }
.more-section {
  margin: 0 16px 16px; padding: 10px 16px; border: 1px dashed var(--border);
  border-radius: 8px; color: var(--text-muted); font-size: 13px;
  display: flex; align-items: center; gap: 8px; cursor: pointer;
  transition: all var(--transition-speed);
}
.more-section:hover { border-color: var(--accent); color: var(--text); }
.more-section .count { background: var(--accent); color: #fff; border-radius: 10px; padding: 2px 8px; font-size: 11px; }
.more-panels { display: none; padding: 0 16px 16px; }
.more-panels.open { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--grid-gap); }
.attention-badge {
  position: absolute; top: 6px; left: 8px; font-size: 10px; color: var(--accent);
  opacity: 0; transition: opacity 0.3s;
}
.panel.rank-high .attention-badge { opacity: 0.9; }
.heatmap-indicator {
  position: absolute; inset: 0; border-radius: 10px; pointer-events: none;
  transition: box-shadow 1s;
}
.panel.rank-high .heatmap-indicator { box-shadow: inset 0 0 40px rgba(108,140,255,0.08); }
.toast {
  position: fixed; bottom: 20px; right: 20px; background: var(--surface);
  border: 1px solid var(--border); padding: 10px 16px; border-radius: 8px;
  font-size: 13px; z-index: 200; opacity: 0; transform: translateY(10px);
  transition: all 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.manual-order-indicator {
  background: var(--accent); color: #fff; font-size: 10px; padding: 1px 6px;
  border-radius: 4px; position: absolute; bottom: 8px; right: 8px; display: none;
}
.panel.manually-placed .manual-order-indicator { display: block; }
@media (max-width: 1200px) { .dashboard { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <span class="status-dot tracking" id="trackingStatus" title="Tracking active"></span>
    <span style="font-size:12px;color:var(--text-muted)" id="trackTime">00:00</span>
    <button class="btn" id="btnReset" title="Reset layout to default">Reset</button>
    <button class="btn" id="btnExport" title="Export layout config">Export</button>
    <button class="btn" id="btnApply" title="Force re-rank now">Re-rank</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection" style="display:none">
  <span>More panels</span> <span class="count" id="moreCount">0</span>
</div>
<div class="more-panels" id="morePanels"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
'use strict';
var STORAGE_KEY = 'adaptive_dashboard_v2';
var RANK_INTERVAL = 5000;
var DECAY_HALF_LIFE = 3600000;
var COMPACT_THRESHOLD = 0.15;
var COLLAPSE_THRESHOLD = 0.05;
var PANEL_DATA_DEFAULTS = [
  { id: 'revenue', title: 'Monthly Revenue', value: '$128,430', change: '+12.4%', trend: 'up', initialRank: 'high' },
  { id: 'users', title: 'Active Users', value: '24,892', change: '+8.1%', trend: 'up', initialRank: 'high' },
  { id: 'conversion', title: 'Conversion Rate', value: '3.24%', change: '-0.3%', trend: 'down', initialRank: 'medium' },
  { id: 'churn', title: 'Churn Rate', value: '1.8%', change: '+0.2%', trend: 'down', initialRank: 'medium' },
  { id: 'latency', title: 'API Latency', value: '142ms', change: '-15ms', trend: 'up', initialRank: 'medium' },
  { id: 'errors', title: 'Error Rate', value: '0.12%', change: '-0.04%', trend: 'up', initialRank: 'medium' },
  { id: 'nps', title: 'NPS Score', value: '72', change: '+3', trend: 'up', initialRank: 'low' },
  { id: 'cpu', title: 'CPU Usage', value: '67%', change: '+5%', trend: 'down', initialRank: 'low' },
  { id: 'disk', title: 'Disk I/O', value: '320MB/s', change: '+42MB/s', trend: 'down', initialRank: 'low' },
  { id: 'cache', title: 'Cache Hit Ratio', value: '94.2%', change: '+1.1%', trend: 'up', initialRank: 'low' }
];
var attentionState = {};
var panelConfig = {};
var trackingStartTime = Date.now();
var rankOrder = [];
var visibilityObserver = null;
var rafId = null;
var lastFlush = 0;
var FLUSH_DEBOUNCE = 2000;
var dragState = null;
function initAttentionState() {
  PANEL_DATA_DEFAULTS.forEach(function(p) {
    attentionState[p.id] = {
      viewMs: 0,
      interactions: 0,
      lastInteraction: 0,
      expandCount: 0,
      collapseCount: 0,
      viewSessions: 0
    };
    panelConfig[p.id] = {
      locked: false,
      manualOrder: -1,
      compactForced: false,
      collapsedForced: false
    };
  });
}
function loadState() {
  try {
    var raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    var saved = JSON.parse(raw);
    if (saved.attentionState) {
      Object.keys(saved.attentionState).forEach(function(k) {
        if (attentionState[k]) {
          attentionState[k].viewMs = saved.attentionState[k].viewMs || 0;
          attentionState[k].interactions = saved.attentionState[k].interactions || 0;
          attentionState[k].lastInteraction = saved.attentionState[k].lastInteraction || 0;
          attentionState[k].expandCount = saved.attentionState[k].expandCount || 0;
          attentionState[k].collapseCount = saved.attentionState[k].collapseCount || 0;
          attentionState[k].viewSessions = saved.attentionState[k].viewSessions || 0;
        }
      });
    }
    if (saved.panelConfig) {
      Object.keys(saved.panelConfig).forEach(function(k) {
        if (panelConfig[k]) Object.assign(panelConfig[k], saved.panelConfig[k]);
      });
    }
    if (saved.rankOrder) rankOrder = saved.rankOrder;
  } catch(e) {}
}
function saveState() {
  var now = Date.now();
  if (now - lastFlush < FLUSH_DEBOUNCE) return;
  lastFlush = now;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      attentionState: attentionState,
      panelConfig: panelConfig,
      rankOrder: rankOrder
    }));
  } catch(e) {}
}
function computeAttentionScore(panelId) {
  var s = attentionState[panelId];
  var now = Date.now();
  var recencyMs = now - s.lastInteraction;
  if (recencyMs < 0) recencyMs = 0;
  var recencyDecay = Math.exp(-Math.log(2) * recencyMs / DECAY_HALF_LIFE);
  var durationWeight = Math.log1p(s.viewMs / 1000);
  var freqWeight = Math.log1p(s.interactions);
  var expandBonus = 1 + (s.expandCount * 0.1);
  return freqWeight * durationWeight * recencyDecay * expandBonus;
}
function computeRanks() {
  var scores = [];
  PANEL_DATA_DEFAULTS.forEach(function(p) {
    scores.push({ id: p.id, score: computeAttentionScore(p.id) });
  });
  scores.sort(function(a, b) { return b.score - a.score; });
  var total = 0;
  scores.forEach(function(s) { total += s.score; });
  if (total === 0) total = 1;
  var ranks = [];
  scores.forEach(function(s, i) {
    var share = s.score / total;
    var rank;
    if (i < 2 || share > 0.2) rank = 'high';
    else if (share < COLLAPSE_THRESHOLD) rank = 'collapsed';
    else if (share < COMPACT_THRESHOLD) rank = 'compact';
    else rank = 'medium';
    ranks.push({ id: s.id, score: s.score, rank: rank, order: i });
  });
  rankOrder = ranks;
  return ranks;
}
function getPanelRank(panelId) {
  var cfg = panelConfig[panelId];
  if (cfg.compactForced) return 'compact';
  if (cfg.collapsedForced) return 'collapsed';
  for (var i = 0; i < rankOrder.length; i++) {
    if (rankOrder[i].id === panelId) return rankOrder[i].rank;
  }
  return 'medium';
}
function getPanelOrder(panelId) {
  var cfg = panelConfig[panelId];
  if (cfg.manualOrder >= 0) return cfg.manualOrder;
  for (var i = 0; i < rankOrder.length; i++) {
    if (rankOrder[i].id === panelId) return i;
  }
  return 999;
}
function recordInteraction(panelId) {
  attentionState[panelId].interactions++;
  attentionState[panelId].lastInteraction = Date.now();
  saveState();
}
function recordExpand(panelId) {
  attentionState[panelId].expandCount++;
  attentionState[panelId].lastInteraction = Date.now();
  saveState();
}
function recordCollapse(panelId) {
  attentionState[panelId].collapseCount++;
  attentionState[panelId].lastInteraction = Date.now();
  saveState();
}
function generateSparklinePath(panelId) {
  var seed = 0;
  for (var i = 0; i < panelId.length; i++) seed += panelId.charCodeAt(i);
  var points = [];
  var val = 50;
  for (var j = 0; j < 20; j++) {
    val += (Math.sin(j * 0.7 + seed) * 12) + (Math.cos(j * 0.3 + seed * 2) * 6) + 2;
    val = Math.max(10, Math.min(90, val));
    points.push(val);
  }
  var min = Math.min.apply(null, points);
  var max = Math.max.apply(null, points);
  var range = max - min || 1;
  var w = 200, h = 50, pad = 4;
  var path = '';
  points.forEach(function(v, i) {
    var x = (i / (points.length - 1)) * (w - pad * 2) + pad;
    var y = h - pad - ((v - min) / range) * (h - pad * 2);
    path += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1);
  });
  var last = points[points.length - 1];
  var trend = last > points[0] ? '#4ade80' : '#f87171';
  return { path: path, trend: trend };
}
function createPanelHTML(p) {
  var spark = generateSparklinePath(p.id);
  var changeClass = p.trend === 'up' ? 'up' : 'down';
  var changeArrow = p.trend === 'up' ? '\u2191' : '\u2193';
  return [
    '<div class="heatmap-indicator"></div>',
    '<div class="attention-badge">' + '\u2605' + ' Top</div>',
    '<div class="manual-order-indicator">manual</div>',
    '<div class="panel-controls">',
    '  <button class="panel-btn compact-btn" title="Compact mode" data-action="compact" data-id="' + p.id + '">\u25F0</button>',
    '  <button class="panel-btn collapse-btn" title="Collapse" data-action="collapse" data-id="' + p.id + '">\u2013</button>',
    '  <button class="panel-btn lock-btn" title="Lock position" data-action="lock" data-id="' + p.id + '">\uD83D\uDD12</button>',
    '</div>',
    '<div class="panel-content">',
    '  <div class="panel-header">' + p.title + '</div>',
    '  <div class="panel-value">' + p.value + '</div>',
    '  <div class="panel-sub ' + changeClass + '">' + changeArrow + ' ' + p.change + '</div>',
    '  <div class="sparkline"><svg viewBox="0 0 200 50"><path d="' + spark.path + '" fill="none" stroke="' + spark.trend + '" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg></div>',
    '</div>',
    '<div class="panel-compact-preview" style="display:none;font-size:12px;color:var(--text-muted)">' + p.title + ': ' + p.value + '</div>'
  ].join('');
}
var dashboardEl = document.getElementById('dashboard');
var moreSectionEl = document.getElementById('moreSection');
var morePanelsEl = document.getElementById('morePanels');
var moreCountEl = document.getElementById('moreCount');
var trackTimeEl = document.getElementById('trackTime');
var toastEl = document.getElementById('toast');
function showToast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  setTimeout(function() { toastEl.classList.remove('show'); }, 2000);
}
function buildDashboard() {
  var ranks = computeRanks();
  var ordered = PANEL_DATA_DEFAULTS.slice().sort(function(a, b) {
    return getPanelOrder(a.id) - getPanelOrder(b.id);
  });
  dashboardEl.innerHTML = '';
  morePanelsEl.innerHTML = '';
  ordered.forEach(function(p) {
    var rank = getPanelRank(p.id);
    var cfg = panelConfig[p.id];
    var div = document.createElement('div');
    div.className = 'panel';
    div.dataset.panelId = p.id;
    div.draggable = true;
    if (rank === 'high') div.classList.add('rank-high');
    else if (rank === 'medium') div.classList.add('rank-medium');
    else if (rank === 'compact' || cfg.compactForced) div.classList.add('compact', 'rank-low');
    else if (rank === 'collapsed' || cfg.collapsedForced) div.classList.add('collapsed');
    if (cfg.locked) div.classList.add('locked');
    if (cfg.manualOrder >= 0) div.classList.add('manually-placed');
    div.innerHTML = createPanelHTML(p);
    var lockBtn = div.querySelector('.lock-btn');
    if (cfg.locked) lockBtn.classList.add('locked');
    if (rank === 'collapsed' || cfg.collapsedForced) {
      morePanelsEl.appendChild(div);
    } else {
      dashboardEl.appendChild(div);
    }
  });
  updateMoreSection();
}
function updateMoreSection() {
  var collapsed = morePanelsEl.children.length;
  if (collapsed > 0) {
    moreSectionEl.style.display = 'flex';
    moreCountEl.textContent = collapsed;
  } else {
    moreSectionEl.style.display = 'none';
    morePanelsEl.classList.remove('open');
  }
}
function applyRanksToDOM() {
  var ranks = computeRanks();
  var allPanels = document.querySelectorAll('.panel');
  allPanels.forEach(function(panel) {
    var pid = panel.dataset.panelId;
    var rank = getPanelRank(pid);
    var cfg = panelConfig[pid];
    panel.classList.remove('rank-high', 'rank-medium', 'rank-low', 'compact', 'collapsed', 'locked', 'manually-placed');
    if (rank === 'high') panel.classList.add('rank-high');
    else if (rank === 'medium') panel.classList.add('rank-medium');
    else if (rank === 'compact' || cfg.compactForced) panel.classList.add('compact', 'rank-low');
    else if (rank === 'collapsed' || cfg.collapsedForced) {
      panel.classList.add('collapsed');
      if (panel.parentNode === dashboardEl) {
        morePanelsEl.appendChild(panel);
      }
    } else {
      panel.classList.add('rank-medium');
    }
    if (cfg.locked) panel.classList.add('locked');
    if (cfg.manualOrder >= 0) panel.classList.add('manually-placed');
    var lockBtn = panel.querySelector('.lock-btn');
    if (lockBtn) {
      if (cfg.locked) lockBtn.classList.add('locked');
      else lockBtn.classList.remove('locked');
    }
    if (rank !== 'collapsed' && !cfg.collapsedForced) {
      if (panel.parentNode === morePanelsEl) {
        var order = getPanelOrder(pid);
        insertPanelByOrder(dashboardEl, panel, order);
      }
    }
  });
  updateMoreSection();
}
function insertPanelByOrder(parent, panel, order) {
  var allPanels = parent.querySelectorAll('.panel');
  var inserted = false;
  for (var i = 0; i < allPanels.length; i++) {
    var otherOrder = getPanelOrder(allPanels[i].dataset.panelId);
    if (order < otherOrder) {
      parent.insertBefore(panel, allPanels[i]);
      inserted = true;
      break;
    }
  }
  if (!inserted) parent.appendChild(panel);
}
function reorderDashboardPanels() {
  var panels = Array.from(dashboardEl.querySelectorAll('.panel'));
  panels.sort(function(a, b) {
    return getPanelOrder(a.dataset.panelId) - getPanelOrder(b.dataset.panelId);
  });
  panels.forEach(function(p) { dashboardEl.appendChild(p); });
}
var periodicRankTimer = null;
function startPeriodicRanking() {
  if (periodicRankTimer) clearInterval(periodicRankTimer);
  periodicRankTimer = setInterval(function() {
    applyRanksToDOM();
    reorderDashboardPanels();
  }, RANK_INTERVAL);
}
function setupVisibilityTracking() {
  if (visibilityObserver) visibilityObserver.disconnect();
  var visiblePanels = {};
  visibilityObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      var pid = entry.target.dataset.panelId;
      if (!pid) return;
      if (entry.isIntersecting) {
        visiblePanels[pid] = { el: entry.target, since: Date.now(), ratio: entry.intersectionRatio };
        if (!attentionState[pid].viewSessions) attentionState[pid].viewSessions = 0;
        attentionState[pid].viewSessions++;
      } else {
        if (visiblePanels[pid]) {
          var elapsed = Date.now() - visiblePanels[pid].since;
          attentionState[pid].viewMs += elapsed;
          delete visiblePanels[pid];
          saveState();
        }
      }
    });
  }, { threshold: [0, 0.1, 0.5, 0.9] });
  function observeAll() {
    document.querySelectorAll('.panel').forEach(function(p) {
      visibilityObserver.observe(p);
    });
  }
  observeAll();
  var rafRunning = true;
  function rafLoop() {
    if (!rafRunning) return;
    var now = Date.now();
    Object.keys(visiblePanels).forEach(function(pid) {
      attentionState[pid].viewMs += 16;
      if (now - (visiblePanels[pid].since || now) > 1000) {
        visiblePanels[pid].since = now;
      }
    });
    if (now - lastFlush > FLUSH_DEBOUNCE) {
      lastFlush = now;
      saveState();
    }
    updateTrackTimer();
    rafId = requestAnimationFrame(rafLoop);
  }
  rafId = requestAnimationFrame(rafLoop);
  var domObserver = new MutationObserver(function() {
    observeAll();
  });
  domObserver.observe(dashboardEl, { childList: true, subtree: false });
  domObserver.observe(morePanelsEl, { childList: true, subtree: false });
}
function updateTrackTimer() {
  var elapsed = Math.floor((Date.now() - trackingStartTime) / 1000);
  var mins = Math.floor(elapsed / 60);
  var secs = elapsed % 60;
  trackTimeEl.textContent = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
}
function handlePanelClick(e) {
  var panel = e.target.closest('.panel');
  if (!panel) return;
  var btn = e.target.closest('.panel-btn');
  var pid = panel.dataset.panelId;
  if (btn) {
    e.preventDefault();
    e.stopPropagation();
    var action = btn.dataset.action;
    if (action === 'compact') {
      panelConfig[pid].compactForced = !panelConfig[pid].compactForced;
      if (panelConfig[pid].compactForced) {
        panelConfig[pid].collapsedForced = false;
        recordCollapse(pid);
      } else {
        recordExpand(pid);
      }
      saveState();
      applyRanksToDOM();
      reorderDashboardPanels();
      showToast(panelConfig[pid].compactForced ? 'Compact mode on' : 'Compact mode off');
    } else if (action === 'collapse') {
      panelConfig[pid].collapsedForced = !panelConfig[pid].collapsedForced;
      if (panelConfig[pid].collapsedForced) {
        panelConfig[pid].compactForced = false;
        recordCollapse(pid);
      } else {
        recordExpand(pid);
      }
      saveState();
      applyRanksToDOM();
      reorderDashboardPanels();
      showToast(panelConfig[pid].collapsedForced ? 'Collapsed to More' : 'Restored');
    } else if (action === 'lock') {
      panelConfig[pid].locked = !panelConfig[pid].locked;
      saveState();
      var lockBtn = panel.querySelector('.lock-btn');
      if (lockBtn) {
        if (panelConfig[pid].locked) lockBtn.classList.add('locked');
        else lockBtn.classList.remove('locked');
      }
      panel.classList.toggle('locked', panelConfig[pid].locked);
      showToast(panelConfig[pid].locked ? 'Position locked' : 'Position unlocked');
    }
    return;
  }
  recordInteraction(pid);
  saveState();
}
document.addEventListener('click', handlePanelClick);
moreSectionEl.addEventListener('click', function() {
  morePanelsEl.classList.toggle('open');
});
function setupDragAndDrop() {
  var dragSrcId = null;
  document.addEventListener('dragstart', function(e) {
    var panel = e.target.closest('.panel');
    if (!panel) return;
    dragSrcId = panel.dataset.panelId;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', dragSrcId);
  });
  document.addEventListener('dragend', function(e) {
    var panel = e.target.closest('.panel');
    if (panel) panel.classList.remove('dragging');
    document.querySelectorAll('.panel.drag-over').forEach(function(p) {
      p.classList.remove('drag-over');
    });
    dragSrcId = null;
  });
  document.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    var panel = e.target.closest('.panel');
    if (panel && panel.dataset.panelId !== dragSrcId) {
      panel.classList.add('drag-over');
    }
  });
  document.addEventListener('dragleave', function(e) {
    var panel = e.target.closest('.panel');
    if (panel) panel.classList.remove('drag-over');
  });
  document.addEventListener('drop', function(e) {
    e.preventDefault();
    var targetPanel = e.target.closest('.panel');
    if (!targetPanel || !dragSrcId || targetPanel.dataset.panelId === dragSrcId) return;
    targetPanel.classList.remove('drag-over');
    var srcOrder = getPanelOrder(dragSrcId);
    var dstOrder = getPanelOrder(targetPanel.dataset.panelId);
    panelConfig[dragSrcId].manualOrder = dstOrder;
    panelConfig[targetPanel.dataset.panelId].manualOrder = srcOrder;
    recordInteraction(dragSrcId);
    recordInteraction(targetPanel.dataset.panelId);
    saveState();
    applyRanksToDOM();
    reorderDashboardPanels();
    showToast('Panels swapped');
  });
}
document.getElementById('btnReset').addEventListener('click', function() {
  if (rafId) cancelAnimationFrame(rafId);
  if (visibilityObserver) visibilityObserver.disconnect();
  if (periodicRankTimer) clearInterval(periodicRankTimer);
  localStorage.removeItem(STORAGE_KEY);
  attentionState = {};
  panelConfig = {};
  rankOrder = [];
  initAttentionState();
  buildDashboard();
  setupVisibilityTracking();
  startPeriodicRanking();
  showToast('Layout reset');
});
document.getElementById('btnApply').addEventListener('click', function() {
  applyRanksToDOM();
  reorderDashboardPanels();
  showToast('Re-ranked by attention');
});
document.getElementById('btnExport').addEventListener('click', function() {
  var ranks = computeRanks();
  var config = {
    attention: attentionState,
    config: panelConfig,
    rankOrder: rankOrder,
    scores: ranks.map(function(r) { return { id: r.id, score: r.score.toFixed(2), rank: r.rank }; })
  };
  var blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'dashboard-config-' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
  showToast('Config exported');
});
initAttentionState();
loadState();
buildDashboard();
setupVisibilityTracking();
setupDragAndDrop();
startPeriodicRanking();
console.log('[AdaptiveDashboard] Runtime verification: Dashboard initialized');
console.log('[AdaptiveDashboard] Panels tracked: ' + PANEL_DATA_DEFAULTS.length);
console.log('[AdaptiveDashboard] Tracking method: rAF loop + IntersectionObserver');
console.log('[AdaptiveDashboard] Storage: localStorage key=' + STORAGE_KEY);
console.log('[AdaptiveDashboard] Rank interval: ' + RANK_INTERVAL + 'ms');
var verifyPanels = document.querySelectorAll('.panel');
console.log('[AdaptiveDashboard] DOM panels rendered: ' + verifyPanels.length);
var verifyIds = [];
verifyPanels.forEach(function(p) { verifyIds.push(p.dataset.panelId); });
var expectedIds = PANEL_DATA_DEFAULTS.map(function(p) { return p.id; });
var allPresent = expectedIds.every(function(id) { return verifyIds.indexOf(id) >= 0; });
console.log('[AdaptiveDashboard] All panel IDs present: ' + allPresent);
if (!allPresent) {
  var missing = expectedIds.filter(function(id) { return verifyIds.indexOf(id) < 0; });
  console.error('[AdaptiveDashboard] MISSING PANEL IDs: ' + missing.join(', '));
}
console.log('[AdaptiveDashboard] Runtime verification complete');
})();
</script>
</body>
</html>