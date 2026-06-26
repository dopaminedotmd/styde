<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Styde Forge — Core Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0a0e;--surface:#121216;--surface2:#1a1a22;--border:#2a2a36;--accent:#ff6b35;--accent2:#ffd23f;--accent3:#4cc9f0;--text:#e8e8ee;--text2:#9090a0;--red:#ef4444;--green:#22c55e;--amber:#f59e0b;--radius:4px;--font:'Segoe UI','Helvetica Neue',Arial,sans-serif;--mono:'SF Mono','Cascadia Code','Consolas',monospace}
html{font-size:16px}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;line-height:1.5}
.loading-body{display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:1rem}
.loading-body .forge-logo-pulse{width:60px;height:60px;border:3px solid var(--accent);border-radius:50%;animation:pulse-ring 1.5s ease-in-out infinite;display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--accent2)}
@keyframes pulse-ring{0%{box-shadow:0 0 0 0 rgba(255,107,53,.6)}70%{box-shadow:0 0 0 20px rgba(255,107,53,0)}100%{box-shadow:0 0 0 0 rgba(255,107,53,0)}}
.loading-body.loaded{opacity:0;transition:opacity .4s;pointer-events:none}
.app-wrapper{display:none;flex-direction:column;min-height:100vh}
.app-wrapper.visible{display:flex}
/* HEADER */
.header{background:linear-gradient(135deg,#121216 0%,#1a1a22 50%,#121216 100%);border-bottom:2px solid var(--accent);display:flex;align-items:center;padding:0 1.25rem;height:56px;position:sticky;top:0;z-index:100;gap:.75rem}
.header-logo{display:flex;align-items:center;gap:.5rem;font-weight:700;font-size:1.15rem;letter-spacing:.02em}
.header-logo .forge-icon{width:28px;height:28px;background:var(--accent);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:700;flex-shrink:0}
.header-status{display:flex;align-items:center;gap:.35rem;margin-left:auto;font-size:.75rem;color:var(--text2)}
.header-status .dot{width:8px;height:8px;border-radius:50%;background:var(--green);animation:dot-breathe 2s ease-in-out infinite}
@keyframes dot-breathe{0%,100%{opacity:1}50%{opacity:.35}}
.hamburger{display:none;background:none;border:none;color:var(--text);font-size:1.5rem;cursor:pointer;padding:.25rem}
/* NAV */
.nav-bar{background:var(--surface);border-bottom:1px solid var(--border);display:flex;gap:0;overflow-x:auto;padding:0 .5rem}
.nav-bar a{color:var(--text2);text-decoration:none;padding:.65rem 1rem;font-size:.82rem;white-space:nowrap;border-bottom:2px solid transparent;transition:color .2s,border-color .2s;display:flex;align-items:center;gap:.35rem}
.nav-bar a:hover,.nav-bar a.active{color:var(--accent);border-bottom-color:var(--accent)}
.nav-bar a.active{color:var(--accent2);border-bottom-color:var(--accent2)}
/* MAIN */
.main{flex:1;padding:1.25rem;max-width:1440px;margin:0 auto;width:100%}
.breadcrumb{font-size:.75rem;color:var(--text2);margin-bottom:1rem;display:flex;gap:.35rem;flex-wrap:wrap}
.breadcrumb a{color:var(--accent3);text-decoration:none}
.breadcrumb a:hover{text-decoration:underline}
.breadcrumb span{color:var(--text2)}
/* GRID */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;margin-bottom:1.5rem}
.grid-2{grid-template-columns:repeat(auto-fill,minmax(400px,1fr))}
.grid-4{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;position:relative}
.card::before{content:'';position:absolute;top:-1px;left:1rem;right:1rem;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:.5}
.card-title{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text2);margin-bottom:.5rem;display:flex;align-items:center;gap:.4rem}
.card-value{font-size:1.6rem;font-weight:700;font-family:var(--mono);line-height:1.2}
.card-value .unit{font-size:.75rem;font-weight:400;color:var(--text2);font-family:var(--font)}
.card-label{font-size:.7rem;color:var(--text2);margin-top:.15rem}
/* FORGE METER */
.forge-meter{display:flex;align-items:center;gap:.5rem;margin-top:.4rem}
.forge-meter .track{flex:1;height:4px;background:var(--surface2);border-radius:2px;overflow:hidden}
.forge-meter .fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--accent2),var(--accent));transition:width .6s ease}
/* AGENT LIST */
.agent-list{display:flex;flex-direction:column;gap:.35rem;max-height:280px;overflow-y:auto}
.agent-item{display:flex;align-items:center;gap:.6rem;padding:.4rem .5rem;background:var(--surface2);border-radius:3px;font-size:.8rem;transition:background .2s}
.agent-item:hover{background:#22222e}
.agent-item .status-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.agent-item .status-dot.on{background:var(--green);box-shadow:0 0 6px rgba(34,197,94,.4)}
.agent-item .status-dot.off{background:var(--red)}
.agent-item .status-dot.busy{background:var(--amber);animation:pulse-ring 2s infinite}
.agent-name{flex:1;font-family:var(--mono);font-size:.78rem}
.agent-meta{font-size:.65rem;color:var(--text2)}
/* ACTIVITY FEED */
.activity-feed{max-height:300px;overflow-y:auto;display:flex;flex-direction:column;gap:2px}
.activity-entry{display:flex;gap:.5rem;padding:.35rem .4rem;font-size:.75rem;font-family:var(--mono);border-bottom:1px solid rgba(42,42,54,.4)}
.activity-entry .time{color:var(--text2);flex-shrink:0;width:60px}
.activity-entry .msg{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.activity-entry .level{width:10px;flex-shrink:0;text-align:center}
.activity-entry.info .level{color:var(--accent3)}
.activity-entry.warn .level{color:var(--amber)}
.activity-entry.err .level{color:var(--red)}
.activity-entry.ok .level{color:var(--green)}
/* GPU CARDS */
.gpu-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.75rem}
.gpu-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:.85rem;position:relative}
.gpu-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;border-radius:0 0 3px 3px;background:var(--accent);opacity:.3;transition:opacity .4s}
.gpu-card:hover::after{opacity:.8}
.gpu-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem}
.gpu-name{font-size:.75rem;font-weight:600;font-family:var(--mono)}
.gpu-temp{font-size:.7rem;color:var(--text2)}
.gpu-value{font-size:1.3rem;font-weight:700;font-family:var(--mono)}
.gpu-stat{display:flex;justify-content:space-between;font-size:.7rem;color:var(--text2);margin-top:.25rem}
/* COLLAPSIBLE */
.collapsible-panel .panel-toggle{display:flex;align-items:center;gap:.35rem;cursor:pointer;background:none;border:none;color:var(--text);font-size:.8rem;font-weight:600;padding:.35rem 0;width:100%;text-align:left;font-family:var(--font)}
.collapsible-panel .panel-toggle .arrow{transition:transform .25s;font-size:.65rem}
.collapsible-panel.collapsed .panel-toggle .arrow{transform:rotate(-90deg)}
.collapsible-panel .panel-body{max-height:600px;overflow:hidden;transition:max-height .35s ease}
.collapsible-panel.collapsed .panel-body{max-height:0}
.collapsible-panel .panel-body-inner{padding-top:.5rem}
/* FOOTER */
.footer{background:var(--surface);border-top:1px solid var(--border);padding:1rem 1.25rem;text-align:center;font-size:.72rem;color:var(--text2);display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap}
.footer a{color:var(--text2);text-decoration:none}
.footer a:hover{color:var(--accent)}
/* STATES */
.state-empty,.state-error,.state-loading{padding:1.5rem;text-align:center;color:var(--text2);font-size:.8rem}
.state-error{color:var(--red)}
.state-loading .spark{display:inline-block;width:12px;height:12px;border:2px solid var(--accent);border-radius:50%;border-top-color:transparent;animation:spin .8s linear infinite;margin-bottom:.5rem}
@keyframes spin{to{transform:rotate(360deg)}}
/* EMPTY STATE ICON */
.empty-icon{font-size:1.8rem;opacity:.3;margin-bottom:.25rem}
/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
/* RESPONSIVE */
@media(max-width:768px){
  .hamburger{display:block}
  .nav-bar{display:none}
  .nav-bar.open{display:flex;flex-direction:column;position:absolute;top:56px;left:0;right:0;background:var(--surface);border-bottom:1px solid var(--border);z-index:99}
  .grid-2{grid-template-columns:1fr}
  .grid-4{grid-template-columns:repeat(2,1fr)}
  .gpu-grid{grid-template-columns:1fr}
  .header{padding:0 .75rem}
  .main{padding:.9rem}
}
@media(min-width:769px)and(max-width:1024px){
  .gpu-grid{grid-template-columns:repeat(2,1fr)}
}
/* FORGE GLOW ANIMATION */
@keyframes forge-glow{0%,100%{opacity:.3}50%{opacity:.7}}
.glow-pulse{animation:forge-glow 3s ease-in-out infinite}
/* RIVET DOT */
.rivet{display:inline-block;width:4px;height:4px;background:var(--accent);border-radius:50%;margin:0 4px;opacity:.4}
</style>
</head>
<body>
<div id="app-loading" class="loading-body" role="status" aria-label="Loading Styde Forge Dashboard">
  <div class="forge-logo-pulse" aria-hidden="true">F</div>
  <span style="font-size:.8rem;color:var(--text2)">kindling forge...</span>
</div>
<div id="app" class="app-wrapper" role="application">
  <header class="header">
    <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation menu" aria-expanded="false">☰</button>
    <div class="header-logo">
      <div class="forge-icon" aria-hidden="true">F</div>
      <span>Styde Forge</span>
      <span class="rivet" aria-hidden="true"></span>
      <span class="rivet" aria-hidden="true"></span>
      <span class="rivet" aria-hidden="true"></span>
    </div>
    <div class="header-status" aria-live="polite">
      <span class="dot" aria-hidden="true"></span>
      <span>All Systems Nominal</span>
    </div>
  </header>
  <nav class="nav-bar" id="mainNav" aria-label="Main navigation">
    <a href="#" class="active" data-section="dashboard" aria-current="page">Dashboard</a>
    <a href="#" data-section="agents">Agents</a>
    <a href="#" data-section="gpu">GPU Farm</a>
    <a href="#" data-section="forge">Forge</a>
    <a href="#" data-section="activity">Activity</a>
    <a href="#" data-section="settings">Settings</a>
  </nav>
  <main class="main">
    <div class="breadcrumb">
      <a href="#">Styde</a><span>/</span><span>Forge</span><span>/</span><span>Dashboard</span>
    </div>
    <h2 style="font-size:1.1rem;font-weight:600;margin-bottom:1rem;letter-spacing:.01em">Forge Core Dashboard</h2>
    <!-- METRIC CARDS ROW -->
    <div class="grid grid-4" id="metricsGrid" aria-label="System metrics">
      <div class="card" id="metric-cpu" data-metric="cpu">
        <div class="card-title"><span aria-hidden="true">⚙</span> CPU Load</div>
        <div class="card-value" id="cpu-value">--<span class="unit">%</span></div>
        <div class="forge-meter"><div class="track"><div class="fill" id="cpu-fill" style="width:0%"></div></div></div>
        <div class="card-label" id="cpu-label">fetching...</div>
      </div>
      <div class="card" id="metric-mem" data-metric="mem">
        <div class="card-title"><span aria-hidden="true">▦</span> Memory</div>
        <div class="card-value" id="mem-value">--<span class="unit"> GB</span></div>
        <div class="forge-meter"><div class="track"><div class="fill" id="mem-fill" style="width:0%"></div></div></div>
        <div class="card-label" id="mem-label">fetching...</div>
      </div>
      <div class="card" id="metric-disk" data-metric="disk">
        <div class="card-title"><span aria-hidden="true">◫</span> Disk</div>
        <div class="card-value" id="disk-value">--<span class="unit"> TB</span></div>
        <div class="forge-meter"><div class="track"><div class="fill" id="disk-fill" style="width:0%"></div></div></div>
        <div class="card-label" id="disk-label">fetching...</div>
      </div>
      <div class="card" id="metric-uptime" data-metric="uptime">
        <div class="card-title"><span aria-hidden="true">◷</span> Uptime</div>
        <div class="card-value" id="uptime-value">--<span class="unit"> h</span></div>
        <div class="card-label" id="uptime-label">since last restart</div>
      </div>
    </div>
    <!-- AGENTS + ACTIVITY ROW -->
    <div class="grid grid-2" style="margin-bottom:1.5rem">
      <!-- AGENTS PANEL (collapsible) -->
      <section class="card collapsible-panel" id="agentsPanel" aria-label="Agent Status">
        <button class="panel-toggle" id="agentsToggle" aria-expanded="true" aria-controls="agentsBody">
          <span class="arrow" aria-hidden="true">▼</span> Running Agents
          <span style="margin-left:auto;font-size:.7rem;color:var(--text2);font-family:var(--mono)" id="agentCount">0 online</span>
        </button>
        <div class="panel-body" id="agentsBody" role="region" aria-labelledby="agentsToggle">
          <div class="panel-body-inner">
            <div class="state-loading" id="agentsLoading" role="status">
              <div class="spark" aria-hidden="true"></div>
              <div>loading agents...</div>
            </div>
            <div class="state-empty" id="agentsEmpty" style="display:none">
              <div class="empty-icon" aria-hidden="true">∅</div>
              <div>no agents registered</div>
            </div>
            <div class="state-error" id="agentsError" style="display:none">
              <div class="empty-icon" aria-hidden="true">⚠</div>
              <div>could not reach agent registry</div>
            </div>
            <div class="agent-list" id="agentList" style="display:none" role="list"></div>
          </div>
        </div>
      </section>
      <!-- ACTIVITY FEED (collapsible) -->
      <section class="card collapsible-panel" id="activityPanel" aria-label="Activity Feed">
        <button class="panel-toggle" id="activityToggle" aria-expanded="true" aria-controls="activityBody">
          <span class="arrow" aria-hidden="true">▼</span> Activity Feed
        </button>
        <div class="panel-body" id="activityBody" role="region" aria-labelledby="activityToggle">
          <div class="panel-body-inner">
            <div class="state-loading" id="activityLoading" role="status">
              <div class="spark" aria-hidden="true"></div>
              <div>loading feed...</div>
            </div>
            <div class="state-empty" id="activityEmpty" style="display:none">
              <div class="empty-icon" aria-hidden="true">∅</div>
              <div>no recent activity</div>
            </div>
            <div class="state-error" id="activityError" style="display:none">
              <div class="empty-icon" aria-hidden="true">⚠</div>
              <div>feed connection failed</div>
            </div>
            <div class="activity-feed" id="activityFeed" style="display:none" role="log" aria-live="off"></div>
          </div>
        </div>
      </section>
    </div>
    <!-- GPU MONITOR (collapsible) -->
    <section class="card collapsible-panel" id="gpuPanel" aria-label="GPU Monitor" style="margin-bottom:1.5rem">
      <button class="panel-toggle" id="gpuToggle" aria-expanded="true" aria-controls="gpuBody">
        <span class="arrow" aria-hidden="true">▼</span> GPU Farm Monitor
        <span style="margin-left:auto;font-size:.7rem;color:var(--text2);font-family:var(--mono)" id="gpuCount">0 GPUs</span>
      </button>
      <div class="panel-body" id="gpuBody" role="region" aria-labelledby="gpuToggle">
        <div class="panel-body-inner">
          <div class="state-loading" id="gpuLoading" role="status">
            <div class="spark" aria-hidden="true"></div>
            <div>probing GPU farm...</div>
          </div>
          <div class="state-empty" id="gpuEmpty" style="display:none">
            <div class="empty-icon" aria-hidden="true">∅</div>
            <div>no GPUs detected</div>
          </div>
          <div class="state-error" id="gpuError" style="display:none">
            <div class="empty-icon" aria-hidden="true">⚠</div>
            <div>GPU interface unavailable</div>
          </div>
          <div class="gpu-grid" id="gpuGrid" style="display:none" role="list"></div>
        </div>
      </div>
    </section>
    <!-- QUICK METRICS -->
    <div class="grid grid-4" id="quickMetrics" aria-label="Performance metrics">
      <div class="card">
        <div class="card-title"><span aria-hidden="true">⇄</span> Throughput</div>
        <div class="card-value" id="metric-tput">--<span class="unit"> r/s</span></div>
        <div class="card-label" id="tput-trend">awaiting data</div>
      </div>
      <div class="card">
        <div class="card-title"><span aria-hidden="true">⏱</span> Avg Latency</div>
        <div class="card-value" id="metric-lat">--<span class="unit"> ms</span></div>
        <div class="card-label" id="lat-trend">awaiting data</div>
      </div>
      <div class="card">
        <div class="card-title"><span aria-hidden="true">✕</span> Error Rate</div>
        <div class="card-value" id="metric-err">--<span class="unit"> %</span></div>
        <div class="card-label" id="err-trend">awaiting data</div>
      </div>
      <div class="card">
        <div class="card-title"><span aria-hidden="true">✓</span> Success Rate</div>
        <div class="card-value" id="metric-succ">--<span class="unit"> %</span></div>
        <div class="card-label" id="succ-trend">awaiting data</div>
      </div>
    </div>
  </main>
  <footer class="footer">
    <span>&copy; 2026 Styde AB</span>
    <a href="#">Forge Docs</a>
    <a href="#">Agent API</a>
    <a href="#">System Health</a>
    <a href="#">Status Page</a>
  </footer>
</div>
<script>
(function(){
'use strict';
const AGENTS=[
{name:'refinery-01',status:'on',task:'fine-tune Qwen 2.5 7B',uptime:'12h'},
{name:'refinery-02',status:'on',task:'data dedup pass 3',uptime:'8h'},
{name:'production-01',status:'busy',task:'batch eval: 42/120',uptime:'4h'},
{name:'production-02',status:'on',task:'idle — awaiting queue',uptime:'2h'},
{name:'monitor-01',status:'on',task:'watchdog active',uptime:'36h'},
{name:'cache-01',status:'off',task:'offline',uptime:'0h'}
];
const ACTIVITY_LOG=[
{t:'14:32:17',m:'refinery-01 checkpoint saved — step 4800',l:'ok'},
{t:'14:31:05',m:'eval batch 3 complete: 94.2% pass',l:'ok'},
{t:'14:29:44',m:'GPU-04 temp spike 82°C — throttling engaged',l:'warn'},
{t:'14:28:10',m:'production-01 dequeued job forge-eval-v7',l:'info'},
{t:'14:26:33',m:'cache-01 heartbeat missed — restart queued',l:'err'},
{t:'14:25:01',m:'memory pool cleanup freed 3.2GB',l:'info'},
{t:'14:23:18',m:'throughput 142 req/s — peak surge',l:'info'},
{t:'14:21:40',m:'forge pipeline: blueprint v46 promoted to prod',l:'ok'},
{t:'14:19:55',m:'GPU-02 memory 19.8/24 GB — 82% util',l:'warn'},
{t:'14:18:12',m:'refinery-02 iteration 1200 — loss 0.023',l:'info'}
];
const GPU_NAMES=['RTX 4090','RTX 4090','RTX 4080','A100 80G','A100 80G','RTX 3090'];
const GPU_BASE_TEMP=[68,65,72,62,60,74];
const GPU_BASE_POWER=[145,150,120,185,180,110];
const GPU_BASE_MEM=[24,24,16,80,80,24];
const GPU_BASE_UTIL=[78,62,45,55,70,38];
let gpuData=GPU_NAMES.map((name,i)=>({
name:name,
temp:GPU_BASE_TEMP[i]+Math.round(Math.random()*6-3),
power:GPU_BASE_POWER[i]+Math.round(Math.random()*10-5),
mem:Math.round(GPU_BASE_MEM[i]*(0.3+Math.random()*0.4)*10)/10,
util:Math.min(100,Math.max(10,GPU_BASE_UTIL[i]+Math.round(Math.random()*16-8)))
}));
function pad(n){return n<10?'0'+n:''+n}
function formatUptime(h){var d=Math.floor(h/24);var r=Math.round(h%24);return d>0?d+'d '+r+'h':r+'h'}
function deg(dir){return dir||'N/A'}
const intervalMgr={_registry:{},_timers:{},register:function(key,fn,ms,id){if(!this._registry[key])this._registry[key]=[];var entry={fn:fn,ms:ms,id:id||null};this._registry[key].push(entry);return entry},start:function(key){var self=this;if(this._timers[key])return;var entries=this._registry[key];if(!entries||!entries.length)return;var timer=setInterval(function(){var v=document.visibilityState==='visible';entries.forEach(function(e){if(v||!e.id||document.getElementById(e.id)){try{e.fn()}catch(ex){console.warn('timer err:',ex)}}})},entries[0].ms);this._timers[key]=timer},stop:function(key){if(this._timers[key]){clearInterval(this._timers[key]);delete this._timers[key]}},stopAll:function(){var self=this;Object.keys(this._timers).forEach(function(k){self.stop(k)})},restart:function(key){this.stop(key);this.start(key)}};
function collapsibleSetup(toggleId,bodyId,panelId){
function init(){
var toggle=document.getElementById(toggleId);
var body=document.getElementById(bodyId);
var panel=document.getElementById(panelId);
if(!toggle||!body||!panel)return;
var isOpen=true;
toggle.addEventListener('click',function(){
isOpen=!isOpen;
panel.classList.toggle('collapsed',!isOpen);
toggle.setAttribute('aria-expanded',isOpen?'true':'false');
});
panel.classList.remove('collapsed');
toggle.setAttribute('aria-expanded','true');
}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init)}else{init()}
}
function populateAgents(){
var list=document.getElementById('agentList');
var loading=document.getElementById('agentsLoading');
var empty=document.getElementById('agentsEmpty');
var error=document.getElementById('agentsError');
var count=document.getElementById('agentCount');
if(!list||!loading||!empty||!error||!count)return;
try{
loading.style.display='none';
empty.style.display='none';
error.style.display='none';
if(!AGENTS||AGENTS.length===0){
empty.style.display='block';
count.textContent='0 online';
return;
}
list.style.display='flex';
var frag=document.createDocumentFragment();
AGENTS.forEach(function(a){
var item=document.createElement('div');
item.className='agent-item';
item.setAttribute('role','listitem');
var dot=document.createElement('span');
dot.className='status-dot '+a.status;
dot.setAttribute('aria-hidden','true');
item.appendChild(dot);
var name=document.createElement('span');
name.className='agent-name';
name.textContent=a.name;
item.appendChild(name);
var meta=document.createElement('span');
meta.className='agent-meta';
meta.textContent=a.task+(a.uptime?(' · '+a.uptime):'');
item.appendChild(meta);
frag.appendChild(item);
});
list.innerHTML='';
list.appendChild(frag);
var on=AGENTS.filter(function(a){return a.status==='on'}).length;
var busy=AGENTS.filter(function(a){return a.status==='busy'}).length;
count.textContent=on+' on, '+busy+' busy';
}catch(ex){
loading.style.display='none';
error.style.display='block';
error.textContent='could not load agents: '+ex.message;
count.textContent='error';
}
}
function populateActivity(){
var feed=document.getElementById('activityFeed');
var loading=document.getElementById('activityLoading');
var empty=document.getElementById('activityEmpty');
var error=document.getElementById('activityError');
if(!feed||!loading||!empty||!error)return;
try{
loading.style.display='none';
empty.style.display='none';
error.style.display='none';
if(!ACTIVITY_LOG||ACTIVITY_LOG.length===0){
empty.style.display='block';
return;
}
feed.style.display='flex';
var frag=document.createDocumentFragment();
ACTIVITY_LOG.forEach(function(e){
var entry=document.createElement('div');
entry.className='activity-entry '+e.l;
var time=document.createElement('span');
time.className='time';
time.textContent=e.t;
entry.appendChild(time);
var lvl=document.createElement('span');
lvl.className='level';
var icons={info:'i',warn:'!',err:'✕',ok:'✓'};
lvl.textContent=icons[e.l]||'·';
entry.appendChild(lvl);
var msg=document.createElement('span');
msg.className='msg';
msg.textContent=e.m;
entry.appendChild(msg);
frag.appendChild(entry);
});
feed.innerHTML='';
feed.appendChild(frag);
}catch(ex){
loading.style.display='none';
error.style.display='block';
error.textContent='feed error: '+ex.message;
}
}
function renderGPUs(){
var grid=document.getElementById('gpuGrid');
var loading=document.getElementById('gpuLoading');
var empty=document.getElementById('gpuEmpty');
var error=document.getElementById('gpuError');
var count=document.getElementById('gpuCount');
if(!grid||!loading||!empty||!error||!count)return;
try{
loading.style.display='none';
empty.style.display='none';
error.style.display='none';
if(!gpuData||gpuData.length===0){
empty.style.display='block';
count.textContent='0 GPUs';
return;
}
grid.style.display='grid';
var frag=document.createDocumentFragment();
gpuData.forEach(function(g,i){
var card=document.createElement('div');
card.className='gpu-card';
card.setAttribute('role','listitem');
card.setAttribute('aria-label',g.name+' temp '+g.temp+'C util '+g.util+'%');
var header=document.createElement('div');
header.className='gpu-header';
var name=document.createElement('span');
name.className='gpu-name';
name.textContent=g.name+' #'+(i+1);
header.appendChild(name);
var temp=document.createElement('span');
temp.className='gpu-temp';
var tColor=g.temp>80?'var(--red)':g.temp>70?'var(--amber)':'var(--text2)';
temp.style.color=tColor;
temp.textContent=g.temp+'\u00B0C';
header.appendChild(temp);
card.appendChild(header);
var val=document.createElement('div');
val.className='gpu-value';
val.textContent=g.util+'%';
val.style.color=g.util>85?'var(--red)':g.util>65?'var(--amber)':'var(--green)';
card.appendChild(val);
var stat=document.createElement('div');
stat.className='gpu-stat';
var pw=document.createElement('span');
pw.textContent=g.power+'W';
var mem=document.createElement('span');
mem.textContent=g.mem+'GB';
stat.appendChild(pw);
stat.appendChild(mem);
card.appendChild(stat);
card.style.setProperty('--bar-color',g.temp>80?'var(--red)':g.temp>70?'var(--amber)':'var(--green)');
card.querySelector('::after')&&false;
frag.appendChild(card);
});
grid.innerHTML='';
grid.appendChild(frag);
count.textContent=gpuData.length+' GPUs';
}catch(ex){
loading.style.display='none';
error.style.display='block';
error.textContent='GPU render error: '+ex.message;
count.textContent='error';
}
}
function updateMetrics(){
try{
var cpuEl=document.getElementById('cpu-value');
var cpuFill=document.getElementById('cpu-fill');
var cpuLabel=document.getElementById('cpu-label');
var cpuVal=16+Math.round(Math.random()*24);
if(cpuEl)cpuEl.innerHTML=cpuVal+'<span class="unit">%</span>';
if(cpuFill)cpuFill.style.width=cpuVal+'%';
if(cpuLabel)cpuLabel.textContent=cpuVal<30?'idle':cpuVal<60?'moderate':'heavy load';
var memEl=document.getElementById('mem-value');
var memFill=document.getElementById('mem-fill');
var memLabel=document.getElementById('mem-label');
var totalMem=64;
var usedMem=12+Math.round(Math.random()*32);
var memPct=Math.round(usedMem/totalMem*100);
if(memEl)memEl.innerHTML=usedMem+'<span class="unit">/'+totalMem+' GB</span>';
if(memFill)memFill.style.width=memPct+'%';
if(memLabel)memLabel.textContent=memPct+'% utilized';
var diskEl=document.getElementById('disk-value');
var diskFill=document.getElementById('disk-fill');
var diskLabel=document.getElementById('disk-label');
var totalDisk=12;
var usedDisk=3.2+Math.round(Math.random()*40)/10;
var diskPct=Math.round(usedDisk/totalDisk*100);
if(diskEl)diskEl.innerHTML=usedDisk.toFixed(1)+'<span class="unit">/'+totalDisk+' TB</span>';
if(diskFill)diskFill.style.width=diskPct+'%';
if(diskLabel)diskLabel.textContent=diskPct+'% used';
var upEl=document.getElementById('uptime-value');
if(upEl){
var hrs=36+Math.round(Math.random()*4);
upEl.innerHTML=hrs+'<span class="unit"> h</span>';
var upLabel=document.getElementById('uptime-label');
if(upLabel)upLabel.textContent='since '+(hrs>40?'Jun 24':'Jun 25');
}
}catch(ex){console.warn('metrics err:',ex)}
}
function updateQuickMetrics(){
try{
var tput=document.getElementById('metric-tput');
var lat=document.getElementById('metric-lat');
var err=document.getElementById('metric-err');
var succ=document.getElementById('metric-succ');
var tputTrend=document.getElementById('tput-trend');
var latTrend=document.getElementById('lat-trend');
var errTrend=document.getElementById('err-trend');
var succTrend=document.getElementById('succ-trend');
var tVal=110+Math.round(Math.random()*70);
var lVal=28+Math.round(Math.random()*20);
var eVal=Math.round(Math.random()*30)/10;
var sVal=Math.max(99,100-Math.round(eVal*10)/10);
if(tput)tput.innerHTML=tVal+'<span class="unit"> r/s</span>';
if(lat)lat.innerHTML=lVal+'<span class="unit"> ms</span>';
if(err)err.innerHTML=eVal.toFixed(1)+'<span class="unit"> %</span>';
if(succ)succ.innerHTML=sVal.toFixed(1)+'<span class="unit"> %</span>';
if(tputTrend)tputTrend.textContent=tVal>150?'surge':'steady';
if(latTrend)latTrend.textContent=lVal>40?'elevated':'normal';
if(errTrend)errTrend.textContent=eVal>1.5?'degraded':'clean';
if(succTrend)succTrend.textContent=sVal>99.5?'excellent':'good';
}catch(ex){console.warn('quick metrics err:',ex)}
}
function staggerGPUUpdate(i){
return function(){
if(!gpuData[i])return;
var dir=(Math.random()>0.5?1:-1);
gpuData[i].temp=Math.max(40,Math.min(90,gpuData[i].temp+dir*Math.round(Math.random()*3)));
gpuData[i].power=Math.max(50,Math.min(400,gpuData[i].power+dir*Math.round(Math.random()*8-4)));
gpuData[i].util=Math.max(5,Math.min(100,gpuData[i].util+dir*Math.round(Math.random()*6-3)));
gpuData[i].mem=Math.max(0.5,Math.min(gpuData[i].name.includes('80')?80:24,gpuData[i].mem+Math.random()*1.2-0.6));
gpuData[i].mem=Math.round(gpuData[i].mem*10)/10;
renderGPUs();
};
}
function startGPUStaggered(){
for(var i=0;i<gpuData.length;i++){
intervalMgr.register('gpu-stagger-'+i,staggerGPUUpdate(i),1500+Math.round(Math.random()*1500),'gpuGrid');
intervalMgr.start('gpu-stagger-'+i);
}
}
function initDashboard(){
try{
collapsibleSetup('agentsToggle','agentsBody','agentsPanel');
collapsibleSetup('activityToggle','activityBody','activityPanel');
collapsibleSetup('gpuToggle','gpuBody','gpuPanel');
populateAgents();
populateActivity();
renderGPUs();
updateMetrics();
updateQuickMetrics();
intervalMgr.register('metrics-update',updateMetrics,3500,'metricsGrid');
intervalMgr.start('metrics-update');
intervalMgr.register('quick-metrics-update',updateQuickMetrics,4000,'quickMetrics');
intervalMgr.start('quick-metrics-update');
startGPUStaggered();
var hamburger=document.getElementById('hamburgerBtn');
var nav=document.getElementById('mainNav');
if(hamburger&&nav){
hamburger.addEventListener('click',function(){
var open=nav.classList.toggle('open');
hamburger.setAttribute('aria-expanded',open?'true':'false');
});
}
document.querySelectorAll('.nav-bar a').forEach(function(a){
a.addEventListener('click',function(e){
e.preventDefault();
document.querySelectorAll('.nav-bar a').forEach(function(x){x.classList.remove('active');x.removeAttribute('aria-current')});
a.classList.add('active');
a.setAttribute('aria-current','page');
if(window.innerWidth<=768&&nav)nav.classList.remove('open');
});
});
var io=new IntersectionObserver(function(entries){
entries.forEach(function(entry){
if(entry.isIntersecting){
var id=entry.target.id||'';
if(id.includes('metric')||id==='metricsGrid'){intervalMgr.start('metrics-update');intervalMgr.start('quick-metrics-update');gpuData.forEach(function(_,i){intervalMgr.start('gpu-stagger-'+i)})}
}else{
var id=entry.target.id||'';
if(id.includes('metric')||id==='metricsGrid'){intervalMgr.stop('metrics-update');intervalMgr.stop('quick-metrics-update');gpuData.forEach(function(_,i){intervalMgr.stop('gpu-stagger-'+i)})}
}
});
},{threshold:0.1});
document.querySelectorAll('.card,.grid').forEach(function(el){io.observe(el)});
document.addEventListener('visibilitychange',function(){
if(document.visibilityState==='visible'){
gpuData.forEach(function(_,i){intervalMgr.start('gpu-stagger-'+i)});
intervalMgr.start('metrics-update');
intervalMgr.start('quick-metrics-update');
}else{
gpuData.forEach(function(_,i){intervalMgr.stop('gpu-stagger-'+i)});
intervalMgr.stop('metrics-update');
intervalMgr.stop('quick-metrics-update');
}
});
var loadEl=document.getElementById('app-loading');
var appEl=document.getElementById('app');
if(loadEl)loadEl.classList.add('loaded');
if(appEl)appEl.classList.add('visible');
setTimeout(function(){
if(loadEl)loadEl.style.display='none';
},500);
}catch(ex){
console.error('dashboard init error:',ex);
var appEl=document.getElementById('app');
if(appEl)appEl.innerHTML='<div class="state-error" style="padding:2rem;text-align:center"><div class="empty-icon">⚠</div><div>Dashboard failed to initialize: '+ex.message+'</div><button onclick="location.reload()" style="margin-top:1rem;padding:.5rem 1rem;background:var(--accent);color:#fff;border:none;border-radius:4px;cursor:pointer">Reload</button></div>';
var loadEl=document.getElementById('app-loading');
if(loadEl){loadEl.classList.add('loaded');setTimeout(function(){loadEl.style.display='none'},400)}
}
}
if(document.readyState==='loading'){
document.addEventListener('DOMContentLoaded',initDashboard);
}else{
initDashboard();
}
})();
</script>
</body>
</html>