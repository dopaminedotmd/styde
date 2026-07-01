<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #222533;
  --text: #e1e4ed;
  --text2: #8b8fa8;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}
h1 { font-size: 1.4rem; font-weight: 600; letter-spacing: -0.02em; }
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
.btn {
  padding: 7px 14px;
  border: 1px solid var(--surface2);
  background: var(--surface);
  color: var(--text);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: var(--transition);
}
.btn:hover { background: var(--surface2); }
.btn.active { border-color: var(--accent); color: var(--accent); }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  align-items: start;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--surface2);
  border-radius: var(--radius);
  overflow: hidden;
  transition: var(--transition);
  position: relative;
}
.panel.span2 { grid-column: span 2; }
.panel.compact { grid-column: span 1; font-size: 0.8rem; }
.panel.compact .panel-body { padding: 8px 12px; max-height: 120px; overflow: hidden; }
.panel.compact .panel-content { opacity: 0.6; transform: scale(0.95); }
.panel.collapsed { display: none; }
.panel.locked { border-color: var(--warn); }
.panel.locked::after {
  content: "🔒";
  position: absolute;
  top: 6px;
  right: 36px;
  font-size: 0.7rem;
  opacity: 0.7;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--surface2);
  cursor: grab;
  user-select: none;
}
.panel-header:active { cursor: grabbing; }
.panel-title { font-weight: 600; font-size: 0.9rem; }
.panel-actions { display: flex; gap: 4px; }
.panel-btn {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  transition: var(--transition);
}
.panel-btn:hover { color: var(--text); background: rgba(255,255,255,0.05); }
.panel-btn.lock-btn.locked { color: var(--warn); }
.panel-body { padding: 14px; }
.panel-content { transition: var(--transition); }
.metric-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; }
.metric-label { font-size: 0.75rem; color: var(--text2); margin-top: 2px; }
.chart-bar {
  height: 8px;
  background: var(--surface2);
  border-radius: 4px;
  margin-top: 6px;
  overflow: hidden;
}
.chart-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--accent);
  transition: width 0.5s ease;
}
.chart-fill.green { background: var(--accent2); }
.chart-fill.warn { background: var(--warn); }
.more-section {
  margin-top: 16px;
  padding: 10px 14px;
  background: var(--surface);
  border: 1px dashed var(--surface2);
  border-radius: var(--radius);
  cursor: pointer;
  text-align: center;
  color: var(--text2);
  font-size: 0.82rem;
  transition: var(--transition);
}
.more-section:hover { border-color: var(--accent); color: var(--text); }
.more-panels { display: none; margin-top: var(--gap); }
.more-panels.open { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--gap); }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface2);
  border: 1px solid var(--accent);
  color: var(--text);
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 0.82rem;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
  z-index: 100;
}
.toast.show { opacity: 1; transform: translateY(0); }
.score-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 0.65rem;
  color: var(--text2);
  opacity: 0;
  transition: opacity 0.3s;
}
.panel:hover .score-badge { opacity: 1; }
@media (max-width: 640px) {
  .grid { grid-template-columns: 1fr; }
  .panel.span2 { grid-column: span 1; }
}
</style>
</head>
<body>
<header>
<h1>Adaptive Dashboard</h1>
<div class="controls">
<button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
<button class="btn" id="btnExport" title="Export layout">Export</button>
<button class="btn" id="btnImport" title="Import layout">Import</button>
<input type="file" id="importFile" style="display:none" accept=".json">
<span style="font-size:0.7rem;color:var(--text2)" id="scoreDisplay"></span>
</div>
</header>
<div class="grid" id="grid"></div>
<div class="more-section" id="moreToggle">More panels ▸</div>
<div class="more-panels" id="morePanels"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
  'use strict';
  const CACHE_TTL = { scores: 30000, prefs: 300000 };
  const COMPACT_THRESHOLD = 0.12;
  const COLLAPSE_THRESHOLD = 0.04;
  const DECAY_HALF_LIFE = 86400000;
  const DEBOUNCE_MS = 2000;
  const SCORE_INTERVAL = 5000;
  let panels = [];
  let scores = {};
  let dirtyPanels = new Set();
  let observers = {};
  let scoreTimer = null;
  let saveTimer = null;
  let domRefs = {};
  const defaultPanels = [
    { id:'revenue', title:'Revenue', type:'metric', content:{value:'$128.4K', change:'+12.3%', target:85}, locked:false },
    { id:'users', title:'Active Users', type:'metric', content:{value:'2,847', change:'+5.7%', target:70}, locked:false },
    { id:'cpu', title:'CPU Usage', type:'chart', content:{value:42, unit:'%', color:'green'}, locked:false },
    { id:'memory', title:'Memory', type:'chart', content:{value:68, unit:'%', color:'warn'}, locked:false },
    { id:'errors', title:'Error Rate', type:'metric', content:{value:'0.12%', change:'-0.03%', target:95}, locked:false },
    { id:'latency', title:'P95 Latency', type:'chart', content:{value:210, unit:'ms', color:'green'}, locked:false },
    { id:'throughput', title:'Throughput', type:'metric', content:{value:'1.2K/s', change:'+8.1%', target:60}, locked:false },
    { id:'disk', title:'Disk I/O', type:'chart', content:{value:55, unit:'%', color:'green'}, locked:false },
    { id:'cache', title:'Cache Hit Rate', type:'metric', content:{value:'94.7%', change:'+1.2%', target:90}, locked:false },
    { id:'queue', title:'Queue Depth', type:'chart', content:{value:18, unit:'items', color:'warn'}, locked:false },
  ];
  function now() { return Date.now(); }
  function loadCache(key) {
    try {
      const raw = localStorage.getItem('ad_' + key);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (data._expiry && now() > data._expiry) { localStorage.removeItem('ad_' + key); return null; }
      return data._payload !== undefined ? data._payload : data;
    } catch(e) { return null; }
  }
  function saveCache(key, payload, ttl) {
    try {
      const data = { _payload: payload, _expiry: now() + ttl };
      localStorage.setItem('ad_' + key, JSON.stringify(data));
    } catch(e) {}
  }
  function loadPanels() {
    const cached = loadCache('panels');
    if (cached && Array.isArray(cached) && cached.length) return cached;
    return defaultPanels.map(p => ({...p, content:{...p.content}}));
  }
  function savePanels() {
    saveCache('panels', panels, CACHE_TTL.prefs);
  }
  function loadScores() {
    const cached = loadCache('scores');
    if (cached && typeof cached === 'object') return cached;
    return {};
  }
  function saveScores() {
    saveCache('scores', scores, CACHE_TTL.scores);
  }
  function loadOverrides() {
    const cached = loadCache('overrides');
    if (cached && typeof cached === 'object') return cached;
    return {};
  }
  function saveOverrides(overrides) {
    saveCache('overrides', overrides, CACHE_TTL.prefs);
  }
  function computeScore(panelId, metric) {
    const m = metric || { viewDuration: 0, interactions: 0, lastViewed: 0, collapseCount: 0 };
    const hoursSinceView = Math.max(0, (now() - (m.lastViewed || 0)) / 3600000);
    const recencyFactor = Math.pow(0.5, hoursSinceView / (DECAY_HALF_LIFE / 3600000));
    const freqComponent = Math.log2((m.interactions || 0) + 2);
    const durComponent = Math.log2((m.viewDuration || 0) / 1000 + 2);
    const rawScore = freqComponent * durComponent * recencyFactor;
    const penalty = 1 / (1 + (m.collapseCount || 0));
    return rawScore * penalty;
  }
  function recomputeAllScores() {
    const metrics = loadScores();
    let changed = false;
    panels.forEach(p => {
      const old = scores[p.id] || 0;
      const ns = computeScore(p.id, metrics[p.id]);
      if (Math.abs(old - ns) > 0.001) { changed = true; dirtyPanels.add(p.id); }
      scores[p.id] = ns;
    });
    if (changed) saveScores();
    return changed;
  }
  function rankPanels() {
    const overrides = loadOverrides();
    const maxScore = Math.max(...Object.values(scores), 0.001);
    return panels.map(p => {
      const norm = maxScore > 0 ? (scores[p.id] || 0) / maxScore : 0;
      return { ...p, score: scores[p.id] || 0, norm };
    }).sort((a, b) => {
      if (a.locked && !b.locked) return -1;
      if (!a.locked && b.locked) return 1;
      if (overrides[a.id] !== undefined && overrides[b.id] === undefined) return -1;
      if (overrides[a.id] === undefined && overrides[b.id] !== undefined) return 1;
      return b.score - a.score;
    });
  }
  function panelClass(p, norm) {
    if (norm < COLLAPSE_THRESHOLD && !p.locked) return 'collapsed';
    if (norm < COMPACT_THRESHOLD && !p.locked) return 'compact';
    if (norm > 0.65 && !p.locked) return 'span2';
    return '';
  }
  function buildHTML(p, cls) {
    const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const lockCls = p.locked ? 'locked' : '';
    let body = '';
    if (p.type === 'metric') {
      body = '<div class="metric-value">' + esc(p.content.value) + '</div>'
        + '<div class="metric-label">' + esc(p.content.change || '') + '</div>'
        + '<div class="chart-bar"><div class="chart-fill" style="width:' + (p.content.target || 50) + '%"></div></div>';
    } else {
      const color = p.content.color || 'green';
      body = '<div class="metric-value">' + esc(String(p.content.value)) + '<span style="font-size:0.6em;color:var(--text2)"> ' + esc(p.content.unit || '') + '</span></div>'
        + '<div class="chart-bar"><div class="chart-fill ' + color + '" style="width:' + Math.min(100, p.content.value || 0) + '%"></div></div>';
    }
    const scoreStr = p.score ? (p.score < 10 ? p.score.toFixed(2) : p.score.toFixed(0)) : '0';
    return '<div class="panel ' + cls + ' ' + lockCls + '" data-id="' + esc(p.id) + '" id="panel-' + esc(p.id) + '">'
      + '<div class="score-badge">s:' + scoreStr + '</div>'
      + '<div class="panel-header">'
      + '<span class="panel-title">' + esc(p.title) + '</span>'
      + '<div class="panel-actions">'
      + '<button class="panel-btn lock-btn ' + lockCls + '" data-action="lock" data-id="' + esc(p.id) + '">' + (p.locked ? '🔒' : '🔓') + '</button>'
      + '<button class="panel-btn" data-action="collapse" data-id="' + esc(p.id) + '">−</button>'
      + '</div></div>'
      + '<div class="panel-body"><div class="panel-content">' + body + '</div></div></div>';
  }
  function renderPanel(p, cls, container) {
    const existing = container.querySelector('#panel-' + p.id);
    const html = buildHTML(p, cls);
    if (existing) {
      const temp = document.createElement('div');
      temp.innerHTML = html;
      const newNode = temp.firstElementChild;
      if (existing.className !== newNode.className || existing.querySelector('.score-badge')?.textContent !== newNode.querySelector('.score-badge')?.textContent) {
        existing.replaceWith(newNode);
        bindPanelEvents(newNode);
        observePanel(newNode, p.id);
        return newNode;
      }
      existing.querySelector('.score-badge').textContent = 's:' + (p.score < 10 ? p.score.toFixed(2) : p.score.toFixed(0));
      return existing;
    }
    const temp = document.createElement('div');
    temp.innerHTML = html;
    const node = temp.firstElementChild;
    container.appendChild(node);
    bindPanelEvents(node);
    observePanel(node, p.id);
    return node;
  }
  function renderAll(force) {
    recomputeAllScores();
    const ranked = rankPanels();
    const grid = document.getElementById('grid');
    const more = document.getElementById('morePanels');
    if (force) {
      grid.innerHTML = '';
      more.innerHTML = '';
      domRefs = {};
    }
    const visibleIds = new Set();
    ranked.forEach(p => {
      const cls = panelClass(p, p.norm);
      if (cls === 'collapsed') {
        const node = renderPanel(p, 'compact', more);
        domRefs[p.id] = node;
      } else {
        const node = renderPanel(p, cls, grid);
        domRefs[p.id] = node;
        visibleIds.add(p.id);
      }
    });
    Array.from(grid.children).forEach(child => {
      const id = child.getAttribute('data-id');
      if (id && !visibleIds.has(id)) child.remove();
    });
    updateMoreToggle();
  }
  function incrementalRender() {
    if (dirtyPanels.size === 0) return;
    recomputeAllScores();
    const ranked = rankPanels();
    const grid = document.getElementById('grid');
    const more = document.getElementById('morePanels');
    const panelMap = new Map(ranked.map(p => [p.id, p]));
    dirtyPanels.forEach(id => {
      const p = panelMap.get(id);
      if (!p) return;
      const cls = panelClass(p, p.norm);
      const oldNode = domRefs[id];
      const targetContainer = cls === 'collapsed' ? more : grid;
      if (oldNode) {
        const inGrid = grid.contains(oldNode);
        const inMore = more.contains(oldNode);
        const shouldBeGrid = cls !== 'collapsed';
        if ((inGrid && !shouldBeGrid) || (inMore && shouldBeGrid)) {
          const newNode = renderPanel(p, cls, targetContainer);
          domRefs[id] = newNode;
          oldNode.remove();
        } else {
          domRefs[id] = renderPanel(p, cls, targetContainer);
        }
      } else {
        domRefs[id] = renderPanel(p, cls, targetContainer);
      }
    });
    dirtyPanels.clear();
    updateMoreToggle();
    updateScoreDisplay();
  }
  function updateMoreToggle() {
    const more = document.getElementById('morePanels');
    const toggle = document.getElementById('moreToggle');
    const count = more.children.length;
    if (count === 0) {
      toggle.style.display = 'none';
    } else {
      toggle.style.display = '';
      toggle.textContent = 'More panels (' + count + ') ▸';
    }
  }
  function updateScoreDisplay() {
    const el = document.getElementById('scoreDisplay');
    if (!el) return;
    const ranked = rankPanels();
    const top3 = ranked.slice(0, 3).map(p => p.title).join(', ');
    el.textContent = 'Top: ' + top3;
  }
  function recordMetric(panelId, field, delta) {
    const all = loadScores();
    if (!all[panelId]) all[panelId] = { viewDuration: 0, interactions: 0, lastViewed: 0, collapseCount: 0 };
    if (field === 'viewDuration') all[panelId].viewDuration += delta;
    else if (field === 'interactions') all[panelId].interactions += delta;
    else if (field === 'lastViewed') all[panelId].lastViewed = now();
    else if (field === 'collapseCount') all[panelId].collapseCount += delta;
    const oldScore = scores[panelId] || 0;
    const newScore = computeScore(panelId, all[panelId]);
    if (Math.abs(oldScore - newScore) > 0.001) dirtyPanels.add(panelId);
    scores[panelId] = newScore;
    saveScores();
    saveCache('scores', all, CACHE_TTL.scores);
  }
  function observePanel(node, panelId) {
    if (observers[panelId]) observers[panelId].disconnect();
    let entryTime = 0;
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          entryTime = now();
          recordMetric(panelId, 'lastViewed', 0);
        } else if (entryTime > 0) {
          const dur = now() - entryTime;
          recordMetric(panelId, 'viewDuration', dur);
          entryTime = 0;
        }
      });
    }, { threshold: 0.3 });
    observer.observe(node);
    observers[panelId] = observer;
    node.addEventListener('mouseenter', () => recordMetric(panelId, 'interactions', 1));
    node.addEventListener('click', () => recordMetric(panelId, 'interactions', 1));
  }
  function bindPanelEvents(node) {
    const id = node.getAttribute('data-id');
    node.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const action = btn.getAttribute('data-action');
        if (action === 'lock') toggleLock(id);
        if (action === 'collapse') toggleCollapse(id);
      });
    });
  }
  function toggleLock(panelId) {
    const p = panels.find(x => x.id === panelId);
    if (!p) return;
    p.locked = !p.locked;
    dirtyPanels.add(panelId);
    savePanels();
    incrementalRender();
    showToast(p.locked ? 'Locked: ' + p.title : 'Unlocked: ' + p.title);
  }
  function toggleCollapse(panelId) {
    const all = loadScores();
    if (!all[panelId]) all[panelId] = { viewDuration: 0, interactions: 0, lastViewed: 0, collapseCount: 0 };
    all[panelId].collapseCount += 1;
    saveCache('scores', all, CACHE_TTL.scores);
    scores[panelId] = computeScore(panelId, all[panelId]);
    dirtyPanels.add(panelId);
    incrementalRender();
  }
  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timeout);
    t._timeout = setTimeout(() => t.classList.remove('show'), 2000);
  }
  function resetAll() {
    localStorage.removeItem('ad_panels');
    localStorage.removeItem('ad_scores');
    localStorage.removeItem('ad_overrides');
    panels = defaultPanels.map(p => ({...p, content:{...p.content}}));
    scores = {};
    dirtyPanels = new Set(panels.map(p => p.id));
    Object.values(observers).forEach(o => o.disconnect());
    observers = {};
    domRefs = {};
    savePanels();
    renderAll(true);
    showToast('Dashboard reset');
  }
  function exportLayout() {
    const data = {
      panels: panels.map(p => ({ id:p.id, title:p.title, locked:p.locked })),
      scores,
      overrides: loadOverrides(),
      exported: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dashboard-layout-' + new Date().toISOString().slice(0,10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Layout exported');
  }
  function importLayout(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const data = JSON.parse(e.target.result);
        if (data.panels && Array.isArray(data.panels)) {
          data.panels.forEach(imp => {
            const existing = panels.find(p => p.id === imp.id);
            if (existing) existing.locked = imp.locked || false;
          });
          if (data.overrides) saveOverrides(data.overrides);
          savePanels();
          dirtyPanels = new Set(panels.map(p => p.id));
          renderAll(true);
          showToast('Layout imported');
        }
      } catch(err) {
        showToast('Import failed: invalid file');
      }
    };
    reader.readAsText(file);
  }
  function init() {
    panels = loadPanels();
    scores = loadScores();
    Object.keys(scores).forEach(id => {
      if (!panels.find(p => p.id === id)) delete scores[id];
    });
    renderAll(true);
    document.getElementById('btnReset').addEventListener('click', resetAll);
    document.getElementById('btnExport').addEventListener('click', exportLayout);
    document.getElementById('btnImport').addEventListener('click', () => document.getElementById('importFile').click());
    document.getElementById('importFile').addEventListener('change', e => {
      if (e.target.files[0]) importLayout(e.target.files[0]);
      e.target.value = '';
    });
    document.getElementById('moreToggle').addEventListener('click', () => {
      document.getElementById('morePanels').classList.toggle('open');
      const t = document.getElementById('moreToggle');
      t.textContent = document.getElementById('morePanels').classList.contains('open') ? 'More panels ▾' : 'More panels ▸';
    });
    scoreTimer = setInterval(() => {
      recomputeAllScores();
      if (dirtyPanels.size > 0) incrementalRender();
    }, SCORE_INTERVAL);
    window.addEventListener('beforeunload', () => {
      Object.values(observers).forEach(o => o.disconnect());
      savePanels();
      saveScores();
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  function validateIntegrity() {
    const tags = document.documentElement.outerHTML;
    const openDivs = (tags.match(/<div/g) || []).length;
    const closeDivs = (tags.match(/<\/div>/g) || []).length;
    const openScripts = (tags.match(/<script/g) || []).length;
    const closeScripts = (tags.match(/<\/script>/g) || []).length;
    if (openDivs !== closeDivs) console.error('INTEGRITY: unbalanced div tags', openDivs, closeDivs);
    if (openScripts !== closeScripts) console.error('INTEGRITY: unbalanced script tags', openScripts, closeScripts);
    return openDivs === closeDivs && openScripts === closeScripts;
  }
  setTimeout(() => { if (!validateIntegrity()) console.error('SELF-CHECK FAILED: unbalanced tags'); }, 100);
})();
</script>
</body>
</html>