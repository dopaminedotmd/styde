<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4eb;--muted:#8b8fa8;--accent:#6c8cff;--warn:#f0a040;--good:#4caf88;--bad:#f05050;--compact-bg:#141720;--focus-ring:#6c8cff88}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.4}
.skip-link{position:absolute;top:-100px;left:8px;background:var(--accent);color:#fff;padding:8px 16px;z-index:100;border-radius:4px}
.skip-link:focus{top:8px}
.header{display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 20px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:10}
.header h1{font-size:1.1rem;font-weight:600;flex:1;min-width:200px}
.status{font-size:0.8rem;color:var(--muted)}
.btn{background:var(--border);color:var(--text);border:1px solid var(--border);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.85rem;transition:background .15s}
.btn:hover,.btn:focus-visible{background:#3a3d4a}
.btn:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.dashboard{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:16px;max-width:1400px;margin:0 auto}
@media(max-width:900px){.dashboard{grid-template-columns:repeat(2,1fr)}}
@media(max-width:500px){.dashboard{grid-template-columns:1fr}}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;transition:border-color .2s,box-shadow .2s;position:relative;display:flex;flex-direction:column;gap:10px;min-height:120px}
.panel:focus-within{outline:2px solid var(--focus-ring);outline-offset:2px}
.panel.highlight{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.normal{grid-column:span 1;grid-row:span 1}
.panel.compact{grid-column:span 1;grid-row:span 1;min-height:60px;padding:10px 14px;background:var(--compact-bg);gap:4px;cursor:pointer}
.panel.locked{border-style:dashed}
.panel.locked::after{content:"🔒";position:absolute;top:6px;right:10px;font-size:0.7rem;opacity:.6}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.panel-title{font-weight:600;font-size:0.9rem;color:var(--text)}
.panel-badge{font-size:0.65rem;padding:2px 8px;border-radius:10px;font-weight:500;white-space:nowrap}
.badge-real{background:#1a3a2a;color:var(--good)}
.badge-sim{background:#3a2a1a;color:var(--warn)}
.panel-value{font-size:1.8rem;font-weight:700;line-height:1}
.panel-meta{font-size:0.72rem;color:var(--muted)}
.panel-actions{display:flex;gap:6px;margin-top:auto}
.panel-actions .btn{padding:3px 10px;font-size:0.72rem}
.compact-preview{display:flex;align-items:center;gap:10px}
.compact-preview .panel-value{font-size:1.2rem}
.lock-indicator{font-size:0.7rem;color:var(--accent)}
.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.empty-state{grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--muted)}
.error-toast{position:fixed;bottom:20px;right:20px;background:var(--bad);color:#fff;padding:12px 20px;border-radius:8px;font-size:0.85rem;z-index:100;max-width:360px;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
[role="alert"]:empty{display:none}
</style>
</head>
<body>
<a href="#dashboard" class="skip-link">Skip to dashboard</a>
<header class="header">
<h1>Adaptive Layout</h1>
<div class="toolbar">
<span class="status" id="status" aria-live="polite">Tracking 0 panels</span>
<button class="btn" id="btn-reset" aria-label="Reset layout to defaults">Reset</button>
</div>
</header>
<main id="dashboard" class="dashboard" role="region" aria-label="Metric dashboard" aria-live="polite"></main>
<div id="toast-container" role="alert" aria-live="assertive"></div>
<script>
(function(){
'use strict';
var STORAGE_KEY = 'adaptive_layout_v1';
var RECENCY_BUCKETS = [1,5,30,120];
var RECENCY_MULTS = [5,3,2,1];
var RECENCY_FALLBACK = 0.5;
var panels = [];
var tracking = {};
var locks = {};
var observer = null;
var visibilityTimers = {};
var bcChannel = null;
var tabId = 'tab_' + Date.now() + '_' + Math.random().toString(36).slice(2,6);
var peerTabs = new Set();
function safeLocalStorage(fn, fallback){
  try { return fn(); }
  catch(e){ console.warn('localStorage error:', e); showToast('Storage unavailable — layout will not persist'); return fallback; }
}
function loadState(){
  return safeLocalStorage(function(){
    var raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return null;
    var data = JSON.parse(raw);
    if(data && typeof data === 'object'){
      tracking = data.tracking || {};
      locks = data.locks || {};
    }
    return data;
  }, null);
}
function saveState(){
  safeLocalStorage(function(){
    var data = { tracking: tracking, locks: locks, savedAt: Date.now() };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }, null);
}
function showToast(msg){
  var el = document.getElementById('toast-container');
  el.textContent = msg;
  el.className = 'error-toast';
  setTimeout(function(){ el.textContent = ''; el.className = ''; }, 4000);
}
function metricCPU(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  var longTasks = 0;
  try {
    var po = new PerformanceObserver(function(list){
      longTasks += list.getEntries().length;
      if(val) val.textContent = longTasks + ' tasks';
      if(meta) meta.textContent = 'since load';
    });
    po.observe({type:'longtask',buffered:true});
    setTimeout(function(){ po.disconnect(); }, 120000);
    if(val) val.textContent = '0 tasks';
    if(meta) meta.textContent = 'monitoring...';
  } catch(e){
    if(val) val.textContent = '--';
    if(meta) meta.textContent = 'API not available';
    return true;
  }
  return false;
}
function metricMemory(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  try {
    if(performance.memory){
      var mb = (performance.memory.usedJSHeapSize / 1048576).toFixed(1);
      if(val) val.textContent = mb + ' MB';
      if(meta) meta.textContent = 'limit: ' + (performance.memory.jsHeapSizeLimit / 1048576).toFixed(0) + ' MB';
      var intv = setInterval(function(){
        var m = (performance.memory.usedJSHeapSize / 1048576).toFixed(1);
        if(val) val.textContent = m + ' MB';
      }, 3000);
      setTimeout(function(){ clearInterval(intv); }, 300000);
      return false;
    }
  } catch(e){}
  if(val) val.textContent = '--';
  if(meta) meta.textContent = 'Chrome only';
  return true;
}
function metricDisk(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  try {
    if(navigator.storage && navigator.storage.estimate){
      navigator.storage.estimate().then(function(est){
        if(est.usage && est.quota){
          var pct = ((est.usage / est.quota) * 100).toFixed(1);
          if(val) val.textContent = pct + '%';
          if(meta) meta.textContent = (est.usage/1048576).toFixed(0) + ' / ' + (est.quota/1048576).toFixed(0) + ' MB';
        } else {
          if(val) val.textContent = '--';
          if(meta) meta.textContent = 'no data';
        }
      }).catch(function(){
        if(val) val.textContent = '--';
        if(meta) meta.textContent = 'error';
      });
      return false;
    }
  } catch(e){}
  if(val) val.textContent = '--';
  if(meta) meta.textContent = 'API unavailable';
  return true;
}
function metricTabs(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  peerTabs.add(tabId);
  if(val) val.textContent = peerTabs.size;
  if(meta) meta.textContent = 'active tabs';
  var update = function(){ if(val) val.textContent = peerTabs.size; };
  try {
    bcChannel = new BroadcastChannel('adaptive_layout_tabs');
    bcChannel.postMessage({type:'hello',id:tabId});
    bcChannel.onmessage = function(ev){
      if(ev.data && ev.data.type === 'hello' && ev.data.id){
        peerTabs.add(ev.data.id);
        update();
        bcChannel.postMessage({type:'ack',id:tabId});
      }
      if(ev.data && ev.data.type === 'ack' && ev.data.id){
        peerTabs.add(ev.data.id);
        update();
      }
    };
    setInterval(function(){
      bcChannel.postMessage({type:'hello',id:tabId});
    }, 10000);
    return false;
  } catch(e){
    if(val) val.textContent = '1';
    if(meta) meta.textContent = 'API unavailable (simulated)';
    return true;
  }
}
function metricNetwork(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  try {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if(conn){
      var update = function(){
        if(val) val.textContent = conn.effectiveType || conn.type || '?';
        if(meta) meta.textContent = (conn.downlink || '?') + ' Mbps, RTT ' + (conn.rtt || '?') + 'ms';
      };
      update();
      conn.addEventListener('change', update);
      return false;
    }
  } catch(e){}
  if(val) val.textContent = '--';
  if(meta) meta.textContent = 'API unavailable';
  return true;
}
function metricErrors(panelEl){
  var val = panelEl.querySelector('.panel-value');
  var meta = panelEl.querySelector('.panel-meta');
  var count = 0;
  if(val) val.textContent = '0';
  if(meta) meta.textContent = 'monitoring...';
  var handler = function(){
    count++;
    if(val) val.textContent = count;
    if(meta) meta.textContent = 'caught';
  };
  window.addEventListener('error', handler);
  window.addEventListener('unhandledrejection', handler);
  setTimeout(function(){
    window.removeEventListener('error', handler);
    window.removeEventListener('unhandledrejection', handler);
  }, 600000);
  return false;
}
var PANEL_DEFS = [
  {id:'cpu',title:'CPU (Long Tasks)',metric:metricCPU,icon:'⚡'},
  {id:'memory',title:'Memory Usage',metric:metricMemory,icon:'🧠'},
  {id:'disk',title:'Disk Usage',metric:metricDisk,icon:'💾'},
  {id:'tabs',title:'Active Tabs',metric:metricTabs,icon:'👥'},
  {id:'network',title:'Network',metric:metricNetwork,icon:'📶'},
  {id:'errors',title:'Errors',metric:metricErrors,icon:'🐛'}
];
function createPanel(def){
  var el = document.createElement('div');
  el.className = 'panel normal';
  el.setAttribute('role','article');
  el.setAttribute('aria-label', def.title + ' panel');
  el.setAttribute('tabindex','0');
  el.setAttribute('data-panel-id', def.id);
  el.innerHTML =
    '<div class="panel-header">' +
      '<span class="panel-title">' + def.icon + ' ' + def.title + '</span>' +
      '<span class="panel-badge badge-sim" aria-label="simulated metric">simulated</span>' +
    '</div>' +
    '<div class="panel-value" aria-live="polite">--</div>' +
    '<div class="panel-meta">loading...</div>' +
    '<div class="panel-actions">' +
      '<button class="btn btn-lock" aria-label="Lock ' + def.title + ' position">Lock</button>' +
    '</div>';
  var badge = el.querySelector('.panel-badge');
  var isSim = def.metric(el);
  if(isSim){
    badge.className = 'panel-badge badge-sim';
    badge.textContent = 'simulated';
  } else {
    badge.className = 'panel-badge badge-real';
    badge.textContent = 'live';
  }
  el.querySelector('.btn-lock').addEventListener('click', function(e){
    e.stopPropagation();
    toggleLock(def.id, el);
  });
  el.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){
      e.preventDefault();
      if(el.classList.contains('compact')){
        expandPanel(def.id, el);
      }
    }
    if(e.key === 'Escape'){
      if(el.classList.contains('compact')){
        e.preventDefault();
        collapsePanel(def.id, el);
      }
    }
  });
  el.addEventListener('click', function(e){
    if(e.target.tagName === 'BUTTON') return;
    if(el.classList.contains('compact')){
      expandPanel(def.id, el);
    }
    recordInteraction(def.id);
  });
  el.addEventListener('focus', function(){
    recordInteraction(def.id);
  });
  return el;
}
function toggleLock(id, el){
  if(locks[id]){
    delete locks[id];
    el.classList.remove('locked');
    el.querySelector('.btn-lock').classList.remove('active');
    el.querySelector('.btn-lock').textContent = 'Lock';
  } else {
    locks[id] = {position: getPanelPosition(el), size: getPanelSize(el)};
    el.classList.add('locked');
    el.querySelector('.btn-lock').classList.add('active');
    el.querySelector('.btn-lock').textContent = 'Unlock';
  }
  saveState();
}
function getPanelPosition(el){
  var idx = Array.from(el.parentNode.children).indexOf(el);
  return idx;
}
function getPanelSize(el){
  if(el.classList.contains('large')) return 'large';
  if(el.classList.contains('compact')) return 'compact';
  return 'normal';
}
function recordInteraction(id){
  if(!tracking[id]){
    tracking[id] = { interactions: 0, viewStart: null, totalViewMs: 0, lastInteraction: 0 };
  }
  tracking[id].interactions++;
  tracking[id].lastInteraction = Date.now();
  saveState();
  rankAndLayout();
}
function computeScore(id){
  var t = tracking[id] || { interactions: 0, totalViewMs: 0, lastInteraction: 0 };
  var freq = t.interactions || 0;
  var durSec = (t.totalViewMs || 0) / 1000;
  if(freq === 0 && durSec === 0) {
    var idx = PANEL_DEFS.findIndex(function(d){ return d.id === id; });
    return -idx;
  }
  var minsSince = t.lastInteraction ? (Date.now() - t.lastInteraction) / 60000 : 999;
  var recencyMult = RECENCY_FALLBACK;
  for(var i = 0; i < RECENCY_BUCKETS.length; i++){
    if(minsSince <= RECENCY_BUCKETS[i]){ recencyMult = RECENCY_MULTS[i]; break; }
  }
  return freq * Math.max(durSec, 1) * recencyMult;
}
var currentLayout = [];
var layoutVersion = 0;
function rankAndLayout(){
  var now = Date.now();
  var ranked = PANEL_DEFS.map(function(def){
    return { id: def.id, score: computeScore(def.id) };
  });
  ranked.sort(function(a,b){ return b.score - a.score; });
  var layout = [];
  var usedIds = {};
  for(var i = 0; i < ranked.length; i++){
    var id = ranked[i].id;
    if(locks[id]){
      layout.push({id:id, size:locks[id].size, locked:true, score:ranked[i].score});
      usedIds[id] = true;
    }
  }
  for(var j = 0; j < ranked.length; j++){
    var rid = ranked[j].id;
    if(!usedIds[rid]){
      var sz = 'normal';
      if(j === 0) sz = 'large';
      else if(j === 1) sz = 'large';
      else if(j >= 5) sz = 'compact';
      layout.push({id:rid, size:sz, locked:false, score:ranked[j].score});
    }
  }
  if(JSON.stringify(currentLayout.map(function(l){return l.id+l.size;})) !==
     JSON.stringify(layout.map(function(l){return l.id+l.size;}))){
    currentLayout = layout;
    layoutVersion++;
    applyLayout();
  }
}
function applyLayout(){
  var container = document.getElementById('dashboard');
  var existing = {};
  Array.from(container.children).forEach(function(el){
    existing[el.getAttribute('data-panel-id')] = el;
  });
  var fragment = document.createDocumentFragment();
  for(var i = 0; i < currentLayout.length; i++){
    var item = currentLayout[i];
    var panelEl = existing[item.id];
    if(!panelEl){
      var def = PANEL_DEFS.find(function(d){ return d.id === item.id; });
      if(def) panelEl = createPanel(def);
    }
    if(!panelEl) continue;
    panelEl.classList.remove('large','normal','compact','locked');
    panelEl.classList.add(item.size);
    if(item.locked) panelEl.classList.add('locked');
    if(item.size === 'compact'){
      collapsePanelDOM(panelEl, item.id);
    } else {
      expandPanelDOM(panelEl, item.id);
    }
    panelEl.style.order = i;
    fragment.appendChild(panelEl);
  }
  container.innerHTML = '';
  container.appendChild(fragment);
  updateStatus();
}
function collapsePanelDOM(el, id){
  var val = el.querySelector('.panel-value');
  var meta = el.querySelector('.panel-meta');
  var actions = el.querySelector('.panel-actions');
  if(val) val.style.display = 'none';
  if(meta) meta.style.display = 'none';
  if(actions) actions.style.display = 'none';
  el.setAttribute('aria-expanded','false');
  el.classList.add('compact');
}
function expandPanelDOM(el, id){
  var val = el.querySelector('.panel-value');
  var meta = el.querySelector('.panel-meta');
  var actions = el.querySelector('.panel-actions');
  if(val) val.style.display = '';
  if(meta) meta.style.display = '';
  if(actions) actions.style.display = '';
  el.setAttribute('aria-expanded','true');
  el.classList.remove('compact');
}
function collapsePanel(id, el){
  if(locks[id]) return;
  collapsePanelDOM(el, id);
}
function expandPanel(id, el){
  expandPanelDOM(el, id);
  recordInteraction(id);
  if(!locks[id]){
    setTimeout(function(){
      if(!locks[id]){
        rankAndLayout();
      }
    }, 5000);
  }
}
function updateStatus(){
  var status = document.getElementById('status');
  var total = PANEL_DEFS.length;
  var locked = Object.keys(locks).length;
  status.textContent = total + ' panels, ' + locked + ' locked';
}
function setupObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      var id = entry.target.getAttribute('data-panel-id');
      if(!id) return;
      if(entry.isIntersecting){
        if(!visibilityTimers[id]){
          visibilityTimers[id] = Date.now();
        }
      } else {
        if(visibilityTimers[id]){
          var elapsed = Date.now() - visibilityTimers[id];
          if(!tracking[id]) tracking[id] = { interactions: 0, viewStart: null, totalViewMs: 0, lastInteraction: 0 };
          tracking[id].totalViewMs += elapsed;
          delete visibilityTimers[id];
          saveState();
        }
      }
    });
  }, { threshold: 0.5 });
  var container = document.getElementById('dashboard');
  Array.from(container.children).forEach(function(el){
    observer.observe(el);
  });
}
function init(){
  loadState();
  var container = document.getElementById('dashboard');
  container.setAttribute('aria-busy','true');
  container.innerHTML = '';
  currentLayout = PANEL_DEFS.map(function(def, i){
    var sz = 'normal';
    if(i === 0) sz = 'large';
    else if(i === 1) sz = 'large';
    else if(i >= 5) sz = 'compact';
    if(locks[def.id]) sz = locks[def.id].size;
    return {id:def.id, size:sz, locked:!!locks[def.id], score:0};
  });
  applyLayout();
  container.setAttribute('aria-busy','false');
  setupObserver();
  var mutationObs = new MutationObserver(function(){
    setupObserver();
  });
  mutationObs.observe(container, { childList: true });
  document.getElementById('btn-reset').addEventListener('click', function(){
    if(confirm('Reset all layout data? This clears tracking and unlocks all panels.')){
      tracking = {};
      locks = {};
      saveState();
      currentLayout = [];
      init();
    }
  });
  updateStatus();
  window.addEventListener('beforeunload', function(){
    var container = document.getElementById('dashboard');
    Array.from(container.children).forEach(function(el){
      var id = el.getAttribute('data-panel-id');
      if(id && visibilityTimers[id]){
        var elapsed = Date.now() - visibilityTimers[id];
        if(!tracking[id]) tracking[id] = { interactions: 0, viewStart: null, totalViewMs: 0, lastInteraction: 0 };
        tracking[id].totalViewMs += elapsed;
        delete visibilityTimers[id];
      }
    });
    saveState();
  });
}
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
})();
</script>
</body>
</html>