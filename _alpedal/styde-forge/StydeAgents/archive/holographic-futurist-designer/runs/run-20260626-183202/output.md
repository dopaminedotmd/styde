```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0d1117;color:#e6f1ff;font-family:'Space Grotesk',sans-serif;display:grid;grid-template-columns:220px 1fr;min-height:100vh;overflow-x:hidden}
.sidebar{background:rgba(0,240,255,.04);border-right:1px solid rgba(0,240,255,.12);padding:24px 16px}.sidebar h2{color:#00f0ff;font-size:14px;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px;text-shadow:0 0 20px rgba(0,240,255,.3)}.sidebar a{display:block;padding:10px 12px;color:#8b949e;text-decoration:none;font-size:13px;border-radius:8px;margin-bottom:4px;border-left:2px solid transparent}.sidebar a.active,.sidebar a:hover{background:rgba(0,240,255,.08);color:#00f0ff;border-left-color:#00f0ff}
.main{padding:32px 40px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:36px}.header h1{font-size:22px;font-weight:600;background:linear-gradient(135deg,#00f0ff,#00bcd4);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.header .badge{background:rgba(0,240,255,.12);color:#00f0ff;padding:6px 16px;border-radius:20px;font-size:12px;border:1px solid rgba(0,240,255,.2);text-shadow:0 0 10px rgba(0,240,255,.2)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:28px}
.card{background:rgba(255,255,255,.03);border:1px solid rgba(0,240,255,.1);border-radius:16px;padding:20px;backdrop-filter:blur(12px);transition:.3s}.card:hover{border-color:#00f0ff;box-shadow:0 0 30px rgba(0,240,255,.12);transform:translateY(-2px)}.card .value{font-size:28px;font-weight:700;color:#00f0ff;text-shadow:0 0 20px rgba(0,240,255,.15)}.card .label{font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:2px;margin-top:6px}.card .sub{font-size:12px;color:#58a6ff;margin-top:8px}
.activity{background:rgba(255,255,255,.02);border:1px solid rgba(0,240,255,.08);border-radius:16px;padding:20px}.activity h3{font-size:13px;color:#00f0ff;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px}.row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:13px}.row .stat{color:#00f0ff}
.pulse{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;background:radial-gradient(ellipse at 80% 20%,rgba(0,240,255,.03) 0%,transparent 60%)}
</style></head><body>
<div class="pulse"></div>
<nav class="sidebar"><h2>✦ NEXUS</h2><a href="#" class="active">Dashboard</a><a href="#">Analytics</a><a href="#">Nodes</a><a href="#">Network</a><a href="#">Settings</a></nav>
<div class="main">
<div class="header"><h1>Neon Command Center</h1><span class="badge">● LIVE — 12 nodes</span></div>
<div class="grid">
<div class="card"><div class="value">4,892</div><div class="label">Active Sessions</div><div class="sub">▲ 12% from yesterday</div></div>
<div class="card"><div class="value">94.7%</div><div class="label">Uptime</div><div class="sub">▼ 0.3% this week</div></div>
<div class="card"><div class="value">128</div><div class="label">Connected Devices</div><div class="sub">▲ 8 new today</div></div>
</div>
<div class="activity"><h3>Recent Activity</h3><div class="row"><span>Node Alpha — sync complete</span><span class="stat">2m ago</span></div><div class="row"><span>Gateway 7 — handshake</span><span class="stat">5m ago</span></div><div class="row"><span>Firmware update deployed</span><span class="stat">12m ago</span></div></div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#1a0a2e;color:#e0d4ff;font-family:'Orbitron',sans-serif;overflow-x:hidden}
.nav{display:flex;justify-content:space-between;align-items:center;padding:18px 40px;border-bottom:1px solid rgba(255,0,255,.12);background:rgba(10,0,20,.6);backdrop-filter:blur(16px);position:sticky;top:0;z-index:10}
.nav h1{font-size:15px;color:#ff00ff;letter-spacing:4px;text-shadow:0 0 25px rgba(255,0,255,.25)}.nav a{color:#a78bfa;text-decoration:none;font-size:11px;margin-left:24px;letter-spacing:2px}.nav a.active{color:#ff00ff}
.hero{padding:48px 40px 24px;text-align:center}.hero h2{font-size:36px;font-weight:800;background:linear-gradient(135deg,#ff00ff,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;letter-spacing:2px}.hero p{color:#a78bfa;font-size:12px;letter-spacing:4px;margin-top:8px}
.glance{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;padding:24px 40px}
.g-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,0,255,.08);border-radius:20px;padding:24px;text-align:center;backdrop-filter:blur(8px);transition:.3s;position:relative;overflow:hidden}.g-card::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:conic-gradient(from 0deg,transparent,rgba(255,0,255,.06),transparent);animation:spin 6s linear infinite;pointer-events:none}@keyframes spin{to{transform:rotate(360deg)}}.g-card:hover{border-color:#ff00ff;box-shadow:0 0 40px rgba(255,0,255,.1)}
.g-card .num{font-size:32px;font-weight:800;color:#c084fc;text-shadow:0 0 25px rgba(192,132,252,.2)}.g-card .lbl{font-size:9px;letter-spacing:3px;color:#9ca3af;margin-top:10px}
.metrics{margin:24px 40px;background:rgba(255,255,255,.02);border:1px solid rgba(255,0,255,.06);border-radius:20px;padding:24px;backdrop-filter:blur(8px)}
.metrics h3{font-size:11px;color:#ff00ff;letter-spacing:3px;margin-bottom:16px}.bar{display:flex;align-items:center;margin-bottom:12px;font-size:10px;letter-spacing:2px;color:#c4b5fd}.bar-fill{height:8px;background:linear-gradient(90deg,#ff00ff,#7c3aed);border-radius:4px;margin-left:12px;flex:1;max-width:70%;box-shadow:0 0 12px rgba(255,0,255,.2)}
</style></head><body>
<nav class="nav"><h1>✦ DREAMCORE</h1><div><a href="#" class="active">Dashboard</a><a href="#">Clusters</a><a href="#">Agents</a><a href="#">Logs</a></div></nav>
<div class="hero"><h2>System Pulse</h2><p>MAGENTA GRID v2.4 — 6 CLUSTERS ONLINE</p></div>
<div class="glance">
<div class="g-card"><div class="num">2,847</div><div class="lbl">✦ AGENTS</div></div>
<div class="g-card"><div class="num">99.2%</div><div class="lbl">✦ ACCURACY</div></div>
<div class="g-card"><div class="num">1.4s</div><div class="lbl">✦ LATENCY</div></div>
<div class="g-card"><div class="num">18</div><div class="lbl">✦ QUEUE</div></div>
</div>
<div class="metrics"><h3>CLUSTER LOAD</h3><div class="bar"><span>PRIME</span><div class="bar-fill" style="width:78%"></div><span>78%</span></div><div class="bar"><span>SECONDARY</span><div class="bar-fill" style="width:42%"></div><span>42%</span></div><div class="bar"><span>EDGE</span><div class="bar-fill" style="width:91%"></div><span>91%</span></div></div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0f0b00;color:#ffeedd;font-family:'Rajdhani',sans-serif;display:flex;flex-direction:column;align-items:center;min-height:100vh;padding:48px 24px}
.wrap{max-width:720px;width:100%}.tag{display:inline-block;padding:4px 14px;border:1px solid rgba(255,179,0,.25);border-radius:20px;color:#ffb300;font-size:11px;letter-spacing:3px;margin-bottom:32px;text-shadow:0 0 12px rgba(255,179,0,.12)}
h1{font-size:42px;font-weight:700;line-height:1.1;margin-bottom:8px;background:linear-gradient(135deg,#ffb300,#ff8f00);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{font-size:14px;color:#a0824a;letter-spacing:2px;margin-bottom:48px;border-left:2px solid rgba(255,179,0,.3);padding-left:16px}
.h-bar{display:flex;align-items:center;padding:16px 0;border-bottom:1px solid rgba(255,179,0,.06);font-size:14px;cursor:pointer;transition:.2s}.h-bar:hover{padding-left:12px;border-left:2px solid #ffb300}.h-bar .key{color:#ffb300;font-weight:600;width:140px;text-shadow:0 0 8px rgba(255,179,0,.1)}.h-bar .val{color:#d4c5a0;flex:1}.h-bar .pct{color:#a0824a;font-size:12px}.h-bar .glow{margin-left:auto;width:60px;height:4px;background:linear-gradient(90deg,transparent,#ffb300);border-radius:2px}
.cta{display:flex;justify-content:center;gap:32px;margin-top:40px;padding-top:32px;border-top:1px solid rgba(255,179,0,.1)}.cta span{color:#a0824a;font-size:12px;letter-spacing:2px;cursor:pointer;transition:.2s}.cta span:hover{color:#ffb300;text-shadow:0 0 15px rgba(255,179,0,.25)}
.glow-bg{position:fixed;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(255,179,0,.04) 0%,transparent 70%);top:20%;left:30%;pointer-events:none}
</style></head><body>
<div class="glow-bg"></div>
<div class="wrap"><span class="tag">✦ NEON NOIR</span>
<h1>Amber Protocol</h1>
<div class="sub">Real-time status board · 4 active channels</div>
<div class="h-bar"><span class="key">SIGNAL STRENGTH</span><span class="val">98%</span><div class="glow" style="width:98%"></div></div>
<div class="h-bar"><span class="key">DATA THROUGHPUT</span><span class="val">2.4 Gbps</span><div class="glow" style="width:74%"></div></div>
<div class="h-bar"><span class="key">NODE INTEGRITY</span><span class="val">100% — All clean</span><div class="glow" style="width:100%"></div></div>
<div class="h-bar"><span class="key">CHANNEL HEAT</span><span class="val">Nominal</span><div class="glow" style="width:45%"></div></div>
<div class="cta"><span>● VIEW LOGS</span><span>● ALERTS</span><span>● CONFIG</span></div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#00ff41;font-family:'JetBrains Mono',monospace;padding:32px;min-height:100vh;position:relative}
body::after{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,.03) 2px,rgba(0,255,65,.03) 4px);pointer-events:none}
.term{border:1px solid #00ff41;border-radius:8px;max-width:800px;margin:0 auto;overflow:hidden;box-shadow:0 0 40px rgba(0,255,65,.08)}
.term-head{background:rgba(0,255,65,.06);padding:12px 20px;border-bottom:1px solid #00ff41;display:flex;justify-content:space-between;font-size:11px;color:#00ff41;text-shadow:0 0 8px rgba(0,255,65,.3)}
.term-body{padding:24px}.line{display:flex;align-items:center;margin-bottom:8px;font-size:13px;white-space:nowrap}.prompt{color:#008f2a;margin-right:8px}.cmd{color:#00ff41;margin-right:12px;text-shadow:0 0 6px rgba(0,255,65,.15)}.result{color:#33ff77}.blink{animation:blink 1s step-end infinite}@keyframes blink{50%{opacity:0}}
.grid-m{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.m-cell{border:1px solid rgba(0,255,65,.15);border-radius:4px;padding:12px;font-size:11px;background:rgba(0,255,65,.02)}.m-cell .v{font-size:18px;font-weight:800;color:#00ff41;text-shadow:0 0 12px rgba(0,255,65,.12)}
</style></head><body>
<div class="term"><div class="term-head"><span>root@matrix:~ — TTY1</span><span>● ONLINE</span></div>
<div class="term-body">
<div class="line"><span class="prompt">$</span><span class="cmd">./pulse --scan</span></div>
<div class="line"><span class="result">>> 4 nodes · 12 processes · 0 threats</span></div>
<div class="line"><span class="prompt">$</span><span class="cmd">watch --live</span></div>
<div class="grid-m">
<div class="m-cell"><div class="v">256<span style="font-size:12px;color:#008f2a">MB/s</span></div><div>DMA Throughput</div></div>
<div class="m-cell"><div class="v">99.7<span style="font-size:12px;color:#008f2a">%</span></div><div>Kernel Efficiency</div></div>
<div class="m-cell"><div class="v">18<span style="font-size:12px;color:#008f2a">°C</span></div><div>Core Temp</div></div>
<div class="m-cell"><div class="v">OK</div><div>Integrity Check</div></div>
</div>
<div class="line" style="margin-top:12px"><span class="prompt">$</span><span class="cmd blink">▌</span></div>
</div></div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#f0f6ff;color:#1a1a2e;font-family:'Inter',sans-serif;min-height:100vh;padding:32px}
.top{display:flex;justify-content:space-between;align-items:center;max-width:1000px;margin:0 auto 32px}.top h1{font-size:20px;font-weight:700;color:#0066ff;letter-spacing:-.5px}.top nav a{color:#555;text-decoration:none;font-size:13px;margin-left:20px;font-weight:500;transition:.2s}.top nav a.active{color:#0066ff}
.cont{max-width:1000px;margin:0 auto}.hero{margin-bottom:36px}.hero h2{font-size:28px;font-weight:700;color:#1a1a2e;margin-bottom:4px}.hero p{color:#666;font-size:14px}
.w-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.w-card{background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,102,255,.06);border:1px solid #e0e8f0;transition:.2s}.w-card:hover{border-color:#0066ff;box-shadow:0 4px 24px rgba(0,102,255,.12)}.w-card .wv{font-size:24px;font-weight:700;color:#0066ff;margin-bottom:2px}.w-card .wl{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:600}.w-card .ws{font-size:11px;color:#00b4d8;margin-top:6px}
.section{background:#fff;border-radius:14px;padding:24px;box-shadow:0 2px 12px rgba(0,102,255,.04);border:1px solid #e0e8f0}.section h3{font-size:12px;color:#0066ff;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:16px}.s-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f0f4f8;font-size:13px;color:#444}.s-row .sv{color:#0066ff;font-weight:600}
.note{text-align:center;margin-top:24px;font-size:11px;color:#aaa;letter-spacing:1px}
</style></head><body>
<div class="top"><h1>BLUE ⚡</h1><nav><a href="#" class="active">Dashboard</a><a href="#">Analytics</a><a href="#">Team</a><a href="#">Settings</a></nav></div>
<div class="cont">
<div class="hero"><h2>Good morning, Alex</h2><p>Your workspace has 4 active projects</p></div>
<div class="w-grid">
<div class="w-card"><div class="wv">$48.2k</div><div class="wl">Revenue</div><div class="ws">▲ 8.2%</div></div>
<div class="w-card"><div class="wv">1,284</div><div class="wl">Users</div><div class="ws">▲ 24 new</div></div>
<div class="w-card"><div class="wv">92%</div><div class="wl">Retention</div><div class="ws">— steady</div></div>
<div class="w-card"><div class="wv">18</div><div class="wl">Open Tasks</div><div class="ws">▼ 3 done</div></div>
</div>
<div class="section"><h3>Recent Activity</h3><div class="s-row"><span>Deploy v2.4 to production</span><span class="sv">12 min ago</span></div><div class="s-row"><span>Database backup completed</span><span class="sv">47 min ago</span></div><div class="s-row"><span>New team member onboarded</span><span class="sv">2h ago</span></div></div>
<div class="note">● system nominal</div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0d0000;color:#f0d0d0;font-family:'Inter',sans-serif;min-height:100vh;overflow-x:hidden}
.bg-splat{position:fixed;top:-20%;right:-10%;width:600px;height:600px;background:radial-gradient(ellipse at center,rgba(220,20,60,.08) 0%,transparent 70%);pointer-events:none;transform:rotate(-15deg)}
header{display:flex;justify-content:space-between;align-items:center;padding:20px 40px;border-bottom:1px solid rgba(220,20,60,.1)}header h1{font-family:'Bebas Neue',sans-serif;font-size:32px;letter-spacing:6px;color:#ff0033;text-shadow:0 0 20px rgba(255,0,51,.15)}header nav a{color:#a04040;text-decoration:none;font-size:12px;font-weight:600;margin-left:28px;letter-spacing:2px;text-transform:uppercase;transition:.2s}header nav a.active{color:#ff0033}
.dash{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:32px 40px;max-width:1100px;margin:0 auto}
.col{display:flex;flex-direction:column;gap:20px}
.big-num{background:rgba(220,20,60,.03);border:1px solid rgba(220,20,60,.1);border-radius:4px;padding:28px;position:relative;overflow:hidden}.big-num::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:linear-gradient(180deg,#ff0033,transparent)}.big-num .v{font-family:'Bebas Neue',sans-serif;font-size:60px;line-height:1;color:#ff0033;letter-spacing:4px;text-shadow:0 0 30px rgba(255,0,51,.1)}.big-num .l{font-size:11px;color:#a04040;letter-spacing:3px;text-transform:uppercase;margin-top:4px}
.card-c{background:rgba(220,20,60,.02);border:1px solid rgba(220,20,60,.08);border-radius:4px;padding:20px;border-left:3px solid #ff0033}.card-c h4{font-family:'Bebas Neue',sans-serif;font-size:18px;color:#ff0033;letter-spacing:3px;margin-bottom:8px}.card-c p{font-size:12px;color:#b06060;line-height:1.6}
.tagline{grid-column:1/-1;text-align:right;font-size:10px;color:#600;letter-spacing:6px;text-transform:uppercase;border-top:1px solid rgba(220,20,60,.06);padding-top:16px}
</style></head><body>
<div class="bg-splat"></div>
<header><h1>CRIMSON</h1><nav><a href="#" class="active">Dashboard</a><a href="#">Threats</a><a href="#">Firewall</a><a href="#">Audit</a></nav></header>
<div class="dash">
<div class="col">
<div class="big-num"><div class="v">127</div><div class="l">Active Threats</div></div>
<div class="card-c"><h4>DISTRIBUTED SCAN</h4><p>12 nodes reporting anomalous traffic from 3 geographic regions. Mitigation running.</p></div>
</div>
<div class="col">
<div class="big-num"><div class="v">99.2<span style="font-size:28px">%</span></div><div class="l">Block Rate</div></div>
<div class="card-c"><h4>CRITICAL ALERT</h4><p>Port scan detected on gateway 7. Auto-block enacted. 4 attempts logged in 30s.</p></div>
</div>
<div class="tagline">● STORMWATCH v3.1 — ALL CLEAR</div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0f0b02;color:#e8dcc8;font-family:'Inter',sans-serif;min-height:100vh}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:16px 48px;border-bottom:1px solid rgba(255,215,0,.08);background:rgba(15,11,2,.8);backdrop-filter:blur(12px);position:sticky;top:0;z-index:10}
.topbar h1{font-family:'Playfair Display',serif;font-size:22px;color:#ffd700;letter-spacing:2px;text-shadow:0 0 20px rgba(255,215,0,.12)}
.topbar nav a{color:#8a7a50;text-decoration:none;font-size:12px;margin-left:28px;letter-spacing:2px;transition:.2s;font-weight:600}.topbar nav a.active{color:#ffd700}
.cont{max-width:1100px;margin:0 auto;padding:40px 48px}
.head{margin-bottom:40px}.head .kicker{font-size:10px;color:#8a7a50;letter-spacing:6px;text-transform:uppercase;margin-bottom:4px}.head h2{font-family:'Playfair Display',serif;font-size:34px;color:#ffd700;text-shadow:0 0 30px rgba(255,215,0,.08)}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.g-card-o{background:rgba(255,215,0,.02);border:1px solid rgba(255,215,0,.08);border-radius:2px;padding:24px;position:relative;transition:.3s;overflow:hidden}.g-card-o::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,#ffd700,transparent)}.g-card-o:hover{border-color:rgba(255,215,0,.2);background:rgba(255,215,0,.04)}.g-card-o .ov{font-family:'Playfair Display',serif;font-size:30px;color:#ffd700;margin-bottom:2px}.g-card-o .ol{font-size:10px;color:#8a7a50;letter-spacing:2px;text-transform:uppercase;font-weight:600}.g-card-o .os{font-size:11px;color:#b8a870;margin-top:8px}
.bottom-section{margin-top:28px;background:rgba(255,215,0,.01);border:1px solid rgba(255,215,0,.06);padding:20px 24px;border-radius:2px}.bottom-section h3{font-family:'Playfair Display',serif;font-size:14px;color:#ffd700;margin-bottom:12px;letter-spacing:1px}.gold-line{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,215,0,.04);font-size:12px;color:#a09060}
</style></head><body>
<div class="topbar"><h1>✦ SOLARA</h1><nav><a href="#" class="active">Dashboard</a><a href="#">Portfolio</a><a href="#">Markets</a><a href="#">Treasury</a></nav></div>
<div class="cont">
<div class="head"><div class="kicker">✦ Wealth Management</div><h2>Golden Ledger</h2></div>
<div class="g3">
<div class="g-card-o"><div class="ov">$842k</div><div class="ol">Total Value</div><div class="os">▲ 3.2% this month</div></div>
<div class="g-card-o"><div class="ov">18.4%</div><div class="ol">Yield</div><div class="os">Annualized return</div></div>
<div class="g-card-o"><div class="ov">32</div><div class="ol">Assets</div><div class="os">Across 4 portfolios</div></div>
</div>
<div class="bottom-section"><h3>Recent Transactions</h3><div class="gold-line"><span>USDC → ETH swap</span><span>+2,400 USDC</span></div><div class="gold-line"><span>Staking rewards</span><span>+0.42 ETH</span></div><div class="gold-line"><span>Bridge fee</span><span>-0.008 ETH</span></div></div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0a001a;color:#e0c0ff;font-family:'Unbounded',sans-serif;min-height:100vh;padding:32px}
.head-brut{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:48px}.head-brut h1{font-size:48px;font-weight:700;color:#ff00a0;line-height:.9;letter-spacing:-2px;text-shadow:0 0 40px rgba(255,0,160,.15)}.head-brut .badge-b{background:#ff00a0;color:#0a001a;padding:4px 12px;font-size:10px;letter-spacing:2px;font-weight:700}
.b-grid{display:grid;grid-template-columns:2fr 1fr;gap:20px}
.b-left{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-content:start}
.b-card{background:rgba(255,0,160,.02);border:2px solid rgba(255,0,160,.08);padding:24px;position:relative;transition:.2s;clip-path:polygon(0 0,100% 0,100% 85%,85% 100%,0 100%)}.b-card:hover{border-color:#ff00a0;background:rgba(255,0,160,.06)}.b-card .bv{font-size:34px;font-weight:700;color:#ff00a0;text-shadow:0 0 25px rgba(255,0,160,.1)}.b-card .bl{font-size:9px;color:#8a5a8a;letter-spacing:3px;text-transform:uppercase;margin-top:6px}.b-card .bs{font-size:10px;color:#bb70bb;margin-top:8px}
.b-right{background:rgba(255,0,160,.02);border:2px solid rgba(255,0,160,.06);padding:24px;clip-path:polygon(0 0,100% 0,100% 100%,10% 100%,0 90%)}.b-right h3{font-size:14px;color:#8a2be2;letter-spacing:3px;text-transform:uppercase;margin-bottom:16px}.b-item{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid rgba(255,0,160,.04);font-size:11px;color:#c0a0c0}.b-item .bi-v{color:#ff00a0;font-weight:600}
.footer-b{display:flex;gap:32px;margin-top:36px}.footer-b span{font-size:10px;color:#4a2a4a;letter-spacing:4px;text-transform:uppercase;cursor:pointer;transition:.2s}.footer-b span:hover{color:#8a2be2}
</style></head><body>
<div class="head-brut"><h1>NEON<br>PINK</h1><span class="badge-b">BRUTAL v2</span></div>
<div class="b-grid">
<div class="b-left">
<div class="b-card"><div class="bv">1,482</div><div class="bl">Views</div><div class="bs">▲ 32% spike</div></div>
<div class="b-card"><div class="bv">89%</div><div class="bl">Engagement</div><div class="bs">High affinity</div></div>
<div class="b-card"><div class="bv">42</div><div class="bl">Conversions</div><div class="bs">▼ 2 this week</div></div>
<div class="b-card"><div class="bv">$6.2k</div><div class="bl">Revenue</div><div class="bs">▲ 14% MoM</div></div>
</div>
<div class="b-right"><h3>Top Pages</h3><div class="b-item"><span>/onboarding</span><span class="bi-v">342</span></div><div class="b-item"><span>/pricing</span><span class="bi-v">218</span></div><div class="b-item"><span>/features</span><span class="bi-v">156</span></div><div class="b-item"><span>/blog</span><span class="bi-v">94</span></div></div>
</div>
<div class="footer-b"><span>● Analytics</span><span>● Reports</span><span>● Export</span></div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0a1628;color:#c0d8f0;font-family:'Nunito',sans-serif;min-height:100vh;display:grid;grid-template-columns:200px 1fr}
.side-frost{background:rgba(255,255,255,.02);border-right:1px solid rgba(0,212,255,.06);padding:28px 16px;backdrop-filter:blur(20px)}.side-frost h2{font-size:13px;color:#00d4ff;letter-spacing:4px;text-transform:uppercase;margin-bottom:32px;text-shadow:0 0 20px rgba(0,212,255,.15)}.side-frost a{display:block;padding:10px 12px;color:#708090;text-decoration:none;font-size:13px;border-radius:12px;margin-bottom:4px;font-weight:600}.side-frost a.active,.side-frost a:hover{background:rgba(0,212,255,.06);color:#00d4ff}
.chat-area{padding:32px 36px;position:relative}.chat-area::before{content:'';position:fixed;top:0;right:0;width:300px;height:300px;background:radial-gradient(circle,rgba(0,212,255,.03) 0%,transparent 70%);pointer-events:none}
.chat-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px}.chat-header h1{font-size:20px;font-weight:700;color:#e8f4ff}.chat-header .status{font-size:11px;color:#00d4ff;letter-spacing:2px;text-shadow:0 0 10px rgba(0,212,255,.1)}
.msg{display:grid;grid-template-columns:auto 1fr;gap:12px;margin-bottom:20px;align-items:start}.msg .av{width:36px;height:36px;border-radius:50%;border:1px solid rgba(0,212,255,.15);display:flex;align-items:center;justify-content:center;font-size:12px;color:#00d4ff;background:rgba(0,212,255,.04)}.msg .bubble{background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.08);border-radius:16px;padding:12px 16px;font-size:13px;line-height:1.5;backdrop-filter:blur(8px)}.msg .bubble .time{font-size:10px;color:#506880;margin-top:4px}.msg.in .bubble{border-radius:16px 16px 16px 4px}.msg.out .bubble{background:rgba(0,212,255,.04);border-color:rgba(0,212,255,.12);border-radius:16px 16px 4px 16px;text-align:right}.msg.out{grid-template-columns:1fr auto}
.input-bar{margin-top:24px;display:flex;gap:12px;background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.06);border-radius:16px;padding:12px 16px;backdrop-filter:blur(8px)}.input-bar span{color:#506880;font-size:13px;flex:1}.input-bar .btn{color:#00d4ff;font-size:12px;cursor:pointer}
</style></head><body>
<nav class="side-frost"><h2>❄ FROST</h2><a href="#" class="active">Chat</a><a href="#">Channels</a><a href="#">Files</a><a href="#">Contacts</a></nav>
<div class="chat-area">
<div class="chat-header"><h1>Arctic Chat</h1><span class="status">● 4 online</span></div>
<div class="msg in"><div class="av">A</div><div class="bubble"><strong style="color:#00d4ff">Agent Alpha:</strong> Cluster sync complete. All nodes nominal.<div class="time">2 min ago</div></div></div>
<div class="msg out"><div class="bubble">Copy that. Deploying v3.1 patch now.<div class="time">1 min ago</div></div><div class="av" style="border-color:rgba(255,255,255,.1);color:#e8f4ff">U</div></div>
<div class="msg in"><div class="av">A</div><div class="bubble"><strong style="color:#00d4ff">Agent Alpha:</strong> Patch received. Rebooting gateway 4.<div class="time">30s ago</div></div></div>
<div class="input-bar"><span>Type a message...</span><span class="btn">❄ Send</span></div>
</div>
</body></html>
```
```html
<!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0d0d0d;color:#e0e0e0;font-family:'Outfit',sans-serif;min-height:100vh;overflow-x:hidden;position:relative}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg,rgba(0,229,255,.04) 0%,transparent 50%,rgba(255,102,0,.04) 100%);pointer-events:none;z-index:0}
.content{position:relative;z-index:1;max-width:1000px;margin:0 auto;padding:40px 48px}
.top-duo{display:flex;justify-content:space-between;align-items:center;margin-bottom:48px;padding-bottom:24px;border-bottom:1px solid rgba(255,255,255,.04)}
.top-duo h1{font-size:24px;font-weight:700;background:linear-gradient(135deg,#00e5ff,#ff6600);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:1px}.top-duo nav a{color:#666;text-decoration:none;font-size:12px;margin-left:24px;letter-spacing:2px;text-transform:uppercase;transition:.2s}.top-duo nav a.active{color:#00e5ff;text-shadow:0 0 12px rgba(0,229,255,.12);border-bottom:2px solid #00e5ff;padding-bottom:4px}
.diag-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px}
.d-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:16px;padding:24px;position:relative;overflow:hidden;transition:.2s}.d-card:hover{transform:translateY(-1px)}.d-card.c-cyan{border-left:3px solid #00e5ff}.d-card.c-orange{border-left:3px solid #ff6600}.d-card .dv{font-size:28px;font-weight:700}.d-card .dv.c{color:#00e5ff;text-shadow:0 0 20px rgba(0,229,255,.1)}.d-card .dv.o{color:#ff6600;text-shadow:0 0 20px rgba(255,102,0,.1)}.d-card .dl{font-size:10px;color:#666;letter-spacing:2px;text-transform:uppercase;margin-top:4px}
.split-bar{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.split-panel{background:rgba(255,255,255,.01);border:1px solid rgba(255,255,255,.03);border-radius:16px;padding:20px}.split-panel h3{font-size:11px;letter-spacing:3px;text-transform:uppercase;margin-bottom:16px;font-weight:600}.split-panel.cyan h3{color:#00e5ff;text-shadow:0 0 10px rgba(0,229,255,.08)}.split-panel.orange h3{color:#ff6600;text-shadow:0 0 10px rgba(255,102,0,.08)}.split-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:12px;color:#999}.split-row .sr-v.cyan{color:#00e5ff}.split-row .sr-v.orange{color:#ff6600}
</style></head><body>
<div class="content">
<div class="top-duo"><h1>✦ DUALITY</h1><nav><a href="#" class="active">Dashboard</a><a href="#">Networks</a><a href="#">Bridges</a><a href="#">Peers</a></nav></div>
<div class="diag-grid">
<div class="d-card c-cyan"><div class="dv c">4,201</div><div class="dl">Cyan Channel — Inbound</div></div>
<div class="d-card c-orange"><div class="dv o">3,847</div><div class="dl">Orange Channel — Outbound</div></div>
</div>
<div class="split-bar">
<div class="split-panel cyan"><h3>● Cyan Metrics</h3><div class="split-row"><span>Bandwidth</span><span class="sr-v cyan">2.4 Gbps</span></div><div class="split-row"><span>Latency</span><span class="sr-v cyan">12 ms</span></div><div class="split-row"><span>Packets</span><span class="sr-v cyan">841K</span></div></div>
<div class="split-panel orange"><h3>● Orange Metrics</h3><div class="split-row"><span>Bandwidth</span><span class="sr-v orange">1.8 Gbps</span></div><div class="split-row"><span>Latency</span><span class="sr-v orange">8 ms</span></div><div class="split-row"><span>Packets</span><span class="sr-v orange">623K</span></div></div>
</div>
</div>
</body></html>
```
TRUNCATION SELF-CHECK: All 10 HTML documents are complete — each opens with `<!DOCTYPE html><html>` and closes with `</body></html>`. No mid-tag cuts, no missing closing brackets. Count: 10/10 prototypes delivered inline.