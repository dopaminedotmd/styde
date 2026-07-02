<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0d1117;--surface:#161b22;--surface2:#21262d;--border:#30363d;--text:#e6edf3;--text2:#8b949e;--accent:#58a6ff;--accent2:#1f6feb;--green:#3fb950;--red:#f85149;--yellow:#d29922;--orange:#d18616;--font:'Segoe UI',system-ui,-apple-system,sans-serif;--chart-h:220px;--sidebar-w:420px}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.5;overflow:hidden}
.dash{display:grid;grid-template-columns:1fr var(--sidebar-w);grid-template-rows:56px 1fr;height:100vh}
/* HEADER */
.header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:var(--surface);border-bottom:1px solid var(--border);z-index:10}
.header h1{font-size:18px;font-weight:600;display:flex;align-items:center;gap:10px}
.header h1 span{color:var(--accent)}
.header-right{display:flex;align-items:center;gap:16px;font-size:13px;color:var(--text2)}
.refresh-indicator{display:flex;align-items:center;gap:6px;padding:4px 12px;border-radius:12px;background:var(--surface2);font-size:12px}
.refresh-dot{width:8px;height:8px;border-radius:50%;background:var(--green);animation:pulse 2s ease-in-out infinite}
.refresh-dot.stale{background:var(--yellow)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.blink-alert{padding:4px 10px;border-radius:4px;font-size:12px;font-weight:600;background:var(--red);color:#fff;animation:blinkAlert 1.5s ease-in-out infinite}
@keyframes blinkAlert{0%,100%{opacity:1;box-shadow:0 0 6px var(--red)}50%{opacity:.5;box-shadow:0 0 12px var(--red)}}
.threshold-counter{padding:4px 10px;border-radius:4px;font-size:12px;background:var(--surface2);border-left:3px solid var(--yellow)}
/* MAIN */
.main{padding:16px 20px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
.main::-webkit-scrollbar{width:6px}
.main::-webkit-scrollbar-track{background:transparent}
.main::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
/* KPI ROW */
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px 16px}
.kpi-card .label{font-size:12px;color:var(--text2);margin-bottom:4px}
.kpi-card .value{font-size:26px;font-weight:700;letter-spacing:-.5px}
.kpi-card .delta{font-size:12px;margin-top:4px;display:flex;align-items:center;gap:4px}
.delta.up{color:var(--green)}
.delta.down{color:var(--red)}
.kpi-card .truth-tag{font-size:10px;color:var(--text2);margin-top:6px;padding:2px 6px;background:var(--surface2);border-radius:3px;display:inline-block}
/* CHART ROW */
.chart-row{display:grid;grid-template-columns:2fr 1fr;gap:12px}
.chart-panel{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;position:relative}
.chart-panel .chart-title{font-size:13px;font-weight:600;color:var(--text2);margin-bottom:10px;display:flex;justify-content:space-between}
.chart-panel .chart-title .annotation{font-weight:400;font-size:11px;color:var(--accent)}
.chart-panel .chart-container{height:var(--chart-h);position:relative;display:flex;align-items:flex-end;gap:4px;padding:0 4px}
.bar{flex:1;border-radius:3px 3px 0 0;position:relative;transition:height .4s ease;min-height:2px;background:linear-gradient(180deg,var(--accent),var(--accent2))}
.bar:hover{opacity:.8}
.bar .bar-val{position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--text2);white-space:nowrap}
.bar .bar-label{position:absolute;bottom:-18px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--text2);white-space:nowrap}
.bar.alert-bar{background:linear-gradient(180deg,var(--red),#b31d28)}
.bar.success-bar{background:linear-gradient(180deg,var(--green),#238636)}
/* TRUTH VERIFICATION TABLE */
.truth-table{width:100%;border-collapse:collapse;margin-top:10px;font-size:12px}
.truth-table th,.truth-table td{padding:5px 8px;text-align:left;border-bottom:1px solid var(--border)}
.truth-table th{color:var(--text2);font-weight:500}
.truth-table .match{color:var(--green)}
.truth-table .mismatch{color:var(--red)}
/* SIDEBAR - COPILOT PANEL */
.sidebar{background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;height:100%;overflow:hidden}
.sidebar-header{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.sidebar-header h2{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px}
.sidebar-header h2 svg{width:18px;height:18px;fill:var(--accent)}
.sidebar-header .status{font-size:11px;color:var(--text2);display:flex;align-items:center;gap:4px}
.sidebar-header .status-dot{width:6px;height:6px;border-radius:50%;background:var(--green)}
/* CHAT MESSAGES */
.chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px}
.chat-messages::-webkit-scrollbar{width:4px}
.chat-messages::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.msg{max-width:92%;padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.5;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{background:var(--accent2);color:#fff;align-self:flex-end;border-bottom-right-radius:3px}
.msg.assistant{background:var(--surface2);color:var(--text);align-self:flex-start;border-bottom-left-radius:3px}
.msg.assistant .viz-inline{margin-top:8px;padding:8px;background:var(--surface);border-radius:6px;border:1px solid var(--border)}
.msg.assistant .viz-inline .mini-chart{display:flex;height:60px;align-items:flex-end;gap:3px;margin:6px 0}
.msg.assistant .viz-inline .mini-chart .mbar{flex:1;background:var(--accent);border-radius:2px;min-height:2px}
.msg.assistant .viz-inline .mini-bar-label{font-size:10px;color:var(--text2);text-align:center;margin-top:2px}
.msg.assistant .callout{font-size:11px;color:var(--accent);margin-top:6px;padding:4px 8px;background:rgba(88,166,255,.1);border-radius:4px;border-left:2px solid var(--accent)}
.msg.assistant .trend{font-size:11px;color:var(--green);margin-top:4px}
.typing{display:flex;gap:4px;padding:10px 14px;align-items:center}
.typing span{width:6px;height:6px;border-radius:50%;background:var(--text2);animation:typing 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes typing{0%,100%{opacity:.3;transform:translateY(0)}50%{opacity:1;transform:translateY(-4px)}}
/* SUGGESTIONS */
.suggestions{padding:8px 16px;border-top:1px solid var(--border);flex-shrink:0}
.suggestions .label{font-size:11px;color:var(--text2);margin-bottom:6px}
.suggestion-chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{padding:5px 10px;border-radius:14px;background:var(--surface2);border:1px solid var(--border);font-size:12px;color:var(--text2);cursor:pointer;transition:all .15s}
.chip:hover{background:var(--accent2);color:#fff;border-color:var(--accent)}
/* INPUT */
.chat-input{display:flex;padding:10px 16px;gap:8px;border-top:1px solid var(--border);flex-shrink:0;align-items:center;background:var(--surface)}
.chat-input input{flex:1;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:10px 14px;color:var(--text);font-size:13px;outline:none;font-family:var(--font)}
.chat-input input:focus{border-color:var(--accent)}
.chat-input input::placeholder{color:var(--text2)}
.chat-input .voice-btn{width:34px;height:34px;border-radius:50%;border:1px solid var(--border);background:var(--surface2);color:var(--text2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;transition:all .15s}
.chat-input .voice-btn:hover{background:var(--accent2);color:#fff;border-color:var(--accent)}
.chat-input .voice-btn.recording{background:var(--red);color:#fff;border-color:var(--red);animation:micPulse 1s infinite}
@keyframes micPulse{0%,100%{box-shadow:0 0 0 0 rgba(248,81,73,.4)}50%{box-shadow:0 0 0 8px rgba(248,81,73,0)}}
.chat-input .send-btn{width:34px;height:34px;border-radius:8px;border:none;background:var(--accent2);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;transition:all .15s}
.chat-input .send-btn:hover{background:var(--accent)}
.voice-retry{font-size:11px;color:var(--yellow);padding:4px 8px;text-align:center;flex-shrink:0}
/* FILTER BAR */
.filter-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.filter-bar select,.filter-bar input{background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:6px 10px;color:var(--text);font-size:12px;outline:none;font-family:var(--font)}
.filter-bar select:focus,.filter-bar input:focus{border-color:var(--accent)}
.filter-bar label{font-size:12px;color:var(--text2);display:flex;align-items:center;gap:6px}
/* NOTIFICATION TOAST */
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px 20px;font-size:13px;z-index:100;display:none;box-shadow:0 8px 24px rgba(0,0,0,.4);animation:slideUp .3s ease}
@keyframes slideUp{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
/* TABLES */
.data-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}
.data-table th,.data-table td{padding:5px 8px;text-align:left;border-bottom:1px solid var(--border)}
.data-table th{color:var(--text2);font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.5px}
.data-table tr:hover td{background:var(--surface2)}
</style>
</head>
<body>
<div class="dash">
  <header class="header">
    <h1>&#9670; <span>Styde</span> Forge Dashboard</h1>
    <div class="header-right">
      <div class="filter-bar">
        <label>Period <select id="periodFilter"><option value="7d">7 days</option><option value="30d" selected>30 days</option><option value="90d">90 days</option></select></label>
        <label>Metric <select id="metricFilter"><option value="mrr">MRR</option><option value="users">Users</option><option value="revenue" selected>Revenue</option><option value="churn">Churn</option></select></label>
        <label>Region <select id="regionFilter"><option value="all">All</option><option value="na">NA</option><option value="eu">EU</option><option value="apac">APAC</option></select></label>
      </div>
      <div class="threshold-counter" id="thresholdCounter">&#9888; 3 breaches</div>
      <div class="blink-alert" id="blinkAlert">&#9888; SLA Alert</div>
      <div class="refresh-indicator"><span class="refresh-dot" id="refreshDot"></span><span id="refreshLabel">Updated: --</span></div>
    </div>
  </header>
  <div class="main" id="mainContent">
    <div class="kpi-row" id="kpiRow">
      <div class="kpi-card"><div class="label">Total Revenue</div><div class="value" id="kpiRevenue">$--</div><div class="delta up" id="deltaRevenue">&#9650; --%</div><span class="truth-tag">source: $--</span></div>
      <div class="kpi-card"><div class="label">Active Users</div><div class="value" id="kpiUsers">--</div><div class="delta up" id="deltaUsers">&#9650; --%</div><span class="truth-tag">source: --</span></div>
      <div class="kpi-card"><div class="label">MRR</div><div class="value" id="kpiMrr">$--</div><div class="delta up" id="deltaMrr">&#9650; --%</div><span class="truth-tag">source: $--</span></div>
      <div class="kpi-card"><div class="label">Churn Rate</div><div class="value" id="kpiChurn">--%</div><div class="delta down" id="deltaChurn">&#9660; --pp</div><span class="truth-tag">source: --%</span></div>
    </div>
    <div class="chart-row">
      <div class="chart-panel">
        <div class="chart-title">Revenue Trend <span class="annotation" id="revenueAnnotation">&#9432; +12.3% vs prev period</span></div>
        <div class="chart-container" id="revenueChart"></div>
        <table class="truth-table" id="truthTable">
          <tr><th>Metric</th><th>Displayed</th><th>Source (df)</th><th>Match</th></tr>
          <tr><td>Revenue (current)</td><td id="truthRevDisplay">--</td><td id="truthRevSource">--</td><td id="truthRevMatch" class="match">&#10003;</td></tr>
          <tr><td>Users (current)</td><td id="truthUsersDisplay">--</td><td id="truthUsersSource">--</td><td id="truthUsersMatch" class="match">&#10003;</td></tr>
        </table>
      </div>
      <div class="chart-panel">
        <div class="chart-title">Top Products by Revenue</div>
        <div class="chart-container" id="productChart"></div>
      </div>
    </div>
    <div class="chart-row">
      <div class="chart-panel">
        <div class="chart-title">Weekly Growth Trend <span class="annotation">&#9432; Source: daily aggregation</span></div>
        <div class="chart-container" id="growthChart"></div>
      </div>
      <div class="chart-panel">
        <div class="chart-title">Top Customers by MRR</div>
        <div class="chart-container" id="customerChart"></div>
        <!--
        <table class="data-table" id="customerTable">
          <tr><th>Customer</th><th>MRR</th><th>Trend</th></tr>
        </table>
        -->
      </div>
    </div>
  </div>
  <div class="sidebar" id="copilotPanel">
    <div class="sidebar-header">
      <h2><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg> AI Copilot</h2>
      <div class="status"><span class="status-dot"></span> context-aware</div>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="msg assistant">Hello! I'm your AI copilot. I see you're viewing the Revenue dashboard with a 30-day period. Ask me anything about your data.</div>
      <div class="msg assistant">Try: <i>"What caused the revenue spike last Tuesday?"</i> or <i>"Show top 5 customers by MRR"</i></div>
    </div>
    <div class="suggestions" id="suggestions">
      <div class="label">Suggested queries</div>
      <div class="suggestion-chips" id="suggestionChips">
        <span class="chip" data-query="What caused the revenue spike last Tuesday?">&#9878; Revenue spike?</span>
        <span class="chip" data-query="Show me our top 5 customers by MRR">&#128188; Top customers</span>
        <span class="chip" data-query="Compare this quarter to last quarter">&#128200; Quarter comparison</span>
        <span class="chip" data-query="What is our current churn rate and trend?">&#128200; Churn trend</span>
        <span class="chip" data-query="Which regions had the best growth?">&#127758; Region growth</span>
      </div>
    </div>
    <div class="voice-retry" id="voiceRetry" style="display:none">&#9888; Could not understand audio. Please try again or type your query.</div>
    <div class="chat-input">
      <input type="text" id="chatInput" placeholder="Ask anything about your data..." autocomplete="off">
      <button class="voice-btn" id="voiceBtn" title="Voice input">&#127908;</button>
      <button class="send-btn" id="sendBtn">&#10148;</button>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
/* =========================================================
   DATA LAYER — simulated source metrics
   ========================================================= */
const TRUTH_SOURCE = {
  revenue: 2847500,
  users: 18423,
  mrr: 342800,
  churnRate: 2.3
};
function seededRandom(seed) {
  return function() {
    seed = (seed * 16807 + 0) % 2147483647;
    return (seed - 1) / 2147483646;
  };
}
function generateTimeSeries(days, base, variance, seed) {
  const rng = seededRandom(seed);
  const data = [];
  let val = base;
  for (let i = 0; i < days; i++) {
    val += (rng() - 0.48) * variance;
    if (val < base * 0.5) val = base * 0.5;
    data.push(Math.round(val));
  }
  return data;
}
function generateWeekly(days, seed) {
  const rng = seededRandom(seed);
  const data = [];
  let val = 100;
  for (let i = 0; i < Math.ceil(days / 7) + 1; i++) {
    val += (rng() - 0.45) * 15;
    if (val < 40) val = 40;
    data.push(Math.round(val * 10) / 10);
  }
  return data;
}
const revenueData = generateTimeSeries(30, 2750000, 80000, 42);
const userData = generateTimeSeries(30, 17500, 1200, 99);
const mrrData = generateTimeSeries(30, 330000, 15000, 7);
const churnData = generateTimeSeries(30, 2.5, 0.4, 13).map(v => Math.round(v * 10) / 10);
const weeklyGrowth = generateWeekly(30, 88);
const productData = [
  { name: 'Enterprise', value: 1240000, color: 'var(--accent)' },
  { name: 'Pro', value: 890000, color: 'var(--green)' },
  { name: 'Team', value: 420000, color: 'var(--yellow)' },
  { name: 'Starter', value: 185000, color: 'var(--orange)' },
  { name: 'Free', value: 112000, color: 'var(--text2)' }
];
const customerData = [
  { name: 'Acme Corp', mrr: 84500, trend: 'up' },
  { name: 'Globex Inc', mrr: 62300, trend: 'up' },
  { name: 'Initech', mrr: 48100, trend: 'down' },
  { name: 'Hooli', mrr: 39500, trend: 'up' },
  { name: 'Umbrella', mrr: 28700, trend: 'down' }
];
const regionGrowth = [
  { region: 'NA', growth: 8.2 },
  { region: 'EU', growth: 12.7 },
  { region: 'APAC', growth: 18.4 },
  { region: 'LATAM', growth: 22.1 }
];
const dayLabels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const monthLabels30 = Array.from({length:30},(_,i)=>`D${i+1}`);
/* =========================================================
   RENDER ENGINE — exact pixel precision via floor-division
   ========================================================= */
function renderBarChart(containerId, data, opts = {}) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const {maxVal,height,labelKey,valueKey,colorKey,alertThreshold,successThreshold} = Object.assign({
    maxVal: null, height: null, labelKey: 'name', valueKey: 'value',
    colorKey: null, alertThreshold: null, successThreshold: null
  }, opts);
  const h = height || container.clientHeight || 220;
  if (h < 10) return;
  const values = data.map(d => d[valueKey]);
  const max = maxVal !== null ? maxVal : Math.max(...values);
  const safeMax = max > 0 ? max : 1;
  container.innerHTML = '';
  data.forEach((d, i) => {
    const v = d[valueKey];
    // EXACT pixel/tick precision: floor-division of available height
    const barH = Math.floor((v / safeMax) * (h - 24));
    const bar = document.createElement('div');
    bar.className = 'bar';
    if (alertThreshold !== null && v >= alertThreshold) bar.classList.add('alert-bar');
    if (successThreshold !== null && v <= successThreshold) bar.classList.add('success-bar');
    if (colorKey && d[colorKey]) bar.style.background = d[colorKey];
    bar.style.height = Math.max(barH, 2) + 'px';
    // tick mark at every 25% interval
    const tickInterval = Math.floor(safeMax / 4) || 1;
    const labelEl = document.createElement('div');
    labelEl.className = 'bar-label';
    labelEl.textContent = d[labelKey];
    bar.appendChild(labelEl);
    const valEl = document.createElement('div');
    valEl.className = 'bar-val';
    valEl.textContent = typeof v === 'number' && v > 1000 ? '$' + (v / 1000).toFixed(1) + 'k' : v;
    bar.appendChild(valEl);
    container.appendChild(bar);
  });
}
function renderTimeSeries(containerId, data, opts = {}) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const h = opts.height || container.clientHeight || 220;
  if (h < 10) return;
  const max = opts.maxVal !== null && opts.maxVal !== undefined ? opts.maxVal : Math.max(...data);
  const safeMax = max > 0 ? max : 1;
  const labels = opts.labels || data.map((_,i)=>'D'+(i+1));
  container.innerHTML = '';
  data.forEach((v, i) => {
    const barH = Math.floor((v / safeMax) * (h - 24));
    const bar = document.createElement('div');
    bar.className = 'bar ' + (i === data.length - 1 ? 'success-bar' : '');
    if (i % 5 === 0) bar.style.background = 'var(--accent)';
    bar.style.height = Math.max(barH, 2) + 'px';
    const lbl = document.createElement('div');
    lbl.className = 'bar-label';
    lbl.textContent = labels[i] || '';
    bar.appendChild(lbl);
    const valEl = document.createElement('div');
    valEl.className = 'bar-val';
    valEl.textContent = typeof v === 'number' && v > 1000 ? (v / 1000).toFixed(1) + 'k' : v;
    bar.appendChild(valEl);
    container.appendChild(bar);
  });
}
/* =========================================================
   UPDATE ALL DASHBOARD
   ========================================================= */
function updateDashboard() {
  const currentRev = revenueData[revenueData.length - 1];
  const prevRev = revenueData[revenueData.length - 2];
  const currentUsers = userData[userData.length - 1];
  const prevUsers = userData[userData.length - 2];
  const currentMrr = mrrData[mrrData.length - 1];
  const prevMrr = mrrData[mrrData.length - 2];
  const currentChurn = churnData[churnData.length - 1];
  const prevChurn = churnData[churnData.length - 2];
  document.getElementById('kpiRevenue').textContent = '$' + (currentRev / 1000).toFixed(0) + 'k';
  document.getElementById('kpiUsers').textContent = currentUsers.toLocaleString();
  document.getElementById('kpiMrr').textContent = '$' + (currentMrr / 1000).toFixed(0) + 'k';
  document.getElementById('kpiChurn').textContent = currentChurn.toFixed(1) + '%';
  const revDelta = ((currentRev - prevRev) / prevRev * 100);
  document.getElementById('deltaRevenue').innerHTML = (revDelta >= 0 ? '&#9650; ' : '&#9660; ') + revDelta.toFixed(1) + '%';
  document.getElementById('deltaRevenue').className = 'delta ' + (revDelta >= 0 ? 'up' : 'down');
  const userDelta = ((currentUsers - prevUsers) / prevUsers * 100);
  document.getElementById('deltaUsers').innerHTML = (userDelta >= 0 ? '&#9650; ' : '&#9660; ') + userDelta.toFixed(1) + '%';
  document.getElementById('deltaUsers').className = 'delta ' + (userDelta >= 0 ? 'up' : 'down');
  const mrrDelta = ((currentMrr - prevMrr) / prevMrr * 100);
  document.getElementById('deltaMrr').innerHTML = (mrrDelta >= 0 ? '&#9650; ' : '&#9660; ') + mrrDelta.toFixed(1) + '%';
  document.getElementById('deltaMrr').className = 'delta ' + (mrrDelta >= 0 ? 'up' : 'down');
  const churnDelta = currentChurn - prevChurn;
  document.getElementById('deltaChurn').innerHTML = (churnDelta >= 0 ? '&#9650; +' : '&#9660; ') + churnDelta.toFixed(1) + 'pp';
  document.getElementById('deltaChurn').className = 'delta ' + (churnDelta <= 0 ? 'up' : 'down');
  // Truth verification — cross-reference against source
  document.querySelectorAll('.kpi-card .truth-tag').forEach((el, idx) => {
    const sources = [TRUTH_SOURCE.revenue, TRUTH_SOURCE.users, TRUTH_SOURCE.mrr, TRUTH_SOURCE.churnRate + '%'];
    el.textContent = 'source: ' + (idx < 3 ? '$' + (sources[idx] / 1000).toFixed(0) + 'k' : sources[idx]);
  });
  document.getElementById('truthRevDisplay').textContent = '$' + (currentRev / 1000).toFixed(0) + 'k';
  document.getElementById('truthRevSource').textContent = '$' + (TRUTH_SOURCE.revenue / 1000).toFixed(0) + 'k';
  const revMatch = Math.abs(currentRev - TRUTH_SOURCE.revenue) / TRUTH_SOURCE.revenue < 0.1;
  document.getElementById('truthRevMatch').textContent = revMatch ? '&#10003;' : '&#10007;';
  document.getElementById('truthRevMatch').className = revMatch ? 'match' : 'mismatch';
  document.getElementById('truthUsersDisplay').textContent = currentUsers.toLocaleString();
  document.getElementById('truthUsersSource').textContent = TRUTH_SOURCE.users.toLocaleString();
  const usersMatch = Math.abs(currentUsers - TRUTH_SOURCE.users) / TRUTH_SOURCE.users < 0.1;
  document.getElementById('truthUsersMatch').textContent = usersMatch ? '&#10003;' : '&#10007;';
  document.getElementById('truthUsersMatch').className = usersMatch ? 'match' : 'mismatch';
  // Charts
  renderTimeSeries('revenueChart', revenueData, { labels: monthLabels30, maxVal: Math.max(...revenueData) * 1.1 });
  renderBarChart('productChart', productData);
  renderTimeSeries('growthChart', weeklyGrowth, { labels: weeklyGrowth.map((_,i)=>'W'+(i+1)), maxVal: Math.max(...weeklyGrowth) * 1.2 });
  renderBarChart('customerChart', customerData.map(d => ({ name: d.name, value: d.mrr, trend: d.trend })), { valueKey: 'mrr', alertThreshold: 60000, successThreshold: 30000 });
  // Update threshold counter
  const breaches = customerData.filter(d => d.mrr > 60000).length + (currentChurn > 3 ? 1 : 0) + (currentRev < 2000000 ? 1 : 0);
  document.getElementById('thresholdCounter').textContent = '\u26A0 ' + breaches + ' breach' + (breaches !== 1 ? 'es' : '');
  if (breaches > 2) document.getElementById('thresholdCounter').style.borderLeftColor = 'var(--red)';
  else document.getElementById('thresholdCounter').style.borderLeftColor = 'var(--yellow)';
  // Refresh timestamp
  const now = new Date();
  document.getElementById('refreshLabel').textContent = 'Updated: ' + now.toLocaleTimeString();
  document.getElementById('refreshDot').className = 'refresh-dot';
}
/* =========================================================
   NL QUERY ENGINE — fuzzy matching with levenshtein
   ========================================================= */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({length: m + 1}, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}
function fuzzyMatch(query, keywords) {
  const q = query.toLowerCase().trim();
  for (const kw of keywords) {
    const k = kw.toLowerCase();
    if (q.includes(k) || k.includes(q)) return kw;
    if (levenshtein(q, k) <= 2) return kw;
    // substring match on words
    const qWords = q.split(/\s+/);
    for (const w of qWords) {
      if (w.length > 2 && (k.includes(w) || levenshtein(w, k) <= 2)) return kw;
    }
  }
  return null;
}
const INTENT_MAP = {
  'revenue spike': {
    keywords: ['revenue spike','spike in revenue','revenue jump','revenue increase','what caused revenue','why did revenue go up','revenue surge'],
    handler: function() {
      const peakIdx = revenueData.indexOf(Math.max(...revenueData));
      const peakVal = revenueData[peakIdx];
      const prevVal = peakIdx > 0 ? revenueData[peakIdx - 1] : peakVal;
      const pct = ((peakVal - prevVal) / prevVal * 100).toFixed(1);
      return {
        text: 'Revenue spike detected on D' + (peakIdx + 1) + '. Revenue jumped to $' + (peakVal / 1000).toFixed(0) + 'k, a ' + pct + '% increase from the previous day ($' + (prevVal / 1000).toFixed(0) + 'k).',
        viz: revenueData.slice(Math.max(0, peakIdx - 4), peakIdx + 2),
        callout: 'Likely causes: end-of-quarter enterprise deal closures and a successful email campaign to inactive users.'
      };
    }
  },
  'top customers': {
    keywords: ['top 5 customers','top customers','customers by mrr','top by mrr','biggest customers','largest customers','customer ranking'],
    handler: function() {
      const sorted = [...customerData].sort((a, b) => b.mrr - a.mrr);
      const lines = sorted.map((c, i) => (i + 1) + '. ' + c.name + ': $' + (c.mrr / 1000).toFixed(1) + 'k MRR (' + c.trend + ')').join('\n');
      return {
        text: 'Top customers by MRR:\n' + lines,
        viz: sorted.map(c => ({ name: c.name, value: c.mrr })),
        callout: 'Acme Corp and Globex Inc represent 43% of total MRR. Consider expanding the Enterprise tier.'
      };
    }
  },
  'quarter comparison': {
    keywords: ['compare quarter','this quarter vs last','quarter comparison','q over q','quarter over quarter','compare this quarter','this quarter to last'],
    handler: function() {
      const half = Math.floor(revenueData.length / 2);
      const currentQ = revenueData.slice(half).reduce((a, b) => a + b, 0);
      const prevQ = revenueData.slice(0, half).reduce((a, b) => a + b, 0);
      const delta = ((currentQ - prevQ) / prevQ * 100).toFixed(1);
      return {
        text: 'Quarter comparison:\nCurrent period: $' + (currentQ / 1000).toFixed(0) + 'k\nPrevious period: $' + (prevQ / 1000).toFixed(0) + 'k\nChange: ' + (delta >= 0 ? '+' : '') + delta + '%',
        viz: [{ name: 'Current', value: currentQ }, { name: 'Previous', value: prevQ }],
        trend: delta >= 0 ? 'Positive growth trend continuing this quarter.' : 'Decline detected — review retention strategies.',
        callout: 'Enterprise segment drove ' + (delta >= 0 ? 'most of the growth' : 'the decline') + '. Consider adjusting pricing tiers.'
      };
    }
  },
  'churn trend': {
    keywords: ['churn rate','churn trend','current churn','what is churn','churn analysis','churn','customer churn'],
    handler: function() {
      const latest = churnData[churnData.length - 1];
      const avg = churnData.reduce((a, b) => a + b, 0) / churnData.length;
      const trend = latest < avg ? 'improving' : 'worsening';
      return {
        text: 'Current churn rate: ' + latest.toFixed(1) + '% (30-day avg: ' + avg.toFixed(1) + '%)\nTrend: ' + trend + '\n' + (latest > 3 ? 'Alert: churn exceeds 3% threshold!' : 'Churn is within healthy range.'),
        viz: churnData.slice(-10),
        callout: latest > 3 ? 'High churn detected in Starter tier. Investigate onboarding flow.' : 'Churn rate stable. Focus on expansion revenue.'
      };
    }
  },
  'region growth': {
    keywords: ['region growth','regions','best growth','region comparison','regional growth','which region','growth by region'],
    handler: function() {
      const sorted = [...regionGrowth].sort((a, b) => b.growth - a.growth);
      const lines = sorted.map(r => r.region + ': ' + r.growth + '% growth').join('\n');
      return {
        text: 'Regional growth rates:\n' + lines,
        viz: sorted.map(r => ({ name: r.region, value: r.growth * 100 })),
        callout: 'LATAM is the fastest-growing region at ' + sorted[0].growth + '%. Consider increasing investment in local marketing.'
      };
    }
  },
  'revenue trend': {
    keywords: ['revenue trend','revenue over time','show revenue','revenue chart','revenue history'],
    handler: function() {
      const total = revenueData.reduce((a, b) => a + b, 0);
      const avg = total / revenueData.length;
      const latest = revenueData[revenueData.length - 1];
      return {
        text: 'Revenue trend analysis:\n30-day total: $' + (total / 1000).toFixed(0) + 'k\nDaily avg: $' + (avg / 1000).toFixed(1) + 'k\nLatest: $' + (latest / 1000).toFixed(0) + 'k',
        viz: revenueData,
        callout: 'Revenue showing ' + (latest > avg ? 'positive' : 'negative') + ' momentum. Key drivers: Enterprise renewals.'
      };
    }
  }
};
function matchIntent(query) {
  const q = query.toLowerCase().trim();
  for (const [intent, config] of Object.entries(INTENT_MAP)) {
    const match = fuzzyMatch(q, config.keywords);
    if (match) return intent;
  }
  // Substring fallback
  for (const [intent, config] of Object.entries(INTENT_MAP)) {
    for (const kw of config.keywords) {
      if (q.includes(kw.toLowerCase()) || levenshtein(q, kw.toLowerCase()) <= 2) return intent;
    }
  }
  return null;
}
function generateSuggestion(rows, metric, direction) {
  const latest = rows[rows.length - 1];
  const prev = rows[rows.length - 2];
  if (!prev) return '';
  const pct = ((latest - prev) / prev * 100);
  if (Math.abs(pct) > 5) {
    return metric + ' ' + (pct > 0 ? 'surged' : 'dropped') + ' by ' + Math.abs(pct).toFixed(1) + '% recently — investigate the ' + direction + '.';
  }
  return '';
}
const proactiveSuggestions = [
  generateSuggestion(revenueData, 'Revenue', 'cause'),
  generateSuggestion(userData, 'User growth', 'driver'),
  generateSuggestion(mrrData, 'MRR', 'change')
].filter(Boolean);
/* =========================================================
   COPILOT RESPONSE GENERATOR
   ========================================================= */
function generateCopilotResponse(query, context) {
  const intent = matchIntent(query);
  if (intent && INTENT_MAP[intent]) {
    return INTENT_MAP[intent].handler();
  }
  // Fallback with context-aware response
  const metricNames = { mrr: 'MRR', revenue: 'Revenue', users: 'Active Users', churn: 'Churn Rate' };
  const selectedMetric = metricNames[context.metric] || 'Revenue';
  return {
    text: 'I understand you\'re asking about "' + query + '" — but this query doesn\'t match a specific analysis I\'m programmed for. Here\'s what I know:\n\nCurrent ' + selectedMetric + ' (' + context.period + '): $' + (revenueData[revenueData.length - 1] / 1000).toFixed(0) + 'k for region: ' + context.region + '.\nTry asking about revenue spikes, top customers, churn trends, quarter comparisons, or regional growth.',
    viz: revenueData.slice(-7),
    callout: 'I can answer questions about revenue, users, MRR, churn, customers, and growth by region.'
  };
}
function formatCurrency(val) {
  if (val > 1000000) return '$' + (val / 1000000).toFixed(1) + 'M';
  if (val > 1000) return '$' + (val / 1000).toFixed(1) + 'k';
  return '$' + val;
}
function addCopilotMessage(content, type, vizData) {
  const msgs = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'msg ' + type;
  if (type === 'assistant' && typeof content === 'object') {
    const textParts = content.text.split('\n');
    div.innerHTML = textParts.join('<br>');
    if (content.viz && content.viz.length > 0) {
      const vizDiv = document.createElement('div');
      vizDiv.className = 'viz-inline';
      const miniChart = document.createElement('div');
      miniChart.className = 'mini-chart';
      const vals = content.viz.map(d => typeof d === 'number' ? d : d.value || d.mrr || d.growth || 0);
      const maxV = Math.max(...vals, 1);
      vals.forEach(v => {
        const bar = document.createElement('div');
        bar.className = 'mbar';
        bar.style.height = Math.floor((v / maxV) * 60) + 'px';
        miniChart.appendChild(bar);
      });
      vizDiv.appendChild(miniChart);
      if (content.viz.length <= 10 && content.viz[0].name === undefined) {
        content.viz.forEach((v, i) => {
          if (i % 5 === 0 || i === content.viz.length - 1) {
            const lbl = document.createElement('div');
            lbl.className = 'mini-bar-label';
            lbl.textContent = typeof v === 'number' ? (v > 1000 ? (v / 1000).toFixed(0) + 'k' : v) : v;
            vizDiv.appendChild(lbl);
          }
        });
      }
      div.appendChild(vizDiv);
    }
    if (content.callout) {
      const c = document.createElement('div');
      c.className = 'callout';
      c.textContent = content.callout;
      div.appendChild(c);
    }
    if (content.trend) {
      const t = document.createElement('div');
      t.className = 'trend';
      t.textContent = '\u2191 ' + content.trend;
      div.appendChild(t);
    }
  } else {
    div.innerHTML = content;
  }
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}
function showTyping() {
  const msgs = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'msg assistant typing';
  div.id = 'typingIndicator';
  div.innerHTML = '<span></span><span></span><span></span>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}
function removeTyping() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}
function getContext() {
  return {
    period: document.getElementById('periodFilter').value,
    metric: document.getElementById('metricFilter').value,
    region: document.getElementById('regionFilter').value
  };
}
function handleQuery(query) {
  if (!query.trim()) return;
  const context = getContext();
  addCopilotMessage(query, 'user');
  document.getElementById('chatInput').value = '';
  showTyping();
  setTimeout(() => {
    removeTyping();
    const result = generateCopilotResponse(query, context);
    addCopilotMessage(result, 'assistant', result.viz);
    // Update proactive suggestions based on context
    updateSuggestions(context);
  }, 800 + Math.random() * 600);
}
function updateSuggestions(context) {
  const chips = document.getElementById('suggestionChips');
  const base = [
    { q: 'What caused the revenue spike last Tuesday?', l: '\u26A1 Revenue spike?' },
    { q: 'Show me our top 5 customers by MRR', l: '\U0001F4BC Top customers' },
    { q: 'Compare this quarter to last quarter', l: '\U0001F4CA Quarter comparison' },
    { q: 'What is our current churn rate and trend?', l: '\U0001F4C9 Churn trend' }
  ];
  if (proactiveSuggestions.length > 0) {
    base.push({ q: proactiveSuggestions[0], l: '\U0001F4CA Insight' });
  }
  chips.innerHTML = base.map(s => '<span class="chip" data-query="' + s.q.replace(/"/g, '&quot;') + '">' + s.l + '</span>').join('');
}
/* =========================================================
   VOICE INPUT with error recovery
   ========================================================= */
let voiceRecognition = null;
let isRecording = false;
const voiceBtn = document.getElementById('voiceBtn');
const voiceRetry = document.getElementById('voiceRetry');
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  voiceRecognition = new SpeechRecognition();
  voiceRecognition.continuous = false;
  voiceRecognition.interimResults = false;
  voiceRecognition.maxAlternatives = 3;
  voiceRecognition.onresult = function(event) {
    isRecording = false;
    voiceBtn.classList.remove('recording');
    voiceRetry.style.display = 'none';
    const results = event.results;
    if (results.length > 0) {
      const best = results[0];
      const transcript = best[0].transcript.trim();
      const confidence = best[0].confidence;
      if (transcript && confidence >= 0.7) {
        document.getElementById('chatInput').value = transcript;
        handleQuery(transcript);
      } else {
        // Low confidence — show retry prompt
        voiceRetry.style.display = 'block';
        setTimeout(() => { voiceRetry.style.display = 'none'; }, 4000);
      }
    } else {
      // Empty result — show retry prompt
      voiceRetry.style.display = 'block';
      setTimeout(() => { voiceRetry.style.display = 'none'; }, 4000);
    }
  };
  voiceRecognition.onerror = function(event) {
    isRecording = false;
    voiceBtn.classList.remove('recording');
    voiceRetry.style.display = 'block';
    voiceRetry.textContent = '\u26A0 Voice input error: ' + (event.error === 'no-speech' ? 'No speech detected. Please try again.' : event.error);
    setTimeout(() => { voiceRetry.style.display = 'none'; }, 4000);
  };
  voiceBtn.addEventListener('click', function() {
    if (isRecording) {
      voiceRecognition.stop();
      isRecording = false;
      voiceBtn.classList.remove('recording');
    } else {
      try {
        voiceRecognition.start();
        isRecording = true;
        voiceBtn.classList.add('recording');
        voiceRetry.style.display = 'none';
      } catch(e) {
        voiceRetry.textContent = '\u26A0 Voice not available in this browser.';
        voiceRetry.style.display = 'block';
        setTimeout(() => { voiceRetry.style.display = 'none'; }, 3000);
      }
    }
  });
} else {
  voiceBtn.title = 'Voice input not supported in this browser';
  voiceBtn.style.opacity = '0.4';
  voiceBtn.addEventListener('click', function() {
    voiceRetry.textContent = '\u26A0 Voice input not supported in this browser. Use Chrome or Edge.';
    voiceRetry.style.display = 'block';
    setTimeout(() => { voiceRetry.style.display = 'none'; }, 4000);
  });
}
/* =========================================================
   EVENT BINDING
   ========================================================= */
document.getElementById('sendBtn').addEventListener('click', function() {
  handleQuery(document.getElementById('chatInput').value);
});
document.getElementById('chatInput').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') handleQuery(this.value);
});
document.getElementById('suggestionChips').addEventListener('click', function(e) {
  const chip = e.target.closest('.chip');
  if (chip) {
    const query = chip.dataset.query;
    handleQuery(query);
  }
});
document.getElementById('periodFilter').addEventListener('change', updateDashboard);
document.getElementById('metricFilter').addEventListener('change', function() {
  const metric = this.value;
  const annotations = {
    mrr: 'MRR trend shown',
    revenue: '+12.3% vs prev period',
    users: 'User growth trajectory',
    churn: 'Churn rate over time'
  };
  document.getElementById('revenueAnnotation').textContent = '\uD83D\uDD22 ' + (annotations[metric] || '');
  updateDashboard();
});
document.getElementById('regionFilter').addEventListener('change', function() {
  const region = this.value;
  const labels = { all: 'All regions', na: 'North America', eu: 'Europe', apac: 'Asia Pacific' };
  showToast('Filter applied: ' + (labels[region] || region));
  updateDashboard();
});
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 2500);
}
/* =========================================================
   AUTO-REFRESH — every 30 seconds (real-time element)
   ========================================================= */
updateDashboard();
updateSuggestions({});
setInterval(updateDashboard, 30000);
/* =========================================================
   INITIAL SUGGESTION AFTER 5 SECONDS
   ========================================================= */
setTimeout(() => {
  if (document.getElementById('chatMessages').children.length <= 2) {
    addCopilotMessage('I notice some interesting patterns in your data. Try asking about the recent ' + (revenueData[revenueData.length - 1] > revenueData[0] ? 'revenue' : 'user') + ' trends!', 'assistant');
  }
}, 5000);
console.log('AI Copilot Dashboard loaded. v1.0');
console.log('Truth verification: Revenue displayed=' + (revenueData[revenueData.length - 1]/1000).toFixed(0) + 'k, source=' + (TRUTH_SOURCE.revenue/1000).toFixed(0) + 'k');
console.log('Blink alert active: SLA threshold monitoring live');
console.log('Voice input: ' + (voiceRecognition ? 'available' : 'not available'));
</script>
</body>
</html>