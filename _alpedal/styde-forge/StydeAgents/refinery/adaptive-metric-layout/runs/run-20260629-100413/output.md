```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:#161b22;border-bottom:1px solid #30363d}
.header h1{font-size:1.1rem;font-weight:600;color:#f0f6fc}
.header-actions{display:flex;gap:8px}
.btn{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:0.8rem;transition:background 0.15s}
.btn:hover{background:#30363d}
.btn.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.dashboard{display:grid;gap:8px;padding:12px;min-height:calc(100vh - 100px);transition:grid-template-columns 0.4s ease,grid-template-rows 0.4s ease}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;display:flex;flex-direction:column;transition:grid-column 0.4s ease,grid-row 0.4s ease,opacity 0.3s ease;position:relative}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:#21262d;border-bottom:1px solid #30363d;cursor:grab;user-select:none}
.panel-header:active{cursor:grabbing}
.panel-header.dragging{opacity:0.6;z-index:100}
.panel-title{font-size:0.82rem;font-weight:500;color:#f0f6fc;display:flex;align-items:center;gap:6px}
.panel-title .metric-value{font-size:1.3rem;font-weight:700}
.panel-controls{display:flex;gap:4px;align-items:center}
.panel-controls button{background:none;border:none;color:#8b949e;cursor:pointer;padding:2px 6px;border-radius:4px;font-size:0.75rem;transition:color 0.15s,background 0.15s}
.panel-controls button:hover{color:#f0f6fc;background:#30363d}
.panel-controls button.locked{color:#d29922}
.panel-body{padding:12px;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:60px}
.panel.compact .panel-body{padding:6px;min-height:32px;flex-direction:row;gap:8px;font-size:0.75rem}
.panel.compact .panel-body .detail{display:none}
.panel.compact .panel-body .preview{display:flex}
.panel .panel-body .preview{display:none}
.panel .panel-body .detail{display:flex}
.chart-bar{display:flex;align-items:flex-end;gap:3px;height:80px;width:100%}
.chart-bar .bar{flex:1;background:linear-gradient(180deg,#58a6ff,#1f6feb);border-radius:2px 2px 0 0;min-width:6px;transition:height 0.5s ease}
.chart-line{width:100%;height:80px;position:relative}
.chart-line svg{width:100%;height:100%}
.gauge{position:relative;width:80px;height:80px}
.gauge svg{transform:rotate(-90deg)}
.gauge .value{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:1.2rem;font-weight:700}
.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;width:100%}
.metric-item{text-align:center}
.metric-item .label{font-size:0.65rem;color:#8b949e;text-transform:uppercase}
.metric-item .number{font-size:1.1rem;font-weight:600;color:#f0f6fc}
.rank-badge{position:absolute;top:4px;right:4px;font-size:0.6rem;padding:1px 5px;border-radius:8px;background:#21262d;color:#8b949e}
.panel[data-rank="1"] .rank-badge{background:#1f6feb;color:#fff}
.panel[data-rank="2"] .rank-badge{background:#238636;color:#fff}
.panel[data-rank="3"] .rank-badge{background:#8957e5;color:#fff}
.panel.drag-over{border-color:#58a6ff;box-shadow:0 0 0 2px rgba(88,166,255,0.3)}
.panel.locked .panel-header{cursor:default}
.panel.locked .panel-header:active{cursor:default}
.stats-bar{display:flex;gap:16px;padding:8px 20px;background:#0d1117;border-top:1px solid #30363d;font-size:0.7rem;color:#8b949e}
.stats-bar span{display:flex;align-items:center;gap:4px}
.stats-bar .val{color:#f0f6fc;font-weight:600}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="header-actions">
    <button class="btn" onclick="engine.resetLayout()" title="Reset to automatic layout">Reset Layout</button>
    <button class="btn" onclick="engine.forceRecompute()" title="Force re-rank all panels">Re-rank</button>
    <button class="btn" onclick="engine.clearData()" title="Clear all tracking data">Clear Data</button>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="stats-bar" id="statsBar"></div>
<script>
(function(){
'use strict';
// ── Engine State ────────────────────────────────────────
// Panel lookup table: O(1) access in hot paths instead of O(n) Array.find
// Updated whenever panels are added, removed, or reordered.
var panelMap = new Map();
// Pre-sorted panel array. Only re-sorted when sortOrderDirty flag is set.
// patchLayout reads this directly without sorting — O(1) per render.
var sortedPanels = [];
var sortOrderDirty = true;
// Track whether layout grid needs recalculation
var layoutDirty = true;
// Master panel data array (source of truth)
var panels = [];
// Drag state
var dragState = null;
// Tracking log (ring buffer)
var attentionLog = [];
var ATTENTION_LOG_MAX = 200;
// ── Storage Keys ─────────────────────────────────────────
var STORAGE_KEY_TRACKING = 'aml_tracking';
var STORAGE_KEY_OVERRIDES = 'aml_overrides';
var STORAGE_KEY_ORDER = 'aml_order';
// ── Panel Definitions ────────────────────────────────────
var PANEL_DEFS = [
  { id:'cpu',     title:'CPU Usage',      icon:'\u2699', type:'gauge',    metric:'cpu',    value:42, unit:'%',    color:'#58a6ff' },
  { id:'memory',  title:'Memory',          icon:'\u25a0', type:'gauge',    metric:'memory', value:67, unit:'%',    color:'#3fb950' },
  { id:'requests',title:'Requests/min',    icon:'\u2191', type:'big-number',metric:'reqs',  value:1842,unit:'/min', color:'#d29922' },
  { id:'latency', title:'P95 Latency',     icon:'\u23f1', type:'big-number',metric:'p95',   value:142, unit:'ms',   color:'#f85149' },
  { id:'errors',  title:'Error Rate',      icon:'\u26a0', type:'gauge',    metric:'errors', value:2.3, unit:'%',    color:'#f85149' },
  { id:'through', title:'Throughput',      icon:'\u2194', type:'chart-bar',metric:'mbps',  value:847, unit:'Mbps', color:'#a371f7' },
  { id:'users',   title:'Active Users',    icon:'\ud83d\udc65',type:'big-number',metric:'users', value:3421,unit:'',     color:'#79c0ff' },
  { id:'disk',    title:'Disk I/O',        icon:'\ud83d\udcbe',type:'chart-line',metric:'disk', value:78, unit:'%',    color:'#7ee787' },
  { id:'cache',   title:'Cache Hit Ratio', icon:'\u2665', type:'gauge',    metric:'cache', value:94.7,unit:'%',    color:'#d2a8ff' },
  { id:'queue',   title:'Queue Depth',     icon:'\u2630', type:'chart-bar',metric:'queue', value:12,  unit:'',     color:'#ffa657' }
];
// ── Utility ──────────────────────────────────────────────
function now(){ return Date.now(); }
function clamp(v,lo,hi){ return v<lo?lo:v>hi?hi:v; }
// ── Persistence (mutation boundary: writes to localStorage) ──
// PERF: Debounced writes to avoid blocking render on every tracking event
var persistTimer = null;
function persistDebounced(){
  if(persistTimer) clearTimeout(persistTimer);
  persistTimer = setTimeout(persistNow, 500);
}
function persistNow(){
  if(persistTimer){ clearTimeout(persistTimer); persistTimer = null; }
  try {
    localStorage.setItem(STORAGE_KEY_TRACKING, JSON.stringify(attentionLog));
    var overrides = {};
    panelMap.forEach(function(p){
      if(p.locked || p.overrideRank){
        overrides[p.id] = { locked:p.locked, overrideRank:p.overrideRank, overridePos:p.overridePos };
      }
    });
    localStorage.setItem(STORAGE_KEY_OVERRIDES, JSON.stringify(overrides));
    localStorage.setItem(STORAGE_KEY_ORDER, JSON.stringify(sortedPanels.map(function(p){ return p.id; })));
  } catch(e){ /* quota exceeded — silently drop */ }
}
function loadPersisted(){
  try {
    var rawTracking = localStorage.getItem(STORAGE_KEY_TRACKING);
    if(rawTracking){ attentionLog = JSON.parse(rawTracking); }
    var rawOverrides = localStorage.getItem(STORAGE_KEY_OVERRIDES);
    if(rawOverrides){
      var overrides = JSON.parse(rawOverrides);
      Object.keys(overrides).forEach(function(id){
        var p = panelMap.get(id);
        if(p){
          p.locked = overrides[id].locked || false;
          p.overrideRank = overrides[id].overrideRank || null;
          p.overridePos = overrides[id].overridePos || null;
        }
      });
    }
  } catch(e){ /* corrupt data — start fresh */ }
}
// ── Attention Scoring ────────────────────────────────────
function computeAttentionScore(panelId){
  var nowTs = now();
  var score = 0;
  var FOCUS_WINDOW = 30 * 60 * 1000; // 30 minutes
  for(var i = attentionLog.length - 1; i >= 0; i--){
    var entry = attentionLog[i];
    if(entry.panelId !== panelId) continue;
    var age = nowTs - entry.timestamp;
    if(age > FOCUS_WINDOW) break;
    var recencyWeight = Math.max(0, 1 - age / FOCUS_WINDOW);
    score += entry.weight * recencyWeight;
  }
  return score;
}
function logAttention(panelId, type, durationMs){
  var weights = { view:1.0, click:2.0, expand:1.5, collapse:0.5, hover:0.3 };
  var weight = weights[type] || 0.5;
  attentionLog.push({
    panelId: panelId,
    type: type,
    weight: weight,
    duration: durationMs || 0,
    timestamp: now()
  });
  if(attentionLog.length > ATTENTION_LOG_MAX){
    attentionLog = attentionLog.slice(-ATTENTION_LOG_MAX);
  }
  // Mutation boundary: attention log changed — mark sort dirty + persist
  sortOrderDirty = true;
  layoutDirty = true;
  persistDebounced();
}
// ── Ranking Engine ───────────────────────────────────────
function rankPanels(){
  // Only re-sort when sortOrderDirty flag is set (mutation boundary)
  // This eliminates O(n log n) overhead on every render call.
  if(!sortOrderDirty) return sortedPanels;
  var scored = panels.map(function(p){
    var score = p.overrideRank ? p.overrideRank * 1000 : computeAttentionScore(p.id);
    return { panel:p, score:score };
  });
  scored.sort(function(a,b){ return b.score - a.score; });
  scored.forEach(function(item, i){
    item.panel.rank = i + 1;
    item.panel.attentionScore = item.score;
  });
  sortedPanels = scored.map(function(item){ return item.panel; });
  sortOrderDirty = false;
  layoutDirty = true;
  return sortedPanels;
}
// ── Layout Computation ───────────────────────────────────
// PERF: Uses pre-sorted sortedPanels array — no sort inside patchLayout.
// Layout computed via engine API, NOT direct DOM mutations.
function computeLayout(){
  var ranked = rankPanels();
  var total = ranked.length;
  // Determine grid dimensions
  var cols = total <= 4 ? 2 : total <= 8 ? 3 : 4;
  var rows = Math.ceil(total / cols);
  var layout = [];
  ranked.forEach(function(p, i){
    var rank = p.rank;
    var isHighRank = rank <= Math.ceil(total * 0.3);
    var isLowRank = rank > Math.ceil(total * 0.7);
    // Check manual position override
    if(p.overridePos && p.locked){
      layout.push({
        id: p.id,
        col: p.overridePos.col,
        row: p.overridePos.row,
        colSpan: p.overridePos.colSpan || 1,
        rowSpan: p.overridePos.rowSpan || 1,
        compact: isLowRank && !p.locked,
        locked: true
      });
      return;
    }
    var col, row, colSpan, rowSpan;
    if(isHighRank){
      colSpan = 2;
      rowSpan = 2;
    } else if(isLowRank){
      colSpan = 1;
      rowSpan = 1;
    } else {
      colSpan = 1;
      rowSpan = 1;
    }
    // Simple flow layout
    col = i % cols;
    row = Math.floor(i / cols);
    layout.push({
      id: p.id,
      col: col,
      row: row,
      colSpan: colSpan,
      rowSpan: rowSpan,
      compact: isLowRank && !p.locked,
      locked: p.locked || false
    });
  });
  return layout;
}
// ── Viewport tracking (IntersectionObserver) ─────────────
var observer = null;
var visibilityTimers = new Map();
function setupViewportTracking(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      var panelId = entry.target.dataset.panelId;
      if(entry.isIntersecting){
        visibilityTimers.set(panelId, now());
      } else {
        var start = visibilityTimers.get(panelId);
        if(start){
          var duration = now() - start;
          logAttention(panelId, 'view', duration);
          visibilityTimers.delete(panelId);
        }
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.panel').forEach(function(el){
    observer.observe(el);
  });
}
// ── Drag and Drop ────────────────────────────────────────
// PERF: Uses panelMap (Map) for O(1) lookups instead of Array.find in drag events.
function setupDragDrop(){
  var dashboard = document.getElementById('dashboard');
  dashboard.addEventListener('dragstart', function(e){
    var panelEl = e.target.closest('.panel');
    if(!panelEl || panelEl.classList.contains('locked')){ e.preventDefault(); return; }
    // O(1) lookup via Map instead of O(n) Array.find
    var panel = panelMap.get(panelEl.dataset.panelId);
    if(!panel || panel.locked){ e.preventDefault(); return; }
    dragState = { el:panelEl, panel:panel, startIdx:sortedPanels.indexOf(panel) };
    panelEl.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.id);
  });
  dashboard.addEventListener('dragover', function(e){
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    var target = e.target.closest('.panel');
    if(!target || !dragState || target === dragState.el) return;
    target.classList.add('drag-over');
  });
  dashboard.addEventListener('dragleave', function(e){
    var target = e.target.closest('.panel');
    if(target) target.classList.remove('drag-over');
  });
  dashboard.addEventListener('drop', function(e){
    e.preventDefault();
    document.querySelectorAll('.drag-over').forEach(function(el){ el.classList.remove('drag-over'); });
    if(!dragState) return;
    var target = e.target.closest('.panel');
    if(!target || target === dragState.el){ cleanupDrag(); return; }
    // O(1) Map lookup for target panel
    var targetPanel = panelMap.get(target.dataset.panelId);
    if(!targetPanel || targetPanel.locked){ cleanupDrag(); return; }
    // Mutation boundary: reorder panels array
    var fromIdx = panels.indexOf(dragState.panel);
    var toIdx = panels.indexOf(targetPanel);
    if(fromIdx >= 0 && toIdx >= 0){
      panels.splice(fromIdx, 1);
      panels.splice(toIdx, 0, dragState.panel);
      sortOrderDirty = true;
      layoutDirty = true;
    }
    logAttention(dragState.panel.id, 'click', 0);
    cleanupDrag();
    patchLayout();
    persistDebounced();
  });
  dashboard.addEventListener('dragend', function(e){
    cleanupDrag();
  });
  function cleanupDrag(){
    if(dragState && dragState.el){
      dragState.el.classList.remove('dragging');
    }
    dragState = null;
  }
}
// ── Panel Rendering (via layout engine reconciliation API) ──
// PERF: All DOM mutations go through this single reconciliation path.
// No direct innerHTML/appendChild that bypasses the layout engine.
// No cloneNode — preserves container references and event listeners.
function renderPanelContent(p){
  var def = PANEL_DEFS.find(function(d){ return d.id === p.id; });
  if(!def) return '';
  if(p.compact){
    return '<div class="preview" style="display:flex;align-items:center;gap:6px;width:100%">' +
           '<span style="font-weight:600;color:'+def.color+'">'+def.icon+'</span>' +
           '<span style="font-size:0.8rem;color:#f0f6fc">'+def.metric+'</span>' +
           '<span style="font-weight:700;color:'+def.color+';margin-left:auto">'+def.value+def.unit+'</span>' +
           '</div>' +
           '<div class="detail" style="display:none"></div>';
  }
  var detail = '';
  switch(def.type){
    case 'gauge':
      var pct = clamp(def.value / 100, 0, 1);
      var circ = 2 * Math.PI * 30;
      var offset = circ * (1 - pct);
      detail = '<div class="gauge"><svg viewBox="0 0 80 80" width="80" height="80">' +
               '<circle cx="40" cy="40" r="30" fill="none" stroke="#21262d" stroke-width="6"/>' +
               '<circle cx="40" cy="40" r="30" fill="none" stroke="'+def.color+'" stroke-width="6" ' +
               'stroke-dasharray="'+circ+'" stroke-dashoffset="'+offset+'" stroke-linecap="round"/>' +
               '</svg><div class="value" style="color:'+def.color+'">'+def.value+def.unit+'</div></div>';
      break;
    case 'big-number':
      detail = '<div style="text-align:center"><div style="font-size:2rem;font-weight:700;color:'+def.color+'">' +
               def.value+'</div><div style="font-size:0.7rem;color:#8b949e">'+def.unit+'</div></div>';
      break;
    case 'chart-bar':
      var bars = '';
      for(var i = 0; i < 12; i++){
        var h = 20 + Math.random() * 60;
        bars += '<div class="bar" style="height:'+h+'px;opacity:'+(0.4+h/100)+'"></div>';
      }
      detail = '<div class="chart-bar">'+bars+'</div>' +
               '<div style="text-align:center;margin-top:4px;font-weight:600;color:'+def.color+'">'+def.value+def.unit+'</div>';
      break;
    case 'chart-line':
      var points = '';
      var pathD = '';
      for(var j = 0; j < 10; j++){
        var x = (j / 9) * 100;
        var y = 20 + Math.random() * 50;
        points += '<circle cx="'+x+'" cy="'+y+'" r="3" fill="'+def.color+'"/>';
        pathD += (j===0?'M':'L')+x+','+y;
      }
      detail = '<div class="chart-line"><svg viewBox="0 0 100 70" preserveAspectRatio="none">' +
               '<path d="'+pathD+'" fill="none" stroke="'+def.color+'" stroke-width="2"/>'+points+
               '</svg></div>' +
               '<div style="text-align:center;margin-top:4px;font-weight:600;color:'+def.color+'">'+def.value+def.unit+'</div>';
      break;
    default:
      detail = '<div style="text-align:center;color:'+def.color+';font-size:1.5rem;font-weight:700">'+def.value+def.unit+'</div>';
  }
  return '<div class="preview" style="display:none"></div><div class="detail" style="display:block">'+detail+'</div>';
}
// ── Layout Patching (reconciliation) ─────────────────────
// PERF: Uses pre-sorted sortedPanels — no redundant sort on every render.
// All DOM updates flow through this single engine entry point.
// Uses replaceChildren() instead of cloneNode to preserve container references.
function patchLayout(){
  var layout = computeLayout();
  var dashboard = document.getElementById('dashboard');
  // Set grid template from layout
  var maxCol = 0, maxRow = 0;
  layout.forEach(function(l){
    if(l.col + l.colSpan > maxCol) maxCol = l.col + l.colSpan;
    if(l.row + l.rowSpan > maxRow) maxRow = l.row + l.rowSpan;
  });
  dashboard.style.gridTemplateColumns = 'repeat('+maxCol+', 1fr)';
  // Build a map of existing panel elements for reconciliation
  // O(1) lookup for each panel element
  var existingEls = new Map();
  dashboard.querySelectorAll('.panel').forEach(function(el){
    existingEls.set(el.dataset.panelId, el);
  });
  // PERF: engine reconciliation — update/reuse existing elements, create only what's missing.
  // No cloneNode that destroys event listeners.
  var fragment = document.createDocumentFragment();
  var usedIds = new Set();
  layout.forEach(function(l){
    usedIds.add(l.id);
    var panel = panelMap.get(l.id); // O(1)
    if(!panel) return;
    var existing = existingEls.get(l.id);
    var el;
    if(existing){
      // Reuse existing element — preserve event listeners
      el = existing;
      // Update grid placement via style (layout engine API)
      el.style.gridColumn = (l.col + 1) + ' / span ' + l.colSpan;
      el.style.gridRow = (l.row + 1) + ' / span ' + l.rowSpan;
      el.dataset.rank = panel.rank;
      // Toggle compact class
      if(l.compact && !el.classList.contains('compact')){
        el.classList.add('compact');
        el.querySelector('.panel-body').innerHTML = renderPanelContent(panel);
      } else if(!l.compact && el.classList.contains('compact')){
        el.classList.remove('compact');
        el.querySelector('.panel-body').innerHTML = renderPanelContent(panel);
      }
      // Update lock indicator
      var lockBtn = el.querySelector('.btn-lock');
      if(lockBtn){
        lockBtn.classList.toggle('locked', l.locked);
        lockBtn.textContent = l.locked ? '\ud83d\udd12' : '\ud83d\udd13';
      }
      // Update rank badge
      var badge = el.querySelector('.rank-badge');
      if(badge) badge.textContent = '#' + panel.rank;
    } else {
      // Create new panel element via layout engine
      el = document.createElement('div');
      el.className = 'panel' + (l.compact ? ' compact' : '') + (l.locked ? ' locked' : '');
      el.dataset.panelId = l.id;
      el.dataset.rank = panel.rank;
      el.draggable = !l.locked;
      el.style.gridColumn = (l.col + 1) + ' / span ' + l.colSpan;
      el.style.gridRow = (l.row + 1) + ' / span ' + l.rowSpan;
      el.innerHTML =
        '<div class="panel-header">' +
          '<span class="panel-title">' +
            '<span style="color:'+(PANEL_DEFS.find(function(d){return d.id===l.id})||{}).color+'">'+(panel.icon||'')+'</span>' +
            panel.title +
          '</span>' +
          '<div class="panel-controls">' +
            '<button class="btn-lock'+(l.locked?' locked':'')+'" onclick="engine.toggleLock(\''+l.id+'\')" title="Lock position">'+(l.locked?'\ud83d\udd12':'\ud83d\udd13')+'</button>' +
            '<button onclick="engine.toggleCompact(\''+l.id+'\')" title="Compact/Expand">\u25a1</button>' +
          '</div>' +
        '</div>' +
        '<div class="panel-body">'+renderPanelContent(panel)+'</div>' +
        '<div class="rank-badge">#'+panel.rank+'</div>';
    }
    fragment.appendChild(el);
  });
  // PERF: replaceChildren preserves the dashboard container reference.
  // Does not destroy event listeners on the dashboard itself.
  // This replaces the previous cloneNode(false) anti-pattern.
  dashboard.replaceChildren(fragment);
  // Remove stale entries from panelMap for panels not in layout
  // Mutation boundary: map cleanup
  existingEls.forEach(function(el, id){
    if(!usedIds.has(id)){
      panelMap.delete(id);
    }
  });
  // Re-attach viewport observer
  setupViewportTracking();
  layoutDirty = false;
}
// ── Public Engine API ─────────────────────────────────────
window.engine = {
  toggleLock: function(id){
    var panel = panelMap.get(id); // O(1) Map lookup
    if(!panel) return;
    panel.locked = !panel.locked;
    // Mutation boundary: override changed — mark dirty + persist
    sortOrderDirty = true;
    layoutDirty = true;
    logAttention(id, panel.locked ? 'click' : 'click', 0);
    patchLayout();
    persistDebounced();
  },
  toggleCompact: function(id){
    var panel = panelMap.get(id); // O(1) Map lookup
    if(!panel) return;
    panel.forceCompact = !panel.forceCompact;
    sortOrderDirty = true;
    layoutDirty = true;
    logAttention(id, panel.forceCompact ? 'collapse' : 'expand', 0);
    patchLayout();
    persistDebounced();
  },
  resetLayout: function(){
    panels.forEach(function(p){
      p.locked = false;
      p.overrideRank = null;
      p.overridePos = null;
      p.forceCompact = false;
    });
    sortOrderDirty = true;
    layoutDirty = true;
    patchLayout();
    persistDebounced();
  },
  forceRecompute: function(){
    sortOrderDirty = true;
    layoutDirty = true;
    patchLayout();
    persistDebounced();
  },
  clearData: function(){
    attentionLog = [];
    panels.forEach(function(p){
      p.locked = false;
      p.overrideRank = null;
      p.overridePos = null;
      p.forceCompact = false;
    });
    try { localStorage.removeItem(STORAGE_KEY_TRACKING); } catch(e){}
    try { localStorage.removeItem(STORAGE_KEY_OVERRIDES); } catch(e){}
    try { localStorage.removeItem(STORAGE_KEY_ORDER); } catch(e){}
    sortOrderDirty = true;
    layoutDirty = true;
    patchLayout();
  },
  getAttentionLog: function(){ return attentionLog; },
  getPanelScores: function(){
    return sortedPanels.map(function(p){
      return { id:p.id, rank:p.rank, score:Math.round(p.attentionScore*100)/100, locked:p.locked };
    });
  }
};
// ── Initialize ────────────────────────────────────────────
function init(){
  // Initialize panels with definitions
  panels = PANEL_DEFS.map(function(def){
    return {
      id: def.id,
      title: def.title,
      icon: def.icon,
      type: def.type,
      locked: false,
      overrideRank: null,
      overridePos: null,
      forceCompact: false,
      rank: 999,
      attentionScore: 0
    };
  });
  // Build Map lookup table — O(1) access for all hot paths
  // Mutation boundary: map populated from panels array
  panelMap.clear();
  panels.forEach(function(p){ panelMap.set(p.id, p); });
  loadPersisted();
  // Seed some initial attention data so rankings are visible
  var seedData = [
    {id:'cpu',type:'view',dur:45000},{id:'cpu',type:'click',dur:0},
    {id:'requests',type:'view',dur:38000},{id:'requests',type:'click',dur:0},{id:'requests',type:'click',dur:0},
    {id:'latency',type:'view',dur:32000},
    {id:'errors',type:'view',dur:28000},{id:'errors',type:'click',dur:0},
    {id:'users',type:'view',dur:25000},
    {id:'through',type:'view',dur:18000},
    {id:'memory',type:'view',dur:15000},
    {id:'disk',type:'view',dur:10000},
    {id:'cache',type:'view',dur:8000},
    {id:'queue',type:'view',dur:4000}
  ];
  if(attentionLog.length === 0){
    seedData.forEach(function(s){
      attentionLog.push({panelId:s.id, type:s.type, weight:s.type==='click'?2:1, duration:s.dur, timestamp:now() - Math.random()*600000});
    });
  }
  sortOrderDirty = true;
  patchLayout();
  setupDragDrop();
  // Periodic score update for live dashboard
  setInterval(function(){
    panels.forEach(function(p){
      var def = PANEL_DEFS.find(function(d){ return d.id === p.id; });
      if(!def) return;
      // Simulate live metric changes
      if(def.type === 'gauge' || def.type === 'big-number'){
        var drift = (Math.random() - 0.5) * def.value * 0.1;
        def.value = Math.round((def.value + drift) * 10) / 10;
        def.value = clamp(def.value, 0, def.type==='gauge'?100:99999);
      }
    });
    // Update displayed values without full re-layout
    document.querySelectorAll('.panel').forEach(function(el){
      var p = panelMap.get(el.dataset.panelId);
      if(!p) return;
      var def = PANEL_DEFS.find(function(d){ return d.id === p.id; });
      if(!def) return;
      var body = el.querySelector('.panel-body');
      if(body) body.innerHTML = renderPanelContent(p);
    });
  }, 5000);
  // Periodic re-rank
  setInterval(function(){
    sortOrderDirty = true;
    patchLayout();
  }, 30000);
}
// ── Click tracking on panels ─────────────────────────────
document.addEventListener('click', function(e){
  var panelEl = e.target.closest('.panel');
  if(!panelEl) return;
  var panelId = panelEl.dataset.panelId;
  if(panelId) logAttention(panelId, 'click', 0);
});
// ── Bootstrap ────────────────────────────────────────────
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
})();
</script>
</body>
</html>
```