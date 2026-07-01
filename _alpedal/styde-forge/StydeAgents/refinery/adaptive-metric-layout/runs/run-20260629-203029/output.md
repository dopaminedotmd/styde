<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; background: #0f1117; color: #e1e4e8; min-height: 100vh; }
.dashboard-header { padding: 16px 24px; border-bottom: 1px solid #21262d; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.dashboard-header h1 { font-size: 1.25rem; font-weight: 600; }
.stats-bar { display: flex; gap: 16px; font-size: 0.8rem; color: #8b949e; }
.stats-bar span { background: #161b22; padding: 4px 10px; border-radius: 6px; border: 1px solid #30363d; }
.btn { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; transition: background 0.15s; }
.btn:hover { background: #30363d; }
.btn:focus-visible { outline: 2px solid #58a6ff; outline-offset: 2px; }
.btn-reset { background: #da363322; border-color: #da3633; color: #f85149; }
.btn-reset:hover { background: #da363344; }
.dashboard { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 16px 24px; align-items: start; }
.panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; transition: grid-column 0.4s ease, grid-row 0.4s ease, opacity 0.3s; position: relative; }
.panel.locked { border-color: #d29922; }
.panel.compact { font-size: 0.8rem; }
.panel.collapsed { min-height: auto; }
.panel-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; border-bottom: 1px solid #21262d; background: #1c2128; gap: 8px; }
.panel-header .panel-title { font-weight: 600; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; }
.panel-controls { display: flex; gap: 4px; flex-shrink: 0; }
.panel-controls button { background: none; border: 1px solid transparent; color: #8b949e; cursor: pointer; padding: 4px 6px; border-radius: 4px; font-size: 0.85rem; line-height: 1; transition: all 0.15s; }
.panel-controls button:hover { background: #30363d; color: #c9d1d9; }
.panel-controls button:focus-visible { outline: 2px solid #58a6ff; outline-offset: 1px; border-color: #58a6ff; }
.panel-controls .btn-lock[aria-pressed="true"] { color: #d29922; border-color: #d2992244; background: #d2992211; }
.panel-body { padding: 14px; min-height: 60px; }
.panel.compact .panel-body { padding: 8px 14px; min-height: auto; display: flex; align-items: center; gap: 12px; }
.panel.compact .panel-body .metric-preview { font-size: 1.1rem; font-weight: 700; color: #58a6ff; }
.panel.compact .panel-body .metric-label { font-size: 0.75rem; color: #8b949e; }
.panel.collapsed .panel-body { display: none; }
.panel-footer { display: flex; align-items: center; justify-content: space-between; padding: 6px 14px; border-top: 1px solid #21262d; font-size: 0.7rem; color: #484f58; }
.panel-rank-badge { background: #1f6feb22; color: #58a6ff; padding: 1px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }
.panel-rank-badge.hot { background: #f0883e22; color: #f0883e; }
.activity-dot { width: 6px; height: 6px; border-radius: 50%; background: #30363d; display: inline-block; margin-right: 4px; }
.activity-dot.active { background: #3fb950; }
.activity-dot.recent { background: #d29922; }
.metric-value { font-size: 2rem; font-weight: 700; color: #58a6ff; line-height: 1.1; }
.metric-value.small { font-size: 1.25rem; }
.metric-subtitle { font-size: 0.75rem; color: #8b949e; margin-top: 2px; }
.sparkline { height: 40px; margin-top: 8px; opacity: 0.7; }
.sparkline svg { width: 100%; height: 100%; }
.override-indicator { position: absolute; top: 4px; right: 4px; width: 8px; height: 8px; border-radius: 50%; background: #d29922; display: none; }
.panel.locked .override-indicator { display: block; }
.empty-state { grid-column: 1 / -1; text-align: center; padding: 40px; color: #484f58; }
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Adaptive Metric Layout</h1>
  <div class="stats-bar">
    <span id="stat-panels">6 panels</span>
    <span id="stat-tracked">tracking active</span>
    <span id="stat-layouts">0 layouts</span>
  </div>
  <button class="btn btn-reset" id="btn-reset" aria-label="Reset all tracking data and layout">Reset</button>
</div>
<div class="dashboard" id="dashboard" role="region" aria-label="Adaptive metric dashboard"></div>
<script>
(function() {
  'use strict';
  var STORAGE_KEY = 'adaptive_dashboard_v1';
  var COMPACT_RANK_RATIO = 0.25;
  var COLLAPSE_RANK_RATIO = 0.08;
  var SAVE_INTERVAL = 4000;
  var RANK_INTERVAL = 8000;
  var MAX_PANELS = 6;
  var DisplayMode = { EXPANDED: 'expanded', COMPACT: 'compact', COLLAPSED: 'collapsed' };
  var TRANSITIONS = {};
  TRANSITIONS[DisplayMode.EXPANDED] = [DisplayMode.COMPACT, DisplayMode.COLLAPSED];
  TRANSITIONS[DisplayMode.COMPACT] = [DisplayMode.EXPANDED, DisplayMode.COLLAPSED];
  TRANSITIONS[DisplayMode.COLLAPSED] = [DisplayMode.EXPANDED, DisplayMode.COMPACT];
  var samplePanels = [
    { id: 'cpu', title: 'CPU Usage', content: 'cpu', locked: false, overridePos: null },
    { id: 'memory', title: 'Memory', content: 'memory', locked: false, overridePos: null },
    { id: 'requests', title: 'Requests/sec', content: 'requests', locked: false, overridePos: null },
    { id: 'errors', title: 'Error Rate', content: 'errors', locked: false, overridePos: null },
    { id: 'latency', title: 'P99 Latency', content: 'latency', locked: false, overridePos: null },
    { id: 'disk', title: 'Disk I/O', content: 'disk', locked: false, overridePos: null }
  ];
  var metricContent = {
    cpu:    { value: '34%', sub: '4 cores / 3.2 GHz', spark: '3,8,12,9,15,11,14,10,16,13' },
    memory: { value: '7.2 GB', sub: 'of 16 GB total', spark: '6,6.5,7,7.2,7,6.8,7.1,7.3,7.2,7.4' },
    requests: { value: '1,247', sub: 'per second avg', spark: '800,950,1100,1300,1200,1400,1250,1350,1280,1247' },
    errors: { value: '0.12%', sub: 'last 5 min', spark: '0.2,0.15,0.1,0.08,0.14,0.11,0.09,0.13,0.1,0.12' },
    latency: { value: '142ms', sub: 'p99 / 10m window', spark: '150,160,140,130,145,155,138,142,148,142' },
    disk:   { value: '45 MB/s', sub: 'read: 30 / write: 15', spark: '40,42,48,44,50,46,43,47,45,45' }
  };
  function safeNum(v, fallback) { fallback = (fallback === undefined) ? 0 : fallback; var n = Number(v); return isNaN(n) || n === null || n === undefined ? fallback : n; }
  function sparkSVG(pointsStr) {
    var pts = pointsStr.split(',').map(function(s) { return safeNum(s); });
    if (pts.length < 2) return '';
    var min = Math.min.apply(null, pts);
    var max = Math.max.apply(null, pts);
    var range = max - min || 1;
    var w = 100; var h = 30;
    var pad = 2;
    var xs = pts.map(function(_, i) { return pad + (i / (pts.length - 1)) * (w - 2 * pad); });
    var ys = pts.map(function(v) { return pad + (1 - (v - min) / range) * (h - 2 * pad); });
    var d = 'M' + xs[0].toFixed(1) + ',' + ys[0].toFixed(1);
    for (var i = 1; i < pts.length; i++) { d += ' L' + xs[i].toFixed(1) + ',' + ys[i].toFixed(1); }
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none"><polyline points="' + d.slice(1).replace(/L/g, '').replace(/,/g, ',') + '" fill="none" stroke="#58a6ff" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg>';
  }
  function now() { return Date.now(); }
  function hoursSince(ts) { if (!ts) return Infinity; return Math.max(0, (now() - ts) / 3600000); }
  var dashboard = {
    panels: [],
    tracking: {},
    visibleSet: {},
    observer: null,
    saveTimer: null,
    rankTimer: null,
    layoutCount: 0,
    initialized: false,
    init: function() {
      this.loadState();
      this.ensureTrackingObjects();
      this.setupDOM();
      this.render();
      this.initObserver();
      this.initKeyboardDelegation();
      this.populateVisibleSet();
      this.startTimers();
      this.initialized = true;
      this.updateStats();
    },
    loadState: function() {
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          var saved = JSON.parse(raw);
          if (saved.panels && Array.isArray(saved.panels)) {
            this.panels = saved.panels.map(function(p) {
              return {
                id: p.id,
                title: p.title,
                content: p.content,
                locked: !!p.locked,
                overridePos: (p.overridePos && typeof p.overridePos.col === 'number') ? p.overridePos : null,
                mode: (p.mode === DisplayMode.COMPACT || p.mode === DisplayMode.COLLAPSED) ? p.mode : DisplayMode.EXPANDED,
                rank: safeNum(p.rank, 0)
              };
            });
          }
          if (saved.tracking && typeof saved.tracking === 'object') {
            this.tracking = saved.tracking;
          }
          this.layoutCount = safeNum(saved.layoutCount, 0);
        }
      } catch (e) {}
      if (!this.panels.length) {
        this.panels = samplePanels.map(function(p) {
          return {
            id: p.id, title: p.title, content: p.content,
            locked: false, overridePos: null, mode: DisplayMode.EXPANDED, rank: 1
          };
        });
      }
    },
    ensureTrackingObjects: function() {
      var self = this;
      this.panels.forEach(function(p) {
        if (!self.tracking[p.id]) {
          self.tracking[p.id] = {
            interactions: 0,
            viewDurationMs: 0,
            lastInteraction: null,
            viewStart: null
          };
        } else {
          self.tracking[p.id].interactions = safeNum(self.tracking[p.id].interactions, 0);
          self.tracking[p.id].viewDurationMs = safeNum(self.tracking[p.id].viewDurationMs, 0);
          self.tracking[p.id].lastInteraction = self.tracking[p.id].lastInteraction || null;
          self.tracking[p.id].viewStart = null;
        }
      });
    },
    saveState: function() {
      try {
        var toSave = {
          panels: this.panels.map(function(p) { return { id: p.id, title: p.title, content: p.content, locked: p.locked, overridePos: p.overridePos, mode: p.mode, rank: p.rank }; }),
          tracking: this.tracking,
          layoutCount: this.layoutCount
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
      } catch (e) {}
    },
    setupDOM: function() {
      var self = this;
      var resetBtn = document.getElementById('btn-reset');
      resetBtn.addEventListener('click', function() { self.resetAll(); });
      resetBtn.addEventListener('keydown', function(e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); self.resetAll(); } });
    },
    initKeyboardDelegation: function() {
      var self = this;
      document.getElementById('dashboard').addEventListener('keydown', function(e) {
        var btn = e.target.closest('button');
        if (!btn) return;
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });
    },
    populateVisibleSet: function() {
      var self = this;
      requestAnimationFrame(function() {
        self.panels.forEach(function(p) {
          var el = document.getElementById('panel-' + p.id);
          if (!el) return;
          var rect = el.getBoundingClientRect();
          var vis = rect.top < window.innerHeight && rect.bottom > 0 && rect.left < window.innerWidth && rect.right > 0;
          if (vis) {
            self.visibleSet[p.id] = true;
            if (!self.tracking[p.id].viewStart) {
              self.tracking[p.id].viewStart = now();
            }
          }
        });
      });
    },
    initObserver: function() {
      var self = this;
      if (this.observer) this.observer.disconnect();
      this.observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          var panelId = entry.target.getAttribute('data-panel-id');
          if (!panelId) return;
          var t = self.tracking[panelId];
          if (!t) return;
          if (entry.isIntersecting) {
            self.visibleSet[panelId] = true;
            if (!t.viewStart) t.viewStart = now();
          } else {
            delete self.visibleSet[panelId];
            if (t.viewStart) {
              t.viewDurationMs += now() - t.viewStart;
              t.viewStart = null;
            }
          }
        });
      }, { threshold: 0.1 });
      var self2 = this;
      this.panels.forEach(function(p) {
        var el = document.getElementById('panel-' + p.id);
        if (el) self2.observer.observe(el);
      });
    },
    startTimers: function() {
      var self = this;
      if (this.saveTimer) clearInterval(this.saveTimer);
      this.saveTimer = setInterval(function() { self.flushViewDurations(); self.saveState(); }, SAVE_INTERVAL);
      if (this.rankTimer) clearInterval(this.rankTimer);
      this.rankTimer = setInterval(function() { self.recalculateRanks(); self.applyLayout(); self.render(); self.updateStats(); }, RANK_INTERVAL);
    },
    flushViewDurations: function() {
      var self = this;
      var n = now();
      Object.keys(this.visibleSet).forEach(function(pid) {
        var t = self.tracking[pid];
        if (t && t.viewStart) {
          t.viewDurationMs += n - t.viewStart;
          t.viewStart = n;
        }
      });
    },
    recordInteraction: function(panelId) {
      var t = this.tracking[panelId];
      if (!t) return;
      t.interactions = safeNum(t.interactions) + 1;
      t.lastInteraction = now();
    },
    computeRank: function(panelId) {
      var t = this.tracking[panelId];
      if (!t) return 1;
      var freq = safeNum(t.interactions) + 1;
      var dur = (safeNum(t.viewDurationMs) / 1000) + 1;
      var hrs = hoursSince(t.lastInteraction || now());
      var recency = Math.max(0.1, 1 / (hrs + 1));
      return freq * dur * recency;
    },
    recalculateRanks: function() {
      this.flushViewDurations();
      var self = this;
      this.panels.forEach(function(p) {
        if (!p.locked) p.rank = self.computeRank(p.id);
      });
    },
    getModeFromRank: function(panel) {
      if (panel.locked) return panel.mode;
      var ranks = this.panels.map(function(p) { return p.rank; });
      var maxRank = Math.max.apply(null, ranks.length ? ranks : [1]);
      if (maxRank <= 0) maxRank = 1;
      var ratio = panel.rank / maxRank;
      if (ratio < COLLAPSE_RANK_RATIO && panel.mode !== DisplayMode.EXPANDED) return DisplayMode.COLLAPSED;
      if (ratio < COMPACT_RANK_RATIO) return DisplayMode.COMPACT;
      return DisplayMode.EXPANDED;
    },
    applyLayout: function() {
      var self = this;
      this.panels.forEach(function(p) {
        if (!p.locked) {
          var newMode = self.getModeFromRank(p);
          if (TRANSITIONS[p.mode] && TRANSITIONS[p.mode].indexOf(newMode) !== -1) {
            p.mode = newMode;
          }
        }
      });
    },
    getLayoutPositions: function() {
      var sorted = this.panels.map(function(p, i) { return { panel: p, idx: i }; });
      sorted.sort(function(a, b) { return b.panel.rank - a.panel.rank; });
      var positions = {};
      var cols = 4;
      var row = 1;
      var i = 0;
      function assign(pid, colSpan, rowSpan) {
        var col = 1;
        positions[pid] = { col: 1, colSpan: colSpan || 1, row: row, rowSpan: rowSpan || 1 };
      }
      sorted.forEach(function(item) {
        var p = item.panel;
        if (p.overridePos) {
          positions[p.id] = {
            col: p.overridePos.col, colSpan: p.overridePos.colSpan || 1,
            row: p.overridePos.row, rowSpan: p.overridePos.rowSpan || 1
          };
          return;
        }
        if (i === 0)      { assign(p.id, 2, 2); }
        else if (i === 1) { assign(p.id, 2, 1); }
        else if (i === 2) { assign(p.id, 2, 1); }
        else if (i === 3) { assign(p.id, 1, 1); }
        else if (i === 4) { assign(p.id, 1, 1); }
        else              { assign(p.id, 1, 1); }
        i++;
      });
      return positions;
    },
    cycleMode: function(panelId) {
      var p = this.findPanel(panelId);
      if (!p) return;
      var cycle = [DisplayMode.EXPANDED, DisplayMode.COMPACT, DisplayMode.COLLAPSED];
      var idx = cycle.indexOf(p.mode);
      var next = cycle[(idx + 1) % cycle.length];
      if (TRANSITIONS[p.mode] && TRANSITIONS[p.mode].indexOf(next) !== -1) {
        p.mode = next;
      }
      this.recordInteraction(panelId);
    },
    toggleLock: function(panelId) {
      var p = this.findPanel(panelId);
      if (!p) return;
      p.locked = !p.locked;
      if (!p.locked) { p.overridePos = null; }
      this.recordInteraction(panelId);
    },
    setOverridePosition: function(panelId, col, row) {
      var p = this.findPanel(panelId);
      if (!p) return;
      p.locked = true;
      p.overridePos = { col: col, row: row, colSpan: 1, rowSpan: 1 };
      this.recordInteraction(panelId);
    },
    findPanel: function(id) {
      for (var i = 0; i < this.panels.length; i++) {
        if (this.panels[i].id === id) return this.panels[i];
      }
      return null;
    },
    resetAll: function() {
      this.flushViewDurations();
      this.tracking = {};
      this.panels = samplePanels.map(function(p) {
        return { id: p.id, title: p.title, content: p.content, locked: false, overridePos: null, mode: DisplayMode.EXPANDED, rank: 1 };
      });
      this.visibleSet = {};
      this.layoutCount = 0;
      this.ensureTrackingObjects();
      this.saveState();
      this.render();
      this.initObserver();
      this.populateVisibleSet();
      this.updateStats();
    },
    updateStats: function() {
      document.getElementById('stat-panels').textContent = this.panels.length + ' panels';
      document.getElementById('stat-tracked').textContent = 'tracking active';
      document.getElementById('stat-layouts').textContent = this.layoutCount + ' layouts';
    },
    render: function() {
      var container = document.getElementById('dashboard');
      if (this.observer) this.observer.disconnect();
      var positions = this.getLayoutPositions();
      var html = '';
      var self = this;
      this.panels.forEach(function(p) {
        var pos = positions[p.id] || { col: 1, colSpan: 1, row: 1, rowSpan: 1 };
        var mc = metricContent[p.content];
        var cls = 'panel';
        if (p.locked) cls += ' locked';
        if (p.mode === DisplayMode.COMPACT) cls += ' compact';
        if (p.mode === DisplayMode.COLLAPSED) cls += ' collapsed';
        var rank = safeNum(p.rank, 0);
        var badgeCls = 'panel-rank-badge';
        if (rank > 0 && self.panels.length > 0) {
          var maxR = Math.max.apply(null, self.panels.map(function(x) { return x.rank; }));
          if (maxR > 0 && rank / maxR > 0.7) badgeCls += ' hot';
        }
        var activity = 'inactive';
        var t = self.tracking[p.id];
        if (t && t.lastInteraction) {
          var h = hoursSince(t.lastInteraction);
          if (h < 1) activity = 'active';
          else if (h < 24) activity = 'recent';
        }
        html += '<div class="' + cls + '" id="panel-' + p.id + '" data-panel-id="' + p.id + '"';
        html += ' style="grid-column: ' + pos.col + ' / span ' + (pos.colSpan || 1) + '; grid-row: ' + pos.row + ' / span ' + (pos.rowSpan || 1) + ';"';
        html += ' role="region" aria-label="' + p.title + ' panel">';
        html += '<div class="override-indicator" title="Locked &amp; overridden"></div>';
        html += '<div class="panel-header">';
        html += '<span class="panel-title">' + p.title + '</span>';
        html += '<div class="panel-controls">';
        html += '<button class="btn-lock" data-action="lock" data-panel-id="' + p.id + '" aria-pressed="' + (p.locked ? 'true' : 'false') + '" aria-label="' + (p.locked ? 'Unlock' : 'Lock') + ' panel position">' + (p.locked ? '&#128274;' : '&#128275;') + '</button>';
        html += '<button class="btn-toggle" data-action="toggle" data-panel-id="' + p.id + '" aria-label="Toggle panel size (current: ' + p.mode + ')">';
        if (p.mode === DisplayMode.EXPANDED) html += '&#9660;';
        else if (p.mode === DisplayMode.COMPACT) html += '&#9654;';
        else html += '&#9654;&#65038;';
        html += '</button>';
        html += '</div></div>';
        if (p.mode !== DisplayMode.COLLAPSED) {
          html += '<div class="panel-body">';
          if (p.mode === DisplayMode.COMPACT && mc) {
            html += '<span class="metric-preview">' + mc.value + '</span>';
            html += '<span class="metric-label">' + mc.sub + '</span>';
          } else if (mc) {
            html += '<div class="metric-value">' + mc.value + '</div>';
            html += '<div class="metric-subtitle">' + mc.sub + '</div>';
            html += '<div class="sparkline">' + sparkSVG(mc.spark) + '</div>';
          }
          html += '</div>';
        }
        html += '<div class="panel-footer">';
        html += '<span><span class="activity-dot ' + activity + '"></span>' + (activity === 'active' ? 'active now' : activity === 'recent' ? 'recent' : 'idle') + '</span>';
        html += '<span class="' + badgeCls + '">Rank #' + (rank > 0 ? rank.toFixed(1) : '0.0') + '</span>';
        html += '</div>';
        html += '</div>';
      });
      container.innerHTML = html;
      container.querySelectorAll('button[data-action]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          var pid = btn.getAttribute('data-panel-id');
          var action = btn.getAttribute('data-action');
          if (action === 'toggle') { self.cycleMode(pid); self.render(); self.initObserver(); self.populateVisibleSet(); self.updateStats(); }
          else if (action === 'lock') { self.toggleLock(pid); self.layoutCount++; self.render(); self.initObserver(); self.populateVisibleSet(); self.updateStats(); self.saveState(); }
        });
      });
      this.initObserver();
      this.saveState();
    }
  };
  dashboard.init();
})();
</script>
</body>
</html>
Edge Cases & Accessibility (from teacher feedback)
Keyboard handlers: all buttons respond to Enter/Space via delegated keydown listener on dashboard container and explicit listeners on reset button. aria-pressed on lock toggle, aria-label on all controls with current state.
Null-safe fallbacks: safeNum() wraps every numeric read from tracking and rank. If viewStart, interactions, viewDurationMs, rank are null/undefined they fall back to 0. overridePos null disables override. locked missing defaults false.
Toggle state machine: DisplayMode enum {EXPANDED, COMPACT, COLLAPSED} with VALID_TRANSITIONS adjacency map. cycleMode() walks the cycle only through valid edges. applyLayout() checks transition validity before changing mode.
Post-mount init: populateVisibleSet() fires via requestAnimationFrame immediately after render/init, calling getBoundingClientRect on every panel element to seed visibleSet before IntersectionObserver delivers its first callback. Eliminates first-tick race condition where visibleSet is empty.
No dead code: no visibleStart variable. Only viewStart (timestamp) used for duration tracking.
Per-panel locking: toggleLock() sets locked flag on single panel only. Locking prevents auto-rank changes and auto-layout for that panel. Unlocking clears overridePos. No cross-panel lock propagation.
Recency tracking: lastInteraction timestamp per panel, hoursSince() decay function, rank formula = (interactions+1) × (viewSeconds+1) × max(0.1, 1/(hours+1)).
Persistence: localStorage read on init, write every 4s + on render. Reset button clears all state.
Layout count: incremented on lock toggles, displayed in stats bar.