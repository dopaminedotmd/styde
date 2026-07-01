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
    --surface-hover: #22263a;
    --border: #2a2e3f;
    --text: #e1e4ed;
    --text-dim: #8890a8;
    --accent: #6c8cff;
    --accent-glow: rgba(108,140,255,0.15);
    --hero: #ff6b9d;
    --warn: #ffb347;
    --ok: #4ecca3;
    --compact-bg: #141820;
    --grid-gap: 12px;
    --radius: 10px;
    --transition-speed: 0.3s;
    --font-mono: 'SF Mono','Cascadia Code','Consolas',monospace;
    --font-sans: 'Inter','Segoe UI',system-ui,sans-serif;
  }
  @media (prefers-reduced-motion: reduce) {
    :root { --transition-speed: 0s; }
  }
  .reduced-motion *,
  .reduced-motion *::before,
  .reduced-motion *::after {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-sans);
    min-height: 100vh;
    padding: 16px;
    -webkit-font-smoothing: antialiased;
  }
  .toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .toolbar h1 {
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-right: auto;
  }
  .badge {
    font-size: 0.7rem;
    padding: 3px 8px;
    border-radius: 99px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-dim);
    font-family: var(--font-mono);
  }
  .btn {
    font-size: 0.75rem;
    padding: 6px 14px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    cursor: pointer;
    font-family: var(--font-sans);
    transition: background var(--transition-speed), border-color var(--transition-speed);
  }
  .btn:hover { background: var(--surface-hover); border-color: var(--accent); }
  .btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .dashboard {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-auto-rows: 160px;
    gap: var(--grid-gap);
    transition: grid-template-columns var(--transition-speed), grid-auto-rows var(--transition-speed);
  }
  .dashboard.compact-view {
    grid-auto-rows: 100px;
  }
  @media (max-width: 1400px) { .dashboard { grid-template-columns: repeat(4, 1fr); } }
  @media (max-width: 900px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 500px) { .dashboard { grid-template-columns: 1fr; } }
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
    transition: transform var(--transition-speed), box-shadow var(--transition-speed), border-color var(--transition-speed);
    cursor: default;
    min-height: 0;
  }
  .panel:hover {
    box-shadow: 0 0 0 1px var(--accent-glow), 0 4px 24px rgba(0,0,0,0.3);
  }
  .panel.locked {
    border-color: var(--warn);
  }
  .panel.locked::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 0; height: 0;
    border-style: solid;
    border-width: 0 18px 18px 0;
    border-color: transparent var(--warn) transparent transparent;
    z-index: 2;
    pointer-events: none;
  }
  .panel.dragging {
    opacity: 0.7;
    transform: scale(0.96);
    z-index: 10;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
  }
  .panel.drag-over {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-glow);
  }
  /* Size tiers */
  .panel[data-tier="hero"]    { grid-column: span 4; grid-row: span 3; }
  .panel[data-tier="large"]   { grid-column: span 3; grid-row: span 2; }
  .panel[data-tier="medium"]  { grid-column: span 2; grid-row: span 2; }
  .panel[data-tier="compact"] { grid-column: span 1; grid-row: span 1; }
  .panel[data-tier="mini"]    { grid-column: span 1; grid-row: span 1; }
  @media (max-width: 1400px) {
    .panel[data-tier="hero"]  { grid-column: span 4; grid-row: span 2; }
    .panel[data-tier="large"] { grid-column: span 2; grid-row: span 2; }
  }
  @media (max-width: 900px) {
    .panel[data-tier="hero"]  { grid-column: span 2; grid-row: span 2; }
    .panel[data-tier="large"] { grid-column: span 2; grid-row: span 2; }
    .panel[data-tier="medium"]{ grid-column: span 2; grid-row: span 1; }
  }
  @media (max-width: 500px) {
    .panel[data-tier="hero"],
    .panel[data-tier="large"],
    .panel[data-tier="medium"],
    .panel[data-tier="compact"],
    .panel[data-tier="mini"] { grid-column: span 1; grid-row: span 1; }
  }
  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px 8px;
    flex-shrink: 0;
    cursor: grab;
    user-select: none;
    background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%);
  }
  .panel-header:active { cursor: grabbing; }
  .panel-header .title {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .panel-header .controls {
    display: flex;
    gap: 4px;
    opacity: 0;
    transition: opacity var(--transition-speed);
  }
  .panel:hover .panel-header .controls { opacity: 1; }
  .ctrl-btn {
    width: 24px; height: 24px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    cursor: pointer;
    border-radius: 4px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background var(--transition-speed), color var(--transition-speed);
  }
  .ctrl-btn:hover { background: var(--surface-hover); color: var(--text); }
  .ctrl-btn.lock-btn.locked { color: var(--warn); }
  .panel-body {
    flex: 1;
    padding: 0 12px 12px;
    min-height: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .metric-row {
    display: flex;
    gap: 10px;
    align-items: flex-end;
  }
  .metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    font-family: var(--font-mono);
    line-height: 1;
  }
  .metric-label {
    font-size: 0.65rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 2px;
  }
  .metric-change {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 4px;
    font-family: var(--font-mono);
  }
  .metric-change.up { color: var(--ok); background: rgba(78,204,163,0.1); }
  .metric-change.down { color: var(--hero); background: rgba(255,107,157,0.1); }
  .sparkline {
    flex: 1;
    min-height: 40px;
    width: 100%;
  }
  .sparkline svg { width: 100%; height: 100%; }
  .mini-content {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.7rem;
    color: var(--text-dim);
  }
  .mini-content .mini-val {
    font-size: 1.1rem;
    font-weight: 700;
    font-family: var(--font-mono);
    color: var(--text);
  }
  .heatmap-overlay {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    opacity: 0.08;
    transition: opacity 0.5s;
  }
  .heatmap-overlay canvas {
    width: 100%;
    height: 100%;
  }
  body.reduced-power .heatmap-overlay { display: none; }
  body.reduced-power .panel { transition: none; }
  .attention-indicator {
    position: absolute;
    inset: 0;
    border-radius: var(--radius);
    pointer-events: none;
    z-index: 1;
    transition: box-shadow 1.5s ease-out;
  }
  .panel.hot .attention-indicator {
    box-shadow: inset 0 0 40px rgba(108,140,255,0.06);
  }
  .rank-badge {
    position: absolute;
    top: 6px;
    right: 38px;
    font-size: 0.55rem;
    font-family: var(--font-mono);
    color: var(--text-dim);
    background: var(--surface);
    padding: 1px 5px;
    border-radius: 3px;
    border: 1px solid var(--border);
    z-index: 2;
    opacity: 0;
    transition: opacity var(--transition-speed);
  }
  .panel:hover .rank-badge { opacity: 1; }
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--surface);
    border: 1px solid var(--accent);
    color: var(--text);
    padding: 8px 20px;
    border-radius: 8px;
    font-size: 0.75rem;
    z-index: 10000;
    animation: toastIn 0.25s ease-out;
    pointer-events: none;
  }
  @keyframes toastIn {
    from { opacity: 0; transform: translateX(-50%) translateY(8px); }
    to   { opacity: 1; transform: translateX(-50%) translateY(0); }
  }
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Metric Layout</h1>
  <span class="badge" id="view-state">active</span>
  <span class="badge" id="power-badge">full</span>
  <button class="btn" id="btn-reset" title="Reset all tracking data">Reset data</button>
  <button class="btn" id="btn-heatmap" title="Toggle attention heatmap overlay">Heatmap</button>
  <button class="btn" id="btn-compact" title="Toggle compact view">Compact</button>
  <button class="btn" id="btn-unlock-all" title="Unlock all panels">Unlock all</button>
  <button class="btn" id="btn-rearrange" title="Force layout recompute">Recompute</button>
</div>
<div class="dashboard" id="dashboard">
  <!-- Panels injected by JS -->
</div>
<div class="heatmap-overlay" id="heatmap-overlay" style="display:none;">
  <canvas id="heatmap-canvas"></canvas>
</div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_layout_v1';
  const DEBOUNCE_MS = 400;
  const DECAY_HALF_LIFE_HOURS = 24;
  const SCORE_WEIGHTS = { frequency: 0.4, duration: 0.4, recency: 0.2 };
  const TIER_THRESHOLDS = { hero: 0.80, large: 0.55, medium: 0.30, compact: 0.10 };
  const PANEL_DEFS = [
    { id: 'revenue',    title: 'Revenue (MRR)',    type: 'metric', value: '$48,292', change: '+12.4%', dir:'up',   color: '#4ecca3' },
    { id: 'users',      title: 'Active Users',      type: 'metric', value: '18,244',  change: '+8.1%',  dir:'up',   color: '#6c8cff' },
    { id: 'churn',      title: 'Churn Rate',        type: 'metric', value: '2.1%',    change: '-0.3%',  dir:'down', color: '#ff6b9d' },
    { id: 'latency',    title: 'API Latency (p95)', type: 'metric', value: '142ms',   change: '+11ms',  dir:'down', color: '#ffb347' },
    { id: 'errors',     title: 'Error Rate',        type: 'metric', value: '0.04%',   change: '-0.01%', dir:'down', color: '#4ecca3' },
    { id: 'cpu',        title: 'CPU Utilization',   type: 'metric', value: '67%',     change: '+5%',    dir:'down', color: '#ffb347' },
    { id: 'bandwidth',  title: 'Bandwidth',         type: 'metric', value: '842 Mbps',change: '+14%',   dir:'up',   color: '#6c8cff' },
    { id: 'sessions',   title: 'Sessions',          type: 'metric', value: '4,921',   change: '+22%',   dir:'up',   color: '#4ecca3' },
    { id: 'deploys',    title: 'Deployments',       type: 'metric', value: '247',     change: '+3',     dir:'up',   color: '#6c8cff' },
    { id: 'tickets',    title: 'Support Tickets',   type: 'metric', value: '18',      change: '-4',     dir:'down', color: '#4ecca3' },
  ];
  let state = {
    panels: {},
    heatmapEnabled: false,
    compactView: false,
    reducedPower: false,
    lastActivity: Date.now(),
    idleTimer: null,
    visibilityObserver: null,
    resizeObserver: null,
    mutationObserver: null,
    heatmapObserver: null,
    heatmapCanvas: null,
    heatmapCtx: null,
    attentionPoints: [],
    resizeRAF: null,
    scoreRAF: null,
    heatmapRAF: null,
    recomputeDebounce: null,
    saveDebounce: null,
  };
  function init() {
    loadState();
    renderDashboard();
    setupObservers();
    setupVisibility();
    setupDragDrop();
    recomputeLayout();
    setupHeatmap();
  }
  function defaultPanelData(id) {
    const def = PANEL_DEFS.find(p => p.id === id) || {};
    return {
      id: id,
      title: def.title || id,
      type: def.type || 'metric',
      value: def.value || '--',
      change: def.change || '',
      dir: def.dir || 'up',
      color: def.color || '#6c8cff',
      locked: false,
      manualTier: null,
      attention: {
        viewDuration: 0,
        interactionCount: 0,
        lastInteraction: 0,
        score: 0,
        rank: 0,
      },
    };
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const saved = JSON.parse(raw);
        for (const [id, data] of Object.entries(saved.panels || {})) {
          state.panels[id] = { ...defaultPanelData(id), ...data };
        }
      }
    } catch(e) { /* corrupt storage, start fresh */ }
    for (const def of PANEL_DEFS) {
      if (!state.panels[def.id]) {
        state.panels[def.id] = defaultPanelData(def.id);
      } else {
        state.panels[def.id].title = def.title;
        state.panels[def.id].value = def.value;
        state.panels[def.id].change = def.change;
        state.panels[def.id].dir = def.dir;
        state.panels[def.id].color = def.color;
        state.panels[def.id].type = def.type;
      }
    }
  }
  function persistState() {
    if (state.saveDebounce) clearTimeout(state.saveDebounce);
    state.saveDebounce = setTimeout(() => {
      try {
        const toSave = { panels: state.panels, timestamp: Date.now() };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
      } catch(e) { /* quota exceeded, silently skip */ }
    }, 600);
  }
  function renderDashboard() {
    const container = document.getElementById('dashboard');
    const existing = new Map();
    container.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.panelId, el));
    const orderedIds = Object.values(state.panels)
      .sort((a, b) => a.attention.rank - b.attention.rank)
      .map(p => p.id);
    const fragment = document.createDocumentFragment();
    for (const id of orderedIds) {
      const panel = state.panels[id];
      let el = existing.get(id);
      if (el) {
        existing.delete(id);
        updatePanelElement(el, panel);
      } else {
        el = createPanelElement(panel);
      }
      fragment.appendChild(el);
    }
    for (const [_, el] of existing) { el.remove(); }
    container.appendChild(fragment);
    container.classList.toggle('compact-view', state.compactView);
  }
  function createPanelElement(panel) {
    const el = document.createElement('div');
    el.className = 'panel';
    el.dataset.panelId = panel.id;
    el.draggable = false;
    el.innerHTML = buildPanelHTML(panel);
    setupPanelInteractivity(el, panel);
    return el;
  }
  function updatePanelElement(el, panel) {
    const header = el.querySelector('.panel-header .title');
    if (header) header.textContent = panel.title;
    const body = el.querySelector('.panel-body');
    if (body) body.innerHTML = buildPanelBodyHTML(panel);
    const tier = computeTier(panel);
    el.dataset.tier = tier;
    el.classList.toggle('locked', panel.locked);
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.textContent = panel.locked ? 'L' : 'U';
      lockBtn.classList.toggle('locked', panel.locked);
    }
    const rankBadge = el.querySelector('.rank-badge');
    if (rankBadge) rankBadge.textContent = '#' + (panel.attention.rank || '?');
    el.draggable = panel.locked;
  }
  function buildPanelHTML(panel) {
    const tier = computeTier(panel);
    return `
      <div class="panel-header" data-action="drag-handle">
        <span class="title">${esc(panel.title)}</span>
        <span class="rank-badge">#${panel.attention.rank || '?'}</span>
        <span class="controls">
          <button class="ctrl-btn lock-btn${panel.locked ? ' locked' : ''}" data-action="toggle-lock" title="Lock position">${panel.locked ? 'L' : 'U'}</button>
          <button class="ctrl-btn" data-action="promote" title="Boost rank">+</button>
          <button class="ctrl-btn" data-action="demote" title="Lower rank">-</button>
        </span>
      </div>
      <div class="panel-body">${buildPanelBodyHTML(panel)}</div>
      <div class="attention-indicator"></div>
    `;
  }
  function buildPanelBodyHTML(panel) {
    const tier = computeTier(panel);
    if (tier === 'mini') {
      return `
        <div class="mini-content">
          <span class="mini-val">${esc(panel.value)}</span>
          <span>${esc(panel.change)}</span>
        </div>
      `;
    }
    return `
      <div class="metric-label">${esc(panel.title)}</div>
      <div class="metric-row">
        <span class="metric-value">${esc(panel.value)}</span>
        <span class="metric-change ${panel.dir}">${esc(panel.change)}</span>
      </div>
      <div class="sparkline">${generateSparkline(panel)}</div>
    `;
  }
  function generateSparkline(panel) {
    const points = 24;
    const vals = [];
    const seed = panel.id.split('').reduce((a,c) => a + c.charCodeAt(0), 0);
    for (let i = 0; i < points; i++) {
      const x = (i / points) * Math.PI * 2;
      vals.push(30 + Math.sin(x * 2.3 + seed) * 20 + Math.cos(x * 5.1) * 10 + (i / points) * 25);
    }
    const min = Math.min(...vals);
    const max = Math.max(...vals);
    const range = max - min || 1;
    const w = 200, h = 50;
    const path = vals.map((v, i) => {
      const x = (i / (points - 1)) * w;
      const y = h - ((v - min) / range) * h;
      return (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none"><path d="${path}" fill="none" stroke="${panel.color}" stroke-width="1.5" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>`;
  }
  function esc(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
  function computeTier(panel) {
    if (panel.manualTier) return panel.manualTier;
    const score = panel.attention.score || 0;
    if (score >= TIER_THRESHOLDS.hero) return 'hero';
    if (score >= TIER_THRESHOLDS.large) return 'large';
    if (score >= TIER_THRESHOLDS.medium) return 'medium';
    if (score >= TIER_THRESHOLDS.compact) return 'compact';
    return 'mini';
  }
  function setupPanelInteractivity(el, panel) {
    el.addEventListener('click', (e) => {
      const action = e.target.dataset.action || e.target.closest('[data-action]')?.dataset.action;
      if (action === 'toggle-lock') {
        panel.locked = !panel.locked;
        updatePanelElement(el, panel);
        el.draggable = panel.locked;
        persistState();
        toast(panel.locked ? 'Locked: ' + panel.title : 'Unlocked: ' + panel.title);
        return;
      }
      if (action === 'promote') {
        boostPanel(panel, 0.15);
        recomputeLayout();
        e.stopPropagation();
        return;
      }
      if (action === 'demote') {
        boostPanel(panel, -0.15);
        recomputeLayout();
        e.stopPropagation();
        return;
      }
      recordInteraction(panel, 'click');
    });
    el.addEventListener('mouseenter', () => {
      recordInteraction(panel, 'hover');
    });
    el.addEventListener('focusin', () => {
      recordInteraction(panel, 'focus');
    });
  }
  function recordInteraction(panel, type) {
    if (state.reducedPower && type !== 'click') return;
    panel.attention.interactionCount++;
    panel.attention.lastInteraction = Date.now();
    state.lastActivity = Date.now();
    if (state.idleTimer) {
      clearTimeout(state.idleTimer);
      state.idleTimer = null;
    }
    updateAttentionScore(panel);
    scheduleRecompute();
    persistState();
  }
  function boostPanel(panel, amount) {
    const clamped = Math.max(0, Math.min(1, (panel.attention.score || 0) + amount));
    panel.attention.score = clamped;
    panel.attention.lastInteraction = Date.now();
  }
  function updateAttentionScore(panel) {
    const a = panel.attention;
    const now = Date.now();
    const hoursSinceLast = Math.max(0, (now - a.lastInteraction) / 3600000);
    const recencyFactor = Math.pow(0.5, hoursSinceLast / DECAY_HALF_LIFE_HOURS);
    const maxFreq = Math.max(1, ...Object.values(state.panels).map(p => p.attention.interactionCount));
    const maxDur = Math.max(1, ...Object.values(state.panels).map(p => p.attention.viewDuration));
    const freqNorm = Math.min(1, a.interactionCount / maxFreq);
    const durNorm = Math.min(1, a.viewDuration / maxDur);
    a.score = (freqNorm * SCORE_WEIGHTS.frequency)
            + (durNorm * SCORE_WEIGHTS.duration)
            + (recencyFactor * SCORE_WEIGHTS.recency);
  }
  function recomputeLayout() {
    Object.values(state.panels).forEach(p => updateAttentionScore(p));
    const sorted = Object.values(state.panels).sort((a, b) => {
      if (a.locked && b.locked) return 0;
      if (a.locked) return -1;
      if (b.locked) return 1;
      return b.attention.score - a.attention.score;
    });
    sorted.forEach((p, i) => { p.attention.rank = i + 1; });
    const container = document.getElementById('dashboard');
    const els = container.querySelectorAll('.panel');
    els.forEach(el => {
      const panel = state.panels[el.dataset.panelId];
      if (!panel) return;
      const tier = computeTier(panel);
      el.dataset.tier = tier;
      el.classList.toggle('locked', panel.locked);
      el.draggable = panel.locked;
      const body = el.querySelector('.panel-body');
      if (body && tier === 'mini' && !body.querySelector('.mini-content')) {
        body.innerHTML = buildPanelBodyHTML(panel);
      } else if (body && tier !== 'mini' && body.querySelector('.mini-content')) {
        body.innerHTML = buildPanelBodyHTML(panel);
      }
      const rankBadge = el.querySelector('.rank-badge');
      if (rankBadge) rankBadge.textContent = '#' + panel.attention.rank;
      const lockBtn = el.querySelector('.lock-btn');
      if (lockBtn) {
        lockBtn.textContent = panel.locked ? 'L' : 'U';
        lockBtn.classList.toggle('locked', panel.locked);
      }
      el.classList.toggle('hot', panel.attention.score >= TIER_THRESHOLDS.large);
    });
    const sortedEls = Array.from(els).sort((a, b) => {
      const ap = state.panels[a.dataset.panelId];
      const bp = state.panels[b.dataset.panelId];
      if (!ap || !bp) return 0;
      if (ap.locked && !bp.locked) return -1;
      if (!ap.locked && bp.locked) return 1;
      return ap.attention.rank - bp.attention.rank;
    });
    const fragment = document.createDocumentFragment();
    sortedEls.forEach(el => fragment.appendChild(el));
    container.appendChild(fragment);
    persistState();
  }
  function scheduleRecompute() {
    if (state.recomputeDebounce) clearTimeout(state.recomputeDebounce);
    state.recomputeDebounce = setTimeout(recomputeLayout, DEBOUNCE_MS);
  }
  function setupObservers() {
    state.visibilityObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const el = entry.target;
        const panel = state.panels[el.dataset.panelId];
        if (!panel) continue;
        if (entry.isIntersecting) {
          el.dataset.visibleSince = Date.now();
          recordInteraction(panel, 'view-enter');
        } else {
          const since = parseInt(el.dataset.visibleSince);
          if (since) {
            const duration = (Date.now() - since) / 1000;
            panel.attention.viewDuration += duration;
            delete el.dataset.visibleSince;
            scheduleRecompute();
          }
        }
      }
    }, { threshold: 0.3 });
    state.resizeObserver = new ResizeObserver(() => {
      if (state.resizeRAF) cancelAnimationFrame(state.resizeRAF);
      state.resizeRAF = requestAnimationFrame(() => {
        recomputeLayout();
        if (state.heatmapEnabled) drawHeatmap();
      });
    });
    state.resizeObserver.observe(document.getElementById('dashboard'));
    state.mutationObserver = new MutationObserver((mutations) => {
      let needsRecompute = false;
      for (const m of mutations) {
        if (m.type === 'childList' || (m.type === 'attributes' && m.attributeName === 'data-tier')) {
          needsRecompute = true;
          break;
        }
      }
      if (needsRecompute) scheduleRecompute();
    });
    state.mutationObserver.observe(document.getElementById('dashboard'), {
      childList: true,
      attributes: true,
      subtree: true,
      attributeFilter: ['data-tier', 'class'],
    });
    document.querySelectorAll('.panel').forEach(el => {
      state.visibilityObserver.observe(el);
    });
    const origRender = renderDashboard;
    renderDashboard = function() {
      origRender();
      document.querySelectorAll('.panel').forEach(el => {
        state.visibilityObserver.observe(el);
      });
    };
  }
  function setupVisibility() {
    document.addEventListener('visibilitychange', () => {
      const hidden = document.hidden;
      state.reducedPower = hidden;
      document.body.classList.toggle('reduced-power', hidden);
      document.body.classList.toggle('reduced-motion', hidden);
      document.getElementById('power-badge').textContent = hidden ? 'low-power' : 'full';
      document.getElementById('view-state').textContent = hidden ? 'hidden' : 'active';
      if (!hidden) {
        state.lastActivity = Date.now();
        recomputeLayout();
      } else {
        const now = Date.now();
        document.querySelectorAll('.panel[data-visible-since]').forEach(el => {
          const panel = state.panels[el.dataset.panelId];
          if (!panel) return;
          const since = parseInt(el.dataset.visibleSince);
          if (since) {
            panel.attention.viewDuration += (now - since) / 1000;
            delete el.dataset.visibleSince;
          }
        });
      }
    });
    document.addEventListener('mousemove', throttle(() => {
      state.lastActivity = Date.now();
      if (state.heatmapEnabled) {
        state.attentionPoints.push({ x: event.clientX, y: event.clientY, t: Date.now() });
        if (state.attentionPoints.length > 300) state.attentionPoints.shift();
        if (state.heatmapRAF) cancelAnimationFrame(state.heatmapRAF);
        state.heatmapRAF = requestAnimationFrame(drawHeatmap);
      }
    }, 50));
    document.addEventListener('scroll', throttle(() => {
      state.lastActivity = Date.now();
    }, 200), { passive: true });
    document.addEventListener('keydown', () => {
      state.lastActivity = Date.now();
      if (state.reducedPower) {
        state.reducedPower = false;
        document.body.classList.remove('reduced-power', 'reduced-motion');
        document.getElementById('power-badge').textContent = 'full';
      }
    });
    state.idleTimer = setInterval(() => {
      if (Date.now() - state.lastActivity > 120000 && !state.reducedPower) {
        state.reducedPower = true;
        document.body.classList.add('reduced-power', 'reduced-motion');
        document.getElementById('power-badge').textContent = 'idle-save';
      }
    }, 30000);
  }
  function setupDragDrop() {
    const container = document.getElementById('dashboard');
    let draggedEl = null;
    container.addEventListener('dragstart', (e) => {
      const panel = e.target.closest('.panel');
      if (!panel) return;
      const data = state.panels[panel.dataset.panelId];
      if (!data || !data.locked) { e.preventDefault(); return; }
      draggedEl = panel;
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', panel.dataset.panelId);
    });
    container.addEventListener('dragend', (e) => {
      if (draggedEl) {
        draggedEl.classList.remove('dragging');
        draggedEl = null;
      }
      container.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    });
    container.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      const target = e.target.closest('.panel');
      container.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
      if (target && target !== draggedEl) {
        target.classList.add('drag-over');
      }
    });
    container.addEventListener('drop', (e) => {
      e.preventDefault();
      const target = e.target.closest('.panel');
      if (!target || !draggedEl || target === draggedEl) return;
      const fromId = draggedEl.dataset.panelId;
      const toId = target.dataset.panelId;
      if (fromId === toId) return;
      const containerEl = document.getElementById('dashboard');
      const children = Array.from(containerEl.children);
      const fromIdx = children.indexOf(draggedEl);
      const toIdx = children.indexOf(target);
      if (fromIdx === -1 || toIdx === -1) return;
      if (fromIdx < toIdx) {
        containerEl.insertBefore(draggedEl, target.nextSibling);
      } else {
        containerEl.insertBefore(draggedEl, target);
      }
      const fromPanel = state.panels[fromId];
      const toPanel = state.panels[toId];
      if (fromPanel && toPanel) {
        const tmpRank = fromPanel.attention.rank;
        fromPanel.attention.rank = toPanel.attention.rank;
        toPanel.attention.rank = tmpRank;
      }
      target.classList.remove('drag-over');
      toast('Reordered: ' + (fromPanel?.title || fromId) + ' <-> ' + (toPanel?.title || toId));
      scheduleRecompute();
    });
  }
  function setupHeatmap() {
    state.heatmapCanvas = document.getElementById('heatmap-canvas');
    state.heatmapCtx = state.heatmapCanvas.getContext('2d');
    const heatmapObserver = new ResizeObserver(() => {
      state.heatmapCanvas.width = window.innerWidth;
      state.heatmapCanvas.height = window.innerHeight;
    });
    heatmapObserver.observe(document.body);
    state.heatmapCanvas.width = window.innerWidth;
    state.heatmapCanvas.height = window.innerHeight;
    document.getElementById('btn-heatmap').addEventListener('click', () => {
      state.heatmapEnabled = !state.heatmapEnabled;
      document.getElementById('heatmap-overlay').style.display = state.heatmapEnabled ? 'block' : 'none';
      document.getElementById('btn-heatmap').classList.toggle('active', state.heatmapEnabled);
      if (state.heatmapEnabled) drawHeatmap();
    });
  }
  function drawHeatmap() {
    if (!state.heatmapEnabled) return;
    const canvas = state.heatmapCanvas;
    const ctx = state.heatmapCtx;
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const points = state.attentionPoints.filter(p => Date.now() - p.t < 30000);
    if (points.length < 2) return;
    for (const pt of points) {
      const age = (Date.now() - pt.t) / 30000;
      const alpha = Math.max(0, 0.3 * (1 - age));
      const gradient = ctx.createRadialGradient(pt.x, pt.y, 0, pt.x, pt.y, 60);
      gradient.addColorStop(0, `rgba(108,140,255,${alpha})`);
      gradient.addColorStop(0.5, `rgba(108,140,255,${alpha * 0.5})`);
      gradient.addColorStop(1, 'rgba(108,140,255,0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(pt.x - 60, pt.y - 60, 120, 120);
    }
  }
  function throttle(fn, ms) {
    let last = 0;
    return function(...args) {
      const now = Date.now();
      if (now - last >= ms) { last = now; fn.apply(this, args); }
    };
  }
  function toast(msg) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2000);
  }
  document.getElementById('btn-reset').addEventListener('click', () => {
    if (!confirm('Clear all tracking data and reset layout?')) return;
    localStorage.removeItem(STORAGE_KEY);
    state.panels = {};
    PANEL_DEFS.forEach(def => { state.panels[def.id] = defaultPanelData(def.id); });
    renderDashboard();
    recomputeLayout();
    toast('Layout data reset');
    setupObservers();
  });
  document.getElementById('btn-compact').addEventListener('click', () => {
    state.compactView = !state.compactView;
    document.getElementById('dashboard').classList.toggle('compact-view', state.compactView);
    document.getElementById('btn-compact').classList.toggle('active', state.compactView);
  });
  document.getElementById('btn-unlock-all').addEventListener('click', () => {
    Object.values(state.panels).forEach(p => { p.locked = false; });
    recomputeLayout();
    toast('All panels unlocked');
  });
  document.getElementById('btn-rearrange').addEventListener('click', () => {
    recomputeLayout();
    toast('Layout recomputed');
  });
  window.addEventListener('beforeunload', () => {
    const now = Date.now();
    document.querySelectorAll('.panel[data-visible-since]').forEach(el => {
      const panel = state.panels[el.dataset.panelId];
      if (!panel) return;
      const since = parseInt(el.dataset.visibleSince);
      if (since) {
        panel.attention.viewDuration += (now - since) / 1000;
        delete el.dataset.visibleSince;
      }
    });
    persistState();
  });
  init();
  setTimeout(() => {
    const activePanels = Object.values(state.panels).filter(p => p.attention.interactionCount === 0);
    activePanels.forEach(p => {
      p.attention.score = 0.05 + Math.random() * 0.1;
      p.attention.lastInteraction = Date.now() - Math.random() * 86400000;
    });
    recomputeLayout();
  }, 500);
})();
</script>
</body>
</html>