```yaml
file: slo-dashboard.html
type: interactive-html-dashboard
size: ~650 lines
features:
  - error-budget-gauge: true
  - latency-sparklines: true
  - error-heatmap: true
  - dependency-tree: true
  - slo-definitions: true
  - incident-timeline: true
  - deterministic-mock-data: true
  - css-variable-tokens: true
  - fixture-json-stub: true
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Real-Time SLO Dashboard</title>
<style>
:root {
  --bg-surface: #0f1117;
  --bg-card: #1a1d27;
  --bg-card-hover: #22263a;
  --bg-input: #1e2235;
  --border: #2a2e42;
  --border-active: #3b82f6;
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --green: #22c55e;
  --green-bg: rgba(34,197,94,0.12);
  --yellow: #eab308;
  --yellow-bg: rgba(234,179,8,0.12);
  --red: #ef4444;
  --red-bg: rgba(239,68,68,0.12);
  --blue: #3b82f6;
  --blue-bg: rgba(59,130,246,0.10);
  --purple: #a855f7;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
  --font: 'Segoe UI','Inter',system-ui,-apple-system,sans-serif;
  --mono: 'Cascadia Code','JetBrains Mono','Fira Code',monospace;
  --transition: 0.2s ease;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg-surface); color: var(--text-primary); font-family: var(--font); padding: 20px; min-height: 100vh; }
.dashboard { max-width: 1440px; margin: 0 auto; display: grid; grid-template-columns: 300px 1fr 1fr; gap: 16px; }
h2 { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-muted); margin-bottom: 12px; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px; box-shadow: var(--shadow); }
.card:hover { border-color: var(--border-active); transition: var(--transition); }
.full-width { grid-column: 1 / -1; }
.half-width { grid-column: span 2; }
/* Header */
.header { grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: center; padding: 0 4px 8px 4px; }
.header h1 { font-size: 22px; font-weight: 700; color: var(--text-primary); }
.header .status { display: flex; gap: 16px; align-items: center; }
.header .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.status-badge.ok { background: var(--green-bg); color: var(--green); }
.status-badge.warn { background: var(--yellow-bg); color: var(--yellow); }
/* Gauge */
.gauge-container { display: flex; flex-direction: column; align-items: center; padding: 8px 0; }
.gauge-svg { width: 200px; height: 130px; }
.gauge-value { font-size: 36px; font-weight: 700; font-family: var(--mono); margin-top: -20px; }
.gauge-label { font-size: 13px; color: var(--text-secondary); }
.gauge-meta { display: flex; gap: 24px; margin-top: 12px; font-size: 12px; color: var(--text-secondary); }
.gauge-meta span { display: flex; flex-direction: column; align-items: center; }
.gauge-meta .num { font-weight: 600; color: var(--text-primary); font-family: var(--mono); font-size: 14px; }
/* Latency sparklines */
.latency-grid { display: flex; flex-direction: column; gap: 12px; }
.latency-row { display: grid; grid-template-columns: 80px 1fr 100px; align-items: center; gap: 12px; }
.latency-label { font-size: 12px; font-weight: 500; color: var(--text-secondary); }
.latency-chart { height: 40px; position: relative; }
.latency-chart svg { width: 100%; height: 100%; }
.latency-stat { font-size: 12px; font-family: var(--mono); text-align: right; }
.latency-stat .p50 { color: var(--green); }
.latency-stat .p95 { color: var(--yellow); }
.latency-stat .p99 { color: var(--red); }
.slo-threshold { position: absolute; left: 0; right: 0; border-top: 1px dashed var(--red); top: 20%; opacity: 0.5; }
/* Heatmap */
.heatmap-grid { display: grid; grid-template-columns: repeat(24,1fr); gap: 2px; margin-top: 8px; }
.heatmap-cell { aspect-ratio: 1; border-radius: 2px; cursor: pointer; position: relative; min-width: 14px; }
.heatmap-cell:hover { transform: scale(1.3); z-index: 10; }
.heatmap-cell[data-severity="0"] { background: var(--bg-input); }
.heatmap-cell[data-severity="1"] { background: #166534; }
.heatmap-cell[data-severity="2"] { background: #854d0e; }
.heatmap-cell[data-severity="3"] { background: #991b1b; }
.heatmap-cell[data-severity="4"] { background: #7c1d6e; }
.heatmap-preview { display: none; position: absolute; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 8px; font-size: 11px; z-index: 100; white-space: nowrap; pointer-events: none; box-shadow: var(--shadow); }
.heatmap-cell:hover .heatmap-preview { display: block; }
.heatmap-legend { display: flex; gap: 8px; align-items: center; margin-top: 8px; font-size: 11px; color: var(--text-secondary); }
.heatmap-legend .swatch { width: 12px; height: 12px; border-radius: 2px; }
/* Dependency tree */
.tree ul { list-style: none; padding-left: 20px; }
.tree li { position: relative; padding: 4px 0 4px 12px; }
.tree li::before { content: ''; position: absolute; left: 0; top: 0; bottom: 50%; width: 12px; border-left: 1.5px solid var(--border); border-bottom: 1.5px solid var(--border); }
.tree li:last-child::before { bottom: auto; height: 50%; }
.tree li::after { content: ''; position: absolute; left: 0; top: 50%; width: 12px; border-bottom: 1.5px solid var(--border); }
.tree > li::before, .tree > li::after { display: none; }
.tree .node { display: inline-flex; align-items: center; gap: 8px; padding: 4px 10px; border-radius: var(--radius-sm); font-size: 12px; cursor: pointer; transition: var(--transition); }
.tree .node:hover { background: var(--bg-card-hover); }
.tree .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot.green { background: var(--green); }
.dot.yellow { background: var(--yellow); }
.dot.red { background: var(--red); }
.dot.purple { background: var(--purple); }
.tree .node .cascade { font-size: 10px; color: var(--red); margin-left: 4px; }
/* SLO table */
.slo-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.slo-table th { text-align: left; padding: 6px 8px; color: var(--text-muted); font-weight: 500; border-bottom: 1px solid var(--border); }
.slo-table td { padding: 6px 8px; border-bottom: 1px solid var(--border); }
.slo-table tr:last-child td { border-bottom: none; }
.slo-table .progress { height: 4px; border-radius: 2px; background: var(--bg-input); width: 80px; display: inline-block; vertical-align: middle; margin-right: 6px; }
.slo-table .progress-bar { height: 100%; border-radius: 2px; }
/* Incident timeline */
.incident-timeline { position: relative; padding: 8px 0; }
.incident-timeline::before { content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: var(--border); }
.incident-item { position: relative; padding: 8px 0 8px 28px; }
.incident-item::before { content: ''; position: absolute; left: 3px; top: 12px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid; background: var(--bg-card); }
.incident-item.resolved::before { border-color: var(--green); }
.incident-item.active::before { border-color: var(--red); background: var(--red-bg); }
.incident-item.mitigated::before { border-color: var(--yellow); background: var(--yellow-bg); }
.incident-time { font-size: 11px; color: var(--text-muted); }
.incident-title { font-size: 13px; font-weight: 500; }
.incident-desc { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
/* SLO burndown overlay svg area */
.burndown-area { margin-top: 8px; height: 60px; position: relative; }
.burndown-area svg { width: 100%; height: 100%; }
/* Controls */
.controls { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
.controls select, .controls button { background: var(--bg-input); border: 1px solid var(--border); color: var(--text-primary); padding: 6px 12px; border-radius: var(--radius-sm); font-size: 12px; cursor: pointer; }
.controls select:hover, .controls button:hover { border-color: var(--border-active); }
/* Drill-down modal */
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }
.modal-overlay.open { display: flex; }
.modal { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 24px; max-width: 500px; width: 90%; max-height: 70vh; overflow-y: auto; }
.modal h3 { font-size: 16px; margin-bottom: 12px; }
.modal .close-btn { float: right; background: none; border: none; color: var(--text-muted); font-size: 18px; cursor: pointer; }
.modal .close-btn:hover { color: var(--text-primary); }
.modal table { width: 100%; font-size: 12px; }
.modal table td { padding: 6px 4px; border-bottom: 1px solid var(--border); }
/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
</head>
<body>
<div class="dashboard">
<div class="header">
  <h1>SLO Dashboard</h1>
  <div class="status">
    <select id="serviceSelect" onchange="switchService(this.value)">
      <option value="api-gateway">api-gateway</option>
      <option value="user-service">user-service</option>
      <option value="payment-service">payment-service</option>
      <option value="search-service">search-service</option>
      <option value="notification-service">notification-service</option>
    </select>
    <select id="windowSelect" onchange="switchWindow(this.value)">
      <option value="24h">24h</option>
      <option value="7d" selected>7d</option>
      <option value="30d">30d</option>
    </select>
    <span class="status-badge ok" id="globalStatusBadge">HEALTHY</span>
  </div>
</div>
<div class="card">
  <h2>Error Budget</h2>
  <div class="gauge-container" id="gaugeContainer">
    <svg class="gauge-svg" viewBox="0 0 200 130" id="gaugeSvg">
      <path id="gaugeArcBg" d="M 20 110 A 80 80 0 1 1 180 110" fill="none" stroke="var(--bg-input)" stroke-width="14" stroke-linecap="round"/>
      <path id="gaugeArc" d="M 20 110 A 80 80 0 1 1 180 110" fill="none" stroke="var(--green)" stroke-width="14" stroke-linecap="round" stroke-dasharray="377 377" stroke-dashoffset="0"/>
      <text id="gaugeCenterText" x="100" y="100" text-anchor="middle" font-size="28" font-weight="700" fill="var(--text-primary)" font-family="var(--mono)">92.4%</text>
      <text x="100" y="120" text-anchor="middle" font-size="11" fill="var(--text-muted)">remaining</text>
    </svg>
    <div class="gauge-meta">
      <span>Burn Rate <span class="num" id="burnRate">0.8x</span></span>
      <span>Budget Used <span class="num" id="budgetUsed">7.6%</span></span>
      <span>ETA Exhaust <span class="num" id="etaExhaust">34d</span></span>
    </div>
  </div>
</div>
<div class="card half-width">
  <h2>Latency (p50 / p95 / p99)</h2>
  <div class="latency-grid" id="latencyGrid"></div>
</div>
<div class="card">
  <h2>Error Heatmap</h2>
  <div style="display:flex; gap:6px; font-size:11px; color:var(--text-muted); margin-bottom:6px;">
    <span>Last 24h &middot; hover for details</span>
  </div>
  <div class="heatmap-grid" id="heatmapGrid"></div>
  <div class="heatmap-legend">
    <span>none</span>
    <span class="swatch" style="background:#166534;"></span>
    <span class="swatch" style="background:#854d0e;"></span>
    <span class="swatch" style="background:#991b1b;"></span>
    <span class="swatch" style="background:#7c1d6e;"></span>
    <span>critical</span>
  </div>
</div>
<div class="card">
  <h2>Dependency Health</h2>
  <div class="tree" id="dependencyTree"></div>
</div>
<div class="card half-width">
  <h2>SLO Definitions</h2>
  <table class="slo-table" id="sloTable">
    <thead>
      <tr><th>Service</th><th>Window</th><th>Target</th><th>Current</th><th>Budget</th></tr>
    </thead>
    <tbody id="sloTableBody"></tbody>
  </table>
</div>
<div class="card">
  <h2>Incidents</h2>
  <div class="incident-timeline" id="incidentTimeline"></div>
  <div class="burndown-area" id="burndownArea">
    <svg viewBox="0 0 400 60" id="burndownSvg">
      <line x1="0" y1="6" x2="400" y2="6" stroke="var(--border)" stroke-width="1" stroke-dasharray="4 4"/>
      <line x1="0" y1="30" x2="400" y2="30" stroke="var(--green)" stroke-width="1" opacity="0.3"/>
      <line x1="0" y1="54" x2="400" y2="54" stroke="var(--red)" stroke-width="1" opacity="0.3"/>
    </svg>
  </div>
</div>
</div>
<div class="modal-overlay" id="drillModal">
  <div class="modal">
    <button class="close-btn" onclick="closeDrillModal()">&times;</button>
    <h3 id="drillModalTitle">Error Details</h3>
    <table><tbody id="drillModalBody"></tbody></table>
  </div>
</div>
<script>
(function(){
const SEED = 42;
let seedState = SEED;
function seededRandom() {
  seedState = (seedState * 1664525 + 1013904223) & 0x7fffffff;
  return (seedState & 0x7fffffff) / 0x7fffffff;
}
function reseed() { seedState = SEED; }
function randInt(min, max) { return Math.floor(seededRandom() * (max - min + 1)) + min; }
function randFloat(min, max) { return seededRandom() * (max - min) + min; }
const SERVICES = ['api-gateway','user-service','payment-service','search-service','notification-service'];
const WINDOWS = ['24h','7d','30d'];
const WINDOW_HOURS = { '24h':24, '7d':168, '30d':720 };
function generateSLOData() {
  reseed();
  const data = {};
  for (const svc of SERVICES) {
    data[svc] = {};
    for (const win of WINDOWS) {
      const target = randFloat(98.0, 99.99);
      const attainment = target - randFloat(0.1, 2.5);
      const budget = ((attainment - (target - 100)) / (target - (target - 100))) * 100;
      data[svc][win] = { target:+target.toFixed(2), attainment:+attainment.toFixed(2), budget:+Math.max(0,budget).toFixed(1) };
    }
  }
  return data;
}
function generateLatencyData(service, window) {
  reseed();
  const hours = WINDOW_HOURS[window];
  const points = Math.min(hours, 168);
  const base = SERVICES.indexOf(service) * 5 + 20;
  const d = [];
  for (let i = 0; i < points; i++) {
    const t = i / points;
    const noise = randFloat(-3, 3) + Math.sin(t * Math.PI * 4) * 2;
    const spike = seededRandom() > 0.92 ? randFloat(10, 40) : 0;
    d.push({
      p50: +Math.max(1, base + noise + spike * 0.2).toFixed(1),
      p95: +Math.max(2, base * 1.8 + noise * 2 + spike * 0.8).toFixed(1),
      p99: +Math.max(3, base * 3.2 + noise * 3 + spike * 2.5).toFixed(1)
    });
  }
  return d;
}
function generateHeatmapData(service, window) {
  reseed();
  const hours = WINDOW_HOURS[window];
  const cols = Math.min(hours, 72);
  const rows = 7;
  const grid = [];
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < cols; c++) {
      const baseProb = 0.05 + (r / rows) * 0.3;
      const severity = seededRandom() < baseProb ? randInt(1, 4) : 0;
      row.push(severity);
    }
    grid.push(row);
  }
  return { grid, rows, cols, hours };
}
function generateTreeData() {
  const deps = {
    'api-gateway': ['user-service','payment-service','search-service','notification-service','auth-service'],
    'user-service': ['db-primary','cache-redis'],
    'payment-service': ['payment-processor','fraud-check','db-primary'],
    'search-service': ['search-index','db-replica','cache-redis'],
    'notification-service': ['email-relay','push-gateway','sms-gateway'],
    'auth-service': ['db-primary','cache-redis','sso-provider'],
    'db-primary': [],
    'db-replica': ['db-primary'],
    'cache-redis': [],
    'payment-processor': [],
    'fraud-check': ['ml-scoring'],
    'ml-scoring': [],
    'search-index': [],
    'email-relay': [],
    'push-gateway': [],
    'sms-gateway': [],
    'sso-provider': []
  };
  reseed();
  const health = {};
  for (const k of Object.keys(deps)) {
    const r = seededRandom();
    health[k] = r < 0.70 ? 'green' : r < 0.88 ? 'yellow' : 'red';
  }
  health['auth-service'] = 'red';
  health['db-primary'] = 'yellow';
  return { deps, health };
}
function generateIncidents(service) {
  reseed();
  // consume some seed based on service
  for (let i = 0; i < SERVICES.indexOf(service); i++) seededRandom();
  const count = randInt(2, 5);
  const incidents = [];
  const now = Date.now();
  for (let i = 0; i < count; i++) {
    const daysAgo = randInt(0, 14);
    const hoursAgo = randInt(0, 23);
    const ts = now - (daysAgo * 86400000 + hoursAgo * 3600000 + randInt(0, 59) * 60000);
    const labels = ['degraded performance','partial outage','latency spike','connection errors','timeout burst','high error rate','upstream failure','SSL handshake failures','DB connection pool exhaustion'];
    const statuses = ['resolved','resolved','resolved','resolved','active','mitigated','resolved','resolved','resolved'];
    const idx = randInt(0, labels.length - 1);
    const duration = randInt(10, 180);
    incidents.push({
      time: new Date(ts).toISOString(),
      label: labels[idx],
      status: statuses[idx % statuses.length],
      duration: duration + 'min',
      desc: service + ' ' + labels[idx] + ' affecting ' + randInt(200, 5000) + ' requests'
    });
  }
  return incidents.sort((a,b) => new Date(b.time) - new Date(a.time));
}
function generateDetailedErrors(service, hour, severity) {
  reseed();
  for (let i = 0; i < SERVICES.indexOf(service) * 7 + hour * 3 + severity; i++) seededRandom();
  const count = randInt(3, 12);
  const errors = [];
  const codes = [400,401,403,404,429,500,502,503,504];
  const messages = ['timeout','bad request','unauthorized','not found','rate limited','internal error','bad gateway','service unavailable','gateway timeout'];
  for (let i = 0; i < count; i++) {
    const idx = randInt(0, codes.length - 1);
    errors.push({ code: codes[idx], message: messages[idx], count: randInt(1, 50), source: service });
  }
  return errors;
}
const sloData = generateSLOData();
let currentService = 'api-gateway';
let currentWindow = '7d';
function switchService(svc) { currentService = svc; renderAll(); }
function switchWindow(w) { currentWindow = w; renderAll(); }
function renderAll() {
  renderGauge();
  renderLatency();
  renderHeatmap();
  renderTree();
  renderSLOTable();
  renderIncidents();
}
function renderGauge() {
  const d = sloData[currentService][currentWindow];
  const budget = d.budget;
  const attainment = d.attainment;
  const target = d.target;
  const arcLen = 377;
  const offset = arcLen * (1 - budget / 100);
  const arc = document.getElementById('gaugeArc');
  const color = budget > 80 ? 'var(--green)' : budget > 40 ? 'var(--yellow)' : 'var(--red)';
  arc.setAttribute('stroke', color);
  arc.setAttribute('stroke-dashoffset', Math.max(0, offset));
  document.getElementById('gaugeCenterText').textContent = budget.toFixed(1) + '%';
  const burnRate = +((100 - budget) / 100 * randFloat(0.5, 1.5)).toFixed(1);
  document.getElementById('burnRate').textContent = burnRate + 'x';
  document.getElementById('budgetUsed').textContent = (100 - budget).toFixed(1) + '%';
  const eta = budget > 50 ? randInt(20, 60) : budget > 20 ? randInt(5, 19) : randInt(1, 4);
  document.getElementById('etaExhaust').textContent = eta + 'd';
  const badge = document.getElementById('globalStatusBadge');
  if (budget > 80) { badge.textContent = 'HEALTHY'; badge.className = 'status-badge ok'; }
  else if (budget > 40) { badge.textContent = 'WARNING'; badge.className = 'status-badge warn'; }
  else { badge.textContent = 'CRITICAL'; badge.className = 'status-badge'; badge.style.background = 'var(--red-bg)'; badge.style.color = 'var(--red)'; }
}
function renderLatency() {
  const data = generateLatencyData(currentService, currentWindow);
  const grid = document.getElementById('latencyGrid');
  grid.innerHTML = '';
  const maxVal = Math.max(...data.map(d=>d.p99)) * 1.15;
  const sloLine = maxVal * 0.8;
  const stats = ['p50','p95','p99'];
  const colors = ['var(--green)','var(--yellow)','var(--red)'];
  for (const p of stats) {
    const vals = data.map(d=>d[p]);
    const avg = (vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(1);
    const row = document.createElement('div');
    row.className = 'latency-row';
    const label = document.createElement('div');
    label.className = 'latency-label';
    label.textContent = p.toUpperCase();
    const chart = document.createElement('div');
    chart.className = 'latency-chart';
    const w = data.length;
    const h = 40;
    const pad = 2;
    const pts = data.map((d,i)=>{
      const x = pad + (i/(w-1||1))*(100-pad*2);
      const y = h - 4 - ((d[p]-0)/(maxVal-0||1))*(h-8);
      return x+','+y;
    }).join(' ');
    chart.innerHTML = '<svg viewBox="0 0 100 40"><polyline points="'+pts+'" fill="none" stroke="'+colors[stats.indexOf(p)]+'" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="0" y1="'+((h-4-((sloLine-0)/(maxVal-0||1))*(h-8))/40*100).toFixed(0)+'" x2="100" y2="'+((h-4-((sloLine-0)/(maxVal-0||1))*(h-8))/40*100).toFixed(0)+'" stroke="var(--red)" stroke-width="0.5" stroke-dasharray="3 3" opacity="0.4"/></svg>';
    const stat = document.createElement('div');
    stat.className = 'latency-stat';
    stat.innerHTML = '<span class="'+p+'">'+avg+' ms</span> <span style="color:var(--text-muted);font-size:10px;">avg</span>';
    row.appendChild(label);
    row.appendChild(chart);
    row.appendChild(stat);
    grid.appendChild(row);
  }
}
function renderHeatmap() {
  const data = generateHeatmapData(currentService, currentWindow);
  const grid = document.getElementById('heatmapGrid');
  grid.innerHTML = '';
  grid.style.gridTemplateColumns = 'repeat('+data.cols+',1fr)';
  for (let r = 0; r < data.rows; r++) {
    for (let c = 0; c < data.cols; c++) {
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      const sev = data.grid[r][c];
      cell.setAttribute('data-severity', sev);
      const preview = document.createElement('div');
      preview.className = 'heatmap-preview';
      const sevLabel = ['none','low','medium','high','critical'][sev] || 'none';
      const hourLabel = 'h-'+((data.hours/data.cols)*c).toFixed(0);
      const sevName = ['ok','warning','error','high','critical'][sev];
      preview.innerHTML = '<b>'+sevName.toUpperCase()+'</b><br>'+hourLabel+' &middot; row '+(r+1)+'<br>click to drill';
      cell.appendChild(preview);
      cell.addEventListener('click', function(){
        openDrill(currentService, c, sev);
      });
      grid.appendChild(cell);
    }
  }
}
function renderTree() {
  const data = generateTreeData();
  const container = document.getElementById('dependencyTree');
  container.innerHTML = '';
  function buildNode(name, deps, health, depth) {
    const li = document.createElement('li');
    const node = document.createElement('div');
    node.className = 'node';
    const dot = document.createElement('span');
    dot.className = 'dot ' + (health[name]||'green');
    node.appendChild(dot);
    node.appendChild(document.createTextNode(name));
    if (health['auth-service'] === 'red' && name !== 'auth-service' && deps[name] && deps[name].includes('auth-service')) {
      const flag = document.createElement('span');
      flag.className = 'cascade';
      flag.textContent = '!! UPSTREAM FAILURE';
      node.appendChild(flag);
    }
    if (health['db-primary'] === 'yellow' && deps[name] && deps[name].includes('db-primary')) {
      const flag = document.createElement('span');
      flag.className = 'cascade';
      flag.textContent = '! DB DEGRADED';
      node.appendChild(flag);
    }
    li.appendChild(node);
    if (deps[name] && deps[name].length > 0) {
      const ul = document.createElement('ul');
      for (const child of deps[name]) {
        ul.appendChild(buildNode(child, deps, health, depth+1));
      }
      li.appendChild(ul);
    }
    return li;
  }
  const ul = document.createElement('ul');
  ul.appendChild(buildNode(currentService, data.deps, data.health, 0));
  container.appendChild(ul);
}
function renderSLOTable() {
  const tbody = document.getElementById('sloTableBody');
  tbody.innerHTML = '';
  for (const svc of SERVICES) {
    const win = currentWindow;
    const d = sloData[svc][win];
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>'+svc+'</td><td>'+win+'</td><td>'+d.target+'%</td><td>'+d.attainment+'%</td><td><div class="progress"><div class="progress-bar" style="width:'+d.budget+'%;background:'+(d.budget>80?'var(--green)':d.budget>40?'var(--yellow)':'var(--red)')+';"></div></div>'+d.budget+'%</td>';
    if (svc === currentService) tr.style.background = 'var(--blue-bg)';
    tbody.appendChild(tr);
  }
}
function renderIncidents() {
  const data = generateIncidents(currentService);
  const tl = document.getElementById('incidentTimeline');
  tl.innerHTML = '';
  for (const inc of data) {
    const div = document.createElement('div');
    div.className = 'incident-item ' + inc.status;
    const dt = new Date(inc.time);
    const timeStr = dt.toLocaleDateString('en-US',{month:'short',day:'numeric'})+' '+dt.toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'});
    div.innerHTML = '<div class="incident-time">'+timeStr+' &middot; '+inc.duration+'</div><div class="incident-title">'+inc.label+'</div><div class="incident-desc">'+inc.desc+'</div>';
    tl.appendChild(div);
  }
  // burndown overlay
  const svg = document.getElementById('burndownSvg');
  let burndownHtml = '<line x1="0" y1="6" x2="400" y2="6" stroke="var(--border)" stroke-width="1" stroke-dasharray="4 4"/>';
  burndownHtml += '<line x1="0" y1="30" x2="400" y2="30" stroke="var(--green)" stroke-width="1" opacity="0.3"/>';
  burndownHtml += '<line x1="0" y1="54" x2="400" y2="54" stroke="var(--red)" stroke-width="1" opacity="0.3"/>';
  // plot SLO burndown
  const budget = sloData[currentService][currentWindow].budget;
  const pts = [];
  for (let i = 0; i < data.length; i++) {
    const pct = (i / Math.max(data.length-1,1));
    const x = 20 + pct * 360;
    const y = 6 + (1 - budget/100) * 48;
    pts.push(x+','+y);
    // incident markers
    burndownHtml += '<circle cx="'+x+'" cy="'+y+'" r="4" fill="'+(data[i].status==='resolved'?'var(--green)':'var(--red)')+'" stroke="var(--bg-card)" stroke-width="2"><title>'+data[i].label+'</title></circle>';
  }
  if (pts.length >= 2) {
    burndownHtml += '<polyline points="'+pts.join(' ')+'" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.7"/>';
  }
  svg.innerHTML = burndownHtml;
}
function openDrill(service, hourCol, severity) {
  if (severity === 0) return;
  const modal = document.getElementById('drillModal');
  modal.classList.add('open');
  document.getElementById('drillModalTitle').textContent = service + ' errors (hour~' + hourCol + ', severity=' + severity + ')';
  const errors = generateDetailedErrors(service, hourCol, severity);
  const tbody = document.getElementById('drillModalBody');
  tbody.innerHTML = '';
  for (const e of errors) {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>'+e.code+'</td><td>'+e.message+'</td><td>'+e.count+'</td><td>'+e.source+'</td>';
    tbody.appendChild(tr);
  }
}
function closeDrillModal() {
  document.getElementById('drillModal').classList.remove('open');
}
document.getElementById('drillModal').addEventListener('click', function(e) {
  if (e.target === this) closeDrillModal();
});
renderAll();
window.switchService = switchService;
window.switchWindow = switchWindow;
window.openDrill = openDrill;
window.closeDrillModal = closeDrillModal;
})();
</script>
</body>
</html>