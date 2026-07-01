<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root { --bg: #0f1117; --surface: #1a1d27; --surface2: #232736; --border: #2d3348; --text: #e1e4ed; --text2: #8b92a8; --accent: #6c5ce7; --accent2: #00cec9; --danger: #fd79a8; --warn: #fdcb6e; --good: #00b894; --radius: 10px; --shadow: 0 4px 24px rgba(0,0,0,0.3); --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; padding: 20px; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
header h1 { font-size: 22px; font-weight: 600; letter-spacing: -0.3px; display: flex; align-items: center; gap: 10px; }
header h1::before { content: ''; display: inline-block; width: 10px; height: 26px; background: linear-gradient(var(--accent), var(--accent2)); border-radius: 5px; }
.controls { display: flex; gap: 8px; flex-wrap: wrap; }
.controls button { padding: 8px 16px; border: 1px solid var(--border); background: var(--surface); color: var(--text); border-radius: 8px; cursor: pointer; font-size: 13px; transition: var(--transition); }
.controls button:hover { background: var(--surface2); border-color: var(--accent); }
.controls button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.stats-bar { display: flex; gap: 16px; padding: 12px 16px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 20px; font-size: 13px; color: var(--text2); flex-wrap: wrap; }
.stats-bar span strong { color: var(--text); }
.dashboard-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; grid-auto-rows: minmax(80px, auto); transition: gap var(--transition); }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; transition: all var(--transition); position: relative; display: flex; flex-direction: column; }
.panel:hover { border-color: rgba(108,92,231,0.4); box-shadow: 0 0 0 1px rgba(108,92,231,0.15); }
.panel.dragging { opacity: 0.5; }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }
.panel-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; cursor: grab; user-select: none; border-bottom: 1px solid var(--border); background: var(--surface2); transition: background var(--transition); }
.panel-header:active { cursor: grabbing; }
.panel-header .panel-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.panel-header .panel-title .icon { width: 18px; height: 18px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; }
.panel-header .panel-actions { display: flex; gap: 4px; }
.panel-header .panel-actions button { width: 26px; height: 26px; border: none; background: transparent; color: var(--text2); border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: var(--transition); }
.panel-header .panel-actions button:hover { background: rgba(255,255,255,0.08); color: var(--text); }
.panel-header .panel-actions button.locked { color: var(--accent); }
.panel-body { padding: 16px; flex: 1; overflow-y: auto; transition: all var(--transition); position: relative; }
.panel.collapsed .panel-body { display: none; }
.panel.collapsed .panel-header { border-bottom: none; }
.panel.compact .panel-body { padding: 8px 12px; font-size: 12px; max-height: 60px; overflow: hidden; }
.panel.compact .panel-header { padding: 6px 12px; font-size: 11px; }
.panel.compact .panel-title .icon { width: 14px; height: 14px; font-size: 9px; }
.panel.locked { border-left: 3px solid var(--accent); }
.panel .rank-badge { position: absolute; top: 8px; right: 48px; font-size: 10px; color: var(--text2); background: var(--bg); padding: 2px 8px; border-radius: 10px; opacity: 0; transition: opacity var(--transition); pointer-events: none; }
.panel:hover .rank-badge { opacity: 1; }
.metric-value { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2; }
.metric-label { font-size: 12px; color: var(--text2); margin-top: 4px; }
.metric-change { font-size: 13px; margin-top: 6px; font-weight: 500; }
.metric-change.up { color: var(--good); }
.metric-change.down { color: var(--danger); }
.chart-area { height: 100px; margin-top: 8px; background: linear-gradient(180deg, rgba(108,92,231,0.15) 0%, transparent 100%); border-radius: 6px; position: relative; overflow: hidden; }
.chart-area .bar { position: absolute; bottom: 0; width: 12%; background: linear-gradient(180deg, var(--accent), var(--accent2)); border-radius: 4px 4px 0 0; transition: height 0.6s ease; min-height: 4px; }
.chart-area .bar:nth-child(2n) { background: linear-gradient(180deg, var(--accent2), #00b894); }
.mini-chart { height: 30px; background: linear-gradient(90deg, rgba(108,92,231,0.2), rgba(108,92,231,0.05)); border-radius: 4px; position: relative; overflow: hidden; }
.mini-chart .fill { position: absolute; bottom: 0; left: 0; right: 0; height: 100%; background: linear-gradient(90deg, var(--accent), transparent); border-radius: 4px; opacity: 0.6; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.status-dot.green { background: var(--good); }
.status-dot.yellow { background: var(--warn); }
.status-dot.red { background: var(--danger); }
.status-dot.blue { background: var(--accent); }
.status-row { display: flex; align-items: center; padding: 4px 0; font-size: 13px; }
.status-row span:last-child { margin-left: auto; color: var(--text2); font-size: 12px; }
.list-item { display: flex; align-items: center; padding: 4px 0; font-size: 13px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.list-item:last-child { border-bottom: none; }
.list-item .count { margin-left: auto; color: var(--text2); font-size: 12px; }
.compact-preview { display: flex; gap: 12px; align-items: center; }
.compact-preview .mini-metric { font-size: 18px; font-weight: 700; }
.compact-preview .mini-label { font-size: 11px; color: var(--text2); }
.drop-indicator { position: absolute; background: var(--accent); opacity: 0.3; border-radius: var(--radius); pointer-events: none; z-index: 10; transition: opacity 0.15s; }
#recent-activity { padding: 0; max-height: 180px; overflow-y: auto; }
#recent-activity .activity-item { padding: 6px 16px; font-size: 12px; color: var(--text2); border-bottom: 1px solid rgba(255,255,255,0.04); display: flex; justify-content: space-between; }
#recent-activity .activity-item .time { color: var(--text2); opacity: 0.6; }
.pulse { animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.empty-state { text-align: center; padding: 20px; color: var(--text2); font-size: 13px; }
.more-section { margin-top: 16px; display: none; }
.more-section.visible { display: block; }
.more-toggle { background: none; border: 1px dashed var(--border); color: var(--text2); padding: 8px; border-radius: var(--radius); cursor: pointer; font-size: 12px; width: 100%; transition: var(--transition); }
.more-toggle:hover { border-color: var(--accent); color: var(--text); }
@media (max-width: 900px) { .dashboard-grid { grid-template-columns: repeat(2, 1fr); } body { padding: 12px; } }
@media (max-width: 500px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Dashboard</h1>
  <div class="controls">
    <button id="btnAutoArrange" class="active">Auto-Arrange ON</button>
    <button id="btnResetLayout">Reset Layout</button>
    <button id="btnClearData">Clear Data</button>
  </div>
</header>
<div class="stats-bar" id="statsBar">
  <span>Panels: <strong id="totalPanels">0</strong></span>
  <span>Locked: <strong id="lockedCount">0</strong></span>
  <span>Compact: <strong id="compactCount">0</strong></span>
  <span>Top Panel: <strong id="topPanel">-</strong></span>
  <span>Interactions: <strong id="totalInteractions">0</strong></span>
</div>
<div class="dashboard-grid" id="dashboard"></div>
<div id="moreSection" class="more-section">
  <button class="more-toggle" id="moreToggle">Show Compact Panels (0)</button>
  <div class="dashboard-grid" id="moreGrid" style="margin-top:12px;"></div>
</div>
<div id="recent-activity" style="margin-top:20px; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);">
  <div style="padding:10px 16px; font-size:12px; color:var(--text2); border-bottom:1px solid var(--border); font-weight:600;">RECENT ACTIVITY</div>
  <div id="activityLog" style="max-height:120px; overflow-y:auto;"></div>
</div>
<script>
(function() {
  'use strict';
  var STORAGE_KEY = 'adaptive-dashboard-v1';
  var SCORE_KEY = 'adaptive-dashboard-scores';
  var ACTIVITY_KEY = 'adaptive-dashboard-activity';
  var DECAY_DAYS = 7;
  var AUTO_ARRANGE_INTERVAL = 30000;
  var panelData = [
    { id: 'revenue', title: 'Revenue', icon: '💰', color: '#6c5ce7', type: 'metric', metric: '$284,520', label: 'monthly recurring', change: '+12.4%', changeDir: 'up', chart: true },
    { id: 'users', title: 'User Growth', icon: '📈', color: '#00cec9', type: 'chart', metric: '14,892', label: 'total users', change: '+8.2%', changeDir: 'up', chart: true },
    { id: 'conversion', title: 'Conversion Rate', icon: '🎯', color: '#fd79a8', type: 'metric', metric: '3.42%', label: 'avg across funnels', change: '-0.18%', changeDir: 'down', chart: false },
    { id: 'sessions', title: 'Active Sessions', icon: '👤', color: '#fdcb6e', type: 'counter', metric: '247', label: 'right now', change: '+23 vs last hour', changeDir: 'up', chart: false },
    { id: 'pages', title: 'Top Pages', icon: '📄', color: '#e17055', type: 'list', items: ['/dashboard', '/pricing', '/docs', '/blog/analytics', '/settings'], counts: [1240, 876, 543, 321, 198] },
    { id: 'errors', title: 'Recent Errors', icon: '⚠️', color: '#d63031', type: 'errors', items: ['DB timeout /api/v2/users', 'Rate limit /checkout', 'Cache miss pipeline'], counts: ['2m ago', '12m ago', '47m ago'] },
    { id: 'health', title: 'System Health', icon: '🔵', color: '#00b894', type: 'status', items: ['API Latency', 'DB Connections', 'Cache Hit Rate', 'Queue Depth'], statuses: ['green','green','yellow','green'], values: ['24ms', '32/100', '87%', '3'] },
    { id: 'traffic', title: 'Traffic Sources', icon: '🌐', color: '#a29bfe', type: 'compact-chart', metric: 'Organic 42%', label: 'top source', chart: true }
  ];
  var defaultLayout = {};
  panelData.forEach(function(p, i) {
    defaultLayout[p.id] = { order: i, locked: false, collapsed: false, compact: false, gridCol: null, gridRow: null };
  });
  var usageData = loadUsageData();
  var layoutState = loadLayoutState();
  var activityLog = loadActivity();
  var autoArrangeOn = true;
  var dragSrcId = null;
  var dragOverId = null;
  var interactionCount = 0;
  var viewStartTimes = {};
  var autoTimer = null;
  var nextId = panelData.length + 1;
  function loadUsageData() {
    try {
      var raw = localStorage.getItem(SCORE_KEY);
      if (raw) {
        var data = JSON.parse(raw);
        if (data && typeof data === 'object') return data;
      }
    } catch(e) {}
    var init = {};
    panelData.forEach(function(p) {
      init[p.id] = { viewDuration: 0, interactionCount: 0, lastAccess: null, expandCount: 0, collapseCount: 0, viewSessions: 0 };
    });
    return init;
  }
  function loadLayoutState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var data = JSON.parse(raw);
        if (data && typeof data === 'object') {
          panelData.forEach(function(p) {
            if (data[p.id] === undefined) data[p.id] = JSON.parse(JSON.stringify(defaultLayout[p.id]));
          });
          return data;
        }
      }
    } catch(e) {}
    return JSON.parse(JSON.stringify(defaultLayout));
  }
  function loadActivity() {
    try {
      var raw = localStorage.getItem(ACTIVITY_KEY);
      if (raw) {
        var data = JSON.parse(raw);
        if (Array.isArray(data)) return data.slice(0, 100);
      }
    } catch(e) {}
    return [];
  }
  function saveUsageData() {
    try { localStorage.setItem(SCORE_KEY, JSON.stringify(usageData)); } catch(e) {}
  }
  function saveLayoutState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(layoutState)); } catch(e) {}
  }
  function saveActivity() {
    try { localStorage.setItem(ACTIVITY_KEY, JSON.stringify(activityLog.slice(0, 200))); } catch(e) {}
  }
  function logActivity(text) {
    var time = new Date();
    var timeStr = time.getHours().toString().padStart(2,'0') + ':' + time.getMinutes().toString().padStart(2,'0');
    var entry = { text: text, time: timeStr, ts: time.getTime() };
    activityLog.unshift(entry);
    if (activityLog.length > 50) activityLog.length = 50;
    saveActivity();
    renderActivity();
  }
  function renderActivity() {
    var el = document.getElementById('activityLog');
    if (!el) return;
    if (activityLog.length === 0) {
      el.innerHTML = '<div class="empty-state">No activity yet. Interact with panels to track usage.</div>';
      return;
    }
    el.innerHTML = activityLog.map(function(a) {
      return '<div class="activity-item"><span>' + a.text + '</span><span class="time">' + a.time + '</span></div>';
    }).join('');
  }
  function trackInteraction(panelId) {
    if (!usageData[panelId]) return;
    usageData[panelId].interactionCount++;
    interactionCount++;
    saveUsageData();
    updateStatsBar();
  }
  function trackViewStart(panelId) {
    if (!usageData[panelId]) return;
    viewStartTimes[panelId] = Date.now();
    usageData[panelId].viewSessions = (usageData[panelId].viewSessions || 0) + 1;
  }
  function trackViewEnd(panelId) {
    if (!viewStartTimes[panelId] || !usageData[panelId]) return;
    var duration = (Date.now() - viewStartTimes[panelId]) / 1000;
    usageData[panelId].viewDuration += duration;
    usageData[panelId].lastAccess = Date.now();
    delete viewStartTimes[panelId];
    saveUsageData();
  }
  function computeScore(panelId) {
    var u = usageData[panelId];
    if (!u) return 0;
    var freq = Math.log2((u.interactionCount || 0) + 1);
    var dur = Math.sqrt(u.viewDuration || 0);
    var daysSinceAccess = u.lastAccess ? (Date.now() - u.lastAccess) / (86400000) : 999;
    var recency = Math.exp(-daysSinceAccess / DECAY_DAYS);
    var viewSessionsBonus = Math.log2((u.viewSessions || 0) + 1) * 0.5;
    return freq * dur * recency + viewSessionsBonus;
  }
  function computeAllScores() {
    var scores = {};
    panelData.forEach(function(p) {
      scores[p.id] = computeScore(p.id);
    });
    return scores;
  }
  function getRankedPanels() {
    var scores = computeAllScores();
    var entries = panelData.map(function(p) {
      return { id: p.id, data: p, score: scores[p.id] };
    });
    entries.sort(function(a, b) { return b.score - a.score; });
    entries.forEach(function(e, i) { e.rank = i + 1; });
    return entries;
  }
  function assignLayoutPositions() {
    if (!autoArrangeOn) return;
    var ranked = getRankedPanels();
    var locked = [];
    var unlocked = [];
    ranked.forEach(function(r) {
      if (layoutState[r.id] && layoutState[r.id].locked) {
        locked.push(r);
      } else {
        unlocked.push(r);
      }
    });
    var order = locked.concat(unlocked);
    var cols = [1,2,3,4];
    var row = 1;
    var colIdx = 0;
    order.forEach(function(entry, index) {
      var l = layoutState[entry.id];
      if (!l) return;
      if (l.locked) {
        l.compact = (entry.rank > 4);
        return;
      }
      if (index === 0) {
        l.gridCol = '1 / 3';
        l.gridRow = row + ' / ' + (row + 2);
        l.compact = false;
        colIdx = 2;
      } else if (index === 1) {
        if (colIdx < 2) {
          l.gridCol = '3 / 5';
          l.gridRow = row + ' / ' + (row + 2);
          colIdx = 4;
        } else {
          l.gridCol = '3 / 5';
          l.gridRow = row + ' / ' + (row + 2);
          row += 2;
          colIdx = 4;
        }
        l.compact = false;
      } else if (index === 2) {
        if (colIdx >= 4) { row += 1; colIdx = 0; }
        l.gridCol = (colIdx + 1) + ' / ' + (colIdx + 3);
        l.gridRow = row + ' / ' + (row + 1);
        colIdx += 2;
        l.compact = false;
      } else if (index === 3) {
        if (colIdx >= 4) { row += 1; colIdx = 0; }
        l.gridCol = (colIdx + 1) + ' / ' + (colIdx + 3);
        l.gridRow = row + ' / ' + (row + 1);
        colIdx += 2;
        l.compact = false;
      } else if (index >= 4 && index < 6) {
        if (colIdx >= 4) { row += 1; colIdx = 0; }
        l.gridCol = (colIdx + 1) + ' / ' + (colIdx + 2);
        l.gridRow = row + ' / ' + (row + 1);
        colIdx += 1;
        l.compact = false;
      } else {
        l.compact = true;
        l.gridCol = null;
        l.gridRow = null;
      }
    });
    saveLayoutState();
  }
  function renderPanel(entry, rank) {
    var p = entry.data;
    var ls = layoutState[p.id] || {};
    var isCompact = ls.compact && !ls.collapsed;
    var panelEl = document.createElement('div');
    panelEl.className = 'panel';
    panelEl.id = 'panel-' + p.id;
    panelEl.draggable = false;
    if (ls.locked) panelEl.classList.add('locked');
    if (ls.collapsed) panelEl.classList.add('collapsed');
    if (isCompact) panelEl.classList.add('compact');
    if (ls.gridCol && ls.gridCol !== 'null') {
      panelEl.style.gridColumn = ls.gridCol;
    }
    if (ls.gridRow && ls.gridRow !== 'null') {
      panelEl.style.gridRow = ls.gridRow;
    }
    var header = document.createElement('div');
    header.className = 'panel-header';
    header.setAttribute('draggable', 'true');
    header.dataset.panelId = p.id;
    var title = document.createElement('div');
    title.className = 'panel-title';
    title.innerHTML = '<span class="icon" style="background:' + p.color + '20;color:' + p.color + '">' + p.icon + '</span>' + p.title;
    header.appendChild(title);
    var rankBadge = document.createElement('span');
    rankBadge.className = 'rank-badge';
    rankBadge.textContent = '#' + rank;
    header.appendChild(rankBadge);
    var actions = document.createElement('div');
    actions.className = 'panel-actions';
    var lockBtn = document.createElement('button');
    lockBtn.textContent = ls.locked ? '\u{1F512}' : '\u{1F513}';
    lockBtn.title = ls.locked ? 'Unlock' : 'Lock position';
    if (ls.locked) lockBtn.classList.add('locked');
    lockBtn.addEventListener('click', function(e) { e.stopPropagation(); toggleLock(p.id); });
    var collapseBtn = document.createElement('button');
    collapseBtn.textContent = ls.collapsed ? '\u25BC' : '\u25B2';
    collapseBtn.title = ls.collapsed ? 'Expand' : 'Collapse';
    collapseBtn.addEventListener('click', function(e) { e.stopPropagation(); toggleCollapse(p.id); });
    actions.appendChild(lockBtn);
    actions.appendChild(collapseBtn);
    header.appendChild(actions);
    panelEl.appendChild(header);
    var body = document.createElement('div');
    body.className = 'panel-body';
    body.dataset.panelId = p.id;
    if (isCompact) {
      renderCompactBody(body, p);
    } else {
      renderFullBody(body, p);
    }
    panelEl.appendChild(body);
    panelEl.addEventListener('mouseenter', function() { trackViewStart(p.id); });
    panelEl.addEventListener('mouseleave', function() { trackViewEnd(p.id); });
    header.addEventListener('dragstart', onDragStart);
    header.addEventListener('dragend', onDragEnd);
    panelEl.addEventListener('dragover', onDragOver);
    panelEl.addEventListener('dragleave', onDragLeave);
    panelEl.addEventListener('drop', onDrop);
    body.addEventListener('click', function() {
      trackInteraction(p.id);
    });
    return panelEl;
  }
  function renderFullBody(body, p) {
    if (p.type === 'metric' || p.type === 'chart') {
      body.innerHTML = '<div class="metric-value">' + p.metric + '</div><div class="metric-label">' + p.label + '</div>';
      if (p.change) {
        body.innerHTML += '<div class="metric-change ' + p.changeDir + '">' + (p.changeDir === 'up' ? '\u25B2 ' : '\u25BC ') + p.change + '</div>';
      }
      if (p.chart) {
        body.innerHTML += '<div class="chart-area">' + generateBars() + '</div>';
      }
    } else if (p.type === 'counter') {
      body.innerHTML = '<div class="metric-value pulse" style="color:' + p.color + '">' + p.metric + '</div><div class="metric-label">' + p.label + '</div>';
      if (p.change) {
        body.innerHTML += '<div class="metric-change ' + p.changeDir + '">' + p.change + '</div>';
      }
    } else if (p.type === 'list' && p.items) {
      body.innerHTML = p.items.map(function(item, i) {
        return '<div class="list-item"><span>' + item + '</span><span class="count">' + (p.counts[i] || '') + '</span></div>';
      }).join('');
    } else if (p.type === 'errors' && p.items) {
      body.innerHTML = p.items.map(function(item, i) {
        return '<div class="list-item" style="color:' + p.color + '"><span>' + item + '</span><span class="count">' + (p.counts[i] || '') + '</span></div>';
      }).join('');
    } else if (p.type === 'status' && p.items) {
      body.innerHTML = p.items.map(function(item, i) {
        var dotClass = p.statuses[i] || 'green';
        var val = p.values[i] || '';
        return '<div class="status-row"><span><span class="status-dot ' + dotClass + '"></span>' + item + '</span><span>' + val + '</span></div>';
      }).join('');
    } else if (p.type === 'compact-chart') {
      body.innerHTML = '<div class="metric-value" style="font-size:20px;">' + p.metric + '</div><div class="metric-label">' + p.label + '</div>';
      body.innerHTML += '<div class="mini-chart"><div class="fill" style="width:42%"></div></div>';
    } else {
      body.innerHTML = '<div class="empty-state">Panel content</div>';
    }
  }
  function renderCompactBody(body, p) {
    body.innerHTML = '<div class="compact-preview">';
    if (p.metric) {
      body.innerHTML += '<span class="mini-metric" style="color:' + p.color + '">' + p.metric + '</span><span class="mini-label">' + (p.label || p.title) + '</span>';
    } else if (p.items) {
      body.innerHTML += '<span class="mini-label">' + p.items[0] + '</span><span class="mini-label">+' + (p.items.length - 1) + ' more</span>';
    } else {
      body.innerHTML += '<span class="mini-label">' + p.title + '</span>';
    }
    body.innerHTML += '</div>';
  }
  function generateBars() {
    var bars = '';
    for (var i = 0; i < 7; i++) {
      var h = 20 + Math.random() * 80;
      bars += '<div class="bar" style="left:' + (i * 14 + 2) + '%;height:' + h + '%;"></div>';
    }
    return bars;
  }
  function renderDashboard() {
    var container = document.getElementById('dashboard');
    var moreSection = document.getElementById('moreSection');
    var moreGrid = document.getElementById('moreGrid');
    assignLayoutPositions();
    var ranked = getRankedPanels();
    var mainPanels = [];
    var compactPanels = [];
    ranked.forEach(function(entry) {
      var ls = layoutState[entry.id];
      if (ls && ls.compact && !ls.locked) {
        compactPanels.push(entry);
      } else {
        mainPanels.push(entry);
      }
    });
    container.innerHTML = '';
    mainPanels.forEach(function(entry) {
      container.appendChild(renderPanel(entry, entry.rank));
    });
    if (compactPanels.length > 0) {
      moreSection.classList.add('visible');
      moreGrid.innerHTML = '';
      compactPanels.forEach(function(entry) {
        moreGrid.appendChild(renderPanel(entry, entry.rank));
      });
      document.getElementById('moreToggle').textContent = 'Show Compact Panels (' + compactPanels.length + ')';
      var hidden = true;
      moreGrid.style.display = 'none';
      document.getElementById('moreToggle').onclick = function() {
        hidden = !hidden;
        moreGrid.style.display = hidden ? 'none' : 'grid';
        this.textContent = hidden ? 'Show Compact Panels (' + compactPanels.length + ')' : 'Hide Compact Panels';
      };
    } else {
      moreSection.classList.remove('visible');
    }
    updateStatsBar();
    setupIntersectionObserver();
  }
  function setupIntersectionObserver() {
    if (window._panelObserver) window._panelObserver.disconnect();
    var panels = document.querySelectorAll('.panel');
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        var panelEl = e.target;
        var body = panelEl.querySelector('.panel-body');
        if (!body) return;
        var id = body.dataset.panelId;
        if (!id) return;
        if (e.isIntersecting) {
          trackViewStart(id);
        } else {
          trackViewEnd(id);
        }
      });
    }, { threshold: 0.3 });
    panels.forEach(function(p) { observer.observe(p); });
    window._panelObserver = observer;
  }
  function updateStatsBar() {
    var total = panelData.length;
    var locked = 0;
    var compact = 0;
    panelData.forEach(function(p) {
      var ls = layoutState[p.id];
      if (ls) {
        if (ls.locked) locked++;
        if (ls.compact) compact++;
      }
    });
    var scores = computeAllScores();
    var topId = null;
    var topScore = -1;
    panelData.forEach(function(p) {
      if (scores[p.id] > topScore) {
        topScore = scores[p.id];
        topId = p.id;
      }
    });
    var topPanel = document.getElementById('topPanel');
    if (topPanel) topPanel.textContent = topId ? panelData.find(function(p) { return p.id === topId; }).title : '-';
    var elTotal = document.getElementById('totalPanels');
    if (elTotal) elTotal.textContent = total;
    var elLocked = document.getElementById('lockedCount');
    if (elLocked) elLocked.textContent = locked;
    var elCompact = document.getElementById('compactCount');
    if (elCompact) elCompact.textContent = compact;
    var elInter = document.getElementById('totalInteractions');
    if (elInter) elInter.textContent = interactionCount;
  }
  function toggleLock(panelId) {
    var ls = layoutState[panelId];
    if (!ls) return;
    ls.locked = !ls.locked;
    saveLayoutState();
    logActivity((ls.locked ? 'Locked' : 'Unlocked') + ' panel: ' + (panelData.find(function(p) { return p.id === panelId; }) || {}).title);
    trackInteraction(panelId);
    renderDashboard();
  }
  function toggleCollapse(panelId) {
    var ls = layoutState[panelId];
    if (!ls) return;
    if (ls.collapsed) {
      ls.collapsed = false;
      if (usageData[panelId]) usageData[panelId].expandCount++;
      logActivity('Expanded panel: ' + (panelData.find(function(p) { return p.id === panelId; }) || {}).title);
    } else {
      ls.collapsed = true;
      if (usageData[panelId]) usageData[panelId].collapseCount++;
      logActivity('Collapsed panel: ' + (panelData.find(function(p) { return p.id === panelId; }) || {}).title);
    }
    saveLayoutState();
    trackInteraction(panelId);
    renderDashboard();
  }
  function onDragStart(e) {
    var header = e.target.closest('.panel-header');
    if (!header) return;
    var id = header.dataset.panelId;
    if (!id) return;
    dragSrcId = id;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', id);
    var panel = document.getElementById('panel-' + id);
    if (panel) panel.classList.add('dragging');
  }
  function onDragEnd(e) {
    var panels = document.querySelectorAll('.panel');
    panels.forEach(function(p) { p.classList.remove('dragging', 'drag-over'); });
    dragSrcId = null;
    dragOverId = null;
  }
  function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    var panel = e.target.closest('.panel');
    if (!panel) return;
    var id = panel.id.replace('panel-', '');
    if (id === dragSrcId) return;
    dragOverId = id;
    document.querySelectorAll('.panel').forEach(function(p) { p.classList.remove('drag-over'); });
    panel.classList.add('drag-over');
  }
  function onDragLeave(e) {
    var panel = e.target.closest('.panel');
    if (panel) panel.classList.remove('drag-over');
  }
  function onDrop(e) {
    e.preventDefault();
    document.querySelectorAll('.panel').forEach(function(p) { p.classList.remove('drag-over', 'dragging'); });
    var srcId = dragSrcId || e.dataTransfer.getData('text/plain');
    var targetPanel = e.target.closest('.panel');
    if (!targetPanel || !srcId) return;
    var targetId = targetPanel.id.replace('panel-', '');
    if (srcId === targetId) return;
    var srcLayout = layoutState[srcId];
    var tgtLayout = layoutState[targetId];
    if (!srcLayout || !tgtLayout) return;
    var srcOrder = srcLayout.gridCol + '|' + srcLayout.gridRow;
    var tgtOrder = tgtLayout.gridCol + '|' + tgtLayout.gridRow;
    srcLayout.gridCol = tgtLayout.gridCol;
    srcLayout.gridRow = tgtLayout.gridRow;
    tgtLayout.gridCol = srcOrder.split('|')[0];
    tgtLayout.gridRow = srcOrder.split('|')[1];
    srcLayout.locked = true;
    logActivity('Moved panel via drag-drop');
    saveLayoutState();
    renderDashboard();
  }
  function resetLayout() {
    panelData.forEach(function(p) {
      layoutState[p.id] = JSON.parse(JSON.stringify(defaultLayout[p.id]));
    });
    saveLayoutState();
    logActivity('Layout reset to defaults');
    renderDashboard();
  }
  function clearTrackingData() {
    var init = {};
    panelData.forEach(function(p) {
      init[p.id] = { viewDuration: 0, interactionCount: 0, lastAccess: null, expandCount: 0, collapseCount: 0, viewSessions: 0 };
    });
    usageData = init;
    interactionCount = 0;
    saveUsageData();
    logActivity('Usage tracking data cleared');
    renderDashboard();
  }
  function toggleAutoArrange() {
    autoArrangeOn = !autoArrangeOn;
    var btn = document.getElementById('btnAutoArrange');
    if (btn) {
      btn.textContent = autoArrangeOn ? 'Auto-Arrange ON' : 'Auto-Arrange OFF';
      btn.classList.toggle('active', autoArrangeOn);
    }
    if (autoArrangeOn) {
      logActivity('Auto-arrange enabled');
      assignLayoutPositions();
      renderDashboard();
    } else {
      logActivity('Auto-arrange disabled — layout frozen');
    }
  }
  function autoArrangeTick() {
    if (!autoArrangeOn) return;
    assignLayoutPositions();
    renderDashboard();
  }
  function init() {
    renderDashboard();
    renderActivity();
    document.getElementById('btnAutoArrange').addEventListener('click', toggleAutoArrange);
    document.getElementById('btnResetLayout').addEventListener('click', resetLayout);
    document.getElementById('btnClearData').addEventListener('click', clearTrackingData);
    autoTimer = setInterval(autoArrangeTick, AUTO_ARRANGE_INTERVAL);
    logActivity('Dashboard initialized — tracking active');
  }
  document.addEventListener('DOMContentLoaded', init);
  if (document.readyState !== 'loading') init();
})();
</script>
</body>
</html>