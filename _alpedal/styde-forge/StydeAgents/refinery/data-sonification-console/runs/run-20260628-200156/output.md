AudioContext = new (window.AudioContext || window.webkitAudioContext)()
masterGain = AudioContext.createGain()
masterGain.gain.value = 0.7
masterGain.connect(AudioContext.destination)
dummyData = { revenue: 75, errorRate: 12, activeUsers: 340, churnRate: 5, uptime: 99.8 }
prevData = { ...dummyData }
channels = {}
healthScore = 0
soloActive = false
class AudioChannel {
  constructor(label, color) {
    this.label = label
    this.color = color
    this.gain = AudioContext.createGain()
    this.gain.gain.value = 0.5
    this.panner = AudioContext.createStereoPanner()
    this.panner.pan.value = 0
    this.gain.connect(this.panner)
    this.panner.connect(masterGain)
    this.muted = false
    this.soloed = false
    this.volume = 0.5
    this.pan = 0
    this.nodes = []
  }
  applyMuteSolo() {
    let targetGain = this.volume
    if (this.muted) targetGain = 0
    if (soloActive && !this.soloed) targetGain = 0
    if (soloActive && this.soloed) targetGain = this.volume
    this.gain.gain.setTargetAtTime(targetGain, AudioContext.currentTime, 0.05)
    this._reapplySoloGuard()
  }
  _reapplySoloGuard() {
    if (!soloActive) return
    for (const key in channels) {
      const ch = channels[key]
      if (ch === this) continue
      const chTarget = (ch.soloed && !ch.muted) ? ch.volume : 0
      ch.gain.gain.setTargetAtTime(chTarget, AudioContext.currentTime, 0.02)
    }
  }
  setVolume(v) {
    this.volume = Math.max(0, Math.min(1, v))
    this.applyMuteSolo()
  }
  setPan(v) {
    this.pan = Math.max(-1, Math.min(1, v))
    this.panner.pan.setTargetAtTime(this.pan, AudioContext.currentTime, 0.05)
  }
  toggleMute() {
    this.muted = !this.muted
    this.applyMuteSolo()
    console.log('CHANNEL:' + this.label + ' mute=' + this.muted + ' at t=' + AudioContext.currentTime.toFixed(3))
  }
  toggleSolo() {
    this.soloed = !this.soloed
    const anySolo = Object.values(channels).some(c => c.soloed)
    soloActive = anySolo
    for (const key in channels) channels[key].applyMuteSolo()
    console.log('CHANNEL:' + this.label + ' solo=' + this.soloed + ' soloActive=' + soloActive + ' at t=' + AudioContext.currentTime.toFixed(3))
  }
}
function createOscillatorChannel(label, type, baseFreq, color) {
  const ch = new AudioChannel(label, color)
  const osc = AudioContext.createOscillator()
  osc.type = type
  osc.frequency.value = baseFreq
  const gainNode = AudioContext.createGain()
  gainNode.gain.value = 0.3
  osc.connect(gainNode)
  gainNode.connect(ch.gain)
  osc.start()
  ch.nodes = [osc, gainNode]
  channels[label] = ch
  return ch
}
function createNoiseChannel(label, color) {
  const ch = new AudioChannel(label, color)
  const bufferSize = AudioContext.sampleRate * 2
  const buffer = AudioContext.createBuffer(1, bufferSize, AudioContext.sampleRate)
  const data = buffer.getChannelData(0)
  for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1
  const source = AudioContext.createBufferSource()
  source.buffer = buffer
  source.loop = true
  const filter = AudioContext.createBiquadFilter()
  filter.type = 'highpass'
  filter.frequency.value = 1000
  const gainNode = AudioContext.createGain()
  gainNode.gain.value = 0.15
  source.connect(filter)
  filter.connect(gainNode)
  gainNode.connect(ch.gain)
  source.start()
  ch.nodes = [source, filter, gainNode]
  ch.setFilter = function(freq) {
    filter.frequency.setTargetAtTime(freq, AudioContext.currentTime, 0.1)
  }
  channels[label] = ch
  return ch
}
function createPulseChannel(label, color) {
  const ch = new AudioChannel(label, color)
  ch.tempo = 120
  ch.lastPulse = 0
  ch.pulseInterval = null
  ch.pulseGain = AudioContext.createGain()
  ch.pulseGain.gain.value = 0
  ch.pulseGain.connect(ch.gain)
  ch.nodes = [ch.pulseGain]
  ch.startPulse = function() {
    const intervalMs = 60000 / ch.tempo
    const osc = AudioContext.createOscillator()
    osc.type = 'sine'
    osc.frequency.value = 440
    const g = AudioContext.createGain()
    g.gain.value = 0.2
    g.gain.exponentialRampToValueAtTime(0.001, AudioContext.currentTime + 0.08)
    osc.connect(g)
    g.connect(ch.pulseGain)
    osc.start()
    osc.stop(AudioContext.currentTime + 0.08)
    ch.lastPulse++
    console.log('PULSE:' + label + ' beat=' + ch.lastPulse + ' tempo=' + ch.tempo + ' at t=' + AudioContext.currentTime.toFixed(3))
  }
  ch.setTempo = function(bpm) {
    ch.tempo = Math.max(20, Math.min(300, bpm))
    if (ch.pulseInterval) clearInterval(ch.pulseInterval)
    ch.pulseInterval = setInterval(() => ch.startPulse(), 60000 / ch.tempo)
  }
  channels[label] = ch
  return ch
}
function createChimeChannel(label, color) {
  const ch = new AudioChannel(label, color)
  ch.triggerAscending = function() {
    const t = AudioContext.currentTime
    const notes = [523.25, 659.25, 783.99]
    notes.forEach((freq, i) => {
      const osc = AudioContext.createOscillator()
      osc.type = 'sine'
      osc.frequency.value = freq
      const g = AudioContext.createGain()
      g.gain.setValueAtTime(0, t + i * 0.12)
      g.gain.linearRampToValueAtTime(0.25, t + i * 0.12 + 0.02)
      g.gain.exponentialRampToValueAtTime(0.001, t + i * 0.12 + 0.4)
      osc.connect(g)
      g.connect(ch.gain)
      osc.start(t + i * 0.12)
      osc.stop(t + i * 0.12 + 0.4)
    })
    console.log('CHIME:ascending at t=' + t.toFixed(3))
  }
  ch.triggerDescending = function() {
    const t = AudioContext.currentTime
    const notes = [783.99, 659.25, 523.25]
    notes.forEach((freq, i) => {
      const osc = AudioContext.createOscillator()
      osc.type = 'sine'
      osc.frequency.value = freq
      const g = AudioContext.createGain()
      g.gain.setValueAtTime(0, t + i * 0.15)
      g.gain.linearRampToValueAtTime(0.2, t + i * 0.15 + 0.02)
      g.gain.exponentialRampToValueAtTime(0.001, t + i * 0.15 + 0.5)
      osc.connect(g)
      g.connect(ch.gain)
      osc.start(t + i * 0.15)
      osc.stop(t + i * 0.15 + 0.5)
    })
    console.log('CHIME:descending at t=' + t.toFixed(3))
  }
  channels[label] = ch
  return ch
}
function createAmbientDrone() {
  const ch = new AudioChannel('AmbientDrone', '#9b59b6')
  const oscs = []
  const harmonics = [55, 82.5, 110, 165, 220]
  harmonics.forEach((freq) => {
    const osc = AudioContext.createOscillator()
    osc.type = 'sawtooth'
    osc.frequency.value = freq
    const g = AudioContext.createGain()
    g.gain.value = 0.04
    osc.connect(g)
    g.connect(ch.gain)
    osc.start()
    oscs.push({ osc, gain: g })
  })
  ch.nodes = oscs
  ch.setHealth = function(health) {
    const baseFreq = 40 + health * 0.6
    const filterFreq = 200 + health * 8
    oscs.forEach((o, i) => {
      const f = baseFreq * (i + 1) * 0.5
      o.osc.frequency.setTargetAtTime(f, AudioContext.currentTime, 0.5)
      o.gain.gain.setTargetAtTime(0.02 + health * 0.04, AudioContext.currentTime, 0.5)
    })
    console.log('AMBIENT:health=' + health.toFixed(2) + ' baseFreq=' + baseFreq.toFixed(1) + ' at t=' + AudioContext.currentTime.toFixed(3))
  }
  channels[label] = ch
  return ch
}
function initChannels() {
  createOscillatorChannel('Revenue', 'sine', 80, '#27ae60')
  createNoiseChannel('ErrorRate', '#e74c3c')
  createPulseChannel('ActiveUsers', '#3498db')
  createChimeChannel('Events', '#f39c12')
  createAmbientDrone()
  console.log('AUDIO_READY: channels=' + Object.keys(channels).length + ' at t=' + AudioContext.currentTime.toFixed(3))
}
function updateSonification(data) {
  const revCh = channels['Revenue']
  if (revCh && !revCh.muted && !(soloActive && !revCh.soloed)) {
    const freq = 40 + (data.revenue / 100) * 160
    const vol = 0.1 + (data.revenue / 100) * 0.4
    revCh.nodes[0].frequency.setTargetAtTime(freq, AudioContext.currentTime, 0.3)
    revCh.nodes[1].gain.setTargetAtTime(vol, AudioContext.currentTime, 0.3)
    revCh.applyMuteSolo()
  }
  const errCh = channels['ErrorRate']
  if (errCh && typeof errCh.setFilter === 'function') {
    const filterFreq = 200 + (data.errorRate / 100) * 6000
    errCh.setFilter(filterFreq)
    errCh.applyMuteSolo()
  }
  const userCh = channels['ActiveUsers']
  if (userCh && typeof userCh.setTempo === 'function') {
    const bpm = 40 + (data.activeUsers / 1000) * 180
    userCh.setTempo(bpm)
    userCh.applyMuteSolo()
  }
  const eventCh = channels['Events']
  if (eventCh) {
    if (data.revenue > prevData.revenue + 2) eventCh.triggerAscending()
    else if (data.revenue < prevData.revenue - 2) eventCh.triggerDescending()
    if (data.errorRate < prevData.errorRate - 1) eventCh.triggerAscending()
    else if (data.errorRate > prevData.errorRate + 1) eventCh.triggerDescending()
    if (data.uptime > prevData.uptime && data.uptime >= 99.9) eventCh.triggerAscending()
    eventCh.applyMuteSolo()
  }
  healthScore = (data.revenue * 0.25) + ((100 - data.errorRate) * 0.35) + ((data.activeUsers / 1000) * 100 * 0.2) + (data.uptime * 0.2)
  healthScore = Math.max(0, Math.min(100, healthScore))
  const ambientCh = channels['AmbientDrone']
  if (ambientCh && typeof ambientCh.setHealth === 'function') {
    ambientCh.setHealth(healthScore / 100)
  }
  Object.assign(prevData, data)
  console.log('SONIFICATION_UPDATE: revenue=' + data.revenue + ' errors=' + data.errorRate + ' users=' + data.activeUsers + ' health=' + healthScore.toFixed(1) + ' at t=' + AudioContext.currentTime.toFixed(3))
}
function buildUI() {
  const container = document.createElement('div')
  container.style.cssText = 'font-family:monospace;background:#1a1a2e;color:#e0e0e0;padding:20px;max-width:600px;margin:auto'
  const title = document.createElement('h1')
  title.textContent = 'DATA SONIFICATION CONSOLE'
  title.style.cssText = 'color:#ff6b6b;text-align:center;font-size:18px;margin:0 0 20px 0;letter-spacing:2px'
  container.appendChild(title)
  const statusBar = document.createElement('div')
  statusBar.id = 'statusBar'
  statusBar.style.cssText = 'background:#16213e;padding:8px 12px;margin-bottom:15px;border-left:3px solid #ff6b6b;font-size:11px'
  statusBar.innerHTML = 'AudioContext: <span id="audioStatus" style="color:#e74c3c">STOPPED</span> | Health: <span id="healthDisplay">--</span>% | <span id="eventLogDisplay" style="color:#f39c12">--</span>'
  container.appendChild(statusBar)
  const startBtn = document.createElement('button')
  startBtn.id = 'startBtn'
  startBtn.textContent = '> INITIALIZE AUDIO'
  startBtn.style.cssText = 'background:#e74c3c;color:#fff;border:none;padding:10px 20px;font-family:monospace;font-size:13px;cursor:pointer;margin-bottom:20px;display:block;width:100%'
  container.appendChild(startBtn)
  const controlsDiv = document.createElement('div')
  controlsDiv.id = 'controls'
  controlsDiv.style.cssText = 'display:none'
  const channelHeaders = ['Revenue', 'ErrorRate', 'ActiveUsers', 'Events', 'AmbientDrone']
  channelHeaders.forEach(label => {
    const ch = channels[label]
    if (!ch) return
    const row = document.createElement('div')
    row.style.cssText = 'background:#16213e;padding:10px 12px;margin-bottom:8px;border-left:3px solid ' + ch.color
    const header = document.createElement('div')
    header.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'
    const name = document.createElement('span')
    name.textContent = label.toUpperCase()
    name.style.cssText = 'font-size:12px;font-weight:bold;color:' + ch.color
    header.appendChild(name)
    const indicator = document.createElement('span')
    indicator.id = 'indicator_' + label
    indicator.textContent = 'ACTIVE'
    indicator.style.cssText = 'font-size:9px;color:#27ae60'
    header.appendChild(indicator)
    row.appendChild(header)
    const controlsRow = document.createElement('div')
    controlsRow.style.cssText = 'display:flex;gap:8px;align-items:center'
    const muteBtn = document.createElement('button')
    muteBtn.textContent = 'M'
    muteBtn.style.cssText = 'background:#333;color:#fff;border:1px solid #555;padding:4px 10px;font-family:monospace;font-size:11px;cursor:pointer'
    muteBtn.onclick = function() {
      ch.toggleMute()
      muteBtn.style.background = ch.muted ? '#c0392b' : '#333'
      indicator.textContent = ch.muted ? 'MUTED' : 'ACTIVE'
      indicator.style.color = ch.muted ? '#e74c3c' : '#27ae60'
    }
    controlsRow.appendChild(muteBtn)
    const soloBtn = document.createElement('button')
    soloBtn.textContent = 'S'
    soloBtn.style.cssText = 'background:#333;color:#fff;border:1px solid #555;padding:4px 10px;font-family:monospace;font-size:11px;cursor:pointer'
    soloBtn.onclick = function() {
      ch.toggleSolo()
      soloBtn.style.background = ch.soloed ? '#f39c12' : '#333'
      indicator.textContent = soloActive ? (ch.soloed ? 'SOLO' : 'OFF') : (ch.muted ? 'MUTED' : 'ACTIVE')
      indicator.style.color = ch.soloed ? '#f39c12' : (ch.muted ? '#e74c3c' : '#27ae60')
      channelHeaders.forEach(lbl => {
        const c = channels[lbl]
        if (!c) return
        const ind = document.getElementById('indicator_' + lbl)
        if (ind) {
          ind.textContent = soloActive ? (c.soloed ? 'SOLO' : 'OFF') : (c.muted ? 'MUTED' : 'ACTIVE')
          ind.style.color = c.soloed ? '#f39c12' : (c.muted ? '#e74c3c' : '#27ae60')
        }
      })
    }
    controlsRow.appendChild(soloBtn)
    const volSlider = document.createElement('input')
    volSlider.type = 'range'
    volSlider.min = 0
    volSlider.max = 100
    volSlider.value = 50
    volSlider.style.cssText = 'flex:1;height:4px;accent-color:' + ch.color
    volSlider.oninput = function() {
      ch.setVolume(this.value / 100)
    }
    controlsRow.appendChild(volSlider)
    const volLabel = document.createElement('span')
    volLabel.textContent = '50%'
    volLabel.style.cssText = 'font-size:10px;width:32px;text-align:right'
    volSlider.oninput = function() {
      ch.setVolume(this.value / 100)
      volLabel.textContent = this.value + '%'
    }
    controlsRow.appendChild(volLabel)
    row.appendChild(controlsRow)
    controlsDiv.appendChild(row)
  })
  const headphoneRow = document.createElement('div')
  headphoneRow.style.cssText = 'background:#16213e;padding:10px 12px;margin-top:12px;display:flex;align-items:center;gap:10px'
  const hpLabel = document.createElement('span')
  hpLabel.textContent = 'HEADPHONE MODE'
  hpLabel.style.cssText = 'font-size:11px;font-weight:bold'
  headphoneRow.appendChild(hpLabel)
  const hpToggle = document.createElement('input')
  hpToggle.type = 'checkbox'
  hpToggle.onchange = function() {
    masterGain.gain.setTargetAtTime(this.checked ? 1.0 : 0.7, AudioContext.currentTime, 0.1)
    console.log('HEADPHONE_MODE:' + (this.checked ? 'ON' : 'OFF') + ' at t=' + AudioContext.currentTime.toFixed(3))
  }
  headphoneRow.appendChild(hpToggle)
  controlsDiv.appendChild(headphoneRow)
  const simRow = document.createElement('div')
  simRow.style.cssText = 'background:#16213e;padding:10px 12px;margin-top:12px'
  const simLabel = document.createElement('div')
  simLabel.textContent = 'SIMULATION CONTROLS'
  simLabel.style.cssText = 'font-size:11px;font-weight:bold;color:#ff6b6b;margin-bottom:8px'
  simRow.appendChild(simLabel)
  const sliderConfig = [
    { label: 'Revenue', key: 'revenue', min: 0, max: 100, color: '#27ae60' },
    { label: 'Error Rate', key: 'errorRate', min: 0, max: 100, color: '#e74c3c' },
    { label: 'Active Users', key: 'activeUsers', min: 0, max: 1000, color: '#3498db' },
    { label: 'Uptime', key: 'uptime', min: 90, max: 100, color: '#9b59b6' }
  ]
  sliderConfig.forEach(cfg => {
    const row = document.createElement('div')
    row.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:4px'
    const lbl = document.createElement('span')
    lbl.textContent = cfg.label
    lbl.style.cssText = 'font-size:10px;width:80px;color:' + cfg.color
    row.appendChild(lbl)
    const slider = document.createElement('input')
    slider.type = 'range'
    slider.min = cfg.min
    slider.max = cfg.max
    slider.value = dummyData[cfg.key]
    slider.style.cssText = 'flex:1;height:3px'
    const val = document.createElement('span')
    val.textContent = dummyData[cfg.key]
    val.style.cssText = 'font-size:10px;width:35px;text-align:right'
    slider.oninput = function() {
      dummyData[cfg.key] = parseFloat(this.value)
      val.textContent = this.value
    }
    row.appendChild(slider)
    row.appendChild(val)
    simRow.appendChild(row)
  })
  const simBtnRow = document.createElement('div')
  simBtnRow.style.cssText = 'display:flex;gap:8px;margin-top:8px'
  const updateBtn = document.createElement('button')
  updateBtn.textContent = '> UPDATE'
  updateBtn.style.cssText = 'background:#27ae60;color:#fff;border:none;padding:6px 16px;font-family:monospace;font-size:11px;cursor:pointer'
  updateBtn.onclick = function() {
    updateSonification(dummyData)
    document.getElementById('healthDisplay').textContent = healthScore.toFixed(1)
  }
  simBtnRow.appendChild(updateBtn)
  const autoBtn = document.createElement('button')
  autoBtn.textContent = '> AUTO SIM'
  autoBtn.style.cssText = 'background:#3498db;color:#fff;border:none;padding:6px 16px;font-family:monospace;font-size:11px;cursor:pointer'
  let autoInterval = null
  autoBtn.onclick = function() {
    if (autoInterval) {
      clearInterval(autoInterval)
      autoInterval = null
      autoBtn.textContent = '> AUTO SIM'
      autoBtn.style.background = '#3498db'
      return
    }
    autoBtn.textContent = 'STOP AUTO'
    autoBtn.style.background = '#e74c3c'
    autoInterval = setInterval(function() {
      dummyData.revenue = Math.max(0, Math.min(100, dummyData.revenue + (Math.random() - 0.5) * 10))
      dummyData.errorRate = Math.max(0, Math.min(100, dummyData.errorRate + (Math.random() - 0.5) * 5))
      dummyData.activeUsers = Math.max(0, Math.min(1000, dummyData.activeUsers + (Math.random() - 0.5) * 30))
      dummyData.uptime = Math.max(90, Math.min(100, dummyData.uptime + (Math.random() - 0.5) * 0.5))
      updateSonification(dummyData)
      document.getElementById('healthDisplay').textContent = healthScore.toFixed(1)
      ;[].forEach.call(document.querySelectorAll('#controls input[type=range]'), function(sl, i) {
        if (sliderConfig[i]) sl.value = dummyData[sliderConfig[i].key]
      })
    }, 3000)
  }
  simBtnRow.appendChild(autoBtn)
  simRow.appendChild(simBtnRow)
  controlsDiv.appendChild(simRow)
  const testRow = document.createElement('div')
  testRow.style.cssText = 'background:#16213e;padding:10px 12px;margin-top:12px'
  const testLabel = document.createElement('div')
  testLabel.textContent = 'VERIFICATION TESTS'
  testLabel.style.cssText = 'font-size:11px;font-weight:bold;color:#f39c12;margin-bottom:8px'
  testRow.appendChild(testLabel)
  const testBtn = document.createElement('button')
  testBtn.textContent = '> RUN MUTE/SOLO INVARIANT TEST'
  testBtn.style.cssText = 'background:#f39c12;color:#000;border:none;padding:6px 12px;font-family:monospace;font-size:10px;cursor:pointer;margin-right:6px'
  testBtn.onclick = function() {
    runMuteSoloInvariantTest()
  }
  testRow.appendChild(testBtn)
  const testBtn2 = document.createElement('button')
  testBtn2.textContent = '> RUN AUDIO GRAPH TEST'
  testBtn2.style.cssText = 'background:#9b59b6;color:#fff;border:none;padding:6px 12px;font-family:monospace;font-size:10px;cursor:pointer'
  testBtn2.onclick = function() {
    runAudioGraphTest()
  }
  testRow.appendChild(testBtn2)
  controlsDiv.appendChild(testRow)
  container.appendChild(controlsDiv)
  document.body.appendChild(container)
  startBtn.onclick = function() {
    if (AudioContext.state === 'suspended') AudioContext.resume()
    document.getElementById('controls').style.display = 'block'
    document.getElementById('audioStatus').textContent = 'RUNNING'
    document.getElementById('audioStatus').style.color = '#27ae60'
    startBtn.style.display = 'none'
    console.log('AUDIO_STARTED:' + AudioContext.state + ' sampleRate=' + AudioContext.sampleRate + ' at t=' + AudioContext.currentTime.toFixed(3))
    initChannels()
    updateSonification(dummyData)
    document.getElementById('healthDisplay').textContent = healthScore.toFixed(1)
  }
}
function runMuteSoloInvariantTest() {
  console.log('TEST:muteSoloInvariant START at t=' + AudioContext.currentTime.toFixed(3))
  const revCh = channels['Revenue']
  const errCh = channels['ErrorRate']
  const userCh = channels['ActiveUsers']
  revCh.muted = false
  revCh.soloed = false
  errCh.muted = false
  errCh.soloed = false
  userCh.muted = false
  userCh.soloed = false
  soloActive = false
  revCh.applyMuteSolo()
  errCh.applyMuteSolo()
  userCh.applyMuteSolo()
  console.log('TEST:all channels active, gains should be volume')
  console.log('TEST:Revenue gain target=' + revCh.gain.gain.value.toFixed(4))
  console.log('TEST:ErrorRate gain target=' + errCh.gain.gain.value.toFixed(4))
  console.log('TEST:ActiveUsers gain target=' + userCh.gain.gain.value.toFixed(4))
  revCh.soloed = true
  revCh.toggleSolo()
  console.log('TEST:solo on Revenue, others should be 0')
  console.log('TEST:Revenue gain target=' + revCh.gain.gain.value.toFixed(4) + ' expected nonzero')
  console.log('TEST:ErrorRate gain target=' + errCh.gain.gain.value.toFixed(4) + ' expected ~0')
  console.log('TEST:ActiveUsers gain target=' + userCh.gain.gain.value.toFixed(4) + ' expected ~0')
  errCh.muted = true
  errCh.applyMuteSolo()
  console.log('TEST:mute ErrorRate while Revenue soloed')
  console.log('TEST:ErrorRate gain target=' + errCh.gain.gain.value.toFixed(4) + ' expected ~0')
  revCh.soloed = false
  revCh.toggleSolo()
  console.log('TEST:no solo, all should return to normal')
  console.log('TEST:Revenue gain target=' + revCh.gain.gain.value.toFixed(4))
  console.log('TEST:ActiveUsers gain target=' + userCh.gain.gain.value.toFixed(4))
  errCh.muted = false
  errCh.applyMuteSolo()
  errCh.toggleSolo()
  errCh.soloed = true
  errCh.toggleSolo()
  console.log('TEST:solo on ErrorRate, muted channels unaffected')
  console.log('TEST:ErrorRate gain target=' + errCh.gain.gain.value.toFixed(4) + ' expected ~0 (muted)')
  console.log('TEST:soloActive=' + soloActive)
  errCh.soloed = false
  errCh.toggleSolo()
  console.log('TEST:muteSoloInvariant COMPLETE at t=' + AudioContext.currentTime.toFixed(3))
}
function runAudioGraphTest() {
  console.log('TEST:audioGraph START at t=' + AudioContext.currentTime.toFixed(3))
  console.log('TEST:AudioContext state=' + AudioContext.state + ' sampleRate=' + AudioContext.sampleRate)
  console.log('TEST:masterGain gain=' + masterGain.gain.value)
  console.log('TEST:channels count=' + Object.keys(channels).length)
  for (const key in channels) {
    const ch = channels[key]
    console.log('TEST:channel[' + key + '] gain=' + ch.gain.gain.value.toFixed(4) + ' pan=' + ch.panner.pan.value.toFixed(2) + ' muted=' + ch.muted + ' soloed=' + ch.soloed + ' nodes=' + ch.nodes.length)
    const dest = ch.panner
    const destNode = dest ? dest.constructor.name : 'null'
    console.log('TEST:channel[' + key + '] panner.destination=' + destNode)
  }
  console.log('TEST:audioGraph COMPLETE at t=' + AudioContext.currentTime.toFixed(3))
}
window.onload = buildUI