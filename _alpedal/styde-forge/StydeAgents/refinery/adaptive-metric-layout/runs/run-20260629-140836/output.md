<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --compact-bg: #141720;
  --rank-1-size: 1;
  --rank-2-size: 1;
  --rank-3-size: 1;
  --rank-4-size: 1;
  --rank-5-size: 1;
  --rank-6-size: 1;
  --rank-7-size: 1;
  --rank-8-size: 1;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 12px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  margin-bottom: 12px;
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
}
.header h1 { font-size: 1.15rem; font-weight: 600; letter-spacing: -0.01em; }
.header-actions { display: flex; gap: 8px; align-items: center; }
.btn {
  background: #252836;
  border: 1px solid var(--panel-border);
  color: var(--text);
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: background 0.15s;
}
.btn:hover { background: #30344a; }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(160px, auto);
  gap: 10px;
}
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  padding: 14px;
  transition: transform 0.25s ease, box-shadow 0.25s ease, grid-column 0.3s ease, grid-row 0.3s ease;
  position: relative;
  cursor: grab;
  min-height: 140px;
  display: flex;
  flex-direction: column;
}
.panel:active { cursor: grabbing; }
.panel.dragging { opacity: 0.6; z-index: 10; }
.panel.drag-over { box-shadow: 0 0 0 2px var(--accent); }
.panel.high-rank {
  background: linear-gradient(135deg, #1a1d27 0%, #1e2340 100%);
  box-shadow: 0 0 20px var(--accent-glow);
}
.panel.compact {
  padding: 8px 10px;
  min-height: 72px;
  font-size: 0.78rem;
  background: var(--compact-bg);
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-title { font-size: 0.78rem; }
.panel.compact .panel-value { font-size: 1rem; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.panel.compact .panel-header { margin-bottom: 2px; }
.panel-title {
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.panel-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}
.panel-actions button {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  padding: 2px 5px;
  font-size: 0.75rem;
  border-radius: 4px;
  line-height: 1;
}
.panel-actions button:hover { color: var(--text); background: #252836; }
.panel-actions button.locked { color: #f0c040; }
.panel-value {
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}
.panel-sub {
  font-size: 0.75rem;
  color: var(--text-dim);
}
.panel-body { flex: 1; }
.chart-mini {
  height: 48px;
  display: flex;
  align-items: flex-end;
  gap: 2px;
  margin-top: 8px;
}
.chart-mini .bar {
  flex: 1;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
  opacity: 0.6;
  transition: height 0.4s ease;
}
.rank-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 0.6rem;
  color: var(--text-dim);
  background: #252836;
  padding: 1px 6px;
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.2s;
}
.panel:hover .rank-badge { opacity: 1; }
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #252836;
  border: 1px solid var(--panel-border);
  color: var(--text);
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  z-index: 100;
}
.toast.show { opacity: 1; }
.compact-row {
  grid-column: 1 / -1;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.compact-row .panel.compact {
  flex: 1;
  min-width: 140px;
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-actions">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset Stats</button>
    <span style="font-size:0.75rem;color:var(--text-dim)" id="statusText">Auto-arrange active</span>
  </div>
</div>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
  'use strict';
  const PANEL_DEFS = [
    { id: 'cpu',     title: 'CPU Usage',     value: '23%',   sub: '4 cores',    color: '#6c8cff' },
    { id: 'memory',  title: 'Memory',        value: '7.2GB', sub: 'of 16GB',    color: '#50c878' },
    { id: 'network', title: 'Network I/O',   value: '142',   sub: 'MB/s total', color: '#ff8c42' },
    { id: 'sales',   title: 'Sales Revenue', value: '$48.2K', sub: 'today',      color: '#f0c040' },
    { id: 'users',   title: 'Active Users',  value: '1,247', sub: 'online now',  color: '#c084fc' },
    { id: 'errors',  title: 'Error Rate',    value: '0.12%', sub: 'last hour',   color: '#f87171' },
    { id: 'latency', title: 'P95 Latency',   value: '142ms', sub: 'avg 98ms',    color: '#38bdf8' },
    { id: 'storage', title: 'Storage',       value: '412GB', sub: 'free of 1TB', color: '#a3e635' }
  ];
  const STORAGE_KEY = 'adaptive_dashboard_v2';
  const COMPACT_THRESHOLD = 0.15;
  const ARRANGE_DEBOUNCE_MS = 4000;
  const RECENCY_HALFLIFE_HOURS = 4;
  const TRACK_INTERVAL_MS = 2000;
  let panels = [];
  let scores = new Map();
  let panelEls = new Map();
  let arrangeTimer = null;
  let observer = null;
  let dragState = null;
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch(e) { return null; }
  }
  function saveState(s) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
    } catch(e) {}
  }
  function initState() {
    const saved = loadState();
    const now = Date.now();
    panels = PANEL_DEFS.map((def, i) => {
      const savedPanel = saved?.panels?.find(p => p.id === def.id);
      return {
        id: def.id,
        order: savedPanel?.order ?? i,
        locked: savedPanel?.locked ?? false,
        compact: savedPanel?.compact ?? false,
        freq: savedPanel?.freq ?? 0,
        totalDuration: savedPanel?.totalDuration ?? 0,
        lastInteraction: savedPanel?.lastInteraction ?? now,
        interactions: savedPanel?.interactions ?? 0
      };
    });
  }
  function persistPanels() {
    saveState({ panels, savedAt: Date.now() });
  }
  function computeScore(p) {
    const now = Date.now();
    const hoursSince = Math.max(0, (now - p.lastInteraction) / 3600000);
    const recency = Math.exp(-hoursSince * Math.log(2) / RECENCY_HALFLIFE_HOURS);
    const durWeight = Math.log2(p.totalDuration / 1000 + 1) + 1;
    const freqWeight = Math.log2(p.freq + 1) + 1;
    const intWeight = Math.log2(p.interactions + 1) + 1;
    return freqWeight * durWeight * intWeight * recency;
  }
  function rankAll() {
    const ranked = panels.map(p => ({ ...p, score: computeScore(p) }));
    ranked.sort((a, b) => b.score - a.score);
    const maxScore = ranked[0]?.score || 1;
    ranked.forEach((p, i) => {
      p.rank = i;
      p.normalizedScore = maxScore > 0 ? p.score / maxScore : 0;
    });
    return ranked;
  }
  function shouldCompact(p) {
    return !p.locked && p.normalizedScore < COMPACT_THRESHOLD && p.rank >= Math.floor(panels.length * 0.6);
  }
  function computeGridPlacement(ranked) {
    const result = [];
    const normal = [];
    const compactList = [];
    ranked.forEach(p => {
      const compact = shouldCompact(p);
      const panel = { ...p, compact };
      if (compact) {
        compactList.push(panel);
      } else {
        normal.push(panel);
      }
    });
    normal.sort((a, b) => {
      if (a.locked !== b.locked) return a.locked ? -1 : 1;
      return a.rank - b.rank;
    });
    let idx = 0;
    const assignments = [];
    const cols = 4;
    for (const p of normal) {
      const span = p.rank <= 1 ? 2 : 1;
      assignments.push({ ...p, gridCol: `span ${span}`, idx: idx++ });
    }
    return { assignments, compactList, normal };
  }
  function recordInteraction(pid, type) {
    const p = panels.find(x => x.id === pid);
    if (!p) return;
    p.freq++;
    p.interactions++;
    p.lastInteraction = Date.now();
    if (type === 'expand' && p.compact) {
      p.compact = false;
    }
    persistPanels();
    scheduleArrange();
  }
  function recordViewTime(pid, ms) {
    const p = panels.find(x => x.id === pid);
    if (!p) return;
    p.totalDuration += ms;
    p.lastInteraction = Date.now();
    persistPanels();
  }
  function toggleLock(pid) {
    const p = panels.find(x => x.id === pid);
    if (!p) return;
    p.locked = !p.locked;
    persistPanels();
    scheduleArrange();
    showToast(p.locked ? 'Panel locked' : 'Panel unlocked');
  }
  function toggleCompact(pid) {
    const p = panels.find(x => x.id === pid);
    if (!p) return;
    if (p.locked) {
      p.compact = !p.compact;
      persistPanels();
      scheduleArrange();
      showToast(p.compact ? 'Panel minimized' : 'Panel expanded');
    }
  }
  function showToast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._timeout);
    el._timeout = setTimeout(() => el.classList.remove('show'), 1800);
  }
  function scheduleArrange() {
    clearTimeout(arrangeTimer);
    arrangeTimer = setTimeout(applyArrange, ARRANGE_DEBOUNCE_MS);
  }
  function applyArrange() {
    const ranked = rankAll();
    const { assignments, compactList, normal } = computeGridPlacement(ranked);
    const grid = document.getElementById('grid');
    const existingCompactRow = grid.querySelector('.compact-row');
    if (existingCompactRow) {
      existingCompactRow.remove();
    }
    const orderedIds = assignments.map(a => a.id);
    orderedIds.forEach(id => {
      const el = panelEls.get(id);
      if (!el) return;
      const a = assignments.find(x => x.id === id);
      if (a) {
        const span = a.rank <= 1 ? 2 : 1;
        el.style.gridColumn = `span ${span}`;
        el.style.gridRow = '';
      }
      if (a && a.compact) {
        el.classList.add('compact');
      } else {
        el.classList.remove('compact');
      }
      if (a && a.rank <= 1) {
        el.classList.add('high-rank');
      } else {
        el.classList.remove('high-rank');
      }
      const badge = el.querySelector('.rank-badge');
      if (badge && a) {
        badge.textContent = '#' + (a.rank + 1);
      }
    });
    orderedIds.forEach(id => {
      const el = panelEls.get(id);
      if (el) grid.appendChild(el);
    });
    if (compactList.length > 0) {
      const row = document.createElement('div');
      row.className = 'compact-row';
      compactList.forEach(p => {
        const el = panelEls.get(p.id);
        if (el) {
          el.style.gridColumn = '';
          el.classList.add('compact');
          el.classList.remove('high-rank');
          row.appendChild(el);
        }
      });
      grid.appendChild(row);
    }
    panels.forEach(p => {
      const a = assignments.find(x => x.id === p.id);
      if (a) p.compact = a.compact;
      else if (compactList.find(x => x.id === p.id)) p.compact = true;
    });
    persistPanels();
    document.getElementById('statusText').textContent =
      'Auto-arranged at ' + new Date().toLocaleTimeString();
  }
  function createPanelElement(def, panel) {
    const el = document.createElement('div');
    el.className = 'panel';
    el.dataset.panelId = def.id;
    el.draggable = true;
    const defData = PANEL_DEFS.find(d => d.id === def.id);
    const color = defData ? defData.color : '#6c8cff';
    el.innerHTML =
      '<span class="rank-badge">#' + (panel.rank !== undefined ? panel.rank + 1 : '?') + '</span>' +
      '<div class="panel-header">' +
        '<span class="panel-title">' + def.title + '</span>' +
        '<div class="panel-actions">' +
          '<button class="btn-lock' + (panel.locked ? ' locked' : '') + '" data-action="lock" title="Lock position">&#128274;</button>' +
          '<button data-action="compact" title="Minimize/Expand">&#9660;</button>' +
        '</div>' +
      '</div>' +
      '<span class="panel-value" style="color:' + color + '">' + def.value + '</span>' +
      '<span class="panel-sub">' + def.sub + '</span>' +
      '<div class="panel-body">' +
        '<div class="chart-mini">' +
          Array.from({length: 14}, () => {
            const h = 12 + Math.random() * 36;
            return '<div class="bar" style="height:' + h + 'px; background:' + color + '"></div>';
          }).join('') +
        '</div>' +
      '</div>';
    el.addEventListener('click', function(e) {
      const action = e.target.dataset.action;
      if (action === 'lock') {
        e.stopPropagation();
        toggleLock(def.id);
        const btn = el.querySelector('.btn-lock');
        const p = panels.find(x => x.id === def.id);
        if (btn) {
          btn.classList.toggle('locked', p ? p.locked : false);
          btn.innerHTML = p && p.locked ? '&#128274;' : '&#128275;';
        }
        return;
      }
      if (action === 'compact') {
        e.stopPropagation();
        toggleCompact(def.id);
        return;
      }
      recordInteraction(def.id, 'click');
    });
    el.addEventListener('dragstart', handleDragStart);
    el.addEventListener('dragover', handleDragOver);
    el.addEventListener('dragleave', handleDragLeave);
    el.addEventListener('drop', handleDrop);
    el.addEventListener('dragend', handleDragEnd);
    animateChart(el);
    return el;
  }
  function animateChart(el) {
    const bars = el.querySelectorAll('.bar');
    if (!bars.length) return;
    const interval = setInterval(() => {
      if (!el.isConnected) { clearInterval(interval); return; }
      bars.forEach(b => {
        const h = 12 + Math.random() * 36;
        b.style.height = h + 'px';
      });
    }, 2800);
  }
  function handleDragStart(e) {
    const pid = this.dataset.panelId;
    const p = panels.find(x => x.id === pid);
    if (p && p.locked) {
      e.preventDefault();
      showToast('Panel is locked');
      return;
    }
    dragState = { id: pid, el: this };
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', pid);
  }
  function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    const target = e.currentTarget;
    if (target !== dragState?.el) {
      target.classList.add('drag-over');
    }
  }
  function handleDragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
  }
  function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    const targetId = e.currentTarget.dataset.panelId;
    const sourceId = dragState?.id;
    if (!sourceId || !targetId || sourceId === targetId) return;
    const srcPanel = panels.find(p => p.id === sourceId);
    const tgtPanel = panels.find(p => p.id === targetId);
    if (!srcPanel || !tgtPanel) return;
    const srcOrder = srcPanel.order;
    srcPanel.order = tgtPanel.order;
    tgtPanel.order = srcOrder;
    srcPanel.locked = true;
    tgtPanel.locked = true;
    srcPanel.lastInteraction = Date.now();
    tgtPanel.lastInteraction = Date.now();
    persistPanels();
    scheduleArrange();
    showToast('Panels swapped & locked');
    recordInteraction(sourceId, 'drag');
  }
  function handleDragEnd(e) {
    this.classList.remove('dragging');
    document.querySelectorAll('.panel.drag-over').forEach(el => el.classList.remove('drag-over'));
    dragState = null;
  }
  function setupViewTracking() {
    if (observer) observer.disconnect();
    const viewTimers = new Map();
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const pid = entry.target.dataset.panelId;
        if (!pid) return;
        if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
          if (!viewTimers.has(pid)) {
            viewTimers.set(pid, { start: Date.now(), interval: setInterval(() => {
              const t = viewTimers.get(pid);
              if (t) {
                recordViewTime(pid, TRACK_INTERVAL_MS);
              }
            }, TRACK_INTERVAL_MS) });
          }
        } else {
          const timer = viewTimers.get(pid);
          if (timer) {
            clearInterval(timer.interval);
            const elapsed = Date.now() - timer.start;
            if (elapsed > 500) {
              recordViewTime(pid, elapsed);
            }
            viewTimers.delete(pid);
          }
        }
      });
    }, { threshold: [0.0, 0.5] });
    panelEls.forEach(el => observer.observe(el));
  }
  function buildUI() {
    const grid = document.getElementById('grid');
    const ranked = rankAll();
    panelEls.clear();
    const fragment = document.createDocumentFragment();
    ranked.forEach((p, idx) => {
      const def = PANEL_DEFS.find(d => d.id === p.id);
      if (!def) return;
      p.order = idx;
      const el = createPanelElement(def, p);
      panelEls.set(p.id, el);
      if (p.locked && p.compact) el.classList.add('compact');
      if (p.rank <= 1) el.classList.add('high-rank');
      fragment.appendChild(el);
    });
    grid.appendChild(fragment);
    applyArrange();
    setupViewTracking();
  }
  function resetStats() {
    const now = Date.now();
    panels.forEach(p => {
      p.freq = 0;
      p.totalDuration = 0;
      p.interactions = 0;
      p.lastInteraction = now;
      p.locked = false;
      p.compact = false;
      p.order = PANEL_DEFS.findIndex(d => d.id === p.id);
    });
    persistPanels();
    applyArrange();
    showToast('Tracking data reset');
  }
  document.getElementById('btnReset').addEventListener('click', resetStats);
  initState();
  buildUI();
  // Runtime verification
  (function verify() {
    const errors = [];
    if (panels.length !== PANEL_DEFS.length) errors.push('panel count mismatch');
    if (typeof computeScore(panels[0]) !== 'number') errors.push('score not numeric');
    if (panelEls.size !== panels.length) errors.push('DOM elements missing');
    panels.forEach(p => {
      const el = panelEls.get(p.id);
      if (!el) errors.push('missing element: ' + p.id);
      else if (!el.querySelector('.panel-value')) errors.push('missing value in: ' + p.id);
      else if (!el.querySelector('.chart-mini')) errors.push('missing chart in: ' + p.id);
    });
    const stored = loadState();
    if (!stored || !stored.panels) errors.push('localStorage save/load broken');
    if (errors.length) {
      console.error('VERIFY FAIL:', errors.join('; '));
    } else {
      console.log('VERIFY OK: ' + panels.length + ' panels, scoring active, persistence valid, DOM intact');
    }
  })();
})();
</script>
</body>
</html>