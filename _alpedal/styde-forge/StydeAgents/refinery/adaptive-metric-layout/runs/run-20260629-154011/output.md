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
  --surface2: #22262f;
  --border: #2a2e38;
  --text: #d1d5db;
  --text2: #9ca3af;
  --accent: #6366f1;
  --accent2: #818cf8;
  --gold: #f59e0b;
  --green: #10b981;
  --red: #ef4444;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.4);
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 16px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}
.header h1 {
  font-size: 1.4rem;
  font-weight: 600;
  letter-spacing: -0.3px;
}
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.controls button {
  padding: 6px 14px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background var(--transition);
}
.controls button:hover { background: var(--border); }
.controls button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.badge {
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 12px;
  background: var(--surface2);
  color: var(--text2);
}
.dashboard {
  display: grid;
  gap: 12px;
  transition: grid-template-columns var(--transition), grid-template-rows var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: transform var(--transition), box-shadow var(--transition), opacity var(--transition);
  position: relative;
  min-height: 120px;
  cursor: grab;
}
.panel:active { cursor: grabbing; }
.panel.compact {
  min-height: 60px;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.dragging {
  opacity: 0.7;
  transform: scale(1.02);
  box-shadow: 0 8px 32px rgba(99,102,241,0.3);
  z-index: 100;
}
.panel.drag-over {
  border-color: var(--accent2);
  box-shadow: 0 0 0 2px var(--accent);
}
.panel.locked { cursor: default; }
.panel.locked .lock-indicator { display: block; }
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  user-select: none;
}
.panel-title {
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.panel-rank {
  font-size: 0.65rem;
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: 500;
}
.rank-high { background: rgba(245,158,11,0.15); color: var(--gold); }
.rank-mid { background: rgba(99,102,241,0.12); color: var(--accent2); }
.rank-low { background: rgba(156,163,175,0.1); color: var(--text2); }
.panel-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}
.panel-actions button {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  transition: color var(--transition), background var(--transition);
}
.panel-actions button:hover { color: var(--text); background: var(--border); }
.panel-actions button.locked-btn { color: var(--gold); }
.lock-indicator {
  display: none;
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 0.6rem;
  color: var(--gold);
  background: rgba(245,158,11,0.15);
  padding: 2px 6px;
  border-radius: 4px;
}
.panel-body {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.panel-preview {
  display: none;
  padding: 10px 14px;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
  color: var(--text2);
}
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}
.metric-value {
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.metric-label { color: var(--text2); }
.sparkline {
  height: 32px;
  width: 100%;
}
.sparkline svg { width: 100%; height: 100%; }
.heat-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  color: var(--text2);
}
.heat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.heat-hot { background: var(--red); }
.heat-warm { background: var(--gold); }
.heat-cool { background: var(--green); }
.heat-cold { background: var(--text2); }
.drag-ghost {
  position: fixed;
  pointer-events: none;
  z-index: 999;
  opacity: 0.6;
  transform: rotate(2deg);
}
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 0.8rem;
  z-index: 200;
  animation: slideIn 0.25s ease-out;
  box-shadow: 0 4px 16px rgba(0,0,0,0.5);
}
@keyframes slideIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
@media (max-width: 768px) {
  .dashboard { grid-template-columns: 1fr !important; }
  .header { flex-direction: column; align-items: flex-start; }
}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>Adaptive Dashboard</h1>
    <span class="badge" id="sessionBadge">session: --</span>
  </div>
  <div class="controls">
    <button id="btnReset" title="Reset all tracking data">Reset</button>
    <button id="btnLockAll" title="Lock/unlock all panels">Lock All</button>
    <button id="btnCompactAll" title="Toggle compact mode for all low-rank panels">Compact</button>
    <span class="badge" id="updateBadge" style="opacity:0">updated</span>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<script>
// ========== SINGLETON ENGINE STATE ==========
const Engine = (() => {
  // Memoized stable references — never recreated per tick
  let _observer = null;
  let _resizeObserver = null;
  let _dashboardEl = null;
  let _panels = [];
  let _order = [];
  let _locked = new Set();
  let _compactForced = new Set();
  let _tracking = {};        // panelId -> { totalDuration, viewCount, lastViewed, events[] }
  let _activeTimers = {};    // panelId -> { startTime, intervalId }
  let _dirty = false;
  let _debounceRank = null;
  let _debouncePersist = null;
  let _dragState = null;     // stable ref — mutated, never recreated
  let _renderScheduled = false;
  let _lastRenderHash = '';
  let _renderCount = 0;
  let _sessionStart = Date.now();
  let _attachedListeners = new WeakSet();
  // ========== DATA ==========
  const initialPanels = [
    { id: 'revenue',    title: 'Revenue',       value: '$48,291', change: '+12.3%', trend: [20,25,22,30,28,32,35,38,40,45,42,48], color: '#10b981' },
    { id: 'users',      title: 'Active Users',  value: '18,442',  change: '+5.7%',  trend: [30,32,28,35,38,40,42,38,45,48,44,50], color: '#6366f1' },
    { id: 'errors',     title: 'Error Rate',    value: '0.23%',   change: '-0.8%',  trend: [5,4,6,3,4,5,3,2,4,3,2,3],           color: '#ef4444' },
    { id: 'latency',    title: 'P95 Latency',   value: '142ms',   change: '-8ms',   trend: [50,48,52,45,47,44,46,42,40,44,38,42], color: '#f59e0b' },
    { id: 'throughput', title: 'Throughput',    value: '8.2k/s',  change: '+2.1%',  trend: [60,62,58,65,68,70,72,68,75,78,80,82], color: '#8b5cf6' },
    { id: 'storage',    title: 'Storage',       value: '742 GB',  change: '-3%',    trend: [80,82,78,76,74,72,70,68,65,62,60,58], color: '#ec4899' },
    { id: 'cpu',        title: 'CPU Usage',     value: '67%',     change: '+1.2%',  trend: [55,58,60,62,65,68,70,72,68,65,67,67], color: '#06b6d4' },
    { id: 'memory',     title: 'Memory',        value: '14.2 GB', change: '-0.5%',  trend: [40,42,38,44,46,48,45,42,40,38,36,35], color: '#84cc16' },
  ];
  // ========== ATTENTION SCORING ==========
  function calcScore(panelId) {
    const t = _tracking[panelId];
    if (!t || t.viewCount === 0) return 0;
    const now = Date.now();
    const hoursSinceLastView = Math.max(0.1, (now - t.lastViewed) / 3600000);
    const recency = 1 / Math.log(1 + hoursSinceLastView);
    const frequency = Math.log(1 + t.viewCount);
    const duration = Math.log(1 + t.totalDuration / 1000);
    return frequency * duration * recency;
  }
  // ========== RANKING (memoized by input identity) ==========
  let _lastRankInputHash = '';
  let _cachedRanks = null;
  function computeRanks() {
    const inputHash = JSON.stringify([_order, ..._order.map(id => _tracking[id]?.totalDuration || 0)]);
    if (inputHash === _lastRankInputHash && _cachedRanks) return _cachedRanks;
    const scored = _order.map(id => ({ id, score: calcScore(id) }));
    scored.sort((a, b) => b.score - a.score);
    const ranks = {};
    scored.forEach((s, i) => { ranks[s.id] = i + 1; });
    _lastRankInputHash = inputHash;
    _cachedRanks = ranks;
    return ranks;
  }
  // ========== STABLE INTERSECTION OBSERVER (created once) ==========
  function getObserver() {
    if (_observer) return _observer;
    _observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const id = entry.target.dataset.panelId;
        if (!id) continue;
        if (entry.isIntersecting) {
          startTimer(id);
        } else {
          stopTimer(id);
        }
      }
    }, { threshold: 0.5 });
    return _observer;
  }
  function getResizeObserver() {
    if (_resizeObserver) return _resizeObserver;
    _resizeObserver = new ResizeObserver(() => {
      scheduleRender();
    });
    return _resizeObserver;
  }
  // ========== TIMER MANAGEMENT ==========
  function startTimer(panelId) {
    if (_activeTimers[panelId]) return;
    if (!_tracking[panelId]) {
      _tracking[panelId] = { totalDuration: 0, viewCount: 0, lastViewed: Date.now(), events: [] };
    }
    _tracking[panelId].viewCount++;
    _tracking[panelId].lastViewed = Date.now();
    _tracking[panelId].events.push({ type: 'view', ts: Date.now() });
    const startTime = Date.now();
    const intervalId = setInterval(() => {
      _tracking[panelId].totalDuration += 1000;
      _dirty = true;
      scheduleDebouncedRank();
    }, 1000);
    _activeTimers[panelId] = { startTime, intervalId };
  }
  function stopTimer(panelId) {
    const timer = _activeTimers[panelId];
    if (!timer) return;
    clearInterval(timer.intervalId);
    _tracking[panelId].totalDuration += Date.now() - timer.startTime;
    _tracking[panelId].events.push({ type: 'hide', ts: Date.now(), duration: Date.now() - timer.startTime });
    delete _activeTimers[panelId];
    _dirty = true;
    scheduleDebouncedRank();
  }
  // ========== DEBOUNCED UPDATES ==========
  function scheduleDebouncedRank() {
    if (_debounceRank) clearTimeout(_debounceRank);
    _debounceRank = setTimeout(() => {
      _cachedRanks = null;
      _lastRankInputHash = '';
      scheduleRender();
    }, 200);
  }
  function scheduleDebouncedPersist() {
    if (_debouncePersist) clearTimeout(_debouncePersist);
    _debouncePersist = setTimeout(persist, 500);
  }
  // ========== SINGLE RENDER ENTRY POINT WITH DIRTY CHECKING ==========
  function scheduleRender() {
    if (_renderScheduled) return;
    _renderScheduled = true;
    requestAnimationFrame(() => {
      _renderScheduled = false;
      doRender();
    });
  }
  function doRender() {
    if (!_dashboardEl) return;
    _renderCount++;
    const ranks = computeRanks();
    // Compute layout grid
    const sorted = [..._order];
    sorted.sort((a, b) => {
      const aLocked = _locked.has(a);
      const bLocked = _locked.has(b);
      if (aLocked && !bLocked) return -1;
      if (!aLocked && bLocked) return 1;
      if (aLocked && bLocked) return _order.indexOf(a) - _order.indexOf(b);
      return (ranks[a] || 99) - (ranks[b] || 99);
    });
    const cols = Math.min(4, Math.max(1, Math.floor(window.innerWidth / 280)));
    _dashboardEl.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    // Dirty check: compute hash of desired DOM state
    const hashParts = sorted.map(id => {
      const p = _panels.find(x => x.id === id);
      const rank = ranks[id] || 99;
      const compact = shouldCompact(id, rank);
      const locked = _locked.has(id);
      return `${id}:${rank}:${compact}:${locked}:${p?.value || ''}`;
    });
    const newHash = hashParts.join('|') + `|cols:${cols}`;
    if (newHash === _lastRenderHash) return;
    _lastRenderHash = newHash;
    // Incremental DOM update: only touch changed nodes
    const existingEls = new Map();
    _dashboardEl.querySelectorAll('.panel').forEach(el => {
      existingEls.set(el.dataset.panelId, el);
    });
    const fragment = document.createDocumentFragment();
    const seen = new Set();
    for (const id of sorted) {
      const p = _panels.find(x => x.id === id);
      if (!p) continue;
      seen.add(id);
      const rank = ranks[id] || 99;
      const compact = shouldCompact(id, rank);
      let el = existingEls.get(id);
      if (el) {
        // Update existing element in place — only changed attributes
        if (el.dataset.rank !== String(rank)) {
          el.dataset.rank = rank;
          const rankEl = el.querySelector('.panel-rank');
          if (rankEl) {
            rankEl.textContent = '#' + rank;
            rankEl.className = 'panel-rank ' + (rank <= 2 ? 'rank-high' : rank <= 5 ? 'rank-mid' : 'rank-low');
          }
        }
        if (el.classList.contains('compact') !== compact) {
          el.classList.toggle('compact', compact);
        }
        if (el.classList.contains('locked') !== _locked.has(id)) {
          el.classList.toggle('locked', _locked.has(id));
        }
        const dur = _tracking[id]?.totalDuration || 0;
        const heatEl = el.querySelector('.heat-dot');
        if (heatEl && heatEl.dataset.duration !== String(dur)) {
          heatEl.dataset.duration = dur;
          heatEl.className = 'heat-dot ' + (dur > 120000 ? 'heat-hot' : dur > 60000 ? 'heat-warm' : dur > 10000 ? 'heat-cool' : 'heat-cold');
        }
        const lockBtn = el.querySelector('.locked-btn');
        if (lockBtn) lockBtn.classList.toggle('locked-btn', _locked.has(id));
        // Move in DOM order if position changed
        const currentChildren = Array.from(_dashboardEl.children);
        const targetIdx = sorted.indexOf(id);
        const currentIdx = currentChildren.indexOf(el);
        if (currentIdx !== targetIdx && targetIdx < _dashboardEl.children.length) {
          const ref = _dashboardEl.children[targetIdx];
          _dashboardEl.insertBefore(el, ref);
        } else if (currentIdx !== -1 && targetIdx >= _dashboardEl.children.length) {
          _dashboardEl.appendChild(el);
        }
      } else {
        // Create new element
        el = buildPanelElement(p, rank, compact);
        if (!_attachedListeners.has(el)) {
          attachPanelListeners(el);
          _attachedListeners.add(el);
        }
        fragment.appendChild(el);
      }
    }
    // Remove stale elements
    for (const [id, el] of existingEls) {
      if (!seen.has(id)) el.remove();
    }
    if (fragment.children.length > 0) {
      _dashboardEl.appendChild(fragment);
    }
    // Re-observe all panels (observer is stable, just (un)observe targets)
    const observer = getObserver();
    _dashboardEl.querySelectorAll('.panel').forEach(el => {
      observer.unobserve(el);
      observer.observe(el);
    });
    getResizeObserver().unobserve(_dashboardEl);
    getResizeObserver().observe(_dashboardEl);
    updateBadge();
  }
  function shouldCompact(id, rank) {
    if (_locked.has(id)) return false;
    if (_compactForced.has(id)) return true;
    const t = _tracking[id];
    if (!t) return rank >= 7;
    const isCold = t.totalDuration < 15000 && t.viewCount < 3;
    return rank >= 6 || isCold;
  }
  function updateBadge() {
    const badge = document.getElementById('updateBadge');
    if (!badge) return;
    badge.textContent = 'render #' + _renderCount;
    badge.style.opacity = '1';
    setTimeout(() => { badge.style.opacity = '0'; }, 1500);
  }
  // ========== PANEL DOM BUILD (fragment-based) ==========
  function buildPanelElement(p, rank, compact) {
    const el = document.createElement('div');
    el.className = 'panel' + (compact ? ' compact' : '') + (_locked.has(p.id) ? ' locked' : '');
    el.dataset.panelId = p.id;
    el.dataset.rank = rank;
    el.draggable = !_locked.has(p.id);
    const dur = _tracking[p.id]?.totalDuration || 0;
    const heatClass = dur > 120000 ? 'heat-hot' : dur > 60000 ? 'heat-warm' : dur > 10000 ? 'heat-cool' : 'heat-cold';
    const rankClass = rank <= 2 ? 'rank-high' : rank <= 5 ? 'rank-mid' : 'rank-low';
    el.innerHTML = `
      <div class="lock-indicator">LOCKED</div>
      <div class="panel-header">
        <div class="panel-title">
          <span class="panel-rank ${rankClass}">#${rank}</span>
          ${p.title}
        </div>
        <div class="panel-actions">
          <span class="heat-badge"><span class="heat-dot ${heatClass}" data-duration="${dur}"></span>${formatDuration(dur)}</span>
          <button class="lock-btn ${_locked.has(p.id) ? 'locked-btn' : ''}" data-action="lock" title="Lock position">${_locked.has(p.id) ? 'U' : 'L'}</button>
          <button data-action="compact" title="Toggle compact">C</button>
        </div>
      </div>
      <div class="panel-preview">
        <span>${p.title}: ${p.value} (${p.change})</span>
      </div>
      <div class="panel-body">
        <div class="metric-row">
          <span class="metric-label">Value</span>
          <span class="metric-value">${p.value}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Change</span>
          <span class="metric-value" style="color:${p.change.startsWith('+') ? 'var(--green)' : 'var(--red)'}">${p.change}</span>
        </div>
        <div class="sparkline">${buildSparkline(p.trend, p.color)}</div>
      </div>`;
    return el;
  }
  function buildSparkline(data, color) {
    const w = 200, h = 32, pad = 2;
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    let points = data.map((v, i) => {
      const x = pad + (i / (data.length - 1)) * (w - 2 * pad);
      const y = h - pad - ((v - min) / range) * (h - 2 * pad);
      return `${x},${y}`;
    }).join(' ');
    return `<svg viewBox="0 0 ${w} ${h}"><polyline points="${points}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  }
  function formatDuration(ms) {
    if (ms < 1000) return '0s';
    const sec = Math.floor(ms / 1000);
    if (sec < 60) return sec + 's';
    const min = Math.floor(sec / 60);
    return min + 'm';
  }
  // ========== STABLE DRAG HANDLERS (attached once per element) ==========
  function attachPanelListeners(el) {
    let dragStartX, dragStartY, dragOrigIdx, dragClone;
    el.addEventListener('dragstart', (e) => {
      if (_locked.has(el.dataset.panelId)) { e.preventDefault(); return; }
      el.classList.add('dragging');
      dragStartX = e.clientX;
      dragStartY = e.clientY;
      dragOrigIdx = Array.from(_dashboardEl.children).indexOf(el);
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', el.dataset.panelId);
    });
    el.addEventListener('dragend', () => {
      el.classList.remove('dragging');
      if (dragClone) { dragClone.remove(); dragClone = null; }
      document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
    });
    el.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      const target = e.currentTarget;
      document.querySelectorAll('.panel.drag-over').forEach(p => {
        if (p !== target) p.classList.remove('drag-over');
      });
      if (!target.classList.contains('dragging')) {
        target.classList.add('drag-over');
      }
    });
    el.addEventListener('dragleave', () => {
      el.classList.remove('drag-over');
    });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      el.classList.remove('drag-over');
      const srcId = e.dataTransfer.getData('text/plain');
      const dstId = el.dataset.panelId;
      if (srcId === dstId) return; // prevent swap on same-element
      const srcIdx = _order.indexOf(srcId);
      const dstIdx = _order.indexOf(dstId);
      if (srcIdx === -1 || dstIdx === -1) return;
      _order.splice(srcIdx, 1);
      _order.splice(dstIdx, 0, srcId);
      _dirty = true;
      scheduleDebouncedPersist();
      scheduleRender();
      showToast('Panel moved: ' + (_panels.find(p => p.id === srcId)?.title || srcId));
    });
    el.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;
      const action = btn.dataset.action;
      const panelId = el.dataset.panelId;
      if (action === 'lock') {
        toggleLock(panelId);
      } else if (action === 'compact') {
        toggleCompactForce(panelId);
      }
    });
  }
  // ========== ACTIONS ==========
  function toggleLock(panelId) {
    if (_locked.has(panelId)) {
      _locked.delete(panelId);
      _tracking[panelId]?.events.push({ type: 'unlock', ts: Date.now() });
    } else {
      _locked.add(panelId);
      _tracking[panelId]?.events.push({ type: 'lock', ts: Date.now() });
    }
    _dirty = true;
    _cachedRanks = null;
    scheduleDebouncedPersist();
    scheduleRender();
  }
  function toggleCompactForce(panelId) {
    if (_compactForced.has(panelId)) {
      _compactForced.delete(panelId);
      _tracking[panelId]?.events.push({ type: 'expand', ts: Date.now() });
    } else {
      _compactForced.add(panelId);
      _tracking[panelId]?.events.push({ type: 'collapse', ts: Date.now() });
    }
    _dirty = true;
    scheduleDebouncedPersist();
    scheduleRender();
  }
  function lockAll() {
    const allLocked = _order.every(id => _locked.has(id));
    if (allLocked) {
      _order.forEach(id => _locked.delete(id));
      showToast('All panels unlocked');
    } else {
      _order.forEach(id => _locked.add(id));
      showToast('All panels locked');
    }
    _dirty = true;
    scheduleDebouncedPersist();
    scheduleRender();
  }
  function compactAllLow() {
    const ranks = computeRanks();
    let toggled = 0;
    for (const id of _order) {
      const rank = ranks[id] || 99;
      if (rank >= 5 && !_locked.has(id)) {
        if (_compactForced.has(id)) {
          _compactForced.delete(id);
        } else {
          _compactForced.add(id);
          toggled++;
        }
      }
    }
    if (toggled === 0) {
      // un-compact all
      _compactForced.clear();
      showToast('All panels expanded');
    } else {
      showToast(toggled + ' panels compacted');
    }
    scheduleDebouncedPersist();
    scheduleRender();
  }
  function resetAll() {
    for (const id of _order) {
      stopTimer(id);
    }
    _tracking = {};
    _cachedRanks = null;
    _lastRankInputHash = '';
    _locked.clear();
    _compactForced.clear();
    _order = _panels.map(p => p.id);
    _sessionStart = Date.now();
    _dirty = true;
    persist();
    scheduleRender();
    showToast('Tracking data reset');
  }
  // ========== PERSISTENCE ==========
  function persist() {
    const data = {
      order: _order,
      locked: Array.from(_locked),
      compactForced: Array.from(_compactForced),
      tracking: _tracking,
      sessionStart: _sessionStart,
      renderCount: _renderCount,
    };
    try {
      localStorage.setItem('adaptive-dashboard-v2', JSON.stringify(data));
    } catch(e) {}
  }
  function restore() {
    try {
      const raw = localStorage.getItem('adaptive-dashboard-v2');
      if (!raw) return false;
      const data = JSON.parse(raw);
      if (data.order && Array.isArray(data.order)) {
        _order = data.order.filter(id => _panels.some(p => p.id === id));
        // Add any new panels not in saved order
        _panels.forEach(p => { if (!_order.includes(p.id)) _order.push(p.id); });
      }
      if (data.locked) data.locked.forEach(id => _locked.add(id));
      if (data.compactForced) data.compactForced.forEach(id => _compactForced.add(id));
      if (data.tracking) _tracking = data.tracking;
      if (data.sessionStart) _sessionStart = data.sessionStart;
      if (data.renderCount) _renderCount = data.renderCount;
      return true;
    } catch(e) {
      return false;
    }
  }
  // ========== TOAST ==========
  function showToast(msg) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
  }
  // ========== INIT ==========
  function init() {
    _panels = initialPanels;
    _dashboardEl = document.getElementById('dashboard');
    if (!_dashboardEl) return;
    _order = _panels.map(p => p.id);
    const restored = restore();
    _lastRenderHash = '';
    _cachedRanks = null;
    _lastRankInputHash = '';
    scheduleRender();
    document.getElementById('btnReset').addEventListener('click', resetAll);
    document.getElementById('btnLockAll').addEventListener('click', lockAll);
    document.getElementById('btnCompactAll').addEventListener('click', compactAllLow);
    document.getElementById('sessionBadge').textContent = 'session: ' + new Date(_sessionStart).toLocaleTimeString();
    // Periodic persist
    setInterval(() => {
      if (_dirty) { persist(); _dirty = false; }
    }, 10000);
    window.addEventListener('beforeunload', () => {
      for (const id of _order) stopTimer(id);
      persist();
    });
    window.addEventListener('resize', () => {
      _lastRenderHash = '';
      scheduleRender();
    });
  }
  return { init };
})();
document.addEventListener('DOMContentLoaded', Engine.init);
</script>
</body>
</html>
```