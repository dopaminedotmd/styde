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
  --surface2: #222636;
  --border: #2a3040;
  --text: #c9d1d9;
  --text2: #8b949e;
  --accent: #58a6ff;
  --accent2: #3fb950;
  --warn: #d2991d;
  --compact-scale: 0.45;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
  line-height: 1.4;
}
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; border-bottom: 1px solid var(--border);
  background: var(--surface); position: sticky; top: 0; z-index: 100;
}
.header h1 { font-size: 16px; font-weight: 600; letter-spacing: 0.3px; }
.header-actions { display: flex; gap: 8px; align-items: center; }
.btn {
  padding: 6px 14px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--surface2); color: var(--text); cursor: pointer;
  font-size: 12px; font-weight: 500; transition: background 0.15s;
}
.btn:hover { background: var(--border); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.dashboard {
  display: grid; gap: 10px; padding: 14px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  transition: grid-template-columns 0.3s ease;
}
.dashboard.dense {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease, opacity 0.25s ease;
  position: relative; display: flex; flex-direction: column;
  will-change: transform; contain: layout style;
}
.panel:hover { box-shadow: 0 4px 24px rgba(0,0,0,0.35); }
.panel.tier-dominant { grid-column: span 2; grid-row: span 2; }
.panel.tier-standard { grid-column: span 1; grid-row: span 1; }
.panel.tier-compact {
  grid-column: span 1; grid-row: span 1;
  transform: scale(var(--compact-scale));
  transform-origin: top left;
  opacity: 0.7;
  margin-bottom: calc(-1 * var(--panel-h) * (1 - var(--compact-scale)));
}
.panel.tier-collapsed {
  grid-column: span 1; grid-row: span 1;
  max-height: 40px; overflow: hidden;
}
.panel.tier-collapsed .panel-body { display: none; }
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.panel.dragging { opacity: 0.6; z-index: 200; cursor: grabbing; }
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; cursor: grab; user-select: none;
  border-bottom: 1px solid var(--border); background: var(--surface2);
  font-size: 13px; font-weight: 600; gap: 8px;
}
.panel-header:active { cursor: grabbing; }
.panel-title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.panel-rank {
  font-size: 10px; color: var(--text2); background: var(--bg);
  padding: 2px 8px; border-radius: 10px; white-space: nowrap;
}
.panel-score {
  font-size: 10px; color: var(--accent2); white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.panel-actions { display: flex; gap: 4px; }
.panel-btn {
  width: 26px; height: 26px; border: none; background: transparent;
  color: var(--text2); cursor: pointer; border-radius: 4px;
  font-size: 14px; display: flex; align-items: center; justify-content: center;
  transition: color 0.15s, background 0.15s;
}
.panel-btn:hover { color: var(--text); background: var(--border); }
.panel-btn.lock-btn.locked { color: var(--accent); }
.panel-body {
  padding: 14px; flex: 1; display: flex; flex-direction: column; gap: 10px;
  min-height: 100px; overflow: auto;
}
.panel-body.compact-preview { padding: 8px; gap: 6px; font-size: 10px; }
.metric-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12px; padding: 4px 0; border-bottom: 1px solid var(--border);
}
.metric-row:last-child { border-bottom: none; }
.metric-value {
  font-weight: 600; font-variant-numeric: tabular-nums;
  font-size: 13px;
}
.metric-label { color: var(--text2); }
.spark { height: 40px; background: var(--surface2); border-radius: 6px; overflow: hidden; }
.spark svg { width: 100%; height: 100%; }
.stats-bar {
  display: flex; gap: 6px; font-size: 10px; color: var(--text2);
  padding-top: 4px; border-top: 1px solid var(--border);
}
.more-section {
  grid-column: 1 / -1; border: 1px dashed var(--border);
  border-radius: 10px; padding: 12px 20px; cursor: pointer;
  color: var(--text2); font-size: 13px; text-align: center;
  transition: background 0.15s; background: var(--surface);
}
.more-section:hover { background: var(--surface2); }
.tooltip {
  position: fixed; background: var(--surface2); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 12px; font-size: 11px; z-index: 300;
  pointer-events: none; opacity: 0; transition: opacity 0.2s;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.tooltip.visible { opacity: 1; }
.reset-banner {
  position: fixed; bottom: 20px; right: 20px; background: var(--surface2);
  border: 1px solid var(--border); border-radius: 10px; padding: 12px 18px;
  font-size: 13px; z-index: 200; box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  display: flex; gap: 10px; align-items: center;
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout</h1>
  <div class="header-actions">
    <span style="font-size:11px;color:var(--text2)" id="panel-count">12 panels</span>
    <button class="btn" id="btn-dense" title="Toggle compact grid">Dense Grid</button>
    <button class="btn" id="btn-reset" title="Reset all tracking data">Reset</button>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_metric_layout';
  const DEBOUNCE_STORAGE_MS = 2000;
  const INTERSECTION_THRESHOLD = 0.3;
  const RECENCY_DECAY_DAYS = 7;
  const COMPACT_THRESHOLD_PCT = 25;
  const COLLAPSE_THRESHOLD_PCT = 10;
  const THROTTLE_SCROLL_MS = 50;
  const THROTTLE_RESIZE_MS = 100;
  const TIER_DOMINANT_MIN = 70;
  const CLEANUP = new Set();
  function registerCleanup(fn) {
    CLEANUP.add(fn);
    return function() {
      fn();
      CLEANUP.delete(fn);
    };
  }
  function cleanupAll() {
    for (const fn of CLEANUP) {
      try { fn(); } catch(e) { /* swallow */ }
    }
    CLEANUP.clear();
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function now() { return Date.now(); }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch(e) { return null; }
  }
  let storageTimer = null;
  function saveState(state) {
    if (storageTimer) clearTimeout(storageTimer);
    storageTimer = setTimeout(function() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch(e) { /* quota exceeded, silently fail */ }
      storageTimer = null;
    }, DEBOUNCE_STORAGE_MS);
  }
  function defaultPanels() {
    const types = [
      { id: 'cpu', title: 'CPU Usage', unit: '%', base: 45 },
      { id: 'memory', title: 'Memory', unit: 'GB', base: 12.4 },
      { id: 'requests', title: 'Requests/sec', unit: '', base: 2840 },
      { id: 'latency', title: 'P95 Latency', unit: 'ms', base: 142 },
      { id: 'errors', title: 'Error Rate', unit: '%', base: 0.8 },
      { id: 'revenue', title: 'Revenue', unit: ' USD', base: 12500 },
      { id: 'users', title: 'Active Users', unit: '', base: 1420 },
      { id: 'storage', title: 'Storage IOPS', unit: '', base: 8400 },
      { id: 'bandwidth', title: 'Bandwidth', unit: 'Mbps', base: 940 },
      { id: 'uptime', title: 'Uptime', unit: '%', base: 99.97 },
      { id: 'threads', title: 'Thread Pool', unit: '', base: 64 },
      { id: 'cache', title: 'Cache Hit Rate', unit: '%', base: 94.2 },
    ];
    return types.map(function(t, i) {
      return {
        id: t.id,
        title: t.title,
        unit: t.unit,
        baseValue: t.base,
        currentValue: t.base + (Math.random() - 0.5) * t.base * 0.2,
        viewDurationMs: 0,
        interactionCount: 0,
        lastInteraction: 0,
        expandCount: 0,
        collapseCount: 0,
        locked: false,
        manualPosition: null,
        tier: 'standard',
        engagementScore: 0,
      };
    });
  }
  function loadOrInit() {
    let saved = loadState();
    if (saved && Array.isArray(saved.panels) && saved.panels.length > 0) {
      saved.panels.forEach(function(p) {
        p.viewDurationMs = p.viewDurationMs || 0;
        p.interactionCount = p.interactionCount || 0;
        p.lastInteraction = p.lastInteraction || 0;
        p.expandCount = p.expandCount || 0;
        p.collapseCount = p.collapseCount || 0;
        p.locked = !!p.locked;
        p.manualPosition = p.manualPosition || null;
        p.engagementScore = p.engagementScore || 0;
        p.tier = p.tier || 'standard';
      });
      return saved.panels;
    }
    return defaultPanels();
  }
  let panels = loadOrInit();
  let viewStartTimes = {};
  let dirtyPanels = new Set();
  let rafId = null;
  let domNodes = {};
  let observer = null;
  let denseMode = false;
  function computeEngagementScore(p) {
    var hoursSinceLast = p.lastInteraction
      ? (now() - p.lastInteraction) / (1000 * 60 * 60)
      : Infinity;
    var decayDays = RECENCY_DECAY_DAYS;
    var recencyFactor = Math.exp(-hoursSinceLast / (decayDays * 24));
    var frequencyScore = Math.log2(p.interactionCount + 2);
    var durationScore = Math.sqrt(p.viewDurationMs / 1000 + 1);
    var expandBonus = p.expandCount * 2;
    var collapsePenalty = p.collapseCount * -0.5;
    return (frequencyScore * durationScore * recencyFactor) + expandBonus + collapsePenalty;
  }
  function recalculateAllScores() {
    panels.forEach(function(p) {
      p.engagementScore = computeEngagementScore(p);
    });
  }
  function getTier(p, sortedPanels) {
    if (!sortedPanels || sortedPanels.length === 0) return 'standard';
    var maxScore = sortedPanels[0].engagementScore || 1;
    var normalized = maxScore > 0 ? (p.engagementScore / maxScore) * 100 : 0;
    if (normalized >= TIER_DOMINANT_MIN) return 'dominant';
    if (normalized >= COMPACT_THRESHOLD_PCT) return 'standard';
    if (normalized >= COLLAPSE_THRESHOLD_PCT) return 'compact';
    return 'collapsed';
  }
  function rankPanels() {
    recalculateAllScores();
    var sorted = panels.slice().sort(function(a, b) {
      return (b.engagementScore || 0) - (a.engagementScore || 0);
    });
    sorted.forEach(function(p) {
      p.tier = getTier(p, sorted);
    });
    return sorted;
  }
  function getOrderedPanels() {
    var sorted = rankPanels();
    var lockedPanels = sorted.filter(function(p) { return p.locked; });
    var unlockedPanels = sorted.filter(function(p) { return !p.locked; });
    var ordered = [];
    lockedPanels.forEach(function(p, i) {
      if (p.manualPosition != null && p.manualPosition < ordered.length) {
        ordered.splice(p.manualPosition, 0, p);
      } else {
        ordered.push(p);
      }
    });
    unlockedPanels.forEach(function(p) {
      if (p.manualPosition != null && !p.locked && p.manualPosition < ordered.length) {
        ordered.splice(p.manualPosition, 0, p);
      } else {
        ordered.push(p);
      }
    });
    return ordered;
  }
  function recordInteraction(panelId, type) {
    var p = panels.find(function(x) { return x.id === panelId; });
    if (!p) return;
    p.interactionCount++;
    p.lastInteraction = now();
    if (type === 'expand') p.expandCount++;
    if (type === 'collapse') p.collapseCount++;
    dirtyPanels.add(panelId);
    scheduleRender();
  }
  function recordViewTime(panelId, ms) {
    var p = panels.find(function(x) { return x.id === panelId; });
    if (!p) return;
    p.viewDurationMs += ms;
  }
  function toggleLock(panelId) {
    var p = panels.find(function(x) { return x.id === panelId; });
    if (!p) return;
    p.locked = !p.locked;
    recordInteraction(panelId, p.locked ? 'lock' : 'unlock');
    scheduleRender();
  }
  function toggleCollapse(panelId) {
    var p = panels.find(function(x) { return x.id === panelId; });
    if (!p) return;
    if (p.tier === 'collapsed') {
      p.tier = 'compact';
      recordInteraction(panelId, 'expand');
    } else {
      p.tier = 'collapsed';
      recordInteraction(panelId, 'collapse');
    }
    scheduleRender();
  }
  function movePanel(panelId, newIndex) {
    var ordered = getOrderedPanels();
    var idx = ordered.findIndex(function(p) { return p.id === panelId; });
    if (idx === -1) return;
    var p = ordered[idx];
    p.manualPosition = clamp(newIndex, 0, ordered.length - 1);
    recordInteraction(panelId, 'move');
    scheduleRender();
  }
  function createSparklineData() {
    var points = 20;
    var data = [];
    var v = 0.5;
    for (var i = 0; i < points; i++) {
      v += (Math.random() - 0.5) * 0.3;
      v = clamp(v, 0.05, 0.95);
      data.push(v);
    }
    return data;
  }
  function sparklineSVG(data) {
    var w = 200, h = 40, pad = 2;
    var pts = data.map(function(v, i) {
      return (i / (data.length - 1)) * (w - pad * 2) + pad + ',' + ((1 - v) * (h - pad * 2) + pad);
    }).join(' ');
    return '<svg viewBox="0 0 ' + w + ' ' + h + '">' +
      '<polyline fill="none" stroke="#58a6ff" stroke-width="1.5" points="' + pts + '"/>' +
      '<polygon fill="rgba(88,166,255,0.1)" points="' + pad + ',' + (h - pad) + ' ' + pts + ' ' + (w - pad) + ',' + (h - pad) + '"/>' +
      '</svg>';
  }
  function panelHTML(p, rank) {
    var sparkData = createSparklineData();
    var tierClass = 'tier-' + p.tier;
    var lockClass = p.locked ? 'locked' : '';
    var compactBody = p.tier === 'compact' ? 'compact-preview' : '';
    var bodyContent = p.tier === 'collapsed' ? '' :
      '<div class="spark">' + sparklineSVG(sparkData) + '</div>' +
      '<div class="metric-row"><span class="metric-label">Current</span><span class="metric-value">' +
        (p.currentValue != null ? (typeof p.currentValue === 'number' ? p.currentValue.toFixed(1) : p.currentValue) : '--') +
        (p.unit || '') + '</span></div>' +
      '<div class="metric-row"><span class="metric-label">Baseline</span><span class="metric-value">' +
        (p.baseValue != null ? (typeof p.baseValue === 'number' ? p.baseValue.toFixed(1) : p.baseValue) : '--') +
        (p.unit || '') + '</span></div>' +
      '<div class="stats-bar">' +
        '<span>Views: ' + Math.round(p.viewDurationMs / 1000) + 's</span>' +
        '<span>Interact: ' + p.interactionCount + '</span>' +
        '<span>Score: ' + (p.engagementScore || 0).toFixed(1) + '</span>' +
      '</div>';
    return '<div class="panel ' + tierClass + ' ' + lockClass + '" data-panel-id="' + p.id + '" data-rank="' + rank + '" draggable="true">' +
      '<div class="panel-header">' +
        '<span class="panel-title">' + p.title + '</span>' +
        '<span class="panel-rank">#' + (rank + 1) + '</span>' +
        '<span class="panel-score">' + (p.engagementScore || 0).toFixed(1) + '</span>' +
        '<div class="panel-actions">' +
          '<button class="panel-btn collapse-btn" data-action="collapse" title="Toggle collapse">' + (p.tier === 'collapsed' ? '⊞' : '⊟') + '</button>' +
          '<button class="panel-btn lock-btn ' + lockClass + '" data-action="lock" title="Lock position">' + (p.locked ? '🔒' : '🔓') + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body ' + compactBody + '">' + bodyContent + '</div>' +
    '</div>';
  }
  function moreSectionHTML(collapsedPanels) {
    if (collapsedPanels.length === 0) return '';
    return '<div class="more-section" id="more-section">+ ' + collapsedPanels.length + ' collapsed panels — click to expand all</div>';
  }
  function reconcileDOM(ordered) {
    var container = document.getElementById('dashboard');
    if (!container) return;
    var newIds = new Set(ordered.map(function(p) { return p.id; }));
    var existingNodes = {};
    var children = Array.from(container.children);
    children.forEach(function(child) {
      var id = child.getAttribute && child.getAttribute('data-panel-id');
      if (id && !newIds.has(id)) {
        child.remove();
      } else if (id) {
        existingNodes[id] = child;
      } else if (child.id === 'more-section') {
        existingNodes['__more__'] = child;
      }
    });
    var fragment = document.createDocumentFragment();
    var currentInDOM = Array.from(container.children).filter(function(c) {
      return c.getAttribute && c.getAttribute('data-panel-id');
    }).map(function(c) { return c.getAttribute('data-panel-id'); });
    var needReorder = false;
    var orderedIds = ordered.map(function(p) { return p.id; });
    if (currentInDOM.length !== orderedIds.length) {
      needReorder = true;
    } else {
      for (var i = 0; i < currentInDOM.length; i++) {
        if (currentInDOM[i] !== orderedIds[i]) { needReorder = true; break; }
      }
    }
    if (needReorder) {
      ordered.forEach(function(p, rank) {
        var existing = existingNodes[p.id];
        if (existing) {
          var rankAttr = parseInt(existing.getAttribute('data-rank'), 10);
          if (rankAttr !== rank) existing.setAttribute('data-rank', String(rank));
          fragment.appendChild(existing);
        } else {
          var div = document.createElement('div');
          div.innerHTML = panelHTML(p, rank);
          fragment.appendChild(div.firstElementChild);
        }
      });
      var moreEl = existingNodes['__more__'];
      if (moreEl) fragment.appendChild(moreEl);
      container.innerHTML = '';
      container.appendChild(fragment);
    } else {
      ordered.forEach(function(p) {
        var existing = existingNodes[p.id];
        if (existing) {
          var currentTier = Array.from(existing.classList).find(function(c) { return c.startsWith('tier-'); });
          var desiredTier = 'tier-' + p.tier;
          if (currentTier !== desiredTier) {
            existing.classList.remove(currentTier);
            existing.classList.add(desiredTier);
          }
          if (p.locked && !existing.classList.contains('locked')) {
            existing.classList.add('locked');
          } else if (!p.locked && existing.classList.contains('locked')) {
            existing.classList.remove('locked');
          }
          var lockBtn = existing.querySelector('.lock-btn');
          if (lockBtn) {
            lockBtn.className = 'panel-btn lock-btn' + (p.locked ? ' locked' : '');
            lockBtn.textContent = p.locked ? '🔒' : '🔓';
          }
          var collapseBtn = existing.querySelector('.collapse-btn');
          if (collapseBtn) {
            collapseBtn.textContent = p.tier === 'collapsed' ? '⊞' : '⊟';
          }
          var bodyEl = existing.querySelector('.panel-body');
          if (bodyEl) {
            if (p.tier === 'collapsed') {
              bodyEl.style.display = 'none';
            } else {
              bodyEl.style.display = '';
              bodyEl.className = 'panel-body' + (p.tier === 'compact' ? ' compact-preview' : '');
            }
          }
          var scoreEl = existing.querySelector('.panel-score');
          if (scoreEl) scoreEl.textContent = (p.engagementScore || 0).toFixed(1);
          var rankEl = existing.querySelector('.panel-rank');
          if (rankEl) rankEl.textContent = '#' + (rank + 1);
        }
      });
    }
  }
  function render() {
    rafId = null;
    var ordered = getOrderedPanels();
    reconcileDOM(ordered);
    rebindObservers(ordered);
    saveState({ panels: panels });
  }
  function scheduleRender() {
    if (rafId) return;
    rafId = requestAnimationFrame(render);
  }
  function rebindObservers(orderedPanels) {
    if (observer) {
      observer.disconnect();
      CLEANUP.delete(disconnectObserver);
    }
    var panelElements = document.querySelectorAll('.panel[data-panel-id]');
    observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var panelId = entry.target.getAttribute('data-panel-id');
        if (entry.isIntersecting) {
          viewStartTimes[panelId] = now();
        } else if (viewStartTimes[panelId]) {
          var duration = now() - viewStartTimes[panelId];
          recordViewTime(panelId, duration);
          delete viewStartTimes[panelId];
        }
      });
    }, { threshold: INTERSECTION_THRESHOLD });
    panelElements.forEach(function(el) { observer.observe(el); });
    var disconnectObserver = function() {
      if (observer) { observer.disconnect(); observer = null; }
    };
    registerCleanup(disconnectObserver);
  }
  function setupEventDelegation() {
    var dashboard = document.getElementById('dashboard');
    if (!dashboard) return;
    var clickHandler = function(e) {
      var target = e.target;
      var action = target.getAttribute && target.getAttribute('data-action');
      var panelEl = target.closest && target.closest('.panel');
      if (!panelEl || !action) return;
      var panelId = panelEl.getAttribute('data-panel-id');
      if (!panelId) return;
      e.stopPropagation();
      if (action === 'lock') toggleLock(panelId);
      if (action === 'collapse') toggleCollapse(panelId);
    };
    dashboard.addEventListener('click', clickHandler);
    var hoverHandler = function(e) {
      var panelEl = e.target.closest && e.target.closest('.panel');
      var tooltip = document.getElementById('tooltip');
      if (!tooltip) return;
      if (panelEl) {
        var panelId = panelEl.getAttribute('data-panel-id');
        var p = panels.find(function(x) { return x.id === panelId; });
        if (p) {
          tooltip.textContent = p.title + ' | Score: ' + (p.engagementScore || 0).toFixed(1) + ' | Views: ' + Math.round(p.viewDurationMs/1000) + 's | Clicks: ' + p.interactionCount;
          tooltip.classList.add('visible');
          tooltip.style.left = (e.clientX + 12) + 'px';
          tooltip.style.top = (e.clientY + 12) + 'px';
          return;
        }
      }
      tooltip.classList.remove('visible');
    };
    var throttledHover = throttle(hoverHandler, 80);
    document.addEventListener('mousemove', throttledHover);
    var moreClickHandler = function(e) {
      var more = e.target.closest && e.target.closest('#more-section');
      if (!more) return;
      panels.forEach(function(p) {
        if (p.tier === 'collapsed') {
          p.tier = 'compact';
          p.expandCount++;
          p.lastInteraction = now();
        }
      });
      scheduleRender();
    };
    dashboard.addEventListener('click', moreClickHandler);
    var dragStartHandler = function(e) {
      var panelEl = e.target.closest && e.target.closest('.panel');
      if (!panelEl) return;
      var actionTarget = e.target.closest && (e.target.closest('[data-action]') || e.target.closest('.panel-btn'));
      if (actionTarget) return;
      e.dataTransfer.setData('text/plain', panelEl.getAttribute('data-panel-id'));
      e.dataTransfer.effectAllowed = 'move';
      panelEl.classList.add('dragging');
    };
    var dragEndHandler = function(e) {
      var panelEl = e.target.closest && e.target.closest('.panel');
      if (panelEl) panelEl.classList.remove('dragging');
      var allDragging = document.querySelectorAll('.panel.dragging');
      allDragging.forEach(function(el) { el.classList.remove('dragging'); });
    };
    var dropHandler = function(e) {
      e.preventDefault();
      var panelId = e.dataTransfer.getData('text/plain');
      if (!panelId) return;
      var targetPanel = e.target.closest && e.target.closest('.panel');
      if (!targetPanel) return;
      var targetId = targetPanel.getAttribute('data-panel-id');
      if (!targetId || targetId === panelId) return;
      var ordered = getOrderedPanels();
      var targetIdx = ordered.findIndex(function(p) { return p.id === targetId; });
      if (targetIdx === -1) return;
      movePanel(panelId, targetIdx);
    };
    var dragOverHandler = function(e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    };
    dashboard.addEventListener('dragstart', dragStartHandler);
    dashboard.addEventListener('dragend', dragEndHandler);
    dashboard.addEventListener('drop', dropHandler);
    dashboard.addEventListener('dragover', dragOverHandler);
    var removeDragStart = registerCleanup(function() {
      dashboard.removeEventListener('dragstart', dragStartHandler);
    });
    var removeDragEnd = registerCleanup(function() {
      dashboard.removeEventListener('dragend', dragEndHandler);
    });
    var removeDrop = registerCleanup(function() {
      dashboard.removeEventListener('drop', dropHandler);
    });
    var removeDragOver = registerCleanup(function() {
      dashboard.removeEventListener('dragover', dragOverHandler);
    });
    var removeClick = registerCleanup(function() {
      dashboard.removeEventListener('click', clickHandler);
    });
    var removeHover = registerCleanup(function() {
      document.removeEventListener('mousemove', throttledHover);
    });
    var removeMoreClick = registerCleanup(function() {
      dashboard.removeEventListener('click', moreClickHandler);
    });
  }
  function throttle(fn, ms) {
    var last = 0;
    var timer = null;
    return function() {
      var args = arguments;
      var ctx = this;
      var elapsed = now() - last;
      if (elapsed >= ms) {
        last = now();
        fn.apply(ctx, args);
      } else if (!timer) {
        timer = setTimeout(function() {
          last = now();
          timer = null;
          fn.apply(ctx, args);
        }, ms - elapsed);
      }
    };
  }
  function simulateValueUpdates() {
    panels.forEach(function(p) {
      p.currentValue = p.baseValue + (Math.random() - 0.5) * p.baseValue * 0.3;
    });
    scheduleRender();
  }
  function setupHeaderButtons() {
    var btnDense = document.getElementById('btn-dense');
    var btnReset = document.getElementById('btn-reset');
    var dashboard = document.getElementById('dashboard');
    if (btnDense) {
      btnDense.addEventListener('click', function() {
        denseMode = !denseMode;
        if (denseMode) {
          dashboard.classList.add('dense');
          btnDense.classList.add('active');
          btnDense.textContent = 'Dense: ON';
        } else {
          dashboard.classList.remove('dense');
          btnDense.classList.remove('active');
          btnDense.textContent = 'Dense Grid';
        }
      });
    }
    if (btnReset) {
      btnReset.addEventListener('click', function() {
        panels = defaultPanels();
        viewStartTimes = {};
        dirtyPanels.clear();
        localStorage.removeItem(STORAGE_KEY);
        render();
      });
    }
  }
  var valueInterval = setInterval(simulateValueUpdates, 5000);
  registerCleanup(function() { clearInterval(valueInterval); });
  var saveInterval = setInterval(function() {
    saveState({ panels: panels });
  }, 15000);
  registerCleanup(function() { clearInterval(saveInterval); });
  function init() {
    render();
    setupEventDelegation();
    setupHeaderButtons();
    var handleResize = throttle(function() {
      scheduleRender();
    }, THROTTLE_RESIZE_MS);
    window.addEventListener('resize', handleResize);
    registerCleanup(function() {
      window.removeEventListener('resize', handleResize);
    });
    window.addEventListener('beforeunload', function() {
      saveState({ panels: panels });
      cleanupAll();
    });
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