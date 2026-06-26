Now I have the full picture. Existing desktop mockup #1: cyan/navy, sidebar layout, horizontal split, bar gauges. Mockup #2 will be warm amber/bronze, vertical split, radial gauges, industrial console aesthetic — completely different DNA.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Styde Forge · Control Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg-deep:#0d0a08;
  --bg-surface:#1a1410;
  --bg-panel:#221b16;
  --bg-card:#2c231d;
  --bg-card-hover:#362c24;
  --bg-titlebar:#0a0806;
  --text-primary:#e8ddd4;
  --text-secondary:#a09080;
  --text-dim:#706050;
  --amber:#d4a050;
  --amber-bright:#e8b860;
  --amber-glow:rgba(212,160,80,0.12);
  --copper:#b87840;
  --copper-dim:#8a6030;
  --green:#70b848;
  --green-dim:#508830;
  --red:#c84830;
  --orange:#d08030;
  --border:rgba(180,150,110,0.12);
  --border-strong:rgba(180,150,110,0.25);
  --radius:6px;
  --radius-lg:10px;
  --font-sans:'Inter',-apple-system,sans-serif;
  --font-mono:'IBM Plex Mono',monospace;
  --titlebar-h:38px;
  --transition:200ms cubic-bezier(0.4,0,0.2,1)
}
html,body{height:100%;width:100%;overflow:hidden;background:transparent;font-family:var(--font-sans);color:var(--text-primary);user-select:none}
body{display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.5)}
::selection{background:var(--amber);color:var(--bg-deep)}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:2px}
.window{
  width:1280px;height:840px;
  background:var(--bg-surface);
  border-radius:var(--radius-lg);
  box-shadow:0 0 0 1px var(--border),0 20px 60px rgba(0,0,0,0.7),0 0 80px rgba(212,160,80,0.03);
  display:flex;flex-direction:column;
  overflow:hidden;position:relative
}
.window::before{content:'';position:absolute;inset:0;border-radius:var(--radius-lg);padding:1px;background:linear-gradient(180deg,rgba(212,160,80,0.06) 0%,transparent 50%);-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;z-index:100}
/* titlebar */
.titlebar{
  height:var(--titlebar-h);
  background:var(--bg-titlebar);
  display:flex;align-items:center;
  padding:0 10px 0 14px;
  flex-shrink:0;position:relative;z-index:10;
  border-bottom:1px solid var(--border)
}
.titlebar-drag{flex:1;display:flex;align-items:center;gap:8px;height:100%;-webkit-app-region:drag}
.titlebar-icon{width:16px;height:16px;background:linear-gradient(135deg,var(--amber),var(--copper));border-radius:3px;flex-shrink:0;opacity:0.9}
.titlebar-text{font-size:12px;font-weight:500;color:var(--text-secondary);letter-spacing:0.5px;font-family:var(--font-mono)}
.titlebar-text span{color:var(--amber-bright)}
.titlebar-sep{width:1px;height:14px;background:var(--border);margin:0 6px}
.titlebar-status{font-size:10px;color:var(--green);font-family:var(--font-mono);display:flex;align-items:center;gap:4px}
.titlebar-status::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--green);box-shadow:0 0 6px rgba(112,184,72,0.5)}
.titlebar-controls{display:flex;gap:4px;align-items:center}
.titlebar-btn{
  width:34px;height:24px;border:none;background:transparent;
  color:var(--text-dim);font-size:10px;cursor:pointer;
  border-radius:3px;display:flex;align-items:center;justify-content:center;
  transition:var(--transition);font-family:var(--font-mono)
}
.titlebar-btn:hover{background:rgba(180,150,110,0.1);color:var(--text-secondary)}
.titlebar-btn.close:hover{background:var(--red);color:#fff}
/* main layout — vertical split (top/bottom) instead of left/right sidebar */
.content{flex:1;display:flex;flex-direction:column;padding:16px 20px;gap:12px;overflow:hidden}
/* top band — status bar + quick stats */
.top-band{
  display:flex;gap:10px;flex-shrink:0;
  padding:10px 14px;
  background:var(--bg-panel);
  border:1px solid var(--border);
  border-radius:var(--radius);
  align-items:center
}
.quick-stat{display:flex;align-items:center;gap:8px;padding-right:14px;border-right:1px solid var(--border)}
.quick-stat:last-child{border-right:none}
.quick-stat-value{font-size:18px;font-weight:700;color:var(--amber-bright);font-family:var(--font-mono);letter-spacing:-0.5px}
.quick-stat-label{font-size:10px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.6px;font-weight:500}
.quick-stat .dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.dot.green{background:var(--green);box-shadow:0 0 6px rgba(112,184,72,0.4)}
.dot.amber{background:var(--amber);box-shadow:0 0 6px rgba(212,160,80,0.3)}
.dot.red{background:var(--red);box-shadow:0 0 6px rgba(200,72,48,0.3)}
/* main body — two horizontal halves */
.main-body{flex:1;display:flex;gap:12px;min-height:0}
/* left column — agents + activity */
.col-left{flex:1.4;display:flex;flex-direction:column;gap:12px;min-width:0}
.panel{
  background:var(--bg-panel);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:12px 14px;
  transition:border-color var(--transition)
}
.panel:hover{border-color:var(--border-strong)}
.panel-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.panel-title{font-size:10px;font-weight:600;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.9px}
.panel-count{font-size:10px;padding:1px 7px;border-radius:8px;background:rgba(212,160,80,0.1);color:var(--amber);font-family:var(--font-mono);font-weight:500}
/* agent list */
.agent-list{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px;min-height:0;padding-right:2px}
.agent-item{
  display:flex;align-items:center;gap:10px;
  padding:7px 10px;border-radius:4px;
  background:rgba(255,255,255,0.015);
  border:1px solid transparent;
  transition:var(--transition);cursor:default
}
.agent-item:hover{background:var(--bg-card);border-color:var(--border)}
.agent-item.active{background:rgba(212,160,80,0.06);border-color:rgba(212,160,80,0.2)}
.agent-status{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.agent-status.online{background:var(--green);box-shadow:0 0 5px rgba(112,184,72,0.35)}
.agent-status.busy{background:var(--amber);box-shadow:0 0 5px rgba(212,160,80,0.3)}
.agent-status.offline{background:var(--red);box-shadow:0 0 5px rgba(200,72,48,0.25)}
.agent-status.idle{background:var(--text-dim)}
.agent-info{flex:1;min-width:0}
.agent-name{font-size:12px;font-weight:500;color:var(--text-primary)}
.agent-meta{font-size:10px;color:var(--text-dim);margin-top:1px;font-family:var(--font-mono)}
.agent-tasks{font-size:10px;color:var(--amber);font-family:var(--font-mono);font-weight:500}
/* activity feed (panel, scrollable) */
.activity-feed{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column}
.feed-scroll{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:3px;padding-right:4px}
.feed-item{
  display:flex;align-items:flex-start;gap:8px;
  padding:5px 6px;border-radius:3px;
  font-size:11px;line-height:1.4;
  color:var(--text-secondary);font-family:var(--font-mono);
  transition:var(--transition)
}
.feed-item:hover{background:rgba(255,255,255,0.02)}
.feed-time{color:var(--text-dim);flex-shrink:0;font-size:10px;width:48px}
.feed-msg{flex:1;min-width:0}
.feed-msg .highlight{color:var(--amber-bright)}
.feed-msg .ok{color:var(--green)}
.feed-msg .err{color:var(--red)}
/* right column — GPU + system metrics */
.col-right{flex:1;display:flex;flex-direction:column;gap:12px;min-width:0}
.metrics-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.metric-card{
  background:var(--bg-panel);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:12px;
  text-align:center;
  transition:var(--transition);cursor:default
}
.metric-card:hover{border-color:var(--border-strong);background:var(--bg-card)}
.metric-ring{
  width:72px;height:72px;margin:0 auto 6px;
  position:relative
}
.metric-ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.metric-ring .bg{fill:none;stroke:var(--border);stroke-width:4}
.metric-ring .fg{fill:none;stroke-width:4;stroke-linecap:round;transition:stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)}
.metric-ring .fg.amber{stroke:var(--amber)}
.metric-ring .fg.green{stroke:var(--green)}
.metric-ring .fg.copper{stroke:var(--copper)}
.metric-ring .fg.orange{stroke:var(--orange)}
.metric-ring .center{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:16px;font-weight:700;color:var(--text-primary);font-family:var(--font-mono)
}
.metric-label{font-size:9px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.7px;font-weight:500}
.metric-sub{font-size:10px;color:var(--text-secondary);margin-top:2px;font-family:var(--font-mono)}
/* GPU panel (full width in right column) */
.gpu-panel{flex:1;background:var(--bg-panel);border:1px solid var(--border);border-radius:var(--radius);padding:12px 14px;display:flex;flex-direction:column;min-height:0}
.gpu-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-shrink:0}
.gpu-title{font-size:10px;font-weight:600;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.9px}
.gpu-temp{font-size:20px;font-weight:700;color:var(--amber-bright);font-family:var(--font-mono)}
.gpu-temp small{font-size:12px;font-weight:400;color:var(--text-dim)}
.gpu-details{flex:1;display:flex;flex-direction:column;gap:8px;justify-content:center}
.gpu-row{display:flex;align-items:center;gap:8px}
.gpu-row-label{font-size:10px;color:var(--text-dim);width:70px;flex-shrink:0;text-transform:uppercase;letter-spacing:0.4px}
.gpu-row-bar{flex:1;height:4px;background:var(--border);border-radius:2px;overflow:hidden}
.gpu-row-fill{height:100%;border-radius:2px;transition:width 0.8s ease}
.gpu-row-fill.amber{background:linear-gradient(90deg,var(--copper-dim),var(--amber))}
.gpu-row-fill.green{background:linear-gradient(90deg,var(--green-dim),var(--green))}
.gpu-row-fill.orange{background:linear-gradient(90deg,var(--copper-dim),var(--orange))}
.gpu-row-val{font-size:10px;color:var(--text-secondary);font-family:var(--font-mono);width:40px;text-align:right;flex-shrink:0}
/* memory bar group */
.mem-group{display:flex;flex-direction:column;gap:4px;padding-top:6px;border-top:1px solid var(--border)}
.mem-row{display:flex;align-items:center;gap:8px}
.mem-label{font-size:9px;color:var(--text-dim);width:60px;flex-shrink:0}
.mem-bar{flex:1;height:3px;background:var(--border);border-radius:2px;overflow:hidden}
.mem-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--copper-dim),var(--amber-bright));transition:width 0.8s ease}
.mem-val{font-size:9px;color:var(--text-dim);font-family:var(--font-mono);width:50px;text-align:right}
/* bottom system tray */
.system-tray{
  display:flex;align-items:center;justify-content:space-between;
  padding:6px 14px;
  background:var(--bg-titlebar);
  border-top:1px solid var(--border);
  flex-shrink:0;height:28px
}
.tray-left{display:flex;align-items:center;gap:14px}
.tray-item{font-size:9px;color:var(--text-dim);font-family:var(--font-mono);display:flex;align-items:center;gap:4px}
.tray-item .dot{width:4px;height:4px;border-radius:50%}
.tray-right{display:flex;align-items:center;gap:10px}
.tray-clock{font-size:10px;color:var(--text-secondary);font-family:var(--font-mono);font-weight:500}
.tray-battery{display:flex;align-items:center;gap:3px;font-size:9px;color:var(--green);font-family:var(--font-mono)}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="titlebar-drag">
      <div class="titlebar-icon"></div>
      <span class="titlebar-text">styde-<span>forge</span>.exe</span>
      <span class="titlebar-sep"></span>
      <span class="titlebar-status">all systems nominal</span>
    </div>
    <div class="titlebar-controls">
      <button class="titlebar-btn" onclick="window.close()">_</button>
      <button class="titlebar-btn" onclick="toggleMaximize()">□</button>
      <button class="titlebar-btn close" onclick="window.close()">×</button>
    </div>
  </div>
  <div class="content">
    <div class="top-band">
      <div class="quick-stat">
        <div class="dot green"></div>
        <div>
          <div class="quick-stat-value">12</div>
          <div class="quick-stat-label">agents active</div>
        </div>
      </div>
      <div class="quick-stat">
        <div class="quick-stat-value" id="statThroughput">47</div>
        <div>
          <div class="quick-stat-label">tasks/min</div>
        </div>
      </div>
      <div class="quick-stat">
        <div class="quick-stat-value" id="statQueue">3</div>
        <div>
          <div class="quick-stat-label">queued</div>
        </div>
      </div>
      <div class="quick-stat">
        <div class="dot amber"></div>
        <div>
          <div class="quick-stat-value" id="statUptime">14h 23m</div>
          <div class="quick-stat-label">uptime</div>
        </div>
      </div>
      <div class="quick-stat">
        <div class="quick-stat-value" id="statTokens">2.4M</div>
        <div>
          <div class="quick-stat-label">tokens today</div>
        </div>
      </div>
    </div>
    <div class="main-body">
      <div class="col-left">
        <div class="panel" style="flex:1;display:flex;flex-direction:column;min-height:0">
          <div class="panel-header">
            <span class="panel-title">agent grid</span>
            <span class="panel-count" id="agentCount">12/16</span>
          </div>
          <div class="agent-list" id="agentList"></div>
        </div>
        <div class="panel activity-feed">
          <div class="panel-header">
            <span class="panel-title">activity log</span>
            <span class="panel-count" id="feedCount">0</span>
          </div>
          <div class="feed-scroll" id="feedScroll"></div>
        </div>
      </div>
      <div class="col-right">
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-ring">
              <svg viewBox="0 0 40 40">
                <circle class="bg" cx="20" cy="20" r="16"/>
                <circle class="fg amber" id="ringCPU" cx="20" cy="20" r="16" stroke-dasharray="100.53" stroke-dashoffset="0"/>
              </svg>
              <div class="center" id="cpuVal">64%</div>
            </div>
            <div class="metric-label">cpu</div>
          </div>
          <div class="metric-card">
            <div class="metric-ring">
              <svg viewBox="0 0 40 40">
                <circle class="bg" cx="20" cy="20" r="16"/>
                <circle class="fg green" id="ringRAM" cx="20" cy="20" r="16" stroke-dasharray="100.53" stroke-dashoffset="0"/>
              </svg>
              <div class="center" id="ramVal">7.2G</div>
            </div>
            <div class="metric-label">ram</div>
          </div>
          <div class="metric-card">
            <div class="metric-ring">
              <svg viewBox="0 0 40 40">
                <circle class="bg" cx="20" cy="20" r="16"/>
                <circle class="fg copper" id="ringDisk" cx="20" cy="20" r="16" stroke-dasharray="100.53" stroke-dashoffset="0"/>
              </svg>
              <div class="center" id="diskVal">340G</div>
            </div>
            <div class="metric-label">disk</div>
          </div>
          <div class="metric-card">
            <div class="metric-ring">
              <svg viewBox="0 0 40 40">
                <circle class="bg" cx="20" cy="20" r="16"/>
                <circle class="fg orange" id="ringNet" cx="20" cy="20" r="16" stroke-dasharray="100.53" stroke-dashoffset="0"/>
              </svg>
              <div class="center" id="netVal">1.2G</div>
            </div>
            <div class="metric-label">network</div>
          </div>
        </div>
        <div class="gpu-panel">
          <div class="gpu-header">
            <span class="gpu-title">nvidia rtx 5090</span>
            <span class="gpu-temp" id="gpuTemp">72<small>°c</small></span>
          </div>
          <div class="gpu-details">
            <div class="gpu-row">
              <span class="gpu-row-label">util</span>
              <div class="gpu-row-bar"><div class="gpu-row-fill amber" id="gpuUtilFill" style="width:0%"></div></div>
              <span class="gpu-row-val" id="gpuUtilVal">0%</span>
            </div>
            <div class="gpu-row">
              <span class="gpu-row-label">vram</span>
              <div class="gpu-row-bar"><div class="gpu-row-fill green" id="gpuVRAMFill" style="width:0%"></div></div>
              <span class="gpu-row-val" id="gpuVRAMVal">0/24G</span>
            </div>
            <div class="gpu-row">
              <span class="gpu-row-label">power</span>
              <div class="gpu-row-bar"><div class="gpu-row-fill orange" id="gpuPwrFill" style="width:0%"></div></div>
              <span class="gpu-row-val" id="gpuPwrVal">0W</span>
            </div>
            <div class="mem-group">
              <div class="mem-row">
                <span class="mem-label">model cache</span>
                <div class="mem-bar"><div class="mem-fill" id="memCacheFill" style="width:62%"></div></div>
                <span class="mem-val" id="memCacheVal">3.8G / 6.1G</span>
              </div>
              <div class="mem-row">
                <span class="mem-label">context</span>
                <div class="mem-bar"><div class="mem-fill" id="memCtxFill" style="width:41%"></div></div>
                <span class="mem-val" id="memCtxVal">1.7G / 4.2G</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="system-tray">
    <div class="tray-left">
      <span class="tray-item"><span class="dot green"></span>forge-engine</span>
      <span class="tray-item"><span class="dot green"></span>scheduler</span>
      <span class="tray-item"><span class="dot green"></span>teacher</span>
      <span class="tray-item" id="trayWorkers">8 workers</span>
    </div>
    <div class="tray-right">
      <span class="tray-item">🔊 68%</span>
      <span class="tray-item">📡 5.8G</span>
      <span class="tray-clock" id="trayClock"></span>
    </div>
  </div>
</div>
<script>
const R=200,CIRC=2*Math.PI*16;
const AGENTS=[
  {n:'Hermes Orchestrator',s:'online',t:'12 tasks'},
  {n:'Teacher Evaluator',s:'busy',t:'eval batch #46'},
  {n:'Blueprint Manager',s:'online',t:'idle'},
  {n:'Subagent Dispatcher',s:'busy',t:'spawn 3 agents'},
  {n:'Quality Gate',s:'online',t:'pending review'},
  {n:'Prompt Engineer',s:'online',t:'v7 → v8'},
  {n:'Caveman Coder',s:'idle',t:'waiting'},
  {n:'CommandCenter UI',s:'online',t:'live at :8766'},
  {n:'Batch Scheduler',s:'busy',t:'queue 14 BPs'},
  {n:'Dashboard Server',s:'online',t:'port 8765'},
  {n:'Log Parser',s:'online',t:'tailing forge_b1.log'},
  {n:'Config Sync',s:'idle',t:'last sync 2m ago'},
];
const FEED_T=[
  '[Hermes] spawned subagent for blueprint <span class="highlight">data-migration-simulator</span>',
  '[Teacher] eval scores: 82.4 <span class="ok">+3.1</span> vs baseline',
  '[Worker 4] completed task in <span class="highlight">14.2s</span>',
  '[QualityGate] <span class="ok">passed</span> persona.md checks',
  '[Scheduler] queued 7 BPs for batch run',
  '[GPU] compute allocation: <span class="highlight">4096MB</span>',
  '[Worker 7] <span class="err">timeout</span> on long-running task, retrying',
  '[Hermes] health check <span class="ok">passed</span> — all subsystems nominal',
  '[Cache] warmed 12 model shards in 3.4s',
  '[Dashboard] SSE stream connected at :8765',
  '[Worker 2] processing blueprint <span class="highlight">agent-code-reviewer-v3</span>',
  '[Teacher] weakest: completeness (72.1) — proposing fix',
  '[Config] checkpoint saved: batch #46 state.yaml',
  '[PromptEng] PlanPrompt-v8.md <span class="ok">compiled</span> — ready for review',
  '[LogParser] indexed 2400 lines from forge_b3.log',
];
let fi=0,loop;
function setRing(id,pct){const el=document.getElementById(id);if(el)el.setAttribute('stroke-dashoffset',CIRC-CIRC*pct/100)}
function renderAgents(){
  const el=document.getElementById('agentList');
  el.innerHTML=AGENTS.map((a,i)=>`
    <div class="agent-item${i<3?' active':''}">
      <div class="agent-status ${a.s}"></div>
      <div class="agent-info">
        <div class="agent-name">${a.n}</div>
        <div class="agent-meta">${a.t}</div>
      </div>
      <span class="agent-tasks">${a.s==='busy'?'▶':'○'}</span>
    </div>
  `).join('');
  document.getElementById('agentCount').textContent=AGENTS.filter(a=>a.s==='online'||a.s==='busy').length+'/'+AGENTS.length;
}
function addFeedItem(){
  const el=document.getElementById('feedScroll');
  const msg=FEED_T[fi%FEED_T.length];fi++;
  const t=new Date();
  const ts=String(t.getHours()).padStart(2,'0')+':'+String(t.getMinutes()).padStart(2,'0')+':'+String(t.getSeconds()).padStart(2,'0');
  const div=document.createElement('div');
  div.className='feed-item';
  div.innerHTML='<span class="feed-time">'+ts+'</span><span class="feed-msg">'+msg+'</span>';
  el.insertBefore(div,el.firstChild);
  const c=el.querySelectorAll('.feed-item').length;
  document.getElementById('feedCount').textContent=c;
  while(el.children.length>50)el.removeChild(el.lastChild);
}
function updateMetrics(){
  const cpu=30+Math.random()*60|0;
  const ramPct=40+Math.random()*40|0;
  const diskPct=50+Math.random()*20|0;
  const netPct=20+Math.random()*30|0;
  const gpuUtil=20+Math.random()*70|0;
  const gpuVRAM=8+Math.random()*14|0;
  const gpuPwr=120+Math.random()*280|0;
  const temp=55+Math.random()*25|0;
  document.getElementById('cpuVal').textContent=cpu+'%';
  document.getElementById('ramVal').textContent=(6+Math.random()*8|0)+'.'+(Math.random()*9|0)+'G';
  document.getElementById('diskVal').textContent=(280+Math.random()*120|0)+'G';
  document.getElementById('netVal').textContent=(0.5+Math.random()*2.5).toFixed(1)+'G';
  document.getElementById('gpuTemp').innerHTML=temp+'<small>°c</small>';
  document.getElementById('gpuUtilVal').textContent=gpuUtil+'%';
  document.getElementById('gpuVRAMVal').textContent=gpuVRAM+'/24G';
  document.getElementById('gpuPwrVal').textContent=gpuPwr+'W';
  document.getElementById('gpuUtilFill').style.width=gpuUtil+'%';
  document.getElementById('gpuVRAMFill').style.width=(gpuVRAM/24*100)+'%';
  document.getElementById('gpuPwrFill').style.width=(gpuPwr/400*100)+'%';
  setRing('ringCPU',cpu);
  setRing('ringRAM',ramPct);
  setRing('ringDisk',diskPct);
  setRing('ringNet',netPct);
  const thru=document.getElementById('statThroughput');
  const v=parseInt(thru.textContent);
  thru.textContent=v+(-1+Math.random()*3|0);
  document.getElementById('trayWorkers').textContent=(6+Math.random()*8|0)+' workers';
}
function updateClock(){
  const t=new Date();
  document.getElementById('trayClock').textContent=t.toLocaleTimeString('sv-SE',{hour:'2-digit',minute:'2-digit'});
}
renderAgents();
for(let i=0;i<12;i++)addFeedItem();
updateMetrics();
updateClock();
loop=setInterval(()=>{
  addFeedItem();
  updateMetrics();
  updateClock();
},2800);
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){clearInterval(loop)}else{
    updateMetrics();updateClock();
    loop=setInterval(()=>{addFeedItem();updateMetrics();updateClock()},2800);
  }
});
</script>
</body>
</html>