┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml[0m
[38;2;139;134;130m@@ -14,54 +14,39 @@[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;184;134;11m   version: 3.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  enforceexecution: true[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 2.0.0[0m
[38;2;184;134;11m     reason: 'MAJOR: quality gate passed (score=92.4)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 92.4[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: null[0m
[38;2;184;134;11m     timestamp: '2026-06-25T23:00:50Z'[0m
[38;2;184;134;11m   - from: 2.0.0[0m
[38;2;184;134;11m     to: 2.0.1[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=81.2, delta=-11.2)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 81.2[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 92.4[0m
[38;2;184;134;11m     timestamp: '2026-06-26T00:45:52Z'[0m
[38;2;184;134;11m   - from: 2.0.1[0m
[38;2;184;134;11m     to: 2.0.2[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=63.2, delta=-18.0)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 63.2[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 81.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T06:37:11Z'[0m
[38;2;184;134;11m   - from: 2.0.2[0m
[38;2;184;134;11m     to: 2.0.3[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=51.0, delta=-12.2)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 51.0[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 63.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T06:38:00Z'[0m
[38;2;184;134;11m   - from: 2.0.3[0m
[38;2;184;134;11m     to: 2.1.0[0m
[38;2;184;134;11m     reason: 'MINOR: score improved by 28.6 points (prev=51.0, new=79.6)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 79.6[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 51.0[0m
[38;2;184;134;11m     timestamp: '2026-06-26T06:40:28Z'[0m
[38;2;184;134;11m   - from: 2.1.0[0m
[38;2;184;134;11m     to: 2.1.1[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=74.4, delta=-5.2)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 74.4[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 79.6[0m
[38;2;184;134;11m     timestamp: '2026-06-26T06:41:21Z'[0m
[38;2;184;134;11m   - from: 2.1.1[0m
[38;2;184;134;11m     to: 2.1.2[0m
[38;2;184;134;11m     reason: 'PATCH: minor change (score=75.6, delta=1.2)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 75.6[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 74.4[0m
[38;2;184;134;11m     timestamp: '2026-06-26T06:42:10Z'[0m
[38;2;184;134;11m   - from: 2.1.2[0m
[38;2;184;134;11m     to: 3.0.0[0m
[38;2;184;134;11m     reason: 'MAJOR: quality gate passed (score=90.4)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 90.4[0m
[38;2;255;255;255;48;2;119;20;20m-    previous_score: 75.6[0m
[38;2;184;134;11m     timestamp: '2026-06-26T07:20:14Z'[0m
[38;2;184;134;11m eval:[0m
[38;2;184;134;11m   benchmarks: [][0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\accessibility-auditor\templates\report.md → b/StydeAgents\blueprints\accessibility-auditor\templates\report.md[0m
[38;2;139;134;130m@@ -0,0 +1,44 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# Accessibility Audit Report[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Summary[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- **Target:** <page or component URL/file>[0m
[38;2;255;255;255;48;2;19;87;20m+- **Conformance target:** WCAG 2.2 <AA|AAA>[0m
[38;2;255;255;255;48;2;19;87;20m+- **Audit date:** <YYYY-MM-DD>[0m
[38;2;255;255;255;48;2;19;87;20m+- **Total violations:** <count>[0m
[38;2;255;255;255;48;2;19;87;20m+- **Critical:** <count> | **High:** <count> | **Medium:** <count> | **Low:** <count>[0m
[38;2;255;255;255;48;2;19;87;20m+- **Files modified:** <count>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Violations by Severity[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Critical[0m
[38;2;255;255;255;48;2;19;87;20m+| # | Criterion | Element | Issue | Fix |[0m
[38;2;255;255;255;48;2;19;87;20m+|---|-----------|---------|-------|-----|[0m
[38;2;255;255;255;48;2;19;87;20m+|   |           |         |       |     |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### High[0m
[38;2;255;255;255;48;2;19;87;20m+| # | Criterion | Element | Issue | Fix |[0m
[38;2;255;255;255;48;2;19;87;20m+|---|-----------|---------|-------|-----|[0m
[38;2;255;255;255;48;2;19;87;20m+|   |           |         |       |     |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Medium[0m
[38;2;255;255;255;48;2;19;87;20m+| # | Criterion | Element | Issue | Fix |[0m
[38;2;255;255;255;48;2;19;87;20m+|---|-----------|---------|-------|-----|[0m
[38;2;255;255;255;48;2;19;87;20m+|   |           |         |       |     |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Low[0m
[38;2;255;255;255;48;2;19;87;20m+| # | Criterion | Element | Issue | Fix |[0m
[38;2;255;255;255;48;2;19;87;20m+|---|-----------|---------|-------|-----|[0m
[38;2;255;255;255;48;2;19;87;20m+|   |           |         |       |     |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Diffs Applied[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<for each file mutated: path, before/after snippet, and the WCAG criterion resolved>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Verdict[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- **PASS** if all critical and high violations fixed[0m
[38;2;255;255;255;48;2;19;87;20m+- **FAIL** if any critical or high violation remains[0m
[38;2;255;255;255;48;2;19;87;20m+- **files_modified:** <count>[0m
[38;2;255;255;255;48;2;19;87;20m+- **violations_fixed:** <count>[0m
[38;2;255;255;255;48;2;19;87;20m+- **critical_violations_resolved:** <count>[0m
All tre ändringar är på plats.
**config.yaml** (rad 17):
- `enforceexecution: true` — penaliserar compositescore med 10 poäng om action-field är 'plan' istallet för 'write'/'patch'
- `score` och `previous_score` borttagna från samtliga version_history-poster (inga spekulativa scores längre)
**BLUEPRINT.md** (redan uppdaterad i tidigare session):
- Step 3 pekar på `templates/report.md` — ingen inline-tabell
- Contracts-sektion med `conclusionformat: appliedchanges`
- Tvingande diff-sammanfattning av alla mutationer, inga rekommendationer utan patchar
- Severity-taxonomi och AAA-scoping inlagd
**templates/report.md** (ny):
- Återanvändbar rapportmall med severity-tabeller, diff-sektion och verdict-block