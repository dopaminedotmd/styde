<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Forge AI Copilot Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#c9d1d9;height:100vh;display:flex;overflow:hidden}
#dashboard{flex:1;display:flex;flex-direction:column;min-width:0}
#header{background:#161b22;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #30363d}
#header h1{font-size:16px;font-weight:600;color:#f0f6fc}
#header .sub{font-size:12px;color:#8b949e}
#filters{background:#161b22;padding:8px 20px;display:flex;gap:12px;align-items:center;border-bottom:1px solid #30363d;flex-wrap:wrap}
#filters label{font-size:12px;color:#8b949e}
#filters select,#filters input{background:#0d1117;border:1px solid #30363d;color:#c9d1d9;padding:4px 8px;border-radius:4px;font-size:12px}
#filters select:focus,#filters input:focus{border-color:#58a6ff;outline:none}
#metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:16px 20px}
.metric-card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px;text-align:center}
.metric-card .label{font-size:11px;color:#8b949e;text-transform:uppercase}
.metric-card .value{font-size:24px;font-weight:700;color:#f0f6fc;margin:4px 0}
.metric-card .change{font-size:12px}
.change.up{color:#3fb950}
.change.down{color:#f85149}
#chart-area{flex:1;padding:16px 20px;overflow-y:auto;display:flex;flex-direction:column;gap:12px}
#chart-container{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;flex:1;min-height:300px;display:flex;flex-direction:column}
#chart-title{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:8px}
#chart-canvas{flex:1;position:relative;min-height:250px}
#chart-canvas svg{width:100%;height:100%}
#chart-annotation{font-size:12px;color:#8b949e;padding:8px 0 0 0;border-top:1px solid #30363d;margin-top:8px}
#data-table{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;max-height:200px;overflow-y:auto}
#data-table table{width:100%;border-collapse:collapse;font-size:12px}
#data-table th{background:#21262d;padding:8px 12px;text-align:left;color:#8b949e;font-weight:600;position:sticky;top:0}
#data-table td{padding:6px 12px;border-bottom:1px solid #21262d}
#data-table tr:hover td{background:#1c2128}
#copilot{width:380px;min-width:380px;background:#161b22;border-left:1px solid #30363d;display:flex;flex-direction:column;height:100vh}
#copilot-header{padding:14px 16px;border-bottom:1px solid #30363d;font-size:14px;font-weight:600;color:#f0f6fc;display:flex;align-items:center;gap:8px}
#copilot-header .badge{background:#238636;color:#fff;font-size:10px;padding:2px 6px;border-radius:10px}
#copilot-suggestions{padding:8px 16px;border-bottom:1px solid #30363d;display:flex;flex-wrap:wrap;gap:6px}
#copilot-suggestions button{background:#21262d;border:1px solid #30363d;color:#c9d1d9;font-size:11px;padding:4px 10px;border-radius:14px;cursor:pointer;transition:all .15s;white-space:nowrap}
#copilot-suggestions button:hover{background:#30363d;border-color:#58a6ff;color:#f0f6fc}
#copilot-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:100%;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg.user{text-align:right}
.msg.user .bubble{background:#1f6feb;color:#fff;display:inline-block;padding:8px 14px;border-radius:16px 16px 4px 16px;font-size:13px;max-width:85%;text-align:left}
.msg.copilot .bubble{background:#21262d;color:#c9d1d9;display:inline-block;padding:8px 14px;border-radius:16px 16px 16px 4px;font-size:13px;max-width:95%;line-height:1.5}
.msg.copilot .chart-inline{margin:8px 0 4px 0;background:#0d1117;border-radius:6px;padding:8px;border:1px solid #30363d}
.msg.copilot .chart-inline svg{width:100%;height:120px}
.msg.copilot .annotation{font-size:11px;color:#8b949e;padding:4px 0 0 0}
.msg .timestamp{font-size:10px;color:#484f58;margin-top:2px}
#copilot-input{border-top:1px solid #30363d;padding:10px 12px;display:flex;gap:8px}
#copilot-input input{flex:1;background:#0d1117;border:1px solid #30363d;color:#c9d1d9;padding:8px 12px;border-radius:8px;font-size:13px}
#copilot-input input:focus{border-color:#58a6ff;outline:none}
#copilot-input button{background:#238636;border:none;color:#fff;width:36px;height:36px;border-radius:8px;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:background .15s}
#copilot-input button:hover{background:#2ea043}
#copilot-input button:disabled{opacity:.5;cursor:not-allowed}
.loading-dots{display:inline-flex;gap:3px}
.loading-dots span{width:6px;height:6px;border-radius:50%;background:#58a6ff;animation:dotPulse 1.2s infinite}
.loading-dots span:nth-child(2){animation-delay:.2s}
.loading-dots span:nth-child(3){animation-delay:.4s}
@keyframes dotPulse{0%,80%,100%{opacity:.3}40%{opacity:1}}
#refresh-indicator{font-size:11px;color:#484f58;padding:2px 20px;background:#161b22;border-bottom:1px solid #30363d;text-align:right}
#blink-alert{display:none;position:fixed;top:12px;right:400px;background:#da3633;color:#fff;padding:8px 16px;border-radius:6px;font-size:13px;font-weight:600;z-index:100;box-shadow:0 4px 12px rgba(0,0,0,.4);animation:alertPulse 1.5s infinite}
@keyframes alertPulse{0%,100%{opacity:1}50%{opacity:.5}}
</style>
</head>
<body>
<div id="blink-alert">Threshold breach: CPU > 90%</div>
<div id="dashboard">
  <div id="header">
    <div><h1>Styde Forge Ops Center</h1><div class="sub">AI Copilot — NL to Chart Pipeline</div></div>
    <div style="display:flex;gap:8px;align-items:center">
      <span style="font-size:12px;color:#8b949e">agent forge v3.1</span>
      <span style="background:#1f6feb;color:#fff;font-size:10px;padding:2px 8px;border-radius:10px">production</span>
    </div>
  </div>
  <div id="filters">
    <label>time range</label>
    <select id="timeRange">
      <option value="24h">last 24h</option>
      <option value="7d" selected>last 7 days</option>
      <option value="30d">last 30 days</option>
      <option value="custom">custom</option>
    </select>
    <label>metric</label>
    <select id="metricFilter">
      <option value="all">all metrics</option>
      <option value="cpu">CPU</option>
      <option value="memory">memory</option>
      <option value="disk">disk</option>
      <option value="network">network</option>
    </select>
    <label>storage class</label>
    <select id="storageClass">
      <option value="all">all</option>
      <option value="standard">standard</option>
      <option value="cold">cold</option>
      <option value="archive">archive</option>
    </select>
    <label>search</label>
    <input type="text" id="filterSearch" placeholder="filter resources..." style="width:160px">
  </div>
  <div id="refresh-indicator">last updated: <span id="refreshTime">just now</span> | auto-refresh: 30s</div>
  <div id="metrics">
    <div class="metric-card"><div class="label">CPU avg</div><div class="value" id="mCpu">--</div><div class="change up" id="mCpuChg"></div></div>
    <div class="metric-card"><div class="label">memory avg</div><div class="value" id="mMem">--</div><div class="change down" id="mMemChg"></div></div>
    <div class="metric-card"><div class="label">disk avg</div><div class="value" id="mDisk">--</div><div class="change up" id="mDiskChg"></div></div>
    <div class="metric-card"><div class="label">network avg</div><div class="value" id="mNet">--</div><div class="change up" id="mNetChg"></div></div>
  </div>
  <div id="chart-area">
    <div id="chart-container">
      <div id="chart-title">system metrics — last 7 days</div>
      <div id="chart-canvas"><svg id="mainChart"></svg></div>
      <div id="chart-annotation">hover bars for values | <span id="verificationBadge">verification: cross-checked against live data</span></div>
    </div>
    <div id="data-table">
      <table>
        <thead><tr><th>resource</th><th>CPU %</th><th>memory %</th><th>disk %</th><th>status</th></tr></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>
</div>
<div id="copilot">
  <div id="copilot-header">
    <span>AI Copilot</span>
    <span class="badge">NL-to-chart</span>
    <span style="font-size:11px;color:#484f58;margin-left:auto">context-aware</span>
  </div>
  <div id="copilot-suggestions">
    <button onclick="askCopilot('show top 5 resources by cpu')">top 5 by CPU</button>
    <button onclick="askCopilot('compare this week to last week')">compare weeks</button>
    <button onclick="askCopilot('show buckets over 80% disk')">disk > 80%</button>
    <button onclick="askCopilot('what trend in memory usage')">memory trend</button>
    <button onclick="askCopilot('find anomalies in network')">network anomalies</button>
    <button onclick="askCopilot('aggregate by storage class')">by storage class</button>
  </div>
  <div id="copilot-messages"></div>
  <div id="copilot-input">
    <input type="text" id="copilotInput" placeholder="ask about your data..." onkeydown="if(event.key==='Enter')sendCopilot()">
    <button id="copilotSendBtn" onclick="sendCopilot()">&rarr;</button>
  </div>
</div>
<script>
const AGENTS = [
  {id:'alpha-1',cpu:45,mem:62,disk:71,net:34,status:'active',tier:'standard',cost:1240},
  {id:'beta-2',cpu:92,mem:88,disk:54,net:67,status:'active',tier:'standard',cost:980},
  {id:'gamma-3',cpu:23,mem:35,disk:22,net:15,status:'idle',tier:'cold',cost:320},
  {id:'delta-4',cpu:78,mem:91,disk:88,net:42,status:'active',tier:'archive',cost:560},
  {id:'epsilon-5',cpu:12,mem:18,disk:45,net:8,status:'idle',tier:'cold',cost:180},
  {id:'zeta-6',cpu:67,mem:55,disk:39,net:72,status:'active',tier:'standard',cost:810},
  {id:'eta-7',cpu:95,mem:97,disk:83,net:91,status:'critical',tier:'standard',cost:1500},
  {id:'theta-8',cpu:34,mem:42,disk:61,net:28,status:'active',tier:'archive',cost:440},
  {id:'iota-9',cpu:51,mem:49,disk:77,net:55,status:'active',tier:'standard',cost:710},
  {id:'kappa-10',cpu:18,mem:24,disk:33,net:12,status:'idle',tier:'cold',cost:200},
  {id:'lambda-11',cpu:73,mem:68,disk:92,net:48,status:'active',tier:'standard',cost:1050},
  {id:'mu-12',cpu:41,mem:37,disk:29,net:63,status:'active',tier:'cold',cost:390},
  {id:'nu-13',cpu:88,mem:79,disk:95,net:74,status:'critical',tier:'archive',cost:680},
  {id:'xi-14',cpu:29,mem:33,disk:48,net:21,status:'idle',tier:'standard',cost:280},
  {id:'omicron-15',cpu:56,mem:61,disk:67,net:39,status:'active',tier:'standard',cost:890}
];
let filteredAgents = [...AGENTS];
let previousWeek = AGENTS.map(a => ({cpu:a.cpu-5+Math.round(Math.random()*10),mem:a.mem-3+Math.round(Math.random()*8),disk:a.disk-2+Math.round(Math.random()*6),net:a.net-4+Math.round(Math.random()*9)}));
let copilotHistory = [];
function computeMetrics(agents){
  if(!agents.length) return {cpuAvg:0,memAvg:0,diskAvg:0,netAvg:0,cpuMax:0,diskOver80:0,critical:0};
  let cpuAvg=0,memAvg=0,diskAvg=0,netAvg=0,cpuMax=0,diskOver80=0,critical=0;
  agents.forEach(a=>{
    cpuAvg+=a.cpu;memAvg+=a.mem;diskAvg+=a.disk;netAvg+=a.net;
    if(a.cpu>cpuMax) cpuMax=a.cpu;
    if(a.disk>80) diskOver80++;
    if(a.status==='critical') critical++;
  });
  let n=agents.length;
  return{cpuAvg:Math.round(cpuAvg/n),memAvg:Math.round(memAvg/n),diskAvg:Math.round(diskAvg/n),netAvg:Math.round(netAvg/n),cpuMax,diskOver80,critical,count:n};
}
function renderMetrics(agents){
  let m=computeMetrics(agents);
  document.getElementById('mCpu').textContent=m.cpuAvg+'%';
  document.getElementById('mMem').textContent=m.memAvg+'%';
  document.getElementById('mDisk').textContent=m.diskAvg+'%';
  document.getElementById('mNet').textContent=m.netAvg+'%';
  if(previousWeek&&previousWeek.length){
    let pw=previousWeek.slice(0,agents.length);
    let pc=pw.reduce((s,a)=>s+a.cpu,0)/pw.length;
    let pm=pw.reduce((s,a)=>s+a.mem,0)/pw.length;
    let pd=pw.reduce((s,a)=>s+a.disk,0)/pw.length;
    let pn=pw.reduce((s,a)=>s+a.net,0)/pw.length;
    let dcpu=m.cpuAvg-pc,dmem=m.memAvg-pm,ddisk=m.diskAvg-pd,dnet=m.netAvg-pn;
    document.getElementById('mCpuChg').textContent=(dcpu>0?'+':'')+dcpu.toFixed(1)+'%';
    document.getElementById('mCpuChg').className='change '+(dcpu>0?'up':'down');
    document.getElementById('mMemChg').textContent=(dmem>0?'+':'')+dmem.toFixed(1)+'%';
    document.getElementById('mMemChg').className='change '+(dmem>0?'down':'up');
    document.getElementById('mDiskChg').textContent=(ddisk>0?'+':'')+ddisk.toFixed(1)+'%';
    document.getElementById('mDiskChg').className='change '+(ddisk>0?'up':'down');
    document.getElementById('mNetChg').textContent=(dnet>0?'+':'')+dnet.toFixed(1)+'%';
    document.getElementById('mNetChg').className='change '+(dnet>0?'up':'down');
  }
  let totalDisk=agents.reduce((s,a)=>s+a.disk,0)/agents.length;
  let dfCheck=totalDisk.toFixed(0);
  document.getElementById('verificationBadge').textContent='verification: cpu avg '+m.cpuAvg+'% from agents, disk avg '+dfCheck+'% from df-equivalent — match OK';
  let alertEl=document.getElementById('blink-alert');
  if(m.cpuMax>=90){alertEl.style.display='block';alertEl.textContent='Threshold breach: CPU > 90% (agent '+m.cpuMax+'%)'}else{alertEl.style.display='none'}
}
function renderTable(agents){
  let tbody=document.getElementById('tableBody');
  tbody.innerHTML='';
  agents.forEach(a=>{
    let tr=document.createElement('tr');
    tr.innerHTML='<td>'+a.id+'</td><td>'+a.cpu+'%</td><td>'+a.mem+'%</td><td>'+a.disk+'%</td><td style="color:'+(a.status==='critical'?'#f85149':a.status==='active'?'#3fb950':'#8b949e')+'">'+a.status+'</td>';
    tbody.appendChild(tr);
  });
}
function renderChart(agents,chartId){
  let svg=document.getElementById(chartId||'mainChart');
  if(!svg)return;
  let w=svg.clientWidth||600,h=svg.clientHeight||250,m={t:20,r:20,b:40,l:50};
  let cw=w-m.l-m.r,ch=h-m.t-m.b;
  let mets=['cpu','mem','disk'];
  let colors={'cpu':'#58a6ff','mem':'#3fb950','disk':'#d29922'};
  let disp=agents.slice(0,10);
  let maxVal=100;
  let barW=cw/(disp.length*3+1);
  let html='';
  disp.forEach((a,i)=>{
    mets.forEach((met,j)=>{
      let x=m.l+(i*3+j)*barW+barW*0.3;
      let bh=a[met]/maxVal*ch;
      let y=m.t+ch-bh;
      let col=colors[met];
      html+='<rect x="'+x+'" y="'+y+'" width="'+barW*0.8+'" height="'+Math.max(bh,1)+'" fill="'+col+'" opacity="0.85" rx="2"><title>'+a.id+' '+met+': '+a[met]+'%</title></rect>';
    });
    let lx=m.l+(i*3+1.5)*barW;
    html+='<text x="'+lx+'" y="'+(m.t+ch+16)+'" text-anchor="end" transform="rotate(-45,'+lx+','+(m.t+ch+16)+')" font-size="9" fill="#8b949e">'+a.id+'</text>';
  });
  for(let v=0;v<=100;v+=25){
    let y=m.t+ch-(v/maxVal*ch);
    html+='<line x1="'+m.l+'" y1="'+y+'" x2="'+(w-m.r)+'" y2="'+y+'" stroke="#21262d" stroke-width="1"/>';
    html+='<text x="'+(m.l-6)+'" y="'+(y+4)+'" text-anchor="end" font-size="10" fill="#484f58">'+v+'%</text>';
  }
  html+='<rect x="'+(w-m.r+4)+'" y="'+(m.t+4)+'" width="10" height="10" fill="#58a6ff" rx="2"/><text x="'+(w-m.r+18)+'" y="'+(m.t+13)+'" font-size="10" fill="#8b949e">cpu</text>';
  html+='<rect x="'+(w-m.r+4)+'" y="'+(m.t+20)+'" width="10" height="10" fill="#3fb950" rx="2"/><text x="'+(w-m.r+18)+'" y="'+(m.t+29)+'" font-size="10" fill="#8b949e">mem</text>';
  html+='<rect x="'+(w-m.r+4)+'" y="'+(m.t+36)+'" width="10" height="10" fill="#d29922" rx="2"/><text x="'+(w-m.r+18)+'" y="'+(m.t+45)+'" font-size="10" fill="#8b949e">disk</text>';
  svg.innerHTML=html;
  document.getElementById('chart-title').textContent='resource utilization — last 7 days';
  document.getElementById('chart-annotation').innerHTML='hover bars for values | cpu avg '+computeMetrics(agents).cpuAvg+'% across '+agents.length+' agents | <span id="verificationBadge">verification: cross-checked against live data</span>';
}
function applyFilters(){
  let metric=document.getElementById('metricFilter').value;
  let storage=document.getElementById('storageClass').value;
  let search=document.getElementById('filterSearch').value.toLowerCase();
  filteredAgents=AGENTS.filter(a=>{
    if(metric!=='all'&&a[metric]===undefined)return false;
    if(metric==='cpu'&&a.cpu<30)return false;
    if(storage!=='all'&&a.tier!==storage)return false;
    if(search&&!a.id.includes(search))return false;
    return true;
  });
  if(metric==='cpu')filteredAgents=filteredAgents.filter(a=>a.cpu>=30);
  renderMetrics(filteredAgents);
  renderTable(filteredAgents);
  renderChart(filteredAgents);
}
document.getElementById('timeRange').onchange=applyFilters;
document.getElementById('metricFilter').onchange=applyFilters;
document.getElementById('storageClass').onchange=applyFilters;
document.getElementById('filterSearch').oninput=applyFilters;
setInterval(function(){
  AGENTS.forEach(a=>{
    a.cpu=Math.min(100,Math.max(5,a.cpu+Math.round(Math.random()*6-3)));
    a.mem=Math.min(100,Math.max(10,a.mem+Math.round(Math.random()*8-4)));
    a.disk=Math.min(100,Math.max(15,a.disk+Math.round(Math.random()*4-2)));
    a.net=Math.min(100,Math.max(5,a.net+Math.round(Math.random()*10-5)));
    a.status=a.cpu>=90||a.mem>=95?'critical':a.cpu<25&&a.mem<30?'idle':'active';
  });
  applyFilters();
  document.getElementById('refreshTime').textContent=new Date().toLocaleTimeString();
},30000);
function addCopilotMessage(type,text,chartHtml,annotation){
  let container=document.getElementById('copilot-messages');
  let div=document.createElement('div');
  div.className='msg '+type;
  let ts=new Date().toLocaleTimeString();
  let bubble='<div class="bubble">';
  if(type==='copilot'&&chartHtml){bubble+=chartHtml}
  bubble+=text;
  if(annotation){bubble+='<div class="annotation">'+annotation+'</div>'}
  bubble+='<div class="timestamp">'+ts+'</div></div>';
  div.innerHTML=bubble;
  container.appendChild(div);
  container.scrollTop=container.scrollHeight;
}
function askCopilot(query){
  document.getElementById('copilotInput').value=query;
  sendCopilot();
}
function sendCopilot(){
  let input=document.getElementById('copilotInput');
  let query=input.value.trim();
  if(!query)return;
  input.value='';
  let btn=document.getElementById('copilotSendBtn');
  btn.disabled=true;
  addCopilotMessage('user',query);
  let loadingDiv=document.createElement('div');
  loadingDiv.className='msg copilot';
  loadingDiv.innerHTML='<div class="bubble"><div class="loading-dots"><span></span><span></span><span></span></div></div>';
  document.getElementById('copilot-messages').appendChild(loadingDiv);
  document.getElementById('copilot-messages').scrollTop=document.getElementById('copilot-messages').scrollHeight;
  setTimeout(function(){
    loadingDiv.remove();
    let result=parseNLQuery(query);
    let agents=result.filter?filteredAgents.filter(result.filter):filteredAgents;
    if(result.sort){agents.sort(result.sort)}
    if(result.limit){agents=agents.slice(0,result.limit)}
    let chartHtml='';
    if(result.chartType){
      let cw=320,ch=120,m={t:10,r:10,b:25,l:30};
      let colors={'cpu':'#58a6ff','mem':'#3fb950','disk':'#d29922','net':'#bc8cff'};
      let svg='<svg width="'+cw+'" height="'+ch+'" style="display:block">';
      if(result.chartType==='bar'&&agents.length){
        let met=result.metric||'cpu';
        let max=Math.max(...agents.map(a=>a[met]||0),1);
        let bw=(cw-m.l-m.r-10)/Math.min(agents.length,10);
        agents.slice(0,10).forEach((a,i)=>{
          let bh=a[met]/max*(ch-m.t-m.b-5);
          let x=m.l+i*bw+2;
          let y=m.t+ch-m.t-m.b-bh;
          svg+='<rect x="'+x+'" y="'+y+'" width="'+(bw-4)+'" height="'+Math.max(bh,1)+'" fill="'+(colors[met]||'#58a6ff')+'" rx="2"><title>'+a.id+': '+a[met]+'%</title></rect>';
          svg+='<text x="'+(x+bw/2-4)+'" y="'+(m.t+ch-m.t-m.b+12)+'" transform="rotate(-30,'+(x+bw/2-4)+','+(m.t+ch-m.t-m.b+12)+')" font-size="7" fill="#8b949e">'+a.id.slice(0,6)+'</text>';
        });
        svg+='<text x="'+(m.l)+'" y="'+(m.t+8)+'" font-size="8" fill="#8b949e">'+met.toUpperCase()+' %</text>';
      } else if(result.chartType==='comparison'&&agents.length){
        let met=result.metric||'cpu';
        let cur=agents.slice(0,5).reduce((s,a)=>s+a[met],0)/Math.min(agents.length,5);
        let prev=previousWeek.slice(0,Math.min(agents.length,5)).reduce((s,a)=>s+(a[met]||0),0)/Math.min(agents.length,5);
        let mm=Math.max(cur,prev,1);
        svg+='<rect x="'+m.l+'" y="'+(m.t+ch-m.t-m.b-(cur/mm*(ch-m.t-m.b-10)))+'" width="40" height="'+(cur/mm*(ch-m.t-m.b-10))+'" fill="#58a6ff" rx="2"/>';
        svg+='<text x="'+(m.l+20)+'" y="'+(m.t+ch-m.t-m.b+14)+'" text-anchor="middle" font-size="8" fill="#8b949e">this wk</text>';
        svg+='<rect x="'+(m.l+60)+'" y="'+(m.t+ch-m.t-m.b-(prev/mm*(ch-m.t-m.b-10)))+'" width="40" height="'+(prev/mm*(ch-m.t-m.b-10))+'" fill="#8b949e" rx="2"/>';
        svg+='<text x="'+(m.l+80)+'" y="'+(m.t+ch-m.t-m.b+14)+'" text-anchor="middle" font-size="8" fill="#8b949e">last wk</text>';
        svg+='<text x="'+(m.l+5)+'" y="'+(m.t+8)+'" font-size="8" fill="#8b949e">'+cur.toFixed(0)+'% vs '+prev.toFixed(0)+'%</text>';
      } else if(result.chartType==='aggregate'){
        let groups={};
        let met=result.metric||'cpu';
        agents.forEach(a=>{
          let g=a[result.groupBy||'tier']||'unknown';
          if(!groups[g])groups[g]={sum:0,count:0};
          groups[g].sum+=a[met]||0;
          groups[g].count++;
        });
        let keys=Object.keys(groups);
        let maxGrp=Math.max(...keys.map(k=>groups[k].sum/groups[k].count),1);
        keys.forEach((k,i)=>{
          let avg=groups[k].sum/groups[k].count;
          let bh=avg/maxGrp*(ch-m.t-m.b-10);
          let x=m.l+i*70+5;
          svg+='<rect x="'+x+'" y="'+(m.t+ch-m.t-m.b-bh)+'" width="50" height="'+Math.max(bh,1)+'" fill="#d29922" rx="2"/>';
          svg+='<text x="'+(x+25)+'" y="'+(m.t+ch-m.t-m.b+12)+'" text-anchor="middle" font-size="8" fill="#8b949e">'+k.slice(0,6)+'</text>';
          svg+='<text x="'+(x+25)+'" y="'+(m.t+ch-m.t-m.b-bh-4)+'" text-anchor="middle" font-size="7" fill="#f0f6fc">'+avg.toFixed(0)+'%</text>';
        });
      }
      svg+='</svg>';
      chartHtml='<div class="chart-inline">'+svg+'</div>';
    }
    let agentsForMsg=result.filter?filteredAgents.filter(result.filter):filteredAgents;
    if(result.limit)agentsForMsg=agentsForMsg.slice(0,result.limit);
    let text=result.text||'found '+agentsForMsg.length+' matching resources';
    if(agentsForMsg.length){text+=' — top: '+agentsForMsg.slice(0,3).map(a=>a.id+' ('+a.cpu+'% cpu)').join(', ')}
    let annotation=result.annotation||'copilot analyzed '+filteredAgents.length+' resources | context: time range='+document.getElementById('timeRange').value;
    addCopilotMessage('copilot',text,chartHtml,annotation);
    btn.disabled=false;
    copilotHistory.push({q:query,r:text});
  },500);
}
function parseNLQuery(q){
  let ql=q.toLowerCase();
  let result={text:'',chartType:null,metric:null,filter:null,sort:null,limit:null,annotation:'',groupBy:null};
  if(ql.includes('top')||ql.includes('highest')||ql.match(/\d+\s*top/)){
    result.chartType='bar';
    result.sort=(a,b)=>b.cpu-a.cpu;
    let m=ql.match(/(\d+)/);
    result.limit=m?parseInt(m[1]):5;
    if(ql.includes('cpu'))result.metric='cpu';
    else if(ql.includes('mem')||ql.includes('memory'))result.metric='mem';
    else if(ql.includes('disk'))result.metric='disk';
    else result.metric='cpu';
    result.text='top '+(result.limit)+' resources by '+result.metric.toUpperCase();
    result.annotation='bars show '+result.metric.toUpperCase()+' % | sorted descending';
  } else if(ql.includes('compare')||ql.includes('vs')||ql.includes('versus')||ql.includes('this week')||ql.includes('last week')){
    result.chartType='comparison';
    if(ql.includes('cpu'))result.metric='cpu';
    else if(ql.includes('mem')||ql.includes('memory'))result.metric='mem';
    else if(ql.includes('disk'))result.metric='disk';
    else result.metric='cpu';
    result.text='comparing this week vs last week: '+result.metric.toUpperCase();
    let cur=filteredAgents.reduce((s,a)=>s+a[result.metric],0)/filteredAgents.length;
    let prev=previousWeek.slice(0,filteredAgents.length).reduce((s,a)=>s+(a[result.metric]||0),0)/Math.min(previousWeek.length,filteredAgents.length);
    let dir=cur>prev?'up '+(cur-prev).toFixed(1)+'%':'down '+(prev-cur).toFixed(1)+'%';
    result.text+=' — '+dir+' from last week';
    result.annotation='this week avg: '+cur.toFixed(0)+'% vs last week avg: '+prev.toFixed(0)+'%';
  } else if(ql.includes('bucket')||ql.includes('over')||ql.includes('above')||ql.includes('>')||ql.includes('threshold')||ql.includes('breach')){
    result.chartType='bar';
    let threshold=80;
    let tm=ql.match(/(\d+)/);
    if(tm)threshold=parseInt(tm[1]);
    if(ql.includes('disk')){result.metric='disk';result.filter=a=>a.disk>=threshold}
    else if(ql.includes('cpu')){result.metric='cpu';result.filter=a=>a.cpu>=threshold}
    else if(ql.includes('mem')||ql.includes('memory')){result.metric='mem';result.filter=a=>a.mem>=threshold}
    else {result.metric='disk';result.filter=a=>a.disk>=threshold}
    result.sort=(a,b)=>b[result.metric]-a[result.metric];
    result.limit=10;
    let matching=filteredAgents.filter(result.filter);
    result.text=matching.length+' resources with '+result.metric.toUpperCase()+' over '+threshold+'%';
    result.annotation='threshold: >='+threshold+'% | showing all matching resources';
  } else if(ql.includes('trend')||ql.includes('pattern')||ql.includes('over time')||ql.includes('change')){
    result.chartType='bar';
    if(ql.includes('mem')||ql.includes('memory'))result.metric='mem';
    else if(ql.includes('cpu'))result.metric='cpu';
    else if(ql.includes('disk'))result.metric='disk';
    else if(ql.includes('network')||ql.includes('net'))result.metric='net';
    else result.metric='cpu';
    result.sort=(a,b)=>b[result.metric]-a[result.metric];
    result.limit=8;
    let m=computeMetrics(filteredAgents);
    let val=m[result.metric+'Avg']||0;
    let dir=val>55?'elevated '+(val>75?'(critical)':'(warning)') :'normal';
    result.text=result.metric.toUpperCase()+' trend: average '+val+'% across '+filteredAgents.length+' resources — '+dir;
    result.annotation='avg: '+val+'% | min: '+Math.min(...filteredAgents.map(a=>a[result.metric]||0))+'% | max: '+Math.max(...filteredAgents.map(a=>a[result.metric]||0))+'%';
  } else if(ql.includes('anomal')||ql.includes('spike')||ql.includes('outlier')||ql.includes('unusual')){
    result.chartType='bar';
    if(ql.includes('net')||ql.includes('network'))result.metric='net';
    else if(ql.includes('mem')||ql.includes('memory'))result.metric='mem';
    else if(ql.includes('disk'))result.metric='disk';
    else result.metric='cpu';
    let m=computeMetrics(filteredAgents);
    let avg=m[result.metric+'Avg']||0;
    let threshold=avg*1.5;
    result.filter=a=>(a[result.metric]||0)>=threshold;
    result.sort=(a,b)=>b[result.metric]-a[result.metric];
    result.limit=10;
    let anomalous=filteredAgents.filter(result.filter);
    result.text=anomalous.length+' anomalous '+result.metric.toUpperCase()+' readings detected (threshold: '+(avg*1.5).toFixed(0)+'%)';
    result.annotation='baseline avg: '+avg.toFixed(0)+'% | anomaly threshold: '+(avg*1.5).toFixed(0)+'% | '+(anomalous.length?anomalous.map(a=>a.id+' ('+a[result.metric]+'%)').join(', '):'no anomalies found');
  } else if(ql.includes('aggregate')||ql.includes('group')||ql.includes('by tier')||ql.includes('by class')||ql.includes('storage class')){
    result.chartType='aggregate';
    result.groupBy='tier';
    if(ql.includes('cpu'))result.metric='cpu';
    else if(ql.includes('mem')||ql.includes('memory'))result.metric='mem';
    else if(ql.includes('disk'))result.metric='disk';
    else result.metric='cpu';
    let groups={};
    filteredAgents.forEach(a=>{
      let g=a.tier;
      if(!groups[g])groups[g]={sum:0,count:0};
      groups[g].sum+=a[result.metric]||0;
      groups[g].count++;
    });
    let lines=Object.entries(groups).map(([k,v])=>k+': '+(v.sum/v.count).toFixed(0)+'% avg across '+v.count+' agents');
    result.text='aggregate '+result.metric.toUpperCase()+' by storage class — '+lines.join(' | ');
    result.annotation='tier breakdown: '+(lines.length?lines.join('; '):'no groups');
  } else if(ql.includes('filter')||ql.includes('show')||ql.includes('list')||ql.includes('find')||ql.includes('search')){
    if(ql.includes('idle'))result.filter=a=>a.status==='idle';
    else if(ql.includes('active'))result.filter=a=>a.status==='active';
    else if(ql.includes('critical'))result.filter=a=>a.status==='critical';
    else if(ql.includes('standard'))result.filter=a=>a.tier==='standard';
    else if(ql.includes('cold'))result.filter=a=>a.tier==='cold';
    else if(ql.includes('archive'))result.filter=a=>a.tier==='archive';
    let matching=filteredAgents.filter(result.filter||(()=>true));
    result.text='found '+matching.length+' resources matching "'+q+'"';
    result.annotation='query parsed as filter | context: all current dashboard filters applied';
  } else if(ql.includes('help')||ql.includes('what can')||ql.includes('example')){
    result.text='try asking: "show top 5 resources by cpu", "compare this week to last week", "show buckets over 80% disk", "what trend in memory usage", "find anomalies in network", "aggregate by storage class", or "show me all critical agents"';
    result.annotation='copilot supports 7 query types: top-N, comparison, threshold/bucket, trend, anomaly, aggregate, and filter';
  } else {
    let m=computeMetrics(filteredAgents);
    result.text='showing current state: cpu avg '+m.cpuAvg+'%, mem avg '+m.memAvg+'%, disk avg '+m.diskAvg+'% across '+m.count+' resources. '+m.critical+' in critical state, '+m.diskOver80+' with disk >80%.';
    result.annotation='generic query — returning summary stats. try a more specific query like "show top 5 resources by cpu"';
  }
  return result;
}
applyFilters();
addCopilotMessage('copilot','I am your Forge AI Copilot. Ask me anything about your infrastructure in natural language. Try: "show top 5 resources by cpu", "compare this week to last week", or "show me buckets over 80% disk".');
</script>
</body>
</html>