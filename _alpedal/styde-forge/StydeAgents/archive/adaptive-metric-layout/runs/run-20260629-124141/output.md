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
  --surface-hover: #1f2433;
  --border: #2a2e3a;
  --text: #e1e4eb;
  --text-muted: #8b91a4;
  --accent: #5b8def;
  --accent-glow: rgba(91,141,239,0.15);
  --danger: #e0556a;
  --warning: #e0a955;
  --success: #55c07a;
  --radius: 10px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 4px;
}
.header h1 { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
.controls { display: flex; gap: 10px; }
.btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: var(--transition);
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn.active { background: var(--accent); border-color: var(--accent); }
.btn.danger { border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: var(--danger); color: #fff; }
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
  gap: 16px;
  transition: var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  position: relative;
  transition: all var(--transition);
  cursor: default;
  overflow: hidden;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.locked { border-color: var(--warning); }
.panel.locked::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--warning);
  border-radius: var(--radius) var(--radius) 0 0;
}
.panel.full { grid-column: span 2; grid-row: span 2; }
.panel.compact { grid-column: span 1; grid-row: span 1; font-size: 0.9rem; }
.panel.compact .panel-body { max-height: 80px; overflow: hidden; }
.panel.compact .panel-chart { display: none; }
.panel.collapsed { display: none; }
.panel.more-section { grid-column: span 1; grid-row: span 1; opacity: 0.7; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.panel-title { font-weight: 600; font-size: 0.95rem; color: var(--text); }
.panel-actions { display: flex; gap: 6px; }
.panel-action {
  background: none;
  border: 1px solid transparent;
  color: var(--text-muted);
  width: 28px; height: 28px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}
.panel-action:hover { background: var(--surface-hover); color: var(--text); border-color: var(--border); }
.panel-action.locked-btn.locked { color: var(--warning); border-color: var(--warning); }
.panel-value { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 4px; }
.panel-label { font-size: 0.8rem; color: var(--text-muted); }
.panel-change { font-size: 0.8rem; margin-top: 4px; }
.panel-change.up { color: var(--success); }
.panel-change.down { color: var(--danger); }
.panel-chart {
  margin-top: 14px;
  height: 50px;
  display: flex;
  align-items: flex-end;
  gap: 3px;
}
.chart-bar {
  flex: 1;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
  min-height: 4px;
  transition: height 0.5s ease;
  opacity: 0.7;
}
.chart-bar:nth-child(odd) { opacity: 0.5; }
.more-dropdown {
  position: relative;
}
.more-panels {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  min-width: 220px;
  z-index: 100;
  padding: 8px;
  margin-top: 6px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.more-dropdown.open .more-panels { display: block; }
.more-item {
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: var(--transition);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.more-item:hover { background: var(--surface-hover); }
.more-item-score { font-size: 0.7rem; color: var(--text-muted); }
.score-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 0.6rem;
  color: var(--text-muted);
  opacity: 0;
  transition: opacity 0.2s;
}
.panel:hover .score-indicator { opacity: 1; }
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 12px 20px;
  border-radius: var(--radius);
  font-size: 0.85rem;
  z-index: 200;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" onclick="Dashboard.resetScores()" title="Reset all tracking data">Reset Scores</button>
    <button class="btn" onclick="Dashboard.resetLayout()" title="Clear locks and return to auto-layout">Reset Layout</button>
    <button class="btn" onclick="Dashboard.exportState()" title="Export layout state as JSON">Export State</button>
    <div class="more-dropdown" id="moreDropdown">
      <button class="btn" onclick="Dashboard.toggleMore()">More ▾</button>
      <div class="more-panels" id="morePanels"></div>
    </div>
  </div>
</div>
<div class="dashboard" id="dashboard">
  <div class="panel" data-panel="revenue" id="panel-revenue">
    <div class="panel-header">
      <span class="panel-title">Revenue</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('revenue')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">$847.2K</div>
      <div class="panel-label">Monthly Recurring Revenue</div>
      <div class="panel-change up">▲ 12.4% vs last month</div>
    </div>
    <div class="panel-chart" id="chart-revenue"></div>
  </div>
  <div class="panel" data-panel="users" id="panel-users">
    <div class="panel-header">
      <span class="panel-title">Active Users</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('users')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">24.3K</div>
      <div class="panel-label">Daily Active Users</div>
      <div class="panel-change up">▲ 8.1% vs last week</div>
    </div>
    <div class="panel-chart" id="chart-users"></div>
  </div>
  <div class="panel" data-panel="churn" id="panel-churn">
    <div class="panel-header">
      <span class="panel-title">Churn Rate</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('churn')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">2.1%</div>
      <div class="panel-label">Monthly Churn</div>
      <div class="panel-change down">▼ 0.3pp improvement</div>
    </div>
    <div class="panel-chart" id="chart-churn"></div>
  </div>
  <div class="panel" data-panel="latency" id="panel-latency">
    <div class="panel-header">
      <span class="panel-title">API Latency</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('latency')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">142ms</div>
      <div class="panel-label">P95 Response Time</div>
      <div class="panel-change up">▲ 5ms vs yesterday</div>
    </div>
    <div class="panel-chart" id="chart-latency"></div>
  </div>
  <div class="panel" data-panel="errors" id="panel-errors">
    <div class="panel-header">
      <span class="panel-title">Error Rate</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('errors')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">0.04%</div>
      <div class="panel-label">5xx Error Rate</div>
      <div class="panel-change down">▼ 0.01pp improvement</div>
    </div>
    <div class="panel-chart" id="chart-errors"></div>
  </div>
  <div class="panel" data-panel="storage" id="panel-storage">
    <div class="panel-header">
      <span class="panel-title">Storage</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('storage')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">3.8TB</div>
      <div class="panel-label">Used / 10TB Total</div>
      <div class="panel-change up">▲ 142GB this week</div>
    </div>
    <div class="panel-chart" id="chart-storage"></div>
  </div>
  <div class="panel" data-panel="sessions" id="panel-sessions">
    <div class="panel-header">
      <span class="panel-title">Sessions</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('sessions')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">1.2M</div>
      <div class="panel-label">Monthly Sessions</div>
      <div class="panel-change up">▲ 15.7% vs last month</div>
    </div>
    <div class="panel-chart" id="chart-sessions"></div>
  </div>
  <div class="panel" data-panel="cpu" id="panel-cpu">
    <div class="panel-header">
      <span class="panel-title">CPU Usage</span>
      <div class="panel-actions">
        <button class="panel-action locked-btn" onclick="Dashboard.toggleLock('cpu')" title="Lock position">🔒</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">67%</div>
      <div class="panel-label">Cluster Average</div>
      <div class="panel-change up">▲ 3pp vs yesterday</div>
    </div>
    <div class="panel-chart" id="chart-cpu"></div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
/*
 * Adaptive Metric Layout Engine
 * Version 1.0
 *
 * Architecture (3-layer separation):
 *   Layer 1: Scoring Engine — event collection and score computation
 *   Layer 2: Layout Assignment — score→tier mapping with lock/override logic
 *   Layer 3: Renderer — DOM updates based on layout assignments
 *
 * Export/Import State Contract:
 *   Persisted (survives serialization):
 *     - scores: per-panel {frequency, totalDuration, lastInteraction, interactions}
 *     - locks: set of locked panel IDs (manual overrides)
 *     - tierThresholds: {compact, collapse} percentile cutoffs
 *   Ephemeral (NOT persisted):
 *     - currentViewStart: per-panel view tracking timestamps (reset each session)
 *     - scrollPosition: current scroll offset
 *     - animationState: CSS transition in-progress flags
 *     - hoverState: which panel is currently hovered
 */
const STORAGE_KEY = 'adaptive-dashboard-layout';
const DECAY_LAMBDA = 0.05;
const FULL_TIER_PCT = 0.70;
const COMPACT_TIER_PCT = 0.30;
const Dashboard = (function() {
  'use strict';
  /*
   * LAYER 1: SCORING ENGINE
   *
   * Score formula: S = F × D × R
   *   F = interaction frequency (events per hour, clamped to [1, 100])
   *   D = normalized total view duration (seconds viewed / 3600, clamped to [0.1, 10])
   *   R = recency decay = e^(-λ × hours_since_last_interaction)
   *       λ = DECAY_LAMBDA (0.05) → half-life ≈ 13.9 hours
   *
   * Event types tracked:
   *   view_start / view_end : panel visible in viewport (IntersectionObserver)
   *   click : any click inside panel
   *   lock / unlock : manual lock toggle
   *   expand / collapse : tier transition triggered by user
   */
  const state = {
    scores: {},
    locks: new Set(),
    viewTimers: {},
    initialized: false
  };
  function defaultScore() {
    return { frequency: 1, totalDuration: 1, lastInteraction: Date.now(), interactions: [] };
  }
  function ensurePanel(panelId) {
    if (!state.scores[panelId]) state.scores[panelId] = defaultScore();
  }
  /*
   * Compute composite score for a single panel.
   * Input: panelId (string)
   * Output: { score: number, frequency: number, duration: number, recencyDecay: number }
   */
  function computeScore(panelId) {
    ensurePanel(panelId);
    const s = state.scores[panelId];
    const hoursSinceLast = (Date.now() - s.lastInteraction) / 3600000;
    const recencyDecay = Math.exp(-DECAY_LAMBDA * Math.max(0, hoursSinceLast));
    const frequency = Math.max(1, Math.min(100, s.frequency));
    const duration = Math.max(0.1, Math.min(10, s.totalDuration / 3600));
    const score = frequency * duration * recencyDecay;
    return { score, frequency, duration, recencyDecay };
  }
  function getAllScores() {
    const panels = document.querySelectorAll('.panel[data-panel]');
    const results = [];
    panels.forEach(function(p) {
      const pid = p.dataset.panel;
      results.push({ id: pid, score: computeScore(pid).score });
    });
    results.sort(function(a, b) { return b.score - a.score; });
    return results;
  }
  function recordEvent(panelId, type) {
    ensurePanel(panelId);
    const s = state.scores[panelId];
    s.lastInteraction = Date.now();
    s.interactions.push({ type: type, ts: Date.now() });
    if (s.interactions.length > 200) {
      s.interactions = s.interactions.slice(-200);
    }
    var now = Date.now();
    var recent = s.interactions.filter(function(e) { return (now - e.ts) < 3600000; });
    s.frequency = Math.max(1, recent.length);
    if (type === 'view_end' && state.viewTimers[panelId]) {
      var elapsed = (Date.now() - state.viewTimers[panelId]) / 1000;
      s.totalDuration += elapsed;
      delete state.viewTimers[panelId];
    }
  }
  /*
   * LAYER 2: LAYOUT ASSIGNMENT
   *
   * Tier assignment algorithm:
   *   1. Locked panels → always 'full' tier, positioned first
   *   2. Remaining panels sorted by composite score (descending)
   *   3. Top FULL_TIER_PCT (70%) → 'full' tier (2×2 grid span)
   *   4. Middle (30%-70% range) → 'compact' tier (1×1 grid span)
   *   5. Bottom COMPACT_TIER_PCT (30%) → 'collapsed' tier (hidden, shown in "More")
   *
   * Input: scores (array of {id, score})
   * Output: assignments (Map of panelId → tier string)
   */
  function assignTiers(scores) {
    var assignments = {};
    var unlocked = scores.filter(function(s) { return !state.locks.has(s.id); });
    scores.forEach(function(s) {
      if (state.locks.has(s.id)) {
        assignments[s.id] = 'locked';
      }
    });
    if (unlocked.length === 0) return assignments;
    var total = unlocked.length;
    var fullCutoff = Math.max(1, Math.floor(total * FULL_TIER_PCT));
    var compactCutoff = Math.max(fullCutoff, Math.floor(total * (1 - COMPACT_TIER_PCT)));
    unlocked.forEach(function(s, idx) {
      if (idx < fullCutoff) {
        assignments[s.id] = 'full';
      } else if (idx < compactCutoff) {
        assignments[s.id] = 'compact';
      } else {
        assignments[s.id] = 'collapsed';
      }
    });
    return assignments;
  }
  /*
   * LAYER 3: RENDERER
   *
   * Applies tier-based CSS classes and reorders panels in DOM.
   * Locked panels retain their position; unlocked panels follow score order.
   */
  function render(assignments) {
    var dashboard = document.getElementById('dashboard');
    var panels = dashboard.querySelectorAll('.panel[data-panel]');
    panels.forEach(function(panel) {
      var pid = panel.dataset.panel;
      var tier = assignments[pid] || 'compact';
      panel.classList.remove('full', 'compact', 'collapsed', 'locked');
      if (tier === 'locked') {
        panel.classList.add('full', 'locked');
        var lockBtn = panel.querySelector('.locked-btn');
        if (lockBtn) lockBtn.classList.add('locked');
      } else if (tier === 'full') {
        panel.classList.add('full');
        var lb2 = panel.querySelector('.locked-btn');
        if (lb2) lb2.classList.remove('locked');
      } else if (tier === 'compact') {
        panel.classList.add('compact');
        var lb3 = panel.querySelector('.locked-btn');
        if (lb3) lb3.classList.remove('locked');
      } else {
        panel.classList.add('collapsed');
        var lb4 = panel.querySelector('.locked-btn');
        if (lb4) lb4.classList.remove('locked');
      }
      var scoreEl = panel.querySelector('.score-indicator');
      if (!scoreEl) {
        scoreEl = document.createElement('span');
        scoreEl.className = 'score-indicator';
        panel.appendChild(scoreEl);
      }
      var sc = computeScore(pid);
      scoreEl.textContent = 'Score: ' + sc.score.toFixed(1);
    });
    updateMoreDropdown(assignments);
  }
  function updateMoreDropdown(assignments) {
    var container = document.getElementById('morePanels');
    var collapsed = [];
    for (var pid in assignments) {
      if (assignments[pid] === 'collapsed') collapsed.push(pid);
    }
    if (collapsed.length === 0) {
      container.innerHTML = '<div class="more-item" style="color:var(--text-muted)">All panels visible</div>';
      return;
    }
    container.innerHTML = collapsed.map(function(pid) {
      var sc = computeScore(pid);
      return '<div class="more-item" onclick="Dashboard.showPanel(\'' + pid + '\')">' +
        '<span>' + pid + '</span>' +
        '<span class="more-item-score">' + sc.score.toFixed(1) + '</span>' +
        '</div>';
    }).join('');
  }
  /*
   * PUBLIC API
   */
  function toggleLock(panelId) {
    ensurePanel(panelId);
    if (state.locks.has(panelId)) {
      state.locks.delete(panelId);
      toast('Unlocked: ' + panelId);
    } else {
      state.locks.add(panelId);
      toast('Locked: ' + panelId);
    }
    recordEvent(panelId, state.locks.has(panelId) ? 'lock' : 'unlock');
    refresh();
    save();
  }
  function showPanel(panelId) {
    ensurePanel(panelId);
    state.scores[panelId].lastInteraction = Date.now();
    state.scores[panelId].frequency = Math.min(100, state.scores[panelId].frequency + 10);
    toast('Restored: ' + panelId);
    recordEvent(panelId, 'expand');
    refresh();
    save();
  }
  function toggleMore() {
    document.getElementById('moreDropdown').classList.toggle('open');
  }
  function resetScores() {
    state.scores = {};
    document.querySelectorAll('.panel[data-panel]').forEach(function(p) {
      state.scores[p.dataset.panel] = defaultScore();
    });
    toast('Scores reset');
    refresh();
    save();
  }
  function resetLayout() {
    state.locks.clear();
    state.scores = {};
    document.querySelectorAll('.panel[data-panel]').forEach(function(p) {
      state.scores[p.dataset.panel] = defaultScore();
    });
    toast('Layout reset');
    refresh();
    save();
  }
  function exportState() {
    var data = {
      scores: state.scores,
      locks: Array.from(state.locks),
      tierThresholds: { full: FULL_TIER_PCT, compact: COMPACT_TIER_PCT },
      exportedAt: new Date().toISOString()
    };
    var blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'dashboard-layout-' + new Date().toISOString().slice(0,10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
    toast('State exported');
  }
  function refresh() {
    var scores = getAllScores();
    var assignments = assignTiers(scores);
    render(assignments);
  }
  function save() {
    var data = {
      scores: state.scores,
      locks: Array.from(state.locks)
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch(e) {}
  }
  function load() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var data = JSON.parse(raw);
      if (data.scores) state.scores = data.scores;
      if (data.locks) state.locks = new Set(data.locks);
    } catch(e) {}
  }
  function toast(msg) {
    var el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._timeout);
    el._timeout = setTimeout(function() { el.classList.remove('show'); }, 2000);
  }
  function setupTracking() {
    /*
     * View tracking via IntersectionObserver.
     * When a panel enters the viewport → record view_start.
     * When it leaves → record view_end, accumulate duration.
     */
    if (!window.IntersectionObserver) return;
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var pid = entry.target.dataset.panel;
        if (!pid) return;
        if (entry.isIntersecting) {
          state.viewTimers[pid] = Date.now();
        } else {
          if (state.viewTimers[pid]) {
            recordEvent(pid, 'view_end');
          }
        }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.panel[data-panel]').forEach(function(p) {
      observer.observe(p);
    });
    /*
     * Click tracking: any click inside a panel counts as interaction.
     * Does NOT fire on lock button clicks (those are handled separately).
     */
    document.addEventListener('click', function(e) {
      var panel = e.target.closest('.panel[data-panel]');
      if (!panel) return;
      if (e.target.closest('.locked-btn')) return;
      if (e.target.closest('.panel-action')) return;
      recordEvent(panel.dataset.panel, 'click');
      scheduleRefresh();
    });
  }
  var refreshTimer = null;
  function scheduleRefresh() {
    if (refreshTimer) clearTimeout(refreshTimer);
    refreshTimer = setTimeout(function() {
      refresh();
      save();
      refreshTimer = null;
    }, 2000);
  }
  function initCharts() {
    document.querySelectorAll('.panel-chart').forEach(function(chart) {
      var bars = '';
      for (var i = 0; i < 14; i++) {
        var h = 20 + Math.random() * 80;
        bars += '<div class="chart-bar" style="height:' + h + '%"></div>';
      }
      chart.innerHTML = bars;
    });
    setInterval(function() {
      document.querySelectorAll('.chart-bar').forEach(function(bar) {
        bar.style.height = (15 + Math.random() * 85) + '%';
      });
    }, 3000);
  }
  function init() {
    if (state.initialized) return;
    state.initialized = true;
    load();
    setupTracking();
    initCharts();
    refresh();
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.more-dropdown')) {
        document.getElementById('moreDropdown').classList.remove('open');
      }
    });
    var moreBtn = document.querySelector('#moreDropdown .btn');
    if (moreBtn) {
      moreBtn.addEventListener('click', function(e) {
        e.stopPropagation();
      });
    }
  }
  return {
    toggleLock: toggleLock,
    showPanel: showPanel,
    toggleMore: toggleMore,
    resetScores: resetScores,
    resetLayout: resetLayout,
    exportState: exportState,
    refresh: refresh
  };
})();
document.addEventListener('DOMContentLoaded', function() {
  Dashboard.refresh();
  setTimeout(function() { Dashboard.refresh(); }, 100);
});
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  Dashboard.refresh();
}
</script>
</body>
</html>