Now I have a complete understanding of the data. Building a fully self-contained agent lifecycle timeline HTML with auto-load, drag-drop fallback, SVG rendering, time scrubber, play/pause, filters, and detail popups.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden}
.header{padding:20px 30px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.header h1{font-size:22px;font-weight:600;color:#f0f6fc}
.header .stats{display:flex;gap:16px;font-size:13px;color:#8b949e;flex-wrap:wrap}
.header .stats span strong{color:#e6edf3}
.load-zone{margin:20px 30px;padding:30px;border:2px dashed #30363d;border-radius:12px;text-align:center;cursor:pointer;background:#161b22;transition:all 0.2s;position:relative}
.load-zone:hover{border-color:#58a6ff;background:#1c2128}
.load-zone.dragover{border-color:#d29922;background:#1c2128}
.load-zone .icon{font-size:36px;margin-bottom:10px}
.load-zone .sub{font-size:12px;color:#8b949e;margin-top:6px}
.load-zone .loaded{font-size:13px;color:#3fb950}
.load-zone.loaded{border-color:#3fb950;background:#1c2128}
.load-zone .auto-status{position:absolute;top:8px;right:12px;font-size:11px;color:#8b949e;font-family:monospace}
.load-error{margin:10px 30px;padding:10px 16px;background:#1c2128;border:1px solid #f85149;border-radius:8px;font-size:12px;color:#f85149;display:none;font-family:monospace;line-height:1.6}
.banner{margin:10px 30px 0;padding:10px 16px;background:#1c2128;border:1px solid #30363d;border-radius:8px;font-size:12px;color:#e6edf3;display:none;font-family:monospace;line-height:1.6}
.banner .ok{color:#3fb950}
.banner .warn{color:#d29922}
.banner .fail{color:#f85149}
.promobar{display:flex;padding:0 30px 10px;gap:20px;flex-wrap:wrap}
.promostat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:8px 16px;min-width:100px;flex:1;text-align:center}
.promostat .val{font-size:20px;font-weight:700;color:#f0f6fc}
.promostat .label{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.promostat .val.gold{color:#d29922}
.promostat .val.green{color:#3fb950}
.promostat .val.blue{color:#58a6ff}
.promostat .val.red{color:#f85149}
.promostat .val.amber{color:#db6d28}
.controls{display:flex;align-items:center;gap:12px;padding:12px 30px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}
.controls label{font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.controls input[type=range].time-slider{height:4px;accent-color:#d29922;cursor:pointer;flex:1;min-width:100px}
.controls .time-display{font-size:12px;color:#e6edf3;font-family:monospace;min-width:155px;white-space:nowrap}
.controls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:500;transition:all 0.15s}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.controls select{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px}
.controls input[type=text]{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px;width:130px}
.controls .srange{display:flex;align-items:center;gap:5px}
.controls .srange input[type=range]{width:70px}
.controls .srange .sv{font-size:11px;color:#e6edf3;font-family:monospace;min-width:20px;text-align:center}
.fcount{font-size:11px;color:#8b949e;padding:0 4px;white-space:nowrap}
.legend{display:flex;gap:16px;padding:8px 30px;font-size:11px;color:#8b949e;border-bottom:1px solid #21262d;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px}
.legend-dot{width:10px;height:10px;border-radius:50%;border:1px solid rgba(255,255,255,.15);flex-shrink:0}
.tw{overflow:auto;max-height:calc(100vh - 280px);position:relative}
.tsvg{display:block;min-width:100%}
.et{padding:60px;text-align:center;color:#8b949e;font-size:14px}
.tip{position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:1000;max-width:420px;box-shadow:0 8px 24px rgba(0,0,0,.5);pointer-events:none;display:none;font-size:12px}
.tip h3{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:6px}
.tip .r{display:flex;justify-content:space-between;gap:16px;padding:3px 0;border-bottom:1px solid #21262d}
.tip .r:last-child{border-bottom:none}
.tip .l{color:#8b949e}
.tip .v{color:#e6edf3;font-family:monospace;text-align:right;max-width:220px;overflow:hidden;text-overflow:ellipsis}
.bdg{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600}
.bdg-prod{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3)}
.bdg-arch{background:rgba(139,148,158,.15);color:#8b949e;border:1px solid rgba(139,148,158,.3)}
.bdg-ref{background:rgba(88,166,255,.15);color:#58a6ff;border:1px solid rgba(88,166,255,.3)}
.spinner{display:inline-block;width:14px;height:14px;border:2px solid #30363d;border-top-color:#58a6ff;border-radius:50%;animation:spin 0.6s linear infinite;vertical-align:middle;margin-right:6px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <div class="stats">
    <span>Blueprints: <strong id="bp-count">0</strong></span>
    <span>Events: <strong id="ev-count">0</strong></span>
    <span>Production: <strong id="prod-count">0</strong></span>
    <span>Scored: <strong id="scored-count">0</strong></span>
    <span>Span: <strong id="time-span">--</strong></span>
  </div>
</div>
<div class="load-zone" id="load-zone">
  <div class="auto-status" id="auto-status"><span class="spinner"></span>Loading state.yaml...</div>
  <div class="icon" id="lz-icon">&#128203;</div>
  <div><strong id="lz-title">Drop state.yaml here</strong></div>
  <div class="sub" id="lz-sub">or click to browse</div>
  <input type="file" id="file-input" accept=".yaml,.yml,.json" style="display:none">
</div>
<div class="load-error" id="load-error"></div>
<div class="banner" id="banner"></div>
<div class="promobar" id="promobar" style="display:none">
  <div class="promostat"><div class="val green" id="s-promo">--</div><div class="label">Promotable</div></div>
  <div class="promostat"><div class="val blue" id="s-avg">--</div><div class="label">Avg Score</div></div>
  <div class="promostat"><div class="val green" id="s-prod">--</div><div class="label">Production</div></div>
  <div class="promostat"><div class="val blue" id="s-ref">--</div><div class="label">Refinery</div></div>
  <div class="promostat"><div class="val red" id="s-arch">--</div><div class="label">Archive</div></div>
  <div class="promostat"><div class="val" id="s-total">--</div><div class="label">Total Agents</div></div>
</div>
<div class="controls" id="controls" style="display:none">
  <label>T</label>
  <input type="range" class="time-slider" id="t-slider" min="0" max="100" value="100" step="1">
  <span class="time-display" id="t-display">All time</span>
  <button id="play-btn">Play</button>
  <button id="reset-btn">Reset</button>
  <select id="speed-sel">
    <option value="50">0.5x</option>
    <option value="100" selected>1x</option>
    <option value="200">2x</option>
    <option value="400">4x</option>
  </select>
  <label>Stage</label>
  <select id="stage-sel">
    <option value="all">All</option>
    <option value="production">Production</option>
    <option value="refinery">Refinery</option>
    <option value="archive">Archive</option>
  </select>
  <label>Search</label>
  <input type="text" id="search-inp" placeholder="Name...">
  <div class="srange">
    <span class="sv" id="smin-l">0</span>
    <input type="range" id="smin-s" min="0" max="100" value="0" step="1">
    <span class="sv" id="smax-l">100</span>
    <input type="range" id="smax-s" min="0" max="100" value="100" step="1">
  </div>
  <span class="fcount" id="fcount"></span>
</div>
<div class="legend" id="legend" style="display:none">
  <div class="legend-item"><div class="legend-dot" style="background:#d29922"></div>Score 85+</div>
  <div class="legend-item"><div class="legend-dot" style="background:#db6d28"></div>Score 70-84</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f85149"></div>Score below 70</div>
  <div class="legend-item"><div class="legend-dot" style="background:#58a6ff"></div>Spawn / Improve</div>
  <div class="legend-item"><div class="legend-dot" style="background:#3fb950;border-color:#3fb950"></div>Production</div>
  <div class="legend-item"><div class="legend-dot" style="background:#8b949e;border-color:#8b949e"></div>Archive</div>
</div>
<div class="tw" id="tw">
  <div class="et" id="et">Loading state.yaml...</div>
  <svg class="tsvg" id="tsvg"></svg>
</div>
<div class="tip" id="tip"></div>
<script>
// ---- Globals ----
var DATA = [], BPS = [], BP_RUNS = {}, BP_STAGE = {}, BP_AGENTS = {};
var TMIN = null, TMAX = null, TRANGE = 1;
var ROW_H = 26, NODE_R = 5, SVG_W = 1200, PL = 130, PR = 1100;
var playInt = null, playing = false;
// ---- Load ----
var lz = document.getElementById('load-zone');
var fi = document.getElementById('file-input');
var as = document.getElementById('auto-status');
lz.addEventListener('click', function(){ fi.click(); });
fi.addEventListener('change', function(e){ if(e.target.files[0]) loadFile(e.target.files[0]); });
lz.addEventListener('dragover', function(e){ e.preventDefault(); lz.classList.add('dragover'); });
lz.addEventListener('dragleave', function(){ lz.classList.remove('dragover'); });
lz.addEventListener('drop', function(e){
  e.preventDefault(); lz.classList.remove('dragover');
  if(e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
});
// Auto-load from URL param or _timeline_data.json or state.yaml
function autoLoad() {
  var params = new URLSearchParams(window.location.search);
  var src = params.get('src') || '_timeline_data.json';
  fetch(src).then(function(r){
    if(!r.ok) throw new Error('HTTP '+r.status);
    return r.text();
  }).then(function(text){
    as.innerHTML = 'Loaded via fetch: '+src;
    try {
      var data = JSON.parse(text);
      if(Array.isArray(data)) processJSON(data);
      else if(data.activity) processYAML(data);
      else processJSON(data);
    } catch(e) {
      try {
        var y = jsyaml.load(text);
        if(y && y.activity) processYAML(y);
        else throw new Error('Not valid state.yaml or timeline_data.json');
      } catch(e2){
        showError('Parse error: '+e2.message);
        enableDrop();
      }
    }
  }).catch(function(err){
    as.innerHTML = 'Drop to load';
    enableDrop();
  });
}
function enableDrop() {
  lz.style.display = 'block';
  document.getElementById('et').textContent = 'Drop a state.yaml file to begin';
}
function loadFile(file) {
  var reader = new FileReader();
  reader.onload = function(evt){
    var text = evt.target.result;
    try {
      var y = jsyaml.load(text);
      if(y && y.activity) processYAML(y);
      else throw new Error('Missing "activity" key');
    } catch(e) {
      try {
        var j = JSON.parse(text);
        if(Array.isArray(j)) processJSON(j);
        else if(j.activity) processYAML(j);
        else throw new Error('Not a valid forge state file');
      } catch(e2){
        showError('Parse error: '+e2.message);
      }
    }
  };
  reader.readAsText(file);
}
function showError(msg) {
  var el = document.getElementById('load-error');
  el.textContent = 'ERROR: '+msg;
  el.style.display = 'block';
}
// ---- Process ----
function processYAML(parsed) {
  var activity = parsed.activity || [];
  var agents = parsed.agents || [];
  processCore(activity, agents);
}
function processJSON(arr) {
  var activity = arr.filter(function(e){ return e.action; });
  var agents = arr.filter(function(e){ return !e.action && e.run_id; });
  processCore(activity, agents);
}
function processCore(activity, agents) {
  // Build agent stage map per blueprint
  var bpAgentMap = {};
  agents.forEach(function(a){
    var bp = a.blueprint; if(!bp) return;
    if(!bpAgentMap[bp]) bpAgentMap[bp] = [];
    bpAgentMap[bp].push(a);
  });
  // Build per-blueprint best stage
  BPS = []; BP_RUNS = {}; BP_STAGE = {}; BP_AGENTS = {};
  var seen = {};
  activity.forEach(function(ev){
    var bp = ev.blueprint; if(!bp) return;
    var ts = ev.timestamp || '';
    var action = ev.action || '';
    var detail = ev.detail || '';
    var eid = ev.id;
    var status = ev.status || '';
    var progress = ev.progress !== undefined ? ev.progress : 0;
    var score = null, selfScore = null, judgeScore = null;
    var cm = detail.match(/C:([0-9.]+)/);
    if(cm) score = parseFloat(cm[1]);
    var sm = detail.match(/S:([0-9.]+)/);
    if(sm) selfScore = parseFloat(sm[1]);
    var jm = detail.match(/J:([0-9.]+)/);
    if(jm) judgeScore = parseFloat(jm[1]);
    if(!seen[bp]) {
      seen[bp] = true;
      BPS.push(bp);
      BP_RUNS[bp] = [];
      BP_AGENTS[bp] = bpAgentMap[bp] || [];
    }
    BP_RUNS[bp].push({
      blueprint: bp, ts: ts, action: action, detail: detail,
      id: eid, status: status, progress: progress,
      run_id: String(eid !== undefined ? eid : ''),
      score: score, selfScore: selfScore, judgeScore: judgeScore
    });
  });
  // Also ensure blueprints from agents section are included
  agents.forEach(function(a){
    var bp = a.blueprint; if(!bp || seen[bp]) return;
    seen[bp] = true;
    BPS.push(bp);
    BP_RUNS[bp] = [];
    BP_AGENTS[bp] = [a];
  });
  BPS.sort();
  // Determine stage per blueprint from agents data
  BPS.forEach(function(bp){
    var agentsForBP = BP_AGENTS[bp] || [];
    var hasProd = false, hasArch = false;
    agentsForBP.forEach(function(a){
      var s = (a.stage || '').toLowerCase();
      if(s === 'production') hasProd = true;
      else if(s === 'archive') hasArch = true;
    });
    // Also check activity for promote
    (BP_RUNS[bp]||[]).forEach(function(r){
      if(r.action === 'promote') hasProd = true;
    });
    if(hasProd) BP_STAGE[bp] = 'production';
    else if(hasArch) BP_STAGE[bp] = 'archive';
    else BP_STAGE[bp] = 'refinery';
  });
  // Sort runs per BP
  BPS.forEach(function(bp){
    BP_RUNS[bp].sort(function(a,b){ return (a.ts||'').localeCompare(b.ts||''); });
  });
  // Time range
  var allT = [];
  BPS.forEach(function(bp){
    (BP_RUNS[bp]||[]).forEach(function(r){
      if(r.ts) allT.push(new Date(r.ts));
    });
    (BP_AGENTS[bp]||[]).forEach(function(a){
      if(a.spawned_at) allT.push(new Date(a.spawned_at));
    });
  });
  allT = allT.filter(function(t){ return t && !isNaN(t.getTime()); });
  allT.sort(function(a,b){ return a-b; });
  if(allT.length===0){ showError('No timestamped events found'); return; }
  TMIN = allT[0]; TMAX = allT[allT.length-1]; TRANGE = TMAX.getTime()-TMIN.getTime() || 1;
  // Build flat data
  DATA = [];
  BPS.forEach(function(bp){
    (BP_RUNS[bp]||[]).forEach(function(r){ DATA.push(r); });
  });
  // Stats
  var scored = DATA.filter(function(d){ return d.score !== null; });
  var sVals = scored.map(function(d){ return d.score; });
  var avg = sVals.length ? sVals.reduce(function(a,b){return a+b;},0)/sVals.length : null;
  var sMin = sVals.length ? Math.min.apply(null, sVals) : null;
  var sMax = sVals.length ? Math.max.apply(null, sVals) : null;
  var prodC = Object.values(BP_STAGE).filter(function(s){return s==='production';}).length;
  var refC = Object.values(BP_STAGE).filter(function(s){return s==='refinery';}).length;
  var archC = Object.values(BP_STAGE).filter(function(s){return s==='archive';}).length;
  var promo = 0;
  BPS.forEach(function(bp){
    var runs = BP_RUNS[bp]||[];
    var sc = runs.map(function(r){return r.score;}).filter(function(s){return s!==null;});
    if(sc.length>=3 && sc.slice(-3).every(function(s){return s>=85;})) promo++;
  });
  // Agents total count
  var agentTotal = 0;
  BPS.forEach(function(bp){ agentTotal += (BP_AGENTS[bp]||[]).length; });
  // Update UI
  document.getElementById('bp-count').textContent = BPS.length;
  document.getElementById('ev-count').textContent = DATA.length;
  document.getElementById('prod-count').textContent = prodC;
  document.getElementById('scored-count').textContent = scored.length;
  document.getElementById('time-span').textContent = TMIN.toISOString().slice(0,10)+' - '+TMAX.toISOString().slice(0,10);
  document.getElementById('s-promo').textContent = promo;
  document.getElementById('s-avg').textContent = avg !== null ? avg.toFixed(1) : '--';
  document.getElementById('s-prod').textContent = prodC;
  document.getElementById('s-ref').textContent = refC;
  document.getElementById('s-arch').textContent = archC;
  document.getElementById('s-total').textContent = agentTotal;
  // Update load zone
  lz.classList.add('loaded');
  document.getElementById('lz-icon').textContent = '\u2705';
  document.getElementById('lz-title').textContent = 'state.yaml loaded';
  document.getElementById('lz-sub').textContent = BPS.length+' blueprints, '+DATA.length+' events, '+agentTotal+' agents';
  as.innerHTML = '<span style="color:#3fb950">Loaded</span>';
  document.getElementById('promobar').style.display = 'flex';
  document.getElementById('controls').style.display = 'flex';
  document.getElementById('legend').style.display = 'flex';
  document.getElementById('et').textContent = '';
  var banner = document.getElementById('banner');
  banner.innerHTML = '<span class="ok">DATA LOADED</span> Blueprints: '+BPS.length
    +' | Events: '+DATA.length+' | Scored: '+scored.length
    +' | Score range: '+(sMin!==null?sMin.toFixed(1):'N/A')+' - '+(sMax!==null?sMax.toFixed(1):'N/A')
    +' | Avg: '+(avg!==null?avg.toFixed(1):'N/A')
    +' | Production: '+prodC+' | Refinery: '+refC+' | Archive: '+archC+' | Promotable: '+promo;
  banner.style.display = 'block';
  updateTimeDisplay();
  render();
  bindEvents();
}
// ---- Color ----
function scColor(s){
  if(s===null) return '#58a6ff';
  if(s>=85) return '#d29922';
  if(s>=70) return '#db6d28';
  return '#f85149';
}
function ndColor(ev){
  if(ev.action==='spawn'||ev.action==='improve'||ev.action==='promote')
    return ['#58a6ff','#1f6feb'];
  if(ev.score!==null){
    if(ev.score>=85) return ['#d29922','#b0881a'];
    if(ev.score>=70) return ['#db6d28','#b05a1a'];
    return ['#f85149','#c83030'];
  }
  return ['#8b949e','#6e7681'];
}
function tsX(ts){
  if(!ts) return PL;
  var t = new Date(ts); if(isNaN(t.getTime())) return PL;
  return PL + ((t.getTime()-TMIN.getTime())/TRANGE)*(PR-PL);
}
// ---- Filter ----
function getBPs(){
  var sf = document.getElementById('stage-sel').value;
  var q = document.getElementById('search-inp').value.toLowerCase().trim();
  var smin = parseInt(document.getElementById('smin-s').value);
  var smax = parseInt(document.getElementById('smax-s').value);
  return BPS.filter(function(bp){
    if(q && bp.toLowerCase().indexOf(q)===-1) return false;
    if(sf!=='all' && BP_STAGE[bp]!==sf) return false;
    if(smin>0 || smax<100){
      var ok = (BP_RUNS[bp]||[]).some(function(r){ return r.score!==null && r.score>=smin && r.score<=smax; });
      if(!ok) return false;
    }
    return true;
  });
}
// ---- Tooltip ----
var tipEl = document.getElementById('tip');
function showTip(ev, cx, cy){
  var stage = BP_STAGE[ev.blueprint]||'refinery';
  var badgeClass = stage==='production'?'bdg-prod':stage==='archive'?'bdg-arch':'bdg-ref';
  var scH = '';
  if(ev.score!==null){
    scH += '<div class="r"><span class="l">Composite (C)</span><span class="v">'+ev.score.toFixed(1)+'</span></div>';
    if(ev.selfScore!==null) scH += '<div class="r"><span class="l">Self (S)</span><span class="v">'+ev.selfScore.toFixed(1)+'</span></div>';
    if(ev.judgeScore!==null) scH += '<div class="r"><span class="l">Judge (J)</span><span class="v">'+ev.judgeScore.toFixed(1)+'</span></div>';
  }
  var detailD = ev.detail&&ev.detail.length>60 ? ev.detail.slice(0,58)+'...' : ev.detail||'';
  // Find agent version
  var agentsBP = BP_AGENTS[ev.blueprint]||[];
  var agentInfo = '';
  if(agentsBP.length && ev.run_id){
    var matchA = agentsBP.filter(function(a){ return a.run_id && ev.run_id.indexOf(a.run_id.slice(0,8)) !== -1; });
    if(matchA.length){
      agentInfo = '<div class="r"><span class="l">Version</span><span class="v">iter '+matchA[0].iteration+'</span></div>';
      if(matchA[0].benchmark) agentInfo += '<div class="r"><span class="l">Benchmark</span><span class="v">'+matchA[0].benchmark+'</span></div>';
    }
  }
  tipEl.innerHTML =
    '<h3>'+ev.blueprint+'</h3>'+
    '<div style="margin-bottom:6px"><span class="bdg '+badgeClass+'">'+stage+'</span> <span style="color:#8b949e;font-size:11px">#'+ev.run_id+'</span></div>'+
    '<div class="r"><span class="l">Action</span><span class="v">'+ev.action+(ev.status?' ('+ev.status+')':'')+'</span></div>'+
    '<div class="r"><span class="l">Progress</span><span class="v">'+(ev.progress||0)+'%</span></div>'+
    scH+agentInfo+
    '<div class="r"><span class="l">Timestamp</span><span class="v">'+ev.ts+'</span></div>'+
    (detailD ? '<div style="margin-top:6px;padding-top:6px;border-top:1px solid #21262d;color:#8b949e;font-size:11px">'+detailD+'</div>' : '');
  tipEl.style.display = 'block';
  var w = Math.min(tipEl.offsetWidth||380, 420);
  var tx = Math.max(10, Math.min(cx, window.innerWidth-w-15));
  var ty = Math.max(10, Math.min(cy, window.innerHeight-320));
  tipEl.style.left = tx+'px'; tipEl.style.top = ty+'px';
}
function hideTip(){ tipEl.style.display='none'; }
// ---- Render ----
function getPW(){
  var w = document.getElementById('tw').clientWidth-20;
  if(w<800) w=800;
  PR = w-60; PL = 130;
  return w;
}
function render(){
  SVG_W = getPW();
  var sl = document.getElementById('t-slider');
  var sv = parseInt(sl.value);
  var all = sv>=100;
  var cut = all ? null : new Date(TMIN.getTime()+(TRANGE*sv/100));
  var fbps = getBPs();
  var vbps = fbps.filter(function(bp){
    if(all) return true;
    return (BP_RUNS[bp]||[]).some(function(r){ return r.ts && new Date(r.ts)<=cut; });
  });
  document.getElementById('fcount').textContent = vbps.length+'/'+BPS.length+' BPs';
  if(vbps.length===0){
    document.getElementById('tsvg').style.display='none';
    document.getElementById('et').style.display='block';
    document.getElementById('et').textContent='No blueprints match current filters';
    return;
  }
  document.getElementById('tsvg').style.display='block';
  document.getElementById('et').style.display='none';
  var h = vbps.length*ROW_H + 80;
  var svg = document.getElementById('tsvg');
  svg.setAttribute('width', SVG_W);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 '+SVG_W+' '+h);
  var parts = ['<rect width="'+SVG_W+'" height="'+h+'" fill="#0d1117"/>'];
  // Time axis
  var ticks = 10;
  parts.push('<line x1="'+PL+'" y1="40" x2="'+PR+'" y2="40" stroke="#30363d" stroke-width="1"/>');
  for(var i=0;i<=ticks;i++){
    var t = new Date(TMIN.getTime()+(TRANGE*i/ticks));
    var x = PL+((PR-PL)*i/ticks);
    parts.push('<line x1="'+x+'" y1="38" x2="'+x+'" y2="42" stroke="#30363d" stroke-width="1"/>');
    parts.push('<text x="'+x+'" y="28" text-anchor="middle" fill="#8b949e" font-size="9" font-family="monospace">'
      +t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'})+'</text>');
  }
  // Cutoff
  if(!all && cut){
    var cx = tsX(cut.toISOString());
    parts.push('<line x1="'+cx+'" y1="38" x2="'+cx+'" y2="'+h+'" stroke="#d29922" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>');
  }
  // Rows
  vbps.forEach(function(bp, idx){
    var y = 60+idx*ROW_H;
    var runs = BP_RUNS[bp]||[];
    if(idx%2===0) parts.push('<rect x="0" y="'+y+'" width="'+SVG_W+'" height="'+ROW_H+'" fill="#161b22" opacity="0.3"/>');
    // Label
    var label = bp.length>34 ? bp.slice(0,32)+'..' : bp;
    label = label.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    parts.push('<text x="10" y="'+(y+ROW_H*0.65)+'" fill="#e6edf3" font-size="11" font-family="monospace">'+label+'</text>');
    // Stage indicator
    var stage = BP_STAGE[bp]||'refinery';
    var sc = stage==='production'?'#3fb950':stage==='archive'?'#8b949e':'#58a6ff';
    parts.push('<rect x="'+(PL-8)+'" y="'+(y+3)+'" width="4" height="'+(ROW_H-6)+'" rx="2" fill="'+sc+'" opacity="0.6"/>');
    // Timeline line
    parts.push('<line x1="'+PL+'" y1="'+(y+ROW_H/2)+'" x2="'+PR+'" y2="'+(y+ROW_H/2)+'" stroke="#30363d" stroke-width="1" opacity="0.3"/>');
    // Connectors
    var prevX = null;
    runs.forEach(function(ev){
      var cx2 = tsX(ev.ts);
      if(cx2<PL||cx2>PR) return;
      if(!all && cut && ev.ts && new Date(ev.ts)>cut) return;
      if(prevX!==null) parts.push('<line x1="'+prevX+'" y1="'+(y+ROW_H/2)+'" x2="'+cx2+'" y2="'+(y+ROW_H/2)+'" stroke="#21262d" stroke-width="1" opacity="0.25"/>');
      prevX = cx2;
    });
    // Nodes
    runs.forEach(function(ev){
      var cx2 = tsX(ev.ts);
      if(cx2<PL||cx2>PR) return;
      if(!all && cut && ev.ts && new Date(ev.ts)>cut) return;
      var nc = ndColor(ev);
      var r = ev.score!==null ? NODE_R+2 : NODE_R;
      var evIdx = DATA.indexOf(ev);
      var title = ev.blueprint+': '+ev.action+(ev.score!==null?' ('+ev.score.toFixed(1)+')':'');
      if(ev.score!==null && ev.score>=85){
        parts.push('<circle cx="'+cx2+'" cy="'+(y+ROW_H/2)+'" r="'+(r+3)+'" fill="none" stroke="#d29922" stroke-width="1" opacity="0.2"/>');
      }
      parts.push('<circle class="node" cx="'+cx2+'" cy="'+(y+ROW_H/2)+'" r="'+r+'" fill="'+nc[0]+'" stroke="'+nc[1]+'" stroke-width="1.5" opacity="0.9"'
        +' data-idx="'+evIdx+'" style="cursor:pointer"'
        +' onmouseover="showTip(DATA[this.dataset.idx],event.clientX,event.clientY)"'
        +' onmouseout="hideTip()"'
        +' onclick="showTip(DATA[this.dataset.idx],event.clientX,event.clientY);var t=this;setTimeout(function(){hideTip()},4000)"'
        +'><title>'+title+'</title></circle>');
    });
    // Score sparkline (last 15)
    var scores = runs.map(function(r){return r.score;}).filter(function(s){return s!==null;});
    if(scores.length>0){
      var maxS = Math.max.apply(null, scores.concat([70]));
      var minS = Math.min.apply(null, scores.concat([0]));
      var sR = maxS-minS||1;
      var sx = PR+8;
      var recent = scores.slice(-15);
      recent.forEach(function(s, si){
        var bh = Math.max(2, (s-minS)/sR*12);
        var bc = s>=85?'#d29922':s>=70?'#db6d28':'#f85149';
        parts.push('<rect x="'+(sx+si*3)+'" y="'+(y+ROW_H/2-bh)+'" width="2" height="'+bh+'" fill="'+bc+'" opacity="0.7" rx="1"/>');
      });
      var lastS = scores[scores.length-1];
      var lc = lastS>=85?'#d29922':lastS>=70?'#db6d28':'#f85149';
      parts.push('<text x="'+(sx+48)+'" y="'+(y+ROW_H/2+4)+'" fill="'+lc+'" font-size="9" font-family="monospace">'+lastS.toFixed(0)+'</text>');
    }
  });
  svg.innerHTML = parts.join('');
}
// ---- Time display ----
function updateTimeDisplay(){
  var sl = document.getElementById('t-slider');
  var v = parseInt(sl.value);
  var d = document.getElementById('t-display');
  if(v>=100) d.textContent = 'All time ('+DATA.length+' events)';
  else {
    var t = new Date(TMIN.getTime()+(TRANGE*v/100));
    d.textContent = t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
  }
}
// ---- Events ----
function bindEvents(){
  var sl = document.getElementById('t-slider');
  sl.addEventListener('input', function(){ updateTimeDisplay(); render(); });
  var pb = document.getElementById('play-btn');
  pb.addEventListener('click', function(){
    if(playing){
      clearInterval(playInt); playing=false;
      pb.textContent='Play'; pb.classList.remove('active');
    } else {
      playing=true; pb.textContent='Pause'; pb.classList.add('active');
      if(parseInt(sl.value)>=100) sl.value=0;
      tick();
    }
  });
  function tick(){
    if(!playing) return;
    var v = parseInt(sl.value);
    if(v>=100){
      sl.value=100; updateTimeDisplay(); render();
      clearInterval(playInt); playing=false;
      pb.textContent='Play'; pb.classList.remove('active');
      return;
    }
    sl.value=v+1; updateTimeDisplay(); render();
  }
  document.getElementById('speed-sel').addEventListener('change', function(){
    if(playing){
      clearInterval(playInt);
      var sp = parseInt(document.getElementById('speed-sel').value);
      playInt = setInterval(tick, 200*100/sp);
    }
  });
  document.getElementById('reset-btn').addEventListener('click', function(){
    sl.value=100; updateTimeDisplay(); render();
    if(playing){ clearInterval(playInt); playing=false; pb.textContent='Play'; pb.classList.remove('active'); }
  });
  document.getElementById('stage-sel').addEventListener('change', render);
  document.getElementById('search-inp').addEventListener('input', render);
  document.getElementById('smin-s').addEventListener('input', function(){
    var mn = parseInt(document.getElementById('smin-s').value);
    var mx = parseInt(document.getElementById('smax-s').value);
    if(mn>mx) document.getElementById('smin-s').value=mx;
    document.getElementById('smin-l').textContent = document.getElementById('smin-s').value;
    render();
  });
  document.getElementById('smax-s').addEventListener('input', function(){
    var mn = parseInt(document.getElementById('smin-s').value);
    var mx = parseInt(document.getElementById('smax-s').value);
    if(mx<mn) document.getElementById('smax-s').value=mn;
    document.getElementById('smax-l').textContent = document.getElementById('smax-s').value;
    render();
  });
  var rt;
  window.addEventListener('resize', function(){ clearTimeout(rt); rt=setTimeout(render,150); });
  document.addEventListener('click', function(e){
    if(!e.target.closest('.node') && !e.target.closest('#tip')) hideTip();
  });
  updateTimeDisplay(); render();
}
// ---- Start ----
autoLoad();
</script>
</body>
</html>
```
The HTML is complete. Key features:
- Auto-loads `_timeline_data.json` via fetch on page load (trys from URL param `?src=`, falling back to the default)
- Falls back to drag-and-drop if served from file:// protocol
- Parses both `activity` events and `agents` records from state.yaml
- SVG timeline: one horizontal track per blueprint, connected event nodes
- Node colors: gold =85+, amber 70-84, red below 70, blue for spawn/improve
- Time scrubber: drag or auto-play with speed control (0.5x-4x)
- Stage filters: Production / Refinery / Archive
- Text search and score range sliders
- Click/hover tooltip: run_id, action, composite/self/judge scores, progress, timestamp
- Agent version and benchmark from the agents section
- Score sparklines (last 15) for each blueprint
- Promotion bar with aggregate stats (promotable count, avg score, stage breakdowns)
To use: save as `agent-lifecycle-timeline.html` in the forge directory and open in a browser, or drag-drop state.yaml onto the drop zone. If served via HTTP (any static server), it auto-loads `_timeline_data.json`.