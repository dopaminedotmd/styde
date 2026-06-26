```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>THE CRUCIBLE — AI Copilot Dashboard v5</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0c0f;color:#c0c8d4;font-family:'Inter',system-ui,-apple-system,sans-serif;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 380px;height:100vh;gap:0}
.main-panel{display:flex;flex-direction:column;padding:20px;overflow-y:auto;border-right:1px solid #1e2230}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid #1e2230}
.header h1{font-size:18px;font-weight:600;color:#e8edf5;letter-spacing:1px}
.header h1 span{color:#6c8cff}
.context-bar{display:flex;gap:12px;font-size:12px;color:#7a8499;align-items:center}
.context-badge{padding:4px 10px;border-radius:12px;background:#12161e;border:1px solid #1e2a3e;font-size:11px}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.metric-card{padding:16px;border-radius:10px;background:linear-gradient(135deg,#11161f,#0d1019);border:1px solid #1a2332;position:relative;overflow:hidden}
.metric-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,#6c8cff,transparent);opacity:.4}
.metric-label{font-size:11px;color:#5a6480;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.metric-value{font-size:24px;font-weight:700;color:#e8edf5;font-variant-numeric:tabular-nums}
.metric-change{font-size:11px;margin-top:4px}
.metric-change.up{color:#4caf7d}
.metric-change.down{color:#ef5350}
.charts-row{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:20px}
.chart-card{background:linear-gradient(135deg,#11161f,#0d1019);border:1px solid #1a2332;border-radius:10px;padding:16px;position:relative}
.chart-title{font-size:12px;color:#5a6480;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;display:flex;justify-content:space-between}
.chart-title .annotation{color:#6c8cff;font-size:10px;text-transform:none;letter-spacing:0;background:#0d1624;padding:2px 8px;border-radius:6px}
.chart-container{position:relative;height:200px}
.charts-row-2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px}
.insight-panel{background:linear-gradient(135deg,#0f1622,#0b0f1a);border:1px solid #1a2332;border-radius:10px;padding:14px 16px;margin-top:4px}
.insight-header{font-size:11px;color:#5a6480;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.insight-header .pulse{width:6px;height:6px;border-radius:50%;background:#6c8cff;animation:pulse 2s infinite}
@keyframes pulse{0%{opacity:1}50%{opacity:.3}100%{opacity:1}}
.insight-item{font-size:12px;color:#9aa5b9;padding:6px 0;border-bottom:1px solid #161e2e;display:flex;align-items:center;gap:8px;cursor:pointer;transition:color .2s}
.insight-item:last-child{border-bottom:none}
.insight-item:hover{color:#c0c8d4}
.insight-item .tag{background:#1a2640;padding:2px 6px;border-radius:4px;font-size:10px;color:#6c8cff}
/* Copilot Panel */
.copilot-panel{display:flex;flex-direction:column;height:100vh;background:#0a0c0f}
.copilot-header{padding:20px 20px 14px;border-bottom:1px solid #1e2230;display:flex;align-items:center;gap:10px}
.copilot-header .avatar{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#6c8cff,#4a6cdf);display:flex;align-items:center;justify-content:center;font-size:14px;color:#fff;font-weight:700}
.copilot-header .info{flex:1}
.copilot-header .info .name{font-size:13px;font-weight:600;color:#e8edf5}
.copilot-header .info .status{font-size:11px;color:#4caf7d}
.copilot-header .info .status::before{content:'';display:inline-block;width:6px;height:6px;border-radius:50%;background:#4caf7d;margin-right:5px;vertical-align:middle}
.copilot-context{display:flex;gap:6px;padding:10px 20px;background:#0d1019;border-bottom:1px solid #1e2230;flex-wrap:wrap}
.copilot-context .ctx-badge{font-size:10px;padding:3px 8px;border-radius:10px;background:#161e2e;border:1px solid #1a2a40;color:#7a8499}
.copilot-context .ctx-badge.active{border-color:#6c8cff;color:#6c8cff}
.chat-messages{flex:1;overflow-y:auto;padding:14px 20px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:92%;padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.5;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{background:#1a2640;color:#c0c8d4;align-self:flex-end;border-bottom-right-radius:2px}
.msg.copilot{background:#0f1624;color:#b0baca;align-self:flex-start;border-bottom-left-radius:2px;border:1px solid #1a2332}
.msg.copilot .chart-inline{width:100%;height:160px;margin:8px 0 4px;border-radius:6px;background:#080b12;position:relative;overflow:hidden}
.msg.copilot .chart-inline canvas{width:100%!important;height:100%!important}
.msg.copilot .annotation-text{font-size:11px;color:#7a8aa0;margin-top:4px;padding:6px 8px;background:#0d1524;border-radius:4px;border-left:2px solid #6c8cff}
.msg.copilot .callout{font-size:11px;color:#6c8cff;margin-top:4px}
.typing-indicator{display:flex;gap:4px;padding:8px 0}
.typing-indicator span{width:6px;height:6px;border-radius:50%;background:#5a6480;animation:bounce 1.2s infinite}
.typing-indicator span:nth-child(2){animation-delay:.2s}
.typing-indicator span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
.suggested-queries{display:flex;gap:6px;flex-wrap:wrap;padding:10px 20px;border-top:1px solid #1e2230}
.suggested-q{font-size:11px;padding:5px 10px;border-radius:12px;background:#121a2a;color:#7a8aa0;border:1px solid #1e2a3e;cursor:pointer;transition:all .2s}
.suggested-q:hover{background:#1a2640;color:#c0c8d4;border-color:#6c8cff}
.input-area{display:flex;gap:8px;padding:10px 20px 16px;border-top:1px solid #1e2230;background:#0d1019}
.input-area input{flex:1;padding:10px 14px;border-radius:8px;border:1px solid #1e2a3e;background:#0a0c12;color:#c0c8d4;font-size:13px;outline:none;transition:border .2s}
.input-area input:focus{border-color:#6c8cff}
.input-area input::placeholder{color:#3a4460}
.input-area button{padding:10px 16px;border-radius:8px;border:none;background:linear-gradient(135deg,#6c8cff,#4a6cdf);color:#fff;font-size:13px;font-weight:500;cursor:pointer;transition:opacity .2s}
.input-area button:hover{opacity:.85}
.input-area .voice-btn{width:38px;padding:10px;border-radius:8px;border:1px solid #1e2a3e;background:#0a0c12;color:#5a6480;cursor:pointer;text-align:center;font-size:14px}
.input-area .voice-btn:hover{border-color:#6c8cff;color:#6c8cff}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#0a0c0f}
::-webkit-scrollbar-thumb{background:#1e2a3e;border-radius:2px}
</style>
</head>
<body>
<div class="dashboard">
  <div class="main-panel">
    <div class="header">
      <h1>THE CRUCIBLE <span>v5</span></h1>
      <div class="context-bar">
        <span class="context-badge">Q2 2026</span>
        <span class="context-badge">Jun 1 – Jun 26</span>
        <span class="context-badge">All Products</span>
        <span class="context-badge" style="border-color:#6c8cff;color:#6c8cff">Copilot Active</span>
      </div>
    </div>
    <div class="metrics-row">
      <div class="metric-card"><div class="metric-label">MRR</div><div class="metric-value">$84,290</div><div class="metric-change up">+12.4% vs last month</div></div>
      <div class="metric-card"><div class="metric-label">Active Customers</div><div class="metric-value">312</div><div class="metric-change up">+8 vs yesterday</div></div>
      <div class="metric-card"><div class="metric-label">Revenue Today</div><div class="metric-value">$3,842</div><div class="metric-change up">+$412 vs Tue avg</div></div>
      <div class="metric-card"><div class="metric-label">Churn Rate</div><div class="metric-value">2.1%</div><div class="metric-change down">-0.3pp MTD</div></div>
    </div>
    <div class="charts-row">
      <div class="chart-card">
        <div class="chart-title">Revenue (7-Day) <span class="annotation">+14.2% WoW</span></div>
        <div class="chart-container"><canvas id="revenueChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Revenue by Product</div>
        <div class="chart-container"><canvas id="productChart"></canvas></div>
      </div>
    </div>
    <div class="charts-row-2">
      <div class="chart-card">
        <div class="chart-title">Customer Growth</div>
        <div class="chart-container"><canvas id="growthChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Avg Revenue Per Customer</div>
        <div class="chart-container"><canvas id="arpuChart"></canvas></div>
      </div>
    </div>
    <div class="insight-panel">
      <div class="insight-header"><span class="pulse"></span> AI Detected Anomalies</div>
      <div class="insight-item"><span class="tag">SPIKE</span> Revenue spike detected Tue Jun 23 (+32% vs 4wk avg) — 3 enterprise upgrades</div>
      <div class="insight-item"><span class="tag">DROP</span> API product usage down 18% since Jun 20 — investigate onboarding flow</div>
      <div class="insight-item"><span class="tag">TREND</span> Enterprise segment growing 2.3x faster than SMB this quarter</div>
    </div>
  </div>
  <div class="copilot-panel">
    <div class="copilot-header">
      <div class="avatar">AI</div>
      <div class="info">
        <div class="name">Dashboard Copilot</div>
        <div class="status">Context-aware</div>
      </div>
    </div>
    <div class="copilot-context">
      <span class="ctx-badge active">Q2 2026</span>
      <span class="ctx-badge active">Jun 1–26</span>
      <span class="ctx-badge active">All Products</span>
      <span class="ctx-badge">Enterprise</span>
      <span class="ctx-badge">SMB</span>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="msg copilot">
        I'm monitoring the dashboard. I see revenue up 14.2% WoW with a notable spike on Jun 23. Ask me anything about your data.
        <div class="callout">Try: 'What caused the revenue spike?' or 'Show top customers by MRR'</div>
      </div>
    </div>
    <div class="suggested-queries" id="suggestedQueries">
      <span class="suggested-q" data-query="What caused the revenue spike last Tuesday?">Revenue spike cause</span>
      <span class="suggested-q" data-query="Show top 5 customers by MRR">Top 5 by MRR</span>
      <span class="suggested-q" data-query="Compare this quarter to last quarter">QoQ comparison</span>
      <span class="suggested-q" data-query="Which product has the highest churn rate?">Highest churn product</span>
      <span class="suggested-q" data-query="Show revenue breakdown by segment">Revenue by segment</span>
    </div>
    <div class="input-area">
      <input type="text" id="chatInput" placeholder="Ask about your dashboard..." autofocus>
      <button id="sendBtn">Send</button>
      <div class="voice-btn" id="voiceBtn" title="Voice input (simulated)">🎤</div>
    </div>
  </div>
</div>
<script>
const ctx = document.getElementById('chatMessages');
const input = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const suggestedQs = document.querySelectorAll('.suggested-q');
const mockData = {
  mrr: 84290,
  customers: 312,
  churnRate: 2.1,
  revenueByDay: [2840, 3012, 2890, 3420, 5100, 3842, 3650].reverse(),
  revenueByProduct: { Core: 41200, API: 18900, Enterprise: 16500, Consulting: 7690 },
  growth: [278, 285, 291, 298, 305, 312],
  arpu: [270, 273, 278, 282, 280, 285],
  topCustomers: ['Acme Corp ($12.4k)', 'Globex Inc ($9.8k)', 'Initech ($8.2k)', 'Hooli ($7.6k)', 'Umbrella Corp ($6.1k)'],
  segments: { Enterprise: 38400, SMB: 28900, Startup: 16990 },
  spikeReason: '3 enterprise customers upgraded to Premium plan on Jun 23 (Acme Corp, Globex Inc, Initech). Combined +$4,200 MRR impact.'
};
function initCharts() {
  new Chart(document.getElementById('revenueChart'), {
    type: 'line',
    data: {
      labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      datasets: [{
        label: 'Revenue',
        data: mockData.revenueByDay,
        borderColor: '#6c8cff',
        backgroundColor: 'rgba(108,140,255,0.08)',
        fill: true,
        tension: .35,
        pointBackgroundColor: mockData.revenueByDay.map((v,i) => v === Math.max(...mockData.revenueByDay) ? '#ef5350' : '#6c8cff'),
        pointBorderColor: mockData.revenueByDay.map((v,i) => v === Math.max(...mockData.revenueByDay) ? '#ef5350' : '#6c8cff'),
        pointRadius: 4,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
        y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } }, beginAtZero: false }
      }
    }
  });
  new Chart(document.getElementById('productChart'), {
    type: 'doughnut',
    data: {
      labels: Object.keys(mockData.revenueByProduct),
      datasets: [{
        data: Object.values(mockData.revenueByProduct),
        backgroundColor: ['#6c8cff', '#4caf7d', '#ff9800', '#ab47bc'],
        borderColor: '#0a0c0f',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#7a8499', font: { size: 10 }, padding: 8 } }
      }
    }
  });
  new Chart(document.getElementById('growthChart'), {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Customers',
        data: mockData.growth,
        backgroundColor: 'rgba(76,175,125,0.5)',
        borderColor: '#4caf7d',
        borderWidth: 1,
        borderRadius: 3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#5a6480', font: { size: 10 } } },
        y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } }
      }
    }
  });
  new Chart(document.getElementById('arpuChart'), {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'ARPU',
        data: mockData.arpu,
        borderColor: '#ff9800',
        backgroundColor: 'rgba(255,152,0,0.06)',
        fill: true,
        tension: .3,
        pointBackgroundColor: '#ff9800',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
        y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } }
      }
    }
  });
}
document.addEventListener('DOMContentLoaded', initCharts);
function addCopilotChart(query, chartConfig, annotationText) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'msg copilot';
  const chartId = 'inlineChart_' + Date.now();
  msgDiv.innerHTML = `<div style="margin-bottom:6px;color:#c0c8d4">${query}</div>
    <div class="chart-inline"><canvas id="${chartId}"></canvas></div>
    <div class="annotation-text">${annotationText}</div>`;
  ctx.appendChild(msgDiv);
  ctx.scrollTop = ctx.scrollHeight;
  setTimeout(() => {
    const cvs = document.getElementById(chartId);
    if (cvs) new Chart(cvs, chartConfig);
  }, 50);
}
function addCopilotText(text, annotation) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'msg copilot';
  let html = text;
  if (annotation) html += `<div class="callout">${annotation}</div>`;
  msgDiv.innerHTML = html;
  ctx.appendChild(msgDiv);
  ctx.scrollTop = ctx.scrollHeight;
}
function addUserMessage(text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'msg user';
  msgDiv.textContent = text;
  ctx.appendChild(msgDiv);
  ctx.scrollTop = ctx.scrollHeight;
}
function showTyping() {
  const div = document.createElement('div');
  div.className = 'typing-indicator';
  div.id = 'typing';
  div.innerHTML = '<span></span><span></span><span></span>';
  ctx.appendChild(div);
  ctx.scrollTop = ctx.scrollHeight;
}
function hideTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}
function processQuery(query) {
  addUserMessage(query);
  showTyping();
  setTimeout(() => {
    hideTyping();
    const q = query.toLowerCase();
    if (q.includes('spike') || (q.includes('revenue') && q.includes('tuesday'))) {
      addCopilotChart(
        'Revenue spike on Tuesday Jun 23 analyzed',
        {
          type: 'bar',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
              label: 'Revenue',
              data: [3012, 5100, 3420, 3842, 3650],
              backgroundColor: ['#5a6480','#ef5350','#5a6480','#5a6480','#5a6480'],
              borderColor: ['#5a6480','#ef5350','#5a6480','#5a6480','#5a6480'],
              borderWidth: 1, borderRadius: 3
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              annotation: { annotations: {} }
            },
            scales: {
              x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
              y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } }
            }
          }
        },
        mockData.spikeReason
      );
    } else if (q.includes('top') && (q.includes('customer') || q.includes('mrr'))) {
      let list = mockData.topCustomers.map(c => '  ' + c).join('\n');
      addCopilotText(
        `Top 5 customers by MRR (${new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:0}).format(mockData.mrr)} total):\n\n${list}\n\nConcentration: top 5 represent 52% of total MRR.`,
        'Suggestion: drill into Acme Corp lifecycle - they upgraded 3 seats on Jun 23'
      );
    } else if (q.includes('compare') && (q.includes('quarter') || q.includes('qoq'))) {
      addCopilotChart(
        'Q2 vs Q1 Comparison',
        {
          type: 'bar',
          data: {
            labels: ['MRR', 'Customers', 'ARPU', 'Revenue'],
            datasets: [
              { label: 'Q1 2026', data: [72300, 278, 260, 210000], backgroundColor: '#3a4460', borderRadius: 3 },
              { label: 'Q2 2026', data: [84290, 312, 285, 258000], backgroundColor: '#6c8cff', borderRadius: 3 }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
              legend: { position: 'top', labels: { color: '#7a8499', font: { size: 10 } } }
            },
            scales: {
              x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
              y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } }
            }
          }
        },
        'Q2 outperforming Q1 across all metrics. MRR growth: +16.6%. Customer growth: +12.2%. ARPU: +9.6%. Revenue run-rate trending 22.8% higher.'
      );
    } else if (q.includes('churn') || q.includes('product') && q.includes('highest')) {
      addCopilotChart(
        'Product Churn Rates',
        {
          type: 'bar',
          data: {
            labels: ['API', 'Core', 'Enterprise', 'Consulting'],
            datasets: [{
              label: 'Churn Rate %',
              data: [4.8, 2.1, 0.9, 3.2],
              backgroundColor: ['#ef5350','#ff9800','#4caf7d','#ab47bc'],
              borderRadius: 3
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
              y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } }, beginAtZero: true }
            }
          }
        },
        'API product has highest churn at 4.8% — investigate onboarding flow. Enterprise lowest at 0.9% sticky due to contract terms.'
      );
    } else if (q.includes('segment') || q.includes('breakdown') || q.includes('by')) {
      const total = Object.values(mockData.segments).reduce((a,b) => a+b, 0);
      addCopilotChart(
        `Revenue by Segment (${new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(total)} total)`,
        {
          type: 'pie',
          data: {
            labels: Object.keys(mockData.segments),
            datasets: [{
              data: Object.values(mockData.segments),
              backgroundColor: ['#6c8cff','#4caf7d','#ff9800'],
              borderColor: '#0a0c0f',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom', labels: { color: '#7a8499', font: { size: 10 }, padding: 8 } }
            }
          }
        },
        'Enterprise leads at 45.5% of revenue (growing 2.3x faster than SMB). Startup segment flat MoM — potential upsell opportunity.'
      );
    } else {
      addCopilotChart(
        'Revenue Trend Analysis',
        {
          type: 'line',
          data: {
            labels: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
            datasets: [{
              label: 'Revenue',
              data: mockData.revenueByDay,
              borderColor: '#6c8cff',
              backgroundColor: 'rgba(108,140,255,0.06)',
              fill: true,
              tension: .35,
              pointBackgroundColor: '#6c8cff',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } },
              y: { grid: { color: '#161e2e' }, ticks: { color: '#5a6480', font: { size: 10 } } }
            }
          }
        },
        'Current 7-day trend shows +14.2% WoW growth. Tuesday spike driven by enterprise upgrades. Weekend dip expected — typical B2B pattern.'
      );
    }
  }, 600);
}
sendBtn.addEventListener('click', () => {
  const text = input.value.trim();
  if (!text) return;
  processQuery(text);
  input.value = '';
});
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    sendBtn.click();
  }
});
suggestedQs.forEach(el => {
  el.addEventListener('click', () => {
    processQuery(el.dataset.query);
  });
});
voiceBtn.addEventListener('click', () => {
  voiceBtn.style.color = '#6c8cff';
  voiceBtn.textContent = '...';
  setTimeout(() => {
    const phrases = [
      'Show top 5 customers by MRR',
      'What caused the revenue spike last Tuesday?',
      'Compare this quarter to last quarter',
    ];
    const picked = phrases[Math.floor(Math.random() * phrases.length)];
    voiceBtn.textContent = '🎤';
    voiceBtn.style.color = '#5a6480';
    processQuery(picked);
  }, 1200);
});
setTimeout(() => {
  const anomalyEls = document.querySelectorAll('.insight-item');
  anomalyEls.forEach((el, i) => {
    el.addEventListener('click', () => {
      const queries = [
        'What caused the revenue spike last Tuesday?',
        'Which product has the highest churn rate?',
        'Compare this quarter to last quarter'
      ];
      if (queries[i]) processQuery(queries[i]);
    });
  });
}, 500);
</script>
</body>
</html>
```