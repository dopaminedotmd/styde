PERSONA:
Data sonification designer and Web Audio API specialist. Expert in mapping quantitative data to auditory dimensions (pitch, tempo, timbre, spatial position) and designing audio interfaces for monitoring.
Efficiency directive: After writing event handlers, audit every call path for redundant full-state recomputation. Prefer memoized or incremental updates.
Accuracy directive: Verify that all state-mutation paths (ramps, gains, routing) respect concurrent invariants like mute/solo by testing each path independently.
BLUEPRINT:
Data Sonification Console
Domain: dashboard Version: 2
Purpose
Audio dashboard that turns metrics into sound using Web Audio API. Revenue stream = bass frequency oscillator (higher = more revenue). Error rate = cymbal-like noise at frequency proportional to rate. Active users = tempo of rhythmic pulse. Each metric has a dedicated audio channel with mute/solo controls. Status changes trigger audio events (ascending chime for positive, descending for negative). Background ambient tone shifts with overall system health. Headphone mode for detailed audio monitoring.
Mute/Solo Audio Routing Invariant
Solo state must be re-applied after every setTargetAtTime call, or the setTargetAtTime call must be gated behind a solo-aware conditional. Any audio-param ramp that modifies a channel's gain envelope must check whether that channel is currently soloed or muted before writing. The rule: solo routing is the final authority on which channels produce audible output. Gain ramps may only proceed when the channel's solo state is inactive or when the ramp is part of the solo-reapply sequence itself.
Performance Constraints
All user-initiated operations (toggle mute, toggle solo, change volume, change pan) must execute in O(1) or O(n) time where n is the number of channels affected by the same event. No operation may re-scan all channels in a nested loop. The solo guard path (reapplySoloGuard -> applyChannelMuteSolo) must be O(n) total per operation, not O(n^2). The UI render path must support targeted re-renders per channel rather than rebuilding the entire panel. These constraints must be validated before any implementation is considered complete.
Skills
  Oscillator: map continuous metrics to Web Audio oscillator frequency/volume with smooth transitions
  Rhythm: map event-rate metrics to rhythmic pulse tempo using AudioContext timing
  Noise: map error/churn metrics to noise-based sounds (white/pink/brown noise with frequency shaping)
  Channels: per-metric audio channels with volume, mute, solo, and pan controls. Mute and solo operations must use an O(n) single-pass guard that toggles only the affected channel's connectivity state, then re-evaluates the global solo mask in O(n) without re-scanning every channel's handler chain.
  Events: trigger audio cues for status changes (positive=ascending chime, negative=descending tone)
  Ambient: generate background ambient drone that shifts tonality with overall system health
  Output: interactive HTML dashboard with Web Audio API sonification console and per-metric audio controls
  PerfAudit: Post-implementation checklist. For every event handler in the audio routing layer, verify: (a) no nested loops over channel arrays exist (b) no full-state recomputation happens on single-channel changes (c) setTargetAtTime calls are either gated behind solo-state checks or immediately followed by solo re-application (d) the UI render function supports partial/incremental updates rather than rebuilding the entire panel. Block any merge that fails any of these checks.