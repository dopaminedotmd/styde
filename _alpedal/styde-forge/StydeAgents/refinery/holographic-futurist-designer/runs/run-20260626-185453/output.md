--- Mockup 1: Holographic System Core ---
Interactive radial holodashboard with click-driven state toggles and responsive grid reflow.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic System Core</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--neon-cyan:#00f5ff;--neon-magenta:#ff00e6;--neon-amber:#ffb347;--neon-green:#39ff14;--bg-deep:#08081a;--bg-panel:rgba(10,10,35,0.75);--glow-cyan:0 0 15px rgba(0,245,255,0.4),0 0 40px rgba(0,245,255,0.15);--glow-magenta:0 0 15px rgba(255,0,230,0.4),0 0 40px rgba(255,0,230,0.15);--radius:12px;--font:'Courier New',monospace}
body{background:var(--bg-deep);color:#c8d6e5;font-family:var(--font);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(0,245,255,0.03) 0%,transparent 60%),radial-gradient(ellipse at 70% 80%,rgba(255,0,230,0.02) 0%,transparent 60%);pointer-events:none;z-index:0}
.scanline{position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,245,255,0.015) 2px,rgba(0,245,255,0.015) 4px);pointer-events:none;z-index:1}
.core-wrap{position:relative;z-index:2;width:100%;max-width:1200px}
.core-header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;margin-bottom:24px;border-bottom:1px solid rgba(0,245,255,0.15);flex-wrap:wrap;gap:12px}
.core-header h1{font-size:1.4em;letter-spacing:4px;text-transform:uppercase;color:var(--neon-cyan);text-shadow:var(--glow-cyan)}
.core-header h1 span{color:var(--neon-magenta);text-shadow:var(--glow-magenta)}
.status-badge{display:flex;align-items:center;gap:8px;font-size:0.75em;letter-spacing:2px;border:1px solid rgba(0,245,255,0.3);padding:6px 14px;border-radius:20px;background:rgba(0,245,255,0.05)}
.status-badge .dot{width:8px;height:8px;border-radius:50%;background:var(--neon-green);box-shadow:0 0 10px var(--neon-green);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:0.3}}
.core-grid{display:grid;grid-template-columns:2fr 1fr;gap:20px}
.holo-card{background:var(--bg-panel);border:1px solid rgba(0,245,255,0.12);border-radius:var(--radius);padding:20px;backdrop-filter:blur(8px);position:relative;overflow:hidden}
.holo-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--neon-cyan),var(--neon-magenta),transparent);opacity:0.6}
.holo-card h2{font-size:0.8em;letter-spacing:3px;text-transform:uppercase;color:rgba(200,214,229,0.6);margin-bottom:16px}
.radial-container{display:flex;justify-content:center;align-items:center;padding:10px 0}
.radial-chart{position:relative;width:200px;height:200px;cursor:pointer}
.radial-chart svg{width:100%;height:100%;transform:rotate(-90deg)}
.radial-chart .bg-ring{fill:none;stroke:rgba(0,245,255,0.1);stroke-width:8}
.radial-chart .progress-ring{fill:none;stroke:var(--neon-cyan);stroke-width:8;stroke-linecap:round;stroke-dasharray:502.65;stroke-dashoffset:150.8;transition:stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1),stroke 0.4s}
.radial-chart .progress-ring.magenta{stroke:var(--neon-magenta)}
.radial-chart .progress-ring.amber{stroke:var(--neon-amber)}
.radial-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;pointer-events:none}
.radial-center .value{font-size:2.2em;font-weight:bold;color:var(--neon-cyan);text-shadow:var(--glow-cyan)}
.radial-center .label{font-size:0.6em;letter-spacing:2px;color:rgba(200,214,229,0.5)}
.metrics-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}
.metric-item{border:1px solid rgba(0,245,255,0.08);border-radius:8px;padding:12px;background:rgba(0,0,0,0.2);transition:border-color 0.3s,background 0.3s;cursor:pointer}
.metric-item:hover,.metric-item.active{border-color:rgba(0,245,255,0.4);background:rgba(0,245,255,0.05)}
.metric-item .m-label{font-size:0.6em;letter-spacing:1px;color:rgba(200,214,229,0.5)}
.metric-item .m-value{font-size:1.3em;font-weight:bold;margin-top:4px;color:var(--neon-cyan);text-shadow:0 0 10px rgba(0,245,255,0.3)}
.metric-item .m-value.hot{color:var(--neon-magenta);text-shadow:0 0 10px rgba(255,0,230,0.3)}
.metric-item .m-value.warn{color:var(--neon-amber);text-shadow:0 0 10px rgba(255,179,71,0.3)}
.side-stack{display:flex;flex-direction:column;gap:20px}
.activity-feed{max-height:220px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(0,245,255,0.2) transparent}
.activity-feed::-webkit-scrollbar{width:4px}
.activity-feed::-webkit-scrollbar-thumb{background:rgba(0,245,255,0.2);border-radius:4px}
.activity-item{padding:8px 0;border-bottom:1px solid rgba(0,245,255,0.05);display:flex;gap:10px;align-items:flex-start;opacity:0;animation:fadeIn 0.4s forwards}
.activity-item .time{font-size:0.65em;color:rgba(200,214,229,0.4);white-space:nowrap;min-width:50px}
.activity-item .text{font-size:0.75em;color:rgba(200,214,229,0.7)}
.activity-item .marker{width:4px;height:4px;border-radius:50%;background:var(--neon-cyan);margin-top:6px;flex-shrink:0;box-shadow:0 0 8px var(--neon-cyan)}
@keyframes fadeIn{to{opacity:1}}
.toggle-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.toggle-btn{font-family:var(--font);font-size:0.65em;letter-spacing:1px;padding:8px 16px;border:1px solid rgba(0,245,255,0.2);border-radius:6px;background:rgba(0,245,255,0.03);color:rgba(200,214,229,0.7);cursor:pointer;transition:all 0.3s;text-transform:uppercase}
.toggle-btn:hover{border-color:var(--neon-cyan);color:var(--neon-cyan);box-shadow:0 0 12px rgba(0,245,255,0.15)}
.toggle-btn.on{border-color:var(--neon-cyan);background:rgba(0,245,255,0.1);color:var(--neon-cyan);box-shadow:0 0 15px rgba(0,245,255,0.2)}
.toggle-btn.on.mag{border-color:var(--neon-magenta);background:rgba(255,0,230,0.1);color:var(--neon-magenta);box-shadow:0 0 15px rgba(255,0,230,0.2)}
.bottom-bar{display:flex;justify-content:space-between;align-items:center;margin-top:20px;padding:12px 16px;border:1px solid rgba(0,245,255,0.08);border-radius:var(--radius);background:rgba(0,0,0,0.3);flex-wrap:wrap;gap:10px}
.bottom-bar span{font-size:0.7em;letter-spacing:1px;color:rgba(200,214,229,0.5)}
.pulse-ring{position:absolute;inset:0;border-radius:var(--radius);border:1px solid rgba(0,245,255,0.05);animation:borderPulse 4s ease-in-out infinite;pointer-events:none}
@keyframes borderPulse{0%,100%{border-color:rgba(0,245,255,0.05)}50%{border-color:rgba(0,245,255,0.15)}}
.particles{position:absolute;inset:0;overflow:hidden;pointer-events:none;border-radius:var(--radius)}
.particle{position:absolute;width:2px;height:2px;background:var(--neon-cyan);border-radius:50%;opacity:0;animation:floatParticle 8s infinite}
@keyframes floatParticle{0%{transform:translateY(100%) scale(0);opacity:0}10%{opacity:0.6}90%{opacity:0.4}100%{transform:translateY(-20px) scale(1);opacity:0}}
@media(max-width:768px){
.core-grid{grid-template-columns:1fr}
.core-header h1{font-size:1em}
.radial-chart{width:160px;height:160px}
.metrics-grid{grid-template-columns:1fr}
.side-stack{gap:16px}
.activity-feed{max-height:160px}
.bottom-bar{flex-direction:column;align-items:stretch;text-align:center}
}
@media(max-width:480px){
body{padding:10px}
.holo-card{padding:14px}
.radial-chart{width:130px;height:130px}
.metric-item{padding:10px}
}
</style>
</head>
<body>
<div class="scanline"></div>
<div class="core-wrap">
<div class="core-header">
<h1>Holo<span>Core</span> SYSTEM</h1>
<div class="status-badge"><span class="dot"></span>ONLINE</div>
</div>
<div class="core-grid">
<div class="holo-card">
<div class="particles" id="particles1"></div>
<div class="pulse-ring"></div>
<h2>Core Performance</h2>
<div class="radial-container">
<div class="radial-chart" id="radialChart" data-metric="cpu">
<svg viewBox="0 0 180 180">
<circle class="bg-ring" cx="90" cy="90" r="80"/>
<circle class="progress-ring" id="progressRing" cx="90" cy="90" r="80"/>
</svg>
<div class="radial-center">
<span class="value" id="radialValue">78%</span>
<span class="label" id="radialLabel">CPU LOAD</span>
</div>
</div>
</div>
<div class="toggle-row">
<button class="toggle-btn on" data-metric="cpu">CPU</button>
<button class="toggle-btn" data-metric="mem">MEM</button>
<button class="toggle-btn" data-metric="net">NET</button>
<button class="toggle-btn mag" data-metric="temp">TEMP</button>
</div>
<div class="metrics-grid" id="metricsGrid">
<div class="metric-item active" data-metric="cpu"><div class="m-label">CPU LOAD</div><div class="m-value">78.4%</div></div>
<div class="metric-item" data-metric="mem"><div class="m-label">MEMORY</div><div class="m-value" id="memVal">44.2 GB</div></div>
<div class="metric-item" data-metric="net"><div class="m-label">NETWORK</div><div class="m-value" id="netVal">1.2 Gbps</div></div>
<div class="metric-item" data-metric="temp"><div class="m-label warning">TEMP</div><div class="m-value warn" id="tempVal">72.8 C</div></div>
</div>
</div>
<div class="side-stack">
<div class="holo-card">
<div class="particles"></div>
<h2>Event Log</h2>
<div class="activity-feed" id="activityFeed">
<div class="activity-item" style="animation-delay:0.1s"><span class="marker"></span><span class="time">14:32</span><span class="text">System sync complete</span></div>
<div class="activity-item" style="animation-delay:0.2s"><span class="marker"></span><span class="time">14:28</span><span class="text">Anomaly detected in sector 7G</span></div>
<div class="activity-item" style="animation-delay:0.3s"><span class="marker"></span><span class="time">14:21</span><span class="text">Data pipeline rebalanced</span></div>
<div class="activity-item" style="animation-delay:0.4s"><span class="marker"></span><span class="time">14:15</span><span class="text">Heat sink efficiency at 92%</span></div>
<div class="activity-item" style="animation-delay:0.5s"><span class="marker"></span><span class="time">14:08</span><span class="text">Neural core handshake OK</span></div>
</div>
</div>
<div class="holo-card">
<div class="particles"></div>
<h2>Quick Controls</h2>
<button class="toggle-btn on" id="btnAutoBalance" style="margin-bottom:6px">AUTO-BALANCE</button>
<button class="toggle-btn" id="btnDiagnostic">DIAGNOSTIC MODE</button>
<button class="toggle-btn mag" id="btnOverclock">OVERCLOCK</button>
<div class="bottom-bar">
<span>CORE v4.2.1</span>
<span id="uptimeDisplay">UPTIME: 47h 12m</span>
</div>
</div>
</div>
</div>
</div>
<div style="height:20px"></div>
<div class="core-wrap">
<div class="core-grid">
<div class="holo-card">
<div class="particles"></div>
<div class="pulse-ring"></div>
<h2>Subsystem Health</h2>
<div style="display:flex;flex-direction:column;gap:12px">
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:0.7em;letter-spacing:1px;color:rgba(200,214,229,0.6)">COOLANT PUMP</span><div style="display:flex;gap:4px"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot" style="background:var(--bg-deep);box-shadow:none"></span></div></div>
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:0.7em;letter-spacing:1px;color:rgba(200,214,229,0.6)">OPTIC RELAY</span><div style="display:flex;gap:4px"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:0.7em;letter-spacing:1px;color:rgba(200,214,229,0.6)">SIGNAL FILTER</span><div style="display:flex;gap:4px"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dot" style="background:var(--neon-amber);box-shadow:0 0 8px var(--neon-amber)"></span><span class="dot" style="background:var(--bg-deep);box-shadow:none"></span></div></div>
</div>
<button class="toggle-btn" id="btnRefreshHealth" style="margin-top:14px;width:100%">REFRESH ALL</button>
</div>
<div class="holo-card">
<div class="particles"></div>
<h2>Power Distribution</h2>
<div class="radial-container">
<div style="display:flex;gap:24px;flex-wrap:wrap;justify-content:center">
<div style="text-align:center"><div style="width:60px;height:60px;border-radius:50%;border:3px solid var(--neon-cyan);display:flex;align-items:center;justify-content:center;font-size:1.1em;font-weight:bold;color:var(--neon-cyan);text-shadow:var(--glow-cyan)">62%</div><div style="font-size:0.55em;letter-spacing:1px;margin-top:6px;color:rgba(200,214,229,0.5)">PWR A</div></div>
<div style="text-align:center"><div style="width:60px;height:60px;border-radius:50%;border:3px solid var(--neon-magenta);display:flex;align-items:center;justify-content:center;font-size:1.1em;font-weight:bold;color:var(--neon-magenta);text-shadow:var(--glow-magenta)">88%</div><div style="font-size:0.55em;letter-spacing:1px;margin-top:6px;color:rgba(200,214,229,0.5)">PWR B</div></div>
<div style="text-align:center"><div style="width:60px;height:60px;border-radius:50%;border:3px solid var(--neon-amber);display:flex;align-items:center;justify-content:center;font-size:1.1em;font-weight:bold;color:var(--neon-amber);text-shadow:0 0 10px rgba(255,179,71,0.3)">41%</div><div style="font-size:0.55em;letter-spacing:1px;margin-top:6px;color:rgba(200,214,229,0.5)">PWR C</div></div>
</div>
</div>
</div>
</div>
</div>
<script>
(function(){
var ring=document.getElementById('progressRing');
var valEl=document.getElementById('radialValue');
var labelEl=document.getElementById('radialLabel');
var btnRow=document.querySelectorAll('.toggle-btn[data-metric]');
var metricItems=document.querySelectorAll('.metric-item');
var metrics={
cpu:{val:78.4,unit:'%',offset:150.8,color:'--neon-cyan',cls:''},
mem:{val:44.2,unit:'GB',offset:201.06,color:'--neon-cyan',cls:''},
net:{val:1.2,unit:'Gbps',offset:251.32,color:'--neon-cyan',cls:''},
temp:{val:72.8,unit:'C',offset:301.59,color:'--neon-magenta',cls:'magenta'}
};
function setMetric(metric){
var m=metrics[metric];
if(!m)return;
var circumference=502.65;
var pct=m.val/(metric==='mem'?64:metric==='net'?10:metric==='temp'?120:100);
var offset=circumference-(pct*circumference);
if(metric==='cpu')offset=m.offset;
ring.style.strokeDashoffset=offset;
ring.classList.toggle('magenta',metric==='temp');
ring.classList.toggle('amber',metric==='net'&&m.val>5);
valEl.textContent=metric==='temp'?m.val+m.unit:metric==='net'?m.val+' '+m.unit:m.val+(metric==='mem'?' '+m.unit:m.unit);
labelEl.textContent=metric.toUpperCase()+' '+(metric==='mem'?'USAGE':metric==='temp'?'TEMP':'LOAD');
btnRow.forEach(function(b){b.classList.toggle('on',b.dataset.metric===metric);b.classList.toggle('mag',metric==='temp');});
metricItems.forEach(function(it){it.classList.toggle('active',it.dataset.metric===metric);});
}
btnRow.forEach(function(b){b.addEventListener('click',function(e){setMetric(e.target.dataset.metric);});});
metricItems.forEach(function(it){it.addEventListener('click',function(e){var met=e.currentTarget.dataset.metric;if(met)setMetric(met);});});
document.getElementById('btnAutoBalance').addEventListener('click',function(e){e.target.classList.toggle('on');});
document.getElementById('btnDiagnostic').addEventListener('click',function(e){e.target.classList.toggle('on');});
document.getElementById('btnOverclock').addEventListener('click',function(e){e.target.classList.toggle('on');e.target.classList.toggle('mag');});
document.getElementById('btnRefreshHealth').addEventListener('click',function(){alert('[HOLO] Subsystem health refreshed.');});
var particlesContainers=document.querySelectorAll('.particles');
particlesContainers.forEach(function(container,ci){
for(var i=0;i<12;i++){
var p=document.createElement('div');
p.className='particle';
p.style.left=(Math.random()*100)+'%';
p.style.animationDelay=(Math.random()*8)+'s';
p.style.animationDuration=(6+Math.random()*6)+'s';
p.style.background=ci%2===0?'var(--neon-cyan)':'var(--neon-magenta)';
container.appendChild(p);
}
});
var uptimeEl=document.getElementById('uptimeDisplay');
var uptimeHours=47;
var uptimeMin=12;
setInterval(function(){uptimeMin++;if(uptimeMin>=60){uptimeHours++;uptimeMin=0;}
uptimeEl.textContent='UPTIME: '+uptimeHours+'h '+uptimeMin+'m';},60000);
var feed=document.getElementById('activityFeed');
var logMsgs=['Packet loss normalized','Thermal threshold stable','Neural sync acquired','Sector scan complete','Memory defrag done','Core heartbeat verified'];
var logIdx=0;
setInterval(function(){var d=new Date();var h=String(d.getHours()).padStart(2,'0');var m=String(d.getMinutes()).padStart(2,'0');var item=document.createElement('div');item.className='activity-item';item.innerHTML='<span class="marker"></span><span class="time">'+h+':'+m+'</span><span class="text">'+logMsgs[logIdx%logMsgs.length]+'</span>';feed.insertBefore(item,feed.firstChild);if(feed.children.length>12)feed.removeChild(feed.lastChild);logIdx++;},8000);
setMetric('cpu');
})();
</script>
</body>
</html>
```
---
--- Mockup 2: Neural Flux Analyzer ---
Click-driven node graph with keyboard shortcut toggles and responsive container query layout.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neural Flux Analyzer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--flux-cyan:#00e5ff;--flux-violet:#b388ff;--flux-pink:#ff4081;--flux-lime:#76ff03;--bg-deep:#0a0a1a;--bg-card:rgba(12,12,35,0.8);--glow-cyan:0 0 12px rgba(0,229,255,0.35),0 0 35px rgba(0,229,255,0.1);--glow-violet:0 0 12px rgba(179,136,255,0.35),0 0 35px rgba(179,136,255,0.1);--radius:10px;--font:'Courier New',monospace}
body{background:var(--bg-deep);color:#c0c8e0;font-family:var(--font);min-height:100vh;padding:16px;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(circle at 60% 40%,rgba(179,136,255,0.02) 0%,transparent 50%),radial-gradient(circle at 20% 80%,rgba(0,229,255,0.015) 0%,transparent 50%);pointer-events:none;z-index:0}
.scan-overlay{position:fixed;inset:0;background:repeating-linear-gradient(90deg,transparent,transparent 3px,rgba(0,229,255,0.008) 3px,rgba(0,229,255,0.008) 6px);pointer-events:none;z-index:1}
.flux-wrap{position:relative;z-index:2;max-width:1300px;margin:0 auto}
.top-bar{display:flex;justify-content:space-between;align-items:center;padding:12px 0;margin-bottom:16px;border-bottom:1px solid rgba(179,136,255,0.12);flex-wrap:wrap;gap:10px}
.top-bar h1{font-size:1.3em;letter-spacing:5px;color:var(--flux-cyan);text-shadow:var(--glow-cyan)}.top-bar h1 em{font-style:normal;color:var(--flux-violet);text-shadow:var(--glow-violet)}
.top-bar .kbd-hint{font-size:0.6em;letter-spacing:1px;color:rgba(192,200,224,0.4);border:1px solid rgba(179,136,255,0.15);padding:4px 12px;border-radius:4px}
.grid-2col{display:grid;grid-template-columns:3fr 2fr;gap:18px}
.flux-card{background:var(--bg-card);border:1px solid rgba(0,229,255,0.08);border-radius:var(--radius);padding:18px;backdrop-filter:blur(6px);position:relative;overflow:hidden}
.flux-card::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--flux-cyan),var(--flux-violet),transparent);opacity:0.5}
.flux-card h2{font-size:0.7em;letter-spacing:3px;text-transform:uppercase;color:rgba(192,200,224,0.5);margin-bottom:12px}
.node-canvas-wrap{position:relative;width:100%;aspect-ratio:4/3;border:1px solid rgba(0,229,255,0.06);border-radius:8px;background:rgba(0,0,0,0.3);overflow:hidden;cursor:crosshair}
.node-canvas-wrap canvas{width:100%;height:100%;display:block}
.canvas-label{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);font-size:0.55em;letter-spacing:2px;color:rgba(192,200,224,0.2);pointer-events:none}
.viz-controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.viz-btn{font-family:var(--font);font-size:0.6em;letter-spacing:1px;padding:6px 14px;border:1px solid rgba(0,229,255,0.15);border-radius:5px;background:rgba(0,229,255,0.02);color:rgba(192,200,224,0.6);cursor:pointer;transition:all 0.25s;text-transform:uppercase}
.viz-btn:hover{border-color:var(--flux-cyan);color:var(--flux-cyan);box-shadow:0 0 10px rgba(0,229,255,0.1)}
.viz-btn.active{border-color:var(--flux-violet);background:rgba(179,136,255,0.08);color:var(--flux-violet);box-shadow:0 0 12px rgba(179,136,255,0.12)}
.viz-btn.pulse{animation:vizPulse 0.6s ease}
@keyframes vizPulse{0%{box-shadow:0 0 0 0 rgba(0,229,255,0.4)}100%{box-shadow:0 0 0 12px transparent}}
.stat-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(0,229,255,0.04);flex-wrap:wrap}
.stat-row .s-label{font-size:0.6em;letter-spacing:1px;color:rgba(192,200,224,0.4)}
.stat-row .s-value{font-size:0.85em;color:var(--flux-cyan);text-shadow:0 0 8px rgba(0,229,255,0.2)}
.stat-row .s-value.highlight{color:var(--flux-pink);text-shadow:0 0 8px rgba(255,64,129,0.2)}
.node-list{max-height:240px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(0,229,255,0.15) transparent}
.node-list::-webkit-scrollbar{width:3px}
.node-list::-webkit-scrollbar-thumb{background:rgba(0,229,255,0.15);border-radius:3px}
.node-entry{display:flex;justify-content:space-between;align-items:center;padding:6px 8px;border-bottom:1px solid rgba(0,229,255,0.04);cursor:pointer;transition:background 0.2s;font-size:0.7em;letter-spacing:0.5px}
.node-entry:hover{background:rgba(0,229,255,0.04)}
.node-entry .n-name{color:rgba(192,200,224,0.7)}
.node-entry .n-val{color:var(--flux-cyan);text-shadow:0 0 6px rgba(0,229,255,0.15)}
.node-entry .n-val.hot{color:var(--flux-pink);text-shadow:0 0 6px rgba(255,64,129,0.15)}
.node-entry .n-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-right:8px}
.flux-footer{display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding:10px 14px;border:1px solid rgba(179,136,255,0.08);border-radius:8px;background:rgba(0,0,0,0.25);flex-wrap:wrap;gap:8px;font-size:0.65em;letter-spacing:1px;color:rgba(192,200,224,0.4)}
.flux-footer .key{color:var(--flux-violet)}
@container(min-width:600px){.node-list{max-height:300px}}
@media(max-width:820px){.grid-2col{grid-template-columns:1fr}}
@media(max-width:480px){
body{padding:8px}
.flux-card{padding:12px}
.top-bar h1{font-size:1em}
.stat-row{flex-direction:column;gap:2px}
.node-canvas-wrap{aspect-ratio:3/2}
}
</style>
</head>
<body>
<div class="scan-overlay"></div>
<div class="flux-wrap">
<div class="top-bar">
<h1>NEURAL <em>FLUX</em> v2</h1>
<div class="kbd-hint">[N] new &nbsp; [R] reset &nbsp; [1-3] layout</div>
</div>
<div class="grid-2col">
<div class="flux-card" style="container-type:inline-size">
<h2>Node Topology</h2>
<div class="node-canvas-wrap">
<canvas id="fluxCanvas"></canvas>
<div class="canvas-label">click nodes to inspect &middot; drag to explore</div>
</div>
<div class="viz-controls">
<button class="viz-btn active" id="layoutBtn1">FORCE</button>
<button class="viz-btn" id="layoutBtn2">RADIAL</button>
<button class="viz-btn" id="layoutBtn3">GRID</button>
<button class="viz-btn" id="addNodeBtn">+ NODE</button>
<button class="viz-btn" id="resetBtn">RESET</button>
</div>
</div>
<div class="flux-card">
<h2>Node Inspector</h2>
<div style="margin-bottom:10px">
<div class="stat-row"><span class="s-label">ACTIVE NODES</span><span class="s-value" id="nodeCount">0</span></div>
<div class="stat-row"><span class="s-label">EDGE COUNT</span><span class="s-value" id="edgeCount">0</span></div>
<div class="stat-row"><span class="s-label">SELECTED</span><span class="s-value" id="selectedLabel">NONE</span></div>
<div class="stat-row"><span class="s-label">AVG SIGNAL</span><span class="s-value highlight" id="avgSignal">0.00</span></div>
</div>
<h2 style="margin-top:6px">Active Nodes</h2>
<div class="node-list" id="nodeList"></div>
</div>
</div>
<div class="flux-footer">
<span>press <span class="key">H</span> for keyboard help</span>
<span>COMPOSITE v2.4</span>
<span id="frameCounter">FPS: 60</span>
</div>
</div>
<script>
(function(){
var canvas=document.getElementById('fluxCanvas');
var ctx=canvas.getContext('2d');
var nodes=[];var edges=[];var selectedId=null;var layoutMode=0;
var colors=['#00e5ff','#b388ff','#ff4081','#76ff03','#ffd740'];
var colorGlows=['rgba(0,229,255,0.3)','rgba(179,136,255,0.3)','rgba(255,64,129,0.3)','rgba(118,255,3,0.3)','rgba(255,215,64,0.3)'];
var seedNames=['AETHER','NEXUS','ORION','VECTOR','PRISM','ECHO','DRIFT','PHASE','CIPHER','LUMEN','SOLAR','TANGLE'];
function resize(){var rect=canvas.parentElement.getBoundingClientRect();canvas.width=rect.width-2;canvas.height=rect.height-2;drawScene();}
window.addEventListener('resize',resize);
function initGraph(){
nodes=[];edges=[];
for(var i=0;i<8;i++){
var a=Math.random()*Math.PI*2;
var r=Math.random()*0.35+0.2;
nodes.push({id:i,x:0.5+Math.cos(a)*r*0.8,y:0.5+Math.sin(a)*r*0.8,vx:0,vy:0,label:seedNames[i%seedNames.length],color:colors[i%colors.length],signal:Math.random()*100});
}
for(var i=0;i<10;i++){var a=Math.floor(Math.random()*nodes.length);var b=Math.floor(Math.random()*nodes.length);if(a!==b&&!edges.some(function(e){return(e.a===a&&e.b===b)||(e.a===b&&e.b===a);}))edges.push({a:a,b:b,strength:Math.random()});}
selectedId=null;layoutMode=0;updateStats();
}
function layoutForce(){
var w=canvas.width;var h=canvas.height;
if(w<1||h<1)return;
for(var iter=0;iter<50;iter++){
for(var i=0;i<nodes.length;i++){nodes[i].vx=0;nodes[i].vy=0;}
var rep=0.002;var att=0.0005;var damp=0.85;
for(var i=0;i<nodes.length;i++){for(var j=i+1;j<nodes.length;j++){var dx=nodes[j].x-nodes[i].x;var dy=nodes[j].y-nodes[i].y;var d=Math.sqrt(dx*dx+dy*dy)||0.001;var f=rep/(d*d);nodes[i].vx-=f*dx/d;nodes[i].vy-=f*dy/d;nodes[j].vx+=f*dx/d;nodes[j].vy+=f*dy/d;}}
for(var e=0;e<edges.length;e++){var a=nodes[edges[e].a];var b=nodes[edges[e].b];var dx=b.x-a.x;var dy=b.y-a.y;var d=Math.sqrt(dx*dx+dy*dy)||0.001;var f=(d-0.2)*att*10;var fx=f*dx/d;var fy=f*dy/d;a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;}
var cx=0;var cy=0;for(var i=0;i<nodes.length;i++){cx+=nodes[i].x;cy+=nodes[i].y;}cx/=nodes.length;cy/=nodes.length;
for(var i=0;i<nodes.length;i++){nodes[i].vx+=(0.5-cx)*0.0005;nodes[i].vy+=(0.5-cy)*0.0005;nodes[i].vx*=damp;nodes[i].vy*=damp;nodes[i].x+=nodes[i].vx;nodes[i].y+=nodes[i].vy;nodes[i].x=Math.max(0.05,Math.min(0.95,nodes[i].x));nodes[i].y=Math.max(0.05,Math.min(0.95,nodes[i].y));}
}
}
function layoutRadial(){
var cx=0.5;var cy=0.5;
for(var i=0;i<nodes.length;i++){var a=(i/nodes.length)*Math.PI*2;var r=0.32;nodes[i].x=cx+Math.cos(a)*r;nodes[i].y=cy+Math.sin(a)*r;}
}
function layoutGrid(){
var cols=Math.ceil(Math.sqrt(nodes.length));
for(var i=0;i<nodes.length;i++){var row=Math.floor(i/cols);var col=i%cols;nodes[i].x=0.1+col*(0.8/(cols-1||1));nodes[i].y=0.1+row*(0.8/(Math.ceil(nodes.length/cols)-1||1));}
}
function applyLayout(mode){
if(mode===0)layoutForce();
else if(mode===1)layoutRadial();
else if(mode===2)layoutGrid();
drawScene();
}
function drawScene(){
var w=canvas.width;var h=canvas.height;
if(w<1||h<1)return;
ctx.clearRect(0,0,w,h);
ctx.fillStyle='rgba(0,0,0,0.15)';ctx.fillRect(0,0,w,h);
var gx=w*0.02;var gy=h*0.02;ctx.strokeStyle='rgba(0,229,255,0.02)';ctx.lineWidth=1;
for(var i=0;i<20;i++){ctx.beginPath();ctx.moveTo(i*gx,0);ctx.lineTo(i*gx,h);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*gy);ctx.lineTo(w,i*gy);ctx.stroke();}
for(var e=0;e<edges.length;e++){var a=nodes[edges[e].a];var b=nodes[edges[e].b];if(!a||!b)continue;var ax=a.x*w;var ay=a.y*h;var bx=b.x*w;var by=b.y*h;ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(bx,by);ctx.strokeStyle='rgba(0,229,255,'+(0.1+edges[e].strength*0.3)+')';ctx.lineWidth=1+edges[e].strength*2;ctx.stroke();}
for(var i=0;i<nodes.length;i++){var n=nodes[i];var nx=n.x*w;var ny=n.y*h;var r=Math.max(12,18*(n.signal/100));var isSel=selectedId===n.id;ctx.beginPath();ctx.arc(nx,ny,r,0,Math.PI*2);var col=n.color;var glow='rgba(0,229,255,0.08)';if(isSel){glow=colorGlows[colors.indexOf(col)]||'rgba(0,229,255,0.15)';}ctx.shadowColor=col;ctx.shadowBlur=isSel?25:12;ctx.fillStyle=col+(isSel?'0.35':'0.15');ctx.fill();ctx.shadowBlur=0;ctx.beginPath();ctx.arc(nx,ny,r*0.6,0,Math.PI*2);ctx.fillStyle=col+'0.5';ctx.fill();ctx.beginPath();ctx.arc(nx,ny,3,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='rgba(200,200,220,0.6)';ctx.font='9px Courier New';ctx.textAlign='center';ctx.fillText(n.label,nx,ny+r+12);}
if(selectedId!==null){var sn=nodes[selectedId];if(sn){var sx=sn.x*w;var sy=sn.y*h;ctx.beginPath();ctx.arc(sx,sy,28,0,Math.PI*2);ctx.strokeStyle=sn.color+'0.4';ctx.lineWidth=1;ctx.setLineDash([4,4]);ctx.stroke();ctx.setLineDash([]);}}
}
function updateStats(){
document.getElementById('nodeCount').textContent=nodes.length;
document.getElementById('edgeCount').textContent=edges.length;
document.getElementById('selectedLabel').textContent=selectedId!==null?nodes[selectedId]&&nodes[selectedId].label||'NONE':'NONE';
var sum=0;for(var i=0;i<nodes.length;i++)sum+=nodes[i].signal;
document.getElementById('avgSignal').textContent=(nodes.length?(sum/nodes.length).toFixed(1):'0.00')+' %';
renderNodeList();
}
function renderNodeList(){
var el=document.getElementById('nodeList');el.innerHTML='';
nodes.forEach(function(n,i){
var div=document.createElement('div');div.className='node-entry';
div.innerHTML='<span class="n-dot" style="background:'+n.color+';box-shadow:0 0 6px '+n.color+'40"></span><span class="n-name">'+n.label+'</span><span class="n-val'+(n.signal>70?' hot':'')+'">'+n.signal.toFixed(1)+'%</span>';
if(selectedId===i)div.style.background='rgba(0,229,255,0.06)';
div.addEventListener('click',function(id){return function(){selectedId=(selectedId===id)?null:id;drawScene();updateStats();};}(i));
el.appendChild(div);
});
}
function addNode(){
var nid=nodes.length;
var x=0.2+Math.random()*0.6;var y=0.2+Math.random()*0.6;
nodes.push({id:nid,x:x,y:y,vx:0,vy:0,label:seedNames[nid%seedNames.length],color:colors[nid%colors.length],signal:Math.random()*100});
if(nodes.length>1){var conn=Math.floor(Math.random()*(nodes.length-1));edges.push({a:nid,b:conn,strength:Math.random()});}
if(layoutMode===0)layoutForce();
else if(layoutMode===1)layoutRadial();
else if(layoutMode===2)layoutGrid();
drawScene();updateStats();
}
canvas.addEventListener('click',function(e){
var rect=canvas.getBoundingClientRect();
var mx=(e.clientX-rect.left)/canvas.width;
var my=(e.clientY-rect.top)/canvas.height;
var found=null;var minDist=0.06;
for(var i=0;i<nodes.length;i++){var dx=mx-nodes[i].x;var dy=my-nodes[i].y;var d=Math.sqrt(dx*dx+dy*dy);if(d<minDist){minDist=d;found=i;}}
selectedId=(found!==null&&found===selectedId)?null:found;
drawScene();updateStats();
});
window.addEventListener('keydown',function(e){
var k=e.key.toLowerCase();
if(k==='n'){addNode();e.preventDefault();}
else if(k==='r'){initGraph();if(layoutMode===0)layoutForce();else if(layoutMode===1)layoutRadial();else if(layoutMode===2)layoutGrid();drawScene();updateStats();e.preventDefault();}
else if(k==='1'){layoutMode=0;document.querySelectorAll('.viz-btn')[0].classList.add('active');document.querySelectorAll('.viz-btn')[1].classList.remove('active');document.querySelectorAll('.viz-btn')[2].classList.remove('active');applyLayout(0);e.preventDefault();}
else if(k==='2'){layoutMode=1;document.querySelectorAll('.viz-btn')[1].classList.add('active');document.querySelectorAll('.viz-btn')[0].classList.remove('active');document.querySelectorAll('.viz-btn')[2].classList.remove('active');applyLayout(1);e.preventDefault();}
else if(k==='3'){layoutMode=2;document.querySelectorAll('.viz-btn')[2].classList.add('active');document.querySelectorAll('.viz-btn')[0].classList.remove('active');document.querySelectorAll('.viz-btn')[1].classList.remove('active');applyLayout(2);e.preventDefault();}
});
document.getElementById('layoutBtn1').addEventListener('click',function(){layoutMode=0;this.classList.add('active');document.getElementById('layoutBtn2').classList.remove('active');document.getElementById('layoutBtn3').classList.remove('active');applyLayout(0);});
document.getElementById('layoutBtn2').addEventListener('click',function(){layoutMode=1;this.classList.add('active');document.getElementById('layoutBtn1').classList.remove('active');document.getElementById('layoutBtn3').classList.remove('active');applyLayout(1);});
document.getElementById('layoutBtn3').addEventListener('click',function(){layoutMode=2;this.classList.add('active');document.getElementById('layoutBtn1').classList.remove('active');document.getElementById('layoutBtn2').classList.remove('active');applyLayout(2);});
document.getElementById('addNodeBtn').addEventListener('click',addNode);
document.getElementById('resetBtn').addEventListener('click',function(){initGraph();if(layoutMode===0)layoutForce();else if(layoutMode===1)layoutRadial();else if(layoutMode===2)layoutGrid();drawScene();updateStats();});
initGraph();resize();
var frameCount=0;var lastTime=performance.now();
function frameLoop(){frameCount++;var now=performance.now();if(now-lastTime>=1000){document.getElementById('frameCounter').textContent='FPS: '+frameCount;frameCount=0;lastTime=now;}
requestAnimationFrame(frameLoop);}
frameLoop();
setTimeout(function(){layoutForce();drawScene();updateStats();},50);
})();
</script>
</body>
</html>
```
---
--- Mockup 3: Quantum Terminal Interface ---
Input-driven holographic terminal with keyboard event capture and media-query-responsive layout.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quantum Terminal Interface</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--q-cyan:#0af;--q-magenta:#f0f;--q-amber:#fa0;--q-green:#0f0;--bg-void:#06060f;--bg-pane:rgba(8,8,20,0.85);--glow-cyan:0 0 10px rgba(0,170,255,0.3),0 0 30px rgba(0,170,255,0.08);--glow-magenta:0 0 10px rgba(255,0,255,0.3),0 0 30px rgba(255,0,255,0.08);--radius:8px;--font:'Courier New',monospace}
body{background:var(--bg-void);color:#b0b8d0;font-family:var(--font);min-height:100vh;padding:14px;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 40% 30%,rgba(0,170,255,0.015) 0%,transparent 50%),radial-gradient(ellipse at 80% 70%,rgba(255,0,255,0.01) 0%,transparent 50%);pointer-events:none;z-index:0}
.grid-overlay{position:fixed;inset:0;background-image:linear-gradient(rgba(0,170,255,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(0,170,255,0.02) 1px,transparent 1px);background-size:30px 30px;pointer-events:none;z-index:1}
.q-wrap{position:relative;z-index:2;max-width:1100px;margin:0 auto}
.q-header{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;margin-bottom:14px;border-bottom:1px solid rgba(0,170,255,0.1);flex-wrap:wrap;gap:8px}
.q-header h1{font-size:1.2em;letter-spacing:6px;color:var(--q-cyan);text-shadow:var(--glow-cyan)}.q-header h1 i{font-style:normal;color:var(--q-magenta);text-shadow:var(--glow-magenta)}
.q-header .prompt{font-size:0.6em;letter-spacing:2px;color:rgba(176,184,208,0.35);border:1px solid rgba(0,170,255,0.1);padding:4px 12px;border-radius:4px}
.q-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.q-pane{background:var(--bg-pane);border:1px solid rgba(0,170,255,0.06);border-radius:var(--radius);padding:16px;backdrop-filter:blur(5px);position:relative;overflow:hidden}
.q-pane::before{content:'';position:absolute;top:0;left:20%;right:20%;height:1px;background:linear-gradient(90deg,transparent,var(--q-cyan),transparent);opacity:0.4}
.q-pane h2{font-size:0.65em;letter-spacing:4px;text-transform:uppercase;color:rgba(176,184,208,0.4);margin-bottom:10px}
.terminal-screen{background:rgba(0,0,0,0.4);border:1px solid rgba(0,170,255,0.05);border-radius:5px;padding:12px;min-height:260px;max-height:320px;overflow-y:auto;font-size:0.7em;line-height:1.5;scrollbar-width:thin;scrollbar-color:rgba(0,170,255,0.1) transparent}
.terminal-screen::-webkit-scrollbar{width:3px}
.terminal-screen::-webkit-scrollbar-thumb{background:rgba(0,170,255,0.1);border-radius:3px}
.terminal-screen .t-line{opacity:0;animation:tFadeIn 0.3s forwards;word-break:break-all}
.terminal-screen .t-line.system{color:var(--q-cyan);text-shadow:0 0 6px rgba(0,170,255,0.2)}
.terminal-screen .t-line.output{color:rgba(176,184,208,0.6)}
.terminal-screen .t-line.error{color:var(--q-magenta);text-shadow:0 0 6px rgba(255,0,255,0.2)}
.terminal-screen .t-line.data{color:var(--q-green);text-shadow:0 0 6px rgba(0,255,0,0.15)}
.terminal-screen .t-line.input{color:var(--q-amber);text-shadow:0 0 6px rgba(255,170,0,0.15)}
@keyframes tFadeIn{to{opacity:1}}
.terminal-input-wrap{display:flex;align-items:center;gap:8px;margin-top:10px;border:1px solid rgba(0,170,255,0.08);border-radius:4px;padding:4px 8px;background:rgba(0,0,0,0.3)}
.terminal-input-wrap .prompt-sym{color:var(--q-cyan);text-shadow:var(--glow-cyan);font-size:0.75em}
.terminal-input-wrap input{flex:1;background:transparent;border:none;outline:none;color:var(--q-amber);font-family:var(--font);font-size:0.75em;letter-spacing:1px;caret-color:var(--q-cyan)}
.terminal-input-wrap input::placeholder{color:rgba(176,184,208,0.15);letter-spacing:2px}
.terminal-input-wrap .send-btn{background:rgba(0,170,255,0.05);border:1px solid rgba(0,170,255,0.12);color:var(--q-cyan);font-family:var(--font);font-size:0.55em;letter-spacing:2px;padding:4px 10px;border-radius:3px;cursor:pointer;text-transform:uppercase;transition:all 0.25s}
.terminal-input-wrap .send-btn:hover{border-color:var(--q-cyan);box-shadow:0 0 10px rgba(0,170,255,0.15)}
.quickcmds{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.quickcmd{font-family:var(--font);font-size:0.55em;letter-spacing:1px;padding:3px 10px;border:1px solid rgba(0,170,255,0.08);border-radius:3px;background:rgba(0,170,255,0.02);color:rgba(176,184,208,0.4);cursor:pointer;transition:all 0.2s;text-transform:uppercase}
.quickcmd:hover{border-color:rgba(0,170,255,0.3);color:var(--q-cyan)}
.status-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.stat-block{border:1px solid rgba(0,170,255,0.04);border-radius:5px;padding:8px;background:rgba(0,0,0,0.15)}
.stat-block .sb-label{font-size:0.5em;letter-spacing:2px;color:rgba(176,184,208,0.3);text-transform:uppercase}
.stat-block .sb-value{font-size:1.1em;margin-top:2px;color:var(--q-cyan);text-shadow:0 0 8px rgba(0,170,255,0.15)}
.stat-block .sb-value.warn{color:var(--q-amber);text-shadow:0 0 8px rgba(255,170,0,0.15)}
.stat-block .sb-value.crit{color:var(--q-magenta);text-shadow:0 0 8px rgba(255,0,255,0.15)}
.stat-block .sb-bar{height:4px;margin-top:6px;border-radius:2px;background:rgba(0,170,255,0.06);overflow:hidden}
.stat-block .sb-bar-fill{height:100%;border-radius:2px;transition:width 0.6s,background 0.4s}
.output-line{margin-top:4px;padding:2px 0;font-size:0.6em;letter-spacing:1px;color:rgba(176,184,208,0.3);border-bottom:1px solid rgba(0,170,255,0.02)}
.q-footer{display:flex;justify-content:space-between;margin-top:12px;padding:8px 14px;border:1px solid rgba(0,170,255,0.04);border-radius:5px;background:rgba(0,0,0,0.2);flex-wrap:wrap;gap:6px;font-size:0.6em;letter-spacing:1px;color:rgba(176,184,208,0.3)}
@media(max-width:720px){.q-grid{grid-template-columns:1fr}}
@media(max-width:480px){
body{padding:8px}
.q-pane{padding:12px}
.terminal-screen{min-height:180px;max-height:240px;font-size:0.65em}
.status-grid{grid-template-columns:1fr}
.q-header h1{font-size:1em}
}
</style>
</head>
<body>
<div class="grid-overlay"></div>
<div class="q-wrap">
<div class="q-header">
<h1>QUANTUM <i>TERM</i></h1>
<div class="prompt">type help for commands</div>
</div>
<div class="q-grid">
<div class="q-pane">
<h2>Terminal</h2>
<div class="terminal-screen" id="terminalScreen">
<div class="t-line system">[QUANTUM TERMINAL v3.1]</div>
<div class="t-line system">[system ready | quantum link established]</div>
<div class="t-line output" style="animation-delay:0.05s">> type a command or click a quick command below</div>
</div>
<div class="terminal-input-wrap">
<span class="prompt-sym">></span>
<input type="text" id="termInput" placeholder="enter command..." autofocus>
<button class="send-btn" id="sendBtn">EXEC</button>
</div>
<div class="quickcmds">
<button class="quickcmd" data-cmd="status">STATUS</button>
<button class="quickcmd" data-cmd="scan">SCAN</button>
<button class="quickcmd" data-cmd="nodes">NODES</button>
<button class="quickcmd" data-cmd="clear">CLEAR</button>
<button class="quickcmd" data-cmd="help">HELP</button>
</div>
</div>
<div class="q-pane">
<h2>Quantum State</h2>
<div class="status-grid">
<div class="stat-block">
<div class="sb-label">Signal</div>
<div class="sb-value" id="sigVal">94.2%</div>
<div class="sb-bar"><div class="sb-bar-fill" id="sigBar" style="width:94.2%;background:var(--q-cyan)"></div></div>
</div>
<div class="stat-block">
<div class="sb-label">Entropy</div>
<div class="sb-value warn" id="entVal">0.67</div>
<div class="sb-bar"><div class="sb-bar-fill" id="entBar" style="width:67%;background:var(--q-amber)"></div></div>
</div>
<div class="stat-block">
<div class="sb-label">Coherence</div>
<div class="sb-value" id="cohVal">99.1%</div>
<div class="sb-bar"><div class="sb-bar-fill" id="cohBar" style="width:99.1%;background:var(--q-cyan)"></div></div>
</div>
<div class="stat-block">
<div class="sb-label">Latency</div>
<div class="sb-value crit" id="latVal">12ms</div>
<div class="sb-bar"><div class="sb-bar-fill" id="latBar" style="width:12%;background:var(--q-magenta)"></div></div>
</div>
</div>
<div style="margin-top:14px;border-top:1px solid rgba(0,170,255,0.04);padding-top:10px">
<h2 style="margin-bottom:6px">Event Stream</h2>
<div id="eventStream" style="font-size:0.6em;line-height:1.6;max-height:100px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(0,170,255,0.05) transparent">
<div class="output-line">[quantum sync established]</div>
<div class="output-line">[no anomalies detected]</div>
</div>
</div>
</div>
</div>
<div class="q-footer">
<span>[QUANTUM v3.1]</span>
<span id="qTime">--:--:--</span>
<span>press Enter to execute</span>
</div>
</div>
<script>
(function(){
var screen=document.getElementById('terminalScreen');
var input=document.getElementById('termInput');
var sendBtn=document.getElementById('sendBtn');
var cmdBtns=document.querySelectorAll('.quickcmd');
var sigVal=document.getElementById('sigVal');
var sigBar=document.getElementById('sigBar');
var entVal=document.getElementById('entVal');
var entBar=document.getElementById('entBar');
var cohVal=document.getElementById('cohVal');
var cohBar=document.getElementById('cohBar');
var latVal=document.getElementById('latVal');
var latBar=document.getElementById('latBar');
var eventStream=document.getElementById('eventStream');
var qTime=document.getElementById('qTime');
var cmdHistory=[];var histIdx=-1;
var responses={
help:'Available: status, scan, nodes, clear, ping, quantum, entropy, coherence, signal, time, about.',
status:'Status: ONLINE | Quantum link: STABLE | Nodes: 8 | Signal: 94.2% | Entropy: 0.67',
scan:'Scanning quantum field... [done] Nodes detected: 8 | Anomalies: 0 | Coherence: 99.1%',
nodes:'Active quantum nodes: AETHER, NEXUS, ORION, VECTOR, PRISM, ECHO, DRIFT, PHASE',
ping:'PONG | round-trip: 12ms',
quantum:'Quantum state: SUPERPOSITION | Decoherence rate: 0.03%/s | Stabilized: yes',
entropy:'Entropy: 0.67 | Low-entropy channels: 6 | High-entropy: 2 (ORION, DRIFT)',
coherence:'Coherence: 99.1% | Phase alignment: nominal | Drift: 0.02 deg/s',
signal:'Signal strength: 94.2% | SNR: 32.4 dB | Bandwidth: 2.4 Gbps',
time:'System time: ' + new Date().toLocaleTimeString(),
about:'Quantum Terminal v3.1 | Interface: holographic | Protocol: Q-NEURAL | Author: HoloForge'
};
function addLine(text,cls){
var div=document.createElement('div');div.className='t-line '+(cls||'output');
div.textContent='> '+text;screen.appendChild(div);screen.scrollTop=screen.scrollHeight;
}
function addSystem(text){
var div=document.createElement('div');div.className='t-line system';
div.textContent='[system] '+text;screen.appendChild(div);screen.scrollTop=screen.scrollHeight;
}
function executeCommand(cmd){
cmd=cmd.trim().toLowerCase();
if(!cmd){addSystem('enter a command');return;}
cmdHistory.push(cmd);histIdx=cmdHistory.length;
addLine(cmd,'input');
if(cmd==='clear'){screen.innerHTML='';addSystem('terminal cleared');return;}
if(cmd==='help'){
var keys=Object.keys(responses);
var msg='Available commands: '+keys.join(', ');
addLine(msg,'output');
return;
}
var found=responses[cmd];
if(found){addLine(found,'output');}
else{addLine('unknown command: "'+cmd+'". type "help" for available commands.','error');}
updateQuantumState();
}
function updateQuantumState(){
var sig=90+Math.random()*8;
sigVal.textContent=sig.toFixed(1)+'%';
sigBar.style.width=sig+'%';
sigBar.style.background=sig>80?'var(--q-cyan)':sig>60?'var(--q-amber)':'var(--q-magenta)';
sigVal.className='sb-value'+(sig<60?' crit':sig<80?' warn':'');
var ent=(0.4+Math.random()*0.5).toFixed(2);
entVal.textContent=ent;
entBar.style.width=(parseFloat(ent)*100)+'%';
entVal.className='sb-value'+(parseFloat(ent)>0.7?' warn':'');
var coh=97+Math.random()*2.9;
cohVal.textContent=coh.toFixed(1)+'%';
cohBar.style.width=coh+'%';
cohVal.className='sb-value'+(coh<98?' crit':'');
var lat=8+Math.random()*10;
latVal.textContent=Math.round(lat)+'ms';
latBar.style.width=Math.min(lat*2,100)+'%';
latVal.className='sb-value'+(lat>18?' crit':lat>12?' warn':'');
var evt=document.createElement('div');evt.className='output-line';
var events=['quantum pulse received','coherence check passed','node heartbeat OK','signal fluctuation normalized','entropy threshold stable','phase correction applied'];
evt.textContent='['+events[Math.floor(Math.random()*events.length)]+']';
eventStream.insertBefore(evt,eventStream.firstChild);
if(eventStream.children>8)eventStream.removeChild(eventStream.lastChild);
}
input.addEventListener('keydown',function(e){
if(e.key==='Enter'){executeCommand(input.value);input.value='';}
else if(e.key==='ArrowUp'){if(cmdHistory.length){histIdx=Math.max(0,histIdx-1);input.value=cmdHistory[histIdx]||'';setTimeout(function(){input.setSelectionRange(input.value.length,input.value.length);},0);}}
else if(e.key==='ArrowDown'){if(histIdx<cmdHistory.length-1){histIdx++;input.value=cmdHistory[histIdx];setTimeout(function(){input.setSelectionRange(input.value.length,input.value.length);},0);}else{histIdx=cmdHistory.length;input.value='';}}
else if(e.key==='Escape'){input.blur();}
});
sendBtn.addEventListener('click',function(){executeCommand(input.value);input.value='';input.focus();});
cmdBtns.forEach(function(btn){btn.addEventListener('click',function(){executeCommand(btn.dataset.cmd);input.focus();});});
document.addEventListener('keydown',function(e){
if(e.key==='/'&&document.activeElement!==input){e.preventDefault();input.focus();}
});
setInterval(function(){var now=new Date();qTime.textContent=now.toLocaleTimeString();},1000);
setInterval(function(){updateQuantumState();},5000);
input.focus();
})();
</script>
</body>
</html>
```
---
Summary Table
| Mockup | Theme | Interactive Elements | Responsive | Key Differentiator |
|---|---|---|---|---|
| 1. HoloCore System | Holographic dashboard with radial gauge | Click-driven metric toggle (4 states), button toggles (auto-balance, diagnostic, overclock), live uptime counter, real-time activity feed | @media 768px, 480px — grid collapses to single column, font/radial scale | Radially animated SVG ring + clickable metric card grid + particle overlay |
| 2. Neural Flux Analyzer | Node topology visualization | Canvas click-to-select nodes, keyboard shortcuts (N/R/1-3), 3 layout algorithms (force/radial/grid), add-node button, node list click-to-inspect | @media 820px, 480px + container query (600px) — 2col→1col, node list expands | Procedural canvas graph with force simulation, direct keyboard binding, multiple layout engines |
| 3. Quantum Terminal | Input-driven holographic terminal | Keyboard-driven command execution (Enter, arrow history, / focus), clickable quick-command buttons, real-time quantum state bars, live event stream, / key to focus | @media 720px, 480px — grid→1col, term shrinks, status grid→1col | Fully interactive terminal REPL with 10+ commands, animated state bars, keyboard-first UX |