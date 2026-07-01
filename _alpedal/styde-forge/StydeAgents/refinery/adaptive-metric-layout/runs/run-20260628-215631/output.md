<!-- ARTIFACT_START -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f1117; color: #e1e4e8; min-height: 100vh; }
.header { padding: 16px 24px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 1.25rem; font-weight: 600; color: #f0f6fc; }
.header-controls { display: flex; gap: 12px; align-items: center; }
.btn { padding: 6px 14px; border-radius: 6px; border: 1px solid #30363d; background: #21262d; color: #c9d1d9; cursor: pointer; font-size: 0.8rem; }
.btn:hover { background: #30363d; }
.btn-primary { background: #238636; border-color: #2ea043; color: #fff; }
.btn-primary:hover { background: #2ea043; }
.btn-danger { background: #da3633; border-color: #f85149; color: #fff; }
.btn-danger:hover { background: #f85149; }
.stats-bar { display: flex; gap: 16px; padding: 8px 24px; background: #161b22; border-bottom: 1px solid #21262d; font-size: 0.75rem; color: #8b949e; }
.stats-bar span { display: flex; align-items: center; gap: 4px; }
.dashboard-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 16px; transition: grid-template-columns 0.3s; }
.panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; min-height: 120px; display: flex; flex-direction: column; }
.panel.locked { border-color: #58a6ff; box-shadow: 0 0 0 1px #58a6ff40; }
.panel.compact { min-height: 48px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-footer { display: none; }
.panel.compact .panel-header { cursor: pointer; }
.panel.preview { min-height: 80px; }
.panel.preview .panel-body { display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: #8b949e; padding: 8px; }
.panel.preview .chart-area { display: none; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #1c2128; border-bottom: 1px solid #21262d; cursor: grab; }
.panel-header:active { cursor: grabbing; }
.panel-title { font-size: 0.8rem; font-weight: 600; color: #c9d1d9; display: flex; align-items: center; gap: 6px; }
.panel-title .indicator { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.panel-title .rank-badge { font-size: 0.65rem; background: #21262d; padding: 1px 6px; border-radius: 10px; color: #8b949e; }
.panel-controls { display: flex; gap: 4px; }
.panel-controls button { background: none; border: none; color: #8b949e; cursor: pointer; padding: 2px 4px; font-size: 0.75rem; border-radius: 4px; }
.panel-controls button:hover { background: #30363d; color: #c9d1d9; }
.panel-controls button.lock-active { color: #58a6ff; }
.panel-body { padding: 12px; flex: 1; display: flex; flex-direction: column; }
.metric-value { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.02em; }
.metric-label { font-size: 0.7rem; color: #8b949e; margin-bottom: 4px; }
.metric-change { font-size: 0.7rem; }
.metric-change.up { color: #3fb950; }
.metric-change.down { color: #f85149; }
.chart-area { flex: 1; min-height: 60px; position: relative; margin-top: 8px; }
.chart-bar { display: flex; align-items: flex-end; gap: 2px; height: 100%; }
.chart-bar div { flex: 1; background: #238636; border-radius: 2px 2px 0 0; min-height: 4px; transition: height 0.3s; }
.chart-bar div:nth-child(odd) { background: #1a7f37; }
.panel-footer { padding: 4px 12px; font-size: 0.65rem; color: #484f58; border-top: 1px solid #21262d; display: flex; justify-content: space-between; }
.panel-footer .track-stats { display: flex; gap: 8px; }
.placeholder-chart { width: 100%; height: 60px; background: linear-gradient(90deg, #1c2128 0%, #21262d 50%, #1c2128 100%); border-radius: 4px; }
.dragging { opacity: 0.5; transform: scale(0.95); z-index: 1000; }
.drag-over { border: 2px dashed #58a6ff; }
.drop-zone { position: absolute; inset: 0; z-index: -1; }
.tooltip { position: fixed; background: #1c2128; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; font-size: 0.75rem; color: #c9d1d9; pointer-events: none; z-index: 9999; display: none; max-width: 200px; }
.panel[data-rank="1"] { grid-column: span 2; grid-row: span 2; }
.panel[data-rank="2"] { grid-column: span 2; }
.panel[data-rank="3"] { grid-column: span 2; }
.panel[data-rank="4"], .panel[data-rank="5"] { grid-column: span 1; }
.panel[data-rank="6"], .panel[data-rank="7"] { grid-column: span 1; }
.panel[data-mode="compact"] .chart-area, .panel[data-mode="compact"] .metric-value { display: none; }
.panel[data-mode="compact"] .panel-body { padding: 4px 12px; flex-direction: row; align-items: center; gap: 8px; }
.panel[data-mode="compact"] .metric-label { margin-bottom: 0; }
.panel.dragging-source { opacity: 0.4; }
.more-section { margin: 0 16px 16px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; }
.more-header { padding: 8px 12px; background: #1c2128; border-bottom: 1px solid #21262d; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #8b949e; }
.more-header:hover { color: #c9d1d9; }
.more-grid { display: none; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 12px; }
.more-grid.open { display: grid; }
.panel[data-mode="miniature"] { min-height: 60px; }
.panel[data-mode="miniature"] .panel-body { display: flex; align-items: center; justify-content: center; padding: 8px; }
.panel[data-mode="miniature"] .metric-value { font-size: 1rem; }
.panel[data-mode="miniature"] .chart-area, .panel[data-mode="miniature"] .panel-footer { display: none; }
@media (max-width: 900px) { .dashboard-grid { grid-template-columns: repeat(2, 1fr); } .panel[data-rank="1"] { grid-column: span 2; grid-row: span 1; } }
@media (max-width: 600px) { .dashboard-grid { grid-template-columns: 1fr; } .panel[data-rank] { grid-column: span 1; } }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="header-controls">
    <span id="sessionLabel" style="font-size:0.75rem;color:#8b949e;">Tracking session</span>
    <button class="btn" onclick="Dashboard.resetTracking()">Reset tracking</button>
    <button class="btn" onclick="Dashboard.forceRecalculate()">Recalculate layout</button>
    <button class="btn btn-danger" onclick="Dashboard.resetLayout()">Reset layout</button>
  </div>
</div>
<div class="stats-bar">
  <span>Panels: <strong id="panelCount">0</strong></span>
  <span>Locked: <strong id="lockedCount">0</strong></span>
  <span>Compact: <strong id="compactCount">0</strong></span>
  <span>Top panel: <strong id="topPanel">-</strong></span>
  <span>Session views: <strong id="totalViews">0</strong></span>
</div>
<div id="dashboardGrid" class="dashboard-grid"></div>
<div id="moreSection" class="more-section" style="display:none;">
  <div class="more-header" onclick="Dashboard.toggleMore()">
    <span>More panels (<span id="moreCount">0</span>)</span>
    <span id="moreToggle">+</span>
  </div>
  <div id="moreGrid" class="more-grid"></div>
</div>
<div id="tooltip" class="tooltip"></div>
<script>
// ============================================================
// DASHBOARD — Adaptive metric layout engine
// ============================================================
// Module pattern: all state in Dashboard object, each function
// named and self-contained. Compose at bottom via manifest map.
// ============================================================
const Dashboard = (function() {
  // ----- state -----
  const STORAGE_KEY = 'adaptive_dashboard_v1';
  let panels = [];
  let tracking = { views: 0, startTime: Date.now() };
  let moreOpen = false;
  let dragState = null;
  let tooltipTimer = null;
  let observers = [];
  // ---- default panel definitions ----
  const DEFAULT_PANELS = [
    { id: 'cpu',        title: 'CPU Usage',       value: '42%',     change: '+3%', changeDir: 'up',   color: '#3fb950' },
    { id: 'memory',     title: 'Memory',          value: '6.2 GB',  change: '-1.2 GB', changeDir: 'down', color: '#58a6ff' },
    { id: 'network',    title: 'Network I/O',     value: '1.4 Gbps',change: '+12%', changeDir: 'up',   color: '#d29922' },
    { id: 'disk',       title: 'Disk Usage',      value: '234 GB',  change: '+8%', changeDir: 'up',   color: '#db6d28' },
    { id: 'users',      title: 'Active Users',    value: '1,247',   change: '+5%', changeDir: 'up',   color: '#3fb950' },
    { id: 'response',   title: 'Response Time',   value: '87 ms',   change: '-12 ms', changeDir: 'down', color: '#58a6ff' },
    { id: 'errors',     title: 'Error Rate',      value: '0.3%',    change: '-0.1%', changeDir: 'down', color: '#f85149' },
    { id: 'throughput', title: 'Throughput',      value: '8.4k/s',  change: '+2.1k/s', changeDir: 'up',  color: '#3fb950' },
  ];
  // ----- helper: generate mini sparkline bars -----
  function generateSparkData(count) {
    const data = [];
    for (let i = 0; i < count; i++) {
      data.push(Math.floor(Math.random() * 40) + 10);
    }
    return data;
  }
  // ----- helper: recency weight -----
  function recencyWeight(lastInteraction) {
    if (!lastInteraction) return 0.1;
    const daysSince = (Date.now() - lastInteraction) / (1000 * 60 * 60 * 24);
    return Math.exp(-daysSince / 7);
  }
  // ----- helper: compute composite score -----
  function computeScore(panel) {
    if (!panel.usage) return 0.01;
    const freq = panel.usage.frequency || 0;
    const dur = panel.usage.totalDuration || 0;
    const rec = recencyWeight(panel.usage.lastInteraction);
    const interactions = panel.usage.interactions || 0;
    const score = (freq * 5 + dur * 0.01 + interactions * 10) * rec;
    return Math.max(0.01, score);
  }
  // ============================================================
  // INIT — Load saved state or create defaults
  // ============================================================
  function init() {
    const saved = loadState();
    if (saved && saved.panels && saved.panels.length > 0) {
      panels = saved.panels;
      tracking = saved.tracking || { views: 0, startTime: Date.now() };
    } else {
      panels = DEFAULT_PANELS.map((def, i) => ({
        ...def,
        sparkData: generateSparkData(20),
        usage: { frequency: 0, totalDuration: 0, lastInteraction: Date.now(), interactions: 0, viewCount: 0 },
        locked: false,
        manualPosition: null,
        mode: 'full',
        collapseCount: 0,
        expandCount: 0
      }));
    }
    render();
    setupTracking();
    updateStats();
  }
  // ============================================================
  // SAVE/LOAD — localStorage persistence
  // ============================================================
  function saveState() {
    try {
      const state = { panels: panels.map(p => ({
        id: p.id, title: p.title, value: p.value, change: p.change, changeDir: p.changeDir,
        color: p.color, sparkData: p.sparkData, usage: p.usage, locked: p.locked,
        manualPosition: p.manualPosition, mode: p.mode, collapseCount: p.collapseCount,
        expandCount: p.expandCount
      })), tracking: tracking, version: 1 };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch(e) { /* quota exceeded or private mode */ }
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch(e) { return null; }
  }
  // ============================================================
  // TRACKING — IntersectionObserver + event listeners
  // ============================================================
  function setupTracking() {
    cleanupObservers();
    const grid = document.getElementById('dashboardGrid');
    if (!grid) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const panelEl = entry.target;
        const id = panelEl.dataset.panelId;
        const panel = panels.find(p => p.id === id);
        if (!panel) return;
        if (entry.isIntersecting) {
          panel.usage.viewCount = (panel.usage.viewCount || 0) + 1;
          panel.usage.lastInteraction = Date.now();
          panel.usage.frequency += 0.1;
          tracking.views++;
          panelEl.dataset.viewStart = Date.now();
        } else {
          const start = parseInt(panelEl.dataset.viewStart);
          if (start) {
            panel.usage.totalDuration += Date.now() - start;
            delete panelEl.dataset.viewStart;
          }
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
    observers.push(observer);
    // Also observe more grid panels
    const moreObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const panelEl = entry.target;
          const id = panelEl.dataset.panelId;
          const panel = panels.find(p => p.id === id);
          if (panel) { panel.usage.frequency += 0.05; panel.usage.lastInteraction = Date.now(); }
        }
      });
    }, { threshold: 0.3 });
    const moreGrid = document.getElementById('moreGrid');
    if (moreGrid) document.querySelectorAll('#moreGrid .panel').forEach(el => moreObserver.observe(el));
    observers.push(moreObserver);
    // Periodic save
    setInterval(saveState, 5000);
  }
  function cleanupObservers() {
    observers.forEach(obs => obs.disconnect());
    observers = [];
  }
  // ============================================================
  // RANK — score and sort panels, assign modes
  // ============================================================
  function rankAndAssign() {
    const scored = panels.map(p => ({ ...p, score: computeScore(p) }));
    scored.sort((a, b) => b.score - a.score);
    // Assign rank index
    scored.forEach((p, i) => { p.rank = i + 1; });
    // Assign display mode based on rank
    const total = scored.length;
    scored.forEach((p, i) => {
      if (p.locked) { /* keep current mode unless compacted */ return; }
      if (total <= 4) { p.mode = 'full'; return; }
      if (i === 0) p.mode = 'full';
      else if (i <= 1) p.mode = 'full';
      else if (i <= 3) p.mode = 'full';
      else if (i <= 5) p.mode = 'full';
      else p.mode = 'preview';
    });
    return scored;
  }
  // ============================================================
  // RENDER — build DOM from scored panels
  // ============================================================
  function render() {
    const scored = rankAndAssign();
    const grid = document.getElementById('dashboardGrid');
    if (!grid) return;
    grid.innerHTML = '';
    const visible = scored.filter(p => p.rank <= 5 || (p.locked && p.mode !== 'miniature'));
    const morePanels = scored.filter(p => p.rank > 5 && !p.locked);
    // Render visible panels
    visible.forEach((p, i) => {
      const el = createPanelElement(p, i);
      el.dataset.rank = Math.min(p.rank, 5);
      grid.appendChild(el);
    });
    // Render more section
    const moreSection = document.getElementById('moreSection');
    const moreGrid = document.getElementById('moreGrid');
    const moreCount = document.getElementById('moreCount');
    if (morePanels.length > 0) {
      moreSection.style.display = 'block';
      moreCount.textContent = morePanels.length;
      moreGrid.innerHTML = '';
      morePanels.forEach((p, i) => {
        const el = createPanelElement(p, i, true);
        moreGrid.appendChild(el);
      });
      if (moreOpen) moreGrid.classList.add('open');
    } else {
      moreSection.style.display = 'none';
    }
    // Update stats
    updateStats();
    saveState();
    setupTracking();
  }
  // ============================================================
  // CREATE PANEL ELEMENT — build DOM node for a panel
  // ============================================================
  function createPanelElement(panel, index, isMore) {
    const div = document.createElement('div');
    div.className = 'panel';
    div.dataset.panelId = panel.id;
    div.dataset.rank = panel.rank || (index + 1);
    if (panel.locked) div.classList.add('locked');
    if (panel.mode === 'compact' || panel.mode === 'preview' || panel.mode === 'miniature') {
      div.dataset.mode = panel.mode;
      if (panel.mode === 'compact') div.classList.add('compact');
      if (panel.mode === 'preview') div.classList.add('preview');
      if (panel.mode === 'miniature') div.classList.add('miniature');
    }
    // Header
    const header = document.createElement('div');
    header.className = 'panel-header';
    header.draggable = false;
    header.innerHTML = `
      <div class="panel-title">
        <span class="indicator" style="background:${panel.color}"></span>
        ${panel.title}
        <span class="rank-badge">#${panel.rank || '?'}</span>
      </div>
      <div class="panel-controls">
        <button class="${panel.locked ? 'lock-active' : ''}" onclick="Dashboard.toggleLock('${panel.id}')" title="Lock position">${panel.locked ? '🔒' : '🔓'}</button>
        <button onclick="Dashboard.toggleCompact('${panel.id}')" title="Toggle compact">${panel.mode === 'compact' ? '📂' : '📁'}</button>
        <button onclick="Dashboard.removePanel('${panel.id}')" title="Remove panel">✕</button>
      </div>
    `;
    // Drag handlers
    header.addEventListener('mousedown', (e) => startDrag(e, panel.id));
    header.addEventListener('touchstart', (e) => startDragTouch(e, panel.id), { passive: true });
    // Body
    const body = document.createElement('div');
    body.className = 'panel-body';
    body.innerHTML = `
      <div class="metric-label">${panel.title}</div>
      <div class="metric-value">${panel.value}</div>
      <div class="metric-change ${panel.changeDir}">${panel.change}</div>
      <div class="chart-area">
        <div class="chart-bar">${panel.sparkData.map(v => `<div style="height:${v}%"></div>`).join('')}</div>
      </div>
    `;
    // Footer
    const footer = document.createElement('div');
    footer.className = 'panel-footer';
    const u = panel.usage || {};
    footer.innerHTML = `
      <div class="track-stats">
        <span>${Math.round(u.frequency || 0)} views</span>
        <span>${Math.round((u.totalDuration || 0) / 1000)}s viewed</span>
        <span>score: ${(panel.score || computeScore(panel)).toFixed(1)}</span>
      </div>
    `;
    div.appendChild(header);
    div.appendChild(body);
    div.appendChild(footer);
    return div;
  }
  // ============================================================
  // DRAG & DROP — manual reordering via drag
  // ============================================================
  function startDrag(e, panelId) {
    if (e.button !== 0) return;
    e.preventDefault();
    const panel = panels.find(p => p.id === panelId);
    if (!panel) return;
    dragState = { panelId, startX: e.clientX, startY: e.clientY, moved: false };
    const el = e.currentTarget.closest('.panel');
    el.classList.add('dragging-source');
    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('mouseup', onDragEnd);
  }
  function startDragTouch(e, panelId) {
    const touch = e.touches[0];
    dragState = { panelId, startX: touch.clientX, startY: touch.clientY, moved: false };
    const el = e.currentTarget.closest('.panel');
    el.classList.add('dragging-source');
    document.addEventListener('touchmove', onDragTouchMove, { passive: true });
    document.addEventListener('touchend', onDragTouchEnd);
  }
  function onDragMove(e) {
    if (!dragState) return;
    const dx = e.clientX - dragState.startX;
    const dy = e.clientY - dragState.startY;
    if (Math.abs(dx) > 10 || Math.abs(dy) > 10) dragState.moved = true;
    if (dragState.moved) {
      e.target.closest('.panel')?.classList.add('dragging');
      highlightDropTarget(e.clientX, e.clientY);
    }
  }
  function onDragTouchMove(e) {
    if (!dragState) return;
    const touch = e.touches[0];
    const dx = touch.clientX - dragState.startX;
    const dy = touch.clientY - dragState.startY;
    if (Math.abs(dx) > 10 || Math.abs(dy) > 10) dragState.moved = true;
  }
  function highlightDropTarget(x, y) {
    document.querySelectorAll('.panel.drag-over').forEach(el => el.classList.remove('drag-over'));
    const target = document.elementFromPoint(x, y);
    if (target) {
      const panel = target.closest('.panel');
      if (panel && panel.dataset.panelId !== dragState.panelId) {
        panel.classList.add('drag-over');
        dragState.targetId = panel.dataset.panelId;
      }
    }
  }
  function onDragEnd(e) {
    document.removeEventListener('mousemove', onDragMove);
    document.removeEventListener('mouseup', onDragEnd);
    if (dragState && dragState.moved && dragState.targetId) {
      swapPositions(dragState.panelId, dragState.targetId);
    }
    document.querySelectorAll('.panel.dragging-source, .panel.dragging, .panel.drag-over').forEach(el => {
      el.classList.remove('dragging-source', 'dragging', 'drag-over');
    });
    dragState = null;
  }
  function onDragTouchEnd(e) {
    document.removeEventListener('touchmove', onDragTouchMove);
    document.removeEventListener('touchend', onDragTouchEnd);
    if (dragState && dragState.moved) {
      const touch = e.changedTouches[0];
      const target = document.elementFromPoint(touch.clientX, touch.clientY);
      if (target) {
        const panel = target.closest('.panel');
        if (panel && panel.dataset.panelId !== dragState.panelId) {
          swapPositions(dragState.panelId, panel.dataset.panelId);
        }
      }
    }
    document.querySelectorAll('.panel.dragging-source, .panel.dragging, .panel.drag-over').forEach(el => {
      el.classList.remove('dragging-source', 'dragging', 'drag-over');
    });
    dragState = null;
  }
  function swapPositions(idA, idB) {
    const a = panels.find(p => p.id === idA);
    const b = panels.find(p => p.id === idB);
    if (!a || !b) return;
    // Swap usage scores to swap position
    const tempScore = a.usage.frequency;
    a.usage.frequency = b.usage.frequency;
    b.usage.frequency = tempScore;
    const tempDur = a.usage.totalDuration;
    a.usage.totalDuration = b.usage.totalDuration;
    b.usage.totalDuration = tempDur;
    render();
  }
  // ============================================================
  // LOCK — toggle manual lock on panel
  // ============================================================
  function toggleLock(id) {
    const panel = panels.find(p => p.id === id);
    if (panel) { panel.locked = !panel.locked; render(); }
  }
  // ============================================================
  // COMPACT — toggle compact mode
  // ============================================================
  function toggleCompact(id) {
    const panel = panels.find(p => p.id === id);
    if (!panel) return;
    if (panel.mode === 'compact') {
      panel.mode = 'full';
      panel.expandCount = (panel.expandCount || 0) + 1;
    } else {
      panel.mode = 'compact';
      panel.collapseCount = (panel.collapseCount || 0) + 1;
    }
    render();
  }
  // ============================================================
  // REMOVE — remove panel from dashboard
  // ============================================================
  function removePanel(id) {
    panels = panels.filter(p => p.id !== id);
    render();
  }
  // ============================================================
  // TOGGLE MORE — expand/collapse more section
  // ============================================================
  function toggleMore() {
    moreOpen = !moreOpen;
    const grid = document.getElementById('moreGrid');
    const toggle = document.getElementById('moreToggle');
    if (grid) grid.classList.toggle('open');
    if (toggle) toggle.textContent = moreOpen ? '−' : '+';
  }
  // ============================================================
  // UPDATE STATS — refresh stats bar
  // ============================================================
  function updateStats() {
    document.getElementById('panelCount').textContent = panels.length;
    document.getElementById('lockedCount').textContent = panels.filter(p => p.locked).length;
    document.getElementById('compactCount').textContent = panels.filter(p => p.mode === 'compact' || p.mode === 'preview').length;
    document.getElementById('totalViews').textContent = tracking.views;
    const scored = panels.map(p => ({ ...p, score: computeScore(p) }));
    scored.sort((a, b) => b.score - a.score);
    if (scored.length > 0) document.getElementById('topPanel').textContent = scored[0].title;
  }
  // ============================================================
  // RESET TRACKING — clear all usage data
  // ============================================================
  function resetTracking() {
    panels.forEach(p => {
      p.usage = { frequency: 0, totalDuration: 0, lastInteraction: null, interactions: 0, viewCount: 0 };
    });
    tracking = { views: 0, startTime: Date.now() };
    render();
  }
  // ============================================================
  // FORCE RECALCULATE — re-rank and re-render
  // ============================================================
  function forceRecalculate() {
    render();
  }
  // ============================================================
  // RESET LAYOUT — clear localStorage and reload defaults
  // ============================================================
  function resetLayout() {
    localStorage.removeItem(STORAGE_KEY);
    panels = DEFAULT_PANELS.map((def, i) => ({
      ...def,
      sparkData: generateSparkData(20),
      usage: { frequency: 0, totalDuration: 0, lastInteraction: Date.now(), interactions: 0, viewCount: 0 },
      locked: false,
      manualPosition: null,
      mode: 'full',
      collapseCount: 0,
      expandCount: 0
    }));
    tracking = { views: 0, startTime: Date.now() };
    render();
  }
  // ============================================================
  // COUNTERINTUITIVE VALUES TEST — verify scoring logic
  // ============================================================
  function testScoringEdgeCases() {
    const cases = [
      { label: 'all recent', panels: [
        { usage: { frequency: 10, totalDuration: 5000, lastInteraction: Date.now(), interactions: 5 } },
        { usage: { frequency: 8, totalDuration: 3000, lastInteraction: Date.now(), interactions: 3 } }
      ]},
      { label: 'all old', panels: [
        { usage: { frequency: 10, totalDuration: 5000, lastInteraction: Date.now() - 30*86400000, interactions: 5 } },
        { usage: { frequency: 8, totalDuration: 3000, lastInteraction: Date.now() - 30*86400000, interactions: 3 } }
      ]},
      { label: 'mixed', panels: [
        { usage: { frequency: 10, totalDuration: 5000, lastInteraction: Date.now(), interactions: 5 } },
        { usage: { frequency: 8, totalDuration: 5000, lastInteraction: Date.now() - 30*86400000, interactions: 5 } }
      ]}
    ];
    const results = cases.map(c => ({
      label: c.label,
      scores: c.panels.map(p => {
        const freq = p.usage.frequency || 0;
        const dur = p.usage.totalDuration || 0;
        const rec = recencyWeight(p.usage.lastInteraction);
        const interactions = p.usage.interactions || 0;
        return (freq * 5 + dur * 0.01 + interactions * 10) * rec;
      })
    }));
    console.log('Scoring edge-case test results:', results);
    return results;
  }
  // ============================================================
  // PUBLIC API — manifest map
  // ============================================================
  return {
    init: init,
    toggleLock: toggleLock,
    toggleCompact: toggleCompact,
    removePanel: removePanel,
    toggleMore: toggleMore,
    resetTracking: resetTracking,
    forceRecalculate: forceRecalculate,
    resetLayout: resetLayout,
    testScoring: testScoringEdgeCases,
    getPanels: function() { return panels; },
    getTracking: function() { return tracking; }
  };
})();
// ============================================================
// BOOT
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
  Dashboard.init();
  console.log('Adaptive Dashboard initialized');
  console.log('Edge-case scoring test:', Dashboard.testScoring());
});
</script>
</body>
</html>
<!-- ARTIFACT_END -->