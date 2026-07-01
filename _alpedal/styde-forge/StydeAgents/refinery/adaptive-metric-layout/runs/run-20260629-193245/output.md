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
  --border: #2a2e3d;
  --text: #e1e4ed;
  --text-muted: #7c829e;
  --accent: #6c8aff;
  --accent-glow: rgba(108,138,255,0.25);
  --danger: #ff5e7a;
  --warning: #ffb444;
  --success: #3dd68c;
  --scale: 1;
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
  padding: 16px;
}
.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 10px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.toolbar button {
  background: var(--surface-hover);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s;
}
.toolbar button:hover { background: #2a3050; }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.toolbar .spacer { flex: 1; }
.toolbar .status {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}
.toolbar .status .dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--success);
}
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 180px;
  gap: 12px;
  transition: grid-template-rows 0.4s ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, opacity 0.3s ease, grid-row 0.4s ease, grid-column 0.4s ease;
  -moz-transform: scale(var(--scale));
  transform: scale(var(--scale));
  cursor: default;
  display: flex;
  flex-direction: column;
}
.panel:hover {
  border-color: var(--accent);
  box-shadow: 0 0 20px var(--accent-glow);
  z-index: 2;
}
.panel.compact {
  grid-row: span 1 !important;
  min-height: 80px;
  max-height: 100px;
  -moz-transform: scale(0.92);
  transform: scale(0.92);
  opacity: 0.72;
  padding: 8px 14px;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-summary { display: flex; }
.panel .panel-summary { display: none; }
.panel.locked { border-color: var(--warning); }
.panel.locked::after {
  content: 'locked';
  position: absolute;
  top: 6px; right: 10px;
  font-size: 10px;
  color: var(--warning);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
}
.panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.2px;
}
.panel-score {
  font-size: 10px;
  color: var(--text-muted);
  background: var(--surface-hover);
  padding: 2px 7px;
  border-radius: 5px;
}
.panel-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
}
.panel-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1;
}
.panel-unit {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}
.panel-sparkline {
  margin-top: 6px;
  height: 36px;
  width: 100%;
}
.panel-sparkline svg { width: 100%; height: 100%; }
.panel-summary {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}
.panel-summary .mini-value {
  font-size: 18px;
  font-weight: 700;
}
.panel-summary .mini-spark {
  flex: 1;
  height: 30px;
}
.panel-summary .mini-label {
  font-size: 11px;
  color: var(--text-muted);
}
.panel-actions {
  position: absolute;
  bottom: 8px; right: 10px;
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.15s;
}
.panel:hover .panel-actions { opacity: 1; }
.panel-actions button {
  background: var(--surface-hover);
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 3px 8px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 11px;
}
.panel-actions button:hover { color: var(--text); border-color: var(--accent); }
.more-section {
  margin-top: 12px;
  padding: 10px 14px;
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  min-height: 50px;
}
.more-section-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.more-section .chip {
  font-size: 11px;
  background: var(--surface-hover);
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid var(--border);
}
.more-section .chip:hover { border-color: var(--accent); }
@media (max-width: 900px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) {
  .grid { grid-template-columns: 1fr; }
  .toolbar { flex-direction: column; align-items: stretch; }
}
</style>
</head>
<body>
<div class="toolbar">
  <button id="btnReset" title="Reset all attention scores and layout">Reset Learning</button>
  <button id="btnCompactAll" title="Compact all unlocked panels">Compact All</button>
  <button id="btnExpandAll" title="Expand all panels to full size">Expand All</button>
  <span class="spacer"></span>
  <span class="status">
    <span class="dot"></span>
    <span id="statusText">Tracking active</span>
    &mdash;
    <span id="trackedCount">0 panels</span>
  </span>
</div>
<div class="grid" id="grid"></div>
<div class="more-section" id="moreSection">
  <span class="more-section-label">More</span>
</div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v1';
const UPDATE_INTERVAL = 5000;
const DECAY_HALFLIFE_HOURS = 4;
const COMPACT_THRESHOLD_PERCENTILE = 30;
const MORE_THRESHOLD_PERCENTILE = 10;
const PANEL_CACHE = new Map();
const demoPanels = [
  { id: 'cpu', title: 'CPU Usage', value: 47, unit: '%', trend: 'up', sparkline: [30,35,42,38,45,52,47,44,48,47] },
  { id: 'mem', title: 'Memory', value: 62, unit: '%', trend: 'steady', sparkline: [58,60,59,61,63,62,64,62,61,62] },
  { id: 'disk', title: 'Disk I/O', value: 128, unit: 'MB/s', trend: 'down', sparkline: [150,145,140,135,130,128,132,129,127,128] },
  { id: 'net_in', title: 'Network In', value: 3.2, unit: 'Gbps', trend: 'up', sparkline: [2.1,2.5,2.8,3.0,2.9,3.1,3.3,3.0,3.2,3.2] },
  { id: 'net_out', title: 'Network Out', value: 1.8, unit: 'Gbps', trend: 'steady', sparkline: [1.5,1.6,1.7,1.8,1.7,1.9,1.8,1.7,1.8,1.8] },
  { id: 'req_rate', title: 'Request Rate', value: 942, unit: 'req/s', trend: 'up', sparkline: [800,850,820,880,900,910,930,920,940,942] },
  { id: 'err_rate', title: 'Error Rate', value: 0.12, unit: '%', trend: 'down', sparkline: [0.3,0.25,0.22,0.18,0.15,0.14,0.13,0.11,0.12,0.12] },
  { id: 'lat_p50', title: 'Latency p50', value: 12, unit: 'ms', trend: 'steady', sparkline: [11,12,13,12,11,12,12,13,12,12] },
  { id: 'lat_p99', title: 'Latency p99', value: 87, unit: 'ms', trend: 'up', sparkline: [70,72,75,78,80,82,85,86,88,87] },
  { id: 'cache_hit', title: 'Cache Hit Rate', value: 94.3, unit: '%', trend: 'steady', sparkline: [93,94,93,95,94,94,95,94,94,94.3] },
  { id: 'queue_depth', title: 'Queue Depth', value: 3, unit: 'items', trend: 'down', sparkline: [8,7,6,5,4,3,4,3,3,3] },
  { id: 'conn_pool', title: 'Connection Pool', value: 78, unit: '%', trend: 'up', sparkline: [65,68,70,72,74,75,76,77,78,78] },
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return { panels: {}, locks: {}, compactions: {} };
}
function saveState() {
  const state = {
    panels: {},
    locks: {},
    compactions: {}
  };
  for (const [id, panel] of Object.entries(window._panelState || {})) {
    state.panels[id] = {
      frequency: panel.frequency,
      totalDuration: panel.totalDuration,
      lastViewed: panel.lastViewed,
      interactions: panel.interactions
    };
    state.locks[id] = panel.locked;
    state.compactions[id] = panel.compact;
  }
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch(e) {}
}
function initPanelState() {
  const saved = loadState();
  const state = {};
  for (const dp of demoPanels) {
    const sp = saved.panels[dp.id] || {};
    state[dp.id] = {
      id: dp.id,
      title: dp.title,
      value: dp.value,
      unit: dp.unit,
      trend: dp.trend,
      sparklineData: dp.sparkline.slice(),
      frequency: sp.frequency || 0,
      totalDuration: sp.totalDuration || 0,
      lastViewed: sp.lastViewed || null,
      interactions: sp.interactions || 0,
      locked: saved.locks[dp.id] || false,
      compact: saved.compactions[dp.id] || false,
      lastSparklineHash: '',
      element: null
    };
  }
  window._panelState = state;
}
function computeAttentionScore(panel) {
  const now = Date.now();
  let recency = 1.0;
  if (panel.lastViewed) {
    const hours = (now - panel.lastViewed) / (1000 * 60 * 60);
    recency = Math.exp(-hours / DECAY_HALFLIFE_HOURS);
  }
  const durLog = Math.log(panel.totalDuration + 1);
  const freq = panel.frequency;
  const interactions = panel.interactions;
  return (freq * 0.4 + interactions * 0.3 + durLog * 0.2 + recency * 0.1) * 100;
}
function rankPanels() {
  const panels = Object.values(window._panelState);
  const scored = panels.map(p => ({
    ...p,
    score: computeAttentionScore(p)
  }));
  scored.sort((a, b) => b.score - a.score);
  const scores = scored.map(s => s.score);
  const compactCutoff = percentile(scores, COMPACT_THRESHOLD_PERCENTILE);
  const moreCutoff = percentile(scores, MORE_THRESHOLD_PERCENTILE);
  for (const p of scored) {
    if (p.locked) continue;
    if (p.score <= moreCutoff && scores.length > 6) {
      p.targetCompact = 'more';
    } else if (p.score <= compactCutoff) {
      p.targetCompact = 'compact';
    } else {
      p.targetCompact = 'full';
    }
  }
  return scored;
}
function percentile(arr, pct) {
  if (arr.length === 0) return 0;
  const sorted = arr.slice().sort((a, b) => a - b);
  const idx = Math.floor((pct / 100) * (sorted.length - 1));
  return sorted[idx];
}
function sparklineHash(data) {
  if (!data || data.length === 0) return 'empty';
  let h = 0;
  for (let i = 0; i < data.length; i++) {
    h = ((h << 5) - h + Math.round(data[i] * 100)) | 0;
  }
  return String(h);
}
function renderSparkline(data, width, height, color) {
  if (!data || data.length < 2) return '';
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const stepX = width / (data.length - 1);
  let points = '';
  for (let i = 0; i < data.length; i++) {
    const x = i * stepX;
    const y = height - ((data[i] - min) / range) * (height - 2) - 1;
    points += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
  }
  const fillColor = color === 'up' ? 'rgba(255,94,122,0.15)' :
                    color === 'down' ? 'rgba(61,214,140,0.15)' :
                    'rgba(108,138,255,0.15)';
  const strokeColor = color === 'up' ? '#ff5e7a' :
                      color === 'down' ? '#3dd68c' : '#6c8aff';
  const lastY = height - ((data[data.length-1] - min) / range) * (height - 2) - 1;
  const areaPath = points + 'L' + (data.length-1)*stepX + ',' + (height) + ' L0,' + (height) + ' Z';
  return '<svg viewBox="0 0 ' + width + ' ' + height + '" preserveAspectRatio="none">' +
    '<path d="' + areaPath + '" fill="' + fillColor + '" stroke="none"/>' +
    '<path d="' + points + '" fill="none" stroke="' + strokeColor + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="' + ((data.length-1)*stepX).toFixed(1) + '" cy="' + lastY.toFixed(1) + '" r="2.5" fill="' + strokeColor + '"/>' +
    '</svg>';
}
function buildPanelHTML(panel, score) {
  const color = panel.trend || 'steady';
  let sparkHTML = '';
  const dataHash = sparklineHash(panel.sparklineData);
  if (dataHash !== panel.lastSparklineHash) {
    panel.lastSparklineHash = dataHash;
    sparkHTML = renderSparkline(panel.sparklineData, 200, 36, color);
    panel._cachedSparkline = sparkHTML;
  } else {
    sparkHTML = panel._cachedSparkline || '';
  }
  return '' +
    '<div class="panel-header">' +
      '<span class="panel-title">' + esc(panel.title) + '</span>' +
      '<span class="panel-score">' + score.toFixed(0) + '</span>' +
    '</div>' +
    '<div class="panel-body">' +
      '<span class="panel-value">' + panel.value + '</span>' +
      '<span class="panel-unit">' + esc(panel.unit) + '</span>' +
      '<div class="panel-sparkline">' + sparkHTML + '</div>' +
    '</div>' +
    '<div class="panel-summary">' +
      '<span class="mini-value">' + panel.value + '</span>' +
      '<span class="mini-label">' + esc(panel.unit) + '</span>' +
      '<div class="mini-spark">' + sparkHTML + '</div>' +
    '</div>' +
    '<div class="panel-actions">' +
      '<button data-action="lock" data-id="' + esc(panel.id) + '">' + (panel.locked ? 'Unlock' : 'Lock') + '</button>' +
      '<button data-action="toggle-compact" data-id="' + esc(panel.id) + '">' + (panel.compact ? 'Expand' : 'Compact') + '</button>' +
    '</div>';
}
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'<').replace(/>/g,'>').replace(/"/g,'&quot;');
}
function refreshPanelCache() {
  PANEL_CACHE.clear();
  const grid = document.getElementById('grid');
  if (!grid) return;
  const panels = grid.querySelectorAll('.panel');
  for (const el of panels) {
    const id = el.dataset.panelId;
    if (id) PANEL_CACHE.set(id, el);
  }
}
function getPanelElement(id) {
  let el = PANEL_CACHE.get(id);
  if (!el) {
    el = document.querySelector('.panel[data-panel-id="' + CSS.escape(id) + '"]');
    if (el) PANEL_CACHE.set(id, el);
  }
  return el;
}
function applyLayout(rankedPanels) {
  const grid = document.getElementById('grid');
  const moreSection = document.getElementById('moreSection');
  const existingOrder = [];
  const existingIds = new Set();
  for (const child of grid.children) {
    if (child.classList.contains('panel')) {
      existingIds.add(child.dataset.panelId);
      existingOrder.push(child.dataset.panelId);
    }
  }
  const desiredOrder = [];
  const morePanels = [];
  for (const p of rankedPanels) {
    if (p.targetCompact === 'more') {
      morePanels.push(p);
    } else {
      desiredOrder.push(p);
    }
  }
  const desiredIds = new Set(desiredOrder.map(p => p.id));
  const fullPanels = desiredOrder.filter(p => p.targetCompact === 'full');
  const compactPanels = desiredOrder.filter(p => p.targetCompact === 'compact');
  const totalColumns = 4;
  let row = 0;
  const positions = new Map();
  for (const p of fullPanels) {
    const span = (p.score > 60) ? 2 : 1;
    const col = 1;
    positions.set(p.id, { row: row + 1, col: col, rowSpan: 1, colSpan: Math.min(span, totalColumns) });
    row++;
  }
  for (const p of compactPanels) {
    positions.set(p.id, { row: row + 1, col: 1, rowSpan: 1, colSpan: 1 });
    row++;
  }
  const explicitRows = [];
  for (let r = 0; r < row; r++) {
    const hasFullAtRow = fullPanels.some((p, i) => {
      const pos = positions.get(p.id);
      return pos && pos.row === r + 1;
    });
    explicitRows.push(hasFullAtRow ? '180px' : '100px');
  }
  grid.style.gridTemplateRows = explicitRows.join(' ') || '180px';
  const currentMap = new Map();
  for (const child of grid.children) {
    if (child.classList.contains('panel')) {
      currentMap.set(child.dataset.panelId, child);
    }
  }
  for (const p of rankedPanels) {
    const pos = positions.get(p.id);
    let el = currentMap.get(p.id);
    const isCompact = p.targetCompact === 'compact';
    const isMore = p.targetCompact === 'more';
    if (!el && !isMore) {
      el = document.createElement('div');
      el.className = 'panel';
      el.dataset.panelId = p.id;
      el.innerHTML = buildPanelHTML(p, p.score);
      grid.appendChild(el);
      PANEL_CACHE.set(p.id, el);
    }
    if (el && isMore) {
      el.remove();
      PANEL_CACHE.delete(p.id);
      continue;
    }
    if (el && !isMore) {
      if (pos) {
        el.style.gridRow = pos.row + ' / span ' + pos.rowSpan;
        el.style.gridColumn = pos.col + ' / span ' + pos.colSpan;
      }
      el.classList.toggle('compact', isCompact);
      el.classList.toggle('locked', p.locked);
      const scoreEl = el.querySelector('.panel-score');
      if (scoreEl) scoreEl.textContent = p.score.toFixed(0);
      const dataHash = sparklineHash(p.sparklineData);
      const sparkEl = el.querySelector('.panel-sparkline');
      const miniSparkEl = el.querySelector('.mini-spark');
      if (dataHash !== p.lastSparklineHash) {
        p.lastSparklineHash = dataHash;
        const sparkHTML = renderSparkline(p.sparklineData, 200, 36, p.trend || 'steady');
        p._cachedSparkline = sparkHTML;
        if (sparkEl) sparkEl.innerHTML = sparkHTML;
        if (miniSparkEl) miniSparkEl.innerHTML = sparkHTML;
      }
      const valueEl = el.querySelector('.panel-value');
      const miniValueEl = el.querySelector('.mini-value');
      if (valueEl) valueEl.textContent = p.value;
      if (miniValueEl) miniValueEl.textContent = p.value;
      const lockBtn = el.querySelector('[data-action="lock"]');
      if (lockBtn) lockBtn.textContent = p.locked ? 'Unlock' : 'Lock';
      const compactBtn = el.querySelector('[data-action="toggle-compact"]');
      if (compactBtn) compactBtn.textContent = p.compact ? 'Expand' : 'Compact';
    }
  }
  for (const [id, el] of currentMap) {
    if (!desiredIds.has(id) && !morePanels.find(mp => mp.id === id)) {
      el.remove();
      PANEL_CACHE.delete(id);
    }
  }
  const moreContainer = moreSection.querySelector('.more-chips') || (() => {
    const div = document.createElement('div');
    div.className = 'more-chips';
    div.style.display = 'flex';
    div.style.gap = '8px';
    div.style.flexWrap = 'wrap';
    moreSection.appendChild(div);
    return div;
  })();
  let labelEl = moreSection.querySelector('.more-section-label');
  if (!labelEl) {
    labelEl = document.createElement('span');
    labelEl.className = 'more-section-label';
    labelEl.textContent = 'More';
    moreSection.insertBefore(labelEl, moreSection.firstChild);
  }
  moreContainer.innerHTML = '';
  for (const p of morePanels) {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = p.title + ' (' + p.value + p.unit + ')';
    chip.dataset.panelId = p.id;
    chip.addEventListener('click', () => {
      p.compact = false;
      window._panelState[p.id].compact = false;
      window._panelState[p.id].locked = true;
      window._panelState[p.id].frequency += 3;
      window._panelState[p.id].interactions += 1;
      window._panelState[p.id].lastViewed = Date.now();
      saveState();
      runLayoutCycle();
    });
    moreContainer.appendChild(chip);
  }
  if (morePanels.length === 0) {
    moreSection.style.display = 'none';
  } else {
    moreSection.style.display = '';
  }
  document.getElementById('trackedCount').textContent =
    Object.keys(window._panelState).filter(id => {
      const p = window._panelState[id];
      return p.frequency > 0 || p.totalDuration > 0;
    }).length + ' panels';
}
function runLayoutCycle() {
  const ranked = rankPanels();
  applyLayout(ranked);
  saveState();
}
function setupIntersectionObserver() {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const id = entry.target.dataset.panelId;
      if (!id || !window._panelState[id]) return;
      if (entry.isIntersecting) {
        entry.target._visibleSince = entry.target._visibleSince || Date.now();
      } else if (entry.target._visibleSince) {
        const duration = Date.now() - entry.target._visibleSince;
        window._panelState[id].totalDuration += duration;
        window._panelState[id].lastViewed = Date.now();
        entry.target._visibleSince = null;
        saveState();
      }
    }
  }, { threshold: 0.3 });
  const grid = document.getElementById('grid');
  const mutationObs = new MutationObserver((mutations) => {
    let structuralChange = false;
    for (const m of mutations) {
      if (m.type === 'childList') {
        for (const node of m.addedNodes) {
          if (node.nodeType === 1 && node.classList.contains('panel')) {
            structuralChange = true;
            observer.observe(node);
            PANEL_CACHE.set(node.dataset.panelId, node);
          }
        }
        for (const node of m.removedNodes) {
          if (node.nodeType === 1 && node.classList.contains('panel')) {
            PANEL_CACHE.delete(node.dataset.panelId);
            observer.unobserve(node);
          }
        }
      }
    }
    if (structuralChange) refreshPanelCache();
  });
  mutationObs.observe(grid, { childList: true, subtree: false });
  for (const el of grid.querySelectorAll('.panel')) {
    observer.observe(el);
    PANEL_CACHE.set(el.dataset.panelId, el);
  }
}
function setupEventDelegation() {
  const grid = document.getElementById('grid');
  grid.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) {
      const panel = e.target.closest('.panel');
      if (panel) {
        const id = panel.dataset.panelId;
        if (id && window._panelState[id]) {
          window._panelState[id].frequency += 1;
          window._panelState[id].interactions += 1;
          window._panelState[id].lastViewed = Date.now();
        }
      }
      return;
    }
    const id = btn.dataset.id;
    if (!id || !window._panelState[id]) return;
    const panel = window._panelState[id];
    if (btn.dataset.action === 'lock') {
      panel.locked = !panel.locked;
      panel.interactions += 1;
    } else if (btn.dataset.action === 'toggle-compact') {
      panel.compact = !panel.compact;
      panel.interactions += 1;
    }
    saveState();
    runLayoutCycle();
  });
  grid.addEventListener('mouseenter', (e) => {
    const panel = e.target.closest('.panel');
    if (panel && panel.dataset.panelId && window._panelState[panel.dataset.panelId]) {
      window._panelState[panel.dataset.panelId].frequency += 0.5;
    }
  }, true);
}
function setupToolbar() {
  document.getElementById('btnReset').addEventListener('click', () => {
    localStorage.removeItem(STORAGE_KEY);
    initPanelState();
    runLayoutCycle();
  });
  document.getElementById('btnCompactAll').addEventListener('click', () => {
    for (const [id, p] of Object.entries(window._panelState)) {
      if (!p.locked) p.compact = true;
    }
    saveState();
    runLayoutCycle();
  });
  document.getElementById('btnExpandAll').addEventListener('click', () => {
    for (const [id, p] of Object.entries(window._panelState)) {
      p.compact = false;
    }
    saveState();
    runLayoutCycle();
  });
}
function simulateDataUpdates() {
  setInterval(() => {
    for (const [id, panel] of Object.entries(window._panelState)) {
      const delta = (Math.random() - 0.5) * (panel.value * 0.05);
      panel.value = Math.max(0, +(panel.value + delta).toFixed(panel.value < 10 ? 2 : 0));
      panel.sparklineData.push(panel.value);
      if (panel.sparklineData.length > 20) panel.sparklineData.shift();
    }
    runLayoutCycle();
  }, UPDATE_INTERVAL);
}
function init() {
  initPanelState();
  setupIntersectionObserver();
  setupEventDelegation();
  setupToolbar();
  runLayoutCycle();
  simulateDataUpdates();
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