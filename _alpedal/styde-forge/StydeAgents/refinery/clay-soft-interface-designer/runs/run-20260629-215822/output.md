┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -2,6 +2,8 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Domain: dashboard[0m
[38;2;184;134;11m Version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+ARTIFACT-FIRST GATE — MUST produce working files (HTML/CSS/JS) as primary output. Never output a specification document or design plan. If context or constraints are missing, produce best-effort files and note assumptions inline rather than falling back to a spec. This blueprint exists only to guide artifact creation; the artifact is the deliverable.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -96,7 +96,7 @@[0m
[38;2;184;134;11m   2. On decode failure, fall back to oscillator-based synthesis for that sound[0m
[38;2;184;134;11m   3. Report fallback count to a diagnostic panel visible in the UI[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-Deliver: produce exact artifact type stated; verify against every test case; only then mark done.[0m
[38;2;255;255;255;48;2;19;87;20m+DELIVERABLE VERIFICATION GATE — agent MUST list the absolute paths of every file it created (e.g., /path/to/index.html, /path/to/script.js). If no files were produced, the gate fails and the agent must produce files before marking done. Each file must be verified: check that its size > 0 bytes, that referenced assets exist or are inlined, and that opening the HTML in a browser produces a working dashboard (no blank page, no console errors from missing dependencies).[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Frequency Mapping Formulas[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -80,6 +80,21 @@[0m
[38;2;184;134;11m   - Both, toggled via a UI button[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m If neither is wired, remove the analyser node entirely. Dead nodes that consume CPU but produce no output are not allowed.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Accessibility Checklist[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+All interactive elements (buttons, toggles, sliders, channel panels, mute/solo controls, visualisation switchers, file-drop zones) MUST include:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  - aria-label describing the element's function (e.g., aria-label="Mute revenue channel")[0m
[38;2;255;255;255;48;2;19;87;20m+  - role attribute matching the element's interactive purpose (role="switch" for mute/solo toggles, role="slider" for volume sliders, role="button" for clickable controls)[0m
[38;2;255;255;255;48;2;19;87;20m+  - visible focus indicator on keyboard focus (outline: 2px solid or equivalent, never outline: none)[0m
[38;2;255;255;255;48;2;19;87;20m+  - full keyboard navigation: Tab to move between controls, Enter/Space to activate toggles and buttons, Arrow keys for sliders and pan controls[0m
[38;2;255;255;255;48;2;19;87;20m+  - aria-pressed or aria-checked reflecting current state on toggle and switch elements[0m
[38;2;255;255;255;48;2;19;87;20m+  - aria-live="polite" region for announcements of metric changes, audio state transitions, and error conditions[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Cards and channel panels MUST use semantic HTML: <article> for standalone channel panels with <h2> or <h3> headings for the channel name, <section> for grouped content regions.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+File-drop zones MUST include an accessible method (hidden <input type="file"> with explicit label) as an alternative to drag-and-drop.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Implementation Guidance[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -316,3 +316,11 @@[0m
[38;2;184;134;11m Scenario C: Oscillator frequency overflow[0m
[38;2;184;134;11m   A mapping formula produces a frequency above the channel's Nyquist limit (sampleRate / 2) or below the audible floor (20 Hz).[0m
[38;2;184;134;11m   Resolution: clamp to [20, sampleRate/2 - 1]. If the clamped value equals either boundary, increment a per-channel overflow counter visible in the diagnostic panel. After 5 overflows in 10 seconds on the same channel, reset the channel's mapping range to a narrower default band and log a re-calibration event.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## CSS Quality[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+All CSS transitions MUST be defined on the base element (not only on :hover or :focus pseudo-classes) with at least 200ms duration and ease-in-out timing function. This ensures the exit transition is also animated rather than snapping back instantly.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Shared hover, focus, and animation rules MUST be extracted into reusable utility classes (e.g., .transition-soft, .hover-lift, .focus-ring) to eliminate redundant declarations. Identical transition blocks appearing on more than 3 different selectors fail review.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Each transition must specify exactly which property is transitioning (e.g., transition: background-color 200ms ease-in-out, not transition: all 200ms). The only exception is transform-based animations where the transitioning element has only one animated property.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py[0m
[38;2;139;134;130m@@ -0,0 +1,65 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: check all 4 teacher-feedback changes applied to BLUEPRINT.md"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+bp = os.path.join(os.environ.get('FORGE_ROOT', r'E:\Stryde\_alpedal\styde-forge'), 'BLUEPRINT.md')[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(bp):[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = r'E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    text = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Artifact-first gate[0m
[38;2;255;255;255;48;2;19;87;20m+if 'ARTIFACT-FIRST GATE' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: artifact-first gate (ARTIFACT-FIRST GATE)')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. Deliverable Verification Gate (replaces old self-validation)[0m
[38;2;255;255;255;48;2;19;87;20m+if 'DELIVERABLE VERIFICATION GATE' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: deliverable verification gate')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'list the absolute paths' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: file path listing requirement in verification gate')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check old text is GONE[0m
[38;2;255;255;255;48;2;19;87;20m+if 'produce exact artifact type stated; verify against every test case' in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('STALE: old self-validation gate still present')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Accessibility Checklist[0m
[38;2;255;255;255;48;2;19;87;20m+if 'Accessibility Checklist' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: Accessibility Checklist section')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'aria-label' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: aria-label requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'role attribute' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: role attribute requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'focus indicator' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: focus indicator requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'keyboard navigation' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: keyboard navigation requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if '<article>' not in text or 'semantic HTML' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: semantic HTML requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. CSS Quality section[0m
[38;2;255;255;255;48;2;19;87;20m+if 'CSS Quality' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: CSS Quality section')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'base element' not in text and 'not only on :hover' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: transition on base element rule')[0m
[38;2;255;255;255;48;2;19;87;20m+if '200ms' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: 200ms duration requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'ease-in-out' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: ease-in-out timing requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+if 'utility class' not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append('MISSING: reusable utility class requirement')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+total_checks = 16[0m
[38;2;255;255;255;48;2;19;87;20m+passed = total_checks - len(errors)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print(f'BLUEPRINT.md: {len(text)} chars, {text.count(chr(10)) + 1} lines')[0m
[38;2;255;255;255;48;2;19;87;20m+print(f'Checks passed: {passed}/{total_checks}')[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'FAILURES ({len(errors)}):')[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f'  - {e}')[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print('ALL CHECKS PASSED')[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(0)[0m
Ad-hoc verification: 16/16 checks passed, temp script cleaned up.
Sammanfattning av fyra ändringar i BLUEPRINT.md:
| Andring | Hittades i filen |
|---|---|
| Artifact-first gate (rad 6) | ARTIFACT-FIRST GATE — MUST produce working files |
| Deliverable Verification Gate (rad 114) | DELIVERABLE VERIFICATION GATE — MUST list absolute paths |
| Accessibility Checklist (raderna 84-97) | aria-label, role, focus indicator, keyboard nav, semantic HTML |
| CSS Quality (raderna 320-326) | transitions on base element, 200ms ease-in-out, utility classes, inget transition: all |
Inget gammalt material kvar — den ursprungliga self-validation texten ("produce exact artifact type stated; verify against every test case") ar borttagen.