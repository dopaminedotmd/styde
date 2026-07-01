<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent-dim: #1f6feb33;
  --green: #3fb950;
  --orange: #d2991d;
  --red: #f85149;
  --compact-ratio: 0.35;
  --gap: 10px;
  --radius: 8px;
  --transition: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  overflow-x: hidden;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; background: var(--surface); border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
}
header h1 { font-size: 16px; font-weight: 600; letter-spacing: -0.3px; }
header .controls { display: flex; gap: 8px; align-items: center; }
.btn {
  padding: 6px 14px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--surface); color: var(--text); cursor: pointer;
  font-size: 12px; font-weight: 500; transition: background 150ms;
}
.btn:hover { background: var(--accent-dim); border-color: var(--accent); }
.btn.active { background: var(--accent-dim); border-color: var(--accent); color: var(--accent); }
.dashboard {
  display: grid; gap: var(--gap); padding: 16px;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(160px, auto);
  transition: all var(--transition);
}
@media (min-width: 1400px) { .dashboard { grid-template-columns: repeat(6, 1fr); } }
@media (max-width: 900px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .dashboard { grid-template-columns: 1fr; } }
.panel {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 14px; position: relative; overflow: hidden;
  transition: grid-column var(--transition), grid-row var(--transition), opacity var(--transition), transform var(--transition);
  display: flex; flex-direction: column; min-height: 140px;
}
.panel.rank-0 { grid-column: span 2; grid-row: span 2; }
.panel.rank-1 { grid-column: span 2; grid-row: span 1; }
.panel.rank-2 { grid-column: span 1; grid-row: span 1; }
.panel.rank-3 { grid-column: span 1; grid-row: span 1; }
.panel.compact {
  grid-column: span 1; grid-row: span 1;
  min-height: 70px; padding: 8px 12px;
  opacity: 0.7; transform: scale(0.97);
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-header { margin-bottom: 0; }
.panel.locked { border-color: var(--orange); box-shadow: 0 0 0 1px var(--orange); }
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px; gap: 8px;
}
.panel-title { font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-score {
  font-size: 10px; color: var(--text-dim); white-space: nowrap;
  background: var(--bg); padding: 2px 8px; border-radius: 10px;
}
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none; border: 1px solid transparent; color: var(--text-dim);
  cursor: pointer; font-size: 14px; padding: 2px 5px; border-radius: 4px;
  line-height: 1; transition: all 120ms;
}
.panel-actions button:hover { color: var(--text); border-color: var(--border); }
.panel-actions button.locked-btn { color: var(--orange); }
.panel-body { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.metric-value { font-size: 28px; font-weight: 700; line-height: 1; }
.metric-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }
.metric-change { font-size: 12px; }
.metric-change.up { color: var(--green); }
.metric-change.down { color: var(--red); }
.sparkline-canvas { width: 100%; height: 40px; border-radius: 4px; }
.bar-container { display: flex; align-items: end; gap: 3px; height: 50px; }
.bar {
  flex: 1; border-radius: 3px 3px 0 0; background: var(--accent);
  transition: height 300ms; min-width: 4px;
}
.progress-ring { position: relative; width: 64px; height: 64px; }
.progress-ring canvas { width: 64px; height: 64px; }
.compact-preview {
  display: flex; align-items: center; gap: 10px;
  font-size: 12px; color: var(--text-dim);
}
.compact-preview .mini-val { font-size: 18px; font-weight: 600; color: var(--text); }
.more-section {
  margin-top: 12px; padding: 12px 16px; border-top: 1px solid var(--border);
  display: none;
}
.more-section.visible { display: block; }
.more-section h3 {
  font-size: 12px; color: var(--text-dim); text-transform: uppercase;
  letter-spacing: 0.8px; margin-bottom: 8px; cursor: pointer;
}
.more-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--gap); }
.focus-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 200;
  display: none; align-items: center; justify-content: center;
}
.focus-overlay.active { display: flex; }
.focus-panel {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 24px; max-width: 700px; width: 90%; max-height: 80vh; overflow-y: auto;
  position: relative;
}
.focus-close {
  position: absolute; top: 10px; right: 14px;
  background: none; border: none; color: var(--text-dim); font-size: 22px; cursor: pointer;
}
.focus-close:hover { color: var(--text); }
.toast {
  position: fixed; bottom: 20px; right: 20px; z-index: 300;
  background: var(--surface); border: 1px solid var(--border); border-radius: 6px;
  padding: 8px 16px; font-size: 12px; opacity: 0; transform: translateY(10px);
  transition: all 200ms; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.panel.dragging { opacity: 0.5; z-index: 50; cursor: grabbing; }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-dim); }
.resize-handle {
  position: absolute; bottom: 0; right: 0; width: 16px; height: 16px;
  cursor: nwse-resize; background: linear-gradient(135deg, transparent 50%, var(--border) 50%);
  border-radius: 0 0 var(--radius) 0; opacity: 0; transition: opacity 150ms;
}
.panel:hover .resize-handle { opacity: 1; }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset layout to default">Reset</button>
    <button class="btn" id="btnExport" title="Export layout config">Export</button>
    <span style="font-size:11px;color:var(--text-dim);margin-left:8px" id="trackStatus">tracking active</span>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection">
  <h3 id="moreToggle">&#9654; More panels (<span id="moreCount">0</span>)</h3>
  <div class="more-grid" id="moreGrid"></div>
</div>
<div class="focus-overlay" id="focusOverlay">
  <div class="focus-panel" id="focusPanel"></div>
</div>
<div class="toast" id="toast"></div>
<script>
(function() {
  'use strict';
  const LS_KEY = 'adaptive_dashboard_v2';
  const DEBOUNCE_MS = 50;
  const THROTTLE_MS = 50;
  const INACTIVITY_COMPACT_MS = 300000;
  const SCORE_DECAY = 0.985;
  const COMPACT_THRESHOLD = 0.18;
  const RESIZE_DEBOUNCE = 100;
  const RANK_COUNT = 4;
  const INITIAL_PANELS = [
    { id: 'revenue', title: 'Revenue', type: 'metric', value: '$128,430', change: '+12.3%', dir: 'up', label: 'Monthly Revenue' },
    { id: 'users', title: 'Active Users', type: 'metric', value: '24,891', change: '+8.7%', dir: 'up', label: 'DAU' },
    { id: 'conversion', title: 'Conversion', type: 'progress', value: 6.8, max: 10, label: 'Conversion Rate' },
    { id: 'latency', title: 'API Latency', type: 'metric', value: '142ms', change: '-5.1%', dir: 'down', label: 'p95' },
    { id: 'errors', title: 'Error Rate', type: 'metric', value: '0.12%', change: '+0.03%', dir: 'down', label: '5xx Errors' },
    { id: 'sessions', title: 'Sessions', type: 'sparkline', data: genSparkData(30, 2000, 8000), label: '30-day trend' },
    { id: 'cpu', title: 'CPU Usage', type: 'progress', value: 62, max: 100, label: 'Server CPU' },
    { id: 'memory', title: 'Memory', type: 'progress', value: 78, max: 100, label: 'RAM Usage' },
    { id: 'requests', title: 'Requests/s', type: 'sparkline', data: genSparkData(30, 400, 1200), label: '30-day trend' },
    { id: 'bounce', title: 'Bounce Rate', type: 'metric', value: '34.2%', change: '-2.1%', dir: 'up', label: '7-day avg' },
    { id: 'bandwidth', title: 'Bandwidth', type: 'sparkline', data: genSparkData(30, 50, 300), label: 'Mbps' },
    { id: 'storage', title: 'Storage', type: 'progress', value: 54, max: 100, label: 'Disk Usage' },
  ];
  let panels = [];
  let layout = {};
  let tracking = {};
  let viewTimers = {};
  let rankOrder = [];
  let lockedPanels = new Set();
  let manualPositions = {};
  let throttleTimers = {};
  let lastRenderHash = '';
  let resizeRAF = null;
  let canvasCache = new Map();
  let moreExpanded = false;
  function genSparkData(n, min, max) {
    const data = []; let v = (min + max) / 2;
    for (let i = 0; i < n; i++) {
      v += (Math.random() - 0.45) * (max - min) * 0.15;
      v = Math.max(min, Math.min(max, v));
      data.push(Math.round(v));
    }
    return data;
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (raw) {
        const saved = JSON.parse(raw);
        tracking = saved.tracking || {};
        lockedPanels = new Set(saved.lockedPanels || []);
        manualPositions = saved.manualPositions || {};
        if (saved.panels) panels = saved.panels;
      }
    } catch(e) {}
    if (!panels.length) {
      panels = INITIAL_PANELS.map(p => ({ ...p, id: p.id, score: p.score || 0.1 }));
    }
    panels.forEach(p => {
      if (!tracking[p.id]) tracking[p.id] = { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
    });
    layout = computeRankedLayout();
  }
  function saveState() {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify({
        panels: panels.map(p => ({ id: p.id, score: p.score })),
        tracking, lockedPanels: [...lockedPanels], manualPositions
      }));
    } catch(e) {}
  }
  function computeScore(panelId) {
    const t = tracking[panelId] || { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
    const now = Date.now();
    const hoursSince = Math.max(0.1, (now - (t.lastInteraction || now)) / 3600000);
    const recency = 1 / (1 + hoursSince * 0.15);
    const freq = Math.log(1 + t.views + t.interactions * 0.5);
    const dur = Math.log(1 + t.totalDuration / 1000);
    return (freq * 0.45 + dur * 0.3 + recency * 0.25) * SCORE_DECAY;
  }
  function computeRankedLayout() {
    const scored = panels.map(p => ({
      id: p.id,
      score: computeScore(p.id),
      locked: lockedPanels.has(p.id),
      manualPos: manualPositions[p.id]
    }));
    scored.sort((a, b) => b.score - a.score);
    rankOrder = scored.map(s => s.id);
    const ranked = {};
    scored.forEach((s, i) => {
      let rank;
      if (s.locked && s.manualPos) {
        rank = s.manualPos.rank !== undefined ? Math.min(s.manualPos.rank, RANK_COUNT - 1) : Math.min(Math.floor(i / Math.max(1, scored.length / RANK_COUNT)), RANK_COUNT - 1);
      } else {
        rank = Math.min(Math.floor(i / Math.max(1, scored.length / RANK_COUNT)), RANK_COUNT - 1);
      }
      ranked[s.id] = { score: s.score, rank, compact: s.score < COMPACT_THRESHOLD && !s.locked };
    });
    return ranked;
  }
  function recordView(panelId) {
    if (!viewTimers[panelId]) {
      viewTimers[panelId] = Date.now();
      tracking[panelId] = tracking[panelId] || { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
      tracking[panelId].views++;
    }
  }
  function endView(panelId) {
    if (viewTimers[panelId]) {
      const duration = Date.now() - viewTimers[panelId];
      tracking[panelId] = tracking[panelId] || { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
      tracking[panelId].totalDuration += duration;
      tracking[panelId].lastInteraction = Date.now();
      delete viewTimers[panelId];
      scheduleRelayout();
    }
  }
  function recordInteraction(panelId) {
    tracking[panelId] = tracking[panelId] || { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 };
    tracking[panelId].interactions++;
    tracking[panelId].lastInteraction = Date.now();
    scheduleRelayout();
  }
  let relayoutTimer = null;
  function scheduleRelayout() {
    if (relayoutTimer) return;
    relayoutTimer = setTimeout(() => {
      relayoutTimer = null;
      const oldHash = lastRenderHash;
      const newLayout = computeRankedLayout();
      const newHash = JSON.stringify(newLayout);
      if (newHash !== oldHash) {
        layout = newLayout;
        updatePanelDOM();
        saveState();
      }
    }, DEBOUNCE_MS);
  }
  function buildPanelDOM(panel) {
    const lay = layout[panel.id] || { rank: 2, compact: false };
    const el = document.getElementById('panel-' + panel.id);
    if (!el) return null;
    return el;
  }
  function updatePanelDOM() {
    const container = document.getElementById('dashboard');
    const moreGrid = document.getElementById('moreGrid');
    const moreSection = document.getElementById('moreSection');
    const moreCount = document.getElementById('moreCount');
    const newHash = JSON.stringify(layout);
    if (newHash === lastRenderHash) return;
    lastRenderHash = newHash;
    const visiblePanels = panels.filter(p => !layout[p.id]?.compact);
    const compactPanels = panels.filter(p => layout[p.id]?.compact);
    visiblePanels.sort((a, b) => (layout[a.id]?.score || 0) < (layout[b.id]?.score || 0) ? 1 : -1);
    const existingIds = new Set();
    container.querySelectorAll('.panel').forEach(el => existingIds.add(el.id.replace('panel-', '')));
    visiblePanels.forEach((panel, idx) => {
      const elId = 'panel-' + panel.id;
      let el = document.getElementById(elId);
      if (!el) {
        el = createPanelElement(panel);
        container.appendChild(el);
      }
      const rank = layout[panel.id]?.rank ?? 2;
      el.className = 'panel rank-' + rank;
      if (lockedPanels.has(panel.id)) el.classList.add('locked');
      el.style.order = idx;
      el.setAttribute('data-rank', rank);
      el.setAttribute('data-score', (layout[panel.id]?.score || 0).toFixed(3));
      updatePanelContent(el, panel);
    });
    panels.filter(p => layout[p.id]?.compact).forEach(panel => {
      const elId = 'panel-' + panel.id;
      let el = document.getElementById(elId);
      if (el && el.parentElement === container) {
        el.remove();
      }
    });
    compactPanels.forEach(panel => {
      const elId = 'panel-compact-' + panel.id;
      let el = document.getElementById(elId);
      if (!el) {
        el = createPanelElement(panel, true);
        el.id = elId;
        moreGrid.appendChild(el);
      }
      el.className = 'panel compact';
      updatePanelContent(el, panel, true);
    });
    moreGrid.querySelectorAll('.panel').forEach(el => {
      const id = el.id.replace('panel-compact-', '');
      if (!compactPanels.find(p => p.id === id)) el.remove();
    });
    moreCount.textContent = compactPanels.length;
    moreSection.classList.toggle('visible', compactPanels.length > 0);
    if (compactPanels.length === 0) moreExpanded = false;
    updateMoreToggle();
    invalidateCanvasCache();
  }
  function updateMoreToggle() {
    const toggle = document.getElementById('moreToggle');
    const grid = document.getElementById('moreGrid');
    if (moreExpanded) {
      toggle.innerHTML = '&#9660; More panels (<span id="moreCount">' + grid.children.length + '</span>)';
      grid.style.display = 'grid';
    } else {
      toggle.innerHTML = '&#9654; More panels (<span id="moreCount">' + grid.children.length + '</span>)';
      grid.style.display = 'none';
    }
  }
  function createPanelElement(panel, compact) {
    const el = document.createElement('div');
    el.className = 'panel' + (compact ? ' compact' : '');
    el.id = (compact ? 'panel-compact-' : 'panel-') + panel.id;
    el.setAttribute('data-panel-id', panel.id);
    el.innerHTML = `
      <div class="panel-header">
        <span class="panel-title">${panel.title}</span>
        <span class="panel-score" id="score-${panel.id}">0.00</span>
        <div class="panel-actions">
          <button class="lock-btn" data-action="lock" data-panel="${panel.id}" title="Lock position">&#128274;</button>
          <button data-action="focus" data-panel="${panel.id}" title="Expand">&#9971;</button>
        </div>
      </div>
      <div class="panel-body" id="body-${panel.id}"></div>
      ${compact ? '<div class="compact-preview" id="preview-' + panel.id + '"></div>' : ''}
      <div class="resize-handle" data-action="resize" data-panel="${panel.id}"></div>
    `;
    return el;
  }
  function updatePanelContent(el, panel, compact) {
    const scoreEl = el.querySelector('.panel-score');
    if (scoreEl && layout[panel.id]) {
      scoreEl.textContent = layout[panel.id].score.toFixed(2);
    }
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.className = 'lock-btn' + (lockedPanels.has(panel.id) ? ' locked-btn' : '');
      lockBtn.innerHTML = lockedPanels.has(panel.id) ? '&#128274;' : '&#128275;';
    }
    if (compact) {
      const preview = el.querySelector('.compact-preview');
      if (preview) {
        preview.innerHTML = renderCompactPreview(panel);
      }
      return;
    }
    const body = el.querySelector('.panel-body');
    if (!body) return;
    const cacheKey = panel.id + '|' + JSON.stringify(panel);
    if (body.getAttribute('data-cache') === cacheKey) return;
    body.setAttribute('data-cache', cacheKey);
    body.innerHTML = renderPanelBody(panel);
    requestAnimationFrame(() => {
      const canvas = body.querySelector('canvas');
      if (canvas) drawCanvasFromCache(canvas, panel);
    });
  }
  function renderPanelBody(panel) {
    switch (panel.type) {
      case 'metric':
        return `
          <div class="metric-value">${panel.value}</div>
          <div class="metric-label">${panel.label}</div>
          <div class="metric-change ${panel.dir}">${panel.change}</div>`;
      case 'progress':
        const pct = Math.round((panel.value / panel.max) * 100);
        const color = pct > 80 ? 'var(--red)' : pct > 60 ? 'var(--orange)' : 'var(--green)';
        return `
          <div style="display:flex;align-items:center;gap:12px;">
            <div class="progress-ring"><canvas width="64" height="64" data-panel="${panel.id}" data-value="${panel.value}" data-max="${panel.max}"></canvas></div>
            <div>
              <div class="metric-value">${pct}%</div>
              <div class="metric-label">${panel.label}</div>
            </div>
          </div>`;
      case 'sparkline':
        return `
          <canvas class="sparkline-canvas" width="300" height="40" data-panel="${panel.id}" data-spark="${(panel.data||[]).join(',')}"></canvas>
          <div class="metric-label">${panel.label}</div>`;
      default:
        return `<div class="metric-value">${panel.value || '—'}</div>`;
    }
  }
  function renderCompactPreview(panel) {
    let val = panel.value || '—';
    if (panel.type === 'progress') val = Math.round((panel.value / panel.max) * 100) + '%';
    return `<span class="mini-val">${val}</span><span style="font-size:10px">${panel.title}</span>`;
  }
  function drawCanvasFromCache(canvas, panel) {
    if (!canvas) return;
    const key = canvas.getAttribute('data-spark') || canvas.getAttribute('data-value');
    if (!key) return;
    if (canvasCache.get(key) === canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    if (canvas.classList.contains('sparkline-canvas')) {
      const data = (canvas.getAttribute('data-spark') || '').split(',').map(Number).filter(n => !isNaN(n));
      if (!data.length) return;
      ctx.clearRect(0, 0, w, h);
      const max = Math.max(...data), min = Math.min(...data);
      const range = max - min || 1;
      ctx.beginPath();
      ctx.strokeStyle = '#58a6ff';
      ctx.lineWidth = 1.5;
      data.forEach((v, i) => {
        const x = (i / (data.length - 1)) * w;
        const y = h - ((v - min) / range) * (h - 4) - 2;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      });
      ctx.stroke();
      const lastX = w, lastY = h - ((data[data.length-1] - min) / range) * (h - 4) - 2;
      ctx.beginPath(); ctx.arc(lastX - 1, lastY, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#58a6ff'; ctx.fill();
    } else {
      const val = parseFloat(canvas.getAttribute('data-value')) || 0;
      const max = parseFloat(canvas.getAttribute('data-max')) || 100;
      const pct = val / max;
      ctx.clearRect(0, 0, w, h);
      const cx = w/2, cy = h/2, r = 28, lw = 4;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'var(--border)'; ctx.lineWidth = lw; ctx.stroke();
      ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI/2, -Math.PI/2 + Math.PI * 2 * pct);
      const color = pct > 0.8 ? '#f85149' : pct > 0.6 ? '#d2991d' : '#3fb950';
      ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.stroke();
    }
    canvasCache.set(key, canvas);
  }
  function invalidateCanvasCache() {
    canvasCache.clear();
    requestAnimationFrame(() => {
      document.querySelectorAll('canvas').forEach(c => {
        const panelId = c.getAttribute('data-panel');
        if (panelId) {
          const panel = panels.find(p => p.id === panelId);
          if (panel) drawCanvasFromCache(c, panel);
        }
      });
    });
  }
  let observer = null;
  function setupViewTracking() {
    if (observer) observer.disconnect();
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const panelId = entry.target.getAttribute('data-panel-id');
        if (!panelId) return;
        if (entry.isIntersecting && entry.intersectionRatio > 0.4) {
          recordView(panelId);
        } else {
          endView(panelId);
        }
      });
    }, { threshold: [0, 0.4] });
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  }
  function handlePanelClick(e) {
    const action = e.target.getAttribute('data-action') || e.target.closest('[data-action]')?.getAttribute('data-action');
    const panelId = e.target.getAttribute('data-panel') || e.target.closest('[data-panel]')?.getAttribute('data-panel');
    if (!panelId) return;
    if (action === 'lock') {
      e.stopPropagation();
      if (lockedPanels.has(panelId)) {
        lockedPanels.delete(panelId);
        delete manualPositions[panelId];
      } else {
        lockedPanels.add(panelId);
        const curLayout = layout[panelId];
        manualPositions[panelId] = { rank: curLayout?.rank ?? 2 };
      }
      recordInteraction(panelId);
      layout = computeRankedLayout();
      updatePanelDOM();
      saveState();
      showToast(lockedPanels.has(panelId) ? 'Panel locked' : 'Panel unlocked');
    } else if (action === 'focus') {
      e.stopPropagation();
      showFocusPanel(panelId);
      recordInteraction(panelId);
    }
  }
  function showFocusPanel(panelId) {
    const panel = panels.find(p => p.id === panelId);
    if (!panel) return;
    const overlay = document.getElementById('focusOverlay');
    const focusPanel = document.getElementById('focusPanel');
    focusPanel.innerHTML = `
      <button class="focus-close" id="focusClose">&times;</button>
      <h2 style="margin-bottom:16px;">${panel.title}</h2>
      <div>${renderPanelBody(panel)}</div>
      <div style="margin-top:16px;font-size:11px;color:var(--text-dim)">
        Score: ${(layout[panelId]?.score || 0).toFixed(3)} | Views: ${tracking[panelId]?.views || 0} | Interactions: ${tracking[panelId]?.interactions || 0}
      </div>
    `;
    overlay.classList.add('active');
    requestAnimationFrame(() => {
      const canvas = focusPanel.querySelector('canvas');
      if (canvas) {
        const pId = canvas.getAttribute('data-panel');
        const p = panels.find(pp => pp.id === pId);
        if (p) drawCanvasFromCache(canvas, p);
      }
    });
  }
  function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 1800);
  }
  document.addEventListener('click', function(e) {
    handlePanelClick(e);
    if (e.target.id === 'focusClose' || e.target.id === 'focusOverlay') {
      document.getElementById('focusOverlay').classList.remove('active');
    }
    if (e.target.id === 'btnReset') {
      panels = INITIAL_PANELS.map(p => ({ ...p, score: 0.1 }));
      tracking = {};
      lockedPanels.clear();
      manualPositions = {};
      panels.forEach(p => { tracking[p.id] = { views: 0, totalDuration: 0, lastInteraction: 0, interactions: 0 }; });
      layout = computeRankedLayout();
      rebuildAllDOM();
      saveState();
      showToast('Layout reset');
    }
    if (e.target.id === 'btnExport') {
      const cfg = { panels: panels.map(p => ({ id: p.id, score: p.score })), tracking, lockedPanels: [...lockedPanels], manualPositions };
      navigator.clipboard.writeText(JSON.stringify(cfg, null, 2)).then(() => showToast('Config copied'));
    }
    if (e.target.id === 'moreToggle' || e.target.closest('#moreToggle')) {
      moreExpanded = !moreExpanded;
      updateMoreToggle();
    }
  });
  function rebuildAllDOM() {
    const container = document.getElementById('dashboard');
    const moreGrid = document.getElementById('moreGrid');
    container.innerHTML = '';
    moreGrid.innerHTML = '';
    lastRenderHash = '';
    canvasCache.clear();
    updatePanelDOM();
    setupViewTracking();
  }
  let resizeTimer = null;
  function onResize() {
    if (resizeTimer) return;
    resizeTimer = setTimeout(() => {
      resizeTimer = null;
      invalidateCanvasCache();
    }, RESIZE_DEBOUNCE);
  }
  window.addEventListener('resize', onResize, { passive: true });
  document.addEventListener('mousemove', function(e) {
    const panelEl = e.target.closest('.panel');
    if (panelEl) {
      const panelId = panelEl.getAttribute('data-panel-id');
      if (panelId && !throttleTimers['move_' + panelId]) {
        throttleTimers['move_' + panelId] = true;
        recordInteraction(panelId);
        setTimeout(() => { delete throttleTimers['move_' + panelId]; }, THROTTLE_MS);
      }
    }
  }, { passive: true });
  setInterval(() => {
    panels.forEach(p => {
      p.score = computeScore(p.id);
    });
    layout = computeRankedLayout();
    updatePanelDOM();
    setupViewTracking();
    saveState();
  }, 30000);
  function init() {
    loadState();
    rebuildAllDOM();
    document.getElementById('trackStatus').textContent = 'tracking active';
  }
  init();
})();
</script>
</body>
</html>