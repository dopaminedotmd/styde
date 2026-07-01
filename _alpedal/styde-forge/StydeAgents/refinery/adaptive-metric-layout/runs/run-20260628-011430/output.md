<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Adaptive Metric Layout Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d28;--surface-hover:#232738;--border:#2a2e3e;--text:#e2e4ed;--text-dim:#787c8c;--accent:#6c5ce7;--accent-glow:rgba(108,92,231,0.15);--danger:#e74c3c;--success:#2ecc71;--compact-w:280px;--compact-h:80px;--gap:12px;--radius:10px;--transition:0.35s cubic-bezier(0.4,0,0.2,1)}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.dashboard-header{padding:16px 24px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);background:var(--surface)}
.dashboard-header h1{font-size:20px;font-weight:600;letter-spacing:-0.3px}
.header-controls{display:flex;gap:10px;align-items:center}
.header-controls button{padding:6px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface);color:var(--text);cursor:pointer;font-size:13px;transition:all var(--transition)}
.header-controls button:hover{background:var(--surface-hover);border-color:var(--accent)}
.header-controls button.reset-btn{color:var(--danger);border-color:transparent}
.header-controls button.reset-btn:hover{border-color:var(--danger);background:rgba(231,76,60,0.1)}
.confidence-badge{font-size:12px;padding:4px 10px;border-radius:12px;background:var(--accent-glow);color:var(--accent);border:1px solid rgba(108,92,231,0.25)}
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:var(--gap);padding:16px;transition:all var(--transition);min-height:calc(100vh - 60px)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);position:relative;display:flex;flex-direction:column;min-height:100px}
.panel:hover{border-color:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 30px var(--accent-glow)}
.panel.locked{outline:2px solid var(--accent);outline-offset:-2px}
.panel-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid var(--border);cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:14px;font-weight:500;display:flex;align-items:center;gap:8px}
.panel-title .rank-badge{font-size:10px;background:var(--accent-glow);color:var(--accent);padding:1px 6px;border-radius:8px;font-weight:600}
.panel-controls{display:flex;gap:4px;align-items:center}
.panel-controls button{background:none;border:1px solid transparent;color:var(--text-dim);cursor:pointer;font-size:13px;padding:2px 6px;border-radius:4px;transition:all 0.15s;line-height:1}
.panel-controls button:hover{color:var(--text);background:var(--surface-hover);border-color:var(--border)}
.panel-controls button.lock-btn.active{color:var(--accent);border-color:var(--accent);background:var(--accent-glow)}
.panel-controls button.collapse-btn.active{color:var(--success)}
.panel-body{padding:14px;flex:1;transition:all var(--transition);overflow:hidden}
.panel.compact{grid-column:span 1;min-height:var(--compact-h)}
.panel.compact .panel-body{max-height:0;padding:0 14px;opacity:0;overflow:hidden}
.panel.compact .panel-body .compact-preview{max-height:none;opacity:1;padding:8px 0}
.panel.miniature{width:var(--compact-w);min-height:var(--compact-h)}
.panel.miniature .panel-body{max-height:0;padding:0;opacity:0}
.panel.miniature .panel-header{padding:6px 10px}
.panel.miniature .panel-title{font-size:12px}
.compact-preview{display:none;font-size:12px;color:var(--text-dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel.compact .compact-preview,.panel.miniature .compact-preview{display:block}
.metric-value{font-size:28px;font-weight:700;letter-spacing:-0.5px;margin-bottom:4px}
.metric-label{font-size:13px;color:var(--text-dim)}
.metric-change{font-size:12px;margin-top:4px;display:inline-block;padding:1px 6px;border-radius:4px}
.metric-change.up{color:var(--success);background:rgba(46,204,113,0.1)}
.metric-change.down{color:var(--danger);background:rgba(231,76,60,0.1)}
.chart-placeholder{height:80px;display:flex;align-items:flex-end;gap:3px;margin-top:10px}
.chart-bar{flex:1;border-radius:2px 2px 0 0;transition:height 0.5s ease;min-height:4px}
.usage-stats{font-size:11px;color:var(--text-dim);margin-top:8px;padding-top:8px;border-top:1px solid var(--border);display:flex;gap:12px}
.usage-stats span{display:flex;align-items:center;gap:3px}
.usage-stats .num{color:var(--text);font-weight:500}
.debug-overlay{position:fixed;bottom:0;right:0;z-index:999;background:var(--surface);border:1px solid var(--border);border-radius:8px 0 0 0;padding:12px 16px;font-size:11px;font-family:monospace;max-width:360px;max-height:200px;overflow-y:auto;color:var(--text-dim);opacity:0.85}
.debug-overlay .score-line{display:flex;justify-content:space-between;gap:8px;padding:1px 0}
.debug-overlay .score-line .name{color:var(--text)}
.empty-state{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;color:var(--text-dim);display:none}
.empty-state h3{font-size:18px;margin-bottom:6px;color:var(--text)}
@media(max-width:768px){
  .dashboard-grid{grid-template-columns:1fr;padding:8px;gap:8px}
  .dashboard-header{padding:12px;flex-wrap:wrap;gap:8px}
  .debug-overlay{max-width:100%;border-radius:0;max-height:120px}
}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Adaptive Metric Layout</h1>
  <div class="header-controls">
    <span class="confidence-badge">tracking active</span>
    <button id="resetBtn" class="reset-btn" title="Reset all tracking data and layout">reset</button>
    <button id="debugToggle" title="Toggle debug overlay">debug</button>
  </div>
</div>
<div class="dashboard-grid" id="dashboardGrid"></div>
<div class="debug-overlay" id="debugOverlay" style="display:none">
  <div style="font-weight:600;margin-bottom:4px;color:var(--accent)">attention scores</div>
  <div id="debugContent"></div>
</div>
<script>
(function(){
  'use strict';
  //  configuration
  const CONFIG = {
    HALF_LIFE_MS: 7 * 24 * 60 * 60 * 1000,   // 7-day half-life for recency
    SCORE_INTERVAL_MS: 3000,                   // recalculate every 3s
    LAYOUT_INTERVAL_MS: 8000,                  // re-layout every 8s
    COMPACT_THRESHOLD: 0.25,                   // panels below 25% of max score go compact
    MINIATURE_THRESHOLD: 0.10,                 // panels below 10% go miniature
    MAX_COMPACT_PANELS: 4,                     // max panels in compact row before hiding
    STORAGE_KEY: 'adaptive_metric_layout_v2'
  };
  //  panel definitions
  const PANEL_DEFS = [
    { id: 'revenue',      title: 'Revenue',        value: '$284,500', label: 'Monthly Recurring', change: '+12.4%', changeDir: 'up', bars: [45,62,58,71,65,78,82,74,85,80,88,92] },
    { id: 'users',        title: 'Active Users',    value: '48,291',   label: '7-day MAU',        change: '+3.2%',  changeDir: 'up', bars: [30,35,42,38,45,50,48,55,52,58,60,62] },
    { id: 'conversion',   title: 'Conversion',      value: '3.42%',   label: 'Avg across funnels', change: '-0.8%', changeDir: 'down', bars: [22,25,28,24,30,27,32,29,34,31,33,30] },
    { id: 'engagement',   title: 'Engagement',      value: '14.7m',   label: 'Avg session duration', change: '+8.1%', changeDir: 'up', bars: [55,58,62,60,68,72,70,78,75,80,85,88] },
    { id: 'retention',    title: 'Retention',       value: '0.87',    label: 'D7 cohort ratio',   change: '+1.5%',  changeDir: 'up', bars: [40,42,45,48,50,52,55,58,60,62,65,68] },
    { id: 'growth',       title: 'Growth Rate',     value: '7.2%',    label: 'WoW net new',       change: '-0.3%',  changeDir: 'down', bars: [15,18,22,20,25,28,30,27,32,29,35,33] },
    { id: 'churn',        title: 'Churn',           value: '4.1%',    label: 'Monthly voluntary',  change: '+0.6%',  changeDir: 'down', bars: [8,10,12,9,11,14,10,13,15,12,14,16] },
    { id: 'nps',          title: 'NPS',             value: '62',      label: 'Net Promoter Score', change: '+5pts',  changeDir: 'up', bars: [50,52,55,58,60,62,58,65,68,70,72,75] }
  ];
  //  state
  let state = {
    layout: [],           // ordered panel IDs as rendered
    panels: {},           // id -> {locked, collapsed, score, freq, duration, lastSeen, totalTime}
    initialized: false
  };
  //  load from localStorage
  function loadState() {
    try {
      const raw = localStorage.getItem(CONFIG.STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state.layout = parsed.layout || PANEL_DEFS.map(p => p.id);
        state.panels = parsed.panels || {};
        state.initialized = true;
        // ensure all panel defs exist in state
        PANEL_DEFS.forEach(p => {
          if (!state.panels[p.id]) {
            state.panels[p.id] = { locked: false, collapsed: false, score: 0, freq: 0, duration: 0, lastSeen: Date.now(), totalTime: 0 };
          }
        });
        return true;
      }
    } catch(e) { /* corrupted, reset */ }
    return false;
  }
  function saveState() {
    try {
      const data = { layout: state.layout, panels: state.panels };
      localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(data));
    } catch(e) { /* storage full or unavailable */ }
  }
  function resetState() {
    localStorage.removeItem(CONFIG.STORAGE_KEY);
    state.layout = PANEL_DEFS.map(p => p.id);
    state.panels = {};
    PANEL_DEFS.forEach(p => {
      state.panels[p.id] = { locked: false, collapsed: false, score: 0, freq: 0, duration: 0, lastSeen: Date.now(), totalTime: 0 };
    });
    saveState();
    renderGrid();
  }
  //  scoring: composite attention = frequency * duration_weighted * recency
  //  recency uses exponential decay: 2^(-elapsed / halfLife)
  function recencyDecay(lastSeen) {
    const elapsed = Date.now() - lastSeen;
    const halfLives = elapsed / CONFIG.HALF_LIFE_MS;
    return Math.pow(2, -halfLives);
  }
  function computeScore(panel) {
    const freq = panel.freq || 0;
    const duration = panel.duration || 0;
    const recency = recencyDecay(panel.lastSeen || Date.now());
    // floor durationWeight to avoid division instability when freq is 0
    const durationWeight = freq > 0 ? duration / Math.max(freq, 1) : 0;
    // composite: log-freq avoids linear dominance, capped at practical max
    const freqFactor = Math.log2(Math.max(freq, 1) + 1);
    const durFactor = Math.min(durationWeight / 10000, 10);
    const score = freqFactor * durFactor * recency;
    return Math.max(score, 0);
  }
  function recalculateScores() {
    PANEL_DEFS.forEach(p => {
      const ps = state.panels[p.id];
      if (ps) {
        ps.score = computeScore(ps);
      }
    });
  }
  //  layout engine: sort by score, respect locked panels, compact low-score
  function calculateLayout() {
    recalculateScores();
    // separate locked and unlocked
    const locked = state.layout.filter(id => {
      const ps = state.panels[id];
      return ps && ps.locked;
    });
    const unlocked = state.layout.filter(id => {
      const ps = state.panels[id];
      return ps && !ps.locked;
    });
    // sort unlocked by score descending
    unlocked.sort((a, b) => {
      const sa = state.panels[a] ? state.panels[a].score : 0;
      const sb = state.panels[b] ? state.panels[b].score : 0;
      return sb - sa;
    });
    // interleave: locked items keep their relative order, unlocked sorted between them
    const newLayout = [];
    const lockedSet = new Set(locked);
    // preserve relative order from current layout for locked, insert unlocked sorted
    let unlockedIdx = 0;
    state.layout.forEach(id => {
      if (lockedSet.has(id)) {
        newLayout.push(id);
      } else {
        // fill with next sorted unlocked
        while (unlockedIdx < unlocked.length && newLayout.includes(unlocked[unlockedIdx])) {
          unlockedIdx++;
        }
        if (unlockedIdx < unlocked.length) {
          const nextId = unlocked[unlockedIdx];
          if (!newLayout.includes(nextId)) {
            newLayout.push(nextId);
          }
          unlockedIdx++;
        }
      }
    });
    // append any remaining unlocked not yet placed
    unlocked.forEach(id => {
      if (!newLayout.includes(id)) {
        newLayout.push(id);
      }
    });
    // ensure all panel IDs present
    const allIds = new Set(PANEL_DEFS.map(p => p.id));
    allIds.forEach(id => {
      if (!newLayout.includes(id)) {
        newLayout.push(id);
      }
    });
    state.layout = newLayout;
  }
  //  rendering
  function renderGrid() {
    const grid = document.getElementById('dashboardGrid');
    if (!grid) return;
    calculateLayout();
    recalculateScores();
    // find max score for threshold calculations
    const maxScore = Math.max(1, ...PANEL_DEFS.map(p => state.panels[p.id]?.score || 0));
    grid.innerHTML = '';
    state.layout.forEach((id, idx) => {
      const def = PANEL_DEFS.find(p => p.id === id);
      if (!def) return;
      const ps = state.panels[id];
      if (!ps) return;
      const score = ps.score || 0;
      const scoreRatio = maxScore > 0 ? score / maxScore : 0;
      const panel = document.createElement('div');
      panel.className = 'panel';
      panel.dataset.panelId = id;
      panel.dataset.score = score.toFixed(4);
      panel.draggable = false;
      // size class
      if (ps.collapsed || scoreRatio <= CONFIG.MINIATURE_THRESHOLD) {
        panel.classList.add('miniature');
      } else if (scoreRatio <= CONFIG.COMPACT_THRESHOLD && idx >= Math.floor(state.layout.length * 0.5)) {
        panel.classList.add('compact');
      }
      if (ps.locked) panel.classList.add('locked');
      //  chart colors
      const barColors = ['#6c5ce7','#a29bfe','#fd79a8','#e17055','#00cec9','#55efc4','#fdcb6e','#74b9ff'];
      panel.innerHTML = `
        <div class="panel-header" data-panel-id="${id}">
          <div class="panel-title">
            ${def.title}
            <span class="rank-badge">#${idx + 1}</span>
          </div>
          <div class="panel-controls">
            <button class="lock-btn ${ps.locked ? 'active' : ''}" data-action="lock" title="${ps.locked ? 'Unlock' : 'Lock'} position">${ps.locked ? 'unlock' : 'lock'}</button>
            <button class="collapse-btn ${ps.collapsed ? 'active' : ''}" data-action="collapse" title="${ps.collapsed ? 'Expand' : 'Collapse'}">
              ${ps.collapsed ? '+' : chr(8722)}
            </button>
          </div>
        </div>
        <div class="panel-body">
          <div class="compact-preview">${def.value} | ${def.label}</div>
          <div class="metric-value">${def.value}</div>
          <div class="metric-label">${def.label}</div>
          <div class="metric-change ${def.changeDir}">${def.change}</div>
          <div class="chart-placeholder">
            ${def.bars.map((h, i) => `<div class="chart-bar" style="height:${h * 0.6}%;background:${barColors[i % barColors.length]}"></div>`).join('')}
          </div>
          <div class="usage-stats">
            <span>views <span class="num">${ps.freq || 0}</span></span>
            <span>time <span class="num">${fmtDuration(ps.duration || 0)}</span></span>
            <span>score <span class="num">${score.toFixed(2)}</span></span>
          </div>
        </div>
      `;
      grid.appendChild(panel);
    });
    //  attach event listeners
    attachPanelListeners();
    updateDebugOverlay();
  }
  function chr(code) {
    return String.fromCharCode(code);
  }
  function fmtDuration(ms) {
    if (ms < 1000) return ms + 'ms';
    if (ms < 60000) return (ms / 1000).toFixed(0) + 's';
    return (ms / 60000).toFixed(1) + 'm';
  }
  //  event binding
  function attachPanelListeners() {
    // lock buttons
    document.querySelectorAll('.lock-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const panelEl = this.closest('.panel');
        if (!panelEl) return;
        const id = panelEl.dataset.panelId;
        const ps = state.panels[id];
        if (!ps) return;
        ps.locked = !ps.locked;
        this.textContent = ps.locked ? 'unlock' : 'lock';
        this.classList.toggle('active');
        panelEl.classList.toggle('locked');
        // push locked panels to top of layout
        if (ps.locked) {
          state.layout = [id, ...state.layout.filter(i => i !== id)];
        }
        saveState();
        renderGrid();
      });
    });
    // collapse buttons
    document.querySelectorAll('.collapse-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const panelEl = this.closest('.panel');
        if (!panelEl) return;
        const id = panelEl.dataset.panelId;
        const ps = state.panels[id];
        if (!ps) return;
        ps.collapsed = !ps.collapsed;
        this.textContent = ps.collapsed ? '+' : chr(8722);
        this.classList.toggle('active');
        saveState();
        renderGrid();
      });
    });
    // track visibility via IntersectionObserver for view duration
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const panelEl = entry.target;
        const id = panelEl.dataset.panelId;
        const ps = state.panels[id];
        if (!ps) return;
        if (entry.isIntersecting) {
          ps._visibleSince = Date.now();
          // increment frequency for this view session (debounced, once per panel visibility)
          if (!ps._trackingView) {
            ps.freq = (ps.freq || 0) + 1;
            ps._trackingView = true;
          }
        } else {
          if (ps._visibleSince) {
            const elapsed = Date.now() - ps._visibleSince;
            ps.duration = (ps.duration || 0) + elapsed;
            ps.totalTime = (ps.totalTime || 0) + elapsed;
            ps.lastSeen = Date.now();
            ps._visibleSince = null;
          }
          ps._trackingView = false;
        }
      });
    }, { threshold: [0, 0.25, 0.5, 0.75, 1.0] });
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  }
  //  debug overlay
  function updateDebugOverlay() {
    const debug = document.getElementById('debugContent');
    if (!debug) return;
    const sorted = PANEL_DEFS.map(p => ({
      id: p.id,
      title: p.title,
      score: state.panels[p.id]?.score || 0,
      freq: state.panels[p.id]?.freq || 0,
      dur: state.panels[p.id]?.duration || 0,
      locked: state.panels[p.id]?.locked || false
    })).sort((a, b) => b.score - a.score);
    debug.innerHTML = sorted.map((s, i) =>
      `<div class="score-line"><span>${i + 1}. ${s.title}${s.locked ? ' 🔒' : ''}</span><span>${s.score.toFixed(3)} <span style="color:var(--text-dim)">| ${s.freq}v ${fmtDuration(s.dur)}</span></span></div>`
    ).join('');
  }
  //  periodic score recalculation and layout refresh
  function startAutoRecalculation() {
    setInterval(() => {
      // update visible panel durations
      document.querySelectorAll('.panel').forEach(el => {
        const id = el.dataset.panelId;
        const ps = state.panels[id];
        if (ps && ps._visibleSince) {
          // accumulate async
        }
      });
      renderGrid();
      saveState();
    }, CONFIG.SCORE_INTERVAL_MS);
    // full layout recalc less frequently
    setInterval(() => {
      recalculateScores();
      calculateLayout();
      renderGrid();
      saveState();
    }, CONFIG.LAYOUT_INTERVAL_MS);
  }
  //  initialization
  function init() {
    const loaded = loadState();
    if (!loaded) {
      state.layout = PANEL_DEFS.map(p => p.id);
      PANEL_DEFS.forEach(p => {
        if (!state.panels[p.id]) {
          state.panels[p.id] = { locked: false, collapsed: false, score: 0, freq: 0, duration: 0, lastSeen: Date.now(), totalTime: 0 };
        }
      });
    }
    renderGrid();
    startAutoRecalculation();
    // reset button
    document.getElementById('resetBtn')?.addEventListener('click', resetState);
    // debug toggle
    const debugOverlay = document.getElementById('debugOverlay');
    document.getElementById('debugToggle')?.addEventListener('click', () => {
      const isHidden = debugOverlay.style.display === 'none' || !debugOverlay.style.display;
      debugOverlay.style.display = isHidden ? 'block' : 'none';
    });
    // page-level visibility tracking: update lastSeen when tab hidden
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // mark all visible panels as last seen now
        document.querySelectorAll('.panel').forEach(el => {
          const id = el.dataset.panelId;
          const ps = state.panels[id];
          if (ps && ps._visibleSince) {
            const elapsed = Date.now() - ps._visibleSince;
            ps.duration = (ps.duration || 0) + elapsed;
            ps.totalTime = (ps.totalTime || 0) + elapsed;
            ps.lastSeen = Date.now();
            ps._visibleSince = null;
          }
        });
        saveState();
      } else {
        // restart visibility tracking on existing panels
        document.querySelectorAll('.panel').forEach(el => {
          const id = el.dataset.panelId;
          const ps = state.panels[id];
          if (ps) {
            ps._visibleSince = Date.now();
          }
        });
      }
    });
    // save on beforeunload
    window.addEventListener('beforeunload', () => {
      document.querySelectorAll('.panel').forEach(el => {
        const id = el.dataset.panelId;
        const ps = state.panels[id];
        if (ps && ps._visibleSince) {
          const elapsed = Date.now() - ps._visibleSince;
          ps.duration = (ps.duration || 0) + elapsed;
          ps.totalTime = (ps.totalTime || 0) + elapsed;
          ps.lastSeen = Date.now();
          ps._visibleSince = null;
        }
      });
      saveState();
    });
  }
  //  dom ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
</body>
</html>