```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SLO Dashboard - Real-Time Reliability</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}
.dashboard{max-width:1600px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:16px}
h2{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#8b949e;margin-bottom:12px}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;position:relative}
.card.full{grid-column:1/-1}
/* GAUGE */
.gauge-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 0}
.gauge-svg{width:220px;height:220px}
.gauge-center{fill:none}
.gauge-label{font-size:28px;font-weight:700;fill:#c9d1d9}
.gauge-sublabel{font-size:12px;fill:#8b949e}
.gauge-stats{display:flex;gap:32px;margin-top:8px;text-align:center}
.gauge-stat-value{font-size:20px;font-weight:600}
.gauge-stat-label{font-size:11px;color:#8b949e;margin-top:2px}
.color-green{color:#3fb950}
.color-yellow{color:#d29922}
.color-red{color:#f85149}
.color-blue{color:#58a6ff}
.color-purple{color:#bc8cff}
/* LATENCY CHARTS */
.chart-row{display:flex;gap:16px;margin-bottom:8px}
.chart-box{flex:1;min-width:0}
.chart-box canvas{max-height:120px;width:100% !important}
.chart-meta{display:flex;justify-content:space-between;font-size:11px;color:#8b949e;margin-top:4px}
.chart-percentile{font-size:12px;font-weight:600;color:#c9d1d9;margin-bottom:2px}
/* HEATMAP */
.heatmap-wrap{overflow-x:auto}
.heatmap-grid{display:grid;grid-template-columns:50px repeat(24,1fr);gap:2px;font-size:10px;min-width:600px}
.heatmap-header{font-weight:600;color:#8b949e;text-align:center;padding:2px 0}
.heatmap-label{display:flex;align-items:center;color:#8b949e;padding-right:6px;justify-content:flex-end;font-size:10px;height:24px}
.heatmap-cell{height:24px;border-radius:2px;cursor:pointer;transition:opacity 0.15s;position:relative}
.heatmap-cell:hover{opacity:0.8;outline:2px solid #58a6ff}
.heatmap-cell.critical{background:#f85149}
.heatmap-cell.high{background:#d29922}
.heatmap-cell.medium{background:#58a6ff}
.heatmap-cell.low{background:#1f6feb33}
.heatmap-cell.none{background:#0d1117}
.heatmap-legend{display:flex;gap:16px;margin-top:8px;font-size:11px;color:#8b949e;align-items:center}
.legend-swatch{width:12px;height:12px;border-radius:2px;display:inline-block;margin-right:4px}
/* DEPENDENCY TREE */
.dep-tree{font-size:13px;line-height:1.8}
.dep-node{display:flex;align-items:center;gap:8px;padding:3px 0}
.dep-node.level-0{padding-left:0;font-weight:600}
.dep-node.level-1{padding-left:24px}
.dep-node.level-2{padding-left:48px}
.dep-node.level-3{padding-left:72px}
.dep-status{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.dep-status.healthy{background:#3fb950;box-shadow:0 0 6px #3fb95066}
.dep-status.degraded{background:#d29922;box-shadow:0 0 6px #d2992266}
.dep-status.down{background:#f85149;box-shadow:0 0 6px #f8514966}
.dep-status.unknown{background:#8b949e}
.dep-cascade{font-size:10px;background:#f8514922;color:#f85149;padding:1px 6px;border-radius:4px;margin-left:6px}
.dep-name{color:#c9d1d9}
.dep-latency{font-size:11px;color:#8b949e;margin-left:auto}
/* SLO TABLE */
.slo-table{width:100%;border-collapse:collapse;font-size:13px}
.slo-table th{text-align:left;padding:6px 8px;border-bottom:1px solid #30363d;color:#8b949e;font-weight:600;font-size:11px;text-transform:uppercase}
.slo-table td{padding:6px 8px;border-bottom:1px solid #21262d}
.slo-table tr:last-child td{border-bottom:none}
.slo-bar{height:6px;border-radius:3px;background:#21262d;overflow:hidden;min-width:80px}
.slo-bar-fill{height:100%;border-radius:3px;transition:width 0.5s}
.slo-attainment{font-weight:600;font-size:13px}
.slo-budget{font-size:11px}
/* INCIDENT TIMELINE */
.incident-timeline{position:relative;padding-left:24px}
.incident-timeline::before{content:'';position:absolute;left:8px;top:0;bottom:0;width:2px;background:#30363d}
.incident-item{position:relative;padding:8px 0 8px 16px;border-left:3px solid transparent}
.incident-item::before{content:'';position:absolute;left:-20px;top:13px;width:10px;height:10px;border-radius:50%;border:2px solid}
.incident-item.resolved{border-left-color:#3fb950}
.incident-item.resolved::before{background:#3fb950;border-color:#3fb950}
.incident-item.ongoing{border-left-color:#d29922}
.incident-item.ongoing::before{background:#d29922;border-color:#d29922}
.incident-item.critical{border-left-color:#f85149}
.incident-item.critical::before{background:#f85149;border-color:#f85149}
.incident-time{font-size:11px;color:#8b949e}
.incident-title{font-size:13px;color:#c9d1d9;font-weight:500;margin:2px 0}
.incident-desc{font-size:11px;color:#8b949e}
.incident-tag{display:inline-block;font-size:10px;padding:1px 6px;border-radius:4px;margin-right:4px;margin-top:4px}
.incident-tag.p0{background:#f8514933;color:#f85149}
.incident-tag.p1{background:#d2992233;color:#d29922}
.incident-tag.p2{background:#58a6ff33;color:#58a6ff}
/* BURN-DOWN CHART WRAPPER */
.burndown-wrap{height:100px;margin-top:8px}
@media(max-width:900px){.dashboard{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="dashboard">
  <!-- CARD: Error Budget Gauge -->
  <div class="card">
    <h2>Error Budget — api-gateway (99.9% SLO)</h2>
    <div class="gauge-wrap">
      <svg class="gauge-svg" viewBox="0 0 220 220">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#f85149"/>
            <stop offset="40%" stop-color="#d29922"/>
            <stop offset="70%" stop-color="#3fb950"/>
            <stop offset="100%" stop-color="#3fb950"/>
          </linearGradient>
        </defs>
        <circle cx="110" cy="110" r="85" fill="none" stroke="#21262d" stroke-width="14" transform="rotate(-90 110 110)"/>
        <circle id="budgetArc" cx="110" cy="110" r="85" fill="none" stroke="url(#gaugeGrad)" stroke-width="14" stroke-dasharray="534" stroke-dashoffset="534" stroke-linecap="round" transform="rotate(-90 110 110)"/>
        <text id="budgetText" class="gauge-label" x="110" y="106" text-anchor="middle">0%</text>
        <text class="gauge-sublabel" x="110" y="126" text-anchor="middle">budget remaining</text>
      </svg>
      <div class="gauge-stats">
        <div><div class="gauge-stat-value color-green" id="budgetPct">87.3%</div><div class="gauge-stat-label">Remaining</div></div>
        <div><div class="gauge-stat-value color-yellow" id="burnRate">2.1x</div><div class="gauge-stat-label">Burn Rate</div></div>
        <div><div class="gauge-stat-value" id="exhaustDate" style="color:#58a6ff">+12d</div><div class="gauge-stat-label">Exhaustion ETA</div></div>
        <div><div class="gauge-stat-value" id="sloWindow">24h</div><div class="gauge-stat-label">Window</div></div>
      </div>
    </div>
  </div>
  <!-- CARD: SLO Definitions -->
  <div class="card">
    <h2>Service Level Objectives</h2>
    <table class="slo-table">
      <thead><tr><th>Service</th><th>Target</th><th>Window</th><th>Attainment</th><th>Budget</th><th>Trend</th></tr></thead>
      <tbody id="sloTableBody"></tbody>
    </table>
  </div>
  <!-- CARD: Latency Sparklines -->
  <div class="card full">
    <h2>Multi-Percentile Latency (last 24h) · SLO Threshold: 200ms</h2>
    <div class="chart-row">
      <div class="chart-box"><div class="chart-percentile color-blue">p50</div><canvas id="latencyP50"></canvas></div>
      <div class="chart-box"><div class="chart-percentile color-yellow">p95</div><canvas id="latencyP95"></canvas></div>
      <div class="chart-box"><div class="chart-percentile color-purple">p99</div><canvas id="latencyP99"></canvas></div>
    </div>
    <div class="chart-meta">
      <span>Current: <span id="latencyCurrent">—</span></span>
      <span>SLO breached: <span id="latencyBreach" style="color:#3fb950">0</span> times</span>
      <span>Max: <span id="latencyMax">—</span></span>
    </div>
  </div>
  <!-- CARD: Error Rate Heatmap -->
  <div class="card">
    <h2>Error Rate Heatmap — Time × Severity (24h)</h2>
    <div class="heatmap-wrap">
      <div class="heatmap-grid" id="heatmapGrid"></div>
    </div>
    <div class="heatmap-legend">
      <span><span class="legend-swatch" style="background:#f85149"></span>Critical</span>
      <span><span class="legend-swatch" style="background:#d29922"></span>High</span>
      <span><span class="legend-swatch" style="background:#58a6ff"></span>Medium</span>
      <span><span class="legend-swatch" style="background:#1f6feb33"></span>Low</span>
      <span><span class="legend-swatch" style="background:#0d1117"></span>None</span>
    </div>
  </div>
  <!-- CARD: Dependency Tree -->
  <div class="card">
    <h2>Service Dependency Tree — Cascading Failure Detection</h2>
    <div class="dep-tree" id="depTree"></div>
  </div>
  <!-- CARD: Incidents + Burn-Down -->
  <div class="card full">
    <h2>Incident Timeline &amp; SLO Burn-Down</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="burndown-wrap"><canvas id="burndownChart"></canvas></div>
      <div class="incident-timeline" id="incidentTimeline"></div>
    </div>
  </div>
</div>
<script>
// ============================================================
// DATA
// ============================================================
const SLO_SERVICES = [
  {name:'api-gateway',        target:99.90, window:'24h', attainment:99.52, budgetPct:87.3, burnRate:2.1, trend:'down', color:'#f85149'},
  {name:'user-service',       target:99.95, window:'7d',  attainment:99.91, budgetPct:92.0, burnRate:0.8, trend:'up',   color:'#3fb950'},
  {name:'payment-processor',  target:99.99, window:'30d', attainment:99.97, budgetPct:67.2, burnRate:3.4, trend:'down', color:'#d29922'},
  {name:'inventory-service',  target:99.50, window:'24h', attainment:99.48, budgetPct:96.1, burnRate:0.3, trend:'up',   color:'#3fb950'},
  {name:'notification-svc',   target:99.00, window:'7d',  attainment:99.10, budgetPct:100,  burnRate:0.0, trend:'flat', color:'#8b949e'},
  {name:'search-indexer',     target:99.90, window:'24h', attainment:98.70, budgetPct:12.4, burnRate:8.7, trend:'down', color:'#f85149'},
];
const DEPENDENCIES = [
  {name:'api-gateway',     level:0, status:'degraded', latency:'42ms', cascade:false},
  {name:'user-service',    level:1, status:'healthy',  latency:'12ms', cascade:false},
  {name:'payment-processor',level:1,status:'degraded', latency:'89ms', cascade:true},
  {name:'inventory-service',level:2,status:'healthy',  latency:'8ms',  cascade:false},
  {name:'fulfillment-svc', level:2, status:'down',     latency:'—',    cascade:true},
  {name:'search-indexer',  level:1, status:'down',     latency:'—',    cascade:true},
  {name:'notification-svc',level:2, status:'healthy',  latency:'15ms', cascade:false},
  {name:'cache-layer',     level:3, status:'healthy',  latency:'1ms',  cascade:false},
  {name:'db-primary',      level:3, status:'degraded', latency:'34ms', cascade:false},
  {name:'db-replica',      level:3, status:'healthy',  latency:'3ms',  cascade:false},
];
const INCIDENTS = [
  {time:'2026-06-25 14:32', title:'search-indexer OOM crash loop',     desc:'Pod restarted 12x in 8 min. Rolling restart deployed.',     severity:'p0', status:'resolved'},
  {time:'2026-06-25 18:15', title:'payment timeout spike',             desc:'p95 latency 1.2s. DB connection pool exhausted.',           severity:'p1', status:'resolved'},
  {time:'2026-06-26 02:00', title:'fulfillment-svc partial outage',    desc:'AZ-west region degraded. Traffic shifted to AZ-east.',      severity:'p1', status:'ongoing'},
  {time:'2026-06-26 07:30', title:'api-gateway error rate elevation',  desc:'5xx rate 2.3%. Upstream timeout from payment-processor.',    severity:'p2', status:'ongoing'},
];
const SEVERITIES = ['critical','high','medium','low','none'];
function randHeat() {
  // 24h x 4 severity columns
  const grid = [];
  for(let h=0;h<24;h++){
    const row=[];
    for(let s=0;s<4;s++){
      const v=Math.random();
      if(v>0.85) row.push('critical');
      else if(v>0.70) row.push('high');
      else if(v>0.50) row.push('medium');
      else if(v>0.25) row.push('low');
      else row.push('none');
    }
    grid.push(row);
  }
  return grid;
}
function genLatencyData(base, jitter) {
  const points=[];
  for(let i=0;i<48;i++){
    const v = base + (Math.random()-0.5)*jitter;
    points.push(Math.max(1, Math.round(v*10)/10));
  }
  return points;
}
const LATENCY = {
  p50: genLatencyData(45, 20),
  p95: genLatencyData(120, 50),
  p99: genLatencyData(250, 100),
};
// ============================================================
// GAUGE
// ============================================================
function updateGauge(pct) {
  const circumference = 534; // 2*pi*85
  const offset = circumference - (pct/100)*circumference;
  const arc = document.getElementById('budgetArc');
  const text = document.getElementById('budgetText');
  const pctEl = document.getElementById('budgetPct');
  arc.style.strokeDashoffset = offset;
  text.textContent = pct.toFixed(1)+'%';
  pctEl.textContent = pct.toFixed(1)+'%';
  // color
  if(pct>50){text.style.fill='#3fb950';pctEl.style.color='#3fb950'}
  else if(pct>20){text.style.fill='#d29922';pctEl.style.color='#d29922'}
  else {text.style.fill='#f85149';pctEl.style.color='#f85149'}
}
// ============================================================
// SLO TABLE
// ============================================================
function renderSLOTable() {
  const tbody = document.getElementById('sloTableBody');
  tbody.innerHTML = SLO_SERVICES.map(s => {
    const pct = s.attainment;
    const barColor = pct >= s.target ? '#3fb950' : (pct >= s.target-0.5 ? '#d29922' : '#f85149');
    const budgetBarColor = s.budgetPct > 50 ? '#3fb950' : (s.budgetPct > 20 ? '#d29922' : '#f85149');
    const arrow = s.trend==='up' ? '\u2191' : (s.trend==='down' ? '\u2193' : '\u2192');
    return `<tr>
      <td style="font-weight:500">${s.name}</td>
      <td>${s.target.toFixed(2)}%</td>
      <td>${s.window}</td>
      <td>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="slo-attainment" style="color:${barColor}">${pct.toFixed(2)}%</span>
          <span style="font-size:14px;color:${s.color}">${arrow}</span>
        </div>
      </td>
      <td>
        <div style="display:flex;align-items:center;gap:6px">
          <div class="slo-bar"><div class="slo-bar-fill" style="width:${Math.min(100,s.budgetPct)}%;background:${budgetBarColor}"></div></div>
          <span class="slo-budget">${s.budgetPct.toFixed(1)}%</span>
        </div>
      </td>
      <td style="font-size:12px;color:${s.color}">${s.burnRate.toFixed(1)}x</td>
    </tr>`;
  }).join('');
}
// ============================================================
// LATENCY CHARTS
// ============================================================
const chartInstances = {};
function buildLatencyCharts() {
  const commonOpts = {
    type:'line',
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{enabled:true,mode:'index',intersect:false}},
      scales:{
        x:{display:false,grid:{display:false}},
        y:{display:false,grid:{display:false},beginAtZero:true}
      },
      elements:{point:{radius:0},line:{borderWidth:2,tension:0.3}},
      animation:{duration:500}
    }
  };
  const colorMap = {p50:'#58a6ff', p95:'#d29922', p99:'#bc8cff'};
  const labels = Array.from({length:48},(_,i)=>i*30+'m ago');
  ['p50','p95','p99'].forEach(key => {
    const ctx = document.getElementById('latency'+key.toUpperCase()).getContext('2d');
    const data = LATENCY[key];
    const max = Math.max(...data);
    const current = data[data.length-1];
    const threshold200 = data.filter(v=>v>200).length;
    document.getElementById('latencyCurrent').textContent = current.toFixed(1)+'ms';
    document.getElementById('latencyMax').textContent = max.toFixed(1)+'ms';
    document.getElementById('latencyBreach').textContent = threshold200;
    chartInstances[key] = new Chart(ctx, {
      ...commonOpts,
      data:{
        labels,
        datasets:[
          {
            data,
            borderColor:colorMap[key],
            backgroundColor:colorMap[key]+'22',
            fill:true,
          },
          // SLO threshold line at 200ms
          {
            data: labels.map(()=>200),
            borderColor:'#f8514966',
            borderWidth:1,
            borderDash:[5,5],
            pointRadius:0,
            fill:false,
          }
        ]
      }
    });
  });
}
// ============================================================
// HEATMAP
// ============================================================
function renderHeatmap() {
  const grid = document.getElementById('heatmapGrid');
  const data = randHeat();
  let html = '<div class="heatmap-header"></div>';
  for(let h=0;h<24;h++){
    html += `<div class="heatmap-header">${h.toString().padStart(2,'0')}:00</div>`;
  }
  const sevLabels = ['Critical','High','Medium','Low'];
  sevLabels.forEach((label, sIdx) => {
    html += `<div class="heatmap-label">${label}</div>`;
    for(let h=0;h<24;h++){
      const cls = data[h] ? data[h][sIdx] || 'none' : 'none';
      html += `<div class="heatmap-cell ${cls}" title="${label} at ${h}:00"></div>`;
    }
  });
  grid.innerHTML = html;
}
// ============================================================
// DEPENDENCY TREE
// ============================================================
function renderDependencyTree() {
  const el = document.getElementById('depTree');
  el.innerHTML = DEPENDENCIES.map(d => {
    const cascadeHtml = d.cascade ? '<span class="dep-cascade">cascading</span>' : '';
    return `<div class="dep-node level-${d.level}">
      <span class="dep-status ${d.status}"></span>
      <span class="dep-name">${d.name}</span>
      ${cascadeHtml}
      <span class="dep-latency">${d.latency}</span>
    </div>`;
  }).join('');
}
// ============================================================
// INCIDENT TIMELINE
// ============================================================
function renderIncidents() {
  const el = document.getElementById('incidentTimeline');
  el.innerHTML = INCIDENTS.map(inc => {
    return `<div class="incident-item ${inc.status}">
      <div class="incident-time">${inc.time}</div>
      <div class="incident-title">${inc.title}</div>
      <div class="incident-desc">${inc.desc}</div>
      <div><span class="incident-tag ${inc.severity}">${inc.severity.toUpperCase()}</span> <span style="font-size:10px;color:#8b949e">${inc.status}</span></div>
    </div>`;
  }).join('');
}
// ============================================================
// BURN-DOWN CHART
// ============================================================
function buildBurndownChart() {
  const ctx = document.getElementById('burndownChart').getContext('2d');
  const labels = Array.from({length:24},(_,i)=>i+':00');
  const budget = Array.from({length:24},(_,i)=>{
    const decay = 100 - (i * (12.4/24));
    const noise = (Math.random()-0.5)*5;
    return Math.max(0, Math.round((decay+noise)*10)/10);
  });
  // Mark incident times
  const incidentMarkers = [
    {time:14, label:'OOM'},
    {time:18, label:'timeout'},
    {time:2, label:'outage'},
    {time:7, label:'5xx'},
  ];
  chartInstances.burndown = new Chart(ctx, {
    type:'line',
    data:{
      labels,
      datasets:[
        {
          label:'Budget Remaining %',
          data:budget,
          borderColor:'#58a6ff',
          backgroundColor:'#58a6ff22',
          fill:true,
          tension:0.4,
          pointRadius:3,
          pointBackgroundColor:ctx=>{
            const idx = ctx.dataIndex;
            const marker = incidentMarkers.find(m=>m.time===idx);
            return marker ? '#f85149' : '#58a6ff';
          },
          pointBorderColor:ctx=>{
            const idx = ctx.dataIndex;
            const marker = incidentMarkers.find(m=>m.time===idx);
            return marker ? '#f85149' : '#58a6ff';
          },
          pointRadius:ctx=>{
            const idx = ctx.dataIndex;
            return incidentMarkers.find(m=>m.time===idx) ? 6 : 3;
          },
        }
      ]
    },
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{
        legend:{display:false},
        tooltip:{
          callbacks:{
            afterLabel:function(ctx){
              const idx = ctx.dataIndex;
              const marker = incidentMarkers.find(m=>m.time===idx);
              return marker ? 'Incident: '+marker.label : '';
            }
          }
        }
      },
      scales:{
        x:{grid:{color:'#21262d'},ticks:{color:'#8b949e',font:{size:10}}},
        y:{grid:{color:'#21262d'},ticks:{color:'#8b949e',font:{size:10}},beginAtZero:true,max:100}
      },
      elements:{point:{hoverRadius:6}}
    }
  });
}
// ============================================================
// INIT
// ============================================================
updateGauge(87.3);
renderSLOTable();
buildLatencyCharts();
renderHeatmap();
renderDependencyTree();
renderIncidents();
buildBurndownChart();
</script>
</body>
</html>
```