<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-2: #22253a;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8890a4;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff6b7a;
  --success: #4ade80;
  --warn: #f59e0b;
  --panel-radius: 10px;
  --transition: 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 12px;
}
.dashboard-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 4px 12px;
  flex-wrap: wrap;
}
.dashboard-header h1 {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: -0.3px;
  color: var(--text);
}
.badge {
  font-size: 0.7rem;
  padding: 3px 10px;
  border-radius: 20px;
  background: var(--surface-2);
  color: var(--accent);
  border: 1px solid var(--border);
  white-space: nowrap;
}
.btn-reset {
  margin-left: auto;
  padding: 5px 14px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-dim);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.75rem;
  transition: var(--transition);
}
.btn-reset:hover { background: var(--surface-2); color: var(--text); }
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 180px;
  gap: 10px;
  transition: var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--panel-radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: grid-column var(--transition), grid-row var(--transition), opacity 0.3s, transform 0.3s;
  min-height: 180px;
}
.panel:hover { border-color: #4a5080; }
.panel.locked { border-left: 3px solid var(--accent); }
.panel.compacted {
  grid-column: span 1;
  grid-row: span 1;
  opacity: 0.72;
  transform: scale(0.96);
  min-height: 100px;
}
.panel.compacted .panel-body { display: none; }
.panel.compacted .panel-preview { display: flex; }
.panel.panel-lg { grid-column: span 2; grid-row: span 2; }
.panel.panel-md-h { grid-column: span 2; grid-row: span 1; }
.panel.panel-md-v { grid-column: span 1; grid-row: span 2; }
.panel.panel-sm { grid-column: span 1; grid-row: span 1; }
.panel-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.1px;
  cursor: grab;
  user-select: none;
  flex-shrink: 0;
}
.panel-header:active { cursor: grabbing; }
.panel-title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-rank {
  font-size: 0.6rem;
  padding: 1px 7px;
  border-radius: 8px;
  background: var(--surface);
  color: var(--text-dim);
}
.panel-header button {
  width: 24px; height: 24px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  flex-shrink: 0;
}
.panel-header button:hover { background: var(--border); color: var(--text); }
.btn-lock.locked { color: var(--accent); }
.panel-body {
  flex: 1;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.panel-preview { display: none; padding: 6px 10px; align-items: center; gap: 8px; font-size: 0.7rem; color: var(--text-dim); }
.panel-preview .mini-spark { width: 60px; height: 28px; }
.panel-preview .mini-val { font-weight: 700; font-size: 0.85rem; color: var(--text); }
.resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 16px;
  height: 16px;
  cursor: nwse-resize;
  opacity: 0;
  transition: opacity 0.2s;
  background: linear-gradient(135deg, transparent 50%, var(--border) 50%);
  border-radius: 0 0 var(--panel-radius) 0;
}
.panel:hover .resize-handle { opacity: 1; }
.compact-zone {
  margin-top: 12px;
  padding: 8px 12px;
  border: 1px dashed var(--border);
  border-radius: var(--panel-radius);
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  min-height: 48px;
  align-items: center;
}
.compact-zone-label {
  font-size: 0.7rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-right: 8px;
}
.compact-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.7rem;
  cursor: pointer;
  transition: var(--transition);
}
.compact-card:hover { border-color: var(--accent); background: var(--surface-2); }
.compact-card .mini-spark { width: 44px; height: 20px; }
.metric-value {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -1px;
  line-height: 1;
}
.metric-label { font-size: 0.7rem; color: var(--text-dim); margin-top: 2px; }
.metric-delta { font-size: 0.72rem; margin-top: 4px; display: flex; align-items: center; gap: 4px; }
.delta-up { color: var(--success); }
.delta-down { color: var(--danger); }
.bar-chart {
  display: flex;
  gap: 3px;
  align-items: flex-end;
  height: 80px;
  width: 100%;
}
.bar {
  flex: 1;
  background: var(--accent);
  border-radius: 3px 3px 0 0;
  transition: height 0.6s;
  opacity: 0.6;
}
.bar:last-child { opacity: 1; }
.heat-cell {
  width: 18px; height: 18px;
  border-radius: 3px;
  transition: background 0.4s;
}
.tooltip {
  position: fixed;
  pointer-events: none;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 0.7rem;
  color: var(--text);
  z-index: 9999;
  opacity: 0;
  transition: opacity 0.15s;
  white-space: nowrap;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
.recording-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--success);
  animation: pulse 2s infinite;
  display: inline-block;
  margin-right: 4px;
}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Adaptive Metric Dashboard</h1>
  <span class="badge"><span class="recording-dot"></span>tracking</span>
  <span class="badge" id="adapt-count">adapts: 0</span>
  <button class="btn-reset" onclick="resetAll()">reset layout</button>
</div>
<div class="dashboard-grid" id="grid"></div>
<div class="compact-zone" id="compactZone">
  <span class="compact-zone-label">compacted</span>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
(function() {
  const PANELS = [
    { id:'cpu', title:'CPU Usage', unit:'%', icon:'⚙', type:'gauge', seed:42 },
    { id:'mem', title:'Memory', unit:'GB', icon:'🧠', type:'gauge', seed:77 },
    { id:'req', title:'Requests/s', unit:'rps', icon:'📡', type:'spark', seed:13 },
    { id:'err', title:'Error Rate', unit:'%', icon:'🚨', type:'gauge-inv', seed:91 },
    { id:'lat', title:'P99 Latency', unit:'ms', icon:'⏱', type:'gauge', seed:55 },
    { id:'users', title:'Active Users', unit:'', icon:'👥', type:'spark', seed:28 },
    { id:'throughput', title:'Throughput', unit:'Mbps', icon:'📶', type:'spark', seed:64 },
    { id:'storage', title:'Storage I/O', unit:'IOPS', icon:'💾', type:'gauge', seed:39 }
  ];
  let rankings = loadState('rankings') || {};
  let locks = loadState('locks') || {};
  let compacted = loadState('compacted') || {};
  let interactions = loadState('interactions') || {};
  let durations = loadState('durations') || {};
  let adaptationCount = loadState('adaptCount') || 0;
  function loadState(key) {
    try { const v = localStorage.getItem('ad-' + key); return v ? JSON.parse(v) : null; }
    catch(e) { return null; }
  }
  function saveState(key, val) {
    try { localStorage.setItem('ad-' + key, JSON.stringify(val)); }
    catch(e) {}
  }
  function persistAll() {
    saveState('rankings', rankings);
    saveState('locks', locks);
    saveState('compacted', compacted);
    saveState('interactions', interactions);
    saveState('durations', durations);
    saveState('adaptCount', adaptationCount);
  }
  PANELS.forEach(p => {
    if (!(p.id in rankings)) rankings[p.id] = 0.5;
    if (!(p.id in locks)) locks[p.id] = false;
    if (!(p.id in compacted)) compacted[p.id] = false;
    if (!(p.id in interactions)) interactions[p.id] = { freq:0, lastClick:0 };
    if (!(p.id in durations)) durations[p.id] = { total:0, lastView:0 };
  });
  function seededRandom(seed) {
    let s = seed;
    return function() {
      s = (s * 16807 + 0) % 2147483647;
      return (s - 1) / 2147483646;
    };
  }
  function genValue(panelId, seed) {
    const rng = seededRandom(seed + Math.floor(Date.now() / 30000));
    const base = { cpu:[20,60], mem:[4,28], req:[300,2200], err:[0.1,3.5],
      lat:[12,180], users:[80,950], throughput:[40,380], storage:[600,4200] }[panelId] || [0,100];
    return Math.round((base[0] + rng() * (base[1] - base[0])) * 10) / 10;
  }
  function genSparkline(panelId, seed, points) {
    const rng = seededRandom(seed + Math.floor(Date.now() / 60000));
    const base = { cpu:[20,60], mem:[4,28], req:[300,2200], err:[0.1,3.5],
      lat:[12,180], users:[80,950], throughput:[40,380], storage:[600,4200] }[panelId] || [0,100];
    const vals = [];
    for (let i = 0; i < points; i++) {
      vals.push(Math.round((base[0] + rng() * (base[1] - base[0])) * 10) / 10);
    }
    return vals;
  }
  function computeRank(panelId) {
    const i = interactions[panelId];
    const d = durations[panelId];
    const now = Date.now();
    const recencyHours = Math.max(0.01, (now - Math.max(i.lastClick, d.lastView)) / 3600000);
    const recencyDecay = Math.exp(-recencyHours / 2);
    const freq = Math.log2(i.freq + 1);
    const dur = Math.log2((d.total / 1000) + 1);
    return (freq * 0.35 + dur * 0.35 + recencyDecay * 0.30);
  }
  function recomputeAllRanks() {
    PANELS.forEach(p => { rankings[p.id] = computeRank(p.id); });
    persistAll();
  }
  function applyLayout() {
    const unlocked = PANELS.filter(p => !locks[p.id] && !compacted[p.id]);
    const lockedPanels = PANELS.filter(p => locks[p.id] && !compacted[p.id]);
    const compactedPanels = PANELS.filter(p => compacted[p.id]);
    unlocked.sort((a, b) => rankings[b.id] - rankings[a.id]);
    const allGridPanels = [...lockedPanels, ...unlocked];
    const sizeClasses = [];
    allGridPanels.forEach((p, idx) => {
      const total = allGridPanels.length;
      const rank = total - idx;
      if (rank <= 2) sizeClasses.push({ id:p.id, cls:'panel-lg' });
      else if (rank <= 4) sizeClasses.push({ id:p.id, cls:'panel-md-h' });
      else if (rank <= 6) sizeClasses.push({ id:p.id, cls:'panel-md-v' });
      else sizeClasses.push({ id:p.id, cls:'panel-sm' });
    });
    const clsMap = {};
    sizeClasses.forEach(s => { clsMap[s.id] = s.cls; });
    const grid = document.getElementById('grid');
    const existing = {};
    Array.from(grid.children).forEach(el => {
      existing[el.dataset.panelId] = el;
    });
    const orderedIds = allGridPanels.map(p => p.id);
    orderedIds.forEach(id => {
      const el = existing[id];
      if (!el) return;
      el.className = 'panel ' + (clsMap[id] || 'panel-sm');
      if (locks[id]) el.classList.add('locked');
      el.querySelector('.btn-lock').textContent = locks[id] ? '🔒' : '🔓';
      el.querySelector('.btn-lock').classList.toggle('locked', locks[id]);
      const rankIdx = orderedIds.indexOf(id);
      if (rankIdx >= 0) {
        el.querySelector('.panel-rank').textContent = '#' + (rankIdx + 1);
      }
      el.style.order = orderedIds.indexOf(id);
      grid.appendChild(el);
    });
    const compactZone = document.getElementById('compactZone');
    compactZone.querySelectorAll('.compact-card').forEach(c => c.remove());
    const label = compactZone.querySelector('.compact-zone-label');
    compactedPanels.forEach(p => {
      const card = document.createElement('div');
      card.className = 'compact-card';
      card.dataset.panelId = p.id;
      card.title = 'Click to expand ' + p.title;
      const sparkVals = genSparkline(p.id, p.seed, 8);
      const svg = buildMiniSpark(sparkVals, 44, 20, p.id);
      const val = genValue(p.id, p.seed);
      card.innerHTML = '<span style="font-size:0.8rem">' + p.icon + '</span>' +
        '<span>' + p.title + '</span>' +
        '<span class="mini-val">' + val + (p.unit ? ' ' + p.unit : '') + '</span>';
      card.querySelector('.mini-val').insertAdjacentHTML('afterbegin', svg);
      card.addEventListener('click', () => toggleCompact(p.id));
      compactZone.appendChild(card);
    });
    if (compactedPanels.length === 0 && label) label.style.display = 'none';
    else if (label) label.style.display = '';
    persistAll();
  }
  function toggleLock(panelId) {
    locks[panelId] = !locks[panelId];
    persistAll();
    applyLayout();
  }
  function toggleCompact(panelId) {
    compacted[panelId] = !compacted[panelId];
    if (!compacted[panelId]) {
      interactions[panelId].freq += 2;
      interactions[panelId].lastClick = Date.now();
    }
    recomputeAllRanks();
    applyLayout();
  }
  function buildMiniSpark(vals, w, h, id) {
    if (!vals.length) return '';
    const min = Math.min(...vals);
    const max = Math.max(...vals);
    const range = max - min || 1;
    const pts = vals.map((v, i) => {
      const x = (i / (vals.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    const color = { err:'#ff6b7a' }[id] || '#6c8cff';
    return '<svg class="mini-spark" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '">' +
      '<polyline points="' + pts + '" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>' +
      '</svg>';
  }
  function buildPanelHTML(p) {
    const val = genValue(p.id, p.seed);
    const sparkVals = genSparkline(p.id, p.seed, 20);
    const prevVals = genSparkline(p.id, p.seed + 999, 20);
    const delta = val - prevVals[prevVals.length - 1];
    const deltaPct = prevVals[prevVals.length - 1] ? Math.round((delta / prevVals[prevVals.length - 1]) * 1000) / 10 : 0;
    const deltaCls = delta > 0 ? (p.type === 'gauge-inv' ? 'delta-down' : 'delta-up') :
      delta < 0 ? (p.type === 'gauge-inv' ? 'delta-up' : 'delta-down') : '';
    let bodyHTML = '';
    if (p.type === 'gauge' || p.type === 'gauge-inv') {
      const pct = p.type === 'gauge-inv' ? Math.min(100, Math.max(0, val / 3.5 * 100)) :
        Math.min(100, Math.max(0, val / (p.id === 'cpu' ? 100 : p.id === 'mem' ? 32 : p.id === 'lat' ? 200 : p.id === 'storage' ? 5000 : 100) * 100));
      const gaugeColor = p.type === 'gauge-inv' ?
        (val > 2 ? 'var(--danger)' : val > 1 ? 'var(--warn)' : 'var(--success)') :
        (pct > 80 ? 'var(--warn)' : 'var(--accent)');
      bodyHTML = '<div style="display:flex;align-items:center;gap:16px;width:100%">' +
        '<div style="flex:1"><div class="metric-value">' + val + '</div>' +
        '<div class="metric-label">' + p.unit + '</div>' +
        '<div class="metric-delta ' + deltaCls + '">' + (delta >= 0 ? '↑' : '↓') + ' ' + Math.abs(deltaPct) + '%</div></div>' +
        '<svg width="70" height="70" viewBox="0 0 70 70"><circle cx="35" cy="35" r="30" fill="none" stroke="var(--border)" stroke-width="5"/>' +
        '<circle cx="35" cy="35" r="30" fill="none" stroke="' + gaugeColor + '" stroke-width="5" stroke-dasharray="' + (pct * 1.884) + ' 188.4" stroke-linecap="round" transform="rotate(-90 35 35)"/></svg></div>';
    } else {
      const bars = sparkVals.slice(-12);
      const maxV = Math.max(...bars);
      bodyHTML = '<div style="width:100%"><div class="metric-value" style="font-size:1.4rem">' + val + ' <span style="font-size:0.7rem;color:var(--text-dim)">' + p.unit + '</span></div>' +
        '<div class="metric-delta ' + deltaCls + '">' + (delta >= 0 ? '↑' : '↓') + ' ' + Math.abs(deltaPct) + '%</div>' +
        '<div class="bar-chart" style="margin-top:8px;height:50px">' +
        bars.map(v => '<div class="bar" style="height:' + ((v / maxV) * 100) + '%"></div>').join('') + '</div></div>';
    }
    const previewSpark = buildMiniSpark(sparkVals.slice(-12), 60, 28, p.id);
    return '<div class="panel ' + (compacted[p.id] ? '' : 'panel-sm') + (locks[p.id] ? ' locked' : '') +
      (compacted[p.id] ? ' compacted' : '') + '" data-panel-id="' + p.id + '">' +
      '<div class="panel-header"><span style="font-size:0.85rem">' + p.icon + '</span>' +
      '<span class="panel-title">' + p.title + '</span>' +
      '<span class="panel-rank">#' + (PANELS.indexOf(p) + 1) + '</span>' +
      '<button class="btn-compact" onclick="toggleCompact(\'' + p.id + '\')" title="compact/expand">' + (compacted[p.id] ? '⊞' : '⊟') + '</button>' +
      '<button class="btn-lock' + (locks[p.id] ? ' locked' : '') + '" onclick="toggleLock(\'' + p.id + '\')" title="lock position">' + (locks[p.id] ? '🔒' : '🔓') + '</button></div>' +
      '<div class="panel-body">' + bodyHTML + '</div>' +
      '<div class="panel-preview">' + previewSpark + '<span class="mini-val">' + val + (p.unit ? ' ' + p.unit : '') + '</span></div>' +
      '<div class="resize-handle"></div></div>';
  }
  function renderAll() {
    const grid = document.getElementById('grid');
    grid.innerHTML = PANELS.map(p => buildPanelHTML(p)).join('');
    applyLayout();
    attachObservers();
  }
  function attachObservers() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.dataset.panelId;
        if (!id) return;
        if (entry.isIntersecting) {
          entry.target._viewStart = Date.now();
        } else if (entry.target._viewStart) {
          const elapsed = Date.now() - entry.target._viewStart;
          durations[id].total += elapsed;
          durations[id].lastView = Date.now();
          entry.target._viewStart = null;
          persistAll();
        }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.panel').forEach(el => observer.observe(el));
    document.querySelectorAll('.panel').forEach(el => {
      el.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        const id = el.dataset.panelId;
        interactions[id].freq++;
        interactions[id].lastClick = Date.now();
        persistAll();
      });
    });
    document.querySelectorAll('.resize-handle').forEach(handle => {
      let startX, startY, startW, startH, panel;
      handle.addEventListener('mousedown', (e) => {
        e.preventDefault();
        panel = handle.closest('.panel');
        startX = e.clientX;
        startY = e.clientY;
        const rect = panel.getBoundingClientRect();
        startW = rect.width;
        startH = rect.height;
        document.addEventListener('mousemove', onDrag);
        document.addEventListener('mouseup', onDrop);
      });
      function onDrag(e) {
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        if (Math.abs(dx) > 20 || Math.abs(dy) > 20) {
          const id = panel.dataset.panelId;
          interactions[id].freq += 1;
          interactions[id].lastClick = Date.now();
          locks[id] = true;
          persistAll();
          applyLayout();
          document.removeEventListener('mousemove', onDrag);
          document.removeEventListener('mouseup', onDrop);
        }
      }
      function onDrop() {
        document.removeEventListener('mousemove', onDrag);
        document.removeEventListener('mouseup', onDrop);
      }
    });
  }
  function adaptCycle() {
    const now = Date.now();
    document.querySelectorAll('.panel').forEach(el => {
      if (el._viewStart) {
        const elapsed = now - el._viewStart;
        const id = el.dataset.panelId;
        durations[id].total += elapsed;
        durations[id].lastView = now;
        el._viewStart = now;
      }
    });
    recomputeAllRanks();
    adaptationCount++;
    document.getElementById('adapt-count').textContent = 'adapts: ' + adaptationCount;
    applyLayout();
    persistAll();
  }
  window.toggleLock = toggleLock;
  window.toggleCompact = toggleCompact;
  window.resetAll = function() {
    PANELS.forEach(p => {
      rankings[p.id] = 0.5;
      locks[p.id] = false;
      compacted[p.id] = false;
      interactions[p.id] = { freq:0, lastClick:0 };
      durations[p.id] = { total:0, lastView:0 };
    });
    adaptationCount = 0;
    document.getElementById('adapt-count').textContent = 'adapts: 0';
    persistAll();
    renderAll();
  };
  renderAll();
  setInterval(() => {
    document.querySelectorAll('.panel').forEach(el => {
      const id = el.dataset.panelId;
      if (!id) return;
      const p = PANELS.find(x => x.id === id);
      if (!p) return;
      const val = genValue(id, p.seed);
      const valEl = el.querySelector('.metric-value');
      if (valEl) valEl.textContent = val;
      const miniVal = el.querySelector('.mini-val');
      if (miniVal) {
        const unit = p.unit ? ' ' + p.unit : '';
        const sparkVals = genSparkline(id, p.seed, 12);
        miniVal.innerHTML = buildMiniSpark(sparkVals, 60, 28, id) + val + unit;
      }
    });
    document.querySelectorAll('.compact-card').forEach(card => {
      const id = card.dataset.panelId;
      const p = PANELS.find(x => x.id === id);
      if (!p) return;
      const val = genValue(id, p.seed);
      const miniVal = card.querySelector('.mini-val');
      if (miniVal) {
        const unit = p.unit ? ' ' + p.unit : '';
        const sparkVals = genSparkline(id, p.seed, 8);
        miniVal.innerHTML = buildMiniSpark(sparkVals, 44, 20, id) + val + unit;
      }
    });
  }, 5000);
  setInterval(adaptCycle, 15000);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      document.querySelectorAll('.panel').forEach(el => {
        if (el._viewStart) {
          const id = el.dataset.panelId;
          const elapsed = Date.now() - el._viewStart;
          durations[id].total += elapsed;
          durations[id].lastView = Date.now();
          el._viewStart = null;
        }
      });
      persistAll();
    }
  });
  const tooltip = document.getElementById('tooltip');
  document.addEventListener('mousemove', (e) => {
    const panel = e.target.closest('.panel-header');
    if (panel) {
      const id = panel.closest('.panel').dataset.panelId;
      const i = interactions[id];
      const d = durations[id];
      tooltip.textContent = 'clicks: ' + i.freq + ' | viewed: ' + Math.round(d.total / 1000) + 's | rank: ' + rankings[id].toFixed(3);
      tooltip.style.left = (e.clientX + 12) + 'px';
      tooltip.style.top = (e.clientY - 28) + 'px';
      tooltip.style.opacity = '1';
    } else {
      tooltip.style.opacity = '0';
    }
  });
})();
</script>
</body>
</html>