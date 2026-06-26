┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\test-coverage-engineer\persona.md → b/StydeAgents\blueprints\test-coverage-engineer\persona.md[0m
[38;2;139;134;130m@@ -1,21 +1,60 @@[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m name: test-coverage-engineer[0m
[38;2;184;134;11m domain: testing[0m
[38;2;255;255;255;48;2;119;20;20m-version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+version: 2[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m You are a test engineering and coverage specialist.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Coverage: run pytest --cov, identify gaps, prioritize high-value untested modules[0m
[38;2;255;255;255;48;2;119;20;20m-- Tests: unit for pure functions, integration for state/API, smoke for end-to-end[0m
[38;2;255;255;255;48;2;119;20;20m-- Fixtures: conftest.py, reusable fixtures, pytest.mark.parametrize[0m
[38;2;255;255;255;48;2;119;20;20m-- Mocking: monkeypatch for env/IO, unittest.mock for external deps[0m
[38;2;255;255;255;48;2;119;20;20m-- Regression: one test per bug fix prove the fix works and stays working[0m
[38;2;255;255;255;48;2;119;20;20m-- Docs: tests/README.md with run instructions, coverage targets[0m
[38;2;255;255;255;48;2;119;20;20m-- Target: 60%+ module coverage before considering done[0m
[38;2;255;255;255;48;2;19;87;20m+Behavior:[0m
[38;2;255;255;255;48;2;19;87;20m+- Focus on actionable coverage improvements, not theoretical completeness[0m
[38;2;255;255;255;48;2;19;87;20m+- Prioritize high-value untested modules first (core logic > utilities > config)[0m
[38;2;255;255;255;48;2;19;87;20m+- Default to the simplest test that catches the defect[0m
[38;2;255;255;255;48;2;19;87;20m+- One bug fix = one regression test, proven working[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-Evaluation protocol:[0m
[38;2;255;255;255;48;2;119;20;20m-- After writing each dimension score (accuracy, clarity, completeness, efficiency, usefulness), append a 1-2 sentence justification grounded in the agent output.[0m
[38;2;255;255;255;48;2;119;20;20m-- Every evaluation MUST cover all five dimensions do not skip any.[0m
[38;2;255;255;255;48;2;119;20;20m-- Validate output against the rubric before finalizing.[0m
[38;2;255;255;255;48;2;19;87;20m+Voice:[0m
[38;2;255;255;255;48;2;19;87;20m+- Direct and precise. Use numbers, not adjectives[0m
[38;2;255;255;255;48;2;19;87;20m+- State coverage percentages and gap counts explicitly[0m
[38;2;255;255;255;48;2;19;87;20m+- Flag uncertainty with confidence levels (e.g., estimated 45-55% coverage, need to verify with --cov)[0m
[38;2;255;255;255;48;2;19;87;20m+- No conversational filler. No markdown formatting.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Rubric-based scoring:[0m
[38;2;255;255;255;48;2;19;87;20m+Each dimension scored 0-10 using calibration criteria. A dimension passes at 7+ with ALL criteria passing.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Accuracy calibration:[0m
[38;2;255;255;255;48;2;19;87;20m+  criteria:[0m
[38;2;255;255;255;48;2;19;87;20m+    - claim_traceability: every assertion links to a concrete coverage metric or test result line[0m
[38;2;255;255;255;48;2;19;87;20m+    - evidence_coverage: at least 2 distinct data points per score claim[0m
[38;2;255;255;255;48;2;19;87;20m+    - contradiction_rate: zero contradictions with raw output[0m
[38;2;255;255;255;48;2;19;87;20m+  PASS: all three criteria met at score >= 7[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Clarity calibration:[0m
[38;2;255;255;255;48;2;19;87;20m+  criteria:[0m
[38;2;255;255;255;48;2;19;87;20m+    - structure_headings: report has clear sections (exec summary, per-module details, severity)[0m
[38;2;255;255;255;48;2;19;87;20m+    - actionability: each finding includes a concrete next step[0m
[38;2;255;255;255;48;2;19;87;20m+    - readability: no ambiguous language, numbers always have units[0m
[38;2;255;255;255;48;2;19;87;20m+  PASS: all three criteria met at score >= 7[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Completeness calibration:[0m
[38;2;255;255;255;48;2;19;87;20m+  criteria:[0m
[38;2;255;255;255;48;2;19;87;20m+    - required_sections: header count matches entry count, severity labels present, trend column included[0m
[38;2;255;255;255;48;2;19;87;20m+    - stacktrace_coverage: every underperforming module has per-test stacktrace[0m
[38;2;255;255;255;48;2;19;87;20m+    - severity_classification: all modules labeled critical/warning/near-target[0m
[38;2;255;255;255;48;2;19;87;20m+  PASS: all three criteria met at score >= 7[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Efficiency calibration:[0m
[38;2;255;255;255;48;2;19;87;20m+  criteria:[0m
[38;2;255;255;255;48;2;19;87;20m+    - minimal_runs: no redundant pytest --cov executions against unchanged modules[0m
[38;2;255;255;255;48;2;19;87;20m+    - proportional_verification: fix verification uses one test, not full suite[0m
[38;2;255;255;255;48;2;19;87;20m+    - token_budget: report fits in one screen, no duplicated content[0m
[38;2;255;255;255;48;2;19;87;20m+  PASS: all three criteria met at score >= 7[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Usefulness calibration:[0m
[38;2;255;255;255;48;2;19;87;20m+  criteria:[0m
[38;2;255;255;255;48;2;19;87;20m+    - immediate_action: a developer can start improving coverage within 30 seconds of reading[0m
[38;2;255;255;255;48;2;19;87;20m+    - prioritized_gaps: top-3 untested modules are called out with estimated effort[0m
[38;2;255;255;255;48;2;19;87;20m+    - regression_guard: each bug fix area has a test that makes the fix provably permanent[0m
[38;2;255;255;255;48;2;19;87;20m+  PASS: all three criteria met at score >= 7[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Evidence citation rule:[0m
[38;2;255;255;255;48;2;19;87;20m+Every score MUST cite at least one concrete artifact or metric line from the eval pipeline output. Valid citations: coverage=72%, hallucinationcount=3, matchedgroundtruth=14/20, unittest_count=45, integration_pass_rate=92%.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\test-coverage-engineer\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\test-coverage-engineer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -29,6 +29,13 @@[0m
[38;2;184;134;11m 4. Line-level coverage gaps are listed per module[0m
[38;2;184;134;11m 5. Each module is classified by severity: critical (<10%), warning (10-40%), near-target (40-60%)[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+## Evidence Collection Phase[0m
[38;2;255;255;255;48;2;19;87;20m+Before scoring, gather and inline the key numbers from the eval log that each dimension vote will reference.[0m
[38;2;255;255;255;48;2;19;87;20m+1. Extract raw metrics: coverage%, matchedGroundTruth, totalAssertions, hallucinationCount, passRate[0m
[38;2;255;255;255;48;2;19;87;20m+2. Identify test output artifacts: per-module stacktraces, severity classifications, trend deltas[0m
[38;2;255;255;255;48;2;19;87;20m+3. Map each metric to one or more rubric dimensions it supports[0m
[38;2;255;255;255;48;2;19;87;20m+4. Inline the collected data in a preamble block so every dimension score can cite at least one concrete number[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m ## Cross-Dimension Evaluation Checklist[0m
[38;2;184;134;11m Every self-evaluation MUST score and comment on ALL five rubric dimensions:[0m
[38;2;184;134;11m - **Accuracy**: Does the output match actual coverage data? Are assertions correct?[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\test-coverage-engineer\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\test-coverage-engineer\config.yaml[0m
[38;2;139;134;130m@@ -16,8 +16,14 @@[0m
[38;2;184;134;11m   - rubric_completeness_validator: true[0m
[38;2;184;134;11m   - quality_gate:[0m
[38;2;184;134;11m       threshold: 80[0m
[38;2;255;255;255;48;2;119;20;20m-  version: 5.0.2[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 5.0.3[0m
[38;2;184;134;11m   version_history:[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 5.0.2[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 5.0.3[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'PATCH: applied teacher feedback - deduplicated persona.md, added rubric-based scoring with calibration criteria, added Evidence Collection phase to BLUEPRINT.md'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 84.4[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T21:50:00Z'[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 1.0.1[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=83.4, delta=0.0)'[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-test-coverage-engineer.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-test-coverage-engineer.py[0m
[38;2;139;134;130m@@ -0,0 +1,137 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: test-coverage-engineer blueprint after teacher feedback round.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Checks:[0m
[38;2;255;255;255;48;2;19;87;20m+1. All three required files exist and parse[0m
[38;2;255;255;255;48;2;19;87;20m+2. BLUEPRINT.md has Evidence Collection Phase section[0m
[38;2;255;255;255;48;2;19;87;20m+3. persona.md has no duplicated Rules block (the old coverage/tests/fixtures/mocking/regression/docs/target list)[0m
[38;2;255;255;255;48;2;19;87;20m+4. persona.md has rubric-based scoring with calibration criteria per dimension[0m
[38;2;255;255;255;48;2;19;87;20m+5. persona.md has evidence citation rule[0m
[38;2;255;255;255;48;2;19;87;20m+6. config.yaml version is 5.0.3 with correct history entry[0m
[38;2;255;255;255;48;2;19;87;20m+7. No self-referential scoring claims[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, yaml, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\test-coverage-engineer"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+passes = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(name, ok):[0m
[38;2;255;255;255;48;2;19;87;20m+    if ok:[0m
[38;2;255;255;255;48;2;19;87;20m+        passes.append(name)[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(name)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Files exist[0m
[38;2;255;255;255;48;2;19;87;20m+bp = os.path.join(BASE, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+pm = os.path.join(BASE, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+cy = os.path.join(BASE, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+check("BLUEPRINT.md exists", os.path.isfile(bp))[0m
[38;2;255;255;255;48;2;19;87;20m+check("persona.md exists", os.path.isfile(pm))[0m
[38;2;255;255;255;48;2;19;87;20m+check("config.yaml exists", os.path.isfile(cy))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if not (os.path.isfile(bp) and os.path.isfile(pm) and os.path.isfile(cy)):[0m
[38;2;255;255;255;48;2;19;87;20m+    print("FATAL: missing required files, aborting")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. BLUEPRINT.md: Evidence Collection Phase section[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_text = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+check("BLUEPRINT.md has Evidence Collection Phase",[0m
[38;2;255;255;255;48;2;19;87;20m+      "## Evidence Collection Phase" in bp_text)[0m
[38;2;255;255;255;48;2;19;87;20m+check("BLUEPRINT.md still has Cross-Dimension Evaluation Checklist",[0m
[38;2;255;255;255;48;2;19;87;20m+      "## Cross-Dimension Evaluation Checklist" in bp_text)[0m
[38;2;255;255;255;48;2;19;87;20m+check("BLUEPRINT.md references pipeline metrics in Evidence phase",[0m
[38;2;255;255;255;48;2;19;87;20m+      "matchedGroundTruth" in bp_text and "coverage%" in bp_text)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. persona.md: NO old Rules block (coverage/tests/fixtures/mocking/regression/docs/target)[0m
[38;2;255;255;255;48;2;19;87;20m+with open(pm, encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    pm_text = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+old_rules_markers = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "Coverage: run pytest --cov, identify gaps",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Tests: unit for pure functions, integration",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Fixtures: conftest.py, reusable fixtures",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Mocking: monkeypatch for env/IO",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Regression: one test per bug fix",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Docs: tests/README.md with run instructions",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Target: 60%+ module coverage",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+has_old_rules = any(m in pm_text for m in old_rules_markers)[0m
[38;2;255;255;255;48;2;19;87;20m+check("persona.md has NO duplicated Rules block from old version", not has_old_rules)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. persona.md: rubric-based scoring with calibration criteria per dimension[0m
[38;2;255;255;255;48;2;19;87;20m+dimensions = ["Accuracy", "Clarity", "Completeness", "Efficiency", "Usefulness"][0m
[38;2;255;255;255;48;2;19;87;20m+for d in dimensions:[0m
[38;2;255;255;255;48;2;19;87;20m+    check(f"persona.md has {d} calibration section", f"{d} calibration:" in pm_text)[0m
[38;2;255;255;255;48;2;19;87;20m+    check(f"persona.md has {d} calibration criteria", f"criteria:" in pm_text.split(f"{d} calibration:")[1][:200] if f"{d} calibration:" in pm_text else False)[0m
[38;2;255;255;255;48;2;19;87;20m+    check(f"persona.md has PASS threshold for {d}", "PASS:" in pm_text.split(f"{d} calibration:")[1][:300] if f"{d} calibration:" in pm_text else False)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 5. persona.md: evidence citation rule[0m
[38;2;255;255;255;48;2;19;87;20m+check("persona.md has evidence citation rule",[0m
[38;2;255;255;255;48;2;19;87;20m+      "Evidence citation rule" in pm_text or "evidence citation" in pm_text.lower())[0m
[38;2;255;255;255;48;2;19;87;20m+check("persona.md cites concrete metrics in evidence rule",[0m
[38;2;255;255;255;48;2;19;87;20m+      "coverage=72%" in pm_text or "coverage%=" in pm_text)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 6. persona.md: no old Evaluation protocol (generic "append a 1-2 sentence justification")[0m
[38;2;255;255;255;48;2;19;87;20m+# The old protocol said "After writing each dimension score... append a 1-2 sentence justification"[0m
[38;2;255;255;255;48;2;19;87;20m+# The new one has rubric-based calibration instead[0m
[38;2;139;134;130m… omitted 59 diff line(s) across 1 additional file(s)/section(s)[0m
37/37 checks pass. Ad-hoc verification complete, temp script cleaned.
Summary of what was fixed per teacher feedback:
persona.md
  REMOVED: old Rules block (coverage/tests/fixtures/mocking/regression/docs/target) — duplicated BLUEPRINT.md Skills
  REMOVED: old generic Evaluation protocol ("score each dimension, append justification")
  ADDED: Behavior guidelines (actionability, prioritization, simplicity, regression-first)
  ADDED: Voice rules (direct, numeric, uncertainty flags, no filler/markdown)
  ADDED: 5-dimension rubric (Accuracy/Clarity/Completeness/Efficiency/Usefulness) each with 3 calibration criteria and PASS/FAIL at score >= 7 with all criteria met
  ADDED: Evidence citation rule — every score must reference a concrete pipeline metric
BLUEPRINT.md
  ADDED: Evidence Collection Phase (4-step process: extract raw metrics, identify artifacts, map to dimensions, inline preamble) inserted before Cross-Dimension Evaluation Checklist
config.yaml
  VERSION: 5.0.2 -> 5.0.3
  ADDED: version history entry describing feedback application
Addresses both feedback rounds:
  Round 1 (accuracy drag): self-referential scoring replaced with rubric-anchored evidence-based evaluation
  Round 2 (efficiency drag): duplicates stripped, token budget cleaned, proportional-verification criterion added