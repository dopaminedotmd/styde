```html
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Anomaly Detection Visualizer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#d0d8e8;font-family:'Segoe UI',system-ui,sans-serif;padding:16px;min-height:100vh}
h2{font-size:14px;font-weight:600;color:#7a8aad;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:1600px;margin:0 auto}
.card{background:#111827;border:1px solid #1e293b;border-radius:10px;padding:14px;position:relative}
.full{grid-column:1/-1}
canvas{display:block;width:100%;height:280px;border-radius:6px;background:#0d111c}
.heatmap-canvas{height:200px}
.pulse-canvas{height:140px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.stat{background:#0d111c;border:1px solid #1e293b;border-radius:6px;padding:8px 12px;font-size:12px}
.stat label{color:#6b7b9e;display:block;font-size:10px;text-transform:uppercase}
.stat span{color:#e0e8f4;font-weight:600;font-size:15px}
.stat .alert{color:#f87171}
.stat .ok{color:#4ade80}
.stat .warn{color:#fbbf24}
.chain{display:flex;gap:4px;align-items:center;flex-wrap:wrap;font-size:12px;margin-top:6px}
.chain .link{color:#818cf8;padding:2px 6px;background:#1e1b4b;border-radius:4px;font-size:11px}
.chain .arrow{color:#4b5563}
.tooltip{position:absolute;background:#1e293b;border:1px solid #334155;border-radius:6px;padding:6px 10px;font-size:11px;pointer-events:none;z-index:10;display:none;white-space:nowrap;color:#e0e8f4}
.slider-row{display:flex;gap:16px;align-items:center;margin-top:8px}
.slider-row label{font-size:11px;color:#7a8aad}
.slider-row input[type=range]{width:100px;accent-color:#818cf8}
#alertBanner{display:none;background:linear-gradient(90deg,#7f1d1d,#1e293b);border:1px solid #991b1b;border-radius:6px;padding:8px 14px;margin-bottom:10px;font-size:13px}
#alertBanner.active{display:block}
#alertBanner strong{color:#fca5a5}
.metrics-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.tag{font-size:10px;padding:2px 8px;border-radius:10px;background:#1e293b;color:#9ca3af}
.tag.active{background:#312e81;color:#a5b4fc}
</style>
<div class=grid>
<div class="card full" id=alertBanner><strong id=alertMsg></strong> <span id=alertDetail></span></div>
<div class="card full"><h2>Anomaly Pulse Monitor</h2><canvas id=pulseCanvas class=pulse-canvas></canvas></div>
<div class=card><h2>Deviation Heatmap</h2><canvas id=heatmapCanvas class=heatmap-canvas></canvas><div id=heatmapTooltip class=tooltip></div></div>
<div class=card><h2>Drift Chart</h2><canvas id=driftCanvas class=heatmap-canvas></canvas></div>
<div class="card full"><h2>Root-Cause Chains</h2><div id=rootCauseChains style=min-height:48px></div></div>
</div>
<script>
const W=720,H={pulse:140,heat:200,drift:200};
let metrics={cpu:[],mem:[],latency:[],throughput:[],error_rate:[]};
let predictions={cpu:[],mem:[],latency:[],throughput:[],error_rate:[]};
let anomalyFlags={cpu:[],mem:[],latency:[],throughput:[],error_rate:[]};
let thresholds={cpu:[],mem:[],latency:[],throughput:[],error_rate:[]};
const LABELS=['cpu','mem','latency','throughput','error_rate'];
const MAX_PTS=180;
let frameCount=0;
const pulseC=document.getElementById('pulseCanvas');
const heatC=document.getElementById('heatmapCanvas');
const driftC=document.getElementById('driftCanvas');
const pctx=pulseC.getContext('2d');
const hctx=heatC.getContext('2d');
const dctx=driftC.getContext('2d');
const tooltip=document.getElementById('heatmapTooltip');
const chainDiv=document.getElementById('rootCauseChains');
const alertBanner=document.getElementById('alertBanner');
const alertMsg=document.getElementById('alertMsg');
function resize(c,w,h){const dpr=window.devicePixelRatio||1;c.width=w*dpr;c.height=h*dpr;c.style.width=w+'px';c.style.height=h+'px';const ctx=c.getContext('2d');ctx.scale(dpr,dpr);return ctx}
function resizeAll(){
 resize(pulseC,W,H.pulse);
 resize(heatC,W,H.heat);
 resize(driftC,W,H.drift);
}
resizeAll();window.addEventListener('resize',resizeAll);
function normal(){let u=0,v=0;while(v===0){u=2*Math.random()-1;v=2*Math.random()-1;let s=u*u+v*v;if(s>=1||s===0){u=0;v=0;continue}}return u*Math.sqrt(-2*Math.log(u*u+v*v)/(u*u+v*v))}
function genMetric(base,vol,anomalyChance){
 let v=base+normal()*vol;
 if(Math.random()<anomalyChance)v+=normal()*vol*4;
 return Math.max(0,v);
}
function predictMetric(series){
 if(series.length<5)return series[series.length-1]||50;
 let n=series.length;
 let sumX=0,sumY=0,sumXY=0,sumX2=0;
 for(let i=0;i<n;i++){sumX+=i;sumY+=series[i];sumXY+=i*series[i];sumX2+=i*i}
 let slope=(n*sumXY-sumX*sumY)/(n*sumX2-sumX*sumX);
 let intercept=(sumY-slope*sumX)/n;
 return Math.max(0,slope*n+intercept);
}
function zScore(val,series){
 if(series.length<4)return 0;
 let n=series.length;
 let mean=series.reduce((a,b)=>a+b,0)/n;
 let variance=series.reduce((s,v)=>s+(v-mean)**2,0)/(n-1);
 let std=Math.sqrt(variance)||1e-10;
 return(val-mean)/std;
}
function movingIQR(val,series,winsize){
 let n=series.length;
 let window=series.slice(Math.max(0,n-winsize),n);
 if(window.length<4)return 0;
 let sorted=[...window].sort((a,b)=>a-b);
 let q1=sorted[Math.floor(sorted.length*.25)];
 let q3=sorted[Math.floor(sorted.length*.75)];
 let iqr=q3-q1||1e-10;
 return(val-(q1+q3)/2)/iqr;
}
function changePoint(series,winsize){
 if(series.length<winsize*2)return 0;
 let n=series.length;
 let w1=series.slice(n-winsize*2,n-winsize);
 let w2=series.slice(n-winsize,n);
 let m1=w1.reduce((a,b)=>a+b,0)/w1.length;
 let m2=w2.reduce((a,b)=>a+b,0)/w2.length;
 let v1=w1.reduce((s,v)=>s+(v-m1)**2,0)/(w1.length-1)||1e-10;
 let v2=w2.reduce((s,v)=>s+(v-m2)**2,0)/(w2.length-1)||1e-10;
 let se=Math.sqrt(v1/w1.length+v2/w2.length);
 return(m2-m1)/se;
}
function pushMetric(key,val){
 metrics[key].push(val);
 if(metrics[key].length>MAX_PTS)metrics[key].shift();
 predictions[key].push(predictMetric(metrics[key]));
 if(predictions[key].length>MAX_PTS)predictions[key].shift();
 let z=zScore(val,metrics[key]);
 let iqr=movingIQR(val,metrics[key],20);
 let cp=changePoint(metrics[key],10);
 let isAnomaly=Math.abs(z)>2.5||Math.abs(iqr)>2||Math.abs(cp)>2.5;
 anomalyFlags[key].push(isAnomaly);
 if(anomalyFlags[key].length>MAX_PTS)anomalyFlags[key].shift();
 let thresh=2*metrics[key].slice(-20).reduce((s,v)=>s+(v-metrics[key].slice(-20).reduce((a,b)=>a+b,0)/20)**2,0)/19||1;
 thresholds[key].push(Math.sqrt(thresh)*2.5+metrics[key].slice(-20).reduce((a,b)=>a+b,0)/20);
 if(thresholds[key].length>MAX_PTS)thresholds[key].shift();
 return isAnomaly;
}
function tick(){
 frameCount++;
 let newAlerts=[];
 LABELS.forEach(k=>{
  let base={cpu:65,mem:72,latency:120,throughput:450,error_rate:3}[k];
  let vol={cpu:8,mem:6,latency:25,throughput:60,error_rate:1.2}[k];
  let anomChance=frameCount%40===0?.12:.03;
  let val=genMetric(base,vol,anomChance);
  let isAnom=pushMetric(k,val);
  if(isAnom)newAlerts.push(k);
 });
 if(newAlerts.length){showAlert(newAlerts);drawPulseAnomalies(true)}else drawPulseAnomalies(false);
 drawHeatmap();
 drawDrift();
 drawRootCause(newAlerts);
 requestAnimationFrame(tick);
}
let lastAnomalyFrame=0;
function drawPulseAnomalies(hasNew){
 const ctx=pctx;const cw=W,ch=H.pulse;
 ctx.clearRect(0,0,cw,ch);
 let anomalies=[];
 LABELS.forEach((k,i)=>{
  let flags=anomalyFlags[k];
  for(let j=flags.length-1;j>=Math.max(0,flags.length-30);j--){
   if(flags[j])anomalies.push({idx:j,metric:k,color:['#f87171','#fbbf24','#60a5fa','#a78bfa','#34d399'][i]});
  }
 });
 if(hasNew)lastAnomalyFrame=frameCount;
 let age=frameCount-lastAnomalyFrame;
 anomalies.forEach((a,i)=>{
  let x=i*70+40;if(x>cw-20)x=20+(i%9)*70;
  let y=ch/2+Math.sin(frameCount*.05+i)*20;
  ctx.beginPath();
  ctx.arc(x,y,6,0,Math.PI*2);
  ctx.fillStyle=a.color;ctx.fill();
  ctx.strokeStyle=a.color;ctx.lineWidth=2;ctx.stroke();
  for(let r=0;r<3;r++){
   let rad=10+r*14+(age%60)*.8;
   let alpha=Math.max(0,1-rad/80);
   ctx.beginPath();
   ctx.arc(x,y,rad,0,Math.PI*2);
   ctx.strokeStyle=a.color.replace(')',`,${alpha.toFixed(2)})`);
   ctx.lineWidth=2;ctx.stroke();
  }
  ctx.fillStyle='#9ca3af';ctx.font='10px sans-serif';ctx.textAlign='center';
  ctx.fillText(a.metric,x,y+24);
 });
}
function drawHeatmap(){
 const ctx=hctx;const cw=W,ch=H.heat;
 ctx.clearRect(0,0,cw,ch);
 let cols=36,rows=5;
 let cellW=cw/cols,cellH=ch/rows;
 let maxAnom=Math.max(...LABELS.map(k=>{
  let flags=anomalyFlags[k];return flags.filter(f=>f).length||1;
 }));
 let recentMetrics={};
 LABELS.forEach((k,i)=>{
  let vals=metrics[k].slice(-cols);
  let flags=anomalyFlags[k].slice(-cols);
  for(let j=0;j<cols;j++){
   let v=vals[j]||50;
   let f=flags[j]||false;
   let z=zScore(v,metrics[k]);
   let normZ=Math.min(1,Math.abs(z)/4);
   let r=0,g=0,b=0;
   if(f){r=255;g=80+Math.floor((1-normZ)*100);b=80}else if(z>0){r=Math.floor(255*normZ);g=Math.floor(200*(1-normZ));b=50}else if(z<-0.5){r=60;g=Math.floor(200*(1-normZ*.5));b=Math.floor(255*normZ*.8)}else{r=30;g=80+Math.floor(120*(1-normZ));b=60}
   ctx.fillStyle=`rgb(${r},${g},${b})`;
   ctx.fillRect(j*cellW,i*cellH,cellW,cellH);
   if(f){
    ctx.strokeStyle='#fca5a5';ctx.lineWidth=1;ctx.strokeRect(j*cellW+1,i*cellH+1,cellW-2,cellH-2);
   }
  }
 });
 heatC.onmousemove=function(e){
  let rect=heatC.getBoundingClientRect();
  let mx=e.clientX-rect.left,my=e.clientY-rect.top;
  let col=Math.floor(mx/(rect.width/cols)),row=Math.floor(my/(rect.height/rows));
  if(col>=0&&col<cols&&row>=0&&row<rows){
   let k=LABELS[row];
   let vals=metrics[k];
   let idx=vals.length-cols+col;
   let val=vals[idx]||'--';
   let flag=anomalyFlags[k][idx];
   tooltip.style.display='block';
   tooltip.style.left=(mx+12)+'px';tooltip.style.top=(my-10)+'px';
   tooltip.innerHTML=`<b>${k}</b> t-${cols-col-1} value:${typeof val==='number'?val.toFixed(1):val} ${flag?'<span style=color:#f87171>ANOMALY</span>':''}`;
  }else{tooltip.style.display='none'}
 };
 heatC.onmouseleave=()=>tooltip.style.display='none';
}
function drawDrift(){
 const ctx=dctx;const cw=W,ch=H.drift;
 ctx.clearRect(0,0,cw,ch);
 let activeMetric=LABELS.reduce((a,b)=>anomalyFlags[b].filter(f=>f).length>anomalyFlags[a].filter(f=>f).length?b:a);
 let actual=metrics[activeMetric]||[];
 let predicted=predictions[activeMetric]||[];
 let n=actual.length;
 if(n<2)return;
 let minVal=Math.min(...actual,...predicted),maxVal=Math.max(...actual,...predicted);
 let range=maxVal-minVal||1;
 function toY(v){return ch-(v-minVal)/range*(ch-20)-10}
 function toX(i){return i/(n-1)*(cw-20)+10}
 ctx.beginPath();ctx.strokeStyle='#4ade80';ctx.lineWidth=2;
 for(let i=0;i<n;i++){let x=toX(i),y=toY(actual[i]);i===0?ctx.moveTo(x,y):ctx.lineTo(x,y)}
 ctx.stroke();
 ctx.beginPath();ctx.strokeStyle='#818cf8';ctx.lineWidth=1.5;ctx.setLineDash([4,4]);
 for(let i=0;i<n;i++){let x=toX(i),y=toY(predicted[i]);i===0?ctx.moveTo(x,y):ctx.lineTo(x,y)}
 ctx.stroke();ctx.setLineDash([]);
 for(let i=1;i<n;i++){
  let gap=actual[i]-predicted[i];
  let x1=toX(i-1),x2=toX(i);
  let ya=toY(actual[i-1]),yb=toY(actual[i]);
  let yp1=toY(predicted[i-1]),yp2=toY(predicted[i]);
  let color=Math.abs(gap)/range<.05?'rgba(74,222,128,0.15)':'rgba(248,113,113,0.2)';
  ctx.fillStyle=color;
  ctx.beginPath();
  ctx.moveTo(x1,Math.min(ya,yp1));ctx.lineTo(x1,Math.max(ya,yp1));
  ctx.lineTo(x2,Math.max(yb,yp2));ctx.lineTo(x2,Math.min(yb,yp2));
  ctx.closePath();ctx.fill();
 }
 let thresh=thresholds[activeMetric]?.[thresholds[activeMetric].length-1];
 if(thresh){
  ctx.beginPath();ctx.strokeStyle='rgba(251,191,36,0.4)';ctx.lineWidth=1;ctx.setLineDash([3,3]);
  let ty=toY(thresh);ctx.moveTo(10,ty);ctx.lineTo(cw-10,ty);
  let ty2=toY(minVal+(maxVal-minVal)*.9);
  ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(251,191,36,0.6)';ctx.font='10px sans-serif';ctx.fillText('threshold',cw-90,ty-4);
 }
 ctx.fillStyle='#6b7b9e';ctx.font='10px sans-serif';
 ctx.fillText(activeMetric+' (green=actual, dash=predicted)',14,16);
 let drift=actual[n-1]-predicted[n-1];
 let driftColor=Math.abs(drift)/range<.05?'#4ade80':'#f87171';
 ctx.fillStyle=driftColor;ctx.fillText('drift: '+(drift>0?'+':'')+drift.toFixed(1),cw-120,16);
}
let causalHistory=[];
function drawRootCause(newAlerts){
 if(!newAlerts||!newAlerts.length){chainDiv.innerHTML=causalHistory.slice(0,8).map(c=>{
  return `<div class=chain>${c.map(m=>`<span class=link>${m}</span>`).join('<span class=arrow> &#8594; </span>')}</div>`;
 }).join('');return}
 function getCorrelated(metric){
  let ranks=LABELS.filter(k=>k!==metric).map(k=>{
   let m1=metrics[metric].slice(-15),m2=metrics[k].slice(-15);
   if(m1.length<5||m2.length<5)return{k,score:0};
   let mx1=m1.reduce((a,b)=>a+b,0)/m1.length;
   let mx2=m2.reduce((a,b)=>a+b,0)/m2.length;
   let num=0,d1=0,d2=0;
   for(let i=0;i<m1.length;i++){num+=(m1[i]-mx1)*(m2[i]-mx2);d1+=(m1[i]-mx1)**2;d2+=(m2[i]-mx2)**2}
   let r=num/Math.sqrt(d1*d2)||0;
   return{k,score:r};
  });
  return ranks.sort((a,b)=>Math.abs(b.score)-Math.abs(a.score)).slice(0,2).map(r=>r.k);
 }
 let chains=newAlerts.map(alert=>{
  let chain=[alert];
  let corr=getCorrelated(alert);
  corr.forEach(c=>{
   let sub=getCorrelated(c).filter(k=>k!==alert);
   chain.push(c);
   if(sub.length)chain.push(sub[0]);
  });
  return chain;
 });
 causalHistory.unshift(...chains);
 if(causalHistory.length>16)causalHistory=causalHistory.slice(0,16);
 chainDiv.innerHTML=causalHistory.slice(0,8).map(c=>{
  return `<div class=chain>${c.map(m=>`<span class=link>${m}</span>`).join('<span class=arrow> &#8594; </span>')}</div>`;
 }).join('');
}
function showAlert(alerts){
 alertBanner.classList.add('active');
 alertMsg.textContent='Anomaly detected: '+alerts.join(', ')+' ';
 document.getElementById('alertDetail').textContent='at t='+metrics[alerts[0]].length;
 setTimeout(()=>{alertBanner.classList.remove('active')},3000);
}
let statsDiv=document.createElement('div');
statsDiv.className='stats';
document.querySelector('.grid').prepend(statsDiv);
function updateStats(){
 statsDiv.innerHTML=LABELS.map(k=>{
  let vals=metrics[k];let last=vals[vals.length-1]||0;
  let flags=anomalyFlags[k];let anomCount=flags.filter(f=>f).length;
  let anomClass=anomCount>5?'alert':anomCount>2?'warn':'ok';
  return `<div class=stat><label>${k}</label><span>${last.toFixed(1)} <span class=${anomClass}>${anomCount>0?'!'+anomCount:''}</span></span></div>`;
 }).join('');
 requestAnimationFrame(updateStats);
}
updateStats();
for(let i=0;i<40;i++){
 LABELS.forEach(k=>{
  let base={cpu:65,mem:72,latency:120,throughput:450,error_rate:3}[k];
  let vol={cpu:8,mem:6,latency:25,throughput:60,error_rate:1.2}[k];
  pushMetric(k,genMetric(base,vol,.02));
 });
}
tick();
</script>
```