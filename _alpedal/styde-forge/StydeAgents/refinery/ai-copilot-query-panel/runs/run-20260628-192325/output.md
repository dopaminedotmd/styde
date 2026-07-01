<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>AI Copilot Dashboard</title>
<script src=https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js defer></script>
<script src=https://cdn.jsdelivr.net/npm/luxon@3.4.4/build/global/luxon.min.js defer></script>
<script src=https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.3.1/dist/chartjs-adapter-luxon.min.js defer></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fb;color:#1a1a2e;display:flex;height:100vh;overflow:hidden}
.dashboard{flex:1;display:flex;flex-direction:column;padding:20px}
.dashboard-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.filters{display:flex;gap:12px;align-items:center}
.filters select,.filters input{padding:6px 12px;border:1px solid #d0d5dd;border-radius:6px;font-size:13px;background:#fff}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.metric-card{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.metric-card .label{font-size:12px;color:#667085;margin-bottom:4px}
.metric-card .value{font-size:24px;font-weight:600}
.metric-card .delta{font-size:12px;margin-top:4px}
.delta.up{color:#16b364}.delta.down{color:#e53e3e}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0}
.chart-card{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.06);display:flex;flex-direction:column}
.chart-card h3{font-size:14px;font-weight:600;margin-bottom:8px;color:#344054}
.chart-wrapper{flex:1;position:relative;min-height:0}
.chart-wrapper canvas{width:100%!important;height:100%!important}
.copilot-panel{width:380px;background:#fff;border-left:1px solid #eaecf0;display:flex;flex-direction:column;flex-shrink:0}
.copilot-header{padding:16px 20px;border-bottom:1px solid #eaecf0;display:flex;justify-content:space-between;align-items:center}
.copilot-header h2{font-size:16px;font-weight:600}
.copilot-header .badge{background:#eef2ff;color:#3538cd;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:500}
.chat-history{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:16px}
.message{max-width:90%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5}
.message.user{background:#3538cd;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.message.assistant{background:#f2f4f7;color:#1d2939;align-self:flex-start;border-bottom-left-radius:4px}
.message.assistant .chart-inline{width:100%;height:140px;margin-top:8px;background:#f9fafb;border-radius:6px;position:relative}
.message.assistant .annotation{font-size:12px;color:#667085;margin-top:6px;padding:8px;background:#f9fafb;border-radius:6px;border-left:3px solid #3538cd}
.suggestions{padding:8px 20px;border-top:1px solid #eaecf0}
.suggestions .suggestion-chip{display:inline-block;padding:4px 12px;background:#f2f4f7;border-radius:16px;font-size:12px;color:#344054;cursor:pointer;margin:4px 4px 0 0;border:1px solid #eaecf0}
.suggestions .suggestion-chip:hover{background:#eef2ff;border-color:#3538cd;color:#3538cd}
.chat-input{display:flex;align-items:center;padding:12px 16px;border-top:1px solid #eaecf0;gap:8px}
.chat-input input{flex:1;padding:8px 12px;border:1px solid #d0d5dd;border-radius:8px;font-size:13px;outline:0}
.chat-input input:focus{border-color:#3538cd}
.chat-input button{background:#3538cd;color:#fff;border:none;padding:8px 16px;border-radius:8px;font-size:13px;cursor:pointer;font-weight:500}
.chat-input button:hover{background:#2e31a8}
</style>
</head>
<body>
<div class=dashboard>
  <div class=dashboard-header>
    <h1>Revenue Dashboard</h1>
    <div class=filters>
      <select id=period><option>Last 7 days<option>Last 30 days<option selected>This quarter<option>Year to date</select>
      <select id=region><option selected>All regions<option>North America<option>Europe<option>APAC</select>
      <input type=text placeholder="Filter by segment..." id=segmentFilter>
    </div>
  </div>
  <div class=metrics>
    <div class=metric-card><div class=label>Total Revenue</div><div class=value>$847,230</div><div class="delta up">+12.3% vs prev period</div></div>
    <div class=metric-card><div class=label>Active Customers</div><div class=value>1,284</div><div class="delta up">+8.1%</div></div>
    <div class=metric-card><div class=label>MRR</div><div class=value>$94,150</div><div class="delta up">+3.2%</div></div>
    <div class=metric-card><div class=label>Churn Rate</div><div class=value>2.1%</div><div class="delta down">+0.4pp</div></div>
  </div>
  <div class=chart-grid>
    <div class=chart-card><h3>Revenue Trend</h3><div class=chart-wrapper><canvas id=revenueChart></canvas></div></div>
    <div class=chart-card><h3>Top Customers by MRR</h3><div class=chart-wrapper><canvas id=customersChart></canvas></div></div>
  </div>
</div>
<div class=copilot-panel>
  <div class=copilot-header>
    <h2>Copilot</h2>
    <span class=badge>context-aware</span>
  </div>
  <div class=chat-history id=chatHistory>
    <div class="message assistant">Hi, I'm your AI copilot. I see current filters: This quarter, All regions. Ask me anything about your data.</div>
    <div class="message user">What caused the revenue spike last Tuesday?</div>
    <div class="message assistant">
      <div class=chart-inline><canvas id=inlineChart1></canvas></div>
      <div class=annotation>The revenue spike on Tuesday June 24 (+37% vs daily avg) was driven by a $28K enterprise deal from Acme Corp and a 22% surge in subscription upgrades following the feature release email. Seasonal patterns show Tuesdays typically run 8% above average, but this was an outlier.</div>
    </div>
    <div class="message user">Show me our top 5 customers by MRR</div>
    <div class="message assistant">
      Top 5 customers by MRR:
      Acme Corp ($22,400), Globex Inc ($18,900), Initech ($15,200), Hooli ($11,800), Dunder Mifflin ($10,500). These 5 represent 83% of total MRR.
      <div class=chart-inline><canvas id=inlineChart2></canvas></div>
    </div>
  </div>
  <div class=suggestions>
    <span class="suggestion-chip" data-q="Compare this quarter to last">Compare this quarter to last</span>
    <span class="suggestion-chip" data-q="Which segment grew fastest">Which segment grew fastest</span>
    <span class="suggestion-chip" data-q="Forecast next month MRR">Forecast next month MRR</span>
  </div>
  <div class=chat-input>
    <input type=text id=chatInput placeholder="Ask about your data..." autofocus>
    <button id=sendBtn>Ask</button>
  </div>
</div>
<script>
(function(){
const COLORS={primary:'#3538cd',green:'#16b364',orange:'#f79009',red:'#e53e3e'}
function timeSeriesData(){
const data=[],labels=[]
const now=Date.now()
for(let i=29;i>=0;i--){
const d=new Date(now-i*86400000)
labels.push(d.toISOString().slice(0,10))
let val=22000+Math.sin(i*0.3)*3000+Math.random()*4000
if(i===24)val+=28000
if(i===18)val-=12000
if(i===10)val+=8000
data.push(Math.round(val))
}
return{labels,data}
}
function initCharts(){
const revCtx=document.getElementById('revenueChart')
if(revCtx){
const ts=timeSeriesData()
new Chart(revCtx,{type:'line',data:{labels:ts.labels,datasets:[{label:'Revenue',data:ts.data,borderColor:COLORS.primary,backgroundColor:(ctx)=>{
const g=ctx.chart.ctx.createLinearGradient(0,0,0,300)
g.addColorStop(0,'rgba(53,56,205,0.15)')
g.addColorStop(1,'rgba(53,56,205,0)')
return g
},fill:true,tension:0.3,pointRadius:3,pointBackgroundColor:COLORS.primary,borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d2939',titleFont:{size:12},bodyFont:{size:12},cornerRadius:6}},scales:{x:{grid:{display:false},ticks:{font:{size:11}}},y:{beginAtZero:true,grid:{color:'rgba(0,0,0,0.06)'},ticks:{font:{size:11}}}}}})
}
const custCtx=document.getElementById('customersChart')
if(custCtx){
const customers=['Acme Corp','Globex Inc','Initech','Hooli','Dunder Mifflin','Stark Industries','Wayne Enterprises','Oscorp']
const vals=[22400,18900,15200,11800,10500,6700,5200,4100]
new Chart(custCtx,{type:'bar',data:{labels:customers,datasets:[{label:'MRR ($)',data:vals,backgroundColor:[COLORS.primary,'#5a5de0','#7c7fe8','#9ea0f0','#b9baf5','#d4d4fa','#e8e8fc','#f2f2fe'],borderRadius:4,borderSkipped:false}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d2939',cornerRadius:6,callbacks:{label:(ctx)=>'$'+ctx.parsed.x.toLocaleString()}}},scales:{x:{beginAtZero:true,grid:{color:'rgba(0,0,0,0.06)'},ticks:{font:{size:11}}},y:{grid:{display:false},ticks:{font:{size:11}}}}}})
}
}
function initInlineCharts(){
const c1=document.getElementById('inlineChart1')
if(c1){
const parent=c1.closest('.chart-inline')
if(parent){
new Chart(c1,{type:'line',data:{labels:['Mon','Tue (spike)','Wed','Thu','Fri','Sat','Sun'],datasets:[{label:'Revenue',data:[21000,37600,22500,23800,24200,19800,20500],borderColor:COLORS.primary,tension:0.3,fill:false,borderWidth:2,pointRadius:[4,6,4,4,4,4,4],pointBackgroundColor:COLORS.primary,pointBorderColor:['#3538cd','#e53e3e','#3538cd','#3538cd','#3538cd','#3538cd','#3538cd']}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d2939'}},scales:{x:{grid:{display:false},ticks:{font:{size:10}}},y:{beginAtZero:true,grid:{color:'rgba(0,0,0,0.04)'},ticks:{font:{size:10}}}}}})
}
}
const c2=document.getElementById('inlineChart2')
if(c2){
const parent=c2.closest('.chart-inline')
if(parent){
new Chart(c2,{type:'doughnut',data:{labels:['Acme Corp','Globex Inc','Initech','Hooli','Dunder Mifflin','Others'],datasets:[{data:[22400,18900,15200,11800,10500,16000],backgroundColor:[COLORS.primary,'#5a5de0','#7c7fe8','#9ea0f0','#b9baf5','#e8e8fc'],borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:10},boxWidth:10,padding:8}},tooltip:{backgroundColor:'#1d2939',cornerRadius:6,callbacks:{label:(ctx)=>{const total=ctx.dataset.data.reduce((a,b)=>a+b,0);return ctx.label+': $'+ctx.parsed.toLocaleString()+' ('+Math.round(ctx.parsed/total*100)+'%)'}}}}}})
}
}
}
function loadChartJsAndInit(){
if(typeof Chart!=='undefined'){initCharts();initInlineCharts()}
else{document.addEventListener('DOMContentLoaded',()=>{setTimeout(()=>{initCharts();initInlineCharts()},500)})}
}
loadChartJsAndInit()
const sendBtn=document.getElementById('sendBtn')
const chatInput=document.getElementById('chatInput')
const chatHistory=document.getElementById('chatHistory')
function addMessage(text,role='user'){
const div=document.createElement('div')
div.className='message '+role
div.textContent=text
chatHistory.appendChild(div)
chatHistory.scrollTop=chatHistory.scrollHeight
}
function handleQuery(query){
const lower=query.toLowerCase()
if(lower.includes('spike')||lower.includes('tuesday')){
addMessage(query,'user')
addMessage('The revenue spike on Tuesday June 24 (+37% vs daily avg) was driven by a $28K enterprise deal from Acme Corp and a 22% surge in subscription upgrades following the feature release email. Seasonal patterns show Tuesdays typically run 8% above average, but this was an outlier.','assistant')
}
else if(lower.includes('customer')||lower.includes('mrr')||lower.includes('top')){
addMessage(query,'user')
addMessage('Top 5 customers by MRR:\nAcme Corp ($22,400), Globex Inc ($18,900), Initech ($15,200), Hooli ($11,800), Dunder Mifflin ($10,500). These 5 represent 83% of total MRR.\nConcentration risk: losing the top customer would reduce MRR by 24%.','assistant')
}
else if(lower.includes('compare')&&lower.includes('quarter')){
addMessage(query,'user')
addMessage('This quarter vs last quarter:\nRevenue: $847K vs $724K (+17%)\nNew customers: 142 vs 98 (+45%)\nAvg deal size: $5,970 vs $5,120 (+16.6%)\nChurn: 2.1% vs 2.8% (-0.7pp)\nDrivers: Q2 campaign + product launch in April.','assistant')
}
else if(lower.includes('segment')||lower.includes('grew')){
addMessage(query,'user')
addMessage('Fastest growing segments this quarter:\n1. Enterprise: +31% (driven by 3 new six-figure deals)\n2. Mid-market: +18%\n3. SMB: +9%\nEnterprise is outpacing other segments 2:1. Consider allocating more SDR resources there.','assistant')
}
else if(lower.includes('forecast')||lower.includes('next month')){
addMessage(query,'user')
addMessage('Based on current pipeline ($1.2M weighted) and seasonal trends, next month MRR forecast:\nConservative: $96,200 (+2.2%)\nBase: $98,500 (+4.6%)\nOptimistic: $103,800 (+10.2%)\nKey variables: 3 enterprise deals in late-stage negotiation, expected close rate ~60%.','assistant')
}
else{
addMessage(query,'user')
addMessage('I see you asked: "'+query+'". Based on the current dashboard context (This quarter, All regions), I can help with:\n- Revenue trends and anomalies\n- Customer segmentation and ranking\n- Quarter-over-quarter comparisons\n- Growth analysis by segment\n- MRR forecasting\nCould you rephrase or pick one of these topics?','assistant')
}
chatInput.value=''
}
if(sendBtn){
sendBtn.addEventListener('click',()=>{
const q=chatInput.value.trim()
if(q)handleQuery(q)
})
}
if(chatInput){
chatInput.addEventListener('keydown',(e)=>{
if(e.key==='Enter'){const q=chatInput.value.trim();if(q)handleQuery(q)}
})
}
document.querySelectorAll('.suggestion-chip').forEach(chip=>{
chip.addEventListener('click',()=>{
const q=chip.dataset.q
if(q)handleQuery(q)
})
})
})()
</script>
</body>
</html>