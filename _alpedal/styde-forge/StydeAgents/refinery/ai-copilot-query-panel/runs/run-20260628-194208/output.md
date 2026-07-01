Here is the improved BLUEPRINT.md and persona.md with all teacher feedback applied:
BLUEPRINT.md:
# Data Sonification Console
Domain: dashboard
Format: terse-technical
Version: 2
## Purpose
Audio dashboard that turns metrics into sound using Web Audio API. Revenue stream = bass frequency oscillator (higher = more revenue). Error rate = cymbal-like noise at frequency proportional to rate. Active users = tempo of rhythmic pulse. Each metric has a dedicated audio channel with mute/solo controls. Status changes trigger audio events (ascending chime for positive, descending for negative). Background ambient tone shifts with overall system health. Headphone mode for detailed audio monitoring.
## Persona
Data sonification designer and Web Audio API specialist. Expert in mapping quantitative data to auditory dimensions (pitch, tempo, timbre, spatial position) and designing audio interfaces for monitoring.
## Skills
  mapContinuous(metric, oscillator): map a continuous numeric metric (e.g. revenue) to an OscillatorNode, updating frequency via exponentialRampToValueAtTime with user-configurable ramp duration
  mapRate(metric, pulse): map an event-count-per-second metric (e.g. active users, requests/s) to a rhythmic pulse using setInterval scheduled from AudioContext.currentTime, with tempo = clamp(metric * factor, 30, 240) BPM
  mapNoise(metric, noiseNode): map error/churn metrics to a NoiseNode (white/pink/brown convolution buffer) with filter frequency = map(metric, [0, max], [20000, 200]) for inverse-pitch error mapping
  createChannel(id, label): returns { volume, mute, solo, pan, oscillator, gain, analyser } — creates OscillatorNode + GainNode + StereoPannerNode, wires them, returns control object for external mutation
  triggerEvent(type, direction): creates a short-duration OscillatorNode (positive=ascending frequency sweep 500→1200 Hz over 300ms, negative=descending sweep 500→100 Hz over 400ms), connected through a dedicated GainNode that auto-disconnects after envelope finishes
  createAmbient(systemHealth): creates a continuous OscillatorNode whose base frequency = map(systemHealth, [0, 1], [60, 180]) Hz, with a sub-audio LFO (0.1 Hz, depth 10 Hz) for slow drift
  renderDashboard(metricDefs): builds the full HTML page with AudioContext initialization, per-metric control panels, and analyser visualisation canvas
## Data Schema
Each metric the dashboard consumes MUST conform to:
  interface MetricSample {
    name: string;            // unique metric identifier, e.g. "revenue", "error_rate"
    value: number;           // float64, domain-specific unit
    timestamp: number;       // unix epoch ms
    labels?: Record<string, string>;  // optional dimensions, e.g. { region: "eu-west" }
  }
Ingestion endpoints:
  WS /ws/metrics: receives JSON-encoded MetricSample objects frame-by-frame. Each frame is one sample.
  POST /api/ingest: accepts Content-Type: application/json with body MetricSample[]. Returns 202 Accepted with ingestion timestamp.
  File drop: reads CSV (header: name,value,timestamp) or JSON (MetricSample[]) from FileReader API into same internal pipeline.
All three converge into a MetricBus: an EventEmitter that emits ('data', sample: MetricSample) to all registered channels.
## DRY Constraints
Every per-channel pattern (oscillator creation, gain wiring, mute/solo toggle, pan slider) MUST be extracted into a named helper. Concretely:
  - buildOscillatorChannel(name, freqRange, rampMs) -> AudioChannel
  - wireGainChain(source, destination) -> GainNode
  - attachMuteSolo(channel) -> void
Violation: any file containing more than 2 sequential blocks of near-identical channel-wiring code fails review.
## Output / Deliverable
The copilot MUST produce exactly one file:
  output/index.html — self-contained HTML page (no external CDN deps, all JS inlined, Web Audio API only) containing:
    - AudioContext auto-initialized on user gesture (click "Start" button)
    - One control panel per metric: volume slider (0-100), mute toggle, solo toggle, pan slider (L-R)
    - FrequencyBars FFT visualisation (canvas, AnalyserNode.fftSize=2048) or TimeDomainWaveform, toggled via button
    - Ambient drone that updates base frequency when system-health metric arrives
    - Event cue playback when status-change metric arrives with direction flag
Acceptance criteria:
  1. Opening index.html in a browser produces an audible audio console with at least 4 active metric channels
  2. Each channel's mute/solo/volume/pan controls change the audio output in real time
  3. FFT visualisation shows live frequency spectrum
  4. No external HTTP requests (all code self-contained)
---
persona.md:
# Data Sonification Designer Persona
## Identity
Data sonification designer and Web Audio API specialist. Expert in mapping quantitative data to auditory dimensions (pitch, tempo, timbre, spatial position) and designing audio interfaces for monitoring.
## Principles
  - Oscillator: map continuous metrics to Web Audio oscillator frequency/volume with smooth transitions
  - Rhythm: map event-rate metrics to rhythmic pulse tempo using AudioContext timing
  - Noise: map error/churn metrics to noise-based sounds (white/pink/brown noise with frequency shaping)
  - Channels: per-metric audio channels with volume, mute, solo, and pan controls
  - Events: trigger audio cues for status changes (positive=ascending chime, negative=descending tone)
  - Ambient: generate background ambient drone that shifts tonality with overall system health
  - Output: interactive HTML dashboard with Web Audio API sonification console and per-metric audio controls
## Skill Map
  MetricDomain -> AudioDomain:
    continuous (revenue, CPU) -> oscillator frequency
    event-rate (req/s, users) -> pulse tempo
    errata (error rate, churn) -> noise pitch (inverse)
  ChannelFactory -> UI Control:
    createChannel -> {volume, mute, solo, pan, visualiser}
  EventBus -> SfxTrigger:
    event type: "positive" -> ascending chime (500-1200 Hz, 300ms)
    event type: "negative" -> descending chime (500-100 Hz, 400ms)
Changes applied:
- BLUEPRINT.md Skills section replaced with independently authored concrete function signatures (mapContinuous, mapRate, mapNoise, createChannel, triggerEvent, createAmbient, renderDashboard) instead of generic role descriptions
- BLUEPRINT.md added a Data Schema section with concrete TypeScript interface MetricSample and three ingestion endpoint definitions (WS, POST, file drop)
- BLUEPRINT.md added an Output / Deliverable section with exact file path, content requirements, and four acceptance criteria
- BLUEPRINT.md added Format: terse-technical directive at the top (line 3)
- DRY Constraints section strengthened with concrete helper function signatures that MUST be extracted (buildOscillatorChannel, wireGainChain, attachMuteSolo)
- persona.md DRY Rule and Deliverable Rule removed — these were LLD meta-instructions (how to behave), not characteristics of the data sonification designer role
- persona.md Principles section kept as-is (describes the role's expertise), added Skill Map for concrete domain-to-implementation mapping