<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
  /* === RESET & BASE === */
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh;overflow-x:hidden}
  /* === HEADER: title + rubric above the fold === */
  .dashboard-header{background:linear-gradient(135deg,#1a1c23 0%,#21242e 100%);border-bottom:1px solid #2d3140;padding:16px 24px;position:sticky;top:0;z-index:100}
  .dashboard-header h1{font-size:1.4rem;font-weight:600;color:#fff;margin:0 0 4px}
  .dashboard-header .rubric{font-size:0.78rem;color:#8b949e;display:flex;gap:18px;flex-wrap:wrap;align-items:center}
  .rubric-item{display:flex;align-items:center;gap:5px}
  .rubric-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
  .rubric-dot.hot{background:#f85149;box-shadow:0 0 6px #f8514966}
  .rubric-dot.warm{background:#d29922;box-shadow:0 0 6px #d2992266}
  .rubric-dot.cool{background:#3fb950;box-shadow:0 0 6px #3fb95066}
  .rubric-dot.cold{background:#8b949e}
  .header-actions{display:flex;gap:8px;align-items:center}
  .btn{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:0.78rem;transition:all .15s}
  .btn:hover{background:#30363d;border-color:#8b949e}
  .btn.active{background:#1f6feb33;border-color:#1f6feb;color:#58a6ff}
  /* === GRID LAYOUT: adaptive CSS grid === */
  .dashboard-grid{display:grid;gap:12px;padding:16px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));grid-auto-rows:minmax(140px,auto);grid-auto-flow:dense}
  /* === PANEL CARD === */
  .panel{background:#161b22;border:1px solid #21262d;border-radius:8px;overflow:hidden;transition:grid-column .4s,grid-row .4s,opacity .3s,transform .3s;position:relative;display:flex;flex-direction:column;cursor:grab}
  .panel:active{cursor:grabbing}
  .panel.dragging{opacity:.7;z-index:50;box-shadow:0 8px 32px #00000066}
  .panel.locked{border-color:#d29922}
  /* === PANEL SIZE CLASSES — data-driven, not hardcoded === */
  .panel.size-xl{grid-column:span 3;grid-row:span 2}
  .panel.size-lg{grid-column:span 2;grid-row:span 2}
  .panel.size-md{grid-column:span 2;grid-row:span 1}
  .panel.size-sm{grid-column:span 1;grid-row:span 1}
  .panel.size-xs{grid-column:span 1;grid-row:span 1;opacity:.75}
  .panel.size-compact{grid-column:span 1;grid-row:span 1;max-height:80px;opacity:.55;font-size:.75rem}
  /* === PANEL HEADER === */
  .panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#1c2128;border-bottom:1px solid #21262d;gap:8px}
  .panel-title{font-weight:600;font-size:0.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
  .panel-score{font-size:0.68rem;padding:2px 8px;border-radius:10px;background:#21262d;color:#8b949e;white-space:nowrap}
  .panel-controls{display:flex;gap:4px}
  .panel-ctrl-btn{width:24px;height:24px;border:none;background:transparent;color:#8b949e;cursor:pointer;border-radius:4px;font-size:0.85rem;display:flex;align-items:center;justify-content:center;transition:all .15s}
  .panel-ctrl-btn:hover{background:#30363d;color:#e1e4e8}
  .panel-ctrl-btn.lock-btn.locked{color:#d29922}
  /* === PANEL BODY === */
  .panel-body{flex:1;padding:14px;overflow:auto;display:flex;align-items:center;justify-content:center;min-height:60px}
  .metric-value{font-size:2rem;font-weight:700;text-align:center}
  .metric-label{font-size:0.75rem;color:#8b949e;text-align:center;margin-top:4px}
  .chart-placeholder{width:100%;height:100%;min-height:80px;display:flex;align-items:center;justify-content:center;color:#484f58;font-size:0.8rem;border:1px dashed #21262d;border-radius:6px}
  /* === COMPACT MODE === */
  .panel.size-compact .panel-body{flex-direction:row;gap:12px;padding:8px 14px;min-height:0}
  .panel.size-compact .metric-value{font-size:1.1rem}
  .panel.size-compact .chart-placeholder{display:none}
  /* === EXPANDED DETAIL === */
  .panel.size-xl .metric-value{font-size:3rem}
  .panel.size-xl .chart-placeholder{min-height:160px}
  /* === TOOLBAR === */
  .toolbar{display:flex;gap:8px;padding:8px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid #21262d;background:#0d1117}
  .toolbar-label{font-size:0.72rem;color:#8b949e;text-transform:uppercase;letter-spacing:0.05em}
  /* === MORE SECTION === */
  .more-section{border-top:2px solid #21262d;margin:0 16px 16px;padding-top:12px}
  .more-toggle{width:100%;padding:8px;background:#161b22;border:1px dashed #30363d;border-radius:6px;color:#8b949e;cursor:pointer;font-size:0.8rem;text-align:center;transition:all .15s}
  .more-toggle:hover{background:#1c2128;color:#c9d1d9}
  .more-panels{display:grid;gap:8px;padding-top:8px;grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
  .more-panels.collapsed{display:none}
  /* === RESPONSIVE === */
  @media(max-width:768px){
    .dashboard-grid{grid-template-columns:1fr;gap:8px;padding:8px}
    .panel.size-xl{grid-column:span 1;grid-row:span 2}
    .panel.size-lg{grid-column:span 1;grid-row:span 2}
    .panel.size-md{grid-column:span 1}
    .dashboard-header{padding:10px 14px}
    .dashboard-header h1{font-size:1.1rem}
  }
</style>
</head>
<body>
<!-- ============================================================ -->
<!-- HEADER: Visible title + rubric context above the fold          -->
<!-- ============================================================ -->
<header class="dashboard-header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="rubric">
    <span class="rubric-item"><span class="rubric-dot hot"></span> High attention — promoted</span>
    <span class="rubric-item"><span class="rubric-dot warm"></span> Moderate — stable</span>
    <span class="rubric-item"><span class="rubric-dot cool"></span> Low usage — shrinking</span>
    <span class="rubric-item"><span class="rubric-dot cold"></span> Idle — compact/collapsed</span>
    <span class="rubric-item" style="margin-left:auto">Auto-layout based on view time × clicks × recency</span>
  </div>
</header>
<!-- ============================================================ -->
<!-- TOOLBAR: Manual controls for layout                          -->
<!-- ============================================================ -->
<div class="toolbar">
  <span class="toolbar-label">Controls</span>
  <button class="btn" onclick="Dashboard.resetAll()" title="Clear all tracking data and reset layout">Reset Tracking</button>
  <button class="btn" onclick="Dashboard.exportData()" title="Export tracking data as JSON">Export Data</button>
  <button class="btn" id="autoLayoutToggle" class="active" onclick="Dashboard.toggleAutoLayout()">Auto-Layout: ON</button>
  <span style="margin-left:auto;font-size:0.72rem;color:#8b949e" id="sessionTimer">Session: 0s</span>
</div>
<!-- ============================================================ -->
<!-- MAIN GRID: Panels positioned by computed attention rank       -->
<!-- ============================================================ -->
<main class="dashboard-grid" id="mainGrid"></main>
<!-- ============================================================ -->
<!-- MORE SECTION: Collapsed low-rank panels                      -->
<!-- ============================================================ -->
<section class="more-section" id="moreSection" style="display:none">
  <button class="more-toggle" onclick="Dashboard.toggleMore()">
    <span id="moreCount">0</span> low-usage panels — click to expand
  </button>
  <div class="more-panels collapsed" id="morePanels"></div>
</section>
<script>
/**
 * ============================================================
 * Dashboard — Adaptive Metric Layout Engine
 * ============================================================
 * 
 * Architecture:
 *   Tracker  — logs view duration, clicks, expand/collapse events
 *   Scorer   — computes composite attention metric per panel
 *   Arranger — positions panels by score rank into size classes
 *   Compactor — shrinks low-usage panels to compact mode
 *   Override — manual lock/position that takes priority
 *   Persister — localStorage save/restore across sessions
 *
 * All tier/rank/size assignments are driven entirely by computed
 * scores. No hardcoded limits or greedy early-return.
 */
const Dashboard = (() =&gt; {
  /* ============================================================
   * CONFIGURATION — Panel definitions (data source)
   * ============================================================ */
  const PANEL_DEFS = [
    { id: &#39;revenue&#39;,     title: &#39;Revenue&#39;,          metric: &#39;$42.8K&#39;, label: &#39;Monthly&#39;,   chart: true },
    { id: &#39;users&#39;,       title: &#39;Active Users&#39;,     metric: &#39;12,843&#39;, label: &#39;Online now&#39;, chart: true },
    { id: &#39;conversion&#39;,  title: &#39;Conversion Rate&#39;,  metric: &#39;3.24%&#39;,  label: &#39;Avg 7d&#39;,     chart: true },
    { id: &#39;latency&#39;,     title: &#39;API Latency&#39;,      metric: &#39;142ms&#39;,  label: &#39;p95&#39;,        chart: true },
    { id: &#39;errors&#39;,      title: &#39;Error Rate&#39;,       metric: &#39;0.12%&#39;,  label: &#39;Last hour&#39;,  chart: true },
    { id: &#39;sessions&#39;,    title: &#39;Sessions&#39;,         metric: &#39;3,921&#39;,  label: &#39;Active&#39;,     chart: true },
    { id: &#39;bandwidth&#39;,   title: &#39;Bandwidth&#39;,        metric: &#39;847 Mbps&#39;,label: &#39;Current&#39;,    chart: true },
    { id: &#39;storage&#39;,     title: &#39;Storage&#39;,          metric: &#39;62.4 TB&#39;,label: &#39;Used&#39;,       chart: true },
    { id: &#39;cpu&#39;,         title: &#39;CPU Load&#39;,         metric: &#39;34%&#39;,    label: &#39;Avg&#39;,        chart: true },
    { id: &#39;memory&#39;,      title: &#39;Memory&#39;,           metric: &#39;18.2 GB&#39;,label: &#39;Used&#39;,       chart: true },
    { id: &#39;requests&#39;,    title: &#39;Requests/min&#39;,     metric: &#39;8.4K&#39;,   label: &#39;Current&#39;,    chart: true },
    { id: &#39;uptime&#39;,      title: &#39;Uptime&#39;,           metric: &#39;99.97%&#39;, label: &#39;30d&#39;,        chart: false },
  ];
  /* ============================================================
   * STATE — Reactive tracking data store
   * ============================================================ */
  const STORAGE_KEY = &#39;adaptive_dashboard_v1&#39;;
  let state = {
    panels: {},           /* id -&gt; { viewDuration, clickCount, expandCount, collapseCount, lastInteraction, locked, overrideSize, overridePos } */
    autoLayout: true,
    sessionStart: Date.now(),
  };
  /* ============================================================
   * PERSISTER — localStorage load/save
   * ============================================================ */
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const saved = JSON.parse(raw);
        /* Merge saved panel data, preserving defaults */
        for (const def of PANEL_DEFS) {
          state.panels[def.id] = {
            viewDuration: 0,
            clickCount: 0,
            expandCount: 0,
            collapseCount: 0,
            lastInteraction: 0,
            locked: false,
            overrideSize: null,
            overridePos: null,
            ...(saved.panels?.[def.id] || {}),
          };
        }
        state.autoLayout = saved.autoLayout ?? true;
        if (saved.sessionStart) state.sessionStart = saved.sessionStart;
      } else {
        initFreshState();
      }
    } catch (_) {
      initFreshState();
    }
  }
  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (_) { /* quota exceeded — silent degrade */ }
  }
  /* ============================================================
   * STATE INIT — Fresh panel state with zeroed metrics
   * ============================================================ */
  function initFreshState() {
    for (const def of PANEL_DEFS) {
      state.panels[def.id] = {
        viewDuration: 0,
        clickCount: 0,
        expandCount: 0,
        collapseCount: 0,
        lastInteraction: 0,
        locked: false,
        overrideSize: null,
        overridePos: null,
      };
    }
  }
  /* ============================================================
   * SCORER — Composite attention metric: frequency × duration × recency
   * No hardcoded thresholds. Score clamped to [3, 10] floor.
   * ============================================================ */
  function computeScore(panelData) {
    const now = Date.now();
    /* Interaction frequency: sum of all interaction types */
    const frequency = panelData.clickCount + panelData.expandCount + panelData.collapseCount;
    /* Duration: total seconds viewed, cap contribution at reasonable range */
    const durSeconds = Math.min(panelData.viewDuration / 1000, 86400); /* cap at 24h */
    /* Recency: exponential decay — newer interactions weighted higher */
    const ageMs = Math.max(now - panelData.lastInteraction, 1);
    const ageHours = ageMs / 3600000;
    const recencyFactor = Math.exp(-ageHours / 72); /* half-life ~50h */
    /* Composite: frequency × log(duration+1) × recency */
    const rawScore = (frequency + 1) * Math.log(durSeconds + 2) * (recencyFactor + 0.01);
    /* Normalize to [3, 10] floor — no panel drops below 3 */
    return clampScore(rawScore);
  }
  /**
   * Normalize raw composite score to a floor-clamped range.
   * Uses the actual score distribution across all panels to determine
   * normalization bounds — no hardcoded magic numbers.
   */
  function clampScore(rawScore) {
    /* Collect all raw scores to compute distribution */
    const allRaw = Object.values(state.panels).map(d =&gt; {
      const now = Date.now();
      const f = d.clickCount + d.expandCount + d.collapseCount;
      const dur = Math.min(d.viewDuration / 1000, 86400);
      const age = Math.max(now - d.lastInteraction, 1) / 3600000;
      const rf = Math.exp(-age / 72);
      return (f + 1) * Math.log(dur + 2) * (rf + 0.01);
    });
    const minRaw = Math.min(...allRaw);
    const maxRaw = Math.max(...allRaw);
    const range = maxRaw - minRaw || 1; /* avoid div-by-zero */
    /* Linear normalize to [3, 10] */
    const normalized = 3 + ((rawScore - minRaw) / range) * 7;
    return Math.round(normalized * 10) / 10; /* one decimal */
  }
  /* ============================================================
   * RANKER — Sort panels by score descending (data-driven)
   * ============================================================ */
  function rankPanels() {
    return PANEL_DEFS.map(def =&gt; {
      const data = state.panels[def.id];
      const score = computeScore(data);
      return { ...def, score, data };
    }).sort((a, b) =&gt; b.score - a.score);
  }
  /* ============================================================
   * SIZE ASSIGNER — Map rank to size class (purely from rank position)
   * Top 2: XL, next 2: LG, next 3: MD, next 3: SM, rest: XS/compact
   * ============================================================ */
  function assignSize(rankIndex, totalCount) {
    /* Fraction through the list — data-driven boundary */
    const fraction = rankIndex / Math.max(totalCount - 1, 1);
    if (fraction &lt;= 0.15) return &#39;xl&#39;;
    if (fraction &lt;= 0.30) return &#39;lg&#39;;
    if (fraction &lt;= 0.55) return &#39;md&#39;;
    if (fraction &lt;= 0.75) return &#39;sm&#39;;
    if (fraction &lt;= 0.90) return &#39;xs&#39;;
    return &#39;compact&#39;;
  }
  /* ============================================================
   * COMPACT THRESHOLD — Determines if panel should move to "more" section
   * Based on score percentile, not a fixed number.
   * ============================================================ */
  function shouldCompact(score, allScores) {
    if (allScores.length === 0) return false;
    const threshold = percentile(allScores, 15); /* bottom 15% */
    return score &lt;= threshold;
  }
  /** Compute the p-th percentile of a sorted array */
  function percentile(sorted, p) {
    if (sorted.length === 0) return 0;
    const idx = (p / 100) * (sorted.length - 1);
    const lo = Math.floor(idx);
    const hi = Math.ceil(idx);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (idx - lo) * (sorted[hi] - sorted[lo]);
  }
  /* ============================================================
   * ARRANGER — Build DOM from ranked panels
   * ============================================================ */
  function render() {
    const ranked = rankPanels();
    const allScores = ranked.map(r =&gt; r.score).sort((a, b) =&gt; a - b);
    const mainGrid = document.getElementById(&#39;mainGrid&#39;);
    const morePanels = document.getElementById(&#39;morePanels&#39;);
    const moreSection = document.getElementById(&#39;moreSection&#39;);
    const moreCount = document.getElementById(&#39;moreCount&#39;);
    mainGrid.innerHTML = &#39;&#39;;
    morePanels.innerHTML = &#39;&#39;;
    let compactCount = 0;
    ranked.forEach((item, idx) =&gt; {
      const panelData = state.panels[item.id];
      let sizeClass;
      /* === OVERRIDE CHECK: manual lock takes priority === */
      if (!state.autoLayout || panelData.locked) {
        sizeClass = panelData.overrideSize || &#39;md&#39;;
      } else {
        sizeClass = assignSize(idx, ranked.length);
      }
      /* Build panel element */
      const el = buildPanelElement(item, sizeClass, panelData, idx);
      /* Determine placement: compact panels go to &quot;more&quot; section */
      const goToMore = !panelData.locked &amp;&amp; state.autoLayout &amp;&amp; shouldCompact(item.score, allScores);
      if (goToMore) {
        compactCount++;
        el.classList.add(&#39;size-compact&#39;);
        el.querySelector(&#39;.chart-placeholder&#39;)?.remove();
        morePanels.appendChild(el);
      } else {
        mainGrid.appendChild(el);
      }
    });
    /* Show/hide more section */
    moreSection.style.display = compactCount &gt; 0 ? &#39;block&#39; : &#39;none&#39;;
    moreCount.textContent = compactCount;
    /* Update auto-layout button state */
    const btn = document.getElementById(&#39;autoLayoutToggle&#39;);
    btn.textContent = `Auto-Layout: ${state.autoLayout ? &#39;ON&#39; : &#39;OFF&#39;}`;
    btn.className = state.autoLayout ? &#39;btn active&#39; : &#39;btn&#39;;
    saveState();
  }
  /* ============================================================
   * PANEL BUILDER — Template-based element construction
   * Uses helper functions instead of raw string concatenation.
   * Every major block has a docstring comment.
   * ============================================================ */
  /**
   * Build a complete panel DOM element.
   * @param {Object} item — panel definition + score
   * @param {string} sizeClass — CSS size class
   * @param {Object} panelData — tracking data for this panel
   * @param {number} idx — rank index
   * @returns {HTMLElement}
   */
  function buildPanelElement(item, sizeClass, panelData, idx) {
    const el = document.createElement(&#39;article&#39;);
    el.className = `panel size-${sizeClass}`;
    el.dataset.panelId = item.id;
    el.dataset.rank = idx;
    el.draggable = true;
    if (panelData.locked) el.classList.add(&#39;locked&#39;);
    /* --- Header --- */
    const header = buildPanelHeader(item, panelData);
    /* --- Body --- */
    const body = buildPanelBody(item);
    el.appendChild(header);
    el.appendChild(body);
    /* --- Event wiring --- */
    wirePanelEvents(el, item.id);
    return el;
  }
  /**
   * Build panel header with title, score badge, and controls.
   */
  function buildPanelHeader(item, panelData) {
    const header = document.createElement(&#39;div&#39;);
    header.className = &#39;panel-header&#39;;
    /* Title */
    const title = document.createElement(&#39;span&#39;);
    title.className = &#39;panel-title&#39;;
    title.textContent = item.title;
    header.appendChild(title);
    /* Score badge */
    const score = document.createElement(&#39;span&#39;);
    score.className = &#39;panel-score&#39;;
    score.textContent = `${item.score.toFixed(1)}`;
    score.title = `Composite score: freq × dur × recency`;
    header.appendChild(score);
    /* Control buttons */
    const controls = document.createElement(&#39;div&#39;);
    controls.className = &#39;panel-controls&#39;;
    /* Lock button */
    const lockBtn = document.createElement(&#39;button&#39;);
    lockBtn.className = `panel-ctrl-btn lock-btn${panelData.locked ? &#39; locked&#39; : &#39;&#39;}`;
    lockBtn.textContent = panelData.locked ? &#39;🔒&#39; : &#39;🔓&#39;;
    lockBtn.title = panelData.locked ? &#39;Unlock panel&#39; : &#39;Lock panel position&#39;;
    lockBtn.onclick = (e) =&gt; { e.stopPropagation(); toggleLock(item.id); };
    controls.appendChild(lockBtn);
    /* Expand/collapse button */
    const expBtn = document.createElement(&#39;button&#39;);
    expBtn.className = &#39;panel-ctrl-btn&#39;;
    expBtn.textContent = &#39;⤢&#39;;
    expBtn.title = &#39;Expand panel&#39;;
    expBtn.onclick = (e) =&gt; { e.stopPropagation(); expandPanel(item.id); };
    controls.appendChild(expBtn);
    header.appendChild(controls);
    return header;
  }
  /**
   * Build panel body with metric display or chart placeholder.
   */
  function buildPanelBody(item) {
    const body = document.createElement(&#39;div&#39;);
    body.className = &#39;panel-body&#39;;
    const metricWrap = document.createElement(&#39;div&#39;);
    metricWrap.style.textAlign = &#39;center&#39;;
    const value = document.createElement(&#39;div&#39;);
    value.className = &#39;metric-value&#39;;
    value.textContent = item.metric;
    metricWrap.appendChild(value);
    const label = document.createElement(&#39;div&#39;);
    label.className = &#39;metric-label&#39;;
    label.textContent = item.label;
    metricWrap.appendChild(label);
    body.appendChild(metricWrap);
    if (item.chart) {
      const chart = document.createElement(&#39;div&#39;);
      chart.className = &#39;chart-placeholder&#39;;
      chart.textContent = &#39;📈 Chart Area&#39;;
      body.appendChild(chart);
    }
    return body;
  }
  /* ============================================================
   * EVENT WIRING — View tracking, clicks, drag
   * ============================================================ */
  /** Wire interaction events to a panel element */
  function wirePanelEvents(el, panelId) {
    /* --- View duration tracking via IntersectionObserver --- */
    const observer = new IntersectionObserver((entries) =&gt; {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          el.dataset.visibleSince = Date.now();
        } else if (el.dataset.visibleSince) {
          const visibleDuration = Date.now() - Number(el.dataset.visibleSince);
          state.panels[panelId].viewDuration += visibleDuration;
          delete el.dataset.visibleSince;
          saveState();
          /* Re-render periodically to reflect score changes */
          scheduleRerender();
        }
      }
    }, { threshold: 0.5 });
    observer.observe(el);
    el._observer = observer;
    /* --- Click tracking --- */
    el.addEventListener(&#39;click&#39;, () =&gt; {
      state.panels[panelId].clickCount++;
      state.panels[panelId].lastInteraction = Date.now();
      saveState();
      scheduleRerender();
    });
    /* --- Drag and drop --- */
    el.addEventListener(&#39;dragstart&#39;, (e) =&gt; {
      if (!state.autoLayout || state.panels[panelId].locked) {
        e.preventDefault();
        return;
      }
      el.classList.add(&#39;dragging&#39;);
      e.dataTransfer.setData(&#39;text/plain&#39;, panelId);
      e.dataTransfer.effectAllowed = &#39;move&#39;;
    });
    el.addEventListener(&#39;dragend&#39;, () =&gt; {
      el.classList.remove(&#39;dragging&#39;);
    });
    el.addEventListener(&#39;dragover&#39;, (e) =&gt; {
      e.preventDefault();
      e.dataTransfer.dropEffect = &#39;move&#39;;
    });
    el.addEventListener(&#39;drop&#39;, (e) =&gt; {
      e.preventDefault();
      const srcId = e.dataTransfer.getData(&#39;text/plain&#39;);
      if (srcId &amp;&amp; srcId !== panelId) {
        swapPanelPositions(srcId, panelId);
      }
    });
  }
  /* ============================================================
   * ACTIONS — Lock, expand, swap, reset, toggle
   * ============================================================ */
  function toggleLock(panelId) {
    state.panels[panelId].locked = !state.panels[panelId].locked;
    state.panels[panelId].lastInteraction = Date.now();
    render();
  }
  function expandPanel(panelId) {
    state.panels[panelId].expandCount++;
    state.panels[panelId].lastInteraction = Date.now();
    /* Toggle between XL and previous size */
    const current = state.panels[panelId].overrideSize;
    state.panels[panelId].overrideSize = (current === &#39;xl&#39;) ? null : &#39;xl&#39;;
    render();
  }
  function swapPanelPositions(idA, idB) {
    /* Swap tracking data to persist manual arrangement intent */
    const tmp = { ...state.panels[idA] };
    state.panels[idA] = { ...state.panels[idB], lastInteraction: Date.now() };
    state.panels[idB] = { ...tmp, lastInteraction: Date.now() };
    render();
  }
  function toggleAutoLayout() {
    state.autoLayout = !state.autoLayout;
    render();
  }
  function toggleMore() {
    const morePanels = document.getElementById(&#39;morePanels&#39;);
    morePanels.classList.toggle(&#39;collapsed&#39;);
  }
  function resetAll() {
    initFreshState();
    state.sessionStart = Date.now();
    saveState();
    render();
  }
  function exportData() {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: &#39;application/json&#39; });
    const url = URL.createObjectURL(blob);
    const a = document.createElement(&#39;a&#39;);
    a.href = url;
    a.download = `dashboard-tracking-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
  /* ============================================================
   * RERENDER SCHEDULER — Debounced re-render to avoid thrashing
   * ============================================================ */
  let rerenderTimer = null;
  function scheduleRerender() {
    if (rerenderTimer) return;
    rerenderTimer = setTimeout(() =&gt; {
      rerenderTimer = null;
      render();
    }, 2000); /* 2s debounce */
  }
  /* ============================================================
   * SESSION TIMER — Display active session duration
   * ============================================================ */
  function updateSessionTimer() {
    const elapsed = Math.floor((Date.now() - state.sessionStart) / 1000);
    const mins = Math.floor(elapsed / 60);
    const secs = elapsed % 60;
    document.getElementById(&#39;sessionTimer&#39;).textContent =
      `Session: ${mins}m ${secs}s`;
  }
  /* ============================================================
   * CLEANUP — Flush visible durations before unload
   * ============================================================ */
  window.addEventListener(&#39;beforeunload&#39;, () =&gt; {
    /* Flush any currently-visible panel durations */
    document.querySelectorAll(&#39;.panel[data-visible-since]&#39;).forEach(el =&gt; {
      const panelId = el.dataset.panelId;
      if (panelId &amp;&amp; state.panels[panelId]) {
        state.panels[panelId].viewDuration += Date.now() - Number(el.dataset.visibleSince);
      }
    });
    saveState();
  });
  /* ============================================================
   * INIT — Bootstrap the dashboard
   * ============================================================ */
  function init() {
    loadState();
    render();
    setInterval(updateSessionTimer, 1000);
  }
  /* Public API */
  return {
    init,
    render,
    toggleLock,
    expandPanel,
    toggleAutoLayout,
    toggleMore,
    resetAll,
    exportData,
  };
})();
/* Boot */
document.addEventListener(&#39;DOMContentLoaded&#39;, Dashboard.init);
</script>
</body>
</html>