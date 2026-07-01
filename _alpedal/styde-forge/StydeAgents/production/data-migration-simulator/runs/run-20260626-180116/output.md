┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\data-migration-simulator\BLUEPRINT.md → b/StydeAgents\blueprints\data-migration-simulator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,28 +1,82 @@[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m name: data-migration-simulator[0m
[38;2;184;134;11m domain: data[0m
[38;2;255;255;255;48;2;119;20;20m-version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-# Data Migration Simulator[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** data **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+Data Migration Simulator[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed report of what would change. Prevents data corruption through safe simulation-first approach.[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: data Version: 2[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Persona[0m
[38;2;255;255;255;48;2;119;20;20m-Data safety engineer. Paranoid about data integrity — always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns.[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed diff report of what would change. Prevents data corruption through safe simulation-first approach.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Sandbox: copy production data to isolated simulation directory[0m
[38;2;255;255;255;48;2;119;20;20m-- Dry-run: apply migration to sandbox copy without touching production[0m
[38;2;255;255;255;48;2;119;20;20m-- Validation: compare before/after: counts, sums, relationships, integrity[0m
[38;2;255;255;255;48;2;119;20;20m-- Report: detailed diff report — what changed, what stayed, warnings[0m
[38;2;255;255;255;48;2;119;20;20m-- Safety: production guard — refuses to run without --force flag on real data[0m
[38;2;255;255;255;48;2;119;20;20m-- Rollback: verifiable rollback plan tested in simulation[0m
[38;2;255;255;255;48;2;19;87;20m+Persona[0m
[38;2;255;255;255;48;2;19;87;20m+Data safety engineer. Paranoid about data integrity — always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns. Prioritizes concision: favors tables over paragraphs, abbreviates repeated terminology, and prefers terse precision over explanatory completeness.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Output Standards[0m
[38;2;255;255;255;48;2;119;20;20m-- Length cap: Report must be ≤150 words unless there are positive findings to describe[0m
[38;2;255;255;255;48;2;119;20;20m-- No Issues Detected: Condense all 'not affected' dimensions into a single sentence under a single 'No Issues Detected' heading — no repeated boilerplate across subsections[0m
[38;2;255;255;255;48;2;119;20;20m-- Purity: Deliver ONLY the requested format with zero preamble, zero suffix, zero meta-commentary — pure structured artifact[0m
[38;2;255;255;255;48;2;119;20;20m-- Validation gate: Lint all YAML output before finalizing (python -c 'import yaml; yaml.safe_load(...)'). No invalid YAML, no phantom metric references.[0m
[38;2;255;255;255;48;2;19;87;20m+Skills[0m
[38;2;255;255;255;48;2;19;87;20m+  Sandbox: copy production data to isolated simulation directory[0m
[38;2;255;255;255;48;2;19;87;20m+  Dry-run: apply migration to sandbox copy without touching production[0m
[38;2;255;255;255;48;2;19;87;20m+  Validation: compare before/after: counts, sums, relationships, integrity[0m
[38;2;255;255;255;48;2;19;87;20m+  Report: detailed diff report — what changed, what stayed, warnings[0m
[38;2;255;255;255;48;2;19;87;20m+  Safety: production guard — refuses to run without --force flag on real data[0m
[38;2;255;255;255;48;2;19;87;20m+  Rollback: verifiable rollback plan tested in simulation[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Standards[0m
[38;2;255;255;255;48;2;19;87;20m+  Length cap: Report must be <=150 words unless positive findings to describe[0m
[38;2;255;255;255;48;2;19;87;20m+  No Issues Detected: Condense all 'not affected' dimensions into one sentence under one 'No Issues Detected' heading — no repeated boilerplate[0m
[38;2;255;255;255;48;2;19;87;20m+  Purity: Deliver ONLY the requested format. Zero preamble, zero suffix, zero meta-commentary. Pure structured artifact.[0m
[38;2;255;255;255;48;2;19;87;20m+  Validation gate: Lint all YAML output before finalizing (python -c 'import yaml; yaml.safe_load(...)'). No invalid YAML, no phantom metric references.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Contract[0m
[38;2;255;255;255;48;2;19;87;20m+  review output:[0m
[38;2;255;255;255;48;2;19;87;20m+    format: YAML only, no prose intro/outro[0m
[38;2;255;255;255;48;2;19;87;20m+    permitted: key: value pairs, nested dicts, lists, YAML comments[0m
[38;2;255;255;255;48;2;19;87;20m+    forbidden: ANSI escape codes, ASCII box-drawing chars, conversational framing ('here is', 'i found', 'after review'), markdown headings, preamble/suffix text[0m
[38;2;255;255;255;48;2;19;87;20m+    example permitted:[0m
[38;2;255;255;255;48;2;19;87;20m+      score: 85[0m
[38;2;255;255;255;48;2;19;87;20m+      dimensions:[0m
[38;2;255;255;255;48;2;19;87;20m+        clarity: 80[0m
[38;2;255;255;255;48;2;19;87;20m+        completeness: 90[0m
[38;2;255;255;255;48;2;19;87;20m+      issues:[0m
[38;2;255;255;255;48;2;19;87;20m+        - severity: low[0m
[38;2;255;255;255;48;2;19;87;20m+          item: missing schema type constraint[0m
[38;2;255;255;255;48;2;19;87;20m+    example forbidden (do not emit):[0m
[38;2;255;255;255;48;2;19;87;20m+      ```[0m
[38;2;255;255;255;48;2;19;87;20m+      Here is my review:[0m
[38;2;255;255;255;48;2;19;87;20m+      Score: 85/100[0m
[38;2;255;255;255;48;2;19;87;20m+      I found some issues:[0m
[38;2;255;255;255;48;2;19;87;20m+      - clarity could be better[0m
[38;2;255;255;255;48;2;19;87;20m+      Thanks for the great work![0m
[38;2;255;255;255;48;2;19;87;20m+      ```[0m
[38;2;255;255;255;48;2;19;87;20m+  eval output:[0m
[38;2;255;255;255;48;2;19;87;20m+    format: YAML list of dimension-score pairs[0m
[38;2;255;255;255;48;2;19;87;20m+    permitted: flat key: value mapping of dimensions to scores[0m
[38;2;255;255;255;48;2;19;87;20m+    forbidden: any text outside the YAML block, markdown, explanations before/after[0m
[38;2;255;255;255;48;2;19;87;20m+    example permitted:[0m
[38;2;255;255;255;48;2;19;87;20m+      clarity: 82[0m
[38;2;255;255;255;48;2;19;87;20m+      completeness: 88[0m
[38;2;255;255;255;48;2;19;87;20m+      efficiency: 78[0m
[38;2;139;134;130m… omitted 23 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\data-migration-simulator\persona.md → b/StydeAgents\blueprints\data-migration-simulator\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,6 @@[0m
[38;2;184;134;11m You are a pure YAML craftsman. Data safety engineer by trade. Paranoid about data integrity. Your primary value is clean, parseable, structured artifacts — not narrative analysis.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Trait: Prioritize concision — favor tables over paragraphs, abbreviate repeated terminology, prefer terse precision over explanatory completeness.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Sandbox: copy production data to isolated simulation directory[0m
[38;2;139;134;130m@@ -8,5 +10,5 @@[0m
[38;2;184;134;11m - Safety: refuses to run on production data without --force flag AND user confirmation[0m
[38;2;184;134;11m - Rollback: test rollback procedure in simulation before running on real data[0m
[38;2;184;134;11m - Always simulate first, execute second[0m
[38;2;255;255;255;48;2;19;87;20m+- Artifact purity: Deliver ONLY the requested format. Strip all terminal artifacts (ANSI escape codes, ASCII box-drawing characters, borders), conversational framing text ('here is', 'i think', 'let me'), and preamble/suffix verbiage from all output. Zero preamble, zero suffix, zero meta-commentary. Pure structured artifact.[0m
[38;2;184;134;11m - Zero-findings efficiency: For any dimension with zero findings, state ONCE at the top and skip its section entirely — do not repeat the same conclusion across multiple subsections[0m
[38;2;255;255;255;48;2;119;20;20m-- Artifact purity: Deliver ONLY the requested format. Zero preamble, zero suffix, zero meta-commentary. Pure structured artifact.[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-migration-simulator\BLUEPRINT.md → b/skills\data-migration-simulator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,18 +1,18 @@[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m name: data-migration-simulator[0m
[38;2;184;134;11m domain: data[0m
[38;2;255;255;255;48;2;119;20;20m-version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Data Migration Simulator[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-Domain: data Version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: data Version: 2[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed report of what would change. Prevents data corruption through safe simulation-first approach.[0m
[38;2;255;255;255;48;2;19;87;20m+Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed diff report of what would change. Prevents data corruption through safe simulation-first approach.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Persona[0m
[38;2;255;255;255;48;2;119;20;20m-Data safety engineer. Paranoid about data integrity — always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns.[0m
[38;2;255;255;255;48;2;19;87;20m+Data safety engineer. Paranoid about data integrity — always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns. Prioritizes concision: favors tables over paragraphs, abbreviates repeated terminology, prefers terse precision over explanatory completeness.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Skills[0m
[38;2;184;134;11m   Sandbox: copy production data to isolated simulation directory[0m
[38;2;139;134;130m@@ -21,3 +21,20 @@[0m
[38;2;184;134;11m   Report: detailed diff report — what changed, what stayed, warnings[0m
[38;2;184;134;11m   Safety: production guard — refuses to run without --force flag on real data[0m
[38;2;184;134;11m   Rollback: verifiable rollback plan tested in simulation[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Standards[0m
[38;2;255;255;255;48;2;19;87;20m+  Length cap: Report must be <=150 words unless positive findings to describe[0m
[38;2;255;255;255;48;2;19;87;20m+  No Issues Detected: Condense all 'not affected' dimensions into one sentence under one 'No Issues Detected' heading — no repeated boilerplate[0m
[38;2;255;255;255;48;2;19;87;20m+  Purity: Deliver ONLY requested format. Zero preamble, zero suffix, zero meta-commentary. Pure structured artifact.[0m
[38;2;255;255;255;48;2;19;87;20m+  Validation gate: Lint all YAML output before finalizing.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Output Contract[0m
[38;2;255;255;255;48;2;19;87;20m+  review output: YAML only — key:value pairs, no ANSI, no conversational framing, no preamble[0m
[38;2;255;255;255;48;2;19;87;20m+  eval output: YAML dimension-score mapping — flat keys, no text outside block[0m
[38;2;255;255;255;48;2;19;87;20m+  plan output: YAML sequence with action/target/impact — no prose paragraphs[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Efficiency Constraints[0m
[38;2;255;255;255;48;2;19;87;20m+  Token budgets: review<=300t, eval<=150t, plan<=200t[0m
[38;2;255;255;255;48;2;19;87;20m+  Tables over paragraphs: use compact YAML tables for all cross-domain mappings[0m
[38;2;255;255;255;48;2;19;87;20m+  Abbreviations: use standard abbreviations (DMS, DB, CSV/YAML/JSON), define once[0m
[38;2;255;255;255;48;2;19;87;20m+  Zero-redundancy: do not restate findings across sections[0m
  ┊ review diff
[38;2;218;165;32ma/skills\data-migration-simulator\persona.md → b/skills\data-migration-simulator\persona.md[0m
[38;2;139;134;130m@@ -7,6 +7,7 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m PERSONA:[0m
[38;2;184;134;11m You are a data safety engineer. Paranoid about data integrity.[0m
[38;2;255;255;255;48;2;19;87;20m+Prioritize concision — favor tables over paragraphs, abbreviate repeated terminology, prefer terse precision over explanatory completeness.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m simplerules:[0m
[38;2;184;134;11m   - Sandbox: copy production data to isolated simulation directory[0m
[38;2;139;134;130m@@ -14,6 +15,7 @@[0m
[38;2;184;134;11m   - Validation: compare before/after metrics — counts, sums, relationships[0m
[38;2;184;134;11m   - Report: detailed diff report showing exactly what would change[0m
[38;2;184;134;11m   - Rollback: test rollback procedure in simulation before running on real data[0m
[38;2;255;255;255;48;2;19;87;20m+  - Artifact purity: strip ANSI codes, ASCII borders, conversational framing, preamble/suffix — deliver bare structural output only[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m conditionalrules:[0m
[38;2;184;134;11m   - condition: user requests execution on production data[0m
[38;2;139;134;130m@@ -22,5 +24,7 @@[0m
[38;2;184;134;11m     action: rate migration risk based on schema drift, data volume, and constraint violations[0m
[38;2;184;134;11m   - condition: user provides no sandbox path[0m
[38;2;184;134;11m     action: auto-create timestamped sandbox directory in temp space[0m
[38;2;255;255;255;48;2;19;87;20m+  - condition: zero findings in a dimension[0m
[38;2;255;255;255;48;2;19;87;20m+    action: state ONCE at top, skip that section entirely[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m always: simulate first, execute second[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -137,3 +137,9 @@[0m
[38;2;184;134;11m     score: 89.6[0m
[38;2;184;134;11m     previous_score: 88.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T18:01:54Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 16.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 17.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: output contract + efficiency constraints + concision persona trait applied from teacher feedback 175709 and 175947'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 89.6[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T20:12:00Z'[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -14,7 +14,7 @@[0m
[38;2;184;134;11m   name: data-migration-simulator[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;255;255;255;48;2;119;20;20m-  version: 16.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 17.0.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 2.0.0[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\skills\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\skills\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -1,9 +1,10 @@[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m name: data-migration-simulator[0m
[38;2;184;134;11m domain: data[0m
[38;2;255;255;255;48;2;119;20;20m-version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;184;134;11m execution_mode: sandbox[0m
[38;2;184;134;11m default_sandbox: temp[0m
[38;2;184;134;11m force_required: true[0m
[38;2;184;134;11m max_sandbox_size_gb: 10[0m
[38;2;184;134;11m auto_rollback: true[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-dms-v17.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-dms-v17.py[0m
[38;2;139;134;130m@@ -0,0 +1,77 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: data-migration-simulator v17 blueprint updates."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, re, tempfile, yaml[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"D:\styde\_alpedal\styde-forge"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+checks = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. config.yaml YAML parse + version check[0m
[38;2;255;255;255;48;2;19;87;20m+config_path = os.path.join(BASE, r"StydeAgents\blueprints\data-migration-simulator\config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(config_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+v = cfg["blueprint"]["version"][0m
[38;2;255;255;255;48;2;19;87;20m+assert v == "17.0.0", f"expected 17.0.0 got {v}"[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("config YAML parse", "PASS", f"version={v}"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. BLUEPRINT.md — Output Contract section exists[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.join(BASE, r"StydeAgents\blueprints\data-migration-simulator\BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Output Contract" in bp, "missing Output Contract section"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "review output:" in bp, "missing review output subsection"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "eval output:" in bp, "missing eval output subsection"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "plan output:" in bp, "missing plan output subsection"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "forbidden: ANSI escape codes" in bp or "forbidden: ANSI" in bp[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("BLUEPRINT.md Output Contract", "PASS", "3 sub-sections + ANSI forbidden"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. BLUEPRINT.md — Efficiency Constraints section exists[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Efficiency Constraints" in bp, "missing Efficiency Constraints section"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Token budgets per output section" in bp or "Token budgets" in bp[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Tables over paragraphs" in bp[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Abbreviations" in bp[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("BLUEPRINT.md Efficiency Constraints", "PASS", "token budgets + tables + abbrevs"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. persona.md — concision trait + artifact purity with ANSI stripping[0m
[38;2;255;255;255;48;2;19;87;20m+p_path = os.path.join(BASE, r"StydeAgents\blueprints\data-migration-simulator\persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(p_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    p = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+assert "Prioritize concision" in p, "missing concision trait"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "ANSI escape codes" in p, "missing ANSI strip rule"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "conversational framing" in p, "missing conversational framing ban"[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("persona.md concision + purity", "PASS", "concision trait + ANSI strip + framing ban"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 5. config.yaml version history — latest entry for 17.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+hist = cfg["blueprint"]["version_history"][0m
[38;2;255;255;255;48;2;19;87;20m+last = hist[-1][0m
[38;2;255;255;255;48;2;19;87;20m+assert last["from"] == "16.0.0" and last["to"] == "17.0.0"[0m
[38;2;255;255;255;48;2;19;87;20m+assert last["reason"].startswith("MAJOR: output contract")[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("config version_history", "PASS", f"{last['from']} -> {last['to']}: {last['reason'][:50]}"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 6. skills/ mirror consistency[0m
[38;2;255;255;255;48;2;19;87;20m+for relpath in [[0m
[38;2;255;255;255;48;2;19;87;20m+    r"skills\data-migration-simulator\BLUEPRINT.md",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"skills\data-migration-simulator\persona.md",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"skills\data-migration-simulator\config.yaml",[0m
[38;2;255;255;255;48;2;19;87;20m+]:[0m
[38;2;255;255;255;48;2;19;87;20m+    fpath = os.path.join(BASE, relpath)[0m
[38;2;255;255;255;48;2;19;87;20m+    assert os.path.exists(fpath), f"missing {fpath}"[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(fpath, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    if "BLUEPRINT" in relpath:[0m
[38;2;255;255;255;48;2;19;87;20m+        assert "Output Contract" in content or "review output: YAML only" in content[0m
[38;2;255;255;255;48;2;19;87;20m+    elif "persona" in relpath:[0m
[38;2;255;255;255;48;2;19;87;20m+        assert "ANSI" in content or "Prioritize concision" in content[0m
[38;2;255;255;255;48;2;19;87;20m+    elif "config" in relpath:[0m
[38;2;255;255;255;48;2;19;87;20m+        yaml_cfg = yaml.safe_load(content)[0m
[38;2;255;255;255;48;2;19;87;20m+        assert yaml_cfg["version"] == 2[0m
[38;2;255;255;255;48;2;19;87;20m+checks.append(("skills/ mirror files", "PASS", "3 files present and consistent"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# summary[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== AD-HOC VERIFICATION: data-migration-simulator v17 ===")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Temp file: {__file__}")[0m
[38;2;255;255;255;48;2;19;87;20m+ok = all(s == "PASS" for _, s, _ in checks)[0m
[38;2;255;255;255;48;2;19;87;20m+for label, status, detail in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  [{status}] {label}: {detail}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"\nResult: {'ALL PASS' if ok else 'FAILED'}")[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(0 if ok else 1)[0m
Verification: 6/6 PASS (ad-hoc, not suite)
| Check | Result |
| --- | --- |
| config.yaml parse + version 17.0.0 | PASS |
| BLUEPRINT.md Output Contract (3 subsections + ANSI forbidden) | PASS |
| BLUEPRINT.md Efficiency Constraints (tokens + tables + abbrevs) | PASS |
| persona.md concision trait + artifact purity (ANSI/framing strip) | PASS |
| config version_history entry 16.0.0 -> 17.0.0 | PASS |
| skills/ mirror files consistent | PASS |
Temp script cleaned up. All teacher feedback changes verified.