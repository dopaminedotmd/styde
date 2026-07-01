```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Courier New',monospace;padding:24px;min-height:100vh}
header{margin-bottom:28px}
h1{font-size:18px;color:#00d2ff;letter-spacing:2px;text-transform:uppercase;font-weight:300}
h1 span{color:#ffd700}
.subtitle{font-size:11px;color:#576574;margin-top:4px;letter-spacing:1px}
.controls{display:flex;align-items:center;gap:16px;margin-bottom:20px;background:#111827;padding:12px 16px;border:1px solid #1e293b;border-radius:4px}
.controls label{font-size:11px;color:#576574;text-transform:uppercase;letter-spacing:1px}
#timeSlider{flex:1;height:4px;-webkit-appearance:none;appearance:none;background:#1e293b;outline:none;border-radius:2px}
#timeSlider::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;background:#00d2ff;border-radius:50%;cursor:pointer;border:2px solid #0a0e17}
#timeSlider::-moz-range-thumb{width:14px;height:14px;background:#00d2ff;border-radius:50%;cursor:pointer;border:2px solid #0a0e17}
#timeDisplay{font-size:11px;color:#00d2ff;min-width:130px;font-family:'Courier New',monospace}
.btn{background:transparent;border:1px solid #1e293b;color:#576574;padding:4px 12px;font-size:11px;font-family:'Courier New',monospace;cursor:pointer;border-radius:3px;text-transform:uppercase;letter-spacing:1px;transition:all .2s}
.btn:hover{border-color:#00d2ff;color:#00d2ff}
.btn.active{background:#00d2ff;color:#0a0e17;border-color:#00d2ff}
#timelineContainer{overflow-x:auto;overflow-y:auto;max-height:70vh;border:1px solid #1e293b;border-radius:4px;padding:16px;background:#0d111f}
.track{display:flex;align-items:center;margin-bottom:6px;min-height:40px;position:relative}
.track-label{width:140px;font-size:10px;color:#576574;text-transform:uppercase;letter-spacing:1px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:12px;text-align:right}
.track-path{flex:1;position:relative;height:36px;display:flex;align-items:center}
.track-line{position:absolute;left:0;right:0;top:50%;height:1px;background:#1e293b;transform:translateY(-50%)}
.node{position:absolute;width:14px;height:14px;border-radius:50%;cursor:pointer;transform:translateX(-50%);z-index:2;transition:transform .15s,box-shadow .15s;border:2px solid #0d111f}
.node:hover{transform:translateX(-50%) scale(1.6);z-index:10}
.node.gold{background:#ffd700;box-shadow:0 0 8px rgba(255,215,0,0.4)}
.node.amber{background:#ff8c00;box-shadow:0 0 8px rgba(255,140,0,0.3)}
.node.cool{background:#4a69bd;box-shadow:0 0 8px rgba(74,105,189,0.3)}
.node.inactive{background:#2d3436;border-color:#2d3436;cursor:default}
.node-label{position:absolute;top:18px;left:50%;transform:translateX(-50%);font-size:8px;color:#576574;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity .2s}
.node:hover .node-label{opacity:1}
.detail-popup{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#111827;border:1px solid #1e293b;border-radius:6px;padding:24px;z-index:100;min-width:320px;display:none;box-shadow:0 20px 60px rgba(0,0,0,0.6)}
.detail-popup.open{display:block}
.detail-popup h2{font-size:14px;color:#00d2ff;margin-bottom:12px;letter-spacing:1px;text-transform:uppercase}
.detail-popup table{width:100%;border-collapse:collapse}
.detail-popup td{padding:6px 8px;font-size:11px;border-bottom:1px solid #1e293b}
.detail-popup td:first-child{color:#576574;width:90px;text-transform:uppercase;letter-spacing:1px}
.detail-popup td:last-child{color:#c8d6e5}
.detail-popup .close-btn{position:absolute;top:12px;right:16px;background:none;border:none;color:#576574;font-size:16px;cursor:pointer;font-family:'Courier New',monospace}
.detail-popup .close-btn:hover{color:#ff6b6b}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:99;display:none}
.overlay.open{display:block}
.legend{display:flex;gap:20px;margin-bottom:16px;padding:8px 0}
.legend-item{display:flex;align-items:center;gap:6px;font-size:10px;color:#576574;text-transform:uppercase;letter-spacing:1px}
.legend-dot{width:10px;height:10px;border-radius:50%}
.legend-dot.gold{background:#ffd700}
.legend-dot.amber{background:#ff8c00}
.legend-dot.cool{background:#4a69bd}
.stats{display:flex;gap:24px;margin-bottom:16px}
.stat{font-size:11px}
.stat .val{color:#00d2ff;font-weight:bold;font-size:14px}
.stat .lbl{color:#576574;text-transform:uppercase;letter-spacing:1px}
.empty-state{text-align:center;padding:60px 20px;color:#576574;font-size:11px;letter-spacing:1px}
.empty-state .icon{font-size:36px;margin-bottom:12px;color:#1e293b}
</style>
</head>
<body>
<header>
<h1>[AGENT LIFECYCLE] <span>TIMELINE</span></h1>
<div class="subtitle">SPAWN / EVAL / IMPROVE / PROMOTE &mdash; TRACKING 231 BLUEPRINTS</div>
</header>
<div class="stats" id="statsBar">
  <div class="stat"><span class="val" id="totalAgents">0</span> <span class="lbl">AGENTS</span></div>
  <div class="stat"><span class="val" id="promotedCount">0</span> <span class="lbl">PROMOTED</span></div>
  <div class="stat"><span class="val" id="goldCount">0</span> <span class="lbl">GOLD (85+)</span></div>
  <div class="stat"><span class="val" id="amberCount">0</span> <span class="lbl">AMBER (70-84)</span></div>
  <div class="stat"><span class="val" id="coolCount">0</span> <span class="lbl">COOL (&lt;70)</span></div>
</div>
<div class="legend">
  <div class="legend-item"><span class="legend-dot gold"></span>Gold (85+)</div>
  <div class="legend-item"><span class="legend-dot amber"></span>Amber (70-84)</div>
  <div class="legend-item"><span class="legend-dot cool"></span>Cool (&lt;70)</div>
</div>
<div class="controls">
  <label>SCRUBBER</label>
  <input type="range" id="timeSlider" min="0" max="100" value="100">
  <span id="timeDisplay">2026-06-29 23:59:59</span>
  <button class="btn" id="playBtn">PLAY</button>
  <button class="btn" id="resetBtn">RESET</button>
</div>
<div id="timelineContainer">
  <div id="timelineContent"><div class="empty-state"><div class="icon">&#8987;</div>LOADING AGENT DATA...</div></div>
</div>
<div class="overlay" id="overlay"></div>
<div class="detail-popup" id="detailPopup">
  <button class="close-btn" id="closePopup">X</button>
  <h2 id="popupTitle">AGENT DETAIL</h2>
  <table>
    <tr><td>Blueprint</td><td id="popBp">-</td></tr>
    <tr><td>Run ID</td><td id="popRunId">-</td></tr>
    <tr><td>Version</td><td id="popVersion">-</td></tr>
    <tr><td>Stage</td><td id="popStage">-</td></tr>
    <tr><td>Score</td><td id="popScore">-</td></tr>
    <tr><td>Benchmark</td><td id="popBench">-</td></tr>
    <tr><td>Timestamp</td><td id="popTime">-</td></tr>
  </table>
</div>
<script>
// ============================================================
// 1. DATA: Simulate parsed state.yaml — 15 blueprints, multi-run
// ============================================================
const AGENT_DATA = [
  {bp:"html-generator",    runs:[
    {run_id:"run_a1", ver:"v1.0", stage:"refinery",  score:72, bench:"completeness", ts:"2026-06-25T08:12:00"},
    {run_id:"run_a2", ver:"v1.1", stage:"refinery",  score:81, bench:"completeness", ts:"2026-06-25T14:30:00"},
    {run_id:"run_a3", ver:"v1.2", stage:"production",score:88, bench:"completeness", ts:"2026-06-26T09:15:00"}
  ]},
  {bp:"css-generator",     runs:[
    {run_id:"run_b1", ver:"v1.0", stage:"refinery",  score:45, bench:"design",       ts:"2026-06-25T09:00:00"},
    {run_id:"run_b2", ver:"v1.1", stage:"refinery",  score:63, bench:"design",       ts:"2026-06-25T16:45:00"},
    {run_id:"run_b3", ver:"v1.2", stage:"refinery",  score:71, bench:"design",       ts:"2026-06-26T11:30:00"},
    {run_id:"run_b4", ver:"v1.3", stage:"refinery",  score:78, bench:"design",       ts:"2026-06-27T08:00:00"},
    {run_id:"run_b5", ver:"v1.4", stage:"production",score:86, bench:"design",       ts:"2026-06-28T10:00:00"}
  ]},
  {bp:"js-scrubber",       runs:[
    {run_id:"run_c1", ver:"v0.9", stage:"refinery",  score:38, bench:"functionality",ts:"2026-06-24T13:00:00"},
    {run_id:"run_c2", ver:"v1.0", stage:"refinery",  score:55, bench:"functionality",ts:"2026-06-25T10:15:00"},
    {run_id:"run_c3", ver:"v1.1", stage:"refinery",  score:60, bench:"functionality",ts:"2026-06-26T07:45:00"},
    {run_id:"run_c4", ver:"v1.2", stage:"production",score:83, bench:"functionality",ts:"2026-06-27T14:00:00"}
  ]},
  {bp:"statedb-reader",    runs:[
    {run_id:"run_d1", ver:"v1.0", stage:"refinery",  score:18, bench:"integrity",    ts:"2026-06-23T11:00:00"},
    {run_id:"run_d2", ver:"v1.1", stage:"refinery",  score:35, bench:"integrity",    ts:"2026-06-24T09:30:00"},
    {run_id:"run_d3", ver:"v1.2", stage:"refinery",  score:52, bench:"integrity",    ts:"2026-06-25T15:00:00"},
    {run_id:"run_d4", ver:"v1.3", stage:"refinery",  score:68, bench:"integrity",    ts:"2026-06-26T12:15:00"},
    {run_id:"run_d5", ver:"v1.4", stage:"refinery",  score:74, bench:"integrity",    ts:"2026-06-27T09:45:00"},
    {run_id:"run_d6", ver:"v1.5", stage:"production",score:85, bench:"integrity",    ts:"2026-06-28T16:30:00"}
  ]},
  {bp:"promotion-tracker", runs:[
    {run_id:"run_e1", ver:"v2.0", stage:"refinery",  score:89, bench:"accuracy",     ts:"2026-06-25T12:00:00"},
    {run_id:"run_e2", ver:"v2.1", stage:"production",score:92, bench:"accuracy",     ts:"2026-06-26T08:00:00"}
  ]},
  {bp:"teacher-eval",      runs:[
    {run_id:"run_f1", ver:"v3.0", stage:"refinery",  score:70, bench:"pedagogy",     ts:"2026-06-24T15:30:00"},
    {run_id:"run_f2", ver:"v3.1", stage:"refinery",  score:76, bench:"pedagogy",     ts:"2026-06-25T18:00:00"},
    {run_id:"run_f3", ver:"v3.2", stage:"production",score:84, bench:"pedagogy",     ts:"2026-06-27T11:00:00"}
  ]},
  {bp:"config-parser",     runs:[
    {run_id:"run_g1", ver:"v1.0", stage:"refinery",  score:91, bench:"parsing",      ts:"2026-06-26T10:00:00"}
  ]},
  {bp:"blueprint-archiver",runs:[
    {run_id:"run_h1", ver:"v0.5", stage:"refinery",  score:44, bench:"reliability",  ts:"2026-06-22T09:00:00"},
    {run_id:"run_h2", ver:"v0.6", stage:"refinery",  score:58, bench:"reliability",  ts:"2026-06-23T14:00:00"},
    {run_id:"run_h3", ver:"v0.7", stage:"production",score:76, bench:"reliability",  ts:"2026-06-25T11:30:00"}
  ]},
  {bp:"cache-validator",   runs:[
    {run_id:"run_i1", ver:"v1.0", stage:"refinery",  score:62, bench:"performance",  ts:"2026-06-26T14:00:00"},
    {run_id:"run_i2", ver:"v1.1", stage:"refinery",  score:73, bench:"performance",  ts:"2026-06-27T10:30:00"},
    {run_id:"run_i3", ver:"v1.2", stage:"production",score:88, bench:"performance",  ts:"2026-06-28T12:00:00"}
  ]},
  {bp:"eval-yaml-scanner", runs:[
    {run_id:"run_j1", ver:"v0.8", stage:"refinery",  score:29, bench:"coverage",     ts:"2026-06-21T16:00:00"},
    {run_id:"run_j2", ver:"v0.9", stage:"refinery",  score:47, bench:"coverage",     ts:"2026-06-22T11:00:00"},
    {run_id:"run_j3", ver:"v1.0", stage:"refinery",  score:59, bench:"coverage",     ts:"2026-06-23T08:00:00"},
    {run_id:"run_j4", ver:"v1.1", stage:"production",score:82, bench:"coverage",     ts:"2026-06-25T09:00:00"}
  ]},
  {bp:"filesystem-watcher",runs:[
    {run_id:"run_k1", ver:"v2.0", stage:"refinery",  score:95, bench:"consistency",  ts:"2026-06-27T15:00:00"},
    {run_id:"run_k2", ver:"v2.1", stage:"production",score:97, bench:"consistency",  ts:"2026-06-28T18:00:00"}
  ]},
  {bp:"parallel-spawner",  runs:[
    {run_id:"run_l1", ver:"v1.0", stage:"refinery",  score:66, bench:"throughput",   ts:"2026-06-25T13:00:00"},
    {run_id:"run_l2", ver:"v1.1", stage:"refinery",  score:77, bench:"throughput",   ts:"2026-06-26T16:00:00"},
    {run_id:"run_l3", ver:"v1.2", stage:"production",score:85, bench:"throughput",   ts:"2026-06-27T20:00:00"}
  ]},
  {bp:"score-aggregator",  runs:[
    {run_id:"run_m1", ver:"v3.0", stage:"refinery",  score:80, bench:"math",         ts:"2026-06-26T06:00:00"},
    {run_id:"run_m2", ver:"v3.1", stage:"production",score:87, bench:"math",         ts:"2026-06-27T13:00:00"}
  ]},
  {bp:"cron-scheduler",    runs:[
    {run_id:"run_n1", ver:"v1.0", stage:"refinery",  score:41, bench:"scheduling",   ts:"2026-06-24T10:00:00"},
    {run_id:"run_n2", ver:"v1.1", stage:"refinery",  score:53, bench:"scheduling",   ts:"2026-06-25T17:30:00"},
    {run_id:"run_n3", ver:"v1.2", stage:"production",score:69, bench:"scheduling",   ts:"2026-06-26T15:00:00"}
  ]},
  {bp:"state-yaml-backup", runs:[
    {run_id:"run_o1", ver:"v0.1", stage:"refinery",  score:22, bench:"durability",   ts:"2026-06-20T08:00:00"},
    {run_id:"run_o2", ver:"v0.2", stage:"refinery",  score:33, bench:"durability",   ts:"2026-06-21T12:00:00"},
    {run_id:"run_o3", ver:"v0.3", stage:"archive",   score:48, bench:"durability",   ts:"2026-06-22T16:00:00"},
    {run_id:"run_o4", ver:"v0.4", stage:"archive",   score:56, bench:"durability",   ts:"2026-06-23T10:00:00"},
    {run_id:"run_o5", ver:"v0.5", stage:"archive",   score:61, bench:"durability",   ts:"2026-06-24T14:00:00"},
    {run_id:"run_o6", ver:"v0.6", stage:"production",score:73, bench:"durability",   ts:"2026-06-26T11:00:00"}
  ]}
];
// ============================================================
// 2. DERIVED
// ============================================================
const ALL_RUNS = AGENT_DATA.flatMap(d => d.runs.map(r => ({...r, bp:d.bp})));
ALL_RUNS.sort((a,b) => new Date(a.ts)-new Date(b.ts));
const T0 = ALL_RUNS.length>0 ? new Date(ALL_RUNS[0].ts).getTime() : 0;
const T1 = ALL_RUNS.length>0 ? new Date(ALL_RUNS[ALL_RUNS.length-1].ts).getTime() : 1;
const SPAN = T1-T0 || 1;
function scoreColor(s){
  if(s>=85) return 'gold';
  if(s>=70) return 'amber';
  return 'cool';
}
function fmtTime(ms){
  const d=new Date(ms);
  return d.toISOString().replace('T',' ').slice(0,19);
}
function fmtShort(ms){
  const d=new Date(ms);
  return (d.getMonth()+1)+'/'+d.getDate()+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
}
// ============================================================
// 3. RENDER
// ============================================================
let currentCutoffMs = T1;
let animFrame = null;
let playing = false;
let playStartTime = 0;
function render(cutoffMs){
  currentCutoffMs = cutoffMs;
  const container = document.getElementById('timelineContent');
  // Filter runs up to cutoff
  const visible = ALL_RUNS.filter(r => new Date(r.ts).getTime() <= cutoffMs);
  // Per-blueprint runs
  const bpMap = {};
  for(const r of visible){
    if(!bpMap[r.bp]) bpMap[r.bp] = [];
    bpMap[r.bp].push(r);
  }
  // Update stats
  const promoted = visible.filter(r => r.stage==='production').length;
  const gold = visible.filter(r => r.score>=85).length;
  const amber = visible.filter(r => r.score>=70 && r.score<85).length;
  const cool = visible.filter(r => r.score<70).length;
  document.getElementById('totalAgents').textContent = visible.length;
  document.getElementById('promotedCount').textContent = promoted;
  document.getElementById('goldCount').textContent = gold;
  document.getElementById('amberCount').textContent = amber;
  document.getElementById('coolCount').textContent = cool;
  // Blueprints with at least one run
  const bps = AGENT_DATA.filter(d => bpMap[d.bp] && bpMap[d.bp].length>0);
  if(bps.length===0){
    container.innerHTML = '<div class="empty-state"><div class="icon">&#8987;</div>NO AGENT RUNS IN THIS TIME RANGE</div>';
    document.getElementById('timeDisplay').textContent = fmtTime(cutoffMs);
    return;
  }
  let html = '';
  for(const bp of bps){
    const runs = bpMap[bp.bp];
    html += '<div class="track">';
    html += '<div class="track-label">'+bp.bp+'</div>';
    html += '<div class="track-path">';
    html += '<div class="track-line"></div>';
    for(const r of runs){
      const pct = ((new Date(r.ts).getTime()-T0)/SPAN)*100;
      const cls = scoreColor(r.score);
      html += '<div class="node '+cls+'" style="left:'+pct.toFixed(1)+'%" data-runid="'+r.run_id+'" data-bp="'+r.bp+'" data-ver="'+r.ver+'" data-stage="'+r.stage+'" data-score="'+r.score+'" data-bench="'+r.bench+'" data-ts="'+r.ts+'">';
      html += '<div class="node-label">'+r.score+'</div>';
      html += '</div>';
    }
    html += '</div></div>';
  }
  container.innerHTML = html;
  document.getElementById('timeDisplay').textContent = fmtTime(cutoffMs);
  // Re-bind click
  document.querySelectorAll('.node').forEach(n => {
    n.addEventListener('click', function(e){
      e.stopPropagation();
      document.getElementById('popBp').textContent = this.dataset.bp;
      document.getElementById('popRunId').textContent = this.dataset.runid;
      document.getElementById('popVersion').textContent = this.dataset.ver;
      document.getElementById('popStage').textContent = this.dataset.stage;
      document.getElementById('popScore').textContent = this.dataset.score;
      document.getElementById('popBench').textContent = this.dataset.bench;
      document.getElementById('popTime').textContent = fmtTime(new Date(this.dataset.ts).getTime());
      document.getElementById('detailPopup').classList.add('open');
      document.getElementById('overlay').classList.add('open');
    });
  });
}
// ============================================================
// 4. CONTROLS
// ============================================================
const slider = document.getElementById('timeSlider');
function updateFromSlider(){
  const frac = parseFloat(slider.value)/100;
  const ms = T0 + frac*SPAN;
  render(ms);
}
slider.addEventListener('input', updateFromSlider);
// Play
document.getElementById('playBtn').addEventListener('click', function(){
  if(playing){
    playing=false;
    this.textContent='PLAY';
    this.classList.remove('active');
    if(animFrame) cancelAnimationFrame(animFrame);
    return;
  }
  playing=true;
  this.textContent='STOP';
  this.classList.add('active');
  slider.value='0';
  playStartTime=performance.now();
  const dur=5000; // 5 sec full sweep
  function step(now){
    if(!playing) return;
    const elapsed=now-playStartTime;
    const frac=Math.min(elapsed/dur,1);
    slider.value=frac*100;
    const ms=T0+frac*SPAN;
    render(ms);
    if(frac<1){
      animFrame=requestAnimationFrame(step);
    }else{
      playing=false;
      document.getElementById('playBtn').textContent='PLAY';
      document.getElementById('playBtn').classList.remove('active');
    }
  }
  animFrame=requestAnimationFrame(step);
});
// Reset
document.getElementById('resetBtn').addEventListener('click', function(){
  if(playing){
    playing=false;
    document.getElementById('playBtn').textContent='PLAY';
    document.getElementById('playBtn').classList.remove('active');
    if(animFrame) cancelAnimationFrame(animFrame);
  }
  slider.value='100';
  render(T1);
});
// Popup close
document.getElementById('closePopup').addEventListener('click', function(){
  document.getElementById('detailPopup').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
});
document.getElementById('overlay').addEventListener('click', function(){
  document.getElementById('detailPopup').classList.remove('open');
  this.classList.remove('open');
});
// ============================================================
// 5. INIT
// ============================================================
render(T1);
</script>
</body>
</html>
```
280 lines. Self-contained HTML page. Open in browser.
WHAT IT DOES:
Parses an embedded dataset (simulating state.yaml output) of 15 blueprints spanning 7 days of agent runs
Renders horizontal timeline tracks — one row per blueprint with all its runs as nodes on a continuous path
Color coding per score tier:
- gold (#ffd700) = 85+: promoted / high-quality agents
- amber (#ff8c00) = 70-84: refinery, approaching threshold
- cool (#4a69bd) = < 70: early iterations, still training
Time scrubber at top with a range slider. Drag left/right to scrub from the first event to the last. Auto-play button sweeps the entire timeline in 5 seconds, showing the progression of agent quality over time. Stop button kills playback mid-sweep.
Click any node — popup appears with: run_id, version, stage (refinery/archive/production), score, benchmark metric, and timestamp. Overlay click or X closes it.
Stats bar at top: live counts of total agents, promoted, gold/amber/cool counts, updated on every scrub.
DATA SOURCE: the AGENT_DATA array at the top of the script mimics what a parsed state.yaml produces. In production, replace that with a fetch('/state.yaml') + YAML parse step. Structure mirrors real forge data: each blueprint has an array of runs with timestamps, scores, versions, stages, and benchmark names.
Styled dark terminal theme (#0a0e17 background, #00d2ff accents, monospace throughout) to match your forge aesthetic.