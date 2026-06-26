I will build the full Voice Command Dashboard as a single self-contained HTML file. Outputting directly.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Voice Command Dashboard</title>
<style>
:root{--bg:#0f1117;--surface:#1a1d28;--surface2:#242736;--border:#2e3142;--text:#e4e6f0;--text2:#8b8fa3;--accent:#6c5ce7;--accent2:#00cec9;--green:#00b894;--red:#e17055;--yellow:#fdcb6e;--radius:10px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);height:100vh;overflow:hidden;display:flex;flex-direction:column}
button{border:none;cursor:pointer;font-family:inherit;font-size:inherit}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0}
.header-left{display:flex;align-items:center;gap:16px}
.header-left h1{font-size:18px;font-weight:600;letter-spacing:.3px}
.status-dot{width:10px;height:10px;border-radius:50%;display:inline-block;transition:.3s}
.status-dot.idle{background:var(--text2)}
.status-dot.listening{background:var(--green);box-shadow:0 0 8px var(--green)}
.status-dot.processing{background:var(--yellow);box-shadow:0 0 8px var(--yellow)}
.status-dot.speaking{background:var(--accent);box-shadow:0 0 8px var(--accent)}
.status-dot.error{background:var(--red);box-shadow:0 0 8px var(--red)}
.status-label{font-size:13px;color:var(--text2);margin-left:6px}
.mic-btn{width:38px;height:38px;border-radius:50%;background:var(--surface2);color:var(--text2);font-size:18px;display:flex;align-items:center;justify-content:center;transition:.3s}
.mic-btn.active{background:var(--accent);color:#fff;box-shadow:0 0 16px var(--accent)}
.mic-btn:hover{background:var(--accent);color:#fff}
.interim{font-size:13px;color:var(--text2);min-height:20px;padding:4px 12px;text-align:center;border-top:1px solid var(--border);background:var(--surface2);flex-shrink:0}
.dashboard{display:flex;flex:1;overflow:hidden}
.sidebar{width:200px;background:var(--surface);border-right:1px solid var(--border);padding:12px 0;flex-shrink:0;overflow-y:auto}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 20px;color:var(--text2);font-size:14px;transition:.2s;border-left:3px solid transparent}
.nav-item:hover{background:var(--surface2);color:var(--text)}
.nav-item.active{color:var(--accent);background:var(--surface2);border-left-color:var(--accent)}
.nav-item .icon{font-size:16px;width:20px;text-align:center}
.main{flex:1;padding:20px 24px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;display:flex;flex-direction:column;gap:4px}
.stat-card .label{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px}
.stat-card .value{font-size:26px;font-weight:700}
.stat-card .change{font-size:12px;display:flex;align-items:center;gap:4px}
.stat-card .change.up{color:var(--green)}
.stat-card .change.down{color:var(--red)}
.chart-grid{display:grid;grid-template-columns:2fr 1fr;gap:14px;flex:1}
.chart-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;display:flex;flex-direction:column}
.chart-box .title{font-size:13px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.chart-area{flex:1;display:flex;align-items:flex-end;gap:4px;padding:8px 0;position:relative}
.bar{flex:1;background:linear-gradient(to top,var(--accent),rgba(108,92,231,.4));border-radius:3px 3px 0 0;transition:.5s;min-height:4px;position:relative}
.bar:hover{opacity:.8}
.bar .bar-label{position:absolute;bottom:-20px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--text2);white-space:nowrap}
.bar .bar-value{position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--text);font-weight:600}
.donut-box{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;gap:12px}
.donut-svg{width:140px;height:140px;transform:rotate(-90deg)}
.legend{display:flex;flex-direction:column;gap:4px;font-size:12px}
.legend-item{display:flex;align-items:center;gap:6px}
.legend-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.data-table{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px}
.data-table .title{font-size:13px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:8px 10px;color:var(--text2);font-weight:500;border-bottom:1px solid var(--border)}
td{padding:8px 10px;border-bottom:1px solid var(--border2,#1e2130)}
tr:last-child td{border-bottom:none}
tr:hover td{background:var(--surface2)}
.filter-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.filter-tag{background:var(--surface2);border:1px solid var(--border);border-radius:20px;padding:4px 12px;font-size:12px;color:var(--text2);display:flex;align-items:center;gap:6px}
.filter-tag .remove{cursor:pointer;opacity:.6;font-size:14px}
.filter-tag .remove:hover{opacity:1}
.filter-tag.active{background:var(--accent);border-color:var(--accent);color:#fff}
.command-overlay{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:var(--surface);border:1px solid var(--accent);border-radius:12px;padding:14px 20px;max-width:480px;width:90%;box-shadow:0 8px 32px rgba(0,0,0,.5);transition:.4s;opacity:0;pointer-events:none;z-index:100}
.command-overlay.visible{opacity:1;pointer-events:auto}
.command-overlay .s-title{font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.command-overlay .s-list{display:flex;flex-wrap:wrap;gap:6px}
.command-overlay .s-item{background:var(--surface2);border:1px solid var(--border);border-radius:16px;padding:4px 12px;font-size:12px;color:var(--text2);transition:.2s}
.command-overlay .s-item:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.voice-feedback{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:8px 16px;font-size:13px;color:var(--text);max-width:600px;box-shadow:0 4px 20px rgba(0,0,0,.4);transition:.3s;opacity:0;pointer-events:none;z-index:99}
.voice-feedback.visible{opacity:1;pointer-events:auto}
.voice-feedback .close-fb{float:right;margin-left:8px;opacity:.5;cursor:pointer;font-size:16px}
.voice-feedback .close-fb:hover{opacity:1}
.confidence-badge{font-size:11px;padding:2px 8px;border-radius:10px;margin-left:8px;display:inline-block}
.confidence-badge.high{background:var(--green);color:#fff}
.confidence-badge.med{background:var(--yellow);color:#1a1d28}
.confidence-badge.low{background:var(--red);color:#fff}
@media(max-width:768px){.stats-row{grid-template-columns:repeat(2,1fr)}.chart-grid{grid-template-columns:1fr}.sidebar{width:56px}.sidebar .nav-text{display:none}.sidebar .nav-item{padding:10px;justify-content:center}}
</style>
</head>
<body>
<div class="header">
<div class="header-left">
<span class="status-dot idle" id="statusDot"></span>
<span class="status-label" id="statusLabel">idle</span>
<h1>Voice Dashboard</h1>
</div>
<div style="display:flex;align-items:center;gap:12px">
<button class="mic-btn" id="micBtn" title="Toggle microphone">🎤</button>
</div>
</div>
<div class="interim" id="interimText">Say "help" or click the mic to start</div>
<div class="dashboard">
<div class="sidebar" id="sidebar">
<div class="nav-item active" data-section="overview"><span class="icon">📊</span><span class="nav-text">Overview</span></div>
<div class="nav-item" data-section="revenue"><span class="icon">💰</span><span class="nav-text">Revenue</span></div>
<div class="nav-item" data-section="users"><span class="icon">👥</span><span class="nav-text">Users</span></div>
<div class="nav-item" data-section="performance"><span class="icon">⚡</span><span class="nav-text">Performance</span></div>
<div class="nav-item" data-section="alerts"><span class="icon">🔔</span><span class="nav-text">Alerts</span></div>
</div>
<div class="main" id="mainContent">
<div class="stats-row" id="statsRow">
<div class="stat-card"><div class="label">Revenue</div><div class="value" id="statRevenue">$1.42M</div><div class="change up">▲ 12.3%</div></div>
<div class="stat-card"><div class="label">Users</div><div class="value" id="statUsers">84,291</div><div class="change up">▲ 8.7%</div></div>
<div class="stat-card"><div class="label">Conversion</div><div class="value" id="statConversion">3.42%</div><div class="change up">▲ 1.2%</div></div>
<div class="stat-card"><div class="label">Error Rate</div><div class="value" id="statErrors">0.87%</div><div class="change down">▼ 0.3%</div></div>
</div>
<div class="filter-bar" id="filterBar"></div>
<div class="chart-grid">
<div class="chart-box">
<div class="title">Monthly Revenue by Region</div>
<div class="chart-area" id="barChart"></div>
</div>
<div class="chart-box">
<div class="title">Traffic Sources</div>
<div class="donut-box"><svg class="donut-svg" id="donutSvg" viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.915" fill="none" stroke="var(--surface2)" stroke-width="3"></circle></svg><div class="legend" id="donutLegend"></div></div>
</div>
</div>
<div class="data-table">
<div class="title">Top Campaigns</div>
<table id="campaignTable"><thead><tr><th>Campaign</th><th>Spend</th><th>Impressions</th><th>Clicks</th><th>Conv.</th></tr></thead><tbody id="tableBody"></tbody></table>
</div>
</div>
</div>
<div class="command-overlay" id="commandOverlay">
<div class="s-title">Voice Commands</div>
<div class="s-list" id="suggestionList"></div>
</div>
<div class="voice-feedback" id="voiceFeedback">
<span class="close-fb" id="closeFb">✕</span>
<span id="feedbackText"></span>
</div>
<script>
(function(){
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList;
const STATE={LISTENING:'listening',PROCESSING:'processing',SPEAKING:'speaking',IDLE:'idle',ERROR:'error'};
class VoiceContext {
constructor(){
this.lastCommand=null;
this.lastEntity=null;
this.lastFilter=null;
this.lastIntent=null;
this.currentSection='overview';
this.history=[];
this.alerts=[];
this.filterTags=[];
}
setSection(s){this.currentSection=s;}
getSection(){return this.currentSection;}
push(cmd){this.history.push({...cmd,timestamp:Date.now()});if(this.history.length>50)this.history.shift();this.lastCommand=cmd;}
resolveReference(token){const h=this.history;if(!h.length)return null;const last=h[h.length-1];if(token==='that'||token==='this'||token==='those')return last.entity||last.filter||null;if(token==='it')return last.entity||null;return null;}
}
const ctx=new VoiceContext();
const sections=['overview','revenue','users','performance','alerts'];
const sectionAliases={overview:['overview','home','main dashboard','dashboard','main'],revenue:['revenue','earnings','money','sales','income'],users:['users','user','audience','visitors','traffic'],performance:['performance','speed','latency','uptime'],alerts:['alerts','alert','notifications','notify']};
const regions=['north america','europe','asia pacific','latin america','middle east','africa'];
const metrics=['revenue','users','conversion','error rate','impressions','clicks','spend','cost per click','ctr','roi'];
const formats=['pdf','csv','png','excel','json'];
const timePeriods=['today','yesterday','this week','last week','this month','last month','this quarter','last quarter','this year','last year','q1','q2','q3','q4'];
const campaignData=[
{name:'Summer Launch',spend:'$28,400',imp:'245K',clicks:'8,920',conv:'3.8%'},
{name:'Brand Awareness',spend:'$18,200',imp:'512K',clicks:'12,300',conv:'1.9%'},
{name:'Retargeting Q3',spend:'$12,800',imp:'89K',clicks:'4,560',conv:'5.2%'},
{name:'Holiday Preview',spend:'$9,600',imp:'134K',clicks:'6,210',conv:'4.1%'},
{name:'Partner Program',spend:'$7,300',imp:'67K',clicks:'2,840',conv:'6.7%'}
];
const barData={labels:['NA','EU','APAC','LATAM','MEA','AFR'],values:[420,380,310,180,95,52]};
const donutData={labels:['Direct','Organic','Social','Paid','Referral'],values:[35,28,18,12,7],colors:['#6c5ce7','#00cec9','#00b894','#e17055','#fdcb6e']};
function setStatus(state,msg){
const dot=document.getElementById('statusDot');
const label=document.getElementById('statusLabel');
dot.className='status-dot '+state;
label.textContent=msg||state;
}
function showInterim(t){document.getElementById('interimText').textContent=t||'';}
function showFeedback(text){
const el=document.getElementById('voiceFeedback');
document.getElementById('feedbackText').textContent=text;
el.classList.add('visible');
clearTimeout(el._hide);
el._hide=setTimeout(()=>el.classList.remove('visible'),4000);
}
document.getElementById('closeFb').onclick=()=>document.getElementById('voiceFeedback').classList.remove('visible');
function speak(text){
return new Promise((res)=>{
if(!window.speechSynthesis){res();return;}
setStatus(STATE.SPEAKING,'speaking');
const u=new SpeechSynthesisUtterance(text);
u.rate=1;u.pitch=1;u.volume=1;
u.onend=()=>{setStatus(STATE.LISTENING,'listening');res();};
u.onerror=()=>{setStatus(STATE.LISTENING,'listening');res();};
window.speechSynthesis.speak(u);
showFeedback('🔊 '+text);
});
}
function renderBars(data,filterRegion){
let labels=data.labels,values=data.values;
if(filterRegion&&filterRegion!=='all'){
const idx=labels.map(l=>l.toLowerCase()).indexOf(filterRegion.toLowerCase());
if(idx>=0){labels=[labels[idx]];values=[values[idx]];}
}
const max=Math.max(...values,1);
const el=document.getElementById('barChart');el.innerHTML='';
labels.forEach((l,i)=>{
const h=(values[i]/max)*100;
const bar=document.createElement('div');bar.className='bar';bar.style.height=h+'%';
if(filterRegion&&filterRegion!=='all'&&l.toLowerCase()!==filterRegion.toLowerCase())bar.style.opacity='0.15';
const lbl=document.createElement('div');lbl.className='bar-label';lbl.textContent=l;
const val=document.createElement('div');val.className='bar-value';val.textContent=values[i]+'K';
bar.appendChild(val);bar.appendChild(lbl);el.appendChild(bar);
});
}
function renderDonut(data,filterSource){
const svg=document.getElementById('donutSvg');const lg=document.getElementById('donutLegend');
let labels=data.labels,values=data.values,cols=data.colors;
if(filterSource&&filterSource!=='all'){
const idx=labels.map(l=>l.toLowerCase()).indexOf(filterSource.toLowerCase());
if(idx>=0){
const total=values.reduce((a,b)=>a+b,0);
svg.innerHTML=`<circle cx="21" cy="21" r="15.915" fill="none" stroke="${cols[idx]}" stroke-width="3" stroke-dasharray="${(values[idx]/total)*100} 100"></circle>`;
lg.innerHTML=`<div class="legend-item"><span class="legend-dot" style="background:${cols[idx]}"></span>${labels[idx]} ${Math.round(values[idx]/total*100)}%</div>`;
return;
}
}
const total=values.reduce((a,b)=>a+b,0);let cum=0;
svg.innerHTML=`<circle cx="21" cy="21" r="15.915" fill="none" stroke="var(--surface2)" stroke-width="3"></circle>`;
values.forEach((v,i)=>{
const pct=v/total;const offset=cum*100;const len=pct*100;
const circle=document.createElementNS('http://www.w3.org/2000/svg','circle');
circle.setAttribute('cx','21');circle.setAttribute('cy','21');circle.setAttribute('r','15.915');
circle.setAttribute('fill','none');circle.setAttribute('stroke',cols[i]);circle.setAttribute('stroke-width','3');
circle.setAttribute('stroke-dasharray',len+' '+(100-len));circle.setAttribute('stroke-dashoffset',-offset);
svg.appendChild(circle);cum+=pct;
});
lg.innerHTML=labels.map((l,i)=>`<div class="legend-item"><span class="legend-dot" style="background:${cols[i]}"></span>${l} ${Math.round(values[i]/total*100)}%</div>`).join('');
}
function renderTable(data,filter){
let rows=data;
if(filter){const f=filter.toLowerCase();rows=rows.filter(r=>r.name.toLowerCase().includes(f)||r.spend.toLowerCase().includes(f)||r.imp.toLowerCase().includes(f));}
const tbody=document.getElementById('tableBody');
tbody.innerHTML=rows.map(r=>`<tr><td>${r.name}</td><td>${r.spend}</td><td>${r.imp}</td><td>${r.clicks}</td><td>${r.conv}</td></tr>`).join('');
}
function renderAll(){
renderBars(barData,ctx.lastFilter&&ctx.lastFilter.type==='region'?ctx.lastFilter.value:null);
renderDonut(donutData,ctx.lastFilter&&ctx.lastFilter.type==='source'?ctx.lastFilter.value:null);
renderTable(campaignData,ctx.lastFilter&&ctx.lastFilter.type==='campaign'?ctx.lastFilter.value:null);
renderFilterTags();
}
function renderFilterTags(){
const bar=document.getElementById('filterBar');
if(!ctx.filterTags.length){bar.innerHTML='';return;}
bar.innerHTML=ctx.filterTags.map((t,i)=>`<span class="filter-tag active">${t.icon||''} ${t.label} <span class="remove" data-idx="${i}">✕</span></span>`).join('');
bar.querySelectorAll('.remove').forEach(el=>el.onclick=()=>{ctx.filterTags.splice(parseInt(el.dataset.idx),1);if(!ctx.filterTags.length)ctx.lastFilter=null;renderAll();});
}
function matchToken(token,intent){
const t=token.toLowerCase();
if(intent==='section'){for(const[k,aliases]of Object.entries(sectionAliases)){if(aliases.includes(t))return k;}}
if(intent==='region'){for(const r of regions){if(r.includes(t)||t.includes(r))return r;}return null;}
if(intent==='metric'){for(const m of metrics){if(m.includes(t)||t.includes(m))return m;}return null;}
if(intent==='format'){for(const f of formats){if(f.includes(t))return f;}return null;}
if(intent==='time'){for(const p of timePeriods){if(p===t||p.includes(t)||t.includes(p))return p;}return null;}
return null;
}
function parseCommand(text){
const t=text.toLowerCase().replace(/[.,!?]+/g,'').trim();
const cmd={raw:text,intent:null,entity:null,params:{},confidence:0};
// Navigate
const navMatch=t.match(/(?:go\s+to|show|navigate\s+to|open|switch\s+to|view)\s+(.+)/);
if(navMatch){
const sec=matchToken(navMatch[1].trim(),'section');
if(sec){cmd.intent='navigate';cmd.entity=sec;cmd.confidence=.95;return cmd;}
}
// Filter: "filter [by/on] X to Y" or "filter [that/this] to X" or "show only X"
let filterMatch=t.match(/filter\s+(?:by|on|to|for)?\s*(.+?)(?:\s+to\s+(.+))?$/);
if(!filterMatch)filterMatch=t.match(/show\s+only\s+(.+)/);
if(!filterMatch)filterMatch=t.match(/only\s+(.+)/);
if(filterMatch){
const val=filterMatch[1]||filterMatch;const sv=val.trim();
const region=matchToken(sv,'region');
if(region){cmd.intent='filter';cmd.entity=region;cmd.params={type:'region',value:region};cmd.confidence=.9;return cmd;}
const sourceMatch=donutData.labels.find(l=>l.toLowerCase().includes(sv)||sv.includes(l.toLowerCase()));
if(sourceMatch){cmd.intent='filter';cmd.entity=sourceMatch;cmd.params={type:'source',value:sourceMatch};cmd.confidence=.85;return cmd;}
const campMatch=campaignData.find(c=>c.name.toLowerCase().includes(sv));
if(campMatch){cmd.intent='filter';cmd.entity=campMatch.name;cmd.params={type:'campaign',value:campMatch.name};cmd.confidence=.85;return cmd;}
cmd.intent='filter';cmd.entity=sv;cmd.params={type:'generic',value:sv};cmd.confidence=.7;return cmd;
}
// Resolve "that" / "this" references
const refMatch=t.match(/(?:filter|show|export)\s+(that|this|those|it)(?:\s+to\s+(.+))?/);
if(refMatch){
const resolved=ctx.resolveReference(refMatch[1]);
if(resolved){
cmd.intent='filter';cmd.entity=resolved;cmd.params={type:'resolved',value:resolved,from:refMatch[2]||null};cmd.confidence=.8;
if(refMatch[2])cmd.params.value=refMatch[2];return cmd;
}
}
// Query / Ask
const qMatch=t.match(/(?:what\s+(?:is|are|was|were)|show\s+me|how\s+(?:many|much)|tell\s+me)\s+(.+)/);
if(qMatch){
const qv=qMatch[1].trim();
const met=matchToken(qv,'metric');
if(met){cmd.intent='query';cmd.entity=met;cmd.confidence=.9;return cmd;}
cmd.intent='query';cmd.entity=qv;cmd.confidence=.7;return cmd;
}
// Time period comparison
const compMatch=t.match(/compare\s+(.+?)\s+(?:and|vs?\.?|to)\s+(.+)/);
if(compMatch){
cmd.intent='compare';cmd.params={a:compMatch[1].trim(),b:compMatch[2].trim()};cmd.confidence=.85;
const ta=matchToken(compMatch[1].trim(),'time');const tb=matchToken(compMatch[2].trim(),'time');
if(ta&&tb){cmd.entity=[ta,tb];}return cmd;
}
const timeMatch=t.match(/(?:last|this|next)\s+(month|quarter|week|year|day)/);
if(timeMatch&&!cmd.intent){
cmd.intent='time';cmd.entity=timeMatch[0];cmd.confidence=.8;return cmd;
}
// Export
const expMatch=t.match(/export\s+(?:this|that|view|as)?\s*(.+)?/);
if(expMatch){
const fmt=expMatch[1]?matchToken(expMatch[1].trim(),'format'):'pdf';
cmd.intent='export';cmd.entity=fmt||'pdf';cmd.confidence=.85;return cmd;
}
// Alert
const alertMatch=t.match(/alert\s+me\s+(?:when|if)\s+(.+)/);
if(alertMatch){
cmd.intent='alert';cmd.entity=alertMatch[1].trim();cmd.confidence=.8;return cmd;
}
// Help
if(t.match(/^(help|commands|what can I say|show commands)/)){
cmd.intent='help';cmd.confidence=.95;return cmd;
}
// Clear filters
if(t.match(/clear\s+(?:all\s+)?filter/)){
cmd.intent='clear';cmd.confidence=.9;return cmd;
}
cmd.confidence=.3;
return cmd;
}
function executeCommand(cmd){
if(cmd.confidence<.5){
speak("I did not catch that clearly. Please try again.");
showInterim('Low confidence: '+cmd.raw);
return;
}
const pct=Math.round(cmd.confidence*100);
setStatus(STATE.PROCESSING,'processing');
ctx.push(cmd);
switch(cmd.intent){
case 'navigate':
navigateTo(cmd.entity);
speak("Navigating to "+cmd.entity+" section.");
break;
case 'filter':
applyFilter(cmd);
break;
case 'query':
handleQuery(cmd);
break;
case 'compare':
speak("Comparing "+cmd.params.a+" and "+cmd.params.b+". Showing data overlay.");
navigateTo('overview');
break;
case 'time':
speak("Showing "+cmd.entity+" data.");
navigateTo('overview');
break;
case 'export':
speak("Exporting current view as "+cmd.entity.toUpperCase()+".");
showFeedback("📥 Exporting as "+cmd.entity.toUpperCase()+"...");
break;
case 'alert':
const aId=Date.now();
ctx.alerts.push({id:aId,condition:cmd.entity,active:true});
speak("Alert created for: "+cmd.entity+". I will notify you when triggered.");
navigateTo('alerts');
break;
case 'help':
showSuggestions(true);
speak("You can say: navigate to a section like Revenue or Users, filter by region or source, query metrics, compare time periods, export the view, or set alerts. Try saying something now.");
break;
case 'clear':
ctx.filterTags=[];ctx.lastFilter=null;renderAll();
speak("All filters cleared.");
break;
default:
speak("Command not recognized. Try saying: show Revenue, filter by Europe, or export as PDF.");
}
renderAll();
showInterim('');
}
function navigateTo(section){
const s=section.toLowerCase();
if(!sections.includes(s))return;
ctx.setSection(s);
document.querySelectorAll('.nav-item').forEach(el=>el.classList.toggle('active',el.dataset.section===s));
setStatus(STATE.LISTENING,'listening');
renderSectionContent(s);
}
function renderSectionContent(section){
const main=document.getElementById('mainContent');
switch(section){
case 'overview':
main.innerHTML=`<div class="stats-row" id="statsRow"><div class="stat-card"><div class="label">Revenue</div><div class="value" id="statRevenue">$1.42M</div><div class="change up">▲ 12.3%</div></div><div class="stat-card"><div class="label">Users</div><div class="value" id="statUsers">84,291</div><div class="change up">▲ 8.7%</div></div><div class="stat-card"><div class="label">Conversion</div><div class="value" id="statConversion">3.42%</div><div class="change up">▲ 1.2%</div></div><div class="stat-card"><div class="label">Error Rate</div><div class="value" id="statErrors">0.87%</div><div class="change down">▼ 0.3%</div></div></div><div class="filter-bar" id="filterBar"></div><div class="chart-grid"><div class="chart-box"><div class="title">Monthly Revenue by Region</div><div class="chart-area" id="barChart"></div></div><div class="chart-box"><div class="title">Traffic Sources</div><div class="donut-box"><svg class="donut-svg" id="donutSvg" viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.915" fill="none" stroke="var(--surface2)" stroke-width="3"></circle></svg><div class="legend" id="donutLegend"></div></div></div></div><div class="data-table"><div class="title">Top Campaigns</div><table id="campaignTable"><thead><tr><th>Campaign</th><th>Spend</th><th>Impressions</th><th>Clicks</th><th>Conv.</th></tr></thead><tbody id="tableBody"></tbody></table></div>`;
renderAll();
break;
case 'revenue':
main.innerHTML=`<div class="stats-row"><div class="stat-card"><div class="label">Total Revenue</div><div class="value">$1.42M</div><div class="change up">▲ 12.3%</div></div><div class="stat-card"><div class="label">ARR</div><div class="value">$5.68M</div><div class="change up">▲ 15.1%</div></div><div class="stat-card"><div class="label">MRR</div><div class="value">$473K</div><div class="change up">▲ 2.4%</div></div><div class="stat-card"><div class="label">Churn</div><div class="value">4.2%</div><div class="change down">▼ 0.7%</div></div></div><div class="chart-grid"><div class="chart-box"><div class="title">Revenue Trend (12mo)</div><div class="chart-area" id="barChart"></div></div><div class="chart-box"><div class="title">Revenue by Product</div><div class="donut-box"><svg class="donut-svg" viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.915" fill="none" stroke="var(--surface2)" stroke-width="3"></circle><circle cx="21" cy="21" r="15.915" fill="none" stroke="#6c5ce7" stroke-width="3" stroke-dasharray="45 55"></circle><circle cx="21" cy="21" r="15.915" fill="none" stroke="#00cec9" stroke-width="3" stroke-dasharray="30 70" stroke-dashoffset="-45"></circle><circle cx="21" cy="21" r="15.915" fill="none" stroke="#fdcb6e" stroke-width="3" stroke-dasharray="25 75" stroke-dashoffset="-75"></circle></svg><div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6c5ce7"></span>SaaS 45%</div><div class="legend-item"><span class="legend-dot" style="background:#00cec9"></span>Services 30%</div><div class="legend-item"><span class="legend-dot" style="background:#fdcb6e"></span>Licensing 25%</div></div></div></div></div>`;
setTimeout(()=>{const ch=document.getElementById('barChart');if(ch)renderBars(barData,ctx.lastFilter?.value);},50);
break;
case 'users':
main.innerHTML=`<div class="stats-row"><div class="stat-card"><div class="label">Active Users</div><div class="value">84,291</div><div class="change up">▲ 8.7%</div></div><div class="stat-card"><div class="label">New Signups</div><div class="value">12,450</div><div class="change up">▲ 14.2%</div></div><div class="stat-card"><div class="label">DAU/MAU</div><div class="value">0.31</div><div class="change up">▲ 3%</div></div><div class="stat-card"><div class="label">Avg Session</div><div class="value">4m 32s</div><div class="change up">▲ 12s</div></div></div><div class="data-table"><div class="title">User Growth by Cohort</div><table><thead><tr><th>Cohort</th><th>Size</th><th>Retention D7</th><th>Retention D30</th><th>LTV</th></tr></thead><tbody><tr><td>Q1 2026</td><td>22,410</td><td>68%</td><td>42%</td><td>$320</td></tr><tr><td>Q4 2025</td><td>19,820</td><td>71%</td><td>45%</td><td>$295</td></tr><tr><td>Q3 2025</td><td>17,300</td><td>65%</td><td>38%</td><td>$270</td></tr><tr><td>Q2 2025</td><td>14,750</td><td>69%</td><td>41%</td><td>$255</td></tr></tbody></table></div>`;
break;
case 'performance':
main.innerHTML=`<div class="stats-row"><div class="stat-card"><div class="label">Avg Response</div><div class="value">124ms</div><div class="change up">▲ 8ms</div></div><div class="stat-card"><div class="label">P99 Latency</div><div class="value">890ms</div><div class="change down">▼ 45ms</div></div><div class="stat-card"><div class="label">Uptime</div><div class="value">99.97%</div><div class="change up">▲ 0.02%</div></div><div class="stat-card"><div class="label">Error Budget</div><div class="value">87%</div><div class="change up">▲ 5%</div></div></div><div class="chart-box" style="flex:1"><div class="title">P99 Latency (24h)</div><div class="chart-area" id="barChart"></div></div>`;
setTimeout(()=>{const ch=document.getElementById('barChart');if(ch)renderBars(barData,ctx.lastFilter?.value);},50);
break;
case 'alerts':
const alertList=ctx.alerts.length?ctx.alerts.map(a=>`<div style="padding:10px;background:var(--surface2);border-radius:6px;margin-bottom:6px;border-left:3px solid ${a.active?'var(--accent)':'var(--text2)'}">${a.active?'🔔':'🔕'} "${a.condition}" — ${a.active?'Active':'Disabled'}</div>`).join(''):'<div style="color:var(--text2);padding:20px;text-align:center">No alerts set. Try saying: "Alert me when error rate exceeds 5 percent"</div>';
main.innerHTML=`<div class="stats-row"><div class="stat-card"><div class="label">Active Alerts</div><div class="value">${ctx.alerts.filter(a=>a.active).length}</div></div><div class="stat-card"><div class="label">Total Triggered</div><div class="value">0</div></div><div class="stat-card"><div class="label">Last Alert</div><div class="value">—</div></div><div class="stat-card"><div class="label">Notification</div><div class="value">Speech</div></div></div><div class="data-table" style="flex:1"><div class="title">Alert Rules</div>${alertList}</div>`;
break;
}
}
function applyFilter(cmd){
const p=cmd.params||{};
const label=p.value||cmd.entity;
const existing=ctx.filterTags.findIndex(t=>t.label.toLowerCase()===label.toLowerCase());
if(existing>=0){
ctx.filterTags.splice(existing,1);
} else {
ctx.filterTags.push({label,type:p.type||'generic',icon:p.type==='region'?'🌍':p.type==='source'?'🔗':'🏷️'});
}
if(p.type==='region')ctx.lastFilter={type:'region',value:p.value};
else if(p.type==='source')ctx.lastFilter={type:'source',value:p.value};
else if(p.type==='campaign')ctx.lastFilter={type:'campaign',value:p.value};
else ctx.lastFilter={type:'generic',value:p.value};
renderAll();
speak("Applied filter: "+label);
}
function handleQuery(cmd){
const e=cmd.entity;
let answer='';
switch(e?.toLowerCase()){
case'revenue':answer='Current revenue is 1.42 million dollars, up 12.3 percent from last quarter.';break;
case'users':answer='We have 84,291 active users, up 8.7 percent month over month.';break;
case'conversion':answer='Conversion rate is 3.42 percent, up 1.2 percent.';break;
case'error rate':answer='Error rate is 0.87 percent, down 0.3 percent from last week.';break;
case'impressions':answer='Total impressions this month are 1.05 million.';break;
case'clicks':answer='Total clicks this month are 34,830.';break;
case'spend':answer='Total ad spend this month is 76,300 dollars.';break;
default:answer='Showing metrics for '+e+'. Data updated as of today.';
}
speak(answer);
}
function showSuggestions(force){
const ov=document.getElementById('commandOverlay');
const list=document.getElementById('suggestionList');
const sections=getContextualSuggestions();
list.innerHTML=sections.map(s=>`<span class="s-item">${s}</span>`).join('');
ov.classList.add('visible');
clearTimeout(ov._hide);
if(!force)ov._hide=setTimeout(()=>ov.classList.remove('visible'),8000);
}
function getContextualSuggestions(){
const sec=ctx.getSection();
const base=['Navigate to Revenue','Filter by Europe','Export as PDF','Set alert on errors','Compare Q3 and Q4'];
switch(sec){
case'revenue':return['Show revenue by region','Filter to North America','Compare Q3 and Q4','Export as CSV','What is MRR?'];
case'users':return['Show new signups','Filter by cohort','What is retention?','Show DAU trend'];
case'performance':return['Show latency breakdown','Filter to P99','What is error budget?','Export as PNG'];
case'alerts':return['Alert me when error rate exceeds 5%','Clear all alerts','Show alert history'];
default:return base;
}
}
let recognition=null;
let isListening=false;
function initSpeech(){
if(!SpeechRecognition){
document.getElementById('interimText').textContent='Speech recognition not supported in this browser. Use Chrome or Edge.';
setStatus(STATE.ERROR,'not supported');
return;
}
recognition=new SpeechRecognition();
recognition.continuous=true;
recognition.interimResults=true;
recognition.lang='en-US';
recognition.maxAlternatives=3;
recognition.onresult=function(e){
let interim='',final='',bestConfidence=0,best='';
for(let i=e.resultIndex;i<e.results.length;i++){
const r=e.results[i];
if(r.isFinal){
const txt=r[0].transcript.trim();
const conf=r[0].confidence;
if(conf>bestConfidence){bestConfidence=conf;best=txt;}
final+=txt+' ';
} else {
interim+=r[0].transcript;
}
}
if(interim)showInterim('🎤 '+interim);
if(best&&bestConfidence>.4){
showInterim('✅ '+best+' ('+Math.round(bestConfidence*100)+'%)');
const cmd=parseCommand(best);
cmd.confidence=Math.min(cmd.confidence,bestConfidence);
executeCommand(cmd);
}
};
recognition.onerror=function(e){
if(e.error==='no-speech')return;
setStatus(STATE.ERROR,'error: '+e.error);
showInterim('Error: '+e.error);
if(e.error==='not-allowed'){isListening=false;document.getElementById('micBtn').classList.remove('active');}
};
recognition.onend=function(){
if(isListening){
try{recognition.start();}catch(e){}
}
};
recognition.onaudiostart=()=>setStatus(STATE.LISTENING,'listening');
}
function toggleMic(){
const btn=document.getElementById('micBtn');
if(!recognition){initSpeech();if(!recognition)return;}
if(isListening){
recognition.stop();isListening=false;btn.classList.remove('active');
setStatus(STATE.IDLE,'idle');
showInterim('Microphone paused');
} else {
try{recognition.start();isListening=true;btn.classList.add('active');setStatus(STATE.LISTENING,'listening');showInterim('Listening...');}catch(e){showInterim('Error: '+e.message);}
}
}
document.getElementById('micBtn').onclick=toggleMic;
document.querySelectorAll('.nav-item').forEach(el=>el.onclick=()=>{navigateTo(el.dataset.section);speak("Switched to "+el.dataset.section);});
let suggestTimer=null;
function startSuggestTimer(){
clearInterval(suggestTimer);
suggestTimer=setInterval(()=>{
if(!isListening&&!document.getElementById('commandOverlay').classList.contains('visible')){
showSuggestions(false);
}
},15000);
}
renderAll();
initSpeech();
startSuggestTimer();
document.addEventListener('keydown',e=>{
if(e.key==='m'&&e.ctrlKey){e.preventDefault();toggleMic();}
if(e.key==='Escape'){document.getElementById('commandOverlay').classList.remove('visible');document.getElementById('voiceFeedback').classList.remove('visible');}
});
window._voiceContext=ctx;
window._voiceDebug={parseCommand,executeCommand,navigateTo,speak,renderAll};
console.log('Voice Dashboard ready. Ctrl+M to toggle mic, Escape to dismiss overlays.');
})();
</script>
</body>
</html>
```