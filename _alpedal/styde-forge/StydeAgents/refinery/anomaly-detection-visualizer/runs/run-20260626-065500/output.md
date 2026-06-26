```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Detection Visualizer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
.dash{display:grid;grid-template-columns:1fr 380px;grid-template-rows:auto 280px auto;gap:12px;padding:16px;max-width:1600px;margin:0 auto;min-height:100vh}
.header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:8px 16px;background:#111827;border:1px solid #1e293b;border-radius:8px}
.header h1{font-size:18px;font-weight:600;color:#e2e8f0;letter-spacing:0.5px}
.header h1 span{color:#f59e0b}
.status-bar{display:flex;gap:16px;font-size:13px;color:#94a3b8}
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;animation:pulse-dot 2s infinite}
.status-dot.green{background:#22c55e}
.status-dot.yellow{background:#eab308}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:0.4}}
.main-chart{grid-column:1;grid-row:2;background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px;position:relative;min-height:400px}
.main-chart h2{font-size:13px;font-weight:500;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px}
#metricChart{width:100%;height:340px;display:block}
.anomaly-count{position:absolute;top:12px;right:12px;font-size:12px;color:#94a3b8;background:#1e293b;padding:4px 10px;border-radius:4px}
.anomaly-count b{color:#ef4444}
.sidebar{grid-column:2;grid-row:2;display:flex;flex-direction:column;gap:12px}
.panel{background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px;flex:1}
.panel h3{font-size:12px;font-weight:500;color:#64748b;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.heatmap{grid-column:1/2;grid-row:3;background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px;min-height:240px}
.heatmap h2{font-size:13px;font-weight:500;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px}
#heatmapCanvas{width:100%;height:200px;display:block}
.drift-panel{grid-column:2;grid-row:3;background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px}
.drift-panel h2{font-size:13px;font-weight:500;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px}
#driftChart{width:100%;height:180px;display:block}
.root-cause{background:#111827;border:1px solid #1e293b;border-radius:8px;padding:12px;margin-top:0}
.root-cause h3{font-size:12px;font-weight:500;color:#64748b;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.cause-chain{display:flex;flex-direction:column;gap:4px}
.cause-item{display:flex;align-items:center;gap:6px;font-size:12px;padding:4px 8px;background:#1e293b;border-radius:4px;border-left:3px solid #64748b}
.cause-item.critical{border-left-color:#ef4444}
.cause-item.warning{border-left-color:#eab308}
.cause-item .metric-name{color:#e2e8f0;font-weight:500}
.cause-item .corr-val{color:#94a3b8;font-size:11px}
.cause-item .arrow{color:#64748b;margin:0 4px}
.cause-item .lag{color:#64748b;font-size:10px}
.empty-state{color:#475569;font-size:12px;text-align:center;padding:12px}
.metric-selector{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.metric-tag{font-size:11px;padding:2px 8px;border-radius:3px;background:#1e293b;color:#94a3b8;cursor:pointer;border:1px solid transparent}
.metric-tag.active{border-color:#f59e0b;color:#f59e0b;background:#1e293b}
.metric-tag:hover{background:#334155}
.controls{grid-column:1/-1;display:flex;gap:8px;align-items:center;padding:4px 0}
.controls button{background:#1e293b;border:1px solid #334155;color:#c8d6e5;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px}
.controls button:hover{background:#334155}
.controls button.active{background:#f59e0b;color:#0a0e17;border-color:#f59e0b;font-weight:600}
.controls label{font-size:12px;color:#64748b;margin-left:8px}
.controls input[type=range]{width:120px;accent-color:#f59e0b}
.legend{margin-left:auto;display:flex;gap:12px;font-size:11px;color:#94a3b8}
.legend span{display:flex;align-items:center;gap:4px}
.legend .swatch{width:10px;height:10px;border-radius:2px;display:inline-block}
.tooltip{position:fixed;background:#0f172a;border:1px solid #334155;border-radius:6px;padding:8px 12px;font-size:12px;pointer-events:none;z-index:100;display:none;box-shadow:0 4px 20px rgba(0,0,0,0.5);max-width:260px}
.tooltip .tt-title{color:#e2e8f0;font-weight:500;margin-bottom:4px}
.tooltip .tt-row{color:#94a3b8;display:flex;justify-content:space-between;gap:12px}
.tooltip .tt-val{color:#e2e8f0;font-weight:400}
.heatmap-tooltip{position:fixed;background:#0f172a;border:1px solid #334155;border-radius:6px;padding:6px 10px;font-size:11px;pointer-events:none;z-index:100;display:none;box-shadow:0 4px 12px rgba(0,0,0,0.4)}
</style>
</head>
<body>
<div class="dash">
  <div class="header">
    <h1>anomaly <span>pulse</span> &mdash; real-time detector</h1>
    <div class="status-bar">
      <span><span class="status-dot green"></span>streaming</span>
      <span>alerts: <b id="alertCount" style="color:#ef4444">0</b></span>
      <span>points: <b id="pointCount">0</b></span>
    </div>
  </div>
  <div class="main-chart">
    <h2>metric stream &mdash; cpu utilization</h2>
    <div class="anomaly-count">anomalies: <b id="anomalyBadge">0</b></div>
    <canvas id="metricChart"></canvas>
    <div class="metric-selector" id="metricSelector">
      <span class="metric-tag active" data-m="cpu">cpu</span>
      <span class="metric-tag" data-m="memory">memory</span>
      <span class="metric-tag" data-m="disk_io">disk_io</span>
      <span class="metric-tag" data-m="latency">latency</span>
      <span class="metric-tag" data-m="error_rate">error_rate</span>
    </div>
  </div>
  <div class="sidebar">
    <div class="panel">
      <h3>root cause chain</h3>
      <div id="rootCausePanel"><div class="empty-state">awaiting anomaly detection...</div></div>
    </div>
    <div class="panel">
      <h3>detection controls</h3>
      <div class="controls" style="flex-direction:column;align-items:stretch">
        <div><label>sensitivity</label><input type="range" id="sensitivitySlider" min="1" max="5" value="3" step="0.5"> <span id="sensLabel" style="font-size:12px;color:#94a3b8">3.0</span></div>
        <div style="display:flex;gap:6px;margin-top:4px">
          <button id="btnZscore" class="active">z-score</button>
          <button id="btnIqr">moving IQR</button>
          <button id="btnCp">change-point</button>
          <button id="btnPause">pause</button>
        </div>
      </div>
    </div>
  </div>
  <div class="heatmap">
    <h2>deviation heatmap &mdash; last 20 time slices</h2>
    <canvas id="heatmapCanvas"></canvas>
  </div>
  <div class="drift-panel">
    <h2>drift: prediction vs actual</h2>
    <canvas id="driftChart"></canvas>
  </div>
</div>
<div id="chartTooltip" class="tooltip"></div>
<div id="heatmapTooltip" class="heatmap-tooltip"></div>
<script>
// ---- state ---------------------------------------------------------------
const MAX_POINTS = 200;
const HISTORY = { cpu:[], memory:[], disk_io:[], latency:[], error_rate:[] };
const PREDICTIONS = [];
let activeMetric = 'cpu';
let algorithm = 'zscore';
let sensitivity = 3.0;
let paused = false;
let alertCount = 0;
let time = 0;
let animFrame = null;
let pulseAnomalies = [];
let heatmapData = [];
// ---- metric generators ---------------------------------------------------
function genBaseline(metric) {
  const bases = { cpu:45, memory:62, disk_io:120, latency:35, error_rate:2.1 };
  const noises = { cpu:8, memory:12, disk_io:25, latency:10, error_rate:1.8 };
  const b = bases[metric]||50, n = noises[metric]||10;
  let v = b + (Math.random()-0.5)*n*2;
  // weekly pattern
  const hour = (Date.now()/3600000)%168;
  if(metric==='cpu') v += 15*Math.sin(hour/168*Math.PI*2);
  if(metric==='memory') v += 8*Math.sin((hour+12)/168*Math.PI*2);
  if(metric==='latency') v += 12*Math.sin(hour/84*Math.PI*2);
  return Math.max(0.1, v);
}
function injectAnomaly(metric) {
  const p = Math.random();
  if(p>0.04) return null; // ~4% chance
  const types = ['spike','dip','shift','noise_burst'];
  const t = types[Math.floor(Math.random()*types.length)];
  const spikes = { cpu:[60,85], memory:[75,95], disk_io:[200,400], latency:[80,200], error_rate:[8,25] };
  const dips = { cpu:[5,20], memory:[20,35], disk_io:[30,60], latency:[5,15], error_rate:[0,0.5] };
  const s = spikes[metric]||[80,150];
  const d = dips[metric]||[5,20];
  let val, duration=1;
  if(t==='spike'){ val=s[0]+Math.random()*(s[1]-s[0]); duration=1+Math.floor(Math.random()*3); }
  else if(t==='dip'){ val=d[0]+Math.random()*(d[1]-d[0]); duration=1+Math.floor(Math.random()*2); }
  else if(t==='shift'){ val=genBaseline(metric)+(Math.random()-0.5)*5+20*(Math.random()>0.5?1:-1); duration=3+Math.floor(Math.random()*8); }
  else { val=genBaseline(metric)+(Math.random()-0.5)*40; duration=2+Math.floor(Math.random()*4); }
  return { metric, type:t, value:Math.max(0.1,val), duration, startTime:time };
}
// active anomalies (multi-step)
let activeAnomalies = [];
function getMetricValue(metric) {
  let v = genBaseline(metric);
  // apply active anomalies
  for(let i=activeAnomalies.length-1;i>=0;i--){
    const a=activeAnomalies[i];
    if(a.metric!==metric) continue;
    if(a.expires<=time){ activeAnomalies.splice(i,1); continue; }
    if(a.type==='shift') v=genBaseline(metric)+a.offset;
    else if(a.type==='noise_burst') v+= (Math.random()-0.5)*40;
    else v=a.value;
  }
  // inject new anomalies (only on main metric for simplicity)
  if(metric===activeMetric){
    const newA = injectAnomaly(metric);
    if(newA){
      let val;
      if(newA.type==='shift'){ val=genBaseline(metric); newA.offset=genBaseline(metric)*0.3*(Math.random()>0.5?1:-1); }
      else val=newA.value;
      activeAnomalies.push({...newA, expires:time+newA.duration, offset:newA.offset||0, value:val});
    }
  }
  return v;
}
// ---- detection algorithms -------------------------------------------------
function detectZscore(data, window=20) {
  if(data.length<window+2) return [];
  const slice = data.slice(-window);
  const recent = data.slice(-(window+5));
  const mean = slice.reduce((a,b)=>a+b,0)/slice.length;
  const std = Math.sqrt(slice.reduce((a,b)=>a+(b-mean)**2,0)/slice.length)||1;
  const threshold = 1.0 + sensitivity*0.5;
  const out = [];
  for(let i=recent.length-1;i>=Math.max(0,recent.length-5);i--){
    const z = Math.abs((recent[i]-mean)/std);
    if(z>threshold) out.push({idx:data.length-(recent.length-i), value:recent[i], zscore:z, severity: z>threshold*1.8?'critical':'warning' });
  }
  return out;
}
function detectIQR(data, window=20) {
  if(data.length<window+2) return [];
  const slice = data.slice(-window).sort((a,b)=>a-b);
  const q1=slice[Math.floor(slice.length*0.25)], q3=slice[Math.floor(slice.length*0.75)];
  const iqr=q3-q1||1;
  const threshold = 0.8 + sensitivity*0.3;
  const recent = data.slice(-5);
  const out = [];
  for(let i=recent.length-1;i>=0;i--){
    const v=recent[i];
    if(v<q1-threshold*iqr||v>q3+threshold*iqr){
      const sev = (v<q1-threshold*1.5*iqr||v>q3+threshold*1.5*iqr)?'critical':'warning';
      out.push({idx:data.length-(recent.length-i), value:v, severity:sev });
    }
  }
  return out;
}
function detectChangepoint(data, window=15) {
  if(data.length<window*2+2) return [];
  const slice = data.slice(-window*2);
  const mid = Math.floor(slice.length/2);
  const first = slice.slice(0,mid), second = slice.slice(mid);
  const m1=first.reduce((a,b)=>a+b,0)/first.length;
  const m2=second.reduce((a,b)=>a+b,0)/second.length;
  const v1=first.reduce((a,b)=>a+(b-m1)**2,0)/first.length||1;
  const v2=second.reduce((a,b)=>a+(b-m2)**2,0)/second.length||1;
  const pooled = Math.sqrt((v1+v2)/2);
  const diff = Math.abs(m1-m2)/pooled;
  const threshold = 1.5 + (sensitivity-1)*0.5;
  if(diff>threshold){
    const sev = diff>threshold*1.6?'critical':'warning';
    return [{idx:data.length-1, value:data[data.length-1], severity:sev, cpStat:diff }];
  }
  return [];
}
function detect(metric) {
  const data = HISTORY[metric]||[];
  if(data.length<10) return [];
  switch(algorithm){
    case 'zscore': return detectZscore(data);
    case 'iqr': return detectIQR(data);
    case 'changepoint': return detectChangepoint(data);
    default: return detectZscore(data);
  }
}
// ---- root cause suggestion ------------------------------------------------
function suggestRootCause(mainMetric, anomalyTime) {
  const candidates = Object.keys(HISTORY).filter(m=>m!==mainMetric);
  const results = [];
  for(const m of candidates){
    const d = HISTORY[m];
    if(!d||d.length<10) continue;
    const recent = d.slice(-10);
    const mean = recent.reduce((a,b)=>a+b,0)/recent.length;
    const prev = d.slice(-20,-10);
    const pmean = prev.reduce((a,b)=>a+b,0)/prev.length||1;
    const pctChange = ((mean-pmean)/pmean)*100;
    if(Math.abs(pctChange)>5){
      const corr = Math.min(100, Math.abs(pctChange)*3);
      const lag = 1+Math.floor(Math.random()*3);
      const dir = pctChange>0?'spike':'dip';
      results.push({ metric:m, change:Math.round(pctChange*10)/10, direction:dir, correlation:Math.round(corr), lag });
    }
  }
  results.sort((a,b)=>b.correlation-a.correlation);
  return results.slice(0,4);
}
// ---- tick -----------------------------------------------------------------
function tick() {
  if(paused) { animFrame = requestAnimationFrame(tick); return; }
  time++;
  const v = getMetricValue(activeMetric);
  HISTORY[activeMetric].push(v);
  // maintain other metrics
  for(const m of Object.keys(HISTORY)){
    if(m===activeMetric) continue;
    HISTORY[m].push(getMetricValue(m));
    if(HISTORY[m].length>MAX_POINTS) HISTORY[m].splice(0, HISTORY[m].length-MAX_POINTS);
  }
  // prediction for drift (simple trailing average)
  const pd = HISTORY[activeMetric];
  if(pd.length>=10){
    const pred = pd.slice(-10).reduce((a,b)=>a+b,0)/10 + (Math.random()-0.5)*3;
    PREDICTIONS.push({ actual:v, prediction:pred, time });
    if(PREDICTIONS.length>MAX_POINTS) PREDICTIONS.splice(0, PREDICTIONS.length-MAX_POINTS);
  }
  // detection
  const anomalies = detect(activeMetric);
  for(const a of anomalies){
    if(a.severity==='critical'){
      alertCount++;
      pulseAnomalies.push({ x:0, y:0, radius:8, opacity:1, time:Date.now(), severity:'critical', value:a.value, zscore:a.zscore||0 });
      // push heatmap slice
      const slice = {};
      for(const m of Object.keys(HISTORY)){
        const d = HISTORY[m];
        if(d&&d.length>0) slice[m]=d[d.length-1];
      }
      slice._time=time;
      heatmapData.push(slice);
      if(heatmapData.length>30) heatmapData.splice(0, heatmapData.length-30);
    }
  }
  if(HISTORY[activeMetric].length>MAX_POINTS) HISTORY[activeMetric].splice(0, HISTORY[activeMetric].length-MAX_POINTS);
  render();
  animFrame = requestAnimationFrame(tick);
}
// ---- rendering ------------------------------------------------------------
function render() {
  renderMainChart();
  renderHeatmap();
  renderDrift();
  updateUI();
}
function renderMainChart() {
  const c = document.getElementById('metricChart');
  const rect = c.parentElement.getBoundingClientRect();
  const W = c.width = c.clientWidth * (window.devicePixelRatio||1);
  const H = c.height = 340 * (window.devicePixelRatio||1);
  const ctx = c.getContext('2d');
  const dpr = window.devicePixelRatio||1;
  ctx.scale(dpr,dpr);
  const w = c.clientWidth, h = 340;
  ctx.clearRect(0,0,w,h);
  const pad = { t:20, r:20, b:30, l:50 };
  const pw = w-pad.l-pad.r, ph = h-pad.t-pad.b;
  const data = HISTORY[activeMetric]||[];
  if(data.length<2) return;
  const min=Math.max(0,Math.min(...data)*0.8), max=Math.max(...data)*1.1;
  const range = max-min||1;
  function x(i){ return pad.l + (i/(data.length-1||1))*pw; }
  function y(v){ return pad.t + ph - ((v-min)/range)*ph; }
  // threshold bands (dynamic)
  const recentSlice = data.slice(-20);
  const mean = recentSlice.reduce((a,b)=>a+b,0)/recentSlice.length;
  const std = Math.sqrt(recentSlice.reduce((a,b)=>a+(b-mean)**2,0)/recentSlice.length)||range*0.05;
  const bandWidth = (0.5 + sensitivity*0.4)*std;
  const upper = mean+bandWidth*2;
  const lower = mean-bandWidth*2;
  // band fill
  ctx.beginPath();
  for(let i=0;i<data.length;i++) ctx.lineTo(x(i), y(upper));
  for(let i=data.length-1;i>=0;i--) ctx.lineTo(x(i), y(Math.max(0,lower)));
  ctx.closePath();
  ctx.fillStyle = 'rgba(34,197,94,0.08)';
  ctx.fill();
  // threshold lines
  ctx.strokeStyle = 'rgba(34,197,94,0.3)';
  ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(pad.l, y(upper)); ctx.lineTo(w-pad.r, y(upper)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(pad.l, y(lower)); ctx.lineTo(w-pad.r, y(lower)); ctx.stroke();
  ctx.setLineDash([]);
  // metric line
  ctx.beginPath();
  ctx.strokeStyle = '#3b82f6';
  ctx.lineWidth=2;
  for(let i=0;i<data.length;i++){
    if(i===0) ctx.moveTo(x(i), y(data[i]));
    else ctx.lineTo(x(i), y(data[i]));
  }
  ctx.stroke();
  // gradient fill under line
  ctx.beginPath();
  ctx.moveTo(pad.l, h-pad.b);
  for(let i=0;i<data.length;i++) ctx.lineTo(x(i), y(data[i]));
  ctx.lineTo(x(data.length-1), h-pad.b);
  ctx.closePath();
  const grad = ctx.createLinearGradient(0,pad.t,0,h-pad.b);
  grad.addColorStop(0,'rgba(59,130,246,0.15)');
  grad.addColorStop(1,'rgba(59,130,246,0.01)');
  ctx.fillStyle = grad;
  ctx.fill();
  // anomalies
  const anoms = detect(activeMetric);
  for(const a of anoms){
    const idx = a.idx;
    const i = idx - (data.length - data.length);
    if(i<0||i>=data.length) continue;
    const cx = x(i), cy = y(a.value);
    const r = a.severity==='critical'?7:4;
    // glow
    const glow = ctx.createRadialGradient(cx,cy,0,cx,cy,r*3);
    if(a.severity==='critical'){
      glow.addColorStop(0,'rgba(239,68,68,0.4)');
      glow.addColorStop(1,'rgba(239,68,68,0)');
    } else {
      glow.addColorStop(0,'rgba(234,179,8,0.3)');
      glow.addColorStop(1,'rgba(234,179,8,0)');
    }
    ctx.fillStyle = glow;
    ctx.beginPath(); ctx.arc(cx,cy,r*3,0,Math.PI*2); ctx.fill();
    // point
    ctx.fillStyle = a.severity==='critical'?'#ef4444':'#eab308';
    ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth=1;
    ctx.stroke();
    // pulse ring animation
    const pulsePhase = (Date.now()%2000)/2000;
    const pulseR = r + pulsePhase*15;
    ctx.strokeStyle = a.severity==='critical'?`rgba(239,68,68,${0.5-pulsePhase*0.4})`:`rgba(234,179,8,${0.4-pulsePhase*0.35})`;
    ctx.lineWidth=2;
    ctx.beginPath(); ctx.arc(cx,cy,pulseR,0,Math.PI*2); ctx.stroke();
  }
  // axes
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(pad.l,pad.t); ctx.lineTo(pad.l,h-pad.b); ctx.lineTo(w-pad.r,h-pad.b); ctx.stroke();
  ctx.fillStyle = '#475569'; ctx.font='10px sans-serif'; ctx.textAlign='right';
  for(let i=0;i<=4;i++){
    const val = min + (range/4)*i;
    const yy = pad.t + ph - (i/4)*ph;
    ctx.fillText(Math.round(val)+'%', pad.l-6, yy+3);
    ctx.strokeStyle='rgba(30,41,59,0.5)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(pad.l-3,yy); ctx.lineTo(w-pad.r,yy); ctx.stroke();
  }
}
function renderHeatmap() {
  const c = document.getElementById('heatmapCanvas');
  const W = c.width = c.clientWidth * (window.devicePixelRatio||1);
  const H = c.height = 200 * (window.devicePixelRatio||1);
  const ctx = c.getContext('2d');
  const dpr = window.devicePixelRatio||1;
  ctx.scale(dpr,dpr);
  const w = c.clientWidth, h = 200;
  ctx.clearRect(0,0,w,h);
  const metrics = ['cpu','memory','disk_io','latency','error_rate'];
  const rows = metrics.length;
  const cols = 20;
  const cellW = (w-60)/cols, cellH = (h-30)/rows;
  if(cellW<1||cellH<1) return;
  // compute mean/std per metric for z-score
  const stats = {};
  for(const m of metrics){
    const d = HISTORY[m]||[];
    if(d.length<2) { stats[m]={mean:50,std:10}; continue; }
    const mean = d.reduce((a,b)=>a+b,0)/d.length;
    const std = Math.sqrt(d.reduce((a,b)=>a+(b-mean)**2,0)/d.length)||1;
    stats[m]={mean,std};
  }
  // last 20 time slices
  const sliceCount = Math.min(cols, heatmapData.length);
  const startIdx = Math.max(0, heatmapData.length-cols);
  for(let r=0;r<rows;r++){
    const m = metrics[r];
    const s = stats[m];
    for(let c2=0;c2<sliceCount;c2++){
      const di = startIdx + c2;
      if(di>=heatmapData.length) continue;
      const val = heatmapData[di][m];
      if(val===undefined) continue;
      const z = (val-s.mean)/s.std;
      const az = Math.abs(z);
      let color;
      if(az<1.5) color='#0f172a';
      else if(az<2.5) {
        const t = (az-1.5)/1.0;
        color = lerpColor('#0f172a','#eab308',t);
      } else if(az<3.5){
        const t = (az-2.5)/1.0;
        color = lerpColor('#eab308','#ef4444',t);
      } else {
        const t = Math.min(1,(az-3.5)/1.5);
        color = lerpColor('#ef4444','#7f1d1d',t);
      }
      const x = 50 + c2*cellW;
      const y = 10 + r*cellH;
      ctx.fillStyle = color;
      ctx.fillRect(x,y,cellW-1,cellH-1);
      // severity dot
      if(az>2.5){
        ctx.fillStyle = az>3.5?'#ef4444':'#eab308';
        ctx.beginPath();
        ctx.arc(x+cellW/2, y+cellH-4, 2, 0, Math.PI*2);
        ctx.fill();
      }
    }
  }
  // labels
  ctx.fillStyle='#64748b'; ctx.font='10px sans-serif'; ctx.textAlign='right';
  for(let r=0;r<rows;r++){
    ctx.fillText(metrics[r], 44, 10+r*cellH+cellH/2+3);
  }
}
function lerpColor(c1,c2,t){
  const r1=parseInt(c1.slice(1,3),16), g1=parseInt(c1.slice(3,5),16), b1=parseInt(c1.slice(5,7),16);
  const r2=parseInt(c2.slice(1,3),16), g2=parseInt(c2.slice(3,5),16), b2=parseInt(c2.slice(5,7),16);
  const r=Math.round(r1+(r2-r1)*t), g=Math.round(g1+(g2-g1)*t), b=Math.round(b1+(b2-b1)*t);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}
function renderDrift() {
  const c = document.getElementById('driftChart');
  const W = c.width = c.clientWidth * (window.devicePixelRatio||1);
  const H = c.height = 180 * (window.devicePixelRatio||1);
  const ctx = c.getContext('2d');
  const dpr = window.devicePixelRatio||1;
  ctx.scale(dpr,dpr);
  const w = c.clientWidth, h = 180;
  ctx.clearRect(0,0,w,h);
  const pad = {t:10,r:10,b:20,l:35};
  const pw = w-pad.l-pad.r, ph = h-pad.t-pad.b;
  const data = PREDICTIONS;
  if(data.length<3) return;
  const allVals = data.flatMap(d=>[d.actual,d.prediction]);
  const min = Math.max(0,Math.min(...allVals)*0.9);
  const max = Math.max(...allVals)*1.1;
  const range = max-min||1;
  function x(i){ return pad.l + (i/(data.length-1||1))*pw; }
  function y(v){ return pad.t + ph - ((v-min)/range)*ph; }
  // drift gap fill
  for(let i=1;i<data.length;i++){
    const aPrev=data[i-1], aCur=data[i];
    const diff = aCur.actual - aCur.prediction;
    const absDiff = Math.abs(diff);
    const threshold = range*0.05*(1+(sensitivity-1)*0.2);
    const color = absDiff<threshold?'rgba(34,197,94,0.15)':'rgba(239,68,68,0.2)';
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x(i-1), y(aPrev.actual));
    ctx.lineTo(x(i), y(aCur.actual));
    ctx.lineTo(x(i), y(aCur.prediction));
    ctx.lineTo(x(i-1), y(aPrev.prediction));
    ctx.closePath();
    ctx.fill();
  }
  // prediction line
  ctx.beginPath();
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
  for(let i=0;i<data.length;i++){
    if(i===0) ctx.moveTo(x(i), y(data[i].prediction));
    else ctx.lineTo(x(i), y(data[i].prediction));
  }
  ctx.stroke();
  ctx.setLineDash([]);
  // actual line
  ctx.beginPath();
  ctx.strokeStyle = '#3b82f6';
  ctx.lineWidth=2;
  for(let i=0;i<data.length;i++){
    if(i===0) ctx.moveTo(x(i), y(data[i].actual));
    else ctx.lineTo(x(i), y(data[i].actual));
  }
  ctx.stroke();
  // axes
  ctx.strokeStyle='#1e293b';
  ctx.beginPath(); ctx.moveTo(pad.l,pad.t); ctx.lineTo(pad.l,h-pad.b); ctx.lineTo(w-pad.r,h-pad.b); ctx.stroke();
  ctx.fillStyle='#475569'; ctx.font='9px sans-serif';
  ctx.textAlign='right';
  for(let i=0;i<=3;i++){
    const val = min+(range/3)*i;
    ctx.fillText(Math.round(val)+'%', pad.l-4, pad.t+ph-(i/3)*ph+3);
  }
  ctx.textAlign='center';
  ctx.fillStyle='#475569'; ctx.font='9px sans-serif';
  ctx.fillText('prediction (dashed) vs actual', w/2, h-4);
}
function updateUI() {
  document.getElementById('alertCount').textContent = alertCount;
  document.getElementById('anomalyBadge').textContent = detect(activeMetric).filter(a=>a.severity==='critical').length||'0';
  document.getElementById('pointCount').textContent = HISTORY[activeMetric].length;
  // root cause
  const lastAnoms = detect(activeMetric).filter(a=>a.severity==='critical');
  const panel = document.getElementById('rootCausePanel');
  if(lastAnoms.length>0){
    const causes = suggestRootCause(activeMetric, time);
    if(causes.length>0){
      panel.innerHTML = '<div class="cause-chain">' +
        causes.map((c,i)=>{
          const level = c.correlation>60?'critical':c.correlation>30?'warning':'';
          return `<div class="cause-item ${level}">
            <span class="metric-name">${c.metric}</span>
            <span class="arrow">→</span>
            <span style="color:${c.direction==='spike'?'#ef4444':'#3b82f6'}">${c.direction==='spike'?'↑':'↓'}${Math.abs(c.change)}%</span>
            <span class="corr-val">corr:${c.correlation}%</span>
            <span class="lag">lag:${c.lag}s</span>
          </div>`;
        }).join('') + '</div>';
    } else {
      panel.innerHTML = '<div class="empty-state">anomaly detected — insufficient correlated metric history</div>';
    }
  } else {
    panel.innerHTML = '<div class="empty-state">awaiting anomaly detection...</div>';
  }
}
// ---- controls -------------------------------------------------------------
document.getElementById('sensitivitySlider').addEventListener('input', function(){
  sensitivity = parseFloat(this.value);
  document.getElementById('sensLabel').textContent = sensitivity.toFixed(1);
});
document.getElementById('btnZscore').addEventListener('click', function(){
  algorithm='zscore';
  document.querySelectorAll('.controls button:not(#btnPause)').forEach(b=>b.classList.remove('active'));
  this.classList.add('active');
});
document.getElementById('btnIqr').addEventListener('click', function(){
  algorithm='iqr';
  document.querySelectorAll('.controls button:not(#btnPause)').forEach(b=>b.classList.remove('active'));
  this.classList.add('active');
});
document.getElementById('btnCp').addEventListener('click', function(){
  algorithm='changepoint';
  document.querySelectorAll('.controls button:not(#btnPause)').forEach(b=>b.classList.remove('active'));
  this.classList.add('active');
});
document.getElementById('btnPause').addEventListener('click', function(){
  paused=!paused;
  this.textContent = paused?'resume':'pause';
  this.classList.toggle('active');
});
document.querySelectorAll('.metric-tag').forEach(tag => {
  tag.addEventListener('click', function(){
    document.querySelectorAll('.metric-tag').forEach(t=>t.classList.remove('active'));
    this.classList.add('active');
    activeMetric = this.dataset.m;
  });
});
// ---- resize handler -------------------------------------------------------
window.addEventListener('resize', ()=>{
  renderMainChart();
  renderHeatmap();
  renderDrift();
});
// ---- start ----------------------------------------------------------------
tick();
</script>
</body>
</html>
```