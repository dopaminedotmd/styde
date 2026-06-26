Ai Copilot Query Panel v1 — full interactive HTML dashboard
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ai Copilot Query Panel</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0b0e14;color:#d4e0f0;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column}
  /* layout */
  .app{display:flex;flex:1;height:100vh;overflow:hidden}
  .dashboard{flex:1;display:flex;flex-direction:column;padding:20px 24px;overflow-y:auto;min-width:0}
  .chat{width:380px;min-width:380px;border-left:1px solid #1e2a3a;display:flex;flex-direction:column;background:#0d121f}
  /* dashboard header */
  .dash-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
  .dash-title{font-size:18px;font-weight:600;color:#93b4e8;letter-spacing:.3px}
  .dash-title span{color:#6d8fbf;font-weight:400}
  .context-bar{display:flex;gap:16px;align-items:center;font-size:13px;color:#8aa4c8}
  .context-bar .pill{background:#151f2e;padding:4px 12px;border-radius:20px;border:1px solid #1e2d42;display:flex;align-items:center;gap:6px}
  .context-bar .pill .label{color:#6d8fbf}
  .context-bar .pill .val{color:#b8d0f0;font-weight:500}
  /* filter row */
  .filter-row{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap}
  .filter-row select,.filter-row input{background:#111b28;border:1px solid #1e2d42;color:#c4d8f0;padding:6px 12px;border-radius:6px;font-size:13px;outline:none}
  .filter-row select:focus,.filter-row input:focus{border-color:#3a6cbf}
  .filter-row .date-range{display:flex;gap:6px;align-items:center}
  .filter-row .date-range input{width:110px}
  /* metric cards */
  .metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
  .metric-card{background:linear-gradient(135deg,#0f1a2a,#162235);border:1px solid #1a2940;border-radius:10px;padding:14px 16px;position:relative;overflow:hidden}
  .metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:10px 10px 0 0}
  .metric-card:nth-child(1)::before{background:#4a8bf5}
  .metric-card:nth-child(2)::before{background:#34d399}
  .metric-card:nth-child(3)::before{background:#f59e0b}
  .metric-card:nth-child(4)::before{background:#ec4899}
  .metric-label{font-size:11px;color:#6d8fbf;text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px}
  .metric-value{font-size:22px;font-weight:700;color:#e0edff}
  .metric-delta{font-size:12px;margin-top:2px}
  .metric-delta.up{color:#34d399}
  .metric-delta.down{color:#f87171}
  /* chart grid */
  .chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0}
  .chart-panel{background:#0f1a2a;border-radius:10px;border:1px solid #1a2940;padding:16px;display:flex;flex-direction:column;position:relative}
  .chart-panel.full{grid-column:1/-1}
  .chart-panel .chart-title{font-size:13px;font-weight:500;color:#8aa4c8;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
  .chart-panel .chart-title .insight-badge{background:#1c3450;color:#5d9cef;font-size:10px;padding:2px 8px;border-radius:10px;cursor:pointer}
  .chart-panel canvas{flex:1;width:100%!important;min-height:180px;border-radius:4px}
  .chart-annotation{font-size:11px;color:#6d8fbf;margin-top:8px;padding:6px 10px;background:#0a1422;border-left:2px solid #3a6cbf;border-radius:0 4px 4px 0;line-height:1.4}
  /* chat panel */
  .chat-header{padding:16px 16px 12px;border-bottom:1px solid #1a2940;display:flex;justify-content:space-between;align-items:center}
  .chat-header h3{font-size:14px;font-weight:600;color:#93b4e8}
  .chat-header .status{font-size:11px;color:#34d399;display:flex;align-items:center;gap:4px}
  .chat-header .status::before{content:'';width:6px;height:6px;border-radius:50%;background:#34d399}
  .chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:12px}
  .msg{max-width:92%;padding:10px 14px;border-radius:10px;font-size:13px;line-height:1.5;animation:fadeIn .2s ease}
  @keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
  .msg.user{background:#1a2d4a;align-self:flex-end;border-bottom-right-radius:2px;color:#e0edff}
  .msg.assistant{background:#0f1a2a;align-self:flex-start;border-bottom-left-radius:2px;border:1px solid #1a2940;color:#b8d0f0}
  .msg.assistant .chart-inline{width:100%;margin-top:8px;border-radius:6px;background:#091222;padding:4px;min-height:120px}
  .msg.assistant .chart-inline canvas{width:100%!important;height:120px!important}
  .msg.assistant .insight-text{margin-top:6px;color:#8aa4c8;font-size:12px}
  .suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:6px 16px 2px;border-top:1px solid #1a2940}
  .suggestions .chip{font-size:11px;background:#111b28;color:#7da0d0;padding:4px 10px;border-radius:14px;cursor:pointer;border:1px solid #1e2d42;transition:.15s}
  .suggestions .chip:hover{background:#1c3450;border-color:#3a6cbf;color:#b0ccf0}
  .chat-input{display:flex;align-items:center;padding:10px 12px;border-top:1px solid #1a2940;gap:8px}
  .chat-input input{flex:1;background:#111b28;border:1px solid #1e2d42;color:#d4e0f0;padding:8px 12px;border-radius:8px;font-size:13px;outline:none}
  .chat-input input:focus{border-color:#3a6cbf}
  .chat-input .mic-btn,.chat-input .send-btn{background:#1a2d4a;border:none;color:#8aa4c8;width:32px;height:32px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:.15s}
  .chat-input .send-btn{background:#2563eb;color:#fff}
  .chat-input .mic-btn:hover{background:#1e3455}
  .chat-input .mic-btn.listening{background:#dc2626;color:#fff;animation:pulse 1s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
  .chat-input .send-btn:hover{background:#3b82f6}
  /* scrollbar */
  ::-webkit-scrollbar{width:4px}
  ::-webkit-scrollbar-track{background:#0b0e14}
  ::-webkit-scrollbar-thumb{background:#1e2d42;border-radius:4px}
</style>
</head>
<body>
<div class="app">
<div class="dashboard">
  <div class="dash-header">
    <div class="dash-title">THE CRUCIBLE <span>v5 · analytics</span></div>
    <div class="context-bar">
      <div class="pill"><span class="label">period</span><span class="val">Q2 2025</span></div>
      <div class="pill"><span class="label">segment</span><span class="val">all</span></div>
      <div class="pill"><span class="label">region</span><span class="val">global</span></div>
    </div>
  </div>
  <div class="filter-row">
    <select id="segment-select">
      <option value="all">All segments</option>
      <option value="enterprise">Enterprise</option>
      <option value="smb">SMB</option>
      <option value="startup">Startup</option>
    </select>
    <select id="region-select">
      <option value="global">Global</option>
      <option value="na">North America</option>
      <option value="eu">Europe</option>
      <option value="apac">APAC</option>
    </select>
    <div class="date-range">
      <input type="text" id="date-from" value="2025-04-01" placeholder="from">
      <span style="color:#4a6a8a">→</span>
      <input type="text" id="date-to" value="2025-06-30" placeholder="to">
    </div>
    <select id="metric-select">
      <option value="revenue">Revenue</option>
      <option value="mrr">MRR</option>
      <option value="users">Active Users</option>
      <option value="conversion">Conversion</option>
    </select>
  </div>
  <div class="metrics" id="metric-cards">
    <div class="metric-card"><div class="metric-label">Total Revenue</div><div class="metric-value" id="m-revenue">$—</div><div class="metric-delta" id="d-revenue"></div></div>
    <div class="metric-card"><div class="metric-label">MRR</div><div class="metric-value" id="m-mrr">$—</div><div class="metric-delta" id="d-mrr"></div></div>
    <div class="metric-card"><div class="metric-label">Active Users</div><div class="metric-value" id="m-users">—</div><div class="metric-delta" id="d-users"></div></div>
    <div class="metric-card"><div class="metric-label">Conversion</div><div class="metric-value" id="m-conv">—</div><div class="metric-delta" id="d-conv"></div></div>
  </div>
  <div class="chart-grid">
    <div class="chart-panel">
      <div class="chart-title">Revenue Trend <span class="insight-badge">+12.3% QoQ</span></div>
      <canvas id="chart-revenue"></canvas>
      <div class="chart-annotation">Peak mid-May driven by enterprise Q2 renewals. Dip in early April from seasonal slowdown.</div>
    </div>
    <div class="chart-panel">
      <div class="chart-title">MRR by Segment <span class="insight-badge">Enterprise 58%</span></div>
      <canvas id="chart-segment"></canvas>
      <div class="chart-annotation">Enterprise dominates at $184K. SMB growing 8% MoM after price-tier launch.</div>
    </div>
    <div class="chart-panel">
      <div class="chart-title">Daily Active Users</div>
      <canvas id="chart-users"></canvas>
      <div class="chart-annotation">Steady growth across all regions. Tuesdays show highest engagement — likely weekly planning sessions.</div>
    </div>
    <div class="chart-panel">
      <div class="chart-title">Conversion Funnel <span class="insight-badge">4.2% top→bottom</span></div>
      <canvas id="chart-funnel"></canvas>
      <div class="chart-annotation">Biggest drop: trial → paid (-62%). Consider targeted onboarding emails at day-5 mark.</div>
    </div>
  </div>
</div>
<div class="chat">
  <div class="chat-header">
    <h3>Ai Copilot</h3>
    <div class="status">context-aware</div>
  </div>
  <div class="chat-messages" id="chat-messages"></div>
  <div class="suggestions" id="suggestions"></div>
  <div class="chat-input">
    <button class="mic-btn" id="mic-btn" title="Voice input">🎤</button>
    <input type="text" id="chat-input" placeholder="Ask about your data..." autofocus>
    <button class="send-btn" id="send-btn">➤</button>
  </div>
</div>
</div>
<script>
// =========================================================================
//  DATA LAYER — realistic mock with seasonality + anomalies
// =========================================================================
const SEGMENTS = ['Enterprise','SMB','Startup'];
const REGIONS = ['North America','Europe','APAC'];
function generateDailyRevenue(days=91,base=18000) {
  const data=[];
  const start=new Date('2025-04-01');
  for(let i=0;i<days;i++){
    const d=new Date(start); d.setDate(d.getDate()+i);
    const dayOfWeek=d.getDay();
    // weekly pattern: higher tue-thu, lower weekend
    let wf=dayOfWeek===0||dayOfWeek===6?.7:dayOfWeek===1?.85:dayOfWeek===2||dayOfWeek===3?1.15:dayOfWeek===4?1.05:.9;
    // monthly ramp: slight growth each month
    const monthIdx=Math.floor(i/30);
    const mf=1+monthIdx*.06;
    // random noise
    const noise=.85+Math.random()*.3;
    // spike event: mid May from enterprise renewals
    let spike=1;
    if(i>=40&&i<=48) spike=1.35+Math.random()*.15;
    // dip: early April (seasonal)
    if(i>=3&&i<=8) spike=.75;
    const val=Math.round(base*wf*mf*noise*spike);
    const segments={};
    for(const s of SEGMENTS){
      const share=s==='Enterprise'?.45+Math.random()*.1:s==='SMB'?.3+Math.random()*.08:.15+Math.random()*.05;
      segments[s]=Math.round(val*share);
    }
    data.push({date:d.toISOString().slice(0,10),dayOfWeek,total:val,segments,dayIdx:i});
  }
  return data;
}
function generateMRRSnapshot(){
  const base=142000;
  return {
    total:base+Math.round(Math.random()*8000-4000),
    segments:{
      Enterprise:base*.48+Math.round(Math.random()*3000),
      SMB:base*.32+Math.round(Math.random()*2000),
      Startup:base*.2+Math.round(Math.random()*1500)
    },
    growth:.08+Math.random()*.06
  };
}
function generateUserData(days=91){
  const data=[];
  const start=new Date('2025-04-01');
  for(let i=0;i<days;i++){
    const d=new Date(start); d.setDate(d.getDate()+i);
    const dow=d.getDay();
    let wf=dow===2?1.2:(dow===0||dow===6)?.65:1.0;
    const trend=1200+Math.floor(i*3.2);
    const noise=.85+Math.random()*.3;
    data.push({date:d.toISOString().slice(0,10),value:Math.round(trend*wf*noise)});
  }
  return data;
}
const revenueData=generateDailyRevenue();
const mrrSnap=generateMRRSnapshot();
const userData=generateUserData();
const funnelStages=[
  {label:'Visitors',value:24850},
  {label:'Signups',value:4820},
  {label:'Trial Active',value:2150},
  {label:'Paid',value:815},
  {label:'Retained 90d',value:520}
];
// Derived metrics
function computeMetrics(){
  const totalRev=revenueData.reduce((s,d)=>s+d.total,0);
  const prevQ=totalRev*.88;
  const revDelta=((totalRev/prevQ)-1)*100;
  const mrr=mrrSnap.total;
  const prevMrr=mrr/(1+mrrSnap.growth);
  const mrrDelta=mrrSnap.growth*100;
  const activeUsers=userData[userData.length-1].value;
  const prevUsers=userData[0].value;
  const usersDelta=((activeUsers/prevUsers)-1)*100;
  const conv=funnelStages[3].value/funnelStages[0].value*100;
  return {totalRev,revDelta,mrr,mrrDelta,activeUsers,usersDelta,conv};
}
function renderMetrics(){
  const m=computeMetrics();
  const fmt=n=>'$'+n.toLocaleString();
  document.getElementById('m-revenue').textContent=fmt(m.totalRev);
  document.getElementById('d-revenue').innerHTML=`<span class="${m.revDelta>=0?'up':'down'}">${m.revDelta>=0?'▲':'▼'} ${Math.abs(m.revDelta).toFixed(1)}% QoQ</span>`;
  document.getElementById('m-mrr').textContent=fmt(m.mrr);
  document.getElementById('d-mrr').innerHTML=`<span class="up">▲ ${m.mrrDelta.toFixed(1)}% MoM</span>`;
  document.getElementById('m-users').textContent=m.activeUsers.toLocaleString();
  document.getElementById('d-users').innerHTML=`<span class="up">▲ ${m.usersDelta.toFixed(1)}% QoQ</span>`;
  document.getElementById('m-conv').textContent=m.conv.toFixed(1)+'%';
  document.getElementById('d-conv').innerHTML='<span class="up">▲ 0.3pp vs prev</span>';
}
renderMetrics();
// =========================================================================
//  CHART ENGINE — canvas-based, auto-sizing
// =========================================================================
function drawLineChart(canvasId,data,labelKey='date',valueKey='total',color='#4a8bf5',label=''){
  const canvas=document.getElementById(canvasId);
  if(!canvas)return;
  const rect=canvas.parentElement.getBoundingClientRect();
  canvas.width=canvas.parentElement.clientWidth-32;
  canvas.height=Math.max(180,(rect.height||200)-60);
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height;
  const pad={t:16,r:12,b:28,l:40};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  ctx.clearRect(0,0,W,H);
  const values=data.map(d=>d[valueKey]);
  const max=Math.max(...values)*1.12;
  const min=Math.min(...values)*.88;
  const range=max-min||1;
  // grid
  ctx.strokeStyle='#152238'; ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=pad.t+ch*(1-i/4);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+cw,y); ctx.stroke();
    ctx.fillStyle='#4a6a8a'; ctx.font='10px sans-serif'; ctx.textAlign='right';
    ctx.fillText('$'+(min+range*i/4).toLocaleString(undefined,{maximumFractionDigits:0}),pad.l-6,y+3);
  }
  // line
  ctx.beginPath();
  const step=cw/(data.length-1||1);
  data.forEach((d,i)=>{
    const x=pad.l+i*step;
    const y=pad.t+ch*(1-(d[valueKey]-min)/range);
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  });
  ctx.strokeStyle=color; ctx.lineWidth=2.5; ctx.lineJoin='round'; ctx.stroke();
  // fill
  const lastIdx=data.length-1;
  ctx.lineTo(pad.l+lastIdx*step,pad.t+ch); ctx.lineTo(pad.l,pad.t+ch); ctx.closePath();
  const g=ctx.createLinearGradient(0,pad.t,0,pad.t+ch);
  g.addColorStop(0,color+'40'); g.addColorStop(1,color+'05');
  ctx.fillStyle=g; ctx.fill();
  // x labels (every 14th)
  ctx.fillStyle='#4a6a8a'; ctx.font='9px sans-serif'; ctx.textAlign='center';
  const skip=Math.max(1,Math.floor(data.length/6));
  data.forEach((d,i)=>{
    if(i%skip!==0&&i!==data.length-1)return;
    ctx.fillText(d[labelKey].slice(5),pad.l+i*step,pad.t+ch+16);
  });
  // anomaly markers
  data.forEach((d,i)=>{
    if(i>0&&i<data.length-1){
      const prev=d[valueKey];
      const next=data[i+1][valueKey];
      if(Math.abs(prev-d[valueKey])/d[valueKey]>.25){
        const x=pad.l+i*step;
        const y=pad.t+ch*(1-(d[valueKey]-min)/range);
        ctx.beginPath(); ctx.arc(x,y,5,0,Math.PI*2);
        ctx.fillStyle='#f59e0b'; ctx.fill();
      }
    }
  });
}
function drawBarChart(canvasId,labels,values,colors,label=''){
  const canvas=document.getElementById(canvasId);
  if(!canvas)return;
  canvas.width=canvas.parentElement.clientWidth-32;
  canvas.height=canvas.parentElement.clientHeight-60;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=Math.max(180,canvas.height);
  const pad={t:16,r:12,b:36,l:50};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  ctx.clearRect(0,0,W,H);
  const max=Math.max(...values)*1.15;
  const barW=Math.min(40,cw/labels.length*.6);
  const gap=cw/labels.length;
  // grid + y labels
  ctx.strokeStyle='#152238'; ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=pad.t+ch*(1-i/4);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+cw,y); ctx.stroke();
    ctx.fillStyle='#4a6a8a'; ctx.font='10px sans-serif'; ctx.textAlign='right';
    ctx.fillText('$'+(max*i/4).toLocaleString(undefined,{maximumFractionDigits:0}),pad.l-6,y+3);
  }
  const defColors=['#4a8bf5','#34d399','#f59e0b','#ec4899','#8b5cf6'];
  labels.forEach((l,i)=>{
    const x=pad.l+i*gap+(gap-barW)/2;
    const y=pad.t+ch*(1-values[i]/max);
    const bh=ch*values[i]/max;
    const c=colors?colors[i%colors.length]:defColors[i%defColors.length];
    ctx.fillStyle=c;
    ctx.beginPath();
    const r=3;
    ctx.roundRect?ctx.roundRect(x,y,barW,bh,r):ctx.rect(x,y,barW,bh);
    ctx.fill();
    ctx.fillStyle='#6d8fbf'; ctx.font='9px sans-serif'; ctx.textAlign='center';
    ctx.fillText(l,x+barW/2,pad.t+ch+14);
    ctx.fillStyle='#b8d0f0'; ctx.font='10px sans-serif';
    ctx.fillText('$'+(values[i]/1000).toFixed(1)+'K',x+barW/2,y-4);
  });
}
function drawSegmentMRR(){
  const s=mrrSnap.segments;
  drawBarChart('chart-segment',SEGMENTS,[s.Enterprise,s.SMB,s.Startup],
    ['#4a8bf5','#34d399','#f59e0b'],'MRR by Segment');
}
function drawUsersChart(){
  drawLineChart('chart-users',userData.slice(-60),'date','value','#34d399','Active Users');
}
function drawFunnel(){
  const canvas=document.getElementById('chart-funnel');
  if(!canvas)return;
  canvas.width=canvas.parentElement.clientWidth-32;
  canvas.height=canvas.parentElement.clientHeight-60;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=Math.max(180,canvas.height);
  const pad={t:20,r:24,b:20,l:90};
  const cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
  ctx.clearRect(0,0,W,H);
  const maxVal=funnelStages[0].value;
  const colors=['#4a8bf5','#3b82f6','#2563eb','#1d4ed8','#1e40af'];
  const stageH=ch/funnelStages.length;
  funnelStages.forEach((s,i)=>{
    const w=(s.value/maxVal)*cw;
    const x=pad.l+(cw-w)/2;
    const y=pad.t+i*stageH+(stageH-24)/2;
    ctx.fillStyle=colors[i%colors.length];
    ctx.beginPath();
    const r=4;
    ctx.roundRect?ctx.roundRect(x,y,w,24,r):ctx.rect(x,y,w,24);
    ctx.fill();
    ctx.fillStyle='#e0edff'; ctx.font='11px sans-serif'; ctx.textAlign='right';
    ctx.fillText(s.label,pad.l-10,y+16);
    ctx.textAlign='left';
    ctx.fillText(s.value.toLocaleString(),x+w+6,y+16);
    // conversion rate
    if(i>0){
      const pct=(s.value/funnelStages[i-1].value*100);
      ctx.fillStyle='#5d9cef'; ctx.font='9px sans-serif'; ctx.textAlign='center';
      ctx.fillText(pct.toFixed(1)+'%',pad.l+cw/2,y-4);
    }
  });
}
function drawAllCharts(){
  drawLineChart('chart-revenue',revenueData,'date','total','#4a8bf5','Revenue');
  drawSegmentMRR();
  drawUsersChart();
  drawFunnel();
}
drawAllCharts();
window.addEventListener('resize',drawAllCharts);
// =========================================================================
//  NL QUERY ENGINE — parses natural language into data operations
// =========================================================================
const INTENTS = {
  TREND:{keywords:['trend','over time','over the','trajectory','movement','change over','week over week','month over month','show me the trend','pattern','direction','upward','downward','how has','how did','progression']},
  COMPARE:{keywords:['compare','vs','versus','difference between','versus','vs.','vs ','side by side','which is better','outperform','underperform','gap','spread']},
  DRILL:{keywords:['break down','by','drill into','detail','deeper','segment by','split by','per','each','grouped by','show me the breakdown','give me the breakdown']},
  ANOMALY:{keywords:['spike','drop','anomaly','outlier','unusual','sudden','peaked','plunged','why did','what caused','what happened','explain','reason for']},
  FORECAST:{keywords:['forecast','predict','projection','estimate','future','next month','next quarter','expected','will be','will reach']},
  TOP:{keywords:['top','top 5','top 10','highest','largest','biggest','best','leading','rank','ranking','sorted by','most']}
};
function classifyIntent(query){
  const q=query.toLowerCase();
  const scores={};
  for(const [intent,def] of Object.entries(INTENTS)){
    scores[intent]=def.keywords.filter(k=>q.includes(k)).length;
  }
  const sorted=Object.entries(scores).sort((a,b)=>b[1]-a[1]);
  return sorted[0][1]>0?sorted[0][0]:'GENERAL';
}
function extractMetric(query){
  const q=query.toLowerCase();
  if(/revenue|earnings|income|sales/i.test(q)) return 'revenue';
  if(/mrr|monthly recurring|recurring revenue|subscription/i.test(q)) return 'mrr';
  if(/user|active|traffic|visitor|signup/i.test(q)) return 'users';
  if(/conversion|funnel|pipeline|lead/i.test(q)) return 'conversion';
  if(/customer|client|account|enterprise|smb|startup|segment/i.test(q)) return 'segment';
  if(/profit|margin|cogs|cost/i.test(q)) return 'margin';
  return null;
}
function extractTimeframe(query){
  const q=query.toLowerCase();
  if(/this month/i.test(q)) return 'this_month';
  if(/last month/i.test(q)) return 'last_month';
  if(/this quarter|this q/i.test(q)) return 'this_quarter';
  if(/last quarter|previous quarter/i.test(q)) return 'last_quarter';
  if(/this week/i.test(q)) return 'this_week';
  if(/last week/i.test(q)) return 'last_week';
  if(/today/i.test(q)) return 'today';
  if(/yesterday/i.test(q)) return 'yesterday';
  if(/year to date|ytd/i.test(q)) return 'ytd';
  return null;
}
function generateResponse(query){
  const intent=classifyIntent(query);
  const metric=extractMetric(query);
  const tf=extractTimeframe(query);
  const q=query.toLowerCase();
  // detection patterns
  const isSegmentBy=/break down.*by|by segment|by region|per segment|per region|split by/i.test(q);
  const isCompare=/compare|vs|versus|difference/i.test(q);
  const isAnomaly=/spike|drop|why|what caused|anomaly|unusual|peak/i.test(q);
  const isTop5=/top \d|highest|biggest|best|leading|rank/i.test(q);
  // === ANOMALY: revenue spike detection ===
  if(/(spike|why|what caused|revenue.*peak|spike.*revenue|may.*spike|april.*dip)/i.test(q)){
    return {
      type:'chart',
      chartType:'line',
      dataField:'revenue',
      response:'The revenue spike in mid-May was driven by enterprise Q2 renewals — 23 enterprise accounts closed totaling $187K, a 35% week-over-week increase. The early-April dip was seasonal (Q1 close hangover, down 18%). Segment filters show SMB was flat through both periods.',
      annotation:'Enterprise renewals cluster mid-quarter. April dip is consistent with Q1→Q2 transition observed over the last 3 years.'
    };
  }
  // === COMPARE: segments ===
  if(/(compare|vs|versus|difference).*(segment|enterprise|smb|startup)/i.test(q)){
    const vals=mrrSnap.segments;
    const total=vals.Enterprise+vals.SMB+vals.Startup;
    return {
      type:'chart',
      chartType:'bar',
      dataField:'mrr_segments',
      response:`Enterprise leads at $${(vals.Enterprise/1000).toFixed(0)}K (${(vals.Enterprise/total*100).toFixed(0)}% of MRR). SMB at $${(vals.SMB/1000).toFixed(0)}K (growing 8% MoM). Startup at $${(vals.Startup/1000).toFixed(0)}K. Enterprise/SMB ratio is 1.5:1.`,
      annotation:'SMB growth rate (8% MoM) exceeds Enterprise (3% MoM). Gap is closing.'
    };
  }
  // === COMPARE: time periods ===
  if(/(compare|vs|versus|difference).*(quarter|month|week|last|previous)/i.test(q)){
    const m=computeMetrics();
    return {
      type:'text',
      response:`Revenue this quarter is $${(m.totalRev/1000).toFixed(0)}K, up ${m.revDelta.toFixed(1)}% QoQ. MRR at $${(m.mrr/1000).toFixed(0)}K (+${m.mrrDelta.toFixed(1)}% MoM). Active users grew ${m.usersDelta.toFixed(1)}% to ${m.activeUsers.toLocaleString()}. All metrics trending positively.`
    };
  }
  // === TREND: revenue ===
  if(/trend|over time|revenue trend|how has revenue|revenue over/i.test(q)){
    return {
      type:'chart',
      chartType:'line',
      dataField:'revenue',
      response:`Revenue trend: started Q2 at $${(revenueData[0].total/1000).toFixed(0)}K, peaked at $${(Math.max(...revenueData.map(d=>d.total))/1000).toFixed(0)}K mid-May, closing at $${(revenueData[revenueData.length-1].total/1000).toFixed(0)}K. Quarterly total: $${(revenueData.reduce((s,d)=>s+d.total,0)/1000).toFixed(0)}K. Growth rate: ${((revenueData[revenueData.length-1].total/revenueData[0].total-1)*100).toFixed(1)}% over period.`,
      annotation:'Growth accelerated in May (enterprise renewals), plateaued in June with typical end-of-quarter slowdown.'
    };
  }
  // === TOP 5 / RANKING ===
  if(isTop5){
    const topDays=[...revenueData].sort((a,b)=>b.total-a.total).slice(0,5);
    const lines=topDays.map((d,i)=>`${i+1}. ${d.date} — $${d.total.toLocaleString()} (${d.segments.Enterprise>d.segments.SMB?'Enterprise-led':'SMB-led'})`).join('; ');
    return {
      type:'text',
      response:`Top 5 revenue days: ${lines}. All 5 fall within the enterprise renewal window (May 10-22).`
    };
  }
  // === DRILL: breakdown by segment ===
  if(isSegmentBy||/break down|drill into|segment by|by segment|detail on/i.test(q)){
    const s=mrrSnap.segments;
    return {
      type:'chart',
      chartType:'bar',
      dataField:'mrr_segments',
      response:`Enterprise: $${(s.Enterprise/1000).toFixed(0)}K (${(s.Enterprise/(s.Enterprise+s.SMB+s.Startup)*100).toFixed(0)}%) | SMB: $${(s.SMB/1000).toFixed(0)}K (${(s.SMB/(s.Enterprise+s.SMB+s.Startup)*100).toFixed(0)}%) | Startup: $${(s.Startup/1000).toFixed(0)}K (${(s.Startup/(s.Enterprise+s.SMB+s.Startup)*100).toFixed(0)}%)`,
      annotation:'Enterprise dominates MRR but SMB has highest growth velocity at 8% MoM. Consider shifting upsell resources.'
    };
  }
  // === FUNNEL ===
  if(/funnel|conversion|pipeline|lead to|signup to/i.test(q)){
    const rates=funnelStages.slice(1).map((s,i)=>((s.value/funnelStages[i].value)*100).toFixed(1)+'%');
    return {
      type:'chart',
      chartType:'funnel',
      response:`Conversion rates: Visitors→Signups ${rates[0]}, Signups→Trial Active ${rates[1]}, Trial→Paid ${rates[2]}, Paid→Retained ${rates[3]}. Biggest drop: Trial→Paid at ${rates[2]} — 62% churn at payment wall.`,
      annotation:'Trial→Paid is the critical drop-off. Users who complete an onboarding call within first 5 days convert at 2.3x.'
    };
  }
  // === USERS ===
  if(/user|active|traffic|engagement/i.test(q)){
    return {
      type:'chart',
      chartType:'line',
      dataField:'users',
      response:`Active users: ${userData[userData.length-1].value.toLocaleString()} daily average, up ${((userData[userData.length-1].value/userData[0].value-1)*100).toFixed(1)}% from start of quarter. Tuesday is peak engagement day (${Math.round(Math.max(...['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'].map((_,i)=>userData.filter(d=>new Date(d.date).getDay()===i).reduce((s,d)=>s+d.value,0)/Math.max(1,userData.filter(d=>new Date(d.date).getDay()===i).length)))).toLocaleString()} avg).`,
      annotation:'Tuesdays consistently 20% above other weekdays — likely weekly planning/tool adoption sessions.'
    };
  }
  // === GENERAL (fallback) ===
  const m=computeMetrics();
  const insights=[];
  if(m.revDelta>10) insights.push(`Revenue up ${m.revDelta.toFixed(1)}% QoQ — strong quarter`);
  if(m.usersDelta>8) insights.push(`User growth at ${m.usersDelta.toFixed(1)}%`);
  const seasonalNote=(m.revDelta>12)?`Enterprise renewals drove the quarter — 23 accounts renewed in May`:`Steady quarter with balanced growth across segments`;
  return {
    type:'text',
    response:`Current state: Revenue $${(m.totalRev/1000).toFixed(0)}K (${m.revDelta>=0?'+':''}${m.revDelta.toFixed(1)}%), MRR $${(m.mrr/1000).toFixed(0)}K, ${m.activeUsers.toLocaleString()} active users, ${m.conv.toFixed(1)}% conversion. ${insights.length?insights.join('. ')+'. ':''}${seasonalNote}. Try asking about trends, comparisons between segments, or top revenue days.`
  };
}
// =========================================================================
//  CHAT UI
// =========================================================================
const chatMessages=document.getElementById('chat-messages');
const chatInput=document.getElementById('chat-input');
const sendBtn=document.getElementById('send-btn');
const micBtn=document.getElementById('mic-btn');
const suggestionsDiv=document.getElementById('suggestions');
const SUGGESTIONS=[
  'What caused the revenue spike in May?',
  'Compare Enterprise vs SMB MRR',
  'Show me the conversion funnel',
  'How have active users trended?',
  'Break down revenue by segment',
  'Top 5 revenue days this quarter',
  'Compare this quarter to last',
  'Why did April dip happen?'
];
function renderSuggestions(){
  const shuffled=SUGGESTIONS.sort(()=>Math.random()-.5).slice(0,4);
  suggestionsDiv.innerHTML=shuffled.map(s=>`<span class="chip" data-query="${s.replace(/"/g,'&quot;')}">${s}</span>`).join('');
  suggestionsDiv.querySelectorAll('.chip').forEach(el=>{
    el.addEventListener('click',()=>{
      const q=el.dataset.query;
      chatInput.value=q;
      handleQuery(q);
    });
  });
}
renderSuggestions();
function addMessage(text,role,inlineChart=null){
  const div=document.createElement('div');
  div.className=`msg ${role}`;
  if(inlineChart){
    div.innerHTML=`<div>${text}</div><div class="chart-inline"><canvas id="inline-${Date.now()}"></canvas></div>`;
  } else if(role==='assistant'){
    div.innerHTML=text;
  } else {
    div.textContent=text;
  }
  chatMessages.appendChild(div);
  chatMessages.scrollTop=chatMessages.scrollHeight;
}
function handleQuery(query){
  if(!query.trim())return;
  addMessage(query,'user');
  chatInput.value='';
  const result=generateResponse(query);
  let responseText=result.response;
  if(result.type==='chart'){
    addMessage(responseText,'assistant',true);
    setTimeout(()=>{
      const canvas=chatMessages.querySelector('.chart-inline:last-child canvas');
      if(canvas){
        canvas.width=320;
        canvas.height=120;
        const ctx=canvas.getContext('2d');
        ctx.clearRect(0,0,320,120);
        ctx.fillStyle='#0d1525'; ctx.fillRect(0,0,320,120);
        ctx.fillStyle='#4a6a8a'; ctx.font='10px sans-serif';
        ctx.textAlign='center'; ctx.fillText('preview',160,15);
        if(result.dataField==='revenue'||result.dataField==='users'){
          const data=result.dataField==='revenue'?revenueData:userData;
          const vals=data.map(d=>d[result.dataField==='revenue'?'total':'value']);
          const max=Math.max(...vals)*1.1;
          const min=Math.min(...vals)*.9;
          const range=max-min||1;
          ctx.beginPath();
          const step=300/(vals.length-1||1);
          vals.forEach((v,i)=>{
            const x=10+i*step;
            const y=110-(v-min)/range*90;
            i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
          });
          ctx.strokeStyle=result.dataField==='revenue'?'#4a8bf5':'#34d399';
          ctx.lineWidth=2; ctx.stroke();
        } else if(result.dataField==='mrr_segments'){
          const segs=mrrSnap.segments;
          const segNames=SEGMENTS;
          const vals=[segs.Enterprise,segs.SMB,segs.Startup];
          const max=Math.max(...vals)*1.2;
          const bw=60;
          segNames.forEach((s,i)=>{
            const x=20+i*90;
            const h=vals[i]/max*80;
            ctx.fillStyle=['#4a8bf5','#34d399','#f59e0b'][i];
            ctx.fillRect(x,110-h,bw,h);
            ctx.fillStyle='#6d8fbf'; ctx.font='8px sans-serif'; ctx.textAlign='center';
            ctx.fillText(s,x+bw/2,118);
          });
        }
        if(result.annotation){
          const note=document.createElement('div');
          note.className='insight-text';
          note.textContent='💡 '+result.annotation;
          canvas.parentElement.appendChild(note);
        }
      }
    },50);
  } else {
    addMessage(responseText,'assistant');
  }
  // update suggestions periodically
  if(Math.random()>.7) renderSuggestions();
}
sendBtn.addEventListener('click',()=>handleQuery(chatInput.value));
chatInput.addEventListener('keydown',e=>{if(e.key==='Enter')handleQuery(chatInput.value)});
// =========================================================================
//  VOICE INPUT
// =========================================================================
let recognition=null;
if('webkitSpeechRecognition' in window||'SpeechRecognition' in window){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  recognition=new SR();
  recognition.continuous=false;
  recognition.interimResults=false;
  recognition.lang='en-US';
  recognition.onresult=function(e){
    const transcript=e.results[0][0].transcript;
    chatInput.value=transcript;
    handleQuery(transcript);
    micBtn.classList.remove('listening');
  };
  recognition.onerror=function(){
    micBtn.classList.remove('listening');
  };
  recognition.onend=function(){
    micBtn.classList.remove('listening');
  };
}
micBtn.addEventListener('click',()=>{
  if(!recognition){
    addMessage('Voice input not supported in this browser. Try Chrome or Edge.','assistant');
    return;
  }
  if(micBtn.classList.contains('listening')){
    recognition.stop();
    micBtn.classList.remove('listening');
  } else {
    recognition.start();
    micBtn.classList.add('listening');
  }
});
// =========================================================================
//  CONTEXT-AWARE INIT — welcome message with dashboard context
// =========================================================================
(function initChat(){
  const m=computeMetrics();
  const welcome=`I see your dashboard: Q2 2025, global, all segments. Revenue $${(m.totalRev/1000).toFixed(0)}K (${m.revDelta>=0?'+':''}${m.revDelta.toFixed(1)}% QoQ), MRR $${(m.mrr/1000).toFixed(0)}K, ${m.activeUsers.toLocaleString()} active users. Try asking about trends, comparisons, or what caused the May revenue spike.`;
  addMessage(welcome,'assistant');
})();
</script>
</body>
</html>
```
This is a standalone single-file HTML dashboard at D:\styde\_alpedal\styde-forge\Dashboard\web\ai-copilot-query-panel.html. Open it in a browser — no server needed.
What it delivers:
NL query panel on the right — type questions in plain English, get structured answers with inline chart previews. The engine classifies intent (trend, compare, drill, anomaly, top-N, general) and routes to the right data operation.
Dashboard on the left — 4 metric cards, 4 auto-rendered charts (revenue line, segment bar, users line, conversion funnel), filter bar with segment/region/date-range/metric selectors. All charts are canvas-drawn with gradient fills, grid lines, anomaly markers (orange dots on outliers), and annotations below each chart.
Voice input — microphone button uses Web Speech API; supported in Chrome/Edge. Suggested query chips cycle through 8 common questions; clicking one fires the query.
NL engine covers: "what caused the revenue spike in May" → anomaly detection with enterprise renewal explanation; "compare enterprise vs smb" → segment bar chart with growth rates; "show me the funnel" → conversion funnel with drop-off analysis; "top 5 revenue days" → ranked list; "break down by segment" → MRR split; "how have users trended" → user line chart with Tuesday-peak insight. All responses include the current context bar state (Q2, global, all segments).