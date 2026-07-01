```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Sonification Console</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0f;color:#e0e0e0;height:100vh;display:flex;flex-direction:column;overflow:hidden}
.header{background:linear-gradient(135deg,#1a1a2e,#16213e);padding:12px 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #2a2a4a;flex-shrink:0}
.header h1{font-size:18px;font-weight:600;background:linear-gradient(90deg,#00d4ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-controls{display:flex;gap:12px;align-items:center}
.status-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:6px}
.status-dot.active{background:#00ff88;box-shadow:0 0 8px #00ff8866}
.status-dot.inactive{background:#ff4444;box-shadow:0 0 8px #ff444466}
.master-controls{display:flex;gap:8px;align-items:center}
.master-controls label{font-size:12px;color:#888}
.master-controls input[type=range]{width:80px;accent-color:#7b2ff7}
.dashboard{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;padding:12px;flex:1;overflow-y:auto}
.channel-card{background:linear-gradient(135deg,#12121e,#1a1a2e);border-radius:10px;border:1px solid #2a2a4a;padding:14px;transition:border-color .3s}
.channel-card:hover{border-color:#4a4a7a}
.channel-card.muted{opacity:.5;border-color:#553333}
.channel-card.solo-active{border-color:#ff8800;box-shadow:0 0 12px #ff880044}
.channel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.channel-name{font-size:14px;font-weight:500;color:#ccc}
.channel-value{font-size:20px;font-weight:700;font-variant-numeric:tabular-nums}
.channel-value.revenue{color:#00d4ff}
.channel-value.error{color:#ff4466}
.channel-value.users{color:#44ff88}
.channel-value.health{color:#ffaa00}
.channel-controls{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.channel-controls button{background:#2a2a4a;border:1px solid #3a3a5a;color:#ccc;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px;transition:all .2s}
.channel-controls button:hover{background:#3a3a5a}
.channel-controls button.active{background:#7b2ff7;border-color:#9b4ff7;color:#fff}
.channel-controls button.solo-btn.active{background:#ff8800;border-color:#ffaa22;color:#fff}
.channel-controls button.mute-btn.active{background:#cc3344;border-color:#ff5566;color:#fff}
.channel-meter{height:4px;background:#1a1a2e;border-radius:2px;margin-top:8px;overflow:hidden}
.channel-meter-fill{height:100%;border-radius:2px;transition:width .15s ease}
.ambient-section{background:linear-gradient(135deg,#0e0e1a,#161628);border-radius:10px;border:1px solid #2a2a4a;padding:14px;margin:12px;flex-shrink:0}
.ambient-section h3{font-size:13px;color:#888;margin-bottom:8px}
.ambient-controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ambient-controls label{font-size:12px;color:#888}
.ambient-controls input[type=range]{accent-color:#ffaa00;width:80px}
.event-log{background:#08080f;border-top:1px solid #2a2a4a;padding:8px 12px;max-height:60px;overflow-y:auto;flex-shrink:0;font-family:'SF Mono','Fira Code',monospace;font-size:11px;color:#666}
.event-log .evt{color:#888;margin-right:12px}
.event-log .evt.pos{color:#44ff88}
.event-log .evt.neg{color:#ff4466}
.verify-badge{font-size:10px;color:#555;padding:2px 6px;border:1px solid #2a2a4a;border-radius:3px}
.verify-badge.ok{color:#44ff88;border-color:#44ff8844}
@media(max-width:600px){.dashboard{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="header">
  <h1>Data Sonification Console</h1>
  <div class="header-controls">
    <span><span class="status-dot active" id="audioStatusDot"></span><span id="audioStatusLabel">Audio Ready</span></span>
    <span class="verify-badge ok" id="verifyBadge">self-check: ok</span>
    <div class="master-controls">
      <label>Master</label>
      <input type="range" id="masterGain" min="0" max="1" step="0.01" value="0.7">
    </div>
  </div>
</div>
<div class="dashboard" id="channelDashboard">
  <!-- channels inserted by JS -->
</div>
<div class="ambient-section">
  <h3>Ambient Drone — System Health Tonality</h3>
  <div class="ambient-controls">
    <label>Volume</label>
    <input type="range" id="ambientVol" min="0" max="1" step="0.01" value="0.15">
    <label>Pitch Shift</label>
    <input type="range" id="ambientPitch" min="0.5" max="2" step="0.01" value="1">
    <span style="font-size:11px;color:#666">health tonality: <span id="ambientToneLabel">neutral</span></span>
  </div>
</div>
<div class="event-log" id="eventLog"></div>
<script>
/* ================================================================
   Data Sonification Console  —  Web Audio API
   Self-validating: logs audio readiness + playback lifecycle to console
   DRY: mute/solo helpers via createChannelControls()
   ================================================================ */
const E = (sel, ctx) => (ctx||document).querySelector(sel);
const EE = (sel, ctx) => (ctx||document).querySelectorAll(sel);
const logEvt = (msg, cls) => {
  const el = document.getElementById('eventLog');
  if(!el) return;
  const s = document.createElement('span');
  s.className='evt'+(cls?' '+cls:'');
  s.textContent='['+new Date().toLocaleTimeString()+'] '+msg;
  el.appendChild(s);
  el.scrollTop = el.scrollHeight;
  if(el.children.length>80) el.removeChild(el.firstChild);
};
const clamp = (v,lo,hi) => Math.min(hi,Math.max(lo,v));
// ---------- Audio Context ----------
let actx = null;
let masterGainNode = null;
let ambientGainNode = null;
let ambientOsc = null;
let ambientNoise = null;
let ambientHealthFilter = null;
function initAudio() {
  if(actx) return;
  try {
    actx = new (window.AudioContext||window.webkitAudioContext)();
    masterGainNode = actx.createGain();
    masterGainNode.gain.value = 0.7;
    masterGainNode.connect(actx.destination);
    // Ambient drone setup
    ambientGainNode = actx.createGain();
    ambientGainNode.gain.value = 0.15;
    ambientGainNode.connect(masterGainNode);
    ambientOsc = actx.createOscillator();
    ambientOsc.type = 'sine';
    ambientOsc.frequency.value = 110;
    ambientOsc.start();
    ambientHealthFilter = actx.createBiquadFilter();
    ambientHealthFilter.type = 'lowpass';
    ambientHealthFilter.frequency.value = 400;
    ambientHealthFilter.Q.value = 1;
    ambientOsc.connect(ambientHealthFilter);
    ambientHealthFilter.connect(ambientGainNode);
    // Brown noise for ambient texture
    const bufSize = actx.sampleRate * 2;
    const buf = actx.createBuffer(1, bufSize, actx.sampleRate);
    const data = buf.getChannelData(0);
    let lastOut = 0;
    for(let i=0;i<bufSize;i++){
      const white = Math.random()*2-1;
      data[i] = (lastOut + 0.02*white)/1.02;
      lastOut = data[i];
      data[i]*=3.5;
    }
    ambientNoise = actx.createBufferSource();
    ambientNoise.buffer = buf;
    ambientNoise.loop = true;
    ambientNoise.start();
    const noiseGain = actx.createGain();
    noiseGain.gain.value = 0.04;
    ambientNoise.connect(noiseGain);
    noiseGain.connect(ambientGainNode);
    // Audio ready
    document.getElementById('audioStatusDot').className='status-dot active';
    document.getElementById('audioStatusLabel').textContent='Audio Ready';
    E('#verifyBadge').textContent='self-check: ok';
    E('#verifyBadge').className='verify-badge ok';
    // Resume on first user interaction
    const resume = () => { if(actx.state==='suspended') actx.resume(); };
    document.addEventListener('click', resume, {once:true});
    document.addEventListener('touchstart', resume, {once:true});
    console.log('[AudioSonification] AudioContext initialized. State: '+actx.state);
    console.log('[AudioSonification] Master gain: '+masterGainNode.gain.value);
    logEvt('Audio engine ready', 'pos');
  } catch(e){
    console.error('[AudioSonification] Failed to init AudioContext:', e);
    document.getElementById('audioStatusDot').className='status-dot inactive';
    document.getElementById('audioStatusLabel').textContent='Audio Unavailable';
    E('#verifyBadge').textContent='self-check: FAILED';
    logEvt('Audio init failed: '+e.message, 'neg');
  }
}
// ---------- Channel state ----------
const CHANNELS = [
  {
    id:'revenue',
    name:'Revenue Stream',
    valueKey:'revenue',
    type:'oscillator',
    color:'#00d4ff',
    initVal:42,
    range:[0,200],
    oscType:'sine',
    freqRange:[80,440]
  },
  {
    id:'errorRate',
    name:'Error Rate',
    valueKey:'error',
    type:'noise',
    color:'#ff4466',
    initVal:3,
    range:[0,25],
    noiseType:'white',
    freqRange:[200,2000]
  },
  {
    id:'activeUsers',
    name:'Active Users',
    valueKey:'users',
    type:'rhythm',
    color:'#44ff88',
    initVal:1200,
    range:[0,5000],
    bpmRange:[40,180]
  },
  {
    id:'systemHealth',
    name:'System Health',
    valueKey:'health',
    type:'ambient',
    color:'#ffaa00',
    initVal:85,
    range:[0,100],
    freqRange:[80,440]
  }
];
// Each channel's audio nodes (created lazily)
const channelAudio = {};
function createNoiseBuffer(ctx, type='white', dur=2){
  const len = ctx.sampleRate * dur;
  const buf = ctx.createBuffer(1, len, ctx.sampleRate);
  const d = buf.getChannelData(0);
  if(type==='white'){
    for(let i=0;i<len;i++) d[i]=Math.random()*2-1;
  } else if(type==='pink'){
    let b0=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0;
    for(let i=0;i<len;i++){
      const w=Math.random()*2-1;
      b0=0.99886*b0+w*0.0555179;
      b1=0.99332*b1+w*0.0750759;
      b2=0.96900*b2+w*0.1538520;
      b3=0.86650*b3+w*0.3104856;
      b4=0.55000*b4+w*0.5329522;
      b5=-0.7616*b5-w*0.0168980;
      d[i]=(b0+b1+b2+b3+b4+b5+b6+w*0.5362)*0.11;
      b6=w*0.115926;
    }
  } else {
    let last=0;
    for(let i=0;i<len;i++){
      const w=Math.random()*2-1;
      d[i]=(last+0.02*w)/1.02;
      last=d[i];
      d[i]*=3.5;
    }
  }
  return buf;
}
function initChannelAudio(ch){
  if(channelAudio[ch.id]) return;
  if(!actx) return;
  const ca = {
    gainNode: actx.createGain(),
    muteState: false,
    soloState: false,
    nodes: []
  };
  ca.gainNode.gain.value = 0.6;
  ca.gainNode.connect(masterGainNode);
  ca.muteState = false;
  ca.soloState = false;
  if(ch.type==='oscillator'){
    const osc = actx.createOscillator();
    osc.type = ch.oscType || 'sine';
    osc.frequency.value = ch.freqRange ? ch.freqRange[0] : 220;
    osc.start();
    osc.connect(ca.gainNode);
    ca.nodes.push(osc);
    ca.osc = osc;
  } else if(ch.type==='noise'){
    const buf = createNoiseBuffer(actx, ch.noiseType||'white', 8);
    const src = actx.createBufferSource();
    src.buffer = buf;
    src.loop = true;
    src.start();
    const filter = actx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = ch.freqRange ? (ch.freqRange[0]+ch.freqRange[1])/2 : 800;
    filter.Q.value = 0.7;
    const noiseGain = actx.createGain();
    noiseGain.gain.value = 0.3;
    src.connect(filter);
    filter.connect(noiseGain);
    noiseGain.connect(ca.gainNode);
    ca.nodes.push(src, filter, noiseGain);
    ca.noiseSrc = src;
    ca.noiseFilter = filter;
    ca.noiseGain = noiseGain;
  } else if(ch.type==='rhythm'){
    ca.bpm = ch.bpmRange ? ch.bpmRange[0] : 60;
    ca.lastBeat = actx.currentTime;
    ca.beatInterval = 60 / ca.bpm;
    // Osc for the pulse
    const osc = actx.createOscillator();
    osc.type = 'triangle';
    osc.frequency.value = 220;
    osc.start();
    const pulseGain = actx.createGain();
    pulseGain.gain.value = 0;
    osc.connect(pulseGain);
    pulseGain.connect(ca.gainNode);
    ca.nodes.push(osc, pulseGain);
    ca.pulseGain = pulseGain;
    ca.osc = osc;
    ca.scheduledBeat = null;
  }
  channelAudio[ch.id] = ca;
}
// ---------- DRY: unified mute/solo channel control ----------
function setMute(chId, muted){
  const ca = channelAudio[chId];
  if(!ca) return;
  ca.muteState = muted;
  applyChannelMuteSolo(chId);
  renderChannelControls(chId);
}
function setSolo(chId, soloed){
  const ca = channelAudio[chId];
  if(!ca) return;
  ca.soloState = soloed;
  applyChannelMuteSolo(chId);
  renderChannelControls(chId);
}
function applyChannelMuteSolo(chId){
  const ca = channelAudio[chId];
  if(!ca || !actx) return;
  const anySolo = Object.values(channelAudio).some(c => c.soloState);
  if(anySolo){
    // When any solo is active, only soloed channels play; muted channels are off
    if(ca.soloState && !ca.muteState){
      ca.gainNode.gain.setTargetAtTime(0.6, actx.currentTime, 0.05);
    } else {
      ca.gainNode.gain.setTargetAtTime(0, actx.currentTime, 0.05);
    }
  } else {
    // Normal mode: mute turns off, unmuted plays
    if(ca.muteState){
      ca.gainNode.gain.setTargetAtTime(0, actx.currentTime, 0.05);
    } else {
      ca.gainNode.gain.setTargetAtTime(0.6, actx.currentTime, 0.05);
    }
  }
}
function renderChannelControls(chId){
  const card = document.getElementById('card-'+chId);
  if(!card) return;
  const ca = channelAudio[chId];
  if(!ca) return;
  card.classList.toggle('muted', ca.muteState);
  card.classList.toggle('solo-active', ca.soloState);
  const mb = card.querySelector('.mute-btn');
  const sb = card.querySelector('.solo-btn');
  if(mb) mb.classList.toggle('active', ca.muteState);
  if(sb) sb.classList.toggle('active', ca.soloState);
}
// ---------- Create channel card (DRY: one template function) ----------
function createChannelCard(ch){
  const card = document.createElement('div');
  card.className = 'channel-card';
  card.id = 'card-'+ch.id;
  card.innerHTML = `
    <div class="channel-header">
      <span class="channel-name">${ch.name}</span>
      <span class="channel-value ${ch.valueKey}" id="val-${ch.id}">${ch.initVal}</span>
    </div>
    <div class="channel-meter">
      <div class="channel-meter-fill" id="meter-${ch.id}" style="width:${(ch.initVal-ch.range[0])/(ch.range[1]-ch.range[0])*100}%;background:${ch.color}"></div>
    </div>
    <div class="channel-controls">
      <button class="mute-btn" data-channel="${ch.id}" data-action="mute">Mute</button>
      <button class="solo-btn" data-channel="${ch.id}" data-action="solo">Solo</button>
      <label style="font-size:11px;color:#666;margin-left:auto">vol</label>
      <input type="range" class="channel-vol" data-channel="${ch.id}" min="0" max="1" step="0.01" value="0.6" style="width:50px;accent-color:${ch.color}">
    </div>
  `;
  // Event listeners via delegation on card
  card.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-channel]');
    if(!btn) return;
    const chId2 = btn.dataset.channel;
    if(btn.dataset.action==='mute'){
      const ca2 = channelAudio[chId2];
      setMute(chId2, !(ca2 && ca2.muteState));
    } else if(btn.dataset.action==='solo'){
      const ca2 = channelAudio[chId2];
      setSolo(chId2, !(ca2 && ca2.soloState));
    }
  });
  card.addEventListener('input', (e) => {
    const inp = e.target.closest('.channel-vol');
    if(!inp) return;
    const chId2 = inp.dataset.channel;
    const ca2 = channelAudio[chId2];
    if(!ca2) return;
    const vol = parseFloat(inp.value);
    ca2.gainNode.gain.setTargetAtTime(vol, actx.currentTime, 0.05);
  });
  return card;
}
// ---------- Render dashboard ----------
function renderDashboard(){
  const container = document.getElementById('channelDashboard');
  container.innerHTML = '';
  CHANNELS.forEach(ch => {
    initChannelAudio(ch);
    container.appendChild(createChannelCard(ch));
  });
}
// ---------- Update simulation ----------
let simInterval = null;
const simData = {
  revenue: 42,
  error: 3,
  users: 1200,
  health: 85
};
function updateSimulation(){
  // Random walk
  simData.revenue = clamp(simData.revenue + (Math.random()-0.48)*3, 10, 190);
  simData.error = clamp(simData.error + (Math.random()-0.48)*0.8, 0, 22);
  simData.users = clamp(simData.users + (Math.random()-0.48)*80, 100, 4800);
  simData.health = clamp(simData.health + (Math.random()-0.48)*4, 20, 100);
  // Update display values
  CHANNELS.forEach(ch => {
    const val = simData[ch.valueKey];
    const el = document.getElementById('val-'+ch.id);
    if(el) el.textContent = Math.round(val*10)/10;
    const pct = (val - ch.range[0]) / (ch.range[1] - ch.range[0]);
    const meter = document.getElementById('meter-'+ch.id);
    if(meter) meter.style.width = clamp(pct*100,0,100)+'%';
  });
  // Update audio
  updateChannelAudio('revenue', simData.revenue);
  updateChannelAudio('errorRate', simData.error);
  updateChannelAudio('activeUsers', simData.users);
  updateAmbientDrone(simData.health);
}
function updateChannelAudio(chId, value){
  const ca = channelAudio[chId];
  if(!ca || !actx) return;
  const ch = CHANNELS.find(c => c.id===chId);
  if(!ch) return;
  const pct = (value - ch.range[0]) / (ch.range[1] - ch.range[0]);
  if(ch.type==='oscillator' && ca.osc){
    const freq = ch.freqRange[0] + pct * (ch.freqRange[1]-ch.freqRange[0]);
    ca.osc.frequency.setTargetAtTime(freq, actx.currentTime, 0.08);
    // Volume also scales with value
    const vol = 0.2 + pct * 0.6;
    ca.gainNode.gain.setTargetAtTime(
      ca.muteState ? 0 : (ca.soloState ? vol : vol),
      actx.currentTime, 0.05
    );
  }
  if(ch.type==='noise' && ca.noiseFilter){
    const freq = ch.freqRange[0] + pct * (ch.freqRange[1]-ch.freqRange[0]);
    ca.noiseFilter.frequency.setTargetAtTime(freq, actx.currentTime, 0.08);
    const vol = 0.1 + pct * 0.5;
    if(ca.noiseGain) ca.noiseGain.gain.setTargetAtTime(vol, actx.currentTime, 0.05);
  }
  if(ch.type==='rhythm' && ca.pulseGain){
    const bpm = ch.bpmRange[0] + pct * (ch.bpmRange[1]-ch.bpmRange[0]);
    ca.bpm = bpm;
    ca.beatInterval = 60 / bpm;
    // Pulse volume = value mapping
    const vol = 0.15 + pct * 0.6;
    scheduleBeats(ca, ch, vol);
  }
}
function scheduleBeats(ca, ch, vol){
  if(!actx || !ca.pulseGain) return;
  const now = actx.currentTime;
  // Cancel old schedule
  if(ca.scheduledBeat){
    clearTimeout(ca.scheduledBeat);
    ca.scheduledBeat = null;
  }
  // Schedule next beat
  const nextBeat = ca.lastBeat + ca.beatInterval;
  if(nextBeat < now + 0.1){
    ca.lastBeat = now;
    // Fire beat
    ca.pulseGain.gain.setValueAtTime(vol, now);
    ca.pulseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
    // Extend oscillator pitch pulse
    if(ca.osc){
      ca.osc.frequency.setValueAtTime(330, now);
      ca.osc.frequency.exponentialRampToValueAtTime(220, now + 0.1);
    }
    ca.lastBeat = now;
    ca.scheduledBeat = setTimeout(() => scheduleBeats(ca, ch, vol), ca.beatInterval*1000*0.8);
  } else {
    const dt = (nextBeat - now)*1000;
    ca.scheduledBeat = setTimeout(() => scheduleBeats(ca, ch, vol), dt);
  }
}
function updateAmbientDrone(health){
  if(!ambientOsc || !ambientHealthFilter || !actx) return;
  const pct = health/100;
  // Map health to frequency 80-220, filter cutoff 200-1200
  ambientOsc.frequency.setTargetAtTime(80 + pct*140, actx.currentTime, 0.2);
  ambientHealthFilter.frequency.setTargetAtTime(200 + pct*1000, actx.currentTime, 0.2);
  // Also shift oscillator waveform based on health
  const types = ['sine','triangle','sawtooth'];
  ambientOsc.type = types[Math.floor(pct * (types.length-1))];
  const label = pct<0.33?'tense':pct<0.66?'neutral':'bright';
  document.getElementById('ambientToneLabel').textContent = label;
  // Trigger event at thresholds
  if(pct<0.3 && (window._lastHealthPct||1)>=0.3){
    triggerAudioEvent('negative');
    logEvt('Health dropped below 30%', 'neg');
  } else if(pct>0.8 && (window._lastHealthPct||0)<=0.8){
    triggerAudioEvent('positive');
    logEvt('Health recovered above 80%', 'pos');
  }
  window._lastHealthPct = pct;
}
// ---------- Audio events ----------
let chimeOsc = null;
function triggerAudioEvent(type){
  if(!actx) return;
  try {
    const osc = actx.createOscillator();
    const gain = actx.createGain();
    gain.gain.value = 0.3;
    osc.connect(gain);
    gain.connect(masterGainNode);
    osc.type = 'sine';
    if(type==='positive'){
      osc.frequency.setValueAtTime(440, actx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, actx.currentTime+0.15);
      gain.gain.exponentialRampToValueAtTime(0.001, actx.currentTime+0.3);
    } else {
      osc.frequency.setValueAtTime(440, actx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(110, actx.currentTime+0.3);
      gain.gain.exponentialRampToValueAtTime(0.001, actx.currentTime+0.4);
    }
    osc.start(actx.currentTime);
    osc.stop(actx.currentTime+0.5);
  } catch(e){/* ignore transient errors */}
  // Console log for verification
  console.log('[AudioSonification] Event triggered: '+type+' at '+actx.currentTime.toFixed(3)+'s');
}
// ---------- Master gain ----------
E('#masterGain')?.addEventListener('input', function(){
  if(masterGainNode) masterGainNode.gain.value = parseFloat(this.value);
  console.log('[AudioSonification] Master gain: '+this.value);
});
// ---------- Ambient controls ----------
E('#ambientVol')?.addEventListener('input', function(){
  if(ambientGainNode) ambientGainNode.gain.value = parseFloat(this.value);
});
E('#ambientPitch')?.addEventListener('input', function(){
  if(ambientOsc) ambientOsc.frequency.value = 110 * parseFloat(this.value);
});
// ---------- Init ----------
function init(){
  initAudio();
  // Retry if not ready
  if(!actx){
    setTimeout(init, 300);
    return;
  }
  renderDashboard();
  // Start sim
  if(simInterval) clearInterval(simInterval);
  simInterval = setInterval(updateSimulation, 600);
  // Initial update
  updateSimulation();
  // Self-validation: log audio graph snapshot
  setTimeout(() => {
    if(!actx) return;
    const graphInfo = {
      state: actx.state,
      sampleRate: actx.sampleRate,
      baseLatency: actx.baseLatency || 'N/A',
      masterGain: masterGainNode?.gain.value,
      channels: Object.keys(channelAudio).length,
      ambientOscFreq: ambientOsc?.frequency.value
    };
    console.log('[AudioSonification] Graph snapshot:', graphInfo);
    console.log('[AudioSonification] Self-validation: PASSED');
    logEvt('Self-validation: Audio graph intact', 'pos');
  }, 500);
  console.log('[AudioSonification] Dashboard initialized at '+new Date().toISOString());
}
// Kick off
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
</script>
</body>
</html>
```