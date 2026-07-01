Source file: bi-blueprint-report.csv
Output file: bi-blueprint-report_cleaned.csv
Rows: 8
Original preserved: bi-blueprint-report.csv (unchanged)
Issues found: 10 total across 8 rows
FLOATING POINT PRECISION (7 rows)
3d-data-terrain-explorer: 22.200000000000003 -> 22.2
activity-feed-designer: 15.399999999999991 -> 15.4
adaptive-metric-layout: 25.200000000000003 -> 25.2
aesthetic-style-composer: 23.599999999999994 -> 23.6
agent-promotion-evaluator: 7.400000000000006 -> 7.4
agent-lifecycle-timeline: -12.800000000000011 -> -12.8
ab-testing-statistician: -24.200000000000003 -> -24.2
Root cause: Unrounded float arithmetic in production pipeline
Action: Rounded to 1 decimal place in all 7 rows
INCONSISTENT TOTAL_EVENTS (1 row)
ab-testing-statistician: total_events=14 but spawns(4)+improves(3)+evals(6)=13
Root cause: Off-by-one counting error in event aggregation
Action: Corrected to 13
JUDGE SCORE > FINAL SCORE (6 rows) -- informational, not a bug
3d-data-terrain-explorer: judge=91.0 > final=90.2
activity-feed-designer: judge=93.0 > final=84.6
adaptive-metric-layout: judge=90.0 > final=87.2
aesthetic-style-composer: judge=92.0 > final=86.8
agent-promotion-evaluator: judge=93.0 > final=90.2
ab-testing-statistician: judge=72.0 > final=68.0
accessibility-auditor: judge=65.0 > final=51.0
Explanation: final_score is a composite (usefulness+judge weighted?), not equal to judge_score alone. Expected behavior.
Needs manual review: 2 items
NEGATIVE IMPROVEMENT
agent-lifecycle-timeline: improvement=-12.8
ab-testing-statistician: improvement=-24.2
accessibility-auditor: improvement=-37.0
These may be valid (agent regressed between generations) or indicate a calculation bug.
If improvents can be negative, this is correct. If improvement is expected to always be non-negative, the calculation formula needs auditing.
SPAWNS=0 BUT IMPROVES=2
accessibility-auditor: spawns=0 but improves=2
Cannot auto-fix. Two scenarios:
(a) spawns field was miscounted (should be >=2)
(b) improves was miscounted (should be 0)
Either requires domain knowledge to resolve. Recommend checking the agent lifecycle pipeline for this blueprint.