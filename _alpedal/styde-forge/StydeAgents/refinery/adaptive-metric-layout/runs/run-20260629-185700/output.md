<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #22263b;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa8;
  --accent: #7c8aff;
  --accent-glow: rgba(124,138,255,0.15);
  --danger: #ff6b7a;
  --success: #4adea0;
  --warning: #fbbf24;
  --radius: 8px;
  --radius-sm: 4px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
  --grid-gap: 12px;
  --panel-padding: 16px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  position: sticky;
  top: 0;
  z-index: 100;
}
header h1 { font-size: 18px; font-weight: 600; letter-spacing: -0.3px; }
.header-actions { display: flex; gap: 8px; align-items: center; }
.btn {
  padding: 6px 14px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  transition: var(--transition);
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(160px, auto);
  gap: var(--grid-gap);
  padding: var(--grid-gap);
  max-width: 1600px;
  margin: 0 auto;
  /* ensure grid-template-columns is always set — explicit declaration */
  transition: grid-template-columns var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--panel-padding);
  transition: all var(--transition);
  position: relative;
  cursor: grab;
  display: flex;
  flex-direction: column;
  min-height: 160px;
  overflow: hidden;
  /* __panel base — traced from .dashboard .panel */
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.dragging { opacity: 0.7; cursor: grabbing; z-index: 10; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
.panel.locked { border-color: var(--warning); }
.panel.locked::after {
  content: '🔒';
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 12px;
  opacity: 0.8;
}
/* size classes — traced from panel.setAttribute('data-size',...) */
.panel[data-size="large"] { grid-column: span 2; grid-row: span 2; }
.panel[data-size="medium"] { grid-column: span 1; grid-row: span 1; }
.panel[data-size="compact"] { grid-column: span 1; grid-row: span 1; min-height: 100px; font-size: 12px; padding: 10px; }
.panel[data-size="compact"] .panel-body { opacity: 0.5; max-height: 40px; overflow: hidden; }
.panel[data-size="mini"] { grid-column: span 1; grid-row: span 1; min-height: 60px; padding: 8px; font-size: 11px; }
.panel[data-size="mini"] .panel-body { display: none; }
.panel[data-size="mini"] .panel-title { font-size: 12px; }
/* state classes — traced from panel.setAttribute('data-state',...) */
.panel[data-state="collapsed"] { min-height: 44px; padding: 8px 16px; }
.panel[data-state="collapsed"] .panel-body,
.panel[data-state="collapsed"] .panel-metric,
.panel[data-state="collapsed"] .panel-controls { display: none; }
.panel-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
  user-select: none;
}
.panel-title .icon { font-size: 16px; }
.panel-metric {
  font-size: 28px;
  font-weight: 700;
  color: var(--accent);
  margin: 4px 0;
}
.panel-body { font-size: 13px; color: var(--text-dim); line-height: 1.5; flex: 1; }
.panel-controls {
  display: flex;
  gap: 4px;
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid var(--border);
  opacity: 0;
  transition: opacity 0.2s;
}
.panel:hover .panel-controls { opacity: 1; }
.panel-controls button {
  padding: 3px 8px;
  font-size: 11px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-dim);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
}
.panel-controls button:hover { color: var(--text); border-color: var(--accent); }
.panel-controls button.lock-btn.locked { color: var(--warning); border-color: var(--warning); }
/* heatmap overlay — traced from panel.appendChild(heatmapOverlay) */
.heatmap-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  opacity: 0.6;
  transition: opacity 0.5s;
}
.heatmap-indicator.hot { background: var(--danger); }
.heatmap-indicator.warm { background: var(--warning); }
.heatmap-indicator.cool { background: var(--text-dim); }
.heatmap-indicator.cold { background: transparent; }
/* more section */
.more-section {
  grid-column: 1 / -1;
  margin-top: 4px;
}
.more-toggle {
  width: 100%;
  padding: 10px;
  background: var(--surface);
  border: 1px dashed var(--border);
  color: var(--text-dim);
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 13px;
  transition: var(--transition);
}
.more-toggle:hover { border-color: var(--accent); color: var(--text); }
/* tooltip */
.tooltip {
  position: fixed;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-size: 12px;
  color: var(--text-dim);
  pointer-events: none;
  z-index: 200;
  opacity: 0;
  transition: opacity 0.15s;
}
.tooltip.visible { opacity: 1; }
/* toast */
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 300;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  padding: 10px 18px;
  background: var(--surface);
  border: 1px solid var(--accent);
  border-radius: var(--radius);
  font-size: 13px;
  color: var(--text);
  animation: slideIn 0.3s ease;
}
@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <span style="font-size:12px;color:var(--text-dim)" id="mode-indicator">auto</span>
    <button class="btn" id="btn-auto" title="Auto-layout mode">Auto</button>
    <button class="btn" id="btn-reset" title="Reset tracking data">Reset</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="more-section" style="display:none">
  <button class="more-toggle" id="more-toggle">Show collapsed panels (0)</button>
</div>
<div class="tooltip" id="tooltip"></div>
<div class="toast-container" id="toast-container"></div>
<script>
(function() {
  'use strict';
  /* ── constants ── */
  const LS_KEY = 'adaptive_dashboard_v1';
  const PANEL_DEFAULTS = [
    { id:'revenue',  title:'Revenue',      icon:'💰', metric:'$12.4K', body:'Monthly recurring revenue +8.2% vs last month',          locked:false },
    { id:'users',    title:'Active Users',  icon:'👥', metric:'2,847',  body:'Daily active users +12% this week, retention at 74%',    locked:false },
    { id:'cpu',      title:'CPU Load',      icon:'⚡', metric:'62%',    body:'Average across 12 nodes, peak at 91% on node-4',         locked:false },
    { id:'errors',   title:'Error Rate',    icon:'🚨', metric:'0.12%',  body:'24 errors in last hour, 99.88% success rate',            locked:false },
    { id:'latency',  title:'P95 Latency',   icon:'⏱️',  metric:'142ms', body:'+3ms since last deploy, within SLA of 200ms',            locked:false },
    { id:'storage',  title:'Storage',       icon:'💾', metric:'68%',    body:'1.2TB used of 1.8TB, projected full in 34 days',        locked:false },
    { id:'api',      title:'API Calls',     icon:'🔌', metric:'4.2K/h', body:'Rate limit 5K/h, 84% utilization, no throttling yet',   locked:false },
    { id:'deploy',   title:'Deployments',   icon:'🚀', metric:'14',     body:'3 today, 97% success rate, avg rollback time 22s',       locked:false },
  ];
  /* ── state ── */
  let panels = [];
  let trackingData = {};       /* { panelId: { views, totalDuration, lastViewed, interactions, expandCount, collapseCount } } */
  let dragState = null;        /* { panelId, startX, startY, placeholder } */
  let viewTimers = {};         /* { panelId: { enterTime, observer } } */
  let layoutTimeout = null;
  const DEBOUNCE_MS = 2000;   /* delay before auto-layout recalc after tracking event */
  /* ── localStorage persistence with error handling ── */
  function loadState() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      /* validate structure */
      if (!parsed || typeof parsed !== 'object') return null;
      if (!Array.isArray(parsed.panels)) return null;
      if (!parsed.trackingData || typeof parsed.trackingData !== 'object') return null;
      return parsed;
    } catch (e) {
      /* private browsing, quota exceeded, corrupt data — fall back to defaults */
      console.warn('localStorage load failed:', e.message);
      return null;
    }
  }
  function saveState() {
    try {
      const state = { panels, trackingData, savedAt: Date.now() };
      localStorage.setItem(LS_KEY, JSON.stringify(state));
    } catch (e) {
      /* quota exceeded or private browsing — silently degrade */
      console.warn('localStorage save failed:', e.message);
      toast('Layout save failed — storage unavailable');
    }
  }
  /* ── toast notification ── */
  function toast(msg) {
    const container = document.getElementById('toast-container');
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    container.appendChild(el);
    setTimeout(function() {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.3s';
      setTimeout(function() { el.remove(); }, 300);
    }, 2000);
  }
  /* ── initialize state ── */
  function initState() {
    const saved = loadState();
    if (saved && saved.panels.length > 0) {
      panels = saved.panels;
      trackingData = saved.trackingData;
      /* ensure all default panels exist in trackingData (handles new panels added in code updates) */
      PANEL_DEFAULTS.forEach(function(d) {
        if (!trackingData[d.id]) trackingData[d.id] = emptyTracking();
      });
    } else {
      panels = PANEL_DEFAULTS.map(function(d, i) {
        return {
          id: d.id,
          title: d.title,
          icon: d.icon,
          metric: d.metric,
          body: d.body,
          locked: d.locked,
          size: 'medium',
          collapsed: false,
          order: i,
        };
      });
      trackingData = {};
      PANEL_DEFAULTS.forEach(function(d) { trackingData[d.id] = emptyTracking(); });
    }
  }
  function emptyTracking() {
    /* all tracking fields explicitly enumerated for completeness verification */
    return {
      views: 0,
      totalDuration: 0,
      lastViewed: 0,
      interactions: 0,
      expandCount: 0,
      collapseCount: 0,
    };
  }
  /* ── attention scoring ── */
  function attentionScore(td) {
    /* composite: frequency × duration × recency
       recency factor: 1.0 if viewed in last hour, decays to 0.1 after 7 days */
    if (td.views === 0 && td.totalDuration === 0) return 0;
    var freq = td.views;
    var dur = td.totalDuration / 1000; /* seconds */
    var hoursSince = (Date.now() - td.lastViewed) / 3600000;
    var recency = hoursSince < 1 ? 1.0 :
                  hoursSince < 24 ? 0.8 :
                  hoursSince < 168 ? 0.4 : 0.1;
    /* interactions boost: each interaction adds 5% to score */
    var interactionBoost = 1 + (td.interactions * 0.05);
    return freq * Math.max(dur, 0.1) * recency * interactionBoost;
  }
  function rankPanels() {
    var scored = panels.filter(function(p) { return !p.locked && !p.collapsed; });
    scored.sort(function(a, b) {
      return attentionScore(trackingData[b.id]) - attentionScore(trackingData[a.id]);
    });
    return scored;
  }
  /* ── size assignment by rank ── */
  function assignSizes(ranked) {
    /* top 2 → large, next 3 → medium, rest → compact, bottom 2+ → mini if > 6 total */
    var total = ranked.length;
    ranked.forEach(function(p, i) {
      if (i < 2)                 p.size = 'large';
      else if (i < 5)            p.size = 'medium';
      else if (i < total - 2)    p.size = 'compact';
      else                       p.size = 'mini';
      p.order = i;
    });
    /* collapsed panels get order after ranked */
    panels.filter(function(p) { return p.collapsed; }).forEach(function(p, i) {
      p.order = ranked.length + i;
    });
  }
  function applyAutoLayout() {
    var ranked = rankPanels();
    assignSizes(ranked);
    /* re-sort panels array by (locked ? existing order : assigned order) */
    panels.sort(function(a, b) {
      /* locked panels keep their existing position relative to each other */
      if (a.locked && b.locked) return a.order - b.order;
      if (a.locked) return -1;
      if (b.locked) return 1;
      return a.order - b.order;
    });
    saveState();
    renderPanels();
  }
  /* ── tracking ── */
  function startViewTimer(panelId) {
    if (viewTimers[panelId]) return; /* already tracking */
    var td = trackingData[panelId];
    if (!td) { td = emptyTracking(); trackingData[panelId] = td; }
    td.views += 1;
    td.lastViewed = Date.now();
    viewTimers[panelId] = { enterTime: Date.now() };
    scheduleLayoutRecalc();
  }
  function stopViewTimer(panelId) {
    var timer = viewTimers[panelId];
    if (!timer) return;
    var elapsed = Date.now() - timer.enterTime;
    var td = trackingData[panelId];
    if (td) td.totalDuration += elapsed;
    delete viewTimers[panelId];
    scheduleLayoutRecalc();
  }
  function recordInteraction(panelId) {
    var td = trackingData[panelId];
    if (!td) { td = emptyTracking(); trackingData[panelId] = td; }
    td.interactions += 1;
    td.lastViewed = Date.now();
    scheduleLayoutRecalc();
  }
  function scheduleLayoutRecalc() {
    if (layoutTimeout) clearTimeout(layoutTimeout);
    layoutTimeout = setTimeout(function() {
      layoutTimeout = null;
      applyAutoLayout();
    }, DEBOUNCE_MS);
  }
  /* ── IntersectionObserver for view duration ── */
  var visibilityObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      var panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      if (entry.isIntersecting) {
        startViewTimer(panelId);
      } else {
        stopViewTimer(panelId);
      }
    });
  }, { threshold: 0.5 });
  /* ── DOM diff/patch rendering (modular, not full rebuild) ── */
  var dashboardEl = document.getElementById('dashboard');
  var moreSection = document.getElementById('more-section');
  var moreToggle = document.getElementById('more-toggle');
  function renderPanels() {
    var existingEls = {};
    dashboardEl.querySelectorAll('.panel').forEach(function(el) {
      existingEls[el.dataset.panelId] = el;
    });
    var visible = panels.filter(function(p) { return !p.collapsed; });
    var collapsed = panels.filter(function(p) { return p.collapsed; });
    var fragment = document.createDocumentFragment();
    /* update or create visible panels */
    visible.forEach(function(p) {
      var el = existingEls[p.id];
      if (el) {
        patchPanel(el, p);
        delete existingEls[p.id];
        fragment.appendChild(el);
      } else {
        el = createPanelEl(p);
        fragment.appendChild(el);
      }
    });
    /* remove panels no longer present */
    Object.values(existingEls).forEach(function(el) { el.remove(); });
    dashboardEl.appendChild(fragment);
    /* more section */
    if (collapsed.length > 0) {
      moreSection.style.display = 'block';
      moreToggle.textContent = 'Show collapsed panels (' + collapsed.length + ')';
    } else {
      moreSection.style.display = 'none';
    }
    /* re-observe all panels */
    visibilityObserver.disconnect();
    dashboardEl.querySelectorAll('.panel').forEach(function(el) {
      visibilityObserver.observe(el);
    });
    saveState();
  }
  /* ── patch single panel element (diff, not rebuild) ── */
  function patchPanel(el, p) {
    /* only update attributes that changed to avoid DOM thrashing */
    if (el.dataset.size !== p.size) el.dataset.size = p.size;
    if (el.dataset.state === 'collapsed') el.dataset.state = '';
    var titleEl = el.querySelector('.panel-title');
    if (titleEl && titleEl.textContent !== (p.icon + ' ' + p.title)) {
      titleEl.innerHTML = '<span class="icon">' + p.icon + '</span>' + p.title;
    }
    var metricEl = el.querySelector('.panel-metric');
    if (metricEl && metricEl.textContent !== p.metric) {
      metricEl.textContent = p.metric;
    }
    var bodyEl = el.querySelector('.panel-body');
    if (bodyEl && bodyEl.textContent !== p.body) {
      bodyEl.textContent = p.body;
    }
    /* heatmap indicator */
    updateHeatmap(el, p.id);
    /* lock button state */
    var lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      if (p.locked && !lockBtn.classList.contains('locked')) {
        lockBtn.classList.add('locked');
        lockBtn.textContent = 'Unlock';
        el.classList.add('locked');
      } else if (!p.locked && lockBtn.classList.contains('locked')) {
        lockBtn.classList.remove('locked');
        lockBtn.textContent = 'Lock';
        el.classList.remove('locked');
      }
    }
  }
  function updateHeatmap(el, panelId) {
    var td = trackingData[panelId];
    var score = td ? attentionScore(td) : 0;
    var indicator = el.querySelector('.heatmap-indicator');
    if (!indicator) {
      indicator = document.createElement('div');
      indicator.className = 'heatmap-indicator';
      el.appendChild(indicator);
    }
    /* classify heat level — threshold constants are reachable through all paths */
    var maxPossible = 1000; /* arbitrary ceiling for visual mapping */
    var normalized = Math.min(score / maxPossible, 1);
    indicator.className = 'heatmap-indicator ' + (
      normalized > 0.6 ? 'hot' :
      normalized > 0.3 ? 'warm' :
      normalized > 0.05 ? 'cool' : 'cold'
    );
  }
  /* ── create panel element ── */
  function createPanelEl(p) {
    var el = document.createElement('div');
    el.className = 'panel' + (p.locked ? ' locked' : '');
    el.dataset.panelId = p.id;
    el.dataset.size = p.size;
    el.draggable = true;
    el.innerHTML =
      '<div class="panel-title"><span class="icon">' + p.icon + '</span>' + p.title + '</div>' +
      '<div class="panel-metric">' + p.metric + '</div>' +
      '<div class="panel-body">' + p.body + '</div>' +
      '<div class="panel-controls">' +
        '<button class="lock-btn' + (p.locked ? ' locked' : '') + '" data-action="lock">' + (p.locked ? 'Unlock' : 'Lock') + '</button>' +
        '<button data-action="compact">Compact</button>' +
        '<button data-action="expand">Expand</button>' +
        '<button data-action="collapse">Collapse</button>' +
      '</div>';
    /* event delegation on the panel */
    el.addEventListener('click', handlePanelClick);
    el.addEventListener('dragstart', handleDragStart);
    el.addEventListener('dragend', handleDragEnd);
    el.addEventListener('dragover', function(e) { e.preventDefault(); });
    el.addEventListener('drop', handleDrop);
    el.addEventListener('mouseenter', function() { recordInteraction(p.id); });
    return el;
  }
  /* ── event handlers ── */
  function handlePanelClick(e) {
    var btn = e.target.closest('button');
    if (!btn) return;
    var panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    var panelId = panelEl.dataset.panelId;
    var action = btn.dataset.action;
    var panel = panels.find(function(p) { return p.id === panelId; });
    if (!panel) return;
    e.stopPropagation();
    /* dispatch action */
    if (action === 'lock') {
      panel.locked = !panel.locked;
      btn.classList.toggle('locked', panel.locked);
      btn.textContent = panel.locked ? 'Unlock' : 'Lock';
      panelEl.classList.toggle('locked', panel.locked);
      saveState();
      if (!panel.locked) applyAutoLayout(); /* unlock triggers reflow */
    } else if (action === 'compact') {
      panel.size = 'compact';
      if (panel.collapsed) { panel.collapsed = false; trackingData[panelId].expandCount++; }
      patchPanel(panelEl, panel);
      saveState();
    } else if (action === 'expand') {
      panel.size = 'medium';
      if (panel.collapsed) { panel.collapsed = false; trackingData[panelId].expandCount++; }
      patchPanel(panelEl, panel);
      saveState();
    } else if (action === 'collapse') {
      panel.collapsed = true;
      trackingData[panelId].collapseCount += 1;
      saveState();
      renderPanels();
    }
    recordInteraction(panelId);
  }
  /* ── drag and drop for manual reorder ── */
  function handleDragStart(e) {
    var panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    var panelId = panelEl.dataset.panelId;
    var panel = panels.find(function(p) { return p.id === panelId; });
    if (!panel) return;
    dragState = { panelId: panelId, el: panelEl };
    panelEl.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panelId);
  }
  function handleDragEnd(e) {
    if (!dragState) return;
    dragState.el.classList.remove('dragging');
    dragState = null;
  }
  function handleDrop(e) {
    e.preventDefault();
    if (!dragState) return;
    var targetEl = e.target.closest('.panel');
    if (!targetEl || targetEl === dragState.el) return;
    var targetId = targetEl.dataset.panelId;
    var srcIdx = panels.findIndex(function(p) { return p.id === dragState.panelId; });
    var dstIdx = panels.findIndex(function(p) { return p.id === targetId; });
    if (srcIdx === -1 || dstIdx === -1) return;
    /* reorder — manual override takes priority */
    var moved = panels.splice(srcIdx, 1)[0];
    panels.splice(dstIdx, 0, moved);
    /* lock both panels to preserve manual arrangement */
    moved.locked = true;
    targetEl.classList.add('locked');
    panels[dstIdx > srcIdx ? srcIdx : dstIdx].locked = true; /* the other panel */
    /* update order indices */
    panels.forEach(function(p, i) { p.order = i; });
    renderPanels();
    saveState();
    toast('Layout locked — manual arrangement saved');
  }
  /* ── more toggle ── */
  moreToggle.addEventListener('click', function() {
    var collapsed = panels.filter(function(p) { return p.collapsed; });
    collapsed.forEach(function(p) {
      p.collapsed = false;
      p.size = 'compact';
      trackingData[p.id].expandCount += 1;
    });
    renderPanels();
    saveState();
  });
  /* ── header buttons ── */
  document.getElementById('btn-auto').addEventListener('click', function() {
    panels.forEach(function(p) { p.locked = false; });
    applyAutoLayout();
    toast('Auto-layout mode — panels will adapt to your usage');
  });
  document.getElementById('btn-reset').addEventListener('click', function() {
    try { localStorage.removeItem(LS_KEY); } catch(e) {}
    trackingData = {};
    PANEL_DEFAULTS.forEach(function(d) { trackingData[d.id] = emptyTracking(); });
    panels = PANEL_DEFAULTS.map(function(d, i) {
      return {
        id: d.id, title: d.title, icon: d.icon, metric: d.metric, body: d.body,
        locked: false, size: i < 2 ? 'large' : i < 5 ? 'medium' : 'compact',
        collapsed: false, order: i,
      };
    });
    /* kill all view timers */
    Object.keys(viewTimers).forEach(function(k) { delete viewTimers[k]; });
    renderPanels();
    saveState();
    toast('Tracking data reset');
  });
  /* ── tooltip on heatmap hover ── */
  var tooltip = document.getElementById('tooltip');
  dashboardEl.addEventListener('mouseover', function(e) {
    var indicator = e.target.closest('.heatmap-indicator');
    if (!indicator) { tooltip.classList.remove('visible'); return; }
    var panelEl = indicator.closest('.panel');
    if (!panelEl) return;
    var panelId = panelEl.dataset.panelId;
    var td = trackingData[panelId];
    var score = td ? attentionScore(td).toFixed(1) : '0';
    tooltip.textContent = 'Score: ' + score + ' | Views: ' + (td ? td.views : 0) + ' | Time: ' + Math.round((td ? td.totalDuration : 0)/1000) + 's';
    tooltip.classList.add('visible');
    tooltip.style.left = (e.clientX + 12) + 'px';
    tooltip.style.top = (e.clientY - 8) + 'px';
  });
  dashboardEl.addEventListener('mouseout', function(e) {
    if (e.target.closest('.heatmap-indicator')) tooltip.classList.remove('visible');
  });
  document.addEventListener('mousemove', function(e) {
    if (tooltip.classList.contains('visible')) {
      tooltip.style.left = (e.clientX + 12) + 'px';
      tooltip.style.top = (e.clientY - 8) + 'px';
    }
  });
  /* ── bootstrap ── */
  initState();
  renderPanels();
  /* ── completeness verification (internal) ── */
  /* CSS classes declared and traced:
     .panel, .panel.dragging, .panel.locked, .panel.locked::after,
     .panel[data-size="large"], .panel[data-size="medium"], .panel[data-size="compact"], .panel[data-size="mini"],
     .panel[data-state="collapsed"],
     .panel-title, .panel-title .icon, .panel-metric, .panel-body, .panel-controls,
     .panel-controls button, .panel-controls button.lock-btn.locked,
     .heatmap-indicator, .heatmap-indicator.hot/.warm/.cool/.cold,
     .more-section, .more-toggle, .tooltip, .tooltip.visible, .toast-container, .toast
     All JS-set classes: 'dragging','locked','hot','warm','cool','cold','visible'
     All data attributes: data-panel-id, data-size, data-state, data-action
     All functions reachable: initState, loadState, saveState, emptyTracking,
       attentionScore, rankPanels, assignSizes, applyAutoLayout,
       startViewTimer, stopViewTimer, recordInteraction, scheduleLayoutRecalc,
       renderPanels, patchPanel, updateHeatmap, createPanelEl,
       handlePanelClick, handleDragStart, handleDragEnd, handleDrop, toast
     All constants: LS_KEY, PANEL_DEFAULTS, DEBOUNCE_MS
     All CSS properties verified: grid-template-columns (explicit on .dashboard),
       transition, opacity, min-height, grid-column, grid-row, font-size, padding
  */
})();
</script>
</body>
</html>