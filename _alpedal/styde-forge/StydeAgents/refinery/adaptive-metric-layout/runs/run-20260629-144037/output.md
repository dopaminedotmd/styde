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
  --surface2: #22262f;
  --border: #2a2e3a;
  --text: #e1e4ea;
  --text2: #8b90a0;
  --accent: #5b8def;
  --accent2: #3dd68c;
  --warn: #f0a040;
  --danger: #ef5350;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  padding: 16px;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; flex-wrap: wrap; gap: 12px;
}
h1 { font-size: 1.4rem; font-weight: 700; letter-spacing: -0.02em; }
.controls { display: flex; gap: 8px; flex-wrap: wrap; }
.btn {
  padding: 7px 14px; border-radius: 7px; border: 1px solid var(--border);
  background: var(--surface2); color: var(--text); cursor: pointer;
  font-size: 0.82rem; font-weight: 500; transition: all 0.2s;
  white-space: nowrap;
}
.btn:hover { background: var(--border); border-color: #4a5060; }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.dashboard {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--gap);
  transition: all var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
  display: flex; flex-direction: column;
  min-height: 0;
}
.panel.tier-1 { grid-column: span 4; grid-row: span 2; }
.panel.tier-2 { grid-column: span 3; }
.panel.tier-3 { grid-column: span 2; padding: 10px 12px; font-size: 0.85rem; }
.panel.collapsed { grid-column: span 1; padding: 8px; }
.panel.collapsed .panel-body,
.panel.collapsed .panel-metric { display: none; }
.panel.collapsed .panel-header { margin-bottom: 0; }
.panel.locked { border-color: var(--accent); }
.panel.locked::after {
  content: ''; position: absolute; top: 0; right: 0;
  width: 0; height: 0;
  border-left: 12px solid transparent;
  border-top: 12px solid var(--accent);
  border-radius: 0 0 0 3px;
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px; gap: 8px;
}
.panel-title { font-weight: 600; font-size: 0.9rem; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.panel-actions { display: flex; gap: 4px; flex-shrink: 0; }
.panel-btn {
  width: 26px; height: 26px; border-radius: 5px; border: none;
  background: transparent; color: var(--text2); cursor: pointer;
  font-size: 0.75rem; display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.panel-btn:hover { background: var(--surface2); color: var(--text); }
.panel-btn.locked-btn { color: var(--warn); }
.panel-btn.locked-btn.active { color: var(--accent); background: rgba(91,141,239,0.12); }
.panel-body { flex: 1; min-height: 60px; }
.panel-metric {
  font-size: 1.8rem; font-weight: 700; letter-spacing: -0.03em;
  line-height: 1;
}
.panel-sub { font-size: 0.78rem; color: var(--text2); margin-top: 4px; }
.chart-area {
  width: 100%; height: 100%; min-height: 80px;
  display: flex; align-items: flex-end; gap: 2px;
}
.chart-bar {
  flex: 1; background: var(--accent); border-radius: 3px 3px 0 0;
  min-width: 4px; transition: height 0.4s ease;
}
.chart-bar.warn { background: var(--warn); }
.chart-bar.danger { background: var(--danger); }
.sparkline {
  display: flex; align-items: flex-end; gap: 1px; height: 50px; width: 100%;
}
.sparkline svg { width: 100%; height: 100%; overflow: visible; }
.usage-bar {
  height: 4px; background: var(--surface2); border-radius: 2px; margin-top: 8px; overflow: hidden;
}
.usage-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.rank-badge {
  font-size: 0.65rem; padding: 2px 6px; border-radius: 4px;
  background: var(--surface2); color: var(--text2);
  font-weight: 600;
}
.score-bar {
  margin-top: auto; padding-top: 8px; display: flex; align-items: center; gap: 6px;
}
.score-label { font-size: 0.7rem; color: var(--text2); white-space: nowrap; }
.score-fill-wrap { flex: 1; height: 3px; background: var(--surface2); border-radius: 2px; overflow: hidden; }
.score-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; background: var(--accent2); }
.toast {
  position: fixed; bottom: 24px; right: 24px; padding: 10px 18px;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 0.82rem; opacity: 0; transform: translateY(10px);
  transition: all 0.3s; pointer-events: none; z-index: 100;
}
.toast.show { opacity: 1; transform: translateY(0); }
.empty-state { grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text2); }
@media (max-width: 900px) {
  .panel.tier-1 { grid-column: span 6; }
  .panel.tier-2 { grid-column: span 4; }
  .panel.tier-3 { grid-column: span 3; }
}
@media (max-width: 600px) {
  .panel.tier-1 { grid-column: span 12; }
  .panel.tier-2 { grid-column: span 6; }
  .panel.tier-3 { grid-column: span 4; }
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Layout</h1>
  <div class="controls">
    <button class="btn" onclick="resetAll()" title="Clear all tracking data and reset layout">Reset</button>
    <button class="btn" onclick="unlockAll()" title="Remove all manual locks">Unlock All</button>
    <button class="btn" onclick="simulateUsage()" title="Simulate random usage to demonstrate adaptation">Simulate</button>
    <button class="btn" onclick="exportData()" title="Export tracking data as JSON">Export</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
'use strict';
const STORAGE_KEY = 'adaptive_layout_v2';
const DECAY_HALF_LIFE_MS = 1000 * 60 * 30;
const REBALANCE_INTERVAL_MS = 5000;
const VIEW_TRACK_INTERVAL_MS = 2000;
const COMPACT_THRESHOLD_PERCENTILE = 0.33;
const MAX_SCORE = 1_000_000;
function safeParse(v, fallback) {
  if (typeof v === 'number' && !isNaN(v)) return v;
  if (v === null || v === undefined) return fallback;
  var n = Number(v);
  if (!isNaN(n)) return n;
  n = parseFloat(v);
  if (!isNaN(n)) return n;
  var m = String(v).match(/[\d.]+/);
  if (m) { n = parseFloat(m[0]); if (!isNaN(n)) return n; }
  return fallback;
}
function uid() {
  return 'p_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
}
var state = {
  panels: [],
  layoutHash: '',
  rebalanceTimer: null,
  observer: null,
  visibleStart: {}
};
var DEFAULT_PANELS = [
  { id: uid(), title: 'CPU Usage', type: 'metric', unit: '%', value: 42, color: 'accent', history: [] },
  { id: uid(), title: 'Memory', type: 'metric', unit: 'GB', value: 12.4, max: 32, color: 'warn', history: [] },
  { id: uid(), title: 'Requests/s', type: 'metric', unit: '', value: 2847, color: 'accent2', history: [] },
  { id: uid(), title: 'Error Rate', type: 'metric', unit: '%', value: 0.34, color: 'danger', history: [] },
  { id: uid(), title: 'Disk I/O', type: 'chart', unit: 'MB/s', values: [18,22,31,28,45,38,52,44,39,48], color: 'accent', history: [] },
  { id: uid(), title: 'Network In', type: 'chart', unit: 'Mbps', values: [120,145,132,168,155,190,210,188,202,195], color: 'accent2', history: [] },
  { id: uid(), title: 'Active Users', type: 'metric', unit: '', value: 1284, color: 'accent', history: [] },
  { id: uid(), title: 'Cache Hit %', type: 'metric', unit: '%', value: 94.7, color: 'accent2', history: [] },
  { id: uid(), title: 'DB Queries', type: 'chart', unit: 'qps', values: [340,380,410,390,450,420,480,460,430,470], color: 'accent', history: [] },
  { id: uid(), title: 'Latency p99', type: 'metric', unit: 'ms', value: 245, color: 'warn', history: [] },
];
function initTracking(panelId) {
  return {
    panelId: panelId,
    totalViewMs: 0,
    interactionCount: 0,
    collapseCount: 0,
    lastInteraction: 0,
    pinned: false,
    locked: false,
    manualOrder: null,
    createdAt: Date.now()
  };
}
function loadState() {
  try {
    var raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      var parsed = JSON.parse(raw);
      if (parsed && parsed.panels && Array.isArray(parsed.panels) && parsed.panels.length > 0) {
        state.panels = parsed.panels;
        return;
      }
    }
  } catch(e) {}
  state.panels = DEFAULT_PANELS.map(function(p) {
    var t = initTracking(p.id);
    t.createdAt = Date.now();
    p._tracking = t;
    return p;
  });
}
function saveState() {
  try {
    var toSave = { panels: state.panels, savedAt: Date.now() };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  } catch(e) {
    toast('Storage full — cannot persist layout');
  }
}
function ensureTracking(p) {
  if (!p._tracking || p._tracking.panelId !== p.id) {
    p._tracking = initTracking(p.id);
  }
  return p._tracking;
}
function recencyFactor(lastInteractionMs) {
  if (!lastInteractionMs || lastInteractionMs <= 0) return 0.15;
  var age = Date.now() - lastInteractionMs;
  if (age <= 0) return 1.0;
  return Math.pow(0.5, age / DECAY_HALF_LIFE_MS);
}
function computeScore(panel) {
  var t = ensureTracking(panel);
  var freq = Math.log1p(t.interactionCount);
  var dur = Math.log1p(t.totalViewMs / 1000);
  var rec = recencyFactor(t.lastInteraction);
  var raw = freq * dur * rec;
  var normalized = Math.min(raw / 15, 1) * 100;
  return Math.round(normalized * 100) / 100;
}
function rankPanels() {
  return state.panels.map(function(p) {
    var t = ensureTracking(p);
    var score = computeScore(p);
    return { panel: p, tracking: t, score: score };
  }).sort(function(a, b) {
    if (a.tracking.locked && !b.tracking.locked) return -1;
    if (!a.tracking.locked && b.tracking.locked) return 1;
    if (a.tracking.locked && b.tracking.locked) {
      var ao = a.tracking.manualOrder !== null ? a.tracking.manualOrder : 0;
      var bo = b.tracking.manualOrder !== null ? b.tracking.manualOrder : 0;
      if (ao !== bo) return ao - bo;
    }
    return b.score - a.score;
  });
}
function assignTiers(ranked) {
  var n = ranked.length;
  if (n === 0) return ranked;
  var t1 = Math.max(1, Math.ceil(n * 0.3));
  var t2 = Math.max(1, Math.ceil(n * 0.35));
  var t3 = n - t1 - t2;
  if (t3 < 1 && n > 2) { t2 = n - t1; t3 = 0; }
  ranked.forEach(function(item, i) {
    if (i < t1) item.tier = 1;
    else if (i < t1 + t2) item.tier = 2;
    else item.tier = 3;
    if (item.tracking.pinned) item.tier = 1;
  });
  return ranked;
}
function layoutHash(ranked) {
  return ranked.map(function(r) {
    return r.panel.id + ':' + r.tier + ':' + (r.tracking.locked ? 1 : 0) + ':' + (r.tracking.pinned ? 1 : 0);
  }).join('|');
}
var GRADIENT_COUNTER = 0;
function nextGradientId() {
  return 'grd-' + (GRADIENT_COUNTER++);
}
function buildSparklineSvg(values, colorVar, panelId) {
  if (!values || values.length < 2) return '';
  var w = 200, h = 50, pad = 2;
  var min = Infinity, max = -Infinity;
  for (var i = 0; i < values.length; i++) {
    var v = safeParse(values[i], 0);
    if (v < min) min = v;
    if (v > max) max = v;
  }
  var range = max - min || 1;
  var stepX = (w - pad * 2) / (values.length - 1);
  var points = values.map(function(v, i) {
    var x = pad + i * stepX;
    var y = h - pad - ((safeParse(v, 0) - min) / range) * (h - pad * 2);
    return x.toFixed(1) + ',' + y.toFixed(1);
  }).join(' ');
  var gradId = 'sg-' + panelId + '-' + (GRADIENT_COUNTER++);
  var c = colorVar === 'accent' ? '#5b8def' : colorVar === 'accent2' ? '#3dd68c' : colorVar === 'warn' ? '#f0a040' : '#ef5350';
  return '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" style="width:100%;height:50px"><defs><linearGradient id="' + gradId + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="' + c + '" stop-opacity="0.3"/><stop offset="100%" stop-color="' + c + '" stop-opacity="0.02"/></linearGradient></defs><polyline points="' + points + '" fill="none" stroke="' + c + '" stroke-width="1.5" vector-effect="non-scaling-stroke"/><polygon points="' + (pad + ',' + (h-pad)) + ' ' + points + ' ' + (w-pad + ',' + (h-pad)) + '" fill="url(#' + gradId + ')"/></svg>';
}
function buildChartBars(values, colorVar) {
  if (!values || values.length === 0) return '';
  var max = 0;
  for (var i = 0; i < values.length; i++) { var v = safeParse(values[i], 0); if (v > max) max = v; }
  if (max === 0) max = 1;
  return values.map(function(v) {
    var h = Math.max(4, (safeParse(v, 0) / max) * 100);
    var cls = 'chart-bar';
    if (colorVar === 'warn') cls += ' warn';
    if (colorVar === 'danger') cls += ' danger';
    return '<div class="' + cls + '" style="height:' + h + '%" title="' + safeParse(v, 0) + '"></div>';
  }).join('');
}
function buildPanelHTML(panel, rankedItem) {
  var t = ensureTracking(panel);
  var score = rankedItem ? rankedItem.score : computeScore(panel);
  var tier = rankedItem ? rankedItem.tier : 1;
  var tierClass = 'tier-' + tier;
  var lockClass = t.locked ? ' locked' : '';
  var collapseClass = panel._collapsed ? ' collapsed' : '';
  var body = '';
  if (panel.type === 'metric') {
    body = '<div class="panel-metric" style="color:var(--' + (panel.color || 'text') + ')">' + safeParse(panel.value, 0).toLocaleString() + (panel.unit ? '<span style="font-size:0.9rem;font-weight:400;opacity:0.7;margin-left:3px">' + panel.unit + '</span>' : '') + '</div>';
    if (panel.max) {
      var pct = Math.min(100, Math.max(0, (safeParse(panel.value, 0) / safeParse(panel.max, 1)) * 100));
      body += '<div class="usage-bar"><div class="usage-fill" style="width:' + pct + '%;background:var(--' + (panel.color || 'accent') + ')"></div></div>';
    }
    if (panel.history && panel.history.length > 1) {
      body += buildSparklineSvg(panel.history, panel.color || 'accent', panel.id);
    }
  } else if (panel.type === 'chart') {
    body = '<div class="chart-area" style="height:100px">' + buildChartBars(panel.values, panel.color || 'accent') + '</div>';
    if (panel.unit) body += '<div class="panel-sub">' + panel.unit + '</div>';
  } else {
    body = '<div class="panel-sub">' + (panel.value || '—') + '</div>';
  }
  var maxScore = MAX_SCORE;
  var scorePct = Math.min(100, Math.round((score / 100) * 100));
  return '<div class="panel ' + tierClass + lockClass + collapseClass + '" data-panel-id="' + panel.id + '" style="order:' + (t.locked && t.manualOrder !== null ? t.manualOrder : Math.round(score * 10)) + '">' +
    '<div class="panel-header">' +
      '<span class="panel-title" title="' + panel.title + '">' + panel.title + '</span>' +
      '<span class="rank-badge" title="Score: ' + score.toFixed(1) + '">#' + (rankedItem ? (rankedItem._rank || '—') : '—') + ' ' + score.toFixed(0) + '</span>' +
      '<div class="panel-actions">' +
        '<button class="panel-btn locked-btn' + (t.locked ? ' active' : '') + '" onclick="toggleLock(\'' + panel.id + '\')" title="' + (t.locked ? 'Unlock' : 'Lock') + ' position">&#128274;</button>' +
        '<button class="panel-btn" onclick="toggleCollapse(\'' + panel.id + '\')" title="' + (panel._collapsed ? 'Expand' : 'Compact') + '">' + (panel._collapsed ? '&#9654;' : '&#9660;') + '</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' + body + '</div>' +
    '<div class="score-bar"><span class="score-label">Attention</span><div class="score-fill-wrap"><div class="score-fill" style="width:' + scorePct + '%"></div></div></div>' +
  '</div>';
}
function render(ranked) {
  var container = document.getElementById('dashboard');
  var hash = layoutHash(ranked);
  if (hash === state.layoutHash && container.children.length > 0) return;
  state.layoutHash = hash;
  var existing = {};
  Array.from(container.children).forEach(function(el) {
    var pid = el.getAttribute('data-panel-id');
    if (pid) existing[pid] = el;
  });
  var fragment = document.createDocumentFragment();
  ranked.forEach(function(item, i) {
    item._rank = i + 1;
    var pid = item.panel.id;
    if (existing[pid]) {
      var el = existing[pid];
      el.className = 'panel tier-' + item.tier + (item.tracking.locked ? ' locked' : '') + (item.panel._collapsed ? ' collapsed' : '');
      el.style.order = item.tracking.locked && item.tracking.manualOrder !== null ? item.tracking.manualOrder : Math.round(item.score * 10);
      var badge = el.querySelector('.rank-badge');
      if (badge) badge.textContent = '#' + (i + 1) + ' ' + item.score.toFixed(0);
      var scoreFill = el.querySelector('.score-fill');
      if (scoreFill) scoreFill.style.width = Math.min(100, Math.round((item.score / 100) * 100)) + '%';
      delete existing[pid];
      fragment.appendChild(el);
    } else {
      var div = document.createElement('div');
      div.innerHTML = buildPanelHTML(item.panel, item);
      fragment.appendChild(div.firstElementChild);
    }
  });
  Object.keys(existing).forEach(function(pid) {
    if (existing[pid].parentNode) existing[pid].parentNode.removeChild(existing[pid]);
  });
  container.innerHTML = '';
  container.appendChild(fragment);
  setupObservers();
  saveState();
}
function setupObservers() {
  if (state.observer) state.observer.disconnect();
  var visibleStart = {};
  state.observer = new IntersectionObserver(function(entries) {
    var now = Date.now();
    entries.forEach(function(entry) {
      var pid = entry.target.getAttribute('data-panel-id');
      if (!pid) return;
      if (entry.isIntersecting) {
        visibleStart[pid] = now;
      } else if (visibleStart[pid]) {
        var dur = now - visibleStart[pid];
        recordViewDuration(pid, dur);
        delete visibleStart[pid];
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.panel').forEach(function(el) {
    state.observer.observe(el);
    el.addEventListener('click', function(e) {
      if (e.target.closest('.panel-btn')) return;
      recordInteraction(el.getAttribute('data-panel-id'));
    });
  });
  state._visibleStart = visibleStart;
}
var VIEW_FLUSH_INTERVAL = null;
function flushVisibleDurations() {
  var now = Date.now();
  var vs = state._visibleStart || {};
  Object.keys(vs).forEach(function(pid) {
    var dur = now - vs[pid];
    if (dur > 500) {
      recordViewDuration(pid, dur);
      vs[pid] = now;
    }
  });
}
function recordViewDuration(panelId, ms) {
  var p = findPanel(panelId);
  if (!p) return;
  var t = ensureTracking(p);
  t.totalViewMs += ms;
  saveState();
}
function recordInteraction(panelId) {
  var p = findPanel(panelId);
  if (!p) return;
  var t = ensureTracking(p);
  t.interactionCount++;
  t.lastInteraction = Date.now();
  saveState();
}
function findPanel(panelId) {
  for (var i = 0; i < state.panels.length; i++) {
    if (state.panels[i].id === panelId) return state.panels[i];
  }
  return null;
}
function toggleLock(panelId) {
  var p = findPanel(panelId);
  if (!p) return;
  var t = ensureTracking(p);
  t.locked = !t.locked;
  if (t.locked) {
    t.manualOrder = state.panels.indexOf(p);
    toast('Panel locked at position #' + (t.manualOrder + 1));
  } else {
    t.manualOrder = null;
    toast('Panel unlocked — auto-layout restored');
  }
  saveState();
  rebalance();
}
function toggleCollapse(panelId) {
  var p = findPanel(panelId);
  if (!p) return;
  p._collapsed = !p._collapsed;
  var t = ensureTracking(p);
  t.collapseCount++;
  t.lastInteraction = Date.now();
  saveState();
  rebalance();
}
function toast(msg) {
  var el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(function() { el.classList.remove('show'); }, 2000);
}
function rebalance() {
  var ranked = assignTiers(rankPanels());
  render(ranked);
}
function resetAll() {
  if (confirm('Reset all tracking data and layout to defaults?')) {
    localStorage.removeItem(STORAGE_KEY);
    GRADIENT_COUNTER = 0;
    state.panels = DEFAULT_PANELS.map(function(p) {
      var t = initTracking(p.id);
      t.createdAt = Date.now();
      p._tracking = t;
      p._collapsed = false;
      return p;
    });
    state.layoutHash = '';
    rebalance();
    toast('Layout reset to defaults');
  }
}
function unlockAll() {
  state.panels.forEach(function(p) {
    var t = ensureTracking(p);
    t.locked = false;
    t.manualOrder = null;
  });
  saveState();
  rebalance();
  toast('All panels unlocked');
}
function simulateUsage() {
  var ranked = rankPanels();
  var highRanked = ranked.slice(0, Math.ceil(ranked.length * 0.4));
  highRanked.forEach(function(item) {
    var t = item.tracking;
    t.interactionCount += Math.floor(Math.random() * 8) + 3;
    t.totalViewMs += (Math.floor(Math.random() * 30000) + 10000);
    t.lastInteraction = Date.now();
  });
  var lowRanked = ranked.slice(Math.ceil(ranked.length * 0.6));
  lowRanked.forEach(function(item) {
    var t = item.tracking;
    t.collapseCount += 1;
    t.lastInteraction = Date.now() - Math.floor(Math.random() * DECAY_HALF_LIFE_MS * 3);
  });
  saveState();
  rebalance();
  toast('Simulated usage — top panels boosted, bottom panels decayed');
}
function exportData() {
  var data = {
    exportedAt: new Date().toISOString(),
    panels: state.panels.map(function(p) {
      var t = ensureTracking(p);
      return {
        id: p.id,
        title: p.title,
        type: p.type,
        score: computeScore(p),
        totalViewMs: t.totalViewMs,
        interactionCount: t.interactionCount,
        collapseCount: t.collapseCount,
        lastInteraction: t.lastInteraction,
        locked: t.locked,
        pinned: t.pinned
      };
    })
  };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'adaptive-layout-export-' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
  toast('Tracking data exported');
}
function handleVisibilityChange() {
  if (document.hidden) {
    flushVisibleDurations();
  } else {
    var now = Date.now();
    var vs = state._visibleStart || {};
    document.querySelectorAll('.panel').forEach(function(el) {
      var pid = el.getAttribute('data-panel-id');
      if (pid && !vs[pid]) vs[pid] = now;
    });
  }
}
function init() {
  loadState();
  GRADIENT_COUNTER = 0;
  var ranked = assignTiers(rankPanels());
  render(ranked);
  VIEW_FLUSH_INTERVAL = setInterval(flushVisibleDurations, VIEW_TRACK_INTERVAL_MS);
  state.rebalanceTimer = setInterval(function() {
    var ranked = assignTiers(rankPanels());
    render(ranked);
  }, REBALANCE_INTERVAL_MS);
  document.addEventListener('visibilitychange', handleVisibilityChange);
  setTimeout(function() {
    var anyData = state.panels.some(function(p) {
      var t = ensureTracking(p);
      return t.interactionCount > 0 || t.totalViewMs > 10000;
    });
    if (!anyData) {
      toast('Interact with panels to train the adaptive layout');
    }
  }, 3000);
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
</script>
</body>
</html>