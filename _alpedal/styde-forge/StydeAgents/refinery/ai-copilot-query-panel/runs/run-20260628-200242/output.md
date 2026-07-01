```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f2f5;color:#1a1a2e;height:100vh;overflow:hidden}
.dashboard{display:flex;height:100vh}
.main{flex:1;display:flex;flex-direction:column;overflow:hidden}
.header{background:#fff;padding:16px 24px;border-bottom:1px solid #e0e3eb;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.header h1{font-size:20px;font-weight:600}
.header-controls{display:flex;gap:12px;align-items:center}
.filter-group{display:flex;gap:8px;align-items:center}
.filter-group label{font-size:12px;color:#666;font-weight:500}
.filter-group select,.filter-group input{padding:6px 10px;border:1px solid #d0d5dd;border-radius:6px;font-size:13px;background:#fff}
.filter-group input[type=date]{width:140px}
.metrics-bar{display:flex;gap:16px;padding:16px 24px;background:#fff;border-bottom:1px solid #e0e3eb;flex-shrink:0}
.metric-card{flex:1;padding:12px 16px;border-radius:8px;background:#f8f9fc;border:1px solid #e8ecf0}
.metric-card .label{font-size:11px;color:#666;text-transform:uppercase;letter-spacing:.5px}
.metric-card .value{font-size:22px;font-weight:700;margin-top:4px}
.metric-card .change{font-size:12px;margin-top:2px}
.metric-card .change.up{color:#059669}
.metric-card .change.down{color:#dc2626}
.content{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;padding:16px;overflow:auto}
.chart-panel{background:#fff;border-radius:10px;border:1px solid #e0e3eb;padding:16px;display:flex;flex-direction:column;overflow:hidden}
.chart-panel .chart-title{font-size:14px;font-weight:600;margin-bottom:8px;color:#333}
.chart-panel .chart-subtitle{font-size:11px;color:#888;margin-bottom:12px}
.chart-panel svg{flex:1;width:100%;min-height:0}
.chart-panel .chart-annotation{font-size:11px;color:#666;margin-top:8px;padding:8px 10px;background:#f0f4ff;border-radius:6px;border-left:3px solid #3b82f6}
.chart-panel.full{grid-column:1/-1}
.copilot-panel{width:380px;background:#fff;border-left:1px solid #e0e3eb;display:flex;flex-direction:column;flex-shrink:0}
.copilot-header{padding:16px;border-bottom:1px solid #e0e3eb;font-weight:600;font-size:15px;display:flex;align-items:center;gap:8px}
.copilot-header .status{width:8px;height:8px;border-radius:50%;background:#059669}
.copilot-messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.message{max-width:90%;padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.5;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.message.user{background:#3b82f6;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.message.copilot{background:#f0f2f5;color:#1a1a2e;align-self:flex-start;border-bottom-left-radius:4px}
.message.copilot .chart-inline{width:100%;margin-top:8px;border-radius:6px;background:#fff;padding:8px}
.message.copilot .chart-inline svg{width:100%;height:auto}
.message.copilot .metric-inline{display:flex;gap:8px;margin-top:6px;flex-wrap:wrap}
.message.copilot .metric-inline .pill{padding:4px 10px;border-radius:12px;font-size:11px;font-weight:500}
.message.copilot .metric-inline .pill.green{background:#d1fae5;color:#065f46}
.message.copilot .metric-inline .pill.red{background:#fee2e2;color:#991b1b}
.message.copilot .metric-inline .pill.blue{background:#dbeafe;color:#1e40af}
.suggestions{display:flex;gap:6px;flex-wrap:wrap;padding:8px 12px;border-top:1px solid #e0e3eb}
.suggestions .chip{padding:5px 10px;border-radius:14px;background:#f0f2f5;border:1px solid #d0d5dd;font-size:11px;color:#555;cursor:pointer;transition:all .15s}
.suggestions .chip:hover{background:#3b82f6;color:#fff;border-color:#3b82f6}
.copilot-input{display:flex;padding:10px 12px;border-top:1px solid #e0e3eb;gap:8px}
.copilot-input input{flex:1;padding:8px 12px;border:1px solid #d0d5dd;border-radius:8px;font-size:13px;outline:none}
.copilot-input input:focus{border-color:#3b82f6}
.copilot-input button{padding:8px 16px;background:#3b82f6;color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer}
.copilot-input button:hover{background:#2563eb}
.loading-dots{display:flex;gap:3px;padding:4px 0}
.loading-dots span{width:6px;height:6px;border-radius:50%;background:#999;animation:bounce 1.2s infinite}
.loading-dots span:nth-child(2){animation-delay:.2s}
.loading-dots span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}
.no-chart{display:flex;align-items:center;justify-content:center;flex:1;color:#aaa;font-size:13px}
</style>
</head>
<body>
<div class="dashboard">
<div class="main">
<div class="header">
<h1>Styde Forge Analytics</h1>
<div class="header-controls">
<div class="filter-group">
<label>Period</label>
<input type="date" id="dateFrom" value="2026-06-01">
<input type="date" id="dateTo" value="2026-06-28">
</div>
<div class="filter-group">
<label>Metric</label>
<select id="metricSelect"><option value="revenue">Revenue</option><option value="mrr">MRR</option><option value="users">Users</option><option value="churn">Churn</option></select>
</div>
<div class="filter-group">
<label>Segment</label>
<select id="segmentSelect"><option value="all">All</option><option value="enterprise">Enterprise</option><option value="smb">SMB</option><option value="startup">Startup</option></select>
</div>
</div>
</div>
<div class="metrics-bar" id="metricsBar"></div>
<div class="content" id="chartGrid">
<div class="chart-panel" id="chartRevenue"><div class="chart-title">Revenue Trend</div><div class="chart-subtitle">Daily revenue for selected period</div><svg id="svgRevenue"></svg></div>
<div class="chart-panel" id="chartTopCustomers"><div class="chart-title">Top Customers by MRR</div><div class="chart-subtitle">Highest MRR contributors</div><svg id="svgCustomers"></svg></div>
<div class="chart-panel" id="chartBreakdown"><div class="chart-title">Revenue by Segment</div><div class="chart-subtitle">Current period breakdown</div><svg id="svgBreakdown"></svg></div>
<div class="chart-panel" id="chartComparison"><div class="chart-title">Quarter Comparison</div><div class="chart-subtitle">Current vs previous quarter</div><svg id="svgComparison"></svg></div>
</div>
</div>
<div class="copilot-panel">
<div class="copilot-header"><span class="status"></span> AI Copilot</div>
<div class="copilot-messages" id="chatMessages"></div>
<div class="suggestions" id="suggestionChips"></div>
<div class="copilot-input">
<input id="chatInput" type="text" placeholder="Ask about your data..." autofocus>
<button id="chatSend">Send</button>
</div>
</div>
</div>
<script>
(function(){
// ----------------------------------------------------------------
// DATA
// ----------------------------------------------------------------
const DATA = {
revenue: [],
customers: [],
segments: {}
};
function initData(){
const now = new Date(2026,5,28);
for(let i=60;i>=0;i--){
const d = new Date(now); d.setDate(d.getDate()-i);
const dateStr = d.toISOString().slice(0,10);
const base = 12000 + Math.sin(i*0.3)*3000 + Math.random()*2000;
const spike = (i===3||i===4)?8000:0;
const weekFactor = (d.getDay()===0||d.getDay()===6)?0.6:1;
DATA.revenue.push({date:dateStr,value:Math.round((base+spike)*weekFactor),label:d.toLocaleDateString('en',{weekday:'short',month:'short',day:'numeric'})});
}
DATA.customers = [
{name:'Acme Corp',mrr:12500,segment:'enterprise',growth:12},
{name:'Globex Inc',mrr:9800,segment:'enterprise',growth:8},
{name:'Initech',mrr:7200,segment:'smb',growth:22},
{name:'Hooli',mrr:6500,segment:'enterprise',growth:-3},
{name:'Umbrella Co',mrr:5400,segment:'startup',growth:35},
{name:'MassiveDyn',mrr:4800,segment:'enterprise',growth:5},
{name:'Cyberdyne',mrr:3900,segment:'smb',growth:18},
{name:'Wonka Ind',mrr:3100,segment:'startup',growth:45}
];
DATA.segments = {
enterprise:{revenue:45200,prev:42800,users:124,churn:2.1},
smb:{revenue:21800,prev:19500,users:340,churn:3.8},
startup:{revenue:14200,prev:11000,users:210,churn:5.2}
};
}
initData();
function getFilteredRevenue(from,to){
return DATA.revenue.filter(d => (!from||d.date>=from)&&(!to||d.date<=to));
}
// ----------------------------------------------------------------
// CHART FACTORY
// ----------------------------------------------------------------
function ChartFactory(svgId){
const svg = document.getElementById(svgId);
if(!svg) return null;
const W = svg.clientWidth||600;
const H = svg.clientHeight||250;
const PAD = {t:20,r:20,b:30,l:50};
const iw = W-PAD.l-PAD.r;
const ih = H-PAD.t-PAD.b;
function scaffold(){
svg.innerHTML = '';
const defs = document.createElementNS('http://www.w3.org/2000/svg','defs');
const clip = document.createElementNS('http://www.w3.org/2000/svg','clipPath');
clip.setAttribute('id','clip-'+svgId);
const rect = document.createElementNS('http://www.w3.org/2000/svg','rect');
rect.setAttribute('x','0');rect.setAttribute('y','0');
rect.setAttribute('width',iw);rect.setAttribute('height',ih);
clip.appendChild(rect);defs.appendChild(clip);svg.appendChild(defs);
const g = document.createElementNS('http://www.w3.org/2000/svg','g');
g.setAttribute('transform','translate('+PAD.l+','+PAD.t+')');
svg.appendChild(g);
return {g,iw,ih,W,H,PAD,svg,defs,clip};
}
function renderBar(data,xKey,yKey,opts){
opts=opts||{}; const s=scaffold(); const n=data.length;
const bw=Math.min(iw/n*0.7,30); const gap=(iw/n-bw)/2;
const max=Math.max(...data.map(d=>d[yKey]))*1.1;
const yScale=v=>ih-(v/max)*ih;
const xScale=i=>(iw/n)*i+gap;
const tooltipG = document.createElementNS('http://www.w3.org/2000/svg','g');
for(let i=0;i<n;i++){
const bar = document.createElementNS('http://www.w3.org/2000/svg','rect');
const x=xScale(i), w=bw, h=ih-yScale(data[i][yKey]), y=yScale(data[i][yKey]);
bar.setAttribute('x',x);bar.setAttribute('y',y);
bar.setAttribute('width',w);bar.setAttribute('height',h);
bar.setAttribute('fill',opts.color||'#3b82f6');
bar.setAttribute('rx','3');
bar.setAttribute('data-value',data[i][yKey]);
bar.setAttribute('data-label',data[i][xKey]);
s.g.appendChild(bar);
if(opts.showLabels){
const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
txt.setAttribute('x',x+w/2);txt.setAttribute('y',y-4);
txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','9');
txt.setAttribute('fill','#666');txt.textContent=opts.fmt?opts.fmt(data[i][yKey]):data[i][yKey];
s.g.appendChild(txt);
}
}
if(opts.yGrid){
for(let v=0;v<=max;v+=max/4){
const line=document.createElementNS('http://www.w3.org/2000/svg','line');
const yy=yScale(v);
line.setAttribute('x1',0);line.setAttribute('y1',yy);
line.setAttribute('x2',iw);line.setAttribute('y2',yy);
line.setAttribute('stroke','#e8ecf0');line.setAttribute('stroke-width','1');
s.g.appendChild(line);
const lbl=document.createElementNS('http://www.w3.org/2000/svg','text');
lbl.setAttribute('x',-8);lbl.setAttribute('y',yy+3);
lbl.setAttribute('text-anchor','end');lbl.setAttribute('font-size','9');
lbl.setAttribute('fill','#999');lbl.textContent=opts.fmt?opts.fmt(Math.round(v)):Math.round(v);
s.g.appendChild(lbl);
}
}
return s;
}
function renderLine(data,xKey,yKey,opts){
opts=opts||{}; const s=scaffold();
const max=Math.max(...data.map(d=>d[yKey]))*1.1;
const min=Math.min(...data.map(d=>d[yKey]))*0.9;
const range=max-min||1;
const yScale=v=>ih-((v-min)/range)*ih;
const xScale=i=>(iw/(data.length-1||1))*i;
const pts=data.map((d,i)=>({x:xScale(i),y:yScale(d[yKey]),val:d[yKey],lbl:d[xKey]}));
const path = document.createElementNS('http://www.w3.org/2000/svg','path');
let d='M'+pts[0].x+','+pts[0].y;
for(let i=1;i<pts.length;i++) d+=' L'+pts[i].x+','+pts[i].y;
path.setAttribute('d',d);path.setAttribute('fill','none');
path.setAttribute('stroke',opts.color||'#3b82f6');path.setAttribute('stroke-width','2');
path.setAttribute('stroke-linejoin','round');path.setAttribute('stroke-linecap','round');
s.g.appendChild(path);
if(opts.yGrid){
const steps=4;
for(let i=0;i<=steps;i++){
const v=min+(range/steps)*i;
const yy=yScale(v);
const line=document.createElementNS('http://www.w3.org/2000/svg','line');
line.setAttribute('x1',0);line.setAttribute('y1',yy);
line.setAttribute('x2',iw);line.setAttribute('y2',yy);
line.setAttribute('stroke','#e8ecf0');line.setAttribute('stroke-width','1');
s.g.appendChild(line);
const lbl=document.createElementNS('http://www.w3.org/2000/svg','text');
lbl.setAttribute('x',-8);lbl.setAttribute('y',yy+3);
lbl.setAttribute('text-anchor','end');lbl.setAttribute('font-size','9');
lbl.setAttribute('fill','#999');lbl.textContent=opts.fmt?opts.fmt(Math.round(v)):Math.round(v);
s.g.appendChild(lbl);
}
}
if(opts.area){
const area=document.createElementNS('http://www.w3.org/2000/svg','path');
let ad='M'+pts[0].x+','+pts[0].y;
for(let i=1;i<pts.length;i++) ad+=' L'+pts[i].x+','+pts[i].y;
ad+=' L'+pts[pts.length-1].x+','+ih+' L'+pts[0].x+','+ih+' Z';
area.setAttribute('d',ad);area.setAttribute('fill',opts.color||'#3b82f6');
area.setAttribute('opacity','0.1');s.g.insertBefore(area,s.g.firstChild);
}
if(opts.annotate && pts.length>0){
const last=pts[pts.length-1];
const circle=document.createElementNS('http://www.w3.org/2000/svg','circle');
circle.setAttribute('cx',last.x);circle.setAttribute('cy',last.y);
circle.setAttribute('r','4');circle.setAttribute('fill','#fff');
circle.setAttribute('stroke',opts.color||'#3b82f6');circle.setAttribute('stroke-width','2');
s.g.appendChild(circle);
}
if(opts.xLabels){
const step=Math.max(1,Math.floor(pts.length/8));
for(let i=0;i<pts.length;i+=step){
const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
txt.setAttribute('x',pts[i].x);txt.setAttribute('y',ih+14);
txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','8');
txt.setAttribute('fill','#999');txt.textContent=data[i][xKey].length>4?data[i][xKey].slice(0,3):data[i][xKey];
s.g.appendChild(txt);
}
}
return s;
}
function renderPie(data,key,labelKey,opts){
opts=opts||{}; const s=scaffold();
const cx=iw/2,cy=ih/2,r=Math.min(iw,ih)/2*0.75;
const total=data.reduce((a,d)=>a+d[key],0);
const colors=['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6','#ec4899','#14b8a6','#f97316'];
let angle=-Math.PI/2;
data.forEach((d,i)=>{
const v=d[key]/total*Math.PI*2;
const x1=cx+Math.cos(angle)*r;
const y1=cy+Math.sin(angle)*r;
const x2=cx+Math.cos(angle+v)*r;
const y2=cy+Math.sin(angle+v)*r;
const large=v>Math.PI?1:0;
const path=document.createElementNS('http://www.w3.org/2000/svg','path');
const dAttr='M'+cx+','+cy+' L'+x1+','+y1+' A'+r+','+r+' 0 '+large+' 1 '+x2+','+y2+' Z';
path.setAttribute('d',dAttr);path.setAttribute('fill',colors[i%colors.length]);
path.setAttribute('stroke','#fff');path.setAttribute('stroke-width','2');
s.g.appendChild(path);
const midAngle=angle+v/2;
const lx=cx+Math.cos(midAngle)*r*0.65;
const ly=cy+Math.sin(midAngle)*r*0.65;
const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
txt.setAttribute('x',lx);txt.setAttribute('y',ly+3);
txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','10');
txt.setAttribute('fill','#fff');txt.setAttribute('font-weight','bold');
txt.textContent=opts.fmt?opts.fmt(d[key]):Math.round(v/total*100)+'%';
s.g.appendChild(txt);
angle+=v;
});
const legendY=12;
data.forEach((d,i)=>{
const lx=10,ly=legendY+i*18;
const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
rect.setAttribute('x',lx);rect.setAttribute('y',ly-8);
rect.setAttribute('width','10');rect.setAttribute('height','10');
rect.setAttribute('fill',colors[i%colors.length]);rect.setAttribute('rx','2');
s.g.appendChild(rect);
const txt=document.createElementNS('http://www.w3.org/2000/svg','text');
txt.setAttribute('x',lx+16);txt.setAttribute('y',ly+1);
txt.setAttribute('font-size','9');txt.setAttribute('fill','#555');
txt.textContent=d[labelKey];
s.g.appendChild(txt);
});
return s;
}
function renderComparison(bars1,bars2,xKey,yKey,opts){
opts=opts||{}; const s=scaffold();
const allVals=[...bars1.map(d=>d[yKey]),...bars2.map(d=>d[yKey])];
const max=Math.max(...allVals)*1.1;
const n=Math.max(bars1.length,bars2.length);
const bw=Math.min(iw/n*0.6,24)/2; const gap=(iw/n-bw*2)/2;
const yScale=v=>ih-(v/max)*ih;
const xScale=i=>(iw/n)*i+gap;
for(let i=0;i<n;i++){
if(bars1[i]){
const x=xScale(i),h=ih-yScale(bars1[i][yKey]),y=yScale(bars1[i][yKey]);
const bar=document.createElementNS('http://www.w3.org/2000/svg','rect');
bar.setAttribute('x',x);bar.setAttribute('y',y);
bar.setAttribute('width',bw);bar.setAttribute('height',h);
bar.setAttribute('fill',opts.color1||'#3b82f6');bar.setAttribute('rx','2');
s.g.appendChild(bar);
}
if(bars2[i]){
const x=xScale(i)+bw,h=ih-yScale(bars2[i][yKey]),y=yScale(bars2[i][yKey]);
const bar=document.createElementNS('http://www.w3.org/2000/svg','rect');
bar.setAttribute('x',x);bar.setAttribute('y',y);
bar.setAttribute('width',bw);bar.setAttribute('height',h);
bar.setAttribute('fill',opts.color2||'#10b981');bar.setAttribute('rx','2');
s.g.appendChild(bar);
}
}
if(opts.yGrid){
for(let v=0;v<=max;v+=max/4){
const yy=yScale(v);
const line=document.createElementNS('http://www.w3.org/2000/svg','line');
line.setAttribute('x1',0);line.setAttribute('y1',yy);
line.setAttribute('x2',iw);line.setAttribute('y2',yy);
line.setAttribute('stroke','#e8ecf0');line.setAttribute('stroke-width','1');
s.g.appendChild(line);
const lbl=document.createElementNS('http://www.w3.org/2000/svg','text');
lbl.setAttribute('x',-8);lbl.setAttribute('y',yy+3);
lbl.setAttribute('text-anchor','end');lbl.setAttribute('font-size','9');
lbl.setAttribute('fill','#999');lbl.textContent=opts.fmt?opts.fmt(Math.round(v)):Math.round(v);
s.g.appendChild(lbl);
}
}
const lx=iw-100,ly=ih-20;
const r1=document.createElementNS('http://www.w3.org/2000/svg','rect');
r1.setAttribute('x',lx);r1.setAttribute('y',ly-8);r1.setAttribute('width','10');r1.setAttribute('height','10');
r1.setAttribute('fill',opts.color1||'#3b82f6');r1.setAttribute('rx','2');s.g.appendChild(r1);
const t1=document.createElementNS('http://www.w3.org/2000/svg','text');
t1.setAttribute('x',lx+14);t1.setAttribute('y',ly+1);t1.setAttribute('font-size','9');t1.setAttribute('fill','#555');
t1.textContent=opts.label1||'Current';s.g.appendChild(t1);
const r2=document.createElementNS('http://www.w3.org/2000/svg','rect');
r2.setAttribute('x',lx);r2.setAttribute('y',ly+10);r2.setAttribute('width','10');r2.setAttribute('height','10');
r2.setAttribute('fill',opts.color2||'#10b981');r2.setAttribute('rx','2');s.g.appendChild(r2);
const t2=document.createElementNS('http://www.w3.org/2000/svg','text');
t2.setAttribute('x',lx+14);t2.setAttribute('y',ly+19);t2.setAttribute('font-size','9');t2.setAttribute('fill','#555');
t2.textContent=opts.label2||'Previous';s.g.appendChild(t2);
return s;
}
return {renderBar,renderLine,renderPie,renderComparison,W,H};
}
// ----------------------------------------------------------------
// NL QUERY PARSER
// ----------------------------------------------------------------
function parseQuery(text,state){
const q=text.toLowerCase().trim();
const ctx = {
type:'unknown',
chartType:'none',
dataKey:'revenue',
segment:'all',
timeRange:'current',
metric:state.metric||'revenue',
filter:{}
};
if(/churn|attrition|lost/i.test(q)){ctx.type='metric';ctx.dataKey='churn';ctx.metric='churn'}
else if(/top.*customer|biggest|customer.*mrr|who.*pay/i.test(q)){ctx.type='chart';ctx.chartType='bar';ctx.dataKey='customers'}
else if(/compare|vs|versus|vs\.|quarter|previous/i.test(q)){ctx.type='chart';ctx.chartType='comparison';ctx.dataKey='revenue'}
else if(/segment|breakdown|by.*type|by.*segment|distribution/i.test(q)){ctx.type='chart';ctx.chartType='pie';ctx.dataKey='segments'}
else if(/spike|anomaly|unusual|why.*up|why.*down|caused/i.test(q)){ctx.type='anomaly';ctx.dataKey='revenue'}
else if(/trend|over time|this month|this week|movement/i.test(q)){ctx.type='chart';ctx.chartType='line';ctx.dataKey='revenue'}
else if(/growth|growing|fastest|top.*product/i.test(q)){ctx.type='chart';ctx.chartType='bar';ctx.dataKey='customers';ctx.filter={sort:'growth'}}
else{ctx.type='chart';ctx.chartType='line';ctx.dataKey='revenue'}
if(/enterprise/i.test(q)) ctx.filter.segment='enterprise';
if(/smb/i.test(q)) ctx.filter.segment='smb';
if(/startup/i.test(q)) ctx.filter.segment='startup';
return ctx;
}
// ----------------------------------------------------------------
// CHAT ENGINE
// ----------------------------------------------------------------
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');
const suggestionChips = document.getElementById('suggestionChips');
const SUGGESTIONS = [
'What caused the revenue spike last Tuesday?',
'Show me our top 5 customers by MRR',
'Compare this quarter to last',
'What is our churn rate?',
'Show revenue breakdown by segment',
'Which customers are growing fastest?'
];
let chatHistory = [];
function addMessage(role,content,extra){
chatHistory.push({role,content,extra});
const div=document.createElement('div');
div.className='message '+role;
if(typeof content==='string') div.textContent=content;
else div.appendChild(content);
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
}
function addLoading(){
const div=document.createElement('div');
div.className='message copilot';
div.innerHTML='<div class="loading-dots"><span></span><span></span><span></span></div>';
div.id='loadingIndicator';
chatMessages.appendChild(div);
chatMessages.scrollTop=chatMessages.scrollHeight;
return div;
}
function removeLoading(){
const el=document.getElementById('loadingIndicator');
if(el) el.remove();
}
function fmtNum(n){
if(n>=1000000) return '$'+(n/1000000).toFixed(1)+'M';
if(n>=1000) return '$'+(n/1000).toFixed(1)+'K';
return '$'+Math.round(n);
}
function buildChartResponse(query,ctx){
const from=document.getElementById('dateFrom').value;
const to=document.getElementById('dateTo').value;
const segment=document.getElementById('segmentSelect').value;
let responseText='';
let chartData=null;
let chartType='';
let annotations='';
if(ctx.chartType==='bar'&&ctx.dataKey==='customers'){
const custs=ctx.filter.segment?DATA.customers.filter(c=>c.segment===ctx.filter.segment):DATA.customers;
const sorted=[...custs].sort((a,b)=>ctx.filter.sort==='growth'?b.growth-a.growth:b.mrr-a.mrr).slice(0,5);
responseText='Here are the top customers by MRR.';
chartType='bar';chartData={type:'bar',data:sorted,xKey:'name',yKey:'mrr',opts:{color:'#10b981',showLabels:true,fmt:fmtNum,yGrid:true}};
annotations='Total MRR from top 5: '+fmtNum(sorted.reduce((a,c)=>a+c.mrr,0));
}
else if(ctx.chartType==='comparison'){
const revs=getFilteredRevenue(from,to);
const mid=Math.floor(revs.length/2);
const current=revs.slice(mid);
const prev=revs.slice(0,mid);
const curAvg=current.reduce((a,d)=>a+d.value,0)/current.length;
const prvAvg=prev.reduce((a,d)=>a+d.value,0)/prev.length;
const pct=((curAvg-prvAvg)/prvAvg*100).toFixed(1);
responseText='Comparing two halves of the selected period. '+(pct>0?'Up '+pct+'%':'Down '+Math.abs(pct)+'%')+' vs previous period.';
chartType='comparison';chartData={type:'comparison',bars1:current.slice(0,14),bars2:prev.slice(0,14),xKey:'label',yKey:'value',opts:{color1:'#3b82f6',color2:'#10b981',label1:'Recent',label2:'Earlier',fmt:fmtNum}};
annotations='Current avg: '+fmtNum(Math.round(curAvg))+' | Previous avg: '+fmtNum(Math.round(prvAvg));
}
else if(ctx.chartType==='pie'){
const segs=DATA.segments;
const data=Object.entries(segs).filter(([k])=>segment==='all'||k===segment).map(([k,v])=>({name:k.charAt(0).toUpperCase()+k.slice(1),value:v.revenue}));
responseText='Revenue distribution by customer segment.';
chartType='pie';chartData={type:'pie',data,key:'value',labelKey:'name',opts:{fmt:fmtNum}};
const total=Object.values(segs).reduce((a,s)=>a+s.revenue,0);
annotations='Total: '+fmtNum(total);
}
else if(ctx.metric==='churn'){
const segs=DATA.segments;
const data=Object.entries(segs).filter(([k])=>segment==='all'||k===segment).map(([k,v])=>({name:k.charAt(0).toUpperCase()+k.slice(1),value:v.churn}));
responseText='Churn rate by segment. Enterprise churn is lowest at '+segs.enterprise.churn+'%, while startup churn is highest at '+segs.startup.churn+'%.';
chartType='bar';chartData={type:'bar',data,xKey:'name',yKey:'value',opts:{color:'#ef4444',showLabels:true,yGrid:true,fmt:v=>v+'%'}};
annotations='Average churn: '+((segs.enterprise.churn+segs.smb.churn+segs.startup.churn)/3).toFixed(1)+'%';
}
else {
const revs=getFilteredRevenue(from,to);
responseText='Showing revenue trend for the selected period.';
chartType='line';chartData={type:'line',data:revs,xKey:'label',yKey:'value',opts:{color:'#3b82f6',area:true,annotate:true,yGrid:true,xLabels:true,fmt:fmtNum}};
const total=revs.reduce((a,d)=>a+d.value,0);
const avg=total/revs.length;
annotations='Total: '+fmtNum(total)+' | Daily avg: '+fmtNum(Math.round(avg));
}
if(/spike|anomaly|unusual|why/i.test(query)){
const revs=getFilteredRevenue(from,to);
let peak=0,peakIdx=-1;
revs.forEach((d,i)=>{if(d.value>peak){peak=d.value;peakIdx=i}});
if(peakIdx>=0&&peak>15000){
const prevDay=revs[peakIdx-1]||{value:0};
const spikePct=((peak-prevDay.value)/prevDay.value*100).toFixed(0);
responseText='I found a revenue spike on '+revs[peakIdx].label+'. Revenue jumped '+spikePct+'% to '+fmtNum(peak)+'. This is likely driven by an enterprise deal close — check the Enterprise segment filter.';
annotations='Spike detected: '+revs[peakIdx].label+' — '+fmtNum(peak)+' ('+spikePct+'% increase)';
}
}
return {responseText,chartData,chartType,annotations};
}
function generateInlineChart(chartData){
if(!chartData) return null;
const div=document.createElement('div');
div.className='chart-inline';
const svgNS='http://www.w3.org/2000/svg';
const svg=document.createElementNS(svgNS,'svg');
svg.setAttribute('width','100%');svg.setAttribute('height','160');
svg.setAttribute('viewBox','0 0 400 160');
const tempId='svg_inline_'+(Math.random()*1e9|0);
const container=document.createElement('div');
container.appendChild(svg);
div.appendChild(container);
setTimeout(()=>{
svg.setAttribute('width','100%');svg.setAttribute('height','160');
svg.setAttribute('viewBox','0 0 400 160');
const tempEl=document.createElement('div');
tempEl.style.display='none';tempEl.id=tempId;
document.body.appendChild(tempEl);
const factory=ChartFactory(tempId);
if(!factory) return;
const W=400,H=160,PAD={t:10,r:10,b:20,l:40},iw=W-PAD.l-PAD.r,ih=H-PAD.t-PAD.b;
const g=document.createElementNS(svgNS,'g');
g.setAttribute('transform','translate('+PAD.l+','+PAD.t+')');
svg.innerHTML='';svg.appendChild(g);
if(chartData.type==='bar'){
const data=chartData.data;const n=data.length;
const bw=Math.min(iw/n*0.7,24);const gap=(iw/n-bw)/2;
const max=Math.max(...data.map(d=>d[chartData.yKey]))*1.1;
const yScale=v=>ih-(v/max)*ih;
const xScale=i=>(iw/n)*i+gap;
for(let i=0;i<n;i++){
const bar=document.createElementNS(svgNS,'rect');
const x=xScale(i),h=ih-yScale(data[i][chartData.yKey]),y=yScale(data[i][chartData.yKey]);
bar.setAttribute('x',x);bar.setAttribute('y',y);bar.setAttribute('width',bw);bar.setAttribute('height',h);
bar.setAttribute('fill',(chartData.opts&&chartData.opts.color)||'#3b82f6');bar.setAttribute('rx','3');
g.appendChild(bar);
}
const maxVal=max;
for(let v=0;v<=maxVal;v+=maxVal/3){
const yy=yScale(v);
const line=document.createElementNS(svgNS,'line');
line.setAttribute('x1',0);line.setAttribute('y1',yy);line.setAttribute('x2',iw);line.setAttribute('y2',yy);
line.setAttribute('stroke','#e8ecf0');line.setAttribute('stroke-width','1');g.appendChild(line);
const lbl=document.createElementNS(svgNS,'text');
lbl.setAttribute('x',-6);lbl.setAttribute('y',yy+3);lbl.setAttribute('text-anchor','end');
lbl.setAttribute('font-size','8');lbl.setAttribute('fill','#999');
lbl.textContent=chartData.opts&&chartData.opts.fmt?chartData.opts.fmt(Math.round(v)):Math.round(v);
g.appendChild(lbl);
}
}
else if(chartData.type==='line'){
const data=chartData.data;const max=Math.max(...data.map(d=>d[chartData.yKey]))*1.1;
const min=Math.min(...data.map(d=>d[chartData.yKey]))*0.9;
const range=max-min||1;
const yScale=v=>ih-((v-min)/range)*ih;
const xScale=i=>(iw/(data.length-1||1))*i;
const pts=data.map((d,i)=>({x:xScale(i),y:yScale(d[chartData.yKey])}));
const path=document.createElementNS(svgNS,'path');
let d='M'+pts[0].x+','+pts[0].y;for(let i=1;i<pts.length;i++) d+=' L'+pts[i].x+','+pts[i].y;
path.setAttribute('d',d);path.setAttribute('fill','none');
path.setAttribute('stroke',(chartData.opts&&chartData.opts.color)||'#3b82f6');path.setAttribute('stroke-width','2');
g.appendChild(path);
if(chartData.opts&&chartData.opts.area){
const area=document.createElementNS(svgNS,'path');
let ad='M'+pts[0].x+','+pts[0].y;for(let i=1;i<pts.length;i++) ad+=' L'+pts[i].x+','+pts[i].y;
ad+=' L'+pts[pts.length-1].x+','+ih+' L'+pts[0].x+','+ih+' Z';
area.setAttribute('d',ad);area.setAttribute('fill',(chartData.opts&&chartData.opts.color)||'#3b82f6');
area.setAttribute('opacity','0.1');g.insertBefore(area,g.firstChild);
}
const maxVal=max;
for(let v=0;v<=maxVal;v+=maxVal/3){
const yy=yScale(v);
const line=document.createElementNS(svgNS,'line');
line.setAttribute('x1',0);line.setAttribute('y1',yy);line.setAttribute('x2',iw);line.setAttribute('y2',yy);
line.setAttribute('stroke','#e8ecf0');line.setAttribute('stroke-width','1');g.appendChild(line);
const lbl=document.createElementNS(svgNS,'text');
lbl.setAttribute('x',-6);lbl.setAttribute('y',yy+3);lbl.setAttribute('text-anchor','end');
lbl.setAttribute('font-size','8');lbl.setAttribute('fill','#999');
lbl.textContent=chartData.opts&&chartData.opts.fmt?chartData.opts.fmt(Math.round(v)):Math.round(v);
g.appendChild(lbl);
}
}
else if(chartData.type==='pie'){
const data=chartData.data;const key=chartData.key;
const cx=iw/2,cy=ih/2,r=Math.min(iw,ih)/2*0.6;
const total=data.reduce((a,d)=>a+d[key],0);
const colors=['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6','#ec4899'];
let angle=-Math.PI/2;
data.forEach((d,i)=>{
const v=d[key]/total*Math.PI*2;
const x1=cx+Math.cos(angle)*r;const y1=cy+Math.sin(angle)*r;
const x2=cx+Math.cos(angle+v)*r;const y2=cy+Math.sin(angle+v)*r;
const large=v>Math.PI?1:0;
const path=document.createElementNS(svgNS,'path');
path.setAttribute('d','M'+cx+','+cy+' L'+x1+','+y1+' A'+r+','+r+' 0 '+large+' 1 '+x2+','+y2+' Z');
path.setAttribute('fill',colors[i%colors.length]);path.setAttribute('stroke','#fff');path.setAttribute('stroke-width','1.5');
g.appendChild(path);
angle+=v;
});
const ly=10;
data.forEach((d,i)=>{
const rx=iw-80,ry=ly+i*16;
const r=document.createElementNS(svgNS,'rect');
r.setAttribute('x',rx);r.setAttribute('y',ry-6);r.setAttribute('width','8');r.setAttribute('height','8');
r.setAttribute('fill',colors[i%colors.length]);r.setAttribute('rx','2');g.appendChild(r);
const t=document.createElementNS(svgNS,'text');
t.setAttribute('x',rx+12);t.setAttribute('y',ry+1);t.setAttribute('font-size','8');t.setAttribute('fill','#555');
t.textContent=d[chartData.labelKey];g.appendChild(t);
});
}
else if(chartData.type==='comparison'){
const b1=chartData.bars1,b2=chartData.bars2;
const allVals=[...b1.map(d=>d[chartData.yKey]),...b2.map(d=>d[chartData.yKey])];
const max=Math.max(...allVals)*1.1;
const n=b1.length;
const bw=Math.min(iw/n*0.55,20)/2;const gap=(iw/n-bw*2)/2;
const yScale=v=>ih-(v/max)*ih;
const xScale=i=>(iw/n)*i+gap;
for(let i=0;i<n;i++){
if(b1[i]){
const x=xScale(i),h=ih-yScale(b1[i][chartData.yKey]),y=yScale(b1[i][chartData.yKey]);
const bar=document.createElementNS(svgNS,'rect');
bar.setAttribute('x',x);bar.setAttribute('y',y);bar.setAttribute('width',bw);bar.setAttribute('height',h);
bar.setAttribute('fill',(chartData.opts&&chartData.opts.color1)||'#3b82f6');bar.setAttribute('rx','2');
g.appendChild(bar);
}
if(b2[i]){
const x=xScale(i)+bw,h=ih-yScale(b2[i][chartData.yKey]),y=yScale(b2[i][chartData.yKey]);
const bar=document.createElementNS(svgNS,'rect');
bar.setAttribute('x',x);bar.setAttribute('y',y);bar.setAttribute('width',bw);bar.setAttribute('height',h);
bar.setAttribute('fill',(chartData.opts&&chartData.opts.color2)||'#10b981');bar.setAttribute('rx','2');
g.appendChild(bar);
}
}
}
document.body.removeChild(tempEl);
},50);
return div;
}
function processQuery(query){
const state={
metric:document.getElementById('metricSelect').value,
segment:document.getElementById('segmentSelect').value,
dateFrom:document.getElementById('dateFrom').value,
dateTo:document.getElementById('dateTo').value
};
addMessage('user',query);
const loader=addLoading();
const ctx=parseQuery(query,state);
setTimeout(()=>{
removeLoading();
const result=buildChartResponse(query,ctx);
let contentDiv=document.createElement('div');
let responseP=document.createElement('div');
responseP.textContent=result.responseText;
contentDiv.appendChild(responseP);
if(result.annotations){
const ann=document.createElement('div');
ann.style.cssText='margin-top:6px;padding:6px 8px;background:#f0f4ff;border-radius:4px;border-left:2px solid #3b82f6;font-size:11px;color:#555';
ann.textContent=result.annotations;
contentDiv.appendChild(ann);
}
if(result.chartData){
const inline=generateInlineChart(result.chartData);
if(inline) contentDiv.appendChild(inline);
}
addMessage('copilot',contentDiv);
updateMainCharts(ctx,state);
},400);
}
function updateMainCharts(ctx,state){
const from=document.getElementById('dateFrom').value;
const to=document.getElementById('dateTo').value;
const revs=getFilteredRevenue(from,to);
if(revs.length===0) return;
const f=ChartFactory('svgRevenue');
if(f){
f.renderLine(revs,'label','value',{color:'#3b82f6',area:true,annotate:true,yGrid:true,xLabels:true,fmt:fmtNum});
}
const f2=ChartFactory('svgCustomers');
if(f2){
const top5=[...DATA.customers].sort((a,b)=>b.mrr-a.mrr).slice(0,5);
f2.renderBar(top5,'name','mrr',{color:'#10b981',showLabels:true,fmt:fmtNum,yGrid:true});
}
const f3=ChartFactory('svgBreakdown');
if(f3){
const segs=DATA.segments;
const data=Object.entries(segs).map(([k,v])=>({name:k.charAt(0).toUpperCase()+k.slice(1),value:v.revenue}));
f3.renderPie(data,'value','name',{fmt:fmtNum});
}
const f4=ChartFactory('svgComparison');
if(f4){
const mid=Math.floor(revs.length/2);
const current=revs.slice(mid).slice(0,14);
const prev=revs.slice(Math.max(0,mid-14),mid);
f4.renderComparison(current,prev,'label','value',{color1:'#3b82f6',color2:'#10b981',label1:'Recent',label2:'Earlier',fmt:fmtNum});
}
}
function updateMetrics(){
const revs=getFilteredRevenue(
document.getElementById('dateFrom').value,
document.getElementById('dateTo').value
);
const bar=document.getElementById('metricsBar');
if(revs.length===0){bar.innerHTML='';return}
const total=revs.reduce((a,d)=>a+d.value,0);
const avg=Math.round(total/revs.length);
const first=revs[0].value,last=revs[revs.length-1].value;
const trend=((last-first)/first*100).toFixed(1);
const mrrTotal=DATA.customers.reduce((a,c)=>a+c.mrr,0);
const churnAvg=Object.values(DATA.segments).reduce((a,s)=>a+s.churn,0)/3;
bar.innerHTML=
'<div class="metric-card"><div class="label">Total Revenue</div><div class="value">'+fmtNum(total)+'</div><div class="change '+(trend>0?'up':'down')+'">'+trend+'% vs period start</div></div>'+
'<div class="metric-card"><div class="label">Daily Average</div><div class="value">'+fmtNum(avg)+'</div><div class="change">Over '+(revs.length-1)+' days</div></div>'+
'<div class="metric-card"><div class="label">MRR</div><div class="value">'+fmtNum(mrrTotal)+'</div><div class="change up">From '+DATA.customers.length+' customers</div></div>'+
'<div class="metric-card"><div class="label">Churn Rate</div><div class="value">'+churnAvg.toFixed(1)+'%</div><div class="change '+(churnAvg>3?'down':'up')+'">'+(churnAvg>3?'Needs attention':'Healthy')+'</div></div>';
}
// ----------------------------------------------------------------
// INIT
// ----------------------------------------------------------------
SUGGESTIONS.forEach(s=>{
const chip=document.createElement('span');
chip.className='chip';chip.textContent=s;
chip.addEventListener('click',()=>processQuery(s));
suggestionChips.appendChild(chip);
});
chatSend.addEventListener('click',()=>{
const q=chatInput.value.trim();if(!q) return;
chatInput.value='';processQuery(q);
});
chatInput.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();chatSend.click()}});
document.getElementById('dateFrom').addEventListener('change',()=>{updateMetrics();updateMainCharts()});
document.getElementById('dateTo').addEventListener('change',()=>{updateMetrics();updateMainCharts()});
document.getElementById('metricSelect').addEventListener('change',()=>{updateMetrics();updateMainCharts()});
document.getElementById('segmentSelect').addEventListener('change',()=>{updateMetrics();updateMainCharts()});
updateMetrics();
setTimeout(()=>updateMainCharts(),100);
addMessage('copilot','Hi, I am your AI copilot. Ask me anything about your dashboard data — revenue trends, customer insights, comparisons, or anomalies. Try one of the suggested queries below.');
})();
</script>
</body>
</html>
```