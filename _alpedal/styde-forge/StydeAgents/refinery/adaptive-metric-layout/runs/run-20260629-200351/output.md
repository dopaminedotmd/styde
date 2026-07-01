<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout v2</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --panel-bg: #1e1e2e;
  --panel-border: #313244;
  --text-primary: #cdd6f4;
  --text-secondary: #a6adc8;
  --accent: #89b4fa;
  --accent-dim: #45475a;
  --compact-bg: #181825;
  --rank-high: #a6e3a1;
  --rank-mid: #f9e2af;
  --rank-low: #f38ba8;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
  --radius: 8px;
  --grid-gap: 12px;
  --responsive-breakpoint: 768px;
}
body {
  background: #11111b;
  color: #cdd6f4;
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}
.toolbar {
  display: flex;
  gap: 12px;
  padding: 12px 20px;
  background: #181825;
  border-bottom: 1px solid #313244;
  align-items: center;
  flex-wrap: wrap;
}
.toolbar label { font-size: 13px; color: #a6adc8; }
.toolbar select, .toolbar button {
  background: #1e1e2e;
  color: #cdd6f4;
  border: 1px solid #313244;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 13px;
  cursor: pointer;
}
.toolbar button:hover { background: #313244; }
.toolbar button.active { background: #89b4fa; color: #11111b; border-color: #89b4fa; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--grid-gap, 12px);
  padding: 16px;
  grid-auto-flow: dense;
}
.panel {
  background: var(--panel-bg, #1e1e2e);
  border: 1px solid var(--panel-border, #313244);
  border-radius: var(--radius, 8px);
  box-shadow: var(--shadow, 0 2px 8px rgba(0,0,0,0.3));
  transition: grid-column 0.3s, grid-row 0.3s, opacity 0.3s, transform 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 140px;
  position: relative;
}
.panel.size-large { grid-column: span 2; grid-row: span 2; }
.panel.size-medium { grid-column: span 1; grid-row: span 1; }
.panel.size-compact { grid-column: span 1; grid-row: span 1; max-height: 100px; opacity: 0.75; }
.panel.size-collapsed { grid-column: span 1; grid-row: span 1; max-height: 40px; opacity: 0.5; }
.panel.locked { border-color: #89b4fa; box-shadow: 0 0 0 1px #89b4fa; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--panel-border, #313244);
  cursor: grab;
}
.panel-header:active { cursor: grabbing; }
.panel-header.dragging { opacity: 0.6; }
.panel-title { font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px; }
.panel-rank-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.panel-rank-dot.high { background: #a6e3a1; }
.panel-rank-dot.mid { background: #f9e2af; }
.panel-rank-dot.low { background: #f38ba8; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none;
  border: 1px solid transparent;
  color: #a6adc8;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 6px;
  border-radius: 3px;
  line-height: 1;
}
.panel-actions button:hover { background: #313244; color: #cdd6f4; }
.panel-actions button.lock-btn.locked { color: #89b4fa; border-color: #89b4fa; }
.panel-body { padding: 12px; flex: 1; overflow: hidden; }
.panel-body.compact-body { display: flex; align-items: center; gap: 8px; padding: 6px 12px; font-size: 12px; }
.panel-body .metric-value { font-size: 28px; font-weight: 700; line-height: 1.2; }
.panel-body .metric-label { font-size: 12px; color: #a6adc8; margin-top: 2px; }
.panel-body .metric-spark {
  margin-top: 8px;
  height: 40px;
  background: rgba(137,180,250,0.08);
  border-radius: 4px;
  overflow: hidden;
}
.compact-body .metric-value { font-size: 16px; }
.compact-body .metric-label { font-size: 10px; margin-top: 0; }
.more-section {
  margin: 0 16px 16px;
  padding: 8px 16px;
  background: #181825;
  border: 1px dashed #313244;
  border-radius: 8px;
  color: #a6adc8;
  font-size: 13px;
  cursor: pointer;
  text-align: center;
}
.more-section:hover { border-color: #89b4fa; color: #cdd6f4; }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #1e1e2e;
  border: 1px solid #313244;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 13px;
  z-index: 1000;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.toast.error { border-color: #f38ba8; }
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
  .panel.size-large { grid-column: span 1; grid-row: span 1; }
  .toolbar { padding: 8px 12px; }
  .panel-body .metric-value { font-size: 22px; }
}
</style>
</head>
<body>
<div class="toolbar">
  <label>Sort:</label>
  <select id="sortMode">
    <option value="auto">Auto (adaptive)</option>
    <option value="manual">Manual (drag order)</option>
    <option value="alpha">Alphabetical</option>
  </select>
  <button id="resetBtn" title="Reset all tracking data">Reset tracking</button>
  <button id="expandAllBtn">Expand all</button>
  <span style="margin-left:auto;font-size:12px;color:#a6adc8;" id="statusText">Ready</span>
</div>
<div class="grid" id="grid"></div>
<div class="more-section" id="moreSection" style="display:none;">Show hidden panels</div>
<div class="toast" id="toast"></div>
<script>
(function() {
'use strict';
const THEME = {
  colors: {
    panelBg: '#1e1e2e',
    panelBorder: '#313244',
    textPrimary: '#cdd6f4',
    textSecondary: '#a6adc8',
    accent: '#89b4fa',
    rankHigh: '#a6e3a1',
    rankMid: '#f9e2af',
    rankLow: '#f38ba8',
    bg: '#11111b',
  },
  visibilityCap: { default: 5, min: 1, max: 60 },
  decayHalfLife: 3600,
  unseenDecayThreshold: 600,
  unseenDecayFactor: 0.5,
  storagePrefix: 'aml_v2_',
  responsiveBreakpoint: 768,
  rankWeights: { frequency: 1, duration: 1, recency: 1 },
  compactionThreshold: 0.2,
  collapseThreshold: 0.05,
  expandThreshold: 0.35,
};
function clamp(val, min, max) { return Math.max(min, Math.min(max, val)); }
function cssVar(name, fallback) {
  if (typeof getComputedStyle === 'undefined') return fallback;
  try {
    const v = getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim();
    return v || fallback;
  } catch(e) {
    return fallback;
  }
}
function safeLocalStorageGet(key, fallback) {
  try {
    const raw = localStorage.getItem(THEME.storagePrefix + key);
    if (raw === null) return fallback;
    const parsed = JSON.parse(raw);
    return parsed;
  } catch(e) {
    safeLocalStorageSet(key, fallback);
    return fallback;
  }
}
function safeLocalStorageSet(key, value) {
  try {
    localStorage.setItem(THEME.storagePrefix + key, JSON.stringify(value));
  } catch(e) {}
}
const PANEL_DEFS = [
  { id: 'cpu', title: 'CPU Usage', unit: '%', color: '#89b4fa' },
  { id: 'memory', title: 'Memory', unit: 'GB', color: '#a6e3a1' },
  { id: 'network_in', title: 'Network RX', unit: 'MB/s', color: '#f9e2af' },
  { id: 'network_out', title: 'Network TX', unit: 'MB/s', color: '#fab387' },
  { id: 'disk', title: 'Disk I/O', unit: 'MB/s', color: '#cba6f7' },
  { id: 'users', title: 'Active Users', unit: '', color: '#94e2d5' },
  { id: 'errors', title: 'Error Rate', unit: '%', color: '#f38ba8' },
  { id: 'latency', title: 'P95 Latency', unit: 'ms', color: '#89dceb' },
];
const NOW = () => Date.now() / 1000;
let tracking = safeLocalStorageGet('tracking', {});
let overrides = safeLocalStorageGet('overrides', {});
let compositeCache = null;
let cacheVersion = 0;
let sortMode = safeLocalStorageGet('sortMode', 'auto');
let toastTimer = null;
let collapsedPanels = safeLocalStorageGet('collapsedPanels', {});
function initTracking() {
  if (!tracking || typeof tracking !== 'object') tracking = {};
  PANEL_DEFS.forEach(p => {
    if (!tracking[p.id]) {
      tracking[p.id] = {
        viewCount: 0,
        totalDuration: 0,
        interactionCount: 0,
        lastSeen: null,
        lastInteraction: null,
      };
    }
  });
  persistTracking();
}
function recordView(panelId, duration) {
  if (!tracking[panelId]) return;
  const cap = clamp(THEME.visibilityCap.default, THEME.visibilityCap.min, THEME.visibilityCap.max);
  const clamped = Math.min(duration, cap);
  tracking[panelId].viewCount += 1;
  tracking[panelId].totalDuration += clamped;
  tracking[panelId].lastSeen = NOW();
  cacheVersion++;
  persistTracking();
}
function recordInteraction(panelId) {
  if (!tracking[panelId]) return;
  tracking[panelId].interactionCount += 1;
  tracking[panelId].lastInteraction = NOW();
  cacheVersion++;
  persistTracking();
}
function persistTracking() {
  safeLocalStorageSet('tracking', tracking);
}
function computeRanks() {
  if (compositeCache && compositeCache._version === cacheVersion) return compositeCache;
  const now = NOW();
  const scores = {};
  let maxScore = 0;
  let minScore = Infinity;
  PANEL_DEFS.forEach(p => {
    const t = tracking[p.id];
    if (!t) { scores[p.id] = 0; return; }
    const freq = t.viewCount;
    const avgDuration = t.viewCount > 0 ? t.totalDuration / t.viewCount : 0;
    const timeSinceSeen = t.lastSeen ? now - t.lastSeen : Infinity;
    const unseenOverThreshold = timeSinceSeen > THEME.unseenDecayThreshold;
    const decayFactor = unseenOverThreshold ? THEME.unseenDecayFactor : 1;
    const recency = Math.exp(-timeSinceSeen / (THEME.decayHalfLife * decayFactor));
    const score = (freq * THEME.rankWeights.frequency) + (avgDuration * THEME.rankWeights.duration) + (recency * THEME.rankWeights.recency);
    scores[p.id] = score;
    if (score > maxScore) maxScore = score;
    if (score < minScore) minScore = score;
  });
  const range = maxScore - minScore || 1;
  const normalized = {};
  PANEL_DEFS.forEach(p => {
    normalized[p.id] = (scores[p.id] - minScore) / range;
  });
  const sorted = PANEL_DEFS.map(p => ({ id: p.id, score: normalized[p.id] })).sort((a, b) => b.score - a.score);
  const rankMap = {};
  sorted.forEach((item, i) => { rankMap[item.id] = i; });
  compositeCache = { scores, normalized, sorted, rankMap, _version: cacheVersion };
  return compositeCache;
}
function getSizeClass(panelId, ranks) {
  if (collapsedPanels[panelId]) return 'collapsed';
  const score = ranks.normalized[panelId];
  if (score >= THEME.expandThreshold) return 'large';
  if (score >= THEME.compactionThreshold) return 'medium';
  if (score >= THEME.collapseThreshold) return 'compact';
  return 'collapsed';
}
function getVisualOrder(panelId, ranks) {
  if (overrides[panelId] && overrides[panelId].locked) {
    return overrides[panelId].position != null ? overrides[panelId].position : ranks.rankMap[panelId];
  }
  return ranks.rankMap[panelId];
}
class Dashboard {
  constructor() {
    this.grid = document.getElementById('grid');
    this.moreSection = document.getElementById('moreSection');
    this.intersectionObserver = null;
    this.viewTimers = {};
    this.panelElements = {};
    this.render();
    this.setupIntersectionObserver();
    this.setupGlobalListeners();
    this.startDataSimulation();
  }
  setupIntersectionObserver() {
    this.intersectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const pid = entry.target.dataset.panelId;
        if (!pid) return;
        if (entry.isIntersecting) {
          this.viewTimers[pid] = NOW();
        } else if (this.viewTimers[pid]) {
          const duration = NOW() - this.viewTimers[pid];
          if (duration >= 0.3) recordView(pid, duration);
          delete this.viewTimers[pid];
        }
      });
    }, { threshold: 0.5 });
  }
  flushViewTimers() {
    const now = NOW();
    Object.keys(this.viewTimers).forEach(pid => {
      const duration = now - this.viewTimers[pid];
      if (duration >= 0.3) recordView(pid, duration);
      delete this.viewTimers[pid];
    });
  }
  setupGlobalListeners() {
    document.getElementById('sortMode').value = sortMode;
    document.getElementById('sortMode').addEventListener('change', (e) => {
      sortMode = e.target.value;
      safeLocalStorageSet('sortMode', sortMode);
      this.render();
    });
    document.getElementById('resetBtn').addEventListener('click', () => {
      tracking = {};
      compositeCache = null;
      cacheVersion = 0;
      initTracking();
      this.render();
      this.toast('Tracking data reset');
    });
    document.getElementById('expandAllBtn').addEventListener('click', () => {
      collapsedPanels = {};
      safeLocalStorageSet('collapsedPanels', collapsedPanels);
      this.render();
    });
    window.addEventListener('beforeunload', () => this.flushViewTimers());
    window.addEventListener('resize', () => {
      this.render();
    });
  }
  toast(msg, isError) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.className = 'toast show' + (isError ? ' error' : '');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { el.className = 'toast'; }, 2500);
  }
  startDataSimulation() {
    this.metrics = {};
    PANEL_DEFS.forEach(p => {
      let base;
      switch(p.id) {
        case 'cpu': base = 35 + Math.random() * 30; break;
        case 'memory': base = 8 + Math.random() * 8; break;
        case 'network_in': base = 20 + Math.random() * 40; break;
        case 'network_out': base = 10 + Math.random() * 30; break;
        case 'disk': base = 40 + Math.random() * 60; break;
        case 'users': base = 200 + Math.random() * 800; break;
        case 'errors': base = 0.5 + Math.random() * 3; break;
        case 'latency': base = 20 + Math.random() * 80; break;
        default: base = 50;
      }
      this.metrics[p.id] = { value: base, history: Array(30).fill(base) };
    });
    this.simInterval = setInterval(() => {
      PANEL_DEFS.forEach(p => {
        const m = this.metrics[p.id];
        const change = (Math.random() - 0.5) * m.value * 0.15;
        let newVal = m.value + change;
        switch(p.id) {
          case 'cpu': newVal = clamp(newVal, 0, 100); break;
          case 'memory': newVal = clamp(newVal, 0, 16); break;
          case 'network_in':
          case 'network_out': newVal = clamp(newVal, 0, 100); break;
          case 'disk': newVal = clamp(newVal, 0, 200); break;
          case 'users': newVal = clamp(newVal, 0, 2000); break;
          case 'errors': newVal = clamp(newVal, 0, 10); break;
          case 'latency': newVal = clamp(newVal, 5, 500); break;
        }
        m.value = newVal;
        m.history.push(newVal);
        if (m.history.length > 30) m.history.shift();
      });
      this.updateLiveMetrics();
    }, 2000);
  }
  updateLiveMetrics() {
    if (!this.metrics) return;
    PANEL_DEFS.forEach(p => {
      const el = this.panelElements[p.id];
      if (!el) return;
      const valEl = el.querySelector('.metric-value');
      const sparkEl = el.querySelector('.metric-spark');
      if (valEl && this.metrics[p.id]) {
        valEl.textContent = this.metrics[p.id].value.toFixed(1) + p.unit;
      }
      if (sparkEl && this.metrics[p.id] && this.metrics[p.id].history) {
        sparkEl.innerHTML = this.renderSparkline(p.id);
      }
    });
  }
  renderSparkline(pid) {
    const hist = this.metrics[pid].history;
    if (!hist || hist.length < 2) return '';
    const min = Math.min(...hist);
    const max = Math.max(...hist);
    const range = max - min || 1;
    const h = 40;
    const w = 200;
    const points = hist.map((v, i) => {
      const x = (i / (hist.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return `${x},${y}`;
    }).join(' ');
    const color = PANEL_DEFS.find(p => p.id === pid)?.color || THEME.colors.accent;
    return `<svg width="100%" height="${h}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="display:block;"><polyline points="${points}" fill="none" stroke="${color}" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg>`;
  }
  render() {
    this.flushViewTimers();
    const ranks = computeRanks();
    const panels = PANEL_DEFS.map(p => ({
      ...p,
      score: ranks.normalized[p.id],
      rank: ranks.rankMap[p.id],
      sizeClass: sortMode === 'auto' ? getSizeClass(p.id, ranks) : 'medium',
      visualOrder: sortMode === 'auto' ? getVisualOrder(p.id, ranks) :
                    sortMode === 'alpha' ? PANEL_DEFS.findIndex(d => d.id === p.id) :
                    ranks.rankMap[p.id],
      locked: overrides[p.id] && overrides[p.id].locked,
    }));
    panels.sort((a, b) => a.visualOrder - b.visualOrder);
    const collapsed = panels.filter(p => p.sizeClass === 'collapsed' && sortMode === 'auto');
    const visible = panels.filter(p => !(p.sizeClass === 'collapsed' && sortMode === 'auto'));
    this.grid.innerHTML = '';
    visible.forEach(panel => {
      const el = this.createPanelElement(panel, ranks);
      this.grid.appendChild(el);
      this.panelElements[panel.id] = el;
      if (this.intersectionObserver) {
        this.intersectionObserver.observe(el);
      }
    });
    if (collapsed.length > 0) {
      this.moreSection.style.display = 'block';
      this.moreSection.textContent = `${collapsed.length} hidden panel${collapsed.length > 1 ? 's' : ''} — click to show`;
      this.moreSection.onclick = () => {
        collapsed.forEach(p => { collapsedPanels[p.id] = false; });
        safeLocalStorageSet('collapsedPanels', collapsedPanels);
        this.render();
      };
    } else {
      this.moreSection.style.display = 'none';
    }
    document.getElementById('statusText').textContent =
      `Panels: ${visible.length} visible · ${collapsed.length} hidden · Auto-layout ${sortMode === 'auto' ? 'active' : 'paused'}`;
    this.updateLiveMetrics();
  }
  createPanelElement(panel, ranks) {
    const el = document.createElement('div');
    el.className = `panel size-${panel.sizeClass}` + (panel.locked ? ' locked' : '');
    el.dataset.panelId = panel.id;
    el.draggable = true;
    el.style.order = panel.visualOrder;
    const isCompact = panel.sizeClass === 'compact' || panel.sizeClass === 'collapsed';
    const rankTier = panel.score >= 0.66 ? 'high' : panel.score >= 0.33 ? 'mid' : 'low';
    el.innerHTML = `
      <div class="panel-header">
        <span class="panel-title">
          <span class="panel-rank-dot ${rankTier}"></span>
          ${panel.title}
        </span>
        <span class="panel-actions">
          ${isCompact ? '<button class="expand-btn" title="Expand">⊕</button>' : ''}
          <button class="lock-btn ${panel.locked ? 'locked' : ''}" title="${panel.locked ? 'Unlock' : 'Lock'} position">${panel.locked ? '🔒' : '🔓'}</button>
          <button class="collapse-btn" title="Collapse">−</button>
        </span>
      </div>
      <div class="panel-body ${isCompact ? 'compact-body' : ''}">
        <span class="metric-value">--</span>
        <span class="metric-label">${panel.unit}</span>
        ${!isCompact ? '<div class="metric-spark"></div>' : ''}
      </div>
    `;
    const lockBtn = el.querySelector('.lock-btn');
    const collapseBtn = el.querySelector('.collapse-btn');
    const expandBtn = el.querySelector('.expand-btn');
    el.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      recordInteraction(panel.id);
    });
    lockBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!overrides[panel.id]) overrides[panel.id] = {};
      overrides[panel.id].locked = !overrides[panel.id].locked;
      if (overrides[panel.id].locked) {
        overrides[panel.id].position = panel.visualOrder;
      }
      safeLocalStorageSet('overrides', overrides);
      this.toast(`${panel.title} ${overrides[panel.id].locked ? 'locked' : 'unlocked'}`);
      this.render();
    });
    collapseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      collapsedPanels[panel.id] = true;
      safeLocalStorageSet('collapsedPanels', collapsedPanels);
      this.toast(`${panel.title} hidden`);
      this.render();
    });
    if (expandBtn) {
      expandBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        collapsedPanels[panel.id] = false;
        safeLocalStorageSet('collapsedPanels', collapsedPanels);
        this.render();
      });
    }
    el.addEventListener('dragstart', (e) => {
      if (sortMode !== 'manual') {
        e.preventDefault();
        this.toast('Switch sort mode to "Manual" to drag panels', true);
        return;
      }
      e.dataTransfer.setData('text/plain', panel.id);
      el.classList.add('dragging');
    });
    el.addEventListener('dragend', () => {
      el.classList.remove('dragging');
    });
    el.addEventListener('dragover', (e) => {
      if (sortMode !== 'manual') return;
      e.preventDefault();
    });
    el.addEventListener('drop', (e) => {
      if (sortMode !== 'manual') return;
      e.preventDefault();
      const draggedId = e.dataTransfer.getData('text/plain');
      const targetId = panel.id;
      if (draggedId === targetId) return;
      const draggedIdx = PANEL_DEFS.findIndex(p => p.id === draggedId);
      const targetIdx = PANEL_DEFS.findIndex(p => p.id === targetId);
      if (!overrides[draggedId]) overrides[draggedId] = {};
      overrides[draggedId].position = targetIdx;
      overrides[draggedId].locked = true;
      safeLocalStorageSet('overrides', overrides);
      recordInteraction(draggedId);
      this.toast(`Moved ${PANEL_DEFS.find(p => p.id === draggedId)?.title} to position ${targetIdx + 1}`);
      this.render();
    });
    return el;
  }
}
initTracking();
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new Dashboard());
} else {
  new Dashboard();
}
})();
</script>
</body>
</html>