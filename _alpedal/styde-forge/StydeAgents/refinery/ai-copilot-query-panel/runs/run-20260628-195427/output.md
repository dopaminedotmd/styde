<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Query Panel</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
body{display:flex;height:100vh;background:#f5f7fa;color:#1a1a2e}
.dashboard{flex:1;display:flex;flex-direction:column;padding:20px;overflow:hidden}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.08);margin-bottom:16px}
.header h1{font-size:20px;font-weight:600}
.filters{display:flex;gap:12px;align-items:center}
.filters select,.filters input{padding:6px 12px;border:1px solid #dde1e6;border-radius:6px;font-size:13px;background:#fff}
.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;overflow:hidden}
.card{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:16px;display:flex;flex-direction:column;overflow:hidden}
.card h3{font-size:13px;color:#6b7280;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px;font-weight:500}
.card .chart-area{flex:1;display:flex;align-items:flex-end;justify-content:center;position:relative;min-height:120px}
.card .chart-area svg{width:100%;height:100%;max-height:180px}
.callout{font-size:11px;color:#6b7280;background:#f0f4f8;padding:6px 10px;border-radius:6px;margin-top:8px;border-left:3px solid #6366f1}
.copilot{width:380px;min-width:380px;background:#fff;border-left:1px solid #e5e7eb;display:flex;flex-direction:column;box-shadow:-2px 0 8px rgba(0,0,0,0.04)}
.copilot-header{padding:16px 20px;border-bottom:1px solid #e5e7eb;background:#fafbfc}
.copilot-header h2{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px}
.copilot-header h2 span{background:#6366f1;color:#fff;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:500}
.messages{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:92%;padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.5;animation:fadeIn .2s ease}
.msg.user{background:#6366f1;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.msg.bot{background:#f0f4f8;color:#1a1a2e;align-self:flex-start;border-bottom-left-radius:4px}
.msg.bot .chart-inline{width:100%;height:100px;margin:8px 0 4px;background:#fff;border-radius:8px;padding:4px}
.msg.bot .chart-inline svg{width:100%;height:100%}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.suggestions{display:flex;gap:6px;flex-wrap:wrap;padding:8px 20px;border-top:1px solid #e5e7eb}
.suggestions button{font-size:12px;padding:5px 10px;border:1px solid #dde1e6;border-radius:16px;background:#fff;cursor:pointer;color:#4b5563;white-space:nowrap;transition:all .15s}
.suggestions button:hover{background:#6366f1;color:#fff;border-color:#6366f1}
.input-bar{display:flex;padding:12px 20px 16px;border-top:1px solid #e5e7eb;gap:8px;background:#fafbfc}
.input-bar input{flex:1;padding:10px 14px;border:1px solid #dde1e6;border-radius:24px;font-size:13px;outline:none;transition:border .15s}
.input-bar input:focus{border-color:#6366f1}
.input-bar button{width:38px;height:38px;border-radius:50%;border:none;background:#6366f1;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:background .15s}
.input-bar button:hover{background:#4f46e5}
.voice-btn{width:38px;height:38px;border-radius:50%;border:1px solid #dde1e6;background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all .15s}
.voice-btn:hover{background:#f0f4f8}
.typing{display:flex;gap:3px;padding:4px 0}
.typing span{width:6px;height:6px;background:#9ca3af;border-radius:50%;animation:bounce 1.4s infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:scale(0.6)}40%{transform:scale(1)}}
</style>
</head>
<body>
<div class="dashboard">
<div class="header">
<h1>Styde Analytics</h1>
<div class="filters">
<span style="font-size:13px;color:#6b7280">Filters:</span>
<select id="dateFilter"><option>Last 7 days</option><option>Last 30 days</option><option>This quarter</option><option>Last quarter</option><option>Year to date</option></select>
<select id="metricFilter"><option>All metrics</option><option>Revenue</option><option>MRR</option><option>Users</option><option>Churn</option></select>
</div>
</div>
<div class="grid">
<div class="card" id="card-revenue">
<h3>Revenue Trend</h3>
<div class="chart-area" id="chart-revenue"></div>
<div class="callout" id="callout-revenue">Revenue up 23% vs last period. Tuesday spike correlated with product launch campaign.</div>
</div>
<div class="card" id="card-top-customers">
<h3>Top Customers by MRR</h3>
<div class="chart-area" id="chart-customers"></div>
<div class="callout" id="callout-customers">Acme Corp leads at $12.4k MRR. Top 5 represent 47% of total MRR.</div>
</div>
<div class="card" id="card-comparison">
<h3>Quarter Comparison</h3>
<div class="chart-area" id="chart-comparison"></div>
<div class="callout" id="callout-comparison">Q2 vs Q1: Revenue +18.2%, MRR +12.7%, New customers +31%.</div>
</div>
<div class="card" id="card-cohorts">
<h3>Cohort Retention</h3>
<div class="chart-area" id="chart-cohorts"></div>
<div class="callout" id="callout-cohorts">Week-4 retention trending upward. Jan cohort maintaining 82% at week 8.</div>
</div>
</div>
</div>
<div class="copilot" id="copilot">
<div class="copilot-header">
<h2><span>AI</span> Copilot <span style="font-size:11px;font-weight:400;color:#6b7280;margin-left:auto">dashboard-aware</span></h2>
</div>
<div class="messages" id="messages"></div>
<div class="suggestions" id="suggestions">
<button data-query="What caused the revenue spike last Tuesday?">Revenue spike Tuesday</button>
<button data-query="Show top 5 customers by MRR">Top 5 customers</button>
<button data-query="Compare this quarter to last">Compare quarters</button>
<button data-query="Which cohort has best retention?">Best retention</button>
</div>
<div class="input-bar">
<button class="voice-btn" id="voiceBtn" title="Voice input">🎤</button>
<input type="text" id="queryInput" placeholder="Ask a question about your data..." autofocus>
<button id="sendBtn">➤</button>
</div>
</div>
<script>
(function(){
const DASHBOARD_STATE = {
filters: { date: 'Last 7 days', metric: 'All metrics' },
metrics: { revenue: 124500, mrr: 48700, users: 3420, churn: 3.2 }
};
const MOCK_DATA = {
revenue: { labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], values: [12400, 21800, 16200, 15800, 17500, 19100, 18700] },
customers: { labels: ['Acme Corp','Globex','Initech','Umbrella','Wayne Ent'], values: [12400, 8900, 7600, 5400, 4200] },
comparison: { labels: ['Q1 2026','Q2 2026'], values: [{label:'Revenue',vals:[105200,124500]},{label:'MRR',vals:[43200,48700]},{label:'Customers',vals:[2610,3420]}] },
cohorts: { labels: ['W1','W2','W4','W8','W12'], values: [100,94,82,71,63], series: [{label:'Jan cohort',vals:[100,96,88,82,76]},{label:'Feb cohort',vals:[100,93,82,71,63]},{label:'Mar cohort',vals:[100,91,78,65,null]}] }
};
function drawBarChart(svgEl, data, color='#6366f1', maxVal, label){
if(!svgEl)return;const svg=svgEl;const w=svg.clientWidth||240;const h=svg.clientHeight||120;const pad={t:8,r:8,b:20,l:32};const cw=w-pad.l-pad.r;const ch=h-pad.t-pad.b;if(!data||!data.values||data.values.length===0)return;const mx=maxVal||Math.max(...data.values.filter(v=>v!==null));const bw=Math.min(cw/data.values.length*0.7,28);const gap=(cw-bw*data.values.length)/(data.values.length+1);svg.innerHTML='<g transform="translate('+pad.l+','+pad.t+')">';const g=svg.querySelector('g');for(let i=0;i<data.values.length;i++){const v=data.values[i];if(v===null)continue;const barH=(v/mx)*ch;const x=gap+i*(bw+gap);const y=ch-barH;const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');rect.setAttribute('x',x);rect.setAttribute('y',y);rect.setAttribute('width',bw);rect.setAttribute('height',barH);rect.setAttribute('fill',color);rect.setAttribute('rx','3');rect.addEventListener('mouseenter',function(){this.setAttribute('opacity','0.8')});rect.addEventListener('mouseleave',function(){this.setAttribute('opacity','1')});g.appendChild(rect);const txt=document.createElementNS('http://www.w3.org/2000/svg','text');txt.setAttribute('x',x+bw/2);txt.setAttribute('y',ch+14);txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','9');txt.setAttribute('fill','#9ca3af');txt.textContent=data.labels[i]||'';g.appendChild(txt);if(label){const lbl=document.createElementNS('http://www.w3.org/2000/svg','text');lbl.setAttribute('x',-30);lbl.setAttribute('y',-4);lbl.setAttribute('font-size','9');lbl.setAttribute('fill','#6b7280');lbl.textContent=label;g.appendChild(lbl)}}
}
function drawComparisonChart(svgEl, data){
if(!svgEl||!data)return;const svg=svgEl;const w=svg.clientWidth||240;const h=svg.clientHeight||120;const pad={t:8,r:8,b:22,l:36};const cw=w-pad.l-pad.r;const ch=h-pad.t-pad.b;const series=data.values;const mx=Math.max(...series.flatMap(s=>s.vals.filter(v=>v!==null)));const nGroups=series[0].vals.length;const groupW=cw/nGroups;const bw=Math.min(groupW*0.25,14);const colors=['#6366f1','#10b981'];svg.innerHTML='<g transform="translate('+pad.l+','+pad.t+')">';const g=svg.querySelector('g');for(let gIdx=0;gIdx<nGroups;gIdx++){for(let sIdx=0;sIdx<series.length;sIdx++){const v=series[sIdx].vals[gIdx];if(v===null)continue;const barH=(v/mx)*ch;const x=gIdx*groupW+groupW*0.1+sIdx*(bw+2);const y=ch-barH;const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');rect.setAttribute('x',x);rect.setAttribute('y',y);rect.setAttribute('width',bw);rect.setAttribute('height',barH);rect.setAttribute('fill',colors[sIdx]);rect.setAttribute('rx','3');g.appendChild(rect)}const txt=document.createElementNS('http://www.w3.org/2000/svg','text');txt.setAttribute('x',gIdx*groupW+groupW/2);txt.setAttribute('y',ch+14);txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','9');txt.setAttribute('fill','#9ca3af');txt.textContent=data.labels[gIdx];g.appendChild(txt)}const legY=-4;for(let i=0;i<series.length;i++){const lx=8+i*70;const lr=document.createElementNS('http://www.w3.org/2000/svg','rect');lr.setAttribute('x',lx);lr.setAttribute('y',legY);lr.setAttribute('width',8);lr.setAttribute('height',8);lr.setAttribute('fill',colors[i]);lr.setAttribute('rx','2');g.appendChild(lr);const lt=document.createElementNS('http://www.w3.org/2000/svg','text');lt.setAttribute('x',lx+11);lt.setAttribute('y',legY+7);lt.setAttribute('font-size','8');lt.setAttribute('fill','#6b7280');lt.textContent=series[i].label;g.appendChild(lt)}
}
function drawLineChart(svgEl, data, color='#6366f1'){
if(!svgEl||!data)return;const svg=svgEl;const w=svg.clientWidth||240;const h=svg.clientHeight||120;const pad={t:8,r:8,b:20,l:32};const cw=w-pad.l-pad.r;const ch=h-pad.t-pad.b;const values=data.values;const mx=Math.max(...values.filter(v=>v!==null));const mn=Math.min(...values.filter(v=>v!==null))||0;const range=mx-mn||1;const step=cw/(values.length-1);svg.innerHTML='<g transform="translate('+pad.l+','+pad.t+')">';const g=svg.querySelector('g');let path='';for(let i=0;i<values.length;i++){if(values[i]===null)continue;const x=i*step;const y=ch-((values[i]-mn)/range)*ch;path+=(i===0?'M':'L')+x+','+y}if(path){const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('d',path);p.setAttribute('fill','none');p.setAttribute('stroke',color);p.setAttribute('stroke-width','2');p.setAttribute('stroke-linejoin','round');g.appendChild(p)}for(let i=0;i<values.length;i++){if(values[i]===null)continue;const x=i*step;const y=ch-((values[i]-mn)/range)*ch;const circ=document.createElementNS('http://www.w3.org/2000/svg','circle');circ.setAttribute('cx',x);circ.setAttribute('cy',y);circ.setAttribute('r','2.5');circ.setAttribute('fill',color);g.appendChild(circ);if(i%Math.max(1,Math.floor(values.length/7))===0){const txt=document.createElementNS('http://www.w3.org/2000/svg','text');txt.setAttribute('x',x);txt.setAttribute('y',ch+14);txt.setAttribute('text-anchor','middle');txt.setAttribute('font-size','9');txt.setAttribute('fill','#9ca3af');txt.textContent=data.labels[i];g.appendChild(txt)}}
}
function renderDashboard(){
drawBarChart(document.getElementById('chart-revenue'),MOCK_DATA.revenue,'#6366f1');
drawBarChart(document.getElementById('chart-customers'),MOCK_DATA.customers,'#10b981');
drawComparisonChart(document.getElementById('chart-comparison'),MOCK_DATA.comparison);
drawLineChart(document.getElementById('chart-cohorts'),MOCK_DATA.cohorts,'#f59e0b');
}
const msgEl=document.getElementById('messages');
const inputEl=document.getElementById('queryInput');
const sendBtn=document.getElementById('sendBtn');
const voiceBtn=document.getElementById('voiceBtn');
const suggestions=document.getElementById('suggestions');
function addMessage(text, role, chartType, chartData){
const div=document.createElement('div');div.className='msg '+role;
const p=document.createElement('p');p.textContent=text;div.appendChild(p);
if(chartType&&chartData){
const chartDiv=document.createElement('div');chartDiv.className='chart-inline';
const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
svg.style.width='100%';svg.style.height='100%';
chartDiv.appendChild(svg);div.appendChild(chartDiv);
setTimeout(()=>{
if(chartType==='bar')drawBarChart(svg,chartData,'#6366f1');
else if(chartType==='line')drawLineChart(svg,chartData,'#f59e0b');
},50)
}
msgEl.appendChild(div);msgEl.scrollTop=msgEl.scrollHeight;
}
function addTypingIndicator(){
const div=document.createElement('div');div.className='msg bot';div.id='typing-indicator';
div.innerHTML='<div class="typing"><span></span><span></span><span></span></div>';
msgEl.appendChild(div);msgEl.scrollTop=msgEl.scrollHeight;
}
function removeTypingIndicator(){
const el=document.getElementById('typing-indicator');if(el)el.remove();
}
const RESPONSES={
'revenue':'The revenue spike on Tuesday ($21.8k) was driven by the product launch campaign that went live Monday evening. Conversion rate hit 8.2% (vs 4.1% avg). Wednesday remained elevated at $16.2k as email sequences continued to convert.',
'customers':'Here are your top 5 customers by MRR — Acme Corp ($12.4k), Globex ($8.9k), Initech ($7.6k), Umbrella Corp ($5.4k), Wayne Enterprises ($4.2k). Together they represent 47% of total MRR ($79.3k).',
'compare':'Q2 2026 vs Q1: Revenue grew 18.2% ($105k to $124.5k). MRR up 12.7% ($43.2k to $48.7k). New customers surged 31% (2,610 to 3,420). Churn improved from 3.8% to 3.2%. The product launch in Q2 was the primary growth catalyst.',
'retention':'The Jan 2026 cohort has the strongest retention at 82% through week 8. Feb cohort trails at 71%. Mar cohort is still young but showing 78% at week 4 — trending well. Suggestion: investigate what onboarding flows drove Jan cohort success and apply to newer cohorts.',
'default':'Based on current dashboard state (date: '+DASHBOARD_STATE.filters.date+', metric: '+DASHBOARD_STATE.filters.metric+'), I see revenue at $'+DASHBOARD_STATE.metrics.revenue.toLocaleString()+', MRR $'+DASHBOARD_STATE.metrics.mrr.toLocaleString()+', and '+DASHBOARD_STATE.metrics.users.toLocaleString()+' active users. What specific insight are you looking for?'
};
function processQuery(q){
const lower=q.toLowerCase();
if(lower.includes('tuesday')||lower.includes('spike')||lower.includes('revenue spike')){return{text:RESPONSES.revenue,chart:'bar',data:MOCK_DATA.revenue,callout:'Revenue spike Tuesday: $21.8k — 2.3x daily average'}}
else if(lower.includes('top 5')||lower.includes('top five')||lower.includes('customer')){return{text:RESPONSES.customers,chart:'bar',data:MOCK_DATA.customers,callout:'Top 5: 47% of total MRR'}}
else if(lower.includes('compar')||lower.includes('quarter')||lower.includes('q1')||lower.includes('q2')){return{text:RESPONSES.compare,chart:null,data:null,callout:'Q2 revenue +18.2% vs Q1'}}
else if(lower.includes('retention')||lower.includes('cohort')||lower.includes('churn')){return{text:RESPONSES.retention,chart:'line',data:MOCK_DATA.cohorts,callout:'Jan cohort: 82% at week 8'}}
return{text:RESPONSES.default,chart:null,data:null,callout:null}
}
function handleQuery(q){
if(!q.trim())return;
addMessage(q,'user');inputEl.value='';addTypingIndicator();
const result=processQuery(q);
const dateFilter=document.getElementById('dateFilter').value;
const metricFilter=document.getElementById('metricFilter').value;
DASHBOARD_STATE.filters.date=dateFilter;
DASHBOARD_STATE.filters.metric=metricFilter;
setTimeout(()=>{
removeTypingIndicator();
addMessage(result.text,'bot',result.chart,result.data);
if(result.callout){
const calloutEls=document.querySelectorAll('.callout');
const activeCallout=calloutEls[calloutEls.length-1];
if(activeCallout)activeCallout.textContent=result.callout;
}
},800+Math.random()*600);
}
sendBtn.addEventListener('click',()=>handleQuery(inputEl.value));
inputEl.addEventListener('keydown',e=>{if(e.key==='Enter')handleQuery(inputEl.value)});
suggestions.addEventListener('click',e=>{
const btn=e.target.closest('button');
if(btn&&btn.dataset.query){handleQuery(btn.dataset.query)}
});
voiceBtn.addEventListener('click',()=>{
if('webkitSpeechRecognition' in window||'SpeechRecognition' in window){
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
const rec=new SR();rec.lang='en-US';rec.interimResults=false;
rec.onresult=function(e){inputEl.value=e.results[0][0].transcript;handleQuery(inputEl.value)};
rec.start();voiceBtn.textContent='🔴';setTimeout(()=>voiceBtn.textContent='🎤',5000)
}else{inputEl.value='Voice input not supported in this browser. Try Chrome.';setTimeout(()=>inputEl.value='',2000)}
});
document.getElementById('dateFilter').addEventListener('change',function(){
DASHBOARD_STATE.filters.date=this.value;
const toast=document.createElement('div');toast.textContent='Filter updated: '+this.value;toast.style.cssText='position:fixed;bottom:80px;right:400px;background:#1a1a2e;color:#fff;padding:8px 16px;border-radius:8px;font-size:13px;z-index:999;animation:fadeIn .2s';
document.body.appendChild(toast);setTimeout(()=>toast.remove(),2000);
});
document.getElementById('metricFilter').addEventListener('change',function(){
DASHBOARD_STATE.filters.metric=this.value;
});
addMessage('Hi, I\'m your AI copilot. I see the dashboard is showing Last 7 days with all metrics. Ask me anything about your data — try one of the suggested queries below.','bot');
renderDashboard();
window.addEventListener('resize',renderDashboard);
})();
</script>
</body>
</html>