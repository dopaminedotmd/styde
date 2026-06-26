┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\rate-limiting-engineer\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\rate-limiting-engineer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -20,3 +20,13 @@[0m
[38;2;184;134;11m - Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset[0m
[38;2;184;134;11m - HTTP 429: proper Retry-After header, informative error body[0m
[38;2;184;134;11m - Override: admin bypass capability for debugging[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Quality Gate — Mandatory Pre-Finalization Checklist[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Before shipping any code implementation, run through all three:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+1. None/TypeError trace: Walk every code path and verify no function returns None where an int/str/dict is expected. Check that `remaining`, `limit`, `reset` are always populated before being passed to headers or response bodies. Pay special attention to edge cases: first request on empty bucket, burst exhaustion, admin bypass fast-path.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+2. Decorator syntax verification: For each decorator, mentally inline it against the function it wraps. Verify the decorator factory returns a callable that takes (func) and returns a wrapped callable with the same signature. Check for missing parentheses, wrong argument counts, and `@decorator` vs `@decorator()` mismatches.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+3. Import discipline: All imports at module level, never inside function bodies. Confirm `json`, `time`, `threading`, `dataclasses`, and any stdlib/third-party modules used anywhere in the code are imported at the top of the file. Check for implicit imports (e.g. `json.dumps` without `import json`).[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\rate-limiting-engineer\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\rate-limiting-engineer\persona.md[0m
[38;2;139;134;130m@@ -8,3 +8,4 @@[0m
[38;2;184;134;11m - HTTP 429: proper Retry-After header, informative JSON error body[0m
[38;2;184;134;11m - Override: admin bypass capability for debugging and testing[0m
[38;2;184;134;11m - Python: implement as decorator or middleware for easy integration[0m
[38;2;255;255;255;48;2;19;87;20m+- Code review: After writing any code block, trace through every code path looking for None returns, missing imports, and invalid Python syntax before submitting. Do not ship a single function without this verification pass.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-rate-limit-docs.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-rate-limit-docs.py[0m
[38;2;139;134;130m@@ -0,0 +1,61 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: rate-limiting-engineer blueprint docs.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Checks that teacher feedback changes were correctly applied:[0m
[38;2;255;255;255;48;2;19;87;20m+1. BLUEPRINT.md has the Quality Gate checklist with 3 items[0m
[38;2;255;255;255;48;2;19;87;20m+2. persona.md has the code review trace instruction[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+import os[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+base = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\rate-limiting-engineer"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(base, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must have the Quality Gate section[0m
[38;2;255;255;255;48;2;19;87;20m+if "Quality Gate" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: missing 'Quality Gate' section heading")[0m
[38;2;255;255;255;48;2;19;87;20m+if "None/TypeError trace" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: missing 'None/TypeError trace' checklist item")[0m
[38;2;255;255;255;48;2;19;87;20m+if "Decorator syntax verification" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: missing 'Decorator syntax verification' checklist item")[0m
[38;2;255;255;255;48;2;19;87;20m+if "Import discipline" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: missing 'Import discipline' checklist item")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Must mention the specific bugs from feedback[0m
[38;2;255;255;255;48;2;19;87;20m+if "remaining" not in bp or "limit" not in bp or "reset" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: should mention specific header fields (remaining, limit, reset)")[0m
[38;2;255;255;255;48;2;19;87;20m+if "admin bypass" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md: should mention admin bypass edge case")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- persona.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+pm_path = os.path.join(base, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(pm_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    pm = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "Code review:" not in pm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'Code review:' rule")[0m
[38;2;255;255;255;48;2;19;87;20m+if "trace through every code path" not in pm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing trace instruction")[0m
[38;2;255;255;255;48;2;19;87;20m+if "None returns" not in pm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'None returns' in trace instruction")[0m
[38;2;255;255;255;48;2;19;87;20m+if "missing imports" not in pm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'missing imports' in trace instruction")[0m
[38;2;255;255;255;48;2;19;87;20m+if "invalid Python syntax" not in pm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'invalid Python syntax' in trace instruction")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Summary ---[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: {len(errors)} issue(s) found")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  - {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("PASS: All teacher feedback changes verified in both docs")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  BLUEPRINT.md: {len(bp.splitlines())} lines, Quality Gate section present")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  persona.md: {len(pm.splitlines())} lines, code review rule present")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(0)[0m
Ad-hoc verification: PASS
Ran targeted content audit via temp script. Confirmed:
- BLUEPRINT.md: Quality Gate section present with all 3 checklist items (None/TypeError trace, Decorator syntax verification, Import discipline)
- persona.md: Code review rule present with full trace instruction covering None returns, missing imports, and invalid Python syntax
Temp script cleaned up. This is documentation-only verification — no runtime code exists to execute.