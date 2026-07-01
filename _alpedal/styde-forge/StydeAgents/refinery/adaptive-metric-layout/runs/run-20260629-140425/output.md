<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0f1117;color:#e1e4e8;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:20px;font-weight:600}
.controls{display:flex;gap:8px}
button{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:13px}
button:hover{background:#30363d}
button.reset{background:#da363320;border-color:#da3633;color:#f85149}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;align-items:start}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;transition:all .3s ease;position:relative;min-height:120px}
.panel.tier1{grid-column:span 2;min-height:200px}
.panel.tier2{grid-column:span 1;min-height:150px}
.panel.compact{min-height:48px;padding:8px 12px;font-size:12px;overflow:hidden}
.panel.compact .body,.panel.compact canvas{display:none}
.panel.compact .title{font-size:13px;margin-bottom:0}
.panel.locked{border-color:#58a6ff;box-shadow:0 0 0 1px #58a6ff40}
.title{font-size:14px;font-weight:600;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}
.meta{font-size:11px;color:#8b949e;display:flex;gap:8px}
.body{font-size:24px;font-weight:700;color:#58a6ff;margin:8px 0}
.spark{height:40px;background:linear-gradient(90deg,#23863620,#58a6ff40);border-radius:4px;margin-top:8px}
.actions{display:flex;gap:4px;opacity:0;transition:opacity .2s}
.panel:hover .actions{opacity:1}
.lock-btn,.expand-btn{background:none;border:none;color:#8b949e;cursor:pointer;font-size:14px;padding:2px 4px}
.lock-btn.locked{color:#58a6ff}
.score-badge{font-size:10px;padding:1px 6px;border-radius:10px;background:#21262d;color:#8b949e}
.score-badge.hot{background:#da363320;color:#f85149}
.legend{display:flex;gap:12px;margin-top:12px;font-size:11px;color:#8b949e}
.legend span{display:flex;align-items:center;gap:4px}
.legend .dot{width:8px;height:8px;border-radius:2px}
.legend .dot.t1{background:#58a6ff}
.legend .dot.t2{background:#3fb950}
.legend .dot.t3{background:#8b949e}
</style>
</head>
<body>
<header>
<h1>Adaptive Dashboard</h1>
<div class="controls">
<button onclick="AD.toggleAuto()" id="autoBtn">Auto: ON</button>
<button class="reset" onclick="AD.reset()">Reset</button>
</div>
</header>
<div class="grid" id="grid">
<div class="panel" data-id="cpu">
<div class="title">CPU Usage <span class="score-badge" id="scpu">—</span></div>
<div class="body">42%</div><div class="spark"></div>
<div class="meta">1m avg | 8 cores</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="cpu">&#128274;</button></div>
</div>
<div class="panel" data-id="memory">
<div class="title">Memory <span class="score-badge" id="smem">—</span></div>
<div class="body">7.2 GB</div><div class="spark"></div>
<div class="meta">of 16 GB | 45%</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="memory">&#128274;</button></div>
</div>
<div class="panel" data-id="requests">
<div class="title">Requests/s <span class="score-badge" id="sreq">—</span></div>
<div class="body">1,247</div><div class="spark"></div>
<div class="meta">+12% vs last hour</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="requests">&#128274;</button></div>
</div>
<div class="panel" data-id="errors">
<div class="title">Error Rate <span class="score-badge" id="serr">—</span></div>
<div class="body">0.03%</div><div class="spark"></div>
<div class="meta">3 errors last 5 min</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="errors">&#128274;</button></div>
</div>
<div class="panel" data-id="latency">
<div class="title">P99 Latency <span class="score-badge" id="slat">—</span></div>
<div class="body">142ms</div><div class="spark"></div>
<div class="meta">p50: 38ms | p95: 89ms</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="latency">&#128274;</button></div>
</div>
<div class="panel" data-id="throughput">
<div class="title">Throughput <span class="score-badge" id="sthr">—</span></div>
<div class="body">3.8 Gb/s</div><div class="spark"></div>
<div class="meta">in: 2.1 | out: 1.7</div>
<div class="actions"><button class="lock-btn" data-action="lock" data-panel="throughput">&#128274;</button></div>
</div>
</div>
<div class="legend">
<span><span class="dot t1"></span> Tier 1 (dominant)</span>
<span><span class="dot t2"></span> Tier 2 (active)</span>
<span><span class="dot t3"></span> Tier 3 (compact)</span>
<span>&#128274; = locked position</span>
</div>
<script>
(function(){
var STORE='ad_dash_v1', grid=document.getElementById('grid'), autoMode=true, state;
function load(){try{var d=localStorage.getItem(STORE);state=d?JSON.parse(d):{scores:{},locks:{},order:[]}}catch(e){state={scores:{},locks:{},order:[]}}initEach()}
function save(){try{localStorage.setItem(STORE,JSON.stringify(state))}catch(e){}}
function initEach(){var ids=[];grid.querySelectorAll('.panel').forEach(function(p){var id=p.dataset.id;ids.push(id);if(!state.scores[id])state.scores[id]={clicks:0,duration:0,lastSeen:0}}}state.order=state.order.length?state.order:ids;save()}
function recompute(){
var now=Date.now(),scored=[];
Object.keys(state.scores).forEach(function(id){
var s=state.scores[id],recency=Math.exp(-(now-s.lastSeen)/86400000);
var score=s.clicks*Math.max(s.duration,1)*recency;
scored.push({id:id,score:score,locked:!!state.locks[id]});
});
scored.sort(function(a,b){return b.score-a.score});
var locked=[],unlocked=[];
scored.forEach(function(x){if(x.locked)locked.push(x);else unlocked.push(x)});
var ranked=locked.concat(unlocked);
state.order=ranked.map(function(x){return x.id});
var tier1=2,tier2=3;
ranked.forEach(function(x,i){
var el=grid.querySelector('[data-id="'+x.id+'"]');
if(!el)return;
el.classList.remove('tier1','tier2','compact');
if(i<tier1)el.classList.add('tier1');
else if(i<tier1+tier2)el.classList.add('tier2');
else el.classList.add('compact');
if(x.locked)el.classList.add('locked');else el.classList.remove('locked');
var badge=document.getElementById('s'+x.id);if(badge){badge.textContent=Math.round(x.score);badge.classList.toggle('hot',i<tier1)}
});
applyOrder();
}
function applyOrder(){
var els=[],panels=grid.querySelectorAll('.panel');
state.order.forEach(function(id){var el=grid.querySelector('[data-id="'+id+'"]');if(el)els.push(el)});
els.forEach(function(el,i){el.style.order=i});
}
grid.addEventListener('click',function(e){
var btn=e.target.closest('[data-action="lock"]');
if(!btn)return;
var pid=btn.dataset.panel,el=grid.querySelector('[data-id="'+pid+'"]');
if(!el)return;
if(state.locks[pid]){delete state.locks[pid];el.classList.remove('locked');btn.classList.remove('locked');btn.innerHTML='&#128274;'}
else{state.locks[pid]=true;el.classList.add('locked');btn.classList.add('locked');btn.innerHTML='&#128275;'}
recompute();save();
});
grid.addEventListener('click',function(e){
var panel=e.target.closest('.panel');
if(!panel)return;var id=panel.dataset.id;if(!id)return;
state.scores[id].clicks=(state.scores[id].clicks||0)+1;
state.scores[id].lastSeen=Date.now();
recompute();save();
});
var observer=new IntersectionObserver(function(entries){
entries.forEach(function(entry){
var id=entry.target.dataset.id;if(!id||!state.scores[id])return;
if(entry.isIntersecting){
entry.target._visStart=Date.now();
entry.target._visInterval=setInterval(function(){
var elapsed=(Date.now()-entry.target._visStart)/1000;
state.scores[id].duration=(state.scores[id].duration||0)+elapsed;
entry.target._visStart=Date.now();
},10000);
}else{
if(entry.target._visInterval){clearInterval(entry.target._visInterval);entry.target._visInterval=null}
if(entry.target._visStart){
var elapsed=(Date.now()-entry.target._visStart)/1000;
state.scores[id].duration=(state.scores[id].duration||0)+elapsed;
}
save();
}
});
},{threshold:[0.3]});
grid.querySelectorAll('.panel').forEach(function(p){observer.observe(p)});
window.AD={toggleAuto:function(){autoMode=!autoMode;document.getElementById('autoBtn').textContent='Auto: '+(autoMode?'ON':'OFF');if(autoMode)recompute()},
reset:function(){state={scores:{},locks:{},order:[]};initEach();grid.querySelectorAll('.panel').forEach(function(p){p.classList.remove('tier1','tier2','compact','locked');p.style.order=''});save();recompute()}};
load();recompute();
setInterval(function(){if(autoMode)recompute()},30000);
})();
</script>
</body>
</html>