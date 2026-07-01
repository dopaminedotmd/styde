<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --warn: #f0a040;
  --compact-bg: #141720;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.4,0,0.2,1);
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 16px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}
h1 { font-size: 1.3rem; font-weight: 600; letter-spacing: -0.01em; }
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
.btn {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: var(--transition);
}
.btn:hover { border-color: var(--accent); background: var(--accent-glow); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  transition: var(--transition);
}
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: var(--radius);
  padding: 16px;
  transition: var(--transition);
  position: relative;
  cursor: grab;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.dragging { opacity: 0.7; cursor: grabbing; z-index: 10; }
.panel.high-rank { grid-column: span 2; grid-row: span 2; }
.panel.medium-rank { grid-column: span 1; grid-row: span 1; }
.panel.compact {
  grid-column: span 1;
  grid-row: span 1;
  padding: 10px 14px;
  background: var(--compact-bg);
  max-height: 90px;
  overflow: hidden;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: block; }
.panel.compact .metric-value { font-size: 1rem; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.panel-title { font-size: 0.85rem; font-weight: 600; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.04em; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  font-size: 0.75rem;
  padding: 3px 6px;
  border-radius: 4px;
  transition: var(--transition);
}
.panel-actions button:hover { background: var(--panel-border); color: var(--text); }
.panel-actions button.locked { color: var(--warn); }
.panel-actions button.compacted { color: var(--accent); }
.metric-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; }
.metric-label { font-size: 0.78rem; color: var(--text-dim); }
.panel-preview { display: none; font-size: 0.78rem; color: var(--text-dim); }
.sparkline { display: flex; gap: 2px; align-items: flex-end; height: 40px; }
.sparkline-bar { background: var(--accent); border-radius: 2px 2px 0 0; flex: 1; min-width: 4px; transition: height 0.3s; }
.stats-bar {
  display: flex;
  gap: 12px;
  font-size: 0.7rem;
  color: var(--text-dim);
  margin-top: 4px;
}
.stats-bar span { display: flex; align-items: center; gap: 3px; }
.rank-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: var(--accent);
  color: #fff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  z-index: 2;
  transition: var(--transition);
}
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: "LOCKED";
  position: absolute;
  top: 8px;
  right: 44px;
  font-size: 0.6rem;
  color: var(--warn);
  font-weight: 700;
  letter-spacing: 0.1em;
}
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--panel-bg);
  border: 1px solid var(--accent);
  color: var(--text);
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.8rem;
  z-index: 100;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}
.toast.show { opacity: 1; }
.layout-mode-indicator {
  font-size: 0.7rem;
  color: var(--text-dim);
  padding: 4px 10px;
  border-radius: 12px;
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <span class="layout-mode-indicator" id="modeIndicator">auto</span>
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btnForceLayout" title="Force recalculation now">Recalc</button>
    <button class="btn" id="btnExport" title="Export tracking data">Export</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
// --- Adaptive Layout Engine ---
const STORAGE_KEY = 'adaptive_dashboard_v1';
const DECAY_HALF_LIFE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
const MIN_VIEW_DURATION_MS = 500;
const COMPACT_THRESHOLD_PERCENTILE = 0.35;
const HIGH_RANK_THRESHOLD_PERCENTILE = 0.75;
const RECALC_INTERVAL_MS = 30000;
const METRICS = [
  { id: 'revenue',    title: 'Revenue',       value: '$84,254', change: '+12.3%', color: '#6c8cff' },
  { id: 'users',      title: 'Active Users',  value: '12,847',  change: '+8.1%',  color: '#50c878' },
  { id: 'conversion', title: 'Conversion',    value: '3.24%',   change: '-0.4%',  color: '#f0a040' },
  { id: 'churn',      title: 'Churn Rate',    value: '2.1%',    change: '-0.3%',  color: '#ff6b6b' },
  { id: 'latency',    title: 'P95 Latency',   value: '142ms',   change: '+5ms',   color: '#c084fc' },
  { id: 'errors',     title: 'Error Rate',    value: '0.12%',   change: '-0.02%', color: '#ff6b6b' },
  { id: 'sessions',   title: 'Sessions',      value: '3,421',   change: '+15.2%', color: '#50c878' },
  { id: 'bounce',     title: 'Bounce Rate',   value: '42.8%',   change: '+1.1%',  color: '#f0a040' },
  { id: 'nps',        title: 'NPS Score',     value: '72',      change: '+3',     color: '#6c8cff' },
  { id: 'cpu',        title: 'CPU Usage',     value: '67%',     change: '-5%',    color: '#c084fc' },
  { id: 'memory',     title: 'Memory',        value: '8.2 GB',  change: '+0.3GB', color: '#f0a040' },
  { id: 'uptime',     title: 'Uptime',        value: '99.97%',  change: '0%',     color: '#50c878' },
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const state = JSON.parse(raw);
    if (!state || typeof state !== 'object') return null;
    return state;
  } catch (e) {
    console.warn('localStorage read failed, resetting state', e);
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
    return null;
  }
}
function saveState(state) {
  try {
    const serialized = JSON.stringify(state);
    localStorage.setItem(STORAGE_KEY, serialized);
    return true;
  } catch (e) {
    if (e.name === 'QuotaExceededError' || e.code === 22) {
      state.events = state.events.slice(-500);
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); return true; } catch (_) {}
    }
    showToast('Storage full — tracking continues in memory only');
    return false;
  }
}
let state = loadState() || {
  events: [],
  locks: {},
  manualCompacts: {},
  manualPositions: {},
  lastLayoutTs: 0,
};
let viewStartTimes = {};
let observer = null;
let dragging = null;
let dragClone = null;
let dragStartX = 0;
let dragStartY = 0;
let recalcTimer = null;
let saveTimer = null;
function now() { return Date.now(); }
function track(panelId, type, detail) {
  state.events.push({ panelId, type, ts: now(), detail: detail || {} });
  debouncedSave();
}
function viewStart(panelId) {
  viewStartTimes[panelId] = now();
}
function viewEnd(panelId) {
  const start = viewStartTimes[panelId];
  if (!start) return;
  const duration = now() - start;
  if (duration >= MIN_VIEW_DURATION_MS) {
    track(panelId, 'view', { durationMs: duration });
  }
  delete viewStartTimes[panelId];
}
function debouncedSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => saveState(state), 1000);
}
function showToast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2500);
}
// --- Scoring Engine ---
function computeScores() {
  const nowTs = now();
  const panelScores = {};
  const panelIds = METRICS.map(m => m.id);
  panelIds.forEach(id => { panelScores[id] = { frequency: 0, totalDuration: 0, recency: 0, score: 0 }; });
  const relevantEvents = state.events.filter(e => {
    if (!panelIds.includes(e.panelId)) return false;
    if (e.type === 'view') return (e.detail?.durationMs || 0) >= MIN_VIEW_DURATION_MS;
    return e.type === 'click' || e.type === 'expand' || e.type === 'collapse' || e.type === 'lock' || e.type === 'unlock';
  });
  relevantEvents.forEach(e => {
    const s = panelScores[e.panelId];
    s.frequency++;
    if (e.type === 'view') {
      s.totalDuration += e.detail.durationMs || 0;
    }
    const age = nowTs - e.ts;
    const recencyWeight = Math.pow(0.5, age / DECAY_HALF_LIFE_MS);
    if (recencyWeight > s.recency) s.recency = recencyWeight;
  });
  panelIds.forEach(id => {
    const s = panelScores[id];
    const freqNorm = Math.min(s.frequency / Math.max(1, relevantEvents.length / panelIds.length), 3);
    const durNorm = Math.log1p(s.totalDuration / 1000);
    const score = freqNorm * durNorm * (0.3 + 0.7 * s.recency);
    s.score = Math.round(score * 1000) / 1000;
  });
  const scores = Object.values(panelScores).map(s => s.score).filter(s => s > 0).sort((a, b) => a - b);
  if (scores.length === 0) {
    panelIds.forEach(id => { panelScores[id].rank = 0; panelScores[id].tier = 'medium'; });
    return panelScores;
  }
  const compactCutoff = scores[Math.floor(scores.length * COMPACT_THRESHOLD_PERCENTILE)] || 0;
  const highCutoff = scores[Math.floor(scores.length * HIGH_RANK_THRESHOLD_PERCENTILE)] || 0;
  const scored = panelIds.map(id => ({ id, score: panelScores[id].score })).sort((a, b) => b.score - a.score);
  scored.forEach((item, i) => {
    panelScores[item.id].rank = i + 1;
    if (item.score >= highCutoff && item.score > 0) panelScores[item.id].tier = 'high';
    else if (item.score <= compactCutoff && scores.length > 3) panelScores[item.id].tier = 'compact';
    else panelScores[item.id].tier = 'medium';
  });
  return panelScores;
}
// --- Rendering ---
function renderDashboard() {
  const scores = computeScores();
  const container = document.getElementById('dashboard');
  const existingPanels = {};
  container.querySelectorAll('.panel').forEach(p => { existingPanels[p.dataset.panelId] = p; });
  const orderedIds = Object.entries(scores)
    .sort((a, b) => {
      if (state.locks[a[0]] && !state.locks[b[0]]) return -1;
      if (!state.locks[a[0]] && state.locks[b[0]]) return 1;
      if (state.locks[a[0]] && state.locks[b[0]]) {
        const pa = state.manualPositions[a[0]] || 999;
        const pb = state.manualPositions[b[0]] || 999;
        return pa - pb;
      }
      return a[1].rank - b[1].rank;
    })
    .map(e => e[0]);
  const fragment = document.createDocumentFragment();
  orderedIds.forEach(id => {
    let panel = existingPanels[id];
    if (!panel) {
      panel = createPanelElement(id);
    } else {
      delete existingPanels[id];
    }
    const score = scores[id];
    const isLocked = !!state.locks[id];
    const isCompact = state.manualCompacts[id] !== undefined ? state.manualCompacts[id] : (score.tier === 'compact');
    panel.className = 'panel';
    if (isLocked) panel.classList.add('locked');
    if (isCompact) panel.classList.add('compact');
    else if (score.tier === 'high') panel.classList.add('high-rank');
    else panel.classList.add('medium-rank');
    const rankBadge = panel.querySelector('.rank-badge');
    if (rankBadge) rankBadge.textContent = score.rank || '—';
    const lockBtn = panel.querySelector('.btn-lock');
    if (lockBtn) {
      lockBtn.classList.toggle('locked', isLocked);
      lockBtn.textContent = isLocked ? 'unlock' : 'lock';
    }
    const compactBtn = panel.querySelector('.btn-compact');
    if (compactBtn) {
      compactBtn.classList.toggle('compacted', isCompact);
      compactBtn.textContent = isCompact ? 'expand' : 'compact';
    }
    fragment.appendChild(panel);
  });
  Object.values(existingPanels).forEach(p => p.remove());
  container.appendChild(fragment);
  state.lastLayoutTs = now();
  document.getElementById('modeIndicator').textContent = 'auto';
  setupIntersectionObserver();
}
function createPanelElement(id) {
  const metric = METRICS.find(m => m.id === id);
  if (!metric) return document.createElement('div');
  const panel = document.createElement('div');
  panel.className = 'panel medium-rank';
  panel.dataset.panelId = id;
  panel.draggable = true;
  panel.innerHTML = `
    <span class="rank-badge">—</span>
    <div class="panel-header">
      <span class="panel-title">${metric.title}</span>
      <div class="panel-actions">
        <button class="btn-compact" title="Toggle compact mode">compact</button>
        <button class="btn-lock" title="Lock position">lock</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="metric-value" style="color:${metric.color}">${metric.value}</div>
      <div class="metric-label">${metric.change} vs last period</div>
      <div class="sparkline">${generateSparkline(20, 40, 90)}</div>
      <div class="stats-bar">
        <span>views 0</span>
        <span>clicks 0</span>
        <span>time 0s</span>
      </div>
    </div>
    <div class="panel-preview">${metric.value} ${metric.change} — click to expand</div>
  `;
  panel.addEventListener('click', (e) => {
    if (e.target.closest('button')) return;
    track(id, 'click', {});
    updateStatsBar(panel, id);
  });
  panel.addEventListener('dragstart', handleDragStart);
  panel.addEventListener('dragend', handleDragEnd);
  panel.addEventListener('dragover', e => e.preventDefault());
  panel.querySelector('.btn-lock').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleLock(id);
  });
  panel.querySelector('.btn-compact').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleCompact(id);
  });
  return panel;
}
function generateSparkline(min, max, count) {
  let html = '';
  for (let i = 0; i < count; i++) {
    const h = min + Math.random() * (max - min);
    html += `<div class="sparkline-bar" style="height:${h}%"></div>`;
  }
  return html;
}
function updateStatsBar(panel, panelId) {
  const views = state.events.filter(e => e.panelId === panelId && e.type === 'view').length;
  const clicks = state.events.filter(e => e.panelId === panelId && e.type === 'click').length;
  const totalMs = state.events
    .filter(e => e.panelId === panelId && e.type === 'view')
    .reduce((sum, e) => sum + (e.detail?.durationMs || 0), 0);
  const bar = panel.querySelector('.stats-bar');
  if (bar) bar.innerHTML = `<span>views ${views}</span><span>clicks ${clicks}</span><span>time ${Math.round(totalMs / 1000)}s</span>`;
}
function toggleLock(panelId) {
  if (state.locks[panelId]) {
    delete state.locks[panelId];
    delete state.manualPositions[panelId];
    track(panelId, 'unlock', {});
  } else {
    state.locks[panelId] = true;
    state.manualPositions[panelId] = Object.keys(state.locks).length;
    track(panelId, 'lock', {});
  }
  saveState(state);
  renderDashboard();
  showToast(state.locks[panelId] ? `${panelId} locked` : `${panelId} unlocked`);
}
function toggleCompact(panelId) {
  const current = state.manualCompacts[panelId];
  if (current !== undefined) {
    delete state.manualCompacts[panelId];
    track(panelId, 'expand', {});
  } else {
    state.manualCompacts[panelId] = true;
    track(panelId, 'collapse', {});
  }
  saveState(state);
  renderDashboard();
}
function handleDragStart(e) {
  const panel = e.target.closest('.panel');
  if (!panel) return;
  dragging = panel;
  dragStartX = e.clientX;
  dragStartY = e.clientY;
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panel.dataset.panelId);
}
function handleDragEnd(e) {
  if (!dragging) return;
  dragging.classList.remove('dragging');
  const container = document.getElementById('dashboard');
  const panels = [...container.querySelectorAll('.panel:not(.dragging)')];
  const targetX = e.clientX;
  const targetY = e.clientY;
  let dropIndex = panels.length;
  for (let i = 0; i < panels.length; i++) {
    const rect = panels[i].getBoundingClientRect();
    if (targetY < rect.top + rect.height / 2) {
      dropIndex = i;
      break;
    }
  }
  const draggedId = dragging.dataset.panelId;
  if (!state.locks[draggedId]) {
    state.locks[draggedId] = true;
  }
  state.manualPositions[draggedId] = dropIndex;
  track(draggedId, 'move', { position: dropIndex });
  saveState(state);
  const sibling = panels[dropIndex];
  if (sibling) {
    container.insertBefore(dragging, sibling);
  } else {
    container.appendChild(dragging);
  }
  // Re-render all locked positions
  const locked = Object.entries(state.locks).filter(([id, v]) => v).sort((a, b) => {
    return (state.manualPositions[a[0]] || 999) - (state.manualPositions[b[0]] || 999);
  });
  locked.forEach(([id], i) => {
    state.manualPositions[id] = i;
  });
  document.getElementById('modeIndicator').textContent = 'manual';
  dragging = null;
}
// --- Intersection Observer for view tracking ---
function setupIntersectionObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
        viewStart(panelId);
      } else {
        viewEnd(panelId);
      }
    });
  }, { threshold: [0, 0.5, 1.0] });
  document.querySelectorAll('.panel').forEach(p => observer.observe(p));
}
// --- Auto-recalc ---
function startAutoRecalc() {
  recalcTimer = setInterval(() => {
    const scores = computeScores();
    let changed = false;
    METRICS.forEach(m => {
      const panel = document.querySelector(`.panel[data-panel-id="${m.id}"]`);
      if (!panel) return;
      const score = scores[m.id];
      const isLocked = !!state.locks[m.id];
      if (isLocked) return;
      const isCompact = state.manualCompacts[m.id] !== undefined ? state.manualCompacts[m.id] : (score.tier === 'compact');
      const wasCompact = panel.classList.contains('compact');
      const wasHigh = panel.classList.contains('high-rank');
      if (wasCompact !== isCompact || wasHigh !== (score.tier === 'high' && !isCompact)) {
        changed = true;
      }
    });
    if (changed) renderDashboard();
  }, RECALC_INTERVAL_MS);
}
// --- Controls ---
document.getElementById('btnReset').addEventListener('click', () => {
  state = { events: [], locks: {}, manualCompacts: {}, manualPositions: {}, lastLayoutTs: 0 };
  try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
  viewStartTimes = {};
  renderDashboard();
  showToast('All tracking data reset');
});
document.getElementById('btnForceLayout').addEventListener('click', () => {
  renderDashboard();
  showToast('Layout recalculated');
});
document.getElementById('btnExport').addEventListener('click', () => {
  const scores = computeScores();
  const exportData = {
    exportedAt: new Date().toISOString(),
    state,
    scores: Object.fromEntries(Object.entries(scores).map(([id, s]) => [id, { rank: s.rank, tier: s.tier, score: s.score }])),
  };
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `dashboard-export-${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Exported');
});
// --- Init ---
renderDashboard();
startAutoRecalc();
// Re-render on visibility change to re-trigger observer
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    document.querySelectorAll('.panel').forEach(p => {
      const id = p.dataset.panelId;
      if (id) viewEnd(id);
    });
    renderDashboard();
  }
});
</script>
</body>
</html>