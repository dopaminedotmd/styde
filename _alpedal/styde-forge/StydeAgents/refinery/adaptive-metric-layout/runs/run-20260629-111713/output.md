<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e0e0e0;
  --text-dim: #888;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff5c5c;
  --success: #4cdf80;
  --warn: #ffb347;
  --compact-bg: #141720;
  --rank-high: #6c8cff;
  --rank-mid: #8b9dc3;
  --rank-low: #5a5f72;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  background: var(--panel-bg);
  border-bottom: 1px solid var(--panel-border);
  flex-wrap: wrap;
  position: sticky;
  top: 0;
  z-index: 100;
}
.toolbar h1 {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.3px;
  margin-right: auto;
}
.toolbar label { font-size: 12px; color: var(--text-dim); display:flex; align-items:center; gap:6px; }
.toolbar select, .toolbar button {
  background: var(--bg);
  border: 1px solid var(--panel-border);
  color: var(--text);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: 0.15s;
}
.toolbar select:hover, .toolbar button:hover { border-color: var(--accent); }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.toolbar .badge {
  font-size: 10px;
  background: var(--accent-glow);
  color: var(--accent);
  padding: 3px 8px;
  border-radius: 10px;
  font-weight: 500;
}
#grid {
  display: grid;
  gap: 10px;
  padding: 16px;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 180px;
  transition: all var(--transition);
  max-width: 1400px;
  margin: 0 auto;
}
@media (max-width: 900px) { #grid { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 160px; } }
@media (max-width: 500px) { #grid { grid-template-columns: 1fr; grid-auto-rows: 150px; } }
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  padding: 14px;
  cursor: grab;
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.panel:active { cursor: grabbing; }
.panel:hover { border-color: #3a3d4f; }
.panel.large { grid-column: span 2; grid-row: span 2; }
.panel.medium { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; font-size:0.85em; padding:10px; }
.panel.compact .panel-value { font-size: 1.2em; }
.panel.compact .sparkline-canvas { height: 30px; }
.panel.mini { grid-column: span 1; grid-row: span 1; padding:8px 10px; font-size:0.78em; }
.panel.mini .panel-value { font-size: 1em; }
.panel.mini .sparkline-canvas { height: 22px; }
.panel.mini .panel-header { margin-bottom: 2px; }
.panel.dragging {
  opacity: 0.5;
  transform: scale(0.95);
  z-index: 50;
  pointer-events: none;
}
.panel.drop-target {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-glow);
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  gap: 6px;
}
.panel-title {
  font-size: 0.8em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-dim);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-controls { display:flex; gap:4px; flex-shrink:0; }
.panel-controls button {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  font-size: 14px;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.15s;
  line-height: 1;
}
.panel-controls button:hover { background: #2a2d3a; color: #fff; }
.panel-controls button.locked { color: var(--accent); }
.panel-value {
  font-size: 1.6em;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1;
  margin-bottom: 2px;
}
.panel-value.warn { color: var(--warn); }
.panel-value.danger { color: var(--danger); }
.panel-value.ok { color: var(--success); }
.panel-subtitle {
  font-size: 0.7em;
  color: var(--text-dim);
  margin-bottom: 4px;
}
.sparkline-canvas {
  flex: 1;
  min-height: 0;
  width: 100%;
  opacity: 0.85;
}
.panel-rank-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  opacity: 0.6;
  transition: 0.3s;
}
.rank-high .panel-rank-indicator { background: var(--rank-high); opacity:1; }
.rank-mid .panel-rank-indicator { background: var(--rank-mid); }
.rank-low .panel-rank-indicator { background: var(--rank-low); }
.panel.compact .panel-value { font-size:1.3em; }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--accent);
  color: #fff;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  z-index: 200;
  opacity: 0;
  transform: translateY(10px);
  transition: 0.25s;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
@keyframes value-update { 0% { transform: scale(1); } 50% { transform: scale(1.08); } 100% { transform: scale(1); } }
.value-flash { animation: value-update 0.3s ease-out; }
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <label>Refresh
    <select id="refreshInterval">
      <option value="0">Off</option>
      <option value="5000">5s</option>
      <option value="15000" selected>15s</option>
      <option value="30000">30s</option>
    </select>
  </label>
  <button id="btnReset" title="Reset layout to default">Reset Layout</button>
  <button id="btnResetData" title="Clear all attention tracking data">Clear History</button>
  <span class="badge" id="trackingBadge">Learning</span>
</div>
<div id="grid"></div>
<div class="toast" id="toast"></div>
<script>
// ============================================================
// METRIC ENGINE — realistic data layer with seeded history
// ============================================================
const MetricEngine = {
  metrics: [
    { id: 'cpu', name: 'CPU Usage', unit: '%', range: [15, 85], spikeChance: 0.08, trend: 0.02, warn: 70, crit: 90, color: '#6c8cff' },
    { id: 'mem', name: 'Memory', unit: 'GB', range: [4.2, 12.8], spikeChance: 0.04, trend: 0.01, warn: 10, crit: 12, color: '#b06cff', decimals: 1 },
    { id: 'reqs', name: 'Requests/s', unit: '', range: [80, 450], spikeChance: 0.06, trend: -0.3, warn: null, crit: null, color: '#4cdf80' },
    { id: 'errors', name: 'Error Rate', unit: '%', range: [0.1, 3.5], spikeChance: 0.12, trend: 0.005, warn: 2, crit: 5, color: '#ff5c5c', decimals: 2 },
    { id: 'latency', name: 'Latency p95', unit: 'ms', range: [45, 280], spikeChance: 0.07, trend: 0.5, warn: 200, crit: 300, color: '#ffb347' },
    { id: 'diskio', name: 'Disk I/O', unit: 'MB/s', range: [10, 180], spikeChance: 0.05, trend: -0.1, warn: null, crit: null, color: '#4dc9f6', decimals: 1 },
  ],
  history: {}, // { metricId: [{value, ts}] }
  init() {
    const now = Date.now();
    this.metrics.forEach(m => {
      const seed = m.range[0] + Math.random() * (m.range[1] - m.range[0]);
      this.history[m.id] = [];
      // Generate 120 data points (30 min at 15s intervals)
      for (let i = 119; i >= 0; i--) {
        this.history[m.id].push({
          value: this._nextValue(m, i === 119 ? seed : this.history[m.id][this.history[m.id].length - 1].value),
          ts: now - i * 15000
        });
      }
    });
  },
  _nextValue(metric, prevValue) {
    const range = metric.range[1] - metric.range[0];
    const noise = (Math.random() - 0.5) * range * 0.12;
    let v = prevValue + noise + metric.trend;
    if (Math.random() < metric.spikeChance) {
      v += (Math.random() - 0.3) * range * 0.4; // asymmetric spikes
    }
    v = Math.max(metric.range[0] * 0.5, Math.min(metric.range[1] * 1.3, v));
    if (metric.decimals !== undefined) {
      v = parseFloat(v.toFixed(metric.decimals));
    } else {
      v = Math.round(v);
    }
    return v;
  },
  tick() {
    const now = Date.now();
    this.metrics.forEach(m => {
      const prev = this.history[m.id][this.history[m.id].length - 1].value;
      const next = this._nextValue(m, prev);
      this.history[m.id].push({ value: next, ts: now });
      // Keep last 120 points
      if (this.history[m.id].length > 120) {
        this.history[m.id].shift();
      }
    });
    return this.snapshot();
  },
  snapshot() {
    const snap = {};
    this.metrics.forEach(m => {
      const series = this.history[m.id];
      snap[m.id] = {
        current: series[series.length - 1].value,
        history: series.map(p => p.value),
        ts: series[series.length - 1].ts,
        unit: m.unit,
        warn: m.warn,
        crit: m.crit,
        name: m.name,
        color: m.color,
        decimals: m.decimals,
      };
    });
    return snap;
  }
};
// ============================================================
// ATTENTION TRACKER — view duration, interaction, collapse events
// ============================================================
const AttentionTracker = {
  storageKey: 'adb_attention_v2',
  data: {}, // { panelId: { views, totalDuration, clicks, expands, collapses, lastInteraction, score } }
  init() {
    const raw = localStorage.getItem(this.storageKey);
    if (raw) {
      try { this.data = JSON.parse(raw); } catch(e) { this.data = {}; }
    }
    MetricEngine.metrics.forEach(m => {
      if (!this.data[m.id]) {
        this.data[m.id] = { views: 0, totalDuration: 0, clicks: 0, expands: 0, collapses: 0, lastInteraction: 0, locked: false, overriddenPos: null };
      }
    });
    this._startObserver();
  },
  _startObserver() {
    const visibilityMap = new Map(); // panelId -> { enterTime, totalVisible }
    const observer = new IntersectionObserver((entries) => {
      const now = Date.now();
      entries.forEach(entry => {
        const panelId = entry.target.dataset.panelId;
        if (!panelId || !this.data[panelId]) return;
        if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
          if (!visibilityMap.has(panelId)) {
            visibilityMap.set(panelId, { enterTime: now, accumulated: 0 });
            this.data[panelId].views++;
          }
        } else {
          const vis = visibilityMap.get(panelId);
          if (vis) {
            const duration = now - vis.enterTime;
            this.data[panelId].totalDuration += duration;
            this.data[panelId].lastInteraction = now;
            visibilityMap.delete(panelId);
          }
        }
      });
      // Flush all active on each check
      visibilityMap.forEach((vis, panelId) => {
        const duration = Date.now() - vis.enterTime;
        this.data[panelId].totalDuration += duration;
        vis.enterTime = Date.now();
      });
    }, { threshold: [0, 0.5] });
    // Observe panels after render
    this._observer = observer;
    this._visibilityMap = visibilityMap;
  },
  observePanels() {
    if (!this._observer) return;
    document.querySelectorAll('.panel').forEach(el => {
      this._observer.observe(el);
    });
  },
  recordClick(panelId) {
    if (!this.data[panelId]) return;
    this.data[panelId].clicks++;
    this.data[panelId].lastInteraction = Date.now();
    this.save();
  },
  recordExpand(panelId) {
    if (!this.data[panelId]) return;
    this.data[panelId].expands++;
    this.data[panelId].lastInteraction = Date.now();
    this.save();
  },
  recordCollapse(panelId) {
    if (!this.data[panelId]) return;
    this.data[panelId].collapses++;
    this.data[panelId].lastInteraction = Date.now();
    this.save();
  },
  setLocked(panelId, locked) {
    if (!this.data[panelId]) return;
    this.data[panelId].locked = locked;
    this.save();
  },
  setOverride(panelId, pos) {
    if (!this.data[panelId]) return;
    this.data[panelId].overriddenPos = pos;
    this.save();
  },
  getScore(panelId) {
    const d = this.data[panelId];
    if (!d) return 0;
    const now = Date.now();
    const hoursSinceLast = Math.max(0.1, (now - d.lastInteraction) / 3600000);
    const recencyDecay = Math.exp(-hoursSinceLast / 24); // half-life ~17h
    const durationScore = Math.log1p(d.totalDuration / 1000) * 2;
    const freqScore = Math.log1p(d.views + d.clicks) * 3;
    const interactionBonus = (d.expands * 0.5 + d.clicks * 1.5) * 0.5;
    return (freqScore + durationScore + interactionBonus) * recencyDecay;
  },
  getRankedPanels() {
    return MetricEngine.metrics
      .map(m => ({ id: m.id, score: this.getScore(m.id), locked: this.data[m.id]?.locked, overriddenPos: this.data[m.id]?.overriddenPos }))
      .sort((a, b) => b.score - a.score);
  },
  save() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.data));
  },
  reset() {
    this.data = {};
    MetricEngine.metrics.forEach(m => {
      this.data[m.id] = { views: 0, totalDuration: 0, clicks: 0, expands: 0, collapses: 0, lastInteraction: 0, locked: false, overriddenPos: null };
    });
    this.save();
  }
};
// ============================================================
// DROP-TARGET SPATIAL INDEX — avoids elementFromPoint ambiguity
// ============================================================
const DropTargetIndex = {
  rects: new Map(), // panelId -> DOMRect
  gridColumns: 4,
  rebuild() {
    this.rects.clear();
    document.querySelectorAll('.panel').forEach(el => {
      const id = el.dataset.panelId;
      if (id) this.rects.set(id, el.getBoundingClientRect());
    });
    const grid = document.getElementById('grid');
    if (grid) {
      const style = getComputedStyle(grid);
      this.gridColumns = style.gridTemplateColumns.split(' ').length || 4;
    }
  },
  findTarget(x, y) {
    let bestId = null;
    let bestArea = Infinity;
    this.rects.forEach((rect, id) => {
      if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
        const area = (rect.right - rect.left) * (rect.bottom - rect.top);
        if (area < bestArea) { bestArea = area; bestId = id; }
      }
    });
    return bestId;
  },
  findClosest(x, y, excludeId) {
    let bestId = null;
    let bestDist = Infinity;
    this.rects.forEach((rect, id) => {
      if (id === excludeId) return;
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dist = Math.hypot(cx - x, cy - y);
      if (dist < bestDist) { bestDist = dist; bestId = id; }
    });
    return bestId;
  }
};
// ============================================================
// DRAG-DROP CONTROLLER — pointer events, touch + mouse unified
// ============================================================
const DragDropController = {
  dragEl: null,
  dragPanelId: null,
  ghostEl: null,
  startX: 0, startY: 0,
  currentDropTarget: null,
  init() {
    document.getElementById('grid').addEventListener('pointerdown', this.onPointerDown.bind(this));
    document.addEventListener('pointermove', this.onPointerMove.bind(this));
    document.addEventListener('pointerup', this.onPointerUp.bind(this));
    document.addEventListener('pointercancel', this.onPointerUp.bind(this));
    // Prevent browser drag behaviors on touch
    document.addEventListener('touchstart', e => {
      if (e.target.closest('.panel')) e.preventDefault();
    }, { passive: false });
  },
  onPointerDown(e) {
    const panel = e.target.closest('.panel');
    if (!panel) return;
    // Don't drag if clicking controls
    if (e.target.closest('button')) return;
    const panelId = panel.dataset.panelId;
    if (!panelId) return;
    if (AttentionTracker.data[panelId]?.locked) return;
    this.dragEl = panel;
    this.dragPanelId = panelId;
    this.startX = e.clientX;
    this.startY = e.clientY;
    panel.setPointerCapture(e.pointerId);
    // Create ghost
    this.ghostEl = panel.cloneNode(true);
    this.ghostEl.style.position = 'fixed';
    this.ghostEl.style.zIndex = '150';
    this.ghostEl.style.width = panel.offsetWidth + 'px';
    this.ghostEl.style.pointerEvents = 'none';
    this.ghostEl.style.opacity = '0.9';
    this.ghostEl.style.transform = 'rotate(1deg) scale(1.02)';
    this.ghostEl.style.boxShadow = '0 8px 32px rgba(0,0,0,0.5)';
    const rect = panel.getBoundingClientRect();
    this.ghostEl.style.left = rect.left + 'px';
    this.ghostEl.style.top = rect.top + 'px';
    document.body.appendChild(this.ghostEl);
    panel.classList.add('dragging');
    DropTargetIndex.rebuild();
    AttentionTracker.recordClick(panelId);
  },
  onPointerMove(e) {
    if (!this.dragEl) return;
    const dx = e.clientX - this.startX;
    const dy = e.clientY - this.startY;
    const rect = this.dragEl.getBoundingClientRect();
    this.ghostEl.style.left = (rect.left + dx) + 'px';
    this.ghostEl.style.top = (rect.top + dy) + 'px';
    const targetId = DropTargetIndex.findTarget(e.clientX, e.clientY);
    if (targetId !== this.currentDropTarget && targetId !== this.dragPanelId) {
      // Remove previous highlight
      if (this.currentDropTarget) {
        const prev = document.querySelector(`[data-panel-id="${this.currentDropTarget}"]`);
        if (prev) prev.classList.remove('drop-target');
      }
      this.currentDropTarget = targetId;
      if (targetId) {
        const el = document.querySelector(`[data-panel-id="${targetId}"]`);
        if (el) el.classList.add('drop-target');
      }
    }
  },
  onPointerUp(e) {
    if (!this.dragEl) return;
    if (this.currentDropTarget && this.currentDropTarget !== this.dragPanelId) {
      const targetData = AttentionTracker.data[this.currentDropTarget];
      if (!targetData?.locked) {
        // Swap positions: save overridden positions
        const draggedRank = AttentionTracker.getRankedPanels().findIndex(p => p.id === this.dragPanelId);
        const targetRank = AttentionTracker.getRankedPanels().findIndex(p => p.id === this.currentDropTarget);
        AttentionTracker.setOverride(this.dragPanelId, targetRank);
        AttentionTracker.setOverride(this.currentDropTarget, draggedRank);
        LayoutEngine.apply();
        showToast('Panels swapped');
      }
    }
    // Cleanup
    if (this.currentDropTarget) {
      const el = document.querySelector(`[data-panel-id="${this.currentDropTarget}"]`);
      if (el) el.classList.remove('drop-target');
    }
    this.dragEl.classList.remove('dragging');
    if (this.ghostEl) { this.ghostEl.remove(); this.ghostEl = null; }
    try { this.dragEl.releasePointerCapture(e.pointerId); } catch(_) {}
    this.dragEl = null;
    this.dragPanelId = null;
    this.currentDropTarget = null;
  }
};
// ============================================================
// LAYOUT ENGINE — rank-based grid positioning with targeted updates
// ============================================================
const LayoutEngine = {
  sizeClasses: ['large', 'medium', 'compact', 'mini'],
  computeLayout() {
    const ranked = AttentionTracker.getRankedPanels();
    // Apply overrides: if a panel has overriddenPos, move it there
    const overridden = ranked.filter(p => p.overriddenPos !== null);
    const normal = ranked.filter(p => p.overriddenPos === null);
    overridden.forEach(p => {
      const targetIdx = Math.min(p.overriddenPos, ranked.length - 1);
      const currentIdx = ranked.findIndex(r => r.id === p.id);
      if (currentIdx >= 0 && targetIdx >= 0 && targetIdx < ranked.length) {
        const [moved] = ranked.splice(currentIdx, 1);
        ranked.splice(targetIdx, 0, moved);
      }
    });
    // Assign size classes: top 2 = large, next 2 = medium, rest = compact, bottom 2 = mini
    const total = ranked.length;
    ranked.forEach((p, i) => {
      if (i < 2) p.sizeClass = 'large';
      else if (i < 4) p.sizeClass = 'medium';
      else if (i < total - 2) p.sizeClass = 'compact';
      else p.sizeClass = 'mini';
      // Locked panels always stay medium+
      if (p.locked && (p.sizeClass === 'compact' || p.sizeClass === 'mini')) {
        p.sizeClass = 'medium';
      }
    });
    return ranked;
  },
  apply() {
    const layout = this.computeLayout();
    const grid = document.getElementById('grid');
    const existingPanels = new Map();
    grid.querySelectorAll('.panel').forEach(el => {
      existingPanels.set(el.dataset.panelId, el);
    });
    // Reorder DOM — only move elements, don't rebuild
    layout.forEach((p, idx) => {
      let panelEl = existingPanels.get(p.id);
      if (!panelEl) {
        panelEl = this._createPanelElement(p.id);
      }
      // Update size class
      const oldClasses = panelEl.className;
      const newClasses = 'panel ' + p.sizeClass;
      if (oldClasses !== newClasses) {
        panelEl.className = newClasses;
      }
      // Update rank indicator class
      if (idx < 2) {
        panelEl.classList.add('rank-high'); panelEl.classList.remove('rank-mid', 'rank-low');
      } else if (idx < 5) {
        panelEl.classList.add('rank-mid'); panelEl.classList.remove('rank-high', 'rank-low');
      } else {
        panelEl.classList.add('rank-low'); panelEl.classList.remove('rank-high', 'rank-mid');
      }
      // Move to correct position
      const currentIdx = Array.from(grid.children).indexOf(panelEl);
      if (currentIdx !== idx && currentIdx >= 0) {
        if (idx >= grid.children.length) {
          grid.appendChild(panelEl);
        } else if (currentIdx < idx) {
          grid.insertBefore(panelEl, grid.children[idx + 1] || null);
        } else {
          grid.insertBefore(panelEl, grid.children[idx]);
        }
      } else if (currentIdx < 0) {
        if (idx >= grid.children.length) {
          grid.appendChild(panelEl);
        } else {
          grid.insertBefore(panelEl, grid.children[idx]);
        }
      }
    });
    // Remove panels that no longer exist
    const currentIds = new Set(layout.map(p => p.id));
    existingPanels.forEach((el, id) => {
      if (!currentIds.has(id)) el.remove();
    });
    AttentionTracker.observePanels();
    DropTargetIndex.rebuild();
  },
  _createPanelElement(panelId) {
    const el = document.createElement('div');
    el.className = 'panel medium';
    el.dataset.panelId = panelId;
    el.innerHTML = `
      <div class="panel-rank-indicator"></div>
      <div class="panel-header">
        <span class="panel-title"></span>
        <div class="panel-controls">
          <button class="btn-lock" title="Lock position">&#128274;</button>
          <button class="btn-expand" title="Toggle size">&#8690;</button>
        </div>
      </div>
      <div class="panel-value"></div>
      <div class="panel-subtitle"></div>
      <canvas class="sparkline-canvas"></canvas>
    `;
    el.querySelector('.btn-lock').addEventListener('click', (e) => {
      e.stopPropagation();
      const locked = !AttentionTracker.data[panelId]?.locked;
      AttentionTracker.setLocked(panelId, locked);
      e.target.classList.toggle('locked', locked);
      e.target.textContent = locked ? '\uD83D\uDD12' : '\uD83D\uDD13';
      LayoutEngine.apply();
      showToast(locked ? 'Panel locked' : 'Panel unlocked');
    });
    el.querySelector('.btn-expand').addEventListener('click', (e) => {
      e.stopPropagation();
      AttentionTracker.recordExpand(panelId);
      const p = AttentionTracker.getRankedPanels().find(r => r.id === panelId);
      if (p && p.sizeClass === 'compact' || p.sizeClass === 'mini') {
        // Temporarily boost
        AttentionTracker.data[panelId].totalDuration += 120000;
        AttentionTracker.data[panelId].lastInteraction = Date.now();
        AttentionTracker.data[panelId].expands++;
        AttentionTracker.save();
        LayoutEngine.apply();
      }
    });
    el.addEventListener('click', () => {
      AttentionTracker.recordClick(panelId);
    });
    return el;
  },
  // Targeted update: only update the panel whose data changed
  updatePanelData(panelId, metricData) {
    const el = document.querySelector(`[data-panel-id="${panelId}"]`);
    if (!el) return;
    const titleEl = el.querySelector('.panel-title');
    const valueEl = el.querySelector('.panel-value');
    const subtitleEl = el.querySelector('.panel-subtitle');
    const canvas = el.querySelector('.sparkline-canvas');
    if (titleEl) titleEl.textContent = metricData.name;
    if (valueEl) {
      const v = metricData.current;
      const display = metricData.decimals !== undefined ? v.toFixed(metricData.decimals) : v;
      valueEl.textContent = display + ' ' + metricData.unit;
      valueEl.className = 'panel-value';
      if (metricData.crit !== null && v >= metricData.crit) valueEl.classList.add('danger');
      else if (metricData.warn !== null && v >= metricData.warn) valueEl.classList.add('warn');
      else valueEl.classList.add('ok');
      // Flash animation
      valueEl.classList.remove('value-flash');
      void valueEl.offsetWidth;
      valueEl.classList.add('value-flash');
    }
    if (subtitleEl) {
      const prev = metricData.history[metricData.history.length - 2] || metricData.current;
      const delta = metricData.current - prev;
      const sign = delta >= 0 ? '+' : '';
      const pct = prev !== 0 ? ((delta / Math.abs(prev)) * 100).toFixed(1) : '0.0';
      subtitleEl.textContent = `${sign}${delta.toFixed(metricData.decimals || 0)} (${sign}${pct}%)`;
    }
    if (canvas) {
      this._drawSparkline(canvas, metricData.history, metricData.color);
    }
  },
  _drawSparkline(canvas, data, color) {
    const rect = canvas.parentElement.getBoundingClientRect();
    const w = rect.width - 28;
    const h = canvas.parentElement.classList.contains('compact') ? 30 :
              canvas.parentElement.classList.contains('mini') ? 22 : 44;
    if (canvas.width !== w * devicePixelRatio || canvas.height !== h * devicePixelRatio) {
      canvas.width = w * devicePixelRatio;
      canvas.height = h * devicePixelRatio;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
    }
    const ctx = canvas.getContext('2d');
    const dpr = devicePixelRatio;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (data.length < 2) return;
    const min = Math.min(...data) * 0.9;
    const max = Math.max(...data) * 1.1;
    const range = max - min || 1;
    const stepX = w * dpr / (data.length - 1);
    const baseline = h * dpr;
    // Fill gradient
    const grad = ctx.createLinearGradient(0, 0, 0, baseline);
    grad.addColorStop(0, color + '40');
    grad.addColorStop(1, color + '05');
    ctx.beginPath();
    ctx.moveTo(0, baseline);
    data.forEach((v, i) => {
      const x = i * stepX;
      const y = baseline - ((v - min) / range) * baseline * 0.85;
      ctx.lineTo(x, y);
    });
    ctx.lineTo((data.length - 1) * stepX, baseline);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();
    // Line
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5 * dpr;
    ctx.lineJoin = 'round';
    data.forEach((v, i) => {
      const x = i * stepX;
      const y = baseline - ((v - min) / range) * baseline * 0.85;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }
};
// ============================================================
// UI HELPERS
// ============================================================
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('show'), 2000);
}
// ============================================================
// AUTO-REFRESH + INIT
// ============================================================
let refreshTimer = null;
function startRefresh(intervalMs) {
  clearInterval(refreshTimer);
  if (intervalMs > 0) {
    refreshTimer = setInterval(() => {
      const snap = MetricEngine.tick();
      // Targeted updates per panel
      Object.keys(snap).forEach(panelId => {
        LayoutEngine.updatePanelData(panelId, snap[panelId]);
      });
    }, intervalMs);
  }
}
function init() {
  MetricEngine.init();
  AttentionTracker.init();
  DragDropController.init();
  // Build initial panel elements
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  MetricEngine.metrics.forEach(m => {
    const el = LayoutEngine._createPanelElement(m.id);
    grid.appendChild(el);
  });
  // Apply layout ranking
  LayoutEngine.apply();
  // Initial data render
  const snap = MetricEngine.snapshot();
  Object.keys(snap).forEach(panelId => {
    LayoutEngine.updatePanelData(panelId, snap[panelId]);
  });
  // Auto-refresh
  const refreshSelect = document.getElementById('refreshInterval');
  refreshSelect.addEventListener('change', () => {
    startRefresh(parseInt(refreshSelect.value));
  });
  startRefresh(parseInt(refreshSelect.value));
  // Reset button
  document.getElementById('btnReset').addEventListener('click', () => {
    MetricEngine.metrics.forEach(m => {
      AttentionTracker.setOverride(m.id, null);
      AttentionTracker.setLocked(m.id, false);
    });
    AttentionTracker.save();
    LayoutEngine.apply();
    const snap = MetricEngine.snapshot();
    Object.keys(snap).forEach(id => LayoutEngine.updatePanelData(id, snap[id]));
    showToast('Layout reset');
  });
  document.getElementById('btnResetData').addEventListener('click', () => {
    AttentionTracker.reset();
    LayoutEngine.apply();
    showToast('History cleared — relearning');
  });
  // Periodic layout re-rank (every 30s)
  setInterval(() => {
    LayoutEngine.apply();
  }, 30000);
  // Periodic save
  setInterval(() => {
    AttentionTracker.save();
  }, 10000);
  // Update tracking badge
  const badge = document.getElementById('trackingBadge');
  setInterval(() => {
    const totalViews = Object.values(AttentionTracker.data).reduce((s, d) => s + d.views, 0);
    badge.textContent = totalViews > 10 ? `Trained (${totalViews} views)` : 'Learning';
  }, 5000);
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>