┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -25,15 +25,31 @@[0m
[38;2;184;134;11m - JavaScript modern syntax: Use const/let (no var), arrow functions (no function keyword), template literals (no string concatenation with +), and spread/rest operators. Every function must be an arrow function or method shorthand; the `function` keyword is prohibited in inline scripts.[0m
[38;2;184;134;11m - Sub-label clarity: All sub-labels and units must be unambiguous and descriptive (e.g., "12% of 10 Gbps link" not just "12%", "3.2 GHz / 8 cores" not just "3.2") so users never need to infer context.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Verification Protocol[0m
[38;2;255;255;255;48;2;119;20;20m-After every build or generate action, execute a structural integrity check instead of grepping for keywords:[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-1. HTML well-formedness: validate that all tags opened are closed, no orphaned brackets, DOCTYPE present[0m
[38;2;255;255;255;48;2;19;87;20m+## Verification[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Runtime Verification Protocol (post-build)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+After every build or generate action, execute a structural integrity check that outputs a compact single-line-per-file status table. Each line: `FILENAME | PASS|FAIL | reason`. Never replay verbatim diffs or ANSI-colored output.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+1. HTML well-formedness: validate all tags closed, no orphaned brackets, DOCTYPE present[0m
[38;2;184;134;11m 2. CSS syntax: confirm no unclosed rules, selectors reference known element classes[0m
[38;2;184;134;11m 3. JavaScript completeness: all event handlers bound, all functions closed, no trailing commas in objects[0m
[38;2;255;255;255;48;2;119;20;20m-4. Content rendering: verify visual elements produce content (non-empty SVG, chart canvases with data, populated data tables)[0m
[38;2;255;255;255;48;2;19;87;20m+4. Content rendering: verify visual elements produce real content (non-empty SVG, chart canvases with data, populated tables)[0m
[38;2;184;134;11m 5. JSON state: if inline JSON is used (chart configs, mock data), validate it is parseable[0m
[38;2;184;134;11m 6. Structural presence: confirm all expected UI zones from the structural catalog exist in the DOM[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Pre-Submission Static Checklist[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Before finalizing any generated HTML mockup, confirm every item. Output is a single yes/no rollup:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- Structural zones from the catalog present and correctly positioned[0m
[38;2;255;255;255;48;2;19;87;20m+- All widgets render with real content (no "Lorem ipsum" or "Sample text")[0m
[38;2;255;255;255;48;2;19;87;20m+- CSS at-rules (@font-face, @keyframes, @media) complete and closed[0m
[38;2;255;255;255;48;2;19;87;20m+- All event listeners reference defined functions (no undefined handlers)[0m
[38;2;255;255;255;48;2;19;87;20m+- Chart/visualization canvas elements have at minimum a rendered border/background[0m
[38;2;255;255;255;48;2;19;87;20m+- SVG elements (if any) have viewBox, width, height, and content[0m
[38;2;255;255;255;48;2;19;87;20m+- No hardcoded example URLs that would 404 — use data: URIs or relative paths[0m
[38;2;255;255;255;48;2;19;87;20m+- Pre-submission style lint: `grep -n "function "` for unintended function keyword; `grep` for string concatenation via + that should be template literals; `grep` for `var` declarations — all must report zero violations[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Structural Element Catalog for Desktop Mockups[0m
[38;2;184;134;11m When generating a desktop mockup, the output MUST contain a coherent subset of the following structural elements. List which zones you include before writing code.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -233,14 +233,3 @@[0m
[38;2;184;134;11m ```[0m
[38;2;184;134;11m Zones: titlebar, left sidebar (category nav), header (none — integrated in content), content zone (general form + integration status + danger zone), status bar.[0m
[38;2;184;134;11m Rationale: Settings panel — left nav for category switching, main area with grouped sections, integration status as actionable list, danger zone visually separated with red styling.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Verification Checklist[0m
[38;2;255;255;255;48;2;119;20;20m-Before finalizing any generated HTML mockup, confirm:[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] Structural zones from the catalog are present and correctly positioned[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] All widgets render with real content (no placeholder "Lorem ipsum" or "Sample text")[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] CSS at-rules (@font-face, @keyframes, @media) are complete and closed[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] All event listeners reference defined functions (no undefined handlers)[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] Chart/visualization canvas elements have at minimum a rendered border/background to confirm DOM presence[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] SVG elements (if any) have viewBox, width, height, and content[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] No hardcoded example URLs that would 404 — use data: URIs or relative paths if images needed[0m
[38;2;255;255;255;48;2;119;20;20m-- [ ] Pre-submission style lint: grep -n "function " for unintended function keyword usage; grep for string concatenation via + that should be template literals; grep for var declarations and replace with const/let[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\config.yaml[0m
[38;2;139;134;130m@@ -21,8 +21,22 @@[0m
[38;2;184;134;11m     - css_custom_properties_for_repeated_values[0m
[38;2;184;134;11m     - unambiguous_labels_and_units[0m
[38;2;184;134;11m     pre_submit_commands:[0m
[38;2;255;255;255;48;2;119;20;20m-    - grep -n 'function ' generated/*.html || true[0m
[38;2;255;255;255;48;2;119;20;20m-    - grep -n '"[a-zA-Z]+\s*+\s*[a-zA-Z]' generated/*.html || true[0m
[38;2;255;255;255;48;2;19;87;20m+    - grep -n '\''function '\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;19;87;20m+    - grep -nE '\''"[a-zA-Z]+\s*\+\s*[a-zA-Z]'\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;19;87;20m+    - grep -n '\''\bvar\b'\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;19;87;20m+    postverify:[0m
[38;2;255;255;255;48;2;19;87;20m+      enabled: true[0m
[38;2;255;255;255;48;2;19;87;20m+      format: compact_table[0m
[38;2;255;255;255;48;2;19;87;20m+      header: "FILENAME | STATUS | REASON"[0m
[38;2;255;255;255;48;2;19;87;20m+      separator: "|"[0m
[38;2;255;255;255;48;2;19;87;20m+      rules:[0m
[38;2;255;255;255;48;2;19;87;20m+      - check: "diff_output"[0m
[38;2;255;255;255;48;2;19;87;20m+        action: "exit_code_only"[0m
[38;2;255;255;255;48;2;19;87;20m+        strip_ansi: true[0m
[38;2;255;255;255;48;2;19;87;20m+        max_lines: 0[0m
[38;2;255;255;255;48;2;19;87;20m+      - check: "summary_rollup"[0m
[38;2;255;255;255;48;2;19;87;20m+        action: "count_pass_fail"[0m
[38;2;255;255;255;48;2;19;87;20m+        output: "single_line"[0m
[38;2;184;134;11m   version: 9.0.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\desktop-mockup-artist\config.yaml → b/StydeAgents\blueprints\desktop-mockup-artist\config.yaml[0m
[38;2;139;134;130m@@ -21,9 +21,9 @@[0m
[38;2;184;134;11m     - css_custom_properties_for_repeated_values[0m
[38;2;184;134;11m     - unambiguous_labels_and_units[0m
[38;2;184;134;11m     pre_submit_commands:[0m
[38;2;255;255;255;48;2;119;20;20m-    - grep -n '\''function '\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;119;20;20m-    - grep -nE '\''"[a-zA-Z]+\s*\+\s*[a-zA-Z]'\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;119;20;20m-    - grep -n '\''\bvar\b'\'' generated/*.html || true[0m
[38;2;255;255;255;48;2;19;87;20m+    - "grep -n 'function ' generated/*.html || true"[0m
[38;2;255;255;255;48;2;19;87;20m+    - 'grep -nE ''"[a-zA-Z]+\s*\+\s*[a-zA-Z]'' generated/*.html || true'[0m
[38;2;255;255;255;48;2;19;87;20m+    - "grep -nw 'var' generated/*.html || true"[0m
[38;2;184;134;11m     postverify:[0m
[38;2;184;134;11m       enabled: true[0m
[38;2;184;134;11m       format: compact_table[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-desktop-mockup-artist.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-desktop-mockup-artist.py[0m
[38;2;139;134;130m@@ -0,0 +1,96 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: desktop-mockup-artist blueprint + config changes."""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, re, json, tempfile, shutil[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\config.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 1. BLUEPRINT.md checks ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must NOT contain standalone "## Verification Checklist" (the old one)[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification Checklist" in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Old '## Verification Checklist' section still present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must have merged "## Verification" (singular) with two sub-headings[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification\n" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing merged '## Verification' section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "### Runtime Verification Protocol (post-build)" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing Runtime Verification Protocol sub-section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "### Pre-Submission Static Checklist" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing Pre-Submission Static Checklist sub-section")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must specify compact single-line-per-file output format[0m
[38;2;255;255;255;48;2;19;87;20m+if "FILENAME | PASS|FAIL | reason" not in bp and "single-line-per-file" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing compact output format specification")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must have pre-submission lint instructions[0m
[38;2;255;255;255;48;2;19;87;20m+if "Pre-submission style lint" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing pre-submission style lint instructions")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must NOT have old Verification Protocol (singular heading)[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification Protocol\n" in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Old '## Verification Protocol' section still present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 2. Config.yaml checks ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must have postverify section[0m
[38;2;255;255;255;48;2;19;87;20m+if "postverify:" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | Missing postverify section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "compact_table" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must use compact_table format")[0m
[38;2;255;255;255;48;2;19;87;20m+if "exit_code_only" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must have exit_code_only check")[0m
[38;2;255;255;255;48;2;19;87;20m+if "strip_ansi: true" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must strip ANSI")[0m
[38;2;255;255;255;48;2;19;87;20m+if "single_line" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must have single_line summary")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# pre_submit_commands must have proper quoting (double or single quoted in YAML)[0m
[38;2;255;255;255;48;2;19;87;20m+# Find the pre_submit_commands block[0m
[38;2;255;255;255;48;2;19;87;20m+psc_match = re.search(r"pre_submit_commands:\n((?:    - .+\n?)+)", cfg)[0m
[38;2;255;255;255;48;2;19;87;20m+if psc_match:[0m
[38;2;255;255;255;48;2;19;87;20m+    psc_block = psc_match.group(1)[0m
[38;2;255;255;255;48;2;19;87;20m+    lines = [l.strip() for l in psc_block.split("\n") if l.strip()][0m
[38;2;255;255;255;48;2;19;87;20m+    # Each line must start with '- "' or "- '" or similar YAML quoting[0m
[38;2;255;255;255;48;2;19;87;20m+    for i, line in enumerate(lines):[0m
[38;2;255;255;255;48;2;19;87;20m+        # Map: strip leading "- " to get the value[0m
[38;2;255;255;255;48;2;19;87;20m+        val = line[2:].strip() if line.startswith("- ") else line.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+        if not (val.startswith('"') and val.endswith('"')) and not (val.startswith("'") and val.endswith("'")):[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"FAIL | config.yaml | pre_submit_command #{i+1} not YAML-quoted: {val[:40]}")[0m
[38;2;255;255;255;48;2;19;87;20m+        # Must contain 'function ' or 'var' or string concat pattern[0m
[38;2;255;255;255;48;2;19;87;20m+        has_pattern = any(kw in val for kw in ['function', 'var', '[a-zA-Z]'])[0m
[38;2;255;255;255;48;2;19;87;20m+        if not has_pattern:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"FAIL | config.yaml | pre_submit_command #{i+1} missing expected pattern")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | Missing pre_submit_commands block")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 3. YAML parseability check ─────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        parsed = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_info = parsed.get("blueprint", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    val = bp_info.get("validation", {})[0m
[38;2;139;134;130m… omitted 18 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-desktop-mockup-artist.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-desktop-mockup-artist.py[0m
[38;2;139;134;130m@@ -0,0 +1,80 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: desktop-mockup-artist blueprint + config changes."""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\desktop-mockup-artist\config.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 1. BLUEPRINT.md checks ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification Checklist" in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Old standalone '## Verification Checklist' still present")[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification\n" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing merged '## Verification' section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "### Runtime Verification Protocol (post-build)" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing Runtime Verification Protocol sub-section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "### Pre-Submission Static Checklist" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing Pre-Submission Static Checklist sub-section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "FILENAME | PASS|FAIL | reason" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing compact output format spec")[0m
[38;2;255;255;255;48;2;19;87;20m+if "Pre-submission style lint" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Missing pre-submission style lint")[0m
[38;2;255;255;255;48;2;19;87;20m+if "## Verification Protocol\n" in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | BLUEPRINT.md | Old '## Verification Protocol' still present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 2. Config.yaml checks ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "postverify:" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | Missing postverify section")[0m
[38;2;255;255;255;48;2;19;87;20m+if "compact_table" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must use compact_table")[0m
[38;2;255;255;255;48;2;19;87;20m+if "exit_code_only" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must have exit_code_only")[0m
[38;2;255;255;255;48;2;19;87;20m+if "strip_ansi: true" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must strip ANSI")[0m
[38;2;255;255;255;48;2;19;87;20m+if "single_line" not in cfg:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | postverify must have single_line summary")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+psc_match = re.search(r"pre_submit_commands:\n((?:    - .+\n?)+)", cfg)[0m
[38;2;255;255;255;48;2;19;87;20m+if psc_match:[0m
[38;2;255;255;255;48;2;19;87;20m+    lines = [l.strip() for l in psc_match.group(1).split("\n") if l.strip()][0m
[38;2;255;255;255;48;2;19;87;20m+    for i, line in enumerate(lines):[0m
[38;2;255;255;255;48;2;19;87;20m+        val = line[2:].strip() if line.startswith("- ") else line.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+        if not (val.startswith('"') and val.endswith('"')) and not (val.startswith("'") and val.endswith("'")):[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"FAIL | config.yaml | pre_submit_command #{i+1} not YAML-quoted: {val[:50]}")[0m
[38;2;255;255;255;48;2;19;87;20m+        has_kw = any(kw in val for kw in ['function', 'var', '[a-zA-Z]'])[0m
[38;2;255;255;255;48;2;19;87;20m+        if not has_kw:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"FAIL | config.yaml | pre_submit_command #{i+1} missing expected pattern")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("FAIL | config.yaml | Missing pre_submit_commands block")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 3. YAML parse check ────────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        parsed = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    pv = parsed.get("blueprint", {}).get("validation", {}).get("postverify", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if not pv.get("enabled"):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("FAIL | config.yaml | postverify.enabled not true in parsed YAML")[0m
[38;2;255;255;255;48;2;19;87;20m+    if pv.get("format") != "compact_table":[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("FAIL | config.yaml | postverify.format != compact_table")[0m
[38;2;255;255;255;48;2;19;87;20m+except ImportError:[0m
[38;2;255;255;255;48;2;19;87;20m+    pass[0m
[38;2;255;255;255;48;2;19;87;20m+except yaml.YAMLError as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"FAIL | config.yaml | YAML parse error: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── Results ─────────────────────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(e)[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"\nTOTAL: {len(errors)} failures")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("ALL PASS | 0 failures")[0m
[38;2;139;134;130m… omitted 2 diff line(s) across 1 additional file(s)/section(s)[0m
**Ad-hoc verification: ALL PASS | 0 failures**
Verifieringsskript kvar på `C:\Users\Pontus\AppData\Local\Temp\hermes-verify-desktop-mockup-artist.py`.
Sammanfattning av vad som kontrollerades:
| Check | Result |
|---|---|
| BLUEPRINT: inget kvarvarande gammalt `## Verification Checklist` | PASS |
| BLUEPRINT: merged `## Verification` med båda sub-sektioner | PASS |
| BLUEPRINT: `FILENAME \| PASS\|FAIL \| reason` output-spec | PASS |
| BLUEPRINT: pre-submission style lint instruktion | PASS |
| BLUEPRINT: ingen gammal `## Verification Protocol` kvar | PASS |
| config.yaml: `postverify` sektion med alla delar | PASS |
| config.yaml: `pre_submit_commands` YAML-quoted + har mönster | PASS |
| config.yaml: YAML-struktur parsebar, `postverify.enabled: true` | PASS |
Detta är ad-hoc verifiering, inte ett formellt test-suite. Ändringarna är strukturellt korrekta och matchar all tre feedbackpunkter.