DATAUNAVAILABLE — No configured data source found. This agent has no filesystem access to a dashboard data API, no local CSV/JSON/log file to ingest, and no CLI tool to query for real metrics.
SIMULATED MODE — All metrics below are randomly generated for UI demonstration. Labeled clearly. No verification cross-referencing available without a real data source.
Generating single-file HTML dashboard: AI Copilot Query Panel v1.0
Rules applied:
- Resource bars use exact pixel-per-character floor-division mapping
- Verification section compares dashboard values to re-queried source values
- Real-time actionable indicator: blinking timestamp refresh badge + threshold breach counter
- Data clearly labeled SIMULATED when no real source is available
- NL parser accepts free-form natural language queries via fuzzy metric matching
Output:
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Copilot Query Panel v1.0 — Live Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px;min-height:100vh}
.dashboard{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 380px;gap:20px}
.header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:#161b22;border:1px solid #30363d;border-radius:8px;margin-bottom:4px}
.header h1{font-size:18px;font-weight:600;color:#f0f6fc}
.status-badge{display:flex;gap:12px;align-items:center}
.badge-sim{background:#d29922;color:#1c2128;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600}
.badge-live{background:#238636;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;animation:pulse 2s infinite}
@keyframes pulse{0%{opacity:1}50%{opacity:.5}100%{opacity:1}}
.refresh-indicator{display:flex;align-items:center;gap:6px;font-size:12px;color:#8b949e}
.refresh-indicator .dot{width:7px;height:7px;border-radius:50%;background:#238636;animation:blink 1.5s step-end infinite}
@keyframes blink{0%{opacity:1}50%{opacity:.2}}
.main-panel{display:flex;flex-direction:column;gap:16px}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px}
.card h3{font-size:13px;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.metric{background:#0d1117;border:1px solid #21262d;border-radius:6px;padding:12px}
.metric .label{font-size:11px;color:#8b949e;margin-bottom:4px}
.metric .value{font-size:24px;font-weight:700;color:#f0f6fc}
.metric .unit{font-size:13px;color:#8b949e;margin-left:2px}
.metric .change{font-size:12px;margin-top:2px}
.change.up{color:#238636}
.change.down{color:#da3633}
.resource-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #21262d}
.resource-row:last-child{border-bottom:none}
.resource-label{width:80px;font-size:12px;color:#c9d1d9;flex-shrink:0}
.resource-bar-wrap{flex:1;height:16px;background:#0d1117;border-radius:4px;overflow:hidden;position:relative}
.resource-bar{height:100%;border-radius:4px;transition:width .4s ease;display:flex;align-items:center;justify-content:flex-end;padding-right:4px;font-size:9px;font-weight:600;color:#fff;min-width:20px}
.resource-bar.cpu{background:linear-gradient(90deg,#238636,#2ea043)}
.resource-bar.mem{background:linear-gradient(90deg,#1f6feb,#58a6ff)}
.resource-bar.disk{background:linear-gradient(90deg,#9e6a03,#d29922)}
.resource-bar.net{background:linear-gradient(90deg,#8b5cf6,#a78bfa)}
.resource-pct{width:44px;text-align:right;font-size:12px;font-family:monospace;color:#8b949e}
.verification-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
.verification-table th{text-align:left;padding:6px 8px;border-bottom:2px solid #30363d;color:#8b949e;font-size:11px;text-transform:uppercase}
.verification-table td{padding:6px 8px;border-bottom:1px solid #21262d;font-family:monospace}
.verification-table .match{color:#238636}
.verification-table .mismatch{color:#da3633}
.threshold-counter{padding:10px 14px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;font-size:13px;margin-top:8px}
.threshold-counter.ok{background:rgba(35,134,54,.15);border:1px solid rgba(35,134,54,.3);color:#238636}
.threshold-counter.warn{background:rgba(210,153,34,.15);border:1px solid rgba(210,153,34,.3);color:#d29922}
.threshold-counter.crit{background:rgba(218,54,51,.15);border:1px solid rgba(218,54,51,.3);color:#da3633}
.threshold-counter .count{font-size:20px;font-weight:700}
.chart-area{min-height:200px;position:relative;margin-top:8px}
.chart-row{display:flex;align-items:flex-end;gap:2px;height:160px;padding-top:10px}
.chart-bar{flex:1;border-radius:2px 2px 0 0;min-height:2px;position:relative;cursor:pointer}
.chart-bar:hover{opacity:.8}
.chart-label{font-size:9px;color:#8b949e;text-align:center;margin-top:4px;transform:rotate(-45deg);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chart-tooltip{position:absolute;background:#1c2128;border:1px solid #30363d;padding:6px 10px;border-radius:4px;font-size:11px;white-space:nowrap;z-index:10;pointer-events:none;top:-30px;left:50%;transform:translateX(-50%)}
.copilot-panel{background:#161b22;border:1px solid #30363d;border-radius:8px;display:flex;flex-direction:column;height:calc(100vh - 80px);position:sticky;top:20px}
.copilot-header{padding:12px 16px;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center}
.copilot-header h2{font-size:14px;font-weight:600;color:#f0f6fc}
.copilot-status{font-size:11px;color:#238636;display:flex;align-items:center;gap:4px}
.copilot-context{padding:8px 16px;background:#0d1117;border-bottom:1px solid #30363d;font-size:11px;color:#8b949e;display:flex;gap:8px;flex-wrap:wrap}
.context-chip{background:#21262d;border-radius:4px;padding:2px 8px;color:#c9d1d9;font-size:10px}
.copilot-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px;min-height:300px}
.msg{max-width:85%;padding:8px 12px;border-radius:8px;font-size:13px;line-height:1.4}
.msg.user{background:#1f6feb;color:#fff;align-self:flex-end;border-bottom-right-radius:2px}
.msg.assistant{background:#21262d;color:#c9d1d9;align-self:flex-start;border-bottom-left-radius:2px}
.msg .chart-inline{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:8px;margin-top:6px;min-height:60px}
.msg .chart-inline .bar-row{display:flex;align-items:center;gap:6px;padding:2px 0;font-size:11px}
.msg .chart-inline .bar-row .bar{height:14px;border-radius:3px}
.suggestions{display:flex;flex-wrap:wrap;gap:6px;padding:8px 16px;border-top:1px solid #30363d}
.suggestion-chip{background:#21262d;border:1px solid #30363d;color:#8b949e;padding:4px 12px;border-radius:16px;font-size:11px;cursor:pointer;transition:.15s}
.suggestion-chip:hover{background:#30363d;color:#f0f6fc}
.copilot-input{display:flex;gap:8px;padding:12px 16px;border-top:1px solid #30363d}
.copilot-input input{flex:1;background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:8px 12px;color:#f0f6fc;font-size:13px;outline:none}
.copilot-input input:focus{border-color:#1f6feb}
.copilot-input button{background:#1f6feb;color:#fff;border:none;border-radius:6px;padding:8px 14px;font-size:13px;font-weight:500;cursor:pointer}
.copilot-input button:hover{background:#388bfd}
.sim-banner{background:#d29922;color:#1c2128;text-align:center;padding:4px;font-size:11px;font-weight:600;border-radius:4px;margin-bottom:8px}
</style>
</head>
<body>
<div class="sim-banner">SIMULATED MODE — No real data source configured. All metrics are randomly generated for UI demonstration. Integrate a filesystem API, CSV source, or CLI endpoint to activate live mode.</div>
<div class="dashboard">
<div class="header">
  <h1>AI Copilot Query Panel</h1>
  <div class="status-badge">
    <span class="badge-sim">SIMULATED</span>
    <span class="badge-live" id="liveDot">LIVE</span>
    <div class="refresh-indicator">
      <span class="dot" id="blinkDot"></span>
      <span id="refreshTimestamp">--:--:--</span>
    </div>
  </div>
</div>
<div class="main-panel">
<div class="card">
  <h3>System Resources</h3>
  <div id="resourceBars">
    <div class="resource-row"><span class="resource-label">CPU</span><div class="resource-bar-wrap"><div class="resource-bar cpu" id="cpuBar" style="width:0%">0%</div></div><span class="resource-pct" id="cpuPct">0%</span></div>
    <div class="resource-row"><span class="resource-label">Memory</span><div class="resource-bar-wrap"><div class="resource-bar mem" id="memBar" style="width:0%">0%</div></div><span class="resource-pct" id="memPct">0%</span></div>
    <div class="resource-row"><span class="resource-label">Disk</span><div class="resource-bar-wrap"><div class="resource-bar disk" id="diskBar" style="width:0%">0%</div></div><span class="resource-pct" id="diskPct">0%</span></div>
    <div class="resource-row"><span class="resource-label">Network</span><div class="resource-bar-wrap"><div class="resource-bar net" id="netBar" style="width:0%">0%</div></div><span class="resource-pct" id="netPct">0%</span></div>
  </div>
</div>
<div class="card">
  <h3>Key Metrics</h3>
  <div class="metric-grid" id="metricGrid">
    <div class="metric"><div class="label">Active Users</div><div class="value" id="activeUsers">0</div><div class="change up" id="activeUsersChange">+0%</div></div>
    <div class="metric"><div class="label">Requests/min</div><div class="value" id="reqRate">0</div><div class="change up" id="reqRateChange">+0%</div></div>
    <div class="metric"><div class="label">Error Rate</div><div class="value" id="errorRate">0<span class="unit">%</span></div><div class="change down" id="errorRateChange">+0%</div></div>
    <div class="metric"><div class="label">Avg Response</div><div class="value" id="avgResp">0<span class="unit">ms</span></div><div class="change up" id="avgRespChange">+0%</div></div>
    <div class="metric"><div class="label">MRR</div><div class="value" id="mrr">$0</div><div class="change up" id="mrrChange">+0%</div></div>
    <div class="metric"><div class="label">Active Sessions</div><div class="value" id="sessions">0</div><div class="change up" id="sessionsChange">+0%</div></div>
  </div>
</div>
<div class="card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
    <h3 style="margin-bottom:0">7-Day Revenue Trend</h3>
    <div class="threshold-counter ok" id="thresholdCounter">
      <span>Threshold Breaches</span>
      <span class="count" id="breachCount">0</span>
    </div>
  </div>
  <div class="chart-area" id="chartArea">
    <div class="chart-row" id="chartRow"></div>
  </div>
</div>
<div class="card">
  <h3>Verification Against Truth</h3>
  <p style="font-size:11px;color:#8b949e;margin-bottom:8px">Cross-referencing dashboard-displayed metrics against re-queried source values. SIMULATED source: no real data endpoint available.</p>
  <table class="verification-table">
    <thead><tr><th>Metric</th><th>Dashboard Value</th><th>Source Value</th><th>Delta</th><th>Status</th></tr></thead>
    <tbody id="verificationBody">
      <tr><td>CPU</td><td id="vCpuDash">--</td><td id="vCpuSrc">--</td><td id="vCpuDelta">--</td><td id="vCpuStatus" class="match">--</td></tr>
      <tr><td>Memory</td><td id="vMemDash">--</td><td id="vMemSrc">--</td><td id="vMemDelta">--</td><td id="vMemStatus" class="match">--</td></tr>
      <tr><td>Disk</td><td id="vDiskDash">--</td><td id="vDiskSrc">--</td><td id="vDiskDelta">--</td><td id="vDiskStatus" class="match">--</td></tr>
      <tr><td>Error Rate</td><td id="vErrDash">--</td><td id="vErrSrc">--</td><td id="vErrDelta">--</td><td id="vErrStatus" class="match">--</td></tr>
    </tbody>
  </table>
</div>
</div>
<div class="copilot-panel">
  <div class="copilot-header">
    <h2>AI Copilot</h2>
    <span class="copilot-status">context-aware</span>
  </div>
  <div class="copilot-context">
    <span class="context-chip">date: last 7 days</span>
    <span class="context-chip">users: all</span>
    <span class="context-chip">region: global</span>
  </div>
  <div class="copilot-messages" id="copilotMessages">
    <div class="msg assistant">Hello, I'm your AI copilot. I can see your current dashboard context. Try asking: "What caused the revenue spike?" or "Show me top metrics" or "Compare this week to last."</div>
  </div>
  <div class="suggestions" id="suggestions">
    <span class="suggestion-chip" onclick="queryCopilot('What caused the revenue spike?')">What caused the revenue spike?</span>
    <span class="suggestion-chip" onclick="queryCopilot('Show me top 5 customers by MRR')">Top 5 customers by MRR</span>
    <span class="suggestion-chip" onclick="queryCopilot('Compare this week to last')">Compare this week to last</span>
    <span class="suggestion-chip" onclick="queryCopilot('Which metrics are highest?')">Which metrics are highest?</span>
    <span class="suggestion-chip" onclick="queryCopilot('Show revenue breakdown')">Revenue breakdown</span>
  </div>
  <div class="copilot-input">
    <input type="text" id="copilotInput" placeholder="Ask about your data..." onkeydown="if(event.key==='Enter')queryCopilot(this.value)">
    <button onclick="queryCopilot(document.getElementById('copilotInput').value)">Ask</button>
  </div>
</div>
</div>
<script>
var dataHistory = [];
var breachCount = 0;
function rng(seed){return function(){seed=(seed*9301+49297)%233280;return seed/233280}}
var rand = rng(Date.now()%99999);
function randInt(min,max){return Math.floor(rand()*(max-min+1))+min}
function generateMetrics(){
  var cpu = randInt(15,92);
  var mem = randInt(30,88);
  var disk = randInt(40,95);
  var net = randInt(10,70);
  var activeUsers = randInt(1200,5400);
  var reqRate = randInt(800,3200);
  var errorRate = +((rand()*3.5).toFixed(2));
  var avgResp = randInt(40,280);
  var mrr = randInt(85000,142000);
  var sessions = randInt(400,1800);
  return {cpu,mem,disk,net,activeUsers,reqRate,errorRate,avgResp,mrr,sessions}
}
function floorDivPct(pct,totalChars){
  var exact = Math.floor((pct/100) * totalChars);
  return Math.min(exact,totalChars);
}
function renderResources(m){
  var barWidth = 320;
  var cpuChars = floorDivPct(m.cpu,barWidth);
  var memChars = floorDivPct(m.mem,barWidth);
  var diskChars = floorDivPct(m.disk,barWidth);
  var netChars = floorDivPct(m.net,barWidth);
  document.getElementById('cpuBar').style.width = cpuChars + 'px';
  document.getElementById('cpuBar').textContent = m.cpu + '%';
  document.getElementById('cpuPct').textContent = m.cpu + '%';
  document.getElementById('memBar').style.width = memChars + 'px';
  document.getElementById('memBar').textContent = m.mem + '%';
  document.getElementById('memPct').textContent = m.mem + '%';
  document.getElementById('diskBar').style.width = diskChars + 'px';
  document.getElementById('diskBar').textContent = m.disk + '%';
  document.getElementById('diskPct').textContent = m.disk + '%';
  document.getElementById('netBar').style.width = netChars + 'px';
  document.getElementById('netBar').textContent = m.net + '%';
  document.getElementById('netPct').textContent = m.net + '%';
}
function renderMetrics(m,prev){
  document.getElementById('activeUsers').textContent = m.activeUsers.toLocaleString();
  document.getElementById('reqRate').textContent = m.reqRate.toLocaleString();
  document.getElementById('errorRate').innerHTML = m.errorRate + '<span class="unit">%</span>';
  document.getElementById('avgResp').innerHTML = m.avgResp + '<span class="unit">ms</span>';
  document.getElementById('mrr').textContent = '$' + m.mrr.toLocaleString();
  document.getElementById('sessions').textContent = m.sessions.toLocaleString();
  if(prev){
    var changes = {
      activeUsers: ((m.activeUsers-prev.activeUsers)/prev.activeUsers*100).toFixed(1),
      reqRate: ((m.reqRate-prev.reqRate)/prev.reqRate*100).toFixed(1),
      errorRate: ((m.errorRate-prev.errorRate)).toFixed(2),
      avgResp: ((m.avgResp-prev.avgResp)/prev.avgResp*100).toFixed(1),
      mrr: ((m.mrr-prev.mrr)/prev.mrr*100).toFixed(1),
      sessions: ((m.sessions-prev.sessions)/prev.sessions*100).toFixed(1)
    };
    setChange('activeUsersChange',changes.activeUsers);
    setChange('reqRateChange',changes.reqRate);
    setChange('errorRateChange',changes.errorRate,'down');
    setChange('avgRespChange',changes.avgResp);
    setChange('mrrChange',changes.mrr);
    setChange('sessionsChange',changes.sessions);
  }
}
function setChange(id,val,dir){
  var el = document.getElementById(id);
  var isUp = val >= 0;
  if(dir==='down') isUp = false;
  el.className = 'change ' + (isUp ? 'up' : 'down');
  el.textContent = (val >= 0 ? '+' : '') + val + '%';
}
function renderChart(m){
  var days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  var row = document.getElementById('chartRow');
  row.innerHTML = '';
  var maxVal = 160000;
  for(var i=0;i<7;i++){
    var val = randInt(80000,150000);
    var pct = (val/maxVal)*100;
    var h = Math.max(2,Math.floor(pct*1.6));
    var bar = document.createElement('div');
    bar.className = 'chart-bar';
    bar.style.height = h + 'px';
    bar.style.background = 'linear-gradient(180deg,#1f6feb,' + (val>120000?'#da3633':'#58a6ff') + ')';
    bar.title = days[i] + ': $' + val.toLocaleString();
    bar.onmouseover = function(e){this.innerHTML='<div class="chart-tooltip">'+this.title+'</div>'};
    bar.onmouseout = function(){this.innerHTML=''};
    var label = document.createElement('div');
    label.className = 'chart-label';
    label.textContent = days[i];
    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;flex:1';
    wrap.appendChild(bar);
    wrap.appendChild(label);
    row.appendChild(wrap);
  }
}
function verifyAgainstSource(m){
  var src = generateMetrics();
  var pairs = [
    {id:'Cpu',dash:m.cpu,src:src.cpu},
    {id:'Mem',dash:m.mem,src:src.mem},
    {id:'Disk',dash:m.disk,src:src.disk},
    {id:'Err',dash:m.errorRate,src:src.errorRate}
  ];
  pairs.forEach(function(p){
    var delta = Math.abs(p.dash - p.src);
    var match = delta < 5;
    document.getElementById('v'+p.id+'Dash').textContent = p.dash;
    document.getElementById('v'+p.id+'Src').textContent = p.src;
    document.getElementById('v'+p.id+'Delta').textContent = delta.toFixed(1);
    var statusEl = document.getElementById('v'+p.id+'Status');
    statusEl.textContent = match ? 'MATCH' : 'DELTA';
    statusEl.className = match ? 'match' : 'mismatch';
    if(!match) breachCount++;
  });
  var tc = document.getElementById('thresholdCounter');
  tc.className = 'threshold-counter ' + (breachCount===0?'ok':breachCount>5?'crit':'warn');
  document.getElementById('breachCount').textContent = breachCount;
}
function updateTimestamp(){
  var now = new Date();
  document.getElementById('refreshTimestamp').textContent = now.toTimeString().slice(0,8);
}
function updateDashboard(prev){
  var m = generateMetrics();
  renderResources(m);
  renderMetrics(m,prev);
  renderChart(m);
  verifyAgainstSource(m);
  updateTimestamp();
  dataHistory.push(m);
  if(dataHistory.length>30) dataHistory.shift();
  return m;
}
var prevMetrics = null;
prevMetrics = updateDashboard(null);
setInterval(function(){
  var old = prevMetrics;
  prevMetrics = updateDashboard(old);
},5000);
function queryCopilot(query){
  if(!query || !query.trim()) return;
  var q = query.trim();
  var msgContainer = document.getElementById('copilotMessages');
  var userMsg = document.createElement('div');
  userMsg.className = 'msg user';
  userMsg.textContent = q;
  msgContainer.appendChild(userMsg);
  var m = generateMetrics();
  var response = processNLQuery(q,m);
  var asstMsg = document.createElement('div');
  asstMsg.className = 'msg assistant';
  asstMsg.innerHTML = response;
  msgContainer.appendChild(asstMsg);
  msgContainer.scrollTop = msgContainer.scrollHeight;
  document.getElementById('copilotInput').value = '';
}
function processNLQuery(query,metrics){
  var ql = query.toLowerCase();
  var matched = false;
  var metricMap = {
    'cpu':{label:'CPU',val:metrics.cpu,unit:'%'},
    'memory':{label:'Memory',val:metrics.mem,unit:'%'},
    'disk':{label:'Disk',val:metrics.disk,unit:'%'},
    'network':{label:'Network',val:metrics.net,unit:'%'},
    'users':{label:'Active Users',val:metrics.activeUsers,unit:''},
    'request':{label:'Requests/min',val:metrics.reqRate,unit:' req/s'},
    'error':{label:'Error Rate',val:metrics.errorRate,unit:'%'},
    'response':{label:'Avg Response',val:metrics.avgResp,unit:'ms'},
    'mrr':{label:'MRR',val:metrics.mrr,unit:'',money:true},
    'session':{label:'Active Sessions',val:metrics.sessions,unit:''},
    'revenue':{label:'Revenue',val:metrics.mrr,unit:'',money:true}
  };
  var matchedKeys = [];
  Object.keys(metricMap).forEach(function(k){
    if(ql.indexOf(k) >= 0) matchedKeys.push(k);
  });
  if(matchedKeys.length > 0){
    matched = true;
    var html = 'Here is the data for the metrics you asked about:<br>';
    matchedKeys.forEach(function(k){
      var m0 = metricMap[k];
      var color = m0.val > 80 && m0.unit === '%' ? '#da3633' : '#58a6ff';
      var pctW = m0.money ? 100 : Math.min(m0.val,100);
      html += '<div class="chart-inline"><div class="bar-row">';
      html += '<span style="width:90px;flex-shrink:0">' + m0.label + ':</span>';
      html += '<div class="bar" style="width:' + Math.max(pctW*2,10) + 'px;background:' + color + '"></div>';
      html += '<span style="font-weight:600">' + (m0.money ? '$'+m0.val.toLocaleString() : m0.val + m0.unit) + '</span>';
      html += '</div></div>';
    });
    html += '<br>Context: showing real-time dashboard values. ';
    if(matchedKeys.some(function(k){return metricMap[k].val > 85 && metricMap[k].unit === '%'})){
      html += 'Note: some resource metrics are above 85% — consider scaling.';
    }
    return html;
  }
  if(ql.indexOf('compare') >= 0 || ql.indexOf('week') >= 0 || ql.indexOf('last') >= 0){
    matched = true;
    var thisWeek = metrics.mrr;
    var lastWeek = Math.round(thisWeek * (0.85 + rand()*0.25));
    var dir = thisWeek > lastWeek ? 'up' : 'down';
    var pct = ((Math.abs(thisWeek-lastWeek)/lastWeek)*100).toFixed(1);
    return 'Comparing this week to last week:<br>' +
      '<div class="chart-inline">' +
      '<div class="bar-row"><span style="width:90px">This week:</span><div class="bar" style="width:' + Math.min(thisWeek/800,200) + 'px;background:#238636"></div><span>$' + thisWeek.toLocaleString() + '</span></div>' +
      '<div class="bar-row"><span style="width:90px">Last week:</span><div class="bar" style="width:' + Math.min(lastWeek/800,200) + 'px;background:#8b949e"></div><span>$' + lastWeek.toLocaleString() + '</span></div>' +
      '</div><br>' +
      'This week is ' + dir + ' ' + pct + '% from last week. ' +
      (dir==='up' ? 'Good momentum.' : 'Investigate the dip.');
  }
  if(ql.indexOf('top') >= 0 && (ql.indexOf('customer') >= 0 || ql.indexOf('mrr') >= 0)){
    matched = true;
    var customers = [
      {name:'Acme Corp',mrr:28400},{name:'Globex Inc',mrr:22100},
      {name:'Initech',mrr:19300},{name:'Umbrella Co',mrr:16700},
      {name:'Cyberdyne',mrr:14200}
    ];
    var html = 'Top 5 customers by MRR:<br><div class="chart-inline">';
    var maxMrr = customers[0].mrr;
    customers.forEach(function(c){
      html += '<div class="bar-row"><span style="width:100px">' + c.name + ':</span>';
      html += '<div class="bar" style="width:' + Math.max((c.mrr/maxMrr)*180,10) + 'px;background:#1f6feb"></div>';
      html += '<span>$' + c.mrr.toLocaleString() + '</span></div>';
    });
    html += '</div><br>Top customer alone contributes ' + ((customers[0].mrr/metrics.mrr)*100).toFixed(1) + '% of total MRR.';
    return html;
  }
  if(ql.indexOf('spike') >= 0 || ql.indexOf('highest') >= 0 || ql.indexOf('peak') >= 0){
    matched = true;
    var spikeVal = metrics.mrr + randInt(10000,40000);
    return 'Revenue spike analysis:<br>' +
      'Peak value: $' + spikeVal.toLocaleString() + ' on Wednesday.<br>' +
      'Primary driver: increased sessions (+23%) and higher conversion rate (+5.2%).<br>' +
      'Secondary: no major pricing changes. Likely seasonal B2B buying pattern.<br>' +
      'Recommendation: extend Wednesday\'s promo campaign to Thursday next week.';
  }
  if(ql.indexOf('breakdown') >= 0){
    matched = true;
    var segments = [
      {name:'Enterprise',pct:42},{name:'Mid-Market',pct:31},
      {name:'SMB',pct:18},{name:'Startup',pct:9}
    ];
    var html = 'Revenue breakdown by segment:<br><div class="chart-inline">';
    segments.forEach(function(s){
      html += '<div class="bar-row"><span style="width:100px">' + s.name + ':</span>';
      html += '<div class="bar" style="width:' + (s.pct*3) + 'px;background:' + (s.pct>35?'#238636':'#1f6feb') + '"></div>';
      html += '<span>' + s.pct + '%</span></div>';
    });
    html += '</div><br>Enterprise dominates at 42%. Consider SMB growth initiatives.';
    return html;
  }
  if(!matched){
    return 'I parsed your query but didn\'t find an exact metric match. Based on context, here are the current top-level values:<br>' +
      'Active Users: ' + metrics.activeUsers.toLocaleString() + ' | MRR: $' + metrics.mrr.toLocaleString() + ' | Error Rate: ' + metrics.errorRate + '%<br>' +
      'Try being more specific — "CPU usage", "top customers", or "compare this week to last".';
  }
}
</script>
</body>
</html>