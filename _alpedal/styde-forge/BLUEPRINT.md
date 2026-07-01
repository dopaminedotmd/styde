# Data Sonification Console

Domain: dashboard
Version: 1

ARTIFACT-FIRST GATE — MUST produce working files (HTML/CSS/JS) as primary output. Never output a specification document or design plan. If context or constraints are missing, produce best-effort files and note assumptions inline rather than falling back to a spec. This blueprint exists only to guide artifact creation; the artifact is the deliverable.

## Purpose

Audio dashboard that turns metrics into sound using Web Audio API. Revenue stream = bass frequency oscillator (higher = more revenue). Error rate = cymbal-like noise at frequency proportional to rate. Active users = tempo of rhythmic pulse. Each metric has a dedicated audio channel with mute/solo controls. Status changes trigger audio events (ascending chime for positive, descending for negative). Background ambient tone shifts with overall system health. Headphone mode for detailed audio monitoring.

## Persona

Data sonification designer and Web Audio API specialist. Expert in mapping quantitative data to auditory dimensions (pitch, tempo, timbre, spatial position) and designing audio interfaces for monitoring.

## Skills

  Oscillator: map continuous metrics to Web Audio oscillator frequency/volume with smooth transitions
  Rhythm: map event-rate metrics to rhythmic pulse tempo using AudioContext timing
  Noise: map error/churn metrics to noise-based sounds (white/pink/brown noise with frequency shaping)
  Channels: per-metric audio channels with volume, mute, solo, and pan controls
  Events: trigger audio cues for status changes (positive=ascending chime, negative=descending tone)
  Ambient: generate background ambient drone that shifts tonality with overall system health
  Output: interactive HTML dashboard with Web Audio API sonification console and per-metric audio controls

## Mute/Solo Audio Routing Invariant

Solo state MUST be re-applied after every setTargetAtTime call on any gain node. Alternatively, gate the setTargetAtTime call behind a solo-aware conditional that checks the target channel's solo state and the global solo count before mutating the gain envelope.

Rationale: setTargetAtTime schedules an automated ramp on the audio thread that overrides any immediate gain.value assignment from mute/solo routing if the ramp target !== 0. Without explicit re-application, muting a channel that was previously ramped up will leave audible output.

Implementation:

  1. Define a function applyChannelMuteSolo(channelId) that reads the channel's mute/solo state
  2. If any channel has solo=true, mute ALL non-soloed channels by setting their gain.value=0
  3. After every setTargetAtTime call, schedule a follow-up automation that reapplies step 2 (or make setTargetAtTime conditional on the channel not being muted/soloed-out)
  4. Recommendation: wrap setTargetAtTime in a helper that accepts (gainNode, targetValue, rampDuration, channelId) and internally calls applyChannelMuteSolo after scheduling

## Performance Constraints

All per-user-action code paths MUST complete in O(1) or O(n) where n = number of audio channels (typically <= 8). Never O(n^2) or worse.

Specifically:

  1. Solo reapplication: toggleSolo must NOT re-scan all channels redundantly. Use a global solo-count tracker: increment on solo-on, decrement on solo-off. If soloCount > 0, mute all non-soloed channels by setting gain to 0 in a single loop; if soloCount === 0, unmute all. O(n) total, never O(n^2).
  2. UI rendering: buildUI must support targeted re-renders per channel (e.g., update only the channel panel whose state changed) rather than rebuilding the entire DOM tree on every state change. Use component-level DOM references or a virtual-DOM diff.
  3. Audio parameter automation: batch consecutive setValueAtTime / setTargetAtTime calls on the same AudioParam into a single scheduling call where possible.
  4. Ingestion: the MetricBus must present the latest value per metric in O(1) lookups. No iterating over all metrics to find one channel's value.
  5. No disposable AudioNode creation per tick in rhythm channels. Pre-wire an OscillatorNode graph with silent scheduling and toggle frequency/start-stop instead of allocating a new AudioNode per pulse.
  6. Metric DOM updates must use textContent or replaceChildren on pre-queried element references. innerHTML is forbidden in hot paths (any handler called more than once per second).
  7. Analyser node must exist only when at least one visualisation is active. Dispose the analyser and disconnect it from the output chain when all visualisations are hidden or closed.

## DRY Constraints

All repeated per-channel logic MUST be extracted into a helper function or loop rather than inlined 8 times. This includes:

  - Oscillator creation and frequency/volume ramping
  - Gain node wiring (createGain -> connect -> destination)
  - Preset value assignment (frequency range, ramp duration, initial volume)
  - Mute/solo toggle wiring

Violation: any file containing more than 2 sequential blocks of near-identical channel-wiring code fails review.

## Data Ingestion

External data sources MUST use one of the following concrete ingestion paths:

  - WebSocket endpoint (ws://host:port/metrics-stream) for real-time streaming data
  - POST endpoint (POST http://host:port/api/ingest) for batch/event-driven data
  - File-drop handler (drag-and-drop CSV/JSON file onto the dashboard) for offline/development data

All three paths converge into a single internal MetricBus that feeds all audio channels.

## Visualisation

Wire the analyser node into a concrete visualisation. One of:

  - FrequencyBars: real-time FFT-based bar chart (canvas or WebGL) showing frequency spectrum of the combined audio output
  - TimeDomainWaveform: real-time oscilloscope-style waveform display
  - Both, toggled via a UI button

If neither is wired, remove the analyser node entirely. Dead nodes that consume CPU but produce no output are not allowed.

## Accessibility Checklist

All interactive elements (buttons, toggles, sliders, channel panels, mute/solo controls, visualisation switchers, file-drop zones) MUST include:

  - aria-label describing the element's function (e.g., aria-label="Mute revenue channel")
  - role attribute matching the element's interactive purpose (role="switch" for mute/solo toggles, role="slider" for volume sliders, role="button" for clickable controls)
  - visible focus indicator on keyboard focus (outline: 2px solid or equivalent, never outline: none)
  - full keyboard navigation: Tab to move between controls, Enter/Space to activate toggles and buttons, Arrow keys for sliders and pan controls
  - aria-pressed or aria-checked reflecting current state on toggle and switch elements
  - aria-live="polite" region for announcements of metric changes, audio state transitions, and error conditions

Cards and channel panels MUST use semantic HTML: <article> for standalone channel panels with <h2> or <h3> headings for the channel name, <section> for grouped content regions.

File-drop zones MUST include an accessible method (hidden <input type="file"> with explicit label) as an alternative to drag-and-drop.

## Implementation Guidance

### Edge Cases & Error Recovery

AudioContext lifecycle:
  1. Create AudioContext on first user gesture only — never on page load
  2. Resume suspended context via ctx.resume() on click/tap. Handle promise rejection if browser blocks autoplay
  3. State transitions: 'suspended' -> show "tap to enable audio" overlay; 'closed' -> create fresh context; 'running' -> normal operation
  4. AudioContext unavailable: run in silent mode with visual indicator. Never throw or blank the dashboard

Unsupported codecs:
  1. Wrap decodeAudioData in try/catch
  2. On decode failure, fall back to oscillator-based synthesis for that sound
  3. Report fallback count to a diagnostic panel visible in the UI

DELIVERABLE VERIFICATION GATE — agent MUST list the absolute paths of every file it created (e.g., /path/to/index.html, /path/to/script.js). If no files were produced, the gate fails and the agent must produce files before marking done. Each file must be verified: check that its size > 0 bytes, that referenced assets exist or are inlined, and that opening the HTML in a browser produces a working dashboard (no blank page, no console errors from missing dependencies).

## Frequency Mapping Formulas

All metric-to-audio mappings MUST use one of the following three mapping functions, selected by metric type. No hardcoded frequency ranges outside these formulas.

### Linear Slope Mapping (oscillator channels)

  Given metric value v, metric range [min, max], audio range [f_low, f_high]:
    f(v) = f_low + ((v - min) / (max - min)) * (f_high - f_low)

  Constraints:
    f_low >= 55 (fundamental bass floor)
    f_high <= 2200 (avoid piercing treble in continuous tones)
    f_high - f_low >= 200 (perceptible span)
    RampRate <= 0.15 (slew limiting via setTargetAtTime timeConstant)

### Exponential Slope Mapping (rhythm tempo channels)

  Given event rate r, rate range [r_min, r_max], tempo range [bpm_low, bpm_high]:
    bpm(r) = bpm_low * (bpm_high / bpm_low) ^ ((r - r_min) / (r_max - r_min))

  Constraints:
    bpm_low >= 30, bpm_high <= 240
    If r < r_min: clamp to bpm_low. If r > r_max: clamp to bpm_high.
    Interval between pulses = (60 / bpm(r)) seconds, scheduled via AudioContext.currentTime + lookahead.

### Power-Law Noise Mapping (error/churn channels)

  Given error rate e, error range [e_min, e_max], noise frequency range [N_low, N_high]:
    N(e) = N_low + ((e - e_min) / (e_max - e_min))^gamma * (N_high - N_low)

  Constraints:
    gamma = 0.5 (square-root curve: sensitive to low rates, compressive at high rates)
    N_low >= 80, N_high <= 4000
    Noise type must transition: white noise at N <= 200, pink noise at 200 < N <= 1000, brown noise at N > 1000.

### Summation Constraint

  Total peak gain across all active channels MUST NOT exceed 1.0 (0 dBFS) to prevent clipping.
  Implement via a MasterLimiter node (threshold -0.5 dB, attack 0.003 s, release 0.050 s) on the final output bus.
  Per-channel gain reduction: if master gain > 0.8 RMS over 1 second window, apply a linear scale factor = 0.8 / currentMasterRms to all channel gain values. Restore when RMS drops below 0.6.

## Headphone Mode Routing

When headphone mode is active (toggled via UI or MIDI key), the following routing rules apply:

  Rule 1. Panner automation is enabled on every channel's StereoPannerNode. Pan values map to headphone stereo position directly.
  Rule 2. Rhythm metro pulse is routed 30% left, 10% right: mix via GainNode(0.3) to left channel + GainNode(0.1) to right channel.
  Rule 3. Error/noise channel is routed to right channel only via PannerNode.pan.value = 1.0, isolating churn to one ear.
  Rule 4. Ambient drone is centre-panned (pan = 0) and its gain reduced by 6 dB relative to non-headphone mode.
  Rule 5. All other channels obey their per-channel pan setting, defaulting to centre.
  Rule 6. A headphone-mode indicator light and the active panning ruleset MUST be visible in the dashboard UI.
  Rule 7. Exit headphone mode resets all PannerNode.pan.value to 0, restores ambient gain, removes the indicator.

## Worked Examples

### Example 1: Mute-Group Toggle

Input: Three channels named revenue, errors, users. All channels unmuted. Revenue gain = 0.8, errors gain = 0.4, users gain = 0.6. User clicks the mute toggle on the revenue channel.

Invariants:
  - Mute state model: each channel has a boolean muted flag.
  - Solo state is irrelevant in this example (all false).
  - When a channel's muted flag flips to true, its gain node MUST be set to 0 immediately via gain.value = 0 (not setTargetAtTime).
  - When a channel's muted flag flips to false, its gain must return to its target volume via setTargetAtTime with timeConstant = 0.02.
  - No other channel's gain changes.

Step-by-step:
  1. User clicks mute button on revenue channel.
  2. Event handler reads channel state: revenue.muted = false.
  3. Handler toggles revenue.muted = true.
  4. Handler sets revenueGain.value = 0.
  5. Since soloCount = 0, no mute-group rebalancing needed.
  6. UI update: mute icon becomes active (filled speaker icon), volume slider visually dimmed.
  7. Audio output: revenue channel silent, errors and users continue at 0.4 and 0.6.

Output: Revenue channel silenced. Errors and users gain unchanged.

### Example 2: Solo-Exclusive Flip

Input: Four channels: revenue, errors, users, latency. All channels unmuted, no solo active. Revenue gain = 0.7, errors gain = 0.5, users gain = 0.6, latency gain = 0.4. User clicks the solo button on the errors channel.

Invariants:
  - Solo state model: each channel has a boolean solo flag.
  - soloCount tracks the number of channels with solo = true.
  - When soloCount transitions from 0 to > 0, all non-soloed channels must mute immediately.
  - When soloCount transitions from > 0 to 0, all channels must unmute (restore pre-solo gain envelopes).
  - The soloed channel itself remains at its target gain.
  - Exclusive rule: toggling solo on one channel when another is already soloed must NOT affect the already-soloed channel, and must NOT change soloCount incorrectly.

Step-by-step:
  1. User clicks solo button on errors channel.
  2. Handler reads channel state: errors.solo = false, soloCount = 0.
  3. Handler sets errors.solo = true, soloCount = 1.
  4. Handler iterates all channels:
     - revenue.solo = false -> mute (set revenueGain.value = 0)
     - errors.solo = true -> maintain target gain 0.5 (no change)
     - users.solo = false -> mute (set usersGain.value = 0)
     - latency.solo = false -> mute (set latencyGain.value = 0)
  5. UI update: solo button on errors channel becomes active (glowing/yellow). All non-solo channels show visually muted state.
  6. Audio output: only errors channel audible at 0.5 gain.

Now user clicks solo on revenue channel while errors is still soloed:
  7. Handler reads revenue.solo = false, soloCount = 1.
  8. Handler sets revenue.solo = true, soloCount = 2.
  9. Handler checks soloCount > 0 (still true), so only unmutes channels with solo = true:
     - errors (unchanged, stays unmuted at 0.5)
     - revenue (unmuted, ramps from 0 to 0.7 via setTargetAtTime with timeConstant 0.02)
     - users (solo = false, stays muted)
     - latency (solo = false, stays muted)

Output: errors and revenue simultaneously audible. Users and latency remain silent.

Now user clicks solo on errors channel to deactivate it:
  10. Handler reads errors.solo = true, soloCount = 2.
  11. Handler sets errors.solo = false, soloCount = 1.
  12. Since soloCount > 0 (revenue still soloed), no unmute occurs for non-soloed channels.
  13. errors mutes (revenueGain.value = 0). Wait — invariant: when a channel's solo transitions from true to false, that channel must mute IF soloCount > 0 after decrement. This is correct.
  14. Audio output: only revenue channel audible at 0.7.

Finally user clicks solo on revenue channel to deactivate:
  15. Handler reads revenue.solo = true, soloCount = 1.
  16. Handler sets revenue.solo = false, soloCount = 0.
  17. Since soloCount === 0, all channels unmute: revenue ramps to 0.7, errors ramps to 0.5, users ramps to 0.6, latency ramps to 0.4.
  18. Audio output: all four channels audible at original gain values.

### Example 3: Frequency-Split Merge

Input: A single channel named system-health carrying a composite metric value v = 75 (scale 0-100). The channel uses a FrequencySplitMergeNode that splits the signal into three bands: bass (20-250 Hz), mid (250-2000 Hz), treble (2000-8000 Hz). Each band is mapped to a sub-component of the metric: CPU load maps to bass amplitude, memory pressure maps to mid, I/O wait maps to treble.

Invariants:
  - Each band uses a BiquadFilterNode configured as lowpass/highpass/bandpass with the specified cutoff frequencies.
  - Band type: bass = lowpass at 250 Hz, mid = bandpass (250-2000 Hz), treble = highpass at 2000 Hz.
  - Each band's gain is controlled by a separate GainNode whose value is computed from the sub-metric value using the Linear Slope Mapping formula.
  - The band gain nodes are connected in parallel from the source, then each band sums into the master gain bus.
  - The sum of all three band gains MUST NOT exceed 1.0.
  - If a sub-metric is missing (null/undefined), its band gain defaults to 0 and the BiquadFilterNode is bypassed via a direct connection around it.

Step-by-step:
  1. Dashboard receives metric update: system-health = 75.
  2. MetricBus parses the composite value into sub-components: cpuLoad = 80 (range 0-100), memPressure = 65 (range 0-100), ioWait = 30 (range 0-100).
  3. Linear mapping for each band:
     - Bass gain (maps cpuLoad): 0.0 + ((80 - 0) / (100 - 0)) * 1.0 = 0.8
     - Mid gain (maps memPressure): 0.0 + ((65 - 0) / (100 - 0)) * 1.0 = 0.65
     - Treble gain (maps ioWait): 0.0 + ((30 - 0) / (100 - 0)) * 1.0 = 0.3
  4. Summation check: 0.8 + 0.65 + 0.3 = 1.75. This exceeds 1.0.
  5. Apply summation constraint: scale factor = 1.0 / 1.75 = 0.571.
  6. Final gains: bass = 0.8 * 0.571 = 0.457, mid = 0.65 * 0.571 = 0.371, treble = 0.3 * 0.571 = 0.171.
  7. Set band gain values via setTargetAtTime with timeConstant = 0.05.
  8. If ioWait were null: treble gain would be 0, treble BiquadFilterNode bypassed via direct connection from source to master bus. Recalculate: 0.8 + 0.65 = 1.45 > 1.0, scale to 0.690. Final: bass = 0.552, mid = 0.448.

Output: Three-band audio signal where bass dominates (high CPU), mid is moderate (medium memory), treble is faint (low I/O wait), scaled to prevent clipping.

## Error-Handling Edge Cases

### Circular Mute-Group Chains

A mute group chain is defined as a set where toggling one channel's mute triggers programmatic mute on a second channel, which triggers mute on the first. This creates infinite recursion.

Detection: maintain a Set<mutedChannelId> accumulator before entering the mute-group propagation loop. After each channel is programmatically muted, add its id to the set. If the next channel to mute is already in the set, abort the propagation chain for that branch and log a warning to a circular-dependency diagnostic panel.

Recovery: break the chain by skipping the duplicate mute operation. The channel that caused the cycle remains in its current mute state. The diagnostic panel must display the full chain: [channelA, channelB, channelA] and highlight it in red.

Prevention: during channel initialisation, the mute-group configuration must be validated. If the graph of mute-group edges contains a cycle (detected via DFS traversal over the adjacency list), the config is rejected and the dashboard loads with all mute groups disabled. The validation error must be shown on screen.

### Orphaned Solo-Latches After Source Removal

A solo latch is the boolean solo flag on a channel being true. When a data source is removed (e.g., a metric stream disconnects, a file is closed), all channels associated with that source must have their solo flag cleared and their gain reset to 0 before the channel is disposed.

The orphaned solo latch hazard: if a source is removed while soloCount > 0 and the channel's solo flag is true, removing that channel from the channel list decrements soloCount inconsistently (the handler never fires).

Resolution: implement a sourceDisconnectHandler that runs before any channel removal:

  1. For each channel linked to the departing source:
     a. If channel.solo === true, set channel.solo = false, decrement soloCount.
     b. If soloCount === 0 after decrement: unmute all channels by restoring their pre-solo gain envelopes.
     c. Set channel.gain.value = 0 via immediate assignment.
     d. Disconnect channel's audio nodes from the routing graph.
     e. Remove channel from the channel registry.
  2. If soloCount > 0 after all removals, the remaining soloed channels maintain their exclusive output.
  3. After removal, verify that soloCount >= 0 and soloCount <= number of remaining channels. If violated, roll soloCount to the actual number of soloed channels and log a state-correction warning.

Edge sub-case: removing the last soloed channel must trigger the soloCount -> 0 unmute all transition (step 1b above). Failing this leaves all channels muted permanently.

### Overflow in Frequency-Mapped Buses

A frequency-mapped bus is any bus whose gain result exceeds the limits established by the Summation Constraint (total peak gain > 1.0). Three overflow scenarios:

Scenario A: Single-channel overflow
  A metric value exceeds the formula's expected range and maps to a frequency above f_high.
  Resolution: apply input clamping before mapping: v_clamped = Math.max(min, Math.min(v, max)). The clamp boundary is logged to console once per source per session. No frequency above f_high + 10% of range is ever scheduled.

Scenario B: Multi-channel summation overflow
  After scaling, individual channels are within range but the sum exceeds 1.0.
  Resolution: execute the summation constraint algorithm on every MetricBus tick:
    1. Sum all current channel gain values.
    2. If sum > 1.0, compute scaleFactor = 1.0 / sum.
    3. Apply gain *= scaleFactor to every channel via setTargetAtTime with timeConstant = 0.02.
    4. Track RMS master gain over a 1-second sliding window. If RMS stays > 0.8, hold the scale factor. If RMS drops below 0.6, release (set scaleFactor back to 1.0 over 200 ms ramp).
    5. Log a warning to the diagnostic panel each time the scale factor is applied for more than 2 consecutive seconds.

Scenario C: Oscillator frequency overflow
  A mapping formula produces a frequency above the channel's Nyquist limit (sampleRate / 2) or below the audible floor (20 Hz).
  Resolution: clamp to [20, sampleRate/2 - 1]. If the clamped value equals either boundary, increment a per-channel overflow counter visible in the diagnostic panel. After 5 overflows in 10 seconds on the same channel, reset the channel's mapping range to a narrower default band and log a re-calibration event.

## CSS Quality

All CSS transitions MUST be defined on the base element (not only on :hover or :focus pseudo-classes) with at least 200ms duration and ease-in-out timing function. This ensures the exit transition is also animated rather than snapping back instantly.

Shared hover, focus, and animation rules MUST be extracted into reusable utility classes (e.g., .transition-soft, .hover-lift, .focus-ring) to eliminate redundant declarations. Identical transition blocks appearing on more than 3 different selectors fail review.

Each transition must specify exactly which property is transitioning (e.g., transition: background-color 200ms ease-in-out, not transition: all 200ms). The only exception is transform-based animations where the transitioning element has only one animated property.
