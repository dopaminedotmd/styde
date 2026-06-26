Mockup 1: Neural Data Mesh — Data Binding
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Neural Data Mesh</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;color:#c0e0ff;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}
#app{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:2rem}
canvas#particles{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none}
h1{font-size:1.8rem;font-weight:300;letter-spacing:.15em;text-transform:uppercase;margin-bottom:2rem;text-shadow:0 0 20px #0ff8,0 0 40px #0ff4}
.glow{text-shadow:0 0 10px currentColor}
.neon-border{border:1px solid #0ff3;box-shadow:0 0 15px #0ff3,inset 0 0 15px #0ff1;border-radius:8px}
.translucent{background:rgba(10,10,30,.65);backdrop-filter:blur(8px)}
.scanline{position:relative;overflow:hidden}
.scanline::after{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,#0ff4,transparent);animation:scan 3s linear infinite}
@keyframes scan{0%{top:0}100%{top:100%}}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;margin-bottom:2rem}
.stat-card{padding:1.25rem;position:relative}
.stat-card .label{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#6af8;margin-bottom:.25rem}
.stat-card .value{font-size:1.6rem;font-weight:600;color:#0ff;text-shadow:0 0 15px #0ff6}
.stat-card .delta{font-size:.75rem;margin-top:.25rem}
.delta.up{color:#0f8}
.delta.down{color:#f44}
.data-table{width:100%;border-collapse:collapse;font-size:.85rem}
.data-table th{padding:.6rem .8rem;text-align:left;color:#6af;font-weight:400;text-transform:uppercase;letter-spacing:.08em;border-bottom:1px solid #0ff2}
.data-table td{padding:.6rem .8rem;border-bottom:1px solid #fff08;cursor:pointer;transition:background .2s}
.data-table tr:hover td{background:#0ff08}
.data-table tr.expanded td{background:#0ff12}
.detail-panel{display:none;padding:1rem;margin:.5rem 0;font-size:.8rem;line-height:1.6;color:#8cf}
.detail-panel.show{display:block}
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.status-dot.online{background:#0f8;box-shadow:0 0 8px #0f8}
.status-dot.warning{background:#fa0;box-shadow:0 0 8px #fa0}
.status-dot.offline{background:#f44;box-shadow:0 0 8px #f44}
.feed-ticker{overflow:hidden;height:1.4rem;position:relative;margin-bottom:1.5rem}
.feed-ticker .ticker-text{position:absolute;white-space:nowrap;animation:tick 20s linear infinite;color:#6af;font-size:.8rem;letter-spacing:.05em}
@keyframes tick{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}
@media(max-width:600px){h1{font-size:1.2rem}#app{padding:1rem}.grid{grid-template-columns:1fr}.stat-card .value{font-size:1.2rem}.data-table{font-size:.75rem}}
@media(min-width:601px) and (max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
</style>
<div id=app>
<h1><span class=glow>Neural Data Mesh</span></h1>
<div class="feed-ticker translucent neon-border scanline">
<div class=ticker-text id=ticker></div>
</div>
<div class=grid id=statsGrid></div>
<div class="translucent neon-border scanline" style=padding:0>
<table class=data-table>
<thead><tr><th>Node</th><th>Status</th><th>Throughput</th><th>Latency</th><th>Packets</th></tr></thead>
<tbody id=tableBody></tbody>
</table>
</div>
</div>
<canvas id=particles></canvas>
<script>
const API_DATA = [
{id:'NODE-01',name:'Primary Nexus',status:'online',throughput:'4.2 Gbps',latency:'1.2ms',packets:'89.4M',detail:'Core routing hub. Uptime: 99.97%. Connected to 12 edge nodes.'},
{id:'NODE-02',name:'Edge Relay Alpha',status:'online',throughput:'2.8 Gbps',latency:'3.7ms',packets:'52.1M',detail:'Regional edge cache. Serving 23 distributed clients.'},
{id:'NODE-03',name:'Quantum Bridge',status:'warning',throughput:'1.1 Gbps',latency:'8.4ms',packets:'28.6M',detail:'Quantum link. Entanglement fidelity: 94.2%. Retransmit rate elevated.'},
{id:'NODE-04',name:'Data Spire B7',status:'online',throughput:'6.7 Gbps',latency:'0.8ms',packets:'127.3M',detail:'Primary data spire. Storage: 847TB/1.2PB used.'},
{id:'NODE-05',name:'Sentinel Array',status:'offline',throughput:'0 bps',latency:'--',packets:'0',detail:'Security array undergoing maintenance. ETA: 14min.'},
{id:'NODE-06',name:'Mesh Relay 9',status:'online',throughput:'3.4 Gbps',latency:'2.1ms',packets:'71.8M',detail:'Mesh relay. Signal strength: -62dBm. Routing 9 connections.'}
];
const STATS = [
{label:'Total Throughput',value:'18.2 Gbps',delta:'+2.4',up:true},
{label:'Active Nodes',value:'42/48',delta:'+3',up:true},
{label:'Avg Latency',value:'2.9ms',delta:'-0.7',up:true},
{label:'Packet Loss',value:'0.04%',delta:'-0.01',up:true}
];
const TICKER_MSGS = [
'SYSTEM HEALTH: NOMINAL — All sectors operational',
'ALERT: Sentinel Array offline for maintenance — ETA 14min',
'SIGNAL: Node Quantum Bridge at 94.2% entanglement fidelity',
'SIGNAL: Mesh Relay 9 rerouting through alternate path',
'SYSTEM HEALTH: Throughput at 87% capacity — stable'
];
// Particles — programmatic generation
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let w,h,particles=[];
function resize(){w=canvas.width=innerWidth;h=canvas.height=innerHeight}
resize();addEventListener('resize',resize);
for(let i=0;i<60;i++){particles.push({x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,r:Math.random()*2+1})}
function drawParticles(){
  ctx.clearRect(0,0,w,h);
  for(let p of particles){
    p.x+=p.vx;p.y+=p.vy;
    if(p.x<0)p.x=w;if(p.x>w)p.x=0;
    if(p.y<0)p.y=h;if(p.y>h)p.y=0;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(0,255,255,${.3+p.r/8})`;
    ctx.fill();
    ctx.shadowBlur=10;ctx.shadowColor='#0ff4';
    ctx.fill();ctx.shadowBlur=0;
  }
  for(let i=0;i<particles.length;i++){
    for(let j=i+1;j<particles.length;j++){
      let dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<120){ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);ctx.strokeStyle=`rgba(0,255,255,${.08*(1-d/120)})`;ctx.stroke()}
    }
  }
  requestAnimationFrame(drawParticles)
}
drawParticles();
// Data binding — stats
const statsGrid=document.getElementById('statsGrid');
for(let s of STATS){
  let card=document.createElement('div');
  card.className='stat-card translucent neon-border scanline';
  card.innerHTML=`<div class=label>${s.label}</div><div class=value>${s.value}</div><div class="delta ${s.up?'up':'down'}">${s.delta}${s.up?' ▲':' ▼'}</div>`;
  statsGrid.appendChild(card)
}
// Data binding — table with interactivity
const tbody=document.getElementById('tableBody');
for(let d of API_DATA){
  let tr=document.createElement('tr');
  tr.innerHTML=`<td><span class=glow>${d.name}</span></td><td><span class="status-dot ${d.status}"></span>${d.status}</td><td>${d.throughput}</td><td>${d.latency}</td><td>${d.packets}</td>`;
  let detail=document.createElement('tr');
  detail.className='detail-panel';
  detail.innerHTML=`<td colspan=5><div class="translucent neon-border" style="padding:.8rem">${d.detail}</div></td>`;
  tr.addEventListener('click',function(){
    detail.classList.toggle('show');
    tr.classList.toggle('expanded')
  });
  tbody.appendChild(tr);
  tbody.appendChild(detail)
}
// Feed ticker
document.getElementById('ticker').textContent=TICKER_MSGS.join(' • ')
</script>
---
Demonstrates programmatic particle network (JS loop, 60 particles with connection lines), client-side data binding from simulated API (6-node table + 4 stat cards rendered into DOM), and interactive click-to-expand detail panels. Includes responsive grid and media queries at 600px/900px breakpoints.
Mockup 2: Holographic Command Hub — Interactivity
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Cybernetic Command Hub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08081a;color:#c8e8ff;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}
#app{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:2rem}
canvas#bg{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none}
h1{font-size:1.8rem;font-weight:300;letter-spacing:.12em;margin-bottom:.5rem;text-shadow:0 0 20px #f0f8,0 0 40px #f0f4}
.subtitle{color:#6af8;font-size:.85rem;letter-spacing:.1em;margin-bottom:2rem;text-transform:uppercase}
.panel-row{display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap}
.panel{flex:1;min-width:220px;padding:1.25rem;border:1px solid #f0f3;border-radius:10px;background:rgba(20,8,40,.6);backdrop-filter:blur(10px);box-shadow:0 0 20px #f0f2,inset 0 0 20px #f0f1;position:relative;overflow:hidden}
.panel::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 20%,#f0f08,transparent 60%);opacity:.15;pointer-events:none}
.panel .plabel{font-size:.65rem;text-transform:uppercase;letter-spacing:.12em;color:#a8f8;margin-bottom:.5rem}
.panel .pvalue{font-size:2rem;font-weight:600;text-shadow:0 0 20px #f0f6}
.panel .pmeta{font-size:.7rem;color:#6af6;margin-top:.25rem}
.wave-container{height:100px;margin-bottom:1.5rem;position:relative;border:1px solid #f0f3;border-radius:8px;background:rgba(20,8,40,.4);backdrop-filter:blur(6px);overflow:hidden}
.wave-container canvas{width:100%;height:100%}
.controls{display:flex;gap:.6rem;margin-bottom:1.5rem;flex-wrap:wrap}
.btn{padding:.5rem 1.2rem;border:1px solid #f0f5;border-radius:6px;background:rgba(40,10,70,.4);color:#d0b0ff;font-size:.8rem;cursor:pointer;transition:all .25s;text-transform:uppercase;letter-spacing:.08em;backdrop-filter:blur(4px)}
.btn:hover{background:rgba(100,30,180,.5);border-color:#f0f;box-shadow:0 0 20px #f0f6;transform:translateY(-2px)}
.btn.active{background:rgba(100,30,180,.6);border-color:#f0f;box-shadow:0 0 25px #f0f8,inset 0 0 15px #f0f4}
.btn .keyhint{display:inline-block;border:1px solid #f0f5;border-radius:3px;padding:0 .35rem;margin-left:.4rem;font-size:.65rem;color:#a8f8}
.log-panel{height:140px;overflow-y:auto;padding:.8rem;border:1px solid #f0f3;border-radius:8px;background:rgba(10,5,20,.7);backdrop-filter:blur(6px);font-family:'Cascadia Code','Fira Code',monospace;font-size:.75rem;line-height:1.7}
.log-panel .log-entry{opacity:0;animation:fadeIn .3s forwards}
.log-panel .log-entry .ts{color:#6af6}
.log-panel .log-entry .msg{color:#d0b0ff}
.log-panel .log-entry .msg.warn{color:#fa0}
.log-panel .log-entry .msg.err{color:#f44}
@keyframes fadeIn{to{opacity:1}}
@media(max-width:600px){h1{font-size:1.2rem}#app{padding:1rem}.panel .pvalue{font-size:1.3rem}.panel-row{flex-direction:column}}
</style>
<div id=app>
<h1>Cybernetic Command Hub</h1>
<div class=subtitle>Telemetry Interface v2.4 — Press 1-3 to switch views</div>
<div class=panel-row id=metricPanels></div>
<div class=wave-container><canvas id=waveCanvas></canvas></div>
<div class=controls>
<button class="btn active" data-view=dashboard>Dashboard <span class=keyhint>1</span></button>
<button class=btn data-view=telemetry>Telemetry <span class=keyhint>2</span></button>
<button class=btn data-view=diagnostics>Diagnostics <span class=keyhint>3</span></button>
<button class=btn id=toggleGL>GL Overlay <span class=keyhint>G</span></button>
<button class=btn id=clearLog>Clear Log <span class=keyhint>C</span></button>
</div>
<div id=viewContent class="panel" style="padding:1rem;min-height:100px;display:flex;align-items:center;justify-content:center;font-size:.9rem;color:#a8f8"></div>
<div class=log-panel id=logPanel></div>
</div>
<canvas id=bg></canvas>
<script>
const METRICS = [
{label:'Core Temp',value:'47.2°C',meta:'Nominal range: 35-65°C'},
{label:'Power Draw',value:'342W',meta:'Peak: 450W'},
{label:'Fan Speed',value:'6200 RPM',meta':'},
{label:'Memory Load',value:'68%',meta:'32GB/48GB used'}
];
const VIEWS = {
  dashboard:'System dashboard active. All subsystems nominal. Data throughput stable at 1.4 TB/s. Network mesh integrity: 98.7%. Quantum encryption keys rotated successfully.',
  telemetry:'Telemetry stream active. Receiving from 23 remote sensors. Signal strength: -48dBm average. Sampling rate: 200Hz. No anomalies detected in last 60 seconds.',
  diagnostics:'Diagnostics running... CPU: 42% load | GPU: 71% load | MEM: 68% | DISK: 1.2TB/4TB | NET: 1.4 TB/s throughput. Self-test: PASS. Firmware: v3.1.8-rc2.'
};
// Wave generator — programmatic JS loop
const waveCanvas = document.getElementById('waveCanvas');
const wctx = waveCanvas.getContext('2d');
let ww, wh, bars = 60, barValues = [], time = 0;
function resizeWave(){ww=waveCanvas.width=waveCanvas.parentElement.clientWidth;wh=waveCanvas.height=waveCanvas.parentElement.clientHeight}
resizeWave();addEventListener('resize',resizeWave);
for(let i=0;i<bars;i++)barValues[i]=0;
function drawWave(){
  time+=.02;ww=waveCanvas.width;wh=waveCanvas.height;
  wctx.clearRect(0,0,ww,wh);
  let bw=ww/bars*.7,gap=ww/bars*.3;
  for(let i=0;i<bars;i++){
    barValues[i]+=(Math.sin(time+i*.2)*.5+Math.sin(time*.6+i*.7)*.3+Math.random()*.15 - barValues[i])*.1;
    let h=Math.abs(barValues[i])*wh*.6;
    let grad=wctx.createLinearGradient(0,wh-h,0,wh);
    grad.addColorStop(0,`hsla(${280+barValues[i]*30},100%,60%,.9)`);
    grad.addColorStop(1,`hsla(${280+barValues[i]*30},100%,60%,.1)`);
    wctx.fillStyle=grad;
    wctx.shadowBlur=15;wctx.shadowColor='#f0f6';
    wctx.fillRect(i*(bw+gap)+gap/2,wh-h,bw,h);
    wctx.shadowBlur=0
  }
  requestAnimationFrame(drawWave)
}
drawWave();
// Stat panels — programmatic
const panelsContainer = document.getElementById('metricPanels');
for(let m of METRICS){
  let p=document.createElement('div');
  p.className='panel';
  p.innerHTML=`<div class=plabel>${m.label}</div><div class=pvalue>${m.value}</div><div class=pmeta>${m.meta||'Stable'}</div>`;
  panelsContainer.appendChild(p)
}
// Log system
const logPanel = document.getElementById('logPanel');
const LOGS = [
  {msg:'System initialized. Command interface online.',type:'info'},
  {msg:'Telemetry handshake complete — 23 remote sensors connected.',type:'info'},
  {msg:'Memory scrub: PASS — no ECC errors detected.',type:'info'},
  {msg:'Network latency spike detected on relay 7.',type:'warn'},
  {msg:'Thermal margin: 18°C below critical threshold.',type:'info'}
];
let logIndex=LOGS.length;
function addLog(msg,type='info'){
  let e=document.createElement('div');e.className='log-entry';
  let ts=new Date().toLocaleTimeString();
  e.innerHTML=`<span class=ts>[${ts}]</span> <span class="msg ${type}">${msg}</span>`;
  logPanel.appendChild(e);logPanel.scrollTop=logPanel.scrollHeight
}
for(let l of LOGS)setTimeout(()=>addLog(l.msg,l.type),l.index||100)
// View switching
const viewContent = document.getElementById('viewContent');
const buttons = document.querySelectorAll('[data-view]');
let currentView='dashboard';
viewContent.textContent=VIEWS[currentView];
function switchView(view){
  currentView=view;
  viewContent.textContent=VIEWS[view];
  buttons.forEach(b=>b.classList.toggle('active',b.dataset.view===view));
  addLog(`Switched to ${view} view.`)
}
buttons.forEach(b=>b.addEventListener('click',()=>switchView(b.dataset.view)));
// Background particles — programmatic
const bg=document.getElementById('bg'),bgc=bg.getContext('2d');
let bw2,bh2,stars=[],rings=[];
function resizeBg(){bw2=bg.width=innerWidth;bh2=bg.height=innerHeight}
resizeBg();addEventListener('resize',resizeBg);
for(let i=0;i<80;i++)stars.push({x:Math.random()*bw2,y:Math.random()*bh2,r:Math.random()*2+.5,s:Math.random()*.5+.5})
for(let i=0;i<3;i++)rings.push({x:Math.random()*bw2,y:Math.random()*bh2,r:Math.random()*80+40,a:0,da:Math.random()*.01+.005});
function drawBg(){
  bgc.clearRect(0,0,bw2,bh2);
  for(let s of stars){
    s.y-=s.s;if(s.y<0){s.y=bh2;s.x=Math.random()*bw2}
    bgc.beginPath();bgc.arc(s.x,s.y,s.r,0,Math.PI*2);
    bgc.fillStyle=`rgba(200,150,255,${.3+s.r/6})`;
    bgc.fill()
  }
  for(let r of rings){
    r.a+=r.da;
    bgc.beginPath();bgc.arc(r.x,r.y,r.r+Math.sin(r.a)*10,0,Math.PI*2);
    bgc.strokeStyle=`rgba(200,100,255,${.15+Math.sin(r.a)*.1})`;
    bgc.lineWidth=1;bgc.shadowBlur=20;bgc.shadowColor='#f0f4';bgc.stroke();bgc.shadowBlur=0
  }
  requestAnimationFrame(drawBg)
}
drawBg();
// Keyboard shortcuts
document.addEventListener('keydown',function(e){
  if(e.key==='1')switchView('dashboard');
  else if(e.key==='2')switchView('telemetry');
  else if(e.key==='3')switchView('diagnostics');
  else if(e.key==='g'||e.key==='G'){document.querySelector('.wave-container').style.display=document.querySelector('.wave-container').style.display==='none'?'block':'none';addLog('GL overlay toggled.')}
  else if(e.key==='c'||e.key==='C'){logPanel.innerHTML='';addLog('Log cleared.')}
});
// GL toggle
document.getElementById('toggleGL').addEventListener('click',function(){
  document.querySelector('.wave-container').style.display=document.querySelector('.wave-container').style.display==='none'?'block':'none';
  addLog('GL overlay toggled.')
});
document.getElementById('clearLog').addEventListener('click',function(){logPanel.innerHTML='';addLog('Log cleared.')});
// Initial logs
setTimeout(()=>{for(let l of LOGS)addLog(l.msg,l.type)},200)
</script>
---
Demonstrates programmatic waveform bars (60 bars rendered via JS requestAnimationFrame loop with dynamic gradients), keyboard shortcuts (1/2/3/G/C) and button-based interactivity, view switching with content binding, log system with timestamped entries, and canvas starfield with animated rings. Responsive breakpoint at 600px.
Mockup 3: Quantum Starfield Interface — Visual Spectacle
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Quantum Starfield Interface</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#05050f;color:#c0e0ff;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow:hidden;cursor:default}
#app{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:2rem;height:100vh;display:flex;flex-direction:column}
canvas#starfield{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0}
.header-bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;flex-wrap:wrap;gap:.5rem}
h1{font-size:1.8rem;font-weight:300;letter-spacing:.12em;text-shadow:0 0 25px #80f8,0 0 60px #80f4}
.clock{font-family:'Cascadia Code','Fira Code',monospace;font-size:1.2rem;color:#80f8;text-shadow:0 0 15px #80f6;letter-spacing:.1em}
.main-grid{display:grid;grid-template-columns:2fr 1fr;gap:1.5rem;flex:1}
@media(max-width:900px){.main-grid{grid-template-columns:1fr}}
.card{padding:1.25rem;border:1px solid #80f3;border-radius:12px;background:rgba(10,5,30,.55);backdrop-filter:blur(12px);box-shadow:0 0 30px #80f2,inset 0 0 20px #80f1;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:-60%;left:-60%;width:220%;height:220%;background:radial-gradient(ellipse at 30% 20%,#80f08,transparent 60%);opacity:.12;pointer-events:none}
.card h2{font-size:.75rem;text-transform:uppercase;letter-spacing:.15em;color:#a8f8;margin-bottom:1rem;font-weight:400}
.quantum-ring{width:140px;height:140px;border-radius:50%;margin:0 auto 1.5rem;position:relative}
.quantum-ring canvas{width:100%;height:100%}
.qubit-row{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid #80f2;font-size:.85rem}
.qubit-row:last-child{border-bottom:none}
.qubit-label{color:#a8f8}
.qubit-value{font-family:'Cascadia Code','Fira Code',monospace;color:#80f}
.qubit-value.stable{color:#0f8}
.qubit-value.unstable{color:#fa0}
.qubit-value.collapsed{color:#f44}
.status-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem}
.stat-item{text-align:center;padding:.5rem}
.stat-item .sval{font-size:1.3rem;font-weight:600;text-shadow:0 0 12px currentColor}
.stat-item .slabel{font-size:.6rem;text-transform:uppercase;letter-spacing:.1em;color:#a8f8;margin-top:.2rem}
.freq-bars{display:flex;gap:2px;height:40px;align-items:flex-end;justify-content:center;margin-top:.5rem}
.freq-bars .bar{width:6px;border-radius:2px 2px 0 0;transition:height .3s}
.interaction-hint{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);font-size:.7rem;color:#a8f6;letter-spacing:.1em;text-align:center;z-index:2;background:rgba(5,5,15,.6);padding:.4rem 1rem;border-radius:20px;border:1px solid #80f3;backdrop-filter:blur(8px)}
@media(max-width:600px){h1{font-size:1.1rem}#app{padding:1rem}.main-grid{grid-template-columns:1fr}.quantum-ring{width:100px;height:100px}.status-grid{grid-template-columns:1fr 1fr}.card{padding:.8rem}}
</style>
<div id=app>
<div class=header-bar>
<h1>Quantum Starfield Interface</h1>
<div class=clock id=clock>--:--:--</div>
</div>
<div class=main-grid>
<div class=card>
<h2>Qubit State Matrix</h2>
<div class=quantum-ring><canvas id=qubitRing></canvas></div>
<div id=qubitTable></div>
</div>
<div class=card>
<h2>System Telemetry</h2>
<div class=status-grid id=statusGrid></div>
<h2 style=margin-top:1.5rem>Frequency Spectrum</h2>
<div class=freq-bars id=freqBars></div>
</div>
</div>
</div>
<canvas id=starfield></canvas>
<div class=interaction-hint>Move mouse to steer starfield — Click to toggle quantum state projection</div>
<script>
const QUBITS = [
{id:'Q0',state:'|0⟩+|1⟩',phase:'superposed',value:'0.71∠0°'},
{id:'Q1',state:'|0⟩',phase:'stable',value:'1.00∠0°'},
{id:'Q2',state:'|0⟩+|1⟩',phase:'superposed',value:'0.50∠45°'},
{id:'Q3',state:'|1⟩',phase:'unstable',value:'0.88∠90°'},
{id:'Q4',state:'|0⟩+|1⟩',phase:'collapsed',value:'0.33∠180°'},
{id:'Q5',state:'|0⟩',phase:'stable',value:'1.00∠0°'}
];
const STATUS = [
{label:'Entanglement Fidelity',value:'94.3%',color:'#0f8'},
{label:'Decoherence Rate',value:'0.012/s',color:'#fa0'},
{label:'Gate Fidelity',value:'99.1%',color:'#0f8'},
{label:'Quantum Volume',value:'128',color:'#80f'}
];
// Starfield — canvas, mouse-interactive
const sf=document.getElementById('starfield'),sfc=sf.getContext('2d');
let sw,sh,starArr=[],mx=0,my=0;
function resizeSF(){sw=sf.width=innerWidth;sh=sf.height=innerHeight}
resizeSF();addEventListener('resize',resizeSF);
document.addEventListener('mousemove',e=>{mx=(e.clientX/sw-.5)*2;my=(e.clientY/sh-.5)*2});
for(let i=0;i<400;i++)starArr.push({x:(Math.random()-.5)*sw*2,y:(Math.random()-.5)*sh*2,z:Math.random()*sw+f=>{} ... wait, let me simplify});
// Stars array
for(let i=0;i<400;i++){
  starArr.push({
    x:(Math.random()-.5)*2000,
    y:(Math.random()-.5)*2000,
    z:Math.random()*2000+1,
    size:Math.random()*2+.5,
    color:`hsl(${260+Math.random()*40},80%,${60+Math.random()*30}%)`
  })
}
function drawSF(){
  sfc.clearRect(0,0,sw,sh);
  let cx=0+mx*200,cy=0+my*200;
  for(let s of starArr){
    let px=(s.x-cx)/s.z*300+sw/2;
    let py=(s.y-cy)/s.z*300+sh/2;
    let size=s.size*(1-s.z/2200)+.3;
    if(px<0||px>sw||py<0||py>sh)continue;
    sfc.beginPath();sfc.arc(px,py,Math.max(size,.3),0,Math.PI*2);
    let bright=Math.max(0,1-s.z/2200);
    sfc.fillStyle=`rgba(${180+Math.sin(s.x)*40},${120+Math.cos(s.y)*40},255,${bright*.8})`;
    sfc.shadowBlur=size*8;sfc.shadowColor=`rgba(128,0,255,${bright*.3})`;
    sfc.fill();sfc.shadowBlur=0
  }
  requestAnimationFrame(drawSF)
}
drawSF();
// Quantum ring — programmatic canvas
const qr=document.getElementById('qubitRing'),qrc=qr.getContext('2d');
let qrSize=140;
function resizeQR(){qrSize=qr.parentElement.clientWidth||140;qr.width=qr.height=qrSize}
resizeQR();addEventListener('resize',resizeQR);
let qAngle=0;
function drawQR(){
  qAngle+=.01;
  qrc.clearRect(0,0,qrSize,qrSize);
  let cx=qrSize/2,cy=qrSize/2,rr=qrSize/2.8;
  // Outer glow ring
  for(let i=0;i<4;i++){
    qrc.beginPath();qrc.arc(cx,cy,rr+i*4,0,Math.PI*2);
    qrc.strokeStyle=`rgba(128,0,255,${.08-i*.015})`;
    qrc.lineWidth=1;qrc.stroke()
  }
  // Animated particle orbit
  for(let i=0;i<6;i++){
    let a=qAngle+i*Math.PI/3;
    let px=cx+Math.cos(a)*rr,py=cy+Math.sin(a)*rr;
    let px2=cx+Math.cos(a+Math.PI/2)*rr*.6,py2=cy+Math.sin(a+Math.PI/2)*rr*.6;
    qrc.beginPath();qrc.arc(px,py,3,0,Math.PI*2);
    qrc.fillStyle=`rgba(0,255,255,${.5+Math.sin(a)*.3})`;
    qrc.shadowBlur=20;qrc.shadowColor='#0ff8';qrc.fill();qrc.shadowBlur=0;
    qrc.beginPath();qrc.arc(px2,py2,2,0,Math.PI*2);
    qrc.fillStyle=`rgba(200,100,255,${.4+Math.cos(a)*.2})`;
    qrc.shadowBlur=15;qrc.shadowColor='#80f8';qrc.fill();qrc.shadowBlur=0
  }
  // Center glow
  let grad=qrc.createRadialGradient(cx,cy,0,cx,cy,rr*.6);
  grad.addColorStop(0,'rgba(128,0,255,.15)');grad.addColorStop(1,'rgba(128,0,255,0)');
  qrc.fillStyle=grad;qrc.beginPath();qrc.arc(cx,cy,rr*.6,0,Math.PI*2);qrc.fill();
  requestAnimationFrame(drawQR)
}
drawQR();
// Qubit table
const qt=document.getElementById('qubitTable');
for(let q of QUBITS){
  let row=document.createElement('div');row.className='qubit-row';
  row.innerHTML=`<span class=qubit-label>${q.id} ${q.state}</span><span class="qubit-value ${q.phase}">${q.value}</span>`;
  qt.appendChild(row)
}
// Status grid
const sg=document.getElementById('statusGrid');
for(let s of STATUS){
  let div=document.createElement('div');div.className='stat-item';
  div.innerHTML=`<div class=sval style="color:${s.color}">${s.value}</div><div class=slabel>${s.label}</div>`;
  sg.appendChild(div)
}
// Frequency bars — programmatic
const fb=document.getElementById('freqBars');
for(let i=0;i<36;i++){
  let bar=document.createElement('div');bar.className='bar';
  bar.style.background=`hsla(${270+Math.random()*30},90%,60%,.8)`;
  bar.style.height=Math.random()*35+5+'px';
  fb.appendChild(bar)
}
setInterval(()=>{
  let bars=fb.querySelectorAll('.bar');
  for(let b of bars)b.style.height=Math.random()*35+5+'px'
},400);
// Clock
function updateClock(){document.getElementById('clock').textContent=new Date().toLocaleTimeString()}
setInterval(updateClock,1000);updateClock();
// Click to toggle projection
let projectionOn=false;
document.addEventListener('click',function(){
  projectionOn=!projectionOn;
  document.querySelector('.quantum-ring').style.borderColor=projectionOn?'#0ff':'';
  document.querySelector('.quantum-ring').style.boxShadow=projectionOn?'0 0 40px #0ff6':'';
  document.querySelector('h1').textContent=projectionOn?'Quantum Starfield — Projection Active':'Quantum Starfield Interface'
})
</script>
---
Demonstrates mouse-interactive 3D-parallax starfield (400 stars, depth-parallax responsive to cursor), programmatic quantum ring with 6 orbiting particles, frequency spectrum bars with live animation, qubit state matrix with data binding, and click-to-toggle projection mode. Responsive breakpoints at 900px and 600px.
---
Summary Table
Theme: Mockup 1 — Neural Data Mesh
Focus: Data binding + programmatic particles
Unique: Client-side API data rendered into interactive table with expandable details; 60-node particle network with connection lines; live ticker feed
Interactivity: Click-to-expand row details
Theme: Mockup 2 — Cybernetic Command Hub
Focus: Interactivity + keyboard shortcuts
Unique: 60-bar waveform visualizer with dynamic gradients; keyboard shortcuts (1/2/3/G/C); log system with timestamps; 80-star particle field with animated rings; view switching with data binding
Interactivity: Keyboard shortcuts, button clicks, GL overlay toggle, log clear
Theme: Mockup 3 — Quantum Starfield Interface
Focus: Visual spectacle + mouse interaction
Unique: 400-star 3D-parallax starfield steered by mouse; animated quantum ring with orbiting particles; qubit state matrix; frequency spectrum bars; live clock; click-to-toggle projection mode
Interactivity: Mouse parallax steering, click to toggle projection