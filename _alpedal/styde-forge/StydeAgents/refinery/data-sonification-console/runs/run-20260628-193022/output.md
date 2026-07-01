<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Sonification Console</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#c0c8d4;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
header{background:linear-gradient(135deg,#0f0f1a,#1a1a2e);border-bottom:1px solid #2a2a4a;padding:20px 30px;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:22px;font-weight:300;letter-spacing:3px;text-transform:uppercase;color:#8a9bb5}
header .sub{font-size:12px;color:#5a6a8a;letter-spacing:1px}
.system-status{display:flex;align-items:center;gap:10px}
.health-indicator{width:12px;height:12px;border-radius:50%;transition:background .8s}
.health-label{font-size:13px;color:#7a8aaa}
.controls-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;padding:20px 30px}
.channel-card{background:linear-gradient(135deg,#12121f,#1a1a2e);border:1px solid #2a2a4a;border-radius:12px;padding:18px;position:relative;overflow:hidden}
.channel-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;opacity:.6;transition:height .3s}
.channel-card.revenue::before{background:#22c55e}
.channel-card.errors::before{background:#ef4444}
.channel-card.users::before{background:#3b82f6}
.channel-card.ambient::before{background:#a855f7}
.channel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.channel-name{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#8a9bb5}
.channel-value{font-size:28px;font-weight:300;font-variant-numeric:tabular-nums}
.channel-value.revenue{color:#22c55e}
.channel-value.errors{color:#ef4444}
.channel-value.users{color:#3b82f6}
.channel-meta{font-size:11px;color:#5a6a8a;margin:4px 0 10px}
.controls-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.controls-row label{font-size:11px;color:#6a7a9a;width:40px}
input[type="range"]{flex:1;height:4px;appearance:none;-webkit-appearance:none;background:#2a2a4a;border-radius:2px;outline:none;min-width:60px}
input[type="range"]::-webkit-slider-thumb{appearance:none;-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#5a7aaa;cursor:pointer;border:2px solid #3a4a6a}
.btn{padding:4px 12px;font-size:11px;border:1px solid #3a3a5a;border-radius:6px;background:#1a1a2e;color:#8a9bb5;cursor:pointer;transition:all .15s;text-transform:uppercase;letter-spacing:.5px}
.btn:hover{border-color:#5a7aaa;color:#aabbd5}
.btn.active{background:#2a3a5a;border-color:#5a7aaa;color:#c0d0e8}
.btn.muted{background:#3a1a1a;border-color:#6a2a2a;color:#e05050}
.btn.solo{background:#1a3a1a;border-color:#2a6a2a;color:#50e050}
.event-log{background:#0a0a14;border:1px solid #2a2a4a;border-radius:12px;padding:18px;margin:0 30px 20px}
.event-log h3{font-size:13px;color:#6a7a9a;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}
.event-list{max-height:120px;overflow-y:auto;font-size:12px;font-family:'Cascadia Code','Courier New',monospace;color:#6a7a9a}
.event-list div{padding:3px 0;border-bottom:1px solid #1a1a2e}
.event-list .positive{color:#22c55e}
.event-list .negative{color:#ef4444}
.event-list .info{color:#6a8acc}
.spectrum-vis{height:80px;background:#0a0a14;border:1px solid #2a2a4a;border-radius:8px;margin:0 30px 20px;overflow:hidden;position:relative}
.spectrum-vis canvas{width:100%;height:100%;display:block}
.pulse-ring{position:absolute;top:50%;left:50%;width:0;height:0;border-radius:50%;border:2px solid rgba(100,150,255,.3);transform:translate(-50%,-50%);pointer-events:none;transition:none}
.pulse-ring.pulse{animation:pulseAnim .6s ease-out}
@keyframes pulseAnim{0%{width:0;height:0;opacity:1}100%{width:200px;height:200px;opacity:0}}
.mode-toggle{text-align:center;padding:0 30px 20px;display:flex;gap:10px;justify-content:center}
.mode-toggle .mode-btn{padding:8px 24px;font-size:12px;border-radius:20px;border:1px solid #3a3a5a;background:#12121f;color:#6a7a9a;cursor:pointer;transition:all .2s;text-transform:uppercase;letter-spacing:1px}
.mode-toggle .mode-btn.active{background:#2a3a5a;border-color:#5a7aaa;color:#c0d0e8}
.mode-toggle .mode-btn:hover{border-color:#5a7aaa}
.freq-display{display:flex;justify-content:space-between;font-size:10px;color:#3a4a5a;padding:0 4px;margin-top:2px}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#0a0a14}
::-webkit-scrollbar-thumb{background:#2a2a4a;border-radius:2px}
@media(max-width:600px){.controls-grid{grid-template-columns:1fr;padding:10px}header{flex-direction:column;gap:10px;text-align:center}}
</style>
</head>
<body>
<header>
<div>
<h1>Data Sonification Console</h1>
<div class="sub">Web Audio API &mdash; Revenue &bull; Errors &bull; Users</div>
</div>
<div class="system-status">
<div class="health-indicator" id="healthDot" style="background:#22c55e"></div>
<span class="health-label" id="healthLabel">Healthy</span>
</div>
</header>
<div class="controls-grid" id="channels">
<div class="channel-card revenue" data-channel="revenue">
<div class="channel-header">
<span class="channel-name">Revenue Stream</span>
<span class="channel-value revenue" id="revVal">$0</span>
</div>
<div class="channel-meta">Bass oscillator &mdash; pitch maps to revenue</div>
<div class="controls-row">
<label>Volume</label>
<input type="range" min="0" max="1" step="0.01" value="0.5" data-param="volume" data-channel="revenue">
<button class="btn" data-action="mute" data-channel="revenue">M</button>
<button class="btn" data-action="solo" data-channel="revenue">S</button>
<button class="btn" data-action="reset" data-channel="revenue">R</button>
</div>
<div class="controls-row" style="margin-top:6px">
<label>Pan</label>
<input type="range" min="-1" max="1" step="0.01" value="0" data-param="pan" data-channel="revenue" style="max-width:100px">
<span style="font-size:10px;color:#5a6a8a;min-width:20px" id="revFreq">60 Hz</span>
</div>
</div>
<div class="channel-card errors" data-channel="errors">
<div class="channel-header">
<span class="channel-name">Error Rate</span>
<span class="channel-value errors" id="errVal">0%</span>
</div>
<div class="channel-meta">Noise cymbal &mdash; frequency proportional to rate</div>
<div class="controls-row">
<label>Volume</label>
<input type="range" min="0" max="1" step="0.01" value="0.4" data-param="volume" data-channel="errors">
<button class="btn" data-action="mute" data-channel="errors">M</button>
<button class="btn" data-action="solo" data-channel="errors">S</button>
<button class="btn" data-action="reset" data-channel="errors">R</button>
</div>
<div class="controls-row" style="margin-top:6px">
<label>Pan</label>
<input type="range" min="-1" max="1" step="0.01" value="0" data-param="pan" data-channel="errors" style="max-width:100px">
<span style="font-size:10px;color:#5a6a8a;min-width:20px" id="errFreq">0 Hz</span>
</div>
</div>
<div class="channel-card users" data-channel="users">
<div class="channel-header">
<span class="channel-name">Active Users</span>
<span class="channel-value users" id="usrVal">0</span>
</div>
<div class="channel-meta">Rhythmic pulse &mdash; tempo follows user count</div>
<div class="controls-row">
<label>Volume</label>
<input type="range" min="0" max="1" step="0.01" value="0.45" data-param="volume" data-channel="users">
<button class="btn" data-action="mute" data-channel="users">M</button>
<button class="btn" data-action="solo" data-channel="users">S</button>
<button class="btn" data-action="reset" data-channel="users">R</button>
</div>
<div class="controls-row" style="margin-top:6px">
<label>Pan</label>
<input type="range" min="-1" max="1" step="0.01" value="-0.3" data-param="pan" data-channel="users" style="max-width:100px">
<span style="font-size:10px;color:#5a6a8a;min-width:20px" id="usrBpm">0 BPM</span>
</div>
</div>
<div class="channel-card ambient" data-channel="ambient">
<div class="channel-header">
<span class="channel-name">Ambient Drone</span>
<span class="channel-value" style="color:#a855f7;font-size:16px;font-weight:300" id="ambHealth">--</span>
</div>
<div class="channel-meta">Background tone &mdash; shifts with system health</div>
<div class="controls-row">
<label>Volume</label>
<input type="range" min="0" max="1" step="0.01" value="0.25" data-param="volume" data-channel="ambient">
<button class="btn" data-action="mute" data-channel="ambient">M</button>
<button class="btn" data-action="solo" data-channel="ambient">S</button>
<button class="btn" data-action="reset" data-channel="ambient">R</button>
</div>
<div class="controls-row" style="margin-top:6px">
<label>Pan</label>
<input type="range" min="-1" max="1" step="0.01" value="0.5" data-param="pan" data-channel="ambient" style="max-width:100px">
<span style="font-size:10px;color:#5a6a8a;min-width:20px" id="ambFreq">110 Hz</span>
</div>
</div>
</div>
<div class="spectrum-vis">
<canvas id="spectrumCanvas"></canvas>
<div class="pulse-ring" id="pulseRing"></div>
</div>
<div class="event-log">
<h3>Sonification Events</h3>
<div class="event-list" id="eventList">
<div class="info">Console initialized. Audio context ready.</div>
</div>
</div>
<div class="mode-toggle">
<button class="mode-btn active" data-mode="normal">Normal</button>
<button class="mode-btn" data-mode="headphone">Headphone Mode</button>
<button class="mode-btn" data-mode="simulate" id="simBtn">Simulate Data</button>
</div>
<script>
(function(){
'use strict';
// Audio context
let actx = null;
let masterGain = null;
// Channel state
const state = {
revenue: { vol: 0.5, pan: 0, mute: false, solo: false, osc: null, gain: null, panner: null, val: 0, freq: 60 },
errors: { vol: 0.4, pan: 0, mute: false, solo: false, noiseNode: null, gain: null, panner: null, val: 0, freq: 0 },
users: { vol: 0.45, pan: -0.3, mute: false, solo: false, gain: null, panner: null, val: 0, bpm: 0, pulseTimer: null },
ambient: { vol: 0.25, pan: 0.5, mute: false, solo: false, osc1: null, osc2: null, gain: null, panner: null, health: 0.85 }
};
let headphoneMode = false;
let simulating = false;
let simInterval = null;
let healthValue = 0.85;
let eventList = [];
const eventLog = document.getElementById('eventList');
function initAudio() {
if (actx) return;
try {
actx = new (window.AudioContext || window.webkitAudioContext)();
masterGain = actx.createGain();
masterGain.gain.value = 0.7;
masterGain.connect(actx.destination);
setupRevenue();
setupErrors();
setupUsers();
setupAmbient();
setInitialVolumes();
logEvent('info', 'Audio context initialized. Sample rate: ' + actx.sampleRate + ' Hz');
} catch(e) {
logEvent('negative', 'Audio init failed: ' + e.message);
}
}
function setupRevenue() {
const c = state.revenue;
c.osc = actx.createOscillator();
c.osc.type = 'sawtooth';
c.osc.frequency.value = 60;
c.gain = actx.createGain();
c.gain.gain.value = 0;
c.panner = actx.createStereoPanner();
c.panner.pan.value = c.pan;
c.osc.connect(c.gain);
c.gain.connect(c.panner);
c.panner.connect(masterGain);
c.osc.start();
}
function createNoiseBuffer(length) {
const buf = actx.createBuffer(1, length, actx.sampleRate);
const data = buf.getChannelData(0);
for (let i = 0; i < length; i++) {
data[i] = Math.random() * 2 - 1;
}
return buf;
}
function setupErrors() {
const c = state.errors;
const buf = createNoiseBuffer(actx.sampleRate * 0.5);
c.noiseNode = actx.createBufferSource();
c.noiseNode.buffer = buf;
c.noiseNode.loop = true;
const bp = actx.createBiquadFilter();
bp.type = 'bandpass';
bp.frequency.value = 200;
bp.Q.value = 1.5;
c.gain = actx.createGain();
c.gain.gain.value = 0;
c.panner = actx.createStereoPanner();
c.panner.pan.value = c.pan;
c.noiseNode.connect(bp);
bp.connect(c.gain);
c.gain.connect(c.panner);
c.panner.connect(masterGain);
c.noiseNode.start();
state.errors._filter = bp;
}
function setupUsers() {
const c = state.users;
c.gain = actx.createGain();
c.gain.gain.value = 0;
c.panner = actx.createStereoPanner();
c.panner.pan.value = c.pan;
c.gain.connect(c.panner);
c.panner.connect(masterGain);
}
function setupAmbient() {
const c = state.ambient;
c.osc1 = actx.createOscillator();
c.osc1.type = 'sine';
c.osc1.frequency.value = 110;
c.osc2 = actx.createOscillator();
c.osc2.type = 'sine';
c.osc2.frequency.value = 164.81;
c.gain = actx.createGain();
c.gain.gain.value = 0;
c.panner = actx.createStereoPanner();
c.panner.pan.value = c.pan;
c.osc1.connect(c.gain);
c.osc2.connect(c.gain);
c.gain.connect(c.panner);
c.panner.connect(masterGain);
c.osc1.start();
c.osc2.start();
}
function setInitialVolumes() {
Object.keys(state).forEach(key => {
const c = state[key];
if (c.gain) c.gain.gain.value = 0;
});
state.revenue.gain.gain.value = state.revenue.vol * 0.15;
state.errors.gain.gain.value = 0;
state.ambient.gain.gain.value = state.ambient.vol * 0.08;
}
function setChannelVolume(ch, vol) {
const c = state[ch];
if (!c) return;
c.vol = vol;
updateChannelAudio(ch);
}
function setChannelPan(ch, pan) {
const c = state[ch];
if (!c) return;
c.pan = pan;
if (c.panner) c.panner.pan.value = pan;
}
function toggleMute(ch) {
const c = state[ch];
if (!c) return;
c.mute = !c.mute;
if (c.mute) {
logEvent('info', ch + ' muted');
} else {
logEvent('info', ch + ' unmuted');
}
updateChannelAudio(ch);
updateMuteButtons();
}
function toggleSolo(ch) {
const c = state[ch];
if (!c) return;
c.solo = !c.solo;
if (c.solo) {
logEvent('info', ch + ' solo');
} else {
logEvent('info', ch + ' unsolo');
}
updateAllAudio();
updateSoloButtons();
}
function isAnySolo() {
return Object.values(state).some(c => c.solo);
}
function updateChannelAudio(ch) {
const c = state[ch];
if (!c || !c.gain) return;
const anySolo = isAnySolo();
let out = 0;
if (!c.mute) {
if (!anySolo || c.solo) {
out = c.vol;
}
}
const gainNode = c.gain;
const base = ch === 'revenue' ? 0.15 :
ch === 'errors' ? 0.12 :
ch === 'users' ? 0.1 :
ch === 'ambient' ? 0.08 : 0.1;
gainNode.gain.setTargetAtTime(out * base, actx.currentTime, 0.05);
}
function updateAllAudio() {
Object.keys(state).forEach(k => updateChannelAudio(k));
}
function updateMuteButtons() {
document.querySelectorAll('[data-action="mute"]').forEach(btn => {
const ch = btn.dataset.channel;
if (state[ch] && state[ch].mute) {
btn.classList.add('muted');
btn.textContent = 'M!';
} else {
btn.classList.remove('muted');
btn.textContent = 'M';
}
});
}
function updateSoloButtons() {
document.querySelectorAll('[data-action="solo"]').forEach(btn => {
const ch = btn.dataset.channel;
if (state[ch] && state[ch].solo) {
btn.classList.add('solo');
btn.textContent = 'S!';
} else {
btn.classList.remove('solo');
btn.textContent = 'S';
}
});
}
function updateDisplay(ch, val) {
const el = document.getElementById(ch + 'Val');
if (!el) return;
if (ch === 'revenue') {
el.textContent = '$' + Math.round(val);
document.getElementById('revFreq').textContent = Math.round(state.revenue.freq) + ' Hz';
} else if (ch === 'errors') {
el.textContent = (val * 100).toFixed(1) + '%';
document.getElementById('errFreq').textContent = Math.round(state.errors.freq) + ' Hz';
} else if (ch === 'users') {
el.textContent = Math.round(val);
document.getElementById('usrBpm').textContent = Math.round(state.users.bpm) + ' BPM';
}
}
function setRevenue(val) {
val = Math.max(0, val);
const c = state.revenue;
c.val = val;
const freq = 40 + (val / 10000) * 200;
c.freq = Math.min(240, Math.max(40, freq));
if (c.osc) c.osc.frequency.setTargetAtTime(c.freq, actx.currentTime, 0.08);
updateDisplay('revenue', val);
}
function setErrors(val) {
val = Math.max(0, Math.min(1, val));
const c = state.errors;
c.val = val;
const freq = 100 + val * 2000;
c.freq = Math.min(2100, Math.max(100, freq));
if (c._filter) {
c._filter.frequency.setTargetAtTime(c.freq, actx.currentTime, 0.05);
const gainVal = val * 0.6;
c.gain.gain.setTargetAtTime(c.mute ? 0 : (isAnySolo() && !c.solo ? 0 : gainVal * c.vol), actx.currentTime, 0.05);
}
updateDisplay('errors', val);
}
function setUsers(val) {
val = Math.max(0, val);
const c = state.users;
c.val = val;
const bpm = 20 + (val / 1000) * 140;
c.bpm = Math.min(160, Math.max(20, bpm));
updateDisplay('users', val);
schedulePulse();
function schedulePulse() {
if (c.pulseTimer) {
clearTimeout(c.pulseTimer);
c.pulseTimer = null;
}
if (!actx || c.mute) return;
const interval = 60000 / c.bpm;
const now = actx.currentTime;
playPulse(now);
const next = interval / 1000;
c.pulseTimer = setTimeout(() => { schedulePulse(); }, interval);
}
function playPulse(time) {
if (c.mute) return;
const osc = actx.createOscillator();
osc.type = 'sine';
osc.frequency.value = 440 + (c.bpm / 160) * 400;
const g = actx.createGain();
g.gain.setValueAtTime(0, time);
g.gain.linearRampToValueAtTime(0.06 * c.vol, time + 0.005);
g.gain.linearRampToValueAtTime(0, time + 0.06);
osc.connect(g);
g.connect(c.panner);
osc.start(time);
osc.stop(time + 0.06);
const ring = document.getElementById('pulseRing');
if (ring) {
ring.classList.remove('pulse');
void ring.offsetWidth;
ring.classList.add('pulse');
}
}
}
function setAmbientHealth(health) {
health = Math.max(0, Math.min(1, health));
healthValue = health;
const c = state.ambient;
c.health = health;
const baseFreq = 80 + health * 80;
const fifthFreq = baseFreq * 1.5;
if (c.osc1) c.osc1.frequency.setTargetAtTime(baseFreq, actx.currentTime, 0.3);
if (c.osc2) c.osc2.frequency.setTargetAtTime(fifthFreq, actx.currentTime, 0.3);
c.gain.gain.setTargetAtTime(c.mute ? 0 : c.vol * 0.06 * (0.3 + health * 0.7), actx.currentTime, 0.2);
const dot = document.getElementById('healthDot');
const label = document.getElementById('healthLabel');
document.getElementById('ambFreq').textContent = Math.round(baseFreq) + ' Hz';
document.getElementById('ambHealth').textContent = (health * 100).toFixed(0) + '%';
if (health > 0.7) {
dot.style.background = '#22c55e';
label.textContent = 'Healthy';
} else if (health > 0.4) {
dot.style.background = '#eab308';
label.textContent = 'Degraded';
} else {
dot.style.background = '#ef4444';
label.textContent = 'Critical';
}
}
function logEvent(type, msg) {
const now = new Date();
const ts = now.toLocaleTimeString();
const div = document.createElement('div');
div.className = type;
div.textContent = '[' + ts + '] ' + msg;
eventList.push({type, msg, ts});
eventLog.prepend(div);
while (eventLog.children.length > 40) {
eventLog.removeChild(eventLog.lastChild);
}
}
function triggerEvent(oldVal, newVal, metric) {
const diff = newVal - oldVal;
const absDiff = Math.abs(diff);
if (absDiff < 0.001) return;
if (diff > 0 && absDiff > 0.05) {
playChime(metric === 'errors' ? 'positive' : 'positive', metric);
logEvent('positive', metric + ' increased: ' + oldVal.toFixed(2) + ' -> ' + newVal.toFixed(2));
} else if (diff < 0 && absDiff > 0.05) {
if (metric === 'errors') {
playChime('positive', metric);
logEvent('positive', 'Errors decreased: ' + (oldVal * 100).toFixed(1) + '% -> ' + (newVal * 100).toFixed(1) + '%');
} else {
playChime('negative', metric);
logEvent('negative', metric + ' decreased: ' + oldVal.toFixed(2) + ' -> ' + newVal.toFixed(2));
}
}
}
function playChime(type) {
if (!actx) return;
const osc = actx.createOscillator();
osc.type = 'sine';
const g = actx.createGain();
const now = actx.currentTime;
if (type === 'positive') {
osc.frequency.setValueAtTime(523, now);
osc.frequency.linearRampToValueAtTime(1047, now + 0.15);
g.gain.setValueAtTime(0.08, now);
g.gain.linearRampToValueAtTime(0, now + 0.35);
} else {
osc.frequency.setValueAtTime(523, now);
osc.frequency.linearRampToValueAtTime(262, now + 0.2);
g.gain.setValueAtTime(0.08, now);
g.gain.linearRampToValueAtTime(0, now + 0.4);
}
osc.connect(g);
g.connect(masterGain);
osc.start(now);
osc.stop(now + 0.4);
const ring = document.getElementById('pulseRing');
if (ring) { ring.classList.remove('pulse'); void ring.offsetWidth; ring.classList.add('pulse'); }
}
// Spectrum visualization
let spectrumAnimId = null;
function startSpectrum() {
const canvas = document.getElementById('spectrumCanvas');
const ctx = canvas.getContext('2d');
function resize() {
const parent = canvas.parentElement;
canvas.width = parent.offsetWidth;
canvas.height = parent.offsetHeight;
}
resize();
window.addEventListener('resize', resize);
function draw() {
resize();
const w = canvas.width, h = canvas.height;
ctx.clearRect(0, 0, w, h);
const grad = ctx.createLinearGradient(0, 0, w, 0);
grad.addColorStop(0, 'rgba(34,197,94,0.15)');
grad.addColorStop(0.3, 'rgba(59,130,246,0.15)');
grad.addColorStop(0.6, 'rgba(168,85,247,0.15)');
grad.addColorStop(1, 'rgba(239,68,68,0.15)');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, w, h);
const rev = state.revenue.val / 10000;
const err = state.errors.val;
const usr = state.users.val / 1000;
const cols = 60;
const barW = w / cols;
for (let i = 0; i < cols; i++) {
const t = i / cols;
let amp = 0;
amp += Math.sin(t * Math.PI * 2 + Date.now() * 0.001) * 0.3 * (0.2 + rev * 0.8);
amp += Math.sin(t * Math.PI * 4 + Date.now() * 0.0015) * 0.2 * err;
amp += Math.sin(t * Math.PI * 3 + Date.now() * 0.002) * 0.25 * (0.3 + usr * 0.7);
amp = Math.max(0, Math.min(1, amp * 0.8 + 0.05));
const barH = amp * h * 0.9;
const hue = 200 - i * 1.2 + err * 30;
ctx.fillStyle = 'hsla(' + hue + ', 60%, ' + (30 + amp * 30) + '%, 0.7)';
ctx.fillRect(i * barW, h - barH, barW - 1, barH);
}
spectrumAnimId = requestAnimationFrame(draw);
}
if (spectrumAnimId) cancelAnimationFrame(spectrumAnimId);
draw();
}
// Event data simulation
function initSimulation() {
let rev = 2500, err = 0.03, usr = 350;
let prevRev = rev, prevErr = err, prevUsr = usr;
setRevenue(rev);
setErrors(err);
setUsers(usr);
setAmbientHealth(0.85);
function tick() {
if (!simulating) return;
const delta = Math.random() * 200 - 60;
rev = Math.max(0, rev + delta);
err = Math.max(0, Math.min(1, err + (Math.random() - 0.48) * 0.04));
usr = Math.max(0, usr + Math.floor(Math.random() * 30 - 10));
const health = 0.9 + (rev - 2500) / 10000 - err * 0.5 + (usr - 350) / 2000;
const clampedHealth = Math.max(0, Math.min(1, health));
triggerEvent(prevRev, rev, 'revenue');
triggerEvent(prevErr, err, 'errors');
triggerEvent(prevUsr, usr, 'users');
prevRev = rev; prevErr = err; prevUsr = usr;
setRevenue(rev);
setErrors(err);
setUsers(usr);
setAmbientHealth(clampedHealth);
simInterval = setTimeout(tick, 1500 + Math.random() * 1000);
}
tick();
simulating = true;
document.getElementById('simBtn').textContent = 'Stop Simulation';
logEvent('info', 'Data simulation started');
}
function stopSimulation() {
simulating = false;
if (simInterval) { clearTimeout(simInterval); simInterval = null; }
if (state.users.pulseTimer) { clearTimeout(state.users.pulseTimer); state.users.pulseTimer = null; }
document.getElementById('simBtn').textContent = 'Simulate Data';
logEvent('info', 'Data simulation stopped');
}
// Controls binding
document.addEventListener('click', function(e) {
const btn = e.target.closest('.btn');
if (!btn) return;
const action = btn.dataset.action;
const ch = btn.dataset.channel;
if (!action || !ch) return;
if (action === 'mute') toggleMute(ch);
else if (action === 'solo') toggleSolo(ch);
else if (action === 'reset') {
const c = state[ch];
if (!c) return;
c.mute = false; c.solo = false;
updateAllAudio();
updateMuteButtons();
updateSoloButtons();
logEvent('info', ch + ' reset');
}
});
document.addEventListener('input', function(e) {
const input = e.target.closest('input[type="range"]');
if (!input) return;
const param = input.dataset.param;
const ch = input.dataset.channel;
if (!param || !ch || !state[ch]) return;
const val = parseFloat(input.value);
if (param === 'volume') setChannelVolume(ch, val);
else if (param === 'pan') setChannelPan(ch, val);
});
document.querySelectorAll('.mode-btn').forEach(btn => {
btn.addEventListener('click', function() {
const mode = this.dataset.mode;
document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
this.classList.add('active');
if (mode === 'headphone') {
headphoneMode = !headphoneMode;
if (headphoneMode) {
masterGain.gain.setTargetAtTime(0.5, actx.currentTime, 0.1);
logEvent('info', 'Headphone mode: crossfeed reduced, stereo expanded');
this.textContent = 'Headphone Mode ON';
this.classList.add('active');
} else {
masterGain.gain.setTargetAtTime(0.7, actx.currentTime, 0.1);
logEvent('info', 'Normal mode restored');
this.textContent = 'Headphone Mode';
}
} else if (mode === 'simulate') {
if (simulating) {
stopSimulation();
} else {
initSimulation();
}
} else if (mode === 'normal') {
if (headphoneMode) {
headphoneMode = false;
masterGain.gain.setTargetAtTime(0.7, actx.currentTime, 0.1);
logEvent('info', 'Normal mode restored');
}
stopSimulation();
}
});
});
// Init
initAudio();
startSpectrum();
document.getElementById('simBtn').click();
// Cleanup on page unload
window.addEventListener('beforeunload', function() {
if (spectrumAnimId) cancelAnimationFrame(spectrumAnimId);
if (state.users.pulseTimer) clearTimeout(state.users.pulseTimer);
if (simInterval) clearTimeout(simInterval);
if (actx) actx.close();
});
})();
</script>
</body>
</html>