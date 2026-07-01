<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Dashboard — Query Panel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 400px;grid-template-rows:60px 1fr;height:100vh}
.header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:0 24px;background:#1e293b;border-bottom:1px solid #334155}
.header h1{font-size:18px;font-weight:600;color:#f8fafc}
.header h1 span{color:#38bdf8;margin-right:8px}
.header-controls{display:flex;gap:16px;align-items:center}
.filter-group{display:flex;gap:8px;align-items:center}
.filter-group label{font-size:12px;color:#94a3b8}
.filter-group select,.filter-group input{background:#0f172a;border:1px solid #334155;color:#e2e8f0;padding:4px 8px;border-radius:6px;font-size:12px;outline:none}
.filter-group select:focus,.filter-group input:focus{border-color:#38bdf8}
.main{overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:16px}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.metric-card{background:#1e293b;border-radius:10px;padding:16px;border:1px solid #334155}
.metric-card .label{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#94a3b8;margin-bottom:4px}
.metric-card .value{font-size:24px;font-weight:700;color:#f8fafc}
.metric-card .change{font-size:12px;margin-top:4px}
.metric-card .change.up{color:#22c55e}
.metric-card .change.down{color:#ef4444}
.chart-area{background:#1e293b;border-radius:10px;padding:20px;border:1px solid #334155;flex:1;min-height:300px;display:flex;flex-direction:column}
.chart-area h3{font-size:14px;font-weight:600;color:#f8fafc;margin-bottom:12px}
.chart-area .chart-insight{margin-top:10px;padding:10px 14px;background:#0f172a;border-radius:8px;border-left:3px solid #38bdf8;font-size:12px;color:#94a3b8;line-height:1.5}
.chart-container{flex:1;position:relative;min-height:250px}
.chart-container canvas{width:100%!important;height:100%!important}
.copilot-panel{background:#1e293b;border-left:1px solid #334155;display:flex;flex-direction:column;height:calc(100vh - 60px)}
.copilot-header{padding:16px;border-bottom:1px solid #334155;display:flex;align-items:center;gap:8px;flex-shrink:0}
.copilot-header .badge{background:#38bdf8;color:#0f172a;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px}
.copilot-header h2{font-size:14px;font-weight:600;color:#f8fafc}
.copilot-messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.message{display:flex;gap:10px;max-width:100%;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.message.assistant{flex-direction:row}
.message.user{flex-direction:row-reverse}
.message .avatar{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
.message.assistant .avatar{background:#0f172a;color:#38bdf8;border:1px solid #334155}
.message.user .avatar{background:#38bdf8;color:#0f172a}
.message .bubble{background:#0f172a;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;max-width:85%}
.message.user .bubble{background:#38bdf8;color:#0f172a;border-bottom-right-radius:4px}
.message.assistant .bubble{background:#1e293b;border:1px solid #334155;border-bottom-left-radius:4px;color:#e2e8f0}
.message .bubble .chart-mini{margin-top:8px;height:100px;background:#0f172a;border-radius:6px;padding:8px;display:flex;align-items:flex-end;gap:3px}
.message .bubble .chart-mini .bar{background:#38bdf8;border-radius:2px 2px 0 0;flex:1;transition:height .3s ease}
.message .bubble .chart-mini .bar:nth-child(2n){background:#818cf8}
.message .bubble .insight-label{font-size:11px;color:#94a3b8;margin-top:6px;}
.suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:8px 12px 4px;border-top:1px solid #334155;flex-shrink:0}
.suggestions button{background:#0f172a;border:1px solid #334155;color:#94a3b8;padding:6px 12px;border-radius:16px;font-size:11px;cursor:pointer;transition:all .15s;white-space:nowrap}
.suggestions button:hover{background:#334155;color:#f8fafc;border-color:#38bdf8}
.copilot-input{display:flex;gap:8px;padding:12px;border-top:1px solid #334155;flex-shrink:0}
.copilot-input input{flex:1;background:#0f172a;border:1px solid #334155;color:#e2e8f0;padding:10px 14px;border-radius:8px;font-size:13px;outline:none}
.copilot-input input:focus{border-color:#38bdf8}
.copilot-input button{background:#38bdf8;color:#0f172a;border:none;width:38px;height:38px;border-radius:8px;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:background .15s;flex-shrink:0}
.copilot-input button:hover{background:#7dd3fc}
.copilot-input button:disabled{opacity:.4;cursor:not-allowed}
.typing-indicator{display:flex;gap:4px;padding:8px 0;align-items:center}
.typing-indicator .dot{width:6px;height:6px;background:#94a3b8;border-radius:50%;animation:typingPulse 1.2s infinite}
.typing-indicator .dot:nth-child(2){animation-delay:.2s}
.typing-indicator .dot:nth-child(3){animation-delay:.4s}
@keyframes typingPulse{0%,60%,100%{opacity:.3;transform:scale(.8)}30%{opacity:1;transform:scale(1)}}
</style>
</head>
<body>
<div class="dashboard">
<div class="header">
<h1><span>AI</span> Copilot Dashboard</h1>
<div class="header-controls">
<div class="filter-group">
<label for="dateRange">Period</label>
<select id="dateRange">
<option value="7d">Last 7 days</option>
<option value="30d" selected>Last 30 days</option>
<option value="90d">Last quarter</option>
<option value="1y">Year to date</option>
</select>
</div>
<div class="filter-group">
<label for="segmentFilter">Segment</label>
<select id="segmentFilter">
<option value="all">All</option>
<option value="enterprise">Enterprise</option>
<option value="midmarket">Mid-Market</option>
<option value="startup">Startup</option>
</select>
</div>
<div class="filter-group">
<label for="metricToggle">View</label>
<select id="metricToggle">
<option value="mrr">MRR</option>
<option value="revenue">Revenue</option>
<option value="customers">Customers</option>
</select>
</div>
</div>
</div>
<div class="main" id="mainArea">
<div class="metrics-row">
<div class="metric-card">
<div class="label">Monthly Recurring Revenue</div>
<div class="value" id="metricMRR">$284,500</div>
<div class="change up">+12.4% vs previous period</div>
</div>
<div class="metric-card">
<div class="label">Total Revenue</div>
<div class="value" id="metricRevenue">$892,300</div>
<div class="change up">+8.7% vs previous period</div>
</div>
<div class="metric-card">
<div class="label">Active Customers</div>
<div class="value" id="metricCustomers">1,847</div>
<div class="change up">+5.2% vs previous period</div>
</div>
<div class="metric-card">
<div class="label">Avg Revenue per Customer</div>
<div class="value" id="metricARPU">$483</div>
<div class="change up">+3.1% vs previous period</div>
</div>
</div>
<div class="chart-area" id="chartArea">
<h3 id="chartTitle">Revenue Trend — Last 30 Days</h3>
<div class="chart-container">
<canvas id="mainChart"></canvas>
</div>
<div class="chart-insight" id="chartInsight">
The upward trend continues with notable spikes on week 3 (product launch impact). Weekend dips are consistent with B2B buying patterns.
</div>
</div>
</div>
<div class="copilot-panel">
<div class="copilot-header">
<div class="badge">BETA</div>
<h2>Copilot Query Panel</h2>
</div>
<div class="copilot-messages" id="copilotMessages">
<div class="message assistant">
<div class="avatar">AI</div>
<div class="bubble">
Hello! I am your AI copilot. Ask me anything about your data — try 'What caused the revenue spike?' or 'Show me top customers by MRR'.
</div>
</div>
</div>
<div class="suggestions" id="suggestionBar">
<button data-query="What caused the revenue spike last Tuesday?">Revenue spike analysis</button>
<button data-query="Show me top 5 customers by MRR">Top 5 customers</button>
<button data-query="Compare this quarter to last quarter">Quarter comparison</button>
<button data-query="Which segment grew fastest this month?">Fastest segment</button>
</div>
<div class="copilot-input">
<input type="text" id="queryInput" placeholder="Ask your data a question..." autocomplete="off">
<button id="sendBtn" title="Send query">➤</button>
</div>
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
(function(){
const ctx = document.getElementById('mainChart').getContext('2d');
const days = Array.from({length:30},(_,i)=>'D'+(i+1));
const revenueData = [28400,29100,28800,30200,31500,29800,27500,31000,32500,31800,
33500,34200,32800,31000,35500,36800,37200,35900,34000,38500,
39800,41000,39500,37800,42000,43500,44200,42800,45000,46800];
const mrrData = revenueData.map(v=>Math.round(v*0.68));
const customerData = Array.from({length:30},(_,i)=>Math.round(1750+i*3.2+Math.random()*15));
const topCustomers = [
{name:'Acme Corp',mrr:42500,segment:'Enterprise',growth:18},
{name:'GlobalTech Inc',mrr:38200,segment:'Enterprise',growth:12},
{name:'Midwest Logistics',mrr:28400,segment:'Mid-Market',growth:22},
{name:'NovaSoft',mrr:25300,segment:'Mid-Market',growth:15},
{name:'BrightStart',mrr:22100,segment:'Startup',growth:35}
];
let currentView = 'revenue';
function getChartData(view){
switch(view){
case 'mrr': return {label:'MRR ($)',data:mrrData,color:'#818cf8'};
case 'revenue': return {label:'Revenue ($)',data:revenueData,color:'#38bdf8'};
case 'customers': return {label:'Customers',data:customerData,color:'#34d399'};
default: return {label:'Revenue ($)',data:revenueData,color:'#38bdf8'};
}
}
let chart = new Chart(ctx,{
type:'line',
data:{labels:days,datasets:[{
label:'Revenue ($)',
data:revenueData,
borderColor:'#38bdf8',
backgroundColor:'rgba(56,189,248,0.08)',
fill:true,
tension:.35,
pointRadius:3,
pointHoverRadius:6,
pointBackgroundColor:'#38bdf8',
borderWidth:2
}]},
options:{
responsive:true,
maintainAspectRatio:false,
plugins:{legend:{display:false},tooltip:{backgroundColor:'#1e293b',titleColor:'#f8fafc',bodyColor:'#e2e8f0',borderColor:'#334155',borderWidth:1,padding:10}},
scales:{x:{grid:{color:'rgba(51,65,85,0.3)'},ticks:{color:'#94a3b8',maxTicksLimit:8}},y:{grid:{color:'rgba(51,65,85,0.3)'},ticks:{color:'#94a3b8',callback:function(v){return'$'+v.toLocaleString()}}}}
}
});
const insights = {
revenue:'The upward trend continues with notable spikes on week 3 (product launch impact). Weekend dips are consistent with B2B buying patterns.',
mrr:'MRR growth is steady at 12.4% MoM. The compounding effect is visible in the accelerating curve from D20 onward.',
customers:'Customer acquisition is linear with slight acceleration in the last week. Average 96 new customers per period.'
};
function renderMiniChart(data,color){
let max=Math.max(...data);
let bars=data.slice(-20).map(v=>Math.round((v/max)*60)+10);
return '<div class="chart-mini">'+bars.map(h=>'<div class="bar" style="height:'+h+'px;background:'+color+'"></div>').join('')+'</div>';
}
function addMessage(role,text,miniData){
let msg=document.getElementById('copilotMessages');
let div=document.createElement('div');
div.className='message '+role;
let content='<div class="avatar">'+(role==='user'?'U':'AI')+'</div><div class="bubble">'+text;
if(miniData) content+=miniData;
content+='</div>';
div.innerHTML=content;
msg.appendChild(div);
msg.scrollTop=msg.scrollHeight;
}
function addTypingIndicator(){
let msg=document.getElementById('copilotMessages');
let div=document.createElement('div');
div.className='message assistant';
div.id='typingIndicator';
div.innerHTML='<div class="avatar">AI</div><div class="bubble"><div class="typing-indicator"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>';
msg.appendChild(div);
msg.scrollTop=msg.scrollHeight;
}
function removeTypingIndicator(){
let el=document.getElementById('typingIndicator');
if(el) el.remove();
}
function generateResponse(query){
let q=query.toLowerCase();
if(q.includes('revenue spike')||q.includes('spike')||q.includes('jump')){
let spikeIdx=25;
let prevVal=revenueData[spikeIdx-1];
let spikeVal=revenueData[spikeIdx];
let pct=Math.round(((spikeVal-prevVal)/prevVal)*100);
return {
text:'The revenue spike on D26 was primarily driven by the Enterprise segment closing 3 large deals worth $38,200 combined. Acme Corp upgraded their plan (+$12,500 MRR) and GlobalTech signed their annual renewal early (+$8,400). The product launch on D20 created pipeline that converted D24-D27.',
mini:renderMiniChart(revenueData.slice(22,30),'#38bdf8')+'<div class="insight-label">D22-D30 revenue: +23% spike detected</div>'
};
}
if(q.includes('top 5')||q.includes('top customers')||q.includes('by mrr')||q.includes('largest')){
let rows=topCustomers.map(c=>c.name+': $'+c.mrr.toLocaleString()+' ('+c.segment+', +'+c.growth+'%)').join('<br>');
let data=topCustomers.map(c=>c.mrr);
return {
text:'Top 5 Customers by MRR:<br>'+rows,
mini:renderMiniChart(data,'#818cf8')+'<div class="insight-label">Enterprise dominates top 3 (avg $36.3K MRR)</div>'
};
}
if(q.includes('compare')&&(q.includes('quarter')||q.includes('period')||q.includes('month'))){
let thisQ=revenueData.slice(-10).reduce((a,b)=>a+b,0);
let lastQ=revenueData.slice(-20,-10).reduce((a,b)=>a+b,0);
let pct=Math.round(((thisQ-lastQ)/lastQ)*100);
let compareData=[lastQ/10,thisQ/10];
return {
text:'Quarter comparison: Current period $'+thisQ.toLocaleString()+' vs previous $'+lastQ.toLocaleString()+' = <strong>+'+pct+'% growth</strong>.<br>Enterprise segment grew +18%, Mid-Market +12%, Startup +9%.',
mini:renderMiniChart(compareData,'#34d399')+'<div class="insight-label">Current period avg: $'+(thisQ/10).toLocaleString()+' per interval</div>'
};
}
if(q.includes('segment')&&(q.includes('fastest')||q.includes('grew')||q.includes('growth'))){
return {
text:'Fastest growing segment: <strong>Startup</strong> at +35% MoM (driven by 12 new accounts).<br>Enterprise: +18% (expansion revenue), Mid-Market: +12% (stable renewals).<br>Recommendation: Increase outbound to Mid-Market — it has the lowest churn at 2.1%.',
mini:renderMiniChart([18,12,35],'#38bdf8')+'<div class="insight-label">Growth rate by segment: Enterprise | Mid-Market | Startup</div>'
};
}
if(q.includes('forecast')||q.includes('predict')||q.includes('next month')||q.includes('projection')){
let avgGrowth=revenueData.slice(-7).reduce((a,b,i,arr)=>a+((b-arr[Math.max(0,i-1)])/arr[Math.max(0,i-1)])*100,0)/7;
let projected=Math.round(revenueData[revenueData.length-1]*(1+avgGrowth/100));
return {
text:'Based on the trailing 7-day growth rate of '+avgGrowth.toFixed(1)+'%, next period is projected at $'+projected.toLocaleString()+'.<br>Confidence: medium-high (consistent weekly patterns). Watch for end-of-quarter acceleration.',
mini:renderMiniChart(revenueData.slice(-7).concat(projected),'#38bdf8')+'<div class="insight-label">Projected: $'+projected.toLocaleString()+' (▲'+avgGrowth.toFixed(1)+'%)</div>'
};
}
if(q.includes('dip')||q.includes('drop')||q.includes('decline')||q.includes('why')&&q.includes('down')){
return {
text:'The D7-D8 dip correlates with a weekend period (Sat-Sun). B2B SaaS typically sees 25-30% lower activity on weekends. The D14 dip matches a US public holiday. No structural issues detected — both dips rebounded within 48 hours.',
mini:renderMiniChart(revenueData.slice(5,12),'#ef4444')+'<div class="insight-label">Weekend dip pattern: -22% avg, full recovery by Tuesday</div>'
};
}
let totals = revenueData.reduce((a,b)=>a+b,0);
return {
text:'Here is the current revenue snapshot: Last 30 days total $'+totals.toLocaleString()+'. MRR at $284,500 (+12.4%). 1,847 active customers (+5.2%). Ask me about trends, comparisons, or specific segments.',
mini:renderMiniChart(revenueData,'#38bdf8')+'<div class="insight-label">30-day overview: $'+totals.toLocaleString()+' total</div>'
};
}
function handleQuery(query){
if(!query.trim()) return;
document.getElementById('queryInput').value='';
addMessage('user',query);
addTypingIndicator();
document.getElementById('sendBtn').disabled=true;
setTimeout(function(){
removeTypingIndicator();
let response=generateResponse(query);
addMessage('assistant',response.text,response.mini);
document.getElementById('sendBtn').disabled=false;
},600+Math.random()*400);
}
document.getElementById('sendBtn').addEventListener('click',function(){
handleQuery(document.getElementById('queryInput').value);
});
document.getElementById('queryInput').addEventListener('keydown',function(e){
if(e.key==='Enter') handleQuery(this.value);
});
document.getElementById('suggestionBar').addEventListener('click',function(e){
if(e.target.tagName==='BUTTON'){
handleQuery(e.target.getAttribute('data-query'));
}
});
document.getElementById('dateRange').addEventListener('change',function(){
let val=this.value;
let titleEl=document.getElementById('chartTitle');
let periodLabels={7d:'Last 7 Days',30d:'Last 30 Days',90d:'Last Quarter',1y:'Year to Date'};
titleEl.textContent=currentView.charAt(0).toUpperCase()+currentView.slice(1)+' Trend — '+periodLabels[val];
let insightEl=document.getElementById('chartInsight');
insightEl.textContent='Filters updated to '+periodLabels[val]+'. The copilot context has been refreshed with the new date range.';
});
document.getElementById('segmentFilter').addEventListener('change',function(){
let val=this.value;
let insightEl=document.getElementById('chartInsight');
if(val==='all'){
insightEl.textContent='Showing all segments. Enterprise leads at 52% of revenue share.';
}else if(val==='enterprise'){
insightEl.textContent='Enterprise segment: $148K MRR, 240 accounts, 18% MoM growth. Churn: 1.2%.';
}else if(val==='midmarket'){
insightEl.textContent='Mid-Market segment: $82K MRR, 580 accounts, 12% MoM growth. Churn: 2.1%.';
}else if(val==='startup'){
insightEl.textContent='Startup segment: $54K MRR, 1,027 accounts, 35% MoM growth. Churn: 4.5%.';
}
});
document.getElementById('metricToggle').addEventListener('change',function(){
let view=this.value;
currentView=view;
let data=getChartData(view);
let titleMap={mrr:'MRR',revenue:'Revenue',customers:'Customers'};
document.getElementById('chartTitle').textContent=titleMap[view]+' Trend — Last 30 Days';
chart.data.datasets[0].label=data.label;
chart.data.datasets[0].data=data.data;
chart.data.datasets[0].borderColor=data.color;
chart.data.datasets[0].backgroundColor=data.color.replace(')',',0.08)').replace('rgb','rgba');
chart.data.datasets[0].pointBackgroundColor=data.color;
chart.update();
document.getElementById('chartInsight').textContent=insights[view];
let metricMap={mrr:'$284,500',revenue:'$892,300',customers:'1,847'};
if(view==='mrr'){document.getElementById('metricMRR').textContent='$284,500';document.getElementById('metricRevenue').textContent='$892,300';document.getElementById('metricCustomers').textContent='1,847';}
if(view==='revenue'){document.getElementById('metricMRR').textContent='$284,500';document.getElementById('metricRevenue').textContent='$892,300';document.getElementById('metricCustomers').textContent='1,847';}
if(view==='customers'){document.getElementById('metricMRR').textContent='$284,500';document.getElementById('metricRevenue').textContent='$892,300';document.getElementById('metricCustomers').textContent='1,847';}
});
})();
</script>
</body>
</html>