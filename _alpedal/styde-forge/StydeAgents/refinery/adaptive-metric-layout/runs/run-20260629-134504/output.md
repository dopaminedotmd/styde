<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --grid-cols: 4; --gap: 12px; --panel-min: 280px;
  --bg: #0f1117; --surface: #1a1d27; --surface-hover: #22263a;
  --border: #2a2d3a; --text: #e1e4eb; --text-dim: #8b8fa3;
  --accent: #6c8cff; --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff6b7a; --warning: #f0a050; --success: #5cdb8b;
  --rank-1-size: 2; --rank-2-size: 1.5; --rank-3-size: 1;
  --compact-scale: 0.35; --transition-speed: 0.35s;
}
body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; overflow-x: hidden; }
.dashboard-shell { display: flex; flex-direction: column; height: 100vh; }
.toolbar { display: flex; align-items: center; gap: 12px; padding: 12px 20px; background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }
.toolbar h1 { font-size: 16px; font-weight: 600; letter-spacing: -0.01em; }
.toolbar .spacer { flex: 1; }
.toolbar button { background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 500; transition: all 0.15s; }
.toolbar button:hover { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
.toolbar button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.toolbar .frame-budget { font-size: 11px; color: var(--text-dim); padding: 4px 10px; border-radius: 4px; background: var(--bg); min-width: 90px; text-align: center; }
.toolbar .frame-budget.warn { color: var(--warning); }
.toolbar .frame-budget.bad { color: var(--danger); }
.grid-container { flex: 1; overflow-y: auto; padding: 16px 20px 24px; }
.grid { display: grid; grid-template-columns: repeat(var(--grid-cols), 1fr); gap: var(--gap); grid-auto-rows: minmax(180px, auto); grid-auto-flow: dense; }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1); position: relative; cursor: grab; display: flex; flex-direction: column; }
.panel:hover { border-color: #3a3e55; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.panel:active { cursor: grabbing; }
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent-glow); }
.panel.compact { grid-row: span 1; min-height: 70px; max-height: 70px; overflow: hidden; opacity: 0.7; }
.panel.compact:hover { opacity: 0.9; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-header { padding: 8px 14px; }
.panel.rank-0 { grid-column: span 2; grid-row: span 2; }
.panel.rank-1 { grid-column: span 2; grid-row: span 2; }
.panel.rank-2 { grid-column: span 1; grid-row: span 1; }
.panel.rank-3 { grid-column: span 1; grid-row: span 1; }
.panel-header { padding: 12px 16px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; user-select: none; }
.panel-header .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.panel-header .dot.hot { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
.panel-header .dot.warm { background: var(--warning); }
.panel-header .dot.cold { background: var(--text-dim); }
.panel-header .title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-header .score { font-size: 11px; color: var(--text-dim); font-weight: 400; flex-shrink: 0; }
.panel-header .actions { display: flex; gap: 4px; flex-shrink: 0; }
.panel-header .actions button { background: none; border: none; color: var(--text-dim); cursor: pointer; padding: 2px 6px; border-radius: 4px; font-size: 14px; line-height: 1; transition: all 0.15s; }
.panel-header .actions button:hover { color: var(--text); background: var(--surface-hover); }
.panel-header .actions button.lock-btn.locked { color: var(--accent); }
.panel-body { padding: 16px; flex: 1; display: flex; flex-direction: column; gap: 12px; overflow: auto; }
.panel-body .metric-value { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }
.panel-body .metric-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.04em; }
.panel-body .mini-chart { height: 60px; background: linear-gradient(180deg, var(--surface-hover) 0%, var(--surface) 100%); border-radius: 6px; display: flex; align-items: flex-end; padding: 4px; gap: 2px; }
.panel-body .mini-chart .bar { flex: 1; background: var(--accent); border-radius: 2px 2px 0 0; min-height: 2px; transition: height 0.5s; }
.panel.compact .compact-preview { display: flex; align-items: center; gap: 8px; padding: 8px 14px; font-size: 12px; color: var(--text-dim); }
.panel:not(.compact) .compact-preview { display: none; }
.expand-hint { font-size: 11px; color: var(--accent); margin-left: auto; opacity: 0; transition: opacity 0.2s; }
.panel.compact:hover .expand-hint { opacity: 1; }
.more-section { grid-column: 1 / -1; margin-top: 8px; }
.more-section summary { cursor: pointer; padding: 10px 16px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; font-size: 13px; font-weight: 500; color: var(--text-dim); user-select: none; }
.more-section summary:hover { color: var(--text); border-color: #3a3e55; }
.more-section .more-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--gap); padding: var(--gap) 0 0; }
.more-section .more-grid .panel { grid-column: auto; grid-row: auto; min-height: 120px; }
.drag-ghost { opacity: 0.4; border: 2px dashed var(--accent); }
.manual-indicator { position: absolute; top: 6px; right: 6px; width: 6px; height: 6px; border-radius: 50%; background: var(--accent); display: none; }
.panel.locked .manual-indicator { display: block; }
@keyframes pulse-accent { 0%,100% { box-shadow: 0 0 0 0 var(--accent-glow); } 50% { box-shadow: 0 0 0 4px transparent; } }
.panel.just-reordered { animation: pulse-accent 0.6s ease-out; }
</style>
</head>
<body>
<div class="dashboard-shell">
  <div class="toolbar">
    <h1>Adaptive Dashboard</h1>
    <span class="spacer"></span>
    <span class="frame-budget" id="frameBudget">16ms budget</span>
    <button id="resetBtn" title="Reset all tracking data and layout">Reset</button>
    <button id="exportBtn" title="Export tracking data">Export</button>
  </div>
  <div class="grid-container">
    <div class="grid" id="grid"></div>
  </div>
</div>
<script>
(function() {
  'use strict';
  const PANEL_DEFS = [
    { id: 'revenue', title: 'Revenue', icon: '💰', hot: true },
    { id: 'users', title: 'Active Users', icon: '👥', hot: true },
    { id: 'conversion', title: 'Conversion Rate', icon: '📈', hot: false },
    { id: 'latency', title: 'API Latency', icon: '⚡', hot: false },
    { id: 'errors', title: 'Error Rate', icon: '🚨', hot: true },
    { id: 'retention', title: 'Retention', icon: '🔄', hot: false },
    { id: 'bandwidth', title: 'Bandwidth', icon: '🌐', hot: false },
    { id: 'cpu', title: 'CPU Usage', icon: '🖥️', hot: false },
    { id: 'memory', title: 'Memory', icon: '💾', hot: false },
    { id: 'queue', title: 'Queue Depth', icon: '📬', hot: false },
  ];
  const STORAGE_KEY = 'adaptive_dashboard_v2';
  const DECAY_HALF_LIFE_MS = 7 * 24 * 60 * 60 * 1000;
  const COMPACT_THRESHOLD_PERCENTILE = 65;
  const MIN_SCORE_FOR_FULL = 5;
  const FRAME_BUDGET_MS = 16;
  const SCROLL_DEBOUNCE_MS = 100;
  const STATE_VERSION = 2;
  let panels = [];
  let layoutOrder = [];
  let lockedPanels = new Set();
  let manualOverrides = {};
  let lastRenderKeys = null;
  let frameBudgetEl = null;
  let budgetHistory = [];
  let budgetHistoryMax = 60;
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (data._version !== STATE_VERSION) return null;
      return data;
    } catch(e) { return null; }
  }
  function saveState() {
    const data = {
      _version: STATE_VERSION,
      _ts: Date.now(),
      panels: panels.map(p => ({ id: p.id, views: p.views, totalDuration: p.totalDuration, interactions: p.interactions, lastViewed: p.lastViewed, lastInteraction: p.lastInteraction, collapses: p.collapses, expands: p.expands })),
      layoutOrder,
      lockedPanels: [...lockedPanels],
      manualOverrides,
    };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch(e) {}
  }
  function initPanels() {
    const saved = loadState();
    panels = PANEL_DEFS.map(def => {
      const savedPanel = saved?.panels?.find(p => p.id === def.id);
      return {
        id: def.id,
        title: def.title,
        icon: def.icon,
        hot: def.hot,
        views: savedPanel?.views || 0,
        totalDuration: savedPanel?.totalDuration || 0,
        interactions: savedPanel?.interactions || 0,
        lastViewed: savedPanel?.lastViewed || 0,
        lastInteraction: savedPanel?.lastInteraction || 0,
        collapses: savedPanel?.collapses || 0,
        expands: savedPanel?.expands || 0,
        isCompact: false,
      };
    });
    layoutOrder = saved?.layoutOrder || panels.map(p => p.id);
    lockedPanels = new Set(saved?.lockedPanels || []);
    manualOverrides = saved?.manualOverrides || {};
  }
  function saveStateDebounced() {
    if (saveState._timer) clearTimeout(saveState._timer);
    saveState._timer = setTimeout(saveState, 300);
  }
  function decayFactor(lastTs, now) {
    if (!lastTs || lastTs <= 0) return 1;
    const age = now - lastTs;
    return Math.pow(0.5, age / DECAY_HALF_LIFE_MS);
  }
  function computeScore(panel, now) {
    const recencyDecay = decayFactor(Math.max(panel.lastViewed, panel.lastInteraction), now);
    const frequency = panel.views + panel.interactions * 1.5 + panel.expands * 0.5;
    const avgDuration = panel.views > 0 ? panel.totalDuration / panel.views : 0;
    const durationScore = Math.log2(Math.max(avgDuration / 1000, 1));
    const raw = frequency * durationScore * recencyDecay;
    const collapsePenalty = 1 / (1 + panel.collapses * 0.15);
    return Math.max(raw * collapsePenalty, 0.01);
  }
  function rankPanels() {
    const now = Date.now();
    const scored = panels.map(p => ({ ...p, score: computeScore(p, now) }));
    scored.sort((a, b) => b.score - a.score);
    return scored;
  }
  function assignRanks(scored) {
    const top = scored.slice(0, 3);
    const mid = scored.slice(3, 7);
    const rest = scored.slice(7);
    const rankMap = {};
    top.forEach(p => rankMap[p.id] = 0);
    mid.forEach(p => rankMap[p.id] = 1);
    rest.forEach(p => rankMap[p.id] = 2);
    return rankMap;
  }
  function decideCompact(scored) {
    const compactIds = new Set();
    const thresholds = scored.map(p => p.score);
    thresholds.sort((a, b) => a - b);
    const cutoffIdx = Math.floor(thresholds.length * COMPACT_THRESHOLD_PERCENTILE / 100);
    const cutoff = thresholds[cutoffIdx] || 0;
    scored.forEach(p => {
      if (p.score < MIN_SCORE_FOR_FULL || (p.score <= cutoff && scored.indexOf(p) >= 5)) {
        compactIds.add(p.id);
      }
    });
    lockedPanels.forEach(id => compactIds.delete(id));
    return compactIds;
  }
  function applyOverrides(rankMap, compactIds) {
    const result = { rankMap: { ...rankMap }, compactIds: new Set(compactIds) };
    for (const [panelId, override] of Object.entries(manualOverrides)) {
      if (override.rank !== undefined) result.rankMap[panelId] = override.rank;
      if (override.compact !== undefined) {
        if (override.compact) result.compactIds.add(panelId);
        else result.compactIds.delete(panelId);
      }
    }
    lockedPanels.forEach(id => {
      result.compactIds.delete(id);
    });
    return result;
  }
  function buildRenderState(ranked, overrides) {
    const state = {};
    const ordered = [];
    let lockFirst = [];
    let rest = [];
    ranked.forEach(p => {
      const entry = { id: p.id, score: p.score, rank: overrides.rankMap[p.id] ?? 2, compact: overrides.compactIds.has(p.id), locked: lockedPanels.has(p.id) };
      state[p.id] = entry;
      if (entry.locked) lockFirst.push(entry);
      else rest.push(entry);
    });
    lockFirst.sort((a, b) => b.score - a.score);
    rest.sort((a, b) => b.score - a.score);
    const fullOrder = [...lockFirst, ...rest];
    return { state, order: fullOrder.map(e => e.id) };
  }
  function renderKey(renderState) {
    return renderState.order.map(id => `${id}:${renderState.state[id].rank}:${renderState.state[id].compact ? 1 : 0}:${renderState.state[id].locked ? 1 : 0}`).join('|');
  }
  function diffRender(prevKey, newKey, prevState, newState) {
    if (prevKey === newKey && prevState) return { fullRender: false, changed: [] };
    const changed = [];
    if (!prevState) return { fullRender: true, changed: [] };
    const allIds = new Set([...Object.keys(prevState), ...Object.keys(newState)]);
    for (const id of allIds) {
      const prev = prevState[id];
      const next = newState[id];
      if (!prev || !next || prev.rank !== next.rank || prev.compact !== next.compact || prev.locked !== next.locked) {
        changed.push(id);
      }
    }
    return { fullRender: false, changed };
  }
  let prevRenderState = null;
  let prevRenderKeyVal = null;
  function renderGrid(forceFull) {
    const t0 = performance.now();
    const grid = document.getElementById('grid');
    const scored = rankPanels();
    const autoRankMap = assignRanks(scored);
    const autoCompactIds = decideCompact(scored);
    const overrides = applyOverrides(autoRankMap, autoCompactIds);
    const renderState = buildRenderState(scored, overrides);
    const newKey = renderKey(renderState);
    const diff = forceFull ? { fullRender: true, changed: [] } : diffRender(prevRenderKeyVal, newKey, prevRenderState?.state, renderState.state);
    if (!diff.fullRender && diff.changed.length === 0) {
      trackFrameBudget(performance.now() - t0);
      return;
    }
    if (diff.fullRender) {
      grid.innerHTML = '';
      renderAllPanels(grid, renderState, scored, panMetrics());
    } else {
      diff.changed.forEach(id => {
        const el = document.getElementById('panel-' + id);
        if (el) updatePanelElement(el, renderState.state[id], getPanelById(id), panMetrics());
      });
      reorderGrid(grid, renderState.order);
    }
    prevRenderState = renderState;
    prevRenderKeyVal = newKey;
    const elapsed = performance.now() - t0;
    trackFrameBudget(elapsed);
  }
  function panMetrics() {
    const m = {};
    panels.forEach(p => { m[p.id] = randomMetrics(p.id); });
    return m;
  }
  let metricsCache = {};
  let metricsCacheTs = 0;
  function randomMetrics(id) {
    const now = Date.now();
    if (now - metricsCacheTs < 2000 && metricsCache[id]) return metricsCache[id];
    const base = id.charCodeAt(0) * 37 + id.length * 13;
    metricsCache[id] = {
      value: (Math.abs(Math.sin(base + now / 5000)) * 8000 + 200).toFixed(0),
      trend: Math.sin(base + now / 7000) > 0.3 ? 'up' : Math.sin(base + now / 7000) < -0.3 ? 'down' : 'flat',
      bars: Array.from({ length: 12 }, (_, i) => Math.abs(Math.sin(base * 1.7 + i * 0.8 + now / 8000)) * 60 + 10),
    };
    metricsCacheTs = now;
    return metricsCache[id];
  }
  function getPanelById(id) {
    return panels.find(p => p.id === id);
  }
  function createPanelElement(panel, renderEntry, metrics) {
    const el = document.createElement('div');
    el.id = 'panel-' + panel.id;
    el.className = 'panel';
    el.draggable = true;
    el.dataset.panelId = panel.id;
    applyPanelClasses(el, renderEntry);
    el.innerHTML = panelInnerHTML(panel, renderEntry, metrics);
    bindPanelEvents(el, panel.id);
    return el;
  }
  function updatePanelElement(el, renderEntry, panel, metrics) {
    applyPanelClasses(el, renderEntry);
    const header = el.querySelector('.panel-header');
    if (header) {
      const scoreEl = header.querySelector('.score');
      if (scoreEl) scoreEl.textContent = renderEntry.score.toFixed(1);
      const lockBtn = header.querySelector('.lock-btn');
      if (lockBtn) {
        lockBtn.textContent = renderEntry.locked ? '🔒' : '🔓';
        if (renderEntry.locked) lockBtn.classList.add('locked');
        else lockBtn.classList.remove('locked');
      }
    }
    const body = el.querySelector('.panel-body');
    if (body && !renderEntry.compact) {
      const m = metrics || randomMetrics(panel.id);
      const valEl = body.querySelector('.metric-value');
      if (valEl) valEl.textContent = m.value;
      const bars = body.querySelectorAll('.bar');
      if (bars.length && m.bars) {
        bars.forEach((bar, i) => { bar.style.height = (m.bars[i] || 10) + '%'; });
      }
    }
    const compactPrev = el.querySelector('.compact-preview');
    if (compactPrev) {
      const m = metrics || randomMetrics(panel.id);
      compactPrev.textContent = panel.icon + ' ' + m.value;
    }
    if (renderEntry.compact) {
      const hint = el.querySelector('.expand-hint');
      if (!hint) {
        const h = document.createElement('span');
        h.className = 'expand-hint';
        h.textContent = 'click to expand';
        el.querySelector('.panel-header')?.appendChild(h);
      }
    }
    const manualInd = el.querySelector('.manual-indicator');
    if (manualInd) manualInd.style.display = renderEntry.locked ? 'block' : 'none';
  }
  function applyPanelClasses(el, renderEntry) {
    el.classList.remove('rank-0', 'rank-1', 'rank-2', 'rank-3', 'compact', 'locked');
    el.classList.add('rank-' + renderEntry.rank);
    if (renderEntry.compact) el.classList.add('compact');
    if (renderEntry.locked) el.classList.add('locked');
  }
  function panelInnerHTML(panel, renderEntry, metrics) {
    const m = metrics || randomMetrics(panel.id);
    const trendArrow = m.trend === 'up' ? '↑' : m.trend === 'down' ? '↓' : '→';
    const trendColor = m.trend === 'up' ? 'var(--success)' : m.trend === 'down' ? 'var(--danger)' : 'var(--text-dim)';
    return `
      <div class="manual-indicator"></div>
      <div class="panel-header">
        <span class="dot ${panel.hot ? 'hot' : 'cold'}"></span>
        <span class="title">${panel.icon} ${panel.title}</span>
        <span class="score">${renderEntry.score.toFixed(1)}</span>
        <span class="actions">
          <button class="lock-btn${renderEntry.locked ? ' locked' : ''}" data-action="lock" title="Lock position">${renderEntry.locked ? '🔒' : '🔓'}</button>
          <button data-action="toggle" title="${renderEntry.compact ? 'Expand' : 'Compact'}">${renderEntry.compact ? '⤢' : '⤡'}</button>
        </span>
      </div>
      <div class="compact-preview">${panel.icon} ${m.value}</div>
      <span class="expand-hint" style="display:${renderEntry.compact ? '' : 'none'}">click to expand</span>
      <div class="panel-body">
        <div class="metric-value" style="color:${trendColor}">${trendArrow} ${m.value}</div>
        <div class="metric-label">${panel.title}</div>
        <div class="mini-chart">${m.bars.map(h => `<div class="bar" style="height:${h}%"></div>`).join('')}</div>
      </div>`;
  }
  function renderAllPanels(grid, renderState, scored, metrics) {
    const frag = document.createDocumentFragment();
    const panelMap = {};
    scored.forEach(p => { panelMap[p.id] = p; });
    renderState.order.forEach(id => {
      const panel = panelMap[id];
      const entry = renderState.state[id];
      if (entry) {
        const el = createPanelElement(panel, entry, metrics[id]);
        frag.appendChild(el);
      }
    });
    grid.appendChild(frag);
  }
  function reorderGrid(grid, order) {
    const existing = new Map();
    grid.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.panelId, el));
    order.forEach((id, idx) => {
      const el = existing.get(id);
      if (el && Array.from(grid.children).indexOf(el) !== idx) {
        grid.insertBefore(el, grid.children[idx] || null);
      }
    });
  }
  function trackFrameBudget(elapsed) {
    budgetHistory.push(elapsed);
    if (budgetHistory.length > budgetHistoryMax) budgetHistory.shift();
    if (!frameBudgetEl) frameBudgetEl = document.getElementById('frameBudget');
    const avg = budgetHistory.reduce((a, b) => a + b, 0) / budgetHistory.length;
    frameBudgetEl.textContent = avg.toFixed(1) + 'ms render';
    frameBudgetEl.classList.remove('warn', 'bad');
    if (avg > FRAME_BUDGET_MS * 1.5) frameBudgetEl.classList.add('bad');
    else if (avg > FRAME_BUDGET_MS) frameBudgetEl.classList.add('warn');
  }
  function recordView(panelId, duration) {
    const panel = panels.find(p => p.id === panelId);
    if (!panel) return;
    panel.views++;
    panel.totalDuration += duration;
    panel.lastViewed = Date.now();
    saveStateDebounced();
  }
  function recordInteraction(panelId, type) {
    const panel = panels.find(p => p.id === panelId);
    if (!panel) return;
    panel.interactions++;
    panel.lastInteraction = Date.now();
    if (type === 'collapse') panel.collapses++;
    if (type === 'expand') panel.expands++;
    saveStateDebounced();
  }
  function toggleLock(panelId) {
    if (lockedPanels.has(panelId)) {
      lockedPanels.delete(panelId);
      delete manualOverrides[panelId];
    } else {
      lockedPanels.add(panelId);
      manualOverrides[panelId] = { rank: prevRenderState?.state?.[panelId]?.rank ?? 1, compact: false };
    }
    saveStateDebounced();
    scheduleRender();
  }
  function toggleCompact(panelId) {
    const isCompact = prevRenderState?.state?.[panelId]?.compact;
    if (isCompact) {
      manualOverrides[panelId] = { ...manualOverrides[panelId], compact: false };
      recordInteraction(panelId, 'expand');
    } else {
      manualOverrides[panelId] = { ...manualOverrides[panelId], compact: true };
      recordInteraction(panelId, 'collapse');
    }
    saveStateDebounced();
    scheduleRender();
  }
  function bindPanelEvents(el, panelId) {
    el.addEventListener('click', (e) => {
      const action = e.target.closest('[data-action]')?.dataset?.action;
      if (action === 'lock') { toggleLock(panelId); return; }
      if (action === 'toggle') { toggleCompact(panelId); return; }
      if (el.classList.contains('compact')) {
        toggleCompact(panelId);
        return;
      }
      recordInteraction(panelId, 'click');
    });
    el.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', panelId);
      el.classList.add('drag-ghost');
      e.dataTransfer.effectAllowed = 'move';
    });
    el.addEventListener('dragend', (e) => {
      el.classList.remove('drag-ghost');
    });
    el.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      const draggedId = e.dataTransfer.getData('text/plain');
      const targetId = panelId;
      if (draggedId === targetId) return;
      if (!prevRenderState) return;
      const order = [...prevRenderState.order];
      const fromIdx = order.indexOf(draggedId);
      const toIdx = order.indexOf(targetId);
      if (fromIdx < 0 || toIdx < 0) return;
      order.splice(fromIdx, 1);
      order.splice(toIdx, 0, draggedId);
      layoutOrder = order;
      lockedPanels.add(draggedId);
      lockedPanels.add(targetId);
      manualOverrides[draggedId] = { rank: prevRenderState.state[targetId]?.rank ?? 1, compact: false };
      manualOverrides[targetId] = { rank: prevRenderState.state[draggedId]?.rank ?? 1, compact: false };
      saveStateDebounced();
      scheduleRender();
      el.classList.add('just-reordered');
      setTimeout(() => el.classList.remove('just-reordered'), 600);
    });
  }
  let renderScheduled = false;
  let renderRAF = null;
  function scheduleRender() {
    if (renderScheduled) return;
    renderScheduled = true;
    renderRAF = requestAnimationFrame(() => {
      renderScheduled = false;
      renderRAF = null;
      renderGrid(false);
    });
  }
  class ObserverManager {
    constructor() {
      this.viewDurations = new Map();
      this.viewStartTimes = new Map();
      this.io = null;
      this.mo = null;
      this.connected = false;
    }
    connect() {
      if (this.connected) return;
      this.connected = true;
      this.io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const panelId = entry.target.dataset.panelId;
          if (!panelId) return;
          if (entry.isIntersecting) {
            this.viewStartTimes.set(panelId, performance.now());
          } else {
            const start = this.viewStartTimes.get(panelId);
            if (start) {
              const duration = performance.now() - start;
              this.viewDurations.set(panelId, (this.viewDurations.get(panelId) || 0) + duration);
              this.viewStartTimes.delete(panelId);
              if (duration > 500) {
                recordView(panelId, duration);
              }
            }
          }
        });
      }, { threshold: 0.3 });
      this.mo = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
          mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.classList.contains('panel')) {
              this.io.observe(node);
            }
          });
          mutation.removedNodes.forEach(node => {
            if (node.nodeType === 1 && node.classList.contains('panel')) {
              this.io.unobserve(node);
              const pid = node.dataset.panelId;
              if (pid) {
                const start = this.viewStartTimes.get(pid);
                if (start) {
                  recordView(pid, performance.now() - start);
                  this.viewStartTimes.delete(pid);
                }
              }
            }
          });
        }
      });
      this.mo.observe(document.getElementById('grid'), { childList: true, subtree: false });
      document.querySelectorAll('.panel').forEach(el => this.io.observe(el));
    }
    disconnect() {
      this.connected = false;
      if (this.io) { this.io.disconnect(); this.io = null; }
      if (this.mo) { this.mo.disconnect(); this.mo = null; }
      this.viewStartTimes.forEach((start, panelId) => {
        recordView(panelId, performance.now() - start);
      });
      this.viewStartTimes.clear();
    }
    flushViewDurations() {
      this.viewStartTimes.forEach((start, panelId) => {
        const duration = performance.now() - start;
        if (duration > 500) recordView(panelId, duration);
        this.viewStartTimes.set(panelId, performance.now());
      });
    }
  }
  let observerManager = null;
  let scrollThrottleRAF = null;
  let scrollPending = false;
  function onScroll() {
    if (scrollPending) return;
    scrollPending = true;
    scrollThrottleRAF = requestAnimationFrame(() => {
      scrollPending = false;
      scrollThrottleRAF = null;
      if (observerManager) observerManager.flushViewDurations();
    });
  }
  function resetAll() {
    if (!confirm('Reset all tracking data and layout preferences?')) return;
    panels.forEach(p => {
      p.views = 0; p.totalDuration = 0; p.interactions = 0;
      p.lastViewed = 0; p.lastInteraction = 0;
      p.collapses = 0; p.expands = 0;
    });
    layoutOrder = panels.map(p => p.id);
    lockedPanels.clear();
    manualOverrides = {};
    prevRenderState = null;
    prevRenderKeyVal = null;
    localStorage.removeItem(STORAGE_KEY);
    renderGrid(true);
  }
  function exportData() {
    const scored = rankPanels();
    const data = {
      exportedAt: new Date().toISOString(),
      panels: scored.map(p => ({
        id: p.id, title: p.title, score: p.score.toFixed(2),
        views: p.views, totalDuration: p.totalDuration,
        interactions: p.interactions, lastViewed: new Date(p.lastViewed).toISOString(),
        collapses: p.collapses, expands: p.expands,
        rank: (prevRenderState?.state?.[p.id]?.rank ?? '-'),
        compact: prevRenderState?.state?.[p.id]?.compact ?? false,
        locked: lockedPanels.has(p.id),
      })),
      manualOverrides,
      layoutOrder,
      frameBudgetAvg: budgetHistory.length ? (budgetHistory.reduce((a,b)=>a+b,0)/budgetHistory.length).toFixed(2) : 0,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'dashboard-export-' + Date.now() + '.json';
    a.click();
    URL.revokeObjectURL(url);
  }
  function periodicRecompute() {
    scheduleRender();
  }
  function init() {
    initPanels();
    observerManager = new ObserverManager();
    renderGrid(true);
    observerManager.connect();
    document.querySelector('.grid-container').addEventListener('scroll', onScroll, { passive: true });
    document.getElementById('resetBtn').addEventListener('click', resetAll);
    document.getElementById('exportBtn').addEventListener('click', exportData);
    window.addEventListener('beforeunload', () => {
      if (observerManager) observerManager.disconnect();
      saveState();
    });
    setInterval(periodicRecompute, 15000);
    setInterval(() => {
      metricsCacheTs = 0;
      scheduleRender();
    }, 4000);
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