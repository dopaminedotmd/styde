<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface2: #242834;
  --border: #2a2e3a; --text: #e1e4ed; --text2: #8b90a0;
  --accent: #6c8cff; --accent2: #4ade80; --warn: #f59e0b;
  --danger: #ef4444; --radius: 8px; --gap: 12px;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.25rem;font-weight:600}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:6px 14px;border-radius:var(--radius);border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:0.8rem;transition:background .15s}
.btn:hover{background:var(--surface2)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.danger{background:var(--danger);border-color:var(--danger);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);transition:all .3s ease}
.panel{background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .3s ease;position:relative;display:flex;flex-direction:column}
.panel.compact{grid-row:span 1;max-height:120px}
.panel.compact .body{display:none}
.panel.expanded{grid-column:span 2;grid-row:span 2}
.panel.dominant{grid-column:span 2;grid-row:span 2;border-color:var(--accent)}
.panel.pinned{border-color:var(--accent2)}
.panel-head{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:var(--surface2);cursor:grab;user-select:none;gap:8px}
.panel-head:active{cursor:grabbing}
.panel-head h2{font-size:0.85rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-head .badge{font-size:0.6rem;padding:2px 6px;border-radius:10px;background:var(--accent);color:#fff;white-space:nowrap}
.panel-head .badge.low{background:var(--text2)}
.panel-head .badge.mid{background:var(--warn)}
.panel-head .badge.high{background:var(--accent2)}
.head-actions{display:flex;gap:4px;align-items:center}
.icon-btn{width:26px;height:26px;display:flex;align-items:center;justify-content:center;border:none;background:transparent;color:var(--text2);cursor:pointer;border-radius:4px;font-size:0.75rem;transition:all .15s}
.icon-btn:hover{background:var(--border);color:var(--text)}
.icon-btn.pinned{color:var(--accent2)}
.body{padding:14px;flex:1;display:flex;flex-direction:column;gap:8px}
.metric-big{font-size:2rem;font-weight:700;line-height:1}
.metric-label{font-size:0.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:.05em}
.sparkline-wrap{width:100%;height:60px}
.sparkline-wrap svg{width:100%;height:100%}
.metric-row{display:flex;justify-content:space-between;align-items:center}
.metric-change{font-size:0.75rem;font-weight:600}
.metric-change.up{color:var(--accent2)}
.metric-change.down{color:var(--danger)}
.empty-state{text-align:center;padding:40px 20px;color:var(--text2);font-size:0.85rem}
.collapsed-section{margin-top:var(--gap)}
.collapsed-toggle{width:100%;padding:8px;background:var(--surface);border:1px dashed var(--border);border-radius:var(--radius);color:var(--text2);cursor:pointer;font-size:0.75rem;text-align:center;transition:all .15s}
.collapsed-toggle:hover{border-color:var(--accent);color:var(--accent)}
.collapsed-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px;margin-top:8px}
.mini-panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px;cursor:pointer;transition:all .15s}
.mini-panel:hover{border-color:var(--accent)}
.mini-panel h3{font-size:0.65rem;color:var(--text2);margin-bottom:4px}
.mini-panel .mini-val{font-size:1rem;font-weight:600}
.tooltip{position:fixed;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-size:0.7rem;pointer-events:none;z-index:100;opacity:0;transition:opacity .15s}
.tooltip.show{opacity:1}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" onclick="App.reset()">Reset layout</button>
    <button class="btn primary" onclick="App.forceReRank()">Re-rank now</button>
  </div>
</header>
<div id="grid" class="grid"></div>
<div id="collapsed-section" class="collapsed-section" style="display:none">
  <button class="collapsed-toggle" onclick="App.toggleCollapsed()">
    <span id="collapsed-count">0</span> collapsed panels — click to expand
  </button>
  <div id="collapsed-grid" class="collapsed-grid" style="display:none"></div>
</div>
<script>
/* ============================================================
   DataStore — localStorage persistence, attention metrics
   ============================================================ */
const DataStore = (() => {
  const KEY = 'adash_data';
  let _data = null;
  function defaults() {
    return {
      panels: [
        {id:'revenue',  title:'Revenue',       value:'$48,294', change:'+12.3%', dir:'up',   spark:[12,18,22,28,25,32,38,35,42,48,44,52,49,55,60,58,65,70,68,74]},
        {id:'users',    title:'Active Users',   value:'2,847',   change:'+8.1%',  dir:'up',   spark:[120,140,155,180,210,230,250,240,260,280,300,310,330,340,360,350,370,390,400,420]},
        {id:'churn',    title:'Churn Rate',      value:'1.8%',    change:'-0.3%',  dir:'down', spark:[3.2,3.0,2.8,2.6,2.5,2.4,2.3,2.2,2.1,2.0,1.9,1.9,1.8,1.8,1.7,1.8,1.7,1.8,1.7,1.8]},
        {id:'uptime',   title:'Uptime',          value:'99.97%',  change:'+0.02%', dir:'up',   spark:[99.9,99.9,99.8,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9,99.9]},
        {id:'latency',  title:'P95 Latency',     value:'142ms',   change:'-5ms',   dir:'down', spark:[180,175,168,160,155,150,148,145,142,140,138,135,133,130,128,126,124,122,120,118]},
        {id:'errors',   title:'Error Rate',      value:'0.12%',   change:'-0.04%', dir:'down', spark:[0.5,0.45,0.4,0.38,0.35,0.3,0.28,0.25,0.22,0.2,0.18,0.16,0.15,0.14,0.13,0.12,0.12,0.11,0.11,0.12]},
        {id:'storage',  title:'Storage Used',    value:'67.4 GB', change:'+2.1%',  dir:'up',   spark:[40,42,44,46,48,50,52,54,56,58,60,61,63,64,65,66,67,67,67,67]},
        {id:'reqs',     title:'Requests/min',    value:'3,421',   change:'+15.7%', dir:'up',   spark:[800,900,1100,1200,1400,1600,1800,2000,2200,2400,2600,2800,2900,3000,3100,3200,3300,3400,3400,3421]}
      ],
      attention: {},
      pinned: {},
      collapsed: [],
      order: null
    };
  }
  function load() {
    if (_data) return _data;
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        const d = defaults();
        _data = Object.assign({}, d, parsed, {
          panels: d.panels.map(p => {
            const saved = (parsed.panels || []).find(sp => sp.id === p.id);
            return saved ? Object.assign({}, p, saved, {spark: p.spark, title: p.title}) : p;
          })
        });
        return _data;
      }
    } catch(e) { /* corrupt, use defaults */ }
    _data = defaults();
    return _data;
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(_data)); } catch(e) {}
  }
  function recordAttention(panelId, durationMs, interacted) {
    const d = load();
    const now = Date.now();
    if (!d.attention[panelId]) {
      d.attention[panelId] = {totalDuration: 0, interactions: 0, views: 0, lastSeen: now, firstSeen: now};
    }
    const a = d.attention[panelId];
    a.totalDuration += durationMs;
    if (interacted) a.interactions += 1;
    a.views += 1;
    a.lastSeen = now;
    save();
  }
  function togglePin(panelId) {
    const d = load();
    d.pinned[panelId] = !d.pinned[panelId];
    save();
    return d.pinned[panelId];
  }
  function collapsePanel(panelId) {
    const d = load();
    if (!d.collapsed.includes(panelId)) d.collapsed.push(panelId);
    d.pinned[panelId] = false;
    save();
  }
  function expandPanel(panelId) {
    const d = load();
    d.collapsed = d.collapsed.filter(id => id !== panelId);
    save();
  }
  function setOrder(order) {
    const d = load();
    d.order = order;
    save();
  }
  function reset() {
    localStorage.removeItem(KEY);
    _data = defaults();
    save();
  }
  return {load, save, recordAttention, togglePin, collapsePanel, expandPanel, setOrder, reset};
})();
/* ============================================================
   Ranker — composite scoring (frequency × duration × recency)
   ============================================================ */
const Ranker = (() => {
  function score(attention, panelId) {
    const a = attention[panelId];
    if (!a) return 0;
    const now = Date.now();
    const hoursSinceLast = Math.max(1, (now - a.lastSeen) / 3600000);
    const recency = 1 / Math.log(hoursSinceLast + 1);
    const freqScore = Math.log(a.views + 1);
    const durScore = Math.log(a.totalDuration / 1000 + 1);
    const intScore = Math.log(a.interactions + 1);
    return (freqScore * 0.35 + durScore * 0.35 + intScore * 0.15 + recency * 0.15) * 100;
  }
  function rankAll(data) {
    const active = data.panels.filter(p => !data.collapsed.includes(p.id));
    const ranked = active.map(p => ({
      id: p.id,
      score: score(data.attention, p.id),
      pinned: !!data.pinned[p.id]
    }));
    ranked.sort((a, b) => {
      if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
      return b.score - a.score;
    });
    if (data.order) {
      const orderMap = {};
      data.order.forEach((id, i) => orderMap[id] = i);
      ranked.sort((a, b) => {
        if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
        const oa = orderMap[a.id] !== undefined ? orderMap[a.id] : 999;
        const ob = orderMap[b.id] !== undefined ? orderMap[b.id] : 999;
        if (oa !== ob) return oa - ob;
        return b.score - a.score;
      });
    }
    return ranked;
  }
  function tierClass(rank, total) {
    if (total <= 3) return 'high';
    const pct = rank / total;
    if (pct < 0.25) return 'high';
    if (pct < 0.6) return 'mid';
    return 'low';
  }
  return {score, rankAll, tierClass};
})();
/* ============================================================
   Drawer — SVG sparklines with edge case guards
   ============================================================ */
const Drawer = (() => {
  function sparklinePath(data, width, height) {
    if (!data || data.length === 0) return {d: '', min: 0, max: 0};
    const nums = data.map(v => {
      const n = Number(v);
      return (isNaN(n) || !isFinite(n)) ? null : n;
    }).filter(v => v !== null);
    if (nums.length === 0) return {d: '', min: 0, max: 0};
    if (nums.length === 1) {
      const y = height / 2;
      return {d: `M0,${y} L${width},${y}`, min: nums[0], max: nums[0]};
    }
    let min = nums[0], max = nums[0];
    for (let i = 1; i < nums.length; i++) {
      if (nums[i] < min) min = nums[i];
      if (nums[i] > max) max = nums[i];
    }
    const range = max - min;
    const effectiveRange = range === 0 ? 1 : range;
    const pad = 4;
    const usableH = height - pad * 2;
    const stepX = width / (nums.length - 1);
    const points = nums.map((v, i) => {
      const x = i * stepX;
      const y = pad + usableH - ((v - min) / effectiveRange) * usableH;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    });
    return {d: points.join(' '), min, max};
  }
  function renderSparkline(container, data, color) {
    const rect = container.getBoundingClientRect();
    const w = rect.width || 280;
    const h = rect.height || 60;
    const {d, min, max} = sparklinePath(data, w, h);
    if (!d) {
      container.innerHTML = '<div style="color:var(--text2);font-size:0.6rem;text-align:center;padding-top:20px">No data</div>';
      return;
    }
    const svg = `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
      <defs><linearGradient id="sg-${color.replace('#','')}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="${color}" stop-opacity="0.3"/>
        <stop offset="100%" stop-color="${color}" stop-opacity="0.02"/>
      </linearGradient></defs>
      <path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
      <path d="${d} L${w},${h} L0,${h} Z" fill="url(#sg-${color.replace('#','')})"/>
    </svg>`;
    container.innerHTML = svg;
  }
  return {sparklinePath, renderSparkline};
})();
/* ============================================================
   Renderer — DOM updates with caching and rAF batching
   ============================================================ */
const Renderer = (() => {
  const $els = {};
  let rafId = null;
  let pendingUpdate = null;
  function cache() {
    $els.grid = document.getElementById('grid');
    $els.collapsedSection = document.getElementById('collapsed-section');
    $els.collapsedGrid = document.getElementById('collapsed-grid');
    $els.collapsedCount = document.getElementById('collapsed-count');
    $els.collapsedToggle = document.querySelector('.collapsed-toggle');
  }
  function batchRender(fn) {
    pendingUpdate = fn;
    if (rafId === null) {
      rafId = requestAnimationFrame(() => {
        rafId = null;
        if (pendingUpdate) pendingUpdate();
        pendingUpdate = null;
      });
    }
  }
  function panelHTML(p, rankInfo, data) {
    const pinned = !!data.pinned[p.id];
    const tier = rankInfo ? Ranker.tierClass(rankInfo.rank, rankInfo.total) : 'mid';
    const scoreDisplay = rankInfo ? Math.round(rankInfo.score) : 0;
    let cls = 'panel';
    if (pinned) cls += ' pinned';
    if (rankInfo) {
      if (rankInfo.rank === 0 && rankInfo.total > 3) cls += ' dominant';
      else if (rankInfo.rank < Math.ceil(rankInfo.total * 0.25)) cls += ' expanded';
      else if (rankInfo.rank > rankInfo.total * 0.7) cls += ' compact';
    }
    return `<div class="${cls}" data-id="${p.id}" id="panel-${p.id}">
      <div class="panel-head">
        <h2>${p.title}</h2>
        <div class="head-actions">
          <span class="badge ${tier}">${scoreDisplay}</span>
          <button class="icon-btn ${pinned ? 'pinned' : ''}" data-action="pin" data-pid="${p.id}" title="Toggle pin">📌</button>
          <button class="icon-btn" data-action="collapse" data-pid="${p.id}" title="Collapse">−</button>
        </div>
      </div>
      <div class="body">
        <div class="metric-big">${p.value}</div>
        <div class="metric-row">
          <span class="metric-label">${p.title}</span>
          <span class="metric-change ${p.dir}">${p.change}</span>
        </div>
        <div class="sparkline-wrap" id="spark-${p.id}"></div>
      </div>
    </div>`;
  }
  function miniPanelHTML(p) {
    return `<div class="mini-panel" data-action="expand" data-pid="${p.id}">
      <h3>${p.title}</h3>
      <div class="mini-val">${p.value}</div>
      <span class="metric-change ${p.dir}" style="font-size:0.65rem">${p.change}</span>
    </div>`;
  }
  function renderAll(data, ranked) {
    if (!$els.grid) cache();
    const rankedMap = {};
    ranked.forEach((r, i) => rankedMap[r.id] = {rank: i, score: r.score, total: ranked.length});
    const activeIds = ranked.map(r => r.id);
    const activePanels = activeIds.map(id => data.panels.find(p => p.id === id)).filter(Boolean);
    const orderToSet = activeIds.slice();
    if (data.order) {
      const orderSet = new Set(data.order);
      activeIds.forEach(id => { if (!orderSet.has(id)) orderSet.add(id); });
      DataStore.setOrder(Array.from(orderSet));
    } else {
      DataStore.setOrder(orderToSet);
    }
    $els.grid.innerHTML = activePanels.map(p => panelHTML(p, rankedMap[p.id], data)).join('');
    const collapsedPanels = data.panels.filter(p => data.collapsed.includes(p.id));
    if (collapsedPanels.length > 0) {
      $els.collapsedSection.style.display = 'block';
      $els.collapsedCount.textContent = collapsedPanels.length;
      $els.collapsedGrid.innerHTML = collapsedPanels.map(miniPanelHTML).join('');
    } else {
      $els.collapsedSection.style.display = 'none';
    }
    activePanels.forEach(p => {
      const container = document.getElementById('spark-' + p.id);
      if (container) {
        const color = p.dir === 'up' ? 'var(--accent2)' : p.dir === 'down' ? 'var(--danger)' : 'var(--accent)';
        Drawer.renderSparkline(container, p.spark, color);
      }
    });
  }
  function bindDelegation() {
    if (!$els.grid) cache();
    $els.grid.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      const action = btn.dataset.action;
      const pid = btn.dataset.pid;
      if (action === 'pin') App.togglePin(pid);
      if (action === 'collapse') App.collapsePanel(pid);
    });
    const cs = document.getElementById('collapsed-grid');
    if (cs) {
      cs.addEventListener('click', e => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        if (btn.dataset.action === 'expand') App.expandPanel(btn.dataset.pid);
      });
    }
  }
  return {cache, batchRender, renderAll, bindDelegation, getEls: () => $els};
})();
/* ============================================================
   Controller — thin orchestration layer
   ============================================================ */
const App = (() => {
  let _viewTimers = {};
  let _observer = null;
  let _lastRender = 0;
  function init() {
    Renderer.cache();
    Renderer.bindDelegation();
    setupIntersectionObserver();
    rerank();
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) flushTimers();
    });
  }
  function setupIntersectionObserver() {
    _observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.dataset.id;
        if (!id) return;
        if (entry.isIntersecting) {
          startTimer(id);
        } else {
          stopTimer(id);
        }
      });
    }, {threshold: 0.5});
    setTimeout(() => {
      document.querySelectorAll('.panel[data-id]').forEach(el => _observer.observe(el));
    }, 100);
  }
  function startTimer(id) {
    if (_viewTimers[id] && _viewTimers[id].start) return;
    _viewTimers[id] = {start: performance.now(), interacted: false};
    const panel = document.getElementById('panel-' + id);
    if (panel && !panel.dataset.listening) {
      panel.dataset.listening = '1';
      panel.addEventListener('click', () => {
        if (_viewTimers[id]) _viewTimers[id].interacted = true;
      }, {once: false});
      panel.addEventListener('mouseenter', () => {
        if (_viewTimers[id]) _viewTimers[id].interacted = true;
      });
    }
  }
  function stopTimer(id) {
    const t = _viewTimers[id];
    if (!t || !t.start) return;
    const duration = performance.now() - t.start;
    DataStore.recordAttention(id, duration, t.interacted);
    delete _viewTimers[id];
  }
  function flushTimers() {
    Object.keys(_viewTimers).forEach(id => stopTimer(id));
  }
  function rerank() {
    flushTimers();
    const data = DataStore.load();
    const ranked = Ranker.rankAll(data);
    Renderer.batchRender(() => {
      Renderer.renderAll(data, ranked);
      requestAnimationFrame(() => {
        document.querySelectorAll('.panel[data-id]').forEach(el => {
          if (_observer) _observer.observe(el);
        });
      });
    });
    _lastRender = Date.now();
  }
  function forceReRank() {
    rerank();
  }
  function togglePin(id) {
    const pinned = DataStore.togglePin(id);
    rerank();
  }
  function collapsePanel(id) {
    DataStore.collapsePanel(id);
    rerank();
  }
  function expandPanel(id) {
    DataStore.expandPanel(id);
    rerank();
  }
  function toggleCollapsed() {
    const cg = document.getElementById('collapsed-grid');
    if (cg) cg.style.display = cg.style.display === 'none' ? 'grid' : 'none';
  }
  function reset() {
    DataStore.reset();
    rerank();
  }
  return {init, rerank, forceReRank, togglePin, collapsePanel, expandPanel, toggleCollapsed, reset};
})();
document.addEventListener('DOMContentLoaded', () => App.init());
window.App = App;
</script>
</body>
</html>