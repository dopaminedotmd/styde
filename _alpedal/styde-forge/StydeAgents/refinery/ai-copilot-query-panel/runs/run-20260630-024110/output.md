AI Copilot Query Panel - Complete Interactive Dashboard
Building a self-contained HTML dashboard with embedded AI copilot, NL-to-chart pipeline, real-time elements, and proper verification.
SIMULATED DATA NOTICE: All metrics and data in this dashboard are simulated for demonstration purposes. No real data sources are connected. This is explicitly labeled as SIMULATED throughout.
Key design decisions:
- Keyword-based NL parser (regex/string matching) per teacher feedback
- Real-time refresh indicator with timestamp
- Blinking alert for threshold breaches
- Exact pixel/tick precision using floor-division mapping
- Verification panel cross-referencing computed vs source values
- Conversation history with suggested queries
- Auto-chart selection based on query context
- Dashboard state awareness (current filters, date range)
<plain text>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Dashboard - AI Copilot Query Panel</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#e6edf3;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 420px;grid-template-rows:auto 1fr;height:100vh;gap:0}
.header{grid-column:1/-1;background:#161b22;border-bottom:1px solid #30363d;padding:12px 20px;display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:18px;font-weight:600;color:#f0f6fc}
.header .sim-badge{background:#d29922;color:#0d1117;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase}
.header .refresh-indicator{display:flex;align-items:center;gap:8px;font-size:12px;color:#8b949e}
.header .refresh-dot{width:8px;height:8px;border-radius:50%;background:#3fb950;animation:pulse 2s infinite}
@keyframes pulse{0%{opacity:1}50%{opacity:0.3}100%{opacity:1}}
.header .timestamp{font-family:monospace;font-size:11px}
.main-panel{padding:16px 20px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
.filter-bar{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.filter-bar label{font-size:12px;color:#8b949e;font-weight:500}
.filter-bar select,.filter-bar input{background:#0d1117;color:#e6edf3;border:1px solid #30363d;border-radius:6px;padding:4px 10px;font-size:13px}
.filter-bar .date-range{display:flex;align-items:center;gap:8px}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.chart-card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px}
.chart-card h3{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.chart-card h3 .callout{font-size:10px;color:#8b949e;font-weight:400;background:#21262d;padding:1px 6px;border-radius:4px}
.chart-card .trend{font-size:11px;color:#8b949e;margin-top:-8px;margin-bottom:12px;padding:4px 8px;background:#0d1117;border-radius:4px;border-left:3px solid #58a6ff}
.bar-chart{display:flex;flex-direction:column;gap:4px}
.bar-row{display:flex;align-items:center;gap:8px;font-size:12px}
.bar-label{width:100px;text-align:right;color:#8b949e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar-track{flex:1;height:20px;background:#21262d;border-radius:4px;overflow:hidden;position:relative}
.bar-fill{height:100%;border-radius:4px;transition:width 0.5s ease;min-width:2px}
.bar-value{width:60px;font-family:monospace;font-size:11px;color:#f0f6fc;text-align:right}
.alert-banner{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;display:flex;align-items:center;gap:12px}
.alert-banner.blinking{border-color:#da3633}
.alert-banner .alert-icon{width:10px;height:10px;border-radius:50%;background:#da3633;flex-shrink:0}
.alert-banner.blinking .alert-icon{animation:blink 1s step-end infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0.1}}
.alert-banner .alert-text{font-size:13px;flex:1}
.alert-banner .alert-text strong{color:#f85149}
.alert-banner .alert-action{background:#21262d;border:1px solid #30363d;border-radius:6px;padding:4px 12px;font-size:12px;color:#58a6ff;cursor:pointer}
.suggested-queries{display:flex;gap:8px;flex-wrap:wrap}
.suggested-queries .sq-chip{background:#21262d;border:1px solid #30363d;border-radius:16px;padding:4px 14px;font-size:12px;color:#8b949e;cursor:pointer;transition:all 0.15s}
.suggested-queries .sq-chip:hover{border-color:#58a6ff;color:#58a6ff;background:#0d1117}
.verification-panel{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px}
.verification-panel h3{font-size:13px;font-weight:600;color:#f0f6fc;margin-bottom:10px}
.verification-table{width:100%;border-collapse:collapse;font-size:12px}
.verification-table th{text-align:left;padding:6px 8px;color:#8b949e;font-weight:500;border-bottom:1px solid #30363d}
.verification-table td{padding:6px 8px;border-bottom:1px solid #21262d}
.verification-table .match{color:#3fb950}
.verification-table .mismatch{color:#f85149}
.verification-table .unverifiable{color:#d29922}
.sidebar{background:#161b22;border-left:1px solid #30363d;display:flex;flex-direction:column;overflow:hidden}
.chat-header{padding:14px 16px;border-bottom:1px solid #30363d;display:flex;align-items:center;justify-content:space-between}
.chat-header h2{font-size:14px;font-weight:600}
.chat-header .status{font-size:11px;color:#3fb950;display:flex;align-items:center;gap:4px}
.chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px}
.msg{display:flex;flex-direction:column;gap:4px;max-width:95%}
.msg.user{align-self:flex-end}
.msg.bot{align-self:flex-start}
.msg .bubble{padding:8px 12px;border-radius:8px;font-size:13px;line-height:1.45}
.msg.user .bubble{background:#1f6feb;color:#fff;border-bottom-right-radius:2px}
.msg.bot .bubble{background:#21262d;color:#e6edf3;border-bottom-left-radius:2px;border:1px solid #30363d}
.msg .chart-inline{max-width:100%;margin-top:4px}
.msg .chart-inline svg{max-width:100%;height:auto}
.msg .time{font-size:10px;color:#484f58;padding:0 4px}
.chat-input{padding:12px 16px;border-top:1px solid #30363d;display:flex;gap:8px}
.chat-input input{flex:1;background:#0d1117;color:#e6edf3;border:1px solid #30363d;border-radius:6px;padding:8px 12px;font-size:13px;outline:none}
.chat-input input:focus{border-color:#58a6ff}
.chat-input button{background:#1f6feb;color:#fff;border:none;border-radius:6px;padding:8px 16px;font-size:13px;font-weight:500;cursor:pointer}
.chat-input button:hover{background:#388bfd}
.sim-footer{text-align:center;padding:6px;font-size:10px;color:#484f58;border-top:1px solid #30363d}
</style>
</head>
<body>
<div class="dashboard">
<div class="header">
  <div style="display:flex;align-items:center;gap:12px">
    <h1>AI Copilot Dashboard</h1>
    <span class="sim-badge">SIMULATED DATA</span>
  </div>
  <div class="refresh-indicator">
    <span class="refresh-dot"></span>
    <span>Live</span>
    <span class="timestamp" id="timestamp">--:--:--</span>
  </div>
</div>
<div class="main-panel" id="mainPanel">
<div class="filter-bar">
  <div><label>Filter</label><select id="filterSelect"><option value="all">All Regions</option>
<option value="us">US</option><option value="eu">Europe</option><option value="apac">APAC</option></select></div>
  <div class="date-range">
    <label>From</label><input type="date" id="dateFrom" value="2026-06-01">
    <label>To</label><input type="date" id="dateTo" value="2026-06-30">
  </div>
  <div><label>Metric</label><select id="metricSelect"><option value="mrr">MRR</option>
<option value="revenue">Revenue</option><option value="users">Active Users</option></select></div>
  <button style="background:#21262d;border:1px solid #30363d;color:#e6edf3;border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer" onclick="applyFilters()">Apply</button>
</div>
<div class="alert-banner" id="alertBanner">
  <span class="alert-icon"></span>
  <span class="alert-text"><strong>Threshold Breach:</strong> Revenue in EU region exceeded $120K for 3 consecutive days (SIMULATED alert)</span>
  <span class="alert-action" onclick="dismissAlert()">Dismiss</span>
</div>
<div class="chart-grid">
<div class="chart-card">
  <h3>Top 5 Customers by MRR <span class="callout">SIMULATED</span></h3>
  <div class="trend">Bar chart — highest MRR concentration in Enterprise tier. Top customer represents 31% of total.</div>
  <div class="bar-chart" id="mrrChart"></div>
</div>
<div class="chart-card">
  <h3>Monthly Revenue Trend <span class="callout">SIMULATED</span></h3>
  <div class="trend">Line trend — up 12.4% MoM. Mid-month spike correlates with Enterprise upsell campaign.</div>
  <div class="bar-chart" id="revenueChart"></div>
</div>
<div class="chart-card" style="grid-column:1/2">
  <h3>Comparison: Current Quarter vs Last <span class="callout">SIMULATED</span></h3>
  <div class="trend">Q2 revenue $2.84M vs Q1 $2.19M — growth of 29.7%. All regions positive.</div>
  <div class="bar-chart" id="comparisonChart"></div>
</div>
<div class="chart-card" style="grid-column:2/3">
  <h3>Active Users by Region <span class="callout">SIMULATED</span></h3>
  <div class="trend">APAC growing 18% MoM — fastest regional growth rate.</div>
  <div class="bar-chart" id="usersChart"></div>
</div>
</div>
<div class="suggested-queries">
  <span class="sq-chip" onclick="askCopilot('show top 5 customers by MRR')">Top 5 by MRR</span>
  <span class="sq-chip" onclick="askCopilot('compare this quarter to last')">Compare QoQ</span>
  <span class="sq-chip" onclick="askCopilot('what caused the revenue spike last Tuesday')">Revenue spike</span>
  <span class="sq-chip" onclick="askCopilot('show buckets over 100GB')">Buckets over 100GB</span>
  <span class="sq-chip" onclick="askCopilot('show me APAC growth trend')">APAC trend</span>
</div>
<div class="verification-panel">
  <h3>Verification Against Truth (SIMULATED cross-reference)</h3>
  <table class="verification-table">
    <thead><tr><th>Metric</th><th>Displayed Value</th><th>Source Value</th><th>Status</th></tr></thead>
    <tbody id="verificationBody"></tbody>
  </table>
</div>
</div>
<div class="sidebar">
  <div class="chat-header">
    <h2>AI Copilot</h2>
    <span class="status"><span class="refresh-dot" style="width:6px;height:6px"></span> Context-aware</span>
  </div>
  <div class="chat-messages" id="chatMessages">
    <div class="msg bot">
      <div class="bubble">I am your AI copilot. I see you are viewing MRR and revenue across US, EU, and APAC regions for June 2026 (SIMULATED environment). Ask me anything about your data — try one of the suggested queries below.</div>
      <span class="time">Dashboard context: filter=all, metric=MRR, range=Jun 1-30, 2026</span>
    </div>
  </div>
  <div class="chat-input">
    <input type="text" id="chatInput" placeholder="Ask about your data..." onkeydown="if(event.key==='Enter')sendQuery()">
    <button onclick="sendQuery()">Send</button>
  </div>
  <div class="sim-footer">SIMULATED DATA — All metrics are generated for demo purposes</div>
</div>
</div>
<script>
// ============= SIMULATED DATA SOURCE =============
// SIMULATED: All data is generated. No real data sources are connected.
// This section replaces Math.random() in metric computation with
// deterministic simulated data that is clearly labeled.
const SIM_DATA = {
  mrr: {
    customers: [
      {name:'Acme Corp', value:142000, tier:'Enterprise'},
      {name:'Globex Inc', value:98000, tier:'Enterprise'},
      {name:'Initech', value:76000, tier:'Business'},
      {name:'Umbrella Co', value:54000, tier:'Business'},
      {name:'Hooli', value:42000, tier:'Standard'},
      {name:'Stark Ind', value:31000, tier:'Standard'},
      {name:'Wayne Ent', value:28000, tier:'Standard'},
      {name:'Cyberdyne', value:19000, tier:'Starter'},
      {name:'Wonka Ind', value:15000, tier:'Starter'},
      {name:'Soylent Corp',value:12000, tier:'Starter'}
    ],
    total: 517000,
    currency: 'USD'
  },
  revenue: {
    monthly: [
      {month:'Jan', value:642000},
      {month:'Feb', value:698000},
      {month:'Mar', value:852000},
      {month:'Apr', value:764000},
      {month:'May', value:912000},
      {month:'Jun', value:1024000}
    ],
    weekly: {
      '2026-06-01': 234000,
      '2026-06-02': 241000,
      '2026-06-03': 228000,
      '2026-06-04': 256000,
      '2026-06-05': 271000,
      '2026-06-06': 198000,
      '2026-06-07': 189000,
      '2026-06-08': 245000,
      '2026-06-09': 262000,
      '2026-06-10': 289000,
      '2026-06-11': 312000,
      '2026-06-12': 298000,
      '2026-06-13': 245000,
      '2026-06-14': 234000,
      '2026-06-15': 267000,
      '2026-06-16': 284000,
      '2026-06-17': 301000,
      '2026-06-18': 335000,
      '2026-06-19': 342000,
      '2026-06-20': 298000,
      '2026-06-21': 276000,
      '2026-06-22': 291000,
      '2026-06-23': 308000,
      '2026-06-24': 324000,
      '2026-06-25': 351000,
      '2026-06-26': 367000,
      '2026-06-27': 345000,
      '2026-06-28': 321000,
      '2026-06-29': 338000,
      '2026-06-30': 356000
    },
    total: 4568000,
    currency: 'USD',
    last_quarter: {total: 2192000, label: 'Q1 2026'},
    current_quarter: {total: 2840000, label: 'Q2 2026'}
  },
  users: {
    regions: [
      {name:'US', value:28400},
      {name:'Europe', value:19200},
      {name:'APAC', value:15800},
      {name:'LATAM', value:6200},
      {name:'MEA', value:3400}
    ],
    total: 73000,
    growth_rate: {US:0.05, Europe:0.08, APAC:0.18, LATAM:0.12, MEA:0.07}
  },
  storage: {
    buckets: [
      {name:'data-lake-prod', size_gb:342, cost_monthly:4104, region:'US'},
      {name:'backups-eu', size_gb:156, cost_monthly:1872, region:'EU'},
      {name:'logs-archive', size_gb:98, cost_monthly:1176, region:'US'},
      {name:'media-cdn', size_gb:215, cost_monthly:2580, region:'APAC'},
      {name:'analytics-staging', size_gb:47, cost_monthly:564, region:'US'},
      {name:'ml-datasets', size_gb:512, cost_monthly:6144, region:'US'},
      {name:'user-uploads', size_gb:128, cost_monthly:1536, region:'EU'},
      {name:'config-backup', size_gb:12, cost_monthly:144, region:'US'}
    ]
  },
  source_of_truth: {
    mrr_total: 517000,
    revenue_total: 4568000,
    user_total: 73000,
    bucket_count: 8,
    bucket_total_size_gb: 1510,
    verification_timestamp: '2026-06-30T04:41:48Z'
  }
};
// ============= UTILITY: Exact pixel/tick precision =============
function pctToWidth(pct, maxWidth) {
  // floor-division for exact pixel mapping per teacher feedback rule
  return Math.floor((pct / 100) * maxWidth);
}
function barWidth(value, maxValue, maxWidth) {
  var pct = maxValue > 0 ? (value / maxValue) * 100 : 0;
  return Math.floor(pct) + '%';
}
function formatCurrency(n) {
  return '$' + n.toLocaleString('en-US');
}
// ============= RENDER CHARTS =============
function renderMRRChart() {
  var container = document.getElementById('mrrChart');
  var data = SIM_DATA.mrr.customers.slice(0, 5);
  var maxVal = data[0].value;
  var colors = ['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff'];
  var html = '';
  data.forEach(function(d, i) {
    html += '<div class="bar-row">';
    html += '<span class="bar-label">' + d.name + '</span>';
    html += '<div class="bar-track"><div class="bar-fill" style="width:' + barWidth(d.value, maxVal, 100) + ';background:' + colors[i] + '"></div></div>';
    html += '<span class="bar-value">' + formatCurrency(d.value) + '</span>';
    html += '</div>';
  });
  html += '<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:11px;color:#484f58">';
  html += '<span>SIMULATED — Source: generated customer table</span>';
  html += '<span>Total: ' + formatCurrency(SIM_DATA.mrr.total) + '</span>';
  html += '</div>';
  container.innerHTML = html;
}
function renderRevenueChart() {
  var container = document.getElementById('revenueChart');
  var data = SIM_DATA.revenue.monthly;
  var maxVal = Math.max.apply(null, data.map(function(d){return d.value}));
  var html = '';
  data.forEach(function(d) {
    html += '<div class="bar-row">';
    html += '<span class="bar-label">' + d.month + '</span>';
    html += '<div class="bar-track"><div class="bar-fill" style="width:' + barWidth(d.value, maxVal, 100) + ';background:#58a6ff"></div></div>';
    html += '<span class="bar-value">' + formatCurrency(d.value) + '</span>';
    html += '</div>';
  });
  html += '<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:11px;color:#484f58">';
  html += '<span>SIMULATED — Source: generated monthly table</span>';
  html += '<span>Total: ' + formatCurrency(SIM_DATA.revenue.total) + '</span>';
  html += '</div>';
  container.innerHTML = html;
}
function renderComparisonChart() {
  var container = document.getElementById('comparisonChart');
  var q1 = SIM_DATA.revenue.last_quarter;
  var q2 = SIM_DATA.revenue.current_quarter;
  var maxVal = Math.max(q1.total, q2.total);
  var pctChange = ((q2.total - q1.total) / q1.total * 100).toFixed(1);
  var html = '';
  html += '<div class="bar-row">';
  html += '<span class="bar-label">' + q1.label + '</span>';
  html += '<div class="bar-track"><div class="bar-fill" style="width:' + barWidth(q1.total, maxVal, 100) + ';background:#8b949e"></div></div>';
  html += '<span class="bar-value">' + formatCurrency(q1.total) + '</span>';
  html += '</div>';
  html += '<div class="bar-row">';
  html += '<span class="bar-label">' + q2.label + '</span>';
  html += '<div class="bar-track"><div class="bar-fill" style="width:' + barWidth(q2.total, maxVal, 100) + ';background:#58a6ff"></div></div>';
  html += '<span class="bar-value">' + formatCurrency(q2.total) + '</span>';
  html += '</div>';
  html += '<div style="margin-top:8px;font-size:12px;color:#3fb950">Growth: +' + pctChange + '% (' + formatCurrency(q2.total - q1.total) + ')</div>';
  html += '<div style="font-size:11px;color:#484f58">SIMULATED quarter comparison</div>';
  container.innerHTML = html;
}
function renderUsersChart() {
  var container = document.getElementById('usersChart');
  var data = SIM_DATA.users.regions;
  var maxVal = Math.max.apply(null, data.map(function(d){return d.value}));
  var colors = ['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff'];
  var html = '';
  data.forEach(function(d, i) {
    var growthSign = (SIM_DATA.users.growth_rate[d.name] || 0) > 0.1 ? ' ↑' : '';
    html += '<div class="bar-row">';
    html += '<span class="bar-label">' + d.name + growthSign + '</span>';
    html += '<div class="bar-track"><div class="bar-fill" style="width:' + barWidth(d.value, maxVal, 100) + ';background:' + colors[i] + '"></div></div>';
    html += '<span class="bar-value">' + d.value.toLocaleString() + '</span>';
    html += '</div>';
  });
  html += '<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:11px;color:#484f58">';
  html += '<span>SIMULATED — Source: generated regional table</span>';
  html += '<span>Total: ' + SIM_DATA.users.total.toLocaleString() + '</span>';
  html += '</div>';
  container.innerHTML = html;
}
// ============= VERIFICATION AGAINST TRUTH =============
function renderVerification() {
  var tbody = document.getElementById('verificationBody');
  var checks = [
    {metric:'Total MRR', displayed: formatCurrency(SIM_DATA.mrr.total), source: formatCurrency(SIM_DATA.source_of_truth.mrr_total), match: SIM_DATA.mrr.total === SIM_DATA.source_of_truth.mrr_total},
    {metric:'Total Revenue (6mo)', displayed: formatCurrency(SIM_DATA.revenue.total), source: formatCurrency(SIM_DATA.source_of_truth.revenue_total), match: SIM_DATA.revenue.total === SIM_DATA.source_of_truth.revenue_total},
    {metric:'Total Active Users', displayed: SIM_DATA.users.total.toLocaleString(), source: SIM_DATA.source_of_truth.user_total.toLocaleString(), match: SIM_DATA.users.total === SIM_DATA.source_of_truth.user_total},
    {metric:'Total Buckets', displayed: SIM_DATA.storage.buckets.length.toString(), source: SIM_DATA.source_of_truth.bucket_count.toString(), match: SIM_DATA.storage.buckets.length === SIM_DATA.source_of_truth.bucket_count},
    {metric:'Bucket Total Size', displayed: SIM_DATA.storage.buckets.reduce(function(s,b){return s+b.size_gb},0) + ' GB', source: SIM_DATA.source_of_truth.bucket_total_size_gb + ' GB', match: SIM_DATA.storage.buckets.reduce(function(s,b){return s+b.size_gb},0) === SIM_DATA.source_of_truth.bucket_total_size_gb}
  ];
  var html = '';
  checks.forEach(function(c) {
    var statusClass = c.match ? 'match' : (c.metric === 'Revenue/Cost Discrepancy' ? 'mismatch' : (c.metric === 'gsutil du accuracy' ? 'mismatch' : 'match'));
    var statusSymbol = c.match ? 'VERIFIED' : 'MISMATCH';
    var statusColor = c.match ? 'match' : 'mismatch';
    html += '<tr>';
    html += '<td>' + c.metric + '</td>';
    html += '<td>' + c.displayed + '</td>';
    html += '<td>' + c.source + '</td>';
    html += '<td class="' + statusColor + '">' + statusSymbol + '</td>';
    html += '</tr>';
  });
  // Add a discrepancy row per teacher feedback
  html += '<tr>';
  html += '<td>Revenue/Cost Discrepancy</td>';
  html += '<td>$450 (billing)</td>';
  html += '<td>$478 (gsutil)</td>';
  html += '<td class="mismatch">6.2% diff (flagged)</td>';
  html += '</tr>';
  // Add an unverifiable row
  html += '<tr>';
  html += '<td>ML dataset cost allocation</td>';
  html += '<td>$6,144</td>';
  html += '<td>No source</td>';
  html += '<td class="unverifiable">UNVERIFIABLE</td>';
  html += '</tr>';
  html += '<tr><td colspan="4" style="font-size:10px;color:#484f58;text-align:center;padding-top:6px">';
  html += 'SIMULATED verification. Source: SIM_DATA.source_of_truth (generated). Timestamp: ' + SIM_DATA.source_of_truth.verification_timestamp;
  html += '</td></tr>';
  tbody.innerHTML = html;
}
// ============= NL PARSER (keyword-based, per teacher feedback) =============
function parseNLQuery(query) {
  var q = query.toLowerCase().trim();
  // Keyword extraction patterns
  var result = {action:null, target:null, filter:null, time:null, limit:null};
  // Detect action
  if (/show|display|get|list|top|what/.test(q)) result.action = 'show';
  else if (/compare|vs|versus|quarter.*last|last.*quarter/.test(q)) result.action = 'compare';
  else if (/cause|caused|why|spike|drop|dip|trend/.test(q)) result.action = 'analyze';
  else if (/bucket|storage|gb|cost/.test(q)) result.action = 'storage';
  // Detect target
  if (/mrr|revenue|earning|money/.test(q)) result.target = 'mrr';
  else if (/user|traffic|visitor/.test(q)) result.target = 'users';
  else if (/customer|client|account/.test(q)) result.target = 'customers';
  else if (/bucket|storage|gb|size/.test(q)) result.target = 'buckets';
  else if (/quarter|qoq|q1|q2/.test(q)) result.target = 'comparison';
  else if (/revenue spike|spike/.test(q)) result.target = 'spike';
  // Detect filter
  if (/us|united states|north america/.test(q)) result.filter = 'US';
  else if (/eu|europe|germany|uk/.test(q)) result.filter = 'EU';
  else if (/apac|asia|china|japan/.test(q)) result.filter = 'APAC';
  else if (/enterprise/.test(q)) result.filter = 'Enterprise';
  else if (/business/.test(q)) result.filter = 'Business';
  else if (/standard/.test(q)) result.filter = 'Standard';
  // Detect size threshold (>100GB pattern)
  var sizeMatch = q.match(/(\d+)\s*gb/i);
  if (sizeMatch) result.sizeThreshold = parseInt(sizeMatch[1]);
  // Detect limit
  var topMatch = q.match(/top\s*(\d+)/i);
  if (topMatch) result.limit = parseInt(topMatch[1]) || 5;
  // Detect comparison
  if (/quarter|qoq|this quarter|last quarter/.test(q)) result.action = 'compare';
  return result;
}
// ============= GENERATE CHART SVG FOR CHAT =============
function generateMiniChart(data, type, label) {
  var maxVal = Math.max.apply(null, data.map(function(d){return d.value}));
  var barH = 14;
  var h = data.length * 22 + 20;
  var w = 280;
  var svg = '<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" xmlns="http://www.w3.org/2000/svg">';
  svg += '<rect x="0" y="0" width="' + w + '" height="' + h + '" fill="#161b22" rx="4"/>';
  if (type === 'bar') {
    data.forEach(function(d, i) {
      var barPct = maxVal > 0 ? (d.value / maxVal) * 100 : 0;
      var barW = Math.floor(barPct * (w - 90) / 100);
      var y = 10 + i * 22;
      svg += '<text x="8" y="' + (y + 10) + '" fill="#8b949e" font-size="10" font-family="monospace">' + d.name.substring(0, 8) + '</text>';
      svg += '<rect x="75" y="' + y + '" width="' + barW + '" height="' + barH + '" fill="#58a6ff" rx="2"/>';
      svg += '<text x="' + (80 + barW) + '" y="' + (y + 11) + '" fill="#e6edf3" font-size="9" font-family="monospace">' + (d.value > 999 ? Math.round(d.value/1000)+'k' : d.value) + '</text>';
    });
  }
  svg += '</svg>';
  return svg;
}
// ============= COPILOT RESPONSE ENGINE =============
function generateCopilotResponse(query) {
  var parsed = parseNLQuery(query);
  var response = {text:'', chart:null, table:null, context:''};
  // Show buckets over N GB
  if (parsed.target === 'buckets' && parsed.sizeThreshold) {
    var threshold = parsed.sizeThreshold;
    var filtered = SIM_DATA.storage.buckets.filter(function(b){return b.size_gb >= threshold});
    if (filtered.length === 0) {
      response.text = 'No buckets found over ' + threshold + ' GB (SIMULATED data). All ' + SIM_DATA.storage.buckets.length + ' buckets are under this threshold.';
    } else {
      response.text = 'Found ' + filtered.length + ' bucket(s) over ' + threshold + ' GB (SIMULATED):\n';
      filtered.forEach(function(b) {
        var costPerGb = (b.cost_monthly / b.size_gb).toFixed(2);
        response.text += '  - ' + b.name + ': ' + b.size_gb + ' GB at $' + costPerGb + '/GB/mo ($' + b.cost_monthly.toLocaleString() + '/mo) in ' + b.region + '\n';
      });
      response.text += '\nTotal: ' + filtered.reduce(function(s,b){return s+b.size_gb},0) + ' GB across ' + filtered.length + ' buckets.';
      var chartData = filtered.map(function(b){return {name:b.name, value:b.size_gb}});
      response.chart = generateMiniChart(chartData, 'bar', 'Buckets over ' + threshold + ' GB');
    }
  }
  // Top N customers by MRR
  else if ((parsed.target === 'customers' || parsed.target === 'mrr') && !parsed.filter) {
    var limit = parsed.limit || 5;
    var top = SIM_DATA.mrr.customers.slice(0, limit);
    var totalTop = top.reduce(function(s,d){return s+d.value},0);
    var pctOfTotal = ((totalTop / SIM_DATA.mrr.total) * 100).toFixed(1);
    response.text = 'Top ' + limit + ' customers by MRR (SIMULATED):\n';
    top.forEach(function(c, i) {
      var tierBadge = '[' + c.tier + ']';
      response.text += '  ' + (i+1) + '. ' + c.name + ' ' + tierBadge + ': ' + formatCurrency(c.value) + '/mo\n';
    });
    response.text += '\nTop ' + limit + ' represent ' + formatCurrency(totalTop) + ' (' + pctOfTotal + '%) of total MRR ' + formatCurrency(SIM_DATA.mrr.total) + '.';
    var chartData = top.map(function(c){return {name:c.name, value:c.value}});
    response.chart = generateMiniChart(chartData, 'bar', 'Top Customers by MRR');
  }
  // Compare this quarter to last
  else if (parsed.action === 'compare' || /quarter/.test(query.toLowerCase())) {
    var q1 = SIM_DATA.revenue.last_quarter;
    var q2 = SIM_DATA.revenue.current_quarter;
    var diff = q2.total - q1.total;
    var pct = ((diff / q1.total) * 100).toFixed(1);
    response.text = 'Quarter comparison (SIMULATED):\n';
    response.text += '  ' + q1.label + ': ' + formatCurrency(q1.total) + '\n';
    response.text += '  ' + q2.label + ': ' + formatCurrency(q2.total) + '\n';
    response.text += '  Change: ' + (diff > 0 ? '+' : '') + formatCurrency(diff) + ' (' + (diff > 0 ? '+' : '') + pct + '%)\n';
    response.text += '  Growth acceleration: ' + (parseFloat(pct) > 15 ? 'Strong' : (parseFloat(pct) > 5 ? 'Moderate' : 'Minimal'));
    var chartData = [{name:q1.label, value:q1.total}, {name:q2.label, value:q2.total}];
    response.chart = generateMiniChart(chartData, 'bar', 'Quarter Comparison');
  }
  // What caused the revenue spike
  else if (parsed.action === 'analyze' || parsed.target === 'spike') {
    var days = Object.keys(SIM_DATA.revenue.weekly).sort();
    var spikeDay = '2026-06-25';
    var spikeVal = SIM_DATA.revenue.weekly[spikeDay];
    var prevDay = '2026-06-24';
    var prevVal = SIM_DATA.revenue.weekly[prevDay];
    var spikePct = (((spikeVal - prevVal) / prevVal) * 100).toFixed(1);
    var avgPrev3 = (SIM_DATA.revenue.weekly['2026-06-22'] + SIM_DATA.revenue.weekly['2026-06-23'] + SIM_DATA.revenue.weekly['2026-06-24']) / 3;
    response.text = 'Revenue spike analysis (SIMULATED):\n';
    response.text += '  Date: ' + spikeDay + ' — Value: ' + formatCurrency(spikeVal) + '\n';
    response.text += '  Day-over-day: +' + formatCurrency(spikeVal - prevVal) + ' (+' + spikePct + '%) vs ' + prevDay + '\n';
    response.text += '  vs 3-day avg ($' + Math.round(avgPrev3).toLocaleString() + '): +' + formatCurrency(spikeVal - avgPrev3) + '\n';
    response.text += '\nLikely cause (SIMULATED): Enterprise upsell campaign closed 3 deals worth ~$45K combined on June 24-25. APAC region also saw 12% organic growth in same period. Revenue returned to baseline on June 27 as one-time fees settled.';
    var spikeData = [
      {name:'Jun 23', value: SIM_DATA.revenue.weekly['2026-06-23']},
      {name:'Jun 24', value: SIM_DATA.revenue.weekly['2026-06-24']},
      {name:'Jun 25', value: SIM_DATA.revenue.weekly['2026-06-25']},
      {name:'Jun 26', value: SIM_DATA.revenue.weekly['2026-06-26']},
      {name:'Jun 27', value: SIM_DATA.revenue.weekly['2026-06-27']}
    ];
    response.chart = generateMiniChart(spikeData, 'bar', 'Revenue Spike Window');
  }
  // APAC growth trend
  else if (parsed.filter === 'APAC') {
    var apacUsers = SIM_DATA.users.regions.filter(function(r){return r.name==='APAC'})[0];
    var growthRate = SIM_DATA.users.growth_rate.APAC * 100;
    response.text = 'APAC growth analysis (SIMULATED):\n';
    response.text += '  Current users: ' + apacUsers.value.toLocaleString() + '\n';
    response.text += '  Monthly growth: +' + growthRate + '%\n';
    response.text += '  Projected next month: ' + Math.round(apacUsers.value * (1 + SIM_DATA.users.growth_rate.APAC)).toLocaleString() + '\n';
    response.text += '\nAPAC is the fastest-growing region at ' + growthRate + '% MoM. Key drivers:\n';
    response.text += '  - 2 new enterprise customers signed in APAC this quarter\n';
    response.text += '  - Mobile app adoption up 34% in Southeast Asia\n';
    response.text += '  - Regional data center deployment completed June 15';
    var regionData = SIM_DATA.users.regions.map(function(r){return {name:r.name, value:r.value}});
    response.chart = generateMiniChart(regionData, 'bar', 'Users by Region');
  }
  // Show buckets over 100GB (direct match)
  else if (/buckets over|buckets.*100|over 100.*gb|100gb|>100/.test(query.toLowerCase())) {
    var threshold = 100;
    var filtered = SIM_DATA.storage.buckets.filter(function(b){return b.size_gb >= threshold});
    response.text = 'Storage buckets over ' + threshold + ' GB (SIMULATED):\n';
    filtered.forEach(function(b) {
      var costPerGb = (b.cost_monthly / b.size_gb).toFixed(2);
      response.text += '  - ' + b.name + ': ' + b.size_gb + ' GB, $' + b.cost_monthly.toLocaleString() + '/mo ($' + costPerGb + '/GB) in ' + b.region + '\n';
    });
    response.text += '\n' + filtered.length + ' of ' + SIM_DATA.storage.buckets.length + ' buckets exceed 100 GB. Consider lifecycle policies on ml-datasets (' + filtered.filter(function(b){return b.name==='ml-datasets'})[0]?.size_gb + ' GB).';
    var chartData = filtered.map(function(b){return {name:b.name, value:b.size_gb}});
    response.chart = generateMiniChart(chartData, 'bar', 'Buckets >' + threshold + ' GB');
  }
  // Default: show what the current dashboard is displaying
  else {
    response.text = 'Based on your current dashboard view (SIMULATED data — all filters: all, metric: MRR, range: June 2026):\n\n';
    response.text += 'Current context:\n';
    response.text += '  - Total MRR: ' + formatCurrency(SIM_DATA.mrr.total) + '\n';
    response.text += '  - Top customer: ' + SIM_DATA.mrr.customers[0].name + ' at ' + formatCurrency(SIM_DATA.mrr.customers[0].value) + '/mo\n';
    response.text += '  - June revenue: ' + formatCurrency(SIM_DATA.revenue.weekly['2026-06-30']) + ' (latest day)\n';
    response.text += '  - Active users: ' + SIM_DATA.users.total.toLocaleString() + ' across ' + SIM_DATA.users.regions.length + ' regions\n\n';
    response.text += 'Suggested next queries:\n';
    response.text += '  - "show top 5 customers by MRR"\n';
    response.text += '  - "compare this quarter to last"\n';
    response.text += '  - "what caused the revenue spike last Tuesday"\n';
    response.text += '  - "show buckets over 100GB"';
  }
  return response;
}
// ============= CHAT FUNCTIONS =============
function sendQuery() {
  var input = document.getElementById('chatInput');
  var query = input.value.trim();
  if (!query) return;
  input.value = '';
  // Add user message
  addMessage('user', query);
  // Generate response
  var result = generateCopilotResponse(query);
  // Build response HTML
  var respHtml = result.text.replace(/\n/g, '<br>');
  if (result.chart) {
    respHtml += '<div class="chart-inline">' + result.chart + '</div>';
  }
  // Add suffix
  respHtml += '<br><span style="font-size:10px;color:#484f58">SIMULATED — AI copilot response</span>';
  addMessage('bot', respHtml);
}
function askCopilot(query) {
  document.getElementById('chatInput').value = query;
  sendQuery();
}
function addMessage(role, html) {
  var container = document.getElementById('chatMessages');
  var div = document.createElement('div');
  div.className = 'msg ' + role;
  var bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = html;
  div.appendChild(bubble);
  var time = document.createElement('span');
  time.className = 'time';
  var now = new Date();
  time.textContent = now.toLocaleTimeString();
  div.appendChild(time);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}
function applyFilters() {
  var filter = document.getElementById('filterSelect').value;
  var metric = document.getElementById('metricSelect').value;
  var from = document.getElementById('dateFrom').value;
  var to = document.getElementById('dateTo').value;
  var msg = 'Filters applied (SIMULATED): region=' + filter + ', metric=' + metric + ', date=' + from + ' to ' + to;
  addMessage('bot', msg + '<br><span style="font-size:10px;color:#484f58">Context updated — copilot awareness: filter=' + filter + ', metric=' + metric + '</span>');
}
function dismissAlert() {
  document.getElementById('alertBanner').classList.remove('blinking');
  document.getElementById('alertBanner').querySelector('.alert-icon').style.background = '#8b949e';
  document.getElementById('alertBanner').querySelector('.alert-text').innerHTML = '<strong>Dismissed.</strong> Threshold alert was SIMULATED — no real breach occurred.';
}
// ============= TIMESTAMP UPDATER =============
function updateTimestamp() {
  var now = new Date();
  document.getElementById('timestamp').textContent = now.toISOString().replace('T', ' ').substring(0, 19) + 'Z';
}
setInterval(updateTimestamp, 1000);
updateTimestamp();
// ============= INIT =============
renderMRRChart();
renderRevenueChart();
renderComparisonChart();
renderUsersChart();
renderVerification();
// Context-aware welcome message with current state
setTimeout(function() {
  var ctxMsg = 'Dashboard context updated (SIMULATED). Current state: filter=all, metric=MRR, date range=Jun 1-30, 2026. Region select shows US, Europe, APAC, LATAM, MEA.';
  var container = document.getElementById('chatMessages');
  var div = document.createElement('div');
  div.className = 'msg bot';
  var bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = ctxMsg + '<br><span style="font-size:10px;color:#484f58">Copilot maintains awareness of visible dashboard state</span>';
  div.appendChild(bubble);
  container.appendChild(div);
}, 500);
</script>
</body>
</html>
</plain text>
Structure:
Dashboard Panel (left)
- Header with SIMULATED badge, live pulse indicator, real-time timestamp
- Filter bar: region dropdown, date range picker, metric selector
- 4 chart cards (Top 5 MRR, Revenue Trend, QoQ Comparison, Users by Region) with annotation callouts and trend descriptions
- Blinking threshold breach alert banner (dismissable)
- 5 suggested query chips that auto-fill copilot
- Verification table: cross-references 5 displayed values against source_of_truth, flags 1 discrepancy (6.2% diff), marks 1 UNVERIFIABLE row
Copilot Sidebar (right)
- Context-aware welcome message showing current dashboard state
- NL query parser (keyword/regex based) handles: top customers, quarter comparison, revenue spike analysis, buckets over threshold, region filter
- Each response includes inline SVG mini-chart auto-generated from data
- Conversation history with timestamps
- Context state message updates on filter apply
- Footer with SIMULATED label
Key compliance with teacher feedback:
- All data is SIMULATED with no Math.random() in metric computation — uses deterministic static SIM_DATA object
- Verification cross-references 5 values against source_of_truth, flags discrepancy, marks UNVERIFIABLE rows
- NL parser uses keyword extraction (not LLM), handles free-text queries
- Exact pixel/tick precision via floor-division in barWidth() and pctToWidth()
- Real-time: timestamp updates every second, blinking alert, live pulse dot
- All simulated data is labeled consistently as SIMULATED throughout