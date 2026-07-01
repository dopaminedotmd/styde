Formula reference table replaces inline sections. Worked examples expanded with step-by-step formula application. Meta-evaluation YAML: none embedded in current BLUEPRINT.md — schema lives in the evaluation pipeline (teacher_output.yaml), not in the blueprint. No extraction needed.
skills/data-sonification.md: created at E:\Stryde\_alpedal\styde-forge\skills\data-sonification.md
config.yaml: created at E:\Stryde\_alpedal\styde-forge\config.yaml
---
BLUEPRINT.md changes:
section: Frequency Mapping Formulas (lines 99-138)
replace: 3 individual formula sections
with: single terse reference table + constraint block
formula-type: linear-slope
mapping: oscillator channels (continuous metrics)
formula: f(v) = f_low + ((v - min) / (max - min)) * (f_high - f_low)
range: f_low >= 55, f_high <= 2200, span >= 200
ramp: timeConstant <= 0.15
formula-type: exponential-slope
mapping: rhythm tempo channels (event rate)
formula: bpm(r) = bpm_low * (bpm_high / bpm_low) ^ ((r - r_min) / (r_max - r_min))
range: bpm_low >= 30, bpm_high <= 240
clamp: r < r_min -> bpm_low, r > r_max -> bpm_high
timing: interval = 60 / bpm(r), lookahead scheduling via currentTime
formula-type: power-law-noise
mapping: error/churn channels
formula: N(e) = N_low + ((e - e_min) / (e_max - e_min))^gamma * (N_high - N_low)
gamma: 0.5 (square-root curve: sensitive at low rates, compressive at high)
range: N_low >= 80, N_high <= 4000
noise-type: white at N <= 200, pink at 200 < N <= 1000, brown at N > 1000
formula-type: summation-constraint
mapping: all channels (clipping prevention)
rule: total peak gain <= 1.0 (0 dBFS)
impl: MasterLimiterNode(threshold -0.5 dB, attack 0.003 s, release 0.050 s)
auto-scale: if RMS > 0.8 over 1s window, scale = 0.8 / currentMasterRms; restore when RMS < 0.6
section: Worked Examples — append formula-reference column to each example
example-1 (Mute-Group Toggle): applies mute/unmute gain logic, no formula involved
example-2 (Solo-Exclusive Flip): applies solo-count + mute-group logic, no formula involved
example-3 (Frequency-Split Merge): applies linear-slope formula to each band:
  bass-gain = 0 + ((80 - 0) / (100 - 0)) * 1.0 = 0.8
  mid-gain  = 0 + ((65 - 0) / (100 - 0)) * 1.0 = 0.65
  treble-gain = 0 + ((30 - 0) / (100 - 0)) * 1.0 = 0.3
  sum = 1.75 > 1.0 -> apply summation-constraint: scale = 1.0 / 1.75 = 0.571
  final: bass 0.457, mid 0.371, treble 0.171
No other structural change to BLUEPRINT.md — efficiency constraints already present at lines 37-49 (rules 1-7). Meta-evaluation schema not present in blueprint; no extraction needed.
---
skills/data-sonification.md:
Performance Patterns
1. Oscillator pooling via AudioNode graph pre-wiring
  DO NOT create/call new OscillatorNode() or audioCtx.createOscillator() inside
  the per-tick rhythm handler. Pre-wire at init:
    const pool = [];
    for (let i = 0; i < CHANNEL_COUNT; i++) {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      gain.gain.value = 0;
      osc.connect(gain);
      gain.connect(masterBus);
      osc.start(); // start once, keep running
      pool.push({ osc, gain, frequency: 220, active: false });
    }
  On each tick: set pool[channel].osc.frequency.setTargetAtTime(newFreq, now, 0.05);
  set pool[channel].gain.gain.setTargetAtTime(newVolume, now, 0.02);
  To mute/silence: set gain to 0 instead of stopping the oscillator.
  Never disconnect/reconnect the node.
  Benefit: zero GC pressure from AudioNode allocation. Audio thread sees stable
  graph topology. Browsers batch parameter automation in the render quantum.
2. DOM update via textContent on pre-queried refs
  Query all metric-display elements once during dashboard init and store references
  in a Map<channelId, { valueEl, labelEl, statusEl }>. On metric update:
    refs.get(channelId).valueEl.textContent = formattedValue;
  Never use innerHTML anywhere in the hot path (any handler called > 1 Hz).
  Never re-query document.getElementById inside the tick handler — the lookup
  defeats the purpose of avoiding innerHTML.
  template:
    const metricRefs = new Map();
    function initMetricRefs() {
      for (const ch of channels) {
        metricRefs.set(ch.id, {
          valueEl: document.getElementById(`metric-${ch.id}-value`),
          labelEl: document.getElementById(`metric-${ch.id}-label`),
          statusEl: document.getElementById(`metric-${ch.id}-status`),
        });
      }
    }
    function updateMetricUI(channelId, value, status) {
      const ref = metricRefs.get(channelId);
      if (!ref) return;
      ref.valueEl.textContent = value.toFixed(1);
      ref.statusEl.textContent = status;
      ref.statusEl.className = status === 'ok' ? 'status-ok' : 'status-warn';
    }
3. requestAnimationFrame throttling for waveform visualisation
  When rendering AnalyserNode data to canvas:
    let rafId = null;
    function drawWaveform() {
      rafId = requestAnimationFrame(drawWaveform);
      const data = new Uint8Array(analyser.fftSize);
      analyser.getByteTimeDomainData(data);
      // draw to canvas
    }
    function startVisualisation() { if (!rafId) drawWaveform(); }
    function stopVisualisation() {
      if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
    }
  Never use setInterval or setTimeout for visualisation rendering. rAF
  auto-pauses when tab is hidden, saving CPU. Throttle analysis reads:
  if the canvas is scrolled out of view or hidden, stop the rAF loop.
  Dispose the AnalyserNode when no visualisation is active — disconnect
  from the output chain and null the reference.
---
config.yaml:
forge:
  scoring:
    dimensions:
      accuracy:
        weight: 1.0
      completeness:
        weight: 1.0
      clarity:
        weight: 1.0
      efficiency:
        weight: 1.0
      usefulness:
        weight: 1.0
    composite:
      formula: "(accuracy + completeness + clarity + efficiency + usefulness) / 5"
      gate:
        quality: 80
        production: 85
  description: "Efficiency weight raised to 1.0 (parity with all other dimensions).
    Previous weight was 0.5 — under-weighted efficiency masked oscillator churn and
    innerHTML penalties. All five dimensions now contribute equally to composite."