I will output the complete HTML dashboard directly as plain text.
AI Copilot Query Panel - Complete Dashboard
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Query Panel - Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,-apple-system,sans-serif}
body{background:#0a0e17;color:#e0e6ed;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 380px;height:100vh}
.main-panel{padding:20px;overflow-y:auto;display:flex;flex-direction:column}
.header{display:flex;justify-content:space-between;align-items:center;padding:0 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px}
.header h1{font-size:22px;font-weight:600;color:#f0f4f8}
.header .badge{background:#2d7a4a;color:#b7f0c3;font-size:11px;padding:3px 10px;border-radius:12px;font-weight:500}
.filters-bar{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.filter-group{display:flex;flex-direction:column;gap:4px}
.filter-group label{font-size:11px;color:#7a8a9e;text-transform:uppercase;letter-spacing:0.5px}
.filter-group select,.filter-group input{background:#121a28;border:1px solid #1e2a3a;color:#e0e6ed;padding:6px 10px;border-radius:6px;font-size:13px;outline:none}
.filter-group select:focus,.filter-group input:focus{border-color:#4a7cf7}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.metric-card{background:#0f1724;border:1px solid #1e2a3a;border-radius:10px;padding:16px;transition:border-color 0.2s}
.metric-card:hover{border-color:#2a3a5a}
.metric-card .label{font-size:12px;color:#7a8a9e;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.4px}
.metric-card .value{font-size:28px;font-weight:700;color:#f0f4f8}
.metric-card .delta{font-size:12px;margin-top:4px;display:flex;align-items:center;gap:4px}
.delta.up{color:#4ade80}
.delta.down{color:#f87171}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0}
.chart-container{background:#0f1724;border:1px solid #1e2a3a;border-radius:10px;padding:16px;position:relative}
.chart-container h3{font-size:13px;color:#7a8a9e;margin-bottom:12px;font-weight:500;text-transform:uppercase;letter-spacing:0.4px}
.chart-wrapper{position:relative;height:200px}
.chart-full{grid-column:1/-1}
.chart-full .chart-wrapper{height:240px}
.copilot-panel{background:#0c1120;border-left:1px solid #1e2a3a;display:flex;flex-direction:column;height:100vh}
.copilot-header{padding:16px 16px 12px;border-bottom:1px solid #1e2a3a;display:flex;justify-content:space-between;align-items:center}
.copilot-header h2{font-size:16px;font-weight:600;color:#f0f4f8;display:flex;align-items:center;gap:8px}
.copilot-header h2 span{font-size:10px;background:#2d4a7a;color:#8ab4f8;padding:2px 8px;border-radius:10px;font-weight:400}
.context-badge{background:#1a2540;color:#7a9ad8;font-size:11px;padding:3px 10px;border-radius:10px;display:inline-block;margin-top:4px}
.chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px}
.message{max-width:92%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;animation:fadeIn 0.25s ease}
.message.user{background:#1a4a8a;color:#e0edff;align-self:flex-end;border-bottom-right-radius:4px}
.message.assistant{background:#162033;color:#d0dae8;align-self:flex-start;border-bottom-left-radius:4px;border:1px solid #1e2a3a}
.message.assistant .chart-mini{margin-top:8px;background:#0a1120;border-radius:8px;padding:8px;border:1px solid #1e2a3a}
.message.assistant .chart-mini canvas{width:100%!important;height:120px!important}
.message.assistant .insight-text{margin-top:6px;padding:6px 10px;background:#0f1a2e;border-left:3px solid #4a7cf7;border-radius:4px;font-size:12px;color:#b0c4e0}
.suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:8px 16px 4px}
.suggestion-chip{background:#162033;border:1px solid #1e2a3a;color:#8ab4f8;padding:6px 12px;border-radius:16px;font-size:12px;cursor:pointer;transition:all 0.2s}
.suggestion-chip:hover{background:#1e3050;border-color:#4a7cf7}
.input-area{border-top:1px solid #1e2a3a;padding:12px 16px 16px}
.input-row{display:flex;gap:8px;background:#121a28;border:1px solid #1e2a3a;border-radius:10px;padding:4px;transition:border-color 0.2s}
.input-row:focus-within{border-color:#4a7cf7}
.input-row input{flex:1;background:transparent;border:none;color:#e0e6ed;padding:8px 12px;font-size:13px;outline:none}
.input-row input::placeholder{color:#4a5a7a}
.input-row button{background:#4a7cf7;border:none;color:#fff;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:500;transition:background 0.2s}
.input-row button:hover{background:#3a6ae6}
.input-row button:disabled{background:#2a3a5a;color:#5a6a8a;cursor:not-allowed}
.voice-btn{background:transparent;border:1px solid #1e2a3a;color:#7a8a9e;padding:8px 10px;border-radius:8px;cursor:pointer;font-size:14px;transition:all 0.2s}
.voice-btn:hover{background:#1e2a3a;border-color:#4a7cf7}
.voice-btn.recording{background:#7a2a2a;border-color:#f87171;color:#f87171;animation:pulse 1.2s infinite}
.typing-indicator{display:flex;gap:4px;padding:10px 14px;align-items:center}
.typing-indicator span{width:6px;height:6px;background:#4a7cf7;border-radius:50%;animation:bounce 1.4s infinite}
.typing-indicator span:nth-child(2){animation-delay:0.2s}
.typing-indicator span:nth-child(3){animation-delay:0.4s}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-8px)}}
.blink-alert{animation:blinkAlert 2s infinite}
@keyframes blinkAlert{0%,100%{opacity:1}50%{opacity:0.3}}
.timestamp-refresh{font-size:10px;color:#4a5a7a;text-align:right;padding:2px 0}
</style>
</head>
<body>
<div class="dashboard">
<div class="main-panel">
  <div class="header">
    <h1>Styde Operations Dashboard</h1>
    <span class="badge">live</span>
  </div>
  <div class="filters-bar">
    <div class="filter-group">
      <label>Date Range</label>
      <select id="dateRange">
        <option>Last 7 days</option>
        <option selected>Last 30 days</option>
        <option>This quarter</option>
        <option>Year to date</option>
      </select>
    </div>
    <div class="filter-group">
      <label>Region</label>
      <select id="regionFilter">
        <option>All Regions</option>
        <option>NA</option>
        <option>EMEA</option>
        <option>APAC</option>
      </select>
    </div>
    <div class="filter-group">
      <label>Product</label>
      <select id="productFilter">
        <option>All Products</option>
        <option>Core</option>
        <option>Pro</option>
        <option>Enterprise</option>
      </select>
    </div>
  </div>
  <div class="metrics-row" id="metricsRow">
    <div class="metric-card">
      <div class="label">MRR</div>
      <div class="value" id="mrrValue">$284,512</div>
      <div class="delta up">+12.4% vs last period</div>
    </div>
    <div class="metric-card">
      <div class="label">Active Users</div>
      <div class="value" id="usersValue">8,247</div>
      <div class="delta up">+5.2% vs last period</div>
    </div>
    <div class="metric-card">
      <div class="label">Avg Response Time</div>
      <div class="value" id="responseValue">1.8s</div>
      <div class="delta down">-0.3s vs last period</div>
    </div>
    <div class="metric-card">
      <div class="label">Error Rate</div>
      <div class="value" id="errorValue">0.47%</div>
      <div class="delta up">+0.08% vs last period</div>
    </div>
  </div>
  <div class="charts-grid">
    <div class="chart-container chart-full">
      <h3>Revenue Trend (Last 30 Days)</h3>
      <div class="chart-wrapper"><canvas id="revenueChart"></canvas></div>
    </div>
    <div class="chart-container">
      <h3>Revenue by Region</h3>
      <div class="chart-wrapper"><canvas id="regionChart"></canvas></div>
    </div>
    <div class="chart-container">
      <h3>Top Customers by MRR</h3>
      <div class="chart-wrapper"><canvas id="topCustomersChart"></canvas></div>
    </div>
  </div>
  <div class="timestamp-refresh" id="refreshIndicator">Last updated: just now</div>
</div>
<div class="copilot-panel">
  <div class="copilot-header">
    <div>
      <h2>AI Copilot <span>context-aware</span></h2>
      <div class="context-badge" id="contextBadge">Filters: Last 30 days, All Regions, All Products</div>
    </div>
  </div>
  <div class="suggestions" id="suggestionsBar">
    <div class="suggestion-chip" data-query="What caused the revenue spike last Tuesday?">Revenue spike last Tuesday</div>
    <div class="suggestion-chip" data-query="Show top 5 customers by MRR">Top 5 customers by MRR</div>
    <div class="suggestion-chip" data-query="Compare this quarter to last quarter">Compare this quarter to last</div>
    <div class="suggestion-chip" data-query="Which region grew the most?">Which region grew most?</div>
  </div>
  <div class="chat-messages" id="chatMessages">
    <div class="message assistant">
      Hello, I'm your Styde Copilot. Ask me anything about your data — revenue, users, trends, comparisons. I see you're viewing Last 30 days across all regions and products.
    </div>
  </div>
  <div class="input-area">
    <div class="input-row">
      <input type="text" id="queryInput" placeholder="Ask a question about your data..." autocomplete="off">
      <button class="voice-btn" id="voiceBtn" title="Voice input">🎤</button>
      <button id="sendBtn">Send</button>
    </div>
  </div>
</div>
</div>
<script>
(function(){
const CHARTS = {};
let chartInstances = {};
let messageCount = 0;
const mockData = {
  dailyRevenue: [128400,132100,125900,131200,138500,142100,139800,135600,141200,147800,152300,148900,145600,151200,158400,162100,159800,155600,161200,168500,172100,169800,175600,182100,178900,185200,192300,188600,195100,201400],
  dates: Array.from({length:30},(_,i)=>{const d=new Date();d.setDate(d.getDate()-29+i);return d.toLocaleDateString('en-US',{month:'short',day:'numeric'})}),
  regionRevenue:{NA:425000,EMEA:285000,APAC:172000},
  topCustomers:[
    {name:'Acme Corp',mrr:48500},
    {name:'Globex Inc',mrr:42100},
    {name:'Initech',mrr:38900},
    {name:'Hooli',mrr:35200},
    {name:'Umbrella Co',mrr:31800}
  ],
  weeklyComparison:{thisQ:[284512,291300,298100,305400],lastQ:[252100,258400,265200,272100]},
  unusualEvents:{
    '2026-06-24':{reason:'Enterprise deal closed with Globex Inc ($42K MRR)',impact:42100,metric:'mrr'},
    '2026-06-17':{reason:'Feature launch: AI Copilot v2 drove 18% user growth',impact:0.18,metric:'users'},
    '2026-06-10':{reason:'EMEA region campaign: 22% traffic increase, 15% conversion lift',impact:0.15,metric:'conversion'}
  }
};
function initMainCharts(){
  const revCtx = document.getElementById('revenueChart').getContext('2d');
  chartInstances.revenue = new Chart(revCtx, {
    type: 'line', data: {
      labels: mockData.dates,
      datasets: [{
        label: 'Revenue ($)',
        data: mockData.dailyRevenue,
        borderColor: '#4a7cf7',
        backgroundColor: 'rgba(74,124,247,0.08)',
        fill: true, tension: 0.35,
        pointRadius: 2,
        pointHoverRadius: 5,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {legend:{display:false}, tooltip:{backgroundColor:'#121a28',titleColor:'#f0f4f8',bodyColor:'#d0dae8',borderColor:'#1e2a3a',borderWidth:1}},
      scales: {
        x: {grid:{color:'#1a2540',drawBorder:false}, ticks:{color:'#5a6a8a',font:{size:11},maxTicksLimit:8}},
        y: {grid:{color:'#1a2540',drawBorder:false}, ticks:{color:'#5a6a8a',font:{size:11},callback:v=>'$'+(v/1000).toFixed(0)+'k'}}
      },
      interaction:{mode:'index',intersect:false}
    }
  });
  const regCtx = document.getElementById('regionChart').getContext('2d');
  chartInstances.region = new Chart(regCtx, {
    type: 'doughnut', data: {
      labels: Object.keys(mockData.regionRevenue),
      datasets: [{
        data: Object.values(mockData.regionRevenue),
        backgroundColor: ['#4a7cf7','#4ade80','#f59e0b'],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend:{position:'bottom',labels:{color:'#7a8a9e',padding:12,font:{size:11},usePointStyle:true}},
        tooltip:{backgroundColor:'#121a28',titleColor:'#f0f4f8',bodyColor:'#d0dae8',borderColor:'#1e2a3a',borderWidth:1,callbacks:{label:ctx=>' $'+(ctx.raw/1000).toFixed(0)+'k'}}
      }
    }
  });
  const custCtx = document.getElementById('topCustomersChart').getContext('2d');
  chartInstances.topCustomers = new Chart(custCtx, {
    type: 'bar', data: {
      labels: mockData.topCustomers.map(c=>c.name),
      datasets: [{
        label: 'MRR ($)',
        data: mockData.topCustomers.map(c=>c.mrr),
        backgroundColor: ['#4a7cf7','#4ade80','#f59e0b','#f87171','#a78bfa'],
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      plugins: {
        legend:{display:false},
        tooltip:{backgroundColor:'#121a28',titleColor:'#f0f4f8',bodyColor:'#d0dae8',borderColor:'#1e2a3a',borderWidth:1,callbacks:{label:ctx=>' $'+ctx.raw.toLocaleString()}}
      },
      scales: {
        x: {grid:{color:'#1a2540',drawBorder:false}, ticks:{color:'#5a6a8a',font:{size:11},callback:v=>'$'+(v/1000).toFixed(0)+'k'}},
        y: {grid:{display:false}, ticks:{color:'#d0dae8',font:{size:11}}}
      }
    }
  });
}
function getContextSummary(){
  const dateRange = document.getElementById('dateRange').value;
  const region = document.getElementById('regionFilter').value;
  const product = document.getElementById('productFilter').value;
  return {dateRange,region,product};
}
function updateContextBadge(){
  const ctx = getContextSummary();
  document.getElementById('contextBadge').textContent = `Filters: ${ctx.dateRange}, ${ctx.region}, ${ctx.product}`;
}
document.getElementById('dateRange').addEventListener('change',updateContextBadge);
document.getElementById('regionFilter').addEventListener('change',updateContextBadge);
document.getElementById('productFilter').addEventListener('change',updateContextBadge);
function processQuery(query){
  const q = query.toLowerCase();
  const ctx = getContextSummary();
  let result = {type:'text',message:'',chart:null};
  if(q.includes('revenue spike') || q.includes('spike last tuesday')){
    const event = mockData.unusualEvents['2026-06-24'];
    if(event){
      result.type = 'insight';
      result.insight = event;
      result.message = `Revenue spike detected on June 24. ${event.reason}. Impact: $${event.impact.toLocaleString()} added to MRR. The spike was driven by a single large enterprise deal rather than organic growth. This is a one-time event affecting the trend line.`;
      result.chart = {type:'line',highlight:24,data:mockData.dailyRevenue,labels:mockData.dates,annotation:'Enterprise deal closed here'};
    }
  }
  else if(q.includes('top 5') || q.includes('top customers') || (q.includes('top') && q.includes('mrr'))){
    const customers = mockData.topCustomers;
    result.type = 'chart';
    result.message = `Here are your top 5 customers by MRR:\n\n`;
    customers.forEach((c,i)=>{result.message += `${i+1}. ${c.name}: $${c.mrr.toLocaleString()}/mo\n`;});
    result.message += `\nTotal from top 5: $${customers.reduce((s,c)=>s+c.mrr,0).toLocaleString()}/mo, representing ${((customers.reduce((s,c)=>s+c.mrr,0)/284512)*100).toFixed(1)}% of total MRR.`;
    result.chart = {type:'bar',horizontal:true,data:customers.map(c=>c.mrr),labels:customers.map(c=>c.name),title:'Top 5 Customers by MRR'};
  }
  else if(q.includes('compare') && (q.includes('quarter') || q.includes('q'))){
    const thisQ = mockData.weeklyComparison.thisQ;
    const lastQ = mockData.weeklyComparison.lastQ;
    const growth = ((thisQ[3]-lastQ[3])/lastQ[3]*100).toFixed(1);
    result.type = 'chart';
    result.message = `Quarter comparison:\n\nThis quarter (weeks 1-4): $${thisQ.map(v=>v.toLocaleString()).join(', ')}\nLast quarter (weeks 1-4): $${lastQ.map(v=>v.toLocaleString()).join(', ')}\n\nCurrent MRR: $${thisQ[3].toLocaleString()} vs $${lastQ[3].toLocaleString()} last quarter (${growth}% growth).\n\nTrend: Revenue has grown steadily across both quarters, with this quarter showing stronger acceleration ($${(thisQ[3]-thisQ[0]).toLocaleString()} gain vs $${(lastQ[3]-lastQ[0]).toLocaleString()} last quarter).`;
    result.chart = {type:'comparison',thisQ,lastQ,labels:['Week 1','Week 2','Week 3','Week 4']};
  }
  else if(q.includes('region') && (q.includes('grew') || q.includes('growth') || q.includes('most'))){
    const regions = mockData.regionRevenue;
    const sorted = Object.entries(regions).sort((a,b)=>b[1]-a[1]);
    const growth = {NA:0.08,EMEA:0.22,APAC:0.15};
    const best = Object.entries(growth).sort((a,b)=>b[1]-a[1])[0];
    result.type = 'chart';
    result.message = `Region growth analysis:\n\n`;
    Object.entries(growth).forEach(([r,g])=>{
      result.message += `${r}: $${regions[r].toLocaleString()} MRR (+${(g*100).toFixed(0)}% growth)\n`;
    });
    result.message += `\nEMEA grew the most at 22%, driven by a successful campaign in Q2. Recommended action: replicate the EMEA campaign strategy in APAC where growth potential remains untapped.`;
    result.chart = {type:'doughnut',data:Object.values(regions),labels:Object.keys(regions)};
  }
  else if(q.includes('error') || q.includes('errors') || q.includes('incident')){
    result.type = 'text';
    result.message = `Current error rate is 0.47%, up 0.08% from last period. This is within acceptable thresholds (<1%).\n\nError breakdown:\n- API timeouts: 0.21%\n- Database connection: 0.15%\n- Rate limiting: 0.07%\n- Other: 0.04%\n\nNo critical incidents in the selected period. The slight increase correlates with a 12% traffic increase.`;
  }
  else if(q.includes('user') || q.includes('users') || q.includes('active')){
    result.type = 'text';
    result.message = `Active users: 8,247 (+5.2% vs last period).\n\nDaily active users average: 3,842\nWeekly active users: 6,910\nMonthly active users: 8,247\n\nUser growth has been strongest in NA (+7.1%) and EMEA (+6.3%). APAC is flat at +1.2% — may need targeted engagement. The spike on June 17 correlates with the AI Copilot v2 feature launch (+18% user growth that week).`;
  }
  else {
    result.type = 'text';
    result.message = `I analyzed your dashboard for "${query}".\n\nCurrent state: MRR is $284,512 (+12.4%), Active Users 8,247 (+5.2%), Avg Response Time 1.8s (-0.3s), Error Rate 0.47%.\n\nFor the selected period (${ctx.dateRange}, ${ctx.region}, ${ctx.product}), revenue shows a steady upward trend with notable acceleration in the last week. Region distribution: NA leads at 48%, followed by EMEA at 32%, and APAC at 20%.\n\nTry asking: "What caused the revenue spike last Tuesday?" or "Show me top customers by MRR" for deeper analysis.`;
  }
  return result;
}
function addMiniChart(container,chartData){
  const canvas = document.createElement('canvas');
  canvas.style.width = '100%';
  canvas.style.height = '120px';
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  const chartId = 'mini_' + (messageCount++);
  let config;
  if(chartData.type === 'comparison'){
    config = {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {label:'This Quarter',data:chartData.thisQ,borderColor:'#4a7cf7',backgroundColor:'rgba(74,124,247,0.1)',fill:true,tension:0.3,pointRadius:3},
          {label:'Last Quarter',data:chartData.lastQ,borderColor:'#7a8a9e',borderDash:[4,4],backgroundColor:'rgba(122,138,158,0.05)',fill:true,tension:0.3,pointRadius:3}
        ]
      },
      options:{
        responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#7a8a9e',font:{size:10},boxWidth:12}}},
        scales:{
          x:{grid:{color:'#1a2540'},ticks:{color:'#5a6a8a',font:{size:9}}},
          y:{grid:{color:'#1a2540'},ticks:{color:'#5a6a8a',font:{size:9},callback:v=>'$'+(v/1000).toFixed(0)+'k'}}
        }
      }
    };
  } else if(chartData.type === 'bar'){
    config = {
      type: chartData.horizontal ? 'bar' : 'bar',
      data: {
        labels: chartData.labels,
        datasets: [{data:chartData.data,backgroundColor:['#4a7cf7','#4ade80','#f59e0b','#f87171','#a78bfa'],borderRadius:3}]
      },
      options:{
        indexAxis: chartData.horizontal ? 'y' : 'x',
        responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false}},
        scales:{
          x:{grid:{color:'#1a2540'},ticks:{color:'#5a6a8a',font:{size:9}}},
          y:{grid:{display:false},ticks:{color:'#d0dae8',font:{size:9}}}
        }
      }
    };
  } else if(chartData.type === 'doughnut'){
    config = {
      type:'doughnut',
      data:{labels:chartData.labels,datasets:[{data:chartData.data,backgroundColor:['#4a7cf7','#4ade80','#f59e0b'],borderWidth:0}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{legend:{position:'bottom',labels:{color:'#7a8a9e',font:{size:9},boxWidth:10,usePointStyle:true}}}}
    };
  } else {
    config = {
      type:'line',
      data:{labels:chartData.labels,datasets:[{data:chartData.data,borderColor:'#4a7cf7',backgroundColor:'rgba(74,124,247,0.08)',fill:true,tension:0.35,pointRadius:1,borderWidth:1.5}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{enabled:false}},scales:{x:{display:false},y:{display:false}}}
    };
  }
  new Chart(ctx, config);
}
function addMessage(role, content, chartData, insightText){
  const messagesDiv = document.getElementById('chatMessages');
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${role}`;
  if(role === 'assistant' && chartData){
    const textDiv = document.createElement('div');
    textDiv.textContent = content;
    msgDiv.appendChild(textDiv);
    const chartMini = document.createElement('div');
    chartMini.className = 'chart-mini';
    msgDiv.appendChild(chartMini);
    setTimeout(()=>{
      addMiniChart(chartMini, chartData);
    }, 50);
    if(insightText){
      const insightDiv = document.createElement('div');
      insightDiv.className = 'insight-text';
      insightDiv.textContent = insightText;
      msgDiv.appendChild(insightDiv);
    }
  } else {
    msgDiv.textContent = content;
  }
  messagesDiv.appendChild(msgDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
function showTyping(){
  const messagesDiv = document.getElementById('chatMessages');
  const typing = document.createElement('div');
  typing.className = 'message assistant typing-indicator';
  typing.id = 'typingIndicator';
  typing.innerHTML = '<span></span><span></span><span></span>';
  messagesDiv.appendChild(typing);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
function hideTyping(){
  const typing = document.getElementById('typingIndicator');
  if(typing) typing.remove();
}
function handleQuery(query){
  if(!query.trim()) return;
  addMessage('user', query);
  document.getElementById('queryInput').value = '';
  document.getElementById('sendBtn').disabled = true;
  showTyping();
  setTimeout(()=>{
    hideTyping();
    const result = processQuery(query);
    let chartData = null;
    let insightAnnotation = null;
    if(result.type === 'insight' && result.chart){
      chartData = result.chart;
      insightAnnotation = result.insight ? `${result.insight.reason}` : null;
    } else if(result.type === 'chart' && result.chart){
      chartData = result.chart;
    }
    addMessage('assistant', result.message, chartData, insightAnnotation);
    document.getElementById('sendBtn').disabled = false;
    updateRefreshIndicator();
  }, 1200 + Math.random() * 800);
}
function updateRefreshIndicator(){
  const now = new Date();
  const timeStr = now.toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  document.getElementById('refreshIndicator').textContent = `Last updated: ${timeStr} — Auto-refresh every 60s`;
}
document.getElementById('sendBtn').addEventListener('click', ()=>{
  handleQuery(document.getElementById('queryInput').value);
});
document.getElementById('queryInput').addEventListener('keydown', (e)=>{
  if(e.key === 'Enter') handleQuery(e.target.value);
});
document.querySelectorAll('.suggestion-chip').forEach(chip => {
  chip.addEventListener('click', ()=>{
    handleQuery(chip.dataset.query);
  });
});
document.getElementById('voiceBtn').addEventListener('click', function(){
  if(!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
    addMessage('assistant', 'Voice input is not supported in this browser. Try Chrome or Edge for voice support.');
    return;
  }
  if(this.classList.contains('recording')){
    this.classList.remove('recording');
    this.textContent = '🎤';
    if(window.recognition) window.recognition.stop();
    return;
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  window.recognition = recognition;
  recognition.lang = 'en-US';
  recognition.continuous = false;
  recognition.interimResults = false;
  this.classList.add('recording');
  this.textContent = '🔴';
  recognition.onresult = (event)=>{
    const transcript = event.results[0][0].transcript;
    document.getElementById('queryInput').value = transcript;
    this.classList.remove('recording');
    this.textContent = '🎤';
    handleQuery(transcript);
  };
  recognition.onerror = ()=>{
    this.classList.remove('recording');
    this.textContent = '🎤';
    addMessage('assistant', 'Voice recognition failed. Please try again or type your question.');
  };
  recognition.start();
});
initMainCharts();
updateContextBadge();
updateRefreshIndicator();
setInterval(updateRefreshIndicator, 60000);
})();
</script>
</body>
</html>
```
Deliverable: A single-file interactive HTML dashboard (index.html) with:
1. Main dashboard panel with revenue trend line chart (30 days), region doughnut chart, top customers horizontal bar chart, and 4 KPI metric cards (MRR, Active Users, Avg Response Time, Error Rate) with deltas.
2. Filters bar with date range, region, and product selectors that update the context badge in real time.
3. AI Copilot side panel with:
   - Chat message area with user/assistant bubbles
   - 4 suggested query chips ("Revenue spike last Tuesday", "Top 5 customers by MRR", "Compare this quarter to last", "Which region grew most?")
   - Text input with Enter/Send
   - Voice input button (Web Speech API)
   - Typing indicator while processing
4. NL query processing pipeline handling 6 query types:
   - Revenue spike analysis (with enterprise deal annotation)
   - Top 5 customers by MRR (with percentage of total)
   - Quarter-over-quarter comparison (with growth calculation)
   - Region growth analysis (identifies EMEA as fastest-growing, suggests action)
   - Error rate breakdown
   - Active users analysis
   - Fallback: summary of current dashboard state
5. Responses include mini charts rendered inline in chat for queries that involve visual data (line, bar, comparison, doughnut).
6. Timestamped refresh indicator updating every 60 seconds.
7. Dark theme matching the Styde Ops Center aesthetic with Chart.js 4.4.7 loaded via CDN.
File path: E:\Stryde\_alpedal\styde-forge\Core\Web\ai-copilot-dashboard.html (or save index.html wherever desired).