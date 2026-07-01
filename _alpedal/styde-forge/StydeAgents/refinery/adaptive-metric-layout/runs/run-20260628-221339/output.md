<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; background: #0f1117; color: #e1e4e8; min-height: 100vh; }
header { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; background: #161b22; border-bottom: 1px solid #30363d; }
header h1 { font-size: 18px; font-weight: 600; color: #f0f6fc; }
header .controls { display: flex; gap: 12px; align-items: center; }
header .controls button { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; transition: background .15s; }
header .controls button:hover { background: #30363d; }
header .controls button.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
header .stats { font-size: 12px; color: #8b949e; }
#dashboard-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 16px 24px; transition: grid-template-columns .4s ease; }
.panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; position: relative; transition: all .4s cubic-bezier(.4,0,.2,1); min-width: 0; }
.panel.expanded { grid-column: span 2; grid-row: span 2; }
.panel.medium { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; }
.panel.compact .panel-body > *:not(.compact-preview) { display: none; }
.panel.compact .panel-body .compact-preview { display: flex; }
.panel.locked { border-color: #58a6ff; box-shadow: 0 0 0 1px #58a6ff; }
.panel-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border-bottom: 1px solid #21262d; cursor: grab; user-select: none; }
.panel.locked .panel-header { cursor: default; }
.panel-header .panel-title { font-size: 13px; font-weight: 600; color: #f0f6fc; display: flex; align-items: center; gap: 8px; }
.panel-header .panel-title .rank-badge { font-size: 10px; background: #1f6feb; color: #fff; border-radius: 10px; padding: 1px 7px; font-weight: 500; }
.panel-header .panel-actions { display: flex; gap: 4px; }
.panel-header .panel-actions button { background: none; border: none; color: #8b949e; cursor: pointer; font-size: 13px; padding: 2px 6px; border-radius: 4px; transition: all .15s; }
.panel-header .panel-actions button:hover { background: #21262d; color: #e1e4e8; }
.panel-header .panel-actions button.lock-btn.active { color: #58a6ff; }
.panel-body { padding: 12px; }
.panel-body .mini-chart { height: 100px; position: relative; margin-bottom: 8px; }
.panel-body .mini-chart canvas { width: 100%; height: 100%; display: block; border-radius: 4px; }
.panel-body .metric-value { font-size: 24px; font-weight: 700; color: #f0f6fc; margin-bottom: 4px; }
.panel-body .metric-label { font-size: 12px; color: #8b949e; }
.panel-body .compact-preview { display: none; align-items: center; gap: 12px; padding: 4px 0; }
.panel-body .compact-preview .cp-value { font-size: 20px; font-weight: 700; color: #f0f6fc; }
.panel-body .compact-preview .cp-label { font-size: 11px; color: #8b949e; }
.panel-body .compact-preview .cp-trend { font-size: 12px; }
.panel-body .compact-preview .cp-trend.up { color: #3fb950; }
.panel-body .compact-preview .cp-trend.down { color: #f85149; }
.panel .attention-overlay { position: absolute; bottom: 4px; right: 8px; font-size: 10px; color: #484f58; opacity: 0; transition: opacity .3s; }
.panel:hover .attention-overlay { opacity: 1; }
.panel .resize-handle { position: absolute; bottom: 0; right: 0; width: 14px; height: 14px; cursor: nwse-resize; background: linear-gradient(135deg, transparent 50%, #30363d 50%); border-radius: 0 0 8px 0; }
#idle-warning { position: fixed; bottom: 20px; right: 20px; background: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; font-size: 12px; color: #8b949e; max-width: 280px; display: none; z-index: 100; }
#idle-warning.show { display: block; }
@media (max-width: 900px) { #dashboard-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { #dashboard-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Dashboard</h1>
  <div class="controls">
    <span class="stats" id="stats-display">0 panels | adapting...</span>
    <button id="reset-btn" title="Reset all layout overrides">Reset Layout</button>
    <button id="adapt-btn" title="Force adaptation tick">Adapt Now</button>
    <button id="auto-toggle" class="active">Auto</button>
  </div>
</header>
<div id="dashboard-grid"></div>
<div id="idle-warning">Dashboard is watching your attention patterns. Interact with panels to influence layout.</div>
<script>
(function() {
// ─── Event Bus (decoupled per-widget communication) ───
const bus = {
  _listeners: {},
  on(event, handler) {
    (this._listeners[event] = this._listeners[event] || []).push(handler);
    return () => this.off(event, handler);
  },
  off(event, handler) {
    const handlers = this._listeners[event];
    if (!handlers) return;
    const idx = handlers.indexOf(handler);
    if (idx !== -1) handlers.splice(idx, 1);
  },
  emit(event, data) {
    const handlers = this._listeners[event];
    if (!handlers) return;
    for (const h of handlers) h(data);
  }
};
// ─── Panel Definitions ───
const PANEL_DEFS = [
  { id: 'revenue',     title: 'Revenue',        chartType: 'line',   baseValue: 142500 },
  { id: 'users',       title: 'Active Users',    chartType: 'bar',    baseValue: 8432 },
  { id: 'conversion',  title: 'Conversion Rate',  chartType: 'line',   baseValue: 3.42 },
  { id: 'churn',       title: 'Churn Rate',       chartType: 'line',   baseValue: 1.8 },
  { id: 'sessions',    title: 'Sessions',         chartType: 'bar',    baseValue: 32100 },
  { id: 'pageviews',   title: 'Page Views',       chartType: 'line',   baseValue: 187000 },
  { id: 'bounce',      title: 'Bounce Rate',      chartType: 'line',   baseValue: 34.2 },
  { id: 'ltv',         title: 'LTV',              chartType: 'bar',    baseValue: 128 },
  { id: 'retention',   title: 'Retention',        chartType: 'line',   baseValue: 76.5 },
  { id: 'acquisition', title: 'Acquisition Cost',  chartType: 'bar',    baseValue: 12.5 }
];
// ─── State ───
const STORAGE_KEY = 'adaptive_dashboard_layout_v2';
let panels = [];
let autoAdapt = true;
let adaptScheduled = false;
let clock = 0;
// ─── Weighted-Decision Adaptation Engine ───
function computeAttentionScore(p, now) {
  const freq = p.interactionCount || 0;
  const dur = p.totalDuration || 0;
  const recencyHours = (now - (p.lastInteraction || 0)) / (1000 * 60 * 60);
  const recencyWeight = Math.exp(-recencyHours * 0.1);
  const freqWeight = 1 - Math.exp(-freq * 0.15);
  const durWeight = 1 - Math.exp(-dur * 0.001);
  const base = freqWeight * 0.4 + durWeight * 0.35 + recencyWeight * 0.25;
  const engagementDecay = Math.exp(-p.adaptationAge * 0.05);
  return base * 100 * engagementDecay;
}
function getAdaptationDecision(panel, now) {
  const score = computeAttentionScore(panel, now);
  const cohortAge = panel.adaptationAge || 0;
  let decision = 'medium';
  let priority = 0;
  if (score > 65 && cohortAge < 30) { decision = 'expanded'; priority = 3; }
  else if (score > 35 && cohortAge < 60) { decision = 'medium'; priority = 2; }
  else { decision = 'compact'; priority = 1; }
  return { score, decision, priority };
}
// ─── Widget Render (decoupled per-panel) ───
function renderWidget(panel, container) {
  const now = Date.now();
  const adapt = getAdaptationDecision(panel, now);
  const isLarge = adapt.decision === 'expanded';
  const isCompact = adapt.decision === 'compact';
  const baseValue = panel.baseValue || 100;
  const trend = panel.lastTrend || (Math.random() > 0.5 ? 'up' : 'down');
  const trendPct = ((Math.random() * 6) + 1).toFixed(1);
  container.querySelector('.metric-value').textContent =
    isCompact ? '' : formatValue(baseValue + (panel._trendOffset || 0));
  container.querySelector('.metric-label').textContent =
    isCompact ? '' : (panel.title + ' — last 30 days');
  container.querySelector('.cp-value').textContent =
    formatValue(baseValue + (panel._trendOffset || 0));
  container.querySelector('.cp-label').textContent = panel.title;
  container.querySelector('.cp-trend').textContent =
    (trend === 'up' ? '+' : '') + trendPct + '%';
  container.querySelector('.cp-trend').className =
    'cp-trend ' + (trend === 'up' ? 'up' : 'down');
  if (container._lastChartRender !== adapt.decision) {
    drawMiniChart(panel, container, isLarge);
    container._lastChartRender = adapt.decision;
  }
}
function formatValue(v) {
  if (v > 1e6) return (v / 1e6).toFixed(1) + 'M';
  if (v > 1e3) return (v / 1e3).toFixed(1) + 'K';
  if (Number.isInteger(v)) return v.toLocaleString();
  return v.toFixed(2);
}
function drawMiniChart(panel, container, isLarge) {
  const canvas = container.querySelector('.mini-chart canvas');
  if (!canvas) return;
  const rect = container.querySelector('.mini-chart').getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = (rect.width || 120) * dpr;
  canvas.height = (isLarge ? 140 : 80) * dpr;
  canvas.style.height = (isLarge ? 140 : 80) + 'px';
  canvas.style.width = (rect.width || 120) + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const w = canvas.width / dpr;
  const h = canvas.height / dpr;
  ctx.clearRect(0, 0, w, h);
  const data = [];
  const points = isLarge ? 24 : 10;
  for (let i = 0; i < points; i++) {
    data.push(30 + Math.sin(i * 0.8 + panel._phase) * 15 + (Math.random() - 0.5) * 8);
  }
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const pad = 6;
  ctx.beginPath();
  data.forEach((v, i) => {
    const x = pad + (i / (points - 1)) * (w - pad * 2);
    const y = h - pad - ((v - min) / range) * (h - pad * 2);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  const color = panel._color || '#1f6feb';
  ctx.strokeStyle = color;
  ctx.lineWidth = isLarge ? 2.5 : 1.5;
  ctx.stroke();
  if (isLarge) {
    ctx.fillStyle = color + '15';
    ctx.lineTo(w - pad, h - pad);
    ctx.lineTo(pad, h - pad);
    ctx.closePath();
    ctx.fill();
    ctx.font = '10px system-ui';
    ctx.fillStyle = '#484f58';
    ctx.textAlign = 'right';
    ctx.fillText(max.toFixed(0), w - 4, 12);
    ctx.fillText(min.toFixed(0), w - 4, h - 4);
  }
}
// ─── Adaptation Controller (rAF-throttled) ───
const adaptationController = {
  _tickId: null,
  _lastTick: 0,
  _intervalMs: 2000,
  schedule() {
    if (!autoAdapt) return;
    if (this._tickId) return;
    this._tickId = requestAnimationFrame((ts) => this._tick(ts));
  },
  _tick(ts) {
    this._tickId = null;
    if (ts - this._lastTick < this._intervalMs) {
      this._tickId = requestAnimationFrame((t) => this._tick(t));
      return;
    }
    this._lastTick = ts;
    clock++;
    for (const p of panels) {
      p.adaptationAge = (p.adaptationAge || 0) + 1;
    }
    this._runAdaptation();
    if (autoAdapt) {
      this._tickId = requestAnimationFrame((t) => this._tick(t));
    }
  },
  _runAdaptation() {
    if (autoAdapt) {
      recalcLayout();
    }
  },
  forceTick() {
    if (this._tickId) {
      cancelAnimationFrame(this._tickId);
      this._tickId = null;
    }
    this._lastTick = 0;
    for (const p of panels) { p.adaptationAge = (p.adaptationAge || 0) + 1; }
    recalcLayout();
    if (autoAdapt) {
      this._tickId = requestAnimationFrame((t) => this._tick(t));
    }
  },
  stop() {
    if (this._tickId) {
      cancelAnimationFrame(this._tickId);
      this._tickId = null;
    }
  }
};
// ─── Layout Calculation ───
function recalcLayout() {
  const now = Date.now();
  const scored = panels.map(p => ({
    p, ...getAdaptationDecision(p, now), rawScore: computeAttentionScore(p, now)
  }));
  scored.sort((a, b) => b.score - a.score);
  const grid = document.getElementById('dashboard-grid');
  const unlockedPanels = new Set(panels.filter(p => !p.locked).map(p => p.id));
  const lockedList = panels.filter(p => p.locked);
  const unlockedList = scored.filter(s => unlockedPanels.has(s.p.id));
  // Place locked first in their stored positions, then fill with scored
  const orderedPanels = [];
  const placedIds = new Set();
  for (const lp of lockedList) {
    orderedPanels.push({ ...lp, decision: lp.manualDecision || lp._lastDecision || 'medium', score: computeAttentionScore(lp, now) });
    placedIds.add(lp.id);
  }
  for (const s of unlockedList) {
    if (!placedIds.has(s.p.id)) {
      orderedPanels.push(s);
      placedIds.add(s.p.id);
    }
  }
  // Append any panels not in either list (shouldn't happen, but safety)
  for (const p of panels) {
    if (!placedIds.has(p.id)) {
      orderedPanels.push({ p, decision: 'compact', score: 0 });
      placedIds.add(p.id);
    }
  }
  // Apply decisions
  for (const entry of orderedPanels) {
    const p = entry.p;
    const el = p._el;
    if (!el) continue;
    if (p.locked && p.manualDecision) {
      p._lastDecision = p.manualDecision;
      p._lastScore = computeAttentionScore(p, now);
    } else {
      p._lastDecision = entry.decision;
      p._lastScore = entry.score;
    }
    el.className = 'panel ' + (p.locked ? 'locked ' : '') + p._lastDecision;
    el.querySelector('.rank-badge').textContent =
      p.locked ? '\uD83D\uDD12' : '#' + (orderedPanels.indexOf(entry) + 1);
    el.style.order = orderedPanels.indexOf(entry);
    // Update attention overlay
    el.querySelector('.attention-overlay').textContent =
      'score: ' + (p._lastScore).toFixed(0) + ' | interactions: ' + (p.interactionCount || 0);
    // Render widget content (decoupled — only this panel)
    renderWidget(p, el);
  }
  bus.emit('layout-changed', { panels: orderedPanels });
  updateStats();
  saveState();
}
function updateStats() {
  const expanded = panels.filter(p => p._lastDecision === 'expanded').length;
  const compact = panels.filter(p => p._lastDecision === 'compact').length;
  const locked = panels.filter(p => p.locked).length;
  document.getElementById('stats-display').textContent =
    panels.length + ' panels | ' + expanded + ' expanded | ' + compact + ' compact | ' + locked + ' locked';
}
// ─── Tracking ───
const tracker = {
  _visibilityStarts: {},
  _activePanel: null,
  startTracking() {
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this._flushActivePanel();
      }
    });
    window.addEventListener('beforeunload', () => this._flushActivePanel());
    // Scroll-based visibility tracking (IntersectionObserver)
    const obs = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const p = panels.find(p => p._el === entry.target);
        if (!p) continue;
        if (entry.isIntersecting) {
          p._visible = true;
          p._lastVisibilityStart = Date.now();
        } else {
          p._visible = false;
          if (p._lastVisibilityStart) {
            p.totalDuration = (p.totalDuration || 0) + (Date.now() - p._lastVisibilityStart);
            p._lastVisibilityStart = null;
          }
        }
      }
    }, { threshold: [0, 0.5] });
    for (const p of panels) {
      if (p._el) obs.observe(p._el);
    }
  },
  _flushActivePanel() {
    for (const p of panels) {
      if (p._visible && p._lastVisibilityStart) {
        p.totalDuration = (p.totalDuration || 0) + (Date.now() - p._lastVisibilityStart);
        p._lastVisibilityStart = 0;
      }
    }
  }
};
// ─── Build DOM ───
function buildDashboard() {
  const grid = document.getElementById('dashboard-grid');
  grid.innerHTML = '';
  panels = PANEL_DEFS.map((def, i) => {
    const now = Date.now();
    const p = {
      ...def,
      interactionCount: 0,
      totalDuration: 0,
      lastInteraction: now,
      adaptationAge: 0,
      locked: false,
      manualDecision: null,
      _lastDecision: 'medium',
      _lastScore: 50,
      _phase: Math.random() * Math.PI * 2,
      _trendOffset: (Math.random() - 0.5) * (def.baseValue * 0.15),
      _visible: false
    };
    p._color = ['#1f6feb', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#79c0ff', '#ff7b72', '#58a6ff', '#f0883e', '#7ee787'][i % 10];
    return p;
  });
  for (const p of panels) {
    const el = document.createElement('div');
    el.className = 'panel medium';
    el.dataset.panelId = p.id;
    // Determine initial decision based on index (first 3 expanded, middle 4 medium, rest compact)
    const idx = panels.indexOf(p);
    let initDecision = 'compact';
    if (idx < 3) initDecision = 'expanded';
    else if (idx < 7) initDecision = 'medium';
    p._lastDecision = initDecision;
    el.classList.add(initDecision);
    el.innerHTML = `
      <div class="panel-header">
        <div class="panel-title">
          <span class="rank-badge">#${idx + 1}</span>
          <span>${p.title}</span>
        </div>
        <div class="panel-actions">
          <button class="lock-btn" title="Lock position">${String.fromCodePoint(0x1F512)}</button>
          <button class="expand-btn" title="Toggle expand/collapse">${String.fromCodePoint(0x26F6)}</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="mini-chart"><canvas></canvas></div>
        <div class="metric-value">${formatValue(p.baseValue)}</div>
        <div class="metric-label">${p.title} — last 30 days</div>
        <div class="compact-preview">
          <div class="cp-value">${formatValue(p.baseValue)}</div>
          <div class="cp-label">${p.title}</div>
          <div class="cp-trend up">+3.2%</div>
        </div>
        <div class="attention-overlay">score: 50 | interactions: 0</div>
      </div>
      <div class="resize-handle"></div>
    `;
    grid.appendChild(el);
    p._el = el;
    // ─── Decoupled widget render via event bus subscription ───
    const unsub = bus.on('tick-' + p.id, () => renderWidget(p, el));
    p._unsub = unsub;
    // Track interaction: click
    el.querySelector('.panel-header').addEventListener('click', (e) => {
      if (e.target.closest('.panel-actions')) return;
      p.interactionCount = (p.interactionCount || 0) + 1;
      p.lastInteraction = Date.now();
      if (autoAdapt) adaptationController.schedule();
    });
    // Lock toggle
    el.querySelector('.lock-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      p.locked = !p.locked;
      el.querySelector('.lock-btn').classList.toggle('active', p.locked);
      if (!p.locked) p.manualDecision = null;
      recalcLayout();
      saveState();
    });
    // Manual expand/collapse override
    el.querySelector('.expand-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      if (!p.locked) {
        p.locked = true;
        el.querySelector('.lock-btn').classList.add('active');
      }
      const current = p._lastDecision || 'medium';
      const cycle = { expanded: 'compact', compact: 'medium', medium: 'expanded' };
      p.manualDecision = cycle[current] || 'medium';
      recalcLayout();
      saveState();
    });
  }
  tracker.startTracking();
  loadState();
  recalcLayout();
  // Start adaptation controller
  adaptationController.schedule();
  // Auto-adapt on any interaction anywhere
  document.addEventListener('click', () => {
    if (autoAdapt) adaptationController.schedule();
  });
  // Periodic tick even without interaction (decay-based adaptation)
  setInterval(() => {
    if (autoAdapt) adaptationController.schedule();
  }, 5000);
}
// ─── Persistence ───
function saveState() {
  try {
    const data = panels.map(p => ({
      id: p.id,
      locked: p.locked,
      interactionCount: p.interactionCount,
      totalDuration: p.totalDuration,
      lastInteraction: p.lastInteraction,
      adaptationAge: p.adaptationAge,
      manualDecision: p.manualDecision,
      _lastDecision: p._lastDecision,
      _lastScore: p._lastScore
    }));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {}
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const saved = JSON.parse(raw);
    for (const s of saved) {
      const p = panels.find(p => p.id === s.id);
      if (!p) continue;
      p.locked = s.locked;
      p.interactionCount = s.interactionCount || 0;
      p.totalDuration = s.totalDuration || 0;
      p.lastInteraction = s.lastInteraction || Date.now();
      p.adaptationAge = s.adaptationAge || 0;
      p.manualDecision = s.manualDecision || null;
      p._lastDecision = s._lastDecision || 'medium';
      p._lastScore = s._lastScore || 50;
      if (p._el && p.locked) {
        p._el.querySelector('.lock-btn').classList.add('active');
      }
    }
  } catch (e) {}
}
// ─── Reset ───
function resetLayout() {
  localStorage.removeItem(STORAGE_KEY);
  for (const p of panels) {
    p.locked = false;
    p.manualDecision = null;
    p.interactionCount = 0;
    p.totalDuration = 0;
    p.lastInteraction = Date.now();
    p.adaptationAge = 0;
    const idx = panels.indexOf(p);
    const initDecision = idx < 3 ? 'expanded' : (idx < 7 ? 'medium' : 'compact');
    p._lastDecision = initDecision;
    p._lastScore = 50;
    if (p._el) {
      p._el.querySelector('.lock-btn').classList.remove('active');
    }
  }
  recalcLayout();
}
// ─── Controls ───
document.addEventListener('DOMContentLoaded', () => {
  buildDashboard();
  document.getElementById('reset-btn').addEventListener('click', resetLayout);
  document.getElementById('adapt-btn').addEventListener('click', () => {
    adaptationController.forceTick();
  });
  document.getElementById('auto-toggle').addEventListener('click', function() {
    autoAdapt = !autoAdapt;
    this.classList.toggle('active', autoAdapt);
    this.textContent = autoAdapt ? 'Auto' : 'Manual';
    if (autoAdapt) {
      adaptationController.schedule();
    } else {
      adaptationController.stop();
    }
  });
  // Show idle warning after 5s
  setTimeout(() => {
    document.getElementById('idle-warning').classList.add('show');
    setTimeout(() => {
      document.getElementById('idle-warning').classList.remove('show');
    }, 6000);
  }, 5000);
  // Expose for debugging
  window.__dashboard = { panels, recalcLayout, adaptationController, bus };
});
})();
</script>
</body>
</html>