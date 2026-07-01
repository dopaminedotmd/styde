┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\data-cleaner\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\data-cleaner\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,9 @@[0m
[38;2;184;134;11m - Report: what was found, what was fixed, what needs manual review[0m
[38;2;184;134;11m - Preserve: original data, log all changes[0m
[38;2;184;134;11m - Handle: CSV, Excel, TSV formats[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Missing-Input Fallback[0m
[38;2;255;255;255;48;2;19;87;20m+When the user has not provided a data file or spreadsheet data:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Offer to scan the current working directory for matching data files (.csv, .xlsx, .tsv, .json)[0m
[38;2;255;255;255;48;2;19;87;20m+2. Show a paste-this-format example (e.g. `name,email,age` with 2-3 sample rows) so the user can paste inline[0m
[38;2;255;255;255;48;2;19;87;20m+3. Accept a file path argument and read from it directly. If none of these work, ask the user what format they prefer — do not abort with an error[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\data-cleaner\persona.md → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\data-cleaner\persona.md[0m
[38;2;139;134;130m@@ -6,3 +6,4 @@[0m
[38;2;184;134;11m - Report: what was found, what was fixed, what needs manual review[0m
[38;2;184;134;11m - Preserve: original data, log all changes[0m
[38;2;184;134;11m - Handle: CSV, Excel, TSV formats[0m
[38;2;255;255;255;48;2;19;87;20m+- When the user has not provided all required data, do NOT stop with an error message. Instead, immediately offer the user concrete ways to provide it (paste inline, point at a file, use the format shown)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-data-cleaner-blueprint.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-data-cleaner-blueprint.py[0m
[38;2;139;134;130m@@ -0,0 +1,52 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: Data Cleaner blueprint missing-input fallback changes."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\data-cleaner"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(BASE, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(bp_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"BLUEPRINT.md not found at {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(bp_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    checks_bp = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Missing-Input Fallback heading", "## Missing-Input Fallback"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("alternative 1: scan cwd", "scan the current working directory"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("alternative 2: paste format example", "paste-this-format example"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("alternative 3: file path argument", "file path argument"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("do not abort with an error", "do not abort with an error"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, needle in checks_bp:[0m
[38;2;255;255;255;48;2;19;87;20m+        if needle not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT.md missing: {name} ('{needle}')")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- persona.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+p_path = os.path.join(BASE, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(p_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"persona.md not found at {p_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(p_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        p = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    checks_p = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("do NOT stop with an error message", "do NOT stop with an error message"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("offer concrete ways", "immediately offer the user concrete ways"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("paste inline", "paste inline"),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("point at a file", "point at a file"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, needle in checks_p:[0m
[38;2;255;255;255;48;2;19;87;20m+        if needle not in p:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"persona.md missing: {name} ('{needle}')")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Result ---[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: {len(errors)} check(s) failed")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  - {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("PASS: all 9 checks passed (3 alternatives + heading + abort guard in BLUEPRINT.md, 4 constraints in persona.md)")[0m
ad-hoc verification: 9/9 checks pass. Cleaned upp temp-skriptet.
BLUEPRINT.md: sektionen Missing-Input Fallback finns med alla tre alternativen (scan cwd, paste-format-exempel, file path) + explicit "do not abort with an error".
persona.md: constraint att inte stoppa med felmeddelande, istället direkt erbjuda konkreta sätt att leverera data.