Mockup 1: holographic-main-dashboard.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Holo Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a12;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 20% 50%,rgba(0,180,255,.08),transparent 60%),radial-gradient(ellipse at 80% 30%,rgba(120,0,255,.06),transparent 50%);pointer-events:none;z-index:0}
.particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden}
.particle{position:absolute;width:2px;height:2px;background:#00d4ff;border-radius:50%;box-shadow:0 0 6px #00d4ff,0 0 12px #0055ff44;animation:float linear infinite}
@keyframes float{0%{transform:translateY(100vh) scale(0);opacity:0}10%{opacity:1}90%{opacity:.6}100%{transform:translateY(-10vh) scale(1);opacity:0}}
.dashboard{position:relative;z-index:1;padding:20px 30px;max-width:1440px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding:16px 0 24px;border-bottom:1px solid rgba(0,180,255,.15);margin-bottom:28px}
h1{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:700;background:linear-gradient(90deg,#00d4ff,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;letter-spacing:3px;position:relative}
h1::after{content:'_';-webkit-text-fill-color:#00d4ff;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}
.header-stats{display:flex;gap:24px}
.header-stat{text-align:right}
.header-stat .label{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:#00d4ff88}
.header-stat .value{font-family:'Orbitron',sans-serif;font-size:18px;color:#00d4ff;text-shadow:0 0 10px #00d4ff66}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.card{background:linear-gradient(135deg,rgba(20,30,60,.7),rgba(10,15,35,.7));border:1px solid rgba(0,180,255,.15);border-radius:12px;padding:18px;backdrop-filter:blur(10px);position:relative;overflow:hidden;transition:all .3s}
.card:hover{border-color:#00d4ff55;box-shadow:0 0 30px rgba(0,180,255,.1),inset 0 0 30px rgba(0,180,255,.03);transform:translateY(-2px)}
.card::before{content:'';position:absolute;top:0;left:-100%;width:200%;height:2px;background:linear-gradient(90deg,transparent,#00d4ff88,transparent);animation:scan 4s linear infinite}
@keyframes scan{0%{left:-100%}100%{left:100%}}
.card-icon{font-size:28px;margin-bottom:10px;opacity:.8}
.card-label{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:#00d4ff88;margin-bottom:4px}
.card-value{font-family:'Orbitron',sans-serif;font-size:28px;font-weight:700;color:#fff;text-shadow:0 0 20px #00d4ff44}
.card-trend{font-size:13px;margin-top:4px;color:#22c55e;display:flex;align-items:center;gap:4px}
.panels{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:24px}
.panel{background:linear-gradient(135deg,rgba(20,30,60,.7),rgba(10,15,35,.7));border:1px solid rgba(0,180,255,.15);border-radius:12px;padding:20px;backdrop-filter:blur(10px);position:relative}
.panel-title{font-family:'Orbitron',sans-serif;font-size:13px;letter-spacing:2px;color:#00d4ff88;margin-bottom:16px;text-transform:uppercase}
.chart{height:200px;display:flex;align-items:flex-end;gap:8px;padding-top:10px}
.bar{flex:1;background:linear-gradient(to top,#00d4ff33,#00d4ff);border-radius:4px 4px 0 0;position:relative;transition:height .5s;min-height:4px;box-shadow:0 0 15px #00d4ff33}
.bar::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:#00d4ff;filter:blur(3px)}
.activity-list{display:flex;flex-direction:column;gap:10px}
.activity{display:flex;align-items:center;gap:12px;padding:8px 12px;background:rgba(0,180,255,.04);border-radius:8px;border-left:2px solid #00d4ff55}
.activity-dot{width:6px;height:6px;border-radius:50%;background:#00d4ff;box-shadow:0 0 8px #00d4ff}
.activity-text{flex:1;font-size:14px}
.activity-time{font-size:11px;color:#00d4ff66;font-family:'Orbitron',sans-serif}
.bottom-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.mini-panel{background:linear-gradient(135deg,rgba(20,30,60,.7),rgba(10,15,35,.7));border:1px solid rgba(0,180,255,.1);border-radius:12px;padding:16px;backdrop-filter:blur(10px);position:relative}
.mini-panel .panel-title{font-size:11px;margin-bottom:10px}
.data-row{display:flex;justify-content:space-between;padding:4px 0;font-size:13px;border-bottom:1px solid rgba(0,180,255,.05)}
.data-row:last-child{border-bottom:none}
.data-row .val{font-family:'Orbitron',sans-serif;color:#fff;font-size:12px}
.progress-track{height:4px;background:rgba(0,180,255,.1);border-radius:2px;margin-top:8px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#00d4ff,#a855f7);border-radius:2px;width:0%;box-shadow:0 0 10px #00d4ff44;animation:fillBar 1.5s ease-out forwards}
@keyframes fillBar{to{width:var(--w)}}
.glow-ring{width:60px;height:60px;border-radius:50%;border:2px solid #00d4ff44;position:relative;margin:0 auto 8px;display:flex;align-items:center;justify-content:center}
.glow-ring::before{content:'';position:absolute;inset:-4px;border-radius:50%;border:1px solid #00d4ff22;animation:spin 4s linear infinite;border-top-color:#00d4ff}
@keyframes spin{to{transform:rotate(360deg)}}
.glow-ring .inner{font-family:'Orbitron',sans-serif;font-size:14px;color:#00d4ff;text-shadow:0 0 15px #00d4ff}
@media(max-width:1024px){.grid{grid-template-columns:repeat(2,1fr)}.panels{grid-template-columns:1fr}.bottom-grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.grid{grid-template-columns:1fr}.bottom-grid{grid-template-columns:1fr}.dashboard{padding:12px 16px}header{flex-direction:column;gap:12px}.header-stats{gap:16px}}
</style>
</head>
<body>
<div class=particles id=particles></div>
<div class=dashboard>
<header>
<h1>HOLO_DASH</h1>
<div class=header-stats>
<div class=header-stat><div class=label>SYSTEM</div><div class=value>ONLINE</div></div>
<div class=header-stat><div class=label>UPTIME</div><div class=value>47:12:08</div></div>
<div class=header-stat><div class=label>ALERTS</div><div class=value>0</div></div>
</div>
</header>
<div class=grid>
<div class=card><div class=card-icon>🌐</div><div class=card-label>Network Traffic</div><div class=card-value>2.4Tb</div><div class=card-trend>↑ 12.3%</div></div>
<div class=card><div class=card-icon>⚡</div><div class=card-label>Processing</div><div class=card-value>847K</div><div class=card-trend style=color:#22c55e>↑ 8.1%</div></div>
<div class=card><div class=card-icon>👥</div><div class=card-label>Active Users</div><div class=card-value>12,847</div><div class=card-trend style=color:#22c55e>↑ 5.2%</div></div>
<div class=card><div class=card-icon>📡</div><div class=card-label>Latency</div><div class=card-value>24ms</div><div class=card-trend style=color:#f97316>→ 0.3%</div></div>
</div>
<div class=panels>
<div class=panel><div class=panel-title>REALTIME THROUGHPUT</div><div class=chart id=chart></div></div>
<div class=panel><div class=panel-title>RECENT ACTIVITY</div><div class=activity-list><div class=activity><div class=activity-dot></div><div class=activity-text>Node cluster sync complete</div><div class=activity-time>12s ago</div></div><div class=activity><div class=activity-dot></div><div class=activity-text>Data pipeline flush @ 2.4GB/s</div><div class=activity-time>47s ago</div></div><div class=activity><div class=activity-dot></div><div class=activity-text>Authentication spike detected</div><div class=activity-time>2m ago</div></div><div class=activity><div class=activity-dot></div><div class=activity-text>Backup replication verified</div><div class=activity-time>5m ago</div></div><div class=activity><div class=activity-dot></div><div class=activity-text>CDN edge sync completed</div><div class=activity-time>11m ago</div></div></div></div>
</div>
<div class=bottom-grid>
<div class=mini-panel><div class=panel-title>SYSTEM RESOURCES</div><div class=data-row><span>CPU</span><span class=val>34%</span></div><div class=progress-track><div class=progress-fill style=--w:34%></div></div><div class=data-row><span>RAM</span><span class=val>62%</span></div><div class=progress-track><div class=progress-fill style=--w:62%></div></div><div class=data-row><span>STORAGE</span><span class=val>78%</span></div><div class=progress-track><div class=progress-fill style=--w:78%></div></div></div>
<div class=mini-panel><div class=panel-title>NODE STATUS</div><div class=data-row><span>Primary</span><span class=val style=color:#22c55e>● Active</span></div><div class=data-row><span>Secondary</span><span class=val style=color:#22c55e>● Active</span></div><div class=data-row><span>Replica</span><span class=val style=color:#f97316>● Syncing</span></div><div class=data-row><span>Backup</span><span class=val style=color:#22c55e>● Standby</span></div></div>
<div class=mini-panel style=display:flex;flex-direction:column;align-items:center;justify-content:center><div class=glow-ring><div class=inner>98%</div></div><div style=font-size:11px;color:#00d4ff88;letter-spacing:2px;text-transform:uppercase>System Health</div><div style=font-size:13px;color:#22c55e;margin-top:4px>All nominal</div></div>
</div>
</div>
<script>
const pContainer=document.getElementById('particles');
for(let i=0;i<40;i++){const p=document.createElement('div');p.className='particle';p.style.left=Math.random()*100+'%';p.style.animationDuration=(8+Math.random()*16)+'s';p.style.animationDelay=Math.random()*20+'s';p.style.width=(1+Math.random()*2)+'px';p.style.height=p.style.width;pContainer.appendChild(p)}
const chart=document.getElementById('chart');
const heights=[20,35,28,45,38,52,42,60,50,68,58,75,62,85];
heights.forEach(h=>{const bar=document.createElement('div');bar.className='bar';bar.style.height=h+'%';setTimeout(()=>{bar.style.height=(h+Math.random()*10-5)+'%'},500+Math.random()*1000);chart.appendChild(bar)})
</script>
</body>
</html>
Mockup 2: analytics-hub.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Analytics Hub</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08081a;color:#d0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 70% 20%,rgba(140,0,255,.08),transparent 60%),radial-gradient(ellipse at 20% 80%,rgba(0,200,255,.06),transparent 50%);pointer-events:none;z-index:0}
.grid-lines{position:fixed;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(rgba(0,180,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,180,255,.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:20px 30px;max-width:1440px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding:16px 0 24px;border-bottom:1px solid rgba(140,0,255,.2);margin-bottom:28px}
h1{font-family:'Orbitron',sans-serif;font-size:20px;font-weight:700;background:linear-gradient(90deg,#a855f7,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px}
.header-actions{display:flex;gap:12px}
.holo-btn{background:rgba(140,0,255,.1);border:1px solid rgba(140,0,255,.3);color:#a855f7;padding:6px 16px;border-radius:6px;font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:1px;cursor:pointer;transition:all .3s}
.holo-btn:hover{background:rgba(140,0,255,.2);box-shadow:0 0 20px rgba(140,0,255,.2)}
.period{color:#d0d0ff88;font-size:13px;font-family:'Orbitron',sans-serif;letter-spacing:1px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}
.kpi{background:linear-gradient(135deg,rgba(20,20,60,.6),rgba(40,10,80,.6));border:1px solid rgba(140,0,255,.15);border-radius:10px;padding:16px;backdrop-filter:blur(8px);position:relative;transition:all .3s}
.kpi:hover{border-color:#a855f7;box-shadow:0 0 25px rgba(140,0,255,.1)}
.kpi::after{content:'';position:absolute;bottom:0;right:0;width:40px;height:40px;background:radial-gradient(circle,rgba(140,0,255,.1),transparent);pointer-events:none}
.kpi-label{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#a855f788;margin-bottom:2px}
.kpi-value{font-family:'Orbitron',sans-serif;font-size:26px;font-weight:700;color:#e0d0ff;text-shadow:0 0 15px rgba(168,85,247,.3)}
.kpi-change{font-size:12px;margin-top:2px;display:flex;align-items:center;gap:4px}
.chart-grid{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:24px}
.chart-panel{background:linear-gradient(135deg,rgba(20,20,60,.6),rgba(40,10,80,.6));border:1px solid rgba(140,0,255,.15);border-radius:12px;padding:20px;backdrop-filter:blur(8px)}
.chart-panel .title{font-family:'Orbitron',sans-serif;font-size:12px;letter-spacing:2px;color:#a855f788;margin-bottom:14px;display:flex;justify-content:space-between}
.line-chart{height:180px;position:relative;display:flex;align-items:flex-end;gap:0}
.line-group{flex:1;display:flex;flex-direction:column;align-items:center;position:relative;height:100%}
.line-bar{width:6px;background:linear-gradient(to top,#a855f7,#00d4ff);border-radius:3px 3px 0 0;position:absolute;bottom:0;transition:height .6s;box-shadow:0 0 10px #a855f744}
.line-bar:nth-child(2){width:4px;background:linear-gradient(to top,#f59e0b,#f97316);right:2px}
.line-dot{width:4px;height:4px;background:#a855f7;border-radius:50%;position:absolute;box-shadow:0 0 8px #a855f7;z-index:2}
.metrics-list{display:flex;flex-direction:column;gap:12px}
.metric-item{padding:10px 14px;background:rgba(140,0,255,.04);border-radius:8px;border-left:2px solid #a855f766}
.metric-item .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
.metric-item .name{font-size:13px;font-weight:600}
.metric-item .val{font-family:'Orbitron',sans-serif;font-size:14px;color:#e0d0ff}
.metric-item .sub{font-size:11px;color:#a855f788;display:flex;gap:12px}
.triple{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.mini-card{background:linear-gradient(135deg,rgba(20,20,60,.6),rgba(40,10,80,.6));border:1px solid rgba(140,0,255,.1);border-radius:10px;padding:16px;backdrop-filter:blur(8px)}
.mini-card .mc-title{font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:2px;color:#a855f788;margin-bottom:10px}
.pie-wrap{display:flex;align-items:center;justify-content:center;gap:16px}
.pie{width:70px;height:70px;border-radius:50%;background:conic-gradient(#a855f7 0% 45%,#00d4ff 45% 72%,#f97316 72% 88%,#22c55e 88% 100%);position:relative}
.pie::after{content:'';position:absolute;inset:12px;border-radius:50%;background:#0e0e24}
.pie-legend{display:flex;flex-direction:column;gap:4px;font-size:11px}
.pie-legend span{display:flex;align-items:center;gap:6px}
.pie-legend .dot{width:6px;height:6px;border-radius:50%}
.data-table{width:100%;font-size:12px;border-collapse:collapse}
.data-table th{font-family:'Orbitron',sans-serif;font-size:9px;letter-spacing:2px;color:#a855f788;text-align:left;padding:6px 4px;border-bottom:1px solid rgba(140,0,255,.1)}
.data-table td{padding:6px 4px;border-bottom:1px solid rgba(140,0,255,.05);color:#d0d0ff}
.data-table tr:hover td{background:rgba(140,0,255,.05)}
.status-on{color:#22c55e}
.status-warn{color:#f97316}
@media(max-width:1024px){.kpi-grid{grid-template-columns:repeat(2,1fr)}.chart-grid{grid-template-columns:1fr}.triple{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.kpi-grid{grid-template-columns:1fr}.triple{grid-template-columns:1fr}.dash{padding:12px 16px}header{flex-direction:column;gap:12px}}
</style>
</head>
<body>
<div class=grid-lines></div>
<div class=dash>
<header>
<h1>ANALYTICS_HUB</h1>
<div class=header-actions><button class=holo-btn>REALTIME</button><button class=holo-btn>EXPORT</button><span class=period>Q2 2026</span></div>
</header>
<div class=kpi-grid>
<div class=kpi><div class=kpi-label>Total Revenue</div><div class=kpi-value>$2.84M</div><div class=kpi-change style=color:#22c55e>↑ 18.3% vs last Q</div></div>
<div class=kpi><div class=kpi-label>Conversion Rate</div><div class=kpi-value>4.82%</div><div class=kpi-change style=color:#22c55e>↑ 0.7pp</div></div>
<div class=kpi><div class=kpi-label>Avg Order Value</div><div class=kpi-value>$247</div><div class=kpi-change style=color:#f97316>↑ 3.2%</div></div>
<div class=kpi><div class=kpi-label>Churn Rate</div><div class=kpi-value>1.24%</div><div class=kpi-change style=color:#22c55e>↓ 0.4pp</div></div>
</div>
<div class=chart-grid>
<div class=chart-panel><div class=title><span>REVENUE TREND</span><span style=color:#a855f744>← 6mo →</span></div><div class=line-chart id=revenueChart></div></div>
<div class=chart-panel><div class=title><span>TOP METRICS</span></div><div class=metrics-list><div class=metric-item><div class=top><span class=name>Page Views</span><span class=val>847.3K</span></div><div class=sub><span>↑ 12.4%</span><span>bounce: 32.1%</span></div></div><div class=metric-item><div class=top><span class=name>Sessions</span><span class=val>312.8K</span></div><div class=sub><span>↑ 8.7%</span><span>avg dur: 4:12</span></div></div><div class=metric-item><div class=top><span class=name>New Users</span><span class=val>48.2K</span></div><div class=sub><span>↑ 22.1%</span><span>retention: 68%</span></div></div><div class=metric-item><div class=top><span class=name>API Calls</span><span class=val>1.2M</span></div><div class=sub><span>↑ 5.3%</span><span>p99: 124ms</span></div></div></div></div>
</div>
<div class=triple>
<div class=mini-card><div class=mc-title>SEGMENT DISTRIBUTION</div><div class=pie-wrap><div class=pie></div><div class=pie-legend><span><span class=dot style=background:#a855f7></span>Enterprise 45%</span><span><span class=dot style=background:#00d4ff></span>Mid-Market 27%</span><span><span class=dot style=background:#f97316></span>SMB 16%</span><span><span class=dot style=background:#22c55e></span>Startup 12%</span></div></div></div>
<div class=mini-card><div class=mc-title>GEO PERFORMANCE</div><table class=data-table><tr><th>Region</th><th>Revenue</th><th>Growth</th></tr><tr><td>North America</td><td>$1.24M</td><td class=status-on>↑ 14.2%</td></tr><tr><td>Europe</td><td>$892K</td><td class=status-on>↑ 9.8%</td></tr><tr><td>APAC</td><td>$512K</td><td class=status-on>↑ 27.4%</td></tr><tr><td>LATAM</td><td>$186K</td><td class=status-warn>↑ 4.1%</td></tr></table></div>
<div class=mini-card><div class=mc-title>TOP PAGES</div><table class=data-table><tr><th>Page</th><th>Visits</th><th>Conv</th></tr><tr><td>/dashboard</td><td>142K</td><td class=status-on>5.2%</td></tr><tr><td>/pricing</td><td>98K</td><td class=status-on>8.7%</td></tr><tr><td>/features</td><td>67K</td><td class=status-warn>3.1%</td></tr><tr><td>/docs</td><td>41K</td><td class=status-on>1.8%</td></tr></table></div>
</div>
</div>
<script>
const rc=document.getElementById('revenueChart');
const vals=[30,42,38,55,48,65,58,72,62,80,68,88];
vals.forEach((v,i)=>{const g=document.createElement('div');g.className='line-group';const b=document.createElement('div');b.className='line-bar';b.style.height=v+'%';const d=document.createElement('div');d.className='line-dot';d.style.bottom=v+'%';d.style.left='50%';d.style.transform='translateX(-50%)';g.appendChild(b);g.appendChild(d);rc.appendChild(g)})
</script>
</body>
</html>
Mockup 3: system-monitor.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>System Monitor</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050510;color:#c0e0ff;font-family:'Rajdhani',sans-serif;min-height:100vh;overflow:hidden}
.scanlines{position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,180,255,.008) 2px,rgba(0,180,255,.008) 4px);pointer-events:none;z-index:0}
.vignette{position:fixed;top:0;left:0;width:100%;height:100%;box-shadow:inset 0 0 150px rgba(0,0,0,.6);pointer-events:none;z-index:1}
.dash{position:relative;z-index:2;padding:16px 24px;height:100vh;display:flex;flex-direction:column}
.top-bar{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid rgba(0,200,255,.1);margin-bottom:16px}
h1{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:700;color:#00c8ff;text-shadow:0 0 20px #00c8ff44;letter-spacing:4px;display:flex;align-items:center;gap:10px}
h1 .pulse{width:8px;height:8px;background:#22c55e;border-radius:50%;box-shadow:0 0 10px #22c55e;animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.3)}}
.status-row{display:flex;gap:20px;font-size:12px;font-family:'Orbitron',sans-serif;letter-spacing:1px;color:#00c8ff88}
.main-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:12px;flex:1;min-height:0}
.main-grid>div{background:linear-gradient(135deg,rgba(0,20,40,.6),rgba(0,5,20,.6));border:1px solid rgba(0,200,255,.12);border-radius:8px;padding:14px;backdrop-filter:blur(6px);display:flex;flex-direction:column;overflow:hidden}
.section-title{font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:2px;color:#00c8ff66;margin-bottom:10px;flex-shrink:0}
.server-list{flex:1;display:flex;flex-direction:column;gap:8px;overflow-y:auto}
.server{display:flex;align-items:center;gap:10px;padding:8px 10px;background:rgba(0,200,255,.03);border-radius:6px;border-left:3px solid}
.server.ok{border-left-color:#22c55e}
.server.warn{border-left-color:#f97316}
.server.crit{border-left-color:#ef4444}
.server .s-name{flex:1;font-size:13px;font-weight:600}
.server .s-load{font-family:'Orbitron',sans-serif;font-size:11px;width:40px;text-align:right}
.server .s-bar{width:60px;height:4px;background:rgba(0,200,255,.1);border-radius:2px;overflow:hidden}
.server .s-bar .fill{height:100%;border-radius:2px;transition:width .5s}
.live-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;flex:1}
.live-block{background:rgba(0,200,255,.03);border-radius:6px;padding:10px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.live-block .lb-val{font-family:'Orbitron',sans-serif;font-size:22px;color:#00c8ff;text-shadow:0 0 15px #00c8ff44}
.live-block .lb-label{font-size:9px;letter-spacing:1px;color:#00c8ff66;text-transform:uppercase;margin-top:2px}
.live-block .lb-mini{font-size:10px;color:#00c8ff88;margin-top:2px}
.alert-feed{flex:1;display:flex;flex-direction:column;gap:6px;overflow-y:auto}
.alert{display:flex;align-items:flex-start;gap:8px;padding:6px 8px;background:rgba(0,200,255,.03);border-radius:4px;font-size:12px;border-left:2px solid}
.alert.info{border-left-color:#00c8ff}
.alert.warn{border-left-color:#f97316}
.alert.crit{border-left-color:#ef4444}
.alert .a-time{font-family:'Orbitron',sans-serif;font-size:9px;color:#00c8ff66;white-space:nowrap;width:50px;flex-shrink:0}
.alert .a-msg{flex:1}
.bottom-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;flex-shrink:0}
.bottom-row>div{background:linear-gradient(135deg,rgba(0,20,40,.6),rgba(0,5,20,.6));border:1px solid rgba(0,200,255,.08);border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:16px}
.metric-group{display:flex;gap:24px}
.metric-group .mg-item{display:flex;flex-direction:column}
.metric-group .mg-val{font-family:'Orbitron',sans-serif;font-size:16px;color:#00c8ff}
.metric-group .mg-label{font-size:9px;letter-spacing:1px;color:#00c8ff66;text-transform:uppercase}
@media(max-width:1024px){.main-grid{grid-template-columns:1fr 1fr}.bottom-row{grid-template-columns:1fr}}
@media(max-width:640px){.main-grid{grid-template-columns:1fr}.top-bar{flex-direction:column;gap:8px}.dash{padding:10px;height:auto;min-height:100vh}.status-row{flex-wrap:wrap;gap:8px}}
</style>
</head>
<body>
<div class=scanlines></div>
<div class=vignette></div>
<div class=dash>
<div class=top-bar>
<h1><span class=pulse></span>SYS_MONITOR</h1>
<div class=status-row><span>47 NODES ONLINE</span><span>0 CRITICAL</span><span>UPTIME 312d 14h</span><span>LOAD 42%</span></div>
</div>
<div class=main-grid>
<div><div class=section-title>NODE CLUSTER</div><div class=server-list><div class="server ok"><span class=s-name>Alpha-Primary</span><div class=s-bar><div class=fill style=width:34%;background:linear-gradient(90deg,#22c55e,#4ade80)></div></div><span class=s-load style=color:#22c55e>34%</span></div><div class="server ok"><span class=s-name>Beta-Secondary</span><div class=s-bar><div class=fill style=width:28%;background:linear-gradient(90deg,#22c55e,#4ade80)></div></div><span class=s-load style=color:#22c55e>28%</span></div><div class="server ok"><span class=s-name>Gamma-Replica</span><div class=s-bar><div class=fill style=width:52%;background:linear-gradient(90deg,#22c55e,#facc15)></div></div><span class=s-load style=color:#facc15>52%</span></div><div class="server warn"><span class=s-name>Delta-Cache</span><div class=s-bar><div class=fill style=width:81%;background:linear-gradient(90deg,#facc15,#f97316)></div></div><span class=s-load style=color:#f97316>81%</span></div><div class="server ok"><span class=s-name>Epsilon-Backup</span><div class=s-bar><div class=fill style=width:12%;background:linear-gradient(90deg,#22c55e,#4ade80)></div></div><span class=s-load style=color:#22c55e>12%</span></div><div class="server ok"><span class=s-name>Zeta-Edge</span><div class=s-bar><div class=fill style=width:45%;background:linear-gradient(90deg,#22c55e,#facc15)></div></div><span class=s-load style=color:#facc15>45%</span></div></div></div>
<div><div class=section-title>LIVE METRICS</div><div class=live-grid><div class=live-block><div class=lb-val>847</div><div class=lb-label>Req/s</div><div class=lb-mini>peak: 1,240</div></div><div class=live-block><div class=lb-val>24ms</div><div class=lb-label>Latency</div><div class=lb-mini>p99: 68ms</div></div><div class=live-block><div class=lb-val>2.4TB</div><div class=lb-label>Throughput</div><div class=lb-mini>↑ 18%</div></div><div class=live-block><div class=lb-val>99.97%</div><div class=lb-label>Uptime</div><div class=lb-mini>30d avg</div></div></div></div>
<div><div class=section-title>ALERT FEED</div><div class=alert-feed><div class="alert crit"><span class=a-time>12:47</span><span class=a-msg>Delta-Cache memory threshold exceeded (81%)</span></div><div class="alert warn"><span class=a-time>12:32</span><span class=a-msg>Gamma-Replica replication lag at 347ms</span></div><div class="alert info"><span class=a-time>12:18</span><span class=a-msg>Auto-scale: +2 workers provisioned</span></div><div class="alert info"><span class=a-time>11:54</span><span class=a-msg>Backup cycle completed (4.2TB)</span></div><div class="alert warn"><span class=a-time>11:22</span><span class=a-msg>CDN edge node elevated error rate (2.1%)</span></div><div class="alert info"><span class=a-time>10:58</span><span class=a-msg>SSL cert renewal succeeded</span></div></div></div>
</div>
<div class=bottom-row>
<div><span style=font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:1px;color:#00c8ff66;flex-shrink:0>NETWORK</span><div class=metric-group><div class=mg-item><span class=mg-val>847 Mbps</span><span class=mg-label>Inbound</span></div><div class=mg-item><span class=mg-val>412 Mbps</span><span class=mg-label>Outbound</span></div><div class=mg-item><span class=mg-val>0.02%</span><span class=mg-label>Packet Loss</span></div></div></div>
<div style=display:flex;align-items:center;gap:12px><span style=font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:1px;color:#00c8ff66;flex-shrink:0>STORAGE</span><div style=display:flex;gap:16px;flex:1><div style=flex:1><div style=display:flex;justify-content:space-between;font-size:10px;color:#00c8ff88;margin-bottom:2px><span>/data</span><span>64%</span></div><div style=height:4px;background:rgba(0,200,255,.1);border-radius:2px;overflow:hidden><div style=height:100%;width:64%;background:linear-gradient(90deg,#22c55e,#facc15);border-radius:2px></div></div></div><div style=flex:1><div style=display:flex;justify-content:space-between;font-size:10px;color:#00c8ff88;margin-bottom:2px><span>/backup</span><span>41%</span></div><div style=height:4px;background:rgba(0,200,255,.1);border-radius:2px;overflow:hidden><div style=height:100%;width:41%;background:linear-gradient(90deg,#22c55e,#4ade80);border-radius:2px></div></div></div></div></div>
</div>
</div>
</body>
</html>
Mockup 4: data-grid-terminal.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Data Grid Terminal</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@400;600;700&family=Rajdhani:wght@400;600&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#b0ffb0;font-family:'JetBrains Mono',monospace;min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 50% 0%,rgba(0,255,100,.04),transparent 70%);pointer-events:none;z-index:0}
.terminal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 30px,rgba(0,255,100,.02) 30px,rgba(0,255,100,.02) 31px);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:16px 24px;max-width:1440px;margin:0 auto}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid rgba(0,255,100,.15);margin-bottom:20px}
h1{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:700;color:#00ff64;text-shadow:0 0 15px rgba(0,255,100,.3);letter-spacing:3px;display:flex;align-items:center;gap:8px}
h1::before{content:'>';color:#00ff6488;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}
.header-right{display:flex;gap:16px;font-size:11px;color:#00ff6488;align-items:center}
.header-right span{cursor:pointer;padding:4px 8px;border:1px solid transparent;transition:all .2s}
.header-right span:hover{border-color:#00ff6444;border-radius:4px;color:#00ff64}
.toolbar{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.tb-btn{background:rgba(0,255,100,.05);border:1px solid rgba(0,255,100,.15);color:#00ff6488;padding:4px 12px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:11px;cursor:pointer;transition:all .2s}
.tb-btn:hover{background:rgba(0,255,100,.1);border-color:#00ff6444;color:#00ff64}
.search-bar{display:flex;align-items:center;gap:8px;flex:1;max-width:400px;background:rgba(0,255,100,.03);border:1px solid rgba(0,255,100,.1);border-radius:4px;padding:4px 10px}
.search-bar input{background:transparent;border:none;color:#00ff64;font-family:'JetBrains Mono',monospace;font-size:11px;outline:none;width:100%}
.search-bar input::placeholder{color:#00ff6422}
.search-bar .icon{color:#00ff6444;font-size:12px}
.grid-controls{display:flex;gap:12px;align-items:center;margin-bottom:14px;font-size:11px;color:#00ff6488}
.grid-controls .active{color:#00ff64}
.table-wrap{background:linear-gradient(135deg,rgba(0,20,10,.6),rgba(0,10,5,.6));border:1px solid rgba(0,255,100,.1);border-radius:8px;overflow:auto;backdrop-filter:blur(4px)}
table{width:100%;border-collapse:collapse;font-size:12px;min-width:800px}
thead{background:rgba(0,255,100,.04);position:sticky;top:0}
th{font-family:'Orbitron',sans-serif;font-size:9px;letter-spacing:2px;color:#00ff6488;text-align:left;padding:10px 12px;border-bottom:1px solid rgba(0,255,100,.1);cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:#00ff64}
th .sort{font-size:7px;margin-left:4px;color:#00ff6444}
td{padding:8px 12px;border-bottom:1px solid rgba(0,255,100,.04);color:#a0e0b0;transition:background .15s}
tr:hover td{background:rgba(0,255,100,.04)}
tr.selected td{background:rgba(0,255,100,.08)}
.id-col{color:#00ff64;font-family:'Orbitron',sans-serif;font-size:10px}
.status-badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:10px;border:1px solid}
.status-badge.active{color:#22c55e;border-color:#22c55e55;background:rgba(34,197,94,.08)}
.status-badge.pending{color:#facc15;border-color:#facc1555;background:rgba(250,204,21,.08)}
.status-badge.error{color:#ef4444;border-color:#ef444455;background:rgba(239,68,68,.08)}
.status-badge.dormant{color:#64748b;border-color:#64748b55;background:rgba(100,116,139,.08)}
.progress-cell{display:flex;align-items:center;gap:8px}
.progress-cell .pbar{width:60px;height:4px;background:rgba(0,255,100,.1);border-radius:2px;overflow:hidden}
.progress-cell .pbar .fill{height:100%;background:linear-gradient(90deg,#00ff64,#22c55e);border-radius:2px}
.footer-stats{display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding:8px 12px;background:rgba(0,255,100,.02);border:1px solid rgba(0,255,100,.06);border-radius:6px;font-size:11px;color:#00ff6488}
.pagination{display:flex;gap:6px}
.pagination span{padding:2px 8px;border:1px solid rgba(0,255,100,.1);border-radius:3px;cursor:pointer;font-size:10px}
.pagination span:hover,.pagination span.active{border-color:#00ff6444;color:#00ff64;background:rgba(0,255,100,.05)}
@media(max-width:768px){.toolbar{flex-direction:column}.search-bar{max-width:100%}.dash{padding:10px 12px}header{flex-direction:column;gap:8px;align-items:flex-start}}
</style>
</head>
<body>
<div class=terminal-overlay></div>
<div class=dash>
<div class=header>
<h1>DATA_GRID</h1>
<div class=header-right><span>FILTER</span><span>COLUMNS</span><span>EXPORT</span><span style=color:#00ff64>● 2,847 records</span></div>
</div>
<div class=toolbar>
<div class=search-bar><span class=icon>⌕</span><input placeholder="Query records..." value="status:active"></div>
<button class=tb-btn>⟳ Refresh</button>
<button class=tb-btn>+ New Record</button>
<button class=tb-btn>🗑 Delete</button>
<button class=tb-btn>⚙ Batch</button>
</div>
<div class=grid-controls><span class=active>ALL</span><span>ACTIVE</span><span>PENDING</span><span>ERROR</span><span>DORMANT</span><span style=margin-left:auto>Rows: 25 ▾</span></div>
<div class=table-wrap>
<table>
<thead><tr><th>ID <span class=sort>▲</span></th><th>NAME <span class=sort>▽</span></th><th>STATUS</th><th>REGION</th><th>PROGRESS</th><th>REVENUE</th><th>LAST ACTIVE</th></tr></thead>
<tbody>
<tr><td class=id-col>#0427</td><td>NeoPrime Core</td><td><span class=status-badge active>Active</span></td><td>US-EAST</td><td class=progress-cell><div class=pbar><div class=fill style=width:100%></div></div><span>100%</span></td><td>$284,700</td><td style=color:#00ff6488>12s ago</td></tr>
<tr class=selected><td class=id-col>#0419</td><td>Quantum Sync</td><td><span class=status-badge pending>Pending</span></td><td>EU-WEST</td><td class=progress-cell><div class=pbar><div class=fill style=width:67%></div></div><span>67%</span></td><td>$142,300</td><td style=color:#00ff6488>3m ago</td></tr>
<tr><td class=id-col>#0408</td><td>Helios Pipeline</td><td><span class=status-badge active>Active</span></td><td>APAC</td><td class=progress-cell><div class=pbar><div class=fill style=width:92%></div></div><span>92%</span></td><td>$498,200</td><td style=color:#00ff6488>47s ago</td></tr>
<tr><td class=id-col>#0395</td><td>Nova Backup</td><td><span class=status-badge dormant>Dormant</span></td><td>US-WEST</td><td class=progress-cell><div class=pbar><div class=fill style=width:100%></div></div><span>100%</span></td><td>$12,400</td><td style=color:#00ff6488>2d ago</td></tr>
<tr><td class=id-col>#0388</td><td>Echo Cache Layer</td><td><span class=status-badge error>Error</span></td><td>EU-CENTRAL</td><td class=progress-cell><div class=pbar><div class=fill style=width:23%;background:linear-gradient(90deg,#ef4444,#f97316)></div></div><span>23%</span></td><td>$0</td><td style=color:#ef4444>FAILED</td></tr>
<tr><td class=id-col>#0372</td><td>Aurora Stream</td><td><span class=status-badge active>Active</span></td><td>US-EAST</td><td class=progress-cell><div class=pbar><div class=fill style=width:78%></div></div><span>78%</span></td><td>$67,800</td><td style=color:#00ff6488>8m ago</td></tr>
<tr><td class=id-col>#0361</td><td>Titan Replica</td><td><span class=status-badge pending>Pending</span></td><td>APAC</td><td class=progress-cell><div class=pbar><div class=fill style=width:44%></div></div><span>44%</span></td><td>$0</td><td style=color:#00ff6488>1h ago</td></tr>
</tbody>
</table>
</div>
<div class=footer-stats>
<span>Showing 1-7 of 2,847 <span style=color:#00ff64>●</span></span>
<div class=pagination><span class=active>1</span><span>2</span><span>3</span><span>4</span><span>...</span><span>114</span></div>
</div>
</div>
</body>
</html>
Mockup 5: map-geo-dashboard.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Geo Command</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#060618;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh;overflow:hidden}
.dash{position:relative;z-index:1;padding:16px 24px;height:100vh;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid rgba(0,180,255,.1);margin-bottom:12px;flex-shrink:0}
h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;background:linear-gradient(90deg,#00d4ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px}
.top-right{display:flex;gap:16px;font-size:11px;color:#00d4ff88;font-family:'Orbitron',sans-serif;letter-spacing:1px}
.map-area{flex:1;background:linear-gradient(135deg,rgba(10,10,40,.8),rgba(5,5,25,.8));border:1px solid rgba(0,180,255,.1);border-radius:12px;position:relative;overflow:hidden;backdrop-filter:blur(4px);min-height:300px}
.map-area::before{content:'';position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 30% 40%,rgba(0,180,255,.06),transparent 50%),radial-gradient(circle at 70% 60%,rgba(124,58,237,.04),transparent 50%);pointer-events:none;z-index:0}
.map-grid{position:absolute;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(rgba(0,180,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,180,255,.04) 1px,transparent 1px);background-size:60px 60px;z-index:1}
.map-pin{position:absolute;z-index:2;cursor:pointer;transition:all .3s}
.map-pin:hover{transform:scale(1.3);z-index:5}
.map-pin .pin{width:12px;height:12px;border-radius:50%;position:relative}
.map-pin .pin::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:24px;height:24px;border-radius:50%;animation:ping 2s ease-out infinite}
@keyframes ping{0%{transform:translate(-50%,-50%) scale(1);opacity:.4}100%{transform:translate(-50%,-50%) scale(2.5);opacity:0}}
.map-pin .pin.hot{background:#ef4444;box-shadow:0 0 20px #ef4444,0 0 40px rgba(239,68,68,.3)}
.map-pin .pin.hot::after{background:#ef4444}
.map-pin .pin.warm{background:#f97316;box-shadow:0 0 15px #f97316,0 0 30px rgba(249,115,22,.3)}
.map-pin .pin.warm::after{background:#f97316}
.map-pin .pin.cool{background:#22c55e;box-shadow:0 0 12px #22c55e,0 0 24px rgba(34,197,94,.3)}
.map-pin .pin.cool::after{background:#22c55e}
.map-pin .pin.info{background:#00d4ff;box-shadow:0 0 12px #00d4ff,0 0 24px rgba(0,212,255,.3)}
.map-pin .pin.info::after{background:#00d4ff}
.map-pin .label{position:absolute;top:-22px;left:50%;transform:translateX(-50%);font-size:9px;font-family:'Orbitron',sans-serif;color:#fff;text-shadow:0 0 8px rgba(0,0,0,.8);white-space:nowrap;background:rgba(0,0,0,.5);padding:1px 6px;border-radius:3px;border:1px solid rgba(255,255,255,.1)}
.map-label{position:absolute;z-index:3;font-family:'Orbitron',sans-serif;font-size:8px;color:#00d4ff44;letter-spacing:2px;text-transform:uppercase}
.bottom-panel{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px;flex-shrink:0}
.geo-card{background:linear-gradient(135deg,rgba(10,10,40,.6),rgba(5,5,25,.6));border:1px solid rgba(0,180,255,.08);border-radius:8px;padding:12px;backdrop-filter:blur(4px);display:flex;flex-direction:column}
.geo-card .gc-label{font-size:9px;letter-spacing:2px;color:#00d4ff66;text-transform:uppercase;font-family:'Orbitron',sans-serif}
.geo-card .gc-value{font-family:'Orbitron',sans-serif;font-size:20px;color:#e0d0ff;text-shadow:0 0 10px rgba(0,212,255,.2)}
.geo-card .gc-sub{font-size:11px;color:#00d4ff88;margin-top:2px}
.geo-card .gc-bar{margin-top:6px;height:3px;background:rgba(0,180,255,.1);border-radius:2px;overflow:hidden}
.geo-card .gc-bar .fill{height:100%;border-radius:2px}
@media(max-width:1024px){.bottom-panel{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.bottom-panel{grid-template-columns:1fr}.dash{padding:10px 12px}.top{flex-direction:column;gap:8px}.top-right{flex-wrap:wrap;gap:8px}}
</style>
</head>
<body>
<div class=dash>
<div class=top>
<h1>GEO_COMMAND</h1>
<div class=top-right><span>LIVE</span><span>·</span><span>42 ACTIVE NODES</span><span>·</span><span>REGIONS: 8</span></div>
</div>
<div class=map-area>
<div class=map-grid></div>
<div class=map-label style=top:20px;left:30px>NORTH AMERICA</div>
<div class=map-label style=top:20px;right:50px>EUROPE</div>
<div class=map-label style=bottom:60px;right:30px>APAC</div>
<div class=map-label style=bottom:30px;left:40px>LATAM</div>
<div class="map-pin" style=top:28%;left:22%><div class="pin hot"></div><div class=label>US-EAST (12)</div></div>
<div class="map-pin" style=top:25%;left:18%><div class="pin warm"></div><div class=label>US-WEST (8)</div></div>
<div class="map-pin" style=top:24%;left:52%><div class="pin info"></div><div class=label>EU-WEST (10)</div></div>
<div class="map-pin" style=top:30%;left:57%><div class="pin cool"></div><div class=label>EU-CENTRAL (6)</div></div>
<div class="map-pin" style=top:55%;left:68%><div class="pin warm"></div><div class=label>APAC (14)</div></div>
<div class="map-pin" style=top:58%;left:30%><div class="pin cool"></div><div class=label>LATAM (4)</div></div>
<div class="map-pin" style=top:32%;left:75%><div class="pin info"></div><div class=label>ME (3)</div></div>
</div>
<div class=bottom-panel>
<div class=geo-card><div class=gc-label>Total Requests</div><div class=gc-value>2.47M</div><div class=gc-sub>↑ 14.2% this hour</div><div class=gc-bar><div class=fill style=width:74%;background:linear-gradient(90deg,#00d4ff,#7c3aed)></div></div></div>
<div class=geo-card><div class=gc-label>Avg Latency</div><div class=gc-value>38ms</div><div class=gc-sub>fastest: US-EAST (12ms)</div><div class=gc-bar><div class=fill style=width:38%;background:linear-gradient(90deg,#22c55e,#00d4ff)></div></div></div>
<div class=geo-card><div class=gc-label>Bandwidth</div><div class=gc-value>1.84 Tbps</div><div class=gc-sub>↑ 8.7% vs yesterday</div><div class=gc-bar><div class=fill style=width:61%;background:linear-gradient(90deg,#7c3aed,#a855f7)></div></div></div>
<div class=geo-card><div class=gc-label>Error Rate</div><div class=gc-value>0.04%</div><div class=gc-sub style=color:#22c55e>● nominal</div><div class=gc-bar><div class=fill style=width:4%;background:#22c55e></div></div></div>
</div>
</div>
</body>
</html>
Mockup 6: user-profile-hub.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Profile Hub</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0820;color:#d0c0ff;font-family:'Rajdhani',sans-serif;min-height:100vh}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 30% 20%,rgba(120,0,255,.08),transparent 60%),radial-gradient(ellipse at 80% 80%,rgba(0,180,255,.04),transparent 50%);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:24px 32px;max-width:1200px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:28px}
h1{font-family:'Orbitron',sans-serif;font-size:20px;font-weight:700;color:#a855f7;text-shadow:0 0 20px rgba(168,85,247,.3);letter-spacing:3px}
.header-nav{display:flex;gap:20px;font-size:12px;font-family:'Orbitron',sans-serif;letter-spacing:1px}
.header-nav span{color:#a855f788;cursor:pointer;padding-bottom:4px;border-bottom:2px solid transparent;transition:all .2s}
.header-nav span:hover,.header-nav span.active{color:#a855f7;border-bottom-color:#a855f7}
.profile-hero{display:grid;grid-template-columns:auto 1fr;gap:24px;background:linear-gradient(135deg,rgba(30,10,60,.7),rgba(10,5,30,.7));border:1px solid rgba(168,85,247,.15);border-radius:16px;padding:24px;backdrop-filter:blur(10px);margin-bottom:20px;position:relative;overflow:hidden}
.profile-hero::before{content:'';position:absolute;top:-50%;right:-20%;width:300px;height:300px;background:radial-gradient(circle,rgba(168,85,247,.06),transparent);pointer-events:none}
.avatar-wrap{width:80px;height:80px;border-radius:50%;border:2px solid rgba(168,85,247,.4);display:flex;align-items:center;justify-content:center;position:relative;flex-shrink:0}
.avatar-wrap::before{content:'';position:absolute;inset:-4px;border-radius:50%;border:1px solid rgba(168,85,247,.2);animation:spin 6s linear infinite;border-top-color:#a855f7}
@keyframes spin{to{transform:rotate(360deg)}}
.avatar{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,#a855f7,#00d4ff);display:flex;align-items:center;justify-content:center;font-family:'Orbitron',sans-serif;font-size:24px;color:#fff;box-shadow:0 0 30px rgba(168,85,247,.3)}
.profile-info{display:flex;flex-direction:column;justify-content:center}
.profile-info .name{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:700;color:#e0d0ff}
.profile-info .role{font-size:14px;color:#a855f788;margin-top:2px}
.profile-info .meta{display:flex;gap:20px;margin-top:8px;font-size:12px;color:#a855f788}
.profile-info .meta span{display:flex;align-items:center;gap:6px}
.detail-grid{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:20px}
.detail-panel{background:linear-gradient(135deg,rgba(30,10,60,.6),rgba(10,5,30,.6));border:1px solid rgba(168,85,247,.1);border-radius:12px;padding:18px;backdrop-filter:blur(8px)}
.detail-panel .dp-title{font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:2px;color:#a855f788;margin-bottom:12px}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.info-field{display:flex;flex-direction:column;gap:2px}
.info-field .if-label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#a855f766}
.info-field .if-value{font-size:14px;color:#d0c0ff}
.activity-timeline{display:flex;flex-direction:column;gap:10px}
.tl-item{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid rgba(168,85,247,.04)}
.tl-item:last-child{border-bottom:none}
.tl-dot{width:8px;height:8px;border-radius:50%;background:#a855f7;margin-top:4px;box-shadow:0 0 8px #a855f7;flex-shrink:0}
.tl-content{flex:1}
.tl-content .tl-text{font-size:13px}
.tl-content .tl-time{font-size:10px;color:#a855f788;font-family:'Orbitron',sans-serif;margin-top:2px}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.stat-card{background:linear-gradient(135deg,rgba(30,10,60,.6),rgba(10,5,30,.6));border:1px solid rgba(168,85,247,.08);border-radius:10px;padding:14px;text-align:center;backdrop-filter:blur(6px)}
.stat-card .sc-val{font-family:'Orbitron',sans-serif;font-size:24px;color:#e0d0ff;text-shadow:0 0 10px rgba(168,85,247,.2)}
.stat-card .sc-label{font-size:10px;letter-spacing:2px;color:#a855f788;text-transform:uppercase;margin-top:4px}
.stat-card .sc-trend{font-size:11px;margin-top:2px}
@media(max-width:768px){.profile-hero{grid-template-columns:1fr;text-align:center;justify-items:center}.detail-grid{grid-template-columns:1fr}.info-grid{grid-template-columns:1fr}.stats-row{grid-template-columns:1fr}.dash{padding:16px}}
</style>
</head>
<body>
<div class=dash>
<header>
<h1>PROFILE_HUB</h1>
<div class=header-nav><span class=active>OVERVIEW</span><span>ACTIVITY</span><span>SECURITY</span><span>BILLING</span><span>TEAMS</span></div>
</header>
<div class=profile-hero>
<div class=avatar-wrap><div class=avatar>AK</div></div>
<div class=profile-info>
<div class=name>Alexei Korzhenevski</div>
<div class=role>Principal Engineer · Systems Division</div>
<div class=meta><span>● alexei@neocore.io</span><span>⌂ San Francisco, CA</span><span>⚑ Joined Mar 2023</span><span>⚡ Admin</span></div>
</div>
</div>
<div class=detail-grid>
<div class=detail-panel><div class=dp-title>ACCOUNT DETAILS</div><div class=info-grid><div class=info-field><span class=if-label>Department</span><span class=if-value>Engineering</span></div><div class=info-field><span class=if-label>Team</span><span class=if-value>Core Platform</span></div><div class=info-field><span class=if-label>Reports To</span><span class=if-value>Dr. N. Chen</span></div><div class=info-field><span class=if-label>Access Level</span><span class=if-value>Level 4 · Full</span></div><div class=info-field><span class=if-label>2FA</span><span class=if-value style=color:#22c55e>● Enabled</span></div><div class=info-field><span class=if-label>Last Login</span><span class=if-value>12s ago · US-EAST</span></div><div class=info-field><span class=if-label>Sessions</span><span class=if-value>3 active</span></div><div class=info-field><span class=if-label>API Keys</span><span class=if-value>4 keys · none expiring</span></div></div></div>
<div class=detail-panel><div class=dp-title>RECENT ACTIVITY</div><div class=activity-timeline><div class=tl-item><div class=tl-dot></div><div class=tl-content><div class=tl-text>Deployed v4.2.1 to production</div><div class=tl-time>14m ago</div></div></div><div class=tl-item><div class=tl-dot></div><div class=tl-content><div class=tl-text>Reviewed PR #847 - cache layer</div><div class=tl-time>1h ago</div></div></div><div class=tl-item><div class=tl-dot></div><div class=tl-content><div class=tl-text>Created cluster scaling policy</div><div class=tl-time>3h ago</div></div></div><div class=tl-item><div class=tl-dot></div><div class=tl-content><div class=tl-text>Updated CI/CD pipeline triggers</div><div class=tl-time>5h ago</div></div></div></div></div>
</div>
<div class=stats-row>
<div class=stat-card><div class=sc-val>847</div><div class=sc-label>Commits (30d)</div><div class=sc-trend style=color:#22c55e>↑ 12%</div></div>
<div class=stat-card><div class=sc-val>23</div><div class=sc-label>Open PRs</div><div class=sc-trend style=color:#facc15>7 awaiting review</div></div>
<div class=stat-card><div class=sc-val>99.7%</div><div class=sc-label>Deploy Success</div><div class=sc-trend style=color:#22c55e>● excellent</div></div>
</div>
</div>
</body>
</html>
Mockup 7: control-panel-settings.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Control Panel</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#08081a;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 70% 30%,rgba(0,180,255,.05),transparent 50%),radial-gradient(ellipse at 20% 70%,rgba(120,0,255,.04),transparent 50%);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:20px 30px;max-width:1200px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding-bottom:16px;border-bottom:1px solid rgba(0,180,255,.1);margin-bottom:24px}
h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;color:#00d4ff;text-shadow:0 0 20px rgba(0,212,255,.3);letter-spacing:3px}
.header-actions{display:flex;gap:10px}
.ctrl-btn{background:rgba(0,180,255,.05);border:1px solid rgba(0,180,255,.15);color:#00d4ff88;padding:6px 14px;border-radius:6px;font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:1px;cursor:pointer;transition:all .2s}
.ctrl-btn:hover{background:rgba(0,180,255,.1);border-color:#00d4ff44;color:#00d4ff}
.ctrl-btn.primary{background:linear-gradient(135deg,rgba(0,180,255,.2),rgba(0,212,255,.1));border-color:#00d4ff44;color:#00d4ff}
.set-grid{display:grid;grid-template-columns:240px 1fr;gap:20px}
.sidebar{background:linear-gradient(135deg,rgba(10,15,40,.6),rgba(5,8,25,.6));border:1px solid rgba(0,180,255,.08);border-radius:10px;padding:12px;backdrop-filter:blur(6px);height:fit-content}
.sidebar-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:6px;cursor:pointer;transition:all .2s;font-size:13px;color:#00d4ff88}
.sidebar-item:hover{background:rgba(0,180,255,.05);color:#00d4ff}
.sidebar-item.active{background:rgba(0,180,255,.1);color:#00d4ff;border-left:2px solid #00d4ff}
.sidebar-item .si-icon{width:20px;text-align:center;font-size:14px}
.content-area{display:flex;flex-direction:column;gap:16px}
.section{background:linear-gradient(135deg,rgba(10,15,40,.6),rgba(5,8,25,.6));border:1px solid rgba(0,180,255,.08);border-radius:10px;padding:18px;backdrop-filter:blur(6px)}
.section-title{font-family:'Orbitron',sans-serif;font-size:12px;letter-spacing:2px;color:#00d4ff88;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center}
.set-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(0,180,255,.04)}
.set-row:last-child{border-bottom:none}
.set-row .set-label{font-size:13px;display:flex;align-items:center;gap:8px}
.set-row .set-label .hint{font-size:10px;color:#00d4ff55}
.toggle{width:36px;height:20px;background:rgba(0,180,255,.1);border-radius:10px;position:relative;cursor:pointer;transition:all .3s;flex-shrink:0}
.toggle.on{background:#00d4ff44}
.toggle::after{content:'';position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#00d4ff66;transition:all .3s}
.toggle.on::after{left:18px;background:#00d4ff;box-shadow:0 0 8px #00d4ff}
.select-input{background:rgba(0,180,255,.05);border:1px solid rgba(0,180,255,.1);color:#00d4ff;font-family:'Rajdhani',sans-serif;font-size:13px;padding:4px 10px;border-radius:4px;cursor:pointer;outline:none}
.select-input option{background:#0a0a20}
.text-input{background:rgba(0,180,255,.03);border:1px solid rgba(0,180,255,.08);color:#c0d0ff;font-family:'Rajdhani',sans-serif;font-size:13px;padding:4px 10px;border-radius:4px;width:200px;outline:none;transition:border-color .2s}
.text-input:focus{border-color:#00d4ff44}
.action-buttons{display:flex;gap:10px;justify-content:flex-end;margin-top:8px}
@media(max-width:768px){.set-grid{grid-template-columns:1fr}.sidebar{display:flex;overflow-x:auto;padding:8px}.sidebar-item{white-space:nowrap}.text-input{width:100%}.dash{padding:12px 16px}header{flex-direction:column;gap:10px;align-items:flex-start}}
</style>
</head>
<body>
<div class=dash>
<header>
<h1>CONTROL_PANEL</h1>
<div class=header-actions><button class=ctrl-btn>UNDO</button><button class=ctrl-btn>SAVE DRAFT</button><button class="ctrl-btn primary">APPLY CHANGES</button></div>
</header>
<div class=set-grid>
<div class=sidebar>
<div class="sidebar-item active"><span class=si-icon>⚙</span> General</div>
<div class=sidebar-item><span class=si-icon>🔒</span> Security</div>
<div class=sidebar-item><span class=si-icon>📊</span> Monitoring</div>
<div class=sidebar-item><span class=si-icon>🔔</span> Notifications</div>
<div class=sidebar-item><span class=si-icon>🌐</span> Network</div>
<div class=sidebar-item><span class=si-icon>📁</span> Storage</div>
<div class=sidebar-item><span class=si-icon>👥</span> Team</div>
<div class=sidebar-item><span class=si-icon>⚡</span> Advanced</div>
</div>
<div class=content-area>
<div class=section>
<div class=section-title><span>SYSTEM PREFERENCES</span><span style=color:#00d4ff44>6 settings</span></div>
<div class=set-row><span class=set-label>Auto-scaling <span class=hint>dynamically provision workers</span></span><div class="toggle on"></div></div>
<div class=set-row><span class=set-label>Maintenance mode <span class=hint>block external traffic</span></span><div class=toggle></div></div>
<div class=set-row><span class=set-label>Metrics collection <span class=hint>gather system telemetry</span></span><div class="toggle on"></div></div>
<div class=set-row><span class=set-label>Default region</span><select class=select-input><option>US-EAST (default)</option><option>US-WEST</option><option>EU-WEST</option><option>APAC</option></select></div>
<div class=set-row><span class=set-label>Log retention</span><select class=select-input><option>30 days</option><option>90 days</option><option>180 days</option><option selected>365 days</option></select></div>
<div class=set-row><span class=set-label>Environment</span><select class=select-input><option>Production</option><option>Staging</option><option>Development</option></select></div>
</div>
<div class=section>
<div class=section-title><span>NOTIFICATION RULES</span><span style=color:#00d4ff44>3 active</span></div>
<div class=set-row><span class=set-label>Critical alerts <span class=hint>P0 incidents, outages</span></span><div class="toggle on"></div></div>
<div class=set-row><span class=set-label>Deployment notices <span class=hint>build + deploy events</span></span><div class="toggle on"></div></div>
<div class=set-row><span class=set-label>Weekly digests <span class=hint>performance summaries</span></span><div class=toggle></div></div>
<div class=set-row><span class=set-label>Webhook URL</span><input class=text-input placeholder="https://hooks.example.com/..." value="https://hooks.neocore.io/events"></div>
</div>
<div class=action-buttons><button class=ctrl-btn>CANCEL</button><button class="ctrl-btn primary">SAVE ALL</button></div>
</div>
</div>
</div>
</body>
</html>
Mockup 8: pipeline-workflow.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Pipeline Workflow</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e1a;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 50% 0%,rgba(0,200,255,.04),transparent 70%);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:20px 30px;max-width:1400px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid rgba(0,200,255,.1);margin-bottom:20px}
h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;color:#00c8ff;text-shadow:0 0 15px rgba(0,200,255,.3);letter-spacing:3px;display:flex;align-items:center;gap:10px}
h1 .badge{font-size:9px;background:rgba(0,200,255,.1);border:1px solid rgba(0,200,255,.2);padding:2px 8px;border-radius:4px;color:#00c8ff88;letter-spacing:1px}
.header-info{display:flex;gap:20px;font-size:11px;color:#00c8ff88;font-family:'Orbitron',sans-serif;letter-spacing:1px}
.pipeline-bar{display:flex;gap:0;align-items:stretch;margin-bottom:24px;background:linear-gradient(135deg,rgba(0,20,40,.6),rgba(0,10,20,.6));border:1px solid rgba(0,200,255,.1);border-radius:10px;overflow:hidden;backdrop-filter:blur(6px)}
.pipe-stage{flex:1;padding:14px 12px;text-align:center;position:relative;display:flex;flex-direction:column;align-items:center;gap:4px}
.pipe-stage:not(:last-child)::after{content:'';position:absolute;right:-1px;top:20%;height:60%;width:1px;background:rgba(0,200,255,.1)}
.pipe-stage .ps-icon{font-size:20px;margin-bottom:2px}
.pipe-stage .ps-name{font-size:10px;letter-spacing:2px;color:#00c8ff88;text-transform:uppercase;font-family:'Orbitron',sans-serif}
.pipe-stage .ps-status{font-size:11px;font-weight:600}
.pipe-stage.done .ps-status{color:#22c55e}
.pipe-stage.active .ps-status{color:#00c8ff}
.pipe-stage.active{background:rgba(0,200,255,.04)}
.pipe-stage.active::before{content:'';position:absolute;bottom:0;left:10%;width:80%;height:2px;background:#00c8ff;border-radius:2px;box-shadow:0 0 10px #00c8ff;animation:flowPulse 2s ease-in-out infinite}
@keyframes flowPulse{0%,100%{opacity:.6}50%{opacity:1}}
.pipe-stage.pending .ps-status{color:#64748b}
.pipe-stage.fail .ps-status{color:#ef4444}
.pipeline-detail{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.pl-card{background:linear-gradient(135deg,rgba(0,20,40,.6),rgba(0,10,20,.6));border:1px solid rgba(0,200,255,.08);border-radius:10px;padding:16px;backdrop-filter:blur(6px)}
.pl-card .pl-title{font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:2px;color:#00c8ff88;margin-bottom:12px}
.pl-card .pl-title .count{font-size:10px;color:#00c8ff44;margin-left:8px}
.log-line{display:flex;gap:8px;padding:3px 0;font-size:12px;font-family:'JetBrains Mono',monospace,monospace;border-bottom:1px solid rgba(0,200,255,.03)}
.log-line .ll-time{color:#00c8ff44;width:56px;flex-shrink:0}
.log-line .ll-msg{flex:1;color:#a0c0e0}
.log-line.ll-pass .ll-msg{color:#22c55e}
.log-line.ll-fail .ll-msg{color:#ef4444}
.log-line.ll-info .ll-msg{color:#00c8ff}
.runner-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.runner{display:flex;align-items:center;gap:8px;padding:6px 8px;background:rgba(0,200,255,.02);border-radius:6px;font-size:12px}
.runner .r-name{flex:1}
.runner .r-time{font-family:'Orbitron',sans-serif;font-size:10px;color:#00c8ff66}
.build-artifacts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.artifact{background:linear-gradient(135deg,rgba(0,20,40,.6),rgba(0,10,20,.6));border:1px solid rgba(0,200,255,.08);border-radius:8px;padding:12px;display:flex;align-items:center;gap:10px}
.artifact .a-icon{font-size:24px}
.artifact .a-info{flex:1}
.artifact .a-name{font-size:13px;font-weight:600}
.artifact .a-size{font-size:10px;color:#00c8ff66;font-family:'Orbitron',sans-serif}
.artifact .a-status{font-size:10px;padding:1px 6px;border-radius:3px}
.a-status.pass{background:rgba(34,197,94,.1);color:#22c55e;border:1px solid rgba(34,197,94,.2)}
.a-status.build{background:rgba(0,200,255,.1);color:#00c8ff;border:1px solid rgba(0,200,255,.2)}
@media(max-width:1024px){.pipeline-detail{grid-template-columns:1fr}.build-artifacts{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.pipeline-bar{flex-direction:column}.pipe-stage:not(:last-child)::after{display:none}.build-artifacts{grid-template-columns:1fr}.dash{padding:12px 16px}header{flex-direction:column;gap:8px;align-items:flex-start}}
</style>
</head>
<body>
<div class=dash>
<header>
<h1>PIPELINE_RUN <span class=badge>#8472</span></h1>
<div class=header-info><span>STATUS: IN PROGRESS</span><span>BRANCH: main</span><span>COMMIT: 4a7b2f1</span><span>TRIGGER: push</span></div>
</header>
<div class=pipeline-bar>
<div class="pipe-stage done"><div class=ps-icon>📦</div><div class=ps-name>Build</div><div class=ps-status>✓ Passed</div></div>
<div class="pipe-stage done"><div class=ps-icon>🔬</div><div class=ps-name>Lint</div><div class=ps-status>✓ Passed</div></div>
<div class="pipe-stage done"><div class=ps-icon>🧪</div><div class=ps-name>Unit Tests</div><div class=ps-status>✓ 84/84</div></div>
<div class="pipe-stage active"><div class=ps-icon>⚡</div><div class=ps-name>Integration</div><div class=ps-status>◉ 12/28 passing</div></div>
<div class="pipe-stage pending"><div class=ps-icon>📊</div><div class=ps-name>Benchmark</div><div class=ps-status>○ Queued</div></div>
<div class="pipe-stage pending"><div class=ps-icon>🚀</div><div class=ps-name>Deploy</div><div class=ps-status>○ Waiting</div></div>
</div>
<div class=pipeline-detail>
<div class=pl-card><div class=pl-title>LIVE BUILD LOG <span class=count>last 8 lines</span></div><div class=log-line class=ll-pass><span class=ll-time>12:47:03</span><span class=ll-msg>✓ Build artifact created: neocore-v4.2.1.tar.gz</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:58</span><span class=ll-msg>✓ Module federation resolved (12/12)</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:42</span><span class=ll-msg>✓ Webpack bundle completed (2.4s)</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:40</span><span class=ll-msg>✓ TypeScript compilation: 0 errors</span></div><div class="log-line ll-info"><span class=ll-time>12:46:30</span><span class=ll-msg>◉ Starting integration test suite...</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:22</span><span class=ll-msg>✓ All 84 unit tests passed</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:18</span><span class=ll-msg>✓ ESLint: 0 warnings, 0 errors</span></div><div class="log-line ll-pass"><span class=ll-time>12:46:10</span><span class=ll-msg>✓ Dependency install: 247 packages cached</span></div></div>
<div class=pl-card><div class=pl-title>PARALLEL RUNNERS <span class=count>6 active</span></div><div class=runner-grid><div class=runner><span class=r-name>test:core</span><span class=r-time>12.4s</span><span style=color:#22c55e>✓</span></div><div class=runner><span class=r-name>test:api</span><span class=r-time>18.7s</span><span style=color:#22c55e>✓</span></div><div class=runner><span class=r-name>test:integ</span><span class=r-time>24.1s</span><span style=color:#00c8ff>◉</span></div><div class=runner><span class=r-name>bench:perf</span><span class=r-time>—</span><span style=color:#64748b>○</span></div><div class=runner><span class=r-name>bundle:analyze</span><span class=r-time>—</span><span style=color:#64748b>○</span></div><div class=runner><span class=r-name>docker:build</span><span class=r-time>—</span><span style=color:#64748b>○</span></div></div></div>
</div>
<div class=build-artifacts>
<div class=artifact><div class=a-icon>📦</div><div class=a-info><div class=a-name>neocore-v4.2.1.tar.gz</div><div class=a-size>24.7 MB</div></div><span class="a-status pass">✓ Signed</span></div>
<div class=artifact><div class=a-icon>🐳</div><div class=a-info><div class=a-name>ghcr.io/neocore/api:latest</div><div class=a-size>187 MB</div></div><span class="a-status build">◉ Building</span></div>
<div class=artifact><div class=a-icon>📋</div><div class=a-info><div class=a-name>test-report-8472.html</div><div class=a-size>1.2 MB</div></div><span class="a-status pass">✓ Ready</span></div>
</div>
</div>
</body>
</html>
Mockup 9: calendar-timeline-dashboard.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Timeline Hub</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#080818;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 30% 50%,rgba(60,0,200,.06),transparent 60%),radial-gradient(ellipse at 80% 20%,rgba(0,200,255,.04),transparent 50%);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:20px 30px;max-width:1200px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid rgba(100,0,255,.15);margin-bottom:20px}
h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;background:linear-gradient(90deg,#7c3aed,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px}
.nav-controls{display:flex;align-items:center;gap:12px}
.nav-controls .arrow{color:#7c3aed88;cursor:pointer;font-size:18px;padding:2px 6px;border:1px solid rgba(124,58,237,.15);border-radius:4px;transition:all .2s}
.nav-controls .arrow:hover{color:#7c3aed;border-color:#7c3aed44}
.nav-controls .period-label{font-family:'Orbitron',sans-serif;font-size:13px;color:#7c3aed88;letter-spacing:1px;min-width:160px;text-align:center}
.timeline-grid{display:grid;grid-template-columns:70px 1fr;gap:8px;margin-bottom:20px}
.time-axis{display:flex;flex-direction:column;gap:4px;padding-top:28px}
.time-axis .tick{height:48px;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;font-family:'Orbitron',sans-serif;font-size:10px;color:#7c3aed66}
.events-track{position:relative;min-height:300px;background:linear-gradient(135deg,rgba(20,10,50,.5),rgba(10,5,30,.5));border:1px solid rgba(124,58,237,.08);border-radius:10px;padding:12px;backdrop-filter:blur(4px)}
.day-headers{display:grid;grid-template-columns:repeat(7,1fr);margin-bottom:8px}
.day-header{text-align:center;font-family:'Orbitron',sans-serif;font-size:9px;letter-spacing:1px;color:#7c3aed66;text-transform:uppercase}
.day-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.day-cell{aspect-ratio:1;background:rgba(124,58,237,.02);border-radius:6px;padding:4px;display:flex;flex-direction:column;align-items:center;font-size:11px;color:#7c3aed88;cursor:pointer;transition:all .2s;position:relative;min-height:50px}
.day-cell:hover{background:rgba(124,58,237,.08)}
.day-cell.today{border:1px solid rgba(124,58,237,.4);box-shadow:0 0 15px rgba(124,58,237,.1)}
.day-cell.other-month{opacity:.3}
.day-cell .date{font-family:'Orbitron',sans-serif;font-size:11px}
.day-cell .event-dot{width:5px;height:5px;border-radius:50%;background:#7c3aed;box-shadow:0 0 6px #7c3aed;margin-top:2px}
.day-cell .event-dot.multi{background:#00d4ff;box-shadow:0 0 6px #00d4ff}
.bottom-panels{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.bp-card{background:linear-gradient(135deg,rgba(20,10,50,.5),rgba(10,5,30,.5));border:1px solid rgba(124,58,237,.08);border-radius:10px;padding:16px;backdrop-filter:blur(4px)}
.bp-title{font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:2px;color:#7c3aed88;margin-bottom:12px}
.event-list{display:flex;flex-direction:column;gap:8px}
.tl-event{display:flex;gap:10px;padding:8px 10px;background:rgba(124,58,237,.03);border-radius:6px;border-left:3px solid #7c3aed88}
.tl-event .ev-time{font-family:'Orbitron',sans-serif;font-size:10px;color:#7c3aed88;width:50px;flex-shrink:0}
.tl-event .ev-info{flex:1}
.tl-event .ev-title{font-size:13px}
.tl-event .ev-sub{font-size:10px;color:#7c3aed88}
.sprint-track{display:flex;flex-direction:column;gap:8px}
.sprint{display:flex;align-items:center;gap:10px;padding:8px 10px;background:rgba(124,58,237,.03);border-radius:6px}
.sprint .s-name{flex:1;font-size:13px}
.sprint .s-dates{font-size:10px;color:#7c3aed88;font-family:'Orbitron',sans-serif}
.sprint .s-bar{width:80px;height:4px;background:rgba(124,58,237,.1);border-radius:2px;overflow:hidden}
.sprint .s-bar .fill{height:100%;border-radius:2px}
@media(max-width:768px){.timeline-grid{grid-template-columns:1fr}.time-axis{display:none}.day-cell{min-height:36px}.bottom-panels{grid-template-columns:1fr}.dash{padding:12px 16px}header{flex-direction:column;gap:8px}}
</style>
</head>
<body>
<div class=dash>
<header>
<h1>TIMELINE_HUB</h1>
<div class=nav-controls><span class=arrow>◀</span><span class=period-label>JUNE 2026</span><span class=arrow>▶</span></div>
</header>
<div class=timeline-grid>
<div class=time-axis></div>
<div class=events-track>
<div class=day-headers><div class=day-header>Mon</div><div class=day-header>Tue</div><div class=day-header>Wed</div><div class=day-header>Thu</div><div class=day-header>Fri</div><div class=day-header>Sat</div><div class=day-header>Sun</div></div>
<div class=day-grid>
<div class="day-cell other-month"><span class=date>25</span></div>
<div class="day-cell other-month"><span class=date>26</span></div>
<div class="day-cell other-month"><span class=date>27</span></div>
<div class="day-cell other-month"><span class=date>28</span></div>
<div class="day-cell other-month"><span class=date>29</span></div>
<div class="day-cell other-month"><span class=date>30</span></div>
<div class="day-cell other-month"><span class=date>31</span></div>
<div class=day-cell><span class=date>1</span><div class=event-dot></div></div>
<div class=day-cell><span class=date>2</span></div>
<div class=day-cell><span class=date>3</span><div class=event-dot></div></div>
<div class=day-cell><span class=date>4</span></div>
<div class=day-cell><span class=date>5</span><div class="event-dot multi"></div></div>
<div class=day-cell><span class=date>6</span></div>
<div class=day-cell><span class=date>7</span></div>
<div class=day-cell><span class=date>8</span><div class=event-dot></div></div>
<div class=day-cell><span class=date>9</span></div>
<div class=day-cell><span class=date>10</span></div>
<div class="day-cell today"><span class=date>11</span><div class="event-dot multi"></div></div>
<div class=day-cell><span class=date>12</span></div>
<div class=day-cell><span class=date>13</span></div>
<div class=day-cell><span class=date>14</span></div>
<div class=day-cell><span class=date>15</span><div class=event-dot></div></div>
<div class=day-cell><span class=date>16</span><div class=event-dot></div></div>
<div class=day-cell><span class=date>17</span></div>
<div class=day-cell><span class=date>18</span></div>
<div class=day-cell><span class=date>19</span></div>
<div class=day-cell><span class=date>20</span></div>
<div class=day-cell><span class=date>21</span></div>
<div class=day-cell><span class=date>22</span><div class=event-dot></div></div>
</div>
</div>
</div>
<div class=bottom-panels>
<div class=bp-card><div class=bp-title>UPCOMING EVENTS</div><div class=event-list><div class=tl-event><span class=ev-time>09:00</span><div class=ev-info><div class=ev-title>Sprint Planning · Platform Team</div><div class=ev-sub>Room Holo-3 · 12 attendees</div></div></div><div class=tl-event><span class=ev-time>14:00</span><div class=ev-info><div class=ev-title>Architecture Review · Cache Strategy</div><div class=ev-sub>Lead: A. Korzhenevski · 45 min</div></div></div><div class=tl-event><span class=ev-time>16:30</span><div class=ev-info><div class=ev-title>Deploy Window · v4.2.1</div><div class=ev-sub>Pipeline #8472 · auto-rollback enabled</div></div></div></div></div>
<div class=bp-card><div class=bp-title>ACTIVE SPRINTS</div><div class=sprint-track><div class=sprint><span class=s-name>Sprint 24 · Core</span><span class=s-dates>Jun 8 — Jun 22</span><div class=s-bar><div class=fill style=width:60%;background:linear-gradient(90deg,#7c3aed,#a855f7)></div></div></div><div class=sprint><span class=s-name>Sprint 12 · Platform</span><span class=s-dates>Jun 1 — Jun 15</span><div class=s-bar><div class=fill style=width:88%;background:linear-gradient(90deg,#7c3aed,#00d4ff)></div></div></div><div class=sprint><span class=s-name>Sprint 7 · Mobile</span><span class=s-dates>Jun 15 — Jun 29</span><div class=s-bar><div class=fill style=width:24%;background:linear-gradient(90deg,#7c3aed,#f97316)></div></div></div><div class=sprint><span class=s-name>Sprint 3 · Data</span><span class=s-dates>Jun 22 — Jul 6</span><div class=s-bar><div class=fill style=width:8%;background:linear-gradient(90deg,#7c3aed,#f97316)></div></div></div></div></div>
</div>
</div>
</body>
</html>
Mockup 10: ai-assistant-dashboard.html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>AI Command</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#05051a;color:#c0d0ff;font-family:'Rajdhani',sans-serif;min-height:100vh}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 50% 30%,rgba(0,100,255,.05),transparent 60%),radial-gradient(ellipse at 80% 70%,rgba(100,0,255,.03),transparent 50%);pointer-events:none;z-index:0}
.dash{position:relative;z-index:1;padding:20px 30px;max-width:1200px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid rgba(60,100,255,.15);margin-bottom:20px}
h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;background:linear-gradient(90deg,#3b82f6,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px;display:flex;align-items:center;gap:10px}
h1 .status-pulse{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 12px #22c55e;animation:pulseS 2s ease-in-out infinite}
@keyframes pulseS{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(1.4)}}
.status-line{display:flex;gap:16px;font-size:10px;color:#3b82f688;font-family:'Orbitron',sans-serif;letter-spacing:1px}
.conversation-area{display:grid;grid-template-columns:1fr 320px;gap:16px;margin-bottom:20px}
.chat-panel{background:linear-gradient(135deg,rgba(10,10,50,.6),rgba(5,5,30,.6));border:1px solid rgba(60,100,255,.1);border-radius:12px;padding:16px;backdrop-filter:blur(6px);display:flex;flex-direction:column;min-height:360px}
.chat-messages{flex:1;display:flex;flex-direction:column;gap:10px;overflow-y:auto;padding-right:4px;margin-bottom:12px}
.msg{display:flex;gap:10px;padding:10px 12px;border-radius:8px;max-width:85%;font-size:13px;line-height:1.4}
.msg.user{background:rgba(60,100,255,.08);align-self:flex-end;border-bottom-right-radius:2px}
.msg.assistant{background:rgba(30,30,80,.4);align-self:flex-start;border-bottom-left-radius:2px;border-left:2px solid #3b82f766}
.msg .msg-time{font-size:9px;color:#3b82f644;font-family:'Orbitron',sans-serif;margin-top:4px}
.msg .msg-icon{width:20px;height:20px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#a855f7);display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;flex-shrink:0}
.chat-input{display:flex;gap:8px;border-top:1px solid rgba(60,100,255,.08);padding-top:10px}
.chat-input input{flex:1;background:rgba(60,100,255,.03);border:1px solid rgba(60,100,255,.1);border-radius:6px;padding:8px 12px;color:#c0d0ff;font-family:'Rajdhani',sans-serif;font-size:13px;outline:none}
.chat-input input:focus{border-color:#3b82f644}
.chat-input button{background:linear-gradient(135deg,rgba(60,100,255,.2),rgba(168,85,247,.1));border:1px solid rgba(60,100,255,.2);color:#3b82f6;padding:6px 16px;border-radius:6px;font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:1px;cursor:pointer;transition:all .2s}
.chat-input button:hover{background:linear-gradient(135deg,rgba(60,100,255,.3),rgba(168,85,247,.15));box-shadow:0 0 15px rgba(60,100,255,.2)}
.context-panel{background:linear-gradient(135deg,rgba(10,10,50,.6),rgba(5,5,30,.6));border:1px solid rgba(60,100,255,.1);border-radius:12px;padding:16px;backdrop-filter:blur(6px)}
.context-panel .cp-title{font-family:'Orbitron',sans-serif;font-size:10px;letter-spacing:2px;color:#3b82f688;margin-bottom:12px}
.context-item{display:flex;align-items:center;gap:8px;padding:8px 10px;background:rgba(60,100,255,.03);border-radius:6px;margin-bottom:6px;font-size:12px}
.context-item .ci-icon{width:24px;text-align:center;font-size:14px}
.context-item .ci-info{flex:1}
.context-item .ci-info .ci-name{font-size:12px;color:#c0d0ff}
.context-item .ci-info .ci-detail{font-size:10px;color:#3b82f688}
.bottom-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.ai-card{background:linear-gradient(135deg,rgba(10,10,50,.6),rgba(5,5,30,.6));border:1px solid rgba(60,100,255,.08);border-radius:10px;padding:14px;backdrop-filter:blur(6px);display:flex;flex-direction:column;align-items:center;text-align:center}
.ai-card .ac-val{font-family:'Orbitron',sans-serif;font-size:24px;color:#3b82f6;text-shadow:0 0 15px rgba(59,130,246,.3)}
.ai-card .ac-label{font-size:10px;letter-spacing:1px;color:#3b82f688;text-transform:uppercase;margin-top:4px}
.ai-card .ac-sub{font-size:10px;color:#3b82f688;margin-top:2px}
.ai-card .ac-bar{width:100%;height:3px;background:rgba(60,100,255,.1);border-radius:2px;margin-top:8px;overflow:hidden}
.ai-card .ac-bar .fill{height:100%;border-radius:2px}
.ai-card .ac-bar .fill.good{background:linear-gradient(90deg,#3b82f6,#22c55e);width:92%}
.ai-card .ac-bar .fill.warn{background:linear-gradient(90deg,#f97316,#facc15);width:67%}
.ai-card .ac-bar .fill.info{background:linear-gradient(90deg,#a855f7,#3b82f6);width:100%}
@media(max-width:1024px){.conversation-area{grid-template-columns:1fr}.bottom-cards{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.bottom-cards{grid-template-columns:1fr}.dash{padding:12px 16px}header{flex-direction:column;gap:8px;align-items:flex-start}.status-line{flex-wrap:wrap;gap:8px}}
</style>
</head>
<body>
<div class=dash>
<header>
<h1><span class=status-pulse></span>AI_COMMAND</h1>
<div class=status-line><span>MODEL: NEXUS-4</span><span>TOKENS: 847/4096</span><span>LATENCY: 124ms</span><span>SESSION: 47m</span></div>
</header>
<div class=conversation-area>
<div class=chat-panel>
<div class=chat-messages>
<div class="msg assistant"><div class=msg-icon>AI</div><div><div>I have analyzed the cache layer. Three nodes show elevated read latency. Recommend rebalancing replica shards 4-7.</div><div class=msg-time>12:47:03 · just now</div></div></div>
<div class="msg user"><div><div>Run diagnostics on the Delta-Cache cluster and report degradation thresholds</div><div class=msg-time>12:46:48 · 15s ago</div></div></div>
<div class="msg assistant"><div class=msg-icon>AI</div><div><div>Diagnostics complete. Delta-Cache: 81% memory utilization (threshold: 75%), read latency p95 at 247ms (threshold: 200ms). Recommend immediate scaling or key eviction.</div><div class=msg-time>12:46:32 · 31s ago</div></div></div>
<div class="msg user"><div><div>Show me the current system health summary</div><div class=msg-time>12:45:10 · 2m ago</div></div></div>
</div>
<div class=chat-input><input placeholder="Ask AI Command..." value="Scale Delta-Cache by +2"><button>SEND</button></div>
</div>
<div class=context-panel>
<div class=cp-title>CONTEXT WINDOW</div>
<div class=context-item><span class=ci-icon>📊</span><div class=ci-info><div class=ci-name>System Monitor</div><div class=ci-detail>47 nodes · 0 critical</div></div></div>
<div class=context-item><span class=ci-icon>🔧</span><div class=ci-info><div class=ci-name>Delta-Cache Cluster</div><div class=ci-detail>Warning: 81% memory</div></div></div>
<div class=context-item><span class=ci-icon>🚀</span><div class=ci-info><div class=ci-name>Pipeline #8472</div><div class=ci-detail>Integration: 12/28</div></div></div>
<div class=context-item><span class=ci-icon>👤</span><div class=ci-info><div class=ci-name>Active Session</div><div class=ci-detail>A. Korzhenevski · Admin</div></div></div>
<div class=context-item><span class=ci-icon>📋</span><div class=ci-info><div class=ci-name>Recent Actions</div><div class=ci-detail>3 pending approvals</div></div></div>
<hr style=border:none;border-top:1px solid rgba(60,100,255,.06);margin:10px 0>
<div class=cp-title>SUGGESTED ACTIONS</div>
<div class=context-item style=cursor:pointer><span class=ci-icon>⚡</span><div class=ci-info><div class=ci-name>Scale Delta-Cache</div><div class=ci-detail>+2 workers · estimated 4m</div></div></div>
<div class=context-item style=cursor:pointer><span class=ci-icon>📊</span><div class=ci-info><div class=ci-name>Generate Report</div><div class=ci-detail>Weekly performance summary</div></div></div>
</div>
</div>
<div class=bottom-cards>
<div class=ai-card><div class=ac-val>99.97%</div><div class=ac-label>Uptime SLA</div><div class=ac-sub>30d rolling</div><div class=ac-bar><div class="fill good"></div></div></div>
<div class=ai-card><div class=ac-val>847</div><div class=ac-label>Queries Today</div><div class=ac-sub>↑ 18% vs yesterday</div><div class=ac-bar><div class="fill warn"></div></div></div>
<div class=ai-card><div class=ac-val>94.2%</div><div class=ac-label>Confidence Score</div><div class=ac-sub>↑ 2.1pp this week</div><div class=ac-bar><div class="fill info"></div></div></div>
</div>
</div>
</body>
</html>