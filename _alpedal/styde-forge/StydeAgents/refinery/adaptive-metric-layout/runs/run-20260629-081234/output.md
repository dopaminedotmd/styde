<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:#161b22;border-bottom:1px solid #30363d}
header h1{font-size:18px;font-weight:600;color:#f0f6fc}
header .controls{display:flex;gap:8px;align-items:center}
.btn{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:13px;transition:background .15s}
.btn:hover{background:#30363d}
.btn.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.btn.danger{color:#f85149}
.btn.danger:hover{background:#da3633;color:#fff}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:16px 24px;grid-auto-rows:minmax(140px,auto)}
/* Panel size classes assigned by rank */
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;position:relative;transition:grid-column .35s ease,grid-row .35s ease,opacity .25s;overflow:hidden}
.panel.size-lg{grid-column:span 2;grid-row:span 2}
.panel.size-md{grid-column:span 2;grid-row:span 1}
.panel.size-sm{grid-column:span 1;grid-row:span 1}
.panel.size-xs{grid-column:span 1;grid-row:span 1;opacity:.7;font-size:12px;padding:10px}
.panel.size-hidden{display:none}
.panel.locked{border-color:#d2991b;box-shadow:0 0 0 1px #d2991b}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.panel-title{font-size:13px;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.panel-value{font-size:28px;font-weight:700;color:#f0f6fc}
.panel-sub{font-size:12px;color:#8b949e;margin-top:4px}
.panel-actions{display:flex;gap:4px}
.panel-actions button{background:none;border:none;color:#484f58;cursor:pointer;padding:2px 4px;font-size:14px;line-height:1;border-radius:4px}
.panel-actions button:hover{color:#c9d1d9;background:#21262d}
.panel-actions button.lock-btn.locked{color:#d2991b}
.chart-bar{display:flex;align-items:flex-end;gap:4px;height:60px;margin-top:8px}
.chart-bar span{flex:1;background:#1f6feb;border-radius:3px 3px 0 0;min-height:4px;transition:height .3s}
.chart-labels{display:flex;justify-content:space-between;font-size:10px;color:#484f58;margin-top:4px}
.metric-row{display:flex;gap:8px;margin-top:8px}
.metric-chip{background:#21262d;border-radius:6px;padding:6px 10px;font-size:12px;color:#8b949e}
.metric-chip strong{color:#f0f6fc;display:block;font-size:16px}
.more-section{border-top:1px solid #30363d;margin-top:12px;padding-top:8px}
.more-toggle{background:none;border:none;color:#484f58;cursor:pointer;font-size:12px;padding:4px 8px}
.more-toggle:hover{color:#c9d1d9}
.more-panels{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.more-panels .panel.size-xs{display:block;flex:0 0 200px}
.reset-banner{background:#1f2429;color:#8b949e;font-size:12px;padding:8px 16px;text-align:center;border-bottom:1px solid #30363d;display:none}
.reset-banner.show{display:block}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset all tracking data and layout">Reset Data</button>
    <button class="btn" id="btnApply" title="Re-rank and re-arrange panels now">Apply Layout</button>
  </div>
</header>
<div class="reset-banner" id="resetBanner">Tracking data reset. Layout will re-adapt as you interact with panels.</div>
<div class="grid" id="grid"></div>
<script>
// --- Adaptive Layout Engine ---
// Tracks panel visibility, interactions, and collapse/expand events.
// Ranks panels by composite attention score: frequency * duration * recency.
// Applies layout: high-rank = large (span 2), low-rank = compact or hidden.
// Supports manual lock/override and localStorage persistence.
// No background timers or polling — entirely event-driven.
const STORAGE_KEY = 'adaptive_dashboard_v1';
// --- Panel definitions (mock data, values are static for demo) ---
// TODO: Wire real data source — replace static values with API/WebSocket fetches.
const PANEL_DEFS = [
  { id: 'revenue',   title: 'Revenue',       value: '$48,291', sub: '+12.3% vs last month', type: 'metric' },
  { id: 'users',     title: 'Active Users',  value: '12,844',  sub: '+8.1% vs last month',  type: 'metric' },
  { id: 'conv',      title: 'Conversion',    value: '3.24%',   sub: '-0.3% vs last month',  type: 'metric' },
  { id: 'churn',     title: 'Churn Rate',    value: '1.8%',    sub: '-0.2% vs last month',  type: 'metric' },
  { id: 'sales',     title: 'Sales Trend',   value: '',        sub: '',                     type: 'chart', bars: [40,65,35,80,55,90,70] },
  { id: 'traffic',   title: 'Traffic Sources', value: '',      sub: '',                     type: 'traffic' },
  { id: 'sessions',  title: 'Sessions',      value: '94.2K',   sub: '+5.7% vs last month',  type: 'metric' },
  { id: 'bounce',    title: 'Bounce Rate',   value: '42.1%',   sub: '+1.2% vs last month',  type: 'metric' },
  { id: 'latency',   title: 'API Latency',   value: '187ms',   sub: 'p95, -22ms improvement', type: 'metric' },
  { id: 'errors',    title: 'Error Rate',    value: '0.12%',   sub: 'Below 0.5% threshold', type: 'metric' },
];
// --- Tracking state ---
// Tracks per-panel: totalVisibleMs, interactionCount, lastInteractionAt, expanded state
let tracking = {};        // { [panelId]: { visibleMs, interactions, lastTs, expanded } }
let layoutRank = [];      // ordered list of panel IDs by rank (high to low)
let lockedPanels = new Set(); // panel IDs locked by user
let visibleStart = {};    // { [panelId]: timestamp } — when the panel became visible
let applyTimeout = null;  // debounced re-apply timer
// --- Persistence ---
function saveState() {
  const state = { tracking, lockedPanels: [...lockedPanels] };
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) { /* quota exceeded, ignore */ }
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const state = JSON.parse(raw);
    if (state.tracking) tracking = state.tracking;
    if (state.lockedPanels) lockedPanels = new Set(state.lockedPanels);
  } catch(e) { /* corrupt data, start fresh */ }
}
// --- Ranking ---
// Pure function: takes tracking data, returns array of panel IDs sorted by score descending.
// Score = interactions * (visibleMs / 1000) * recencyFactor
// recencyFactor: 1.0 if interaction < 1min ago, linear decay to 0.1 over 24h.
function computeRankings(trackingData) {
  const now = Date.now();
  const scored = Object.entries(trackingData).map(([id, t]) => {
    const freq = t.interactions || 0;
    const durSec = (t.visibleMs || 0) / 1000;
    const ageMs = now - (t.lastTs || now);
    // recency: 1.0 at 0s, 0.5 at 12h, 0.1 at 24h+
    const recency = Math.max(0.1, 1.0 - (ageMs / (24 * 60 * 60 * 1000)) * 0.9);
    const score = freq * Math.max(1, durSec) * recency;
    return { id, score };
  });
  // Sort descending by score
  scored.sort((a, b) => b.score - a.score);
  return scored.map(s => s.id);
}
// --- Layout application ---
// Clears any pending re-apply timeout, computes fresh rankings, updates DOM classes.
function applyLayout() {
  // Guard: clear pending timeout to prevent double-fires (per teacher feedback)
  if (applyTimeout !== null) {
    clearTimeout(applyTimeout);
    applyTimeout = null;
  }
  layoutRank = computeRankings(tracking);
  const grid = document.getElementById('grid');
  if (!grid) return;
  // Remove all panels from grid
  while (grid.firstChild) grid.removeChild(grid.firstChild);
  // Partition: visible (top N) vs hidden rest
  const visibleCutoff = 6; // show top 6 panels, rest go to "more" section
  const visibleIds = layoutRank.slice(0, visibleCutoff);
  const hiddenIds = layoutRank.slice(visibleCutoff);
  // Build visible panels in rank order
  visibleIds.forEach((id, idx) => {
    const def = PANEL_DEFS.find(d => d.id === id);
    if (!def) return;
    // Assign size class by rank position
    let sizeClass = 'size-sm';
    if (idx === 0) sizeClass = 'size-lg';       // top rank: largest
    else if (idx <= 2) sizeClass = 'size-md';   // ranks 2-3: medium
    else if (idx <= 4) sizeClass = 'size-sm';   // ranks 4-5: standard
    else sizeClass = 'size-xs';                  // rank 6: compact
    const panel = buildPanel(def, sizeClass);
    grid.appendChild(panel);
  });
  // Build "more" section with hidden panels (if any)
  if (hiddenIds.length > 0) {
    const moreWrapper = document.createElement('div');
    moreWrapper.className = 'more-section';
    moreWrapper.style.gridColumn = 'span 4';
    const toggle = document.createElement('button');
    toggle.className = 'more-toggle';
    toggle.textContent = '+ ' + hiddenIds.length + ' more panels';
    moreWrapper.appendChild(toggle);
    const moreContainer = document.createElement('div');
    moreContainer.className = 'more-panels';
    moreContainer.style.display = 'none';
    hiddenIds.forEach(id => {
      const def = PANEL_DEFS.find(d => d.id === id);
      if (!def) return;
      moreContainer.appendChild(buildPanel(def, 'size-xs'));
    });
    moreWrapper.appendChild(moreContainer);
    // Toggle expanded state: logs collapse/expand events
    toggle.addEventListener('click', function() {
      const expanded = moreContainer.style.display !== 'none';
      if (expanded) {
        moreContainer.style.display = 'none';
        toggle.textContent = '+ ' + hiddenIds.length + ' more panels';
      } else {
        moreContainer.style.display = 'flex';
        toggle.textContent = '- Show less';
      }
      // Log collapse/expand as interaction on all hidden panels
      hiddenIds.forEach(hid => recordInteraction(hid, expanded ? 'collapse' : 'expand'));
    });
    grid.appendChild(moreWrapper);
  }
}
// --- Panel DOM builder ---
function buildPanel(def, sizeClass) {
  const el = document.createElement('div');
  el.className = 'panel ' + sizeClass;
  el.dataset.panelId = def.id;
  if (lockedPanels.has(def.id)) el.classList.add('locked');
  // Header
  const header = document.createElement('div');
  header.className = 'panel-header';
  const title = document.createElement('span');
  title.className = 'panel-title';
  title.textContent = def.title;
  header.appendChild(title);
  // Action buttons: lock + collapse
  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const lockBtn = document.createElement('button');
  lockBtn.className = 'lock-btn' + (lockedPanels.has(def.id) ? ' locked' : '');
  lockBtn.textContent = lockedPanels.has(def.id) ? '🔒' : '🔓';
  lockBtn.title = lockedPanels.has(def.id) ? 'Unlock panel position' : 'Lock panel position';
  lockBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    toggleLock(def.id);
  });
  actions.appendChild(lockBtn);
  header.appendChild(actions);
  el.appendChild(header);
  // Content by type
  if (def.type === 'metric') {
    const value = document.createElement('div');
    value.className = 'panel-value';
    value.textContent = def.value;
    el.appendChild(value);
    if (def.sub) {
      const sub = document.createElement('div');
      sub.className = 'panel-sub';
      sub.textContent = def.sub;
      el.appendChild(sub);
    }
  } else if (def.type === 'chart' && def.bars) {
    const chartWrap = document.createElement('div');
    chartWrap.className = 'chart-bar';
    const maxVal = Math.max(...def.bars);
    def.bars.forEach(v => {
      const bar = document.createElement('span');
      bar.style.height = (v / maxVal * 100) + '%';
      chartWrap.appendChild(bar);
    });
    el.appendChild(chartWrap);
    const labels = document.createElement('div');
    labels.className = 'chart-labels';
    ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].forEach(d => {
      const lbl = document.createElement('span');
      lbl.textContent = d;
      labels.appendChild(lbl);
    });
    el.appendChild(labels);
  } else if (def.type === 'traffic') {
    const row = document.createElement('div');
    row.className = 'metric-row';
    [
      { label: 'Direct', val: '38%', sub: '12.1K' },
      { label: 'Search', val: '29%', sub: '9.2K' },
      { label: 'Social', val: '18%', sub: '5.7K' },
      { label: 'Referral', val: '15%', sub: '4.8K' },
    ].forEach(src => {
      const chip = document.createElement('div');
      chip.className = 'metric-chip';
      chip.innerHTML = '<strong>' + src.val + '</strong>' + src.label + ' · ' + src.sub;
      row.appendChild(chip);
    });
    el.appendChild(row);
  }
  // Interaction tracking: clicks anywhere on panel
  el.addEventListener('click', function() {
    recordInteraction(def.id, 'click');
  });
  return el;
}
// --- Lock toggle ---
function toggleLock(panelId) {
  if (lockedPanels.has(panelId)) {
    lockedPanels.delete(panelId);
  } else {
    lockedPanels.add(panelId);
  }
  saveState();
  applyLayout(); // re-render to update lock icons and positions
}
// --- Interaction recording ---
// Logs interaction frequency and recency. Called on click, expand, collapse.
function recordInteraction(panelId, type) {
  if (!tracking[panelId]) {
    tracking[panelId] = { visibleMs: 0, interactions: 0, lastTs: 0, expanded: true };
  }
  tracking[panelId].interactions += 1;
  tracking[panelId].lastTs = Date.now();
  if (type === 'collapse') tracking[panelId].expanded = false;
  if (type === 'expand') tracking[panelId].expanded = true;
  saveState();
  // Debounced re-apply after interaction (1.5s delay to batch rapid clicks)
  if (applyTimeout !== null) clearTimeout(applyTimeout);
  applyTimeout = setTimeout(applyLayout, 1500);
}
// --- Visibility tracking via IntersectionObserver ---
// Tracks how long each panel is visible in the viewport. No polling.
const observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    const panelId = entry.target.dataset.panelId;
    if (!panelId) return;
    if (!tracking[panelId]) {
      tracking[panelId] = { visibleMs: 0, interactions: 0, lastTs: 0, expanded: true };
    }
    if (entry.isIntersecting) {
      // Panel became visible: start timing
      visibleStart[panelId] = Date.now();
    } else {
      // Panel left viewport: accumulate visible duration
      if (visibleStart[panelId]) {
        tracking[panelId].visibleMs += Date.now() - visibleStart[panelId];
        delete visibleStart[panelId];
      }
      saveState();
    }
  });
}, { threshold: 0.1 }); // 10% visibility threshold
// Observe all panels after each layout render via MutationObserver
const panelObserver = new MutationObserver(function() {
  document.querySelectorAll('.panel[data-panel-id]').forEach(function(panel) {
    observer.observe(panel);
  });
});
panelObserver.observe(document.getElementById('grid'), { childList: true, subtree: true });
// --- Page visibility: pause tracking when tab is hidden ---
document.addEventListener('visibilitychange', function() {
  if (document.hidden) {
    // Flush all active visibility timers
    Object.keys(visibleStart).forEach(function(id) {
      if (tracking[id]) {
        tracking[id].visibleMs += Date.now() - visibleStart[id];
      }
      delete visibleStart[id];
    });
    saveState();
  }
  // On return, IntersectionObserver will re-fire for visible panels automatically
});
// --- Before unload: flush any remaining visibility time ---
window.addEventListener('beforeunload', function() {
  Object.keys(visibleStart).forEach(function(id) {
    if (tracking[id]) {
      tracking[id].visibleMs += Date.now() - visibleStart[id];
    }
    delete visibleStart[id];
  });
  saveState();
});
// --- Manual controls ---
document.getElementById('btnApply').addEventListener('click', function() {
  // Flush visibility timers before ranking so current session counts
  Object.keys(visibleStart).forEach(function(id) {
    if (tracking[id]) {
      tracking[id].visibleMs += Date.now() - visibleStart[id];
      visibleStart[id] = Date.now(); // restart timing
    }
  });
  applyLayout();
});
document.getElementById('btnReset').addEventListener('click', function() {
  tracking = {};
  lockedPanels = new Set();
  visibleStart = {};
  layoutRank = [];
  if (applyTimeout !== null) { clearTimeout(applyTimeout); applyTimeout = null; }
  try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
  applyLayout();
  var banner = document.getElementById('resetBanner');
  banner.classList.add('show');
  setTimeout(function() { banner.classList.remove('show'); }, 3000);
});
// --- Initialization ---
// Initialize tracking for all panel defs that have no data yet
PANEL_DEFS.forEach(function(def) {
  if (!tracking[def.id]) {
    tracking[def.id] = { visibleMs: 0, interactions: 0, lastTs: 0, expanded: true };
  }
});
applyLayout();
// Observe initial panels (MutationObserver handles subsequent renders)
document.querySelectorAll('.panel[data-panel-id]').forEach(function(panel) {
  observer.observe(panel);
});
</script>
</body>
</html>