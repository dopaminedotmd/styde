<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --grid-gap: 12px;
  --panel-min-w: 280px;
  --panel-border-radius: 6px;
  --compact-scale: 0.4;
  --rank-decay-days: 7;
  --tracking-interval-ms: 2000;
  --bg: #f4f5f7;
  --panel-bg: #ffffff;
  --panel-border: #dfe1e6;
  --text: #172b4d;
  --text-subtle: #6b778c;
  --accent: #0052cc;
  --accent-light: #deebff;
  --compact-bg: #fafbfc;
  --lock-color: #ff8b00;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.4;
  min-height: 100vh;
}
.skip-link {
  position: absolute; top: -100px; left: 8px;
  background: var(--accent); color: #fff; padding: 8px 16px;
  z-index: 1000; border-radius: 0 0 4px 4px;
}
.skip-link:focus { top: 0; }
.toolbar {
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  padding: 12px 16px; background: var(--panel-bg);
  border-bottom: 1px solid var(--panel-border);
  position: sticky; top: 0; z-index: 100;
}
.toolbar h1 { font-size: 1.1rem; font-weight: 600; margin-right: auto; }
.toolbar button, .toolbar select {
  padding: 6px 14px; border: 1px solid var(--panel-border);
  border-radius: 4px; background: var(--panel-bg); cursor: pointer;
  font-size: 0.85rem; color: var(--text);
}
.toolbar button:hover, .toolbar select:hover { background: var(--accent-light); }
.toolbar button:focus-visible, .toolbar select:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px;
}
.toolbar button[aria-pressed="true"] {
  background: var(--accent); color: #fff; border-color: var(--accent);
}
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--panel-min-w), 1fr));
  grid-auto-rows: minmax(200px, auto);
  gap: var(--grid-gap);
  padding: 16px;
  align-content: start;
}
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: var(--panel-border-radius);
  overflow: hidden;
  transition: grid-column 0.3s ease, grid-row 0.3s ease;
  display: flex; flex-direction: column;
  position: relative;
  contain: layout style;
}
.panel.rank-1 { grid-column: span 2; grid-row: span 2; }
.panel.rank-2 { grid-column: span 2; }
.panel.rank-3 { grid-column: span 1; grid-row: span 1; }
.panel.compact {
  grid-column: span 1;
  grid-row: span 1;
  max-height: 120px;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.locked { border-color: var(--lock-color); box-shadow: 0 0 0 1px var(--lock-color); }
.panel-header {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px; border-bottom: 1px solid var(--panel-border);
  background: var(--panel-bg); cursor: grab;
  user-select: none;
}
.panel-header:focus-visible {
  outline: 2px solid var(--accent); outline-offset: -2px;
}
.panel-header h3 {
  font-size: 0.9rem; font-weight: 600; flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.panel-score {
  font-size: 0.7rem; color: var(--text-subtle);
  background: var(--accent-light); padding: 2px 8px;
  border-radius: 10px; white-space: nowrap;
}
.panel-controls { display: flex; gap: 4px; }
.panel-controls button {
  background: none; border: none; cursor: pointer;
  padding: 4px 6px; border-radius: 3px; font-size: 0.8rem;
  color: var(--text-subtle);
}
.panel-controls button:hover { background: var(--accent-light); color: var(--text); }
.panel-controls button:focus-visible { outline: 2px solid var(--accent); }
.panel-controls button[aria-pressed="true"] { color: var(--lock-color); font-weight: 700; }
.panel-body {
  padding: 12px; flex: 1; overflow: auto;
  display: flex; flex-direction: column; gap: 8px;
}
.panel-preview { display: none; padding: 8px 12px; font-size: 0.8rem; color: var(--text-subtle); }
.metric-value { font-size: 2rem; font-weight: 700; color: var(--accent); }
.metric-label { font-size: 0.8rem; color: var(--text-subtle); }
.metric-change { font-size: 0.8rem; }
.metric-change.up { color: #00875a; }
.metric-change.down { color: #de350b; }
.chart-placeholder {
  background: var(--accent-light); border-radius: 4px;
  height: 120px; display: flex; align-items: center; justify-content: center;
  color: var(--text-subtle); font-size: 0.85rem;
}
.data-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.data-table th, .data-table td {
  padding: 6px 8px; text-align: left; border-bottom: 1px solid var(--panel-border);
}
.data-table th { font-weight: 600; color: var(--text-subtle); }
.config-panel label {
  display: flex; align-items: center; gap: 8px; font-size: 0.85rem;
  padding: 4px 0;
}
.config-panel input[type="range"] { flex: 1; }
.config-panel input[type="number"] {
  width: 60px; padding: 4px; border: 1px solid var(--panel-border);
  border-radius: 4px; text-align: right;
}
[aria-live] { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
.empty-state {
  grid-column: 1 / -1; text-align: center; padding: 40px;
  color: var(--text-subtle);
}
@media (max-width: 768px) {
  .dashboard { grid-template-columns: 1fr; }
  .panel.rank-1, .panel.rank-2 { grid-column: span 1; }
  .toolbar { flex-direction: column; align-items: stretch; }
}
@media (max-width: 480px) {
  .toolbar h1 { font-size: 1rem; }
  .metric-value { font-size: 1.5rem; }
}
</style>
</head>
<body>
<a href="#dashboard-main" class="skip-link" role="navigation" aria-label="Skip to dashboard">Skip to dashboard</a>
<div class="toolbar" role="toolbar" aria-label="Dashboard controls">
  <h1>Adaptive Dashboard</h1>
  <button id="btn-reset" aria-label="Reset layout to default">Reset Layout</button>
  <button id="btn-export" aria-label="Export layout data">Export</button>
  <label style="display:flex;align-items:center;gap:4px;font-size:0.85rem;">
    Decay:
    <select id="cfg-decay" aria-label="Rank decay period in days">
      <option value="3">3 days</option>
      <option value="7" selected>7 days</option>
      <option value="14">14 days</option>
      <option value="30">30 days</option>
    </select>
  </label>
  <label style="display:flex;align-items:center;gap:4px;font-size:0.85rem;">
    Compact threshold:
    <select id="cfg-threshold" aria-label="Compact threshold percentile">
      <option value="0.1">Bottom 10%</option>
      <option value="0.2" selected>Bottom 20%</option>
      <option value="0.3">Bottom 30%</option>
    </select>
  </label>
</div>
<div id="aria-announcer" class="sr-only" aria-live="polite" aria-atomic="true"></div>
<main id="dashboard-main" class="dashboard" role="region" aria-label="Adaptive dashboard panels">
</main>
<script>
(function() {
'use strict';
const CONFIG = {
  decayDays: 7,
  compactThreshold: 0.2,
  trackingIntervalMs: 2000,
  maxPanels: 12,
  rankClasses: { 1: 'rank-1', 2: 'rank-2', 3: 'rank-3' }
};
const REAL_DATA = {
  revenue: { value: 284500, change: 12.4, unit: 'SEK', label: 'Monthly Revenue' },
  users: { value: 1842, change: 8.7, unit: '', label: 'Active Users' },
  conversion: { value: 3.24, change: -0.5, unit: '%', label: 'Conversion Rate' },
  latency: { value: 142, change: -15.2, unit: 'ms', label: 'Avg Latency' },
  errors: { value: 23, change: -42.5, unit: '', label: 'Error Count' },
  cpu: { value: 67, change: 3.1, unit: '%', label: 'CPU Usage' },
  memory: { value: 8.4, change: 0.3, unit: 'GB', label: 'Memory' },
  requests: { value: 12500, change: 22.1, unit: '/min', label: 'Requests' },
  satisfaction: { value: 4.7, change: 0.1, unit: '/5', label: 'CSAT Score' },
  uptime: { value: 99.97, change: 0.02, unit: '%', label: 'Uptime' },
  bandwidth: { value: 340, change: 5.2, unit: 'Mbps', label: 'Bandwidth' },
  queue: { value: 14, change: -8.3, unit: '', label: 'Queue Depth' }
};
const TABLE_DATA = [
  { name: 'Landing Page', views: 45200, bounce: 42, avgTime: '2:34' },
  { name: 'Pricing', views: 18200, bounce: 28, avgTime: '4:12' },
  { name: 'Docs', views: 12300, bounce: 35, avgTime: '8:45' },
  { name: 'Sign Up', views: 9800, bounce: 15, avgTime: '1:20' },
  { name: 'Dashboard', views: 8700, bounce: 8, avgTime: '12:30' }
];
const PANEL_DEFS = [
  { id: 'revenue', type: 'metric', dataKey: 'revenue', title: 'Revenue' },
  { id: 'users', type: 'metric', dataKey: 'users', title: 'Active Users' },
  { id: 'conversion', type: 'metric', dataKey: 'conversion', title: 'Conversion' },
  { id: 'latency', type: 'metric', dataKey: 'latency', title: 'Latency' },
  { id: 'errors', type: 'metric', dataKey: 'errors', title: 'Errors' },
  { id: 'cpu', type: 'metric', dataKey: 'cpu', title: 'CPU' },
  { id: 'memory', type: 'metric', dataKey: 'memory', title: 'Memory' },
  { id: 'requests', type: 'metric', dataKey: 'requests', title: 'Requests/min' },
  { id: 'satisfaction', type: 'metric', dataKey: 'satisfaction', title: 'CSAT' },
  { id: 'uptime', type: 'metric', dataKey: 'uptime', title: 'Uptime' },
  { id: 'bandwidth', type: 'metric', dataKey: 'bandwidth', title: 'Bandwidth' },
  { id: 'traffic-chart', type: 'chart', title: 'Traffic Trend' },
  { id: 'top-pages', type: 'table', title: 'Top Pages' },
  { id: 'config', type: 'config', title: 'Settings' }
];
let state = {
  panels: [],
  lockedPanels: {},
  manualOverrides: {},
  scores: {},
  tracking: {}
};
function loadState() {
  try {
    const raw = localStorage.getItem('adaptive-dashboard-state');
    if (raw) {
      const parsed = JSON.parse(raw);
      state.lockedPanels = parsed.lockedPanels || {};
      state.manualOverrides = parsed.manualOverrides || {};
      state.scores = parsed.scores || {};
      state.tracking = parsed.tracking || {};
    }
  } catch(e) {}
  CONFIG.decayDays = parseInt(localStorage.getItem('adaptive-dashboard-decay') || '7', 10);
  CONFIG.compactThreshold = parseFloat(localStorage.getItem('adaptive-dashboard-threshold') || '0.2');
}
function saveState() {
  try {
    localStorage.setItem('adaptive-dashboard-state', JSON.stringify({
      lockedPanels: state.lockedPanels,
      manualOverrides: state.manualOverrides,
      scores: state.scores,
      tracking: state.tracking
    }));
    localStorage.setItem('adaptive-dashboard-decay', CONFIG.decayDays.toString());
    localStorage.setItem('adaptive-dashboard-threshold', CONFIG.compactThreshold.toString());
  } catch(e) {}
}
function computeScore(panelId) {
  const t = state.tracking[panelId];
  if (!t) return 0;
  const now = Date.now();
  const decayFactor = Math.exp(-(now - t.lastInteraction) / (CONFIG.decayDays * 86400000));
  const frequency = t.interactionCount || 0;
  const totalDuration = t.totalViewDuration || 0;
  const recency = t.recentInteractions ? t.recentInteractions.reduce((s, ts) => s + Math.exp(-(now - ts) / (CONFIG.decayDays * 86400000)), 0) : 0;
  return (frequency * 0.3 + (totalDuration / 1000) * 0.3 + recency * 0.4) * decayFactor;
}
function trackInteraction(panelId, type) {
  const now = Date.now();
  if (!state.tracking[panelId]) {
    state.tracking[panelId] = {
      interactionCount: 0,
      totalViewDuration: 0,
      lastInteraction: now,
      recentInteractions: [],
      viewStart: null,
      collapseCount: 0,
      expandCount: 0
    };
  }
  const t = state.tracking[panelId];
  t.interactionCount++;
  t.lastInteraction = now;
  t.recentInteractions = (t.recentInteractions || []);
  t.recentInteractions.push(now);
  if (t.recentInteractions.length > 100) t.recentInteractions = t.recentInteractions.slice(-50);
  if (type === 'collapse') t.collapseCount = (t.collapseCount || 0) + 1;
  if (type === 'expand') t.expandCount = (t.expandCount || 0) + 1;
  state.scores[panelId] = computeScore(panelId);
}
function startViewTracking(panelId) {
  if (!state.tracking[panelId]) trackInteraction(panelId, 'view');
  state.tracking[panelId].viewStart = Date.now();
}
function endViewTracking(panelId) {
  const t = state.tracking[panelId];
  if (t && t.viewStart) {
    t.totalViewDuration = (t.totalViewDuration || 0) + (Date.now() - t.viewStart);
    t.viewStart = null;
    state.scores[panelId] = computeScore(panelId);
  }
}
function rankPanels() {
  const scored = PANEL_DEFS.map(def => ({
    id: def.id,
    score: state.scores[def.id] || 0,
    locked: !!state.lockedPanels[def.id],
    overrideRank: state.manualOverrides[def.id] ? state.manualOverrides[def.id].rank : null
  }));
  scored.sort((a, b) => b.score - a.score);
  let rank = 1;
  const threshold = Math.max(1, Math.floor(scored.length * CONFIG.compactThreshold));
  const compactIds = new Set(scored.slice(-threshold).filter(s => !s.locked).map(s => s.id));
  const ranks = {};
  const active = scored.filter(s => !compactIds.has(s.id) || s.locked);
  active.forEach((s, i) => {
    const r = s.overrideRank || (i < 2 ? 1 : i < 5 ? 2 : 3);
    ranks[s.id] = r;
  });
  compactIds.forEach(id => {
    if (!ranks[id]) ranks[id] = 3;
  });
  return { ranks, compactIds, scored };
}
function renderMetricBody(panel) {
  const data = REAL_DATA[panel.dataKey];
  if (!data) return '<div class="chart-placeholder" role="img" aria-label="No data available">---</div>';
  const changeClass = data.change >= 0 ? 'up' : 'down';
  const changeSymbol = data.change >= 0 ? '+' : '';
  return [
    '<div class="metric-value" role="status" aria-label="' + data.label + ': ' + data.value + data.unit + '">' + data.value.toLocaleString() + '<span style="font-size:0.5em;font-weight:400;"> ' + data.unit + '</span></div>',
    '<div class="metric-change ' + changeClass + '" aria-label="Change: ' + changeSymbol + data.change + '%">' + changeSymbol + data.change + '% vs last period</div>',
    '<div class="metric-label">' + data.label + '</div>'
  ].join('');
}
function renderChartBody(panel) {
  const bars = [65, 72, 58, 81, 74, 90, 85, 78, 92, 88, 76, 95];
  const max = Math.max(...bars);
  const svgBars = bars.map((v, i) => {
    const h = (v / max) * 100;
    return '<rect x="' + (i * 24 + 4) + '" y="' + (100 - h) + '" width="18" height="' + h + '" fill="var(--accent)" rx="2" role="img" aria-label="Hour ' + i + ': ' + v + ' requests"/>';
  }).join('');
  return [
    '<div class="chart-placeholder">',
    '<svg width="100%" height="100%" viewBox="0 0 300 120" role="img" aria-label="Traffic trend chart: 12-hour request volume">',
    svgBars,
    '</svg>',
    '</div>',
    '<div class="metric-label">Requests per hour (last 12h)</div>'
  ].join('');
}
function renderTableBody(panel) {
  const rows = TABLE_DATA.map(r =>
    '<tr><td>' + r.name + '</td><td>' + r.views.toLocaleString() + '</td><td>' + r.bounce + '%</td><td>' + r.avgTime + '</td></tr>'
  ).join('');
  return [
    '<table class="data-table" role="table" aria-label="Top pages by traffic">',
    '<thead><tr><th scope="col">Page</th><th scope="col">Views</th><th scope="col">Bounce</th><th scope="col">Avg Time</th></tr></thead>',
    '<tbody>' + rows + '</tbody>',
    '</table>'
  ].join('');
}
function renderConfigBody(panel) {
  return [
    '<div class="config-panel" role="form" aria-label="Dashboard configuration">',
    '<label>Decay days <input type="number" id="cfg-decay-inline" value="' + CONFIG.decayDays + '" min="1" max="90" aria-label="Rank decay days"></label>',
    '<label>Compact threshold <input type="range" id="cfg-threshold-inline" min="0.05" max="0.5" step="0.05" value="' + CONFIG.compactThreshold + '" aria-label="Compact threshold"><span id="threshold-val">' + Math.round(CONFIG.compactThreshold * 100) + '%</span></label>',
    '<label>Tracking interval <input type="number" id="cfg-interval" value="' + (CONFIG.trackingIntervalMs / 1000) + '" min="1" max="30" aria-label="Tracking interval in seconds">s</label>',
    '</div>'
  ].join('');
}
function renderPanelHTML(panel, rank, isCompact) {
  const def = PANEL_DEFS.find(d => d.id === panel.id);
  if (!def) return '';
  const rankClass = CONFIG.rankClasses[rank] || '';
  const compactClass = isCompact ? ' compact' : '';
  const lockedClass = panel.locked ? ' locked' : '';
  const score = state.scores[panel.id] || 0;
  let bodyHTML = '';
  if (def.type === 'metric') bodyHTML = renderMetricBody(def);
  else if (def.type === 'chart') bodyHTML = renderChartBody(def);
  else if (def.type === 'table') bodyHTML = renderTableBody(def);
  else if (def.type === 'config') bodyHTML = renderConfigBody(def);
  const previewHTML = def.type === 'metric' && REAL_DATA[def.dataKey]
    ? REAL_DATA[def.dataKey].value.toLocaleString() + REAL_DATA[def.dataKey].unit + ' (' + (REAL_DATA[def.dataKey].change >= 0 ? '+' : '') + REAL_DATA[def.dataKey].change + '%)'
    : (def.type === 'table' ? TABLE_DATA.length + ' pages tracked' : 'Click to expand');
  return [
    '<div class="panel ' + rankClass + compactClass + lockedClass + '"',
    ' data-panel-id="' + panel.id + '"',
    ' role="region" aria-label="' + def.title + ' panel"',
    ' tabindex="0"',
    '>',
    '<div class="panel-header" role="button" aria-expanded="' + (!isCompact) + '" aria-label="' + def.title + ' - ' + (isCompact ? 'collapsed' : 'expanded') + '">',
    '<h3>' + def.title + '</h3>',
    '<span class="panel-score" aria-label="Attention score: ' + Math.round(score) + '">' + Math.round(score) + '</span>',
    '<div class="panel-controls">',
    '<button class="btn-compact" aria-label="' + (isCompact ? 'Expand' : 'Compact') + ' ' + def.title + '" aria-pressed="' + isCompact + '">' + (isCompact ? '&#x26F6;' : '&#x2013;') + '</button>',
    '<button class="btn-lock" aria-label="' + (panel.locked ? 'Unlock' : 'Lock') + ' ' + def.title + '" aria-pressed="' + panel.locked + '">' + (panel.locked ? '&#x1F512;' : '&#x1F513;') + '</button>',
    '</div>',
    '</div>',
    '<div class="panel-body">' + bodyHTML + '</div>',
    '<div class="panel-preview">' + previewHTML + '</div>',
    '</div>'
  ].join('');
}
function patchPanel(container, panelId, newHTML) {
  const existing = container.querySelector('[data-panel-id="' + panelId + '"]');
  if (!existing) {
    const temp = document.createElement('div');
    temp.innerHTML = newHTML;
    const el = temp.firstElementChild;
    if (el) container.appendChild(el);
    return;
  }
  const existingHTML = existing.outerHTML;
  if (existingHTML === newHTML) return;
  const temp = document.createElement('div');
  temp.innerHTML = newHTML;
  const newEl = temp.firstElementChild;
  if (!newEl) { existing.remove(); return; }
  patchElement(existing, newEl);
}
function patchElement(oldEl, newEl) {
  if (oldEl.tagName !== newEl.tagName) {
    oldEl.replaceWith(newEl);
    return;
  }
  const oldAttrs = {};
  for (const a of oldEl.attributes) oldAttrs[a.name] = a.value;
  const newAttrs = {};
  for (const a of newEl.attributes) newAttrs[a.name] = a.value;
  for (const name in oldAttrs) {
    if (!(name in newAttrs)) oldEl.removeAttribute(name);
  }
  for (const name in newAttrs) {
    if (oldAttrs[name] !== newAttrs[name]) oldEl.setAttribute(name, newAttrs[name]);
  }
  const oldKids = Array.from(oldEl.childNodes);
  const newKids = Array.from(newEl.childNodes);
  const minLen = Math.min(oldKids.length, newKids.length);
  for (let i = 0; i < minLen; i++) {
    if (oldKids[i].nodeType === 3 && newKids[i].nodeType === 3) {
      if (oldKids[i].textContent !== newKids[i].textContent) oldKids[i].textContent = newKids[i].textContent;
    } else if (oldKids[i].nodeType === 1 && newKids[i].nodeType === 1) {
      patchElement(oldKids[i], newKids[i]);
    } else {
      oldKids[i].replaceWith(newKids[i].cloneNode(true));
    }
  }
  while (oldKids.length > minLen) oldEl.removeChild(oldEl.lastChild);
  while (newKids.length > minLen) oldEl.appendChild(newKids[minLen + (oldKids.length - minLen)] ? newKids[minLen + (oldKids.length - minLen)].cloneNode(true) : newKids[newKids.length - 1].cloneNode(true));
}
function render() {
  const container = document.getElementById('dashboard-main');
  if (!container) return;
  const { ranks, compactIds, scored } = rankPanels();
  const orderedIds = scored.map(s => s.id);
  const currentIds = Array.from(container.querySelectorAll('[data-panel-id]')).map(el => el.dataset.panelId);
  const toRemove = currentIds.filter(id => !orderedIds.includes(id));
  toRemove.forEach(id => {
    const el = container.querySelector('[data-panel-id="' + id + '"]');
    if (el) el.remove();
  });
  orderedIds.forEach(panelId => {
    const isCompact = compactIds.has(panelId) && !state.lockedPanels[panelId];
    const rank = ranks[panelId] || 3;
    const locked = !!state.lockedPanels[panelId];
    const panel = { id: panelId, locked, rank, compact: isCompact };
    const newHTML = renderPanelHTML(panel, rank, isCompact);
    patchPanel(container, panelId, newHTML);
  });
  rebindEvents();
}
function rebindEvents() {
  const container = document.getElementById('dashboard-main');
  if (!container) return;
  container.querySelectorAll('.panel').forEach(panel => {
    const id = panel.dataset.panelId;
    panel.addEventListener('mouseenter', () => startViewTracking(id));
    panel.addEventListener('mouseleave', () => endViewTracking(id));
    panel.addEventListener('focusin', () => { trackInteraction(id, 'focus'); startViewTracking(id); });
    panel.addEventListener('focusout', () => endViewTracking(id));
    panel.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        panel.focus();
        trackInteraction(id, 'keyboard');
      }
    });
  });
  container.querySelectorAll('.btn-compact').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panel = btn.closest('.panel');
      if (!panel) return;
      const id = panel.dataset.panelId;
      const currentlyCompact = panel.classList.contains('compact');
      if (currentlyCompact) {
        state.lockedPanels[id] = undefined;
        delete state.lockedPanels[id];
        trackInteraction(id, 'expand');
      } else {
        state.lockedPanels[id] = true;
        trackInteraction(id, 'collapse');
      }
      saveState();
      render();
      announce('Panel ' + (currentlyCompact ? 'expanded' : 'compacted'));
    });
  });
  container.querySelectorAll('.btn-lock').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panel = btn.closest('.panel');
      if (!panel) return;
      const id = panel.dataset.panelId;
      const currentlyLocked = panel.classList.contains('locked');
      if (currentlyLocked) {
        state.lockedPanels[id] = undefined;
        delete state.lockedPanels[id];
      } else {
        state.lockedPanels[id] = true;
      }
      saveState();
      render();
      announce('Panel ' + (currentlyLocked ? 'unlocked' : 'locked'));
    });
  });
  const cfgDecay = document.getElementById('cfg-decay-inline');
  if (cfgDecay && !cfgDecay._bound) {
    cfgDecay._bound = true;
    cfgDecay.addEventListener('change', () => {
      CONFIG.decayDays = parseInt(cfgDecay.value, 10) || 7;
      document.getElementById('cfg-decay').value = CONFIG.decayDays.toString();
      Object.keys(state.tracking).forEach(id => { state.scores[id] = computeScore(id); });
      saveState();
      render();
    });
  }
  const cfgThreshold = document.getElementById('cfg-threshold-inline');
  if (cfgThreshold && !cfgThreshold._bound) {
    cfgThreshold._bound = true;
    cfgThreshold.addEventListener('input', () => {
      CONFIG.compactThreshold = parseFloat(cfgThreshold.value);
      document.getElementById('threshold-val').textContent = Math.round(CONFIG.compactThreshold * 100) + '%';
      document.getElementById('cfg-threshold').value = CONFIG.compactThreshold.toString();
    });
    cfgThreshold.addEventListener('change', () => {
      CONFIG.compactThreshold = parseFloat(cfgThreshold.value);
      document.getElementById('cfg-threshold').value = CONFIG.compactThreshold.toString();
      saveState();
      render();
    });
  }
}
function announce(msg) {
  const el = document.getElementById('aria-announcer');
  if (el) { el.textContent = ''; setTimeout(() => { el.textContent = msg; }, 50); }
}
function initToolbar() {
  document.getElementById('btn-reset').addEventListener('click', () => {
    state.tracking = {};
    state.scores = {};
    state.lockedPanels = {};
    state.manualOverrides = {};
    saveState();
    render();
    announce('Layout reset to default');
  });
  document.getElementById('btn-export').addEventListener('click', () => {
    const data = {
      config: CONFIG,
      tracking: state.tracking,
      scores: state.scores,
      lockedPanels: state.lockedPanels,
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'dashboard-layout-' + new Date().toISOString().slice(0,10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
    announce('Layout exported');
  });
  document.getElementById('cfg-decay').addEventListener('change', e => {
    CONFIG.decayDays = parseInt(e.target.value, 10);
    Object.keys(state.tracking).forEach(id => { state.scores[id] = computeScore(id); });
    saveState();
    render();
  });
  document.getElementById('cfg-threshold').addEventListener('change', e => {
    CONFIG.compactThreshold = parseFloat(e.target.value);
    saveState();
    render();
  });
}
function startTrackingLoop() {
  setInterval(() => {
    Object.keys(state.tracking).forEach(id => {
      state.scores[id] = computeScore(id);
    });
    render();
    saveState();
  }, CONFIG.trackingIntervalMs);
}
function init() {
  if (!document.getElementById('dashboard-main')) return;
  loadState();
  state.panels = PANEL_DEFS.map(d => ({
    id: d.id,
    locked: !!state.lockedPanels[d.id],
    rank: state.manualOverrides[d.id] ? state.manualOverrides[d.id].rank : 3,
    compact: false
  }));
  Object.keys(state.tracking).forEach(id => {
    state.scores[id] = computeScore(id);
  });
  render();
  initToolbar();
  startTrackingLoop();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
})();
</script>
</body>
</html>