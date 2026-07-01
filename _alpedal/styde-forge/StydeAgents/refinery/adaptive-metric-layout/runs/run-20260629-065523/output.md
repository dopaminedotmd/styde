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
    --surface2: #242836;
    --border: #2e3344;
    --text: #e1e4ed;
    --text2: #949ab0;
    --accent: #6c8cff;
    --accent2: #4ade80;
    --warn: #f59e0b;
    --radius: 10px;
    --gap: 12px;
    --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  @media (prefers-reduced-motion: reduce) {
    :root { --transition: 0s; }
    * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 16px;
  }
  .toolbar {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    align-items: center;
  }
  .btn {
    background: var(--surface2);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    transition: background var(--transition);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .btn:hover { background: var(--border); }
  .btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .grid {
    display: grid;
    gap: var(--gap);
    transition: grid-template-columns var(--transition), grid-template-rows var(--transition);
    contain: layout style;
  }
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all var(--transition);
    position: relative;
    contain: layout style paint;
  }
  .panel.large { grid-column: span 3; grid-row: span 2; }
  .panel.medium { grid-column: span 2; grid-row: span 1; }
  .panel.compact {
    grid-column: span 1;
    grid-row: span 1;
    opacity: 0.65;
    max-height: 160px;
  }
  .panel.compact .panel-body { display: none; }
  .panel.compact .panel-preview { display: flex; }
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    cursor: grab;
    user-select: none;
    min-height: 42px;
  }
  .panel-header:active { cursor: grabbing; }
  .panel-title {
    font-weight: 600;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .panel-actions {
    display: flex;
    gap: 4px;
    align-items: center;
  }
  .icon-btn {
    background: none;
    border: none;
    color: var(--text2);
    cursor: pointer;
    padding: 4px 6px;
    border-radius: 4px;
    font-size: 16px;
    line-height: 1;
    transition: color var(--transition), background var(--transition);
  }
  .icon-btn:hover { color: var(--text); background: var(--border); }
  .icon-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .icon-btn.locked { color: var(--warn); }
  .panel-body {
    padding: 14px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
  }
  .panel-preview {
    display: none;
    padding: 10px 14px;
    font-size: 12px;
    color: var(--text2);
    gap: 12px;
    align-items: center;
    flex: 1;
    min-height: 60px;
  }
  .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 13px;
  }
  .metric-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--accent2);
    font-variant-numeric: tabular-nums;
  }
  .metric-label { color: var(--text2); font-size: 12px; }
  .spark {
    height: 60px;
    width: 100%;
    border-radius: 6px;
    background: var(--surface2);
  }
  .spark svg { width: 100%; height: 100%; }
  .heatmap {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 3px;
    height: 80px;
  }
  .heatmap-cell {
    border-radius: 3px;
    transition: background var(--transition);
  }
  .rank-badge {
    font-size: 10px;
    background: var(--accent);
    color: #fff;
    padding: 1px 6px;
    border-radius: 8px;
    font-weight: 700;
  }
  .drag-hint {
    position: absolute;
    inset: 0;
    background: rgba(108, 140, 255, 0.08);
    border: 2px dashed var(--accent);
    border-radius: var(--radius);
    pointer-events: none;
    z-index: 2;
    display: none;
  }
  .panel.drag-over .drag-hint { display: block; }
  .toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 13px;
    z-index: 100;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.2s, transform 0.2s;
    pointer-events: none;
  }
  .toast.show { opacity: 1; transform: translateY(0); }
  .sr-only {
    position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
    overflow: hidden; clip: rect(0,0,0,0); border: 0;
  }
</style>
</head>
<body>
<header class="toolbar" role="toolbar" aria-label="Dashboard controls">
  <button class="btn active" id="btnAuto" aria-pressed="true" onclick="toggleMode()">
    Auto-Layout
  </button>
  <button class="btn" id="btnReset" onclick="resetLayout()">
    Reset Layout
  </button>
  <button class="btn" id="btnStats" onclick="showStats()">
    Usage Stats
  </button>
  <span style="margin-left:auto;font-size:12px;color:var(--text2)" id="statusText">
    Learning from your behavior...
  </span>
</header>
<div class="grid" id="grid" role="list" aria-label="Dashboard panels">
</div>
<div class="toast" id="toast" aria-live="polite"></div>
<script>
(function() {
  'use strict';
  const METRICS = [
    { id: 'revenue',    title: 'Revenue',         metric: '$',  base: 124000, variance: 0.02, color: '#4ade80' },
    { id: 'users',      title: 'Active Users',     metric: '',   base: 8700,   variance: 0.03, color: '#6c8cff' },
    { id: 'conversion', title: 'Conversion Rate',  metric: '%',  base: 3.8,    variance: 0.05, color: '#f59e0b' },
    { id: 'latency',    title: 'API Latency',      metric: 'ms', base: 142,    variance: 0.06, color: '#ef4444' },
    { id: 'errors',     title: 'Error Rate',       metric: '%',  base: 0.42,   variance: 0.10, color: '#ef4444' },
    { id: 'throughput', title: 'Throughput',       metric: '/s',  base: 3200,   variance: 0.04, color: '#8b5cf6' },
    { id: 'storage',    title: 'Storage Usage',    metric: '%',  base: 67,     variance: 0.02, color: '#ec4899' },
    { id: 'nps',        title: 'NPS Score',        metric: '',   base: 72,     variance: 0.03, color: '#14b8a6' },
  ];
  const STORAGE_KEY = 'adaptive_dashboard_v1';
  const MAX_HISTORY = 200;
  let panels = METRICS.map((m, i) => ({
    ...m,
    order: i,
    size: i < 4 ? 'large' : (i < 6 ? 'medium' : 'compact'),
    locked: false,
    viewStart: 0,
    totalViewMs: 0,
    interactions: 0,
    lastInteract: Date.now(),
    collapsed: false,
  }));
  let tracking = {
    activePanelId: null,
    focusStart: 0,
    observers: [],
  };
  let state = {
    autoMode: true,
    interactionCount: 0,
    lastArrange: Date.now(),
  };
  let toastTimer = 0;
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      if (!saved || !saved.panels) return;
      const byId = Object.fromEntries(panels.map(p => [p.id, p]));
      for (const sp of saved.panels) {
        const p = byId[sp.id];
        if (!p) continue;
        p.order = sp.order ?? p.order;
        p.size = sp.size ?? p.size;
        p.locked = sp.locked ?? p.locked;
        p.totalViewMs = sp.totalViewMs ?? p.totalViewMs;
        p.interactions = sp.interactions ?? p.interactions;
        p.lastInteract = sp.lastInteract ?? p.lastInteract;
        p.collapsed = sp.collapsed ?? p.collapsed;
      }
      if (saved.autoMode != null) state.autoMode = saved.autoMode;
    } catch (e) { /* corrupt, ignore */ }
  }
  function saveState() {
    const data = {
      panels: panels.map(p => ({
        id: p.id,
        order: p.order,
        size: p.size,
        locked: p.locked,
        totalViewMs: p.totalViewMs,
        interactions: p.interactions,
        lastInteract: p.lastInteract,
        collapsed: p.collapsed,
      })),
      autoMode: state.autoMode,
    };
    requestAnimationFrame(() => {
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch(e) {}
    });
  }
  let savePending = false;
  function debouncedSave() {
    if (savePending) return;
    savePending = true;
    requestAnimationFrame(() => {
      saveState();
      savePending = false;
    });
  }
  function attentionScore(p) {
    const now = Date.now();
    const hoursAgo = Math.max(0.01, (now - p.lastInteract) / 3600000);
    const recency = 1 / Math.log(2 + hoursAgo);
    const durationSec = p.totalViewMs / 1000;
    return (p.interactions * 0.35 + durationSec * 0.45 + recency * 0.20);
  }
  function rankPanels() {
    return panels.map((p, i) => ({ ...p, idx: i, score: attentionScore(p) }))
      .sort((a, b) => b.score - a.score);
  }
  function assignSizes(ranked) {
    const total = ranked.length;
    const largeCount = Math.min(2, Math.ceil(total * 0.25));
    const mediumCount = Math.min(3, Math.ceil(total * 0.35));
    ranked.forEach((r, i) => {
      if (r.locked) return;
      if (i < largeCount) r.size = 'large';
      else if (i < largeCount + mediumCount) r.size = 'medium';
      else r.size = 'compact';
    });
  }
  function arrangeLayout() {
    if (!state.autoMode) return;
    const ranked = rankPanels();
    assignSizes(ranked);
    ranked.sort((a, b) => {
      if (a.locked && !b.locked) return -1;
      if (!a.locked && b.locked) return 1;
      return a.score > b.score ? -1 : a.score < b.score ? 1 : 0;
    });
    ranked.forEach((r, i) => { r.order = i; });
    // Write back
    ranked.forEach(r => {
      const p = panels[r.idx];
      p.order = r.order;
      if (!p.locked) p.size = r.size;
    });
    panels.sort((a, b) => a.order - b.order);
    state.lastArrange = Date.now();
  }
  function renderGrid() {
    const grid = document.getElementById('grid');
    const sorted = [...panels].sort((a, b) => a.order - b.order);
    const total = sorted.length;
    const cols = Math.min(6, Math.max(3, Math.ceil(Math.sqrt(total * 2))));
    grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    const existing = new Map();
    for (const el of grid.querySelectorAll('.panel')) {
      existing.set(el.dataset.panelId, el);
    }
    const fragment = document.createDocumentFragment();
    sorted.forEach((p, i) => {
      let el = existing.get(p.id);
      if (el) {
        existing.delete(p.id);
        el.style.order = i;
      } else {
        el = createPanelElement(p);
        el.style.order = i;
      }
      updatePanelElement(el, p);
      fragment.appendChild(el);
    });
    for (const [_, el] of existing) {
      teardownPanel(el);
      el.remove();
    }
    grid.innerHTML = '';
    grid.appendChild(fragment);
    setupObservers();
  }
  function createPanelElement(p) {
    const el = document.createElement('div');
    el.className = 'panel';
    el.dataset.panelId = p.id;
    el.setAttribute('role', 'listitem');
    el.setAttribute('aria-label', p.title + ' panel');
    el.tabIndex = 0;
    el.innerHTML =
      '<div class="drag-hint" aria-hidden="true"></div>' +
      '<div class="panel-header" draggable="true" aria-grabbed="false">' +
        '<span class="panel-title">' +
          '<span class="rank-badge" aria-hidden="true">#' + (p.order + 1) + '</span>' +
          escapeHtml(p.title) +
        '</span>' +
        '<div class="panel-actions">' +
          '<button class="icon-btn lock-btn" aria-label="' + (p.locked ? 'Unlock' : 'Lock') + ' position">' + (p.locked ? '\uD83D\uDD12' : '\uD83D\uDD13') + '</button>' +
          '<button class="icon-btn collapse-btn" aria-label="' + (p.collapsed ? 'Expand' : 'Collapse') + ' panel">' + (p.collapsed ? '\u25B6' : '\u25BC') + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body"></div>' +
      '<div class="panel-preview">' +
        '<span class="metric-value" style="font-size:18px">' + formatMetric(p) + '</span>' +
        '<span style="font-size:11px;color:var(--text2)">Click to expand</span>' +
      '</div>';
    bindPanelEvents(el, p);
    return el;
  }
  function updatePanelElement(el, p) {
    const badge = el.querySelector('.rank-badge');
    if (badge) badge.textContent = '#' + (p.order + 1);
    el.className = 'panel ' + p.size;
    if (p.collapsed) el.classList.add('compact');
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.setAttribute('aria-label', (p.locked ? 'Unlock' : 'Lock') + ' position');
      lockBtn.innerHTML = p.locked ? '\uD83D\uDD12' : '\uD83D\uDD13';
      lockBtn.classList.toggle('locked', p.locked);
    }
    const collapseBtn = el.querySelector('.collapse-btn');
    if (collapseBtn) {
      collapseBtn.setAttribute('aria-label', (p.collapsed ? 'Expand' : 'Collapse') + ' panel');
      collapseBtn.innerHTML = p.collapsed ? '\u25B6' : '\u25BC';
    }
    const body = el.querySelector('.panel-body');
    if (body && !p.collapsed) {
      body.innerHTML = renderPanelContent(p);
    }
    const preview = el.querySelector('.panel-preview');
    if (preview) {
      const previewVal = preview.querySelector('.metric-value');
      if (previewVal) previewVal.textContent = formatMetric(p);
    }
  }
  function renderPanelContent(p) {
    const val = formatMetric(p);
    const sparkData = generateSparkline(p, 40);
    return (
      '<div class="metric-row">' +
        '<span class="metric-label">Current</span>' +
        '<span class="metric-value">' + val + '</span>' +
      '</div>' +
      '<div class="spark">' + sparkData + '</div>' +
      '<div class="metric-row" style="margin-top:4px">' +
        '<span class="metric-label">Interactions</span>' +
        '<span>' + p.interactions + '</span>' +
      '</div>' +
      '<div class="metric-row">' +
        '<span class="metric-label">View Time</span>' +
        '<span>' + formatDuration(p.totalViewMs) + '</span>' +
      '</div>'
    );
  }
  function generateSparkline(p, points) {
    const seed = hashStr(p.id + '_spark');
    const vals = [];
    let v = p.base;
    for (let i = 0; i < points; i++) {
      v = v * (1 + (seededRandom(seed + i) - 0.5) * p.variance);
      vals.push(v);
    }
    const min = Math.min(...vals) * 0.95;
    const max = Math.max(...vals) * 1.05;
    const range = max - min || 1;
    const height = 60;
    const width = 200;
    const path = vals.map((v, i) => {
      const x = (i / (points - 1)) * width;
      const y = height - ((v - min) / range) * (height - 8) - 4;
      return (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    return '<svg viewBox="0 0 ' + width + ' ' + height + '" aria-hidden="true"><path d="' + path + '" fill="none" stroke="' + p.color + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function formatMetric(p) {
    const val = p.base * (1 + (seededRandom(hashStr(p.id + '_' + Date.now() / 30000)) - 0.5) * p.variance * 2);
    if (p.metric === '$') return '$' + val.toLocaleString(undefined, {maximumFractionDigits: 0});
    if (p.metric === '%') return val.toFixed(1) + '%';
    if (p.metric === 'ms') return Math.round(val) + 'ms';
    if (p.metric === '/s') return Math.round(val).toLocaleString() + '/s';
    return Math.round(val).toLocaleString();
  }
  function formatDuration(ms) {
    if (ms < 1000) return Math.round(ms) + 'ms';
    if (ms < 60000) return (ms / 1000).toFixed(0) + 's';
    return (ms / 60000).toFixed(1) + 'min';
  }
  function seededRandom(seed) {
    let s = seed | 0;
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return (s % 10000) / 10000;
  }
  function hashStr(s) {
    let h = 0;
    for (let i = 0; i < s.length; i++) {
      h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    }
    return h;
  }
  function escapeHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function bindPanelEvents(el, p) {
    const header = el.querySelector('.panel-header');
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.onclick = (e) => {
        e.stopPropagation();
        p.locked = !p.locked;
        recordInteraction(p);
        updatePanelElement(el, p);
        if (p.locked) arrangeLayout();
        debouncedSave();
        toast(p.locked ? 'Panel locked in position' : 'Panel unlocked');
      };
    }
    const collapseBtn = el.querySelector('.collapse-btn');
    if (collapseBtn) {
      collapseBtn.onclick = (e) => {
        e.stopPropagation();
        p.collapsed = !p.collapsed;
        recordInteraction(p);
        updatePanelElement(el, p);
        debouncedSave();
        toast(p.collapsed ? 'Panel collapsed' : 'Panel expanded');
      };
    }
    el.onclick = () => {
      recordInteraction(p);
      if (p.collapsed) {
        p.collapsed = false;
        updatePanelElement(el, p);
        debouncedSave();
        arrangeLayout();
        renderGrid();
      }
    };
    el.onkeydown = (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        recordInteraction(p);
        if (p.collapsed) {
          p.collapsed = false;
          updatePanelElement(el, p);
          debouncedSave();
          arrangeLayout();
          renderGrid();
        }
      }
    };
    // Drag and drop reorder
    header.addEventListener('dragstart', (e) => {
      if (!state.autoMode) return;
      e.dataTransfer.setData('text/plain', p.id);
      e.dataTransfer.effectAllowed = 'move';
      header.setAttribute('aria-grabbed', 'true');
      recordInteraction(p);
    });
    header.addEventListener('dragend', (e) => {
      header.setAttribute('aria-grabbed', 'false');
      document.querySelectorAll('.drag-over').forEach(d => d.classList.remove('drag-over'));
    });
    el.addEventListener('dragover', (e) => {
      if (!state.autoMode) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      el.classList.add('drag-over');
    });
    el.addEventListener('dragleave', () => { el.classList.remove('drag-over'); });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      el.classList.remove('drag-over');
      if (!state.autoMode) return;
      const srcId = e.dataTransfer.getData('text/plain');
      if (!srcId || srcId === p.id) return;
      const src = panels.find(pp => pp.id === srcId);
      const dst = p;
      if (!src || !dst) return;
      const srcOrder = src.order;
      const dstOrder = dst.order;
      panels.forEach(pp => {
        if (pp.order === srcOrder) pp.order = dstOrder;
        else if (pp.order === dstOrder) pp.order = srcOrder;
      });
      recordInteraction(src);
      debouncedSave();
      renderGrid();
      toast('Panels swapped');
    });
    // View duration tracking via focus
    el.addEventListener('focusin', () => startView(p));
    el.addEventListener('focusout', () => endView(p));
    el.addEventListener('mouseenter', () => startView(p));
    el.addEventListener('mouseleave', () => endView(p));
  }
  function teardownPanel(el) {
    // Weak cleanup: just nullify listeners via replacing node (handled by re-render)
  }
  function startView(p) {
    if (tracking.activePanelId === p.id) return;
    if (tracking.activePanelId) {
      const prev = panels.find(pp => pp.id === tracking.activePanelId);
      if (prev) endView(prev);
    }
    tracking.activePanelId = p.id;
    tracking.focusStart = performance.now();
  }
  function endView(p) {
    if (tracking.activePanelId !== p.id) return;
    const elapsed = performance.now() - tracking.focusStart;
    if (elapsed > 0 && elapsed < 600000) {
      p.totalViewMs += elapsed;
    }
    tracking.activePanelId = null;
    tracking.focusStart = 0;
    state.interactionCount++;
    p.lastInteract = Date.now();
    debouncedSave();
    // Event-driven layout update after significant interaction
    if (state.interactionCount >= 5) {
      state.interactionCount = 0;
      if (Date.now() - state.lastArrange > 2000) {
        arrangeLayout();
        renderGrid();
      } else {
        scheduleArrange();
      }
    }
  }
  let arrangeScheduled = false;
  function scheduleArrange() {
    if (arrangeScheduled) return;
    arrangeScheduled = true;
    requestAnimationFrame(() => {
      arrangeLayout();
      renderGrid();
      arrangeScheduled = false;
      state.interactionCount = 0;
    });
  }
  function recordInteraction(p) {
    p.interactions++;
    p.lastInteract = Date.now();
    state.interactionCount++;
    debouncedSave();
    if (state.interactionCount >= 5) {
      scheduleArrange();
    }
  }
  function setupObservers() {
    // Clean old observers
    tracking.observers.forEach(o => o.disconnect());
    tracking.observers = [];
    // MutationObserver on grid for structural changes
    const grid = document.getElementById('grid');
    if (!grid) return;
    const mo = new MutationObserver((mutations) => {
      // Detect panel additions/removals and re-rank
      let significant = false;
      for (const m of mutations) {
        if (m.type === 'childList' && (m.addedNodes.length > 0 || m.removedNodes.length > 0)) {
          significant = true;
          break;
        }
      }
      if (significant && state.autoMode) {
        state.interactionCount = 5;
        scheduleArrange();
      }
    });
    mo.observe(grid, { childList: true, subtree: false });
    tracking.observers.push(mo);
    // VisibilityObserver for viewport-based tracking
    if (typeof IntersectionObserver !== 'undefined') {
      const io = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          const pid = entry.target.dataset.panelId;
          if (!pid) continue;
          const p = panels.find(pp => pp.id === pid);
          if (!p) continue;
          if (entry.isIntersecting) {
            if (tracking.activePanelId !== pid) startView(p);
          } else {
            if (tracking.activePanelId === pid) endView(p);
          }
        }
      }, { threshold: 0.5 });
      for (const el of grid.querySelectorAll('.panel')) {
        io.observe(el);
      }
      tracking.observers.push(io);
    }
  }
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2000);
  }
  window.toggleMode = function() {
    state.autoMode = !state.autoMode;
    const btn = document.getElementById('btnAuto');
    btn.classList.toggle('active', state.autoMode);
    btn.setAttribute('aria-pressed', state.autoMode);
    btn.textContent = state.autoMode ? 'Auto-Layout' : 'Manual Layout';
    document.getElementById('statusText').textContent =
      state.autoMode ? 'Learning from your behavior...' : 'Manual mode — drag panels freely';
    debouncedSave();
    if (state.autoMode) {
      arrangeLayout();
      renderGrid();
    }
    toast(state.autoMode ? 'Auto-layout enabled' : 'Manual layout — drag to rearrange');
  };
  window.resetLayout = function() {
    panels.forEach((p, i) => {
      p.order = i;
      p.size = i < 4 ? 'large' : (i < 6 ? 'medium' : 'compact');
      p.locked = false;
      p.totalViewMs = 0;
      p.interactions = 0;
      p.lastInteract = Date.now();
      p.collapsed = false;
    });
    saveState();
    if (state.autoMode) arrangeLayout();
    renderGrid();
    toast('Layout reset');
  };
  window.showStats = function() {
    const ranked = rankPanels();
    const lines = ranked.map((r, i) =>
      (i + 1) + '. ' + r.title + ' \u2014 score: ' + r.score.toFixed(2) +
      ' | interactions: ' + r.interactions +
      ' | view: ' + formatDuration(r.totalViewMs)
    );
    toast('Top panel: ' + ranked[0].title + ' (' + ranked[0].score.toFixed(1) + ')');
    console.log('=== Dashboard Usage Stats ===');
    console.log(lines.join('\n'));
  };
  function init() {
    loadState();
    arrangeLayout();
    renderGrid();
    const btn = document.getElementById('btnAuto');
    btn.classList.toggle('active', state.autoMode);
    btn.setAttribute('aria-pressed', state.autoMode);
    btn.textContent = state.autoMode ? 'Auto-Layout' : 'Manual Layout';
    document.getElementById('statusText').textContent =
      state.autoMode ? 'Learning from your behavior...' : 'Manual mode — drag panels freely';
  }
  init();
})();
</script>
</body>
</html>