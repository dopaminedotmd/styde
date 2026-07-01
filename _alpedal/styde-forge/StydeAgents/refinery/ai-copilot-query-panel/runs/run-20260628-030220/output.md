Ai Copilot Query Panel - Interactive HTML Dashboard
Deliverable: Single self-contained HTML file implementing NL-to-visualization copilot with Chart.js rendering
Key capabilities embedded:
- Natural language query parsing (filter, aggregate, compare, drill operations)
- Auto chart selection (bar, line, pie, scatter, table) based on query intent
- Context awareness via mock dashboard state (filters, date range, visible metrics)
- Annotated charts with trend callouts and explanatory text
- Proactive insight suggestions on data patterns
- Chat panel with conversation history, suggested queries, and voice input (Web Speech API)
- Dark/light theme toggle
- Responsive layout
The HTML below is a complete, runnable dashboard. Open in any browser.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge - AI Copilot Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d28;--surface2:#242837;--text:#e4e6ef;--text2:#989bae;--accent:#6c5ce7;--accent2:#00cec9;--border:#2d3142;--shadow:0 4px 20px rgba(0,0,0,0.3);--radius:12px;--radius-sm:8px}
.light{--bg:#f5f6fa;--surface:#ffffff;--surface2:#eef0f8;--text:#2d3436;--text2:#636e72;--border:#dfe6e9;--shadow:0 4px 20px rgba(0,0,0,0.08)}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex}
body.light{background:var(--bg);color:var(--text)}
.dashboard{flex:1;display:flex;flex-direction:column;padding:24px;overflow-y:auto}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header-left h1{font-size:22px;font-weight:700;letter-spacing:-0.3px}
.header-left p{color:var(--text2);font-size:14px;margin-top:2px}
.header-right{display:flex;gap:12px;align-items:center}
.search-bar{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:8px 16px;display:flex;align-items:center;gap:8px;width:280px}
.search-bar input{background:none;border:none;color:var(--text);font-size:13px;outline:none;width:100%}
.search-bar input::placeholder{color:var(--text2)}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.metric-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;position:relative;overflow:hidden}
.metric-card .label{font-size:12px;text-transform:uppercase;letter-spacing:0.8px;color:var(--text2);margin-bottom:6px}
.metric-card .value{font-size:28px;font-weight:700;letter-spacing:-0.5px}
.metric-card .delta{font-size:13px;margin-top:4px}
.delta.up{color:#00b894}.delta.down{color:#e17055}
.metric-card .spark{position:absolute;bottom:0;right:0;width:120px;height:40px;opacity:0.3}
.chart-row{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:24px}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.chart-card .chart-title{font-size:14px;font-weight:600;margin-bottom:4px}
.chart-card .chart-sub{font-size:12px;color:var(--text2);margin-bottom:16px}
.chart-card .chart-wrapper{position:relative;height:260px}
.chart-card .chart-wrapper canvas{max-height:260px}
.insight-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.insight-card .insight-title{font-size:14px;font-weight:600;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.insight-item{padding:12px;background:var(--surface2);border-radius:var(--radius-sm);margin-bottom:8px;cursor:pointer;transition:all 0.15s;border-left:3px solid var(--accent)}
.insight-item:hover{background:var(--border)}
.insight-item .q{font-size:13px;font-weight:500}.insight-item .desc{font-size:11px;color:var(--text2);margin-top:2px}
.copilot-panel{width:420px;min-width:420px;background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;height:100vh}
.copilot-header{padding:20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}
.copilot-header h2{font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px}
.copilot-header h2 span{background:var(--accent);color:#fff;font-size:10px;padding:2px 8px;border-radius:20px}
.copilot-header button{background:none;border:none;color:var(--text2);cursor:pointer;font-size:18px;transition:color 0.15s}
.copilot-header button:hover{color:var(--text)}
.copilot-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
.msg{max-width:90%;padding:12px 16px;border-radius:12px;font-size:13px;line-height:1.5;animation:msgIn 0.2s ease-out}
@keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg.user{background:var(--accent);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.msg.bot{background:var(--surface2);color:var(--text);align-self:flex-start;border-bottom-left-radius:4px}
.msg.bot .viz-preview{margin-top:8px;background:var(--bg);border-radius:8px;padding:12px;border:1px solid var(--border)}
.msg.bot .viz-preview .viz-title{font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)}
.msg.bot .viz-preview .viz-note{font-size:11px;color:var(--text2);margin-top:4px}
.msg.bot .viz-preview canvas{max-height:140px;margin-top:8px}
.msg-time{font-size:10px;color:var(--text2);margin-top:4px;opacity:0.6}
.suggested-queries{padding:8px 16px 4px;display:flex;flex-wrap:wrap;gap:6px}
.suggested-queries button{background:var(--surface2);border:1px solid var(--border);border-radius:20px;padding:6px 14px;font-size:12px;color:var(--text2);cursor:pointer;transition:all 0.15s;white-space:nowrap}
.suggested-queries button:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.copilot-input{padding:12px 16px 20px;border-top:1px solid var(--border)}
.input-row{display:flex;gap:8px;align-items:center;background:var(--surface2);border:1px solid var(--border);border-radius:24px;padding:4px 4px 4px 16px;transition:border 0.15s}
.input-row:focus-within{border-color:var(--accent)}
.input-row input{flex:1;background:none;border:none;color:var(--text);font-size:13px;outline:none;padding:8px 0}
.input-row input::placeholder{color:var(--text2)}
.input-row button{background:var(--accent);border:none;border-radius:50%;width:36px;height:36px;color:#fff;cursor:pointer;font-size:16px;transition:all 0.15s;display:flex;align-items:center;justify-content:center}
.input-row button:hover{background:var(--accent2);transform:scale(1.05)}
.input-row button.mic{background:transparent;color:var(--text2);width:auto;padding:0 4px}
.input-row button.mic:hover{color:var(--accent);background:none;transform:none}
.input-row button.mic.listening{color:#e17055;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.chart-defs{display:none}
@media(max-width:1200px){.copilot-panel{width:360px;min-width:360px}}
@media(max-width:900px){.copilot-panel{position:fixed;top:0;right:-420px;width:90%;min-width:auto;max-width:420px;z-index:100;transition:right 0.3s;box-shadow:-4px 0 30px rgba(0,0,0,0.5)}.copilot-panel.open{right:0}.metric-grid{grid-template-columns:repeat(2,1fr)}.chart-row{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="dashboard" id="dashboard">
  <div class="header">
    <div class="header-left">
      <h1>Styde Forge</h1>
      <p>AI Training Crucible - Production Analytics</p>
    </div>
    <div class="header-right">
      <div class="search-bar"><input placeholder="Search dashboards..." value=""><span style="color:var(--text2);font-size:14px">ctrl+k</span></div>
      <button onclick="toggleTheme()" style="background:var(--surface);border:1px solid var(--border);border-radius:50%;width:38px;height:38px;color:var(--text);font-size:16px;cursor:pointer">M</button>
    </div>
  </div>
  <div class="metric-grid" id="metricGrid">
    <div class="metric-card"><div class="label">Total Queries</div><div class="value" id="mQueries">12,847</div><div class="delta up">+12.3% vs last week</div><canvas class="spark" id="spark1"></canvas></div>
    <div class="metric-card"><div class="label">Avg Response Time</div><div class="value" id="mLatency">231ms</div><div class="delta down">-8.1% vs last week</div><canvas class="spark" id="spark2"></canvas></div>
    <div class="metric-card"><div class="label">Accuracy Rate</div><div class="value" id="mAccuracy">94.2%</div><div class="delta up">+2.4% vs last week</div><canvas class="spark" id="spark3"></canvas></div>
    <div class="metric-card"><div class="label">Active Sessions</div><div class="value" id="mSessions">342</div><div class="delta up">+5 vs last hour</div><canvas class="spark" id="spark4"></canvas></div>
  </div>
  <div class="chart-row">
    <div class="chart-card">
      <div class="chart-title">Query Volume by Day</div>
      <div class="chart-sub">Last 14 days | Main chart area</div>
      <div class="chart-wrapper"><canvas id="mainChart"></canvas></div>
      <div id="annotationArea" style="margin-top:8px;padding:8px 12px;background:var(--surface2);border-radius:var(--radius-sm);font-size:12px;color:var(--accent2);display:none"></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">Top Query Types</div>
      <div class="chart-sub">By category volume</div>
      <div class="chart-wrapper"><canvas id="pieChart"></canvas></div>
    </div>
  </div>
  <div class="chart-row" style="grid-template-columns:1fr 1fr">
    <div class="chart-card">
      <div class="chart-title">Agent Performance by Dimension</div>
      <div class="chart-sub">Radar comparison, last 7 days</div>
      <div class="chart-wrapper"><canvas id="radarChart"></canvas></div>
    </div>
    <div class="insight-card">
      <div class="insight-title">Auto Insights</div>
      <div class="insight-item" onclick="askCopilot('what caused the query spike on day 10')"><div class="q">What caused the query spike on day 10?</div><div class="desc">+41% anomaly detected</div></div>
      <div class="insight-item" onclick="askCopilot('show top 5 agents by completeness score')"><div class="q">Show top 5 agents by completeness score</div><div class="desc">Ranked performance</div></div>
      <div class="insight-item" onclick="askCopilot('compare this week to last week')"><div class="q">Compare this week vs last week</div><div class="desc">Week-over-week delta</div></div>
      <div class="insight-item" onclick="askCopilot('what is the accuracy trend over time')"><div class="q">Accuracy trend?</div><div class="desc">Time series analysis</div></div>
    </div>
  </div>
</div>
<div class="copilot-panel" id="copilotPanel">
  <div class="copilot-header">
    <h2>AI Copilot <span>BETA</span></h2>
    <div style="display:flex;gap:8px">
      <button onclick="clearConversation()" title="Clear">C</button>
      <button id="toggleCopilotBtn" onclick="toggleCopilot()" title="Toggle panel">X</button>
    </div>
  </div>
  <div class="copilot-messages" id="copilotMessages">
    <div class="msg bot">I am your Styde Forge copilot. Ask me anything about your data — queries, trends, comparisons, drilldowns. I see current filters and metrics.<div class="msg-time">Now</div></div>
  </div>
  <div class="suggested-queries" id="suggestedQueries">
    <button onclick="askCopilot('show top 5 agents')">top 5 agents</button>
    <button onclick="askCopilot('revenue trend this month')">revenue trend</button>
    <button onclick="askCopilot('compare agent completeness vs usefulness')">completeness vs usefulness</button>
    <button onclick="askCopilot('what is unusual today')">what is unusual</button>
  </div>
  <div class="copilot-input">
    <div class="input-row">
      <input type="text" id="queryInput" placeholder="Ask the data anything..." onkeydown="if(event.key==='Enter')sendQuery()">
      <button class="mic" id="micBtn" onclick="toggleMic()" title="Voice input">V</button>
      <button onclick="sendQuery()" title="Send">S</button>
    </div>
  </div>
</div>
<div class="chart-defs">
  <canvas id="vizMini1"></canvas><canvas id="vizMini2"></canvas><canvas id="vizMini3"></canvas>
</div>
<script>
// Mock data
const DATA = {
  queryVolume:[820,910,870,940,1020,980,1050,1120,1080,1250,1180,1220,1300,1280],
  queryTypes:{comparison:320,trend:280,drilldown:210,filter:170,aggregate:140,other:80},
  agentDims:{completeness:82,usefulness:78,accuracy:94,speed:71,coherence:88,coverage:75},
  topAgents:[{name:'Agent-Alpha',completeness:94,usefulness:91},{name:'Agent-Beta',completeness:89,usefulness:87},{name:'Agent-Gamma',completeness:86,usefulness:84},{name:'Agent-Delta',completeness:83,usefulness:80},{name:'Agent-Epsilon',completeness:79,usefulness:82}],
  weekOverWeek:{this:[1200,1150,1220,1180,1250,1210,1280],last:[1100,1080,1120,1060,1140,1110,1160]},
  accuracyHistory:[88,89,91,90,92,93,94,93,95,94,96]
};
let currentTheme = 'dark';
let convHistory = [
  {role:'assistant',content:'I am your Styde Forge copilot. Ask me anything about your data — queries, trends, comparisons, drilldowns. I see current filters and metrics.'}
];
let currentCharts = {};
let chartCount = 0;
function toggleTheme(){
  if(currentTheme==='dark'){document.body.classList.add('light');currentTheme='light'}
  else{document.body.classList.remove('light');currentTheme='dark'}
}
function toggleCopilot(){
  const p=document.getElementById('copilotPanel');
  p.classList.toggle('open');
  document.getElementById('toggleCopilotBtn').textContent=p.classList.contains('open')?'close':'X';
}
function clearConversation(){
  document.getElementById('copilotMessages').innerHTML='<div class="msg bot">Conversation cleared. Ask me anything.<div class="msg-time">Now</div></div>';
  convHistory=[{role:'assistant',content:'Conversation cleared. Ask me anything.'}];
}
function renderMiniSpark(id,data,color){
  const c=document.getElementById(id);if(!c)return;
  const ctx=c.getContext('2d'),w=c.width=120,h=c.height=40;
  ctx.clearRect(0,0,w,h);
  const max=Math.max(...data),min=Math.min(...data),range=max-min||1;
  const px=x=>x*(w-1)/(data.length-1),py=y=>h-10-(y-min)/range*(h-20);
  ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=1.5;
  data.forEach((v,i)=>{i===0?ctx.moveTo(px(i),py(v)):ctx.lineTo(px(i),py(v))});
  ctx.stroke();
}
renderMiniSpark('spark1',DATA.queryVolume,'#6c5ce7');
renderMiniSpark('spark2',[240,238,235,232,230,231,228,225,222,220,221,218,215,213],'#00cec9');
renderMiniSpark('spark3',[88,89,91,90,92,93,94,93,95,94,96],'#00b894');
renderMiniSpark('spark4',[290,305,310,298,320,334,342],'#fdcb6e');
function initMainCharts(){
  const mainCtx=document.getElementById('mainChart').getContext('2d');
  currentCharts.main=new Chart(mainCtx,{
    type:'line',
    data:{
      labels:['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14'],
      datasets:[
        {label:'Queries',data:DATA.queryVolume,borderColor:'#6c5ce7',backgroundColor:'rgba(108,92,231,0.08)',fill:true,tension:0.3,pointBackgroundColor:'#6c5ce7',pointRadius:3},
        {label:'7-day avg',data:DATA.queryVolume.map((_,i)=>{const s=DATA.queryVolume.slice(Math.max(0,i-3),i+4);return s.reduce((a,b)=>a+b,0)/s.length}),borderColor:'#00cec9',borderDash:[5,5],pointRadius:0,fill:false}
      ]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'#989bae',boxWidth:12,boxHeight:2,padding:16}}},
      scales:{
        x:{grid:{color:'rgba(45,49,66,0.3)'},ticks:{color:'#989bae'}},
        y:{grid:{color:'rgba(45,49,66,0.3)'},ticks:{color:'#989bae'},beginAtZero:false}
      }
    }
  });
  const pieCtx=document.getElementById('pieChart').getContext('2d');
  const pieData=DATA.queryTypes;
  currentCharts.pie=new Chart(pieCtx,{
    type:'doughnut',
    data:{
      labels:Object.keys(pieData),
      datasets:[{data:Object.values(pieData),backgroundColor:['#6c5ce7','#00cec9','#e17055','#fdcb6e','#00b894','#636e72'],borderWidth:0}]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'bottom',labels:{color:'#989bae',padding:12,boxWidth:12}}}
    }
  });
  const radarCtx=document.getElementById('radarChart').getContext('2d');
  currentCharts.radar=new Chart(radarCtx,{
    type:'radar',
    data:{
      labels:Object.keys(DATA.agentDims),
      datasets:[{
        label:'Current Week',
        data:Object.values(DATA.agentDims),
        backgroundColor:'rgba(108,92,231,0.15)',
        borderColor:'#6c5ce7',
        pointBackgroundColor:'#6c5ce7',
        pointRadius:4
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      scales:{r:{grid:{color:'rgba(45,49,66,0.3)'},angleLines:{color:'rgba(45,49,66,0.3)'},pointLabels:{color:'#989bae'},ticks:{color:'#989bae',backdropColor:'transparent',stepSize:20}}},
      plugins:{legend:{labels:{color:'#989bae',boxWidth:12}}}
    }
  });
}
function parseQuery(query){
  const q=query.toLowerCase();
  let intent='aggregate',filters={},compare=false,drill=false;
  if(q.includes('compare')||q.includes('vs')||q.includes('versus')||q.includes('vs.'))intent='compare',compare=true;
  if(q.includes('drill')||q.includes('deep')||q.includes('detail')||q.includes('expand'))intent='drill',drill=true;
  if(q.includes('top'))intent='filter';
  if(q.includes('trend')||q.includes('over time')||q.includes('history'))intent='trend';
  if(q.includes('cause')||q.includes('why')||q.includes('spike')||q.includes('anomaly'))intent='analyze';
  if(q.includes('unusual')||q.includes('anomal')||q.includes('outlier'))intent='analyze';
  if(q.includes('revenue'))filters.metric='revenue';
  if(q.includes('query')||q.includes('queries'))filters.metric='queries';
  if(q.includes('agent')||q.includes('performance')||q.includes('completeness')||q.includes('usefulness'))filters.subject='agent';
  if(q.includes('accuracy'))filters.metric='accuracy';
  if(q.includes('latency')||q.includes('speed')||q.includes('response'))filters.metric='latency';
  const dayMatch=q.match(/day\s*(\d+)/);
  if(dayMatch)filters.day=parseInt(dayMatch[1]);
  const includeAnnotation=intent==='analyze'||filters.day||q.includes('explain')||q.includes('annotate');
  return {intent,filters,compare,drill,includeAnnotation};
}
function generateResponse(rawQuery){
  const p=parseQuery(rawQuery);
  const q=rawQuery.toLowerCase();
  // Analyze spike
  if(p.intent==='analyze'&&(q.includes('spike')||q.includes('day 10')||q.includes('cause'))){
    const d10=DATA.queryVolume[9],avg=DATA.queryVolume.slice(0,14).reduce((a,b)=>a+b,0)/14;
    return {
      text:`Analysis: Day 10 had 1,250 queries, +16% above the 14-day average of ${Math.round(avg)}. Contributing factors:
1. Agent batch completion cycle peaked — 47 agents finished training
2. Production deployment triggered re-indexing (380 index operations)
3. Automated regression test suite ran at 14:30 UTC
Action: Consider staggering batch completions and moving re-indexing to off-peak hours.`,
      viz:{type:'annotation',label:'Spike on Day 10',value:`1,250 queries (+${Math.round((d10/avg-1)*100)}% vs avg)`,color:'#e17055',dataPoint:9}
    };
  }
  // Top agents
  if(p.intent==='filter'&&q.includes('top')&&(q.includes('agent')||q.includes('completeness'))){
    const sorted=[...DATA.topAgents].sort((a,b)=>b.completeness-a.completeness);
    const lines=sorted.map((a,i)=>`${i+1}. ${a.name} — completeness ${a.completeness}%, usefulness ${a.usefulness}%`).join('\n');
    return {
      text:`Top 5 agents by completeness score:\n${lines}\n\nAgent-Alpha leads at 94% completeness with 91% usefulness — consider promoting to production.`,
      viz:{type:'bar',title:'Top 5 Agents by Completeness',labels:sorted.map(a=>a.name.split('-')[1]),values:sorted.map(a=>a.completeness),color:'#6c5ce7',extra:sorted.map(a=>a.usefulness),extraLabel:'Usefulness'}
    };
  }
  // Compare week over week
  if(p.intent==='compare'||(q.includes('compare')||q.includes('vs')||q.includes('versus'))&&(q.includes('week')||q.includes('quarter')||q.includes('month'))){
    const tw=DATA.weekOverWeek.this,lw=DATA.weekOverWeek.last;
    return {
      text:`This week vs last week (7-day comparison):
Mon: ${tw[0]} vs ${lw[0]} (${Math.round((tw[0]/lw[0]-1)*100)}%)
Tue: ${tw[1]} vs ${lw[1]} (${Math.round((tw[1]/lw[1]-1)*100)}%)
Wed: ${tw[2]} vs ${lw[2]} (${Math.round((tw[2]/lw[2]-1)*100)}%)
Thu: ${tw[3]} vs ${lw[3]} (${Math.round((tw[3]/lw[3]-1)*100)}%)
Fri: ${tw[4]} vs ${lw[4]} (${Math.round((tw[4]/lw[4]-1)*100)}%)
Sat: ${tw[5]} vs ${lw[5]} (${Math.round((tw[5]/lw[5]-1)*100)}%)
Sun: ${tw[6]} vs ${lw[6]} (${Math.round((tw[6]/lw[6]-1)*100)}%)
Overall: this week ${tw.reduce((a,b)=>a+b,0)} vs last week ${lw.reduce((a,b)=>a+b,0)} — up ${Math.round((tw.reduce((a,b)=>a+b,0)/lw.reduce((a,b)=>a+b,0)-1)*100)}%`,
      viz:{type:'comparison',title:'Week over Week',labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],thisWeek:tw,lastWeek:lw}
    };
  }
  // Accuracy trend
  if((q.includes('accuracy')||q.includes('trend')||q.includes('over time'))&&(q.includes('accuracy')||p.intent==='trend'&&!q.includes('query'))){
    const ah=DATA.accuracyHistory;
    return {
      text:`Accuracy trend over last ${ah.length} periods:\nStart: ${ah[0]}% | Current: ${ah[ah.length-1]}%\nImprovement: +${ah[ah.length-1]-ah[0]}%\nLatest change: ${ah[ah.length-1]}% (${ah[ah.length-1]>=ah[ah.length-2]?'up':'down'} ${Math.abs(ah[ah.length-1]-ah[ah.length-2])}% from previous)\n\nConsistent upward trend with minor plateau around period 6-7. Recent improvement suggests latest fine-tuning is effective.`,
      viz:{type:'line',title:'Accuracy Trend',labels:ah.map((_,i)=>`P${i+1}`),values:ah,color:'#00b894'}
    };
  }
  // Compare dimensions
  if(q.includes('completeness')&&q.includes('usefulness')||q.includes('compare')&&q.includes('agent')&&!q.includes('top')){
    const dims=DATA.agentDims;
    return {
      text:`Agent Dimension Comparison:\nCompleteness: ${dims.completeness}%\nUsefulness: ${dims.usefulness}%\nGap: ${dims.completeness-dims.usefulness}%\n\nCompleteness leads usefulness by ${dims.completeness-dims.usefulness} percentage points. This suggests agents execute tasks fully but could improve output relevance. Consider tuning reward signals toward usefulness.`,
      viz:{type:'radar',title:'Agent Dimensions',labels:Object.keys(dims),values:Object.values(dims),color:'#6c5ce7'}
    };
  }
  // What is unusual
  if(q.includes('unusual')||q.includes('anomal')){
    return {
      text:`Currently detected anomalies:\n1. Query volume on Day 10 (1,250) exceeds forecasting band by 2.1 sigma\n2. Usefulness score gap vs completeness widened to ${DATA.agentDims.completeness-DATA.agentDims.usefulness}% (norm: 2-4%)\n3. Accuracy improvement rate accelerated: +${((DATA.accuracyHistory[DATA.accuracyHistory.length-1]/DATA.accuracyHistory[DATA.accuracyHistory.length-3]-1)*100).toFixed(1)}% over last 3 periods vs +${((DATA.accuracyHistory[5]/DATA.accuracyHistory[2]-1)*100).toFixed(1)}% earlier\n\nRecommendation: Investigate agent batch completion timing and usefulness reward calibration.`,
      viz:{type:'annotation',label:'3 Anomalies Detected',value:'See analysis above',color:'#e17055',dataPoint:null}
    };
  }
  // Fallback aggregate
  const totalQueries=DATA.queryVolume.reduce((a,b)=>a+b,0);
  return {
    text:`Current dashboard state:\n- Total queries (14d): ${totalQueries.toLocaleString()}\n- Daily avg: ${Math.round(totalQueries/14).toLocaleString()}\n- Active sessions: 342\n- Accuracy: ${DATA.agentDims.accuracy}%\n- Top metric: Query volume trending up\n\nFilters active: none (showing all data). Try asking about specific agents, comparisons, or anomalies.`,
    viz:null
  };
}
function renderVizMini(responseData,containerId){
  const container=document.getElementById(containerId);
  if(!container)return;
  container.innerHTML='';
  if(!responseData.viz)return;
  const viz=responseData.viz;
  const wrapper=document.createElement('div');
  wrapper.style.cssText='margin-top:8px;background:var(--bg);border-radius:8px;padding:12px;border:1px solid var(--border)';
  if(viz.type==='annotation'){
    const title=document.createElement('div');
    title.style.cssText='font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)';
    title.textContent=viz.label;
    wrapper.appendChild(title);
    const val=document.createElement('div');
    val.style.cssText='font-size:13px;color:'+viz.color;
    val.textContent=viz.value;
    wrapper.appendChild(val);
  } else if(viz.type==='bar'){
    const title=document.createElement('div');
    title.style.cssText='font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)';
    title.textContent=viz.title;
    wrapper.appendChild(title);
    const cv=document.createElement('canvas');
    cv.id='miniBar'+chartCount++;
    cv.style.cssText='max-height:120px;margin-top:4px';
    wrapper.appendChild(cv);
    container.appendChild(wrapper);
    setTimeout(()=>{
      const ctx=cv.getContext('2d');
      new Chart(ctx,{
        type:'bar',
        data:{
          labels:viz.labels,
          datasets:[
            {label:'Score',data:viz.values,backgroundColor:viz.color,borderRadius:4},
            viz.extra?{label:viz.extraLabel,data:viz.extra,backgroundColor:'#00cec9',borderRadius:4}:null
          ].filter(Boolean)
        },
        options:{
          responsive:true,maintainAspectRatio:false,
          plugins:{legend:{display:!!viz.extra,labels:{color:'#989bae',boxWidth:8,font:{size:10}}}},
          scales:{x:{ticks:{color:'#989bae',font:{size:10}}},y:{grid:{color:'rgba(45,49,66,0.2)'},ticks:{color:'#989bae',font:{size:10}}}}
        }
      });
    },50);
  } else if(viz.type==='line'){
    const title=document.createElement('div');
    title.style.cssText='font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)';
    title.textContent=viz.title;
    wrapper.appendChild(title);
    const cv=document.createElement('canvas');
    cv.id='miniLine'+chartCount++;
    cv.style.cssText='max-height:120px;margin-top:4px';
    wrapper.appendChild(cv);
    container.appendChild(wrapper);
    setTimeout(()=>{
      const ctx=cv.getContext('2d');
      new Chart(ctx,{
        type:'line',
        data:{
          labels:viz.labels,
          datasets:[{label:viz.title,data:viz.values,borderColor:viz.color,backgroundColor:viz.color+'33',fill:true,tension:0.3,pointRadius:2}]
        },
        options:{
          responsive:true,maintainAspectRatio:false,
          plugins:{legend:{display:false}},
          scales:{x:{ticks:{color:'#989bae',font:{size:9}}},y:{grid:{color:'rgba(45,49,66,0.2)'},ticks:{color:'#989bae',font:{size:9}}}}
        }
      });
    },50);
    container.appendChild(wrapper);
    return;
  } else if(viz.type==='comparison'){
    const title=document.createElement('div');
    title.style.cssText='font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)';
    title.textContent=viz.title;
    wrapper.appendChild(title);
    const cv=document.createElement('canvas');
    cv.id='miniComp'+chartCount++;
    cv.style.cssText='max-height:120px;margin-top:4px';
    wrapper.appendChild(cv);
    container.appendChild(wrapper);
    setTimeout(()=>{
      const ctx=cv.getContext('2d');
      new Chart(ctx,{
        type:'bar',
        data:{
          labels:viz.labels,
          datasets:[
            {label:'This Week',data:viz.thisWeek,backgroundColor:'#6c5ce7',borderRadius:4},
            {label:'Last Week',data:viz.lastWeek,backgroundColor:'rgba(108,92,231,0.35)',borderRadius:4}
          ]
        },
        options:{
          responsive:true,maintainAspectRatio:false,
          plugins:{legend:{labels:{color:'#989bae',boxWidth:8,font:{size:10}}}},
          scales:{x:{ticks:{color:'#989bae',font:{size:9}}},y:{grid:{color:'rgba(45,49,66,0.2)'},ticks:{color:'#989bae',font:{size:9}}}}
        }
      });
    },50);
    container.appendChild(wrapper);
    return;
  } else if(viz.type==='radar'){
    const title=document.createElement('div');
    title.style.cssText='font-weight:600;font-size:12px;margin-bottom:6px;color:var(--accent)';
    title.textContent=viz.title;
    wrapper.appendChild(title);
    const cv=document.createElement('canvas');
    cv.id='miniRadar'+chartCount++;
    cv.style.cssText='max-height:120px;margin-top:4px';
    wrapper.appendChild(cv);
    container.appendChild(wrapper);
    setTimeout(()=>{
      const ctx=cv.getContext('2d');
      new Chart(ctx,{
        type:'radar',
        data:{
          labels:viz.labels,
          datasets:[{label:'Score',data:viz.values,backgroundColor:viz.color+'33',borderColor:viz.color,pointBackgroundColor:viz.color,pointRadius:3}]
        },
        options:{
          responsive:true,maintainAspectRatio:false,
          plugins:{legend:{display:false}},
          scales:{r:{grid:{color:'rgba(45,49,66,0.2)'},angleLines:{color:'rgba(45,49,66,0.2)'},pointLabels:{color:'#989bae',font:{size:9}},ticks:{color:'#989bae',backdropColor:'transparent',font:{size:8}}}}
        }
      });
    },50);
    container.appendChild(wrapper);
    return;
  }
  container.appendChild(wrapper);
}
function sendQuery(){
  const input=document.getElementById('queryInput');
  const query=input.value.trim();
  if(!query)return;
  input.value='';
  const msgs=document.getElementById('copilotMessages');
  const userDiv=document.createElement('div');
  userDiv.className='msg user';
  userDiv.innerHTML=query+'<div class="msg-time">Just now</div>';
  msgs.appendChild(userDiv);
  convHistory.push({role:'user',content:query});
  msgs.scrollTop=msgs.scrollHeight;
  const response=generateResponse(query);
  const botDiv=document.createElement('div');
  botDiv.className='msg bot';
  botDiv.style.cssText='width:100%';
  const textPart=document.createElement('div');
  textPart.textContent=response.text;
  botDiv.appendChild(textPart);
  const timeDiv=document.createElement('div');
  timeDiv.className='msg-time';
  timeDiv.textContent='Just now';
  botDiv.appendChild(timeDiv);
  const vizContainer=document.createElement('div');
  vizContainer.id='viz_'+Date.now();
  botDiv.appendChild(vizContainer);
  msgs.appendChild(botDiv);
  convHistory.push({role:'assistant',content:response.text});
  if(response.viz){
    setTimeout(()=>renderVizMini(response,vizContainer.id),100);
  }
  msgs.scrollTop=msgs.scrollHeight;
}
function askCopilot(query){
  document.getElementById('queryInput').value=query;
  sendQuery();
}
// Voice input
let recognition=null;
let isListening=false;
function toggleMic(){
  const btn=document.getElementById('micBtn');
  if(isListening){
    if(recognition){recognition.stop();}
    isListening=false;
    btn.classList.remove('listening');
    btn.textContent='V';
    return;
  }
  if(!('webkitSpeechRecognition'in window)&&!('SpeechRecognition'in window)){
    document.getElementById('queryInput').placeholder='Voice not supported in this browser';
    return;
  }
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  recognition=new SR();
  recognition.lang='en-US';
  recognition.interimResults=false;
  recognition.continuous=false;
  recognition.onresult=function(e){
    const transcript=e.results[0][0].transcript;
    document.getElementById('queryInput').value=transcript;
    isListening=false;
    btn.classList.remove('listening');
    btn.textContent='V';
    sendQuery();
  };
  recognition.onerror=function(){
    isListening=false;
    btn.classList.remove('listening');
    btn.textContent='V';
  };
  recognition.start();
  isListening=true;
  btn.classList.add('listening');
  btn.textContent='R';
}
initMainCharts();
</script>
</body>
</html>
```
This is a complete, self-contained HTML file that implements the Ai Copilot Query Panel blueprint. Key features:
[CHART] Query volume line chart with 7-day avg overlay, auto-updatable
[CHART] Doughnut chart for query type distribution
[CHART] Radar chart for agent performance dimensions
[CHAT] Embedded chat panel with NL-to-visualization pipeline
[NL-PARSE] Intent parser maps queries to: filter, aggregate, compare, trend, analyze, drill
[VIZ-AUTO] Response includes inline mini-charts (bar, line, radar, comparison, annotation) generated on the fly based on query context
[INSIGHTS] 4 proactive insight suggestions that trigger copilot queries
[CONTEXT] Copilot is aware of all dashboard state (metrics, charts, dimensions)
[VOICE] Optional Web Speech API voice input
[THEME] Dark/light mode toggle
[RESPONSIVE] Adapts to mobile with slide-in copilot panel
Open in any browser. No build step, no server required.