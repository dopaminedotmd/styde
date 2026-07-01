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
  --border: #2a2e3a;
  --text: #e1e4eb;
  --text2: #8b90a0;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 16px;
  user-select: none;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 0 4px;
}
h1 { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; }
.badge {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.75rem;
  color: var(--text2);
}
.badge span { color: var(--accent2); font-weight: 600; margin-left: 4px; }
.toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
}
.btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn:hover { background: var(--border); border-color: var(--text2); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.dashboard {
  display: grid;
  gap: var(--gap);
  transition: all var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: all var(--transition);
  display: flex;
  flex-direction: column;
  position: relative;
}
.panel.dominant { grid-column: span 2; grid-row: span 2; }
.panel.normal { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; }
.panel.compact .panel-body { max-height: 80px; overflow: hidden; opacity: 0.6; }
.panel.compact .panel-metric { font-size: 1rem; }
.panel.compact .panel-chart { height: 40px !important; }
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.panel.locked::after {
  content: 'locked';
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 11px;
  color: var(--accent);
  background: rgba(108,140,255,0.15);
  padding: 2px 8px;
  border-radius: 10px;
  z-index: 2;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px 8px;
  gap: 8px;
}
.panel-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.panel-controls { display: flex; gap: 4px; }
.panel-ctrl {
  width: 26px; height: 26px;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text2);
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}
.panel-ctrl:hover { background: var(--surface2); border-color: var(--border); color: var(--text); }
.panel-ctrl.lock-btn.locked { color: var(--accent); background: rgba(108,140,255,0.12); }
.panel-body { padding: 0 14px 14px; flex: 1; }
.panel-metric {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
  margin-bottom: 4px;
}
.panel-sub {
  font-size: 0.75rem;
  color: var(--text2);
}
.panel-chart {
  height: 60px;
  margin-top: 8px;
  border-radius: 6px;
  overflow: hidden;
}
.panel-chart svg { width: 100%; height: 100%; }
.trend-up { color: var(--accent2); }
.trend-down { color: var(--danger); }
.rank-indicator {
  position: absolute;
  bottom: 8px;
  right: 10px;
  font-size: 10px;
  color: var(--text2);
  opacity: 0.5;
}
.heatmap-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 9999;
  transition: opacity 0.3s;
}
.heatmap-overlay.hidden { opacity: 0; }
.heat-cell {
  position: absolute;
  border-radius: var(--radius);
  transition: all 0.5s;
}
.panel-duration {
  position: absolute;
  top: 8px;
  left: 8px;
  font-size: 10px;
  color: var(--text2);
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 2;
  background: var(--surface);
  padding: 2px 8px;
  border-radius: 8px;
}
.panel:hover .panel-duration { opacity: 1; }
.section-label {
  grid-column: 1/-1;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text2);
  padding: 8px 4px 0;
  border-top: 1px solid var(--border);
  margin-top: 4px;
}
@keyframes rankShift {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}
.rank-shifting { animation: rankShift 0.4s ease; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Adaptive Metric Layout</h1>
    <div style="font-size:0.7rem;color:var(--text2);margin-top:2px">Self-organizing — learns from your attention</div>
  </div>
  <div class="toolbar">
    <div class="badge">Attention Score <span id="globalScore">0</span></div>
    <button class="btn" id="btnHeatmap" title="Toggle heatmap overlay">Heatmap</button>
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="heatmap-overlay hidden" id="heatmapOverlay"></div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_metric_layout_v1';
  const DECAY_HALF_LIFE_MS = 30 * 60 * 1000;
  const RANK_UPDATE_INTERVAL = 5000;
  const HOVER_THRESHOLD_MS = 800;
  const COMPACT_THRESHOLD_PERCENTILE = 30;
  const PANEL_DEFS = [
    { id: 'revenue', title: 'Revenue', unit: '$', color: '#6c8cff', trend: 'up', base: 48200, noise: 1200 },
    { id: 'users', title: 'Active Users', unit: '', color: '#4ade80', trend: 'up', base: 18400, noise: 400 },
    { id: 'latency', title: 'P95 Latency', unit: 'ms', color: '#f59e0b', trend: 'down', base: 142, noise: 18 },
    { id: 'errors', title: 'Error Rate', unit: '%', color: '#ef4444', trend: 'down', base: 0.34, noise: 0.08 },
    { id: 'throughput', title: 'Throughput', unit: 'rps', color: '#a78bfa', trend: 'up', base: 8900, noise: 600 },
    { id: 'sessions', title: 'Sessions', unit: '', color: '#38bdf8', trend: 'up', base: 6200, noise: 300 },
    { id: 'cpu', title: 'CPU Usage', unit: '%', color: '#fb923c', trend: 'down', base: 47, noise: 8 },
    { id: 'memory', title: 'Memory', unit: 'GB', color: '#e879f9', trend: 'up', base: 12.4, noise: 1.2 },
    { id: 'disk', title: 'Disk I/O', unit: 'MB/s', color: '#22d3ee', trend: 'down', base: 84, noise: 15 },
    { id: 'cache', title: 'Cache Hit Rate', unit: '%', color: '#34d399', trend: 'up', base: 94.2, noise: 2.5 },
    { id: 'queue', title: 'Queue Depth', unit: '', color: '#f87171', trend: 'down', base: 230, noise: 45 },
    { id: 'uptime', title: 'Uptime', unit: '%', color: '#60a5fa', trend: 'up', base: 99.97, noise: 0.02 },
  ];
  function mulberry32(a) {
    return function() {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const seeds = {};
  for (const p of PANEL_DEFS) {
    let h = 0;
    for (let i = 0; i < p.id.length; i++) h = ((h << 5) - h + p.id.charCodeAt(i)) | 0;
    seeds[p.id] = Math.abs(h) || 1;
  }
  const frozenMetrics = {};
  const frozenSparklines = {};
  for (const p of PANEL_DEFS) {
    const rng = mulberry32(seeds[p.id]);
    frozenMetrics[p.id] = {
      current: p.base + (rng() - 0.5) * p.noise * 2,
      trend: rng() > 0.5 ? 'up' : 'down',
      delta: ((rng() - 0.5) * p.noise * 0.3).toFixed(1),
    };
    const pts = [];
    for (let i = 0; i < 14; i++) {
      pts.push(p.base + (rng() - 0.5) * p.noise * 2);
    }
    frozenSparklines[p.id] = pts;
  }
  let panels = PANEL_DEFS.map((def, i) => ({
    ...def,
    index: i,
    rank: 0,
    size: 'normal',
    locked: false,
    lockedSize: null,
    lockedPosition: null,
    metrics: frozenMetrics[def.id],
    sparkline: frozenSparklines[def.id],
  }));
  let attentionData = loadAttentionData();
  let hoverTimers = {};
  let viewStartTimes = {};
  let rankHistory = [];
  function loadAttentionData() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        const out = {};
        for (const [id, d] of Object.entries(parsed.attention || {})) {
          out[id] = { frequency: d.frequency || 0, duration: d.duration || 0, lastInteraction: d.lastInteraction || 0, locks: d.locks || [] };
        }
        if (parsed.locks) {
          for (const [id, lock] of Object.entries(parsed.locks)) {
            const p = panels.find(pp => pp.id === id);
            if (p) { p.locked = lock.locked || false; p.lockedSize = lock.size || null; p.lockedPosition = lock.position || null; }
          }
        }
        return out;
      }
    } catch(e) {}
    const out = {};
    for (const p of panels) out[p.id] = { frequency: 0, duration: 0, lastInteraction: 0, locks: [] };
    return out;
  }
  function saveState() {
    const att = {};
    for (const [id, d] of Object.entries(attentionData)) {
      att[id] = { frequency: d.frequency, duration: d.duration, lastInteraction: d.lastInteraction };
    }
    const locks = {};
    for (const p of panels) {
      locks[p.id] = { locked: p.locked, size: p.lockedSize, position: p.lockedPosition };
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ attention: att, locks, savedAt: Date.now() }));
  }
  function computeAttentionScore(data, now) {
    const age = Math.max(0, now - data.lastInteraction);
    const decay = Math.exp(-age * Math.LN2 / DECAY_HALF_LIFE_MS);
    return data.frequency * data.duration * decay;
  }
  function computeRanks() {
    const now = Date.now();
    const scores = panels.map(p => ({
      id: p.id,
      score: computeAttentionScore(attentionData[p.id] || { frequency: 0, duration: 0, lastInteraction: 0 }, now),
    }));
    scores.sort((a, b) => b.score - a.score);
    const rankMap = {};
    scores.forEach((s, i) => { rankMap[s.id] = i + 1; });
    const total = panels.length;
    const compactCutoff = Math.ceil(total * (1 - COMPACT_THRESHOLD_PERCENTILE / 100));
    panels.forEach(p => {
      const r = rankMap[p.id] || total;
      p.rank = r;
      if (!p.locked) {
        if (r === 1) p.size = 'dominant';
        else if (r >= compactCutoff) p.size = 'compact';
        else p.size = 'normal';
      } else {
        p.size = p.lockedSize || p.size;
      }
    });
    const globalScore = scores.length > 0 ? scores[0].score.toFixed(0) : '0';
    const el = document.getElementById('globalScore');
    if (el) el.textContent = globalScore;
    return { scores, rankMap, globalScore };
  }
  function recordInteraction(panelId, type) {
    if (!attentionData[panelId]) {
      attentionData[panelId] = { frequency: 0, duration: 0, lastInteraction: 0 };
    }
    const d = attentionData[panelId];
    d.frequency += 1;
    d.lastInteraction = Date.now();
    if (type === 'expand' || type === 'collapse') {
      d.locks = d.locks || [];
      d.locks.push({ type, time: Date.now() });
      if (d.locks.length > 20) d.locks = d.locks.slice(-20);
    }
    saveState();
  }
  function recordViewDuration(panelId, ms) {
    if (!attentionData[panelId]) {
      attentionData[panelId] = { frequency: 0, duration: 0, lastInteraction: 0 };
    }
    attentionData[panelId].duration += ms;
    attentionData[panelId].lastInteraction = Date.now();
    saveState();
  }
  function lockPanel(panelId) {
    const p = panels.find(pp => pp.id === panelId);
    if (!p) return;
    p.locked = !p.locked;
    if (p.locked) {
      p.lockedSize = p.size;
    } else {
      p.lockedSize = null;
      p.lockedPosition = null;
    }
    recordInteraction(panelId, p.locked ? 'lock' : 'unlock');
    render();
  }
  function resetAll() {
    attentionData = {};
    for (const p of panels) {
      attentionData[p.id] = { frequency: 0, duration: 0, lastInteraction: 0, locks: [] };
      p.locked = false;
      p.lockedSize = null;
      p.lockedPosition = null;
      p.size = 'normal';
      p.rank = 0;
    }
    localStorage.removeItem(STORAGE_KEY);
    computeRanks();
    render();
  }
  function formatMetric(val, unit) {
    if (unit === '$') return '$' + val.toLocaleString('en-US', { maximumFractionDigits: 0 });
    if (unit === '%') return val.toFixed(2) + '%';
    if (unit === 'ms') return Math.round(val) + 'ms';
    if (unit === 'rps') return val.toLocaleString('en-US', { maximumFractionDigits: 0 });
    if (unit === 'GB') return val.toFixed(1) + ' GB';
    if (unit === 'MB/s') return Math.round(val) + ' MB/s';
    return val.toLocaleString('en-US', { maximumFractionDigits: 0 });
  }
  function sparklineSVG(points, color, width, height) {
    const min = Math.min(...points);
    const max = Math.max(...points);
    const range = max - min || 1;
    const stepX = width / (points.length - 1);
    const pts = points.map((v, i) => {
      const x = i * stepX;
      const y = height - ((v - min) / range) * (height - 4) - 2;
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    const area = pts + ' ' + width.toFixed(1) + ',' + (height + 2).toFixed(1) + ' 0,' + (height + 2).toFixed(1);
    return '<svg viewBox="0 0 ' + width + ' ' + height + '" preserveAspectRatio="none">' +
      '<polyline points="' + pts + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>' +
      '<polygon points="' + area + '" fill="' + color + '" opacity="0.1"/>' +
      '</svg>';
  }
  function panelHTML(p) {
    const cls = ['panel', p.size, p.locked ? 'locked' : ''].filter(Boolean).join(' ');
    const metric = p.metrics;
    const trendCls = metric.trend === 'up' ? 'trend-up' : 'trend-down';
    const trendSign = metric.trend === 'up' ? '+' : '';
    const spark = sparklineSVG(p.sparkline, p.color, 200, 40);
    const dur = attentionData[p.id] ? (attentionData[p.id].duration / 1000).toFixed(0) + 's viewed' : '0s viewed';
    return '<div class="' + cls + '" data-panel-id="' + p.id + '" data-rank="' + p.rank + '">' +
      '<div class="panel-duration">' + dur + '</div>' +
      '<div class="panel-header">' +
        '<div class="panel-title">' + p.title + '</div>' +
        '<div class="panel-controls">' +
          '<button class="panel-ctrl lock-btn' + (p.locked ? ' locked' : '') + '" data-action="lock" data-panel="' + p.id + '" title="' + (p.locked ? 'Unlock' : 'Lock') + ' position">' + (p.locked ? 'L' : '') + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body">' +
        '<div class="panel-metric">' + formatMetric(metric.current, p.unit) + '</div>' +
        '<div class="panel-sub ' + trendCls + '">' + trendSign + metric.delta + (p.unit === '%' ? 'pp' : p.unit) + ' vs last cycle</div>' +
        '<div class="panel-chart">' + spark + '</div>' +
      '</div>' +
      '<div class="rank-indicator">#' + p.rank + '</div>' +
    '</div>';
  }
  function render() {
    const sorted = [...panels].sort((a, b) => {
      if (a.locked && b.locked) return 0;
      if (a.locked) return -1;
      if (b.locked) return 1;
      return a.rank - b.rank;
    });
    const dominant = sorted.find(p => p.size === 'dominant');
    const normal = sorted.filter(p => p.size === 'normal');
    const compact = sorted.filter(p => p.size === 'compact');
    const sections = [];
    if (dominant) sections.push(dominant);
    if (normal.length) sections.push(...normal);
    if (compact.length) {
      sections.push({ _sectionLabel: 'Compact — low-usage panels' });
      sections.push(...compact);
    }
    let cols = 4;
    if (dominant) cols = Math.max(cols, 4);
    const dashboard = document.getElementById('dashboard');
    dashboard.style.gridTemplateColumns = 'repeat(' + cols + ', 1fr)';
    dashboard.innerHTML = '';
    sections.forEach(item => {
      if (item._sectionLabel) {
        const label = document.createElement('div');
        label.className = 'section-label';
        label.textContent = item._sectionLabel;
        dashboard.appendChild(label);
      } else {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = panelHTML(item);
        const el = wrapper.firstElementChild;
        dashboard.appendChild(el);
      }
    });
    bindPanelEvents();
    updateHeatmap();
    saveState();
  }
  function bindPanelEvents() {
    document.querySelectorAll('.panel').forEach(el => {
      const panelId = el.dataset.panelId;
      el.addEventListener('mouseenter', () => {
        viewStartTimes[panelId] = Date.now();
        if (!hoverTimers[panelId]) {
          hoverTimers[panelId] = setTimeout(() => {
            recordInteraction(panelId, 'hover');
          }, HOVER_THRESHOLD_MS);
        }
      });
      el.addEventListener('mouseleave', () => {
        if (viewStartTimes[panelId]) {
          const dur = Date.now() - viewStartTimes[panelId];
          recordViewDuration(panelId, dur);
          delete viewStartTimes[panelId];
        }
        if (hoverTimers[panelId]) {
          clearTimeout(hoverTimers[panelId]);
          delete hoverTimers[panelId];
        }
      });
      el.addEventListener('click', (e) => {
        if (e.target.closest('[data-action="lock"]')) return;
        recordInteraction(panelId, 'click');
      });
    });
    document.querySelectorAll('[data-action="lock"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        lockPanel(btn.dataset.panel);
      });
    });
  }
  function updateHeatmap() {
    const overlay = document.getElementById('heatmapOverlay');
    if (overlay.classList.contains('hidden')) return;
    overlay.innerHTML = '';
    const now = Date.now();
    let maxScore = 0;
    const scores = [];
    document.querySelectorAll('.panel').forEach(el => {
      const pid = el.dataset.panelId;
      const score = computeAttentionScore(attentionData[pid] || { frequency: 0, duration: 0, lastInteraction: 0 }, now);
      scores.push({ el, score });
      if (score > maxScore) maxScore = score;
    });
    scores.forEach(({ el, score }) => {
      const rect = el.getBoundingClientRect();
      const intensity = maxScore > 0 ? score / maxScore : 0;
      const alpha = 0.08 + intensity * 0.3;
      const cell = document.createElement('div');
      cell.className = 'heat-cell';
      cell.style.cssText = [
        'left:' + rect.left + 'px',
        'top:' + rect.top + 'px',
        'width:' + rect.width + 'px',
        'height:' + rect.height + 'px',
        'background:rgba(108,140,255,' + alpha.toFixed(2) + ')',
      ].join(';');
      overlay.appendChild(cell);
    });
  }
  function rankTick() {
    const before = panels.map(p => ({ id: p.id, rank: p.rank }));
    computeRanks();
    const shifted = panels.filter(p => {
      const old = before.find(b => b.id === p.id);
      return old && old.rank !== p.rank;
    });
    render();
    if (shifted.length > 0) {
      shifted.forEach(p => {
        const el = document.querySelector('[data-panel-id="' + p.id + '"]');
        if (el) {
          el.classList.add('rank-shifting');
          setTimeout(() => el.classList.remove('rank-shifting'), 400);
        }
      });
    }
  }
  document.getElementById('btnHeatmap').addEventListener('click', function() {
    const overlay = document.getElementById('heatmapOverlay');
    overlay.classList.toggle('hidden');
    this.classList.toggle('active');
    updateHeatmap();
  });
  document.getElementById('btnReset').addEventListener('click', () => {
    if (confirm('Reset all tracking data and layout preferences?')) resetAll();
  });
  window.addEventListener('resize', () => { updateHeatmap(); });
  window.addEventListener('scroll', () => { updateHeatmap(); });
  computeRanks();
  render();
  setInterval(rankTick, RANK_UPDATE_INTERVAL);
  window._adaptiveLayout = {
    getPanels: () => panels,
    getAttentionData: () => attentionData,
    lockPanel,
    resetAll,
    forceRank: () => { computeRanks(); render(); },
  };
})();
</script>
</body>
</html>
```