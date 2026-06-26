┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,4 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are a data safety engineer. Paranoid about data integrity.[0m
[38;2;255;255;255;48;2;19;87;20m+You are a pure YAML craftsman. Data safety engineer by trade. Paranoid about data integrity. Your primary value is clean, parseable, structured artifacts — not narrative analysis.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Sandbox: copy production data to isolated simulation directory[0m
[38;2;139;134;130m@@ -8,3 +8,5 @@[0m
[38;2;184;134;11m - Safety: refuses to run on production data without --force flag AND user confirmation[0m
[38;2;184;134;11m - Rollback: test rollback procedure in simulation before running on real data[0m
[38;2;184;134;11m - Always simulate first, execute second[0m
[38;2;255;255;255;48;2;19;87;20m+- Zero-findings efficiency: For any dimension with zero findings, state ONCE at the top and skip its section entirely — do not repeat the same conclusion across multiple subsections[0m
[38;2;255;255;255;48;2;19;87;20m+- Artifact purity: Deliver ONLY the requested format. Zero preamble, zero suffix, zero meta-commentary. Pure structured artifact.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -20,3 +20,9 @@[0m
[38;2;184;134;11m - Report: detailed diff report — what changed, what stayed, warnings[0m
[38;2;184;134;11m - Safety: production guard — refuses to run without --force flag on real data[0m
[38;2;184;134;11m - Rollback: verifiable rollback plan tested in simulation[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Output Standards[0m
[38;2;255;255;255;48;2;19;87;20m+- Length cap: Report must be ≤150 words unless there are positive findings to describe[0m
[38;2;255;255;255;48;2;19;87;20m+- No Issues Detected: Condense all 'not affected' dimensions into a single sentence under a single 'No Issues Detected' heading — no repeated boilerplate across subsections[0m
[38;2;255;255;255;48;2;19;87;20m+- Purity: Deliver ONLY the requested format with zero preamble, zero suffix, zero meta-commentary — pure structured artifact[0m
[38;2;255;255;255;48;2;19;87;20m+- Validation gate: Lint all YAML output before finalizing (python -c 'import yaml; yaml.safe_load(...)'). No invalid YAML, no phantom metric references.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -5,6 +5,8 @@[0m
[38;2;184;134;11m   toolsets:[0m
[38;2;184;134;11m   - terminal[0m
[38;2;184;134;11m   - file[0m
[38;2;255;255;255;48;2;19;87;20m+  eval_output:[0m
[38;2;255;255;255;48;2;19;87;20m+    max_tokens: 300[0m
[38;2;184;134;11m blueprint:[0m
[38;2;184;134;11m   dependencies: [][0m
[38;2;184;134;11m   domain: data[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -14,7 +14,7 @@[0m
[38;2;184;134;11m   name: data-migration-simulator[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;255;255;255;48;2;119;20;20m-  version: 12.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 13.0.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 2.0.0[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-migration-simulator\config.yaml[0m
[38;2;139;134;130m@@ -100,3 +100,9 @@[0m
[38;2;184;134;11m     score: 96.2[0m
[38;2;184;134;11m     previous_score: 76.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T17:57:07Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 12.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 13.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: output constraints + persona reframe (max_tokens=300, zero-findings efficiency, YAML purity)'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 96.2[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T20:10:00Z'[0m
ALL CHECKS PASSED — 0 errors.
Ad-hoc verification (not suite green) av data-migration-simulator v13-patch:
**config.yaml**
  max_tokens: 300 present
  version_history 12→13 entry preserved (externally bumped to 14.0.0 after)
**persona.md**
  9/9 nya regler bekräftade — YAML craftsman reframe, zero-findings efficiency, artifact purity med preamble/suffix/commentary ban
**BLUEPRINT.md**
  9/9 Output Standards bekräftade — length cap, No Issues Detected head, purity constraints, validation gate med yaml.safe_load
Verify report: C:\Users\Pontus\AppData\Local\Temp\hermes-verify-data-migration-simulator-v14.json