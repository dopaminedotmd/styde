<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f1117;color:#e1e4e8;font-family:system-ui,-apple-system,sans-serif;min-height:100vh}
header{background:#161b22;border-bottom:1px solid #30363d;padding:12px 20px;display:flex;align-items:center;justify-content:space-between}
header h1{font-size:16px;font-weight:600;color:#58a6ff}
.header-actions{display:flex;gap:8px;align-items:center}
.btn{background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .15s}
.btn:hover{background:#30363d;border-color:#58a6ff}
.btn.active{background:#1f6feb33;border-color:#58a6ff;color:#58a6ff}
.rank-badge{font-size:11px;color:#8b949e;margin-left:8px}
#dashboard{display:grid;gap:12px;padding:16px;transition:all .4s ease}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;transition:all .4s ease;position:relative;display:flex;flex-direction:column}
.panel.locked{border-color:#d29922}
.panel.compact{grid-row:span 1!important}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#1c2128;border-bottom:1px solid #30363d;cursor:move;user-select:none}
.panel-header h2{font-size:13px;font-weight:600;color:#e6edf3}
.panel-controls{display:flex;gap:6px;align-items:center}
.panel-controls button{background:none;border:none;color:#8b949e;cursor:pointer;padding:2px 6px;border-radius:4px;font-size:14px;line-height:1;transition:all .15s}
.panel-controls button:hover{color:#e6edf3;background:#30363d}
.panel-controls button.lock-btn.locked{color:#d29922}
.panel-controls button.expand-btn{font-size:12px}
.panel-body{padding:14px;flex:1;overflow:auto;min-height:80px}
.panel.compact .panel-body{max-height:60px;overflow:hidden;position:relative}
.panel.compact .panel-body::after{content:'';position:absolute;bottom:0;left:0;right:0;height:30px;background:linear-gradient(transparent,#161b22)}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:40px}
.sparkline-bar{flex:1;background:#58a6ff;border-radius:2px 2px 0 0;min-height:2px;transition:height .3s}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:8px}
.metric-item{text-align:center;padding:8px;background:#0d1117;border-radius:6px}
.metric-value{font-size:20px;font-weight:700;color:#58a6ff}
.metric-label{font-size:10px;color:#8b949e;margin-top:2px;text-transform:uppercase}
.heatmap{height:80px;display:grid;grid-template-columns:repeat(7,1fr);gap:2px;align-items:end}
.heatmap-cell{border-radius:2px;min-height:4px;transition:all .3s}
.attention-bar{height:4px;background:#21262d;border-radius:2px;margin-top:4px;overflow:hidden}
.attention-fill{height:100%;background:#58a6ff;border-radius:2px;transition:width .5s ease}
.empty-state{color:#484f58;text-align:center;padding:40px 20px;grid-column:1/-1}
.lock-indicator{position:absolute;top:4px;left:4px;width:6px;height:6px;background:#d29922;border-radius:50%;opacity:0;transition:opacity .2s}
.panel.locked .lock-indicator{opacity:1}
.resize-handle{position:absolute;bottom:0;right:0;width:16px;height:16px;cursor:nwse-resize;background:linear-gradient(135deg,transparent 50%,#30363d 50%);border-radius:0 0 6px 0;opacity:0;transition:opacity .2s}
.panel:hover .resize-handle{opacity:1}
#more-section{border-top:2px dashed #30363d;padding-top:12px;margin-top:8px}
.more-label{font-size:11px;color:#8b949e;text-transform:uppercase;margin-bottom:8px;text-align:center}
.stats-row{display:flex;gap:16px;font-size:11px;color:#8b949e;margin-top:8px}
.compact-preview{display:flex;gap:4px;align-items:flex-end;height:20px}
.compact-preview .mini-bar{width:3px;background:#30363d;border-radius:1px;min-height:2px}
</style>
</head>
<body>
<header>
<h1>Adaptive Metric Layout</h1>
<div class="header-actions">
<button class="btn" onclick="resetAll()">Reset Tracking</button>
<button class="btn" onclick="applyAutoLayout()">Re-Apply Layout</button>
<span class="rank-badge" id="sessionInfo"></span>
</div>
</header>
<div id="dashboard"></div>
<script>
const STORAGE_KEY = 'adaptive_layout_v1';
const DECAY_DAYS = 14;
const RANK_WEIGHTS = { frequency: 0.35, duration: 0.45, recency: 0.20 };
const COMPACT_THRESHOLD = 0.15;
const VIEW_INTERVAL = 2000;
let panels = [
  { id: 'revenue', title: 'Revenue', type: 'metric', value: '$45.2K', sub: '+12.3%', locked: false, overridePos: null, overrideSpan: null },
  { id: 'users', title: 'Active Users', type: 'metric', value: '8,421', sub: '+5.7%', locked: false, overridePos: null, overrideSpan: null },
  { id: 'conversion', title: 'Conversion Rate', type: 'metric', value: '3.24%', sub: '-0.8%', locked: false, overridePos: null, overrideSpan: null },
  { id: 'latency', title: 'API Latency', type: 'sparkline', data: [42,38,45,40,35,32,30,28,31,29,27,25,28,26,24,22,25,23,20,18], locked: false, overridePos: null, overrideSpan: null },
  { id: 'errors', title: 'Error Rate', type: 'sparkline', data: [5,3,7,4,2,1,3,2,0,1,2,0,1,3,1,0,2,1,0,1], locked: false, overridePos: null, overrideSpan: null },
  { id: 'traffic', title: 'Traffic Sources', type: 'heatmap', data: [0.8,0.6,0.9,0.4,0.7,0.5,0.3,0.9,0.8,0.6,0.7,0.5,0.4,0.8,0.9,0.6,0.5,0.7,0.8,0.4,0.3], locked: false, overridePos: null, overrideSpan: null },
  { id: 'billing', title: 'Billing Overview', type: 'metric', value: '$12.8K', sub: 'MRR', locked: false, overridePos: null, overrideSpan: null },
  { id: 'sessions', title: 'Sessions', type: 'sparkline', data: [120,135,142,138,150,155,148,160,165,158,170,175,168,180,185,178,190,195,188,200], locked: false, overridePos: null, overrideSpan: null },
  { id: 'churn', title: 'Churn Rate', type: 'metric', value: '1.8%', sub: '-0.3%', locked: false, overridePos: null, overrideSpan: null },
  { id: 'storage', title: 'Storage Usage', type: 'metric', value: '67%', sub: '2.1 TB', locked: false, overridePos: null, overrideSpan: null },
  { id: 'bandwidth', title: 'Bandwidth', type: 'sparkline', data: [80,82,78,85,90,88,92,95,90,88,85,82,86,89,92,88,85,90,87,84], locked: false, overridePos: null, overrideSpan: null },
  { id: 'cpu', title: 'CPU Load', type: 'sparkline', data: [45,42,48,50,47,44,40,38,42,40,37,35,38,35,32,30,28,25,22,20], locked: false, overridePos: null, overrideSpan: null },
];
let tracking = loadTracking();
let viewTimers = {};
let observer = null;
function loadTracking() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  const t = {};
  panels.forEach(p => {
    t[p.id] = { views: 0, totalDuration: 0, lastViewed: null, interactions: 0, collapseEvents: 0, expandEvents: 0 };
  });
  return t;
}
function saveTracking() { localStorage.setItem(STORAGE_KEY, JSON.stringify(tracking)); }
function trackView(panelId) {
  if (!tracking[panelId]) return;
  tracking[panelId].views++;
  tracking[panelId].lastViewed = Date.now();
  saveTracking();
}
function trackInteraction(panelId) {
  if (!tracking[panelId]) return;
  tracking[panelId].interactions++;
  tracking[panelId].lastViewed = Date.now();
  saveTracking();
}
function trackDuration(panelId, ms) {
  if (!tracking[panelId]) return;
  tracking[panelId].totalDuration += ms;
  saveTracking();
}
function trackCollapse(panelId, collapsed) {
  if (!tracking[panelId]) return;
  if (collapsed) tracking[panelId].collapseEvents++;
  else tracking[panelId].expandEvents++;
  tracking[panelId].lastViewed = Date.now();
  saveTracking();
}
function computeAttentionScore(panelId) {
  const t = tracking[panelId];
  if (!t || t.views === 0) return 0;
  const freqScore = Math.min(t.views / 50, 1.0);
  const durScore = Math.min(t.totalDuration / 600000, 1.0);
  let recencyScore = 0;
  if (t.lastViewed) {
    const hoursAgo = (Date.now() - t.lastViewed) / 3600000;
    const daysAgo = hoursAgo / 24;
    recencyScore = Math.exp(-daysAgo / DECAY_DAYS);
  }
  return freqScore * RANK_WEIGHTS.frequency + durScore * RANK_WEIGHTS.duration + recencyScore * RANK_WEIGHTS.recency;
}
function rankPanels() {
  return panels.map(p => ({
    ...p,
    attentionScore: computeAttentionScore(p.id)
  })).sort((a, b) => b.attentionScore - a.attentionScore);
}
function getLayout() {
  let ranked = rankPanels();
  let lockedPanels = [];
  let unlockedPanels = [];
  ranked.forEach((p, i) => {
    if (p.locked && p.overridePos !== null) {
      lockedPanels.push({ ...p, _rank: i, _origIndex: i });
    } else {
      unlockedPanels.push({ ...p, _rank: i });
    }
  });
  let layout = [];
  let occupied = new Set();
  lockedPanels.forEach(p => {
    let pos = p.overridePos;
    if (pos !== null && !occupied.has(pos)) {
      layout[pos] = p;
      occupied.add(pos);
    }
  });
  let nextPos = 0;
  unlockedPanels.forEach(p => {
    while (occupied.has(nextPos)) nextPos++;
    layout[nextPos] = p;
    occupied.add(nextPos);
    nextPos++;
  });
  let result = [];
  for (let i = 0; i < layout.length; i++) {
    if (layout[i]) result.push(layout[i]);
  }
  return result;
}
function isCompact(panel) {
  if (panel.locked && panel.overrideSpan !== null) return panel.overrideSpan === 'compact';
  return panel.attentionScore < COMPACT_THRESHOLD;
}
function renderSparkline(id, data) {
  if (!data || data.length === 0) return '<div style="color:#484f58;padding:20px;text-align:center">No data</div>';
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const bars = data.slice(-20).map(v => {
    const h = ((v - min) / range) * 100;
    const color = v > (max + min) / 2 ? '#3fb950' : v < (max + min) / 3 ? '#f85149' : '#58a6ff';
    return `<div class="sparkline-bar" style="height:${Math.max(h,4)}%;background:${color}" title="${v}"></div>`;
  }).join('');
  return `<div class="sparkline">${bars}</div>`;
}
function renderHeatmap(id, data) {
  if (!data || data.length === 0) return '<div style="color:#484f58;padding:20px;text-align:center">No data</div>';
  const cells = data.slice(0, 21).map(v => {
    const intensity = Math.round(v * 255);
    return `<div class="heatmap-cell" style="height:${Math.max(v*100,4)}%;background:rgb(${intensity},${Math.round(intensity*0.6)},255)" title="${(v*100).toFixed(0)}%"></div>`;
  }).join('');
  return `<div class="heatmap">${cells}</div>`;
}
function renderPanelBody(panel) {
  switch(panel.type) {
    case 'sparkline': return renderSparkline(panel.id, panel.data);
    case 'heatmap': return renderHeatmap(panel.id, panel.data);
    case 'metric':
    default:
      return `<div class="metric-item"><div class="metric-value">${panel.value}</div><div class="metric-label">${panel.sub}</div></div>`;
  }
}
function renderCompactBody(panel) {
  switch(panel.type) {
    case 'sparkline':
      const bars = (panel.data || []).slice(-20).map(v => `<div class="mini-bar" style="height:${Math.max(v/Math.max(...panel.data,1)*100,10)}%"></div>`).join('');
      return `<div class="compact-preview">${bars}</div>`;
    case 'heatmap':
      const dots = (panel.data || []).slice(0,10).map(v => `<div class="mini-bar" style="height:${Math.max(v*100,10)}%;background:rgb(${Math.round(v*255)},100,255)"></div>`).join('');
      return `<div class="compact-preview">${dots}</div>`;
    default:
      return `<div style="font-size:14px;font-weight:600;color:#58a6ff">${panel.value || '—'}</div>`;
  }
}
function renderDashboard() {
  const layout = getLayout();
  const container = document.getElementById('dashboard');
  const compactPanels = [];
  const visiblePanels = [];
  layout.forEach(p => {
    if (isCompact(p) && !p.locked) compactPanels.push(p);
    else visiblePanels.push(p);
  });
  let cols = Math.min(visiblePanels.length, 4);
  if (cols < 1) cols = 1;
  if (visiblePanels.length <= 2) cols = visiblePanels.length;
  container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
  let html = '';
  visiblePanels.forEach(p => {
    const compact = isCompact(p);
    const score = (p.attentionScore * 100).toFixed(1);
    const lockClass = p.locked ? ' locked' : '';
    const compactClass = compact ? ' compact' : '';
    const spanStyle = (!compact && visiblePanels.length <= 2) ? 'grid-column:span 1' : '';
    html += `
      <div class="panel${lockClass}${compactClass}" data-panel-id="${p.id}" style="${spanStyle}">
        <div class="lock-indicator"></div>
        <div class="panel-header" draggable="true" data-panel-id="${p.id}">
          <h2>${p.title}</h2>
          <div class="panel-controls">
            <span style="font-size:10px;color:#484f58;margin-right:4px">${score}%</span>
            <button class="lock-btn${p.locked?' locked':''}" data-action="lock" data-panel-id="${p.id}" title="${p.locked?'Unlock':'Lock'} position">${p.locked?'⚓':'🔓'}</button>
            <button class="expand-btn" data-action="toggle-compact" data-panel-id="${p.id}" title="Expand">${compact ? '⤢' : '⊟'}</button>
          </div>
        </div>
        <div class="panel-body">
          ${compact ? renderCompactBody(p) : renderPanelBody(p)}
        </div>
        <div class="attention-bar"><div class="attention-fill" style="width:${Math.min(score,100)}%"></div></div>
        <div class="resize-handle" data-panel-id="${p.id}"></div>
      </div>`;
  });
  if (compactPanels.length > 0) {
    html += `<div id="more-section" style="grid-column:1/-1">
      <div class="more-label">More (${compactPanels.length} auto-compacted)</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">`;
    compactPanels.forEach(p => {
      html += `<div class="panel compact" data-panel-id="${p.id}" style="flex:1;min-width:160px;max-width:240px">
        <div class="panel-header">
          <h2 style="font-size:11px">${p.title}</h2>
          <div class="panel-controls">
            <button class="lock-btn" data-action="lock" data-panel-id="${p.id}" title="Lock">🔓</button>
            <button class="expand-btn" data-action="expand" data-panel-id="${p.id}" title="Move to main">⤢</button>
          </div>
        </div>
        <div class="panel-body">${renderCompactBody(p)}</div>
      </div>`;
    });
    html += '</div></div>';
  }
  if (visiblePanels.length === 0 && compactPanels.length === 0) {
    html = '<div class="empty-state">No panels to display</div>';
  }
  container.innerHTML = html;
  bindEvents();
  setupObserver();
  updateSessionInfo();
}
function bindEvents() {
  document.querySelectorAll('.lock-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panelId = btn.dataset.panelId;
      const panel = panels.find(p => p.id === panelId);
      if (!panel) return;
      panel.locked = !panel.locked;
      if (panel.locked) {
        const idx = getLayout().findIndex(p => p.id === panelId);
        panel.overridePos = idx >= 0 ? idx : null;
      } else {
        panel.overridePos = null;
        panel.overrideSpan = null;
      }
      trackInteraction(panelId);
      savePanelState();
      renderDashboard();
    });
  });
  document.querySelectorAll('[data-action="toggle-compact"]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panelId = btn.dataset.panelId;
      const panel = panels.find(p => p.id === panelId);
      if (!panel) return;
      const currentlyCompact = isCompact(panel);
      panel.locked = true;
      panel.overrideSpan = currentlyCompact ? 'full' : 'compact';
      const idx = getLayout().findIndex(p => p.id === panelId);
      panel.overridePos = idx >= 0 ? idx : null;
      trackCollapse(panelId, !currentlyCompact);
      trackInteraction(panelId);
      savePanelState();
      renderDashboard();
    });
  });
  document.querySelectorAll('[data-action="expand"]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const panelId = btn.dataset.panelId;
      const panel = panels.find(p => p.id === panelId);
      if (!panel) return;
      panel.locked = true;
      panel.overrideSpan = 'full';
      trackInteraction(panelId);
      savePanelState();
      renderDashboard();
    });
  });
  document.querySelectorAll('.panel-header[draggable]').forEach(header => {
    header.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', header.dataset.panelId);
      header.closest('.panel').style.opacity = '0.5';
    });
    header.addEventListener('dragend', e => {
      header.closest('.panel').style.opacity = '1';
    });
  });
  document.querySelectorAll('.panel').forEach(panelEl => {
    panelEl.addEventListener('dragover', e => {
      e.preventDefault();
      panelEl.style.borderColor = '#58a6ff';
    });
    panelEl.addEventListener('dragleave', e => {
      panelEl.style.borderColor = '';
    });
    panelEl.addEventListener('drop', e => {
      e.preventDefault();
      panelEl.style.borderColor = '';
      const srcId = e.dataTransfer.getData('text/plain');
      const dstId = panelEl.dataset.panelId;
      if (srcId && dstId && srcId !== dstId) {
        const layout = getLayout();
        const srcIdx = layout.findIndex(p => p.id === srcId);
        const dstIdx = layout.findIndex(p => p.id === dstId);
        if (srcIdx >= 0 && dstIdx >= 0) {
          const srcPanel = panels.find(p => p.id === srcId);
          const dstPanel = panels.find(p => p.id === dstId);
          if (srcPanel && dstPanel) {
            srcPanel.locked = true;
            srcPanel.overridePos = dstIdx;
            dstPanel.locked = true;
            dstPanel.overridePos = srcIdx;
            trackInteraction(srcId);
            trackInteraction(dstId);
            savePanelState();
            renderDashboard();
          }
        }
      }
    });
  });
  document.querySelectorAll('.resize-handle').forEach(handle => {
    let startX, startY, panelEl;
    handle.addEventListener('mousedown', e => {
      e.preventDefault();
      e.stopPropagation();
      panelEl = handle.closest('.panel');
      startX = e.clientX;
      startY = e.clientY;
      const onMove = ev => {
        const dx = ev.clientX - startX;
        const dy = ev.clientY - startY;
        const newW = Math.max(200, (panelEl.offsetWidth + dx));
        const newH = Math.max(120, (panelEl.offsetHeight + dy));
        panelEl.style.width = newW + 'px';
        panelEl.style.minHeight = newH + 'px';
        startX = ev.clientX;
        startY = ev.clientY;
      };
      const onUp = () => {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });
  });
}
function setupObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      if (entry.isIntersecting) {
        if (!viewTimers[panelId]) {
          viewTimers[panelId] = { start: Date.now(), interval: null };
          trackView(panelId);
          viewTimers[panelId].interval = setInterval(() => {
            if (viewTimers[panelId]) {
              const elapsed = Date.now() - viewTimers[panelId].start;
              trackDuration(panelId, VIEW_INTERVAL);
              viewTimers[panelId].start = Date.now();
            }
          }, VIEW_INTERVAL);
        }
      } else {
        if (viewTimers[panelId]) {
          const elapsed = Date.now() - viewTimers[panelId].start;
          trackDuration(panelId, elapsed);
          clearInterval(viewTimers[panelId].interval);
          delete viewTimers[panelId];
        }
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
function applyAutoLayout() {
  panels.forEach(p => {
    if (!p.locked) {
      p.overridePos = null;
      p.overrideSpan = null;
    }
  });
  savePanelState();
  renderDashboard();
}
function resetAll() {
  if (confirm('Reset all tracking data and layout overrides?')) {
    tracking = {};
    panels.forEach(p => {
      tracking[p.id] = { views: 0, totalDuration: 0, lastViewed: null, interactions: 0, collapseEvents: 0, expandEvents: 0 };
      p.locked = false;
      p.overridePos = null;
      p.overrideSpan = null;
    });
    saveTracking();
    savePanelState();
    renderDashboard();
  }
}
function savePanelState() {
  try {
    const state = panels.map(p => ({
      id: p.id, locked: p.locked, overridePos: p.overridePos, overrideSpan: p.overrideSpan
    }));
    localStorage.setItem(STORAGE_KEY + '_panels', JSON.stringify(state));
  } catch(e) {}
}
function loadPanelState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY + '_panels');
    if (raw) {
      const state = JSON.parse(raw);
      state.forEach(s => {
        const panel = panels.find(p => p.id === s.id);
        if (panel) {
          panel.locked = s.locked || false;
          panel.overridePos = s.overridePos || null;
          panel.overrideSpan = s.overrideSpan || null;
        }
      });
    }
  } catch(e) {}
}
function updateSessionInfo() {
  const totalViews = Object.values(tracking).reduce((s, t) => s + t.views, 0);
  const totalInteractions = Object.values(tracking).reduce((s, t) => s + t.interactions, 0);
  document.getElementById('sessionInfo').textContent = `views:${totalViews} | clicks:${totalInteractions}`;
}
loadPanelState();
renderDashboard();
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    Object.keys(viewTimers).forEach(panelId => {
      if (viewTimers[panelId]) {
        const elapsed = Date.now() - viewTimers[panelId].start;
        trackDuration(panelId, elapsed);
        clearInterval(viewTimers[panelId].interval);
        viewTimers[panelId].start = Date.now();
      }
    });
  } else {
    Object.keys(viewTimers).forEach(panelId => {
      if (viewTimers[panelId] && document.querySelector(`[data-panel-id="${panelId}"]`)) {
        viewTimers[panelId].start = Date.now();
      }
    });
  }
});
window.addEventListener('beforeunload', () => {
  Object.keys(viewTimers).forEach(panelId => {
    if (viewTimers[panelId]) {
      const elapsed = Date.now() - viewTimers[panelId].start;
      trackDuration(panelId, elapsed);
      clearInterval(viewTimers[panelId].interval);
      delete viewTimers[panelId];
    }
  });
  savePanelState();
});
</script>
</body>
</html>