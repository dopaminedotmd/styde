```html
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
  --surface2: #21252f;
  --border: #2a2e3a;
  --text: #d4d8e0;
  --text2: #8b90a0;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --gap: 12px;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
.header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:var(--surface);border-bottom:1px solid var(--border);}
.header h1{font-size:1.2rem;font-weight:600;}
.header-actions{display:flex;gap:8px;}
.btn{padding:7px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:0.82rem;transition:all .15s;}
.btn:hover{background:var(--border);}
.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff;}
.btn.danger{background:transparent;border-color:var(--danger);color:var(--danger);}
.grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(140px,auto);gap:var(--gap);padding:24px;max-width:1400px;margin:0 auto;}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);cursor:grab;transition:all .25s ease;display:flex;flex-direction:column;overflow:hidden;position:relative;min-height:140px;}
.panel.dragging{opacity:.5;border-color:var(--accent);box-shadow:0 0 20px rgba(108,140,255,.2);}
.panel.drag-over{border-color:var(--accent2);box-shadow:0 0 16px rgba(74,222,128,.15);}
.panel.locked{border-left:3px solid var(--warn);}
.panel.compact{min-height:60px;grid-row:span 1;}
.panel.compact .panel-body{display:none;}
.panel.compact .panel-compact-preview{display:flex;}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--border);gap:8px;flex-shrink:0;}
.panel-title{font-size:.82rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.panel-rank{font-size:.68rem;color:var(--text2);white-space:nowrap;}
.panel-actions{display:flex;gap:4px;flex-shrink:0;}
.panel-actions button{background:none;border:none;color:var(--text2);cursor:pointer;padding:3px;border-radius:4px;font-size:.75rem;line-height:1;transition:all .15s;}
.panel-actions button:hover{color:var(--text);background:var(--border);}
.panel-actions button.locked-btn{color:var(--warn);}
.panel-body{padding:14px;flex:1;display:flex;flex-direction:column;justify-content:center;min-height:60px;}
.metric-value{font-size:2.2rem;font-weight:700;line-height:1.1;}
.metric-label{font-size:.72rem;color:var(--text2);margin-top:4px;}
.metric-change{font-size:.75rem;margin-top:4px;}
.metric-change.up{color:var(--accent2);}
.metric-change.down{color:var(--danger);}
.sparkline{height:40px;margin-top:10px;display:flex;align-items:flex-end;gap:2px;}
.sparkline-bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;opacity:.6;min-height:2px;transition:height .3s;}
.panel-footer{display:flex;align-items:center;justify-content:space-between;padding:8px 14px;border-top:1px solid var(--border);font-size:.68rem;color:var(--text2);flex-shrink:0;}
.panel-compact-preview{display:none;align-items:center;padding:10px 14px;gap:12px;flex:1;}
.panel-compact-preview .mini-val{font-size:1.1rem;font-weight:700;}
.panel-compact-preview .mini-label{font-size:.7rem;color:var(--text2);}
.panel:hover{background:var(--surface2);}
.usage-bar{height:3px;background:var(--border);border-radius:2px;margin-top:6px;overflow:hidden;}
.usage-bar-fill{height:100%;background:var(--accent);transition:width .3s;}
.stats-bar{display:flex;gap:20px;padding:10px 24px;background:var(--surface);border-bottom:1px solid var(--border);font-size:.72rem;color:var(--text2);}
.stats-bar span{display:flex;align-items:center;gap:4px;}
.stats-bar b{color:var(--text);}
.toast{position:fixed;bottom:20px;right:20px;padding:10px 18px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;font-size:.78rem;opacity:0;transform:translateY(10px);transition:all .25s;z-index:100;pointer-events:none;}
.toast.show{opacity:1;transform:translateY(0);}
.drag-ghost{position:fixed;pointer-events:none;z-index:1000;opacity:.85;transform:rotate(2deg);background:var(--surface);border:2px solid var(--accent);border-radius:var(--radius);padding:8px 16px;font-size:.8rem;font-weight:600;box-shadow:0 8px 30px rgba(0,0,0,.5);}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <button class="btn" onclick="resetTracking()" title="Reset all tracking data">Reset Tracking</button>
    <button class="btn" onclick="forceRecompute()" title="Recompute layout from tracking data">Recompute</button>
    <button class="btn danger" onclick="resetAll()">Reset All</button>
  </div>
</div>
<div class="stats-bar" id="statsBar">
  <span>Session: <b id="sessionTime">0s</b></span>
  <span>Interactions: <b id="interactionCount">0</b></span>
  <span>Layout recomputes: <b id="recomputeCount">0</b></span>
  <span>Panels: <b id="panelCount">0</b></span>
</div>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<div class="drag-ghost" id="dragGhost" style="display:none"></div>
<script>
// ── Deterministic Mock Data Layer ──
const MockDataSource = (() => {
  const seeds = {
    revenue: 0.72, users: 0.31, latency: 0.88, errors: 0.15,
    cpu: 0.54, memory: 0.67, disk: 0.41, requests: 0.93,
    uptime: 0.99, throughput: 0.77, cost: 0.23, apdex: 0.89,
    churn: 0.12, conversion: 0.45, sessions: 0.61, bandwidth: 0.56
  };
  function seededRand(seed, index) {
    const x = Math.sin(seed * 9999 + index * 0.1) * 10000;
    return x - Math.floor(x);
  }
  function getValue(key, index = 0) {
    const s = seeds[key] || 0.5;
    return seededRand(s, index);
  }
  return {
    getMetric(panelId, now = Date.now()) {
      const minute = Math.floor(now / 60000);
      const r = getValue(panelId, minute);
      const configs = {
        revenue:    { base: 48250,  range: 12000, unit: '$',   format: v => '$' + v.toLocaleString(undefined,{maximumFractionDigits:0}) },
        users:      { base: 12400,  range: 5000,  unit: '',    format: v => v.toLocaleString(undefined,{maximumFractionDigits:0}) },
        latency:    { base: 45,     range: 30,    unit: 'ms',  format: v => v.toFixed(0) + 'ms' },
        errors:     { base: 12,     range: 25,    unit: '',    format: v => v.toFixed(0) },
        cpu:        { base: 62,     range: 30,    unit: '%',   format: v => v.toFixed(0) + '%' },
        memory:     { base: 74,     range: 20,    unit: '%',   format: v => v.toFixed(0) + '%' },
        disk:       { base: 58,     range: 20,    unit: '%',   format: v => v.toFixed(0) + '%' },
        requests:   { base: 8500,   range: 4000,  unit: '/s',  format: v => v.toLocaleString(undefined,{maximumFractionDigits:0}) + '/s' },
        uptime:     { base: 99.95,  range: 0.5,   unit: '%',   format: v => v.toFixed(2) + '%' },
        throughput: { base: 3200,   range: 1500,  unit: 'rps', format: v => v.toLocaleString(undefined,{maximumFractionDigits:0}) + ' rps' },
        cost:       { base: 1840,   range: 400,   unit: '$',   format: v => '$' + v.toFixed(0) },
        apdex:      { base: 0.94,   range: 0.08,  unit: '',    format: v => v.toFixed(3) },
        churn:      { base: 2.3,    range: 1.5,   unit: '%',   format: v => v.toFixed(1) + '%' },
        conversion: { base: 8.2,    range: 3,     unit: '%',   format: v => v.toFixed(1) + '%' },
        sessions:   { base: 5600,   range: 2000,  unit: '',    format: v => v.toLocaleString(undefined,{maximumFractionDigits:0}) },
        bandwidth:  { base: 240,    range: 80,    unit: 'Mbps',format: v => v.toFixed(0) + ' Mbps' }
      };
      const c = configs[panelId] || { base: 100, range: 50, unit: '', format: v => v.toFixed(1) };
      const val = c.base + (r - 0.5) * 2 * c.range;
      return { value: val, formatted: c.format(val), unit: c.unit };
    },
    getSparkline(panelId, points = 20, now = Date.now()) {
      const vals = [];
      for (let i = 0; i < points; i++) {
        const minute = Math.floor((now - (points - 1 - i) * 60000) / 60000);
        vals.push(getValue(panelId, minute));
      }
      return vals;
    },
    getChange(panelId, now = Date.now()) {
      const current = getValue(panelId, Math.floor(now / 60000));
      const prev = getValue(panelId, Math.floor((now - 60000) / 60000));
      return ((current - prev) * 100).toFixed(1);
    }
  };
})();
// ── State ──
const STORAGE_KEY_TRACKING = 'adaptive_dashboard_tracking';
const STORAGE_KEY_LAYOUT = 'adaptive_dashboard_layout';
const STORAGE_KEY_ORDER = 'adaptive_dashboard_order';
const defaultPanels = [
  { id: 'revenue', title: 'Revenue', size: 'large' },
  { id: 'users', title: 'Active Users', size: 'medium' },
  { id: 'latency', title: 'P95 Latency', size: 'medium' },
  { id: 'errors', title: 'Error Rate', size: 'medium' },
  { id: 'cpu', title: 'CPU Usage', size: 'small' },
  { id: 'memory', title: 'Memory', size: 'small' },
  { id: 'requests', title: 'Request Rate', size: 'large' },
  { id: 'uptime', title: 'Uptime', size: 'small' },
  { id: 'throughput', title: 'Throughput', size: 'medium' },
  { id: 'cost', title: 'Cloud Cost', size: 'small' },
  { id: 'apdex', title: 'Apdex Score', size: 'small' },
  { id: 'churn', title: 'Churn Rate', size: 'small' },
  { id: 'conversion', title: 'Conversion', size: 'small' },
  { id: 'sessions', title: 'Sessions', size: 'medium' },
  { id: 'bandwidth', title: 'Bandwidth', size: 'small' },
  { id: 'disk', title: 'Disk Usage', size: 'small' }
];
let panelStates = [];
let tracking = {};
let sessionStart = Date.now();
let interactionTotal = 0;
let recomputeCount = 0;
let observer = null;
let visibilityTimers = {};
let recomputeTimeout = null;
let dragState = null;
// ── Load/Save ──
function loadTracking() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY_TRACKING);
    if (raw) tracking = JSON.parse(raw);
  } catch(e) { tracking = {}; }
  for (const p of defaultPanels) {
    if (!tracking[p.id]) tracking[p.id] = { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0 };
  }
}
function saveTracking() {
  try { localStorage.setItem(STORAGE_KEY_TRACKING, JSON.stringify(tracking)); } catch(e) {}
}
function loadLayout() {
  try {
    const order = JSON.parse(localStorage.getItem(STORAGE_KEY_ORDER));
    if (order && Array.isArray(order) && order.length === defaultPanels.length) {
      const map = new Map(order.map((o,i) => [o.id, i]));
      const reordered = [...defaultPanels].sort((a,b) => (map.get(a.id)??99) - (map.get(b.id)??99));
      return reordered.map((p,i) => ({
        ...p,
        rank: 0,
        locked: order[i]?.locked || false,
        collapsed: order[i]?.collapsed || false,
        viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0
      }));
    }
  } catch(e) {}
  return defaultPanels.map((p,i) => ({...p, rank: i, locked: false, collapsed: false, viewCount:0, totalDuration:0, lastViewed:0, interactions:0}));
}
function saveLayoutOrder() {
  try {
    localStorage.setItem(STORAGE_KEY_ORDER, JSON.stringify(
      panelStates.map(p => ({ id: p.id, locked: p.locked, collapsed: p.collapsed }))
    ));
  } catch(e) {}
}
function saveAll() {
  saveTracking();
  saveLayoutOrder();
}
// ── Attention Ranking ──
function computeScore(t, now) {
  const freq = Math.log2(1 + t.viewCount);
  const dur = Math.log2(1 + t.totalDuration / 1000);
  const hoursSince = Math.max(0.01, (now - t.lastViewed) / 3600000);
  const recency = 1 / Math.sqrt(hoursSince);
  return (freq * 0.4 + dur * 0.35 + recency * 0.25) * 100;
}
function recomputeRanks() {
  const now = Date.now();
  const scored = panelStates.map((p, idx) => {
    const t = tracking[p.id] || { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0 };
    const score = computeScore(t, now);
    return { ...p, score, viewCount: t.viewCount, totalDuration: t.totalDuration, lastViewed: t.lastViewed, interactions: t.interactions };
  });
  const locked = scored.filter(p => p.locked);
  const unlocked = scored.filter(p => !p.locked);
  unlocked.sort((a, b) => b.score - a.score);
  const merged = [];
  let li = 0, ui = 0;
  const lockPositions = new Map();
  locked.forEach((p, i) => { lockPositions.set(p.id, i); });
  const origLockedOrder = panelStates.filter(p => p.locked).map(p => p.id);
  const lockedSorted = origLockedOrder.map(id => locked.find(p => p.id === id)).filter(Boolean);
  const newOrder = [];
  const usedIds = new Set();
  for (const lp of lockedSorted) { newOrder.push(lp); usedIds.add(lp.id); }
  for (const up of unlocked) { if (!usedIds.has(up.id)) newOrder.push(up); usedIds.add(up.id); }
  panelStates = newOrder.map((p, i) => ({...p, rank: i}));
  recomputeCount++;
  document.getElementById('recomputeCount').textContent = recomputeCount;
  saveAll();
}
// ── Compact Logic ──
function applyCompact() {
  if (panelStates.length < 4) return;
  const unlocked = panelStates.filter(p => !p.locked && !p.collapsed);
  const compactCount = Math.max(1, Math.floor(unlocked.length * 0.2));
  const toCompact = unlocked.slice(-compactCount);
  for (const p of toCompact) {
    p.collapsed = true;
  }
}
// ── Render ──
function renderPanel(p, index) {
  const now = Date.now();
  const metric = MockDataSource.getMetric(p.id);
  const sparkData = MockDataSource.getSparkline(p.id, 20);
  const change = MockDataSource.getChange(p.id);
  const changeClass = parseFloat(change) >= 0 ? 'up' : 'down';
  const maxSpark = Math.max(...sparkData, 0.01);
  const t = tracking[p.id] || { viewCount: 0, totalDuration: 0, interactions: 0 };
  const maxScore = Math.max(...panelStates.map(ps => ps.score || 0), 0.01);
  const scorePct = ((p.score || 0) / maxScore * 100).toFixed(0);
  let sizeClass = 'medium';
  if (p.collapsed) sizeClass = 'compact';
  else if (p.size === 'large') sizeClass = 'large';
  else if (p.size === 'small') sizeClass = 'small';
  const gridSpan = p.collapsed ? '' : (p.size === 'large' ? 'style="grid-column:span 2;grid-row:span 2"' : (p.size === 'small' ? 'style="grid-row:span 1"' : 'style="grid-column:span 1;grid-row:span 1"'));
  return `
    <div class="panel ${sizeClass} ${p.locked ? 'locked' : ''}" 
         data-panel-id="${p.id}" data-index="${index}"
         draggable="true"
         ${gridSpan}>
      <div class="panel-header">
        <span class="panel-title">${p.title}</span>
        <span class="panel-rank">#${p.rank + 1} · ${scorePct}%</span>
        <div class="panel-actions">
          <button class="${p.locked ? 'locked-btn' : ''}" onclick="toggleLock('${p.id}')" title="${p.locked ? 'Unlock' : 'Lock'} position">${p.locked ? '🔒' : '🔓'}</button>
          <button onclick="toggleCollapse('${p.id}')" title="${p.collapsed ? 'Expand' : 'Compact'}">${p.collapsed ? '⤢' : '⤡'}</button>
        </div>
      </div>
      <div class="panel-compact-preview">
        <span class="mini-val">${metric.formatted}</span>
        <span class="mini-label">${metric.unit}</span>
        <span class="metric-change ${changeClass}">${change >= 0 ? '▲' : '▼'} ${Math.abs(change)}%</span>
      </div>
      <div class="panel-body">
        <div class="metric-value">${metric.formatted}</div>
        <div class="metric-label">${metric.unit} · current value</div>
        <div class="metric-change ${changeClass}">${change >= 0 ? '▲' : '▼'} ${Math.abs(change)}% vs previous</div>
        <div class="sparkline">
          ${sparkData.map(v => `<div class="sparkline-bar" style="height:${(v/maxSpark*100).toFixed(1)}%"></div>`).join('')}
        </div>
        <div class="usage-bar">
          <div class="usage-bar-fill" style="width:${scorePct}%"></div>
        </div>
      </div>
      <div class="panel-footer">
        <span>👁 ${t.viewCount}</span>
        <span>🖱 ${t.interactions}</span>
        <span>⏱ ${(t.totalDuration/1000).toFixed(0)}s</span>
      </div>
    </div>`;
}
function renderAll() {
  const grid = document.getElementById('grid');
  grid.innerHTML = panelStates.map((p, i) => renderPanel(p, i)).join('');
  document.getElementById('panelCount').textContent = panelStates.length;
  attachPanelEvents();
}
// ── Intersection Observer for view tracking ──
function setupObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    const now = Date.now();
    for (const entry of entries) {
      const id = entry.target.dataset.panelId;
      if (!id) continue;
      if (entry.isIntersecting) {
        visibilityTimers[id] = now;
      } else {
        if (visibilityTimers[id]) {
          const duration = now - visibilityTimers[id];
          if (tracking[id]) tracking[id].totalDuration = (tracking[id].totalDuration || 0) + duration;
          delete visibilityTimers[id];
          saveTracking();
        }
      }
    }
  }, { threshold: 0.3 });
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
function finalizeVisibleDurations() {
  const now = Date.now();
  for (const [id, start] of Object.entries(visibilityTimers)) {
    if (tracking[id]) tracking[id].totalDuration = (tracking[id].totalDuration || 0) + (now - start);
  }
  visibilityTimers = {};
  saveTracking();
}
// ── Interaction Tracking ──
function trackInteraction(panelId, type) {
  if (!tracking[panelId]) return;
  tracking[panelId].interactions = (tracking[panelId].interactions || 0) + 1;
  tracking[panelId].lastViewed = Date.now();
  if (!tracking[panelId].viewCount) tracking[panelId].viewCount = 1;
  interactionTotal++;
  document.getElementById('interactionCount').textContent = interactionTotal;
  saveTracking();
  scheduleRecompute();
}
function scheduleRecompute() {
  clearTimeout(recomputeTimeout);
  recomputeTimeout = setTimeout(() => {
    finalizeVisibleDurations();
    recomputeRanks();
    applyCompact();
    renderAll();
    setupObserver();
  }, 2000);
}
// ── Panel Events ──
function attachPanelEvents() {
  const panels = document.querySelectorAll('.panel');
  panels.forEach(panel => {
    panel.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      const id = panel.dataset.panelId;
      if (!id) return;
      if (!tracking[id]) return;
      tracking[id].viewCount = (tracking[id].viewCount || 0) + 1;
      tracking[id].lastViewed = Date.now();
      interactionTotal++;
      document.getElementById('interactionCount').textContent = interactionTotal;
      saveTracking();
      scheduleRecompute();
    });
    panel.addEventListener('dragstart', (e) => {
      dragState = { id: panel.dataset.panelId, index: parseInt(panel.dataset.index) };
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', panel.dataset.panelId);
      const ghost = document.getElementById('dragGhost');
      ghost.textContent = panel.querySelector('.panel-title').textContent;
      ghost.style.display = 'block';
      requestAnimationFrame(() => {
        ghost.style.left = (e.clientX - 60) + 'px';
        ghost.style.top = (e.clientY - 20) + 'px';
      });
      setTimeout(() => { if (ghost) ghost.style.display = 'none'; }, 0);
    });
    panel.addEventListener('drag', (e) => {
      const ghost = document.getElementById('dragGhost');
      if (ghost && ghost.style.display !== 'none') {
        ghost.style.left = (e.clientX - 60) + 'px';
        ghost.style.top = (e.clientY - 20) + 'px';
      }
    });
    panel.addEventListener('dragend', (e) => {
      panel.classList.remove('dragging');
      const ghost = document.getElementById('dragGhost');
      if (ghost) ghost.style.display = 'none';
      document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
      if (!dragState) return;
      const dropTarget = document.elementFromPoint(e.clientX, e.clientY);
      const targetPanel = dropTarget?.closest('.panel');
      if (targetPanel && targetPanel.dataset.panelId !== dragState.id) {
        const targetIndex = parseInt(targetPanel.dataset.index);
        reorderPanels(dragState.index, targetIndex);
      }
      dragState = null;
    });
    panel.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      panel.classList.add('drag-over');
    });
    panel.addEventListener('dragleave', () => {
      panel.classList.remove('drag-over');
    });
    panel.addEventListener('drop', (e) => {
      e.preventDefault();
      panel.classList.remove('drag-over');
      const fromId = e.dataTransfer.getData('text/plain');
      const toId = panel.dataset.panelId;
      if (fromId === toId) return;
      const fromIndex = panelStates.findIndex(p => p.id === fromId);
      const toIndex = panelStates.findIndex(p => p.id === toId);
      if (fromIndex >= 0 && toIndex >= 0) {
        reorderPanels(fromIndex, toIndex);
      }
    });
  });
}
// ── Reorder ──
function reorderPanels(fromIndex, toIndex) {
  finalizeVisibleDurations();
  const item = panelStates.splice(fromIndex, 1)[0];
  panelStates.splice(toIndex, 0, item);
  panelStates.forEach((p, i) => { p.rank = i; });
  renderAll();
  setupObserver();
  saveLayoutOrder();
  showToast('Panel reordered');
  recomputeRanks();
  recomputeCount--;
}
// ── Toggle Functions ──
function toggleLock(panelId) {
  const p = panelStates.find(ps => ps.id === panelId);
  if (!p) return;
  p.locked = !p.locked;
  if (p.locked) p.collapsed = false;
  renderAll();
  setupObserver();
  saveAll();
  showToast(p.locked ? 'Panel locked' : 'Panel unlocked');
}
function toggleCollapse(panelId) {
  const p = panelStates.find(ps => ps.id === panelId);
  if (!p) return;
  if (p.locked && !p.collapsed) return;
  p.collapsed = !p.collapsed;
  renderAll();
  setupObserver();
  saveAll();
  showToast(p.collapsed ? 'Panel compacted' : 'Panel expanded');
}
function resetTracking() {
  for (const k of Object.keys(tracking)) {
    tracking[k] = { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0 };
  }
  interactionTotal = 0;
  document.getElementById('interactionCount').textContent = '0';
  saveTracking();
  recomputeRanks();
  applyCompact();
  renderAll();
  setupObserver();
  showToast('Tracking data reset');
}
function resetAll() {
  tracking = {};
  for (const p of defaultPanels) {
    tracking[p.id] = { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0 };
  }
  interactionTotal = 0;
  recomputeCount = 0;
  panelStates = defaultPanels.map((p,i) => ({...p, rank: i, locked: false, collapsed: false, score: 0, viewCount:0, totalDuration:0, lastViewed:0, interactions:0}));
  localStorage.removeItem(STORAGE_KEY_TRACKING);
  localStorage.removeItem(STORAGE_KEY_LAYOUT);
  localStorage.removeItem(STORAGE_KEY_ORDER);
  renderAll();
  setupObserver();
  document.getElementById('interactionCount').textContent = '0';
  document.getElementById('recomputeCount').textContent = '0';
  showToast('All reset to defaults');
}
function forceRecompute() {
  finalizeVisibleDurations();
  recomputeRanks();
  applyCompact();
  renderAll();
  setupObserver();
  showToast('Layout recomputed');
}
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timeout);
  t._timeout = setTimeout(() => t.classList.remove('show'), 2000);
}
// ── Periodic recompute ──
function periodicRecompute() {
  finalizeVisibleDurations();
  recomputeRanks();
  applyCompact();
  renderAll();
  setupObserver();
}
// ── Session timer ──
function updateSessionTimer() {
  const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
  const m = Math.floor(elapsed / 60);
  const s = elapsed % 60;
  document.getElementById('sessionTime').textContent = m + 'm ' + s + 's';
}
// ── Init ──
function init() {
  loadTracking();
  panelStates = loadLayout();
  const now = Date.now();
  panelStates.forEach((p, i) => {
    const t = tracking[p.id] || { viewCount: 0, totalDuration: 0, lastViewed: 0, interactions: 0 };
    p.score = computeScore(t, now);
    p.viewCount = t.viewCount;
    p.totalDuration = t.totalDuration;
    p.lastViewed = t.lastViewed;
    p.interactions = t.interactions;
    p.rank = i;
  });
  renderAll();
  setupObserver();
  updateSessionTimer();
  setInterval(updateSessionTimer, 10000);
  setInterval(periodicRecompute, 60000);
  document.getElementById('panelCount').textContent = panelStates.length;
}
document.addEventListener('DOMContentLoaded', init);
window.addEventListener('beforeunload', () => {
  finalizeVisibleDurations();
  saveAll();
});
// Global drag ghost tracking
document.addEventListener('dragover', (e) => {
  const ghost = document.getElementById('dragGhost');
  if (ghost && ghost.style.display !== 'none') {
    ghost.style.left = (e.clientX - 60) + 'px';
    ghost.style.top = (e.clientY - 20) + 'px';
  }
});
</script>
</body>
</html>
```