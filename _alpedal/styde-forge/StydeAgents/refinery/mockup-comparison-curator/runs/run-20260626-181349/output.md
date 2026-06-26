┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md → b/StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -19,3 +19,36 @@[0m
[38;2;184;134;11m - Feedback: specific, actionable design critique per mockup[0m
[38;2;184;134;11m - Selection: recommends best desktop + best web mockup for implementation[0m
[38;2;184;134;11m - Output: structured markdown report with scores and recommendations[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Deliverable Integrity[0m
[38;2;255;255;255;48;2;19;87;20m+Every mockup under evaluation MUST tag each interactive element with its implementation status in a visible overlay or legend. Three statuses are allowed:[0m
[38;2;255;255;255;48;2;19;87;20m+- **functional**: the feature works with real data/state[0m
[38;2;255;255;255;48;2;19;87;20m+- **simulated**: the feature appears rendered but uses hardcoded/static data, no backend[0m
[38;2;255;255;255;48;2;19;87;20m+- **mock**: placeholder content only (lorem ipsum, grey boxes, wireframe blocks)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Annotate the status per element, not per page. Include a legend in the mockup HTML or a status table in the evaluation metadata. Any element lacking a status tag defaults to `mock`.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+This section exists to prevent the accuracy-inflation problem where non-functional or simulated mockups receive scores as though they were production-ready.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Implementation Details[0m
[38;2;255;255;255;48;2;19;87;20m+Each recommendation in the comparison report MUST include:[0m
[38;2;255;255;255;48;2;19;87;20m+1. **Code snippet**: a concrete, minimal code example showing the recommended change (HTML/CSS/JS as applicable)[0m
[38;2;255;255;255;48;2;19;87;20m+2. **Configuration block**: relevant config or setup (e.g. Tailwind theme extension, CSS custom properties, animation keyframes)[0m
[38;2;255;255;255;48;2;19;87;20m+3. **Technical trade-off analysis**: at least one pro and one con or risk for the recommendation (e.g. "declarative animation is easier to maintain but may not hit 60fps on mid-range GPUs")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+This applies to every scoring dimension where a recommendation is made. Recommendations without technical backing are omitted.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Format Constraints[0m
[38;2;255;255;255;48;2;19;87;20m+All comparison sections MUST use tabular or annotated-list format. Constraints:[0m
[38;2;255;255;255;48;2;19;87;20m+- **1 table per comparison** — one row per mockup, one column per scoring dimension[0m
[38;2;255;255;255;48;2;19;87;20m+- **Max 3 sentences per mockup-row** — no expanded breakdowns per dimension[0m
[38;2;255;255;255;48;2;19;87;20m+- **Status column** — collapse functional/simulated/mock into a single annotation column (e.g. `status: [F/S/M]` or `F:3,S:2,M:0`)[0m
[38;2;255;255;255;48;2;19;87;20m+- **No separate sub-sections** for functional, simulated, and mock categories — merge into one status annotation[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Violations: the output is rejected and regenerated.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Output Pipeline[0m
[38;2;255;255;255;48;2;19;87;20m+Before rendering the final report into persona.md or any downstream artifact:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Strip all ANSI escape codes from any diff output embedded in the report[0m
[38;2;255;255;255;48;2;19;87;20m+2. Use standard code fences with language tags for code blocks[0m
[38;2;255;255;255;48;2;19;87;20m+3. Replace any non-standard line-number prefixes (e.g. `|N|`) with conventional `@@` hunk headers[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\mockup-comparison-curator\persona.md → b/StydeAgents\blueprints\mockup-comparison-curator\persona.md[0m
[38;2;139;134;130m@@ -8,3 +8,5 @@[0m
[38;2;184;134;11m - Output: structured markdown report with scores and recommendations[0m
[38;2;184;134;11m - Knows what template/AI-generated designs look like — flags them immediately[0m
[38;2;184;134;11m - Prefers bold, original design decisions over safe, generic layouts[0m
[38;2;255;255;255;48;2;19;87;20m+- Honesty directive: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring[0m
[38;2;255;255;255;48;2;19;87;20m+- Concise analyst — prefers one dense table over three paragraphs[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\mockup-comparison-curator\config.yaml → b/StydeAgents\blueprints\mockup-comparison-curator\config.yaml[0m
[38;2;139;134;130m@@ -12,7 +12,7 @@[0m
[38;2;184;134;11m   name: mockup-comparison-curator[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;255;255;255;48;2;119;20;20m-  version: 6.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 7.0.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 2.0.0[0m
[38;2;139;134;130m@@ -50,3 +50,20 @@[0m
[38;2;184;134;11m     score: 90.0[0m
[38;2;184;134;11m     previous_score: 91.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T18:13:48Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 6.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 7.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: batch-fix applied all 11 pending changes from 4 feedback rounds (ANSI strip, implementation details, format constraints, deliverable integrity, functional verification gate, honesty directive, concise analyst trait, status column collapse)'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 90.0[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T20:13:00Z'[0m
[38;2;255;255;255;48;2;19;87;20m+functional_verification:[0m
[38;2;255;255;255;48;2;19;87;20m+  enabled: true[0m
[38;2;255;255;255;48;2;19;87;20m+  gate:[0m
[38;2;255;255;255;48;2;19;87;20m+    before_scoring: true[0m
[38;2;255;255;255;48;2;19;87;20m+    mandatory_checklist:[0m
[38;2;255;255;255;48;2;19;87;20m+      - for each mockup, create a checklist column marking every interactive element as 'working', 'simulated', or 'non-functional'[0m
[38;2;255;255;255;48;2;19;87;20m+      - no scoring may begin until the checklist is populated[0m
[38;2;255;255;255;48;2;19;87;20m+      - the checklist is attached to the evaluation report as an appendix[0m
[38;2;255;255;255;48;2;19;87;20m+    scoring_impact:[0m
[38;2;255;255;255;48;2;19;87;20m+      - any element marked 'non-functional' deducts 20% from the relevant accuracy/functionality component before scoring[0m
[38;2;255;255;255;48;2;19;87;20m+      - any element marked 'simulated' deducts 10% unless the simulation is explicitly noted in the comparison criteria[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-mockup-curator.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-mockup-curator.py[0m
[38;2;139;134;130m@@ -0,0 +1,85 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: mockup-comparison-curator blueprint updates."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, yaml, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Config YAML validity + functional_verification gate[0m
[38;2;255;255;255;48;2;19;87;20m+config_path = os.path.join(BASE, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(config_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    config = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+fv = config.get("functional_verification", {})[0m
[38;2;255;255;255;48;2;19;87;20m+if not fv.get("enabled"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml: functional_verification.enabled != true")[0m
[38;2;255;255;255;48;2;19;87;20m+gate = fv.get("gate", {})[0m
[38;2;255;255;255;48;2;19;87;20m+if not gate.get("before_scoring"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml: functional_verification.gate.before_scoring != true")[0m
[38;2;255;255;255;48;2;19;87;20m+if not gate.get("mandatory_checklist"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml: missing mandatory_checklist")[0m
[38;2;255;255;255;48;2;19;87;20m+scoring = gate.get("scoring_impact", {})[0m
[38;2;255;255;255;48;2;19;87;20m+if not scoring:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml: missing scoring_impact rules")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+vhist = config.get("blueprint", {}).get("version_history", [])[0m
[38;2;255;255;255;48;2;19;87;20m+latest = vhist[-1] if vhist else {}[0m
[38;2;255;255;255;48;2;19;87;20m+if latest.get("to") != "7.0.0":[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"config.yaml: expected version 7.0.0, got {latest.get('to')}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. BLUEPRINT.md sections[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(BASE, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+required_sections = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "Deliverable Integrity",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Implementation Details",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Format Constraints",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Output Pipeline",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for sec in required_sections:[0m
[38;2;255;255;255;48;2;19;87;20m+    if f"## {sec}" not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"BLUEPRINT.md: missing section '## {sec}'")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check specific content markers[0m
[38;2;255;255;255;48;2;19;87;20m+checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+    ("functional", "simulated", "mock"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("code snippet", "configuration block", "trade-off"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("tabular", "annotated-list", "3 sentences"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("ANSI escape", "code fences", "hunk headers"),[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for group in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+    for keyword in group:[0m
[38;2;255;255;255;48;2;19;87;20m+        if keyword.lower() not in bp.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT.md: missing keyword '{keyword}'")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. persona.md rules[0m
[38;2;255;255;255;48;2;19;87;20m+persona_path = os.path.join(BASE, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(persona_path, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    persona = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+persona_checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+    ("Honesty directive", "honesty directive"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("deduct at least 20%", "20%"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("Concise analyst", "concise analyst"),[0m
[38;2;255;255;255;48;2;19;87;20m+    ("prefers one dense table", "dense table"),[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for label, keyword in persona_checks:[0m
[38;2;255;255;255;48;2;19;87;20m+    if keyword.lower() not in persona.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"persona.md: missing '{label}'")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Summary[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== mockup-comparison-curator ad-hoc verification ===")[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAILURES ({len(errors)}):")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  - {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;139;134;130m… omitted 7 diff line(s) across 1 additional file(s)/section(s)[0m
**Ad-hoc verification: PASSED** (temp script cleaned up)
All 11 changes från feedback-rundorna är applicerade och verifierade:
| Feedback-round | Changes | Status |
|---|---|---|
| 20260626-180601 (83.4) | Deliverable Integrity, config functional_verification gate, honesty directive | verified |
| 20260626-180804 (90.2) | ANSI strip pipeline step, standard annotations | verified |
| 20260626-181034 (91.2) | Implementation Details section with code+config+trade-offs | verified |
| 20260626-181206 (90.0) | Format Constraints (tabular, 3 sentences, collapsed status column), concise analyst trait | verified |