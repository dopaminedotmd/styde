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
  --surface-hover: #22252f;
  --border: #2a2d37;
  --text: #e1e4eb;
  --text-muted: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff5c6c;
  --success: #4ade80;
  --warn: #f59e0b;
  --radius: 8px;
  --transition-speed: 0.2s;
  --compact-scale: 0.45;
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--bg);
  color:var(--text);
  font-family:system-ui,-apple-system,sans-serif;
  min-height:100vh;
  padding:16px;
}
.toolbar{
  display:flex;
  gap:10px;
  margin-bottom:16px;
  flex-wrap:wrap;
  align-items:center;
}
.toolbar button{
  background:var(--surface);
  color:var(--text);
  border:1px solid var(--border);
  padding:8px 16px;
  border-radius:var(--radius);
  cursor:pointer;
  font-size:13px;
  transition:background var(--transition-speed);
}
.toolbar button:hover{background:var(--surface-hover)}
.toolbar button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.toolbar .spacer{flex:1}
.stats{
  font-size:12px;
  color:var(--text-muted);
  background:var(--surface);
  padding:6px 12px;
  border-radius:var(--radius);
}
.dashboard{
  display:grid;
  gap:12px;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  grid-auto-rows:minmax(160px,auto);
  transition:grid-template-columns 0.3s ease,grid-template-rows 0.3s ease;
}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:16px;
  position:relative;
  overflow:hidden;
  transition:transform var(--transition-speed),opacity var(--transition-speed),grid-column var(--transition-speed),grid-row var(--transition-speed),width var(--transition-speed),height var(--transition-speed);
  display:flex;
  flex-direction:column;
  min-width:0;
}
.panel:hover{border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.panel.high-rank{grid-column:span 2;grid-row:span 2}
.panel.medium-rank{grid-column:span 1;grid-row:span 1}
.panel.low-rank{grid-column:span 1;grid-row:span 1;transform:scale(var(--compact-scale));transform-origin:top left;opacity:0.7;max-height:120px;max-width:280px}
.panel.low-rank:hover{transform:scale(1);opacity:1;max-height:none;max-width:none;z-index:100;position:relative}
.panel.locked{border-color:var(--warn);box-shadow:0 0 12px rgba(245,158,11,0.2)}
.panel.locked::after{
  content:"LOCKED";
  position:absolute;
  top:6px;
  right:6px;
  background:var(--warn);
  color:#000;
  font-size:10px;
  padding:2px 6px;
  border-radius:3px;
  font-weight:700;
}
.panel-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:8px;
  gap:6px;
}
.panel-title{font-weight:600;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{
  background:none;
  border:1px solid var(--border);
  color:var(--text-muted);
  width:24px;
  height:24px;
  border-radius:4px;
  cursor:pointer;
  font-size:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  transition:all var(--transition-speed);
}
.panel-actions button:hover{background:var(--surface-hover);color:var(--text)}
.panel-actions button.lock-btn.locked-state{background:var(--warn);color:#000;border-color:var(--warn)}
.panel-content{flex:1;min-height:0;overflow:auto;font-size:13px}
.panel-content .metric-value{font-size:28px;font-weight:700;color:var(--accent)}
.panel-content .metric-label{font-size:11px;color:var(--text-muted);margin-top:2px}
.panel-content .chart-placeholder{
  height:80px;
  background:linear-gradient(135deg,var(--accent) 0%,transparent 100%);
  border-radius:var(--radius);
  opacity:0.15;
  margin-top:8px;
}
.panel-rank-badge{
  position:absolute;
  bottom:6px;
  left:6px;
  font-size:10px;
  color:var(--text-muted);
  background:var(--bg);
  padding:1px 6px;
  border-radius:3px;
}
/* Animation fallback: use opacity+transform instead of grid properties */
@supports not (transition:grid-column 0.3s){
  .panel{transition:transform var(--transition-speed),opacity var(--transition-speed),width var(--transition-speed),height var(--transition-speed)}
}
.tooltip{
  position:fixed;
  background:var(--surface);
  border:1px solid var(--accent);
  color:var(--text);
  padding:8px 12px;
  border-radius:var(--radius);
  font-size:12px;
  pointer-events:none;
  z-index:9999;
  max-width:280px;
  box-shadow:0 4px 20px rgba(0,0,0,0.5);
  opacity:0;
  transition:opacity 0.15s;
}
.tooltip.visible{opacity:1}
.reset-warning{
  background:var(--danger);
  color:#fff;
  padding:8px 16px;
  border-radius:var(--radius);
  font-size:13px;
  margin-bottom:12px;
  display:none;
}
.reset-warning.show{display:block}
@media(max-width:768px){
  .dashboard{grid-template-columns:1fr}
  .panel.high-rank{grid-column:span 1}
}
</style>
</head>
<body>
<div class="reset-warning" id="resetWarning">Private browsing detected. Layout data is stored in memory only — it will be lost when you close this tab.</div>
<div class="toolbar">
  <button onclick="toggleAutoArrange()" id="autoBtn" class="active">Auto-Arrange: ON</button>
  <button onclick="resetAllData()">Reset All Data</button>
  <button onclick="exportData()">Export Data</button>
  <span class="spacer"></span>
  <span class="stats" id="statsDisplay">Tracking 0 panels | Session: 0s</span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<script>
'use strict';
const STORE_KEY = 'adaptive_dashboard_v1';
const TRACKING_INTERVAL_MS = 2000;
const COMPACT_THRESHOLD = 0.15;
const HIGH_RANK_THRESHOLD = 0.7;
const VIEWPORT_PADDING = 12;
let store = null;
let panels = new Map();
let trackingState = new Map();
let prevTrackingSnapshot = '';
let autoArrange = true;
let sessionStart = Date.now();
let trackingTimer = null;
function createStore() {
  try {
    const testKey = '__hermes_store_test__';
    localStorage.setItem(testKey, '1');
    localStorage.removeItem(testKey);
    return {
      get(k, fallback) {
        try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : fallback; }
        catch (e) { return fallback; }
      },
      set(k, v) {
        try { localStorage.setItem(k, JSON.stringify(v)); return true; }
        catch (e) { return false; }
      },
      remove(k) {
        try { localStorage.removeItem(k); return true; }
        catch (e) { return false; }
      },
      get persistent() { return true; }
    };
  } catch (e) {
    document.getElementById('resetWarning').classList.add('show');
    const mem = new Map();
    return {
      get(k, fallback) { return mem.has(k) ? JSON.parse(JSON.stringify(mem.get(k))) : fallback; },
      set(k, v) { mem.set(k, JSON.parse(JSON.stringify(v))); return true; },
      remove(k) { mem.delete(k); return true; },
      get persistent() { return false; }
    };
  }
}
store = createStore();
const DEFAULT_PANELS = [
  { id: 'cpu', title: 'CPU Usage', metric: '23%', label: 'of 8 cores', color: '#6c8cff' },
  { id: 'memory', title: 'Memory', metric: '7.2 GB', label: 'of 16 GB', color: '#4ade80' },
  { id: 'requests', title: 'Requests/min', metric: '1,247', label: 'avg over 5min', color: '#f59e0b' },
  { id: 'latency', title: 'P95 Latency', metric: '142ms', label: 'p50: 34ms', color: '#ff5c6c' },
  { id: 'errors', title: 'Error Rate', metric: '0.12%', label: 'last hour', color: '#a78bfa' },
  { id: 'users', title: 'Active Users', metric: '892', label: 'concurrent', color: '#38bdf8' },
  { id: 'storage', title: 'Disk I/O', metric: '340 MB/s', label: 'read: 280 write: 60', color: '#fb923c' },
  { id: 'network', title: 'Network', metric: '8.4 Gbps', label: 'in: 5.1 out: 3.3', color: '#34d399' },
];
function loadData() {
  return store.get(STORE_KEY, {
    panels: {},
    settings: { autoArrange: true },
    sessionStart: Date.now()
  });
}
function saveData(data) {
  store.set(STORE_KEY, data);
}
function initPanelData(panelId) {
  return {
    interactions: 0,
    totalViewDuration: 0,
    lastInteraction: 0,
    expandCount: 0,
    collapseCount: 0,
    locked: false,
    manualPosition: null,
    visible: true
  };
}
function getOrCreatePanelStats(panelId) {
  const data = loadData();
  if (!data.panels[panelId]) {
    data.panels[panelId] = initPanelData(panelId);
    saveData(data);
  }
  return data.panels[panelId];
}
function updatePanelStats(panelId, updates) {
  const data = loadData();
  if (!data.panels[panelId]) {
    data.panels[panelId] = initPanelData(panelId);
  }
  const seen = new Set(Object.keys(updates));
  for (const k of seen) {
    data.panels[panelId][k] = updates[k];
  }
  saveData(data);
}
function getCompositeScore(stats, now) {
  const recencyBonus = stats.lastInteraction > 0
    ? Math.max(0, 1 - (now - stats.lastInteraction) / (3600 * 1000))
    : 0;
  const freqScore = Math.log2(stats.interactions + 1) / Math.log2(100);
  const durScore = Math.min(1, stats.totalViewDuration / 300000);
  return (freqScore * 0.35 + durScore * 0.35 + recencyBonus * 0.30);
}
function getAllScores() {
  const data = loadData();
  const now = Date.now();
  const scores = new Map();
  const panelIds = new Set(DEFAULT_PANELS.map(p => p.id));
  for (const id of panelIds) {
    const stats = data.panels[id] || initPanelData(id);
    scores.set(id, getCompositeScore(stats, now));
  }
  return scores;
}
function getRankedPanels() {
  const scores = getAllScores();
  const maxScore = Math.max(0.001, ...scores.values());
  const ranked = [];
  for (const [id, score] of scores) {
    ranked.push({ id, score, normalized: score / maxScore });
  }
  ranked.sort((a, b) => b.score - a.score);
  return ranked;
}
function getRankClass(normalized) {
  if (normalized >= HIGH_RANK_THRESHOLD) return 'high-rank';
  if (normalized >= COMPACT_THRESHOLD) return 'medium-rank';
  return 'low-rank';
}
function buildPanelHTML(panelDef, rankInfo) {
  const data = loadData();
  const stats = data.panels[panelDef.id] || initPanelData(panelDef.id);
  const rankClass = getRankClass(rankInfo.normalized);
  const isLocked = stats.locked;
  const lockClass = isLocked ? 'locked locked-state' : '';
  return '<div class="panel ' + rankClass + (isLocked ? ' locked' : '') + '" data-panel-id="' + panelDef.id + '" style="border-left:3px solid ' + panelDef.color + '">'
    + '<div class="panel-header">'
    + '<span class="panel-title">' + panelDef.title + '</span>'
    + '<div class="panel-actions">'
    + '<button class="lock-btn ' + lockClass + '" data-action="lock" title="Lock position">L</button>'
    + '<button data-action="expand" title="Expand">+</button>'
    + '<button data-action="collapse" title="Collapse">-</button>'
    + '</div>'
    + '</div>'
    + '<div class="panel-content">'
    + '<div class="metric-value" style="color:' + panelDef.color + '">' + panelDef.metric + '</div>'
    + '<div class="metric-label">' + panelDef.label + '</div>'
    + '<div class="chart-placeholder"></div>'
    + '</div>'
    + '<div class="panel-rank-badge">Score: ' + (rankInfo.normalized * 100).toFixed(1) + '% | Hits: ' + stats.interactions + '</div>'
    + '</div>';
}
function recordInteraction(panelId, type) {
  const now = Date.now();
  const updates = { lastInteraction: now };
  if (type === 'view') {
    updates.totalViewDuration = (getOrCreatePanelStats(panelId).totalViewDuration || 0) + TRACKING_INTERVAL_MS;
  } else if (type === 'click') {
    updates.interactions = (getOrCreatePanelStats(panelId).interactions || 0) + 1;
  } else if (type === 'expand') {
    updates.expandCount = (getOrCreatePanelStats(panelId).expandCount || 0) + 1;
    updates.interactions = (getOrCreatePanelStats(panelId).interactions || 0) + 1;
  } else if (type === 'collapse') {
    updates.collapseCount = (getOrCreatePanelStats(panelId).collapseCount || 0) + 1;
    updates.interactions = (getOrCreatePanelStats(panelId).interactions || 0) + 1;
  }
  updatePanelStats(panelId, updates);
}
function trackVisiblePanels() {
  const visibleIds = new Set();
  const dashboardEl = document.getElementById('dashboard');
  if (!dashboardEl) return;
  const dbRect = dashboardEl.getBoundingClientRect();
  for (const panelEl of dashboardEl.children) {
    if (!panelEl.dataset.panelId) continue;
    const rect = panelEl.getBoundingClientRect();
    const visible = (
      rect.bottom > dbRect.top &&
      rect.top < dbRect.bottom &&
      rect.right > dbRect.left &&
      rect.left < dbRect.right
    );
    if (visible) {
      visibleIds.add(panelEl.dataset.panelId);
    }
  }
  const nowKey = Array.from(visibleIds).sort().join(',');
  // Early-return guard: skip if unchanged
  if (nowKey === prevTrackingSnapshot) return;
  prevTrackingSnapshot = nowKey;
  for (const id of visibleIds) {
    recordInteraction(id, 'view');
  }
}
function renderDashboard() {
  const dashboard = document.getElementById('dashboard');
  const ranked = getRankedPanels();
  const panelDefMap = new Map(DEFAULT_PANELS.map(p => [p.id, p]));
  const scoreMap = new Map(ranked.map(r => [r.id, r]));
  let html = '';
  for (const entry of ranked) {
    const def = panelDefMap.get(entry.id);
    if (!def) continue;
    html += buildPanelHTML(def, entry);
  }
  dashboard.innerHTML = html;
  bindPanelEvents();
}
function bindPanelEvents() {
  const dashboard = document.getElementById('dashboard');
  const seen = new Set();
  for (const el of dashboard.querySelectorAll('[data-panel-id]')) {
    const id = el.dataset.panelId;
    if (seen.has(id)) continue;
    seen.add(id);
    el.addEventListener('click', function(e) {
      const action = e.target.dataset.action;
      if (action === 'lock') {
        e.stopPropagation();
        toggleLock(id);
        return;
      }
      if (action === 'expand') {
        e.stopPropagation();
        recordInteraction(id, 'expand');
        return;
      }
      if (action === 'collapse') {
        e.stopPropagation();
        recordInteraction(id, 'collapse');
        return;
      }
      recordInteraction(id, 'click');
    });
    el.addEventListener('mouseenter', function(e) {
      showTooltip(e, id);
    });
    el.addEventListener('mouseleave', hideTooltip);
  }
}
function toggleLock(panelId) {
  const stats = getOrCreatePanelStats(panelId);
  updatePanelStats(panelId, { locked: !stats.locked });
  renderDashboard();
}
function showTooltip(e, panelId) {
  const stats = getOrCreatePanelStats(panelId);
  const scores = getAllScores();
  const score = scores.get(panelId) || 0;
  const tt = document.getElementById('tooltip');
  tt.innerHTML = 'Interactions: ' + stats.interactions
    + '<br>View time: ' + (stats.totalViewDuration / 1000).toFixed(0) + 's'
    + '<br>Expands: ' + (stats.expandCount || 0)
    + '<br>Collapses: ' + (stats.collapseCount || 0)
    + '<br>Score: ' + (score * 100).toFixed(1) + '%'
    + '<br>' + (stats.locked ? 'LOCKED' : 'Auto-positioned');
  tt.classList.add('visible');
  positionTooltip(e.clientX, e.clientY);
}
function positionTooltip(mx, my) {
  const tt = document.getElementById('tooltip');
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  let x = mx + VIEWPORT_PADDING;
  let y = my + VIEWPORT_PADDING;
  const ttRect = tt.getBoundingClientRect();
  if (x + ttRect.width > vw - VIEWPORT_PADDING) {
    x = mx - ttRect.width - VIEWPORT_PADDING;
  }
  if (y + ttRect.height > vh - VIEWPORT_PADDING) {
    y = my - ttRect.height - VIEWPORT_PADDING;
  }
  if (x < VIEWPORT_PADDING) x = VIEWPORT_PADDING;
  if (y < VIEWPORT_PADDING) y = VIEWPORT_PADDING;
  tt.style.left = x + 'px';
  tt.style.top = y + 'px';
}
function hideTooltip() {
  document.getElementById('tooltip').classList.remove('visible');
}
function toggleAutoArrange() {
  autoArrange = !autoArrange;
  const btn = document.getElementById('autoBtn');
  if (autoArrange) {
    btn.textContent = 'Auto-Arrange: ON';
    btn.classList.add('active');
  } else {
    btn.textContent = 'Auto-Arrange: OFF';
    btn.classList.remove('active');
  }
  const data = loadData();
  data.settings.autoArrange = autoArrange;
  saveData(data);
  if (autoArrange) renderDashboard();
}
function resetAllData() {
  store.remove(STORE_KEY);
  prevTrackingSnapshot = '';
  renderDashboard();
}
function exportData() {
  const data = loadData();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'dashboard-layout-' + new Date().toISOString().slice(0,10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
}
function updateStatsDisplay() {
  const data = loadData();
  const panelCount = Object.keys(data.panels).length;
  const sessionSec = Math.floor((Date.now() - sessionStart) / 1000);
  document.getElementById('statsDisplay').textContent = 'Tracking ' + panelCount + ' panels | Session: ' + sessionSec + 's';
}
function startTracking() {
  const data = loadData();
  autoArrange = data.settings.autoArrange !== false;
  const btn = document.getElementById('autoBtn');
  if (autoArrange) {
    btn.textContent = 'Auto-Arrange: ON';
    btn.classList.add('active');
  } else {
    btn.textContent = 'Auto-Arrange: OFF';
    btn.classList.remove('active');
  }
  sessionStart = data.sessionStart || Date.now();
  if (trackingTimer) clearInterval(trackingTimer);
  trackingTimer = setInterval(function() {
    if (!autoArrange) {
      updateStatsDisplay();
      return;
    }
    trackVisiblePanels();
    updateStatsDisplay();
    const ranked = getRankedPanels();
    const dashboard = document.getElementById('dashboard');
    const panelEls = new Map();
    for (const el of dashboard.querySelectorAll('[data-panel-id]')) {
      panelEls.set(el.dataset.panelId, el);
    }
    for (const entry of ranked) {
      const el = panelEls.get(entry.id);
      if (!el) continue;
      const data = loadData();
      const stats = data.panels[entry.id];
      if (stats && stats.locked) continue;
      const targetClass = getRankClass(entry.normalized);
      el.classList.remove('high-rank', 'medium-rank', 'low-rank');
      el.classList.add(targetClass);
      const badge = el.querySelector('.panel-rank-badge');
      if (badge) {
        badge.textContent = 'Score: ' + (entry.normalized * 100).toFixed(1) + '% | Hits: ' + (stats ? stats.interactions : 0);
      }
    }
  }, TRACKING_INTERVAL_MS);
}
renderDashboard();
startTracking();
updateStatsDisplay();
</script>
</body>
</html>