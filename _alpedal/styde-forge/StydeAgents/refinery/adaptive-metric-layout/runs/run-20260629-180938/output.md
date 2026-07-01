<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --muted: #8b949e;
  --accent: #58a6ff;
  --green: #3fb950;
  --red: #f85149;
  --orange: #d2991d;
  --purple: #a371f7;
  --radius: 8px;
  --gap: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
}
header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
header h1 { font-size: 18px; font-weight: 600; color: var(--text); }
.badge {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  color: var(--muted);
}
.badge span { color: var(--accent); font-weight: 600; }
.btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: background .15s;
}
.btn:hover { background: #1c2333; }
.btn.accent { border-color: var(--accent); color: var(--accent); }
.btn.danger { border-color: var(--red); color: var(--red); }
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--gap);
  grid-auto-rows: minmax(160px, auto);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: grid-column .4s ease, grid-row .4s ease, opacity .3s, transform .3s;
  position: relative;
}
.panel.compact { grid-row: auto !important; min-height: 80px; }
.panel.compact .panel-body { max-height: 80px; overflow: hidden; opacity: .65; }
.panel.compact .panel-content { pointer-events: none; }
.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  cursor: grab;
  user-select: none;
  background: rgba(255,255,255,.02);
}
.panel-header:active { cursor: grabbing; }
.panel-header .drag-handle { color: var(--muted); font-size: 14px; line-height: 1; }
.panel-title { font-size: 13px; font-weight: 600; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none;
  border: none;
  color: var(--muted);
  cursor: pointer;
  font-size: 14px;
  padding: 2px 5px;
  border-radius: 4px;
  line-height: 1;
  transition: color .15s, background .15s;
}
.panel-actions button:hover { color: var(--text); background: rgba(255,255,255,.06); }
.panel-actions button.locked { color: var(--orange); }
.panel-actions button.compacted { color: var(--purple); }
.panel-body { flex: 1; padding: 12px; overflow: auto; }
.panel-body.metric-large { font-size: 36px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.panel-body.metric-large .trend { font-size: 14px; font-weight: 500; }
.trend.up { color: var(--green); }
.trend.down { color: var(--red); }
.sparkline { display: flex; align-items: flex-end; gap: 2px; height: 60px; }
.sparkline .bar {
  flex: 1;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
  min-width: 4px;
  transition: height .5s ease;
}
.sparkline .bar.low { opacity: .35; }
.mini-table { width: 100%; font-size: 12px; border-collapse: collapse; }
.mini-table th { text-align: left; color: var(--muted); font-weight: 500; padding: 3px 6px; border-bottom: 1px solid var(--border); }
.mini-table td { padding: 3px 6px; }
.status-dots { display: flex; gap: 6px; flex-wrap: wrap; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; }
.status-dot.ok { background: var(--green); }
.status-dot.warn { background: var(--orange); }
.status-dot.down { background: var(--red); }
.status-label { font-size: 12px; color: var(--muted); }
.progress-bar { height: 6px; background: var(--border); border-radius: 3px; margin: 4px 0; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; transition: width .6s ease; }
.gauge-ring { width: 80px; height: 80px; }
.log-lines { font-family: 'SF Mono', 'Cascadia Code', monospace; font-size: 11px; color: var(--muted); line-height: 1.6; }
.log-lines .err { color: var(--red); }
.log-lines .warn { color: var(--orange); }
.drag-ghost { opacity: .5; border: 2px dashed var(--accent); }
.drag-over { border-color: var(--accent); box-shadow: 0 0 12px rgba(88,166,255,.25); }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 16px;
  font-size: 13px;
  z-index: 1000;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity .25s, transform .25s;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.rank-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 10px;
  color: var(--muted);
  background: rgba(255,255,255,.04);
  border-radius: 3px;
  padding: 1px 5px;
  pointer-events: none;
}
.panel.pinned { border-color: var(--orange); }
.panel.pinned .panel-header { background: rgba(210,153,29,.06); }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="badge">Sessions: <span id="sessionCount">0</span></div>
  <div class="badge">Events: <span id="eventCount">0</span></div>
  <div class="badge">Layout age: <span id="layoutAge">--</span></div>
  <button class="btn accent" onclick="resetLayout()" title="Clear all tracking data and reset layout">Reset</button>
  <button class="btn" onclick="exportData()">Export</button>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY = 'adaptive_layout_v1';
const COMPACT_THRESHOLD_RANK = 7;
const RECENCY_WINDOWS = [
  { maxHours: 1, weight: 1.0 },
  { maxHours: 24, weight: 0.9 },
  { maxHours: 72, weight: 0.7 },
  { maxHours: 168, weight: 0.5 },
  { maxHours: 336, weight: 0.3 },
  { maxHours: Infinity, weight: 0.1 }
];
function recencyWeight(lastTs) {
  const hours = (Date.now() - lastTs) / 3600000;
  for (const w of RECENCY_WINDOWS) {
    if (hours <= w.maxHours) return w.weight;
  }
  return 0.1;
}
const PANEL_DEFS = [
  { id: 'revenue', title: 'Revenue Overview', type: 'metric', value: '$48,294', trend: '+12.3%', trendDir: 'up' },
  { id: 'users', title: 'Active Users', type: 'metric', value: '18,442', trend: '+5.7%', trendDir: 'up' },
  { id: 'conversion', title: 'Conversion Rate', type: 'gauge', value: 3.42 },
  { id: 'servers', title: 'Server Status', type: 'status', servers: [{name:'US-East',status:'ok'},{name:'US-West',status:'ok'},{name:'EU-Central',status:'ok'},{name:'APAC',status:'warn'},{name:'SA-East',status:'ok'}] },
  { id: 'transactions', title: 'Recent Transactions', type: 'table', rows: [{id:'TX-8821',amt:'$1,240',status:'Complete'},{id:'TX-8820',amt:'$89',status:'Complete'},{id:'TX-8819',amt:'$3,450',status:'Pending'},{id:'TX-8818',amt:'$567',status:'Failed'}] },
  { id: 'errors', title: 'Error Log', type: 'log', lines: [{l:'Connection pool exhausted',s:'err'},{l:'Rate limit approaching 80%',s:'warn'},{l:'Cache miss ratio 0.34',s:'info'},{l:'Worker-3 heartbeat timeout',s:'err'},{l:'SSL cert renews in 14d',s:'warn'}] },
  { id: 'health', title: 'System Health', type: 'progress', metrics: [{label:'CPU',pct:34,color:'var(--green)'},{label:'Memory',pct:67,color:'var(--orange)'},{label:'Disk',pct:42,color:'var(--green)'},{label:'Network',pct:12,color:'var(--green)'}] },
  { id: 'latency', title: 'API Latency', type: 'spark', points: [45,62,38,71,55,48,92,44,58,63,47,52,39,81,56,49,61,43,57,68] },
  { id: 'queue', title: 'Queue Depth', type: 'metric', value: '1,247', trend: '-3.1%', trendDir: 'down' },
  { id: 'memory', title: 'Memory Usage', type: 'spark', points: [34,38,42,39,45,51,48,55,52,49,46,44,41,47,53,50,48,45,42,40] },
  { id: 'uptime', title: 'Uptime', type: 'metric', value: '99.97%', trend: '+0.02%', trendDir: 'up' },
];
let state = loadState();
let viewEntries = new Map();
let intersectionObserver = null;
function defaultState() {
  return {
    panels: {},
    layoutAge: Date.now(),
    sessionCount: 0,
    eventCount: 0
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const s = JSON.parse(raw);
      if (s.panels && typeof s.panels === 'object') return s;
    }
  } catch (e) {}
  return defaultState();
}
function saveState() {
  state.layoutAge = Date.now();
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    toast('Storage full — clearing old data');
    state = defaultState();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }
}
function ensurePanel(id) {
  if (!state.panels[id]) {
    state.panels[id] = {
      viewCount: 0,
      totalViewMs: 0,
      clickCount: 0,
      expandCount: 0,
      collapseCount: 0,
      lastInteraction: 0,
      locked: false,
      lockedPosition: null,
      compacted: false,
      manualOrder: null
    };
  }
  return state.panels[id];
}
function attentionScore(p) {
  const avgDuration = p.viewCount > 0 ? (p.totalViewMs / p.viewCount / 1000) : 0;
  const freq = p.clickCount + p.expandCount + Math.max(1, p.viewCount);
  const recency = p.lastInteraction > 0 ? recencyWeight(p.lastInteraction) : 0.05;
  return freq * avgDuration * recency;
}
function computeRanks() {
  const entries = PANEL_DEFS.map(def => {
    const p = ensurePanel(def.id);
    return { id: def.id, score: attentionScore(p), locked: p.locked, lockedPosition: p.lockedPosition, manualOrder: p.manualOrder };
  });
  const unlocked = entries.filter(e => !e.locked).sort((a, b) => b.score - a.score);
  const locked = entries.filter(e => e.locked).sort((a, b) => (a.manualOrder ?? 999) - (b.manualOrder ?? 999));
  let rank = 1;
  for (const e of unlocked) { e.rank = rank++; }
  for (const e of locked) { e.rank = rank++; }
  return { ranked: [...locked, ...unlocked.sort((a,b) => b.score - a.score)], entries };
}
function gridPosition(rankIndex, total, isLocked, lockedPos) {
  if (isLocked && lockedPos) {
    return { col: lockedPos.col, row: lockedPos.row, span: lockedPos.span ?? 1 };
  }
  if (rankIndex < 2) {
    const row = Math.floor(rankIndex / 2) * 2 + 1;
    const col = (rankIndex % 2) * 2 + 1;
    return { col, row, span: 2, tier: 1 };
  }
  if (rankIndex < 6) {
    const idx = rankIndex - 2;
    const row = Math.floor(idx / 4) * 2 + 3;
    const col = (idx % 4) + 1;
    return { col, row, span: 1, tier: 2 };
  }
  const idx = rankIndex - 6;
  const row = 7 + Math.floor(idx / 4);
  const col = (idx % 4) + 1;
  return { col, row, span: 1, tier: 3 };
}
function renderPanel(def) {
  const p = ensurePanel(def.id);
  let body = '';
  switch (def.type) {
    case 'metric':
      body = `<div class="panel-body metric-large">${def.value}<span class="trend ${def.trendDir}">${def.trend}</span></div>`;
      break;
    case 'gauge': {
      const pct = def.value / 5 * 100;
      const color = def.value >= 3 ? 'var(--green)' : def.value >= 2 ? 'var(--orange)' : 'var(--red)';
      body = `<div class="panel-body" style="display:flex;align-items:center;gap:16px">
        <svg class="gauge-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" fill="none" stroke="var(--border)" stroke-width="10"/><circle cx="50" cy="50" r="38" fill="none" stroke="${color}" stroke-width="10" stroke-dasharray="${pct * 2.39} 239" stroke-linecap="round" transform="rotate(-90 50 50)" style="transition:stroke-dasharray .6s"/><text x="50" y="54" text-anchor="middle" fill="var(--text)" font-size="18" font-weight="700">${def.value}%</text></svg>
        <div><div style="font-size:24px;font-weight:700">${def.value}%</div><div style="color:var(--muted);font-size:12px">target: 5%</div></div></div>`;
      break;
    }
    case 'status':
      body = `<div class="panel-body"><div class="status-dots">${def.servers.map(s => `<div style="display:flex;align-items:center;gap:4px"><div class="status-dot ${s.status}"></div><span class="status-label">${s.name}</span></div>`).join('')}</div></div>`;
      break;
    case 'table':
      body = `<div class="panel-body"><table class="mini-table"><thead><tr><th>ID</th><th>Amount</th><th>Status</th></tr></thead><tbody>${def.rows.map(r => `<tr><td>${r.id}</td><td>${r.amt}</td><td>${r.status}</td></tr>`).join('')}</tbody></table></div>`;
      break;
    case 'log':
      body = `<div class="panel-body"><div class="log-lines">${def.lines.map(l => `<div class="${l.s}">${l.l}</div>`).join('')}</div></div>`;
      break;
    case 'progress':
      body = `<div class="panel-body">${def.metrics.map(m => `<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;font-size:12px"><span>${m.label}</span><span style="color:var(--muted)">${m.pct}%</span></div><div class="progress-bar"><div class="progress-fill" style="width:${m.pct}%;background:${m.color}"></div></div></div>`).join('')}</div>`;
      break;
    case 'spark': {
      const max = Math.max(...def.points);
      body = `<div class="panel-body"><div class="sparkline">${def.points.map(v => `<div class="bar${v < max * 0.35 ? ' low' : ''}" style="height:${(v / max) * 100}%"></div>`).join('')}</div><div style="font-size:11px;color:var(--muted);margin-top:6px">last ${def.points.length} samples &middot; avg ${Math.round(def.points.reduce((a,b)=>a+b,0)/def.points.length)}ms</div></div>`;
      break;
    }
    default: body = `<div class="panel-body"></div>`;
  }
  return { id: def.id, title: def.title, body, locked: p.locked, compacted: p.compacted };
}
function renderAll() {
  const { ranked, entries } = computeRanks();
  const container = document.getElementById('dashboard');
  container.innerHTML = '';
  const rendered = PANEL_DEFS.map(def => renderPanel(def));
  const map = Object.fromEntries(rendered.map(r => [r.id, r]));
  ranked.forEach((entry, i) => {
    const r = map[entry.id];
    const pos = gridPosition(i, ranked.length, r.locked, entry.lockedPosition);
    const el = document.createElement('div');
    el.className = 'panel' + (r.compacted ? ' compact' : '') + (r.locked ? ' pinned' : '');
    el.id = 'panel-' + entry.id;
    el.dataset.panelId = entry.id;
    el.style.gridColumn = `${pos.col} / span ${pos.span}`;
    el.style.gridRow = `${pos.row}`;
    el.innerHTML = `
      <div class="panel-header" draggable="true">
        <span class="drag-handle">⠿</span>
        <span class="panel-title">${r.title}</span>
        <div class="panel-actions">
          <button class="${r.compacted ? 'compacted' : ''}" data-action="toggle-compact" data-panel="${entry.id}" title="Compact/expand">${r.compacted ? '⊞' : '⊟'}</button>
          <button class="${r.locked ? 'locked' : ''}" data-action="toggle-lock" data-panel="${entry.id}" title="Lock position">${r.locked ? '🔒' : '🔓'}</button>
        </div>
      </div>
      ${r.body}
      <div class="rank-badge">#${entry.rank ?? (i+1)}</div>`;
    container.appendChild(el);
  });
  document.getElementById('sessionCount').textContent = state.sessionCount;
  document.getElementById('eventCount').textContent = state.eventCount;
  document.getElementById('layoutAge').textContent = formatAge(state.layoutAge);
  setupIntersectionObserver();
  attachEventListeners();
  attachDragListeners();
}
function formatAge(ts) {
  if (!ts) return '--';
  const mins = Math.floor((Date.now() - ts) / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return mins + 'm ago';
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return hrs + 'h ago';
  return Math.floor(hrs / 24) + 'd ago';
}
function trackEvent(id, type) {
  const p = ensurePanel(id);
  p.lastInteraction = Date.now();
  state.eventCount++;
  switch (type) {
    case 'view-start':
      viewEntries.set(id, Date.now());
      break;
    case 'view-end': {
      const start = viewEntries.get(id);
      if (start) {
        p.viewCount++;
        p.totalViewMs += Date.now() - start;
        viewEntries.delete(id);
      }
      break;
    }
    case 'click': p.clickCount++; break;
    case 'expand': p.expandCount++; break;
    case 'collapse': p.collapseCount++; break;
  }
  saveState();
  scheduleRerender();
}
let rerenderTimer = null;
function scheduleRerender() {
  if (rerenderTimer) return;
  rerenderTimer = setTimeout(() => {
    rerenderTimer = null;
    renderAll();
  }, 2000);
}
function setupIntersectionObserver() {
  if (intersectionObserver) intersectionObserver.disconnect();
  intersectionObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const id = entry.target.dataset.panelId;
      if (!id) continue;
      if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
        trackEvent(id, 'view-start');
      } else {
        trackEvent(id, 'view-end');
      }
    }
  }, { threshold: [0, 0.5] });
  document.querySelectorAll('.panel').forEach(el => intersectionObserver.observe(el));
}
function attachEventListeners() {
  document.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const id = btn.dataset.panel;
      const action = btn.dataset.action;
      if (action === 'toggle-compact') {
        const p = ensurePanel(id);
        p.compacted = !p.compacted;
        trackEvent(id, p.compacted ? 'collapse' : 'expand');
        saveState();
        renderAll();
      } else if (action === 'toggle-lock') {
        const p = ensurePanel(id);
        p.locked = !p.locked;
        if (p.locked) {
          const el = document.getElementById('panel-' + id);
          if (el) {
            p.lockedPosition = {
              col: parseInt(el.style.gridColumnStart) || 1,
              row: parseInt(el.style.gridRowStart) || 1,
              span: el.style.gridColumnEnd ? parseInt(el.style.gridColumnEnd) - parseInt(el.style.gridColumnStart) : 1
            };
          }
        } else {
          p.lockedPosition = null;
        }
        trackEvent(id, 'click');
        saveState();
        renderAll();
        toast(p.locked ? id + ' locked' : id + ' unlocked');
      }
    });
  });
  document.querySelectorAll('.panel-body').forEach(body => {
    body.addEventListener('click', () => {
      const panel = body.closest('.panel');
      if (panel) trackEvent(panel.dataset.panelId, 'click');
    });
  });
}
function attachDragListeners() {
  let dragSrc = null;
  document.querySelectorAll('.panel-header').forEach(header => {
    header.addEventListener('dragstart', e => {
      dragSrc = header.closest('.panel');
      if (dragSrc) {
        dragSrc.classList.add('drag-ghost');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', dragSrc.dataset.panelId);
      }
    });
    header.addEventListener('dragend', e => {
      if (dragSrc) dragSrc.classList.remove('drag-ghost');
      document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
      dragSrc = null;
    });
  });
  document.querySelectorAll('.panel').forEach(panel => {
    panel.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      panel.classList.add('drag-over');
    });
    panel.addEventListener('dragleave', () => panel.classList.remove('drag-over'));
    panel.addEventListener('drop', e => {
      e.preventDefault();
      panel.classList.remove('drag-over');
      const srcId = e.dataTransfer.getData('text/plain');
      const dstId = panel.dataset.panelId;
      if (srcId && dstId && srcId !== dstId) {
        const srcPanel = ensurePanel(srcId);
        const dstPanel = ensurePanel(dstId);
        const srcEl = document.getElementById('panel-' + srcId);
        srcPanel.locked = true;
        if (srcEl) {
          srcPanel.lockedPosition = {
            col: parseInt(panel.style.gridColumnStart) || parseInt(panel.style.gridColumn) || 1,
            row: parseInt(panel.style.gridRowStart) || parseInt(panel.style.gridRow) || 1,
            span: panel.style.gridColumnEnd ? parseInt(panel.style.gridColumnEnd) - parseInt(panel.style.gridColumnStart) : 1
          };
        }
        dstPanel.locked = true;
        const dstEl = document.getElementById('panel-' + dstId);
        if (dstEl) {
          dstPanel.lockedPosition = {
            col: parseInt(dstEl.style.gridColumnStart) || 1,
            row: parseInt(dstEl.style.gridRowStart) || 1,
            span: 1
          };
        }
        const tmp = srcPanel.manualOrder;
        srcPanel.manualOrder = dstPanel.manualOrder;
        dstPanel.manualOrder = tmp;
        trackEvent(srcId, 'click');
        saveState();
        renderAll();
        toast('Swapped ' + srcId + ' ↔ ' + dstId);
      }
    });
  });
}
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2200);
}
function resetLayout() {
  if (!confirm('Clear all tracking data and reset layout?')) return;
  localStorage.removeItem(STORAGE_KEY);
  state = defaultState();
  viewEntries.clear();
  renderAll();
  toast('Layout reset');
}
function exportData() {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'adaptive-layout-data.json';
  a.click();
  URL.revokeObjectURL(url);
}
state.sessionCount++;
saveState();
renderAll();
setInterval(() => {
  document.getElementById('layoutAge').textContent = formatAge(state.layoutAge);
}, 30000);
</script>
</body>
</html>