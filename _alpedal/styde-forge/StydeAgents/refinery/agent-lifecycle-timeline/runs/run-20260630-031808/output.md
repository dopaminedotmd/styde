```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}
#app{max-width:1400px;margin:0 auto}
h1{font-size:1.5rem;font-weight:600;margin-bottom:8px;color:#f0f6fc}
.subtitle{font-size:.85rem;color:#8b949e;margin-bottom:24px}
.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:24px;padding:16px;background:#161b22;border:1px solid #30363d;border-radius:8px}
.btn{padding:8px 18px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:.85rem;transition:.15s}
.btn:hover{background:#30363d;border-color:#8b949e}
.btn.primary{background:#238636;border-color:#2ea043;color:#fff}
.btn.primary:hover{background:#2ea043}
.btn:disabled{opacity:.4;cursor:default}
#file-input{display:none}
#file-label{padding:8px 18px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:.85rem}
#file-label:hover{background:#30363d}
.scrubber-wrap{flex:1;min-width:200px;display:flex;align-items:center;gap:12px}
.scrubber-wrap label{font-size:.8rem;color:#8b949e;white-space:nowrap}
.scrubber-wrap input[type=range]{flex:1;accent-color:#d29922;height:6px;cursor:pointer}
#time-display{font-size:.8rem;color:#8b949e;min-width:80px;text-align:right;font-variant-numeric:tabular-nums}
.stats{display:flex;gap:24px;margin-bottom:24px;flex-wrap:wrap}
.stat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 20px;flex:1;min-width:120px}
.stat-label{font-size:.75rem;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.stat-value{font-size:1.4rem;font-weight:600;color:#f0f6fc;margin-top:4px}
.timeline-wrap{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;overflow-x:auto;position:relative}
#timeline{width:100%;min-height:400px;display:block}
.track-label{font-size:.75rem;fill:#8b949e}
.node{cursor:pointer;transition:r .12s,opacity .12s}
.node:hover{r:6.5;opacity:1}
.node.muted{opacity:.3}
.tick-label{font-size:.65rem;fill:#484f58}
.grid-line{stroke:#21262d;stroke-width:1}
.popup-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6);z-index:1000;align-items:center;justify-content:center}
.popup-overlay.open{display:flex}
.popup{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:24px;max-width:440px;width:90%;max-height:80vh;overflow-y:auto;position:relative}
.popup h2{font-size:1.1rem;margin-bottom:16px;color:#f0f6fc}
.popup-close{position:absolute;top:12px;right:16px;background:none;border:none;color:#8b949e;font-size:1.4rem;cursor:pointer;padding:4px 8px;border-radius:4px}
.popup-close:hover{color:#f0f6fc;background:#30363d}
.popup table{width:100%;border-collapse:collapse}
.popup td{padding:6px 8px;border-bottom:1px solid #21262d;font-size:.85rem}
.popup td:first-child{color:#8b949e;width:100px}
.popup td:last-child{color:#f0f6fc}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:500}
.badge.hot{background:rgba(210,153,34,.2);color:#d29922;border:1px solid rgba(210,153,34,.3)}
.badge.amber{background:rgba(187,128,9,.2);color:#bb8009;border:1px solid rgba(187,128,9,.3)}
.badge.cool{background:rgba(48,54,61,.3);color:#8b949e;border:1px solid #30363d}
.toast{position:fixed;bottom:24px;right:24px;background:#21262d;border:1px solid #30363d;border-radius:8px;padding:12px 20px;font-size:.85rem;color:#8b949e;z-index:999;opacity:0;transition:opacity .25s;pointer-events:none}
.toast.show{opacity:1}
.loading{display:flex;align-items:center;justify-content:center;min-height:300px;color:#8b949e;font-size:.9rem}
.loading .spinner{width:24px;height:24px;border:3px solid #30363d;border-top-color:#d29922;border-radius:50%;animation:spin .8s linear infinite;margin-right:12px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div id="app">
<h1>Agent Lifecycle Timeline</h1>
<p class="subtitle">Interactive timeline showing every agent spawn, eval, improve, and promote cycle</p>
<div class="stats" id="stats">
<div class="stat"><div class="stat-label">Blueprints</div><div class="stat-value" id="stat-bps">—</div></div>
<div class="stat"><div class="stat-label">Total Agents</div><div class="stat-value" id="stat-agents">—</div></div>
<div class="stat"><div class="stat-label">Total Runs</div><div class="stat-value" id="stat-runs">—</div></div>
<div class="stat"><div class="stat-label">Promoted</div><div class="stat-value" id="stat-promoted">—</div></div>
</div>
<div class="controls">
<label id="file-label" for="file-input">Choose state.yaml</label>
<input type="file" id="file-input" accept=".yaml,.yml">
<button class="btn primary" id="btn-play" disabled>Play</button>
<button class="btn" id="btn-reset" disabled>Reset</button>
<div class="scrubber-wrap">
<label for="scrubber">Time</label>
<input type="range" id="scrubber" min="0" max="100" value="100" disabled>
<span id="time-display">—</span>
</div>
</div>
<div class="timeline-wrap" id="timeline-wrap">
<div class="loading" id="loading-msg"><div class="spinner"></div>Load a state.yaml file to begin</div>
<svg id="timeline" style="display:none"></svg>
</div>
</div>
<div class="popup-overlay" id="popup-overlay">
<div class="popup">
<button class="popup-close" id="popup-close">&times;</button>
<h2 id="popup-title">Agent Details</h2>
<table id="popup-body"></table>
</div>
</div>
<div class="toast" id="toast"></div>
<script>
const COLORS = {hot:'#d29922', amber:'#bb8009', cool:'#58a6ff'};
let state = null, runs = [], timestamps = [], playing = false, playInterval = null;
let currentTime = 0, maxTime = 0;
const svg = document.getElementById('timeline');
const wrap = document.getElementById('timeline-wrap');
const fileInput = document.getElementById('file-input');
const scrubber = document.getElementById('scrubber');
const timeDisplay = document.getElementById('time-display');
const btnPlay = document.getElementById('btn-play');
const btnReset = document.getElementById('btn-reset');
const loadingMsg = document.getElementById('loading-msg');
const popupOverlay = document.getElementById('popup-overlay');
const popupTitle = document.getElementById('popup-title');
const popupBody = document.getElementById('popup-body');
const toast = document.getElementById('toast');
function showToast(msg){toast.textContent=msg;toast.classList.add('show');setTimeout(()=>toast.classList.remove('show'),2500)}
function colorFor(s){if(s>=85)return COLORS.hot;if(s>=70)return COLORS.amber;return COLORS.cool}
function badgeFor(s){if(s>=85)return 'hot';if(s>=70)return 'amber';return 'cool'}
function fmtTime(ts){const d=new Date(ts);return d.toLocaleDateString()+' '+d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}
function fmtShort(ts){const d=new Date(ts);return d.toLocaleDateString([],{month:'short',day:'numeric'})}
fileInput.addEventListener('change', async function(e){
const file = e.target.files[0];
if(!file)return;
const text = await file.text();
try{
state = jsyaml.load(text);
if(!state || !state.agents){
showToast('state.yaml must contain an agents key');
return;
}
buildData();
render();
btnPlay.disabled=false;btnReset.disabled=false;scrubber.disabled=false;
loadingMsg.style.display='none';svg.style.display='block';
showToast('Loaded ' + Object.keys(state.agents).length + ' blueprints');
}catch(err){
showToast('Failed to parse YAML: ' + err.message);
}
fileInput.value='';
});
// Flatten state.agents into a sorted array of run events
function buildData(){
runs = [];
const agents = state.agents || {};
let bpCount=0,agentCount=0,runCount=0,promotedCount=0;
for(const [bp,bpData] of Object.entries(agents)){
bpCount++;
const bpAgents = bpData.agents || bpData;
if(!bpAgents||typeof bpAgents!=='object')continue;
for(const [agentId,agentData] of Object.entries(bpAgents)){
agentCount++;
const evals = agentData.evals || [];
const meta = agentData.meta || agentData;
const isPromoted = meta.promoted || agentData.promoted || false;
if(isPromoted)promotedCount++;
let version = parseInt(agentData.version||agentId.split('v')[1]||'1');
evals.forEach((ev,i)=>{
if(!ev||!ev.timestamp)return;
runCount++;
const score = ev.score!==undefined?ev.score:(ev.eval_score||ev.accuracy||0);
runs.push({
id: agentId,
blueprint: bp,
version: version,
stage: i===0?'spawn':(i===evals.length-1?'eval':'improve'),
score: score,
timestamp: new Date(ev.timestamp).getTime(),
benchmark: ev.benchmark||ev.bench||'—',
run_id: ev.run_id||ev.id||(agentId+'-r'+i),
full: ev,
promoted: isPromoted,
index: i,
total: evals.length
});
});
}
}
document.getElementById('stat-bps').textContent=bpCount;
document.getElementById('stat-agents').textContent=agentCount;
document.getElementById('stat-runs').textContent=runCount;
document.getElementById('stat-promoted').textContent=promotedCount;
runs.sort((a,b)=>a.timestamp-b.timestamp);
timestamps = runs.map(r=>r.timestamp);
maxTime = timestamps.length-1;
scrubber.max = maxTime;
scrubber.value = maxTime;
currentTime = maxTime;
updateTimeDisplay(maxTime);
}
function updateTimeDisplay(idx){
if(!runs.length){timeDisplay.textContent='—';return;}
const t = runs[idx]?.timestamp;
timeDisplay.textContent = t?fmtTime(t):'—';
}
// Get visible runs at current scrub position
function visibleRuns(at){
const t = runs[at]?.timestamp||Infinity;
return runs.filter(r=>r.timestamp<=t);
}
function render(){
const v = visibleRuns(currentTime);
const bpMap = {};
v.forEach(r=>{
if(!bpMap[r.blueprint])bpMap[r.blueprint]=[];
bpMap[r.blueprint].push(r);
});
const bpNames = Object.keys(bpMap).sort();
const MARGIN={top:30,right:40,bottom:50,left:220};
const TRACK_H=36;
const h = MARGIN.top+MARGIN.bottom+bpNames.length*TRACK_H;
const w = wrap.clientWidth||1000;
const innerW = w-MARGIN.left-MARGIN.right;
const minT = runs.length?runs[0].timestamp:0;
const maxT = runs.length?runs[currentTime]?.timestamp||runs[runs.length-1].timestamp:0;
const tRange = Math.max(maxT-minT,1);
svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
svg.innerHTML='';
// Grid lines (5 ticks)
for(let i=0;i<=5;i++){
const x = MARGIN.left+(innerW/5)*i;
const t = minT+(tRange/5)*i;
const line = document.createElementNS('http://www.w3.org/2000/svg','line');
line.setAttribute('class','grid-line');
line.setAttribute('x1',x);line.setAttribute('y1',MARGIN.top);
line.setAttribute('x2',x);line.setAttribute('y2',h-MARGIN.bottom);
svg.appendChild(line);
const lbl = document.createElementNS('http://www.w3.org/2000/svg','text');
lbl.setAttribute('class','tick-label');
lbl.setAttribute('x',x);lbl.setAttribute('y',h-12);
lbl.setAttribute('text-anchor','middle');
lbl.textContent=fmtShort(t);
svg.appendChild(lbl);
}
// Tracks
bpNames.forEach((bp,i)=>{
const y = MARGIN.top+i*TRACK_H+TRACK_H/2;
const lbl = document.createElementNS('http://www.w3.org/2000/svg','text');
lbl.setAttribute('class','track-label');
lbl.setAttribute('x',MARGIN.left-10);
lbl.setAttribute('y',y);
lbl.setAttribute('text-anchor','end');
lbl.setAttribute('dominant-baseline','central');
let label=bp.length>30?bp.slice(0,27)+'...':bp;
lbl.textContent=label;
svg.appendChild(lbl);
// Track line
const line = document.createElementNS('http://www.w3.org/2000/svg','line');
line.setAttribute('stroke','#21262d');line.setAttribute('stroke-width','2');
line.setAttribute('x1',MARGIN.left);line.setAttribute('y1',y);
line.setAttribute('x2',MARGIN.left+innerW);line.setAttribute('y2',y);
svg.appendChild(line);
// Nodes
const arr = bpMap[bp];
arr.forEach((r,j)=>{
const frac = (r.timestamp-minT)/tRange;
const cx = MARGIN.left+frac*innerW;
const col = colorFor(r.score);
const node = document.createElementNS('http://www.w3.org/2000/svg','circle');
node.setAttribute('class','node');
node.setAttribute('cx',cx);
node.setAttribute('cy',y);
node.setAttribute('r','5');
node.setAttribute('fill',col);
node.setAttribute('stroke','#0d1117');
node.setAttribute('stroke-width','1.5');
node.setAttribute('data-idx',runs.indexOf(r));
svg.appendChild(node);
// Promote marker
if(r.promoted&&r.stage==='eval'){
const diamond = document.createElementNS('http://www.w3.org/2000/svg','polygon');
const sz=7;
const pts=`${cx},${y-sz} ${cx+sz},${y} ${cx},${y+sz} ${cx-sz},${y}`;
diamond.setAttribute('points',pts);
diamond.setAttribute('fill','none');
diamond.setAttribute('stroke','#3fb950');
diamond.setAttribute('stroke-width','2');
diamond.setAttribute('data-idx',runs.indexOf(r));
svg.appendChild(diamond);
}
// Connect consecutive nodes for same agent
if(j>0){
const prev = arr[j-1];
if(prev.id===r.id){
const fracP = (prev.timestamp-minT)/tRange;
const cxP = MARGIN.left+fracP*innerW;
const conn = document.createElementNS('http://www.w3.org/2000/svg','line');
conn.setAttribute('x1',cxP);conn.setAttribute('y1',y);
conn.setAttribute('x2',cx);conn.setAttribute('y2',y);
conn.setAttribute('stroke','#30363d');conn.setAttribute('stroke-width','1.5');
conn.setAttribute('stroke-dasharray','3,3');
svg.insertBefore(conn,svg.firstChild);
}
}
});
});
}
// Click handler (delegated)
svg.addEventListener('click',function(e){
const target=e.target.closest('.node,[data-idx]');
if(!target)return;
const idx=parseInt(target.getAttribute('data-idx'));
if(isNaN(idx)||!runs[idx])return;
const r=runs[idx];
popupTitle.textContent=r.id+' — '+r.blueprint.slice(0,40);
popupBody.innerHTML=`
<tr><td>Run ID</td><td>${r.run_id}</td></tr>
<tr><td>Blueprint</td><td>${r.blueprint}</td></tr>
<tr><td>Version</td><td>v${r.version}</td></tr>
<tr><td>Stage</td><td>${r.stage}</td></tr>
<tr><td>Score</td><td><span class="badge ${badgeFor(r.score)}">${r.score}</span></td></tr>
<tr><td>Timestamp</td><td>${fmtTime(r.timestamp)}</td></tr>
<tr><td>Benchmark</td><td>${r.benchmark}</td></tr>
<tr><td>Promoted</td><td>${r.promoted?'Yes':'No'}</td></tr>
`;
popupOverlay.classList.add('open');
});
popupOverlay.addEventListener('click',function(e){
if(e.target===popupOverlay||e.target.closest('.popup-close'))popupOverlay.classList.remove('open');
});
// Scrubber
scrubber.addEventListener('input',function(){
currentTime=parseInt(this.value);
updateTimeDisplay(currentTime);
render();
});
// Play
btnPlay.addEventListener('click',function(){
if(playing){
clearInterval(playInterval);playing=false;btnPlay.textContent='Play';return;
}
playing=true;btnPlay.textContent='Pause';
let idx=0;
playInterval=setInterval(()=>{
if(idx>maxTime){clearInterval(playInterval);playing=false;btnPlay.textContent='Play';return;}
scrubber.value=idx;currentTime=idx;
updateTimeDisplay(idx);render();
idx++;
},200);
});
// Reset
btnReset.addEventListener('click',function(){
if(playing){clearInterval(playInterval);playing=false;btnPlay.textContent='Play';}
currentTime=maxTime;scrubber.value=maxTime;
updateTimeDisplay(maxTime);render();
});
window.addEventListener('resize',()=>{if(runs.length)render()});
</script>
</body>
</html>
```