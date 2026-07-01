<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #222636;
  --border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.25);
  --danger: #ff5c72;
  --warning: #ffb347;
  --success: #4cd964;
  --rank-1-size: 2fr;
  --rank-2-size: 1fr;
  --rank-3-size: 0.5fr;
  --touch-min: 48px;
  --transition-speed: 0.35s;
}
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
  -webkit-font-smoothing: antialiased;
}
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}
.dashboard-header h1 {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.header-actions {
  display: flex;
  gap: 8px;
}
.header-btn {
  min-height: var(--touch-min);
  min-width: var(--touch-min);
  padding: 8px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 0.8125rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background var(--transition-speed) ease, border-color var(--transition-speed) ease;
}
.header-btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.header-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.dashboard-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
  transition: grid-template-columns var(--transition-speed) ease, grid-template-rows var(--transition-speed) ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform var(--transition-speed) ease, opacity var(--transition-speed) ease, grid-column var(--transition-speed) ease, grid-row var(--transition-speed) ease, background var(--transition-speed) ease, border-color var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
  transform: scale(1);
  -moz-transform: scale(1);
  transform-origin: center center;
  will-change: transform, grid-column, grid-row;
  cursor: pointer;
}
.panel:hover {
  background: var(--surface-hover);
  border-color: var(--accent);
  box-shadow: 0 0 20px var(--accent-glow);
}
.panel:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.panel.rank-dominant {
  grid-column: span 2;
  grid-row: span 2;
}
.panel.rank-standard {
  grid-column: span 1;
  grid-row: span 1;
}
.panel.rank-compact {
  grid-column: span 1;
  grid-row: span 1;
  padding: 8px;
  gap: 4px;
  transform: scale(0.85);
  -moz-transform: scale(0.85);
  opacity: 0.7;
  grid-template-rows: auto;
}
.panel.rank-compact:hover {
  transform: scale(0.9);
  -moz-transform: scale(0.9);
  opacity: 1;
}
.panel.rank-miniature {
  grid-column: span 1;
  grid-row: span 1;
  padding: 6px 8px;
  gap: 2px;
  transform: scale(0.65);
  -moz-transform: scale(0.65);
  opacity: 0.5;
  grid-template-rows: auto;
}
.panel.rank-miniature:hover {
  transform: scale(0.72);
  -moz-transform: scale(0.72);
  opacity: 0.85;
}
.panel.locked {
  border-color: var(--warning);
  box-shadow: 0 0 0 1px var(--warning);
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}
.panel-title {
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-dim);
}
.panel-value {
  font-size: 1.75rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  line-height: 1;
}
.panel-subtitle {
  font-size: 0.75rem;
  color: var(--text-dim);
}
.panel-actions {
  display: flex;
  gap: 6px;
  align-items: center;
}
.lock-btn {
  min-height: var(--touch-min);
  min-width: var(--touch-min);
  padding: 6px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-dim);
  font-size: 0.875rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-speed) ease, border-color var(--transition-speed) ease, background var(--transition-speed) ease;
  aria-label: "Toggle panel lock";
}
.lock-btn:hover { color: var(--text); border-color: var(--accent); background: var(--surface-hover); }
.lock-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.lock-btn.locked { color: var(--warning); border-color: var(--warning); }
.lock-btn.locked aria-label: "Unlock panel";
.rank-badge {
  font-size: 0.625rem;
  padding: 2px 8px;
  border-radius: 10px;
  background: var(--border);
  color: var(--text-dim);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.sparkline {
  width: 100%;
  height: 32px;
  opacity: 0.6;
}
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: auto;
  }
  .panel.rank-dominant,
  .panel.rank-standard,
  .panel.rank-compact,
  .panel.rank-miniature {
    grid-column: span 1;
    grid-row: span 1;
    transform: scale(1);
    -moz-transform: scale(1);
    opacity: 1;
  }
  .panel.rank-compact { padding: 14px; gap: 8px; }
  .panel.rank-miniature { padding: 14px; gap: 8px; }
  body { padding: 8px; }
  .dashboard-header h1 { font-size: 1.1rem; }
}
@media (prefers-reduced-motion: reduce) {
  .panel,
  .dashboard-grid,
  .header-btn,
  .lock-btn {
    transition: none;
    animation: none;
  }
  .panel { will-change: auto; }
}
.panel[aria-expanded="false"] .panel-content { display: none; }
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border: 0;
}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1 id="dashboard-title">Adaptive Metric Layout</h1>
  <div class="header-actions">
    <button class="header-btn" id="btn-reset" aria-label="Reset all layout preferences and tracking data">Reset Layout</button>
    <button class="header-btn" id="btn-export" aria-label="Export tracking data as JSON">Export Data</button>
    <span class="rank-badge" aria-live="polite" id="cycle-indicator">Cycle 0</span>
  </div>
</div>
<div class="dashboard-grid" id="dashboard-grid" role="region" aria-label="Adaptive metric dashboard panels">
</div>
<span class="sr-only" aria-live="polite" id="sr-announce"></span>
<script>
(function() {
  'use strict';
  const elCache = new Map();
  function $(sel, root) {
    const key = root ? root.dataset.cacheKey + '|' + sel : sel;
    if (elCache.has(key)) return elCache.get(key);
    const el = root ? root.querySelector(sel) : document.querySelector(sel);
    if (el) {
      if (root) root.dataset.cacheKey = root.dataset.cacheKey || root.id || Math.random().toString(36);
      elCache.set(key, el);
    }
    return el;
  }
  const domObserver = new MutationObserver(function(mutations) {
    for (const m of mutations) {
      if (m.type === 'childList') {
        for (const node of m.removedNodes) {
          if (node.nodeType === 1) {
            elCache.forEach(function(v, k) {
              if (v === node || node.contains(v)) elCache.delete(k);
            });
          }
        }
      }
    }
  });
  domObserver.observe(document.body, { childList: true, subtree: true });
  const STORAGE_KEY = 'adaptive_dashboard_v2';
  const CYCLE_INTERVAL_MS = 4000;
  const HISTORY_LENGTH = 30;
  const DECAY_HALF_LIFE_MS = 300000;
  const MIN_DWELL_MS = 500;
  const PANEL_DEFS = [
    { id: 'cpu', title: 'CPU Usage', unit: '%', max: 100, icon: '⚙', initial: 42 },
    { id: 'memory', title: 'Memory', unit: 'GB', max: 32, icon: '🧠', initial: 18.4 },
    { id: 'network', title: 'Network I/O', unit: 'MB/s', max: 1000, icon: '🌐', initial: 127 },
    { id: 'disk', title: 'Disk IOPS', unit: 'K', max: 500, icon: '💾', initial: 84 },
    { id: 'errors', title: 'Error Rate', unit: '/min', max: 100, icon: '⚠', initial: 3 },
    { id: 'requests', title: 'Requests', unit: 'rps', max: 5000, icon: '📡', initial: 1240 },
    { id: 'users', title: 'Active Users', unit: '', max: 10000, icon: '👥', initial: 487 },
    { id: 'latency', title: 'P99 Latency', unit: 'ms', max: 500, icon: '⏱', initial: 42 },
  ];
  let state = {
    panels: {},
    cycleCount: 0,
    lastPersist: 0,
  };
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const saved = JSON.parse(raw);
        for (const [id, data] of Object.entries(saved.panels || {})) {
          if (state.panels[id]) {
            state.panels[id].interactions = data.interactions || [];
            state.panels[id].locked = data.locked || false;
            state.panels[id].overrideRank = data.overrideRank || null;
            state.panels[id].dwellStart = null;
          }
        }
        state.cycleCount = saved.cycleCount || 0;
      }
    } catch (e) { /* corrupt storage, use defaults */ }
  }
  function persistState() {
    const now = Date.now();
    if (now - state.lastPersist < 2000) return;
    state.lastPersist = now;
    const payload = { cycleCount: state.cycleCount, panels: {} };
    for (const [id, p] of Object.entries(state.panels)) {
      payload.panels[id] = {
        interactions: p.interactions.slice(-HISTORY_LENGTH),
        locked: p.locked,
        overrideRank: p.overrideRank,
      };
    }
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(payload)); } catch (e) {}
  }
  function initPanels() {
    for (const def of PANEL_DEFS) {
      state.panels[def.id] = {
        id: def.id,
        title: def.title,
        unit: def.unit,
        max: def.max,
        icon: def.icon,
        value: def.initial,
        history: Array(20).fill(def.initial),
        interactions: [],
        locked: false,
        overrideRank: null,
        dwellStart: null,
      };
    }
  }
  function logInteraction(panelId, type, meta) {
    const p = state.panels[panelId];
    if (!p) return;
    p.interactions.push({
      type: type,
      timestamp: Date.now(),
      meta: meta || {},
    });
    if (p.interactions.length > HISTORY_LENGTH * 2) {
      p.interactions = p.interactions.slice(-HISTORY_LENGTH);
    }
  }
  function startDwell(panelId) {
    const p = state.panels[panelId];
    if (!p || p.dwellStart) return;
    p.dwellStart = Date.now();
  }
  function endDwell(panelId) {
    const p = state.panels[panelId];
    if (!p || !p.dwellStart) return;
    const duration = Date.now() - p.dwellStart;
    p.dwellStart = null;
    if (duration >= MIN_DWELL_MS) {
      logInteraction(panelId, 'view', { duration });
    }
  }
  function computeAttentionScore(panelId) {
    const p = state.panels[panelId];
    if (!p) return 0;
    const now = Date.now();
    let score = 0;
    const views = p.interactions.filter(function(i) { return i.type === 'view'; });
    const clicks = p.interactions.filter(function(i) { return i.type === 'click' || i.type === 'expand' || i.type === 'collapse'; });
    const viewFreq = views.length;
    let viewDur = 0;
    for (const v of views) {
      const age = now - v.timestamp;
      const decay = Math.exp(-age * Math.LN2 / DECAY_HALF_LIFE_MS);
      viewDur += (v.meta.duration || 0) * decay;
    }
    let clickFreq = 0;
    for (const c of clicks) {
      const age = now - c.timestamp;
      clickFreq += Math.exp(-age * Math.LN2 / DECAY_HALF_LIFE_MS);
    }
    const recencyBonus = views.length > 0
      ? Math.exp(-(now - views[views.length - 1].timestamp) * Math.LN2 / DECAY_HALF_LIFE_MS)
      : 0;
    score = (viewFreq * 10) + (viewDur * 0.01) + (clickFreq * 20) + (recencyBonus * 50);
    return Math.round(score * 100) / 100;
  }
  function rankPanels() {
    const rankings = [];
    for (const [id, p] of Object.entries(state.panels)) {
      if (p.locked && p.overrideRank !== null) {
        rankings.push({ id, score: -p.overrideRank });
      } else {
        rankings.push({ id, score: computeAttentionScore(id) });
      }
    }
    rankings.sort(function(a, b) { return b.score - a.score; });
    const tiers = [];
    const total = rankings.length;
    for (let i = 0; i < total; i++) {
      let tier;
      if (i === 0) tier = 'dominant';
      else if (i <= Math.ceil(total * 0.35)) tier = 'standard';
      else if (i <= Math.ceil(total * 0.7)) tier = 'compact';
      else tier = 'miniature';
      tiers.push({ id: rankings[i].id, rank: i + 1, tier: tier, score: rankings[i].score });
    }
    return tiers;
  }
  function buildSparklineSVG(history, max, color) {
    if (history.length < 2) return '';
    const w = 120, h = 32, pad = 2;
    const xStep = (w - pad * 2) / (history.length - 1);
    const yScale = (h - pad * 2) / (max || 1);
    let points = '';
    for (let i = 0; i < history.length; i++) {
      const x = pad + i * xStep;
      const y = h - pad - Math.min(history[i], max || Infinity) * yScale;
      points += (i === 0 ? 'M' : 'L') + x.toFixed(1) + ',' + y.toFixed(1) + ' ';
    }
    const c = color || 'var(--accent)';
    return '<svg class="sparkline" viewBox="0 0 ' + w + ' ' + h + '" aria-hidden="true"><path d="' + points + '" fill="none" stroke="' + c + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function renderPanel(panelData, rankInfo) {
    const p = panelData;
    const def = PANEL_DEFS.find(function(d) { return d.id === p.id; });
    const icon = def ? def.icon : '';
    const spark = buildSparklineSVG(p.history, p.max, rankInfo.tier === 'dominant' ? 'var(--accent)' : 'var(--text-dim)');
    const tierClass = 'rank-' + rankInfo.tier;
    const lockClass = p.locked ? ' locked' : '';
    const lockIcon = p.locked ? '🔒' : '🔓';
    const lockLabel = p.locked ? 'Unlock panel ' + p.title : 'Lock panel ' + p.title;
    return '<div class="panel ' + tierClass + lockClass + '" id="panel-' + p.id + '" data-panel-id="' + p.id + '" role="region" aria-label="' + p.title + ' panel, rank ' + rankInfo.rank + ', ' + rankInfo.tier + '" tabindex="0" aria-expanded="true">'
      + '<div class="panel-header">'
      + '<span class="panel-title">' + icon + ' ' + p.title + '</span>'
      + '<div class="panel-actions">'
      + '<span class="rank-badge" aria-label="Rank ' + rankInfo.rank + '">#' + rankInfo.rank + ' ' + rankInfo.tier + '</span>'
      + '<button class="lock-btn' + lockClass + '" data-panel-id="' + p.id + '" data-action="toggle-lock" aria-label="' + lockLabel + '">' + lockIcon + '</button>'
      + '</div>'
      + '</div>'
      + '<div class="panel-content">'
      + '<div class="panel-value" aria-live="polite">' + formatValue(p.value, p.unit) + '</div>'
      + '<div class="panel-subtitle">Score: ' + rankInfo.score.toFixed(1) + '</div>'
      + spark
      + '</div>'
      + '</div>';
  }
  function formatValue(val, unit) {
    if (typeof val === 'number') {
      return (val % 1 === 0 ? val.toString() : val.toFixed(1)) + (unit ? ' ' + unit : '');
    }
    return val + (unit ? ' ' + unit : '');
  }
  function renderAll() {
    const rankings = rankPanels();
    const grid = $('#dashboard-grid');
    let html = '';
    for (const r of rankings) {
      html += renderPanel(state.panels[r.id], r);
    }
    grid.innerHTML = html;
    rebindEvents();
  }
  function rebindEvents() {
    const panels = document.querySelectorAll('.panel');
    for (const panelEl of panels) {
      const pid = panelEl.dataset.panelId;
      if (!pid) continue;
      panelEl.addEventListener('mouseenter', function() { startDwell(pid); });
      panelEl.addEventListener('mouseleave', function() { endDwell(pid); });
      panelEl.addEventListener('focus', function() { startDwell(pid); });
      panelEl.addEventListener('blur', function() { endDwell(pid); });
      panelEl.addEventListener('click', function(e) {
        if (e.target.closest('[data-action="toggle-lock"]')) return;
        logInteraction(pid, 'click', {});
      });
      const lockBtn = panelEl.querySelector('[data-action="toggle-lock"]');
      if (lockBtn) {
        lockBtn.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          toggleLock(pid);
        });
      }
    }
  }
  function toggleLock(panelId) {
    const p = state.panels[panelId];
    if (!p) return;
    p.locked = !p.locked;
    if (p.locked) {
      const rankings = rankPanels();
      const r = rankings.find(function(rr) { return rr.id === panelId; });
      p.overrideRank = r ? r.rank : 1;
      logInteraction(panelId, 'lock', { rank: p.overrideRank });
    } else {
      p.overrideRank = null;
      logInteraction(panelId, 'unlock', {});
    }
    renderAll();
    persistState();
  }
  function resetAll() {
    initPanels();
    renderAll();
    localStorage.removeItem(STORAGE_KEY);
    state.cycleCount = 0;
    $('#cycle-indicator').textContent = 'Cycle 0';
    announceSR('Layout and tracking data reset');
  }
  function exportData() {
    const payload = { exportedAt: new Date().toISOString(), state: state };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'adaptive-dashboard-data.json';
    a.click();
    URL.revokeObjectURL(url);
    announceSR('Data exported');
  }
  function announceSR(msg) {
    const el = $('#sr-announce');
    el.textContent = msg;
  }
  function updateMetrics() {
    for (const [id, p] of Object.entries(state.panels)) {
      const def = PANEL_DEFS.find(function(d) { return d.id === id; });
      const max = def ? def.max : 100;
      const delta = (Math.random() - 0.5) * max * 0.15;
      p.value = Math.max(0, Math.min(max, p.value + delta));
      if (typeof p.value === 'number' && p.value < 1) p.value = parseFloat(p.value.toFixed(2));
      else if (typeof p.value === 'number') p.value = Math.round(p.value);
      p.history.push(p.value);
      if (p.history.length > 30) p.history.shift();
      const panelEl = document.getElementById('panel-' + id);
      if (panelEl) {
        const valueEl = panelEl.querySelector('.panel-value');
        if (valueEl) valueEl.textContent = formatValue(p.value, p.unit);
        const sparkEl = panelEl.querySelector('.sparkline');
        if (sparkEl) {
          sparkEl.outerHTML = buildSparklineSVG(p.history, p.max, panelEl.classList.contains('rank-dominant') ? 'var(--accent)' : 'var(--text-dim)');
        }
      }
    }
  }
  function cycleTick() {
    state.cycleCount++;
    updateMetrics();
    if (state.cycleCount % 8 === 0) {
      const unlocked = Object.values(state.panels).filter(function(p) { return !p.locked; });
      for (const p of unlocked) {
        if (Math.random() < 0.3) {
          logInteraction(p.id, 'view', { duration: Math.floor(Math.random() * 8000) + 1000 });
        }
      }
      renderAll();
    }
    $('#cycle-indicator').textContent = 'Cycle ' + state.cycleCount;
    persistState();
  }
  function boot() {
    initPanels();
    loadState();
    renderAll();
    document.getElementById('btn-reset').addEventListener('click', resetAll);
    document.getElementById('btn-export').addEventListener('click', exportData);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        resetAll();
        announceSR('Layout reset via Escape key');
      }
    });
    const observer = new IntersectionObserver(function(entries) {
      for (const entry of entries) {
        const pid = entry.target.dataset.panelId;
        if (!pid) continue;
        if (entry.isIntersecting) {
          logInteraction(pid, 'expand', { visible: true });
        } else {
          logInteraction(pid, 'collapse', { visible: false });
        }
      }
    }, { threshold: 0.5 });
    for (const panelEl of document.querySelectorAll('.panel')) {
      observer.observe(panelEl);
    }
    setInterval(cycleTick, CYCLE_INTERVAL_MS);
    announceSR('Adaptive dashboard ready. Panels will reorder based on your usage.');
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
</script>
</body>
</html>