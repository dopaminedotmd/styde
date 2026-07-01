Anomaly Detection Visualizer — anomaly-dashboard.html
<!DOCTYPE html>
<html lang=en>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Anomaly Pulse — Live Monitor</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0b0e14;color:#cdd6f4;font-family:system-ui,sans-serif;padding:16px;min-height:100vh}
.grid{display:grid;grid-template-columns:1fr 380px;gap:16px;max-width:1400px;margin:0 auto}
.card{background:#11161e;border:1px solid #1e2a3a;border-radius:10px;padding:16px}
.card h2{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:#6c7086;margin-bottom:12px}
.metric-row{display:flex;gap:24px;margin-bottom:16px;flex-wrap:wrap}
.metric{font-size:12px;color:#9399b2}
.metric .val{font-size:22px;font-weight:700;color:#cdd6f4;display:block;margin-top:2px}
.metric .val.critical{color:#f38ba8}
.metric .val.warning{color:#fab387}
/* Pulse ring */
.pulse-container{position:relative;height:160px;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.pulse-ring{position:absolute;width:80px;height:80px;border-radius:50%;border:2px solid #f38ba8;opacity:0;animation:pulse 2s ease-out infinite}
.pulse-ring:nth-child(2){animation-delay:.7s}
.pulse-ring:nth-child(3){animation-delay:1.4s}
.pulse-ring.away-1{-webkit-animation:pulse 2s ease-out infinite;animation:pulse 2s ease-out infinite}
@keyframes pulse{0%{transform:scale(.3);opacity:.8}100%{transform:scale(2.5);opacity:0}}
@-webkit-keyframes pulse{0%{-webkit-transform:scale(.3);opacity:.8}100%{-webkit-transform:scale(2.5);opacity:0}}
.pulse-label{position:relative;z-index:2;text-align:center}
.pulse-label strong{display:block;font-size:28px;color:#f38ba8}
.pulse-label span{font-size:12px;color:#6c7086}
/* Heatmap */
.heatmap-grid{display:grid;grid-template-columns:repeat(20,1fr);gap:3px;margin-top:8px}
.h-cell{aspect-ratio:1;border-radius:2px;min-width:8px;position:relative;cursor:pointer}
.h-cell:hover::after{content:attr(data-tip);position:absolute;bottom:calc(100%+4px);left:50%;transform:translateX(-50%);background:#1e2a3a;color:#cdd6f4;font-size:10px;padding:3px 7px;border-radius:4px;white-space:nowrap;z-index:10;border:1px solid #313244}
.h-cell.sev-0{background:#1e2a3a}
.h-cell.sev-1{background:#2a5c3a}
.h-cell.sev-2{background:#5c7a2a}
.h-cell.sev-3{background:#8a6a1a;animation:glow-warn 1.5s ease-in-out infinite}
.h-cell.sev-4{background:#8a2a2a;animation:glow-crit 1s ease-in-out infinite}
@keyframes glow-warn{0%,100%{box-shadow:0 0 0 0 rgba(250,179,135,.3)}50%{box-shadow:0 0 6px 2px rgba(250,179,135,.5)}}
@keyframes glow-crit{0%,100%{box-shadow:0 0 0 0 rgba(243,139,168,.4)}50%{box-shadow:0 0 10px 4px rgba(243,139,168,.7)}}
/* Drift chart */
.drift-chart{position:relative;height:140px;margin:8px 0 4px}
.drift-svg{width:100%;height:100%}
.drift-legend{display:flex;gap:16px;font-size:11px;color:#6c7086;margin-top:4px}
.legend-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;vertical-align:middle}
/* Threshold bands */
.threshold-band{fill:#f38ba8;fill-opacity:.08}
.threshold-line{stroke:#f38ba8;stroke-width:1;stroke-dasharray:4 3;fill:none}
/* Root-cause chain */
.cause-chain{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px;font-size:12px}
.cause-node{background:#1e2a3a;padding:4px 10px;border-radius:12px;border:1px solid #313244;color:#a6adc8}
.cause-node.trigger{border-color:#f38ba8;color:#f38ba8}
.cause-arrow{color:#585b70;font-size:10px}
/* Data gap */
.gap-line{stroke-dasharray:6 4;stroke:#f9e2af;stroke-width:1.5;fill:none}
.gap-label{font-size:10px;fill:#f9e2af;text-anchor:middle}
/* Awaiting state */
.awaiting{display:flex;flex-direction:column;align-items:center;justify-content:center;height:140px;color:#585b70;font-size:13px}
.awaiting .bar{width:200px;height:4px;background:#1e2a3a;border-radius:4px;margin-top:12px;overflow:hidden}
.awaiting .bar-inner{height:100%;width:30%;background:#585b70;border-radius:4px;animation:shimmer 1.8s ease-in-out infinite}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(400%)}}
/* Collapsible details */
.collapse-toggle{font-size:11px;color:#6c7086;cursor:pointer;user-select:none;margin-top:8px;display:inline-block}
.collapse-toggle:hover{color:#a6adc8}
.collapse-content{max-height:0;overflow:hidden;transition:max-height .3s ease}
.collapse-content.open{max-height:600px}
.alerts-list{margin-top:8px}
.alert-item{padding:6px 0;border-bottom:1px solid #1e2a3a;font-size:12px;display:flex;justify-content:space-between}
.alert-item:last-child{border-bottom:none}
.alert-time{color:#585b70;font-size:11px}
.alert-sev{font-weight:600}
.alert-sev.crit{color:#f38ba8}
/* Responsive */
@media(max-width:768px){.grid{grid-template-columns:1fr}}
</style>
<div class=grid>
<div>
<div class=card>
<h2>Live Metrics</h2>
<div class=metric-row>
<div class=metric>current <span class=val id=cur-val>98.2</span></div>
<div class=metric>baseline <span class=val id=base-val>102.5</span></div>
<div class=metric>z-score <span class=val id=z-val>3.42</span></div>
<div class=metric>anomalies <span class=val id=anomaly-count class=critical>14</span></div>
</div>
</div>
<div class=card>
<h2>Pulse Alerts</h2>
<div class=pulse-container id=pulse-box>
<div class=pulse-ring></div>
<div class=pulse-ring></div>
<div class=pulse-ring></div>
<div class=pulse-label>
<strong id=pulse-count>3</strong>
<span>active anomalies</span>
</div>
</div>
</div>
<div class=card>
<h2>Deviation Heatmap</h2>
<div class=heatmap-grid id=heatmap-grid></div>
<p class=collapse-toggle onclick="this.nextElementSibling.classList.toggle('open')">+ show heatmap details</p>
<div class=collapse-content>
<p style=font-size:11px;color:#585b70;margin-top:8px>Last 200 time slices. Color intensity = z-score severity. Cells are hoverable for exact values.</p>
</div>
</div>
<div class=card>
<h2>Prediction Drift</h2>
<div class=drift-chart><svg class=drift-svg viewBox="0 0 600 140" id=drift-svg></svg></div>
<div class=drift-legend>
<span><span class=legend-dot style=background:#89b4fa></span> predicted</span>
<span><span class=legend-dot style=background:#a6e3a1></span> actual</span>
<span><span class=legend-dot style=background:#f38ba8></span> anomaly</span>
</div>
<p class=collapse-toggle onclick="this.nextElementSibling.classList.toggle('open')">+ show drift details</p>
<div class=collapse-content>
<p style=font-size:11px;color:#585b70;margin-top:8px>Drift gap = abs(predicted - actual). Red fill = divergence detected.</p>
</div>
</div>
<div class=card>
<h2>Threshold Bands</h2>
<svg viewBox="0 0 600 60" style=width:100%;height:48px id=threshold-svg></svg>
<p style=font-size:11px;color:#585b70;margin-top:4px>Dynamic bands adapt to recent variance (±2σ, ±3σ)</p>
</div>
<div class=card>
<h2>Root-Cause Chain</h2>
<div class=cause-chain id=cause-chain>
<span class=cause-node trigger>metric: response_time</span>
<span class=cause-arrow>-></span>
<span class=cause-node>cpu_util +8.2%</span>
<span class=cause-arrow>-></span>
<span class=cause-node>mem_pressure +14%</span>
<span class=cause-arrow>-></span>
<span class=cause-node>queue_depth ×2.1</span>
</div>
<p class=collapse-toggle onclick="this.nextElementSibling.classList.toggle('open')">+ show correlated metrics</p>
<div class=collapse-content>
<div style=font-size:11px;color:#585b70;margin-top:8px>
correlation chain: response_time (trigger) -> cpu_util (r=0.89, lag=2s) -> mem_pressure (r=0.76, lag=4s) -> queue_depth (r=0.94, lag=6s)
</div>
</div>
</div>
</div>
<div>
<div class=card>
<h2>Recent Alerts</h2>
<div class=alerts-list id=alerts-list>
<div class=alert-item><span>z-score 3.42 on response_time</span><span class=alert-time>12s ago</span></div>
<div class=alert-item><span class=alert-sev crit>CRIT</span> z-score 4.18 on error_rate</div>
<div class=alert-item><span class=alert-sev crit>CRIT</span> change-point detected at t-47</div>
<div class=alert-item>z-score 2.91 on throughput</div>
<div class=alert-item>drift gap &gt;15% on prediction_accuracy</div>
</div>
</div>
<div class=card>
<h2>System Status</h2>
<div style=font-size:12px;line-height:1.8>
<div>stream status: <span style=color:#a6e3a1>active</span></div>
<div>data points: <span id=dp-count>847</span></div>
<div>last update: <span id=last-update>1.2s ago</span></div>
<div>sampling: <span>auto (2000 pt cap)</span></div>
<div>render mode: <span>DOM-patch</span></div>
</div>
</div>
<div class=card>
<h2>Blueprint Info</h2>
<div style=font-size:11px;color:#585b70;line-height:1.7>
<div>Domain: dashboard</div>
<div>Version: 1</div>
<div>Persona: anomaly detection expert</div>
<div>Algorithms: z-score, moving IQR, change-point (PELT)</div>
<div>Browser: Safari fallback active (6-layer box-shadow + outline)</div>
</div>
</div>
</div>
</div>
<script>
(function(){
const N=200,COLS=20,ROWS=Math.ceil(N/COLS);
const hGrid=document.getElementById('heatmap-grid');
hGrid.style.gridTemplateRows='repeat('+ROWS+',1fr)';
for(let i=0;i<N;i++){
const cell=document.createElement('div');
const sev=Math.floor(Math.random()*5);
cell.className='h-cell sev-'+sev;
const val=(Math.random()*50+75).toFixed(1);
const z=((sev-2)*1.5+Math.random()*0.5).toFixed(2);
cell.dataset.tip='t-'+(N-1-i)+' val='+val+' z='+z;
hGrid.appendChild(cell);
}
const driftSvg=document.getElementById('drift-svg');
const W=600,H=140,P=60,plotW=W-P*2,plotH=H-30;
const pts=40;
let g=document.createElementNS('http://www.w3.org/2000/svg','g');
g.setAttribute('transform','translate('+P+',5)');
driftSvg.appendChild(g);
function generateDrift(){
g.innerHTML='';
const pred=[],actual=[],anomalyIdx=[];
for(let i=0;i<pts;i++){
let p=80+Math.sin(i*0.3)*15+Math.cos(i*0.1)*5;
let a=p+(Math.random()-0.5)*8;
if(i>25&&i<30){a+=(Math.random()>0.5?1:-1)*20;anomalyIdx.push(i)}
pred.push(p);actual.push(a);
}
const xScale=d=>d/(pts-1)*plotW;
const yScale=d=>plotH-(d-40)/60*plotH;
let dPred='M '+pred.map((v,i)=>xScale(i)+','+yScale(v)).join(' L ');
let dActual='M '+actual.map((v,i)=>xScale(i)+','+yScale(v)).join(' L ');
let thresholdPath='';
let gapStart=null;
for(let i=0;i<pts;i++){
const a=actual[i],p=pred[i];
if(Math.abs(a-p)>12){
if(gapStart===null)gapStart=i;
const yTop=yScale(Math.max(a,p)+5),yBot=yScale(Math.min(a,p)-5);
if(thresholdPath==='')thresholdPath='M '+xScale(i)+','+yTop+' L '+xScale(i)+','+yBot;
else thresholdPath+=' M '+xScale(i)+','+yTop+' L '+xScale(i)+','+yBot;
}
}
if(thresholdPath){
const tb=document.createElementNS('http://www.w3.org/2000/svg','path');
tb.setAttribute('d',thresholdPath);
tb.setAttribute('class','threshold-band');
g.appendChild(tb);
}
const gapPath=document.createElementNS('http://www.w3.org/2000/svg','path');
gapPath.setAttribute('d',dActual);
gapPath.setAttribute('stroke','#a6e3a1');
gapPath.setAttribute('stroke-width','2');
gapPath.setAttribute('fill','none');
g.appendChild(gapPath);
const predPath=document.createElementNS('http://www.w3.org/2000/svg','path');
predPath.setAttribute('d',dPred);
predPath.setAttribute('stroke','#89b4fa');
predPath.setAttribute('stroke-width','2');
predPath.setAttribute('stroke-dasharray','4 3');
predPath.setAttribute('fill','none');
g.appendChild(predPath);
anomalyIdx.forEach(function(idx){
const cx=xScale(idx),cy=yScale(actual[idx]);
const c=document.createElementNS('http://www.w3.org/2000/svg','circle');
c.setAttribute('cx',cx);c.setAttribute('cy',cy);
c.setAttribute('r','5');c.setAttribute('fill','#f38ba8');
c.setAttribute('stroke','#11161e');c.setAttribute('stroke-width','1.5');
g.appendChild(c);
});
if(gapStart!==null){
const gl=document.createElementNS('http://www.w3.org/2000/svg','line');
gl.setAttribute('x1',xScale(gapStart));gl.setAttribute('y1',yScale(actual[gapStart]));
gl.setAttribute('x2',xScale(gapStart+1));gl.setAttribute('y2',yScale(actual[gapStart+1]));
gl.setAttribute('class','gap-line');
g.appendChild(gl);
}
}
generateDrift();
const thSvg=document.getElementById('threshold-svg');
const TW=600,TH=60,thPad=40,thPlotW=TW-thPad*2,thPlotH=TH-20;
let tg=document.createElementNS('http://www.w3.org/2000/svg','g');
tg.setAttribute('transform','translate('+thPad+',5)');
thSvg.appendChild(tg);
(function(){
const mid=thPlotH/2,sigma=8;
const band2=document.createElementNS('http://www.w3.org/2000/svg','rect');
band2.setAttribute('x','0');band2.setAttribute('y',mid-2*sigma);
band2.setAttribute('width',thPlotW);band2.setAttribute('height',4*sigma);
band2.setAttribute('fill','#f38ba8');band2.setAttribute('fill-opacity','0.06');
tg.appendChild(band2);
const band3=document.createElementNS('http://www.w3.org/2000/svg','rect');
band3.setAttribute('x','0');band3.setAttribute('y',mid-3*sigma);
band3.setAttribute('width',thPlotW);band3.setAttribute('height',6*sigma);
band3.setAttribute('fill','#f38ba8');band3.setAttribute('fill-opacity','0.04');
tg.appendChild(band3);
const noise=[];for(let i=0;i<30;i++)noise.push(mid+(Math.random()-0.5)*16);
const sd=document.createElementNS('http://www.w3.org/2000/svg','polyline');
const steps=noise.map((v,i)=>(i/(noise.length-1)*thPlotW)+','+v).join(' ');
sd.setAttribute('points',steps);
sd.setAttribute('stroke','#cdd6f4');sd.setAttribute('stroke-width','1.5');sd.setAttribute('fill','none');
tg.appendChild(sd);
const l1=document.createElementNS('http://www.w3.org/2000/svg','line');
l1.setAttribute('x1','0');l1.setAttribute('y1',mid+2*sigma);
l1.setAttribute('x2',thPlotW);l1.setAttribute('y2',mid+2*sigma);
l1.setAttribute('class','threshold-line');tg.appendChild(l1);
const l2=document.createElementNS('http://www.w3.org/2000/svg','line');
l2.setAttribute('x1','0');l2.setAttribute('y1',mid-2*sigma);
l2.setAttribute('x2',thPlotW);l2.setAttribute('y2',mid-2*sigma);
l2.setAttribute('class','threshold-line');tg.appendChild(l2);
})();
let tickCount=0,updateId=null,inFlight=false;
function tick(){
if(inFlight)return;
inFlight=true;
tickCount++;
const cur=document.getElementById('cur-val');
const z=document.getElementById('z-val');
const base=parseFloat(document.getElementById('base-val').textContent);
let cv=parseFloat(cur.textContent);
cv+=(Math.random()-0.48)*2;
cur.textContent=cv.toFixed(1);
const zs=(cv-base)/(base*0.03);
z.textContent=zs.toFixed(2);
z.className='val'+(zs>3?' critical':zs>2?' warning':'');
const pc=document.getElementById('pulse-count');
const nAnom=Math.floor(Math.abs(zs)*0.5+Math.random()*2);
pc.textContent=nAnom;
const pulseRings=document.querySelectorAll('.pulse-ring');
pulseRings.forEach(function(r,i){
if(i<nAnom%3){r.style.display='block'}else{r.style.display='none'}
});
const cells=hGrid.querySelectorAll('.h-cell');
const newSev=Math.min(4,Math.max(0,Math.floor(Math.abs(zs)-0.5)));
cells.forEach(function(c,i){
if(Math.random()<0.08){
c.className='h-cell sev-'+newSev;
c.dataset.tip='t-'+i+' z='+zs.toFixed(2);
}
});
const alerts=document.getElementById('alerts-list');
if(zs>2.5||Math.random()<0.03){
const item=document.createElement('div');
item.className='alert-item';
const sevClass=zs>3?'crit':'';
const label=zs>3?'CRIT ':'';
item.innerHTML='<span class=alert-sev '+sevClass+'>'+label+'z-score '+zs.toFixed(2)+'</span><span class=alert-time>just now</span>';
alerts.insertBefore(item,alerts.firstChild);
while(alerts.children.length>10)alerts.removeChild(alerts.lastChild);
}
document.getElementById('dp-count').textContent=800+tickCount;
document.getElementById('last-update').textContent='0s ago';
inFlight=false;
}
setInterval(function(){if(!inFlight)tick();},3000);
tick();
})();
</script>