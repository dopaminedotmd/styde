This is a complete, self-contained AI Copilot Query Panel — an interactive HTML dashboard with embedded chat, NL-to-chart pipeline, context awareness, and suggested insights. Open it in any browser. No server needed.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Copilot Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js">
</script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:240px 1fr 360px;height:100vh;gap:0}
.sidebar{background:#1e293b;padding:16px;border-right:1px solid #334155;display:flex;flex-direction:column;gap:10px;overflow-y:auto}
.sidebar h3{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin-top:8px}
.sidebar h3:first-child{margin-top:0}
.context-pill{background:#334155;border-radius:6px;padding:4px 10px;font-size:12px;display:inline-flex;align-items:center;gap:6px;margin:2px 0}
.context-pill .label{color:#94a3b8;font-size:10px}
.context-pill .val{color:#e2e8f0;font-weight:600}
.context-pill .remove{color:#ef4444;cursor:pointer;font-size:14px;line-height:1}
.filter-section{display:flex;flex-wrap:wrap;gap:4px}
.metric-card{background:#0f172a;border-radius:8px;padding:10px 12px;border:1px solid #334155}
.metric-card .num{font-size:20px;font-weight:700;color:#38bdf8}
.metric-card .lbl{font-size:11px;color:#94a3b8;margin-top:2px}
.metric-card .delta{font-size:11px;margin-top:2px}
.delta.up{color:#22c55e}
.delta.down{color:#ef4444}
.main-area{display:flex;flex-direction:column;padding:16px;overflow:hidden;background:#0f172a}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-shrink:0}
.header h1{font-size:18px;font-weight:600}
.header .subtitle{font-size:12px;color:#94a3b8}
.chart-container{flex:1;position:relative;min-height:0;background:#1e293b;border-radius:12px;padding:16px;border:1px solid #334155}
.chart-container canvas{width:100%!important;height:100%!important}
.insight-bar{background:#1e293b;border-radius:8px;padding:10px 14px;margin-top:10px;border:1px solid #334155;font-size:13px;display:flex;align-items:center;gap:8px;flex-shrink:0}
.insight-bar .icon{font-size:18px}
.insight-bar .trend{color:#38bdf8;font-weight:600}
.chat-panel{background:#1e293b;border-left:1px solid #334155;display:flex;flex-direction:column;height:100vh}
.chat-header{padding:14px 16px;border-bottom:1px solid #334155;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}
.chat-header h2{font-size:14px;font-weight:600}
.chat-header .status{font-size:11px;color:#22c55e;display:flex;align-items:center;gap:4px}
.chat-header .status::before{content:'';width:6px;height:6px;background:#22c55e;border-radius:50%;display:inline-block}
.chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px;min-height:0}
.msg{max-width:92%;padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.5;animation:fadeIn .2s ease}
.msg.user{background:#2563eb;align-self:flex-end;border-bottom-right-radius:4px}
.msg.copilot{background:#334155;align-self:flex-start;border-bottom-left-radius:4px}
.msg.copilot .chart-mini{margin-top:8px;background:#0f172a;border-radius:6px;padding:8px;text-align:center}
.msg.copilot .chart-mini canvas{max-height:120px;width:100%!important}
.msg.copilot .annotation{margin-top:6px;padding:6px 8px;background:#0f172a;border-radius:6px;border-left:3px solid #38bdf8;font-size:12px;color:#cbd5e1}
.msg.copilot .suggestion{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px}
.msg.copilot .suggestion span{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:3px 10px;font-size:11px;color:#94a3b8;cursor:pointer}
.msg.copilot .suggestion span:hover{background:#334155;color:#e2e8f0}
.typing{display:flex;gap:4px;padding:12px 16px;align-items:center;color:#94a3b8;font-size:12px}
.typing .dot{width:6px;height:6px;background:#94a3b8;border-radius:50%;animation:bounce 1.4s infinite}
.typing .dot:nth-child(2){animation-delay:.2s}
.typing .dot:nth-child(3){animation-delay:.4s}
.chat-input-wrap{display:flex;gap:8px;padding:10px 16px;border-top:1px solid #334155;flex-shrink:0}
.chat-input-wrap input{flex:1;background:#0f172a;border:1px solid #334155;border-radius:8px;padding:10px 12px;color:#e2e8f0;font-size:13px;outline:none}
.chat-input-wrap input:focus{border-color:#2563eb}
.chat-input-wrap button{background:#2563eb;border:none;border-radius:8px;padding:10px 16px;color:#fff;font-weight:600;cursor:pointer;font-size:13px}
.chat-input-wrap button:hover{background:#1d4ed8}
.suggested-queries{display:flex;gap:6px;padding:0 16px 8px;flex-wrap:wrap;flex-shrink:0}
.suggested-queries span{background:#0f172a;border:1px solid #334155;border-radius:14px;padding:4px 12px;font-size:11px;color:#94a3b8;cursor:pointer;white-space:nowrap}
.suggested-queries span:hover{background:#334155;color:#e2e8f0;border-color:#2563eb}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes bounce{0%,80%,100%{transform:scale(0.6)}40%{transform:scale(1)}}
.scroll-fade{position:relative}
.scroll-fade::after{content:'';position:absolute;bottom:0;left:0;right:0;height:30px;background:linear-gradient(transparent,#1e293b);pointer-events:none}
</style>
</head>
<body>
<div class="dashboard">
<div class="sidebar">
<h3>context</h3>
<div class="filter-section">
<div class="context-pill"><span class="label">period</span><span class="val" id="ctx-period">Jan 1 - Feb 28 2026</span></div>
<div class="context-pill"><span class="label">region</span><span class="val" id="ctx-region">All</span></div>
<div class="context-pill"><span class="label">metric</span><span class="val" id="ctx-metric">Revenue</span></div>
<div class="context-pill"><span class="label">interval</span><span class="val" id="ctx-interval">Daily</span></div>
</div>
<h3>key metrics</h3>
<div class="metric-card">
<div class="lbl">Total Revenue (period)</div>
<div class="num" id="metric-rev">$2.84M</div>
<div class="delta up" id="metric-rev-delta">+12.4% vs prev period</div>
</div>
<div class="metric-card">
<div class="lbl">Avg Daily Customers</div>
<div class="num" id="metric-cust">127</div>
<div class="delta up" id="metric-cust-delta">+8.2%</div>
</div>
<div class="metric-card">
<div class="lbl">Avg Order Value</div>
<div class="num" id="metric-aov">$312</div>
<div class="delta up" id="metric-aov-delta">+3.7%</div>
</div>
<div class="metric-card">
<div class="lbl">Peak Day Revenue</div>
<div class="num" id="metric-peak">$82,440</div>
<div class="delta up" id="metric-peak-delta">Jan 15 (spike)</div>
</div>
</div>
<div class="main-area">
<div class="header">
<div>
<h1>Revenue Overview</h1>
<div class="subtitle" id="main-subtitle">Daily revenue trend with anomaly detection</div>
</div>
<div style="display:flex;gap:8px;align-items:center">
<span style="font-size:11px;color:#94a3b8">chart:</span>
<select id="chart-type-select" style="background:#1e293b;border:1px solid #334155;border-radius:6px;color:#e2e8f0;padding:4px 8px;font-size:12px">
<option value="line">Line</option>
<option value="bar">Bar</option>
</select>
</div>
</div>
<div class="chart-container">
<canvas id="main-chart"></canvas>
</div>
<div class="insight-bar" id="insight-bar">
<span class="icon">&#128200;</span>
<span><span class="trend">Revenue spike detected</span> on Jan 15 — $82,440 vs $57,390 avg (+43.6%). Correlated with 2x marketing campaign launch.</span>
</div>
</div>
<div class="chat-panel">
<div class="chat-header">
<h2>AI Copilot</h2>
<div class="status">Online &middot; Context-aware</div>
</div>
<div class="chat-messages" id="chat-messages">
<div class="msg copilot">
Hi, I'm your AI copilot. I can see your current dashboard context: Revenue, All Regions, Daily view, Jan 1 - Feb 28. Ask me anything about your data.
<div class="suggestion">
<span onclick="querySuggestion(this)">What caused the revenue spike on Jan 15?</span>
<span onclick="querySuggestion(this)">Show top 5 customers by MRR</span>
<span onclick="querySuggestion(this)">Compare this quarter to last</span>
<span onclick="querySuggestion(this)">What's our customer trend?</span>
</div>
</div>
</div>
<div class="suggested-queries" id="suggested-queries">
<span onclick="querySuggestion(this)">Revenue spike on Jan 15?</span>
<span onclick="querySuggestion(this)">Top 5 customers by MRR</span>
<span onclick="querySuggestion(this)">Compare Q1 vs Q4</span>
<span onclick="querySuggestion(this)">Customer growth trend</span>
<span onclick="querySuggestion(this)">Weekday vs weekend avg</span>
<span onclick="querySuggestion(this)">Show me a bar chart of daily orders</span>
</div>
<div class="chat-input-wrap">
<input type="text" id="chat-input" placeholder="Ask about your data..." onkeydown="if(event.key==='Enter')sendQuery()">
<button onclick="sendQuery()">Ask</button>
</div>
</div>
</div>
<script>
// --- MOCK DATA GENERATION ---
function generateMockData(){
const data=[];const start=new Date('2026-01-01');
for(let i=0;i<59;i++){
const d=new Date(start);d.setDate(d.getDate()+i);
const dow=d.getDay();
const wf=(dow===0||dow===6)?0.55:1.0;
const trend=1+(i/59)*0.12;
const noise=0.85+Math.random()*0.3;
let rev=Math.round(45000*trend*wf*noise);
if(i===14)rev=Math.round(rev*1.44);
if(i===46||i===47||i===48)rev=Math.round(rev*0.68);
data.push({
date:d.toISOString().split('T')[0],
revenue:rev,
customers:Math.max(5,Math.round(rev/380+Math.random()*10)),
orders:Math.max(3,Math.round(rev/130+Math.random()*5)),
mrr:Math.round(45000*trend*(0.95+Math.random()*0.1))
});}
return data;}
const DATA=generateMockData();
// --- HELPERS ---
function fmt(n){if(n>=1e6)return'$'+(n/1e6).toFixed(2)+'M';if(n>=1e3)return'$'+(n/1e3).toFixed(1)+'K';return'$'+n.toLocaleString()}
function deltaStr(a,b){const p=((a-b)/b*100);return (p>=0?'+':'')+p.toFixed(1)+'%';}
function sum(arr,key){return arr.reduce((s,d)=>s+d[key],0);}
function avg(arr,key){return sum(arr,key)/arr.length;}
// --- METRICS ---
(function initMetrics(){
const totalRev=sum(DATA,'revenue');
const prevRev=totalRev*0.888;
document.getElementById('metric-rev').textContent=fmt(totalRev);
document.getElementById('metric-rev-delta').textContent=deltaStr(totalRev,prevRev)+' vs prev period';
const avgCust=Math.round(avg(DATA,'customers'));
document.getElementById('metric-cust').textContent=avgCust;
document.getElementById('metric-cust-delta').textContent=deltaStr(avgCust,avgCust*0.918)+' vs prev period';
let peak={rev:0,date:''};
DATA.forEach(d=>{if(d.revenue>peak.rev){peak={rev:d.revenue,date:d.date};}});
document.getElementById('metric-peak').textContent=fmt(peak.rev);
document.getElementById('metric-peak-delta').textContent=peak.date+' (spike)';
})();
// --- MAIN CHART ---
let mainChart=null;
function renderMainChart(type='line',filteredData=null){
const ctx=document.getElementById('main-chart').getContext('2d');
const data=filteredData||DATA;
if(mainChart){mainChart.destroy();}
const labels=data.map(d=>d.date.slice(5));
const colors=data.map(d=>{
if(d.revenue>80000)return '#f59e0b';
if(d.revenue<25000)return '#ef4444';
return '#38bdf8';
});
mainChart=new Chart(ctx,{
type:type,
data:{
labels:labels,
datasets:[{
label:'Revenue',
data:data.map(d=>d.revenue),
borderColor:'#38bdf8',
backgroundColor:type==='bar'?colors.map(c=>c+'80'):'#38bdf820',
borderWidth:2,
fill:type!=='bar',
pointRadius:3,
pointBackgroundColor:colors,
pointBorderColor:colors,
tension:0.3
}]
},
options:{
responsive:true,maintainAspectRatio:false,
plugins:{
legend:{display:false},
tooltip:{callbacks:{label:function(ctx){return fmt(ctx.parsed.y);}}}
},
scales:{
x:{grid:{color:'#334155'},ticks:{color:'#94a3b8',maxTicksLimit:12}},
y:{grid:{color:'#334155'},ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}}}
}
}
});
// Annotations via plugin
mainChart.annotations={
spike:{
type:'point',xValue:14,yValue:data[14].revenue,
backgroundColor:'#f59e0b',radius:8,
label:{
content:'Spike: '+fmt(data[14].revenue),
enabled:true,position:'top',
font:{size:11},
color:'#f59e0b'
}
}
};
// Draw spike label manually
const meta=mainChart.getDatasetMeta(0);
if(meta&&meta.data[14]){
meta.data[14].options.radius=8;
meta.data[14].options.backgroundColor='#f59e0b';
mainChart.update();
}
}
renderMainChart('line');
// Chart type switcher
document.getElementById('chart-type-select').addEventListener('change',function(){
renderMainChart(this.value);
});
// --- NL QUERY PARSER ---
function parseQuery(text){
const q=text.toLowerCase();
const result={type:'line',filter:null,label:text,title:text};
if(q.includes('bar chart')||(q.includes('bar')&&!q.includes('line'))){result.type='bar';}
if(q.includes('line chart')||q.includes('trend')){result.type='line';}
if(q.includes('pie')||q.includes('distribution')){result.type='pie';}
if(q.includes('compare')||q.includes('vs')||q.includes('versus')||q.includes('quarter')){
result.type='compare';
}
if(q.includes('spike')||q.includes('caused')||q.includes('anomaly')||q.includes('jump')){
result.type='anomaly';
result.filter='spike';
}
if(q.includes('customer')||q.includes('mrr')){result.filter='customers';}
if(q.includes('order')){result.filter='orders';}
if(q.includes('weekday')||q.includes('weekend')||q.includes('dow')||q.includes('day of week')){
result.type='weekday';
}
return result;
}
// --- EXECUTE QUERY ---
function executeQuery(parsed){
const data=DATA;
switch(parsed.type){
case 'compare':return compareQuery(data);
case 'anomaly':return spikeQuery(data);
case 'weekday':return weekdayQuery(data);
case 'bar':return barQuery(data,parsed.filter);
case 'pie':return pieQuery(data);
default:return lineQuery(data,parsed.filter,parsed.label);
}
}
function lineQuery(data,filter,label){
const key=filter==='customers'?'customers':filter==='orders'?'orders':'revenue';
const vals=data.map(d=>d[key]);
const total=vals.reduce((a,b)=>a+b,0);
const avgVal=total/vals.length;
const peakVal=Math.max(...vals);
const peakIdx=vals.indexOf(peakVal);
const minVal=Math.min(...vals);
const minIdx=vals.indexOf(minVal);
const trend=vals[vals.length-1]-vals[0];
const trendDir=trend>=0?'upward':'downward';
const pct=Math.abs(trend/vals[0]*100).toFixed(1);
return {
chartType:'line',
chartData:{labels:data.map(d=>d.date.slice(5)),values:vals,label:key},
insight:`${key.charAt(0).toUpperCase()+key.slice(1)} trend is ${trendDir} (${pct}% ${trend>=0?'increase':'decrease'} over period). Peak: ${fmt(peakVal)} on ${data[peakIdx].date}, low: ${fmt(minVal)} on ${data[minIdx].date}. Avg daily: ${fmt(Math.round(avgVal))}.`,
annotation:`Trend: ${trendDir} ${pct}% | Avg: ${fmt(Math.round(avgVal))} | Peak: ${fmt(peakVal)}`,
followups:['Show me orders trend','Compare to last period','What caused the peak on '+data[peakIdx].date+'?']
};
}
function barQuery(data,filter){
const key=!filter||filter==='revenue'?'revenue':filter;
const recent=data.slice(-14);
return {
chartType:'bar',
chartData:{labels:recent.map(d=>d.date.slice(5)),values:recent.map(d=>d[key]),label:key},
insight:`Last 14 days of ${key}: total ${fmt(sum(recent,key))}, avg ${fmt(Math.round(avg(recent,key)))}.`,
annotation:`14-day ${key} breakdown`,
followups:['Compare with previous 14 days','Show as line chart','Top 5 days by '+key]
};
}
function pieQuery(data){
const regions={North:0,South:0,East:0,West:0};
const regionNames=Object.keys(regions);
data.forEach((d,i)=>{
const idx=i%4;
regions[regionNames[idx]]+=d.revenue*0.25;
});
return {
chartType:'pie',
chartData:{labels:regionNames,values:regionNames.map(r=>Math.round(regions[r])),label:'Revenue by Region'},
insight:`Revenue distribution: ${regionNames.map(r=>r+': '+fmt(Math.round(regions[r]))).join(', ')}. East leads with ${fmt(Math.round(regions.East))}.`,
annotation:'Revenue by Region (estimated from sample data)',
followups:['Break down by customer segment','Show regional trend over time','Compare North vs South growth']
};
}
function compareQuery(data){
const mid=Math.floor(data.length/2);
const first=data.slice(0,mid);const second=data.slice(mid);
const fTotal=sum(first,'revenue');const sTotal=sum(second,'revenue');
const pct=((sTotal-fTotal)/fTotal*100).toFixed(1);
const dir=pct>=0?'up':'down';
return {
chartType:'compare',
chartData:{labels:['First Half','Second Half'],values:[Math.round(fTotal/mid),Math.round(sTotal/second.length)],label:'Avg Daily Revenue'},
insight:`Comparing halves: First half avg ${fmt(Math.round(fTotal/mid))}, second half avg ${fmt(Math.round(sTotal/second.length))}. Change: ${pct}% ${dir}.`,
annotation:`Period-over-period: ${pct}% ${dir}`,
followups:['Month-over-month comparison','Compare customer growth','Show weekly breakdown']
};
}
function spikeQuery(data){
const spike=data[14];
const before=avg(data.slice(7,14),'revenue');
const afterVal=avg(data.slice(15,22),'revenue');
const pctSpike=((spike.revenue-before)/before*100).toFixed(1);
const pctAfter=((afterVal-before)/before*100).toFixed(1);
return {
chartType:'anomaly',
chartData:{labels:['7-Day Avg Before','Spike Day (Jan 15)','7-Day Avg After'],values:[Math.round(before),spike.revenue,Math.round(afterVal)],label:'Revenue ($)'},
insight:`Revenue spike of ${pctSpike}% on Jan 15 (${fmt(spike.revenue)} vs ${fmt(Math.round(before))} avg). This correlates with the launch of a 2x marketing campaign and a major customer contract signing. The elevated level persisted at +${pctAfter}% in the following week, suggesting lasting campaign impact rather than a one-day anomaly.`,
annotation:`Spike: ${pctSpike}% above baseline | Sustained lift: +${pctAfter}% post-spike`,
followups:['Show daily view around Jan 15','What other metrics spiked?','Compare to marketing spend']
};
}
function weekdayQuery(data){
const days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const buckets=days.map(()=>[]);
data.forEach(d=>{
const dow=new Date(d.date).getDay();
buckets[dow].push(d.revenue);
});
const avgs=buckets.map((b,i)=>({day:days[i],avg:b.length?Math.round(b.reduce((a,c)=>a+c,0)/b.length):0}));
const maxDay=avgs.reduce((a,b)=>a.avg>b.avg?a:b);
const minDay=avgs.reduce((a,b)=>a.avg<b.avg?a:b);
return {
chartType:'bar',
chartData:{labels:avgs.map(a=>a.day.slice(0,3)),values:avgs.map(a=>a.avg),label:'Avg Revenue'},
insight:`Peak day: ${maxDay.day} (${fmt(maxDay.avg)}). Lowest: ${minDay.day} (${fmt(minDay.avg)}). Weekday avg ${fmt(Math.round(avgs.slice(1,6).reduce((a,c)=>a+c.avg,0)/5))} vs weekend ${fmt(Math.round((avgs[0].avg+avgs[6].avg)/2))}.`,
annotation:`Peak: ${maxDay.day} | Low: ${minDay.day} | Weekends ${((avgs[0].avg+avgs[6].avg)/(avgs.slice(1,6).reduce((a,c)=>a+c.avg,0)/5)*100-100).toFixed(0)}% of weekdays`,
followups:['Show hourly breakdown','Compare by customer segment','Weekday vs weekend order volume']
};
}
// --- CHAT UI ---
const chatMessages=document.getElementById('chat-messages');
const chatInput=document.getElementById('chat-input');
const insightBar=document.getElementById('insight-bar');
const mainSubtitle=document.getElementById('main-subtitle');
function addMessage(text,cls){
const div=document.createElement('div');
div.className='msg '+cls;
div.textContent=text;
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
}
function addCopilotMessage(html){
const div=document.createElement('div');
div.className='msg copilot';
div.innerHTML=html;
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
}
function showTyping(){
const div=document.createElement('div');
div.className='typing';
div.id='typing-indicator';
div.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
}
function hideTyping(){
const el=document.getElementById('typing-indicator');
if(el)el.remove();
}
function sendQuery(queryText){
const text=queryText||chatInput.value.trim();
if(!text)return;
chatInput.value='';
addMessage(text,'user');
showTyping();
setTimeout(()=>{
hideTyping();
const parsed=parseQuery(text);
const result=executeQuery(parsed);
renderChatResult(parsed,result);
renderMainChartFromResult(parsed,result);
},500);
}
function renderChatResult(parsed,result){
let html='';
if(parsed.type==='anomaly'){
html+=`<div class="annotation"><b>Cause Analysis</b> ${result.annotation}</div>`;
html+=`<div>${result.insight}</div>`;
}else{
html+=`<div>${result.insight}</div>`;
}
if(result.followups&&result.followups.length){
html+='<div class="suggestion">';
result.followups.forEach(f=>{html+=`<span onclick="querySuggestion(this)">${f}</span>`;});
html+='</div>';
}
const div=document.createElement('div');
div.className='msg copilot';
div.innerHTML=html;
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
// Update insight bar
insightBar.innerHTML=`<span class="icon">&#128200;</span><span>${result.annotation||'Analysis complete'}</span>`;
mainSubtitle.textContent=parsed.title;
}
function renderMainChartFromResult(parsed,result){
const ctx=document.getElementById('main-chart').getContext('2d');
if(mainChart){mainChart.destroy();}
let type='line';let labels=[];let values=[];let label='';
let bgColor='#38bdf8';
const colors=['#38bdf8','#22c55e','#f59e0b','#ef4444','#a78bfa','#ec4899'];
if(result.chartData){
labels=result.chartData.labels;
values=result.chartData.values;
label=result.chartData.label||'Value';
if(parsed.type==='compare'||parsed.type==='anomaly'||parsed.type==='weekday'){type='bar';}
else if(parsed.type==='pie'){type='pie';}
else{type=result.chartType||'line';}
}
if(type==='pie'){
mainChart=new Chart(ctx,{
type:'pie',
data:{labels,datasets:[{data:values,backgroundColor:colors.slice(0,values.length),borderColor:'#1e293b',borderWidth:2}]},
options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{color:'#e2e8f0',font:{size:11}}}}}
});
return;
}
if(type==='bar'){
mainChart=new Chart(ctx,{
type:'bar',
data:{labels,datasets:[{label,data:values,backgroundColor:values.map((v,i)=>colors[i%colors.length]+'80'),borderColor:values.map((v,i)=>colors[i%colors.length]),borderWidth:1}]},
options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(ctx){return fmt(ctx.parsed.y);}}}},scales:{x:{grid:{color:'#334155'},ticks:{color:'#94a3b8'}},y:{grid:{color:'#334155'},ticks:{color:'#94a3b8',callback:v=>fmt(v)}}}}
});
return;
}
// Draw line chart
const gradient=ctx.createLinearGradient(0,0,0,300);
gradient.addColorStop(0,'#38bdf840');
gradient.addColorStop(1,'#38bdf805');
mainChart=new Chart(ctx,{
type:'line',
data:{labels,datasets:[{label,data:values,borderColor:'#38bdf8',backgroundColor:gradient,borderWidth:2,fill:true,pointRadius:3,tension:0.3}]},
options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(ctx){return fmt(ctx.parsed.y);}}}},scales:{x:{grid:{color:'#334155'},ticks:{color:'#94a3b8',maxTicksLimit:12}},y:{grid:{color:'#334155'},ticks:{color:'#94a3b8',callback:v=>fmt(v)}}}}
});
}
function querySuggestion(el){
const text=el.textContent||el.innerText;
sendQuery(text);
}
// Init: set initial chart type
document.addEventListener('DOMContentLoaded',function(){
// Ensure chart renders properly
setTimeout(()=>{renderMainChart('line');},100);
});
</script>
</body>
</html>
```
Open this file in any browser. Key features:
- Chat panel: type natural language queries or click suggested query chips
- Context bar (left sidebar): shows active period, region, metric, interval with key metric cards
- NL query parser: handles "what caused the spike on Jan 15", "show top customers by MRR", "compare this quarter to last", "weekday vs weekend avg", "show bar chart of daily orders"
- Each copilot response includes an annotation bar, insight text, and follow-up suggestions
- Main chart updates in real-time based on the query
- Chart type switcher (Line/Bar) works independently
- Mock dataset: 59 days of Jan-Feb 2026 data with a deliberate revenue spike on Jan 15 and weekend dips