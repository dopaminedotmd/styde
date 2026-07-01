<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-muted: #8b949e;
  --accent: #58a6ff;
  --accent-dim: #1f6feb;
  --danger: #f85149;
  --success: #3fb950;
  --warning: #d2991d;
  --panel-gap: 8px;
  --radius: 8px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.toolbar h1 { font-size: 16px; font-weight: 600; letter-spacing: -0.3px; }
.toolbar .spacer { flex: 1; }
.btn {
  background: var(--border);
  color: var(--text);
  border: 1px solid var(--border);
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: background 0.15s, border-color 0.15s;
}
.btn:hover { background: #3a3f4b; border-color: #5a5f6b; }
.btn.active { background: var(--accent-dim); border-color: var(--accent); color: #fff; }
.btn.danger { border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: rgba(248,81,73,0.15); }
.badge {
  background: var(--accent-dim);
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 600;
}
.dashboard {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-auto-rows: minmax(140px, auto);
  gap: var(--panel-gap);
  padding: 12px;
  max-width: 1600px;
  margin: 0 auto;
  transition: grid-template-columns 0.3s ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: grid-column 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              grid-row 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.25s,
              transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}
.panel.dragging {
  opacity: 0.7;
  transform: scale(0.97);
  z-index: 50;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.panel.locked { border-color: var(--warning); }
.panel.locked::after {
  content: '🔒';
  position: absolute;
  top: 4px;
  right: 8px;
  font-size: 10px;
  opacity: 0.7;
  pointer-events: none;
}
.panel.compact .panel-body { padding: 8px; font-size: 11px; }
.panel.compact .panel-body canvas,
.panel.compact .panel-body svg { max-height: 60px; }
.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--border);
  font-size: 12px;
  font-weight: 600;
  cursor: grab;
  user-select: none;
  min-height: 34px;
}
.panel-header:active { cursor: grabbing; }
.panel-header .title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-header .score-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.panel-header .score-dot.hot { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
.panel-header .score-dot.warm { background: var(--warning); }
.panel-header .score-dot.cool { background: var(--text-muted); }
.panel-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.panel-actions button {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 12px;
  padding: 2px 4px;
  border-radius: 4px;
  line-height: 1;
}
.panel-actions button:hover { color: var(--text); background: rgba(255,255,255,0.08); }
.panel-body {
  flex: 1;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}
.panel-body .metric-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}
.panel-body .metric-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}
.panel-body .sparkline {
  width: 100%;
  height: 40px;
  margin-top: 8px;
}
.compact-only { display: none; }
.panel.compact .compact-only { display: block; }
.panel.compact .full-only { display: none; }
.panel.compact .metric-value { font-size: 16px; }
.panel-rank-badge {
  position: absolute;
  top: 6px;
  left: 8px;
  font-size: 10px;
  color: var(--text-muted);
  opacity: 0.5;
  pointer-events: none;
}
.more-section {
  grid-column: 1 / -1;
  margin-top: 8px;
}
.more-section summary {
  cursor: pointer;
  padding: 8px 12px;
  font-size: 12px;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  list-style: none;
}
.more-section summary::-webkit-details-marker { display: none; }
.more-section summary::before { content: '▸ '; }
.more-section[open] summary::before { content: '▾ '; }
.more-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--panel-gap);
  margin-top: 8px;
}
.panel-drag-over { border-color: var(--accent) !important; background: rgba(88,166,255,0.05); }
.toast {
  position: fixed;
  bottom: 16px;
  right: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 10px 16px;
  border-radius: var(--radius);
  font-size: 12px;
  z-index: 200;
  animation: toastIn 0.3s ease, toastOut 0.3s ease 2s forwards;
  pointer-events: none;
}
@keyframes toastIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes toastOut { from { opacity: 1; } to { opacity: 0; } }
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Layout</h1>
  <span class="badge" id="sessionBadge">Session 1</span>
  <span class="spacer"></span>
  <button class="btn" id="btnReset" title="Reset all tracking data">Reset Data</button>
  <button class="btn" id="btnExport" title="Export layout config">Export</button>
  <button class="btn" id="btnImport" title="Import layout config">Import</button>
  <input type="file" id="importFile" style="display:none" accept=".json">
  <span style="font-size:11px;color:var(--text-muted)" id="trackStatus">● Active</span>
</div>
<div class="dashboard" id="dashboard"></div>
<div id="toastContainer"></div>
<script>
(function() {
'use strict';
const STORAGE_KEY = 'adaptive_dashboard_v2';
const IDLE_THRESHOLD_MS = 5000;
const THROTTLE_IDLE_HZ = 1;
const COMPACT_THRESHOLD = 0.15;
const COLLAPSE_THRESHOLD = 0.05;
const RECENCY_DECAY = 0.92;
const MAX_PANELS_VISIBLE = 12;
const PANEL_DEFS = [
  { id: 'revenue',    title: 'Revenue',        icon: '📊', color: '#3fb950', value: '$48,291', change: '+12.4%', sparkData: [20,25,22,30,28,35,32,38,42,40,45,48] },
  { id: 'users',      title: 'Active Users',   icon: '👥', color: '#58a6ff', value: '18,432',  change: '+7.2%',  sparkData: [10,12,11,15,14,16,15,17,18,17,19,18] },
  { id: 'latency',    title: 'API Latency',    icon: '⚡', color: '#d2991d', value: '124ms',   change: '-3.1%',  sparkData: [150,145,140,135,130,128,126,125,124,123,124,124] },
  { id: 'errors',     title: 'Error Rate',     icon: '🚨', color: '#f85149', value: '0.12%',   change: '-0.8%',  sparkData: [0.5,0.4,0.35,0.3,0.25,0.2,0.18,0.15,0.14,0.13,0.12,0.12] },
  { id: 'cpu',        title: 'CPU Usage',      icon: '💻', color: '#bc8cff', value: '67%',     change: '+2.1%',  sparkData: [55,58,60,62,61,63,65,64,66,67,66,67] },
  { id: 'memory',     title: 'Memory',         icon: '🧠', color: '#ff7b72', value: '8.2 GB',  change: '+4.5%',  sparkData: [6,6.5,6.8,7,7.2,7.5,7.8,7.9,8,8.1,8.2,8.2] },
  { id: 'requests',   title: 'Requests/sec',   icon: '🌐', color: '#79c0ff', value: '3,821',   change: '+15.2%', sparkData: [2,2.2,2.5,2.8,3,3.2,3.1,3.3,3.5,3.6,3.7,3.8] },
  { id: 'uptime',     title: 'Uptime',         icon: '✅', color: '#56d364', value: '99.97%',  change: '+0.02%', sparkData: [99.9,99.9,99.9,99.9,99.9,99.9,99.95,99.96,99.97,99.97,99.97,99.97] },
  { id: 'disk',       title: 'Disk I/O',       icon: '💾', color: '#e3b341', value: '142 MB/s',change: '-5.3%',  sparkData: [180,175,170,165,160,155,150,148,145,143,142,142] },
  { id: 'cache',      title: 'Cache Hit Rate', icon: '🎯', color: '#a5d6ff', value: '94.2%',   change: '+1.1%',  sparkData: [88,89,90,91,92,92.5,93,93.5,93.8,94,94.1,94.2] },
  { id: 'queue',      title: 'Queue Depth',    icon: '📋', color: '#ffa657', value: '342',     change: '+8.7%',  sparkData: [250,260,270,280,290,300,310,320,330,335,340,342] },
  { id: 'sessions',   title: 'Sessions',       icon: '🔑', color: '#7ee787', value: '5,821',   change: '+3.4%',  sparkData: [5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.7,5.8,5.8,5.82] },
  { id: 'bandwidth',  title: 'Bandwidth',      icon: '📡', color: '#d2a8ff', value: '2.4 Gbps',change: '+9.8%',  sparkData: [1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.3,2.4,2.4] },
  { id: 'db_conn',    title: 'DB Connections', icon: '🗄️', color: '#ffa198', value: '48',      change: '-2.1%',  sparkData: [55,53,52,51,50,49,49,48,48,48,48,48] },
  { id: 'logs',       title: 'Log Rate',       icon: '📝', color: '#c9d1d9', value: '1.2k/s',  change: '+0.5%',  sparkData: [1,1.1,1.15,1.18,1.2,1.21,1.22,1.2,1.21,1.2,1.2,1.2] },
];
let panels = [];
let trackingState = {};
let layoutOrder = [];
let lockedPanels = new Set();
let manualPositions = {};
let observer = null;
let idleTimer = null;
let isIdle = false;
let isVisible = true;
let sessionCount = 1;
let dragState = null;
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const saved = JSON.parse(raw);
      trackingState = saved.tracking || {};
      layoutOrder = saved.layoutOrder || [];
      lockedPanels = new Set(saved.lockedPanels || []);
      manualPositions = saved.manualPositions || {};
      sessionCount = (saved.sessionCount || 0) + 1;
      if (saved.panels) {
        saved.panels.forEach(sp => {
          const def = PANEL_DEFS.find(d => d.id === sp.id);
          if (def) Object.assign(def, sp);
        });
      }
    }
  } catch(e) { /* first run */ }
}
function saveState() {
  const data = {
    tracking: trackingState,
    layoutOrder,
    lockedPanels: [...lockedPanels],
    manualPositions,
    sessionCount,
    panels: PANEL_DEFS.map(p => ({ id: p.id, value: p.value, change: p.change, sparkData: p.sparkData })),
    savedAt: Date.now()
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
function initTracking() {
  PANEL_DEFS.forEach(def => {
    if (!trackingState[def.id]) {
      trackingState[def.id] = {
        views: 0,
        totalDuration: 0,
        lastInteraction: 0,
        interactions: 0,
        expanded: 0,
        collapsed: 0,
        viewStart: null
      };
    }
  });
}
function computeScore(panelId) {
  const t = trackingState[panelId] || { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
  const now = Date.now();
  const hoursSinceLast = Math.max(0.1, (now - (t.lastInteraction || now - 86400000)) / 3600000);
  const recency = Math.exp(-hoursSinceLast * (1 - RECENCY_DECAY));
  const frequency = t.interactions + t.views * 0.5;
  const duration = Math.min(t.totalDuration / 1000, 3600);
  return frequency * Math.log2(duration + 2) * recency;
}
function rankPanels() {
  const scored = PANEL_DEFS.map(def => ({
    id: def.id,
    score: computeScore(def.id),
    locked: lockedPanels.has(def.id)
  }));
  scored.sort((a, b) => b.score - a.score);
  return scored;
}
function computeLayout() {
  const ranked = rankPanels();
  layoutOrder = ranked.map(r => r.id);
  const maxScore = ranked.length > 0 ? Math.max(...ranked.map(r => r.score)) : 1;
  const result = [];
  const visible = [];
  const collapsed = [];
  ranked.forEach((r, i) => {
    const normScore = maxScore > 0 ? r.score / maxScore : 0;
    const def = PANEL_DEFS.find(d => d.id === r.id);
    let cols, rows, compact;
    if (normScore >= 0.65) {
      cols = 2; rows = 2; compact = false;
    } else if (normScore >= 0.3) {
      cols = 1; rows = 2; compact = false;
    } else if (normScore >= COMPACT_THRESHOLD) {
      cols = 1; rows = 1; compact = true;
    } else {
      cols = 1; rows = 1; compact = true;
    }
    if (r.locked && manualPositions[r.id]) {
      const mp = manualPositions[r.id];
      cols = mp.cols || cols;
      rows = mp.rows || rows;
      compact = mp.compact !== undefined ? mp.compact : compact;
    }
    const panelLayout = { id: r.id, score: r.score, cols, rows, compact, locked: r.locked, rank: i + 1 };
    if (normScore < COLLAPSE_THRESHOLD && !r.locked && visible.length >= MAX_PANELS_VISIBLE) {
      collapsed.push(panelLayout);
    } else {
      visible.push(panelLayout);
    }
    result.push(panelLayout);
  });
  return { visible, collapsed, all: result };
}
function renderSparkline(data, width, height, color) {
  if (!data || data.length < 2) return '';
  const w = width || 120;
  const h = height || 40;
  const pad = 2;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const points = data.map((v, i) => {
    const x = pad + (i / (data.length - 1)) * (w - 2 * pad);
    const y = h - pad - ((v - min) / range) * (h - 2 * pad);
    return `${x},${y}`;
  });
  const lastX = pad + (data.length - 1) / (data.length - 1) * (w - 2 * pad);
  const lastY = h - pad - ((data[data.length - 1] - min) / range) * (h - 2 * pad);
  const fillPoints = points.join(' ') + ` ${lastX},${h - pad} ${pad},${h - pad}`;
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="overflow:visible">
    <defs><linearGradient id="grad_${color.slice(1)}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${color}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="${color}" stop-opacity="0.02"/>
    </linearGradient></defs>
    <polygon points="${fillPoints}" fill="url(#grad_${color.slice(1)})"/>
    <polyline points="${points.join(' ')}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="${lastX}" cy="${lastY}" r="2.5" fill="${color}"/>
  </svg>`;
}
function scoreClass(score, maxScore) {
  if (!maxScore || maxScore === 0) return 'cool';
  const norm = score / maxScore;
  if (norm >= 0.65) return 'hot';
  if (norm >= 0.3) return 'warm';
  return 'cool';
}
function renderPanel(panelLayout) {
  const def = PANEL_DEFS.find(d => d.id === panelLayout.id);
  if (!def) return '';
  const cl = panelLayout.compact ? ' compact' : '';
  const locked = panelLayout.locked ? ' locked' : '';
  const sc = scoreClass(panelLayout.score, panelLayout.score);
  const sparkSvg = renderSparkline(def.sparkData, panelLayout.compact ? 80 : 120, panelLayout.compact ? 28 : 40, def.color);
  return `<div class="panel${cl}${locked}" data-panel-id="${def.id}" draggable="true">
    <div class="panel-header">
      <span class="score-dot ${sc}" title="Score: ${panelLayout.score.toFixed(2)}"></span>
      <span class="title">${def.icon} ${def.title}</span>
      <span style="font-size:10px;color:var(--text-muted);flex-shrink:0">#${panelLayout.rank}</span>
      <div class="panel-actions">
        <button class="btn-lock" title="${panelLayout.locked ? 'Unlock' : 'Lock'} position">${panelLayout.locked ? '🔓' : '🔒'}</button>
        <button class="btn-compact" title="Toggle compact">${panelLayout.compact ? '⛶' : '⊟'}</button>
      </div>
    </div>
    <div class="panel-body">
      <div style="text-align:center">
        <div class="metric-value" style="color:${def.color}">${def.value}</div>
        <div class="metric-label">${def.change.startsWith('+') ? '↑' : '↓'} ${def.change}</div>
        <div class="sparkline full-only">${sparkSvg}</div>
        <div class="compact-only" style="font-size:10px;color:var(--text-muted);margin-top:4px">${def.change}</div>
      </div>
    </div>
  </div>`;
}
function renderDashboard() {
  const { visible, collapsed } = computeLayout();
  const maxScore = visible.length > 0 ? Math.max(...visible.map(v => v.score)) : 1;
  const dash = document.getElementById('dashboard');
  let html = '';
  visible.forEach(panelLayout => {
    const cols = Math.min(panelLayout.cols, 6);
    html += `<div style="grid-column:span ${cols};grid-row:span ${panelLayout.rows}">${renderPanel(panelLayout)}</div>`;
  });
  if (collapsed.length > 0) {
    html += `<div class="more-section"><details><summary>${collapsed.length} more panels ▾</summary><div class="more-grid">`;
    collapsed.forEach(panelLayout => {
      html += renderPanel(panelLayout);
    });
    html += '</div></details></div>';
  }
  dash.innerHTML = html;
  attachPanelEvents();
}
function attachPanelEvents() {
  document.querySelectorAll('.panel').forEach(el => {
    const id = el.dataset.panelId;
    if (!id) return;
    el.addEventListener('mouseenter', () => startView(id));
    el.addEventListener('mouseleave', () => endView(id));
    el.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      recordInteraction(id);
    });
    el.addEventListener('dragstart', handleDragStart);
    el.addEventListener('dragover', handleDragOver);
    el.addEventListener('dragleave', handleDragLeave);
    el.addEventListener('drop', handleDrop);
    el.addEventListener('dragend', handleDragEnd);
    el.querySelector('.btn-lock')?.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleLock(id);
    });
    el.querySelector('.btn-compact')?.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCompact(id);
    });
  });
}
function startView(id) {
  if (!isVisible || isIdle) return;
  if (!trackingState[id]) return;
  if (trackingState[id].viewStart) return;
  trackingState[id].viewStart = Date.now();
  trackingState[id].views = (trackingState[id].views || 0) + 1;
}
function endView(id) {
  if (!trackingState[id]) return;
  if (trackingState[id].viewStart) {
    const duration = Date.now() - trackingState[id].viewStart;
    trackingState[id].totalDuration = (trackingState[id].totalDuration || 0) + duration;
    trackingState[id].viewStart = null;
  }
}
function recordInteraction(id) {
  if (!isVisible || isIdle) return;
  if (!trackingState[id]) return;
  trackingState[id].interactions = (trackingState[id].interactions || 0) + 1;
  trackingState[id].lastInteraction = Date.now();
  if (!trackingState[id].viewStart) {
    trackingState[id].views = (trackingState[id].views || 0) + 1;
  }
  scheduleSave();
}
function toggleLock(id) {
  if (lockedPanels.has(id)) {
    lockedPanels.delete(id);
    delete manualPositions[id];
    toast(`Unlocked: ${PANEL_DEFS.find(d => d.id === id)?.title || id}`);
  } else {
    lockedPanels.add(id);
    manualPositions[id] = { cols: 2, rows: 2, compact: false };
    toast(`Locked: ${PANEL_DEFS.find(d => d.id === id)?.title || id}`);
  }
  recordInteraction(id);
  renderDashboard();
  saveState();
}
function toggleCompact(id) {
  const existing = manualPositions[id] || {};
  const panelEl = document.querySelector(`[data-panel-id="${id}"]`);
  const currentlyCompact = panelEl?.classList.contains('compact');
  manualPositions[id] = { ...existing, compact: !currentlyCompact };
  lockedPanels.add(id);
  recordInteraction(id);
  renderDashboard();
  saveState();
}
function handleDragStart(e) {
  const id = e.currentTarget.dataset.panelId;
  dragState = { id, startX: e.clientX, startY: e.clientY };
  e.currentTarget.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', id);
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('panel-drag-over');
}
function handleDragLeave(e) {
  e.currentTarget.classList.remove('panel-drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('panel-drag-over');
  const fromId = e.dataTransfer.getData('text/plain');
  const toId = e.currentTarget.dataset.panelId;
  if (fromId && toId && fromId !== toId) {
    swapPanels(fromId, toId);
  }
}
function handleDragEnd(e) {
  e.currentTarget.classList.remove('dragging');
  document.querySelectorAll('.panel-drag-over').forEach(el => el.classList.remove('panel-drag-over'));
  dragState = null;
}
function swapPanels(idA, idB) {
  lockedPanels.add(idA);
  lockedPanels.add(idB);
  const posA = manualPositions[idA] || { cols: 2, rows: 2, compact: false };
  const posB = manualPositions[idB] || { cols: 2, rows: 2, compact: false };
  manualPositions[idA] = posB;
  manualPositions[idB] = posA;
  recordInteraction(idA);
  recordInteraction(idB);
  renderDashboard();
  saveState();
  toast('Panels swapped');
}
function toast(msg) {
  const container = document.getElementById('toastContainer');
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}
let saveTimeout = null;
function scheduleSave() {
  clearTimeout(saveTimeout);
  saveTimeout = setTimeout(saveState, 2000);
}
function setupIntersectionObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    isVisible = entries[0].isIntersecting;
    updateTrackingStatus();
  }, { threshold: 0.1 });
  observer.observe(document.getElementById('dashboard'));
}
function setupIdleDetection() {
  const resetIdle = () => {
    isIdle = false;
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      isIdle = true;
      updateTrackingStatus();
    }, IDLE_THRESHOLD_MS);
  };
  ['mousemove', 'keydown', 'scroll', 'click', 'touchstart'].forEach(evt => {
    document.addEventListener(evt, resetIdle, { passive: true });
  });
  resetIdle();
}
function updateTrackingStatus() {
  const el = document.getElementById('trackStatus');
  if (!isVisible) {
    el.textContent = '◌ Paused (off-screen)';
    el.style.color = 'var(--text-muted)';
  } else if (isIdle) {
    el.textContent = '◌ Throttled (idle)';
    el.style.color = 'var(--warning)';
  } else {
    el.textContent = '● Active';
    el.style.color = 'var(--success)';
  }
}
function resetAll() {
  trackingState = {};
  layoutOrder = [];
  lockedPanels.clear();
  manualPositions = {};
  initTracking();
  renderDashboard();
  saveState();
  toast('All tracking data reset');
}
function exportConfig() {
  const data = {
    tracking: trackingState,
    layoutOrder,
    lockedPanels: [...lockedPanels],
    manualPositions,
    sessionCount,
    panels: PANEL_DEFS.map(p => ({ id: p.id, value: p.value, change: p.change, sparkData: p.sparkData })),
    exportedAt: new Date().toISOString()
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `dashboard-layout-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  toast('Layout exported');
}
function importConfig(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      if (data.tracking) trackingState = data.tracking;
      if (data.layoutOrder) layoutOrder = data.layoutOrder;
      if (data.lockedPanels) lockedPanels = new Set(data.lockedPanels);
      if (data.manualPositions) manualPositions = data.manualPositions;
      if (data.sessionCount) sessionCount = data.sessionCount;
      if (data.panels) {
        data.panels.forEach(sp => {
          const def = PANEL_DEFS.find(d => d.id === sp.id);
          if (def) Object.assign(def, sp);
        });
      }
      renderDashboard();
      saveState();
      toast('Layout imported');
    } catch(err) {
      toast('Import failed: invalid file');
    }
  };
  reader.readAsText(file);
}
function simulateActivity() {
  const ids = PANEL_DEFS.map(d => d.id);
  for (let i = 0; i < 30; i++) {
    const id = ids[Math.floor(Math.random() * ids.length)];
    if (!trackingState[id]) continue;
    trackingState[id].views = (trackingState[id].views || 0) + 1;
    trackingState[id].interactions = (trackingState[id].interactions || 0) + Math.floor(Math.random() * 3);
    trackingState[id].totalDuration = (trackingState[id].totalDuration || 0) + Math.random() * 30000;
    trackingState[id].lastInteraction = Date.now() - Math.random() * 86400000;
  }
}
document.getElementById('btnReset').addEventListener('click', resetAll);
document.getElementById('btnExport').addEventListener('click', exportConfig);
document.getElementById('btnImport').addEventListener('click', () => {
  document.getElementById('importFile').click();
});
document.getElementById('importFile').addEventListener('change', (e) => {
  if (e.target.files[0]) importConfig(e.target.files[0]);
});
document.getElementById('sessionBadge').textContent = `Session ${sessionCount}`;
loadState();
initTracking();
setupIntersectionObserver();
setupIdleDetection();
simulateActivity();
renderDashboard();
saveState();
const refreshInterval = setInterval(() => {
  if (isVisible && !isIdle) {
    PANEL_DEFS.forEach(def => {
      const base = parseFloat(def.value.replace(/[^0-9.]/g, ''));
      if (!isNaN(base)) {
        const jitter = base * (Math.random() * 0.04 - 0.02);
        const newVal = base + jitter;
        if (def.value.includes('$')) def.value = '$' + Math.round(newVal).toLocaleString();
        else if (def.value.includes('ms')) def.value = Math.round(newVal) + 'ms';
        else if (def.value.includes('%') && def.value.length < 6) def.value = newVal.toFixed(2) + '%';
        else if (def.value.includes('GB')) def.value = newVal.toFixed(1) + ' GB';
        else if (def.value.includes('Gbps')) def.value = newVal.toFixed(1) + ' Gbps';
        else if (def.value.includes('MB/s')) def.value = Math.round(newVal) + ' MB/s';
        else if (def.value.includes('k/s')) def.value = newVal.toFixed(1) + 'k/s';
        else def.value = Math.round(newVal).toLocaleString();
      }
      if (def.sparkData && def.sparkData.length > 0) {
        def.sparkData.push(def.sparkData[def.sparkData.length - 1] * (1 + (Math.random() - 0.5) * 0.06));
        if (def.sparkData.length > 24) def.sparkData.shift();
      }
    });
    renderDashboard();
  }
}, 3000);
})();
</script>
</body>
</html>