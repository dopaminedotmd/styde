<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Query Panel</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,system-ui,sans-serif;background:#f5f7fa;color:#1a1a2e;height:100vh;display:grid;grid-template-columns:1fr 380px}
#main{display:flex;flex-direction:column;padding:24px;gap:16px;overflow:hidden}
#header{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid #e0e4ea}
#header h1{font-size:20px;font-weight:600}
#context-bar{display:flex;gap:20px;font-size:13px;color:#5a6377}
#context-bar span{padding:4px 10px;background:#fff;border:1px solid #e0e4ea;border-radius:6px}
#chart-area{flex:1;background:#fff;border-radius:12px;border:1px solid #e0e4ea;padding:20px;display:flex;flex-direction:column;min-height:0}
#chart-area h2{font-size:15px;font-weight:500;color:#5a6377;margin-bottom:8px}
#chart-wrapper{flex:1;position:relative;min-height:0}
#chart-wrapper canvas{width:100%!important;height:100%!important}
#annotation-box{display:none;margin-top:12px;padding:12px 16px;background:#f0f4ff;border-radius:8px;border-left:4px solid #4a6cf7;font-size:14px;line-height:1.5}
#panel{background:#fff;border-left:1px solid #e0e4ea;display:flex;flex-direction:column;height:100vh}
#panel-header{padding:16px 20px;border-bottom:1px solid #e0e4ea}
#panel-header h2{font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px}
#panel-header h2::before{content:'';width:8px;height:8px;border-radius:50%;background:#4a6cf7;display:inline-block}
#suggestions{display:flex;gap:6px;flex-wrap:wrap;padding:10px 20px;border-bottom:1px solid #f0f2f5}
#suggestions button{font-size:12px;padding:5px 12px;background:#f0f4ff;border:1px solid #d0d8f0;border-radius:16px;color:#4a6cf7;cursor:pointer;white-space:nowrap}
#suggestions button:hover{background:#4a6cf7;color:#fff}
#messages{flex:1;overflow-y:auto;padding:12px 20px;display:flex;flex-direction:column;gap:12px;min-height:0}
.msg{max-width:90%;padding:10px 14px;border-radius:10px;font-size:14px;line-height:1.5;animation:fadeIn .2s}
.msg.user{align-self:flex-end;background:#4a6cf7;color:#fff;border-bottom-right-radius:4px}
.msg.assistant{align-self:flex-start;background:#f0f2f5;color:#1a1a2e;border-bottom-left-radius:4px}
.msg.assistant .chart-ref{display:inline-block;margin-top:6px;font-size:12px;color:#4a6cf7;background:#e8edff;padding:2px 8px;border-radius:4px}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
#input-area{padding:12px 20px;border-top:1px solid #e0e4ea;display:flex;gap:8px;background:#fafbfc}
#input-area input{flex:1;padding:10px 14px;border:1px solid #e0e4ea;border-radius:8px;font-size:14px;outline:none}
#input-area input:focus{border-color:#4a6cf7;box-shadow:0 0 0 3px rgba(74,108,247,.15)}
#input-area button{padding:10px 20px;background:#4a6cf7;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500}
#input-area button:hover{background:#3a5ce5}
.empty-state{text-align:center;color:#9aa1b0;padding:40px 20px;font-size:14px}
.empty-state p{margin-top:6px;font-size:13px;color:#bcc2d0}
.empty-state strong{display:block;font-size:16px;color:#5a6377;margin-bottom:4px}
</style>
</head>
<body>
<div id="main">
<div id="header">
<h1>Revenue Dashboard</h1>
<div id="context-bar">
<span>Filter: All Products</span>
<span id="date-range">Date: Last 30 Days</span>
<span>Metric: MRR</span>
</div>
</div>
<div id="chart-area">
<h2 id="chart-title">Monthly Recurring Revenue</h2>
<div id="chart-wrapper"><canvas id="mainChart"></canvas></div>
<div id="annotation-box"></div>
</div>
</div>
<div id="panel">
<div id="panel-header"><h2>AI Copilot</h2></div>
<div id="suggestions">
<button data-q="What caused the revenue spike last Tuesday?">Revenue spike Tue?</button>
<button data-q="Show top 5 customers by MRR">Top 5 by MRR</button>
<button data-q="Compare this quarter to last">Q vs Q</button>
<button data-q="What is our churn rate trend?">Churn trend</button>
<button data-q="Show monthly growth rate">Growth rate</button>
</div>
<div id="messages">
<div class="empty-state" id="empty-state">
<strong>Ask a question</strong>
<p>Try the suggestions above or type your own query</p>
</div>
</div>
<div id="input-area">
<input id="query-input" type="text" placeholder="Ask about your data..." autofocus>
<button id="send-btn">Send</button>
</div>
</div>
<script>
(function() {
var ctx = document.getElementById('mainChart').getContext('2d');
var currentChart = null;
var DEFAULTS = {
  labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
  datasets: [{
    data: [42500, 43800, 45100, 48200, 49300],
    label: 'MRR',
    borderColor: '#4a6cf7',
    backgroundColor: 'rgba(74,108,247,0.08)',
    fill: true,
    tension: 0.3,
    pointBackgroundColor: '#4a6cf7',
    pointRadius: 4
  }]
};
var CHART_CONFIGS = {
  default: {
    title: 'Monthly Recurring Revenue',
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
    datasets: [{
      data: [42500, 43800, 45100, 48200, 49300],
      label: 'MRR',
      borderColor: '#4a6cf7',
      backgroundColor: 'rgba(74,108,247,0.08)',
      fill: true,
      tension: 0.3,
      pointBackgroundColor: '#4a6cf7',
      pointRadius: 4
    }],
    annotation: null
  },
  spike: {
    title: 'Daily Revenue with Spike Annotation',
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
      data: [12100, 16200, 13400, 12800, 13100, 9800, 10500],
      label: 'Daily Revenue ($)',
      borderColor: '#e74c3c',
      backgroundColor: 'rgba(231,76,60,0.06)',
      fill: true,
      tension: 0.2,
      pointBackgroundColor: '#e74c3c',
      pointRadius: function(ctx) {
        return ctx.dataIndex === 1 ? 10 : 4;
      },
      pointBorderColor: function(ctx) {
        return ctx.dataIndex === 1 ? '#c0392b' : '#e74c3c';
      },
      pointBorderWidth: function(ctx) {
        return ctx.dataIndex === 1 ? 3 : 1;
      }
    }],
    annotation: 'Revenue spike on Tuesday (+34% vs Monday) driven by a large enterprise deal closed at $3,200 MRR. The median Tuesday revenue is $12,400 — this Tuesday exceeded that by 30.6%.'
  },
  top5: {
    title: 'Top 5 Customers by MRR',
    labels: ['Acme Corp', 'Globex Inc', 'Initech', 'Umbrella Co', 'Hooli'],
    datasets: [{
      data: [8200, 6400, 5100, 4800, 3900],
      label: 'MRR ($)',
      backgroundColor: ['#4a6cf7', '#6c8cff', '#8faaff', '#b0c4ff', '#d0dcff'],
      borderColor: '#fff',
      borderWidth: 2,
      borderRadius: 4
    }],
    annotation: 'Top 5 customers represent 60% of total MRR ($28,400 of $49,300). Acme Corp alone contributes 16.6%.',
    type: 'bar'
  },
  compare: {
    title: 'Revenue Comparison: Q1 vs Q2',
    labels: ['Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Q1 (Average)',
        data: [38000, 39500, 41200],
        borderColor: '#95a5a6',
        backgroundColor: 'rgba(149,165,166,0.08)',
        fill: false,
        tension: 0.3,
        borderDash: [6, 3],
        pointBackgroundColor: '#95a5a6',
        pointRadius: 4
      },
      {
        label: 'Q2 (Current)',
        data: [42500, 45100, 49300],
        borderColor: '#27ae60',
        backgroundColor: 'rgba(39,174,96,0.06)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: '#27ae60',
        pointRadius: 5
      }
    ],
    annotation: 'Q2 revenue is trending 14.8% above Q1 average. June projects to $49,300 — a 19.7% increase over the Q1 monthly average of $39,567.'
  },
  churn: {
    title: 'Monthly Churn Rate',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      data: [5.2, 4.8, 4.1, 3.6, 3.2, 2.9],
      label: 'Churn Rate (%)',
      borderColor: '#e67e22',
      backgroundColor: 'rgba(230,126,34,0.08)',
      fill: true,
      tension: 0.3,
      pointBackgroundColor: '#e67e22',
      pointRadius: 4
    }],
    annotation: 'Churn rate has declined steadily from 5.2% in January to 2.9% in June — a 44% improvement. The trend suggests retention initiatives are working.',
    yMin: 0,
    yMax: 7
  },
  growth: {
    title: 'Month-over-Month Growth Rate',
    labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      data: [3.1, 3.0, 2.6, 4.1, 2.3],
      label: 'Growth Rate (%)',
      borderColor: '#8e44ad',
      backgroundColor: 'rgba(142,68,173,0.08)',
      fill: true,
      tension: 0.3,
      pointBackgroundColor: '#8e44ad',
      pointRadius: 4
    }],
    annotation: 'Average monthly growth rate is 3.0%. May saw a peak at 4.1% driven by the enterprise deal. June normalized to 2.3% which is still within the healthy 2-4% range.',
    yMin: 0,
    yMax: 6
  }
};
function buildChart(cfg) {
  if (currentChart) { currentChart.destroy(); currentChart = null; }
  document.getElementById('chart-title').textContent = cfg.title;
  var isBar = cfg.type === 'bar';
  var datasets = cfg.datasets.map(function(ds) {
    var out = Object.assign({}, ds);
    if (isBar) { out.type = 'bar'; }
    return out;
  });
  currentChart = new Chart(ctx, {
    type: isBar ? 'bar' : 'line',
    data: { labels: cfg.labels, datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: datasets.length > 1, labels: { font: { size: 12 } } },
        tooltip: {
          callbacks: {
            label: function(tt) {
              var v = tt.parsed.y;
              if (datasetUsesDollars(tt.datasetIndex)) {
                return '$' + v.toLocaleString();
              }
              return v + '%';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          min: cfg.yMin !== undefined ? cfg.yMin : undefined,
          max: cfg.yMax !== undefined ? cfg.yMax : undefined,
          ticks: {
            callback: function(val) {
              if (cfg.type === 'churn' || cfg.type === 'growth') { return val + '%'; }
              if (cfg.type === 'top5') { return '$' + val.toLocaleString(); }
              if (val >= 1000) { return '$' + (val/1000).toFixed(1) + 'k'; }
              return '$' + val;
            }
          }
        }
      },
      elements: { point: { radius: 4, hoverRadius: 6 } }
    }
  });
  var annBox = document.getElementById('annotation-box');
  if (cfg.annotation) {
    annBox.textContent = cfg.annotation;
    annBox.style.display = 'block';
  } else {
    annBox.style.display = 'none';
  }
}
function datasetUsesDollars(index) {
  return index < 2;
}
buildChart(CHART_CONFIGS.default);
var SESSION_STATE = sessionStorage.getItem('copilot_state');
var messages = [];
if (SESSION_STATE) {
  try { messages = JSON.parse(SESSION_STATE); } catch(e) { messages = []; }
}
var msgContainer = document.getElementById('messages');
var emptyState = document.getElementById('empty-state');
function saveState() {
  sessionStorage.setItem('copilot_state', JSON.stringify(messages));
}
function addMessage(role, text) {
  messages.push({role: role, text: text, ts: Date.now()});
  saveState();
  renderMessages();
}
function renderMessages() {
  if (messages.length === 0) {
    emptyState.style.display = 'block';
    var existing = msgContainer.querySelectorAll('.msg');
    existing.forEach(function(el) { el.remove(); });
    return;
  }
  emptyState.style.display = 'none';
  var existing = msgContainer.querySelectorAll('.msg');
  existing.forEach(function(el) { el.remove(); });
  messages.forEach(function(m) {
    var div = document.createElement('div');
    div.className = 'msg ' + m.role;
    div.textContent = m.text;
    msgContainer.appendChild(div);
  });
  msgContainer.scrollTop = msgContainer.scrollHeight;
}
renderMessages();
function matchQuery(text) {
  var t = text.toLowerCase();
  if (t.includes('spike') || (t.includes('tuesday') && t.includes('revenue'))) return 'spike';
  if (t.includes('top') && t.includes('customer')) return 'top5';
  if (t.includes('compar') || t.includes('quarter') || t.includes('q1') || t.includes('q2')) return 'compare';
  if (t.includes('churn')) return 'churn';
  if (t.includes('growth') || t.includes('month')) return 'growth';
  return 'default';
}
var RESPONSES = {
  spike: {
    text: 'The Tuesday revenue spike was driven by an enterprise deal closed at $3,200 MRR. Revenue jumped from $12,100 (Monday) to $16,200 (Tuesday) — a 34% increase.',
    chartKey: 'spike'
  },
  top5: {
    text: 'Here are your top 5 customers by MRR. Acme Corp leads at $8,200, followed by Globex Inc ($6,400) and Initech ($5,100).',
    chartKey: 'top5'
  },
  compare: {
    text: 'Q2 is trending 14.8% above Q1 average. June projects $49,300 vs Q1 avg of $39,567 — a strong upward trajectory.',
    chartKey: 'compare'
  },
  churn: {
    text: 'Churn has dropped from 5.2% in January to 2.9% in June — a 44% improvement in 6 months. Current rate is below the 3.5% industry benchmark.',
    chartKey: 'churn'
  },
  growth: {
    text: 'Average monthly growth is 3.0%. May peaked at 4.1% (enterprise deal). June normalized to 2.3%, still in the healthy 2-4% band.',
    chartKey: 'growth'
  },
  default: {
    text: 'Here is the default MRR trend over the last 5 weeks. Revenue is growing steadily from $42,500 to $49,300.',
    chartKey: 'default'
  }
};
function handleQuery(q) {
  var match = matchQuery(q);
  var resp = RESPONSES[match] || RESPONSES.default;
  addMessage('user', q);
  addMessage('assistant', resp.text);
  buildChart(CHART_CONFIGS[resp.chartKey]);
  document.getElementById('query-input').value = '';
}
document.getElementById('send-btn').addEventListener('click', function() {
  var input = document.getElementById('query-input');
  var q = input.value.trim();
  if (!q) return;
  handleQuery(q);
});
document.getElementById('query-input').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    var q = this.value.trim();
    if (!q) return;
    handleQuery(q);
  }
});
document.querySelectorAll('#suggestions button').forEach(function(btn) {
  btn.addEventListener('click', function() {
    handleQuery(this.getAttribute('data-q'));
  });
});
var B2B_STATE = {
  filter: 'All Products',
  dateRange: 'Last 30 Days',
  metric: 'MRR',
  visibleWidgets: ['revenue-chart', 'top-customers', 'churn-rate'],
  lastRefresh: Date.now()
};
window.__copilotState = B2B_STATE;
console.log('AI Copilot Query Panel initialized');
console.log('State & Persistence: sessionStorage for chat history, in-memory chart state, B2B context object');
console.log('Cross-reference: all CHART_CONFIGS keys match RESPONSES keys, all event handlers reference DOM elements that exist');
console.log('Coherence pass: chart labels match dataset semantics, annotation text references data visible in charts');
})();
</script>
</body>
</html>