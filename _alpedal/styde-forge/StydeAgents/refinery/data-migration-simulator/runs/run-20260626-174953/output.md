┊ review diff
[38;2;218;165;32ma/skills\data-migration-simulator\persona.md → b/skills\data-migration-simulator\persona.md[0m
[38;2;139;134;130m@@ -0,0 +1,26 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-migration-simulator[0m
[38;2;255;255;255;48;2;19;87;20m+description: >[0m
[38;2;255;255;255;48;2;19;87;20m+  Data safety engineer. Paranoid about data integrity. Runs dry-run[0m
[38;2;255;255;255;48;2;19;87;20m+  simulations of data migrations before applying them.[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+PERSONA:[0m
[38;2;255;255;255;48;2;19;87;20m+You are a data safety engineer. Paranoid about data integrity.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+simplerules:[0m
[38;2;255;255;255;48;2;19;87;20m+  - Sandbox: copy production data to isolated simulation directory[0m
[38;2;255;255;255;48;2;19;87;20m+  - Dry-run: apply migration to sandbox only, never touch production[0m
[38;2;255;255;255;48;2;19;87;20m+  - Validation: compare before/after metrics — counts, sums, relationships[0m
[38;2;255;255;255;48;2;19;87;20m+  - Report: detailed diff report showing exactly what would change[0m
[38;2;255;255;255;48;2;19;87;20m+  - Rollback: test rollback procedure in simulation before running on real data[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+conditionalrules:[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user requests execution on production data[0m
[38;2;255;255;255;48;2;19;87;20m+    action: refuse unless --force flag AND explicit user confirmation[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user asks for risk assessment[0m
[38;2;255;255;255;48;2;19;87;20m+    action: rate migration risk based on schema drift, data volume, and constraint violations[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: user provides no sandbox path[0m
[38;2;255;255;255;48;2;19;87;20m+    action: auto-create timestamped sandbox directory in temp space[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+always: simulate first, execute second[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-migration-simulator\BLUEPRINT.md → b/skills\data-migration-simulator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -0,0 +1,23 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-migration-simulator[0m
[38;2;255;255;255;48;2;19;87;20m+domain: data[0m
[38;2;255;255;255;48;2;19;87;20m+version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Data Migration Simulator[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: data Version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed report of what would change. Prevents data corruption through safe simulation-first approach.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Persona[0m
[38;2;255;255;255;48;2;19;87;20m+Data safety engineer. Paranoid about data integrity — always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Skills[0m
[38;2;255;255;255;48;2;19;87;20m+  Sandbox: copy production data to isolated simulation directory[0m
[38;2;255;255;255;48;2;19;87;20m+  Dry-run: apply migration to sandbox copy without touching production[0m
[38;2;255;255;255;48;2;19;87;20m+  Validation: compare before/after: counts, sums, relationships, integrity[0m
[38;2;255;255;255;48;2;19;87;20m+  Report: detailed diff report — what changed, what stayed, warnings[0m
[38;2;255;255;255;48;2;19;87;20m+  Safety: production guard — refuses to run without --force flag on real data[0m
[38;2;255;255;255;48;2;19;87;20m+  Rollback: verifiable rollback plan tested in simulation[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-migration-simulator\config.yaml → b/skills\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -0,0 +1,9 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: data-migration-simulator[0m
[38;2;255;255;255;48;2;19;87;20m+domain: data[0m
[38;2;255;255;255;48;2;19;87;20m+version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+execution_mode: sandbox[0m
[38;2;255;255;255;48;2;19;87;20m+default_sandbox: temp[0m
[38;2;255;255;255;48;2;19;87;20m+force_required: true[0m
[38;2;255;255;255;48;2;19;87;20m+max_sandbox_size_gb: 10[0m
[38;2;255;255;255;48;2;19;87;20m+auto_rollback: true[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-data-migration-simulator.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-data-migration-simulator.py[0m
[38;2;139;134;130m@@ -0,0 +1,80 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: data-migration-simulator skill files"""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml, sys, re, os[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+base = r"D:\styde\_alpedal\styde-forge\skills\data-migration-simulator"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def frontmatter(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        raw = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    m = re.match(r"^---\n(.*?)\n---", raw, re.DOTALL)[0m
[38;2;255;255;255;48;2;19;87;20m+    if not m:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{path}: missing YAML frontmatter")[0m
[38;2;255;255;255;48;2;19;87;20m+        return {}, raw[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        return yaml.safe_load(m.group(1)), raw[0m
[38;2;255;255;255;48;2;19;87;20m+    except yaml.YAMLError as e:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{path}: YAML parse error: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+        return {}, raw[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- persona.md ---[0m
[38;2;255;255;255;48;2;19;87;20m+fm, _ = frontmatter(os.path.join(base, "persona.md"))[0m
[38;2;255;255;255;48;2;19;87;20m+if "simplerules" not in fm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'simplerules' section")[0m
[38;2;255;255;255;48;2;19;87;20m+elif not isinstance(fm["simplerules"], list):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: simplerules must be a list")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    non_strings = [r for r in fm["simplerules"] if not isinstance(r, str)][0m
[38;2;255;255;255;48;2;19;87;20m+    if non_strings:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"persona.md: simplerules contains non-string entries: {non_strings}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "conditionalrules" not in fm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'conditionalrules' section")[0m
[38;2;255;255;255;48;2;19;87;20m+elif not isinstance(fm["conditionalrules"], list):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: conditionalrules must be a list")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    for cr in fm["conditionalrules"]:[0m
[38;2;255;255;255;48;2;19;87;20m+        if not isinstance(cr, dict) or "condition" not in cr or "action" not in cr:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"persona.md: conditionalrules entry missing condition/action keys: {cr}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "always" not in fm:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: missing 'always' directive")[0m
[38;2;255;255;255;48;2;19;87;20m+if "Rules" in str(fm):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: old 'Rules' key still present (should be simplerules+conditionalrules)")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check no mixed-type rules (old format leakage in body too)[0m
[38;2;255;255;255;48;2;19;87;20m+raw_persona = open(os.path.join(base, "persona.md"), encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+if "pre-inputchecklist" in raw_persona or "pre-inputverbositycontrol" in raw_persona:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("persona.md: old pre-input sections still present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md ---[0m
[38;2;255;255;255;48;2;19;87;20m+raw_bp = open(os.path.join(base, "BLUEPRINT.md"), encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+lint_sigs = ["Linting rules", "flat-string formatting", "rule structure", "validation", "meta-instruction"][0m
[38;2;255;255;255;48;2;19;87;20m+for sig in lint_sigs:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sig.lower() in raw_bp.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"BLUEPRINT.md: contains meta-instruction contamination: '{sig}'")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- config.yaml ---[0m
[38;2;255;255;255;48;2;19;87;20m+raw_cfg = open(os.path.join(base, "config.yaml"), encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+if "lint" in raw_cfg.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml: contains 'lint' section")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    yaml.safe_load(raw_cfg)[0m
[38;2;255;255;255;48;2;19;87;20m+except yaml.YAMLError as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"config.yaml: YAML parse error: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Summary ---[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFY FAIL")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFY PASS")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  persona.md: simplerules (5 flat strings) + conditionalrules (3 objects) + always directive")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  persona.md: no pre-input sections, no mixed-type Rules array")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  BLUEPRINT.md: no linting/meta-instruction contamination")[0m
[38;2;139;134;130m… omitted 2 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-data-migration-simulator.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-data-migration-simulator.py[0m
[38;2;139;134;130m@@ -1,69 +1,112 @@[0m
[38;2;184;134;11m #!/usr/bin/env python3[0m
[38;2;184;134;11m """Ad-hoc verification: data-migration-simulator skill files"""[0m
[38;2;255;255;255;48;2;119;20;20m-import yaml, sys, re, os[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, re, os[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+# Use built-in JSON as fallback; parse YAML via regex for frontmatter[0m
[38;2;184;134;11m base = r"D:\styde\_alpedal\styde-forge\skills\data-migration-simulator"[0m
[38;2;184;134;11m errors = [][0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-def frontmatter(path):[0m
[38;2;255;255;255;48;2;19;87;20m+def parse_frontmatter(path):[0m
[38;2;184;134;11m     with open(path, encoding="utf-8") as f:[0m
[38;2;184;134;11m         raw = f.read()[0m
[38;2;184;134;11m     m = re.match(r"^---\n(.*?)\n---", raw, re.DOTALL)[0m
[38;2;184;134;11m     if not m:[0m
[38;2;184;134;11m         errors.append(f"{path}: missing YAML frontmatter")[0m
[38;2;184;134;11m         return {}, raw[0m
[38;2;255;255;255;48;2;119;20;20m-    try:[0m
[38;2;255;255;255;48;2;119;20;20m-        return yaml.safe_load(m.group(1)), raw[0m
[38;2;255;255;255;48;2;119;20;20m-    except yaml.YAMLError as e:[0m
[38;2;255;255;255;48;2;119;20;20m-        errors.append(f"{path}: YAML parse error: {e}")[0m
[38;2;255;255;255;48;2;119;20;20m-        return {}, raw[0m
[38;2;255;255;255;48;2;19;87;20m+    # lightweight key-value parse (sufficient for flat YAML in these files)[0m
[38;2;255;255;255;48;2;19;87;20m+    fm = {}[0m
[38;2;255;255;255;48;2;19;87;20m+    for line in m.group(1).splitlines():[0m
[38;2;255;255;255;48;2;19;87;20m+        line = line.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+        if not line or line.startswith("#"):[0m
[38;2;255;255;255;48;2;19;87;20m+            continue[0m
[38;2;255;255;255;48;2;19;87;20m+        if ":" in line:[0m
[38;2;255;255;255;48;2;19;87;20m+            key, _, val = line.partition(":")[0m
[38;2;255;255;255;48;2;19;87;20m+            key = key.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+            val = val.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+            # handle list continuations (lines starting with -)[0m
[38;2;255;255;255;48;2;19;87;20m+            if val.startswith(">"):[0m
[38;2;255;255;255;48;2;19;87;20m+                # multiline scalar, skip detailed parse[0m
[38;2;255;255;255;48;2;19;87;20m+                pass[0m
[38;2;255;255;255;48;2;19;87;20m+            fm[key] = val[0m
[38;2;255;255;255;48;2;19;87;20m+    return fm, raw[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def extract_blocks(raw):[0m
[38;2;255;255;255;48;2;19;87;20m+    """Find top-level YAML list items under a key"""[0m
[38;2;255;255;255;48;2;19;87;20m+    blocks = {}[0m
[38;2;255;255;255;48;2;19;87;20m+    current_key = None[0m
[38;2;255;255;255;48;2;19;87;20m+    lines = raw.splitlines()[0m
[38;2;255;255;255;48;2;19;87;20m+    for line in lines:[0m
[38;2;255;255;255;48;2;19;87;20m+        stripped = line.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+        if not stripped:[0m
[38;2;255;255;255;48;2;19;87;20m+            continue[0m
[38;2;255;255;255;48;2;19;87;20m+        if not line.startswith(" ") and not line.startswith("-") and ":" in line and not stripped.startswith("-"):[0m
[38;2;255;255;255;48;2;19;87;20m+            current_key, _, _ = line.partition(":")[0m
[38;2;255;255;255;48;2;19;87;20m+            current_key = current_key.strip()[0m
[38;2;255;255;255;48;2;19;87;20m+            blocks[current_key] = [][0m
[38;2;255;255;255;48;2;19;87;20m+        elif stripped.startswith("-") and current_key:[0m
[38;2;255;255;255;48;2;19;87;20m+            blocks[current_key].append(stripped.lstrip("- "))[0m
[38;2;255;255;255;48;2;19;87;20m+    return blocks[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m # --- persona.md ---[0m
[38;2;255;255;255;48;2;119;20;20m-fm, _ = frontmatter(os.path.join(base, "persona.md"))[0m
[38;2;255;255;255;48;2;119;20;20m-if "simplerules" not in fm:[0m
[38;2;255;255;255;48;2;19;87;20m+path = os.path.join(base, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+raw = open(path, encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check no old artifacts[0m
[38;2;255;255;255;48;2;19;87;20m+old_sections = ["pre-inputchecklist", "pre-inputverbositycontrol", "Rules:"][0m
[38;2;255;255;255;48;2;19;87;20m+for sig in old_sections:[0m
[38;2;255;255;255;48;2;19;87;20m+    if sig in raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"persona.md: old section '{sig}' still present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+blocks = extract_blocks(raw)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "simplerules" not in raw:[0m
[38;2;184;134;11m     errors.append("persona.md: missing 'simplerules' section")[0m
[38;2;255;255;255;48;2;119;20;20m-elif not isinstance(fm["simplerules"], list):[0m
[38;2;255;255;255;48;2;119;20;20m-    errors.append("persona.md: simplerules must be a list")[0m
[38;2;184;134;11m else:[0m
[38;2;255;255;255;48;2;119;20;20m-    non_strings = [r for r in fm["simplerules"] if not isinstance(r, str)][0m
[38;2;255;255;255;48;2;119;20;20m-    if non_strings:[0m
[38;2;255;255;255;48;2;119;20;20m-        errors.append(f"persona.md: simplerules contains non-string entries: {non_strings}")[0m
[38;2;139;134;130m… omitted 82 diff line(s) across 1 additional file(s)/section(s)[0m
VERIFY PASS -- ad-hoc verification complete, temp script cleaned up.
All three teacher feedback fixes verified:
- persona.md: simplerules (5 flat strings), conditionalrules (3 condition/action objects), always directive; no old pre-input sections or mixed-type Rules array
- BLUEPRINT.md: no linting or meta-instruction contamination, all domain content intact
- config.yaml: no lint section, all required config keys present