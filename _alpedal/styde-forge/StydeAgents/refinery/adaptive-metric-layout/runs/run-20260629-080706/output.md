<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh}
header{padding:16px 24px;border-bottom:1px solid #21262d;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:18px;font-weight:600;color:#f0f6fc}
header .controls{display:flex;gap:8px}
button{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:13px;transition:background .15s}
button:hover{background:#30363d}
button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.dashboard{display:grid;gap:12px;padding:16px;grid-template-columns:repeat(12,1fr);grid-auto-rows:minmax(140px,auto);transition:all .4s ease}
.panel{border:1px solid #30363d;border-radius:8px;background:#161b22;overflow:hidden;display:flex;flex-direction:column;transition:all .4s ease;position:relative}
.panel-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid #21262d;background:#1c2128;flex-shrink:0}
.panel-header h3{font-size:14px;font-weight:500;color:#f0f6fc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{font-size:11px;padding:3px 8px;border-radius:4px;position:relative}
.lock-btn.locked{background:#d29922;border-color:#d29922;color:#0f1117}
.collapse-btn{min-width:24px;text-align:center}
.panel-body{flex:1;padding:12px 14px;overflow:hidden;display:flex;align-items:center;justify-content:center;min-height:80px}
.panel-body .metric-value{font-size:36px;font-weight:700;color:#58a6ff}
.panel-body .metric-label{font-size:12px;color:#8b949e;margin-top:4px}
.panel-body canvas{max-width:100%;max-height:100%}
.panel-body .mini-chart{width:100%;height:60px}
/* Size classes based on rank */
.panel.size-xl{grid-column:span 4;grid-row:span 2}
.panel.size-lg{grid-column:span 4;grid-row:span 2}
.panel.size-md{grid-column:span 3;grid-row:span 1}
.panel.size-sm{grid-column:span 2;grid-row:span 1}
.panel.size-xs{grid-column:span 2;grid-row:span 1}
/* Compact mode styling */
.panel.mode-compact .panel-body{min-height:40px;padding:8px}
.panel.mode-compact .panel-body .metric-value{font-size:22px}
.panel.mode-compact .panel-body canvas{height:40px}
/* Manual override indicator */
.panel.overridden{border-color:#d29922;box-shadow:0 0 0 1px #d29922}
.panel.overridden::after{content:'MANUAL';position:absolute;top:6px;right:6px;font-size:9px;color:#d29922;font-weight:700;opacity:.8}
.rank-badge{font-size:10px;color:#8b949e;padding:1px 6px;background:#21262d;border-radius:10px;margin-left:6px}
.toast{position:fixed;bottom:20px;right:20px;background:#238636;color:#fff;padding:10px 18px;border-radius:8px;font-size:13px;z-index:1000;animation:fadeInOut 2s ease forwards}
@keyframes fadeInOut{0%{opacity:0;transform:translateY(10px)}15%{opacity:1;transform:translateY(0)}85%{opacity:1}100%{opacity:0}}
.score-info{font-size:10px;color:#484f58;margin-top:2px}
</style>
</head>
<body>
<header>
<h1>Adaptive Metric Dashboard</h1>
<div class="controls">
<button id="resetBtn" title="Reset all tracking data and layout">Reset All</button>
<button id="recalcBtn">Recalculate</button>
</div>
</header>
<div class="dashboard" id="dashboard"></div>
<script>
// =============================================================================
// Adaptive Metric Layout — Self-organizing dashboard from behavioral tracking
// =============================================================================
// --- Configuration ---
var CONFIG = {
  STORAGE_KEY: 'adaptive_dashboard_v1',
  RECENCY_DECAY_HALFLIFE_MS: 3600000,   // 1 hour half-life for recency weight
  MIN_VIEW_DURATION_MS: 800,            // Minimum view duration to count as "viewed"
  RANK_THRESHOLD_XL: 0.75,              // Top 25% percentile gets XL
  RANK_THRESHOLD_LG: 0.50,              // Top 50% gets LG
  RANK_THRESHOLD_MD: 0.30,              // Above 30% gets MD
  RANK_THRESHOLD_SM: 0.10,              // Above 10% gets SM, rest XS + compact
  RECALCULATE_COOLDOWN_MS: 5000,        // Min ms between layout recomputes
  COMPACT_SCORE_THRESHOLD: 0.08         // Below this fraction of max score: compact mode
};
// --- State ---
var state = {
  panels: [],
  tracking: {},         // panelId -> { viewStart, totalViewMs, interactions, collapses, lastInteractionTs }
  overrides: {},        // panelId -> { locked: bool, size: string }
  lastRecalculate: 0
};
// --- Panel definitions with mock data ---
// TODO: Wire a real data source (API endpoint, WebSocket stream, or metrics collector)
//       Replace mock values with live data fetches. Add a config toggle `dataSource: 'mock'|'live'`.
var PANEL_DEFS = [
  { id: 'cpu',       title: 'CPU Usage',          value: '47%',   unit: '%',     trend: [35,42,38,44,47,45,52,49,47,46] },
  { id: 'memory',    title: 'Memory',             value: '62%',   unit: '%',     trend: [58,60,59,61,63,62,64,63,62,62] },
  { id: 'requests',  title: 'Requests/sec',       value: '1.2k',  unit: '/s',    trend: [800,950,1100,1050,1200,1150,1300,1250,1180,1200] },
  { id: 'latency',   title: 'P95 Latency',        value: '142ms', unit: 'ms',    trend: [180,165,155,148,150,145,140,138,142,142] },
  { id: 'errors',    title: 'Error Rate',         value: '0.12%', unit: '%',     trend: [0.5,0.3,0.25,0.2,0.18,0.15,0.14,0.13,0.12,0.12] },
  { id: 'disk',      title: 'Disk I/O',           value: '34MB/s',unit: 'MB/s',  trend: [20,28,32,30,35,33,38,36,34,34] },
  { id: 'conns',     title: 'Active Connections', value: '843',   unit: '',      trend: [700,750,780,800,820,830,850,840,843,843] },
  { id: 'cache',     title: 'Cache Hit Ratio',    value: '94.2%', unit: '%',     trend: [91,92,93,93.5,94,94.1,94.3,94.2,94.2,94.2] },
  { id: 'queue',     title: 'Queue Depth',        value: '17',    unit: '',      trend: [25,22,20,19,18,17,16,18,17,17] },
  { id: 'uptime',    title: 'Uptime',             value: '99.97%',unit: '%',     trend: [99.95,99.96,99.95,99.97,99.98,99.97,99.96,99.98,99.97,99.97] }
];
// =============================================================================
// Persistence: load/save from localStorage
// =============================================================================
function loadState() {
  try {
    var raw = localStorage.getItem(CONFIG.STORAGE_KEY);
    if (raw) {
      var saved = JSON.parse(raw);
      state.tracking = saved.tracking || {};
      state.overrides = saved.overrides || {};
    }
  } catch(e) { /* Corrupted data — start fresh */ }
}
function saveState() {
  try {
    localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify({
      tracking: state.tracking,
      overrides: state.overrides
    }));
  } catch(e) { /* Storage full or unavailable */ }
}
// =============================================================================
// Tracking: view duration via IntersectionObserver, click counts, collapse events
// =============================================================================
function ensureTracking(panelId) {
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = {
      totalViewMs: 0,
      interactions: 0,
      collapses: 0,
      lastInteractionTs: Date.now()
    };
  }
}
// Called when panel enters viewport
function onPanelVisible(panelId) {
  ensureTracking(panelId);
  state.tracking[panelId]._viewStart = Date.now();
}
// Called when panel leaves viewport
function onPanelHidden(panelId) {
  var t = state.tracking[panelId];
  if (!t) return;
  if (t._viewStart) {
    var duration = Date.now() - t._viewStart;
    if (duration > CONFIG.MIN_VIEW_DURATION_MS) {
      t.totalViewMs += duration;
    }
    t._viewStart = null;
  }
}
// Called on any panel interaction (click, metric hover, etc.)
function onPanelInteraction(panelId) {
  ensureTracking(panelId);
  state.tracking[panelId].interactions++;
  state.tracking[panelId].lastInteractionTs = Date.now();
  scheduleRecalculate();
}
// Called on collapse/expand toggle
function onPanelCollapse(panelId) {
  ensureTracking(panelId);
  state.tracking[panelId].collapses++;
  state.tracking[panelId].lastInteractionTs = Date.now();
  scheduleRecalculate();
}
// =============================================================================
// Ranking: composite attention score = normalized frequency × duration × recency
// =============================================================================
function computeScore(track, now) {
  // Recency factor: exponential decay, half-life from CONFIG
  var ageMs = now - track.lastInteractionTs;
  var recency = Math.pow(0.5, ageMs / CONFIG.RECENCY_DECAY_HALFLIFE_MS);
  // Duration factor: log-scaled to avoid dominance over interaction count
  var durationSec = track.totalViewMs / 1000;
  var durationFactor = Math.log1p(durationSec); // ln(1 + seconds)
  // Interaction factor: total interactions + collapse events
  var interactionFactor = track.interactions + track.collapses * 2; // collapses weighted 2x
  // Composite: interaction count * duration * recency
  // +1 avoids zero-score for never-seen panels
  var raw = (1 + interactionFactor) * (1 + durationFactor) * (0.1 + recency);
  return raw;
}
function rankPanels() {
  var now = Date.now();
  var scored = state.panels.map(function(p) {
    var track = state.tracking[p.id] || { totalViewMs: 0, interactions: 0, collapses: 0, lastInteractionTs: now };
    return {
      id: p.id,
      score: computeScore(track, now)
    };
  });
  // Sort descending by score
  scored.sort(function(a, b) { return b.score - a.score; });
  var maxScore = scored.length > 0 ? scored[0].score : 1;
  // Assign size classes based on percentile rank
  var total = scored.length;
  scored.forEach(function(item, idx) {
    var percentile = 1 - (idx / total); // Top item = 1.0, bottom = ~0
    var scoreFrac = maxScore > 0 ? item.score / maxScore : 0;
    // Override takes priority
    if (state.overrides[item.id] && state.overrides[item.id].locked) {
      item.size = state.overrides[item.id].size || 'md';
      item.locked = true;
    } else {
      item.locked = false;
      if (percentile >= CONFIG.RANK_THRESHOLD_XL)      item.size = 'xl';
      else if (percentile >= CONFIG.RANK_THRESHOLD_LG) item.size = 'lg';
      else if (percentile >= CONFIG.RANK_THRESHOLD_MD) item.size = 'md';
      else if (percentile >= CONFIG.RANK_THRESHOLD_SM) item.size = 'sm';
      else                                              item.size = 'xs';
    }
    // Compact mode for very low scores (relative to max)
    item.compact = !item.locked && (scoreFrac < CONFIG.COMPACT_SCORE_THRESHOLD);
  });
  return scored;
}
// =============================================================================
// Arrange: auto-position panels by rank — dominant top-left, low-rank compact/bottom
// =============================================================================
var recalculateTimer = null;
function scheduleRecalculate() {
  if (recalculateTimer) return; // Already scheduled
  var elapsed = Date.now() - state.lastRecalculate;
  var remaining = Math.max(0, CONFIG.RECALCULATE_COOLDOWN_MS - elapsed);
  recalculateTimer = setTimeout(function() {
    recalculateTimer = null;
    applyLayout();
  }, remaining);
}
function applyLayout() {
  state.lastRecalculate = Date.now();
  var ranked = rankPanels();
  var container = document.getElementById('dashboard');
  var existingPanels = container.querySelectorAll('.panel');
  // Update each panel's DOM classes and position based on rank
  ranked.forEach(function(item, idx) {
    var el = container.querySelector('[data-panel-id="' + item.id + '"]');
    if (!el) return;
    // Remove old size classes
    el.classList.remove('size-xl', 'size-lg', 'size-md', 'size-sm', 'size-xs');
    el.classList.add('size-' + item.size);
    // Toggle compact mode
    if (item.compact) {
      el.classList.add('mode-compact');
    } else {
      el.classList.remove('mode-compact');
    }
    // Toggle override indicator
    if (item.locked) {
      el.classList.add('overridden');
    } else {
      el.classList.remove('overridden');
    }
    // Update rank badge
    var badge = el.querySelector('.rank-badge');
    if (badge) {
      badge.textContent = '#' + (idx + 1) + ' · ' + item.score.toFixed(1);
    }
    // Reorder in DOM: grid auto-placement respects source order
    // Move element to correct position (CSS Grid auto-flow: row)
    var currentPos = Array.from(container.children).indexOf(el);
    if (currentPos !== idx && currentPos >= 0) {
      // Find the element currently at target position
      var targetChild = container.children[idx] || null;
      if (targetChild) {
        container.insertBefore(el, targetChild);
      } else {
        container.appendChild(el);
      }
    }
  });
  saveState();
}
// =============================================================================
// Manual Override: lock panel position and size
// =============================================================================
function toggleLock(panelId) {
  if (state.overrides[panelId] && state.overrides[panelId].locked) {
    // Unlock: remove override, let algorithm control again
    delete state.overrides[panelId];
    showToast('Panel unlocked — auto-layout restored');
  } else {
    // Lock: capture current size as override
    var el = document.querySelector('[data-panel-id="' + panelId + '"]');
    var currentSize = 'md'; // default
    if (el) {
      var classes = el.classList;
      if (classes.contains('size-xl')) currentSize = 'xl';
      else if (classes.contains('size-lg')) currentSize = 'lg';
      else if (classes.contains('size-sm')) currentSize = 'sm';
      else if (classes.contains('size-xs')) currentSize = 'xs';
    }
    state.overrides[panelId] = { locked: true, size: currentSize };
    showToast('Panel locked at ' + currentSize.toUpperCase() + ' size');
  }
  applyLayout();
}
// =============================================================================
// Compact mode: shrink low-usage panels with preview
// =============================================================================
function toggleCollapse(panelId) {
  var el = document.querySelector('[data-panel-id="' + panelId + '"]');
  if (!el) return;
  var body = el.querySelector('.panel-body');
  var btn = el.querySelector('.collapse-btn');
  if (body.style.display === 'none') {
    body.style.display = '';
    btn.textContent = '−';
  } else {
    body.style.display = 'none';
    btn.textContent = '+';
  }
  onPanelCollapse(panelId);
}
// =============================================================================
// Rendering: build panel DOM with sparkline charts
// =============================================================================
function drawSparkline(canvas, data, color) {
  if (!canvas || !data || data.length === 0) return;
  var ctx = canvas.getContext('2d');
  var w = canvas.width = canvas.offsetWidth || 200;
  var h = canvas.height = canvas.offsetHeight || 60;
  ctx.clearRect(0, 0, w, h);
  var min = Math.min.apply(null, data);
  var max = Math.max.apply(null, data);
  var range = max - min || 1;
  ctx.beginPath();
  ctx.strokeStyle = color || '#58a6ff';
  ctx.lineWidth = 1.5;
  ctx.lineJoin = 'round';
  data.forEach(function(val, i) {
    var x = (i / (data.length - 1)) * (w - 4) + 2;
    var y = h - ((val - min) / range) * (h - 8) - 4;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
  // Fill area under curve
  ctx.lineTo(w - 2, h - 2);
  ctx.lineTo(2, h - 2);
  ctx.closePath();
  ctx.fillStyle = (color || '#58a6ff') + '15';
  ctx.fill();
}
function buildDashboard() {
  loadState();
  // Initialize panels from definitions
  state.panels = PANEL_DEFS.map(function(d) {
    return { id: d.id, title: d.title };
  });
  var container = document.getElementById('dashboard');
  container.innerHTML = '';
  PANEL_DEFS.forEach(function(def) {
    var panel = document.createElement('div');
    panel.className = 'panel size-md'; // Default, will be recalculated
    panel.setAttribute('data-panel-id', def.id);
    panel.onclick = function(e) {
      // Only count if not clicking a button
      if (e.target.tagName !== 'BUTTON') {
        onPanelInteraction(def.id);
      }
    };
    // Panel header
    var header = document.createElement('div');
    header.className = 'panel-header';
    var titleWrap = document.createElement('div');
    titleWrap.style.cssText = 'display:flex;align-items:center;min-width:0;flex:1';
    var title = document.createElement('h3');
    title.textContent = def.title;
    var badge = document.createElement('span');
    badge.className = 'rank-badge';
    badge.textContent = '#-';
    titleWrap.appendChild(title);
    titleWrap.appendChild(badge);
    var actions = document.createElement('div');
    actions.className = 'panel-actions';
    var lockBtn = document.createElement('button');
    lockBtn.className = 'lock-btn';
    lockBtn.textContent = 'LOCK';
    lockBtn.title = 'Toggle manual position lock';
    lockBtn.onclick = function(e) {
      e.stopPropagation();
      toggleLock(def.id);
    };
    var collapseBtn = document.createElement('button');
    collapseBtn.className = 'collapse-btn';
    collapseBtn.textContent = '−';
    collapseBtn.title = 'Collapse/Expand panel';
    collapseBtn.onclick = function(e) {
      e.stopPropagation();
      toggleCollapse(def.id);
    };
    actions.appendChild(lockBtn);
    actions.appendChild(collapseBtn);
    header.appendChild(titleWrap);
    header.appendChild(actions);
    // Panel body
    var body = document.createElement('div');
    body.className = 'panel-body';
    var metricWrap = document.createElement('div');
    metricWrap.style.cssText = 'text-align:center;width:100%';
    var metricValue = document.createElement('div');
    metricValue.className = 'metric-value';
    metricValue.textContent = def.value;
    var metricLabel = document.createElement('div');
    metricLabel.className = 'metric-label';
    metricLabel.textContent = def.unit || '';
    var canvas = document.createElement('canvas');
    canvas.className = 'mini-chart';
    canvas.style.cssText = 'margin-top:8px';
    metricWrap.appendChild(metricValue);
    metricWrap.appendChild(metricLabel);
    metricWrap.appendChild(canvas);
    body.appendChild(metricWrap);
    panel.appendChild(header);
    panel.appendChild(body);
    container.appendChild(panel);
    // Draw sparkline after DOM insertion (needs layout dimensions)
    requestAnimationFrame(function() {
      drawSparkline(canvas, def.trend, '#58a6ff');
    });
  });
  // Set up IntersectionObserver for view duration tracking
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      var panelId = entry.target.getAttribute('data-panel-id');
      if (!panelId) return;
      if (entry.isIntersecting) {
        onPanelVisible(panelId);
      } else {
        onPanelHidden(panelId);
      }
    });
  }, { threshold: 0.3 });
  container.querySelectorAll('.panel').forEach(function(el) {
    observer.observe(el);
  });
  // Apply initial layout from saved state
  applyLayout();
  // Update lock button states
  updateLockButtonStates();
}
function updateLockButtonStates() {
  document.querySelectorAll('.panel').forEach(function(el) {
    var panelId = el.getAttribute('data-panel-id');
    var lockBtn = el.querySelector('.lock-btn');
    if (!lockBtn) return;
    if (state.overrides[panelId] && state.overrides[panelId].locked) {
      lockBtn.textContent = 'UNLOCK';
      lockBtn.classList.add('locked');
    } else {
      lockBtn.textContent = 'LOCK';
      lockBtn.classList.remove('locked');
    }
  });
}
// Override toggleLock to also update button state
var _origToggleLock = toggleLock;
toggleLock = function(panelId) {
  _origToggleLock(panelId);
  updateLockButtonStates();
};
// =============================================================================
// Utility: toast notification
// =============================================================================
function showToast(msg) {
  var toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(function() { toast.remove(); }, 2200);
}
// =============================================================================
// Controls
// =============================================================================
document.getElementById('resetBtn').onclick = function() {
  state.tracking = {};
  state.overrides = {};
  state.lastRecalculate = 0;
  localStorage.removeItem(CONFIG.STORAGE_KEY);
  buildDashboard();
  showToast('All tracking data and layouts reset');
};
document.getElementById('recalcBtn').onclick = function() {
  applyLayout();
  showToast('Layout recalculated');
};
// =============================================================================
// Bootstrap
// =============================================================================
buildDashboard();
// Save tracking on page unload (captures last view duration)
window.addEventListener('beforeunload', function() {
  // Flush any active view durations
  Object.keys(state.tracking).forEach(function(panelId) {
    onPanelHidden(panelId);
  });
  saveState();
});
</script>
</body>
</html>