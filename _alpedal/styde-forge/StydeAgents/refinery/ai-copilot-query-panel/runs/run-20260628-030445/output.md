```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f2f5;color:#1a1a2e;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 380px;height:100vh}
.main-panel{padding:20px;overflow-y:auto;background:#f8f9fb}
.copilot-panel{background:#fff;border-left:1px solid #e0e3e8;display:flex;flex-direction:column;height:100vh}
.header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid #e0e3e8;background:#fff}
.header h2{font-size:16px;font-weight:600;color:#1a1a2e}
.header-controls{display:flex;gap:10px;align-items:center}
.filter-badge{padding:4px 10px;background:#eef2ff;border-radius:12px;font-size:12px;color:#4f46e5}
.chat-messages{flex:1;overflow-y:auto;padding:16px}
.message{margin-bottom:16px;max-width:100%}
.message.user{text-align:right}
.message.user .bubble{background:#4f46e5;color:#fff;border-radius:16px 16px 4px 16px;padding:10px 14px;display:inline-block;font-size:14px;line-height:1.4;max-width:85%;text-align:left}
.message.assistant .bubble{background:#f0f2f5;color:#1a1a2e;border-radius:16px 16px 16px 4px;padding:10px 14px;display:inline-block;font-size:14px;line-height:1.4;max-width:100%}
.message.assistant .bubble .chart-container{margin-top:10px;background:#fff;border-radius:8px;padding:12px;border:1px solid #e0e3e8}
.message.assistant .bubble .chart-container canvas{width:100%!important;height:200px!important}
.message.assistant .bubble .annotation{background:#fef3c7;border-left:3px solid #f59e0b;padding:8px 10px;margin-top:8px;border-radius:4px;font-size:12px;line-height:1.4;color:#92400e}
.message.assistant .bubble .insight-text{margin-top:6px;font-size:13px;color:#374151}
.suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:10px 16px 4px}
.suggestion-chip{padding:6px 12px;background:#f0f2f5;border-radius:16px;font-size:12px;color:#4f46e5;cursor:pointer;border:none;white-space:nowrap;transition:all .15s}
.suggestion-chip:hover{background:#e0e7ff;transform:translateY(-1px)}
.input-area{padding:12px 16px;border-top:1px solid #e0e3e8;background:#fff}
.input-row{display:flex;gap:8px;align-items:center}
.input-row input{flex:1;padding:10px 14px;border:1px solid #d1d5db;border-radius:20px;font-size:14px;outline:none;transition:border-color .15s}
.input-row input:focus{border-color:#4f46e5}
.input-row button{width:38px;height:38px;border-radius:50%;border:none;background:#4f46e5;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:background .15s;flex-shrink:0}
.input-row button:hover{background:#4338ca}
.input-row button.voice-btn{background:#f0f2f5;color:#6b7280}
.input-row button.voice-btn:hover{background:#e0e3e8}
.input-row button.voice-btn.listening{background:#ef4444;color:#fff;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.typing-indicator{padding:4px 0;color:#9ca3af;font-size:13px;font-style:italic}
.status-bar{display:flex;justify-content:space-between;padding:4px 16px;background:#f9fafb;font-size:11px;color:#6b7280;border-top:1px solid #e0e3e8}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:20px}
.kpi-card{background:#fff;border-radius:12px;padding:16px;border:1px solid #e0e3e8}
.kpi-label{font-size:12px;color:#6b7280;margin-bottom:4px}
.kpi-value{font-size:28px;font-weight:700;color:#1a1a2e}
.kpi-change{font-size:12px;margin-top:4px}
.kpi-change.up{color:#10b981}
.kpi-change.down{color:#ef4444}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.chart-card{background:#fff;border-radius:12px;padding:16px;border:1px solid #e0e3e8}
.chart-card h3{font-size:13px;color:#6b7280;margin-bottom:12px;font-weight:500}
.chart-card canvas{width:100%!important;height:240px!important}
.context-badge{font-size:11px;color:#6b7280;padding:2px 8px;background:#f3f4f6;border-radius:10px}
@media(max-width:900px){.dashboard{grid-template-columns:1fr}.copilot-panel{position:fixed;right:0;top:0;width:380px;box-shadow:-4px 0 20px rgba(0,0,0,.15);z-index:100}}
</style>
</head>
<body>
<div class="dashboard">
  <div class="main-panel">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <div>
        <h1 style="font-size:22px;font-weight:700">Revenue Dashboard</h1>
        <div style="display:flex;gap:12px;margin-top:6px;font-size:13px;color:#6b7280">
          <span>Filters: All regions, All products</span>
          <span>Q1 2026 (Jan 1 - Mar 31)</span>
        </div>
      </div>
      <div style="display:flex;gap:8px">
        <span class="filter-badge">Last 90 days</span>
        <span class="filter-badge">Compare: Q4 2025</span>
      </div>
    </div>
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">$4,283,500</div>
        <div class="kpi-change up">+12.4% vs last quarter</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Active Customers</div>
        <div class="kpi-value">847</div>
        <div class="kpi-change up">+8.2% vs last quarter</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Avg MRR / Customer</div>
        <div class="kpi-value">$5,058</div>
        <div class="kpi-change up">+3.1% vs last quarter</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Churn Rate</div>
        <div class="kpi-value">2.3%</div>
        <div class="kpi-change down">+0.4pp vs last quarter</div>
      </div>
    </div>
    <div class="chart-grid">
      <div class="chart-card">
        <h3>Revenue Trend (Daily)</h3>
        <canvas id="revenueChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Revenue by Product</h3>
        <canvas id="productChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Top Customers by MRR</h3>
        <canvas id="customersChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>QoQ Comparison</h3>
        <canvas id="comparisonChart"></canvas>
      </div>
    </div>
  </div>
  <div class="copilot-panel">
    <div class="header">
      <h2>AI Copilot</h2>
      <div style="display:flex;gap:8px;align-items:center">
        <span class="context-badge" id="contextBadge">Q1 2026</span>
        <button onclick="clearChat()" style="background:none;border:none;cursor:pointer;color:#9ca3af;font-size:16px;padding:4px" title="Clear chat">+</button>
      </div>
    </div>
    <div class="suggestions" id="suggestions">
      <button class="suggestion-chip" onclick="sendQuery('what caused the revenue spike last tuesday')">Revenue spike last Tuesday?</button>
      <button class="suggestion-chip" onclick="sendQuery('top 5 customers by mrr')">Top 5 customers by MRR</button>
      <button class="suggestion-chip" onclick="sendQuery('compare this quarter to last')">Compare QoQ</button>
      <button class="suggestion-chip" onclick="sendQuery('show me churn trends')">Churn trends</button>
      <button class="suggestion-chip" onclick="sendQuery('which product grew the most')">Fastest growing product</button>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="message assistant">
        <div class="bubble">
          Hello! I'm your AI copilot. I can see you're viewing Q1 2026 with All regions and All products selected. Ask me anything about your data — I'll analyze it and generate charts on the fly.
        </div>
      </div>
    </div>
    <div class="input-area">
      <div class="input-row">
        <input type="text" id="queryInput" placeholder="Ask about your data..." onkeydown="if(event.key==='Enter')sendQuery(this.value)">
        <button class="voice-btn" id="voiceBtn" onclick="toggleVoice()" title="Voice input">o</button>
        <button onclick="sendQuery(document.getElementById('queryInput').value)" title="Send">v</button>
      </div>
    </div>
    <div class="status-bar">
      <span>Context: Q1 2026, All regions, All products</span>
      <span id="statusIndicator">Ready</span>
    </div>
  </div>
</div>
<script>
// ---- DATA ----
const DATA = {
  dailyRevenue: [],
  products: [
    {name:'Cloud Pro', revenue:1580000, growth:18.2},
    {name:'Analytics Suite', revenue:1120000, growth:24.7},
    {name:'Data Sync', revenue:875000, growth:-2.1},
    {name:'API Gateway', revenue:453500, growth:31.5},
    {name:'Mobile SDK', revenue:256000, growth:8.9}
  ],
  topCustomers: [
    {name:'Acme Corp', mrr:48500},
    {name:'Globex Inc', mrr:42300},
    {name:'Initech', mrr:38900},
    {name:'Umbrella Co', mrr:35200},
    {name:'Hooli', mrr:31800}
  ],
  weeklyRevenue: [785000,812000,798000,845000,823000,867000,891000,854000,832000,796000,912000,858000],
  weeklyRevenuePrev: [712000,698000,734000,755000,721000,743000,768000,752000,739000,728000,756000,741000]
};
const startDate = new Date(2026,0,1);
for(let i=0;i<90;i++){
  const d = new Date(startDate);
  d.setDate(d.getDate()+i);
  const base = 46000 + Math.sin(i*0.3)*8000 + Math.random()*6000;
  const spike = (i===58||i===59||i===60)?25000+Math.random()*8000:0;
  DATA.dailyRevenue.push({date:d,value:Math.round(base+spike)});
}
// ---- CHART ENGINE ----
function getCanvasContext(id,width,height){
  const canvas = document.getElementById(id);
  if(!canvas)return null;
  canvas.width=width||canvas.parentElement.clientWidth||300;
  canvas.height=height||240;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0,0,canvas.width,canvas.height);
  return ctx;
}
function drawLineChart(ctx,labels,datasets,options={}){
  if(!ctx)return;
  const w=ctx.canvas.width,h=ctx.canvas.height;
  const pad={top:20,bottom:30,left:45,right:20};
  const cw=w-pad.left-pad.right,ch=h-pad.top-pad.bottom;
  ctx.clearRect(0,0,w,h);
  const allValues=datasets.flatMap(d=>d.data);
  const yMin=Math.min(...allValues)*0.9,yMax=Math.max(...allValues)*1.1;
  const yRange=yMax-yMin||1;
  ctx.strokeStyle='#e5e7eb';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=pad.top+ch*(1-i/4);
    const val=yMin+yRange*i/4;
    ctx.beginPath();ctx.moveTo(pad.left,y);ctx.lineTo(w-pad.right,y);ctx.stroke();
    ctx.fillStyle='#9ca3af';ctx.font='10px sans-serif';ctx.textAlign='right';
    ctx.fillText('$'+(val/1000).toFixed(0)+'k',pad.left-5,y+3);
  }
  const colors=['#4f46e5','#10b981','#f59e0b','#ef4444'];
  datasets.forEach((ds,di)=>{
    const color=colors[di%colors.length];
    const step=cw/(ds.data.length-1||1);
    ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=2;
    ds.data.forEach((v,i)=>{
      const x=pad.left+i*step,y=pad.top+ch-(v-yMin)/yRange*ch;
      i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    });
    ctx.stroke();
    ds.data.forEach((v,i)=>{
      const x=pad.left+i*step,y=pad.top+ch-(v-yMin)/yRange*ch;
      ctx.beginPath();ctx.arc(x,y,3,0,Math.PI*2);ctx.fillStyle=color;ctx.fill();
    });
  });
  if(labels&&labels.length>1){
    ctx.fillStyle='#9ca3af';ctx.font='10px sans-serif';ctx.textAlign='center';
    const labelStep=cw/(labels.length-1||1);
    labels.forEach((l,i)=>{
      if(i%Math.max(1,Math.floor(labels.length/8))===0||i===labels.length-1){
        const x=pad.left+i*labelStep;
        ctx.fillText(typeof l==='string'?l:l.toLocaleString(),x,h-8);
      }
    });
  }
  // annotations
  if(options.annotations){
    options.annotations.forEach(a=>{
      const idx=a.index;
      const step=cw/((datasets[0]?.data.length||1)-1||1);
      const x=pad.left+idx*step;
      const v=datasets[0]?.data[idx]||0;
      const y=pad.top+ch-(v-yMin)/yRange*ch;
      ctx.strokeStyle='#f59e0b';ctx.setLineDash([4,4]);ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(x,pad.top);ctx.lineTo(x,pad.top+ch);ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle='#fef3c7';ctx.strokeStyle='#f59e0b';ctx.lineWidth=1;
      ctx.beginPath();ctx.roundRect(x-60,y-30,120,24,4);ctx.fill();ctx.stroke();
      ctx.fillStyle='#92400e';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText(a.text,x,y-14);
    });
  }
}
function drawBarChart(ctx,labels,values,options={}){
  if(!ctx)return;
  const w=ctx.canvas.width,h=ctx.canvas.height;
  const pad={top:20,bottom:30,left:45,right:20};
  const cw=w-pad.left-pad.right,ch=h-pad.top-pad.bottom;
  ctx.clearRect(0,0,w,h);
  const maxVal=Math.max(...values)*1.15;
  const barWidth=Math.min(cw/values.length*0.7,40);
  const gap=cw/values.length;
  ctx.strokeStyle='#e5e7eb';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=pad.top+ch*(1-i/4);
    ctx.beginPath();ctx.moveTo(pad.left,y);ctx.lineTo(w-pad.right,y);ctx.stroke();
    ctx.fillStyle='#9ca3af';ctx.font='10px sans-serif';ctx.textAlign='right';
    ctx.fillText('$'+(maxVal*i/4/1000).toFixed(0)+'k',pad.left-5,y+3);
  }
  const colors=options.colors||values.map(()=>'#4f46e5');
  values.forEach((v,i)=>{
    const x=pad.left+i*gap+(gap-barWidth)/2;
    const barH=v/maxVal*ch;
    const y=pad.top+ch-barH;
    const gradient=ctx.createLinearGradient(x,y,x,pad.top+ch);
    gradient.addColorStop(0,colors[i]||'#4f46e5');
    gradient.addColorStop(1,(colors[i]||'#4f46e5')+'66');
    ctx.fillStyle=gradient;
    ctx.beginPath();ctx.roundRect(x,y,barWidth,barH,4);ctx.fill();
    ctx.fillStyle='#374151';ctx.font='11px sans-serif';ctx.textAlign='center';
    const label=options.formatter?options.formatter(v):v>=1000?'$'+(v/1000).toFixed(1)+'k':'$'+v.toLocaleString();
    ctx.fillText(label,x+barWidth/2,y-6);
    if(labels&&labels[i]){
      ctx.fillStyle='#6b7280';ctx.font='10px sans-serif';ctx.textAlign='center';
      ctx.fillText(labels[i],x+barWidth/2,h-8);
    }
  });
}
function drawGroupedBarChart(ctx,labels,datasets,options={}){
  if(!ctx)return;
  const w=ctx.canvas.width,h=ctx.canvas.height;
  const pad={top:25,bottom:30,left:45,right:20};
  const cw=w-pad.left-pad.right,ch=h-pad.top-pad.bottom;
  ctx.clearRect(0,0,w,h);
  const allVals=datasets.flatMap(d=>d.data);
  const maxVal=Math.max(...allVals)*1.15;
  const groupWidth=cw/labels.length;
  const n=datasets.length;
  const barWidth=Math.min(groupWidth*0.7/n,22);
  ctx.strokeStyle='#e5e7eb';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=pad.top+ch*(1-i/4);
    ctx.beginPath();ctx.moveTo(pad.left,y);ctx.lineTo(w-pad.right,y);ctx.stroke();
    ctx.fillStyle='#9ca3af';ctx.font='10px sans-serif';ctx.textAlign='right';
    ctx.fillText('$'+(maxVal*i/4/1000).toFixed(0)+'k',pad.left-5,y+3);
  }
  const colors=['#4f46e5','#93c5fd'];
  const legends={};
  datasets.forEach((ds,di)=>{
    legends[ds.label]=colors[di%colors.length];
    ds.data.forEach((v,i)=>{
      const x=pad.left+i*groupWidth+(groupWidth-n*barWidth)/2+di*barWidth;
      const barH=v/maxVal*ch;
      const y=pad.top+ch-barH;
      ctx.fillStyle=colors[di%colors.length];
      ctx.beginPath();ctx.roundRect(x,y,barWidth-2,barH,3);ctx.fill();
    });
  });
  labels.forEach((l,i)=>{
    ctx.fillStyle='#6b7280';ctx.font='10px sans-serif';ctx.textAlign='center';
    ctx.fillText(l,pad.left+i*groupWidth+groupWidth/2,h-8);
  });
  // legend
  let lx=pad.left;
  Object.entries(legends).forEach(([label,color])=>{
    ctx.fillStyle=color;ctx.fillRect(lx,6,10,10);
    ctx.fillStyle='#374151';ctx.font='10px sans-serif';ctx.textAlign='left';
    ctx.fillText(label,lx+14,15);
    lx+=ctx.measureText(label).width+30;
  });
}
ctxProto=CanvasRenderingContext2D.prototype;
if(!ctxProto.roundRect){
  ctxProto.roundRect=function(x,y,w,h,r){
    if(r>w/2)r=w/2;if(r>h/2)r=h/2;
    this.moveTo(x+r,y);this.lineTo(x+w-r,y);
    this.quadraticCurveTo(x+w,y,x+w,y+r);
    this.lineTo(x+w,y+h-r);
    this.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    this.lineTo(x+r,y+h);
    this.quadraticCurveTo(x,y+h,x,y+h-r);
    this.lineTo(x,y+r);
    this.quadraticCurveTo(x,y,x+r,y);
    this.closePath();
    return this;
  };
}
// ---- NL PARSER ----
function parseQuery(query){
  const q=query.toLowerCase().trim();
  const context={
    dateRange:{start:'2026-01-01',end:'2026-03-31'},
    filters:{region:'All',product:'All'},
    visibleMetrics:['revenue','customers','mrr','churn']
  };
  if(q.includes('spike')||(q.includes('revenue')&&q.includes('tuesday'))){
    return{
      type:'analyze_spike',
      metric:'revenue',
      date:'2026-03-03',
      context
    };
  }
  if((q.includes('top')||q.includes('leading'))&&q.includes('customer')){
    return{
      type:'top_customers',
      metric:'mrr',
      limit:5,
      context
    };
  }
  if(q.includes('compare')&&(q.includes('quarter')||q.includes('qoq')||q.includes('last'))){
    return{
      type:'compare',
      metric:'revenue',
      period1:'Q1 2026',
      period2:'Q4 2025',
      context
    };
  }
  if(q.includes('churn')||q.includes('retention')){
    return{
      type:'trend',
      metric:'churn',
      context
    };
  }
  if((q.includes('product')||q.includes('grew')||q.includes('fastest'))&&(q.includes('growth')||q.includes('grew')||q.includes('fastest'))){
    return{
      type:'product_growth',
      metric:'growth',
      context
    };
  }
  if(q.includes('revenue')&&(q.includes('trend')||q.includes('over time')||q.includes('show'))){
    return{
      type:'revenue_trend',
      context
    };
  }
  return{
    type:'general',
    query:q,
    context
  };
}
// ---- QUERY EXECUTOR ----
function executeQuery(parsed){
  switch(parsed.type){
    case 'analyze_spike':return analyzeSpike(parsed);
    case 'top_customers':return getTopCustomers(parsed);
    case 'compare':return compareQuarters(parsed);
    case 'trend':return getChurnTrend(parsed);
    case 'product_growth':return getProductGrowth(parsed);
    case 'revenue_trend':return getRevenueTrend(parsed);
    default:return generalResponse(parsed);
  }
}
function getDaysSinceStart(dateStr){
  const d=new Date(dateStr);
  const start=new Date(2026,0,1);
  return Math.floor((d-start)/(86400000));
}
function analyzeSpike(parsed){
  const spikeDays=[58,59,60];
  const spikeData=spikeDays.map(i=>({day:i,date:DATA.dailyRevenue[i].date,revenue:DATA.dailyRevenue[i].value}));
  const avgPrev=spikeDays.map(i=>{
    const vals=DATA.dailyRevenue.slice(Math.max(0,i-7),i).map(d=>d.value);
    return vals.reduce((a,b)=>a+b,0)/vals.length;
  });
  const avgPrevOverall=avgPrev.reduce((a,b)=>a+b,0)/avgPrev.length;
  const spikeTotal=spikeData.reduce((a,b)=>a+b.revenue,0);
  const estimatedNormal=avgPrevOverall*3;
  const impact=spikeTotal-estimatedNormal;
  const pctIncrease=(impact/estimatedNormal*100);
  const topProducts=DATA.products.slice().sort((a,b)=>b.growth-a.growth);
  const likelyProduct=topProducts[0];
  const annotation=impact>30000?
    `Major anomaly detected: +$${(impact/1000).toFixed(0)}k (${pctIncrease.toFixed(0)}% above baseline) over 3 days. Primary contributor appears to be ${likelyProduct.name} (${likelyProduct.growth}% growth).`:
    `Moderate increase of $${(impact/1000).toFixed(0)}k (${pctIncrease.toFixed(0)}% above baseline).`;
  return{
    text:`Revenue Spike Analysis - March 1-3, 2026
A revenue spike of $${(spikeTotal/1000).toFixed(0)}k was detected across March 1-3, approximately ${pctIncrease.toFixed(0)}% above the trailing 7-day average of $${(avgPrevOverall/1000).toFixed(1)}k/day.
${annotation}
Breakdown by day:
${spikeData.map(d=>`  ${d.date.toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric'})}: $${(d.revenue/1000).toFixed(0)}k`).join('\n')}
Suggested drill-down: filter by product category to identify which segments drove the increase.`,
    type:'bar',
    chartData:{
      labels:spikeData.map(d=>d.date.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})),
      values:spikeData.map(d=>d.revenue),
      colors:['#f59e0b','#f59e0b','#f59e0b']
    },
    annotations:[{index:0,text:`+${pctIncrease.toFixed(0)}% vs avg`}],
    insight:`The spike coincides with the ${likelyProduct.name} product launch. Revenue increased ${likelyProduct.growth}% this quarter.`
  };
}
function getTopCustomers(parsed){
  const limit=parsed.limit||5;
  const top=DATA.topCustomers.slice(0,limit);
  return{
    text:`Top ${limit} Customers by MRR
${top.map((c,i)=>`  ${i+1}. ${c.name} - $${c.mrr.toLocaleString()}/mo`).join('\n')}
These ${limit} customers represent $${top.reduce((a,b)=>a+b.mrr,0).toLocaleString()}/mo in MRR, approximately ${(top.reduce((a,b)=>a+b.mrr,0)/5058*100).toFixed(0)}% of total customer count.`,
    type:'bar',
    chartData:{
      labels:top.map(c=>c.name),
      values:top.map(c=>c.mrr),
      colors:['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe']
    },
    annotations:[],
    insight:`${top[0].name} leads at $${top[0].mrr.toLocaleString()}/mo. Consider a QBR with the bottom 2 to discuss expansion opportunities.`
  };
}
function compareQuarters(parsed){
  const currentTotal=DATA.weeklyRevenue.reduce((a,b)=>a+b,0);
  const prevTotal=DATA.weeklyRevenuePrev.reduce((a,b)=>a+b,0);
  const change=((currentTotal-prevTotal)/prevTotal*100);
  const weeks=DATA.weeklyRevenue.map((_,i)=>`W${i+1}`);
  return{
    text:`Quarter-over-Quarter Comparison
Q1 2026 Revenue: $${(currentTotal/1000).toFixed(0)}k
Q4 2025 Revenue: $${(prevTotal/1000).toFixed(0)}k
Change: ${change>0?'+':''}${change.toFixed(1)}%
Q1 2026 outperformed Q4 2025 across most weeks. The largest gap occurred in weeks 6-7 (mid-Feb), where revenue peaked at $${(Math.max(...DATA.weeklyRevenue)/1000).toFixed(0)}k/week.
Key metrics comparison:
  Weekly avg Q1 2026: $${(currentTotal/DATA.weeklyRevenue.length/1000).toFixed(1)}k
  Weekly avg Q4 2025: $${(prevTotal/DATA.weeklyRevenuePrev.length/1000).toFixed(1)}k
  Best week Q1: $${(Math.max(...DATA.weeklyRevenue)/1000).toFixed(0)}k (W${DATA.weeklyRevenue.indexOf(Math.max(...DATA.weeklyRevenue))+1})
  Best week Q4: $${(Math.max(...DATA.weeklyRevenuePrev)/1000).toFixed(0)}k (W${DATA.weeklyRevenuePrev.indexOf(Math.max(...DATA.weeklyRevenuePrev))+1})`,
    type:'groupedBar',
    chartData:{
      labels:weeks,
      datasets:[
        {label:'Q1 2026',data:DATA.weeklyRevenue},
        {label:'Q4 2025',data:DATA.weeklyRevenuePrev}
      ]
    },
    annotations:[],
    insight:`Q1 2026 shows a ${change.toFixed(1)}% improvement over Q4 2025. The growth appears to accelerate in weeks 5-8, suggesting the new feature releases in Feb drove adoption.`
  };
}
function getChurnTrend(parsed){
  const churnRates=[2.8,2.6,2.5,2.4,2.3,2.3,2.4,2.3,2.2,2.1,2.2,2.3];
  const months=['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep'];
  const currentRate=churnRates[3];
  const prevQuarterAvg=(churnRates[0]+churnRates[1]+churnRates[2])/3;
  return{
    text:`Churn Rate Trend Analysis
Current churn rate (Q1 2026): ${currentRate}%
Previous quarter avg (Q4 2025): ${prevQuarterAvg.toFixed(1)}%
Change: ${(currentRate-prevQuarterAvg)>0?'+':''}${(currentRate-prevQuarterAvg).toFixed(1)}pp
Churn has shown a gradual decline from 2.8% in October to 2.2% in June (lowest point), before rising slightly to 2.3% in recent months. The Q1 2026 average of 2.3% represents an improvement of ${(prevQuarterAvg-currentRate).toFixed(1)} percentage points versus Q4 2025.
Key observations:
  - Churn bottomed at 2.1% in June, suggesting the customer success initiatives launched in Q1 are taking effect
  - The slight uptick to 2.3% in recent months warrants monitoring
  - Current rate of 2.3% is within healthy SaaS benchmarks (2-3% monthly is typical for SMB-focused products)`,
    type:'line',
    chartData:{
      labels:months,
      datasets:[{label:'Churn Rate %',data:churnRates,color:'#ef4444'}]
    },
    annotations:[{index:7,text:'Low: 2.1%'}],
    insight:`Churn improved ${(prevQuarterAvg-currentRate).toFixed(1)}pp QoQ. The customer success program launch in Jan correlates with the downward trend.`
  };
}
function getProductGrowth(parsed){
  const sorted=DATA.products.slice().sort((a,b)=>b.growth-a.growth);
  const top=sorted[0];
  const bottom=sorted[sorted.length-1];
  return{
    text:`Product Growth Analysis (QoQ)
${sorted.map((p,i)=>`  ${i+1}. ${p.name}: ${p.growth>0?'+':''}${p.growth}% | Revenue: $${(p.revenue/1000).toFixed(0)}k`).join('\n')}
Fastest growing: ${top.name} at +${top.growth}% — driven by the new API version 3 launch and enterprise tier expansion.
Slowest: ${bottom.name} at ${bottom.growth}% — may need pricing review or feature refresh.
Revenue concentration:
  ${sorted[0].name} + ${sorted[1].name}: $${((sorted[0].revenue+sorted[1].revenue)/1000).toFixed(0)}k (${((sorted[0].revenue+sorted[1].revenue)/DATA.products.reduce((a,b)=>a+b.revenue,0)*100).toFixed(0)}% of total)
  Bottom 3 combined: $${((sorted[2].revenue+sorted[3].revenue+sorted[4].revenue)/1000).toFixed(0)}k`,
    type:'bar',
    chartData:{
      labels:sorted.map(p=>p.name),
      values:sorted.map(p=>p.revenue),
      colors:sorted.map(p=>p.growth>0?'#10b981':'#ef4444')
    },
    annotations:[],
    insight:`${top.name} is the growth champion at +${top.growth}%. ${bottom.name} at ${bottom.growth}% needs attention — consider A/B testing new pricing tiers.`
  };
}
function getRevenueTrend(parsed){
  const weeklyData=[];
  for(let w=0;w<12;w++){
    const start=w*7;
    const end=Math.min(start+7,DATA.dailyRevenue.length);
    const week=data=>data.slice(start,end).reduce((a,b)=>a+b.value,0);
    weeklyData.push(week(DATA.dailyRevenue));
  }
  const labels=weeklyData.map((_,i)=>`W${i+1}`);
  const total=weeklyData.reduce((a,b)=>a+b,0);
  const avg=total/weeklyData.length;
  return{
    text:`Revenue Trend Overview (Q1 2026)
Total Revenue: $${(total/1000).toFixed(0)}k
Weekly Average: $${(avg/1000).toFixed(1)}k
Best Week: W${weeklyData.indexOf(Math.max(...weeklyData))+1} at $${(Math.max(...weeklyData)/1000).toFixed(0)}k
Lowest Week: W${weeklyData.indexOf(Math.min(...weeklyData))+1} at $${(Math.min(...weeklyData)/1000).toFixed(0)}k
The trend shows a generally upward trajectory with some week-to-week variability. Revenue peaked in the period corresponding to the product launch (W9-10), with a notable spike.`,
    type:'line',
    chartData:{
      labels,
      datasets:[{label:'Weekly Revenue',data:weeklyData,color:'#4f46e5'}]
    },
    annotations:[
      {index:weeklyData.indexOf(Math.max(...weeklyData)),text:`Peak: $${(Math.max(...weeklyData)/1000).toFixed(0)}k`}
    ],
    insight:`Revenue is trending up with a ${((weeklyData[weeklyData.length-1]-weeklyData[0])/weeklyData[0]*100).toFixed(0)}% increase from W1 to W12.`
  };
}
function generalResponse(parsed){
  return{
    text:`I understand you're asking about: "${parsed.query}"
Based on the current dashboard context (Q1 2026, All regions, All products), here's what I can help with:
Available insights:
  1. Revenue spike analysis (March 1-3 detected)
  2. Top customers by MRR
  3. Quarter-over-quarter comparison
  4. Product growth analysis
  5. Churn trend analysis
  6. Revenue trend overview
Try one of these suggested queries, or rephrase your question with specific metrics like "revenue", "customers", "churn", or "products".`,
    type:'text',
    chartData:null,
    annotations:[],
    insight:''
  };
}
// ---- RENDER ----
function renderResult(result){
  const chat=document.getElementById('chatMessages');
  const div=document.createElement('div');
  div.className='message assistant';
  let bubbleHTML=`<div class="bubble">${result.text.replace(/\n/g,'<br>')}`;
  if(result.insight){
    bubbleHTML+=`<div class="insight-text">Insight: ${result.insight}</div>`;
  }
  if(result.chartData){
    const chartId='chart_'+Date.now();
    bubbleHTML+=`<div class="chart-container"><canvas id="${chartId}" width="310" height="200"></canvas></div>`;
    bubbleHTML+=`</div>`;
    div.innerHTML=bubbleHTML;
    chat.appendChild(div);
    chat.scrollTop=chat.scrollHeight;
    setTimeout(()=>{
      renderChartById(chartId,result);
    },50);
  }else{
    bubbleHTML+=`</div>`;
    div.innerHTML=bubbleHTML;
    chat.appendChild(div);
    chat.scrollTop=chat.scrollHeight;
  }
  updateStatus('Ready');
}
function renderChartById(id,result){
  const ctx=getCanvasContext(id,310,200);
  if(!ctx)return;
  if(result.type==='bar'){
    drawBarChart(ctx,result.chartData.labels,result.chartData.values,{
      colors:result.chartData.colors,
      formatter:v=>'$'+(v/1000).toFixed(0)+'k'
    });
    if(result.annotations&&result.annotations.length>0){
      const w=ctx.canvas.width,h=ctx.canvas.height;
      ctx.fillStyle='#fef3c7';ctx.strokeStyle='#f59e0b';ctx.lineWidth=1;
      const maxVal=Math.max(...result.chartData.values)*1.15;
      const idx=result.annotations[0].index;
      const gap=ctx.canvas.width/result.chartData.labels.length;
      const x=idx*gap+gap/2;
      ctx.beginPath();ctx.roundRect(x-70,8,140,22,6);ctx.fill();ctx.stroke();
      ctx.fillStyle='#92400e';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText(result.annotations[0].text,x,23);
    }
  }else if(result.type==='groupedBar'){
    drawGroupedBarChart(ctx,result.chartData.labels,result.chartData.datasets);
  }else if(result.type==='line'){
    drawLineChart(ctx,result.chartData.labels,result.chartData.datasets,{
      annotations:result.annotations||[]
    });
  }
}
// ---- CHAT ----
function sendQuery(input){
  if(!input||!input.trim())return;
  const query=input.trim();
  document.getElementById('queryInput').value='';
  updateStatus('Thinking...');
  const chat=document.getElementById('chatMessages');
  const userDiv=document.createElement('div');
  userDiv.className='message user';
  userDiv.innerHTML=`<div class="bubble">${query.replace(/</g,'&lt;')}</div>`;
  chat.appendChild(userDiv);
  chat.scrollTop=chat.scrollHeight;
  const typingDiv=document.createElement('div');
  typingDiv.className='typing-indicator';
  typingDiv.textContent='Copilot is analyzing your data...';
  chat.appendChild(typingDiv);
  chat.scrollTop=chat.scrollHeight;
  setTimeout(()=>{
    typingDiv.remove();
    const parsed=parseQuery(query);
    const result=executeQuery(parsed);
    renderResult(result);
    updateSuggestions(query);
    updateStatus('Ready');
  },800+Math.random()*600);
}
function clearChat(){
  const chat=document.getElementById('chatMessages');
  chat.innerHTML=`<div class="message assistant">
    <div class="bubble">
      Chat cleared. I still see Q1 2026 with All regions and All products. Ask me anything about your data.
    </div>
  </div>`;
}
function updateStatus(text){
  document.getElementById('statusIndicator').textContent=text;
}
function updateSuggestions(lastQuery){
  const chips=document.querySelectorAll('.suggestion-chip');
  const followups={
    'spike':['Show me the products driving this spike','Compare this week to last week','Show me customer activity during the spike'],
    'customer':['Show revenue breakdown by customer tier','Which customers grew the most MRR?','Show customers at risk of churning'],
    'compare':['Show me MoM comparison','Compare by product category','Show YOY growth rate'],
    'churn':['Show churn by customer segment','What causes churn? (top 3 reasons)','Show retention cohort analysis'],
    'product':['Show product margin analysis','Compare product adoption rates','Show feature usage by product'],
    'revenue':['Show revenue by region','Forecast next quarter revenue','Show revenue by customer segment']
  };
  let key='revenue';
  const lq=lastQuery.toLowerCase();
  if(lq.includes('spike'))key='spike';
  else if(lq.includes('customer')||lq.includes('mrr'))key='customer';
  else if(lq.includes('compare')||lq.includes('quarter'))key='compare';
  else if(lq.includes('churn'))key='churn';
  else if(lq.includes('product')||lq.includes('growth'))key='product';
  const suggestions=followups[key]||followups.revenue;
  const container=document.getElementById('suggestions');
  container.innerHTML=suggestions.map(s=>
    `<button class="suggestion-chip" onclick="sendQuery('${s.replace(/'/g,"\\'")}')">${s}</button>`
  ).join('');
}
// ---- VOICE ----
let mediaRecorder=null;
let audioChunks=[];
let isListening=false;
function toggleVoice(){
  const btn=document.getElementById('voiceBtn');
  if(!isListening){
    if(!('webkitSpeechRecognition' in window)&&!('SpeechRecognition' in window)){
      updateStatus('Voice input not supported in this browser');
      return;
    }
    isListening=true;
    btn.classList.add('listening');
    btn.textContent='x';
    updateStatus('Listening...');
    const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
    const recognition=new SpeechRecognition();
    recognition.lang='en-US';
    recognition.interimResults=true;
    recognition.maxAlternatives=1;
    recognition.onresult=function(event){
      const transcript=Array.from(event.results)
        .map(r=>r[0].transcript)
        .join('');
      document.getElementById('queryInput').value=transcript;
      if(event.results[event.results.length-1].isFinal){
        recognition.stop();
        isListening=false;
        btn.classList.remove('listening');
        btn.textContent='o';
        updateStatus('Voice captured');
        setTimeout(()=>sendQuery(transcript),300);
      }
    };
    recognition.onerror=function(){
      isListening=false;
      btn.classList.remove('listening');
      btn.textContent='o';
      updateStatus('Voice input error - try again');
    };
    recognition.onend=function(){
      if(isListening){
        isListening=false;
        btn.classList.remove('listening');
        btn.textContent='o';
        updateStatus('Ready');
      }
    };
    recognition.start();
  }else{
    isListening=false;
    btn.classList.remove('listening');
    btn.textContent='o';
    updateStatus('Ready');
  }
}
// ---- INIT CHARTS ----
function initCharts(){
  // Revenue line chart
  const labels=DATA.dailyRevenue.filter((_,i)=>i%7===0||i===89).map(d=>d.date.toLocaleDateString('en-US',{month:'short',day:'numeric'}));
  const ctx1=getCanvasContext('revenueChart');
  const weeklySum=[];
  for(let w=0;w<12;w++){
    const start=w*7;const end=Math.min(start+7,DATA.dailyRevenue.length);
    weeklySum.push(DATA.dailyRevenue.slice(start,end).reduce((a,b)=>a+b.value,0));
  }
  drawLineChart(ctx1,weeklySum.map((_,i)=>'W'+(i+1)),[{label:'Revenue',data:weeklySum,color:'#4f46e5'}],{
    annotations:[
      {index:8,text:'Spike detected'}
    ]
  });
  const ctx2=getCanvasContext('productChart');
  drawBarChart(ctx2,DATA.products.map(p=>p.name),DATA.products.map(p=>p.revenue),{colors:['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe'],formatter:v=>'$'+(v/1000).toFixed(0)+'k'});
  const ctx3=getCanvasContext('customersChart');
  drawBarChart(ctx3,DATA.topCustomers.map(c=>c.name),DATA.topCustomers.map(c=>c.mrr),{colors:['#10b981','#34d399','#6ee7b7','#a7f3d0','#d1fae5'],formatter:v=>'$'+(v/1000).toFixed(0)+'k'});
  const ctx4=getCanvasContext('comparisonChart');
  drawGroupedBarChart(ctx4,DATA.weeklyRevenue.map((_,i)=>'W'+(i+1)),[
    {label:'Q1 2026',data:DATA.weeklyRevenue},
    {label:'Q4 2025',data:DATA.weeklyRevenuePrev}
  ]);
}
window.onload=function(){initCharts();};
</script>
</body>
</html>
```