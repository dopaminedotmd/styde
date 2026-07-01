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
    --surface2: #22263a;
    --border: #2a2e3f;
    --text: #e1e4ed;
    --text2: #9298aa;
    --accent: #6c8cff;
    --accent2: #4ade80;
    --warn: #f59e0b;
    --danger: #ef4444;
    --radius: 10px;
    --gap: 12px;
    --transition: 350ms cubic-bezier(0.4, 0, 0.2, 1);
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 16px;
    transition: background var(--transition);
  }
  body.reduced-motion * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  body.low-power .heatmap-overlay { display: none; }
  body.low-power .panel-glow { opacity: 0; }
  .toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: var(--gap);
    flex-wrap: wrap;
  }
  .toolbar-title {
    font-weight: 700;
    font-size: 16px;
    letter-spacing: -0.01em;
    margin-right: auto;
    color: var(--accent);
  }
  .toolbar-btn {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text2);
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    transition: all var(--transition);
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .toolbar-btn:hover { background: var(--border); color: var(--text); }
  .toolbar-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .toolbar-badge {
    background: var(--surface2);
    color: var(--text2);
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 20px;
    border: 1px solid var(--border);
  }
  .dashboard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(140px, auto);
    gap: var(--gap);
    transition: grid-template-columns var(--transition);
  }
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    position: relative;
    transition: all var(--transition);
    cursor: grab;
    display: flex;
    flex-direction: column;
  }
  .panel:active { cursor: grabbing; }
  .panel.rank-high { grid-column: span 2; grid-row: span 2; border-color: var(--accent2); }
  .panel.rank-mid { grid-column: span 1; grid-row: span 1; }
  .panel.rank-low { grid-column: span 1; grid-row: span 1; opacity: 0.78; transform: scale(0.97); }
  .panel.compact {
    grid-column: span 1;
    grid-row: span 1;
    max-height: 100px;
    opacity: 0.65;
  }
  .panel.compact .panel-body { display: none; }
  .panel.compact .panel-preview { display: flex; }
  .panel.collapsed {
    grid-column: span 1;
    grid-row: span 1;
    max-height: 48px;
    opacity: 0.5;
  }
  .panel.collapsed .panel-body, .panel.collapsed .panel-preview { display: none; }
  .panel.locked { border-color: var(--warn); }
  .panel.locked::after {
    content: 'locked';
    position: absolute;
    top: 6px;
    right: 8px;
    font-size: 10px;
    color: var(--warn);
    background: rgba(245, 158, 11, 0.15);
    padding: 1px 6px;
    border-radius: 3px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }
  .panel.dragging { opacity: 0.5; z-index: 10; transform: scale(1.02); box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    font-weight: 600;
    font-size: 13px;
    user-select: none;
    flex-shrink: 0;
  }
  .panel-icon { font-size: 15px; }
  .panel-title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .panel-actions { display: flex; gap: 4px; }
  .panel-action {
    background: none;
    border: none;
    color: var(--text2);
    cursor: pointer;
    padding: 3px 6px;
    border-radius: 4px;
    font-size: 12px;
    transition: all 0.15s;
  }
  .panel-action:hover { background: var(--border); color: var(--text); }
  .panel-action.lock-active { color: var(--warn); }
  .panel-body {
    padding: 14px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 60px;
  }
  .panel-preview {
    display: none;
    padding: 8px 14px;
    font-size: 11px;
    color: var(--text2);
    align-items: center;
    gap: 8px;
  }
  .metric-value {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
  }
  .metric-label {
    font-size: 12px;
    color: var(--text2);
    margin-top: 4px;
  }
  .metric-spark {
    margin-top: 8px;
    height: 40px;
    width: 100%;
  }
  .metric-spark svg { width: 100%; height: 100%; }
  .heatmap-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 1000;
    opacity: 0.12;
    transition: opacity var(--transition);
  }
  .heatmap-cell {
    position: absolute;
    border-radius: 8px;
    transition: all 1.5s ease-out;
  }
  .more-section {
    grid-column: 1 / -1;
    border-top: 1px dashed var(--border);
    padding-top: 12px;
    margin-top: 4px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  .more-chip {
    background: var(--surface2);
    border: 1px solid var(--border);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: var(--text2);
    cursor: pointer;
    transition: all 0.2s;
  }
  .more-chip:hover { background: var(--border); color: var(--text); }
  @media (max-width: 900px) {
    .dashboard { grid-template-columns: repeat(2, 1fr); }
    .panel.rank-high { grid-column: span 2; }
  }
  @media (max-width: 520px) {
    .dashboard { grid-template-columns: 1fr; }
    .panel.rank-high, .panel.rank-mid, .panel.rank-low { grid-column: span 1; }
  }
</style>
</head>
<body>
<div class="toolbar">
  <span class="toolbar-title">Adaptive Dashboard</span>
  <span class="toolbar-badge" id="sessionBadge">session 1</span>
  <button class="toolbar-btn" id="btnReset" title="Reset all tracking data">Reset Layout</button>
  <button class="toolbar-btn" id="btnCompact" title="Auto-compact low-usage panels">Auto-Compact</button>
  <button class="toolbar-btn" id="btnLowPower" title="Toggle low-power mode">Low Power</button>
  <button class="toolbar-btn" id="btnHeatmap" title="Toggle attention heatmap">Heatmap</button>
  <span class="toolbar-badge" id="eventLog" style="font-size:10px;max-width:200px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"></span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="heatmap-overlay" id="heatmapOverlay" style="display:none;"></div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_layout_v1';
  const DECAY_HALF_LIFE_MS = 30 * 60 * 1000; /* 30 min half-life for recency decay */
  const VIEW_THRESHOLD_MS = 800; /* minimum visible ms to count as a view */
  const COMPACT_THRESHOLD = 0.20; /* panels below 20% of median score -> compact */
  const COLLAPSE_THRESHOLD = 0.05; /* panels below 5% of max score -> collapsed */
  const DEBOUNCE_RECOMPUTE_MS = 400;
  const PANEL_DEFS = [
    { id: 'revenue',     title: 'Revenue',         icon: '\u{1F4B0}', type: 'metric', value: 84720, unit: 'USD', color: '#4ade80' },
    { id: 'users',       title: 'Active Users',    icon: '\u{1F465}', type: 'metric', value: 12453, unit: '',   color: '#6c8cff' },
    { id: 'conversion',  title: 'Conversion Rate', icon: '\u{1F3AF}', type: 'metric', value: 3.82,  unit: '%',  color: '#f59e0b' },
    { id: 'churn',       title: 'Churn Rate',      icon: '\u{1F4C9}', type: 'metric', value: 1.24,  unit: '%',  color: '#ef4444' },
    { id: 'latency',     title: 'API Latency',     icon: '\u{26A1}',  type: 'metric', value: 42,    unit: 'ms', color: '#a78bfa' },
    { id: 'errors',      title: 'Error Rate',      icon: '\u{274C}',  type: 'metric', value: 0.12,  unit: '%',  color: '#ef4444' },
    { id: 'throughput',  title: 'Throughput',      icon: '\u{1F4E6}', type: 'metric', value: 9832,  unit: '/s', color: '#38bdf8' },
    { id: 'uptime',      title: 'Uptime',          icon: '\u{2705}',  type: 'metric', value: 99.97, unit: '%',  color: '#4ade80' },
  ];
  let state = {
    panels: {},
    sessionCount: 1,
    lowPower: false,
    showHeatmap: false,
    reducedMotion: false,
    lockedPanels: {}
  };
  function defaultPanelState(id) {
    return {
      id: id,
      viewCount: 0,
      totalViewMs: 0,
      interactCount: 0,
      lastInteractTs: 0,
      collapsed: false,
      compact: false,
      locked: false,
      manualRank: null,
    };
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state.sessionCount = (parsed.sessionCount || 0) + 1;
        state.lowPower = parsed.lowPower || false;
        state.reducedMotion = parsed.reducedMotion || false;
        state.lockedPanels = parsed.lockedPanels || {};
        for (const pid of PANEL_DEFS.map(p => p.id)) {
          if (parsed.panels && parsed.panels[pid]) {
            state.panels[pid] = { ...defaultPanelState(pid), ...parsed.panels[pid] };
            state.panels[pid].locked = !!state.lockedPanels[pid];
          } else {
            state.panels[pid] = defaultPanelState(pid);
          }
        }
      }
    } catch (e) { /* ignore corrupt storage */ }
    for (const pid of PANEL_DEFS.map(p => p.id)) {
      if (!state.panels[pid]) state.panels[pid] = defaultPanelState(pid);
    }
  }
  function saveState() {
    const persist = {
      panels: {},
      sessionCount: state.sessionCount,
      lowPower: state.lowPower,
      reducedMotion: state.reducedMotion,
      lockedPanels: state.lockedPanels,
    };
    for (const pid of Object.keys(state.panels)) {
      const p = state.panels[pid];
      persist.panels[pid] = {
        viewCount: p.viewCount,
        totalViewMs: p.totalViewMs,
        interactCount: p.interactCount,
        lastInteractTs: p.lastInteractTs,
      };
    }
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(persist)); } catch (e) {}
  }
  function computeAttentionScore(panel, now) {
    const recencyMs = now - panel.lastInteractTs;
    const recencyWeight = Math.pow(0.5, recencyMs / DECAY_HALF_LIFE_MS);
    const frequencyWeight = Math.log2(panel.interactCount + 2);
    const durationWeight = Math.log2((panel.totalViewMs / 1000) + 2);
    return panel.viewCount * frequencyWeight * durationWeight * recencyWeight;
  }
  function rankPanels() {
    const now = Date.now();
    const scored = PANEL_DEFS.map(def => {
      const p = state.panels[def.id] || defaultPanelState(def.id);
      if (p.locked && p.manualRank !== null) {
        return { id: def.id, score: p.manualRank, locked: true };
      }
      return { id: def.id, score: computeAttentionScore(p, now), locked: false };
    });
    scored.sort((a, b) => {
      if (a.locked && b.locked) return (a.score - b.score);
      if (a.locked) return -1;
      if (b.locked) return 1;
      return b.score - a.score;
    });
    const maxScore = Math.max(1, scored[0]?.score || 0);
    const scores = scored.filter(s => !s.locked).map(s => s.score);
    const median = scores.length ? scores.sort((a,b) => a-b)[Math.floor(scores.length / 2)] : 1;
    const ranks = {};
    let pos = 0;
    for (const item of scored) {
      const ratio = maxScore > 0 ? item.score / maxScore : 0;
      let tier;
      if (item.locked) {
        tier = 'locked';
      } else if (ratio >= 0.50) {
        tier = 'high';
      } else if (ratio >= 0.15) {
        tier = 'mid';
      } else if (ratio >= COLLAPSE_THRESHOLD) {
        tier = 'low';
      } else {
        tier = 'collapsed';
      }
      ranks[item.id] = { tier, score: item.score, position: pos++, locked: item.locked };
    }
    return ranks;
  }
  let viewTimers = {};
  let observer = null;
  function startViewTimer(panelId) {
    if (viewTimers[panelId]) return;
    viewTimers[panelId] = Date.now();
  }
  function stopViewTimer(panelId) {
    if (!viewTimers[panelId]) return;
    const elapsed = Date.now() - viewTimers[panelId];
    if (elapsed >= VIEW_THRESHOLD_MS) {
      state.panels[panelId].totalViewMs += elapsed;
      state.panels[panelId].viewCount += 1;
      logEvent(panelId + ' viewed ' + Math.round(elapsed/1000) + 's');
    }
    delete viewTimers[panelId];
  }
  function setupIntersectionObserver() {
    if (observer) observer.disconnect();
    observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const panelId = entry.target.dataset.panelId;
        if (!panelId) continue;
        if (entry.isIntersecting) {
          startViewTimer(panelId);
        } else {
          stopViewTimer(panelId);
        }
      }
    }, { threshold: 0.5 });
  }
  function logEvent(msg) {
    const el = document.getElementById('eventLog');
    if (el) { el.textContent = msg; }
  }
  function trackInteraction(panelId, type) {
    const now = Date.now();
    state.panels[panelId].interactCount += 1;
    state.panels[panelId].lastInteractTs = now;
    logEvent(panelId + ' ' + type);
    saveState();
    scheduleRecompute();
  }
  let recomputeTimer = null;
  function scheduleRecompute() {
    if (recomputeTimer) clearTimeout(recomputeTimer);
    recomputeTimer = setTimeout(() => {
      recomputeTimer = null;
      renderDashboard();
    }, DEBOUNCE_RECOMPUTE_MS);
  }
  function buildSparkline(values, color) {
    if (!values || values.length < 2) values = [0, 0];
    const w = 120, h = 36;
    const min = Math.min(...values), max = Math.max(...values);
    const range = max - min || 1;
    const points = values.map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    const area = points + ' ' + w.toFixed(1) + ',' + (h).toFixed(1) + ' 0,' + (h).toFixed(1);
    return '<svg viewBox="0 0 ' + w + ' ' + h + '"><defs><linearGradient id="g' + color.replace('#','') + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="' + color + '" stop-opacity="0.25"/><stop offset="100%" stop-color="' + color + '" stop-opacity="0.02"/></linearGradient></defs><polygon fill="url(#g' + color.replace('#','') + ')" points="' + area + '"/><polyline fill="none" stroke="' + color + '" stroke-width="1.6" points="' + points + '"/></svg>';
  }
  function generateMockValues(seed, count) {
    const vals = [];
    let v = 30 + (seed * 7) % 40;
    for (let i = 0; i < count; i++) {
      v += (Math.sin(i * 0.7 + seed) * 8) + (Math.random() - 0.5) * 4;
      vals.push(Math.max(0, Math.round(v * 10) / 10));
    }
    return vals;
  }
  function renderDashboard() {
    const container = document.getElementById('dashboard');
    const ranks = rankPanels();
    const now = Date.now();
    const orderedIds = Object.entries(ranks)
      .sort(([,a], [,b]) => a.position - b.position)
      .map(([id]) => id);
    const existingEls = {};
    for (const child of container.children) {
      if (child.dataset.panelId) existingEls[child.dataset.panelId] = child;
    }
    const fragment = document.createDocumentFragment();
    const moreIds = [];
    for (const pid of orderedIds) {
      const def = PANEL_DEFS.find(d => d.id === pid);
      if (!def) continue;
      const rank = ranks[pid];
      const pstate = state.panels[pid];
      if (rank.tier === 'collapsed' && !pstate.locked) {
        moreIds.push(pid);
        continue;
      }
      let el = existingEls[pid];
      if (!el) {
        el = document.createElement('div');
        el.className = 'panel';
        el.dataset.panelId = pid;
        el.draggable = true;
        el.innerHTML =
          '<div class="panel-header">' +
            '<span class="panel-icon">' + def.icon + '</span>' +
            '<span class="panel-title">' + def.title + '</span>' +
            '<div class="panel-actions">' +
              '<button class="panel-action lock-btn" title="Lock/unlock position">lock</button>' +
              '<button class="panel-action compact-btn" title="Toggle compact">-</button>' +
            '</div>' +
          '</div>' +
          '<div class="panel-body"></div>' +
          '<div class="panel-preview">' +
            '<span class="panel-icon">' + def.icon + '</span>' +
            '<span>' + def.title + ' &mdash; click to expand</span>' +
          '</div>';
      }
      el.className = 'panel';
      if (rank.tier === 'high') el.classList.add('rank-high');
      else if (rank.tier === 'mid') el.classList.add('rank-mid');
      else if (rank.tier === 'low') el.classList.add('rank-low');
      if (pstate.locked) el.classList.add('locked');
      if (pstate.compact && rank.tier !== 'high') el.classList.add('compact');
      const body = el.querySelector('.panel-body');
      const sparkVals = generateMockValues(def.id.charCodeAt(0) + def.id.charCodeAt(1), 20);
      body.innerHTML =
        '<div style="text-align:center;">' +
          '<div class="metric-value" style="color:' + def.color + '">' +
            (def.type === 'metric' && def.unit === '%' ? def.value.toFixed(2) : def.value.toLocaleString()) +
            '<span style="font-size:16px;font-weight:500;margin-left:4px;">' + def.unit + '</span>' +
          '</div>' +
          '<div class="metric-label">' + def.title + ' &middot; score: ' + rank.score.toFixed(1) + '</div>' +
          '<div class="metric-spark">' + buildSparkline(sparkVals, def.color) + '</div>' +
        '</div>';
      const lockBtn = el.querySelector('.lock-btn');
      lockBtn.textContent = pstate.locked ? 'unlock' : 'lock';
      lockBtn.className = 'panel-action lock-btn' + (pstate.locked ? ' lock-active' : '');
      el.querySelector('.compact-btn').textContent = pstate.compact ? '+' : '-';
      fragment.appendChild(el);
      delete existingEls[pid];
    }
    for (const leftover of Object.values(existingEls)) {
      const pid = leftover.dataset.panelId;
      if (pid && viewTimers[pid]) stopViewTimer(pid);
      leftover.remove();
    }
    if (moreIds.length > 0) {
      const moreSection = document.createElement('div');
      moreSection.className = 'more-section';
      moreSection.style.gridColumn = '1 / -1';
      for (const pid of moreIds) {
        const def = PANEL_DEFS.find(d => d.id === pid);
        const chip = document.createElement('span');
        chip.className = 'more-chip';
        chip.textContent = (def ? def.icon + ' ' + def.title : pid);
        chip.dataset.panelId = pid;
        chip.title = 'Click to restore';
        moreSection.appendChild(chip);
      }
      fragment.appendChild(moreSection);
    }
    container.innerHTML = '';
    container.appendChild(fragment);
    setupIntersectionObserver();
    for (const child of container.querySelectorAll('.panel')) {
      observer.observe(child);
    }
    bindEvents(container);
    updateHeatmap();
    document.getElementById('sessionBadge').textContent = 'session ' + state.sessionCount;
    saveState();
  }
  function bindEvents(container) {
    container.querySelectorAll('.panel').forEach(panel => {
      const pid = panel.dataset.panelId;
      panel.onclick = (e) => {
        if (e.target.closest('.panel-action')) return;
        trackInteraction(pid, 'click');
      };
      panel.querySelector('.lock-btn').onclick = (e) => {
        e.stopPropagation();
        const p = state.panels[pid];
        p.locked = !p.locked;
        if (p.locked) {
          state.lockedPanels[pid] = true;
          const ranks = rankPanels();
          p.manualRank = ranks[pid]?.position ?? 0;
        } else {
          delete state.lockedPanels[pid];
          p.manualRank = null;
        }
        trackInteraction(pid, p.locked ? 'locked' : 'unlocked');
        renderDashboard();
      };
      panel.querySelector('.compact-btn').onclick = (e) => {
        e.stopPropagation();
        state.panels[pid].compact = !state.panels[pid].compact;
        trackInteraction(pid, state.panels[pid].compact ? 'compacted' : 'expanded');
        renderDashboard();
      };
      panel.addEventListener('dragstart', (e) => {
        panel.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', pid);
      });
      panel.addEventListener('dragend', (e) => {
        panel.classList.remove('dragging');
        const target = document.elementFromPoint(e.clientX, e.clientY);
        const targetPanel = target?.closest('.panel');
        if (targetPanel && targetPanel !== panel) {
          const targetId = targetPanel.dataset.panelId;
          state.panels[pid].locked = true;
          state.panels[targetId].locked = true;
          state.lockedPanels[pid] = true;
          state.lockedPanels[targetId] = true;
          const ranks = rankPanels();
          state.panels[pid].manualRank = ranks[targetId]?.position ?? 0;
          state.panels[targetId].manualRank = ranks[pid]?.position ?? 0;
          trackInteraction(pid, 'dragged');
          renderDashboard();
        }
      });
      panel.addEventListener('dragover', (e) => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
      panel.addEventListener('drop', (e) => { e.preventDefault(); });
    });
    container.querySelectorAll('.more-chip').forEach(chip => {
      chip.onclick = () => {
        const pid = chip.dataset.panelId;
        if (pid && state.panels[pid]) {
          state.panels[pid].interactCount += 5;
          state.panels[pid].lastInteractTs = Date.now();
          state.panels[pid].viewCount += 1;
          logEvent(pid + ' restored from more');
          saveState();
          renderDashboard();
        }
      };
    });
  }
  function updateHeatmap() {
    const overlay = document.getElementById('heatmapOverlay');
    if (!state.showHeatmap) { overlay.style.display = 'none'; return; }
    overlay.style.display = 'block';
    overlay.innerHTML = '';
    const ranks = rankPanels();
    const panels = document.querySelectorAll('.panel');
    panels.forEach(panel => {
      const pid = panel.dataset.panelId;
      const rect = panel.getBoundingClientRect();
      const score = ranks[pid]?.score || 0;
      const maxScore = Math.max(1, ...Object.values(ranks).map(r => r.score));
      const intensity = Math.min(1, score / maxScore);
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      cell.style.left = rect.left + 'px';
      cell.style.top = rect.top + 'px';
      cell.style.width = rect.width + 'px';
      cell.style.height = rect.height + 'px';
      const r = Math.round(108 + intensity * 60);
      const g = Math.round(140 - intensity * 40);
      const b = Math.round(255 - intensity * 100);
      cell.style.background = 'rgba(' + r + ',' + g + ',' + b + ', ' + (0.3 + intensity * 0.4) + ')';
      overlay.appendChild(cell);
    });
  }
  function autoCompact() {
    const ranks = rankPanels();
    for (const pid of Object.keys(state.panels)) {
      if (state.panels[pid].locked) continue;
      const tier = ranks[pid]?.tier;
      if (tier === 'low' || tier === 'collapsed') {
        state.panels[pid].compact = true;
      } else if (tier === 'high') {
        state.panels[pid].compact = false;
      }
    }
    renderDashboard();
    logEvent('auto-compacted low-usage panels');
  }
  function resetAll() {
    state.panels = {};
    state.sessionCount = 1;
    state.lockedPanels = {};
    for (const pid of PANEL_DEFS.map(p => p.id)) {
      state.panels[pid] = defaultPanelState(pid);
    }
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
    renderDashboard();
    logEvent('layout reset');
  }
  function toggleLowPower() {
    state.lowPower = !state.lowPower;
    document.body.classList.toggle('low-power', state.lowPower);
    document.getElementById('btnLowPower').classList.toggle('active', state.lowPower);
    saveState();
  }
  function toggleHeatmap() {
    state.showHeatmap = !state.showHeatmap;
    document.getElementById('btnHeatmap').classList.toggle('active', state.showHeatmap);
    updateHeatmap();
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      for (const pid of Object.keys(viewTimers)) {
        stopViewTimer(pid);
      }
      if (!state.lowPower) {
        document.body.classList.add('low-power');
      }
    } else {
      if (!state.lowPower) {
        document.body.classList.remove('low-power');
      }
      setupIntersectionObserver();
      for (const child of document.querySelectorAll('.panel')) {
        observer.observe(child);
      }
      scheduleRecompute();
    }
  });
  let resizeDebounce = null;
  window.addEventListener('resize', () => {
    if (resizeDebounce) clearTimeout(resizeDebounce);
    resizeDebounce = setTimeout(() => {
      resizeDebounce = null;
      updateHeatmap();
    }, 200);
  });
  document.getElementById('btnReset').addEventListener('click', resetAll);
  document.getElementById('btnCompact').addEventListener('click', autoCompact);
  document.getElementById('btnLowPower').addEventListener('click', toggleLowPower);
  document.getElementById('btnHeatmap').addEventListener('click', toggleHeatmap);
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    state.reducedMotion = true;
    document.body.classList.add('reduced-motion');
  }
  loadState();
  if (state.lowPower) document.body.classList.add('low-power');
  if (state.reducedMotion) document.body.classList.add('reduced-motion');
  document.getElementById('btnLowPower').classList.toggle('active', state.lowPower);
  document.getElementById('btnHeatmap').classList.toggle('active', state.showHeatmap);
  renderDashboard();
  setInterval(() => {
    for (const pid of Object.keys(viewTimers)) {
      const elapsed = Date.now() - viewTimers[pid];
      if (elapsed >= VIEW_THRESHOLD_MS) {
        state.panels[pid].totalViewMs += elapsed;
        state.panels[pid].viewCount += 1;
        viewTimers[pid] = Date.now();
      }
    }
    saveState();
  }, 5000);
})();
</script>
</body>
</html>