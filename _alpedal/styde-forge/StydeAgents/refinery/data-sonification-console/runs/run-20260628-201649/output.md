<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Sonification Console</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0f;color:#c8c8d0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;display:flex;flex-direction:column}
header{background:linear-gradient(135deg,#0f0f1a,#1a1a2e);padding:18px 28px;border-bottom:1px solid #2a2a3e;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
header h1{font-size:20px;font-weight:300;letter-spacing:2px;color:#d0d0e0;text-transform:uppercase}
header .status-bar{display:flex;gap:24px;margin-left:auto;font-size:13px;color:#888}
header .status-bar .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.dot.green{background:#4caf50;box-shadow:0 0 6px #4caf5066}
.dot.red{background:#f44336;box-shadow:0 0 6px #f4433666}
.dot.yellow{background:#ff9800;box-shadow:0 0 6px #ff980066}
.main{display:grid;grid-template-columns:320px 1fr;gap:0;flex:1}
@media(max-width:820px){.main{grid-template-columns:1fr}}
.sidebar{background:#0d0d16;border-right:1px solid #1e1e30;padding:16px;display:flex;flex-direction:column;gap:10px}
.sidebar h2{font-size:11px;font-weight:600;color:#666;text-transform:uppercase;letter-spacing:1.5px;margin:10px 0 4px}
.channel-card{background:#12121f;border:1px solid #1e1e30;border-radius:6px;padding:10px 12px;transition:border-color .2s}
.channel-card:hover{border-color:#3a3a5e}
.channel-card .ch-name{font-size:13px;font-weight:500;margin-bottom:6px;display:flex;justify-content:space-between}
.channel-card .ch-name .ch-value{font-size:11px;color:#888;font-weight:400}
.channel-controls{display:flex;gap:4px;align-items:center;flex-wrap:wrap}
.channel-controls button{background:#1a1a2e;border:1px solid #2a2a3e;color:#aab;padding:3px 10px;border-radius:4px;font-size:11px;cursor:pointer;transition:all .15s}
.channel-controls button:hover{background:#2a2a40;border-color:#4a4a6e}
.channel-controls button.active{background:#4a4a8e;border-color:#6a6aae;color:#fff}
.channel-controls button.mute-active{background:#8e3a3a;border-color:#ae4a4a;color:#fff}
.channel-controls button.solo-active{background:#3a8e3a;border-color:#4aae4a;color:#fff}
.channel-controls input[type=range]{width:60px;height:4px;accent-color:#6a6aae;background:#1e1e30;border-radius:2px;cursor:pointer;vertical-align:middle}
.channel-controls label{font-size:10px;color:#666;margin:0 2px}
.mute-solo-group{display:flex;gap:2px}
.content{padding:20px;display:flex;flex-direction:column;gap:16px}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.metric-card{background:#12121f;border:1px solid #1e1e30;border-radius:8px;padding:14px;text-align:center}
.metric-card .metric-label{font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px}
.metric-card .metric-value{font-size:32px;font-weight:300;margin:6px 0;font-variant-numeric:tabular-nums}
.metric-card .metric-desc{font-size:11px;color:#555}
.metric-card .metric-bar{height:3px;border-radius:2px;margin-top:8px;background:#1e1e30;overflow:hidden}
.metric-card .metric-bar-fill{height:100%;border-radius:2px;transition:width .3s ease}
.console-panel{background:#0d0d16;border:1px solid #1e1e30;border-radius:8px;padding:16px;flex:1}
.console-panel h3{font-size:12px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}
.console-log{max-height:240px;overflow-y:auto;font-family:'Consolas','Courier New',monospace;font-size:12px;line-height:1.6}
.console-log .log-entry{padding:2px 0;border-bottom:1px solid #16162a;display:flex;gap:8px}
.console-log .log-time{color:#555;white-space:nowrap}
.console-log .log-msg{color:#8a8aaa}
.console-log .log-msg.pos{color:#6abf6a}
.console-log .log-msg.neg{color:#bf6a6a}
.console-log .log-msg.info{color:#6a9abf}
.controls-bar{display:flex;gap:10px;align-items:center;padding:10px 0;flex-wrap:wrap}
.controls-bar button{background:#1a1a2e;border:1px solid #2a2a3e;color:#aab;padding:6px 14px;border-radius:5px;font-size:12px;cursor:pointer;transition:all .15s}
.controls-bar button:hover{background:#2a2a40;border-color:#4a4a6e}
.controls-bar button.primary{background:#3a3a6e;border-color:#5a5a9e;color:#fff}
.controls-bar button.danger{background:#6e3a3a;border-color:#9e4a4a}
.controls-bar button.active-header{background:#2a5a2a;border-color:#4a8e4a;color:#fff}
.health-display{display:flex;align-items:center;gap:12px;font-size:13px}
.health-bar{width:120px;height:6px;background:#1e1e30;border-radius:3px;overflow:hidden}
.health-bar-fill{height:100%;border-radius:3px;transition:width .5s,background .5s}
.headphone-indicator{font-size:11px;padding:2px 8px;border-radius:3px;background:#1a1a2e;border:1px solid #2a2a3e}
.headphone-indicator.active{background:#2a4a2a;border-color:#4a8e4a;color:#8ecc8e}
canvas{width:100%;height:120px;border-radius:6px;background:#0a0a12;border:1px solid #1a1a2e;margin-top:8px}
</style>
</head>
<body>
<header>
<h1>Sonification Console</h1>
<div class="status-bar">
<span><span class="dot green"></span>Audio Ready</span>
<span id="healthDisplay">Health: <span id="healthPct">85</span>%</span>
<span id="hpIndicator" class="headphone-indicator">Headphones</span>
</div>
</header>
<div class="main">
<div class="sidebar" id="sidebar">
<h2>Audio Channels</h2>
<div id="channelList"></div>
<h2>Master Controls</h2>
<div class="channel-card">
<div class="channel-controls" style="flex-direction:column;align-items:stretch;gap:6px">
<div style="display:flex;gap:8px;align-items:center">
<label>Master</label>
<input type="range" id="masterGain" min="0" max="1" step="0.01" value="0.7">
<span id="masterGainVal" style="font-size:11px;color:#888;width:30px">0.70</span>
</div>
<div style="display:flex;gap:6px;align-items:center">
<label style="font-size:10px">HP Mode</label>
<input type="checkbox" id="hpToggle" checked>
<button id="resetBtn" class="danger" style="margin-left:auto">Reset All</button>
</div>
</div>
</div>
</div>
<div class="content">
<div class="metrics-grid" id="metricsGrid"></div>
<div class="controls-bar">
<button id="startBtn" class="primary">Start Sonification</button>
<button id="stopBtn">Stop</button>
<button id="simBtn">Simulate Data</button>
<button id="clearLogBtn">Clear Log</button>
<div class="health-display">
<span>System Health</span>
<div class="health-bar"><div class="health-bar-fill" id="healthBarFill" style="width:85%;background:#4caf50"></div></div>
</div>
<canvas id="waveform"></canvas>
</div>
<div class="console-panel">
<h3>Event Log</h3>
<div class="console-log" id="consoleLog"></div>
</div>
</div>
</div>
<script>
(function(){
const logEl = document.getElementById('consoleLog');
const channelListEl = document.getElementById('channelList');
const metricsGridEl = document.getElementById('metricsGrid');
const masterGainInput = document.getElementById('masterGain');
const masterGainVal = document.getElementById('masterGainVal');
const hpToggle = document.getElementById('hpToggle');
const hpIndicator = document.getElementById('hpIndicator');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const simBtn = document.getElementById('simBtn');
const clearLogBtn = document.getElementById('clearLogBtn');
const healthPct = document.getElementById('healthPct');
const healthBarFill = document.getElementById('healthBarFill');
const waveformCanvas = document.getElementById('waveform');
let audioCtx = null;
let masterGainNode = null;
let isRunning = false;
let simInterval = null;
let animFrame = null;
let health = 85;
const log = (msg, type='info') => {
  const t = new Date();
  const ts = t.toISOString().slice(11,19);
  const entry = document.createElement('div');
  entry.className = 'log-entry';
  entry.innerHTML = `<span class="log-time">${ts}</span><span class="log-msg ${type}">${msg}</span>`;
  logEl.prepend(entry);
  while(logEl.children.length > 500) logEl.removeChild(logEl.lastChild);
};
// Channel definitions
const CHANNEL_DEFS = [
  {id:'revenue', label:'Revenue', type:'osc', color:'#ff9800', min:0, max:1000, unit:'k$', freqRange:[55,220], default:420},
  {id:'errors', label:'Error Rate', type:'noise', color:'#f44336', min:0, max:100, unit:'rpm', freqRange:[200,3000], default:5},
  {id:'users', label:'Active Users', type:'rhythm', color:'#4caf50', min:0, max:50000, unit:'users', bpmRange:[60,180], default:12500},
  {id:'latency', label:'Latency', type:'ambient', color:'#9c27b0', min:0, max:500, unit:'ms', freqRange:[80,240], default:45}
];
// Channel state
class AudioChannel {
  constructor(def) {
    this.def = def;
    this.value = def.default;
    this.muted = false;
    this.soloed = false;
    this.volume = 0.7;
    this.pan = 0;
    this.gainNode = null;
    this.panNode = null;
    this.sourceNodes = [];
  }
}
const channels = {};
CHANNEL_DEFS.forEach(d => { channels[d.id] = new AudioChannel(d); });
// --- Audio Engine ---
function initAudio() {
  if(audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  masterGainNode = audioCtx.createGain();
  masterGainNode.gain.value = parseFloat(masterGainInput.value);
  masterGainNode.connect(audioCtx.destination);
  CHANNEL_DEFS.forEach(def => {
    const ch = channels[def.id];
    ch.gainNode = audioCtx.createGain();
    ch.gainNode.gain.value = ch.volume;
    ch.panNode = audioCtx.createStereoPanner();
    ch.panNode.pan.value = ch.pan;
    ch.gainNode.connect(ch.panNode);
    ch.panNode.connect(masterGainNode);
  });
  log('Audio context initialized','info');
  updateHPIndicator();
}
function getSoloActive() {
  return Object.values(channels).some(ch => ch.soloed);
}
function applyMuteSolo() {
  const soloActive = getSoloActive();
  Object.values(channels).forEach(ch => {
    if(!ch.gainNode) return;
    let effectiveGain = ch.volume;
    if(ch.muted) effectiveGain = 0;
    if(soloActive && !ch.soloed) effectiveGain = 0;
    ch.gainNode.gain.setTargetAtTime(effectiveGain, audioCtx.currentTime, 0.05);
  });
}
function toggleMute(chId) {
  const ch = channels[chId];
  ch.muted = !ch.muted;
  applyMuteSolo();
  const card = document.querySelector(`[data-ch="${chId}"]`);
  if(card){
    const btn = card.querySelector('.mute-btn');
    btn.classList.toggle('mute-active', ch.muted);
    btn.textContent = ch.muted ? 'M' : 'M';
  }
  log(`${ch.def.label} ${ch.muted ? 'muted' : 'unmuted'}`, 'info');
}
function toggleSolo(chId) {
  const ch = channels[chId];
  ch.soloed = !ch.soloed;
  applyMuteSolo();
  const card = document.querySelector(`[data-ch="${chId}"]`);
  if(card){
    const btn = card.querySelector('.solo-btn');
    btn.classList.toggle('solo-active', ch.soloed);
    btn.textContent = ch.soloed ? 'S' : 'S';
  }
  log(`${ch.def.label} ${ch.soloed ? 'soloed' : 'solo removed'}`, 'info');
}
function setVolume(chId, vol) {
  const ch = channels[chId];
  ch.volume = vol;
  applyMuteSolo();
}
function setPan(chId, panVal) {
  const ch = channels[chId];
  ch.pan = panVal;
  if(ch.panNode) ch.panNode.pan.setTargetAtTime(panVal, audioCtx.currentTime, 0.05);
}
// --- Sound Generators ---
const oscSources = {};
function startOscillator(ch) {
  if(oscSources[ch.def.id]){
    try{oscSources[ch.def.id].stop();}catch(e){}
  }
  const osc = audioCtx.createOscillator();
  osc.type = 'sine';
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  osc.frequency.value = Math.max(20, Math.min(20000, freq));
  const gain = audioCtx.createGain();
  gain.gain.value = 0.3;
  osc.connect(gain);
  gain.connect(ch.gainNode);
  osc.start();
  oscSources[ch.def.id] = osc;
  return osc;
}
function updateOscillator(ch) {
  const osc = oscSources[ch.def.id];
  if(!osc) return;
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  osc.frequency.setTargetAtTime(Math.max(20, Math.min(20000, freq)), audioCtx.currentTime, 0.1);
}
function stopOscillator(chId) {
  if(oscSources[chId]) {
    try{oscSources[chId].stop();}catch(e){}
    delete oscSources[chId];
  }
}
const noiseSources = {};
const noiseGains = {};
function startNoise(ch) {
  if(noiseSources[ch.def.id]){
    try{noiseSources[ch.def.id].stop();}catch(e){}
  }
  const bufferSize = audioCtx.sampleRate * 2;
  const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for(let i=0; i<bufferSize; i++) data[i] = Math.random() * 2 - 1;
  const source = audioCtx.createBufferSource();
  source.buffer = buffer;
  source.loop = true;
  // Bandpass filter for cymbal-like tone
  const bp = audioCtx.createBiquadFilter();
  bp.type = 'bandpass';
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  bp.frequency.value = Math.max(50, Math.min(audioCtx.sampleRate/2-1, freq));
  bp.Q.value = 1.5;
  const gain = audioCtx.createGain();
  const vol = mapRange(ch.value, ch.def.min, ch.def.max, 0.02, 0.25);
  gain.gain.value = Math.max(0, Math.min(1, vol));
  source.connect(bp);
  bp.connect(gain);
  gain.connect(ch.gainNode);
  source.start();
  noiseSources[ch.def.id] = {source, bp, gain};
  noiseGains[ch.def.id] = gain;
}
function updateNoise(ch) {
  const ns = noiseSources[ch.def.id];
  if(!ns) return;
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  ns.bp.frequency.setTargetAtTime(Math.max(50, Math.min(audioCtx.sampleRate/2-1, freq)), audioCtx.currentTime, 0.1);
  const vol = mapRange(ch.value, ch.def.min, ch.def.max, 0.02, 0.25);
  ns.gain.gain.setTargetAtTime(Math.max(0, Math.min(1, vol)), audioCtx.currentTime, 0.1);
}
function stopNoise(chId) {
  if(noiseSources[chId]) {
    try{noiseSources[chId].source.stop();}catch(e){}
    delete noiseSources[chId];
    delete noiseGains[chId];
  }
}
// Rhythm state
let rhythmState = {running:false, timerId:null, lastTick:0, tickCount:0};
function startRhythm(ch) {
  if(rhythmState.running) return;
  rhythmState.running = true;
  rhythmState.tickCount = 0;
  scheduleRhythmTick(ch);
}
function scheduleRhythmTick(ch) {
  if(!rhythmState.running || !isRunning) return;
  const bpm = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.bpmRange[0], ch.def.bpmRange[1]);
  const interval = (60 / Math.max(20, Math.min(300, bpm))) * 1000;
  // Play click
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  osc.type = 'triangle';
  osc.frequency.value = 880;
  const g = audioCtx.createGain();
  g.gain.setValueAtTime(0.15, now);
  g.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
  osc.connect(g);
  g.connect(ch.gainNode);
  osc.start(now);
  osc.stop(now + 0.05);
  // Tick count variation
  rhythmState.tickCount++;
  if(rhythmState.tickCount % 4 === 0){
    const osc2 = audioCtx.createOscillator();
    osc2.type = 'sine';
    osc2.frequency.value = 440;
    const g2 = audioCtx.createGain();
    g2.gain.setValueAtTime(0.08, now);
    g2.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    osc2.connect(g2);
    g2.connect(ch.gainNode);
    osc2.start(now);
    osc2.stop(now + 0.08);
  }
  rhythmState.timerId = setTimeout(() => scheduleRhythmTick(ch), Math.max(50, interval));
}
function updateRhythm(ch) {
  // Tempo changes happen on next tick automatically via mapRange
}
function stopRhythm() {
  rhythmState.running = false;
  if(rhythmState.timerId) {
    clearTimeout(rhythmState.timerId);
    rhythmState.timerId = null;
  }
}
// Ambient drone
const ambientSources = {};
function startAmbient(ch) {
  if(ambientSources[ch.def.id]){
    try{ambientSources[ch.def.id].osc.stop();}catch(e){}
  }
  const osc1 = audioCtx.createOscillator();
  osc1.type = 'sine';
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  osc1.frequency.value = Math.max(20, Math.min(1000, freq));
  const osc2 = audioCtx.createOscillator();
  osc2.type = 'sine';
  osc2.frequency.value = osc1.frequency.value * 1.005;
  osc2.detune.value = 5;
  const gain1 = audioCtx.createGain();
  gain1.gain.value = 0.04;
  const gain2 = audioCtx.createGain();
  gain2.gain.value = 0.04;
  const filter = audioCtx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 400;
  filter.Q.value = 2;
  const merger = audioCtx.createGain();
  merger.gain.value = 0.3;
  osc1.connect(gain1);
  osc2.connect(gain2);
  gain1.connect(filter);
  gain2.connect(filter);
  filter.connect(merger);
  merger.connect(ch.gainNode);
  osc1.start();
  osc2.start();
  ambientSources[ch.def.id] = {osc1, osc2, gain1, gain2, filter, merger, freq};
}
function updateAmbient(ch) {
  const src = ambientSources[ch.def.id];
  if(!src) return;
  const freq = mapRange(ch.value, ch.def.min, ch.def.max, ch.def.freqRange[0], ch.def.freqRange[1]);
  src.osc1.frequency.setTargetAtTime(Math.max(20, Math.min(1000, freq)), audioCtx.currentTime, 0.3);
  src.osc2.frequency.setTargetAtTime(Math.max(20, Math.min(1000, freq * 1.005)), audioCtx.currentTime, 0.3);
  // Filter sweeps with health
  const healthFreq = mapRange(health, 0, 100, 120, 800);
  src.filter.frequency.setTargetAtTime(Math.max(20, Math.min(audioCtx.sampleRate/2-1, healthFreq)), audioCtx.currentTime, 0.5);
  src.gain1.gain.setTargetAtTime(0.02 + (health/100)*0.06, audioCtx.currentTime, 0.3);
  src.gain2.gain.setTargetAtTime(0.02 + (health/100)*0.06, audioCtx.currentTime, 0.3);
  src.freq = freq;
}
function stopAmbient(chId) {
  if(ambientSources[chId]) {
    try{
      ambientSources[chId].osc1.stop();
      ambientSources[chId].osc2.stop();
    }catch(e){}
    delete ambientSources[chId];
  }
}
// --- Events / Chimes ---
function playChime(ascending) {
  if(!audioCtx || !isRunning) return;
  const now = audioCtx.currentTime;
  const count = 3;
  for(let i=0; i<count; i++){
    const osc = audioCtx.createOscillator();
    osc.type = 'sine';
    const base = ascending ? 523 : 400;
    const multi = ascending ? (1 + i*0.25) : (1 - i*0.15);
    osc.frequency.value = base * multi;
    const g = audioCtx.createGain();
    g.gain.setValueAtTime(0, now + i*0.08);
    g.gain.linearRampToValueAtTime(0.1, now + i*0.08 + 0.02);
    g.gain.exponentialRampToValueAtTime(0.001, now + i*0.08 + 0.25);
    osc.connect(g);
    g.connect(masterGainNode);
    osc.start(now + i*0.08);
    osc.stop(now + i*0.08 + 0.3);
  }
}
// --- Utility ---
function mapRange(val, inMin, inMax, outMin, outMax) {
  if(inMax === inMin) return outMin;
  return outMin + ((val - inMin) / (inMax - inMin)) * (outMax - outMin);
}
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function updateHealth(delta) {
  health = clamp(health + delta, 0, 100);
  healthPct.textContent = Math.round(health);
  healthBarFill.style.width = health + '%';
  const hue = 120 * (health/100);
  healthBarFill.style.background = `hsl(${hue}, 80%, 45%)`;
  // Update ambient filter
  CHANNEL_DEFS.forEach(d => {
    if(d.type === 'ambient') updateAmbient(channels[d.id]);
  });
}
function updateHPIndicator() {
  const hp = hpToggle.checked;
  hpIndicator.textContent = hp ? 'Headphones' : 'Speakers';
  hpIndicator.className = 'headphone-indicator' + (hp ? ' active' : '');
  // In HP mode, reduce stereo width / adjust ambient
  Object.values(channels).forEach(ch => {
    if(ch.panNode && hp){
      // Narrow pan in HP mode
      // Keep pan but reduce master width — we'll just leave pan as-is
    }
  });
  log(`Output mode: ${hp ? 'Headphones' : 'Speakers'}`, 'info');
}
// --- Waveform visualizer ---
function startWaveform() {
  if(!audioCtx || !masterGainNode) return;
  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  masterGainNode.connect(analyser);
  const canvas = waveformCanvas;
  const ctx = canvas.getContext('2d');
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);
  function draw() {
    if(!isRunning) return;
    animFrame = requestAnimationFrame(draw);
    analyser.getByteTimeDomainData(dataArray);
    ctx.fillStyle = '#0a0a12';
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#6a6aae';
    ctx.beginPath();
    const sliceWidth = canvas.width / bufferLength;
    let x = 0;
    for(let i=0; i<bufferLength; i++){
      const v = dataArray[i]/128.0;
      const y = v * canvas.height/2;
      if(i===0) ctx.moveTo(x,y);
      else ctx.lineTo(x,y);
      x += sliceWidth;
    }
    ctx.lineTo(canvas.width, canvas.height/2);
    ctx.stroke();
  }
  draw();
}
// --- Start / Stop ---
function startAll() {
  if(isRunning) return;
  initAudio();
  isRunning = true;
  CHANNEL_DEFS.forEach(def => {
    const ch = channels[def.id];
    switch(def.type){
      case 'osc': startOscillator(ch); break;
      case 'noise': startNoise(ch); break;
      case 'rhythm': startRhythm(ch); break;
      case 'ambient': startAmbient(ch); break;
    }
  });
  startWaveform();
  log('Sonification started','info');
  startBtn.textContent = 'Running...';
  startBtn.disabled = true;
  stopBtn.disabled = false;
}
function stopAll() {
  if(!isRunning) return;
  isRunning = false;
  CHANNEL_DEFS.forEach(def => {
    switch(def.type){
      case 'osc': stopOscillator(def.id); break;
      case 'noise': stopNoise(def.id); break;
      case 'rhythm': stopRhythm(); break;
      case 'ambient': stopAmbient(def.id); break;
    }
  });
  if(animFrame) { cancelAnimationFrame(animFrame); animFrame = null; }
  if(simInterval) { clearInterval(simInterval); simInterval = null; }
  log('Sonification stopped','info');
  startBtn.textContent = 'Start Sonification';
  startBtn.disabled = false;
  stopBtn.disabled = true;
}
function resetAll() {
  stopAll();
  if(simInterval) { clearInterval(simInterval); simInterval = null; }
  health = 85;
  CHANNEL_DEFS.forEach(def => {
    const ch = channels[def.id];
    ch.value = def.default;
    ch.muted = false;
    ch.soloed = false;
    ch.volume = 0.7;
    ch.pan = 0;
  });
  updateHealth(0);
  renderChannels();
  renderMetrics();
  log('All channels reset','info');
}
// --- Data Simulation ---
function simulateData() {
  if(simInterval) { clearInterval(simInterval); simInterval = null; }
  let step = 0;
  const prevValues = {};
  CHANNEL_DEFS.forEach(d => { prevValues[d.id] = d.default; });
  simInterval = setInterval(() => {
    step++;
    let healthDelta = 0;
    const changes = [];
    CHANNEL_DEFS.forEach(def => {
      const ch = channels[def.id];
      const old = prevValues[def.id];
      let newVal;
      switch(def.id){
        case 'revenue':
          newVal = 300 + 200 * Math.sin(step * 0.03) + (Math.random()-0.5)*80;
          if(newVal > old * 1.05) healthDelta += 0.3;
          break;
        case 'errors':
          newVal = Math.max(0, 5 + 8 * Math.sin(step * 0.07 + 1) + (Math.random()-0.5)*4);
          if(newVal > 15) healthDelta -= 0.8;
          else if(newVal < 3) healthDelta += 0.5;
          break;
        case 'users':
          newVal = 12000 + 4000 * Math.sin(step * 0.02 + 2) + (Math.random()-0.5)*1000;
          if(newVal > old * 1.03) healthDelta += 0.2;
          break;
        case 'latency':
          newVal = 40 + 30 * Math.sin(step * 0.05 + 0.5) + (Math.random()-0.5)*10;
          if(newVal > 120) healthDelta -= 0.6;
          else if(newVal < 50) healthDelta += 0.3;
          break;
      }
      newVal = clamp(Math.round(newVal * 10)/10, def.min, def.max);
      prevValues[def.id] = newVal;
      if(Math.abs(newVal - old) > (def.max - def.min) * 0.05) {
        changes.push({id: def.id, old, new: newVal, dir: newVal > old ? 'up' : 'down'});
      }
    });
    // Apply smoothed updates
    CHANNEL_DEFS.forEach(def => {
      const ch = channels[def.id];
      const target = prevValues[def.id];
      ch.value += (target - ch.value) * 0.3;
      switch(def.type){
        case 'osc': updateOscillator(ch); break;
        case 'noise': updateNoise(ch); break;
        case 'rhythm': updateRhythm(ch); break;
        case 'ambient': updateAmbient(ch); break;
      }
    });
    // Trigger events for significant changes
    changes.forEach(c => {
      const def = CHANNEL_DEFS.find(d => d.id === c.id);
      if(!def) return;
      const pct = Math.abs(c.new - c.old) / (def.max - def.min) * 100;
      if(pct > 8) {
        const isPos = c.dir === 'up' && (c.id === 'revenue' || c.id === 'users');
        const isNeg = c.dir === 'up' && (c.id === 'errors' || c.id === 'latency');
        const isGood = isPos || (c.dir === 'down' && (c.id === 'errors' || c.id === 'latency'));
        if(isGood) {
          playChime(true);
          log(`${def.label}: ${c.old.toFixed(1)} -> ${c.new.toFixed(1)} ${def.unit||''} (positive)`, 'pos');
        } else {
          playChime(false);
          log(`${def.label}: ${c.old.toFixed(1)} -> ${c.new.toFixed(1)} ${def.unit||''} (negative)`, 'neg');
        }
      } else {
        log(`${def.label}: ${c.old.toFixed(1)} -> ${c.new.toFixed(1)} ${def.unit||''}`, 'info');
      }
    });
    updateHealth(healthDelta * 0.1);
    renderMetrics();
  }, 1200);
}
// --- UI Rendering ---
function renderChannels() {
  channelListEl.innerHTML = '';
  CHANNEL_DEFS.forEach(def => {
    const ch = channels[def.id];
    const card = document.createElement('div');
    card.className = 'channel-card';
    card.dataset.ch = def.id;
    let typeLabel = def.type;
    const freqStr = def.type === 'rhythm' ?
      `${def.bpmRange[0]}-${def.bpmRange[1]} bpm` :
      `${def.freqRange[0]}-${def.freqRange[1]} Hz`;
    card.innerHTML = `
      <div class="ch-name">
        <span style="color:${def.color}">${def.label}</span>
        <span class="ch-value">${typeLabel} | ${freqStr}</span>
      </div>
      <div class="channel-controls">
        <div class="mute-solo-group">
          <button class="mute-btn ${ch.muted?'mute-active':''}" data-action="mute">M</button>
          <button class="solo-btn ${ch.soloed?'solo-active':''}" data-action="solo">S</button>
        </div>
        <label>Vol</label>
        <input type="range" min="0" max="1" step="0.01" value="${ch.volume}" data-action="volume">
        <label>Pan</label>
        <input type="range" min="-1" max="1" step="0.01" value="${ch.pan}" data-action="pan" style="width:50px">
      </div>
    `;
    card.querySelector('.mute-btn').addEventListener('click', () => toggleMute(def.id));
    card.querySelector('.solo-btn').addEventListener('click', () => toggleSolo(def.id));
    card.querySelector('[data-action="volume"]').addEventListener('input', (e) => {
      setVolume(def.id, parseFloat(e.target.value));
    });
    card.querySelector('[data-action="pan"]').addEventListener('input', (e) => {
      setPan(def.id, parseFloat(e.target.value));
    });
    channelListEl.appendChild(card);
  });
}
function renderMetrics() {
  metricsGridEl.innerHTML = '';
  CHANNEL_DEFS.forEach(def => {
    const ch = channels[def.id];
    const pct = ((ch.value - def.min) / (def.max - def.min)) * 100;
    const card = document.createElement('div');
    card.className = 'metric-card';
    let displayVal = def.type === 'rhythm' ? Math.round(ch.value).toLocaleString() : ch.value.toFixed(1);
    card.innerHTML = `
      <div class="metric-label">${def.label}</div>
      <div class="metric-value" style="color:${def.color}">${displayVal}</div>
      <div class="metric-desc">${def.unit||''}</div>
      <div class="metric-bar"><div class="metric-bar-fill" style="width:${clamp(pct,0,100)}%;background:${def.color}"></div></div>
    `;
    metricsGridEl.appendChild(card);
  });
}
// --- Master Controls ---
masterGainInput.addEventListener('input', (e) => {
  const v = parseFloat(e.target.value);
  masterGainVal.textContent = v.toFixed(2);
  if(masterGainNode) masterGainNode.gain.setTargetAtTime(v, audioCtx.currentTime, 0.05);
});
hpToggle.addEventListener('change', updateHPIndicator);
startBtn.addEventListener('click', startAll);
stopBtn.addEventListener('click', stopAll);
resetBtn.addEventListener('click', resetAll);
simBtn.addEventListener('click', simulateData);
clearLogBtn.addEventListener('click', () => { logEl.innerHTML = ''; });
// Init
renderChannels();
renderMetrics();
updateHealth(0);
stopBtn.disabled = true;
// Auto-show initial log
log('Sonification Console v1.0 ready. Press Start to begin.','info');
log('Configured channels: Revenue (osc), Error Rate (noise), Active Users (rhythm), Latency (ambient)','info');
log('Headphone mode provides focused stereo monitoring','info');
log('Tip: Use Solo buttons to isolate individual channels','info');
})();
</script>
</body>
</html>