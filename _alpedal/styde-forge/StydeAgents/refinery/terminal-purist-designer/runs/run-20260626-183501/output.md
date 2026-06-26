┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,5 +1,5 @@[0m
[38;2;184;134;11m # Terminal Purist Designer[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** frontend **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+**Domain:** frontend **Version:** 2[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;184;134;11m Design true terminal-aesthetic dashboard mockups. Monochrome green/amber on black, block cursor, fixed-width typography, ASCII borders, minimal CSS. Feels like a real TUI brought to web.[0m
[38;2;139;134;130m@@ -11,3 +11,29 @@[0m
[38;2;184;134;11m - industrial-brutalist-ui[0m
[38;2;184;134;11m - high-end-visual-design[0m
[38;2;184;134;11m - swiss-design[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Viewport Width Guard[0m
[38;2;255;255;255;48;2;19;87;20m+Before emitting any mockup, verify total character width (including borders) does not exceed the allowed maximum for the target font-size and viewport. Calculate NNN as floor(viewport_px / font_size_px). At 12px font and 480px viewport, NNN = 40 characters (480/12). At 14px and 480px, NNN = 34. At 12px and 640px, NNN = 53. If the mockup's widest line exceeds NNN, truncate content or reflow to a multi-line layout. Box-drawing characters (─, │, ┌, ┐, └, ┘, ├, ┤, ┬, ┴, ┼) count as 1 character each. Unibody characters at fullwidth count as 2. Measure every line before emission.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Row-Boundary Alignment[0m
[38;2;255;255;255;48;2;19;87;20m+After drawing each horizontal section separator (any line composed of box-drawing horizontals and junctions), verify that box-drawing characters on the following line align with their counterparts above. Concretely: for every column position c, if the separator at c contains a vertical junction (┬, ┴, ┼, ├, ┤) or corner (┌, ┐, └, ┘), verify the character directly below at (next_row, c) is also a vertical box-drawing character (│, ├, ┤, ┼, ┬, ┴) or an empty cell that should contain one. If misalignment is detected, adjust spacing in the content row by inserting or removing spaces at content boundaries; do not break the separator. Re-check after every row until the panel boundary is closed.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Failure Modes[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### NNN Threshold Non-Convergence[0m
[38;2;255;255;255;48;2;19;87;20m+If the computed NNN for a given viewport/font-size pair yields a value below the minimum content width required for any single panel (e.g. less than 20 chars for a label column), fall back to the smallest panel-level NNN across all panels. If even that fails, emit a warning and render at a hard minimum of 16 characters, truncating with ellipsis (...) for any overflowing cells.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Reflow Failure[0m
[38;2;255;255;255;48;2;19;87;20m+When reflowing a single-row layout to multi-row, adjacent cells may drift out of vertical alignment. If reflow is triggered, perform a post-reflow row-alignment pass: for every logical table row, pad each cell's text content to the width of its widest cell in that logical row. If alignment still diverges by more than 1 character column, abort reflow and render the panel as a flat labeled list (key: value) with no column alignment.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Row-Alignment Divergence[0m
[38;2;255;255;255;48;2;19;87;20m+If a row-boundary alignment check (see above) fails after two correction attempts, the mockup MUST NOT emit a malformed box-drawing section. Instead, replace the entire panel with a plain text section using simple dashes (-----) as separators and pipe symbols (|) for vertical edges. Log a structured warning to output noting which panel failed and why.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Verification Criteria[0m
[38;2;255;255;255;48;2;19;87;20m+Every improvement or change to the mockup pipeline must be accompanied by:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+(a) Integration point in pipeline — specify where in the render chain the change applies (e.g. "after character-width calculation, before mockup serialization").[0m
[38;2;255;255;255;48;2;19;87;20m+(b) Expected observable outcome — describe the specific difference in mockup output (e.g. "all lines are <= NNN characters", "separator junctions align perfectly with content-row vertical bars").[0m
[38;2;255;255;255;48;2;19;87;20m+(c) Fallback on mismatch — what action is taken when the assertion fails (e.g. "truncate to NNN-2 and append '..'", "replace panel with flat list").[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Test cases must cover at minimum: normal case (content fits NNN), edge case (content exactly equals NNN), overflow case (content exceeds NNN by 1-3 chars), and extreme case (content exceeds NNN by 50%). Each test case must document the expected output format and any fallback triggered.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\persona.md[0m
[38;2;139;134;130m@@ -2,3 +2,11 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Fas 0.5 — Design mockups[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Enforcement directives:[0m
[38;2;255;255;255;48;2;19;87;20m+- Before emitting any mockup, verify total character width (including borders) <= NNN for the given font-size; truncate or reflow if violated.[0m
[38;2;255;255;255;48;2;19;87;20m+- After drawing each horizontal section separator, verify that box-drawing characters on the following line align with their counterparts above.[0m
[38;2;255;255;255;48;2;19;87;20m+- For every proposed change to the mockup pipeline, also specify:[0m
[38;2;255;255;255;48;2;19;87;20m+  (a) how it integrates with the existing pipeline,[0m
[38;2;255;255;255;48;2;19;87;20m+  (b) expected observable outcome,[0m
[38;2;255;255;255;48;2;19;87;20m+  (c) fallback on mismatch.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-terminal-purist-bp.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-terminal-purist-bp.py[0m
[38;2;139;134;130m@@ -0,0 +1,135 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: terminal-purist-designer BLUEPRINT.md + persona.md changes.[0m
[38;2;255;255;255;48;2;19;87;20m+Checks all requirements from Teacher Feedback (88.6 + 87.0) are present in the updated files."""[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BP = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+PERSONA = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\terminal-purist-designer\persona.md"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+passed = 0[0m
[38;2;255;255;255;48;2;19;87;20m+failed = 0[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(label, condition, detail=""):[0m
[38;2;255;255;255;48;2;19;87;20m+    global passed, failed[0m
[38;2;255;255;255;48;2;19;87;20m+    if condition:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  PASS  {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        failed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL  {label}  {detail}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+with open(BP, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== BLUEPRINT.md ===")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# VERSION BUMP[0m
[38;2;255;255;255;48;2;19;87;20m+check("Version bumped to 2",[0m
[38;2;255;255;255;48;2;19;87;20m+      "Version: 2" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "got version " + (re.search(r'Version:\s*(\d+)', bp).group(1) if re.search(r'Version:\s*(\d+)', bp) else "none"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# VIEWPORT WIDTH GUARD - from feedback 88.6[0m
[38;2;255;255;255;48;2;19;87;20m+check("Viewport Width Guard section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+      "## Viewport Width Guard" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("NNN calculation formula present (floor/viewport/font-size)",[0m
[38;2;255;255;255;48;2;19;87;20m+      "floor(viewport_px / font_size_px)" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing floor formula")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Concrete examples given (12px/480px, 14px/480px, 12px/640px)",[0m
[38;2;255;255;255;48;2;19;87;20m+      "12px font and 480px" in bp and "14px and 480px" in bp and "12px and 640px" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing concrete examples")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Box-drawing char counting rule present",[0m
[38;2;255;255;255;48;2;19;87;20m+      "count as 1 character each" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing box-drawing char rule")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Truncate or reflow fallback specified",[0m
[38;2;255;255;255;48;2;19;87;20m+      "truncate content or reflow" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing truncate/reflow fallback")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ROW-BOUNDARY ALIGNMENT - from feedback 88.6[0m
[38;2;255;255;255;48;2;19;87;20m+check("Row-Boundary Alignment section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+      "## Row-Boundary Alignment" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Row alignment procedure (column-by-column check) present",[0m
[38;2;255;255;255;48;2;19;87;20m+      "for every column position c" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing column-by-column check description")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Vertical junction/corner verification specified",[0m
[38;2;255;255;255;48;2;19;87;20m+      "verify the character directly below" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing vertical alignment verification")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Adjustment strategy specified (insert/remove spaces at content boundaries)",[0m
[38;2;255;255;255;48;2;19;87;20m+      "adjust spacing in the content row" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "missing alignment adjustment strategy")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# FAILURE MODES - from feedback 87.0[0m
[38;2;255;255;255;48;2;19;87;20m+check("Failure Modes section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+      "## Failure Modes" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("NNN Threshold Non-Convergence sub-section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+      "### NNN Threshold Non-Convergence" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check("Reflow Failure sub-section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+      "### Reflow Failure" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 57 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-terminal-purist-bp.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-terminal-purist-bp.py[0m
[38;2;139;134;130m@@ -27,8 +27,8 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m # VERSION BUMP[0m
[38;2;184;134;11m check("Version bumped to 2",[0m
[38;2;255;255;255;48;2;119;20;20m-      "Version: 2" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-      "got version " + (re.search(r'Version:\s*(\d+)', bp).group(1) if re.search(r'Version:\s*(\d+)', bp) else "none"))[0m
[38;2;255;255;255;48;2;19;87;20m+      "Version:** 2" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+      "got version " + (re.search(r'Version:\*+\s*(\d+)', bp).group(1) if re.search(r'Version:\*+\s*(\d+)', bp) else "none"))[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m # VIEWPORT WIDTH GUARD - from feedback 88.6[0m
[38;2;184;134;11m check("Viewport Width Guard section exists",[0m
Ad-hoc verification: 25/25 passed, 0 failed.
All requirements from both feedback runs confirmed present:
- 88.6 feedback: Viewport Width Guard with NNN math + Row-Boundary Alignment with column-by-column check -- both sections exist with concrete procedures
- 87.0 feedback: Failure Modes (3 sub-scenarios with fallback logic) + Verification Criteria (a/b/c requirements + 4 test case types) -- all present in BLUEPRINT.md
- persona.md: all 3 enforcement directives present (viewport guard, row-alignment, pipeline integration/outcome/fallback)
Temp script cleaned up. No canonical test suite exists for .md blueprint files -- this was ad-hoc structural verification only.