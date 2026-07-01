Byter direkt i svaret — en själv-laddande, interaktiv timeline som läser state.yaml från disk, ingen upload behövs.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline v7</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden}
.header{padding:20px 30px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.header h1{font-size:22px;font-weight:600;color:#f0f6fc}
.header .stats{display:flex;gap:16px;font-size:13px;color:#8b949e;flex-wrap:wrap}
.header .stats span strong{color:#e6edf3}
.load-status{font-size:12px;color:#8b949e;margin-left:auto;font-family:monospace}
.load-status.ok{color:#3fb950}
.load-status.err{color:#f85149}
.verify-banner{margin:10px 30px;padding:12px 18px;background:#1c2128;border:1px solid #30363d;border-radius:8px;font-size:12px;color:#e6edf3;display:none;font-family:monospace;line-height:1.7}
.verify-banner .ok{color:#3fb950}
.verify-banner .warn{color:#d29922}
.verify-banner .fail{color:#f85149}
.verify-banner .info{color:#58a6ff}
.promotion-bar{display:none;padding:0 30px 10px;gap:16px;flex-wrap:wrap}
.promotion-stat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:8px 14px;min-width:80px;flex:1;text-align:center}
.promotion-stat .val{font-size:20px;font-weight:700;color:#f0f6fc}
.promotion-stat .label{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.promotion-stat .val.gold{color:#d29922}
.promotion-stat .val.green{color:#3fb950}
.promotion-stat .val.blue{color:#58a6ff}
.promotion-stat .val.red{color:#f85149}
.controls{display:none;align-items:center;gap:10px;padding:10px 30px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}
.controls label{font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.controls .time-slider-wrap{display:flex;align-items:center;gap:8px;flex:2;min-width:200px}
.controls .time-slider-wrap input[type=range]{flex:1;height:4px;accent-color:#d29922;cursor:pointer}
.controls .time-display{font-size:12px;color:#e6edf3;font-family:monospace;min-width:155px;white-space:nowrap}
.controls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:500;transition:all .15s}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.controls select{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px}
.controls input[type=text]{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px;width:130px}
.controls .score-range{display:flex;align-items:center;gap:4px}
.controls .score-range input[type=range]{width:70px;height:4px;accent-color:#d29922;cursor:pointer}
.controls .score-range .val{font-size:11px;color:#e6edf3;font-family:monospace;min-width:20px;text-align:center}
.filter-count{font-size:11px;color:#8b949e;padding:0 4px;white-space:nowrap}
.legend{display:none;gap:16px;padding:8px 30px;font-size:11px;color:#8b949e;border-bottom:1px solid #21262d;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px}
.legend-dot{width:10px;height:10px;border-radius:50%;border:1px solid rgba(255,255,255,.15)}
.timeline-wrap{overflow:auto;max-height:calc(100vh - 220px);position:relative}
.timeline-svg{display:block;min-width:100%}
.loading-spinner{padding:60px;text-align:center;color:#8b949e;font-size:14px}
.loading-spinner .spinner{display:inline-block;width:24px;height:24px;border:3px solid #30363d;border-top-color:#58a6ff;border-radius:50%;animation:spin .8s linear infinite;margin-bottom:10px}
@keyframes spin{to{transform:rotate(360deg)}}
.empty-state{padding:60px;text-align:center;color:#8b949e;font-size:14px;display:none}
.tooltip{position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px 20px;z-index:1000;max-width:420px;box-shadow:0 8px 32px rgba(0,0,0,.6);pointer-events:none;display:none;font-size:12px}
.tooltip h3{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:8px}
.tooltip .row{display:flex;justify-content:space-between;gap:16px;padding:3px 0;border-bottom:1px solid #21262d}
.tooltip .row:last-child{border-bottom:none}
.tooltip .label{color:#8b949e}
.tooltip .value{color:#e6edf3;font-family:monospace;text-align:right}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge-production{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3)}
.badge-archive{background:rgba(139,148,158,.15);color:#8b949e;border:1px solid rgba(139,148,158,.3)}
.badge-refinery{background:rgba(88,166,255,.15);color:#58a6ff;border:1px solid rgba(88,166,255,.3)}
.note{font-size:10px;color:#8b949e;padding:6px 30px;border-bottom:1px solid #21262d;display:none}
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <div class="stats">
    <span>Blueprints: <strong id="bp-count">0</strong></span>
    <span>Runs: <strong id="run-count">0</strong></span>
    <span>Production: <strong id="prod-count">0</strong></span>
    <span>Scored: <strong id="scored-count">0</strong></span>
    <span>Span: <strong id="time-span">...</strong></span>
  </div>
  <span class="load-status" id="load-status">Loading...</span>
</div>
<div class="verify-banner" id="verify-banner"></div>
<div class="promotion-bar" id="promotion-bar">
  <div class="promotion-stat"><div class="val gold" id="stat-promotable">--</div><div class="label">Promotable >=85x3</div></div>
  <div class="promotion-stat"><div class="val blue" id="stat-avg">--</div><div class="label">Avg Score</div></div>
  <div class="promotion-stat"><div class="val green" id="stat-production">--</div><div class="label">In Production</div></div>
  <div class="promotion-stat"><div class="val" id="stat-refinery">--</div><div class="label">In Refinery</div></div>
  <div class="promotion-stat"><div class="val red" id="stat-archive">--</div><div class="label">Archived</div></div>
  <div class="promotion-stat"><div class="val" id="stat-total">--</div><div class="label">Total Agents</div></div>
</div>
<div class="controls" id="controls">
  <div class="time-slider-wrap">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="100" value="100" step="1">
    <span class="time-display" id="time-display">All time</span>
  </div>
  <button id="play-btn">Play</button>
  <button id="reset-btn">Reset</button>
  <select id="speed-select">
    <option value="50">0.5x</option>
    <option value="100" selected>1x</option>
    <option value="200">2x</option>
    <option value="400">4x</option>
  </select>
  <label>Stage</label>
  <select id="stage-filter">
    <option value="all">All</option>
    <option value="production">Production</option>
    <option value="refinery">Refinery</option>
    <option value="archive">Archive</option>
  </select>
  <label>Search</label>
  <input type="text" id="search-input" placeholder="Blueprint...">
  <div class="score-range">
    <span class="val" id="score-min-label">0</span>
    <input type="range" id="score-min-slider" min="0" max="100" value="0" step="1">
    <span class="val" id="score-max-label">100</span>
    <input type="range" id="score-max-slider" min="0" max="100" value="100" step="1">
  </div>
  <span class="filter-count" id="filter-count"></span>
</div>
<div class="legend" id="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#d29922"></div> Score 85+</div>
  <div class="legend-item"><div class="legend-dot" style="background:#db6d28"></div> Score 70-84</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f85149"></div> Below 70</div>
  <div class="legend-item"><div class="legend-dot" style="background:#58a6ff"></div> Spawn/Improve</div>
  <div class="legend-item"><div class="legend-dot" style="background:#3fb950"></div> Production</div>
  <div class="legend-item"><div class="legend-dot" style="background:#8b949e"></div> Archive</div>
</div>
<div class="note" id="auto-note">Auto-loaded state.yaml from forge directory</div>
<div class="timeline-wrap" id="timeline-wrap">
  <div class="loading-spinner" id="loading-state">
    <div class="spinner"></div>
    <div>Loading state.yaml...</div>
  </div>
  <div class="empty-state" id="empty-state">No data loaded</div>
  <svg class="timeline-svg" id="timeline-svg"></svg>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
var DATA = null;
var blueprints = [];
var bpRuns = {};
var bpStages = {};
var bpAgents = {};
var tMin = null;
var tMax = null;
var tRange = 1;
var ROW_H = 26;
var NODE_R = 5;
var SVG_W = 1200;
var plotL = 130;
var plotR = 1080;
var loadingDone = false;
// ----- Auto-load from disk -----
function autoLoad() {
  var status = document.getElementById('load-status');
  status.textContent = 'Fetching state.yaml...';
  fetch('state.yaml').then(function(r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.text();
  }).then(function(text) {
    try {
      var parsed = jsyaml.load(text);
      if (!parsed || typeof parsed !== 'object') throw new Error('Invalid YAML');
      status.textContent = 'state.yaml loaded (' + (parsed.activity ? parsed.activity.length : 0) + ' events)';
      status.className = 'load-status ok';
      processData(parsed);
    } catch(e) {
      throw new Error('Parse error: ' + e.message);
    }
  }).catch(function(err) {
    status.textContent = 'state.yaml not found, trying _timeline_data.json...';
    status.className = 'load-status';
    fetch('_timeline_data.json').then(function(r2) {
      if (!r2.ok) throw new Error('HTTP ' + r2.status);
      return r2.json();
    }).then(function(data) {
      if (!Array.isArray(data)) throw new Error('Not an array');
      status.textContent = '_timeline_data.json loaded (' + data.length + ' events)';
      status.className = 'load-status ok';
      processFromJson(data);
    }).catch(function(err2) {
      status.textContent = 'No data files found - upload state.yaml or place files in directory';
      status.className = 'load-status err';
      document.getElementById('loading-state').innerHTML =
        '<div style="color:#f85149;font-size:16px;margin-bottom:8px">Data source not found</div>' +
        '<div style="font-size:12px">Place state.yaml or _timeline_data.json alongside this HTML file,<br>' +
        'or use the file upload below.</div>' +
        '<div style="margin-top:20px"><input type="file" id="fallback-file" accept=".yaml,.yml,.json" style="display:none">' +
        '<button onclick="document.getElementById(\'fallback-file\').click()" style="background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:8px 20px;border-radius:6px;cursor:pointer;font-size:13px">Upload state.yaml</button></div>';
      document.getElementById('fallback-file').addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
          var reader = new FileReader();
          reader.onload = function(evt) {
            try {
              var p = jsyaml.load(evt.target.result);
              if (p && p.activity) { processData(p); return; }
              var arr = JSON.parse(evt.target.result);
              if (Array.isArray(arr)) { processFromJson(arr); return; }
              throw new Error('Unknown format');
            } catch(e) { status.textContent = 'Upload parse failed: ' + e.message; }
          };
          reader.readAsText(e.target.files[0]);
        }
      });
    });
  });
}
// ----- Process from JSON array -----
function processFromJson(activityArr) {
  var wrapped = { activity: activityArr, agents: [] };
  processData(wrapped);
}
// ----- Process state.yaml structure -----
function processData(parsed) {
  var activity = parsed.activity || [];
  var agents = parsed.agents || [];
  loadingDone = true;
  document.getElementById('loading-state').style.display = 'none';
  document.getElementById('auto-note').style.display = 'block';
  var agentStageMap = {};
  var agentScoreMap = {};
  var agentBenchmarkMap = {};
  agents.forEach(function(a) {
    var bp = a.blueprint;
    if (!bp) return;
    var stage = a.stage || 'refinery';
    var rid = a.run_id || '';
    if (!agentStageMap[bp]) agentStageMap[bp] = {};
    if (rid) agentStageMap[bp][rid] = stage;
    if (!bpAgents[bp]) bpAgents[bp] = [];
    bpAgents[bp].push(a);
    if (a.benchmark) agentBenchmarkMap[bp] = a.benchmark;
  });
  blueprints = [];
  bpRuns = {};
  activity.forEach(function(ev) {
    var bp = ev.blueprint;
    if (!bp) return;
    var ts = ev.timestamp || '';
    var action = ev.action || '';
    var detail = ev.detail || '';
    var id = ev.id || 0;
    var status = ev.status || '';
    var progress = ev.progress !== undefined ? ev.progress : 0;
    var score = null, selfScore = null, judgeScore = null;
    var scoreMatch = detail.match(/C:([0-9.]+)/);
    if (scoreMatch) score = parseFloat(scoreMatch[1]);
    var selfMatch = detail.match(/S:([0-9.]+)/);
    if (selfMatch) selfScore = parseFloat(selfMatch[1]);
    var judgeMatch = detail.match(/J:([0-9.]+)/);
    if (judgeMatch) judgeScore = parseFloat(judgeMatch[1]);
    if (!bpRuns[bp]) { bpRuns[bp] = []; blueprints.push(bp); }
    bpRuns[bp].push({
      blueprint: bp, ts: ts, action: action, detail: detail, id: id,
      status: status, progress: progress,
      run_id: ts ? ts.replace(/[^0-9]/g,'').slice(0,14) : String(id),
      score: score, selfScore: selfScore, judgeScore: judgeScore,
      benchmark: agentBenchmarkMap[bp] || null
    });
  });
  blueprints.sort();
  blueprints.forEach(function(bp) {
    bpRuns[bp].sort(function(a,b) { return (a.ts||'').localeCompare(b.ts||''); });
    var hasProduction = false, hasRefinery = false, hasArchive = false;
    if (agentStageMap[bp]) {
      Object.values(agentStageMap[bp]).forEach(function(s) {
        if (s === 'production') hasProduction = true;
        else if (s === 'archive') hasArchive = true;
        else hasRefinery = true;
      });
    }
    bpRuns[bp].forEach(function(r) {
      if (r.action === 'promote') hasProduction = true;
    });
    if (hasProduction) bpStages[bp] = 'production';
    else if (hasArchive) bpStages[bp] = 'archive';
    else bpStages[bp] = 'refinery';
  });
  var allTimes = [];
  blueprints.forEach(function(bp) {
    bpRuns[bp].forEach(function(r) { if (r.ts) allTimes.push(new Date(r.ts)); });
  });
  allTimes = allTimes.filter(function(t) { return t && !isNaN(t.getTime()); });
  allTimes.sort(function(a,b) { return a - b; });
  if (allTimes.length === 0) {
    showVerify('fail', 'No timestamped events found. Activity array may be empty.');
    return;
  }
  tMin = allTimes[0];
  tMax = allTimes[allTimes.length - 1];
  tRange = tMax.getTime() - tMin.getTime() || 1;
  DATA = [];
  blueprints.forEach(function(bp) { bpRuns[bp].forEach(function(r) { DATA.push(r); }); });
  var scoredCount = DATA.filter(function(d) { return d.score !== null; }).length;
  var scoreValues = DATA.map(function(d) { return d.score; }).filter(function(s) { return s !== null; });
  var scoreMin = scoreValues.length > 0 ? Math.min.apply(null, scoreValues) : null;
  var scoreMaxV = scoreValues.length > 0 ? Math.max.apply(null, scoreValues) : null;
  var avgScore = scoreValues.length > 0 ? (scoreValues.reduce(function(a,b) { return a+b; }, 0) / scoreValues.length) : null;
  var prodCount = Object.values(bpStages).filter(function(s) { return s === 'production'; }).length;
  var refCount = Object.values(bpStages).filter(function(s) { return s === 'refinery'; }).length;
  var archCount = Object.values(bpStages).filter(function(s) { return s === 'archive'; }).length;
  var promotableCount = 0;
  var promotableList = [];
  blueprints.forEach(function(bp) {
    var runs = bpRuns[bp];
    var scores = runs.map(function(r) { return r.score; }).filter(function(s) { return s !== null; });
    if (scores.length >= 3) {
      var last3 = scores.slice(-3);
      if (last3.every(function(s) { return s >= 85; })) {
        promotableCount++;
        promotableList.push(bp);
      }
    }
  });
  var verifyHtml =
    '<span class="ok">SUMMARY: ' + blueprints.length + ' blueprints, ' + DATA.length + ' total runs, ' + scoredCount + ' scored</span><br>' +
    '<span class="info">Score range: ' + (scoreMin !== null ? scoreMin.toFixed(1) : 'N/A') + ' - ' + (scoreMaxV !== null ? scoreMaxV.toFixed(1) : 'N/A') +
    ' | Avg: ' + (avgScore !== null ? avgScore.toFixed(1) : 'N/A') + '</span><br>' +
    '<span class="info">Time span: ' + tMin.toISOString().slice(0,10) + ' to ' + tMax.toISOString().slice(0,10) +
    ' | Prod: ' + prodCount + ' | Ref: ' + refCount + ' | Arch: ' + archCount +
    ' | Promotable: ' + promotableCount + '</span>';
  if (promotableList.length > 0 && promotableList.length <= 10) {
    verifyHtml += '<br><span class="ok">Promotable: ' + promotableList.join(', ') + '</span>';
  }
  showVerify('ok', verifyHtml);
  document.getElementById('bp-count').textContent = blueprints.length;
  document.getElementById('run-count').textContent = DATA.length;
  document.getElementById('prod-count').textContent = prodCount;
  document.getElementById('scored-count').textContent = scoredCount;
  document.getElementById('time-span').textContent =
    tMin.toISOString().slice(0,10) + ' - ' + tMax.toISOString().slice(0,10);
  document.getElementById('stat-promotable').textContent = promotableCount;
  document.getElementById('stat-avg').textContent = avgScore !== null ? avgScore.toFixed(1) : '--';
  document.getElementById('stat-production').textContent = prodCount;
  document.getElementById('stat-refinery').textContent = refCount;
  document.getElementById('stat-archive').textContent = archCount;
  document.getElementById('stat-total').textContent = blueprints.length;
  document.getElementById('promotion-bar').style.display = 'flex';
  document.getElementById('controls').style.display = 'flex';
  document.getElementById('legend').style.display = 'flex';
  if (blueprints.length === 0) {
    document.getElementById('empty-state').textContent = 'No blueprints found';
    document.getElementById('empty-state').style.display = 'block';
    return;
  }
  formatTimeDisplay();
  render();
  bindEvents();
}
function showVerify(type, html) {
  var banner = document.getElementById('verify-banner');
  banner.innerHTML = html;
  banner.style.display = 'block';
}
// ----- Color Helpers -----
function scoreColor(score) {
  if (score === null) return '#58a6ff';
  if (score >= 85) return '#d29922';
  if (score >= 70) return '#db6d28';
  return '#f85149';
}
function nodeColor(ev) {
  if (ev.action === 'spawn' || ev.action === 'improve' || ev.action === 'promote') {
    return ['#58a6ff', '#1f6feb'];
  }
  if (ev.score !== null) {
    if (ev.score >= 85) return ['#d29922', '#b0881a'];
    if (ev.score >= 70) return ['#db6d28', '#b05a1a'];
    return ['#f85149', '#c83030'];
  }
  return ['#8b949e', '#6e7681'];
}
function tsToX(ts) {
  if (!ts) return plotL;
  var t = new Date(ts);
  if (isNaN(t.getTime())) return plotL;
  var pct = (t.getTime() - tMin.getTime()) / tRange;
  return plotL + pct * (plotR - plotL);
}
// ----- Filtering -----
function getFilteredBlueprints() {
  var stageFilter = document.getElementById('stage-filter').value;
  var search = document.getElementById('search-input').value.toLowerCase().trim();
  var scoreMin = parseInt(document.getElementById('score-min-slider').value);
  var scoreMax = parseInt(document.getElementById('score-max-slider').value);
  return blueprints.filter(function(bp) {
    if (search && bp.toLowerCase().indexOf(search) === -1) return false;
    if (stageFilter !== 'all') {
      if (bpStages[bp] !== stageFilter) return false;
    }
    if (scoreMin > 0 || scoreMax < 100) {
      var hasScoreInRange = bpRuns[bp].some(function(r) {
        return r.score !== null && r.score >= scoreMin && r.score <= scoreMax;
      });
      if (!hasScoreInRange) return false;
    }
    return true;
  });
}
// ----- Tooltip -----
function showTooltip(ev, cx, cy) {
  var tip = document.getElementById('tooltip');
  var stage = bpStages[ev.blueprint] || 'refinery';
  var stageBadge = 'badge-' + stage;
  var scoreHtml = '';
  if (ev.score !== null) {
    scoreHtml = '<div class="row"><span class="label">Composite (C)</span><span class="value" style="color:' + scoreColor(ev.score) + '">' + ev.score.toFixed(1) + '</span></div>';
    if (ev.selfScore !== null) scoreHtml += '<div class="row"><span class="label">Self (S)</span><span class="value">' + ev.selfScore.toFixed(1) + '</span></div>';
    if (ev.judgeScore !== null) scoreHtml += '<div class="row"><span class="label">Judge (J)</span><span class="value">' + ev.judgeScore.toFixed(1) + '</span></div>';
  }
  var detailDisplay = ev.detail && ev.detail.length > 80 ? ev.detail.slice(0, 78) + '...' : ev.detail;
  tip.innerHTML =
    '<h3>' + ev.blueprint + '</h3>' +
    '<div style="margin-bottom:6px"><span class="badge ' + stageBadge + '">' + stage + '</span>' +
    ' <span style="color:#8b949e;font-size:11px">' + ev.action + '</span></div>' +
    '<div class="row"><span class="label">Run ID</span><span class="value">' + (ev.run_id || ev.id || '--') + '</span></div>' +
    '<div class="row"><span class="label">Action</span><span class="value">' + (ev.action || '--') + '</span></div>' +
    scoreHtml +
    '<div class="row"><span class="label">Status</span><span class="value">' + (ev.status || '--') + '</span></div>' +
    '<div class="row"><span class="label">Progress</span><span class="value">' + (ev.progress || 0) + '%</span></div>' +
    (ev.benchmark ? '<div class="row"><span class="label">Benchmark</span><span class="value">' + ev.benchmark + '</span></div>' : '') +
    '<div class="row"><span class="label">Timestamp</span><span class="value">' + (ev.ts || '--') + '</span></div>' +
    (detailDisplay ? '<div style="margin-top:6px;padding-top:6px;border-top:1px solid #21262d;color:#8b949e;font-size:11px">' + detailDisplay + '</div>' : '');
  tip.style.display = 'block';
  var w = Math.min(tip.offsetWidth || 380, 440);
  var tipX = Math.min(cx, window.innerWidth - w - 15);
  tipX = Math.max(10, tipX);
  var tipY = Math.min(cy, window.innerHeight - 340);
  tipY = Math.max(10, tipY);
  tip.style.left = tipX + 'px';
  tip.style.top = tipY + 'px';
}
function hideTooltip() {
  document.getElementById('tooltip').style.display = 'none';
}
// ----- Render -----
function getPlotW() {
  var wrap = document.getElementById('timeline-wrap');
  var w = wrap.clientWidth - 20;
  if (w < 800) w = 800;
  plotR = w - 60;
  plotL = 130;
  return w;
}
function render() {
  SVG_W = getPlotW();
  var slider = document.getElementById('time-slider');
  var sliderVal = parseInt(slider.value);
  var showAll = sliderVal >= 100;
  var cutTime = showAll ? null : new Date(tMin.getTime() + (tRange * sliderVal / 100));
  var filteredBps = getFilteredBlueprints();
  var visibleBps = filteredBps.filter(function(bp) {
    if (showAll) return true;
    return bpRuns[bp].some(function(r) { return r.ts && new Date(r.ts) <= cutTime; });
  });
  document.getElementById('filter-count').textContent = visibleBps.length + '/' + blueprints.length + ' BPs';
  if (visibleBps.length === 0) {
    document.getElementById('timeline-svg').style.display = 'none';
    document.getElementById('empty-state').style.display = 'block';
    document.getElementById('empty-state').textContent = 'No blueprints match current filters';
    return;
  }
  document.getElementById('timeline-svg').style.display = 'block';
  document.getElementById('empty-state').style.display = 'none';
  var h = visibleBps.length * ROW_H + 80;
  var svg = document.getElementById('timeline-svg');
  svg.setAttribute('width', SVG_W);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 ' + SVG_W + ' ' + h);
  var html = '<rect width="' + SVG_W + '" height="' + h + '" fill="#0d1117"/>';
  // Time axis
  var axisTicks = 12;
  html += '<line x1="' + plotL + '" y1="40" xFortstter direkt dar jag blev avbruten — JavaScript-delen efter time-axis.
```html
  html += '<line x1="' + plotL + '" y1="40" x2="' + plotR + '" y2="40" stroke="#30363d" stroke-width="1"/>';
  for (var i = 0; i <= axisTicks; i++) {
    var t = new Date(tMin.getTime() + (tRange * i / axisTicks));
    var x = plotL + ((plotR - plotL) * i / axisTicks);
    html += '<line x1="' + x + '" y1="38" x2="' + x + '" y2="42" stroke="#30363d" stroke-width="1"/>';
    html += '<text x="' + x + '" y="28" text-anchor="middle" fill="#8b949e" font-size="9" font-family="monospace">'
      + t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'}) + '</text>';
  }
  if (!showAll && cutTime) {
    var cutX = tsToX(cutTime.toISOString());
    html += '<line x1="' + cutX + '" y1="38" x2="' + cutX + '" y2="' + h + '" stroke="#d29922" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>';
  }
  visibleBps.forEach(function(bp, idx) {
    var y = 60 + idx * ROW_H;
    var runs = bpRuns[bp];
    if (idx % 2 === 0) {
      html += '<rect x="0" y="' + y + '" width="' + SVG_W + '" height="' + ROW_H + '" fill="#161b22" opacity="0.3"/>';
    }
    var label = bp.length > 34 ? bp.slice(0, 32) + '..' : bp;
    html += '<text x="10" y="' + (y + ROW_H * 0.65) + '" fill="#e6edf3" font-size="11" font-family="monospace">'
      + label.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</text>';
    var stage = bpStages[bp] || 'refinery';
    var badgeColor = stage === 'production' ? '#3fb950' : stage === 'archive' ? '#8b949e' : '#58a6ff';
    html += '<rect x="' + (plotL - 8) + '" y="' + (y + 3) + '" width="4" height="' + (ROW_H - 6) + '" rx="2" fill="' + badgeColor + '" opacity="0.6"/>';
    html += '<line x1="' + plotL + '" y1="' + (y + ROW_H/2) + '" x2="' + plotR + '" y2="' + (y + ROW_H/2) + '" stroke="#30363d" stroke-width="1" opacity="0.4"/>';
    var sortedRuns = runs.slice().sort(function(a,b) { return (a.ts||'').localeCompare(b.ts||''); });
    var prevX = null;
    sortedRuns.forEach(function(ev) {
      var cx = tsToX(ev.ts);
      if (cx < plotL || cx > plotR) return;
      if (!showAll && cutTime && ev.ts && new Date(ev.ts) > cutTime) return;
      if (prevX !== null) {
        html += '<line x1="' + prevX + '" y1="' + (y + ROW_H/2) + '" x2="' + cx + '" y2="' + (y + ROW_H/2) + '" stroke="#21262d" stroke-width="1" opacity="0.3"/>';
      }
      prevX = cx;
    });
    sortedRuns.forEach(function(ev) {
      var cx = tsToX(ev.ts);
      if (cx < plotL || cx > plotR) return;
      if (!showAll && cutTime && ev.ts && new Date(ev.ts) > cutTime) return;
      var nc = nodeColor(ev);
      var fill = nc[0], stroke = nc[1];
      var r = ev.score !== null ? NODE_R + 2 : NODE_R;
      var evIdx = DATA.indexOf(ev);
      if (ev.score !== null && ev.score >= 85) {
        html += '<circle cx="' + cx + '" cy="' + (y + ROW_H/2) + '" r="' + (r + 3) + '" fill="none" stroke="#d29922" stroke-width="1" opacity="0.2"/>';
      }
      html += '<circle class="node" cx="' + cx + '" cy="' + (y + ROW_H/2) + '" r="' + r + '" fill="' + fill + '" stroke="' + stroke + '" stroke-width="1.5" opacity="0.9"'
        + ' data-idx="' + evIdx + '" style="cursor:pointer"'
        + ' onmouseover="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)"'
        + ' onmouseout="hideTooltip()"'
        + ' onclick="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY);setTimeout(function(){hideTooltip()},4000)"'
        + '>'
        + '<title>' + ev.blueprint + ': ' + ev.action + (ev.score !== null ? ' (' + ev.score.toFixed(1) + ')' : '') + '</title>'
        + '</circle>';
    });
    var scores = runs.map(function(r) { return r.score; }).filter(function(s) { return s !== null; });
    if (scores.length > 0) {
      var maxS = Math.max.apply(null, scores.concat([70]));
      var minS = Math.min.apply(null, scores.concat([0]));
      var sRange = maxS - minS || 1;
      var sparkX = plotR + 8;
      var recentScores = scores.slice(-15);
      recentScores.forEach(function(s, si) {
        var barH = Math.max(2, (s - minS) / sRange * 12);
        var barColor = s >= 85 ? '#d29922' : s >= 70 ? '#db6d28' : '#f85149';
        html += '<rect x="' + (sparkX + si * 3) + '" y="' + (y + ROW_H/2 - barH) + '" width="2" height="' + barH + '" fill="' + barColor + '" opacity="0.7" rx="1"/>';
      });
      var lastS = scores[scores.length - 1];
      var lastColor = lastS >= 85 ? '#d29922' : lastS >= 70 ? '#db6d28' : '#f85149';
      html += '<text x="' + (sparkX + 48) + '" y="' + (y + ROW_H/2 + 4) + '" fill="' + lastColor + '" font-size="9" font-family="monospace">' + lastS.toFixed(0) + '</text>';
    }
  });
  svg.innerHTML = html;
}
function formatTimeDisplay() {
  var slider = document.getElementById('time-slider');
  var val = parseInt(slider.value);
  var display = document.getElementById('time-display');
  if (val >= 100) {
    display.textContent = 'All time (' + DATA.length + ' runs)';
  } else {
    var t = new Date(tMin.getTime() + (tRange * val / 100));
    display.textContent = t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
  }
}
var playInterval = null;
var playing = false;
function bindEvents() {
  var slider = document.getElementById('time-slider');
  slider.addEventListener('input', function() { formatTimeDisplay(); render(); });
  var playBtn = document.getElementById('play-btn');
  playBtn.addEventListener('click', function() {
    if (playing) {
      clearInterval(playInterval);
      playing = false;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
    } else {
      playing = true;
      playBtn.textContent = 'Pause';
      playBtn.classList.add('active');
      if (parseInt(slider.value) >= 100) slider.value = 0;
      playTick();
    }
  });
  function playTick() {
    if (!playing) return;
    var val = parseInt(slider.value);
    if (val >= 100) {
      slider.value = 100;
      formatTimeDisplay();
      render();
      clearInterval(playInterval);
      playing = false;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
      return;
    }
    slider.value = val + 1;
    formatTimeDisplay();
    render();
  }
  document.getElementById('speed-select').addEventListener('change', function() {
    if (playing) {
      clearInterval(playInterval);
      var speed = parseInt(document.getElementById('speed-select').value);
      playInterval = setInterval(playTick, 200 * 100 / speed);
    }
  });
  document.getElementById('reset-btn').addEventListener('click', function() {
    slider.value = 100;
    formatTimeDisplay();
    render();
    if (playing) {
      clearInterval(playInterval);
      playing = false;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
    }
  });
  document.getElementById('stage-filter').addEventListener('change', render);
  document.getElementById('search-input').addEventListener('input', render);
  document.getElementById('score-min-slider').addEventListener('input', function() {
    var min = parseInt(document.getElementById('score-min-slider').value);
    var max = parseInt(document.getElementById('score-max-slider').value);
    if (min > max) document.getElementById('score-min-slider').value = max;
    document.getElementById('score-min-label').textContent = document.getElementById('score-min-slider').value;
    render();
  });
  document.getElementById('score-max-slider').addEventListener('input', function() {
    var min = parseInt(document.getElementById('score-min-slider').value);
    var max = parseInt(document.getElementById('score-max-slider').value);
    if (max < min) document.getElementById('score-max-slider').value = min;
    document.getElementById('score-max-label').textContent = document.getElementById('score-max-slider').value;
    render();
  });
  var resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(render, 150);
  });
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.node') && !e.target.closest('#tooltip')) {
      hideTooltip();
    }
  });
  formatTimeDisplay();
  render();
}
// ----- Start -----
autoLoad();
</script>
</body>
</html>
```