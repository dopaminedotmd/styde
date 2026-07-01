<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117; --panel-bg: #1a1d27; --panel-border: #2a2d3a;
  --text: #e1e4ed; --text-dim: #8b8fa8; --accent: #5b8def;
  --accent-glow: rgba(91,141,239,0.18); --warn: #f0a050; --danger: #e0556a;
  --success: #4ec990; --grid-gap: 10px; --panel-radius: 10px;
  --transition-speed: 0.35s;
}
body {
  background: var(--bg); color: var(--text); font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh; overflow-x: hidden; -webkit-tap-highlight-color: transparent;
  user-select: none; -webkit-user-select: none;
}
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px; border-bottom: 1px solid var(--panel-border); flex-wrap: wrap; gap: 10px;
}
.header h1 { font-size: 1.3rem; font-weight: 600; letter-spacing: -0.3px; }
.controls { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.controls button, .controls select {
  background: var(--panel-bg); border: 1px solid var(--panel-border); color: var(--text);
  padding: 7px 14px; border-radius: 6px; cursor: pointer; font-size: 0.82rem;
  transition: border-color var(--transition-speed), background var(--transition-speed);
  touch-action: manipulation;
}
.controls button:hover, .controls select:hover { border-color: var(--accent); }
.controls button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.refresh-indicator { font-size: 0.75rem; color: var(--text-dim); display: flex; align-items: center; gap: 5px; }
.refresh-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--success); display: inline-block; }
.refresh-dot.off { background: var(--text-dim); }
.dashboard {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--grid-gap); padding: 16px;
  transition: grid-template-columns 0.3s ease, grid-template-rows 0.3s ease;
}
.panel {
  background: var(--panel-bg); border: 1px solid var(--panel-border);
  border-radius: var(--panel-radius); padding: 16px; position: relative;
  transition: transform var(--transition-speed), box-shadow var(--transition-speed),
              grid-column var(--transition-speed), grid-row var(--transition-speed),
              opacity var(--transition-speed);
  cursor: grab; touch-action: none; overflow: hidden;
  display: flex; flex-direction: column; gap: 8px;
}
.panel:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.3); border-color: var(--accent); }
.panel.dragging { opacity: 0.7; z-index: 100; cursor: grabbing; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
.panel.locked { cursor: default; }
.panel.locked .lock-indicator { display: block; }
.panel.pinned { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 0 16px var(--accent-glow); }
.panel.high-rank { grid-column: span 2; grid-row: span 1; }
.panel.mid-rank { grid-column: span 1; grid-row: span 1; }
.panel.low-rank { grid-column: span 1; grid-row: span 1; }
.panel.compact { padding: 10px; gap: 4px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-title { font-size: 0.78rem; }
.panel.compact .panel-value { font-size: 1.1rem; }
.panel-title {
  font-size: 0.85rem; font-weight: 600; color: var(--text-dim);
  display: flex; align-items: center; justify-content: space-between;
  letter-spacing: 0.2px; text-transform: uppercase;
}
.panel-value { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; }
.panel-value.warn { color: var(--warn); }
.panel-value.danger { color: var(--danger); }
.panel-value.success { color: var(--success); }
.panel-body { flex: 1; min-height: 70px; position: relative; }
.panel-body canvas { width: 100%; height: 100%; display: block; }
.panel-actions {
  display: flex; gap: 6px; position: absolute; top: 10px; right: 10px;
  opacity: 0; transition: opacity 0.2s;
}
.panel:hover .panel-actions { opacity: 1; }
.panel-actions button {
  background: rgba(255,255,255,0.06); border: none; color: var(--text-dim);
  width: 26px; height: 26px; border-radius: 5px; cursor: pointer; font-size: 0.75rem;
  display: flex; align-items: center; justify-content: center; touch-action: manipulation;
  transition: background 0.2s, color 0.2s;
}
.panel-actions button:hover { background: rgba(255,255,255,0.14); color: var(--text); }
.lock-indicator { display: none; position: absolute; top: 8px; left: 10px; font-size: 0.65rem; color: var(--accent); }
.trend { font-size: 0.78rem; display: flex; align-items: center; gap: 4px; }
.trend.up { color: var(--danger); }
.trend.down { color: var(--success); }
.trend.stable { color: var(--text-dim); }
.drag-over { border: 2px dashed var(--accent); }
.reset-banner {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  background: var(--accent); color: #fff; padding: 10px 22px; border-radius: 8px;
  font-size: 0.85rem; z-index: 200; cursor: pointer;
  box-shadow: 0 4px 18px rgba(91,141,239,0.4); animation: slideUp 0.3s ease;
  touch-action: manipulation;
}
@keyframes slideUp { from { transform: translateX(-50%) translateY(20px); opacity: 0; } to { transform: translateX(-50%) translateY(0); opacity: 1; } }
.heatmap-legend {
  position: fixed; bottom: 16px; right: 16px; background: var(--panel-bg);
  border: 1px solid var(--panel-border); border-radius: 8px; padding: 10px 14px;
  font-size: 0.72rem; color: var(--text-dim); z-index: 50;
}
.heatmap-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
@media (max-width: 640px) {
  .dashboard { grid-template-columns: 1fr; padding: 8px; }
  .panel.high-rank { grid-column: span 1; }
  .header { padding: 10px 14px; }
  .header h1 { font-size: 1.1rem; }
}
</style>
</head>
<body>
<header class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <select id="pollInterval" title="Auto-refresh interval">
      <option value="0">Off</option>
      <option value="5000">5s</option>
      <option value="15000" selected>15s</option>
      <option value="30000">30s</option>
    </select>
    <span class="refresh-indicator"><span class="refresh-dot" id="refreshDot"></span><span id="refreshLabel">15s</span></span>
    <button id="btnReset" title="Reset layout to defaults">Reset</button>
    <button id="btnCompactAll" title="Toggle compact all">Compact</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<script>
// --- Metric Schema & Data Layer ---
const METRIC_SCHEMA = {
  cpu:    { name: 'CPU Usage',     unit: '%',   warn: 70, danger: 90, history: [] },
  memory: { name: 'Memory',        unit: '%',   warn: 75, danger: 90, history: [] },
  reqs:   { name: 'Requests/s',    unit: '/s',  warn: 800, danger: 1500, history: [] },
  errors: { name: 'Error Rate',    unit: '%',   warn: 2, danger: 5, history: [] },
  latency:{ name: 'P95 Latency',   unit: 'ms',  warn: 200, danger: 500, history: [] },
  disk:   { name: 'Disk I/O',      unit: 'MB/s',warn: 80, danger: 150, history: [] },
  net:    { name: 'Network',       unit: 'Mbps',warn: 400, danger: 800, history: [] },
  conns:  { name: 'Connections',   unit: '',    warn: 2000, danger: 4000, history: [] },
};
const HISTORY_LENGTH = 60;
let metricState = {};
function seedHistory(key) {
  const s = METRIC_SCHEMA[key];
  const base = s.warn * 0.35 + Math.random() * s.warn * 0.3;
  const history = [];
  let val = base;
  for (let i = 0; i < HISTORY_LENGTH; i++) {
    val += (Math.random() - 0.48) * s.warn * 0.08;
    val = Math.max(0, Math.min(s.danger * 1.15, val));
    history.push(val);
  }
  s.history = history;
  metricState[key] = { value: history[history.length - 1], trend: 0 };
}
function simulateTick() {
  for (const key of Object.keys(METRIC_SCHEMA)) {
    const s = METRIC_SCHEMA[key];
    const last = s.history[s.history.length - 1] || s.warn * 0.4;
    const noise = (Math.random() - 0.48) * s.warn * 0.06;
    const spike = Math.random() < 0.05 ? (Math.random() - 0.5) * s.warn * 0.25 : 0;
    let next = last + noise + spike;
    next = Math.max(0, Math.min(s.danger * 1.15, next));
    s.history.push(next);
    if (s.history.length > HISTORY_LENGTH) s.history.shift();
    const prev = metricState[key].value;
    metricState[key] = { value: next, trend: next - prev };
  }
}
Object.keys(METRIC_SCHEMA).forEach(seedHistory);
// --- Usage Tracking ---
const TRACKING_KEY = 'adaptive_dashboard_tracking';
const LAYOUT_KEY = 'adaptive_dashboard_layout';
let usageData = loadUsage();
let layoutOverrides = loadLayout();
function loadUsage() {
  try { const d = JSON.parse(localStorage.getItem(TRACKING_KEY)); return d && typeof d === 'object' ? d : {}; }
  catch { return {}; }
}
function saveUsage() { localStorage.setItem(TRACKING_KEY, JSON.stringify(usageData)); }
function loadLayout() {
  try { const d = JSON.parse(localStorage.getItem(LAYOUT_KEY)); return d && typeof d === 'object' ? d : {}; }
  catch { return {}; }
}
function saveLayout() { localStorage.setItem(LAYOUT_KEY, JSON.stringify(layoutOverrides)); }
function ensureUsageEntry(key) {
  if (!usageData[key]) usageData[key] = { frequency: 0, totalDuration: 0, lastAccess: 0, collapses: 0 };
}
function trackViewStart(key) {
  ensureUsageEntry(key);
  usageData[key]._viewStart = Date.now();
}
function trackViewEnd(key) {
  ensureUsageEntry(key);
  if (usageData[key]._viewStart) {
    usageData[key].totalDuration += Date.now() - usageData[key]._viewStart;
    usageData[key]._viewStart = 0;
  }
  usageData[key].frequency += 1;
  usageData[key].lastAccess = Date.now();
  saveUsageDebounced();
}
function trackCollapse(key) {
  ensureUsageEntry(key);
  usageData[key].collapses += 1;
  saveUsageDebounced();
}
let saveUsageTimer = null;
function saveUsageDebounced() {
  clearTimeout(saveUsageTimer);
  saveUsageTimer = setTimeout(saveUsage, 800);
}
// --- Attention Scoring ---
function computeAttentionScore(key) {
  const u = usageData[key] || { frequency: 0, totalDuration: 0, lastAccess: 0 };
  const now = Date.now();
  const hoursSinceAccess = Math.max(0.01, (now - u.lastAccess) / 3600000);
  const recency = 1 / (1 + hoursSinceAccess);
  const freq = Math.log2(u.frequency + 1);
  const dur = Math.log2(u.totalDuration / 1000 + 1);
  return freq * dur * recency;
}
function rankPanels() {
  const keys = Object.keys(METRIC_SCHEMA);
  return keys.map(k => ({ key: k, score: computeAttentionScore(k) })).sort((a, b) => b.score - a.score);
}
// --- Rendering (memoized) ---
let lastSparkCache = {};
const panelEls = {};
let panelsRendered = false;
function getTrendClass(val) {
  if (val > 0.5) return 'up';
  if (val < -0.5) return 'down';
  return 'stable';
}
function getValueClass(key) {
  const s = METRIC_SCHEMA[key];
  const v = metricState[key]?.value || 0;
  if (v >= s.danger) return 'danger';
  if (v >= s.warn) return 'warn';
  return 'success';
}
function trendArrow(val) {
  if (val > 0.5) return '↑';
  if (val < -0.5) return '↓';
  return '→';
}
function drawSparkline(canvas, history, warn, danger) {
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.parentElement.getBoundingClientRect();
  const w = rect.width;
  const h = rect.height;
  if (w <= 0 || h <= 0) return;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, w, h);
  if (history.length < 2) return;
  const max = danger * 1.1;
  const min = 0;
  const range = max - min || 1;
  const stepX = w / (history.length - 1);
  const points = history.map((v, i) => ({ x: i * stepX, y: h - ((v - min) / range) * h }));
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, 'rgba(91,141,239,0.25)');
  grad.addColorStop(1, 'rgba(91,141,239,0.0)');
  ctx.beginPath();
  ctx.moveTo(points[0].x, h);
  for (const p of points) ctx.lineTo(p.x, p.y);
  ctx.lineTo(points[points.length - 1].x, h);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  for (let i = 1; i < points.length; i++) {
    const cp1x = (points[i].x + points[i-1].x) / 2;
    ctx.bezierCurveTo(cp1x, points[i-1].y, cp1x, points[i].y, points[i].x, points[i].y);
  }
  ctx.strokeStyle = '#5b8def';
  ctx.lineWidth = 1.6;
  ctx.stroke();
  const warnY = h - ((warn - min) / range) * h;
  ctx.setLineDash([4, 6]);
  ctx.strokeStyle = 'rgba(240,160,80,0.35)';
  ctx.lineWidth = 0.8;
  ctx.beginPath(); ctx.moveTo(0, warnY); ctx.lineTo(w, warnY); ctx.stroke();
  ctx.setLineDash([]);
}
function createPanelHTML(key, rankIdx) {
  const s = METRIC_SCHEMA[key];
  const ms = metricState[key];
  const val = ms?.value || 0;
  const trend = ms?.trend || 0;
  const ov = layoutOverrides[key] || {};
  const locked = ov.locked || false;
  const rankClass = rankIdx < 2 ? 'high-rank' : rankIdx < 5 ? 'mid-rank' : 'low-rank';
  const compact = ov.compact || false;
  const pinned = ov.pinned || false;
  return `<div class="panel ${rankClass}${compact ? ' compact' : ''}${locked ? ' locked' : ''}${pinned ? ' pinned' : ''}"
    data-key="${key}" data-rank="${rankIdx}"
    draggable="${locked ? 'false' : 'true'}">
    <span class="lock-indicator">🔒</span>
    <div class="panel-actions">
      <button class="btn-lock" data-key="${key}" title="Lock position">${locked ? '🔒' : '🔓'}</button>
      <button class="btn-compact" data-key="${key}" title="Toggle compact">${compact ? '⛶' : '⊟'}</button>
      <button class="btn-pin" data-key="${key}" title="Pin to top">${pinned ? '📌' : '📍'}</button>
    </div>
    <div class="panel-title">${s.name}</div>
    <div class="panel-value ${getValueClass(key)}">${val.toFixed(1)}<span style="font-size:0.6em;opacity:0.7">${s.unit}</span></div>
    <div class="trend ${getTrendClass(trend)}">${trendArrow(trend)} ${trend > 0 ? '+' : ''}${trend.toFixed(2)}${s.unit}</div>
    <div class="panel-body"><canvas></canvas></div>
  </div>`;
}
function buildDashboard() {
  const container = document.getElementById('dashboard');
  const ranked = rankPanels();
  const pinnedKeys = Object.keys(layoutOverrides).filter(k => layoutOverrides[k]?.pinned);
  const ordered = [...new Set([...pinnedKeys, ...ranked.map(r => r.key)])];
  const fragment = document.createDocumentFragment();
  ordered.forEach((key, i) => {
    const div = document.createElement('div');
    div.innerHTML = createPanelHTML(key, i);
    fragment.appendChild(div.firstElementChild);
  });
  container.innerHTML = '';
  container.appendChild(fragment);
  cachePanelRefs();
  panelsRendered = true;
  lastSparkCache = {};
  requestAnimationFrame(() => drawAllSparklines());
  attachPanelListeners();
}
function cachePanelRefs() {
  document.querySelectorAll('.panel').forEach(el => { panelEls[el.dataset.key] = el; });
}
function drawAllSparklines() {
  for (const [key, el] of Object.entries(panelEls)) {
    const canvas = el?.querySelector('canvas');
    if (!canvas) continue;
    const s = METRIC_SCHEMA[key];
    const cacheKey = key + ':' + s.history.length + ':' + s.history[s.history.length-1];
    if (lastSparkCache[key] === cacheKey) continue;
    lastSparkCache[key] = cacheKey;
    drawSparkline(canvas, s.history, s.warn, s.danger);
  }
}
function updatePanelValues() {
  if (!panelsRendered) return;
  for (const [key, el] of Object.entries(panelEls)) {
    if (!el) continue;
    const ms = metricState[key];
    if (!ms) continue;
    const valEl = el.querySelector('.panel-value');
    const trendEl = el.querySelector('.trend');
    const s = METRIC_SCHEMA[key];
    if (valEl) {
      valEl.className = 'panel-value ' + getValueClass(key);
      valEl.innerHTML = `${ms.value.toFixed(1)}<span style="font-size:0.6em;opacity:0.7">${s.unit}</span>`;
    }
    if (trendEl) {
      trendEl.className = 'trend ' + getTrendClass(ms.trend);
      trendEl.textContent = `${trendArrow(ms.trend)} ${ms.trend > 0 ? '+' : ''}${ms.trend.toFixed(2)}${s.unit}`;
    }
  }
  requestAnimationFrame(() => drawAllSparklines());
}
// --- Interaction & Tracking ---
let interactionTimer = null;
const INTERACTION_DEBOUNCE = 2000;
function attachPanelListeners() {
  document.querySelectorAll('.panel').forEach(panel => {
    panel.addEventListener('mouseenter', () => trackViewStart(panel.dataset.key));
    panel.addEventListener('mouseleave', () => trackViewEnd(panel.dataset.key));
    panel.addEventListener('focusin', () => trackViewStart(panel.dataset.key));
    panel.addEventListener('focusout', () => trackViewEnd(panel.dataset.key));
    panel.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      trackViewEnd(panel.dataset.key);
      trackViewStart(panel.dataset.key);
    });
    // Touch tracking
    panel.addEventListener('touchstart', () => trackViewStart(panel.dataset.key), { passive: true });
    panel.addEventListener('touchend', () => trackViewEnd(panel.dataset.key));
  });
  // Action buttons
  document.querySelectorAll('.btn-lock').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const key = btn.dataset.key;
      if (!layoutOverrides[key]) layoutOverrides[key] = {};
      layoutOverrides[key].locked = !layoutOverrides[key].locked;
      saveLayout();
      rebuildAfterOverride();
    });
  });
  document.querySelectorAll('.btn-compact').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const key = btn.dataset.key;
      if (!layoutOverrides[key]) layoutOverrides[key] = {};
      layoutOverrides[key].compact = !layoutOverrides[key].compact;
      saveLayout();
      rebuildAfterOverride();
    });
  });
  document.querySelectorAll('.btn-pin').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const key = btn.dataset.key;
      if (!layoutOverrides[key]) layoutOverrides[key] = {};
      layoutOverrides[key].pinned = !layoutOverrides[key].pinned;
      saveLayout();
      rebuildAfterOverride();
    });
  });
}
function rebuildAfterOverride() {
  clearTimeout(interactionTimer);
  interactionTimer = setTimeout(() => {
    buildDashboard();
  }, INTERACTION_DEBOUNCE);
}
// --- Drag & Drop (mouse + touch) ---
let dragState = null;
function initDragDrop() {
  const container = document.getElementById('dashboard');
  function getPanelEl(target) { return target?.closest('.panel'); }
  function onDragStart(e) {
    const panel = getPanelEl(e.target);
    if (!panel || panel.classList.contains('locked')) return;
    if (layoutOverrides[panel.dataset.key]?.locked) return;
    const rect = panel.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    dragState = { el: panel, key: panel.dataset.key, startX: clientX, startY: clientY,
      origRect: rect, offsetX: clientX - rect.left, offsetY: clientY - rect.top };
    panel.classList.add('dragging');
    panel.style.position = 'fixed';
    panel.style.left = rect.left + 'px';
    panel.style.top = rect.top + 'px';
    panel.style.width = rect.width + 'px';
    panel.style.zIndex = '100';
    e.preventDefault();
  }
  function onDragMove(e) {
    if (!dragState) return;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    dragState.el.style.left = (clientX - dragState.offsetX) + 'px';
    dragState.el.style.top = (clientY - dragState.offsetY) + 'px';
    const below = document.elementFromPoint(clientX, clientY);
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('drag-over'));
    const targetPanel = getPanelEl(below);
    if (targetPanel && targetPanel !== dragState.el) {
      targetPanel.classList.add('drag-over');
    }
  }
  function onDragEnd(e) {
    if (!dragState) return;
    const clientX = e.changedTouches ? e.changedTouches[0].clientX : e.clientX;
    const clientY = e.changedTouches ? e.changedTouches[0].clientY : e.clientY;
    const below = document.elementFromPoint(clientX, clientY);
    const targetPanel = getPanelEl(below);
    dragState.el.classList.remove('dragging');
    dragState.el.style.position = '';
    dragState.el.style.left = '';
    dragState.el.style.top = '';
    dragState.el.style.width = '';
    dragState.el.style.zIndex = '';
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('drag-over'));
    if (targetPanel && targetPanel !== dragState.el) {
      const targetKey = targetPanel.dataset.key;
      const srcKey = dragState.key;
      if (!layoutOverrides[srcKey]) layoutOverrides[srcKey] = {};
      if (!layoutOverrides[targetKey]) layoutOverrides[targetKey] = {};
      layoutOverrides[srcKey].pinned = true;
      layoutOverrides[targetKey].pinned = true;
      layoutOverrides[srcKey].swapWith = targetKey;
      layoutOverrides[targetKey].swapWith = srcKey;
      saveLayout();
      rebuildAfterOverride();
    }
    dragState = null;
  }
  container.addEventListener('mousedown', onDragStart);
  container.addEventListener('touchstart', onDragStart, { passive: false });
  document.addEventListener('mousemove', onDragMove);
  document.addEventListener('touchmove', onDragMove, { passive: false });
  document.addEventListener('mouseup', onDragEnd);
  document.addEventListener('touchend', onDragEnd);
}
// --- Auto-refresh ---
let pollTimer = null;
function setPollInterval(ms) {
  clearInterval(pollTimer);
  if (ms > 0) {
    pollTimer = setInterval(() => {
      simulateTick();
      updatePanelValues();
    }, ms);
  }
  const dot = document.getElementById('refreshDot');
  const label = document.getElementById('refreshLabel');
  if (ms > 0) {
    dot.className = 'refresh-dot';
    label.textContent = (ms / 1000) + 's';
  } else {
    dot.className = 'refresh-dot off';
    label.textContent = 'off';
  }
}
// --- Periodic layout recalculation ---
let layoutRecalcTimer = null;
function scheduleLayoutRecalc() {
  clearTimeout(layoutRecalcTimer);
  layoutRecalcTimer = setTimeout(() => {
    if (!document.querySelector('.panel.locked') && !Object.values(layoutOverrides).some(o => o.pinned && o.locked)) {
      buildDashboard();
    }
    scheduleLayoutRecalc();
  }, 30000);
}
// --- Init ---
document.getElementById('pollInterval').addEventListener('change', (e) => {
  setPollInterval(parseInt(e.target.value));
});
document.getElementById('btnReset').addEventListener('click', () => {
  localStorage.removeItem(TRACKING_KEY);
  localStorage.removeItem(LAYOUT_KEY);
  usageData = {};
  layoutOverrides = {};
  Object.keys(METRIC_SCHEMA).forEach(seedHistory);
  buildDashboard();
  const banner = document.createElement('div');
  banner.className = 'reset-banner';
  banner.textContent = 'Layout & tracking reset';
  document.body.appendChild(banner);
  setTimeout(() => banner.remove(), 2200);
});
document.getElementById('btnCompactAll').addEventListener('click', function() {
  const anyNotCompact = Object.values(layoutOverrides).some(o => !o.compact);
  Object.keys(METRIC_SCHEMA).forEach(k => {
    if (!layoutOverrides[k]) layoutOverrides[k] = {};
    layoutOverrides[k].compact = anyNotCompact;
  });
  saveLayout();
  buildDashboard();
  this.textContent = anyNotCompact ? 'Expand' : 'Compact';
});
buildDashboard();
initDragDrop();
setPollInterval(15000);
scheduleLayoutRecalc();
// Periodic adaptive re-rank (every 60s if no manual overrides)
setInterval(() => {
  const hasManual = Object.values(layoutOverrides).some(o => o.locked || o.compact);
  if (!hasManual) buildDashboard();
}, 60000);
// Visibility API: track view when tab hidden/shown
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    Object.keys(panelEls).forEach(k => trackViewEnd(k));
  } else {
    Object.keys(panelEls).forEach(k => trackViewStart(k));
  }
});
</script>
</body>
</html>