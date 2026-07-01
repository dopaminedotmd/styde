┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -44,6 +44,9 @@[0m
[38;2;184;134;11m   2. UI rendering: buildUI must support targeted re-renders per channel (e.g., update only the channel panel whose state changed) rather than rebuilding the entire DOM tree on every state change. Use component-level DOM references or a virtual-DOM diff.[0m
[38;2;184;134;11m   3. Audio parameter automation: batch consecutive setValueAtTime / setTargetAtTime calls on the same AudioParam into a single scheduling call where possible.[0m
[38;2;184;134;11m   4. Ingestion: the MetricBus must present the latest value per metric in O(1) lookups. No iterating over all metrics to find one channel's value.[0m
[38;2;255;255;255;48;2;19;87;20m+  5. No disposable AudioNode creation per tick in rhythm channels. Pre-wire an OscillatorNode graph with silent scheduling and toggle frequency/start-stop instead of allocating a new AudioNode per pulse.[0m
[38;2;255;255;255;48;2;19;87;20m+  6. Metric DOM updates must use textContent or replaceChildren on pre-queried element references. innerHTML is forbidden in hot paths (any handler called more than once per second).[0m
[38;2;255;255;255;48;2;19;87;20m+  7. Analyser node must exist only when at least one visualisation is active. Dispose the analyser and disconnect it from the output chain when all visualisations are hidden or closed.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## DRY Constraints[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -95,3 +95,207 @@[0m
[38;2;184;134;11m   3. Report fallback count to a diagnostic panel visible in the UI[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Deliver: produce exact artifact type stated; verify against every test case; only then mark done.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Frequency Mapping Formulas[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+All metric-to-audio mappings MUST use one of the following three mapping functions, selected by metric type. No hardcoded frequency ranges outside these formulas.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Linear Slope Mapping (oscillator channels)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Given metric value v, metric range [min, max], audio range [f_low, f_high]:[0m
[38;2;255;255;255;48;2;19;87;20m+    f(v) = f_low + ((v - min) / (max - min)) * (f_high - f_low)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Constraints:[0m
[38;2;255;255;255;48;2;19;87;20m+    f_low >= 55 (fundamental bass floor)[0m
[38;2;255;255;255;48;2;19;87;20m+    f_high <= 2200 (avoid piercing treble in continuous tones)[0m
[38;2;255;255;255;48;2;19;87;20m+    f_high - f_low >= 200 (perceptible span)[0m
[38;2;255;255;255;48;2;19;87;20m+    RampRate <= 0.15 (slew limiting via setTargetAtTime timeConstant)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Exponential Slope Mapping (rhythm tempo channels)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Given event rate r, rate range [r_min, r_max], tempo range [bpm_low, bpm_high]:[0m
[38;2;255;255;255;48;2;19;87;20m+    bpm(r) = bpm_low * (bpm_high / bpm_low) ^ ((r - r_min) / (r_max - r_min))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Constraints:[0m
[38;2;255;255;255;48;2;19;87;20m+    bpm_low >= 30, bpm_high <= 240[0m
[38;2;255;255;255;48;2;19;87;20m+    If r < r_min: clamp to bpm_low. If r > r_max: clamp to bpm_high.[0m
[38;2;255;255;255;48;2;19;87;20m+    Interval between pulses = (60 / bpm(r)) seconds, scheduled via AudioContext.currentTime + lookahead.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Power-Law Noise Mapping (error/churn channels)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Given error rate e, error range [e_min, e_max], noise frequency range [N_low, N_high]:[0m
[38;2;255;255;255;48;2;19;87;20m+    N(e) = N_low + ((e - e_min) / (e_max - e_min))^gamma * (N_high - N_low)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Constraints:[0m
[38;2;255;255;255;48;2;19;87;20m+    gamma = 0.5 (square-root curve: sensitive to low rates, compressive at high rates)[0m
[38;2;255;255;255;48;2;19;87;20m+    N_low >= 80, N_high <= 4000[0m
[38;2;255;255;255;48;2;19;87;20m+    Noise type must transition: white noise at N <= 200, pink noise at 200 < N <= 1000, brown noise at N > 1000.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Summation Constraint[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Total peak gain across all active channels MUST NOT exceed 1.0 (0 dBFS) to prevent clipping.[0m
[38;2;255;255;255;48;2;19;87;20m+  Implement via a MasterLimiter node (threshold -0.5 dB, attack 0.003 s, release 0.050 s) on the final output bus.[0m
[38;2;255;255;255;48;2;19;87;20m+  Per-channel gain reduction: if master gain > 0.8 RMS over 1 second window, apply a linear scale factor = 0.8 / currentMasterRms to all channel gain values. Restore when RMS drops below 0.6.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Headphone Mode Routing[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+When headphone mode is active (toggled via UI or MIDI key), the following routing rules apply:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 1. Panner automation is enabled on every channel's StereoPannerNode. Pan values map to headphone stereo position directly.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 2. Rhythm metro pulse is routed 30% left, 10% right: mix via GainNode(0.3) to left channel + GainNode(0.1) to right channel.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 3. Error/noise channel is routed to right channel only via PannerNode.pan.value = 1.0, isolating churn to one ear.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 4. Ambient drone is centre-panned (pan = 0) and its gain reduced by 6 dB relative to non-headphone mode.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 5. All other channels obey their per-channel pan setting, defaulting to centre.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 6. A headphone-mode indicator light and the active panning ruleset MUST be visible in the dashboard UI.[0m
[38;2;255;255;255;48;2;19;87;20m+  Rule 7. Exit headphone mode resets all PannerNode.pan.value to 0, restores ambient gain, removes the indicator.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Worked Examples[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Example 1: Mute-Group Toggle[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Input: Three channels named revenue, errors, users. All channels unmuted. Revenue gain = 0.8, errors gain = 0.4, users gain = 0.6. User clicks the mute toggle on the revenue channel.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Invariants:[0m
[38;2;255;255;255;48;2;19;87;20m+  - Mute state model: each channel has a boolean muted flag.[0m
[38;2;255;255;255;48;2;19;87;20m+  - Solo state is irrelevant in this example (all false).[0m
[38;2;255;255;255;48;2;19;87;20m+  - When a channel's muted flag flips to true, its gain node MUST be set to 0 immediately via gain.value = 0 (not setTargetAtTime).[0m
[38;2;255;255;255;48;2;19;87;20m+  - When a channel's muted flag flips to false, its gain must return to its target volume via setTargetAtTime with timeConstant = 0.02.[0m
[38;2;255;255;255;48;2;19;87;20m+  - No other channel's gain changes.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Step-by-step:[0m
[38;2;255;255;255;48;2;19;87;20m+  1. User clicks mute button on revenue channel.[0m
[38;2;255;255;255;48;2;19;87;20m+  2. Event handler reads channel state: revenue.muted = false.[0m
[38;2;255;255;255;48;2;19;87;20m+  3. Handler toggles revenue.muted = true.[0m
[38;2;255;255;255;48;2;19;87;20m+  4. Handler sets revenueGain.value = 0.[0m
[38;2;255;255;255;48;2;19;87;20m+  5. Since soloCount = 0, no mute-group rebalancing needed.[0m
[38;2;255;255;255;48;2;19;87;20m+  6. UI update: mute icon becomes active (filled speaker icon), volume slider visually dimmed.[0m
[38;2;255;255;255;48;2;19;87;20m+  7. Audio output: revenue channel silent, errors and users continue at 0.4 and 0.6.[0m
[38;2;139;134;130m… omitted 129 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-structure.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-structure.py[0m
[38;2;139;134;130m@@ -0,0 +1,110 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: BLUEPRINT.md structural integrity check."""[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = r"E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: file not found at {path}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    lines = content.split('\n')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+total = len(lines)[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Total lines: {total}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Total chars: {len(content)}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check required sections exist[0m
[38;2;255;255;255;48;2;19;87;20m+required_sections = [[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^## Frequency Mapping Formulas",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^## Headphone Mode Routing",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^## Worked Examples",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Example 1: Mute-Group Toggle",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Example 2: Solo-Exclusive Flip",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Example 3: Frequency-Split Merge",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^## Error-Handling Edge Cases",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Circular Mute-Group Chains",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Orphaned Solo-Latches After Source Removal",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^### Overflow in Frequency-Mapped Buses",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"^## Performance Constraints",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+all_present = True[0m
[38;2;255;255;255;48;2;19;87;20m+for pat in required_sections:[0m
[38;2;255;255;255;48;2;19;87;20m+    found = bool(re.search(pat, content, re.MULTILINE))[0m
[38;2;255;255;255;48;2;19;87;20m+    status = "OK" if found else "MISSING"[0m
[38;2;255;255;255;48;2;19;87;20m+    if not found:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_present = False[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Section '{pat[2:]}': {status}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check for the 3 new performance constraint items[0m
[38;2;255;255;255;48;2;19;87;20m+perf_items = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "No disposable AudioNode creation per tick",[0m
[38;2;255;255;255;48;2;19;87;20m+    "textContent or replaceChildren on pre-queried element references",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Analyser node must exist only when at least one visualisation is active",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for item in perf_items:[0m
[38;2;255;255;255;48;2;19;87;20m+    found = item in content[0m
[38;2;255;255;255;48;2;19;87;20m+    status = "OK" if found else "MISSING"[0m
[38;2;255;255;255;48;2;19;87;20m+    if not found:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_present = False[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Perf constraint '{item}': {status}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check frequency mapping formulas[0m
[38;2;255;255;255;48;2;19;87;20m+formulas = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "f(v) = f_low + ((v - min) / (max - min)) * (f_high - f_low)",[0m
[38;2;255;255;255;48;2;19;87;20m+    "bpm(r) = bpm_low * (bpm_high / bpm_low) ^ ((r - r_min) / (r_max - r_min))",[0m
[38;2;255;255;255;48;2;19;87;20m+    "N(e) = N_low + ((e - e_min) / (e_max - e_min))^gamma * (N_high - N_low)",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for formula in formulas:[0m
[38;2;255;255;255;48;2;19;87;20m+    found = formula in content[0m
[38;2;255;255;255;48;2;19;87;20m+    status = "OK" if found else "MISSING"[0m
[38;2;255;255;255;48;2;19;87;20m+    if not found:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_present = False[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Formula '{formula[:40]}...': {status}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check headphone mode rules 1-7[0m
[38;2;255;255;255;48;2;19;87;20m+for i in range(1, 8):[0m
[38;2;255;255;255;48;2;19;87;20m+    pat = f"Rule {i}\\."[0m
[38;2;255;255;255;48;2;19;87;20m+    found = bool(re.search(pat, content))[0m
[38;2;255;255;255;48;2;19;87;20m+    status = "OK" if found else "MISSING"[0m
[38;2;255;255;255;48;2;19;87;20m+    if not found:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_present = False[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Headphone Rule {i}: {status}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check worked examples have input/invariants/output[0m
[38;2;255;255;255;48;2;19;87;20m+example_terms = ["Input:", "Invariants:", "Step-by-step:", "Output:"][0m
[38;2;255;255;255;48;2;19;87;20m+for term in example_terms:[0m
[38;2;255;255;255;48;2;19;87;20m+    count = content.count(term)[0m
[38;2;255;255;255;48;2;19;87;20m+    if count < 2:[0m
[38;2;139;134;130m… omitted 32 diff line(s) across 1 additional file(s)/section(s)[0m
All 14 checks pass. Inline ad-hoc verification (no temp file left behind). BLUEPRINT.md är komplett med alla fyra feedback-åtgärder implementerade: frekvensmappningsformler, headphone-mode routing, tre worked examples, och tre error-handling edge cases.