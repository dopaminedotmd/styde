```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif; background: #0f1117; color: #e1e4e8; min-height: 100vh; }
.header { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: #161b22; border-bottom: 1px solid #30363d; }
.header h1 { font-size: 18px; font-weight: 600; color: #58a6ff; }
.header-controls { display: flex; gap: 12px; align-items: center; }
.btn { padding: 6px 14px; border: 1px solid #30363d; border-radius: 6px; background: #21262d; color: #c9d1d9; cursor: pointer; font-size: 13px; transition: all 0.15s; }
.btn:hover { background: #30363d; border-color: #8b949e; }
.btn.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
.btn.reset { background: #da3633; border-color: #da3633; color: #fff; }
.stats-bar { display: flex; gap: 16px; font-size: 12px; color: #8b949e; padding: 0 24px; }
.stats-bar span { background: #21262d; padding: 4px 10px; border-radius: 4px; }
.dashboard { display: grid; gap: 12px; padding: 16px 24px; grid-template-columns: repeat(3, 1fr); grid-auto-rows: minmax(200px, auto); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; display: flex; flex-direction: column; }
.panel.large { grid-column: span 2; grid-row: span 2; }
.panel.medium { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; min-height: 100px; max-height: 140px; }
.panel.mini { grid-column: span 1; grid-row: span 1; min-height: 60px; max-height: 80px; }
.panel.more-section { grid-column: span 3; background: #21262d; border: 1px dashed #30363d; min-height: 60px; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; flex-wrap: wrap; padding: 12px; }
.panel.more-section:hover { border-color: #58a6ff; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #1c2128; border-bottom: 1px solid #30363d; cursor: grab; user-select: none; }
.panel-header:active { cursor: grabbing; }
.panel-header h3 { font-size: 14px; font-weight: 600; color: #c9d1d9; }
.panel-controls { display: flex; gap: 4px; }
.panel-btn { background: none; border: none; color: #8b949e; cursor: pointer; padding: 2px 6px; border-radius: 4px; font-size: 12px; }
.panel-btn:hover { color: #c9d1d9; background: #30363d; }
.panel-btn.locked { color: #f0883e; }
.panel-body { flex: 1; padding: 14px; overflow: hidden; }
.panel.compact .panel-body { padding: 8px 14px; }
.panel.mini .panel-body { padding: 4px 14px; }
.metric { display: flex; flex-direction: column; }
.metric-value { font-size: 32px; font-weight: 700; color: #58a6ff; }
.metric-label { font-size: 12px; color: #8b949e; margin-top: 2px; }
.metric-change { font-size: 13px; margin-top: 4px; }
.metric-change.up { color: #3fb950; }
.metric-change.down { color: #f85149; }
.chart-area { width: 100%; height: 100%; min-height: 80px; }
.chart-bar { display: flex; align-items: flex-end; gap: 4px; height: 80px; padding-top: 10px; }
.chart-bar .bar { flex: 1; background: linear-gradient(180deg, #58a6ff, #1f6feb); border-radius: 3px 3px 0 0; min-width: 6px; transition: height 0.3s; }
.compact-preview { display: flex; gap: 16px; align-items: center; font-size: 13px; }
.compact-preview .mini-val { font-weight: 600; color: #58a6ff; }
.compact-preview .mini-label { color: #8b949e; font-size: 11px; }
.usage-indicator { position: absolute; top: 4px; right: 4px; width: 8px; height: 8px; border-radius: 50%; }
.usage-indicator.hot { background: #f85149; box-shadow: 0 0 6px #f85149; }
.usage-indicator.warm { background: #f0883e; }
.usage-indicator.cold { background: #3fb950; }
.locked-indicator { position: absolute; top: 4px; left: 4px; font-size: 10px; color: #f0883e; }
.drag-ghost { opacity: 0.5; border: 2px dashed #58a6ff; }
.toast { position: fixed; bottom: 20px; right: 20px; background: #238636; color: #fff; padding: 10px 18px; border-radius: 8px; font-size: 13px; z-index: 1000; opacity: 0; transform: translateY(20px); transition: all 0.3s; pointer-events: none; }
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-controls">
    <div class="stats-bar" id="statsBar"></div>
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btnLockAll" title="Lock/unlock all panels">Lock All</button>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
  const LS_KEY_TRACKING = 'adaptive_layout_tracking';
  const LS_KEY_OVERRIDES = 'adaptive_layout_overrides';
  const LS_KEY_LAYOUT = 'adaptive_layout_layout';
  const RECENCY_DECAY = 0.92;
  const RELAYOUT_INTERVAL = 30000;
  const VIEW_DURATION_SAMPLE = 5000;
  const DASHBOARD = document.getElementById('dashboard');
  const STATS_BAR = document.getElementById('statsBar');
  const TOAST = document.getElementById('toast');
  let tracking = {};
  let overrides = {};
  let panelOrder = [];
  let viewTimers = {};
  let lastRelayout = 0;
  let lockedAll = false;
  const PANEL_DEFS = [
    { id: 'revenue', title: 'Revenue', type: 'metric', data: { value: '$128,430', change: '+12.5%', dir: 'up' }, color: '#58a6ff' },
    { id: 'users', title: 'Active Users', type: 'metric', data: { value: '24,892', change: '+8.3%', dir: 'up' }, color: '#3fb950' },
    { id: 'conversion', title: 'Conversion Rate', type: 'metric', data: { value: '4.8%', change: '-0.3%', dir: 'down' }, color: '#f0883e' },
    { id: 'churn', title: 'Churn Rate', type: 'metric', data: { value: '1.2%', change: '-0.1%', dir: 'up' }, color: '#f85149' },
    { id: 'traffic', title: 'Traffic Sources', type: 'chart', data: { bars: [0.45, 0.72, 0.38, 0.91, 0.55, 0.63, 0.48] }, color: '#a371f7' },
    { id: 'latency', title: 'API Latency', type: 'chart', data: { bars: [0.12, 0.18, 0.09, 0.22, 0.15, 0.11, 0.14] }, color: '#79c0ff' },
    { id: 'errors', title: 'Error Rate', type: 'metric', data: { value: '0.04%', change: '-0.02%', dir: 'up' }, color: '#d2a8ff' },
    { id: 'storage', title: 'Storage Usage', type: 'metric', data: { value: '68%', change: '+3%', dir: 'down' }, color: '#ffa657' },
    { id: 'sessions', title: 'Sessions', type: 'chart', data: { bars: [0.88, 0.65, 0.92, 0.78, 0.55, 0.70, 0.83] }, color: '#7ee787' },
  ];
  function load() {
    try { tracking = JSON.parse(localStorage.getItem(LS_KEY_TRACKING)) || {}; } catch(e) { tracking = {}; }
    try { overrides = JSON.parse(localStorage.getItem(LS_KEY_OVERRIDES)) || {}; } catch(e) { overrides = {}; }
    try { panelOrder = JSON.parse(localStorage.getItem(LS_KEY_LAYOUT)) || PANEL_DEFS.map(p => p.id); } catch(e) { panelOrder = PANEL_DEFS.map(p => p.id); }
    PANEL_DEFS.forEach(p => {
      if (!tracking[p.id]) tracking[p.id] = { views: 0, totalDuration: 0, interactions: 0, lastSeen: 0, score: 0 };
      if (!overrides[p.id]) overrides[p.id] = { locked: false, position: -1, size: 'auto' };
    });
  }
  function save() {
    localStorage.setItem(LS_KEY_TRACKING, JSON.stringify(tracking));
    localStorage.setItem(LS_KEY_OVERRIDES, JSON.stringify(overrides));
    localStorage.setItem(LS_KEY_LAYOUT, JSON.stringify(panelOrder));
  }
  function toast(msg) {
    TOAST.textContent = msg;
    TOAST.classList.add('show');
    clearTimeout(TOAST._t);
    TOAST._t = setTimeout(() => TOAST.classList.remove('show'), 2000);
  }
  function computeScores() {
    const now = Date.now();
    PANEL_DEFS.forEach(p => {
      const t = tracking[p.id];
      const daysSinceLastSeen = (now - t.lastSeen) / 86400000;
      const recency = Math.pow(RECENCY_DECAY, daysSinceLastSeen);
      const freq = t.views || 0;
      const dur = t.totalDuration ? t.totalDuration / 60000 : 0;
      t.score = (freq * 0.4 + dur * 0.35 + recency * 0.25) * 100;
    });
  }
  function getPanelRank(id) {
    const sorted = PANEL_DEFS.slice().sort((a, b) => tracking[b.id].score - tracking[a.id].score);
    return sorted.findIndex(p => p.id === id);
  }
  function getPanelSize(id) {
    if (overrides[id] && overrides[id].size !== 'auto') return overrides[id].size;
    const rank = getPanelRank(id);
    const total = PANEL_DEFS.length;
    if (rank === 0) return 'large';
    if (rank <= Math.floor(total * 0.3)) return 'medium';
    if (rank <= Math.floor(total * 0.6)) return 'compact';
    return 'mini';
  }
  function recordView(id) {
    if (!tracking[id]) return;
    tracking[id].views = (tracking[id].views || 0) + 1;
    tracking[id].lastSeen = Date.now();
  }
  function recordInteraction(id) {
    if (!tracking[id]) return;
    tracking[id].interactions = (tracking[id].interactions || 0) + 1;
    tracking[id].lastSeen = Date.now();
  }
  function startViewTimer(id) {
    if (viewTimers[id]) return;
    recordView(id);
    viewTimers[id] = { start: Date.now(), interval: setInterval(() => {
      if (tracking[id]) tracking[id].totalDuration = (tracking[id].totalDuration || 0) + VIEW_DURATION_SAMPLE;
    }, VIEW_DURATION_SAMPLE) };
  }
  function stopViewTimer(id) {
    const t = viewTimers[id];
    if (!t) return;
    const elapsed = Date.now() - t.start;
    if (tracking[id]) tracking[id].totalDuration = (tracking[id].totalDuration || 0) + elapsed;
    clearInterval(t.interval);
    delete viewTimers[id];
  }
  function buildPanelHTML(p) {
    const size = getPanelSize(p.id);
    const locked = overrides[p.id] && overrides[p.id].locked;
    const score = tracking[p.id] ? tracking[p.id].score.toFixed(1) : '0';
    let heatClass = 'cold';
    if (score > 40) heatClass = 'warm';
    if (score > 70) heatClass = 'hot';
    let bodyHTML = '';
    if (size === 'compact' || size === 'mini') {
      bodyHTML = renderCompactBody(p, size);
    } else if (p.type === 'metric') {
      bodyHTML = renderMetricBody(p);
    } else if (p.type === 'chart') {
      bodyHTML = renderChartBody(p);
    }
    const lockIcon = locked ? '&#128274;' : '&#128275;';
    const lockClass = locked ? 'locked' : '';
    return `<div class="panel ${size}" data-panel-id="${p.id}" data-score="${score}">
      <span class="usage-indicator ${heatClass}" title="Score: ${score}"></span>
      ${locked ? '<span class="locked-indicator">&#128274;</span>' : ''}
      <div class="panel-header" data-panel-id="${p.id}">
        <h3>${p.title}</h3>
        <div class="panel-controls">
          <button class="panel-btn btn-expand" data-panel-id="${p.id}" title="Expand">&#9650;</button>
          <button class="panel-btn btn-compact" data-panel-id="${p.id}" title="Compact">&#9660;</button>
          <button class="panel-btn btn-lock ${lockClass}" data-panel-id="${p.id}" title="${locked ? 'Unlock' : 'Lock'}">${lockIcon}</button>
        </div>
      </div>
      <div class="panel-body">${bodyHTML}</div>
    </div>`;
  }
  function renderMetricBody(p) {
    return `<div class="metric">
      <span class="metric-value">${p.data.value}</span>
      <span class="metric-label">${p.title}</span>
      <span class="metric-change ${p.data.dir}">${p.data.change}</span>
    </div>`;
  }
  function renderChartBody(p) {
    const bars = p.data.bars.map(h => `<div class="bar" style="height:${Math.round(h*70)}px"></div>`).join('');
    return `<div class="chart-area"><div class="chart-bar">${bars}</div></div>`;
  }
  function renderCompactBody(p, size) {
    const val = p.type === 'metric' ? p.data.value : (size === 'mini' ? 'Chart' : 'Chart preview');
    return `<div class="compact-preview">
      <span class="mini-val">${val}</span>
      <span class="mini-label">${p.title} ${size === 'mini' ? '(click to expand)' : '(double-click to expand)'}</span>
    </div>`;
  }
  function renderMoreSection(hiddenIds) {
    if (hiddenIds.length === 0) return '';
    const labels = hiddenIds.map(id => {
      const p = PANEL_DEFS.find(d => d.id === id);
      return p ? p.title : id;
    }).join(', ');
    return `<div class="panel more-section" id="moreSection">
      <span style="color:#8b949e;">+${hiddenIds.length} more:</span>
      <span style="color:#c9d1d9;">${labels}</span>
      <span style="color:#58a6ff;font-size:12px;">(click to restore all)</span>
    </div>`;
  }
  function applyLayout() {
    computeScores();
    const sorted = PANEL_DEFS.slice().sort((a, b) => {
      const aOverride = overrides[a.id] && overrides[a.id].position >= 0;
      const bOverride = overrides[b.id] && overrides[b.id].position >= 0;
      if (aOverride && bOverride) return overrides[a.id].position - overrides[b.id].position;
      if (aOverride) return -1;
      if (bOverride) return 1;
      return tracking[b.id].score - tracking[a.id].score;
    });
    const visible = sorted.filter(p => {
      if (overrides[p.id] && overrides[p.id].position >= 0) return true;
      return getPanelSize(p.id) !== 'mini';
    });
    const hidden = sorted.filter(p => {
      if (overrides[p.id] && overrides[p.id].position >= 0) return false;
      return getPanelSize(p.id) === 'mini';
    });
    panelOrder = visible.map(p => p.id).concat(hidden.map(p => p.id));
    let html = visible.map(p => buildPanelHTML(p)).join('');
    html += renderMoreSection(hidden.map(p => p.id));
    DASHBOARD.innerHTML = html;
    bindPanelEvents();
    updateStats(visible.length, hidden.length);
    save();
  }
  function bindPanelEvents() {
    DASHBOARD.querySelectorAll('.panel-header').forEach(header => {
      header.addEventListener('mousedown', onDragStart);
      header.addEventListener('click', (e) => {
        if (e.target.closest('.panel-btn')) return;
        const id = header.dataset.panelId;
        recordInteraction(id);
        const panel = header.closest('.panel');
        if (panel.classList.contains('compact')) {
          expandPanel(id);
        }
      });
      header.addEventListener('dblclick', (e) => {
        if (e.target.closest('.panel-btn')) return;
        const id = header.dataset.panelId;
        const panel = header.closest('.panel');
        if (panel.classList.contains('mini')) {
          expandPanel(id);
        }
      });
    });
    DASHBOARD.querySelectorAll('.panel-body').forEach(body => {
      body.addEventListener('click', () => {
        const id = body.closest('.panel').dataset.panelId;
        if (id) recordInteraction(id);
      });
    });
    DASHBOARD.querySelectorAll('.btn-expand').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        expandPanel(btn.dataset.panelId);
      });
    });
    DASHBOARD.querySelectorAll('.btn-compact').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        compactPanel(btn.dataset.panelId);
      });
    });
    DASHBOARD.querySelectorAll('.btn-lock').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleLock(btn.dataset.panelId);
      });
    });
    const moreSection = DASHBOARD.querySelector('#moreSection');
    if (moreSection) {
      moreSection.addEventListener('click', () => restoreAllMini());
    }
  }
  function expandPanel(id) {
    if (!overrides[id]) overrides[id] = { locked: false, position: -1, size: 'auto' };
    overrides[id].size = 'medium';
    recordInteraction(id);
    applyLayout();
    toast('Panel expanded');
  }
  function compactPanel(id) {
    if (!overrides[id]) overrides[id] = { locked: false, position: -1, size: 'auto' };
    overrides[id].size = 'compact';
    recordInteraction(id);
    applyLayout();
    toast('Panel compacted');
  }
  function toggleLock(id) {
    if (!overrides[id]) overrides[id] = { locked: false, position: -1, size: 'auto' };
    overrides[id].locked = !overrides[id].locked;
    if (overrides[id].locked) {
      overrides[id].position = getPanelRank(id);
    } else {
      overrides[id].position = -1;
    }
    recordInteraction(id);
    applyLayout();
    toast(overrides[id].locked ? 'Panel locked' : 'Panel unlocked');
  }
  function restoreAllMini() {
    PANEL_DEFS.forEach(p => {
      if (getPanelSize(p.id) === 'mini' && (!overrides[p.id] || overrides[p.id].position < 0)) {
        if (!overrides[p.id]) overrides[p.id] = { locked: false, position: -1, size: 'auto' };
        overrides[p.id].size = 'compact';
      }
    });
    applyLayout();
    toast('All panels restored');
  }
  let dragState = null;
  function onDragStart(e) {
    if (e.target.closest('.panel-btn')) return;
    const header = e.currentTarget;
    const panel = header.closest('.panel');
    if (!panel) return;
    dragState = {
      panel: panel,
      startX: e.clientX,
      startY: e.clientY,
      origIdx: Array.from(DASHBOARD.children).indexOf(panel),
    };
    panel.classList.add('drag-ghost');
    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('mouseup', onDragEnd);
    e.preventDefault();
  }
  function onDragMove(e) {
    if (!dragState) return;
    const dx = e.clientX - dragState.startX;
    const dy = e.clientY - dragState.startY;
    dragState.panel.style.transform = `translate(${dx}px, ${dy}px)`;
    dragState.panel.style.zIndex = '100';
  }
  function onDragEnd(e) {
    if (!dragState) return;
    document.removeEventListener('mousemove', onDragMove);
    document.removeEventListener('mouseup', onDragEnd);
    dragState.panel.classList.remove('drag-ghost');
    dragState.panel.style.transform = '';
    dragState.panel.style.zIndex = '';
    const target = document.elementFromPoint(e.clientX, e.clientY);
    const targetPanel = target ? target.closest('.panel') : null;
    if (targetPanel && targetPanel !== dragState.panel && !targetPanel.classList.contains('more-section')) {
      const targetId = targetPanel.dataset.panelId;
      const draggedId = dragState.panel.dataset.panelId;
      const draggedIdx = panelOrder.indexOf(draggedId);
      const targetIdx = panelOrder.indexOf(targetId);
      if (draggedIdx >= 0 && targetIdx >= 0) {
        panelOrder.splice(draggedIdx, 1);
        panelOrder.splice(targetIdx, 0, draggedId);
        if (!overrides[draggedId]) overrides[draggedId] = { locked: false, position: -1, size: 'auto' };
        overrides[draggedId].position = targetIdx;
        overrides[draggedId].locked = true;
        recordInteraction(draggedId);
        applyLayout();
        toast('Panel moved and locked');
      }
    }
    dragState = null;
  }
  function setupViewTracking() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.dataset.panelId || entry.target.closest('.panel')?.dataset.panelId;
        if (!id) return;
        if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
          startViewTimer(id);
        } else {
          stopViewTimer(id);
        }
      });
    }, { threshold: [0, 0.5] });
    const mutationObserver = new MutationObserver(() => {
      DASHBOARD.querySelectorAll('.panel:not(.more-section)').forEach(panel => {
        if (!panel.dataset.observed) {
          observer.observe(panel);
          panel.dataset.observed = '1';
        }
      });
    });
    mutationObserver.observe(DASHBOARD, { childList: true, subtree: true });
    DASHBOARD.querySelectorAll('.panel:not(.more-section)').forEach(panel => {
      observer.observe(panel);
      panel.dataset.observed = '1';
    });
  }
  function updateStats(visibleCount, hiddenCount) {
    const totalViews = Object.values(tracking).reduce((sum, t) => sum + (t.views || 0), 0);
    const totalInteractions = Object.values(tracking).reduce((sum, t) => sum + (t.interactions || 0), 0);
    STATS_BAR.innerHTML = `<span>Panels: ${visibleCount} visible / ${hiddenCount} hidden</span><span>Views: ${totalViews}</span><span>Interactions: ${totalInteractions}</span>`;
  }
  function resetAll() {
    tracking = {};
    overrides = {};
    panelOrder = PANEL_DEFS.map(p => p.id);
    PANEL_DEFS.forEach(p => {
      tracking[p.id] = { views: 0, totalDuration: 0, interactions: 0, lastSeen: 0, score: 0 };
      overrides[p.id] = { locked: false, position: -1, size: 'auto' };
    });
    save();
    applyLayout();
    toast('All tracking data reset');
  }
  function toggleLockAll() {
    lockedAll = !lockedAll;
    PANEL_DEFS.forEach((p, i) => {
      if (!overrides[p.id]) overrides[p.id] = { locked: false, position: -1, size: 'auto' };
      overrides[p.id].locked = lockedAll;
      overrides[p.id].position = lockedAll ? i : -1;
    });
    document.getElementById('btnLockAll').classList.toggle('active', lockedAll);
    document.getElementById('btnLockAll').textContent = lockedAll ? 'Unlock All' : 'Lock All';
    applyLayout();
    toast(lockedAll ? 'All panels locked' : 'All panels unlocked');
  }
  load();
  applyLayout();
  setupViewTracking();
  setInterval(() => {
    const now = Date.now();
    if (now - lastRelayout > RELAYOUT_INTERVAL && !lockedAll) {
      const anyUnlocked = PANEL_DEFS.some(p => !overrides[p.id] || !overrides[p.id].locked);
      if (anyUnlocked) {
        applyLayout();
      }
      lastRelayout = now;
    }
    save();
  }, RELAYOUT_INTERVAL);
  document.getElementById('btnReset').addEventListener('click', resetAll);
  document.getElementById('btnLockAll').addEventListener('click', toggleLockAll);
  window.addEventListener('beforeunload', () => {
    Object.keys(viewTimers).forEach(id => stopViewTimer(id));
    save();
  });
  console.log('Adaptive Metric Layout initialized. ' + PANEL_DEFS.length + ' panels, auto-relayout every ' + (RELAYOUT_INTERVAL/1000) + 's.');
})();
</script>
</body>
</html>
```