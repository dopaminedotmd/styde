```html
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
  --surface-hover: #22263a;
  --border: #2a2e3d;
  --text: #e1e4ed;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #f44;
  --success: #4caf88;
  --warn: #f0a050;
  --gap: 12px;
  --radius: 10px;
  --transition: 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg); color: var(--text); font-family: var(--font);
  min-height: 100vh; overflow-x: hidden;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; border-bottom: 1px solid var(--border);
  background: var(--surface); position: sticky; top: 0; z-index: 100;
}
header h1 { font-size: 1.1rem; font-weight: 600; letter-spacing: -0.3px; }
header .badge { font-size: 0.7rem; color: var(--accent); background: var(--accent-glow); padding: 3px 10px; border-radius: 20px; }
.toolbar { display: flex; gap: 8px; }
.toolbar button {
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.78rem;
  transition: var(--transition);
}
.toolbar button:hover { background: var(--surface-hover); border-color: var(--accent); }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--gap); padding: 16px; transition: var(--transition);
}
.grid.compact-view { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
.panel {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px; cursor: grab; position: relative; overflow: hidden;
  transition: all var(--transition); min-height: 120px;
  display: flex; flex-direction: column;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 24px var(--accent-glow); }
.panel.dragging { opacity: 0.6; cursor: grabbing; z-index: 50; }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 32px var(--accent-glow); transform: scale(1.02); }
.panel.locked { border-left: 3px solid var(--accent); }
.panel.compact { padding: 10px; min-height: 80px; }
.panel.compact .panel-body { font-size: 0.72rem; }
.panel.compact .metric-value { font-size: 1.2rem; }
.panel.rank-1 { grid-column: span 2; grid-row: span 2; }
.panel.rank-2 { grid-column: span 2; }
.panel.rank-3 { grid-column: span 1; }
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px; font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px;
}
.panel-header .lock-icon { cursor: pointer; font-size: 0.85rem; opacity: 0.5; transition: opacity 0.2s; }
.panel-header .lock-icon:hover { opacity: 1; }
.panel-header .lock-icon.locked { opacity: 1; color: var(--accent); }
.metric-value { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; margin: 4px 0; }
.metric-sub { font-size: 0.72rem; color: var(--text-dim); }
.sparkline { width: 100%; height: 40px; margin-top: 8px; opacity: 0.7; }
.panel-footer {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: auto; padding-top: 8px; border-top: 1px solid var(--border);
  font-size: 0.68rem; color: var(--text-dim);
}
.usage-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 4px; }
.usage-dot.hot { background: var(--danger); }
.usage-dot.warm { background: var(--warn); }
.usage-dot.cold { background: var(--text-dim); }
.rank-badge {
  position: absolute; top: 8px; right: 8px; font-size: 0.6rem;
  background: var(--accent-glow); color: var(--accent);
  padding: 2px 8px; border-radius: 10px; opacity: 0.8;
}
.toast {
  position: fixed; bottom: 20px; right: 20px; background: var(--surface);
  border: 1px solid var(--accent); padding: 10px 18px; border-radius: 8px;
  font-size: 0.78rem; z-index: 999; opacity: 0; transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 200;
  display: flex; align-items: center; justify-content: center;
}
.modal {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; min-width: 320px; max-width: 90vw;
}
.modal h3 { margin-bottom: 12px; }
.modal table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
.modal th { text-align: left; color: var(--text-dim); padding: 6px 8px; border-bottom: 1px solid var(--border); }
.modal td { padding: 6px 8px; border-bottom: 1px solid var(--border); }
.modal button { margin-top: 12px; background: var(--accent); border: none; color: #fff; padding: 8px 18px; border-radius: 6px; cursor: pointer; }
.compact .panel-footer, .compact .sparkline, .compact .rank-badge { display: none; }
</style>
</head>
<body>
<header>
  <div style="display:flex;align-items:center;gap:10px;">
    <h1>Adaptive Metric Layout</h1>
    <span class="badge" id="modeBadge">LEARNING</span>
  </div>
  <div class="toolbar">
    <button id="btnReset" title="Reset tracking data">Reset</button>
    <button id="btnStats" title="View attention scores">Stats</button>
    <button id="btnCompact" title="Toggle compact low-rank panels">Compact</button>
    <button id="btnLockAll" title="Lock/unlock all">Lock All</button>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
  const STORAGE_KEY = 'adaptive_metric_layout_v1';
  const DECAY_DAYS = 7;
  const VIEW_THRESHOLD_MS = 800;
  const SAVE_DEBOUNCE = 2000;
  let panels = [
    { id:'revenue',        title:'Revenue',       value:'$48,293', sub:'+12.4% vs last month', spark:[20,35,30,45,55,40,60,70,65,80,75,90], initRank:1 },
    { id:'users',          title:'Active Users',  value:'2,847',   sub:'+5.7% this week',        spark:[100,120,115,140,160,155,180,200,190,210,220,230], initRank:2 },
    { id:'conversion',     title:'Conversion',    value:'3.82%',   sub:'+0.3pp vs baseline',      spark:[3.2,3.4,3.3,3.5,3.6,3.5,3.7,3.8,3.7,3.9,3.8,3.82], initRank:3 },
    { id:'latency',        title:'P95 Latency',   value:'182ms',   sub:'+8ms since deploy',        spark:[160,155,170,165,175,180,178,185,190,182,188,182], initRank:4 },
    { id:'errors',         title:'Error Rate',    value:'0.12%',   sub:'-0.04pp improvement',      spark:[0.2,0.18,0.19,0.15,0.16,0.14,0.13,0.12,0.11,0.13,0.12,0.12], initRank:5 },
    { id:'churn',          title:'Churn Rate',    value:'1.8%',    sub:'-0.2pp month-over-month',  spark:[2.2,2.1,2.0,1.9,1.95,1.85,1.8,1.82,1.78,1.8,1.79,1.8], initRank:6 },
    { id:'nps',            title:'NPS Score',     value:'72',      sub:'+3 points since Q1',       spark:[65,66,68,67,69,70,71,70,72,71,72,72], initRank:7 },
    { id:'sessions',       title:'Sessions',      value:'14.2K',   sub:'+8.1% daily avg',         spark:[10,11,10.5,12,13,12.5,14,13.8,14.5,14,14.2,14.2], initRank:8 },
    { id:'bounce',         title:'Bounce Rate',   value:'28.4%',   sub:'-1.2pp improvement',       spark:[32,31,30,29.5,29,28.8,28.5,28.2,28.4,28.3,28.5,28.4], initRank:9 },
    { id:'apdex',          title:'Apdex',         value:'0.94',    sub:'Excellent (>0.93)',        spark:[0.9,0.91,0.92,0.93,0.94,0.93,0.94,0.95,0.94,0.95,0.94,0.94], initRank:10 },
  ];
  let state = {
    tracking: {},
    locks: {},
    manualOrder: null,
    timers: {},
    saveTimer: null,
    showCompact: false,
  };
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const saved = JSON.parse(raw);
        if (saved.tracking) state.tracking = saved.tracking;
        if (saved.locks) state.locks = saved.locks;
        if (saved.manualOrder) state.manualOrder = saved.manualOrder;
        if (saved.showCompact !== undefined) state.showCompact = saved.showCompact;
      }
    } catch(e) { /* corrupt data, start fresh */ }
  }
  function saveState() {
    clearTimeout(state.saveTimer);
    state.saveTimer = setTimeout(() => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        tracking: state.tracking,
        locks: state.locks,
        manualOrder: state.manualOrder,
        showCompact: state.showCompact,
        savedAt: Date.now(),
      }));
      toast('Layout saved');
    }, SAVE_DEBOUNCE);
  }
  function now() { return Date.now(); }
  function decayMultiplier(ts) {
    const days = (now() - ts) / (1000 * 60 * 60 * 24);
    return Math.max(0.05, Math.exp(-days / DECAY_DAYS));
  }
  function computeAttention(panelId) {
    const t = state.tracking[panelId] || { views:0, totalMs:0, clicks:0, lastView:0 };
    if (t.views === 0) return 0;
    const freq = t.views;
    const dur = t.totalMs / Math.max(1, t.views) / 1000;
    const recency = decayMultiplier(t.lastView);
    const clickBonus = Math.log(1 + t.clicks);
    return (freq * dur * recency * (1 + clickBonus * 0.3));
  }
  function rankPanels() {
    const scored = panels.map(p => ({ id: p.id, score: computeAttention(p.id), initRank: p.initRank }));
    scored.sort((a, b) => b.score - a.score || a.initRank - b.initRank);
    const rankMap = {};
    scored.forEach((s, i) => { rankMap[s.id] = i + 1; });
    return { scored, rankMap };
  }
  function getPanelOrder() {
    if (state.manualOrder && state.manualOrder.length === panels.length) return [...state.manualOrder];
    const { scored } = rankPanels();
    return scored.map(s => s.id);
  }
  function trackEvent(panelId, type) {
    if (!state.tracking[panelId]) {
      state.tracking[panelId] = { views:0, totalMs:0, clicks:0, lastView:0 };
    }
    const t = state.tracking[panelId];
    if (type === 'view-start') {
      t.views++;
      t.lastView = now();
      state.timers[panelId] = now();
    }
    if (type === 'view-end' && state.timers[panelId]) {
      t.totalMs += now() - state.timers[panelId];
      delete state.timers[panelId];
    }
    if (type === 'click') {
      t.clicks++;
      t.lastView = now();
    }
    saveState();
    render();
  }
  function toggleLock(panelId) {
    state.locks[panelId] = !state.locks[panelId];
    if (!state.locks[panelId] && !state.manualOrder) {
      state.manualOrder = getPanelOrder();
    }
    saveState();
    render();
  }
  function movePanel(panelId, direction) {
    const order = getPanelOrder();
    const idx = order.indexOf(panelId);
    if (idx === -1) return;
    const target = direction === 'left' ? idx - 1 : idx + 1;
    if (target < 0 || target >= order.length) return;
    [order[idx], order[target]] = [order[target], order[idx]];
    state.manualOrder = order;
    state.locks[panelId] = true;
    if (direction === 'left' && target > 0) state.locks[order[target]] = true;
    if (direction === 'right' && target < order.length - 1) state.locks[order[target]] = true;
    saveState();
    render();
  }
  function resetTracking() {
    state.tracking = {};
    state.locks = {};
    state.manualOrder = null;
    state.timers = {};
    saveState();
    render();
    toast('Tracking data reset. Layout will re-learn.');
  }
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._timeout);
    el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
  }
  function renderSparkline(container, data) {
    const w = container.clientWidth || 200;
    const h = 40;
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    const points = data.map((v, i) => {
      const x = (i / (data.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return `${x},${y}`;
    }).join(' ');
    const area = `${points} ${w},${h} 0,${h}`;
    container.innerHTML = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="display:block;">
      <defs><linearGradient id="g-${container.dataset.id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
      </linearGradient></defs>
      <polygon points="${area}" fill="url(#g-${container.dataset.id})"/>
      <polyline points="${points}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
  }
  function render() {
    const grid = document.getElementById('grid');
    const order = getPanelOrder();
    const { rankMap } = rankPanels();
    const modeBadge = document.getElementById('modeBadge');
    const hasLocks = Object.values(state.locks).some(Boolean);
    modeBadge.textContent = hasLocks ? 'OVERRIDE ACTIVE' : 'LEARNING';
    modeBadge.style.background = hasLocks ? 'rgba(240,160,80,0.2)' : 'var(--accent-glow)';
    modeBadge.style.color = hasLocks ? 'var(--warn)' : 'var(--accent)';
    grid.classList.toggle('compact-view', state.showCompact);
    const frag = document.createDocumentFragment();
    order.forEach((id, idx) => {
      const p = panels.find(pp => pp.id === id);
      if (!p) return;
      const rank = rankMap[id] || idx + 1;
      const isLocked = !!state.locks[id];
      const isCompact = state.showCompact && rank > 5;
      const att = computeAttention(id);
      let heatClass = 'cold';
      if (att > 10) heatClass = 'hot';
      else if (att > 2) heatClass = 'warm';
      const el = document.createElement('div');
      el.className = `panel rank-${Math.min(rank, 3)}${isLocked ? ' locked' : ''}${isCompact ? ' compact' : ''}`;
      el.draggable = true;
      el.dataset.id = id;
      el.dataset.rank = rank;
      el.innerHTML = `
        <span class="rank-badge">#${rank}</span>
        <div class="panel-header">
          <span>${p.title}</span>
          <span class="lock-icon${isLocked ? ' locked' : ''}" data-action="lock" data-id="${id}">${isLocked ? '🔒' : '🔓'}</span>
        </div>
        <div class="panel-body">
          <div class="metric-value">${p.value}</div>
          <div class="metric-sub">${p.sub}</div>
        </div>
        <div class="sparkline" data-id="${id}"></div>
        <div class="panel-footer">
          <span><span class="usage-dot ${heatClass}"></span>${att < 0.1 ? 'cold' : att.toFixed(1)} attn</span>
          <span style="display:flex;gap:4px;">
            <button data-action="left" data-id="${id}" style="background:none;border:1px solid var(--border);color:var(--text-dim);cursor:pointer;border-radius:4px;padding:2px 6px;font-size:0.65rem;">◀</button>
            <button data-action="right" data-id="${id}" style="background:none;border:1px solid var(--border);color:var(--text-dim);cursor:pointer;border-radius:4px;padding:2px 6px;font-size:0.65rem;">▶</button>
          </span>
        </div>`;
      el.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-action]');
        if (btn) {
          e.preventDefault();
          const action = btn.dataset.action;
          const pid = btn.dataset.id;
          if (action === 'lock') toggleLock(pid);
          if (action === 'left' || action === 'right') movePanel(pid, action);
          return;
        }
        trackEvent(id, 'click');
      });
      el.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', id);
        el.classList.add('dragging');
      });
      el.addEventListener('dragend', () => { el.classList.remove('dragging'); });
      el.addEventListener('dragover', (e) => { e.preventDefault(); el.classList.add('drag-over'); });
      el.addEventListener('dragleave', () => { el.classList.remove('drag-over'); });
      el.addEventListener('drop', (e) => {
        e.preventDefault();
        el.classList.remove('drag-over');
        const fromId = e.dataTransfer.getData('text/plain');
        const toId = id;
        if (fromId === toId) return;
        const order = getPanelOrder();
        const fromIdx = order.indexOf(fromId);
        const toIdx = order.indexOf(toId);
        if (fromIdx === -1 || toIdx === -1) return;
        order.splice(fromIdx, 1);
        order.splice(toIdx, 0, fromId);
        state.manualOrder = order;
        state.locks[fromId] = true;
        state.locks[toId] = true;
        saveState();
        render();
      });
      frag.appendChild(el);
    });
    grid.innerHTML = '';
    grid.appendChild(frag);
    requestAnimationFrame(() => {
      document.querySelectorAll('.sparkline').forEach(svg => {
        const pid = svg.dataset.id;
        const p = panels.find(pp => pp.id === pid);
        if (p) renderSparkline(svg, p.spark);
      });
    });
  }
  let observer = null;
  function setupObserver() {
    if (observer) observer.disconnect();
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.dataset.id;
        if (!id) return;
        if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
          trackEvent(id, 'view-start');
        } else {
          trackEvent(id, 'view-end');
        }
      });
    }, { threshold: [0, 0.5] });
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  }
  function showStats() {
    const { scored } = rankPanels();
    const rows = scored.map((s, i) => {
      const p = panels.find(pp => pp.id === s.id);
      const t = state.tracking[s.id] || {};
      return `<tr>
        <td>#${i+1}</td>
        <td>${p ? p.title : s.id}</td>
        <td>${s.score.toFixed(2)}</td>
        <td>${t.views || 0}</td>
        <td>${t.clicks || 0}</td>
        <td>${((t.totalMs || 0)/1000).toFixed(1)}s</td>
        <td>${state.locks[s.id] ? '🔒' : '-'}</td>
      </tr>`;
    }).join('');
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `<div class="modal">
      <h3>Attention Scores</h3>
      <table><thead><tr><th>Rank</th><th>Panel</th><th>Score</th><th>Views</th><th>Clicks</th><th>Duration</th><th>Lock</th></tr></thead><tbody>${rows}</tbody></table>
      <button id="closeStats">Close</button>
    </div>`;
    document.body.appendChild(backdrop);
    backdrop.querySelector('#closeStats').addEventListener('click', () => backdrop.remove());
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) backdrop.remove(); });
  }
  function init() {
    loadState();
    render();
    setupObserver();
    const mo = new MutationObserver(() => setupObserver());
    mo.observe(document.getElementById('grid'), { childList: true, subtree: true });
    document.getElementById('btnReset').addEventListener('click', resetTracking);
    document.getElementById('btnStats').addEventListener('click', showStats);
    document.getElementById('btnCompact').addEventListener('click', () => {
      state.showCompact = !state.showCompact;
      saveState();
      render();
    });
    document.getElementById('btnLockAll').addEventListener('click', () => {
      const allLocked = panels.every(p => state.locks[p.id]);
      panels.forEach(p => { state.locks[p.id] = !allLocked; });
      if (!allLocked) state.manualOrder = getPanelOrder();
      else state.manualOrder = null;
      saveState();
      render();
    });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        Object.keys(state.timers).forEach(id => trackEvent(id, 'view-end'));
      }
    });
    window.addEventListener('beforeunload', () => {
      Object.keys(state.timers).forEach(id => trackEvent(id, 'view-end'));
      if (observer) observer.disconnect();
    });
  }
  document.addEventListener('DOMContentLoaded', init);
})();
</script>
</body>
</html>
```