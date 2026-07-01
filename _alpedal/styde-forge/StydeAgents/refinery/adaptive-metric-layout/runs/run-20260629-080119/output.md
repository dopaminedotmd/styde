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
  --surface2: #21252e;
  --border: #2a2d37;
  --text: #c9d1d9;
  --text2: #8b949e;
  --accent: #58a6ff;
  --accent2: #3fb950;
  --warn: #d29922;
  --danger: #f85149;
  --radius: 8px;
  --gap: 10px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 12px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
header h1 { font-size: 16px; font-weight: 600; }
.toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
}
.toolbar button {
  padding: 5px 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--surface2);
  color: var(--text);
  cursor: pointer;
  font-size: 12px;
  transition: background 0.15s;
}
.toolbar button:hover { background: var(--border); }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #000; }
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 140px;
  gap: var(--gap);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: grid-column 0.35s ease, grid-row 0.35s ease, opacity 0.25s;
  overflow: hidden;
}
.panel.large {
  grid-column: span 2;
  grid-row: span 2;
}
.panel.medium {
  grid-column: span 1;
  grid-row: span 1;
}
.panel.compact {
  grid-column: span 1;
  grid-row: span 1;
  padding: 8px;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: block; }
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: '';
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  background: var(--warn);
  border-radius: 50%;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  flex-shrink: 0;
}
.panel-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.panel-actions {
  display: flex;
  gap: 4px;
}
.panel-actions button {
  width: 22px;
  height: 22px;
  border: 1px solid var(--border);
  border-radius: 3px;
  background: transparent;
  color: var(--text2);
  cursor: pointer;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.panel-actions button:hover { background: var(--surface2); color: var(--text); }
.panel-actions button.lock-btn.locked { background: var(--warn); border-color: var(--warn); color: #000; }
.panel-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  min-height: 0;
}
.panel-preview {
  display: none;
  flex: 1;
  min-height: 0;
}
.sparkline {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 100%;
  padding-top: 4px;
}
.sparkline-bar {
  flex: 1;
  background: var(--accent);
  border-radius: 1px;
  min-height: 2px;
  opacity: 0.7;
}
.metric-value {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.metric-value .number { font-size: 28px; font-weight: 700; }
.metric-value .unit { font-size: 12px; color: var(--text2); }
.metric-secondary {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 100%;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
}
.metric-row .label { color: var(--text2); }
.metric-row .value { font-weight: 600; }
.trend-up { color: var(--accent2); }
.trend-down { color: var(--danger); }
.rank-badge {
  position: absolute;
  bottom: 4px;
  right: 6px;
  font-size: 9px;
  color: var(--border);
  font-weight: 700;
}
.more-section {
  margin-top: var(--gap);
  padding: 10px 12px;
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  cursor: pointer;
}
.more-section-header {
  font-size: 12px;
  color: var(--text2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.more-panels {
  display: none;
  margin-top: 8px;
}
.more-section.expanded .more-panels { display: block; }
.more-panel {
  display: flex;
  justify-content: space-between;
  padding: 6px 8px;
  margin-bottom: 4px;
  background: var(--surface2);
  border-radius: 4px;
  font-size: 12px;
}
.position-input {
  width: 36px;
  padding: 2px 4px;
  border: 1px solid var(--border);
  border-radius: 3px;
  background: var(--surface2);
  color: var(--text);
  font-size: 11px;
  text-align: center;
}
.position-input:focus { outline: none; border-color: var(--accent); }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.panel { animation: fadeIn 0.3s ease; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Metrics</h1>
  <div class="toolbar">
    <span style="font-size:11px;color:var(--text2)">Auto-layout</span>
    <button id="btnAutoLayout" class="active" onclick="toggleAutoLayout()">ON</button>
    <button onclick="resetAll()">Reset</button>
    <button onclick="forceReRank()">Re-rank Now</button>
    <span style="font-size:10px;color:var(--text2);margin-left:8px" id="lastUpdate"></span>
  </div>
</header>
<div id="dashboard" class="grid"></div>
<div id="moreSection" class="more-section" style="display:none" onclick="toggleMore(event)">
  <div class="more-section-header">
    <span>More panels</span>
    <span style="font-size:10px;color:var(--text2)" id="moreCount"></span>
  </div>
  <div class="more-panels" id="morePanels"></div>
</div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_metrics_v2';
  const RANK_INTERVAL = 15000;
  const RECENCY_HALF_LIFE = 300000;
  const COMPACT_CUTOFF = 0.25;
  const MORE_CUTOFF = 0.10;
  const PANEL_DEFS = [
    { id: 'cpu',    title: 'CPU Usage',     icon: '⚙', value: () => Math.round(20 + Math.random() * 60) + '%', color: '#58a6ff' },
    { id: 'memory', title: 'Memory',         icon: '▦', value: () => (Math.round(40 + Math.random() * 45) / 10).toFixed(1) + ' GB', color: '#3fb950' },
    { id: 'network',title: 'Network I/O',    icon: '⬡', value: () => Math.round(50 + Math.random() * 400) + ' Mbps', color: '#d29922' },
    { id: 'storage',title: 'Storage',        icon: '◈', value: () => Math.round(60 + Math.random() * 30) + '%', color: '#f85149' },
    { id: 'users',  title: 'Active Users',   icon: '👤', value: () => Math.round(200 + Math.random() * 1800), color: '#a371f7' },
    { id: 'revenue',title: 'Revenue',        icon: '$', value: () => '$' + (Math.round(1000 + Math.random() * 9000)).toLocaleString(), color: '#3fb950' },
    { id: 'errors', title: 'Error Rate',     icon: '⚠', value: () => (Math.random() * 5).toFixed(2) + '%', color: '#f85149' },
    { id: 'latency',title: 'P95 Latency',    icon: '⏱', value: () => Math.round(20 + Math.random() * 180) + 'ms', color: '#58a6ff' },
    { id: 'throughput',title:'Throughput',   icon: '↗', value: () => Math.round(500 + Math.random() * 3500) + ' req/s', color: '#d29922' },
    { id: 'cache',  title: 'Cache Hit Rate', icon: '⊕', value: () => Math.round(70 + Math.random() * 28) + '%', color: '#3fb950' },
  ];
  let panels = [];
  let autoLayout = true;
  let observer = null;
  let observerCleanup = null;
  let rankTimer = null;
  let refreshTimer = null;
  let visibilityMap = new Map();
  let lastVisibleTime = new Map();
  let panelDomCache = new Map();
  function init() {
    const saved = loadState();
    panels = PANEL_DEFS.map((def, i) => {
      const savedPanel = saved?.panels?.find(p => p.id === def.id);
      return {
        id: def.id,
        title: def.title,
        icon: def.icon,
        valueFn: def.value,
        color: def.color,
        locked: savedPanel?.locked ?? false,
        viewCount: savedPanel?.viewCount ?? 0,
        totalViewMs: savedPanel?.totalViewMs ?? 0,
        interactionCount: savedPanel?.interactionCount ?? 0,
        lastInteraction: savedPanel?.lastInteraction ?? 0,
        compactOverride: savedPanel?.compactOverride ?? false,
        position: savedPanel?.position ?? i,
      };
    });
    autoLayout = saved?.autoLayout ?? true;
    document.getElementById('btnAutoLayout').classList.toggle('active', autoLayout);
    document.getElementById('btnAutoLayout').textContent = autoLayout ? 'ON' : 'OFF';
    buildDom();
    setupObserver();
    startTracking();
    applyLayout();
    updateAllValues();
    refreshTimer = setInterval(updateAllValues, 3000);
    rankTimer = setInterval(reRank, RANK_INTERVAL);
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }
  function saveState() {
    const data = {
      panels: panels.map(p => ({
        id: p.id,
        locked: p.locked,
        viewCount: p.viewCount,
        totalViewMs: p.totalViewMs,
        interactionCount: p.interactionCount,
        lastInteraction: p.lastInteraction,
        compactOverride: p.compactOverride,
        position: p.position,
      })),
      autoLayout,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }
  function computeScore(panel) {
    const now = Date.now();
    const hoursSinceLastInteraction = panel.lastInteraction
      ? Math.max(0, (now - panel.lastInteraction) / 3600000)
      : 24;
    const recencyFactor = Math.exp(-hoursSinceLastInteraction * Math.LN2 / (RECENCY_HALF_LIFE / 3600000));
    const viewScore = panel.totalViewMs / 1000;
    const freqScore = panel.viewCount;
    const interactScore = panel.interactionCount;
    return (freqScore * 0.35 + viewScore * 0.40 + interactScore * 0.25) * recencyFactor;
  }
  function rankPanels() {
    const maxScore = Math.max(1, ...panels.map(p => computeScore(p)));
    panels.forEach(p => {
      p.rank = computeScore(p);
      p.normRank = maxScore > 0 ? p.rank / maxScore : 0;
    });
    panels.sort((a, b) => {
      if (a.locked && b.locked) return a.position - b.position;
      if (a.locked) return -1;
      if (b.locked) return 1;
      return b.rank - a.rank;
    });
    panels.forEach((p, i) => { if (!p.locked) p.position = i; });
  }
  function panelSizeClass(p) {
    if (p.compactOverride) return 'compact';
    if (p.normRank >= 0.6) return 'large';
    if (p.normRank >= COMPACT_CUTOFF) return 'medium';
    if (p.normRank >= MORE_CUTOFF) return 'compact';
    return 'more';
  }
  function applyLayout() {
    if (!autoLayout) return;
    rankPanels();
    const visible = panels.filter(p => panelSizeClass(p) !== 'more');
    const hidden = panels.filter(p => panelSizeClass(p) === 'more');
    const grid = document.getElementById('dashboard');
    for (const p of visible) {
      const el = panelDomCache.get(p.id);
      if (!el) continue;
      const sizeClass = panelSizeClass(p);
      el.classList.remove('large', 'medium', 'compact');
      el.classList.add(sizeClass);
      el.querySelector('.rank-badge').textContent = '#' + (p.position + 1);
      el.querySelector('.compact-toggle').textContent = p.compactOverride ? '⤢' : '⤡';
      el.style.order = p.position;
    }
    for (const p of hidden) {
      const el = panelDomCache.get(p.id);
      if (!el) continue;
      el.style.display = 'none';
    }
    updateMoreSection(hidden);
    document.getElementById('lastUpdate').textContent =
      'Updated ' + new Date().toLocaleTimeString();
    saveState();
  }
  function updateMoreSection(hidden) {
    const section = document.getElementById('moreSection');
    const container = document.getElementById('morePanels');
    if (hidden.length === 0) {
      section.style.display = 'none';
      return;
    }
    section.style.display = 'block';
    document.getElementById('moreCount').textContent = hidden.length + ' panel' + (hidden.length > 1 ? 's' : '');
    container.innerHTML = '';
    for (const p of hidden) {
      const div = document.createElement('div');
      div.className = 'more-panel';
      div.innerHTML = '<span>' + p.icon + ' ' + p.title + '</span><span style="color:var(--text2);font-size:10px">rank #' + (p.position + 1) + '</span>';
      div.addEventListener('click', (e) => {
        e.stopPropagation();
        p.compactOverride = false;
        p.interactionCount++;
        p.lastInteraction = Date.now();
        applyLayout();
      });
      container.appendChild(div);
    }
  }
  function toggleMore(e) {
    e.stopPropagation();
    document.getElementById('moreSection').classList.toggle('expanded');
  }
  function buildDom() {
    const grid = document.getElementById('dashboard');
    grid.innerHTML = '';
    panelDomCache.clear();
    for (const p of panels) {
      const el = createPanelDom(p);
      grid.appendChild(el);
      panelDomCache.set(p.id, el);
    }
  }
  function createPanelDom(p) {
    const el = document.createElement('div');
    el.className = 'panel medium';
    el.dataset.panelId = p.id;
    el.style.order = p.position;
    el.innerHTML =
      '<div class="panel-header">' +
        '<span class="panel-title">' + p.icon + ' ' + p.title + '</span>' +
        '<div class="panel-actions">' +
          '<button class="compact-toggle" title="Toggle compact">⤡</button>' +
          '<button class="lock-btn' + (p.locked ? ' locked' : '') + '" title="Lock position">🔒</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body"><span class="number">--</span></div>' +
      '<div class="panel-preview">' +
        '<div class="sparkline">' + Array.from({length: 20}, () =>
          '<div class="sparkline-bar" style="height:' + (15 + Math.random() * 85) + '%"></div>'
        ).join('') + '</div>' +
      '</div>' +
      '<div class="rank-badge">#' + (p.position + 1) + '</div>';
    el.querySelector('.lock-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      p.locked = !p.locked;
      el.querySelector('.lock-btn').classList.toggle('locked', p.locked);
      el.classList.toggle('locked', p.locked);
      p.interactionCount++;
      p.lastInteraction = Date.now();
      saveState();
      applyLayout();
    });
    el.querySelector('.compact-toggle').addEventListener('click', (e) => {
      e.stopPropagation();
      p.compactOverride = !p.compactOverride;
      p.interactionCount++;
      p.lastInteraction = Date.now();
      applyLayout();
    });
    el.addEventListener('click', () => {
      p.interactionCount++;
      p.lastInteraction = Date.now();
    });
    el.querySelector('.panel-body').addEventListener('click', (e) => {
      e.stopPropagation();
      p.interactionCount += 2;
      p.lastInteraction = Date.now();
    });
    return el;
  }
  function cleanupObserver() {
    if (observer) {
      observer.disconnect();
      observer = null;
    }
    visibilityMap.clear();
    lastVisibleTime.clear();
  }
  function setupObserver() {
    cleanupObserver();
    observer = new IntersectionObserver((entries) => {
      const now = Date.now();
      for (const entry of entries) {
        const id = entry.target.dataset.panelId;
        if (!id) continue;
        const panel = panels.find(p => p.id === id);
        if (!panel) continue;
        if (entry.isIntersecting) {
          lastVisibleTime.set(id, now);
          visibilityMap.set(id, true);
        } else {
          visibilityMap.set(id, false);
          const start = lastVisibleTime.get(id);
          if (start) {
            panel.totalViewMs += now - start;
            panel.viewCount++;
            lastVisibleTime.delete(id);
          }
        }
      }
    }, { threshold: 0.3 });
    for (const el of document.querySelectorAll('.panel')) {
      observer.observe(el);
    }
  }
  function flushVisibility() {
    const now = Date.now();
    for (const [id, visible] of visibilityMap) {
      if (!visible) continue;
      const panel = panels.find(p => p.id === id);
      if (!panel) continue;
      const start = lastVisibleTime.get(id);
      if (start) {
        panel.totalViewMs += now - start;
        panel.viewCount++;
        lastVisibleTime.set(id, now);
      }
    }
  }
  function startTracking() {
    window.addEventListener('beforeunload', () => {
      flushVisibility();
      saveState();
    });
  }
  function reRank() {
    flushVisibility();
    applyLayout();
  }
  function forceReRank() {
    flushVisibility();
    rankPanels();
    applyLayout();
  }
  function updateAllValues() {
    for (const p of panels) {
      const el = panelDomCache.get(p.id);
      if (!el) continue;
      const bodyEl = el.querySelector('.panel-body');
      if (!bodyEl) continue;
      const val = p.valueFn();
      bodyEl.innerHTML = '<span class="number" style="color:' + p.color + '">' + val + '</span>';
      const sparkline = el.querySelector('.sparkline');
      if (sparkline) {
        const bars = sparkline.querySelectorAll('.sparkline-bar');
        bars.forEach(b => {
          b.style.height = (15 + Math.random() * 85) + '%';
        });
      }
    }
  }
  window.toggleAutoLayout = function() {
    autoLayout = !autoLayout;
    document.getElementById('btnAutoLayout').classList.toggle('active', autoLayout);
    document.getElementById('btnAutoLayout').textContent = autoLayout ? 'ON' : 'OFF';
    if (autoLayout) applyLayout();
    saveState();
  };
  window.resetAll = function() {
    panels = PANEL_DEFS.map((def, i) => ({
      id: def.id,
      title: def.title,
      icon: def.icon,
      valueFn: def.value,
      color: def.color,
      locked: false,
      viewCount: 0,
      totalViewMs: 0,
      interactionCount: 0,
      lastInteraction: 0,
      compactOverride: false,
      position: i,
    }));
    autoLayout = true;
    document.getElementById('btnAutoLayout').classList.add('active');
    document.getElementById('btnAutoLayout').textContent = 'ON';
    localStorage.removeItem(STORAGE_KEY);
    cleanupObserver();
    if (rankTimer) clearInterval(rankTimer);
    if (refreshTimer) clearInterval(refreshTimer);
    panelDomCache.clear();
    buildDom();
    setupObserver();
    applyLayout();
    updateAllValues();
    refreshTimer = setInterval(updateAllValues, 3000);
    rankTimer = setInterval(reRank, RANK_INTERVAL);
  };
  window.forceReRank = forceReRank;
  window.toggleMore = toggleMore;
  init();
})();
</script>
</body>
</html>