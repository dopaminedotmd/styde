<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22253a;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108, 140, 255, 0.3);
  --danger: #ff5c6c;
  --warning: #ffb84d;
  --success: #4ade80;
  --info: #38bdf8;
  --radius: 10px;
  --radius-sm: 6px;
  --gap: 12px;
  --transition-speed: 0ms;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
  line-height: 1.5;
}
body.animations-enabled { --transition-speed: 280ms; }
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  padding: 10px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 16px;
  font-size: 13px;
}
.toolbar-label { color: var(--text-dim); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; font-size: 11px; }
.toolbar button, .toolbar select {
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 6px 14px;
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
  transition: background 150ms;
}
.toolbar button:hover, .toolbar select:hover { background: var(--surface-hover); }
.toolbar button:focus-visible, .toolbar select:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.toolbar button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 180px;
  gap: var(--gap);
}
@media (max-width: 1200px) { .dashboard { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .dashboard { grid-template-columns: 1fr; grid-auto-rows: 160px; } }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: grid-column var(--transition-speed) ease, grid-row var(--transition-speed) ease,
              transform var(--transition-speed) ease, opacity var(--transition-speed) ease;
  cursor: pointer;
}
.panel:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.panel:hover { border-color: var(--accent); background: var(--surface-hover); }
.panel.locked { border-left: 3px solid var(--warning); }
.panel.compact { grid-row: span 1; font-size: 12px; padding: 10px 12px; }
.panel.compact .panel-value { font-size: 20px; }
.panel.compact .panel-chart { height: 30px; }
.panel.compact .panel-footer { display: none; }
.panel.compact .panel-title { font-size: 11px; }
.panel.hidden-panel { display: none; }
.panel-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }
.panel-title { font-size: 13px; font-weight: 600; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.03em; }
.panel-actions { display: flex; gap: 4px; opacity: 0; transition: opacity 150ms; }
.panel:hover .panel-actions, .panel:focus-within .panel-actions { opacity: 1; }
.pin-btn, .expand-btn {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 14px;
  line-height: 1;
}
.pin-btn:hover, .expand-btn:hover { color: var(--text); background: var(--bg); }
.pin-btn:focus-visible, .expand-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
.pin-btn.pinned { color: var(--warning); }
.panel-value { font-size: 28px; font-weight: 700; margin: 4px 0; font-variant-numeric: tabular-nums; }
.panel-value.trend-up { color: var(--success); }
.panel-value.trend-down { color: var(--danger); }
.panel-value.trend-warn { color: var(--warning); }
.panel-chart {
  flex: 1;
  min-height: 36px;
  margin: 4px 0;
  position: relative;
}
.panel-chart svg { width: 100%; height: 100%; }
.panel-footer {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-dim);
  margin-top: auto;
  padding-top: 6px;
  border-top: 1px solid var(--border);
}
.panel-footer .delta { font-weight: 600; }
.panel-footer .delta.positive { color: var(--success); }
.panel-footer .delta.negative { color: var(--danger); }
.more-section {
  margin-top: 16px;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
}
.more-toggle {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
  padding: 4px 0;
}
.more-toggle:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.more-panels { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.more-panels .mini-panel {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  min-width: 140px;
  cursor: pointer;
  font-size: 12px;
}
.more-panels .mini-panel:hover { border-color: var(--accent); }
.more-panels .mini-panel .mp-title { color: var(--text-dim); font-size: 10px; text-transform: uppercase; }
.more-panels .mini-panel .mp-value { font-size: 16px; font-weight: 600; }
.score-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 9px;
  color: var(--text-dim);
  background: var(--bg);
  padding: 1px 5px;
  border-radius: 3px;
  opacity: 0;
  transition: opacity 150ms;
}
.panel:hover .score-badge { opacity: 1; }
.sparkline { fill: none; stroke-width: 1.5; vector-effect: non-scrolling-stroke; }
.sparkline-area { opacity: 0.15; }
</style>
</head>
<body>
<div class="toolbar" role="toolbar" aria-label="Dashboard controls">
  <span class="toolbar-label">Dashboard</span>
  <button id="btn-reset-layout" aria-label="Reset layout to default">Reset Layout</button>
  <button id="btn-toggle-animations" aria-label="Toggle animations">Animations: Off</button>
  <select id="sel-sort-mode" aria-label="Sort mode">
    <option value="adaptive">Sort: Adaptive</option>
    <option value="manual">Sort: Manual Only</option>
    <option value="name">Sort: By Name</option>
  </select>
  <select id="sel-compact-threshold" aria-label="Compact threshold">
    <option value="3">Compact bottom 3</option>
    <option value="5" selected>Compact bottom 5</option>
    <option value="8">Compact bottom 8</option>
    <option value="0">No compacting</option>
  </select>
  <span id="tracking-status" style="margin-left:auto;font-size:11px;color:var(--text-dim)">Tracking: active</span>
</div>
<div class="dashboard" id="dashboard" role="region" aria-label="Adaptive dashboard grid">
</div>
<div class="more-section" id="more-section" style="display:none">
  <button class="more-toggle" id="more-toggle" aria-expanded="false" aria-controls="more-panels">
    Hidden panels (0)
  </button>
  <div class="more-panels" id="more-panels" role="list" aria-label="Hidden panels"></div>
</div>
<script>
'use strict';
const CONFIG = {
  decayRate: 0.92,
  recencyHalfLife: 3600000,
  viewThreshold: 500,
  rearrangeInterval: 15000,
  compactThreshold: 5,
  maxVisiblePanels: 10,
  animationMs: 0,
  animate: false,
  sortMode: 'adaptive',
  storageKey: 'adaptive_dashboard_v2',
  gridCols: 4,
  compactGridRow: 1,
  normalGridRowMin: 2,
};
const PANEL_DEFS = [
  { id: 'revenue', title: 'Revenue (24h)', unit: '$', format: 'currency', trend: 'up', base: 284500, variance: 0.06, dataPoints: 24, color: '#4ade80' },
  { id: 'users', title: 'Active Users', unit: '', format: 'number', trend: 'up', base: 12430, variance: 0.08, dataPoints: 24, color: '#6c8cff' },
  { id: 'conversion', title: 'Conversion Rate', unit: '%', format: 'percent', trend: 'up', base: 3.42, variance: 0.15, dataPoints: 24, color: '#38bdf8' },
  { id: 'latency', title: 'P95 Latency', unit: 'ms', format: 'number', trend: 'down', base: 187, variance: 0.12, dataPoints: 24, color: '#ffb84d', invertGood: true },
  { id: 'errors', title: 'Error Rate', unit: '%', format: 'percent', trend: 'down', base: 0.23, variance: 0.3, dataPoints: 24, color: '#ff5c6c', invertGood: true },
  { id: 'throughput', title: 'Req/sec', unit: '', format: 'number', trend: 'up', base: 3420, variance: 0.1, dataPoints: 24, color: '#a78bfa' },
  { id: 'cpu', title: 'CPU Usage', unit: '%', format: 'percent', trend: 'neutral', base: 62, variance: 0.09, dataPoints: 24, color: '#f59e0b' },
  { id: 'memory', title: 'Memory', unit: 'GB', format: 'number', trend: 'neutral', base: 14.2, variance: 0.04, dataPoints: 24, color: '#8b5cf6' },
  { id: 'cache', title: 'Cache Hit Rate', unit: '%', format: 'percent', trend: 'up', base: 94.7, variance: 0.03, dataPoints: 24, color: '#10b981' },
  { id: 'storage', title: 'Storage', unit: 'TB', format: 'number', trend: 'up', base: 8.3, variance: 0.02, dataPoints: 24, color: '#ec4899' },
  { id: 'bandwidth', title: 'Bandwidth', unit: 'Gbps', format: 'number', trend: 'up', base: 2.8, variance: 0.11, dataPoints: 24, color: '#f97316' },
  { id: 'queries', title: 'DB Queries/sec', unit: '', format: 'number', trend: 'neutral', base: 1820, variance: 0.07, dataPoints: 24, color: '#06b6d4' },
];
function seededRandom(seed) {
  let s = seed;
  return function() { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
}
function generateDataPoints(base, variance, count, seed) {
  const rng = seededRandom(seed);
  const points = [];
  for (let i = 0; i < count; i++) {
    const v = base * (1 + (rng() - 0.5) * variance * 2);
    points.push(Math.max(0, Math.round(v * 100) / 100));
  }
  return points;
}
function generateSparklinePath(data, width, height, color) {
  if (data.length < 2) return '';
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const padding = 2;
  const w = width - padding * 2;
  const h = height - padding * 2;
  const xStep = w / (data.length - 1);
  let pathD = '';
  let areaD = '';
  for (let i = 0; i < data.length; i++) {
    const x = padding + i * xStep;
    const y = padding + h - ((data[i] - min) / range) * h;
    pathD += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
    if (i === 0) areaD += 'M' + x.toFixed(1) + ',' + (padding + h).toFixed(1) + ' L';
    areaD += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
    if (i === data.length - 1) areaD += 'L' + x.toFixed(1) + ',' + (padding + h).toFixed(1) + ' Z';
  }
  return { path: pathD.trim(), area: areaD.trim() };
}
let panelStates = {};
let usageData = {};
let lockedPanels = new Set();
let hiddenPanels = new Set();
let observers = {};
let rearrangeTimer = null;
let animationFrameId = null;
let panelOrder = [];
function initState() {
  PANEL_DEFS.forEach((def, i) => {
    const seed = (def.id.charCodeAt(0) || 1) * 100 + i + Date.now() % 10000;
    const data = generateDataPoints(def.base, def.variance, def.dataPoints, seed);
    panelStates[def.id] = {
      def: def,
      currentValue: data[data.length - 1],
      prevValue: data[data.length - 2] || data[data.length - 1],
      data: data,
      seed: seed,
      rank: 0,
      score: 0,
      order: i,
    };
  });
  panelOrder = PANEL_DEFS.map(d => d.id);
}
function initUsage() {
  PANEL_DEFS.forEach(def => {
    usageData[def.id] = {
      viewCount: 0,
      totalViewDuration: 0,
      lastViewed: 0,
      clickCount: 0,
      expandCount: 0,
      collapseCount: 0,
    };
  });
}
function loadState() {
  try {
    const raw = localStorage.getItem(CONFIG.storageKey);
    if (raw) {
      const saved = JSON.parse(raw);
      if (saved.usageData) usageData = saved.usageData;
      if (saved.lockedPanels) lockedPanels = new Set(saved.lockedPanels);
      if (saved.hiddenPanels) hiddenPanels = new Set(saved.hiddenPanels);
      if (saved.panelOrder) panelOrder = saved.panelOrder;
      if (saved.config) Object.assign(CONFIG, saved.config);
    }
  } catch (e) { /* ignore corrupt storage */ }
}
function saveState() {
  try {
    localStorage.setItem(CONFIG.storageKey, JSON.stringify({
      usageData,
      lockedPanels: [...lockedPanels],
      hiddenPanels: [...hiddenPanels],
      panelOrder,
      config: {
        decayRate: CONFIG.decayRate,
        recencyHalfLife: CONFIG.recencyHalfLife,
        compactThreshold: CONFIG.compactThreshold,
        sortMode: CONFIG.sortMode,
        animate: CONFIG.animate,
      },
      timestamp: Date.now(),
    }));
  } catch (e) { /* quota exceeded, silently fail */ }
}
let lastKnownPositions = new Map();
function updatePositions() {
  const dashboard = document.getElementById('dashboard');
  const panels = dashboard.querySelectorAll('.panel:not(.hidden-panel)');
  const newPositions = new Map();
  panels.forEach(p => {
    newPositions.set(p.dataset.pid, p.getBoundingClientRect());
  });
  if (CONFIG.animate && lastKnownPositions.size > 0) {
    panels.forEach(p => {
      const oldRect = lastKnownPositions.get(p.dataset.pid);
      const newRect = newPositions.get(p.dataset.pid);
      if (oldRect && newRect) {
        const dx = oldRect.left - newRect.left;
        const dy = oldRect.top - newRect.top;
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
          p.style.transform = `translate(${dx}px, ${dy}px)`;
          p.style.transition = 'none';
          requestAnimationFrame(() => {
            p.style.transition = `transform ${CONFIG.animationMs}ms ease`;
            p.style.transform = 'translate(0, 0)';
          });
        }
      }
    });
  }
  lastKnownPositions = newPositions;
}
function computeScores() {
  const now = Date.now();
  PANEL_DEFS.forEach(def => {
    const u = usageData[def.id];
    const hoursSinceLastView = Math.max(0, (now - u.lastViewed) / 3600000);
    const halfLifeHours = CONFIG.recencyHalfLife / 3600000;
    const recencyFactor = Math.pow(0.5, hoursSinceLastView / halfLifeHours);
    const avgDuration = u.viewCount > 0 ? u.totalViewDuration / u.viewCount : 0;
    const durationScore = Math.log1p(avgDuration);
    const freqScore = Math.log1p(u.viewCount);
    const clickScore = Math.log1p(u.clickCount * 3);
    const score = (freqScore * 0.4 + durationScore * 0.35 + clickScore * 0.15 + recencyFactor * 0.1) * 100;
    panelStates[def.id].score = Math.round(score * 10) / 10;
    panelStates[def.id].rank = 0;
  });
  const sorted = [...PANEL_DEFS].sort((a, b) => {
    if (lockedPanels.has(a.id) && !lockedPanels.has(b.id)) return -1;
    if (!lockedPanels.has(a.id) && lockedPanels.has(b.id)) return 1;
    const aScore = panelStates[a.id].score;
    const bScore = panelStates[b.id].score;
    if (Math.abs(aScore - bScore) < 0.5) {
      return (usageData[a.id].lastViewed || 0) - (usageData[b.id].lastViewed || 0);
    }
    return bScore - aScore;
  });
  sorted.forEach((def, i) => { panelStates[def.id].rank = i + 1; });
  if (CONFIG.sortMode === 'adaptive') {
    panelOrder = sorted.map(d => d.id);
  } else if (CONFIG.sortMode === 'name') {
    panelOrder = [...PANEL_DEFS].sort((a, b) => a.title.localeCompare(b.title)).map(d => d.id);
  }
  computeCompact();
}
function computeCompact() {
  const visible = panelOrder.filter(id => !hiddenPanels.has(id));
  const threshold = CONFIG.compactThreshold;
  for (let i = 0; i < visible.length; i++) {
    const id = visible[i];
    const isCompact = threshold > 0 && i >= visible.length - threshold && !lockedPanels.has(id);
    panelStates[id].compact = isCompact;
  }
}
function getGridPlacement(panelId) {
  const visible = panelOrder.filter(id => !hiddenPanels.has(id));
  const idx = visible.indexOf(panelId);
  if (idx === -1) return { hidden: true };
  const isCompact = panelStates[panelId] && panelStates[panelId].compact;
  const col = (idx % CONFIG.gridCols) + 1;
  const rowSpan = isCompact ? CONFIG.compactGridRow : CONFIG.normalGridRowMin;
  return { col, rowSpan, compact: isCompact, hidden: false };
}
function renderPanel(panelId) {
  const existing = document.querySelector(`.panel[data-pid="${panelId}"]`);
  const state = panelStates[panelId];
  const def = state.def;
  const placement = getGridPlacement(panelId);
  const usage = usageData[panelId];
  if (placement.hidden) {
    if (existing) existing.classList.add('hidden-panel');
    return;
  }
  const delta = state.currentValue - state.prevValue;
  const deltaPct = state.prevValue !== 0 ? (delta / Math.abs(state.prevValue)) * 100 : 0;
  const isGoodMetric = !def.invertGood;
  let trendClass = 'trend-up';
  if (def.invertGood) {
    trendClass = delta > 0 ? 'trend-down' : delta < 0 ? 'trend-up' : 'trend-warn';
  } else {
    trendClass = delta > 0 ? 'trend-up' : delta < 0 ? 'trend-down' : 'trend-warn';
  }
  let displayValue;
  if (def.format === 'currency') displayValue = '$' + state.currentValue.toLocaleString();
  else if (def.format === 'percent') displayValue = state.currentValue.toFixed(2) + '%';
  else displayValue = state.currentValue.toLocaleString();
  const sparkline = generateSparklinePath(state.data, 200, 50, def.color);
  const isLocked = lockedPanels.has(panelId);
  const isCompact = placement.compact;
  let footerHtml = '';
  if (!isCompact) {
    const deltaSign = delta >= 0 ? '+' : '';
    const deltaClass = (def.invertGood ? (delta < 0) : (delta > 0)) ? 'positive' : 'negative';
    footerHtml = `<div class="panel-footer">
      <span class="delta ${deltaClass}">${deltaSign}${deltaPct.toFixed(1)}%</span>
      <span>Rank #${state.rank || '-'}</span>
    </div>`;
  }
  const html = `
    <div class="panel${isCompact ? ' compact' : ''}${isLocked ? ' locked' : ''}"
         data-pid="${panelId}"
         tabindex="0"
         role="article"
         aria-label="${def.title}: ${displayValue}, rank ${state.rank || '-'}"
         style="grid-column: span 1; grid-row: span ${placement.rowSpan};">
      <div class="panel-header">
        <span class="panel-title">${def.title}</span>
        <div class="panel-actions">
          <button class="pin-btn${isLocked ? ' pinned' : ''}" data-action="toggle-lock" aria-label="${isLocked ? 'Unpin' : 'Pin'} ${def.title}" title="${isLocked ? 'Unpin panel' : 'Pin panel'}">${isLocked ? '&#128204;' : '&#128278;'}</button>
        </div>
      </div>
      <div class="panel-value ${trendClass}">${displayValue}</div>
      <div class="panel-chart">
        <svg viewBox="0 0 200 50" preserveAspectRatio="none" aria-hidden="true">
          <path class="sparkline-area" d="${sparkline.area}" fill="${def.color}"/>
          <path class="sparkline" d="${sparkline.path}" stroke="${def.color}"/>
        </svg>
      </div>
      ${footerHtml}
      <span class="score-badge" aria-label="Attention score">S:${state.score.toFixed(0)}</span>
    </div>`;
  if (existing) {
    if (existing.outerHTML.replace(/\s+/g, ' ') !== html.replace(/\s+/g, ' ')) {
      const temp = document.createElement('div');
      temp.innerHTML = html;
      const newEl = temp.firstChild;
      const oldRect = existing.getBoundingClientRect();
      existing.replaceWith(newEl);
      if (CONFIG.animate && oldRect.width > 0) {
        const newRect = newEl.getBoundingClientRect();
        const dx = oldRect.left - newRect.left;
        const dy = oldRect.top - newRect.top;
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
          newEl.style.transform = `translate(${dx}px, ${dy}px)`;
          newEl.style.transition = 'none';
          requestAnimationFrame(() => {
            newEl.style.transition = `transform ${CONFIG.animationMs}ms ease`;
            newEl.style.transform = 'translate(0, 0)';
          });
        }
      }
      attachPanelEvents(newEl);
      observePanel(newEl);
    } else {
      existing.style.gridRow = `span ${placement.rowSpan}`;
    }
  } else {
    const dashboard = document.getElementById('dashboard');
    const temp = document.createElement('div');
    temp.innerHTML = html;
    const el = temp.firstChild;
    el.style.gridRow = `span ${placement.rowSpan}`;
    dashboard.appendChild(el);
    attachPanelEvents(el);
    observePanel(el);
  }
}
function renderAll() {
  const dashboard = document.getElementById('dashboard');
  const existingIds = new Set();
  dashboard.querySelectorAll('.panel').forEach(p => existingIds.add(p.dataset.pid));
  panelOrder.forEach(id => {
    renderPanel(id);
    existingIds.delete(id);
  });
  existingIds.forEach(id => {
    const el = document.querySelector(`.panel[data-pid="${id}"]`);
    if (el) el.classList.add('hidden-panel');
  });
  updateMoreSection();
  saveState();
}
function updateMoreSection() {
  const section = document.getElementById('more-section');
  const container = document.getElementById('more-panels');
  const toggle = document.getElementById('more-toggle');
  const hidden = panelOrder.filter(id => hiddenPanels.has(id));
  if (hidden.length === 0) {
    section.style.display = 'none';
    return;
  }
  section.style.display = 'block';
  toggle.textContent = `Hidden panels (${hidden.length})`;
  container.innerHTML = hidden.map(id => {
    const state = panelStates[id];
    let dv = state.currentValue;
    if (state.def.format === 'currency') dv = '$' + dv.toLocaleString();
    else if (state.def.format === 'percent') dv = dv.toFixed(2) + '%';
    else dv = dv.toLocaleString();
    return `<div class="mini-panel" data-action="unhide" data-pid="${id}" tabindex="0" role="button" aria-label="Restore ${state.def.title}">
      <div class="mp-title">${state.def.title}</div>
      <div class="mp-value">${dv}</div>
    </div>`;
  }).join('');
}
function attachPanelEvents(el) {
  const pid = el.dataset.pid;
  el.addEventListener('click', (e) => {
    if (e.target.closest('[data-action]')) return;
    usageData[pid].clickCount = (usageData[pid].clickCount || 0) + 1;
    saveState();
  });
  el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (e.target.closest('[data-action="toggle-lock"]')) {
        toggleLock(pid);
      } else {
        usageData[pid].clickCount = (usageData[pid].clickCount || 0) + 1;
        saveState();
      }
    }
    if (e.key === 'h' && e.ctrlKey) {
      e.preventDefault();
      toggleHide(pid);
    }
  });
  el.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const action = btn.dataset.action;
      if (action === 'toggle-lock') toggleLock(pid);
      if (action === 'unhide') toggleHide(pid);
    });
  });
}
function observePanel(el) {
  const pid = el.dataset.pid;
  if (observers[pid]) {
    observers[pid].disconnect();
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.dataset.visibleSince = entry.target.dataset.visibleSince || String(Date.now());
      } else {
        const since = parseInt(entry.target.dataset.visibleSince || '0', 10);
        if (since > 0) {
          const duration = Date.now() - since;
          if (duration > CONFIG.viewThreshold) {
            usageData[pid].totalViewDuration = (usageData[pid].totalViewDuration || 0) + duration;
            usageData[pid].viewCount = (usageData[pid].viewCount || 0) + 1;
            usageData[pid].lastViewed = Date.now();
          }
          entry.target.dataset.visibleSince = '0';
        }
      }
    });
  }, { threshold: 0.6 });
  observer.observe(el);
  observers[pid] = observer;
}
function disconnectObserver(pid) {
  if (observers[pid]) {
    observers[pid].disconnect();
    delete observers[pid];
  }
}
function toggleLock(pid) {
  if (lockedPanels.has(pid)) {
    lockedPanels.delete(pid);
  } else {
    lockedPanels.add(pid);
  }
  computeScores();
  renderAll();
}
function toggleHide(pid) {
  if (hiddenPanels.has(pid)) {
    hiddenPanels.delete(pid);
    usageData[pid].expandCount = (usageData[pid].expandCount || 0) + 1;
  } else {
    hiddenPanels.add(pid);
    usageData[pid].collapseCount = (usageData[pid].collapseCount || 0) + 1;
    disconnectObserver(pid);
  }
  computeScores();
  renderAll();
  const el = document.querySelector(`.panel[data-pid="${pid}"]`);
  if (el && !hiddenPanels.has(pid)) observePanel(el);
}
function refreshData() {
  PANEL_DEFS.forEach(def => {
    const state = panelStates[def.id];
    state.seed = state.seed + 1;
    const newData = generateDataPoints(def.base, def.variance, def.dataPoints, state.seed);
    state.prevValue = state.currentValue;
    state.currentValue = newData[newData.length - 1];
    state.data = newData;
  });
}
function fullCycle() {
  refreshData();
  computeScores();
  renderAll();
}
function scheduleRearrangement() {
  if (rearrangeTimer) clearTimeout(rearrangeTimer);
  rearrangeTimer = setTimeout(() => {
    computeScores();
    fullCycle();
    scheduleRearrangement();
  }, CONFIG.rearrangeInterval);
}
function setupToolbar() {
  document.getElementById('btn-reset-layout').addEventListener('click', () => {
    if (confirm('Reset all layout data, usage tracking, and preferences?')) {
      localStorage.removeItem(CONFIG.storageKey);
      lockedPanels.clear();
      hiddenPanels.clear();
      initUsage();
      initState();
      panelOrder = PANEL_DEFS.map(d => d.id);
      computeScores();
      renderAll();
    }
  });
  const animBtn = document.getElementById('btn-toggle-animations');
  animBtn.addEventListener('click', () => {
    CONFIG.animate = !CONFIG.animate;
    CONFIG.animationMs = CONFIG.animate ? 280 : 0;
    document.body.classList.toggle('animations-enabled', CONFIG.animate);
    animBtn.textContent = `Animations: ${CONFIG.animate ? 'On' : 'Off'}`;
    saveState();
  });
  if (CONFIG.animate) {
    document.body.classList.add('animations-enabled');
    animBtn.textContent = 'Animations: On';
  }
  document.getElementById('sel-sort-mode').addEventListener('change', (e) => {
    CONFIG.sortMode = e.target.value;
    if (CONFIG.sortMode === 'manual') return;
    computeScores();
    fullCycle();
  });
  document.getElementById('sel-sort-mode').value = CONFIG.sortMode;
  document.getElementById('sel-compact-threshold').addEventListener('change', (e) => {
    CONFIG.compactThreshold = parseInt(e.target.value, 10);
    computeScores();
    fullCycle();
  });
  document.getElementById('sel-compact-threshold').value = String(CONFIG.compactThreshold);
  document.getElementById('more-toggle').addEventListener('click', () => {
    const container = document.getElementById('more-panels');
    const toggle = document.getElementById('more-toggle');
    const isHidden = container.style.display === 'none';
    container.style.display = isHidden ? 'flex' : 'none';
    toggle.setAttribute('aria-expanded', String(isHidden));
  });
  document.getElementById('more-panels').addEventListener('click', (e) => {
    const mini = e.target.closest('[data-pid]');
    if (mini) toggleHide(mini.dataset.pid);
  });
}
function init() {
  initState();
  initUsage();
  loadState();
  computeScores();
  setupToolbar();
  renderAll();
  scheduleRearrangement();
  setInterval(() => {
    refreshData();
    renderAll();
  }, 30000);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      Object.values(observers).forEach(o => o.disconnect());
    } else {
      document.querySelectorAll('.panel:not(.hidden-panel)').forEach(el => observePanel(el));
      computeScores();
      renderAll();
      scheduleRearrangement();
    }
  });
  window.addEventListener('beforeunload', () => {
    document.querySelectorAll('.panel[data-visible-since]').forEach(el => {
      const pid = el.dataset.pid;
      const since = parseInt(el.dataset.visibleSince || '0', 10);
      if (since > 0) {
        const duration = Date.now() - since;
        if (duration > CONFIG.viewThreshold) {
          usageData[pid].totalViewDuration = (usageData[pid].totalViewDuration || 0) + duration;
          usageData[pid].viewCount = (usageData[pid].viewCount || 0) + 1;
          usageData[pid].lastViewed = Date.now();
        }
      }
    });
    saveState();
  });
  console.log('Adaptive Dashboard initialized. Panels:', PANEL_DEFS.length,
    '| Sort:', CONFIG.sortMode, '| Compact threshold:', CONFIG.compactThreshold,
    '| Animate:', CONFIG.animate, '| Storage:', CONFIG.storageKey);
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>