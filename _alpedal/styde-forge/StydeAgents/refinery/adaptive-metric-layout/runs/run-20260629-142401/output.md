```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d2e;
  --border: #2a2d3e;
  --text: #e0e0e0;
  --text-dim: #888;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.3);
  --compact-scale: 0.6;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg); color: var(--text);
  font-family: 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh; padding: 16px;
  user-select: none;
}
header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 16px; margin-bottom: 16px;
  background: var(--panel-bg); border: 1px solid var(--border); border-radius: 10px;
}
header h1 { font-size: 1.2rem; font-weight: 600; color: var(--accent); }
.header-actions { display: flex; gap: 10px; align-items: center; }
.header-actions button {
  padding: 6px 14px; border: 1px solid var(--border);
  background: var(--bg); color: var(--text); border-radius: 6px;
  cursor: pointer; font-size: 0.8rem; transition: var(--transition);
}
.header-actions button:hover { border-color: var(--accent); color: var(--accent); }
.idle-indicator {
  width: 8px; height: 8px; border-radius: 50%; background: #4caf50;
  transition: background 0.5s;
}
.idle-indicator.paused { background: #ff9800; }
.dashboard {
  display: grid;
  gap: 12px;
  transition: grid-template-columns 0.5s, grid-template-rows 0.5s;
}
.panel {
  background: var(--panel-bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px;
  transition: transform var(--transition), opacity var(--transition), border-color var(--transition);
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
}
.panel.top-rank { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.compact { transform: scale(var(--compact-scale)); opacity: 0.7; z-index: 0; }
.panel.compact:hover { transform: scale(0.66); opacity: 0.9; }
.panel.locked { border-left: 4px solid #ffd54f; }
.panel-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 10px;
}
.panel-title { font-weight: 600; font-size: 0.95rem; }
.panel-controls { display: flex; gap: 6px; }
.panel-controls button {
  background: none; border: 1px solid transparent; color: var(--text-dim);
  cursor: pointer; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px;
  transition: var(--transition);
}
.panel-controls button:hover { border-color: var(--border); color: var(--text); }
.panel-controls button.lock-active { color: #ffd54f; border-color: #ffd54f; }
.panel-content { flex: 1; }
.metric-value { font-size: 2rem; font-weight: 700; color: var(--accent); }
.metric-label { font-size: 0.8rem; color: var(--text-dim); margin-top: 4px; }
.chart-placeholder {
  width: 100%; height: 100%; min-height: 80px;
  background: linear-gradient(135deg, var(--border) 0%, transparent 100%);
  border-radius: 6px; display: flex; align-items: center; justify-content: center;
  color: var(--text-dim); font-size: 0.8rem;
}
.rank-badge {
  position: absolute; top: 8px; right: 8px;
  font-size: 0.65rem; color: var(--accent); opacity: 0.6;
}
.panel.compact .panel-content { overflow: hidden; }
.panel.compact .metric-value { font-size: 1.2rem; }
.panel.compact .chart-placeholder { min-height: 40px; font-size: 0.6rem; }
#more-section { display: none; margin-top: 16px; }
#more-section.visible { display: block; }
#more-section summary {
  cursor: pointer; padding: 10px 16px; background: var(--panel-bg);
  border: 1px solid var(--border); border-radius: 8px; color: var(--text-dim);
  font-size: 0.85rem;
}
#more-section summary:hover { color: var(--text); }
#more-grid { display: grid; gap: 8px; margin-top: 8px; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
#more-grid .panel { transform: scale(0.8); opacity: 0.6; }
#more-grid .panel:hover { transform: scale(0.85); opacity: 0.85; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Layout Dashboard</h1>
  <div class="header-actions">
    <span class="idle-indicator" id="idle-dot" title="Animation state"></span>
    <button onclick="resetData()" title="Clear all tracking data">Reset Data</button>
    <button onclick="forceRank()" title="Trigger immediate re-rank">Re-rank Now</button>
    <span style="font-size:0.75rem;color:var(--text-dim)" id="score-display"></span>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<details id="more-section"><summary id="more-summary">More panels</summary><div id="more-grid"></div></details>
<script>
const PANELS = [
  { id: 'cpu',     title: 'CPU Usage',     type: 'metric', value: '23%',  label: '4 cores active' },
  { id: 'memory',  title: 'Memory',         type: 'metric', value: '7.2GB',label: 'of 16GB used' },
  { id: 'requests',title: 'Requests/s',     type: 'metric', value: '1,247',label: '+12% vs last hour' },
  { id: 'latency', title: 'P95 Latency',    type: 'metric', value: '87ms', label: 'target: 100ms' },
  { id: 'errors',  title: 'Error Rate',     type: 'metric', value: '0.12%',label: 'below threshold' },
  { id: 'chart-a', title: 'Traffic Trend',  type: 'chart' },
  { id: 'chart-b', title: 'DB Connections', type: 'chart' },
  { id: 'chart-c', title: 'Cache Hit Rate', type: 'chart' },
  { id: 'chart-d', title: 'Queue Depth',    type: 'chart' },
  { id: 'chart-e', title: 'Disk I/O',       type: 'chart' },
  { id: 'alerts',  title: 'Active Alerts',  type: 'metric', value: '3',    label: '2 warnings, 1 critical' },
  { id: 'uptime',  title: 'Uptime',         type: 'metric', value: '14d',  label: 'since last deploy' },
];
const STORAGE_KEY = 'adaptive_dashboard_v1';
const IDLE_TIMEOUT = 2000;
const RERANK_INTERVAL = 5000;
const COMPACT_THRESHOLD = 0.3;
let attentionScores = {};
let locks = {};
let dirty = true;
let idle = false;
let idleSince = 0;
let rafId = null;
let lastRerank = 0;
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const state = JSON.parse(raw);
      attentionScores = state.attentionScores || {};
      locks = state.locks || {};
    }
  } catch(e) {}
  PANELS.forEach(p => {
    if (!attentionScores[p.id]) attentionScores[p.id] = { freq: 0, duration: 0, lastAccess: 0 };
  });
}
function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ attentionScores, locks }));
}
function trackEvent(panelId, type) {
  const s = attentionScores[panelId];
  if (!s) return;
  s.freq++;
  s.lastAccess = Date.now();
  if (type === 'expand') s.duration += 5;
  dirty = true;
  saveState();
}
function trackView(panelId, visible, now) {
  if (!visible) return;
  const s = attentionScores[panelId];
  if (!s) return;
  s.duration += 0.1;
  s.lastAccess = now || Date.now();
}
function computeRank(panelId, now) {
  const s = attentionScores[panelId];
  if (!s) return 0;
  const age = Math.max(0, (now || Date.now()) - s.lastAccess) / 1000;
  const recency = 1 / (1 + age / 3600);
  return (s.freq * 0.4 + s.duration * 0.35 + recency * 0.25) * 100;
}
function getSortedPanels() {
  const now = Date.now();
  return [...PANELS].map(p => ({ ...p, rank: computeRank(p.id, now) }))
    .sort((a, b) => b.rank - a.rank);
}
function renderDashboard() {
  const sorted = getSortedPanels();
  const now = Date.now();
  const maxRank = sorted[0]?.rank || 1;
  const dashboard = document.getElementById('dashboard');
  const moreGrid = document.getElementById('more-grid');
  const moreSection = document.getElementById('more-section');
  const moreSummary = document.getElementById('more-summary');
  const activePanels = sorted.filter(p => {
    if (locks[p.id]) return true;
    return (p.rank / maxRank) >= COMPACT_THRESHOLD;
  });
  const compactPanels = sorted.filter(p => {
    if (locks[p.id]) return false;
    return (p.rank / maxRank) < COMPACT_THRESHOLD;
  });
  const colCount = Math.min(activePanels.length, 4) || 1;
  dashboard.style.gridTemplateColumns = `repeat(${colCount}, 1fr)`;
  dashboard.innerHTML = '';
  activePanels.forEach((p, i) => {
    const el = createPanelElement(p, i === 0, false);
    dashboard.appendChild(el);
  });
  if (compactPanels.length > 0) {
    moreGrid.innerHTML = '';
    compactPanels.forEach(p => {
      moreGrid.appendChild(createPanelElement(p, false, true));
    });
    moreSummary.textContent = `More panels (${compactPanels.length})`;
    moreSection.classList.add('visible');
  } else {
    moreSection.classList.remove('visible');
  }
  document.getElementById('score-display').textContent =
    activePanels.map(p => `${p.title}:${p.rank.toFixed(1)}`).join(' | ');
  dirty = false;
  lastRerank = now;
}
function createPanelElement(p, isTop, isCompact) {
  const div = document.createElement('div');
  div.className = 'panel';
  if (isTop && !isCompact) div.classList.add('top-rank');
  if (isCompact) div.classList.add('compact');
  if (locks[p.id]) div.classList.add('locked');
  div.dataset.panelId = p.id;
  div.innerHTML = `
    <div class="panel-header">
      <span class="panel-title">${p.title}</span>
      <div class="panel-controls">
        <button class="${locks[p.id] ? 'lock-active' : ''}" data-action="lock" data-panel="${p.id}">
          ${locks[p.id] ? 'unlock' : 'lock'}
        </button>
      </div>
    </div>
    <div class="panel-content">
      ${p.type === 'metric'
        ? `<div class="metric-value">${p.value}</div><div class="metric-label">${p.label}</div>`
        : `<div class="chart-placeholder">chart: ${p.title}</div>`}
    </div>
    <div class="rank-badge">${p.rank.toFixed(1)}</div>`;
  div.addEventListener('click', () => trackEvent(p.id, 'click'));
  div.addEventListener('mouseenter', () => trackEvent(p.id, 'hover'));
  div.querySelector('[data-action="lock"]')?.addEventListener('click', (e) => {
    e.stopPropagation();
    locks[p.id] = !locks[p.id];
    dirty = true;
    saveState();
    renderDashboard();
  });
  return div;
}
function forceRank() { dirty = true; renderDashboard(); }
function resetData() {
  attentionScores = {};
  locks = {};
  PANELS.forEach(p => { attentionScores[p.id] = { freq: 0, duration: 0, lastAccess: 0 }; });
  dirty = true;
  saveState();
  renderDashboard();
}
function onActivity() {
  idle = false;
  idleSince = 0;
  document.getElementById('idle-dot').classList.remove('paused');
  if (!rafId) startLoop();
}
function startLoop() {
  if (rafId) return;
  function tick(ts) {
    if (idle && idleSince > 0 && (ts - idleSince) > IDLE_TIMEOUT) {
      rafId = null;
      document.getElementById('idle-dot').classList.add('paused');
      return;
    }
    let anyVisible = false;
    document.querySelectorAll('.panel').forEach(el => {
      const rect = el.getBoundingClientRect();
      const visible = rect.top < window.innerHeight && rect.bottom > 0 &&
                      rect.left < window.innerWidth && rect.right > 0;
      if (visible) {
        anyVisible = true;
        trackView(el.dataset.panelId, true, ts);
      }
    });
    if (!anyVisible && !idle) {
      idle = true;
      idleSince = ts;
    }
    if (anyVisible && idle) {
      idle = false;
      idleSince = 0;
    }
    if (dirty && (ts - lastRerank) > RERANK_INTERVAL) {
      renderDashboard();
    }
    rafId = requestAnimationFrame(tick);
  }
  rafId = requestAnimationFrame(tick);
}
['mousemove','keydown','scroll','touchstart'].forEach(evt =>
  document.addEventListener(evt, onActivity, { passive: true }));
loadState();
renderDashboard();
startLoop();
</script>
</body>
</html>
```