Panel layout: adaptive grid
Layout engine tracks user attention and reshapes the dashboard. Drag a panel to lock it — locked panels keep their position. Unlocked panels flow by rank. Rarely used panels shrink to compact mode at the bottom.
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
  :root {
    --bg: #0b0f19;
    --surface: #141b2d;
    --border: #1e2a45;
    --text: #c8d6e5;
    --text-dim: #6b7a93;
    --accent: #4dabf7;
    --warn: #ffa94d;
    --danger: #ff6b6b;
    --compact-bg: #0d1117;
    --shadow: 0 2px 12px rgba(0,0,0,0.4);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }
  header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 20px; border-bottom: 1px solid var(--border);
    background: var(--surface);
  }
  header h1 { font-size: 1.1rem; font-weight: 600; letter-spacing: 0.02em; color: var(--accent); }
  header .controls { display: flex; gap: 10px; align-items: center; }
  button {
    background: var(--surface); border: 1px solid var(--border); color: var(--text);
    padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.85rem;
    transition: background 0.15s, border-color 0.15s;
  }
  button:hover { background: #1e2e50; border-color: var(--accent); }
  button.active { background: #1a3a5c; border-color: var(--accent); color: var(--accent); }
  #dashboard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding: 16px;
    min-height: 200px;
  }
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    cursor: grab;
    user-select: none;
    transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.25s;
    position: relative;
    min-height: 120px;
    display: flex; flex-direction: column;
  }
  .panel:hover { box-shadow: var(--shadow); border-color: #2a3f60; }
  .panel.dragging {
    opacity: 0.7; cursor: grabbing; z-index: 1000;
    transform: scale(1.03); box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  }
  .panel.locked { border-left: 3px solid var(--warn); }
  .panel-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 8px;
  }
  .panel-title { font-weight: 600; font-size: 0.95rem; }
  .panel-rank {
    font-size: 0.7rem; color: var(--text-dim);
    background: #1e2a45; padding: 2px 8px; border-radius: 10px;
  }
  .panel-body { flex: 1; font-size: 0.85rem; color: var(--text-dim); }
  .panel-score { font-size: 1.4rem; font-weight: 700; color: var(--accent); margin-top: 6px; }
  .panel-actions {
    display: flex; gap: 6px; margin-top: 10px;
    border-top: 1px solid var(--border); padding-top: 8px;
  }
  .panel-actions button {
    font-size: 0.72rem; padding: 3px 10px;
    background: transparent; border-color: var(--border);
  }
  .panel.locked .panel-actions .btn-lock { background: #3d2e1a; border-color: var(--warn); color: var(--warn); }
  .panel span.cols { font-size: 0.7rem; color: var(--text-dim); }
  /* Compact zone */
  #compact-zone {
    margin: 0 16px 20px;
    border: 1px dashed #1e2a45;
    border-radius: 10px;
    padding: 14px;
    background: var(--compact-bg);
  }
  #compact-zone h3 {
    font-size: 0.85rem; color: var(--text-dim); margin-bottom: 10px;
    font-weight: 500; letter-spacing: 0.03em; text-transform: uppercase;
  }
  #compact-grid {
    display: flex; flex-wrap: wrap; gap: 8px;
  }
  .compact-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.78rem;
    cursor: pointer;
    transition: background 0.15s;
    display: flex; align-items: center; gap: 8px;
    max-width: 220px;
  }
  .compact-panel:hover { background: #1a2440; border-color: var(--accent); }
  .compact-panel .cp-title { font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .compact-panel .cp-score { color: var(--text-dim); font-size: 0.72rem; }
  /* Stats bar */
  #stats {
    display: flex; gap: 20px; padding: 8px 20px; font-size: 0.75rem;
    color: var(--text-dim); border-bottom: 1px solid var(--border);
    background: #0d1117;
  }
  #stats span strong { color: var(--text); }
  .drag-ghost {
    position: fixed; pointer-events: none; z-index: 9999;
    opacity: 0.85; transform: scale(1.02);
  }
  @media (max-width: 900px) {
    #dashboard { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 500px) {
    #dashboard { grid-template-columns: 1fr; }
  }
</style>
<header>
  <h1>Adaptive Metric Dashboard</h1>
  <div class="controls">
    <button id="btn-reset" title="Reset all tracking data">Reset Tracking</button>
    <button id="btn-unlock-all">Unlock All</button>
    <button id="btn-force-layout">Force Relayout</button>
    <span style="font-size:0.75rem;color:var(--text-dim)">v1 — event-driven</span>
  </div>
</header>
<div id="stats">
  <span>Events tracked: <strong id="stat-events">0</strong></span>
  <span>Panels visible: <strong id="stat-visible">0</strong></span>
  <span>Compact: <strong id="stat-compact">0</strong></span>
  <span>Locked: <strong id="stat-locked">0</strong></span>
  <span>Last layout: <strong id="stat-last">—</strong></span>
</div>
<div id="dashboard"></div>
<div id="compact-zone">
  <h3>Compact — Low Usage</h3>
  <div id="compact-grid"></div>
</div>
<script>
  (function() {
    const HALF_LIFE_DAYS = 7;
    const COLUMNS = 4;
    const COMPACT_THRESHOLD_SCORE = 5;       // panels below this score go compact
    const COMPACT_THRESHOLD_DAYS = 3;        // panels unused for 3+ days go compact
    const MIN_INTERACTION_DURATION_MS = 200;  // ignore fly-by hovers
    let panels = [];
    let panelMap = new Map();        // id -> panel
    let dirty = false;              // dirty flag: true when state changes, triggers layout
    let layoutPending = false;
    let draggingPanelId = null;     // lock-step: if dragging, suppress auto-layout
    let observers = new Map();      // id -> IntersectionObserver
    let viewTimers = new Map();     // id -> {start, accumulated}
    let totalEvents = 0;
    // --- Persistence ---
    function loadState() {
      try {
        const raw = localStorage.getItem('adaptive_dashboard_v1');
        if (raw) {
          const saved = JSON.parse(raw);
          if (saved.panels && Array.isArray(saved.panels)) {
            panels = saved.panels.map(p => ({...p}));
          }
          totalEvents = saved.totalEvents || 0;
        }
      } catch(e) { /* corrupted, use defaults */ }
      if (panels.length === 0) {
        panels = [
          { id: 'cpu',      title: 'CPU Usage',       content: 'System processor load',           value: '34%',  freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'memory',   title: 'Memory',           content: 'RAM consumption over time',        value: '12.4G', freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'disk',     title: 'Disk I/O',         content: 'Read/write throughput',            value: '82 MB/s', freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'network',  title: 'Network Traffic',  content: 'Inbound / outbound packets',       value: '1.2 Gb/s', freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'errors',   title: 'Error Rate',       content: 'Application errors per minute',    value: '0.4%',  freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'latency',  title: 'P95 Latency',      content: '95th percentile response time',    value: '142ms', freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'requests', title: 'Requests/sec',     content: 'HTTP requests per second',         value: '2.3k',  freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
          { id: 'users',    title: 'Active Users',     content: 'Concurrent active sessions',       value: '847',   freq: 0, dur: 0, last: 0, locked: false, colSpan: 1 },
        ];
      }
      panelMap = new Map(panels.map(p => [p.id, p]));
      markDirty();
    }
    function saveState() {
      const data = { panels: panels.map(p => ({...p})), totalEvents };
      localStorage.setItem('adaptive_dashboard_v1', JSON.stringify(data));
    }
    function resetAll() {
      panels.forEach(p => { p.freq = 0; p.dur = 0; p.last = 0; p.locked = false; p.colSpan = 1; });
      totalEvents = 0;
      dirty = true;
      saveState();
      renderAll();
    }
    // --- Scoring ---
    function daysSince(ts) { return ts ? (Date.now() - ts) / 86400000 : 999; }
    function recencyFactor(days) {
      // Math.exp(-days * Math.LN2 / halfLifeDays)
      return Math.exp(-days * Math.LN2 / HALF_LIFE_DAYS);
    }
    function scorePanel(p) {
      const days = daysSince(p.last);
      const avgDur = p.freq > 0 ? (p.dur / p.freq) / 1000 : 0; // avg seconds per interaction
      const rec = recencyFactor(days);
      const raw = (p.freq + 1) * (avgDur + 0.5) * (rec + 0.01);
      return Math.round(raw * 100) / 100;
    }
    // --- Ranking ---
    function rankedPanels() {
      return [...panels]
        .map(p => ({...p, _score: scorePanel(p)}))
        .sort((a, b) => b._score - a._score)
        .map((p, i) => ({...p, _rank: i + 1}));
    }
    // --- Layout assignment ---
    // Top N panels (rank 1-3) get 2-col span, rest get 1-col. Compact if score < threshold and rank > 4.
    function computeLayout() {
      if (draggingPanelId) return; // lock-step: suppress layout during drag
      const ranked = rankedPanels();
      const mainPanels = [];
      const compactPanels = [];
      for (const p of ranked) {
        if (p.locked) {
          mainPanels.push(p);
          continue;
        }
        const days = daysSince(p.last);
        if (p._score < COMPACT_THRESHOLD_SCORE && p._rank > 3) {
          compactPanels.push(p);
        } else if (days > COMPACT_THRESHOLD_DAYS && p._rank > 3 && p.freq < 3) {
          compactPanels.push(p);
        } else {
          // Assign colSpan based on rank
          p.colSpan = (p._rank <= 3) ? 2 : 1;
          p._cols = p.colSpan;
          mainPanels.push(p);
        }
      }
      // Dedup: ensure compact zone has no duplicates of main panels by id
      const mainIds = new Set(mainPanels.map(p => p.id));
      const dedupedCompact = [];
      const seenCompact = new Set();
      for (const p of compactPanels) {
        if (!mainIds.has(p.id) && !seenCompact.has(p.id)) {
          seenCompact.add(p.id);
          dedupedCompact.push(p);
        }
      }
      return { main: mainPanels, compact: dedupedCompact, allRanked: ranked };
    }
    // --- Render ---
    function renderAll() {
      const layout = computeLayout();
      if (!layout) return;
      const dashboard = document.getElementById('dashboard');
      const compactGrid = document.getElementById('compact-grid');
      // Build fragment for main panels
      const df = document.createDocumentFragment();
      for (const p of layout.main) {
        const el = buildPanelDOM(p);
        df.appendChild(el);
      }
      // Targeted DOM: only replace if different
      if (dashboard.children.length !== layout.main.length ||
          !arraysEqualById(dashboard, layout.main)) {
        dashboard.innerHTML = '';
        dashboard.appendChild(df);
        attachObservers(layout.main);
      }
      // Compact zone
      const cf = document.createDocumentFragment();
      for (const p of layout.compact) {
        const cel = buildCompactDOM(p);
        cf.appendChild(cel);
      }
      if (compactGrid.children.length !== layout.compact.length ||
          !arraysEqualById(compactGrid, layout.compact)) {
        compactGrid.innerHTML = '';
        compactGrid.appendChild(cf);
        attachCompactObservers(layout.compact);
      }
      // Update grid column spans
      for (let i = 0; i < dashboard.children.length; i++) {
        const child = dashboard.children[i];
        const pid = child.dataset.panelId;
        const p = panelMap.get(pid);
        if (p && p.colSpan > 1) {
          child.style.gridColumn = `span ${Math.min(p.colSpan, COLUMNS)}`;
        } else {
          child.style.gridColumn = '';
        }
      }
      updateStats(layout);
      dirty = false;
      layoutPending = false;
    }
    function arraysEqualById(container, panelList) {
      if (container.children.length !== panelList.length) return false;
      for (let i = 0; i < container.children.length; i++) {
        if (container.children[i].dataset.panelId !== panelList[i].id) return false;
      }
      return true;
    }
    function buildPanelDOM(p) {
      const div = document.createElement('div');
      div.className = 'panel' + (p.locked ? ' locked' : '');
      div.dataset.panelId = p.id;
      div.draggable = true;
      const score = scorePanel(p);
      div.innerHTML = `
        <div class="panel-header">
          <span class="panel-title">${esc(p.title)}</span>
          <span class="panel-rank">#${p._rank || p._rank} · score ${score.toFixed(1)}</span>
        </div>
        <div class="panel-body">${esc(p.content)}</div>
        <div class="panel-score">${esc(p.value)}</div>
        <div class="panel-actions">
          <button class="btn-lock" data-action="lock" data-id="${esc(p.id)}">${p.locked ? 'Unlock' : 'Lock'}</button>
          <button data-action="promote" data-id="${esc(p.id)}">Promote</button>
          <button data-action="demote" data-id="${esc(p.id)}">Demote</button>
        </div>`;
      // Drag handlers
      div.addEventListener('dragstart', onDragStart);
      div.addEventListener('dragend', onDragEnd);
      div.addEventListener('dragover', e => e.preventDefault());
      div.addEventListener('drop', onDrop);
      // Click handlers
      div.addEventListener('click', onPanelClick);
      div.addEventListener('mouseenter', onPanelEnter);
      return div;
    }
    function buildCompactDOM(p) {
      const div = document.createElement('div');
      div.className = 'compact-panel';
      div.dataset.panelId = p.id;
      const score = scorePanel(p);
      div.innerHTML = `<span class="cp-title">${esc(p.title)}</span><span class="cp-score">${score.toFixed(1)}</span>`;
      div.addEventListener('click', () => promotePanel(p.id));
      div.addEventListener('mouseenter', () => recordInteraction(p.id, 'compact'));
      return div;
    }
    function esc(s) {
      const d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }
    function attachObservers(mainPanels) {
      // Tear down old observers
      for (const [id, obs] of observers) {
        obs.disconnect();
      }
      observers.clear();
      const observerOptions = { threshold: [0, 0.5, 1.0] };
      for (const p of mainPanels) {
        const el = document.querySelector(`.panel[data-panel-id="${p.id}"]`);
        if (!el) continue;
        const obs = new IntersectionObserver((entries) => {
          for (const entry of entries) {
            const pid = entry.target.dataset.panelId;
            if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
              startViewTimer(pid);
            } else {
              stopViewTimer(pid);
            }
          }
        }, observerOptions);
        obs.observe(el);
        observers.set(p.id, obs);
      }
    }
    function attachCompactObservers(compactPanels) {
      // Compact panels get simple mouseenter tracking via inline handler, no IntersectionObserver needed
    }
    // --- View duration tracking ---
    function startViewTimer(pid) {
      if (viewTimers.has(pid)) return;
      viewTimers.set(pid, { start: Date.now(), accumulated: 0 });
    }
    function stopViewTimer(pid) {
      const t = viewTimers.get(pid);
      if (!t) return;
      const elapsed = Date.now() - t.start + t.accumulated;
      viewTimers.delete(pid);
      if (elapsed < MIN_INTERACTION_DURATION_MS) return;
      const p = panelMap.get(pid);
      if (!p) return;
      p.dur = (p.dur || 0) + elapsed;
      p.last = Date.now();
      markDirty();
      scheduleSave();
    }
    // --- Interaction tracking ---
    function recordInteraction(pid, source) {
      const p = panelMap.get(pid);
      if (!p) return;
      p.freq = (p.freq || 0) + 1;
      p.last = Date.now();
      totalEvents++;
      markDirty();
      scheduleSave();
    }
    function onPanelClick(e) {
      const pid = e.currentTarget.dataset.panelId;
      if (e.target.dataset.action === 'lock') {
        toggleLock(pid);
        return;
      }
      if (e.target.dataset.action === 'promote') {
        promotePanel(pid);
        return;
      }
      if (e.target.dataset.action === 'demote') {
        demotePanel(pid);
        return;
      }
      recordInteraction(pid, 'click');
    }
    function onPanelEnter(e) {
      const pid = e.currentTarget.dataset.panelId;
      recordInteraction(pid, 'hover');
    }
    // --- Manual override: lock / promote / demote ---
    function toggleLock(pid) {
      const p = panelMap.get(pid);
      if (!p) return;
      p.locked = !p.locked;
      recordInteraction(pid, 'lock-toggle');
      markDirty();
      scheduleRender();
    }
    function promotePanel(pid) {
      const p = panelMap.get(pid);
      if (!p) return;
      p.freq += 3;
      p.last = Date.now();
      p.locked = false;
      p.colSpan = 2;
      markDirty();
      scheduleRender();
    }
    function demotePanel(pid) {
      const p = panelMap.get(pid);
      if (!p) return;
      p.freq = Math.max(0, (p.freq || 0) - 2);
      p.last = Date.now();
      p.locked = false;
      p.colSpan = 1;
      markDirty();
      scheduleRender();
    }
    // --- Drag & Drop (lock-step protocol) ---
    let dragSourceId = null;
    function onDragStart(e) {
      dragSourceId = e.currentTarget.dataset.panelId;
      draggingPanelId = dragSourceId;
      e.currentTarget.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', dragSourceId);
    }
    function onDragEnd(e) {
      e.currentTarget.classList.remove('dragging');
      draggingPanelId = null;
      // After drag, lock the panel at its new position
      if (dragSourceId) {
        const p = panelMap.get(dragSourceId);
        if (p) {
          p.locked = true;
          recordInteraction(dragSourceId, 'drag-drop');
          markDirty();
          scheduleRender();
          scheduleSave();
        }
      }
      dragSourceId = null;
    }
    function onDrop(e) {
      e.preventDefault();
      const targetId = e.currentTarget.dataset.panelId;
      const sourceId = e.dataTransfer.getData('text/plain');
      if (!sourceId || !targetId || sourceId === targetId) return;
      // Swap positions in the panels array
      const srcIdx = panels.findIndex(p => p.id === sourceId);
      const tgtIdx = panels.findIndex(p => p.id === targetId);
      if (srcIdx === -1 || tgtIdx === -1) return;
      [panels[srcIdx], panels[tgtIdx]] = [panels[tgtIdx], panels[srcIdx]];
      // Lock both after swap
      panels[srcIdx].locked = true;
      panels[tgtIdx].locked = true;
      panels[srcIdx].last = Date.now();
      panels[tgtIdx].last = Date.now();
      recordInteraction(sourceId, 'swap');
      recordInteraction(targetId, 'swap');
      markDirty();
      scheduleRender();
      scheduleSave();
    }
    // --- Dirty flag + adaptive scheduling ---
    let renderTimeout = null;
    let saveTimeout = null;
    let idleSince = Date.now();
    function markDirty() { dirty = true; }
    function scheduleRender() {
      if (!dirty) return;
      if (layoutPending) return;
      if (draggingPanelId) return; // lock-step: no layout during drag
      layoutPending = true;
      clearTimeout(renderTimeout);
      // Adaptive: if recent interaction, render immediately; otherwise back off
      const idleTime = Date.now() - idleSince;
      const delay = idleTime < 2000 ? 50 : idleTime < 10000 ? 300 : 1000;
      renderTimeout = setTimeout(() => {
        if (dirty && !draggingPanelId) {
          renderAll();
          saveState();
          idleSince = Date.now();
        }
        layoutPending = false;
      }, delay);
    }
    function scheduleSave() {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(saveState, 500);
    }
    // --- Stats ---
    function updateStats(layout) {
      document.getElementById('stat-events').textContent = totalEvents;
      document.getElementById('stat-visible').textContent = layout.main.length;
      document.getElementById('stat-compact').textContent = layout.compact.length;
      document.getElementById('stat-locked').textContent = panels.filter(p => p.locked).length;
      document.getElementById('stat-last').textContent = new Date().toLocaleTimeString();
    }
    // --- Simulate some usage so panels have scores on first load ---
    function seedInitialData() {
      let hasData = panels.some(p => p.freq > 0);
      if (hasData) return;
      const seeds = [
        { id: 'cpu',      freq: 12, dur: 45000 },
        { id: 'memory',   freq: 8,  dur: 32000 },
        { id: 'disk',     freq: 3,  dur: 8000 },
        { id: 'network',  freq: 6,  dur: 22000 },
        { id: 'errors',   freq: 15, dur: 60000 },
        { id: 'latency',  freq: 10, dur: 38000 },
        { id: 'requests', freq: 5,  dur: 15000 },
        { id: 'users',    freq: 4,  dur: 11000 },
      ];
      const now = Date.now();
      for (const s of seeds) {
        const p = panelMap.get(s.id);
        if (p) {
          p.freq = s.freq;
          p.dur = s.dur;
          p.last = now - Math.floor(Math.random() * 4 * 86400000); // 0-4 days ago
        }
      }
      totalEvents = seeds.reduce((sum, s) => sum + s.freq, 0);
      markDirty();
      saveState();
    }
    // --- Buttons ---
    document.getElementById('btn-reset').addEventListener('click', resetAll);
    document.getElementById('btn-unlock-all').addEventListener('click', () => {
      panels.forEach(p => { p.locked = false; });
      markDirty();
      scheduleRender();
      saveState();
    });
    document.getElementById('btn-force-layout').addEventListener('click', () => {
      markDirty();
      renderAll();
      saveState();
    });
    // --- Visibility change: pause/resume tracking ---
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // Stop all view timers
        for (const [id, t] of viewTimers) {
          t.accumulated += Date.now() - t.start;
          t.start = 0;
        }
      } else {
        // Resume timers for visible panels
        for (const [id, t] of viewTimers) {
          if (t.start === 0) t.start = Date.now();
        }
        idleSince = Date.now();
      }
    });
    // --- Init ---
    loadState();
    seedInitialData();
    renderAll();
    saveState();
    // Mark initial render time
    document.getElementById('stat-last').textContent = new Date().toLocaleTimeString();
    // Expose API for external testing
    window.adaptiveDashboard = {
      getPanels: () => panels,
      getScore: (id) => scorePanel(panelMap.get(id)),
      getRanked: () => rankedPanels(),
      reset: resetAll,
      promote: promotePanel,
      demote: demotePanel,
      toggleLock,
      forceLayout: () => { markDirty(); renderAll(); },
      getState: () => ({ dirty, draggingPanelId, layoutPending, totalEvents })
    };
  })();
</script>