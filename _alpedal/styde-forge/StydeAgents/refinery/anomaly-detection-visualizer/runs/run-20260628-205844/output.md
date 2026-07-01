```
anomaly-dashboard.html
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anomaly Pulse — Real-time Monitoring</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}
body{background:#0b0e14;color:#e0e6ed;padding:20px;min-height:100vh}
.dashboard{display:grid;grid-template-columns:300px 1fr 1fr;grid-template-rows:auto auto auto;gap:16px;max-width:1440px;margin:0 auto}
.card{background:#131820;border:1px solid #1e293b;border-radius:12px;padding:16px;overflow:hidden}
.card h2{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:#64748b;margin-bottom:12px}
/* pulse ring */
.pulse-ring{width:12px;height:12px;border-radius:50%;background:#ef4444;position:relative;display:inline-block}
.pulse-ring::before,.pulse-ring::after{content:'';position:absolute;inset:-4px;border-radius:50%;border:2px solid #ef4444;animation:pulse-expand 2s ease-out infinite;opacity:0}
.pulse-ring::after{animation-delay:1s}
@keyframes pulse-expand{0%{transform:scale(.5);opacity:1}100%{transform:scale(3);opacity:0}}
.pulse-ring.severity-high{background:#ef4444;box-shadow:0 0 12px #ef4444}
.pulse-ring.severity-medium{background:#f59e0b;box-shadow:0 0 10px #f59e0b}
.pulse-ring.severity-low{background:#3b82f6;box-shadow:0 0 8px #3b82f6}
/* webkit fallback — caps at 6 layers */
@media screen and (-webkit-min-device-pixel-ratio:0){
  .pulse-ring.severity-high{-webkit-box-shadow:0 0 8px #ef4444,0 0 16px rgba(239,68,68,.6),0 0 24px rgba(239,68,68,.4),0 0 32px rgba(239,68,68,.2),0 0 40px rgba(239,68,68,.1);outline:2px solid rgba(239,68,68,.3);outline-offset:6px}
  .pulse-ring.severity-medium{-webkit-box-shadow:0 0 8px #f59e0b,0 0 16px rgba(245,158,11,.6),0 0 24px rgba(245,158,11,.4),0 0 32px rgba(245,158,11,.2),0 0 40px rgba(245,158,11,.1);outline:2px solid rgba(245,158,11,.3);outline-offset:6px}
  .pulse-ring.severity-low{-webkit-box-shadow:0 0 8px #3b82f6,0 0 16px rgba(59,130,246,.6),0 0 24px rgba(59,130,246,.4),0 0 32px rgba(59,130,246,.2),0 0 40px rgba(59,130,246,.1);outline:2px solid rgba(59,130,246,.3);outline-offset:6px}
}
/* heatmap */
.heatmap-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:2px}
.heatmap-cell{aspect-ratio:1;border-radius:3px;position:relative;min-width:20px;transition:transform .15s}
.heatmap-cell:hover{transform:scale(1.8);z-index:10}
.heatmap-cell .tooltip{display:none;position:absolute;bottom:100%;left:50%;transform:translateX(-50%);background:#1e293b;color:#e0e6ed;padding:4px 8px;border-radius:4px;font-size:11px;white-space:nowrap;z-index:20}
.heatmap-cell:hover .tooltip{display:block}
.heatmap-cell.severity-high{background:#ef4444}
.heatmap-cell.severity-medium{background:#f59e0b}
.heatmap-cell.severity-low{background:#3b82f6}
.heatmap-cell.normal{background:#1e293b}
.heatmap-cell.awaiting{background:#0f172a;border:1px dashed #334155}
/* drift chart */
.drift-chart{position:relative;height:120px;margin-top:8px}
.drift-line{position:absolute;bottom:0;left:0;right:0;height:100%;display:flex;align-items:flex-end}
.drift-bar{flex:1;margin:0 1px;border-radius:2px 2px 0 0;min-height:2px;transition:background .3s,height .3s}
.drift-bar.prediction{background:#6366f1;opacity:.7}
.drift-bar.actual{background:#22c55e;opacity:.9}
.drift-bar.diverging{background:#ef4444;opacity:.8}
.drift-bar.gap{background:transparent;border-top:2px dashed #64748b;min-height:0;position:relative}
.drift-bar.gap::after{content:'Data gap — interpolation paused';position:absolute;top:-16px;left:50%;transform:translateX(-50%);font-size:9px;color:#94a3b8;white-space:nowrap}
.drift-threshold{position:absolute;left:0;right:0;border-top:1px dashed rgba(239,68,68,.3);z-index:5}
/* alert feed */
.alert-feed{max-height:400px;overflow-y:auto}
.alert-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #1e293b;font-size:13px}
.alert-item:last-child{border-bottom:none}
.alert-meta{color:#64748b;font-size:11px;white-space:nowrap}
.alert-chain{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px}
.alert-chain span{background:#1e293b;color:#94a3b8;padding:2px 6px;border-radius:4px;font-size:10px}
.alert-chain .causer{color:#ef4444;background:rgba(239,68,68,.1)}
.alert-chain .linked{color:#f59e0b;background:rgba(245,158,11,.1)}
/* threshold bands */
.threshold-bands{height:40px;position:relative;background:#0f172a;border-radius:6px;margin-top:8px;overflow:hidden}
.threshold-band{position:absolute;bottom:0;background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.2);border-radius:2px;transition:all .3s}
.threshold-line{position:absolute;left:0;right:0;height:1px;background:rgba(99,102,241,.5);z-index:2}
.threshold-label{position:absolute;right:4px;font-size:9px;color:#64748b;transform:translateY(-50%)}
/* status */
.status-bar{display:flex;gap:16px;align-items:center;font-size:12px;color:#94a3b8}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.status-dot.streaming{background:#22c55e;animation:pulse-dot 2s ease-in-out infinite}
.status-dot.gap{background:#f59e0b}
.status-dot.idle{background:#64748b}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.3}}
.placeholder-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:200px;color:#64748b;gap:8px}
.placeholder-state .big-icon{font-size:48px;opacity:.3}
.placeholder-state .label{font-size:14px}
</style>
</head>
<body>
<div class="dashboard">
  <!-- status + alerts column -->
  <div class="card" style="grid-row:1/3">
    <div class="status-bar">
      <span><span class="status-dot streaming"></span> Stream: active</span>
      <span>Points: <span id="pointCount">0</span></span>
      <span>Rate: <span id="streamRate">--</span>/s</span>
    </div>
    <h2 style="margin-top:16px">Active Alerts</h2>
    <div class="alert-feed" id="alertFeed">
      <div style="color:#64748b;font-size:13px;text-align:center;padding:20px 0">Awaiting data stream...</div>
    </div>
    <h2 style="margin-top:16px">Root-cause Chains</h2>
    <div id="causalChain" style="font-size:12px;color:#64748b;padding:8px 0">
      <div style="text-align:center;padding:10px 0">No anomalies detected yet</div>
    </div>
  </div>
  <!-- deviation heatmap -->
  <div class="card" style="grid-column:2/4">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2 style="margin-bottom:0">Deviation Heatmap — Time Slices</h2>
      <span style="font-size:11px;color:#64748b" id="heatmapLabel">last 12 slices</span>
    </div>
    <div class="heatmap-grid" id="heatmapGrid">
      <!-- populated by JS -->
    </div>
    <div style="display:flex;gap:12px;margin-top:8px;font-size:11px;color:#64748b;align-items:center">
      <span><span style="display:inline-block;width:10px;height:10px;background:#1e293b;border-radius:2px;vertical-align:middle"></span> normal</span>
      <span><span style="display:inline-block;width:10px;height:10px;background:#3b82f6;border-radius:2px;vertical-align:middle"></span> low</span>
      <span><span style="display:inline-block;width:10px;height:10px;background:#f59e0b;border-radius:2px;vertical-align:middle"></span> medium</span>
      <span><span style="display:inline-block;width:10px;height:10px;background:#ef4444;border-radius:2px;vertical-align:middle"></span> high</span>
      <span style="margin-left:auto" id="zscoreInfo">z=online(welford)</span>
    </div>
  </div>
  <!-- drift chart -->
  <div class="card" style="grid-column:2/3">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2 style="margin-bottom:0">Model Drift — Prediction vs Actual</h2>
      <span style="font-size:11px;color:#64748b" id="driftLabel">on track</span>
    </div>
    <div class="drift-chart" id="driftChart">
      <div class="drift-threshold" style="top:25%" id="driftUpper"></div>
      <div class="drift-threshold" style="top:75%" id="driftLower"></div>
      <div class="drift-line" id="driftBars"></div>
    </div>
    <div style="display:flex;gap:12px;margin-top:4px;font-size:11px;color:#64748b">
      <span><span style="display:inline-block;width:10px;height:10px;background:#6366f1;border-radius:2px;vertical-align:middle;opacity:.7"></span> prediction</span>
      <span><span style="display:inline-block;width:10px;height:10px;background:#22c55e;border-radius:2px;vertical-align:middle"></span> actual</span>
      <span><span style="display:inline-block;width:10px;height:10px;background:#ef4444;border-radius:2px;vertical-align:middle"></span> diverging</span>
    </div>
  </div>
  <!-- threshold bands -->
  <div class="card" style="grid-column:3/4">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2 style="margin-bottom:0">Dynamic Threshold Bands</h2>
      <span style="font-size:11px;color:#64748b" id="thresholdInfo">adapting to variance</span>
    </div>
    <div class="threshold-bands" id="thresholdBands">
      <div class="threshold-line" style="top:50%"></div>
    </div>
    <div style="display:flex;gap:8px;margin-top:4px;font-size:10px;color:#64748b;flex-wrap:wrap" id="thresholdStats"></div>
  </div>
</div>
<script>
// Welford's online algorithm for incremental mean/variance
class WelfordAgg {
  constructor(){this.n=0;this.mu=0;this.m2=0;this.min=Infinity;this.max=-Infinity}
  push(x){
    this.n++;
    if(x<this.min)this.min=x;
    if(x>this.max)this.max=x;
    const delta=x-this.mu;
    this.mu+=delta/this.n;
    this.m2+=delta*(x-this.mu);
  }
  get mean(){return this.n>0?this.mu:0}
  get variance(){return this.n>1?this.m2/(this.n-1):1}
  get std(){return Math.sqrt(this.variance)}
  z(x){return this.std===0?0:(x-this.mean)/this.std}
  reset(){this.n=0;this.mu=0;this.m2=0;this.min=Infinity;this.max=-Infinity}
}
// Moving window (last N) aggregator using Welford
class WindowWelford {
  constructor(window=60){this.window=window;this.data=[];this.w=new WelfordAgg()}
  push(x){
    this.data.push(x);
    this.w.push(x);
    if(this.data.length>this.window){
      const old=this.data.shift();
      // simple approximation: reset and re-aggregate window on overflow
      // for true incremental sliding window, use exponentially weighted moving stats
      if(this.data.length%this.window===0){
        this.w=new WelfordAgg();
        for(const v of this.data)this.w.push(v);
      }
    }
    return this;
  }
  get mean(){return this.w.mean}
  get std(){return this.w.std}
  z(x){return this.w.z(x)}
}
const state={
  points:[],
  predictions:[],
  alerts:[],
  causalHistory:[],
  metricNames:['cpu_pct','mem_mb','req_latency','error_rate','throughput'],
  welfords:{},
  tick:0,
  downsampled:false
};
for(const m of state.metricNames)state.welfords[m]=new WindowWelford(60);
function severity(z){
  const az=Math.abs(z);
  if(az>3)return 'high';
  if(az>2)return 'medium';
  if(az>1.5)return 'low';
  return 'normal';
}
function zColor(z){
  const sz=severity(z);
  if(sz==='high')return '#ef4444';
  if(sz==='medium')return '#f59e0b';
  if(sz==='low')return '#3b82f6';
  return '#1e293b';
}
function fillHeatmap(){
  const grid=document.getElementById('heatmapGrid');
  grid.innerHTML='';
  if(state.points.length===0){
    for(let i=0;i<12;i++){
      for(let j=0;j<5;j++){
        const cell=document.createElement('div');
        cell.className='heatmap-cell awaiting';
        grid.appendChild(cell);
      }
    }
    document.getElementById('heatmapLabel').textContent='Awaiting stream...';
    return;
  }
  document.getElementById('heatmapLabel').textContent=`last ${Math.min(state.points.length,12)} slices`;
  // downsample if >10000
  let pts=state.points;
  if(pts.length>10000){
    const step=Math.floor(pts.length/2000);
    pts=pts.filter((_,i)=>i%step===0).slice(-2000);
    state.downsampled=true;
  }
  const slice=pts.slice(-12);
  for(let i=0;i<12;i++){
    const rowIdx=slice.length-12+i;
    for(let mi=0;mi<state.metricNames.length;mi++){
      const cell=document.createElement('div');
      cell.className='heatmap-cell';
      if(rowIdx<0){
        cell.className+=' awaiting';
      } else {
        const p=slice[rowIdx];
        const val=p.values[mi];
        const w=state.welfords[state.metricNames[mi]];
        w.push(val);
        const z=w.z(val);
        const sev=severity(z);
        cell.className+=` ${sev}`;
        const tooltip=document.createElement('div');
        tooltip.className='tooltip';
        tooltip.textContent=`${state.metricNames[mi]}=${val.toFixed(1)} (z=${z.toFixed(2)})`;
        cell.appendChild(tooltip);
      }
      grid.appendChild(cell);
    }
  }
}
function fillDriftChart(){
  const container=document.getElementById('driftBars');
  container.innerHTML='';
  if(state.points.length===0){
    // placeholder state
    for(let i=0;i<20;i++){
      const bar=document.createElement('div');
      bar.className='drift-bar gap';
      bar.style.height='2px';
      container.appendChild(bar);
    }
    document.getElementById('driftLabel').textContent='Awaiting data...';
    return;
  }
  // check for data gap (>3s without new point)
  const now=Date.now();
  const lastTs=state.points[state.points.length-1].ts;
  const gapActive=(now-lastTs)>3000;
  if(gapActive){
    document.getElementById('driftLabel').textContent='Data gap — interpolation paused';
  } else {
    document.getElementById('driftLabel').textContent='on track';
  }
  const slice=state.points.slice(-20);
  const slicePreds=state.predictions.slice(-20);
  const maxVal=Math.max(...slice.map(p=>p.values[2]||0),3);
  for(let i=0;i<slice.length;i++){
    const p=slice[i];
    const pred=slicePreds[i]||p.values[2]*1.05;
    const actual=p.values[2]||0;
    const hActual=(actual/maxVal)*100;
    const hPred=(pred/maxVal)*100;
    const gapHere=(i<slice.length-1)&&((slice[i+1].ts-p.ts)>3000);
    // actual bar
    const bar=document.createElement('div');
    bar.className='drift-bar actual';
    if(gapHere)bar.className+=' gap';
    // detect divergence: actual deviates from pred by >20%
    const divRatio=pred>0?Math.abs(actual-pred)/pred:0;
    if(divRatio>0.2)bar.className+=' diverging';
    bar.style.height=Math.max(2,hActual)+'%';
    bar.title=`actual=${actual.toFixed(1)} pred=${pred.toFixed(1)}`;
    container.appendChild(bar);
    // pred bar (smaller, behind)
    const pbar=document.createElement('div');
    pbar.className='drift-bar prediction';
    pbar.style.height=Math.max(2,hPred)+'%';
    pbar.style.position='relative';
    pbar.style.marginTop=-Math.max(2,hPred)+'%';
    pbar.title=`prediction=${pred.toFixed(1)}`;
    container.appendChild(pbar);
  }
}
function fillThresholdBands(){
  const bands=document.getElementById('thresholdBands');
  // clear old bands
  bands.querySelectorAll('.threshold-band').forEach(el=>el.remove());
  // pick a metric
  const w=state.welfords['cpu_pct'];
  if(w.data.length<3){
    document.getElementById('thresholdInfo').textContent='accumulating...';
    document.getElementById('thresholdStats').innerHTML='<span>need ≥3 points for thresholds</span>';
    return;
  }
  const mu=w.mean;
  const sigma=w.std;
  // dynamic bands: mu ± sigma, 2*sigma, 3*sigma
  const ranges=[
    {lo:mu-sigma,hi:mu+sigma,label:'±1σ',color:'rgba(99,102,241,.15)'},
    {lo:mu-2*sigma,hi:mu+2*sigma,label:'±2σ',color:'rgba(245,158,11,.1)'},
    {lo:mu-3*sigma,hi:mu+3*sigma,label:'±3σ',color:'rgba(239,68,68,.08)'}
  ];
  const maxVal=Math.max(Math.abs(mu-3*sigma),Math.abs(mu+3*sigma),mu+sigma);
  const minVal=Math.min(Math.abs(mu-3*sigma),Math.abs(mu-2*sigma),mu-3*sigma);
  const range=maxVal-Math.min(minVal,0)||1;
  for(const r of ranges){
    // skip if no meaningful range
    if(r.lo===r.hi)continue;
    const topPct=((mu+3*sigma-r.lo)/(2*3*sigma||1))*100;
    const bottomPct=0;
    // actually position from bottom
    const bottomP=(Math.min(r.lo,mu-3*sigma)-minVal)/range*100;
    const topP=(Math.min(r.hi,mu+3*sigma)-minVal)/range*100;
    const band=document.createElement('div');
    band.className='threshold-band';
    band.style.bottom=Math.max(0,bottomP)+'%';
    band.style.height=Math.max(2,topP-bottomP)+'%';
    band.style.left='5%';
    band.style.right='5%';
    band.style.background=r.color;
    band.style.borderColor=r.color.replace('.1','.3').replace('.15','.3').replace('.08','.2');
    bands.appendChild(band);
    // label
    const label=document.createElement('div');
    label.className='threshold-label';
    label.style.bottom=Math.max(0,bottomP)+'%';
    label.textContent=r.label;
    bands.appendChild(label);
  }
  document.getElementById('thresholdInfo').textContent=`μ=${mu.toFixed(1)} σ=${sigma.toFixed(2)}`;
  document.getElementById('thresholdStats').innerHTML=
    `<span>mean: ${mu.toFixed(1)}</span><span>std: ${sigma.toFixed(2)}</span><span>n: ${w.data.length}</span>`;
}
function pushAlert(metricName,value,z){
  const sev=severity(z);
  const now=new Date();
  const ts=now.toLocaleTimeString();
  // find causers — metrics that changed before this one
  const causers=[];
  for(const m of state.metricNames){
    if(m===metricName)continue;
    const w2=state.welfords[m];
    if(w2.data.length>1){
      const lastVal=w2.data[w2.data.length-1];
      const lz=w2.z(lastVal);
      if(Math.abs(lz)>2){
        causers.push({metric:m,z:lz});
      }
    }
  }
  const alert={
    metric:metricName,
    value:value.toFixed(1),
    z:z.toFixed(2),
    sev:sev,
    ts:ts,
    causers:causers.slice(0,3)
  };
  state.alerts.unshift(alert);
  if(state.alerts.length>50)state.alerts.pop();
  renderAlerts();
}
function renderAlerts(){
  const feed=document.getElementById('alertFeed');
  const chain=document.getElementById('causalChain');
  if(state.alerts.length===0){
    feed.innerHTML='<div style="color:#64748b;font-size:13px;text-align:center;padding:20px 0">No anomalies detected</div>';
    chain.innerHTML='<div style="text-align:center;padding:10px 0">No anomalies detected yet</div>';
    return;
  }
  feed.innerHTML='';
  for(const a of state.alerts.slice(0,20)){
    const item=document.createElement('div');
    item.className='alert-item';
    item.innerHTML=`<span class="pulse-ring severity-${a.sev}"></span>
      <span style="flex:1">${a.metric} = ${a.value}</span>
      <span style="color:#94a3b8">z=${a.z}</span>
      <span class="alert-meta">${a.ts}</span>`;
    feed.appendChild(item);
  }
  // causal chain for latest alert
  const latest=state.alerts[0];
  if(latest.causers.length>0){
    chain.innerHTML=`<div style="margin-bottom:6px;color:#e0e6ed;font-weight:500">${latest.metric} anomaly</div>
      <div class="alert-chain">${
        latest.causers.map(c=>`<span class="causer">${c.metric} (z=${c.z.toFixed(1)})</span>`).join('')
      } <span class="linked">→ ${latest.metric}</span></div>`;
  } else {
    chain.innerHTML=`<div style="color:#64748b">${latest.metric} anomaly — no preceding correlated shifts</div>`;
  }
}
function generateTick(){
  state.tick++;
  const ts=Date.now();
  // simulate metrics with occasional anomalies
  const vals=[];
  const names=state.metricNames;
  for(let i=0;i<names.length;i++){
    let base;
    switch(i){
      case 0:base=45;break; // cpu 20-70
      case 1:base=512;break; // mem 200-800
      case 2:base=120;break; // latency 50-300
      case 3:base=2;break; // error rate 0-5
      case 4:base=1500;break; // throughput 500-2500
      default:base=50;
    }
    let val=base+(Math.random()-0.5)*base*0.4;
    // inject anomalies ~5% of ticks
    if(Math.random()<0.05){
      val+=base*(0.8+Math.random()*1.5);
    }
    vals.push(val);
    const w=state.welfords[names[i]];
    w.push(val);
    const z=w.z(val);
    if(Math.abs(z)>2.5){
      pushAlert(names[i],val,z);
    }
  }
  state.points.push({ts,values:vals});
  // keep last 1000
  if(state.points.length>1000)state.points=state.points.slice(-1000);
  // predictions (slightly lagged)
  state.predictions.push(vals[2]*1.05);
  if(state.predictions.length>1000)state.predictions=state.predictions.slice(-1000);
  // update UI
  document.getElementById('pointCount').textContent=state.points.length;
  const rateEl=document.getElementById('streamRate');
  if(state.tick%5===0){
    rateEl.textContent='2';
  }
  fillHeatmap();
  fillDriftChart();
  fillThresholdBands();
}
// Initial state — show awaiting placeholder before first tick
fillHeatmap();
fillDriftChart();
// Start stream
generateTick(); // immediate first tick
setInterval(generateTick,500);
</script>
</body>
</html>
```