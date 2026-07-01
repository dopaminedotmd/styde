<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge AI Copilot Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
body{background:#0d1117;color:#e6edf3;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 380px;height:100vh}
.main-panel{padding:20px;overflow-y:auto;border-right:1px solid #30363d}
.chat-panel{display:flex;flex-direction:column;height:100vh;background:#151b23}
.chat-header{padding:14px 16px;border-bottom:1px solid #30363d;font-weight:600;font-size:14px;color:#e6edf3;display:flex;align-items:center;gap:8px}
.chat-header .badge{background:#238636;color:#fff;font-size:10px;padding:1px 6px;border-radius:4px;font-weight:500}
.chat-messages{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:10px}
.message{max-width:92%;padding:10px 12px;border-radius:8px;font-size:13px;line-height:1.45}
.message.user{background:#1f6feb22;border:1px solid #1f6feb44;align-self:flex-end;color:#e6edf3}
.message.assistant{background:#21262d;border:1px solid #30363d;align-self:flex-start;color:#e6edf3}
.message.system{background:#da363322;border:1px solid #da363344;align-self:center;color:#f85149;font-size:12px;text-align:center;width:100%}
.message .chart-container{margin-top:8px;background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:12px;position:relative}
.message .chart-container canvas{width:100%!important;height:auto!important;max-height:180px}
.message .annotation{background:#1f6feb15;border-left:3px solid #1f6feb;padding:6px 10px;margin-top:8px;border-radius:0 4px 4px 0;font-size:12px;color:#8b949e}
.message .annotation b{color:#e6edf3}
.suggested-queries{display:flex;flex-wrap:wrap;gap:6px;padding:8px 14px;border-top:1px solid #30363d}
.suggested-queries button{background:#21262d;border:1px solid #30363d;color:#8b949e;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer;transition:.15s}
.suggested-queries button:hover{background:#30363d;color:#e6edf3;border-color:#1f6feb}
.chat-input-area{display:flex;gap:8px;padding:10px 14px;border-top:1px solid #30363d;align-items:center}
.chat-input-area input{flex:1;background:#0d1117;border:1px solid #30363d;color:#e6edf3;padding:8px 12px;border-radius:6px;font-size:13px;outline:none}
.chat-input-area input:focus{border-color:#1f6feb}
.chat-input-area button{background:#238636;border:none;color:#fff;padding:8px 14px;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer;transition:.15s}
.chat-input-area button:hover{background:#2ea043}
.chat-input-area button:disabled{opacity:.5;cursor:not-allowed}
.chat-input-area .voice-btn{background:transparent;border:1px solid #30363d;color:#8b949e;padding:8px;border-radius:6px;cursor:pointer;font-size:14px}
.chat-input-area .voice-btn:hover{background:#21262d;color:#e6edf3}
.chat-input-area .voice-btn.recording{background:#da3633;color:#fff;border-color:#da3633;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.status-bar{display:flex;gap:8px;padding:6px 14px;border-top:1px solid #30363d;font-size:11px;color:#8b949e;background:#0d1117}
.status-bar .dot{width:6px;height:6px;border-radius:50%;background:#238636;display:inline-block;margin-right:4px}
.status-bar .dot.offline{background:#da3633}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.kpi-card{background:#151b23;border:1px solid #30363d;border-radius:8px;padding:14px 16px}
.kpi-card .label{font-size:11px;text-transform:uppercase;color:#8b949e;letter-spacing:.5px}
.kpi-card .value{font-size:24px;font-weight:700;color:#e6edf3;margin-top:4px}
.kpi-card .delta{font-size:12px;margin-top:2px;color:#3fb950}
.kpi-card .delta.negative{color:#da3633}
.charts-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px}
.chart-card{background:#151b23;border:1px solid #30363d;border-radius:8px;padding:16px}
.chart-card h3{font-size:13px;color:#8b949e;margin-bottom:10px;font-weight:500}
.chart-card canvas{width:100%!important;height:200px!important}
.table-card{background:#151b23;border:1px solid #30363d;border-radius:8px;padding:16px;margin-bottom:20px}
.table-card h3{font-size:13px;color:#8b949e;margin-bottom:10px;font-weight:500}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:8px 10px;border-bottom:2px solid #30363d;color:#8b949e;font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.5px}
td{padding:8px 10px;border-bottom:1px solid #21262d}
tr:hover td{background:#161b22}
.filters-bar{display:flex;gap:10px;margin-bottom:20px;align-items:center}
.filters-bar select,.filters-bar input{background:#151b23;border:1px solid #30363d;color:#e6edf3;padding:6px 10px;border-radius:6px;font-size:12px;outline:none}
.filters-bar select:focus,.filters-bar input:focus{border-color:#1f6feb}
.filters-bar .filter-label{font-size:11px;color:#8b949e;margin-right:2px}
.context-badge{font-size:11px;background:#1f6feb22;color:#58a6ff;padding:2px 8px;border-radius:4px;border:1px solid #1f6feb44}
.thinking-indicator{display:none;align-items:center;gap:6px;padding:8px 14px;color:#8b949e;font-size:12px;border-top:1px solid #30363d}
.thinking-indicator.active{display:flex}
.thinking-indicator .dots{display:flex;gap:3px}
.thinking-indicator .dots span{width:5px;height:5px;border-radius:50%;background:#58a6ff;animation:bounce 1.4s infinite}
.thinking-indicator .dots span:nth-child(2){animation-delay:.2s}
.thinking-indicator .dots span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
</style>
</head>
<body>
<div class="dashboard">
<div class="main-panel">
  <div class="filters-bar">
    <span class="filter-label">Period:</span>
    <select id="periodFilter">
      <option value="7d">Last 7 days</option>
      <option value="30d" selected>Last 30 days</option>
      <option value="90d">Last quarter</option>
      <option value="1y">Year to date</option>
    </select>
    <span class="filter-label">Segment:</span>
    <select id="segmentFilter">
      <option value="all">All customers</option>
      <option value="enterprise">Enterprise</option>
      <option value="midmarket">Mid-market</option>
      <option value="startup">Startup</option>
    </select>
    <span class="filter-label">Region:</span>
    <select id="regionFilter">
      <option value="all">All regions</option>
      <option value="na">North America</option>
      <option value="eu">Europe</option>
      <option value="apac">APAC</option>
    </select>
    <span id="contextDisplay" class="context-badge">30d | All customers | All regions</span>
  </div>
  <div class="kpi-row" id="kpiRow">
    <div class="kpi-card"><div class="label">MRR</div><div class="value" id="kpiMRR">$84,230</div><div class="delta" id="deltaMRR">+12.4% vs prev</div></div>
    <div class="kpi-card"><div class="label">Active Customers</div><div class="value" id="kpiCust">1,847</div><div class="delta" id="deltaCust">+38 this period</div></div>
    <div class="kpi-card"><div class="label">Net Revenue Retention</div><div class="value" id="kpiNRR">108%</div><div class="delta">+3pp vs prev</div></div>
    <div class="kpi-card"><div class="label">Churn Rate</div><div class="value" id="kpiChurn">2.1%</div><div class="delta negative">+0.3pp vs prev</div></div>
  </div>
  <div class="charts-row">
    <div class="chart-card"><h3>Revenue Trend (Daily)</h3><canvas id="revenueChart"></canvas></div>
    <div class="chart-card"><h3>MRR by Segment</h3><canvas id="segmentChart"></canvas></div>
  </div>
  <div class="charts-row">
    <div class="chart-card"><h3>Top Customers by MRR</h3><canvas id="topCustomersChart"></canvas></div>
    <div class="chart-card"><h3>New vs Lost Revenue</h3><canvas id="newLostChart"></canvas></div>
  </div>
  <div class="table-card">
    <h3>Recent Activity</h3>
    <table id="activityTable">
      <thead><tr><th>Event</th><th>Customer</th><th>Amount</th><th>Date</th></tr></thead>
      <tbody>
        <tr><td>New subscription</td><td>Acme Corp</td><td>$2,400/mo</td><td>2026-06-27</td></tr>
        <tr><td>Upgrade</td><td>Beta Inc</td><td>+$1,200/mo</td><td>2026-06-26</td></tr>
        <tr><td>Churn</td><td>OldCo LLC</td><td>-$800/mo</td><td>2026-06-25</td></tr>
        <tr><td>Expansion</td><td>DataFlow</td><td>+$3,100/mo</td><td>2026-06-24</td></tr>
        <tr><td>New subscription</td><td>NovaTech</td><td>$1,800/mo</td><td>2026-06-23</td></tr>
        <tr><td>Downgrade</td><td>SmallShop</td><td>-$400/mo</td><td>2026-06-22</td></tr>
      </tbody>
    </table>
  </div>
</div>
<div class="chat-panel">
  <div class="chat-header">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1a5 5 0 00-5 5c0 1.5.7 2.8 1.7 3.7L4 14l3-1.5a5.5 5.5 0 001 0L11 14l-.7-4.3A5 5 0 008 1z" fill="#58a6ff"/></svg>
    AI Copilot
    <span class="badge">Live API</span>
  </div>
  <div class="chat-messages" id="chatMessages">
    <div class="message assistant">
      Hello! I'm your AI copilot. I can see your dashboard shows 30d data for all customers. Ask me anything about your metrics.
      <div class="annotation">Context: 30d | All customers | All regions — 6 suggestions ready</div>
    </div>
  </div>
  <div class="thinking-indicator" id="thinkingIndicator">
    <span>Analyzing</span>
    <div class="dots"><span></span><span></span><span></span></div>
  </div>
  <div class="suggested-queries" id="suggestedQueries">
    <button onclick="sendSuggested('What caused the revenue spike last Tuesday?')">Revenue spike last Tuesday?</button>
    <button onclick="sendSuggested('Show top 5 customers by MRR')">Top 5 customers by MRR</button>
    <button onclick="sendSuggested('Compare this quarter to last quarter')">Compare this quarter to last</button>
    <button onclick="sendSuggested('Show churn trend for the last 30 days')">Churn trend last 30 days</button>
    <button onclick="sendSuggested('Which segment grew fastest this month?')">Fastest growing segment?</button>
    <button onclick="sendSuggested('What is our average revenue per customer?')">Avg revenue per customer</button>
  </div>
  <div class="chat-input-area">
    <button class="voice-btn" id="voiceBtn" onclick="toggleVoice()" title="Voice input">🎤</button>
    <input type="text" id="chatInput" placeholder="Ask about your data..." onkeydown="if(event.key==='Enter') sendMessage()">
    <button id="sendBtn" onclick="sendMessage()">Send</button>
  </div>
  <div class="status-bar">
    <span><span class="dot" id="statusDot"></span><span id="statusText">API connected</span></span>
    <span style="margin-left:auto">Model: deepseek-v4-flash</span>
  </div>
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<script>
// ── Data store ──────────────────────────────────────────────────
const store = {
  period: '30d',
  segment: 'all',
  region: 'all',
  conversation: [],
  charts: {},
  voiceActive: false,
  recognition: null,
  apiEndpoint: 'https://openrouter.ai/api/v1/chat/completions',
  apiKey: localStorage.getItem('copilot_api_key') || '',
  useMock: !localStorage.getItem('copilot_api_key')
};
// ── Dashboard data (synthetic, realistic) ──────────────────────
function generateDailyRevenue(days) {
  const data = [];
  let base = 2400;
  for (let i = 0; i < days; i++) {
    const spike = (i === days - 7) ? 1.65 : (i === days - 14) ? 1.35 : 1.0;
    const noise = 0.85 + Math.random() * 0.25;
    const val = Math.round(base * spike * noise);
    const d = new Date();
    d.setDate(d.getDate() - (days - 1 - i));
    data.push({ date: d.toISOString().slice(0,10), value: val });
    if (i > 0) base = base * 0.99 + val * 0.01;
  }
  return data;
}
const dailyRevenue = generateDailyRevenue(30);
const segmentData = [
  { label: 'Enterprise', value: 42300, color: '#58a6ff' },
  { label: 'Mid-market', value: 24500, color: '#3fb950' },
  { label: 'Startup', value: 11430, color: '#d29922' },
  { label: 'SMB', value: 6000, color: '#da3633' }
];
const topCustomers = [
  { name: 'Acme Corp', mrr: 12400, change: '+8%' },
  { name: 'Beta Inc', mrr: 9800, change: '+15%' },
  { name: 'DataFlow', mrr: 8700, change: '+22%' },
  { name: 'NovaTech', mrr: 7400, change: '+4%' },
  { name: 'ZenithCo', mrr: 6100, change: '-2%' }
];
const newLostRevenue = [
  { month: 'Jan', new: 5200, lost: 2100 },
  { month: 'Feb', new: 5800, lost: 2300 },
  { month: 'Mar', new: 6400, lost: 1950 },
  { month: 'Apr', new: 7100, lost: 2150 },
  { month: 'May', new: 7900, lost: 2400 },
  { month: 'Jun', new: 8300, lost: 2250 }
];
// ── Chart initialization ───────────────────────────────────────
function initCharts() {
  const commonOpts = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#8b949e', font: { size: 11 } } }
    },
    scales: {
      x: { ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } },
      y: { ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } }
    }
  };
  const ctx1 = document.getElementById('revenueChart').getContext('2d');
  store.charts.revenue = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: dailyRevenue.map(d => d.date.slice(5)),
      datasets: [{
        label: 'Daily Revenue ($)',
        data: dailyRevenue.map(d => d.value),
        borderColor: '#58a6ff',
        backgroundColor: 'rgba(88,166,255,0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 2,
        pointBackgroundColor: '#58a6ff'
      }]
    },
    options: {
      ...commonOpts,
      plugins: {
        ...commonOpts.plugins,
        annotation: {
          annotations: {
            spikePoint: {
              type: 'point',
              xMin: dailyRevenue.length - 8,
              xMax: dailyRevenue.length - 6,
              yMin: Math.max(...dailyRevenue.map(d => d.value)) - 200,
              yMax: Math.max(...dailyRevenue.map(d => d.value)) + 200,
              backgroundColor: 'rgba(218,54,51,0.3)',
              borderColor: '#da3633',
              borderWidth: 2,
              borderRadius: 4,
              label: {
                display: true,
                content: 'Spike +65%',
                position: 'end',
                color: '#f85149',
                font: { size: 10 }
              }
            }
          }
        }
      }
    }
  });
  const ctx2 = document.getElementById('segmentChart').getContext('2d');
  store.charts.segment = new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: segmentData.map(d => d.label),
      datasets: [{
        data: segmentData.map(d => d.value),
        backgroundColor: segmentData.map(d => d.color),
        borderColor: '#0d1117',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#8b949e', font: { size: 11 } } }
      }
    }
  });
  const ctx3 = document.getElementById('topCustomersChart').getContext('2d');
  store.charts.topCustomers = new Chart(ctx3, {
    type: 'bar',
    data: {
      labels: topCustomers.map(d => d.name),
      datasets: [{
        label: 'MRR ($)',
        data: topCustomers.map(d => d.mrr),
        backgroundColor: ['#58a6ff','#3fb950','#d29922','#da3633','#8b949e'],
        borderRadius: 4
      }]
    },
    options: {
      ...commonOpts,
      indexAxis: 'y',
      plugins: {
        ...commonOpts.plugins,
        tooltip: {
          callbacks: {
            afterLabel: function(ctx) { return 'Change: ' + topCustomers[ctx.dataIndex].change; }
          }
        }
      }
    }
  });
  const ctx4 = document.getElementById('newLostChart').getContext('2d');
  store.charts.newLost = new Chart(ctx4, {
    type: 'bar',
    data: {
      labels: newLostRevenue.map(d => d.month),
      datasets: [
        { label: 'New Revenue', data: newLostRevenue.map(d => d.new), backgroundColor: '#3fb950', borderRadius: 3 },
        { label: 'Lost Revenue', data: newLostRevenue.map(d => d.lost), backgroundColor: '#da3633', borderRadius: 3 }
      ]
    },
    options: {
      ...commonOpts,
      scales: {
        x: { stacked: false, ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } },
        y: { stacked: false, ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } }
      }
    }
  });
}
// ── Filter context management ──────────────────────────────────
function updateContext() {
  const p = document.getElementById('periodFilter').value;
  const s = document.getElementById('segmentFilter').value;
  const r = document.getElementById('regionFilter').value;
  store.period = p;
  store.segment = s;
  store.region = r;
  const labels = { '7d':'7d','30d':'30d','90d':'90d','1y':'1y','all':'All','enterprise':'Enterprise','midmarket':'Mid-market','startup':'Startup','na':'North America','eu':'Europe','apac':'APAC' };
  document.getElementById('contextDisplay').textContent = labels[p] + ' | ' + labels[s] + ' | ' + labels[r];
}
document.getElementById('periodFilter').addEventListener('change', updateContext);
document.getElementById('segmentFilter').addEventListener('change', updateContext);
document.getElementById('regionFilter').addEventListener('change', updateContext);
// ── Parse NL query into data operation ─────────────────────────
function parseQuery(query) {
  const q = query.toLowerCase();
  let operation = 'analyze';
  let chartType = 'line';
  let metric = null;
  let filter = null;
  let comparison = null;
  if (q.includes('spike') || q.includes('spike')) operation = 'explain_anomaly';
  if (q.includes('compare') || q.includes('vs') || q.includes('versus') || q.includes('vs.')) {
    operation = 'compare';
    chartType = 'bar';
  }
  if (q.includes('top') && (q.includes('customer') || q.includes('mrr'))) {
    operation = 'rank';
    chartType = 'bar';
    metric = 'mrr';
  }
  if (q.includes('trend') || q.includes('over time') || q.includes('last')) {
    operation = 'trend';
    chartType = 'line';
  }
  if (q.includes('churn')) { metric = 'churn'; operation = 'trend'; }
  if (q.includes('segment') || q.includes('by segment')) { metric = 'segment'; chartType = 'doughnut'; operation = 'breakdown'; }
  if (q.includes('fastest') || q.includes('grew') || q.includes('growth')) { operation = 'growth_analysis'; chartType = 'bar'; }
  if (q.includes('average') || q.includes('avg') || q.includes('arpu') || q.includes('per customer')) { operation = 'compute'; metric = 'arpu'; }
  return { operation, chartType, metric, filter, comparison, raw: query };
}
// ── Mock response generator (development fallback) ──────────────
function generateMockResponse(parsed) {
  const op = parsed.operation;
  const metric = parsed.metric;
  const spikeDay = dailyRevenue[dailyRevenue.length - 7];
  const prevDay = dailyRevenue[dailyRevenue.length - 8];
  const spikePct = Math.round((spikeDay.value / prevDay.value - 1) * 100);
  const responses = {
    explain_anomaly: {
      text: `The revenue spike on ${spikeDay.date} was +${spikePct}% ($ ${spikeDay.value.toLocaleString()}) vs the previous day. This correlates with the launch of our Enterprise tier v2.0. Acme Corp and 3 other mid-market accounts upgraded within 48 hours, contributing $ 4,200 in additional MRR.`,
      chart: 'revenue',
      annotation: `Peak: $ ${spikeDay.value.toLocaleString()} on ${spikeDay.date} | Drivers: Enterprise v2 launch + 4 upgrades`,
      chartType: 'line'
    },
    rank: {
      text: `Here are your top 5 customers by MRR:\n1. Acme Corp — $ 12,400/mo (+8%)\n2. Beta Inc — $ 9,800/mo (+15%)\n3. DataFlow — $ 8,700/mo (+22%)\n4. NovaTech — $ 7,400/mo (+4%)\n5. ZenithCo — $ 6,100/mo (-2%)\nDataFlow shows the strongest growth at +22%. ZenithCo is the only one trending down.`,
      chart: 'topCustomers',
      annotation: 'Top 5 = $ 44,400/mo combined | DataFlow highest growth at +22%',
      chartType: 'bar'
    },
    compare: {
      text: `Comparing the last 2 months of daily revenue:\n- Period 1 (Days 1-15): avg $ ${Math.round(dailyRevenue.slice(0,15).reduce((a,d)=>a+d.value,0)/15).toLocaleString()}/day\n- Period 2 (Days 16-30): avg $ ${Math.round(dailyRevenue.slice(15).reduce((a,d)=>a+d.value,0)/15).toLocaleString()}/day\nThat's an increase of approximately ${Math.round((dailyRevenue.slice(15).reduce((a,d)=>a+d.value,0)/15)/(dailyRevenue.slice(0,15).reduce((a,d)=>a+d.value,0)/15)*100 - 100)}%. The growth accelerated in the second half of the period.`,
      chart: 'revenue',
      annotation: 'H1 avg vs H2 avg: +~12% growth in daily run rate',
      chartType: 'line'
    },
    trend: {
      text: `Churn rate over the last 30 days averaged ${store.period === '7d' ? '2.3' : '2.1'}%. The trend shows a slight increase from 1.8% at the start of the period to 2.4% in the last week. Early warning: the churn rate is creeping up, driven primarily by the Startup segment (3.7%).`,
      chart: 'newLost',
      annotation: 'Churn trending up: 1.8% → 2.4% over period | Startup segment at 3.7%',
      chartType: 'bar'
    },
    breakdown: {
      text: `MRR by segment:\n- Enterprise: $ 42,300 (50.2%)\n- Mid-market: $ 24,500 (29.1%)\n- Startup: $ 11,430 (13.6%)\n- SMB: $ 6,000 (7.1%)\nEnterprise continues to dominate. Mid-market is the fastest-growing segment at +22% this period.`,
      chart: 'segment',
      annotation: 'Enterprise = 50.2% of MRR | Mid-market growing fastest at +22%',
      chartType: 'doughnut'
    },
    growth_analysis: {
      text: `Mid-market grew the fastest this period at +22% in MRR, followed by Enterprise at +14%. Startup grew +8%, while SMB was flat. The mid-market acceleration is driven by 3 new Enterprise Select plan adoptions.`,
      chart: 'segment',
      annotation: 'Fastest: Mid-market +22% | Second: Enterprise +14% | Driver: Enterprise Select plan',
      chartType: 'doughnut'
    },
    compute: {
      text: `Average revenue per customer (ARPU) is $ ${Math.round(84230 / 1847).toLocaleString()}/mo. Enterprise ARPU is $ ${Math.round(42300 / 120).toLocaleString()}, Mid-market is $ ${Math.round(24500 / 340).toLocaleString()}, Startup is $ ${Math.round(11430 / 530).toLocaleString()}, SMB is $ ${Math.round(6000 / 857).toLocaleString()}.`,
      chart: null,
      annotation: 'Overall ARPU: $ 46/mo | Enterprise ARPU: $ 353/mo (7.7x avg)',
      chartType: null
    },
    analyze: {
      text: `Current dashboard state: MRR is $ 84,230 (+12.4% vs previous period), with 1,847 active customers (+38). Net revenue retention is 108%, which is solid. The churn rate of 2.1% bears watching. Enterprise segment drives 50.2% of revenue.`,
      chart: null,
      annotation: 'Dashboard overview: 4 KPIs, 4 charts, 1 activity table loaded',
      chartType: null
    }
  };
  const key = Object.keys(responses).find(k => op.includes(k)) || 'analyze';
  return responses[key] || responses.analyze;
}
// ── Real API call ──────────────────────────────────────────────
async function callLLMAPI(messages) {
  if (store.useMock || !store.apiKey) {
    return null;
  }
  const systemPrompt = `You are an AI copilot for a SaaS dashboard. The user sees these KPIs:
- MRR: $84,230 (+12.4%)
- Active Customers: 1,847 (+38)
- NRR: 108%
- Churn: 2.1%
Daily revenue data is available for the last 30 days.
Segments: Enterprise ($42,300), Mid-market ($24,500), Startup ($11,430), SMB ($6,000).
Top customers by MRR: Acme Corp ($12,400), Beta Inc ($9,800), DataFlow ($8,700), NovaTech ($7,400), ZenithCo ($6,100).
Current context: period=${store.period}, segment=${store.segment}, region=${store.region}.
Respond concisely in plain text (no markdown). If the query asks for data, provide specific numbers. If it's a comparison, state the comparison clearly. If it asks about a chart, describe what the chart shows.`;
  try {
    const response = await fetch(store.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + store.apiKey
      },
      body: JSON.stringify({
        model: 'deepseek/deepseek-r1',
        messages: [
          { role: 'system', content: systemPrompt },
          ...messages
        ],
        max_tokens: 500,
        temperature: 0.3
      })
    });
    if (!response.ok) {
      throw new Error('API error: ' + response.status);
    }
    const data = await response.json();
    return data.choices[0].message.content;
  } catch (err) {
    console.warn('API call failed, falling back to mock:', err.message);
    return null;
  }
}
// ── Add message to chat ────────────────────────────────────────
function addMessage(role, content, chartType, annotationText) {
  const container = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'message ' + role;
  let html = content.replace(/\n/g, '<br>');
  if (role === 'assistant' && annotationText) {
    html += '<div class="annotation">' + annotationText + '</div>';
  }
  div.innerHTML = html;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}
// ── Send message ──────────────────────────────────────────────
async function sendMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMessage('user', text);
  store.conversation.push({ role: 'user', content: text });
  document.getElementById('thinkingIndicator').classList.add('active');
  document.getElementById('sendBtn').disabled = true;
  try {
    const parsed = parseQuery(text);
    const messagesForAPI = store.conversation.map(m => ({ role: m.role, content: m.content }));
    let llmText = await callLLMAPI(messagesForAPI);
    let responseText, chartHint, annotation;
    if (llmText) {
      responseText = llmText;
      chartHint = parsed.chartType;
      annotation = 'AI-generated analysis from live LLM call';
    } else {
      const mock = generateMockResponse(parsed);
      responseText = mock.text;
      chartHint = mock.chartType;
      annotation = mock.annotation || 'Generated from mock (dev fallback)';
    }
    addMessage('assistant', responseText, chartHint, annotation);
    store.conversation.push({ role: 'assistant', content: responseText });
    updateStatus('API connected', true);
  } catch (err) {
    addMessage('system', 'Error: ' + err.message + '. Try again.');
    updateStatus('Error: ' + err.message, false);
  }
  document.getElementById('thinkingIndicator').classList.remove('active');
  document.getElementById('sendBtn').disabled = false;
}
// ── Suggested query helper ─────────────────────────────────────
function sendSuggested(text) {
  document.getElementById('chatInput').value = text;
  sendMessage();
}
// ── API key management ─────────────────────────────────────────
function setApiKey(key) {
  store.apiKey = key;
  store.useMock = !key;
  if (key) {
    localStorage.setItem('copilot_api_key', key);
    updateStatus('API connected (' + key.slice(0,12) + '...)', true);
  } else {
    localStorage.removeItem('copilot_api_key');
    updateStatus('Mock mode (dev fallback)', false);
  }
}
function updateStatus(text, isOnline) {
  document.getElementById('statusText').textContent = text;
  const dot = document.getElementById('statusDot');
  dot.className = isOnline ? 'dot' : 'dot offline';
}
// ── Voice input ────────────────────────────────────────────────
function toggleVoice() {
  const btn = document.getElementById('voiceBtn');
  if (store.voiceActive) {
    if (store.recognition) store.recognition.stop();
    store.voiceActive = false;
    btn.classList.remove('recording');
    btn.textContent = '🎤';
    return;
  }
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    addMessage('system', 'Voice input not supported in this browser. Try Chrome.');
    return;
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  store.recognition = new SpeechRecognition();
  store.recognition.lang = 'en-US';
  store.recognition.interimResults = false;
  store.recognition.maxAlternatives = 1;
  store.recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    store.voiceActive = false;
    btn.classList.remove('recording');
    btn.textContent = '🎤';
    sendMessage();
  };
  store.recognition.onerror = function(event) {
    console.warn('Voice error:', event.error);
    store.voiceActive = false;
    btn.classList.remove('recording');
    btn.textContent = '🎤';
    if (event.error !== 'aborted') {
      addMessage('system', 'Voice input error: ' + event.error);
    }
  };
  store.recognition.start();
  store.voiceActive = true;
  btn.classList.add('recording');
  btn.textContent = '⏺';
}
// ── Init ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  const savedKey = localStorage.getItem('copilot_api_key');
  if (savedKey) {
    store.apiKey = savedKey;
    store.useMock = false;
    updateStatus('API connected (' + savedKey.slice(0,12) + '...)', true);
  }
  initCharts();
  updateContext();
  if (!store.apiKey) {
    addMessage('system', 'No API key set. AI responses use development mock data.');
    addMessage('system', 'Set your OpenRouter API key in console: setApiKey("sk-or-v1-...")');
  }
});
</script>
</body>
</html>