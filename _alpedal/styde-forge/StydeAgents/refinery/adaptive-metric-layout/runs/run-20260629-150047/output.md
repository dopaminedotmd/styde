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
    --surface2: #22262f;
    --border: #2a2e3a;
    --text: #e1e4eb;
    --text2: #8b90a0;
    --accent: #6c8aff;
    --accent2: #4ade80;
    --warn: #f59e0b;
    --compact-scale: 0.55;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
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
  .toolbar-title {
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.5px;
    margin-right: auto;
  }
  .toolbar-btn {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text2);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.15s;
  }
  .toolbar-btn:hover { color: var(--text); border-color: var(--accent); }
  .toolbar-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .grid {
    display: grid;
    gap: 10px;
    padding: 12px;
    transition: all 0.35s ease;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(140px, auto);
  }
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.35s ease, grid-column 0.35s ease, grid-row 0.35s ease;
    cursor: grab;
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 140px;
  }
  .panel:active { cursor: grabbing; }
  .panel.dragging {
    opacity: 0.7;
    box-shadow: 0 0 0 2px var(--accent);
    z-index: 50;
    transition: none;
  }
  .panel.compact {
    transform: scale(var(--compact-scale));
    transform-origin: center center;
    opacity: 0.7;
    min-height: 80px;
  }
  .panel.compact .panel-body { padding: 8px; }
  .panel.compact .metric-value { font-size: 18px; }
  .panel.compact .chart-area { height: 50px; }
  .panel.locked { border-color: var(--warn); }
  .panel-header {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 10px;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    color: var(--text2);
    user-select: none;
  }
  .panel-header .title { flex: 1; }
  .panel-header .rank-badge {
    font-size: 10px;
    background: var(--accent);
    color: #fff;
    padding: 2px 7px;
    border-radius: 10px;
    font-weight: 700;
  }
  .panel-header .lock-icon {
    color: var(--warn);
    font-size: 12px;
    display: none;
  }
  .panel.locked .panel-header .lock-icon { display: inline; }
  .panel-controls {
    display: flex;
    gap: 4px;
  }
  .panel-btn {
    background: none;
    border: none;
    color: var(--text2);
    cursor: pointer;
    font-size: 14px;
    padding: 2px 5px;
    border-radius: 4px;
    line-height: 1;
    opacity: 0;
    transition: opacity 0.15s;
  }
  .panel:hover .panel-btn { opacity: 1; }
  .panel-btn:hover { background: var(--border); color: var(--text); }
  .panel-btn.locked-btn { opacity: 1; color: var(--warn); }
  .panel-body {
    flex: 1;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .metric-value {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1;
  }
  .metric-label {
    font-size: 11px;
    color: var(--text2);
  }
  .metric-change {
    font-size: 12px;
    font-weight: 600;
  }
  .metric-change.up { color: var(--accent2); }
  .metric-change.down { color: #ef4444; }
  .chart-area {
    flex: 1;
    min-height: 60px;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .chart-area canvas {
    width: 100%;
    height: 100%;
    display: block;
  }
  .spark-bars {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 100%;
    padding: 4px 0;
  }
  .spark-bar {
    flex: 1;
    background: var(--accent);
    border-radius: 2px 2px 0 0;
    min-width: 4px;
    transition: height 0.4s ease;
    opacity: 0.7;
  }
  .spark-bar.active { opacity: 1; }
  .drag-over {
    box-shadow: 0 0 0 2px var(--accent2);
  }
  .drag-placeholder {
    border: 2px dashed var(--border);
    border-radius: 10px;
    background: var(--surface2);
    grid-column: span 1;
    grid-row: span 1;
  }
  .stats-bar {
    display: flex;
    gap: 16px;
    padding: 6px 16px;
    font-size: 10px;
    color: var(--text2);
    border-top: 1px solid var(--border);
    background: var(--surface);
  }
  .stats-bar span { white-space: nowrap; }
  .stats-bar .val { color: var(--accent); font-weight: 600; }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .panel { animation: fadeIn 0.3s ease; }
</style>
</head>
<body>
<div class="toolbar">
  <span class="toolbar-title">Adaptive Layout</span>
  <button class="toolbar-btn active" id="btnAuto" onclick="setMode('auto')">Auto</button>
  <button class="toolbar-btn" id="btnManual" onclick="setMode('manual')">Manual</button>
  <button class="toolbar-btn" onclick="resetAll()">Reset</button>
  <button class="toolbar-btn" onclick="exportData()">Export</button>
  <span style="font-size:11px;color:var(--text2)">Drag panels to reorder. Lock to pin.</span>
</div>
<div class="grid" id="grid"></div>
<div class="stats-bar" id="statsBar">
  <span>Sessions: <span class="val" id="statSessions">1</span></span>
  <span>Interactions: <span class="val" id="statInteractions">0</span></span>
  <span>Avg attention: <span class="val" id="statAvg">0</span></span>
  <span>Top panel: <span class="val" id="statTop">-</span></span>
</div>
<script>
const PANELS = [
  { id: 'revenue',    title: 'Revenue',        metric: 'revenue',    value: 84720 },
  { id: 'users',      title: 'Active Users',   metric: 'users',      value: 12453 },
  { id: 'conversion', title: 'Conversion',     metric: 'conversion', value: 3.24  },
  { id: 'churn',      title: 'Churn Rate',     metric: 'churn',      value: 1.87  },
  { id: 'latency',    title: 'API Latency',    metric: 'latency',    value: 42    },
  { id: 'errors',     title: 'Error Rate',     metric: 'errors',     value: 0.12  },
  { id: 'storage',    title: 'Storage',        metric: 'storage',    value: 67.4  },
  { id: 'bandwidth',  title: 'Bandwidth',      metric: 'bandwidth',  value: 892   },
  { id: 'cpu',        title: 'CPU Usage',      metric: 'cpu',        value: 34.8  },
  { id: 'memory',     title: 'Memory',         metric: 'memory',     value: 62.1  },
  { id: 'requests',   title: 'Requests/min',   metric: 'requests',   value: 3421  },
  { id: 'uptime',     title: 'Uptime %',       metric: 'uptime',     value: 99.97 },
];
const DECAY_HALF = 7 * 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD = 0.15;
const SIZE_CLASSES = ['xlarge', 'large', 'medium', 'small', 'compact'];
let state = {
  mode: 'auto',
  panels: {},
  order: [],
  nextId: 0,
};
function loadState() {
  try {
    const raw = localStorage.getItem('adaptive_layout_v1');
    if (raw) {
      const saved = JSON.parse(raw);
      state.mode = saved.mode || 'auto';
      state.order = saved.order || [];
      state.panels = {};
      for (const p of PANELS) {
        const sp = saved.panels && saved.panels[p.id];
        state.panels[p.id] = {
          locked: sp ? sp.locked : false,
          overrideSpan: sp ? sp.overrideSpan : null,
          attention: sp ? (sp.attention || 0) : 0,
          durationMs: sp ? (sp.durationMs || 0) : 0,
          interactions: sp ? (sp.interactions || 0) : 0,
          lastViewed: sp ? (sp.lastViewed || 0) : 0,
          history: sp ? (sp.history || []) : [],
          collapsed: sp ? sp.collapsed : false,
        };
      }
      if (!state.order.length) state.order = PANELS.map(p => p.id);
    }
  } catch(e) {}
  if (!state.order.length) {
    state.order = PANELS.map(p => p.id);
    for (const p of PANELS) {
      state.panels[p.id] = {
        locked: false, overrideSpan: null, attention: 0,
        durationMs: 0, interactions: 0, lastViewed: 0,
        history: [], collapsed: false,
      };
    }
  }
}
function saveState() {
  const out = {
    mode: state.mode,
    order: state.order,
    panels: {},
  };
  for (const [id, p] of Object.entries(state.panels)) {
    out.panels[id] = {
      locked: p.locked,
      overrideSpan: p.overrideSpan,
      attention: p.attention,
      durationMs: p.durationMs,
      interactions: p.interactions,
      lastViewed: p.lastViewed,
      history: p.history.slice(-120),
      collapsed: p.collapsed,
    };
  }
  localStorage.setItem('adaptive_layout_v1', JSON.stringify(out));
}
function applyDecay(panel) {
  const now = Date.now();
  const age = now - panel.lastViewed;
  if (age > DECAY_HALF) {
    const factor = Math.exp(-Math.LN2 * age / DECAY_HALF);
    panel.attention *= factor;
    panel.durationMs *= factor;
    panel.interactions = Math.max(0, Math.round(panel.interactions * factor));
  }
}
function computeScore(panel) {
  applyDecay(panel);
  const durMin = Math.max(panel.durationMs / 60000, 0.1);
  const intCount = Math.max(panel.interactions, 1);
  const recency = panel.lastViewed
    ? Math.max(0.1, 1 - (Date.now() - panel.lastViewed) / DECAY_HALF)
    : 0.1;
  return durMin * Math.log2(intCount + 1) * recency;
}
function rankPanels() {
  const scored = state.order.map(id => {
    const panel = state.panels[id];
    return { id, score: computeScore(panel), locked: panel.locked };
  });
  const locked = scored.filter(s => s.locked);
  const unlocked = scored.filter(s => !s.locked).sort((a, b) => b.score - a.score);
  const maxScore = unlocked.length ? Math.max(...unlocked.map(s => s.score)) : 1;
  const ranked = [...locked, ...unlocked];
  const result = [];
  for (let i = 0; i < ranked.length; i++) {
    const r = ranked[i];
    const normalized = maxScore > 0 ? r.score / maxScore : 0;
    let sizeClass;
    if (normalized >= 0.8) sizeClass = 'xlarge';
    else if (normalized >= 0.6) sizeClass = 'large';
    else if (normalized >= 0.4) sizeClass = 'medium';
    else if (normalized >= COMPACT_THRESHOLD) sizeClass = 'small';
    else sizeClass = 'compact';
    result.push({ id: r.id, score: r.score, rank: i + 1, sizeClass, locked: r.locked });
  }
  return result;
}
function getSpan(sizeClass) {
  const map = {
    xlarge: { col: 2, row: 2 },
    large:  { col: 2, row: 1 },
    medium: { col: 1, row: 1 },
    small:  { col: 1, row: 1 },
    compact:{ col: 1, row: 1 },
  };
  return map[sizeClass] || { col: 1, row: 1 };
}
function formatValue(panelId, value) {
  if (panelId === 'conversion' || panelId === 'churn' || panelId === 'errors' || panelId === 'uptime') {
    return value.toFixed(2) + '%';
  }
  if (panelId === 'latency') return value + 'ms';
  if (panelId === 'storage') return value + 'GB';
  if (panelId === 'bandwidth') return value + 'Mbps';
  if (panelId === 'cpu' || panelId === 'memory') return value.toFixed(1) + '%';
  if (panelId === 'requests') return value.toLocaleString();
  if (panelId === 'revenue') return '$' + value.toLocaleString();
  if (panelId === 'users') return value.toLocaleString();
  return String(value);
}
function getChange(panelId) {
  const panel = state.panels[panelId];
  if (panel.history.length < 2) return null;
  const prev = panel.history[panel.history.length - 2].value;
  const curr = panel.history[panel.history.length - 1].value;
  if (prev === 0) return null;
  const pct = ((curr - prev) / Math.abs(prev)) * 100;
  return { pct: pct.toFixed(1), dir: pct >= 0 ? 'up' : 'down' };
}
function generateSparkData(panelId, count) {
  const panel = state.panels[panelId];
  const cfg = PANELS.find(p => p.id === panelId);
  const base = cfg ? cfg.value : 50;
  const bars = [];
  for (let i = 0; i < count; i++) {
    const variation = (Math.sin(i * 0.7 + panelId.charCodeAt(0) * 0.3) * 0.2 + Math.random() * 0.15) * base;
    bars.push(Math.max(0.05, 0.5 + variation / (base * 2)));
  }
  return bars;
}
function buildPanelHTML(panel, rankInfo, span) {
  const cfg = PANELS.find(p => p.id === panel.id);
  const historyLen = state.panels[panel.id].history.length;
  const value = historyLen ? state.panels[panel.id].history[historyLen - 1].value : cfg.value;
  const change = getChange(panel.id);
  const isCompact = rankInfo.sizeClass === 'compact';
  const sparkBars = generateSparkData(panel.id, isCompact ? 8 : 16);
  const sparkHTML = sparkBars.map((h, i) =>
    `<div class="spark-bar${i === sparkBars.length - 1 ? ' active' : ''}" style="height:${(h * 100).toFixed(0)}%"></div>`
  ).join('');
  return `
    <div class="panel${isCompact ? ' compact' : ''}${rankInfo.locked ? ' locked' : ''}"
         data-id="${panel.id}"
         draggable="true"
         style="grid-column: span ${span.col}; grid-row: span ${span.row};">
      <div class="panel-header">
        <span class="rank-badge">#${rankInfo.rank}</span>
        <span class="title">${cfg.title}</span>
        <span class="lock-icon">🔒</span>
        <span style="font-size:10px;color:var(--text2)">${rankInfo.sizeClass}</span>
        <div class="panel-controls">
          <button class="panel-btn${rankInfo.locked ? ' locked-btn' : ''}" onclick="event.stopPropagation();toggleLock('${panel.id}')" title="Lock position">🔒</button>
          <button class="panel-btn" onclick="event.stopPropagation();toggleCollapse('${panel.id}')" title="Collapse">${state.panels[panel.id].collapsed ? '▸' : '▾'}</button>
        </div>
      </div>
      <div class="panel-body"${state.panels[panel.id].collapsed ? ' style="display:none"' : ''}>
        <div class="metric-value">${formatValue(panel.id, value)}</div>
        <div class="metric-label">${cfg.title}</div>
        ${change ? `<div class="metric-change ${change.dir}">${change.dir === 'up' ? '▲' : '▼'} ${Math.abs(change.pct)}%</div>` : ''}
        <div class="chart-area">
          <div class="spark-bars">${sparkHTML}</div>
        </div>
      </div>
    </div>
  `;
}
function render() {
  const ranked = rankPanels();
  const grid = document.getElementById('grid');
  const fragment = document.createDocumentFragment();
  for (const r of ranked) {
    const span = getSpan(r.sizeClass);
    const html = buildPanelHTML({ id: r.id }, r, span);
    const div = document.createElement('div');
    div.innerHTML = html;
    fragment.appendChild(div.firstElementChild);
  }
  grid.innerHTML = '';
  grid.appendChild(fragment);
  attachPanelListeners();
  updateStats(ranked);
  saveState();
}
function attachPanelListeners() {
  const panels = document.querySelectorAll('.panel');
  let viewTimers = {};
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const id = entry.target.dataset.id;
      if (entry.isIntersecting) {
        viewTimers[id] = Date.now();
        state.panels[id].lastViewed = Date.now();
      } else {
        if (viewTimers[id]) {
          state.panels[id].durationMs += Date.now() - viewTimers[id];
          delete viewTimers[id];
        }
      }
    }
  }, { threshold: 0.5 });
  panels.forEach(panel => observer.observe(panel));
  panels.forEach(panel => {
    panel.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      const id = panel.dataset.id;
      state.panels[id].interactions++;
      state.panels[id].lastViewed = Date.now();
      recordValue(id);
      if (state.mode === 'auto') debounceRender();
      saveState();
    });
    panel.addEventListener('dragstart', (e) => {
      if (state.mode !== 'manual') return;
      e.dataTransfer.setData('text/plain', panel.dataset.id);
      panel.classList.add('dragging');
    });
    panel.addEventListener('dragend', () => {
      panel.classList.remove('dragging');
      document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
      rebuildOrder();
      render();
    });
  });
  const grid = document.getElementById('grid');
  grid.addEventListener('dragover', (e) => {
    if (state.mode !== 'manual') return;
    e.preventDefault();
    const target = e.target.closest('.panel');
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    if (target && !target.classList.contains('dragging')) {
      target.classList.add('drag-over');
    }
  });
  grid.addEventListener('drop', (e) => {
    e.preventDefault();
    const dragId = e.dataTransfer.getData('text/plain');
    const target = e.target.closest('.panel');
    if (!target || dragId === target.dataset.id) return;
    const dragIdx = state.order.indexOf(dragId);
    const targetIdx = state.order.indexOf(target.dataset.id);
    state.order.splice(dragIdx, 1);
    state.order.splice(targetIdx, 0, dragId);
  });
}
function recordValue(id) {
  const cfg = PANELS.find(p => p.id === id);
  const panel = state.panels[id];
  const jitter = (Math.random() - 0.5) * 0.05 * cfg.value;
  const val = cfg.value + jitter;
  panel.history.push({ ts: Date.now(), value: val });
  if (panel.history.length > 120) panel.history = panel.history.slice(-120);
}
function rebuildOrder() {
  const grid = document.getElementById('grid');
  const children = [...grid.children];
  state.order = children.map(c => c.dataset.id).filter(Boolean);
}
function toggleLock(id) {
  state.panels[id].locked = !state.panels[id].locked;
  render();
}
function toggleCollapse(id) {
  state.panels[id].collapsed = !state.panels[id].collapsed;
  render();
}
function setMode(mode) {
  state.mode = mode;
  document.getElementById('btnAuto').classList.toggle('active', mode === 'auto');
  document.getElementById('btnManual').classList.toggle('active', mode === 'manual');
  const panels = document.querySelectorAll('.panel');
  panels.forEach(p => { p.draggable = mode === 'manual'; });
  saveState();
}
function resetAll() {
  for (const p of PANELS) {
    state.panels[p.id] = {
      locked: false, overrideSpan: null, attention: 0,
      durationMs: 0, interactions: 0, lastViewed: 0,
      history: [], collapsed: false,
    };
  }
  state.order = PANELS.map(p => p.id);
  render();
}
function exportData() {
  const data = {
    exportTime: new Date().toISOString(),
    mode: state.mode,
    rankings: rankPanels(),
    panels: {},
  };
  for (const [id, p] of Object.entries(state.panels)) {
    data.panels[id] = {
      attention: p.attention,
      durationMs: p.durationMs,
      interactions: p.interactions,
      lastViewed: p.lastViewed,
      locked: p.locked,
      collapsed: p.collapsed,
      historyLen: p.history.length,
    };
  }
  console.log(JSON.stringify(data, null, 2));
  alert('Data exported to console');
}
function updateStats(ranked) {
  let totalInt = 0;
  let totalAtt = 0;
  let count = 0;
  for (const r of ranked) {
    const p = state.panels[r.id];
    totalInt += p.interactions;
    totalAtt += r.score;
    count++;
  }
  document.getElementById('statSessions').textContent = '1';
  document.getElementById('statInteractions').textContent = totalInt;
  document.getElementById('statAvg').textContent = count ? (totalAtt / count).toFixed(2) : '0';
  document.getElementById('statTop').textContent = ranked.length ? ranked[0].id : '-';
}
let renderTimeout;
function debounceRender() {
  clearTimeout(renderTimeout);
  renderTimeout = setTimeout(render, 200);
}
function simulateData() {
  for (const p of PANELS) {
    recordValue(p.id);
  }
}
loadState();
render();
setInterval(simulateData, 5000);
setInterval(() => {
  if (state.mode === 'auto') render();
}, 15000);
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    const panels = document.querySelectorAll('.panel');
    panels.forEach(panel => {
      const id = panel.dataset.id;
      if (id && state.panels[id]) {
        state.panels[id].durationMs += 5000;
      }
    });
    saveState();
  }
});
</script>
</body>
</html>