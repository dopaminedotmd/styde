<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --panel-radius: 8px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
  --font-mono: 'SF Mono','Fira Code','Consolas',monospace;
  --font-sans: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --color-bg: #0f1117;
  --color-surface: #1a1d27;
  --color-surface-hover: #222636;
  --color-border: #2a2e3a;
  --color-text: #e1e4eb;
  --color-text-dim: #8b8fa3;
  --color-accent: #6c8cff;
  --color-accent-glow: rgba(108,140,255,0.3);
  --color-danger: #ff6b6b;
  --color-warn: #ffb347;
  --color-success: #4ecdc4;
  --transition-fast: 150ms ease;
  --transition-smooth: 300ms cubic-bezier(0.4,0,0.2,1);
}
body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
}
.topbar {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 20px; background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky; top: 0; z-index: 100;
}
.topbar h1 { font-size: 16px; font-weight: 600; letter-spacing: 0.3px; }
.topbar .badge {
  font-size: 11px; padding: 3px 8px; border-radius: 12px;
  background: var(--color-accent); color: #fff; font-weight: 500;
}
.topbar .spacer { flex: 1; }
.topbar button {
  padding: 6px 14px; border: 1px solid var(--color-border);
  background: var(--color-surface); color: var(--color-text);
  border-radius: 6px; cursor: pointer; font-size: 12px;
  transition: background var(--transition-fast);
}
.topbar button:hover { background: var(--color-surface-hover); }
.topbar button.danger { border-color: var(--color-danger); color: var(--color-danger); }
.grid {
  display: grid; gap: 12px; padding: 16px;
  grid-template-columns: repeat(4, 1fr);
  transition: grid-template-columns var(--transition-smooth), grid-template-rows var(--transition-smooth);
}
.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--panel-radius);
  padding: 16px;
  position: relative;
  transition: all var(--transition-smooth);
  cursor: grab;
  min-height: 120px;
  display: flex; flex-direction: column;
}
.panel:hover { border-color: var(--color-accent); box-shadow: 0 0 0 1px var(--color-accent-glow); }
.panel.locked { border-color: var(--color-warn); }
.panel.locked::after {
  content: ''; position: absolute; top: 6px; right: 6px;
  width: 8px; height: 8px; border-radius: 50%; background: var(--color-warn);
}
.panel.compact {
  padding: 10px 12px; min-height: 60px;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: block; }
.panel.compact .panel-header { font-size: 12px; }
.panel-header {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 14px; font-weight: 600; margin-bottom: 8px;
  user-select: none;
}
.panel-header .rank-dot {
  width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 6px;
}
.panel-body { flex: 1; font-size: 24px; font-weight: 700; display: flex; align-items: center; }
.panel-body .metric-value { font-family: var(--font-mono); }
.panel-preview { display: none; font-size: 11px; color: var(--color-text-dim); }
.panel-meta {
  display: flex; gap: 8px; margin-top: 8px; font-size: 10px; color: var(--color-text-dim);
}
.panel-actions {
  display: flex; gap: 4px;
}
.panel-actions button {
  background: none; border: none; color: var(--color-text-dim);
  cursor: pointer; font-size: 14px; padding: 2px 4px; border-radius: 4px;
  transition: color var(--transition-fast);
}
.panel-actions button:hover { color: var(--color-text); }
.panel-actions button.lock-btn.locked { color: var(--color-warn); }
.panel-actions button.pin-btn.pinned { color: var(--color-accent); }
.heatmap-legend {
  position: fixed; bottom: 16px; right: 16px;
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 10px 14px; font-size: 11px;
  display: flex; align-items: center; gap: 8px;
}
.heatmap-gradient {
  width: 80px; height: 10px; border-radius: 5px;
  background: linear-gradient(to right, #2a2e3a, #6c8cff, #ffb347);
}
.empty-state {
  grid-column: 1/-1; text-align: center; padding: 60px 20px;
  color: var(--color-text-dim); font-size: 14px;
}
.score-bar {
  height: 3px; background: var(--color-border); border-radius: 2px; margin-top: 6px;
}
.score-bar-fill {
  height: 100%; border-radius: 2px;
  background: linear-gradient(to right, var(--color-accent), var(--color-success));
  transition: width var(--transition-smooth);
}
</style>
</head>
<body>
<div class="topbar">
  <h1>Adaptive Dashboard</h1>
  <span class="badge" id="session-badge">Session 1</span>
  <span class="spacer"></span>
  <span style="font-size:11px;color:var(--color-text-dim)" id="tracking-status">● tracking</span>
  <button onclick="resetAll()" class="danger">Reset Layout</button>
  <button onclick="forceRecompute()">Recompute</button>
</div>
<div class="grid" id="grid"></div>
<div class="heatmap-legend">
  <span>Cold</span>
  <div class="heatmap-gradient"></div>
  <span>Hot</span>
</div>
<script>
// ============================================================
// THEME / CONSTANTS (centralized, no fragile CSS variable refs)
// ============================================================
const C = {
  VISIBILITY_CAP_DEFAULT: 5000,
  VISIBILITY_CAP_MIN: 1000,
  VISIBILITY_CAP_MAX: 30000,
  RECENCY_HALF_LIFE: 3600000,
  RECENCY_MIN: 0.05,
  DEBOUNCE_MS: 100,
  THROTTLE_MS: 100,
  SCORE_WEIGHTS: { freq: 0.4, dur: 0.35, recency: 0.25 },
  COMPACT_SCORE_FRACTION: 0.15,
  COLUMNS: 4,
  PANEL_SIZES: { large: '2fr', normal: '1fr', small: '0.5fr' },
  STORAGE_KEY_PREFS: 'aml_prefs',
  STORAGE_KEY_TRACKING: 'aml_tracking',
};
// ============================================================
// PANEL DEFINITIONS
// ============================================================
const PANEL_DEFS = [
  { id: 'cpu',     title: 'CPU Usage',     metric: '%',  initial: 42 },
  { id: 'memory',  title: 'Memory',        metric: 'GB', initial: 14.2 },
  { id: 'disk',    title: 'Disk I/O',      metric: 'MB/s', initial: 128 },
  { id: 'network', title: 'Network',       metric: 'Mbps', initial: 876 },
  { id: 'errors',  title: 'Error Rate',    metric: '/min', initial: 3 },
  { id: 'latency', title: 'P95 Latency',   metric: 'ms', initial: 47 },
  { id: 'rps',     title: 'Requests/s',    metric: 'rps', initial: 1240 },
  { id: 'cache',   title: 'Cache Hit %',   metric: '%', initial: 94.7 },
  { id: 'queue',   title: 'Queue Depth',   metric: 'items', initial: 18 },
  { id: 'uptime',  title: 'Uptime',        metric: 'days', initial: 127 },
  { id: 'users',   title: 'Active Users',  metric: 'online', initial: 3421 },
  { id: 'revenue', title: 'Revenue',       metric: '$/h', initial: 2840 },
];
// ============================================================
// STATE
// ============================================================
let panels = [];
let tracking = {};       // id -> { totalVisibleMs, interactions, lastSeen, collapseCount }
let prefs = {};          // id -> { locked, pinned, manualPosition }
let sessionStart = Date.now();
let sessionCount = 1;
let observer = null;
let rafScheduled = false;
let recomputeScheduled = false;
let resizeDebounce = null;
// ============================================================
// STORAGE
// ============================================================
function loadState() {
  try {
    const rawT = localStorage.getItem(C.STORAGE_KEY_TRACKING);
    if (rawT) tracking = JSON.parse(rawT);
    const rawP = localStorage.getItem(C.STORAGE_KEY_PREFS);
    if (rawP) prefs = JSON.parse(rawP);
  } catch(e) { /* ignore corrupt storage */ }
}
function saveState() {
  try {
    localStorage.setItem(C.STORAGE_KEY_TRACKING, JSON.stringify(tracking));
    localStorage.setItem(C.STORAGE_KEY_PREFS, JSON.stringify(prefs));
  } catch(e) { /* storage full or disabled */ }
}
// ============================================================
// TRACKING
// ============================================================
function ensureTracking(id) {
  if (!tracking[id]) {
    tracking[id] = { totalVisibleMs: 0, interactions: 0, lastSeen: 0, collapseCount: 0 };
  }
}
function recordVisibility(id, visibleMs) {
  ensureTracking(id);
  tracking[id].totalVisibleMs += visibleMs;
  tracking[id].lastSeen = Date.now();
}
function recordInteraction(id) {
  ensureTracking(id);
  tracking[id].interactions++;
  tracking[id].lastSeen = Date.now();
  scheduleRecompute();
}
function recordCollapse(id) {
  ensureTracking(id);
  tracking[id].collapseCount++;
  tracking[id].lastSeen = Date.now();
}
// ============================================================
// SCORING (cached, single-pass)
// ============================================================
let scoreCache = null;
function computeScores() {
  const now = Date.now();
  const cap = C.VISIBILITY_CAP_DEFAULT;
  const w = C.SCORE_WEIGHTS;
  let maxFreq = 1, maxDur = 1;
  // Find maxes in one pass
  for (const p of panels) {
    const t = tracking[p.id] || { totalVisibleMs: 0, interactions: 0 };
    if (t.interactions > maxFreq) maxFreq = t.interactions;
    if (t.totalVisibleMs > maxDur) maxDur = t.totalVisibleMs;
  }
  maxFreq = Math.max(maxFreq, 1);
  maxDur = Math.max(maxDur, 1);
  // Now single-pass: build cache
  scoreCache = {};
  for (const p of panels) {
    const t = tracking[p.id] || { totalVisibleMs: 0, interactions: 0, lastSeen: 0 };
    const freqNorm = t.interactions / maxFreq;
    const durClamped = Math.min(t.totalVisibleMs, cap);
    const durNorm = durClamped / Math.max(maxDur, cap);
    const ageMs = now - t.lastSeen;
    const recency = Math.max(Math.pow(0.5, ageMs / C.RECENCY_HALF_LIFE), C.RECENCY_MIN);
    const score = (freqNorm * w.freq) + (durNorm * w.dur) + (recency * w.recency);
    scoreCache[p.id] = score;
  }
  return scoreCache;
}
function getRankedPanels() {
  const scores = scoreCache || computeScores();
  return [...panels].sort((a, b) => (scores[b.id] || 0) - (scores[a.id] || 0));
}
function maxScore() {
  if (!scoreCache) computeScores();
  let m = 0;
  for (const k in scoreCache) { if (scoreCache[k] > m) m = scoreCache[k]; }
  return m || 1;
}
// ============================================================
// LAYOUT (debounced recompute)
// ============================================================
function scheduleRecompute() {
  if (recomputeScheduled) return;
  recomputeScheduled = true;
  requestAnimationFrame(() => {
    recomputeScheduled = false;
    computeScores();
    applyLayout();
    saveState();
  });
}
function applyLayout() {
  const grid = document.getElementById('grid');
  const ranked = getRankedPanels();
  const scores = scoreCache || computeScores();
  const ms = maxScore();
  const compactThreshold = ms * C.COMPACT_SCORE_FRACTION;
  // Build grid children in ranked order
  // Manual overrides: locked panels pin to saved position
  const ordered = [];
  const overridden = [];
  for (const p of ranked) {
    const pr = prefs[p.id] || {};
    if (pr.locked || pr.pinned) {
      overridden.push(p);
    } else {
      ordered.push(p);
    }
  }
  // Overrides go first (they hold their position)
  const finalOrder = [...overridden, ...ordered];
  // Clear grid
  grid.innerHTML = '';
  if (finalOrder.length === 0) {
    grid.innerHTML = '<div class="empty-state">No panels. Reset layout to restore defaults.</div>';
    return;
  }
  for (let i = 0; i < finalOrder.length; i++) {
    const p = finalOrder[i];
    const score = scores[p.id] || 0;
    const isCompact = score < compactThreshold && !(prefs[p.id] && prefs[p.id].locked);
    const el = buildPanelDOM(p, score, isCompact, ms);
    grid.appendChild(el);
  }
}
function buildPanelDOM(p, score, compact, maxS) {
  const div = document.createElement('div');
  div.className = 'panel' + (compact ? ' compact' : '') + ((prefs[p.id] && prefs[p.id].locked) ? ' locked' : '');
  div.dataset.panelId = p.id;
  div.draggable = false;
  const scorePct = maxS > 0 ? (score / maxS * 100) : 0;
  const hotness = scorePct > 66 ? 'hot' : scorePct > 33 ? 'warm' : 'cold';
  const dotColor = hotness === 'hot' ? 'var(--color-danger)' : hotness === 'warm' ? 'var(--color-warn)' : 'var(--color-text-dim)';
  div.innerHTML =
    '<div class="panel-header">' +
      '<span><span class="rank-dot" style="background:' + dotColor + '"></span>' + esc(p.title) + '</span>' +
      '<div class="panel-actions">' +
        '<button class="pin-btn' + ((prefs[p.id] && prefs[p.id].pinned) ? ' pinned' : '') + '" title="Pin position" onclick="togglePin(\'' + p.id + '\')">' + String.fromCodePoint(0x1F4CC) + '</button>' +
        '<button class="lock-btn' + ((prefs[p.id] && prefs[p.id].locked) ? ' locked' : '') + '" title="Lock position" onclick="toggleLock(\'' + p.id + '\')">' + String.fromCodePoint(0x1F512) + '</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body"><span class="metric-value">' + p.initial + '</span><span style="font-size:14px;margin-left:4px">' + esc(p.metric) + '</span></div>' +
    '<div class="panel-preview">' + esc(p.title) + ': ' + p.initial + ' ' + esc(p.metric) + '</div>' +
    '<div class="score-bar"><div class="score-bar-fill" style="width:' + scorePct.toFixed(0) + '%"></div></div>' +
    '<div class="panel-meta"><span>Score: ' + score.toFixed(2) + '</span><span>' + hotness + '</span></div>';
  div.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') return;
    recordInteraction(p.id);
    // Simulate metric update on click
    const mv = div.querySelector('.metric-value');
    if (mv) {
      const delta = (Math.random() * 10 - 5).toFixed(1);
      mv.textContent = (parseFloat(p.initial) + parseFloat(delta)).toFixed(1);
    }
  });
  return div;
}
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
// ============================================================
// VISIBILITY OBSERVER (duration tracking)
// ============================================================
const visibilityMap = new Map(); // id -> { enterTime }
function setupObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    const now = Date.now();
    for (const e of entries) {
      const id = e.target.dataset.panelId;
      if (!id) continue;
      if (e.isIntersecting) {
        visibilityMap.set(id, now);
      } else {
        const enter = visibilityMap.get(id);
        if (enter) {
          const visibleMs = now - enter;
          if (visibleMs > 0) {
            recordVisibility(id, visibleMs);
          }
          visibilityMap.delete(id);
        }
      }
    }
    // Throttled recompute via rAF
    if (!rafScheduled) {
      rafScheduled = true;
      requestAnimationFrame(() => {
        rafScheduled = false;
        scheduleRecompute();
      });
    }
  }, { threshold: 0.3 });
  // Observe all panels
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
// Flush any current visibility on page unload
function flushVisibility() {
  const now = Date.now();
  for (const [id, enter] of visibilityMap) {
    const visibleMs = now - enter;
    if (visibleMs > 0) recordVisibility(id, visibleMs);
  }
  visibilityMap.clear();
  saveState();
}
// ============================================================
// MANUAL OVERRIDES
// ============================================================
function toggleLock(id) {
  if (!prefs[id]) prefs[id] = {};
  prefs[id].locked = !prefs[id].locked;
  if (prefs[id].locked) recordInteraction(id);
  scheduleRecompute();
}
function togglePin(id) {
  if (!prefs[id]) prefs[id] = {};
  prefs[id].pinned = !prefs[id].pinned;
  if (prefs[id].pinned) recordInteraction(id);
  scheduleRecompute();
}
function resetAll() {
  tracking = {};
  prefs = {};
  scoreCache = null;
  visibilityMap.clear();
  sessionCount++;
  document.getElementById('session-badge').textContent = 'Session ' + sessionCount;
  saveState();
  initPanels();
  computeScores();
  applyLayout();
  // Re-observe after DOM rebuild
  setTimeout(setupObserver, 50);
}
function forceRecompute() {
  scoreCache = null;
  computeScores();
  applyLayout();
  setupObserver();
}
// ============================================================
// SIMULATED METRIC UPDATES
// ============================================================
function tickMetrics() {
  for (const p of panels) {
    const delta = (Math.random() * 4 - 2);
    p.initial = Math.max(0, parseFloat((p.initial + delta).toFixed(1)));
  }
  // Update DOM values in place
  document.querySelectorAll('.panel').forEach(el => {
    const id = el.dataset.panelId;
    const p = panels.find(x => x.id === id);
    if (!p) return;
    const mv = el.querySelector('.metric-value');
    if (mv) mv.textContent = p.initial;
    const preview = el.querySelector('.panel-preview');
    if (preview) preview.textContent = p.title + ': ' + p.initial + ' ' + p.metric;
  });
}
// ============================================================
// INIT
// ============================================================
function initPanels() {
  panels = PANEL_DEFS.map(d => ({ ...d }));
}
loadState();
initPanels();
scoreCache = null;
computeScores();
applyLayout();
setupObserver();
// Periodic metric ticks
setInterval(tickMetrics, 4000);
// Periodic persistence
setInterval(saveState, 10000);
// Flush on unload
window.addEventListener('beforeunload', flushVisibility);
window.addEventListener('pagehide', flushVisibility);
// Debounced resize handler
window.addEventListener('resize', () => {
  clearTimeout(resizeDebounce);
  resizeDebounce = setTimeout(() => {
    scheduleRecompute();
  }, C.DEBOUNCE_MS);
});
// Throttled scroll (tracking only — observer handles visibility)
let scrollThrottle = null;
window.addEventListener('scroll', () => {
  if (scrollThrottle) return;
  scrollThrottle = requestAnimationFrame(() => {
    scrollThrottle = null;
    // Observer handles tracking; scroll itself needs no action
  });
}, { passive: true });
// Keyboard shortcut: R to recompute, L to lock first panel
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' && !e.ctrlKey && !e.metaKey && document.activeElement === document.body) {
    forceRecompute();
  }
});
document.getElementById('session-badge').textContent = 'Session ' + sessionCount;
document.getElementById('tracking-status').textContent = String.fromCodePoint(0x25CF) + ' tracking';
</script>
</body>
</html>