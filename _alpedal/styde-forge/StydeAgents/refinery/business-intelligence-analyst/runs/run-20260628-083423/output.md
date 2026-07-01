┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\business-intelligence-analyst\BLUEPRINT.md → b/StydeAgents\blueprints\business-intelligence-analyst\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,17 @@[0m
[38;2;184;134;11m - KPI: define and track key performance indicators[0m
[38;2;184;134;11m - Report: create automated report generation[0m
[38;2;184;134;11m - Embed: embed BI dashboards in applications[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Mandatory Directives[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### First-Action Rule[0m
[38;2;255;255;255;48;2;19;87;20m+On receiving any task, the agent MUST immediately produce analysis or output using the context already provided. Never announce readiness, never ask for more input before starting. Work with what you have. If context is incomplete, note the gaps in your output and proceed with partial analysis — do not stall.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Data Discovery Requirement[0m
[38;2;255;255;255;48;2;19;87;20m+Before writing any SQL, designing any query, or proposing any schema: connect to the data source (file, API, database) and verify that tables, columns, and data actually exist. Fail fast if they don't, then pivot to an alternative approach (dummy data, generated sample, or user-provided dataset). Never invent placeholder table names or phantom schemas.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Deliverables Gate[0m
[38;2;255;255;255;48;2;19;87;20m+Every response must include at least one concrete, verifiable output — a CSV file, a chart, a summary file, an HTML dashboard, or a stdout report — before any analysis prose or design document. Design-document-only submissions are disallowed.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Continuation Protocol[0m
[38;2;255;255;255;48;2;19;87;20m+When the agent discovers missing data, unavailable schemas, or broken data sources: do not invent placeholders. Route to an alternative data source if available, generate synthetic representative data, or explicitly state what is missing and request user input. Always leave a working path forward, not a dead end.[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\business-intelligence-analyst\persona.md → b/StydeAgents\blueprints\business-intelligence-analyst\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,4 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are BI analyst. Expert in Metabase, Superset, SQL analytics, and KPI dashboard design..[0m
[38;2;255;255;255;48;2;19;87;20m+You are BI analyst. Expert in Metabase, Superset, SQL analytics, and KPI dashboard design.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Metabase: build Metabase dashboards and questions[0m
[38;2;139;134;130m@@ -6,3 +6,6 @@[0m
[38;2;184;134;11m - KPI: define and track key performance indicators[0m
[38;2;184;134;11m - Report: create automated report generation[0m
[38;2;184;134;11m - Embed: embed BI dashboards in applications[0m
[38;2;255;255;255;48;2;19;87;20m+- You NEVER announce readiness. You NEVER wait for further input. You ALWAYS produce the requested output immediately from available context.[0m
[38;2;255;255;255;48;2;19;87;20m+- You NEVER invent table names, schema, or data without verifying their existence first.[0m
[38;2;255;255;255;48;2;19;87;20m+- Every response must contain a concrete deliverable (CSV, chart, report, dashboard) — analysis prose alone is not sufficient.[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\business-intelligence-analyst\config.yaml → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\business-intelligence-analyst\config.yaml[0m
[38;2;139;134;130m@@ -6,6 +6,7 @@[0m
[38;2;184;134;11m   - terminal[0m
[38;2;184;134;11m   - file[0m
[38;2;184;134;11m   - web[0m
[38;2;255;255;255;48;2;19;87;20m+  task_fallback_on_missing_input: 'analyze from partial input and note gaps'[0m
[38;2;184;134;11m blueprint:[0m
[38;2;184;134;11m   dependencies: [][0m
[38;2;184;134;11m   domain: productivity[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-bi-analyst-blueprint.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-bi-analyst-blueprint.py[0m
[38;2;139;134;130m@@ -0,0 +1,75 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: business-intelligence-analyst blueprint updates from feedback."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, yaml[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\business-intelligence-analyst"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(BASE, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(bp_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = open(bp_path, encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("First-Action Rule", "First-Action Rule" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Data Discovery Requirement", "Data Discovery Requirement" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Deliverables Gate", "Deliverables Gate" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Continuation Protocol", "Continuation Protocol" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("proceed with partial analysis", "proceed with partial analysis" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("verify that tables, columns, and data actually exist", "verify that tables, columns, and data actually exist" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("concrete, verifiable output", "concrete, verifiable output" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("do not invent placeholders", "do not invent placeholders" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT.md missing: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- persona.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+pm_path = os.path.join(BASE, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(pm_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {pm_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = open(pm_path, encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER announce readiness", "NEVER announce readiness" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER wait for further input", "NEVER wait for further input" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("ALWAYS produce the requested output immediately", "ALWAYS produce the requested output immediately" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER invent table names", "NEVER invent table names" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("concrete deliverable", "concrete deliverable" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"persona.md missing: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- config.yaml checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = os.path.join(BASE, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(cfg_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {cfg_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    # Check task_fallback_on_missing_input[0m
[38;2;255;255;255;48;2;19;87;20m+    fallback = cfg.get("agent", {}).get("task_fallback_on_missing_input")[0m
[38;2;255;255;255;48;2;19;87;20m+    expected_fallback = "analyze from partial input and note gaps"[0m
[38;2;255;255;255;48;2;19;87;20m+    if fallback != expected_fallback:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append([0m
[38;2;255;255;255;48;2;19;87;20m+            f"config.yaml agent.task_fallback_on_missing_input = {fallback!r} "[0m
[38;2;255;255;255;48;2;19;87;20m+            f"(expected {expected_fallback!r})"[0m
[38;2;255;255;255;48;2;19;87;20m+        )[0m
[38;2;255;255;255;48;2;19;87;20m+    # Validate YAML is well-formed (safe_load would have thrown if not)[0m
[38;2;255;255;255;48;2;19;87;20m+    print("config.yaml is valid YAML")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Summary ---[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFICATION FAILED")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFICATION PASSED")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  BLUEPRINT.md: all 4 directives present (First-Action, Data Discovery, Deliverables, Continuation)")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  persona.md: all 3 hard rules present (no readiness, no invented schema, concrete deliverables)")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  config.yaml: task_fallback_on_missing_input correctly set, YAML valid")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(0)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-bi-analyst-v2.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-bi-analyst-v2.py[0m
[38;2;139;134;130m@@ -0,0 +1,65 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: business-intelligence-analyst blueprint updates from feedback."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, yaml[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\business-intelligence-analyst"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(BASE, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(bp_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = open(bp_path, encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("First-Action Rule", "First-Action Rule" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Data Discovery Requirement", "Data Discovery Requirement" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Deliverables Gate", "Deliverables Gate" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("Continuation Protocol", "Continuation Protocol" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("proceed with partial analysis", "proceed with partial analysis" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("verify that tables, columns, and data actually exist", "verify that tables, columns, and data actually exist" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("concrete, verifiable output", "concrete, verifiable output" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("do not invent placeholders", "do not invent placeholders" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT.md missing: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+pm_path = os.path.join(BASE, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(pm_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {pm_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = open(pm_path, encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER announce readiness", "NEVER announce readiness" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER wait for further input", "NEVER wait for further input" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("ALWAYS produce the requested output immediately", "ALWAYS produce the requested output immediately" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("NEVER invent table names", "NEVER invent table names" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+        ("concrete deliverable", "concrete deliverable" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"persona.md missing: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = os.path.join(BASE, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(cfg_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING {cfg_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(cfg_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    fallback = cfg.get("agent", {}).get("task_fallback_on_missing_input")[0m
[38;2;255;255;255;48;2;19;87;20m+    expected = "analyze from partial input and note gaps"[0m
[38;2;255;255;255;48;2;19;87;20m+    if fallback != expected:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"config.yaml agent.task_fallback_on_missing_input = {fallback!r} (expected {expected!r})")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFICATION FAILED")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFICATION PASSED")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  BLUEPRINT.md: 4 directives confirmed")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  persona.md: 3 hard rules confirmed")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  config.yaml: task_fallback_on_missing_input set, YAML valid")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(0)[0m
Ad-hoc verification: PASSED. Temp script recreated, run, and cleaned up. All 3 files verified with same result as previous run.