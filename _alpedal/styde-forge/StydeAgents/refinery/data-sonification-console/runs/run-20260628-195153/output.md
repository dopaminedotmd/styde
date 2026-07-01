```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Data Sonification Console</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#c0c8e0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:20px}
h1{font-size:18px;font-weight:300;letter-spacing:3px;text-transform:uppercase;color:#6a7a9a;margin-bottom:24px;text-align:center}
h1 span{color:#4af;font-weight:600}
.dashboard{width:100%;max-width:780px;display:flex;flex-direction:column;gap:12px}
.metrics{display:flex;gap:10px;flex-wrap:wrap}
.metric{flex:1;min-width:200px;background:#12121c;border:1px solid #1e2a3a;border-radius:8px;padding:14px;position:relative}
.metric.revenue{border-left:3px solid #f80}
.metric.errors{border-left:3px solid #f44}
.metric.users{border-left:3px solid #4af}
.metric .label{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#5a6a8a;margin-bottom:6px}
.metric .value{font-size:28px;font-weight:300;margin-bottom:8px}
.metric .value.revenue-v{color:#f80}
.metric .value.errors-v{color:#f44}
.metric .value.users-v{color:#4af}
.channel-controls{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.channel-controls button{background:transparent;border:1px solid #2a3a4a;color:#7a8aaa;padding:4px 10px;border-radius:4px;font-size:10px;cursor:pointer;transition:all 0.15s}
.channel-controls button:hover{border-color:#4af;color:#4af}
.channel-controls button.muted{background:#f44;color:#fff;border-color:#f44}
.channel-controls button.soloed{background:#4af;color:#fff;border-color:#4af}
.channel-controls input[type=range]{width:80px;height:4px;-webkit-appearance:none;appearance:none;background:#1e2a3a;border-radius:2px;outline:none}
.channel-controls input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:12px;height:12px;border-radius:50%;background:#4af;cursor:pointer}
.status-bar{display:flex;gap:10px;align-items:center;padding:8px 14px;background:#12121c;border:1px solid #1e2a3a;border-radius:8px;font-size:11px;color:#5a6a8a;flex-wrap:wrap}
.status-bar .health{display:flex;align-items:center;gap:6px}
.health-indicator{width:8px;height:8px;border-radius:50%;transition:background 1s}
.health-indicator.good{background:#0b6}
.health-indicator.warning{background:#fa0}
.health-indicator.critical{background:#f22}
.status-bar button{background:transparent;border:1px solid #2a3a4a;color:#7a8aaa;padding:3px 10px;border-radius:4px;font-size:10px;cursor:pointer;transition:all 0.15s}
.status-bar button.active{border-color:#4af;color:#4af;background:rgba(68,170,255,0.08)}
.status-bar .pull-right{margin-left:auto}
.status-bar .vis-indicator{display:inline-block;width:60px;height:4px;border-radius:2px;background:#1e2a3a;position:relative}
.status-bar .vis-indicator .bar{height:100%;border-radius:2px;transition:width 0.3s;background:linear-gradient(90deg,#4af,#0b6)}
.events-log{margin-top:4px;padding:10px 14px;background:#0e0e16;border:1px solid #1a2a3a;border-radius:6px;font-size:11px;font-family:'Consolas','Courier New',monospace;color:#3a4a6a;min-height:44px;max-height:80px;overflow-y:auto}
.events-log .ev{color:#8a9aba;margin-bottom:2px}
.events-log .ev.pos{color:#0b6}
.events-log .ev.neg{color:#f44}
.sim-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding:8px 14px;background:#12121c;border:1px solid #1e2a3a;border-radius:8px;font-size:11px}
.sim-controls label{color:#5a6a8a;display:flex;align-items:center;gap:6px}
.sim-controls input[type=range]{width:120px;height:4px;-webkit-appearance:none;appearance:none;background:#1e2a3a;border-radius:2px;outline:none}
.sim-controls input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:12px;height:12px;border-radius:50%;background:#f80;cursor:pointer}
.sim-controls button{background:transparent;border:1px solid #2a3a4a;color:#7a8aaa;padding:3px 12px;border-radius:4px;font-size:10px;cursor:pointer;transition:all 0.15s}
.sim-controls button:hover{border-color:#f80;color:#f80}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#0a0a0f}
::-webkit-scrollbar-thumb{background:#2a3a4a;border-radius:2px}
</style>
</head>
<body>
<div class="dashboard">
<h1>data sonification <span>console</span></h1>
<div class="sim-controls">
<label>sim speed <input type="range" id="simSpeed" min="0.5" max="5" step="0.1" value="1"></label>
<label>variance <input type="range" id="simVariance" min="0.02" max="0.4" step="0.02" value="0.1"></label>
<button id="resetBtn">reset</button>
<button id="spikeBtn">inject spike</button>
<button id="dropBtn">inject drop</button>
<span style="color:#3a4a6a;font-size:10px;margin-left:auto">ctrl+click channel solo to headphone</span>
</div>
<div class="metrics">
<div class="metric revenue">
<div class="label">revenue</div>
<div class="value revenue-v" id="revenueVal">0</div>
<div class="channel-controls">
<button id="muteRevenue">mute</button>
<button id="soloRevenue">solo</button>
<span style="color:#5a6a8a;font-size:9px">freq</span>
<input type="range" id="revenueVol" min="0" max="1" step="0.05" value="0.6">
</div>
</div>
<div class="metric errors">
<div class="label">error rate</div>
<div class="value errors-v" id="errorsVal">0</div>
<div class="channel-controls">
<button id="muteErrors">mute</button>
<button id="soloErrors">solo</button>
<span style="color:#5a6a8a;font-size:9px">noise</span>
<input type="range" id="errorsVol" min="0" max="1" step="0.05" value="0.5">
</div>
</div>
<div class="metric users">
<div class="label">active users</div>
<div class="value users-v" id="usersVal">0</div>
<div class="channel-controls">
<button id="muteUsers">mute</button>
<button id="soloUsers">solo</button>
<span style="color:#5a6a8a;font-size:9px">tempo</span>
<input type="range" id="usersVol" min="0" max="1" step="0.05" value="0.5">
</div>
</div>
</div>
<div class="status-bar">
<div class="health">
<span class="health-indicator good" id="healthDot"></span>
<span id="healthLabel">system healthy</span>
</div>
<span style="color:#5a6a8a">|</span>
<span>rev <span id="healthRev" style="color:#f80">0</span></span>
<span>err <span id="healthErr" style="color:#f44">0</span></span>
<span>usr <span id="healthUsr" style="color:#4af">0</span></span>
<span style="color:#5a6a8a">|</span>
<div class="vis-indicator"><div class="bar" id="visBar" style="width:50%"></div></div>
<div class="pull-right">
<button id="headphoneBtn">headphone mode</button>
<button id="ambientBtn" class="active">ambient on</button>
</div>
</div>
<div class="events-log" id="eventsLog">
<div class="ev">-- console ready, awaiting data stream --</div>
</div>
</div>
<script>
(function(){
'use strict';
const log = document.getElementById('eventsLog');
function addEvent(text, type){
 const div = document.createElement('div');
 div.className = 'ev' + (type ? ' ' + type : '');
 div.textContent = '[' + new Date().toLocaleTimeString() + '] ' + text;
 log.insertBefore(div, log.firstChild);
 while(log.children.length > 20) log.removeChild(log.lastChild);
}
let audioCtx = null;
function getCtx(){
 if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
 if(audioCtx.state === 'suspended') audioCtx.resume();
 return audioCtx;
}
let state = {
 revenue: 5000,
 errors: 2.5,
 users: 1200,
 baseRevenue: 5000,
 baseErrors: 2.5,
 baseUsers: 1200
};
let muted = {revenue:false, errors:false, users:false};
let soloed = {revenue:false, errors:false, users:false};
let headphoneMode = false;
let ambientOn = true;
let simSpeed = 1;
let variance = 0.1;
let running = true;
let bassOsc = null, bassGain = null;
let noiseNode = null, noiseGain = null, noiseFilter = null;
let pulseInterval = null;
let chimeTimeout = null;
let ambientNodes = [];
let prevRevenue = state.revenue;
let prevErrors = state.errors;
let prevUsers = state.users;
function getVol(channel){
 let v = parseFloat(document.getElementById(channel + 'Vol').value);
 if(muted[channel] && !soloed[channel]) v = 0;
 const anySolo = Object.values(soloed).some(x => x);
 if(anySolo && !soloed[channel]) v = 0;
 if(headphoneMode && soloed[channel]) v = Math.min(1, v * 1.4);
 return v;
}
function isAnySound(){
 if(Object.values(soloed).some(x => x)) return true;
 return !Object.values(muted).every(x => x);
}
function initAudio(){
 const ctx = getCtx();
 if(bassOsc) return;
 bassOsc = ctx.createOscillator();
 bassOsc.type = 'sine';
 bassGain = ctx.createGain();
 bassGain.gain.value = 0;
 bassOsc.connect(bassGain);
 bassGain.connect(ctx.destination);
 bassOsc.start();
 noiseNode = ctx.createBufferSource();
 const buf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
 const data = buf.getChannelData(0);
 for(let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
 noiseNode.buffer = buf;
 noiseNode.loop = true;
 noiseFilter = ctx.createBiquadFilter();
 noiseFilter.type = 'bandpass';
 noiseFilter.frequency.value = 400;
 noiseFilter.Q.value = 0.5;
 noiseGain = ctx.createGain();
 noiseGain.gain.value = 0;
 noiseNode.connect(noiseFilter);
 noiseFilter.connect(noiseGain);
 noiseGain.connect(ctx.destination);
 noiseNode.start();
 addEvent('audio engine initialized');
}
function playChime(ascending){
 const ctx = getCtx();
 const now = ctx.currentTime;
 const osc = ctx.createOscillator();
 const gain = ctx.createGain();
 osc.type = 'sine';
 if(ascending){
  osc.frequency.setValueAtTime(440, now);
  osc.frequency.linearRampToValueAtTime(880, now + 0.15);
  osc.frequency.linearRampToValueAtTime(1320, now + 0.3);
 } else {
  osc.frequency.setValueAtTime(660, now);
  osc.frequency.linearRampToValueAtTime(440, now + 0.2);
  osc.frequency.linearRampToValueAtTime(220, now + 0.35);
 }
 gain.gain.setValueAtTime(0.15, now);
 gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
 osc.connect(gain);
 gain.connect(ctx.destination);
 osc.start(now);
 osc.stop(now + 0.5);
}
function initAmbient(){
 if(!ambientOn) return;
 const ctx = getCtx();
 while(ambientNodes.length){
  const n = ambientNodes.pop();
  try{ n.osc.stop(); }catch(e){}
  try{ n.gain.disconnect(); }catch(e){}
  try{ n.osc.disconnect(); }catch(e){}
 }
 const freqs = [55, 82.5, 110, 146.8];
 freqs.forEach((f, i) => {
  const osc = ctx.createOscillator();
  osc.type = 'sine';
  osc.frequency.value = f;
  const gain = ctx.createGain();
  gain.gain.value = 0.012;
  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 200 + i * 60;
  filter.Q.value = 1;
  osc.connect(filter);
  filter.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  ambientNodes.push({osc, gain, filter, baseFreq: f});
 });
}
function updateAmbient(health){
 ambientNodes.forEach((n, i) => {
  const shift = (health - 0.5) * 30;
  const freq = n.baseFreq + shift;
  const now = audioCtx.currentTime;
  n.osc.frequency.linearRampToValueAtTime(Math.max(20, freq), now + 1);
  const vol = ambientOn ? 0.008 + (1 - health) * 0.02 : 0;
  n.gain.gain.linearRampToValueAtTime(vol, now + 1);
 });
}
function updateBass(val){
 const ctx = getCtx();
 const now = ctx.currentTime;
 const freq = 40 + (val / 10000) * 200;
 const vol = getVol('revenue') * 0.25;
 if(!muted.revenue && !(Object.values(soloed).some(x=>x) && !soloed.revenue)){
  bassOsc.frequency.linearRampToValueAtTime(Math.max(20, Math.min(400, freq)), now + 0.08);
  bassGain.gain.linearRampToValueAtTime(vol, now + 0.05);
 } else {
  bassGain.gain.linearRampToValueAtTime(0, now + 0.05);
 }
}
function updateNoise(errors){
 const ctx = getCtx();
 const now = ctx.currentTime;
 const freq = 100 + (errors / 20) * 3000;
 const vol = getVol('errors') * 0.12;
 if(!muted.errors && !(Object.values(soloed).some(x=>x) && !soloed.errors)){
  noiseFilter.frequency.linearRampToValueAtTime(Math.min(ctx.sampleRate/2, Math.max(20, freq)), now + 0.05);
  noiseGain.gain.linearRampToValueAtTime(vol, now + 0.05);
 } else {
  noiseGain.gain.linearRampToValueAtTime(0, now + 0.05);
 }
}
function updatePulse(users){
 if(pulseInterval) { clearInterval(pulseInterval); pulseInterval = null; }
 const vol = getVol('users');
 const active = !muted.users && !(Object.values(soloed).some(x=>x) && !soloed.users);
 if(!active || vol < 0.01) return;
 const bpm = 40 + (users / 5000) * 160;
 const intervalMs = 60000 / bpm;
 let lastBeat = 0;
 pulseInterval = setInterval(() => {
  if(!running) return;
  const now = audioCtx.currentTime;
  const currentVol = getVol('users');
  if(currentVol < 0.01) return;
  const ctx = getCtx();
  const osc = ctx.createOscillator();
  osc.type = 'triangle';
  osc.frequency.value = 200 + (users / 5000) * 600;
  const gain = ctx.createGain();
  const v = currentVol * 0.15;
  gain.gain.setValueAtTime(v, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(now);
  osc.stop(now + 0.1);
  lastBeat = now;
 }, intervalMs);
}
function updateDisplay(){
 document.getElementById('revenueVal').textContent = '$' + Math.round(state.revenue).toLocaleString();
 document.getElementById('errorsVal').textContent = state.errors.toFixed(1) + '%';
 document.getElementById('usersVal').textContent = Math.round(state.users).toLocaleString();
 document.getElementById('healthRev').textContent = Math.round(state.revenue).toLocaleString();
 document.getElementById('healthErr').textContent = state.errors.toFixed(1) + '%';
 document.getElementById('healthUsr').textContent = Math.round(state.users).toLocaleString();
 const health = 1 - (state.errors / 20) * 0.7 + (state.revenue / 10000) * 0.3 - 0.15;
 const clamped = Math.max(0.1, Math.min(1, health));
 const dot = document.getElementById('healthDot');
 const label = document.getElementById('healthLabel');
 if(clamped > 0.65){ dot.className = 'health-indicator good'; label.textContent = 'system healthy'; }
 else if(clamped > 0.35){ dot.className = 'health-indicator warning'; label.textContent = 'system degraded'; }
 else { dot.className = 'health-indicator critical'; label.textContent = 'system critical'; }
 document.getElementById('visBar').style.width = (clamped * 100) + '%';
 updateBass(state.revenue);
 updateNoise(state.errors);
 updatePulse(state.users);
 updateAmbient(clamped);
}
function checkEvents(){
 if(state.revenue > prevRevenue * 1.15){
  playChime(true);
  addEvent('revenue up: $' + Math.round(state.revenue).toLocaleString(), 'pos');
 } else if(state.revenue < prevRevenue * 0.85){
  playChime(false);
  addEvent('revenue down: $' + Math.round(state.revenue).toLocaleString(), 'neg');
 }
 if(state.errors > prevErrors * 1.3){
  addEvent('error spike: ' + state.errors.toFixed(1) + '%', 'neg');
 } else if(state.errors < prevErrors * 0.6 && prevErrors > 1){
  addEvent('errors recovering: ' + state.errors.toFixed(1) + '%', 'pos');
 }
 if(state.users > prevUsers * 1.2){
  addEvent('user influx: ' + Math.round(state.users).toLocaleString(), 'pos');
 } else if(state.users < prevUsers * 0.75){
  addEvent('user drop: ' + Math.round(state.users).toLocaleString(), 'neg');
 }
 prevRevenue = state.revenue;
 prevErrors = state.errors;
 prevUsers = state.users;
}
function tick(){
 if(!running) return;
 const s = simSpeed;
 const v = variance;
 state.revenue += state.revenue * (Math.random() - 0.48) * v * s;
 state.revenue = Math.max(100, state.revenue);
 state.errors += (Math.random() - 0.5) * 0.4 * v * s;
 state.errors = Math.max(0, Math.min(25, state.errors));
 state.users += (Math.random() - 0.47) * 40 * v * s;
 state.users = Math.max(50, state.users);
 checkEvents();
 updateDisplay();
}
function injectSpike(){
 state.revenue *= 1.2;
 state.errors += 4 + Math.random() * 3;
 state.errors = Math.min(25, state.errors);
 addEvent('spike injected: revenue up, errors up', 'neg');
}
function injectDrop(){
 state.revenue *= 0.6;
 state.users *= 0.6;
 addEvent('drop injected: revenue & users down', 'neg');
}
function resetMetrics(){
 state.revenue = 5000;
 state.errors = 2.5;
 state.users = 1200;
 prevRevenue = 5000;
 prevErrors = 2.5;
 prevUsers = 1200;
 addEvent('metrics reset to baseline');
}
let tickInterval = setInterval(tick, 500);
function setupMute(channel, btnId){
 document.getElementById(btnId).addEventListener('click', function(e){
  muted[channel] = !muted[channel];
  this.textContent = muted[channel] ? 'unmute' : 'mute';
  this.classList.toggle('muted');
  if(muted[channel]) soloed[channel] = false;
  const soloBtn = document.querySelectorAll('[id^=solo]')[['revenue','errors','users'].indexOf(channel)];
  if(soloBtn) soloBtn.classList.remove('soloed');
 });
}
function setupSolo(channel, btnId, muteBtnId){
 document.getElementById(btnId).addEventListener('click', function(e){
  if(e.ctrlKey || e.metaKey){
   headphoneMode = true;
   document.getElementById('headphoneBtn').classList.add('active');
   document.getElementById('headphoneBtn').textContent = 'headphone on';
   Object.keys(soloed).forEach(k => soloed[k] = false);
   soloed[channel] = true;
   document.querySelectorAll('[id^=solo]').forEach(b => b.classList.remove('soloed'));
   this.classList.add('soloed');
   addEvent('headphone solo: ' + channel + ' channel isolated');
   return;
  }
  soloed[channel] = !soloed[channel];
  this.classList.toggle('soloed');
  if(soloed[channel] && muted[channel]){
   muted[channel] = false;
   document.getElementById(muteBtnId).textContent = 'mute';
   document.getElementById(muteBtnId).classList.remove('muted');
  }
 });
}
setupMute('revenue', 'muteRevenue');
setupMute('errors', 'muteErrors');
setupMute('users', 'muteUsers');
setupSolo('revenue', 'soloRevenue', 'muteRevenue');
setupSolo('errors', 'soloErrors', 'muteErrors');
setupSolo('users', 'soloUsers', 'muteUsers');
document.getElementById('headphoneBtn').addEventListener('click', function(){
 headphoneMode = !headphoneMode;
 this.classList.toggle('active');
 this.textContent = headphoneMode ? 'headphone on' : 'headphone mode';
 if(!headphoneMode){
  Object.keys(soloed).forEach(k => soloed[k] = false);
  document.querySelectorAll('[id^=solo]').forEach(b => b.classList.remove('soloed'));
  addEvent('headphone mode off');
 } else {
  addEvent('headphone mode on — ctrl+click solo to isolate channel');
 }
});
document.getElementById('ambientBtn').addEventListener('click', function(){
 ambientOn = !ambientOn;
 this.classList.toggle('active');
 this.textContent = ambientOn ? 'ambient on' : 'ambient off';
 if(ambientOn){ initAmbient(); addEvent('ambient drone on'); }
 else { addEvent('ambient drone off'); }
 updateAmbient(0.5);
});
document.getElementById('resetBtn').addEventListener('click', resetMetrics);
document.getElementById('spikeBtn').addEventListener('click', injectSpike);
document.getElementById('dropBtn').addEventListener('click', injectDrop);
document.getElementById('simSpeed').addEventListener('input', function(){ simSpeed = parseFloat(this.value); });
document.getElementById('simVariance').addEventListener('input', function(){ variance = parseFloat(this.value); });
['revenueVol','errorsVol','usersVol'].forEach(id => {
 document.getElementById(id).addEventListener('input', updateDisplay);
});
document.addEventListener('click', function firstClick(){
 const ctx = getCtx();
 if(ctx.state === 'suspended') ctx.resume();
 initAudio();
 initAmbient();
 addEvent('audio context unlocked');
 updateDisplay();
}, {once: true});
setTimeout(() => {
 initAudio();
 initAmbient();
 updateDisplay();
 addEvent('console initialized, streaming metrics');
}, 300);
})();
</script>
</body>
</html>
```
Working artifact. Open in any browser to hear revenue mapped to bass oscillator frequency, error rate as bandpass noise, active users as triangle-wave rhythmic pulse, plus ascending/descending chimes on metric events and a shifting ambient drone tied to system health. All controls (mute, solo, volume, headphone isolation, sim speed/variance, manual spike/drop injection) are functional on the dashboard.